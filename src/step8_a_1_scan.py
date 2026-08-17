"""Step 8, namespace `a`. STAGE 1 of 5 — episode-level scan to pair-level primitives.

GATE. Adopts nothing. Zero API calls: reads processed/step5/full_scan.npz (the Step 4 parsed
store, rescanned at Step 5 with the play `id`) and processed/step2/frame.csv only.

What this stage produces, and the rule each thing obeys:

  * Set-membership drop rule (Step 1 SS3.2): an episode record counts toward a season iff its
    `number` is a member of that season's listed set E. Records failing it are DROPPED and
    counted, per show and per pair. Never a numeric range 1..F. It is a COVERAGE COUNT and NOT
    an invariant (Human Lead ruling, decisions/0074): records examined and records dropped are
    reported; nothing is asserted.
  * The records-examined denominator is reported with its full decomposition and all THREE
    readings, each naming the pipeline that produces it. decisions/0083 SS1 CLOSES it: the
    readings are one family indexed by where D11 is applied, they differ by exactly the 167
    in-frame records D11 discards (94 S2-side, 73 S1-side), and every reading drops ZERO
    records, so nothing downstream reads the denominator. 0074 ruling 4's "publish both, not
    one" stands and is strengthened to three; its routing to Step 14 is withdrawn.
  * Dedup (Step 1 SS2.1/2.2): distinct (show, season, number) per user, canonical timestamp =
    the MINIMUM watched_at across its records; ties broken by episode number then smallest
    event id.
  * D11 (Step 1 SS0/10.0c): tau_pull = 2026-08-11T00:00:00Z is a global frozen cutoff and every
    record with watched_at >= tau_pull is discarded. The count discarded is a required Step 8
    output. Because the canonical timestamp of a distinct episode is the MINIMUM watched_at over
    its records, an episode survives D11 iff its canonical timestamp is < tau_pull -- so D11 is
    a predicate on the stored canonical timestamp and is applied downstream, per computation,
    rather than baked in here. It is applied to the liveness evidence (Human Lead ruling 2,
    decisions/0070) and to the action counts, and it is provably inert on A and A_H at every
    arm (D10 forces tau2 <= tau_pull). It is NOT applied to the S1-completion walk that sets
    waterfall line 1: decisions/0068 fixes line 1 at the PUBLISHED S1-completer population of
    220,107 and lists "whether D11 moves it" as an open question. Both are measured; the
    published base is what the chain uses.
  * Liveness evidence (decisions/0021): record INSERTION time, account-wide, read from the play
    `id` through the STORED Step 5 isotonic calibration. Conjunct (i) needs only the account's
    LAST insertion instant, and np.interp is monotone in rid, so the per-account max rid carries
    it. The calibration is NEVER refitted (decisions/0029).

Output: processed/step8/a/scan.npz, processed/step8/a/scan_summary.json,
        processed/step8/a/drops_per_show.csv
"""
import json
import os

import numpy as np
import pandas as pd

import step8_a_lib as lib

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step8/a")

NULL_TS = np.iinfo(np.int64).min
TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype("int64"))  # D11, decisions/0011
ACT_NAMES = {0: "watch", 1: "checkin", 2: "scrobble", -1: "other"}


def parse_set(s):
    return [int(x) for x in str(s).split(",") if x.strip().isdigit()]


