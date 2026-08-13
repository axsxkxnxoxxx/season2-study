"""Step 7 (rerun), instance A2 — assemble the artifact JSON. Aggregates only. Zero API calls."""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a2")
ART = os.path.join(ROOT, "artifacts")

su = json.load(open(os.path.join(OUT, "bracketing_summary.json")))
sw = json.load(open(os.path.join(OUT, "sweeps.json")))
po = json.load(open(os.path.join(OUT, "pooled_summary.json")))

PRIMARY = "w_estimation_sample_128099"
prim = su["by_population"][PRIMARY]

art = {
    "step": 7,
    "instance": "a2",
    "run": "rerun of 2026-08-13, corrected reference distribution",
    "status": "PROPOSAL. GATE. Not adopted. Human Lead approves.",
    "api_calls": 0,
    "spec": [
        "task-sheet.md Step 7 (lines 226-262)",
        "decisions/0037 (reference distribution + exact gap unit)",
        "decisions/0036 SS2 (rule shape, stands unchanged); SS1's basis withdrawn by 0037",
        "decisions/0029 (continuous instant differences), 0025 (ceiling), 0021 (insertion time)",
        "decisions/0026 (W = 108 days), 0034 (liveness anchored at tau1, not tau2)",
    ],
    "inputs": {
        "calibration": "processed/step5/calibration.npz — READ, NOT REFITTED",
        "sweep": "processed/step5/full_scan.npz",
        "pairs": "processed/step5/pair_revision5.csv",
        "step5_waterfall_reproduced": su["step5_waterfall_reproduced"],
    },
    "gap_unit": {
        "operation": ("insertion instant of every record in the account's sweep; sort ascending; "
                      "collapse runs of EXACTLY equal instants (exact float equality, no rounding "
                      "or bucketing at any resolution); consecutive differences"),
        "insertion_instant": "np.interp(rid, knot_rid, knot_time)",
        "records": po["n_records"],
        "accounts": po["n_accounts"],
        "distinct_instants": po["n_distinct_instants"],
        "records_collapsed_as_exact_ties": po["collapsed_records"],
        "records_collapsed_share": round(po["collapsed_share"], 6),
        "rid_below_calibration_curve_start": po["rid_below_curve_start"],
        "rid_above_calibration_curve_end": po["rid_above_curve_end"],
        "gaps_per_account_median": po["gaps_per_account_median"],
    },
    "pooled_distribution_WITHDRAWN_AS_REFERENCE": {
        "n_gaps": po["n_pooled_gaps"],
        "median_days": po["pooled_gap_days_percentiles"]["50"],
        "p99_days": po["pooled_gap_days_percentiles"]["99"],
        "p99_ceil_days": su["pooled_reference_WITHDRAWN"]["p99_ceil_days"],
        "sub_second_share": round(po["pooled_gap_sub_second_share"], 6),
        "note": ("retained only as the contrast that decisions/0037 SS1 withdrew; it is NOT the "
                 "reference distribution"),
    },
    "reference_distribution": {
        "definition": ("the BRACKETING-gap distribution itself: for each pair, the gap between the "
                       "last distinct insertion instant at or before tau1 and the first after it"),
        "tau1": "[[T0]] + W x 24h, W = 108 days, [[T0]] = UTC midnight of the pair's T0 date",
        "by_population": {k: {
            "n_pairs": v["n_pairs"],
            "n_measured_gap": v["n_measured_gap"],
            "median_days": round(v["bracketing_gap_days"]["median"], 4),
            "p75_days": round(v["bracketing_gap_days"]["p75"], 4),
            "p95_days": round(v["bracketing_gap_days"]["p95"], 4),
            "p99_raw_days": round(v["p99_pair_weighted_raw_days"], 4),
            "p99_ceil_days": v["p99_pair_weighted_ceil_days"],
        } for k, v in su["by_population"].items()},
    },
    "proposed_threshold": {
        "value_days": prim["p99_pair_weighted_ceil_days"],
        "raw_percentile_days": round(prim["p99_pair_weighted_raw_days"], 4),
        "percentile": 99.0,
        "rounding": "ceiling, per decisions/0025",
        "measured_on": PRIMARY,
        "PROPOSAL_ONLY": True,
        "alternatives_if_the_Human_Lead_picks_a_different_population": {
            k: v["p99_pair_weighted_ceil_days"] for k, v in su["by_population"].items()},
    },
    "rule_statement": (
        "A USER-SHOW PAIR is LIVE if, on the account's whole sweep (all shows, all movies, all "
        "record kinds), there exists a distinct insertion instant at or before that pair's "
        "tau1 = [[T0]] + 108 x 24h AND a distinct insertion instant after tau1, AND the gap "
        "between those two instants is STRICTLY LESS THAN the threshold. Otherwise the pair is "
        "NOT LIVE. Insertion instants come from the stored Step 5 play-id calibration, never from "
        "claimed watched_at. Evidence is account-wide; the test is pair-specific; a user is never "
        "dropped wholesale."),
    "rule_application": {k: v["applied_corrected_threshold"] for k, v in su["by_population"].items()},
    "realised_failure_rate": {
        "under_withdrawn_pooled_basis": {
            k: v["applied_withdrawn_pooled_threshold"]["measured_gap_failure_rate"]
            for k, v in su["by_population"].items()},
        "under_corrected_basis": {
            k: v["applied_corrected_threshold"]["measured_gap_failure_rate"]
            for k, v in su["by_population"].items()},
        "note": ("0037 recorded 37.4% under the withdrawn basis; reproduced here at 0.373936 on "
                 "the 201,900 analysis population. The corrected basis takes it to ~0.99%, which "
                 "is 100 - percentile by construction, not an empirical finding."),
    },
    "applied_to_the_full_analysis_population_201900": {
        "note": ("Step 5's precedent for W is 'derived from clean records only, then applied to "
                 "everyone'. If the same is done here, the threshold derived on 128,099 is applied "
                 "to 201,900 and the delivered failure rate is NOT the stated 1%."),
        "by_threshold": json.load(open(os.path.join(OUT, "applied_to_201900.json"))),
    },
    "percentile_sweep": sw["percentile_sweep_corrected_basis"],
    "W_sensitivity_of_threshold": sw["W_sensitivity_of_threshold"],
    "edge_bucket_diagnostics": sw["edge_bucket_diagnostics"],
    "insertion_clock_span_days": sw["insertion_clock_span_days"],
    "weighting_sensitivity": {
        k: {"pair_weighted_ceil_days": v["p99_pair_weighted_ceil_days"],
            "distinct_account_gap_weighted_ceil_days":
                v["p99_distinct_account_gap_weighted_ceil_days"],
            "n_distinct_account_gap_keys": v["n_distinct_account_gap_keys"]}
        for k, v in su["by_population"].items()},
    "percentile_method_panel": {k: v["p99_percentile_panel"] for k, v in su["by_population"].items()},
}

path = os.path.join(ART, "step7-liveness-a2.json")
with open(path, "w") as f:
    json.dump(art, f, indent=2)
print("wrote", path)
