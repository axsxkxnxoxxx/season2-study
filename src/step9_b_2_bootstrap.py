"""Step 9, arm `b`, stage 2: the account-clustered bootstrap.

SIX ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE:
  B                = 10,000                       decisions/0103
  seed             = 20260818                     decisions/0103
  resampling unit  = account                      decisions/0103 / 0044
  statistic        = BOTH levels and paired movements   decisions/0118
  resampling frame = every account with >=1 pair in the POSITION-4 output, built ONCE,
                     and DRAWN FOR EVERY QUANTITY regardless of how much it contributes
                                                  decisions/0124
  draw order       = ONE RNG, SEEDED ONCE PER FILE, its stream consumed CONTINUOUSLY, with
                     every quantity evaluated against THE SAME REPLICATE SET; NOT re-seeded
                     per group                    decisions/0124

WHAT decisions/0124 CHANGED IN THIS FILE, and it is a correction rather than a preference.
  BEFORE: the frame was built PER MASK inside `one()` -- 2,422 accounts on APPLY and 2,402 on
  DERIV, the CONTRIBUTING SUBSET -- and the RNG was constructed inside `one()`, so it was
  re-seeded once per group. That solved the order-independence hazard, and the ruling records
  that neither mechanism was wrong; but a per-group restart pairs a between-setting movement
  only WITHIN a group, and the two populations had different `n_acc` and therefore different
  replicate sets. The ruling takes the shared stream because Step 13 varies `W` across eight
  arms and needs between-setting differences paired at the account level.
  AFTER: one frame of 2,481 accounts, built once, and one `multinomial` call whose output is
  the replicate set for all 24 intervals. Reproduction and the measured before/after are in
  src/step9_b_9_frame_repro.py, run record logs/step9_b_frame_repro.txt.

WHY THE FRAME IS NOT THE CONTRIBUTING SUBSET (decisions/0124 SS2). Accounts the censoring rule
excludes are part of the population the uncertainty is ABOUT. Drawing only contributors
conditions the variance on the censoring outcome and treats survivorship as fixed. Measured
here: 59 accounts on APPLY and 79 on DERIV are drawn and contribute zero.

MEMBERSHIP IS NOT SUPPORT (decisions/0124 SS4(1)). `keep_d10` contains `max(W, 91)`, so the
CONTRIBUTING SUBSET moves with `W` even though the DRAWN FRAME does not. Every field below that
declares arm-independence says it describes the DRAW and not the SUPPORT.

ONE FRAME SERVES BOTH POPULATIONS. The position-4 DERIV rows are a subset of the position-4
APPLY rows, so the DERIV accounts (2,471) are a subset of the APPLY accounts (2,481). The frame
is the position-4 output's accounts, 2,481, and the 10 accounts holding no position-4 DERIV pair
are drawn for DERIV and contribute zero -- the same treatment SS2 gives every zero-contributor.
It is also what makes `the SAME replicate set for every quantity` constructible at all: two
frames of different size cannot share one weight matrix.

A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER. Movements are paired WITHIN each
replicate -- the same account weights produce the filtered and the unfiltered level, so the
difference is a paired delta and not a difference of two independently resampled quantities.
"""
import hashlib
import json
import os
import sys

import numpy as np

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step9/b")

B = 10000
SEED = 20260818
LEVEL = 95
LO, HI = 2.5, 97.5

z = np.load(os.path.join(OUT, "pairs.npz"))
pair_user = z["pair_user"]

# ---------------------------------------------------------------------------------------------
# THE FRAME. Built ONCE, from the position-4 output, before any quantity is computed.
# ---------------------------------------------------------------------------------------------
positions = np.load(os.path.join(ROOT, "processed/step8/a/positions.npz"), allow_pickle=True)
scan = np.load(os.path.join(ROOT, "processed/step8/a/scan.npz"), allow_pickle=True)
if not np.array_equal(scan["pair_user"], pair_user):
    sys.exit("HARD STOP: pairs.npz and positions.npz are not on the same row order, so the "
             "position-4 frame cannot be aligned to this arm's masks.")
