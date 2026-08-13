"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 4b.

Is the DERIV zero FORCED, or merely OBSERVED at the arms tested?

A pair is excluded iff  max_insertion_instant <= tau1  AND  |A| = 0 at tau1.
Let  first_A = the minimum canonical timestamp (Step 1 Sec 2.2) over that
pair's in-E2 S2 episodes, +inf when it has none. Then

    |A| = 0 at tau1  <=>  first_A >= tau1
    silent after tau1 <=> max_inst <= tau1

so the pair is excluded at exactly those W with

    tau1 = [T0] + W x 24h  in  [max_inst, first_A]

and the feasible W set is non-empty iff max_inst <= first_A. For a pair WITH S2
evidence that requires a record claiming a watch later than its own insertion
instant -- which the sweep does contain (stage 4: 22.68% of dated records are
future-dated in that sense).

This stage computes, for every line-1 pair, the interval of W at which the
adopted rule would exclude it, and reports how many DERIV pairs have a
non-empty one and where those intervals sit relative to the tested arms.

ZERO network calls. Reads only.

Out: processed/step7/alt2_b/forcedness.json
     processed/step7/alt2_b/feasible_W.npz  (row-level, stays in processed/)
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7" / "alt2_b"
MISSING = np.iinfo(np.int64).min
DAY = 86400.0
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()


def insert_time(rid, knot_rid, knot_time):
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    uidx, sh = pz["user_idx"], pz["show_trakt_id"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    in_line4 = pz["in_line4"]
    n = len(uidx)

    # ---- per-account max insertion instant, from the stored calibration (READ, NOT REFITTED)
    cal = np.load(P5 / "calibration.npz")
    z = np.load(P5 / "full_scan.npz")
    tau_rec = insert_time(z["rid"], cal["knot_rid"], cal["knot_time"])
    user = z["user"]
    n_users = int(user.max()) + 1
    max_inst_acct = np.full(n_users, -np.inf)
    np.maximum.at(max_inst_acct, user, tau_rec)
    max_inst = max_inst_acct[uidx]

    # ---- first_A per pair: min canonical timestamp over in-E2 S2 episodes
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    del z, tau_rec, user
    inE2 = np.fromiter((nn in e2.get(int(ss), ()) for ss, nn in
                        zip(s2.show_trakt_id.values, s2.number.values)), bool, len(s2))
    s2 = s2[inE2]
    s2 = s2[s2.ts.values.astype(np.float64) < TAU_PULL]      # D11
    idx = {(int(u), int(s)): i for i, (u, s) in enumerate(zip(uidx, sh))}
    row = np.array([idx.get((int(u), int(s)), -1) for u, s in
                    zip(s2.user_idx.values, s2.show_trakt_id.values)])
    sel = row >= 0
    row, ets = row[sel], s2.ts.values[sel].astype(np.float64)
    del s2
    first_A = np.full(n, np.inf)
    np.minimum.at(first_A, row, ets)
    print(f"first_A built  ({time.time() - t:.1f}s)", flush=True)

    # ---- feasible W interval per pair
    lo_days = (max_inst - t0) / DAY          # smallest W with tau1 >= max_inst
    hi_days = (first_A - t0) / DAY           # largest  W with tau1 <= first_A
    feasible = max_inst <= first_A
    lo_clipped = np.maximum(lo_days, 0.0)
    nonempty = feasible & (hi_days >= lo_clipped)

    has_s2 = np.isfinite(first_A)
    res: dict = {
        "instance": "data-scientist-b", "namespace": "alt2_b", "stage": "4b",
        "api_calls": 0, "adopts": "nothing",
        "question": "is the DERIV exclusion zero forced by construction, or observed?",
        "line1": {
            "n": n,
            "pairs_with_a_non_empty_feasible_W_interval": int(nonempty.sum()),
            "of_those_with_S2_evidence": int((nonempty & has_s2).sum()),
            "of_those_with_no_S2_evidence_hence_feasible_for_all_large_W":
                int((nonempty & ~has_s2).sum()),
        },
        "DERIV_line4": {
            "n": int(in_line4.sum()),
            "pairs_with_a_non_empty_feasible_W_interval": int((nonempty & in_line4).sum()),
            "all_of_which_hold_S2_evidence": bool(has_s2[nonempty & in_line4].all())
                if int((nonempty & in_line4).sum()) else None,
        },
    }

    d4 = nonempty & in_line4
    if int(d4.sum()):
        res["DERIV_line4"]["feasible_W_intervals_days"] = {
            "lo_min": float(lo_clipped[d4].min()), "lo_median": float(np.median(lo_clipped[d4])),
            "lo_max": float(lo_clipped[d4].max()),
            "hi_min": float(hi_days[d4].min()), "hi_median": float(np.median(hi_days[d4])),
            "hi_max": float(hi_days[d4].max()),
        }
        # would any be excluded at an arm, once D10 is applied?
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            hit = d4 & (lo_clipped <= W) & (W <= hi_days) & d10
            hit_nod10 = d4 & (lo_clipped <= W) & (W <= hi_days)
            per_arm[str(W)] = {"excluded_at_this_arm_after_D10": int(hit.sum()),
                               "in_the_W_interval_before_D10": int(hit_nod10.sum())}
        res["DERIV_line4"]["per_arm"] = per_arm
        res["DERIV_line4"]["reading"] = (
            "the configuration is NOT foreclosed on DERIV: these pairs would be excluded "
            "at some W. The zero at the tested arms is therefore an OBSERVED zero over the "
            "arm grid, not an identity.")
    else:
        res["DERIV_line4"]["reading"] = (
            "no line-4 pair has a non-empty feasible W interval at any W, so the DERIV zero "
            "holds for every W, not only the tested arms -- forced given this calibration.")

    # same question on APPLY, for completeness, and the W at which each exclusion turns on
    per_arm_apply = {}
    for W in W_ARMS:
        d10 = pz[f"d10_W{W}"]
        hit = nonempty & (lo_clipped <= W) & (W <= hi_days) & d10
        per_arm_apply[str(W)] = int(hit.sum())
    res["APPLY_reconstructed_exclusions_per_arm_from_intervals"] = per_arm_apply

    np.savez(OUT / "feasible_W.npz", lo_days=lo_clipped, hi_days=hi_days,
             nonempty=nonempty, has_s2=has_s2, in_line4=in_line4)
    res["elapsed_s"] = time.time() - t
    (OUT / "forcedness.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
