#!/usr/bin/env python3
"""Step 9, arm `b` -- RE-TAKE the pairing evidence on the weights the current ruling produced.

decisions/0124 SS5: "Also to be re-established after any rerun: arm b's own pairing evidence --
it verified all 12 movements paired BY REPRODUCING PUBLISHED ENDPOINTS FROM THE RECORDED
WEIGHTS, and those weights change." It applies to EVERY rerun that moves the draw, so it applies
again under decisions/0125, which fixed the draw MECHANISM one level below decisions/0124 and
moved the weights a second time. This file names no ruling in its assertions: it reads the
weights the bootstrap actually recorded and checks their digest against the bootstrap's own, so
it re-establishes the claim on whatever draw is current rather than on a draw it was told about.

THE CLAIM UNDER TEST. Each of the 12 paired movements is the percentile interval of
`filtered - unfiltered` differenced INSIDE each replicate -- the same account weight row
produces both terms -- and NOT a difference between two independently resampled quantities. If
it were the latter the interval would be far wider and the pairing that makes a movement
readable would not exist.

HOW IT IS ESTABLISHED, AND WHY THAT WAY.
  1. The RECORDED WEIGHTS are read from processed/step9/b/boot_weights.npz -- the actual
     (B x n_frame) matrix the bootstrap drew -- and their digest is checked against the digest
     the bootstrap stage recorded. Not rebuilt from the seed: a rebuild would test that the seed
     is reproducible, which is a different claim.
  2. Every published endpoint is RECOMPUTED from those weights and compared to the artifact.
     24 intervals, 48 endpoints. Reproduction is the evidence.
  3. THE TEST IS SHOWN FAILING. A guard that cannot fail on the vector it polices is not a
     guard (decisions/0123 SS3), so an UNPAIRED construction is built deliberately -- the
     unfiltered term taken from a DIFFERENT replicate set -- and the same comparison is run
     against it. It must REJECT. A probe that passes on the wrong construction would mean the
     comparison is insensitive to exactly the property it claims to establish.
  4. Coverage is printed. An empty result and a clean result are the same value.

Reads processed/step9/b/boot_weights.npz, which is never published; only counts leave here.

Run:  python3 src/step9_b_10_pairing_evidence.py
      -> logs/step9_b_pairing_evidence.txt
"""

import hashlib
import io
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "processed", "step9", "b")
ART = os.path.join(ROOT, "artifacts", "step9-headline-corrected-2026-08-21-b.json")
OUTLOG = os.path.join(ROOT, "logs", "step9_b_pairing_evidence.txt")

LO, HI = 2.5, 97.5
STATES = ("never_started", "started_and_left", "continued")
ARMS = ("W108_s2_finale", "W91_s2_premiere")
POPS = ("APPLY", "DERIV")
TOL = 1e-12

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


z = np.load(os.path.join(WORK, "boot_weights.npz"))
WEIGHTS = z["weights"].astype(np.float64)
N_FRAME = int(z["n_frame"])
B = int(z["B"])
SEED = int(z["seed"])
stage2 = json.load(open(os.path.join(WORK, "stage2_bootstrap.json")))
doc = json.load(open(ART))

w("=" * 94)
w("STEP 9, ARM b -- PAIRING EVIDENCE, RE-TAKEN ON THE CURRENT WEIGHTS (decisions/0124, 0125)")
w("=" * 94)
w("")
w("weights read from : processed/step9/b/boot_weights.npz  (the matrix that was drawn, not a")
w("                    rebuild from the seed -- a rebuild would test a different claim)")
w("artifact compared : artifacts/step9-headline-corrected-2026-08-21-b.json")
w("B = %d   n_frame = %d   seed = %d" % (B, N_FRAME, SEED))

dig = hashlib.sha256(np.ascontiguousarray(z["weights"].astype(np.int64)).tobytes()).hexdigest()[:16]
recorded = stage2["design"]["replicate_set_digest_sha256_12"]
w("replicate-set digest, recomputed here : %s" % dig)
w("replicate-set digest, recorded by the bootstrap stage : %s" % recorded)
if dig != recorded:
    sys.exit("HARD STOP: the recorded weights are not the replicate set the bootstrap used.")
w("MATCH -- these are the weights that produced the published endpoints.")
w("")

