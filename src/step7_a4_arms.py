"""Step 7 rerun (decisions/0040), instance A4 — Step 13's per-arm refit.

decisions/0038 SS6: the threshold IS a function of W, so Step 13 must REFIT it per arm and
report both the refitted threshold and the realised exclusion rate for each. decisions/0027
sets the arms: the span 46 to 107, plus 150 and 213; 38 is included because 0027's own union
range starts there, and 60/75/91/120/180 are added so the response is traced rather than
interpolated between endpoints.

Every arm re-runs D10 at its own W, because D10 is `[[T0]] + (max(W,91)+H)*24h <= tau_pull`
and decisions/0040 requires derivation on the POST-D10 population. H is held constant at 91
across every arm (D10; task-sheet Step 13), or D3' and D8 are not comparable between arms.

Zero API calls.
"""
import json
import math
import os
import time

import numpy as np
import pandas as pd

from step7_a4_bracketing import (
    SEC_PER_DAY, H_DAYS, PCTL, PUBLISHED_WATERFALL, FROZEN_LINE, TAU_PULL,
    build_waterfall, t0_floor_epoch, d10_mask, bracketing,
)

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step7/a4")

ARMS = [38, 46, 60, 75, 91, 107, 108, 120, 150, 180, 213]
ADOPTED_W = 108
B_ARM = 1000
SEED = 20260813


def clustered_ci(val, u, b=B_ARM, seed=SEED):
    """Account-clustered bootstrap CI of the 99th percentile, vectorised."""
    order = np.argsort(u, kind="stable")
    v_s = val[order]
    u_s = u[order]
    starts = np.flatnonzero(np.r_[True, u_s[1:] != u_s[:-1]])
    counts = np.diff(np.r_[starts, u_s.size])
    n_acc = starts.size
    rng = np.random.default_rng(seed)
    out = np.empty(b)
    for i in range(b):
        samp = rng.integers(0, n_acc, size=n_acc)
        c = counts[samp]
        tot = int(c.sum())
        idx = np.repeat(starts[samp] - np.r_[0, np.cumsum(c)[:-1]], c) + np.arange(tot)
        with np.errstate(invalid="ignore"):
            out[i] = np.percentile(v_s[idx], PCTL)
    ok = np.isfinite(out)
    lo, hi = np.percentile(out[ok], [2.5, 97.5])
    return {
        "replicates": b,
        "infinite_replicates": int((~ok).sum()),
        "ci95_raw_days": [float(lo), float(hi)],
        "ci95_ceil_days": [int(math.ceil(lo)), int(math.ceil(hi))],
    }


