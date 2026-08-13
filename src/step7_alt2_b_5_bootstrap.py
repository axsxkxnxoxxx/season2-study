"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 5.

Account-clustered bootstrap at W = 108 on BOTH populations, for the adopted
rule and for no filter at all. Gaps and outcomes within an account are not
independent, so the cluster is the account. Percentile interval, 2.5th and
97.5th; the SAME resample is used for both rules inside a replicate, so the
rule-minus-no-filter deltas are paired.

The bound's ceiling is resampled too, so the reported bound width can be set
against the sampling width.

ZERO network calls. Reads only.

Out: processed/step7/alt2_b/bootstrap.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "alt2_b"
W = 108
B = 2000
SEED = 20260813
RULES = ["NO_FILTER", "ADOPTED"]
KEYS = ["never_started_pct", "continued_pct", "started_and_left_pct"]


def main() -> None:
    t = time.time()
    pz = np.load(OUT / "pairs.npz")
    oz = np.load(OUT / "outcomes.npz")
    res: dict = {"instance": "data-scientist-b", "namespace": "alt2_b", "stage": 5,
                 "api_calls": 0, "adopts": "nothing", "W": W, "B": B, "seed": SEED,
                 "cluster": "account",
                 "convention": "percentile 2.5/97.5; one resample per replicate shared by "
                               "both rules, so the deltas are paired",
                 "by_population": {}}

    for popname in ("DERIV", "APPLY"):
        d10 = pz[f"d10_W{W}"]
        base = d10 & pz["in_line4"] if popname == "DERIV" else d10
        uidx = pz["user_idx"][base]
        started = oz[f"started_W{W}"][base]
        cont = oz[f"cont_W{W}"][base]
        sal = oz[f"sal_W{W}"][base]
        ns = ~started
        noaft = pz[f"no_after_W{W}"][base]
        n = int(base.sum())
        masks = {"NO_FILTER": np.zeros(n, bool), "ADOPTED": noaft & ns}

        accounts, code = np.unique(uidx, return_inverse=True)
        na = len(accounts)
        order = np.argsort(code, kind="stable")
        starts = np.searchsorted(code[order], np.arange(na + 1))
        groups = [order[starts[i]:starts[i + 1]] for i in range(na)]

        rng = np.random.default_rng(SEED)
        reps = {r: {k: np.empty(B) for k in KEYS} for r in RULES}
        boundreps = {r: np.empty(B) for r in RULES}
        for b in range(B):
            pick = rng.integers(0, na, na)
            rows = np.concatenate([groups[i] for i in pick])
            ns_b, c_b, s_b = ns[rows], cont[rows], sal[rows]
            for r in RULES:
                live = ~masks[r][rows]
                d = int(live.sum())
                ex = len(rows) - d
                nsl = int((ns_b & live).sum())
                reps[r]["never_started_pct"][b] = 100.0 * nsl / d
                reps[r]["continued_pct"][b] = 100.0 * (c_b & live).sum() / d
                reps[r]["started_and_left_pct"][b] = 100.0 * (s_b & live).sum() / d
                boundreps[r][b] = 100.0 * (nsl + ex) / (d + ex)
            if b and b % 500 == 0:
                print(f"  {popname} {b}/{B}  ({time.time() - t:.0f}s)", flush=True)

        pop_out = {"n": n, "accounts": na, "ci95": {}, "paired_delta_pp": {}}
        for r in RULES:
            pop_out["ci95"][r] = {k: [float(np.percentile(reps[r][k], 2.5)),
                                      float(np.percentile(reps[r][k], 97.5))] for k in KEYS}
            pop_out["ci95"][r]["bound_ceiling_pct"] = [
                float(np.percentile(boundreps[r], 2.5)),
                float(np.percentile(boundreps[r], 97.5))]
            pop_out["ci95"][r]["clustered_width_pp"] = {
                k: float(np.percentile(reps[r][k], 97.5) - np.percentile(reps[r][k], 2.5))
                for k in KEYS}
        pop_out["paired_delta_pp"] = {
            k: {"mean_delta_pp": float(np.mean(reps["ADOPTED"][k] - reps["NO_FILTER"][k])),
                "paired_ci95_pp": [
                    float(np.percentile(reps["ADOPTED"][k] - reps["NO_FILTER"][k], 2.5)),
                    float(np.percentile(reps["ADOPTED"][k] - reps["NO_FILTER"][k], 97.5))],
                "excludes_zero": bool(
                    np.percentile(reps["ADOPTED"][k] - reps["NO_FILTER"][k], 2.5) > 0
                    or np.percentile(reps["ADOPTED"][k] - reps["NO_FILTER"][k], 97.5) < 0)}
            for k in KEYS}
        res["by_population"][popname] = pop_out
        print(f"{popname} done ({time.time() - t:.0f}s)", flush=True)

    res["elapsed_s"] = time.time() - t
    (OUT / "bootstrap.json").write_text(json.dumps(res, indent=2))
    for popname in ("DERIV", "APPLY"):
        p = res["by_population"][popname]
        print(f"\n=== {popname}  n={p['n']:,}  accounts={p['accounts']:,}")
        for r in RULES:
            c = p["ci95"][r]["never_started_pct"]
            print(f"  {r:<10} NS 95% CI [{c[0]:.4f}, {c[1]:.4f}]  width {c[1]-c[0]:.4f} pp")
        d = p["paired_delta_pp"]["never_started_pct"]
        print(f"  paired d NS {d['mean_delta_pp']:+.4f} pp "
              f"[{d['paired_ci95_pp'][0]:+.4f}, {d['paired_ci95_pp'][1]:+.4f}]"
              f"{'  EXCLUDES 0' if d['excludes_zero'] else ''}")


if __name__ == "__main__":
    main()
