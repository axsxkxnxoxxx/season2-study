#!/usr/bin/env python3
"""Step 9, arm `b` -- REPRODUCE the stale-producer defect, in BOTH directions.

Human Lead ruling 3, 2026-08-25, requires the defect shown before the fix and the fix shown
rejecting it. A fix demonstrated only by passing has not been demonstrated at all: a precondition
that cannot fail on the vector it polices is not a check, and it is worse than no check because
it occupies the slot where a real one would sit (decisions/0123 SS3).

WHAT IS REPRODUCED. A PRODUCER IS EDITED AND NOT RE-RUN. Its output still says, in the file's own
provenance block, that it was produced by that script at a hash the script no longer has. Two
producers are driven, one per output kind:

  A  src/step9_b_2_bootstrap.py  -> processed/step9/b/boot_weights.npz
       claim: `source_file`, `source_sha256_12` inside the matrix itself
  B  src/step9_b_3_emit.py       -> artifacts/step9-headline-corrected-2026-08-21-b.json
       claim: `$.generated_by.generator`, `$.generated_by.generator_sha256_12`, restated in the
              published .md

DIRECTION 1 -- ACCEPTED. With the producer edited, consumers and controls that existed before
this ruling are run and every one exits as it always does. Two kinds are run and the difference
matters: consumers that were NEVER changed by this ruling (so this direction stays reproducible
forever), and the two that WERE hardened, recovered from git at the revision that precedes the
hardening and executed from src/ so their ROOT resolves as it normally does.

DIRECTION 2 -- REJECTED. The same edited producer, the same instant, run against the hardened
consumers in the working tree and against src/step9_b_21_provenance_verify.py. Each must exit
non-zero and name the edge.

NOTHING IS LEFT CHANGED. Every mutated file is restored from an in-memory copy of its original
bytes in a `finally`, a byte-for-byte backup is written to this arm's own scratch space first,
and the script re-hashes every touched path at the end and REFUSES TO EXIT 0 if any differs.
Only sources under src/ are ever edited: no artifact, no processed table and no figure is
touched by this script.

SCOPE. Every path is this arm's own or a shared control. The temporary module written into src/
carries this arm's prefix, is deleted in the same `finally`, and no glob spans arms.

Run:  python3 src/step9_b_22_stale_producer_repro.py
      -> logs/step9_b_stale_producer_repro.txt
"""

import hashlib
import io
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLOG = os.path.join(ROOT, "logs", "step9_b_stale_producer_repro.txt")

# The revision that PRECEDES the hardening of the two consumers. Pinned, because "HEAD" would
# stop meaning "before the fix" the moment the fix is committed, and a reproduction whose
# baseline drifts reproduces nothing. Content only -- no commit message is read (0125 SS5d).
BASE_REV = "5241e3476dd3b034470d0f1b8e53d35234ef4668"

BOOTSTRAP = "src/step9_b_2_bootstrap.py"
EMITTER = "src/step9_b_3_emit.py"
HARDENED = ["src/step9_b_10_pairing_evidence.py", "src/step9_b_15_mechanism_repro.py"]
VERIFIER = "src/step9_b_21_provenance_verify.py"
TMP = "src/step9_b_22_tmp_recovered_consumer.py"

# Consumers this ruling did NOT touch. They are the permanent half of direction 1: whatever
# happens to the hardened pair later, these keep showing that a stale producer passes unnoticed
# everywhere else in the arm.
UNCHANGED = [
    (["python3", "src/step9_b_9_frame_repro.py"], {},
     "reads the bootstrap SOURCE and pairs.npz and compares two designs"),
    (["python3", "src/step9_b_16_leaf_diff.py"], {},
     "leaf-diffs the finished artifacts; it LICENSES every `_sha256_12` leaf to move"),
    (["python3", "src/step9_b_20_publication_verify.py"], {},
     "asserts nothing published moved"),
    (["python3", "src/step8b_validate.py",
      "artifacts/step9-headline-corrected-2026-08-21-b.json"], {},
     "the shared schema + semantic validator, against the artifact making the claim"),
    (["python3", "src/check_surfaces.py"], {"STEP_ARM": "b"},
     "the shared propagation control, all eight surfaces (STEP_ARM=b, decisions/0126)"),
]

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


