"""Emit the verification deliverable JSON from the computed outputs, without retyping a figure."""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
DF = os.path.join(ROOT, "processed/step7/df_a")

fc = json.load(open(os.path.join(DF, "floor_check.json")))
ir = json.load(open(os.path.join(DF, "instant_recheck.json")))

pops = {}
for nm, r in fc["populations"].items():
    n = r["n_pairs_denominator"]
    f = r["started_and_left_floor"]
    c = r["started_and_left_ceiling"]
    cc = r["continued_ceiling"]
    ns = r["never_started_bound_for_the_three_ceilings_check"]
    pops[nm] = {
        "population": nm,
        "population_definition": r["population_definition"],
        "n_pairs": n,
        "exclusions": r["exclusions_on_this_population"],
        "channel_pairs": r["channel"]["count_half_open_tau1_tau2_SPEC_ITEM_1"],
        "channel_definition": r["channel"]["definition"],
        "channel_open_vs_half_open_agree": r["channel"]["definitions_agree"],
        "channel_pairs_exactly_at_tau2": r["channel"]["pairs_with_last_insertion_exactly_at_tau2"],
        "started_and_left_floor_extreme_NONE": {
            "count": f["extreme_NONE_continued"]["count"],
            "pct": round(f["extreme_NONE_continued"]["pct"], 6)},
        "started_and_left_floor_extreme_ALL_ADOPTED": {
            "count": f["extreme_ALL_continued"]["count"],
            "pct": round(f["extreme_ALL_continued"]["pct"], 6)},
        "floor_movement_between_extremes_pp": round(f["movement_pp"], 6),
        "started_and_left_ceiling": {
            "count": c["extreme_ALL_continued"]["count"],
            "pct": round(c["extreme_ALL_continued"]["pct"], 6),
            "moves_between_extremes": c["moves_between_extremes"],
            "movement_pp": round(c["movement_pp"], 6)},
        "started_and_left_bound_ADOPTED": {
            "floor_pct": round(f["extreme_ALL_continued"]["pct"], 6),
            "ceiling_pct": round(c["extreme_ALL_continued"]["pct"], 6),
            "width_pp": round(c["extreme_ALL_continued"]["pct"]
                              - f["extreme_ALL_continued"]["pct"], 6),
            "width_pp_exact_integer_form": round(
                100.0 * (c["extreme_ALL_continued"]["count"]
                         - f["extreme_ALL_continued"]["count"]) / n, 6)},
        "continued_ceiling_extreme_NONE": {
            "count": cc["extreme_NONE_continued"]["count"],
            "pct": round(cc["extreme_NONE_continued"]["pct"], 6)},
        "continued_ceiling_extreme_ALL_ADOPTED": {
            "count": cc["extreme_ALL_continued"]["count"],
            "pct": round(cc["extreme_ALL_continued"]["pct"], 6)},
        "never_started_bound": {
            "floor_count": ns["floor_count"], "floor_pct": round(ns["floor_pct"], 6),
            "ceiling_count": ns["ceiling_count"], "ceiling_pct": round(ns["ceiling_pct"], 6),
            "degenerate": ns["degenerate"]},
        "three_ceilings": {
            "never_started_pct": round(ns["ceiling_pct"], 6),
            "started_and_left_pct": round(c["extreme_ALL_continued"]["pct"], 6),
            "continued_pct": round(cc["extreme_ALL_continued"]["pct"], 6),
            "sum_pct": round(r["arithmetic_identities_checked"]
                             ["three_ceilings_sum_pct_extreme_ALL"], 6),
            "excess_pairs": r["arithmetic_identities_checked"]["three_ceilings_excess_pairs"],
            "excess_decomposition_2xNS_plus_SL_plus_channel":
                r["arithmetic_identities_checked"]
                ["excess_decomposition_2xNS_plus_1xSL_plus_1xchannel"],
            "decomposition_matches":
                r["arithmetic_identities_checked"]["excess_decomposition_matches"]},
        "unfiltered_counts": r["unfiltered_counts_on_this_population"],
        "retained_counts": r["retained_counts_on_this_population"],
    }

out = {
    "step": 7,
    "task": "verification of the proposed DERIV started-and-left floor and Continued ceiling",
    "spec": "specs/step7-deriv-floor-verification.md",
    "instance_namespace_letter": "a",
    "date": "2026-08-14",
    "api_calls": 0,
    "is_a_gate": False, "is_a_rerun": False, "is_a_rule_change": False,
    "rule": "ALT-BROAD (0048, restored by 0054): NOT LIVE iff (no insertion instant after tau1) "
            "AND (NOT Continued). Silence anchored at tau1 and only at tau1.",
    "W": 108, "H": 91,
    "source": {
        "figures_computed_from": "processed/step7/bb_a/masks_W108.npz -- instance a's own "
                                 "W = 108 ALT-BROAD run",
        "scripts": ["src/step7_df_a_floor_check.py", "src/step7_df_a_instant_recheck.py"],
        "other_instance_output_read": False,
        "step7_floor_extremes_py_read_or_run_by_me": False,
        "nothing_asserted_against_a_proposed_value": True,
    },
    "integrity_checks_on_the_masks": fc["integrity_checks_on_the_stored_masks"],
    "independent_recomputation_of_last_insertion_instant": {
        "recomputed_from": ["processed/step5/full_scan.npz",
                            "processed/step5/calibration.npz (READ, never refitted, 0029)"],
        "n_records": ir["n_records"], "n_accounts": ir["n_accounts"],
        "max_abs_diff_seconds_vs_stored": ir["max_abs_diff_seconds_vs_stored_last_inst"],
        "channel_and_exclusion_counts_unchanged": all(
            v["agree"] for v in ir["populations"].values()),
    },
    "populations": pops,
    "verdicts_on_the_proposed_DERIV_correction": fc["verdicts_on_the_proposed_DERIV_correction"],
    "all_proposed_rows_confirmed": fc["all_rows_confirmed"],
}
with open(os.path.join(ROOT, "artifacts/step7-deriv-floor-check-a.json"), "w") as fh:
    json.dump(out, fh, indent=2)
print(json.dumps({k: out[k] for k in
                  ("all_proposed_rows_confirmed",
                   "independent_recomputation_of_last_insertion_instant")}, indent=2))
for nm, p in pops.items():
    print(nm, p["n_pairs"], p["channel_pairs"],
          p["started_and_left_bound_ADOPTED"], p["three_ceilings"]["sum_pct"])
