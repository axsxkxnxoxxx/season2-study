#!/usr/bin/env python3
"""Step 9, arm b -- STAMP the committed premiere-anchored figures as SUPERSEDED.

WHAT THIS IS
------------
Human Lead ruling, 2026-08-21: *STAMP, DO NOT DELETE.* Arm b's committed
premiere-anchored figures were CORRECTLY PRODUCED UNDER A DEFECTIVE VECTOR, and
the record of what the defect produced is the evidence for the finding. So the
marked originals and the corrected emission must both exist.

THE UNIT ERROR, named once here and named again in every stamp this script
writes: ``src/step9_b_1_compute.py`` converted the premiere-anchored ``T0``
column to epoch seconds with ``prem.astype("int64") // 10 ** 9``. The column's
dtype is ``datetime64[us, UTC]``, so its integer view is MICROseconds. Dividing
by ``10 ** 9`` therefore produced epoch-seconds / 1000 -- a 1970 date -- for
every pair, in every entry, on both populations.

WHAT IT MARKS, AND WHAT IT DELIBERATELY DOES NOT
------------------------------------------------
The mark goes AT THE FIGURE, never in a file-level header. CLAUDE.md: "A
file-level stamp declares a file's STATUS, never its individual values"; a
whole-file exemption once covered 35 files including two operative
deliverables.

``W108_s2_finale`` IS NOT MARKED. It was verified leaf-for-leaf identical and
its harness control reproduces. Marking it would assert a defect that is not
there.

Inside the affected region, a numeric figure is marked when it is AN OUTPUT OF
THIS ARM'S OWN COMPUTATION over the defective vector -- whether or not its value
moved. A figure that is a SPEC INPUT restated, or a Step 8 population size
consumed unchanged, is NOT marked; those did not pass through the vector. The
classification is explicit below and coverage is asserted: an unclassified
numeric leaf is a hard stop, never a default.

THE OWNERSHIP RULE governs that second exclusion and lives at the branch in
classify_numeric(), not here: A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT
WITHOUT RECOMPUTING IT; ANYTHING DOWNSTREAM OF THIS ARM'S OWN LIVENESS FILTER IS
THIS ARM'S, WHATEVER IT WAS DERIVED FROM. Read it there. This paragraph is where
the first pass recorded its reasoning, and a rule recorded away from the branch
is a rule the classifier does not read: `denominator_pairs` was excluded BY NAME
and twelve post-liveness denominators published unmarked as a result.

A string is marked when its text differs from the corrected emission's text at
the same path, or when it has no counterpart there at all. That second case is
how the three vacuous preconditions -- removed, not corrected -- get marked.
Strings are checked because the numeric controls walk numeric leaves only, so a
superseded figure inside a JSON string is invisible to them.

STAMPS ARE NEGATIVE ONLY. A stamp names what is superseded and points at the
corrected block. It restates no adopted figure -- otherwise the positive grep
passes whether or not the body was fixed.

SCHEMA. The headline file is bound by artifacts/step8b-output-schema.json,
whose objects are ``additionalProperties: false`` in 125 places. A new key would
add a structural error at every stamp site and would bury the one real
structural signal in that file. So the headline stamps are prepended to a
SCHEMA-DECLARED string slot on the same object, and the original text is kept
verbatim after a separator. The working-figures file is this arm's own format
and is not schema-bound, so its stamps are a dedicated ``_superseded`` key
inside the figure object itself.

Run:  python3 src/step9_b_6_stamp_superseded.py
Idempotent: a second run makes no change and says so.
"""

import datetime
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMITTED_HEADLINE = os.path.join(ROOT, "artifacts", "step9-headline-b.json")
COMMITTED_MD = os.path.join(ROOT, "artifacts", "step9-headline-b.md")
COMMITTED_WORKING = os.path.join(ROOT, "artifacts", "step9-working-figures-b.json")

CORRECTED_HEADLINE = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.json")
CORRECTED_MD = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.md")
CORRECTED_WORKING = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-working-figures-b.json")

# Where the corrected emission lands. Named here so every stamp can point at it.
EMITTED_HEADLINE = "artifacts/step9-headline-corrected-2026-08-21-b.json"
EMITTED_MD = "artifacts/step9-headline-corrected-2026-08-21-b.md"
EMITTED_WORKING = "artifacts/step9-working-figures-corrected-2026-08-21-b.json"

TOKEN = "[SUPERSEDED 2026-08-21 :: step9-b premiere clock"

# *** THE SECOND SUPERSESSION LAYER. decisions/0124, 2026-08-23. ***
#
# 0124 fixed the RESAMPLING FRAME and the DRAW ORDER, which 0103 and 0118 had left open, and
# this arm's committed run satisfied neither: it drew a per-mask frame (the CONTRIBUTING subset)
# and re-seeded per group. The rerun moves THE CI ENDPOINTS AND NOTHING ELSE -- every point
# estimate, numerator, denominator, bound, width, ceiling, sum and pair count is not
# bootstrap-dependent. So the adopted arm, which 0123 left wholly unmarked on evidence that was
# sound at the time, now carries marks on its intervals and on nothing else.
#
# 0124 SS5b, the ruling this layer discharges: A STAMP IS A CLAIM. A stamp naming what IS
# superseded is a claim about a defect that has already happened and cannot go stale. A stamp
# naming what is NOT superseded is a claim about the ABSENCE of a defect, and it goes stale the
# moment a later ruling creates one in that scope. 0123's table stamps carried exactly such a
# claim about the adopted arm's rows; it is corrected below, not merely supplemented.
#
# CONSEQUENCE FOR EVERY STAMP THIS SCRIPT WRITES FROM NOW ON: a stamp names what IS superseded,
# says the mark covers only the fields it names, and ASSERTS NOTHING ABOUT ANY FIELD IT DOES
# NOT NAME. Declining to make the non-supersession claim is the fix; making a narrower one
# would be the same claim with a smaller scope and the same expiry date.
TOKEN_0124 = "[SUPERSEDED 2026-08-23 :: step9-b resampling frame and draw order"
TOKENS = (TOKEN, TOKEN_0124)
SEP = " || "

# ---------------------------------------------------------------------------
# *** THE MARK SET IS NOT STABLE. Human Lead ruling, 2026-08-24. ***
#
# The ruling generalises a premise of its own that this arm disproved by measurement. The
# premise: the 0124 stamps point at a PATH and not at a VALUE, so moving the corrected emission
# cannot move them. TRUE OF THE JSON STAMPS, whose text is a field list. FALSE OF THE .md CELL
# MARKS, which are written CONDITIONALLY on the cell differing from the corrected emission and
# therefore RE-PARTITION when the corrected values move.
#
#     A CONDITIONAL MARK IS A FUNCTION OF TWO FILES. WHEN EITHER MOVES, THE MARK SET MOVES.
#     ANY MARK WRITTEN BY COMPARISON MUST BE RECOMPUTED WHEN EITHER SIDE CHANGES.
#
# Measured on this build: decisions/0125's re-emission of the corrected figures left two W108
# started-and-left CI WIDTHS newly differing and UNMARKED, and one W108 ratio COINCIDING again
# and still MARKED -- three cells, moving in BOTH directions, from a change to the OTHER file
# alone and none to this one. A stamp asserting something untrue is worse than no stamp
# (decisions/0124 SS5b), and a superfluous mark asserts a defect that is not there.
#
# SO, FOR ANYONE MOVING EITHER SIDE: re-running this script is not housekeeping that follows a
# change to the corrected emission, it is PART of that change. The rule is restated at each of
# the FOUR branches below where a mark is decided by comparison -- a rule recorded away from the
# branch is a rule the code does not read, which is how `denominator_pairs` was excluded by name
# and twelve figures published unmarked.
# ---------------------------------------------------------------------------
CONDITIONAL_MARK_RULE = (
    "A CONDITIONAL MARK IS A FUNCTION OF TWO FILES. WHEN EITHER MOVES, THE MARK SET MOVES. "
    "Any mark written by comparison must be recomputed when either side changes. Human Lead "
    "ruling, 2026-08-24. The .md cell marks in this file are decided by comparing the committed "
    "artifact with the corrected emission, so a change to the CORRECTED emission alone "
    "re-partitions them: decisions/0125's re-emission newly superseded two W108 "
    "started-and-left CI widths and made one W108 ratio mark superfluous, with no edit to the "
    "committed file at all."
)


THE_ERROR = (
    "Produced under a defective T0 vector: src/step9_b_1_compute.py divided a "
    "datetime64[us, UTC] column by 10 ** 9, so every premiere-anchored T0 in this arm was "
    "epoch-SECONDS / 1000 -- a 1970 date -- and not epoch seconds. The named fields are "
    "correctly computed from that vector and are kept as the record of what the defect "
    "produced; they are SUPERSEDED, not withdrawn."
)

