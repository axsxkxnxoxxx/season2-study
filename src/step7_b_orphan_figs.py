"""Step 7 instance A - gap distribution chart + threshold sensitivity sweep."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P7 = ROOT / "processed" / "step7" / "a"
ART = ROOT / "artifacts"
DAY = 86400.0

gd = json.load(open(P7 / "gap_distribution.json"))
pooled = np.load(P7 / "gaps_days.npy")
det = pd.read_csv(P7 / "pair_liveness.csv")
thr = gd["threshold"]["threshold_days"]
p99 = gd["threshold"]["percentile_value_days_continuous"]

# ---------------- chart ----------------
fig, ax = plt.subplots(2, 2, figsize=(13, 9))

# (a) survival function of pooled per-account gaps, log-log
s = np.sort(pooled)
frac = 1.0 - np.arange(s.size) / s.size
sel = np.unique(np.linspace(0, s.size - 1, 60000).astype(int))
ax[0, 0].loglog(np.maximum(s[sel], 1e-6), frac[sel], lw=1.4)
for q, c in [(95, "#bbb"), (99, "#c00"), (99.9, "#999")]:
    v = np.percentile(pooled, q)
    ax[0, 0].axvline(v, color=c, ls="--", lw=1)
    ax[0, 0].text(v, 0.4, f"p{q}={v:.2f}d", rotation=90, fontsize=8, color=c)
ax[0, 0].set_title("(a) Per-account consecutive INSERTION gaps, survival\n"
                   f"all {s.size:,} record-level gaps, 2,549 accounts")
ax[0, 0].set_xlabel("gap (days, log)")
ax[0, 0].set_ylabel("P(gap > x)")
ax[0, 0].grid(alpha=.3, which="both")

# (b) histogram of gaps under 30 days
h = pooled[pooled <= 30]
ax[0, 1].hist(h, bins=300, color="#356", log=True)
ax[0, 1].axvline(p99, color="#c00", lw=1.5)
ax[0, 1].axvline(thr, color="#c00", ls=":", lw=1.5)
ax[0, 1].set_title(f"(b) Gaps <= 30 days ({h.size/pooled.size:.3%} of gaps)\n"
                   f"solid = p99 {p99:.4f}d, dotted = threshold {thr}d (ceiling)")
ax[0, 1].set_xlabel("gap (days)")
ax[0, 1].set_ylabel("records (log)")
ax[0, 1].grid(alpha=.3)

# (c) the bracketing gap actually tested, vs the pooled distribution
b = det.loc[det.in_analysis_pop & det.bracket_gap_days.notna(), "bracket_gap_days"].values
sb = np.sort(b)
ax[1, 0].loglog(np.maximum(sb, 1e-6), 1 - np.arange(sb.size) / sb.size,
                lw=1.5, label=f"bracketing gap at tau1 (n={sb.size:,})")
ax[1, 0].loglog(np.maximum(s[sel], 1e-6), frac[sel], lw=1.2, alpha=.7,
                label="pooled per-account gaps")
ax[1, 0].axvline(thr, color="#c00", ls=":", lw=1.5)
ax[1, 0].set_title("(c) Length bias: the gap the rule tests is NOT a\n"
                   "uniform draw from the pooled distribution")
ax[1, 0].set_xlabel("gap (days, log)")
ax[1, 0].set_ylabel("P(gap > x)")
ax[1, 0].legend(fontsize=8)
ax[1, 0].grid(alpha=.3, which="both")

# (d) threshold sweep
grid = [1, 2, 3, 4, 6, 8, 12, 19, 30, 45, 60, 90, 120, 180, 365]
m = det.in_analysis_pop.values
gapv = det.bracket_gap_days.values
st = det.state.values
rows = []
for t in grid:
    live = int((m & (st <= 1) & np.isfinite(gapv) & (gapv < t)).sum())
    rows.append((t, live, live / m.sum()))
ax[1, 1].plot([r[0] for r in rows], [r[2] for r in rows], "o-")
ax[1, 1].axvline(thr, color="#c00", ls=":", lw=1.5)
ax[1, 1].set_xscale("log")
ax[1, 1].set_title("(d) Live share of the 201,900 analysis pairs\nvs threshold (days)")
ax[1, 1].set_xlabel("threshold (days, log)")
ax[1, 1].set_ylabel("live share")
ax[1, 1].set_ylim(0, 1)
ax[1, 1].grid(alpha=.3)

fig.suptitle("Step 7 instance A - liveness gap distribution and threshold "
             f"(99th percentile, ceiling = {thr} days)", fontsize=12)
fig.tight_layout()
fig.savefig(ART / "step7-gap-distribution-a.png", dpi=140)
print("wrote", ART / "step7-gap-distribution-a.png")

sweep = {str(t): {"live_pairs": lv, "live_share": round(sh, 6)} for t, lv, sh in rows}
pct_sweep = {}
for q in [90, 95, 97.5, 99, 99.5, 99.9]:
    v = float(np.percentile(pooled, q))
    t = int(np.ceil(v))
    live = int((m & (st <= 1) & np.isfinite(gapv) & (gapv < t)).sum())
    pct_sweep[str(q)] = {"percentile_days": v, "threshold_ceiling_days": t,
                         "live_pairs_analysis_pop": live,
                         "live_share": round(live / m.sum(), 6)}
json.dump({"threshold_sweep_days": sweep, "percentile_sweep": pct_sweep},
          open(P7 / "sensitivity.json", "w"), indent=2)
print(json.dumps(pct_sweep, indent=2))
