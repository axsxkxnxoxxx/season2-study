"""Step 7 gate-closing sensitivity test (instance b, namespace sens_b) -- stage 2.

Outcome assignment per artifacts/step1-outcome-definition.md Sec 7 AS AMENDED
(decisions/0034). Computed ONCE, independently of liveness -- liveness is a row
filter applied on top in stage 3, so the outcome arrays are shared by all four
settings and cannot drift between them.

  A    = distinct S2 episodes whose number is in E2, canonical timestamp
         (Sec 2.2: min watched_at across that episode's records) satisfying
         watched_at < tau1,  tau1 = [T0] + 108 x 24h.   Half-open instant form.
  A_H  = the same set at tau2 = [T0] + (108 + 91) x 24h = [T0] + 199 days.
  Never started    : |A| = 0
  Continued        : |A| >= 1 AND F2 in A_H AND |A_H| >= ceil(0.90 x L2)
  Started and left : |A| >= 1 AND NOT Continued

D11 (decisions/0011): records at or after tau_pull are discarded everywhere.

ZERO network calls. Reads only.

Out: processed/step7/sens_b/outcomes.npz, processed/step7/sens_b/stage2.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7" / "sens_b"

MISSING = np.iinfo(np.int64).min
W, H, DAY = 108, 91, 86400.0
TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()


def main() -> None:
    t = time.time()
    prov: dict = {"instance": "data-scientist-b", "namespace": "sens_b", "stage": 2,
                  "api_calls": 0, "W": W, "H": H}

    pz = np.load(OUT / "pairs.npz")
    uidx, sh = pz["user_idx"], pz["show_trakt_id"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    k, f2 = pz["k"], pz["f2"]
    n = len(uidx)

    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}

    z = np.load(P5 / "full_scan.npz")
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    del z
    prov["s2_records_with_a_timestamp"] = int(len(s2))
    # Sec 3.2 set-membership drop: an episode whose number is not in E2 is dropped.
    inE2 = np.fromiter(
        (nn in e2.get(int(ss), ()) for ss, nn in
         zip(s2.show_trakt_id.values, s2.number.values)), bool, len(s2))
    prov["s2_records_dropped_not_in_E2"] = int((~inE2).sum())
    s2 = s2[inE2]
    print(f"in-E2 S2 records {len(s2):,}  ({time.time() - t:.1f}s)", flush=True)

    # Sec 2.2: canonical timestamp of a distinct episode = MIN watched_at.
    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2
    prov["distinct_episode_records_in_scope"] = int(len(ep))

    idx = {(int(u), int(s)): i for i, (u, s) in enumerate(zip(uidx, sh))}
    row = np.array([idx.get((int(u), int(s)), -1) for u, s in
                    zip(ep.user_idx.values, ep.show_trakt_id.values)])
    sel = row >= 0
    row, ets, enum = row[sel], ep.ts.values[sel].astype(np.float64), ep.number.values[sel]
    del ep
    prov["distinct_episode_records_matched_to_the_population"] = int(len(row))

    # D11
    d11 = ets < TAU_PULL
    prov["D11"] = {
        "tau_pull": "2026-08-11T00:00:00Z",
        "discarded_at_or_after_tau_pull": int((~d11).sum()),
        "pairs_touched": int(len(set(row[~d11].tolist()))),
    }
    row, ets, enum = row[d11], ets[d11], enum[d11]
    is_f2 = enum == f2[row]

    def counts_at(bound: np.ndarray):
        s = ets < bound[row]
        cnt = np.bincount(row[s], minlength=n)
        f2hit = np.bincount(row[s & is_f2], minlength=n) > 0
        return cnt, f2hit

    tau1 = t0 + W * DAY
    tau2 = t0 + (W + H) * DAY
    nA, _ = counts_at(tau1)
    nAH, f2hit_H = counts_at(tau2)

    started = nA > 0                                    # |A| >= 1 at tau1
    cont = started & f2hit_H & (nAH >= k)               # Sec 7 as amended
    sal = started & ~cont

    # Sec 7 partition invariant, on the full line-4 set before any liveness filter.
    assert int((~started).sum() + cont.sum() + sal.sum()) == n
    assert not (cont & ~started).any()
    prov["partition_asserted_on_line4"] = True
    prov["line4_unfiltered_counts"] = {
        "n": n, "never_started": int((~started).sum()),
        "continued": int(cont.sum()), "started_and_left": int(sal.sum())}
    # A subset of A_H by construction (tau1 < tau2)
    assert (nAH >= nA).all()
    prov["monotonicity_A_subset_AH_asserted"] = True

    np.savez(OUT / "outcomes.npz", nA=nA, nAH=nAH, f2hit_H=f2hit_H,
             started=started, cont=cont, sal=sal)
    prov["elapsed_s"] = time.time() - t
    (OUT / "stage2.json").write_text(json.dumps(prov, indent=2))
    print(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main()
