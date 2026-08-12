"""Step 6 (instance B): derive the window W.

READ ONLY against the data. ZERO network calls.

Spec: task-sheet.md, "Step 6: Derive window W", as amended by
decisions/0024-w-is-the-90th-percentile.md.

  - Estimation sample: the Step 5 clean-record W estimation sample (128,099
    pairs), taken from artifacts/step5-contamination-diagnostics.md Sec 14 and
    reconstructed here with the same masks src/step5_revision5.py used, then
    asserted equal to 128,099.
  - D14 restriction applied ON TOP: bucket C1 only, per the D12 classifier in
    Step 1 Sec 10.0. The frame's cadence_bucket column is used and is
    independently recomputed here from (P, F_d, L2) as a check.
  - Lag = first S2 watch instant - tau0, in days, where tau0 = the UTC-midnight
    instant of T0 = max(S2 finale date, first-pass S1 completion date), per
    Step 1 Sec 6 and Sec 2.4.  The lag is SIGNED and UNTRUNCATED: no clipping,
    no absolute values, no dropped rows.
  - W = the 90th percentile of that lag distribution on C1.
  - The all-shows curve (all five D12 buckets, same 128,099 provenance filter)
    is descriptive only.  The same percentile is read on it to fix Step 13's
    minimum range.  W is never read off it.

Outputs, all under the -b namespace:
  artifacts/step6-lag-distributions-b.png
  artifacts/step6-lag-tail-b.png
  artifacts/step6-w-derivation-b.json
  processed/step6/b/c1_lags.csv          (user-keyed -- stays in processed/)
  processed/step6/b/all_lags.csv         (user-keyed -- stays in processed/)
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
P2 = ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step6" / "b"
ART = ROOT / "artifacts"

# Constants inherited from Step 5 (src/step5_revision5.py). Not re-derived here.
BACKFILL_D = 180.0
POSTDATE_D = -30.0

# Step 5 gate, decisions/0021: these two numbers are taken, not re-derived.
ANALYSIS_POPULATION = 201_900
W_ESTIMATION_SAMPLE = 128_099

# The percentile is fixed by decisions/0024. It is not a free parameter.
PCTL = 90.0

PULL_DATE = np.datetime64("2026-08-11T00:00:00").astype("datetime64[s]").astype(np.int64)
SEED = 20260812
BUCKETS = ["C0", "C1", "C2", "C3", "C4"]


def d12(row) -> str:
    """Step 1 Sec 10.0 D12, first match wins. Recomputed as a check on the frame."""
    P, F, L2 = row.s2_premiere_date, row.s2_finale_date, row.s2_L
    if pd.isna(P) or pd.isna(F) or pd.isna(L2):
        return "C0"
    span = (pd.Timestamp(F) - pd.Timestamp(P)).days
    if span < 0:
        return "C0"
    weekly = (int(L2) - 1) * 7
    if span <= 1:
        return "C1"
    if abs(span - weekly) <= 3:
        return "C2"
    if 1 < span < weekly - 3:
        return "C3"
    if span > weekly + 3:
        return "C4"
    return "C0"


def build() -> tuple[pd.DataFrame, dict]:
    p = pd.read_csv(P5 / "pair_revision5.csv")
    prov = {"pair_table_rows": int(len(p))}

    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    keep = ~(all_air | the1542)
    fs2_bad = has_s2 & (
        (p.first_s2_lag_days.values > BACKFILL_D)
        | (p.first_s2_airdate.values == 1)
        | (p.first_s2_corrupt.values == 1)
    )

    w1 = keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    prov["waterfall"] = [
        {"step": "analysis population", "n": int(w1.sum())},
        {"step": "has S2 evidence", "n": int(w2.sum()), "dropped": int((w1 & ~w2).sum())},
        {"step": "T0 not contaminated", "n": int(w3.sum()), "dropped": int((w2 & ~w3).sum())},
        {"step": "completing record not postdated", "n": int(w4.sum()),
         "dropped": int((w3 & ~w4).sum())},
        {"step": "first S2 watch clean", "n": int(w5.sum()), "dropped": int((w4 & ~w5).sum())},
    ]
    assert int(w1.sum()) == ANALYSIS_POPULATION, (int(w1.sum()), ANALYSIS_POPULATION)
    assert int(w5.sum()) == W_ESTIMATION_SAMPLE, (int(w5.sum()), W_ESTIMATION_SAMPLE)

    s = p[w5].copy()

    frame = pd.read_csv(P2 / "frame.csv")
    frame["bucket_recomputed"] = [d12(r) for r in frame.itertuples()]
    mism = int((frame.bucket_recomputed != frame.cadence_bucket).sum())
    prov["frame_shows"] = int(len(frame))
    prov["d12_recompute_mismatches_vs_frame_column"] = mism
    prov["frame_shows_within_1d_of_a_bucket_boundary"] = int(
        (frame.cadence_boundary_distance_days <= 1).sum())
    assert mism == 0, f"D12 recompute disagrees with frame.cadence_bucket on {mism} shows"

    s = s.merge(frame[["show_trakt_id", "cadence_bucket", "s2_L", "s2_span_days"]],
                on="show_trakt_id", how="left", validate="m:1")
    assert s.cadence_bucket.notna().all()

    # Lag = first S2 watch instant - tau0. tau0 = T0 at 00:00:00Z (Step 1 Sec 2.4).
    tau0 = pd.to_datetime(s.t0).values.astype("datetime64[s]").astype(np.int64)
    s["tau0_epoch"] = tau0
    s["lag_days"] = (s.first_s2_ts.values - tau0) / 86400.0

    # Diagnostic only. Per the spec, NO row is dropped from the lag distribution.
    prov["rows_with_first_s2_watch_at_or_after_tau_pull_NOT_dropped"] = int(
        (s.first_s2_ts.values >= PULL_DATE).sum())
    prov["rows_used"] = int(len(s))
    prov["distinct_shows_in_sample"] = int(s.show_trakt_id.nunique())
    prov["distinct_users_in_sample"] = int(s.user_idx.nunique())
    return s, prov


def pctl_report(x: np.ndarray, q: float) -> dict:
    return {m: float(np.percentile(x, q, method=m))
            for m in ("linear", "lower", "higher", "nearest", "midpoint")}


def bootstrap(df: pd.DataFrame, q: float, rng) -> dict:
    x = df.lag_days.values
    n = len(x)
    B = 2000
    iid = np.percentile(rng.choice(x, size=(B, n), replace=True), q, axis=1)
    out = {"iid": {"B": B,
                   "ci95": [float(v) for v in np.percentile(iid, [2.5, 97.5])],
                   "sd_days": float(iid.std())}}
    for key, label in (("user_idx", "user"), ("show_trakt_id", "show")):
        groups = [g.values for _, g in df.groupby(key).lag_days]
        g = np.array(groups, dtype=object)
        ncl = len(g)
        vals = []
        for _ in range(500):
            idx = rng.integers(0, ncl, ncl)
            vals.append(np.percentile(np.concatenate([g[i] for i in idx]), q))
        out[f"cluster_{label}"] = {
            "B": 500, "n_clusters": int(ncl),
            "ci95": [float(v) for v in np.percentile(vals, [2.5, 97.5])],
            "sd_days": float(np.std(vals)),
        }
    return out


def figures(c1: pd.DataFrame, allsh: pd.DataFrame, w_c1: float, w_all: float,
            neg: dict, lo: float, hi: float) -> None:
    x_c1 = c1.lag_days.values
    x_all = allsh.lag_days.values

    fig, ax = plt.subplots(2, 2, figsize=(15.5, 11))
    fig.suptitle("Step 6 (instance B) — lag from clock start $T_0$ to first S2 episode\n"
                 "signed and untruncated; $W$ = 90th percentile, read on C1 only",
                 fontsize=14, y=0.985)

    # --- A: signed untruncated densities on a symlog axis -------------------
    a = ax[0, 0]
    edges = np.concatenate([
        -np.logspace(np.log10(12000), np.log10(1), 60),
        np.linspace(-1, 1, 9),
        np.logspace(np.log10(1), np.log10(12000), 60)])
    edges = np.unique(edges)
    for x, lab, col in ((x_all, f"all shows (n={len(x_all):,})", "#888888"),
                        (x_c1, f"C1 only (n={len(x_c1):,})", "#1f77b4")):
        h, _ = np.histogram(x, bins=edges)
        a.step(edges[:-1], h / h.sum(), where="post", label=lab, color=col, lw=1.6)
    a.set_xscale("symlog", linthresh=1)
    a.axvline(0, color="k", lw=0.8, ls=":")
    a.axvline(w_c1, color="#d62728", lw=1.8,
              label=f"$W$ = C1 p{PCTL:.0f} = {w_c1:.2f} d")
    a.axvline(w_all, color="#2ca02c", lw=1.4, ls="--",
              label=f"all-shows p{PCTL:.0f} = {w_all:.2f} d (descriptive)")
    a.set_xlabel("lag, days (symlog; negative = started S2 before clock start)")
    a.set_ylabel("share of pairs in bin\n(log-spaced bins; heights are not a density)")
    a.set_title("A. Lag distribution, C1 vs all shows")
    a.legend(fontsize=8.5, loc="upper left")
    a.grid(alpha=0.25)

    # --- B: ECDFs, the percentile read on both curves -----------------------
    b = ax[0, 1]
    for x, lab, col in ((x_all, "all shows", "#888888"), (x_c1, "C1 only", "#1f77b4")):
        xs = np.sort(x)
        b.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", label=lab, color=col, lw=1.6)
    b.set_xscale("symlog", linthresh=1)
    b.axhline(PCTL / 100, color="#d62728", lw=1.2, ls="--")
    b.axvline(w_c1, color="#d62728", lw=1.8)
    b.axvline(w_all, color="#2ca02c", lw=1.4, ls="--")
    b.axvspan(lo, hi, color="#ffcc66", alpha=0.28,
              label=f"Step 13 minimum range [{lo:.2f}, {hi:.2f}] d")
    b.axvline(0, color="k", lw=0.8, ls=":")
    b.set_ylim(0, 1)
    b.set_xlabel("lag, days (symlog)")
    b.set_ylabel("cumulative share of pairs")
    b.set_title(f"B. ECDF — the {PCTL:.0f}th percentile read on each curve\n"
                f"C1 {w_c1:.2f} d   |   all shows {w_all:.2f} d")
    b.legend(fontsize=8.5, loc="upper left")
    b.grid(alpha=0.25)

    # --- C: negative mass by D12 bucket -------------------------------------
    c = ax[1, 0]
    ks = [k for k in BUCKETS]
    share = [100 * neg[k]["share_of_started"] for k in ks]
    cols = ["#bbbbbb" if k != "C1" else "#1f77b4" for k in ks]
    bars = c.bar(ks, share, color=cols)
    for k, bar in zip(ks, bars):
        c.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.0,
               f"{neg[k]['negative']:,}\nof {neg[k]['started']:,}",
               ha="center", va="bottom", fontsize=8.5)
    c.set_ylim(0, max(share) * 1.35 + 2)
    c.set_ylabel("% of started pairs with a NEGATIVE lag")
    c.set_title("C. Negative mass is a cadence artifact, not viewer behaviour\n"
                "(share of started pairs, by D12 bucket)")
    c.grid(alpha=0.25, axis="y")

    # --- D: C1 positive tail, log-log survival ------------------------------
    d = ax[1, 1]
    pos = np.sort(x_c1[x_c1 > 0])
    surv = 1 - np.arange(len(pos)) / len(x_c1)
    d.loglog(pos, surv, color="#1f77b4", lw=1.6, label="C1, P(lag > t)")
    d.axhline(1 - PCTL / 100, color="#d62728", ls="--", lw=1.2,
              label=f"survival = {1 - PCTL / 100:.2f}")
    d.axvline(w_c1, color="#d62728", lw=1.8, label=f"$W$ = {w_c1:.2f} d")
    d.set_xlabel("lag, days (log)")
    d.set_ylabel("P(lag > t)  (log)")
    d.set_title("D. Why 'flattens' had nothing to read:\n"
                "the C1 tail is near scale-free past ~day 7")
    d.legend(fontsize=8.5)
    d.grid(alpha=0.25, which="both")

    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(ART / "step6-lag-distributions-b.png", dpi=150)
    plt.close(fig)

    # --- second figure: linear zoom -----------------------------------------
    fig2, ax2 = plt.subplots(1, 2, figsize=(14, 4.8))
    bins = np.arange(-200, 401, 5)
    for x, lab, col in ((x_all, "all shows", "#888888"), (x_c1, "C1 only", "#1f77b4")):
        ax2[0].hist(x, bins=bins, weights=np.full(len(x), 1 / len(x)),
                    histtype="step", label=lab, color=col, lw=1.6)
    ax2[0].axvline(0, color="k", lw=0.8, ls=":")
    ax2[0].axvline(w_c1, color="#d62728", lw=1.8, label=f"$W$ = {w_c1:.2f} d")
    ax2[0].axvline(w_all, color="#2ca02c", lw=1.4, ls="--", label=f"all-shows p90 = {w_all:.2f} d")
    ax2[0].set_xlabel("lag, days (linear, clipped to [-200, 400] FOR DISPLAY ONLY;\n"
                      "no row is dropped from any computation)")
    ax2[0].set_ylabel("share of pairs per 5-day bin (log)")
    ax2[0].set_yscale("log")
    ax2[0].set_title("Linear-axis zoom on the body of the distribution")
    ax2[0].legend(fontsize=8.5)
    ax2[0].grid(alpha=0.25)

    qs = np.arange(50, 100.0, 0.5)
    ax2[1].plot(qs, np.percentile(x_c1, qs), color="#1f77b4", lw=1.8, label="C1")
    ax2[1].plot(qs, np.percentile(x_all, qs), color="#888888", lw=1.6, label="all shows")
    ax2[1].axvline(PCTL, color="#d62728", lw=1.6, ls="--")
    ax2[1].scatter([PCTL], [w_c1], color="#d62728", zorder=5)
    ax2[1].scatter([PCTL], [w_all], color="#2ca02c", zorder=5)
    ax2[1].set_yscale("symlog", linthresh=1)
    ax2[1].set_xlabel("percentile")
    ax2[1].set_ylabel("lag, days (symlog)")
    ax2[1].set_title("Percentile → days. The curve has no elbow:\n"
                     "the choice of percentile IS the choice of $W$")
    ax2[1].legend(fontsize=8.5)
    ax2[1].grid(alpha=0.25)
    fig2.tight_layout()
    fig2.savefig(ART / "step6-lag-tail-b.png", dpi=150)
    plt.close(fig2)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)

    s, prov = build()
    c1 = s[s.cadence_bucket == "C1"]
    assert len(c1) > 0

    w_c1_methods = pctl_report(c1.lag_days.values, PCTL)
    w_all_methods = pctl_report(s.lag_days.values, PCTL)
    w_c1 = w_c1_methods["linear"]
    w_all = w_all_methods["linear"]

    neg = {}
    for k in BUCKETS:
        sub = s[s.cadence_bucket == k]
        n = int(len(sub))
        nn = int((sub.lag_days < 0).sum())
        neg[k] = {"started": n, "negative": nn,
                  "share_of_started": (nn / n) if n else 0.0,
                  "share_of_all_started_pairs": nn / len(s)}
    neg["TOTAL"] = {"started": int(len(s)), "negative": int((s.lag_days < 0).sum()),
                    "share_of_started": float((s.lag_days < 0).mean()),
                    "share_of_all_started_pairs": float((s.lag_days < 0).mean())}

    c1neg = c1[c1.lag_days < 0]
    d14 = {
        "claim_in_decisions_0003_D14_and_step1_sec9": "every C1 lag is non-negative by construction",
        "claim_status": "FALSE against the data; open item 24 in decisions/README.md; not repaired here",
        "c1_negative_lags": int(len(c1neg)),
        "c1_negative_share": float((c1.lag_days < 0).mean()),
        "binding_term_s1_completion": int((c1neg.binds == "s1").sum()),
        "binding_term_finale": int((c1neg.binds == "finale").sum()),
        "binding_term_tie": int((c1neg.binds == "tie").sum()),
        "finale_binding_within_1_day_utc_skew": int(((c1neg.binds == "finale") & (c1neg.lag_days > -1)).sum()),
        "finale_binding_beyond_1_day_UNEXPLAINED": int(((c1neg.binds == "finale") & (c1neg.lag_days <= -1)).sum()),
        "most_negative_finale_binding_days": float(c1neg[c1neg.binds == "finale"].lag_days.min()),
        "most_negative_any_days": float(c1neg.lag_days.min()),
    }
    # what the negatives are worth to W, measured not assumed
    d14["W_if_c1_negatives_dropped"] = float(np.percentile(c1[c1.lag_days >= 0].lag_days.values, PCTL))
    d14["W_if_c1_negatives_truncated_to_zero"] = float(
        np.percentile(np.clip(c1.lag_days.values, 0, None), PCTL))

    boot = bootstrap(c1, PCTL, rng)

    # --- exposure / right-censoring diagnostic on C1 -------------------------
    # A pair observed for fewer than L days cannot show a lag above L, so the
    # upper tail of the lag distribution is censored by calendar exposure.
    # This is a LIMITATION statement. It does not change W.
    exp_days = (PULL_DATE - c1.tau0_epoch.values) / 86400.0
    cens = {
        "definition": "exposure = (tau_pull - tau0) / 1 day, per C1 pair",
        "median_exposure_days": float(np.median(exp_days)),
        "min_exposure_days": float(exp_days.min()),
        "pairs_with_exposure_below_W": int((exp_days < w_c1).sum()),
        "share_with_exposure_below_W": float((exp_days < w_c1).mean()),
        "p90_by_minimum_exposure_years": {},
    }
    for yrs in (0, 1, 2, 4, 8, 12):
        m = exp_days >= yrs * 365.25
        cens["p90_by_minimum_exposure_years"][str(yrs)] = {
            "n": int(m.sum()),
            "p90_days": float(np.percentile(c1.lag_days.values[m], PCTL)) if m.sum() else None,
        }
    cens["caveat"] = ("longer-exposure pairs are also older shows, so exposure and cohort are "
                      "not separable here; the movement across these rows is an upper bound on "
                      "the censoring effect, not an estimate of it")

    # --- concentration: is the C1 sample a few shows wearing a trench coat? ---
    per_show = c1.groupby("show_trakt_id").size().sort_values(ascending=False)
    conc = {
        "n_shows": int(len(per_show)),
        "top1_share_of_pairs": float(per_show.iloc[0] / len(c1)),
        "top5_share_of_pairs": float(per_show.iloc[:5].sum() / len(c1)),
        "top10_share_of_pairs": float(per_show.iloc[:10].sum() / len(c1)),
        "top20_share_of_pairs": float(per_show.iloc[:20].sum() / len(c1)),
        "median_pairs_per_show": float(per_show.median()),
        "shows_needed_for_half_the_pairs": int(
            np.searchsorted(np.cumsum(per_show.values), len(c1) / 2) + 1),
    }

    lo, hi = sorted([w_c1, w_all])
    step13_union_lo = min(lo, 46.0)
    step13_union_hi = max(hi, 107.0)

    result = {
        "instance": "data-scientist-b",
        "step": 6,
        "status": "PROPOSED — gate, not adopted. The Human Lead approves.",
        "pull_date": "2026-08-11",
        "api_calls": 0,
        "spec": "task-sheet.md Step 6, as amended by decisions/0024-w-is-the-90th-percentile.md",
        "populations": {
            "analysis_population_NOT_used_here": ANALYSIS_POPULATION,
            "W_estimation_sample_taken_from_step5": W_ESTIMATION_SAMPLE,
            "C1_estimation_sample_after_D14": int(len(c1)),
            "C1_share_of_estimation_sample": float(len(c1) / len(s)),
        },
        "provenance": prov,
        "percentile": PCTL,
        "W_days_raw_C1_p90": w_c1,
        "W_days_by_numpy_method": w_c1_methods,
        "W_integer_candidates": {"floor": int(np.floor(w_c1)), "round": int(np.round(w_c1)),
                                 "ceil": int(np.ceil(w_c1))},
        "all_shows_p90_days_DESCRIPTIVE_ONLY": w_all,
        "all_shows_p90_by_numpy_method": w_all_methods,
        "step13_range_from_the_two_curves": [lo, hi],
        "step13_range_union_with_46_107": [step13_union_lo, step13_union_hi],
        "percentile_grid_C1": {str(q): float(np.percentile(c1.lag_days.values, q))
                               for q in (1, 5, 10, 25, 50, 75, 80, 85, 88, 90, 92, 95, 99)},
        "percentile_grid_all_shows": {str(q): float(np.percentile(s.lag_days.values, q))
                                      for q in (1, 5, 10, 25, 50, 75, 80, 85, 88, 90, 92, 95, 99)},
        "sensitivity_of_W_to_the_percentile_convention": {
            str(q): float(np.percentile(c1.lag_days.values, q)) for q in (75, 80, 85, 90, 95)},
        "negative_mass_by_D12_bucket": neg,
        "D14_warrant_defect": d14,
        "sample_adequacy": {
            "n_C1_pairs": int(len(c1)),
            "n_above_p90": int((c1.lag_days > w_c1).sum()),
            "n_distinct_shows": int(c1.show_trakt_id.nunique()),
            "n_distinct_users": int(c1.user_idx.nunique()),
            "bootstrap": boot,
            "show_concentration": conc,
        },
        "right_censoring_diagnostic_C1": cens,
        "C1_shape": {
            "share_lag_lt_0": float((c1.lag_days < 0).mean()),
            "share_lag_in_0_1d": float(((c1.lag_days >= 0) & (c1.lag_days < 1)).mean()),
            "share_lag_in_0_7d": float(((c1.lag_days >= 0) & (c1.lag_days < 7)).mean()),
            "share_lag_in_0_30d": float(((c1.lag_days >= 0) & (c1.lag_days < 30)).mean()),
            "share_lag_ge_365d": float((c1.lag_days >= 365).mean()),
            "days_bought_by_moving_p85_to_p90": float(
                np.percentile(c1.lag_days.values, 90) - np.percentile(c1.lag_days.values, 85)),
        },
        "lag_range_days": {"C1_min": float(c1.lag_days.min()), "C1_max": float(c1.lag_days.max()),
                           "all_min": float(s.lag_days.min()), "all_max": float(s.lag_days.max())},
        "figures": ["artifacts/step6-lag-distributions-b.png", "artifacts/step6-lag-tail-b.png"],
    }

    figures(c1, s, w_c1, w_all, neg, lo, hi)

    cols = ["user_idx", "show_trakt_id", "cadence_bucket", "t0", "binds",
            "first_s2_ts", "lag_days", "s2_L", "s2_span_days"]
    s[cols].to_csv(OUT / "all_lags.csv", index=False)
    c1[cols].to_csv(OUT / "c1_lags.csv", index=False)
    (ART / "step6-w-derivation-b.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
