#!/usr/bin/env python3
"""Step 9, arm `b` -- VERSION-ONLY MIGRATION VERIFIER (schema v1.9.0 -> v1.10.0).

WHY THIS EXISTS ALONGSIDE src/step9_b_16_leaf_diff.py. That script walks NUMERIC leaves and
hard-stops on a numeric movement it cannot classify; string movements it reports only as a
COUNT. That is the right shape for a rerun whose whole expected movement is numeric -- the
decisions/0125 re-draw -- and it is the WRONG shape here. A VERSION MIGRATION'S ENTIRE EXPECTED
MOVEMENT IS A STRING: `$.schema_version` and `$.schema_id`. A check that counts string
movements without naming them would report "7 string leaves moved" on a run whose correctness
claim is exactly "the only strings that moved are the two version identifiers", and the reader
could not tell the passing case from the failing one.

So this walks EVERY leaf -- string, numeric, boolean and null -- against a NAMED COMMIT, and
puts every moved, added and absent leaf into exactly one of four classes:

  VERSION_IDENTIFIER      the leaf carries the schema version and moved by exactly the version
                          token: substituting 1.9.0 -> 1.10.0 in the OLD value reproduces the
                          NEW value, character for character. Not "contains a version-ish
                          string" -- reproduces it.
  RUN_RECORD              a leaf of the emission's own bookkeeping: its timestamp, its git
                          head, its generator hash, its source/emitted hashes, and the
                          `$._emission` block, whose counts record how many leaves ITS
                          predecessor had. These cannot be equal across two runs without the
                          comparison they record being trivial. Declared by path, listed in
                          full, never inferred.
  SCHEMA_TEXT_v1_10_0     text this arm does not author and did not retype: it is inherited
                          verbatim from artifacts/step8b-placeholder-arm-file.json through the
                          emitter's existing `tpl[...]` reads. MEMBERSHIP IS TESTED AGAINST THE
                          SOURCE, not against a shape: the value must be byte-identical to the
                          v1.10.0 template's value at the same path AND differ from (or be
                          absent in) the v1.9.0 template's. A leaf that merely LOOKS like
                          schema prose does not qualify.
  NEITHER                 anything else. HARD STOP.

AND ANY NUMERIC MOVEMENT OUTSIDE RUN_RECORD IS A HARD STOP ON ITS OWN, before classification,
because the ruling this run answers says NOTHING MOVES -- no figure, no CI endpoint, no bound.

THE CLASSIFIER IS SHOWN REJECTING BEFORE IT IS TRUSTED PASSING (decisions/0123 SS3: a
precondition that cannot fail on the vector it polices is not a check, and a calendar-window
test that passes on a vector wrong in every entry is the example). `--probe` runs four
constructed vectors in memory, touching no file:

  1. a point estimate moved by +1.0                  -> must be NEITHER, and a numeric stray
  2. a CI endpoint moved                             -> must be NEITHER, and a numeric stray
  3. a string rewritten to a DIFFERENT version token -> must be NEITHER, not VERSION_IDENTIFIER
     (this is the one a "contains 1.10.0" test would wave through)
  4. a schema-inherited leaf rewritten by one word   -> must be NEITHER, because the
     set-membership test against the template fails

Each must be reported and the run must exit non-zero. A probe that does not trip the
classification is itself a hard stop.

SCOPE. It reads this arm's own artifacts, this arm's own history, and the SHARED schema and
template, which are spec. It never names, reads or globs another arm's namespace: every path is
literal and every git invocation is `--format=%H`-free and path-qualified, so no commit message
body is fetched (decisions/0125 SS5d -- messages before 2026-08-24 carry cross-arm content).

It writes no artifact, adopts nothing, and makes zero API calls.

Run:  python3 src/step9_b_18_version_migration_verify.py [<commit>] [--probe]
      -> logs/step9_b_version_migration_verify.txt
"""

import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTLOG = os.path.join(ROOT, "logs", "step9_b_version_migration_verify.txt")

ARGV = [x for x in sys.argv[1:] if x != "--probe"]
PROBE = "--probe" in sys.argv
BASE_REV = ARGV[0] if ARGV else "3e8653e"

OLD_VER, NEW_VER = "1.9.0", "1.10.0"

JSON_FILES = [
    "artifacts/step9-headline-corrected-2026-08-21-b.json",
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
]
MD_FILE = "artifacts/step9-headline-corrected-2026-08-21-b.md"

TEMPLATE = "artifacts/step8b-placeholder-arm-file.json"