# THE PRODUCER'S IDENTITY IS COMPARED, NOT ASSUMED (Human Lead ruling 3, 2026-08-25).
# The digest above establishes that these weights are the ones the bootstrap STAGE recorded. It
# says nothing about whether the SCRIPT that drew them is still the script on disk: a producer
# edited and not re-run leaves an output whose stated origin no longer exists in that form, and
# until this block was written every consumer in this arm went on exiting 0 in that state. An
# artifact asserting which script produced it, where nothing checks the assertion is current, is
# a claim its mechanism cannot deliver. NO DEFAULT: an absent field is a hard stop, because an
# absent claim and a stale one are different defects and neither is a pass.
for _k in ("source_file", "source_sha256_12"):
    if _k not in z.files:
        sys.exit("HARD STOP: processed/step9/b/boot_weights.npz carries no `%s`, so the matrix "
                 "does not state what produced it and this script cannot compare it." % _k)
_PROD = str(z["source_file"])
_CLAIMED = str(z["source_sha256_12"])
_ONDISK = hashlib.sha256(open(os.path.join(ROOT, _PROD), "rb").read()).hexdigest()[:12]
w("producer named by the matrix : %s" % _PROD)
w("producer hash it recorded    : %s" % _CLAIMED)
w("producer hash on disk now    : %s" % _ONDISK)
if _CLAIMED != _ONDISK:
    sys.exit("HARD STOP: %s has changed since it wrote these weights (recorded %s, on disk %s). "
             "The reproduction below would then establish a claim about a matrix that the "
             "current producer does not produce. Re-run the producer -- do not re-label the "
             "output." % (_PROD, _CLAIMED, _ONDISK))
w("MATCH -- the script that drew these weights is the script on disk.")
w("")


def recompute(counts):
    agg = (WEIGHTS @ counts.reshape(N_FRAME, 6)).reshape(B, 3, 2)
    ret, exc = agg[:, :, 0], agg[:, :, 1]
    unf = 100.0 * (ret + exc) / (ret + exc).sum(axis=1)[:, None]
    fil = 100.0 * ret / ret.sum(axis=1)[:, None]
    return fil, unf


def pctl(arr, j):
    lo, hi = np.percentile(arr[:, j], [LO, HI])
    return float(lo), float(hi)


# published endpoints, read out of the artifact by path
pub_mov = {e["interval_id"]: (e["ci"]["lower"], e["ci"]["upper"])
           for e in doc["declared_intervals"] if e["ci"]["statistic"] == "movements"}
pub_lvl = {}
for arm_obj, arm in zip(doc["arms"], ARMS):
    for pop in POPS:
        b = arm_obj["headline"][pop]["by_producing_arm"]["arms"]["b"]
        for s in STATES:
            pub_lvl[(arm, pop, s)] = (b["shares"][s]["ci"]["lower"],
                                      b["shares"][s]["ci"]["upper"])

w("-" * 94)
w("1. REPRODUCE EVERY PUBLISHED ENDPOINT FROM THE RECORDED WEIGHTS")
w("-" * 94)
w("")
w("%-16s %-6s %-9s %-17s %14s %14s" % ("arm", "pop", "statistic", "state",
                                        "max|published-", "recomputed|"))
checked = 0
worst = 0.0
for arm in ARMS:
    for pop in POPS:
        counts = z["counts__%s__%s" % (arm, pop)]
        fil, unf = recompute(counts)
        mov = fil - unf                       # PAIRED: same weight row for both terms
        for j, s in enumerate(STATES):
            lo, hi = pctl(fil, j)
            plo, phi = pub_lvl[(arm, pop, s)]
            d1 = max(abs(lo - plo), abs(hi - phi))
            mlo, mhi = pctl(mov, j)
            pmlo, pmhi = pub_mov["movement_%s_%s_%s_b" % (arm, pop, s)]
            d2 = max(abs(mlo - pmlo), abs(mhi - pmhi))
            checked += 2
            worst = max(worst, d1, d2)
            w("%-16s %-6s %-9s %-17s %14.2e %14s" % (arm, pop, "level", s, d1, ""))
            w("%-16s %-6s %-9s %-17s %14.2e %14s" % (arm, pop, "movement", s, d2, ""))
            if d1 > TOL or d2 > TOL:
                sys.exit("HARD STOP: the recorded weights do not reproduce a published endpoint "
                         "at %s/%s/%s." % (arm, pop, s))
