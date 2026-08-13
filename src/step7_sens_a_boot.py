"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 4 of 4 — the yardstick.

"Insensitive" is a claim about size, and a delta in percentage points means nothing until it
is set against how precisely the share is known at all. Two bootstrap quantities, both
ACCOUNT-CLUSTERED (resample the 2,402 accounts with replacement, take all their pairs),
because pairs within an account are not independent — the same reason the threshold carries a
clustered interval rather than an i.i.d. one:

  1. A 95% clustered interval for each of the three shares at the point value T = 1,293 d.
     This is the width the deltas have to be compared against.
  2. The clustered distribution of the DELTA itself between settings, computed PAIRED inside
     each replicate. The two settings are nested subsets of the same pairs, so the delta is
     far more precisely known than either share; the paired form is the honest test of
     whether the delta is distinguishable from zero.

Shares are ratios of sums over accounts, so per-account count vectors are sufficient
statistics and no replicate touches the pair table.

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/sens_a")

B = 4000
SEED = 20260813
THRESHOLDS = [787, 1293, 2200]


def main():
    st = np.load(os.path.join(OUT, "pair_states.npz"))
    user = st["user"]
    never, cont, left = st["never"], st["continued"], st["left"]
    no_before, no_after, gap, measured = (
        st["no_before"], st["no_after"], st["gap"], st["measured"])

    acc, ainv = np.unique(user, return_inverse=True)
    na = acc.size

    live_by = {}
    for T in THRESHOLDS:
        live_by[f"threshold_{T}d"] = ~(no_after | (measured & (gap >= T)))
    live_by["parameter_free_LIMIT"] = ~no_after
    live_by["parameter_free_BRACKET"] = measured

    # per-account (never, continued, left) counts under each setting
    agg = {}
    for k, live in live_by.items():
        agg[k] = np.stack([
            np.bincount(ainv[never & live], minlength=na),
            np.bincount(ainv[cont & live], minlength=na),
            np.bincount(ainv[left & live], minlength=na),
        ], axis=1).astype(np.float64)

    def shares(mat):
        tot = mat.sum(axis=1, keepdims=True)
        tot = np.where(tot == 0, np.nan, tot)
        return 100.0 * mat / tot

    point = {k: shares(v.sum(axis=0)[None, :])[0] for k, v in agg.items()}

    rng = np.random.default_rng(SEED)
    keys = list(agg.keys())
    reps = {k: np.empty((B, 3)) for k in keys}
    for b in range(B):
        idx = rng.integers(0, na, size=na)
        cnt = np.bincount(idx, minlength=na).astype(np.float64)
        for k in keys:
            tot = cnt @ agg[k]
            reps[k][b] = 100.0 * tot / tot.sum()

    states = ["never_started", "continued", "started_and_left"]

    ci = {}
    for k in keys:
        ci[k] = {}
        for j, s in enumerate(states):
            lo, hi = np.percentile(reps[k][:, j], [2.5, 97.5])
            ci[k][s] = {
                "point_pct": round(float(point[k][j]), 4),
                "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                "ci_width_pp": round(float(hi - lo), 4),
                "clustered_se_pp": round(float(reps[k][:, j].std(ddof=1)), 4),
            }

    def paired(a, b):
        dd = reps[b] - reps[a]
        obs = point[b] - point[a]
        out = {}
        for j, s in enumerate(states):
            lo, hi = np.percentile(dd[:, j], [2.5, 97.5])
            out[s] = {
                "observed_delta_pp": round(float(obs[j]), 4),
                "paired_clustered_95_ci_pp": [round(float(lo), 4), round(float(hi), 4)],
                "paired_clustered_se_pp": round(float(dd[:, j].std(ddof=1)), 4),
                "ci_excludes_zero": bool(lo > 0 or hi < 0),
            }
        return out

    deltas = {
        "787_to_2200_FULL_CLUSTERED_INTERVAL": paired("threshold_787d", "threshold_2200d"),
        "787_to_1293": paired("threshold_787d", "threshold_1293d"),
        "1293_to_2200": paired("threshold_1293d", "threshold_2200d"),
        "1293_to_parameter_free_LIMIT": paired("threshold_1293d", "parameter_free_LIMIT"),
        "1293_to_parameter_free_BRACKET": paired("threshold_1293d", "parameter_free_BRACKET"),
    }

    # ratio of the largest candidate-setting movement to the sampling width at the point value
    ratio = {}
    for j, s in enumerate(states):
        cand = [point[k][j] for k in
                ("threshold_787d", "threshold_1293d", "threshold_2200d",
                 "parameter_free_LIMIT")]
        span = float(max(cand) - min(cand))
        w = ci["threshold_1293d"][s]["ci_width_pp"]
        ratio[s] = {
            "threshold_span_pp": round(span, 4),
            "clustered_ci_width_pp": w,
            "span_as_share_of_ci_width": round(span / w, 4) if w else None,
        }

    # seed stability: does the answer depend on the bootstrap draw?
    alt = {}
    for alt_seed in (11, 99, 777):
        r2 = np.random.default_rng(alt_seed)
        rr = np.empty((1000, 3))
        for b in range(1000):
            idx = r2.integers(0, na, size=na)
            cnt = np.bincount(idx, minlength=na).astype(np.float64)
            tot = cnt @ agg["threshold_1293d"]
            rr[b] = 100.0 * tot / tot.sum()
        alt[str(alt_seed)] = {
            s: [round(float(x), 4) for x in np.percentile(rr[:, j], [2.5, 97.5])]
            for j, s in enumerate(states)}

    out = {
        "step": 7,
        "what": "GATE-CLOSING SENSITIVITY DIAGNOSTIC for Step 7 (decisions/0041 SS4). "
                "NOT the Step 9 deliverable. Step 8 has not launched.",
        "instance": "sens_a",
        "api_calls": 0,
        "bootstrap": {"B": B, "seed": SEED, "unit": "account",
                      "n_accounts": int(na),
                      "note": "clustered on the account, not the pair; the i.i.d. interval "
                              "would overstate precision for the same reason it does on the "
                              "threshold itself"},
        "shares_with_clustered_intervals": ci,
        "paired_clustered_deltas": deltas,
        "span_against_sampling_width": ratio,
        "seed_stability_of_the_1293_interval_B1000": alt,
    }
    with open(os.path.join(OUT, "bootstrap.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    np.savez_compressed(os.path.join(OUT, "bootstrap_replicates.npz"),
                        **{k: v for k, v in reps.items()})
    print(json.dumps({"ci_1293": ci["threshold_1293d"],
                      "delta_787_2200": deltas["787_to_2200_FULL_CLUSTERED_INTERVAL"],
                      "delta_1293_pf_bracket": deltas["1293_to_parameter_free_BRACKET"],
                      "span_vs_width": ratio}, indent=2))


if __name__ == "__main__":
    main()
