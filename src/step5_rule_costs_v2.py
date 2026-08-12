"""Step 5 revision: corrected cost table, everything scoped to the binding term of T0.

READ ONLY. Zero network calls. NOTHING HERE IS ADOPTED.

Supersedes src/step5_rule_costs.py, which costed against the S1 completion
instant alone and so overstated every pair-level figure by roughly 3x (Red Team
B1). That file is retained unmodified so the two are diffable.

Adds, per Red Team:
  B2  P2 restored and costed; S2-evidence cross-tab against Layer 2 survivors
  C3  post-dated records costed rather than silently tagged clean
  C5  the "any S1 completion evidence contaminated" rule costed
  R1  W estimation sample sized under the Human Lead's ruling 1
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
BACKFILL_D = 180.0


def main():
    p = pd.read_csv(P5 / "pair_t0.csv")
    m = pd.read_csv(P5 / "user_metrics.csv")
    thr = np.load(P5 / "throughput.npz")
    day = pd.read_csv(P5 / "pair_completion_day_load.csv")
    m3u = np.load(P5 / "mode3_flags.npz")["per_user_mode3"]
    p = p.merge(day, on=["user_idx", "show_trakt_id"], how="left", validate="1:1")

    n = len(p)
    p["has_s2"] = p.s2_ev_n > 0
    s1_binds = p.binds == "s1"

    # ---- record-level classes on the completing record -----------------------
    comp_bad = p.comp_contaminated.values
    comp_postdated = (p.complete_rec_lag_days < -30).values

    # C5: completing record itself clean, but the ORDERING that made it the
    # completing record used fabricated dates. Removing those pushes true
    # completion LATER, so the computed S1 term is too early - and unlike the
    # Layer 2 case, max() does NOT absorb that, because a later true completion
    # can overtake the finale. So this is not scoped to s1_binds.
    earlier_bad = ((p.s1_ev_backfilled.values - p.comp_backfill.values.astype(int)) > 0) | \
                  ((p.s1_ev_corrupt.values - p.comp_corrupt.values.astype(int)) > 0) | \
                  ((p.s1_ev_airdate.values - p.comp_airdate.values.astype(int)) > 0)
    c5_only = earlier_bad & ~comp_bad

    # ---- account-level masks -------------------------------------------------
    m = m.set_index("user_idx").sort_index()
    m["mode3_share"] = m3u / m.records.values
    m["days_over_48_surv"] = thr["days_over_48_survivor"]
    burst_at = pd.to_datetime(m.bf_burst7d_inserted_at, errors="coerce")
    m["wave"] = (burst_at >= pd.Timestamp("2026-06-20")) & (burst_at <= pd.Timestamp("2026-07-25"))
    acct = {
        "A1 largest 7d backfill burst >= 50% of history": m.bf_burst7d_share >= 0.50,
        "A2 largest 7d backfill burst >= 25% of history": m.bf_burst7d_share >= 0.25,
        "A3 overall backfill share >= 50%": m.backfill_share >= 0.50,
        "A4 real-time evidence < 5% of records": m.realtime_share < 0.05,
        "A5 entire history written within 30 days": m.insert_span_days < 30,
        "A6 corrupt share >= 50%": m.corrupt_share >= 0.50,
        "A7 TV Time wave burst >= 25% of history": m.wave & (m.bf_burst7d_share >= 0.25),
        "A8 air-date-stamped share >= 50%": m.mode3_share >= 0.50,
        "A9 >=30 survivor days over 48 distinct episodes": m.days_over_48_surv >= 30,
    }

    rows = []

    def rec(name, drop, accounts=None):
        drop = np.asarray(drop)
        keep = ~drop
        rows.append({
            "rule": name,
            "accounts_removed": accounts if accounts is not None else "",
            "pairs_removed": int(drop.sum()),
            "pct_removed": round(100 * float(drop.mean()), 2),
            "pairs_kept": int(keep.sum()),
            # residual exposure among survivors, on the CORRECTED definition
            "kept_T0_contaminated_pct": round(100 * float(p.t0_contaminated.values[keep].mean()), 2),
            "hasS2_removed": round(float(p.has_s2.values[drop].mean()), 4) if drop.sum() else None,
            "hasS2_kept": round(float(p.has_s2.values[keep].mean()), 4),
        })

    rec("BASELINE no exclusion", np.zeros(n, bool))
    rec("L2 CORRECTED  contaminated S1 date AND S1 term binds", p.t0_contaminated.values)
    rec("L2-old  contaminated completion record, any binding (SUPERSEDED)", comp_bad)
    rec("L2 at 90d variant",
        ((p.complete_rec_lag_days > 90) | p.comp_corrupt | p.comp_airdate).values & s1_binds.values)
    rec("L2 at 365d variant",
        ((p.complete_rec_lag_days > 365) | p.comp_corrupt | p.comp_airdate).values & s1_binds.values)
    rec("C5 add: any S1 completion evidence contaminated (not just completing record)",
        p.t0_contaminated.values | c5_only)
    rec("C3 add: completing record post-dated by >30d",
        p.t0_contaminated.values | (comp_postdated & s1_binds.values))
    rec("P2 add: all S2 evidence air-date-stamped",
        p.t0_contaminated.values | (p.has_s2.values & (p.s2_ev_airdate.values == p.s2_ev_n.values)))
    rec("P3 add: all S2 evidence backfilled",
        p.t0_contaminated.values | (p.has_s2.values & (p.s2_ev_backfilled.values == p.s2_ev_n.values)))

    for name, mask in acct.items():
        drop_idx = set(m.index[mask.values].tolist())
        pm = p.user_idx.isin(drop_idx).values
        rec("ACCT " + name, pm, accounts=int(mask.sum()))

    strict = (m.bf_burst7d_share >= 0.50) | (m.realtime_share < 0.05) | \
             (m.corrupt_share >= 0.50) | (m.mode3_share >= 0.50) | (m.insert_span_days < 30)
    strict_idx = set(m.index[strict.values].tolist())
    pm_strict = p.user_idx.isin(strict_idx).values
    rec("L3 account union (A1,A4,A5,A6,A8)", pm_strict, accounts=int(strict.sum()))
    rec("L2 + L3", p.t0_contaminated.values | pm_strict, accounts=int(strict.sum()))

    l4 = m.days_over_48_surv >= 30
    l4_idx = set(m.index[l4.values].tolist())
    rec("L2 + L3 + L4", p.t0_contaminated.values | pm_strict | p.user_idx.isin(l4_idx).values,
        accounts=int((strict | l4).sum()))

    # bulk-mark options, on the corrected base
    for th in (96, 48, 24):
        bm = (p.completion_day_eps_survivor.values > th) & s1_binds.values
        rec(f"L5 add: completion day carries >{th} distinct episodes (S1 term binding)",
            p.t0_contaminated.values | bm)

    df = pd.DataFrame(rows)
    pd.set_option("display.width", 260, "display.max_colwidth", 68)
    print(df.to_string(index=False))
    df.to_csv(P5 / "rule_costs_v2.csv", index=False)

    # ---- B2: what survives into Step 6 ---------------------------------------
    keep = ~p.t0_contaminated.values
    surv = p[keep]
    s2 = surv[surv.has_s2]
    b2 = {
        "layer2_survivors": int(keep.sum()),
        "survivors_with_any_s2_evidence": int(len(s2)),
        "survivors_s2_evidence_all_backfilled": int((s2.s2_ev_backfilled == s2.s2_ev_n).sum()),
        "survivors_s2_evidence_all_airdate": int((s2.s2_ev_airdate == s2.s2_ev_n).sum()),
        "survivors_s2_evidence_any_backfilled": int((s2.s2_ev_backfilled > 0).sum()),
        "survivors_first_s2_watch_backfilled": int((s2.first_s2_lag_days > BACKFILL_D).sum()),
        "survivors_first_s2_watch_airdate": int((s2.first_s2_airdate == 1).sum()),
        "survivors_first_s2_watch_corrupt": int((s2.first_s2_corrupt == 1).sum()),
    }
    fs2_bad = ((s2.first_s2_lag_days > BACKFILL_D) | (s2.first_s2_airdate == 1)
               | (s2.first_s2_corrupt == 1))
    b2["survivors_first_s2_watch_contaminated_any"] = int(fs2_bad.sum())
    b2["survivors_first_s2_watch_contaminated_pct"] = round(100 * float(fs2_bad.mean()), 2)
    b2["W_estimation_sample_clean_T0_and_clean_first_s2"] = int((~fs2_bad).sum())
    print("\nB2 / Ruling 1 - what Step 6 would actually read:")
    print(json.dumps(b2, indent=2))
    (P5 / "step6_exposure.json").write_text(json.dumps(b2, indent=2))

    # C5 magnitude
    print(f"\nC5: completing record clean but earlier S1 evidence contaminated: {int(c5_only.sum()):,}")
    print(f"    of which the S1 term currently binds: {int((c5_only & s1_binds.values).sum()):,}")
    print(f"\nC3: completing record post-dated >30d: {int(comp_postdated.sum()):,}"
          f"   with S1 term binding: {int((comp_postdated & s1_binds.values).sum()):,}")


if __name__ == "__main__":
    main()