w("")
w("    intervals reproduced : %d   (12 levels + 12 movements)" % checked)
w("    endpoints reproduced : %d" % (2 * checked))
w("    worst absolute discrepancy : %.3e   (tolerance %.0e)" % (worst, TOL))
w("    EVERY published endpoint is reproduced from the recorded weights. The 12 movements are")
w("    therefore differenced INSIDE each replicate: the same weight row produced the filtered")
w("    and the unfiltered term.")
w("")

# ---------------------------------------------------------------------------------------------
w("-" * 94)
w("2. THE SAME TEST, RUN AGAINST A DELIBERATELY UNPAIRED CONSTRUCTION -- IT MUST REJECT")
w("-" * 94)
w("")
w("    THE PROBE. The unfiltered term is taken from a DIFFERENT replicate set (an independent")
w("    draw on the same frame, seed %d), so `filtered - unfiltered` is a difference of two"
  % (SEED + 1))
w("    independently resampled quantities rather than a paired delta. Everything else is")
w("    identical: same frame, same counts, same B, same percentiles, AND THE SAME DRAW")
w("    MECHANISM -- decisions/0125's `integers`-and-count, at a different seed. The probe used")
w("    `multinomial` while the bootstrap used it too; when decisions/0125 changed the")
w("    bootstrap's sampler, leaving the probe on the old one would have made it differ from the")
w("    published draw in TWO ways -- seed AND sampler -- and a probe that varies two things")
w("    cannot show which one it is sensitive to. If the comparison in section 1 could not tell")
w("    these apart, it would not be evidence of pairing at all.")
w("")
rng2 = np.random.default_rng(SEED + 1)
_ix2 = rng2.integers(0, N_FRAME, size=(B, N_FRAME))
_off2 = (np.arange(B) * N_FRAME)[:, None]
W2 = np.bincount((_ix2 + _off2).ravel(),
                 minlength=B * N_FRAME).reshape(B, N_FRAME).astype(np.float64)
w("%-16s %-6s %-17s %12s %12s %10s %10s"
  % ("arm", "pop", "state", "paired w", "unpaired w", "ratio", "rejected"))
rejected = 0
probed = 0
for arm in ARMS:
    for pop in POPS:
        counts = z["counts__%s__%s" % (arm, pop)]
        fil, _ = recompute(counts)
        agg2 = (W2 @ counts.reshape(N_FRAME, 6)).reshape(B, 3, 2)
        ret2, exc2 = agg2[:, :, 0], agg2[:, :, 1]
        unf2 = 100.0 * (ret2 + exc2) / (ret2 + exc2).sum(axis=1)[:, None]
        bad = fil - unf2                      # UNPAIRED
        for j, s in enumerate(STATES):
            blo, bhi = pctl(bad, j)
            pmlo, pmhi = pub_mov["movement_%s_%s_%s_b" % (arm, pop, s)]
            d = max(abs(blo - pmlo), abs(bhi - pmhi))
            probed += 1
            rej = d > TOL
            rejected += int(rej)
            w("%-16s %-6s %-17s %12.6f %12.6f %10.1fx %10s"
              % (arm, pop, s, pmhi - pmlo, bhi - blo, (bhi - blo) / (pmhi - pmlo),
                 "YES" if rej else "NO -- PROBE FAILED"))
w("")
w("    intervals probed  : %d" % probed)
w("    intervals rejected: %d" % rejected)
if rejected != probed:
    sys.exit("HARD STOP: the unpaired construction was NOT rejected on every interval. A test "
             "that passes on the wrong construction is not a test of the property it names.")
w("    THE PROBE IS REJECTED ON EVERY ONE OF THE %d INTERVALS. The comparison in section 1 is"
  % probed)
w("    therefore sensitive to the pairing and not merely to the arithmetic: it distinguishes a")
w("    within-replicate difference from a difference of two independent draws, and the unpaired")
w("    interval is wider by the factors above.")
w("")
w("=" * 94)
w("END. Adopts nothing. Zero API calls. Counts only; boot_weights.npz was read, not published.")
w("=" * 94)

with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
print("\nrun record: logs/step9_b_pairing_evidence.txt")
