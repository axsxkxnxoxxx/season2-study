"""Step 7 (rerun), instance b2 -- stage 1: distinct insertion instants per account.

Implements decisions/0037 section 4 exactly:
  for each account, take the insertion instant of EVERY record in its sweep;
  sort ascending; collapse runs of EXACTLY equal instants to a single instant
  (exact float equality only, no rounding, no bucketing at any resolution);
  then take consecutive differences.

Insertion instant = np.interp(rid, knot_rid, knot_time) on the STORED Step 5
isotonic calibration curve. The curve is READ, never refitted (0029, 0036 s3).

Zero API calls.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b2"
DAY = 86400.0

OUT.mkdir(parents=True, exist_ok=True)

z = np.load(P5 / "full_scan.npz")
user = z["user"]
rid = z["rid"]
n_rec = len(rid)

cal = np.load(P5 / "calibration.npz")
knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
assert np.all(np.diff(knot_rid) > 0), "knot_rid not strictly increasing"
assert np.all(np.diff(knot_time) >= 0), "knot_time not monotone"

below = int((rid < knot_rid[0]).sum())
above = int((rid > knot_rid[-1]).sum())

# sort by (user, rid). The curve is monotone non-decreasing in rid, so sorting
# by rid is sorting by insertion instant.
order = np.lexsort((rid, user))
u_s = user[order]
inst = np.interp(rid[order].astype(np.float64), knot_rid, knot_time)
del order, rid, user, z

assert np.all(np.diff(u_s) >= 0)
# first record of each account, and exact-equality collapse within account
new_user = np.empty(n_rec, dtype=bool)
new_user[0] = True
new_user[1:] = u_s[1:] != u_s[:-1]

keep = np.empty(n_rec, dtype=bool)
keep[0] = True
keep[1:] = inst[1:] != inst[:-1]     # exact float inequality
keep |= new_user                     # always keep the first instant of an account

d_inst = inst[keep]
d_user = u_s[keep]
n_dist = len(d_inst)

uu, starts, counts = np.unique(d_user, return_index=True, return_counts=True)
np.savez(OUT / "instants.npz", users=uu.astype(np.int32), starts=starts.astype(np.int64),
         counts=counts.astype(np.int64), inst=d_inst)

# pooled gap distribution (context only -- NOT the reference distribution)
gap_ok = np.ones(n_dist, dtype=bool)
gap_ok[starts] = False               # drop cross-account differences
pooled = (np.diff(d_inst, prepend=d_inst[0]))[gap_ok] / DAY
np.save(OUT / "pooled_gaps_days.npy", pooled)

qs = [50, 75, 90, 95, 99, 99.5, 99.9]
meta = {
    "records_total": int(n_rec),
    "records_below_curve_start_rid": below,
    "records_above_curve_end_rid": above,
    "accounts": int(len(uu)),
    "distinct_instants_total": int(n_dist),
    "collapsed_records": int(n_rec - n_dist),
    "collapsed_pct": round(100.0 * (n_rec - n_dist) / n_rec, 4),
    "pooled_gaps_n": int(len(pooled)),
    "pooled_gap_days_percentiles": {str(q): float(np.percentile(pooled, q)) for q in qs},
    "pooled_gap_days_mean": float(pooled.mean()),
    "pooled_gap_days_max": float(pooled.max()),
    "pooled_sub_second_share_pct": round(100.0 * float((pooled < 1.0 / DAY).sum()) / len(pooled), 4),
    "distinct_instants_per_account": {
        "median": float(np.median(counts)), "min": int(counts.min()), "max": int(counts.max()),
    },
    "gaps_per_account_median": float(np.median(counts - 1)),
}
(OUT / "instants_meta.json").write_text(json.dumps(meta, indent=1))
print(json.dumps(meta, indent=1))
