"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 2b of 4 — the W arms.

decisions/0044 established that PF-LIMIT has no parameter of its own but is FULLY DETERMINED
BY W: its exclusion set runs 348 -> 949 pairs across the mandated Step 13 arms. This stage
asks the same question of ALT, and asks whether ALT's emptiness at W = 108 is an accident of
the adopted window.

Arms per decisions/0027: the span 46..107 plus 150 and 213; 38, 91 and 108 carried too so the
table lines up with the one in decisions/0044. H is HELD CONSTANT at 91 in every arm.

no_after is computed in closed form rather than by search: with the account's distinct
insertion instants sorted, "no instant after tau1" holds iff the account's LAST instant
is <= tau1. Asserted against the cached W=108 bracketing, which used searchsorted.

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
ARMS = [38, 46, 60, 75, 91, 108, 125, 150, 180, 213]


def main():
    epz = np.load(os.path.join(OUT, "episodes_line4.npz"))
    user_idx = epz["user_idx"]
    L2, F2 = epz["L2"], epz["F2"]
    t0f = epz["t0_floor"]
    ep_row, ep_ts, ep_is_f2 = epz["ep_row"], epz["ep_ts"], epz["ep_is_f2"]
    n = user_idx.size
    need = np.ceil(0.90 * L2).astype(np.int64)

    di = np.load(os.path.join(A4, "distinct_instants.npz"))
    uids, starts, ends, inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)
    slot = u2slot[user_idx]
    assert (slot >= 0).all(), "a pair references an account absent from the sweep"
    last_inst = inst[ends[slot] - 1]
    first_inst = inst[starts[slot]]

    # cross-check the closed form against the cached searchsorted result at W = 108
    br = np.load(os.path.join(A4, "pair_bracketing_W108.npz"))
    tau1_108_all = br["tau1"]
    ref152_all = br["ref152"]
    rows = epz["pair_row"]
    assert bool(ref152_all[rows].all())
    cf = last_inst <= tau1_108_all[rows]
    assert bool((cf == br["no_after"][rows]).all()), "closed form disagrees with searchsorted"
    cb = first_inst > tau1_108_all[rows]
    assert bool((cb == br["no_before"][rows]).all()), "no_before closed form disagrees"

    arms = {}
    for W in ARMS:
        keep10 = np.nan_to_num(t0f, nan=np.inf) + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL
        tau1 = t0f + W * SEC_PER_DAY
        tau2 = t0f + (W + H_DAYS) * SEC_PER_DAY

        selA = ep_ts < tau1[ep_row]
        selH = ep_ts < tau2[ep_row]
        nA = np.bincount(ep_row[selA], minlength=n).astype(np.int64)
        nAH = np.bincount(ep_row[selH], minlength=n).astype(np.int64)
        f2_in_AH = np.bincount(ep_row[selH & ep_is_f2], minlength=n) > 0

        never = nA == 0
        cont = (nA >= 1) & f2_in_AH & (nAH >= need)
        left = (nA >= 1) & ~cont
        assert (never.astype(int) + cont + left == 1).all()

        no_after = last_inst <= tau1
        ex_pf = no_after & keep10
        ex_alt = ex_pf & never
        pop = keep10

        def comp(m):
            return {"pairs": int(m.sum()),
                    "accounts": int(np.unique(user_idx[m]).size),
                    "never_started": int((m & never).sum()),
                    "continued": int((m & cont).sum()),
                    "started_and_left": int((m & left).sum())}

        def sh(live):
            k = int(live.sum())
            c = [int((never & live).sum()), int((cont & live).sum()), int((left & live).sum())]
            return {"pairs": k, "never_started_pct": round(100.0 * c[0] / k, 4),
                    "continued_pct": round(100.0 * c[1] / k, 4),
                    "started_and_left_pct": round(100.0 * c[2] / k, 4),
                    "never_started_n": c[0]}

        s_pf = sh(pop & ~ex_pf)
        s_alt = sh(pop & ~ex_alt)
        s_none = sh(pop)
        k_pf, k_alt = int(ex_pf.sum()), int(ex_alt.sum())
        arms[str(W)] = {
            "W_days": W, "H_days": H_DAYS,
            "post_D10_population": int(pop.sum()),
            "d10_removed_from_152126": int(n - pop.sum()),
            "PF_LIMIT": {"excluded": comp(ex_pf), "shares": s_pf,
                         "bound_ceiling_never_pct": round(
                             100.0 * (s_pf["never_started_n"] + k_pf) /
                             (s_pf["pairs"] + k_pf), 4)},
            "ALT": {"excluded": comp(ex_alt), "shares": s_alt,
                    "bound_ceiling_never_pct": round(
                        100.0 * (s_alt["never_started_n"] + k_alt) /
                        (s_alt["pairs"] + k_alt), 4)},
            "no_filter_shares": s_none,
            "never_started_pairs_in_population": int((pop & never).sum()),
            "pairs_with_zero_distinct_S2_episodes_in_population": int(
                (pop & (np.bincount(ep_row, minlength=n) == 0)).sum()),
        }
        print(f"W={W:4d}  pop={int(pop.sum()):7d}  PF-LIMIT excl={k_pf:5d}  ALT excl={k_alt:4d}")

    out = {
        "step": 7, "instance": "alt_a", "stage": "2b", "api_calls": 0,
        "what": "W-arm coupling of the APPROVED PF-LIMIT and the PROPOSED ALT. "
                "EVALUATION ONLY, adopts nothing.",
        "H_held_constant_days": H_DAYS,
        "arms_source": "decisions/0027 (46..107 plus 150 and 213); 38, 91, 108 added so the "
                       "table lines up with decisions/0044",
        "closed_form_no_after_verified_against_cached_searchsorted_at_W108": True,
        "arms": arms,
    }
    with open(os.path.join(OUT, "arms.json"), "w") as fh:
        json.dump(out, fh, indent=2)


if __name__ == "__main__":
    main()