def main():
    t0w = time.time()
    di = np.load(os.path.join(OUT, "distinct_instants.npz"))
    uids, d_starts, d_ends, d_inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)
    masks = build_waterfall(p)
    assert [int(m.sum()) for m in masks] == PUBLISHED_WATERFALL
    ref152 = masks[FROZEN_LINE]
    t0f = t0_floor_epoch(p)
    uidx = p.user_idx.values

    arms = {}
    keep = {}          # per-arm sorted finite gaps + class counts, for the counterfactual
    for w in ARMS:
        keep10 = d10_mask(t0f, w)
        ref = ref152 & keep10
        n_pairs = int(ref.sum())
        tau1, gap, no_before, no_after = bracketing(
            t0f, uidx, d_starts, d_ends, d_inst, u2slot, w)
        measured = ~no_before & ~no_after

        m_meas = ref & measured
        g = gap[m_meas]
        n_meas = int(m_meas.sum())
        n_open = int((ref & no_after).sum())
        n_nb = int((ref & no_before).sum())
        assert n_meas + n_open + n_nb == n_pairs

        ext = np.concatenate([g, np.full(n_open, np.inf)])
        raw_ext = float(np.percentile(ext, PCTL))
        thr_ext = int(math.ceil(raw_ext)) if np.isfinite(raw_ext) else None
        raw_m = float(np.percentile(g, PCTL))
        thr_m = int(math.ceil(raw_m))

        rec = {
            "W_days": w,
            "H_days": H_DAYS,
            "d10_horizon_days": max(w, 91) + H_DAYS,
            "d10_latest_admissible_T0_utc": str(np.datetime64(
                int(TAU_PULL - (max(w, 91) + H_DAYS) * SEC_PER_DAY), "s")),
            "population_152126_after_D10": n_pairs,
            "d10_removed_from_152126": 152126 - n_pairs,
            "d10_retained_share": round(n_pairs / 152126, 6),
            "measured_gap_pairs": n_meas,
            "open_ended_pairs": n_open,
            "open_ended_share_of_extended_set": round(n_open / (n_meas + n_open), 6),
            "no_instant_at_or_before_tau1_LIVE_per_0021": n_nb,
            "EXTENDED_reference": {
                "p99_raw_days": raw_ext if np.isfinite(raw_ext) else None,
                "p99_is_finite": bool(np.isfinite(raw_ext)),
                "threshold_days": thr_ext,
            },
            "MEASURED_ONLY_reference": {
                "p99_raw_days": raw_m,
                "threshold_days": thr_m,
            },
        }

        for name, thr in (("EXTENDED_reference", thr_ext),
                          ("MEASURED_ONLY_reference", thr_m)):
            if thr is None:
                rec[name]["applied"] = None
                continue
            dead_m = int((g >= thr).sum())
            dead = dead_m + n_open
            rec[name]["applied"] = {
                "live": n_pairs - dead,
                "not_live_total": dead,
                "not_live_measured_gap": dead_m,
                "not_live_open_ended": n_open,
                "realised_rate_vs_measured_gap_pairs": round(dead_m / n_meas, 6),
                "realised_rate_vs_extended_set": round(dead / (n_meas + n_open), 6),
                "realised_rate_vs_post_D10_population": round(dead / n_pairs, 6),
                "live_share_of_post_D10_population": round((n_pairs - dead) / n_pairs, 6),
            }

        rec["EXTENDED_reference"]["clustered_ci"] = clustered_ci(ext, np.concatenate(
            [uidx[m_meas], uidx[ref & no_after]]))
        rec["MEASURED_ONLY_reference"]["clustered_ci"] = clustered_ci(g, uidx[m_meas])

        keep[w] = {"g": np.sort(g), "n_meas": n_meas, "n_open": n_open, "n_pairs": n_pairs}
        arms[str(w)] = rec
        print(f"W={w:>3}  D10-> {n_pairs:>6}  meas {n_meas:>6}  open {n_open:>5}  "
              f"noPre {n_nb:>6}  thr_ext {thr_ext}  thr_meas {thr_m}  "
              f"[{time.time() - t0w:.1f}s]", flush=True)

        with open(os.path.join(OUT, "arms.json"), "w") as f:
            json.dump({"instance": "a4", "api_calls": 0, "arms_so_far": arms}, f, indent=2)

    # counterfactual: freeze the adopted-arm threshold and carry it to every arm
    cf = {}
    for name in ("EXTENDED_reference", "MEASURED_ONLY_reference"):
        frozen = arms[str(ADOPTED_W)][name]["threshold_days"]
        cf[name] = {"frozen_threshold_days": frozen, "by_arm": {}}
        for w in ARMS:
            a = arms[str(w)]
            k = keep[w]
            dead_m = int((k["g"] >= frozen).sum())
            dead = dead_m + k["n_open"]
            cf[name]["by_arm"][str(w)] = {
                "refitted_threshold_days": a[name]["threshold_days"],
                "refitted_realised_rate_vs_extended_set":
                    a[name]["applied"]["realised_rate_vs_extended_set"]
                    if a[name]["applied"] else None,
                "frozen_threshold_not_live_total": dead,
                "frozen_threshold_realised_rate_vs_extended_set":
                    round(dead / (k["n_meas"] + k["n_open"]), 6),
                "frozen_threshold_realised_rate_vs_measured_gap_pairs":
                    round(dead_m / k["n_meas"], 6),
            }

    out = {
        "step": 7,
        "instance": "a4",
        "api_calls": 0,
        "spec": "decisions/0038 SS6 (refit per arm), 0027 (arm list), 0040 (derive after D10)",
        "H_held_constant_days": H_DAYS,
        "adopted_W": ADOPTED_W,
        "arms": arms,
        "W_coupling": {
            "EXTENDED_reference_threshold_span": [
                arms[str(min(ARMS))]["EXTENDED_reference"]["threshold_days"],
                arms[str(max(ARMS))]["EXTENDED_reference"]["threshold_days"]],
            "MEASURED_ONLY_reference_threshold_span": [
                arms[str(min(ARMS))]["MEASURED_ONLY_reference"]["threshold_days"],
                arms[str(max(ARMS))]["MEASURED_ONLY_reference"]["threshold_days"]],
            "note": "the threshold is a function of W and the two are not independent "
                    "robustness axes (decisions/0038 SS6)",
        },
        "frozen_threshold_counterfactual": cf,
        "runtime_seconds": round(time.time() - t0w, 1),
    }
    with open(os.path.join(OUT, "arms.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", os.path.join(OUT, "arms.json"))


if __name__ == "__main__":
    main()
