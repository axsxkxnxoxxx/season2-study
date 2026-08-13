"""Step 7 ALTERNATIVE-RULE EVALUATION, namespace `a`.  STAGE 3b of 4.

Stage 3 left two things unresolved and both bear on whether ALT's emptiness is structural:

  1. Four line-4 pairs have ZERO distinct in-E2 S2 episodes, so |A| = 0 at EVERY W, and their
     accounts' last insertion instant sits at about T0 - so the closed form makes them
     no_after. Yet ALT excluded none of them. The suspect is D10 right-censoring at filter
     position 5, which runs BEFORE liveness at position 6 (decisions/0029). Confirm or refute.
  2. ALT fires 6 pairs at W = 0 and none at W >= 1. W = 0 is not a tested arm - Step 13's span
     is 46..107 plus 150 and 213 (decisions/0027) - but it shows the emptiness is an empirical
     fact over a range, not a theorem.

So: recompute the ALT candidate count on line 4 with D10 SUPPRESSED, at every arm, and
attribute the difference. If D10 is carrying the emptiness, ALT's exclusion set depends on
tau_pull as well as W, and that is a coupling the ruling needs to see.

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
ARMS = [0, 1, 7, 30, 38, 46, 60, 75, 91, 108, 125, 150, 180, 213, 300, 400]


def main():
    epz = np.load(os.path.join(OUT, "episodes_line4.npz"))
    user_idx, t0f = epz["user_idx"], epz["t0_floor"]
    ep_row, ep_ts = epz["ep_row"], epz["ep_ts"]
    n = user_idx.size

    di = np.load(os.path.join(A4, "distinct_instants.npz"))
    uids, starts, ends, inst = di["uids"], di["starts"], di["ends"], di["inst"]
    u2slot = np.full(int(uids.max()) + 1, -1, dtype=np.int64)
    u2slot[uids] = np.arange(uids.size)
    last_inst = inst[ends[u2slot[user_idx]] - 1]

    n_ep = np.bincount(ep_row, minlength=n)
    zero_ep = n_ep == 0

    rows = {}
    for W in ARMS:
        t1 = t0f + W * SEC_PER_DAY
        k10 = (np.nan_to_num(t0f, nan=np.inf)
               + (max(W, 91) + H_DAYS) * SEC_PER_DAY <= TAU_PULL)
        na_raw = last_inst <= t1
        selA = ep_ts < t1[ep_row]
        nev = np.bincount(ep_row[selA], minlength=n) == 0
        cand_raw = na_raw & nev            # ALT candidates BEFORE D10
        cand_d10 = cand_raw & k10          # ALT exclusions AFTER D10, the operative set
        rows[str(W)] = {
            "ALT_candidates_on_line4_before_D10": int(cand_raw.sum()),
            "of_which_removed_by_D10": int((cand_raw & ~k10).sum()),
            "ALT_exclusions_after_D10_OPERATIVE": int(cand_d10.sum()),
            "of_the_candidates_how_many_have_zero_in_E2_S2_episodes": int(
                (cand_raw & zero_ep).sum()),
            "PF_LIMIT_candidates_before_D10": int(na_raw.sum()),
            "PF_LIMIT_after_D10": int((na_raw & k10).sum()),
        }
        r = rows[str(W)]
        print(f"W={W:4d}  ALT pre-D10={r['ALT_candidates_on_line4_before_D10']:5d} "
              f"-> post-D10={r['ALT_exclusions_after_D10_OPERATIVE']:4d}   "
              f"PF pre={r['PF_LIMIT_candidates_before_D10']:5d} "
              f"-> post={r['PF_LIMIT_after_D10']:5d}")

    # the four zero-episode pairs, tracked explicitly
    zi = np.flatnonzero(zero_ep)
    track = []
    for i in zi:
        t1_108 = t0f[i] + 108 * SEC_PER_DAY
        k10_108 = t0f[i] + (108 + H_DAYS) * SEC_PER_DAY <= TAU_PULL
        track.append({
            "T0_floor_utc": str(np.datetime64(int(t0f[i]), "s")),
            "account_last_insertion_instant_utc": str(np.datetime64(int(last_inst[i]), "s")),
            "days_last_insertion_minus_T0": round(
                float((last_inst[i] - t0f[i]) / SEC_PER_DAY), 3),
            "no_after_at_W108_ignoring_D10": bool(last_inst[i] <= t1_108),
            "survives_D10_at_W108": bool(k10_108),
        })

    out = {
        "step": 7, "instance": "alt_a", "stage": "3b", "api_calls": 0,
        "what": "Is D10 right-censoring, not the rule, what makes ALT empty? EVALUATION ONLY.",
        "filter_order": "decisions/0029: ... 5. right-censoring -> 6. liveness -> "
                        "7. outcome assignment. D10 runs BEFORE liveness, so a pair D10 "
                        "removes is never offered to the liveness rule at all.",
        "by_arm": rows,
        "the_four_zero_episode_pairs": track,
        "verdict": None,
    }
    pre = {k: v["ALT_candidates_on_line4_before_D10"] for k, v in rows.items()}
    post = {k: v["ALT_exclusions_after_D10_OPERATIVE"] for k, v in rows.items()}
    out["verdict"] = {
        "ALT_candidates_before_D10_range": [min(pre.values()), max(pre.values())],
        "ALT_exclusions_after_D10_range": [min(post.values()), max(post.values())],
        "D10_is_load_bearing_for_ALT_emptiness": any(
            pre[k] > 0 and post[k] == 0 for k in rows),
        "arms_where_D10_is_load_bearing": [k for k in rows
                                           if pre[k] > 0 and post[k] == 0],
    }
    with open(os.path.join(OUT, "d10_attribution.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps({"the_four_zero_episode_pairs": track,
                      "verdict": out["verdict"]}, indent=2))


if __name__ == "__main__":
    main()
