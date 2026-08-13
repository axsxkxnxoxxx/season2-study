"""Step 7 ALTERNATIVE-RULE EVALUATION (instance b, namespace alt_b) -- stage 2.

Outcome assignment on the line-1 (201,900) population, at EVERY W arm.

Per artifacts/step1-outcome-definition.md Sec 7 as amended by decisions/0034:
  A    = distinct S2 episodes whose number is in E2, canonical timestamp
         (Sec 2.2, min watched_at across that episode's records) < tau1,
         tau1 = [T0] + W x 24h.  Half-open instant form throughout.
  A_H  = the same set at tau2 = [T0] + (W + H) x 24h.
  Never started    : |A| = 0
  Continued        : |A| >= 1 AND F2 in A_H AND |A_H| >= ceil(0.90 x L2)
  Started and left : |A| >= 1 AND NOT Continued

H is held CONSTANT at 91 across every arm (task-sheet Step 13).
D11 (decisions/0011): records at or after tau_pull are discarded everywhere.

Computed INDEPENDENTLY of liveness. That independence is the substance of
question 1 -- |A| is a function of T0, W, E2 and the episode records only.

ZERO network calls. Reads only.

Out: processed/step7/alt_b/outcomes.npz, processed/step7/alt_b/stage2.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7" / "alt_b"

MISSING = np.iinfo(np.int64).min
H, DAY = 91, 86400.0
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()


def main() -> None:
    t = time.time()
    prov: dict = {"instance": "data-scientist-b", "namespace": "alt_b", "stage": 2,
                  "api_calls": 0, "adopts": "nothing", "H": H, "W_arms": W_ARMS}

    pz = np.load(OUT / "pairs.npz")
    uidx, sh = pz["user_idx"], pz["show_trakt_id"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    k, f2 = pz["k"], pz["f2"]
    n = len(uidx)
    prov["n_line1"] = n

    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}

    z = np.load(P5 / "full_scan.npz")
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    del z
    prov["s2_records_with_a_timestamp"] = int(len(s2))
    inE2 = np.fromiter(
        (nn in e2.get(int(ss), ()) for ss, nn in
         zip(s2.show_trakt_id.values, s2.number.values)), bool, len(s2))
    prov["s2_records_dropped_not_in_E2"] = int((~inE2).sum())
    s2 = s2[inE2]
    print(f"in-E2 S2 records {len(s2):,}  ({time.time() - t:.1f}s)", flush=True)

    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2
    prov["distinct_episode_records_in_scope"] = int(len(ep))

    idx = {(int(u), int(s)): i for i, (u, s) in enumerate(zip(uidx, sh))}
    row = np.array([idx.get((int(u), int(s)), -1) for u, s in
                    zip(ep.user_idx.values, ep.show_trakt_id.values)])
    sel = row >= 0
    row, ets, enum = row[sel], ep.ts.values[sel].astype(np.float64), ep.number.values[sel]
    del ep
    prov["distinct_episode_records_matched_to_line1"] = int(len(row))

    d11 = ets < TAU_PULL
    prov["D11_discarded_at_or_after_tau_pull"] = int((~d11).sum())
    row, ets, enum = row[d11], ets[d11], enum[d11]
    is_f2 = enum == f2[row]

    pairs_with_any_in_E2_record = np.zeros(n, dtype=bool)
    pairs_with_any_in_E2_record[row] = True
    prov["line1_pairs_with_at_least_one_in_E2_S2_record"] = int(
        pairs_with_any_in_E2_record.sum())
    prov["line1_pairs_with_NO_in_E2_S2_record"] = int(n - pairs_with_any_in_E2_record.sum())

    def counts_at(bound: np.ndarray):
        s = ets < bound[row]
        cnt = np.bincount(row[s], minlength=n)
        f2hit = np.bincount(row[s & is_f2], minlength=n) > 0
        return cnt, f2hit

    out: dict = {"has_any_in_E2_s2_record": pairs_with_any_in_E2_record}
    per_arm = {}
    for W in W_ARMS:
        tau1 = t0 + W * DAY
        tau2 = t0 + (W + H) * DAY
        nA, _ = counts_at(tau1)
        nAH, f2hit_H = counts_at(tau2)
        started = nA > 0
        cont = started & f2hit_H & (nAH >= k)
        sal = started & ~cont
        assert int((~started).sum() + cont.sum() + sal.sum()) == n
        assert (nAH >= nA).all()
        out[f"started_W{W}"] = started
        out[f"cont_W{W}"] = cont
        out[f"sal_W{W}"] = sal
        per_arm[str(W)] = {
            "W": W, "tau2_days": W + H,
            "line1_unfiltered": {
                "n": n, "never_started": int((~started).sum()),
                "continued": int(cont.sum()), "started_and_left": int(sal.sum())},
        }
        print(f"W={W:>4}  NS {int((~started).sum()):>7,}  C {int(cont.sum()):>7,} "
              f" SL {int(sal.sum()):>7,}  ({time.time() - t:.1f}s)", flush=True)
    prov["partition_asserted_every_arm"] = True
    prov["monotonicity_A_subset_AH_asserted_every_arm"] = True
    prov["per_arm"] = per_arm

    np.savez(OUT / "outcomes.npz", **out)
    prov["elapsed_s"] = time.time() - t
    (OUT / "stage2.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov["per_arm"]["108"], indent=2))


if __name__ == "__main__":
    main()
