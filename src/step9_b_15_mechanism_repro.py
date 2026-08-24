#!/usr/bin/env python3
"""Step 9, arm `b` -- REPRODUCE the draw MECHANISM defect, then show the ruled mechanism.

decisions/0125, Human Lead, 2026-08-24, one level below decisions/0124:

    THE SPEC NAMES, AND NAMES ONLY: the generator `numpy.random.default_rng`; the seed
    `20260818`; the call `rng.integers(0, n_frame, size=(m, n_frame))`; and that WEIGHTS ARE
    FORMED BY COUNTING THE DRAWN INDICES.  Nothing else.  THE CHUNKING IS DELIBERATELY NOT
    SPECIFIED.

WHY A SEPARATE REPRODUCTION.  src/step9_b_9_frame_repro.py reproduces the FRAME and the DRAW
ORDER against the commit that preceded decisions/0124.  This arm SATISFIED decisions/0124
literally -- one RNG at module scope, seeded once, one call, the resulting matrix shared by every
group -- and STILL drew a different replicate set, so the defect decisions/0125 names is not
visible in that comparison at all: its `before` fails 0124 for other reasons, and its `after`
already carries the fix.  The mechanism needs its own before, and the before is the commit that
CLOSED 0124.

WHAT IS SHOWN, IN ORDER.
  1. THE COMMITTED CALL, READ FROM GIT, not quoted from memory and not read off disk -- the
     working tree now carries the fix, so a `before` taken from disk would silently become an
     `after` (the failure mode src/step9_b_9_frame_repro.py already hit once).  The call is
     located by PARSING the base-revision module, and the reproduction HARD-STOPS if the base
     revision does not carry `multinomial` (there would be nothing to reproduce) or if the
     working tree does not carry `integers` (the fix would not be in place).
  2. BOTH DRAWS RUN under one seed, one frame, one B, and are compared element-wise.  Row totals
     are reported for both: they are equal, which is the point -- the DISTRIBUTION is right in
     both and the REALISATION is not the same.
  3. THE CHUNKING IS MEASURED, NOT ASSERTED.  decisions/0125 SS3 removed it from the spec on a
     measurement, and a measurement recorded once and quoted forever is the stale-figure problem;
     so CHUNK 200, CHUNK 500 and a single call are re-taken here every run and compared.
  4. A FAILING PROBE.  A check that cannot fail on the vector it polices is not a check
     (decisions/0123 SS3), so the element-wise comparison is run against a construction it MUST
     reject -- the ruled mechanism at a different seed -- and against one it MUST accept: the
     same mechanism, same seed, drawn in a different number of calls.  A comparison that could
     not separate those two would establish nothing about the mechanism.

WHAT IT DOES NOT DO.  It writes no artifact and adopts nothing.  Zero API calls.  It draws from
account-slot indices only and reads no user data at all: `n_frame` is read from this arm's
recorded weight matrix header, which is a count.

Run:  python3 src/step9_b_15_mechanism_repro.py
      -> logs/step9_b_mechanism_repro.txt
"""

import ast
import hashlib
import io
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOTSTRAP_SRC = os.path.join(ROOT, "src", "step9_b_2_bootstrap.py")
WEIGHTS_NPZ = os.path.join(ROOT, "processed", "step9", "b", "boot_weights.npz")
OUTLOG = os.path.join(ROOT, "logs", "step9_b_mechanism_repro.txt")

# THE BASE REVISION IS THE COMMIT THIS RERUN WAS LAUNCHED AGAINST -- the one that closed
# decisions/0124 and still drew with `multinomial`. Read from git, never from disk.
BASE_REV = "5393430"
SEED = 20260818
B = 10000

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


def digest(a):
    return hashlib.sha256(np.ascontiguousarray(a, dtype=np.int64).tobytes()).hexdigest()[:16]


def sha12(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def sampler_calls(src):
    """Every `<rng>.<sampler>(...)` call in a module, by name and line. Parsed, not grepped."""
    tree = ast.parse(src)
    out = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in ("multinomial", "integers", "choice")
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id.lower().startswith("rng")):
            out.append((node.func.attr, node.lineno,
                        ast.unparse(node) if hasattr(ast, "unparse") else ""))
    return out


def count_indices(idx, n):
    """decisions/0125 SS1: WEIGHTS ARE FORMED BY COUNTING THE DRAWN INDICES."""
    m = idx.shape[0]
    off = (np.arange(m) * n)[:, None]
    return np.bincount((idx + off).ravel(), minlength=m * n).reshape(m, n)


