"""Step 7 (rerun), instance b2 -- stage 3: threshold, sensitivities, chart.

The reference distribution is the BRACKETING-gap distribution (decisions/0037 s1).
Threshold = 99th percentile of it, ceiling to whole days (decisions/0025).
Test: a pair is LIVE iff its measured bracketing gap is STRICTLY UNDER the
threshold ("gaps under the threshold", task-sheet Step 7).

Zero API calls.
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b2"
ART = ROOT / "artifacts"
DAY = 86400.0
PCT = 99.0

d = pd.read_csv(OUT / "pair_bracket.csv")
meas = d.state.values == 0
g = d.gap_days.values[meas]

pooled = np.load(OUT / "pooled_gaps_days.npy")
pooled_99 = float(np.percentile(pooled, PCT))
pooled_thr = math.ceil(pooled_99)

brack_99 = float(np.percentile(g, PCT))
thr = math.ceil(brack_99)


def rate(threshold, x=g):
    return round(100.0 * float((x >= threshold).sum()) / len(x), 4)


res = {
    "reference_distribution": "bracketing gaps only (decisions/0037 s1)",
    "reference_n": int(len(g)),
    "percentile": PCT,
    "percentile_method": "numpy linear interpolation between order statistics",
    "raw_percentile_days": brack_99,
    "THRESHOLD_PROPOSED_days": thr,
    "test_direction": "LIVE iff measured bracketing gap < threshold; >= threshold is not live",
    "realised_failure_rate_pct_on_measured_gaps": rate(thr),
    "withdrawn_basis_check": {
        "pooled_99th_days_raw": pooled_99,
        "pooled_99th_days_ceiled": pooled_thr,
        "realised_failure_rate_pct_at_pooled_threshold": rate(pooled_thr),
        "published_figure_under_withdrawn_basis_pct": 37.4,
    },
    "percentile_grid_on_bracketing": {
        str(q): {
            "raw_days": float(np.percentile(g, q)),
            "ceiled_days": math.ceil(float(np.percentile(g, q))),
            "realised_failure_rate_pct": rate(math.ceil(float(np.percentile(g, q)))),
        } for q in [90, 95, 97.5, 99, 99.5, 99.9]
    },
    "pooled_grid_for_contrast": {
        str(q): {
            "raw_days": float(np.percentile(pooled, q)),
            "ceiled_days": math.ceil(float(np.percentile(pooled, q))),
            "realised_failure_rate_pct_on_bracketing": rate(math.ceil(float(np.percentile(pooled, q)))),
        } for q in [95, 99, 99.9, 99.99]
    },
}

# ---- sensitivity 1: reference population
subsets = {
    "analysis_population_201900_PRIMARY": np.ones(len(d), bool),
    "clean_T0_subset": d.t0_clean.values.astype(bool),
    "step5_estimation_sample_128099": d.in_est_sample.values.astype(bool),
}
res["sensitivity_reference_population"] = {}
for name, m in subsets.items():
    x = d.gap_days.values[m & meas]
    r = float(np.percentile(x, PCT))
    res["sensitivity_reference_population"][name] = {
        "measured_gap_pairs": int(len(x)), "raw_99th_days": r, "ceiled_days": math.ceil(r),
        "median_days": float(np.percentile(x, 50)),
        "realised_failure_rate_pct_at_own_threshold": rate(math.ceil(r), x),
        "realised_failure_rate_pct_at_primary_threshold": rate(thr, x),
    }

# ---- sensitivity 2: weighting. One gap per pair (primary) vs one per distinct
# (account, gap) -- an account's pairs often bracket the same gap.
dd = d.loc[meas, ["user_idx", "gap_days"]].drop_duplicates()
gu = dd.gap_days.values
r = float(np.percentile(gu, PCT))
res["sensitivity_weighting_one_gap_per_distinct_account_gap"] = {
    "n": int(len(gu)), "raw_99th_days": r, "ceiled_days": math.ceil(r),
    "median_days": float(np.percentile(gu, 50)),
    "realised_failure_rate_pct_on_pairs_at_this_threshold": rate(math.ceil(r)),
    "note": "distinct on (user_idx, gap_days); exact float equality within an account identifies the gap",
}

# ---- the W-dependence defect, quantified
p = pd.read_csv(P5 / "pair_revision5.csv")
res["W_dependence_of_the_reference_distribution"] = {}
iz = np.load(OUT / "instants.npz")
users, starts, counts, inst = iz["users"], iz["starts"], iz["counts"], iz["inst"]
pos = {int(u): i for i, u in enumerate(users)}
t0_mid = ((pd.to_datetime(d.t0, utc=True) - pd.Timestamp("1970-01-01", tz="UTC"))
          .dt.total_seconds().values)
uidx = d.user_idx.values
for Warm in [46, 77, 91, 108, 150, 213]:
    tau = t0_mid + Warm * DAY
    gg = np.full(len(d), np.nan)
    for u in np.unique(uidx):
        sel = np.nonzero(uidx == u)[0]
        j = pos[int(u)]
        arr = inst[starts[j]:starts[j] + counts[j]]
        k = np.searchsorted(arr, tau[sel], side="right")
        m2 = (k > 0) & (k < len(arr))
        km = k[m2]
        gg[sel[m2]] = (arr[km] - arr[km - 1]) / DAY
    x = gg[~np.isnan(gg)]
    rr = float(np.percentile(x, PCT))
    res["W_dependence_of_the_reference_distribution"][f"W={Warm}"] = {
        "measured_gap_pairs": int(len(x)), "raw_99th_days": rr, "ceiled_days": math.ceil(rr),
        "median_days": float(np.percentile(x, 50)),
    }

# ---- rule application at the proposed threshold
state = d.state.values
live = meas & (d.gap_days.values < thr)
res["rule_application_at_proposed_threshold"] = {
    "analysis_population": int(len(d)),
    "live": int(live.sum()),
    "not_live_measured_gap_at_or_above_threshold": int((meas & ~live).sum()),
    "not_live_no_instant_after_tau1": int((state == 1).sum()),
    "not_live_no_instant_at_or_before_tau1": int((state == 2).sum()),
    "not_live_total": int(len(d) - live.sum()),
    "live_pct": round(100.0 * int(live.sum()) / len(d), 2),
    "of_which_no_instant_after_tau1_is_after_the_pull_date": int(d.tau1_after_pull.values[state == 1].sum()),
}
sub = d.in_est_sample.values.astype(bool)
res["rule_application_on_step5_estimation_sample"] = {
    "n": int(sub.sum()),
    "live": int((live & sub).sum()),
    "not_live_measured_gap": int((meas & ~live & sub).sum()),
    "not_live_no_instant_after_tau1": int(((state == 1) & sub).sum()),
    "not_live_no_instant_at_or_before_tau1": int(((state == 2) & sub).sum()),
    "live_pct": round(100.0 * int((live & sub).sum()) / int(sub.sum()), 2),
}

(OUT / "threshold.json").write_text(json.dumps(res, indent=1))
print(json.dumps(res, indent=1))

# ---------------------------------------------------------------- chart
fig, ax = plt.subplots(2, 2, figsize=(13, 9))

lo = 1.0 / DAY
bins = np.logspace(np.log10(lo), np.log10(max(g.max(), pooled.max())), 90)
a = ax[0, 0]
a.hist(np.clip(pooled, lo, None), bins=bins, weights=np.full(len(pooled), 1.0 / len(pooled)),
       alpha=.55, label=f"pooled gaps (n={len(pooled):,})", color="#999999")
a.hist(np.clip(g, lo, None), bins=bins, weights=np.full(len(g), 1.0 / len(g)),
       alpha=.65, label=f"bracketing gaps (n={len(g):,})", color="#1f77b4")
a.set_xscale("log"); a.set_xlabel("gap (days, log)"); a.set_ylabel("share of gaps")
a.axvline(pooled_thr, color="#d62728", ls="--", lw=1.2, label=f"pooled 99th, ceil = {pooled_thr} d (withdrawn basis)")
a.axvline(thr, color="#2ca02c", ls="-", lw=1.4, label=f"bracketing 99th, ceil = {thr} d (proposed)")
a.set_title("Reference distribution: pooled vs bracketing\n(the length-bias, on a log axis)")
a.legend(fontsize=7)

a = ax[0, 1]
xs = np.sort(g)
a.plot(xs, np.arange(1, len(xs) + 1) / len(xs), color="#1f77b4", lw=1.3)
a.set_xscale("log"); a.set_xlabel("gap (days, log)"); a.set_ylabel("cumulative share")
a.axvline(pooled_thr, color="#d62728", ls="--", lw=1.2)
a.axvline(thr, color="#2ca02c", lw=1.4)
a.axhline(0.99, color="#666666", ls=":", lw=1)
a.set_title(f"Bracketing-gap CDF\nexceeding pooled thr: {rate(pooled_thr)}%  |  "
            f"proposed thr: {rate(thr)}%", fontsize=10)

a = ax[1, 0]
qgrid = np.array([90, 95, 97.5, 99, 99.5, 99.9])
a.plot(qgrid, [math.ceil(float(np.percentile(g, q))) for q in qgrid], "o-", color="#2ca02c")
a.set_yscale("log"); a.set_xlabel("percentile of the bracketing distribution")
a.set_ylabel("threshold (days, ceiled, log)")
a.set_title("Threshold as a function of the chosen percentile")
for q in qgrid:
    a.annotate(f"{math.ceil(float(np.percentile(g, q)))}", (q, math.ceil(float(np.percentile(g, q)))),
               textcoords="offset points", xytext=(4, 5), fontsize=7)

a = ax[1, 1]
warms = [46, 77, 91, 108, 150, 213]
vals = [res["W_dependence_of_the_reference_distribution"][f"W={x}"]["raw_99th_days"] for x in warms]
a.plot(warms, vals, "s-", color="#9467bd")
a.set_xlabel("W (days) used to place tau1"); a.set_ylabel("99th pct of bracketing gaps (days)")
a.set_title("The corrected reference distribution is a function of W\n(reported as a defect, not repaired)")
for x, y in zip(warms, vals):
    a.annotate(f"{y:.0f}", (x, y), textcoords="offset points", xytext=(3, 5), fontsize=7)

fig.suptitle("Step 7 (rerun), instance b2 -- bracketing-gap reference distribution. Proposal only; not adopted.",
             fontsize=10)
fig.tight_layout()
fig.savefig(ART / "step7-gap-distribution-b2.png", dpi=150)
print("chart written")
