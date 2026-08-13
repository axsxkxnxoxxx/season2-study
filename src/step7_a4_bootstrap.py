"""Step 7 rerun (decisions/0040), instance A4 — ACCOUNT-CLUSTERED bootstrap of the threshold.

Red Team flagged the previous run's interval as estimated from 300 replicates, whose 2.5%/97.5%
endpoints are the 7th and 8th order statistics quoted to the day. This runs B = 2,000 and states
the count. Both candidate reference sets are bootstrapped:

  - EXTENDED  : every TESTED pair, open-ended gaps carried as +inf (decisions/0040 SS2)
  - MEASURED  : finite bracketing gaps only (the superseded decisions/0039 SS5 restriction)

The clustering unit is the ACCOUNT, because gaps within an account are not independent: one
account's insertion sweep supplies the bracketing gap for every pair it owns, and pairs sharing a
bracketing instant share the value exactly.

An i.i.d. pair bootstrap is run alongside, purely to show how much precision the i.i.d. assumption
invents. It is NOT the interval to report.

Vectorised: the per-account slices are precomputed once and indexed, never re-concatenated.
Results are written to disk by this script alone. Zero API calls.
"""
import json
import math
import os
import time

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a4")
PCTL = 99.0
B = 2000
SEED = 20260813


def ceil_or_none(v):
    return int(math.ceil(v)) if np.isfinite(v) else None


