"""Step 5 figures. Counts and shares only - safe for artifacts/.

Left panel revised per Red Team C1. The first version plotted each lag band's
raw SHARE as an equal-width bar over bands that are 2 to 9,716 days wide. That
made the wide old-backfill bands look like a rising mound and the narrow middle
bands look like a trough, and the artifact then read a "flat region" off it that
does not exist. Plotted as DENSITY - share per day - the distribution is monotone
decreasing throughout, and the only sharp break is at 7 days.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
ART = ROOT / "artifacts"

d = np.load(P5 / "record_lag.npz")
lag, corrupt, undated = d["lag_days"], d["corrupt"], d["undated"]
L = lag[(~corrupt) & (~undated)]

fig, ax = plt.subplots(1, 2, figsize=(13.5, 4.9))

# ---- panel 1: lag DENSITY, share per day, log-log ------------------------
edges = np.array([-1, 1, 7, 30, 90, 180, 365, 730, 1825, 3650, 13366], dtype=float)
share = np.array([np.mean((L > a) & (L <= b)) * 100 for a, b in zip(edges[:-1], edges[1:])])
width = np.diff(edges)
dens = share / width
centers = np.sqrt(np.maximum(edges[:-1], 0.5) * edges[1:])

ax[0].step(edges[1:], dens, where="pre", color="#2b4c7e", lw=1.8)
ax[0].fill_between(edges[1:], dens, 1e-5, step="pre", color="#2b4c7e", alpha=0.15)
ax[0].set_xscale("log")
ax[0].set_yscale("log")
ax[0].set_xlim(0.55, 14000)
ax[0].set_ylim(4e-4, 200)
ax[0].set_xlabel("backfill lag, days (log)")
ax[0].set_ylabel("density: % of dated records per day (log)")
ax[0].set_title("Backfill lag DENSITY, not raw band share\n"
                f"{len(L):,} dated records - monotone decreasing throughout", fontsize=10)
ax[0].axvline(7, color="#2e7d32", ls="--", lw=1.3)
ax[0].axvline(180, color="#b5442f", ls="--", lw=1.3)
ax[0].annotate("7 d: the only real break (3.8x)", xy=(7, 0.06), xytext=(13, 3.0),
               fontsize=7.5, color="#2e7d32",
               arrowprops=dict(arrowstyle="->", color="#2e7d32", lw=1))
ax[0].annotate("180 d: the chosen threshold.\nA conservative judgment,\nNOT a data-determined break.",
               xy=(180, 0.0199), xytext=(330, 0.9), fontsize=7.5, color="#b5442f",
               arrowprops=dict(arrowstyle="->", color="#b5442f", lw=1))
ax[0].annotate("61.9% of all dated records\nsit in this one band (+/-1 day)",
               xy=(0.95, 30.9), xytext=(1.35, 0.006), fontsize=7.5,
               arrowprops=dict(arrowstyle="->", color="#333333", lw=1))
for a_, b_, s_ in zip(edges[:-1], edges[1:], share):
    ax[0].text(np.sqrt(max(a_, 0.6) * b_), 6.5e-4, f"{s_:.1f}%", ha="center",
               fontsize=6, color="#555555")

# ---- panel 2: weekly insert volume and backfill share --------------------
agg = json.load(open(P5 / "aggregates.json"))
h = agg["weekly_insert_histogram_tail"]
x = [dt.datetime.strptime(r["week_start"], "%Y-%m-%d") for r in h]
ins = [r["inserted"] for r in h]
sh = [r["share"] * 100 for r in h]
ax[1].bar(x, ins, width=5.5, color="#4a6fa5", label="records written that week")
ax[1].set_ylabel("records written (log scale)")
ax[1].set_yscale("log")
ax[1].axvline(dt.datetime(2026, 7, 15), color="#b5442f", ls="--", lw=1.4)
ax[1].text(dt.datetime(2026, 7, 16), 3e6, "TV Time\nshutdown\n15 Jul 2026",
           fontsize=7.5, color="#b5442f")
a2 = ax[1].twinx()
a2.plot(x, sh, color="#b5442f", lw=1.6, marker="o", ms=2.5)
a2.set_ylabel("% of that week's writes that are backfill >180d", color="#b5442f", fontsize=8)
a2.set_ylim(0, 100)
ax[1].set_title("When the history on disk was actually written\n"
                "last 40 weeks before the pull", fontsize=10)
ax[1].tick_params(axis="x", labelsize=7, rotation=30)

plt.tight_layout()
plt.savefig(ART / "step5-contamination-figures.png", dpi=170)
print("wrote", ART / "step5-contamination-figures.png")
print("\nper-day density, % per day:")
for a_, b_, s_, dn in zip(edges[:-1], edges[1:], share, dens):
    print(f"  {a_:>7.0f} to {b_:>6.0f} d  width {b_-a_:>6.0f}  share {s_:>6.3f}%  density {dn:.5f}")
