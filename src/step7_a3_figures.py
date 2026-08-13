"""Step 7 (frozen-spec run), instance A3 — the gap distribution chart.

Aggregates only: histogram counts and curves. No user identifiers reach artifacts/.
Zero API calls.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from step7_a3_bracketing import OUT, P5, PUBLISHED_WATERFALL, FROZEN_LINE, build_waterfall

ART = "/Users/alyanashantel/Documents/season2-study/artifacts"
THR = 632


def main():
    br = np.load(os.path.join(OUT, "pair_bracketing_W108.npz"))
    ref = br["ref"]
    gap = br["gap_days"]
    g = gap[ref & ~br["no_before"] & ~br["no_after"]]
    pooled = np.load(os.path.join(OUT, "pooled_gaps.npz"))["gap_days"]
    arms = json.load(open(os.path.join(OUT, "arms_and_diagnostics.json")))["arms_refitted"]

    fig, ax = plt.subplots(2, 2, figsize=(13.5, 9))

    # (a) log-spaced histogram, bracketing vs pooled, density so the two are comparable
    lo = min(g.min(), pooled.min())
    bins = np.logspace(np.log10(max(lo, 1e-7)), np.log10(g.max() * 1.05), 90)
    a = ax[0, 0]
    a.hist(pooled, bins=bins, density=True, alpha=0.45, color="#999999",
           label=f"pooled gaps, all accounts (n={pooled.size:,})")
    a.hist(g, bins=bins, density=True, alpha=0.75, color="#1f77b4",
           label=f"bracketing gap, one per pair (n={g.size:,})")
    a.axvline(THR, color="crimson", lw=2,
              label=f"proposed threshold {THR} d = 99th of bracketing")
    a.axvline(4, color="darkorange", lw=1.4, ls="--",
              label="withdrawn pooled-99th basis (4 d)")
    a.set_xscale("log")
    a.set_yscale("log")
    a.set_xlabel("gap between consecutive distinct insertion instants (days, log)")
    a.set_ylabel("density (log)")
    a.set_title("(a) The reference distribution and the test statistic are different objects\n"
                "length bias moves the median from 0.0000007 d to 1.88 d")
    a.legend(fontsize=7.5, loc="lower left")

    # (b) survival curve of the bracketing gap, with the quota read off it
    xs = np.sort(g)
    surv = 1.0 - np.arange(xs.size) / xs.size
    b = ax[0, 1]
    b.plot(xs, surv, color="#1f77b4", lw=1.8)
    b.axvline(THR, color="crimson", lw=2)
    b.axhline(0.01, color="crimson", lw=1, ls=":")
    b.set_xscale("log")
    b.set_yscale("log")
    b.set_xlabel("bracketing gap (days, log)")
    b.set_ylabel("share of pairs with a longer gap (log)")
    b.set_title("(b) The QUOTA PROPERTY, drawn\nthe threshold is read off the y-axis, "
                "not off any feature of the curve")
    b.annotate("pick 1% here ->  read 632 d there", xy=(THR, 0.01),
               xytext=(1.5, 0.0025), fontsize=8,
               arrowprops=dict(arrowstyle="->", color="crimson"))

    # (c) inertness: who does the excluding
    c = ax[1, 0]
    inert = json.load(open(os.path.join(OUT, "bracketing_W108.json")))[
        "inertness_by_percentile"]
    qs = list(inert.keys())
    meas = [inert[q]["not_live_measured_gap"] for q in qs]
    edge = [inert[q]["not_live_edge_cases"] for q in qs]
    x = np.arange(len(qs))
    c.bar(x, edge, color="#999999", label="0036 SS2.3 edge cases (no evidence either side)")
    c.bar(x, meas, bottom=edge, color="#1f77b4", label="measured-gap test")
    for i, q in enumerate(qs):
        c.text(i, edge[i] + meas[i] + 400,
               f"{100 * inert[q]['measured_gap_share_of_exclusions']:.1f}%",
               ha="center", fontsize=8, color="#1f77b4")
    c.set_xticks(x)
    c.set_xticklabels([f"{q}th\n{inert[q]['threshold_days']} d" for q in qs], fontsize=8)
    c.set_ylabel("pairs excluded as not live")
    c.set_title("(c) THE INERTNESS: the threshold does 5.4% of the work at the 99th\n"
                "labelled share = measured-gap test's share of exclusions")
    c.legend(fontsize=8, loc="lower left")

    # (d) the W-coupling
    d = ax[1, 1]
    ws = [int(k) for k in arms]
    thrs = [arms[k]["refitted_threshold_days"] for k in arms]
    rates = [100 * arms[k]["realised_exclusion_rate_measured_gap_pairs"] for k in arms]
    d.plot(ws, thrs, "o-", color="#1f77b4", lw=2)
    for w, t in zip(ws, thrs):
        d.annotate(f"{t} d", (w, t), textcoords="offset points", xytext=(0, 7),
                   ha="center", fontsize=8)
    d.set_xlabel("W (days) — Step 13 arms")
    d.set_ylabel("refitted threshold (days)", color="#1f77b4")
    d2 = d.twinx()
    d2.plot(ws, rates, "s--", color="crimson", lw=1.4)
    d2.set_ylabel("realised exclusion rate, measured-gap pairs (%)", color="crimson")
    d2.set_ylim(0, 2)
    d.axvline(108, color="green", lw=1, ls=":")
    d.set_title("(d) The threshold is a FUNCTION OF W (0038 SS6)\n"
                "the rate is pinned at ~1% at every arm — that is the quota, not a finding")

    fig.suptitle("Step 7 (instance a3) — bracketing-gap distribution on the frozen reference "
                 "population (152,126 pairs), W = 108 d, 99th percentile, ceiling",
                 fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(ART, "step7-gap-distribution-a3.png")
    fig.savefig(out, dpi=145)
    print("wrote", out)


if __name__ == "__main__":
    main()
