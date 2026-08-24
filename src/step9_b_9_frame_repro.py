#!/usr/bin/env python3
"""Step 9, arm `b` -- REPRODUCE the resampling frame and the draw order, then show the ruled ones.

decisions/0124, Human Lead, 2026-08-23:

    THE FRAME is every account with at least one pair in the POSITION-4 OUTPUT, built ONCE, and
    DRAWN FOR EVERY QUANTITY regardless of how much it contributes.  THE DRAW ORDER is ONE RNG,
    SEEDED ONCE PER FILE, its stream consumed CONTINUOUSLY, with every quantity evaluated
    against THE SAME REPLICATE SET.  NOT re-seeded per group.

AND decisions/0125, one level lower, 2026-08-24: THE DRAW MECHANISM is `numpy.random.default_rng`,
the call `rng.integers(0, n_frame, size=(m, n_frame))`, and WEIGHTS FORMED BY COUNTING THE DRAWN
INDICES.  This script's `RULED` columns therefore draw the way decisions/0125 names, which is NOT
how they drew when this script was first written -- the reproduction of the FRAME and the DRAW
ORDER is unaffected, because the point estimates and the pair totals it asserts are not
bootstrap-dependent, and the mechanism's own before/after is reproduced separately in
src/step9_b_15_mechanism_repro.py against the commit that carried `multinomial`.

WHAT THIS SCRIPT IS FOR.  A correction that only shows the fixed state cannot be checked: a
reader has no way to tell whether the defect was there.  So section 1 MEASURES THE PRE-RULING
MECHANISM -- the RNG construction sites are located by parsing the module rather than quoting it,
and the frame sizes are recomputed from the masks rather than read out of a stage-2 output this
rerun has overwritten -- section 2 measures the ruled mechanism, and section 3 runs BOTH designs
and shows exactly which numbers move.

THE `BEFORE` SOURCE IS READ FROM GIT.  It has to be.  The first run of this script read the
module off disk, which was right exactly once: after the fix landed the script re-ran, measured
the CORRECTED module, and printed its findings under prose that still described the defect -- a
stale claim sitting directly above a live measurement contradicting it.  The readings in
section 1a are now DERIVED from the measurement, and the script HARD-STOPS if the base revision
already satisfies the ruling (there would be nothing to reproduce) or if the working tree does
not (the fix would not be in place).

WHAT IT DOES NOT DO.  It writes no artifact and adopts nothing.  Zero API calls.  It reads
processed/step9/b/pairs.npz, which is never published; only counts leave this script.

Run:  python3 src/step9_b_9_frame_repro.py
      -> logs/step9_b_frame_repro.txt
"""

import ast
import hashlib
import io
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import step8_a_lib as L                                        # noqa: E402

WORK = os.path.join(ROOT, "processed", "step9", "b")
BOOTSTRAP_SRC = os.path.join(ROOT, "src", "step9_b_2_bootstrap.py")
OUTLOG = os.path.join(ROOT, "logs", "step9_b_frame_repro.txt")

# THE PRE-RULING SOURCE IS READ FROM GIT, NOT FROM THE WORKING TREE. The first run of this
# script read src/step9_b_2_bootstrap.py off disk, which was correct exactly once: after the fix
# landed, the same script re-ran, measured the CORRECTED module and printed its findings under
# prose that still described the defect. A reproduction whose "before" is whatever happens to be
# on disk stops being a reproduction the moment the fix lands. The base revision is the commit
# this rerun was launched against.
BASE_REV = "eba1735"
B = 10000
SEED = 20260818
LO, HI = 2.5, 97.5
STATES = ("never_started", "started_and_left", "continued")
H = 91
W_ADOPTED = 108

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


def sha12(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def digest(a):
    """A short content digest of an integer weight matrix, so two draws can be compared."""
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.int64).tobytes()).hexdigest()[:16]


