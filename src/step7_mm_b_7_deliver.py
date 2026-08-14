"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 7: DELIVER.

Assembles artifacts/step7-liveness-mm-b.json from the stage outputs. COUNTS AND
AGGREGATES ONLY -- no usernames, no user ids, no individual watch histories.

ZERO network calls.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P = ROOT / "processed" / "step7" / "mm_b"
ART = ROOT / "artifacts" / "step7-liveness-mm-b.json"
ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
W = 108


def main() -> None:
    t = time.time()
    s1 = json.load(open(P / "stage1.json"))
    s2 = json.load(open(P / "stage2.json"))
    rule = json.load(open(P / "rule.json"))
    wf = json.load(open(P / "waterfall.json"))
    ch = json.load(open(P / "channel.json"))
    fz = json.load(open(P / "frozen_d10.json"))
    bs = json.load(open(P / "bootstrap.json"))
    mg = json.load(open(P / "margins.json"))

    out: dict = {
        "step": 7, "instance": "data-scientist-b", "namespace": "mm_b",
        "date": "2026-08-14", "api_calls": 0, "adopts": "nothing",
        "gate": ("Step 7 is a GATE. Everything here is a PROPOSAL for the Human Lead to approve "
                 "and to diff against the other arm. This instance adopted nothing and did not "
                 "read the other arm's work."),
        "rule_name": "ALT-MATCHED",
        "rule": rule["rule"],
        "rule_source": "decisions/0052 Sec 1; task-sheet.md Step 7",
        "supersedes": "ALT-BROAD (decisions/0048 Sec 1)",
        "populations": rule["populations"],
        "W_adopted": W, "H": 91, "W_arms": ARMS,
        "provenance": {
            "step5_waterfall_recomputed": s1["step5_waterfall_measured"],
            "step5_waterfall_expected": s1["step5_waterfall_expected"],
            "populations_asserted_at_W108": s1["populations_asserted_at_W108"],
            "calibration": s1["calibration"],
            "records_in_sweep": s1["records_in_sweep"],
            "accounts_in_line1": s1["accounts_present_in_line1"],
            "crosschecks": {
                "per_account_max_insertion_instant": s1["crosscheck_bb_b_acct_instants"],
                "pair_identity_T0_line4_k_F2_L2": s1["crosscheck_alt2_b_pairs"],
                "silence_at_tau1_and_D10": s1["crosscheck_silence_at_tau1_and_D10"],
                "outcome_assignment": s2["crosscheck_alt2_b_outcomes"],
            },
            "L2_eq_1_pairs_in_this_frame": s1["L2_eq_1_pairs_in_line1"],
            "D10": "RE-DERIVED at each arm (0047 Sec 5); the frozen reading is reported separately",
        },
        "headline_at_W108": {
            pop: {
                "population_n": rule["by_population"][pop][str(W)]["n_before_liveness"],
                "excluded_pairs": rule["by_population"][pop][str(W)]["excluded_pairs"],
                "excluded_never_started": rule["by_population"][pop][str(W)]["excluded_never_started"],
                "excluded_started_and_left":
                    rule["by_population"][pop][str(W)]["excluded_started_and_left"],
                "excluded_continued": 0,
                "accounts_supplying_exclusions":
                    rule["by_population"][pop][str(W)]["accounts_supplying_exclusions"],
                "ALT_BROAD_superseded":
                    rule["by_population"][pop][str(W)]["ALT_BROAD_SUPERSEDED"],
                "selection_path": rule["by_population"][pop][str(W)]["selection_path"],
                "shares_no_filter": rule["by_population"][pop][str(W)]["no_filter"],
                "shares_under_rule": rule["by_population"][pop][str(W)]["under_rule"],
                "movement_pp": rule["by_population"][pop][str(W)]["delta_vs_no_filter_pp"],
                "bounds": rule["by_population"][pop][str(W)]["bounds"],
            } for pop in ("DERIV", "APPLY")
        },
        "claims_tested": rule["claims_tested"],
        "per_arm": {
            pop: {
                "D10_reading": "re-derived at each arm",
                "W": ARMS,
                "n": [rule["by_population"][pop][str(w)]["n_before_liveness"] for w in ARMS],
                "excluded": [rule["by_population"][pop][str(w)]["excluded_pairs"] for w in ARMS],
                "never_started_component":
                    [rule["by_population"][pop][str(w)]["excluded_never_started"] for w in ARMS],
                "started_and_left_component":
                    [rule["by_population"][pop][str(w)]["excluded_started_and_left"] for w in ARMS],
                "accounts":
                    [rule["by_population"][pop][str(w)]["accounts_supplying_exclusions"]
                     for w in ARMS],
                "ALT_BROAD_superseded_excluded":
                    [rule["by_population"][pop][str(w)]["ALT_BROAD_SUPERSEDED"]["excluded_pairs"]
                     for w in ARMS],
                "ALT_BROAD_superseded_started_and_left_component":
                    [rule["by_population"][pop][str(w)]["ALT_BROAD_SUPERSEDED"]
                     ["excluded_started_and_left"] for w in ARMS],
                "never_started_bound_floor_pct":
                    [rule["by_population"][pop][str(w)]["bounds"]["never_started"]["floor_pct"]
                     for w in ARMS],
                "never_started_bound_ceiling_pct":
                    [rule["by_population"][pop][str(w)]["bounds"]["never_started"]["ceiling_pct"]
                     for w in ARMS],
                "started_and_left_bound_floor_pct":
                    [rule["by_population"][pop][str(w)]["bounds"]["started_and_left"]["floor_pct"]
                     for w in ARMS],
                "started_and_left_bound_ceiling_pct":
                    [rule["by_population"][pop][str(w)]["bounds"]["started_and_left"]["ceiling_pct"]
                     for w in ARMS],
                "continued_bound_ceiling_pct":
                    [rule["by_population"][pop][str(w)]["bounds"]["continued"]["ceiling_pct"]
                     for w in ARMS],
            } for pop in ("DERIV", "APPLY")
        },
        "W_coupling": rule["claims_tested"]["APPLY_W_coupling_38_to_213"],
        "waterfall": wf,
        "channel": ch,
        "frozen_D10_reading": fz,
        "bootstrap": bs,
        "margins_and_residual_stability": mg,
    }
    ART.write_text(json.dumps(out, indent=2))
    print(f"wrote {ART}  ({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
