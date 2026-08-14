"""Step 8, namespace `a`. STAGE 4 of 5 — the per-arm required counts.

GATE. Adopts nothing. Zero API calls.

Three Step 8 outputs are per-`W`-arm, not per adopted value:
  * retained-pair counts PER AIR PERIOD after right-censoring (decisions/0033), censoring the
    POSITION-4 output as the mandated filter order requires (0070 ruling 8);
  * D3' -- the resumption-rate report -- each arm reporting its own cleared count and share
    (decisions/0034), because the clearance contains W;
  * the liveness exclusion count, whose set is a pure function of W (decisions/0044).
D10 is RE-DERIVED at each arm and never frozen (decisions/0047): right-censoring contains W.
H is held constant at 91 across every arm (D10, Step 13), or D3' and D8 stop being comparable.

The arm grid is the operative series quoted at task-sheet Steps 7 and 13:
38 / 46 / 77 / 91 / 107 / 108 / 150 / 213. Step 8 itself names no grid; the source is named here
so the choice is visible rather than silent.

Output: processed/step8/a/arms.json
"""
import json
import os

import numpy as np
import pandas as pd

import step8_a_lib as lib

ROOT = "/Users/alyanashantel/Documents/season2-study"
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step8/a")

ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
H = 91
DAY = 86400


def main():
    scan = np.load(os.path.join(OUT, "scan.npz"))
    positions = np.load(os.path.join(OUT, "positions.npz"))
    frame = pd.read_csv(os.path.join(P2, "frame.csv"))
    a = lib.Arms(scan, positions, frame, H=H)
    air = frame.set_index("show_trakt_id").air_period.reindex(a.pair_show).to_numpy()
    periods = ["pre-2020", "2020-2022", "2023-2025"]

    pos4, pos4d = a.pos4, a.pos4_deriv
    base_air = {p: int(((air == p) & pos4).sum()) for p in periods}
    base_air_d = {p: int(((air == p) & pos4d).sum()) for p in periods}

    out = {"step": 8, "instance": "a", "stage": 4, "api_calls": 0, "H_days": H,
           "arm_grid": ARMS,
           "arm_grid_source": "the operative series quoted at task-sheet Step 7 (the ALT-BROAD "
                              "per-arm exclusion series) and Step 13 (decisions/0044). Step 8 "
                              "names no grid of its own.",
           "censoring_denominator": {
               "APPLY_position_4_output": int(pos4.sum()),
               "DERIV_position_4_output": int(pos4d.sum()),
               "note": "the mandated filter order censors the POSITION-4 output; 0033's "
                       "97.6/98.0/97.5/96.0 were computed on the position-3 output and are "
                       "superseded by 0070 ruling 8",
               "APPLY_position_4_by_air_period": base_air,
               "DERIV_position_4_by_air_period": base_air_d},
           "arms": []}

    for W in ARMS:
        r = a.run(W)
        pos5, pos5d = r["pos5"], r["pos5_deriv"]
        pos6 = pos5 & ~r["not_live"]
        pos6d = pos5d & ~r["not_live"]

        # D3': cleared subpopulation of Started-and-left, and completion within [tau2, tau2+H)
        cleared_ok = (a.t0 + (W + 2 * H) * DAY) <= lib.TAU_PULL
        k3 = a.count_before(r["tau2"] + H * DAY)
        m3 = a.maxnum_before(k3)
        completes = (m3 == a.F2) & (k3 >= a.need2)

        d3 = {}
        for name, sl, tot in (("APPLY", pos6 & r["left"], int((pos6 & r["left"]).sum())),
                              ("DERIV", pos6d & r["left"], int((pos6d & r["left"]).sum()))):
            cl = sl & cleared_ok
            n_cl = int(cl.sum())
            d3[name] = {
                "population": name + ", position-7 output at this arm (post-liveness)",
                "all_started_and_left": tot,
                "cleared_count": n_cl,
                "cleared_share_of_all_started_and_left": round(n_cl / tot, 6) if tot else None,
                "share_completing_in_tau2_to_tau2_plus_H": round(
                    float((cl & completes).sum() / n_cl), 6) if n_cl else None,
                "count_completing_in_tau2_to_tau2_plus_H": int((cl & completes).sum()),
            }

        entry = {
            "W_days": W,
            "position_5_APPLY": int(pos5.sum()),
            "position_5_DERIV": int(pos5d.sum()),
            "right_censoring_two_lines_APPLY": {
                "removed_by_max_W_91_term": int((pos4 & ~r["keep_term1"]).sum()),
                "removed_incrementally_by_the_plus_H_term": int(
                    (pos4 & r["keep_term1"] & ~r["keep_d10"]).sum()),
            },
            "retained_share_of_position_4_APPLY": round(float(pos5.sum() / pos4.sum()), 6),
            "retained_per_air_period_APPLY": {
                p: {"retained": int(((air == p) & pos5).sum()),
                    "entering": base_air[p],
                    "retained_share": round(float(((air == p) & pos5).sum() / base_air[p]), 6),
                    "lost_share": round(1 - float(((air == p) & pos5).sum() / base_air[p]), 6)}
                for p in periods},
            "retained_per_air_period_DERIV": {
                p: {"retained": int(((air == p) & pos5d).sum()),
                    "entering": base_air_d[p],
                    "retained_share": round(float(((air == p) & pos5d).sum() / base_air_d[p]), 6)}
                for p in periods},
            "liveness_exclusions_APPLY": {
                "total": int((pos5 & r["not_live"]).sum()),
                "never_started_component": int((pos5 & r["not_live"] & r["never"]).sum()),
                "started_and_left_component": int((pos5 & r["not_live"] & r["left"]).sum()),
                "accounts": int(np.unique(a.pair_user[pos5 & r["not_live"]]).size)},
            "liveness_exclusions_DERIV": {
                "total": int((pos5d & r["not_live"]).sum()),
                "never_started_component": int((pos5d & r["not_live"] & r["never"]).sum()),
                "started_and_left_component": int((pos5d & r["not_live"] & r["left"]).sum()),
                "accounts": int(np.unique(a.pair_user[pos5d & r["not_live"]]).size)},
            "position_7_APPLY": {"never_started": int((pos6 & r["never"]).sum()),
                                 "started_and_left": int((pos6 & r["left"]).sum()),
                                 "continued": int((pos6 & r["continued"]).sum()),
                                 "total": int(pos6.sum())},
            "position_7_DERIV": {"never_started": int((pos6d & r["never"]).sum()),
                                 "started_and_left": int((pos6d & r["left"]).sum()),
                                 "continued": int((pos6d & r["continued"]).sum()),
                                 "total": int(pos6d.sum())},
            "D3_prime": d3,
        }
        out["arms"].append(entry)
        print(f"W={W:>3}  pos5={entry['position_5_APPLY']:>7}  "
              f"liveness={entry['liveness_exclusions_APPLY']['total']:>4} "
              f"(S&L {entry['liveness_exclusions_APPLY']['started_and_left_component']:>3})  "
              f"kept={entry['retained_share_of_position_4_APPLY']:.4f}  "
              f"2023-25 kept={entry['retained_per_air_period_APPLY']['2023-2025']['retained_share']:.4f}",
              flush=True)

    with open(os.path.join(OUT, "arms.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({"arms": [{k: v for k, v in e.items()
                                if k in ("W_days", "liveness_exclusions_APPLY", "D3_prime")}
                               for e in out["arms"]]}, indent=2)[:4000])


if __name__ == "__main__":
    main()
