"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 3.

The adopted rule, measured. NOTHING IS ADOPTED HERE.

    NOT LIVE iff (no insertion instant after tau1) AND (|A| = 0 at tau1)

Measured on BOTH populations at EVERY W arm, against no filter at all. Every
figure carries its population (decisions/0046 Sec 0).

Also tested rather than assumed, because 0046 asserts them:
  C1  DERIV exclusions are 0 at every arm, and the zero is forced by line 4's
      has_s2 requirement.
  C2  APPLY exclusions are 604 at W = 108 and are "exactly the pairs with no S2
      record anywhere". Both readings of "exactly" are tested: subset, and set
      equality against {no S2 record anywhere} INTERSECT D10.
  C3  The exclusion set is a subset of Never started, hence the Step 9 ceiling
      equals the unfiltered never-started share AS AN IDENTITY. Tested on the
      integers, not on the percentages.
  C4  ALT = PF_LIMIT INTERSECT {|A| = 0}, and on APPLY at W = 108 the 751 pairs
      PF_LIMIT deletes but ALT does not are the DERIV 751, of which 652
      continued and 99 left.

ZERO network calls. Reads only.

Out: processed/step7/alt2_b/rule.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt2_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    uidx_all = pz["user_idx"]
    in_line4_all = pz["in_line4"]
    has_s2_step5 = pz["has_s2_evidence"]          # Step 5 field s2_ev_n > 0
    any_rec = oz["has_any_s2_record_anywhere"]    # recomputed from the sweep
    in_e2_rec = oz["has_any_in_E2_s2_record"]
    assert np.array_equal(has_s2_step5, any_rec), \
        "Step 5's has_s2 and the recomputed any-S2-record flag disagree"

    res: dict = {
        "instance": "data-scientist-b", "namespace": "alt2_b", "stage": 3,
        "api_calls": 0, "adopts": "nothing",
        "rule": "NOT LIVE iff (no insertion instant strictly after tau1) AND (|A| = 0 at tau1)",
        "rule_source": "decisions/0046 Sec 1; task-sheet.md Step 7",
        "step5_has_s2_equals_recomputed_any_s2_record": True,
        "populations": {
            "DERIV": "Step 5 line 4 (152,126) less D10 -- 147,370 at W = 108. Requires S2 evidence.",
            "APPLY": "Step 5 line 1 (201,900) less D10 -- 196,654 at W = 108. Step 8 position 6.",
        },
        "by_population": {},
        "claims_tested": {},
    }

    for popname in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            base = d10 & in_line4_all if popname == "DERIV" else d10
            uidx = uidx_all[base]
            started = oz[f"started_W{W}"][base]
            cont = oz[f"cont_W{W}"][base]
            sal = oz[f"sal_W{W}"][base]
            ns = ~started                                  # conjunct (b)
            noaft = pz[f"no_after_W{W}"][base]             # conjunct (a)
            n = int(base.sum())
            assert int(ns.sum() + cont.sum() + sal.sum()) == n

            notlive = noaft & ns
            live = ~notlive
            ex = int(notlive.sum())
            nlive = int(live.sum())
            nsl = int((ns & live).sum())
            cl = int((cont & live).sum())
            sl = int((sal & live).sum())
            assert nsl + cl + sl == nlive
            ns_tot, c_tot, s_tot = int(ns.sum()), int(cont.sum()), int(sal.sum())

            # --- C3, on the integers: exclusions are a subset of never-started
            assert (notlive <= ns).all()
            assert nsl + ex == ns_tot and nlive + ex == n
            floor = 100.0 * nsl / nlive
            ceiling = 100.0 * (nsl + ex) / (nlive + ex)
            unfiltered_ns_pct = 100.0 * ns_tot / n

            per_arm[str(W)] = {
                "W": W, "population": popname, "n_before_liveness": n,
                "accounts_before_liveness": int(len(np.unique(uidx))),
                "excluded_pairs": ex,
                "excluded_share_of_population_pct": 100.0 * ex / n,
                "accounts_supplying_exclusions":
                    int(len(np.unique(uidx[notlive]))) if ex else 0,
                "conjunct_a_alone_would_exclude": int(noaft.sum()),
                "excluded_composition": {
                    "never_started": int((notlive & ns).sum()),
                    "continued": int((notlive & cont).sum()),
                    "started_and_left": int((notlive & sal.astype(bool)).sum()),
                },
                "excluded_with_no_S2_record_anywhere": int((notlive & ~any_rec[base]).sum()),
                "excluded_with_an_S2_record_somewhere": int((notlive & any_rec[base]).sum()),
                "no_filter": {
                    "n": n, "never_started": ns_tot, "continued": c_tot,
                    "started_and_left": s_tot,
                    "never_started_pct": unfiltered_ns_pct,
                    "continued_pct": 100.0 * c_tot / n,
                    "started_and_left_pct": 100.0 * s_tot / n},
                "under_rule": {
                    "n": nlive, "never_started": nsl, "continued": cl,
                    "started_and_left": sl,
                    "never_started_pct": floor,
                    "continued_pct": 100.0 * cl / nlive,
                    "started_and_left_pct": 100.0 * sl / nlive},
                "delta_vs_no_filter_pp": {
                    "never_started": floor - unfiltered_ns_pct,
                    "continued": 100.0 * cl / nlive - 100.0 * c_tot / n,
                    "started_and_left": 100.0 * sl / nlive - 100.0 * s_tot / n},
                "step9_bound": {
                    "floor_pct": floor, "ceiling_pct": ceiling,
                    "width_pp": ceiling - floor,
                    "floor_denominator": nlive, "ceiling_denominator": nlive + ex,
                    "ceiling_equals_unfiltered_share_identity":
                        bool(nsl + ex == ns_tot and nlive + ex == n),
                    "ceiling_minus_unfiltered_pp": ceiling - unfiltered_ns_pct,
                },
            }
        res["by_population"][popname] = per_arm

    # ---------------- claims ----------------
    c: dict = {}

    # C1 -- DERIV zero at every arm, and why it is forced
    deriv_zero = {W: res["by_population"]["DERIV"][str(W)]["excluded_pairs"] for W in W_ARMS}
    c["C1_DERIV_exclusions_per_arm"] = deriv_zero
    c["C1_DERIV_zero_at_every_arm"] = all(v == 0 for v in deriv_zero.values())
    # the mechanism: on DERIV, does |A| = 0 ever coincide with no-insertion-after?
    W = 108
    d10 = pz[f"d10_W{W}"]
    dbase = d10 & in_line4_all
    ns_d = ~oz[f"started_W{W}"][dbase]
    noaft_d = pz[f"no_after_W{W}"][dbase]
    c["C1_mechanism_at_W108_DERIV"] = {
        "n": int(dbase.sum()),
        "pairs_with_A_empty": int(ns_d.sum()),
        "pairs_with_no_insertion_after_tau1": int(noaft_d.sum()),
        "intersection": int((ns_d & noaft_d).sum()),
        "pairs_with_no_S2_record_anywhere": int((~any_rec[dbase]).sum()),
        "reading": ("the DERIV zero is NOT forced by |A| = 0 being empty -- 9,145 line-4 pairs "
                    "are never-started -- it is that none of them coincides with an account "
                    "silent after tau1"),
    }

    # C2 -- APPLY 604 and the two readings of "exactly"
    abase = d10
    ns_a = ~oz[f"started_W{W}"][abase]
    noaft_a = pz[f"no_after_W{W}"][abase]
    notlive_a = ns_a & noaft_a
    nores_a = ~any_rec[abase]
    c["C2_APPLY_at_W108"] = {
        "excluded": int(notlive_a.sum()),
        "subset_reading_all_excluded_have_no_S2_record_anywhere":
            bool((notlive_a <= nores_a).all()),
        "excluded_with_an_S2_record_somewhere": int((notlive_a & ~nores_a).sum()),
        "set_equality_reading_excluded_equals_no_S2_record_anywhere_on_APPLY":
            bool(np.array_equal(notlive_a, nores_a)),
        "pairs_on_APPLY_with_no_S2_record_anywhere": int(nores_a.sum()),
        "of_those_also_silent_after_tau1": int((nores_a & noaft_a).sum()),
        "of_those_with_an_insertion_after_tau1_hence_LIVE": int((nores_a & ~noaft_a).sum()),
        "excluded_with_no_in_E2_S2_record": int((notlive_a & ~in_e2_rec[abase]).sum()),
    }
    c["C2_APPLY_exclusions_per_arm"] = {
        W_: res["by_population"]["APPLY"][str(W_)]["excluded_pairs"] for W_ in W_ARMS}

    # C3 -- identity, stated on the integers at W = 108
    a108 = res["by_population"]["APPLY"]["108"]
    c["C3_identity_APPLY_W108"] = {
        "excluded_all_never_started": a108["excluded_composition"]["continued"] == 0
                                      and a108["excluded_composition"]["started_and_left"] == 0,
        "floor_pct": a108["step9_bound"]["floor_pct"],
        "ceiling_pct": a108["step9_bound"]["ceiling_pct"],
        "unfiltered_never_started_pct": a108["no_filter"]["never_started_pct"],
        "ceiling_equals_unfiltered_exactly":
            a108["step9_bound"]["ceiling_pct"] == a108["no_filter"]["never_started_pct"],
        "single_denominator": a108["step9_bound"]["ceiling_denominator"],
        "width_pp": a108["step9_bound"]["width_pp"],
    }

    # C4 -- ALT vs PF_LIMIT, and the composition of the 751 PF_LIMIT deletes extra
    pf_a = noaft_a                      # PF_LIMIT on APPLY at W = 108
    extra = pf_a & ~notlive_a           # deleted by PF_LIMIT, kept by the adopted rule
    cont_a = oz[f"cont_W{W}"][abase]
    sal_a = oz[f"sal_W{W}"][abase]
    in4_a = in_line4_all[abase]
    c["C4_ALT_vs_PF_LIMIT_APPLY_W108"] = {
        "PF_LIMIT_excluded": int(pf_a.sum()),
        "ALT_excluded": int(notlive_a.sum()),
        "difference": int(extra.sum()),
        "ALT_is_a_subset_of_PF_LIMIT": bool((notlive_a <= pf_a).all()),
        "difference_composition": {
            "continued": int((extra & cont_a).sum()),
            "started_and_left": int((extra & sal_a).sum()),
            "never_started": int((extra & ns_a).sum()),
        },
        "difference_all_in_line4_DERIV": bool((extra <= in4_a).all()),
        "difference_count_in_line4": int((extra & in4_a).sum()),
        "DERIV_PF_LIMIT_excluded_at_W108":
            int((pz[f"no_after_W{W}"] & d10 & in_line4_all).sum()),
    }
    res["claims_tested"] = c

    res["elapsed_s"] = time.time() - t
    (OUT / "rule.json").write_text(json.dumps(res, indent=2))

    for popname in ("DERIV", "APPLY"):
        a = res["by_population"][popname]["108"]
        print(f"\n=== {popname}  W=108  n={a['n_before_liveness']:,}")
        print(f"  excluded {a['excluded_pairs']:,} from "
              f"{a['accounts_supplying_exclusions']} accounts; composition {a['excluded_composition']}")
        print(f"  no filter : NS {a['no_filter']['never_started_pct']:.4f}%  "
              f"C {a['no_filter']['continued_pct']:.4f}%  "
              f"SL {a['no_filter']['started_and_left_pct']:.4f}%")
        print(f"  under rule: NS {a['under_rule']['never_started_pct']:.4f}%  "
              f"C {a['under_rule']['continued_pct']:.4f}%  "
              f"SL {a['under_rule']['started_and_left_pct']:.4f}%")
        print(f"  bound [{a['step9_bound']['floor_pct']:.4f}, "
              f"{a['step9_bound']['ceiling_pct']:.4f}]  "
              f"identity={a['step9_bound']['ceiling_equals_unfiltered_share_identity']}")
    print("\nclaims:", json.dumps(c, indent=1)[:2000])
    print(f"\n({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
