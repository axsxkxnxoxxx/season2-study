"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 4 — THE BOUNDS.

STANDING RULE (0047 SS3): an interval endpoint states the population it is computed on AND the
estimand it bounds, and they must be the SAME population. Everything here is on the POSITION-5
population (APPLY = 196,654; DERIV = 147,370) with a FIXED denominator, exact integer arithmetic.

WHAT THE RULE LEAVES UNRESOLVED, per excluded pair:
  never-started component (604 on APPLY, 0 on DERIV)
      recorded Never started. |A| = 0 is a NULL. Truth may be Never started, Started-and-left or
      Continued. -> can only LEAVE the never-started numerator; can only ENTER the other two.
  started-and-left component (189 on APPLY, 188 on DERIV)
      recorded Started and left. |A| >= 1 is OBSERVED, so the pair DID start. Truth is
      Started-and-left or Continued. -> can only LEAVE the started-and-left numerator; can only
      ENTER continued. It CANNOT reach the never-started numerator, which is why the
      never-started bound is unchanged by the rule change.

THREE CEILINGS (0052 SS2). Continued has a ceiling too, because any EXCLUDED pair may in truth be
Continued. The three are ALTERNATIVE worst cases over ONE set, not simultaneous ones, so they sum
to more than 100%; the excess is computed and attributed here rather than asserted.

