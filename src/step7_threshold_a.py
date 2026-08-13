"""Step 7 (instance a), stage 2: the threshold, its sensitivities, and the chart.

Threshold = 99th percentile of the observed gap distribution (decisions/0036),
on continuous instant differences (decisions/0029), rounded UP (decisions/0025).
"""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P7 = ROOT / "processed" / "step7" / "a"
ART = ROOT / "artifacts"
PCTL = 99.0

g = np.load(P7 / "gaps.npz")
gaps_all = g["gaps_all"].astype("float64")
gaps_dis = g["gaps_distinct"].astype("float64")

s1 = json.loads((P7 / "stage1.json").read_text())
out = {"step": 7, "stage": 2, "instance": "a", "percentile": PCTL, "api_calls": 0}

# ---- per-user gap counts, and a user-equal-weighted variant ------------------
ui = np.load(P7 / "user_instants.npz")
u_s = ui["user"]
same = u_s[1:] == u_s[:-1]
gu = u_s[1:][same]                       # owning user of each all-records gap
assert gu.size == gaps_all.size
uu, cnt = np.unique(gu, return_counts=True)
out["gaps_per_user"] = {
    "n_users_with_gaps": int(uu.size),
    "min": int(cnt.min()), "median": float(np.median(cnt)),
    "mean": float(cnt.mean()), "p90": float(np.percentile(cnt, 90)),
    "max": int(cnt.max()),
}

# weight every ACCOUNT equally rather than every gap equally
w = np.repeat(1.0 / cnt, cnt)            # gu is sorted by user (lexsort)
o = np.argsort(gaps_all, kind="stable")
gs, ws = gaps_all[o], w[o]
cw = np.cumsum(ws) / ws.sum()
p_userw = float(gs[np.searchsorted(cw, PCTL / 100.0)])

variants = {
    "A_all_consecutive_records_gap_weighted": float(np.percentile(gaps_all, PCTL)),
    "B_distinct_insertion_instants_gap_weighted": float(np.percentile(gaps_dis, PCTL)),
    "C_all_consecutive_records_user_equal_weighted": p_userw,
}
out["p99_variants_days"] = variants
out["p99_variants_ceiling_days"] = {k: int(math.ceil(v)) for k, v in variants.items()}

# adopted: variant A, the literal reading of the spec
raw = variants["A_all_consecutive_records_gap_weighted"]
out["threshold_raw_days"] = raw
out["threshold_days"] = int(math.ceil(raw))

# ---- neighbouring percentiles, for the Human Lead's sensitivity --------------
out["percentile_curve_days"] = {
    str(q): {"raw": float(np.percentile(gaps_all, q)),
             "ceil": int(math.ceil(np.percentile(gaps_all, q)))}
    for q in [90, 95, 97, 98, 99, 99.5, 99.9, 99.99]
}

# ---- distribution-free CI for the 99th percentile (order statistics) ---------
n = gaps_all.size
p = PCTL / 100.0
sd = math.sqrt(n * p * (1 - p))
lo_r = max(int(math.floor(n * p - 1.96 * sd)), 0)
hi_r = min(int(math.ceil(n * p + 1.96 * sd)), n - 1)
srt = np.sort(gaps_all)
out["p99_ci95_days"] = {"lo": float(srt[lo_r]), "hi": float(srt[hi_r]),
                        "method": "normal-approx binomial order statistics"}

# ---- chart -------------------------------------------------------------------
edges, hall = g["hist_edges"], g["hist_all"]
fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.8))

centers = np.sqrt(np.maximum(edges[:-1], 1e-7) * edges[1:])
ax[0].step(centers, hall, where="mid", color="#22506e")
ax[0].set_xscale("log"); ax[0].set_yscale("log")
ax[0].axvline(out["threshold_days"], color="#c0392b", lw=2,
              label=f"threshold = {out['threshold_days']} d (ceil of p99 = {raw:.4f} d)")
ax[0].set_xlabel("gap between consecutive insertion instants (days, log)")
ax[0].set_ylabel("gaps (log)")
ax[0].set_title("Step 7a: observed gap distribution\n%d gaps, %d accounts" %
                (n, uu.size))
ax[0].legend(fontsize=8, loc="upper right")

q = np.linspace(90, 100, 1001)
vals = np.percentile(gaps_all, q)
ax[1].plot(q, vals, color="#22506e")
ax[1].axvline(99, color="#c0392b", lw=1.5, ls="--")
ax[1].axhline(raw, color="#c0392b", lw=1.5, ls="--",
              label=f"p99 = {raw:.4f} d -> ceil {out['threshold_days']} d")
ax[1].set_yscale("log")
ax[1].set_xlabel("percentile of the gap distribution")
ax[1].set_ylabel("gap (days, log)")
ax[1].set_title("Upper tail: percentile -> gap length\n(a named percentile, not a curve feature)")
ax[1].legend(fontsize=8, loc="upper left")

fig.tight_layout()
fig.savefig(ART / "step7-gap-distribution-a.png", dpi=150)
plt.close(fig)

(P7 / "stage2.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
