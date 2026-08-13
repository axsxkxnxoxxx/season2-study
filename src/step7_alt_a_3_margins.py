"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 3 of 4 — why ALT is empty, and
how far from empty it is.

An exclusion count of zero at ten W arms is either structural or a coincidence, and the
difference matters to the ruling. Three diagnostics:

  1. MARGIN. For every no_after pair, how far below its own tau1 does its earliest canonical
     S2 timestamp sit? If the margin is large, emptiness is robust; if some pair sits a day
     under, it is a knife-edge.
  2. THE MECHANISM. no_after says every insertion instant of the account is <= tau1. A line-4
     pair has S2 evidence by construction (waterfall line 2). So its S2 records were INSERTED
     at or before tau1, and the only way their CLAIMED watched_at can exceed tau1 is
     post-dating - which Step 5 adoption 3 deliberately did not delete. Measured here.
  3. A FINE W SWEEP down to W = 0 and up to W = 400, to find the value of W, if any, at which
     ALT stops being empty.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
A4 = os.path.join(ROOT, "processed/step7/a4")
OUT = os.path.join(ROOT, "processed/step7/alt_a")

SEC_PER_DAY = 86400.0
H_DAYS = 91
TAU_PULL = np.datetime64("2026-08-11T00:00:00", "s").astype("int64").astype(float)


def main():
    epz = np.load(os.path.join(OUT, "episodes_line4.npz"))
    user_idx = epz["user_idx"]
    t0f = epz["t0_floor"]
    ep_row, ep_ts = epz["ep_row"], epz["ep_ts"]
    n = user_idx.size

    di = np.load(os.path.join(A4, "distinct_instants.npz"))
    uids, starts, ends, inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)
    slot = u2slot[user_idx]
    last_inst = inst[ends[slot] - 1]

    # earliest canonical S2 timestamp per pair; +inf where the pair has no in-E2 S2 episode
    min_ts = np.full(n, np.inf)
    np.minimum.at(min_ts, ep_row, ep_ts)
    n_ep = np.bincount(ep_row, minlength=n)
    zero_ep = n_ep == 0

    # ---------------- 1. margin at the adopted W ----------------
    W = 108
    tau1 = t0f + W * SEC_PER_DAY
    keep10 = np.nan_to_num(t0f, nan=np.inf) + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL
    no_after = (last_inst <= tau1) & keep10
    assert int(no_after.sum()) == 751

    marg = (tau1[no_after] - min_ts[no_after]) / SEC_PER_DAY   # days of headroom, >0 => in A
    margins = {
        "n_no_after_pairs": int(no_after.sum()),
        "n_with_no_in_E2_S2_episode": int((no_after & zero_ep).sum()),
        "headroom_days_tau1_minus_earliest_canonical_S2_ts": {
            "min": float(np.min(marg)), "p1": float(np.percentile(marg, 1)),
            "p5": float(np.percentile(marg, 5)), "p25": float(np.percentile(marg, 25)),
            "median": float(np.median(marg)), "p75": float(np.percentile(marg, 75)),
            "max": float(np.max(marg)),
        },
        "n_with_headroom_below_1_day": int((marg < 1).sum()),
        "n_with_headroom_below_30_days": int((marg < 30).sum()),
        "n_with_headroom_below_108_days": int((marg < 108).sum()),
        "interpretation": "every no_after pair's earliest S2 episode predates its own tau1 by "
                          "this many days, so |A| >= 1 for all of them and the ALT conjunction "
                          "is empty; the minimum is the distance to a knife-edge",
    }

    # ---------------- 2. the mechanism: insertion vs claimed time ----------------
    # For each no_after pair the account's last INSERTION instant is <= tau1. Compare the
    # pair's earliest CLAIMED S2 timestamp with the account's last insertion instant.
    li = last_inst[no_after]
    lag = (min_ts[no_after] - li) / SEC_PER_DAY
    mechanism = {
        "n": int(no_after.sum()),
        "n_earliest_S2_claim_after_the_accounts_last_insertion_instant": int((lag > 0).sum()),
        "earliest_S2_claim_minus_last_insertion_instant_days": {
            "min": float(np.min(lag)), "median": float(np.median(lag)),
            "p99": float(np.percentile(lag, 99)), "max": float(np.max(lag)),
        },
        "note": "a value > 0 is a post-dated S2 record - claimed later than it was written. "
                "Step 5 adoption 3 (decisions/0021) deliberately does NOT delete post-dated "
                "records, so this is the only channel through which ALT could ever bite, and "
                "it would additionally have to carry the claim past tau1.",
    }

    # 4 line-4 pairs have zero in-E2 S2 episodes: |A| = 0 at every W. Are they ever no_after?
    zi = np.flatnonzero(zero_ep)
    zero_ep_diag = {
        "n_pairs_with_zero_distinct_in_E2_S2_episodes": int(zi.size),
        "these_have_A_eq_0_at_every_W": True,
        "days_from_their_tau1_at_W108_to_their_accounts_last_insertion_instant": [
            round(float((last_inst[i] - tau1[i]) / SEC_PER_DAY), 2) for i in zi],
        "n_of_them_no_after_at_W108": int(no_after[zi].sum()),
        "note": "these are the only pairs that could satisfy ALT at arbitrarily large W. "
                "A POSITIVE number above means the account kept logging after tau1, so 0021 "
                "rules the pair live and ALT does not fire.",
    }

    # ---------------- 3. fine W sweep ----------------
    sweep = {}
    for Wq in [0, 1, 3, 7, 14, 21, 30, 38, 46, 60, 75, 91, 108, 125, 150, 180,
               213, 250, 300, 350, 400]:
        t1 = t0f + Wq * SEC_PER_DAY
        k10 = (np.nan_to_num(t0f, nan=np.inf)
               + (max(Wq, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL)
        na = (last_inst <= t1) & k10
        selA = ep_ts < t1[ep_row]
        nA = np.bincount(ep_row[selA], minlength=n).astype(np.int64)
        nev = nA == 0
        sweep[str(Wq)] = {
            "post_D10_population": int(k10.sum()),
            "PF_LIMIT_excluded": int(na.sum()),
            "ALT_excluded": int((na & nev).sum()),
            "never_started_pairs": int((k10 & nev).sum()),
        }
        print(f"W={Wq:4d} pop={int(k10.sum()):7d} PF={int(na.sum()):5d} "
              f"ALT={int((na & nev).sum()):4d} never={int((k10 & nev).sum()):6d}")

    out = {
        "step": 7, "instance": "alt_a", "stage": 3, "api_calls": 0,
        "what": "Is ALT's emptiness structural or a knife-edge? EVALUATION ONLY.",
        "margin_at_W108": margins,
        "mechanism": mechanism,
        "zero_episode_pairs": zero_ep_diag,
        "fine_W_sweep_0_to_400": sweep,
        "ALT_empty_at_every_W_tested": all(v["ALT_excluded"] == 0 for v in sweep.values()),
    }
    with open(os.path.join(OUT, "margins.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({k: out[k] for k in
                      ("margin_at_W108", "mechanism", "zero_episode_pairs",
                       "ALT_empty_at_every_W_tested")}, indent=2))


if __name__ == "__main__":
    main()
