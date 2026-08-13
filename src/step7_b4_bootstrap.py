"""Step 7 rerun (instance b4) -- stage 4: account-clustered bootstrap of the threshold.

READ ONLY. ZERO network calls.

decisions/0040 Sec 6 / Red Team: the previous run used 300 replicates and its
interval endpoints were the 7th and 8th order statistics quoted to the day.
This run uses B >= 1000 and states the count. The i.i.d. pair-level bootstrap
is run alongside, purely to quantify how much it overstates precision.

Usage: python3 src/step7_b4_bootstrap.py <B_adopted> <B_arms>
Out:   processed/step7/b4/bootstrap_W<arm>.json  (one per arm)
"""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b4"
W_ADOPTED = 108
SEED = 20260813


def r7_sorted(x: np.ndarray, q: float) -> float:
    n = len(x)
    h = (n - 1) * q
    lo = int(math.floor(h))
    frac = h - lo
    if lo + 1 >= n or frac == 0.0:
        return float(x[lo])
    a, b = float(x[lo]), float(x[lo + 1])
    if np.isinf(b):
        return float("inf")
    return a + frac * (b - a)


def cluster_boot(flat, off, counts, B, rng):
    """Resample ACCOUNTS with replacement; recompute the extended-set 99th percentile."""
    n_acc = len(counts)
    thr = np.empty(B)
    for r in range(B):
        idx = rng.integers(0, n_acc, n_acc)
        lens = counts[idx]
        total = int(lens.sum())
        if total < 2:
            thr[r] = np.nan
            continue
        starts = off[idx]
        cum = np.concatenate(([0], np.cumsum(lens)[:-1]))
        gather = np.repeat(starts - cum, lens) + np.arange(total)
        thr[r] = r7_sorted(np.sort(flat[gather]), 0.99)
        if (r + 1) % 200 == 0:
            print(f"    cluster replicate {r+1}/{B}", flush=True)
    return thr


def iid_boot(flat, B, rng):
    n = len(flat)
    thr = np.empty(B)
    for r in range(B):
        thr[r] = r7_sorted(np.sort(flat[rng.integers(0, n, n)]), 0.99)
        if (r + 1) % 200 == 0:
            print(f"    iid replicate {r+1}/{B}", flush=True)
    return thr


def interval(thr, meas_sorted, n_open, n_pop):
    fin = np.isfinite(thr)
    t = thr[fin]
    ceil_thr = np.ceil(t)
    # endpoints are whole days: take the outer order statistic at each end, so the
    # interval is not narrowed by interpolating between two adjacent replicates.
    lo = float(np.percentile(ceil_thr, 2.5, method="lower"))
    hi = float(np.percentile(ceil_thr, 97.5, method="higher"))
    d = {
        "endpoint_convention": "2.5th by method='lower', 97.5th by method='higher'; whole days",
        "replicates": int(len(thr)),
        "replicates_with_infinite_p99": int((~fin).sum()),
        "share_infinite": float((~fin).sum() / len(thr)),
        "raw_p99_mean": float(t.mean()),
        "raw_p99_sd": float(t.std(ddof=1)),
        "ci95_on_ceilinged_threshold_days": [lo, hi],
        "ci95_width_days": hi - lo,
    }
    for tag, x in (("lo", lo), ("hi", hi)):
        eg = int((meas_sorted >= x).sum())
        d[f"not_live_at_{tag}"] = eg + n_open
        d[f"not_live_share_of_population_at_{tag}"] = (eg + n_open) / n_pop
    d["not_live_swing_across_interval_pairs"] = d["not_live_at_lo"] - d["not_live_at_hi"]
    d["not_live_swing_across_interval_pp_of_population"] = 100.0 * (
        d["not_live_share_of_population_at_lo"] - d["not_live_share_of_population_at_hi"]
    )
    return d


def main() -> None:
    B_ad = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    B_arm = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    arms = [int(a) for a in sys.argv[3:]] if len(sys.argv) > 3 else [W_ADOPTED]

    z = np.load(OUT / "bracket.npz")
    uidx = z["user_idx"]

    for W in arms:
        t = time.time()
        B = B_ad if W == W_ADOPTED else B_arm
        gap, state, d10 = z[f"gap_days_W{W}"], z[f"state_W{W}"], z[f"d10_W{W}"]
        m = (state == 0) & d10
        o = (state == 1) & d10
        keep = m | o                       # the extended set: one bracketing gap per pair
        vals = np.where(m, gap, np.inf)[keep]
        acc = uidx[keep]

        order = np.argsort(acc, kind="stable")
        flat = vals[order]
        acc_s = acc[order]
        uniq, first = np.unique(acc_s, return_index=True)
        off = first.astype(np.int64)
        counts = np.diff(np.append(off, len(flat)))
        n_pop = int(d10.sum())
        meas_sorted = np.sort(gap[m])
        n_open = int(o.sum())

        print(f"W={W}: extended {len(flat):,} pairs across {len(uniq):,} accounts, B={B}", flush=True)
        rng = np.random.default_rng(SEED + W)
        ct = cluster_boot(flat, off, counts, B, rng)
        print(f"  cluster done ({time.time()-t:.1f}s)", flush=True)
        it = iid_boot(flat, min(B, 1000), np.random.default_rng(SEED + W + 1))
        print(f"  iid done ({time.time()-t:.1f}s)", flush=True)

        res = {
            "instance": "data-scientist-b / namespace b4",
            "W": W,
            "seed": SEED + W,
            "population_post_D10": n_pop,
            "extended_set_n": int(len(flat)),
            "accounts": int(len(uniq)),
            "pairs_per_account": {
                "median": float(np.median(counts)),
                "max": int(counts.max()),
            },
            "account_clustered": interval(ct, meas_sorted, n_open, n_pop),
            "iid_pair_level_FOR_CONTRAST_ONLY": interval(it, meas_sorted, n_open, n_pop),
        }
        cw = res["account_clustered"]["ci95_width_days"]
        iw = res["iid_pair_level_FOR_CONTRAST_ONLY"]["ci95_width_days"]
        res["iid_overstates_precision_by"] = (cw / iw) if iw > 0 else None
        np.savez(OUT / f"bootstrap_replicates_W{W}.npz", cluster=ct, iid=it)
        (OUT / f"bootstrap_W{W}.json").write_text(json.dumps(res, indent=2))
        print(json.dumps({k: res[k] for k in
                          ("W", "account_clustered", "iid_pair_level_FOR_CONTRAST_ONLY",
                           "iid_overstates_precision_by")}, indent=2), flush=True)


if __name__ == "__main__":
    main()
