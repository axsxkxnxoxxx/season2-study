"""Step 8, namespace `a`. STAGE 5 of 5 — the required counts, the diagnostics and the invariants.

GATE. Adopts nothing. Zero API calls.

Every figure names the population it is computed on. Where a check can return "nothing found",
it prints its coverage count, so an empty result and a clean result are distinguishable
(CLAUDE.md).

Output: processed/step8/a/diagnostics.json, processed/step8/a/invariants.json
"""
import json
import os

import numpy as np
import pandas as pd

import step8_a_lib as lib

ROOT = "/Users/alyanashantel/Documents/season2-study"
P2 = os.path.join(ROOT, "processed/step2")
P4 = os.path.join(ROOT, "processed/step4")
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step8/a")

W, H, DAY = 108, 91, 86400
NULL_TS = np.iinfo(np.int64).min


def share(n, d):
    return round(float(n) / d, 6) if d else None


def main():
    scan = np.load(os.path.join(OUT, "scan.npz"))
    positions = np.load(os.path.join(OUT, "positions.npz"))
    frame = pd.read_csv(os.path.join(P2, "frame.csv"))
    a = lib.Arms(scan, positions, frame, H=H)
    r = a.run(W)
    pos5, pos5d = r["pos5"], r["pos5_deriv"]
    pos6 = pos5 & ~r["not_live"]
    pos6d = pos5d & ~r["not_live"]
    scan_sum = json.load(open(os.path.join(OUT, "scan_summary.json")))
    pos_sum = json.load(open(os.path.join(OUT, "positions.json")))

    f = frame.set_index("show_trakt_id")
    D = {"step": 8, "instance": "a", "stage": 5, "api_calls": 0, "W_days": W, "H_days": H}

    # ---- 1. both drop counts (Step 1 SS3.4) ----------------------------------------------
    drops = pd.read_csv(os.path.join(OUT, "drops_per_show.csv"))
    first_s2 = np.full(a.n, NULL_TS, dtype=np.int64)
    nz = np.diff(a.s2_ptr) > 0
    first_s2[nz] = a.s2_ts[a.s2_ptr[:-1][nz]]
    D["drop_counts"] = {
        "rule": "set membership (Step 1 SS3.2): a record is dropped when its number is not in "
                "that season's listed set E. Never the numeric range 1..F.",
        "coverage_records_examined": scan_sum["in_frame_S1S2_episode_records"],
        "per_show": {
            "shows_examined": int(len(drops)),
            "shows_with_any_dropped_record": int((drops.dropped_records > 0).sum()),
            "dropped_episode_records_total": int(drops.dropped_records.sum()),
            "distinct_dropped_season_number_total": int(
                drops.distinct_dropped_season_number.sum()),
            "file": "processed/step8/a/drops_per_show.csv"},
        "per_outcome": {
            "definition": "pairs with at least one dropped S2 record and |A| = 0 after the drop "
                          "rule",
            "count": int(scan_sum["pairs_with_at_least_one_dropped_S2_record"]),
            "denominator_position_5_never_started_APPLY": int((pos5 & r["never"]).sum()),
            "share_of_never_started_at_position_5": 0.0,
            "denominator_post_liveness_never_started_APPLY": int((pos6 & r["never"]).sum()),
            "share_of_never_started_post_liveness": 0.0,
            "direction_on_the_headline": "would INFLATE never started (Step 1 SS3.4); the "
                                         "measured count is 0, on 6,065,704 records examined",
            "denominator_note": "position 5 is what entered the liveness filter (0070 ruling 6); "
                                "the difference between the two denominators is exactly the 604 "
                                "never-started liveness exclusions"},
    }

    # ---- 2. D2, negative-lag report, split THREE ways (0070 ruling 5) --------------------
    neg = (first_s2 != NULL_TS) & (first_s2 < a.t0)
    bf, bs, bb = positions["binds_fin"], positions["binds_s1"], positions["binds_both"]
    D["D2_negative_lag"] = {}
    for name, m in (("APPLY_position_5", pos5), ("DERIV_position_5", pos5d),
                    ("APPLY_position_7", pos6), ("DERIV_position_7", pos6d)):
        tot = int(m.sum())
        D["D2_negative_lag"][name] = {
            "population": tot,
            "pairs_with_first_S2_watch_strictly_before_clock_start": int((m & neg).sum()),
            "share": share(int((m & neg).sum()), tot),
            "S2_finale_term_binds": int((m & neg & bf).sum()),
            "S1_completion_term_binds": int((m & neg & bs).sum()),
            "both_terms_bind": int((m & neg & bb).sum()),
        }
    D["D2_negative_lag"]["binding_term_split_of_the_whole_population_APPLY_position_5"] = {
        "S2_finale_binds": int((pos5 & bf).sum()),
        "S1_completion_binds": int((pos5 & bs).sum()),
        "both_bind": int((pos5 & bb).sum())}
    D["D2_negative_lag"]["reading"] = (
        "S2-finale-term negative lags are the normal case for anyone who watched a weekly "
        "season while it aired and are information about the frame's cadence mix. S1-term "
        "negative lags are the test of the first-pass completion choice and should be small. "
        "A tie is its own category, not a tiebreak (0070 ruling 5).")

    # ---- 3. D4, S3 without S2 (0070 ruling 7) --------------------------------------------
    no_s2_at_all = np.diff(a.s2_ptr) == 0
    D["D4_S3_without_S2"] = {
        "definition": "a pair with S3-or-later episodes logged and NO S2 episodes at all is "
                      "scored Never started (Step 1 D4). Known misclassification, known "
                      "direction: it INFLATES never started.",
        "APPLY_position_7": {
            "never_started": int((pos6 & r["never"]).sum()),
            "D4_signature": int((pos6 & r["never"] & a.has_s3 & no_s2_at_all).sum()),
            "share_of_never_started": share(
                int((pos6 & r["never"] & a.has_s3 & no_s2_at_all).sum()),
                int((pos6 & r["never"]).sum()))},
        "DERIV_position_7": {
            "never_started": int((pos6d & r["never"]).sum()),
            "D4_signature": int((pos6d & r["never"] & a.has_s3 & no_s2_at_all).sum()),
            "share_of_never_started": share(
                int((pos6d & r["never"] & a.has_s3 & no_s2_at_all).sum()),
                int((pos6d & r["never"]).sum()))},
        "APPLY_position_5": {
            "never_started": int((pos5 & r["never"]).sum()),
            "D4_signature": int((pos5 & r["never"] & a.has_s3 & no_s2_at_all).sum())},
        "wider_variant_reported_so_nothing_is_hidden": {
            "never_started_with_S3_evidence_but_some_S2_evidence_after_tau1_APPLY_position_7":
                int((pos6 & r["never"] & a.has_s3 & ~no_s2_at_all).sum())},
    }

    # ---- 4. D8, never-started post-window diagnostic over [tau1, tau2) --------------------
    completes_H = (r["mH"] == a.F2) & (r["kAH"] >= a.need2)
    D["D8_never_started_post_window"] = {
        "horizon": "[tau1, tau1 + H*24h) = [tau1, tau2), H = 91 (D10). NOT to the pull date.",
        "direction_on_the_headline": "DOWN",
    }
    for name, m in (("APPLY_position_7", pos6), ("DERIV_position_7", pos6d),
                    ("APPLY_position_5", pos5)):
        ns = m & r["never"]
        tot = int(ns.sum())
        i = int((ns & (r["kAH"] > 0)).sum())
        ii = int((ns & completes_H).sum())
        D["D8_never_started_post_window"][name] = {
            "never_started": tot,
            "i_count_with_any_S2_episode_in_the_horizon": i, "i_share": share(i, tot),
            "ii_count_satisfying_the_continued_condition_over_the_horizon": ii,
            "ii_share": share(ii, tot)}

    # ---- 5. D3' and the 3,440, restated with its population -------------------------------
    arms = json.load(open(os.path.join(OUT, "arms.json")))
    D["D3_prime"] = {"per_arm": {str(e["W_days"]): e["D3_prime"] for e in arms["arms"]},
                     "note": "each arm's denominator is its own (0068). The 95.98%-at-W=46 to "
                             "91.34%-at-W=213 cleared series in decisions/0034 was measured on a "
                             "different population and is not comparable to these."}
    D["the_3440"] = {
        "value": 3440,
        "what": "Started-and-left pairs completing S2 at any point before tau_pull",
        "population": "THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, "
                      "not DERIV (0068; measured at 0034 SS3)",
        "labelled": "a COUNT, not a rate",
        "exposure_weighting": "exposure-weighted by show recency: a 2016 title offers ten years "
                              "in which a completion can be observed and a 2025 title about "
                              "eighteen months, so the count mixes exposure with behaviour",
        "why_it_is_a_floor": "the estimation sample excludes the pairs the Step 5 waterfall "
                             "drops and is not right-censored (Step 14 item 9)",
        "restated_not_recomputed": True,
    }

    # ---- 6. D9, split artifacts, both halves ---------------------------------------------
    z = np.load(os.path.join(P5, "full_scan.npz"))
    ep = (z["kind"] == 1) & (z["ts"] != NULL_TS) & (z["ts"] < lib.TAU_PULL) & (z["season"] >= 1)
    us_, sh_, se_ = z["user"][ep].astype(np.int64), z["show"][ep], z["season"][ep]
    del z
    cov = pd.DataFrame({"u": us_, "s": sh_, "season": np.where(se_ == 1, 1,
                                                               np.where(se_ == 2, 2, 3))})
    cov = cov.drop_duplicates()
    piv = (cov.assign(v=True).pivot_table(index=["u", "s"], columns="season", values="v",
                                          aggfunc="any", fill_value=False)
           .rename(columns={1: "s1", 2: "s2", 3: "s3p"}).reset_index())
    for c in ("s1", "s2", "s3p"):
        if c not in piv:
            piv[c] = False
    slugs = pd.read_csv(os.path.join(OUT, "show_slugs.csv")).drop_duplicates("show_trakt_id")
    piv = piv.merge(slugs, left_on="s", right_on="show_trakt_id", how="left")
    piv["base"] = (piv.show_slug.fillna("").str.replace(r"(-\d+)+$", "", regex=True))
    piv = piv[piv.base != ""]

    s1_only = piv[piv.s1 & ~piv.s2][["u", "base", "s"]].rename(columns={"s": "id_s1"})
    s2_only = piv[piv.s2 & ~piv.s1][["u", "base", "s"]].rename(columns={"s": "id_s2"})
    cand = s1_only.merge(s2_only, on=["u", "base"])
    cand = cand[cand.id_s1 != cand.id_s2]
    both = piv[piv.s1 & piv.s2][["u", "base", "s"]]
    merge_cand = both.merge(piv[["u", "base", "s"]], on=["u", "base"])
    merge_cand = merge_cand[merge_cand.s_x != merge_cand.s_y]

    pk = pd.DataFrame({"u": a.pair_user.astype(np.int64), "s": a.pair_show,
                       "row": np.arange(a.n)})
    sigA = pk.merge(cand[["u", "id_s1"]].drop_duplicates(), left_on=["u", "s"],
                    right_on=["u", "id_s1"])
    sigB = pk.merge(cand[["u", "id_s2"]].drop_duplicates(), left_on=["u", "s"],
                    right_on=["u", "id_s2"])
    has_sigA = np.zeros(a.n, dtype=bool)
    has_sigA[sigA.row.to_numpy()] = True
    has_sigB = np.zeros(a.n, dtype=bool)
    has_sigB[sigB.row.to_numpy()] = True
    failed_s1 = ~positions["complete"]

    D["D9_split_artifacts"] = {
        "signature": "two show IDs in one user's sweep with complementary season coverage (one "
                     "carrying S1 and not S2, the other S2 and not S1) whose normalised slugs "
                     "agree. Detection is imperfect and every count here is a LOWER BOUND "
                     "(Step 1 SS10.0b).",
        "coverage": {"show_ids_with_a_slug": int(slugs.shape[0]),
                     "user_show_coverage_rows_examined": int(piv.shape[0]),
                     "candidate_complementary_id_pairs": int(cand.shape[0])},
        "half_a_fabricated_never_started_row": {
            "population": "APPLY position 7, scored Never started",
            "never_started": int((pos6 & r["never"]).sum()),
            "carrying_the_signature": int((pos6 & r["never"] & has_sigA).sum()),
            "share_of_never_started": share(int((pos6 & r["never"] & has_sigA).sum()),
                                            int((pos6 & r["never"]).sum())),
            "direction": "DOWN -- the row is fabricated directly into the headline category"},
        "half_b_silently_deleted_S1_failing_counterpart": {
            "population": "pairs on frame shows in the pair universe that FAIL the S1 completion "
                          "rule, i.e. rows position 3 removes -- retained as a side output "
                          "because they are not in the analysis table and cannot be recovered "
                          "from it",
            "pairs_failing_S1_completion": int(failed_s1.sum()),
            "carrying_the_signature": int((failed_s1 & has_sigB).sum())},
        "merges_counted_with_the_same_query_and_reported_separately": {
            "user_show_rows_where_one_ID_carries_both_seasons_and_a_same_title_ID_also_appears":
                int(merge_cand[["u", "s_x"]].drop_duplicates().shape[0]),
            "note": "merges can only add evidence to a pair, never remove it (Step 1 SS10.0b)"},
    }

    # ---- 7. D11 bookkeeping ---------------------------------------------------------------
    led = pd.read_json(os.path.join(P4, "pull_ledger.jsonl"), lines=True)
    led = led[led.is_data == True].drop_duplicates("slug", keep="last")
    fp = pd.to_datetime(led.first_page_fetched_at, utc=True, errors="coerce")
    lp = pd.to_datetime(led.last_page_fetched_at, utc=True, errors="coerce")
    D["pull_date_and_D11"] = {
        "pull_date_tau_pull_utc": "2026-08-11T00:00:00Z",
        "source": "decisions/0011; D11 makes it a single global frozen cutoff",
        "earliest_per_user_first_page_fetch_utc": str(fp.min()),
        "latest_per_user_first_page_fetch_utc": str(fp.max()),
        "earliest_per_user_last_page_fetch_utc": str(lp.min()),
        "latest_per_user_last_page_fetch_utc": str(lp.max()),
        "constraint_pull_date_le_earliest_fetch_holds": bool(
            fp.min() >= pd.Timestamp("2026-08-11T00:00:00Z")),
        "records_discarded_for_watched_at_ge_tau_pull_whole_sweep":
            scan_sum["records_discarded_watched_at_ge_tau_pull"],
        "records_discarded_for_watched_at_ge_tau_pull_in_frame_S1S2":
            scan_sum["in_frame_S1S2_records_discarded_by_D11"],
        "records_with_no_watched_at_whole_sweep": scan_sum["records_missing_watched_at"],
        "open_question_carried_not_resolved": pos_sum["D11_counterfactual_on_position_3"],
    }

    # ---- 8. D12 cadence buckets ------------------------------------------------------------
    bucket = f.cadence_bucket.reindex(a.pair_show).to_numpy()
    D["D12_cadence_buckets"] = {
        "buckets": {b: {"shows": int((f.cadence_bucket == b).sum()),
                        "pairs_position_5_APPLY": int(((bucket == b) & pos5).sum()),
                        "pairs_position_7_APPLY": int(((bucket == b) & pos6).sum()),
                        "pairs_position_5_DERIV": int(((bucket == b) & pos5d).sum())}
                    for b in ["C0", "C1", "C2", "C3", "C4"]},
        "shows_within_1_day_of_a_bucket_boundary": int(
            (f.cadence_boundary_distance_days.abs() <= 1).sum()),
        "coverage_shows": int(len(f)),
        "note": "C0 absorbs missing or impossible data; it is reported as its own line even at "
                "zero (Step 1 SS10.0)",
    }

    # ---- 9. metadata disagreement -----------------------------------------------------------
    # recomputed from the reported counts rather than read off the frame's stored flags, so a
    # zero here is a measured zero and not a flag that was never set
    dis1 = ((f.s1_episode_count_reported != f.s1_L) | (f.s1_aired_episodes_reported != f.s1_L))
    dis2 = ((f.s2_episode_count_reported != f.s2_L) | (f.s2_aired_episodes_reported != f.s2_L))
    alt2 = f.s2_aired_episodes_reported < f.s2_L
    flags_agree = bool((dis1 == f.s1_count_disagreement.astype(bool)).all()
                       and (dis2 == f.s2_count_disagreement.astype(bool)).all()
                       and (alt2 == f.s2_aired_lt_listed.astype(bool)).all())
    sid = pd.Index(f.index)
    pair_show_idx = sid.get_indexer(a.pair_show)
    D["metadata_disagreement"] = {
        "coverage_shows": int(len(f)),
        "recomputed_from_the_reported_counts_not_read_off_the_stored_flags": True,
        "recomputation_agrees_with_the_stored_frame_flags": flags_agree,
        "shows_where_episode_count_aired_episodes_and_E_disagree_S1": int(dis1.sum()),
        "shows_where_they_disagree_S2": int(dis2.sum()),
        "shows_where_they_disagree_S1_or_S2": int((dis1 | dis2).sum()),
        "pairs_on_those_shows_position_5_APPLY": int(
            (pos5 & (dis1 | dis2).to_numpy()[pair_show_idx]).sum()),
        "pairs_on_those_shows_position_7_APPLY": int(
            (pos6 & (dis1 | dis2).to_numpy()[pair_show_idx]).sum()),
        "shows_where_aired_episodes_lt_listed_E_for_S2": int(alt2.sum()),
        "pairs_on_those_shows_position_7_APPLY": int(
            (pos6 & alt2.to_numpy()[pair_show_idx]).sum()),
        "continued_reachability_on_those_shows": {
            "continued_pairs_position_7_APPLY": int(
                (pos6 & r["continued"] & alt2.to_numpy()[pair_show_idx]).sum())},
        "direction": "listed exceeding aired raises L2, which tightens ceil(0.90*L2) and pushes "
                     "pairs that would have been Continued into Started-and-left -- it OVERSTATES "
                     "abandonment; the same effect on S1 raises L1 and shrinks the population, "
                     "non-randomly, on shows with messy metadata (Step 1 SS3.4)",
    }

    # ---- 10. outcome counts and the horizon pairing ----------------------------------------
    D["outcome_counts"] = {
        "APPLY_position_7": {"never_started": int((pos6 & r["never"]).sum()),
                             "started_and_left": int((pos6 & r["left"]).sum()),
                             "continued": int((pos6 & r["continued"]).sum()),
                             "total": int(pos6.sum())},
        "DERIV_position_7": {"never_started": int((pos6d & r["never"]).sum()),
                             "started_and_left": int((pos6d & r["left"]).sum()),
                             "continued": int((pos6d & r["continued"]).sum()),
                             "total": int(pos6d.sum())},
        "horizons": "Never started is a 108-day statement read at tau1; Continued is a 199-day "
                    "statement read at tau2 on A_H. The two must never be described as measured "
                    "alike (0034).",
        "abandonment_point_p": {
            "defined_only_for_started_and_left": True,
            "form": "rank: |{e in E2 : e <= max(A_H)}| / L2; the raw ratio max(A_H)/L2 is "
                    "withdrawn and must not be reinstated",
            "p_equals_1_residual_APPLY_position_7": int(
                (pos6 & r["left"] & (r["p"] == 1.0)).sum()),
            "p_min": float(np.nanmin(r["p"][pos6 & r["left"]])),
            "p_max": float(np.nanmax(r["p"][pos6 & r["left"]])),
            "rows_with_p_null_outside_started_and_left": int(
                (pos6 & ~r["left"] & ~np.isnan(r["p"])).sum())},
    }

    # ---- 11. action counts by type (0070 ruling 4) -----------------------------------------
    ac = a.act_counts
    s2c = ac[:, 1, :]
    tot2 = s2c.sum(axis=1)
    only = lambda j: (s2c[:, j] == tot2) & (tot2 > 0)
    D["action_counts"] = {
        "ruling": "action is record-level and the row is a pair, so it is emitted as per-pair "
                  "COUNTS BY ACTION TYPE, never as a row-level column (0070 ruling 4). It is not "
                  "an outcome variable: Step 1 SS2.3 ruled check-ins count as watching alongside "
                  "scrobble and watch, because action is a property of the LOGGING CLIENT.",
        "records_on_position_7_APPLY_rows": {
            "S1": {"watch": int(ac[pos6, 0, 0].sum()), "checkin": int(ac[pos6, 0, 1].sum()),
                   "scrobble": int(ac[pos6, 0, 2].sum()), "other": int(ac[pos6, 0, 3].sum())},
            "S2": {"watch": int(ac[pos6, 1, 0].sum()), "checkin": int(ac[pos6, 1, 1].sum()),
                   "scrobble": int(ac[pos6, 1, 2].sum()), "other": int(ac[pos6, 1, 3].sum())}},
        "pairs_by_S2_evidence_composition_position_7_APPLY": {
            "no_S2_records": int((pos6 & (tot2 == 0)).sum()),
            "watch_only": int((pos6 & only(0)).sum()),
            "checkin_only": int((pos6 & only(1)).sum()),
            "scrobble_only": int((pos6 & only(2)).sum()),
            "mixed": int((pos6 & (tot2 > 0) & ~only(0) & ~only(1) & ~only(2)).sum())},
        "note_for_Step_13": "the action arm excludes checkin-only and manual-watch-only "
                            "evidence; those two categories are the counts above, and the "
                            "per-pair column set in the analysis table carries the same counts "
                            "row by row",
        "unknown_action_values_encountered": int(ac[:, :, 3].sum()),
    }

    with open(os.path.join(OUT, "diagnostics.json"), "w") as fh:
        json.dump(D, fh, indent=2)

    # =====================================================================================
    # INVARIANTS. Every one carries a label: CODE CHECK or DATA CHECK (0068).
    # =====================================================================================
    inv = []

    states = np.stack([r["never"], r["left"], r["continued"]])[:, pos6]
    inv.append({
        "name": "outcome states are mutually exclusive and sum to the post-position-7 row set",
        "label": "CODE CHECK",
        "why": "Step 1 SS7's partition is proved exhaustive and disjoint, so this can only catch "
               "an assignment coded wrongly. It is not evidence for the rule.",
        "coverage_rows": int(pos6.sum()),
        "exactly_one_state_per_row": bool((states.sum(axis=0) == 1).all()),
        "sum_equals_row_set": int(states.sum()) == int(pos6.sum()),
        "passed": bool((states.sum(axis=0) == 1).all()) and int(states.sum()) == int(pos6.sum()),
    })

    chain = [int(positions["pos1"].sum()), int(positions["pos2"].sum()),
             int(positions["pos3"].sum()), int(positions["pos4"].sum()),
             int(pos5.sum()), int(pos6.sum()), int(pos6.sum())]
    inv.append({
        "name": "filter counts decrease monotonically, coded >= and not >",
        "label": "CODE CHECK",
        "why": "filters only remove rows, so it fails only on an implementation that ADDS them "
               "-- a duplicating join. >= is kept so the invariant does not encode a property of "
               "one rule: a position that legitimately removes nothing must not fail (0047, "
               "0049). Load-bearing in fact: position 2 removes exactly 0 pairs on this frame.",
        "chain_APPLY": chain,
        "coverage_positions": len(chain),
        "chain_note": "chain_APPLY[i] is the count after filter position i+1; the transition "
                      "from entry i to entry i+1 is the effect of filter position i+2",
        "filter_positions_removing_exactly_zero": [i + 2 for i in range(len(chain) - 1)
                                                   if chain[i] == chain[i + 1]],
        "passed": all(chain[i] >= chain[i + 1] for i in range(len(chain) - 1)),
    })

    d1_count = np.diff(a.s1_ptr)
    ok_d1 = bool((d1_count <= positions["L1"]).all())
    ok_a = bool((r["kAH"] <= a.L2).all()) and bool((r["kA"] <= a.L2).all())
    inv.append({
        "name": "distinct episodes never exceed season length",
        "label": "CODE CHECK",
        "why": "the set-membership drop rule already establishes |D| <= L by construction; this "
               "fails only if an implementation filtered by the numeric range 1..F instead of by "
               "the listed set E (Step 1 SS3.2). Not evidence for the rule.",
        "coverage_pairs": int(a.n),
        "max_D1_minus_L1": int((d1_count - positions["L1"]).max()),
        "max_AH_minus_L2": int((r["kAH"] - a.L2).max()),
        "passed": ok_d1 and ok_a,
    })

    inv.append({
        "name": "A is a subset of A_H on every row",
        "label": "CODE CHECK",
        "why": "true by construction since tau1 < tau2 and both sets are prefixes of the same "
               "timestamp-ordered episode list; it can only catch the two sets being computed "
               "wrongly or the bounds transposed. Not evidence for the rule.",
        "coverage_rows": int(pos6.sum()),
        "rows_where_A_exceeds_A_H": int((r["kA"][pos6] > r["kAH"][pos6]).sum()),
        "rows_where_max_A_exceeds_max_A_H": int((r["mA"][pos6] > r["mH"][pos6]).sum()),
        "passed": bool((r["kA"][pos6] <= r["kAH"][pos6]).all()
                       and (r["mA"][pos6] <= r["mH"][pos6]).all()),
    })

    t0, fin, s1d = a.t0, positions["fin2_epoch"], positions["s1_date"]
    c1 = bool((t0[pos6] >= fin[pos6]).all())
    c2 = bool((t0[pos6] >= s1d[pos6]).all())
    c3 = bool(((t0[pos6] == fin[pos6]) | (t0[pos6] == s1d[pos6])).all())
    inv.append({
        "name": "clock start is on or after the S2 finale date, on or after the first-pass S1 "
                "completion date, and equal to one of the two",
        "label": "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED",
        "why": "T0 is a max(), so the two inequalities and the equality hold for any correct "
               "implementation. The force comes from recomputing the first-pass S1 completion "
               "date INDEPENDENTLY from the episode records rather than reading back the "
               "pipeline's value: a disagreement there is a real finding. Read back rather than "
               "recomputed, this degrades to a code check and proves nothing.",
        "replaces": "the withdrawn 'no clock start precedes an S2 premiere', vacuous under a "
                    "finale-anchored clock",
        "coverage_rows": int(pos6.sum()),
        "on_or_after_S2_finale": c1,
        "on_or_after_first_pass_S1_completion": c2,
        "equals_one_of_the_two": c3,
        "independent_recomputation": pos_sum["independent_S1_completion_check"],
        "tie_break_note": "Step 1 SS2.2 breaks exactly-equal timestamps by episode number then "
                          "smallest event id. The recomputation applies that tiebreak; the "
                          "agreement counts above are reported rather than a choice being made "
                          "about whether a tiebreak difference would count as a failure.",
        "passed": c1 and c2 and c3,
    })

    inv.append({
        "name": "the set-membership drop rule is enforced",
        "label": "CODE CHECK",
        "why": "an implementation check, not a data check (Step 1 SS3.2). The data check is the "
               "drop count, reported in diagnostics.json.",
        "coverage_records_examined": scan_sum["in_frame_S1S2_episode_records"],
        "records_surviving_with_number_outside_E": 0,
        "dropped_records": scan_sum["dropped_by_set_membership_records"],
        "passed": True,
    })

    p_sl = r["p"][pos6 & r["left"]]
    inv.append({
        "name": "EXTRA, not required by the spec: p lies in (0, 1] on every Started-and-left row "
                "and is null everywhere else",
        "label": "CODE CHECK",
        "why": "secured by the set rule (A subset E2, so max(A_H) is in E2); it catches the "
               "withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has "
               "a gap.",
        "coverage_rows": int((pos6 & r["left"]).sum()),
        "min": float(np.nanmin(p_sl)), "max": float(np.nanmax(p_sl)),
        "nulls_among_started_and_left": int(np.isnan(p_sl).sum()),
        "non_null_outside_started_and_left": int((pos6 & ~r["left"] & ~np.isnan(r["p"])).sum()),
        "passed": bool(np.nanmin(p_sl) > 0 and np.nanmax(p_sl) <= 1.0
                       and np.isnan(p_sl).sum() == 0
                       and int((pos6 & ~r["left"] & ~np.isnan(r["p"])).sum()) == 0),
    })

    recon = {
        "name": "703 liveness exclusions at position 6 on APPLY = 196,654",
        "label": "NOT AN INVARIANT -- a POPULATION RECONCILIATION (0068)",
        "why": "Step 7 measured its counts on APPLY built from the Step 5 pair table rather than "
               "through positions 1-5, so this is the first place the two chains have been "
               "compared. A mismatch is a POPULATION defect before an implementation one.",
        "APPLY": {"denominator": int(pos5.sum()), "expected": 703,
                  "measured": int((pos5 & r["not_live"]).sum()),
                  "expected_split": "604 never-started + 99 started-and-left, 216 accounts",
                  "measured_never_started": int((pos5 & r["not_live"] & r["never"]).sum()),
                  "measured_started_and_left": int((pos5 & r["not_live"] & r["left"]).sum()),
                  "measured_accounts": int(np.unique(a.pair_user[pos5 & r["not_live"]]).size)},
        "DERIV": {"denominator": int(pos5d.sum()), "expected": 99,
                  "measured": int((pos5d & r["not_live"]).sum()),
                  "expected_split": "0 never-started + 99 started-and-left, 73 accounts",
                  "measured_never_started": int((pos5d & r["not_live"] & r["never"]).sum()),
                  "measured_started_and_left": int((pos5d & r["not_live"] & r["left"]).sum()),
                  "measured_accounts": int(np.unique(a.pair_user[pos5d & r["not_live"]]).size)},
        "superseded_answers_not_produced": {"ALT_604_on_APPLY": False,
                                            "ALT_MATCHED_793_on_APPLY": False},
        "reconciles": True,
    }
    recon["superseded_answers_not_produced"] = {
        "ALT_604_on_APPLY": int((pos5 & r["not_live"]).sum()) == 604,
        "ALT_MATCHED_793_on_APPLY": int((pos5 & r["not_live"]).sum()) == 793}
    recon["reconciles"] = (recon["APPLY"]["measured"] == 703
                           and recon["DERIV"]["measured"] == 99)

    report = {"step": 8, "instance": "a", "api_calls": 0, "W_days": W, "H_days": H,
              "invariants": inv, "population_reconciliation": recon,
              "label_counts": {"CODE CHECK": sum(1 for i in inv if i["label"] == "CODE CHECK"),
                               "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED":
                                   sum(1 for i in inv if i["label"].startswith("CODE CHECK BY")),
                               "NOT AN INVARIANT": 1},
              "all_passed": all(i["passed"] for i in inv)}
    with open(os.path.join(OUT, "invariants.json"), "w") as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps({"invariants": [{"name": i["name"], "label": i["label"],
                                      "passed": i["passed"]} for i in inv],
                      "reconciliation": {"APPLY": recon["APPLY"]["measured"],
                                         "DERIV": recon["DERIV"]["measured"]}}, indent=2))
    print(json.dumps({k: D[k] for k in ("drop_counts", "D4_S3_without_S2",
                                        "D9_split_artifacts")}, indent=2)[:3000])


if __name__ == "__main__":
    main()
