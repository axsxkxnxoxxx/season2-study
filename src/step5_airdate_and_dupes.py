"""Step 5: air-date-stamped imports (contamination mode 3), and duplicate accounts
re-detected on records that mode 3 cannot fake.

READ ONLY. Zero network calls.

MODE 3
A class of import stamps `watched_at` with the episode's ORIGINAL BROADCAST
instant rather than with any date the user supplied. The signature is a
(show, season, episode, instant) tuple shared by many unrelated accounts, landing
on an exact top of the hour, spaced seven days apart, at hours that are US prime
time in UTC. Individually these timestamps look like ordinary viewing. They are
the most dangerous class in this store, because an air-date-stamped S2 record
reads as "watched it the night it aired".

The test used here is cross-account collision: a tuple carrying the same instant
in the same episode for at least MIN_ACCOUNTS distinct accounts. With 2,549
accounts sampled out of Trakt's millions, genuine coincidence at minute precision
across five sampled accounts is not a plausible explanation.

DUPLICATE ACCOUNTS, REDONE
The first pass detected mode 3, not duplicate people: two accounts both carrying
the same air-date stamp are not related. Duplicate detection is therefore
restricted to records with |lag| <= 7 days, which are logged at or near real time
and which an air-date import cannot manufacture.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

MIN_ACCOUNTS = 5
GROUP_CAP = 40
MIN_SHARED = 30


def sig(show, season, number, ts):
    return (
        show.astype(np.uint64) * np.uint64(1000003)
        ^ (season.astype(np.uint64) << np.uint64(17))
        ^ (number.astype(np.uint64) << np.uint64(33))
        ^ (ts.astype(np.uint64) * np.uint64(2654435761))
    )


def main():
    d = np.load(P5 / "record_lag.npz")
    user, ts, kind = d["user"], d["ts"], d["kind"]
    show, season, number = d["show"], d["season"], d["number"]
    lag, corrupt, undated = d["lag_days"], d["corrupt"], d["undated"]
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    n_users = len(users)
    out = {}

    ep = (kind == 1) & (~corrupt) & (~undated) & (show > 0)
    h = sig(show[ep], season[ep], number[ep], ts[ep])
    U, T, L = user[ep], ts[ep], lag[ep]
    o = np.argsort(h, kind="stable")
    H, U, T, L = h[o], U[o], T[o], L[o]
    idx = np.flatnonzero(ep)[o]

    b = np.flatnonzero(np.r_[True, H[1:] != H[:-1], True])
    sizes = np.diff(b)

    # ---- mode 3: cross-account collision -------------------------------------
    cand = np.flatnonzero(sizes >= MIN_ACCOUNTS)
    mode3 = np.zeros(len(H), dtype=bool)
    n_groups = 0
    top_hour = 0
    checked = 0
    max_accounts = 0
    for i in cand:
        a, e = b[i], b[i + 1]
        n_acc = len(np.unique(U[a:e]))
        if n_acc < MIN_ACCOUNTS:
            continue
        if n_acc > max_accounts:
            max_accounts = n_acc
        n_groups += 1
        mode3[a:e] = True
        if checked < 20000:
            checked += 1
            if (T[a] % 3600) == 0:
                top_hour += 1

    n_mode3 = int(mode3.sum())
    total_ep_dated = int(ep.sum())
    out["mode3_airdate_stamp"] = {
        "min_accounts": MIN_ACCOUNTS,
        "groups": n_groups,
        "max_accounts_per_group": max_accounts,
        "records": n_mode3,
        "share_of_dated_episode_records": round(n_mode3 / total_ep_dated, 6),
        "share_of_all_records": round(n_mode3 / len(user), 6),
        "share_at_exact_top_of_hour_sampled": round(top_hour / max(1, checked), 4),
        "share_of_these_that_are_backfill_gt180d": round(float(np.mean(L[mode3] > 180)), 6),
        "median_lag_days": round(float(np.median(L[mode3])), 1),
    }
    # already caught by the lag rule?
    out["mode3_airdate_stamp"]["records_not_caught_by_lag180"] = int(
        np.sum(mode3 & ~(L > 180))
    )

    # per-user mode 3 exposure
    m3u = np.bincount(U[mode3], minlength=n_users)
    tot_u = np.bincount(user, minlength=n_users)
    share = m3u / np.maximum(1, tot_u)
    out["mode3_airdate_stamp"]["accounts_with_any"] = int((m3u > 0).sum())
    out["mode3_airdate_stamp"]["accounts_share_gt_10pct"] = int((share > 0.10).sum())
    out["mode3_airdate_stamp"]["accounts_share_gt_50pct"] = int((share > 0.50).sum())

    # ---- duplicates on near-real-time records only ---------------------------
    clean = np.abs(L) <= 7
    Hc, Uc = H[clean], U[clean]
    oc = np.argsort(Hc, kind="stable")
    Hc, Uc = Hc[oc], Uc[oc]
    bc = np.flatnonzero(np.r_[True, Hc[1:] != Hc[:-1], True])
    per_user = np.bincount(Uc, minlength=n_users)
    pair = Counter()
    over = 0
    for i in range(len(bc) - 1):
        a, e = bc[i], bc[i + 1]
        if e - a < 2:
            continue
        g = np.unique(Uc[a:e])
        if len(g) < 2:
            continue
        if len(g) > GROUP_CAP:
            over += 1
            continue
        for x in range(len(g)):
            for y in range(x + 1, len(g)):
                pair[(int(g[x]), int(g[y]))] += 1

    rows = []
    for (u1, u2), c in pair.items():
        if c < MIN_SHARED:
            continue
        den = min(per_user[u1], per_user[u2])
        rows.append({
            "user_a": users[u1], "user_b": users[u2],
            "idx_a": u1, "idx_b": u2,
            "shared_realtime_events": c,
            "realtime_events_a": int(per_user[u1]),
            "realtime_events_b": int(per_user[u2]),
            "containment": round(float(c / max(1, den)), 6),
        })
    rows.sort(key=lambda r: -r["containment"])
    with open(P5 / "duplicate_pairs_realtime.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=(list(rows[0].keys()) if rows else
                                           ["user_a", "user_b", "idx_a", "idx_b",
                                            "shared_realtime_events", "realtime_events_a",
                                            "realtime_events_b", "containment"]))
        w.writeheader()
        w.writerows(rows)

    bands = {}
    for lo in (0.3, 0.5, 0.7, 0.9):
        sel = [r for r in rows if r["containment"] >= lo]
        acc = {r["idx_a"] for r in sel} | {r["idx_b"] for r in sel}
        bands[f"containment_ge_{lo}"] = {"pairs": len(sel), "accounts": len(acc)}
    out["duplicates_realtime"] = {
        "basis": "|lag| <= 7d records only",
        "min_shared": MIN_SHARED,
        "groups_over_cap": over,
        "pairs_reported": len(rows),
        "bands": bands,
        "top_containments": [r["containment"] for r in rows[:10]],
        "top_shared_counts": [r["shared_realtime_events"] for r in rows[:10]],
    }

    (P5 / "airdate_and_dupes.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))
    np.savez(P5 / "mode3_flags.npz", record_index=idx[mode3], per_user_mode3=m3u)


if __name__ == "__main__":
    main()
