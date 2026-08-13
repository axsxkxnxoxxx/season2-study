"""Step 7 (frozen-spec run), instance A3 — the threshold refitted at each Step 13 W arm
(decisions/0038 SS6), plus two diagnostics:

  (a) a CORRECTED right-censoring diagnostic on the 'no insertion instant after tau1' bucket.
      Testing tau1 against the account's own last instant is tautological under the bucket's
      own definition; the informative tests are against the GLOBAL sweep end and the pull
      instant.
  (b) the inertness split measured on every waterfall line, to locate where 0038 SS5's
      3.45% / 96.55% came from and whether it survives on the frozen population.

Reference and application populations are identical at every arm: the 152,126.
Zero API calls.
"""
import json
import math
import os

import numpy as np
import pandas as pd

from step7_a3_bracketing import (OUT, P5, PCTL, PUBLISHED_WATERFALL, SEC_PER_DAY,
                                 FROZEN_LINE, bracketing, build_waterfall)

W_ARMS = [46, 77, 108, 150, 213]          # decisions/0027, as named in the launch prompt
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def main():
    di = np.load(os.path.join(OUT, "distinct_instants.npz"))
    uids, d_starts, d_ends, d_inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)
    sweep_end = float(d_inst.max())

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)
    masks = build_waterfall(p)
    assert [int(m.sum()) for m in masks] == PUBLISHED_WATERFALL
    ref = masks[FROZEN_LINE]

    arms = {}
    for w in W_ARMS:
        tau1, gap, nb, na = bracketing(p, d_starts, d_ends, d_inst, u2slot, w)
        meas = ~nb & ~na
        m = ref & meas
        g = gap[m]
        raw = float(np.percentile(g, PCTL))
        thr = int(math.ceil(raw))
        n_pairs = int(ref.sum())
        n_meas = int(m.sum())
        n_na = int((ref & na).sum())
        n_nb = int((ref & nb).sum())
        dead = int((g >= thr).sum())
        tot = dead + n_na + n_nb
        nam = ref & na
        arms[str(w)] = {
            "W_days": w,
            "p99_raw_days": raw,
            "refitted_threshold_days": thr,
            "n_pairs": n_pairs,
            "live": n_meas - dead,
            "not_live_measured_gap": dead,
            "not_live_no_instant_after_tau1": n_na,
            "not_live_no_instant_at_or_before_tau1": n_nb,
            "not_live_total": tot,
            "n_measured_gap": n_meas,
            "realised_exclusion_rate_measured_gap_pairs": round(dead / n_meas, 6),
            "realised_exclusion_rate_of_population": round(tot / n_pairs, 6),
            "bracketing_median_days": float(np.median(g)),
            "no_after_tau1_past_global_sweep_end": int((tau1[nam] > sweep_end).sum()),
            "no_after_tau1_past_pull_instant": int((tau1[nam] > TAU_PULL).sum()),
        }
        print(f"W={w:>4}  p99={raw:10.4f}  thr={thr:>5}d  meas={n_meas:>7}  "
              f"dead={dead:>6}  rate={dead / n_meas:.6f}  "
              f"na={n_na}  nb={n_nb}  censored_of_na="
              f"{arms[str(w)]['no_after_tau1_past_global_sweep_end']}")

    # frozen-threshold-across-arms counterfactual: what a single 108-d threshold delivers
    thr108 = arms["108"]["refitted_threshold_days"]
    frozen_cf = {}
    for w in W_ARMS:
        tau1, gap, nb, na = bracketing(p, d_starts, d_ends, d_inst, u2slot, w)
        m = ref & ~nb & ~na
        g = gap[m]
        frozen_cf[str(w)] = {
            "threshold_days": thr108,
            "realised_exclusion_rate_measured_gap_pairs":
                round(float((g >= thr108).sum()) / g.size, 6),
        }

    # inertness by waterfall line at W=108, for context only; NOT the adopted population
    tau1, gap, nb, na = bracketing(p, d_starts, d_ends, d_inst, u2slot, 108)
    meas = ~nb & ~na
    lines = ["analysis_population_201900", "has_s2_evidence_178165",
             "t0_not_contaminated_155131", "completing_record_not_postdated_152126",
             "first_s2_watch_clean_128099"]
    inert_by_line = {}
    for name, mk in zip(lines, masks):
        g = gap[mk & meas]
        n_na = int((mk & na).sum())
        n_nb = int((mk & nb).sum())
        row = {"n_pairs": int(mk.sum()), "n_measured_gap": int(g.size),
               "n_no_after": n_na, "n_no_before": n_nb, "by_percentile": {}}
        for q in (90.0, 95.0, 99.0, 99.9):
            t = int(math.ceil(float(np.percentile(g, q))))
            d = int((g >= t).sum())
            row["by_percentile"][str(q)] = {
                "threshold_days": t,
                "measured_gap_share_of_exclusions": round(d / (d + n_na + n_nb), 6),
            }
        inert_by_line[name] = row
        print(name, {k: v["measured_gap_share_of_exclusions"]
                     for k, v in row["by_percentile"].items()})

    out = {"instance": "a3", "api_calls": 0, "percentile": PCTL,
           "reference_population_n": int(ref.sum()),
           "global_sweep_end_epoch_s": sweep_end,
           "arms_refitted": arms,
           "counterfactual_single_frozen_threshold_from_W108": frozen_cf,
           "inertness_by_waterfall_line_W108_CONTEXT_ONLY": inert_by_line}
    with open(os.path.join(OUT, "arms_and_diagnostics.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote", os.path.join(OUT, "arms_and_diagnostics.json"))


if __name__ == "__main__":
    main()
