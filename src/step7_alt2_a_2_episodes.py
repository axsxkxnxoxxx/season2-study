"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 2 of 5.

Builds ONCE the canonical S2 distinct-episode table for every pair on waterfall LINE 1
(201,900, before D10), which is the superset of both populations. Line 4 pairs are a subset,
so DERIV and APPLY are both served by this one table and the record scan runs once.

Rules applied, none of which depend on W:
  - canonical timestamp of a distinct episode = MIN watched_at across its records (Step 1 SS2.2)
  - membership by SET against E2 (SS3.2), never the range 1..F2
  - D11: records with watched_at >= tau_pull are discarded globally
  - MISSING watched_at sentinel rows discarded

|A|, |A_H| and F2-in-A_H at any W are then bincounts over this table, per arm, in stage 3.

Zero API calls.
"""
import json
import os

import numpy as np
import pandas as pd

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
P2 = os.path.join(ROOT, "processed/step2")
OUT = os.path.join(ROOT, "processed/step7/alt2_a")

MISSING = np.iinfo(np.int64).min
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    line1 = pop["line1"]
    rows = np.flatnonzero(line1)
    n = rows.size
    assert n == 201900

    pairs = pd.DataFrame({
        "row": np.arange(n, dtype=np.int64),
        "user_idx": pop["user_idx"][rows],
        "show": pop["show"][rows],
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
    n_missing = int((rec.ts.values == MISSING).sum())
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
        os.path.join(OUT, "episodes_line1.npz"),
        pair_row=rows,                                  # index into pair_revision5 row order
        user_idx=pairs.user_idx.values, show=pairs.show.values,
        L2=pairs.L2.values, F2=pairs.F2.values,
        ep_row=ep.row.values.astype(np.int64),
        ep_ts=ep.ts.values.astype("float64"),
        ep_is_f2=(ep.number.values == ep.F2.values),
        ep_number=ep.number.values.astype(np.int64),
    )

    has_s2 = pop["has_s2"][rows]
    n_ep = np.bincount(ep.row.values, minlength=n)
    summary = {
        "instance": "alt2_a", "stage": 2, "api_calls": 0,
        "line1_pairs": int(n),
        "s2_records_raw": n_raw,
        "s2_records_missing_watched_at": n_missing,
        "s2_records_at_or_after_tau_pull_D11": n_pull,
        "s2_records_dropped_number_not_in_E2": n_out,
        "distinct_episodes_on_line1": int(len(ep)),
        "pairs_with_zero_distinct_in_E2_S2_episodes": int((n_ep == 0).sum()),
        "of_which_flagged_no_S2_evidence_by_step5": int(((n_ep == 0) & ~has_s2).sum()),
        "of_which_step5_says_has_S2_evidence": int(((n_ep == 0) & has_s2).sum()),
        "pairs_flagged_no_S2_evidence_with_nonzero_episodes": int(((n_ep > 0) & ~has_s2).sum()),
    }
    with open(os.path.join(OUT, "episodes_line1.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