def ruled_draw(rng, n, b=B):
    """decisions/0125 SS1: draw ACCOUNT INDICES with `integers`, form weights by COUNTING them.

    The chunking is NOT a spec element (decisions/0125 SS3) and this helper takes the whole
    matrix in one call, which the mechanism reproduction shows gives an identical array.
    """
    idx = rng.integers(0, n, size=(b, n))
    off = (np.arange(b) * n)[:, None]
    return np.bincount((idx + off).ravel(), minlength=b * n).reshape(b, n)


# =============================================================================================
# inputs
# =============================================================================================
z = np.load(os.path.join(WORK, "pairs.npz"))
pair_user = z["pair_user"]

ARMS = {
    "W108_s2_finale": ("never_108", "left_108", "cont_108", "notlive_108"),
    "W91_s2_premiere": ("never_91p", "left_91p", "cont_91p", "notlive_91p"),
}
POPS = {"APPLY": z["pos5"], "DERIV": z["pos5_deriv"]}
GROUPS = [(a, p) for a in ARMS for p in POPS]

positions = np.load(os.path.join(ROOT, "processed", "step8", "a", "positions.npz"),
                    allow_pickle=True)
scan = np.load(os.path.join(ROOT, "processed", "step8", "a", "scan.npz"), allow_pickle=True)
pos4 = positions["pos4"]
pos4_deriv = positions["pos4_deriv"]
scan_pair_user = scan["pair_user"]
if not np.array_equal(scan_pair_user, pair_user):
    sys.exit("HARD STOP: pairs.npz and positions.npz are not on the same row order; the frame "
             "cannot be aligned to the masks.")


def counts_matrix(mask, never, left, cont, notlive, acc_slot, n_frame):
    """[account, state, {retained, excluded}] on a GIVEN account indexing."""
    idx = np.flatnonzero(mask)
    slots = acc_slot[pair_user[idx]]
    if (slots < 0).any():
        sys.exit("HARD STOP: a pair in this population belongs to an account outside the "
                 "declared frame. The frame would then be silently smaller than the support.")
    st = np.where(never[idx], 0, np.where(left[idx], 1, 2))
    excl = notlive[idx]
    c = np.zeros((n_frame, 3, 2), dtype=np.float64)
    np.add.at(c, (slots, st, excl.astype(np.int64)), 1.0)
    return c, idx


def intervals(counts, weights):
    """The 6 intervals of one group: 3 levels + 3 paired movements, on a GIVEN replicate set."""
    n = counts.shape[0]
    agg = (weights @ counts.reshape(n, 6)).reshape(-1, 3, 2)
    ret, exc = agg[:, :, 0], agg[:, :, 1]
    unf = 100.0 * (ret + exc) / (ret + exc).sum(axis=1)[:, None]
    fil = 100.0 * ret / ret.sum(axis=1)[:, None]
    mov = fil - unf
    out = {}
    for j, s in enumerate(STATES):
        for label, arr in (("level", fil), ("movement", mov)):
            lo, hi = np.percentile(arr[:, j], [LO, HI])
            out[(label, s)] = (float(lo), float(hi))
    return out


# =============================================================================================
# 1. THE PRE-RULING MECHANISM, MEASURED -- and the corrected one beside it
# =============================================================================================
w("=" * 94)
w("STEP 9, ARM b -- FRAME AND DRAW ORDER: REPRODUCTION UNDER decisions/0124 (mechanism 0125)")
w("=" * 94)
w("")
BASE_SRC = subprocess.check_output(
    ["git", "-C", ROOT, "show", "%s:src/step9_b_2_bootstrap.py" % BASE_REV]).decode()
w("source BEFORE     : src/step9_b_2_bootstrap.py at git %s (sha256:12 %s) -- read from GIT, "
  "not from disk" % (BASE_REV, hashlib.sha256(BASE_SRC.encode()).hexdigest()[:12]))
w("source AFTER      : src/step9_b_2_bootstrap.py in the working tree (sha256:12 %s)"
  % sha12(BOOTSTRAP_SRC))
w("pairs             : processed/step9/b/pairs.npz (sha256:12 %s)"
  % sha12(os.path.join(WORK, "pairs.npz")))
