"""Step 7 RERUN on the ADOPTED rule (decisions/0046), namespace `a`. STAGE 6 — checks the
spec does not settle, plus the waterfall.

  1. Tie convention. "AFTER tau1" is implemented as inst > tau1, so NOT LIVE requires
     max_inst <= tau1 and an instant landing EXACTLY on tau1 does not prove liveness. Count
     the ties, so the convention is shown to be non-load-bearing rather than asserted to be.
  2. Pair-level, not user-level. Count accounts that are excluded for one show and live for
     another. If that count is positive the pair-level anchoring is doing visible work.
  3. The waterfall through filter positions 4, 5 and 6, on both populations, with line 6
     reported as OUTCOME-CONDITIONAL, and the monotone-decrease invariant tested strictly and
     non-strictly.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/alt2_a")

SEC_PER_DAY = 86400.0
W, H = 108, 91


def main():
    pop = np.load(os.path.join(OUT, "population.npz"))
    epz = np.load(os.path.join(OUT, "episodes_line1.npz"))
    li = np.load(os.path.join(OUT, "last_instant.npz"))
    m = np.load(os.path.join(OUT, "masks_W108.npz"))

    rows = epz["pair_row"]
    user = epz["user_idx"]
    t0f = pop["t0_floor"][rows]
    tau1 = t0f + W * SEC_PER_DAY
    uids, last = li["uids"], li["last_inst"]
    slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    slot[uids] = np.arange(uids.size)
    last_inst = last[slot[user]]

    ex, never = m["ex"], m["never"]
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    ties = {nm: {
        "pairs_with_last_instant_exactly_equal_to_tau1": int(((last_inst == tau1) & p).sum()),
        "pairs_with_last_instant_within_1_second_of_tau1": int(
            ((np.abs(last_inst - tau1) <= 1.0) & p).sum()),
        "pairs_not_live_flip_if_the_tie_went_the_other_way": int(
            ((last_inst == tau1) & p & never).sum()),
    } for nm, p in pops.items()}

    splits = {}
    for nm, p in pops.items():
        e = ex & p
        acc_ex = np.unique(user[e])
        live_pairs = p & ~ex
        acc_live = np.unique(user[live_pairs])
        both = np.intersect1d(acc_ex, acc_live)
        splits[nm] = {
            "accounts_with_at_least_one_excluded_pair": int(acc_ex.size),
            "accounts_excluded_on_one_show_and_live_on_another": int(both.size),
            "accounts_excluded_on_every_one_of_their_pairs": int(acc_ex.size - both.size),
            "excluded_pairs": int(e.sum()),
            "reading": "a positive middle row is the pair-level anchoring (0034) doing "
                       "visible work: the same account is not live for one show and live "
                       "for another, because tau1 is pair-specific",
        }

    waterfall = {}
    for nm, before, after_d10 in (("DERIV", 152126, int(pops["DERIV"].sum())),
                                  ("APPLY", 201900, int(pops["APPLY"].sum()))):
        removed = int((ex & pops[nm]).sum())
        seq = [before, after_d10, after_d10 - removed]
        waterfall[nm] = {
            "position_4_output_contamination_exclusion": before,
            "position_5_output_right_censoring_D10": after_d10,
            "position_5_removed": before - after_d10,
            "position_6_output_liveness": after_d10 - removed,
            "position_6_removed": removed,
            "position_6_label": "LIVENESS (OUTCOME-CONDITIONAL) — removes only pairs whose "
                                "outcome is Never started, since |A| = 0 is the second "
                                "conjunct; the removed count cannot be stated without "
                                "reference to the position-7 outcome condition",
            "monotone_decrease_strict": all(a > b for a, b in zip(seq, seq[1:])),
            "monotone_decrease_non_strict": all(a >= b for a, b in zip(seq, seq[1:])),
        }

    out = {"step": 7, "instance": "alt2_a", "stage": 6, "api_calls": 0,
           "W": W, "H": H,
           "tie_convention": {
               "implemented": "NOT LIVE iff max insertion instant <= tau1; 'after' is strict",
               "by_population": ties},
           "pair_level_not_user_level": splits,
           "waterfall_positions_4_to_6": waterfall}
    with open(os.path.join(OUT, "checks.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