Zero API calls.
"""
import json
import os
from fractions import Fraction

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/mm_a")


def pct(num, den):
    return float(Fraction(int(num), int(den)) * 100)


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    out = {"step": 7, "instance": "mm_a", "stage": 4, "api_calls": 0,
           "rule": ("NOT LIVE iff (|A|=0 AND silent after tau1) OR "
                    "(|A|>=1 AND NOT Continued AND silent after tau2)"),
           "standing_rule": "every endpoint is on the SAME population as the estimand it bounds; "
                            "here the position-5 population, fixed denominator, exact integers",
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

        ns_lo, ns_hi = n_ns - k_ns, n_ns                  # BOUND 1  never started
        sl_lo, sl_hi = n_sl - k_sl, n_sl + k_ns           # BOUND 2  started and left
        co_lo, co_hi = n_co, n_co + k                     # BOUND 3  continued
        sl_c_lo, sl_c_hi = n_sl - k_sl, n_sl              # conditional sub-interval only

        ceil_sum = pct(ns_hi, N) + pct(sl_hi, N) + pct(co_hi, N)

        rec = {
            "population": nm,
            "population_pairs_denominator": N,
            "population_definition": ("Step 5 line 4 less D10 (requires S2 evidence)"
                                      if nm == "DERIV"
                                      else "Step 5 line 1 less D10, what Step 8 filters"),
            "position": "POSITION 5 — before the liveness filter at position 6",
            "unfiltered_counts": {"never_started": n_ns, "continued": n_co,
                                  "started_and_left": n_sl},
            "exclusions": {"total": k, "never_started_component": k_ns,
                           "started_and_left_component": k_sl},

            "bound_never_started": {
                "estimand": "share of the position-5 population whose TRUE state is Never started",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(ns_lo, N), 6), "ceiling_pct": round(pct(ns_hi, N), 6),
                "floor_numerator": ns_lo, "ceiling_numerator": ns_hi,
                "width_pp": round(pct(ns_hi - ns_lo, N), 6),
                "floor_attained_when": f"all {k_ns} excluded never-started nulls in truth started",
                "ceiling_attained_when": f"all {k_ns} excluded never-started nulls are true "
                                        f"declines; the {k_sl} started-and-left exclusions "
                                        f"cannot enter either endpoint",
                "ceiling_equals_unfiltered_never_started_share": Fraction(ns_hi, N) == Fraction(n_ns, N),
                "identity_note": "the ceiling equals the unfiltered share because the ceiling "
                                 "numerator IS the unfiltered numerator on the unfiltered "
                                 "denominator. 0046 SS4's phrasing -- 'returning every excluded "
                                 "pair as a decliner reproduces the unfiltered population' -- is "
                                 "FALSE here: returning all "
                                 f"{k} exclusions as decliners gives {round(pct(n_ns + k, N), 6)}%, "
                                 f"which is NOT attainable, because the {k_sl} started-and-left "
                                 "exclusions have |A| >= 1 OBSERVED.",
                "unattainable_all_exclusions_as_decliners_pct": round(pct(n_ns + k, N), 6),
                "unchanged_from_ALT_BROAD_because": "the rule change moved only started-and-left "
                                                    "pairs into the exclusion set; k_ns is "
                                                    "identical, and both endpoints depend on k_ns "
                                                    "alone",
            },

            "bound_started_and_left": {
                "estimand": "share of the position-5 population whose TRUE state is "
                            "Started and left",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(sl_lo, N), 6), "ceiling_pct": round(pct(sl_hi, N), 6),
                "floor_numerator": sl_lo, "ceiling_numerator": sl_hi,
                "width_pp": round(pct(sl_hi - sl_lo, N), 6),
                "floor_attained_when": f"all {k_sl} excluded started-and-left nulls in truth "
                                      f"continued",
                "ceiling_attained_when": f"all {k_ns} excluded never-started nulls in truth "
                                        f"started and left, and all {k_sl} started-and-left "
                                        f"exclusions are true exits",
                "over_ALL_exclusions_on_one_denominator": True,
                "both_endpoints_attainable": True,
            },

            "bound_started_and_left_CONDITIONAL_sub_interval": {
                "estimand": "started-and-left share CONDITIONAL on every excluded never-started "
                            "null being a true decline",
                "denominator": N,
                "floor_pct": round(pct(sl_c_lo, N), 6), "ceiling_pct": round(pct(sl_c_hi, N), 6),
                "width_pp": round(pct(sl_c_hi - sl_c_lo, N), 6),
                "WARNING": "NOT a bound on the unconditional estimand. Its ceiling does not cover "
                           "the case in which an excluded never-started null in truth started and "
                           "left. Published only as a LABELLED conditional sub-interval, per "
                           "task-sheet Step 9.",
            },

            "bound_continued": {
                "estimand": "share of the position-5 population whose TRUE state is Continued",
                "denominator": N, "denominator_is_the_estimands_population": True,
                "floor_pct": round(pct(co_lo, N), 6), "ceiling_pct": round(pct(co_hi, N), 6),
                "floor_numerator": co_lo, "ceiling_numerator": co_hi,
                "width_pp": round(pct(co_hi - co_lo, N), 6),
                "floor_attained_when": "no excluded pair is in truth Continued",
                "ceiling_attained_when": f"ALL {k} excluded pairs are in truth Continued",
                "why_continued_has_a_ceiling": "no exclusion can LEAVE Continued -- it is the only "
                                               "state resting on positive evidence -- but every "
                                               "excluded pair can ENTER it, so the ceiling is the "
                                               "unfiltered count plus the whole exclusion set",
            },

            "THREE_CEILINGS": {
                "never_started_ceiling_pct": round(pct(ns_hi, N), 4),
                "started_and_left_ceiling_pct": round(pct(sl_hi, N), 4),
                "continued_ceiling_pct": round(pct(co_hi, N), 4),
                "sum_pct": round(ceil_sum, 4),
                "excess_over_100_pp": round(ceil_sum - 100.0, 4),
                "excess_numerator_check": 2 * k_ns + k_sl,
                "excess_as_fraction_pct": round(pct(2 * k_ns + k_sl, N), 4),
                "mechanism": "the excluded set is counted once in EVERY ceiling it could belong "
                             "to, so the three are ALTERNATIVE worst cases over one set, not "
                             "simultaneous ones. Each of the k_ns never-started exclusions sits "
                             "in all three ceiling numerators (its recorded state, plus both "
                             "states it could flow into) and so contributes 2 to the excess; each "
                             "of the k_sl started-and-left exclusions sits in two (its recorded "
                             "state and Continued) and contributes 1. Excess = 2*k_ns + k_sl "
                             f"= {2 * k_ns + k_sl} pairs.",
            },

            "joint_corner_check": {
                "never_started_floor_with_started_and_left_ceiling": {
                    "resolution": f"all {k_ns} never-started nulls started and left; all {k_sl} "
                                  f"started-and-left exclusions are true exits",
                    "never_started_pct": round(pct(ns_lo, N), 6),
                    "started_and_left_pct": round(pct(sl_hi, N), 6),
                    "continued_pct": round(pct(n_co, N), 6),
                    "sums_to_100": (ns_lo + sl_hi + n_co) == N,
                },
                "never_started_ceiling_with_started_and_left_floor": {
                    "resolution": f"all {k_ns} never-started nulls are true declines; all {k_sl} "
                                  f"started-and-left exclusions in truth continued",
                    "never_started_pct": round(pct(ns_hi, N), 6),
                    "started_and_left_pct": round(pct(sl_lo, N), 6),
                    "continued_pct": round(pct(n_co + k_sl, N), 6),
                    "sums_to_100": (ns_hi + sl_lo + n_co + k_sl) == N,
                },
                "continued_ceiling_corner": {
                    "resolution": f"all {k} exclusions in truth continued",
                    "never_started_pct": round(pct(ns_lo, N), 6),
                    "started_and_left_pct": round(pct(sl_lo, N), 6),
                    "continued_pct": round(pct(co_hi, N), 6),
                    "sums_to_100": (ns_lo + sl_lo + co_hi) == N,
                },
                "reading": "each corner is an attainable resolution of the same population, so "
                           "each bound is tight; no two ceilings are attainable together",
            },

            "PUBLISHED_SHARES_post_liveness_DIFFERENT_POPULATION": {
                "note": "0052 SS7. These are the shares Step 8 hands Step 9, on the POST-LIVENESS "
                        "denominator. They are NOT bound endpoints and the two populations differ "
                        "by construction.",
                "denominator": N - k,
                "never_started_pct": round(pct(n_ns - k_ns, N - k), 6),
                "continued_pct": round(pct(n_co, N - k), 6),
                "started_and_left_pct": round(pct(n_sl - k_sl, N - k), 6),
                "containment_never_started": (pct(ns_lo, N) <= pct(n_ns - k_ns, N - k)
                                              <= pct(ns_hi, N)),
                "containment_started_and_left": (pct(sl_lo, N) <= pct(n_sl - k_sl, N - k)
                                                 <= pct(sl_hi, N)),
                "containment_continued": (pct(co_lo, N) <= pct(n_co, N - k) <= pct(co_hi, N)),
            },
        }
        out["by_population"][nm] = rec

    # explicit confirm/refute against 0052 SS1's expectation for the never-started bound
    a = out["by_population"]["APPLY"]
    out["CONFIRM_OR_REFUTE"] = {
        "0052_SS1_APPLY_exclusions_expected_793": {
            "expected": 793, "measured": a["exclusions"]["total"],
            "verdict": "CONFIRMED" if a["exclusions"]["total"] == 793 else "REFUTED"},
        "0052_SS1_APPLY_started_and_left_component_expected_189": {
            "expected": 189, "measured": a["exclusions"]["started_and_left_component"],
            "verdict": ("CONFIRMED" if a["exclusions"]["started_and_left_component"] == 189
                        else "REFUTED")},
        "0052_SS1_never_started_bound_expected_unchanged": {
            "expected": [16.6633, 16.9704],
            "measured": [round(a["bound_never_started"]["floor_pct"], 4),
                         round(a["bound_never_started"]["ceiling_pct"], 4)],
            "verdict": ("CONFIRMED"
                        if [round(a["bound_never_started"]["floor_pct"], 4),
                            round(a["bound_never_started"]["ceiling_pct"], 4)]
                        == [16.6633, 16.9704] else "REFUTED")},
        "0052_SS1_DERIV_unmeasured": {
            "now_measured_total": out["by_population"]["DERIV"]["exclusions"]["total"],
            "never_started_component": out["by_population"]["DERIV"]["exclusions"][
                "never_started_component"],
            "started_and_left_component": out["by_population"]["DERIV"]["exclusions"][
                "started_and_left_component"]},
        "0052_SS4_floor_moves_to_9.6373": {
            "expected": 9.6373,
            "measured": round(a["bound_started_and_left"]["floor_pct"], 4),
            "measured_6dp": a["bound_started_and_left"]["floor_pct"],
            "numerator_expected": 18952,
            "numerator_measured": a["bound_started_and_left"]["floor_numerator"],
            "verdict": ("CONFIRMED on the numerator (18,952) and to 3 dp (9.637%); 0052 SS4's "
                        "FOURTH digit is a rounding defect -- 18,952 / 196,654 = 9.637231%, which "
                        "rounds to 9.6372%, not 9.6373%. Consequently the gap 0052 SS4 states "
                        "against the published 9.6830% is 0.0458 pp, not 0.0457 pp. Cosmetic; "
                        "recorded because the entry states it to 4 dp."
                        if a["bound_started_and_left"]["floor_numerator"] == 18952
                        else "REFUTED"),
            "reading": "0052 SS4 identified 9.6373% as the floor ALT-BROAD's bound FAILED to "
                       "cover. Under ALT-MATCHED the 90 are excluded, so 9.6373% is the floor "
                       "itself and the non-covering endpoint is repaired rather than widened."},
        "0052_SS2_ALT_BROAD_continued_ceiling_73.6537": {
            "recomputed_under_ALT_BROAD": round(pct(144140 + 703, 196654), 4),
            "under_ALT_MATCHED": a["bound_continued"]["ceiling_pct"],
            "reading": "0052 SS2 restored 73.6537% as the ALT-BROAD Continued ceiling on 196,654. "
                       "Reproduced. Under the adopted rule it moves, because the exclusion set is "
                       "larger."},
    }

    with open(os.path.join(OUT, "bounds.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
