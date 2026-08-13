"""Step 7 rerun (instance b4) -- stage 3: threshold, realised rates, inertness.

READ ONLY. ZERO network calls.

Reference distribution (decisions/0037 Sec 1, 0038 Sec 2/3, 0040 Sec 2):
  the BRACKETING-gap distribution itself, ONE GAP PER PAIR, on the post-D10
  population -- derivation and application populations identical.
  Percentile: the 99th (0036 Sec 1 as amended, 0037), rounded UP (0025).

PRIMARY reference set = the EXTENDED set: every post-D10 pair for which a
bracketing gap is defined, i.e. measured gaps PLUS open-ended gaps entered as
+inf. 0040 Sec 2 requires this: after D10 the open-ended share drops below 1%,
so the 99th percentile over the extended set is finite and edge case (i) no
longer needs to be a separate ruling.

Pairs with no instant at or before tau1 have NO bracketing gap and are LIVE per
0021 (0036 Sec 2.3(ii) WITHDRAWN by 0040 Sec 1). Two readings of their place in
the reference are possible and the spec does not settle it; both are reported.

Out: processed/step7/b4/threshold.json
     processed/step7/b4/gap_hist.npz  (aggregate histogram for the chart)
"""
from __future__ import annotations

import json
import math
import time
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b4"

W_ADOPTED = 108
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
PCTLS = [90.0, 95.0, 97.5, 99.0, 99.5, 99.9]
DAY = 86400.0


def r7(sorted_x: np.ndarray, q: float) -> float:
    """R type-7 / numpy-default 'linear' quantile, inf-safe."""
    n = len(sorted_x)
    if n == 0:
        return float("nan")
    h = (n - 1) * q
    lo = int(math.floor(h))
    frac = h - lo
    if lo + 1 >= n or frac == 0.0:
        return float(sorted_x[lo])
    a, b = float(sorted_x[lo]), float(sorted_x[lo + 1])
    if np.isinf(b):
        return float("inf")
    return a + frac * (b - a)


def summarise(sorted_x: np.ndarray) -> dict:
    n = len(sorted_x)
    fin = sorted_x[np.isfinite(sorted_x)]
    return {
        "n": int(n),
        "n_infinite": int(n - len(fin)),
        "min_d": float(fin[0]) if len(fin) else None,
        "p25_d": r7(sorted_x, 0.25),
        "median_d": r7(sorted_x, 0.50),
        "p75_d": r7(sorted_x, 0.75),
        "p90_d": r7(sorted_x, 0.90),
        "p99_d": r7(sorted_x, 0.99),
        "max_finite_d": float(fin[-1]) if len(fin) else None,
        "mean_finite_d": float(fin.mean()) if len(fin) else None,
    }


