"""Step 7 ALTERNATIVE-RULE EVALUATION (instance b, namespace alt_b) -- stage 3.

Four candidate liveness rules, measured on two populations at every W arm.
NOTHING IS ADOPTED.

  NONE       no liveness filter at all.
  PF_LIMIT   NOT LIVE iff the account shows no insertion instant after tau1.
             The rule approved at decisions/0042.
  ALT        NOT LIVE iff (no insertion instant after tau1) AND |A| = 0.
             Red Team's proposal. |A| is read at tau1, matching the Never
             started condition of step1 Sec 7 -- NOT at tau2 on A_H.
  ALT_BROAD  NOT LIVE iff (no insertion instant after tau1) AND NOT Continued.
             NOT proposed by anyone; added by this instance because it is the
             rule Red Team's own stated principle selects. Continued is the
             only state established by positive evidence alone; Started-and-left
             is positive on entry and INFERRED FROM ABSENCE on exit.

The Step 9 bound, for each rule:
  floor   = never-started share on the live population (the reported figure)
  ceiling = (NS_live + n_excluded) / (n_live + n_excluded)
            i.e. every excluded pair returned to the denominator AND scored a
            decliner. This is the operation task-sheet Step 9 specifies.

ZERO network calls. Reads only.

Out: processed/step7/alt_b/rules.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
RULES = ["NONE", "PF_LIMIT", "ALT", "ALT_BROAD"]


def block(ns, cont, sal, notlive, uidx) -> dict:
    live = ~notlive
    d = int(live.sum())
    ex = int(notlive.sum())
    nsl, cl, sl = int((ns & live).sum()), int((cont & live).sum()), int((sal & live).sum())
    assert nsl + cl + sl == d
    ns_tot = int(ns.sum())
    n_tot = len(ns)
    floor = 100.0 * nsl / d
    ceiling = 100.0 * (nsl + ex) / (d + ex)
    return {
        "excluded_pairs": ex,
        "excluded_share_of_population_pct": 100.0 * ex / n_tot,
        "accounts_supplying_exclusions": int(len(np.unique(uidx[notlive]))) if ex else 0,
        "excluded_composition": {
            "never_started": int((notlive & ns).sum()),
            "continued": int((notlive & cont).sum()),
            "started_and_left": int((notlive & sal).sum()),
        },
        "excluded_with_positive_S2_evidence_in_window": int((notlive & ~ns).sum()),
        "live_pairs": d,
        "never_started": nsl, "continued": cl, "started_and_left": sl,
        "never_started_pct": floor,
        "continued_pct": 100.0 * cl / d,
        "started_and_left_pct": 100.0 * sl / d,
        "step9_bound": {
            "floor_pct": floor,
            "ceiling_pct": ceiling,
            "width_pp": ceiling - floor,
            "ceiling_minus_unfiltered_pp": ceiling - 100.0 * ns_tot / n_tot,
        },
    }


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    uidx_all = pz["user_idx"]
    in_line4_all = pz["in_line4"]

    res: dict = {
        "instance": "data-scientist-b", "namespace": "alt_b", "stage": 3,
        "api_calls": 0, "adopts": "nothing",
        "rule_definitions": {
            "NONE": "no liveness filter",
            "PF_LIMIT": "not live iff no insertion instant after tau1 (decisions/0042)",
            "ALT": "not live iff (no insertion instant after tau1) AND |A| = 0 at tau1",
            "ALT_BROAD": "not live iff (no insertion instant after tau1) AND NOT Continued",
        },
        "populations": {
            "DERIV": "Step 5 line 4 (152,126) less D10 -- the population decisions/0042 "
                     "published 751 on. Requires has_s2 by construction.",
            "APPLY": "Step 5 line 1 (201,900) less D10 -- decisions/0041 Sec 3 / 0042 Sec 5 "
                     "name this as Step 8's population; 196,654 at W = 108.",
        },
        "by_population": {},
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
            ns = ~started
            noaft = pz[f"no_after_W{W}"][base]
            n = int(base.sum())
            assert int(ns.sum() + cont.sum() + sal.sum()) == n

            masks = {
                "NONE": np.zeros(n, dtype=bool),
                "PF_LIMIT": noaft,
                "ALT": noaft & ns,
                "ALT_BROAD": noaft & ~cont,
            }
            # nesting: ALT subset ALT_BROAD subset PF_LIMIT
            assert (masks["ALT"] <= masks["ALT_BROAD"]).all()
            assert (masks["ALT_BROAD"] <= masks["PF_LIMIT"]).all()

            arm = {
                "W": W, "n": n,
                "accounts": int(len(np.unique(uidx))),
                "unfiltered": {
                    "never_started": int(ns.sum()), "continued": int(cont.sum()),
                    "started_and_left": int(sal.sum()),
                    "never_started_pct": 100.0 * ns.sum() / n,
                    "continued_pct": 100.0 * cont.sum() / n,
                    "started_and_left_pct": 100.0 * sal.sum() / n},
                "rules": {r: block(ns, cont, sal, masks[r], uidx) for r in RULES},
            }
            for r in RULES:
                b = arm["rules"][r]
                u = arm["unfiltered"]
                b["delta_vs_no_filter_pp"] = {
                    "never_started": b["never_started_pct"] - u["never_started_pct"],
                    "continued": b["continued_pct"] - u["continued_pct"],
                    "started_and_left": b["started_and_left_pct"] - u["started_and_left_pct"],
                }
            per_arm[str(W)] = arm
        res["by_population"][popname] = per_arm

    res["elapsed_s"] = time.time() - t
    (OUT / "rules.json").write_text(json.dumps(res, indent=2))

    for popname in ("DERIV", "APPLY"):
        a = res["by_population"][popname]["108"]
        print(f"\n=== {popname}  W=108  n={a['n']:,}  "
              f"unfiltered NS {a['unfiltered']['never_started_pct']:.4f}%")
        print(f"{'rule':<11}{'excl':>7}{'exNS':>7}{'exC':>7}{'exSL':>7}"
              f"{'NS%':>10}{'dNS pp':>10}{'ceil%':>10}")
        for r in RULES:
            b = a["rules"][r]
            c = b["excluded_composition"]
            print(f"{r:<11}{b['excluded_pairs']:>7,}{c['never_started']:>7,}"
                  f"{c['continued']:>7,}{c['started_and_left']:>7,}"
                  f"{b['never_started_pct']:>10.4f}"
                  f"{b['delta_vs_no_filter_pp']['never_started']:>+10.4f}"
                  f"{b['step9_bound']['ceiling_pct']:>10.4f}")
    print(f"\n({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
