"""Step 7 (rerun), instance A2 — the BRACKETING-gap distribution, the threshold it yields,
and the rule applied.

Reference distribution per decisions/0037 SS1: the percentile is taken on the distribution of
gaps that actually bracket tau1, not on the pooled distribution.

Rule shape per decisions/0036 SS2 (STANDS UNCHANGED): for each pair take that pair's own
tau1 = [[T0]] + W*24h, find the last insertion instant at or before tau1 and the first after it,
and test THAT ONE GAP.

W = 108 days, approved 2026-08-12 (decisions/0026). W is not an input to the threshold's
derivation; it only fixes the instant at which the bracketing gap is selected.

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
W_DAYS = 108                 # decisions/0026
PCTL = 99.0                  # decisions/0036 SS1 as amended by 0037 SS1
BACKFILL_D = 180.0           # Step 5 constants, not chosen here
POSTDATE_D = -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]


def percentile_panel(x, q):
    """Every standard reading of 'the q-th percentile', so a convention difference between
    two isolated instances is visible rather than silent."""
    xs = np.sort(np.asarray(x, dtype="float64"))
    n = xs.size
    panel = {}
    for m in ("linear", "lower", "higher", "nearest", "midpoint",
              "inverted_cdf", "averaged_inverted_cdf"):
        try:
            panel[m] = float(np.percentile(xs, q, method=m))
        except (TypeError, ValueError):
            panel[m] = None
    k = int(math.ceil(q / 100.0 * n))
    panel["nearest_rank_ceil"] = float(xs[min(max(k, 1), n) - 1])
    return panel


def main():
    os.makedirs(OUT, exist_ok=True)

    # ---- 1. distinct insertion-instant sequences (from step7_a2_gaps.py) ----
    di = np.load(os.path.join(OUT, "distinct_instants.npz"))
    uids, d_starts, d_ends, d_inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)

    # ---- 2. rebuild the Step 5 waterfall (same construction as approved Step 6) ----
    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)

    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    keep = ~(all_air | the1542)
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w1 = keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    waterfall = [int(w.sum()) for w in (w1, w2, w3, w4, w5)]
    assert waterfall == PUBLISHED_WATERFALL, f"waterfall mismatch: {waterfall}"

    # ---- 3. tau1 per pair -------------------------------------------------
    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    t0_floor = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
                .astype("datetime64[s]").astype("int64").astype("float64"))
    t0_floor[t0_dt.isna().to_numpy()] = np.nan              # [[T0]], UTC midnight
    ok = ~np.isnan(t0_floor)
    assert t0_floor[ok].min() > 0 and t0_floor[ok].max() < 2.2e9, "T0 epoch unit wrong"
    tau1 = t0_floor + W_DAYS * SEC_PER_DAY
    n_tau_nan = int(np.isnan(tau1).sum())

    # ---- 4. bracketing gap per pair ---------------------------------------
    slot = u2slot[p.user_idx.values]
    assert (slot >= 0).all(), "a pair references an account absent from the sweep"
    lo = d_starts[slot]
    hi = d_ends[slot]

    # index of the first distinct instant strictly greater than tau1, within the account
    tt = np.where(np.isnan(tau1), np.inf, tau1)
    idx = np.empty(tt.size, dtype=np.int64)
    CH = 200000
    for a in range(0, tt.size, CH):
        b = min(a + CH, tt.size)
        for j in range(a, b):
            idx[j] = np.searchsorted(d_inst[lo[j]:hi[j]], tt[j], side="right")

    no_before = idx == 0                       # no insertion instant at or before tau1
    no_after = idx == (hi - lo)                # no insertion instant after tau1
    measured = ~no_before & ~no_after
    gap_days = np.full(tt.size, np.nan)
    mi = np.flatnonzero(measured)
    gap_days[mi] = (d_inst[lo[mi] + idx[mi]] - d_inst[lo[mi] + idx[mi] - 1]) / SEC_PER_DAY

    np.savez_compressed(
        os.path.join(OUT, "pair_bracketing.npz"),
        user_idx=p.user_idx.values, show=p.show_trakt_id.values, tau1=tau1,
        gap_days=gap_days, no_before=no_before, no_after=no_after,
        w1=w1, w2=w2, w3=w3, w4=w4, w5=w5,
    )

    # ---- 5. threshold on the bracketing distribution, per population -------
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    pooled_p99 = float(np.percentile(pooled, PCTL))
    pooled_thr = int(math.ceil(pooled_p99))

    levels = [
        ("analysis_population_201900", w1),
        ("has_s2_evidence_178165", w2),
        ("t0_not_contaminated_155131", w3),
        ("completing_record_not_postdated_152126", w4),
        ("w_estimation_sample_128099", w5),
    ]

    res = {}
    for name, mask in levels:
        m = mask & measured
        g = gap_days[m]
        raw = float(np.percentile(g, PCTL))
        thr = int(math.ceil(raw))
        # distinct (account, gap) weighting, as a sensitivity on the weighting convention
        key = pd.DataFrame({"u": p.user_idx.values[m], "g": g}).drop_duplicates()
        raw_d = float(np.percentile(key.g.values, PCTL))
        n_pairs = int(mask.sum())
        n_meas = int(m.sum())
        nb = int((mask & no_before).sum())
        na = int((mask & no_after).sum())

        def apply(t):
            dead_m = int((g >= t).sum())
            live = n_meas - dead_m
            return {
                "threshold_days": t,
                "live": live,
                "not_live_measured_gap": dead_m,
                "not_live_no_instant_after_tau1": na,
                "not_live_no_instant_at_or_before_tau1": nb,
                "not_live_total": dead_m + na + nb,
                "live_share_of_population": round(live / n_pairs, 6),
                "measured_gap_failure_rate": round(dead_m / n_meas, 6),
            }

        res[name] = {
            "n_pairs": n_pairs,
            "n_measured_gap": n_meas,
            "n_no_instant_after_tau1": na,
            "n_no_instant_at_or_before_tau1": nb,
            "bracketing_gap_days": {
                "min": float(g.min()), "median": float(np.median(g)),
                "p75": float(np.percentile(g, 75)), "p90": float(np.percentile(g, 90)),
                "p95": float(np.percentile(g, 95)), "p99": raw,
                "p99_5": float(np.percentile(g, 99.5)),
                "p99_9": float(np.percentile(g, 99.9)),
                "max": float(g.max()), "mean": float(g.mean()),
                "sub_second_share": float((g * SEC_PER_DAY < 1.0).mean()),
            },
            "p99_percentile_panel": percentile_panel(g, PCTL),
            "p99_pair_weighted_raw_days": raw,
            "p99_pair_weighted_ceil_days": thr,
            "p99_distinct_account_gap_weighted_raw_days": raw_d,
            "p99_distinct_account_gap_weighted_ceil_days": int(math.ceil(raw_d)),
            "n_distinct_account_gap_keys": int(len(key)),
            "applied_corrected_threshold": apply(thr),
            "applied_corrected_threshold_uncelinged": {
                "threshold_days": raw,
                "measured_gap_failure_rate": round(float((g >= raw).sum()) / n_meas, 6),
            },
            "applied_withdrawn_pooled_threshold": apply(pooled_thr),
        }
        print(name, "n=", n_pairs, "meas=", n_meas, "p99=", round(raw, 4),
              "-> thr", thr, "| pooled-thr fail rate",
              res[name]["applied_withdrawn_pooled_threshold"]["measured_gap_failure_rate"])

    summary = {
        "step": 7,
        "instance": "a2",
        "api_calls": 0,
        "W_days": W_DAYS,
        "percentile": PCTL,
        "n_pairs_in_table": int(len(p)),
        "n_tau1_undefined": n_tau_nan,
        "step5_waterfall_reproduced": {"computed": waterfall,
                                       "published": PUBLISHED_WATERFALL,
                                       "match": waterfall == PUBLISHED_WATERFALL},
        "pooled_reference_WITHDRAWN": {
            "p99_raw_days": pooled_p99, "p99_ceil_days": pooled_thr,
            "n_gaps": int(pooled.size),
            "median_days": float(np.median(pooled)),
        },
        "by_population": res,
    }
    with open(os.path.join(OUT, "bracketing_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("\nwrote", os.path.join(OUT, "bracketing_summary.json"))


if __name__ == "__main__":
    main()
