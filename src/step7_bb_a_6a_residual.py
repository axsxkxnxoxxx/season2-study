"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 6a of 8 —
BOUNDING THE CALIBRATION RESIDUAL. Required by 0048 SS9 and never done by anyone.

WHY THIS MATTERS
Conjunct 1 of the rule is a comparison between an INTERPOLATED instant and tau1. If the
calibration reads EARLY, an account that was in fact alive after tau1 is scored silent, and the
pair is FALSELY EXCLUDED. Two facts on the record point that way:
  - 22.68% of dated records claim a watched_at LATER than their own calibrated insertion
    instant (instance B: 6,271,584 of 27,656,434). A genuine record cannot be inserted before
    it was watched, so every one of those is a place where the curve reads early.
  - 5,094 records are clamped ABOVE the calibration range by np.interp, which assigns them the
    curve's last knot time and therefore also reads early.
Both are CONFIRMED OR REFUTED here by measurement, not assumed.

WHAT IS MEASURED
  1. the two figures above, on this store;
  2. the calibration residual r = interp(rid) - watched_at on the fit family
     (checkin + scrobble, dated, <= tau_pull), where watched_at IS the insertion time, in
     total and by rid decile, plus the STORED held-out figures from calibration_meta.json;
  3. per account: max rid, the interpolated last instant, the latest dated watched_at, the
     action of the max-rid record, and whether the max rid is clamped above the curve.

The curve is READ, never refitted (decisions/0029). Measuring the residual of a stored curve is
not a refit: no knot is recomputed and calibration.npz is opened read-only.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/bb_a")

MISSING = np.iinfo(np.int64).min
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
DAY = 86400.0
QS = [0.1, 1, 5, 10, 25, 50, 75, 90, 95, 99, 99.9]


def qd(x):
    return {f"p{q}": round(float(np.percentile(x, q)), 4) for q in QS}


