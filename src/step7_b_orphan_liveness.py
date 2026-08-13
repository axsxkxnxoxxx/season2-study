"""
Step 7 - derive the liveness threshold, instance A.

Spec source: task-sheet.md Step 7 (lines 226-254), as ruled by
decisions/0036-step7-threshold-and-shape.md (threshold = 99th percentile;
test = the single gap bracketing tau1), decisions/0025 (round UP),
decisions/0029 (continuous instant differences), decisions/0021 (insertion
time, not claimed watched_at), decisions/0034 (anchor is tau1, never tau2),
decisions/0026 (W = 108 days).

ZERO API calls. Row-level detail -> processed/step7/a/. Aggregates -> artifacts/.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
P7 = ROOT / "processed" / "step7" / "a"
ART = ROOT / "artifacts"

PCTL = 99.0            # decisions/0036
W_DAYS = 108           # decisions/0026, adopted value (NOT the 107 in the step6 artifacts)
DAY = 86400.0
BACKFILL_D = 180.0     # Step 5 backfill threshold (for waterfall reproduction only)
POSTDATE_D = -30.0     # Step 5 post-date threshold (for waterfall reproduction only)
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]


def main():
    P7.mkdir(parents=True, exist_ok=True)
    out = {"step": 7, "instance": "a", "api_calls": 0,
           "spec": "task-sheet.md Step 7 as ruled by decisions/0036, 0029, 0025, 0021, 0034",
           "threshold_percentile": PCTL, "W_days_applied": W_DAYS}

    # ---- 1. insertion instants, from the STORED calibration curve (never refit)
    z = np.load(P5 / "full_scan.npz")
    rid = z["rid"]
    user = z["user"]
    c = np.load(P5 / "calibration.npz")
    kr, kt = c["knot_rid"], c["knot_time"]
    assert np.all(np.diff(kr) > 0) and np.all(np.diff(kt) >= 0)

    n_below = int((rid < kr.min()).sum())
    n_above = int((rid > kr.max()).sum())
    ins = np.interp(rid.astype(np.float64), kr, kt)   # clamps outside the knot range

    out["records"] = {
        "records_total": int(rid.size),
        "accounts_in_scan": int(np.unique(user).size),
        "rid_below_first_knot_clamped": n_below,
        "rid_above_last_knot_clamped": n_above,
        "clamped_share": round((n_below + n_above) / rid.size, 8),
        "calibration_source": "processed/step5/calibration.npz (read, not refit)",
    }

    # ---- 2. per-account consecutive insertion gaps, continuous seconds
    order = np.lexsort((rid, user))
    u_s = user[order]
    i_s = ins[order]
    d = np.diff(i_s)
    same = u_s[1:] == u_s[:-1]
    gaps = d[same]                      # seconds
    gaps = np.maximum(gaps, 0.0)        # isotonic curve is non-decreasing; guard only
    gaps_d = gaps / DAY

    np.save(P7 / "insertion_instants_sorted.npy", i_s)
    np.save(P7 / "user_sorted.npy", u_s)
    np.save(P7 / "gaps_days.npy", gaps_d)

    q = [50, 75, 90, 95, 97.5, 99, 99.5, 99.9, 100]
    out["gap_distribution_all_records"] = {
        "n_gaps": int(gaps_d.size),
        "n_accounts_contributing": int(np.unique(u_s[1:][same]).size),
        "mean_days": float(gaps_d.mean()),
        "zero_or_subsecond_share": float((gaps_d < 1.0 / DAY).mean()),
        "percentiles_days": {str(k): float(np.percentile(gaps_d, k)) for k in q},
    }

    p99 = float(np.percentile(gaps_d, PCTL))
    threshold = int(np.ceil(p99))
    out["threshold"] = {
        "percentile_value_days_continuous": p99,
        "rounding": "ceiling to whole days (decisions/0025)",
        "threshold_days": threshold,
        "percentile_interpolation": "numpy default 'linear'",
    }
    print(json.dumps(out["gap_distribution_all_records"], indent=2))
    print("P99 =", p99, "-> threshold", threshold)

    # ---- 2b. sensitivity: dedupe identical insertion instants per account
    key = u_s.astype(np.int64) * (2 ** 40) + np.round(i_s).astype(np.int64)
    keep = np.empty(key.size, bool)
    keep[0] = True
    keep[1:] = key[1:] != key[:-1]
    u_d, i_d = u_s[keep], i_s[keep]
    dd = np.diff(i_d)
    sd = u_d[1:] == u_d[:-1]
    gd = np.maximum(dd[sd], 0.0) / DAY
    out["sensitivity_dedup_same_second"] = {
        "n_gaps": int(gd.size),
        "percentiles_days": {str(k): float(np.percentile(gd, k)) for k in q},
        "threshold_days": int(np.ceil(np.percentile(gd, PCTL))),
    }
    print("dedup P99", np.percentile(gd, PCTL))

    with open(P7 / "gap_distribution.json", "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", P7 / "gap_distribution.json")


if __name__ == "__main__":
    main()
