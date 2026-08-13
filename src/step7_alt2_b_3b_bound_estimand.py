"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 3b.

Which estimand does the Step 9 bound bound?

decisions/0046 Sec 4 rejects PF-LIMIT's published interval because it "mixed
denominators -- floor on 195,299, ceiling on 195,903" and because "its floor was
not a floor: if all 604 had actually started -- the exact case liveness exists
to guard against -- the share is 16.727%, BELOW the published floor."

The adopted rule's interval is floor = NS_live / n_live and ceiling =
NS_unfiltered / n_unfiltered. Those are also two denominators. This stage
computes, on the SINGLE unfiltered denominator, the feasible range of the
never-started share given that the excluded pairs' true status is unknown:

    all excluded truly never started -> NS_unfiltered / n_unfiltered   (= the ceiling)
    all excluded actually started    -> NS_live       / n_unfiltered

and reports where the published floor sits relative to that range.

No adoption, no recommendation beyond stating what each number bounds.

Out: processed/step7/alt2_b/bound_estimand.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt2_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    rule = json.load(open(OUT / "rule.json"))
    res = {"instance": "data-scientist-b", "namespace": "alt2_b", "stage": "3b",
           "api_calls": 0, "adopts": "nothing",
           "estimands": {
               "E1_share_among_live_pairs":
                   "denominator = pairs retained by liveness. The published floor is this.",
               "E2_share_on_the_full_population":
                   "denominator = the position-5 population, the excluded pairs' status unknown.",
           },
           "by_population": {}}

    for pop in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            a = rule["by_population"][pop][str(W)]
            n_tot = a["no_filter"]["n"]
            ns_tot = a["no_filter"]["never_started"]
            n_live = a["under_rule"]["n"]
            ns_live = a["under_rule"]["never_started"]
            ex = a["excluded_pairs"]
            pub_floor = a["step9_bound"]["floor_pct"]
            pub_ceiling = a["step9_bound"]["ceiling_pct"]
            e2_lo = 100.0 * ns_live / n_tot      # every excluded pair actually started
            e2_hi = 100.0 * ns_tot / n_tot       # every excluded pair truly never started
            per_arm[str(W)] = {
                "W": W, "excluded": ex,
                "published_bound_E1_floor_E2_ceiling": [pub_floor, pub_ceiling],
                "floor_denominator": n_live, "ceiling_denominator": n_tot,
                "single_denominator_interval_E2": [e2_lo, e2_hi],
                "single_denominator": n_tot,
                "published_floor_minus_E2_low_pp": pub_floor - e2_lo,
                "published_floor_is_a_floor_for_E2": pub_floor <= e2_lo,
                "E1_and_E2_coincide_when_no_exclusions": ex == 0,
                "E2_width_pp": e2_hi - e2_lo,
                "published_width_pp": pub_ceiling - pub_floor,
            }
        res["by_population"][pop] = per_arm

    a = res["by_population"]["APPLY"]["108"]
    res["headline_reading_APPLY_W108"] = (
        f"The published interval [{a['published_bound_E1_floor_E2_ceiling'][0]:.4f}%, "
        f"{a['published_bound_E1_floor_E2_ceiling'][1]:.4f}%] takes its floor on "
        f"{a['floor_denominator']:,} and its ceiling on {a['ceiling_denominator']:,}. On the single "
        f"denominator {a['single_denominator']:,} the feasible range is "
        f"[{a['single_denominator_interval_E2'][0]:.4f}%, "
        f"{a['single_denominator_interval_E2'][1]:.4f}%], width "
        f"{a['E2_width_pp']:.4f} pp. The published floor sits "
        f"{a['published_floor_minus_E2_low_pp']:+.4f} pp above the low end, so it is NOT a floor "
        "for the full-population share -- which is the objection 0046 Sec 4 raised against "
        "PF-LIMIT's floor, and it applies to the adopted rule's floor in the same form. The "
        "ceiling is unaffected: it is the identity, and it is the same number under both "
        "estimands.")
    (OUT / "bound_estimand.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_population"]["APPLY"]["108"], indent=2))
    print(res["headline_reading_APPLY_W108"])


if __name__ == "__main__":
    main()
