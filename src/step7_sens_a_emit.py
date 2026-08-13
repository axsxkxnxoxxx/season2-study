"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 6 — assemble artifacts/step7-sensitivity-a.json from the frozen stage outputs.

Counts and aggregates only. No usernames, no user IDs, no individual watch histories.

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/sens_a")
ART = os.path.join(ROOT, "artifacts")


def load(name):
    with open(os.path.join(OUT, name)) as fh:
        return json.load(fh)


def main():
    pop, oi = load("population.json"), load("outcome_inputs.json")
    sens, boot, sweep = load("sensitivity.json"), load("bootstrap.json"), load("sweep.json")
    chk = load("crosscheck.json")

    doc = {
        "STATUS": {
            "what_this_is": "A GATE-CLOSING DIAGNOSTIC FOR STEP 7, run under decisions/0041 "
                            "SS4 to decide whether the liveness threshold is load-bearing.",
            "what_this_is_not": "NOT the Step 9 deliverable, and not a study result. The "
                                "shares below must not be cited as the headline.",
            "why_provisional_in_population_too": "Step 8 has not launched and is an "
                                                 "unapproved gate. Step 8 builds the analysis "
                                                 "table and fixes the headline population. "
                                                 "This test runs on the Step 7 "
                                                 "derivation/application population — "
                                                 "waterfall line 4 less D10 = 147,370 — "
                                                 "which decisions/0041 SS3 records as a "
                                                 "strict SUBSET of the population Step 8 "
                                                 "will apply liveness to (196,654). Both the "
                                                 "population and the status are provisional.",
            "adopts": "nothing. The Human Lead rules on whether the threshold survives.",
            "api_calls": 0,
        },
        "question": "Is the headline sensitive to the liveness threshold across its "
                    "account-clustered interval?",
        "answer": {
            "verdict": "NO. The headline is insensitive across the interval and beyond it.",
            "largest_movement_across_the_four_candidate_settings_pp":
                sens["max_minus_min_share_pp_across_the_four_candidate_settings"],
            "same_movement_as_a_fraction_of_the_95pct_clustered_sampling_width":
                {k: v["span_as_share_of_ci_width"]
                 for k, v in boot["span_against_sampling_width"].items()},
            "movement_over_the_whole_swept_range_30_to_4000_days_pp":
                sweep["share_range_over_whole_sweep_pp"],
            "read_this_with_the_caveat_below": "one delta is statistically distinguishable "
                                               "from zero and is still negligible in size; "
                                               "see caveats.paired_test_detects_a_trivial_delta",
        },
        "spec": {
            "governing": ["decisions/0041 SS4 (this test)", "decisions/0040 (the two rulings "
                          "that produced the population)", "decisions/0038 (frozen spec)",
                          "decisions/0037", "decisions/0036 SS2 with SS2.3(ii) withdrawn",
                          "decisions/0034 (two-instant outcome assignment)",
                          "decisions/0029", "decisions/0026 (W=108)", "decisions/0021"],
            "W_days": 108, "H_days": 91,
            "tau1": "[[T0]] + 108*24h — never-started is tested here",
            "tau2": "[[T0]] + (108+91)*24h = [[T0]] + 199 days — Continued is tested here",
            "liveness_anchor": "tau1 only. tau2 plays no part in liveness (decisions/0034).",
            "calibration": "processed/step5/calibration.npz, the STORED isotonic play-id "
                           "curve, read not refitted",
            "boundary_form": "half-open UTC instant, watched_at < tau. "
                             "date(watched_at) <= T1 appears nowhere.",
            "membership": "by SET against E2, never by the range 1..F2",
            "counting": "distinct episodes, canonical timestamp = min watched_at across the "
                        "episode's records (Step 1 SS2.2). Never play events.",
            "drop_flag": "not used and not available — Dropped status is OAuth Required. "
                         "All three states are inferred from episode-level history.",
        },
        "population": pop,
        "outcome_inputs": oi,
        "results": sens,
        "bootstrap_yardstick": boot,
        "continuous_threshold_sweep": sweep,
        "outcome_operator_validation": {
            "why": "the liveness filter here is reused from a4 and already corroborated, but "
                   "the OUTCOME OPERATOR — |A| at tau1, |A_H| at tau2, F2 in A_H, the "
                   "canonical min-watched_at rule — is built fresh for this test. It is run "
                   "unchanged on a population where the answer is already on the record.",
            "population": chk["population"],
            "never_started_without_D11": {"record": 8445,
                                          "measured": chk["never_started_without_D11"]},
            "never_started_with_D11": {"record": 8449,
                                       "measured": chk["never_started_with_D11"]},
            "never_started_share_pct": {"record": 6.5957,
                                        "measured": chk["never_started_share_pct_with_D11"]},
            "pairs_moved_by_the_0034_amendment": {
                "record": 2246,
                "measured": chk["pairs_moved_started_and_left_to_continued_by_the_amendment"]},
            "monotone_A_subset_A_H_no_pair_moves_the_other_way":
                chk["monotone_no_pair_moves_the_other_way"],
            "all_four_reproduce_exactly": bool(chk["reproduces_never_started"]
                                               and chk["reproduces_moved_count"]),
        },
        "corroboration_against_the_record": {
            "post_D10_population": {"decisions/0041 SS1": 147370,
                                    "measured_here": pop["post_D10_population"],
                                    "agrees": pop["post_D10_population"] == 147370},
            "classes_live_open_ended_no_before": {
                "decisions/0041 SS1": [128467, 751, 18152],
                "measured_here": [sens["classes_at_tau1"]["measured_bracketing_gap"],
                                  sens["classes_at_tau1"]["open_ended_no_instant_after_tau1"],
                                  sens["classes_at_tau1"]["no_instant_at_or_before_tau1"]]},
            "not_live_at_1293": {"decisions/0041 SS1": 1282,
                                 "measured_here":
                                     sens["settings"]["threshold_1293d"]["pairs_excluded"]},
            "realised_rate_at_1293_vs_extended_set_pct": {
                "decisions/0041 SS1": 0.9921,
                "measured_here": sens["settings"]["threshold_1293d"][
                    "realised_rate_vs_extended_set_pct"]},
            "accounts_carrying_the_exclusion_set_at_1293": {
                "decisions/0041 SS4": "205 of 2,402",
                "measured_here": f"{sens['settings']['threshold_1293d']['accounts_touched_by_exclusion']} "
                                 f"of {pop['n_distinct_accounts_in_population']}"},
            "exclusion_set_at_the_lower_endpoint": {
                "decisions/0041 SS4 states": 1701,
                "measured_here_at_787": sens["settings"]["threshold_787d"]["pairs_excluded"],
                "note": "1,701 is the count at T = 790, the OTHER arm's lower endpoint "
                        "(decisions/0041 SS1 records 787 against 790 as Monte Carlo noise). "
                        "At 787 the count is 1,707. A 6-pair difference; immaterial to the "
                        "verdict, recorded so the record is not quietly corrected."},
        },
        "caveats": {
            "the_parameter_free_rule_has_two_readings_and_this_instance_reconciles_neither": {
                "why": "decisions/0041 SS4 states the parameter-free rule as 'a distinct "
                       "insertion instant at or before tau1 AND one after it'. Read "
                       "literally that REINSTATES decisions/0036 SS2.3's second edge case, "
                       "which decisions/0040 SS1 WITHDREW for contradicting approved gate "
                       "0021 — the ruling that returned the 18,152 pairs to the population.",
                "PF_LIMIT": "not live iff no insertion instant AFTER tau1. The T -> infinity "
                            "limit of the threshold rule as 0040 leaves it. 751 excluded.",
                "PF_BRACKET": "the literal text. 18,903 excluded — 25x more, and 1,434 of "
                              "2,402 accounts touched rather than 166.",
                "consequence": "the two readings differ by 0.67 pp on Continued and 0.59 pp "
                               "on Started-and-left — an order of magnitude more than the "
                               "entire threshold interval moves anything. Deleting the "
                               "threshold therefore does NOT by itself close the gate: which "
                               "parameter-free rule is meant still has to be said.",
                "this_instance_does_not_choose": True,
            },
            "paired_test_detects_a_trivial_delta": {
                "what": "the paired account-clustered CI for the 787 -> 2200 delta on "
                        "never-started EXCLUDES zero.",
                "size": boot["paired_clustered_deltas"][
                    "787_to_2200_FULL_CLUSTERED_INTERVAL"]["never_started"],
                "reading": "the settings are nested subsets of the same pairs, so the paired "
                           "delta has almost no variance and a 0.026 pp movement is "
                           "resolvable. Detectable is not the same as material: 0.026 pp is "
                           "3.4% of the width the share itself is known to. State both.",
            },
            "the_threshold_is_inert_by_construction_here": {
                "at_1293": {"excluded_on_a_measured_gap": sens["settings"][
                    "threshold_1293d"]["excluded_measured_gap"],
                    "excluded_on_absent_evidence_edge_case_i": sens["settings"][
                        "threshold_1293d"]["excluded_open_ended"],
                    "measured_gap_share_of_exclusions_pct": round(
                        100.0 * sens["settings"]["threshold_1293d"]["excluded_measured_gap"]
                        / sens["settings"]["threshold_1293d"]["pairs_excluded"], 2)},
                "note": "the edge-case count is CONSTANT in T while the gap-test count falls "
                        "with T, so the split moves with the percentile and no invariance is "
                        "claimed (decisions/0040 SS4).",
            },
            "degeneracy_caveat_travels_with_the_threshold": "above the 99.4188th percentile "
                "the extended-set percentile is itself infinite and the rule collapses into "
                "edge case (i) alone — 0.25% of bootstrap replicates at W=108, 2.80% at "
                "W=213 (decisions/0041 SS2.1). At T -> infinity the rule here IS edge case "
                "(i) alone, and that row is computed above as parameter_free_LIMIT.",
            "derive_apply_mismatch_is_recorded_not_repaired": "decisions/0041 SS3. The "
                "threshold was derived on 147,370; Step 8 will apply liveness to 196,654, "
                "where 1,293 d delivers 1.4418% against a stated 1%. Not repairable inside "
                "Step 7. Routed to Step 14.",
            "continued_and_never_started_are_not_measured_alike": "Continued is a 199-day "
                "statement and never-started a 108-day statement (decisions/0034). This "
                "appears wherever the split is reported, not in a footnote.",
        },
        "judgement_calls_the_spec_does_not_settle": [
            {"call": "POPULATION. Ran on waterfall line 4 less D10 = 147,370.",
             "why": "decisions/0040 SS2 and 0038 SS2.1 require the derivation and application "
                    "populations to be identical, and this is the population the threshold "
                    "under test was derived on. Any other choice would test a threshold "
                    "against a population it was not calibrated for.",
             "what_step_8_would_do_differently": "Step 8's analysis population is the wider "
                    "196,654 (decisions/0041 SS3) — a strict superset that includes waterfall "
                    "lines above 152,126. Those lines carry contaminated T0, and tau1 and "
                    "tau2 are both built from T0, so every outcome state there is computed "
                    "off a contaminated clock. The absolute shares below will move at Step 8. "
                    "The SENSITIVITY verdict is a statement about the shape of the curve, and "
                    "the curve is flat because the exclusion sets are tiny relative to the "
                    "population — 0.87% at 787 d, 0.61% at 2,200 d — which is a property that "
                    "survives enlarging the denominator.",
             "direction_if_wrong": "unknown for the absolute shares; the flatness argument is "
                    "if anything stronger on a larger denominator."},
            {"call": "L2 = 1 EXCLUSION (Step 8 position 2) not applied as a separate filter.",
             "why": "asserted rather than assumed: the Step 2 frame contains ZERO shows with "
                    "s2_L = 1, so the filter is a measured no-op on this population.",
             "what_step_8_would_do_differently": "nothing.",
             "direction_if_wrong": "n/a"},
            {"call": "PARAMETER-FREE RULE computed under BOTH readings, neither adopted.",
             "why": "the two readings are a spec contradiction between decisions/0041 SS4 and "
                    "0040 SS1, not an implementation choice. Reconciling it silently is "
                    "exactly what the dual-run discipline forbids.",
             "what_step_8_would_do_differently": "Step 8 needs ONE rule and cannot proceed "
                    "until this is ruled on.",
             "direction_if_wrong": "PF_BRACKET lowers Continued by 0.67 pp and raises "
                    "Started-and-left by 0.59 pp relative to the 1,293 d threshold rule."},
            {"call": "THRESHOLD COMPARATOR is gap >= T, so a gap exactly equal to T is NOT "
                     "live.",
             "why": "carried unchanged from the a4 derivation, where the ceiling ruling "
                    "(decisions/0025) is justified by exactly this comparator: 'if the test "
                    "excludes a gap at or above the threshold'.",
             "what_step_8_would_do_differently": "should carry the same comparator; it is not "
                    "written into task-sheet.md in operator form, only in prose.",
             "direction_if_wrong": "at T=787 the strict-inequality reading gives the "
                    "identical 1,707, so it does not bind at any tested setting."},
            {"call": "D11 applied to S2 records (179 discarded globally).",
             "why": "decisions/0034 SS5 found D11 was not being applied and that applying it "
                    "moved never-started by 4 pairs on the estimation sample.",
             "what_step_8_would_do_differently": "same. On THIS population D10 already "
                    "guarantees tau2 <= tau_pull, so D11 cannot bite on A or A_H; it is "
                    "applied and reported rather than assumed inert.",
             "direction_if_wrong": "none measurable here"},
            {"call": "CONFIDENCE INTERVALS are account-clustered bootstrap, B = 4,000, "
                     "seed 20260813, resampling the 2,402 accounts.",
             "why": "decisions/0041 SS4 asks for shares and deltas, not intervals. An "
                    "interval was computed anyway because 'insensitive' is a claim about "
                    "size and needs a yardstick. Clustered rather than i.i.d. for the same "
                    "reason the threshold carries a clustered interval. Red Team's criticism "
                    "of the 300-replicate interval in decisions/0040 SS6 is why B is 4,000 "
                    "and why three alternate seeds are reported.",
             "what_step_8_would_do_differently": "Step 9 specifies intervals; the method is "
                    "not fixed anywhere and this is a proposal, not an adoption.",
             "direction_if_wrong": "the verdict rests on the point deltas, which are "
                    "bootstrap-free."},
            {"call": "SHARES ARE COMPUTED ON PAIRS, and excluded pairs are dropped rather "
                     "than bounded.",
             "why": "liveness is a pair-level filter, so the excluded set is a set of "
                    "user-show pairs. Step 9 requires a floor-and-ceiling BOUND on the "
                    "excluded set; that is a Step 9 obligation and this diagnostic does not "
                    "discharge it.",
             "what_step_8_would_do_differently": "n/a — the bound is Step 9's.",
             "direction_if_wrong": "the bound would widen the reported range at every "
                    "setting; it would not change the RANKING or the flatness."},
            {"call": "SWEEP RANGE 30 to 4,000 days on a 5-day grid.",
             "why": "the three required settings are three points; a curve shows whether the "
                    "flatness is a property of the rule or an accident of which points were "
                    "chosen. 4,000 d is past the point where the gap test excludes nothing "
                    "at all.",
             "what_step_8_would_do_differently": "n/a — context only.",
             "direction_if_wrong": "n/a"},
        ],
        "what_this_test_does_not_answer": [
            "Whether the parameter-free rule is RIGHT. It shows only that the threshold's "
            "value does not change the shares, which is an argument against publishing a "
            "free parameter, not an argument for any particular replacement.",
            "Whether liveness itself is warranted. The whole filter — every setting — moves "
            "the shares by less than 0.05 pp against no filter at all, which is a fact about "
            "the filter, not only about its parameter.",
            "Anything about the 91-day arm, Channel A vs Channel B, segment cuts, the "
            "abandonment distribution, or the S3-without-S2 and split-artifact bounds. Those "
            "are Steps 9 through 13 and none of them has run.",
        ],
        "files": {
            "figure": "artifacts/step7-sensitivity-a.png",
            "write_up": "artifacts/step7-sensitivity-a.md",
            "row_level_and_intermediate": "processed/step7/sens_a/ (never leaves this machine)",
            "scripts": ["src/step7_sens_a_pop.py", "src/step7_sens_a_outcomes.py",
                        "src/step7_sens_a_apply.py", "src/step7_sens_a_boot.py",
                        "src/step7_sens_a_fig.py", "src/step7_sens_a_emit.py"],
            "reused_without_recomputation": "processed/step7/a4/pair_bracketing_W108.npz "
                                            "(bracketing gaps, asserted row-aligned)",
        },
    }
    path = os.path.join(ART, "step7-sensitivity-a.json")
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=2)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
