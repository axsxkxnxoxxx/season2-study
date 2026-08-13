"""Step 7 (rerun), instance A2 — sensitivity sweeps and edge-bucket diagnostics.

(a) percentile sweep on the corrected (bracketing) reference distribution;
(b) W sensitivity of the threshold, because under decisions/0037 the reference distribution is
    selected AT tau1 = [[T0]] + W*24h and therefore contains W;
(c) diagnostics on the two no-measured-gap buckets.

Zero API calls.
"""
import json
import math
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/a2")
SEC_PER_DAY = 86400.0
BACKFILL_D, POSTDATE_D = 180.0, -30.0
W_ADOPTED = 108
W_ARMS = [46, 60, 91, 108, 150, 213]          # decisions/0027 span + the 91-day arm
PCTLS = [90.0, 95.0, 97.5, 99.0, 99.5, 99.9]


def brackets(d_inst, lo, hi, tau1):
    tt = np.where(np.isnan(tau1), np.inf, tau1)
    idx = np.empty(tt.size, dtype=np.int64)
    for j in range(tt.size):
        idx[j] = np.searchsorted(d_inst[lo[j]:hi[j]], tt[j], side="right")
    nb = idx == 0
    na = idx == (hi - lo)
    meas = ~nb & ~na
    g = np.full(tt.size, np.nan)
    mi = np.flatnonzero(meas)
    g[mi] = (d_inst[lo[mi] + idx[mi]] - d_inst[lo[mi] + idx[mi] - 1]) / SEC_PER_DAY
    return g, nb, na, meas


def main():
    di = np.load(os.path.join(OUT, "distinct_instants.npz"))
    uids, d_starts, d_ends, d_inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    w1 = ~(all_air | (t0c & ~has_s2))
    w5 = (w1 & has_s2 & ~t0c & ~postd
          & ~(has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))))

    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    t0_floor = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
                .astype("datetime64[s]").astype("int64").astype("float64"))
    t0_floor[t0_dt.isna().to_numpy()] = np.nan

    slot = u2slot[p.user_idx.values]
    lo, hi = d_starts[slot], d_ends[slot]

    out = {"step": 7, "instance": "a2", "api_calls": 0}

    # ---- (a) percentile sweep at the adopted W ----------------------------
    g, nb, na, meas = brackets(d_inst, lo, hi, t0_floor + W_ADOPTED * SEC_PER_DAY)
    sweep = {}
    for label, mask in (("analysis_population_201900", w1),
                        ("w_estimation_sample_128099", w5)):
        gg = g[mask & meas]
        rows = []
        for q in PCTLS:
            raw = float(np.percentile(gg, q))
            thr = int(math.ceil(raw))
            rows.append({
                "percentile": q,
                "raw_days": round(raw, 4),
                "threshold_days_ceil": thr,
                "measured_gap_failure_rate_at_ceil": round(float((gg >= thr).mean()), 6),
                "not_live_measured_gap": int((gg >= thr).sum()),
            })
        sweep[label] = rows
    out["percentile_sweep_corrected_basis"] = sweep

    # ---- (b) W sensitivity of the threshold ------------------------------
    wsens = {}
    for W in W_ARMS:
        gw, nbw, naw, mw = brackets(d_inst, lo, hi, t0_floor + W * SEC_PER_DAY)
        row = {}
        for label, mask in (("analysis_population_201900", w1),
                            ("w_estimation_sample_128099", w5)):
            gg = gw[mask & mw]
            raw = float(np.percentile(gg, 99.0))
            row[label] = {
                "n_measured_gap": int(gg.size),
                "n_no_instant_after_tau1": int((mask & naw).sum()),
                "n_no_instant_at_or_before_tau1": int((mask & nbw).sum()),
                "median_days": round(float(np.median(gg)), 4),
                "p99_raw_days": round(raw, 4),
                "p99_ceil_days": int(math.ceil(raw)),
            }
        wsens[f"W={W}"] = row
        print("W", W, {k: v["p99_ceil_days"] for k, v in row.items()})
    out["W_sensitivity_of_threshold"] = wsens

    # ---- (c) edge-bucket diagnostics -------------------------------------
    tau1 = t0_floor + W_ADOPTED * SEC_PER_DAY
    first_inst = d_inst[d_starts][slot]
    last_inst = d_inst[d_ends - 1][slot]
    curve_start = float(d_inst.min())
    sweep_end = float(d_inst.max())
    diag = {}
    for label, mask in (("analysis_population_201900", w1),
                        ("w_estimation_sample_128099", w5)):
        m_na = mask & na
        m_nb = mask & nb
        diag[label] = {
            "no_instant_after_tau1": {
                "n": int(m_na.sum()),
                "median_days_tau1_after_account_last_instant":
                    round(float(np.median((tau1[m_na] - last_inst[m_na]) / SEC_PER_DAY)), 2),
                "n_tau1_after_global_sweep_end":
                    int((tau1[m_na] > sweep_end).sum()),
                "share_tau1_after_global_sweep_end":
                    round(float((tau1[m_na] > sweep_end).mean()), 4),
            },
            "no_instant_at_or_before_tau1": {
                "n": int(m_nb.sum()),
                "median_days_tau1_before_account_first_instant":
                    round(float(np.median((first_inst[m_nb] - tau1[m_nb]) / SEC_PER_DAY)), 2),
                "n_tau1_before_calibration_curve_start":
                    int((tau1[m_nb] < curve_start).sum()),
            },
        }
    out["edge_bucket_diagnostics"] = diag
    out["insertion_clock_span_days"] = round((sweep_end - curve_start) / SEC_PER_DAY, 2)

    with open(os.path.join(OUT, "sweeps.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in
                      ("percentile_sweep_corrected_basis", "edge_bucket_diagnostics",
                       "insertion_clock_span_days")}, indent=2))


if __name__ == "__main__":
    main()
