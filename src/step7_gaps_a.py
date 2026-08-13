"""Step 7 (instance a), stage 1: insertion instants and the observed gap distribution.

Reads processed/step5/full_scan.npz and the STORED isotonic curve
processed/step5/calibration.npz.  DOES NOT REFIT the curve (task-sheet Step 7,
decisions/0036 sec 3).  Insertion instant = np.interp(rid, knot_rid, knot_time).

Gap = interval between consecutive insertion instants on one account, as a
continuous instant difference, in days (decisions/0029; not floored).

Writes processed/step7/a/gaps.npz and processed/step7/a/stage1.json.
ZERO API calls.
"""
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
P7 = ROOT / "processed" / "step7" / "a"
DAY = 86400.0

P7.mkdir(parents=True, exist_ok=True)
out = {"step": 7, "stage": 1, "instance": "a", "api_calls": 0}

z = np.load(P5 / "full_scan.npz")
user = z["user"]
rid = z["rid"]
kind = z["kind"]
action = z["action"]
n = rid.size
out["records_total"] = int(n)
out["users_total"] = int(np.unique(user).size)

c = np.load(P5 / "calibration.npz")
kr = c["knot_rid"].astype("float64")
kt = c["knot_time"].astype("float64")
assert np.all(np.diff(kr) >= 0) and np.all(np.diff(kt) >= 0)
out["calibration"] = {
    "source": "processed/step5/calibration.npz (STORED, not refitted)",
    "n_knots": int(kr.size),
    "knot_rid_min": float(kr[0]), "knot_rid_max": float(kr[-1]),
    "knot_time_min": float(kt[0]), "knot_time_max": float(kt[-1]),
    "records_below_knot_range_clamped": int((rid < kr[0]).sum()),
    "records_above_knot_range_clamped": int((rid > kr[-1]).sum()),
}

ins = np.interp(rid.astype("float64"), kr, kt)   # np.interp clamps outside range

# ---- order by (user, rid).  rid is a global auto-increment assigned at insert,
# so ordering by rid is the exact insertion order; the isotonic curve is monotone
# so this is also the order of `ins`.
order = np.lexsort((rid, user))
u_s = user[order]
ins_s = ins[order]
rid_s = rid[order]

same_user = u_s[1:] == u_s[:-1]
d_all = np.diff(ins_s) / DAY            # days, continuous
gaps_all = d_all[same_user]             # every consecutive RECORD pair
gaps_all = np.maximum(gaps_all, 0.0)    # monotone curve => already >= 0

out["duplicate_rids_global"] = int(n - np.unique(rid).size)
out["gaps_all_records_n"] = int(gaps_all.size)
out["gaps_all_records_zero_n"] = int((gaps_all == 0.0).sum())
out["gaps_all_records_zero_share"] = float((gaps_all == 0.0).mean())

# ---- variant: consecutive DISTINCT insertion instants (drop exact ties)
keep_distinct = np.empty(u_s.size, dtype=bool)
keep_distinct[0] = True
keep_distinct[1:] = (~same_user) | (ins_s[1:] != ins_s[:-1])
u_d = u_s[keep_distinct]
ins_d = ins_s[keep_distinct]
same_user_d = u_d[1:] == u_d[:-1]
gaps_distinct = (np.diff(ins_d) / DAY)[same_user_d]
out["distinct_instants_n"] = int(u_d.size)
out["gaps_distinct_instants_n"] = int(gaps_distinct.size)


def summarise(g):
    qs = [50, 75, 90, 95, 98, 99, 99.5, 99.9, 100]
    return {
        "n": int(g.size),
        "mean_days": float(g.mean()),
        "max_days": float(g.max()),
        "percentiles_days": {str(q): float(np.percentile(g, q)) for q in qs},
    }


out["gap_summary_all_records"] = summarise(gaps_all)
out["gap_summary_distinct_instants"] = summarise(gaps_distinct)

# ---- histogram material for the chart (log-spaced), aggregate only
edges = np.concatenate(([0.0], np.logspace(-6, np.log10(6000.0), 121)))
h_all, _ = np.histogram(gaps_all, bins=edges)
h_dis, _ = np.histogram(gaps_distinct, bins=edges)

np.savez_compressed(
    P7 / "gaps.npz",
    gaps_all=gaps_all.astype("float32"),
    gaps_distinct=gaps_distinct.astype("float32"),
    hist_edges=edges, hist_all=h_all, hist_distinct=h_dis,
)
# per-user insertion instants, for stage 3 (row-level -> processed/ only)
np.savez_compressed(
    P7 / "user_instants.npz",
    user=u_s.astype("int32"), ins=ins_s,
)

(P7 / "stage1.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
