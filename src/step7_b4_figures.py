"""Step 7 rerun (instance b4) -- stage 5: the gap distribution chart.

READ ONLY. ZERO network calls. Aggregates only -- no account or pair identifiers
appear in any output of this script.

Out: artifacts/step7-liveness-b4-gap-distribution.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b4"
ART = ROOT / "artifacts"
W = 108
ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    thr_j = json.load(open(OUT / "threshold.json"))
    a = thr_j["arms"][str(W)]
    THR = a["reference_set_variants"]["V1_extended_PRIMARY"]["threshold_days_ceiling"]
    boot = json.load(open(OUT / f"bootstrap_W{W}.json"))
    lo, hi = boot["account_clustered"]["ci95_on_ceilinged_threshold_days"]

    z = np.load(OUT / "bracket.npz")
    gap, state, d10 = z[f"gap_days_W{W}"], z[f"state_W{W}"], z[f"d10_W{W}"]
    meas = np.sort(gap[(state == 0) & d10])
    n_open = int(((state == 1) & d10).sum())
    n_ext = len(meas) + n_open

    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    d = np.diff(tau_all) / 86400.0
    b = np.zeros(len(d), dtype=bool)
    b[offsets[1:-1] - 1] = True
    pooled = d[~b]
    pooled_p99 = thr_j["arms"][str(W)]["length_bias"]["pooled_p99_days_raw"]

    fig, ax = plt.subplots(1, 3, figsize=(17, 5.2))

    # --- panel 1: bracketing vs pooled, log10 days ---
    bins = np.linspace(-7, 4, 132)
    ax[0].hist(np.log10(np.clip(pooled, 1e-7, None)), bins=bins, density=True,
               color="0.75", label=f"pooled gaps, all accounts (n={len(pooled):,})")
    ax[0].hist(np.log10(np.clip(meas, 1e-7, None)), bins=bins, density=True,
               histtype="step", lw=2, color="C0",
               label=f"bracketing gap at $\\tau_1$, one per pair (n={len(meas):,})")
    ax[0].axvline(np.log10(THR), color="C3", lw=2,
                  label=f"threshold {THR:.0f} d (99th of extended set)")
    ax[0].axvspan(np.log10(lo), np.log10(hi), color="C3", alpha=0.12,
                  label=f"account-clustered 95% CI [{lo:.0f}, {hi:.0f}]")
    ax[0].axvline(np.log10(pooled_p99), color="C2", ls="--", lw=1.5,
                  label=f"pooled 99th {pooled_p99:.2f} d (withdrawn basis)")
    ax[0].set_xticks([-6, -4, -2, 0, 2, 4])
    ax[0].set_xticklabels(["1 $\\mu$d", "0.0001 d", "0.01 d", "1 d", "100 d", "10,000 d"])
    ax[0].set_xlabel("gap between consecutive distinct insertion instants")
    ax[0].set_ylabel("density (per log$_{10}$ day)")
    ax[0].set_title("Length bias: the bracketing gap is not a pooled gap")
    ax[0].legend(fontsize=7.5, loc="upper left")

    # --- panel 2: upper tail of the bracketing-gap distribution ---
    q = 1.0 - np.arange(1, len(meas) + 1) / n_ext        # exceedance over the EXTENDED set
    ax[1].plot(meas, q, color="C0", lw=1.6, label="measured bracketing gaps")
    ax[1].axhline(n_open / n_ext, color="0.4", ls=":",
                  label=f"open-ended floor {n_open:,}/{n_ext:,} = {n_open/n_ext:.3%}")
    ax[1].axhline(0.01, color="C3", ls="--", lw=1, label="1% quota (the 99th percentile)")
    ax[1].axvline(THR, color="C3", lw=2)
    ax[1].axvspan(lo, hi, color="C3", alpha=0.12)
    ax[1].set_xscale("log")
    ax[1].set_yscale("log")
    ax[1].set_xlim(1, 4000)
    ax[1].set_ylim(1e-4, 1)
    ax[1].set_xlabel("gap length (days)")
    ax[1].set_ylabel("share of the extended set at or above")
    ax[1].set_title("The 1% quota is mostly spent before the gap test runs")
    ax[1].legend(fontsize=7.5)

    # --- panel 3: threshold vs W ---
    xs, ys, los, his = [], [], [], []
    for w in ARMS:
        v = thr_j["arms"][str(w)]["reference_set_variants"]["V1_extended_PRIMARY"]
        bj = json.load(open(OUT / f"bootstrap_W{w}.json"))["account_clustered"]
        xs.append(w)
        ys.append(v["threshold_days_ceiling"])
        los.append(bj["ci95_on_ceilinged_threshold_days"][0])
        his.append(bj["ci95_on_ceilinged_threshold_days"][1])
    ax[2].fill_between(xs, los, his, color="C3", alpha=0.15, label="account-clustered 95% CI")
    ax[2].plot(xs, ys, "o-", color="C3", label="refitted threshold")
    ax[2].axvline(W, color="0.3", ls=":", label="adopted $W$ = 108 d")
    ax[2].set_xlabel("window $W$ (days)")
    ax[2].set_ylabel("liveness threshold (days)")
    ax[2].set_title("The threshold is a function of $W$ (Step 13 refit)")
    ax[2].legend(fontsize=8)

    fig.suptitle(
        "Step 7 (instance b4) -- bracketing-gap distribution at $\\tau_1$, post-D10 population "
        f"(n = {int(d10.sum()):,} pairs). PROPOSED, NOT ADOPTED.",
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = ART / "step7-liveness-b4-gap-distribution.png"
    fig.savefig(p, dpi=140)
    print("wrote", p)


if __name__ == "__main__":
    main()
