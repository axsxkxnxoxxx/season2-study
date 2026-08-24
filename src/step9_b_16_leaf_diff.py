#!/usr/bin/env python3
"""Step 9, arm `b` -- leaf-by-leaf diff of the FINAL emitted files against their predecessors.

WHY THIS EXISTS ALONGSIDE `verify_against_previous()` IN src/step9_b_7_emit_corrected.py.

That check runs INSIDE the emitter, and it has to run there: its result is EMBEDDED in the
document, so it cannot compare a document that already contains it.  It therefore compares the
document AS IT STANDS PART-WAY THROUGH CONSTRUCTION, before the emitter appends its own
`$.notes.step9_b_*` records -- which makes every one of those notes look LOST and their
replacements look ADDED.  Measured on the decisions/0125 rerun: it reported 8 lost and 3 added
where the finished files differ by ONE deliberately renamed key.

That is a report artifact and not a movement, but "8 leaves lost" is exactly the kind of line a
reader is entitled to take at face value, so it is not left standing alone.  THIS SCRIPT
COMPARES THE FINISHED BYTES ON DISK against the same paths at a NAMED COMMIT -- the
commit-qualified reference decisions/0125 SS6 makes routine -- and reports:

  * every numeric leaf that moved, classified as a CI endpoint, a CI-derived ratio, a leaf of
    THE EMISSION'S OWN RUN RECORD -- a declared class, listed by path, which cannot be equal
    across two runs without the comparison it records being trivial -- or NEITHER;
  * every leaf present in one file and absent from the other, by path;
  * its own COVERAGE, because an empty result and a clean result are the same value.

A leaf that is NEITHER is a hard stop.  So is a comparison that examined nothing.

AND THE HARD STOP IS SHOWN FIRING.  A check that cannot fail on the vector it polices is not a
check (decisions/0123 SS3), and this one's passing verdict is only worth reading if its failing
one is reachable.  `--probe` moves a single PROTECTED figure -- a point estimate -- in an
in-memory copy and re-runs the identical classification, which must report it as NEITHER and
exit non-zero.  It touches no file.

WHAT IT DOES NOT DO.  It writes no artifact and adopts nothing.  Zero API calls.  It reads only
this arm's own files and this arm's own history.

Run:  python3 src/step9_b_16_leaf_diff.py [<commit>]
      -> logs/step9_b_leaf_diff.txt
"""

import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLOG = os.path.join(ROOT, "logs", "step9_b_leaf_diff.txt")

# The commit that carried the pre-decisions/0125 emission at these same paths. A bare path plus a
# hash resolves only until something else occupies the path; a commit-qualified path resolves
# forever (decisions/0125 SS6).
ARGV = [x for x in sys.argv[1:] if x != "--probe"]
PROBE = "--probe" in sys.argv
PREV_REV = ARGV[0] if ARGV else "5393430"

FILES = [
    "artifacts/step9-headline-corrected-2026-08-21-b.json",
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
]

CI_ENDPOINT = re.compile(r"\.ci\.(lower|upper)$")
CI_DERIVED_RATIO = re.compile(r"\.bound_over_sampling_width_ratios\.[a-z_]+\.value$")

# A THIRD CLASS, DECLARED AND COUNTED RATHER THAN SILENTLY DROPPED. `$._emission` is the record
# OF THE EMISSION ITSELF -- its leaf-verification counts, its source hashes, its timestamp. Those
# leaves CANNOT be equal across two runs without the comparison they record being trivial: the
# previous emission's record says how many leaves ITS predecessor had, and this one's says how
# many THIS one's predecessor had. Calling them movements would make every rerun fail on its own
# bookkeeping; hiding them would let a figure hide behind the word `_emission`. So they are
# separated, COUNTED, and every one is listed by path -- and if a leaf under this prefix ever
# looked like a figure, it would be visible in that list.
EMISSION_RECORD = re.compile(r"^\$\._emission\.")

REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