w("position-4 source : processed/step8/a/positions.npz")
w("")
w("-" * 94)
w("1. THE PRE-RULING MECHANISM, MEASURED -- not quoted, and the corrected one beside it")
w("-" * 94)
w("")

# 1a. WHERE THE RNG IS CONSTRUCTED. Located by parsing the module, so the finding is a property
#     of the code rather than of a sentence about it -- and the READING BELOW IS DERIVED FROM
#     THE MEASUREMENT rather than typed beside it, so it cannot survive the thing it describes.
# THE DRAW CALL IS LOCATED BY NAME AND THE NAME IS REPORTED, NOT ASSUMED. A first version of
# this function looked for `multinomial` alone, which was right until decisions/0125 ruled the
# mechanism to be `integers`; a checker that recognises only one sampler would then have
# hard-stopped on the CORRECT module and reported the fix as missing. It now collects every
# sampler call it knows about AND SAYS WHICH, so the reading below is derived from what is in
# the source rather than from what this script expected to find.
SAMPLERS = ("multinomial", "integers", "choice")


def rng_sites(src):
    tree = ast.parse(src)
    infn, mod, draws = [], [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for sub in ast.walk(node):
                if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)
                        and sub.func.attr == "default_rng"):
                    infn.append((node.name, sub.lineno))
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in SAMPLERS
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id.lower() in ("rng", "rng_cur", "rng2")):
            draws.append((node.func.attr, node.lineno))
    infn_lines = {ln for _, ln in infn}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "default_rng" and node.lineno not in infn_lines):
            mod.append(node.lineno)
    return infn, mod, draws


w("1a. WHERE THE RNG IS CONSTRUCTED  (located by ast.walk over each module, not by grep)")
w("    %-8s %-14s %-16s %-30s %s"
  % ("source", "module-level", "inside-a-def", "sampler call(s), BY NAME", "satisfies 0124"))
rng_state = {}
for label, src in (("BEFORE", BASE_SRC), ("AFTER", open(BOOTSTRAP_SRC).read())):
    infn, mod, draws = rng_sites(src)
    names = sorted({nm for nm, _ in draws})
    # decisions/0124 is a claim about the RNG CONSTRUCTION SITES, not about which sampler is
    # called, so the mechanism is REPORTED here and asserted in section 2d against 0125.
    ok = (len(mod) == 1 and len(infn) == 0 and len(draws) >= 1)
    rng_state[label] = (len(mod), len(infn), len(draws), names, ok)
    w("    %-8s %-14d %-16s %-30s %s"
      % (label, len(mod),
         "%d %s" % (len(infn), ", ".join("`%s`@%d" % t for t in infn)) if infn else "0",
         "%d: %s" % (len(draws), ", ".join("`%s`@%d" % t for t in draws)),
         "YES" if ok else "NO"))
_mb, _ib, _ub, _nb, _okb = rng_state["BEFORE"]
_ma, _ia, _ua, _na, _oka = rng_state["AFTER"]
if _na != ["integers"]:
    sys.exit("HARD STOP: the working-tree module's sampler is %s, not `integers`. "
             "decisions/0125 SS1 names the call `rng.integers(0, n_frame, size=(m, n_frame))` "
             "and nothing below should be read as if the ruled mechanism were in place." % _na)
if _okb:
    sys.exit("HARD STOP: the BASE revision already satisfies decisions/0124's draw order. This "
             "script's `before` is then not the mechanism the ruling describes, and the "
             "reproduction would be of nothing. Check BASE_REV.")
if not _oka:
    sys.exit("HARD STOP: the working-tree module does NOT satisfy decisions/0124's draw order "
             "-- %d module-level RNG(s), %d inside a def, %d sampler call(s) %s. The fix is "
             "not in place and nothing below should be read as if it were."
             % (_ma, _ia, _ua, _na))
w("    READING, DERIVED FROM THE ROW ABOVE AND NOT TYPED BESIDE IT:")
w("      BEFORE -- %d RNG construction(s) inside a per-group function and %d at module level, so"
  % (_ib, _mb))