# ---------------------------------------------------------------------------
# Classification. Explicit, with the reason, and asserted to be exhaustive.
#
# *** THE OWNERSHIP RULE. Human Lead ruling, 2026-08-23. ***
#
#   A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT WITHOUT RECOMPUTING IT.
#   ANYTHING DOWNSTREAM OF THIS ARM'S OWN LIVENESS FILTER IS THIS ARM'S,
#   WHATEVER IT WAS DERIVED FROM.
#
# This is stated HERE and again at the branch in classify_numeric(), which is
# where the classifier actually reads it. A note in a module docstring far from
# the branch is not where the call gets made, and that is how the first pass
# went wrong.
#
# WHAT THE FIRST PASS GOT WRONG, named so the next pass cannot repeat it. It
# classified by FIELD NAME alone and listed `denominator_pairs`, `population_n`
# and `on_population_n` flatly as "STEP 8's population size, consumed
# unchanged". That reading is TRUE under `bounds`, whose denominator IS the
# position-5 population (decisions/0052: the bounds and the shares are on
# DIFFERENT populations). It is FALSE under `shares`, whose denominator is
# POST-LIVENESS -- produced by THIS ARM'S OWN liveness filter over the
# defective T0 vector. Its INPUT was Step 8's; its OUTPUT is not. And it MOVED:
# 196,494 -> 196,048 on APPLY, 147,318 -> 147,297 on DERIV.
#
#   n_position_5   = 196,654 IS Step 8's -- consumed unchanged.
#   n_post_liveness / shares denominators ARE NOT -- this arm's filter made them.
#
# The two sat side by side under one field name and were classified alike, so
# twelve figures published unmarked. The shared register found them; this
# classifier did not.
#
# So a population size is NO LONGER TRUSTED BY ITS NAME. It counts as Step 8's
# only when it still HOLDS Step 8's figure -- the `n_position_5` declared on the
# enclosing `headline.<POPULATION>` object, which this arm consumed unchanged.
# Any population size that differs from that anchor was recomputed here and is
# THIS ARM'S.
# ---------------------------------------------------------------------------

# Numeric leaves whose LAST path component is one of these are SPEC INPUTS
# restated. They did not pass through the T0 vector under any nesting, so
# marking them would assert a defect that is not there.
SPEC_INPUT_FIELDS = {
    "W_days": "spec input -- the window, decisions/0026 and task-sheet.md Step 9",
    "H_days": "spec input -- the horizon, held constant across arms",
    "adopted_rule_revision": "READ from processed/step5/adopted_rule.json, not computed here",
    "level_pct": "spec input -- the interval level",
    "B": "spec input -- the resample count, decisions/0103",
    "seed": "spec input -- the bootstrap seed, decisions/0103",
    "horizon_days": "a function of W and H alone, both spec inputs",
}

# Population sizes. NAME ALONE DECIDES NOTHING HERE -- see the ownership rule
# above. Each is tested against Step 8's anchor at its own point of use.
POPULATION_SIZE_FIELDS = {
    "n_position_5", "denominator_pairs", "population_n", "on_population_n",
}

# The anchor is read from the enclosing `$.arms[i].headline.<POPULATION>`, never
# hardcoded: a hardcoded 196,654 would be a SECOND definition of Step 8's figure
# inside this arm, which is the defect class this study has hit most often.
POP_ANCHOR_RE = re.compile(r"^(\$\.arms\[\d+\]\.headline\.(?:APPLY|DERIV))\.")


def classify_numeric(root, path, field, value):
    """Return the REASON this numeric leaf is NOT marked, or None to MARK it.

    *** A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT WITHOUT RECOMPUTING
    *** IT. ANYTHING DOWNSTREAM OF THIS ARM'S OWN LIVENESS FILTER IS THIS
    *** ARM'S, WHATEVER IT WAS DERIVED FROM.

    `denominator_pairs` under `bounds` is Step 8's; the same field name under
    `shares` is a POST-LIVENESS denominator this arm computed. The test is
    therefore not the name but whether the leaf still holds Step 8's own figure.
    """
    if field in SPEC_INPUT_FIELDS:
        return SPEC_INPUT_FIELDS[field]
    if field in POPULATION_SIZE_FIELDS:
        m = POP_ANCHOR_RE.match(path)
        if not m:
            sys.exit("HARD STOP: population-size field %r at %s has no enclosing "
                     "headline.<POPULATION> object to read Step 8's n_position_5 from, so "
                     "its ownership cannot be established. NO MATCH IS A HARD STOP, NEVER "
                     "A DEFAULT." % (field, path))
        anchor = resolve(root, m.group(1) + ".n_position_5")
        if value == anchor:
            return ("STEP 8's position-5 population size, consumed unchanged -- equal to "
                    "n_position_5 = %s on the enclosing population" % anchor)
        # Downstream of this arm's own liveness filter. MARK IT.
        return None
    return None

# The same idea for the working-figures file, which nests every figure as
# {value, source_file, key}, so the FIGURE NAME is the parent key.
#
# THE SAME OWNERSHIP RULE APPLIES HERE and is enforced the same way: the two
# population-size figures below are trusted only while they still HOLD Step 8's
# n_position_5 for their own population. This file happens to give the
# post-liveness denominator its own name -- `n_post_liveness` -- which is why
# the defect did not reach it; the guard is here so that naming is not what
# protects it.
WF_NOT_THIS_ARMS_OUTPUT = {
    "W_days": "spec input -- the window",
    "n_position_5": "STEP 8's population size, consumed unchanged",
    "start": "conjunct_ladder.start is the position-5 population size, STEP 8's",
}
WF_POPULATION_SIZE_FIGURES = {"n_position_5", "start"}
WF_POP_ANCHOR_RE = re.compile(r"^(\$\.figures\.[A-Za-z0-9_]+\.(?:APPLY|DERIV))\.")
WF_NOT_OUTPUT_PREFIXES = (
    "$.supplementary.account_totals_of_the_populations",
)

# Where a stamp may be written on a schema-bound object, in preference order.
# Every one of these is a property the schema declares, so no stamp adds a
# structural error to the file it marks.
SLOTS = ("note", "populations_differ_note", "conditioning_text", "evidence",
         "denominator_definition")


def sha12(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def leaves(obj, prefix):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, prefix + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, "%s[%d]" % (prefix, i))
    else:
        yield prefix, obj


def is_number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def resolve(root, path):
    """Walk a '$.a.b[3].c' path from root."""
    cur = root
    tok = ""
    i = 1  # skip the leading '$'
    while i < len(path):
        ch = path[i]
        if ch == ".":
            if tok:
                cur = cur[tok]
                tok = ""
            i += 1
        elif ch == "[":
            if tok:
                cur = cur[tok]
                tok = ""
            j = path.index("]", i)
            cur = cur[int(path[i + 1:j])]
            i = j + 1
        else:
            tok += ch
            i += 1
    if tok:
        cur = cur[tok]
    return cur


def strip_stamps(text):
    """Remove every stamp a previous run of THIS script prepended to a slot.

    Stamping must be REGENERATIVE, not additive. The old code skipped any slot
    that already held a token, so a site whose FIELD LIST had grown was never
    revisited -- which is precisely how the twelve stayed unmarked through a
    rerun. Rebuilding the slot from the classification on every run makes the
    written text a pure function of the classification, and idempotent.
    """
    while text.startswith(TOKENS):
        _head, sep, tail = text.partition(SEP)
        if not sep:
            sys.exit("HARD STOP: a stamp with no closing separator was found; refusing to "
                     "guess where it ends. Text begins: %r" % text[:120])
        text = tail
    return text


def field_name_for_stamp(name):
    """Render a field name so the SHARED checker can parse the stamp it sits in.

    `src/check_surfaces.py::STAMP_FIELDS` reads a stamp's field list with
    `fields:\\s*([A-Za-z0-9_,\\s\\.]+?)\\]` -- a grammar with NO array-index
    form. A single `[0]` in one name does not merely drop that name: the regex
    then finds no closing `]` before the bracket, THE WHOLE MATCH FAILS, and
    every OTHER field the stamp names loses its exemption too. That is a silent
    widening of the control's output, and it is measurable here -- one hoisted
    list-element name unexempted `n_post_liveness` on both populations.

    So a list index is rendered `x.0` rather than `x[0]`. The pointer is
    unchanged in meaning and the stamp stays machine-readable. REPORTED to the
    Human Lead as a limitation of the shared checker; not worked around inside
    it, because that file is not this arm's to edit.
    """
    return name.replace("[", ".").replace("]", "")