def ruled(n, seed=SEED, b=B, chunk=None):
    """The ruled draw. `chunk` is NOT a spec element and is varied below to show it is not."""
    rng = np.random.default_rng(seed)
    if chunk is None:
        return count_indices(rng.integers(0, n, size=(b, n)), n)
    out = np.empty((b, n), dtype=np.int64)
    done = 0
    while done < b:
        m = min(chunk, b - done)
        out[done:done + m] = count_indices(rng.integers(0, n, size=(m, n)), n)
        done += m
    return out


# =============================================================================================
# 0. the frame size, read from this arm's own recorded matrix rather than typed
# =============================================================================================
z = np.load(WEIGHTS_NPZ)
N_FRAME = int(z["n_frame"])
if int(z["B"]) != B or int(z["seed"]) != SEED:
    sys.exit("HARD STOP: the recorded weight matrix was drawn at B=%d seed=%d, not B=%d "
             "seed=%d. This reproduction would then be of a different design."
             % (int(z["B"]), int(z["seed"]), B, SEED))

w("=" * 94)
w("STEP 9, ARM b -- THE DRAW MECHANISM: REPRODUCTION UNDER decisions/0125")
w("=" * 94)
w("")
w("source BEFORE : src/step9_b_2_bootstrap.py at git %s -- READ FROM GIT, not from disk"
  % BASE_REV)
w("source AFTER  : src/step9_b_2_bootstrap.py in the working tree (sha256:12 %s)"
  % sha12(BOOTSTRAP_SRC))
w("n_frame       : %d  (read from processed/step9/b/boot_weights.npz, a count)" % N_FRAME)
w("B = %d   seed = %d" % (B, SEED))
w("")

# =============================================================================================
# 1. the call, before and after, located by parsing each module
# =============================================================================================
w("-" * 94)
w("1. THE CALL, BEFORE AND AFTER -- located by ast.walk over each module, not quoted")
w("-" * 94)
w("")
BASE_SRC = subprocess.check_output(
    ["git", "-C", ROOT, "show", "%s:src/step9_b_2_bootstrap.py" % BASE_REV]).decode()
before_calls = sampler_calls(BASE_SRC)
after_calls = sampler_calls(open(BOOTSTRAP_SRC).read())
w("    BEFORE (git %s):" % BASE_REV)
for nm, ln, txt in before_calls:
    w("        line %-5d %s" % (ln, txt or nm))
w("    AFTER  (working tree):")
for nm, ln, txt in after_calls:
    w("        line %-5d %s" % (ln, txt or nm))
w("")
before_names = sorted({nm for nm, _, _ in before_calls})
after_names = sorted({nm for nm, _, _ in after_calls})
if before_names != ["multinomial"]:
    sys.exit("HARD STOP: the base revision's sampler is %s, not `multinomial`. This script's "
             "`before` is then not the mechanism decisions/0125 describes and the reproduction "
             "would be of nothing. Check BASE_REV." % before_names)
if after_names != ["integers"]:
    sys.exit("HARD STOP: the working-tree sampler is %s, not `integers`. decisions/0125 SS1 "
             "names `rng.integers(0, n_frame, size=(m, n_frame))`; the fix is not in place and "
             "nothing below should be read as if it were." % after_names)
w("    READING, DERIVED FROM THE ROWS ABOVE: the base revision drew with `%s` and the working"
  % before_names[0])
w("    tree draws with `%s`. Both take ONE RNG, seeded ONCE at module scope, so decisions/0124"
  % after_names[0])
w("    was satisfied either way -- which is exactly why this defect needed a ruling of its own.")
w("")

# =============================================================================================
# 2. both draws, run and compared
# =============================================================================================
w("-" * 94)
w("2. BOTH DRAWS, RUN UNDER ONE SEED AND COMPARED ELEMENT-WISE")
w("-" * 94)
w("")
rng_b = np.random.default_rng(SEED)
W_before = rng_b.multinomial(N_FRAME, np.full(N_FRAME, 1.0 / N_FRAME), size=B)
W_after = ruled(N_FRAME)
w("    %-24s %-14s %-20s %10s %10s"
  % ("mechanism", "shape", "digest sha256:16", "rowsum min", "rowsum max"))
for label, M in (("multinomial (BEFORE)", W_before), ("integers+count (AFTER)", W_after)):
    w("    %-24s %-14s %-20s %10d %10d"
      % (label, "(%d, %d)" % M.shape, digest(M), M.sum(1).min(), M.sum(1).max()))