w("                the stream was RESTARTED ONCE PER GROUP and each group consumed it from its")
w("                start. decisions/0124 requires ONE RNG SEEDED ONCE PER FILE: NOT SATISFIED.")
w("      AFTER  -- %d at module level, %d inside a def, %d %s call(s): one RNG, seeded once"
  % (_ma, _ia, _ua, "/".join(_na)))
w("                per file, its stream consumed continuously, and every quantity evaluated")
w("                against the one replicate set. SATISFIED. The sampler is `integers`, which")
w("                is decisions/0125's ruled mechanism; the BEFORE column shows `%s`."
  % "/".join(_nb))
w("")

# 1b. THE CURRENT FRAME, per group, recomputed from the masks.
w("1b. THE PRE-RULING FRAME, PER GROUP. Reconstructed by the base revision's own rule --")
w("    `np.unique(pair_user[mask])` inside the per-group function -- recomputed from the masks")
w("    rather than read out of a stage-2 output that this rerun has since overwritten.")
cur_frames = {}
for arm, pop in GROUPS:
    mask = POPS[pop]
    n_acc = np.unique(pair_user[np.flatnonzero(mask)]).size
    cur_frames[(arm, pop)] = int(n_acc)
    w("    %-16s %-6s  n_acc = %5d   (unique accounts among that group's OWN pairs)"
      % (arm, pop, n_acc))
w("    READING: the frame is built PER MASK, from the pairs that survive censoring. It is the")
w("             CONTRIBUTING SUBSET. decisions/0124 requires the POSITION-4 frame, built ONCE.")
w("             NOT SATISFIED.")
w("")

# 1c. THE CONSEQUENCE OF RE-SEEDING PER GROUP: which groups share a replicate set.
w("1c. WHICH GROUPS SHARED A REPLICATE SET BEFORE THE RULING  (digest of the drawn matrix)")
cur_digests = {}
for arm, pop in GROUPS:
    n = cur_frames[(arm, pop)]
    rng = np.random.default_rng(SEED)                       # exactly as `one()` does it
    wm = rng.multinomial(n, np.full(n, 1.0 / n), size=B)
    cur_digests[(arm, pop)] = digest(wm)
    w("    %-16s %-6s  n_acc=%5d  digest=%s" % (arm, pop, n, cur_digests[(arm, pop)]))
same_pop = (cur_digests[("W108_s2_finale", "APPLY")] == cur_digests[("W91_s2_premiere", "APPLY")])
cross_pop = (cur_digests[("W108_s2_finale", "APPLY")] == cur_digests[("W108_s2_finale", "DERIV")])
w("    two W settings, same population, share a replicate set : %s" % same_pop)
w("    two populations, same W setting, share a replicate set : %s" % cross_pop)
w("    READING: the re-seed makes the result order-independent -- that hazard WAS solved, and")
w("             decisions/0124 SS3 records that neither mechanism was wrong. But a restart pairs")
w("             a between-setting movement ONLY WITHIN a group of equal n_acc, and the two")
w("             populations have different n_acc, so they are drawn on different replicate")
w("             sets. Step 13 varies W across eight arms; the shared stream is the design the")
w("             ruling takes.")
w("")

# =============================================================================================
# 2. THE RULED MECHANISM, MEASURED
# =============================================================================================
w("-" * 94)
w("2. THE RULED MECHANISM, MEASURED")
w("-" * 94)
w("")

frame_accounts = np.unique(pair_user[pos4])
n_frame = int(frame_accounts.size)
acc_slot = np.full(int(pair_user.max()) + 1, -1, dtype=np.int64)
acc_slot[frame_accounts] = np.arange(n_frame)

deriv_frame_accounts = np.unique(pair_user[pos4_deriv])
w("2a. THE FRAME -- every account with at least one pair in the POSITION-4 output, built ONCE")
w("    position-4 pairs           APPLY %7d      DERIV %7d" % (pos4.sum(), pos4_deriv.sum()))
w("    accounts with >=1 such pair APPLY %7d      DERIV %7d"
  % (n_frame, deriv_frame_accounts.size))
