"""Step 7 rerun on ALT-MATCHED (instance b, namespace mm_b) -- stage 4C.

THE FROZEN-D10 READING, at W = 125 / 150 / 180 / 213.

task-sheet.md Step 7 and decisions/0050 record, under ALT-BROAD, that freezing
D10 at W = 108 gives TOTALS 746 / 823 / 918 / 1,117 on APPLY, of which the
never-started COMPONENT is 632 / 684 / 753 / 881. Those are ALT-BROAD figures.
Under ALT-MATCHED they go stale, and a Step 13 instance producing the frozen
reading would file a false divergence against them. They are recomputed here
under the adopted rule, BOTH READINGS NAMED, so the record can be corrected.

D10 RE-DERIVED is the operative reading (0047 Sec 5). The frozen reading is
reported only because the record carries it.

W = 125 and 180 are NOT in the mandated arm grid, so outcomes and both silence
tests are computed here for those two arms only.

ZERO network calls. Out: processed/step7/mm_b/frozen_d10.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
OUT = ROOT / "processed" / "step7" / "mm_b"
MISSING = np.iinfo(np.int64).min
H, DAY = 91, 86400.0
ARMS = [125, 150, 180, 213]
TAU_PULL_TS = pd.Timestamp("2026-08-11", tz="UTC").timestamp()
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64)


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    uidx, sh = pz["user_idx"], pz["show_trakt_id"]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    t0i = pz["t0_midnight_epoch"]
    k, f2, in4 = pz["k"], pz["f2"], pz["in_line4"]
    mx = pz["max_inst_pair"]
    n = len(uidx)

    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    z = np.load(P5 / "full_scan.npz")
    s2m = z["season"] == 2
    s2 = pd.DataFrame({"user_idx": z["user"][s2m], "show_trakt_id": z["show"][s2m],
                       "number": z["number"][s2m], "ts": z["ts"][s2m]})
    del z
    s2 = s2[s2.ts.values != MISSING]
    inE2 = np.fromiter((nn in e2.get(int(ss), ()) for ss, nn in
                        zip(s2.show_trakt_id.values, s2.number.values)), bool, len(s2))
    s2 = s2[inE2]
    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2
    idx = {(int(u), int(s)): i for i, (u, s) in enumerate(zip(uidx, sh))}
    row = np.array([idx.get((int(u), int(s)), -1) for u, s in
                    zip(ep.user_idx.values, ep.show_trakt_id.values)])
    sel = row >= 0
    row, ets, enum = row[sel], ep.ts.values[sel].astype(np.float64), ep.number.values[sel]
    del ep
    d11 = ets < TAU_PULL_TS
    row, ets, enum = row[d11], ets[d11], enum[d11]
    is_f2 = enum == f2[row]

    def counts_at(bound):
        s = ets < bound[row]
        return np.bincount(row[s], minlength=n), np.bincount(row[s & is_f2], minlength=n) > 0

    d10_frozen = t0i + (max(108, 91) + H) * 86400 <= TAU_PULL
    assert int(d10_frozen.sum()) == 196_654

    res: dict = {
        "instance": "data-scientist-b", "namespace": "mm_b", "stage": "4C",
        "api_calls": 0, "adopts": "nothing", "rule_name": "ALT-MATCHED",
        "operative_reading": "D10 RE-DERIVED at each arm (0047 Sec 5)",
        "frozen_reading": "D10 held at its W = 108 value, n = 196,654 on APPLY at every arm",
        "why_reported": ("task-sheet.md Step 7 and 0050 carry ALT-BROAD's frozen series "
                         "746 / 823 / 918 / 1,117 with never-started component "
                         "632 / 684 / 753 / 881. Under ALT-MATCHED those go stale."),
        "arms": ARMS, "by_reading": {},
    }
    for reading in ("frozen", "re_derived"):
        per_pop = {}
        for pop in ("DERIV", "APPLY"):
            arm_out = {}
            for W in ARMS:
                d10 = d10_frozen if reading == "frozen" else (
                    t0i + (max(W, 91) + H) * 86400 <= TAU_PULL)
                base = (d10 & in4) if pop == "DERIV" else d10
                tau1, tau2 = t0 + W * DAY, t0 + (W + H) * DAY
                nA, _ = counts_at(tau1)
                nAH, f2hitH = counts_at(tau2)
                started = nA > 0
                cont = started & f2hitH & (nAH >= k)
                sal = started & ~cont
                ns = ~started
                sil1, sil2 = mx <= tau1, mx <= tau2
                notlive = (ns & sil1) | (sal & sil2)
                b = base
                arm_out[str(W)] = {
                    "W": W, "n": int(b.sum()),
                    "excluded_total": int((notlive & b).sum()),
                    "excluded_never_started": int((ns & sil1 & b).sum()),
                    "excluded_started_and_left": int((sal & sil2 & b).sum()),
                }
            per_pop[pop] = arm_out
        res["by_reading"][reading] = per_pop

    res["comparison_APPLY"] = {
        "frozen_totals": [res["by_reading"]["frozen"]["APPLY"][str(W)]["excluded_total"]
                          for W in ARMS],
        "frozen_never_started_component": [
            res["by_reading"]["frozen"]["APPLY"][str(W)]["excluded_never_started"] for W in ARMS],
        "frozen_started_and_left_component": [
            res["by_reading"]["frozen"]["APPLY"][str(W)]["excluded_started_and_left"]
            for W in ARMS],
        "re_derived_totals": [res["by_reading"]["re_derived"]["APPLY"][str(W)]["excluded_total"]
                              for W in ARMS],
        "ALT_BROAD_frozen_totals_now_STALE": [746, 823, 918, 1117],
        "ALT_BROAD_frozen_NS_component_now_STALE": [632, 684, 753, 881],
    }
    res["elapsed_s"] = time.time() - t
    (OUT / "frozen_d10.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(res["comparison_APPLY"], indent=2))
    print(json.dumps(res["by_reading"]["frozen"]["DERIV"], indent=2))
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
