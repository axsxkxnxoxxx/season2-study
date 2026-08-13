"""Step 7 (rerun), instance b2 -- stage 2: the bracketing-gap distribution.

For each user-show pair in the 201,900 analysis population:
  tau1 = floor_to_UTC_midnight(T0) + W * 24h,  W = 108 (decisions/0026)
  last insertion instant <= tau1, first insertion instant > tau1, on that
  ACCOUNT's whole sweep (decisions/0036 s2). That one gap is the test statistic
  and -- per decisions/0037 s1 -- its own distribution is the reference.

Zero API calls.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b2"
DAY = 86400.0
W = 108                      # decisions/0026, adopted; NOT an input to the threshold
BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()   # decisions/0011

p = pd.read_csv(P5 / "pair_revision5.csv")
has_s2 = p.s2_ev_n.values > 0
t0c = p.t0_contaminated.values.astype(bool)
postd = (p.complete_rec_lag_days < POSTDATE_D).values
all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
keep = ~(all_air | (t0c & ~has_s2))
fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                    | (p.first_s2_airdate.values == 1)
                    | (p.first_s2_corrupt.values == 1))
w = [keep]
for m in (has_s2, ~t0c, ~postd, ~fs2_bad):
    w.append(w[-1] & m)
waterfall = [int(x.sum()) for x in w]
assert waterfall == PUBLISHED_WATERFALL, f"waterfall drift: {waterfall}"

pop = p.loc[w[0], ["user_idx", "show_trakt_id", "t0"]].copy()   # 201,900
clean = w[-1][w[0].nonzero()[0]] if False else None
pop["in_est_sample"] = w[-1][w[0]]
pop["t0_clean"] = (~t0c & ~postd)[w[0]]
assert pop.t0.notna().all(), "null T0 in the analysis population"

t0_mid = ((pd.to_datetime(pop.t0, utc=True) - pd.Timestamp("1970-01-01", tz="UTC"))
          .dt.total_seconds().values)
tau1 = t0_mid + W * DAY

iz = np.load(OUT / "instants.npz")
users, starts, counts, inst = iz["users"], iz["starts"], iz["counts"], iz["inst"]
pos = {int(u): i for i, u in enumerate(users)}

n = len(pop)
gap = np.full(n, np.nan)
state = np.zeros(n, dtype=np.int8)   # 0 measured, 1 none-after, 2 none-at-or-before, 3 account absent
uidx = pop.user_idx.values
for u in np.unique(uidx):
    sel = np.nonzero(uidx == u)[0]
    j = pos.get(int(u))
    if j is None:
        state[sel] = 3
        continue
    arr = inst[starts[j]:starts[j] + counts[j]]
    k = np.searchsorted(arr, tau1[sel], side="right")
    none_before = k == 0
    none_after = k == len(arr)
    meas = ~none_before & ~none_after
    state[sel[none_before]] = 2
    state[sel[none_after & ~none_before]] = 1
    km = k[meas]
    gap[sel[meas]] = (arr[km] - arr[km - 1]) / DAY

pop["tau1"] = tau1
pop["gap_days"] = gap
pop["state"] = state
pop["tau1_after_pull"] = tau1 > TAU_PULL
pop.to_csv(OUT / "pair_bracket.csv", index=False)

meas = state == 0
summary = {
    "W_used_for_tau1": W,
    "analysis_population": int(n),
    "measured_gap": int(meas.sum()),
    "no_instant_after_tau1": int((state == 1).sum()),
    "no_instant_at_or_before_tau1": int((state == 2).sum()),
    "account_absent_from_sweep": int((state == 3).sum()),
    "no_instant_after_tau1_of_which_tau1_after_pull_date": int(((state == 1) & (tau1 > TAU_PULL)).sum()),
    "bracketing_gap_days": {
        "n": int(meas.sum()),
        "min": float(np.nanmin(gap)),
        "median": float(np.nanpercentile(gap, 50)),
        "mean": float(np.nanmean(gap)),
        "max": float(np.nanmax(gap)),
        "percentiles": {str(q): float(np.nanpercentile(gap, q))
                        for q in [1, 5, 10, 25, 50, 75, 90, 95, 99, 99.5, 99.9]},
    },
}
(OUT / "bracket_summary.json").write_text(json.dumps(summary, indent=1))
print(json.dumps(summary, indent=1))