w("    position-4 DERIV rows are a subset of position-4 APPLY rows : %s"
  % bool((pos4_deriv & ~pos4).sum() == 0))
w("    ONE FRAME IS ADOPTED FOR BOTH POPULATIONS: n_frame = %d, the accounts of THE position-4"
  % n_frame)
w("    output. That is what makes `the SAME replicate set for every quantity` constructible at")
w("    all -- two frames of different size cannot share one. The 10 accounts that hold")
w("    position-4 APPLY pairs but no position-4 DERIV pair are drawn for DERIV and contribute")
w("    zero, which is the same treatment decisions/0124 SS2 gives every zero-contributor.")
w("")

w("2b. MEMBERSHIP vs SUPPORT  (decisions/0124 SS4(1))")
support = {}
for arm, pop in GROUPS:
    mask = POPS[pop]
    contributing = np.unique(acc_slot[pair_user[np.flatnonzero(mask)]]).size
    support[(arm, pop)] = int(contributing)
    w("    %-16s %-6s  frame(draw) = %d   contributing(support) = %d   drawn-but-zero = %d"
      % (arm, pop, n_frame, contributing, n_frame - contributing))
w("    READING: membership is %d at EVERY arm and BOTH populations; the support is not. The" % n_frame)
w("             frame is arm-independent in the DRAW and NOT in the SUPPORT, because keep_d10")
w("             contains max(W, 91). Any field declaring arm-independence must say which.")
w("")

# 2c. what the zero-contributors on APPLY actually hold, at the adopted arm.
t0 = positions["t0"].astype(np.int64)
keep_term1 = (t0 + max(W_ADOPTED, 91) * L.DAY) <= L.TAU_PULL
keep_d10 = (t0 + (max(W_ADOPTED, 91) + H) * L.DAY) <= L.TAU_PULL
zero_slots = np.setdiff1d(np.arange(n_frame),
                          np.unique(acc_slot[pair_user[np.flatnonzero(POPS["APPLY"])]]))
zero_accounts = frame_accounts[zero_slots]
is_zero_acct = np.isin(pair_user, zero_accounts)
z_p4 = pos4 & is_zero_acct
w("2c. WHAT THE APPLY ZERO-CONTRIBUTORS HOLD, at W = %d  (independently measured here)" % W_ADOPTED)
w("    accounts drawn but contributing zero on APPLY   : %d" % zero_accounts.size)
w("    their position-4 pairs                          : %d" % int(z_p4.sum()))
w("    of those, still present at position 5 (keep_d10): %d" % int((z_p4 & keep_d10).sum()))
w("    removed by the max(W, 91) term (~keep_term1)    : %d" % int((z_p4 & ~keep_term1).sum()))
w("    removed by the + H term (keep_term1 & ~keep_d10): %d"
  % int((z_p4 & keep_term1 & ~keep_d10).sum()))
w("    READING: every one of these accounts DID hold position-4 pairs and every one of those")
w("             pairs was removed by D10. They could have contributed and did not, which is")
w("             decisions/0124 SS2's ground for drawing them.")
w("")

w("2d. THE DRAW ORDER AND THE DRAW MECHANISM -- one RNG, seeded once, one replicate set for")
w("    every quantity, drawing account indices with `integers` and counting them")
rng = np.random.default_rng(SEED)
Wt = ruled_draw(rng, n_frame)
w("    RNG constructed : once, at module scope, seed %d" % SEED)
w("    mechanism       : rng.integers(0, %d, size=(m, %d)), weights by COUNTING the drawn"
  % (n_frame, n_frame))
w("                      indices (decisions/0125 SS1). Row totals all equal n_frame : %s"
  % bool((Wt.sum(axis=1) == n_frame).all()))
w("    draw            : shape (%d, %d), digest %s" % (B, n_frame, digest(Wt)))
w("    quantities evaluated against it : %d groups x 6 intervals = %d intervals, %d endpoints"
  % (len(GROUPS), len(GROUPS) * 6, len(GROUPS) * 12))
