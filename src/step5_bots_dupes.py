"""Step 5: bot signals and duplicate-account detection.

READ ONLY. Zero network calls.

DUPLICATE ACCOUNTS
Two accounts held by the same person, or one account re-uploaded under a second
name, produce the same viewing events at the same instants. The signature used is
the exact tuple (show, season, episode number, watched_at), hashed. Two different
people watching the same episode in the same MINUTE is possible; two people
agreeing on thousands of such tuples is not.

Records with corrupt dates (pre-1990, mostly epoch zero) are excluded from the
signature. They collide across unrelated accounts by construction - everyone's
undated import lands on 1970-01-01 - and would manufacture duplicate pairs.

BOT SIGNALS
No ground truth exists here, so these are reported as signals, not verdicts:
  1. timestamp degeneracy - many records sharing one exact instant
  2. implausible claimed real-time throughput - distinct episodes per claimed
     viewing day, counted only on records that are NOT backfill, so that an
     import's flat timestamps do not read as a bot
  3. sustained volume over the life of the account
"""
from __future__ import annotations

import csv
import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

DAY = 86400.0
T_1990 = int(dt.datetime(1990, 1, 1, tzinfo=dt.timezone.utc).timestamp())
GROUP_CAP = 40  # event-hash groups larger than this are mass events, not evidence
MIN_SHARED = 50  # report account pairs sharing at least this many exact events


