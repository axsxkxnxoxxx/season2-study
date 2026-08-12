"""Step 6: derive the window W.

READ ONLY. Zero network calls. Every figure quoted in
artifacts/step6-window-w.md is written by this file into
artifacts/step6-w-derivation.json under the key named in the artifact's
reproduction table.

WHAT THIS FILE DOES, AND THE SPEC LINE EACH PART ANSWERS
(task-sheet.md "Step 6: Derive window W")

1. Population. The estimation sample is the Step 5 clean-record sample of
   128,099 pairs (decisions/0021, ruling 1). It is not re-derived from the raw
   scan here: the five Boolean masks below are copied verbatim from
   src/step5_revision5.py, the committed code that produced the published
   waterfall 201,900 -> 178,165 -> 155,131 -> 152,126 -> 128,099. The
   reproduction asserts both endpoints against the published numbers and fails
   loudly if either moves.

2. D14 on top. The C1 restriction (cadence_bucket == "C1" in the Step 2 frame,
   per the D12 classifier) is applied ON TOP of the 128,099, not instead of it.

3. Lag. lag = (first S2 watch instant - tau0) / 86400, with
   tau0 = midnight UTC of T0 and T0 = max(S2 finale date, S1 completion date)
   as already computed and stored by src/step5_t0_binding.py. The finale anchor
   is therefore inherited, not re-decided here.

4. Flattening criterion, stated once and applied to both curves. See CRITERION
   below.

5. All-shows curve: SIGNED and UNTRUNCATED. No clipping, no absolute values, no
   dropped negative rows anywhere in this file. The histogram panel uses edge
   bins that accumulate all extreme mass so that no row is invisible, and the
   ECDF panel is drawn over the full signed support.

NOTHING HERE IS ADOPTED. Step 6 is a gate.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
P6 = ROOT / "processed" / "step6"
ART = ROOT / "artifacts"

DAY = 86400.0
TAU_PULL = np.datetime64("2026-08-11")          # decisions/0011
BACKFILL_D = 180.0                              # Step 5 Layer 1 constant
POSTDATE_D = -30.0                              # Step 5 Layer 1 constant
PUBLISHED_ANALYSIS_POP = 201900                 # artifacts/step5-...md Sec 14
PUBLISHED_W_SAMPLE = 128099                     # artifacts/step5-...md Sec 14
BOOT_B = 2000
BOOT_SEED = 20260812

# CRITERION, stated once and applied identically to every curve and every arm.
#
#   Walk the coverage curve F(w) = P(lag < w) in consecutive 7-day blocks
#   starting at day 0. The curve has FLATTENED at the first block whose gain in
#   coverage is below GAIN_PP_PER_WEEK percentage points AND which no later
#   block exceeds. W is then read as the whole percentile of the lag
#   distribution lying inside that block, and W in days is that percentile's
#   value rounded UP to a whole day.
#
# Seven-day blocks rather than single days because a one-day slope on this
# curve wanders above and below any threshold (it crosses 0.10 pp/day down at
# day 56 and back up at day 66), so a first-crossing rule on daily slope is not
# reproducible. The threshold itself is a convention; the sweep over
# GAIN_SWEEP is published so its weight is visible rather than assumed.
GAIN_PP_PER_WEEK = 1.0
GAIN_SWEEP = (2.0, 1.5, 1.0, 0.75, 0.5, 0.25)
MAX_DAY = 3000  # coverage grid horizon; beyond the largest observed C1 lag


def parse_bool(s):
    return s.astype(str).str.lower().isin(("true", "1")).values


# --------------------------------------------------------------------------
# population
# --------------------------------------------------------------------------
def load_pairs():
    p = pd.read_csv(P5 / "pair_revision5.csv")
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    p = p.merge(
        frame[["show_trakt_id", "cadence_bucket", "s2_L", "s2_span_days"]],
        on="show_trakt_id", how="left", validate="m:1")
    assert p.cadence_bucket.notna().all(), "every frame show must carry a D12 bucket"

    # masks copied verbatim from src/step5_revision5.py
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
    waterfall = [int(w1.sum()), int(w2.sum()), int(w3.sum()), int(w4.sum()), int(w5.sum())]
    assert waterfall == [201900, 178165, 155131, 152126, 128099], (
        f"Step 5 waterfall does not reproduce: {waterfall}")

    t0 = pd.to_datetime(p.t0).values.astype("datetime64[s]").astype(np.int64)
    p["lag_days"] = (p.first_s2_ts.values - t0) / DAY
    p["exposure_days"] = (TAU_PULL.astype("datetime64[s]").astype(np.int64) - t0) / DAY
    p["in_w_sample"] = w5
    return p, waterfall


# --------------------------------------------------------------------------
# curves
# --------------------------------------------------------------------------
def coverage(lag, grid):
    """F(w) = P(lag < w), the one-sided in-window test of Step 1 Sec 2.4."""
    s = np.sort(lag)
    return np.searchsorted(s, grid, side="left") / len(s)


def weekly_blocks(lag, n_blocks=60):
    grid = np.arange(0, 7 * n_blocks + 1)
    cov = coverage(lag, grid) * 100
    out = []
    for k in range(n_blocks):
        a, b = 7 * k, 7 * k + 7
        out.append({"block": k, "day_start": a, "day_end": b,
                    "coverage_end_pct": round(float(cov[b]), 4),
                    "gain_pp": round(float(cov[b] - cov[a]), 4)})
    return out


def flattening_block(blocks, thr):
    """First block under thr that no later block exceeds. None if never."""
    gains = np.array([b["gain_pp"] for b in blocks])
    for i in range(len(blocks)):
        if gains[i] < thr and (i + 1 == len(gains) or gains[i + 1:].max() <= gains[i]):
            return blocks[i]
    return None


def whole_percentile_in_block(lag, blk):
    """The whole percentiles whose value falls inside [day_start, day_end)."""
    qs = np.arange(1, 100)
    vals = np.percentile(lag, qs)
    inside = [(int(q), float(v)) for q, v in zip(qs, vals)
              if blk["day_start"] <= v < blk["day_end"]]
    return inside


def _groups(keys, vals):
    order = np.argsort(keys, kind="stable")
    k_sorted, v_sorted = keys[order], vals[order]
    bounds = np.flatnonzero(np.r_[True, k_sorted[1:] != k_sorted[:-1], True])
    return [v_sorted[bounds[i]:bounds[i + 1]] for i in range(len(bounds) - 1)]


def cluster_bootstrap(keys, vals, qs, B=BOOT_B, seed=BOOT_SEED):
    rng = np.random.default_rng(seed)
    groups = _groups(keys, vals)
    n = len(groups)
    draws = np.empty((B, len(qs)))
    for b in range(B):
        pick = rng.integers(0, n, n)
        s = np.concatenate([groups[i] for i in pick])
        draws[b] = np.percentile(s, qs)
    lo, hi = np.percentile(draws, [2.5, 97.5], axis=0)
    return {str(q): {"lo": round(float(a), 2), "hi": round(float(c), 2)}
            for q, a, c in zip(qs, lo, hi)}


def cluster_bootstrap_mean(keys, vals, B=BOOT_B, seed=BOOT_SEED):
    """95% interval on the MEAN of vals, clusters resampled with replacement."""
    rng = np.random.default_rng(seed)
    groups = _groups(keys, vals)
    n = len(groups)
    draws = np.empty(B)
    for b in range(B):
        pick = rng.integers(0, n, n)
        s = np.concatenate([groups[i] for i in pick])
        draws[b] = s.mean()
    lo, hi = np.percentile(draws, [2.5, 97.5])
    return {"point": round(float(vals.mean()), 3),
            "lo": round(float(lo), 3), "hi": round(float(hi), 3)}


# --------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------
def make_figure(c1, allsh, W, pct, blocks, path):
    fig = plt.figure(figsize=(15.5, 10.5))
    gs = fig.add_gridspec(2, 2, hspace=0.32, wspace=0.22)

    # --- panel A: signed untruncated histogram, edge bins carry all mass ----
    ax = fig.add_subplot(gs[0, 0])
    edges = np.r_[-np.inf, np.arange(-120, 181, 7), np.inf]
    plot_edges = np.r_[-127, np.arange(-120, 181, 7), 187]
    for v, lab, col in ((allsh, f"all shows, n={len(allsh):,}", "#c44"),
                        (c1, f"C1 only, n={len(c1):,}", "#248")):
        h, _ = np.histogram(v, bins=edges)
        ax.stairs(h / len(v) * 100, plot_edges, fill=False, lw=1.8,
                  color=col, label=lab)
    ax.axvline(0, color="k", lw=0.8, ls=":")
    ax.axvline(W, color="#191", lw=1.6, ls="--", label=f"proposed W = {W} d")
    ax.set_xlim(-127, 187)
    ax.set_xlabel("lag, clock start to first S2 episode (days) — SIGNED, UNTRUNCATED\n"
                  "outermost bins carry all mass beyond ±120/180 d; nothing is dropped or clipped")
    ax.set_ylabel("% of started pairs per 7-day bin")
    ax.set_title("A. Lag distribution, C1 and all shows")
    ax.legend(fontsize=8)
    ax.grid(alpha=.25)

    # --- panel B: ECDF over the full signed support, symlog -----------------
    ax = fig.add_subplot(gs[0, 1])
    for v, lab, col in ((allsh, "all shows", "#c44"), (c1, "C1 only", "#248")):
        s = np.sort(v)
        ax.plot(s, np.arange(1, len(s) + 1) / len(s) * 100, lw=1.6, color=col, label=lab)
    ax.set_xscale("symlog", linthresh=1)
    ax.axvline(0, color="k", lw=0.8, ls=":")
    ax.axvline(W, color="#191", lw=1.6, ls="--")
    ax.axhline(pct, color="#191", lw=0.9, ls=":")
    ax.set_xlim(min(allsh.min(), c1.min()), max(allsh.max(), c1.max()))
    ax.set_xlabel("lag (days), symlog — full signed support, no truncation")
    ax.set_ylabel("cumulative % of started pairs")
    ax.set_title(f"B. ECDF. P{pct} is {np.percentile(c1, pct):.1f} d on C1 "
                 f"and {np.percentile(allsh, pct):.1f} d on all shows")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=.25)

    # --- panel C: coverage curve on C1, where W is read ---------------------
    ax = fig.add_subplot(gs[1, 0])
    g = np.arange(0, 366)
    ax.plot(g, coverage(c1, g) * 100, lw=1.8, color="#248", label="C1 coverage F(w)")
    ax.axvline(W, color="#191", lw=1.6, ls="--", label=f"W = {W} d")
    ax.axhline(np.mean(c1 < W) * 100, color="#191", lw=0.9, ls=":")
    ax.set_xlabel("candidate window W (days)")
    ax.set_ylabel("% of C1 started pairs with lag < W")
    ax.set_title("C. C1 coverage curve — W is read here, and only here")
    ax.set_ylim(0, 100)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=.25)

    # --- panel D: weekly marginal gain, the flattening test -----------------
    ax = fig.add_subplot(gs[1, 1])
    k = [b["block"] for b in blocks[:30]]
    gain = [b["gain_pp"] for b in blocks[:30]]
    ax.bar([x * 7 + 3.5 for x in k], gain, width=6, color="#248", alpha=.8)
    ax.axhline(GAIN_PP_PER_WEEK, color="#c44", lw=1.4, ls="--",
               label=f"{GAIN_PP_PER_WEEK} pp per week")
    ax.axvline(W, color="#191", lw=1.6, ls="--", label=f"W = {W} d")
    ax.set_yscale("log")
    ax.set_xlabel("day (7-day blocks)")
    ax.set_ylabel("coverage gain in the block (pp, log scale)")
    ax.set_title("D. Flattening test on C1: gain per additional week")
    ax.legend(fontsize=8)
    ax.grid(alpha=.25, which="both")

    fig.suptitle("Step 6 — lag from clock start to first S2 episode. "
                 "PROPOSED, not adopted. Estimation sample: Step 5 clean records, "
                 "C1 restriction on top.", fontsize=11)
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------
def main():
    P6.mkdir(parents=True, exist_ok=True)
    out = {}

    p, waterfall = load_pairs()
    est = p[p.in_w_sample].copy()
    c1 = est[est.cadence_bucket == "C1"].copy()

    out["population"] = {
        "frame_pairs": int(len(p)),
        "published_analysis_population": PUBLISHED_ANALYSIS_POP,
        "published_W_estimation_sample": PUBLISHED_W_SAMPLE,
        "reproduced_waterfall": waterfall,
        "W_estimation_sample": int(len(est)),
        "buckets_in_frame": {k: int(v) for k, v in
                             pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
                             .cadence_bucket.value_counts().items()},
        "estimation_sample_by_bucket": {b: int((est.cadence_bucket == b).sum())
                                        for b in ("C0", "C1", "C2", "C3", "C4")},
        "C1_pairs": int(len(c1)),
        "C1_shows": int(c1.show_trakt_id.nunique()),
        "C1_users": int(c1.user_idx.nunique()),
        "C1_pairs_per_show_median": float(c1.groupby("show_trakt_id").size().median()),
        "C1_pairs_per_show_max": int(c1.groupby("show_trakt_id").size().max()),
        "C1_pairs_per_user_median": float(c1.groupby("user_idx").size().median()),
        "C1_pairs_per_user_max": int(c1.groupby("user_idx").size().max()),
    }

    lc1 = c1.lag_days.values
    lall = est.lag_days.values

    # ---- negative mass, all five buckets, split by binding term ------------
    neg = {}
    for b in ("C0", "C1", "C2", "C3", "C4"):
        m = (est.cadence_bucket == b).values
        n = int(m.sum())
        if n == 0:
            neg[b] = {"started_pairs": 0, "negative": 0, "negative_pct": None,
                      "note": "no shows in this bucket in the Step 2 frame"}
            continue
        nm = m & (est.lag_days.values < 0)
        binds = est.binds.values[nm]
        neg[b] = {
            "started_pairs": n,
            "negative": int(nm.sum()),
            "negative_pct": round(100 * float(nm.sum() / n), 2),
            "negative_binds_s1": int((binds == "s1").sum()),
            "negative_binds_finale": int((binds == "finale").sum()),
            "negative_binds_tie": int((binds == "tie").sum()),
            "pct_of_negatives_binding_finale": (
                round(100 * float((binds == "finale").sum() / nm.sum()), 1)
                if nm.sum() else None),
        }
    neg["ALL"] = {"started_pairs": int(len(est)),
                  "negative": int((lall < 0).sum()),
                  "negative_pct": round(100 * float((lall < 0).mean()), 2)}
    out["negative_mass_by_D12_bucket"] = neg

    # the C1 negatives D14 did not expect
    c1neg = c1[c1.lag_days < 0]
    fb = c1neg[c1neg.binds == "finale"]
    out["C1_negatives_diagnostic"] = {
        "C1_negative_pairs": int(len(c1neg)),
        "C1_negative_pct": round(100 * float(len(c1neg) / len(c1)), 2),
        "binds_s1": int((c1neg.binds == "s1").sum()),
        "binds_finale": int(len(fb)),
        "finale_binding_within_1_day": int((fb.lag_days > -1).sum()),
        "finale_binding_beyond_1_day": int((fb.lag_days <= -1).sum()),
        "finale_binding_min_lag_days": round(float(fb.lag_days.min()), 2) if len(fb) else None,
        "s1_binding_median_lag_days": round(float(c1neg.lag_days[c1neg.binds == "s1"].median()), 2),
        "note": ("D14 states every C1 lag is non-negative by construction. It is not: "
                 "the finale term guarantees non-negativity, the S1-completion term does not, "
                 "and max() can select the S1 term on a C1 show."),
    }

    # ---- percentiles on both curves ---------------------------------------
    qs = [1, 5, 10, 25, 50, 75, 80, 83, 84, 85, 86, 87, 88, 89, 90, 95, 99]
    out["percentiles_days"] = {
        "method": "numpy.percentile, linear interpolation, on signed untruncated lags",
        "C1": {str(q): round(float(np.percentile(lc1, q)), 2) for q in qs},
        "all_shows": {str(q): round(float(np.percentile(lall, q)), 2) for q in qs},
    }

    # ---- flattening test ---------------------------------------------------
    blocks_c1 = weekly_blocks(lc1)
    blocks_all = weekly_blocks(lall)
    out["weekly_gain_C1"] = blocks_c1[:30]
    blk = flattening_block(blocks_c1, GAIN_PP_PER_WEEK)
    assert blk is not None, "no flattening block found at the stated threshold"
    inside = whole_percentile_in_block(lc1, blk)
    assert inside, "no whole percentile falls inside the flattening block"
    pct = inside[0][0]
    w_exact = float(np.percentile(lc1, pct))
    W = int(np.ceil(w_exact))

    out["criterion"] = {
        "statement": ("walk F(w)=P(lag<w) in consecutive 7-day blocks from day 0; the curve "
                      "has flattened at the first block gaining less than "
                      f"{GAIN_PP_PER_WEEK} pp of coverage that no later block exceeds; "
                      "W is the whole percentile falling inside that block, rounded up to a "
                      "whole day"),
        "threshold_pp_per_week": GAIN_PP_PER_WEEK,
        "flattening_block": blk,
        "whole_percentiles_inside_block": [{"percentile": q, "days": round(v, 2)}
                                           for q, v in inside],
        "why_weekly_blocks": ("the one-day slope crosses 0.10 pp/day downward at day 56 and "
                              "back upward at day 66, so a daily first-crossing rule is not "
                              "reproducible; 7-day blocks are and match a weekly release grid"),
    }

    out["CHOSEN"] = {
        "percentile": pct,
        "W_exact_days": round(w_exact, 3),
        "W_days": W,
        "rounding": "ceil to a whole day; the window is exactly W days, half-open [tau0, tau0+W*24h)",
        "C1_coverage_at_W_pct": round(100 * float((lc1 < W).mean()), 3),
        "all_shows_coverage_at_W_pct": round(100 * float((lall < W).mean()), 3),
        "status": "PROPOSED. Step 6 is a gate. Not adopted by this file or its author.",
    }

    # threshold sweep: how load-bearing is the 1.0 pp/week convention
    sweep = {}
    for thr in GAIN_SWEEP:
        b = flattening_block(blocks_c1, thr)
        if b is None:
            sweep[str(thr)] = None
            continue
        ins = whole_percentile_in_block(lc1, b)
        q = ins[0][0] if ins else None
        sweep[str(thr)] = {
            "flattening_block_days": [b["day_start"], b["day_end"]],
            "block_gain_pp": b["gain_pp"],
            "percentile": q,
            "W_days": int(np.ceil(np.percentile(lc1, q))) if q else None,
        }
    out["criterion_threshold_sweep"] = sweep

    # ---- Step 13 range: same percentile read on both curves ----------------
    c1_at_pct = float(np.percentile(lc1, pct))
    all_at_pct = float(np.percentile(lall, pct))
    out["step13_W_range"] = {
        "percentile_used": pct,
        "C1_curve_days": round(c1_at_pct, 2),
        "all_shows_curve_days": round(all_at_pct, 2),
        "minimum_range_whole_days": [int(np.ceil(min(c1_at_pct, all_at_pct))),
                                     int(np.ceil(max(c1_at_pct, all_at_pct)))],
        "note": ("this interval is the size of the D14 transfer assumption and is the "
                 "MINIMUM range Step 13 must cover, not the recommended range"),
    }
    out["weekly_gain_all_shows_first10"] = blocks_all[:10]

    # ---- is C1 large enough for this percentile ---------------------------
    boot_qs = [50, 75, 85, 90, 95]
    out["bootstrap_CI_days_C1"] = {
        "B": BOOT_B, "seed": BOOT_SEED, "method": "percentile bootstrap, 95% interval",
        "cluster_show": cluster_bootstrap(c1.show_trakt_id.values, lc1, boot_qs),
        "cluster_user": cluster_bootstrap(c1.user_idx.values, lc1, boot_qs),
        "iid_pairs": cluster_bootstrap(np.arange(len(c1)), lc1, boot_qs),
    }
    cov_ind = (lc1 < W).astype(float) * 100
    out["bootstrap_CI_coverage_pct_at_W"] = {
        "W_days": W,
        "cluster_show": cluster_bootstrap_mean(c1.show_trakt_id.values, cov_ind),
        "cluster_user": cluster_bootstrap_mean(c1.user_idx.values, cov_ind),
        "iid_pairs": cluster_bootstrap_mean(np.arange(len(c1)), cov_ind),
    }

    # ---- exposure check: can a lag of W even be observed -------------------
    ex = c1.exposure_days.values
    out["exposure_check_C1"] = {
        "median_days": round(float(np.median(ex)), 1),
        "p1_days": round(float(np.percentile(ex, 1)), 1),
        "share_below_W_pct": round(100 * float((ex < W).mean()), 3),
        "share_below_91_pct": round(100 * float((ex < 91).mean()), 3),
        "direction": ("pairs observed for fewer than W days cannot exhibit a lag of W, so "
                      "coverage at W is very slightly overstated and the true percentile "
                      "value is very slightly larger"),
    }

    # ---- what the spec does not decide, quantified rather than chosen -----
    # (i) D14 asserts C1 lags are non-negative by construction; 689 are not, and
    #     no rule says what to do with them. Reported, not resolved.
    lc1_pos = lc1[lc1 >= 0]
    impossible = (c1.lag_days.values < 0) & (c1.binds.values == "finale") & (c1.lag_days.values <= -1)
    lc1_no_impossible = lc1[~impossible]
    out["spec_silence_sensitivity"] = {
        "as_computed_all_C1_signed": {"percentile": pct, "days": round(w_exact, 2), "n": len(lc1)},
        "if_C1_negatives_were_dropped": {
            "percentile": pct, "days": round(float(np.percentile(lc1_pos, pct)), 2),
            "n": int(len(lc1_pos))},
        "if_only_the_95_structurally_impossible_were_dropped": {
            "percentile": pct, "days": round(float(np.percentile(lc1_no_impossible, pct)), 2),
            "n": int(len(lc1_no_impossible))},
        "note": ("no rule in task-sheet.md or Step 1 covers a negative C1 lag, because D14 "
                 "assumed none exist; the primary figure keeps every row untouched, which is "
                 "the only treatment the withdrawal of truncation supports"),
    }

    # (ii) coverage at candidate windows, both curves, for the gate and Step 13
    out["coverage_at_candidate_W"] = {
        str(w): {"C1_pct": round(100 * float((lc1 < w).mean()), 3),
                 "all_shows_pct": round(100 * float((lall < w).mean()), 3)}
        for w in (7, 11, 14, 21, 28, 30, 46, 60, 65, 89, 91, 120)}

    # ---- pair-level table stays in processed/ -----------------------------
    cols = ["user_idx", "username", "show_trakt_id", "cadence_bucket", "t0", "binds",
            "first_s2_ts", "lag_days", "exposure_days", "in_w_sample"]
    p.loc[p.in_w_sample, cols].to_csv(P6 / "pair_lag.csv", index=False)

    make_figure(lc1, lall, W, pct, blocks_c1, ART / "step6-lag-distributions.png")
    out["figure"] = "artifacts/step6-lag-distributions.png"

    (ART / "step6-w-derivation.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: v for k, v in out.items()
                      if k in ("population", "CHOSEN", "criterion", "step13_W_range",
                               "negative_mass_by_D12_bucket", "C1_negatives_diagnostic",
                               "criterion_threshold_sweep", "bootstrap_CI_days_C1",
                               "exposure_check_C1")}, indent=2))


if __name__ == "__main__":
    main()
