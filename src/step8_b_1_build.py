"""Step 8 (instance b) -- stage 1: build the pair-level base from record level.

GATE. NOTHING IS ADOPTED HERE. Step 8 is a gate; this instance produces and stops.

READ ONLY. ZERO network calls. Reads processed/step5/full_scan.npz (the Step 5
record-level sweep, which carries the play `id`), processed/step2/frame.csv,
raw/step3/user_pool.jsonl, processed/step5/user_index.json.

What this stage does, and nothing else:

  * D11 (Step 1 Sec 0 / decisions/0011): tau_pull = 2026-08-11T00:00:00Z is a
    GLOBAL FROZEN CUTOFF and every record with watched_at >= tau_pull is
    discarded from EVERY computation. Both the with- and without-D11 S1
    completer counts are measured, because decisions/0068 rules line 1 = 220,107
    as published and records the D11 question as separately OPEN.
  * Set-membership drop rule (Step 1 Sec 3.2): an episode record counts toward a
    season iff its `number` is a MEMBER of that season's listed set E. Records
    with a missing season/number, or number not in E, are DROPPED and counted.
  * Distinct episodes, never play events (Step 1 Sec 2.1), dedup key
    (show, season, number) scoped to the user; canonical timestamp is the
    MINIMUM watched_at across the episode's records (Step 1 Sec 2.2).
  * First-pass S1 completion (Step 1 Sec 5 definition (b)), computed
    INDEPENDENTLY here -- it is not read back from any upstream table. That
    independence is what gives the Step 8 clock-start invariant its force.
  * T0 = max(S2 finale air date, first-pass S1 completion date), both bare UTC
    dates (Step 1 Sec 6, D1).
  * Per-pair S2 episode evidence in a form the two-instant outcome assignment
    reads: the distinct S2 episodes in E2 with their canonical instants, plus
    the running max episode number in instant order, so |A|, |A_H|, F2 in A_H
    and max(A_H) are all searchsorted lookups at any tau.
  * POSITION 3's DROP SET IS RETAINED AS A SIDE OUTPUT (decisions/0075 ruling 2,
    RESTATED by decisions/0077 Sec 2). Position 3 removes ZERO rows from the
    waterfall, because line 1 is already the S1-completer population (0068), so
    "position 3's drop set" named an empty set as first written. The restated
    set is THE PAIR UNIVERSE LESS THE COMPLETERS -- 58,345 pairs -- carrying each
    pair's distinct-episode counts and the show's threshold, which is what D9
    half (b) reads. It is NOT the set-membership drop rule, which is a different
    rule and deletes 0 records.

Out: processed/step8/b/base.npz, processed/step8/b/stage1.json,
     processed/step8/b/position3_drop_set.csv.gz  (side output, 0075)
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np
import pandas as pd

from step8_b_build_id import BUILD, provenance_block, stamp

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P2, P5 = ROOT / "processed" / "step2", ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step8" / "b"

TAU_PULL = 1786406400          # 2026-08-11T00:00:00Z, decisions/0011
DAY = 86400
NULL_TS = np.iinfo(np.int64).min


def parse_set(s) -> list[int]:
    return sorted({int(x) for x in str(s).split(",") if x.strip().lstrip("-").isdigit()})


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    prov: dict = {
        "instance": "analytics-engineer-b",
        "namespace": "b",
        "stage": 1,
        "api_calls": 0,
        "adopts": "nothing -- Step 8 is a GATE",
        "tau_pull": "2026-08-11T00:00:00Z",
        "provenance": provenance_block(),
    }

    # ------------------------------------------------------------------ frame
    frame = pd.read_csv(P2 / "frame.csv")
    frame = frame.sort_values("show_trakt_id").reset_index(drop=True)
    n_shows = len(frame)
    show_ids = frame.show_trakt_id.values.astype(np.int64)
    E1 = [parse_set(s) for s in frame.s1_E]
    E2 = [parse_set(s) for s in frame.s2_E]
    L1 = np.array([len(e) for e in E1], dtype=np.int64)
    L2 = np.array([len(e) for e in E2], dtype=np.int64)
    F1 = np.array([max(e) for e in E1], dtype=np.int64)
    F2 = np.array([max(e) for e in E2], dtype=np.int64)
    assert (L1 == frame.s1_L.values).all() and (L2 == frame.s2_L.values).all()
    assert (F1 == frame.s1_F.values).all() and (F2 == frame.s2_F.values).all()
    THR1 = np.ceil(0.90 * L1).astype(np.int64)
    THR2 = np.ceil(0.90 * L2).astype(np.int64)
    max_num = max(max(E1[i][-1], E2[i][-1]) for i in range(n_shows))
    assert max_num < 2000, max_num
    prov["frame"] = {
        "shows": n_shows,
        "L2_eq_1_shows": int((L2 == 1).sum()),
        "max_listed_episode_number": int(max_num),
        "E_L_F_derived_from_one_payload": True,
    }

    finale_mid = (pd.to_datetime(frame.s2_finale_date, utc=True)
                  .values.astype("datetime64[s]").astype(np.int64))
    assert (finale_mid % DAY == 0).all()

    # ---------------------------------------------------------------- records
    z = np.load(P5 / "full_scan.npz")
    r_user, r_rid, r_ts = z["user"], z["rid"], z["ts"]
    r_kind, r_action, r_show = z["kind"], z["action"], z["show"]
    r_season, r_number = z["season"], z["number"]
    n_rec = len(r_rid)

    d11_drop = r_ts >= TAU_PULL
    prov["D11"] = {
        "rule": "records with watched_at >= tau_pull are discarded from every computation",
        "records_in_sweep": int(n_rec),
        "records_discarded_watched_at_ge_tau_pull": int(d11_drop.sum()),
        "records_with_no_watched_at": int((r_ts == NULL_TS).sum()),
        "note_undated": ("a record with no watched_at is not >= tau_pull and is not "
                         "discarded by D11; none of them is an in-frame S1/S2 record"),
    }

    show_idx = np.searchsorted(show_ids, r_show)
    show_idx[show_idx >= n_shows] = 0
    in_frame_show = show_ids[show_idx] == r_show
    is_ep = r_kind == 1

    # ---- S3+ evidence on frame shows (for D4), and any-S2-record-at-all -----
    m_s3 = is_ep & in_frame_show & (r_season >= 3) & ~d11_drop
    m_s2_any = is_ep & in_frame_show & (r_season == 2) & ~d11_drop

    # ---- the S1/S2 record slice the drop rule applies to -------------------
    m12 = is_ep & in_frame_show & ((r_season == 1) | (r_season == 2))
    m12_pre = m12.copy()
    prov["records"] = {
        "in_frame_S1_S2_episode_records_before_D11": int(m12.sum()),
        "in_frame_S1_S2_episode_records_dropped_by_D11": int((m12 & d11_drop).sum()),
        "in_frame_S3plus_episode_records_after_D11": int(m_s3.sum()),
    }
    # D11 is applied to every computation. THE ONE EXCEPTION is the construction
    # of waterfall line 1, which decisions/0068 RULES at 220,107 AS PUBLISHED --
    # a value that needs the pairs whose first-pass S1 completion rests on a
    # record D11 discards. Those pairs are carried through positions 1-3 and
    # flagged; stage 2 verifies they are removed at position 5 under either
    # reading, so lines 4-7 do not move. S2 evidence is D11-filtered throughout.
    m12 = m12 & (~d11_drop | (r_season == 1))

    su = r_user[m12].astype(np.int64)
    ss = show_idx[m12].astype(np.int64)
    se = r_season[m12].astype(np.int64)
    sn = r_number[m12].astype(np.int64)
    st = r_ts[m12].astype(np.int64)
    sr = r_rid[m12].astype(np.int64)
    sa = r_action[m12].astype(np.int64)

    # ---- set-membership drop rule -----------------------------------------
    valid_codes = np.array(sorted(
        [(int(show_ids[i]) << 20) | (1 << 12) | e for i in range(n_shows) for e in E1[i]]
        + [(int(show_ids[i]) << 20) | (2 << 12) | e for i in range(n_shows) for e in E2[i]]
    ), dtype=np.int64)
    bad_num = (sn < 0) | (sn >= 4096)
    rec_code = np.where(bad_num, -1,
                        (show_ids[ss] << 20) | (se << 12) | np.clip(sn, 0, 4095))
    in_E = np.isin(rec_code, valid_codes) & ~bad_num
    pairs_examined_by_the_rule = int(len(np.unique(su * n_shows + ss)))
    prov["drop_rule"] = {
        "measured_on_build": BUILD,
        "pairs_examined": pairs_examined_by_the_rule,
        "pairs_examined_note": ("the coverage unit invariant 3 states alongside the record "
                                "count (decisions/0080 Sec 3, row 3): every pair the "
                                "set-membership rule examines, BOTH SEASONS"),
        "status": ("A COVERAGE COUNT, NOT AN INVARIANT (decisions/0074 ruling 3). Step 8's "
                   "own bullet calls it 'an implementation check, not a data check'. Records "
                   "examined and records dropped are REPORTED; nothing is asserted"),
        "rule": "number must be a MEMBER of the season's listed set E, else the record is dropped",
        "records_examined": int(len(sn)),
        "records_dropped": int((~in_E).sum()),
        "records_dropped_missing_season_or_number": int(bad_num.sum()),
        "coverage": "every in-frame S1/S2 episode record surviving D11 was tested",
        "denominator_note": {
            "what_this_instance_counts": ("in-frame S1/S2 episode records after D11 has been "
                                          "applied to the S2 side; the S1 side is carried "
                                          "unfiltered because decisions/0068 rules waterfall "
                                          "line 1 at 220,107 AS PUBLISHED and that value needs "
                                          "the 4 pairs whose completing record is post-cutoff"),
            "READING_A_no_D11_anywhere": int(m12_pre.sum()),
            "READING_B_D11_on_the_S2_side_only_THIS_INSTANCE": int(len(sn)),
            "READING_C_D11_on_both_seasons": int((m12_pre & ~d11_drop).sum()),
            "decomposition_of_the_full_D11_effect": {
                "records_D11_discards_on_the_S1_side": int((m12_pre & d11_drop
                                                            & (r_season == 1)).sum()),
                "records_D11_discards_on_the_S2_side": int((m12_pre & d11_drop
                                                            & (r_season == 2)).sum()),
                "total": int((m12_pre & d11_drop).sum()),
                "why_it_matters": ("decisions/0074 ruling 4 published the gap between the two "
                                   "arms as 94 records and routed it to Step 14 as reported-"
                                   "not-reconciled. The 94 is the S2-SIDE component alone. "
                                   "D11 applied everywhere moves the figure by the TOTAL, so "
                                   "the three readings are separated by two different "
                                   "quantities and the two-figure framing understates the "
                                   "spread"),
            },
            "what_decides_it": ("the denominator is a CONSEQUENCE of one choice and not an "
                                "independent question: whether D11 is applied to the S1 "
                                "completion walk. That is exactly the question decisions/0068 "
                                "records as OPEN when it rules line 1 at 220,107 as published. "
                                "Close that and the denominator closes with it: READING_C with "
                                "line 1 = 220,103, or READING_B with line 1 = 220,107"),
            "reported_unreconciled": ("decisions/0074 ruling 4 publishes 6,065,704 against "
                                      "6,065,610, both reporting 0 drops, and rules the "
                                      "difference REPORTED NOT RECONCILED. All three readings "
                                      "are stated here with their decomposition; this instance "
                                      "does not reconcile them, and nothing downstream depends "
                                      "on the denominator"),
        },
    }

    # per-show drop counts (records, and distinct (season, number) pairs)
    drop_rows = pd.DataFrame({
        "show_trakt_id": show_ids[ss[~in_E]],
        "season": se[~in_E],
        "number": sn[~in_E],
    })
    per_show_drop = pd.DataFrame({"show_trakt_id": show_ids})
    a = drop_rows.groupby("show_trakt_id").size().rename("dropped_records")
    b = (drop_rows.drop_duplicates(["show_trakt_id", "season", "number"])
         .groupby("show_trakt_id").size().rename("distinct_dropped_season_number"))
    per_show_drop = (per_show_drop.merge(a, on="show_trakt_id", how="left")
                     .merge(b, on="show_trakt_id", how="left").fillna(0))
    per_show_drop[["dropped_records", "distinct_dropped_season_number"]] = \
        per_show_drop[["dropped_records", "distinct_dropped_season_number"]].astype(int)
    per_show_drop.to_csv(OUT / "drop_counts_per_show.csv", index=False)

    # pairs that had at least one S2 record dropped (Step 1 Sec 3.4 second count)
    pair_code_all = su * n_shows + ss
    dropped_s2_pair = np.unique(pair_code_all[(~in_E) & (se == 2)])

    # actions on dropped records, so an unexpected action value is visible
    prov["drop_rule"]["dropped_records_by_action"] = {
        k: int(((~in_E) & (sa == v)).sum())
        for k, v in (("watch", 0), ("checkin", 1), ("scrobble", 2), ("other", -1))
    }

    su, ss, se, sn, st, sr, sa = (a[in_E] for a in (su, ss, se, sn, st, sr, sa))
    pair_code = su * n_shows + ss

    # ---- action counts per pair, on in-E records ---------------------------
    # `action` is RECORD-level and the row is a pair (0070 ruling 4), so what is
    # emitted is counts by action type, never one action per row.
    act_key = pair_code * 8 + (se - 1) * 4 + np.where(sa < 0, 3, sa)
    act_u, act_n = np.unique(act_key, return_counts=True)

    # ---- distinct episodes: canonical timestamp = MIN watched_at -----------
    ep_code = pair_code * 8192 + se * 4096 + sn
    order = np.lexsort((sr, st, ep_code))
    ep_s, st_s, sn_s, se_s, pc_s, sr_s = (a[order] for a in
                                          (ep_code, st, sn, se, pair_code, sr))
    first = np.r_[True, ep_s[1:] != ep_s[:-1]]
    d_pc, d_se, d_sn, d_ts, d_rid = (a[first] for a in (pc_s, se_s, sn_s, st_s, sr_s))
    prov["dedup"] = {
        "records_in_E": int(len(ep_code)),
        "distinct_episodes": int(first.sum()),
        "inflation_pct": 100.0 * (len(ep_code) - int(first.sum())) / len(ep_code),
    }
    del ep_code, order, ep_s, st_s, sn_s, se_s, pc_s, sr_s, first

    # =============================== S1: first-pass completion ==============
    m1 = d_se == 1
    p1, n1, t1, r1 = d_pc[m1], d_sn[m1], d_ts[m1], d_rid[m1]
    o = np.lexsort((r1, n1, t1, p1))          # (pair, ts, number, rid) ascending
    p1, n1, t1, r1 = p1[o], n1[o], t1[o], r1[o]
    grp_start = np.flatnonzero(np.r_[True, p1[1:] != p1[:-1]])
    grp_id = np.cumsum(np.r_[True, p1[1:] != p1[:-1]]) - 1
    rank = np.arange(len(p1)) - grp_start[grp_id] + 1        # 1-based distinct count
    n_grp = len(grp_start)
    s1_pair = p1[grp_start]
    s1_show_idx = (s1_pair % n_shows).astype(np.int64)
    s1_count = np.diff(np.r_[grp_start, len(p1)])

    is_fin = n1 == F1[(p1 % n_shows)]
    rank_fin = np.full(n_grp, -1, dtype=np.int64)
    rank_fin[grp_id[is_fin]] = rank[is_fin]                  # finale is one episode
    need = THR1[s1_show_idx]
    comp_rank = np.maximum(need, rank_fin)
    ok = (rank_fin > 0) & (s1_count >= need)
    comp_pos = grp_start + comp_rank - 1
    comp_ts = np.where(ok, t1[np.clip(comp_pos, 0, len(t1) - 1)], -1)
    # the completing record's own D11 status, per pair
    comp_uses_post_cutoff = np.zeros(n_grp, dtype=bool)
    idx_ok = np.flatnonzero(ok)
    comp_uses_post_cutoff[idx_ok] = t1[comp_pos[idx_ok]] >= TAU_PULL

    prov["s1_completion"] = {
        "rule": "F1 in D1 and |D1| >= ceil(0.90 * L1), first-pass (Step 1 Sec 4, Sec 5(b))",
        "pairs_with_any_in_E1_S1_evidence": int(n_grp),
        "S1_completer_pairs_line_1": int(ok.sum()),
        "computed": "INDEPENDENTLY from the record level; not read back from any table",
    }

    # ---- the same count WITH D11 applied to S1 too (decisions/0068: OPEN) ----
    prov["s1_completion"]["D11_open_question"] = _completers_with_d11(
        r_user, r_ts, r_kind, r_season, r_number, show_idx, in_frame_show,
        show_ids, n_shows, F1, THR1, valid_codes)
    prov["s1_completion"]["D11_open_question"]["pairs_whose_completing_record_is_post_cutoff"] = \
        int(comp_uses_post_cutoff.sum())

    comp_pair = s1_pair[ok]
    comp_ts_ok = comp_ts[ok]
    comp_date_mid = (comp_ts_ok // DAY) * DAY
    comp_show_idx = s1_show_idx[ok]
    t0_mid = np.maximum(finale_mid[comp_show_idx], comp_date_mid)
    binds = np.where(finale_mid[comp_show_idx] == comp_date_mid, "tie",
                     np.where(finale_mid[comp_show_idx] > comp_date_mid, "finale", "s1"))

    # =============================== S2 evidence ============================
    m2 = d_se == 2
    p2, n2, t2 = d_pc[m2], d_sn[m2], d_ts[m2]
    o = np.lexsort((n2, t2, p2))
    p2, n2, t2 = p2[o], n2[o], t2[o]
    s2_start = np.flatnonzero(np.r_[True, p2[1:] != p2[:-1]])
    s2_gid = np.cumsum(np.r_[True, p2[1:] != p2[:-1]]) - 1
    # running max episode number in instant order, reset at each pair
    runmax = _grouped_running_max(n2, s2_start)
    s2_pairs = p2[s2_start]
    s2_counts = np.diff(np.r_[s2_start, len(p2)])
    # canonical instant of episode F2 per pair (inf if never watched)
    is_f2 = n2 == F2[(p2 % n_shows)]
    f2_ts = np.full(len(s2_pairs), np.iinfo(np.int64).max, dtype=np.int64)
    # first occurrence in instant order is the canonical instant (episodes are distinct)
    f2_ts[s2_gid[is_f2]] = t2[is_f2]

    prov["s2_evidence"] = {
        "pairs_with_any_in_E2_S2_evidence": int(len(s2_pairs)),
        "distinct_in_E2_S2_episodes": int(len(p2)),
    }

    # ================= POSITION 3's DROP SET (decisions/0075 ruling 2) =======
    # The rows the S1 completion rule REMOVES. Two kinds, and BOTH are needed:
    #   * pairs carrying in-E1 S1 evidence that fails the rule;
    #   * pairs carrying in-E2 S2 evidence and NO in-E1 S1 evidence at all --
    #     these never appear in the S1 walk, and they are exactly D9 half (b),
    #     "the silently deleted S1-failing counterpart".
    all_ev_pairs = np.unique(d_pc)
    n_s1_dist = np.zeros(len(all_ev_pairs), dtype=np.int64)
    n_s2_dist = np.zeros(len(all_ev_pairs), dtype=np.int64)
    pos_all = np.searchsorted(all_ev_pairs, d_pc)
    np.add.at(n_s1_dist, pos_all[d_se == 1], 1)
    np.add.at(n_s2_dist, pos_all[d_se == 2], 1)
    is_completer = np.isin(all_ev_pairs, comp_pair)
    drop3 = ~is_completer
    d3_show_idx = (all_ev_pairs % n_shows).astype(np.int64)
    pd.DataFrame({
        "user_idx": all_ev_pairs[drop3] // n_shows,
        "show_trakt_id": show_ids[d3_show_idx[drop3]],
        "distinct_S1_episodes_in_E1": n_s1_dist[drop3],
        "distinct_S2_episodes_in_E2": n_s2_dist[drop3],
        "S1_threshold_ceil_0_90_L1": THR1[d3_show_idx[drop3]],
        "S1_finale_number": F1[d3_show_idx[drop3]],
    }).to_csv(OUT / "position3_drop_set.csv.gz", index=False, compression="gzip")
    prov["position3_drop_set"] = {
        "retained_because": ("decisions/0075 ruling 2 -- D9 half (b) is measured on the rows "
                             "position 3 REMOVES and cannot be computed without them"),
        "restated_by_0077": ("position 3 removes ZERO rows from the waterfall, so the ruling "
                             "as first written named an empty set. The restated set is THE "
                             "PAIR UNIVERSE LESS THE COMPLETERS, ruled at 58,345 PAIRS -- not "
                             "the set-membership drop rule, which is a different rule, deletes "
                             "0 RECORDS, and whose unit is records rather than pairs"),
        "ruled_count_58345": int(drop3.sum()) == 58_345,
        "ruled_figure_and_its_own_provenance": ("58,345 pairs -- POSITION-3 RULE, POSITION-5 "
                                                "BUILD OF 2026-08-13, reproduced independently "
                                                "by both arms (decisions/0078 Sec 2). This "
                                                "build reproduces it again; the ruled figure "
                                                "keeps the build it was ruled on and this "
                                                "measurement carries this one"),
        "deliverable": ("decisions/0079 Sec 1 -- a DELIVERABLE PRODUCED BY THE PIPELINE, named "
                        "in the deliverable list and written by the same run that writes the "
                        "table. Not a helper script's side file: D9 half (b) cannot be computed "
                        "without it and its absence returns 0 SILENTLY, which reads as a data "
                        "finding rather than an error"),
        "unit": "PAIRS",
        "file": "processed/step8/b/position3_drop_set.csv.gz",
        "in_frame_pairs_with_ANY_in_E_S1_or_S2_distinct_episode": int(len(all_ev_pairs)),
        "of_which_S1_completers_line_1": int(is_completer.sum()),
        "dropped_by_the_S1_completion_rule": int(drop3.sum()),
        "dropped_carrying_S1_evidence_that_fails_the_rule":
            int((drop3 & (n_s1_dist > 0)).sum()),
        "dropped_carrying_S2_evidence_and_NO_S1_evidence":
            int((drop3 & (n_s1_dist == 0) & (n_s2_dist > 0)).sum()),
        "dropped_carrying_S2_evidence_at_all": int((drop3 & (n_s2_dist > 0)).sum()),
        "note": ("under decisions/0068 waterfall line 1 IS the S1-completer population, so "
                 "position 3 removes 0 FROM THE WATERFALL. The rule's drop set is not empty; "
                 "it sits upstream of line 1 and is retained here rather than discarded"),
    }
    d9b_pairs = all_ev_pairs[drop3 & (n_s1_dist == 0) & (n_s2_dist > 0)]

    # =============================== assemble ===============================
    np.savez(
        OUT / "base.npz",
        n_shows=np.int64(n_shows),
        show_ids=show_ids, L1=L1, L2=L2, F1=F1, F2=F2, THR1=THR1, THR2=THR2,
        finale_mid=finale_mid,
        comp_pair=comp_pair, comp_ts=comp_ts_ok, comp_date_mid=comp_date_mid,
        t0_mid=t0_mid, binds=binds.astype("U6"),
        comp_uses_post_cutoff=comp_uses_post_cutoff[ok],
        s2_pairs=s2_pairs, s2_start=s2_start, s2_counts=s2_counts,
        s2_ts=t2, s2_num=n2, s2_runmax=runmax, f2_ts=f2_ts,
        all_s1_pairs=s1_pair, all_s1_is_completer=ok,
        dropped_s2_pair=dropped_s2_pair,
        pos3_drop_pairs=all_ev_pairs[drop3],
        pos3_drop_s2_only_pairs=d9b_pairs,
        all_ev_pairs=all_ev_pairs, all_ev_n_s1=n_s1_dist, all_ev_n_s2=n_s2_dist,
        s3_pairs=np.unique(r_user[m_s3].astype(np.int64) * n_shows + show_idx[m_s3]),
        s2_any_rec_pairs=np.unique(r_user[m_s2_any].astype(np.int64) * n_shows
                                   + show_idx[m_s2_any]),
        act_key=act_u, act_n=act_n,
    )

    # decisions/0079 Sec 2 -- EVERY count group carries the build it was measured on.
    for v in prov.values():
        if isinstance(v, dict):
            stamp(v)

    prov["elapsed_s"] = time.time() - t0
    (OUT / "stage1.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


def _grouped_running_max(vals: np.ndarray, starts: np.ndarray) -> np.ndarray:
    out = np.empty_like(vals)
    ends = np.r_[starts[1:], len(vals)]
    for a, b in zip(starts, ends):
        out[a:b] = np.maximum.accumulate(vals[a:b])
    return out


def _completers_with_d11(r_user, r_ts, r_kind, r_season, r_number, show_idx,
                         in_frame_show, show_ids, n_shows, F1, THR1,
                         valid_codes) -> dict:
    """The S1-completer count with D11 applied to S1 records too."""
    m = (r_kind == 1) & in_frame_show & (r_season == 1) & (r_ts < TAU_PULL)
    su = r_user[m].astype(np.int64)
    ss = show_idx[m].astype(np.int64)
    sn = r_number[m].astype(np.int64)
    st = r_ts[m].astype(np.int64)
    bad = (sn < 0) | (sn >= 4096)
    code = np.where(bad, -1, (show_ids[ss] << 20) | (1 << 12) | np.clip(sn, 0, 4095))
    keep = np.isin(code, valid_codes) & ~bad
    su, ss, sn, st = su[keep], ss[keep], sn[keep], st[keep]
    pc = su * n_shows + ss
    ep = pc * 8192 + 4096 + sn
    o = np.lexsort((st, ep))
    ep, st, sn, pc = ep[o], st[o], sn[o], pc[o]
    first = np.r_[True, ep[1:] != ep[:-1]]
    pc, st, sn = pc[first], st[first], sn[first]
    o = np.lexsort((sn, st, pc))
    pc, st, sn = pc[o], st[o], sn[o]
    starts = np.flatnonzero(np.r_[True, pc[1:] != pc[:-1]])
    gid = np.cumsum(np.r_[True, pc[1:] != pc[:-1]]) - 1
    rank = np.arange(len(pc)) - starts[gid] + 1
    cnt = np.diff(np.r_[starts, len(pc)])
    sidx = (pc[starts] % n_shows)
    isf = sn == F1[pc % n_shows]
    rf = np.full(len(starts), -1, dtype=np.int64)
    rf[gid[isf]] = rank[isf]
    ok = (rf > 0) & (cnt >= THR1[sidx])
    return {
        "S1_completer_pairs_if_D11_applied_to_S1_too": int(ok.sum()),
        "published_line_1": 220107,
        "note": ("decisions/0068 rules line 1 = 220,107 AS PUBLISHED and records "
                 "whether D11 moves it as a SEPARATE OPEN QUESTION"),
    }


if __name__ == "__main__":
    main()
