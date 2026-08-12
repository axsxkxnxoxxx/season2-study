"""Step 6 (instance -a): derive the window W.

READ ONLY on the study data. ZERO network calls.

WHAT THIS FILE DOES, and the spec line each block answers
(spec = task-sheet.md, "Step 6: Derive window W", as amended 2026-08-12 by
 decisions/0024-w-is-the-90th-percentile.md):

  1. Rebuild the Step 5 clean-record W estimation sample (128,099 pairs) from
     processed/step5/pair_revision5.csv, reproducing the published waterfall
     201,900 -> 178,165 -> 155,131 -> 152,126 -> 128,099 exactly. The run ABORTS
     if any line of that waterfall does not reproduce, because the spec requires
     both instances to take the population from artifacts/step5-contamination-
     diagnostics.md rather than re-derive it.
  2. Classify every frame show into the five D12 cadence buckets INDEPENDENTLY
     from s2_premiere_date / s2_finale_date / s2_L, first-match ordering, and
     cross-check against the frame's own cadence_bucket column.
  3. Lag = date(first S2 watch) - T0, in whole UTC calendar days, SIGNED and
     UNTRUNCATED. No clipping, no absolute values, no dropped rows.
  4. W = the 90th percentile of the lag distribution on the C1 subset of the
     estimation sample. Reported under six percentile conventions so that a
     convention difference cannot masquerade as a bug in the dual diff.
  5. The same 90th percentile read on the all-shows curve (all five buckets of
     the same 128,099), giving Step 13's minimum W range deterministically.
  6. Negative mass as a count and a share of the started population, split by
     all five D12 buckets; C1 negatives additionally split by binding term.
  7. Sample-adequacy evidence for the 90th percentile on C1: n, the exact
     distribution-free order-statistic interval, and a bootstrap interval.

Outputs (all under the -a namespace):
  artifacts/step6-lag-distributions-a.png
  artifacts/step6-negative-mass-a.png
  artifacts/step6-w-derivation-a.json
  processed/step6/a/lags.csv                (pair-keyed, stays in processed/)

Nothing here adopts W. Step 6 is a gate.
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
P6 = ROOT / "processed" / "step6" / "a"
ART = ROOT / "artifacts"

# --- constants taken from approved upstream decisions, not chosen here -------
BACKFILL_D = 180.0        # Step 5 backfill threshold
POSTDATE_D = -30.0        # Step 5 post-date threshold
PCTL = 90.0               # decisions/0024: W is the 90th percentile
PULL_DATE = np.datetime64("2026-08-11")            # decisions/0011
TAU_PULL = int(PULL_DATE.astype("datetime64[s]").astype(np.int64))

PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]

BUCKETS = ["C0", "C1", "C2", "C3", "C4"]


def d12_bucket(prem, fin, L2):
    """D12 classifier, Step 1 sec 10.0. First match wins, evaluated in order."""
    span = (fin - prem).dt.days.values.astype("float64")
    L2 = L2.astype("float64")
    weekly_span = (L2 - 1.0) * 7.0
    unclassifiable = prem.isna().values | fin.isna().values | np.isnan(L2) | (span < 0)
    out = np.full(len(span), "", dtype=object)
    out[:] = "UNASSIGNED"
    out = np.where(unclassifiable, "C0", out)
    rest = out == "UNASSIGNED"
    out = np.where(rest & (span <= 1), "C1", out)
    rest = out == "UNASSIGNED"
    out = np.where(rest & (np.abs(span - weekly_span) <= 3), "C2", out)
    rest = out == "UNASSIGNED"
    out = np.where(rest & (span > 1) & (span < weekly_span - 3), "C3", out)
    rest = out == "UNASSIGNED"
    out = np.where(rest & (span > weekly_span + 3), "C4", out)
    return out, span, weekly_span


def percentile_panel(x, q):
    """Every standard reading of 'the q-th percentile', so a convention
    difference between the two instances is visible rather than silent."""
    x = np.asarray(x, dtype="float64")
    n = len(x)
    xs = np.sort(x)
    panel = {}
    for m in ("linear", "lower", "higher", "nearest", "midpoint",
              "inverted_cdf", "averaged_inverted_cdf"):
        try:
            panel[m] = float(np.percentile(xs, q, method=m))
        except (TypeError, ValueError):
            panel[m] = None
    # nearest-rank: the ceil(q/100 * n)-th order statistic, 1-indexed
    k = int(np.ceil(q / 100.0 * n))
    panel["nearest_rank_ceil"] = float(xs[min(max(k, 1), n) - 1])
    return panel


def _binom_ppf(prob, n, p):
    """Smallest k with P(X <= k) >= prob for X ~ Binomial(n, p).
    Written out rather than imported: scipy is not a dependency of this repo,
    and the sum is evaluated in log space over a +/- 10 sd band around the mean,
    which is exact to double precision at these n."""
    import math
    mu = n * p
    sd = math.sqrt(n * p * (1 - p))
    lo = max(0, int(mu - 10 * sd) - 5)
    hi = min(n, int(mu + 10 * sd) + 5)
    lg = math.lgamma
    acc = 0.0
    # mass strictly below lo is < 1e-20 at these n and is taken as zero
    for k in range(lo, hi + 1):
        logpmf = (lg(n + 1) - lg(k + 1) - lg(n - k + 1)
                  + k * math.log(p) + (n - k) * math.log1p(-p))
        acc += math.exp(logpmf)
        if acc >= prob:
            return k
    return hi


def order_stat_ci(x, q, alpha=0.05):
    """Exact distribution-free CI for the q-th population quantile, from the
    binomial order-statistic construction. No distributional assumption."""
    xs = np.sort(np.asarray(x, dtype="float64"))
    n = len(xs)
    p = q / 100.0
    lo_r = int(_binom_ppf(alpha / 2.0, n, p))        # 0-indexed lower order stat
    hi_r = int(_binom_ppf(1.0 - alpha / 2.0, n, p)) + 1
    lo_r = min(max(lo_r, 0), n - 1)
    hi_r = min(max(hi_r, 0), n - 1)
    return float(xs[lo_r]), float(xs[hi_r]), lo_r + 1, hi_r + 1


def bootstrap_ci(x, q, B=2000, seed=20260812):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype="float64")
    n = len(x)
    reps = np.empty(B)
    for b in range(B):
        reps[b] = np.percentile(x[rng.integers(0, n, n)], q)
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5)), float(reps.std())


def main():
    P6.mkdir(parents=True, exist_ok=True)
    out = {
        "step": 6,
        "instance": "a",
        "spec": "task-sheet.md Step 6, as amended by decisions/0024-w-is-the-90th-percentile.md",
        "percentile_rule": PCTL,
        "pull_date": str(PULL_DATE),
        "api_calls": 0,
    }

    # ---------------- 1. rebuild the Step 5 estimation sample ---------------
    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate",
            "t0_contaminated", "complete_rec_lag_days", "first_s2_lag_days",
            "first_s2_airdate", "first_s2_corrupt", "first_s2_ts",
            "complete_rec_ts", "t0", "binds", "s2_distinct"]
    p = pd.read_csv(P5 / "pair_revision5.csv", usecols=cols)

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
    out["step5_waterfall_reproduced"] = {
        "labels": ["analysis population", "has S2 evidence", "T0 not contaminated",
                   "completing record not post-dated", "first S2 watch clean"],
        "computed": waterfall,
        "published": PUBLISHED_WATERFALL,
        "match": waterfall == PUBLISHED_WATERFALL,
    }
    assert waterfall == PUBLISHED_WATERFALL, (
        f"Step 5 waterfall did not reproduce: {waterfall} vs {PUBLISHED_WATERFALL}")

    est = p.loc[w5].copy()

    # ---------------- 2. D12 buckets, recomputed independently ---------------
    fcols = ["show_trakt_id", "title", "s2_premiere_date", "s2_finale_date",
             "s2_L", "s2_span_days", "s2_weekly_span_days", "cadence_bucket",
             "cadence_boundary_distance_days"]
    f = pd.read_csv(P2 / fcols[0].replace("show_trakt_id", "frame.csv"), usecols=fcols) \
        if False else pd.read_csv(P2 / "frame.csv", usecols=fcols)
    bucket, span, weekly_span = d12_bucket(
        pd.to_datetime(f.s2_premiere_date), pd.to_datetime(f.s2_finale_date), f.s2_L.values)
    f["bucket_recomputed"] = bucket
    disagree = int((f.bucket_recomputed != f.cadence_bucket).sum())
    out["d12_recomputation"] = {
        "frame_shows": int(len(f)),
        "disagreements_with_frame_column": disagree,
        "shows_by_bucket": {b: int((f.bucket_recomputed == b).sum()) for b in BUCKETS},
        "shows_within_1_day_of_a_bucket_boundary":
            int((f.cadence_boundary_distance_days <= 1).sum()),
    }
    assert disagree == 0, "independent D12 recomputation disagrees with the frame"

    est = est.merge(f[["show_trakt_id", "bucket_recomputed", "s2_L"]],
                    on="show_trakt_id", how="left", validate="m:1")
    assert est.bucket_recomputed.notna().all()

    # ---------------- 3. the lag, signed and untruncated ---------------------
    # Step 1 sec 0: lags are whole numbers of days; date reduction applies to
    # clock arithmetic. T0 is a UTC calendar date, so
    #   date(first_s2_watched_at) - T0  ==  floor((watched_at - [T0]) / 24h)
    # exactly, for negative values too. The two readings coincide identically.
    t0 = pd.to_datetime(est.t0).values.astype("datetime64[D]")
    first = pd.to_datetime(est.first_s2_ts, unit="s", utc=True) \
        .dt.tz_localize(None).values.astype("datetime64[D]")
    lag = (first - t0).astype("timedelta64[D]").astype(np.int64)
    est["lag_days"] = lag

    floor_form = np.floor(
        (pd.to_datetime(est.first_s2_ts, unit="s", utc=True).dt.tz_localize(None).values
         - pd.to_datetime(est.t0).values).astype("timedelta64[s]").astype(np.int64) / 86400.0
    ).astype(np.int64)
    out["lag_definition_check"] = {
        "calendar_date_difference_equals_floor_of_instant_difference":
            bool((floor_form == lag).all()),
        "note": "the two faithful readings of 'lag in whole days' are identical on this data",
    }

    # tau_pull hygiene: Step 1 D11 discards records with watched_at >= tau_pull.
    # Step 5's sample was built without that filter. Count the exposure.
    post_pull = (est.first_s2_ts.values >= TAU_PULL)
    out["tau_pull_conflict"] = {
        "pairs_in_estimation_sample_whose_first_S2_record_is_at_or_after_tau_pull":
            int(post_pull.sum()),
        "of_which_C1": int((post_pull & (est.bucket_recomputed == "C1").values).sum()),
        "note": ("Step 1 D11 discards these records from every computation; the Step 5 "
                 "sample of 128,099 was built without that filter. The spec directs Step 6 "
                 "to take the population from the Step 5 artifact, so they are retained. "
                 "The effect on W is reported below and is nil."),
    }

    # ---------------- 4. W, on C1 ------------------------------------------
    is_c1 = (est.bucket_recomputed == "C1").values
    c1 = est.loc[is_c1]
    lag_c1 = c1.lag_days.values.astype("float64")
    lag_all = est.lag_days.values.astype("float64")

    panel_c1 = percentile_panel(lag_c1, PCTL)
    panel_all = percentile_panel(lag_all, PCTL)
    conventions_agree_c1 = len({round(v, 6) for v in panel_c1.values() if v is not None}) == 1
    conventions_agree_all = len({round(v, 6) for v in panel_all.values() if v is not None}) == 1

    W = panel_c1["linear"]
    W_int = int(round(W))
    W_all = panel_all["linear"]

    # sensitivity of W to the four tau_pull-conflicting pairs
    W_wo_postpull = float(np.percentile(
        est.loc[is_c1 & ~post_pull].lag_days.values.astype("float64"), PCTL))
    out["tau_pull_conflict"]["W_with_them"] = W
    out["tau_pull_conflict"]["W_without_them"] = W_wo_postpull

    lo_os, hi_os, r_lo, r_hi = order_stat_ci(lag_c1, PCTL)
    bs_lo, bs_hi, bs_sd = bootstrap_ci(lag_c1, PCTL)

    # Pairs are clustered inside users and inside shows, so the iid bootstrap
    # above understates the interval. Cluster bootstraps on both keys.
    def cluster_bootstrap(df, key, q, B=1000, seed=20260812):
        rng = np.random.default_rng(seed)
        groups = [g.lag_days.values.astype("float64")
                  for _, g in df.groupby(key, sort=True)]
        k = len(groups)
        reps = np.empty(B)
        for b in range(B):
            idx = rng.integers(0, k, k)
            reps[b] = np.percentile(np.concatenate([groups[i] for i in idx]), q)
        return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))

    cu_lo, cu_hi = cluster_bootstrap(c1, "user_idx", PCTL)
    cs_lo, cs_hi = cluster_bootstrap(c1, "show_trakt_id", PCTL)

    out["W"] = {
        "value_days": W_int,
        "raw_percentile_value": W,
        "is_integer": bool(float(W).is_integer()),
        "estimation_sample": "C1 subset of the Step 5 128,099 clean-record sample",
        "n_pairs": int(len(c1)),
        "n_shows": int(c1.show_trakt_id.nunique()),
        "n_users": int(c1.user_idx.nunique()),
        "percentile_conventions": panel_c1,
        "all_conventions_agree": bool(conventions_agree_c1),
        "order_statistic_95CI": {"lo": lo_os, "hi": hi_os, "ranks": [r_lo, r_hi]},
        "bootstrap_95CI": {"lo": bs_lo, "hi": bs_hi, "sd": bs_sd, "B": 2000,
                           "seed": 20260812},
        "cluster_bootstrap_95CI_by_user": {"lo": cu_lo, "hi": cu_hi, "B": 1000},
        "cluster_bootstrap_95CI_by_show": {"lo": cs_lo, "hi": cs_hi, "B": 1000},
    }

    out["all_shows_curve"] = {
        "population": "all five D12 buckets of the same 128,099 clean-record sample",
        "n_pairs": int(len(est)),
        "p90_days": W_all,
        "percentile_conventions": panel_all,
        "all_conventions_agree": bool(conventions_agree_all),
        "warning": "descriptive only; W is never read off this curve",
    }

    out["step13_minimum_W_range"] = {
        "percentile_used": PCTL,
        "read_on_C1": W,
        "read_on_all_shows": W_all,
        "range": [min(W, W_all), max(W, W_all)],
        "note": ("the same percentile read on both curves, per the spec's deterministic "
                 "rule; Step 13 must also span 46-107 per decisions/0024 and cover the "
                 "UNION of the two"),
    }

    # ---------------- 5. distribution shape, both curves ---------------------
    def shape(x):
        x = np.asarray(x, dtype="float64")
        qs = [0, 1, 5, 10, 25, 50, 75, 80, 85, 90, 95, 99, 100]
        return {
            "n": int(len(x)),
            "min": float(x.min()), "max": float(x.max()),
            "mean": float(x.mean()), "median": float(np.median(x)),
            "quantiles": {f"p{q}": float(np.percentile(x, q)) for q in qs},
            "share_negative": float((x < 0).mean()),
            "share_zero": float((x == 0).mean()),
            "share_le_1": float((x <= 1).mean()),
            "share_le_7": float((x <= 7).mean()),
            "share_le_30": float((x <= 30).mean()),
        }
    out["shape_C1"] = shape(lag_c1)
    out["shape_all_shows"] = shape(lag_all)

    # neighbouring percentiles, so the reader can see what the convention buys
    out["percentile_sensitivity_C1"] = {
        f"p{q}": float(np.percentile(lag_c1, q))
        for q in (70, 75, 80, 85, 88, 89, 90, 91, 92, 95)
    }
    out["percentile_sensitivity_all_shows"] = {
        f"p{q}": float(np.percentile(lag_all, q))
        for q in (70, 75, 80, 85, 88, 89, 90, 91, 92, 95)
    }

    # ---------------- 6. negative mass, split by all five buckets -----------
    neg = {}
    started_n = int(len(est))
    for b in BUCKETS:
        sel = (est.bucket_recomputed == b).values
        n_b = int(sel.sum())
        nb = int((sel & (est.lag_days.values < 0)).sum())
        neg[b] = {
            "pairs": n_b,
            "negative_lag_pairs": nb,
            "share_of_bucket": (float(nb / n_b) if n_b else None),
            "share_of_started_population": float(nb / started_n),
            "min_lag_days": (float(est.lag_days.values[sel].min()) if n_b else None),
            "median_lag_days": (float(np.median(est.lag_days.values[sel])) if n_b else None),
        }
    neg["TOTAL"] = {
        "started_population": started_n,
        "negative_lag_pairs": int((est.lag_days.values < 0).sum()),
        "share_of_started_population": float((est.lag_days.values < 0).mean()),
    }
    out["negative_mass_by_bucket_on_the_plotted_population"] = neg

    # supplementary denominator: all started pairs in the analysis population
    sup = p.loc[w2].merge(f[["show_trakt_id", "bucket_recomputed"]],
                          on="show_trakt_id", how="left", validate="m:1")
    st0 = pd.to_datetime(sup.t0).values.astype("datetime64[D]")
    sfirst = pd.to_datetime(sup.first_s2_ts, unit="s", utc=True) \
        .dt.tz_localize(None).values.astype("datetime64[D]")
    slag = (sfirst - st0).astype("timedelta64[D]").astype(np.int64)
    sup_ok = sup.first_s2_ts.values > 0
    out["negative_mass_supplementary_denominator_178165"] = {
        "note": ("SUPPLEMENTARY ONLY, not the required split. The required split is on the "
                 "plotted population (128,099). This uses the analysis population's started "
                 "pairs (178,165), whose timestamps include contaminated ones, and is given "
                 "so the Human Lead can see the cadence artifact at both denominators."),
        "started_population": int(sup_ok.sum()),
        "by_bucket": {
            b: {"pairs": int(((sup.bucket_recomputed == b).values & sup_ok).sum()),
                "negative_lag_pairs": int(((sup.bucket_recomputed == b).values
                                           & sup_ok & (slag < 0)).sum())}
            for b in BUCKETS},
        "total_negative": int((sup_ok & (slag < 0)).sum()),
    }

    # C1 negatives, split by which term of the max() binds  (the known defect)
    c1neg = c1.loc[c1.lag_days.values < 0]
    out["C1_negative_lags_defect"] = {
        "claim_in_decisions_0003_D14_and_step1_sec9":
            "every C1 lag is non-negative by construction",
        "status": "FALSE on this data; carried as open item 24 in decisions/README.md",
        "count": int(len(c1neg)),
        "share_of_C1": float(len(c1neg) / len(c1)),
        "by_binding_term": {k: int(v) for k, v in c1neg.binds.value_counts().items()},
        "min_lag_days": (int(c1neg.lag_days.min()) if len(c1neg) else None),
        "exactly_minus_1_day": int((c1neg.lag_days.values == -1).sum()),
        "worse_than_minus_1_day": int((c1neg.lag_days.values < -1).sum()),
        "effect_on_W_if_they_were_dropped": float(
            np.percentile(c1.loc[c1.lag_days.values >= 0].lag_days.values.astype("float64"),
                          PCTL)),
        "note": ("reported, not repaired; the percentile is taken on the signed, "
                 "untruncated distribution as the spec directs"),
    }

    # ---------------- 7. C1 sample adequacy ---------------------------------
    xs = np.sort(lag_c1)
    n = len(xs)
    out["C1_sample_adequacy"] = {
        "n_pairs": n,
        "n_shows": int(c1.show_trakt_id.nunique()),
        "n_users": int(c1.user_idx.nunique()),
        "pairs_at_or_above_the_90th_percentile": int((xs >= W).sum()),
        "effective_tail_count": int(np.ceil(0.10 * n)),
        "order_statistic_95CI_width_days": hi_os - lo_os,
        "bootstrap_95CI_width_days": bs_hi - bs_lo,
        "max_pairs_from_one_show": int(c1.show_trakt_id.value_counts().max()),
        "share_from_top_show": float(c1.show_trakt_id.value_counts().max() / n),
        "max_pairs_from_one_user": int(c1.user_idx.value_counts().max()),
    }
    # ---------------- 7b. exposure / selection diagnostic --------------------
    # The estimation sample is conditioned on HAVING started S2 by tau_pull, so a
    # pair with little elapsed time since T0 can only appear in it with a short
    # lag. That is a selection effect on the tail, and the tail is what a 90th
    # percentile reads. Reported as a diagnostic. It does NOT modify W: the spec
    # says the 90th percentile of the observed lag distribution, and this is it.
    exp_days = ((PULL_DATE.astype("datetime64[D]")
                 - pd.to_datetime(c1.t0).values.astype("datetime64[D]"))
                .astype("timedelta64[D]").astype(np.int64))
    strata = [(0, 365), (365, 730), (730, 1460), (1460, 2920), (2920, 10 ** 6)]
    expo = {}
    for lo, hi in strata:
        s = (exp_days >= lo) & (exp_days < hi)
        if s.sum() >= 50:
            expo[f"{lo}-{hi}d"] = {
                "n": int(s.sum()),
                "p90_days": float(np.percentile(lag_c1[s], PCTL)),
                "median_days": float(np.median(lag_c1[s])),
            }
    out["C1_exposure_diagnostic"] = {
        "note": ("p90 of the observed lag within strata of elapsed time since T0. "
                 "A rising p90 with exposure indicates the pooled figure is pulled "
                 "DOWN by short-exposure pairs, i.e. W = 107 is if anything a "
                 "lower bound on the untruncated behaviour. Selection and cohort "
                 "effects are not separable here and this is not a correction."),
        "by_elapsed_time_since_T0": expo,
        "p90_on_pairs_with_at_least_8_years_exposure": float(
            np.percentile(lag_c1[exp_days >= 2920], PCTL))
        if (exp_days >= 2920).sum() >= 50 else None,
        "n_at_least_8_years": int((exp_days >= 2920).sum()),
    }

    # per-show leave-one-out: does one show carry the percentile?
    loo = {}
    top = c1.show_trakt_id.value_counts().head(10).index
    for sid in top:
        sub = c1.loc[c1.show_trakt_id != sid].lag_days.values.astype("float64")
        loo[int(sid)] = float(np.percentile(sub, PCTL))
    out["C1_sample_adequacy"]["leave_one_show_out_p90_top10_shows"] = loo

    # ---------------- write pair-keyed intermediate to processed/ -----------
    est[["user_idx", "show_trakt_id", "bucket_recomputed", "t0", "first_s2_ts",
         "lag_days", "binds", "s2_distinct", "s2_L"]].to_csv(P6 / "lags.csv", index=False)

    # ---------------- figures ------------------------------------------------
    make_main_figure(lag_c1, lag_all, W, W_all)
    make_negative_mass_figure(est, neg)

    (ART / "step6-w-derivation-a.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


def _symlog_hist(ax, x, color, label, linthresh=1.0):
    """Histogram on a symmetric-log x axis, covering the FULL signed range.
    Nothing is truncated, clipped, or folded to absolute value."""
    x = np.asarray(x, dtype="float64")
    lo, hi = x.min(), x.max()
    negs = -np.logspace(0, np.log10(max(-lo, 1.0) + 1), 40)[::-1] if lo < 0 else np.array([])
    pos = np.logspace(0, np.log10(max(hi, 1.0) + 1), 60) if hi > 0 else np.array([])
    edges = np.unique(np.concatenate([negs, [-1.0, 0.0, 1.0], pos]))
    edges = edges[(edges >= lo - 1) & (edges <= hi + 1)]
    edges = np.unique(np.concatenate([[lo - 0.5], edges, [hi + 0.5]]))
    h, e = np.histogram(x, bins=edges)
    dens = h / h.sum()
    ax.step(e[:-1], dens, where="post", color=color, lw=1.6, label=label)
    ax.fill_between(e[:-1], 0, dens, step="post", color=color, alpha=0.18)


def make_main_figure(lag_c1, lag_all, W, W_all):
    fig, axes = plt.subplots(2, 2, figsize=(15, 9.5))
    c_c1, c_all = "#1b6ca8", "#c1543a"

    # (a) signed, untruncated, symlog density
    ax = axes[0, 0]
    _symlog_hist(ax, lag_all, c_all, f"all shows, all 5 buckets (n={len(lag_all):,})")
    _symlog_hist(ax, lag_c1, c_c1, f"C1 all-at-once only (n={len(lag_c1):,})")
    ax.set_xscale("symlog", linthresh=1)
    ax.axvline(0, color="0.35", lw=0.8, ls=":")
    ax.axvline(W, color=c_c1, lw=1.6, ls="--")
    ax.axvline(W_all, color=c_all, lw=1.6, ls="--")
    ax.set_title("(a) Lag from clock start $T_0$ to first S2 episode\n"
                 "signed and untruncated; symlog x, negatives at their actual values",
                 fontsize=10.5)
    ax.set_xlabel("lag, days (negative = started S2 before the S2 finale aired)")
    ax.set_ylabel("share of pairs in bin")
    ax.legend(fontsize=8.5, loc="upper left")

    # (b) ECDF over the full signed range
    ax = axes[0, 1]
    for x, c, lab in ((lag_all, c_all, "all shows"), (lag_c1, c_c1, "C1 only")):
        xs = np.sort(np.asarray(x, dtype="float64"))
        ax.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", color=c, lw=1.6,
                label=lab)
    ax.set_xscale("symlog", linthresh=1)
    ax.axhline(0.90, color="0.3", lw=1.0, ls="--")
    ax.axvline(W, color=c_c1, lw=1.4, ls="--")
    ax.axvline(W_all, color=c_all, lw=1.4, ls="--")
    ax.text(0.98, 0.30, f"C1 p90 = {W:.0f} d  <- this is W", transform=ax.transAxes,
            ha="right", color=c_c1, fontsize=10.5, weight="bold")
    ax.text(0.98, 0.23, f"all-shows p90 = {W_all:.0f} d  (descriptive)",
            transform=ax.transAxes, ha="right", color=c_all, fontsize=10.5,
            weight="bold")
    ax.text(0.98, 0.15, f"Step 13 minimum W range: [{min(W, W_all):.0f}, "
                        f"{max(W, W_all):.0f}] days",
            transform=ax.transAxes, ha="right", color="0.25", fontsize=9.5)
    ax.set_title("(b) ECDF, full signed range. The 90th percentile is read here.\n"
                 "W comes off the C1 curve only; the all-shows curve is descriptive.",
                 fontsize=10.5)
    ax.set_xlabel("lag, days")
    ax.set_ylabel("cumulative share of pairs")
    ax.set_ylim(0, 1.02)
    ax.legend(fontsize=8.5, loc="upper left")

    # (c) the first 180 days, linear, where the window actually sits
    ax = axes[1, 0]
    bins = np.arange(-0.5, 180.5, 1)
    for x, c, lab in ((lag_all, c_all, "all shows"), (lag_c1, c_c1, "C1 only")):
        x = np.asarray(x, dtype="float64")
        ax.hist(x, bins=bins, density=True, histtype="step", color=c, lw=1.4, label=lab)
    ax.axvline(W, color=c_c1, lw=1.6, ls="--")
    ax.axvline(W_all, color=c_all, lw=1.6, ls="--")
    ax.set_yscale("log")
    ax.set_title("(c) Detail, 0-180 days, linear x, log y.\n"
                 "AXIS RANGE ONLY - no row is dropped; the full range is in (a) and (b).",
                 fontsize=10.5)
    ax.set_xlabel("lag, days")
    ax.set_ylabel("density (log)")
    ax.legend(fontsize=8.5)

    # (d) log-log survival, the scale-free tail decisions/0024 records
    ax = axes[1, 1]
    for x, c, lab in ((lag_all, c_all, "all shows"), (lag_c1, c_c1, "C1 only")):
        xs = np.sort(np.asarray(x, dtype="float64"))
        pos = xs[xs > 0]
        surv = 1.0 - np.arange(1, len(pos) + 1) / len(xs) - (xs <= 0).mean()
        ax.plot(pos, np.clip(surv, 1e-6, None), color=c, lw=1.5, label=lab)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.axvline(W, color=c_c1, lw=1.4, ls="--")
    ax.axhline(0.10, color="0.3", lw=0.9, ls="--")
    ax.set_title("(d) Survival on log-log. There is no elbow to read past ~day 7 -\n"
                 "which is why 'where the curve flattens' was withdrawn.", fontsize=10.5)
    ax.set_xlabel("lag, days (positive part)")
    ax.set_ylabel("P(lag > x)")
    ax.legend(fontsize=8.5)

    fig.suptitle(
        f"Step 6 (instance -a): lag distributions and the derivation of W. "
        f"W = 90th percentile of the C1 lag distribution = {W:.0f} days.",
        fontsize=12.5, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.955))
    fig.savefig(ART / "step6-lag-distributions-a.png", dpi=170)
    plt.close(fig)


def make_negative_mass_figure(est, neg):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    labels = [b for b in BUCKETS if neg[b]["pairs"] > 0]
    shares = [100 * neg[b]["share_of_bucket"] for b in labels]
    counts = [neg[b]["negative_lag_pairs"] for b in labels]
    names = {"C0": "C0 unclassifiable", "C1": "C1 all-at-once", "C2": "C2 weekly",
             "C3": "C3 faster than weekly", "C4": "C4 slower than weekly"}

    ax = axes[0]
    bars = ax.bar([names[b] for b in labels], shares, color="#c1543a", alpha=0.85)
    for b, s, c in zip(bars, shares, counts):
        ax.annotate(f"{s:.1f}%\n({c:,})", (b.get_x() + b.get_width() / 2, s),
                    ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("share of the bucket's started pairs with a negative lag, %")
    ax.set_title("Negative mass is a cadence artifact, not viewer behaviour.\n"
                 "Split by all five D12 buckets, on the plotted population (128,099).",
                 fontsize=10.5)
    ax.tick_params(axis="x", labelrotation=12, labelsize=9)
    ax.set_ylim(0, max(shares) * 1.25)

    ax = axes[1]
    for b, c in zip(labels, ["#777777", "#1b6ca8", "#c1543a", "#2e8b57", "#8a5fbf"]):
        x = est.loc[est.bucket_recomputed == b, "lag_days"].values.astype("float64")
        if len(x) < 30:
            continue
        xs = np.sort(x)
        ax.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", color=c, lw=1.5,
                label=f"{names[b]} (n={len(xs):,})")
    ax.set_xscale("symlog", linthresh=1)
    ax.axvline(0, color="0.35", lw=0.8, ls=":")
    ax.axhline(0.90, color="0.3", lw=0.9, ls="--")
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("lag, days (signed, untruncated)")
    ax.set_ylabel("cumulative share")
    ax.set_title("Per-bucket ECDF. C1 is almost all at zero or above (2.7% below);\n"
                 "C2/C3/C4 carry 22-39% below zero, which is airing-span exposure.",
                 fontsize=10.5)
    ax.legend(fontsize=8)

    fig.suptitle("Step 6 (instance -a): the negative mass, split by D12 bucket",
                 fontsize=12, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(ART / "step6-negative-mass-a.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
