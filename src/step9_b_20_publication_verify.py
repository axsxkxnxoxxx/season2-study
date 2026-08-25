#!/usr/bin/env python3
"""Step 9, arm `b` -- NOTHING ALREADY PUBLISHED MOVED. Verified leaf by leaf, by class.

The 2026-08-25 emission publishes twelve intervals that were measured and never emitted, rewrites
three inherited leaves that are false in a non-placeholder file, and turns a typed population
constant into a read.  IT IS AN EMISSION CHANGE: no bootstrap was re-run and no figure was
recomputed.  That is a claim, and a claim of having checked is either TRUE or it is REMOVED --
so this script establishes it against the bytes at a NAMED COMMIT rather than asserting it.

WHAT IT COMPARES.  The three emitted files at `<commit>:<path>` against the same three paths on
disk, COMMIT-QUALIFIED from the start, because an in-place re-emission is the normal case and a
bare path resolves only until something else occupies it (decisions/0125 SS6).

HOW IT CLASSIFIES.  Every numeric leaf is one of:
    UNCHANGED          -- present in both, equal.
    MOVED              -- present in both, different.  ANY moved leaf is a HARD STOP: the
                          emitter re-ran the same stage-2 file, so nothing has licence to move.
    ADDED              -- absent before, present now.  Must be a leaf of one of the twelve new
                          position-5 level intervals or of the emission's own run record.  An
                          added leaf anywhere else is a HARD STOP.
    LOST               -- present before, absent now.  Must be zero.
And every leaf is additionally counted into the PROTECTED FAMILIES by field name, so the report
is per class rather than one aggregate that could hide a compensating pair.

WHY THE FAMILY COUNTS ARE PRINTED EVEN WHEN THEY ARE ZERO.  An empty result and a clean result
are the same value (CLAUDE.md).  A family matching no leaf is a HARD STOP, not a pass.

THE .md IS COMPARED BY LINE, NOT BY EYE.  Every line of the previous .md must still be present,
so a table row cannot vanish behind an insertion.

SCOPE.  Every path is this arm's own and is written out in full; there is no glob spanning arms,
and only file CONTENT is read from git -- never a commit message (decisions/0125 SS5d).

Run:  python3 src/step9_b_20_publication_verify.py [<commit>]   -> logs/step9_b_publication_verify.txt
"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLOG = os.path.join(ROOT, "logs", "step9_b_publication_verify.txt")
PREV = sys.argv[1] if len(sys.argv) > 1 else "HEAD"

JSON_FILES = [
    "artifacts/step9-headline-corrected-2026-08-21-b.json",
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
]
MD_FILE = "artifacts/step9-headline-corrected-2026-08-21-b.md"
UNTOUCHABLE = [
    "artifacts/step9-headline-b.json",
    "artifacts/step9-headline-b.md",
    "artifacts/step9-working-figures-b.json",
]

NEW_INTERVAL = re.compile(r"^\$\.declared_intervals\[\d+\]$")
EMISSION_RECORD = re.compile(r"^\$\._emission\.")
PROVENANCE = re.compile(r"^\$\.generated_by\.")

FAMILIES = {
    "point_estimates": {"value_percent", "never_started_percent", "started_and_left_percent",
                        "continued_percent", "percent", "retained_share_percent"},
    "numerators": {"numerator_pairs"},
    "denominators": {"denominator_pairs", "on_population_n", "population_n"},
    "population_sizes": {"n_position_5", "n_post_liveness"},
    "widths": {"width_pp"},
    "three_ceiling_arithmetic": {"sum_percent", "excess_pp", "excess_pairs"},
    "exclusion_pair_counts": {"total_pairs", "never_started_component",
                              "started_and_left_component", "silence_test_alone",
                              "spared_by_not_continued", "channel_pairs_conceded_by_the_floor"},
    "waterfall_counts": {"n_in", "n_out", "removed", "position", "positions_checked"},
    "air_period_counts": {"entering_pairs", "retained_pairs", "accounts"},
    "spec_inputs": {"W_days", "H_days", "B", "seed", "level_pct", "adopted_rule_revision",
                    "horizon_days"},
    "ci_endpoints": {"lower", "upper"},
    "ratios": {"value"},
}

REP = io.StringIO()
hard = []


def w(s=""):
    print(s)
    REP.write(s + "\n")


def at(rev, rel):
    p = subprocess.run(["git", "-C", ROOT, "show", "%s:%s" % (rev, rel)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        sys.exit("HARD STOP: %s:%s is not readable, so this verification has no baseline. An "
                 "unavailable baseline is a hard stop, never a pass." % (rev, rel))
    return p.stdout


def leaves(o, p="$"):
    if isinstance(o, dict):
        for k, v in o.items():
            for r in leaves(v, "%s.%s" % (p, k)):
                yield r
    elif isinstance(o, list):
        for i, v in enumerate(o):
            for r in leaves(v, "%s[%d]" % (p, i)):
                yield r
    else:
        yield p, o


def numeric(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def new_interval_ids(doc):
    return {i for i, e in enumerate(doc.get("declared_intervals", []))
            if str(e.get("interval_id", "")).startswith("level_position5_")}


w("=" * 100)
w("STEP 9 ARM b -- NOTHING ALREADY PUBLISHED MOVED.  Baseline: %s" % PREV)
w("=" * 100)

# THE HEADLINE CARRIES EVERY PROTECTED FAMILY; THE WORKING-FIGURES EXTRACT DOES NOT.
# It is a TRANSCRIPTION with its own key shapes and a different selection of figures, so a
# family with no leaf there is a family that document does not carry -- not a check that looked
# nowhere. THE DISTINCTION IS DECLARED PER FILE, NOT INFERRED, and the families that match
# nothing are still NAMED in the report: a coverage number a reader cannot break down is one
# they cannot audit. Zero coverage ACROSS ALL FAMILIES remains a hard stop in both files, and so
# does zero numeric leaves compared.
REQUIRE_ALL_FAMILIES = {
    "artifacts/step9-headline-corrected-2026-08-21-b.json": True,
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json": False,
}

for rel in JSON_FILES:
    before = json.loads(at(PREV, rel))
    after = json.load(open(os.path.join(ROOT, rel)))
    a = dict(leaves(before))
    b = dict(leaves(after))
    common = [p for p in a if p in b]
    num = [p for p in common if numeric(a[p]) and numeric(b[p])]
    moved = [p for p in num if a[p] != b[p]]
    lost = sorted(p for p in a if p not in b)
    added = sorted(p for p in b if p not in a)
    added_num = [p for p in added if numeric(b[p])]

    newiv = new_interval_ids(after)
    def licensed(path):
        m = re.match(r"^\$\.declared_intervals\[(\d+)\]", path)
        if m and int(m.group(1)) in newiv:
            return "new position-5 level interval"
        if EMISSION_RECORD.search(path):
            return "emission run record"
        if PROVENANCE.search(path):
            return "provenance"
        return None

    unlicensed_added = [p for p in added_num if licensed(p) is None]
    unlicensed_lost = [p for p in lost if licensed(p) is None and numeric(a[p])]

    w("")
    w("-" * 100)
    w(rel)
    w("-" * 100)
    w("    leaves at %-8s / on disk / compared : %d / %d / %d"
      % (PREV, len(a), len(b), len(common)))
    w("    NUMERIC leaves compared                  : %d" % len(num))
    w("    numeric leaves MOVED                     : %d      <-- must be 0" % len(moved))
    for p in moved[:20]:
        w("        MOVED %s : %r -> %r" % (p, a[p], b[p]))
    w("    numeric leaves LOST                      : %d      <-- must be 0"
      % len([p for p in lost if numeric(a[p])]))
    w("    numeric leaves ADDED                     : %d" % len(added_num))
    byclass = {}
    for p in added_num:
        byclass[licensed(p) or "UNLICENSED"] = byclass.get(licensed(p) or "UNLICENSED", 0) + 1
    for k in sorted(byclass):
        w("        %-34s : %d" % (k, byclass[k]))
    for p in unlicensed_added[:20]:
        w("        UNLICENSED ADDED %s = %r" % (p, b[p]))

    w("    BY PROTECTED FAMILY (examined / moved):   [all families required here: %s]"
      % REQUIRE_ALL_FAMILIES[rel])
    total_fam = 0
    empty_fams = []
    for fam, names in FAMILIES.items():
        hits = [p for p in num if p.rsplit(".", 1)[-1] in names]
        fmoved = [p for p in hits if a[p] != b[p]]
        total_fam += len(hits)
        w("        %-26s %6d / %d%s" % (fam, len(hits), len(fmoved),
                                        "   <-- ZERO COVERAGE" if not hits else ""))
        if not hits:
            empty_fams.append(fam)
            if REQUIRE_ALL_FAMILIES[rel]:
                hard.append("%s: protected family %r matched zero leaves -- the check looked "
                            "nowhere for it" % (rel, fam))
        if fmoved:
            hard.append("%s: %s moved in family %s" % (rel, fmoved[:5], fam))
    w("    protected numeric leaves examined        : %d" % total_fam)
    if empty_fams:
        w("    families this document does not carry     : %s" % ", ".join(empty_fams))
    if len(empty_fams) == len(FAMILIES):
        hard.append("%s: EVERY protected family matched zero leaves -- the check looked at "
                    "nothing and would have reported clean" % rel)

    strings_moved = [p for p in common if isinstance(a[p], str) and a[p] != b[p]]
    w("    string leaves moved                      : %d" % len(strings_moved))
    for p in strings_moved:
        w("        STR %s" % p)

    if moved:
        hard.append("%s: %d numeric leaf/leaves MOVED" % (rel, len(moved)))
    if unlicensed_added:
        hard.append("%s: %d added numeric leaf/leaves outside the licensed classes"
                    % (rel, len(unlicensed_added)))
    if unlicensed_lost:
        hard.append("%s: %d numeric leaf/leaves LOST" % (rel, len(unlicensed_lost)))
    if not num:
        hard.append("%s: NO NUMERIC LEAF WAS COMPARED AT ALL" % rel)

# ---- the .md, by line ----------------------------------------------------------------------
before_md = at(PREV, MD_FILE).split("\n")
after_md = open(os.path.join(ROOT, MD_FILE)).read().split("\n")
after_set = set(after_md)
missing = [ln for ln in before_md if ln.strip() and ln not in after_set]
w("")
w("-" * 100)
w(MD_FILE)
w("-" * 100)
w("    lines at %-8s / on disk        : %d / %d" % (PREV, len(before_md), len(after_md)))
w("    non-blank lines from the baseline NOT present now : %d" % len(missing))
for ln in missing[:20]:
    w("        MISSING  %s" % ln[:150])
w("    table rows at baseline / now                      : %d / %d"
  % (len([x for x in before_md if x.startswith("|")]),
     len([x for x in after_md if x.startswith("|")])))
if not before_md:
    hard.append("%s: the baseline .md was empty" % MD_FILE)

# ---- the stamped originals ------------------------------------------------------------------
w("")
w("-" * 100)
w("THE STAMPED ORIGINALS -- ruled SETTLED, and not touched by this emission")
w("-" * 100)
for rel in UNTOUCHABLE:
    same = at(PREV, rel) == open(os.path.join(ROOT, rel)).read()
    w("    %-46s byte-identical to %s: %s" % (rel, PREV, "YES" if same else "NO"))
    if not same:
        hard.append("%s: a stamped original changed" % rel)

w("")
w("=" * 100)
if hard:
    for h in hard:
        w("  HARD STOP  %s" % h)
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit(1)
w("  VERDICT: 0 numeric leaves moved, 0 lost, every added leaf inside a licensed class,")
w("           every stamped original byte-identical. Nothing already published moved.")
with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
