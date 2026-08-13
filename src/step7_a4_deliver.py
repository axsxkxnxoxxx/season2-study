"""Step 7 rerun (decisions/0040), instance A4 — emit artifacts/step7-liveness-a4.json.

Aggregates and counts only. No usernames, no user ids, no individual watch histories.
Zero API calls. PROPOSED, NOT ADOPTED — this is a gate.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a4")
ART = os.path.join(ROOT, "artifacts")

THR_PRIMARY = 1293      # extended reference, decisions/0040 SS2
THR_ALT = 632           # measured-gap-only reference, the superseded 0039 SS5 restriction


def main():
    inst = json.load(open(os.path.join(OUT, "instants_summary.json")))
    br = json.load(open(os.path.join(OUT, "bracketing_W108.json")))
    boot = json.load(open(os.path.join(OUT, "bootstrap.json")))
    arms = json.load(open(os.path.join(OUT, "arms.json")))
    supp = json.load(open(os.path.join(OUT, "supplementary.json")))
    endp = json.load(open(os.path.join(OUT, "interval_endpoints.json")))

    ext = br["applied_extended_reference"]
    alt = br["applied_measured_only_reference"]
    cb = boot["ACCOUNT_CLUSTERED"]

    d = {
        "step": 7,
        "instance": "a4",
        "status": "PROPOSED, NOT ADOPTED. Gate reopened by decisions/0040. "
                  "Awaiting Human Lead approval.",
        "date": "2026-08-13",
        "api_calls": 0,
        "spec_read": [
            "decisions/0040-step7-gate-reopened.md (read first, whole)",
            "task-sheet.md lines 226-285",
            "decisions/0038-step7-frozen-spec.md (SS2.1 as corrected by 0040)",
            "decisions/0037 SS4 (gap unit); decisions/0036 SS2 (rule shape), SS2.3(ii) WITHDRAWN",
            "decisions/0021-step5-contamination-gate.md (reinstated insertion-time ruling)",
            "artifacts/step1-outcome-definition.md lines 685-710 and D10",
        ],

        "THE_ONE_UNSETTLED_QUESTION_THAT_SETS_THE_NUMBER": {
            "question": "which set of pairs forms the reference distribution",
            "candidate_A_EXTENDED": {
                "definition": "every TESTED pair in the post-D10 population: the 128,467 "
                              "measured bracketing gaps plus the 751 open-ended gaps carried "
                              "as +infinity",
                "n": 129218,
                "threshold_days": THR_PRIMARY,
                "basis": "decisions/0040 SS2 — after D10 the open-ended share is under 1%, the "
                         "extended 99th is finite, 'an infinite gap fails a finite threshold on "
                         "its own', and the restriction 0039 SS5 called forced is dissolved. "
                         "Also the only reading under which derivation and application sets are "
                         "the same set (0038 SS2.1).",
            },
            "candidate_B_MEASURED_ONLY": {
                "definition": "the finite bracketing gaps only",
                "n": 128467,
                "threshold_days": THR_ALT,
                "basis": "task-sheet.md line 266, which still carries decisions/0039 SS5's "
                         "restriction verbatim. 0039 is SUSPENDED by 0040 and its stated reason "
                         "for the restriction ('a 99th percentile over the extended set would "
                         "itself be infinite') is false on this population.",
            },
            "A4_PROPOSES": "candidate A, 1,293 days",
            "why": "task-sheet.md states that decisions/ is authoritative over it where the two "
                   "disagree. decisions/0040 postdates and suspends 0039, and reasons explicitly "
                   "toward the extended set. Candidate B is reported in full at every number "
                   "below so the Human Lead can select B without a rerun.",
            "DEFECT_TO_REPORT": "decisions/0040 SS4 corrected four superseded figures in "
                                "task-sheet.md and did not correct line 266, which still states "
                                "the suspended entry's reference set as operative spec. Step 8 "
                                "launches off the task sheet.",
            "size_of_the_lever": {
                "threshold_days": [THR_PRIMARY, THR_ALT],
                "pairs_excluded": [ext["not_live_total"], alt["not_live_total"]],
                "excluded_share_of_post_D10_population": [
                    ext["realised_rate_vs_post_D10_population"],
                    alt["realised_rate_vs_post_D10_population"]],
            },
        },

        "population": br["population"],
        "d10_effect_by_class": supp["d10_effect_by_class"],
        "pair_counts_by_class_at_W108": br["classes_at_W108"],

        "PROPOSAL_extended_reference": {
            "threshold_days": THR_PRIMARY,
            "p99_raw_days": br["threshold_panel"]["extended"]["p99_raw_days"],
            "percentile": 99.0,
            "rounding": "ceiling (decisions/0025)",
            "weighting": "one gap per pair (decisions/0038 SS3)",
            "reference_population": "the 152,126 (waterfall line 4) LESS D10 right-censoring "
                                    "= 147,370; tested subset 129,218",
            "W_days": 108,
            "H_days": 91,
            "threshold_is_a_function_of_W": True,
            "account_clustered_95_CI_days": cb["extended"]["ci95_ceil_days"],
            "bootstrap_replicates": boot["replicates"],
            "bootstrap_seed": boot["seed"],
            "infinite_replicates": cb["extended_infinite_replicates"],
            "infinite_replicate_share": cb["extended_infinite_replicate_share"],
            "NEVER_REPORT_BARE": "report 1,293 d with the account-clustered interval, never as "
                                 "a point estimate. Same treatment as W = 108 +/- 18.",
            "applied": ext,
        },

        "ALTERNATIVE_measured_only_reference": {
            "threshold_days": THR_ALT,
            "p99_raw_days": br["threshold_panel"]["measured_only"]["p99_raw_days"],
            "account_clustered_95_CI_days": cb["measured_only"]["ci95_ceil_days"],
            "bootstrap_replicates": boot["replicates"],
            "applied": alt,
            "note": "this is bit-identical to decisions/0039's approved 631.8031044554186 -> "
                    "632 d. D10 removes 1,163 measured-gap pairs and does not move this "
                    "threshold at all, because the selected order statistic sits in a tie "
                    "plateau of 156 pairs. What D10 and the 0036 SS2.3(ii) withdrawal change is "
                    "the EXCLUSION COUNT, not this number.",
        },

        "RULE_STATEMENT": {
            "text": (
                "A USER-SHOW PAIR is LIVE unless the account's insertion history shows a gap of "
                "at least T days bracketing that pair's own tau1 = [[T0]] + W*24h. Concretely: "
                "build the account's sweep-wide sequence of record insertion instants - every "
                "record, all shows and movies, estimated from the STORED Step 5 isotonic play-id "
                "curve, which is read and never refitted - sort ascending, collapse runs of "
                "exactly equal instants, and take the last distinct instant at or before tau1 "
                "and the first distinct instant after tau1. If both exist, the bracketing gap is "
                "their difference in continuous days. If there is no instant after tau1 the "
                "bracketing gap is INFINITE. If there is no instant at or before tau1 the pair "
                "is LIVE and is not tested, because decisions/0021 rules that any record "
                "inserted after the window closed proves the account was alive whatever date it "
                "claims. The pair is NOT LIVE iff the bracketing gap is >= T. The test is "
                "applied to that one gap and to no other gap in the sweep. Evidence is "
                "account-wide; the test is clock-start-relative and clock start is pair-"
                "specific, so one account may be live for one show and not for another. No user "
                "is ever dropped wholesale."
            ),
            "T_proposed_days": THR_PRIMARY,
            "boundary_convention": "not live iff gap >= T (decisions/0025 reason (a)); "
                                   "the spec does not state >= vs >, this is A4's call",
            "tau1_boundary_convention": "an instant exactly equal to tau1 counts as 'at or "
                                        "before tau1' (searchsorted side='right')",
            "anchored_at": "tau1 only. tau2 plays no part in liveness (decisions/0034).",
            "filter_level": "PAIR, never user (decisions/0036 SS3)",
        },

        "EDGE_CASE_I_IS_IT_STILL_NEEDED": supp["edge_case_i_redundancy"],

        "EDGE_CASE_II_WITHDRAWN_WHAT_IT_COST": {
            "pairs_returned_to_the_population": br["classes_at_W108"][
                "no_instant_at_or_before_tau1_LIVE_per_0021"],
            "they_are_LIVE": True,
            "authority": "decisions/0021, approved gate 2 of 5, reinstated by 0040 SS1",
            "corroboration_of_0040s_premise": {
                "accounts_with_no_insertion_instants": inst["accounts_with_zero_gaps"],
                "minimum_gaps_per_account": inst["min_gaps_per_account"],
                "reading": "every pair in this bucket has insertion instants AFTER tau1 by "
                           "construction, so 0021 rules them live. 0040 SS1's premise is "
                           "confirmed on this data: no account in the sweep has zero instants "
                           "and the minimum is 3 gaps.",
            },
            "effect_on_the_filter": {
                "approved_0039_not_live_total_on_152126": 23772,
                "a4_not_live_total_extended_reference": ext["not_live_total"],
                "a4_not_live_total_measured_only_reference": alt["not_live_total"],
                "reduction": "the liveness filter's cost falls by roughly 95%, from 23,772 "
                             "pairs to 1,282 (or 2,026 under candidate B). Step 9's liveness "
                             "bound shrinks accordingly and Step 9 must recompute it.",
            },
        },

        "realised_rate_against_both_denominators": {
            "extended_reference_T_1293": {
                "of_measured_gap_pairs": ext["realised_rate_vs_measured_gap_pairs"],
                "of_the_tested_extended_set": ext["realised_rate_vs_extended_set"],
                "of_the_post_D10_population": ext["realised_rate_vs_post_D10_population"],
            },
            "measured_only_reference_T_632": {
                "of_measured_gap_pairs": alt["realised_rate_vs_measured_gap_pairs"],
                "of_the_tested_extended_set": alt["realised_rate_vs_extended_set"],
                "of_the_post_D10_population": alt["realised_rate_vs_post_D10_population"],
            },
            "reading": "candidate A delivers the stated 1% against the set the percentile was "
                       "taken on (0.9921%). Candidate B delivers 0.9925% of measured-gap pairs "
                       "but 1.5679% of the pairs the rule actually tests, because the "
                       "open-ended pairs are excluded from the reference and then excluded by "
                       "the rule. That is the calibrate-on-one-set-apply-to-another shape "
                       "0037 withdrew, in miniature.",
        },

        "bracketing_gap_distribution_days": br["bracketing_gap_distribution_days"],
        "pooled_gap_distribution_days_CONTEXT": {
            "n_gaps": inst["n_pooled_gaps"],
            "percentiles": inst["pooled_gap_days_percentiles"],
            "sub_second_share": inst["pooled_gap_sub_second_share"],
        },
        "percentile_convention_panels": {
            "extended": br["p99_percentile_convention_panel_extended"],
            "measured_only": br["p99_percentile_convention_panel_measured_only"],
            "note": "all eight conventions agree to the digit on both sets, because the "
                    "selected order statistic sits in a tie plateau",
        },
        "order_statistic_ties": supp["order_statistic_ties"],

        "MANDATORY_DISCLOSURE_1_quota_property": {
            "statement": (
                "The level is set by the exclusion rate, not by any feature of the data. The "
                "percentile is taken on the very distribution the test is applied to, so "
                "choosing the 99th mechanically fixes the exclusion rate at 1% and the "
                "threshold is whatever number delivers it. Any percentile would have produced a "
                "self-consistent answer. 1,293 days is not a point where account behaviour "
                "changes; it is the 1% quota's price tag. This is the price of a calibrated "
                "rate and it is disclosed, not argued away (decisions/0038 SS4)."
            ),
            "evidence_threshold_moves_with_the_quota_extended_reference": {
                q: v.get("threshold_days")
                for q, v in br["inertness_by_percentile_extended_reference"].items()
            },
            "evidence_threshold_moves_with_the_quota_measured_only": {
                q: v["threshold_days"]
                for q, v in supp["inertness_measured_only_reference"].items()
            },
            "what_survives": "0036 SS1's conservative-direction argument still points UP for "
                             "the GAP TEST, because a false-dead removes a pair and the "
                             "liveness exclusion already biases the never-started share down "
                             "(Step 14 bias 2). It identifies a direction, not a level. Per "
                             "0040 SS3 it is WITHDRAWN as a justification for the edge-case "
                             "branches and is not cited beyond the gap test here.",
        },

        "MANDATORY_DISCLOSURE_2_inertness_MEASURED_ON_A4s_POPULATION": {
            "no_invariance_is_claimed": True,
            "statement": (
                "Measured on A4's post-D10 population at the proposed 99th under the extended "
                "reference: the measured-gap test does 531 of 1,282 exclusions (41.42%) and the "
                "remaining evidence-absence branch - open-ended gaps - does 751 (58.58%). Under "
                "candidate B at 632 d the split is 1,275 of 2,026 (62.93%) against 751 (37.07%). "
                "The share is NOT invariant across percentiles and cannot be: the "
                "evidence-absence count is constant in the percentile while the gap-test count "
                "is a function of it."
            ),
            "how_this_differs_from_the_record": (
                "decisions/0038 SS5 as corrected by 0039 published 5.37% / 94.63% on the "
                "pre-D10 152,126. That figure is gone, not merely moved: 94.63% of it was "
                "0036 SS2.3(ii)'s 18,250-pair bucket, which 0040 SS1 withdrew and returned to "
                "the population as LIVE, and most of the rest was right-censoring that D10 "
                "removes. There is no longer an edge-case branch that dominates the filter."
            ),
            "extended_reference_by_percentile": br[
                "inertness_by_percentile_extended_reference"],
            "measured_only_reference_by_percentile": supp[
                "inertness_measured_only_reference"],
        },

        "ACCOUNT_CLUSTERED_BOOTSTRAP": {
            "replicates": boot["replicates"],
            "seed": boot["seed"],
            "rng": boot["rng"],
            "clustering_unit": boot["clustering_unit"],
            "accounts_resampled": boot["population"]["accounts"],
            "why_clustered": boot["why_clustered"],
            "tie_structure": boot["tie_structure"],
            "extended_reference": {
                "point_days": THR_PRIMARY,
                "ci95_ceil_days": cb["extended"]["ci95_ceil_days"],
                "ci95_raw_days": cb["extended"]["ci95_raw_days"],
                "sd_days": cb["extended"]["sd_raw_days"],
                "infinite_replicates": cb["extended_infinite_replicates"],
            },
            "measured_only_reference": {
                "point_days": THR_ALT,
                "ci95_ceil_days": cb["measured_only"]["ci95_ceil_days"],
                "ci95_raw_days": cb["measured_only"]["ci95_raw_days"],
                "sd_days": cb["measured_only"]["sd_raw_days"],
            },
            "iid_for_contrast_only": boot["IID_FOR_CONTRAST_NOT_TO_BE_REPORTED"],
            "endpoint_stability_by_B_and_seed": {
                "table": json.load(open(os.path.join(OUT, "bootstrap_stability.json"))),
                "reading": (
                    "Red Team's objection is confirmed and quantified. At B = 300 the "
                    "measured-only interval's upper endpoint moves 741 -> 812 days on the seed "
                    "alone; at B = 2,000 it sits in 829-836 and the lower endpoint in 542-556. "
                    "The extended interval's upper endpoint is pinned at 2,200 across every B "
                    "and seed, which is a tie plateau rather than precision."
                ),
            },
            "arm_level_intervals_use_B_1000": (
                "the per-arm CIs in STEP_13_PER_ARM_REFIT are B = 1,000 and resample each arm's "
                "own reference set directly; the headline interval here is B = 2,000 and "
                "resamples the tested set once, dropping open-ended values afterwards for the "
                "measured-only variant. The two designs differ slightly and their numbers are "
                "not interchangeable."
            ),
            "vs_the_suspended_approval": (
                "decisions/0039 approved 632 d with a clustered [528, 787] from B = 300. On "
                "A4's post-D10 population at B = 2,000 the same quantity is 632 d with "
                f"{cb['measured_only']['ci95_ceil_days']}. The point estimate is bit-identical; "
                "the interval moves because 300 replicates put the endpoints on the 7th and 8th "
                "order statistics. Red Team's objection is confirmed, and the wider interval is "
                "the honest one."
            ),
        },

        "FILTER_COST_ACROSS_THE_INTERVAL_for_0040_SS6": {
            "question": "0040 SS6 asks Step 9 whether the threshold is load-bearing at all. "
                        "These are the inputs Step 9 needs; Step 7 does not answer it.",
            "by_threshold": endp,
            "reading": "across the whole account-clustered interval of either candidate the "
                       "liveness filter removes between 897 and 2,454 pairs of 147,370 - "
                       "0.61% to 1.67% of the population. Whether that band moves the headline "
                       "is Step 9's measurement, not Step 7's claim.",
        },

        "STEP_13_PER_ARM_REFIT": {
            "spec": "decisions/0038 SS6 requires a refit per arm with the realised rate for "
                    "each; decisions/0027 sets the arms; H is held constant at 91 across every "
                    "arm; D10 is re-run at each arm because D10 is a function of W.",
            "arms_run": sorted(int(k) for k in arms["arms"]),
            "arm_list_note": "0027's union range starts at 38 and the brief names 46-107 plus "
                             "150 and 213; A4 runs a superset so the response is traced, not "
                             "interpolated between endpoints.",
            "by_arm": arms["arms"],
            "W_coupling": arms["W_coupling"],
            "frozen_threshold_counterfactual": arms["frozen_threshold_counterfactual"],
        },

        "weighting_sensitivity_NOT_ADOPTED": br["weighting_sensitivity_NOT_ADOPTED"],
        "withdrawn_pooled_basis_for_continuity": br["withdrawn_pooled_basis"],
        "open_ended_bucket_diagnostic_post_D10": br["open_ended_bucket_diagnostic_post_D10"],

        "provenance": {
            "records_scanned": inst["n_records"],
            "accounts_in_sweep": inst["n_accounts"],
            "distinct_insertion_instants": inst["n_distinct_instants"],
            "exact_ties_collapsed": inst["collapsed_exact_ties"],
            "gaps_per_account_median": inst["gaps_per_account_median"],
            "calibration_curve": "processed/step5/calibration.npz, READ NOT REFITTED",
            "rid_clamped_below_first_knot": inst["rid_below_first_knot_clamped"],
            "rid_clamped_above_last_knot": inst["rid_above_last_knot_clamped"],
            "waterfall_reproduced": br["population"]["waterfall_computed"],
            "sweep_first_instant_utc": inst["sweep_first_instant_utc"],
            "sweep_last_instant_utc": inst["sweep_last_instant_utc"],
            "scripts": [
                "src/step7_a4_instants.py", "src/step7_a4_bracketing.py",
                "src/step7_a4_bootstrap.py", "src/step7_a4_arms.py",
                "src/step7_a4_supp.py", "src/step7_a4_figures.py",
                "src/step7_a4_deliver.py",
            ],
            "chart": "artifacts/step7-gap-distribution-a4.png",
        },

        "corroborations_and_divergences_against_the_record": {
            "reproduced_exactly": {
                "waterfall": [201900, 178165, 155131, 152126, 128099],
                "pooled_p99_days": 3.4431932062376234,
                "pooled_p99_ceil_days": 4,
                "gaps_per_account_median": 7812.0,
                "measured_only_p99_raw_days": 631.8031044554186,
                "largest_tie_group": boot["tie_structure"]["largest_tie_group"],
                "pre_D10_class_counts": supp["d10_effect_by_class"]["before_152126"],
            },
            "divergences_from_figures_in_the_record": {
                "0040_SS2_open_ended_after_D10": {
                    "record": "894 / 130,524 = 0.685%",
                    "a4_measures": "751 / 129,218 = 0.5812%",
                    "cause": "the record's figure subtracts only the 3,352 tau1-past-pull pairs "
                             "from the open-ended bucket. D10 is 91 days stricter than that and "
                             "removes 3,495 open-ended, 1,163 measured and 98 no-pre-tau1 "
                             "pairs. 0040's CONCLUSION is unaffected - the share is well under "
                             "1% and the extended 99th is finite.",
                },
                "task_sheet_line_242_bracketing_gaps_exceeding_the_pooled_99th": {
                    "record": "34.12% on the 152,126",
                    "a4_measures": br["withdrawn_pooled_basis"][
                        "bracketing_pairs_failing_pooled_threshold_rate"],
                    "cause": "different population - A4 measures on the post-D10 set",
                },
                "task_sheet_line_246_weighting_lever": {
                    "record": "190 d on the frozen population",
                    "a4_measures": br["weighting_sensitivity_NOT_ADOPTED"][
                        "distinct_account_gap_p99_ceil_days"],
                    "cause": "post-D10 population",
                },
                "task_sheet_line_235_W_coupling": {
                    "record": "576 -> 697 days across the arms",
                    "a4_measures_measured_only": arms["W_coupling"][
                        "MEASURED_ONLY_reference_threshold_span"],
                    "a4_measures_extended": arms["W_coupling"][
                        "EXTENDED_reference_threshold_span"],
                    "cause": "post-D10 population and a wider arm list",
                },
                "task_sheet_line_267_approved_counts": {
                    "record": "live 128,354; measured-gap 1,276; no-after 4,246; "
                              "no-before 18,250, on the 152,126",
                    "a4_measures": "on the post-D10 147,370: live 146,088; measured-gap 531; "
                                   "open-ended 751; no-before 18,152 and LIVE. The no-before "
                                   "bucket is no longer an exclusion at all.",
                    "cause": "0040 SS1 and SS2, both of which this run implements",
                },
                "task_sheet_line_248_inertness": {
                    "record": "5.37% / 94.63% on the 152,126 at the 99th",
                    "a4_measures": "41.42% / 58.58% (extended) or 62.93% / 37.07% "
                                   "(measured-only) on the post-D10 population",
                    "cause": "0040 SS1 removed the branch that supplied 94.63%",
                },
            },
        },

        "JUDGEMENT_CALLS_THE_SPEC_DOES_NOT_SETTLE": [
            "1. WHICH REFERENCE SET. Extended (1,293 d) vs measured-gap-only (632 d). 0040 SS2 "
            "reasons toward extended; task-sheet.md line 266 still states measured-only. "
            "Largest lever in the step. A4 proposes extended and reports both in full.",
            "2. np.interp CLAMPING. 1,862 records fall below the first calibration knot and "
            "5,094 above the last. np.interp clamps them to the endpoint knot times, so they "
            "become exact ties and collapse under 0037's rule. Extrapolating or dropping them "
            "instead would change every number downstream. The spec says read the curve; it "
            "does not say what to do outside its support.",
            "3. AN ABSENT SUCCESSOR INSTANT IS SCORED AS AN INFINITE GAP, not as undefined. "
            "This is what makes edge case (i) redundant rather than a separate ruling, and it "
            "is a definition A4 supplies.",
            "4. BOUNDARY: not live iff gap >= T. 0025 reason (a) implies it; no entry states "
            "it. An instant exactly equal to tau1 is treated as 'at or before tau1'.",
            "5. DERIVATION = APPLICATION holds on the TESTED set (129,218), not on the full "
            "post-D10 population (147,370). The 18,152 no-pre-tau1 pairs are in the application "
            "population and are unconditionally live, so they contribute no gap to the "
            "reference. 0038 SS2.1's identity requirement is satisfiable only up to that "
            "subset, and A4 states so rather than claiming an identity it does not have.",
            "6. PER-ARM D10. D10 is a function of W, so Step 13's arms each re-run it and each "
            "derives on its own post-D10 population. Freezing D10 at W = 108 across arms would "
            "hold the population constant instead. The spec requires derive-after-D10 but does "
            "not say which of these it means for the arms.",
            "7. BOOTSTRAP CLUSTERING UNIT is the account. A pair also belongs to a show, and "
            "show-level clustering is not modelled here; W's own interval is show-clustered.",
            "8. THE ARM LIST is a superset of the brief's (38 and 60/75/91/120/180 added).",
            "9. THE 99th PERCENTILE is not A4's call and was not re-examined (task-sheet "
            "line 251).",
        ],

        "GATE_DISCIPLINE": "A4 proposes and stops. Nothing is adopted here, Step 8 is not "
                           "begun, and no approval is recorded by this instance.",
    }

    path = os.path.join(ART, "step7-liveness-a4.json")
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
    print("wrote", path)


if __name__ == "__main__":
    main()
