"""Step 7 gate-closing sensitivity test (decisions/0041 SS4), instance namespace `a`.

STAGE 2 of 4 — outcome inputs, per Step 1 SS7 as amended by decisions/0034.

For every pair in the post-D10 population computes, from episode-level history only
(no drop flag exists — it is OAuth Required):

  |A|      distinct S2 episodes whose number is in E2 and whose CANONICAL timestamp
           (SS2.2, the MINIMUM watched_at across that episode's records) satisfies
           watched_at < tau1,  tau1 = [[T0]] + 108*24h
  |A_H|    the same set recomputed at tau2 = [[T0]] + (108+91)*24h = [[T0]] + 199 days
  F2 in A_H   whether the S2 finale episode number is in A_H
  m_H      max(A_H), for context only

Boundary tests are the half-open UTC-instant form (SS2.4). `date(watched_at) <= T1`
appears nowhere. Membership is by SET against E2, never by the range 1..F2.
D11 (records at or after tau_pull are discarded globally) is applied and its bite reported.

Outcome assignment itself is done in stage 3, since it is cheap and the liveness filter
is what varies.

This is NOT the Step 9 deliverable. Step 8 has not launched and is an unapproved gate.

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


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    ref = pop["ref"]
    rows = np.flatnonzero(ref)
    n = rows.size

    pairs = pd.DataFrame({
        "row": np.arange(n, dtype=np.int64),
        "user_idx": pop["user_idx"][rows].astype(np.int64),
        "show": pop["show"][rows].astype(np.int64),
        "tau1": pop["tau1"][rows],
        "tau2": pop["tau2"][rows],
    })
    assert not pairs.duplicated(["user_idx", "show"]).any(), "duplicate user-show pair"

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
    pairs["need"] = np.ceil(0.90 * pairs.L2.values).astype(np.int64)

    # ------------------------------------------------------ S2 episode records
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
    n_s2_raw = len(rec)

    n_missing_ts = int((rec.ts.values == MISSING).sum())
    rec = rec[rec.ts.values != MISSING]

    # D11: the global frozen cutoff. Records at or after tau_pull are discarded everywhere.
    n_at_or_past_pull = int((rec.ts.values >= TAU_PULL).sum())
    rec = rec[rec.ts.values < TAU_PULL]

    # set membership against E2 (SS3.2). Never the range 1..F2.
    in_e2 = np.fromiter(
        (nu in e2.get(sh, ()) for sh, nu in zip(rec.show.values, rec.number.values)),
        dtype=bool, count=len(rec))
    n_out_of_set = int((~in_e2).sum())
    rec = rec[in_e2]

    # canonical timestamp of a distinct episode = MIN watched_at across its records (SS2.2)
    ep = rec.groupby(["user_idx", "show", "number"], as_index=False)["ts"].min()
    n_distinct_ep_all = len(ep)
    del rec

    # ------------------------------------------------------ restrict to the population
    ep = ep.merge(pairs[["row", "user_idx", "show", "tau1", "tau2", "F2"]],
                  on=["user_idx", "show"], how="inner")
    row = ep.row.values
    ts = ep.ts.values.astype("float64")

    selA = ts < ep.tau1.values
    selH = ts < ep.tau2.values
    assert bool((selA & ~selH).sum() == 0), "A must be a subset of A_H (tau1 < tau2)"

    nA = np.bincount(row[selA], minlength=n).astype(np.int64)
    nAH = np.bincount(row[selH], minlength=n).astype(np.int64)
    isF2 = ep.number.values == ep.F2.values
    f2_in_AH = np.bincount(row[selH & isF2], minlength=n) > 0
    f2_in_A = np.bincount(row[selA & isF2], minlength=n) > 0

    mH = np.zeros(n, dtype=np.int64)
    np.maximum.at(mH, row[selH], ep.number.values[selH])

    assert (nA <= nAH).all(), "|A| <= |A_H| violated"
    assert (nAH <= pairs.L2.values).all(), "|A_H| <= L2 violated (set-membership check)"

    np.savez_compressed(
        os.path.join(OUT, "outcome_inputs.npz"),
        row=np.arange(n, dtype=np.int64),
        pair_row_index=rows,                 # index into the full pair_revision5 row order
        nA=nA, nAH=nAH, f2_in_AH=f2_in_AH, f2_in_A=f2_in_A, mH=mH,
        L2=pairs.L2.values, need=pairs.need.values,
    )

    summary = {
        "step": 7,
        "what": "GATE-CLOSING SENSITIVITY DIAGNOSTIC for Step 7 (decisions/0041 SS4). "
                "NOT the Step 9 deliverable. Step 8 has not launched.",
        "instance": "sens_a",
        "api_calls": 0,
        "population_pairs": int(n),
        "s2_records_raw": n_s2_raw,
        "s2_records_missing_ts": n_missing_ts,
        "s2_records_at_or_after_tau_pull_D11": n_at_or_past_pull,
        "s2_records_dropped_number_not_in_E2": n_out_of_set,
        "s2_distinct_episodes_all_accounts": n_distinct_ep_all,
        "s2_distinct_episodes_in_population": int(len(ep)),
        "canonical_timestamp_rule": "min watched_at across the distinct episode's records (SS2.2)",
        "boundary_form": "half-open UTC instant, watched_at < tau",
        "d11_bite_on_this_population": {
            "note": "D10 guarantees tau2 <= tau_pull for every retained pair, so a record at "
                    "or after tau_pull cannot enter A or A_H regardless; the count is the "
                    "global one, reported so the filter is visible rather than assumed inert",
            "records_discarded_globally": n_at_or_past_pull,
        },
        "nA_zero_pairs": int((nA == 0).sum()),
        "nAH_zero_pairs": int((nAH == 0).sum()),
        "pairs_where_A_smaller_than_AH": int((nA < nAH).sum()),
        "A_subset_AH_invariant_holds": True,
    }
    with open(os.path.join(OUT, "outcome_inputs.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
