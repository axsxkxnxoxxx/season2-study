"""Step 7 (rerun), instance A2 — build distinct insertion-instant sequences per account
and the pooled gap distribution.

Gap unit per decisions/0037 SS4, stated exactly:
  for each account, take the insertion instant of EVERY record in its sweep; sort ascending;
  collapse runs of EXACTLY equal instants to a single instant (exact float equality only, no
  rounding, no bucketing at any resolution); then take consecutive differences.

Insertion instant = np.interp(rid, knot_rid, knot_time) from the STORED Step 5 calibration.
The curve is NOT refitted (task-sheet Step 7; decisions/0029, 0036 SS3).

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a2")
os.makedirs(OUT, exist_ok=True)

SEC_PER_DAY = 86400.0


def main():
    scan = np.load(os.path.join(ROOT, "processed/step5/full_scan.npz"))
    user = scan["user"]
    rid = scan["rid"]
    n_records = user.size

    cal = np.load(os.path.join(ROOT, "processed/step5/calibration.npz"))
    knot_rid = cal["knot_rid"]
    knot_time = cal["knot_time"]

    # np.interp clamps outside the knot range; record how many records are clamped.
    below = int((rid < knot_rid[0]).sum())
    above = int((rid > knot_rid[-1]).sum())

    inst = np.interp(rid.astype(np.float64), knot_rid, knot_time)

    # sort by (user, instant)
    order = np.lexsort((inst, user))
    su = user[order]
    si = inst[order]

    # per-user boundaries
    starts = np.flatnonzero(np.r_[True, su[1:] != su[:-1]])
    ends = np.r_[starts[1:], su.size]
    uids = su[starts]

    # collapse runs of EXACTLY equal instants within a user
    keep = np.r_[True, (si[1:] != si[:-1]) | (su[1:] != su[:-1])]
    d_inst = si[keep]
    d_user = su[keep]

    d_starts = np.flatnonzero(np.r_[True, d_user[1:] != d_user[:-1]])
    d_ends = np.r_[d_starts[1:], d_user.size]
    d_uids = d_user[d_starts]
    assert np.array_equal(d_uids, uids)

    # pooled gaps: consecutive differences of the distinct sequence, within user
    gap_mask = np.r_[False, d_user[1:] == d_user[:-1]]
    pooled_gaps_sec = np.diff(d_inst, prepend=0.0)[gap_mask]
    pooled_gap_user = d_user[gap_mask]
    pooled_gaps_days = pooled_gaps_sec / SEC_PER_DAY
    assert (pooled_gaps_sec > 0).all(), "exact-tie collapse should leave strictly positive gaps"

    np.savez_compressed(
        os.path.join(OUT, "distinct_instants.npz"),
        uids=d_uids,
        starts=d_starts.astype(np.int64),
        ends=d_ends.astype(np.int64),
        inst=d_inst,
    )
    np.savez_compressed(
        os.path.join(OUT, "pooled_gaps.npz"),
        gap_days=pooled_gaps_days,
        user=pooled_gap_user,
    )

    n_per_user = (ends - starts)
    n_distinct_per_user = (d_ends - d_starts)
    gaps_per_user = np.maximum(n_distinct_per_user - 1, 0)

    q = [50, 75, 90, 95, 99, 99.5, 99.9]
    summary = {
        "n_records": int(n_records),
        "n_accounts": int(uids.size),
        "n_distinct_instants": int(d_inst.size),
        "collapsed_records": int(n_records - d_inst.size),
        "collapsed_share": float((n_records - d_inst.size) / n_records),
        "rid_below_curve_start": below,
        "rid_above_curve_end": above,
        "n_pooled_gaps": int(pooled_gaps_days.size),
        "records_per_account_median": float(np.median(n_per_user)),
        "distinct_instants_per_account_median": float(np.median(n_distinct_per_user)),
        "gaps_per_account_median": float(np.median(gaps_per_user)),
        "gaps_per_account_mean": float(gaps_per_user.mean()),
        "pooled_gap_days_percentiles": {
            str(p): float(np.percentile(pooled_gaps_days, p)) for p in q
        },
        "pooled_gap_days_mean": float(pooled_gaps_days.mean()),
        "pooled_gap_sub_second_share": float((pooled_gaps_sec < 1.0).mean()),
        "pooled_gap_sub_minute_share": float((pooled_gaps_sec < 60.0).mean()),
    }
    with open(os.path.join(OUT, "pooled_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
