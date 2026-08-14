"""Step 7 RERUN on ALT-MATCHED (decisions/0052), namespace `a`. STAGE 2 — insertion instants.

The rule reads the account's insertion sequence at TWO instants now, not one:

    no insertion instant after tau1   <=>   max_inst(account) <= tau1     (never-started null)
    no insertion instant after tau2   <=>   max_inst(account) <= tau2     (started-and-left null)

Both are statistics of the SAME single number, the account's last insertion instant, so nothing
new has to be computed relative to ALT-BROAD; only the threshold it is compared against changes,
per null.

Insertion instant = np.interp(play_id, knot_rid, knot_time) against the STORED Step 5
calibration processed/step5/calibration.npz. The curve is READ, NEVER REFITTED (0029). np.interp
is monotone non-decreasing in rid, so max_inst = interp(max rid).

Evidence is ACCOUNT-WIDE (all shows, all seasons) per 0021; the TEST is pair-level per 0034.

REUSE + CROSS-CHECK, as instructed: the prior namespace-`a` run's stored instants are loaded and
compared against a full independent recomputation from processed/step5/full_scan.npz.

Zero API calls.
"""
import json
import os
import time

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
PRIOR = os.path.join(ROOT, "processed/step7/bb_a")
EPZ = os.path.join(ROOT, "processed/step7/alt2_a/episodes_line1.npz")
OUT = os.path.join(ROOT, "processed/step7/mm_a")


def main():
    t = time.time()
    scan = np.load(os.path.join(P5, "full_scan.npz"))
    user = scan["user"].astype(np.int64)
    rid = scan["rid"].astype(np.float64)
    n_records = int(user.size)
    assert n_records == 27656813, f"unexpected record count {n_records}"

    cal = np.load(os.path.join(P5, "calibration.npz"))
    knot_rid = cal["knot_rid"].astype(np.float64)
    knot_time = cal["knot_time"].astype(np.float64)
    assert np.all(np.diff(knot_rid) > 0), "knots not strictly increasing in rid"
    assert np.all(np.diff(knot_time) >= 0), "calibration not monotone in time"

    uids = np.unique(user)
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    max_rid = np.full(uids.size, -np.inf)
    np.maximum.at(max_rid, slot[user], rid)
    last_inst = np.interp(max_rid, knot_rid, knot_time)
    n_clamped_above = int((max_rid > knot_rid[-1]).sum())
    n_clamped_below = int((max_rid < knot_rid[0]).sum())
    del user, rid

    prior = np.load(os.path.join(PRIOR, "instants.npz"))
    same_accounts = bool(np.array_equal(prior["uids"], uids))
    assert same_accounts, "account sets differ from the prior namespace-a run"
    d_rid = float(np.max(np.abs(prior["max_rid"] - max_rid)))
    d_inst = float(np.max(np.abs(prior["last_inst"] - last_inst)))
    assert d_rid == 0.0 and d_inst == 0.0, f"instant mismatch: {d_rid} {d_inst}"

    # episode table reuse: alignment against the freshly rebuilt stage-1 population, asserted
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(EPZ)
    rows = epz["pair_row"]
    assert np.array_equal(rows, np.flatnonzero(pop["line1"])), "episode table rows != line 1"
    assert np.array_equal(epz["user_idx"], pop["user_idx"][rows]), "episode table user misaligned"
    assert np.array_equal(epz["show"], pop["show"][rows]), "episode table show misaligned"

    np.savez_compressed(os.path.join(OUT, "instants.npz"),
                        uids=uids, max_rid=max_rid, last_inst=last_inst)

    summary = {
        "step": 7, "instance": "mm_a", "stage": 2, "api_calls": 0,
        "n_records": n_records,
        "n_accounts": int(uids.size),
        "calibration_source": "processed/step5/calibration.npz (STORED, never refitted)",
        "calibration_knots": int(knot_rid.size),
        "calibration_rid_range": [float(knot_rid[0]), float(knot_rid[-1])],
        "calibration_time_range_utc": [str(np.datetime64(int(knot_time[0]), "s")),
                                       str(np.datetime64(int(knot_time[-1]), "s"))],
        "accounts_whose_max_rid_is_clamped_ABOVE_the_curve": n_clamped_above,
        "accounts_whose_max_rid_is_clamped_BELOW_the_curve": n_clamped_below,
        "reuse_and_crosscheck": {
            "reused": "processed/step7/bb_a/instants.npz (namespace a, ALT-BROAD run)",
            "recomputed_independently_from": "processed/step5/full_scan.npz",
            "same_account_set": same_accounts,
            "max_abs_diff_max_rid": d_rid,
            "max_abs_diff_last_instant_seconds": d_inst,
        },
        "episode_table_reused": EPZ,
        "episode_table_alignment_asserted": True,
        "last_instant_utc_min": str(np.datetime64(int(last_inst.min()), "s")),
        "last_instant_utc_max": str(np.datetime64(int(last_inst.max()), "s")),
        "last_instant_utc_median": str(np.datetime64(int(np.median(last_inst)), "s")),
        "seconds_elapsed": round(time.time() - t, 1),
    }
    with open(os.path.join(OUT, "instants.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
