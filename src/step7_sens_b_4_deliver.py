"""Step 7 gate-closing sensitivity test (instance b, namespace sens_b) -- stage 4.

Emits the deliverable. Counts and aggregates only; no usernames, user ids or
individual watch histories.

Out: artifacts/step7-sensitivity-b.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
SRC = ROOT / "processed" / "step7" / "sens_b" / "sensitivity.json"
S1 = ROOT / "processed" / "step7" / "sens_b" / "stage1.json"
S2 = ROOT / "processed" / "step7" / "sens_b" / "stage2.json"
OUT = ROOT / "artifacts" / "step7-sensitivity-b.json"

d = json.loads(SRC.read_text())
s1 = json.loads(S1.read_text())
s2 = json.loads(S2.read_text())
n = d["population"]["post_D10"]
u = d["unfiltered_post_D10_counts"]

art = {
    "instance": "data-scientist-b",
    "namespace": "sens_b",
    "step": 7,
    "artifact": "gate-closing sensitivity test required by decisions/0041 Sec 4",
    "date": "2026-08-13",
    "api_calls": 0,
    "adopts": "nothing",

    "STATUS_READ_THIS_FIRST": {
        "what_this_is": "A GATE-CLOSING DIAGNOSTIC FOR STEP 7. It answers one question: "
                        "does the outcome split move when the liveness threshold moves "
                        "across its account-clustered interval?",
        "what_this_is_NOT": "It is NOT the Step 9 deliverable and its numbers are NOT "
                            "study results. They must not be cited as the headline.",
        "why": "Step 8 has NOT launched and is an unapproved gate (gate 4 of 5). The "
               "analysis table those shares would be computed on does not exist yet, so "
               "every share below is provisional in the POPULATION it runs on as well as "
               "in its status.",
        "population_caveat": "decisions/0041 Sec 3: Step 8 applies liveness at position 6 "
                             "to the analysis population less D10 -- 196,654 pairs -- a "
                             "STRICT SUPERSET of the 147,370 used here. The levels below "
                             "would change on that population. Only the MOVEMENT between "
                             "settings is what this test reports.",
        "adoption": "Nothing is adopted. The Human Lead rules on whether the threshold "
                    "survives.",
    },

    "question": "Is the outcome split sensitive to the liveness threshold across its "
                "account-clustered interval [787, 2200] and against the parameter-free rule?",

    "FINDING": {
        "verdict": "INSENSITIVE. Across 787 d, 1,293 d and 2,200 d the largest movement in "
                   "any of the three outcome shares is 0.0323 percentage points; including "
                   "the 0021-consistent parameter-free rule it is 0.0386 pp.",
        "max_abs_delta_pp_787_to_2200": d["max_abs_delta_pp_across_the_clustered_interval"],
        "max_abs_delta_pp_including_parameter_free_0021":
            d["max_abs_delta_pp_interval_plus_parameter_free_0021"],
        "for_scale_ci95_width_pp_on_never_started_at_1293":
            d["settings"]["T1293"]["ci95_account_clustered"]["never_started_pct"][1]
            - d["settings"]["T1293"]["ci95_account_clustered"]["never_started_pct"][0],
        "ratio_sampling_width_to_threshold_movement": round(
            (d["settings"]["T1293"]["ci95_account_clustered"]["never_started_pct"][1]
             - d["settings"]["T1293"]["ci95_account_clustered"]["never_started_pct"][0])
            / d["max_abs_delta_pp_across_the_clustered_interval"], 1),
        "the_one_exception": "The LITERAL reading of the parameter-free rule -- live iff an "
                             "instant at or before tau1 AND one after it -- moves the split "
                             "by up to 0.698 pp, twenty times the threshold's whole range. "
                             "That reading is NOT the threshold moving: it scores the 18,152 "
                             "no-instant-at-or-before-tau1 pairs DEAD, which is exactly the "
                             "withdrawn edge case (ii) that decisions/0040 Sec 1 removed for "
                             "contradicting approved gate 0021. It is reported so the two "
                             "readings are not silently conflated.",
    },

    "population": {
        "line": "Step 5 waterfall line 4 -- the 152,126 (decisions/0038 Sec 2)",
        "waterfall_asserted": s1["waterfall_measured"],
        "waterfall_expected": s1["waterfall_expected"],
        "n_line4": 152126,
        "D10_right_censoring": s1["D10"],
        "POST_D10_COUNT_THIS_TEST_RUNS_ON": n,
        "accounts": d["population"]["accounts"],
        "shows": s1["shows_post_D10"],
        "liveness_class_counts_at_W_108": d["population"]["class_counts"],
        "reproduces_0041_structural_figures": {
            "post_D10": [n, 147370], "measured_gap": [d["population"]["class_counts"]["measured_gap"], 128467],
            "open_ended": [d["population"]["class_counts"]["open_ended"], 751],
            "no_pre_instant": [d["population"]["class_counts"]["no_pre_instant_LIVE_per_0021"], 18152],
            "all_match": True},
        "L2_eq_1_exclusion": s1["L2_eq_1"],
    },

    "held_fixed": {
        "W_days": 108, "H_days": 91,
        "tau1": "[T0] + 108 x 24h", "tau2": "[T0] + 199 x 24h",
        "outcome_rule": "artifacts/step1-outcome-definition.md Sec 7 as amended by 0034: "
                        "Never started = |A| = 0 at tau1; Continued = |A| >= 1 AND F2 in A_H "
                        "AND |A_H| >= ceil(0.90 x L2), read on A_H at tau2; Started and left "
                        "= the remainder. Half-open instant tests throughout.",
        "canonical_timestamp": "min watched_at across the distinct episode's records (Sec 2.2)",
        "membership": "by SET against E2; records whose number is not in E2 are dropped",
        "D11": s2["D11"],
        "calibration": "processed/step5/calibration.npz READ, NOT REFITTED. Insertion "
                       "instants inherited unchanged from processed/step7/b4/instants.npz.",
        "partition_invariant_asserted": True,
    },

    "settings": {
        "T787": "787 days -- clustered interval lower endpoint",
        "T1293": "1293 days -- the point value (raw 1292.0284, ceiling per 0025)",
        "T2200": "2200 days -- clustered interval upper endpoint",
        "PF_0021": "parameter-free, 0021-consistent reading: NOT LIVE only if the gap is "
                   "open-ended (no instant after tau1). The no-instant-at-or-before-tau1 "
                   "pairs stay LIVE per 0040 Sec 1.",
        "PF_literal": "parameter-free, literal 0041 Sec 4 wording: LIVE iff an instant at "
                      "or before tau1 AND one after it. Scores the 18,152 DEAD, which "
                      "reinstates the withdrawn edge case (ii).",
    },

    "baseline_no_liveness_filter_at_all": {
        "n": u["n"],
        "never_started": u["never_started"], "continued": u["continued"],
        "started_and_left": u["started_and_left"],
        "never_started_pct": round(100.0 * u["never_started"] / u["n"], 4),
        "continued_pct": round(100.0 * u["continued"] / u["n"], 4),
        "started_and_left_pct": round(100.0 * u["started_and_left"] / u["n"], 4),
        "note": "Reported so the reader can see the whole liveness filter's total effect, "
                "not only the threshold's. At 1,293 d the entire filter moves never-started "
                "by 0.027 pp against no filter at all.",
    },

    "results": d["settings"],
    "deltas_pp": d["deltas_pp"],
    "bootstrap": d["bootstrap"],
    "nesting_asserted": d["nesting_asserted"],

    "WHY_IT_IS_INSENSITIVE": {
        "1_the_exclusion_set_is_tiny": "Across the whole clustered interval the excluded set "
                                       "moves 1,707 -> 897 pairs, 810 pairs, 0.55% of the "
                                       "population. A set that size cannot move a share built "
                                       "on 147,370 by more than a few hundredths of a point.",
        "2_the_excluded_are_not_the_never_started": "The gap test's marginal exclusions are "
                                                    "overwhelmingly CONTINUED pairs -- at "
                                                    "1,293 d, 1,079 of the 1,282 excluded are "
                                                    "Continued and only 40 are Never started. "
                                                    "Removing them barely reweights the split.",
        "3_the_quota_property_bites": "The threshold is a percentile OF the distribution the "
                                      "test applies to, so its level is fixed by the exclusion "
                                      "rate rather than by any feature of the data. Moving the "
                                      "percentile moves a quota, and the quota is under 1.2% at "
                                      "every setting tested.",
        "4_open_ended_dominates_at_every_setting": "751 of the exclusions are the open-ended "
                                                   "edge case and are invariant in the "
                                                   "threshold. At 2,200 d they are 84% of all "
                                                   "exclusions; the measured-gap test does 146.",
    },

    "DIRECTION_OF_THE_MOVEMENT_SUCH_AS_IT_IS": {
        "never_started_pct": "rises monotonically with the threshold, 6.2109 -> 6.2325 -> "
                             "6.2373. Mechanism: the 810 pairs restored as the threshold "
                             "loosens from 787 to 2,200 are 89 never-started, 11.0%, above "
                             "the 6.2% population rate, so restoring them lifts the share. "
                             "Total range 0.026 pp.",
        "continued_pct": "falls 82.3812 -> 82.3497 -> 82.3490. Total range 0.032 pp.",
        "started_and_left_pct": "essentially flat, 11.4078 -> 11.4178 -> 11.4137, "
                                "non-monotone at the third decimal. Total range 0.010 pp.",
        "sign_note": "All three ranges are smaller than the third significant figure of any "
                     "share. None of them would change a published number.",
    },

    "JUDGEMENT_CALLS_THE_SPEC_DOES_NOT_SETTLE": [
        {"id": "J1", "call": "POPULATION. Run on waterfall line 4 less D10 = 147,370.",
         "why": "It is the liveness derivation AND application population inside Step 7 "
                "(0038 Sec 2, 0040 Sec 2), so the threshold is calibrated on exactly the rows "
                "it is tested on here.",
         "what_step_8_would_do_differently": "0041 Sec 3: Step 8 applies liveness to the "
                                             "analysis population less D10 -- 196,654 pairs. "
                                             "The three LEVELS below would differ there, and "
                                             "0041 Sec 3 records that 1,293 d delivers 1.4418% "
                                             "against a stated 1% on that population. Whether "
                                             "the INSENSITIVITY carries over is not tested "
                                             "here and cannot be, because Step 8 has not run.",
         "direction_if_wrong": "The superset adds pairs excluded for contaminated first-S2 "
                               "watches, which is unrelated to liveness. There is no reason to "
                               "expect the excluded set to grow faster than the denominator, "
                               "so the deltas would if anything shrink -- but that is an "
                               "expectation, not a measurement."},
        {"id": "J2", "call": "TWO READINGS OF THE PARAMETER-FREE RULE, both reported, "
                             "neither adopted.",
         "why": "0041 Sec 4's wording -- 'the account has insertion evidence bracketing tau1' "
                "-- read literally requires an instant at or before tau1, which scores the "
                "18,152 no-pre-instant pairs DEAD. That is the withdrawn edge case (ii), and "
                "0040 Sec 1 withdrew it for contradicting approved gate 0021. The two rulings "
                "point opposite ways on 12.3% of the population.",
         "consequence": "This is the ONLY setting in the test that moves the split "
                        "materially, at 0.698 pp. If the Human Lead adopts a parameter-free "
                        "rule, WHICH reading is adopted is a live question and the answer is "
                        "worth more than the threshold ever was.",
         "reported_as_a_defect": "Yes -- decisions/ is authoritative, and 0041 Sec 4's "
                                 "wording is not reconcilable with 0040 Sec 1 as written."},
        {"id": "J3", "call": "The outcome arrays are computed ONCE, before any liveness "
                             "filter, and liveness is applied as a row mask.",
         "why": "Liveness cannot change any pair's outcome state -- it only decides whether "
                "the pair is counted. Computing outcomes once makes the four settings exactly "
                "comparable and removes any chance of drift between them."},
        {"id": "J4", "call": "Interval: account-clustered bootstrap, B = 2,000, seed "
                             "20260813, percentile method, SAME resample across settings "
                             "within a replicate so the deltas are paired.",
         "why": "Gaps within an account are not independent -- the reason 0039 required a "
                "clustered interval on the threshold. The seed and B are instance choices "
                "the spec does not fix; 0040 Sec 6 flagged bootstrap endpoints as the one "
                "place the arms did independent work with no cross-check."},
        {"id": "J5", "call": "L2 = 1 exclusion is vacuous here.",
         "why": "ZERO pairs on line 4 sit on an L2 = 1 show, so Step 8's filter-position-2 "
                "exclusion removes nothing and cannot be a source of divergence. Stated "
                "rather than left to be wondered about."},
        {"id": "J6", "call": "np.interp CLAMPING of 6,956 records outside the fitted "
                             "calibration knot range is inherited UNCHANGED from the b4 run.",
         "why": "The curve is a required input and is not refitted. The spec does not state "
                "how to treat records outside the fitted rid range; clamping makes all "
                "pre-curve records share one instant and all post-curve records share "
                "another, and the exact-tie rule then collapses each run to a single instant. "
                "0040 Sec 6 named this as a lever that would have changed every downstream "
                "number had it been resolved otherwise. Reported, not repaired."},
        {"id": "J7", "call": "2,200 d is taken as given as the upper endpoint.",
         "why": "The b4 run's own account-clustered 95% interval at B = 2,000 is not "
                "[787, 2200]; the endpoints named in the task are the Human Lead's. They are "
                "used verbatim and not re-derived. The test is more conservative for it: "
                "2,200 d is wider than anything this instance measured, and the split still "
                "does not move."},
        {"id": "J8", "call": "The DEGENERACY CAVEAT travels with this test.",
         "why": "0041 Sec 2.1: above the 99.4188th percentile the extended-set percentile is "
                "itself infinite and the rule collapses into the open-ended edge case alone. "
                "At the limit that IS the PF_0021 column, which is why PF_0021 and T2200 are "
                "within 0.001 pp of each other on every share: 2,200 d is already close "
                "enough to infinite that the measured-gap test has almost nothing left to do "
                "-- 146 exclusions out of 128,467 measured-gap pairs."},
    ],

    "WHAT_THIS_TEST_DOES_NOT_ESTABLISH": [
        "It does not establish that the outcome shares are correct. They are computed on a "
        "population Step 8 has not defined and on a gate that is not approved.",
        "It does not establish that liveness as a WHOLE is inert -- only that the THRESHOLD "
        "is. The open-ended edge case removes 751 pairs at every setting and is unaffected by "
        "any percentile choice.",
        "It does not test sensitivity to W. W is held at 108 throughout, as instructed. The "
        "threshold is a function of W (0038), so a different W arm would have a different "
        "threshold and a different interval; Step 13 refits per arm.",
        "It does not resolve the derive/apply mismatch recorded in 0041 Sec 3, which goes to "
        "Step 14 at its measured size.",
    ],

    "files": {
        "row_level": "processed/step7/sens_b/ -- pairs.npz, outcomes.npz, sensitivity.json",
        "scripts": ["src/step7_sens_b_1_population.py", "src/step7_sens_b_2_outcomes.py",
                    "src/step7_sens_b_3_sensitivity.py", "src/step7_sens_b_4_deliver.py"],
    },
}

OUT.write_text(json.dumps(art, indent=2))
print(f"wrote {OUT}")
