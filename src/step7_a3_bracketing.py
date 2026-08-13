"""Step 7 (frozen-spec run), instance A3 — the bracketing-gap distribution on the frozen
reference population, the threshold it yields, and the rule applied.

Frozen by decisions/0038:
  - Reference population: the 152,126 (waterfall line 4). Derivation and application
    populations are IDENTICAL.
  - Weighting: ONE GAP PER PAIR.
  - Percentile: the 99th of the BRACKETING-gap distribution, ceiling per 0025.
  - Rule shape (0036 SS2, stands): the single gap bracketing that pair's own tau1.
  - The threshold IS a function of W. W = 108 d (0026).

Zero API calls.
"""
import json
import math
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/a3")

SEC_PER_DAY = 86400.0
W_DAYS = 108                  # decisions/0026
PCTL = 99.0                   # decisions/0036 SS1 as amended by 0037 SS1
BACKFILL_D = 180.0            # Step 5 constant, not chosen here
POSTDATE_D = -30.0            # Step 5 constant, not chosen here
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
FROZEN_LINE = 3               # 0-based index of 152,126 == waterfall line 4


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


def build_waterfall(p):
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
    return [w1, w2, w3, w4, w5]


def bracketing(p, d_starts, d_ends, d_inst, u2slot, w_days):
    """Return (tau1, gap_days, no_before, no_after) for every row of p at window w_days."""
    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    t0_floor = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
                .astype("datetime64[s]").astype("int64").astype("float64"))
    t0_floor[t0_dt.isna().to_numpy()] = np.nan          # [[T0]] = UTC midnight
    ok = ~np.isnan(t0_floor)
    assert t0_floor[ok].min() > 0 and t0_floor[ok].max() < 2.2e9, "T0 epoch unit wrong"
    tau1 = t0_floor + w_days * SEC_PER_DAY

    slot = u2slot[p.user_idx.values]
    assert (slot >= 0).all(), "a pair references an account absent from the sweep"
    lo = d_starts[slot]
    hi = d_ends[slot]

    tt = np.where(np.isnan(tau1), np.inf, tau1)
    idx = np.empty(tt.size, dtype=np.int64)
    for j in range(tt.size):
        idx[j] = np.searchsorted(d_inst[lo[j]:hi[j]], tt[j], side="right")

    no_before = idx == 0                 # no insertion instant at or before tau1
    no_after = idx == (hi - lo)          # no insertion instant after tau1
    measured = ~no_before & ~no_after
    gap = np.full(tt.size, np.nan)
    mi = np.flatnonzero(measured)
    gap[mi] = (d_inst[lo[mi] + idx[mi]] - d_inst[lo[mi] + idx[mi] - 1]) / SEC_PER_DAY
    return tau1, gap, no_before, no_after


