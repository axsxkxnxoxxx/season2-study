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
SEP = " || "

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
    while text.startswith(TOKEN):
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


def removed_text(fields, corrected_path):
    return REMOVED_TEXT % (TOKEN, ", ".join(fields), corrected_path)


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
    report["headline_not_marked"] = [
        "$.arms[%d] (W108_s2_finale) -- verified leaf-for-leaf identical to the corrected "
        "emission and its harness control reproduces; marking it would assert a defect that "
        "is not there" % i for i in finale_arm]

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
# 2. The working-figures JSON -- this arm's own format, not schema-bound
# ---------------------------------------------------------------------------

def stamp_working(report):
    old = json.load(open(COMMITTED_WORKING))
    new = json.load(open(CORRECTED_WORKING))
    old_leaves = dict(leaves(old, "$"))
    new_leaves = dict(leaves(new, "$"))

    def in_region(path):
        return ("W91_s2_premiere" in path) or path.startswith("$.t0_movement")

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
                block[field] = removed_text([field], EMITTED_WORKING)
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

# A stamp above a table must not claim the whole table. The movement, corner and
# ratio tables carry the ADOPTED arm's rows too, and those rows are not
# superseded -- asserting a defect that is not there is the error this whole
# exercise is guarding against.
MD_STAMP_TABLE = (
    MD_TOKEN + "** Every row of the table below that is marked `·SUPERSEDED` was " + _MD_ERROR
    + " **Rows WITHOUT that mark are not superseded and this defect does not reach them.** "
    "This stamp covers only the marked rows; it exempts nothing else in this file.")

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
                             "rows as well, and those are not superseded. A stamp above such a "
                             "table claims only the rows marked inline and says so, because "
                             "asserting a defect that is not there is the error this exercise "
                             "guards against."),
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


def main():
    report = {
        "run": "Step 9, arm b -- STAMP the superseded premiere figures",
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                   .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "authorised_by": "Human Lead ruling, 2026-08-21: STAMP, DO NOT DELETE.",
        "generator": "src/step9_b_6_stamp_superseded.py",
        "generator_sha256_12": sha12(os.path.abspath(__file__)),
        "the_unit_error": THE_ERROR,
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

    n = stamp_headline(report)
    n += stamp_working(report)
    n += stamp_md(report)
    report["total_stamp_sites_written"] = n

    out = os.path.join(ROOT, "logs", "step9_b_stamp_run.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nrun record: logs/step9_b_stamp_run.json")


if __name__ == "__main__":
    main()
