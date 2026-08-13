"""Step 7 ALT-BROAD rerun (instance b, namespace bb_b) -- stage 4, deliverable.

Writes artifacts/step7-liveness-bb-b.json and artifacts/step7-liveness-bb-b.md.
COUNTS AND AGGREGATES ONLY -- no user ids, no usernames, no watch histories.

GATE. This is a proposal. Nothing is adopted here.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "bb_b"
ART = ROOT / "artifacts"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    t = time.time()
    rule = json.load(open(OUT / "rule.json"))
    wf = json.load(open(OUT / "waterfall.json"))
    boot = json.load(open(OUT / "bootstrap.json"))
    resid = json.load(open(OUT / "residual.json"))
    marg = json.load(open(OUT / "margins.json"))

    A, D = rule["by_population"]["APPLY"], rule["by_population"]["DERIV"]
    a8, d8 = A["108"], D["108"]

    out = {
        "step": 7, "instance": "data-scientist-b", "namespace": "bb_b",
        "gate": "GATE. This is a proposal. NOTHING IS ADOPTED HERE.",
        "date": "2026-08-14", "api_calls": 0,
        "rule": rule["rule"], "rule_source": rule["rule_source"],
        "W": 108, "H": 91, "W_arms": W_ARMS,
        "populations": rule["populations"],
        "step5_waterfall_reasserted": rule["step5_waterfall_reasserted"],
        "reused_inputs": rule["reused_inputs"],
        "headline": {
            "DERIV_W108": {
                "n": d8["n_before_liveness"],
                "excluded": d8["excluded_pairs"],
                "excluded_never_started": d8["excluded_never_started"],
                "excluded_started_and_left": d8["excluded_started_and_left"],
                "accounts": d8["accounts_supplying_exclusions"],
                "excluded_share_pct": d8["excluded_share_of_population_pct"],
            },
            "APPLY_W108": {
                "n": a8["n_before_liveness"],
                "excluded": a8["excluded_pairs"],
                "excluded_never_started": a8["excluded_never_started"],
                "excluded_started_and_left": a8["excluded_started_and_left"],
                "accounts": a8["accounts_supplying_exclusions"],
                "excluded_share_pct": a8["excluded_share_of_population_pct"],
            },
        },
        "shares": {p: {"no_filter": rule["by_population"][p]["108"]["no_filter"],
                       "under_rule": rule["by_population"][p]["108"]["under_rule"],
                       "delta_pp": rule["by_population"][p]["108"]["delta_vs_no_filter_pp"]}
                   for p in ("DERIV", "APPLY")},
        "bounds": {p: {"never_started": rule["by_population"][p]["108"]["never_started_bound"],
                       "started_and_left": rule["by_population"][p]["108"]["started_and_left_bound"],
                       "continued": rule["by_population"][p]["108"]["continued_bound"]}
                   for p in ("DERIV", "APPLY")},
        "per_arm": {
            p: {
                "W": W_ARMS,
                "population_n": [rule["by_population"][p][str(w)]["n_before_liveness"]
                                 for w in W_ARMS],
                "excluded_total": [rule["by_population"][p][str(w)]["excluded_pairs"]
                                   for w in W_ARMS],
                "excluded_never_started": [
                    rule["by_population"][p][str(w)]["excluded_never_started"] for w in W_ARMS],
                "excluded_started_and_left": [
                    rule["by_population"][p][str(w)]["excluded_started_and_left"] for w in W_ARMS],
                "accounts": [rule["by_population"][p][str(w)]["accounts_supplying_exclusions"]
                             for w in W_ARMS],
                "never_started_bound_pct": [
                    [rule["by_population"][p][str(w)]["never_started_bound"]["floor_pct"],
                     rule["by_population"][p][str(w)]["never_started_bound"]["ceiling_pct"]]
                    for w in W_ARMS],
                "started_and_left_bound_over_SL_exclusions_pct": [
                    [rule["by_population"][p][str(w)]["started_and_left_bound"]["floor_pct"],
                     rule["by_population"][p][str(w)]["started_and_left_bound"]
                         ["ceiling_over_SL_exclusions_pct"]] for w in W_ARMS],
                "D10_reading": "RE-DERIVED at each arm (decisions/0047 Sec 5). NOT frozen at 108.",
            } for p in ("DERIV", "APPLY")},
        "W_coupling": rule["claims_tested"]["APPLY_W_coupling_factor"],
        "waterfall": wf["waterfall"],
        "monotone_invariant": wf["monotone_invariant_for_step8"],
        "bootstrap": boot,
        "calibration_residual": {
            "calibration": {k: v for k, v in resid["calibration"].items() if k != "stored_meta"},
            "R1_in_sample_residual_days": resid["R1_in_sample_residual_days"],
            "R2_future_dated": resid["R2_future_dated"],
            "R3_clamping": resid["R3_clamping"],
            "margins": marg["by_population"],
            "sensitivity": marg["M3_sensitivity"],
            "stability_verdict": marg["stability_verdict"],
            "residual_ladder_days": marg["residual_ladder_days"],
            "residual_ladder_provenance": marg["residual_ladder_provenance"],
            "residual_shape": marg["residual_shape"],
        },
        "claims_tested": rule["claims_tested"],
    }
    (ART / "step7-liveness-bb-b.json").write_text(json.dumps(out, indent=2))
    print("wrote", ART / "step7-liveness-bb-b.json", f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
