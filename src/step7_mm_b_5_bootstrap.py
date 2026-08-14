"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 5: BOOTSTRAP.

THE DESIGN IS STATED IN FULL, because 0052 Sec 6 records that the two arms'
bootstraps were not diffable last time (A: B = 4,000, seed 20260813, on the
MOVEMENTS; B: B = 2,000, seed 20260814, on the LEVELS) and the spec fixes
neither.

  cluster unit    : ACCOUNT (user), because liveness evidence is account-wide.
                    A pair is not an independent unit.
  resampling      : n_accounts drawn WITH REPLACEMENT, i.e. a multinomial over
                    the account index with uniform probabilities. All of an
                    account's pairs travel together.
  replicates B    : 4,000
  seed            : 20260815 (numpy default_rng)
  interval        : percentile, 2.5 / 97.5
  what is resampled: the rule is RE-APPLIED inside every replicate, so the
                    exclusion count is itself random rather than held fixed.
  reported        : BOTH the LEVELS (the three shares, filtered and unfiltered)
                    AND the MOVEMENTS (filtered minus unfiltered, paired within
                    replicate). Reporting both makes the arm diffable against
                    either design the other arm may have chosen.

Implementation note: every quantity is a count of rows in a category and the
rule is row-local, so a replicate is an exactly equivalent weighted sum of
per-account category counts. No row-level resampling is needed and none is
approximated.

