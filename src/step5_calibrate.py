"""Step 5: calibrate Trakt play-id -> insertion time, and validate the calibration.

WHY THIS EXISTS
Step 5 has to separate a real 2019 watch from a 2026 import that claims 2019.
Nothing inside `watched_at` can do it: an import rewrites that field wholesale.
A second, independent clock is needed.

THE INSTRUMENT
The play `id` is a global auto-increment assigned when Trakt writes the row, so
it orders records by INSERT time no matter what `watched_at` claims. Calibrating
id -> wall-clock turns every record into a pair (claimed watch date, actual
logging date). Backfill is the gap between them.

WHAT THE CALIBRATION IS FITTED ON
`checkin` and `scrobble` records only. These are emitted by a player or app at
the moment of viewing, so their `watched_at` IS their insert time. `watch` rows
are excluded from the fit because a bulk import produces exactly those, and
fitting on them would let the contamination define the clock that is supposed to
detect it.

Evidence that imports do not produce checkins or scrobbles, measured on this
store: in the four highest id bands the `watch` median watched_at collapses to
2021-2023 while the checkin and scrobble medians continue to track real time
(2026-07-03, 07-05, 07-11, 07-28). If imports minted checkins the checkin median
would have collapsed too. It does not.

MONOTONISATION
Isotonic regression by pool-adjacent-violators, weighted by bin count. NOT a
cumulative maximum: a cummax ratchets the whole curve up off one contaminated
bin, which is a bug this file previously had and which produced a 2,065-day
median lag on records that were logged in real time.

RESIDUAL ERROR AND ITS DIRECTION
Per-bin medians sit slightly below the bin's true insert instant, because even a
scrobble is written a few minutes to a few hours after the viewing starts, and
because a sparse bin resolves time only as coarsely as its id span. The estimate
is therefore mildly EARLY, which makes the backfill lag it produces mildly SMALL.
The diagnostic under-flags rather than over-flags. That is the safe direction for
a gate proposal, and it is stated in the report rather than corrected away.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
SCAN = ROOT / "processed" / "step5" / "full_scan.npz"
OUT = ROOT / "processed" / "step5"

NULL_TS = np.iinfo(np.int64).min
TAU_PULL = int(dt.datetime(2026, 8, 11, tzinfo=dt.timezone.utc).timestamp())
FIT_BIN = 400  # checkin+scrobble records per calibration knot
DAY = 86400.0


def iso(x) -> str:
    return dt.datetime.fromtimestamp(int(x), dt.timezone.utc).strftime("%Y-%m-%d")


def pava(y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Weighted isotonic regression, non-decreasing, by pool-adjacent-violators."""
    vals = list(y.astype(np.float64))
    wts = list(w.astype(np.float64))
    sizes = [1] * len(vals)
    i = 0
    while i < len(vals) - 1:
        if vals[i] <= vals[i + 1]:
            i += 1
            continue
        # pool i and i+1, then walk back while the invariant is broken
        tw = wts[i] + wts[i + 1]
        vals[i] = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / tw
        wts[i] = tw
        sizes[i] += sizes[i + 1]
        del vals[i + 1], wts[i + 1], sizes[i + 1]
        while i > 0 and vals[i - 1] > vals[i]:
            tw = wts[i - 1] + wts[i]
            vals[i - 1] = (vals[i - 1] * wts[i - 1] + vals[i] * wts[i]) / tw
            wts[i - 1] = tw
            sizes[i - 1] += sizes[i]
            del vals[i], wts[i], sizes[i]
            i -= 1
    return np.repeat(np.asarray(vals), np.asarray(sizes))