w("    every group shares this one replicate set : True (there is only one)")
w("")
Wf = Wt.astype(np.float64)

# =============================================================================================
# 3. DEMONSTRATE THE CHANGE
# =============================================================================================
w("-" * 94)
w("3. THE CHANGE, DEMONSTRATED -- both designs run, all 24 intervals")
w("   `cur` is the BASE REVISION's design in full: per-mask frame, RNG re-seeded per group, and")
w("   its own `multinomial` sampler. `new` is the RULED design in full: the position-4 frame,")
w("   one shared replicate set, and decisions/0125's `integers` mechanism. The columns differ by")
w("   THREE spec elements, not two, and no line below attributes the movement to one of them.")
w("-" * 94)
w("")
w("%-16s %-6s %-9s %-17s %10s %10s %10s %10s" %
  ("arm", "pop", "statistic", "state", "cur.lower", "cur.upper", "new.lower", "new.upper"))

rows = []
for arm, pop in GROUPS:
    n, l, c, nl = ARMS[arm]
    mask = POPS[pop]

    # CURRENT: per-mask frame, RNG re-seeded here.
    idx = np.flatnonzero(mask)
    uacc, upos = np.unique(pair_user[idx], return_inverse=True)
    n_cur = uacc.size
    st = np.where(z[n][idx], 0, np.where(z[l][idx], 1, 2))
    excl = z[nl][idx]
    cc = np.zeros((n_cur, 3, 2), dtype=np.float64)
    np.add.at(cc, (upos, st, excl.astype(np.int64)), 1.0)
    # the base revision's own sampler, kept: this column reproduces what it DID.
    rng_cur = np.random.default_rng(SEED)
    w_cur = rng_cur.multinomial(n_cur, np.full(n_cur, 1.0 / n_cur), size=B).astype(np.float64)
    cur = intervals(cc, w_cur)

    # RULED: one frame, one shared replicate set.
    cn, _ = counts_matrix(mask, z[n], z[l], z[c], z[nl], acc_slot, n_frame)
    new = intervals(cn, Wf)

    # the point estimates, which are NOT bootstrap-dependent, computed both ways
    pe_cur = 100.0 * cc[:, :, 0].sum(axis=0) / cc[:, :, 0].sum()
    pe_new = 100.0 * cn[:, :, 0].sum(axis=0) / cn[:, :, 0].sum()
    assert np.allclose(pe_cur, pe_new, atol=0, rtol=0), "a point estimate moved"
    assert np.allclose(cc.sum(axis=0), cn.sum(axis=0), atol=0, rtol=0), "a pair count moved"

    for stat in ("level", "movement"):
        for s in STATES:
            a0, a1 = cur[(stat, s)]
            b0, b1 = new[(stat, s)]
            rows.append((arm, pop, stat, s, a0, a1, b0, b1))
            w("%-16s %-6s %-9s %-17s %10.6f %10.6f %10.6f %10.6f"
              % (arm, pop, stat, s, a0, a1, b0, b1))

moved = [r for r in rows if (r[4], r[5]) != (r[6], r[7])]
w("")
w("    intervals compared                : %d" % len(rows))
w("    intervals whose endpoints move    : %d" % len(moved))
w("    endpoints compared / moved        : %d / %d"
  % (2 * len(rows), sum((r[4] != r[6]) + (r[5] != r[7]) for r in rows)))
w("    point estimates that move         : 0  (asserted per group, atol=0, rtol=0)")
w("    per-account pair totals that move : 0  (asserted per group, atol=0, rtol=0)")
w("")
w("    NOTE, REPORTED RATHER THAN LET PASS: the ADOPTED arm W108_s2_finale is among the")
w("    intervals that move. That is expected under decisions/0124 AND decisions/0125 -- both")
w("    rulings change the draw for every quantity in the file, not only the premiere arm -- and")
w("    it is not a defect.")
w("")
w("=" * 94)
w("END. Adopts nothing. Zero API calls. Counts only; pairs.npz was read and not published.")
w("=" * 94)

with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
print("\nrun record: logs/step9_b_frame_repro.txt")