ZERO network calls. Out: processed/step7/mm_b/bootstrap.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "mm_b"
W, H, DAY = 108, 91, 86400.0
B, SEED = 4_000, 20260815
LO, HI = 2.5, 97.5


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    in4 = pz["in_line4"]
    uidx_all = pz["user_idx"]

    res: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": 5,
        "api_calls": 0, "adopts": "nothing", "rule_name": "ALT-MATCHED",
        "design": {
            "cluster_unit": "account (user)",
            "why": "liveness evidence is account-wide; a pair is not an independent unit",
            "resampling": "accounts drawn WITH REPLACEMENT (multinomial over the account index)",
            "replicates_B": B, "seed": SEED, "rng": "numpy default_rng",
            "interval": "percentile, 2.5 / 97.5",
            "rule_re_applied_inside_each_replicate": True,
            "reported": "BOTH levels and movements; movements paired within replicate",
            "equivalence_note": ("every reported quantity is a count of rows in a category and "
                                 "the rule is row-local, so a replicate is exactly a weighted sum "
                                 "of per-account category counts"),
        },
        "by_population": {},
    }

    for pop in ("DERIV", "APPLY"):
        d10 = pz[f"d10_W{W}"]
        base = (d10 & in4) if pop == "DERIV" else d10
        n = int(base.sum())
        ns = ~oz[f"started_W{W}"][base]
        cont = oz[f"cont_W{W}"][base].astype(bool)
        sal = oz[f"sal_W{W}"][base].astype(bool)
        sil1, sil2 = pz[f"no_after_tau1_W{W}"][base], pz[f"no_after_tau2_W{W}"][base]
        ex_ns_m, ex_sl_m = ns & sil1, sal & sil2
        u = uidx_all[base]
        acct, inv = np.unique(u, return_inverse=True)
        na = len(acct)

        cols = np.stack([
            np.bincount(inv, minlength=na),                          # 0 n
            np.bincount(inv, weights=ns, minlength=na),              # 1 ns_tot
            np.bincount(inv, weights=cont, minlength=na),            # 2 c_tot
            np.bincount(inv, weights=sal, minlength=na),             # 3 sl_tot
            np.bincount(inv, weights=ex_ns_m, minlength=na),         # 4 ex_ns
            np.bincount(inv, weights=ex_sl_m, minlength=na),         # 5 ex_sl
        ], axis=1).astype(np.float64)
        assert cols[:, 0].sum() == n
        assert abs(cols[:, 1].sum() + cols[:, 2].sum() + cols[:, 3].sum() - n) < 1e-6

        rng = np.random.default_rng(SEED)
        wts = rng.multinomial(na, np.full(na, 1.0 / na), size=B).astype(np.float64)
        agg = wts @ cols                                             # (B, 6)
        nb, nsb, cb, slb, exn, exs = (agg[:, i] for i in range(6))
        exb = exn + exs
        nlive = nb - exb

        unf = np.stack([100 * nsb / nb, 100 * cb / nb, 100 * slb / nb], axis=1)
        flt = np.stack([100 * (nsb - exn) / nlive, 100 * cb / nlive,
                        100 * (slb - exs) / nlive], axis=1)
        mov = flt - unf

        def ci(a):
            return [float(np.percentile(a, LO)), float(np.percentile(a, HI))]

        res["by_population"][pop] = {
            "n_position5": n, "accounts": int(na),
            "levels_filtered_pct": {
                "never_started": ci(flt[:, 0]), "continued": ci(flt[:, 1]),
                "started_and_left": ci(flt[:, 2])},
            "levels_unfiltered_pct": {
                "never_started": ci(unf[:, 0]), "continued": ci(unf[:, 1]),
                "started_and_left": ci(unf[:, 2])},
            "movements_pp_filtered_minus_unfiltered": {
                "never_started": ci(mov[:, 0]), "continued": ci(mov[:, 1]),
                "started_and_left": ci(mov[:, 2]),
                "never_started_sign_stable": bool((mov[:, 0] > 0).all() or (mov[:, 0] < 0).all()),
                "started_and_left_sign_stable": bool((mov[:, 2] > 0).all() or (mov[:, 2] < 0).all()),
                "continued_sign_stable": bool((mov[:, 1] > 0).all() or (mov[:, 1] < 0).all()),
            },
            "exclusion_count": {"ci": ci(exb), "never_started_component_ci": ci(exn),
                                "started_and_left_component_ci": ci(exs)},
            "sampling_widths_pp": {
                "never_started": float(np.percentile(flt[:, 0], HI) - np.percentile(flt[:, 0], LO)),
                "continued": float(np.percentile(flt[:, 1], HI) - np.percentile(flt[:, 1], LO)),
                "started_and_left": float(np.percentile(flt[:, 2], HI) - np.percentile(flt[:, 2], LO)),
            },
        }
        print(f"{pop}: {na} accounts, B={B}  ({time.time() - t:.1f}s)", flush=True)

    # ---- bound width against sampling width, on the ADOPTED bounds (0052 Sec 6) ----
    rule = json.load(open(OUT / "rule.json"))
    ratios = {}
    for pop in ("DERIV", "APPLY"):
        b = rule["by_population"][pop][str(W)]["bounds"]
        sw = res["by_population"][pop]["sampling_widths_pp"]
        ratios[pop] = {
            "never_started": {"bound_width_pp": b["never_started"]["width_pp"],
                              "sampling_width_pp": sw["never_started"],
                              "ratio": (b["never_started"]["width_pp"] / sw["never_started"])},
            "started_and_left": {"bound_width_pp": b["started_and_left"]["width_pp"],
                                 "sampling_width_pp": sw["started_and_left"],
                                 "ratio": (b["started_and_left"]["width_pp"] / sw["started_and_left"])},
            "continued": {"bound_width_pp": b["continued"]["width_pp"],
                          "sampling_width_pp": sw["continued"],
                          "ratio": (b["continued"]["width_pp"] / sw["continued"])},
        }
    res["bound_width_over_sampling_width"] = ratios
    res["ratio_note"] = (
        "computed on the ADOPTED bounds, never on the labelled conditional sub-interval. "
        "0052 Sec 6 records that arm B previously published this ratio on the sub-interval, "
        "understating the systematic range against sampling error by 7.5x.")

    res["elapsed_s"] = time.time() - t
    (OUT / "bootstrap.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["by_population"], indent=2))
    print(json.dumps(ratios, indent=2))


if __name__ == "__main__":
    main()
