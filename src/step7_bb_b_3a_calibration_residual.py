"""Step 7 ALT-BROAD rerun (instance b, namespace bb_b) -- stage 3a.

BOUND THE CALIBRATION RESIDUAL. Required by decisions/0048 Sec 9 and never done.

The rule's first conjunct is a comparison between an INTERPOLATED insertion
instant and tau1. So the exclusion set inherits the calibration's error, and
nobody has measured how much of it.

What this stage measures, from the STORED curve only -- READ, NEVER REFITTED:

 R1  The in-sample residual on the fit family. The calibration was fitted on
     checkin + scrobble records only, whose watched_at IS their insert time by
     construction (src/step5_calibrate.py). For those records
         r = insert_time(rid) - watched_at
     is the calibration's own error, in days. In-sample, so OPTIMISTIC: it
     understates the error on watch rows, which are the majority. The stored
     held-out figure in calibration_meta.json is quoted beside it and is NOT
     recomputed, because recomputing it would mean refitting.

 R2  Future-dated records: watched_at later than the record's own calibrated
     insertion instant. Impossible for a genuine record, so a direct read on
     the residual's upper tail. 0048 Sec 9 cites 22.68%, 6,271,584 of
     27,656,434. Confirmed or refuted here.

 R3  Clamping. np.interp clamps outside the knot range. Records above the last
     knot are pinned to knot_time[-1], which pushes their instant EARLIER and
     therefore TOWARD FALSE EXCLUSION. 0048 cites 5,094. Measured, and -- the
     part that matters for the rule -- how many ACCOUNTS have their MAXIMUM
     insertion instant attained at a clamped record, since only the maximum
     enters conjunct (a).

Emits the per-account maximum instant, whether that maximum is clamped, and the
per-account maximum computed with clamped records excluded, for stage 3b.

ZERO network calls. Reads only.

Out: processed/step7/bb_b/residual.json, processed/step7/bb_b/acct_instants.npz
"""
from __future__ import annotations

import datetime as dt
import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "bb_b"
MISSING = np.iinfo(np.int64).min
DAY = 86400.0
TAU_PULL = float(dt.datetime(2026, 8, 11, tzinfo=dt.timezone.utc).timestamp())
QS = (0.1, 1, 2.5, 5, 10, 25, 50, 75, 90, 95, 97.5, 99, 99.9)