POS4 = positions["pos4"]
POS4_DERIV = positions["pos4_deriv"]

FRAME_ACCOUNTS = np.unique(pair_user[POS4])
N_FRAME = int(FRAME_ACCOUNTS.size)
ACC_SLOT = np.full(int(pair_user.max()) + 1, -1, dtype=np.int64)
ACC_SLOT[FRAME_ACCOUNTS] = np.arange(N_FRAME)

# ---------------------------------------------------------------------------------------------
# THE DRAW. ONE RNG, seeded once per file, at module scope. ONE multinomial call. The resulting
# replicate set is used by EVERY quantity in this file; nothing below re-seeds and nothing below
# draws again.
# ---------------------------------------------------------------------------------------------
RNG = np.random.default_rng(SEED)
WEIGHTS = RNG.multinomial(N_FRAME, np.full(N_FRAME, 1.0 / N_FRAME), size=B)
REPLICATE_SET_DIGEST = hashlib.sha256(
    np.ascontiguousarray(WEIGHTS, dtype=np.int64).tobytes()).hexdigest()[:16]
W = WEIGHTS.astype(np.float64)

ARMS = {
    "W108_s2_finale": ("never_108", "left_108", "cont_108", "notlive_108"),
    "W91_s2_premiere": ("never_91p", "left_91p", "cont_91p", "notlive_91p"),
}
POPS = {"APPLY": z["pos5"], "DERIV": z["pos5_deriv"]}

STATES = ("never_started", "started_and_left", "continued")

_stored_counts = {}


def one(group, mask, never, left, cont, notlive):
    """Per-account category counts on the FRAME, then the shared B replicates."""
    idx = np.flatnonzero(mask)
    slots = ACC_SLOT[pair_user[idx]]
    if (slots < 0).any():
        sys.exit("HARD STOP: a pair in this population belongs to an account with no position-4 "
                 "pair, so the declared frame is smaller than the support it is drawn for. "
                 "decisions/0124 makes the frame the position-4 accounts; a population reaching "
                 "outside it is a defect in the frame, not something to widen silently.")
    st = np.where(never[idx], 0, np.where(left[idx], 1, 2))
    excl = notlive[idx]

    # counts[frame account, state, {retained, excluded}]. Rows for accounts that contribute
    # nothing to THIS group stay zero: they are drawn, and they contribute zero.
    counts = np.zeros((N_FRAME, 3, 2), dtype=np.float64)
    np.add.at(counts, (slots, st, excl.astype(np.int64)), 1.0)
    _stored_counts[group] = counts

    contributing = int(np.unique(slots).size)

    flat = counts.reshape(N_FRAME, 6)
    agg = (W @ flat).reshape(B, 3, 2)   # THE SHARED REPLICATE SET -- no draw happens here
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
        # THE DRAW. Arm-independent in membership.
        "n_accounts_resampling_frame": N_FRAME,
        # THE SUPPORT. NOT arm-independent: keep_d10 contains max(W, 91).
        "n_accounts_contributing_to_this_group": contributing,
        "n_accounts_drawn_contributing_zero": N_FRAME - contributing,
        "frame_arm_independence": (
            "THE DECLARED FRAME DESCRIBES THE DRAW AND NOT THE SUPPORT (decisions/0124 SS4(1)). "
            "Membership is %d at every arm and on both populations; the contributing subset is "
            "%d here and moves with W, because keep_d10 contains max(W, 91). The %d accounts "
            "drawn with zero contribution are part of the population the uncertainty is about: "
            "they held position-4 pairs, every one removed by D10, so they could have "
            "contributed and did not." % (N_FRAME, contributing, N_FRAME - contributing)),
        "n_pairs_position_5": int(idx.size),
        "n_pairs_post_liveness": int(idx.size - int(excl.sum())),
        "levels_post_liveness_pct": {s: pct(filtered, j) for j, s in enumerate(STATES)},
        "levels_position_5_pct": {s: pct(unfiltered, j) for j, s in enumerate(STATES)},
        "paired_movements_pp": {s: pct(movement, j) for j, s in enumerate(STATES)},
        "movement_sign_stable": {
            s: bool((movement[:, j] > 0).all() or (movement[:, j] < 0).all())
            for j, s in enumerate(STATES)},
    }


