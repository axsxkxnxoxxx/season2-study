"""Step 5 revision: audit contamination against the BINDING TERM of T0.

READ ONLY. Zero network calls. NOTHING HERE IS ADOPTED.

Red Team B1. The first version of this step audited the first-pass S1 completion
instant and called it "clock start". That is not the clock start. Approved
Step 1 Sec 6, decision D1:

    T0 = max(S2_finale_air_date, S1_completion_date)

both as UTC calendar dates, the finale term taken from the Step 2 show frame.

Every contamination class here fabricates dates EARLIER than the truth. So
wherever a fabricated S1 completion date falls at or before the S2 finale air
date, max() discards it and T0 is the finale date - show metadata that no import
can touch. Excluding those pairs removes pairs whose clock start was never in
danger.

This file recomputes which term binds, and rescopes every rule to the pairs where
the contaminated S1 completion date is what max() actually selects.

It also computes, for C5, the pairs whose completing record is itself clean but
which reached the completion threshold through an ordering that includes
fabricated dates.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
BACKFILL_D = 180.0


def main():
    p = pd.read_csv(P5 / "pair_contamination.csv")
    f = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")

    p = p.merge(
        f[["show_trakt_id", "s2_finale_date"]], on="show_trakt_id", how="left", validate="m:1"
    )
    assert p.s2_finale_date.notna().all(), "frame must carry s2_finale_date for every frame show"

    # both terms as UTC calendar dates, per Step 1 Sec 6
    s1_date = pd.to_datetime(p.complete_rec_ts, unit="s", utc=True).dt.normalize().dt.tz_localize(None)
    fin_date = pd.to_datetime(p.s2_finale_date)
    p["s1_completion_date"] = s1_date
    p["s2_finale_dt"] = fin_date
    p["t0"] = np.maximum(s1_date.values, fin_date.values)

    p["binds"] = np.where(s1_date > fin_date, "s1",
                  np.where(s1_date < fin_date, "finale", "tie"))

    # contamination of the completing record
    p["comp_corrupt"] = p.complete_rec_corrupt == 1
    p["comp_airdate"] = p.complete_rec_airdate == 1
    p["comp_backfill"] = p.complete_rec_lag_days > BACKFILL_D
    p["comp_contaminated"] = p.comp_corrupt | p.comp_airdate | p.comp_backfill | (p.complete_rec_undated == 1)

    # OPERATIVE: contaminated AND that contaminated date is what max() selects
    p["t0_contaminated"] = p.comp_contaminated & (p.binds == "s1")

    out = {}
    out["pairs_total"] = int(len(p))
    out["old_removal_set_completion_contaminated"] = int(p.comp_contaminated.sum())

    sub = p[p.comp_contaminated]
    out["of_that_set"] = {
        "finale_binds_absorbed": int((sub.binds == "finale").sum()),
        "tie_absorbed": int((sub.binds == "tie").sum()),
        "absorbed_total": int((sub.binds != "s1").sum()),
        "s1_binds_still_operative": int((sub.binds == "s1").sum()),
    }
    out["of_that_set"]["absorbed_pct"] = round(
        100 * out["of_that_set"]["absorbed_total"] / len(sub), 2)

    # by contamination class
    cls = {}
    for name, mask in (("corrupt_pre1990", p.comp_corrupt),
                       ("airdate_stamped", p.comp_airdate),
                       ("backfilled_gt180d", p.comp_backfill)):
        s = p[mask]
        cls[name] = {
            "removed_by_old_rule": int(len(s)),
            "absorbed_by_max": int((s.binds != "s1").sum()),
            "absorbed_pct": round(100 * float((s.binds != "s1").mean()), 1),
            "still_binding": int((s.binds == "s1").sum()),
        }
    out["by_class"] = cls

    out["corrected_layer2"] = {
        "pairs_removed": int(p.t0_contaminated.sum()),
        "pairs_removed_pct": round(100 * float(p.t0_contaminated.mean()), 2),
        "pairs_retained": int((~p.t0_contaminated).sum()),
    }

    # overall binding split, all pairs
    out["binding_term_all_pairs"] = {
        k: int(v) for k, v in p.binds.value_counts().items()
    }

    p.to_csv(P5 / "pair_t0.csv", index=False)
    (P5 / "t0_binding.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
