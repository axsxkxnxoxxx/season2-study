"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 4c.

Characterises the pairs that COULD be excluded at some W but are not excluded
at the tested arms, and identifies which filter actually produces the DERIV
zero. Counts only; nothing here identifies an account.

Out: processed/step7/alt2_b/candidates.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt2_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    fz = np.load(OUT / "feasible_W.npz")
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    lo, hi = fz["lo_days"], fz["hi_days"]
    ne, has_inE2, in4 = fz["nonempty"], fz["has_s2"], fz["in_line4"]
    any_rec = oz["has_any_s2_record_anywhere"]

    d4 = ne & in4
    res = {
        "instance": "data-scientist-b", "namespace": "alt2_b", "stage": "4c",
        "api_calls": 0, "adopts": "nothing",
        "DERIV_line4_candidates": {
            "total": int(d4.sum()),
            "with_an_in_E2_S2_record_finite_upper_end": int((d4 & has_inE2).sum()),
            "with_an_S2_record_but_none_in_E2_upper_end_infinite":
                int((d4 & ~has_inE2 & any_rec).sum()),
            "with_no_S2_record_anywhere": int((d4 & ~any_rec).sum()),
        },
        "per_arm_DERIV": {},
        "per_arm_APPLY": {},
    }
    for W in W_ARMS:
        d10 = pz[f"d10_W{W}"]
        inW = ne & (lo <= W) & (W <= hi)
        res["per_arm_DERIV"][str(W)] = {
            "line4_pairs_satisfying_both_conjuncts_before_D10": int((inW & in4).sum()),
            "of_which_survive_D10_and_are_therefore_excluded": int((inW & in4 & d10).sum()),
            "of_which_removed_earlier_by_D10_right_censoring": int((inW & in4 & ~d10).sum()),
            "those_removed_by_D10_that_hold_an_in_E2_S2_record":
                int((inW & in4 & ~d10 & has_inE2).sum()),
        }
        res["per_arm_APPLY"][str(W)] = {
            "line1_pairs_satisfying_both_conjuncts_before_D10": int(inW.sum()),
            "of_which_survive_D10_and_are_therefore_excluded": int((inW & d10).sum()),
            "of_which_removed_earlier_by_D10_right_censoring": int((inW & ~d10).sum()),
            "excluded_pairs_holding_an_in_E2_S2_record": int((inW & d10 & has_inE2).sum()),
            "excluded_pairs_holding_an_S2_record_not_in_E2":
                int((inW & d10 & ~has_inE2 & any_rec).sum()),
        }
    res["reading"] = (
        "On DERIV the pairs that satisfy BOTH conjuncts are not absent -- they are removed one "
        "position earlier, by D10 right-censoring at position 5. The zero at position 6 is "
        "produced by the filter order, not by line 4's has_s2 requirement as 0046 Sec 1 states.")
    (OUT / "candidates.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
