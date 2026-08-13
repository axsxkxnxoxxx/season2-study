"""Step 7 (instance a), stage 3: apply the liveness rule and count the pairs.

Rule (task-sheet Step 7; decisions/0036 sec 2): for each user-show pair take that
pair's own tau1 = [[T0]] + W*24h with W = 108 (decisions/0026), find the LAST
insertion instant at or before tau1 and the FIRST insertion instant after tau1 on
that account, and test THAT ONE GAP against the threshold.  Evidence is
account-wide (all shows, all movies); the test is pair-level.
"""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
P7 = ROOT / "processed" / "step7" / "a"
DAY = 86400.0
W = 108                    # decisions/0026, the adopted value
BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
TAU_PULL = float(np.datetime64("2026-08-11", "s").astype(np.int64))

out = {"step": 7, "stage": 3, "instance": "a", "W_days": W, "api_calls": 0}
th = json.loads((P7 / "stage2.json").read_text())
THRESH_D = th["threshold_days"]
out["threshold_days"] = THRESH_D
out["threshold_raw_days"] = th["threshold_raw_days"]

# ---------------- 1. rebuild the Step 5 population, assert the waterfall -----
cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
        "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
        "first_s2_corrupt", "t0"]
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
waterfall = [int(x.sum()) for x in (w1, w2, w3, w4, w5)]
out["step5_waterfall"] = {"computed": waterfall, "published": PUBLISHED_WATERFALL,
                          "match": waterfall == PUBLISHED_WATERFALL}
assert waterfall == PUBLISHED_WATERFALL, waterfall

pop = p.loc[w1].copy()                      # analysis population, 201,900 pairs
out["population"] = {"label": "Step 5 analysis population (waterfall line 1)",
                     "n_pairs": int(len(pop)),
                     "n_users": int(pop.user_idx.nunique())}

# ---------------- 2. tau1 per pair -------------------------------------------
# [[T0]] = UTC midnight opening the T0 calendar date (Step 1 sec 2.4, half-open)
t0_mid = (pd.to_datetime(pop.t0, utc=True).values
          .astype("datetime64[s]").astype("int64").astype("float64"))
assert 1.0e9 < t0_mid.max() < 2.0e9, t0_mid.max()
tau1 = t0_mid + W * DAY
pop["tau1"] = tau1

# ---------------- 3. bracketing gap ------------------------------------------
ui = np.load(P7 / "user_instants.npz")
u_s, ins_s = ui["user"], ui["ins"]          # sorted by (user, rid); ins ascending
starts = np.searchsorted(u_s, np.arange(u_s[-1] + 2), side="left")

uidx = pop.user_idx.values.astype("int64")
n = len(pop)
last_before = np.full(n, np.nan)
first_after = np.full(n, np.nan)

o = np.argsort(uidx, kind="stable")
uo, tauo = uidx[o], tau1[o]
bnds = np.searchsorted(uo, np.arange(uo[-1] + 2), side="left")
lb = np.full(n, np.nan)
fa = np.full(n, np.nan)
for u in np.unique(uo):
    a, b = bnds[u], bnds[u + 1]
    s, e = starts[u], starts[u + 1]
    arr = ins_s[s:e]
    if arr.size == 0:
        continue
    t = tauo[a:b]
    j = np.searchsorted(arr, t, side="right")     # count of instants <= t
    lb[a:b] = np.where(j > 0, arr[np.clip(j - 1, 0, arr.size - 1)], np.nan)
    fa[a:b] = np.where(j < arr.size, arr[np.clip(j, 0, arr.size - 1)], np.nan)
inv = np.empty(n, dtype="int64"); inv[o] = np.arange(n)
last_before, first_after = lb[inv], fa[inv]

out["pairs_with_user_absent_from_scan"] = int(
    np.isnan(last_before).sum() and 0)  # placeholder, resolved below