res = {"design": {
    "B": B, "seed": SEED, "resampling_unit": "account",
    "statistics": ["levels", "movements"],
    "method": "percentile_bootstrap", "level_pct": LEVEL,
    "resampling_frame": "position_4_accounts",
    "resampling_frame_n": N_FRAME,
    "resampling_frame_note": (
        "EVERY ACCOUNT WITH AT LEAST ONE PAIR IN THE POSITION-4 OUTPUT, BUILT ONCE, AND DRAWN "
        "FOR EVERY QUANTITY REGARDLESS OF HOW MUCH IT CONTRIBUTES (decisions/0124). Not the "
        "contributing subset: accounts the censoring rule excludes are part of the population "
        "the uncertainty is about, and drawing only contributors conditions the variance on the "
        "censoring outcome and treats survivorship as fixed. ONE FRAME SERVES BOTH POPULATIONS "
        "-- the position-4 DERIV rows are a subset of the position-4 APPLY rows -- which is "
        "also what makes a single shared replicate set constructible."),
    "draw_order": "one_rng_seeded_once_per_file_shared_replicate_set",
    "draw_order_note": (
        "ONE RNG, SEEDED ONCE PER FILE AT MODULE SCOPE, its stream consumed CONTINUOUSLY, with "
        "every quantity evaluated against THE SAME REPLICATE SET (decisions/0124). NOT "
        "re-seeded per group. A per-group restart makes a difference between two settings "
        "paired only WITHIN a group; the shared stream is what makes a BETWEEN-SETTING movement "
        "paired at the account level, and Step 13 varies W across eight arms."),
    "replicate_set_digest_sha256_12": REPLICATE_SET_DIGEST,
    "rng_construction_sites_module_level": 1,
    "rng_construction_sites_per_group": 0,
    "multinomial_calls": 1,
    "quantities_sharing_the_replicate_set": len(ARMS) * len(POPS) * 6,
    "movements_are_paired_within_replicate": True,
    "apply_minus_deriv_delta_published": False,
    "apply_minus_deriv_delta_note": (
        "decisions/0124 SS4(2) records that an APPLY-minus-DERIV delta cannot be paired at the "
        "account level under any design where the two populations have different frames. This "
        "file publishes no such delta. Under the frame adopted here the two populations share "
        "ONE frame of %d accounts and one replicate set, so the objection does not bite on this "
        "build; the constraint is recorded for Step 13 regardless, and nothing here crosses it."
        % N_FRAME),
    "all_six_elements_fixed_by_spec": True,
    "elements_fixed_by_spec": ["B", "seed", "resampling_unit", "statistics",
                               "resampling_frame", "draw_order"],
    "source": "decisions/0103; decisions/0118; decisions/0124"}}

for arm, (n, l, c, nl) in ARMS.items():
    res[arm] = {pop: one((arm, pop), m, z[n], z[l], z[c], z[nl]) for pop, m in POPS.items()}

with open(os.path.join(OUT, "stage2_bootstrap.json"), "w") as fh:
    json.dump(res, fh, indent=1)

# THE REPLICATE SET AND THE PER-GROUP COUNT MATRICES, RECORDED so this arm's pairing evidence can
# be RE-TAKEN on the weights that actually produced these endpoints rather than on a rebuild of
# them. processed/ only; never published, and it holds no user identifier -- the account axis is
# a frame slot index and the counts are counts.
np.savez_compressed(
    os.path.join(OUT, "boot_weights.npz"),
    weights=WEIGHTS.astype(np.int16),
    n_frame=np.int64(N_FRAME), B=np.int64(B), seed=np.int64(SEED),
    **{"counts__%s__%s" % g: m for g, m in _stored_counts.items()})

print(json.dumps(res, indent=1))
