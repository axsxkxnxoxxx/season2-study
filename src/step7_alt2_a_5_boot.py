"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 5 of 5.

Account-clustered bootstrap, B = 4,000, seed 20260813 — the same design and seed as the
earlier Step 7 runs, so the rows are comparable line for line. Accounts are resampled with
replacement and all of a resampled account's pairs travel with it, because liveness evidence
is account-wide even though the filter is pair-level.

Reported on BOTH populations, every figure tagged:
  - the three outcome shares under the adopted rule and under no filter at all
  - the PAIRED delta between those two settings, computed inside each replicate
  - the Step 9 liveness bound's floor and ceiling
  - the bound's width against the sampling width of the share it bounds

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/alt2_a")

B = 4000
SEED = 20260813
STATES = ["never_started", "continued", "started_and_left"]


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    user, never, cont, left, ex = m["user"], m["never"], m["cont"], m["left"], m["ex"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    rng = np.random.default_rng(SEED)
    out = {"step": 7, "instance": "alt2_a", "stage": 5, "api_calls": 0,
           "bootstrap": {"B": B, "seed": SEED, "unit": "account",
                         "resample": "accounts with replacement, all their pairs travel"},
           "by_population": {}}

    for nm, pop in pops.items():
        idx = np.flatnonzero(pop)
        u = user[idx]
        acc, ainv = np.unique(u, return_inverse=True)
        na = acc.size
        nev, co, le, e = never[idx], cont[idx], left[idx], ex[idx]

        # per-account counts under each setting: filtered (rule applied) and unfiltered
        live = ~e
        agg_f = np.stack([np.bincount(ainv[nev & live], minlength=na),
                          np.bincount(ainv[co & live], minlength=na),
                          np.bincount(ainv[le & live], minlength=na),
                          np.bincount(ainv[e], minlength=na)], axis=1).astype(np.float64)
        agg_u = np.stack([np.bincount(ainv[nev], minlength=na),
                          np.bincount(ainv[co], minlength=na),
                          np.bincount(ainv[le], minlength=na),
                          np.zeros(na)], axis=1).astype(np.float64)

        def shares(v):
            t = v[:3].sum()
            return 100.0 * v[:3] / t if t else np.full(3, np.nan)

        def ceiling(v):
            return 100.0 * (v[0] + v[3]) / (v[:3].sum() + v[3])

        pt_f, pt_u = shares(agg_f.sum(0)), shares(agg_u.sum(0))
        pc = ceiling(agg_f.sum(0))

        rf = np.empty((B, 3)); ru = np.empty((B, 3)); rc = np.empty(B)
        for b in range(B):
            j = rng.integers(0, na, size=na)
            w = np.bincount(j, minlength=na).astype(np.float64)
            tf, tu = w @ agg_f, w @ agg_u
            rf[b] = shares(tf); ru[b] = shares(tu); rc[b] = ceiling(tf)

        rec = {"population_pairs": int(idx.size), "accounts": int(na), "settings": {}}
        for label, pt, rr in (("ADOPTED_RULE", pt_f, rf), ("no_liveness_filter", pt_u, ru)):
            d = {}
            for k, s in enumerate(STATES):
                lo, hi = np.percentile(rr[:, k], [2.5, 97.5])
                d[s] = {"point_pct": round(float(pt[k]), 4),
                        "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                        "ci_width_pp": round(float(hi - lo), 4)}
            rec["settings"][label] = d

        dd = rf - ru
        rec["paired_delta_rule_minus_no_filter"] = {}
        for k, s in enumerate(STATES):
            lo, hi = np.percentile(dd[:, k], [2.5, 97.5])
            rec["paired_delta_rule_minus_no_filter"][s] = {
                "observed_pp": round(float(pt_f[k] - pt_u[k]), 4),
                "paired_clustered_95_ci_pp": [round(float(lo), 4), round(float(hi), 4)],
                "ci_excludes_zero": bool(lo > 0 or hi < 0)}

        lo, hi = np.percentile(rc, [2.5, 97.5])
        w_never = rec["settings"]["ADOPTED_RULE"]["never_started"]["ci_width_pp"]
        rec["step9_liveness_bound"] = {
            "floor_point_pct": round(float(pt_f[0]), 4),
            "floor_clustered_95_ci_pct":
                rec["settings"]["ADOPTED_RULE"]["never_started"]["clustered_95_ci_pct"],
            "ceiling_point_pct": round(float(pc), 4),
            "ceiling_clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
            "bound_width_pp": round(float(pc - pt_f[0]), 4),
            "clustered_ci_width_of_the_floor_pp": w_never,
            "bound_width_as_share_of_the_sampling_width": (
                round(float((pc - pt_f[0]) / w_never), 4) if w_never else None),
        }
        out["by_population"][nm] = rec
        print(nm, json.dumps(rec["step9_liveness_bound"]))

        np.savez_compressed(os.path.join(OUT, f"bootstrap_replicates_{nm}.npz"),
                            shares_rule=rf, shares_nofilter=ru, ceiling_rule=rc)

    with open(os.path.join(OUT, "bootstrap.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out["by_population"]["APPLY"]["settings"], indent=2))


if __name__ == "__main__":
    main()
