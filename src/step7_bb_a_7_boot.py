"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 7 of 8 — sampling error.

Account-clustered bootstrap, B = 4,000, seed 20260813 — the same design and seed as every
earlier Step 7 run, so the rows are comparable line for line. Accounts are resampled with
replacement and all of a resampled account's pairs travel with it, because liveness evidence is
account-wide even though the filter is pair-level.

Reported on BOTH populations, every figure tagged:
  - the three outcome shares under the rule and under no filter at all
  - the PAIRED delta between those two settings, computed inside each replicate
  - both bounds' endpoints, each on the position-5 denominator of that replicate
  - each bound's width against the sampling width of the quantity it bounds

The bounds are NOT confidence intervals. They are the identified set given the rule; the
bootstrap says only how much of each endpoint is sampling noise.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/bb_a")

B = 4000
SEED = 20260813
STATES = ["never_started", "continued", "started_and_left"]


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    rng = np.random.default_rng(SEED)
    out = {"step": 7, "instance": "bb_a", "stage": 7, "api_calls": 0,
           "bootstrap": {"B": B, "seed": SEED, "unit": "account",
                         "resample": "accounts with replacement, all their pairs travel",
                         "caveat": "a bound is an identified set, not a confidence interval"},
           "by_population": {}}

    for nm, p in pops.items():
        idx = np.flatnonzero(p)
        acc, ainv = np.unique(user[idx], return_inverse=True)
        na = acc.size
        nev, co, le = never[idx], cont[idx], left[idx]
        ens, esl = ex_ns[idx], ex_sl[idx]
        e = ex[idx]

        # per-account count vectors: [ns_live, cont, sl_live, k_ns, k_sl]
        agg = np.stack([
            np.bincount(ainv[nev & ~e], minlength=na),
            np.bincount(ainv[co], minlength=na),
            np.bincount(ainv[le & ~e], minlength=na),
            np.bincount(ainv[ens], minlength=na),
            np.bincount(ainv[esl], minlength=na),
        ], axis=1).astype(np.float64)

        def stats(v):
            ns_l, c, sl_l, k_ns, k_sl = v
            N = ns_l + c + sl_l + k_ns + k_sl          # position-5 population
            F = N - k_ns - k_sl                        # filtered population
            rule = 100.0 * np.array([ns_l, c, sl_l]) / F
            none = 100.0 * np.array([ns_l + k_ns, c, sl_l + k_sl]) / N
            return (rule, none,
                    100.0 * (ns_l) / N, 100.0 * (ns_l + k_ns) / N,      # ns floor, ceiling
                    100.0 * (sl_l) / N, 100.0 * (sl_l + k_sl + k_ns) / N)  # sl floor, ceiling

        pt = stats(agg.sum(0))
        rr = np.empty((B, 3)); ru = np.empty((B, 3)); en = np.empty((B, 4))
        for b in range(B):
            j = rng.integers(0, na, size=na)
            w = np.bincount(j, minlength=na).astype(np.float64)
            s = stats(w @ agg)
            rr[b], ru[b] = s[0], s[1]
            en[b] = s[2:]

        rec = {"population_pairs": int(idx.size), "accounts": int(na), "settings": {}}
        for label, point, reps in (("ADOPTED_RULE", pt[0], rr),
                                   ("no_liveness_filter", pt[1], ru)):
            d = {}
            for k, s in enumerate(STATES):
                lo, hi = np.percentile(reps[:, k], [2.5, 97.5])
                d[s] = {"point_pct": round(float(point[k]), 4),
                        "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                        "ci_width_pp": round(float(hi - lo), 4)}
            rec["settings"][label] = d

        dd = rr - ru
        rec["paired_delta_rule_minus_no_filter"] = {}
        for k, s in enumerate(STATES):
            lo, hi = np.percentile(dd[:, k], [2.5, 97.5])
            rec["paired_delta_rule_minus_no_filter"][s] = {
                "observed_pp": round(float(pt[0][k] - pt[1][k]), 4),
                "paired_clustered_95_ci_pp": [round(float(lo), 4), round(float(hi), 4)],
                "ci_excludes_zero": bool(lo > 0 or hi < 0)}

        names = ["never_started_floor", "never_started_ceiling",
                 "started_and_left_floor", "started_and_left_ceiling"]
        rec["bound_endpoints"] = {}
        for k, s in enumerate(names):
            lo, hi = np.percentile(en[:, k], [2.5, 97.5])
            rec["bound_endpoints"][s] = {
                "point_pct": round(float(pt[2 + k]), 6),
                "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                "ci_width_pp": round(float(hi - lo), 4)}
        for nmb, a, bnd in (("never_started", 0, 1), ("started_and_left", 2, 3)):
            w_bound = float(pt[2 + bnd] - pt[2 + a])
            w_samp = rec["settings"]["ADOPTED_RULE"][nmb]["ci_width_pp"]
            rec["bound_endpoints"][f"{nmb}_bound_width_pp"] = round(w_bound, 6)
            rec["bound_endpoints"][f"{nmb}_bound_width_over_sampling_width"] = (
                round(w_bound / w_samp, 4) if w_samp else None)

        out["by_population"][nm] = rec
        np.savez_compressed(os.path.join(OUT, f"bootstrap_replicates_{nm}.npz"),
                            shares_rule=rr, shares_nofilter=ru, endpoints=en)
        print(nm, json.dumps(rec["bound_endpoints"]))

    with open(os.path.join(OUT, "bootstrap.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out["by_population"]["APPLY"], indent=2))


if __name__ == "__main__":
    main()