def main():
    t_start = time.time()
    d = np.load(os.path.join(OUT, "pair_bracketing_W108.npz"))
    ref = d["ref"]
    gap = d["gap_days"]
    no_after = d["no_after"]
    no_before = d["no_before"]
    uidx = d["user_idx"]

    tested = ref & ~no_before                      # measured gap OR open-ended
    val = np.where(no_after, np.inf, gap)[tested]  # one value per tested pair
    u = uidx[tested]
    n_tested = int(val.size)
    n_open = int(np.isinf(val).sum())
    n_meas = n_tested - n_open
    print(f"tested pairs {n_tested}  measured {n_meas}  open-ended {n_open} "
          f"({n_open / n_tested:.4%})")

    # ---- cluster layout: sort once by account, then index ----
    order = np.argsort(u, kind="stable")
    u_s = u[order]
    val_s = val[order]
    starts = np.flatnonzero(np.r_[True, u_s[1:] != u_s[:-1]])
    counts = np.diff(np.r_[starts, u_s.size])
    n_acc = starts.size
    print(f"accounts carrying tested pairs: {n_acc}  "
          f"pairs/account median {np.median(counts):.0f} max {counts.max()}")

    finite_mask_s = np.isfinite(val_s)

    # ---- tie structure of the bracketing-gap values, which is why i.i.d. is wrong ----
    fin = val_s[finite_mask_s]
    uq, cnt = np.unique(fin, return_counts=True)
    share_tied = float(cnt[cnt > 1].sum() / fin.size)
    largest_tie = int(cnt.max())

    rng = np.random.default_rng(SEED)
    thr_ext = np.empty(B)
    thr_meas = np.empty(B)
    open_share = np.empty(B)

    for b in range(B):
        samp = rng.integers(0, n_acc, size=n_acc)
        c = counts[samp]
        tot = int(c.sum())
        # vectorised gather of the sampled accounts' slices
        offs = np.repeat(starts[samp] - np.r_[0, np.cumsum(c)[:-1]], c)
        idx = offs + np.arange(tot)
        v = val_s[idx]
        fm = finite_mask_s[idx]
        open_share[b] = 1.0 - fm.mean()
        with np.errstate(invalid="ignore"):
            thr_ext[b] = np.percentile(v, PCTL)
        thr_meas[b] = np.percentile(v[fm], PCTL)
        if (b + 1) % 250 == 0:
            print(f"  clustered replicate {b + 1}/{B}  "
                  f"elapsed {time.time() - t_start:.1f}s", flush=True)

    n_inf_ext = int(np.isnan(thr_ext).sum() + np.isinf(thr_ext).sum())
    ext_fin = thr_ext[np.isfinite(thr_ext)]

    # ---- i.i.d. pair bootstrap, for contrast only ----
    thr_ext_iid = np.empty(B)
    thr_meas_iid = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n_tested, size=n_tested)
        v = val_s[idx]
        fm = finite_mask_s[idx]
        with np.errstate(invalid="ignore"):
            thr_ext_iid[b] = np.percentile(v, PCTL)
        thr_meas_iid[b] = np.percentile(v[fm], PCTL)
    ext_iid_fin = thr_ext_iid[np.isfinite(thr_ext_iid)]

    def iv(arr, label):
        lo, hi = np.percentile(arr, [2.5, 97.5])
        return {
            "label": label,
            "replicates_used": int(arr.size),
            "point_of_replicates_median_raw_days": float(np.median(arr)),
            "ci95_raw_days": [float(lo), float(hi)],
            "ci95_ceil_days": [int(math.ceil(lo)), int(math.ceil(hi))],
            "sd_raw_days": float(arr.std(ddof=1)),
        }

    out = {
        "step": 7,
        "instance": "a4",
        "api_calls": 0,
        "replicates": B,
        "seed": SEED,
        "rng": "numpy default_rng (PCG64)",
        "clustering_unit": "account",
        "why_clustered": (
            "One account's insertion sweep supplies the bracketing gap for every pair it owns, "
            "so pairs are not independent draws. Measured here: "
            f"{share_tied:.4f} of measured-gap pairs share their bracketing gap value exactly "
            f"with at least one other pair, largest tie group {largest_tie}."
        ),
        "tie_structure": {
            "share_of_measured_gap_pairs_sharing_their_value": round(share_tied, 6),
            "largest_tie_group": largest_tie,
            "n_distinct_values": int(uq.size),
        },
        "population": {
            "post_D10_tested_pairs": n_tested,
            "measured_gap_pairs": n_meas,
            "open_ended_pairs": n_open,
            "open_ended_share": round(n_open / n_tested, 6),
            "accounts": n_acc,
            "pairs_per_account_median": float(np.median(counts)),
            "pairs_per_account_max": int(counts.max()),
        },
        "point_estimates_on_the_observed_sample": {
            "extended_p99_raw_days": float(np.percentile(val_s, PCTL)),
            "extended_threshold_days": ceil_or_none(float(np.percentile(val_s, PCTL))),
            "measured_only_p99_raw_days": float(np.percentile(fin, PCTL)),
            "measured_only_threshold_days": ceil_or_none(float(np.percentile(fin, PCTL))),
        },
        "ACCOUNT_CLUSTERED": {
            "extended": iv(ext_fin, "extended reference, account-clustered"),
            "extended_infinite_replicates": n_inf_ext,
            "extended_infinite_replicate_share": round(n_inf_ext / B, 6),
            "measured_only": iv(thr_meas, "measured-gap-only reference, account-clustered"),
            "open_ended_share_across_replicates": {
                "median": float(np.median(open_share)),
                "p2_5": float(np.percentile(open_share, 2.5)),
                "p97_5": float(np.percentile(open_share, 97.5)),
                "share_of_replicates_above_1pct": float((open_share > 0.01).mean()),
            },
        },
        "IID_FOR_CONTRAST_NOT_TO_BE_REPORTED": {
            "extended": iv(ext_iid_fin, "extended reference, i.i.d. pairs"),
            "extended_infinite_replicates": int(B - ext_iid_fin.size),
            "measured_only": iv(thr_meas_iid, "measured-gap-only reference, i.i.d. pairs"),
        },
        "runtime_seconds": round(time.time() - t_start, 1),
    }

    # width ratio: how much precision the i.i.d. assumption invents
    for k in ("extended", "measured_only"):
        c = out["ACCOUNT_CLUSTERED"][k]["ci95_raw_days"]
        i = out["IID_FOR_CONTRAST_NOT_TO_BE_REPORTED"][k]["ci95_raw_days"]
        wc, wi = c[1] - c[0], i[1] - i[0]
        out["IID_FOR_CONTRAST_NOT_TO_BE_REPORTED"][k]["clustered_width_over_iid_width"] = (
            round(wc / wi, 2) if wi > 0 else None)

    path = os.path.join(OUT, "bootstrap.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    np.savez_compressed(os.path.join(OUT, "bootstrap_replicates.npz"),
                        thr_ext=thr_ext, thr_meas=thr_meas,
                        thr_ext_iid=thr_ext_iid, thr_meas_iid=thr_meas_iid,
                        open_share=open_share)
    print("wrote", path)
    print(json.dumps({k: out[k] for k in (
        "replicates", "seed", "tie_structure", "point_estimates_on_the_observed_sample",
        "ACCOUNT_CLUSTERED", "IID_FOR_CONTRAST_NOT_TO_BE_REPORTED")}, indent=2))


if __name__ == "__main__":
    main()
