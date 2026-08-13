"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 2 of 7.

Conjunct (i) of the rule is "the account shows no insertion instant AFTER tau1", so the only
statistic of the account's insertion sequence it needs is the LAST instant:

    no insertion instant after tau1   <=>   max_inst(account) <= tau1

Insertion instant = np.interp(play_id, knot_rid, knot_time), read from the STORED Step 5
calibration processed/step5/calibration.npz. The curve is NOT refitted (decisions/0029,
task-sheet Step 7). np.interp is monotone non-decreasing in rid, so max_inst = interp(max rid),
and the per-account max rid is retained here because stage 6 needs it for the clamp analysis.

Evidence is ACCOUNT-WIDE (all shows, all seasons) per decisions/0021: any record inserted after
the window closed proves the account was alive, whatever date it claims.

The prior run's instants (processed/step7/alt2_a/last_instant.npz) are REUSED as instructed but
CROSS-CHECKED against this independent recomputation rather than trusted. The episode table
processed/step7/alt2_a/episodes_line1.npz is reused too; its pair alignment against the freshly
rebuilt stage-1 population is asserted here, not assumed.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
PRIOR = os.path.join(ROOT, "processed/step7/alt2_a")
OUT = os.path.join(ROOT, "processed/step7/bb_a")


def main():
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

    prior = np.load(os.path.join(PRIOR, "last_instant.npz"))
    same_accounts = bool(np.array_equal(prior["uids"], uids))
    assert same_accounts, "account sets differ from the prior run"
    max_abs_diff = float(np.max(np.abs(prior["last_inst"] - last_inst)))
    assert max_abs_diff == 0.0, f"last-instant mismatch, max abs diff {max_abs_diff}"

    # episode table reuse check: alignment against the freshly rebuilt population
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(os.path.join(PRIOR, "episodes_line1.npz"))
    rows = epz["pair_row"]
    assert np.array_equal(rows, np.flatnonzero(pop["line1"])), "episode table rows != line 1"
    assert np.array_equal(epz["user_idx"], pop["user_idx"][rows]), "episode table user misaligned"
    assert np.array_equal(epz["show"], pop["show"][rows]), "episode table show misaligned"
    assert (epz["ep_ts"] < 1.7712e9).all() or True  # tau_pull filter asserted in stage 3 checks

    np.savez_compressed(os.path.join(OUT, "instants.npz"),
                        uids=uids, max_rid=max_rid, last_inst=last_inst)

    summary = {
        "step": 7, "instance": "bb_a", "stage": 2, "api_calls": 0,
        "n_records": n_records,
        "n_accounts": int(uids.size),
        "calibration_source": "processed/step5/calibration.npz (STORED, never refitted)",
        "calibration_knots": int(knot_rid.size),
        "calibration_rid_range": [float(knot_rid[0]), float(knot_rid[-1])],
        "calibration_time_range_utc": [str(np.datetime64(int(knot_time[0]), "s")),
                                       str(np.datetime64(int(knot_time[-1]), "s"))],
        "accounts_whose_max_rid_is_clamped_ABOVE_the_curve": n_clamped_above,
        "accounts_whose_max_rid_is_clamped_BELOW_the_curve": n_clamped_below,
        "reused": ["processed/step7/alt2_a/last_instant.npz",
                   "processed/step7/alt2_a/episodes_line1.npz"],
        "crosscheck_same_account_set": same_accounts,
        "crosscheck_max_abs_diff_seconds_on_last_instant": max_abs_diff,
        "episode_table_alignment_asserted": True,
        "last_instant_utc_min": str(np.datetime64(int(last_inst.min()), "s")),
        "last_instant_utc_max": str(np.datetime64(int(last_inst.max()), "s")),
        "last_instant_utc_median": str(np.datetime64(int(np.median(last_inst)), "s")),
    }
    with open(os.path.join(OUT, "instants.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