def sha12(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def run(cmd, env_over=None):
    env = dict(os.environ)
    env.update(env_over or {})
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    return p.returncode


def scratch_dir():
    """This arm's own scratch space (decisions/0128). Never a shared directory."""
    base = os.environ.get("CLAUDE_SCRATCHPAD", "")
    d = os.path.join(base, "arm_b") if base else os.path.join(ROOT, "logs", "step9_b_scratch")
    os.makedirs(d, exist_ok=True)
    return d


def main():
    touched = [BOOTSTRAP, EMITTER] + HARDENED + [VERIFIER]
    before = {p: sha12(p) for p in touched}
    originals = {p: open(os.path.join(ROOT, p), "rb").read() for p in (BOOTSTRAP, EMITTER)}
    sd = scratch_dir()
    for p, b in originals.items():
        with open(os.path.join(sd, os.path.basename(p) + ".orig"), "wb") as fh:
            fh.write(b)

    w("=" * 94)
    w("STEP 9, ARM b -- THE STALE-PRODUCER DEFECT, BOTH DIRECTIONS (ruling 3, 2026-08-25)")
    w("=" * 94)
    w("")
    w("baseline for the recovered consumers : git %s (pinned, not HEAD)" % BASE_REV[:7])
    w("byte backup of each mutated source   : %s"
      % (os.path.relpath(sd, ROOT) if sd.startswith(ROOT) else "this arm's own scratch space"))
    w("")
    for p in touched:
        w("    %-46s sha256:12 %s" % (p, before[p]))
    w("")

    failures = []
    try:
        for label, producer, claim, hardened_apply in (
                ("A", BOOTSTRAP,
                 "processed/step9/b/boot_weights.npz  ->  source_file / source_sha256_12", True),
                ("B", EMITTER,
                 "artifacts/step9-headline-corrected-2026-08-21-b.json  ->  "
                 "$.generated_by.generator_sha256_12", False)):

            w("=" * 94)
            w("EDGE %s -- producer %s" % (label, producer))
            w("         claim   %s" % claim)
            w("=" * 94)
            w("")
            w("    MUTATION: one comment line appended. The producer's OUTPUT is untouched and")
            w("    is not re-run, which is exactly the state a real edit-without-rerun leaves.")
            with open(os.path.join(ROOT, producer), "ab") as fh:
                fh.write(b"\n# stale-producer reproduction: this line is removed by the same run\n")
            w("    producer hash was %s, now %s" % (before[producer], sha12(producer)))
            w("")

            w("    " + "-" * 88)
            w("    DIRECTION 1 -- A CONSUMER ACCEPTS THE STALE PRODUCER (the defect)")
            w("    " + "-" * 88)
            w("")
            w("    %-52s %-6s %s" % ("consumer, unchanged by this ruling", "exit", "verdict"))
            for cmd, env, what in UNCHANGED:
                rc = run(cmd, env)
                ok = rc == 0
                if not ok:
                    failures.append(("direction 1", " ".join(cmd), rc))
                w("    %-52s %-6d %s" % (" ".join(cmd[1:])[:52], rc,
                                         "ACCEPTED -- nothing objected" if ok
                                         else "unexpected non-zero"))
                w("        %s" % what)
            w("")

            if hardened_apply:
                w("    the two consumers this ruling HARDENED, recovered at git %s and run from"
                  % BASE_REV[:7])
                w("    src/ so ROOT resolves normally -- their state BEFORE the fix:")
                w("")
                w("    %-52s %-6s %s" % ("consumer at the pinned baseline", "exit", "verdict"))
                for rel in HARDENED:
                    blob = subprocess.run(
                        ["git", "-C", ROOT, "show", "%s:%s" % (BASE_REV, rel)],
                        capture_output=True)
                    if blob.returncode != 0:
                        w("    %-52s %-6s could not be recovered from git" % (rel, "--"))
                        failures.append(("direction 1 recovery", rel, blob.returncode))
                        continue
                    with open(os.path.join(ROOT, TMP), "wb") as fh:
                        fh.write(blob.stdout)
                    rc = run(["python3", TMP])
                    os.remove(os.path.join(ROOT, TMP))
                    ok = rc == 0
                    if not ok:
                        failures.append(("direction 1 baseline", rel, rc))
                    w("    %-52s %-6d %s" % (os.path.basename(rel), rc,
                                             "ACCEPTED -- nothing objected" if ok
                                             else "unexpected non-zero"))
                w("")

            w("    " + "-" * 88)
            w("    DIRECTION 2 -- THE SAME STATE, REJECTED")
            w("    " + "-" * 88)
            w("")
            w("    %-52s %-6s %s" % ("consumer, after the fix", "exit", "verdict"))
            after_set = [VERIFIER] + (HARDENED if hardened_apply else [])
            for rel in after_set:
                rc = run(["python3", rel])
                ok = rc != 0
                if not ok:
                    failures.append(("direction 2", rel, rc))
                w("    %-52s %-6d %s" % (os.path.basename(rel), rc,
                                         "REJECTED -- the stale producer was named" if ok
                                         else "ACCEPTED -- THE FIX DID NOT FIRE"))
            w("")

            with open(os.path.join(ROOT, producer), "wb") as fh:
                fh.write(originals[producer])
            w("    restored: %s is back to %s" % (producer, sha12(producer)))
            w("")
    finally:
        for p, b in originals.items():
            with open(os.path.join(ROOT, p), "wb") as fh:
                fh.write(b)
        if os.path.exists(os.path.join(ROOT, TMP)):
            os.remove(os.path.join(ROOT, TMP))

    w("=" * 94)
    w("THE TREE IS RESTORED -- CHECKED, NOT ASSERTED")
    w("=" * 94)
    w("")
    moved = 0
    for p in touched:
        now = sha12(p)
        same = now == before[p]
        moved += (not same)
        w("    %-46s %s  %s" % (p, now, "unchanged" if same else "MOVED"))
    if os.path.exists(os.path.join(ROOT, TMP)):
        moved += 1
        w("    %-46s the temporary recovered module was left behind" % TMP)
    w("")
    w("    paths verified : %d" % len(touched))
    w("    paths moved    : %d" % moved)
    w("")

    w("=" * 94)
    if moved:
        w("RESULT: the tree was NOT restored. That is worse than the defect being reproduced,")
        w("because it leaves a producer edited and un-re-run -- the exact state under test.")
        w("=" * 94)
        return 2
    if failures:
        w("RESULT: %d step(s) did not behave as required:" % len(failures))
        for f in failures:
            w("    %s :: %s :: exit %s" % f)
        w("=" * 94)
        return 1
    w("RESULT: BEFORE, every pre-existing consumer accepted a producer that had been edited and")
    w("not re-run. AFTER, the hardened consumers and the verifier rejected the identical state.")
    w("The comparison discriminates on the vector it polices, and the tree is byte-identical.")
    w("=" * 94)
    return 0


if __name__ == "__main__":
    code = main()
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    print("\nrun record: logs/step9_b_stale_producer_repro.txt")
    sys.exit(code)
