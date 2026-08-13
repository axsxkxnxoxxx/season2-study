"""Step 7 (rerun), instance A2 — the gap distribution chart.
Aggregates only: histograms, ECDFs and derived curves. No user-level data. Zero API calls."""
import json
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/a2")
ART = os.path.join(ROOT, "artifacts")
SEC_PER_DAY = 86400.0


def ecdf(x, n=4000):
    xs = np.sort(x)
    q = np.linspace(0, 1, n)
    return np.quantile(xs, q), q


def main():
    pb = np.load(os.path.join(OUT, "pair_bracketing.npz"))
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    sw = json.load(open(os.path.join(OUT, "sweeps.json")))
    su = json.load(open(os.path.join(OUT, "bracketing_summary.json")))

    g, w1, w5 = pb["gap_days"], pb["w1"], pb["w5"]
    meas = ~np.isnan(g)
    g1, g5 = g[w1 & meas], g[w5 & meas]
    thr1 = su["by_population"]["analysis_population_201900"]["p99_pair_weighted_ceil_days"]
    thr5 = su["by_population"]["w_estimation_sample_128099"]["p99_pair_weighted_ceil_days"]
    pooled_thr = su["pooled_reference_WITHDRAWN"]["p99_ceil_days"]

    fig, ax = plt.subplots(2, 2, figsize=(14, 10))

    # (1) bracketing-gap histogram, log x
    a = ax[0, 0]
    bins = np.logspace(np.log10(1e-5), np.log10(max(g1.max(), 1)), 90)
    a.hist(g1, bins=bins, color="#4477aa", alpha=.75, label="analysis population (201,900)")
    a.hist(g5, bins=bins, histtype="step", color="#cc3311", lw=1.6,
           label="clean estimation sample (128,099)")
    a.axvline(thr1, color="#4477aa", ls="--", lw=1.4, label=f"99th pctl = {thr1} d")
    a.axvline(thr5, color="#cc3311", ls=":", lw=1.6, label=f"99th pctl = {thr5} d")
    a.axvline(pooled_thr, color="k", ls="-.", lw=1.2,
              label=f"WITHDRAWN pooled 99th = {pooled_thr} d")
    a.set_xscale("log")
    a.set_xlabel("bracketing gap (days, log scale)")
    a.set_ylabel("pairs")
    a.set_title("A. Bracketing-gap distribution — the corrected reference distribution\n"
                "gap between the last insertion instant at or before $\\tau_1$ and the first after it")
    a.legend(fontsize=8)

    # (2) pooled vs bracketing ECDF — the length bias
    a = ax[0, 1]
    xp, qp = ecdf(pooled)
    xb, qb = ecdf(g1)
    a.plot(np.maximum(xp, 1e-7), qp, color="#999999", lw=2, label="POOLED gaps (25.86M)")
    a.plot(np.maximum(xb, 1e-7), qb, color="#4477aa", lw=2, label="BRACKETING gaps (157,995)")
    a.axvline(pooled_thr, color="k", ls="-.", lw=1.2, label=f"pooled 99th = {pooled_thr} d")
    frac = float((g1 >= pooled_thr).mean())
    a.axhline(1 - frac, color="#cc3311", ls=":", lw=1.2)
    a.annotate(f"{frac*100:.1f}% of bracketing gaps\nexceed the pooled 99th",
               xy=(pooled_thr, 1 - frac), xytext=(30, 0.35), fontsize=9,
               arrowprops=dict(arrowstyle="->", color="#cc3311"), color="#cc3311")
    a.set_xscale("log")
    a.set_xlabel("gap (days, log scale)")
    a.set_ylabel("cumulative share")
    a.set_title("B. The length bias, measured\nthe reference distribution and the test statistic "
                "were not the same object")
    a.legend(fontsize=8, loc="upper left")

    # (3) percentile -> threshold, corrected basis
    a = ax[1, 0]
    for key, col, lab in (("analysis_population_201900", "#4477aa", "201,900"),
                          ("w_estimation_sample_128099", "#cc3311", "128,099")):
        rows = sw["percentile_sweep_corrected_basis"][key]
        a.plot([r["percentile"] for r in rows], [r["threshold_days_ceil"] for r in rows],
               "o-", color=col, label=lab)
        for r in rows:
            a.annotate(f'{r["threshold_days_ceil"]}', (r["percentile"], r["threshold_days_ceil"]),
                       textcoords="offset points", xytext=(4, 4), fontsize=7, color=col)
    a.axvline(99, color="k", ls="--", lw=1, label="99th (standing ruling)")
    a.set_xlabel("percentile taken on the bracketing distribution")
    a.set_ylabel("threshold (days, ceiling)")
    a.set_title("C. Under the corrected basis the percentile IS the exclusion rate\n"
                "failure rate on measured gaps = 100 - percentile, by construction")
    a.legend(fontsize=8)

    # (4) W sensitivity of the threshold
    a = ax[1, 1]
    ws = sorted(int(k.split("=")[1]) for k in sw["W_sensitivity_of_threshold"])
    for key, col, lab in (("analysis_population_201900", "#4477aa", "201,900"),
                          ("w_estimation_sample_128099", "#cc3311", "128,099")):
        y = [sw["W_sensitivity_of_threshold"][f"W={w}"][key]["p99_ceil_days"] for w in ws]
        a.plot(ws, y, "o-", color=col, label=lab)
        for w, v in zip(ws, y):
            a.annotate(str(v), (w, v), textcoords="offset points", xytext=(4, 4),
                       fontsize=7, color=col)
    a.axvline(108, color="k", ls="--", lw=1, label="W = 108 (adopted)")
    a.set_xlabel("W (days) used to place $\\tau_1$")
    a.set_ylabel("99th-percentile threshold (days, ceiling)")
    a.set_title("D. The corrected threshold is a function of W\n"
                "the standing 'derive independently of W' instruction is now unsatisfiable")
    a.legend(fontsize=8)

    fig.suptitle("Step 7 (rerun), instance A2 — liveness gap distributions, corrected reference "
                 "distribution (decisions/0037). Proposal only; not adopted.", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    path = os.path.join(ART, "step7-gap-distribution-a2.png")
    fig.savefig(path, dpi=140)
    print("wrote", path)


if __name__ == "__main__":
    main()
