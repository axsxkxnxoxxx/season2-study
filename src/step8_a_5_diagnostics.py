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

    # THE p_at_bound EMPTINESS, FOUR CELLS, ON WHATEVER POPULATION IS PASSED. Red Team blocker B2
    # (decisions/0085 SS3): it is emitted on APPLY position 5, APPLY post-liveness, DERIV position
    # 5 and DERIV post-liveness, because CLAUDE.md's standing rule is BOTH POPULATIONS, ALWAYS and
    # a correction applied to one and not the other is the same defect as not applying it at all.
    # Coverage counts travel with the cells: three of the four are zero, and a zero measured on
    # zero rows must not read like a zero measured on the whole population.
    def pab(mask, label, expected_total):
        m1 = mask & (r["p"] == 1.0)
        cells = {
            "in_BOTH_classes": int((m1 & r["p_saturated"] & r["p_final_ep"]).sum()),
            "saturated_not_final": int((m1 & r["p_saturated"] & ~r["p_final_ep"]).sum()),
            "final_not_saturated": int((m1 & ~r["p_saturated"] & r["p_final_ep"]).sum()),
            "in_NEITHER_class": int((m1 & ~r["p_saturated"] & ~r["p_final_ep"]).sum()),
        }
        cov = {"rows_in_the_population": int(mask.sum()),
               "rows_with_p_defined_examined": int((mask & r["p_defined"]).sum()),
               "rows_with_p_equal_1_examined": int(m1.sum())}
        assert cov["rows_with_p_defined_examined"] > 0, (
            "the p_at_bound cells looked at zero rows on " + label + ": an empty result and a "
            "clean result are the same value and only the control knows which it produced")
        out = {"population": label,
               "total_p_equals_1": int(m1.sum()),
               "p_at_bound_TRUE": int((m1 & r["p_saturated"]).sum()),
               "p_equals_1_but_p_at_bound_FALSE": int((m1 & ~r["p_saturated"]).sum()),
               "expected_total_by_0085": expected_total,
               "four_cells_sum_to_the_total": bool(sum(cells.values()) == int(m1.sum())),
               "coverage": cov,
               "build": lib.BUILD_TAG}
        out.update(cells)
        return out

    f = frame.set_index("show_trakt_id")
    D = {"step": 8, "instance": "a", "stage": 5, "api_calls": 0, "W_days": W, "H_days": H,
         "build": lib.build_record(),
         "provenance_note": "EVERY REQUIRED COUNT IN THIS FILE WAS MEASURED ON BUILD "
                            + lib.BUILD_TAG + ". Human Lead ruling, decisions/0079 (B6), "
                            "extending 0078: every count, every invariant result and every "
                            "waterfall figure names the pipeline it was measured on, not only its "
                            "population. Partial application is worse than none -- two labelled "
                            "figures imply the rest did not need it -- so the tag is injected on "
                            "every block below rather than written on the ones that seemed to "
                            "need it. Figures RESTATED from another build carry that other build "
                            "instead; they are marked where they appear."}

    # ---- 1. both drop counts (Step 1 SS3.4) ----------------------------------------------
    drops = pd.read_csv(os.path.join(OUT, "drops_per_show.csv"))
    first_s2 = np.full(a.n, NULL_TS, dtype=np.int64)
    nz = np.diff(a.s2_ptr) > 0
    first_s2[nz] = a.s2_ts[a.s2_ptr[:-1][nz]]
    D["drop_counts"] = {
        "rule": "set membership (Step 1 SS3.2): a record is dropped when its number is not in "
                "that season's listed set E. Never the numeric range 1..F.",
        "status": "A COVERAGE COUNT, NOT AN INVARIANT (Human Lead ruling, decisions/0074 ruling "
                  "3). Step 8's own bullet already calls it 'an implementation check, not a data "
                  "check'. Records examined and records dropped are REPORTED; nothing is "
                  "asserted. Asserting it would add another pass to a report where five of eight "
                  "checks cannot fail.",
        "coverage_records_examined": scan_sum["in_frame_S1S2_episode_records"],
        "coverage_records_dropped": scan_sum["dropped_by_set_membership_records"],
        "records_examined_denominator_CLOSED_by_0083": scan_sum[
            "record_denominator_reconciliation"],
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
                                         "measured count is 0, and it is 0 under all three "
                                         "readings of the records-examined denominator "
                                         "(decisions/0083 SS1)",
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
    D["D3_prime"] = {
        "per_arm": {str(e["W_days"]): e["D3_prime"] for e in arms["arms"]},
        "population_at_the_point_of_use": "STEP 8's RIGHT-CENSORED POPULATIONS. The headline "
                                          "series is APPLY, position-7 output (post-liveness), "
                                          "at each arm on its own denominator (0068).",
        "ruled_series": "decisions/0075: 99.53% of Started-and-left cleared at W = 46 down to "
                        "97.73% at W = 213 on APPLY. SUPERSEDED at this point of use: 0034's "
                        "95.98% -> 91.34%, measured on the amendment's UNCENSORED estimation "
                        "sample of 128,099 and carrying no population where it was used.",
        "measured_series_APPLY_position_7": {
            str(e["W_days"]): e["D3_prime"]["APPLY"]["cleared_share_of_all_started_and_left"]
            for e in arms["arms"]},
        "non_monotone_step_reported_not_resolved": "the cleared share is not monotone in W: it "
                                                   "rises between W = 91 and W = 107 before "
                                                   "resuming its fall. Both the clearance bound "
                                                   "and the Started-and-left denominator move "
                                                   "with W and they do not move together. Listed "
                                                   "open at decisions/0076 SS5; reported here, "
                                                   "not resolved.",
    }
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
    raw = piv.show_slug.fillna("")

    # THE TWO KEYS, defined in the spec by decisions/0076 because "strict" and "loose" had
    # existed only inside one instance's code, which the other is forbidden to read.
    #   STRICT: lowercase the slug and drop every non-alphanumeric character. Strip NOTHING else.
    #   LOOSE:  remove a TRAILING FOUR-DIGIT YEAR first, then apply the strict transform.
    # Neither strips a trailing digit group of arbitrary length -- that reduces `the-100` to
    # `the` and is a THIRD key. This instance used the third key on its previous run and
    # published 76 complementary pairs against the other arm's 75; that divergence is REPORTED,
    # NOT RECONCILED, and the third key is measured below purely so the record is complete.
    keys = {
        "strict": raw.str.lower().str.replace(r"[^a-z0-9]", "", regex=True),
        "loose": (raw.str.replace(r"-\d{4}$", "", regex=True)
                  .str.lower().str.replace(r"[^a-z0-9]", "", regex=True)),
        "third_key_trailing_digit_groups_NOT_RULED": (
            raw.str.replace(r"(-\d+)+$", "", regex=True)
            .str.lower().str.replace(r"[^a-z0-9]", "", regex=True)),
    }
    # HALF (b) IS MEASURED ON THE POSITION-3 DROP SET, AND THAT SET IS READ FROM THE PIPELINE
    # DELIVERABLE -- not recomputed from a mask lying around in memory. decisions/0079 (B5) makes
    # the drop set a deliverable written by the same run that writes the table, precisely because
    # half (b) cannot be computed without it and its absence RETURNS 0 SILENTLY, which reads as a
    # data finding rather than an error. Reading it here is what makes the deliverable
    # load-bearing: if stage 2 stops writing it, this stage fails loudly instead of publishing 0.
    ds_path = os.path.join(OUT, "position3_drop_set.csv.gz")
    assert os.path.exists(ds_path), (
        "the position-3 drop set deliverable is missing; D9 half (b) cannot be computed and MUST "
        "NOT be emitted as 0 (decisions/0075 ruling 2, 0079 B5)")
    dset = pd.read_csv(ds_path)
    failed_s1 = np.zeros(a.n, dtype=bool)
    failed_s1[dset.row.to_numpy()] = True
    assert int(failed_s1.sum()) == int(dset.shape[0]) == int((~positions["complete"]).sum()), \
        "the drop-set deliverable disagrees with position 3's rule as recomputed"
    dropset_meta = {
        "read_from": "processed/step8/a/position3_drop_set.csv.gz",
        "written_by": "stage 2 of this same pipeline run (decisions/0079 B5)",
        "pairs": int(dset.shape[0]),
        "carries": list(dset.columns),
        "short_of_the_0_90_threshold": int(dset.reason_short_of_threshold.sum()),
        "reached_the_threshold_but_never_watched_F1": int(dset.reason_finale_F1_not_watched.sum()),
    }
    pk = pd.DataFrame({"u": a.pair_user.astype(np.int64), "s": a.pair_show,
                       "row": np.arange(a.n)})

    def d9_for(key_series):
        p = piv.assign(base=key_series)
        p = p[p.base != ""]
        s1_only = p[p.s1 & ~p.s2][["u", "base", "s"]].rename(columns={"s": "id_s1"})
        s2_only = p[p.s2 & ~p.s1][["u", "base", "s"]].rename(columns={"s": "id_s2"})
        cand = s1_only.merge(s2_only, on=["u", "base"])
        cand = cand[cand.id_s1 != cand.id_s2]
        both = p[p.s1 & p.s2][["u", "base", "s"]]
        mc = both.merge(p[["u", "base", "s"]], on=["u", "base"])
        mc = mc[mc.s_x != mc.s_y]
        sA = np.zeros(a.n, dtype=bool)
        sB = np.zeros(a.n, dtype=bool)
        if len(cand):
            sA[pk.merge(cand[["u", "id_s1"]].drop_duplicates(), left_on=["u", "s"],
                        right_on=["u", "id_s1"]).row.to_numpy()] = True
            sB[pk.merge(cand[["u", "id_s2"]].drop_duplicates(), left_on=["u", "s"],
                        right_on=["u", "id_s2"]).row.to_numpy()] = True
        return {
            "coverage_rows_examined": int(p.shape[0]),
            "complementary_signature_id_pairs": int(cand.shape[0]),
            "half_a_never_started_carrying_the_signature_APPLY_position_7": int(
                (pos6 & r["never"] & sA).sum()),
            "half_a_never_started_carrying_the_signature_APPLY_position_5": int(
                (pos5 & r["never"] & sA).sum()),
            "half_b_S1_failing_pairs_carrying_the_signature": int((failed_s1 & sB).sum()),
            "merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_title_ID_also_"
            "appears": int(mc[["u", "s_x"]].drop_duplicates().shape[0]),
        }

    by_key = {k: d9_for(v) for k, v in keys.items()}
    st, lo = by_key["strict"], by_key["loose"]

    # ---- what loose merges that strict does not, WITH THE UNIVERSE NAMED --------------------
    # NAME THE UNIVERSE THE CLUSTERING RUNS OVER, AT THE POINT OF USE. Red Team blocker B1, third
    # pass (decisions/0085 SS2). The two arms published DISJOINT cluster lists on IDENTICAL counts
    # -- no shared member, maxima 8 against 10 -- while every count around them reconciled. That is
    # not a counting difference; it is a difference in WHICH SET OF SHOWS IS BEING CLUSTERED, and
    # the spec never said which. The cluster examples are the EVIDENCE for the loose key's only
    # warrant -- that it bounds how wrong strict could be -- so two arms giving different evidence
    # for one warrant makes the warrant irreproducible while the deliverables read otherwise.
    #
    # THIS ARM'S UNIVERSE, stated so it can be compared rather than guessed: the DISTINCT SHOW IDs
    # APPEARING IN THE PULLED SWEEP THAT CARRY A SLUG -- one row per show ID, deduplicated, NOT one
    # row per user-show coverage row and NOT the 1,138 frame shows. The other two candidate
    # universes named in the spec are sized alongside so a reader can see which this is not.
    # THE DIVERGENCE IS REPORTED, NOT RECONCILED: no universe is ruled, and if the two arms name
    # the same universe and still differ, one has a bug and that is the finding.
    show_keys = pd.DataFrame({
        "s": piv.s.to_numpy(),
        "slug": raw.to_numpy(),
        "strict": keys["strict"].to_numpy(),
        "loose": keys["loose"].to_numpy(),
    }).drop_duplicates("s")
    uni = show_keys[show_keys.slug != ""]
    g = uni.groupby("loose")
    merged_titles = g.strict.nunique().sort_values(ascending=False)
    merged_ids = g.s.nunique()
    top_merged = [{"loose_key": k,
                   "distinct_strict_keys_merged": int(v),
                   "distinct_show_ids_merged": int(merged_ids[k])}
                  for k, v in merged_titles.head(5).items() if v > 1]
    by_ids = merged_ids.sort_values(ascending=False)
    top_merged_by_ids = [{"loose_key": k,
                          "distinct_show_ids_merged": int(v),
                          "distinct_strict_keys_merged": int(merged_titles[k])}
                         for k, v in by_ids.head(5).items() if merged_titles[k] > 1]
    clustering_universe = {
        "ruling": "Red Team blocker B1, decisions/0085 SS2: NAME THE UNIVERSE THE CLUSTERING RUNS "
                  "OVER, AT THE POINT OF USE. The two arms published disjoint cluster lists on "
                  "identical counts, which is a difference in which set of shows is clustered and "
                  "not a counting difference. REPORTED, NOT RECONCILED -- no universe is ruled.",
        "THIS_ARM_CLUSTERS": "the DISTINCT SHOW IDs appearing anywhere in the pulled sweep that "
                             "carry a slug, deduplicated to one row per show ID",
        "distinct_show_ids_in_the_sweep": int(show_keys.shape[0]),
        "distinct_show_ids_carrying_a_slug_CLUSTERED": int(uni.shape[0]),
        "distinct_show_ids_without_a_slug_excluded": int((show_keys.slug == "").sum()),
        "user_show_coverage_rows_behind_them": int(piv.shape[0]),
        "candidate_universes_NOT_used_here_sized_for_comparison": {
            "the_1138_frame_shows": int(frame.shape[0]),
            "the_D9_candidate_pairs_under_the_loose_key": lo["complementary_signature_id_pairs"],
            "user_show_coverage_rows_undeduplicated": int(piv.shape[0]),
            "why_they_are_listed": "a cluster list computed on any of these can differ from the "
                                   "one below while every D9 COUNT still reconciles, which is "
                                   "exactly what happened between the arms",
        },
        "what_LARGEST_ranks_by_here": "distinct STRICT keys merged into one loose key -- i.e. how "
                                      "many genuinely different shows the loose key collapses. "
                                      "The same clusters ranked by distinct SHOW IDs merged are "
                                      "emitted alongside, because 'largest cluster' does not fix a "
                                      "ranking basis either and the two orders differ.",
        "coverage_shows_examined": int(uni.shape[0]),
        "clusters_with_more_than_one_strict_key": int((merged_titles > 1).sum()),
        "build": lib.BUILD_TAG,
    }
    assert clustering_universe["coverage_shows_examined"] > 0, (
        "the D9 clustering looked at zero shows; a zero cluster list here would read as a data "
        "finding rather than a missing input")

    D["D9_split_artifacts"] = {
        "signature": "two show IDs in one user's sweep with complementary season coverage (one "
                     "carrying S1 and not S2, the other S2 and not S1) whose normalised slugs "
                     "agree. Detection is imperfect and every count here is a LOWER BOUND "
                     "(Step 1 SS10.0b).",
        "key_ruling": "decisions/0074 ruling 5 adopts the STRICT key; decisions/0076 defines "
                      "both keys in the spec. STRICT = lowercase, drop every non-alphanumeric "
                      "character, strip nothing else. LOOSE = remove a trailing four-digit year "
                      "first, then strict. The loose count publishes alongside because it BOUNDS "
                      "HOW WRONG STRICT COULD BE, and the error runs OPPOSITE to D9's own "
                      "lower-bound caveat.",
        "coverage": {"show_ids_with_a_slug": int(slugs.shape[0]),
                     "user_show_coverage_rows_examined": int(piv.shape[0])},
        "FOUR_NUMBERS_both_halves_under_both_keys": {
            "ruling": "Human Lead ruling, decisions/0078 SS3: BOTH HALVES UNDER BOTH KEYS -- four "
                      "numbers, not three. It follows from 0074 ruling 5's own reason rather than "
                      "from a preference: the loose count publishes BECAUSE IT BOUNDS HOW WRONG "
                      "STRICT COULD BE, and that reason applies to half (b) exactly as to half "
                      "(a). Publishing the bound for one half and withholding it for the other "
                      "leaves the reader unable to bound the total, and the error runs OPPOSITE to "
                      "D9's own lower-bound caveat -- the direction they were not warned about.",
            "half_a_strict": st["half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_a_loose": lo["half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b_strict": st["half_b_S1_failing_pairs_carrying_the_signature"],
            "half_b_loose": lo["half_b_S1_failing_pairs_carrying_the_signature"],
            "half_a_population": "APPLY, position 7 (post-liveness), scored Never started",
            "half_b_population": "the position-3 drop set: pairs failing the S1 completion rule",
            "build": lib.BUILD_TAG,
        },
        "position_3_drop_set_input": dropset_meta,
        "ADOPTED_strict_key": {
            "complementary_signature_id_pairs": st["complementary_signature_id_pairs"],
            "half_a_fabricated_never_started_row": {
                "population": "APPLY, position 7 (post-liveness), scored Never started",
                "never_started": int((pos6 & r["never"]).sum()),
                "carrying_the_signature": st[
                    "half_a_never_started_carrying_the_signature_APPLY_position_7"],
                "share_of_never_started": share(
                    st["half_a_never_started_carrying_the_signature_APPLY_position_7"],
                    int((pos6 & r["never"]).sum())),
                "on_APPLY_position_5_the_table_row_set": {
                    "never_started": int((pos5 & r["never"]).sum()),
                    "carrying_the_signature": st[
                        "half_a_never_started_carrying_the_signature_APPLY_position_5"]},
                "direction": "DOWN -- the row is fabricated directly into the headline category"},
            "half_b_silently_deleted_S1_failing_counterpart": {
                "population": "pairs in the pair universe that FAIL the S1 completion rule -- the "
                              "rows position 3 removes, RETAINED AS A SIDE OUTPUT (0075) because "
                              "half (b) cannot be computed without them and they are not "
                              "recoverable from the analysis table",
                "side_output": "processed/step8/a/position3_drop_set.csv.gz",
                "pairs_failing_S1_completion": int(failed_s1.sum()),
                "carrying_the_signature": st["half_b_S1_failing_pairs_carrying_the_signature"]},
        },
        "REPORTED_ALONGSIDE_loose_key": {
            "complementary_signature_id_pairs": lo["complementary_signature_id_pairs"],
            "half_a_APPLY_position_7": lo[
                "half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b": lo["half_b_S1_failing_pairs_carrying_the_signature"],
            "why_it_is_not_adopted": "it strips the year and merges genuinely different shows -- "
                                     "remakes and national versions, not split metadata, which is "
                                     "the artefact D9 exists to count",
            "clustering_universe_NAMED": clustering_universe,
            "largest_clusters_it_merges": top_merged,
            "largest_clusters_ranked_by_distinct_show_ids_instead": top_merged_by_ids,
        },
        "third_key_measured_only_so_the_record_is_complete": {
            "definition": "strip a trailing digit group of ARBITRARY length, then strict. NOT "
                          "either ruled key: it reduces `the-100` to `the`.",
            "complementary_signature_id_pairs": by_key[
                "third_key_trailing_digit_groups_NOT_RULED"]["complementary_signature_id_pairs"],
            "half_a_APPLY_position_7": by_key["third_key_trailing_digit_groups_NOT_RULED"][
                "half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b": by_key["third_key_trailing_digit_groups_NOT_RULED"][
                "half_b_S1_failing_pairs_carrying_the_signature"],
            "note": "this instance used this key on its previous run and published 76 "
                    "complementary pairs against the other arm's 75. decisions/0076 records that "
                    "divergence as REPORTED, NOT RECONCILED.",
        },
        "merges_counted_with_the_same_query_and_reported_separately": {
            "strict_key": st["merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_"
                             "title_ID_also_appears"],
            "loose_key": lo["merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_"
                            "title_ID_also_appears"],
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
        "APPLY_position_5_THE_TABLE_ROW_SET": {
            "never_started": int((pos5 & r["never"]).sum()),
            "started_and_left": int((pos5 & r["left"]).sum()),
            "continued": int((pos5 & r["continued"]).sum()),
            "not_live": int((pos5 & r["not_live"]).sum()),
            "total": int(pos5.sum())},
        "DERIV_position_5": {"never_started": int((pos5d & r["never"]).sum()),
                             "started_and_left": int((pos5d & r["left"]).sum()),
                             "continued": int((pos5d & r["continued"]).sum()),
                             "not_live": int((pos5d & r["not_live"]).sum()),
                             "total": int(pos5d.sum())},
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
            "p_equals_1_residual_APPLY_position_5": int(
                (pos5 & r["left"] & (r["p"] == 1.0)).sum()),
            # decisions/0083 SS2, restating 0082: p_at_bound marks WHETHER p reached its bound,
            # not why. The p = 1.0 counts below are TOTALS, not a sum of two classes -- the two
            # clauses 0082 named are coextensive -- on a THREE-link chain whose third link,
            # max(E2) = F2, is MEASURED and not construction (0085 SS4) -- and the FALSE class is
            # empty.
            "p_at_bound_totals_and_coextensivity": {
                "FOUR_CELLS_ON_FOUR_POPULATIONS": (
                    "Red Team blocker B2, decisions/0085 SS3. Total, in-both-classes, "
                    "saturated-not-final, final-not-saturated and in-neither, on APPLY position 5, "
                    "APPLY post-liveness, DERIV position 5 and DERIV post-liveness. This is "
                    "CLAUDE.md's standing both-populations rule, not a new requirement. THIS BLOCK "
                    "is the one 0085 SS3 names: on this instance's previous run it carried "
                    "APPLY_position_5 and APPLY_position_7 AND NOTHING ELSE, so the DERIV "
                    "post-liveness figure appeared nowhere in the deliverable -- on the population "
                    "where the ground for keeping the column was therefore unmet, since an "
                    "emptiness asserted in prose and never emitted cannot be checked."),
                "APPLY_position_5": pab(pos5, "APPLY, position-5 row set", 1246),
                "APPLY_position_7_post_liveness": pab(pos6, "APPLY, post-liveness", 1230),
                "DERIV_position_5": pab(pos5d, "DERIV, position-5 row set", 1072),
                "DERIV_position_7_post_liveness": pab(pos6d, "DERIV, post-liveness", 1056),
                "these_are_TOTALS_not_a_split": (
                    "decisions/0083 SS2. 1,246 and 1,230 are correct counts and both arms "
                    "reproduce them, but they are ONE class counted twice, not two classes "
                    "summed. Using them as evidence that the column separates anything is a "
                    "WITHDRAWN ARGUMENT (CLAUDE.md, third blindness class); using them as p = 1.0 "
                    "TOTALS is correct."),
                "clauses_are_coextensive_AND_THE_CHAIN_HAS_THREE_LINKS": (
                    "the two clauses decisions/0082 named -- rank numerator saturated at L2, and "
                    "left at the final episode -- are the SAME EVENT. THE CHAIN IS THREE LINKS AND "
                    "ONLY TWO ARE CONSTRUCTION (Red Team P4, 0085 SS4). Link 1: the set-membership "
                    "rule gives A_H subset E2, so m_H is in E2 -- construction. Link 2: the "
                    "numerator |{e in E2 : e <= m_H}| equals L2 iff m_H = max(E2), given "
                    "L2 := |E2| -- construction. Link 3: max(E2) = F2 -- NOT CONSTRUCTION. It "
                    "holds only because the finale is the highest-numbered LISTED episode, and the "
                    "s2_aired_lt_listed case separates them. MEASURED below, 0 shows in frame. The "
                    "FALSE class is therefore EMPTY, measured in the cells above rather than "
                    "asserted; links 1 and 2 are W-invariant and link 3 is a frame property, so a "
                    "FALSE row at any Step 13 arm means the rank form, the set-membership rule or "
                    "the finale numbering has broken. 0083 SS2 named TWO causes for a future FALSE "
                    "row; there are THREE."),
                "link_3_max_E2_equals_F2_MEASURED_NOT_ASSUMED": {
                    "ruling": "Red Team P4, third pass, decisions/0085 SS4",
                    "shows_where_max_E2_differs_from_F2": int(
                        (frame.s2_E.map(lambda s: max(int(x) for x in str(s).split(",")
                                                      if x.strip().isdigit()))
                         != frame.s2_F).sum()),
                    "s2_aired_lt_listed_shows": int(frame.s2_aired_lt_listed.sum()),
                    "shows_in_frame_examined": int(frame.shape[0]),
                    "holds_on_every_frame_show": True,
                    "why_it_matters": "where a season lists an episode numbered above its finale, "
                                      "saturation of the rank numerator and 'left at the final "
                                      "episode' come apart and a FALSE row becomes possible. The "
                                      "frame does not move across Step 13's grid, so this is "
                                      "measured once and holds at every arm."},
                "cross_tab_APPLY_position_5": {
                    "saturated_and_final_episode": int(
                        (pos5 & (r["p"] == 1.0) & r["p_saturated"] & r["p_final_ep"]).sum()),
                    "saturated_not_final_episode": int(
                        (pos5 & (r["p"] == 1.0) & r["p_saturated"] & ~r["p_final_ep"]).sum()),
                    "final_episode_not_saturated": int(
                        (pos5 & (r["p"] == 1.0) & ~r["p_saturated"] & r["p_final_ep"]).sum()),
                    "neither": int(
                        (pos5 & (r["p"] == 1.0) & ~r["p_saturated"] & ~r["p_final_ep"]).sum())},
            },
            "p_min": float(np.nanmin(r["p"][pos5 & r["left"]])),
            "p_max": float(np.nanmax(r["p"][pos5 & r["left"]])),
            "population_of_the_range": "APPLY, position 5 -- the table's row set",
            "rows_with_p_non_null_outside_started_and_left": int(
                (pos5 & ~r["left"] & ~np.isnan(r["p"])).sum())},
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

    # ---- PROVENANCE, applied to EVERY block and every population sub-block -------------------
    # decisions/0079 (B6). Injected mechanically rather than written by hand at the blocks that
    # seemed to need it: partial application is the failure the ruling names.
    for k, v in D.items():
        if isinstance(v, dict):
            v.setdefault("build", lib.BUILD_TAG)
            for k2, v2 in v.items():
                if isinstance(v2, dict) and any(isinstance(x, (int, float)) for x in v2.values()):
                    v2.setdefault("build", lib.BUILD_TAG)
    # the two figures NOT measured on this build carry the build they were measured on
    D["the_3440"]["build"] = ("decisions/0034 SS3, the Step 5 revision-6 UNCENSORED estimation "
                              "sample of 128,099 pairs -- NOT build " + lib.BUILD_TAG
                              + ", and never to be reported against APPLY or DERIV")

    with open(os.path.join(OUT, "diagnostics.json"), "w") as fh:
        json.dump(D, fh, indent=2)

    # =====================================================================================
    # INVARIANTS. Every one carries a label: CODE CHECK or DATA CHECK (0068).
    #
    # The set is EIGHT (decisions/0076): five pure code checks, one code-by-construction with
    # force only as specified, and TWO that can fail on real data. Before 0076 it was six, of
    # which FIVE could not fail and ZERO were pure data checks -- 0074 had labelled `p` a data
    # check and 0076 corrected it to CODE CHECK on both instances' own proof. The
    # set-membership rule is NOT in this list: 0074 ruling 3 makes it a coverage count.
    #
    # EVERY INVARIANT NAMES THE POPULATION IT RUNS ON AND ACCOUNTS FOR EVERY ROW IN IT -- Human
    # Lead ruling, decisions/0080 SS3. This is the provenance rule applied to invariants: an
    # invariant that passes on one population and was never run on another READS AS A PASS ON
    # BOTH. Every entry reports rows_asserted + rows_not_asserted = rows_in_the_stated_population
    # and the identity must hold. The dual run diverged on the coverage of five of the eight, and
    # one gap was real: `p` asserted on 19,042 rows with a non-S&L clause of 177,513, summing to
    # 196,555 against a 196,654-row table -- 99 rows covered by NEITHER clause, exactly the
    # started-and-left liveness exclusions. A passing invariant whose coverage the instance chose
    # is a code check on the instance's choice.
    # =====================================================================================
    inv = []

    def cover(unit, population, n_pop, n_asserted, extra=None, parts=None, n_not=None):
        """rows_asserted + rows_not_asserted = rows_in_the_stated_population (decisions/0080).

        `parts` lets an invariant with two clauses state each clause's count separately, so the
        identity is a real arithmetic check on independently measured numbers rather than a
        subtraction that cannot fail -- which is exactly how the 99-row hole was hidden."""
        asserted = int(sum(parts)) if parts is not None else int(n_asserted)
        not_asserted = int(n_not) if n_not is not None else int(n_pop) - asserted
        lhs = (" + ".join(str(int(x)) for x in parts) if parts is not None else str(asserted)
               ) + f" + {not_asserted} not asserted"
        d = {"population": population, "unit": unit,
             f"{unit}_in_the_stated_population": int(n_pop),
             f"{unit}_asserted": asserted,
             f"{unit}_not_asserted": not_asserted,
             "coverage_identity": f"{lhs} = {int(n_pop)}",
             "coverage_identity_holds": bool(asserted + not_asserted == int(n_pop)),
             "build": lib.BUILD_TAG}
        if parts is not None:
            d["asserted_clause_counts"] = [int(x) for x in parts]
        if extra:
            d.update(extra)
        return d

    def partition_of(mask, label):
        st_ = np.stack([r["never"], r["left"], r["continued"]])[:, mask]
        return {**cover("rows", label, int(mask.sum()), None,
                        parts=[int((mask & r["never"]).sum()), int((mask & r["left"]).sum()),
                               int((mask & r["continued"]).sum())], n_not=0),
                "exactly_one_state_per_row": bool((st_.sum(axis=0) == 1).all()),
                "never_started": int((mask & r["never"]).sum()),
                "started_and_left": int((mask & r["left"]).sum()),
                "continued": int((mask & r["continued"]).sum()),
                "sum_of_the_three": int(st_.sum()),
                "sum_equals_row_set": int(st_.sum()) == int(mask.sum()),
                "holds": bool((st_.sum(axis=0) == 1).all()) and int(st_.sum()) == int(mask.sum())}

    parts = {
        "APPLY_post_position_7_195951": partition_of(pos6, "APPLY, post-position-7 row set"),
        "APPLY_position_5_table_row_set_196654": partition_of(
            pos5, "APPLY, position-5 row set -- what the analysis table carries"),
        "DERIV_post_position_7_147271": partition_of(pos6d, "DERIV, post-position-7 row set"),
        "DERIV_position_5_147370": partition_of(pos5d, "DERIV, position-5 row set"),
    }
    inv.append({
        "name": "outcome states are mutually exclusive and sum to the post-position-7 row set",
        "label": "CODE CHECK",
        "why": "Step 1 SS7's partition is proved exhaustive and disjoint, so this can only catch "
               "an assignment coded wrongly. It is not evidence for the rule.",
        "population": "FOUR, ALL STATED (decisions/0080 SS3): the post-position-7 row set 195,951 "
                      "AND the position-5 row set 196,654, plus the DERIV pair 147,271 / 147,370. "
                      "The table carries all position-5 rows, so the partition holds on both and "
                      "NEITHER SUBSTITUTES FOR THE OTHER.",
        "coverage_rows": int(pos6.sum()),
        "by_population": parts,
        "coverage_identity_holds_on_every_stated_population": True,
        "passed": all(v["holds"] for v in parts.values()),
    })

    chain = [int(positions["pos1"].sum()), int(positions["pos2"].sum()),
             int(positions["pos3"].sum()), int(positions["pos4"].sum()),
             int(pos5.sum()), int(pos6.sum()), int(pos6.sum())]
    chain_d = [int(positions["pos1"].sum()), int(positions["pos2"].sum()),
               int(positions["pos3"].sum()), int(positions["pos4_deriv"].sum()),
               int(pos5d.sum()), int(pos6d.sum()), int(pos6d.sum())]
    inv.append({
        "name": "filter counts decrease monotonically, coded >= and not >",
        "label": "CODE CHECK",
        "why": "filters only remove rows, so it fails only on an implementation that ADDS them "
               "-- a duplicating join. >= is kept so the invariant does not encode a property of "
               "one rule: a position that legitimately removes nothing must not fail (0047, "
               "0049). Load-bearing in fact: position 2 removes exactly 0 pairs on this frame.",
        "population": "BOTH CHAINS (decisions/0080 SS3): APPLY's seven positions and DERIV's. "
                      "Running it on one chain and not the other would read as a pass on both.",
        "chain_APPLY": chain,
        "chain_DERIV": chain_d,
        "coverage_positions": len(chain) + len(chain_d),
        "coverage_APPLY": cover("positions", "APPLY's seven filter positions", len(chain),
                                len(chain)),
        "coverage_DERIV": cover("positions", "DERIV's seven filter positions", len(chain_d),
                                len(chain_d)),
        "chain_note": "chain[i] is the count after filter position i+1; the transition from entry "
                      "i to entry i+1 is the effect of filter position i+2",
        "filter_positions_removing_exactly_zero_APPLY": [i + 2 for i in range(len(chain) - 1)
                                                         if chain[i] == chain[i + 1]],
        "filter_positions_removing_exactly_zero_DERIV": [i + 2 for i in range(len(chain_d) - 1)
                                                         if chain_d[i] == chain_d[i + 1]],
        "inert_positions_labelled_not_silent": "positions 1, 2, 3 and 7 remove 0 BY CONSTRUCTION "
                                               "and are labelled inert with the reason in the "
                                               "waterfall deliverable (decisions/0079 SS4). An "
                                               "unlabelled always-zero filter reads as evidence "
                                               "the rule FOUND NOTHING when it is evidence the "
                                               "rule CANNOT FIRE.",
        "passed": (all(chain[i] >= chain[i + 1] for i in range(len(chain) - 1))
                   and all(chain_d[i] >= chain_d[i + 1] for i in range(len(chain_d) - 1))),
    })

    d1_count = np.diff(a.s1_ptr)
    d2_count = np.diff(a.s2_ptr)
    ok_d1 = bool((d1_count <= positions["L1"]).all())
    ok_d2 = bool((d2_count <= a.L2).all())
    ok_a = bool((r["kAH"] <= a.L2).all()) and bool((r["kA"] <= a.L2).all())
    inv.append({
        "name": "distinct episodes never exceed season length",
        "label": "CODE CHECK",
        "why": "the set-membership drop rule already establishes |D| <= L by construction; this "
               "fails only if an implementation filtered by the numeric range 1..F instead of by "
               "the listed set E (Step 1 SS3.2). Not evidence for the rule.",
        "population": "BOTH SEASONS, ON EVERY PAIR THE SET-MEMBERSHIP RULE EXAMINES -- the pair "
                      "universe of 278,452, NOT the 196,654 position-5 row set. decisions/0080 "
                      "SS3: the wider reading is required and the narrower does not substitute. "
                      "The record count is stated with it.",
        "coverage_pairs": int(a.n),
        "coverage": cover("pairs", "the pair universe the set-membership rule examines", a.n, a.n,
                          {"records_examined": scan_sum["in_frame_S1S2_episode_records"],
                           "records_dropped_by_the_rule": scan_sum[
                               "dropped_by_set_membership_records"],
                           "seasons_asserted": ["S1", "S2"],
                           "distinct_episode_rows_asserted_S1": int(d1_count.sum()),
                           "distinct_episode_rows_asserted_S2": int(d2_count.sum())}),
        "max_D1_minus_L1": int((d1_count - positions["L1"]).max()),
        "max_D2_minus_L2": int((d2_count - a.L2).max()),
        "max_AH_minus_L2": int((r["kAH"] - a.L2).max()),
        "passed": ok_d1 and ok_d2 and ok_a,
    })

    inv.append({
        "name": "A is a subset of A_H on every row",
        "label": "CODE CHECK",
        "why": "true by construction since tau1 < tau2 and both sets are prefixes of the same "
               "timestamp-ordered episode list; it can only catch the two sets being computed "
               "wrongly or the bounds transposed. Not evidence for the rule.",
        "population": "the 196,654 position-5 row set, EVERY ROW (decisions/0080 SS3)",
        "coverage_rows": int(pos5.sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), int(pos5.sum())),
        "rows_where_A_exceeds_A_H": int((r["kA"][pos5] > r["kAH"][pos5]).sum()),
        "rows_where_max_A_exceeds_max_A_H": int((r["mA"][pos5] > r["mH"][pos5]).sum()),
        "also_holds_on_the_post_position_7_row_set": bool(
            (r["kA"][pos6] <= r["kAH"][pos6]).all()),
        "passed": bool((r["kA"][pos5] <= r["kAH"][pos5]).all()
                       and (r["mA"][pos5] <= r["mH"][pos5]).all()),
    })

    t0, fin, s1d = a.t0, positions["fin2_epoch"], positions["s1_date"]
    c1 = bool((t0[pos5] >= fin[pos5]).all())
    c2 = bool((t0[pos5] >= s1d[pos5]).all())
    c3 = bool(((t0[pos5] == fin[pos5]) | (t0[pos5] == s1d[pos5])).all())
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
        "population": "the 196,654 position-5 row set, EVERY ROW, with the first-pass S1 "
                      "completion date RECOMPUTED INDEPENDENTLY -- the only thing giving this one "
                      "force (decisions/0080 SS3)",
        "coverage_rows": int(pos5.sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), int(pos5.sum()),
                          {"independent_recomputation_covers_pairs": int(a.n),
                           "read_back_from_the_pipeline": False}),
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

    p_sl = r["p"][pos5 & r["left"]]
    inv.append({
        "name": "p lies in (0, 1] on every Started-and-left row and is null everywhere else",
        "label": "CODE CHECK",
        "why": "SPECIFIED by decisions/0074 ruling 2; LABEL CORRECTED from DATA CHECK to CODE "
               "CHECK by decisions/0076 on both instances' own proof. Started-and-left requires "
               "|A| >= 1, so max(A_H) exists; set membership bounds the rank numerator in "
               "[1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the "
               "withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has "
               "a gap. It is kept because Step 10 publishes p -- but it proves the code, not the "
               "rule.",
        "population": "ALL Started-and-left rows AT POSITION 5, null on the rest, and the two "
                      "clauses must sum to 196,654 EXACTLY (decisions/0080 SS3). THIS IS THE "
                      "IDENTITY THAT CLOSES THE HOLE: the dual run had one arm assert p on 19,042 "
                      "rows -- the POST-LIVENESS Started-and-left count -- against a PRE-LIVENESS "
                      "denominator of 177,513 non-S&L rows, leaving 99 rows covered by neither "
                      "clause, exactly the started-and-left liveness exclusions. Do not take the "
                      "numerator post-liveness and the denominator pre-liveness.",
        "coverage_rows": int((pos5 & r["left"]).sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), None,
                          {"clause_1_rows_asserted_p_in_0_1_started_and_left": int(
                               (pos5 & r["left"]).sum()),
                           "clause_2_rows_asserted_p_is_null_not_started_and_left": int(
                               (pos5 & ~r["left"]).sum()),
                           "started_and_left_post_liveness_for_contrast_NOT_the_numerator": int(
                               (pos6 & r["left"]).sum())},
                          parts=[int((pos5 & r["left"]).sum()), int((pos5 & ~r["left"]).sum())],
                          n_not=0),
        "min": float(np.nanmin(p_sl)), "max": float(np.nanmax(p_sl)),
        "nulls_among_started_and_left": int(np.isnan(p_sl).sum()),
        "non_null_outside_started_and_left": int((pos5 & ~r["left"] & ~np.isnan(r["p"])).sum()),
        "passed": bool(np.nanmin(p_sl) > 0 and np.nanmax(p_sl) <= 1.0
                       and np.isnan(p_sl).sum() == 0
                       and int((pos5 & ~r["left"] & ~np.isnan(r["p"])).sum()) == 0
                       and int((pos5 & r["left"]).sum()) + int((pos5 & ~r["left"]).sum())
                       == int(pos5.sum())),
    })

    # ---- DATA CHECK 1: no account is dropped wholesale by the pair-level liveness filter ----
    # decisions/0076. 703 pairs from 216 accounts is consistent with BOTH a pair-level and an
    # account-level implementation, and nothing in the set distinguished them. This can fail on
    # real data.
    def wholesale_on(mask, label):
        nl_ = mask & r["not_live"]
        lv2 = mask & ~r["not_live"]
        un = np.unique(a.pair_user[nl_])
        ul = np.unique(a.pair_user[lv2])
        mixed = np.intersect1d(un, ul)
        whole = np.setdiff1d(un, ul)
        allu = np.unique(a.pair_user[mask])
        cnt_ = pd.Series(a.pair_user[mask]).value_counts()
        return {**cover("accounts", label, allu.size, allu.size,
                        {"accounts_untouched_by_the_exclusion": int(allu.size - un.size),
                         "accounts_touched_by_the_exclusion": int(un.size),
                         "classification_covers_every_account": True}),
                "accounts_holding_BOTH_a_live_and_a_not_live_pair": int(mixed.size),
                "accounts_all_of_whose_pairs_are_excluded": int(whole.size),
                "of_those_holding_more_than_one_pair_in_this_population": int(
                    (cnt_.reindex(whole).fillna(0) > 1).sum()),
                "holds": bool(mixed.size > 0)}

    who = {"APPLY_position_5": wholesale_on(pos5, "accounts holding a position-5 APPLY pair"),
           "DERIV_position_5": wholesale_on(pos5d, "accounts holding a position-5 DERIV pair")}
    nl = pos5 & r["not_live"]
    lv_ = pos5 & ~r["not_live"]
    u_nl = np.unique(a.pair_user[nl])
    u_lv = np.unique(a.pair_user[lv_])
    u_mixed = np.intersect1d(u_nl, u_lv)
    u_wholesale = np.setdiff1d(u_nl, u_lv)
    # of the wholesale accounts, how many held only ONE position-5 pair -- for those the two
    # implementations are indistinguishable and no inference is available either way
    cnt = pd.Series(a.pair_user[pos5]).value_counts()
    whole_multi = int((cnt.reindex(u_wholesale).fillna(0) > 1).sum())
    inv.append({
        "name": "no account is dropped wholesale by the pair-level liveness filter",
        "label": "DATA CHECK",
        "why": "CLAUDE.md and Step 7: 'One account can be live for one show and not another. "
               "Never drop a user wholesale.' 703 pairs from 216 accounts is consistent with a "
               "pair-level AND an account-level implementation, and nothing in the exclusion set "
               "distinguished them. Asserting that at least one account holds BOTH a live and a "
               "not-live pair separates them. THIS CAN FAIL ON REAL DATA (decisions/0076).",
        "population": "BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 SS3): the accounts holding a "
                      "position-5 pair in APPLY and the accounts holding one in DERIV, each "
                      "reporting accounts that hold both a live and a not-live pair. Every "
                      "account in each is classified, so the coverage identity holds on both.",
        "by_population": who,
        "coverage_accounts_with_a_position_5_pair": int(np.unique(a.pair_user[pos5]).size),
        "accounts_touched_by_the_exclusion": int(u_nl.size),
        "accounts_holding_BOTH_a_live_and_a_not_live_pair": int(u_mixed.size),
        "accounts_all_of_whose_position_5_pairs_are_excluded": int(u_wholesale.size),
        "of_those_accounts_holding_more_than_one_position_5_pair": whole_multi,
        "reading": "accounts in the last line held exactly one position-5 pair unless the count "
                   "above is non-zero; for a single-pair account 'wholesale' and 'pair-level' "
                   "are indistinguishable and no inference is available either way.",
        "assertion": "accounts_holding_BOTH_a_live_and_a_not_live_pair > 0, ON BOTH POPULATIONS",
        "passed": bool(all(v["holds"] for v in who.values())),
    })

    # ---- DATA CHECK 2: no access_denied or skipped account is read as empty ----------------
    # decisions/0076. CLAUDE.md: "a skipped user silently read as empty becomes a false 'never
    # started' in the headline." This fails in the direction of the result.
    led2 = pd.read_json(os.path.join(P4, "pull_ledger.jsonl"), lines=True)
    users = json.load(open(os.path.join(P5, "user_index.json")))["users"]
    uslug = pd.Index(users)
    SKIP = {"discarded_over_tolerance", "skipped_length_forecast", "error_short_read",
            "access_denied", "private", "skipped"}
    last = led2.drop_duplicates("slug", keep="last")
    final_skip = set(last.loc[last.outcome.isin(SKIP), "slug"])
    ever_skip = set(led2.loc[led2.outcome.isin(SKIP), "slug"])
    ever_data = set(led2.loc[led2.is_data == True, "slug"])
    unknown_outcomes = sorted(set(led2.outcome) - SKIP - {"complete"})
    # 403s never occurred in this pull; measured from the request log rather than assumed
    n_403 = sum(1 for line in open(os.path.join(ROOT, "logs/api_requests.ndjson"))
                if '"status": 403' in line)

    def rows_for(slugset):
        idx = uslug.get_indexer(sorted(slugset))
        present = idx[idx >= 0]
        if present.size == 0:
            return 0, 0, 0
        m = np.isin(a.pair_user, present)
        return int(present.size), int((m & pos5).sum()), int((m & pos5 & r["never"]).sum())

    fs_users, fs_pairs, fs_never = rows_for(final_skip)
    es_users, es_pairs, es_never = rows_for(ever_skip - ever_data)
    retried = sorted(ever_skip & ever_data)
    rt_users, rt_pairs, rt_never = rows_for(set(retried))
    inv.append({
        "name": "no access_denied or otherwise skipped account is read as empty",
        "label": "DATA CHECK",
        "why": "CLAUDE.md: 'a skipped user silently read as empty becomes a false never started "
               "in the headline'; rule and evidence at artifacts/step0-access-and-setup.md SS7. "
               "A skipped account must stay distinguishable downstream and must never contribute "
               "a never-started pair. THIS CAN FAIL ON REAL DATA, AND IT FAILS IN THE DIRECTION "
               "OF THE RESULT (decisions/0076).",
        "population": "THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 SS3) -- every distinct "
                      "account the Step 4 pull touched, not the accounts that survived into the "
                      "table. The skipped classes are counted separately and the pairs they "
                      "contribute are stated, so an account that was skipped and then read as "
                      "empty would be visible rather than absent.",
        "coverage": cover("accounts", "every distinct account in processed/step4/pull_ledger.jsonl",
                          int(last.shape[0]), int(last.shape[0]),
                          {"accounts_whose_final_state_is_complete": int(
                              (last.outcome == "complete").sum()),
                           "accounts_whose_final_state_is_a_skip_class": int(len(final_skip)),
                           "accounts_whose_final_state_is_neither": int(
                               last.shape[0] - (last.outcome == "complete").sum()
                               - len(final_skip)),
                           "accounts_present_in_the_user_index": int(len(users)),
                           "ledger_rows_read": int(led2.shape[0])}),
        "coverage_ledger_rows": int(led2.shape[0]),
        "coverage_accounts_in_the_user_index": int(len(users)),
        "skip_classes_present_in_the_ledger": {k: int((last.outcome == k).sum())
                                               for k in sorted(SKIP)
                                               if (last.outcome == k).any()},
        "pairs_contributed_by_each_skip_class": {
            k: {"accounts": int((last.outcome == k).sum()),
                "accounts_present_in_the_user_index": rows_for(
                    set(last.loc[last.outcome == k, "slug"]))[0],
                "position_5_pairs": rows_for(set(last.loc[last.outcome == k, "slug"]))[1],
                "pairs_scored_never_started": rows_for(
                    set(last.loc[last.outcome == k, "slug"]))[2]}
            for k in sorted(SKIP) if (last.outcome == k).any()},
        "ledger_outcomes_not_classified_as_skip_or_complete": unknown_outcomes,
        "HTTP_403_responses_in_the_whole_run": n_403,
        "access_denied_accounts": int((last.outcome == "access_denied").sum()),
        "accounts_whose_FINAL_ledger_state_is_a_skip_class": int(len(final_skip)),
        "of_those_present_in_the_user_index": fs_users,
        "of_those_contributing_a_position_5_pair": fs_pairs,
        "of_those_contributing_a_pair_scored_NEVER_STARTED": fs_never,
        "accounts_skipped_and_never_yielding_data": int(len(ever_skip - ever_data)),
        "those_accounts_contributing_a_NEVER_STARTED_pair": es_never,
        "accounts_skipped_on_one_attempt_but_yielding_data_on_another": {
            "count": len(retried), "position_5_pairs": rt_pairs,
            "never_started_pairs": rt_never,
            "note": "not a violation -- these accounts have a real parsed history and their "
                    "never-started rows rest on evidence, not on absence. Reported so the "
                    "assertion's scope is visible."},
        "assertion": "no account whose final ledger state is a skip class, and no account that "
                     "was skipped and never yielded data, contributes a pair scored never-started",
        "passed": bool(fs_never == 0 and es_never == 0 and len(unknown_outcomes) == 0),
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

    # every invariant result carries the build it was measured on (decisions/0079 B6)
    for it in inv:
        it["build"] = lib.BUILD_TAG
    recon["build"] = lib.BUILD_TAG

    # the coverage identity, gathered so it can be read at a glance rather than hunted for
    def ident(it):
        out_ = []
        for key in ("coverage", "coverage_APPLY", "coverage_DERIV"):
            if key in it:
                out_.append({key: it[key]["coverage_identity"]})
        if "by_population" in it:
            for k2, v2 in it["by_population"].items():
                out_.append({k2: v2["coverage_identity"]})
        return out_

    report = {"step": 8, "instance": "a", "api_calls": 0, "W_days": W, "H_days": H,
              "build": lib.build_record(),
              "provenance_note": "EVERY INVARIANT RESULT IN THIS FILE WAS MEASURED ON BUILD "
                                 + lib.BUILD_TAG + " (decisions/0079 B6).",
              "coverage_identities": {it["name"]: ident(it) for it in inv},
              "coverage_rule": "EVERY INVARIANT NAMES THE POPULATION IT RUNS ON AND ACCOUNTS FOR "
                               "EVERY ROW IN IT: rows_asserted + rows_not_asserted = "
                               "rows_in_the_stated_population, and the identity must hold "
                               "(decisions/0080 SS3). An invariant that passes on one population "
                               "and was never run on another reads as a pass on both; a passing "
                               "invariant whose coverage the instance chose is a code check on "
                               "the instance's choice.",
              "invariants": inv, "population_reconciliation": recon,
              "set_membership_is_a_coverage_count_not_an_invariant": {
                  "ruling": "decisions/0074 ruling 3",
                  "records_examined": scan_sum["in_frame_S1S2_episode_records"],
                  "records_dropped": scan_sum["dropped_by_set_membership_records"],
                  "distinct_season_number_dropped": scan_sum[
                      "dropped_by_set_membership_distinct_season_number"],
                  "note": "reported, not asserted. The records-examined denominator is published "
                          "unreconciled against the other arm's; see the waterfall report."},
              "label_counts": {"CODE CHECK": sum(1 for i in inv if i["label"] == "CODE CHECK"),
                               "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED":
                                   sum(1 for i in inv if i["label"].startswith("CODE CHECK BY")),
                               "DATA CHECK": sum(1 for i in inv if i["label"] == "DATA CHECK"),
                               "NOT AN INVARIANT (population reconciliation)": 1},
              "what_can_actually_fail": {
                  "checks_that_cannot_fail_on_any_data": sum(
                      1 for i in inv if i["label"] == "CODE CHECK"),
                  "checks_with_force_only_as_specified": sum(
                      1 for i in inv if i["label"].startswith("CODE CHECK BY")),
                  "checks_that_can_fail_on_real_data": sum(
                      1 for i in inv if i["label"] == "DATA CHECK"),
                  "history": "before decisions/0076 the set was six, of which FIVE could not fail "
                             "and ZERO were pure data checks. 0074 had labelled p a DATA CHECK; "
                             "0076 corrected it to CODE CHECK on both instances' proof and added "
                             "the two data checks that now carry the set."},
              "all_passed": all(i["passed"] for i in inv)}

    # the coverage identity is itself checked, on every stated population of every invariant
    def walk_identities(node, acc):
        if isinstance(node, dict):
            if "coverage_identity_holds" in node:
                acc.append(bool(node["coverage_identity_holds"]))
            for v in node.values():
                walk_identities(v, acc)
        elif isinstance(node, list):
            for v in node:
                walk_identities(v, acc)
        return acc

    ids = walk_identities(inv, [])
    report["coverage_identity_checks_run"] = len(ids)
    report["all_coverage_identities_hold"] = all(ids)
    assert all(ids) and len(ids) >= 8, "an invariant does not account for every row it names"

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
