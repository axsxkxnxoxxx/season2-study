"""Step 8, namespace `a`. STAGE 2 of 5 — the S1 completion walk, the clock, and positions 1-5.

GATE. Adopts nothing. Zero API calls.

Filter order is EXACTLY decisions/0029, and the per-filter sample size is the thing that does
not commute, so each position is measured on the previous position's output:

  1 Step 2 frame  ->  2 L2 = 1 exclusion  ->  3 S1 completion rule  ->  4 contamination (Step 5)
  ->  5 right-censoring  ->  6 liveness (stage 3)  ->  7 outcome assignment (stage 3)

WATERFALL LINE 1 IS THE S1-COMPLETER POPULATION, 220,107 PAIRS (decisions/0068). Lines 2 and 3
follow from it. This stage recomputes the S1 completion test and the first-pass S1 completion
DATE independently from the episode records -- not read back from any stored pair table -- which
is what gives the Step 8 clock-start invariant its force (Step 1 SS5, task-sheet Step 8).

Both populations are carried from here on (decisions/0070 ruling 1):
  APPLY = Step 5 waterfall line 1 less D10 = 196,654   (what position 6 filters)
  DERIV = Step 5 waterfall line 4 less D10 = 147,370   (requires S2 evidence)

POSITION 3's DROP SET IS RETAINED AS A SIDE OUTPUT (Human Lead ruling, decisions/0075). D9 half
(b) is measured on the rows the S1 completion rule REMOVES, so it cannot be computed without
them, and they are not recoverable from the analysis table. Note the shape of it on this frame:
waterfall line 1 is already the S1-COMPLETER population (0068), so position 3 removes 0 rows FROM
THE WATERFALL, while the S1 completion rule removes 58,345 pairs from the pair universe. The side
output is the latter -- the rows the rule deletes -- because that is the set half (b) needs. A
zero here would read as a data finding rather than a missing input, which is why it is a file.

Output: processed/step8/a/positions.npz, processed/step8/a/positions.json,
        processed/step8/a/position3_dropset.npz
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P2 = os.path.join(ROOT, "processed/step2")
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step8/a")

TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype("int64"))
DAY = 86400
W = 108                      # decisions/0026
H = 91                       # D10
BACKFILL_D = 180.0           # Step 5 constants, used to rebuild its published waterfall
POSTDATE_D = -30.0
PUBLISHED_STEP5_WATERFALL = [201900, 178165, 155131, 152126, 128099]


def floor_day(x):
    return (np.asarray(x, dtype=np.int64) // DAY) * DAY


def s1_completion(ptr, num, ts, pair_show, F1, need, upper=None):
    """First-pass S1 completion per Step 1 SS4/SS5(b), walking distinct episodes in canonical
    timestamp order. Returns (complete, completion_ts). `upper` optionally truncates the walk to
    episodes strictly before that instant (used to measure the D11 counterfactual)."""
    n = ptr.size - 1
    complete = np.zeros(n, dtype=bool)
    comp_ts = np.full(n, np.iinfo(np.int64).min, dtype=np.int64)
    for i in range(n):
        a, b = ptr[i], ptr[i + 1]
        if upper is not None:
            b = a + int(np.searchsorted(ts[a:b], upper, side="left"))
        if b - a < need[i]:
            continue
        hit = np.flatnonzero(num[a:b] == F1[i])
        if hit.size == 0:
            continue
        k = max(int(hit[0]), int(need[i]) - 1)
        complete[i] = True
        comp_ts[i] = ts[a + k]
    return complete, comp_ts


def main():
    z = np.load(os.path.join(OUT, "scan.npz"))
    pair_user = z["pair_user"]
    pair_show = z["pair_show"]
    s1_ptr, s1_num, s1_ts = z["s1_ptr"], z["s1_num"], z["s1_ts"]
    n_pairs = pair_user.size

    frame = pd.read_csv(os.path.join(P2, "frame.csv")).set_index("show_trakt_id")
    L1 = frame.s1_L.reindex(pair_show).to_numpy().astype(np.int64)
    F1 = frame.s1_F.reindex(pair_show).to_numpy().astype(np.int64)
    L2 = frame.s2_L.reindex(pair_show).to_numpy().astype(np.int64)
    need1 = np.ceil(0.90 * L1).astype(np.int64)
    fin2 = pd.to_datetime(frame.s2_finale_date.reindex(pair_show), utc=True)
    fin2_epoch = floor_day(fin2.to_numpy().astype("datetime64[s]").astype(np.int64))
    assert not np.isnan(fin2_epoch).any()

    # ---- position 3's rule, computed independently ---------------------------------------
    complete, comp_ts = s1_completion(s1_ptr, s1_num, s1_ts, pair_show, F1, need1)
    complete_d11, comp_ts_d11 = s1_completion(s1_ptr, s1_num, s1_ts, pair_show, F1, need1,
                                              upper=TAU_PULL)
    s1_date = floor_day(np.where(complete, comp_ts, 0))

    # ---- the clock (Step 1 SS6): T0 = max(S2 finale, first-pass S1 completion) ------------
    t0 = np.maximum(fin2_epoch, s1_date)
    binds_fin = complete & (fin2_epoch > s1_date)
    binds_s1 = complete & (s1_date > fin2_epoch)
    binds_both = complete & (fin2_epoch == s1_date)

    # ---- cross-check against the stored Step 5 pair table (NOT read back into the clock) --
    p5 = pd.read_csv(os.path.join(P5, "pair_revision5.csv"),
                     usecols=["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate",
                              "t0_contaminated", "complete_rec_lag_days", "first_s2_lag_days",
                              "first_s2_airdate", "first_s2_corrupt", "t0", "s1_completion_date",
                              "binds"])
    show_codes, show_uniq = pd.factorize(pair_show)
    key_mine = pair_user.astype(np.int64) * (10 ** 7) + show_codes
    p5_codes = pd.Index(show_uniq).get_indexer(p5.show_trakt_id.to_numpy())
    assert (p5_codes >= 0).all(), "a Step 5 pair sits on a show absent from my universe"
    key_p5 = p5.user_idx.to_numpy().astype(np.int64) * (10 ** 7) + p5_codes
    pos = pd.Index(key_mine).get_indexer(key_p5)
    assert (pos >= 0).all(), "a Step 5 pair is absent from my pair universe"

    mine_completers = int(complete.sum())
    p5_set = np.zeros(n_pairs, dtype=bool)
    p5_set[pos] = True
    agree = int((p5_set == complete).sum())
    only_mine = int((complete & ~p5_set).sum())
    only_p5 = int((p5_set & ~complete).sum())

    def to_epoch(series):
        # the stored table writes a year-1 date as "1-01-01"; pandas' mixed parser reads that
        # as 2001-01-01, so pad the year before parsing or the comparison invents a mismatch
        s = series.astype(str).str.replace(r"^(\d{1,3})-", lambda m: f"{int(m.group(1)):04d}-",
                                           regex=True)
        v = pd.to_datetime(s, utc=True, errors="coerce", format="mixed")
        bad = v.isna().to_numpy()
        e = np.zeros(len(v), dtype=np.int64)
        e[~bad] = floor_day(v[~bad].to_numpy().astype("datetime64[s]").astype(np.int64))
        return e, bad

    p5_s1date, bad_s1 = to_epoch(p5.s1_completion_date)
    p5_t0, bad_t0 = to_epoch(p5.t0)
    s1_date_mismatch = int(((s1_date[pos] != p5_s1date) & ~bad_s1).sum())
    t0_mismatch = int(((t0[pos] != p5_t0) & ~bad_t0).sum())
    n_unparseable_stored_dates = int(bad_s1.sum()), int(bad_t0.sum())

    # ---- Step 5 contamination masks, rebuilt from the stored flags and asserted ----------
    has_s2 = (p5.s2_ev_n > 0).to_numpy()
    t0c = p5.t0_contaminated.to_numpy().astype(bool)
    postd = (p5.complete_rec_lag_days < POSTDATE_D).to_numpy()
    all_air = has_s2 & (p5.s2_ev_airdate.to_numpy() == p5.s2_ev_n.to_numpy())
    the1542 = t0c & ~has_s2
    fs2_bad = has_s2 & ((p5.first_s2_lag_days.to_numpy() > BACKFILL_D)
                        | (p5.first_s2_airdate.to_numpy() == 1)
                        | (p5.first_s2_corrupt.to_numpy() == 1))
    w1 = ~(all_air | the1542)
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    computed = [int(x.sum()) for x in (w1, w2, w3, w4, w5)]
    assert computed == PUBLISHED_STEP5_WATERFALL, f"Step 5 waterfall mismatch: {computed}"

    keep_contam = np.zeros(n_pairs, dtype=bool)          # Step 8 position 4, APPLY depth
    keep_contam[pos] = w1
    deriv_contam = np.zeros(n_pairs, dtype=bool)         # DERIV depth: Step 5 line 4
    deriv_contam[pos] = w4
    p5_has_s2 = np.zeros(n_pairs, dtype=bool)
    p5_has_s2[pos] = has_s2

    # ---- positions ------------------------------------------------------------------------
    pos1 = complete.copy()                                # Step 2 frame, S1-completer base
    pos2 = pos1 & (L2 != 1)                               # L2 = 1 exclusion
    pos3 = pos2 & complete                                # S1 completion rule
    pos4 = pos3 & keep_contam
    pos4_deriv = pos3 & deriv_contam

    need_cens = (max(W, 91) + H) * DAY
    keep_d10 = (t0 + need_cens) <= TAU_PULL
    keep_term1 = (t0 + max(W, 91) * DAY) <= TAU_PULL      # the max(W, 91) term alone
    pos5 = pos4 & keep_d10
    pos5_deriv = pos4_deriv & keep_d10

    removed_term1 = int((pos4 & ~keep_term1).sum())
    removed_incremental_H = int((pos4 & keep_term1 & ~keep_d10).sum())
    removed_term1_d = int((pos4_deriv & ~keep_term1).sum())
    removed_incremental_H_d = int((pos4_deriv & keep_term1 & ~keep_d10).sum())

    assert int(pos1.sum()) == 220107, f"line 1 is {int(pos1.sum())}, expected 220,107"
    assert int(pos4.sum()) == 201900, f"position 4 is {int(pos4.sum())}"
    assert int(pos4_deriv.sum()) == 152126, f"position 4 (DERIV depth) is {int(pos4_deriv.sum())}"
    assert int(pos5.sum()) == 196654, f"APPLY is {int(pos5.sum())}, expected 196,654"
    assert int(pos5_deriv.sum()) == 147370, f"DERIV is {int(pos5_deriv.sum())}"
    assert int((pos5_deriv & ~pos5).sum()) == 0, "DERIV must be a subset of APPLY"

    # ---- position 3's drop set, retained as a side output (decisions/0075) -----------------
    dropped3 = ~complete
    np.savez_compressed(
        os.path.join(OUT, "position3_dropset.npz"),
        row=np.flatnonzero(dropped3).astype(np.int64),
        pair_user=pair_user[dropped3], pair_show=pair_show[dropped3],
        n_distinct_s1_episodes=np.diff(s1_ptr)[dropped3].astype(np.int32),
        L1=L1[dropped3], F1=F1[dropped3], need1=need1[dropped3],
    )

    np.savez_compressed(
        os.path.join(OUT, "positions.npz"),
        complete=complete, complete_d11=complete_d11, comp_ts=comp_ts, s1_date=s1_date,
        t0=t0, fin2_epoch=fin2_epoch, binds_fin=binds_fin, binds_s1=binds_s1,
        binds_both=binds_both, L1=L1, F1=F1, L2=L2, need1=need1,
        pos1=pos1, pos2=pos2, pos3=pos3, pos4=pos4, pos4_deriv=pos4_deriv,
        pos5=pos5, pos5_deriv=pos5_deriv, keep_d10=keep_d10, keep_term1=keep_term1,
        p5_row=pos, p5_has_s2=p5_has_s2,
    )

    out = {
        "step": 8, "instance": "a", "stage": 2, "api_calls": 0,
        "W_days": W, "H_days": H, "tau_pull_utc": "2026-08-11T00:00:00Z",
        "filter_order": ["1 Step 2 frame", "2 L2 = 1 exclusion", "3 S1 completion rule",
                         "4 contamination exclusion (Step 5)", "5 right-censoring",
                         "6 liveness (stage 3)", "7 outcome assignment (stage 3)"],
        "waterfall_APPLY": {
            "position_1_step2_frame": int(pos1.sum()),
            "position_2_L2_eq_1_excluded": int(pos2.sum()),
            "position_3_S1_completion_rule": int(pos3.sum()),
            "position_4_contamination": int(pos4.sum()),
            "position_5_right_censoring": int(pos5.sum()),
        },
        "waterfall_DERIV": {
            "position_1_step2_frame": int(pos1.sum()),
            "position_2_L2_eq_1_excluded": int(pos2.sum()),
            "position_3_S1_completion_rule": int(pos3.sum()),
            "position_4_contamination_DERIV_depth": int(pos4_deriv.sum()),
            "position_5_right_censoring": int(pos5_deriv.sum()),
        },
        "removed_at_each_position_APPLY": {
            "position_2_L2_eq_1": int(pos1.sum() - pos2.sum()),
            "position_3_S1_completion": int(pos2.sum() - pos3.sum()),
            "position_4_contamination": int(pos3.sum() - pos4.sum()),
            "position_5_right_censoring": int(pos4.sum() - pos5.sum()),
        },
        "right_censoring_two_lines_APPLY": {
            "removed_by_max_W_91_term": removed_term1,
            "removed_incrementally_by_the_plus_H_term": removed_incremental_H,
            "total": removed_term1 + removed_incremental_H,
            "direction_on_the_headline": "UP -- both lines remove recent S1 completers, who are "
                                         "disproportionately likely to roll straight into S2 "
                                         "(Step 1 SS6)",
        },
        "right_censoring_two_lines_DERIV": {
            "removed_by_max_W_91_term": removed_term1_d,
            "removed_incrementally_by_the_plus_H_term": removed_incremental_H_d,
            "total": removed_term1_d + removed_incremental_H_d,
            "direction_on_the_headline": "UP -- same mechanism",
        },
        "step5_waterfall_rebuilt": computed,
        "step5_waterfall_published": PUBLISHED_STEP5_WATERFALL,
        "L2_eq_1_shows_in_frame": int((frame.s2_L == 1).sum()),
        "independent_S1_completion_check": {
            "what": "the S1 completion test and first-pass date recomputed from the episode "
                    "records, never read back from processed/step5/pair_revision5.csv",
            "pair_universe": int(n_pairs),
            "completers_recomputed": mine_completers,
            "completers_in_the_published_pair_table": int(p5_set.sum()),
            "agreement_on_membership_over_the_universe": agree,
            "completers_only_in_my_recomputation": only_mine,
            "completers_only_in_the_published_table": only_p5,
            "s1_completion_date_mismatches": s1_date_mismatch,
            "T0_mismatches": t0_mismatch,
            "stored_dates_unparseable_s1_then_t0": list(n_unparseable_stored_dates),
            "pairs_whose_S1_completion_date_is_a_corrupt_year_1_timestamp": int(
                (complete & (s1_date < 0)).sum()),
        },
        "D11_counterfactual_on_position_3": {
            "note": "decisions/0068 fixes line 1 at the PUBLISHED 220,107 and lists this as an "
                    "OPEN question; it is measured, not applied",
            "completers_with_D11_applied_to_the_S1_walk": int(complete_d11.sum()),
            "pairs_that_stop_being_completers_under_D11": int((complete & ~complete_d11).sum()),
            "completers_whose_completion_date_moves_under_D11": int(
                (complete & complete_d11 & (comp_ts != comp_ts_d11)).sum()),
        },
        "position_3_dropset_side_output": {
            "ruling": "decisions/0075: retained because D9 half (b) is measured on the rows "
                      "position 3 removes and no line of Step 8 said to keep them. An instance "
                      "that does not keep them emits zero or fails, and a zero here reads as a "
                      "DATA FINDING rather than a MISSING INPUT.",
            "file": "processed/step8/a/position3_dropset.npz",
            "rows_the_S1_completion_rule_removes_from_the_pair_universe": int(dropped3.sum()),
            "rows_position_3_removes_from_the_waterfall": int(pos2.sum() - pos3.sum()),
            "why_those_two_differ": "waterfall line 1 is already the S1-completer population "
                                    "(0068), so the waterfall figure is 0 by construction. The "
                                    "set half (b) needs is the rows the RULE deletes, which is "
                                    "the pair universe less the completers.",
            "pair_universe": int(n_pairs),
        },
        "T0_binding_term_three_ways_on_position_5_APPLY": {
            "S2_finale_binds": int((pos5 & binds_fin).sum()),
            "S1_completion_binds": int((pos5 & binds_s1).sum()),
            "both_bind": int((pos5 & binds_both).sum()),
        },
    }
    with open(os.path.join(OUT, "positions.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