def main():
    d = np.load(P5 / "record_lag.npz")
    user, ts, kind = d["user"], d["ts"], d["kind"]
    show, season, number = d["show"], d["season"], d["number"]
    lag, corrupt, undated = d["lag_days"], d["corrupt"], d["undated"]
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    n_users = len(users)
    counts = np.bincount(user, minlength=n_users)

    out = {}

    # ---------- duplicate accounts -------------------------------------------
    ep = (kind == 1) & (~corrupt) & (~undated) & (show > 0)
    h = (
        show[ep].astype(np.uint64) * np.uint64(1000003)
        ^ (season[ep].astype(np.uint64) << np.uint64(17))
        ^ (number[ep].astype(np.uint64) << np.uint64(33))
        ^ (ts[ep].astype(np.uint64) * np.uint64(2654435761))
    )
    hu = user[ep]
    order = np.argsort(h, kind="stable")
    hs, us_ = h[order], hu[order]
    bounds = np.flatnonzero(np.r_[True, hs[1:] != hs[:-1], True])
    print(f"event signatures: {len(hs):,} records, {len(bounds)-1:,} distinct")

    pair_counts = Counter()
    over_cap = 0
    multi = 0
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b - a < 2:
            continue
        grp = np.unique(us_[a:b])
        if len(grp) < 2:
            continue
        multi += 1
        if len(grp) > GROUP_CAP:
            over_cap += 1
            continue
        for x in range(len(grp)):
            for y in range(x + 1, len(grp)):
                pair_counts[(int(grp[x]), int(grp[y]))] += 1
    print(f"  multi-user signature groups: {multi:,}  over cap({GROUP_CAP}): {over_cap:,}")

    per_user_sig = np.bincount(hu, minlength=n_users)
    dup_rows = []
    for (u1, u2), c in pair_counts.items():
        if c < MIN_SHARED:
            continue
        denom = min(per_user_sig[u1], per_user_sig[u2])
        dup_rows.append({
            "user_a": users[u1], "user_b": users[u2],
            "shared_events": c,
            "events_a": int(per_user_sig[u1]), "events_b": int(per_user_sig[u2]),
            "containment": round(float(c / max(1, denom)), 6),
        })
    dup_rows.sort(key=lambda r: -r["containment"])
    with open(P5 / "duplicate_pairs.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(dup_rows[0].keys()) if dup_rows
                           else ["user_a", "user_b", "shared_events", "events_a", "events_b", "containment"])
        w.writeheader()
        w.writerows(dup_rows)
    print(f"  pairs sharing >= {MIN_SHARED} exact events: {len(dup_rows)}")

    bands = {}
    for lo in (0.5, 0.7, 0.9, 0.98):
        sel = [r for r in dup_rows if r["containment"] >= lo]
        involved = {r["user_a"] for r in sel} | {r["user_b"] for r in sel}
        bands[f"containment_ge_{lo}"] = {"pairs": len(sel), "accounts": len(involved)}
    out["duplicates"] = {
        "min_shared_events": MIN_SHARED,
        "group_cap": GROUP_CAP,
        "groups_over_cap": over_cap,
        "pairs_reported": len(dup_rows),
        "bands": bands,
    }

    # ---------- bot signals ---------------------------------------------------
    # 1. timestamp degeneracy: largest single-instant cluster per user
    key = user.astype(np.int64) * np.int64(1 << 34) + (ts - ts.min()) // 60
    ko = np.argsort(key, kind="stable")
    ks = key[ko]
    bnd = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1], True])
    sizes = np.diff(bnd)
    owner = user[ko][bnd[:-1]]
    max_same_instant = np.zeros(n_users, dtype=np.int64)
    np.maximum.at(max_same_instant, owner, sizes)
    in_big = np.zeros(n_users, dtype=np.int64)
    big = sizes >= 20
    np.add.at(in_big, owner[big], sizes[big])

    # 2. claimed real-time throughput: distinct episodes per claimed viewing day,
    #    restricted to records that are not backfill
    live = (~corrupt) & (~undated) & (lag <= 180) & (kind == 1)
    dkey = user[live].astype(np.int64) * np.int64(1 << 20) + (ts[live] // 86400)
    dsort = np.sort(dkey)
    dbnd = np.flatnonzero(np.r_[True, dsort[1:] != dsort[:-1], True])
    dsz = np.diff(dbnd)
    downer = (dsort[dbnd[:-1]] >> np.int64(20)).astype(np.int64)
    max_eps_day = np.zeros(n_users, dtype=np.int64)
    np.maximum.at(max_eps_day, downer, dsz)
    days_over_50 = np.zeros(n_users, dtype=np.int64)
    np.add.at(days_over_50, downer[dsz > 50], 1)

    rows = []
    for u in range(n_users):
        rows.append({
            "user_idx": u,
            "username": users[u],
            "records": int(counts[u]),
            "max_records_one_minute": int(max_same_instant[u]),
            "share_in_minute_clusters_ge20": round(float(in_big[u] / max(1, counts[u])), 6),
            "max_nonbackfill_eps_one_day": int(max_eps_day[u]),
            "nonbackfill_days_over_50_eps": int(days_over_50[u]),
        })
    with open(P5 / "bot_signals.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", P5 / "bot_signals.csv")

    ms = np.array([r["max_records_one_minute"] for r in rows])
    ed = np.array([r["max_nonbackfill_eps_one_day"] for r in rows])
    d50 = np.array([r["nonbackfill_days_over_50_eps"] for r in rows])
    out["bot_signals"] = {
        "max_records_one_minute": {f"p{q}": int(np.percentile(ms, q)) for q in (50, 75, 90, 99)}
        | {"max": int(ms.max()), "ge_100": int((ms >= 100).sum()), "ge_500": int((ms >= 500).sum())},
        "max_nonbackfill_eps_one_day": {f"p{q}": int(np.percentile(ed, q)) for q in (50, 75, 90, 99)}
        | {"max": int(ed.max()), "ge_50": int((ed >= 50).sum()), "ge_100": int((ed >= 100).sum())},
        "accounts_with_days_over_50_eps": {
            "ge_1_day": int((d50 >= 1).sum()),
            "ge_10_days": int((d50 >= 10).sum()),
            "ge_50_days": int((d50 >= 50).sum()),
        },
    }

    (P5 / "bots_dupes.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