no_before = np.isnan(last_before)
no_after = np.isnan(first_after) & ~no_before
measured = ~no_before & ~no_after
gap_d = np.full(n, np.nan)
gap_d[measured] = (first_after[measured] - last_before[measured]) / DAY

live = measured & (gap_d < THRESH_D)
dead_gap = measured & (gap_d >= THRESH_D)

out["counts"] = {
    "pairs_total": int(n),
    "live": int(live.sum()),
    "not_live_measured_gap_ge_threshold": int(dead_gap.sum()),
    "not_live_no_instant_after_tau1": int(no_after.sum()),
    "not_live_no_instant_at_or_before_tau1": int(no_before.sum()),
}
out["counts"]["not_live_total"] = (out["counts"]["not_live_measured_gap_ge_threshold"]
                                   + out["counts"]["not_live_no_instant_after_tau1"]
                                   + out["counts"]["not_live_no_instant_at_or_before_tau1"])
out["shares"] = {k: round(v / n, 6) for k, v in out["counts"].items() if k != "pairs_total"}
out["live_users_note"] = {
    "users_with_at_least_one_live_pair": int(pop.user_idx[live].nunique()),
    "users_with_at_least_one_not_live_pair": int(pop.user_idx[~live].nunique()),
    "users_that_are_mixed": int(len(set(pop.user_idx[live]) & set(pop.user_idx[~live]))),
}

# ---------------- 4. right-censoring interaction ------------------------------
censored = tau1 > TAU_PULL
out["tau1_vs_pull"] = {
    "pull_instant_utc": "2026-08-11T00:00:00Z",
    "pairs_with_tau1_after_pull": int(censored.sum()),
    "of_which_no_instant_after_tau1": int((censored & no_after).sum()),
    "no_instant_after_tau1_with_tau1_before_pull": int((~censored & no_after).sum()),
}
sub = ~censored
out["counts_on_tau1_observable_subset"] = {
    "pairs_total": int(sub.sum()),
    "live": int((live & sub).sum()),
    "not_live_measured_gap_ge_threshold": int((dead_gap & sub).sum()),
    "not_live_no_instant_after_tau1": int((no_after & sub).sum()),
    "not_live_no_instant_at_or_before_tau1": int((no_before & sub).sum()),
}

# ---------------- 5. the bracketing-gap distribution vs the reference ---------
bg = gap_d[measured]
out["bracketing_gap_days"] = {
    "n": int(bg.size),
    "median": float(np.median(bg)),
    "mean": float(bg.mean()),
    "percentiles": {str(q): float(np.percentile(bg, q))
                    for q in [10, 25, 50, 75, 90, 95, 99]},
    "share_ge_threshold": float((bg >= THRESH_D).mean()),
    "note": ("the bracketing gap is LENGTH-BIASED: a longer gap is more likely to "
             "contain an arbitrary instant, so this distribution sits far above the "
             "reference gap distribution the threshold was read off"),
}

# ---------------- 6. threshold sensitivity (for Step 13) ----------------------
sens = {}
for q, t in th["percentile_curve_days"].items():
    T = t["ceil"]
    sens[q] = {"threshold_days": T,
               "live": int((measured & (gap_d < T)).sum()),
               "not_live_measured_gap": int((measured & (gap_d >= T)).sum())}
out["threshold_sensitivity"] = sens

# ---------------- 7. row-level detail -> processed/ only ----------------------
det = pd.DataFrame({
    "user_idx": pop.user_idx.values,
    "show_trakt_id": pop.show_trakt_id.values,
    "tau1": tau1,
    "last_instant_at_or_before_tau1": last_before,
    "first_instant_after_tau1": first_after,
    "bracketing_gap_days": gap_d,
    "status": np.select([live, dead_gap, no_after, no_before],
                        ["live", "not_live_gap", "not_live_no_after",
                         "not_live_no_before"], default="ERROR"),
})
assert (det.status == "ERROR").sum() == 0
det.to_csv(P7 / "pair_liveness.csv", index=False)
out.pop("pairs_with_user_absent_from_scan")

(P7 / "stage3.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
