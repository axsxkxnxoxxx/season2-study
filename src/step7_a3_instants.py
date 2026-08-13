"""Step 7 (frozen-spec run), instance A3 — distinct insertion-instant sequences per account.

Gap unit per decisions/0037 SS4 and task-sheet.md line 238, applied exactly:
  for each account, take the insertion instant of EVERY record in its sweep; sort ascending;
  collapse runs of EXACTLY equal instants to a single instant (exact float equality only; no
  rounding, no bucketing at any resolution); then take consecutive differences.

Insertion instant = np.interp(rid, knot_rid, knot_time) read from the STORED Step 5
calibration curve. The curve is NOT refitted (task-sheet Step 7; decisions/0029, 0036 SS3).

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/a3")
SEC_PER_DAY = 86400.0


def main():
    os.makedirs(OUT, exist_ok=True)

    scan = np.load(os.path.join(P5, "full_scan.npz"))
    user = scan["user"]
    rid = scan["rid"]
    n_records = int(user.size)
    assert n_records == 27656813, f"unexpected record count {n_records}"

    cal = np.load(os.path.join(P5, "calibration.npz"))
    knot_rid = cal["knot_rid"].astype(np.float64)
    knot_time = cal["knot_time"].astype(np.float64)
    assert np.all(np.diff(knot_rid) > 0), "knots not strictly increasing in rid"

    ridf = rid.astype(np.float64)
    n_below = int((ridf < knot_rid[0]).sum())
    n_above = int((ridf > knot_rid[-1]).sum())

    # np.interp clamps outside the knot range: every record below the first knot maps to
    # knot_time[0] exactly, and every record above the last knot to knot_time[-1] exactly.
    # Those clamped records are EXACT ties and therefore collapse under the 0037 rule.
    inst = np.interp(ridf, knot_rid, knot_time)

    order = np.lexsort((inst, user))
    su = user[order]
    si = inst[order]

    starts = np.flatnonzero(np.r_[True, su[1:] != su[:-1]])
    ends = np.r_[starts[1:], su.size]
    uids = su[starts]

    # collapse runs of EXACTLY equal instants, within account
    keep = np.r_[True, (si[1:] != si[:-1]) | (su[1:] != su[:-1])]
    d_inst = si[keep]
    d_user = su[keep]

    d_starts = np.flatnonzero(np.r_[True, d_user[1:] != d_user[:-1]])
    d_ends = np.r_[d_starts[1:], d_user.size]
    d_uids = d_user[d_starts]
    assert np.array_equal(d_uids, uids)

    # pooled gaps = consecutive differences within account
    gap_mask = np.r_[False, d_user[1:] == d_user[:-1]]
    pooled_sec = np.diff(d_inst, prepend=0.0)[gap_mask]
    pooled_user = d_user[gap_mask]
    assert (pooled_sec > 0).all(), "exact-tie collapse must leave strictly positive gaps"
    pooled_days = pooled_sec / SEC_PER_DAY

    np.savez_compressed(
        os.path.join(OUT, "distinct_instants.npz"),
        uids=d_uids, starts=d_starts.astype(np.int64),
        ends=d_ends.astype(np.int64), inst=d_inst,
    )
    np.savez_compressed(
        os.path.join(OUT, "pooled_gaps.npz"), gap_days=pooled_days, user=pooled_user,
    )

    n_rec_per = ends - starts
    n_dist_per = d_ends - d_starts
    gaps_per = np.maximum(n_dist_per - 1, 0)

    summary = {
        "instance": "a3",
        "api_calls": 0,
        "n_records": n_records,
        "n_accounts": int(uids.size),
        "n_distinct_instants": int(d_inst.size),
        "collapsed_exact_ties": int(n_records - d_inst.size),
        "collapsed_share": float((n_records - d_inst.size) / n_records),
        "rid_below_first_knot_clamped": n_below,
        "rid_above_last_knot_clamped": n_above,
        "n_pooled_gaps": int(pooled_days.size),
        "records_per_account_median": float(np.median(n_rec_per)),
        "distinct_instants_per_account_median": float(np.median(n_dist_per)),
        "gaps_per_account_median": float(np.median(gaps_per)),
        "gaps_per_account_mean": float(gaps_per.mean()),
        "pooled_gap_days_percentiles": {
            str(q): float(np.percentile(pooled_days, q))
            for q in (50, 75, 90, 95, 99, 99.5, 99.9)
        },
        "pooled_gap_sub_second_share": float((pooled_sec < 1.0).mean()),
        "pooled_gap_days_max": float(pooled_days.max()),
    }
    with open(os.path.join(OUT, "instants_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
