"""Step 7 (rerun), instance b2 -- stage 5: emit the public artifact JSON.
Aggregates and counts only. No usernames, user IDs or watch histories."""
import json
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b2"
ART = ROOT / "artifacts"

thr = json.loads((OUT / "threshold.json").read_text())
diag = json.loads((OUT / "diag.json").read_text())
inst = json.loads((OUT / "instants_meta.json").read_text())

doc = {
    "step": 7,
    "instance": "b2",
    "run": "rerun of 2026-08-13 on the corrected reference distribution (decisions/0037)",
    "status": "PROPOSAL. Gate not approved. Nothing adopted by this instance.",
    "api_calls": 0,
    "inputs": {
        "calibration_curve": "processed/step5/calibration.npz (READ, not refitted)",
        "pair_table": "processed/step5/pair_revision5.csv",
        "sweep": "processed/step5/full_scan.npz",
        "W_used_only_to_place_tau1": 108,
        "step5_waterfall_asserted": [201900, 178165, 155131, 152126, 128099],
    },
    "gap_unit": {
        "rule": "decisions/0037 s4 -- every record's insertion instant, sorted ascending, "
                "runs of EXACTLY equal instants collapsed, then consecutive differences",
        "records_total": inst["records_total"],
        "distinct_instants_total": inst["distinct_instants_total"],
        "collapsed_records": inst["collapsed_records"],
        "collapsed_pct": inst["collapsed_pct"],
        "accounts": inst["accounts"],
        "median_gaps_per_account": inst["gaps_per_account_median"],
        "records_below_calibration_curve_start": inst["records_below_curve_start_rid"],
        "records_above_calibration_curve_end": inst["records_above_curve_end_rid"],
    },
    "pooled_gap_distribution_context_only": {
        "n": inst["pooled_gaps_n"],
        "percentiles_days": inst["pooled_gap_days_percentiles"],
        "sub_second_share_pct": inst["pooled_sub_second_share_pct"],
    },
    "reference_distribution_bracketing": {
        "n": thr["reference_n"],
        "percentiles_days": thr["percentile_grid_on_bracketing"],
        "median_days": thr["sensitivity_reference_population"]
                          ["analysis_population_201900_PRIMARY"]["median_days"],
    },
    "threshold": {
        "percentile": thr["percentile"],
        "percentile_method": thr["percentile_method"],
        "raw_days": thr["raw_percentile_days"],
        "PROPOSED_days": thr["THRESHOLD_PROPOSED_days"],
        "rounding": "ceiling, decisions/0025",
        "test_direction": thr["test_direction"],
        "realised_failure_rate_pct_on_measured_gaps": thr["realised_failure_rate_pct_on_measured_gaps"],
        "bootstrap_95pct_interval_days": diag["bootstrap_99th_percentile_days"],
    },
    "corrected_vs_withdrawn_basis": thr["withdrawn_basis_check"],
    "pooled_grid_for_contrast": thr["pooled_grid_for_contrast"],
    "rule_application": thr["rule_application_at_proposed_threshold"],
    "rule_application_on_step5_estimation_sample": thr["rule_application_on_step5_estimation_sample"],
    "exclusion_composition": diag["exclusion_composition_at_threshold"],
    "pair_level_not_user_level": {
        "accounts_with_at_least_one_pair": diag["accounts_total"],
        "accounts_all_pairs_live": diag["accounts_all_pairs_live"],
        "accounts_no_pair_live": diag["accounts_no_pair_live"],
        "accounts_mixed": diag["accounts_MIXED_live_and_not"],
        "mixed_pct": diag["mixed_pct_of_accounts"],
    },
    "failing_pairs_gap_days": diag["gap_days_of_failing_pairs"],
    "sensitivity_reference_population": thr["sensitivity_reference_population"],
    "sensitivity_weighting": thr["sensitivity_weighting_one_gap_per_distinct_account_gap"],
    "W_dependence_defect": thr["W_dependence_of_the_reference_distribution"],
    "chart": "artifacts/step7-gap-distribution-b2.png",
    "row_level_detail": "processed/step7/b2/ (not public)",
}
(ART / "step7-liveness-b2.json").write_text(json.dumps(doc, indent=1))
print("written", (ART / "step7-liveness-b2.json"))
