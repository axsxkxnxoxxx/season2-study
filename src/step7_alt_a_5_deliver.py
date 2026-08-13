"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  Emit the artifact JSON.

Counts and aggregates only. No usernames, no user IDs, no individual watch histories.
EVALUATION ONLY - adopts nothing.

Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
P = os.path.join(ROOT, "processed/step7/alt_a")
ART = os.path.join(ROOT, "artifacts")


def main():
    core = json.load(open(os.path.join(P, "core_W108.json")))
    arms = json.load(open(os.path.join(P, "arms.json")))
    marg = json.load(open(os.path.join(P, "margins.json")))
    d10 = json.load(open(os.path.join(P, "d10_attribution.json")))
    boot = json.load(open(os.path.join(P, "bootstrap.json")))

    arm_tbl = {w: {"post_D10_population": v["post_D10_population"],
                   "PF_LIMIT_excluded": v["PF_LIMIT"]["excluded"]["pairs"],
                   "PF_LIMIT_excluded_never_started": v["PF_LIMIT"]["excluded"]["never_started"],
                   "PF_LIMIT_excluded_continued": v["PF_LIMIT"]["excluded"]["continued"],
                   "PF_LIMIT_excluded_started_and_left":
                       v["PF_LIMIT"]["excluded"]["started_and_left"],
                   "ALT_excluded": v["ALT"]["excluded"]["pairs"],
                   "PF_LIMIT_never_started_pct": v["PF_LIMIT"]["shares"]["never_started_pct"],
                   "ALT_never_started_pct": v["ALT"]["shares"]["never_started_pct"],
                   "PF_LIMIT_bound_ceiling_pct": v["PF_LIMIT"]["bound_ceiling_never_pct"],
                   "ALT_bound_ceiling_pct": v["ALT"]["bound_ceiling_never_pct"]}
               for w, v in arms["arms"].items()}

    out = {
        "step": 7,
        "instance": "a",
        "what": "EVALUATION of Red Team's proposed alternative liveness rule against the "
                "approved PF-LIMIT (decisions/0042). ADOPTS NOTHING. Produced for the Human "
                "Lead's ruling; the other arm ran the same brief in isolation.",
        "api_calls": 0,
        "status": "The Step 7 gate is OPEN (decisions/0043, 0044). Step 8 has not launched.",
        "population": {
            "line": "Step 5 waterfall line 4 (152,126) less D10 right-censoring",
            "post_D10_at_W108": 147370,
            "accounts": 2402,
            "shows": 1138,
            "note": "the derivation population. Step 8 applies liveness to the analysis "
                    "population less D10 (196,654), a strict superset whose extra lines carry "
                    "contaminated T0. Absolute shares will move at Step 8 (decisions/0042 SS5).",
        },
        "rules_compared": {
            "PF_LIMIT_approved": "not live iff the account shows no insertion instant after "
                                 "that pair's tau1",
            "ALT_proposed": "not live iff (no insertion instant after tau1) AND (|A| = 0)",
            "threshold_1293d_deleted": "context row only; the rule decisions/0042 deleted",
        },

        "headline_finding": {
            "ALT_exclusions_at_W108": 0,
            "ALT_exclusions_at_every_W_from_1_to_400": 0,
            "PF_LIMIT_exclusions_at_W108": 751,
            "PF_LIMIT_excluded_never_started_pairs_at_W108": 0,
            "statement": "The ALT conjunction is EMPTY on the operative population. Every one "
                         "of PF-LIMIT's 751 exclusions has |A| >= 1. Red Team's estimate of "
                         "'on the order of 40 pairs' is read off the DELETED 1,293-day "
                         "threshold rule's composition, where the 40 never-started exclusions "
                         "come entirely from the measured-gap branch that decisions/0042 "
                         "removed. Under the approved rule the never-started exclusion count "
                         "is ZERO.",
        },

        "Q1_is_the_ordering_obstacle_real": {
            "answer": "No dependency exists. The obstacle is a convention, and the convention "
                      "can be restated without changing any row set.",
            "grounds": [
                "|A| is a function of E2, the pair's canonical S2 timestamps, T0 and W. None "
                "of those is a function of the liveness mask.",
                "Liveness is a function of the account's insertion instants and tau1. Neither "
                "is a function of |A|.",
                "Both are ROW-LOCAL predicates on the output of position 5, and two row-local "
                "predicates commute exactly, so the retained row set is identical whether ALT "
                "is evaluated at position 6 or after position 7.",
                "Position 7 is not a filter. Outcome assignment LABELS rows, it does not drop "
                "them (the L2 = 1 drop is position 2). An ordering constraint between a filter "
                "and a labelling step constrains only which is computed first, and computation "
                "order is free when neither reads the other's output.",
                "decisions/0029's recorded rationale for 5-before-6 is that censoring is "
                "objective and independent of behaviour while liveness is a behavioural "
                "inference. That argument is about censoring before liveness. It says nothing "
                "about liveness before outcome assignment and does not transfer.",
            ],
            "what_genuinely_does_not_commute": "the reported per-filter sample size, which is "
                                               "why decisions/0029 fixed an order at all. "
                                               "Under ALT, waterfall line 6 must be defined as "
                                               "an outcome-conditional count, and the spec "
                                               "must say so or two faithful instances will "
                                               "report it differently.",
            "empirically_verified": "ALT retains 147,370 rows whichever position it is "
                                    "evaluated at, because its exclusion set is empty.",
        },

        "Q2_what_it_would_cost": {
            "exclusion_count": {"PF_LIMIT": 751, "ALT": 0},
            "accounts_touched": {"PF_LIMIT": 166, "ALT": 0},
            "exclusion_composition_by_outcome_at_W108": {
                "PF_LIMIT": core["settings"]["PF_LIMIT_approved"]["excluded_composition"],
                "ALT": core["settings"]["ALT_proposed"]["excluded_composition"],
                "threshold_1293d_deleted":
                    core["settings"]["threshold_1293d_deleted"]["excluded_composition"],
            },
            "three_shares_pct": {
                k: core["settings"][k]["shares_pct"] for k in
                ("no_liveness_filter", "PF_LIMIT_approved", "ALT_proposed",
                 "threshold_1293d_deleted")},
            "PF_LIMIT_to_ALT_delta_pp": boot["paired_clustered_deltas"]["PF_LIMIT_to_ALT"],
            "delta_as_share_of_the_clustered_sampling_width": {
                "never_started": round(0.0318 / 0.7681, 4),
                "continued": round(0.0228 / 1.2482, 4),
                "started_and_left": round(0.0090 / 0.9831, 4),
            },
            "PF_LIMIT_never_started_movement_is_denominator_only": {
                "never_started_numerator_no_filter": 9145,
                "never_started_numerator_PF_LIMIT": 9145,
                "denominator_no_filter": 147370,
                "denominator_PF_LIMIT": 146619,
                "statement": "PF-LIMIT excludes zero never-started pairs, so its entire "
                             "+0.0318 pp effect on the never-started share is the denominator "
                             "shrinking by 751. decisions/0043's UP sign is confirmed and its "
                             "mechanism is now exact rather than approximate.",
            },
            "invariants_and_waterfall_touched": {
                "step8_waterfall_line_6": {"PF_LIMIT": "147,370 -> 146,619 (-751)",
                                           "ALT": "147,370 -> 147,370 (0)"},
                "filter_counts_decrease_monotonically":
                    "holds NON-STRICTLY under ALT. An instance coding a strict `<` would fail "
                    "the assertion on a legitimate no-op. This is a concrete "
                    "dual-implementation hazard and the spec must state non-strict.",
                "outcome_states_mutually_exclusive_and_sum_to_sample": "unaffected by either "
                                                                       "rule",
                "A_subset_of_A_H": "unaffected by either rule",
                "downstream_counts_D3prime_D8_D9_per_air_period":
                    "all are computed on the retained population, so under ALT they equal the "
                    "no-liveness-filter values exactly and under PF-LIMIT they are shifted by "
                    "the 751 removed pairs. Not recomputed here - they are Step 8 outputs and "
                    "Step 8 has not launched.",
            },
        },

        "Q3_the_step9_bound": {
            "definition": "task-sheet Step 9: what the never-started share becomes if every "
                          "inactivity-excluded PAIR is treated as a decliner",
            "by_rule": core["step9_liveness_bound"],
            "with_clustered_intervals": {
                k: boot["shares_with_clustered_intervals"][k]["step9_bound_ceiling_never_started"]
                for k in ("PF_LIMIT_approved", "ALT_proposed", "threshold_1293d_deleted")},
            "inflation_against_sampling_width":
                boot["step9_bound_inflation_against_sampling_width"],
            "answer": "Under PF-LIMIT the bound runs 6.2373% -> 6.7151%, an inflation of "
                      "0.4778 pp which is 0.62x the clustered sampling width of the share it "
                      "bounds. Its 751 pairs comprise 652 confirmed continuers and 99 "
                      "started-and-left and ZERO never-started - 751 of 751 carry positive S2 "
                      "evidence at tau1. It therefore bounds no uncertainty that exists: no "
                      "pair's never-started classification is at risk from account silence, "
                      "because no never-started pair is excluded. Under ALT the bound is "
                      "6.2055% -> 6.2055%, width 0.0000 pp. It bounds the right quantity and "
                      "the quantity is nil.",
            "correction_to_decisions_0043": {
                "0043_SS1_2_says": "'Roughly six in seven of the 751 have positive S2 "
                                   "evidence' and offers the remedy 'or compute it on the ~40 "
                                   "never-started exclusions instead'",
                "measured": "751 of 751 - SEVEN in seven - carry positive S2 evidence at "
                            "tau1; 652 of 751 (six in seven, 86.8%) are confirmed continuers. "
                            "The ~40 never-started exclusions belong to the DELETED 1,293-day "
                            "rule's measured-gap branch. Under the approved rule that count "
                            "is 0, so 0043's proposed remedy cannot be executed as written.",
                "error_class": "a figure measured on one configuration quoted as if measured "
                               "on another - the same class 0043 SS2 itself records as the "
                               "sixth instance. This is the seventh.",
            },
        },

        "Q4_what_breaks": {
            "against_ALT": [
                "It does not supply the missing warrant. Red Team's open item 2 is that the "
                "not-live branch has no warrant from decisions/0021, which licenses only the "
                "sufficient condition 'insertion after tau1 -> live'. ALT makes the branch "
                "EMPTY, which moots the question rather than answering it. If the stopped pull "
                "resumes and the frame grows (decisions/0021, closing note), the branch can "
                "become non-empty and the warrant gap returns unresolved.",
                "Its direction is true by construction, not by measurement. ALT's exclusion "
                "set is a subset of Never-started, so it can only move the never-started share "
                "DOWN. That matches the ledger's original sign, but the conservative-direction "
                "argument decisions/0040 SS3 withdrew is restored as a tautology - the "
                "direction is built into the rule rather than found in the data. Step 14 must "
                "say so or it re-publishes a withdrawn argument in a new form.",
                "A filter that excludes nothing cannot be shown to be working. PF-LIMIT's 751 "
                "exclusions are at least auditable. ALT's zero is consistent both with "
                "'no account silence corrupts any null' and with 'the rule is mis-specified "
                "and never fires'. Only the margin diagnostic distinguishes them, and that "
                "diagnostic is not currently required by any step.",
                "It zeroes the column decisions/0044 SS1.2 added. That entry requires Step 13 "
                "to report the exclusion count per W arm so the W-coupling is visible in the "
                "output rather than only in the decision log. Under ALT the column is zeros at "
                "every arm. The coupling genuinely vanishes, but a reader comparing against "
                "0044's 348-949 table must be told why, or the zeros read as a bug.",
                "It complicates a filter order that has already had to be fixed once. Even "
                "though the row sets commute, position 6 would read a quantity produced at "
                "position 7, and the documented order stops being a simple chain. "
                "decisions/0029 fixed the order precisely because the per-filter sample size "
                "does not commute, and three gate reruns have been spent on defects of this "
                "class.",
                "Dual-implementation exposure. ALT needs the spec to state (i) that waterfall "
                "line 6 is outcome-conditional, (ii) that the monotone-decrease invariant is "
                "non-strict, and (iii) which reading of '|A| = 0' is meant. Absent any of the "
                "three, two faithful instances can diverge on the waterfall while agreeing on "
                "every share - the exact failure mode decisions/0029 SS3 exists to prevent.",
            ],
            "against_PF_LIMIT": [
                "Its analysis population has 652 confirmed continuers deleted for a reason "
                "unrelated to continuing. The published Continued share is then computed on a "
                "denominator from which known continuers were removed by a behavioural "
                "inference that could not have been wrong about them.",
                "Its Step 9 bound inflates the never-started share by 0.4778 pp - 0.62x the "
                "sampling width - entirely out of pairs with positive S2 evidence.",
                "Its never-started effect is denominator-only, which means the filter is not "
                "protecting the null it exists to protect on a single pair in this population.",
            ],
            "what_ALT_damages_that_PF_LIMIT_does_not": "Nothing measurable. On this population "
                                                       "ALT is a strict no-op, so every count, "
                                                       "share, invariant and downstream "
                                                       "diagnostic equals the "
                                                       "no-liveness-filter value. The costs "
                                                       "listed above are costs to the "
                                                       "specification and to what the study "
                                                       "can claim, not to any number.",
        },

        "evidence": {
            "core_W108": core,
            "W_arms": arm_tbl,
            "W_arms_full": arms["arms"],
            "margins_and_mechanism": marg,
            "D10_attribution": d10,
            "bootstrap": boot,
        },

        "judgement_calls": [
            "READING OF '|A| = 0'. Taken as Step 1 SS7's Never-started condition - the set A "
            "at tau1 - because Red Team's own framing invokes the outcome and the filter-order "
            "position of outcome assignment. The competing reading, 'the pair has no S2 "
            "evidence at all in the record', gives a different set: 4 pairs on line 4 have no "
            "distinct in-E2 S2 episode at any bound, against 9,145 with |A| = 0 at tau1. If "
            "the Human Lead means the second reading the numbers here do not apply.",
            "W ARMS. decisions/0027's span plus 150 and 213, with 38, 91 and 108 added so the "
            "table lines up with decisions/0044's, plus a fine sweep from 0 to 400 to test "
            "whether the emptiness is a knife-edge. H held constant at 91 in every arm.",
            "W = 0 IS REPORTED BUT TREATED AS OUT OF SCOPE. ALT excludes 6 pairs at W = 0 and "
            "0 at every W from 1 to 400. W = 0 is not a tested arm and is degenerate under "
            "finale anchoring - it scores 100,175 of 147,685 pairs never-started. Reported so "
            "the emptiness is presented as an empirical fact over a range, not as a theorem.",
            "FLOOR AND CEILING. The Step 9 bound's floor is read as the rule's own point "
            "estimate and the ceiling as every excluded pair returned to the denominator and "
            "counted never-started. The task sheet names the ceiling explicitly and leaves the "
            "floor implicit.",
            "BOOTSTRAP DESIGN COPIED, NOT RE-DESIGNED. B = 4,000, seed 20260813, resampling "
            "the 2,402 accounts - identical to the gate-closing run so the rows are "
            "comparable. This is deliberately not an independent design choice, and the "
            "intervals here therefore corroborate nothing about the interval method.",
            "OUTCOMES COMPUTED FOR ALL ROWS BEFORE EITHER FILTER. Necessary to report the "
            "exclusion sets' composition at all, since PF-LIMIT deletes pairs before outcome "
            "assignment. Legitimate because outcome assignment is row-local, and it is the "
            "same computation the ordering question is about.",
            "STATES RECOMPUTED, NOT READ FROM CACHE. The three states were rebuilt from nA, "
            "nAH, f2_in_AH and need and asserted equal to the cached pair_states, so this run "
            "does not inherit an error from the earlier one.",
            "THE STORED CALIBRATION WAS READ, NEVER REFITTED. Insertion instants come from "
            "processed/step7/a4/distinct_instants.npz unchanged.",
            "NO 91-DAY ARM. Step 9's second headline has a separate origin (D5) and is a Step "
            "9 deliverable; Step 8 has not launched. Not measured here.",
            "no_after COMPUTED IN CLOSED FORM (account's last insertion instant <= tau1) "
            "rather than by searchsorted, and asserted equal to the cached searchsorted result "
            "at W = 108 on all 152,126 line-4 rows.",
        ],

        "recommendation": {
            "stated_as": "a recommendation. Nothing is adopted here.",
            "primary": "The alternative rule's DIAGNOSIS is correct and its REMEDY is null. On "
                       "this population ALT excludes 0 pairs at every W from 1 to 400, so "
                       "adopting it is numerically identical to deleting the liveness filter. "
                       "I recommend adopting ALT rather than deleting the filter, on the "
                       "single ground that the frame is a stopped pull and a stated rule that "
                       "currently fires on nothing survives the frame growing, whereas a "
                       "deleted filter does not. If it is adopted, the artifact must say in "
                       "plain words that it excludes zero pairs on this data - a reader told "
                       "'a liveness filter was applied' would otherwise be misled.",
            "second_and_independent_of_which_rule_is_chosen":
                "The Step 9 liveness bound should not be published in its current form under "
                "either rule. Under PF-LIMIT it adds 751 pairs - 652 of them confirmed "
                "continuers, none of them never-started - to the never-started numerator, "
                "inflating the share by 0.4778 pp, 0.62x its own sampling width. "
                "decisions/0043 already called it 'meaningless, not merely uninformative'; the "
                "measurement here is that the set it bounds contains zero pairs of the kind it "
                "claims to bound. Its remedy - recompute on the ~40 never-started exclusions - "
                "cannot be executed, because that count is 0 under the approved rule.",
            "third": "Red Team's item 2 stays open under either rule. ALT empties the "
                     "unwarranted branch; it does not warrant it.",
        },
    }
    with open(os.path.join(ART, "step7-alt-rule-a.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", os.path.join(ART, "step7-alt-rule-a.json"))


if __name__ == "__main__":
    main()
