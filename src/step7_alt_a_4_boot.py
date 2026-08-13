"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 4 of 4 — the yardstick.

Same account-clustered bootstrap as the gate-closing sensitivity run (B = 4,000, seed
20260813, resample the 2,402 accounts with replacement and take all their pairs), so the
numbers here are comparable with processed/step7/sens_a/bootstrap.json line for line.

Three questions:
  1. What is the clustered interval on each share under ALT and under PF-LIMIT?
  2. Is the PF-LIMIT-to-ALT delta distinguishable from zero, computed PAIRED inside each
     replicate? The two settings are nested subsets of the same pairs.
  3. What does the Step 9 liveness bound's CEILING look like under each rule, and how does its
     width compare with the sampling width of the share it is a bound on?

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/alt_a")

B = 4000
SEED = 20260813
STATES = ["never_started", "continued", "started_and_left"]


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    ex = {"PF_LIMIT_approved": m["ex_pf"], "ALT_proposed": m["ex_alt"],
          "threshold_1293d_deleted": m["ex_thr"],
          "no_liveness_filter": np.zeros(never.size, bool)}

    acc, ainv = np.unique(user, return_inverse=True)
    na = acc.size

    # per-account 4-vector: (never, continued, left, excluded) under each setting
    agg = {}
    for k, e in ex.items():
        live = ~e
        agg[k] = np.stack([
            np.bincount(ainv[never & live], minlength=na),
            np.bincount(ainv[cont & live], minlength=na),
            np.bincount(ainv[left & live], minlength=na),
            np.bincount(ainv[e], minlength=na),
        ], axis=1).astype(np.float64)

    def point_shares(v):
        tot = v[:3].sum()
        return 100.0 * v[:3] / tot

    def point_ceiling(v):
        """Step 9 bound: every excluded pair returned AND counted a decliner."""
        return 100.0 * (v[0] + v[3]) / (v[:3].sum() + v[3])

    keys = list(agg.keys())
    pt = {k: point_shares(agg[k].sum(axis=0)) for k in keys}
    pc = {k: point_ceiling(agg[k].sum(axis=0)) for k in keys}

    rng = np.random.default_rng(SEED)
    reps = {k: np.empty((B, 3)) for k in keys}
    repc = {k: np.empty(B) for k in keys}
    for b in range(B):
        idx = rng.integers(0, na, size=na)
        cnt = np.bincount(idx, minlength=na).astype(np.float64)
        for k in keys:
            tot = cnt @ agg[k]
            reps[k][b] = 100.0 * tot[:3] / tot[:3].sum()
            repc[k][b] = 100.0 * (tot[0] + tot[3]) / (tot[:3].sum() + tot[3])

    ci = {}
    for k in keys:
        ci[k] = {}
        for j, s in enumerate(STATES):
            lo, hi = np.percentile(reps[k][:, j], [2.5, 97.5])
            ci[k][s] = {"point_pct": round(float(pt[k][j]), 4),
                        "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                        "ci_width_pp": round(float(hi - lo), 4)}
        lo, hi = np.percentile(repc[k], [2.5, 97.5])
        ci[k]["step9_bound_ceiling_never_started"] = {
            "point_pct": round(float(pc[k]), 4),
            "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
            "bound_width_pp_point": round(float(pc[k] - pt[k][0]), 4)}

    def paired(a, b):
        dd = reps[b] - reps[a]
        obs = pt[b] - pt[a]
        out = {}
        for j, s in enumerate(STATES):
            lo, hi = np.percentile(dd[:, j], [2.5, 97.5])
            out[s] = {"observed_delta_pp": round(float(obs[j]), 4),
                      "paired_clustered_95_ci_pp": [round(float(lo), 4), round(float(hi), 4)],
                      "ci_excludes_zero": bool(lo > 0 or hi < 0)}
        return out

    deltas = {
        "PF_LIMIT_to_ALT": paired("PF_LIMIT_approved", "ALT_proposed"),
        "no_filter_to_PF_LIMIT": paired("no_liveness_filter", "PF_LIMIT_approved"),
        "no_filter_to_ALT": paired("no_liveness_filter", "ALT_proposed"),
    }

    # the bound's inflation set against the sampling width of the share it bounds
    w_never = ci["PF_LIMIT_approved"]["never_started"]["ci_width_pp"]
    ratio = {k: {"bound_inflation_pp": round(float(pc[k] - pt[k][0]), 4),
                 "clustered_ci_width_of_never_started_pp": w_never,
                 "inflation_as_multiple_of_the_sampling_width": (
                     round(float((pc[k] - pt[k][0]) / w_never), 4) if w_never else None)}
             for k in keys}

    out = {
        "step": 7, "instance": "alt_a", "stage": 4, "api_calls": 0,
        "what": "Account-clustered intervals for the approved PF-LIMIT and the proposed ALT, "
                "and for the Step 9 liveness bound under each. EVALUATION ONLY.",
        "bootstrap": {"B": B, "seed": SEED, "unit": "account", "n_accounts": int(na),
                      "note": "identical design and seed to "
                              "processed/step7/sens_a/bootstrap.json, so the rows are "
                              "comparable with the gate-closing run"},
        "shares_with_clustered_intervals": ci,
        "paired_clustered_deltas": deltas,
        "step9_bound_inflation_against_sampling_width": ratio,
    }
    with open(os.path.join(OUT, "bootstrap.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "bootstrap_replicates.npz"),
                        **{f"shares_{k}": v for k, v in reps.items()},
                        **{f"ceiling_{k}": v for k, v in repc.items()})
    print(json.dumps({"ci": ci, "deltas": deltas, "ratio": ratio}, indent=2))


if __name__ == "__main__":
    main()
