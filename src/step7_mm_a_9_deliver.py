"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 9 — the deliverable.

Consolidates the stage outputs into artifacts/step7-liveness-mm-a.json. Counts and aggregates
only: no usernames, no user ids, no individual watch histories. Row-level masks stay in
processed/step7/mm_a/.

GATE. Nothing here is adopted. Zero API calls.
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
P = os.path.join(ROOT, "processed/step7/mm_a")
ART = os.path.join(ROOT, "artifacts/step7-liveness-mm-a.json")

MANDATED = [38, 46, 77, 91, 107, 108, 150, 213]


def L(name):
    return json.load(open(os.path.join(P, name)))


def main():
    pop, arms, bounds = L("population.json"), L("arms.json"), L("bounds.json")
    checks, chan, marg, boot = L("checks.json"), L("channel.json"), L("margins.json"), L("bootstrap.json")

    grid = {}
    for reading in ("D10_per_arm", "D10_frozen_at_W108"):
        g = {}
        for nm in ("DERIV", "APPLY"):
            ws = sorted(arms["arms"], key=int)
            g[nm] = {
                "W": [int(w) for w in ws],
                "in_mandated_grid": [arms["arms"][w]["in_mandated_grid_0027"] for w in ws],
                "population_pairs": [arms["arms"][w][reading][nm]["population_pairs"] for w in ws],
                "excluded_total": [arms["arms"][w][reading][nm]["excluded_pairs"] for w in ws],
                "excluded_never_started": [
                    arms["arms"][w][reading][nm]["excluded_never_started"] for w in ws],
                "excluded_started_and_left": [
                    arms["arms"][w][reading][nm]["excluded_started_and_left"] for w in ws],
                "excluded_accounts": [
                    arms["arms"][w][reading][nm]["excluded_accounts"] for w in ws],
                "SUPERSEDED_ALT_BROAD_total": [
                    arms["arms"][w][reading][nm]["SUPERSEDED_ALT_BROAD_total"] for w in ws],
            }
            sel = [i for i, w in enumerate(g[nm]["W"]) if w in MANDATED]
            g[nm]["mandated_grid_only"] = {
                "W": [g[nm]["W"][i] for i in sel],
                "excluded_total": [g[nm]["excluded_total"][i] for i in sel],
                "excluded_never_started": [g[nm]["excluded_never_started"][i] for i in sel],
                "excluded_started_and_left": [g[nm]["excluded_started_and_left"][i] for i in sel],
            }
            t = g[nm]["mandated_grid_only"]["excluded_total"]
            s = g[nm]["mandated_grid_only"]["excluded_started_and_left"]
            g[nm]["W_coupling_top_over_bottom"] = {
                "total": round(t[-1] / t[0], 3),
                "started_and_left_component": round(s[-1] / s[0], 3),
            }
        grid[reading] = g

    out = {
        "step": 7,
        "what": "Step 7 liveness rule, RERUN on the ADOPTED rule ALT-MATCHED (decisions/0052)",
        "instance": "mm_a",
        "namespace": "a",
        "mode": "GATE, dual implementation. This artifact proposes and measures. "
                "It adopts nothing and approves nothing.",
        "api_calls": 0,
        "calibration": "processed/step5/calibration.npz READ, NEVER REFITTED (decisions/0029)",
        "rule": {
            "statement": ("A user-show pair is NOT LIVE if and only if EITHER "
                          "(|A| = 0 AND the account shows no insertion instant after "
                          "tau1 = [[T0]] + W*24h) OR "
                          "(|A| >= 1 AND the pair is NOT Continued AND the account shows no "
                          "insertion instant after tau2 = [[T0]] + (W+H)*24h). Otherwise it is "
                          "live."),
            "each_null_at_its_own_instant": "never-started read at tau1, started-and-left read "
                                            "at tau2",
            "continued": "Step 1 SS7 as amended by 0034: |A| >= 1 and F2 in A_H and "
                         "|A_H| >= ceil(0.90*L2), A_H read at tau2. Continued is the only state "
                         "resting on positive evidence and is never excluded.",
            "W_days": 108, "H_days": 91,
            "tie_convention": "'after tau' read strictly; silence is max(instant) <= tau. "
                              "Judgement call, spec-silent. 0 ties at either instant on either "
                              "population.",
        },
        "populations": pop["populations"],
        "waterfall_step5_asserted": pop["waterfall_computed"],
        "exclusions_at_W108": {
            nm: bounds["by_population"][nm]["exclusions"] for nm in ("DERIV", "APPLY")},
        "exclusion_detail_at_W108": {
            nm: arms["adopted_arm"][nm]["exclusions"] for nm in ("DERIV", "APPLY")},
        "outcome_shares_at_W108": {
            nm: {"population_pairs": arms["adopted_arm"][nm]["population_pairs"],
                 "no_liveness_filter": arms["adopted_arm"][nm]["settings"]["no_liveness_filter"],
                 "under_the_adopted_rule": arms["adopted_arm"][nm]["settings"]["ADOPTED_RULE"],
                 "movement_pp": arms["adopted_arm"][nm]["delta_vs_no_filter_pp"]}
            for nm in ("DERIV", "APPLY")},
        "rule_comparison_at_W108": {
            nm: arms["adopted_arm"][nm]["rule_comparison_at_W108"] for nm in ("DERIV", "APPLY")},
        "branch_decomposition": arms["branch_decomposition"],
        "bounds": {nm: {k: v for k, v in bounds["by_population"][nm].items()
                        if k.startswith(("bound_", "THREE_", "joint_", "PUBLISHED_",
                                         "unfiltered_", "population", "position", "exclusions"))}
                   for nm in ("DERIV", "APPLY")},
        "CONFIRM_OR_REFUTE": {**bounds["CONFIRM_OR_REFUTE"], **chan["CONFIRM_OR_REFUTE"]},
        "waterfall_position_6": checks["waterfall"],
        "monotone_decrease": {nm: {k: v for k, v in
                                   checks["monotone_decrease_at_position_6"][nm].items()
                                   if k != "per_arm"} for nm in ("DERIV", "APPLY")},
        "monotone_note": checks["monotone_note"],
        "commutation_check": checks["commutation_check"],
        "post_tau2_observation_window": checks["post_tau2_observation_window"],
        "post_tau2_note": checks["post_tau2_note"],
        "calibration_clamp": checks["calibration_clamp"],
        "calibration_clamp_note": checks["calibration_clamp_note"],
        "channel": {nm: chan["by_population"][nm] for nm in ("DERIV", "APPLY")},
        "margins_and_residual_robustness": marg["by_population"],
        "bootstrap": boot,
        "arms": grid,
    }
    with open(ART, "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote", ART, os.path.getsize(ART), "bytes")


if __name__ == "__main__":
    main()
