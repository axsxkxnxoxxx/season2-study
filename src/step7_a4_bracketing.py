"""Step 7 rerun on the corrected spec (decisions/0040), instance A4 — the bracketing-gap
distribution on the POST-D10 population, the threshold it yields, and the rule applied.

What decisions/0040 changed, and is implemented here:
  1. 0036 SS2.3's SECOND edge case is WITHDRAWN. A pair with no insertion instant at or
     before tau1 is LIVE, because 0021 (approved gate 2 of 5) rules that any record inserted
     after the window closed proves the account was alive. Those pairs are returned to the
     population and are never tested.
  2. Derivation moves to AFTER D10. Liveness is applied at Step 8 position 6, right-censoring
     at position 5, so the application population is the 152,126 LESS D10 right-censoring.
     Derive on that, apply to that.
  3. Consequence to be CHECKED, not assumed: with the open-ended share below 1% the 99th
     percentile over the EXTENDED set (measured gaps plus open-ended treated as infinite) is
     finite, so an infinite gap fails a finite threshold on its own and edge case (i) may not
     need to be a separate ruling. Both reference sets are computed here.

Frozen elsewhere and unchanged:
  - Reference population line: the 152,126 (waterfall line 4) — decisions/0038 SS2.
  - Weighting: ONE GAP PER PAIR — decisions/0038 SS3.
  - Percentile: the 99th, ceiling — decisions/0036 SS1 basis as amended by 0037, and 0025.
  - Rule shape: the single gap bracketing that pair's own tau1 — decisions/0036 SS2.
  - Gap unit: consecutive differences of DISTINCT insertion instants — decisions/0037 SS4.
  - The threshold IS a function of W. W = 108 d (decisions/0026).

Zero API calls.
"""
import json
import math
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/a4")

SEC_PER_DAY = 86400.0
W_DAYS = 108                  # decisions/0026
H_DAYS = 91                   # D10, artifacts/step1-outcome-definition.md SS6
PCTL = 99.0                   # 0036 SS1 as amended by 0037 SS1
BACKFILL_D = 180.0            # Step 5 constant, not chosen here
POSTDATE_D = -30.0            # Step 5 constant, not chosen here
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
FROZEN_LINE = 3               # 0-based index of 152,126 == waterfall line 4
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def percentile_panel(x, q):
    """Every standard reading of 'the q-th percentile', so a convention difference between
    two isolated instances is visible rather than silent."""
    xs = np.sort(np.asarray(x, dtype="float64"))
    n = xs.size
    panel = {}
    for m in ("linear", "lower", "higher", "nearest", "midpoint",
              "inverted_cdf", "averaged_inverted_cdf"):
        try:
            v = float(np.percentile(xs, q, method=m))
        except (TypeError, ValueError):
            v = None
        panel[m] = v
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


def t0_floor_epoch(p):
    """[[T0]] — T0 floored to UTC midnight, as epoch seconds."""
    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    v = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
         .astype("datetime64[s]").astype("int64").astype("float64"))
    v[t0_dt.isna().to_numpy()] = np.nan
    ok = ~np.isnan(v)
    assert v[ok].min() > 0 and v[ok].max() < 2.2e9, "T0 epoch unit wrong"
    return v


def d10_mask(t0f, w_days):
    """D10 right-censoring: retain iff [[T0]] + (max(W,91)+H)*24h <= tau_pull."""
    need = (max(w_days, 91) + H_DAYS) * SEC_PER_DAY
    return np.nan_to_num(t0f, nan=np.inf) + need <= TAU_PULL


def bracketing(t0f, user_idx, d_starts, d_ends, d_inst, u2slot, w_days):
    """Return (tau1, gap_days, no_before, no_after) for every row."""
    tau1 = t0f + w_days * SEC_PER_DAY
    slot = u2slot[user_idx]
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