def main():
    os.makedirs(OUT, exist_ok=True)
    frame = pd.read_csv(os.path.join(P2, "frame.csv"))
    show_ids = frame.show_trakt_id.astype(np.int64).to_numpy()
    assert np.unique(show_ids).size == show_ids.size == 1138

    # ---- listed episode-number sets E1, E2, as flat lookup tables -------------------------
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    e2 = {int(r.show_trakt_id): parse_set(r.s2_E) for r in frame.itertuples()}
    for sid in e1:
        assert len(e1[sid]) == len(set(e1[sid])) and len(e2[sid]) == len(set(e2[sid]))
    l1 = {k: len(v) for k, v in e1.items()}
    l2 = {k: len(v) for k, v in e2.items()}
    f1 = {k: max(v) for k, v in e1.items()}
    f2 = {k: max(v) for k, v in e2.items()}
    # L and F are derived FROM E and never independently (Step 1 SS3.1)
    assert all(l1[k] == int(frame.s1_L.iloc[i]) for i, k in
               enumerate(frame.show_trakt_id.astype(int)))
    assert all(l2[k] == int(frame.s2_L.iloc[i]) for i, k in
               enumerate(frame.show_trakt_id.astype(int)))

    show_slot = np.full(int(show_ids.max()) + 1, -1, dtype=np.int64)
    show_slot[show_ids] = np.arange(show_ids.size)
    maxnum = max(max(max(e1[k]), max(e2[k])) for k in e1)
    inE = np.zeros((show_ids.size, 2, maxnum + 1), dtype=bool)   # [slot, season-1, number]
    for i, sid in enumerate(show_ids):
        inE[i, 0, np.array(e1[int(sid)])] = True
        inE[i, 1, np.array(e2[int(sid)])] = True

    # ---- load the full record scan --------------------------------------------------------
    z = np.load(os.path.join(P5, "full_scan.npz"))
    user = z["user"].astype(np.int32)
    ts = z["ts"].astype(np.int64)
    rid = z["rid"].astype(np.int64)
    n_records = int(user.size)
    assert n_records == 27656813, f"unexpected record count {n_records}"

    ts_missing = ts == NULL_TS
    at_or_after_pull = (~ts_missing) & (ts >= TAU_PULL)
    usable = (~ts_missing) & (ts < TAU_PULL)

    # ---- liveness evidence: last insertion instant per account ---------------------------
    cal = np.load(os.path.join(P5, "calibration.npz"))
    knot_rid = cal["knot_rid"].astype(np.float64)
    knot_time = cal["knot_time"].astype(np.float64)
    assert np.all(np.diff(knot_rid) > 0) and np.all(np.diff(knot_time) >= 0)

    uids = np.unique(user)
    uslot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    uslot[uids] = np.arange(uids.size)
    us = uslot[user]

    max_rid_all = np.full(uids.size, -np.inf)
    np.maximum.at(max_rid_all, us, rid.astype(np.float64))
    max_rid_d11 = np.full(uids.size, -np.inf)
    np.maximum.at(max_rid_d11, us[usable], rid[usable].astype(np.float64))
    assert np.all(np.isfinite(max_rid_d11)), "an account has no record before tau_pull"
    last_inst_all = np.interp(max_rid_all, knot_rid, knot_time)
    last_inst_d11 = np.interp(max_rid_d11, knot_rid, knot_time)

    # ---- episode records on frame shows, seasons 1 and 2 ----------------------------------
    kind = z["kind"]
    show = z["show"].astype(np.int64)
    season = z["season"].astype(np.int32)
    number = z["number"].astype(np.int32)
    action = z["action"].astype(np.int8)
    del z

    is_ep = kind == 1
    in_frame = np.zeros(n_records, dtype=bool)
    ok_show = (show >= 0) & (show < show_slot.size)
    in_frame[ok_show] = show_slot[show[ok_show]] >= 0
    s12 = (season == 1) | (season == 2)
    s3plus = season >= 3

    # D4 evidence: S3-or-later episodes on frame shows, before tau_pull
    m_s3 = is_ep & in_frame & s3plus & usable
    s3_user = user[m_s3]
    s3_show = show[m_s3]

    base = is_ep & in_frame & s12
    n_base_records = int(base.sum())
    n_base_undated = int((base & ts_missing).sum())
    n_base_at_or_after_pull = int((base & at_or_after_pull).sum())

    # the records-examined denominator, decomposed. decisions/0083 SS1 closes it on exactly this
    # decomposition: three readings, one per placement of D11, all dropping zero records. Every
    # reading is emitted with the pipeline that produces it, as a COVERAGE FIGURE.
    _bu, _br = user[base].astype(np.int64), rid[base].astype(np.int64)
    _dupfree = int(np.unique(_bu * (10 ** 13) + (_br % (10 ** 13))).size)
    n_d11_s1 = int((base & at_or_after_pull & (season == 1)).sum())
    n_d11_s2 = int((base & at_or_after_pull & (season == 2)).sum())
    denom_variants = {
        "reported_by_this_instance": n_base_records,
        "reading_produced": "NO D11 -- every dated-or-undated in-frame S1/S2 episode record the "
                            "set-membership rule examines",
        "definition": "episode records (kind == episode) whose show is in the Step 2 frame and "
                      "whose season is 1 or 2, counted BEFORE the set-membership drop rule and "
                      "BEFORE D11",
        "undated_watched_at_null": n_base_undated,
        "discarded_by_D11_watched_at_ge_tau_pull": n_base_at_or_after_pull,
        "discarded_by_D11_S1_side": n_d11_s1,
        "discarded_by_D11_S2_side": n_d11_s2,
        "after_D11": int(n_base_records - n_base_undated - n_base_at_or_after_pull),
        "exact_duplicate_user_play_id_records": int(n_base_records - _dupfree),
        "records_with_number_le_0": int((base & (number <= 0)).sum()),
        # THE THREE READINGS, each with the pipeline that produces it. decisions/0083 SS1 closes
        # the item on this decomposition; 0074 ruling 4's pair is strengthened to three and its
        # Step 14 routing is withdrawn. All three drop ZERO records.
        "three_readings": {
            "reading_A_no_D11": n_base_records,
            "reading_B_D11_on_the_S2_side_only": int(n_base_records - n_d11_s2),
            "reading_C_D11_on_both_sides": int(n_base_records - n_base_at_or_after_pull),
            "gap_A_minus_B": n_d11_s2,
            "gap_A_minus_C": n_base_at_or_after_pull,
            "pipelines": {
                "reading_A_no_D11": "the pipeline this instance runs (src/step8_a_run.py). D11 is "
                                    "applied to every computation on the timeline and NOT to this "
                                    "coverage count, because the set-membership rule reads only "
                                    "`number in E` and never reads watched_at",
                "reading_B_D11_on_the_S2_side_only": "D11 applied on the S2 side, the S1 side "
                                                     "carried at 0068's published line 1",
                "reading_C_D11_on_both_sides": "D11 applied on both sides; line 1 moves to "
                                               "220,103, which is 0068's own open item and is "
                                               "answered there, not here"},
        },
        "note": "CLOSED by decisions/0083 SS1, and it was never a divergence. The readings are "
                "one family indexed by WHERE D11 IS APPLIED: D11 discards 167 in-frame S1/S2 "
                "records, 94 on the S2 side and 73 on the S1 side, and that split is the whole of "
                "the difference. 6,065,704 is the no-D11 reading, 6,065,610 is D11 on the S2 side "
                "only, 6,065,537 is D11 on both. EVERY READING DROPS ZERO RECORDS, so the "
                "numerator is 0 three times over and nothing downstream reads the denominator. "
                "The other candidate axes are all zero and were measured, not assumed: undated "
                "records, exact duplicate (user, play id) records, and records with a "
                "non-positive number. This publishes as a COVERAGE FIGURE with its pipeline "
                "named, not as an open question.",
    }
    del _bu, _br

    # ---- set-membership drop rule ---------------------------------------------------------
    # built on every DATED in-frame S1/S2 record; the D11 cutoff is carried as a timestamp
    # predicate rather than applied here (see the module docstring)
    m = base & (~ts_missing)
    u_m = user[m]
    sh_m = show[m]
    se_m = season[m]
    nu_m = number[m]
    ts_m = ts[m]
    rid_m = rid[m]
    act_m = action[m]
    slot_m = show_slot[sh_m]

    valid_num = (nu_m >= 0) & (nu_m <= maxnum)
    keep = np.zeros(u_m.size, dtype=bool)
    keep[valid_num] = inE[slot_m[valid_num], se_m[valid_num] - 1, nu_m[valid_num]]
    n_dropped_records = int((~keep).sum())

    # per show: dropped episode records, and distinct dropped (season, number)
    drop_df = pd.DataFrame({"show_trakt_id": sh_m[~keep], "season": se_m[~keep],
                            "number": nu_m[~keep]})
    per_show_records = drop_df.groupby("show_trakt_id").size()
    per_show_distinct = drop_df.drop_duplicates().groupby("show_trakt_id").size()
    drops = pd.DataFrame({"dropped_records": per_show_records,
                          "distinct_dropped_season_number": per_show_distinct}).fillna(0)
    drops = drops.astype(int).reindex(show_ids, fill_value=0)
    drops.index.name = "show_trakt_id"
    drops.to_csv(os.path.join(OUT, "drops_per_show.csv"))

    # pairs carrying at least one dropped S2 record (Step 1 SS3.4 count 2, first half)
    dropped_s2_pairs = np.unique(
        np.stack([u_m[(~keep) & (se_m == 2)].astype(np.int64),
                  sh_m[(~keep) & (se_m == 2)]], axis=1), axis=0)

    # ---- the pair universe: any in-E S1/S2 record on a frame show ------------------------
    u_k, sh_k, se_k, nu_k, ts_k, rid_k, act_k = (u_m[keep], sh_m[keep], se_m[keep], nu_m[keep],
                                                 ts_m[keep], rid_m[keep], act_m[keep])
    del u_m, sh_m, se_m, nu_m, ts_m, rid_m, act_m, m, base, keep, slot_m, valid_num

    pair_key = u_k.astype(np.int64) * (10 ** 9) + show_slot[sh_k]
    pairs, pair_idx = np.unique(pair_key, return_inverse=True)
    n_pairs = pairs.size
    pair_user = (pairs // (10 ** 9)).astype(np.int64)
    pair_show = show_ids[(pairs % (10 ** 9)).astype(np.int64)]

    # ---- dedup to distinct episodes -------------------------------------------------------
    order = np.lexsort((rid_k, ts_k, nu_k, se_k, pair_idx))
    p_o, se_o, nu_o, ts_o, rid_o, act_o = (pair_idx[order], se_k[order], nu_k[order],
                                           ts_k[order], rid_k[order], act_k[order])
    first = np.r_[True, (p_o[1:] != p_o[:-1]) | (se_o[1:] != se_o[:-1]) | (nu_o[1:] != nu_o[:-1])]
    ep_id = np.cumsum(first) - 1
    n_eps = int(ep_id[-1]) + 1
    d_pair = p_o[first]
    d_season = se_o[first]
    d_number = nu_o[first]
    d_ts = ts_o[first]          # canonical timestamp = min watched_at (sorted ascending)
    d_rid = rid_o[first]

    # per distinct episode: which action types produced it (bit 0 watch, 1 checkin,
    # 2 scrobble, 3 other) -- Step 13's action arm needs checkin-only / watch-only visible
    bit = np.where(act_o == 0, 1, np.where(act_o == 1, 2, np.where(act_o == 2, 4, 8))
                   ).astype(np.int8)
    d_mask = np.zeros(n_eps, dtype=np.int8)
    np.bitwise_or.at(d_mask, ep_id[ts_o < TAU_PULL], bit[ts_o < TAU_PULL])

    # per-pair record counts by action type, S1 and S2 separately (decisions/0070 ruling 4),
    # over records surviving D11
    act_counts = np.zeros((n_pairs, 2, 4), dtype=np.int32)
    acol = np.where(act_o == 0, 0, np.where(act_o == 1, 1, np.where(act_o == 2, 2, 3)))
    keep_o = ts_o < TAU_PULL
    np.add.at(act_counts, (p_o[keep_o], se_o[keep_o] - 1, acol[keep_o]), 1)

    # ---- CSR per pair, seasons separately, sorted by canonical timestamp -----------------
    def csr(sel):
        o = np.lexsort((d_rid[sel], d_number[sel], d_ts[sel], d_pair[sel]))
        pr = d_pair[sel][o]
        ptr = np.searchsorted(pr, np.arange(n_pairs + 1))
        return ptr, d_number[sel][o], d_ts[sel][o], d_mask[sel][o]

    s1_ptr, s1_num, s1_ts, _ = csr(d_season == 1)
    s2_ptr, s2_num, s2_ts, s2_mask = csr(d_season == 2)

    # prefix max of episode number within each pair's S2 run: with A subset E2 and
    # F2 = max(E2), "F2 in A" is exactly "max(A) == F2"
    s2_prefmax = np.maximum.accumulate(s2_num) if s2_num.size else s2_num.copy()
    for i in range(n_pairs):                      # reset the running max at each pair start
        a, b = s2_ptr[i], s2_ptr[i + 1]
        if b > a:
            s2_prefmax[a:b] = np.maximum.accumulate(s2_num[a:b])

    # ---- D4 flag and dropped-S2 flag on the pair universe ---------------------------------
    pk_s3 = s3_user.astype(np.int64) * (10 ** 9) + show_slot[s3_show]
    has_s3 = np.isin(pairs, np.unique(pk_s3))
    pk_ds2 = dropped_s2_pairs[:, 0] * (10 ** 9) + show_slot[dropped_s2_pairs[:, 1]]
    had_dropped_s2 = np.isin(pairs, np.unique(pk_ds2))

    np.savez_compressed(
        os.path.join(OUT, "scan.npz"),
        pair_user=pair_user, pair_show=pair_show,
        s1_ptr=s1_ptr, s1_num=s1_num, s1_ts=s1_ts,
        s2_ptr=s2_ptr, s2_num=s2_num, s2_ts=s2_ts, s2_mask=s2_mask, s2_prefmax=s2_prefmax,
        act_counts=act_counts, has_s3=has_s3, had_dropped_s2=had_dropped_s2,
        uids=uids, last_inst_d11=last_inst_d11, last_inst_all=last_inst_all,
        max_rid_d11=max_rid_d11, max_rid_all=max_rid_all,
    )

    # ---- B3(b): THE PER-SITE D11 TABLE, the record-level half ------------------------------
    # Human Lead ruling, decisions/0088 SS1, on Red Team's B3/F1, which blocked the gate on the
    # third and fourth passes. D11 is specified to apply "to EVERY computation", and this
    # instance named FIVE SITES IN PROSE WITH A COUNT AT NONE. Compliance was true and was
    # independently confirmed; what was missing is any MEASUREMENT of whether the mandate is
    # load-bearing on this data, and an unmeasured pass is indistinguishable from a check that
    # looked nowhere. The sites whose unit is a RECORD are counted here, at the point the records
    # exist; the sites whose unit is a distinct episode, an account or a coverage row are counted
    # in stage 5, and the table is assembled and ASSERTED AT EACH SITE there.
    d11_act = {}
    for s_ in (1, 2):
        for ai_, an_ in ((0, "watch"), (1, "checkin"), (2, "scrobble"), (3, "other")):
            sel_ = (se_o == s_) & (acol == ai_)
            d11_act[f"action_count_s{s_}_{an_}"] = {
                "unit": "in-frame in-E S1/S2 episode records",
                "records_examined_before_D11": int(sel_.sum()),
                "records_excluded_by_D11": int((sel_ & ~keep_o).sum()),
                "records_counted_after_D11": int((sel_ & keep_o).sum()),
                "D11_applied": True,
            }
    n_undated_all = int(ts_missing.sum())
    d11_sites_records = {
        "ruling": "Human Lead, decisions/0088 SS1(b): emit records excluded by D11 at EACH site "
                  "separately and ASSERT AT EACH SITE, not once and about the rest. Prose naming "
                  "five sites with a count at none is what this replaces.",
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "the_eight_action_count_sites": d11_act,
        "liveness_evidence": {
            "unit": "records, ALL kinds and ALL shows -- the insertion clock is account-wide",
            "records_examined_before_D11": n_records,
            "records_excluded_by_D11_watched_at_ge_tau_pull": int(at_or_after_pull.sum()),
            "records_excluded_as_undated": n_undated_all,
            "records_used_after_D11": int(usable.sum()),
            "accounts_whose_max_play_id_MOVES_under_D11": int((max_rid_d11 != max_rid_all).sum()),
            "accounts_whose_last_insertion_instant_MOVES_under_D11": int(
                (last_inst_d11 != last_inst_all).sum()),
            "D11_applied": True,
            "note": "Human Lead ruling 2, decisions/0070: the silence test's evidence is "
                    "restricted to records dated before tau_pull. This is the site that ruling "
                    "names, and it is the only site where D11 moves an input on this data.",
        },
        "S1_completion_walk": {
            # THE EXAMINED CELL HELD A DIFFERENT QUANTITY FROM THE OTHER TWELVE ROWS. Red Team
            # seventh pass, finding 5, against this arm. Every other site's "examined" column is
            # the count of units the site CONSUMES before D11; this row published 73, which is the
            # count of units D11 WOULD EXCLUDE -- and it is a RECORD count while the walk's unit is
            # a DISTINCT EPISODE. Three distinct objects sit behind this site (decisions/0089 SS1
            # names them) and they are now named apart, with `examined` the same kind of quantity
            # as in every other row.
            "unit": "DISTINCT S1 EPISODES -- the objects the first-pass walk actually consumes. "
                    "The walk runs over the per-pair CSR of distinct S1 episodes in canonical "
                    "timestamp order, not over raw records.",
            "episodes_examined_before_D11": int(s1_num.size),
            "episodes_at_or_after_tau_pull_that_D11_would_exclude": int(
                ((d_season == 1) & (d_ts >= TAU_PULL)).sum()),
            "THREE_OBJECTS_NAMED_APART": {
                "why": "Red Team seventh pass, finding 5. A single number under a single label "
                       "here is what put a would-exclude count in an examined column.",
                "record_level_in_frame_S1_records_at_or_after_tau_pull": n_d11_s1,
                "distinct_S1_episodes_touched_by_those_records": int(
                    np.unique(ep_id[(se_o == 1) & (ts_o >= TAU_PULL)]).size),
                "distinct_S1_episodes_whose_CANONICAL_instant_is_at_or_after_tau_pull": int(
                    ((d_season == 1) & (d_ts >= TAU_PULL)).sum()),
                "note": "the third is smaller than the second because an episode's canonical "
                        "instant is the MINIMUM watched_at over its records, so an episode with "
                        "one post-cutoff record and one earlier record stays pre-cutoff. Only the "
                        "third is what D11 would remove from this walk.",
            },
            "records_at_or_after_tau_pull_on_the_S1_side": n_d11_s1,
            "D11_applied": False,
            "why_not": "decisions/0068 fixes waterfall line 1 at the PUBLISHED S1-completer "
                       "population of 220,107 and lists 'whether D11 moves it' as an OPEN "
                       "question. This site is declared NOT-APPLIED rather than left unstated, "
                       "and the counterfactual is measured in stage 2: 4 pairs stop being "
                       "completers and 0 completion dates move.",
        },
        "in_frame_S1S2_records_at_or_after_tau_pull_total": n_base_at_or_after_pull,
        "of_which_S1_side": n_d11_s1,
        "of_which_S2_side": n_d11_s2,
    }

    summary = {
        "step": 8, "instance": "a", "stage": 1, "api_calls": 0,
        "build": lib.build_record(),
        "provenance_note": "EVERY COUNT IN THIS FILE WAS MEASURED ON BUILD " + lib.BUILD_TAG
                           + " (decisions/0079 B6, extending 0078).",
        "what": "episode-level scan to pair-level primitives. GATE: adopts nothing.",
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "records_total": n_records,
        "records_missing_watched_at": int(ts_missing.sum()),
        "records_discarded_watched_at_ge_tau_pull": int(at_or_after_pull.sum()),
        "in_frame_S1S2_episode_records": n_base_records,
        "record_denominator_reconciliation": denom_variants,
        "in_frame_S1S2_records_undated": n_base_undated,
        "in_frame_S1S2_records_discarded_by_D11": n_base_at_or_after_pull,
        "in_frame_S1S2_records_after_D11": int(n_base_records - n_base_undated
                                               - n_base_at_or_after_pull),
        "dropped_by_set_membership_records": n_dropped_records,
        "dropped_by_set_membership_distinct_season_number": int(drop_df.drop_duplicates()
                                                                .shape[0]),
        "shows_with_any_drop": int((drops.dropped_records > 0).sum()),
        "pairs_with_at_least_one_dropped_S2_record": int(dropped_s2_pairs.shape[0]),
        "pair_universe_any_inE_S1S2_record": int(n_pairs),
        "pair_universe_any_inE_S1S2_record_after_D11": int(
            np.unique(p_o[ts_o < TAU_PULL]).size),
        "distinct_episodes": n_eps,
        "distinct_S1_episodes": int(s1_num.size),
        "distinct_S2_episodes": int(s2_num.size),
        "distinct_episodes_whose_canonical_ts_ge_tau_pull": int((d_ts >= TAU_PULL).sum()),
        "distinct_S2_episodes_whose_canonical_ts_ge_tau_pull": int(
            ((d_season == 2) & (d_ts >= TAU_PULL)).sum()),
        "distinct_S1_episodes_whose_canonical_ts_ge_tau_pull": int(
            ((d_season == 1) & (d_ts >= TAU_PULL)).sum()),
        "D11_per_site_records": d11_sites_records,
        "action_record_counts_in_frame_S1S2_kept_after_D11": {
            ACT_NAMES[k]: int(v) for k, v in
            zip([0, 1, 2, -1], [int(((act_o == 0) & keep_o).sum()),
                                int(((act_o == 1) & keep_o).sum()),
                                int(((act_o == 2) & keep_o).sum()),
                                int(((act_o < 0) & keep_o).sum())])},
        "calibration": {
            "source": "processed/step5/calibration.npz (STORED, never refitted)",
            "knots": int(knot_rid.size),
            "time_range_utc": [str(np.datetime64(int(knot_time[0]), "s")),
                               str(np.datetime64(int(knot_time[-1]), "s"))],
            "accounts_max_rid_above_curve_D11": int((max_rid_d11 > knot_rid[-1]).sum()),
            "accounts_whose_max_rid_moves_under_D11": int((max_rid_d11 != max_rid_all).sum()),
            "last_instant_max_utc_D11": str(np.datetime64(int(last_inst_d11.max()), "s")),
            "last_instant_max_utc_unrestricted": str(np.datetime64(int(last_inst_all.max()),
                                                                   "s")),
        },
        "accounts": int(uids.size),
        "pairs_with_S3_or_later_evidence": int(has_s3.sum()),
    }
    with open(os.path.join(OUT, "scan_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