def leaves(obj, prefix="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, "%s.%s" % (prefix, k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, "%s[%d]" % (prefix, i))
    else:
        yield prefix, obj


def numeric(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


w("=" * 94)
w("STEP 9, ARM b -- LEAF-BY-LEAF DIFF OF THE FINISHED FILES, AGAINST git %s" % PREV_REV)
w("=" * 94)
w("")
w("This compares THIS ARM's files against THIS ARM's own history. It says nothing about the")
w("other arm, which this arm does not see, and nothing about the stamped originals, which are")
w("settled and untouched.")
w("")

total_examined = 0
total_moved = 0
hard_stop = []

for rel in FILES:
    cur = json.load(open(os.path.join(ROOT, rel)))
    prev = json.loads(subprocess.check_output(
        ["git", "-C", ROOT, "show", "%s:%s" % (PREV_REV, rel)]))
    a, b = dict(leaves(prev)), dict(leaves(cur))
    common = [p for p in a if p in b]
    num = [p for p in common if numeric(a[p]) and numeric(b[p])]
    moved = [p for p in num if a[p] != b[p]]
    endpoints = [p for p in moved if CI_ENDPOINT.search(p)]
    ratios = [p for p in moved if CI_DERIVED_RATIO.search(p) and not CI_ENDPOINT.search(p)]
    record = [p for p in moved if EMISSION_RECORD.search(p)]
    neither = [p for p in moved
               if not CI_ENDPOINT.search(p) and not CI_DERIVED_RATIO.search(p)
               and not EMISSION_RECORD.search(p)]
    if PROBE:
        # THE PROBE. Move one PROTECTED figure -- the first `.value_percent` leaf both files
        # carry -- by a value no rounding could produce, in memory only, and let the same
        # classification run. It must land in NEITHER.
        # A PROTECTED FIGURE IN WHICHEVER SHAPE THIS FILE CARRIES. The headline names its point
        # estimates `.value_percent`; the working-figures extract names them `.value` under
        # `$.figures`. A probe that knew only the first hard-stopped on the second -- correctly,
        # under the looked-nowhere rule, but it also meant the probe could not complete.
        cand = ([p for p in num if p.endswith(".value_percent")]
                or [p for p in num if p.startswith("$.figures.") and p.endswith(".value")])
        if not cand:
            sys.exit("HARD STOP: the probe found no protected figure to move in %s, so it "
                     "would have reported clean by looking nowhere." % rel)
        b = dict(b)
        b[cand[0]] = a[cand[0]] + 1.0
        moved = [p for p in num if a[p] != b[p]]
        endpoints = [p for p in moved if CI_ENDPOINT.search(p)]
        ratios = [p for p in moved if CI_DERIVED_RATIO.search(p) and not CI_ENDPOINT.search(p)]
        record = [p for p in moved if EMISSION_RECORD.search(p)]
        neither = [p for p in moved
                   if not CI_ENDPOINT.search(p) and not CI_DERIVED_RATIO.search(p)
                   and not EMISSION_RECORD.search(p)]
        w("    PROBE ACTIVE: %s moved by +1.0 in memory. No file is touched." % cand[0])

    strings_moved = [p for p in common if isinstance(a[p], str) and a[p] != b[p]]
    lost = sorted(p for p in a if p not in b)
    added = sorted(p for p in b if p not in a)

    total_examined += len(num)
    total_moved += len(moved)

    w("-" * 94)
    w(rel)
    w("-" * 94)
    w("    leaves in %s / on disk / compared : %d / %d / %d"
      % (PREV_REV, len(a), len(b), len(common)))
    w("    NUMERIC leaves compared               : %d" % len(num))
    w("    numeric leaves MOVED                  : %d" % len(moved))
    w("      of which CI endpoints               : %d" % len(endpoints))
    w("      of which CI-derived ratios          : %d" % len(ratios))
    w("      of which the EMISSION'S OWN RECORD  : %d  (declared class, listed below)"
      % len(record))
    w("      of which NEITHER                    : %d" % len(neither))
    for p in record:
        w("        RECORD  %s : %r -> %r" % (p, a[p], b[p]))
    w("    string leaves moved                   : %d  (prose, provenance and restated widths)"
      % len(strings_moved))
    w("    leaves lost / added                   : %d / %d" % (len(lost), len(added)))
    lost_record = [p for p in lost if EMISSION_RECORD.search(p)]
    added_record = [p for p in added if EMISSION_RECORD.search(p)]
    w("      lost/added inside the emission record : %d / %d  (same declared class)"
      % (len(lost_record), len(added_record)))
    for p in lost:
        w("        LOST  %s%s" % (p, "   [emission record]" if p in lost_record else ""))
    for p in added:
        w("        ADDED %s  (numeric: %s)%s"
          % (p, numeric(b[p]), "   [emission record]" if p in added_record else ""))
    if neither:
        hard_stop.append((rel, neither))
        for p in neither[:20]:
            w("        NEITHER %s : %r -> %r" % (p, a[p], b[p]))
    if not num:
        hard_stop.append((rel, ["NO NUMERIC LEAF WAS COMPARED AT ALL"]))
    w("")

w("=" * 94)
w("    files compared                    : %d" % len(FILES))
w("    numeric leaves examined, in total  : %d" % total_examined)
w("    numeric leaves moved, in total     : %d" % total_moved)
if PROBE and not hard_stop:
    w("    VERDICT: PROBE FAILED -- a moved point estimate was NOT reported. A check that passes")
    w("             on the wrong vector is not a check.")
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit("HARD STOP: the probe did not trip the classification.")
if hard_stop:
    w("    VERDICT: FAIL%s" % ("  (EXPECTED -- probe mode)" if PROBE else ""))
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit("HARD STOP: %s" % hard_stop)
w("    VERDICT: every moved numeric leaf is a CI endpoint, a ratio derived from a CI width, or")
w("             a leaf of the emission's own run record -- a class that is declared above,")
w("             listed by path, and cannot be equal across two runs without the comparison it")
w("             records being trivial.")
w("=" * 94)
w("END. Adopts nothing. Zero API calls.")

with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
print("\nrun record: logs/step9_b_leaf_diff.txt")