# THE RUN-RECORD CLASS, DECLARED BY PATH. Nothing is admitted here that could carry a
# measurement: every entry is a timestamp, a content hash, a git head, or a count the emission
# keeps about its own comparison with its predecessor.
RUN_RECORD = [
    re.compile(r"^\$\._emission\."),
    re.compile(r"\.generated_at_utc$"),
    re.compile(r"^\$\.generated_at_utc$"),
    re.compile(r"\.git_head_short$"),
    re.compile(r"\.generator_sha256_12$"),
    re.compile(r"_sha256_12$"),
    re.compile(r"^\$\.provenance\.emitted_at_utc$"),
]

# THE SAME CLASS, RENDERED AS PROSE, AND ADMITTED BY EXACT LITERAL PATH RATHER THAN BY PATTERN.
# These two notes are the emission's bookkeeping written as sentences: the first prints the
# source hash, the promotion timestamp and the git head; the second prints the counts from the
# emitter's own leaf verification against its predecessor ("N leaves compared, of which M are
# numeric; K numeric leaves moved"). They cannot be equal across two runs for the same reason
# `$._emission` cannot -- each records what ITS OWN predecessor was.
#
# LITERAL, NOT A WILDCARD, AND THE REASON IS THIS PROJECT'S OWN: a `$.notes.step9_b_*` pattern
# would admit every note this arm writes, including ones that restate a FIGURE, and a class
# broad enough to hide a figure is how twelve superseded denominators published unmarked
# (decisions/0123 SS6d). Adding a path here is a deliberate act, one path at a time.
RUN_RECORD_PROSE = {
    "$.notes.step9_b_emission_provenance",
    "$.notes.step9_b_leaf_verification_of_this_emission",
}

# For the probe only: a leaf that is unambiguously a MEASUREMENT of this study. `$.sentinels.*`
# is excluded -- it holds the schema's -999 documentation values, not a figure -- so the probe
# cannot satisfy itself by moving a number that no reader would act on.
PROTECTED_FIGURE = re.compile(r"\.(value_percent|lower|upper|width_pp)$|^\$\.figures\..*\.value$")


def is_run_record_numeric(path):
    """The numeric-stray test uses the PATTERN form ONLY. The prose set is admitted for string
    classification and must never excuse a moved NUMBER: a note is prose, and if one ever
    arrived as a numeric leaf it would be a shape change, not bookkeeping."""
    return any(rx.search(path) for rx in RUN_RECORD)


def is_run_record(path):
    return path in RUN_RECORD_PROSE or is_run_record_numeric(path)


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


def show(rev, rel):
    return subprocess.check_output(["git", "-C", ROOT, "show", "%s:%s" % (rev, rel)])


REP = io.StringIO()


def w(s=""):
    print(s)
    REP.write(s + "\n")


# ---------------------------------------------------------------- the two template revisions
# SET MEMBERSHIP AGAINST THE SOURCE. The SCHEMA_TEXT class is not "prose that looks inherited";
# it is "byte-identical to the v1.10.0 template at this path, and not what v1.9.0's carried".
# Both sides are read from disk/history here so the test can fail.
tpl_new = json.loads(open(os.path.join(ROOT, TEMPLATE), "rb").read())
tpl_old = json.loads(show(BASE_REV + "^", TEMPLATE))
TPL_NEW = dict(leaves(tpl_new))
TPL_OLD = dict(leaves(tpl_old))


def is_schema_text(path, new_value):
    """Inherited verbatim from the v1.10.0 template, and changed by that version."""
    if path not in TPL_NEW:
        return False
    if TPL_NEW[path] != new_value:
        return False
    return TPL_OLD.get(path, "\0<absent>") != new_value


def version_bump(old_value, new_value):
    """The move is EXACTLY the version token: substituting it in the old reproduces the new."""
    if not isinstance(old_value, str) or not isinstance(new_value, str):
        return False
    if OLD_VER not in old_value:
        return False
    return old_value.replace(OLD_VER, NEW_VER) == new_value


def classify(path, old_value, new_value, present_before=True):
    if present_before and version_bump(old_value, new_value):
        return "VERSION_IDENTIFIER"
    if is_run_record(path):
        return "RUN_RECORD"
    if is_schema_text(path, new_value):
        return "SCHEMA_TEXT_v%s" % NEW_VER.replace(".", "_")
    return "NEITHER"


w("=" * 96)
w("STEP 9, ARM b -- VERSION-ONLY MIGRATION VERIFIER   (schema %s -> %s)" % (OLD_VER, NEW_VER))
w("baseline: git %s   |   probe: %s" % (BASE_REV, PROBE))
w("=" * 96)
w("")
w("Compares THIS ARM's finished bytes on disk against THIS ARM's own files at a named commit.")
w("It says nothing about the other arm, which this arm does not see, and nothing about the")
w("stamped originals, which are settled and untouched by this run.")
w("")