def insert_time(rid, knot_rid, knot_time):
    """Verbatim from src/step5_calibrate.py. The curve is READ, never refitted."""
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def iso(x) -> str:
    return dt.datetime.fromtimestamp(float(x), dt.timezone.utc).isoformat()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    t = time.time()
    res: dict = {"instance": "data-scientist-b", "namespace": "bb_b", "stage": "3a",
                 "api_calls": 0, "adopts": "nothing"}

    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
    meta = json.load(open(P5 / "calibration_meta.json"))
    res["calibration"] = {
        "source": "processed/step5/calibration.npz",
        "status": "READ, NEVER REFITTED",
        "n_knots": int(len(knot_rid)),
        "application": "np.interp(rid, knot_rid, knot_time), verbatim step5_calibrate.insert_time",
        "knot_rid_range": [float(knot_rid[0]), float(knot_rid[-1])],
        "knot_time_range_utc": [iso(knot_time[0]), iso(knot_time[-1])],
        "stored_meta": meta,
    }

    z = np.load(P5 / "full_scan.npz")
    rid, ts, action, user = z["rid"], z["ts"], z["action"], z["user"]
    n_rec = len(rid)
    print(f"records {n_rec:,}  ({time.time() - t:.1f}s)", flush=True)
    tau_rec = insert_time(rid, knot_rid, knot_time)
    print(f"instants interpolated  ({time.time() - t:.1f}s)", flush=True)

    dated = ts != MISSING
    tsf = np.where(dated, ts, 0).astype(np.float64)

    # ---------------- R1: in-sample residual on the fit family ----------------
    fitfam = dated & (action != 0) & (tsf <= TAU_PULL)      # checkin or scrobble
    r = (tau_rec[fitfam] - tsf[fitfam]) / DAY
    res["R1_in_sample_residual_days"] = {
        "definition": "insert_time(rid) - watched_at, on the records the curve was fitted on "
                      "(checkin + scrobble, dated, watched_at <= tau_pull). Their watched_at IS "
                      "their insert time by construction, so this is the calibration's own error.",
        "n": int(fitfam.sum()),
        "in_sample": True,
        "caveat": "IN-SAMPLE. It understates the error on `watch` rows, which the curve was "
                  "deliberately not fitted on and which are the majority of the store.",
        "mean": float(r.mean()),
        "percentiles": {f"p{q}": float(np.percentile(r, q)) for q in QS},
        "abs_percentiles": {f"p{q}": float(np.percentile(np.abs(r), q)) for q in QS},
        "share_abs_le_1d": float(np.mean(np.abs(r) <= 1)),
        "share_abs_le_7d": float(np.mean(np.abs(r) <= 7)),
        "share_abs_le_30d": float(np.mean(np.abs(r) <= 30)),
        "stored_held_out_median_days": meta.get("heldout_median_lag_days"),
        "stored_held_out_abs_le_7d": meta.get("heldout_abs_lag_le_7d"),
        "held_out_note": "the held-out figures are QUOTED from calibration_meta.json, not "
                         "recomputed; recomputing them would require refitting, which is barred.",
    }
    del r
    print(f"R1 done  ({time.time() - t:.1f}s)", flush=True)

    # ---------------- R2: future-dated records --------------------------------
    future = dated & (tsf > tau_rec)
    nf, nd = int(future.sum()), int(dated.sum())
    fd = (tsf - tau_rec)[future] / DAY
    res["R2_future_dated"] = {
        "definition": "watched_at later than the record's own calibrated insertion instant",
        "records_dated": nd, "future_dated": nf,
        "share_pct": 100.0 * nf / nd,
        "claim_0048": {"n": 6_271_584, "of": 27_656_434, "pct": 22.68},
        "verdict": "CONFIRMED" if nf == 6_271_584 else "MEASURED HERE AS ABOVE",
        "excess_days_percentiles": {f"p{q}": float(np.percentile(fd, q)) for q in QS},
        "max_excess_days": float(fd.max()),
        "reading": "a future-dated record is arithmetically impossible for a genuine insert, so "
                   "its excess is a lower bound on the residual at that record. The p50 of the "
                   "excess is the scale at which the curve is wrong for the affected fifth of "
                   "the store.",
    }
    del fd
    print(f"R2 done: {nf:,} of {nd:,}  ({time.time() - t:.1f}s)", flush=True)

    # ---------------- R3: clamping --------------------------------------------
    below = rid < knot_rid[0]
    above = rid > knot_rid[-1]
    res["R3_clamping"] = {
        "records_below_first_knot": int(below.sum()),
        "records_above_last_knot": int(above.sum()),
        "claim_0048_above": 5_094,
        "verdict_above": "CONFIRMED" if int(above.sum()) == 5_094 else "REFUTED",
        "clamp_value_above_utc": iso(knot_time[-1]),
        "direction": "a record above the last knot is pinned to knot_time[-1], so its instant is "
                     "EARLIER than the truth. That lowers max(instant) and pushes TOWARD "
                     "exclusion -- i.e. toward FALSE exclusion.",
    }

    # ---------------- per-account maxima --------------------------------------
    n_users = int(user.max()) + 1
    max_inst = np.full(n_users, -np.inf)
    np.maximum.at(max_inst, user, tau_rec)
    # maximum over UNCLAMPED records only: if it is lower, the max was set by a clamped record
    ok = ~(above | below)
    max_unclamped = np.full(n_users, -np.inf)
    np.maximum.at(max_unclamped, user[ok], tau_rec[ok])
    max_at_clamped = np.zeros(n_users, dtype=bool)
    both = np.isfinite(max_inst) & np.isfinite(max_unclamped)
    max_at_clamped[both] = max_inst[both] > max_unclamped[both]
    max_at_clamped[np.isfinite(max_inst) & ~np.isfinite(max_unclamped)] = True

    # how many accounts hold ANY clamped-above record at all
    holds_above = np.zeros(n_users, dtype=bool)
    holds_above[np.unique(user[above])] = True

    res["R3_clamping"]["accounts_total"] = int(np.isfinite(max_inst).sum())
    res["R3_clamping"]["accounts_holding_a_clamped_above_record"] = int(holds_above.sum())
    res["R3_clamping"]["accounts_whose_MAX_instant_is_set_by_a_clamped_record"] = \
        int(max_at_clamped.sum())
    res["R3_clamping"]["note"] = ("only the per-account MAXIMUM enters conjunct (a), so clamping "
                                  "can only matter where it sets the maximum. That count is the "
                                  "one above; stage 3b intersects it with the excluded pairs.")

    np.savez(OUT / "acct_instants.npz",
             max_inst=max_inst, max_unclamped=max_unclamped,
             max_at_clamped=max_at_clamped, holds_above=holds_above)

    res["elapsed_s"] = time.time() - t
    (OUT / "residual.json").write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items()
                      if k in ("R2_future_dated", "R3_clamping")}, indent=2)[:3000])
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
