"""Step 9, arm `b`, stage 2: the account-clustered bootstrap.

SEVEN ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE:
  B                = 10,000                       decisions/0103
  seed             = 20260818                     decisions/0103
  resampling unit  = account                      decisions/0103 / 0044
  statistic        = BOTH levels and paired movements   decisions/0118
  resampling frame = every account with >=1 pair in the POSITION-4 OUTPUT, built ONCE,
                     and DRAWN FOR EVERY QUANTITY regardless of how much it contributes
                                                  decisions/0124
  draw order       = ONE RNG, SEEDED ONCE PER FILE, its stream consumed CONTINUOUSLY, with
                     every quantity evaluated against THE SAME REPLICATE SET; NOT re-seeded
                     per group                    decisions/0124
  draw mechanism   = numpy.random.default_rng; the call
                     `rng.integers(0, n_frame, size=(m, n_frame))`; and WEIGHTS FORMED BY
                     COUNTING THE DRAWN INDICES  decisions/0125

WHAT decisions/0124 CHANGED IN THIS FILE, and it is a correction rather than a preference.
  BEFORE: the frame was built PER MASK inside `one()` -- 2,422 accounts on APPLY and 2,402 on
  DERIV, the CONTRIBUTING SUBSET -- and the RNG was constructed inside `one()`, so it was
  re-seeded once per group. That solved the order-independence hazard, and the ruling records
  that neither mechanism was wrong; but a per-group restart pairs a between-setting movement
  only WITHIN a group, and the two populations had different `n_acc` and therefore different
  replicate sets. The ruling takes the shared stream because Step 13 varies `W` across eight
  arms and needs between-setting differences paired at the account level.
  AFTER: one frame of 2,481 accounts, built once, and one RNG whose draw is the replicate set
  for all 24 intervals. Reproduction and the measured before/after are in
  src/step9_b_9_frame_repro.py, run record logs/step9_b_frame_repro.txt.

WHAT decisions/0125 CHANGED IN THIS FILE, one level below decisions/0124.
  BEFORE: the draw was `RNG.multinomial(N_FRAME, np.full(N_FRAME, 1/N_FRAME), size=B)`. That
  satisfied decisions/0124 LITERALLY -- one RNG at module scope, seeded once, one call, the
  matrix shared by every group -- AND STILL DREW A DIFFERENT REPLICATE SET, because `integers`
  and `multinomial` are different samplers over the same distribution and consume the stream
  differently. Same seed, same frame, same B, different draws: the distribution is right in
  both, the realisation is not the same, and an unfixed mechanism makes the fixed seed
  decorative in exactly the way decisions/0124 said an unfixed draw order does.
  AFTER: the four elements decisions/0125 SS1 names and nothing else -- the generator
  `numpy.random.default_rng`, the seed 20260818, the call
  `rng.integers(0, n_frame, size=(m, n_frame))`, and weights formed by COUNTING THE DRAWN
  INDICES. Reproduction against the committed source is in src/step9_b_15_mechanism_repro.py,
  run record logs/step9_b_mechanism_repro.txt.

THE CHUNKING IS DELIBERATELY NOT PART OF THE SPEC (decisions/0125 SS3), so the `CHUNK` below is
THIS FILE'S CHOICE and not a spec element. It is a memory bound and nothing else: measured under
one seed on n_frame = 2,481, CHUNK 200, CHUNK 500 and a single call give IDENTICAL arrays. A
spec element earns its place by determining the output, and this one does not. The measurement
is re-taken every run by src/step9_b_15_mechanism_repro.py rather than taken on trust here.

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
# THE DRAW. ONE RNG, seeded once per file, at module scope (decisions/0124), drawing ACCOUNT
# INDICES with `rng.integers(0, n_frame, size=(m, n_frame))` and forming the weights by COUNTING
# THE DRAWN INDICES (decisions/0125). The resulting replicate set is used by EVERY quantity in
# this file; nothing below re-seeds and nothing below draws again.
#
# CHUNK is NOT a spec element (decisions/0125 SS3) -- it bounds memory and does not determine the
# output. The stream is consumed CONTINUOUSLY across the chunks: one RNG, drawn from repeatedly,
# never restarted.
# ---------------------------------------------------------------------------------------------
CHUNK = 500
RNG = np.random.default_rng(SEED)
WEIGHTS = np.empty((B, N_FRAME), dtype=np.int32)
_done = 0
while _done < B:
    _m = min(CHUNK, B - _done)
    _idx = RNG.integers(0, N_FRAME, size=(_m, N_FRAME))
    _off = (np.arange(_m) * N_FRAME)[:, None]
    WEIGHTS[_done:_done + _m] = np.bincount((_idx + _off).ravel(),
                                            minlength=_m * N_FRAME).reshape(_m, N_FRAME)
    _done += _m
# Counting n_frame drawn indices per replicate must give a row total of exactly n_frame. This is
# a property of the CONSTRUCTION, so it cannot fail on a wrong seed or a wrong frame and is NOT
# offered as a check on either (decisions/0123 SS3): it is here only to catch a counting error.
if not (WEIGHTS.sum(axis=1) == N_FRAME).all():
    sys.exit("HARD STOP: a replicate's weights do not sum to n_frame, so the drawn indices were "
             "not counted correctly.")
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
    "draw_mechanism": "default_rng__integers_account_indices__weights_by_counting",
    "draw_mechanism_note": (
        "THE GENERATOR IS numpy.random.default_rng, THE CALL IS "
        "`rng.integers(0, n_frame, size=(m, n_frame))`, AND THE WEIGHTS ARE FORMED BY COUNTING "
        "THE DRAWN INDICES (decisions/0125). Those four things are the spec and nothing else "
        "is. This file previously drew with `multinomial`, which satisfied decisions/0124 "
        "literally -- one RNG, seeded once, one call, one shared matrix -- and still produced a "
        "DIFFERENT replicate set, because the two samplers consume the stream differently. The "
        "distribution was right either way; the realisation was not the same, and an unfixed "
        "mechanism makes a fixed seed decorative. THE CHUNKING IS NOT A SPEC ELEMENT: CHUNK "
        "200, CHUNK 500 and a single call give identical arrays under one seed, and a spec "
        "element earns its place by determining the output."),
    "chunking_is_this_files_choice_not_a_spec_element": True,
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
    "rng_draw_calls": (B + CHUNK - 1) // CHUNK,
    "rng_draw_calls_note": (
        "THE NUMBER OF `integers` CALLS, MEASURED, NOT ONE. The stream is consumed CONTINUOUSLY "
        "across them from a single RNG that is never restarted, and decisions/0125 SS3 records "
        "that the chunking does not determine the output -- CHUNK 200, CHUNK 500 and a single "
        "call give identical arrays under one seed. It is reported rather than rounded to 1 "
        "because `one call` would be false, and a field that is false in an easy place is not "
        "trusted in a hard one."),
    "chunk_size_this_file_used": CHUNK,
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
    "all_seven_elements_fixed_by_spec": True,
    "elements_fixed_by_spec": ["B", "seed", "resampling_unit", "statistics",
                               "resampling_frame", "draw_order", "draw_mechanism"],
    "source": "decisions/0103; decisions/0118; decisions/0124; decisions/0125"}}

for arm, (n, l, c, nl) in ARMS.items():
    res[arm] = {pop: one((arm, pop), m, z[n], z[l], z[c], z[nl]) for pop, m in POPS.items()}

with open(os.path.join(OUT, "stage2_bootstrap.json"), "w") as fh:
    json.dump(res, fh, indent=1)

# THE REPLICATE SET AND THE PER-GROUP COUNT MATRICES, RECORDED so this arm's pairing evidence can
# be RE-TAKEN on the weights that actually produced these endpoints rather than on a rebuild of
# them. processed/ only; never published, and it holds no user identifier -- the account axis is
# a frame slot index and the counts are counts.
_W16 = WEIGHTS.astype(np.int16)
if not np.array_equal(_W16.astype(np.int64), WEIGHTS.astype(np.int64)):
    sys.exit("HARD STOP: the weight matrix does not survive the int16 cast it is stored in, so "
             "the persisted replicate set would not be the one that produced the endpoints.")
with open(__file__, "rb") as _fh:
    _SRC_SHA12 = hashlib.sha256(_fh.read()).hexdigest()[:12]
np.savez_compressed(
    os.path.join(OUT, "boot_weights.npz"),
    weights=_W16,
    # THE MATRIX CARRIES ITS OWN IDENTITY, so a consumer never has to infer it from a filename.
    # The digest is taken over the SAME int64 view the design block records, which is what makes
    # the two comparable at all; the cast above is checked, not assumed.
    shape=np.asarray(WEIGHTS.shape, dtype=np.int64),
    dtype_stored=np.str_(str(_W16.dtype)),
    dtype_drawn=np.str_(str(WEIGHTS.dtype)),
    digest_sha256_12=np.str_(REPLICATE_SET_DIGEST),
    digest_over=np.str_("np.ascontiguousarray(weights, dtype=np.int64).tobytes()"),
    n_frame=np.int64(N_FRAME), B=np.int64(B), seed=np.int64(SEED),
    draw_mechanism=np.str_("default_rng -> integers(0, n_frame, size=(m, n_frame)) -> count "
                           "the drawn indices  [decisions/0125]"),
    source_file=np.str_("src/step9_b_2_bootstrap.py"),
    source_sha256_12=np.str_(_SRC_SHA12),
    **{"counts__%s__%s" % g: m for g, m in _stored_counts.items()})

print(json.dumps(res, indent=1))
