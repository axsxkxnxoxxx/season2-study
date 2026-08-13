"""Step 7 gate-closing sensitivity test, instance namespace `a` — VALIDATION ONLY.

Runs the identical outcome operator on a population where the answer is already on the
record, so a bug in the operator is visible rather than inferred.

decisions/0034 SS5: on the Step 5 clean-record estimation sample (waterfall line 5, the
128,099, NO D10), applying D11 moved never-started from 8,445 to 8,449.
artifacts/step1-amendment-continued-boundary.md / decisions/0034 SS2: the never-started share
there is 6.5957%, and 2,246 pairs move from Started-and-left to Continued under the amendment.

Reproducing 8,449 and 2,246 on that population validates |A|, |A_H|, F2 in A_H and the
canonical-timestamp rule. Nothing here is adopted and no rule is changed.

Zero API calls.
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step7/sens_a")

MISSING = np.iinfo(np.int64).min
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)
SEC_PER_DAY = 86400.0
W, H = 108, 91
BACKFILL_D, POSTDATE_D = 180.0, -30.0
PUBLISHED = [201900, 178165, 155131, 152126, 128099]


def main():
    cols = ["user_idx", "show_trakt_id", "s2_ev_n", "s2_ev_airdate", "t0_contaminated",
            "complete_rec_lag_days", "first_s2_lag_days", "first_s2_airdate",
            "first_s2_corrupt", "t0"]
    p = pd.read_csv(os.path.join(P5, "pair_revision5.csv"), usecols=cols)
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    postd = (p.complete_rec_lag_days < POSTDATE_D).values
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    keep = ~(all_air | (t0c & ~has_s2))
    fs2_bad = has_s2 & ((p.first_s2_lag_days.values > BACKFILL_D)
                        | (p.first_s2_airdate.values == 1)
                        | (p.first_s2_corrupt.values == 1))
    w = [keep]
    for m in (has_s2, ~t0c, ~postd, ~fs2_bad):
        w.append(w[-1] & m)
    assert [int(x.sum()) for x in w] == PUBLISHED
    est = w[-1]                                    # line 5, the 128,099. NO D10.

    t0_dt = pd.to_datetime(p.t0, utc=True, errors="coerce")
    t0f = (t0_dt.dt.floor("D").dt.tz_localize(None).to_numpy()
           .astype("datetime64[s]").astype("int64").astype("float64"))
    rows = np.flatnonzero(est)
    n = rows.size

    pairs = pd.DataFrame({
        "row": np.arange(n, dtype=np.int64),
        "user_idx": p.user_idx.values[rows].astype(np.int64),
        "show": p.show_trakt_id.values[rows].astype(np.int64),
        "tau1": t0f[rows] + W * SEC_PER_DAY,
        "tau2": t0f[rows] + (W + H) * SEC_PER_DAY,
    })
    f = pd.read_csv(os.path.join(P2, "frame.csv"),
                    usecols=["show_trakt_id", "s2_L", "s2_F", "s2_E"])
    e2 = {int(r.show_trakt_id): set(int(x) for x in str(r.s2_E).split(","))
          for r in f.itertuples()}
    l2 = dict(zip(f.show_trakt_id.astype(int), f.s2_L.astype(int)))
    f2m = dict(zip(f.show_trakt_id.astype(int), f.s2_F.astype(int)))
    pairs["L2"] = pairs.show.map(l2).astype(np.int64)
    pairs["F2"] = pairs.show.map(f2m).astype(np.int64)
    need = np.ceil(0.90 * pairs.L2.values).astype(np.int64)

    z = np.load(os.path.join(P5, "full_scan.npz"))
    s2m = z["season"] == 2
    rec = pd.DataFrame({"user_idx": z["user"][s2m].astype(np.int64),
                        "show": z["show"][s2m].astype(np.int64),
                        "number": z["number"][s2m].astype(np.int64),
                        "ts": z["ts"][s2m].astype(np.int64)})
    del z, s2m
    rec = rec[rec.ts.values != MISSING]
    n_d11 = int((rec.ts.values >= TAU_PULL).sum())
    rec_d11 = rec[rec.ts.values < TAU_PULL]

    def states(r):
        keepm = np.fromiter((nu in e2.get(sh, ()) for sh, nu in
                             zip(r.show.values, r.number.values)), dtype=bool, count=len(r))
        ep = r[keepm].groupby(["user_idx", "show", "number"], as_index=False)["ts"].min()
        ep = ep.merge(pairs[["row", "user_idx", "show", "tau1", "tau2", "F2"]],
                      on=["user_idx", "show"], how="inner")
        row, ts = ep.row.values, ep.ts.values.astype("float64")
        sA, sH = ts < ep.tau1.values, ts < ep.tau2.values
        nA = np.bincount(row[sA], minlength=n)
        nAH = np.bincount(row[sH], minlength=n)
        isf = ep.number.values == ep.F2.values
        fA = np.bincount(row[sA & isf], minlength=n) > 0
        fH = np.bincount(row[sH & isf], minlength=n) > 0
        started = nA >= 1
        cont_pre = started & fA & (nA >= need)          # pre-amendment, evaluated at tau1
        cont_post = started & fH & (nAH >= need)        # decisions/0034
        return nA, started, cont_pre, cont_post

    nA_d11, st_d11, cpre_d11, cpost_d11 = states(rec_d11)
    nA_raw, st_raw, _, _ = states(rec)

    out = {
        "what": "VALIDATION of the outcome operator against figures already on the record. "
                "Adopts nothing.",
        "instance": "sens_a", "api_calls": 0,
        "population": "waterfall line 5, the 128,099 estimation sample, NO D10",
        "n_pairs": int(n),
        "never_started_without_D11": int((~st_raw).sum()),
        "never_started_with_D11": int((~st_d11).sum()),
        "decisions_0034_SS5_states": {"without_D11": 8445, "with_D11": 8449},
        "never_started_share_pct_with_D11": round(100.0 * int((~st_d11).sum()) / n, 4),
        "decisions_0034_SS2_states_share_pct": 6.5957,
        "pairs_moved_started_and_left_to_continued_by_the_amendment":
            int((cpost_d11 & ~cpre_d11).sum()),
        "decisions_0034_SS2_states_moved": 2246,
        "monotone_no_pair_moves_the_other_way": int((cpre_d11 & ~cpost_d11).sum()) == 0,
        "s2_records_discarded_by_D11": n_d11,
    }
    out["reproduces_never_started"] = (out["never_started_with_D11"] == 8449
                                       and out["never_started_without_D11"] == 8445)
    out["reproduces_moved_count"] = (
        out["pairs_moved_started_and_left_to_continued_by_the_amendment"] == 2246)
    with open(os.path.join(OUT, "crosscheck.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
