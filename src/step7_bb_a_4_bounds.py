"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 4 of 7 — the bounds.

STANDING RULE (decisions/0047 SS3): an interval endpoint states the population it is computed
on and the estimand it bounds, AND THEY MUST BE THE SAME POPULATION. Three consecutive bounds
in this chain failed that test. Everything here is computed on the POSITION-5 population
(APPLY = 196,654; DERIV = 147,370) with a FIXED denominator, in exact integer arithmetic.

WHAT THE RULE LEAVES UNRESOLVED, per excluded pair:
  never-started component (604 on APPLY, 0 on DERIV)
      recorded Never started. |A| = 0 is a NULL. Truth may be Never started, Started-and-left
      or Continued. -> it can only REMOVE from the never-started numerator, and can only ADD
      to the started-and-left and continued numerators.
  started-and-left component (99 on both)
      recorded Started and left. |A| >= 1 is OBSERVED, so the pair DID start; what is null is
      the failure to meet the Continued condition. Truth is Started-and-left or Continued.
      -> it can only REMOVE from the started-and-left numerator, and only ADD to continued.
      It CANNOT reach the never-started numerator, which is why the never-started bound is
      unchanged from ALT.

Zero API calls.
"""
import json
import os
from fractions import Fraction

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/bb_a")


def pct(num, den):
    return float(Fraction(num, den) * 100)


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    out = {"step": 7, "instance": "bb_a", "stage": 4, "api_calls": 0,
           "rule": "NOT LIVE iff (no insertion instant after tau1) AND (NOT Continued)",
           "standing_rule": "every endpoint is computed on the SAME population as the estimand "
                            "it bounds; here that is the position-5 population, fixed "
                            "denominator, exact integer arithmetic",
           "by_population": {}}

    for nm, p in pops.items():
        N = int(p.sum())
        n_ns = int((never & p).sum())
        n_co = int((cont & p).sum())
        n_sl = int((left & p).sum())
        k_ns = int((ex_ns & p).sum())
        k_sl = int((ex_sl & p).sum())
        k = k_ns + k_sl
        assert n_ns + n_co + n_sl == N
        assert int((ex & p).sum()) == k

        # ---- BOUND 1: never started, on the position-5 population -------------------
        ns_lo_num, ns_hi_num = n_ns - k_ns, n_ns
        # ---- BOUND 2: started and left, on the SAME population ---------------------
        # valid (unconditional) bound: the 99 may float up into Continued, and any of the
        # k_ns never-started nulls may in truth have started and left
        sl_lo_num, sl_hi_num = n_sl - k_sl, n_sl + k_ns
        # the component attributable to the started-and-left exclusions ALONE. This is NOT a
        # bound on the unconditional estimand: its ceiling does not cover the case in which an
        # excluded never-started null in truth started and left. It is a bound on the estimand
        # CONDITIONAL on every never-started null being true.
        sl_c_lo_num, sl_c_hi_num = n_sl - k_sl, n_sl
        # ---- BOUND 3: continued, on the same population ----------------------------
        co_lo_num, co_hi_num = n_co, n_co + k

        rec = {
            "population": nm,
            "population_pairs_denominator": N,
            "population_definition": ("Step 5 line 4 less D10" if nm == "DERIV"
                                      else "Step 5 line 1 less D10, what Step 8 filters"),
            "unfiltered_counts": {"never_started": n_ns, "continued": n_co,
                                  "started_and_left": n_sl},
            "exclusions": {"total": k, "never_started_component": k_ns,
                           "started_and_left_component": k_sl},

            "bound_never_started": {
                "estimand": "share of the position-5 population whose true state is "
                            "Never started",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(ns_lo_num, N), 6),
                "ceiling_pct": round(pct(ns_hi_num, N), 6),
                "floor_numerator": ns_lo_num, "ceiling_numerator": ns_hi_num,
                "width_pp": round(pct(ns_hi_num - ns_lo_num, N), 6),
                "floor_attained_when": f"all {k_ns} excluded never-started nulls in truth "
                                       f"started",
                "ceiling_attained_when": f"all {k_ns} excluded never-started nulls are true "
                                         f"declines; the {k_sl} started-and-left exclusions "
                                         f"cannot enter either endpoint",
                "ceiling_equals_unfiltered_never_started_share": (
                    Fraction(ns_hi_num, N) == Fraction(n_ns, N)),
                "identity_note": "the ceiling equals the unfiltered share because the ceiling "
                                 "numerator IS the unfiltered numerator on the unfiltered "
                                 "denominator. 0046 SS4's phrasing -- 'returning every excluded "
                                 "pair as a decliner reproduces the unfiltered population' -- "
                                 "no longer holds under ALT-BROAD: returning all "
                                 f"{k} exclusions as decliners would give "
                                 f"{round(pct(n_ns + k, N), 6)}%, which is NOT attainable, "
                                 f"because the {k_sl} started-and-left exclusions have "
                                 "|A| >= 1 observed.",
                "unattainable_all_exclusions_as_decliners_pct": round(pct(n_ns + k, N), 6),
            },

            "bound_started_and_left": {
                "estimand": "share of the position-5 population whose true state is "
                            "Started and left",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(sl_lo_num, N), 6),
                "ceiling_pct": round(pct(sl_hi_num, N), 6),
                "floor_numerator": sl_lo_num, "ceiling_numerator": sl_hi_num,
                "width_pp": round(pct(sl_hi_num - sl_lo_num, N), 6),
                "floor_attained_when": f"all {k_sl} excluded started-and-left nulls in truth "
                                       f"continued",
                "ceiling_attained_when": f"all {k_ns} excluded never-started nulls in truth "
                                         f"started and left, and all {k_sl} started-and-left "
                                         f"exclusions are true exits",
                "both_endpoints_attainable": True,
            },

            "bound_started_and_left_COMPONENT_over_the_SL_exclusions_only": {
                "estimand": "share of the position-5 population whose true state is Started "
                            "and left, CONDITIONAL on every excluded never-started null being "
                            "a true decline",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(sl_c_lo_num, N), 6),
                "ceiling_pct": round(pct(sl_c_hi_num, N), 6),
                "width_pp": round(pct(sl_c_hi_num - sl_c_lo_num, N), 6),
                "WARNING": "this is NOT a bound on the unconditional started-and-left share. "
                           "Its ceiling does not cover the case in which an excluded "
                           "never-started null in truth started and left -- the same defect "
                           "0047 SS3 records three times. Published only as the DECOMPOSITION "
                           "of the lower half of bound_started_and_left, which is the "
                           "operative interval.",
            },

            "bound_continued": {
                "estimand": "share of the position-5 population whose true state is Continued",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(co_lo_num, N), 6),
                "ceiling_pct": round(pct(co_hi_num, N), 6),
                "width_pp": round(pct(co_hi_num - co_lo_num, N), 6),
                "note": "Continued is the only state that rests on positive evidence, so no "
                        "exclusion can leave it; both other states can only flow INTO it",
            },

            "joint_corner_check": {
                "never_started_floor_with_started_and_left_ceiling": {
                    "resolution": f"all {k_ns} never-started nulls started and left; all "
                                  f"{k_sl} started-and-left exclusions are true exits",
                    "never_started_pct": round(pct(ns_lo_num, N), 6),
                    "started_and_left_pct": round(pct(sl_hi_num, N), 6),
                    "continued_pct": round(pct(n_co, N), 6),
                    "sums_to_100": (ns_lo_num + sl_hi_num + n_co) == N,
                },
                "never_started_ceiling_with_started_and_left_floor": {
                    "resolution": f"all {k_ns} never-started nulls are true declines; all "
                                  f"{k_sl} started-and-left exclusions in truth continued",
                    "never_started_pct": round(pct(ns_hi_num, N), 6),
                    "started_and_left_pct": round(pct(sl_lo_num, N), 6),
                    "continued_pct": round(pct(n_co + k_sl, N), 6),
                    "sums_to_100": (ns_hi_num + sl_lo_num + n_co + k_sl) == N,
                },
                "reading": "both corners are attainable resolutions of the same population, "
                           "so the two intervals are simultaneously tight",
            },

            "shares_under_the_rule_on_the_FILTERED_denominator": {
                "note": "reported because Step 8 hands Step 9 the filtered table; these are "
                        "NOT the bound endpoints and must never be mixed with them",
                "denominator": N - k,
                "never_started_pct": round(pct(n_ns - k_ns, N - k), 6),
                "continued_pct": round(pct(n_co, N - k), 6),
                "started_and_left_pct": round(pct(n_sl - k_sl, N - k), 6),
            },
        }
        out["by_population"][nm] = rec

    # ALT comparison on the never-started bound: asserted identical, not assumed
    a = out["by_population"]["APPLY"]
    N = a["population_pairs_denominator"]
    n_ns = a["unfiltered_counts"]["never_started"]
    k_ns = a["exclusions"]["never_started_component"]
    out["never_started_bound_vs_ALT"] = {
        "ALT_exclusions_on_APPLY": 604,
        "ALT_BROAD_never_started_component_on_APPLY": k_ns,
        "ALT_published_bound_0047": [16.6633, 16.9704],
        "ALT_BROAD_bound_APPLY": [a["bound_never_started"]["floor_pct"],
                                  a["bound_never_started"]["ceiling_pct"]],
        "identical": (round(pct(n_ns - k_ns, N), 4) == 16.6633
                      and round(pct(n_ns, N), 4) == 16.9704),
        "why": "the started-and-left exclusions have |A| >= 1 OBSERVED, so they cannot enter "
               "either endpoint of the never-started bound; the never-started component of "
               "the exclusion set is exactly ALT's exclusion set, 604 on APPLY",
        "width_pp": a["bound_never_started"]["width_pp"],
    }

    with open(os.path.join(OUT, "bounds.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
