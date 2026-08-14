"""Verification support: recompute last_inst from the STORED Step 5 calibration, independently.

The channel count under review turns on ONE primitive that is not an outcome: the account's
last insertion instant. Everything else in the channel predicate (cont, never, t0f) is Step 1
outcome machinery whose recomputation would be a rerun, and a rerun is explicitly not ordered.
This is not a rerun -- it re-derives a single column from processed/step5/full_scan.npz and
processed/step5/calibration.npz and re-counts the channel with it, so the confirmed count does
not rest on processed/step7/bb_a/instants.npz being correct.

The calibration is READ, never refitted (0029). Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
P5 = os.path.join(ROOT, "processed/step5")
BB = os.path.join(ROOT, "processed/step7/bb_a")
OUT = os.path.join(ROOT, "processed/step7/df_a")

SEC_PER_DAY, W, H = 86400.0, 108, 91


def main():
    scan = np.load(os.path.join(P5, "full_scan.npz"))
    user = scan["user"].astype(np.int64)
    rid = scan["rid"].astype(np.float64)

    cal = np.load(os.path.join(P5, "calibration.npz"))
    knot_rid = cal["knot_rid"].astype(np.float64)
    knot_time = cal["knot_time"].astype(np.float64)

    uids = np.unique(user)
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    max_rid = np.full(uids.size, -np.inf)
    np.maximum.at(max_rid, slot[user], rid)
    last_by_account = np.interp(max_rid, knot_rid, knot_time)
    del user, rid

    m = np.load(os.path.join(BB, "masks_W108.npz"))
    pair_user = m["user"]
    last_recomputed = last_by_account[slot[pair_user]]
    last_stored = m["last_inst"]
    max_abs_diff = float(np.max(np.abs(last_recomputed - last_stored)))

    cont, never, t0f = m["cont"], m["never"], m["t0f"]
    tau1 = t0f + W * SEC_PER_DAY
    tau2 = t0f + (W + H) * SEC_PER_DAY

    res = {"what": "channel count re-derived from an independently recomputed last_inst",
           "api_calls": 0, "n_records": int(np.load(os.path.join(P5, 'full_scan.npz'))['user'].size),
           "n_accounts": int(uids.size),
           "max_abs_diff_seconds_vs_stored_last_inst": max_abs_diff,
           "populations": {}}
    for nm, msk in (("APPLY", m["apply_"]), ("DERIV", m["deriv"])):
        for tag, last in (("stored", last_stored), ("recomputed", last_recomputed)):
            ch = int((msk & (~cont) & (~never) & (last > tau1) & (last <= tau2)).sum())
            ex = int((msk & (~cont) & (last <= tau1)).sum())
            res["populations"].setdefault(nm, {})[tag] = {
                "channel_pairs": ch, "alt_broad_exclusions": ex,
                "n_pairs": int(msk.sum())}
        p = res["populations"][nm]
        p["agree"] = p["stored"] == p["recomputed"]
    with open(os.path.join(OUT, "instant_recheck.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
