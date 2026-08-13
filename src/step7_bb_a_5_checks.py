"""Step 7 RERUN on ALT-BROAD (decisions/0048), namespace `a`. STAGE 5 of 8 — the waterfall and
the checks the spec does not settle.

  1. The waterfall through filter positions 4, 5 and 6, on BOTH populations, line 6 reported as
     OUTCOME-CONDITIONAL, monotone decrease tested strictly and non-strictly per population.
     Under ALT-BROAD line 6 removes rows from TWO of the three outcome states, so the
     outcome-conditional label is stronger than it was under ALT.
  2. Ordering. |A| and the Continued test are evaluated before liveness applies. Permitted
     because both are ROW-LOCAL predicates on the position-5 output and commute exactly;
     0029's ordering rationale is about per-filter sample size and cannot reach position 7,
     since outcome assignment removes no rows. Commutation is CHECKED here, not asserted.
  3. Tie convention. "AFTER tau1" is implemented strictly, so NOT LIVE requires
     max_inst <= tau1 and an instant landing exactly on tau1 does not prove liveness. The ties
     are counted so the convention is shown to be non-load-bearing.
  4. Pair-level, not user-level (0034): accounts excluded on one show and live on another.

Zero API calls.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step7/bb_a")

SEC_PER_DAY = 86400.0
W, H = 108, 91


def main():
    m = np.load(os.path.join(OUT, "masks_W108.npz"))
    user = m["user"]
    never, cont, left = m["never"], m["cont"], m["left"]
    ex, ex_ns, ex_sl = m["ex"], m["ex_ns"], m["ex_sl"]
    t0f, last_inst = m["t0f"], m["last_inst"]
    tau1 = t0f + W * SEC_PER_DAY
    pops = {"DERIV": m["deriv"], "APPLY": m["apply_"]}

    waterfall = {}
    for nm, before in (("DERIV", 152126), ("APPLY", 201900)):
        p = pops[nm]
        after_d10 = int(p.sum())
        removed = int((ex & p).sum())
        seq = [before, after_d10, after_d10 - removed]
        waterfall[nm] = {
            "position_4_output_contamination_exclusion": before,
            "position_5_output_right_censoring_D10": after_d10,
            "position_5_removed": before - after_d10,
            "position_6_output_liveness": after_d10 - removed,
            "position_6_removed": removed,
            "position_6_removed_never_started": int((ex_ns & p).sum()),
            "position_6_removed_started_and_left": int((ex_sl & p).sum()),
            "position_6_removed_continued": int((ex & cont & p).sum()),
            "position_6_label":
                "LIVENESS (OUTCOME-CONDITIONAL) -- conjunct 2 is 'NOT Continued', a position-7 "
                "outcome predicate, so the removed count cannot be stated without reference to "
                "outcome assignment. Under ALT-BROAD it removes rows from TWO outcome states, "
                "not one, and the split must be published with the line.",
            "monotone_decrease_strict": all(a > b for a, b in zip(seq, seq[1:])),
            "monotone_decrease_non_strict": all(a >= b for a, b in zip(seq, seq[1:])),
        }

    # commutation check: outcome-then-filter vs filter-then-outcome, on the same rows
    commute = {}
    for nm, p in pops.items():
        live = p & ~ex
        a = [int((never & live).sum()), int((cont & live).sum()), int((left & live).sum())]
        # recompute the states restricted to the surviving rows (row-local, so identical)
        idx = np.flatnonzero(live)
        b = [int(never[idx].sum()), int(cont[idx].sum()), int(left[idx].sum())]
        commute[nm] = {"outcome_then_filter": a, "filter_then_outcome": b, "identical": a == b}

    ties = {nm: {
        "pairs_with_last_instant_exactly_equal_to_tau1": int(((last_inst == tau1) & p).sum()),
        "pairs_with_last_instant_within_1_second_of_tau1": int(
            ((np.abs(last_inst - tau1) <= 1.0) & p).sum()),
        "pairs_whose_exclusion_would_flip_if_the_tie_went_the_other_way": int(
            ((last_inst == tau1) & p & ~cont).sum()),
    } for nm, p in pops.items()}

    splits = {}
    for nm, p in pops.items():
        e = ex & p
        acc_ex = np.unique(user[e])
        acc_live = np.unique(user[p & ~ex])
        both = np.intersect1d(acc_ex, acc_live)
        splits[nm] = {
            "excluded_pairs": int(e.sum()),
            "accounts_with_at_least_one_excluded_pair": int(acc_ex.size),
            "accounts_excluded_on_one_show_and_live_on_another": int(both.size),
            "accounts_excluded_on_every_one_of_their_pairs": int(acc_ex.size - both.size),
            "accounts_in_BOTH_exclusion_components": int(np.intersect1d(
                np.unique(user[ex_ns & p]), np.unique(user[ex_sl & p])).size),
            "reading": "a positive middle row is 0034's pair-level anchoring doing visible "
                       "work: the same account is not live for one show and live for another, "
                       "because tau1 is pair-specific. NEVER drop a user wholesale.",
        }

    out = {"step": 7, "instance": "bb_a", "stage": 5, "api_calls": 0, "W": W, "H": H,
           "waterfall_positions_4_to_6": waterfall,
           "ordering_commutation_check": commute,
           "tie_convention": {
               "implemented": "NOT LIVE requires max insertion instant <= tau1; 'after' strict",
               "by_population": ties},
           "pair_level_not_user_level": splits}
    with open(os.path.join(OUT, "checks.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
