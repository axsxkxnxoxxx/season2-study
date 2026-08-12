"""Step 5: what the contamination does to the study population.

READ ONLY. Zero network calls.

Account-level shares are not the number the gate needs. The gate needs pairs: how
many user-show pairs carry a clock start that an import wrote, and how many pairs
each candidate exclusion rule would cost.

S1 completion follows the approved Step 1 Sec 4 rule as restated in Step 2 Sec 4:
  F1 in D1  and  |D1| >= ceil(0.90 * L1)
with D1 the distinct S1 episodes whose number is a MEMBER of the real E1,
L1 = |E1|, F1 = max(E1).

The first-pass S1 completion instant is computed the way a downstream step would
compute it, by walking the pair's S1 records in watched_at order and taking the
instant at which both conditions first hold. It is deliberately NOT cleaned
first. The point of this file is to show what that instant is made of.

Nothing here is an exclusion. It is a cost table for proposals.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"

DAY = 86400.0
T_1990 = int(dt.datetime(1990, 1, 1, tzinfo=dt.timezone.utc).timestamp())
BACKFILL_D = 180.0


def parse_set(s):
    return {int(x) for x in str(s).split(",") if x.strip().isdigit()}


def main():
    frame = pd.read_csv(ROOT / "processed" / "step2" / "frame.csv")
    print(f"frame shows: {len(frame)}")
    e1 = {int(r.show_trakt_id): parse_set(r.s1_E) for r in frame.itertuples()}
    e2 = {int(r.show_trakt_id): parse_set(r.s2_E) for r in frame.itertuples()}
    l1 = {k: len(v) for k, v in e1.items()}
    f1 = {k: (max(v) if v else -1) for k, v in e1.items()}
    thr = {k: int(np.ceil(0.90 * v)) for k, v in l1.items()}
    frame_ids = np.array(sorted(e1.keys()), dtype=np.int64)

    d = np.load(P5 / "record_lag.npz")
    user, ts, kind = d["user"], d["ts"], d["kind"]
    show, season, number = d["show"], d["season"], d["number"]
    lag, corrupt, undated = d["lag_days"], d["corrupt"], d["undated"]
    users = json.loads((P5 / "user_index.json").read_text())["users"]

    m3 = np.zeros(len(user), dtype=bool)
    m3[np.load(P5 / "mode3_flags.npz")["record_index"]] = True
    print(f"mode-3 air-date-stamped records: {m3.sum():,}")

    m = (kind == 1) & np.isin(show, frame_ids) & ((season == 1) | (season == 2))
    print(f"episode records on frame shows, S1 or S2: {m.sum():,}")
    u, sh, se, nu = user[m], show[m], season[m], number[m]
    t, lg, co, un, a3 = ts[m], lag[m], corrupt[m], undated[m], m3[m]

    # order by (user, show, season, watched_at); undated sort last
    tsort = np.where(un, np.iinfo(np.int64).max, t)
    order = np.lexsort((tsort, se, sh, u))
    u, sh, se, nu = u[order], sh[order], se[order], nu[order]
    t, lg, co, un, a3 = t[order], lg[order], co[order], un[order], a3[order]
    tsort = tsort[order]

    grp = np.flatnonzero(np.r_[True, (u[1:] != u[:-1]) | (sh[1:] != sh[:-1]), True])
    print(f"user-show groups on frame shows: {len(grp)-1:,}")

    rows = []
    for i in range(len(grp) - 1):
        a, b = grp[i], grp[i + 1]
        sid = int(sh[a])
        E1, E2 = e1[sid], e2[sid]
        s1m = se[a:b] == 1
        if not s1m.any():
            continue
        n1 = nu[a:b][s1m]
        t1 = t[a:b][s1m]
        lg1 = lg[a:b][s1m]
        co1 = co[a:b][s1m]
        un1 = un[a:b][s1m]
        a31 = a3[a:b][s1m]
        inE = np.array([int(x) in E1 for x in n1])
        if not inE.any():
            continue
        n1, t1, lg1, co1, un1, a31 = (n1[inE], t1[inE], lg1[inE],
                                      co1[inE], un1[inE], a31[inE])

        # walk in watched_at order accumulating distinct episodes (already sorted)
        seen = set()
        need = thr[sid]
        fin = f1[sid]
        comp_idx = -1
        for j in range(len(n1)):
            seen.add(int(n1[j]))
            if len(seen) >= need and fin in seen:
                comp_idx = j
                break
        if comp_idx < 0:
            continue  # not an S1 completer

        # S1 evidence used up to and including the completing record
        ev_bf = int(np.sum(lg1[: comp_idx + 1] > BACKFILL_D))
        ev_co = int(np.sum(co1[: comp_idx + 1]))
        ev_a3 = int(np.sum(a31[: comp_idx + 1]))
        ev_n = comp_idx + 1

        s2m = se[a:b] == 2
        n2 = nu[a:b][s2m]
        lg2 = lg[a:b][s2m]
        co2 = co[a:b][s2m]
        a32 = a3[a:b][s2m]
        in2 = np.array([int(x) in E2 for x in n2]) if len(n2) else np.zeros(0, bool)
        n2v = n2[in2] if len(n2) else n2
        d2 = len(set(int(x) for x in n2v))
        s2_bf = int(np.sum(lg2[in2] > BACKFILL_D)) if len(n2) else 0
        s2_n = int(in2.sum()) if len(n2) else 0
        s2_a3 = int(np.sum(a32[in2])) if len(n2) else 0
        # Step 6 reads the lag from T0 to the FIRST S2 watch, so that one
        # record's provenance is what decides whether the pair can inform W.
        if s2_n:
            k0 = int(np.flatnonzero(in2)[0])
            f2_lag = float(lg2[k0])
            f2_co = int(co2[k0])
            f2_a3 = int(a32[k0])
            f2_ts = int(t[a:b][s2m][k0])
        else:
            f2_lag, f2_co, f2_a3, f2_ts = float("nan"), 0, 0, 0

        rows.append((
            int(u[a]), sid, ev_n, ev_bf, ev_co,
            int(co1[comp_idx]), int(un1[comp_idx]),
            float(lg1[comp_idx]), int(t1[comp_idx]), int(a31[comp_idx]),
            ev_a3, d2, s2_n, s2_bf, s2_a3, f2_lag, f2_co, f2_a3, f2_ts,
        ))
        if len(rows) % 50000 == 0:
            print(f"  completer pairs so far: {len(rows):,}")

    cols = ["user_idx", "show_trakt_id", "s1_ev_n", "s1_ev_backfilled", "s1_ev_corrupt",
            "complete_rec_corrupt", "complete_rec_undated", "complete_rec_lag_days",
            "complete_rec_ts", "complete_rec_airdate", "s1_ev_airdate", "s2_distinct",
            "s2_ev_n", "s2_ev_backfilled", "s2_ev_airdate",
            "first_s2_lag_days", "first_s2_corrupt", "first_s2_airdate", "first_s2_ts"]
    df = pd.DataFrame(rows, columns=cols)
    df["username"] = [users[i] for i in df.user_idx]
    print(f"\nS1-completer pairs: {len(df):,}  (Step 2 reports 220,107)")

    df.to_parquet(P5 / "pair_contamination.parquet") if False else df.to_csv(
        P5 / "pair_contamination.csv", index=False)
    print("wrote", P5 / "pair_contamination.csv")

    # ---- headline pair-level contamination ------------------------------------
    out = {"pairs_total": int(len(df))}
    out["clock_start_backfilled_gt180d"] = int((df.complete_rec_lag_days > BACKFILL_D).sum())
    out["clock_start_corrupt_pre1990"] = int(df.complete_rec_corrupt.sum())
    out["clock_start_undated"] = int(df.complete_rec_undated.sum())
    out["clock_start_airdate_stamped"] = int(df.complete_rec_airdate.sum())
    out["clock_start_airdate_not_caught_by_lag"] = int(
        ((df.complete_rec_airdate == 1) & (df.complete_rec_lag_days <= BACKFILL_D)
         & (df.complete_rec_corrupt == 0)).sum())
    bad = ((df.complete_rec_lag_days > BACKFILL_D) | (df.complete_rec_corrupt == 1)
           | (df.complete_rec_undated == 1) | (df.complete_rec_airdate == 1))
    out["clock_start_unusable_any"] = int(bad.sum())
    out["clock_start_unusable_share"] = round(float(bad.mean()), 6)
    for L in (30, 90, 365):
        out[f"clock_start_backfilled_gt{L}d"] = int((df.complete_rec_lag_days > L).sum())
    out["any_s1_evidence_backfilled"] = int((df.s1_ev_backfilled > 0).sum())
    out["all_s1_evidence_backfilled"] = int((df.s1_ev_backfilled == df.s1_ev_n).sum())
    s2p = df[df.s2_ev_n > 0]
    out["pairs_with_s2_evidence"] = int(len(s2p))
    out["s2_evidence_all_backfilled"] = int((s2p.s2_ev_backfilled == s2p.s2_ev_n).sum())
    out["s2_evidence_any_backfilled"] = int((s2p.s2_ev_backfilled > 0).sum())
    out["s2_evidence_any_airdate"] = int((s2p.s2_ev_airdate > 0).sum())
    out["s2_evidence_all_airdate"] = int((s2p.s2_ev_airdate == s2p.s2_ev_n).sum())

    (P5 / "pair_aggregates.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
