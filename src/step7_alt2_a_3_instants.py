"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 3 of 5.

The rule's first conjunct is "the account shows no insertion instant AFTER tau1", so the only
statistic of the account's insertion sequence the rule needs is its LAST instant:

    no insertion instant after tau1   <=>   max_inst(account) <= tau1

Insertion instant = np.interp(play_id, knot_rid, knot_time) read from the STORED Step 5
calibration at processed/step5/calibration.npz. The curve is NOT refitted (task-sheet Step 7,
decisions/0029). np.interp is monotone non-decreasing in rid, so max_inst = interp(max rid).

The account-level insertion sequence built for the earlier runs
(processed/step7/a4/distinct_instants.npz) is REUSED as instructed, but it is CROSS-CHECKED
here against this independent recomputation rather than trusted.

Evidence is ACCOUNT-WIDE (all shows, all seasons) per decisions/0021 gate 2 of 5: any record
inserted after the window closed proves the account was alive, whatever date it claims.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
A4 = os.path.join(ROOT, "processed/step7/a4")
OUT = os.path.join(ROOT, "processed/step7/alt2_a")


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
    del user, rid

    # cross-check against the reused a4 sequence
    di = np.load(os.path.join(A4, "distinct_instants.npz"))
    a4_uids, a4_ends, a4_inst = di["uids"], di["ends"], di["inst"]
    same_accounts = bool(np.array_equal(np.sort(a4_uids), uids))
    a4_last = a4_inst[a4_ends - 1]
    order = np.argsort(a4_uids)
    max_abs_diff = float(np.max(np.abs(a4_last[order] - last_inst))) if same_accounts else None

    assert same_accounts, "account sets differ between the a4 sequence and this recomputation"
    assert max_abs_diff == 0.0, f"last-instant mismatch, max abs diff {max_abs_diff}"

    np.savez_compressed(os.path.join(OUT, "last_instant.npz"),
                        uids=uids, last_inst=last_inst)

    summary = {
        "instance": "alt2_a", "stage": 3, "api_calls": 0,
        "n_records": n_records,
        "n_accounts": int(uids.size),
        "calibration_source": "processed/step5/calibration.npz (STORED, not refitted)",
        "calibration_knots": int(knot_rid.size),
        "reused_sequence": "processed/step7/a4/distinct_instants.npz",
        "crosscheck_same_account_set": same_accounts,
        "crosscheck_max_abs_diff_seconds_on_last_instant": max_abs_diff,
        "last_instant_utc_min": str(np.datetime64(int(last_inst.min()), "s")),
        "last_instant_utc_max": str(np.datetime64(int(last_inst.max()), "s")),
        "last_instant_utc_median": str(np.datetime64(int(np.median(last_inst)), "s")),
    }
    with open(os.path.join(OUT, "last_instant.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
