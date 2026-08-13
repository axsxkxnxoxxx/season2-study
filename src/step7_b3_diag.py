"""Step 7 (instance b3) -- stage 4: diagnostics on the two edge-case buckets,
the inertness claim, and the whole-sweep compounding check.

READ ONLY. ZERO network calls.
Out: processed/step7/b3/diagnostics.json
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step7" / "b3"

W = 108
DAY = 86400.0
PULL = np.datetime64("2026-08-11T00:00:00").astype("datetime64[s]").astype(np.int64)
CURVE_START = np.datetime64("2012-12-02T00:00:00").astype("datetime64[s]").astype(np.int64)


def main() -> None:
    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    br = np.load(OUT / "bracket.npz")
    uid = br["user_idx"]
    t0m = br["t0_midnight_epoch"].astype(np.float64)
    state = br[f"state_W{W}"]
    gap = br[f"gap_days_W{W}"]
    tau1 = t0m + W * DAY

    first = tau_all[offsets[:-1]]
    last = tau_all[offsets[1:] - 1]
    f_p = first[uid]
    l_p = last[uid]

    na = state == 1          # no instant after tau1
    nb = state == 2          # no instant at or before tau1

    d = {}
    d["no_instant_after_tau1"] = {
        "n": int(na.sum()),
        "tau1_after_pull_date_RIGHT_CENSORING": int((tau1[na] > PULL).sum()),
        "tau1_after_pull_date_share": float((tau1[na] > PULL).mean()),
        "tau1_after_accounts_last_instant_but_before_pull": int(
            ((tau1[na] <= PULL) & (tau1[na] > l_p[na])).sum()),
        "median_days_tau1_past_last_instant": float(
            np.median((tau1[na] - l_p[na]) / DAY)),
        "note": ("Step 7 derives on an UNCENSORED population; decisions/0029 places "
                 "right-censoring at Step 8 position 5 and liveness at 6, so this bucket "
                 "is inflated here by pairs D10 removes before liveness ever runs."),
    }
    d["no_instant_at_or_before_tau1"] = {
        "n": int(nb.sum()),
        "median_days_tau1_before_first_instant": float(
            np.median((f_p[nb] - tau1[nb]) / DAY)),
        "tau1_before_calibration_curve_start_2012_12_02": int((tau1[nb] < CURVE_START).sum()),
        "tau1_before_curve_start_share": float((tau1[nb] < CURVE_START).mean()),
        "note": ("decisions/0037 Sec 3: T0 is built from claimed watched_at, liveness from "
                 "insertion time. These are not absent users; their window closed before the "
                 "account existed on the insertion clock. Recorded, not repaired."),
    }

    # inertness claim, tested as stated: does 3.45 / 96.55 hold at every percentile?
    g = gap[state == 0]
    edge = int(na.sum() + nb.sum())
    rows = []
    for q in (90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 99.5, 99.9):
        thr = math.ceil(np.percentile(g, q))
        m = int((g >= thr).sum())
        rows.append({"percentile": q, "threshold_days": int(thr),
                     "measured_gap_exclusions": m, "edge_case_exclusions": edge,
                     "share_measured": m / (m + edge), "share_edge": edge / (m + edge)})
    d["inertness_claim_test"] = {
        "claim_under_test": ("decisions/0038 Sec 5 / the launch brief: the measured-gap test does "
                             "3.45% of exclusions and the edge cases 96.55%, and this holds "
                             "across every percentile from the 90th to the 99.9th"),
        "verdict_on_the_frozen_152126_population": "PARTLY FALSE -- see rows",
        "measured_share_at_99th": rows[[r["percentile"] for r in rows].index(99)]["share_measured"],
        "measured_share_at_90th": rows[0]["share_measured"],
        "measured_share_at_99_9th": rows[-1]["share_measured"],
        "rows": rows,
    }

    # whole-sweep compounding, decisions/0036 Sec 2.1 / 0037 Sec 2
    counts = np.diff(offsets)
    ngaps = np.maximum(counts - 1, 0)
    med = float(np.median(ngaps))
    d["whole_sweep_compounding_check"] = {
        "median_gaps_per_account": med,
        "P_trip_at_99th_median_account": float(1 - 0.99 ** med),
        "P_trip_at_99_9th_median_account": float(1 - 0.999 ** med),
        "note": "corroborates decisions/0037 Sec 2; the whole-sweep alternative is not used",
    }

    # ties in the bracketing distribution: why one-gap-per-pair matters
    vals, cnt = np.unique(g, return_counts=True)
    d["bracketing_gap_ties"] = {
        "n_gaps": int(len(g)),
        "n_distinct_gap_values": int(len(vals)),
        "share_of_pairs_sharing_a_gap_value_with_another_pair": float(
            (cnt[np.searchsorted(vals, g)] > 1).mean()),
        "largest_tie_group": int(cnt.max()),
        "note": ("pairs on one account whose tau1 falls in the same silence share one gap "
                 "exactly; this is the mechanism behind the weighting lever in 0038 Sec 3, "
                 "and it is why the iid bootstrap CI is degenerate at its lower end"),
    }

    (OUT / "diagnostics.json").write_text(json.dumps(d, indent=2))
    print(json.dumps(d, indent=2))


if __name__ == "__main__":
    main()
