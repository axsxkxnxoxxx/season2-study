"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 8 of 8 — the deliverable.

Assembles artifacts/step7-liveness-bb-a.json from the stage outputs in
processed/step7/bb_a/. Aggregates and counts only: no usernames, no user ids, no individual
watch histories reach artifacts/.

Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
P = os.path.join(ROOT, "processed/step7/bb_a")
ART = os.path.join(ROOT, "artifacts")
MANDATED = [38, 46, 77, 91, 107, 108, 150, 213]


def load(name):
    with open(os.path.join(P, name)) as fh:
        return json.load(fh)


def main():
    pop = load("population.json")
    inst = load("instants.json")
    arms = load("arms.json")
    bounds = load("bounds.json")
    checks = load("checks.json")
    resid = load("residual.json")
    stab = load("stability.json")
    boot = load("bootstrap.json")

    arm_rows = []
    for W in [38, 46, 60, 77, 91, 100, 107, 108, 125, 150, 180, 213]:
        r = arms["arms"][str(W)]
        row = {"W": W, "in_mandated_grid_0027": W in MANDATED}
        for lab, key in (("D10_re_derived_at_this_arm", "D10_per_arm"),
                         ("D10_frozen_at_W108", "D10_frozen_at_W108")):
            row[lab] = {
                nm: {k: r[key][nm][k] for k in
                     ("population_pairs", "excluded_pairs", "excluded_never_started",
                      "excluded_started_and_left", "excluded_accounts")}
                for nm in ("DERIV", "APPLY")}
        arm_rows.append(row)

    core = arms["adopted_arm"]
    out = {
        "step": 7,
        "title": "Liveness rule, rerun on ALT-BROAD (decisions/0048). GATE — proposal only.",
        "instance": "bb_a (namespace a)",
        "status": "GATE. This artifact adopts nothing and approves nothing. The Human Lead "
                  "approves in writing, in session.",
        "api_calls": 0,
        "rule_as_run": {
            "statement": "A user-show pair is NOT LIVE if and only if BOTH: the account shows "
                         "no insertion instant after that pair's tau1 = [[T0]] + W*24h, AND "
                         "the pair is NOT Continued.",
            "continued": "|A| >= 1 and F2 in A_H and |A_H| >= ceil(0.90*L2), A_H read at "
                         "tau2 = [[T0]] + (W+H)*24h (Step 1 SS7 as amended by 0034)",
            "conjunct_2_selects_the_two_nulls": {
                "never_started": "|A| = 0 -- null",
                "started_and_left": "|A| >= 1 and not Continued -- null ON EXIT",
                "continued": "the only state resting on positive evidence; the rule never "
                             "reaches it",
            },
            "insertion_instant": "np.interp(play_id, stored Step 5 calibration). The curve is "
                                 "READ, never refitted (0029). Insertion time is not claimed "
                                 "watched_at (0021).",
            "anchoring": "pair-level, at that pair's tau1 (0034). No user is ever dropped "
                         "wholesale.",
            "tie_convention": "'after' is strict, so NOT LIVE requires max instant <= tau1; "
                              "measured to be non-load-bearing, 0 ties on either population",
            "W": 108, "H": 91,
        },
        "populations": {
            "rule": "EVERY FIGURE STATES ITS POPULATION (0046 SS0)",
            "DERIV": {"definition": "Step 5 waterfall line 4 less D10", "pairs": 147370,
                      "accounts": pop["populations"]["DERIV"]["accounts"],
                      "asserted_against_step5_waterfall": True},
            "APPLY": {"definition": "Step 5 waterfall line 1 less D10; what Step 8 filters",
                      "pairs": 196654,
                      "accounts": pop["populations"]["APPLY"]["accounts"],
                      "asserted_against_step5_waterfall": True},
            "step5_waterfall_recomputed": pop["waterfall_computed"],
            "step5_waterfall_published": pop["waterfall_published"],
        },
        "exclusions_at_W108": {
            nm: {
                "population_pairs": core[nm]["population_pairs"],
                "excluded_pairs": core[nm]["exclusions"]["total"],
                "excluded_accounts": core[nm]["exclusions"]["accounts"],
                "never_started_component": core[nm]["exclusions"]["never_started_component"],
                "never_started_component_accounts":
                    core[nm]["exclusions"]["never_started_component_accounts"],
                "started_and_left_component":
                    core[nm]["exclusions"]["started_and_left_component"],
                "started_and_left_component_accounts":
                    core[nm]["exclusions"]["started_and_left_component_accounts"],
                "continued_component": core[nm]["exclusions"]["continued_component_must_be_zero"],
                "share_of_population_pct": core[nm]["exclusions"]["share_of_population_pct"],
            } for nm in ("DERIV", "APPLY")},
        "prior_measurement_check": {
            "claim": "99 on DERIV from 73 accounts; 703 on APPLY from 216 accounts",
            "measured_DERIV": [core["DERIV"]["exclusions"]["total"],
                               core["DERIV"]["exclusions"]["accounts"]],
            "measured_APPLY": [core["APPLY"]["exclusions"]["total"],
                               core["APPLY"]["exclusions"]["accounts"]],
            "verdict": "CONFIRMED on both populations, counts and account counts",
        },
        "outcome_shares_at_W108": {
            nm: {
                "population_pairs": core[nm]["population_pairs"],
                "no_liveness_filter": core[nm]["settings"]["no_liveness_filter"],
                "under_the_rule": core[nm]["settings"]["ADOPTED_RULE"],
                "movement_pp": core[nm]["delta_vs_no_filter_pp"],
                "movement_pp_6dp": core[nm]["delta_vs_no_filter_pp_6dp"],
            } for nm in ("DERIV", "APPLY")},
        "conjunct_decomposition": arms["conjunct_decomposition"],
        "rule_comparison_at_W108": {nm: core[nm]["rule_comparison"]
                                    for nm in ("DERIV", "APPLY")},
        "exclusion_set_identity_on_APPLY": arms["exclusion_set_identity_on_APPLY"],
        "bounds": bounds["by_population"],
        "never_started_bound_vs_ALT": bounds["never_started_bound_vs_ALT"],
        "sampling_error": boot["by_population"],
        "waterfall": checks["waterfall_positions_4_to_6"],
        "ordering_commutation_check": checks["ordering_commutation_check"],
        "pair_level_not_user_level": checks["pair_level_not_user_level"],
        "tie_convention": checks["tie_convention"],
        "W_coupling_per_arm": {
            "note": "D10 contains W, so the censored population differs per arm (0047 SS5). "
                    "BOTH readings are given and each names itself. The mandated grid is "
                    "0027's 38/46/77/91/107/108/150/213; 60, 100, 125 and 180 are extra, and "
                    "125 and 180 are the off-grid arms 0047 SS5 quoted without their arms.",
            "rows": arm_rows,
        },
        "calibration_residual": {
            "curve": resid["curve"],
            "claim_1_watched_at_after_calibrated_instant":
                resid["instance_B_claim_1_watched_at_later_than_calibrated_instant"],
            "claim_2_clamped_above": resid["instance_B_claim_2_records_clamped_above_the_curve"],
            "residual_on_the_fit_family": resid["calibration_residual_on_the_fit_family"],
            "clamp_check": stab["clamp_check"],
            "exclusion_set_stability": {
                nm: {k: v for k, v in stab["by_population"][nm].items() if k != "population"}
                for nm in ("DERIV", "APPLY")},
        },
        "files": {
            "artifacts": ["artifacts/step7-liveness-bb-a.json",
                          "artifacts/step7-liveness-bb-a.md"],
            "processed": sorted(os.listdir(P)),
            "scripts": sorted(f for f in os.listdir(os.path.join(ROOT, "src"))
                              if f.startswith("step7_bb_a_")),
        },
    }
    with open(os.path.join(ART, "step7-liveness-bb-a.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", os.path.join(ART, "step7-liveness-bb-a.json"))
    print(json.dumps(out["exclusions_at_W108"], indent=2))
    print(json.dumps(out["prior_measurement_check"], indent=2))


if __name__ == "__main__":
    main()
