"""Step 7 (frozen-spec run), instance A3 — emit the artifacts/ deliverable JSON.

Aggregates and counts only. No usernames, user ids or watch histories.
Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a3")
ART = os.path.join(ROOT, "artifacts")

THR = 632


def main():
    inst = json.load(open(os.path.join(OUT, "instants_summary.json")))
    br = json.load(open(os.path.join(OUT, "bracketing_W108.json")))
    ar = json.load(open(os.path.join(OUT, "arms_and_diagnostics.json")))

    ap = br["applied"]
    d = {
        "step": 7,
        "instance": "a3",
        "status": "PROPOSED, NOT ADOPTED. Gate. Awaiting Human Lead approval.",
        "date": "2026-08-13",
        "api_calls": 0,
        "spec_read": [
            "task-sheet.md lines 226-275",
            "decisions/0038-step7-frozen-spec.md",
            "decisions/0037-step7-reference-distribution-and-gap-unit.md",
            "decisions/0036-step7-threshold-and-shape.md",
            "artifacts/step1-outcome-definition.md lines 685-710",
        ],

        "proposal": {
            "threshold_days": THR,
            "p99_raw_days": br["threshold"]["p99_raw_days"],
            "percentile": 99.0,
            "reference_distribution": "bracketing-gap distribution, one gap per pair",
            "reference_population_n": 152126,
            "rounding": "ceiling (decisions/0025)",
            "W_days": 108,
            "threshold_is_a_function_of_W": True,
            "percentile_convention_sensitivity":
                "none: all 8 numpy conventions and nearest-rank-ceil agree to the digit "
                "at every W arm tested",
        },

        "rule_statement": (
            "A USER-SHOW PAIR is LIVE if, on the pair's own clock, the account's insertion "
            "history brackets tau1 = [[T0]] + W*24h with a gap shorter than 632 days. "
            "Concretely: build the account's sweep-wide sequence of record insertion instants "
            "(every record, all shows and movies, estimated from the stored Step 5 isotonic "
            "play-id curve), sort ascending, collapse runs of exactly equal instants, and take "
            "the last distinct instant at or before tau1 and the first distinct instant after "
            "tau1. If both exist and their difference is strictly less than 632 days, the pair "
            "is LIVE. If both exist and the difference is 632 days or more, the pair is NOT "
            "LIVE. If there is no instant after tau1, the pair is NOT LIVE. If there is no "
            "instant at or before tau1, the pair is NOT LIVE. The test is applied to that one "
            "bracketing gap and to no other gap in the sweep. Evidence is account-wide; the "
            "test is pair-specific, so one account may be live for one show and not for "
            "another. No user is ever dropped wholesale."
        ),
        "rule_boundary_convention": "excluded iff gap >= threshold (decisions/0025 reason (a))",

        "counts_at_W108": {
            "population": 152126,
            "live": ap["live"],
            "not_live_measured_gap": ap["not_live_measured_gap"],
            "not_live_no_instant_after_tau1": ap["not_live_no_instant_after_tau1"],
            "not_live_no_instant_at_or_before_tau1": ap["not_live_no_instant_at_or_before_tau1"],
            "not_live_total": ap["not_live_total"],
            "n_pairs_with_a_measured_bracketing_gap": ap["n_measured_gap"],
            "realised_exclusion_rate_of_measured_gap_pairs":
                ap["realised_exclusion_rate_measured_gap_pairs"],
            "realised_exclusion_rate_of_population":
                ap["realised_exclusion_rate_of_population"],
            "live_share_of_population": ap["live_share_of_population"],
        },

        "bracketing_gap_distribution_days": br["bracketing_gap_distribution_days"],
        "pooled_gap_distribution_days_CONTEXT": {
            "n_gaps": inst["n_pooled_gaps"],
            "percentiles": inst["pooled_gap_days_percentiles"],
            "sub_second_share": inst["pooled_gap_sub_second_share"],
        },

        "MANDATORY_DISCLOSURE_1_quota_property": {
            "statement": (
                "The threshold is set by the exclusion rate, not by anything in the data. "
                "The percentile is taken on the very distribution the test is applied to, so "
                "choosing the 99th mechanically fixes the exclusion rate at 1% of "
                "measured-gap pairs and the threshold is whatever number delivers it. Any "
                "percentile would have produced a self-consistent answer. 632 days is not a "
                "point where account behaviour changes; it is the 1% quota's price tag."
            ),
            "evidence_realised_rate_equals_the_quota_at_every_W_arm": {
                k: v["realised_exclusion_rate_measured_gap_pairs"]
                for k, v in ar["arms_refitted"].items()
            },
            "evidence_threshold_moves_with_the_quota": {
                str(q): v["threshold_days"] for q, v in br["inertness_by_percentile"].items()
            },
            "what_survives": (
                "0036 SS1's conservative-direction argument survives and still points up: a "
                "false-dead removes a pair and the liveness exclusion already biases the "
                "never-started share down (Step 14 bias 2). It identifies a direction, not a "
                "level."
            ),
        },

        "MANDATORY_DISCLOSURE_2_inertness": {
            "statement": (
                "The threshold does almost none of the excluding. At the proposed 99th, the "
                "measured-gap test removes 1,276 pairs and 0036 SS2.3's two evidence-absence "
                "edge cases remove 22,496 - the threshold is 5.4% of the liveness filter and "
                "the edge-case rulings are 94.6%. A reader must not take the threshold to be "
                "doing work it is not doing."
            ),
            "measured_on_frozen_population_152126": br["inertness_by_percentile"],
            "DIVERGENCE_FROM_0038_SS5": {
                "0038_states": "3.45% / 96.55%, holding across every percentile 90th to 99.9th",
                "a3_measures_at_the_99th_on_the_frozen_population": 0.053677,
                "a3_reproduces_3.45_percent_on_the_201900_line": 0.034524,
                "reading": (
                    "0038 SS5's figure is the 201,900 line's, not the frozen 152,126 line's. "
                    "On the frozen population the split at the 99th is 5.4% / 94.6%. The "
                    "percentile-invariance claim does not hold on any line: the measured-gap "
                    "share runs 36.5% at the 90th to 0.4% at the 99.9th on the frozen "
                    "population. The qualitative claim - the edge cases dominate at the "
                    "adopted percentile - holds."
                ),
                "by_waterfall_line":
                    ar["inertness_by_waterfall_line_W108_CONTEXT_ONLY"],
            },
        },

        "step13_arms_refitted": ar["arms_refitted"],
        "step13_counterfactual_single_frozen_threshold": {
            "note": (
                "What a single 632-day threshold, frozen from W=108, would deliver at each "
                "arm. It misses its stated 1% at every arm but 108, which is why 0038 SS6 "
                "requires a refit per arm."
            ),
            "by_arm": ar["counterfactual_single_frozen_threshold_from_W108"],
        },

        "weighting_sensitivity_NOT_ADOPTED": br["weighting_sensitivity_NOT_ADOPTED"],
        "withdrawn_pooled_basis_for_continuity": br["withdrawn_pooled_basis"],

        "right_censoring_diagnostic": {
            "note": (
                "0038 SS7: Step 7 derives on an uncensored population, so the "
                "no-instant-after-tau1 bucket is inflated by pairs D10 would remove at Step 8. "
                "Measured against the GLOBAL sweep end and against the pull instant; a test "
                "against the account's own last instant is tautological under the bucket's "
                "definition and is not reported."
            ),
            "global_sweep_end_utc": "2026-08-10T20:48:00Z",
            "pull_instant_utc": "2026-08-11T00:00:00Z",
            "by_arm": {
                k: {
                    "n_no_instant_after_tau1": v["not_live_no_instant_after_tau1"],
                    "of_which_tau1_past_global_sweep_end":
                        v["no_after_tau1_past_global_sweep_end"],
                    "of_which_tau1_past_pull_instant": v["no_after_tau1_past_pull_instant"],
                    "censored_share": round(v["no_after_tau1_past_global_sweep_end"]
                                            / v["not_live_no_instant_after_tau1"], 4),
                } for k, v in ar["arms_refitted"].items()
            },
        },

        "provenance": {
            "records_scanned": inst["n_records"],
            "accounts_in_sweep": inst["n_accounts"],
            "accounts_touched_by_reference_pairs": 2471,
            "distinct_insertion_instants": inst["n_distinct_instants"],
            "exact_ties_collapsed": inst["collapsed_exact_ties"],
            "gaps_per_account_median": inst["gaps_per_account_median"],
            "calibration_curve": "processed/step5/calibration.npz, READ NOT REFITTED",
            "rid_clamped_below_first_knot": inst["rid_below_first_knot_clamped"],
            "rid_clamped_above_last_knot": inst["rid_above_last_knot_clamped"],
            "waterfall_reproduced": br["reference_population"]["waterfall_computed"],
            "t0_undefined_in_reference_population": 0,
        },

        "corroborations_of_the_record": {
            "pooled_p99_days": 3.4431932062376234,
            "pooled_p99_ceil_days": 4,
            "gaps_per_account_median": 7812.0,
            "bracketing_median_days": br["bracketing_gap_distribution_days"]["median"],
            "share_of_bracketing_gaps_exceeding_pooled_99th": 0.34121,
            "no_instant_at_or_before_tau1_bucket": 18250,
            "note": (
                "0037/0038 record pooled median 0.0000006 d; a3 measures 0.0000007 d "
                "(7.0019e-07). 0037 records 37.4% exceeding the pooled-99th on its "
                "populations; a3 measures 34.1% on the frozen 152,126. Both are reporting "
                "differences of basis, not arithmetic disagreements."
            ),
        },
    }

    path = os.path.join(ART, "step7-liveness-a3.json")
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
    print("wrote", path)


if __name__ == "__main__":
    main()
