"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 2a of 4.

Builds ONCE the canonical S2 distinct-episode table for every pair on waterfall line 4
(152,126, BEFORE D10), so the W arms in stage 2b can be evaluated without touching the
record table again.

The canonical timestamp of a distinct episode is the MINIMUM watched_at across its records
(Step 1 SS2.2). Membership is by SET against E2 (SS3.2), never the range 1..F2. D11 discards
records at or after tau_pull globally. None of these depend on W, so the table is built once.

For the ALT rule only |A| matters, but |A_H| and F2-in-A_H are carried too so stage 2b can
report the exclusion set's composition by outcome at every arm.

Zero API calls.
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step7/alt_a")

SEC_PER_DAY = 86400.0
BACKFILL_D = 180.0
POSTDATE_D = -30.0
PUBLISHED_WATERFALL = [201900, 178165, 155131, 152126, 128099]
FROZEN_LINE = 3
MISSING = np.iinfo(np.int64).min
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def build_waterfall(p):
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    the1542 = t0c & ~has_s2
    keep = ~(all_air | the1542)
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w1 = keep
    w2 = w1 & has_s2
    w3 = w2 & ~t0c
    w4 = w3 & ~postd
    w5 = w4 & ~fs2_bad
    return [w1, w2, w3, w4, w5]


def t0_floor_epoch(p):
    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    v = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
         .astype("datetime64[s]").astype("int64").astype("float64"))
    v[t0_dt.isna().to_numpy()] = np.nan
    ok = ~np.isnan(v)
    assert v[ok].min() > 0 and v[ok].max() < 2.2e9, "T0 epoch unit wrong"
    return v


def main():
    os.makedirs(OUT, exist_ok=True)

    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)
    masks = build_waterfall(p)
    computed = [int(m.sum()) for m in masks]
    assert computed == PUBLISHED_WATERFALL, f"waterfall mismatch: {computed}"
    ref152 = masks[FROZEN_LINE]
    rows = np.flatnonzero(ref152)
    n = rows.size

    t0f = t0_floor_epoch(p)
    assert int((ref152 & np.isnan(t0f)).sum()) == 0

    pairs = pd.DataFrame({
        "row": np.arange(n, dtype=np.int64),
        "user_idx": p.user_idx.values[rows].astype(np.int64),
        "show": p.show_trakt_id.values[rows].astype(np.int64),
    })
    assert not pairs.duplicated(["user_idx", "show"]).any()

    f = pd.read_csv(os.path.join(P2, "frame.csv"),
                    usecols=["show_trakt_id", "s2_L", "s2_F", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    l2 = dict(zip(f.show_trakt_id.astype(int), f.s2_L.astype(int)))
    f2 = dict(zip(f.show_trakt_id.astype(int), f.s2_F.astype(int)))
    for sh, es in e2.items():
        assert len(es) == l2[sh], f"|E2| != L2 for show {sh}"
        assert f2[sh] in es, f"F2 not in E2 for show {sh}"
    pairs["L2"] = pairs.show.map(l2).astype(np.int64)
    pairs["F2"] = pairs.show.map(f2).astype(np.int64)

    z = np.load(os.path.join(P5, "full_scan.npz"))
    season = z["season"]
    s2m = season == 2
    del season
    rec = pd.DataFrame({
        "user_idx": z["user"][s2m].astype(np.int64),
        "show": z["show"][s2m].astype(np.int64),
        "number": z["number"][s2m].astype(np.int64),
        "ts": z["ts"][s2m].astype(np.int64),
    })
    del z, s2m
    n_raw = len(rec)
    rec = rec[rec.ts.values != MISSING]
    n_pull = int((rec.ts.values >= TAU_PULL).sum())
    rec = rec[rec.ts.values < TAU_PULL]
    in_e2 = np.fromiter(
        (nu in e2.get(sh, ()) for sh, nu in zip(rec.show.values, rec.number.values)),
        dtype=bool, count=len(rec))
    n_out = int((~in_e2).sum())
    rec = rec[in_e2]

    ep = rec.groupby(["user_idx", "show", "number"], as_index=False)["ts"].min()
    del rec
    ep = ep.merge(pairs[["row", "user_idx", "show", "F2"]],
                  on=["user_idx", "show"], how="inner")

    np.savez_compressed(
        os.path.join(OUT, "episodes_line4.npz"),
        pair_row=rows,                                  # index into pair_revision5 row order
        user_idx=pairs.user_idx.values, show=pairs.show.values,
        L2=pairs.L2.values, F2=pairs.F2.values,
        t0_floor=t0f[rows],
        ep_row=ep.row.values.astype(np.int64),
        ep_ts=ep.ts.values.astype("float64"),
        ep_is_f2=(ep.number.values == ep.F2.values),
        ep_number=ep.number.values.astype(np.int64),
    )
    summary = {
        "instance": "alt_a", "stage": "2a", "api_calls": 0,
        "line4_pairs": int(n),
        "s2_records_raw": n_raw,
        "s2_records_at_or_after_tau_pull_D11": n_pull,
        "s2_records_dropped_number_not_in_E2": n_out,
        "distinct_episodes_on_line4": int(len(ep)),
        "pairs_with_zero_distinct_S2_episodes": int(n - ep.row.nunique()),
        "note": "line 2 of the waterfall requires S2 evidence, so a line-4 pair with zero "
                "distinct in-E2 S2 episodes can only arise from the E2 set-membership drop "
                "or D11; the count is reported rather than assumed zero",
    }
    with open(os.path.join(OUT, "episodes_line4.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
