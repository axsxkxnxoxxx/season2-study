"""Step 7 (instance b3) -- stage 1: per-account DISTINCT insertion instants.

READ ONLY. ZERO network calls.

Spec: task-sheet.md Step 7 (frozen), decisions/0038, 0037 Sec 4, 0036, 0029, 0021, 0025.

The operation, verbatim from decisions/0037 Sec 4:
  for each account, take the insertion instant of EVERY record in its sweep;
  sort ascending; collapse runs of EXACTLY equal instants to a single instant
  -- exact equality only, no rounding, no bucketing at any resolution -- then
  take the consecutive differences of that sorted distinct sequence.

Insertion instant = the stored Step 5 isotonic play-id calibration, read and
NOT refitted (decisions/0036 Sec 3).  The application is verbatim
src/step5_calibrate.py::insert_time -> np.interp(rid, knot_rid, knot_time),
which clamps outside the knot range to the endpoint values.

Out:  processed/step7/b3/instants.npz   (flat distinct-instant array + per-user offsets)
      processed/step7/b3/instants_meta.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b3"


def insert_time(rid, knot_rid, knot_time):
    """Verbatim from src/step5_calibrate.py. The curve is READ, never refitted."""
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()

    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]

    z = np.load(P5 / "full_scan.npz")
    user = z["user"]
    rid = z["rid"]
    n_rec = len(rid)
    print(f"records {n_rec:,}  ({time.time() - t:.1f}s)")

    tau = insert_time(rid, knot_rid, knot_time)
    print(f"calibrated  ({time.time() - t:.1f}s)")

    # how much of the sweep is outside the curve's fitted rid range -> clamped
    below = int((rid < knot_rid[0]).sum())
    above = int((rid > knot_rid[-1]).sum())

    order = np.lexsort((tau, user))
    u_s = user[order]
    t_s = tau[order]
    print(f"sorted  ({time.time() - t:.1f}s)")

    # collapse runs of EXACTLY equal instants, within account. Exact equality only.
    first_of_user = np.empty(n_rec, dtype=bool)
    first_of_user[0] = True
    np.not_equal(u_s[1:], u_s[:-1], out=first_of_user[1:])
    tie = np.zeros(n_rec, dtype=bool)
    np.equal(t_s[1:], t_s[:-1], out=tie[1:])
    keep = first_of_user | ~tie

    u_k = u_s[keep]
    t_k = t_s[keep]
    n_dist = len(t_k)
    print(f"distinct instants {n_dist:,}  ({time.time() - t:.1f}s)")

    n_users = int(user.max()) + 1
    # offsets[i]:offsets[i+1] is user i's distinct-instant slice, ascending
    offsets = np.searchsorted(u_k, np.arange(n_users + 1), side="left").astype(np.int64)

    counts = np.diff(offsets)
    ngaps = np.maximum(counts - 1, 0)

    np.savez(OUT / "instants.npz", tau=t_k, offsets=offsets)

    meta = {
        "instance": "data-scientist-b / namespace b3",
        "stage": "1 -- distinct insertion instants",
        "api_calls": 0,
        "records_in_sweep": n_rec,
        "distinct_insertion_instants": n_dist,
        "records_collapsed_by_exact_tie": n_rec - n_dist,
        "share_collapsed": (n_rec - n_dist) / n_rec,
        "accounts": n_users,
        "accounts_with_zero_instants": int((counts == 0).sum()),
        "accounts_with_one_instant_zero_gaps": int((counts == 1).sum()),
        "gaps_per_account": {
            "total": int(ngaps.sum()),
            "min": int(ngaps.min()),
            "median": float(np.median(ngaps)),
            "mean": float(ngaps.mean()),
            "max": int(ngaps.max()),
        },
        "calibration": {
            "source": "processed/step5/calibration.npz -- READ, NOT REFITTED",
            "application": "np.interp(rid, knot_rid, knot_time), verbatim step5_calibrate.insert_time",
            "n_knots": int(len(knot_rid)),
            "records_with_rid_below_first_knot_CLAMPED": below,
            "records_with_rid_above_last_knot_CLAMPED": above,
            "clamped_share": (below + above) / n_rec,
            "clamping_note": (
                "np.interp clamps outside the knot range, so all pre-curve records share one "
                "instant and all post-curve records share another; those runs collapse to a "
                "single instant each by the exact-tie rule. Reported, not repaired -- the curve "
                "is a required input and is not refitted."
            ),
        },
        "elapsed_s": time.time() - t,
    }
    (OUT / "instants_meta.json").write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
