"""Step 7 (instance b3) -- stage 5: the gap distribution chart.

Aggregate curves and counts only. No user-level anything reaches artifacts/.
Out: artifacts/step7-gap-distribution-b3.png
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b3"
ART = ROOT / "artifacts"

W = 108
PCTL = 99.0
W_ARMS = [46, 77, 108, 150, 213]


def main() -> None:
    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    br = np.load(OUT / "bracket.npz")
    res = json.load(open(OUT / "threshold.json"))
    diag = json.load(open(OUT / "diagnostics.json"))

    state = br[f"state_W{W}"]
    g = br[f"gap_days_W{W}"][state == 0]

    pooled = np.concatenate([np.diff(tau_all[offsets[u]:offsets[u + 1]])
                             for u in range(len(offsets) - 1)
                             if offsets[u + 1] - offsets[u] > 1]) / 86400.0

    thr = res["adopted_arm"]["threshold_days_ceiling"]
    raw = res["adopted_arm"]["threshold_raw_days"]
    pooled99 = res["pooled_gap_distribution_CROSS_CHECK_ONLY"]["p99_days"]

    fig, ax = plt.subplots(2, 3, figsize=(21, 11.5))
    fig.suptitle(
        "Step 7 (instance b3) — liveness threshold. Bracketing-gap distribution on the frozen "
        "reference population (152,126 pairs, waterfall line 4), $W$ = 108 d\n"
        "PROPOSED, NOT ADOPTED — the Human Lead approves this gate",
        fontsize=14.5, y=0.985)

    # --- A: the two distributions, and why they are different objects --------
    a = ax[0, 0]
    edges = np.logspace(np.log10(1e-6), np.log10(4000), 130)
    for x, lab, col in ((pooled, f"pooled — every gap on every account (n={len(pooled):,})", "#999999"),
                        (g, f"BRACKETING — one gap per pair (n={len(g):,})", "#1f77b4")):
        h, _ = np.histogram(x, bins=edges)
        a.step(edges[:-1], h / h.sum(), where="post", label=lab, color=col, lw=1.7)
    a.set_xscale("log")
    a.axvline(pooled99, color="#999999", ls="--", lw=1.4,
              label=f"pooled 99th = {pooled99:.4f} d (WITHDRAWN basis, 0037)")
    a.axvline(thr, color="#d62728", lw=2.0,
              label=f"PROPOSED threshold = {thr} d (bracketing 99th, ceil)")
    a.set_xlabel("gap between consecutive DISTINCT insertion instants, days (log)")
    a.set_ylabel("share of gaps in bin")
    a.set_title("A. The reference distribution and the test statistic\nare not the same object "
                "(decisions/0037 §1)")
    a.legend(fontsize=8.2, loc="upper left")
    a.grid(alpha=0.25, which="both")

    # --- B: ECDF, the length bias measured -----------------------------------
    b = ax[0, 1]
    for x, lab, col in ((pooled, "pooled", "#999999"), (g, "bracketing", "#1f77b4")):
        xs = np.sort(x)
        b.step(xs, np.arange(1, len(xs) + 1) / len(xs), where="post", label=lab, color=col, lw=1.7)
    b.set_xscale("log")
    share = res["length_bias"]["share_of_bracketing_gaps_exceeding_pooled_p99_raw"]
    b.axvline(pooled99, color="#999999", ls="--", lw=1.4)
    b.axvline(thr, color="#d62728", lw=2.0)
    b.axhline(PCTL / 100, color="#d62728", ls=":", lw=1.2)
    b.annotate(f"{share:.1%} of bracketing gaps\nexceed the pooled 99th",
               xy=(pooled99, 1 - share), xytext=(0.03, 0.55), textcoords="axes fraction",
               arrowprops=dict(arrowstyle="->", color="#333333"), fontsize=9.5)
    b.set_ylim(0, 1)
    b.set_xlabel("gap, days (log)")
    b.set_ylabel("cumulative share")
    b.set_title("B. Length bias, measured on this population\n"
                f"pooled median {np.median(pooled):.7f} d  vs  bracketing median {np.median(g):.4f} d")
    b.legend(fontsize=9, loc="lower right")
    b.grid(alpha=0.25, which="both")

    # --- C: the quota property ------------------------------------------------
    c = ax[0, 2]
    qs = np.arange(90, 99.91, 0.1)
    thrs = np.array([math.ceil(np.percentile(g, q)) for q in qs])
    rates = np.array([(g >= t).mean() for t in thrs])
    c.plot(qs, thrs, color="#1f77b4", lw=1.9, label="threshold (days, ceil)")
    c.set_yscale("log")
    c.set_xlabel("percentile chosen")
    c.set_ylabel("threshold, days (log)")
    c2 = c.twinx()
    c2.plot(qs, 100 * rates, color="#d62728", lw=1.9, label="realised exclusion rate")
    c2.plot(qs, 100 - qs, color="#d62728", lw=1.0, ls=":", label="100 − p (the quota)")
    c2.set_ylabel("% of measured-gap pairs excluded", color="#d62728")
    c.axvline(PCTL, color="k", ls="--", lw=1.0)
    c.set_title("C. THE QUOTA PROPERTY\nchoosing p fixes the exclusion rate at 100 − p;\n"
                "the data chooses only which pairs, never how many")
    h1, l1 = c.get_legend_handles_labels()
    h2, l2 = c2.get_legend_handles_labels()
    c.legend(h1 + h2, l1 + l2, fontsize=8.5, loc="center left")
    c.grid(alpha=0.25)

    # --- D: the inertness -----------------------------------------------------
    d = ax[1, 0]
    rows = diag["inertness_claim_test"]["rows"]
    xs = np.arange(len(rows))
    m = np.array([r["measured_gap_exclusions"] for r in rows])
    e = np.array([r["edge_case_exclusions"] for r in rows])
    d.bar(xs, m, color="#d62728", label="measured bracketing gap ≥ threshold")
    d.bar(xs, e, bottom=m, color="#7f7f7f", label="0036 §2.3 edge cases (fixed at 22,496)")
    for i, r in enumerate(rows):
        d.text(i, m[i] + e[i] + 700, f"{r['share_measured']:.1%}", ha="center", fontsize=8)
    d.set_xticks(xs)
    d.set_xticklabels([str(r["percentile"]) for r in rows], rotation=45, fontsize=8.5)
    d.set_xlabel("percentile")
    d.set_ylabel("pairs excluded")
    d.set_title("D. THE INERTNESS — and its stated invariance FAILS here\n"
                "measured-gap share runs 36.5% (p90) → 5.4% (p99) → 0.4% (p99.9),\n"
                "not a flat 3.45%")
    d.legend(fontsize=8.5, loc="upper right")
    d.grid(alpha=0.25, axis="y")

    # --- E: exclusion waterfall at the proposed threshold ---------------------
    e_ax = ax[1, 1]
    aa = res["adopted_arm"]
    labs = ["live", "not live:\nmeasured gap\n≥ 632 d", "not live:\nno instant\nafter τ₁",
            "not live:\nno instant\nat or before τ₁"]
    vals = [aa["live"], aa["excluded_measured_gap"],
            aa["excluded_no_instant_after_tau1"], aa["excluded_no_instant_at_or_before_tau1"]]
    cols = ["#2ca02c", "#d62728", "#ff7f0e", "#7f7f7f"]
    bars = e_ax.bar(labs, vals, color=cols)
    for bb, v in zip(bars, vals):
        e_ax.text(bb.get_x() + bb.get_width() / 2, v * 1.05, f"{v:,}\n{v/152126:.2%}",
                  ha="center", fontsize=9.5)
    e_ax.set_yscale("log")
    e_ax.set_ylim(500, 400000)
    e_ax.set_ylabel("pairs (log)")
    e_ax.set_title("E. Pair-level outcome of the rule, on the 152,126\n"
                   f"derivation and application populations identical (0038 §2.1)")
    e_ax.grid(alpha=0.25, axis="y")

    # --- F: the W coupling ----------------------------------------------------
    f = ax[1, 2]
    arms = res["W_arms_refitted"]
    wx = [a["W_days"] for a in arms]
    ty = [a["threshold_days_ceiling"] for a in arms]
    f.plot(wx, ty, "o-", color="#1f77b4", lw=1.9)
    for a in arms:
        f.annotate(f"{a['threshold_days_ceiling']} d\n{a['realised_rate_on_measured_gap_pairs']:.2%}",
                   (a["W_days"], a["threshold_days_ceiling"]), textcoords="offset points",
                   xytext=(6, -16), fontsize=9)
    f.axvline(W, color="#d62728", ls="--", lw=1.2, label="adopted W = 108 d")
    f.set_xlabel("W, days (Step 13 arms)")
    f.set_ylabel("refitted threshold, days")
    f.set_title("F. The threshold IS a function of $W$ (0038 §6)\n"
                "576 → 697 d across the arms; Step 13 must refit per arm")
    f.legend(fontsize=9)
    f.grid(alpha=0.25)

    fig.tight_layout(rect=(0, 0, 1, 0.955))
    fig.savefig(ART / "step7-gap-distribution-b3.png", dpi=140)
    plt.close(fig)
    print("wrote artifacts/step7-gap-distribution-b3.png")


if __name__ == "__main__":
    main()
