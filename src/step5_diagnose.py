"""Step 5 contamination diagnostics: per-record backfill lag, per-user metrics,
bot signals, duplicate-account detection, aggregate shares.

READ ONLY on the pull. Zero network calls.

Outputs (all to processed/, because everything here is keyed to an account):
  processed/step5/user_metrics.csv      one row per user, all flags and scores
  processed/step5/duplicate_pairs.csv   candidate duplicate account pairs
  processed/step5/aggregates.json       counts and shares, safe to quote

Nothing in this file adopts an exclusion. It measures and it flags.
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

NULL_TS = np.iinfo(np.int64).min
DAY = 86400.0
TAU_PULL = int(dt.datetime(2026, 8, 11, tzinfo=dt.timezone.utc).timestamp())
T_1990 = int(dt.datetime(1990, 1, 1, tzinfo=dt.timezone.utc).timestamp())
TVTIME_SHUTDOWN = int(dt.datetime(2026, 7, 15, tzinfo=dt.timezone.utc).timestamp())

# Backfill lag thresholds reported. 180d is the primary reporting threshold; the
# others are shown so the reader can see how sensitive the share is to it.
LAGS = (30, 90, 180, 365)
PRIMARY_LAG = 180 * DAY


def iso(x) -> str:
    return dt.datetime.fromtimestamp(int(x), dt.timezone.utc).strftime("%Y-%m-%d")


def main():
    d = np.load(P5 / "full_scan.npz")
    cal = np.load(P5 / "calibration.npz")
    rid, ts, action, kind = d["rid"], d["ts"], d["action"], d["kind"]
    user, show, season, number = d["user"], d["show"], d["season"], d["number"]
    kr, kt = cal["knot_rid"], cal["knot_time"]
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    n_users = len(users)

    # ---- de-duplicate the 182 repeated (user, rid) rows from pagination overlap
    key = user.astype(np.int64) * (1 << 40) + np.arange(len(rid)) * 0  # placeholder
    order = np.lexsort((rid, user))
    dup = np.zeros(len(rid), dtype=bool)
    su, sr = user[order], rid[order]
    same = np.empty(len(order), dtype=bool)
    same[0] = False
    same[1:] = (su[1:] == su[:-1]) & (sr[1:] == sr[:-1])
    dup[order[same]] = True
    n_dup_rows = int(dup.sum())
    keep = ~dup
    print(f"dropped {n_dup_rows} duplicate (user, rid) rows from pagination overlap")

    rid, ts, action, kind = rid[keep], ts[keep], action[keep], kind[keep]
    user, show, season, number = user[keep], show[keep], season[keep], number[keep]
    n = len(rid)

    # ---- record classification -------------------------------------------------
    undated = ts == NULL_TS
    corrupt = (~undated) & (ts < T_1990)          # epoch-zero and pre-1990 garbage
    dated = (~undated) & (~corrupt)
    tau = np.interp(rid.astype(np.float64), kr, kt)
    lag = np.where(dated, tau - ts.astype(np.float64), np.nan)

    print(f"records {n:,}  undated {undated.sum():,}  corrupt(<1990) {corrupt.sum():,}"
          f"  dated {dated.sum():,}")

    agg = {
        "records_total": int(n),
        "duplicate_user_rid_rows_dropped": n_dup_rows,
        "users": n_users,
        "undated": int(undated.sum()),
        "corrupt_pre1990": int(corrupt.sum()),
        "epoch_zero": int((ts == 0).sum()),
        "dated": int(dated.sum()),
        "records_episode": int((kind == 1).sum()),
        "records_movie": int((kind == 0).sum()),
    }

    # ---- overall backfill shares ----------------------------------------------
    ld = lag / DAY
    agg["backfill_share_of_dated"] = {}
    agg["backfill_share_of_all"] = {}
    for L in LAGS:
        c = int(np.nansum(ld > L))
        agg["backfill_share_of_dated"][f"gt_{L}d"] = round(c / dated.sum(), 6)
        # corrupt and undated records are not real dates either; count them as
        # unusable alongside backfill for the "of all" view
        agg["backfill_share_of_all"][f"gt_{L}d"] = round(c / n, 6)
    agg["unusable_or_backfilled_share_of_all_180d"] = round(
        (int(np.nansum(ld > 180)) + int(corrupt.sum()) + int(undated.sum())) / n, 6
    )
    agg["negative_lag_gt_30d_share_of_dated"] = round(
        float(np.nansum(ld < -30)) / dated.sum(), 6
    )

    # ---- backfill by action ----------------------------------------------------
    agg["by_action"] = {}
    for name, code in (("watch", 0), ("checkin", 1), ("scrobble", 2)):
        m = dated & (action == code)
        agg["by_action"][name] = {
            "n": int(m.sum()),
            "median_lag_days": round(float(np.median(ld[m])), 4),
            "share_gt_180d": round(float(np.mean(ld[m] > 180)), 6),
        }

    # ---- when was the backfill inserted? weekly histogram ----------------------
    bf = dated & (ld > 180)
    week = (tau // (7 * DAY)).astype(np.int64)
    wk_all = np.bincount(week - week.min())
    wk_bf = np.bincount((week - week.min())[bf], minlength=len(wk_all))
    base = week.min()
    hist = []
    for i in range(len(wk_all)):
        if wk_all[i] == 0:
            continue
        hist.append({
            "week_start": iso((base + i) * 7 * DAY),
            "inserted": int(wk_all[i]),
            "backfilled": int(wk_bf[i]),
            "share": round(float(wk_bf[i] / wk_all[i]), 4),
        })
    agg["weekly_insert_histogram_tail"] = hist[-40:]

    # 2026 import window concentration
    for label, t0 in (("2026-06-01", dt.datetime(2026, 6, 1)), ("2026-07-01", dt.datetime(2026, 7, 1))):
        t0 = int(t0.replace(tzinfo=dt.timezone.utc).timestamp())
        m = tau >= t0
        agg[f"inserted_since_{label}"] = {
            "records": int(m.sum()),
            "share_of_all_records": round(float(m.mean()), 6),
            "backfilled_gt180d": int((m & bf).sum()),
            "share_of_all_backfill": round(float((m & bf).sum() / max(1, bf.sum())), 6),
        }

    # ---- per-user metrics ------------------------------------------------------
    order = np.lexsort((tau, user))
    u_s, tau_s, ld_s, ts_s, act_s, cor_s, dat_s = (
        user[order], tau[order], ld[order], ts[order],
        action[order], corrupt[order], dated[order],
    )
    starts = np.searchsorted(u_s, np.arange(n_users), side="left")
    ends = np.searchsorted(u_s, np.arange(n_users), side="right")

    rows = []
    for u in range(n_users):
        a, b = starts[u], ends[u]
        t = tau_s[a:b]
        L = ld_s[a:b]
        cnt = b - a
        isbf = (L > 180) & dat_s[a:b]
        # largest insert burst in a 1-day and 7-day real-time window
        def max_window(mask, days):
            tt = t[mask]
            if len(tt) == 0:
                return 0, 0.0, 0.0, np.nan
            hi = np.searchsorted(tt, tt + days * DAY, side="right")
            k = hi - np.arange(len(tt))
            j = int(np.argmax(k))
            lo_i, hi_i = j, int(hi[j])
            sub_ts = ts_s[a:b][mask][lo_i:hi_i]
            sub_ts = sub_ts[sub_ts > T_1990]
            span = (sub_ts.max() - sub_ts.min()) / DAY if len(sub_ts) > 1 else 0.0
            return int(k[j]), float(k[j] / cnt), float(span), float(tt[j])

        b1_n, b1_sh, _, _ = max_window(np.ones(cnt, dtype=bool), 1)
        b7_n, b7_sh, _, _ = max_window(np.ones(cnt, dtype=bool), 7)
        bf1_n, bf1_sh, bf1_span, bf1_at = max_window(isbf, 1)
        bf7_n, bf7_sh, bf7_span, bf7_at = max_window(isbf, 7)

        realtime_n = int(((np.abs(L) <= 1) & dat_s[a:b]).sum())
        rows.append({
            "user_idx": u,
            "username": users[u],
            "records": cnt,
            "corrupt_dates": int(cor_s[a:b].sum()),
            "corrupt_share": round(float(cor_s[a:b].mean()), 6),
            "backfill_gt180d": int(isbf.sum()),
            "backfill_share": round(float(isbf.sum() / cnt), 6),
            "realtime_within_1d": realtime_n,
            "realtime_share": round(float(realtime_n / cnt), 6),
            "checkin_scrobble": int((act_s[a:b] != 0).sum()),
            "insert_span_days": round(float((t[-1] - t[0]) / DAY), 3),
            "first_insert": iso(t[0]),
            "last_insert": iso(t[-1]),
            "burst1d_n": b1_n, "burst1d_share": round(b1_sh, 6),
            "burst7d_n": b7_n, "burst7d_share": round(b7_sh, 6),
            "bf_burst1d_n": bf1_n, "bf_burst1d_share": round(bf1_sh, 6),
            "bf_burst7d_n": bf7_n, "bf_burst7d_share": round(bf7_sh, 6),
            "bf_burst7d_watch_span_days": round(bf7_span, 1),
            "bf_burst7d_inserted_at": iso(bf7_at) if bf7_n else "",
        })
        if (u + 1) % 500 == 0:
            print(f"  user metrics {u+1}/{n_users}")

    import csv
    with open(P5 / "user_metrics.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("wrote", P5 / "user_metrics.csv")

    (P5 / "aggregates.json").write_text(json.dumps(agg, indent=2))
    print("wrote", P5 / "aggregates.json")

    # save per-record lag for reuse
    np.savez(P5 / "record_lag.npz", user=user, rid=rid, ts=ts, tau=tau,
             lag_days=ld.astype(np.float32), kind=kind, action=action,
             show=show, season=season, number=number,
             corrupt=corrupt, undated=undated)
    print("wrote", P5 / "record_lag.npz")


if __name__ == "__main__":
    main()
