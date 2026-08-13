"""Red Team's minimum ask at the Step 6 gate: the 90th percentile of the
time-to-S2-COMPLETION lag, beside the time-to-first-S2-episode lag W was
derived on.

READ ONLY. ZERO API calls. Nothing here changes W, reopens the gate, or
proposes a rule. It computes one number that was never computed.

WHY IT EXISTS
  WRITTEN BEFORE THE AMENDMENT, AND ITS PREMISE IS NOW THE THING THAT CHANGED.
  At the time, Step 1 sec 7 made W govern TWO boundaries on ONE instant:
    Never started   |A| = 0                                        at tau1
    Continued       |A| >= 1 AND F2 in A AND |A| >= ceil(0.90 * L2) at tau1
  That is SUPERSEDED. decisions/0034 moved Continued to tau2 = [T0] + (W+H)*24h,
  evaluated on A_H, precisely because W was doing two jobs that are different
  questions -- which is the finding this script produced. The number it computes
  is unchanged and remains the live provenance for sec 2 of
  artifacts/step1-amendment-continued-boundary.md; only the premise it was
  written against has moved. Retained as written, with the supersession named,
  because the amendment cites this file's output.
  Step 6 derived W from the lag to the FIRST S2 episode only. For any pair
  with L2 >= 2 the time to satisfy the Continued condition strictly exceeds
  the time to the first episode, so the percentile of the second boundary is
  strictly above 107.7135 by an amount nobody had measured.

DEFINITION USED
  Completion instant = the first instant at which the Continued condition
  holds = max( canonical ts of F2 , k-th smallest canonical ts over A_full )
  where A_full is the distinct S2 episodes whose number is a MEMBER of the
  real E2 (Step 1 sec 3.2), k = ceil(0.90 * L2), and the canonical timestamp
  of a distinct episode is the MINIMUM watched_at across its records
  (Step 1 sec 2.2).
  Lag = completion instant - T0, in CONTINUOUS days (decisions/0025).

POPULATION
  The identical Step 5 clean-record estimation sample used by both Step 6
  instances, rebuilt by the same mask and asserted against the published
  waterfall 201,900 -> 178,165 -> 155,131 -> 152,126 -> 128,099.
  The completion lag is only DEFINED for pairs that actually complete S2, so
  its denominator is a subset. That drop is reported, not hidden.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
SCAN = ROOT / "processed" / "s1s2_scan.npz"
OUT = ROOT / "processed" / "step6" / "completion_lag.json"

BACKFILL_D = 180.0
POSTDATE_D = -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
MISSING = np.iinfo(np.int64).min


def pct(a, q=90):
    return float(np.percentile(a, q))


def main():
    # ---------------- 1. rebuild the estimation sample, identical mask
    p = pd.read_csv(P5 / "pair_revision5.csv")
    has_s2 = (p.s2_ev_n.values > 0)
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
    waterfall = [int(w.sum()) for w in (w1, w2, w3, w4, w5)]
    assert waterfall == PUBLISHED_WATERFALL, f"waterfall drift: {waterfall}"
    est = p.loc[w5, ["user_idx", "show_trakt_id", "t0", "s2_distinct"]].copy()

    # ---------------- 2. frame: real E2, L2, F2, cadence bucket
    f = pd.read_csv(P2 / "frame.csv",
                    usecols=["show_trakt_id", "s2_E", "s2_L", "s2_F", "cadence_bucket"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    need = {int(r.show_trakt_id): math.ceil(0.90 * int(r.s2_L)) for r in f.itertuples()}
    fin = {int(r.show_trakt_id): int(r.s2_F) for r in f.itertuples()}
    bucket = dict(zip(f.show_trakt_id.astype(int), f.cadence_bucket))

    # ---------------- 3. canonical S2 timestamps per (user, show, episode)
    z = np.load(SCAN)
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    # Step 1 sec 2.2: canonical timestamp of a DISTINCT episode is min watched_at
    s2 = s2.groupby(["user_idx", "show_trakt_id", "number"], sort=False,
                    as_index=False)["ts"].min()
    # Step 1 sec 3.2: membership by SET against the real E2
    s2["in_e2"] = [n in e2.get(sh, ()) for sh, n in zip(s2.show_trakt_id, s2.number)]
    s2 = s2[s2.in_e2]

    # ---------------- 4. completion instant per pair
    s2 = s2.sort_values(["user_idx", "show_trakt_id", "ts"], kind="stable")
    g = s2.groupby(["user_idx", "show_trakt_id"], sort=False)
    agg = g.agg(n_distinct=("number", "size"), first_ts=("ts", "first")).reset_index()
    # k-th smallest ts, k = ceil(0.9*L2), per pair
    ranked = s2.copy()
    ranked["rank"] = g.cumcount() + 1
    agg["k"] = [need.get(int(sh), 10**9) for sh in agg.show_trakt_id]
    kth = ranked.merge(agg[["user_idx", "show_trakt_id", "k"]],
                       on=["user_idx", "show_trakt_id"])
    kth = kth[kth["rank"] == kth["k"]][["user_idx", "show_trakt_id", "ts"]] \
        .rename(columns={"ts": "kth_ts"})
    # F2's own timestamp
    f2ts = s2[[n == fin.get(int(sh), -1) for sh, n in zip(s2.show_trakt_id, s2.number)]]
    f2ts = f2ts[["user_idx", "show_trakt_id", "ts"]].rename(columns={"ts": "f2_ts"})

    comp = agg.merge(kth, on=["user_idx", "show_trakt_id"], how="left") \
              .merge(f2ts, on=["user_idx", "show_trakt_id"], how="left")
    comp["completes"] = comp.kth_ts.notna() & comp.f2_ts.notna()
    comp["completion_ts"] = np.maximum(comp.kth_ts.fillna(0), comp.f2_ts.fillna(0))

    # ---------------- 5. join to the estimation sample and lag against T0
    # NOT .astype("int64"): on a tz-aware datetime that returns MICROSECONDS in
    # this pandas version, which silently placed every T0 in January 1970 on the
    # first run of this script and produced 20,000-day lags. Subtract the epoch.
    est["t0_ts"] = ((pd.to_datetime(est.t0, utc=True)
                     - pd.Timestamp("1970-01-01", tz="UTC")).dt.total_seconds())
    d = est.merge(comp, on=["user_idx", "show_trakt_id"], how="left")
    # cross-check: our distinct-S2 count must match Step 5's, where it applies
    chk = d.dropna(subset=["n_distinct"])
    mismatch = int((chk.n_distinct.astype(int) > chk.s2_distinct.astype(int)).sum())

    d["bucket"] = [bucket.get(int(s)) for s in d.show_trakt_id]
    done = d[d.completes.fillna(False)].copy()
    done["lag_days"] = (done.completion_ts - done.t0_ts) / 86400.0
    # MARGINAL completion lag: first S2 episode -> completion. No T0 term, so
    # no datetime conversion and no exposure to the epoch-unit bug above.
    # NB percentiles do not subtract: this is NOT p90(from T0) - p90(to first).
    done["marginal_days"] = (done.completion_ts - done.first_ts) / 86400.0

    def block(sub, label):
        a = sub.lag_days.values
        return {
            "population": label,
            "pairs_in_estimation_sample": None,
            "pairs_that_complete_S2": int(len(a)),
            "p90_completion_lag_days": round(pct(a), 4),
            "p90_ceiling": int(math.ceil(pct(a))),
            "median": round(float(np.median(a)), 2),
            "p75": round(pct(a, 75), 2),
            "p95": round(pct(a, 95), 2),
            "marginal_first_S2_to_completion": {
                "p50": round(float(np.median(sub.marginal_days.values)), 2),
                "p75": round(pct(sub.marginal_days.values, 75), 2),
                "p90": round(pct(sub.marginal_days.values, 90), 4),
                "p90_ceiling": int(math.ceil(pct(sub.marginal_days.values, 90))),
                "p95": round(pct(sub.marginal_days.values, 95), 2),
                "share_within_108d": round(100 * float((sub.marginal_days.values < 108).mean()), 2),
            },
        }

    c1_est = int((d.bucket == "C1").sum())
    all_est = int(len(d))
    b_c1 = block(done[done.bucket == "C1"], "C1 subset")
    b_all = block(done, "all five D12 buckets")
    b_c1["pairs_in_estimation_sample"] = c1_est
    b_all["pairs_in_estimation_sample"] = all_est

    out = {
        "what": "90th percentile of the time-to-S2-COMPLETION lag, Red Team's "
                "minimum ask at the Step 6 gate",
        "api_calls": 0,
        "adopted_W": 108,
        "definition": "completion instant = max(canonical ts of F2, k-th smallest "
                      "canonical ts over distinct S2 episodes in E2), "
                      "k = ceil(0.90*L2); lag = that instant - T0, continuous days",
        "step5_waterfall_reproduced": waterfall,
        "distinct_count_exceeds_step5_s2_distinct": mismatch,
        "first_S2_episode_lag_p90": {"C1": 107.7135, "all_shows": 37.6967,
                                     "source": "decisions/0026, both Step 6 instances"},
        "completion_lag_p90": {"C1": b_c1, "all_shows": b_all},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