def stamp_text(fields, corrected_path, sep=SEP):
    return ("%s :: fields: %s] %s The corrected value of each named field is at the SAME "
            "JSON path in %s. THIS MARK COVERS ONLY THE FIELDS IT NAMES; it exempts nothing "
            "else in this file.%s"
            % (TOKEN, ", ".join(fields), THE_ERROR, corrected_path, sep))


REMOVED_TEXT = (
    "%s :: REMOVED, NOT CORRECTED :: fields: %s] This field has NO counterpart in the "
    "corrected emission. It belongs to the three premiere-arm preconditions, which the "
    "reproduction harness re-ran against the vector on disk and recorded as returning True on "
    "all three (logs/step9_b_premiere_clock_repro.txt): the defective T0 sits in 1970, so it "
    "is earlier than every finale origin and observable before every horizon, and the checks "
    "could not fail whatever the vector held. They were VACUOUS and were removed rather than "
    "corrected. The replacement is the elementwise clock-vector verification at "
    "$.t0_movement.companions_stored_with_it.clock_vector_verification in %s. THIS MARK "
    "COVERS ONLY THE FIELDS IT NAMES.")


# A REMOVAL MUST NAME ITS OWN CAUSE, AND AN UNKNOWN CAUSE IS A HARD STOP.
#
# REMOVED_TEXT tells one specific story -- the three vacuous premiere-arm preconditions -- and
# the first version of this function applied it to EVERY field that had lost its counterpart.
# That was safe only while the preconditions were the only removal. 0124's rerun restructured
# the account-total block, and a rerun of the committed script would have stamped four fields
# with a cause that is not theirs. A stamp asserting the wrong ground is the same class of
# defect as a stamp asserting a defect that is not there.
#
# So the cause is keyed on the path, and a removed field whose path matches no entry HARD
# STOPS. Guessing is what this table exists to prevent.
REMOVAL_CAUSES = (
    ("$.t0_movement.companion_booleans_stored_with_it.", "preconditions"),
    ("$.supplementary.account_totals_of_the_populations.", "frame_0124"),
)

ACCOUNT_TOTALS_PREFIX = "$.supplementary.account_totals_of_the_populations."

RESTRUCTURED_TEXT_0124 = (
    "%s :: RESTRUCTURED, NOT CORRECTED :: fields: %s] This field has NO counterpart in the "
    "corrected emission. decisions/0124 fixed the resampling frame as every account with at "
    "least one pair in the position-4 output, drawn for every quantity, and fixed the draw "
    "order as one continuously-consumed stream; the account-total block was rebuilt to record "
    "THE DRAW and THE SUPPORT as two separate figures, so this pointer addresses a key the "
    "bootstrap stage no longer writes. The corrected block is at the same section of %s. THIS "
    "MARK COVERS ONLY THE FIELDS IT NAMES AND ASSERTS NOTHING ABOUT ANY FIELD IT DOES NOT NAME.")


def removed_text(fields, corrected_path, container):
    cause = next((c for pre, c in REMOVAL_CAUSES if container.startswith(pre)), None)
    if cause is None:
        sys.exit("HARD STOP: %s lost its counterpart in the corrected emission and no entry in "
                 "REMOVAL_CAUSES claims that path, so this script cannot say WHY it was removed. "
                 "A removal stamped with a borrowed cause is a stamp asserting the wrong ground. "
                 "Add the cause or do not mark it." % container)
    if cause == "preconditions":
        return REMOVED_TEXT % (TOKEN, ", ".join(fields), corrected_path)
    return RESTRUCTURED_TEXT_0124 % (TOKEN_0124, ", ".join(fields), corrected_path)


THE_FRAME_RULING = (
    "Produced under a resampling design that decisions/0124 has since fixed against: this arm "
    "drew its bootstrap frame PER MASK -- the accounts contributing to each group -- and "
    "RE-SEEDED the generator per group. 0124 fixes the frame as every account with at least "
    "one pair in the position-4 output, built once and drawn for every quantity regardless of "
    "how much it contributes, and fixes the draw order as one RNG seeded once per file whose "
    "stream is consumed continuously, every quantity evaluated against the same replicate set. "
    "The named fields are correctly computed under the superseded design and are kept as the "
    "record of what it produced; they are SUPERSEDED, not withdrawn."
)


def stamp_text_0124(fields, corrected_path, sep=SEP):
    """A 0124 mark. Negative only, and it makes NO claim about what it does not name.

    The closing clause is the point of the whole layer. 0123's stamps ended by telling the
    reader which rows were NOT superseded, which was true when written and false eight
    entries later. This one declines to say it.
    """
    return ("%s :: fields: %s] %s The corrected value of each named field is at the SAME JSON "
            "path in %s. THIS MARK COVERS ONLY THE FIELDS IT NAMES; it exempts nothing else in "
            "this file AND IT ASSERTS NOTHING ABOUT ANY FIELD IT DOES NOT NAME -- a stamp "
            "naming what is not superseded goes stale the moment a later ruling creates a "
            "defect in that scope (decisions/0124 SS5b).%s"
            % (TOKEN_0124, ", ".join(fields), THE_FRAME_RULING, corrected_path, sep))


# ---------------------------------------------------------------------------
# 1. The headline JSON
# ---------------------------------------------------------------------------

