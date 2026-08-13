"""Step 7 ALT-BROAD rerun (instance b, namespace bb_b) -- stage 3b.

IS THE EXCLUSION SET STABLE UNDER PLAUSIBLE CALIBRATION RESIDUAL?

Conjunct (a) is `max(instant) <= tau1`, an inequality between an interpolated
quantity and an exact one. Stage 3a bounded the residual. This stage puts the
margins beside it.

  M1  For every EXCLUDED pair: tau1 - max(instant), in days. How far below tau1
      the account's last insertion sits. Small margin = fragile exclusion.
  M2  For every NEAR-MISS LIVE pair -- live ONLY because of conjunct (a), i.e.
      NOT Continued and max(instant) > tau1: max(instant) - tau1, in days.
      Small margin = fragile retention.
  M3  Sensitivity: shift every account's max instant by +/- delta and recount.
      +delta means the true insertion was LATER than the curve says, which is
      the direction step5_calibrate.py states the curve errs in ("the estimate
      is therefore mildly EARLY"), and it makes accounts MORE live.
  M4  Clamping: do any excluded pairs sit on accounts whose maximum instant was
      set by a record clamped above the last knot?
  M5  A calibration-INDEPENDENT cross-check: do the excluded pairs' accounts
      hold any record whose CLAIMED watched_at is after tau1? This is a
      diagnostic on the residual, NOT a liveness rule -- 0021 rules liveness on
      insertion time and this stage does not touch that.

ZERO network calls. Reads only.

Out: processed/step7/bb_b/margins.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
SRC = ROOT / "processed" / "step7" / "alt2_b"
OUT = ROOT / "processed" / "step7" / "bb_b"
MISSING = np.iinfo(np.int64).min
DAY = 86400.0
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
W = 108
QS = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100)
# the residual ladder, in days, taken from stage 3a's measured distribution
LADDER = [0.02, 0.107, 1.0, 7.0, 30.0, 124.6, 287.5]


def main() -> None:
    t = time.time()
    pz = np.load(SRC / "pairs.npz")
    oz = np.load(SRC / "outcomes.npz")
    az = np.load(OUT / "acct_instants.npz")
    resid = json.load(open(OUT / "residual.json"))

    max_inst = az["max_inst"]
    max_at_clamped = az["max_at_clamped"]
    uidx_all = pz["user_idx"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    in4 = pz["in_line4"]

    # per-account maximum CLAIMED watched_at, for M5
    z = np.load(P5 / "full_scan.npz")
    user, ts = z["user"], z["ts"]
    dated = ts != MISSING
    n_users = len(max_inst)
    max_claim = np.full(n_users, -np.inf)
    np.maximum.at(max_claim, user[dated], ts[dated].astype(np.float64))
    del z, user, ts, dated
    print(f"per-account max claimed watched_at  ({time.time() - t:.1f}s)", flush=True)

    res: dict = {
        "instance": "data-scientist-b", "namespace": "bb_b", "stage": "3b",
        "api_calls": 0, "adopts": "nothing",
        "residual_ladder_days": LADDER,
        "residual_ladder_provenance": {
            "0.02": "median |residual| on the fit family (28 minutes)",
            "0.107": "p90 |residual| on the fit family (2.6 hours)",
            "1.0": "one day -- 91.5% of fit records are inside this",
            "7.0": "one week -- the stored held-out validation reports 90.6% inside",
            "30.0": "one month",
            "124.6": "p95 |residual| on the fit family",
            "287.5": "p97.5 |residual| on the fit family",
        },
        "residual_shape": ("BIMODAL. 90% of fit-family records sit inside 2.6 HOURS; the top ~8% "
                           "sit in the HUNDREDS OF DAYS. There is no single residual scale, so "
                           "the stability question has to be answered at both."),
        "by_population": {},
    }

    for pop in ("DERIV", "APPLY"):
        d10 = pz[f"d10_W{W}"]
        base = (d10 & in4) if pop == "DERIV" else d10
        u = uidx_all[base]
        tau1 = t0[base] + W * DAY
        mi = max_inst[u]
        cont = oz[f"cont_W{W}"][base].astype(bool)
        sal = oz[f"sal_W{W}"][base].astype(bool)
        ns = ~oz[f"started_W{W}"][base]
        noaft = mi <= tau1
        assert np.array_equal(noaft, pz[f"no_after_W{W}"][base]), \
            "recomputed conjunct (a) disagrees with the stored one"
        notlive = noaft & ~cont
        nearmiss = (~noaft) & (~cont)          # live ONLY by conjunct (a)

        m_ex = (tau1[notlive] - mi[notlive]) / DAY
        m_nm = (mi[nearmiss] - tau1[nearmiss]) / DAY

        def pctl(v):
            return {f"p{q}": float(np.percentile(v, q)) for q in QS} if len(v) else None

        entry = {
            "population": pop, "W": W, "n": int(base.sum()),
            "M1_excluded_margin_days": {
                "definition": "tau1 - max(instant) for excluded pairs; how far below tau1 the "
                              "account's last insertion sits",
                "n": int(notlive.sum()),
                "n_never_started": int((notlive & ns).sum()),
                "n_started_and_left": int((notlive & sal).sum()),
                "percentiles": pctl(m_ex),
                "mean": float(m_ex.mean()) if len(m_ex) else None,
                "count_within_delta": {str(d): int((m_ex <= d).sum()) for d in LADDER},
                "percentiles_never_started": pctl((tau1[notlive & ns] - mi[notlive & ns]) / DAY),
                "percentiles_started_and_left": pctl((tau1[notlive & sal] - mi[notlive & sal]) / DAY),
            },
            "M2_near_miss_live_margin_days": {
                "definition": "max(instant) - tau1 for pairs live ONLY by conjunct (a) "
                              "(not Continued, and an insertion after tau1)",
                "n": int(nearmiss.sum()),
                "percentiles": pctl(m_nm),
                "count_within_delta": {str(d): int((m_nm <= d).sum()) for d in LADDER},
            },
            "M4_clamping": {
                "excluded_pairs_on_accounts_whose_max_instant_is_clamped":
                    int(max_at_clamped[u[notlive]].sum()),
                "near_miss_live_pairs_on_such_accounts":
                    int(max_at_clamped[u[nearmiss]].sum()),
                "clamp_value_utc": resid["R3_clamping"]["clamp_value_above_utc"],
                "reading": ("the clamp value is the last knot time, 2026-08-10T20:48Z, which is "
                            "later than tau1 for EVERY pair surviving D10 -- D10 requires "
                            "[T0] + (max(W,91) + H) x 24h <= tau_pull, so tau1 <= tau_pull - H "
                            "days. An account whose maximum is clamped is therefore live for "
                            "every pair it holds, and the 5,094 clamped records cannot produce a "
                            "false exclusion at any tested arm. 0048 Sec 9's clamping concern is "
                            "real in direction and null in effect on this exclusion set."),
            },
            "M5_claimed_watched_at_cross_check": {
                "definition": "a DIAGNOSTIC only. Does an excluded pair's account hold any record "
                              "whose CLAIMED watched_at is after tau1? Liveness runs on insertion "
                              "time (0021) and this does not change that.",
                "excluded_pairs_whose_account_claims_a_watch_after_tau1":
                    int((max_claim[u[notlive]] > tau1[notlive]).sum()),
                "of_which_never_started": int(((max_claim[u] > tau1) & notlive & ns).sum()),
                "of_which_started_and_left": int(((max_claim[u] > tau1) & notlive & sal).sum()),
                "excess_days_percentiles": pctl(
                    (max_claim[u[notlive]] - tau1[notlive]) / DAY),
                "reading": ("a claim after tau1 on an account with no insertion after tau1 is "
                            "either a backdated-forward claim, which is what 0021 says to ignore, "
                            "or calibration error. It cannot distinguish the two, so it is an "
                            "UPPER bound on the count of exclusions the residual could overturn, "
                            "not an estimate of it."),
            },
        }
        res["by_population"][pop] = entry

    # ------------------------------------------------- M3 sensitivity, per arm
    sens: dict = {}
    for pop in ("DERIV", "APPLY"):
        arms = {}
        for Wa in W_ARMS:
            d10 = pz[f"d10_W{Wa}"]
            base = (d10 & in4) if pop == "DERIV" else d10
            u = uidx_all[base]
            tau1 = t0[base] + Wa * DAY
            mi = max_inst[u]
            cont = oz[f"cont_W{Wa}"][base].astype(bool)
            sal = oz[f"sal_W{Wa}"][base].astype(bool)
            ns = ~oz[f"started_W{Wa}"][base]
            row = {}
            for d in [0.0] + LADDER:
                for sgn, tag in ((+1, "later"), (-1, "earlier")):
                    if d == 0.0 and sgn < 0:
                        continue
                    nl = ((mi + sgn * d * DAY) <= tau1) & ~cont
                    row[f"{tag}_{d}"] = {
                        "excluded": int(nl.sum()),
                        "never_started": int((nl & ns).sum()),
                        "started_and_left": int((nl & sal).sum()),
                    }
            base_ex = row["later_0.0"]["excluded"]
            row["_base"] = base_ex
            row["_range_over_ladder"] = [
                min(v["excluded"] for k, v in row.items() if k.startswith(("later", "earlier"))),
                max(v["excluded"] for k, v in row.items() if k.startswith(("later", "earlier")))]
            row["_range_over_sub_day_residual"] = [
                min(row[f"{tag}_{d}"]["excluded"] for tag in ("later", "earlier")
                    for d in (0.02, 0.107)),
                max(row[f"{tag}_{d}"]["excluded"] for tag in ("later", "earlier")
                    for d in (0.02, 0.107))]
            arms[str(Wa)] = row
        sens[pop] = arms
    res["M3_sensitivity"] = sens

    # headline stability statement
    a = sens["APPLY"]["108"]
    d = sens["DERIV"]["108"]
    res["stability_verdict"] = {
        "APPLY_W108_base": a["_base"],
        "APPLY_W108_range_sub_day_residual": a["_range_over_sub_day_residual"],
        "APPLY_W108_range_full_ladder": a["_range_over_ladder"],
        "DERIV_W108_base": d["_base"],
        "DERIV_W108_range_sub_day_residual": d["_range_over_sub_day_residual"],
        "DERIV_W108_range_full_ladder": d["_range_over_ladder"],
    }

    res["elapsed_s"] = time.time() - t
    (OUT / "margins.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["stability_verdict"], indent=2))
    print(json.dumps(res["by_population"]["APPLY"]["M1_excluded_margin_days"], indent=2)[:2000])
    print(json.dumps(res["by_population"]["APPLY"]["M2_near_miss_live_margin_days"], indent=2)[:1200])
    print(json.dumps(res["by_population"]["APPLY"]["M5_claimed_watched_at_cross_check"], indent=2)[:1200])
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
