"""Step 7 ALTERNATIVE-RULE EVALUATION (instance b, namespace alt_b) -- stage 4.

Three diagnostics the headline comparison does not carry:

  (a) MECHANISM. Split each rule's exclusion set by whether the pair has any S2
      record anywhere in the sweep. Line 4 requires has_s2 by construction, so
      this is the axis on which DERIV and APPLY differ.

  (b) SPEC-AMBIGUITY COST. The alternative says "|A| = 0". Two faithful
      instances could read the absence conjunct three ways:
        ALT_A     |A| = 0 at tau1          -- matches step1 Sec 7 Never started
        ALT_AH    |A_H| = 0 at tau2        -- the Continued clock
        ALT_BROAD NOT Continued            -- "outcome inferred from absence"
      All three are measured. This is the dual-implementation exposure the
      wording would create if adopted without settling it.

  (c) W-COUPLING. Exclusion count per rule per Step 13 arm, both populations,
      the figure decisions/0044 Sec 1.2 requires of any liveness rule.

ZERO network calls. Reads only.

Out: processed/step7/alt_b/variants.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt_b"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    uidx_all = pz["user_idx"]
    in_line4_all = pz["in_line4"]
    has_s2_all = pz["has_s2_evidence"]
    has_inE2_all = oz["has_any_in_E2_s2_record"]

    res: dict = {"instance": "data-scientist-b", "namespace": "alt_b", "stage": 4,
                 "api_calls": 0, "adopts": "nothing"}

    # ---------- (b) needs |A_H| = 0, which is not in outcomes.npz; derive it:
    # |A_H| = 0  <=>  NOT started at tau2. Recomputing the tau2 counts is
    # unnecessary: |A_H| = 0 implies |A| = 0 (A subset A_H), and a pair with
    # |A| = 0 has |A_H| = 0 iff it has no in-E2 S2 record before tau2. Rather
    # than infer it, recompute directly from the arm arrays already stored:
    # started_W* is |A| >= 1 at tau1 for that arm; for tau2 we use the NEXT
    # information available -- cont/sal are both subsets of started, so
    # |A_H| = 0 is not recoverable from these arrays. Recompute it here.
    import pandas as pd
    MISSING = np.iinfo(np.int64).min
    P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
    f = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    z = np.load(P5 / "full_scan.npz")
    m = (z["season"] == 2) & (z["ts"] != MISSING)
    s2 = pd.DataFrame({"user_idx": z["user"][m], "show_trakt_id": z["show"][m],
                       "number": z["number"][m], "ts": z["ts"][m]})
    del z
    inE2 = np.fromiter((nn in e2.get(int(ss), ()) for ss, nn in
                        zip(s2.show_trakt_id.values, s2.number.values)), bool, len(s2))
    s2 = s2[inE2]
    ep = s2.groupby(["user_idx", "show_trakt_id", "number"], as_index=False)["ts"].min()
    del s2
    idx = {(int(u), int(s)): i for i, (u, s) in
           enumerate(zip(uidx_all, pz["show_trakt_id"]))}
    row = np.array([idx.get((int(u), int(s)), -1) for u, s in
                    zip(ep.user_idx.values, ep.show_trakt_id.values)])
    sel = row >= 0
    row, ets = row[sel], ep.ts.values[sel].astype(np.float64)
    del ep
    TAU_PULL = pd.Timestamp("2026-08-11", tz="UTC").timestamp()
    d11 = ets < TAU_PULL
    row, ets = row[d11], ets[d11]
    t0 = pz["t0_midnight_epoch"].astype(np.float64)
    n_all = len(t0)
    print(f"tau2 recompute ready ({time.time() - t:.1f}s)", flush=True)

    out_pop: dict = {}
    for popname in ("DERIV", "APPLY"):
        per_arm = {}
        for W in W_ARMS:
            d10 = pz[f"d10_W{W}"]
            base = d10 & in_line4_all if popname == "DERIV" else d10
            tau2 = t0 + (W + 91) * 86400.0
            startedH_all = np.zeros(n_all, dtype=bool)
            startedH_all[row[ets < tau2[row]]] = True

            uidx = uidx_all[base]
            started = oz[f"started_W{W}"][base]
            cont = oz[f"cont_W{W}"][base]
            sal = oz[f"sal_W{W}"][base]
            ns = ~started
            noaft = pz[f"no_after_W{W}"][base]
            hs2 = has_s2_all[base]
            hE2 = has_inE2_all[base]
            startedH = startedH_all[base]
            n = int(base.sum())
            assert (startedH >= started).all()

            masks = {
                "PF_LIMIT": noaft,
                "ALT_A": noaft & ns,
                "ALT_AH": noaft & ~startedH,
                "ALT_BROAD": noaft & ~cont,
            }
            assert (masks["ALT_AH"] <= masks["ALT_A"]).all()
            assert (masks["ALT_A"] <= masks["ALT_BROAD"]).all()
            assert (masks["ALT_BROAD"] <= masks["PF_LIMIT"]).all()

            arm = {"W": W, "n": n,
                   "never_started_unfiltered_pct": 100.0 * ns.sum() / n,
                   "rules": {}}
            for r, mk in masks.items():
                ex = int(mk.sum())
                live = ~mk
                d = int(live.sum())
                nsl = int((ns & live).sum())
                arm["rules"][r] = {
                    "excluded": ex,
                    "accounts": int(len(np.unique(uidx[mk]))) if ex else 0,
                    "excluded_has_S2_record_anywhere": int((mk & hs2).sum()),
                    "excluded_has_NO_S2_record_anywhere": int((mk & ~hs2).sum()),
                    "excluded_has_in_E2_S2_record": int((mk & hE2).sum()),
                    "never_started_pct": 100.0 * nsl / d,
                    "delta_vs_no_filter_pp": 100.0 * nsl / d - 100.0 * ns.sum() / n,
                    "bound_ceiling_pct": 100.0 * (nsl + ex) / (d + ex),
                }
            per_arm[str(W)] = arm
        out_pop[popname] = per_arm
    res["by_population"] = out_pop

    res["elapsed_s"] = time.time() - t
    (OUT / "variants.json").write_text(json.dumps(res, indent=2))

    for popname in ("DERIV", "APPLY"):
        print(f"\n=== {popname}: excluded pairs per W arm")
        print(f"{'rule':<11}" + "".join(f"{w:>8}" for w in W_ARMS))
        for r in ("PF_LIMIT", "ALT_BROAD", "ALT_A", "ALT_AH"):
            print(f"{r:<11}" + "".join(
                f"{out_pop[popname][str(w)]['rules'][r]['excluded']:>8,}" for w in W_ARMS))
        print(f"{'NS% unfilt':<11}" + "".join(
            f"{out_pop[popname][str(w)]['never_started_unfiltered_pct']:>8.3f}"
            for w in W_ARMS))
    a = out_pop["APPLY"]["108"]["rules"]
    print("\nAPPLY W=108 exclusion mechanism (has any S2 record anywhere / none):")
    for r in ("PF_LIMIT", "ALT_BROAD", "ALT_A", "ALT_AH"):
        print(f"  {r:<11}{a[r]['excluded']:>7,} = "
              f"{a[r]['excluded_has_S2_record_anywhere']:>6,} with / "
              f"{a[r]['excluded_has_NO_S2_record_anywhere']:>6,} without")
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