def stamp_headline(report):
    old = json.load(open(COMMITTED_HEADLINE))
    new = json.load(open(CORRECTED_HEADLINE))

    # The affected region: the premiere arm entry, and the six declared
    # intervals that carry its movements. Found by arm_id and interval_id
    # rather than by index, so a reordering cannot silently move the region.
    regions = []
    prem_idx = [i for i, a in enumerate(old["arms"]) if a["clock_origin"] == "s2_premiere"]
    if len(prem_idx) != 1:
        sys.exit("HARD STOP: expected exactly one premiere-anchored arm, found %d" % len(prem_idx))
    regions.append("$.arms[%d]" % prem_idx[0])
    iv_idx = [i for i, v in enumerate(old["declared_intervals"])
              if "s2_premiere" in v["interval_id"]]
    if not iv_idx:
        sys.exit("HARD STOP: no premiere-anchored declared interval found")
    regions += ["$.declared_intervals[%d]" % i for i in iv_idx]

    finale_arm = [i for i, a in enumerate(old["arms"]) if a["clock_origin"] == "s2_finale"]
    report["headline_region_paths"] = regions
    # CORRECTED 2026-08-23 (decisions/0124 SS5b). This field used to say the adopted arm was
    # not superseded. The claim was sound when written -- 664 leaves verified unmoved -- and
    # 0124 then moved 24 of its CI endpoints. A record of what a layer did NOT mark is a claim
    # about the absence of a defect and expires; it now states only this layer's SCOPE.
    report["headline_not_marked"] = [
        "$.arms[%d] (W108_s2_finale) -- OUT OF SCOPE FOR THE 0123 LAYER, which marks the "
        "premiere-clock defect only. Its supersession status is not asserted here: see "
        "report['headline_0124'], which marks this arm's CI endpoints on decisions/0124's "
        "ground." % i for i in finale_arm]

    marked_fields = {}      # container path -> [field names]
    classified, unclassified = 0, []
    n_numeric_marked = n_string_marked = 0
    not_marked_reasons = {}     # path -> why this arm did not mark it

    for rp in regions:
        o_sub, n_sub = resolve(old, rp), resolve(new, rp)
        old_leaves = dict(leaves(o_sub, rp))
        new_leaves = dict(leaves(n_sub, rp))
        for path, val in old_leaves.items():
            container, _, field = path.rpartition(".")
            if is_number(val):
                classified += 1
                # *** THE BRANCH. A FIGURE IS STEP 8's ONLY IF THIS ARM
                # *** CONSUMED IT WITHOUT RECOMPUTING IT. ANYTHING DOWNSTREAM
                # *** OF THIS ARM'S OWN LIVENESS FILTER IS THIS ARM'S, WHATEVER
                # *** IT WAS DERIVED FROM.
                # A field NAME is not an answer to that question: this file
                # carries `denominator_pairs` in both classes, side by side.
                reason = classify_numeric(old, path, field, val)
                if reason is not None:
                    not_marked_reasons[path] = reason
                    continue
                marked_fields.setdefault(container, []).append(field)
                n_numeric_marked += 1
            elif isinstance(val, (str, bool)) or val is None:
                # Text, flags and explicit nulls. A superseded FIGURE can sit
                # inside a string, where the numeric controls cannot see it, so
                # a string whose text moved is marked exactly like a number.
                #
                # A stamp a previous run wrote into a slot is NOT a movement of
                # the figure; it is this script's own output. Comparing the
                # stamped text would mark every slot it has ever written and
                # grow the marks on every rerun.
                # *** A CONDITIONAL MARK IS A FUNCTION OF TWO FILES: WHEN EITHER MOVES, THE
                # *** MARK SET MOVES. The mark below is decided HERE, by comparison with the
                # *** corrected emission -- so it must be RECOMPUTED whenever EITHER side
                # *** changes, not only this one. See CONDITIONAL_MARK_RULE above.
                base = strip_stamps(val) if isinstance(val, str) else val
                gone = path not in new_leaves
                moved = (not gone) and new_leaves[path] != base
                if gone or moved:
                    marked_fields.setdefault(container, []).append(field)
                    n_string_marked += 1
            else:
                unclassified.append(path)

    if unclassified:
        sys.exit("HARD STOP: %d leaves in the affected region were classified neither as a "
                 "figure nor as text: %s" % (len(unclassified), unclassified[:5]))

    # Every marked field must be reachable from a stamp. A container without a
    # schema-declared string slot hoists to the nearest ancestor that has one,
    # and the stamp then names the field by its RELATIVE path so the reader is
    # sent to the right leaf.
    sites, hoisted, already = {}, 0, 0
    for container in sorted(marked_fields):
        target, rel = container, ""
        hops = 0
        while True:
            tobj = resolve(old, target)
            slot = next((s for s in SLOTS if isinstance(tobj, dict) and s in tobj), None)
            if slot:
                break
            parent, _, last = target.rpartition(".")
            if not parent or not last:
                sys.exit("HARD STOP: no schema-declared string slot above %s" % container)
            rel = (last + "." + rel) if rel else last
            target = parent
            hops += 1
        if hops:
            hoisted += 1
        names = [field_name_for_stamp((rel + "." + f) if rel else f)
                 for f in sorted(set(marked_fields[container]))]
        sites.setdefault((target, slot), []).extend(names)

    # Every slot's final text, built from the classification alone.
    prefix_of = {}
    for (target, slot), names in sorted(sites.items()):
        prefix_of[(target, slot)] = stamp_text(sorted(set(names)), EMITTED_HEADLINE)

    # One ORIENTATION mark on the arm entry itself. It is not a figure mark and
    # it exempts nothing: it says so, and every superseded figure below it
    # carries its own.
    arm_slot = (regions[0], "note")
    orientation_token = TOKEN + " :: ORIENTATION, NOT AN EXEMPTION]"
    orientation = (
        "%s Every figure this arm measured is superseded and EACH ONE CARRIES ITS OWN MARK at "
        "its own point of use; this note exempts nothing and stands in for no individual "
        "value. %s The corrected emission is %s.%s"
        % (orientation_token, THE_ERROR, EMITTED_HEADLINE, SEP))
    prefix_of[arm_slot] = orientation + prefix_of.get(arm_slot, "")

    changed = rewritten = 0
    rewrites = []
    for (target, slot), prefix in sorted(prefix_of.items()):
        tobj = resolve(old, target)
        cur = tobj[slot]
        want = prefix + strip_stamps(cur)
        if cur == want:
            already += 1
            continue
        if TOKEN in cur:
            # The site was stamped, but for a DIFFERENT field list than the
            # classification now yields. Rewritten, not left alone.
            rewritten += 1
            rewrites.append(target + "." + slot)
        else:
            changed += 1
        tobj[slot] = want

    with open(COMMITTED_HEADLINE, "w") as fh:
        json.dump(old, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    report["headline"] = {
        "file": "artifacts/step9-headline-b.json",
        "numeric_leaves_examined_in_region": classified,
        "numeric_figures_marked": n_numeric_marked,
        "numeric_leaves_not_marked": classified - n_numeric_marked,
        "ownership_rule": (
            "A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT WITHOUT RECOMPUTING IT. "
            "ANYTHING DOWNSTREAM OF THIS ARM'S OWN LIVENESS FILTER IS THIS ARM'S, WHATEVER "
            "IT WAS DERIVED FROM. Human Lead ruling, 2026-08-23. Recorded at the branch in "
            "classify_numeric(), not only in the module docstring."),
        "why_some_are_not_marked": dict(SPEC_INPUT_FIELDS, **{
            "<population sizes>": (
                "n_position_5 / denominator_pairs / population_n / on_population_n are NOT "
                "classified by name. Each is compared with the n_position_5 declared on its "
                "own enclosing headline.<POPULATION>; equal means consumed unchanged from "
                "Step 8, different means recomputed downstream of this arm's liveness "
                "filter and MARKED. No enclosing population is a HARD STOP.")}),
        "not_marked_reason_by_path": not_marked_reasons,
        "string_fields_marked": n_string_marked,
        "figures_and_fields_marked_total": n_numeric_marked + n_string_marked,
        "stamp_sites_written": changed,
        "stamp_sites_rewritten_for_a_changed_field_list": rewritten,
        "stamp_sites_rewritten_paths": sorted(rewrites),
        "stamp_sites_already_present": already,
        "hoists_to_an_ancestor_slot": hoisted,
        "containers_holding_a_marked_field": len(marked_fields),
    }
    return changed + rewritten


# ---------------------------------------------------------------------------
# 1b. The headline JSON -- the 0124 layer, on the ADOPTED arm
#
# WHAT MOVED, AND HOW THIS SCRIPT DECIDES. Not by field name. A leaf is marked IFF ITS VALUE
# DIFFERS from the corrected emission's value at the same path. That is a MEASUREMENT, and it
# is the rule 0123 SS6d arrived at the hard way: a field NAME cannot answer whether a figure
# moved, and `denominator_pairs` carries two readings four levels apart in this very file.
#
# The measurement is then GUARDED IN BOTH DIRECTIONS, because a criterion that cannot fail is
# not a criterion (0123 SS3):
#
#   * every leaf that MOVED must be a CI endpoint or a CI-derived ratio. If anything else has
#     moved, the ruling's boundary is wrong and this script HARD STOPS rather than marking it.
#   * every PROTECTED family -- the point estimates, numerators, denominators, population
#     sizes, bound widths, three-ceiling arithmetic, pair counts, waterfall counts, air-period
#     counts and spec inputs -- is asserted to have moved ZERO, family by family, WITH ITS
#     COVERAGE COUNT PRINTED. An empty result and a clean result are the same value, and only
#     the control knows which it produced.
#   * every numeric family name in the region must be claimed by one side or the other. An
#     unclaimed name HARD STOPS; it is never defaulted into "protected".
# ---------------------------------------------------------------------------

# The ten protected families. These are the figures the ruling keeps unmarked, and the reason
# is not that they are uninteresting -- it is that they DID NOT MOVE. Marking them would
# assert a defect they do not have.
PROTECTED_FAMILIES = {
    "point_estimates": {"value_percent", "never_started_percent", "started_and_left_percent",
                        "continued_percent", "percent", "retained_share_percent"},
    "numerators": {"numerator_pairs"},
    "bound_denominators": {"denominator_pairs", "on_population_n", "population_n"},
    "population_sizes": {"n_position_5", "n_post_liveness"},
    "bound_widths": {"width_pp"},
    "three_ceiling_arithmetic": {"sum_percent", "excess_pp", "excess_pairs"},
    "exclusion_pair_counts": {"total_pairs", "never_started_component",
                              "started_and_left_component", "silence_test_alone",
                              "spared_by_not_continued", "channel_pairs_conceded_by_the_floor"},
    "waterfall_counts": {"n_in", "n_out", "removed", "position", "positions_checked"},
    "air_period_counts": {"entering_pairs", "retained_pairs", "accounts"},
    "spec_inputs": {"W_days", "H_days", "B", "seed", "level_pct", "adopted_rule_revision",
                    "horizon_days", "constrains_never_started_exclusions",
                    "says_nothing_about_channel_pairs"},
}

CI_ENDPOINT_SUFFIXES = (".ci.lower", ".ci.upper")
RATIO_PATH = re.compile(r"\.bound_over_sampling_width_ratios\.[A-Za-z0-9_]+\.value$")

# The three string fields that carry a CI figure or a CI description. A string is where a
# superseded figure hides from the numeric controls, which walk numeric leaves only.
CI_STRING_FIELDS = {"note", "denominator_definition", "quantity"}


def is_ci_endpoint(path):
    return path.endswith(CI_ENDPOINT_SUFFIXES)


def is_ci_derived_ratio(path):
    return bool(RATIO_PATH.search(path))


def stamp_headline_0124(report):
    old = json.load(open(COMMITTED_HEADLINE))
    new = json.load(open(CORRECTED_HEADLINE))
    emitted = json.load(open(os.path.join(ROOT, EMITTED_HEADLINE)))

    fin = [i for i, a in enumerate(old["arms"]) if a["clock_origin"] == "s2_finale"]
    if len(fin) != 1:
        sys.exit("HARD STOP: expected exactly one finale-anchored arm, found %d" % len(fin))
    iv = [i for i, v in enumerate(old["declared_intervals"]) if "s2_finale" in v["interval_id"]]
    if not iv:
        sys.exit("HARD STOP: no finale-anchored declared interval found")
    regions = ["$.arms[%d]" % fin[0]] + ["$.declared_intervals[%d]" % i for i in iv]

    marked_fields = {}
    moved_numeric, moved_string = [], []
    family_cov = {k: 0 for k in PROTECTED_FAMILIES}
    family_moved = {k: [] for k in PROTECTED_FAMILIES}
    unclaimed, preview_vs_emitted = [], []
    n_numeric = 0

    for rp in regions:
        o_sub, n_sub, e_sub = resolve(old, rp), resolve(new, rp), resolve(emitted, rp)
        old_leaves = dict(leaves(o_sub, rp))
        new_leaves = dict(leaves(n_sub, rp))
        emitted_leaves = dict(leaves(e_sub, rp))
        # The stamp points at the EMITTED artifact while the comparison is against the
        # PREVIEW. If those two ever disagree in this region the pointer lies, and that is
        # 0123 SS6e's shape -- the committed artifact not being the committed generator's
        # output -- one file further along. Checked, not assumed.
        for path, val in new_leaves.items():
            if emitted_leaves.get(path, "\x00MISSING") != val:
                preview_vs_emitted.append(path)

        for path, val in old_leaves.items():
            container, _, field = path.rpartition(".")
            if is_number(val):
                n_numeric += 1
                fam = next((k for k, names in PROTECTED_FAMILIES.items() if field in names), None)
                ci = is_ci_endpoint(path) or is_ci_derived_ratio(path)
                if fam is None and not ci:
                    unclaimed.append(path)
                    continue
                # *** A CONDITIONAL MARK IS A FUNCTION OF TWO FILES: WHEN EITHER MOVES, THE
                # *** MARK SET MOVES. The mark below is decided HERE, by comparison with the
                # *** corrected emission -- so it must be RECOMPUTED whenever EITHER side
                # *** changes, not only this one. See CONDITIONAL_MARK_RULE above.
                moved = path not in new_leaves or new_leaves[path] != val
                if fam is not None:
                    family_cov[fam] += 1
                    if moved:
                        family_moved[fam].append((path, val, new_leaves.get(path)))
                    continue
                if not moved:
                    continue
                moved_numeric.append((path, val, new_leaves[path]))
                marked_fields.setdefault(container, []).append(field)
            elif isinstance(val, (str, bool)) or val is None:
                base = strip_stamps(val) if isinstance(val, str) else val
                if path not in new_leaves or new_leaves[path] == base:
                    continue
                if field not in CI_STRING_FIELDS:
                    sys.exit("HARD STOP: the string at %s moved between this file and the "
                             "corrected emission, and it is not one of the CI-bearing string "
                             "fields %s. 0124 moves the CI endpoints and nothing else, so a "
                             "moved string outside that set means the ruling's boundary does "
                             "not describe this file. Refusing to mark it."
                             % (path, sorted(CI_STRING_FIELDS)))
                moved_string.append(path)
                marked_fields.setdefault(container, []).append(field)

    if preview_vs_emitted:
        sys.exit("HARD STOP: %d leaves in the adopted-arm region differ between the preview at "
                 "%s and the emitted artifact at %s. Every 0124 stamp points at the emitted "
                 "artifact, so a disagreement makes the pointer false: %s"
                 % (len(preview_vs_emitted), CORRECTED_HEADLINE, EMITTED_HEADLINE,
                    preview_vs_emitted[:5]))
    if unclaimed:
        sys.exit("HARD STOP: %d numeric leaves in the adopted-arm region belong to no protected "
                 "family and are not CI endpoints, so this script cannot say whether they were "
                 "expected to move. AN UNCLAIMED NAME IS A HARD STOP, NEVER A DEFAULT: %s"
                 % (len(unclaimed), unclaimed[:6]))
    broken = {k: v for k, v in family_moved.items() if v}
    if broken:
        sys.exit("HARD STOP: the ruling holds that 0124 moves the CI endpoints and NOTHING "
                 "ELSE. These protected figures moved, which falsifies that: %s"
                 % {k: v[:3] for k, v in broken.items()})
    empty = [k for k, n in family_cov.items() if n == 0]
    if empty:
        sys.exit("HARD STOP: %s were asserted to have moved zero while ZERO leaves of each were "
                 "examined. An empty result and a clean result are the same value; this one is "
                 "empty." % empty)

    # Stamp sites, by the same hoisting rule the 0123 layer uses.
    sites = {}
    for container in sorted(marked_fields):
        target, rel, hops = container, "", 0
        while True:
            tobj = resolve(old, target)
            slot = next((s for s in SLOTS if isinstance(tobj, dict) and s in tobj), None)
            if slot:
                break
            parent, _, last = target.rpartition(".")
            if not parent or not last:
                sys.exit("HARD STOP: no schema-declared string slot above %s" % container)
            rel = (last + "." + rel) if rel else last
            target, hops = parent, hops + 1
        names = [field_name_for_stamp((rel + "." + f) if rel else f)
                 for f in sorted(set(marked_fields[container]))]
        sites.setdefault((target, slot), []).extend(names)

    prefix_of = {(t, s): stamp_text_0124(sorted(set(n)), EMITTED_HEADLINE)
                 for (t, s), n in sorted(sites.items())}

    # One orientation mark on the arm entry. It names NOTHING as unaffected -- that is the
    # claim 0124 SS5b just had to correct -- and it exempts nothing.
    arm_slot = (regions[0], "note")
    orientation = (
        "%s :: ORIENTATION, NOT AN EXEMPTION] Figures in this arm are superseded by "
        "decisions/0124 and EACH ONE CARRIES ITS OWN MARK at its own point of use. %s This "
        "note exempts nothing, stands in for no individual value, AND ASSERTS NOTHING ABOUT "
        "ANY FIELD IT DOES NOT NAME. The corrected emission is %s.%s"
        % (TOKEN_0124, THE_FRAME_RULING, EMITTED_HEADLINE, SEP))
    prefix_of[arm_slot] = orientation + prefix_of.get(arm_slot, "")

    changed = rewritten = already = 0
    for (target, slot), prefix in sorted(prefix_of.items()):
        tobj = resolve(old, target)
        cur = tobj[slot]
        want = prefix + strip_stamps(cur)
        if cur == want:
            already += 1
            continue
        rewritten += 1 if TOKEN_0124 in cur else 0
        changed += 0 if TOKEN_0124 in cur else 1
        tobj[slot] = want

    with open(COMMITTED_HEADLINE, "w") as fh:
        json.dump(old, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    report["headline_0124"] = {
        "file": "artifacts/step9-headline-b.json",
        "ruling": "decisions/0124 -- the resampling frame and the draw order are fixed",
        "region_paths": regions,
        "numeric_leaves_examined_in_region": n_numeric,
        "ci_endpoints_marked": sum(1 for p, _, _ in moved_numeric if is_ci_endpoint(p)),
        "ci_derived_ratio_values_marked": sum(1 for p, _, _ in moved_numeric
                                              if is_ci_derived_ratio(p)),
        "ci_bearing_strings_marked": len(moved_string),
        "protected_families_coverage": family_cov,
        "protected_families_moved": {k: len(v) for k, v in family_moved.items()},
        "preview_vs_emitted_disagreements": len(preview_vs_emitted),
        "stamp_sites_written": changed,
        "stamp_sites_rewritten": rewritten,
        "stamp_sites_already_present": already,
        "why_the_ratios_are_marked": (
            "their DENOMINATOR is a CI sampling width, so they move when the interval moves, "
            "and CLAUDE.md's derived-figures list names 'the bound / account-clustered "
            "sampling width ratio, per arm' as a figure that moves when its endpoint does. "
            "Measured: five of the six moved. The sixth is the DERIV never-started ratio, "
            "whose numerator is a degenerate zero-width bound, so it is 0.0000 under either "
            "design and is NOT marked -- it did not move."),
        "why_no_claim_about_the_unmarked": (
            "0124 SS5b: a stamp naming what is NOT superseded is a claim about the absence of "
            "a defect and goes stale the moment a later ruling creates one. Every mark this "
            "layer writes names only what IS superseded and says so explicitly."),
    }
    return changed + rewritten


# ---------------------------------------------------------------------------
# 2. The working-figures JSON -- this arm's own format, not schema-bound
# ---------------------------------------------------------------------------

def stamp_working(report):
    old = json.load(open(COMMITTED_WORKING))
    new = json.load(open(CORRECTED_WORKING))
    old_leaves = dict(leaves(old, "$"))
    new_leaves = dict(leaves(new, "$"))

    def in_region(path):
        # The account-total block is in region for BOTH arms. 0124 rebuilt it into a DRAW
        # figure and a SUPPORT figure, so its pointers address keys the bootstrap stage no
        # longer writes -- on the adopted arm as much as on the premiere one. Reaching only
        # the premiere half would have marked two of the four identical pointers and left the
        # adopted arm's reader following a dead key. The COUNTS in that block are excluded by
        # WF_NOT_OUTPUT_PREFIXES and stay unmarked: they did not move.
        return ("W91_s2_premiere" in path) or path.startswith("$.t0_movement") \
            or path.startswith(ACCOUNT_TOTALS_PREFIX)

    marked = {}
    n_num = n_str = n_gone = 0
    examined = 0
    wf_reclassified = []   # population sizes the ownership rule pulled back in
    for path, val in old_leaves.items():
        # A stamp this script wrote on an earlier run is not a figure. Without
        # this the second run marks its own marks -- they have no counterpart
        # in the corrected emission, so they read as structurally removed.
        if "_superseded" in path:
            continue
        region = in_region(path)
        # *** A CONDITIONAL MARK IS A FUNCTION OF TWO FILES: WHEN EITHER MOVES, THE
        # *** MARK SET MOVES. The mark below is decided HERE, by comparison with the
        # *** corrected emission -- so it must be RECOMPUTED whenever EITHER side
        # *** changes, not only this one. See CONDITIONAL_MARK_RULE above.
        gone = path not in new_leaves
        moved = (not gone) and new_leaves[path] != val
        if not region:
            # Outside the premiere region only a leaf whose TEXT carries a
            # superseded premiere figure is marked. Pure provenance -- the
            # emission timestamp and the source hashes -- is not a study figure
            # and is correct for the file it describes.
            if not (isinstance(val, str) and moved):
                continue
            if path == "$.generated_at_utc" or path.endswith(".sha256_12"):
                continue
        examined += 1
        container, _, field = path.rpartition(".")
        if is_number(val):
            if field == "value":
                figure_name = container.rpartition(".")[2]
            else:
                figure_name = field
            if figure_name in WF_NOT_THIS_ARMS_OUTPUT:
                # *** A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT WITHOUT
                # *** RECOMPUTING IT. Verified, not assumed: a population size
                # *** that no longer equals its population's n_position_5 was
                # *** rebuilt downstream of this arm's liveness filter, and it
                # *** is MARKED however it is named.
                if figure_name in WF_POPULATION_SIZE_FIGURES:
                    m = WF_POP_ANCHOR_RE.match(path)
                    if not m:
                        sys.exit("HARD STOP: working-figures population size %r at %s has no "
                                 "enclosing figures.<arm>.<POPULATION> to read Step 8's "
                                 "n_position_5 from. NO MATCH IS A HARD STOP, NEVER A "
                                 "DEFAULT." % (figure_name, path))
                    anchor = resolve(old, m.group(1) + ".n_position_5.value")
                    if val != anchor:
                        wf_reclassified.append("%s (%s != n_position_5 %s)" % (path, val, anchor))
                        marked.setdefault(container, {})[field] = "superseded"
                        n_num += 1
                        continue
                continue
            if any(container.startswith(p) for p in WF_NOT_OUTPUT_PREFIXES):
                continue
            marked.setdefault(container, {})[field] = "superseded"
            n_num += 1
        elif isinstance(val, (bool, str)) or val is None:
            if gone:
                # No counterpart in the corrected emission. It was REMOVED, not
                # corrected, so a stamp pointing at "the same JSON path" would
                # point at nothing.
                marked.setdefault(container, {})[field] = "removed"
                n_gone += 1
            elif moved:
                marked.setdefault(container, {})[field] = "superseded"
                n_str += 1

    changed = already = 0
    for container in sorted(marked):
        obj = resolve(old, container)
        if not isinstance(obj, dict):
            sys.exit("HARD STOP: marked field in a non-object container %s" % container)
        block = obj.setdefault("_superseded", {})
        for field, kind in sorted(marked[container].items()):
            if field in block:
                already += 1
                continue
            if kind == "removed":
                block[field] = removed_text([field], EMITTED_WORKING, container)
            else:
                block[field] = stamp_text([field], EMITTED_WORKING, sep="")
            changed += 1

    with open(COMMITTED_WORKING, "w") as fh:
        json.dump(old, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    report["working_figures"] = {
        "file": "artifacts/step9-working-figures-b.json",
        "leaves_examined": examined,
        "numeric_figures_marked": n_num,
        "string_fields_marked": n_str,
        "structurally_removed_fields_marked": n_gone,
        "figures_and_fields_marked_total": n_num + n_str + n_gone,
        "marks_written": changed,
        "marks_already_present": already,
        "why_some_are_not_marked": dict(WF_NOT_THIS_ARMS_OUTPUT,
                                        **{"account_totals_of_the_populations":
                                           "STEP 8's account totals of the position-5 "
                                           "populations; clock-independent"}),
        "ownership_rule_reclassified_population_sizes": wf_reclassified,
        "ownership_rule_note": (
            "A FIGURE IS STEP 8's ONLY IF THIS ARM CONSUMED IT WITHOUT RECOMPUTING IT. The "
            "two population-size figures above are checked against their own population's "
            "n_position_5 rather than trusted by name; an empty list means both still hold "
            "Step 8's figure, not that the check was skipped."),
        "the_three_removed_booleans": (
            "t0_is_earlier_or_equal_for_every_pair and the two tau2_observable_* booleans have "
            "NO counterpart in the corrected emission: they were removed, not corrected, "
            "because each returned True on the defective vector and was vacuous. They are "
            "marked on that ground and the replacement is named in the stamp."),
    }
    return changed


# ---------------------------------------------------------------------------
# 3. The headline .md
# ---------------------------------------------------------------------------

MD_TOKEN = "> **SUPERSEDED — 2026-08-21."

MD_ROW_MARK = " ·**SUPERSEDED**"

_MD_ERROR = (
    "produced under a defective `T0` vector: `src/step9_b_1_compute.py` divided a "
    "`datetime64[us, UTC]` column by `10 ** 9`, so every premiere-anchored `T0` was "
    "epoch-**seconds ÷ 1000** — a 1970 date — instead of epoch seconds. They are correctly "
    "computed from that vector and are kept as the record of what the defect produced. The "
    "corrected figures are at the same section of `" + EMITTED_MD + "`.")

# A stamp above a table must not claim the whole table: the movement, corner and ratio tables
# carry the ADOPTED arm's rows too, and THIS defect does not reach them.
#
# *** CORRECTED 2026-08-23, decisions/0124 SS5b. *** The earlier wording went one step further
# and said those rows WERE NOT SUPERSEDED. That was true when written and 0124 made it false --
# the adopted arm's CI cells are superseded on 0124's ground and sit in exactly those rows.
# A stamp is a CLAIM: one naming what IS superseded is about a defect that has already happened
# and cannot go stale; one naming what is NOT superseded is about the ABSENCE of a defect and
# goes stale the moment a later ruling creates one in that scope. The sentence is REPLACED, not
# supplemented, and the replacement declines to make the claim at all.
#
# THE CLAUSE IS DEFINED ONCE, HERE, AND THE .md IS REWRITTEN FROM IT. CLAUDE.md: if a claim is
# emitted by a script, the script is where it is withdrawn -- a sentence struck by hand in the
# artifact and left in the generator is written back over it on the next run.
# The exact clause as 0123 rendered it. Kept so the rewrite can find it; it is a SUPERSEDED
# literal and appears nowhere else.
MD_CLAUSE_SUPERSEDED_0123 = (
    "**Rows WITHOUT that mark are not superseded and this defect does not reach them.**")

MD_CLAUSE_CORRECTED = (
    "**This unit defect does not reach rows without that mark. THAT IS A STATEMENT ABOUT THIS "
    "DEFECT AND NOTHING ELSE — it is NOT a claim that such a row is not superseded on some "
    "other ground.** A stamp naming what is *not* superseded is a claim about the ABSENCE of a "
    "defect, and it goes stale the moment a later ruling creates one in that scope "
    "(`decisions/0124` §5b). This stamp's earlier wording did exactly that, and `0124` then "
    "superseded the adopted arm's CI cells. Cells superseded on that ruling's ground carry "
    "their own `·SUPERSEDED-0124` mark.")

MD_STAMP_TABLE = (
    MD_TOKEN + "** Every row of the table below that is marked `·SUPERSEDED` was " + _MD_ERROR
    + " " + MD_CLAUSE_CORRECTED
    + " This stamp covers only the rows marked `·SUPERSEDED`; it exempts nothing else in this "
      "file.")

MD_STAMP_PROSE = (
    MD_TOKEN + "** The figures in the block immediately below were " + _MD_ERROR
    + " **This stamp covers only the block it precedes; it exempts nothing else in this file, "
    "and every other superseded block carries its own.**")


def stamp_md(report):
    old = open(COMMITTED_MD).read().split("\n")
    new = open(CORRECTED_MD).read().split("\n")

    if any(MD_TOKEN in ln for ln in old):
        report["headline_md"] = {"file": "artifacts/step9-headline-b.md",
                                 "marks_written": 0, "already_stamped": True}
        return 0

    sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
    affected = set()
    for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            affected.update(range(i1, i2))

    # The one exclusion, and it is named: the file's own provenance row is not a
    # study figure and is correct for the file it describes.
    excluded = {i for i in affected if old[i].startswith("| **Generated** |")}
    affected -= excluded

    if not affected:
        sys.exit("HARD STOP: the diff against the corrected emission found NO affected line. "
                 "An empty result and a clean result are the same value; this one is empty.")

    # Where each stamp goes. A stamp must not land between a table's header
    # rows and its body: that splits one table into two and the second loses
    # its header. So a block that opens on a table row carries its stamp ABOVE
    # the header rows of the table it belongs to.
    starts, i = [], 0
    while i < len(old):
        if i in affected:
            start = i
            if old[start].startswith("|"):
                while start > 0 and old[start - 1].startswith("|"):
                    start -= 1
            starts.append(start)
            while i < len(old) and i in affected:
                i += 1
        else:
            i += 1
    insert_at = sorted(set(starts))

    out, rows, table_stamps, prose_stamps = [], 0, 0, 0
    for i, line in enumerate(old):
        if i in insert_at:
            if out and out[-1].strip():
                out.append("")
            if line.startswith("|"):
                out.append(MD_STAMP_TABLE)
                table_stamps += 1
            else:
                out.append(MD_STAMP_PROSE)
                prose_stamps += 1
            out.append("")
        if i in affected and line.startswith("|") and line.rstrip().endswith("|"):
            stripped = line.rstrip()
            line = stripped[:-1].rstrip() + MD_ROW_MARK + " |"
            rows += 1
        out.append(line)
    blocks = len(insert_at)

    with open(COMMITTED_MD, "w") as fh:
        fh.write("\n".join(out))

    report["headline_md"] = {
        "file": "artifacts/step9-headline-b.md",
        "affected_lines_marked": len(affected),
        "table_rows_marked_inline": rows,
        "stamp_blocks_written": blocks,
        "stamp_blocks_above_a_table": table_stamps,
        "stamp_blocks_above_prose": prose_stamps,
        "why_two_wordings": ("the movement, corner and ratio tables carry the ADOPTED arm's "
                             "rows as well, and THIS defect does not reach them. A stamp above "
                             "such a table claims only the rows marked inline and says so, "
                             "because asserting a defect that is not there is the error this "
                             "exercise guards against. CORRECTED 2026-08-23: the wording used "
                             "to add that the unmarked rows were NOT SUPERSEDED, which "
                             "decisions/0124 falsified -- see MD_CLAUSE_CORRECTED."),
        "lines_excluded_by_name": sorted(old[i][:40] for i in excluded),
        "why_excluded": ("the file's own provenance row is not a study figure and is correct "
                         "for the file it describes"),
        "granularity_note": ("a markdown table row cannot carry a per-cell stamp without "
                             "breaking the table, so each affected row carries a visible "
                             "inline mark and the full stamp sits immediately above the block "
                             "it covers. It is not a file-level header and it exempts nothing."),
        "scope_note": ("THE 2026-08-21 RULING NAMED TWO JSON FILES. This third file is arm b's "
                       "own deliverable and carries the same superseded figures in prose; "
                       "leaving it unmarked would publish them unmarked beside a corrected "
                       "emission. REPORTED to the Human Lead as a scope extension."),
    }
    return blocks


# ---------------------------------------------------------------------------
# 3b. The headline .md -- the 0124 layer, and the correction of a stale claim
#
# TWO JOBS, and the first is a CORRECTION rather than an addition.
#
# (1) 0123's table stamp ended: "Rows WITHOUT that mark are not superseded and this defect
#     does not reach them." The second half is still true. THE FIRST HALF IS NOT. Under
#     decisions/0124 the adopted arm's CI cells are superseded, and those rows carried no
#     mark -- so the sentence tells the reader the opposite of what is true, at the point of
#     use, in the one place a reader would look to check. It is REWRITTEN, not supplemented:
#     0124 SS5b, "a stamp asserting something untrue is worse than no stamp -- a reader
#     TRUSTS it precisely where it misleads."
#
# (2) The adopted arm's CI cells are marked, PER CELL and not per row. A row here carries a
#     point estimate, a pair count and a horizon beside its interval, and none of those moved.
#     0123's granularity note said a markdown row cannot carry a per-cell stamp without
#     breaking the table -- true of a STAMP BLOCK, false of an inline marker, which sits
#     inside the cell and leaves the pipes alone. Marking the whole row would have asserted a
#     defect in the point estimate, which is exactly the error this exercise is about.
# ---------------------------------------------------------------------------

MD_TOKEN_0124 = "> **SUPERSEDED — 2026-08-23 (`decisions/0124`)."
MD_ROW_MARK_0124 = " ·**SUPERSEDED-0124**"

MD_STAMP_0124 = (
    MD_TOKEN_0124 + "** Every CELL in the table below marked `·SUPERSEDED-0124` was produced "
    "under a resampling design `decisions/0124` has since fixed against: this arm drew its "
    "bootstrap frame **per mask** — the accounts contributing to each group — and **re-seeded** "
    "the generator per group. `0124` fixes the frame as every account with at least one pair in "
    "the position-4 output, built once and drawn for every quantity, and fixes the draw order as "
    "one RNG seeded once per file whose stream is consumed continuously. The marked cells are "
    "correctly computed under the superseded design and are kept as the record of what it "
    "produced. The corrected figures are at the same section of `" + EMITTED_MD + "`. "
    "**THIS STAMP COVERS ONLY THE CELLS MARKED `·SUPERSEDED-0124`; it exempts nothing else in "
    "this file AND IT ASSERTS NOTHING ABOUT ANY CELL IT DOES NOT MARK.**")

# Which columns of which table may carry a 0124 mark, and which are PROTECTED. Keyed on the
# WHOLE header row, not on a column name: `width` is a CI width in the level table and a BOUND
# width in the bound table, and a rule keyed on the name alone would treat them alike. That is
# 0123 SS6d's lesson -- one name, two readings, four levels apart -- in a second file.
# A table whose header signature is not in this map HARD STOPS. There is no default.
MD_TABLE_RULES = {
    "outcome|share (post-liveness)|pairs|95% CI, **LEVEL**|width|horizon":
        {"ci": {4, 5}, "protected": {1, 2, 3, 6}},
    "arm|population|outcome|95% CI, **MOVEMENT**|width|level width|ratio":
        {"ci": {4, 5, 6, 7}, "protected": {1, 2, 3}},
    "arm|population|quantity|ratio":
        {"ci": {4}, "protected": {1, 2, 3}},
    "bound|floor|ceiling|width|on":
        {"ci": set(), "protected": {1, 2, 3, 4, 5}},
    "quantity|never started|started and left|continued":
        {"ci": set(), "protected": {1, 2, 3, 4}},
}

ADOPTED_ARM_ID = "W108_s2_finale"


def _cells(line):
    return line.split("|")


def restamp_md_0124(report):
    raw = open(COMMITTED_MD).read().split("\n")

    # -- job 1: the stale clause, rewritten in place. Idempotent: after the first run there
    #    are zero occurrences of the superseded literal.
    clause_hits = sum(ln.count(MD_CLAUSE_SUPERSEDED_0123) for ln in raw)
    raw = [ln.replace(MD_CLAUSE_SUPERSEDED_0123, MD_CLAUSE_CORRECTED) for ln in raw]

    # -- strip this layer's own previous output, so the file is REBUILT from the measurement
    #    rather than added to. Skip-if-present is the mechanism that let a grown field list go
    #    unwritten (0123 SS6e).
    cleaned, i = [], 0
    while i < len(raw):
        if MD_TOKEN_0124 in raw[i]:
            i += 1
            if i < len(raw) and raw[i].strip() == "":
                i += 1
            continue
        cleaned.append(raw[i].replace(MD_ROW_MARK_0124, ""))
        i += 1
    raw = cleaned

    # -- the alignment view: 0123's stamp lines and row marks removed, so the surviving lines
    #    line up with the corrected emission.
    view, back = [], []
    for idx, ln in enumerate(raw):
        if MD_TOKEN in ln:
            continue
        view.append(ln.replace(MD_ROW_MARK, ""))
        back.append(idx)

    new = open(CORRECTED_MD).read().split("\n")
    pairs = {}
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, view, new, autojunk=False).get_opcodes():
        if tag == "replace" and (i2 - i1) == (j2 - j1):
            for k in range(i2 - i1):
                pairs[i1 + k] = j1 + k

    section, header_of = "", {}
    protected_compared = 0
    marks, tables = [], set()
    for vi, ln in enumerate(view):
        if ln.startswith("#"):
            section = ln
        if not ln.startswith("|"):
            continue
        # the header of this row's own table
        h = vi
        while h > 0 and view[h - 1].startswith("|"):
            h -= 1
        header_of[vi] = h
        if h == vi or (h + 1 == vi):          # the header row and its alignment row
            continue
        if ADOPTED_ARM_ID not in ln and ADOPTED_ARM_ID not in section:
            continue
        if vi not in pairs:
            continue
        sig = "|".join(c.strip() for c in _cells(view[h])[1:-1])
        rule = MD_TABLE_RULES.get(sig)
        if rule is None:
            sys.exit("HARD STOP: an adopted-arm table at line %d has header signature %r, which "
                     "is not in MD_TABLE_RULES. Which of its columns are CI columns cannot be "
                     "guessed from a column NAME -- `width` is a CI width in one table and a "
                     "bound width in another. Add the signature or do not mark the table."
                     % (h + 1, sig))
        a, b = _cells(view[vi]), _cells(new[pairs[vi]])
        if len(a) != len(b):
            sys.exit("HARD STOP: adopted-arm row at line %d has %d cells and its counterpart in "
                     "the corrected emission has %d; they are not the same row."
                     % (back[vi] + 1, len(a), len(b)))
        # THE RULE MUST CLASSIFY EVERY COLUMN. Without this, a column listed in neither set is
        # silently neither marked nor policed, and a table that GAINS a column keeps its old
        # header signature only if the addition is invisible -- which is the failure mode a
        # residual "everything else is a stray" branch would have hidden rather than caught.
        inner = set(range(1, len(a) - 1))
        if (rule["ci"] | rule["protected"]) != inner:
            sys.exit("HARD STOP: the MD_TABLE_RULES entry for %r classifies columns %s but the "
                     "table has columns %s. Every column must be declared either CI or "
                     "protected; an unclassified column is neither marked nor policed."
                     % (sig, sorted(rule["ci"] | rule["protected"]), sorted(inner)))
        # *** A CONDITIONAL MARK IS A FUNCTION OF TWO FILES: WHEN EITHER MOVES, THE MARK
        # *** SET MOVES. THIS IS THE BRANCH WHERE THAT WAS MEASURED. `a` is the committed
        # *** cell and `b` is the corrected emission's; a mark is written iff they differ,
        # *** so a change to `b` ALONE re-partitions the marks in `a`'s file -- in BOTH
        # *** directions, newly-superseded and newly-superfluous alike. RECOMPUTE ON EITHER
        # *** SIDE'S CHANGE. See CONDITIONAL_MARK_RULE above.
        differing = {k for k in range(len(a)) if a[k].strip() != b[k].strip()}
        protected_compared += len(rule["protected"])
        moved_protected = sorted(differing & rule["protected"])
        if moved_protected:
            # Checked BEFORE the CI columns so this guard is REACHABLE. A protected column is
            # by construction not a CI column, so a residual "not a CI column" test placed
            # first would dominate it and this branch could never fire -- a guard that cannot
            # fire is the thing 0123 SS3 forbids, and it was in the first draft of this file.
            sys.exit("HARD STOP: protected cells moved on the adopted arm at line %d, columns "
                     "%s -- a point estimate, a pair count, a bound or a horizon. The ruling "
                     "keeps them unmarked BECAUSE they did not move, and they did: %s"
                     % (back[vi] + 1, moved_protected,
                        [(a[k].strip(), b[k].strip()) for k in moved_protected]))
        hit = sorted(differing & rule["ci"])
        if hit:
            marks.append((back[vi], hit))
            tables.add(back[h])

    if protected_compared == 0:
        sys.exit("HARD STOP: zero protected cells were compared, so 'no protected cell moved' "
                 "reports that nothing was looked at, not that nothing was found.")
    if not marks:
        sys.exit("HARD STOP: no adopted-arm cell was found to have moved. The 0124 rerun moves "
                 "24 CI endpoints in this arm; finding none means the diff aligned nothing.")

    cells_marked = 0
    for line_idx, cols in marks:
        c = _cells(raw[line_idx])
        for k in cols:
            c[k] = c[k].rstrip() + MD_ROW_MARK_0124 + " "
            cells_marked += 1
        raw[line_idx] = "|".join(c)

    for h in sorted(tables, reverse=True):
        raw[h:h] = [MD_STAMP_0124, ""]

    with open(COMMITTED_MD, "w") as fh:
        fh.write("\n".join(raw))

    report["headline_md_0124"] = {
        "file": "artifacts/step9-headline-b.md",
        "ruling": "decisions/0124 -- the resampling frame and the draw order are fixed",
        "stale_clause_occurrences_rewritten": clause_hits,
        "what_the_stale_clause_said": MD_CLAUSE_SUPERSEDED_0123,
        "why_rewritten_not_supplemented": (
            "it asserted that rows without a 0123 mark are not superseded. 0124 superseded the "
            "adopted arm's CI cells, which sit in exactly those rows. A stamp asserting "
            "something untrue is worse than no stamp: a reader trusts it precisely where it "
            "misleads (0124 SS5b)."),
        "rows_carrying_a_marked_cell": len(marks),
        "cells_marked": cells_marked,
        "tables_stamped": len(tables),
        "protected_cells_compared": protected_compared,
        "protected_cells_moved": 0,
        "granularity": (
            "PER CELL, not per row. A row carries a point estimate, a pair count and a horizon "
            "beside its interval and none of those moved; marking the row would assert a defect "
            "in all of them. An inline marker inside a cell does not break the table."),
        "known_limit_reported_not_worked_around": (
            "src/check_surfaces.py matches a .md figure against the register LINE-LOCALLY, so a "
            "mark anywhere on a row labels every number on that row for the numeric half. The "
            "unmarked cells on a marked row are therefore not policed by that control while the "
            "mark is present. REPORTED to the Human Lead; not worked around inside a shared "
            "control this arm does not own."),
    }
    return cells_marked


def main():
    report = {
        "run": "Step 9, arm b -- STAMP the superseded premiere figures",
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "authorised_by": "Human Lead ruling, 2026-08-21: STAMP, DO NOT DELETE.",
        "generator": "src/step9_b_6_stamp_superseded.py",
        "generator_sha256_12": sha12(os.path.abspath(__file__)),
        "the_unit_error": THE_ERROR,
        "the_mark_set_is_not_stable": CONDITIONAL_MARK_RULE,
        "adopts": "nothing",
        "api_calls": 0,
        "stamps_are_negative_only": ("no stamp restates a corrected figure; each names what is "
                                     "superseded and points at the corrected block, so the "
                                     "positive grep cannot pass on a stamp alone"),
    }
    try:
        report["git_head_short"] = subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        report["git_head_short"] = None

    # LAYER ORDER. The 0123 layer runs first and owns the premiere region; the 0124 layer runs
    # second and owns the adopted arm. The two regions are DISJOINT and strip_stamps() removes
    # either token, so neither layer can consume or duplicate the other's marks. The .md
    # correction runs last because it rewrites a sentence the 0123 layer wrote.
    n = stamp_headline(report)
    n += stamp_headline_0124(report)
    n += stamp_working(report)
    n += stamp_md(report)
    n += restamp_md_0124(report)
    report["total_stamp_sites_written"] = n
    report["layers"] = {
        "0123": "the premiere-clock unit error -- the W91_s2_premiere region",
        "0124": ("the resampling frame and draw order -- the W108_s2_finale region, CI "
                 "endpoints and CI-derived figures only. Point estimates, numerators, "
                 "denominators, bounds, widths, ceilings, sums and pair counts are NOT marked, "
                 "and the guards in stamp_headline_0124() hard stop if any of them moved."),
    }

    out = os.path.join(ROOT, "logs", "step9_b_stamp_run.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nrun record: logs/step9_b_stamp_run.json")


if __name__ == "__main__":
    main()
