"""Step 7 gate-closing sensitivity test (instance b, namespace sens_b) -- stage 3.

Is the outcome split sensitive to the liveness threshold across its clustered
interval? Four settings, everything else held fixed.

  T787   787 d   -- clustered interval lower endpoint
  T1293  1293 d  -- the point value (raw 1292.0284, ceiling per 0025)
  T2200  2200 d  -- clustered interval upper endpoint
  PF     the parameter-free rule, NO threshold at all

The liveness classes come from processed/step7/b4/bracket.npz at W = 108:
  state 0  measured bracketing gap        -> NOT LIVE iff gap >= threshold
  state 1  no instant after tau1          -> open-ended, NOT LIVE (0036 (i))
  state 2  no instant at or before tau1   -> LIVE (0021, approved gate 2 of 5,
                                             reinstated by 0040 Sec 1)

TWO READINGS OF THE PARAMETER-FREE RULE, and the spec does not settle which:
  PF_literal : live iff an instant at or before tau1 AND one after it -> state 0 only.
               This is the wording in decisions/0041 Sec 4, and it scores the
               state-2 pairs NOT LIVE, which contradicts 0040 Sec 1.
  PF_0021    : live iff NOT open-ended -> states 0 and 2. Consistent with 0040 Sec 1.
Both are computed and both are reported. Neither is adopted.

Intervals are account-clustered (2,402 accounts), because gaps within an account
are not independent -- the same reason 0039 required a clustered interval on the
threshold itself. Deltas use the SAME resample in each replicate, so they are
paired.

NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.
Every share below is provisional in its population as well as in its status.

ZERO network calls. Reads only.

Out: processed/step7/sens_b/sensitivity.json, .../excluded_composition.csv
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "sens_b"

THRESHOLDS = [("T787", 787.0), ("T1293", 1293.0), ("T2200", 2200.0)]
B = 2000
SEED = 20260813


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")

    d10 = pz["d10"]
    uidx = pz["user_idx"][d10]
    state = pz["state"][d10]
    gap = pz["gap_days"][d10]
    started, cont, sal = oz["started"][d10], oz["cont"][d10], oz["sal"][d10]
    ns = ~started
    n = int(d10.sum())
    assert n == 147_370
    assert int(ns.sum() + cont.sum() + sal.sum()) == n

    prov: dict = {
        "instance": "data-scientist-b", "namespace": "sens_b", "stage": 3,
        "api_calls": 0, "adopts": "nothing",
        "STATUS": "GATE-CLOSING DIAGNOSTIC FOR STEP 7. NOT the Step 9 deliverable. "
                  "Step 8 has not launched and is an unapproved gate, so every share "
                  "here is provisional in its population as well as in its status.",
        "population": {
            "line": 4, "n_line4": 152126, "post_D10": n,
            "accounts": int(len(np.unique(uidx))),
            "class_counts": {
                "measured_gap": int((state == 0).sum()),
                "open_ended": int((state == 1).sum()),
                "no_pre_instant_LIVE_per_0021": int((state == 2).sum())}},
        "outcome_definition": "step1 Sec 7 as amended by 0034; tau1 = [T0] + 108d, "
                              "tau2 = [T0] + 199d, Continued read on A_H with the "
                              "|A| >= 1 conjunct; D11 applied",
        "unfiltered_post_D10_counts": {
            "n": n, "never_started": int(ns.sum()),
            "continued": int(cont.sum()), "started_and_left": int(sal.sum())},
    }

    # ---------------------------------------------------------------- settings
    def live_mask(name: str) -> np.ndarray:
        if name == "PF_literal":
            return state == 0
        if name == "PF_0021":
            return state != 1
        thr = dict(THRESHOLDS)[name]
        return ((state == 0) & (gap < thr)) | (state == 2)

    settings = [nm for nm, _ in THRESHOLDS] + ["PF_literal", "PF_0021"]
    masks = {nm: live_mask(nm) for nm in settings}

    # Nesting check: a higher threshold can only make more pairs live.
    assert (masks["T787"] <= masks["T1293"]).all()
    assert (masks["T1293"] <= masks["T2200"]).all()
    assert (masks["PF_literal"] <= masks["PF_0021"]).all()
    prov["nesting_asserted"] = True

    def shares(m: np.ndarray) -> dict:
        d = int(m.sum())
        return {"live_pairs": d,
                "never_started": int((ns & m).sum()),
                "continued": int((cont & m).sum()),
                "started_and_left": int((sal & m).sum()),
                "never_started_pct": 100.0 * (ns & m).sum() / d,
                "continued_pct": 100.0 * (cont & m).sum() / d,
                "started_and_left_pct": 100.0 * (sal & m).sum() / d}

    res = {nm: shares(masks[nm]) for nm in settings}
    for nm in settings:
        m = masks[nm]
        ex = ~m
        res[nm]["excluded_pairs"] = int(ex.sum())
        res[nm]["excluded_share_of_post_D10_pct"] = 100.0 * ex.sum() / n
        res[nm]["excluded_by_channel"] = {
            "measured_gap_test": int((ex & (state == 0)).sum()),
            "open_ended_edge_case": int((ex & (state == 1)).sum()),
            "no_pre_instant": int((ex & (state == 2)).sum())}
        res[nm]["excluded_composition"] = {
            "never_started": int((ex & ns).sum()),
            "continued": int((ex & cont).sum()),
            "started_and_left": int((ex & sal).sum()),
            "never_started_pct_within_excluded":
                (100.0 * (ex & ns).sum() / ex.sum()) if ex.sum() else None}
        res[nm]["accounts_supplying_exclusions"] = int(len(np.unique(uidx[ex])))

    # ------------------------------------------------- account-clustered bootstrap
    accounts, acc_code = np.unique(uidx, return_inverse=True)
    na = len(accounts)
    order = np.argsort(acc_code, kind="stable")
    starts = np.searchsorted(acc_code[order], np.arange(na + 1))
    groups = [order[starts[i]:starts[i + 1]] for i in range(na)]

    rng = np.random.default_rng(SEED)
    keys = ["never_started_pct", "continued_pct", "started_and_left_pct"]
    reps = {nm: {k: np.empty(B) for k in keys} for nm in settings}
    for b in range(B):
        pick = rng.integers(0, na, na)
        rows = np.concatenate([groups[i] for i in pick])
        ns_b, c_b, s_b = ns[rows], cont[rows], sal[rows]
        for nm in settings:
            m = masks[nm][rows]
            d = m.sum()
            if d == 0:
                for k in keys:
                    reps[nm][k][b] = np.nan
                continue
            reps[nm]["never_started_pct"][b] = 100.0 * (ns_b & m).sum() / d
            reps[nm]["continued_pct"][b] = 100.0 * (c_b & m).sum() / d
            reps[nm]["started_and_left_pct"][b] = 100.0 * (s_b & m).sum() / d

    for nm in settings:
        res[nm]["ci95_account_clustered"] = {
            k: [float(np.nanpercentile(reps[nm][k], 2.5)),
                float(np.nanpercentile(reps[nm][k], 97.5))] for k in keys}
    prov["bootstrap"] = {"B": B, "seed": SEED, "clusters_accounts": na,
                         "convention": "percentile, 2.5th and 97.5th, resampling accounts "
                                       "with replacement; the SAME resample is used for "
                                       "every setting in a replicate, so deltas are paired"}

    # --------------------------------------------------------------- deltas, pp
    def delta(a: str, bnm: str) -> dict:
        out = {}
        for k in keys:
            pt = res[bnm][k] - res[a][k]
            dr = reps[bnm][k] - reps[a][k]
            out[k] = {"delta_pp": pt,
                      "paired_ci95_pp": [float(np.nanpercentile(dr, 2.5)),
                                         float(np.nanpercentile(dr, 97.5))]}
        return out

    pairs_to_compare = [
        ("T787", "T1293"), ("T1293", "T2200"), ("T787", "T2200"),
        ("T1293", "PF_0021"), ("T1293", "PF_literal"),
        ("PF_literal", "PF_0021"),
    ]
    prov["deltas_pp"] = {f"{a}__to__{b}": delta(a, b) for a, b in pairs_to_compare}
    prov["max_abs_delta_pp_across_the_clustered_interval"] = max(
        abs(prov["deltas_pp"]["T787__to__T2200"][k]["delta_pp"]) for k in keys)
    prov["max_abs_delta_pp_interval_plus_parameter_free_0021"] = max(
        abs(res[b][k] - res[a][k]) for k in keys
        for a in ["T787", "T1293", "T2200", "PF_0021"]
        for b in ["T787", "T1293", "T2200", "PF_0021"])
    prov["max_abs_delta_pp_including_PF_literal"] = max(
        abs(res[b][k] - res[a][k]) for k in keys
        for a in settings for b in settings)

    prov["settings"] = res
    prov["elapsed_s"] = time.time() - t
    (OUT / "sensitivity.json").write_text(json.dumps(prov, indent=2))

    hdr = f"{'setting':<12}{'live':>10}{'never%':>10}{'cont%':>10}{'S&L%':>10}{'excl':>8}"
    print(hdr)
    for nm in settings:
        r = res[nm]
        print(f"{nm:<12}{r['live_pairs']:>10,}{r['never_started_pct']:>10.4f}"
              f"{r['continued_pct']:>10.4f}{r['started_and_left_pct']:>10.4f}"
              f"{r['excluded_pairs']:>8,}")
    print("\nmax |delta| pp across 787-1293-2200:",
          round(prov["max_abs_delta_pp_across_the_clustered_interval"], 4))
    print("max |delta| pp incl PF_0021        :",
          round(prov["max_abs_delta_pp_interval_plus_parameter_free_0021"], 4))
    print("max |delta| pp incl PF_literal     :",
          round(prov["max_abs_delta_pp_including_PF_literal"], 4))
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