hard_stop = []
# EVERY PROBE KIND MUST ACTUALLY HAVE BEEN CONSTRUCTED SOMEWHERE. A per-file "at least one"
# would let three of the four vectors silently go unbuilt -- the working-figures extract carries
# no inherited template text and no `.ci.` block -- and a probe that never built its
# version-token vector has not shown the classifier rejecting a forged version token.
PROBE_KINDS = set()
PROBE_KINDS_REQUIRED = {"numeric", "version-token", "schema-text"}
tot_compared = tot_moved = 0
class_totals = {}

for rel in JSON_FILES:
    cur = json.loads(open(os.path.join(ROOT, rel), "rb").read())
    old = json.loads(show(BASE_REV, rel))
    a, b = dict(leaves(old)), dict(leaves(cur))

    if PROBE:
        b = dict(b)
        applied = []
        # 1 + 2. a protected figure and a CI endpoint, moved.
        figs = [p for p in b if p in a and numeric(b[p]) and PROTECTED_FIGURE.search(p)
                and not is_run_record(p) and not p.startswith("$.sentinels.")]
        ends = [p for p in figs if p.endswith(".lower") or p.endswith(".upper")]
        pts = [p for p in figs if p not in ends]
        for pick in (pts[:1] + ends[:1]):
            b[pick] = b[pick] + 1.0
            applied.append(("numeric", pick))
        # 3. a string carrying the NEW version token, but not produced by the substitution.
        vers = [p for p in b if p in a and isinstance(b[p], str) and NEW_VER in str(b[p])]
        if vers:
            b[vers[0]] = "urn:season2-study:step8b-output-schema:1.10.0-TAMPERED"
            applied.append(("version-token", vers[0]))
        # 4. a schema-inherited leaf, reworded.
        inh = [p for p in b if isinstance(b[p], str) and is_schema_text(p, b[p])]
        if inh:
            b[inh[0]] = b[inh[0]] + " AND ONE WORD THIS ARM ADDED"
            applied.append(("schema-text", inh[0]))
        if not applied:
            sys.exit("HARD STOP: the probe could construct NO vector in %s, so it would have "
                     "reported by looking nowhere." % rel)
        PROBE_KINDS.update(k for k, _ in applied)
        w("    PROBE ACTIVE on %s: %s  (in memory; no file touched)"
          % (rel, ", ".join("%s@%s" % (k, p) for k, p in applied)))

    common = [p for p in a if p in b]
    moved = [p for p in common if a[p] != b[p]]
    lost = sorted(p for p in a if p not in b)
    added = sorted(p for p in b if p not in a)

    num_common = [p for p in common if numeric(a[p]) and numeric(b[p])]
    num_moved = [p for p in num_common if a[p] != b[p]]
    num_stray = [p for p in num_moved if not is_run_record_numeric(p)]

    rows = []
    for p in moved:
        rows.append((p, classify(p, a[p], b[p]), a[p], b[p]))
    for p in added:
        rows.append((p, classify(p, None, b[p], present_before=False), "<absent>", b[p]))
    for p in lost:
        rows.append((p, "RUN_RECORD" if is_run_record(p) else "NEITHER", a[p], "<absent>"))

    tot_compared += len(common)
    tot_moved += len(moved)
    for _, c, _, _ in rows:
        class_totals[c] = class_totals.get(c, 0) + 1

    w("-" * 96)
    w(rel)
    w("-" * 96)
    w("    leaves at %s / on disk / compared : %d / %d / %d"
      % (BASE_REV, len(a), len(b), len(common)))
    w("    ALL leaves moved (any type)           : %d" % len(moved))
    w("    leaves absent here / added here       : %d / %d" % (len(lost), len(added)))
    w("    NUMERIC leaves compared               : %d" % len(num_common))
    w("    NUMERIC leaves moved                  : %d   (of which outside RUN_RECORD: %d)"
      % (len(num_moved), len(num_stray)))
    w("")
    for p, c, va, vb in sorted(rows, key=lambda r: (r[1], r[0])):
        def sh(v):
            s = repr(v)
            return s if len(s) <= 76 else s[:76] + "..."
        w("      [%s] %s" % (c, p))
        w("            was: %s" % sh(va))
        w("            now: %s" % sh(vb))
    if not rows:
        w("      (no leaf moved, was added, or went absent)")
    w("")

    if not common:
        hard_stop.append((rel, "NO LEAF WAS COMPARED AT ALL"))
    if num_stray:
        hard_stop.append((rel, "NUMERIC MOVEMENT OUTSIDE THE RUN RECORD: %r" % num_stray[:10]))
    bad = [p for p, c, _, _ in rows if c == "NEITHER"]
    if bad:
        hard_stop.append((rel, "UNCLASSIFIED LEAF/LEAVES: %r" % bad[:10]))

