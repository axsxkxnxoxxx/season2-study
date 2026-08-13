"""
Step 7 - liveness threshold and rule. Self-contained, single-file run.

Run tag: ds_run_1254 (2026-08-13 12:54 EDT). This file exists as a single
reproducible unit because another process was writing into the same
processed/step7/a/ namespace and the same src/step7_*_a.py filenames during
this run; everything this script produces goes to
processed/step7/a/_snapshot_ds_run_1254/ so that provenance is unambiguous.

Spec: task-sheet.md Step 7 lines 226-254, as ruled by
  decisions/0036 - threshold = 99th percentile; the test is the single gap
                   BRACKETING tau1, not every gap in the sweep
  decisions/0029 - gap = continuous instant difference between CONSECUTIVE
                   INSERTION INSTANTS on the account, not floored to days
  decisions/0025 - round the threshold UP (ceiling)
  decisions/0021 - liveness runs on INSERTION time, not claimed watched_at
  decisions/0034 - liveness is anchored at tau1; tau2 plays no part
  decisions/0026 - W = 108 days (adopted; NOT the 107 in the Step 6 artifacts)
Calibration curve is READ from processed/step5/calibration.npz. Never refit.
ZERO API calls.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "a" / "_snapshot_ds_run_1254"
ART = ROOT / "artifacts"

PCTL = 99.0
W_DAYS = 108
DAY = 86400.0
BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
TAU_PULL = float(np.datetime64("2026-08-11", "s").astype(np.int64))

OUT.mkdir(parents=True, exist_ok=True)
R = {"step": 7, "run_tag": "ds_run_1254", "api_calls": 0,
     "threshold_percentile": PCTL, "W_days_applied": W_DAYS}

# ---------------------------------------------------------------- 1. instants
z = np.load(P5 / "full_scan.npz")
rid, user, kind = z["rid"], z["user"], z["kind"]
c = np.load(P5 / "calibration.npz")
kr, kt = c["knot_rid"], c["knot_time"]
assert np.all(np.diff(kr) > 0) and np.all(np.diff(kt) >= 0)
ins = np.interp(rid.astype(np.float64), kr, kt)      # clamps outside knot range

R["records"] = {
    "records_total": int(rid.size),
    "accounts_in_scan": int(np.unique(user).size),
    "episode_records": int((kind == 1).sum()),
    "movie_records": int((kind == 0).sum()),
    "rid_below_first_knot_clamped": int((rid < kr.min()).sum()),
    "rid_above_last_knot_clamped": int((rid > kr.max()).sum()),
    "calibration": "processed/step5/calibration.npz, read not refit",
}

# ------------------------------------------------- 2. per-account gap distribution
order = np.lexsort((rid, user))
u_s, i_s = user[order], ins[order]
d = np.diff(i_s)
same = u_s[1:] == u_s[:-1]
gaps_d = np.maximum(d[same], 0.0) / DAY

QS = [50, 75, 90, 95, 97.5, 99, 99.5, 99.9, 100]
R["gap_distribution"] = {
    "unit": "one gap per consecutive pair of records on the same account",
    "n_gaps": int(gaps_d.size),
    "n_accounts": int(np.unique(u_s[1:][same]).size),
    "mean_days": float(gaps_d.mean()),
    "share_under_1_second": float((gaps_d < 1.0 / DAY).mean()),
    "share_under_1_day": float((gaps_d < 1.0).mean()),
    "percentiles_days": {str(q): float(np.percentile(gaps_d, q)) for q in QS},
}
p99 = float(np.percentile(gaps_d, PCTL))
THRESH = int(np.ceil(p99))
R["threshold"] = {"percentile": PCTL, "value_days_continuous": p99,
                  "rounding": "ceiling, decisions/0025", "threshold_days": THRESH,
                  "percentile_interpolation": "numpy default linear"}

# distinct-instant variant, reported as a sensitivity, not adopted
key = u_s.astype(np.int64) * (2 ** 40) + np.round(i_s).astype(np.int64)
keep = np.empty(key.size, bool); keep[0] = True; keep[1:] = key[1:] != key[:-1]
u_dd, i_dd = u_s[keep], i_s[keep]
ddx = np.diff(i_dd); sd = u_dd[1:] == u_dd[:-1]
gaps_dd = np.maximum(ddx[sd], 0.0) / DAY
R["sensitivity_distinct_second_instants"] = {
    "n_gaps": int(gaps_dd.size),
    "percentiles_days": {str(q): float(np.percentile(gaps_dd, q)) for q in QS},
    "threshold_days": int(np.ceil(np.percentile(gaps_dd, PCTL))),
}

# ------------------------------------------------------------- 3. population
cols = ["user_idx", "show_trakt_id", "t0", "t0_contaminated", "s2_ev_n",
        "s2_ev_airdate", "complete_rec_lag_days", "first_s2_lag_days",
        "first_s2_airdate", "first_s2_corrupt"]
p = pd.read_csv(P5 / "pair_revision5.csv", usecols=cols)
has_s2 = (p.s2_ev_n > 0).values
t0c = p.t0_contaminated.values.astype(bool)
postd = (p.complete_rec_lag_days < POSTDATE_D).values
all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
keep_pair = ~(all_air | (t0c & ~has_s2))
fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                    | (p.first_s2_airdate.values == 1)
                    | (p.first_s2_corrupt.values == 1))
w1 = keep_pair
w2 = w1 & has_s2
w3 = w2 & ~t0c
w4 = w3 & ~postd
w5 = w4 & ~fs2_bad
wf = [int(x.sum()) for x in (w1, w2, w3, w4, w5)]
assert wf == PUBLISHED_WATERFALL, wf
R["step5_waterfall"] = {"computed": wf, "published": PUBLISHED_WATERFALL, "match": True}

t0 = pd.to_datetime(p.t0, format="%Y-%m-%d")
tau1 = t0.values.astype("datetime64[s]").astype(np.int64).astype(np.float64) + W_DAYS * DAY

# --------------------------------------------------- 4. the bracketing-gap test
starts = np.searchsorted(u_s, np.arange(int(u_s.max()) + 2), side="left")
uidx = p.user_idx.values.astype(np.int64)
n = len(p)
state = np.zeros(n, np.int8)          # 0 live, 1 dead-measured, 2 no-after, 3 no-before
gap = np.full(n, np.nan)
o = np.argsort(uidx, kind="stable")
uo = uidx[o]
bnd = np.searchsorted(uo, np.arange(int(uo.max()) + 2), side="left")
for u in np.unique(uo):
    a, b = bnd[u], bnd[u + 1]
    rows = o[a:b]
    arr = i_s[starts[u]:starts[u + 1]]
    if arr.size == 0:
        state[rows] = 3
        continue
    t = tau1[rows]
    k = np.searchsorted(arr, t, side="right")     # n of instants <= tau1
    no_before, no_after = k == 0, k == arr.size
    ok = ~no_before & ~no_after
    g = np.full(rows.size, np.nan)
    g[ok] = arr[k[ok]] - arr[k[ok] - 1]
    gap[rows] = g / DAY
    st = np.zeros(rows.size, np.int8)
    st[ok] = np.where(g[ok] < THRESH * DAY, 0, 1)
    st[no_after] = 2
    st[no_before] = 3
    state[rows] = st

LAB = {0: "live", 1: "not_live_measured_gap_ge_threshold",
       2: "not_live_no_instant_after_tau1", 3: "not_live_no_instant_at_or_before_tau1"}


def block(mask, name):
    d = {"n_pairs": int(mask.sum())}
    for k, lab in LAB.items():
        d[lab] = int((mask & (state == k)).sum())
    d["not_live_total"] = d["n_pairs"] - d["live"]
    d["live_share"] = round(d["live"] / d["n_pairs"], 6) if d["n_pairs"] else None
    R.setdefault("counts", {})[name] = d


block(np.ones(n, bool), "frame_all_pairs_220107")
block(w1, "PRIMARY_analysis_population_201900")
block(w2, "has_s2_evidence_178165")
block(w3, "t0_not_contaminated_155131")
block(w5, "w_estimation_sample_128099")
block(w1 & (tau1 <= TAU_PULL), "analysis_pop_tau1_at_or_before_pull")
block(w1 & (tau1 > TAU_PULL), "analysis_pop_tau1_after_pull_censored")
block(w1 & t0c, "analysis_pop_t0_contaminated_subset")

R["pair_level_not_user_level"] = {
    "users_with_at_least_one_live_pair": int(np.unique(uidx[w1 & (state == 0)]).size),
    "users_with_at_least_one_not_live_pair": int(np.unique(uidx[w1 & (state != 0)]).size),
    "users_mixed_live_and_not_live": int(len(
        set(uidx[w1 & (state == 0)].tolist()) & set(uidx[w1 & (state != 0)].tolist()))),
    "users_in_analysis_population": int(np.unique(uidx[w1]).size),
}

m = w1 & (state <= 1) & np.isfinite(gap)
R["bracketing_gap_distribution"] = {
    "n_pairs_with_a_measured_gap": int(m.sum()),
    "median_days": float(np.median(gap[m])),
    "mean_days": float(gap[m].mean()),
    "percentiles_days": {str(q): float(np.percentile(gap[m], q))
                         for q in [10, 25, 50, 75, 90, 95, 99]},
    "share_at_or_above_threshold": float((gap[m] >= THRESH).mean()),
    "length_bias_note": (
        "the gap bracketing a fixed instant is a LENGTH-BIASED draw from the pooled "
        "gap distribution - a long gap covers more calendar time and is therefore far "
        "likelier to contain tau1. The pooled 99th percentile does NOT imply a 1% "
        "failure rate under this rule."),
}

# ------------------------------------------------------- 5. threshold sweep
sw = {}
for q in [90, 95, 97.5, 99, 99.5, 99.9]:
    v = float(np.percentile(gaps_d, q)); t = int(np.ceil(v))
    lv = int((m & (gap < t)).sum())
    sw[str(q)] = {"percentile_days": v, "threshold_ceiling_days": t,
                  "live_pairs": lv, "live_share_of_201900": round(lv / int(w1.sum()), 6)}
R["percentile_sensitivity_on_analysis_population"] = sw
grid = [1, 2, 3, 4, 6, 8, 12, 19, 30, 45, 60, 90, 120, 180, 365]
R["threshold_grid_on_analysis_population"] = {
    str(t): {"live_pairs": int((m & (gap < t)).sum()),
             "live_share": round(int((m & (gap < t)).sum()) / int(w1.sum()), 6)}
    for t in grid}

# ------------------------------------------------------------- 6. row detail
pd.DataFrame({"user_idx": uidx, "show_trakt_id": p.show_trakt_id.values,
              "tau1": tau1, "bracketing_gap_days": gap,
              "status": pd.Series(state).map(LAB).values,
              "in_analysis_population": w1, "in_w5": w5,
              "tau1_at_or_before_pull": tau1 <= TAU_PULL}
             ).to_csv(OUT / "pair_liveness_ds_run_1254.csv", index=False)
np.save(OUT / "pooled_gaps_days.npy", gaps_d)
(OUT / "results.json").write_text(json.dumps(R, indent=2))

# ------------------------------------------------------------------ 7. chart
fig, ax = plt.subplots(2, 2, figsize=(13, 9))
s = np.sort(gaps_d); frac = 1.0 - np.arange(s.size) / s.size
sel = np.unique(np.linspace(0, s.size - 1, 60000).astype(int))
ax[0, 0].loglog(np.maximum(s[sel], 1e-6), frac[sel], lw=1.4)
for q, col in [(95, "#999"), (99, "#c00"), (99.9, "#999")]:
    v = np.percentile(gaps_d, q)
    ax[0, 0].axvline(v, color=col, ls="--", lw=1)
    ax[0, 0].text(v, 0.35, f" p{q}={v:.2f}d", rotation=90, fontsize=8, color=col)
ax[0, 0].set(title="(a) Per-account consecutive INSERTION gaps, survival\n"
                   f"{s.size:,} gaps, {R['gap_distribution']['n_accounts']:,} accounts",
             xlabel="gap (days, log)", ylabel="P(gap > x)")
ax[0, 0].grid(alpha=.3, which="both")

h = gaps_d[gaps_d <= 30]
ax[0, 1].hist(h, bins=300, color="#33556e", log=True)
ax[0, 1].axvline(p99, color="#c00", lw=1.5)
ax[0, 1].axvline(THRESH, color="#c00", ls=":", lw=1.5)
ax[0, 1].set(title=f"(b) Gaps <= 30 days ({h.size / gaps_d.size:.3%} of all gaps)\n"
                   f"solid = p99 {p99:.4f}d   dotted = threshold {THRESH}d (ceiling)",
             xlabel="gap (days)", ylabel="gaps (log)")
ax[0, 1].grid(alpha=.3)

b = np.sort(gap[m])
ax[1, 0].loglog(np.maximum(b, 1e-6), 1 - np.arange(b.size) / b.size, lw=1.5,
                label=f"gap bracketing tau1 (n={b.size:,})")
ax[1, 0].loglog(np.maximum(s[sel], 1e-6), frac[sel], lw=1.2, alpha=.75,
                label="pooled per-account gaps")
ax[1, 0].axvline(THRESH, color="#c00", ls=":", lw=1.5)
ax[1, 0].set(title="(c) Length bias: the gap the rule tests is not a\n"
                   "uniform draw from the pooled distribution",
             xlabel="gap (days, log)", ylabel="P(gap > x)")
ax[1, 0].legend(fontsize=8); ax[1, 0].grid(alpha=.3, which="both")

xs = grid
ys = [R["threshold_grid_on_analysis_population"][str(t)]["live_share"] for t in xs]
ax[1, 1].plot(xs, ys, "o-")
ax[1, 1].axvline(THRESH, color="#c00", ls=":", lw=1.5)
ax[1, 1].set(xscale="log", ylim=(0, 1), xlabel="threshold (days, log)",
             ylabel="live share of 201,900 pairs",
             title="(d) Live share vs threshold\n(measured-gap pairs only; the two "
                   "no-evidence classes never become live)")
ax[1, 1].grid(alpha=.3)

fig.suptitle(f"Step 7 - liveness gap distribution, 99th percentile, threshold = "
             f"{THRESH} days (run ds_run_1254)", fontsize=12)
fig.tight_layout()
fig.savefig(OUT / "step7-gap-distribution.png", dpi=140)
fig.savefig(ART / "step7-gap-distribution-a.png", dpi=140)

print(json.dumps({k: R[k] for k in ("threshold", "counts", "bracketing_gap_distribution",
                                    "pair_level_not_user_level")}, indent=2)[:4000])
print("wrote", OUT)
