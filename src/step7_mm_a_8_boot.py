"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 8 — SAMPLING ERROR.

BOOTSTRAP DESIGN, STATED EXPLICITLY (0052 SS6 records that the two arms used different designs
last time and were not diffable, and that the spec fixes neither):

  unit          ACCOUNT. Accounts are resampled with replacement and ALL of a resampled account's
                pairs travel with it, because liveness evidence is account-wide even though the
                filter is pair-level (0034).
  replicates    B = 4,000.
  seed          20260813, numpy default_rng. Same seed and B as every prior namespace-`a` Step 7
                run, so rows are comparable line for line with the ALT-BROAD deliverable.
  interval      percentile, 2.5 / 97.5.
  BOTH levels AND movements are reported, and neither is presented as the design:
    - LEVELS    the three shares under the rule, and under no filter at all, each with its own CI;
    - MOVEMENTS the PAIRED delta (rule minus no filter) computed INSIDE each replicate, which is
                the correct object for "did the filter move the headline", because the two
                settings share the resampled accounts and the difference is far less variable
                than either level.
  The bound endpoints are bootstrapped too, each on the POSITION-5 denominator of its own
  replicate.

A BOUND IS NOT A CONFIDENCE INTERVAL. It is the identified set given the rule. The bootstrap says
only how much of each endpoint is sampling noise.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/mm_a")

B = 4000
SEED = 20260813
STATES = ["never_started", "continued", "started_and_left"]
ENDPOINTS = ["never_started_floor", "never_started_ceiling",
             "started_and_left_floor", "started_and_left_ceiling",
             "continued_floor", "continued_ceiling"]


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    rng = np.random.default_rng(SEED)
    out = {"step": 7, "instance": "mm_a", "stage": 8, "api_calls": 0,
           "bootstrap_design": {
               "unit": "account", "B": B, "seed": SEED, "rng": "numpy default_rng",
               "resample": "accounts with replacement; all of an account's pairs travel with it",
               "interval": "percentile 2.5 / 97.5",
               "reports": "LEVELS and PAIRED MOVEMENTS, both, explicitly labelled",
               "caveat": "a bound is an identified set, not a confidence interval"},
           "by_population": {}}

    for nm, p in pops.items():
        idx = np.flatnonzero(p)
        acc, ainv = np.unique(user[idx], return_inverse=True)
        na = acc.size
        nev, co, le = never[idx], cont[idx], left[idx]
        ens, esl, e = ex_ns[idx], ex_sl[idx], ex[idx]

        # per-account count vector: [ns_live, cont, sl_live, k_ns, k_sl]
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
            F = N - k_ns - k_sl                        # post-liveness population
            rule = 100.0 * np.array([ns_l, c, sl_l]) / F
            none = 100.0 * np.array([ns_l + k_ns, c, sl_l + k_sl]) / N
            ends = 100.0 * np.array([
                ns_l, ns_l + k_ns,                     # never-started floor, ceiling
                sl_l, sl_l + k_sl + k_ns,              # started-and-left floor, ceiling
                c, c + k_ns + k_sl,                    # continued floor, ceiling
            ]) / N
            return rule, none, ends

        pr, pu, pe = stats(agg.sum(0))
        rr = np.empty((B, 3)); ru = np.empty((B, 3)); en = np.empty((B, 6))
        for b in range(B):
            j = rng.integers(0, na, size=na)
            w = np.bincount(j, minlength=na).astype(np.float64)
            s = stats(w @ agg)
            rr[b], ru[b], en[b] = s

        rec = {"population_pairs": int(idx.size), "accounts": int(na), "LEVELS": {}}
        for label, point, reps in (("ADOPTED_RULE", pr, rr), ("no_liveness_filter", pu, ru)):
            d = {}
            for k, s in enumerate(STATES):
                lo, hi = np.percentile(reps[:, k], [2.5, 97.5])
                d[s] = {"point_pct": round(float(point[k]), 4),
                        "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                        "ci_width_pp": round(float(hi - lo), 4)}
            rec["LEVELS"][label] = d

        dd = rr - ru
        rec["MOVEMENTS_paired_rule_minus_no_filter"] = {}
        for k, s in enumerate(STATES):
            lo, hi = np.percentile(dd[:, k], [2.5, 97.5])
            rec["MOVEMENTS_paired_rule_minus_no_filter"][s] = {
                "observed_pp": round(float(pr[k] - pu[k]), 4),
                "paired_clustered_95_ci_pp": [round(float(lo), 4), round(float(hi), 4)],
                "ci_excludes_zero": bool(lo > 0 or hi < 0)}

        rec["bound_endpoints"] = {}
        for k, s in enumerate(ENDPOINTS):
            lo, hi = np.percentile(en[:, k], [2.5, 97.5])
            rec["bound_endpoints"][s] = {
                "point_pct": round(float(pe[k]), 6),
                "clustered_95_ci_pct": [round(float(lo), 4), round(float(hi), 4)],
                "ci_width_pp": round(float(hi - lo), 4)}
        rec["bound_width_against_sampling_width"] = {}
        for s, a, b_ in (("never_started", 0, 1), ("started_and_left", 2, 3),
                         ("continued", 4, 5)):
            wb = float(pe[b_] - pe[a])
            ws = rec["LEVELS"]["ADOPTED_RULE"][s]["ci_width_pp"]
            rec["bound_width_against_sampling_width"][s] = {
                "bound_width_pp": round(wb, 6),
                "account_clustered_sampling_width_pp": ws,
                "ratio": round(wb / ws, 4) if ws else None,
                "note": "ratio is computed on the OPERATIVE bound, not on any conditional "
                        "sub-interval (0052 SS6 records an arm that used the sub-interval and "
                        "understated the ratio by 7.5x)"}

        out["by_population"][nm] = rec
        np.savez_compressed(os.path.join(OUT, f"bootstrap_replicates_{nm}.npz"),
                            shares_rule=rr, shares_nofilter=ru, endpoints=en)
        print(nm, json.dumps(rec["bound_width_against_sampling_width"]))

    with open(os.path.join(OUT, "bootstrap.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out["by_population"]["APPLY"], indent=2))


if __name__ == "__main__":
    main()
