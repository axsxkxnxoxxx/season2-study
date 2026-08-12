"""Step 5: cost every candidate exclusion rule, in accounts and in pairs.

READ ONLY. Zero network calls. NOTHING HERE IS ADOPTED.

A gate proposal that names a rule without naming its cost is not reviewable. For
each candidate this prints: accounts removed, pairs removed, pairs surviving, and
the composition of what is removed - specifically the share of removed pairs that
carry any S2 evidence at all, next to the same share among survivors. That last
pair of numbers is the direction-of-bias evidence. It is not an outcome state: no
W and no liveness threshold exist yet, so no outcome can be computed and none is.
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
    m = pd.read_csv(P5 / "user_metrics.csv")
    bots = pd.read_csv(P5 / "bot_signals.csv")
    thr = np.load(P5 / "throughput.npz")
    pairs = pd.read_csv(P5 / "pair_contamination.csv")
    m3u = np.load(P5 / "mode3_flags.npz")["per_user_mode3"]

    m = m.merge(bots[["user_idx", "max_records_one_minute"]], on="user_idx")
    m["days_over_48"] = thr["days_over_48"]
    m["mode3_share"] = m3u / m.records.values
    burst_at = pd.to_datetime(m.bf_burst7d_inserted_at, errors="coerce")
    m["wave_burst"] = (burst_at >= pd.Timestamp("2026-06-20")) & (burst_at <= pd.Timestamp("2026-07-25"))

    pairs["clock_unusable"] = (
        (pairs.complete_rec_lag_days > BACKFILL_D)
        | (pairs.complete_rec_corrupt == 1)
        | (pairs.complete_rec_undated == 1)
        | (pairs.complete_rec_airdate == 1)
    )
    pairs["has_s2"] = pairs.s2_ev_n > 0
    n_pairs = len(pairs)
    n_acc = len(m)
    pair_acc = pairs.user_idx.values

    print(f"baseline: {n_acc:,} accounts, {n_pairs:,} pairs, "
          f"has-S2 share {pairs.has_s2.mean():.4f}\n")

    def report(name, acc_mask=None, pair_mask=None):
        if pair_mask is None:
            drop_acc = set(m.user_idx.values[acc_mask])
            pm = np.isin(pair_acc, list(drop_acc))
        else:
            pm = pair_mask.values if hasattr(pair_mask, "values") else pair_mask
            drop_acc = set(pairs.user_idx.values[pm])
        kept = ~pm
        row = {
            "rule": name,
            "accounts_removed": int(acc_mask.sum()) if acc_mask is not None else len(drop_acc),
            "pairs_removed": int(pm.sum()),
            "pairs_removed_pct": round(100 * float(pm.mean()), 2),
            "pairs_kept": int(kept.sum()),
            "hasS2_share_removed": round(float(pairs.has_s2[pm].mean()), 4) if pm.sum() else None,
            "hasS2_share_kept": round(float(pairs.has_s2[kept].mean()), 4),
            "clock_unusable_share_kept": round(float(pairs.clock_unusable[kept].mean()), 4),
        }
        return row

    rows = []
    # --- pair-level ---------------------------------------------------------
    rows.append(report("P1 pair: clock start backfilled >180d / corrupt / air-date",
                       pair_mask=pairs.clock_unusable))
    rows.append(report("P1a pair: clock start backfilled >90d variant",
                       pair_mask=(pairs.complete_rec_lag_days > 90)
                       | (pairs.complete_rec_corrupt == 1) | (pairs.complete_rec_airdate == 1)))
    rows.append(report("P1b pair: clock start backfilled >365d variant",
                       pair_mask=(pairs.complete_rec_lag_days > 365)
                       | (pairs.complete_rec_corrupt == 1) | (pairs.complete_rec_airdate == 1)))
    rows.append(report("P2 pair: P1 plus all S2 evidence air-date-stamped",
                       pair_mask=pairs.clock_unusable
                       | ((pairs.s2_ev_n > 0) & (pairs.s2_ev_airdate == pairs.s2_ev_n))))

    # --- account-level ------------------------------------------------------
    cands = [
        ("A1 acct: largest 7d backfill burst >= 50% of history", m.bf_burst7d_share >= 0.50),
        ("A2 acct: largest 7d backfill burst >= 25% of history", m.bf_burst7d_share >= 0.25),
        ("A3 acct: overall backfill share >= 50%", m.backfill_share >= 0.50),
        ("A4 acct: real-time evidence < 5% of records", m.realtime_share < 0.05),
        ("A5 acct: entire history written within 30 days", m.insert_span_days < 30),
        ("A6 acct: corrupt (pre-1990) share >= 50%", m.corrupt_share >= 0.50),
        ("A7 acct: TV Time wave burst >= 25% of history", m.wave_burst & (m.bf_burst7d_share >= 0.25)),
        ("A8 acct: air-date-stamped share >= 50%", m.mode3_share >= 0.50),
        ("A9 acct: >=30 claimed days over 48 distinct episodes", m.days_over_48 >= 30),
    ]
    for name, mask in cands:
        rows.append(report(name, acc_mask=mask.values))

    # --- combinations -------------------------------------------------------
    acct_strict = (m.bf_burst7d_share >= 0.50) | (m.realtime_share < 0.05) | \
                  (m.corrupt_share >= 0.50) | (m.mode3_share >= 0.50) | (m.insert_span_days < 30)
    rows.append(report("C1 acct union: A1 or A4 or A5 or A6 or A8", acc_mask=acct_strict.values))

    drop_acc = set(m.user_idx.values[acct_strict.values])
    pm_acct = np.isin(pair_acc, list(drop_acc))
    rows.append(report("C2 = C1 account union THEN P1 pair rule on survivors",
                       pair_mask=pd.Series(pm_acct | pairs.clock_unusable.values)))

    acct_wide = acct_strict | (m.bf_burst7d_share >= 0.25) | (m.backfill_share >= 0.50) | (m.days_over_48 >= 30)
    drop_acc_w = set(m.user_idx.values[acct_wide.values])
    pm_w = np.isin(pair_acc, list(drop_acc_w))
    rows.append(report("C3 = wide account union THEN P1 pair rule",
                       pair_mask=pd.Series(pm_w | pairs.clock_unusable.values)))

    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250, "display.max_colwidth", 60)
    print(df.to_string(index=False))
    df.to_csv(P5 / "rule_costs.csv", index=False)
    (P5 / "rule_costs.json").write_text(json.dumps(rows, indent=2))
    print("\nwrote", P5 / "rule_costs.csv")

    # overlap of the account union with the pair rule
    print(f"\naccount union C1 removes {len(drop_acc):,} accounts")
    print(f"  pairs removed by C1 alone: {pm_acct.sum():,}")
    print(f"  pairs with unusable clock start that C1 does NOT remove: "
          f"{int((pairs.clock_unusable.values & ~pm_acct).sum()):,}")
    print(f"  pairs C1 removes whose clock start was usable: "
          f"{int((~pairs.clock_unusable.values & pm_acct).sum()):,}")


if __name__ == "__main__":
    main()
