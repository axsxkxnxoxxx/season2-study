"""Step 5: claimed-viewing-day throughput. Commits a computation that was
previously run ad hoc and was therefore unauditable (Red Team B3).

READ ONLY. Zero network calls.

Writes:
  processed/step5/throughput.npz              per-account day-load measures
  processed/step5/pair_completion_day_load.csv  distinct episodes on each pair's
                                                claimed S1-completion day

TWO VARIANTS, AND WHY THE DISTINCTION MATTERS

  ALL      every dated episode record, backfill included
  SURVIVOR only records that survive the record-level contamination tests
           (not corrupt, not undated, lag <= 180 d, not air-date-stamped)

They answer different questions and must not be swapped for one another.

  - The BOT question asks whether an account behaves like a person. An import
    that stamps hundreds of episodes onto one claimed day inflates the ALL
    variant without the account doing anything botlike, so the bot signal must
    use SURVIVOR. The first version of this step reported the ALL variant in its
    bot table while claiming to have controlled for exactly that confound. It had
    not. Corrected here.

  - The BULK-MARK question (report Sec 8) asks what is left over after every
    contamination test has run. That question is about survivors by construction,
    so it uses SURVIVOR too.

Both are computed and both are written, so the difference is inspectable rather
than asserted. Counting is of DISTINCT episodes per (account, claimed UTC day),
not of records: rewatches and duplicate plays are not extra viewing.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
BACKFILL_D = 180.0
THRESHOLDS = (24, 48, 96)


def day_loads(user, ts, show, season, number, n_users):
    """Return (cell_user, cell_day, distinct_episode_count) per (user, UTC day)."""
    day = (ts // 86400).astype(np.int64)
    ep = (show.astype(np.int64) * 4000
          + (season.astype(np.int64) % 2000) * 1000
          + (number.astype(np.int64) % 1000))
    o = np.lexsort((ep, day, user))
    u, d, e = user[o], day[o], ep[o]
    new = np.r_[True, (u[1:] != u[:-1]) | (d[1:] != d[:-1]) | (e[1:] != e[:-1])]
    uu, dd = u[new], d[new]
    b = np.flatnonzero(np.r_[True, (uu[1:] != uu[:-1]) | (dd[1:] != dd[:-1]), True])
    return uu[b[:-1]], dd[b[:-1]], np.diff(b), int(new.sum())


def main():
    d = np.load(P5 / "record_lag.npz")
    user, ts, kind = d["user"], d["ts"], d["kind"]
    show, season, number = d["show"], d["season"], d["number"]
    lag, corrupt, undated = d["lag_days"], d["corrupt"], d["undated"]
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    n_users = len(users)

    m3 = np.zeros(len(user), dtype=bool)
    m3[np.load(P5 / "mode3_flags.npz")["record_index"]] = True

    base = (kind == 1) & (show > 0) & (~corrupt) & (~undated)
    variants = {
        "all": base,
        "survivor": base & (lag <= BACKFILL_D) & (~m3),
    }

    out = {}
    store = {}
    for name, mask in variants.items():
        cu, cd, sz, n_distinct = day_loads(
            user[mask], ts[mask], show[mask], season[mask], number[mask], n_users)
        maxday = np.zeros(n_users, dtype=np.int64)
        np.maximum.at(maxday, cu, sz)
        store[f"max_eps_day_{name}"] = maxday
        v = {"records": int(mask.sum()), "distinct_episode_days": n_distinct,
             "cells": int(len(sz))}
        for th in THRESHOLDS:
            over = sz > th
            cnt = np.zeros(n_users, dtype=np.int64)
            np.add.at(cnt, cu[over], 1)
            store[f"days_over_{th}_{name}"] = cnt
            v[f"over_{th}"] = {
                "cells": int(over.sum()),
                "distinct_episode_days_in_them": int(sz[over].sum()),
                "share_of_distinct_episode_days": round(float(sz[over].sum() / n_distinct), 4),
                "accounts_ge_1_day": int((cnt >= 1).sum()),
                "accounts_ge_10_days": int((cnt >= 10).sum()),
                "accounts_ge_30_days": int((cnt >= 30).sum()),
                "accounts_ge_100_days": int((cnt >= 100).sum()),
            }
        out[name] = v
        if name == "survivor":
            surv_cu, surv_cd, surv_sz = cu, cd, sz

    np.savez(P5 / "throughput.npz", **store)

    # per-pair: distinct episodes on the claimed S1-completion day, SURVIVOR basis
    lut = dict(zip((surv_cu.astype(np.int64) * 100000 + surv_cd).tolist(), surv_sz.tolist()))
    p = pd.read_csv(P5 / "pair_contamination.csv")
    k = p.user_idx.values.astype(np.int64) * 100000 + (p.complete_rec_ts.values // 86400)
    p_out = pd.DataFrame({
        "user_idx": p.user_idx,
        "show_trakt_id": p.show_trakt_id,
        "completion_day_eps_survivor": [lut.get(int(x), 0) for x in k],
    })
    p_out.to_csv(P5 / "pair_completion_day_load.csv", index=False)

    (P5 / "throughput.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    print("\nwrote throughput.npz, pair_completion_day_load.csv, throughput.json")


if __name__ == "__main__":
    main()