# ------------------------------------------------------------------------------- the markdown
w("-" * 96)
w(MD_FILE)
w("-" * 96)
cur_md = open(os.path.join(ROOT, MD_FILE), "rb").read().decode()
old_md = show(BASE_REV, MD_FILE).decode()
cur_lines, old_lines = cur_md.splitlines(), old_md.splitlines()
if PROBE:
    cur_lines = list(cur_lines)
    cur_lines[0] = cur_lines[0] + "  (PROBE: a line this arm did not emit)"
    w("    PROBE ACTIVE: line 1 altered in memory; no file touched.")
import difflib
md_rows = []
sm = difflib.SequenceMatcher(None, old_lines, cur_lines, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        continue
    olds, news = old_lines[i1:i2], cur_lines[j1:j2]
    for k in range(max(len(olds), len(news))):
        o = olds[k] if k < len(olds) else "<absent>"
        n = news[k] if k < len(news) else "<absent>"
        if version_bump(o, n):
            c = "VERSION_IDENTIFIER"
        elif re.search(r"\*\*Generated\*\*|generated_at_utc|sha256|\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", n) \
                or re.search(r"\*\*Generated\*\*", o):
            c = "RUN_RECORD"
        elif n != "<absent>" and any(is_schema_text(p, v) and isinstance(v, str) and v in n
                                     for p, v in TPL_NEW.items() if isinstance(v, str)):
            c = "SCHEMA_TEXT_v%s" % NEW_VER.replace(".", "_")
        else:
            c = "NEITHER"
        md_rows.append((c, o, n))
w("    lines at %s / on disk : %d / %d" % (BASE_REV, len(old_lines), len(cur_lines)))
w("    lines changed         : %d" % len(md_rows))
for c, o, n in md_rows:
    w("      [%s]" % c)
    w("            was: %s" % (o[:88] + ("..." if len(o) > 88 else "")))
    w("            now: %s" % (n[:88] + ("..." if len(n) > 88 else "")))
if not old_lines:
    hard_stop.append((MD_FILE, "NO LINE WAS COMPARED AT ALL"))
md_bad = [r for r in md_rows if r[0] == "NEITHER"]
if md_bad:
    hard_stop.append((MD_FILE, "UNCLASSIFIED LINE(S): %d" % len(md_bad)))
for c, _, _ in md_rows:
    class_totals[c] = class_totals.get(c, 0) + 1
w("")

w("=" * 96)
w("    JSON files compared              : %d" % len(JSON_FILES))
w("    JSON leaves compared, in total   : %d" % tot_compared)
w("    JSON leaves moved, in total      : %d" % tot_moved)
w("    every difference, by class:")
for c in sorted(class_totals):
    w("        %-28s : %d" % (c, class_totals[c]))
w("")
if PROBE and PROBE_KINDS_REQUIRED - PROBE_KINDS:
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit("HARD STOP: the probe never constructed %r, so the classifier was not shown "
             "rejecting them. Built: %r" % (sorted(PROBE_KINDS_REQUIRED - PROBE_KINDS),
                                            sorted(PROBE_KINDS)))
if PROBE and not hard_stop:
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit("HARD STOP: THE PROBE DID NOT TRIP THE CLASSIFICATION. A check that passes on a "
             "vector carrying a moved figure, a moved CI endpoint, a forged version token and "
             "a reworded inherited leaf is not a check.")
if hard_stop:
    w("    VERDICT: FAIL%s" % ("   (EXPECTED -- probe mode)" if PROBE else ""))
    for rel, why in hard_stop:
        w("        %s : %s" % (rel, why))
    with open(OUTLOG, "w") as fh:
        fh.write(REP.getvalue())
    sys.exit("HARD STOP: %d finding(s); see above." % len(hard_stop))
w("    VERDICT: PASS. No numeric leaf moved outside the emission's own run record. Every")
w("             difference is a version identifier, a leaf of that run record, or text")
w("             inherited verbatim from the v%s template -- and membership in that last" % NEW_VER)
w("             class was tested AGAINST THE TEMPLATE, not against its shape.")
w("=" * 96)
w("END. Writes no artifact. Adopts nothing. Zero API calls.")
with open(OUTLOG, "w") as fh:
    fh.write(REP.getvalue())
print("\nrun record: logs/step9_b_version_migration_verify.txt")