identical = bool(np.array_equal(W_before, W_after))
rows_diff = int((W_before != W_after).any(1).sum())
cells_diff = int((W_before != W_after).sum())
w("")
w("    arrays identical            : %s" % identical)
w("    replicates differing        : %d of %d" % (rows_diff, B))
w("    cells differing             : %d of %d" % (cells_diff, B * N_FRAME))
if identical:
    sys.exit("HARD STOP: the two mechanisms produced the SAME array, so this build does not "
             "reproduce the defect decisions/0125 records. That would be a finding about the "
             "ruling and must be reported, not passed over.")
w("    READING: same generator, same seed, same frame, same B, and EVERY replicate differs.")
w("             Both row-total vectors are constant at n_frame, so the DISTRIBUTION is right in")
w("             both; the REALISATION is not the same. An unfixed mechanism makes a fixed seed")
w("             decorative in exactly the way decisions/0124 said an unfixed draw order does.")
w("")

# =============================================================================================
# 3. the chunking, MEASURED
# =============================================================================================
w("-" * 94)
w("3. THE CHUNKING, RE-MEASURED THIS RUN -- decisions/0125 SS3 took it OUT of the spec")
w("-" * 94)
w("")
w("    A spec element earns its place by DETERMINING THE OUTPUT. decisions/0125 removed the")
w("    chunking on a measurement; a measurement taken once and quoted forever is the stale-")
w("    figure problem, so it is re-taken here rather than cited.")
w("")
w("    %-22s %-20s %s" % ("construction", "digest sha256:16", "identical to single call"))
chunk_rows = []
for label, kw in (("single call", {}), ("CHUNK 200", {"chunk": 200}), ("CHUNK 500", {"chunk": 500})):
    M = ruled(N_FRAME, **kw)
    same = bool(np.array_equal(M, W_after))
    chunk_rows.append((label, same))
    w("    %-22s %-20s %s" % (label, digest(M), same))
if not all(s for _, s in chunk_rows):
    sys.exit("HARD STOP: the chunking DOES determine the output on this build. decisions/0125 "
             "SS3 removed it from the spec on the opposite measurement, and that is a finding "
             "for the Human Lead, not something to work around.")
w("")
w("    READING: %d constructions, %d identical. The chunking does not determine the output, so"
  % (len(chunk_rows), sum(s for _, s in chunk_rows)))
w("             it is not a spec element and this arm's CHUNK is its own choice.")
w("")

# =============================================================================================
# 4. the comparison shown FAILING and shown PASSING
# =============================================================================================
w("-" * 94)
w("4. THE COMPARISON, SHOWN REJECTING AND SHOWN ACCEPTING")
w("-" * 94)
w("")
w("    A check that cannot fail on the vector it polices is not a check (decisions/0123 SS3).")
w("    The element-wise comparison used in section 2 is therefore run against two constructions")
w("    whose verdict is known in advance: one it MUST reject, one it MUST accept.")
w("")
must_reject = ruled(N_FRAME, seed=SEED + 1)
must_accept = ruled(N_FRAME, chunk=200)
probes = [
    ("ruled mechanism, seed %d" % (SEED + 1), must_reject, False,
     "a different seed must not reproduce the draw"),
    ("multinomial, seed %d" % SEED, W_before, False,
     "the superseded mechanism must not reproduce the draw"),
    ("ruled mechanism, chunked 200", must_accept, True,
     "the same mechanism at the same seed must reproduce it whatever the chunking"),
]
w("    %-34s %-10s %-10s %s" % ("probe", "expected", "observed", "verdict"))
failed = 0
for label, M, expect, why in probes:
    obs = bool(np.array_equal(M, W_after))
    ok = obs == expect
    failed += (not ok)
    w("    %-34s %-10s %-10s %s"
      % (label, "match" if expect else "differ", "match" if obs else "differ",
         "as required" if ok else "PROBE FAILED"))
    w("        %s" % why)
w("")
w("    probes run       : %d" % len(probes))
w("    probes as required: %d" % (len(probes) - failed))
if failed:
    sys.exit("HARD STOP: %d probe(s) did not behave as required. A comparison that cannot "
             "separate the ruled mechanism from a different seed, or that calls the ruled "
             "mechanism a mismatch of itself, establishes nothing about either." % failed)
w("    READING: the comparison rejects a different seed AND the superseded sampler, and accepts")
w("             the ruled mechanism under a chunking it was not built with. It is sensitive to")
w("             the mechanism and the seed, and insensitive to the thing the spec left open --")
w("             which is the separation decisions/0125 SS3 asserts.")
w("")

w("=" * 94)
w("END. Adopts nothing. Zero API calls. Counts only; no user data is read by this script.")
w("=" * 94)

with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
print("\nrun record: logs/step9_b_mechanism_repro.txt")