def main() -> None:
    t = time.time()
    z = np.load(OUT / "bracket.npz")
    res: dict = {
        "instance": "data-scientist-b / namespace b4",
        "stage": "3 -- threshold and realised rates",
        "api_calls": 0,
        "percentile": 99.0,
        "rounding": "ceiling, per decisions/0025",
        "quantile_method": "R type-7 / numpy 'linear', inf-safe reimplementation",
    }

    # ---- pooled gap distribution, for the length-bias corroboration only ----
    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    d = np.diff(tau_all) / DAY
    boundary = np.zeros(len(d), dtype=bool)
    boundary[offsets[1:-1] - 1] = True          # differences that straddle accounts
    pooled = np.sort(d[~boundary])
    res["pooled_gap_distribution_all_accounts"] = summarise(pooled)
    pooled_p99 = r7(pooled, 0.99)
    res["pooled_gap_distribution_all_accounts"]["note"] = (
        "NOT the reference distribution -- 0037 Sec 1 withdrew the pooled basis. "
        "Reported only to corroborate the length bias."
    )
    print(f"pooled gaps {len(pooled):,}  p99 {pooled_p99:.4f} d  ({time.time()-t:.1f}s)", flush=True)
    del d, boundary

    arms = {}
    for W in W_ARMS:
        gap = z[f"gap_days_W{W}"]
        state = z[f"state_W{W}"]
        d10 = z[f"d10_W{W}"]

        m = (state == 0) & d10                # measured bracketing gap
        o = (state == 1) & d10                # open-ended (+inf)
        b = (state == 2) & d10                # no instant at or before tau1 -> LIVE per 0021
        n_pop = int(d10.sum())

        meas = np.sort(gap[m])
        ext = np.concatenate([meas, np.full(int(o.sum()), np.inf)])          # already sorted
        allp = np.concatenate([np.zeros(int(b.sum())), ext])                 # variant V3

        a: dict = {
            "W": W,
            "population_post_D10": n_pop,
            "counts": {
                "measured_gap": int(m.sum()),
                "open_ended": int(o.sum()),
                "no_instant_at_or_before_tau1_LIVE": int(b.sum()),
            },
            "open_ended_share_of_extended": float(o.sum() / len(ext)),
            "percentile_at_which_extended_p_becomes_infinite": 100.0 * (1 - o.sum() / len(ext)),
        }
        a["bracketing_gap_distribution_measured"] = summarise(meas)
        a["bracketing_gap_distribution_extended"] = summarise(ext)

        # --- the three readings of the reference set ---
        variants = {
            "V1_extended_PRIMARY": ext,
            "V2_measured_only_0039_basis": meas,
            "V3_all_pairs_no_pre_instant_as_zero": allp,
        }
        vres = {}
        for name, arr in variants.items():
            raw = r7(arr, 0.99)
            thr = float("inf") if not np.isfinite(raw) else float(math.ceil(raw))
            # not live iff bracketing gap >= threshold. An open-ended gap is +inf and
            # therefore fails ANY threshold, a finite one or an infinite one (inf >= inf).
            excl_gap = int((meas >= thr).sum())
            excl_open = int(o.sum())
            excl = excl_gap + excl_open
            vres[name] = {
                "reference_n": int(len(arr)),
                "raw_p99_days": raw,
                "threshold_days_ceiling": thr,
                "not_live_total": excl,
                "not_live_measured_gap": excl_gap,
                "not_live_open_ended": excl_open,
                "realised_rate_vs_measured_gap_pairs": excl_gap / int(m.sum()),
                "realised_rate_vs_extended_set": excl / len(ext),
                "realised_rate_vs_all_post_D10_pairs": excl / n_pop,
                "live_pairs": n_pop - excl,
                "live_share": (n_pop - excl) / n_pop,
            }
        a["reference_set_variants"] = vres

        # --- inertness split, at the primary variant, across percentiles ---
        thr_star = vres["V1_extended_PRIMARY"]["threshold_days_ceiling"]
        sweep = {}
        for p in PCTLS:
            raw = r7(ext, p / 100.0)
            th = float("inf") if not np.isfinite(raw) else float(math.ceil(raw))
            eg = int((meas >= th).sum())
            eo = int(o.sum())
            tot = eg + eo
            sweep[f"{p}"] = {
                "raw_days": raw,
                "threshold_days": th,
                "gap_test_exclusions": eg,
                "edge_case_open_ended_exclusions": eo,
                "gap_test_share_of_exclusions": (eg / tot) if tot else None,
                "edge_case_share_of_exclusions": (eo / tot) if tot else None,
                "realised_rate_vs_extended_set": tot / len(ext),
            }
        a["percentile_sweep_primary_variant"] = sweep

        # --- length bias: bracketing vs pooled ---
        a["length_bias"] = {
            "pooled_p99_days_raw": pooled_p99,
            "pooled_p99_days_ceiling": float(math.ceil(pooled_p99)),
            "share_bracketing_ge_pooled_p99_RAW_comparator": float((meas >= pooled_p99).mean()),
            "share_bracketing_ge_pooled_p99_CEILING_comparator": float(
                (meas >= math.ceil(pooled_p99)).mean()
            ),
            "comparator_note": (
                "decisions/0040 Sec 5: the superseded run's two artifacts published 34.1% and "
                "36.96% for this quantity and misattributed the difference to a different "
                "population. It is the raw-vs-ceiling comparator. Both are stated here."
            ),
            "pooled_median_days": r7(pooled, 0.5),
            "bracketing_median_days": r7(meas, 0.5),
        }

        # --- tie structure, the reason the interval must be account-clustered ---
        vals, cnts = np.unique(meas, return_counts=True)
        a["tie_structure_measured_gaps"] = {
            "distinct_values": int(len(vals)),
            "pairs_sharing_a_value_with_another_pair": int(cnts[cnts > 1].sum()),
            "share_sharing": float(cnts[cnts > 1].sum() / len(meas)),
            "largest_tie_group": int(cnts.max()),
        }

        arms[str(W)] = a
        v = vres["V1_extended_PRIMARY"]
        print(
            f"W={W:3d}  ext n={len(ext):,}  raw p99 {v['raw_p99_days']:.4f} -> {v['threshold_days_ceiling']:.0f} d  "
            f"not-live {v['not_live_total']:,} "
            f"({v['realised_rate_vs_extended_set']:.4%} of extended, "
            f"{v['realised_rate_vs_all_post_D10_pairs']:.4%} of all)  ({time.time()-t:.1f}s)",
            flush=True,
        )

        if W == W_ADOPTED:
            h, edges = np.histogram(np.log10(np.clip(meas, 1e-7, None)), bins=140, range=(-7, 4))
            np.savez(OUT / "gap_hist.npz", counts=h, log10_edges=edges,
                     n_open_ended=int(o.sum()), threshold=thr_star)

    res["arms"] = arms
    res["adopted_arm"] = str(W_ADOPTED)
    res["elapsed_s"] = time.time() - t
    (OUT / "threshold.json").write_text(json.dumps(res, indent=2, default=float))
    print("wrote", OUT / "threshold.json")


if __name__ == "__main__":
    main()
