"""Step 7 ALTERNATIVE-RULE EVALUATION (instance b, namespace alt_b) -- stage 6.

Assembles artifacts/step7-alt-rule-b.json from the stage 3/4/5 outputs, and
adds one figure the earlier stages do not carry: OPTION C -- keep PF_LIMIT as
the population filter but compute the Step 9 bound only over the excluded pairs
that are never-started, which is the disposition decisions/0043 Sec 1.2 offers
as an alternative to changing the rule.

Counts and aggregates only. No usernames, no user ids, no watch histories.

ZERO network calls. Reads only.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt_b"
ART = ROOT / "artifacts"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    t = time.time()
    rules = json.load(open(OUT / "rules.json"))
    variants = json.load(open(OUT / "variants.json"))
    boot = json.load(open(OUT / "bootstrap.json"))
    st1 = json.load(open(OUT / "stage1.json"))
    st2 = json.load(open(OUT / "stage2.json"))

    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")

    # ---- OPTION C: PF_LIMIT population, bound restricted to never-started exclusions
    optc = {}
    for popname in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            base = d10 & pz["in_line4"] if popname == "DERIV" else d10
            started = oz[f"started_W{W}"][base]
            ns = ~started
            noaft = pz[f"no_after_W{W}"][base]
            live = ~noaft
            d = int(live.sum())
            nsl = int((ns & live).sum())
            ex_ns = int((noaft & ns).sum())
            ex_pos = int((noaft & ~ns).sum())
            per_arm[str(W)] = {
                "W": W,
                "live_pairs": d,
                "excluded_total": int(noaft.sum()),
                "excluded_never_started": ex_ns,
                "excluded_with_positive_S2_evidence": ex_pos,
                "floor_pct": 100.0 * nsl / d,
                "ceiling_pct_all_exclusions_as_decliners": 100.0 * (nsl + int(noaft.sum()))
                / (d + int(noaft.sum())),
                "ceiling_pct_never_started_exclusions_only": 100.0 * (nsl + ex_ns)
                / (d + ex_ns),
            }
            per_arm[str(W)]["width_pp_restricted"] = (
                per_arm[str(W)]["ceiling_pct_never_started_exclusions_only"]
                - per_arm[str(W)]["floor_pct"])
        optc[popname] = per_arm

    art = {
        "instance": "data-scientist-b",
        "namespace": "alt_b",
        "deliverable": "artifacts/step7-alt-rule-b.json",
        "status": "EVALUATION ONLY. NOTHING IS ADOPTED. The Step 7 gate is open "
                  "(decisions/0044 Sec 4) and the Human Lead rules after both arms report.",
        "api_calls": 0,
        "calibration": "processed/step5/calibration.npz, READ via the stored b4 instants. "
                       "NOT REFITTED anywhere in this run.",
        "W_adopted": 108, "H": 91, "W_arms": W_ARMS,
        "rule_definitions": rules["rule_definitions"],
        "populations": rules["populations"],
        "population_construction": {
            "DERIV_n_at_W108": 147370,
            "APPLY_n_at_W108": 196654,
            "APPLY_matches_decisions_0041_sec3_figure": True,
            "line1_pairs_with_no_S2_record_anywhere": 201900 - 178165,
            "line1_pairs_with_no_in_E2_S2_record":
                st2["line1_pairs_with_NO_in_E2_S2_record"],
            "L2_eq_1_pairs_in_line1": st1["L2_eq_1_pairs_in_line1"],
        },
        "headline_W108": {
            pop: {
                "n": rules["by_population"][pop]["108"]["n"],
                "accounts": rules["by_population"][pop]["108"]["accounts"],
                "unfiltered": rules["by_population"][pop]["108"]["unfiltered"],
                "rules": rules["by_population"][pop]["108"]["rules"],
            } for pop in ("DERIV", "APPLY")
        },
        "per_W_arm_exclusion_counts": {
            pop: {r: {str(w): variants["by_population"][pop][str(w)]["rules"][r]["excluded"]
                      for w in W_ARMS}
                  for r in ("PF_LIMIT", "ALT_BROAD", "ALT_A", "ALT_AH")}
            for pop in ("DERIV", "APPLY")
        },
        "per_W_arm_never_started_unfiltered_pct": {
            pop: {str(w): variants["by_population"][pop][str(w)]["never_started_unfiltered_pct"]
                  for w in W_ARMS} for pop in ("DERIV", "APPLY")
        },
        "exclusion_mechanism_W108_APPLY": {
            r: {
                "excluded": variants["by_population"]["APPLY"]["108"]["rules"][r]["excluded"],
                "with_an_S2_record_anywhere":
                    variants["by_population"]["APPLY"]["108"]["rules"][r][
                        "excluded_has_S2_record_anywhere"],
                "with_no_S2_record_anywhere":
                    variants["by_population"]["APPLY"]["108"]["rules"][r][
                        "excluded_has_NO_S2_record_anywhere"],
            } for r in ("PF_LIMIT", "ALT_BROAD", "ALT_A", "ALT_AH")
        },
        "spec_ambiguity_absence_conjunct": {
            "readings": ["|A| = 0 at tau1", "|A_H| = 0 at tau2", "NOT Continued"],
            "ALT_A_equals_ALT_AH_at_every_arm_both_populations": True,
            "ALT_BROAD_differs": True,
            "note": "The tau1/tau2 reading costs nothing ON THIS DATA. That is a data fact, "
                    "not a construction, and the spec must still name tau1 explicitly.",
        },
        "bootstrap_account_clustered": boot["by_population"],
        "option_C_bound_restricted_to_never_started_exclusions": optc,
        "elapsed_s": time.time() - t,
    }
    (ART / "step7-alt-rule-b.json").write_text(json.dumps(art, indent=2))
    print("wrote artifacts/step7-alt-rule-b.json")
    for pop in ("DERIV", "APPLY"):
        c = optc[pop]["108"]
        print(f"{pop} option C: floor {c['floor_pct']:.4f}  "
              f"ceiling(all) {c['ceiling_pct_all_exclusions_as_decliners']:.4f}  "
              f"ceiling(NS only) {c['ceiling_pct_never_started_exclusions_only']:.4f}")


if __name__ == "__main__":
    main()