def main():
    scan = np.load(os.path.join(P5, "full_scan.npz"))
    user = scan["user"].astype(np.int64)
    rid = scan["rid"].astype(np.float64)
    ts = scan["ts"].astype(np.float64)
    action = scan["action"]
    n = user.size

    cal = np.load(os.path.join(P5, "calibration.npz"))
    kr = cal["knot_rid"].astype(np.float64)
    kt = cal["knot_time"].astype(np.float64)
    inst = np.interp(rid, kr, kt)

    dated = ts != float(MISSING)
    in_pull = dated & (ts <= TAU_PULL)
    fit_fam = in_pull & (action != 0)          # checkin or scrobble, the calibration's fit set

    # ---- 1. the two figures on the record -------------------------------------------
    claims_later_dated = int((dated & (ts > inst)).sum())
    claims_later_in_pull = int((in_pull & (ts > inst)).sum())
    clamped_above = int((rid > kr[-1]).sum())
    clamped_below = int((rid < kr[0]).sum())
    gap = (ts - inst)[dated & (ts > inst)] / DAY

    # ---- 2. the residual on the fit family ------------------------------------------
    r_fit = (inst[fit_fam] - ts[fit_fam]) / DAY
    dec = np.quantile(rid[fit_fam], np.linspace(0, 1, 11))
    by_decile = []
    for i in range(10):
        lo, hi = dec[i], dec[i + 1]
        sel = fit_fam & (rid >= lo) & (rid <= hi if i == 9 else rid < hi)
        rr = (inst[sel] - ts[sel]) / DAY
        by_decile.append({
            "decile": i + 1,
            "rid_lo": float(lo), "rid_hi": float(hi),
            "instant_lo_utc": str(np.datetime64(int(np.interp(lo, kr, kt)), "s")),
            "instant_hi_utc": str(np.datetime64(int(np.interp(hi, kr, kt)), "s")),
            "n": int(sel.sum()),
            "median_d": round(float(np.median(rr)), 4),
            "p5_d": round(float(np.percentile(rr, 5)), 4),
            "p95_d": round(float(np.percentile(rr, 95)), 4),
            "abs_p95_d": round(float(np.percentile(np.abs(rr), 95)), 4),
            "abs_p99_d": round(float(np.percentile(np.abs(rr), 99)), 4),
        })

    # ---- 3. per-account arrays -------------------------------------------------------
    uids = np.unique(user)
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    u = slot[user]
    max_rid = np.full(uids.size, -np.inf)
    np.maximum.at(max_rid, u, rid)
    last_inst = np.interp(max_rid, kr, kt)
    max_ts = np.full(uids.size, -np.inf)
    np.maximum.at(max_ts, u[in_pull], ts[in_pull])
    # action of each account's max-rid record
    is_max = rid == max_rid[u]
    act_at_max = np.full(uids.size, -1, dtype=np.int64)
    act_at_max[u[is_max]] = action[is_max]
    # residual measured AT the account's own last record, where that record is fit-family
    res_at_max = np.full(uids.size, np.nan)
    sel = is_max & fit_fam
    res_at_max[u[sel]] = (inst[sel] - ts[sel]) / DAY

    np.savez_compressed(os.path.join(OUT, "residual_accounts.npz"),
                        uids=uids, max_rid=max_rid, last_inst=last_inst, max_ts=max_ts,
                        act_at_max=act_at_max, res_at_max=res_at_max,
                        clamped=(max_rid > kr[-1]))

    meta = json.load(open(os.path.join(P5, "calibration_meta.json")))
    out = {
        "step": 7, "instance": "bb_a", "stage": "6a", "api_calls": 0,
        "curve": {"source": "processed/step5/calibration.npz, READ ONLY, never refitted",
                  "knots": int(kr.size),
                  "rid_range": [float(kr[0]), float(kr[-1])],
                  "time_range_utc": [str(np.datetime64(int(kt[0]), "s")),
                                     str(np.datetime64(int(kt[-1]), "s"))],
                  "stored_heldout_median_lag_days": meta["heldout_median_lag_days"],
                  "stored_heldout_abs_lag_le_7d": meta["heldout_abs_lag_le_7d"],
                  "fit_on": meta["fit_on"], "fit_records": meta["fit_records"]},
        "records": {
            "total": int(n),
            "dated": int(dated.sum()),
            "dated_and_le_tau_pull": int(in_pull.sum()),
            "fit_family_checkin_or_scrobble": int(fit_fam.sum()),
        },
        "instance_B_claim_1_watched_at_later_than_calibrated_instant": {
            "claim": "22.68% of dated records, 6,271,584 of 27,656,434",
            "measured_dated_denominator": int(dated.sum()),
            "measured_count_dated": claims_later_dated,
            "measured_pct_dated": round(100.0 * claims_later_dated / dated.sum(), 4),
            "measured_count_dated_and_le_tau_pull": claims_later_in_pull,
            "verdict": ("CONFIRMED" if claims_later_dated == 6271584
                        and int(dated.sum()) == 27656434 else "SEE MEASURED FIGURES"),
            "size_of_the_discrepancy_days": qd(gap),
            "reading": "a genuine record cannot be inserted before it was watched, so each of "
                       "these is a place the curve reads EARLY by at least that much. The "
                       "median discrepancy is the load-bearing number, not the count.",
        },
        "instance_B_claim_2_records_clamped_above_the_curve": {
            "claim": "5,094 records clamped above the calibration range",
            "measured_records_clamped_above": clamped_above,
            "measured_records_clamped_below": clamped_below,
            "verdict": "CONFIRMED" if clamped_above == 5094 else "SEE MEASURED FIGURE",
            "accounts_whose_MAX_rid_is_clamped_above": int((max_rid > kr[-1]).sum()),
            "clamp_value_utc": str(np.datetime64(int(kt[-1]), "s")),
        },
        "calibration_residual_on_the_fit_family": {
            "definition": "r = interp(rid) - watched_at, in days, on checkin+scrobble records "
                          "dated and <= tau_pull, where watched_at IS the insertion time",
            "n": int(fit_fam.sum()),
            "IN_SAMPLE_CAVEAT": "the stored curve was fitted on exactly this family, so these "
                                "residuals are in-sample and UNDERSTATE the true error; the "
                                "stored held-out figures are quoted above beside them",
            "quantiles_days": qd(r_fit),
            "mean_days": round(float(r_fit.mean()), 4),
            "abs_quantiles_days": qd(np.abs(r_fit)),
            "share_abs_le_1d": round(float(np.mean(np.abs(r_fit) <= 1)), 4),
            "share_abs_le_7d": round(float(np.mean(np.abs(r_fit) <= 7)), 4),
            "share_abs_le_30d": round(float(np.mean(np.abs(r_fit) <= 30)), 4),
            "share_reads_early_r_lt_0": round(float(np.mean(r_fit < 0)), 4),
            "by_rid_decile": by_decile,
        },
    }
    with open(os.path.join(OUT, "residual.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
