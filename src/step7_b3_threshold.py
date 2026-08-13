"""Step 7 (instance b3) -- stage 3: threshold, realised rates, inertness, W arms.

READ ONLY. ZERO network calls.  Proposes; adopts nothing.

Threshold = ceil( 99th percentile of the BRACKETING-gap distribution )
  - reference distribution: the bracketing gaps themselves (decisions/0037 Sec 1)
  - reference population: the 152,126, waterfall line 4 (decisions/0038 Sec 2)
  - weighting: ONE GAP PER PAIR (decisions/0038 Sec 3)
  - rounded UP (decisions/0025)
  - percentile 99 (decisions/0036 Sec 1 level, 0037/0038 basis)

Exclusion test: a measured bracketing gap of >= threshold days -> NOT LIVE.
The ">=" is what decisions/0025 (a) assumes when it argues for the ceiling.

Out: processed/step7/b3/threshold.json, processed/step7/b3/gap_percentiles.csv
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b3"

W_ADOPTED = 108
W_ARMS = [46, 77, 108, 150, 213]
PCTL = 99.0
SEED = 20260813

GRID = [50, 75, 90, 95, 97.5, 99, 99.5, 99.9]
INERT_GRID = [90, 92.5, 95, 97.5, 99, 99.5, 99.9]


def methods(x, q):
    return {m: float(np.percentile(x, q, method=m))
            for m in ("linear", "lower", "higher", "nearest", "midpoint")}


def arm(gap, state, W, pctl=PCTL):
    n = len(state)
    meas = state == 0
    g = gap[meas]
    raw = float(np.percentile(g, pctl))
    thr = int(math.ceil(raw))
    excl_meas = int((g >= thr).sum())
    none_after = int((state == 1).sum())
    none_before = int((state == 2).sum())
    edge = none_after + none_before
    excl = excl_meas + edge
    return {
        "W_days": W,
        "percentile": pctl,
        "pairs": n,
        "pairs_with_measured_gap": int(meas.sum()),
        "threshold_raw_days": raw,
        "threshold_days_ceiling": thr,
        "threshold_by_numpy_method": methods(g, pctl),
        "excluded_measured_gap": excl_meas,
        "excluded_no_instant_after_tau1": none_after,
        "excluded_no_instant_at_or_before_tau1": none_before,
        "excluded_total": excl,
        "live": n - excl,
        "realised_rate_on_measured_gap_pairs": excl_meas / int(meas.sum()),
        "realised_rate_on_all_pairs": excl / n,
        "share_of_exclusions_from_measured_gap": excl_meas / excl,
        "share_of_exclusions_from_edge_cases": edge / excl,
        "gap_median_days": float(np.median(g)),
        "gap_p75_days": float(np.percentile(g, 75)),
    }


def main() -> None:
    t = time.time()
    rng = np.random.default_rng(SEED)

    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    br = np.load(OUT / "bracket.npz")

    # ---- pooled gap distribution, for the chart and as a cross-check ---------
    pooled = []
    for u in range(len(offsets) - 1):
        seq = tau_all[offsets[u]:offsets[u + 1]]
        if len(seq) > 1:
            pooled.append(np.diff(seq))
    pooled = np.concatenate(pooled) / 86400.0
    pooled_p99 = float(np.percentile(pooled, 99))
    pooled_stats = {
        "n_gaps": int(len(pooled)),
        "weighting": "every gap on every account, unweighted -- NOT the reference distribution",
        "median_days": float(np.median(pooled)),
        "p99_days": pooled_p99,
        "p99_ceiling_days": int(math.ceil(pooled_p99)),
        "share_sub_second": float((pooled < 1 / 86400).mean()),
        "percentiles": {str(q): float(np.percentile(pooled, q)) for q in GRID},
    }
    print(f"pooled done ({time.time()-t:.1f}s)  median {pooled_stats['median_days']:.7f} d, "
          f"p99 {pooled_p99:.4f} d")

    # ---- adopted arm ---------------------------------------------------------
    gap = br[f"gap_days_W{W_ADOPTED}"]
    state = br[f"state_W{W_ADOPTED}"]
    main_arm = arm(gap, state, W_ADOPTED)
    g = gap[state == 0]

    brack_stats = {
        "n_gaps_one_per_pair": int(len(g)),
        "weighting": "ONE GAP PER PAIR (decisions/0038 Sec 3)",
        "min_days": float(g.min()),
        "max_days": float(g.max()),
        "mean_days": float(g.mean()),
        "percentiles": {str(q): float(np.percentile(g, q)) for q in GRID},
    }

    # length bias, the 0037 Sec 1 corroboration, measured on THIS population
    length_bias = {
        "pooled_median_days": pooled_stats["median_days"],
        "bracketing_median_days": float(np.median(g)),
        "bracketing_p75_days": float(np.percentile(g, 75)),
        "share_of_bracketing_gaps_exceeding_pooled_p99_ceiling": float(
            (g >= pooled_stats["p99_ceiling_days"]).mean()),
        "share_of_bracketing_gaps_exceeding_pooled_p99_raw": float((g >= pooled_p99).mean()),
        "note": ("this is what decisions/0037 withdrew: a threshold set on the pooled "
                 "distribution and applied to the bracketing one delivers this rate, not 1%"),
    }

    # ---- weighting sensitivity, reported not adopted -------------------------
    uid = br["user_idx"]
    key = np.stack([uid.astype(np.float64), gap])[:, state == 0]
    uniq = np.unique(key.T, axis=0)
    gu = uniq[:, 1]
    raw_u = float(np.percentile(gu, PCTL))
    weighting_sens = {
        "adopted": "one gap per pair",
        "alternative_one_per_distinct_account_gap": {
            "n": int(len(gu)),
            "threshold_raw_days": raw_u,
            "threshold_days_ceiling": int(math.ceil(raw_u)),
            "realised_rate_on_measured_gap_pairs_if_used": float(
                (g >= math.ceil(raw_u)).mean()),
        },
        "note": "decisions/0038 Sec 3 rules one-per-pair. The alternative is reported, not used.",
    }

    # ---- percentile sweep: the quota property and the inertness --------------
    sweep = []
    for q in INERT_GRID:
        a = arm(gap, state, W_ADOPTED, pctl=q)
        sweep.append({
            "percentile": q,
            "threshold_raw_days": a["threshold_raw_days"],
            "threshold_days_ceiling": a["threshold_days_ceiling"],
            "excluded_measured_gap": a["excluded_measured_gap"],
            "excluded_edge_cases": a["excluded_no_instant_after_tau1"]
                                   + a["excluded_no_instant_at_or_before_tau1"],
            "excluded_total": a["excluded_total"],
            "realised_rate_on_measured_gap_pairs": a["realised_rate_on_measured_gap_pairs"],
            "realised_rate_on_all_pairs": a["realised_rate_on_all_pairs"],
            "share_of_exclusions_from_measured_gap": a["share_of_exclusions_from_measured_gap"],
            "share_of_exclusions_from_edge_cases": a["share_of_exclusions_from_edge_cases"],
        })

    # ---- Step 13 W arms: refit per arm (decisions/0038 Sec 6) ----------------
    arms = [arm(br[f"gap_days_W{W}"], br[f"state_W{W}"], W) for W in W_ARMS]

    # ---- bootstrap on the threshold -----------------------------------------
    B = 1000
    bs = np.percentile(rng.choice(g, size=(B, len(g)), replace=True), PCTL, axis=1)
    boot = {"B": B, "ci95_raw_days": [float(v) for v in np.percentile(bs, [2.5, 97.5])],
            "sd_days": float(bs.std()),
            "ci95_ceiling_days": [int(math.ceil(v))
                                  for v in np.percentile(bs, [2.5, 97.5])]}
    # account-cluster bootstrap: gaps on one account are not independent
    ug = uid[state == 0]
    o = np.argsort(ug, kind="stable")
    ug_s, g_s = ug[o], g[o]
    bnd = np.searchsorted(ug_s, np.unique(ug_s))
    bnd = np.append(bnd, len(ug_s))
    ncl = len(bnd) - 1
    vals = []
    for _ in range(300):
        pick = rng.integers(0, ncl, ncl)
        vals.append(np.percentile(np.concatenate([g_s[bnd[i]:bnd[i + 1]] for i in pick]), PCTL))
    boot["cluster_by_account"] = {
        "B": 300, "n_accounts": int(ncl),
        "ci95_raw_days": [float(v) for v in np.percentile(vals, [2.5, 97.5])],
        "ci95_ceiling_days": [int(math.ceil(v)) for v in np.percentile(vals, [2.5, 97.5])],
    }

    res = {
        "instance": "data-scientist-b / namespace b3",
        "step": 7,
        "status": "PROPOSED -- gate, not adopted. The Human Lead approves.",
        "api_calls": 0,
        "W_adopted": W_ADOPTED,
        "percentile": PCTL,
        "adopted_arm": main_arm,
        "bracketing_gap_distribution": brack_stats,
        "pooled_gap_distribution_CROSS_CHECK_ONLY": pooled_stats,
        "length_bias": length_bias,
        "weighting_sensitivity": weighting_sens,
        "percentile_sweep": sweep,
        "W_arms_refitted": arms,
        "bootstrap": boot,
        "elapsed_s": time.time() - t,
    }
    (OUT / "threshold.json").write_text(json.dumps(res, indent=2))
    print(json.dumps({k: res[k] for k in
                      ("adopted_arm", "length_bias", "percentile_sweep", "W_arms_refitted",
                       "bootstrap", "weighting_sensitivity")}, indent=2))


if __name__ == "__main__":
    main()
