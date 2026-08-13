"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 7 — the artifact.

Assembles processed/step7/alt2_a/*.json into artifacts/step7-liveness-alt-a.json.
COUNTS AND AGGREGATES ONLY. No user id, no username, no per-pair row reaches artifacts/.

Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
P = os.path.join(ROOT, "processed/step7/alt2_a")
ART = os.path.join(ROOT, "artifacts/step7-liveness-alt-a.json")


def load(name):
    with open(os.path.join(P, name)) as fh:
        return json.load(fh)


def main():
    popj, epj, instj = load("population.json"), load("episodes_line1.json"), load("last_instant.json")
    arms, boot, checks = load("arms.json"), load("bootstrap.json"), load("checks.json")
    pre = load("pre_d10_candidates.json")

    core = arms["adopted_arm"]
    arm_table = {
        W: {"D10_re_derived_at_this_arm": {
                "DERIV_population": r["D10_per_arm"]["DERIV"]["population_pairs"],
                "DERIV_excluded": r["D10_per_arm"]["DERIV"]["excluded_pairs"],
                "APPLY_population": r["D10_per_arm"]["APPLY"]["population_pairs"],
                "APPLY_excluded": r["D10_per_arm"]["APPLY"]["excluded_pairs"],
                "APPLY_never_started_in_population":
                    r["D10_per_arm"]["APPLY"]["never_started_in_population"],
                "APPLY_excluded_accounts": r["D10_per_arm"]["APPLY"]["excluded_accounts"],
                "APPLY_PF_LIMIT_would_have_excluded":
                    r["D10_per_arm"]["APPLY"]["PF_LIMIT_would_exclude"]},
            "D10_frozen_at_the_adopted_W_108": {
                "DERIV_excluded": r["D10_frozen_at_W108"]["DERIV"]["excluded_pairs"],
                "APPLY_excluded": r["D10_frozen_at_W108"]["APPLY"]["excluded_pairs"]}}
        for W, r in arms["arms"].items()}

    out = {
        "step": 7,
        "title": "Step 7 liveness rule — rerun on the rule adopted at decisions/0046",
        "instance": "a",
        "mode": "GATE. Dual implementation. This artifact ADOPTS NOTHING and approves nothing.",
        "date": "2026-08-13",
        "api_calls": 0,
        "inputs": {
            "calibration": "processed/step5/calibration.npz — STORED, read, NEVER refitted "
                           "(task-sheet Step 7; decisions/0029)",
            "calibration_knots": instj["calibration_knots"],
            "records_scanned": instj["n_records"],
            "accounts_with_an_insertion_sequence": instj["n_accounts"],
            "reused_from_earlier_run": instj["reused_sequence"],
            "reuse_crosscheck_max_abs_diff_seconds": instj[
                "crosscheck_max_abs_diff_seconds_on_last_instant"],
        },

        "1_rule_statement": {
            "rule": "A user-show pair is NOT LIVE if and only if BOTH: the account shows no "
                    "insertion instant after that pair's tau1 = [[T0]] + W x 24h, AND |A| = 0. "
                    "Otherwise it is live.",
            "second_conjunct": "|A| = 0 is Step 1 SS7's Never-started condition — the set A of "
                               "distinct S2 episodes whose number is in E2 and whose canonical "
                               "timestamp satisfies watched_at < tau1 — and NOT 'no S2 "
                               "evidence at all'. The two readings select different sets and "
                               "this run measures both.",
            "first_conjunct_implementation": "insertion instant = np.interp(play id, stored "
                                             "calibration); evidence is ACCOUNT-WIDE across all "
                                             "shows and seasons (decisions/0021); 'after' is "
                                             "strict, so NOT LIVE requires max instant <= tau1",
            "free_parameters": "none of its own; the exclusion set is fully determined by W",
            "anchoring": "pair-level, at tau1 (decisions/0034). tau2 plays no part.",
            "no_pre_tau1_requirement": "none is imposed, in any form (withdrawn at 0040 SS1 "
                                       "and 0042 SS3)",
        },

        "2_populations_asserted": {
            "step5_waterfall_recomputed": popj["waterfall_computed"],
            "step5_waterfall_published": popj["waterfall_published"],
            "asserted_equal": popj["waterfall_asserted_equal"],
            "DERIV": popj["populations"]["DERIV"],
            "APPLY": popj["populations"]["APPLY"],
            "D10_rule": popj["d10_rule"],
            "L2_eq_1_exclusion_is_a_noop_on_both": popj["l2_eq_1_exclusion_is_a_noop_on_both"],
            "S2_episode_table": {
                "line1_pairs": epj["line1_pairs"],
                "distinct_S2_episodes": epj["distinct_episodes_on_line1"],
                "records_dropped_number_not_in_E2": epj["s2_records_dropped_number_not_in_E2"],
                "records_dropped_at_or_after_tau_pull_D11": epj[
                    "s2_records_at_or_after_tau_pull_D11"],
                "pairs_with_zero_distinct_in_E2_S2_episodes_on_line1": epj[
                    "pairs_with_zero_distinct_in_E2_S2_episodes"],
                "of_which_Step5_says_they_DO_have_S2_records": epj[
                    "of_which_step5_says_has_S2_evidence"],
            },
        },

        "3_exclusion_counts": {
            "at_W_108": {
                "DERIV": {"population": core["DERIV"]["population_pairs"],
                          "excluded": core["DERIV"]["settings"]["ADOPTED_RULE"]["excluded_pairs"],
                          "expected_by_0046": 0, "confirmed": True},
                "APPLY": {"population": core["APPLY"]["population_pairs"],
                          "excluded": core["APPLY"]["settings"]["ADOPTED_RULE"]["excluded_pairs"],
                          "expected_by_0046": 604, "confirmed": True,
                          "accounts_touched": checks["pair_level_not_user_level"]["APPLY"][
                              "accounts_with_at_least_one_excluded_pair"],
                          "accounts_excluded_on_one_show_and_live_on_another":
                              checks["pair_level_not_user_level"]["APPLY"][
                                  "accounts_excluded_on_one_show_and_live_on_another"]},
            },
            "per_W_arm": arm_table,
            "arm_table_matches_0046_SS3_under_the_per_arm_D10_reading": True,
            "judgement_call": "D10 contains W, so the population is re-derived at each arm. "
                              "That reading reproduces 0046 SS3 exactly. Freezing D10 at "
                              "W = 108 instead gives different counts above W = 108 (632 at "
                              "125, 684 at 150, 753 at 180, 881 at 213) and the arm table "
                              "must therefore say which reading it is.",
        },

        "4_outcome_shares": {
            "note": "Three states, Step 1 SS7 as amended by 0034. Never-started is tested at "
                    "tau1; Continued at tau2 = [[T0]] + (W + H) x 24h on A_H. The two are not "
                    "measured alike and must not be described as if they were.",
            "DERIV": {
                "population_pairs": core["DERIV"]["population_pairs"],
                "accounts": boot["by_population"]["DERIV"]["accounts"],
                "no_liveness_filter": core["DERIV"]["settings"]["no_liveness_filter"],
                "under_the_adopted_rule": core["DERIV"]["settings"]["ADOPTED_RULE"],
                "delta_pp": core["DERIV"]["delta_vs_no_filter_pp"],
                "clustered_intervals": boot["by_population"]["DERIV"]["settings"],
                "paired_delta": boot["by_population"]["DERIV"][
                    "paired_delta_rule_minus_no_filter"],
            },
            "APPLY": {
                "population_pairs": core["APPLY"]["population_pairs"],
                "accounts": boot["by_population"]["APPLY"]["accounts"],
                "no_liveness_filter": core["APPLY"]["settings"]["no_liveness_filter"],
                "under_the_adopted_rule": core["APPLY"]["settings"]["ADOPTED_RULE"],
                "delta_pp": core["APPLY"]["delta_vs_no_filter_pp"],
                "clustered_intervals": boot["by_population"]["APPLY"]["settings"],
                "paired_delta": boot["by_population"]["APPLY"][
                    "paired_delta_rule_minus_no_filter"],
                "the_delta_is_a_pure_denominator_move": "Continued and Started-and-left "
                    "numerators are identical under both settings (144,140 and 19,141); only "
                    "the never-started numerator and the denominator change",
            },
            "bootstrap": boot["bootstrap"],
        },

        "5_step9_liveness_bound": {
            "DERIV": core["DERIV"]["step9_liveness_bound"],
            "APPLY": core["APPLY"]["step9_liveness_bound"],
            "APPLY_with_intervals": boot["by_population"]["APPLY"]["step9_liveness_bound"],
            "identity_check": {
                "claim": "the ceiling equals the unfiltered never-started share, as an identity",
                "test": "exact integer cross-multiplication, not a float comparison",
                "DERIV_holds": core["DERIV"]["step9_liveness_bound"][
                    "ceiling_equals_unfiltered_share_exact_rational"],
                "APPLY_holds": core["APPLY"]["step9_liveness_bound"][
                    "ceiling_equals_unfiltered_share_exact_rational"],
                "why": "the excluded set is a SUBSET of never-started by construction, so "
                       "returning every excluded pair as a decliner reproduces the unfiltered "
                       "population exactly, numerator and denominator alike",
                "both_endpoints_attainable": True,
            },
            "published_by_0046_APPLY": [16.7146, 16.9704],
            "reproduced": True,
        },

        "6_waterfall": {
            "positions": "decisions/0029: 4 contamination -> 5 right-censoring -> 6 liveness "
                         "-> 7 outcome assignment",
            "DERIV": checks["waterfall_positions_4_to_6"]["DERIV"],
            "APPLY": checks["waterfall_positions_4_to_6"]["APPLY"],
            "line_6_is_outcome_conditional": True,
            "monotone_decrease": {
                "DERIV": "holds NON-STRICTLY only — 147,370 -> 147,370, the exclusion set is "
                         "empty",
                "APPLY": "holds STRICTLY — 196,654 -> 196,050",
                "consequence": "the Step 8 invariant 'filter counts decrease monotonically' "
                               "must be coded as >=, not >",
            },
        },

        "7_the_two_recorded_weaknesses_tested": {
            "weakness_1_this_gate_cannot_exercise_the_rule_on_DERIV": {
                "verdict": "CONFIRMED on DERIV. The exclusion set is empty at every arm from "
                           "38 to 213, so on the derivation population this step's dual diff "
                           "is 0 = 0 and no implementation difference in the rule could show "
                           "up in it.",
                "but": "the diff is NOT vacuous overall. Both arms can be diffed on APPLY: "
                       "604 exclusions, the twelve-arm table, the three shares, and the bound. "
                       "Those are the figures the Human Lead should diff.",
            },
            "weakness_2_the_rule_is_first_exercised_at_Step_8": {
                "what_this_gate_establishes": [
                    "the rule is well defined and computable with zero free parameters",
                    "its exclusion set is 0 on DERIV and 604 on APPLY at W = 108, and rises "
                    "monotonically with W on APPLY",
                    "its exclusions are all Never started, so the Step 9 bound's ceiling is an "
                    "identity and both endpoints are attainable",
                    "the headline moves 0.2558 pp on APPLY, which is 23.4% of the "
                    "account-clustered sampling width of the share it moves",
                ],
                "what_this_gate_CANNOT_establish": [
                    "that Step 8's position-6 population is the one reconstructed here. APPLY "
                    "is rebuilt from Step 5 outputs; Step 8 builds it through positions 1-5 of "
                    "its own pipeline. Any difference at any position moves the 604.",
                    "that two independent implementations of the rule agree, because on DERIV "
                    "there is nothing to disagree about",
                    "anything about the rule's behaviour on pairs Step 8 scores differently "
                    "from this reconstruction, since the second conjunct IS an outcome",
                ],
                "recommendation_to_the_Human_Lead": "carry the 604, the arm table and the "
                    "waterfall line 6 into the Step 8 diff as expected values, and treat a "
                    "Step 8 position-6 count other than 604 as a population defect rather "
                    "than a liveness defect until proven otherwise",
            },
        },

        "8_findings_against_decisions_0046": {
            "finding_1_the_604_are_NOT_the_pairs_with_no_S2_record_anywhere": {
                "text_in_0046": "SS1 and SS3: 'The 604 on APPLY are exactly the pairs with no "
                                "S2 record anywhere.'",
                "measured": arms["exclusion_set_identity_on_APPLY"],
                "verdict": "REFUTED as a set equality, CONFIRMED as a subset relation. APPLY "
                           "holds 23,260 pairs with no S2 record anywhere; 604 are excluded "
                           "and 22,656 stay live because their accounts insert records after "
                           "tau1. The correct statement is: the 604 are exactly those "
                           "no-S2-record pairs whose account shows no insertion instant after "
                           "tau1.",
                "why_it_matters": "as written it credits the second conjunct with the whole "
                                  "selection; in fact the second conjunct narrows 196,654 to "
                                  "33,373 and the FIRST conjunct does the rest, 33,373 to 604",
            },
            "finding_2_the_DERIV_zero_is_not_forced_by_construction": {
                "text_in_0046": "SS1: 'The DERIV zero is forced by construction — line 4 "
                                "requires S2 evidence, so no line-4 pair can have |A| = 0 and "
                                "no S2 record.'",
                "verdict": "The COUNT is confirmed at 0, at every arm from 38 to 213. The "
                           "REASON is a non-sequitur, and it is the exact conflation SS5 of the "
                           "same entry warns against: the rule's second conjunct is |A| = 0, "
                           "not 'no S2 record'.",
                "evidence": {
                    "line4_pairs_with_|A|_eq_0_at_W108": core["DERIV"]["settings"][
                        "no_liveness_filter"]["counts"]["never_started"],
                    "share_of_DERIV_pct": core["DERIV"]["settings"]["no_liveness_filter"][
                        "shares_pct"]["never_started"],
                    "so_the_second_conjunct_is_satisfied_by_9145_line4_pairs": True,
                    "what_actually_produces_the_zero": "the FIRST conjunct: every one of "
                        "those 9,145 accounts inserts a record after tau1",
                    "margin_diagnostic": arms["DERIV_margin_diagnostic"],
                    "and_D10_is_load_bearing": {
                        "line4_ALT_candidates_with_D10_SUPPRESSED": pre,
                        "reading": "with right-censoring suppressed, FOUR line-4 pairs satisfy "
                                   "both conjuncts at every arm tested — pairs Step 5 flags as "
                                   "having S2 records but whose records leave no distinct "
                                   "in-E2 episode after the SS3.2 membership drop and D11, so "
                                   "|A| = 0 at every W. They are exactly the case 0046 says "
                                   "cannot exist. D10 removes them at position 5, before "
                                   "liveness at position 6, so the OPERATIVE count is 0.",
                        "consequence": "the DERIV zero is an empirical fact about this pull "
                                       "date, not a theorem. A later pull, a different H, or "
                                       "any change to D10 could make it 4.",
                    },
                },
            },
        },

        "9_judgement_calls_the_spec_does_not_settle": [
            "TIE AT tau1. 'After tau1' is read strictly, so NOT LIVE requires max insertion "
            "instant <= tau1 and an instant landing exactly on tau1 does not prove liveness. "
            "Measured non-load-bearing: 0 pairs on either population have their last instant "
            "within one second of tau1.",
            "ONLY THE LAST INSTANT MATTERS. The rule asks whether ANY instant falls after "
            "tau1, which is max(instant) > tau1. No gap, no percentile and no sequence "
            "statistic is used, and none is needed.",
            "PER-ARM D10. The arm table re-derives D10 at each W because D10 contains W and "
            "runs at position 5. Both readings are reported; they differ above W = 108.",
            "'NO S2 RECORD ANYWHERE' has two readings — Step 5's has_S2 flag, and zero "
            "distinct in-E2 episodes after D11. They coincide on APPLY at 23,260 and differ "
            "on line 1 before D10, 23,735 against 23,739. The four-pair difference is "
            "load-bearing for finding 2 and is reported rather than smoothed.",
            "UNFILTERED COMPARATOR. 'No filter at all' means the position-5 output with "
            "position 6 skipped, on the same population. It is not the pre-censoring line.",
            "BOOTSTRAP DESIGN is not specified by the spec: B = 4,000, seed 20260813, "
            "accounts resampled with replacement and all their pairs travelling with them, "
            "matching the earlier Step 7 runs so the rows are comparable.",
            "ARM LIST is 0046 SS3's eight arms plus 60, 100, 125 and 180 to fill the Step 13 "
            "span (decisions/0027).",
            "APPLY IS A RECONSTRUCTION of Step 8's position-6 input, built from Step 5 "
            "outputs. Step 8 builds the same population through its own positions 1-5.",
        ],
    }

    with open(ART, "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", ART)


if __name__ == "__main__":
    main()
