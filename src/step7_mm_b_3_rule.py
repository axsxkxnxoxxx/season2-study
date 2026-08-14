"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 3: THE RULE.

    NOT LIVE iff EITHER
      (i)  |A| = 0   AND no insertion instant after tau1 ;  OR
      (ii) |A| >= 1  AND NOT Continued AND no insertion instant after tau2 .

Exclusion counts, the three shares, and the THREE bounds, on BOTH populations,
at every W arm, with D10 re-derived at each arm (0047 Sec 5).

ALT-BROAD (both nulls at tau1) is ALSO computed at every arm, LABELLED
SUPERSEDED, solely so the delta the rule change produces can be reported. It is
not offered as a result.

ZERO network calls. Out: processed/step7/mm_b/rule.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "mm_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
W_ADOPTED, H = 108, 91


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    in4 = pz["in_line4"]
    uidx_all = pz["user_idx"]
    any_rec = oz["has_any_s2_record_anywhere"]

    res: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": 3,
        "api_calls": 0, "adopts": "nothing",
        "gate": "Step 7 is a GATE. This artifact is a proposal. Nothing here is adopted.",
        "rule_name": "ALT-MATCHED",
        "rule": ("NOT LIVE iff EITHER (|A| = 0 AND no insertion after tau1) OR "
                 "(|A| >= 1 AND NOT Continued AND no insertion after tau2)"),
        "rule_source": "decisions/0052 Sec 1",
        "supersedes": "ALT-BROAD (0048 Sec 1)",
        "populations": {
            "DERIV": "Step 5 line 4 less D10 = 147,370 at W = 108. Requires S2 evidence.",
            "APPLY": "Step 5 line 1 less D10 = 196,654 at W = 108. Step 8 filters this at position 6.",
        },
        "W_adopted": W_ADOPTED, "H": H, "W_arms": W_ARMS,
        "D10": "RE-DERIVED at each arm (0047 Sec 5). Reading named at every table.",
        "by_population": {},
    }

    for pop in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            base = (d10 & in4) if pop == "DERIV" else d10
            n = int(base.sum())
            started = oz[f"started_W{W}"][base]
            cont = oz[f"cont_W{W}"][base].astype(bool)
            sal = oz[f"sal_W{W}"][base].astype(bool)
            ns = ~started
            sil1 = pz[f"no_after_tau1_W{W}"][base]
            sil2 = pz[f"no_after_tau2_W{W}"][base]
            uidx = uidx_all[base]
            assert int(ns.sum() + cont.sum() + sal.sum()) == n, "states do not partition"

            # -------------------- THE ADOPTED RULE --------------------
            branch_i = ns & sil1                 # never-started null, silence at tau1
            branch_ii = sal & sil2               # started-and-left null, silence at tau2
            notlive = branch_i | branch_ii
            assert not bool((branch_i & branch_ii).any()), "branches must be disjoint"
            live = ~notlive
            ex, ex_ns, ex_sl = int(notlive.sum()), int(branch_i.sum()), int(branch_ii.sum())
            assert int((notlive & cont).sum()) == 0, "a Continued pair was excluded"
            assert ex_ns + ex_sl == ex

            # -------------------- ALT-BROAD, SUPERSEDED, for the delta only ------
            nl_broad = sil1 & ~cont
            ex_b = int(nl_broad.sum())
            ex_b_ns = int((nl_broad & ns).sum())
            ex_b_sl = int((nl_broad & sal).sum())
            # ALT-MATCHED must be a strict superset of ALT-BROAD: sil1 => sil2, and
            # ALT-BROAD's set is (ns & sil1) union (sal & sil1).
            assert bool((nl_broad <= notlive).all()), "ALT-MATCHED must contain ALT-BROAD"

            n_live = int(live.sum())
            ns_live, c_live, sl_live = (int((ns & live).sum()), int((cont & live).sum()),
                                        int((sal & live).sum()))
            ns_tot, c_tot, sl_tot = int(ns.sum()), int(cont.sum()), int(sal.sum())
            assert ns_live + c_live + sl_live == n_live
            assert c_live == c_tot

            # -------------------- BOUNDS, one denominator = n (position-5) --------
            # What is OBSERVED for an excluded pair, which is what fixes the endpoints:
            #   branch (i)  pairs: |A| = 0 is an UNTRUSTED NULL -> true state in {NS, SL, C}
            #   branch (ii) pairs: |A| >= 1 DIRECTLY OBSERVED, exit is the null
            #                      -> true state in {SL, C}; they can never be NS
            ns_floor_num, ns_ceil_num = ns_tot - ex_ns, ns_tot
            sl_floor_num, sl_ceil_num = sl_tot - ex_sl, sl_tot + ex_ns
            c_floor_num, c_ceil_num = c_tot, c_tot + ex
            pc = lambda x: 100.0 * x / n

            # the conditional sub-interval over branch-(ii) exclusions only (labelled, not the bound)
            sl_cond_ceil_num = sl_tot

            ceil_sum = pc(ns_ceil_num) + pc(sl_ceil_num) + pc(c_ceil_num)

            per_arm[str(W)] = {
                "W": W, "population": pop, "D10_reading": "re-derived at this arm",
                "n_before_liveness": n,
                "accounts_before_liveness": int(len(np.unique(uidx))),
                "excluded_pairs": ex,
                "excluded_never_started": ex_ns,
                "excluded_started_and_left": ex_sl,
                "excluded_continued": 0,
                "excluded_share_of_population_pct": pc(ex),
                "accounts_supplying_exclusions": int(len(np.unique(uidx[notlive]))) if ex else 0,
                "accounts_supplying_NS_exclusions":
                    int(len(np.unique(uidx[branch_i]))) if ex_ns else 0,
                "accounts_supplying_SL_exclusions":
                    int(len(np.unique(uidx[branch_ii]))) if ex_sl else 0,
                "selection_path": {
                    "branch_i_never_started_pool": ns_tot,
                    "branch_i_after_silence_at_tau1": ex_ns,
                    "branch_ii_started_and_left_pool": sl_tot,
                    "branch_ii_after_silence_at_tau2": ex_sl,
                    "silence_at_tau1_alone_would_exclude": int(sil1.sum()),
                    "silence_at_tau2_alone_would_exclude": int(sil2.sum()),
                    "not_continued_alone_would_exclude": int((~cont).sum()),
                },
                "excluded_with_no_S2_record_anywhere": int((notlive & ~any_rec[base]).sum()),
                "excluded_with_an_S2_record_somewhere": int((notlive & any_rec[base]).sum()),
                "ALT_BROAD_SUPERSEDED": {
                    "note": "computed only to report the delta the rule change produces",
                    "excluded_pairs": ex_b,
                    "excluded_never_started": ex_b_ns,
                    "excluded_started_and_left": ex_b_sl,
                    "delta_total": ex - ex_b,
                    "delta_never_started": ex_ns - ex_b_ns,
                    "delta_started_and_left": ex_sl - ex_b_sl,
                },
                "no_filter": {
                    "n": n, "never_started": ns_tot, "continued": c_tot,
                    "started_and_left": sl_tot,
                    "never_started_pct": pc(ns_tot), "continued_pct": pc(c_tot),
                    "started_and_left_pct": pc(sl_tot)},
                "under_rule": {
                    "n": n_live, "never_started": ns_live, "continued": c_live,
                    "started_and_left": sl_live,
                    "never_started_pct": 100.0 * ns_live / n_live,
                    "continued_pct": 100.0 * c_live / n_live,
                    "started_and_left_pct": 100.0 * sl_live / n_live},
                "delta_vs_no_filter_pp": {
                    "never_started": 100.0 * ns_live / n_live - pc(ns_tot),
                    "continued": 100.0 * c_live / n_live - pc(c_tot),
                    "started_and_left": 100.0 * sl_live / n_live - pc(sl_tot)},
                "bounds": {
                    "computed_on": "the POSITION-5 population, n = %d" % n,
                    "estimand_population": "the same position-5 population -- no mixed denominators",
                    "published_shares_are_on": "the POST-LIVENESS population, n = %d" % n_live,
                    "never_started": {
                        "floor_pct": pc(ns_floor_num), "ceiling_pct": pc(ns_ceil_num),
                        "width_pp": pc(ns_ceil_num) - pc(ns_floor_num),
                        "floor_numerator": ns_floor_num, "ceiling_numerator": ns_ceil_num,
                        "denominator": n,
                        "ceiling_is_identity_with_unfiltered_share":
                            bool(ns_ceil_num == ns_tot),
                        "spanned_by": "branch-(i) exclusions only",
                    },
                    "started_and_left": {
                        "floor_pct": pc(sl_floor_num), "ceiling_pct": pc(sl_ceil_num),
                        "width_pp": pc(sl_ceil_num) - pc(sl_floor_num),
                        "floor_numerator": sl_floor_num, "ceiling_numerator": sl_ceil_num,
                        "denominator": n,
                        "spanned_by": "ALL exclusions -- branch (i) can in truth be S&L",
                        "conditional_sub_interval_over_branch_ii_only": {
                            "floor_pct": pc(sl_floor_num),
                            "ceiling_pct": pc(sl_cond_ceil_num),
                            "width_pp": pc(sl_cond_ceil_num) - pc(sl_floor_num),
                            "label": ("LABELLED CONDITIONAL. Not the bound: it assumes none of the "
                                      "branch-(i) exclusions is in truth started-and-left."),
                        },
                    },
                    "continued": {
                        "floor_pct": pc(c_floor_num), "ceiling_pct": pc(c_ceil_num),
                        "width_pp": pc(c_ceil_num) - pc(c_floor_num),
                        "floor_numerator": c_floor_num, "ceiling_numerator": c_ceil_num,
                        "denominator": n,
                        "floor_is_identity_with_unfiltered_share": bool(c_floor_num == c_tot),
                        "why_a_ceiling_exists": ("no Continued pair is ever EXCLUDED, but any "
                                                 "EXCLUDED pair may in truth be Continued"),
                    },
                    "three_ceilings": {
                        "never_started_pct": pc(ns_ceil_num),
                        "started_and_left_pct": pc(sl_ceil_num),
                        "continued_pct": pc(c_ceil_num),
                        "sum_pct": ceil_sum,
                        "excess_over_100_pp": ceil_sum - 100.0,
                        "excess_as_count": 2 * ex_ns + ex_sl,
                        "excess_check_pct": pc(2 * ex_ns + ex_sl),
                        "mechanism": ("the same excluded pairs are counted in more than one "
                                      "ceiling. Each branch-(i) pair is compatible with all three "
                                      "states and so appears in all three ceilings; each "
                                      "branch-(ii) pair is compatible with S&L and Continued and "
                                      "appears in two. The three are ALTERNATIVE worst cases over "
                                      "ONE set, never simultaneous ones."),
                    },
                    "containment_of_the_published_point_estimate": {
                        "never_started_point_post_liveness_pct": 100.0 * ns_live / n_live,
                        "never_started_inside_its_own_bound": bool(
                            pc(ns_floor_num) <= 100.0 * ns_live / n_live <= pc(ns_ceil_num)),
                        "started_and_left_point_post_liveness_pct": 100.0 * sl_live / n_live,
                        "started_and_left_inside_its_own_bound": bool(
                            pc(sl_floor_num) <= 100.0 * sl_live / n_live <= pc(sl_ceil_num)),
                        "continued_point_post_liveness_pct": 100.0 * c_live / n_live,
                        "continued_inside_its_own_bound": bool(
                            pc(c_floor_num) <= 100.0 * c_live / n_live <= pc(c_ceil_num)),
                        "note": ("the bounds are on the position-5 population and the published "
                                 "shares are post-liveness -- different populations "
                                 "(0052 Sec 7). Containment is not guaranteed."),
                    },
                },
            }
        res["by_population"][pop] = per_arm

    assert res["by_population"]["APPLY"]["108"]["n_before_liveness"] == 196_654
    assert res["by_population"]["DERIV"]["108"]["n_before_liveness"] == 147_370
    res["populations_asserted_at_W108"] = {"APPLY": 196_654, "DERIV": 147_370}

    a, d = res["by_population"]["APPLY"]["108"], res["by_population"]["DERIV"]["108"]
    res["claims_tested"] = {
        "0052_expects_APPLY_703_to_793": {
            "expected": 793, "measured": a["excluded_pairs"],
            "verdict": "CONFIRMED" if a["excluded_pairs"] == 793 else "REFUTED"},
        "0052_expects_APPLY_SL_component_99_to_189": {
            "expected": 189, "measured": a["excluded_started_and_left"],
            "verdict": "CONFIRMED" if a["excluded_started_and_left"] == 189 else "REFUTED"},
        "0052_says_DERIV_is_unmeasured": {
            "measured_DERIV_total": d["excluded_pairs"],
            "measured_DERIV_never_started": d["excluded_never_started"],
            "measured_DERIV_started_and_left": d["excluded_started_and_left"],
            "measured_DERIV_accounts": d["accounts_supplying_exclusions"],
            "ALT_BROAD_DERIV_total": d["ALT_BROAD_SUPERSEDED"]["excluded_pairs"]},
        "0052_expects_never_started_bound_unchanged": {
            "expected": [16.6633, 16.9704],
            "measured_APPLY": [a["bounds"]["never_started"]["floor_pct"],
                               a["bounds"]["never_started"]["ceiling_pct"]],
            "measured_denominator": a["bounds"]["never_started"]["denominator"]},
        "per_arm_APPLY_excluded": [res["by_population"]["APPLY"][str(W)]["excluded_pairs"]
                                   for W in W_ARMS],
        "per_arm_APPLY_SL_component": [
            res["by_population"]["APPLY"][str(W)]["excluded_started_and_left"] for W in W_ARMS],
        "per_arm_APPLY_NS_component": [
            res["by_population"]["APPLY"][str(W)]["excluded_never_started"] for W in W_ARMS],
        "per_arm_DERIV_excluded": [res["by_population"]["DERIV"][str(W)]["excluded_pairs"]
                                   for W in W_ARMS],
        "per_arm_DERIV_SL_component": [
            res["by_population"]["DERIV"][str(W)]["excluded_started_and_left"] for W in W_ARMS],
        "per_arm_DERIV_NS_component": [
            res["by_population"]["DERIV"][str(W)]["excluded_never_started"] for W in W_ARMS],
        "APPLY_W_coupling_38_to_213": {
            "total": res["by_population"]["APPLY"]["213"]["excluded_pairs"] /
                     res["by_population"]["APPLY"]["38"]["excluded_pairs"],
            "NS_component": res["by_population"]["APPLY"]["213"]["excluded_never_started"] /
                            res["by_population"]["APPLY"]["38"]["excluded_never_started"],
            "SL_component": res["by_population"]["APPLY"]["213"]["excluded_started_and_left"] /
                            res["by_population"]["APPLY"]["38"]["excluded_started_and_left"]},
    }

    res["elapsed_s"] = time.time() - t
    (OUT / "rule.json").write_text(json.dumps(res, indent=2))

    for pop in ("DERIV", "APPLY"):
        x = res["by_population"][pop]["108"]
        b = x["bounds"]
        print(f"\n=== {pop}  W=108  n={x['n_before_liveness']:,}")
        print(f"  excluded {x['excluded_pairs']:,} from {x['accounts_supplying_exclusions']} "
              f"accounts = {x['excluded_never_started']} NS + "
              f"{x['excluded_started_and_left']} SL   "
              f"(ALT-BROAD was {x['ALT_BROAD_SUPERSEDED']['excluded_pairs']})")
        print(f"  no filter : NS {x['no_filter']['never_started_pct']:.4f}  "
              f"C {x['no_filter']['continued_pct']:.4f}  "
              f"SL {x['no_filter']['started_and_left_pct']:.4f}")
        print(f"  under rule: NS {x['under_rule']['never_started_pct']:.4f}  "
              f"C {x['under_rule']['continued_pct']:.4f}  "
              f"SL {x['under_rule']['started_and_left_pct']:.4f}")
        print(f"  NS  [{b['never_started']['floor_pct']:.4f}, {b['never_started']['ceiling_pct']:.4f}]")
        print(f"  S&L [{b['started_and_left']['floor_pct']:.4f}, "
              f"{b['started_and_left']['ceiling_pct']:.4f}]")
        print(f"  C   [{b['continued']['floor_pct']:.4f}, {b['continued']['ceiling_pct']:.4f}]")
        print(f"  ceilings sum {b['three_ceilings']['sum_pct']:.4f}  "
              f"excess {b['three_ceilings']['excess_over_100_pp']:.4f} pp "
              f"= {b['three_ceilings']['excess_as_count']} pairs")
    print(json.dumps(res["claims_tested"], indent=2))


if __name__ == "__main__":
    main()
