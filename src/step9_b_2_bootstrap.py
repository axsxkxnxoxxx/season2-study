"""Step 9, arm `b`, stage 2: the account-clustered bootstrap.

ALL FOUR ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE:
  B                = 10,000                       decisions/0103
  seed             = 20260818                     decisions/0103
  resampling unit  = account                      decisions/0103 / 0044
  statistic        = BOTH levels and paired movements   decisions/0118

A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER. Movements are paired
WITHIN each replicate -- the same account weights produce the filtered and the
unfiltered level, so the difference is a paired delta and not a difference of two
independently resampled quantities.
"""
import json
import os

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step9/b")

B = 10000
SEED = 20260818
LEVEL = 95
LO, HI = 2.5, 97.5

z = np.load(os.path.join(OUT, "pairs.npz"))
pair_user = z["pair_user"]

ARMS = {
    "W108_s2_finale": ("never_108", "left_108", "cont_108", "notlive_108"),
    "W91_s2_premiere": ("never_91p", "left_91p", "cont_91p", "notlive_91p"),
}
POPS = {"APPLY": z["pos5"], "DERIV": z["pos5_deriv"]}

STATES = ("never_started", "started_and_left", "continued")


def one(mask, never, left, cont, notlive):
    """Per-account category counts, then B account-clustered replicates."""
    idx = np.flatnonzero(mask)
    users = pair_user[idx]
    uacc, upos = np.unique(users, return_inverse=True)
    n_acc = uacc.size
    st = np.where(never[idx], 0, np.where(left[idx], 1, 2))
    excl = notlive[idx]

    # counts[account, state, {retained, excluded}]
    counts = np.zeros((n_acc, 3, 2), dtype=np.float64)
    np.add.at(counts, (upos, st, excl.astype(np.int64)), 1.0)

    rng = np.random.default_rng(SEED)
    w = rng.multinomial(n_acc, np.full(n_acc, 1.0 / n_acc), size=B).astype(np.float64)

    flat = counts.reshape(n_acc, 6)
    agg = w @ flat                      # (B, 6)
    agg = agg.reshape(B, 3, 2)
    ret = agg[:, :, 0]
    exc = agg[:, :, 1]
    tot_all = (ret + exc).sum(axis=1)
    tot_ret = ret.sum(axis=1)

    unfiltered = 100.0 * (ret + exc) / tot_all[:, None]     # position-5 levels
    filtered = 100.0 * ret / tot_ret[:, None]               # post-liveness levels
    movement = filtered - unfiltered                        # PAIRED within replicate

    def pct(a, j):
        lo, hi = np.percentile(a[:, j], [LO, HI])
        return {"lower": float(lo), "upper": float(hi), "width_pp": float(hi - lo)}

    return {
        "n_accounts": int(n_acc),
        "n_pairs_position_5": int(idx.size),
        "n_pairs_post_liveness": int(idx.size - int(excl.sum())),
        "levels_post_liveness_pct": {s: pct(filtered, j) for j, s in enumerate(STATES)},
        "levels_position_5_pct": {s: pct(unfiltered, j) for j, s in enumerate(STATES)},
        "paired_movements_pp": {s: pct(movement, j) for j, s in enumerate(STATES)},
        "movement_sign_stable": {
            s: bool((movement[:, j] > 0).all() or (movement[:, j] < 0).all())
            for j, s in enumerate(STATES)},
    }


res = {"design": {"B": B, "seed": SEED, "resampling_unit": "account",
                  "statistics": ["levels", "movements"],
                  "method": "percentile_bootstrap", "level_pct": LEVEL,
                  "rng": "numpy default_rng, re-seeded identically for every group so the "
                         "result does not depend on the order the groups are computed in",
                  "movements_are_paired_within_replicate": True,
                  "all_four_elements_fixed_by_spec": True,
                  "source": "decisions/0103; decisions/0118"}}
for arm, (n, l, c, nl) in ARMS.items():
    res[arm] = {pop: one(m, z[n], z[l], z[c], z[nl]) for pop, m in POPS.items()}

with open(os.path.join(OUT, "stage2_bootstrap.json"), "w") as fh:
    json.dump(res, fh, indent=1)
print(json.dumps(res, indent=1))