def summarise(g_finite, n_open):
    """Threshold panel for both candidate reference sets."""
    n_m = g_finite.size
    ext = np.concatenate([g_finite, np.full(n_open, np.inf)])
    raw_ext = float(np.percentile(ext, PCTL))
    raw_meas = float(np.percentile(g_finite, PCTL))
    return {
        "extended": {
            "n": int(ext.size),
            "n_measured": int(n_m),
            "n_open_ended": int(n_open),
            "open_ended_share": float(n_open / ext.size),
            "p99_raw_days": raw_ext,
            "p99_is_finite": bool(np.isfinite(raw_ext)),
            "threshold_days": int(math.ceil(raw_ext)) if np.isfinite(raw_ext) else None,
        },
        "measured_only": {
            "n": int(n_m),
            "p99_raw_days": raw_meas,
            "threshold_days": int(math.ceil(raw_meas)),
        },
    }


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
    ref152 = masks[FROZEN_LINE]
    print("waterfall", computed, "-> frozen line 4 =", int(ref152.sum()))

    t0f = t0_floor_epoch(p)
    assert int((ref152 & np.isnan(t0f)).sum()) == 0, "T0 undefined inside the reference line"

    keep10 = d10_mask(t0f, W_DAYS)
    ref = ref152 & keep10
    n_pairs = int(ref.sum())
    print(f"D10 at W={W_DAYS}, H={H_DAYS}: 152,126 -> {n_pairs} "
          f"(removed {int(ref152.sum()) - n_pairs})")

    tau1, gap, no_before, no_after = bracketing(
        t0f, p.user_idx.values, d_starts, d_ends, d_inst, u2slot, W_DAYS)
    measured = ~no_before & ~no_after

    np.savez_compressed(
        os.path.join(OUT, "pair_bracketing_W108.npz"),
        user_idx=p.user_idx.values, show=p.show_trakt_id.values, tau1=tau1,
        gap_days=gap, no_before=no_before, no_after=no_after,
        ref152=ref152, keep_d10=keep10, ref=ref,
    )

    # ---------- reference distribution on the POST-D10 population ----------
    m_meas = ref & measured
    g = gap[m_meas]
    n_meas = int(m_meas.sum())
    n_open = int((ref & no_after).sum())
    n_nobefore = int((ref & no_before).sum())
    assert n_meas + n_open + n_nobefore == n_pairs

    panel = summarise(g, n_open)
    thr = panel["extended"]["threshold_days"]
    assert thr is not None, "the extended-set 99th percentile is infinite"
    thr_meas_only = panel["measured_only"]["threshold_days"]

    def apply_rule(threshold):
        dead_m = int((g >= threshold).sum())
        dead = dead_m + n_open            # an infinite gap fails any finite threshold
        live = n_pairs - dead
        return {
            "threshold_days": int(threshold),
            "live": live,
            "not_live_total": dead,
            "not_live_measured_gap": dead_m,
            "not_live_open_ended_no_instant_after_tau1": n_open,
            "not_live_no_instant_at_or_before_tau1": 0,
            "live_of_which_no_instant_at_or_before_tau1_0021": n_nobefore,
            "realised_rate_vs_measured_gap_pairs": round(dead_m / n_meas, 6),
            "realised_rate_vs_extended_set": round(dead / (n_meas + n_open), 6),
            "realised_rate_vs_post_D10_population": round(dead / n_pairs, 6),
            "live_share_of_post_D10_population": round(live / n_pairs, 6),
        }

    applied = apply_rule(thr)
    applied_meas_only = apply_rule(thr_meas_only)

    # ---------- inertness, measured on THIS population, no invariance claimed ----------
    inert = {}
    for q in (90.0, 95.0, 97.5, 99.0, 99.5, 99.9):
        ext = np.concatenate([g, np.full(n_open, np.inf)])
        rq = float(np.percentile(ext, q))
        tq = int(math.ceil(rq)) if np.isfinite(rq) else None
        if tq is None:
            inert[str(q)] = {"threshold_days": None, "p99_infinite": True}
            continue
        dq = int((g >= tq).sum())
        tot = dq + n_open
        inert[str(q)] = {
            "threshold_days": tq,
            "not_live_measured_gap": dq,
            "not_live_open_ended": n_open,
            "not_live_total": tot,
            "measured_gap_share_of_exclusions": round(dq / tot, 6),
            "evidence_absence_share_of_exclusions": round(n_open / tot, 6),
            "realised_rate_vs_extended_set": round(tot / (n_meas + n_open), 6),
            "realised_rate_vs_post_D10_population": round(tot / n_pairs, 6),
        }

    # ---------- what the two withdrawn/superseded readings would have given ----------
    m152 = ref152 & measured
    g152 = gap[m152]
    n_open152 = int((ref152 & no_after).sum())
    n_nb152 = int((ref152 & no_before).sum())
    pre_d10 = {
        "note": "the superseded run's population: the 152,126 BEFORE D10, with 0036 SS2.3(ii) "
                "scoring the no-pre-tau1 bucket dead",
        "n_pairs": int(ref152.sum()),
        "n_measured_gap": int(g152.size),
        "n_open_ended": n_open152,
        "n_no_instant_at_or_before_tau1": n_nb152,
        "open_ended_share_of_extended_set": round(n_open152 / (g152.size + n_open152), 6),
        "p99_measured_only_raw_days": float(np.percentile(g152, PCTL)),
        "p99_measured_only_ceil_days": int(math.ceil(float(np.percentile(g152, PCTL)))),
    }

    # ---------- weighting sensitivity, reported not adopted ----------
    key = pd.DataFrame({"u": p.user_idx.values[m_meas], "g": g}).drop_duplicates()
    raw_dist = float(np.percentile(key.g.values, PCTL))

    # ---------- withdrawn pooled basis, for continuity with 0037 ----------
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    pooled_raw = float(np.percentile(pooled, PCTL))
    pooled_thr = int(math.ceil(pooled_raw))
    pooled_fail = float((g >= pooled_thr).sum()) / n_meas

    # ---------- is the open-ended bucket censoring or silence, post-D10? ----------
    slot = u2slot[p.user_idx.values]
    last_inst = d_inst[d_ends[slot] - 1]
    na = ref & no_after
    global_sweep_end = float(d_inst.max())
    past_sweep_end = int((tau1[na] > global_sweep_end).sum())
    past_own_last = int((tau1[na] > last_inst[na]).sum())
    past_pull = int((tau1[na] > TAU_PULL).sum())

    out = {
        "step": 7,
        "instance": "a4",
        "api_calls": 0,
        "spec": "decisions/0040 (reopening), 0038 (frozen, SS2.1 as corrected), 0037, "
                "0036 SS2 with SS2.3(ii) WITHDRAWN, 0026, 0025, 0021",
        "W_days": W_DAYS,
        "H_days": H_DAYS,
        "percentile": PCTL,
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "population": {
            "waterfall_computed": computed,
            "waterfall_published": PUBLISHED_WATERFALL,
            "frozen_line_152126": int(ref152.sum()),
            "d10_rule": "[[T0]] + (max(W,91)+H)*24h <= tau_pull",
            "d10_latest_admissible_T0_utc": str(
                np.datetime64(int(TAU_PULL - (max(W_DAYS, 91) + H_DAYS) * SEC_PER_DAY), "s")),
            "d10_removed": int(ref152.sum()) - n_pairs,
            "post_D10_population": n_pairs,
            "post_D10_share_of_152126": round(n_pairs / int(ref152.sum()), 6),
            "derivation_equals_application": True,
        },
        "classes_at_W108": {
            "measured_bracketing_gap": n_meas,
            "open_ended_no_instant_after_tau1": n_open,
            "no_instant_at_or_before_tau1_LIVE_per_0021": n_nobefore,
            "extended_set": n_meas + n_open,
            "total": n_pairs,
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
            "p99": float(np.percentile(g, 99)),
            "p99_5": float(np.percentile(g, 99.5)),
            "p99_9": float(np.percentile(g, 99.9)),
            "max": float(g.max()),
            "mean": float(g.mean()),
            "sub_second_share": float((g * SEC_PER_DAY < 1.0).mean()),
        },
        "threshold_panel": panel,
        "p99_percentile_convention_panel_extended": percentile_panel(
            np.concatenate([g, np.full(n_open, np.inf)]), PCTL),
        "p99_percentile_convention_panel_measured_only": percentile_panel(g, PCTL),
        "applied_extended_reference": applied,
        "applied_measured_only_reference": applied_meas_only,
        "inertness_by_percentile_extended_reference": inert,
        "weighting_sensitivity_NOT_ADOPTED": {
            "distinct_account_gap_p99_raw_days": raw_dist,
            "distinct_account_gap_p99_ceil_days": int(math.ceil(raw_dist)),
            "n_distinct_account_gap_keys": int(len(key)),
        },
        "withdrawn_pooled_basis": {
            "pooled_p99_raw_days": pooled_raw,
            "pooled_p99_ceil_days": pooled_thr,
            "n_pooled_gaps": int(pooled.size),
            "pooled_median_days": float(np.median(pooled)),
            "bracketing_pairs_failing_pooled_threshold_rate": round(pooled_fail, 6),
        },
        "open_ended_bucket_diagnostic_post_D10": {
            "n": n_open,
            "tau1_past_global_sweep_end": past_sweep_end,
            "tau1_past_pull_instant": past_pull,
            "tau1_past_the_accounts_own_last_instant": past_own_last,
            "global_sweep_end_utc": str(np.datetime64(int(global_sweep_end), "s")),
        },
        "pre_D10_comparison_CONTEXT_ONLY": pre_d10,
    }
    with open(os.path.join(OUT, "bracketing_W108.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps({k: out[k] for k in (
        "population", "classes_at_W108", "threshold_panel", "applied_extended_reference",
        "applied_measured_only_reference", "open_ended_bucket_diagnostic_post_D10")},
        indent=2))


if __name__ == "__main__":
    main()