def main():
    os.makedirs(OUT, exist_ok=True)

    di = np.load(os.path.join(OUT, "distinct_instants.npz"))
    uids, d_starts, d_ends, d_inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)

    masks = build_waterfall(p)
    computed = [int(m.sum()) for m in masks]
    assert computed == PUBLISHED_WATERFALL, f"waterfall mismatch: {computed}"
    ref = masks[FROZEN_LINE]
    assert int(ref.sum()) == 152126, "frozen reference population is not 152,126"
    print("waterfall", computed, "-> frozen line 4 =", int(ref.sum()))

    tau1, gap, no_before, no_after = bracketing(
        p, d_starts, d_ends, d_inst, u2slot, W_DAYS)
    measured = ~no_before & ~no_after

    np.savez_compressed(
        os.path.join(OUT, "pair_bracketing_W108.npz"),
        user_idx=p.user_idx.values, show=p.show_trakt_id.values, tau1=tau1,
        gap_days=gap, no_before=no_before, no_after=no_after, ref=ref,
    )

    # ---- reference distribution: bracketing gaps on the 152,126, one gap per pair ----
    m = ref & measured
    g = gap[m]
    raw = float(np.percentile(g, PCTL))
    thr = int(math.ceil(raw))

    n_pairs = int(ref.sum())
    n_meas = int(m.sum())
    n_na = int((ref & no_after).sum())
    n_nb = int((ref & no_before).sum())
    assert n_meas + n_na + n_nb == n_pairs

    dead_m = int((g >= thr).sum())
    live = n_meas - dead_m
    not_live = dead_m + n_na + n_nb

    # sensitivity on the withdrawn weighting convention, reported not adopted
    key = pd.DataFrame({"u": p.user_idx.values[m], "g": g}).drop_duplicates()
    raw_dist = float(np.percentile(key.g.values, PCTL))

    # inertness: share of exclusions done by the measured-gap test, across percentiles
    inert = {}
    for q in (90.0, 95.0, 97.5, 99.0, 99.5, 99.9):
        tq = int(math.ceil(float(np.percentile(g, q))))
        dq = int((g >= tq).sum())
        tot = dq + n_na + n_nb
        inert[str(q)] = {
            "threshold_days": tq,
            "not_live_measured_gap": dq,
            "not_live_edge_cases": n_na + n_nb,
            "not_live_total": tot,
            "measured_gap_share_of_exclusions": round(dq / tot, 6),
            "edge_case_share_of_exclusions": round((n_na + n_nb) / tot, 6),
            "realised_measured_gap_exclusion_rate": round(dq / n_meas, 6),
            "realised_exclusion_rate_of_population": round(tot / n_pairs, 6),
        }

    # the withdrawn pooled-99th basis, reported for continuity with 0037
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    pooled_raw = float(np.percentile(pooled, PCTL))
    pooled_thr = int(math.ceil(pooled_raw))
    pooled_fail = float((g >= pooled_thr).sum()) / n_meas

    # right-censoring diagnostic on the no-instant-after bucket (0038 SS7)
    slot = u2slot[p.user_idx.values]
    last_inst = d_inst[d_ends[slot] - 1]
    na_mask = ref & no_after
    past_sweep = int((tau1[na_mask] > last_inst[na_mask]).sum())

    out = {
        "step": 7,
        "instance": "a3",
        "api_calls": 0,
        "spec": "decisions/0038 (frozen), 0037, 0036 SS2, 0026, 0025",
        "W_days": W_DAYS,
        "percentile": PCTL,
        "reference_population": {
            "name": "waterfall line 4 - completing record not postdated",
            "n_pairs": n_pairs,
            "waterfall_computed": computed,
            "waterfall_published": PUBLISHED_WATERFALL,
            "derivation_equals_application": True,
        },
        "bracketing_gap_distribution_days": {
            "n_gaps_one_per_pair": n_meas,
            "min": float(g.min()),
            "p1": float(np.percentile(g, 1)),
            "p10": float(np.percentile(g, 10)),
            "p25": float(np.percentile(g, 25)),
            "median": float(np.median(g)),
            "p75": float(np.percentile(g, 75)),
            "p90": float(np.percentile(g, 90)),
            "p95": float(np.percentile(g, 95)),
            "p99": raw,
            "p99_5": float(np.percentile(g, 99.5)),
            "p99_9": float(np.percentile(g, 99.9)),
            "max": float(g.max()),
            "mean": float(g.mean()),
            "sub_second_share": float((g * SEC_PER_DAY < 1.0).mean()),
        },
        "p99_percentile_panel": percentile_panel(g, PCTL),
        "threshold": {
            "p99_raw_days": raw,
            "proposed_threshold_days": thr,
            "rounding": "ceiling, decisions/0025",
            "weighting": "one gap per pair (decisions/0038 SS3)",
        },
        "weighting_sensitivity_NOT_ADOPTED": {
            "distinct_account_gap_p99_raw_days": raw_dist,
            "distinct_account_gap_p99_ceil_days": int(math.ceil(raw_dist)),
            "n_distinct_account_gap_keys": int(len(key)),
        },
        "applied": {
            "threshold_days": thr,
            "live": live,
            "not_live_measured_gap": dead_m,
            "not_live_no_instant_after_tau1": n_na,
            "not_live_no_instant_at_or_before_tau1": n_nb,
            "not_live_total": not_live,
            "n_pairs": n_pairs,
            "n_measured_gap": n_meas,
            "realised_exclusion_rate_measured_gap_pairs": round(dead_m / n_meas, 6),
            "realised_exclusion_rate_of_population": round(not_live / n_pairs, 6),
            "live_share_of_population": round(live / n_pairs, 6),
        },
        "inertness_by_percentile": inert,
        "withdrawn_pooled_basis": {
            "pooled_p99_raw_days": pooled_raw,
            "pooled_p99_ceil_days": pooled_thr,
            "n_pooled_gaps": int(pooled.size),
            "pooled_median_days": float(np.median(pooled)),
            "bracketing_pairs_failing_pooled_threshold_rate": round(pooled_fail, 6),
        },
        "no_instant_after_tau1_diagnostic": {
            "n": n_na,
            "of_which_tau1_past_last_insertion_instant_on_account": past_sweep,
            "share": round(past_sweep / n_na, 6) if n_na else None,
        },
    }
    with open(os.path.join(OUT, "bracketing_W108.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in
                      ("threshold", "applied", "withdrawn_pooled_basis")}, indent=2))


if __name__ == "__main__":
    main()
