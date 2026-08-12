"""Step 6: derive the window W.  [INSTANCE A]

READ ONLY. ZERO API CALLS. Reads processed/step5/pair_revision5.csv and
processed/step2/frame.csv only.

FILENAME NOTE, AND WHY IT LOOKS DEFENSIVE
This file was originally written as src/step6_derive_w.py. Step 6 is a
dual-implementation step and both instances share one working tree, so that
name collided: the file, and the artifact and processed paths it wrote, were
overwritten mid-run by the other instance's implementation. Everything this
instance produces is therefore suffixed `-instance-a` / `_instance_a`. The
suffix is a collision guard, nothing more, and the Human Lead should rename
both sides to whatever the diff wants. No file written by the other instance
was read.

WHAT THIS FILE IS FOR

Every figure quoted in artifacts/step6-window-w-instance-a.md is written by this
file into processed/step6/step6_w_instance_a.json, under the key named in that
artifact's certification table. Step 5 carried the same defect three times
(B3 / D3 / F3): a figure in the write-up that no committed code produced.
Nothing is computed in a shell here.

WHAT THE SPEC FIXES, AND WHAT THIS FILE THEREFORE DOES NOT CHOOSE

  * Population: the Step 5 clean-record W estimation sample, 128,099 pairs
    (artifacts/step5-contamination-diagnostics.md §14). It is NOT re-derived
    from principle: the five-line waterfall from step5_revision5.py is
    reproduced verbatim and asserted to equal 128,099, so a difference between
    the two isolated instances cannot be a population difference.
  * Estimation restriction: bucket C1 of the D12 classifier ONLY, on top of the
    128,099 (D14, decisions/0003). Not "binge shows" - the bucket name, read
    from frame.cadence_bucket, which Step 2 already computed.
  * Clock start: T0 = max(S2 finale air date, first-pass S1 completion date),
    Step 1 §6 D1. The spec's "anchor the lag on the S2 finale, not the premiere"
    is therefore satisfied by construction and this file adds nothing to it.
  * "Started S2": the pair has at least one distinct S2 episode whose number is
    a member of E2. That is the `has S2 evidence` line of the waterfall. It is
    deliberately NOT the Step 1 §7 `|A| > 0` test, which is bounded by tau1 and
    therefore by W - using it here would make W a function of W.
  * The all-shows curve is SIGNED and UNTRUNCATED. No clipping, no absolute
    values, no dropped negative rows, and no axis that hides mass without
    saying how much is off-panel.
  * W is read off the C1 curve ONLY. The all-shows curve is descriptive.
  * Step 13's range: the SAME percentile read on both curves.

THE ONE READING THIS FILE HAD TO TAKE, AND IT IS FLAGGED IN THE ARTIFACT

D14 asserts "within the C1 estimation sample there are no negative lags to
truncate". That is false in the data: 689 of the 25,120 C1 pairs have a negative
lag, because T0 is a max() and the S1-completion term can bind after the first
S2 watch (Step 1 §5, the S1-term negative lags D2 counts). The spec states no
rule for them. This file applies the only handling the spec ever states -
signed and untruncated, nothing dropped - and reports the percentile computed
the other way (negatives dropped) alongside, so the Human Lead can see the size
of the reading rather than take it on trust. Both are in the JSON.

LAG UNITS

Step 1 §0: "T0, T1, lags and gaps are whole numbers of days". So the lag is a
whole number of UTC calendar days, date(first S2 watched_at) - T0, which is
identically floor((watched_at - tau0) / 24h) and is negative where the first S2
watch precedes the clock start.
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
P2 = ROOT / "processed" / "step2"
P5 = ROOT / "processed" / "step5"
P6 = ROOT / "processed" / "step6"
ART = ROOT / "artifacts"

SUF = "instance_a"
SUF_D = "instance-a"

# Step 5 Layer 1 constants, restated so the waterfall below is verbatim.
BACKFILL_D = 180.0
POSTDATE_D = -30.0
TAU_PULL = np.datetime64("2026-08-11")           # decisions/0011
EXPECTED_ANALYSIS_POPULATION = 201_900
EXPECTED_W_SAMPLE = 128_099

PCT = 90                                          # the percentile, stated once
BUCKETS = ["C0", "C1", "C2", "C3", "C4"]          # D12, all five, none pooled


def load():
    p = pd.read_csv(P5 / "pair_revision5.csv", low_memory=False)
    frame = pd.read_csv(P2 / "frame.csv")
    p["cadence_bucket"] = p.show_trakt_id.map(
        frame.set_index("show_trakt_id").cadence_bucket)
    return p, frame


def w_sample_mask(p: pd.DataFrame):
    """Verbatim reproduction of the step5_revision5.py waterfall. Not a re-derivation."""
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    final_keep = ~(all_air | the1542)
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w1 = final_keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    waterfall = [
        {"step": "analysis population", "n": int(w1.sum())},
        {"step": "has S2 evidence", "n": int(w2.sum()), "dropped": int((w1 & ~w2).sum())},
        {"step": "T0 not contaminated", "n": int(w3.sum()), "dropped": int((w2 & ~w3).sum())},
        {"step": "completing record not postdated", "n": int(w4.sum()),
         "dropped": int((w3 & ~w4).sum())},
        {"step": "first S2 watch clean", "n": int(w5.sum()), "dropped": int((w4 & ~w5).sum())},
    ]
    assert w1.sum() == EXPECTED_ANALYSIS_POPULATION, w1.sum()
    assert w5.sum() == EXPECTED_W_SAMPLE, w5.sum()
    return w5, waterfall


def lag_days(p: pd.DataFrame) -> np.ndarray:
    t0 = pd.to_datetime(p.t0).values.astype("datetime64[D]")
    first = (pd.to_datetime(p.first_s2_ts, unit="s", utc=True)
             .dt.tz_localize(None).values.astype("datetime64[D]"))
    return (first - t0).astype("timedelta64[D]").astype(float)


def quantile_all_conventions(x: np.ndarray, q: float) -> dict:
    return {m: float(np.percentile(x, q, method=m))
            for m in ("linear", "lower", "higher", "nearest", "midpoint")}


def order_stat_ci(x_sorted: np.ndarray, q: float) -> tuple:
    """Distribution-free 95% CI for a quantile, normal approximation to the rank."""
    n = len(x_sorted)
    se = np.sqrt(n * q * (1 - q))
    lo = max(1, int(np.floor(n * q - 1.96 * se)))
    hi = min(n, int(np.ceil(n * q + 1.96 * se)))
    return float(x_sorted[lo - 1]), float(x_sorted[hi - 1]), lo, hi


def main():
    P6.mkdir(parents=True, exist_ok=True)
    out = {}
    p, frame = load()
    w5, waterfall = w_sample_mask(p)
    out["population"] = {
        "source": "artifacts/step5-contamination-diagnostics.md §14, reproduced verbatim",
        "waterfall": waterfall,
        "W_estimation_sample": int(w5.sum()),
        "analysis_population_NOT_USED_HERE": EXPECTED_ANALYSIS_POPULATION,
    }

    lag = lag_days(p)
    cad = p.cadence_bucket.values
    c1 = w5 & (cad == "C1")

    out["frame_cadence_shows"] = {b: int((frame.cadence_bucket == b).sum()) for b in BUCKETS}
    out["estimation_sample_pairs_by_bucket"] = {b: int((w5 & (cad == b)).sum()) for b in BUCKETS}
    out["estimation_sample_pairs_unclassified"] = int((w5 & pd.isna(cad)).sum())

    x = np.sort(lag[c1])            # C1 curve   - W is read off THIS one
    a = np.sort(lag[w5])            # all-shows  - descriptive only, signed, untruncated

    # ---------------- the chosen percentile, on the C1 curve -----------------
    w_c1 = float(np.percentile(x, PCT))
    w_all = float(np.percentile(a, PCT))
    W = int(round(w_c1))
    out["W"] = {
        "percentile": PCT,
        "curve_read": "C1 only (D14). The all-shows curve is descriptive and W is never read off it.",
        "W_days": W,
        "C1_percentile_value_days": w_c1,
        "C1_all_quantile_conventions": quantile_all_conventions(x, PCT),
        "n_C1": int(len(x)),
    }

    # ---------------- Step 13's range: same percentile, both curves ----------
    out["step13_W_range"] = {
        "percentile": PCT,
        "all_shows_days": w_all,
        "C1_days": w_c1,
        "range_days": [int(round(min(w_all, w_c1))), int(round(max(w_all, w_c1)))],
        "all_shows_all_quantile_conventions": quantile_all_conventions(a, PCT),
        "n_all_shows": int(len(a)),
        "meaning": ("the size of the D14 transfer assumption; Step 13 must cover at least "
                    "this interval"),
    }

    # ---------------- percentile tables (published as an aggregate CSV) ------
    grid = [50, 60, 70, 75, 80, 82, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
            96, 97, 98, 99]
    rows = []
    for q in grid:
        vc1, va = float(np.percentile(x, q)), float(np.percentile(a, q))
        rows.append({"percentile": q, "C1_lag_days": vc1, "all_shows_lag_days": va})
    tab = pd.DataFrame(rows)
    tab["C1_marginal_days_per_point"] = tab.C1_lag_days.diff() / tab.percentile.diff()
    tab.round(2).to_csv(ART / f"step6-lag-percentiles-{SUF_D}.csv", index=False)
    out["percentile_table"] = tab.round(3).to_dict(orient="records")

    # ---------------- the flattening diagnostic ------------------------------
    # Coverage per additional day, as a share of the C1 started population.
    # The band is PROPORTIONAL to d - [d/1.3, d*1.3) - not a fixed 31 days. A
    # fixed window is wrong on a heavy tail twice over: near d = 0 it smears the
    # day-0 spike (42.5% of the sample) across the first fortnight and invents a
    # plateau that is not in the data, and far out it averages over a range where
    # the rate has fallen by an order of magnitude. This is the "curve flattens"
    # claim made checkable: at W the marginal day recruits fewer than 1 starter
    # in 2,000.
    def rate_at(d):
        lo, hi = d / 1.3, d * 1.3
        if lo < 0.5:
            return float("nan")
        return float(((x >= lo) & (x < hi)).sum()) / (hi - lo) / len(x)

    out["flattening"] = {
        "definition": ("marginal recruitment rate at lag d = share of the C1 started population "
                       "whose first S2 watch falls in the band [d/1.3, d*1.3), per day of that "
                       "band. Band proportional to d, so the day-0 spike cannot leak into it."),
        "rate_pct_per_day": {str(d): round(100 * rate_at(d), 4)
                             for d in (7, 14, 30, 45, 60, 75, 90, 107, 120, 150, 180, 270, 365)},
        "rate_at_W_pct_per_day": round(100 * rate_at(W), 4),
        "one_in_N_starters_per_extra_day_at_W": int(round(1.0 / rate_at(W))),
        "coverage_at_W_pct": round(100 * float((x <= W).mean()), 3),
        "days_to_buy_next_point_at_W": float(np.percentile(x, PCT + 1) - np.percentile(x, PCT)),
        "days_from_W_to_P99": float(np.percentile(x, 99) - w_c1),
        "max_C1_lag_days": float(x.max()),
        "honest_caveat": ("past roughly day 7 the C1 density is close to scale-free "
                          "(log-log slope near -1.2 to -1.5 across every decade), so there is "
                          "no break in the DENSITY to read. 'Flattens' is a statement about "
                          "the coverage curve: what an extra day of window buys."),
    }
    # log-log slope of the tail, per band, so the caveat above is a number
    slopes = {}
    for lo, hi in ((7, 14), (14, 30), (30, 60), (60, 90), (90, 120), (120, 180),
                   (180, 270), (270, 365), (365, 730), (730, 1460)):
        r = float(((x >= lo) & (x < hi)).sum()) / (hi - lo)
        slopes[f"[{lo},{hi})"] = {"per_day": round(r, 3), "n": int(((x >= lo) & (x < hi)).sum())}
    ks = list(slopes)
    for i in range(1, len(ks)):
        (l0, h0), (l1, h1) = [tuple(int(v) for v in k.strip("[)").split(","))
                              for k in ks[i - 1:i + 1]]
        r0, r1 = slopes[ks[i - 1]]["per_day"], slopes[ks[i]]["per_day"]
        if r0 > 0 and r1 > 0:
            slopes[ks[i]]["loglog_slope_vs_prev"] = round(
                float(np.log(r1 / r0) / np.log(((l1 + h1) / 2) / ((l0 + h0) / 2))), 2)
    out["flattening"]["tail_bands"] = slopes

    # ---------------- is the C1 sample large enough for P90? ----------------
    ci = {}
    for q in (0.85, 0.90, 0.95, 0.99):
        lo, hi, rl, rh = order_stat_ci(x, q)
        ci[f"P{int(q * 100)}"] = {
            "value_days": float(np.percentile(x, q * 100)),
            "ci95_days": [lo, hi],
            "rank_interval": [rl, rh],
            "n_above": int((x > np.percentile(x, q * 100)).sum()),
        }
    out["sample_adequacy"] = {
        "n_C1": int(len(x)),
        "method": "distribution-free order-statistic 95% interval, normal approximation to the rank",
        "quantile_cis": ci,
    }

    # ---------------- negative mass, all five buckets ------------------------
    neg = {}
    for b in BUCKETS:
        m = w5 & (cad == b)
        n = int(m.sum())
        k = int((lag[m] < 0).sum()) if n else 0
        neg[b] = {"started_pairs": n, "negative_lag_pairs": k,
                  "share_of_bucket_pct": round(100 * k / n, 2) if n else None,
                  "share_of_all_started_pct": round(100 * k / int(w5.sum()), 2),
                  "median_negative_lag_days": float(np.median(lag[m][lag[m] < 0])) if k else None}
    neg["ALL"] = {"started_pairs": int(w5.sum()),
                  "negative_lag_pairs": int((a < 0).sum()),
                  "share_of_bucket_pct": round(100 * float((a < 0).mean()), 2),
                  "share_of_all_started_pct": round(100 * float((a < 0).mean()), 2),
                  "median_negative_lag_days": float(np.median(a[a < 0]))}
    out["negative_mass_by_D12_bucket"] = neg

    # ---------------- the flagged reading: negatives kept vs dropped --------
    xp, ap = x[x >= 0], a[a >= 0]
    out["negatives_reading"] = {
        "adopted": "signed and untruncated, nothing dropped, on both curves",
        "D14_claim": "C1 has no negative lags by construction",
        "observed_C1_negatives": int((x < 0).sum()),
        "D14_claim_status": "FALSIFIED in the data - see artifact §6",
        "C1_P90_as_adopted_days": w_c1,
        "C1_P90_if_negatives_dropped_days": float(np.percentile(xp, PCT)),
        "all_shows_P90_as_adopted_days": w_all,
        "all_shows_P90_if_negatives_dropped_days": float(np.percentile(ap, PCT)),
    }

    # ---------------- right-censoring of the lag itself ---------------------
    t0d = pd.to_datetime(p.t0).values.astype("datetime64[D]")
    expo = (TAU_PULL - t0d).astype("timedelta64[D]").astype(float)
    cens = {}
    for lim in (0, 365, 730, 1460, 2920):
        m = c1 & (expo >= lim)
        cens[f"exposure_ge_{lim}d"] = {
            "n": int(m.sum()),
            "P85": float(np.percentile(lag[m], 85)),
            "P90": float(np.percentile(lag[m], 90)),
            "P95": float(np.percentile(lag[m], 95)),
        }
    cens["C1_pairs_with_exposure_below_W"] = int((expo[c1] < W).sum())
    cens["C1_pairs_with_exposure_below_W_pct"] = round(100 * float((expo[c1] < W).mean()), 2)
    cens["direction"] = ("a pair whose T0 is recent can only contribute a short lag, and a pair "
                         "that would have started later than the pull cutoff is absent from the "
                         "sample entirely, so the observed lag distribution UNDERSTATES the tail "
                         "and W = P90 is a LOW estimate. Not corrected: the long-exposure subset "
                         "is also an older-show, older-cohort subset, so the gap is censoring "
                         "and cohort together and this step cannot separate them.")
    out["censoring_sensitivity"] = cens

    # ---------------- coverage of the all-shows curve at W ------------------
    out["coverage_at_W"] = {
        "W_days": W,
        "C1_pct_started_within_W": round(100 * float((x <= W).mean()), 2),
        "all_shows_pct_started_within_W": round(100 * float((a <= W).mean()), 2),
        "by_bucket_pct_started_within_W": {
            b: (round(100 * float((lag[w5 & (cad == b)] <= W).mean()), 2)
                if (w5 & (cad == b)).sum() else None) for b in BUCKETS},
    }

    figure(x, a, W, w_all, rate_at, neg)

    (P6 / f"step6_w_{SUF}.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in
                      ("W", "step13_W_range", "sample_adequacy",
                       "negative_mass_by_D12_bucket", "negatives_reading")}, indent=2))


def figure(x, a, W, w_all, rate_at, neg):
    fig = plt.figure(figsize=(15.5, 11.5))
    gs = fig.add_gridspec(2, 2, hspace=0.34, wspace=0.24)

    # (a) coverage curves, full signed range, symlog x so nothing is off-panel
    ax = fig.add_subplot(gs[0, 0])
    for arr, lab, col in ((a, f"all shows (n={len(a):,})", "#888888"),
                          (x, f"C1 only (n={len(x):,})", "#1f77b4")):
        ax.plot(arr, np.arange(1, len(arr) + 1) / len(arr) * 100, lw=2, color=col, label=lab)
    ax.set_xscale("symlog", linthresh=1)
    ax.axvline(W, color="#d62728", lw=1.6)
    ax.axvline(w_all, color="#d62728", lw=1.2, ls=":")
    ax.axhline(90, color="k", lw=0.7, ls="--")
    ax.plot([w_all, W], [90, 90], "o", color="#d62728", ms=5)
    ax.annotate(f"W = {W} d\nP90 on C1", (W, 90), xytext=(700, 58),
                color="#d62728", fontsize=9.5, fontweight="bold", ha="center",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.3))
    ax.annotate(f"same P90 on all shows = {w_all:.0f} d\n"
                f"descriptive only — never used to set W.\n"
                f"[{w_all:.0f}, {W}] is Step 13's minimum range.",
                (w_all, 90), xytext=(-9000, 38), color="#d62728", fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1))
    ax.set_xlabel("lag, clock start T0 to first S2 episode (days, SIGNED, symlog)")
    ax.set_ylabel("cumulative % of started pairs")
    ax.set_title("(a) Lag coverage. Signed, untruncated, full range on both curves.",
                 fontsize=11, loc="left")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.25)

    # (b) linear zoom, with the off-panel mass stated in numbers
    ax = fig.add_subplot(gs[0, 1])
    for arr, lab, col in ((a, "all shows", "#888888"), (x, "C1 only", "#1f77b4")):
        ax.plot(arr, np.arange(1, len(arr) + 1) / len(arr) * 100, lw=2, color=col, label=lab)
    ax.set_xlim(-200, 400)
    ax.axvline(W, color="#d62728", lw=1.6)
    ax.axvline(0, color="k", lw=0.8)
    ax.axhline(90, color="k", lw=0.7, ls="--")
    off_lo_a, off_hi_a = float((a < -200).mean()) * 100, float((a > 400).mean()) * 100
    off_lo_x, off_hi_x = float((x < -200).mean()) * 100, float((x > 400).mean()) * 100
    ax.set_title("(b) Linear zoom. This is an axis limit, not a truncation:\n"
                 f"off-panel all shows {off_lo_a:.1f}% left / {off_hi_a:.1f}% right; "
                 f"C1 {off_lo_x:.1f}% left / {off_hi_x:.1f}% right.",
                 fontsize=10, loc="left")
    ax.set_xlabel("lag (days, signed)")
    ax.set_ylabel("cumulative % of started pairs")
    ax.legend(loc="upper left", fontsize=9)
    ax.grid(alpha=0.25)

    # (c) the flattening diagnostic
    ax = fig.add_subplot(gs[1, 0])
    d = np.unique(np.round(np.logspace(np.log10(1), np.log10(1500), 140)).astype(int))
    r = np.array([rate_at(float(v)) for v in d]) * 100
    ok = np.isfinite(r) & (r > 0)
    ax.loglog(d[ok], r[ok], lw=1.7, color="#1f77b4")
    ax.axvline(W, color="#d62728", lw=1.6)
    ax.axhline(0.05, color="#2ca02c", lw=1.2, ls="--")
    ax.plot([W], [rate_at(float(W)) * 100], "o", color="#d62728", ms=7, zorder=5)
    ax.text(1.15, 0.058, "0.05 %/day = 1 more starter in 2,000\nper extra day of window",
            color="#2ca02c", fontsize=8.5, va="bottom")
    ax.annotate(f"W = {W} d\n{rate_at(float(W)) * 100:.3f} %/day", (W, rate_at(float(W)) * 100),
                xytext=(190, 1.2), color="#d62728", fontsize=9, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#d62728", lw=1.2))
    ax.set_xlabel("lag (days, positive part)")
    ax.set_ylabel("% of C1 started pairs recruited per extra day\n(band [d/1.3, d×1.3))")
    ax.set_title("(c) What one more day of window buys, C1. Past ~day 7 this is close to a\n"
                 "straight line — the tail is scale-free, with no break to read. So 'the curve\n"
                 "flattens' is a claim about COVERAGE, not about a break in the density.",
                 fontsize=10, loc="left")
    ax.grid(alpha=0.25, which="both")

    # (d) negative mass by D12 bucket
    ax = fig.add_subplot(gs[1, 1])
    bs = ["C0", "C1", "C2", "C3", "C4"]
    shares = [neg[b]["share_of_bucket_pct"] or 0.0 for b in bs]
    counts = [neg[b]["negative_lag_pairs"] for b in bs]
    tot = [neg[b]["started_pairs"] for b in bs]
    bars = ax.bar(bs, shares, color=["#cccccc", "#1f77b4", "#888888", "#888888", "#888888"])
    for b_, s, c, t in zip(bars, shares, counts, tot):
        ax.text(b_.get_x() + b_.get_width() / 2, s + 0.9,
                f"{c:,}\nof {t:,}" if t else "no shows\nin frame",
                ha="center", fontsize=8.5)
    ax.axhline(neg["ALL"]["share_of_bucket_pct"], color="#d62728", lw=1.2, ls="--")
    ax.text(-0.42, neg["ALL"]["share_of_bucket_pct"] + 1.0,
            f"pooled, all shows: {neg['ALL']['share_of_bucket_pct']:.1f}%  "
            f"({neg['ALL']['negative_lag_pairs']:,} of {neg['ALL']['started_pairs']:,})",
            color="#d62728", fontsize=8.5, ha="left")
    ax.set_ylim(0, max(shares) * 1.40)
    ax.set_ylabel("% of the bucket's started pairs with a NEGATIVE lag")
    ax.set_title("(d) The negative mass is a cadence artifact. It tracks release span,\n"
                 "not viewer behaviour - which is why W is estimated on C1 alone.",
                 fontsize=10, loc="left")
    ax.grid(alpha=0.25, axis="y")

    fig.suptitle(
        f"Step 6 [instance A] - lag from clock start to first S2 episode.  "
        f"W = {W} days = P{PCT} of the C1 curve.  "
        f"Estimation sample 128,099 clean pairs (Step 5 §14); C1 subset 25,120.",
        fontsize=12.5, y=0.985)
    fig.savefig(ART / f"step6-lag-distribution-{SUF_D}.png", dpi=155, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
