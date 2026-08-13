"""Step 7 ALT-BROAD rerun (instance b, namespace bb_b) -- stage 2.

(1) THE WATERFALL, line 6 reported OUTCOME-CONDITIONAL (0046 Sec 5, carried into
    task-sheet Step 7). Positions 1-2 belong to Step 8 and are not rebuilt here;
    positions 3-6 are measured; position 7 is an annotation removing no rows.
    Monotone decrease is reported STRICT or NON-STRICT per line and per
    population.

    Under ALT-BROAD line 6 is outcome-conditional in a STRONGER sense than under
    ALT: conjunct (b) is now "NOT Continued", and Continued is read at tau2, not
    tau1. So position 6 depends on an annotation computed at BOTH instants.

(2) AN ACCOUNT-CLUSTERED BOOTSTRAP of the three live shares, so the width of the
    partial-identification bounds can be set beside the sampling width. Clusters
    are ACCOUNTS (liveness evidence is account-wide), pairs are the unit.
    Resampling is over the position-5 population; the rule is re-applied inside
    each replicate, which is what makes the exclusion count itself random.

ZERO network calls. Reads only.

Out: processed/step7/bb_b/waterfall.json, processed/step7/bb_b/bootstrap.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5, P2 = ROOT / "processed" / "step5", ROOT / "processed" / "step2"
SRC = ROOT / "processed" / "step7" / "alt2_b"
OUT = ROOT / "processed" / "step7" / "bb_b"
W, H = 108, 91
N_BOOT, SEED = 2000, 20260814


def main() -> None:
    t = time.time()
    pz = np.load(SRC / "pairs.npz")
    oz = np.load(SRC / "outcomes.npz")
    rule = json.load(open(OUT / "rule.json"))

    # ---------------------------------------------------------------- waterfall
    frame = pd.read_csv(P2 / "frame.csv", usecols=["show_trakt_id", "s2_L"])
    n_pairs_s1 = int(len(pd.read_csv(P5 / "pair_revision5.csv", usecols=["user_idx"])))

    wf: dict = {
        "instance": "data-scientist-b", "namespace": "bb_b", "stage": 2,
        "api_calls": 0, "adopts": "nothing", "W": W, "H": H,
        "shows_in_frame": int(len(frame)),
        "shows_with_L2_eq_1_in_frame": int((frame.s2_L.values == 1).sum()),
        "waterfall": {},
    }
    for pop in ("APPLY", "DERIV"):
        a = rule["by_population"][pop]["108"]
        n5 = a["n_before_liveness"]
        ex = a["excluded_pairs"]
        n6 = n5 - ex
        pre_censor = 201_900 if pop == "APPLY" else 152_126
        lines = [
            {"position": "1-2", "name": "Step 2 frame, then L2 = 1 exclusion", "rows_out": None,
             "note": "owned by Step 8, not rebuilt here. No show in this frame has L2 = 1, "
                     "so position 2 removes nothing."},
            {"position": 3, "name": "S1 completion rule", "rows_out": n_pairs_s1,
             "note": "row count of the Step 5 pair table (Step 2 frame x Step 1 Sec 4)"},
            {"position": 4, "name": "contamination exclusion (Step 5)", "rows_out": pre_censor,
             "note": ("Step 5 line 1 for APPLY; line 4 for DERIV. DERIV additionally requires "
                      "S2 evidence and clean first-S2 timing and is NOT a Step 8 position -- "
                      "it exists to make the Step 6/7 derivation sample clean.")},
            {"position": 5, "name": f"right-censoring D10, re-derived at W = {W}",
             "rows_out": n5,
             "note": "[T0] + (max(W, 91) + H) x 24h <= tau_pull. Contains W (0047 Sec 5)."},
            {"position": 6, "name": "liveness (ALT-BROAD, decisions/0048)", "rows_out": n6,
             "removed": ex,
             "removed_never_started": a["excluded_never_started"],
             "removed_started_and_left": a["excluded_started_and_left"],
             "OUTCOME_CONDITIONAL": True,
             "note": ("line 6's removal count is conditional on the position-7 outcome "
                      "annotation, because conjunct (b) is 'NOT Continued'. Under ALT-BROAD "
                      "that conjunct is read at tau2, not tau1, so line 6 depends on an "
                      "annotation computed at BOTH instants -- a stronger conditioning than "
                      "under the superseded ALT, whose conjunct (b) was |A| = 0 at tau1. "
                      "Permitted: both are row-local predicates on the position-5 output and "
                      "commute exactly; 0029's ordering rationale is per-filter sample size, "
                      "which cannot reach position 7 because outcome assignment removes no rows.")},
            {"position": 7, "name": "outcome assignment at tau1 and tau2", "rows_out": n6,
             "removed": 0, "note": "an annotation, not a filter; contributes no waterfall line"},
        ]
        counts = [n_pairs_s1, pre_censor, n5, n6]
        wf["waterfall"][pop] = lines
        wf["waterfall"][pop + "_monotone"] = {
            "non_strict_holds_all_lines": all(b <= x for x, b in zip(counts, counts[1:])),
            "strict_holds_all_lines": all(b < x for x, b in zip(counts, counts[1:])),
            "line6_removed": ex,
            "line6_decrease": "STRICT" if ex > 0 else "NON-STRICT",
            "statement": (f"on {pop}, monotone decrease at line 6 holds STRICTLY: {ex:,} rows "
                          f"removed ({a['excluded_never_started']} never-started + "
                          f"{a['excluded_started_and_left']} started-and-left)"
                          if ex > 0 else
                          f"on {pop}, monotone decrease at line 6 holds only NON-STRICTLY: "
                          f"the exclusion set is empty"),
        }
        wf["waterfall"][pop + "_final_states"] = a["under_rule"]

    wf["monotone_invariant_for_step8"] = {
        "coded_as": ">=",
        "reason_under_ALT": ("0047 Sec 6: decrease was strict at line 6 on APPLY and only "
                             "NON-STRICT on DERIV, where ALT's exclusion set was empty."),
        "reason_under_ALT_BROAD": ("decrease is STRICT at line 6 on BOTH populations -- 703 on "
                                   "APPLY and 99 on DERIV. The empty-set case that forced '>=' "
                                   "no longer arises at any tested arm. '>=' remains the safe "
                                   "coding, but the stated reason for it is now false."),
        "task_sheet_lines_now_stale": [
            "Step 7 bullet: 'The monotone-decrease invariant holds only NON-STRICTLY where the "
            "exclusion set is empty, which it is on DERIV.' -- it is 99 on DERIV under ALT-BROAD.",
            "Step 8 bullet: 'Decrease is strict at line 6 on the application population and only "
            "NON-STRICT on the derivation population, where the liveness exclusion set is empty.'",
        ],
    }
    (OUT / "waterfall.json").write_text(json.dumps(wf, indent=2))
    print(f"waterfall written  ({time.time() - t:.1f}s)", flush=True)

    # ---------------------------------------------------------------- bootstrap
    d10 = pz[f"d10_W{W}"]
    in4 = pz["in_line4"]
    boot: dict = {"instance": "data-scientist-b", "namespace": "bb_b", "stage": 2,
                  "api_calls": 0, "adopts": "nothing",
                  "method": ("nonparametric bootstrap, clusters = ACCOUNTS, unit = pair. "
                             "Accounts resampled with replacement from the accounts present in "
                             "the position-5 population; the liveness rule is RE-APPLIED inside "
                             "each replicate, so the exclusion count is itself random."),
                  "replicates": N_BOOT, "seed": SEED, "W": W, "by_population": {}}
    rng = np.random.default_rng(SEED)
    for pop in ("DERIV", "APPLY"):
        base = (d10 & in4) if pop == "DERIV" else d10
        u = pz["user_idx"][base]
        cont = oz[f"cont_W{W}"][base].astype(bool)
        sal = oz[f"sal_W{W}"][base].astype(bool)
        ns = ~oz[f"started_W{W}"][base]
        notlive = pz[f"no_after_W{W}"][base] & ~cont
        live = ~notlive

        accounts, inv = np.unique(u, return_inverse=True)
        na = len(accounts)
        # per-account tallies of the four quantities the shares need
        tal = np.zeros((na, 4), dtype=np.int64)
        np.add.at(tal[:, 0], inv, live)
        np.add.at(tal[:, 1], inv, ns & live)
        np.add.at(tal[:, 2], inv, cont & live)
        np.add.at(tal[:, 3], inv, sal & live)
        ex_by_acct = np.zeros(na, dtype=np.int64)
        np.add.at(ex_by_acct, inv, notlive)

        draws = rng.integers(0, na, size=(N_BOOT, na))
        s = tal[draws].sum(axis=1)                       # (N_BOOT, 4)
        exb = ex_by_acct[draws].sum(axis=1)
        pct = 100.0 * s[:, 1:] / s[:, [0]]
        q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
        boot["by_population"][pop] = {
            "accounts_resampled": int(na),
            "point_live_shares_pct": {
                "never_started": float(100.0 * tal[:, 1].sum() / tal[:, 0].sum()),
                "continued": float(100.0 * tal[:, 2].sum() / tal[:, 0].sum()),
                "started_and_left": float(100.0 * tal[:, 3].sum() / tal[:, 0].sum())},
            "ci95_live_shares_pct": {
                "never_started": q(pct[:, 0]), "continued": q(pct[:, 1]),
                "started_and_left": q(pct[:, 2])},
            "ci95_width_pp": {
                "never_started": q(pct[:, 0])[1] - q(pct[:, 0])[0],
                "continued": q(pct[:, 1])[1] - q(pct[:, 1])[0],
                "started_and_left": q(pct[:, 2])[1] - q(pct[:, 2])[0]},
            "exclusion_count_ci95": q(exb),
            "exclusion_count_point": int(notlive.sum()),
        }
    # bound width vs sampling width, the comparison Step 9 needs
    for pop in ("DERIV", "APPLY"):
        r = rule["by_population"][pop]["108"]
        b = boot["by_population"][pop]
        b["bound_width_vs_sampling_width_pp"] = {
            "never_started": {
                "bound_width": r["never_started_bound"]["width_pp"],
                "ci95_width": b["ci95_width_pp"]["never_started"],
                "ratio": (r["never_started_bound"]["width_pp"] /
                          b["ci95_width_pp"]["never_started"])},
            "started_and_left_over_SL_exclusions": {
                "bound_width": r["started_and_left_bound"]["width_over_SL_exclusions_pp"],
                "ci95_width": b["ci95_width_pp"]["started_and_left"],
                "ratio": (r["started_and_left_bound"]["width_over_SL_exclusions_pp"] /
                          b["ci95_width_pp"]["started_and_left"])},
        }
    (OUT / "bootstrap.json").write_text(json.dumps(boot, indent=2))
    print(json.dumps(boot["by_population"]["APPLY"], indent=2))
    print(f"({time.time() - t:.1f}s)")


if __name__ == "__main__":
    main()