def build_calibration(rid, ts, action, fit_mask):
    r = rid[fit_mask]
    t = ts[fit_mask].astype(np.float64)
    order = np.argsort(r, kind="stable")
    r = r[order]
    t = t[order]

    n = len(r)
    nb = max(1, n // FIT_BIN)
    edges = np.linspace(0, n, nb + 1).astype(int)
    knot_rid = np.empty(nb, dtype=np.float64)
    knot_med = np.empty(nb, dtype=np.float64)
    knot_w = np.empty(nb, dtype=np.float64)
    for i in range(nb):
        a, b = edges[i], edges[i + 1]
        knot_rid[i] = np.median(r[a:b])
        knot_med[i] = np.median(t[a:b])
        knot_w[i] = b - a
    knot_time = pava(knot_med, knot_w)
    return knot_rid, knot_time, knot_med


def insert_time(rid, knot_rid, knot_time):
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def main():
    d = np.load(SCAN)
    rid, ts, action, user = d["rid"], d["ts"], d["action"], d["user"]
    have = (ts != NULL_TS) & (ts <= TAU_PULL)
    realtime = have & (action != 0)  # checkin or scrobble

    print(f"fit records (checkin+scrobble, dated, <= tau_pull): {realtime.sum():,}")

    # ---- held-out validation: fit on even users, test on odd users -------------
    even = realtime & (user % 2 == 0)
    odd = realtime & (user % 2 == 1)
    kr_e, kt_e, _ = build_calibration(rid, ts, action, even)
    lag_odd = (insert_time(rid[odd], kr_e, kt_e) - ts[odd]) / DAY
    print("\nHELD-OUT VALIDATION  (fit on even-index users, test on odd-index users)")
    print(f"  test records: {odd.sum():,}")
    for q in (1, 10, 25, 50, 75, 90, 99):
        print(f"    p{q:<3d} lag {np.percentile(lag_odd, q):>10.3f} d")
    print(f"    |lag| <= 1d: {np.mean(np.abs(lag_odd) <= 1):.4f}"
          f"   |lag| <= 7d: {np.mean(np.abs(lag_odd) <= 7):.4f}"
          f"   lag > 180d: {np.mean(lag_odd > 180):.4f}")

    # ---- full fit --------------------------------------------------------------
    knot_rid, knot_time, knot_med = build_calibration(rid, ts, action, realtime)
    viol = int((np.diff(knot_med) < 0).sum())
    print(f"\nFULL FIT: {len(knot_rid)} knots, {viol} raw median violations pooled by PAVA")
    print(f"  curve start {iso(knot_time[0])}  end {iso(knot_time[-1])}")
    print(f"  rid range covered {int(knot_rid[0]):,} .. {int(knot_rid[-1]):,}")

    tau = insert_time(rid, knot_rid, knot_time)

    print("\nLAG BY ACTION on the full fit (in-sample for checkin/scrobble)")
    for name, code in (("watch", 0), ("checkin", 1), ("scrobble", 2)):
        m = have & (action == code)
        lag = (tau[m] - ts[m]) / DAY
        print(f"  {name:9s} n={m.sum():>10,}  p10 {np.percentile(lag,10):>8.2f}"
              f"  median {np.median(lag):>9.2f}  p90 {np.percentile(lag,90):>10.2f}"
              f"  |lag|<=7d {np.mean(np.abs(lag)<=7):.4f}  lag>180d {np.mean(lag>180):.4f}")

    # ---- sanity: curve read at fixed rid points -------------------------------
    print("\nCURVE READ-OUT")
    for r in (6e8, 1e9, 2.4e9, 4.2e9, 7.4e9, 9.7e9, 1.2e10, 1.3e10, 1.42e10):
        print(f"  rid {r:>16,.0f} -> {iso(np.interp(r, knot_rid, knot_time))}")

    np.savez(OUT / "calibration.npz", knot_rid=knot_rid, knot_time=knot_time)
    (OUT / "calibration_meta.json").write_text(json.dumps({
        "fit_on": "checkin+scrobble only",
        "fit_records": int(realtime.sum()),
        "fit_bin_records": FIT_BIN,
        "n_knots": int(len(knot_rid)),
        "monotonisation": "weighted isotonic (PAVA)",
        "curve_start": iso(knot_time[0]),
        "curve_end": iso(knot_time[-1]),
        "heldout_median_lag_days": float(np.median(lag_odd)),
        "heldout_abs_lag_le_7d": float(np.mean(np.abs(lag_odd) <= 7)),
        "tau_pull": "2026-08-11T00:00:00Z",
    }, indent=2))
    print("\nwrote", OUT / "calibration.npz")


if __name__ == "__main__":
    main()
