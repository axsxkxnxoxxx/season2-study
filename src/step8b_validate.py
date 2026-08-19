"""Step 8b — validator for the Step 16 output schema.

Two halves:

  1. A minimal JSON Schema (draft 2020-12 subset) evaluator. `jsonschema` is not
     installed in this environment and installing it needs the network, which
     Step 8b is not permitted to touch, so the subset the schema uses is
     implemented here and the schema is restricted to it. The subset is:
     type, required, properties, additionalProperties, patternProperties,
     propertyNames, items, minItems, maxItems, uniqueItems, enum, const, $ref
     (local only), anyOf, oneOf, allOf, not, if/then/else, minimum, maximum,
     minLength, pattern.

  2. Semantic checks the schema language cannot express: cross-field equalities,
     referential integrity of the two ref families, the sentinel discipline that
     makes a placeholder unmistakable, and branch coverage.

Every check reports the number of sites it examined, and there are FOUR terminal
states rather than three. A check that looked at nothing and cannot say why
reports VACUOUS and counts as a FAILURE, per CLAUDE.md: "an empty result and a
clean result are the same value, and only the control knows which it produced."
A check whose set is empty and whose FILE declares the emptiness -- with a
search record and its coverage count -- reports EMPTY_DECLARED and does not.
That split is reviewer-engineering's F4: the previous version failed a
legitimately empty optional array, which reads "no unreconciled divergence was
found" as "looked nowhere" and inverts the rule it was written from.

SIX CHECKS ADDED AT v1.3.0, against decisions/0109 and reviewer-engineering's M1,
M2, M6, M7, M8 and M10. S30 -- a merged document's two arms come from two named
input FILES, use two sampling-width convention labels and carry a diff record
with content, because ISOLATION IS UNOBSERVABLE BUT ARITY IS OBSERVABLE, and a
merged document assembled from ONE arm file used to validate clean and publish
that the arms agreed everywhere. S31 -- duality is read against the producing
step, so the loosening the split forbade is no longer reachable by RELABELLING.
S32 -- an interval references its OWN arm's bootstrap settings. S33 -- no search
claims to have run while examining nothing. S34 -- ownership reaches the nested
blocks, not only depth 1. S35 -- no oneOf or anyOf sits above
$defs/by_producing_arm, which is the machine-checked form of the constraint
decisions/0109 §4 records: it is the only reason the `dual_status` rename fails
loudly rather than as a silent "matched 0 oneOf branches".

ONE CHECK ADDED AND FOUR CHANGED AT v1.4.0, against decisions/0111. S36 -- NO
ENTRY AND NO FILE CARRIES A BLOCK PUBLISHED BY ANOTHER STEP, which is the
direction nothing policed: the file was checked for writing too LITTLE and never
for writing too MUCH, and that asymmetry let a single-arm step's placeholder ship
carrying a block its own ownership table gave to another step. S2 -- the entry key
gained the PRODUCING STEP, so two steps' measurements at one (W, clock origin)
setting are two entries rather than a duplicate. S22 -- the publisher table moved
OUT OF THE FILE UNDER TEST, because a table read from the file under test could
only agree with itself, and the file's own table is now asserted against the
external one. S30 -- the input list is read in BOTH directions, so a merge that
DROPS an entire declared source no longer validates clean, and the list records
SOURCES rather than only arm files. S35 -- widened from one container to the
family of six, and its root-side scan, which was dead code, fixed.

TWO CHECKS ADDED AND THREE CHANGED AT v1.6.0, against decisions/0118, which fixes
the bootstrap STATISTIC as BOTH levels and paired movements and closes the third
and last unfixed bootstrap element. S40 -- THE REGISTRY RECORDS THE STATISTIC AS A
VALUE, not as a declaration that a choice exists: both objects in
$.bootstrap_spec and in every settings entry, listed as fixed, with the fixed and
not-fixed lists partitioning a DECLARED universe so that an empty not-fixed list
is established rather than merely empty. S41 -- BOTH OBJECTS ACTUALLY APPEAR
among the intervals of every producing arm, because S40 checks what a file
declares and this checks what it emits. S23 -- the statistic is compared by
MEMBERSHIP rather than by equality, the registry now holding both objects while
an interval is one of them. S18 -- `statistic` joined the point-of-use set. S32 --
unchanged in code and NARROWER IN FORCE, for the reason written once at
REGISTRY_ARM_DIFFERENCE_FACT below and restated nowhere.

THREE CHECKS CHANGED AT v1.7.0, against the Human Lead's ruling of 2026-08-19 on
reviewer-engineering's v1.6.0 review. S41 -- ITS EMPTY BRANCH IS SCOPE-AWARE:
Step 12 is EXEMPT from the paired-movement requirement, on the schema's own
warrant that "Step 12 lists every candidate cut and mandates intervals nowhere",
because requiring it to carry intervals would force it to manufacture two figures
it was never asked to compute -- a fabrication to satisfy a control, which is the
defect E1 was -- and would make the schema's own warrant text false. THE EXEMPTION
IS STEP 12'S ALONE and the selftest asserts Steps 9, 10, 11 and 13 still fail that
branch. S40 -- IT POLICES `spec_status`, THE FIELD THAT CARRIES THE CLAIM: the
v1.6.0 form checked `fields_not_fixed_in_spec` by name and never read
`spec_status`, so an entry could declare itself `unfixed_at_time_of_writing` while
listing all four elements as fixed and validate at 41 checks, 0 failures. And each
ENTRY's fixed list gained the partition anchor $.bootstrap_spec got one level up,
so an entry that silently drops B, the seed and the unit from its fixed list is no
longer indistinguishable from one that declares them.

THREE CHECKS CHANGED AT v1.8.0, on reviewer-engineering's v1.7.0 review. S41 --
ITS OWNER KEY IS (PRODUCING STEP, ARM), NOT ARM: in the merged document `sole` is
Steps 10, 11 and 12 together and `a` is Step 9 AND Step 13, so one step's movement
discharged another step's obligation -- the very reasoning the per-arm keying was
written from, one dimension out, and the dimension decisions/0111 E2 already
ruled is part of a measurement's identity. AND ITS EXEMPTION IS SCOPED TO THE
EMPTY BRANCH: it used to gate the per-owner missing-object branch too, so a Step
12 file emitting forty levels-only intervals passed with a note. The ruling's
ground is that requiring intervals would make Step 12 MANUFACTURE two figures; a
file that has already computed intervals is manufacturing nothing, and
decisions/0118's "a run that emits only one is INCOMPLETE" reaches it directly.
S41's scope-empty branch -- IT NO LONGER AWARDS EMPTY_DECLARED OVER ZERO
COVERAGE: it set `declared_empty` unconditionally, carrying the words "so the
emptiness was searched for rather than assumed" with nothing requiring a single
record to have been examined, which is the rule S33 enforces everywhere else.
S40 -- ITS PARTITION UNIVERSE IS ANCHORED OUTSIDE THE FILE: `fields_considered`
was read out of the entry under test, so `fields_considered: ["statistics"]` with
`fields_fixed_in_spec: ["statistics"]` partitioned cleanly and dropped B, the seed
and the unit out of the record entirely -- decisions/0111 E4 reinstalled by the
fix for it.

SCOPED BY DOCUMENT ROLE at v1.2.0 (decisions/0107). ONE FILE PER ARM: an arm file
is written by an isolated instance, the merged document is Step 13b's, and
$.document_scope says which a file is. Two checks are role-aware -- S17, which no
longer requires an arm file to carry a cross-arm search it is structurally
forbidden to have performed, and S21, whose branch coverage is restricted to the
branches a file's role can reach and NAMES the restriction. Two more are new:
S28, which ties the two duality facts to each other and to the file, and S29,
which keeps the blocks only the merge may fill out of an arm file.

Usage:  python3 src/step8b_validate.py <instance.json> [--schema <schema.json>]
Exit 0 if every check passes, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

# ---------------------------------------------------------------------------
# 1. Minimal JSON Schema evaluator
# ---------------------------------------------------------------------------

_TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _is_type(value: Any, name: str) -> bool:
    if name == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if name == "boolean":
        return isinstance(value, bool)
    py = _TYPES.get(name)
    if py is None:
        raise ValueError(f"unsupported type keyword: {name}")
    if py is dict or py is list or py is str:
        return isinstance(value, py)
    return isinstance(value, py)


class SchemaEvaluator:
    """Validates an instance and records where measurement slots were applied."""

    def __init__(self, schema: dict):
        self.root = schema
        self.errors: list[str] = []
        # instance path -> True, for every node a subschema carrying
        # "x-measurement": true was applied to.
        self.measurement_sites: dict[str, bool] = {}
        # instance path -> True, for every node carrying "x-writer-text": true,
        # i.e. a string slot whose content is run-specific and is supplied by the
        # step that writes it. Structural text -- definitions, refs, reasons that
        # are the same in every file -- is deliberately not marked.
        self.writer_text_sites: dict[str, bool] = {}
        self.enum_hits: dict[str, set] = {}

    def resolve(self, ref: str) -> dict:
        if not ref.startswith("#/"):
            raise ValueError(f"only local refs are supported: {ref}")
        node: Any = self.root
        for part in ref[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            node = node[part]
        return node

    def validate(self, instance: Any, schema: dict | bool, path: str = "$") -> bool:
        if schema is True:
            return True
        if schema is False:
            self.errors.append(f"{path}: schema is false, nothing validates here")
            return False

        if "$ref" in schema:
            target = self.resolve(schema["$ref"])
            ok = self.validate(instance, target, path)
            rest = {k: v for k, v in schema.items() if k != "$ref"}
            if rest:
                ok = self.validate(instance, rest, path) and ok
            return ok

        ok = True

        if schema.get("x-measurement") is True:
            self.measurement_sites[path] = True
        if schema.get("x-writer-text") is True:
            self.writer_text_sites[path] = True

        if "type" in schema:
            names = schema["type"]
            names = [names] if isinstance(names, str) else names
            if not any(_is_type(instance, n) for n in names):
                self.errors.append(
                    f"{path}: expected type {names}, got {type(instance).__name__}"
                )
                return False

        if "const" in schema and instance != schema["const"]:
            self.errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")
            ok = False

        if "enum" in schema:
            if instance not in schema["enum"]:
                self.errors.append(f"{path}: {instance!r} not in enum {schema['enum']}")
                ok = False
            else:
                key = schema.get("x-enum-id", path)
                self.enum_hits.setdefault(key, set()).add(
                    instance if isinstance(instance, (str, int, bool)) else str(instance)
                )

        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                self.errors.append(
                    f"{path}: string shorter than minLength {schema['minLength']}"
                )
                ok = False
            if "pattern" in schema and not re.search(schema["pattern"], instance):
                self.errors.append(f"{path}: {instance!r} does not match {schema['pattern']}")
                ok = False

        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            if "minimum" in schema and instance < schema["minimum"]:
                self.errors.append(f"{path}: {instance} < minimum {schema['minimum']}")
                ok = False
            if "maximum" in schema and instance > schema["maximum"]:
                self.errors.append(f"{path}: {instance} > maximum {schema['maximum']}")
                ok = False

        if isinstance(instance, dict):
            for key in schema.get("required", []):
                if key not in instance:
                    self.errors.append(f"{path}: missing required property {key!r}")
                    ok = False
            props = schema.get("properties", {})
            pattern_props = schema.get("patternProperties", {})
            for key, value in instance.items():
                handled = False
                if key in props:
                    ok = self.validate(value, props[key], f"{path}.{key}") and ok
                    handled = True
                for pat, sub in pattern_props.items():
                    if re.search(pat, key):
                        ok = self.validate(value, sub, f"{path}.{key}") and ok
                        handled = True
                if not handled and "additionalProperties" in schema:
                    ap = schema["additionalProperties"]
                    if ap is False:
                        self.errors.append(f"{path}: property {key!r} is not permitted here")
                        ok = False
                    elif ap is not True:
                        ok = self.validate(value, ap, f"{path}.{key}") and ok
            if "propertyNames" in schema:
                for key in instance:
                    ok = self.validate(key, schema["propertyNames"], f"{path}.<name:{key}>") and ok

        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                self.errors.append(f"{path}: {len(instance)} items < minItems {schema['minItems']}")
                ok = False
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                self.errors.append(f"{path}: {len(instance)} items > maxItems {schema['maxItems']}")
                ok = False
            if schema.get("uniqueItems"):
                seen = [json.dumps(i, sort_keys=True) for i in instance]
                if len(set(seen)) != len(seen):
                    self.errors.append(f"{path}: items are not unique")
                    ok = False
            if "items" in schema:
                for i, item in enumerate(instance):
                    ok = self.validate(item, schema["items"], f"{path}[{i}]") and ok

        for kw in ("allOf",):
            for i, sub in enumerate(schema.get(kw, [])):
                ok = self.validate(instance, sub, path) and ok

        if "anyOf" in schema:
            saved = list(self.errors)
            if not any(
                self._quiet(instance, sub, path) for sub in schema["anyOf"]
            ):
                self.errors = saved
                self.errors.append(f"{path}: matches none of the anyOf branches")
                ok = False
            else:
                self.errors = saved

        if "oneOf" in schema:
            saved = list(self.errors)
            matches = sum(1 for sub in schema["oneOf"] if self._quiet(instance, sub, path))
            self.errors = saved
            if matches != 1:
                self.errors.append(f"{path}: matched {matches} oneOf branches, expected exactly 1")
                ok = False
            else:
                for sub in schema["oneOf"]:
                    if self._quiet(instance, sub, path):
                        ok = self.validate(instance, sub, path) and ok
                        break

        if "not" in schema and self._quiet(instance, schema["not"], path):
            self.errors.append(f"{path}: matched a schema it must not match")
            ok = False

        if "if" in schema:
            if self._quiet(instance, schema["if"], path):
                if "then" in schema:
                    ok = self.validate(instance, schema["then"], path) and ok
            elif "else" in schema:
                ok = self.validate(instance, schema["else"], path) and ok

        return ok

    def _quiet(self, instance: Any, schema: dict | bool, path: str) -> bool:
        saved_errors = list(self.errors)
        saved_sites = dict(self.measurement_sites)
        saved_text = dict(self.writer_text_sites)
        saved_enums = {k: set(v) for k, v in self.enum_hits.items()}
        result = self.validate(instance, schema, path)
        self.errors = saved_errors
        self.measurement_sites = saved_sites
        self.writer_text_sites = saved_text
        self.enum_hits = saved_enums
        return result


# ---------------------------------------------------------------------------
# 2. Semantic checks
# ---------------------------------------------------------------------------

SENTINEL_COUNT = -999
SENTINEL_PERCENT = -999.0
PLACEHOLDER_PREFIX = "PLACEHOLDER — NOT A MEASUREMENT"

# The steps the Human Lead owns among the writers. ONE FILE PER ARM
# (decisions/0107): the merged reader-facing document is Step 13b's, and it is
# the only document that reads both arms. A file whose producing step is not one
# of these is an ARM FILE, written by an isolated instance that is structurally
# forbidden to have performed a cross-arm search -- which is why check S17 does
# not apply to it.
HUMAN_LEAD_STEPS = ("human_lead", "step13b")

# WHICH STEPS ARE DUAL IS A FIXED FACT OF THE SPEC (CLAUDE.md, Dual
# implementation; Step 13's duality is decisions/0103 §3). It is repeated here
# rather than read out of the file, because the point of check S31 is to compare
# what the file SAYS against what the spec FIXES: a table read from the file
# under test could only agree with itself.
STEP_DUALITY = {
    "step9": "dual",
    "step10": "single_arm",
    "step11": "single_arm",
    "step12": "single_arm",
    "step13": "dual",
}

# WHICH STEP PUBLISHES EACH PER-ARM BLOCK, HELD OUTSIDE THE FILE UNDER TEST.
# Added at v1.4.0 (decisions/0111 E4). Check S22 used to read `ownership_map`
# out of the instance it was checking, so ANY ARM FILE COULD EXEMPT ITSELF FROM
# S22 BY EDITING ONE STRING IN ITS OWN TABLE -- and `d3_prime` and
# `retained_by_air_period` had no other backstop at all. Check S31 already
# recorded why that cannot work: "a table read from the file under test could
# only agree with itself." THAT REASONING IS CARRIED ACROSS HERE. The file's own
# table is still read -- and is now ASSERTED AGAINST THIS ONE, so a file that
# rewrites it fails on the rewrite rather than escaping through it.
BLOCK_PUBLISHER = {
    "waterfall": "step9",
    "abandonment_distribution": "step10",
    "liveness_exclusions": "step9",
    "d3_prime": "step13",
    "retained_by_air_period": "step9",
    "action_type_counts": "step13",
}
# Top-level blocks whose publisher the spec fixes. `subpopulation_cuts` is NOT
# here: Steps 11 and 12 both write cuts into it, so the question is answered per
# ENTRY by each cut's own producing_step.
#
# `channel_classes` AND `discovery_channel_overlap` JOINED AT v1.5.0
# (decisions/0114 E8). Both hold STEP 8's figures -- D4, D9, and the discovery
# channel overlap in its four units -- and `channel_classes` was REQUIRED at the
# top level of every file, so all seven arm files had to fill it: SEVEN WRITERS
# OF A FIGURE NONE OF THEM PRODUCED, with no precedence rule and no agreement
# check. That is the fourth appearance of one-slot-vs-one-definition, and it
# takes the fix the three before it took -- ONE PLACE, and the ABSENCE IDIOM
# everywhere else. The merged document carries them once, filled at Step 13b
# from Step 8's artifact, so the publisher is `step13b`.
#
# `discovery_channel_overlap` WAS CHECKED RATHER THAN ASSUMED, as E8 asks: it is
# the same shape -- Step 8's measured counts, no publisher row, nothing stopping
# seven files from each writing them -- and differs only in being OPTIONAL rather
# than required, so the defect was reachable rather than shipped.
TOP_LEVEL_PUBLISHER = {
    "tested_ranges": "step13",
    "variants": "step13",
    "channel_classes": "step13b",
    "discovery_channel_overlap": "step13b",
}
# The steps that publish a headline payload of their own.
HEADLINE_PUBLISHERS = ("step9", "step13")
# The entry families whose entries name their own producing step.
ENTRY_FAMILIES = ("arms", "variants", "subpopulation_cuts")

# WHICH STEP MAY DECLARE AN INTERVAL ON EACH QUANTITY CLASS (decisions/0114 E11).
# `$.declared_intervals` sat outside ENTRY_FAMILIES and outside
# TOP_LEVEL_PUBLISHER, so nothing asked whose interval an entry was -- an arm
# file could carry another step's, and the shipped single-arm placeholder was
# OCCUPIED by exactly that: it attributed the WINDOW-W PERCENTILE to `step11`,
# which does not compute W. W is derived at Step 6 and reported at Step 9's two
# window arms and across Step 13's grid; Steps 10, 11 and 12 do not vary it.
# `other_declared` is open to every writer by construction -- it is the class for
# a quantity the record has not ruled on -- so it names no publisher here and the
# arm-identity clause is the only one that applies to it.
INTERVAL_CLASS_PUBLISHERS = {
    "outcome_shares": ("step9", "step11", "step12", "step13"),
    "window_w_percentile": ("step9", "step13"),
}

# THE FOUR BOOTSTRAP ELEMENTS THE SPEC FIXES, HELD OUTSIDE THE FILE UNDER TEST
# (v1.8.0, reviewer-engineering E4 on the v1.7.0 review). B, the seed and the
# resampling unit are fixed by decisions/0103 and the statistic by decisions/0118;
# this tuple is written FROM THOSE RULINGS, not read from the generator and not
# read from the instance.
#
# WHY IT HAD TO EXIST. v1.7.0 gave each registry entry a partition anchor -- the
# fixed and not-fixed lists must partition `fields_considered` -- and read
# `fields_considered` OUT OF THE ENTRY BEING CHECKED, where the schema constrains
# it only to a non-empty array of free strings. So an entry declaring
# `fields_considered: ["statistics"]` and `fields_fixed_in_spec: ["statistics"]`
# partitioned perfectly while dropping B, the seed and the unit out of the record
# entirely. THAT IS decisions/0111 E4 -- a table read from the file under test
# could only agree with itself -- REINSTALLED BY THE FIX FOR E2, and it is the
# same defect the S41 fixture had and caught.
#
# The check is CONTAINMENT, not equality: a writer may consider a fifth element
# the record has not ruled on, and must then partition it like any other. What it
# may not do is consider fewer than the four the spec has already fixed.
# src/step8b_selftest.py asserts this tuple against the generator's
# BOOTSTRAP_FIELDS_CONSIDERED, so the two cannot drift in silence.
BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC = ("B", "seed", "resampling_unit", "statistics")

# THE REGISTRY FACT, WRITTEN ONCE (v1.8.0, reviewer-engineering E7 on the v1.7.0
# review). It had three renderings and two of them disagreed: this module's
# docstring said two entries differ only in `producing_arm`, the generator said
# "and `resampling_unit`", and a placeholder note said `producing_arm` alone. The
# disk settles it -- `a_default` and `b_default` differ in `producing_arm` and
# nothing else, and `a_default` and `a_show_clustered` differ in
# `resampling_unit` AND `spec_status`, which is one arm's two quantity classes
# rather than two arms' one setting. So the unit varies by QUANTITY CLASS, never
# by arm. The generator imports this string for the schema description and the
# placeholder note; nothing restates it.
REGISTRY_ARM_DIFFERENCE_FACT = (
    "with all four bootstrap elements fixed and identical across the arms, two registry "
    "entries OF THE SAME QUANTITY CLASS differ only in `producing_arm` -- `resampling_unit` "
    "varies by QUANTITY CLASS and never by arm, the account-clustered and show-clustered "
    "entries being one arm's two classes rather than two arms' one setting -- so a cross-arm "
    "reference misreports the ARM and no longer misreports a setting"
)

# THE KEYS S30 NORMALISES AWAY BEFORE COMPARING TWO ARMS' PAYLOADS -- ONE
# DEFINITION, AND ITS ARITY IS DERIVED FROM IT (reviewer-engineering E3 on the
# v1.6.0 review). These are ARM LABELS: fields whose whole content is which arm a
# payload belongs to, so a comparison meant to ignore that must ignore them.
#
# `statistic` LEFT THIS TUPLE AT v1.6.0 (decisions/0118) -- the statistic is now
# fixed as BOTH for every arm, so two payloads differing on it differ on WHICH
# OBJECT they report, which is a real divergence and not a label. THE WORD "FIVE"
# WAS LEFT TYPED INTO THE SENTENCE THE CHECK EMITS and travelled from there into
# src/step8b_schema.py and into all three placeholders. Nothing here states the
# count; everything that needs it reads ARM_LABELS_ARITY_WORD.
ARM_LABELS_NORMALISED = ("producing_arm", "merged_from", "bootstrap_ref",
                         "convention_label")
_ARITY_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
                7: "seven", 8: "eight", 9: "nine", 10: "ten"}
ARM_LABELS_ARITY = len(ARM_LABELS_NORMALISED)
ARM_LABELS_ARITY_WORD = _ARITY_WORDS.get(ARM_LABELS_ARITY, str(ARM_LABELS_ARITY))


# WHICH PRODUCING STEPS THE SPEC DOES NOT ASK FOR INTERVALS FROM AT ALL.
# Human Lead ruling, 2026-08-19, on reviewer-engineering's v1.6.0 review of S41.
#
# S41 required BOTH bootstrap objects among every producing arm's intervals, and
# failed unconditionally where an arm had none. decisions/0118 fixes the statistic
# as BOTH for every step that PRODUCES intervals; it does not create an obligation
# to produce them. Step 12 has none: this schema's own warrant, at
# $defs.ci_or_absence, says "Step 12 lists every candidate cut and mandates
# intervals nowhere."
#
# THE RULING'S GROUND, RECORDED AS GIVEN: requiring Step 12 to carry intervals
# would force it to manufacture two figures it was never asked to compute, one a
# paired movement between configurations the spec does not name -- a fabrication
# to satisfy a control, which is the defect E1 was. And it would make the schema's
# own warrant text false, which is fixing a control by breaking a statement of
# fact.
#
# THE EXEMPTION IS ONE STEP'S AND MUST NOT WIDEN. Every step outside this table
# fails the empty branch, and src/step8b_selftest.py asserts that for Steps 9, 10,
# 11 and 13 beside the one pass, because an exemption that quietly covers five
# steps when it was granted to one is the shape this study keeps finding.
#
# THE GROUND IS NOT THE PUBLISHER TABLE, AND SAYING SO WAS A DEFECT (v1.8.0,
# reviewer-engineering E6). This comment used to read "Steps 9, 10, 11 and 13 all
# publish outcome-share intervals", which INTERVAL_CLASS_PUBLISHERS does not
# support: it names Steps 9, 11, 12 and 13 on `outcome_shares` and does NOT name
# Step 10. The table is a PERMISSION -- who may attribute an interval on a class
# -- and this one is a MANDATE, and neither implies the other. What actually
# holds: this table has ONE member because ONE step was ruled on. WHETHER STEP 10
# BELONGS IN IT IS UNRULED AND IS REPORTED TO THE HUMAN LEAD RATHER THAN DECIDED
# HERE; an arm may not widen a ruling to make its own comment true.
#
# THE PERMISSION AND THE MANDATE ARE NOT IN CONFLICT. Step 12 MAY attribute an
# outcome-shares interval (INTERVAL_CLASS_PUBLISHERS) and is REQUIRED to produce
# none (this table); permitted-and-not-required is a coherent pair, and it is what
# makes v1.8.0's narrowing bite -- Step 12 need not publish, and if it does, S41
# holds it to both objects like any other step. What WAS incoherent is the state
# this narrowing removed: the exemption covering the has-intervals case, under
# which Step 12 was permitted to publish a half-run that nothing could see.
#
# The same warrant names Step 13's per-arm SENSITIVITY SERIES as a series of
# shares rather than of intervals. That is NOT a step-level exemption: Step 13
# also writes the headline, where the intervals are mandated, so its arm file
# still owes both objects and is not listed here.
INTERVALS_NOT_MANDATED_BY_STEP = {
    "step12": (
        "the schema's own warrant at $defs.ci_or_absence -- \"Step 12 lists every candidate "
        "cut and mandates intervals nowhere\" -- so requiring intervals here would make the "
        "writing step manufacture two figures the spec never asked it to compute, one of them "
        "a paired movement between configurations the spec does not name"
    ),
}

# THE PER-ARM BLOCKS THAT HAVE NO PRODUCER AT A PREMIERE-ANCHORED ARM
# (decisions/0114 E13). PUBLISHER ROWS KEY ON ARM IDENTITY, NOT PRODUCING STEP
# ALONE: BLOCK_PUBLISHER says WHICH STEP publishes a block, and S22 read that
# alone, so it required `waterfall`, `liveness_exclusions` and
# `retained_by_air_period` wherever a `step9` entry is primary -- INCLUDING a
# premiere-anchored arm, where the schema's own text says nothing produces one.
# The schema's text and its control disagreed and THE TEXT IS RIGHT.
#
# The warrant is the spec, not the file: Step 8 builds the waterfall at the
# adopted finale-anchored arm, Step 10 charts the headline arm, and Step 13's W
# grid is finale-anchored at every one of its eight arms.
#
# ABSENCE STATED, NOT SILENCE. The record stays required wherever the block would
# otherwise be; what stops being required is a FIGURE NO STEP MAKES.
NO_PRODUCER_AT_CLOCK_ORIGIN = {"s2_premiere"}


def _block_has_producer(entry: dict) -> bool:
    """Whether any step in the spec produces a per-arm block at this arm."""
    return (entry or {}).get("clock_origin") not in NO_PRODUCER_AT_CLOCK_ORIGIN


# THE ARM-ENTRY PROPERTIES THAT ARE NOT BLOCKS (decisions/0114 E12). Held here,
# outside the schema and outside the file, so that a per-arm block added to the
# schema WITHOUT a BLOCK_PUBLISHER row fails check S39 instead of falling through
# both S22 and S36 in silence: S22 iterates BLOCK_PUBLISHER and S36 iterates
# BLOCK_PUBLISHER, so a block the table does not name is a block neither of them
# looks at. Adding a property here is a deliberate declaration that it carries no
# figure; adding one to the schema and nowhere else now fails.
ARM_ENTRY_NON_BLOCK_PROPERTIES = frozenset({
    "arm_id", "W_days", "H_days", "clock_origin", "clock_origin_note",
    "producing_step", "in_arm_grid", "is_primary_headline", "note",
    "adopted_rule_revision",
    # `headline` IS a block and is deliberately not in BLOCK_PUBLISHER: every
    # entry carries the slot and the payload inside it is real only where that
    # entry's producing step publishes a headline, which HEADLINE_PUBLISHERS
    # states and check S28 reads. It is named here so the exemption is a written
    # decision rather than an omission.
    "headline",
})

# THE MERGE'S EXPECTED SOURCES, DERIVED RATHER THAN READ FROM THE FILE
# (decisions/0114, E9/E15). S30 had payload<->input closure in both directions
# and NO EXTERNAL ANCHOR, so a merge that declared five of eight sources and
# dropped the payloads to match closed against itself and validated clean. The
# expected set is derived from STEP_DUALITY -- which already holds the material:
# a dual step contributes arms `a` and `b`, a single-arm step contributes `sole`
# -- plus the non-arm-file sources the spec names. That is S31's reasoning
# carried one level out: A TABLE READ FROM THE FILE UNDER TEST COULD ONLY AGREE
# WITH ITSELF.
NON_ARM_MERGE_SOURCES = {
    # decisions/0111 E6: Step 14's limits section is an eighth source, it has no
    # arm, and Step 13b was moved after Step 14 precisely so it could be filled.
    ("human_lead", None): ("limitations",),
    # decisions/0114 E8: Step 8's artifact supplies the blocks no arm produces.
    ("step8", None): ("channel_classes", "discovery_channel_overlap"),
}


def _expected_merge_sources() -> dict:
    """(producing_step, arm) -> source_kind, for every source a merge must name."""
    out = {}
    for step, duality in STEP_DUALITY.items():
        for arm in (("a", "b") if duality == "dual" else ("sole",)):
            out[(step, arm)] = "arm_file"
    for key in NON_ARM_MERGE_SOURCES:
        out[key] = "non_arm_file"
    return out


def _producing_step(inst: dict) -> str | None:
    """The step whose output this document IS -- not its generator.

    $.generated_by names whatever produced the bytes; a placeholder is generated
    by Step 8b and shows the shape of another step's document. $.document_scope
    is what says whose document this is.
    """
    scope = inst.get("document_scope")
    if isinstance(scope, dict):
        return scope.get("producing_step")
    return None


def _is_merged_document(inst: dict) -> bool:
    return _producing_step(inst) in HUMAN_LEAD_STEPS


class Check:
    """One semantic check, and how many sites it looked at.

    Four terminal states, not three. `VACUOUS` -- looked at nothing and cannot
    say why -- remains a FAILURE, per CLAUDE.md: an empty result and a clean
    result are the same value, and only the control knows which it produced.
    `EMPTY_DECLARED` is the case that used to be swept in with it: the file
    itself declares that the set is empty, says why, and carries the coverage
    count of the search that found it empty. Added at v1.1.0 against
    reviewer-engineering's F4, which found S17 failing a legitimately empty
    optional array -- collapsing "no unreconciled divergence was found" into
    "looked nowhere", which INVERTS the rule it was written from.
    """

    def __init__(self, cid: str, title: str):
        self.cid = cid
        self.title = title
        self.sites = 0
        self.failures: list[str] = []
        self.skipped_reason: str | None = None
        self.declared_empty: str | None = None
        self.coverage: int | None = None
        # Notes a check makes about what it did NOT examine and why, where that
        # is a property of the file's scope rather than a failure. A check whose
        # coverage is legitimately restricted says so here; a restricted pass
        # that says nothing is indistinguishable from a full one.
        self.notes: list[str] = []

    @property
    def status(self) -> str:
        # Failures outrank N/A: a check with a half that runs on a placeholder
        # and a half that cannot must report the failure of the half that ran.
        if self.failures:
            return "FAIL"
        if self.skipped_reason is not None:
            return "N/A"
        if self.sites == 0:
            return "EMPTY_DECLARED" if self.declared_empty else "VACUOUS"
        return "PASS"

    def as_dict(self) -> dict:
        return {
            "id": self.cid,
            "title": self.title,
            "status": self.status,
            "sites_examined": self.sites,
            "failures": self.failures[:20],
            "failure_count": len(self.failures),
            "not_applicable_reason": self.skipped_reason,
            "declared_empty_reason": self.declared_empty,
            "search_coverage_count": self.coverage,
            "scope_notes": self.notes,
        }


def _walk(node: Any, path: str = "$"):
    yield path, node
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}[{i}]")


def _get(node: Any, path: str) -> Any:
    """Resolve a '$.a.b[0].c' path produced by the evaluator or _walk."""
    cur = node
    for token in re.findall(r"\.([^.\[\]]+)|\[(\d+)\]", path):
        name, idx = token
        if name:
            if not isinstance(cur, dict) or name not in cur:
                return _MISSING
            cur = cur[name]
        else:
            i = int(idx)
            if not isinstance(cur, list) or i >= len(cur):
                return _MISSING
            cur = cur[i]
    return cur


_MISSING = object()


ABSENCE_STATUSES = (
    "structurally_absent", "not_published", "not_yet_written", "unruled",
    "no_producer_in_spec", "superseded_for_this_purpose", "not_a_dual_step",
    "awaiting_owner_step", "not_required_by_spec",
)


def _is_absence(node: Any) -> bool:
    return isinstance(node, dict) and node.get("status") in ABSENCE_STATUSES


def _is_block_absence(node: Any) -> bool:
    return isinstance(node, dict) and node.get("block_is_absent") is True


def _iter_payloads(inst: dict):
    """Yield (path, population_block) for every population block in the file."""
    containers = []
    for i, arm in enumerate(inst.get("arms", [])):
        containers.append((f"$.arms[{i}]", arm))
    for i, var in enumerate(inst.get("variants", [])):
        containers.append((f"$.variants[{i}]", var))
    for i, cut in enumerate(inst.get("subpopulation_cuts", [])):
        containers.append((f"$.subpopulation_cuts[{i}]", cut))
    for base, node in containers:
        for pop, block in (node.get("headline") or {}).items():
            yield f"{base}.headline.{pop}", pop, block


def _iter_containers(inst: dict):
    """Yield (path, by_producing_arm) for EVERY per-arm container in the file.

    Not only the headline's. Step 13's six non-headline outputs took the same
    container at v1.4.0 (decisions/0111 E1), and a check that walked only the
    headline would have left the new ones unpoliced -- which is how the headline
    came to be the only block whose duality was read against its producing step.
    """
    for path, node in _walk(inst):
        if isinstance(node, dict) and isinstance(node.get("by_producing_arm"), dict):
            yield f"{path}.by_producing_arm", node["by_producing_arm"]


def _iter_arm_payloads(block: dict, base: str):
    """Yield (path, arm_key, payload) for each producing arm of a population block.

    The container gained a level at v1.1.0 (`by_producing_arm.arms`) so that a
    single-arm step can write one payload under `sole` instead of being made to
    name an `a` and a `b` it does not have (reviewer-engineering F5).
    """
    bpa = block.get("by_producing_arm") or {}
    for key, payload in (bpa.get("arms") or {}).items():
        if isinstance(payload, dict) and not _is_absence(payload):
            yield f"{base}.by_producing_arm.arms.{key}", key, payload


def _ownership_path_present(inst: dict, name: str) -> bool:
    """Is the block an ownership key names actually in this file?

    Ownership keys are top-level names or DOTTED PATHS to nested blocks -- since
    v1.3.0, because ownership stopped at depth 1 and one `arms` entry hid three
    other steps' blocks behind it (reviewer-engineering M8). `arms[].waterfall`
    is present if any arm entry carries it.
    """
    cur = [inst]
    for token in name.split("."):
        nxt = []
        wildcard = token.endswith("[]")
        key = token[:-2] if wildcard else token
        for node in cur:
            if not isinstance(node, dict) or key not in node:
                continue
            value = node[key]
            if wildcard:
                nxt.extend(v for v in (value if isinstance(value, list) else []))
            else:
                nxt.append(value)
        if not nxt:
            return False
        cur = nxt
    return True


def _owning_arm_of(payload: dict) -> str | None:
    return payload.get("producing_arm")


def _iter_cis_with_arm(inst: dict):
    """Yield (path, step, arm, ci) for every interval whose OWNER is knowable.

    THE OWNER IS A (PRODUCING STEP, ARM) PAIR, NOT AN ARM (v1.8.0,
    reviewer-engineering E3). An arm label alone identifies a measurement's owner
    only in an arm file, where one file is one step's. IN THE MERGED DOCUMENT
    `sole` IS STEPS 10, 11 AND 12 TOGETHER AND `a` IS STEP 9 AND STEP 13, so
    attributing by arm let Step 13 arm `a`'s single paired movement discharge Step
    9 arm `a`'s obligation -- which is S41's own reason for keying per arm at all,
    one dimension out. decisions/0111 E2 already ruled the producing step is part
    of a measurement's identity, and S2 keys on it.

    An interval inside a payload belongs to that payload's arm and to the step
    that wrote it; one under $.declared_intervals belongs to the step and arm the
    entry names. Nothing else in the file carries an interval.

    The step is read from the payload's own `written_by_step` first, then the
    block's `by_producing_arm.producing_step`, then the containing entry's
    `producing_step`, then the file's -- most specific first, because in a merged
    document the file's own step is Step 13b, which wrote no interval.
    """
    file_step = _producing_step(inst)
    for fam in ("arms", "variants", "subpopulation_cuts"):
        for i, entry in enumerate(inst.get(fam) or []):
            if not isinstance(entry, dict):
                continue
            entry_step = entry.get("producing_step")
            headline = entry.get("headline")
            if not isinstance(headline, dict):
                continue
            for pop, block in headline.items():
                if not isinstance(block, dict):
                    continue
                base = f"$.{fam}[{i}].headline.{pop}"
                bpa = block.get("by_producing_arm")
                block_step = bpa.get("producing_step") if isinstance(bpa, dict) else None
                for ppath, akey, payload in _iter_arm_payloads(block, base):
                    arm = _owning_arm_of(payload) or akey
                    step = (payload.get("written_by_step") or block_step
                            or entry_step or file_step)
                    for path, node in _walk(payload):
                        if isinstance(node, dict) and "lower" in node and "upper" in node \
                                and "bootstrap_ref" in node:
                            yield ppath + path[1:], step, arm, node
    for i, entry in enumerate(inst.get("declared_intervals") or []):
        ci = entry.get("ci")
        if isinstance(ci, dict) and "bootstrap_ref" in ci:
            yield (f"$.declared_intervals[{i}].ci",
                   entry.get("produced_by_step") or file_step,
                   entry.get("producing_arm"), ci)


def _iter_abandonment(inst: dict):
    """Yield (path, population, abandonment_block) over every arm and row set."""
    for i, arm in enumerate(inst.get("arms", [])):
        dist = arm.get("abandonment_distribution")
        if not isinstance(dist, dict) or _is_block_absence(dist):
            continue
        for pop, node in dist.items():
            if _is_block_absence(node):
                continue
            blocks = node if isinstance(node, list) else [node]
            for j, blk in enumerate(blocks):
                if isinstance(blk, dict) and not _is_block_absence(blk):
                    yield (f"$.arms[{i}].abandonment_distribution.{pop}[{j}]", pop, blk)


# THE PARTITION RULE, WRITTEN ONCE AND APPLIED AT BOTH LEVELS (v1.7.0,
# reviewer-engineering E2). $.bootstrap_spec got `fields_considered` at v1.6.0 so
# that an empty `fields_not_fixed_in_spec` would be ESTABLISHED rather than merely
# empty; each registry ENTRY's own fixed list had no anchor at all. Restating the
# rule at the second level would be two definitions of one rule, which is this
# study's most-repeated defect, so it is one function called twice.
def _partition_failures(where: str, considered, fixed, notfixed) -> list[str]:
    out: list[str] = []
    if not isinstance(considered, list) or not considered:
        out.append(
            f"{where}.fields_considered is absent or empty: without a declared universe, an "
            f"empty fields_not_fixed_in_spec cannot be distinguished from an unfilled one"
        )
    if not isinstance(fixed, list):
        out.append(f"{where}.fields_fixed_in_spec is absent or not a list")
    if not isinstance(notfixed, list):
        out.append(
            f"{where}.fields_not_fixed_in_spec is absent or not a list. It is EMPTY as of "
            f"decisions/0118 on the account-clustered entries, and the empty list is the "
            f"record; deleting it makes the emptiness unreadable"
        )
    if out:
        return out
    uni, f_set, n_set = set(considered), set(fixed), set(notfixed)
    # THE UNIVERSE IS ANCHORED OUTSIDE THE FILE (v1.8.0, E4). Without this the
    # anchor was the entry's own `fields_considered`, and a declared universe of
    # one element partitioned cleanly while dropping three the spec has fixed.
    short = [f for f in BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC if f not in uni]
    if short:
        out.append(
            f"{where}.fields_considered is {sorted(uni)} and does not consider {short}. The "
            f"spec fixes all of {list(BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC)} (decisions/0103, "
            f"decisions/0118), so an element left out of the declared universe is left out of "
            f"the record: the two lists would then partition a universe the writer chose. A "
            f"fifth element may be added; none of these four may be dropped"
        )
    if f_set & n_set:
        out.append(
            f"{where}: {sorted(f_set & n_set)} appear in BOTH the fixed and the not-fixed "
            f"list. A field cannot be both"
        )
    if f_set | n_set != uni:
        out.append(
            f"{where}: the fixed and not-fixed lists do not partition fields_considered. "
            f"Missing from both: {sorted(uni - (f_set | n_set))}; named but not considered: "
            f"{sorted((f_set | n_set) - uni)}"
        )
    return out


# THE STATUS IS DERIVED, NOT DECLARED (v1.7.0, reviewer-engineering E1).
# `unfixed_at_time_of_writing` was RETIRED from the enum in the same change: B,
# the seed and the statistic are fixed for every entry by decisions/0103 and
# decisions/0118, so no entry can have an empty fixed list and the token had no
# reachable referent. It is named here so a file still carrying it fails with a
# message that says WHY rather than with a bare enum error.
_RETIRED_SPEC_STATUS = "unfixed_at_time_of_writing"


def _derive_spec_status(fixed, notfixed) -> str | None:
    if not isinstance(fixed, list) or not isinstance(notfixed, list):
        return None
    if not fixed:
        return None
    return "fixed_in_spec" if not notfixed else "partly_fixed_in_spec"


def run_semantic_checks(inst: dict, ev: SchemaEvaluator) -> list[Check]:
    checks: list[Check] = []
    is_placeholder = bool(inst.get("placeholder"))

    # S1 -- the top-level placeholder flag exists, is boolean, and a placeholder
    #       carries the notice while a real file must not.
    c = Check("S1", "placeholder flag present, boolean, and consistent with the notice block")
    c.sites = 1
    if not isinstance(inst.get("placeholder"), bool):
        c.failures.append("$.placeholder is absent or not boolean")
    else:
        has_notice = "placeholder_notice" in inst
        if is_placeholder and not has_notice:
            c.failures.append("placeholder is true but placeholder_notice is absent")
        if not is_placeholder and has_notice:
            c.failures.append("placeholder is false but placeholder_notice is present")
    checks.append(c)

    # S2 -- arm identity is unique on the declared key, AND THE KEY IS THE ONE
    #       THE FILE DECLARES. The producing step joined the key at v1.4.0
    #       (decisions/0111 E2): Step 9's W = 108 and Step 13's W = 108 are
    #       different measurements of one setting and both must exist, so a
    #       two-field key would have called the second a duplicate of the first.
    c = Check("S2", "arm identity unique on (W_days, clock_origin, producing_step, "
                    "adopted_rule_revision), which is the key $.arm_key declares")
    declared_key = ((inst.get("arm_key") or {}).get("fields"))
    # THE ADOPTED-RULE REVISION JOINED THE KEY AT v1.5.0 (decisions/0114 E14).
    # Same lineage as `clock_origin` and `producing_step`: a setting under which
    # the measurement was taken that was invisible in the key. If a Step 5 or
    # Step 7 amendment lands between Step 9's run and Step 13's, their entries at
    # one setting are DIFFERENT MEASUREMENTS -- and without this dimension this
    # very check calls the rerun a duplicate. The dimension has been occupied
    # once already: processed/step5/adopted_rule.json carried revision-3 figures
    # against the approved revision-6 rule, and a Step 8 instance had to work
    # around it.
    expected_key = ["W_days", "clock_origin", "producing_step", "adopted_rule_revision"]
    c.sites += 1
    if declared_key != expected_key:
        c.failures.append(
            f"$.arm_key.fields is {declared_key!r}; the entry key is {expected_key!r} "
            f"(decisions/0111 E2) and a file that declares a narrower one would report a "
            f"second step's measurement at a shared W as a duplicate"
        )
    seen: dict[tuple, str] = {}
    ids: dict[str, str] = {}
    for i, arm in enumerate(inst.get("arms", [])):
        c.sites += 1
        key = tuple(arm.get(f) for f in expected_key)
        if key in seen:
            c.failures.append(f"$.arms[{i}] repeats arm key {key} first seen at {seen[key]}")
        seen[key] = f"$.arms[{i}]"
        # THE LABEL CARRIES THE WHOLE KEY TOO. Several entries share a setting
        # since v1.4.0, so an arm_id naming only the setting reintroduces the
        # collision for any consumer that indexes by it.
        aid = arm.get("arm_id")
        c.sites += 1
        if aid in ids:
            c.failures.append(
                f"$.arms[{i}].arm_id {aid!r} repeats the label at {ids[aid]} -- entries at one "
                f"setting are distinguished by their producing step, and the label has to say so"
            )
        ids[aid] = f"$.arms[{i}]"
    # And every base_arm_id resolves to an entry in this file: a variant or a cut
    # names the arm it is computed at, and a label that resolves to nothing is a
    # reference a consumer cannot follow.
    for family in ("variants", "subpopulation_cuts"):
        for i, entry in enumerate(inst.get(family) or []):
            if not isinstance(entry, dict) or "base_arm_id" not in entry:
                continue
            c.sites += 1
            if entry["base_arm_id"] not in ids:
                c.failures.append(
                    f"$.{family}[{i}].base_arm_id {entry['base_arm_id']!r} names no arm entry "
                    f"in this file; the labels present are {sorted(ids)}"
                )
    checks.append(c)

    # S3 -- every bootstrap_ref resolves into the registry.
    c = Check("S3", "every bootstrap_ref resolves in $.bootstrap_settings")
    registry = inst.get("bootstrap_settings", {})
    for path, node in _walk(inst):
        if isinstance(node, dict) and "bootstrap_ref" in node:
            c.sites += 1
            ref = node["bootstrap_ref"]
            if ref not in registry:
                c.failures.append(f"{path}.bootstrap_ref = {ref!r} is not in the registry")
    checks.append(c)

    # S4 -- every scope_qualifier_ref resolves.
    c = Check("S4", "every scope_qualifier_ref resolves in $.scope_qualifiers")
    quals = inst.get("scope_qualifiers", {})
    for path, node in _walk(inst):
        if isinstance(node, dict) and "scope_qualifier_ref" in node:
            c.sites += 1
            ref = node["scope_qualifier_ref"]
            if ref not in quals:
                c.failures.append(f"{path}.scope_qualifier_ref = {ref!r} is not defined")
    checks.append(c)

    # S5 -- sentinel discipline over the measurement slots the schema marked.
    c = Check(
        "S5",
        "every x-measurement slot holds a sentinel in a placeholder, and none does in a real file",
    )
    for path in sorted(ev.measurement_sites):
        value = _get(inst, path)
        if value is _MISSING:
            continue
        c.sites += 1
        is_sentinel = value in (SENTINEL_COUNT, SENTINEL_PERCENT)
        if is_placeholder and not is_sentinel:
            c.failures.append(f"{path} = {value!r} is not a sentinel in a placeholder file")
        if not is_placeholder and is_sentinel:
            c.failures.append(f"{path} = {value!r} is a sentinel in a file flagged as real data")
    checks.append(c)

    # S6 -- writer-supplied text. In a placeholder every such slot carries the
    #       prefix; in a real file none of them does, so a leftover placeholder
    #       string cannot survive into a published file unnoticed.
    c = Check(
        "S6",
        "every x-writer-text slot carries the placeholder prefix in a placeholder, "
        "and none does in a real file",
    )
    for path in sorted(ev.writer_text_sites):
        value = _get(inst, path)
        if not isinstance(value, str):
            continue
        c.sites += 1
        prefixed = value.startswith(PLACEHOLDER_PREFIX)
        if is_placeholder and not prefixed:
            c.failures.append(f"{path} is a writer-text slot without the placeholder prefix")
        if not is_placeholder and prefixed:
            c.failures.append(
                f"{path} carries the placeholder prefix in a file flagged as real data"
            )
    checks.append(c)

    # S7 -- never-started carries the absent sub-interval; started-and-left the present one.
    c = Check(
        "S7",
        "never-started sub-interval is structurally absent with a reason; "
        "started-and-left's is present",
    )
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            bounds = payload.get("bounds")
            if not isinstance(bounds, dict) or _is_block_absence(bounds):
                continue
            ns = bounds.get("never_started", {}).get("conditional_sub_interval")
            sl = bounds.get("started_and_left", {}).get("conditional_sub_interval")
            if isinstance(ns, dict):
                c.sites += 1
                if ns.get("applicable") is not False:
                    c.failures.append(f"{ppath}: never-started sub-interval is not marked inapplicable")
                if not isinstance(ns.get("reason"), str) or len(ns.get("reason", "")) < 20:
                    c.failures.append(f"{ppath}: never-started sub-interval carries no reason")
            if isinstance(sl, dict):
                c.sites += 1
                if sl.get("applicable") is not True:
                    c.failures.append(f"{ppath}: started-and-left sub-interval is not marked applicable")
                if "coincides_with_bound" not in sl:
                    c.failures.append(f"{ppath}: started-and-left sub-interval does not record coincidence")
    checks.append(c)

    # S8 -- Continued is never emitted as a point: it carries a ceiling and its
    #       floor slot is an explicit not-published record, not a number.
    c = Check("S8", "Continued carries a ceiling and no floor value")
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            bounds = payload.get("bounds")
            if not isinstance(bounds, dict) or _is_block_absence(bounds):
                continue
            cont = bounds.get("continued")
            if not isinstance(cont, dict):
                continue
            c.sites += 1
            if "ceiling" not in cont:
                c.failures.append(f"{ppath}: Continued has no ceiling")
            floor = cont.get("floor")
            if (
                not isinstance(floor, dict)
                or floor.get("status") not in ABSENCE_STATUSES
                or "percent" in floor
            ):
                c.failures.append(
                    f"{ppath}: the Continued floor is not an explicit "
                    f"absence record -- Continued must never be emitted as a point"
                )
    checks.append(c)

    # S9 -- three ceilings are never presented as simultaneous.
    c = Check("S9", "the three-ceiling block records that they cannot all hold")
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            cch = payload.get("ceilings_cannot_all_hold")
            if not isinstance(cch, dict) or _is_block_absence(cch):
                continue
            c.sites += 1
            if cch.get("simultaneous") is not False:
                c.failures.append(f"{ppath}: simultaneous is not false")
            for field in ("sum_percent", "excess_pp", "excess_pairs"):
                if field not in cch:
                    c.failures.append(f"{ppath}: missing {field}")
    checks.append(c)

    # S10 -- p_at_bound is three-valued everywhere it appears, and the two FALSE
    #        classes are named apart.
    c = Check(
        "S10",
        "p_at_bound emits TRUE/FALSE/null cardinalities and names the two FALSE classes apart",
    )
    for path, node in _walk(inst):
        if not (isinstance(node, dict) and "column_cardinalities" in node and "coextensivity_gap" in node):
            continue
        c.sites += 1
        card = node["column_cardinalities"]
        for field in ("true_count", "false_count", "null_count", "total_rows"):
            if field not in card:
                c.failures.append(f"{path}.column_cardinalities: missing {field}")
        gap = node["coextensivity_gap"]
        for field in ("saturated_not_final", "final_not_saturated", "rows_examined"):
            if field not in gap:
                c.failures.append(f"{path}.coextensivity_gap: missing {field}")
    checks.append(c)

    # S11 -- every endpoint names the population it is computed on, and it is the
    #        population of the block it sits in.
    c = Check("S11", "every bound endpoint names its population and it matches the enclosing block")
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            bounds = payload.get("bounds") or {}
            if _is_block_absence(bounds):
                continue
            for bname, bnode in bounds.items():
                if not isinstance(bnode, dict):
                    continue
                for ename in ("floor", "ceiling"):
                    enode = bnode.get(ename)
                    if not isinstance(enode, dict) or "percent" not in enode:
                        continue
                    c.sites += 1
                    if enode.get("population") != pop:
                        c.failures.append(
                            f"{ppath}.bounds.{bname}.{ename}: "
                            f"population {enode.get('population')!r} != enclosing {pop!r}"
                        )
    checks.append(c)

    # S12 -- the declared derived identities, EVALUATED. Its old title said it
    #        recomputed the declared derived fields while the code evaluated one
    #        identity (reviewer-engineering F8). It now evaluates every family
    #        whose operands the schema fixes -- bound width, sub-interval width,
    #        the three-ceiling sum, the excess, and each share's percentage --
    #        and asserts the file's own `machine_checked` flags against the set
    #        it actually evaluated, so the claim and the code check each other.
    MACHINE_CHECKED_FAMILIES = {
        "$..bounds.*.width_pp",
        "$..conditional_sub_interval.width_pp",
        "$..ceilings_cannot_all_hold.sum_percent",
        "$..ceilings_cannot_all_hold.excess_pp",
        "$..shares.*.value_percent",
    }
    c = Check(
        "S12",
        "the five declared derived identities whose operands this file fixes are evaluated "
        "and hold, and every derived_fields entry's machine_checked flag matches the set "
        "actually evaluated",
    )
    decl = inst.get("derived_fields", [])

    # The flag half runs on a placeholder too: it is a claim about the file, not
    # arithmetic on its sentinels.
    claimed = {d.get("field") for d in decl if d.get("machine_checked") is True}
    declared_fields = {d.get("field") for d in decl}
    for field in sorted(MACHINE_CHECKED_FAMILIES):
        c.sites += 1
        if field not in declared_fields:
            c.failures.append(
                f"$.derived_fields: {field} is evaluated by this check but is not declared"
            )
        elif field not in claimed:
            c.failures.append(
                f"$.derived_fields: {field} is evaluated by this check but its "
                f"machine_checked flag is not true"
            )
    for field in sorted(claimed - MACHINE_CHECKED_FAMILIES):
        c.sites += 1
        c.failures.append(
            f"$.derived_fields: {field} claims machine_checked but no check evaluates it"
        )

    def _num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool)

    if is_placeholder:
        would = 0
        for base, pop, block in _iter_payloads(inst):
            for ppath, arm_key, payload in _iter_arm_payloads(block, base):
                bounds = payload.get("bounds") or {}
                if not _is_block_absence(bounds):
                    would += sum(1 for b in bounds.values()
                                 if isinstance(b, dict) and "width_pp" in b)
                would += len(payload.get("shares") or {})
        c.skipped_reason = (
            f"ARITHMETIC HALF ONLY: this instance is a placeholder and every operand is a "
            f"sentinel, so no identity can be evaluated. {would} arithmetic sites would be "
            f"evaluated on a real file. The flag half of this check DID run: "
            f"{c.sites} declared families were compared against the set the code evaluates, "
            f"with {len(c.failures)} failure(s)."
        )
    else:
        for base, pop, block in _iter_payloads(inst):
            for ppath, arm_key, payload in _iter_arm_payloads(block, base):
                bounds = payload.get("bounds") or {}
                if not _is_block_absence(bounds):
                    for bname, bnode in bounds.items():
                        if not isinstance(bnode, dict):
                            continue
                        if "width_pp" in bnode:
                            fl = (bnode.get("floor") or {}).get("percent")
                            ce = (bnode.get("ceiling") or {}).get("percent")
                            if _num(fl) and _num(ce):
                                c.sites += 1
                                if abs((ce - fl) - bnode["width_pp"]) > 5e-4:
                                    c.failures.append(
                                        f"{ppath}.bounds.{bname}: width_pp "
                                        f"{bnode['width_pp']} != ceiling - floor {ce - fl}"
                                    )
                                if fl > ce:
                                    c.failures.append(
                                        f"{ppath}.bounds.{bname}: floor exceeds ceiling"
                                    )
                        sub = bnode.get("conditional_sub_interval")
                        if isinstance(sub, dict) and sub.get("applicable") is True:
                            fl = (sub.get("floor") or {}).get("percent")
                            ce = (sub.get("ceiling") or {}).get("percent")
                            if _num(fl) and _num(ce) and _num(sub.get("width_pp")):
                                c.sites += 1
                                if abs((ce - fl) - sub["width_pp"]) > 5e-4:
                                    c.failures.append(
                                        f"{ppath}.bounds.{bname}.conditional_sub_interval: "
                                        f"width_pp != ceiling - floor"
                                    )
                    ceilings = [
                        ((bounds.get(o) or {}).get("ceiling") or {}).get("percent")
                        for o in ("never_started", "started_and_left", "continued")
                    ]
                    cch = payload.get("ceilings_cannot_all_hold")
                    if (isinstance(cch, dict) and not _is_block_absence(cch)
                            and all(_num(x) for x in ceilings) and _num(cch.get("sum_percent"))):
                        c.sites += 1
                        if abs(sum(ceilings) - cch["sum_percent"]) > 5e-4:
                            c.failures.append(
                                f"{ppath}.ceilings_cannot_all_hold.sum_percent != the three "
                                f"ceilings summed"
                            )
                        if _num(cch.get("excess_pp")):
                            c.sites += 1
                            if abs((cch["sum_percent"] - 100) - cch["excess_pp"]) > 5e-4:
                                c.failures.append(
                                    f"{ppath}.ceilings_cannot_all_hold.excess_pp != "
                                    f"sum_percent - 100"
                                )
                for sname, snode in (payload.get("shares") or {}).items():
                    if not isinstance(snode, dict):
                        continue
                    num, den, val = (snode.get("numerator_pairs"),
                                     snode.get("denominator_pairs"),
                                     snode.get("value_percent"))
                    if _num(num) and _num(den) and _num(val) and den > 0:
                        c.sites += 1
                        if abs(100.0 * num / den - val) > 5e-4:
                            c.failures.append(
                                f"{ppath}.shares.{sname}: value_percent != "
                                f"100 * numerator / denominator"
                            )
    checks.append(c)

    # S13 -- the waterfall arithmetic. THE CHAINING CLAUSE IS THE ADDITION
    #        (reviewer-engineering F8): the old check asserted removed = n_in -
    #        n_out per position and that n_out never rose, and never asserted
    #        that position k's n_in equals position k-1's n_out -- which is
    #        where a waterfall actually breaks, because two positions can each
    #        be internally consistent and not be the same waterfall.
    c = Check(
        "S13",
        "waterfall positions are in the mandated order, chain (position k's n_in equals "
        "position k-1's n_out), are non-increasing (>=), and removed = n_in - n_out",
    )
    if is_placeholder:
        n = 0
        for arm in inst.get("arms", []):
            wf = arm.get("waterfall")
            if isinstance(wf, dict) and not _is_block_absence(wf):
                n += sum(len((w or {}).get("positions", [])) for w in wf.values()
                         if isinstance(w, dict))
        c.skipped_reason = (
            f"instance is a placeholder: position counts are sentinels, so neither the "
            f"chaining clause nor the arithmetic can be evaluated. {n} waterfall positions "
            f"would be checked on a real file. The order clause is exercised in "
            f"src/step8b_selftest.py against a de-sentinelled copy."
        )
    else:
        for i, arm in enumerate(inst.get("arms", [])):
            wf = arm.get("waterfall")
            if not isinstance(wf, dict) or _is_block_absence(wf):
                continue
            for pop, w in wf.items():
                if not isinstance(w, dict) or _is_block_absence(w):
                    continue
                prev_out = None
                for k, p in enumerate((w or {}).get("positions", [])):
                    c.sites += 1
                    where = f"$.arms[{i}].waterfall.{pop} position {p.get('position')}"
                    if p.get("position") != k + 1:
                        c.failures.append(
                            f"{where}: positions are out of the mandated order -- the final "
                            f"row set commutes but the per-filter sample sizes do not"
                        )
                    n_in, n_out = p.get("n_in"), p.get("n_out")
                    if isinstance(n_in, int) and isinstance(n_out, int):
                        if p.get("removed") != n_in - n_out:
                            c.failures.append(f"{where}: removed != n_in - n_out")
                        if prev_out is not None and n_in != prev_out:
                            c.failures.append(
                                f"{where}: n_in {n_in} != the previous position's n_out "
                                f"{prev_out} -- the waterfall does not chain"
                            )
                        if prev_out is not None and not (prev_out >= n_out):
                            c.failures.append(f"{where}: count increased")
                        prev_out = n_out
    checks.append(c)

    # S14 -- an inert filter position states that it is inert and why.
    c = Check("S14", "every waterfall position marked inert carries a reason")
    for i, arm in enumerate(inst.get("arms", [])):
        wf = arm.get("waterfall")
        if not isinstance(wf, dict) or _is_block_absence(wf):
            continue
        for pop, w in wf.items():
            if not isinstance(w, dict) or _is_block_absence(w):
                continue
            for p in (w or {}).get("positions", []):
                c.sites += 1
                if p.get("inert") is True and not p.get("inert_reason"):
                    c.failures.append(
                        f"$.arms[{i}].waterfall.{pop} position {p.get('position')}: "
                        f"inert with no reason"
                    )
    checks.append(c)

    # S15 -- D4 and D9 are published alongside and never folded into a bound.
    c = Check("S15", "D4 and D9 are marked published-alongside and not folded into any bound")
    cc = inst.get("channel_classes", {})
    # ARM FILES NO LONGER CARRY THIS BLOCK (decisions/0114 E8): it holds Step 8's
    # D4 and D9 figures, the merged document carries it once, and an arm file
    # states the absence. The check says which of the two it is looking at rather
    # than reporting a clean pass on a block that is not there.
    if _is_block_absence(cc) or _is_absence(cc):
        c.skipped_reason = (
            f"$.channel_classes is an ABSENCE RECORD here, with status "
            f"{cc.get('status')!r}: this is {_producing_step(inst)!r}'s file, the block holds "
            f"STEP 8's D4 and D9 figures, and it is filled ONCE in the merged document at "
            f"Step 13b (decisions/0114 E8). There is nothing to examine and the file says why."
        )
    else:
        for name in ("d4", "d9"):
            node = cc.get(name)
            if not isinstance(node, dict):
                c.failures.append(f"$.channel_classes.{name} is absent")
                continue
            c.sites += 1
            if node.get("folded_into_bound") is not False:
                c.failures.append(f"$.channel_classes.{name}: folded_into_bound is not false")
            if node.get("published_alongside") is not True:
                c.failures.append(f"$.channel_classes.{name}: published_alongside is not true")
    checks.append(c)

    # S16 -- every D9 quantity with both key forms publishes as a bound with no
    #        point estimate, and carries its coverage.
    c = Check("S16", "each D9 bounded quantity has floor, ceiling, no point estimate, and coverage")
    if _is_block_absence(cc) or _is_absence(cc):
        c.skipped_reason = (
            f"$.channel_classes is an absence record in {_producing_step(inst)!r}'s file "
            f"(decisions/0114 E8), so there are no D9 quantities here to examine; they are in "
            f"the merged document, where this check runs."
        )
    _d9_quantities = {}
    if isinstance(cc, dict) and not (_is_block_absence(cc) or _is_absence(cc)):
        _d9_quantities = ((cc.get("d9") or {}).get("quantities") or {})
    for qname, q in _d9_quantities.items():
        if not isinstance(q, dict):
            continue
        c.sites += 1
        for field in ("floor", "ceiling", "coverage"):
            if field not in q:
                c.failures.append(f"$.channel_classes.d9.quantities.{qname}: missing {field}")
        pe = q.get("point_estimate")
        if not isinstance(pe, dict) or "status" not in pe:
            c.failures.append(
                f"$.channel_classes.d9.quantities.{qname}: point_estimate is not an explicit "
                f"not-published record"
            )
    checks.append(c)

    # S17 -- cross-arm figures the spec forbids reconciling are held twice, AND
    #        an empty list is distinguished from an unsearched one. That second
    #        clause is reviewer-engineering's F4: this check used to fail a
    #        legitimately empty optional array as VACUOUS, which reads "no
    #        unreconciled divergence" as "looked nowhere" -- the inverse of
    #        CLAUDE.md's rule, which requires the control to distinguish them.
    #
    #        SCOPED AT v1.2.0 (decisions/0107, E1). This check applies ONLY where
    #        the file's producing step is the Human Lead's -- the merged document
    #        of task-sheet.md Step 13b. Before that it applied everywhere, and
    #        $.block_ownership already forbade an arm from writing the block: the
    #        arm was forbidden to write it and forbidden to omit it, and the only
    #        path to exit 0 was a cross-arm search an isolated instance cannot
    #        honestly have performed. AN ARM FILE THAT CORRECTLY OMITS THE BLOCK
    #        PASSES. An arm file that CARRIES it still fails, which is the half
    #        that must not be lost: skipping the requirement is not permitting
    #        the fabrication.
    c = Check(
        "S17",
        "in the MERGED document, figures reported-not-reconciled hold both arms' values and "
        "are flagged, and an empty list is accepted only with a search record and its "
        "coverage count; in an ARM FILE the block must be absent",
    )
    cad = inst.get("cross_arm_divergences")
    producing = _producing_step(inst)
    if not _is_merged_document(inst):
        # AN ARM FILE. The requirement is skipped; the prohibition is not.
        if cad is None:
            c.skipped_reason = (
                f"this file's producing step is {producing!r}, which is not the Human Lead's: "
                f"$.cross_arm_divergences belongs to the merged document (task-sheet.md Step "
                f"13b), an isolated arm is forbidden to compute it, and its ABSENCE here is "
                f"correct rather than a gap. Check S29 asserts that absence against the "
                f"ownership registry rather than leaving it assumed"
            )
        else:
            c.sites += 1
            c.failures.append(
                f"$.cross_arm_divergences is present in a file whose producing step is "
                f"{producing!r}: only the merged document may carry it, and an isolated arm "
                f"could not have performed the search it records"
            )
    elif cad is None:
        c.failures.append(
            "$.cross_arm_divergences is absent from the MERGED document: with no search "
            "record, an empty set of divergences cannot be told from a search nobody ran"
        )
        c.sites += 1
    elif not isinstance(cad, dict):
        c.failures.append(
            "$.cross_arm_divergences is not the {entries, search} form, so an empty list "
            "here cannot state whether anything was searched"
        )
        c.sites += 1
    else:
        search = cad.get("search") or {}
        entries = cad.get("entries")
        c.coverage = search.get("coverage_count")
        if not isinstance(entries, list):
            c.failures.append("$.cross_arm_divergences.entries is not a list")
            c.sites += 1
        elif not entries:
            if search.get("performed") is not True:
                c.failures.append(
                    "$.cross_arm_divergences: the list is empty and search.performed is not "
                    "true -- this is 'looked nowhere', not 'found nothing'"
                )
                c.sites += 1
            elif not isinstance(search.get("empty_reason"), str):
                c.failures.append(
                    "$.cross_arm_divergences: the list is empty and no empty_reason is given"
                )
                c.sites += 1
            else:
                c.declared_empty = (
                    f"no unreconciled divergence is recorded; the search was performed with "
                    f"coverage {search.get('coverage_count')}: {search.get('empty_reason')}"
                )
        for i, d in enumerate(entries or []):
            c.sites += 1
            for field in ("figure", "arm_a", "arm_b", "reconciled", "reason"):
                if field not in d:
                    c.failures.append(f"$.cross_arm_divergences.entries[{i}]: missing {field}")
            if d.get("reconciled") is not False:
                c.failures.append(
                    f"$.cross_arm_divergences.entries[{i}]: reconciled is not false"
                )
        if search.get("performed") is True and not isinstance(search.get("coverage_count"), int):
            c.failures.append(
                "$.cross_arm_divergences.search: performed with no coverage count -- a "
                "search that cannot say how much it examined is not distinguishable from "
                "one that examined nothing"
            )
    checks.append(c)

    # S18 -- every CI names the bootstrap settings that produced it, BY REFERENCE
    #        AND AT THE POINT OF USE. The ruling requires the seed, the resample
    #        count and the resampling unit at the point of use (decisions/0103),
    #        and a reference alone is not that.
    c = Check(
        "S18",
        "every confidence interval carries a bootstrap_ref AND states its B, seed, resampling "
        "unit and statistic at the point of use",
    )
    for path, node in _walk(inst):
        if isinstance(node, dict) and "lower" in node and "upper" in node and "level_pct" in node:
            c.sites += 1
            # `statistic` joined this list at v1.6.0 (decisions/0118): the ruling
            # says "every interval declares its statistic at the point of use",
            # and until the statistic was fixed this check did not ask for it.
            for field in ("bootstrap_ref", "B", "seed", "resampling_unit", "quantity_class",
                          "statistic"):
                if field not in node:
                    c.failures.append(f"{path}: confidence interval with no {field}")
    checks.append(c)

    # S19 -- every explicit absence record names a status and a reason.
    c = Check("S19", "every absence record states a status and a reason, so absent != inapplicable")
    for path, node in _walk(inst):
        if not (isinstance(node, dict) and "status" in node
                and node.get("status") in ABSENCE_STATUSES):
            continue
        c.sites += 1
        if not isinstance(node.get("reason"), str) or len(node["reason"]) < 20:
            c.failures.append(f"{path}: absence record with no usable reason")
    checks.append(c)

    # S20 -- a degenerate (zero-width) bound says so, so it cannot read as missing data.
    c = Check("S20", "a bound marked degenerate carries a reason; width is present either way")
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            bounds = payload.get("bounds") or {}
            if _is_block_absence(bounds):
                continue
            for bname, bnode in bounds.items():
                if not isinstance(bnode, dict) or "degenerate" not in bnode:
                    continue
                c.sites += 1
                if "width_pp" not in bnode:
                    c.failures.append(f"{ppath}.bounds.{bname}: no width_pp")
                if bnode["degenerate"] is True and not bnode.get("degenerate_reason"):
                    c.failures.append(
                        f"{ppath}.bounds.{bname}: degenerate with no reason"
                    )
    checks.append(c)

    # S21 -- placeholder branch coverage: every structural enum in the schema is
    #        exercised at least once, so Step 16 can be built against every shape.
    c = Check("S21", "placeholder exercises every structural enum branch the schema defines")
    if not is_placeholder:
        c.skipped_reason = "branch coverage is a property of the placeholder, not of a data file"
    else:
        # ROLE-RESTRICTED at v1.2.0 (decisions/0107). The document role is a
        # property of the whole file, so no single file can exhibit both roles'
        # branches: an arm file holds one arm and none of the merge-only blocks.
        # The restriction is NAMED rather than applied silently -- a restricted
        # pass that says nothing is indistinguishable from a full one.
        merged = _is_merged_document(inst)
        file_arm = (inst.get("document_scope") or {}).get("arm")
        file_step = _producing_step(inst)
        single_arm_file = not merged and STEP_DUALITY.get(file_step) == "single_arm"
        # The reachable branches depend on the file's ROLE and its PRODUCING
        # STEP, because one file per step per arm (decisions/0109 §1) decides
        # which blocks are in it at all. Each restriction is named below rather
        # than applied silently: a restricted pass that says nothing is
        # indistinguishable from a full one.
        # `awaiting_owner_step` LEFT THE REQUIRED SETS AT v1.4.0, and the reason
        # is named here rather than left to be noticed: the shape that used it is
        # gone. It labelled a per-arm block sitting in another step's file as an
        # absence naming its publisher, and under decisions/0111 E2 an arm entry
        # is ONE STEP'S measurement, so another step's block is not present at
        # all -- check S36 fails a file that carries one. The status stays in the
        # enum for a writer that is genuinely waiting on an owner step; no
        # placeholder exercises it, and that is stated in
        # $.known_limits_of_this_schema rather than passed over.
        # RESTRICTED BY PRODUCING STEP AS WELL AS BY ROLE, at v1.5.0. The
        # premiere-anchored arm and the superseded DERIV liveness series are
        # STEP 9's alone: Step 9 reports Netflix's 91-day window on a different
        # origin, and Step 13's W grid is finale-anchored at every one of its
        # eight arms. Requiring those branches of every dual arm file made a
        # STEP 13 arm file -- a shape the spec requires and this build can emit
        # -- fail S21 for holding exactly what the spec asks of it. Found by the
        # synthetic Step 13 arm file the ratification adds to the selftest.
        step9_only_shapes = merged or file_step == "step9"
        if merged:
            absence_needed = {"structurally_absent", "not_published",
                              "no_producer_in_spec", "superseded_for_this_purpose",
                              "not_required_by_spec", "not_a_dual_step"}
        elif single_arm_file:
            absence_needed = {"not_required_by_spec", "not_a_dual_step"}
        elif step9_only_shapes:
            absence_needed = {"structurally_absent", "not_published",
                              "no_producer_in_spec", "superseded_for_this_purpose"}
        else:
            absence_needed = {"structurally_absent", "not_published"}
        required_branches = {
            "clock_origin": {"s2_finale"} | ({"s2_premiere"} if step9_only_shapes else set()),
            "producing_arm": {"a", "b", "sole"} if merged else {file_arm},
            "population": {"APPLY", "DERIV"},
            "absence_status": absence_needed,
            "step_dual_status": ({"dual", "single_arm"} if merged
                                 else {"single_arm" if single_arm_file else "dual"}),
            "arms_in_this_file": {"one_arm", "both_arms"} if merged else {"one_arm"},
            "row_set": ({"position_5", "post_liveness"}
                        if merged or file_step == "step10" else set()),
            "stratum_kind": ({"all", "l2_stratum"}
                             if merged or file_step == "step10" else set()),
            # M10: the show branch is required, not merely permitted. The binding
            # cluster is NOT the same for every quantity, and a Step 16 built
            # only against `account` is built without the branch decisions/0103
            # §2 exists to protect.
            "resampling_unit": {"account", "show"},
            # RESTRICTED BY PUBLISHER at v1.5.0 (decisions/0114 E11). W is not
            # every step's to report: Steps 10, 11 and 12 do not vary it, so
            # requiring the window-W branch of their files is what made the
            # shipped single-arm placeholder attribute the window-W percentile to
            # `step11`. The branch is exercised where it is legal, and the other
            # files still exercise both RESAMPLING UNITS, which is the branch
            # decisions/0103 §2 exists to protect.
            "quantity_class": (
                {"outcome_shares", "window_w_percentile"}
                if merged or file_step in INTERVAL_CLASS_PUBLISHERS["window_w_percentile"]
                else {"outcome_shares"}
            ),
            "unit_disagreement": {"present"},
        }
        if not merged:
            c.notes.append(
                f"role-restricted: this is an ARM FILE, {file_step!r}'s output for arm "
                f"{file_arm!r}. Under ONE FILE PER STEP PER ARM (decisions/0109 §1) the "
                f"branches another arm or another step writes are not reachable in it and are "
                f"not required here: the required sets above are cut to what this file can "
                f"hold, and the branches cut out are exercised by the other placeholders, "
                f"which are validated in the same run. Branch coverage is a property of the "
                f"SET of placeholder files, not of any one of them."
            )
        observed = {k: set() for k in required_branches}
        observed["clock_origin"] = {a.get("clock_origin") for a in inst.get("arms", [])}
        for base, pop, block in _iter_payloads(inst):
            observed["population"].add(pop)
            bpa = block.get("by_producing_arm") or {}
            observed["step_dual_status"].add(bpa.get("step_dual_status"))
            observed["arms_in_this_file"].add(bpa.get("arms_in_this_file"))
            observed["producing_arm"] |= set((bpa.get("arms") or {}).keys())
        for _, pop, blk in _iter_abandonment(inst):
            observed["row_set"].add(blk.get("row_set"))
            for h in blk.get("histograms") or []:
                observed["stratum_kind"].add((h.get("stratum") or {}).get("kind"))
        for _, node in _walk(inst):
            if isinstance(node, dict) and node.get("status") in ABSENCE_STATUSES:
                observed["absence_status"].add(node["status"])
            if isinstance(node, dict) and "resampling_unit" in node:
                observed["resampling_unit"].add(node["resampling_unit"])
            if isinstance(node, dict) and "quantity_class" in node:
                observed["quantity_class"].add(node["quantity_class"])
            if isinstance(node, dict) and isinstance(node.get("unit_disagreement"), dict):
                observed["unit_disagreement"].add("present")
        for name, need in required_branches.items():
            c.sites += 1
            missing = need - (observed[name] - {None})
            if missing:
                c.failures.append(f"branch family {name!r} never exercises {sorted(missing)}")
        unexercised = set(ABSENCE_STATUSES) - observed["absence_status"]
        if unexercised:
            c.notes.append(
                f"absence statuses in the enum that this file does not exercise and that are "
                f"not required of it: {sorted(unexercised)}. A restricted pass that says "
                f"nothing is indistinguishable from a full one."
            )
    checks.append(c)

    # S22 -- a block absence is disciplined, and the primary headline arm has none.
    #        The absence branches exist because three of the four per-arm blocks
    #        have no producer at a non-primary arm (reviewer-engineering F1).
    #        They must not become a way to leave the adopted arm empty.
    c = Check(
        "S22",
        "every block absence names an owning step and a reason; the primary headline arm "
        "carries no absent block WHERE A PRODUCER EXISTS AT THAT ARM, and states an absence "
        "where none does; and ceilings are absent only where the bounds are",
    )
    for path, node in _walk(inst):
        if _is_block_absence(node):
            c.sites += 1
            if node.get("owning_step") is None:
                c.failures.append(f"{path}: block absence with no owning_step")
            if not isinstance(node.get("reason"), str) or len(node["reason"]) < 20:
                c.failures.append(f"{path}: block absence with no usable reason")
    # SCOPED BY PUBLISHER at v1.3.0, AND THE PUBLISHER TABLE MOVED OUT OF THE
    # FILE AT v1.4.0 (decisions/0111 E4). Until then `ownership_map` was read out
    # of the instance under test, so any arm file could exempt itself from this
    # check by editing one string in its own table -- and `d3_prime` and
    # `retained_by_air_period` had no other backstop. The table is now held in
    # this module, for the reason S31 already recorded about duality: A TABLE
    # READ FROM THE FILE UNDER TEST COULD ONLY AGREE WITH ITSELF. The file's own
    # table is still read, and is asserted AGAINST the external one below, so a
    # rewrite fails on the rewrite instead of escaping through it.
    #
    # SCOPED PER ENTRY at v1.4.0 as well: an arm entry is one step's measurement
    # at one setting (decisions/0111 E2), so the blocks required at the adopted
    # setting are the blocks THAT ENTRY'S producing step publishes -- not the
    # file's, which in the merged document is Step 13b's and publishes none.
    ownership_map = inst.get("block_ownership") or {}
    file_step = _producing_step(inst)
    merged_doc = _is_merged_document(inst)

    for name, external in sorted(BLOCK_PUBLISHER.items()):
        entry = ownership_map.get(f"arms[].{name}")
        if not isinstance(entry, dict):
            continue
        c.sites += 1
        claimed = entry.get("published_by_step")
        if claimed != external:
            c.failures.append(
                f"$.block_ownership.arms[].{name}.published_by_step is {claimed!r}; the spec "
                f"fixes {external!r}. A file that rewrites its own ownership table cannot "
                f"exempt itself: a table read from the file under test could only agree with "
                f"itself (decisions/0111 E4)"
            )

    for i, arm in enumerate(inst.get("arms", [])):
        if arm.get("is_primary_headline") is not True:
            continue
        entry_step = arm.get("producing_step")
        # PUBLISHER ROWS KEY ON ARM IDENTITY, NOT PRODUCING STEP ALONE
        # (decisions/0114 E13). BLOCK_PUBLISHER names the step; whether that step
        # produces the block AT THIS ARM is a second question, and reading only
        # the first made this check require a figure no step makes.
        has_producer = _block_has_producer(arm)
        for name in sorted(BLOCK_PUBLISHER):
            pub = BLOCK_PUBLISHER[name]
            if pub != entry_step:
                c.notes.append(
                    f"$.arms[{i}].{name}: not required here -- this entry is {entry_step!r}'s "
                    f"measurement and the block is published by {pub!r}, which writes its own "
                    f"entry and its own file under one file per step per arm"
                )
                continue
            c.sites += 1
            node = arm.get(name)
            if not has_producer:
                # ABSENCE STATED, NOT SILENCE. The record is still required; what
                # is not required is the figure. A missing key is silence and
                # still fails -- an empty result and a clean result are the same
                # value, and only the record says which.
                if node is None:
                    c.failures.append(
                        f"$.arms[{i}].{name}: MISSING at a "
                        f"{arm.get('clock_origin')!r}-anchored entry. No step in the spec "
                        f"produces this block there, so the FIGURE is not required -- but the "
                        f"RECORD is: absence stated, not silence (decisions/0114 E13)"
                    )
                elif not _is_block_absence(node):
                    c.notes.append(
                        f"$.arms[{i}].{name}: carried at a {arm.get('clock_origin')!r}-anchored "
                        f"entry, where the spec names no producer. Not a failure -- a writer "
                        f"that has a figure may publish it -- but it is recorded rather than "
                        f"passed over"
                    )
                else:
                    c.notes.append(
                        f"$.arms[{i}].{name}: absence accepted at a "
                        f"{arm.get('clock_origin')!r}-anchored entry with status "
                        f"{node.get('status')!r}. This entry is the adopted setting for "
                        f"{entry_step!r} AND no step produces this block at this clock origin, "
                        f"so requiring the figure would require one to be invented "
                        f"(decisions/0114 E13)"
                    )
                continue
            if node is None:
                c.failures.append(
                    f"$.arms[{i}].{name}: MISSING on the adopted setting, where the spec names "
                    f"a producer and this entry's own step ({entry_step!r}) publishes it"
                )
            elif _is_block_absence(node):
                c.failures.append(
                    f"$.arms[{i}].{name}: absent on the adopted setting, where the spec "
                    f"does name a producer and this entry's own step ({entry_step!r}) "
                    f"publishes it"
                )
            elif isinstance(node, dict):
                for pop, sub in node.items():
                    if _is_block_absence(sub) and name != "liveness_exclusions":
                        c.failures.append(
                            f"$.arms[{i}].{name}.{pop}: absent on the adopted setting"
                        )
    for base, pop, block in _iter_payloads(inst):
        for ppath, arm_key, payload in _iter_arm_payloads(block, base):
            c.sites += 1
            b_absent = _is_block_absence(payload.get("bounds"))
            ch_absent = _is_block_absence(payload.get("ceilings_cannot_all_hold"))
            if b_absent != ch_absent:
                c.failures.append(
                    f"{ppath}: bounds and ceilings_cannot_all_hold disagree on absence -- "
                    f"the three-ceiling sum is a function of the three ceilings"
                )
    checks.append(c)

    # S23 -- the bootstrap settings restated at the point of use match the registry
    #        they reference. The ruling requires them at the point of use; this is
    #        what stops the restatement drifting from what it restates.
    c = Check(
        "S23",
        "every interval's inline B, seed and resampling unit equal the registry entry it "
        "references, and its statistic is one the entry declares",
    )
    registry = inst.get("bootstrap_settings", {})
    for path, node in _walk(inst):
        if not (isinstance(node, dict) and "lower" in node and "upper" in node
                and "bootstrap_ref" in node):
            continue
        entry = registry.get(node["bootstrap_ref"])
        if not isinstance(entry, dict):
            continue
        c.sites += 1
        for field in ("B", "seed", "resampling_unit"):
            if field in node and field in entry and node[field] != entry[field]:
                c.failures.append(
                    f"{path}: inline {field} {node[field]!r} != registry "
                    f"{entry[field]!r} at $.bootstrap_settings.{node['bootstrap_ref']}"
                )
        # THE STATISTIC IS COMPARED BY MEMBERSHIP, NOT BY EQUALITY (v1.6.0,
        # decisions/0118). It was an equality until v1.5.0, when the registry
        # held ONE statistic per arm and the arms differed on it. The registry now
        # holds BOTH objects and an interval is one of them, so equality would be
        # a type error and the relation that carries the meaning is: the object
        # this interval reports is one the referenced bootstrap actually produced.
        if "statistic" in node and isinstance(entry.get("statistics"), list):
            if node["statistic"] not in entry["statistics"]:
                c.failures.append(
                    f"{path}: inline statistic {node['statistic']!r} is not among the "
                    f"statistics {entry['statistics']!r} declared at "
                    f"$.bootstrap_settings.{node['bootstrap_ref']}"
                )
        elif "statistic" in node and "statistics" not in entry:
            c.failures.append(
                f"$.bootstrap_settings.{node['bootstrap_ref']}: no `statistics` list, so "
                f"{path}'s statistic {node['statistic']!r} is restated against nothing. The "
                f"entry field was RENAMED from `statistic` to `statistics` at v1.6.0 "
                f"(decisions/0118) because it now holds both objects rather than an arm's "
                f"choice of one"
            )
    checks.append(c)

    # S24 -- a quantity's resampling unit is the binding cluster the record states
    #        for its class, or the disagreement is recorded and not reconciled.
    #        THE BINDING CLUSTER IS NOT THE SAME FOR EVERY QUANTITY: the outcome
    #        shares cluster by account and W's interval is show-clustered, so
    #        account level would understate a show-bound quantity (decisions/0103
    #        §2). This is what stops one inheriting `account` silently.
    c = Check(
        "S24",
        "every interval's resampling unit is the binding cluster declared for its quantity "
        "class, or carries an unreconciled disagreement record",
    )
    clusters = inst.get("binding_clusters", {})
    for path, node in _walk(inst):
        if not (isinstance(node, dict) and "lower" in node and "upper" in node
                and "resampling_unit" in node):
            continue
        c.sites += 1
        qclass = node.get("quantity_class")
        declared = clusters.get(qclass)
        if not isinstance(declared, dict):
            c.failures.append(
                f"{path}: quantity_class {qclass!r} has no entry in $.binding_clusters, so "
                f"the unit used cannot be checked against a binding cluster"
            )
            continue
        binding = declared.get("binding_cluster")
        if node["resampling_unit"] != binding:
            dis = node.get("unit_disagreement")
            if not isinstance(dis, dict) or dis.get("reported_not_reconciled") is not True:
                c.failures.append(
                    f"{path}: resamples by {node['resampling_unit']!r} while the binding "
                    f"cluster for {qclass!r} is {binding!r}, with no unreconciled "
                    f"disagreement record"
                )
    checks.append(c)

    # S25 -- every abandonment block names its row set, and no two blocks in one
    #        population name the same one (reviewer-engineering F2).
    c = Check(
        "S25",
        "every abandonment block names its row set and its population, and the row sets "
        "within one population are distinct",
    )
    seen_rowsets: dict[tuple, str] = {}
    for path, pop, blk in _iter_abandonment(inst):
        c.sites += 1
        if blk.get("population") != pop:
            c.failures.append(
                f"{path}: population {blk.get('population')!r} != the key it sits under {pop!r}"
            )
        rs = blk.get("row_set")
        if rs is None:
            c.failures.append(f"{path}: no row_set, so the figures name no row set")
            continue
        key = (path.rsplit("[", 1)[0], pop, rs)
        if key in seen_rowsets:
            c.failures.append(
                f"{path}: row set {rs!r} repeats one already at {seen_rowsets[key]}"
            )
        seen_rowsets[key] = path
    checks.append(c)

    # S26 -- histogram bins are well formed, per stratum (reviewer-engineering F7).
    c = Check(
        "S26",
        "every histogram has one more bin edge than count, ascending edges, and a distinct "
        "stratum label within its block",
    )
    for path, pop, blk in _iter_abandonment(inst):
        labels = set()
        for j, h in enumerate(blk.get("histograms") or []):
            c.sites += 1
            edges, counts = h.get("bin_edges_p"), h.get("counts")
            if not isinstance(edges, list) or not isinstance(counts, list):
                c.failures.append(f"{path}.histograms[{j}]: edges or counts is not a list")
                continue
            if len(edges) != len(counts) + 1:
                c.failures.append(
                    f"{path}.histograms[{j}]: {len(edges)} edges for {len(counts)} counts"
                )
            if any(b <= a for a, b in zip(edges, edges[1:])):
                c.failures.append(f"{path}.histograms[{j}]: bin edges are not ascending")
            label = (h.get("stratum") or {}).get("label")
            if label in labels:
                c.failures.append(
                    f"{path}.histograms[{j}]: stratum label {label!r} repeats in this block"
                )
            labels.add(label)
    checks.append(c)

    # S27 -- every top-level block present in the file has a declared owner
    #        (reviewer-engineering F9), and the two blocks Step 9 is forbidden to
    #        compute say so where they are written.
    c = Check(
        "S27",
        "every top-level block has an ownership entry; D4 and D9 are marked copied from "
        "Step 8 rather than computed here",
    )
    ownership = inst.get("block_ownership")
    if not isinstance(ownership, dict):
        c.sites += 1
        c.failures.append("$.block_ownership is absent: the blocks have no declared owners")
    else:
        for name in inst:
            if name in ("block_ownership",):
                continue
            c.sites += 1
            entry = ownership.get(name)
            if not isinstance(entry, dict):
                c.failures.append(
                    f"$.block_ownership: no entry for the top-level block {name!r}, so it is "
                    f"owned by whichever step writes the file first"
                )
                continue
            for field in ("owner_step", "owner_role", "write_mode", "may_first_writer_fill"):
                if field not in entry:
                    c.failures.append(f"$.block_ownership.{name}: missing {field}")
        cc2 = inst.get("channel_classes") or {}
        for name in ("d4", "d9"):
            node = cc2.get(name)
            if isinstance(node, dict):
                c.sites += 1
                if node.get("copied_not_computed") is not True or \
                        node.get("computed_by") != "step8":
                    c.failures.append(
                        f"$.channel_classes.{name}: not marked as copied from Step 8, which "
                        f"is the one thing Step 9 is forbidden to compute here"
                    )
    checks.append(c)

    # S28 -- THE TWO FACTS AGREE WITH EACH OTHER AND WITH THE FILE (decisions/0107
    #        §4). `step_dual_status` is a property of the STEP; `arms_in_this_file`
    #        is a property of THIS FILE; `arm_held` names which arm a one-arm file
    #        holds. Until v1.2.0 one field carried both, so `dual` required both
    #        arms and a dual step's arm file -- the file the ruling requires -- had
    #        no legal shape at all. The schema now permits it; this check is what
    #        stops the two facts drifting apart inside a file that validates.
    c = Check(
        "S28",
        "every block's step-duality, arms-in-this-file and arm_held agree with its arms keys "
        "and with $.document_scope; a single-arm step never holds two arms",
    )
    scope = inst.get("document_scope")
    if not isinstance(scope, dict):
        c.sites += 1
        c.failures.append(
            "$.document_scope is absent: the file does not say whether it is one arm's "
            "document or the merged one, so nothing can be checked against it"
        )
    else:
        merged = _is_merged_document(inst)
        file_arm = scope.get("arm")
        c.sites += 1
        if merged and file_arm is not None:
            c.failures.append(
                f"$.document_scope: the merged document names arm {file_arm!r}; it holds all "
                f"of them and names none"
            )
        if not merged and file_arm not in ("a", "b", "sole"):
            c.failures.append(
                f"$.document_scope: an arm file must NAME its arm; got {file_arm!r}"
            )
        if not merged:
            also = [s for s in (scope.get("also_written_by_steps") or [])
                    if s in HUMAN_LEAD_STEPS]
            if also:
                c.failures.append(
                    f"$.document_scope.also_written_by_steps names {also} in an ARM FILE: a "
                    f"Human Lead step writing into an arm file is the merge arriving through "
                    f"the side door, and the merge is a separate step on separate inputs"
                )
            # ONE FILE PER STEP PER ARM (decisions/0109 §1), the half that was
            # not checked: the file names ONE producing step, and every payload
            # in it belongs to that step. Until v1.3.0 the arm-file placeholder
            # named two extra writers while the merged document listed seven
            # inputs -- the two files took opposite sides of the ambiguity the
            # ruling closed.
            c.sites += 1
            other = [s for s in (scope.get("also_written_by_steps") or [])]
            if other:
                c.failures.append(
                    f"$.document_scope.also_written_by_steps is {other} in an ARM FILE: "
                    f"granularity is ONE FILE PER STEP PER ARM, so an arm file has exactly one "
                    f"producing step and this list is empty"
                )
            own_step = scope.get("producing_step")
            # EVERY container (decisions/0111 E1 widened the family from one to
            # six), and every ENTRY: an arm entry names its producing step since
            # v1.4.0, and in an arm file that step is the file's own.
            for family in ENTRY_FAMILIES:
                for i, entry in enumerate(inst.get(family) or []):
                    if not isinstance(entry, dict) or "producing_step" not in entry:
                        continue
                    c.sites += 1
                    if entry["producing_step"] != own_step:
                        c.failures.append(
                            f"$.{family}[{i}].producing_step is {entry['producing_step']!r} in "
                            f"{own_step!r}'s file -- one file per step per arm, so another "
                            f"step's measurement arrives in its own file and is merged at "
                            f"Step 13b"
                        )
            for base, bpa in _iter_containers(inst):
                if bpa.get("producing_step") not in (None, own_step):
                    c.sites += 1
                    c.failures.append(
                        f"{base}: written by "
                        f"{bpa.get('producing_step')!r} in {own_step!r}'s file -- one file per "
                        f"step per arm, so another step's payload arrives in its own file and "
                        f"is merged at Step 13b"
                    )
                for akey, payload in (bpa.get("arms") or {}).items():
                    if not isinstance(payload, dict):
                        continue
                    if payload.get("written_by_step") not in (None, own_step):
                        c.sites += 1
                        c.failures.append(
                            f"{base}.arms.{akey}: written_by_step is "
                            f"{payload.get('written_by_step')!r} in {own_step!r}'s file"
                        )
        for base, pop, block in _iter_payloads(inst):
            if not isinstance(block.get("by_producing_arm"), dict):
                c.sites += 1
                c.failures.append(f"{base}: no by_producing_arm block")
        # EVERY per-arm container, not only the headline's: Step 13's six
        # non-headline outputs took the same container at v1.4.0 (decisions/0111
        # E1), and the two facts must agree in all of them.
        for path, bpa in _iter_containers(inst):
            c.sites += 1
            keys = set((bpa.get("arms") or {}).keys())
            dual = bpa.get("step_dual_status")
            held_fact = bpa.get("arms_in_this_file")
            held = bpa.get("arm_held")
            if held_fact == "one_arm":
                if len(keys) != 1:
                    c.failures.append(
                        f"{path}: arms_in_this_file is one_arm but the arms keys are "
                        f"{sorted(keys)}"
                    )
                elif held not in keys:
                    c.failures.append(
                        f"{path}: arm_held is {held!r} but the arm present is "
                        f"{sorted(keys)[0]!r} -- a one-arm block must NAME the arm it holds"
                    )
            elif held_fact == "both_arms":
                if keys != {"a", "b"}:
                    c.failures.append(
                        f"{path}: arms_in_this_file is both_arms but the arms keys are "
                        f"{sorted(keys)}"
                    )
                if held is not None:
                    c.failures.append(
                        f"{path}: arms_in_this_file is both_arms and arm_held is {held!r}; a "
                        f"single name could only contradict one of the two arms present"
                    )
            else:
                c.failures.append(f"{path}: arms_in_this_file is {held_fact!r}")
            if dual == "single_arm":
                # NOT loosened by the split: the mirror defect of the one it
                # fixes is a single-arm step's file claiming two arms.
                if held_fact != "one_arm" or keys != {"sole"}:
                    c.failures.append(
                        f"{path}: a single-arm step holds {sorted(keys)} as "
                        f"{held_fact!r} -- a single-arm step has one arm, under `sole`"
                    )
            elif dual == "dual":
                if keys & {"sole"}:
                    c.failures.append(f"{path}: a dual step holds a `sole` payload")
                if merged and held_fact != "both_arms":
                    c.failures.append(
                        f"{path}: the merged document holds {held_fact!r} of a DUAL step -- a "
                        f"merge that carries one arm of a dual step has dropped the other"
                    )
            else:
                c.failures.append(f"{path}: step_dual_status is {dual!r}")
            if not merged and held_fact == "one_arm" and held != file_arm:
                c.failures.append(
                    f"{path}: this block holds arm {held!r} in the file of arm {file_arm!r} -- "
                    f"one file per arm, and no arm writes into another arm's document"
                )
            for akey, payload in (bpa.get("arms") or {}).items():
                if isinstance(payload, dict) and not _is_absence(payload) \
                        and payload.get("producing_arm") != akey:
                    c.failures.append(
                        f"{path}.arms.{akey}: the payload says producing_arm "
                        f"{payload.get('producing_arm')!r}"
                    )
    checks.append(c)

    # S29 -- THE BLOCKS ONLY THE MERGE MAY FILL APPEAR ONLY IN THE MERGED DOCUMENT
    #        (task-sheet.md Step 13b; decisions/0107). This is what stops an arm
    #        file masquerading as a merged one, and it is the check that makes
    #        S17's skip safe: S17 no longer requires the block in an arm file, so
    #        something must assert that the arm file does not carry it.
    #        The set is read from $.block_ownership, not from a list in here, so a
    #        third such block is added by marking it in one place.
    c = Check(
        "S29",
        "blocks marked merged_document_only in $.block_ownership appear only in the merged "
        "document, and every Human-Lead-owned block is so marked",
    )
    ownership = inst.get("block_ownership")
    if not isinstance(ownership, dict):
        c.sites += 1
        c.failures.append("$.block_ownership is absent: nothing declares which blocks are "
                          "the merge's own")
    else:
        merged = _is_merged_document(inst)
        for name, entry in ownership.items():
            if not isinstance(entry, dict):
                continue
            owner = entry.get("owner_step")
            merge_only = entry.get("merged_document_only")
            if owner in HUMAN_LEAD_STEPS:
                c.sites += 1
                if merge_only is not True:
                    c.failures.append(
                        f"$.block_ownership.{name}: owned by {owner!r} but not marked "
                        f"merged_document_only -- a Human-Lead block an arm file may carry is "
                        f"a block an arm may fabricate"
                    )
            if merge_only is True:
                c.sites += 1
                present = _ownership_path_present(inst, name)
                if not merged and present:
                    c.failures.append(
                        f"$.{name}: present in an arm file. It is filled only by the merged "
                        f"document, so an arm file carrying it is an arm file masquerading as "
                        f"a merged one"
                    )
                if merged and not present:
                    c.failures.append(
                        f"$.{name}: the merged document must carry the blocks only it may "
                        f"fill; this one is absent"
                    )
        if c.sites == 0:
            c.failures.append(
                "$.block_ownership names no merged_document_only block and no Human-Lead "
                "owner, so this check examined nothing: it found nothing because it looked "
                "nowhere"
            )
            c.sites += 1
    checks.append(c)

    # S30 -- THE MERGED DOCUMENT HOLDS TWO ARMS, NOT ONE ARM TWICE.
    #        reviewer-engineering M1, and it is the finding that would corrupt a
    #        PUBLISHED FIGURE rather than block a step: a merged document
    #        assembled from ONE arm file -- the payload deep-copied into the
    #        other arm's slot and relabelled -- validated clean and published, in
    #        $.cross_arm_divergences, that the arms agreed everywhere. A FALSE
    #        CLEAN in the block whose whole purpose is to report where they did
    #        not. It did not exist before v1.2.0; the arm/merged split created it.
    #
    #        ISOLATION IS UNOBSERVABLE, BUT ARITY IS OBSERVABLE. Four independent
    #        legs, each of which a copy-and-relabel trips:
    #          (a) every payload names the input FILE it came from, and a block
    #              holding two arms names two DIFFERENT files;
    #          (b) the two arms' sampling-width convention labels differ -- they
    #              are named inputs the spec forbids reconciling, so one label on
    #              both arms is a reconciliation on its face;
    #          (c) the diff record names two files per dual pair, compares a
    #              non-zero number of figures, and its divergence count equals
    #              the number of entries published;
    #          (d) in an ARM FILE no payload may claim to have been merged from
    #              anything, so the check runs there too rather than reporting
    #              N/A on two thirds of the files.
    c = Check(
        "S30",
        "a merged document's two arms come from two named input files, use two convention "
        "labels and carry a diff record with force; an arm file claims no merge provenance",
    )
    scope = inst.get("document_scope") or {}
    merged = _is_merged_document(inst)
    if not merged:
        # EVERY container, not only the headline's: decisions/0111 E1 gave five
        # more blocks the same shape, and a leg that walked one of six would have
        # been an arity check with five blind spots.
        for base, bpa in _iter_containers(inst):
            for akey, payload in (bpa.get("arms") or {}).items():
                if not isinstance(payload, dict) or _is_absence(payload):
                    continue
                c.sites += 1
                if "merged_from" in payload:
                    c.failures.append(
                        f"{base}.arms.{akey}: an ARM FILE carries merged_from -- it was "
                        f"written by an isolated instance and merged from nothing"
                    )
        for i, entry in enumerate(inst.get("declared_intervals") or []):
            c.sites += 1
            if "merged_from" in entry:
                c.failures.append(
                    f"$.declared_intervals[{i}]: an ARM FILE carries merged_from"
                )
    else:
        merge = scope.get("merge") or {}
        # RENAMED FROM `arm_files_merged` AT v1.4.0 (decisions/0111 E6): the
        # input list records SOURCES, not only arm files, and Step 14's limits
        # section is a named non-arm-file source with no arm.
        inputs = merge.get("sources_merged")
        labels: dict[str, tuple] = {}
        non_arm_labels: dict[str, list] = {}
        if not isinstance(inputs, list) or not inputs:
            c.sites += 1
            c.failures.append(
                "$.document_scope.merge.sources_merged is absent or empty: a merged "
                "document that does not name its inputs cannot be told from an arm file that "
                "grew an extra arm"
            )
        else:
            for j, entry in enumerate(inputs):
                c.sites += 1
                if not isinstance(entry, dict):
                    c.failures.append(
                        f"$.document_scope.merge.sources_merged[{j}] is not an object "
                        f"naming its step and arm"
                    )
                    continue
                label = entry.get("file_label")
                if label in labels:
                    c.failures.append(
                        f"$.document_scope.merge.sources_merged[{j}]: the label {label!r} "
                        f"is already used by another input -- two inputs are two files"
                    )
                labels[label] = (entry.get("producing_step"), entry.get("arm"))
                if entry.get("source_kind") == "non_arm_file":
                    non_arm_labels[label] = entry.get("fills_blocks") or []
        # (a) and (b), per block -- over EVERY per-arm container (decisions/0111
        # E1 widened the family from one to six, and a copy of arm a's D3' into
        # arm b's slot is the same forgery as a copy of its headline).
        for base, bpa in _iter_containers(inst):
            seen_from: dict[str, str] = {}
            seen_conv: dict[str, str] = {}
            for akey, payload in (bpa.get("arms") or {}).items():
                if not isinstance(payload, dict) or _is_absence(payload):
                    continue
                ppath = f"{base}.arms.{akey}"
                c.sites += 1
                src = payload.get("merged_from")
                if src is None:
                    c.failures.append(
                        f"{ppath}: no merged_from -- the merged document must name the input "
                        f"file each payload came from, or a payload copied from the other "
                        f"arm's file is indistinguishable from one that was not"
                    )
                elif src not in labels:
                    c.failures.append(
                        f"{ppath}: merged_from {src!r} is not one of the declared input files"
                    )
                else:
                    step_of, arm_of = labels[src]
                    if arm_of != akey:
                        c.failures.append(
                            f"{ppath}: merged_from names the arm {arm_of!r} file, but this "
                            f"payload sits under arms.{akey}"
                        )
                    if payload.get("written_by_step") not in (None, step_of):
                        c.failures.append(
                            f"{ppath}: written by {payload.get('written_by_step')!r} but "
                            f"merged from {step_of!r}'s file"
                        )
                    if src in seen_from:
                        c.failures.append(
                            f"{ppath}: merged from the SAME file as {seen_from[src]} -- two "
                            f"arms are two files, and one arm file cannot supply both arms of "
                            f"a dual step"
                        )
                    seen_from[src] = ppath
                ratios = payload.get("bound_over_sampling_width_ratios")
                if isinstance(ratios, dict) and not _is_absence(ratios):
                    for rname, rnode in ratios.items():
                        if not isinstance(rnode, dict):
                            continue
                        label = rnode.get("convention_label")
                        key = f"{rname}::{label}"
                        c.sites += 1
                        if key in seen_conv:
                            c.failures.append(
                                f"{ppath}.bound_over_sampling_width_ratios.{rname}: the "
                                f"convention label {label!r} is already used by "
                                f"{seen_conv[key]} -- the two arms' sampling-width conventions "
                                f"are NAMED INPUTS the spec forbids reconciling, so one label "
                                f"on both arms is either a reconciliation or a copy"
                            )
                        seen_conv[key] = ppath
        # (e) INPUT -> PAYLOAD, THE DIRECTION THAT WAS NEVER READ (decisions/0111
        #     E3b). Every leg above walks payload -> input: it asks whether each
        #     payload names a declared source. NOTHING ASKED WHETHER EACH
        #     DECLARED SOURCE IS NAMED BY A PAYLOAD, so A MERGE DROPPING AN
        #     ENTIRE DECLARED INPUT VALIDATED CLEAN -- M1 inverted. One file
        #     supplying two arms was caught; one file supplying nothing was not,
        #     and it needs no forgery, only an omission. The shipped placeholder
        #     was occupied by exactly that: two of its seven declared inputs were
        #     named by no payload at all.
        #     AND IT PROVED MENTION, NOT CONTRIBUTION, until v1.5.0
        #     (decisions/0114, E9/E15). `named` walked EVERY node carrying a
        #     `merged_from` string, so a single `$.declared_intervals` entry --
        #     which is a reference to a file, not a payload from it -- satisfied
        #     an arm-file source that had supplied nothing at all. The two are
        #     counted separately now: a mention keeps its own tally and does not
        #     discharge the requirement.
        named: dict[str, int] = {}
        mentioned: dict[str, int] = {}
        for path, node in _walk(inst):
            if not (isinstance(node, dict) and isinstance(node.get("merged_from"), str)):
                continue
            if path.startswith("$.declared_intervals"):
                mentioned[node["merged_from"]] = mentioned.get(node["merged_from"], 0) + 1
            else:
                named[node["merged_from"]] = named.get(node["merged_from"], 0) + 1
        for label, (step_of, arm_of) in labels.items():
            c.sites += 1
            if label not in named:
                only_mentioned = (
                    f" It IS named by {mentioned[label]} $.declared_intervals entr"
                    f"{'y' if mentioned[label] == 1 else 'ies'}, and that is a MENTION, not a "
                    f"CONTRIBUTION: an interval entry references a file, it is not a payload "
                    f"from one (decisions/0114 E9/E15)." if label in mentioned else ""
                )
                c.failures.append(
                    f"$.document_scope.merge.sources_merged: the source ({step_of!r}, "
                    f"{arm_of!r}) is declared as an input and NO payload names it in "
                    f"merged_from -- a merge that drops an entire declared input is the "
                    f"inverse of the one this check was written for, and it needs no forgery, "
                    f"only an omission.{only_mentioned}"
                )
        # (f) THE EXTERNAL ANCHOR (decisions/0114, E9/E15). Every leg above reads
        #     the declared list against the file's own payloads, so the two close
        #     against each other and A MERGE DECLARING FIVE OF EIGHT SOURCES
        #     VALIDATED CLEAN: drop three sources and the payloads they supplied,
        #     and nothing in the file contradicts anything else in it. The
        #     expected set is DERIVED FROM STEP_DUALITY, which already held the
        #     material -- dual steps contribute two arms, single-arm steps one --
        #     plus the non-arm-file sources the spec names. Same reasoning as S31
        #     and as S22's publisher table: A TABLE READ FROM THE FILE UNDER TEST
        #     COULD ONLY AGREE WITH ITSELF.
        expected_sources = _expected_merge_sources()
        declared_pairs = {}
        for entry in (inputs if isinstance(inputs, list) else []):
            if isinstance(entry, dict):
                declared_pairs[(entry.get("producing_step"), entry.get("arm"))] = entry
        for key, kind in sorted(expected_sources.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
            step_of, arm_of = key
            c.sites += 1
            entry = declared_pairs.get(key)
            if entry is None:
                c.failures.append(
                    f"$.document_scope.merge.sources_merged: the source ({step_of!r}, "
                    f"{arm_of!r}) is EXPECTED and is not declared. The expected set is derived "
                    f"from the duality the spec fixes plus the named non-arm-file sources "
                    f"({len(expected_sources)} in all), not read from this file -- a merge that "
                    f"declares a subset and drops the matching payloads closes against itself "
                    f"and would otherwise validate clean (decisions/0114 E9/E15)"
                )
            elif entry.get("source_kind") != kind:
                c.failures.append(
                    f"$.document_scope.merge.sources_merged: the source ({step_of!r}, "
                    f"{arm_of!r}) declares source_kind {entry.get('source_kind')!r}; the spec "
                    f"makes it {kind!r}"
                )
        for key, entry in sorted(declared_pairs.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            if key in expected_sources:
                continue
            c.sites += 1
            if entry.get("source_kind") == "arm_file":
                c.failures.append(
                    f"$.document_scope.merge.sources_merged: ({key[0]!r}, {key[1]!r}) is "
                    f"declared as an ARM FILE and is not one of the seven the spec fixes "
                    f"(decisions/0109 §1, one file per step per arm)"
                )
            else:
                c.notes.append(
                    f"$.document_scope.merge.sources_merged: ({key[0]!r}, {key[1]!r}) is an "
                    f"undeclared-in-spec NON-ARM-FILE source. Permitted -- the input list "
                    f"records SOURCES (decisions/0111 E6) -- and recorded here rather than "
                    f"passed over; its blocks are checked below like any other"
                )
        # A non-arm-file source names the blocks it fills, and those blocks are
        # where its provenance has to appear: its payloads are not per-arm, so no
        # walk of the arm keys would ever reach them.
        for label, blocks in non_arm_labels.items():
            for block in blocks:
                c.sites += 1
                node = inst.get(block)
                # A NON-ARM SOURCE MAY FILL A LIST OR AN OBJECT (v1.5.0). Step
                # 14's limits section fills a list; Step 8's artifact fills
                # `channel_classes`, which is one object, and a leg that only
                # understood lists would have reported it absent.
                if isinstance(node, dict) and not _is_block_absence(node):
                    if node.get("merged_from") != label:
                        c.failures.append(
                            f"$.{block}: declared as filled by the non-arm-file source "
                            f"{label!r} and does not name it in merged_from -- a block cannot "
                            f"arrive in the reader-facing document with no recorded provenance "
                            f"(decisions/0111 E6)"
                        )
                    continue
                entries = node
                if not isinstance(entries, list) or not entries:
                    c.failures.append(
                        f"$.{block}: declared as filled by the non-arm-file source {label!r}, "
                        f"and absent or empty here"
                    )
                    continue
                unstamped = [k for k, e in enumerate(entries)
                             if not (isinstance(e, dict) and e.get("merged_from") == label)]
                if unstamped:
                    c.failures.append(
                        f"$.{block}: entries {unstamped[:5]} do not name the source that "
                        f"supplied them. A ten-item bias ledger that must not be netted cannot "
                        f"arrive in the reader-facing document with no recorded provenance "
                        f"(decisions/0111 E6)"
                    )
        # A declared interval is merged in from a file too, and names it.
        for i, entry in enumerate(inst.get("declared_intervals") or []):
            c.sites += 1
            src = entry.get("merged_from")
            if src is None:
                c.failures.append(
                    f"$.declared_intervals[{i}]: no merged_from in the merged document"
                )
            elif src not in labels:
                c.failures.append(
                    f"$.declared_intervals[{i}]: merged_from {src!r} is not a declared input"
                )
            elif labels[src] != (entry.get("produced_by_step"), entry.get("producing_arm")):
                c.failures.append(
                    f"$.declared_intervals[{i}]: merged_from names {labels[src]}, but the "
                    f"entry says {(entry.get('produced_by_step'), entry.get('producing_arm'))}"
                )
        # THE RESIDUAL, MEASURED AND REPORTED RATHER THAN ASSERTED AWAY. A
        # forgery that relabels the arm, the bootstrap refs, the convention
        # labels AND the merge provenance leaves two payloads that are identical
        # once those labels are normalised. That is not a failure -- two arms may
        # legitimately agree on every figure, and in a placeholder every
        # measurement is a sentinel, so identity is expected there. It is
        # reported, because it is the only signal left and a residual nobody
        # counts is a residual nobody sees.
        #
        # AND THE SIGNAL IS WEAKER THAN v1.3.0 PUBLISHED (decisions/0111 §4).
        # The keys normalised below do NOT include `convention_definition`
        # -- arm a's convention in arm a's own words -- and a forger making the
        # copy internally coherent rewrites that sentence anyway. THE MOMENT THEY
        # DO, THIS COUNT INVERTS TO 0 OF N, which is exactly what a GENUINE merge
        # of two differing arms produces. So the count separates nothing past
        # that rung, and the note below says so rather than implying a signal it
        # does not have.
        #
        # `statistic` LEFT THIS TUPLE AT v1.6.0 (decisions/0118). It was here
        # because it was an ARM LABEL -- arm a reported movements, arm b levels,
        # and normalising it away was right for a comparison meant to ignore
        # which arm a payload belongs to. The statistic is now fixed as BOTH for
        # every arm, so two payloads differing on it differ on WHICH OBJECT they
        # report, which is a real divergence and not a label. Normalising it
        # would hide exactly what the merged document exists to publish. FOUR
        # KEYS NOW, NOT FIVE -- and the arity below is DERIVED FROM THIS TUPLE
        # rather than restated. v1.6.0 dropped `statistic` from it and left the
        # word "five" typed into the sentence the check emits, which propagated
        # into the schema generator and from there into all three placeholders'
        # `known_limits_of_this_schema` (reviewer-engineering E3). A count typed
        # beside the list it counts is a second definition of the list.
        _ARM_LABELS = ARM_LABELS_NORMALISED

        def _normalise(node):
            if isinstance(node, dict):
                return {k: ("<arm-label>" if k in _ARM_LABELS else _normalise(v))
                        for k, v in node.items()}
            if isinstance(node, list):
                return [_normalise(v) for v in node]
            return node

        pairs = identical = 0
        for base, bpa in _iter_containers(inst):
            arms_map = bpa.get("arms") or {}
            a, b = arms_map.get("a"), arms_map.get("b")
            if not (isinstance(a, dict) and isinstance(b, dict)):
                continue
            pairs += 1
            if json.dumps(_normalise(a), sort_keys=True) == \
                    json.dumps(_normalise(b), sort_keys=True):
                identical += 1
        if pairs:
            c.notes.append(
                f"residual: {identical} of {pairs} two-arm payload pairs are byte-identical "
                f"once these {ARM_LABELS_ARITY_WORD} keys are normalised: "
                f"{', '.join(_ARM_LABELS)}. This is NOT a "
                f"failure -- the arms may agree on every figure, and in a placeholder every "
                f"measurement is a sentinel so identity is expected. AND IT IS NOT A SIGNAL "
                f"EITHER, PAST ONE MORE RUNG: `convention_definition` is NOT normalised, a "
                f"forger making the copy internally coherent rewrites that sentence anyway, "
                f"and the moment they do this count reads 0 of {pairs} -- which is what a "
                f"genuine merge produces. S30 raises the cost of a false merge to a fabricated "
                f"input file PLUS ONE REWRITTEN SENTENCE, and past that there is no in-file "
                f"signal at all. THE HUMAN LEAD'S DIFF REMAINS THE CONTROL past that rung."
            )
        # (c) the diff record.
        diff = merge.get("diff")
        if not isinstance(diff, dict):
            c.sites += 1
            c.failures.append(
                "$.document_scope.merge.diff is absent: the retired "
                "`diff_precedes_merge: true` was a sentence the file contained, and what "
                "replaces it is a record with content"
            )
        else:
            dual_steps = sorted({
                (block.get("by_producing_arm") or {}).get("producing_step")
                for _, _, block in _iter_payloads(inst)
                if (block.get("by_producing_arm") or {}).get("step_dual_status") == "dual"
            } - {None})
            paired = {p.get("producing_step"): p for p in (diff.get("pairs_diffed") or [])
                      if isinstance(p, dict)}
            for step in dual_steps:
                c.sites += 1
                pair = paired.get(step)
                if pair is None:
                    c.failures.append(
                        f"$.document_scope.merge.diff.pairs_diffed: no pair for the DUAL step "
                        f"{step!r}, whose two arms this document carries"
                    )
                    continue
                fa, fb = pair.get("arm_a_file"), pair.get("arm_b_file")
                if fa == fb:
                    c.failures.append(
                        f"$.document_scope.merge.diff.pairs_diffed[{step}]: both sides name "
                        f"the same file -- a file diffed against itself is not a diff"
                    )
                for side, f in (("arm_a_file", fa), ("arm_b_file", fb)):
                    if f not in labels:
                        c.failures.append(
                            f"$.document_scope.merge.diff.pairs_diffed[{step}].{side}: {f!r} "
                            f"is not one of the declared input files"
                        )
            compared = diff.get("figures_compared")
            found = diff.get("divergences_found")
            entries = ((inst.get("cross_arm_divergences") or {}).get("entries")) or []
            if isinstance(compared, int) and compared != SENTINEL_COUNT:
                c.sites += 1
                if compared <= 0:
                    c.failures.append(
                        "$.document_scope.merge.diff.figures_compared is 0: a diff that "
                        "compared nothing and a diff that found nothing are the same value"
                    )
                if isinstance(found, int) and found != SENTINEL_COUNT \
                        and found != len(entries):
                    c.failures.append(
                        f"$.document_scope.merge.diff.divergences_found is {found} while "
                        f"$.cross_arm_divergences.entries holds {len(entries)}"
                    )
            else:
                c.notes.append(
                    "the diff's arithmetic clause is not applicable to a placeholder: "
                    "figures_compared and divergences_found are sentinels here, and the "
                    "clause is exercised against a de-sentinelled copy by src/step8b_selftest.py"
                )
    checks.append(c)

    # S31 -- DUALITY IS READ AGAINST THE STEP (reviewer-engineering M2). Until
    #        v1.3.0 `step_dual_status` was never compared with `producing_step`,
    #        which sits two keys away in the same object, so a Step 9 block could
    #        DECLARE itself single_arm and validate -- and in the merged document
    #        the dropped-arm clause is guarded on `dual` and would never fire.
    #        The loosening the split forbade was reachable by RELABELLING rather
    #        than by widening, and the existing selftest case mutated SHAPE,
    #        which is the half the split already guarded.
    c = Check(
        "S31",
        "every block's step_dual_status equals the duality the spec fixes for its "
        "producing_step, and $.step_duality states that map rather than restating a choice",
    )
    registry = inst.get("step_duality")
    if not isinstance(registry, dict):
        c.sites += 1
        c.failures.append(
            "$.step_duality is absent: nothing in the file states which steps are dual, so a "
            "block's own declaration is the only claim there is"
        )
    else:
        for step, expected in STEP_DUALITY.items():
            c.sites += 1
            entry = registry.get(step)
            if not isinstance(entry, dict):
                c.failures.append(f"$.step_duality: no entry for {step!r}")
            elif entry.get("dual_status") != expected:
                c.failures.append(
                    f"$.step_duality.{step}.dual_status is "
                    f"{entry.get('dual_status')!r}; the spec fixes {expected!r}"
                )
    # EVERY container, not only the headline's (decisions/0111 E1 gave five more
    # blocks the same shape, and a relabelling check that walks one of six is a
    # check with five blind spots).
    for base, bpa in _iter_containers(inst):
        step = bpa.get("producing_step")
        expected = STEP_DUALITY.get(step)
        if expected is None:
            continue
        c.sites += 1
        if bpa.get("step_dual_status") != expected:
            c.failures.append(
                f"{base}: producing_step {step!r} is {expected!r} in the "
                f"spec, but this block declares {bpa.get('step_dual_status')!r} -- duality is "
                f"a fixed fact of the spec, not a label a block picks, and a dual step that "
                f"relabels itself single_arm disarms the clause that catches a dropped arm"
            )
    checks.append(c)

    # S32 -- AN INTERVAL REFERENCES ITS OWN ARM'S SETTINGS (reviewer-engineering
    #        M6). Nothing checked that a CI's bootstrap_ref belonged to the arm
    #        that produced the payload, so in the merged document arm a's
    #        interval could point at `b_default` and pass S3, S23 and S24 in
    #        silence.
    #
    #        WHAT THIS CHECK NOW CATCHES IS NARROWER THAN WHAT IT USED TO CATCH,
    #        and the narrowing is a CONSEQUENCE OF decisions/0118 rather than a
    #        weakening of the code. Its original ground was that the arms' entries
    #        differed on the one field the spec did not fix, so a wrong reference
    #        misreported WHICH STATISTIC produced a published interval. All four
    #        elements are now fixed and identical across the arms, so two default
    #        entries differ ONLY in `producing_arm`: a cross-arm reference now
    #        misreports the ARM and misreports no setting, because there is no
    #        differing setting left to misreport. The check keeps its force on
    #        attribution -- which is what the merged document's diff rests on --
    #        and the ruling has removed one observable difference between the arms.
    #        Reported rather than left to be inferred from a passing check.
    #
    #        AND WHAT IT CATCHES IS AN INCOHERENT REFERENCE, NOT A MISLABEL
    #        (reviewer-engineering, v1.6.0 review; this arm agrees). decisions/0119
    #        §5 wrote "S32 catches an arm MISLABEL", which is one notch too strong:
    #        BOTH sides of this comparison are the writer's own declarations -- the
    #        arm a payload sits under, and the arm the referenced entry says
    #        produced it -- so a writer that labels both with the same wrong arm is
    #        internally coherent and unobservable here. What fails is a payload
    #        under one arm pointing at another arm's entry. THE COHERENT MISLABEL
    #        IS THE HUMAN LEAD'S DIFF TO CATCH, and it is published as a limit
    #        rather than left implied by a passing check.
    c = Check(
        "S32",
        "every interval references bootstrap settings produced by the arm that owns it",
    )
    registry = inst.get("bootstrap_settings") or {}
    for path, _step, arm, ci in _iter_cis_with_arm(inst):
        c.sites += 1
        ref = ci.get("bootstrap_ref")
        entry = registry.get(ref)
        if not isinstance(entry, dict):
            c.failures.append(f"{path}: bootstrap_ref {ref!r} is not in the registry")
            continue
        if arm is not None and entry.get("producing_arm") != arm:
            c.failures.append(
                f"{path}: this interval belongs to arm {arm!r} but references "
                f"$.bootstrap_settings.{ref}, which was produced by arm "
                f"{entry.get('producing_arm')!r}"
            )
    checks.append(c)

    # S33 -- A SEARCH THAT EXAMINED NOTHING IS NOT A SEARCH (reviewer-engineering
    #        M7). `coverage_count: 0` with `performed: true` still passed, which
    #        the schema's own prose called a finding -- a control asserted in a
    #        sentence and not built. The same rule reaches D9's coverage, where a
    #        zero floor beside zero examined records is indistinguishable from a
    #        check that looked nowhere.
    c = Check(
        "S33",
        "no search or coverage record claims to have been performed while reporting zero "
        "records examined",
    )
    for path, node in _walk(inst):
        if isinstance(node, dict) and "performed" in node and "coverage_count" in node:
            c.sites += 1
            if node.get("performed") is True and node.get("coverage_count") == 0:
                c.failures.append(
                    f"{path}: performed with coverage_count 0 -- an empty result and a clean "
                    f"result are the same value, and this one looked at nothing"
                )
    cc33 = inst.get("channel_classes") or {}
    cc33_absent = _is_block_absence(cc33) or _is_absence(cc33)
    d9 = {} if cc33_absent else ((cc33.get("d9") or {}).get("quantities") or {})
    if c.sites == 0 and cc33_absent:
        # SCOPE-EMPTY, AND IT SAYS SO. Both of this check's site families live in
        # the merged document: the cross-arm search record is merge-only, and D9's
        # coverage moved there with `channel_classes` (decisions/0114 E8). The
        # warrant is the EXTERNAL publisher table plus this file's own absence
        # record -- not silence.
        c.skipped_reason = (
            f"this file is {_producing_step(inst)!r}'s and carries neither site family: the "
            f"cross-arm search record belongs to the merged document, and D9's coverage sits "
            f"inside $.channel_classes, which this file records as absent with status "
            f"{cc33.get('status')!r} because the block is published by "
            f"{TOP_LEVEL_PUBLISHER.get('channel_classes')!r} (decisions/0114 E8). Both halves "
            f"run on the merged document, which is validated in the same run."
        )
    for qname, q in d9.items():
        cov = (q or {}).get("coverage") or {}
        if "records_examined" not in cov:
            continue
        c.sites += 1
        examined = cov.get("records_examined")
        floor = ((q.get("floor") or {}).get("value"))
        if examined == 0 and isinstance(floor, int) and floor != SENTINEL_COUNT:
            c.failures.append(
                f"$.channel_classes.d9.quantities.{qname}: a bound is published on zero "
                f"records examined -- a zero floor is not an absence of evidence, and without "
                f"coverage it cannot be told from a check that looked nowhere"
            )
    checks.append(c)

    # S34 -- OWNERSHIP REACHES THE NESTED BLOCKS (reviewer-engineering M8). It
    #        stopped at depth 1, so `arms` -- one entry, owned by Step 9 -- hid
    #        Step 8's waterfall, Step 10's abandonment distribution and Step 13's
    #        D3' behind it. Every nested block the file actually carries must
    #        have an entry at its dotted path.
    c = Check(
        "S34",
        "every nested block the file carries has an ownership entry at its dotted path, and a "
        "block published by a step other than its owner names that step",
    )
    ownership = inst.get("block_ownership")
    if not isinstance(ownership, dict):
        c.sites += 1
        c.failures.append("$.block_ownership is absent: nothing owns the nested blocks either")
    else:
        scalar = (str, int, float, bool, type(None))

        def _is_block(value) -> bool:
            """A block is a container of fields, not a scalar or a list of them."""
            if isinstance(value, scalar):
                return False
            if isinstance(value, list):
                return any(not isinstance(v, scalar) for v in value)
            return True

        families = [("arms", inst.get("arms")), ("variants", inst.get("variants")),
                    ("subpopulation_cuts", inst.get("subpopulation_cuts"))]
        for family, entries in families:
            for entry in (entries or []):
                if not isinstance(entry, dict):
                    continue
                for key, value in entry.items():
                    if not _is_block(value):
                        continue
                    name = f"{family}[].{key}"
                    c.sites += 1
                    if not isinstance(ownership.get(name), dict):
                        c.failures.append(
                            f"$.block_ownership: no entry for {name}, so it is owned by "
                            f"whichever step writes its container"
                        )
        for key, value in (inst.get("channel_classes") or {}).items():
            if isinstance(value, dict):
                name = f"channel_classes.{key}"
                c.sites += 1
                if not isinstance(ownership.get(name), dict):
                    c.failures.append(f"$.block_ownership: no entry for {name}")
        # Every per-arm block names its PUBLISHER, whether or not that is its
        # owner. Check S22 reads this field to decide which absences are
        # legitimate in which file, and a field present only where it differs
        # from the owner would make S22 fall back to ownership silently.
        for name, entry in ownership.items():
            if not isinstance(entry, dict) or not name.startswith("arms[]."):
                continue
            c.sites += 1
            if entry.get("published_by_step") is None:
                c.failures.append(
                    f"$.block_ownership.{name}: no published_by_step. Under one file per step "
                    f"per arm, 'who owns this figure' and 'whose file does it arrive in' are "
                    f"two questions, and check S22 needs the second"
                )
    checks.append(c)

    # S35 -- THE CONSTRAINT decisions/0109 §4 RECORDS, MADE MACHINE-CHECKED.
    #        The `step_dual_status` rename fails LOUDLY only because
    #        `by_producing_arm` is not inside a oneOf: give anything above it an
    #        absence branch and a writer still emitting the old `dual_status` key
    #        stops failing against additionalProperties and instead produces a
    #        silent "matched 0 oneOf branches" at the parent. The ruling asks for
    #        this to be re-checked whenever an absence branch is added; a
    #        constraint that depends on someone remembering is not a control.
    #
    #        TWO CORRECTIONS AT v1.4.0.
    #        (1) THE ROOT-SIDE SCAN WAS DEAD CODE. It was handed a bare PROPERTY
    #            MAP -- {"arms": ..., "document_scope": ...} -- and _scan only
    #            recurses into schema KEYWORDS, so not one of those keys was
    #            followed and the call returned immediately. Verified before
    #            fixing: none of the root property names is a keyword. The $defs
    #            side still reached every reference, because every reference to
    #            this family lives under $defs; the dead call would have mattered
    #            the moment one was inlined at the root.
    #        (2) THE FAMILY, NOT ONE MEMBER. decisions/0111 E1 gave five more
    #            blocks the same container, each carrying the same renamed key,
    #            so the constraint covers every $defs/by_producing_arm* -- a
    #            check that guarded one of six would have been a constraint with
    #            five ways around it.
    c = Check(
        "S35",
        "no oneOf or anyOf branch sits on the path from the schema root to any "
        "$defs/by_producing_arm* container, so a writer emitting the retired key fails loudly",
    )
    schema_root = ev.root
    targets = {f"#/$defs/{name}" for name in (schema_root.get("$defs") or {})
               if name.startswith("by_producing_arm")}
    found_paths: list[str] = []

    def _scan(node, path: str, branching: list[str], seen: set) -> None:
        if isinstance(node, dict):
            if node.get("$ref") in targets:
                found_paths.append(path)
                if branching:
                    c.failures.append(
                        f"{path} reaches by_producing_arm through a branch keyword at "
                        f"{branching[-1]}: a writer emitting the retired `dual_status` key "
                        f"would produce 'matched 0 oneOf branches' at the parent instead of a "
                        f"named additionalProperties failure"
                    )
                return
            ref = node.get("$ref")
            if isinstance(ref, str):
                if ref in seen:
                    return
                _scan(ev.resolve(ref), path, branching, seen | {ref})
                return
            for key, value in node.items():
                if key in ("oneOf", "anyOf"):
                    for i, sub in enumerate(value):
                        _scan(sub, f"{path}.{key}[{i}]", branching + [f"{path}.{key}"], seen)
                elif key in ("properties", "$defs", "patternProperties"):
                    for k, sub in value.items():
                        _scan(sub, f"{path}.{k}", branching, seen)
                elif key in ("items", "then", "else", "if", "additionalProperties"):
                    if isinstance(value, dict):
                        _scan(value, f"{path}.{key}", branching, seen)
                elif key == "allOf":
                    for i, sub in enumerate(value):
                        _scan(sub, f"{path}.allOf[{i}]", branching, seen)

    if not targets:
        c.failures.append(
            "the schema defines no by_producing_arm container at all: this check examined "
            "nothing, which is not the same as finding nothing"
        )
        c.sites += 1
    # WRAPPED IN {"properties": ...} at v1.4.0. Handed the bare property map, as
    # it was until now, _scan followed none of its keys and returned at once.
    _scan({"properties": schema_root.get("properties", {})}, "$", [], set())
    _scan({"properties": schema_root.get("$defs", {})}, "$defs", [], set())
    c.sites += len(found_paths)
    c.notes.append(
        f"{len(targets)} container definition(s) in the family, reached at "
        f"{len(found_paths)} reference site(s): {sorted(targets)}"
    )
    if not found_paths:
        c.failures.append(
            "no reference to any by_producing_arm container was found in the schema: this "
            "check examined nothing, which is not the same as finding nothing"
        )
        c.sites += 1
    checks.append(c)

    # S36 -- NO FILE, AND NO ENTRY, CARRIES A BLOCK PUBLISHED BY ANOTHER STEP.
    #        decisions/0111 §3, Q1. ONLY ABSENCES WERE POLICED: the file was
    #        checked for writing too LITTLE (S22) and never for writing too MUCH,
    #        and that asymmetry is what let a single-arm step's placeholder ship
    #        carrying `action_type_counts` -- a block its OWN ownership table
    #        marked `published_by_step: step9`, `may_first_writer_fill: false` --
    #        in the file Step 11's writer will copy. It declared five blocks
    #        absent on the reasoning that "writing a copy here would be a second
    #        place that figure lives", and then wrote a sixth.
    #
    #        THE PUBLISHER TABLE IS EXTERNAL, for the reason S31 records about
    #        duality and S22 now applies to publishers: a table read from the
    #        file under test could only agree with itself.
    c = Check(
        "S36",
        "no arm entry carries a per-arm block published by another step, and no arm file "
        "carries a top-level block published by another step",
    )
    file_step = _producing_step(inst)
    merged_doc = _is_merged_document(inst)
    for i, arm in enumerate(inst.get("arms", [])):
        entry_step = arm.get("producing_step")
        if entry_step is None:
            c.sites += 1
            c.failures.append(
                f"$.arms[{i}]: no producing_step, so there is nothing to check a block's "
                f"publisher against -- the entry key is (W_days, clock_origin, producing_step)"
            )
            continue
        for name, publisher in sorted(BLOCK_PUBLISHER.items()):
            if name not in arm:
                continue
            c.sites += 1
            if publisher != entry_step:
                c.failures.append(
                    f"$.arms[{i}].{name}: present in a {entry_step!r} entry, and this block is "
                    f"published by {publisher!r}. A block another step publishes arrives in "
                    f"that step's own entry and its own file; writing a copy here would be a "
                    f"second place that figure lives"
                )
    for family in ("variants", "subpopulation_cuts"):
        for i, entry in enumerate(inst.get(family) or []):
            if not isinstance(entry, dict):
                continue
            step_of = entry.get("producing_step")
            for name in sorted(set(entry) & set(BLOCK_PUBLISHER)):
                c.sites += 1
                if BLOCK_PUBLISHER[name] != step_of:
                    c.failures.append(
                        f"$.{family}[{i}].{name}: present in a {step_of!r} entry, and this "
                        f"block is published by {BLOCK_PUBLISHER[name]!r}"
                    )
    if not merged_doc:
        for name, publisher in sorted(TOP_LEVEL_PUBLISHER.items()):
            if name not in inst:
                continue
            c.sites += 1
            if publisher == file_step:
                continue
            # THE ABSENCE IDIOM IS THE LEGAL FORM (decisions/0114 E8). A block
            # another party publishes may be PRESENT as a record that says so --
            # `channel_classes` is REQUIRED at the top level, so an arm file has
            # no way to omit it and must be able to state the absence. What is
            # forbidden is a FILLED copy: that is the seventh writer of a figure
            # none of them produced.
            if _is_block_absence(inst[name]) or _is_absence(inst[name]):
                c.notes.append(
                    f"$.{name}: present as an ABSENCE RECORD in {file_step!r}'s file, which is "
                    f"the legal form -- the block is published by {publisher!r} and this file "
                    f"states that rather than falling silent (decisions/0114 E8)"
                )
                continue
            c.failures.append(
                f"$.{name}: FILLED in {file_step!r}'s file, and this block is published "
                f"by {publisher!r}. It holds figures this file's step did not produce, so a "
                f"copy here is one of seven writers of one figure, with no precedence rule "
                f"and no agreement check. The legal form is the absence idiom "
                f"(decisions/0114 E8)"
            )
    else:
        # THE PUBLISHER'S OWN FILE CARRIES THE REAL ONE. Absence everywhere and
        # presence nowhere is the failure the one-place rule creates if it is
        # applied without its other half.
        for name, publisher in sorted(TOP_LEVEL_PUBLISHER.items()):
            if publisher != file_step or name not in inst:
                continue
            c.sites += 1
            if _is_block_absence(inst[name]) or _is_absence(inst[name]):
                c.failures.append(
                    f"$.{name}: an ABSENCE RECORD in {file_step!r}'s own file, and "
                    f"{file_step!r} is the step that publishes it. Every other file states "
                    f"this block's absence; if this one does too, the figure is nowhere"
                )
        # The file's own table is read here too -- and only to be asserted
        # against the external one, never to decide the question.
        ownership = inst.get("block_ownership") or {}
        for name, publisher in sorted(TOP_LEVEL_PUBLISHER.items()):
            entry = ownership.get(name)
            if not isinstance(entry, dict):
                continue
            c.sites += 1
            if entry.get("published_by_step") != publisher:
                c.failures.append(
                    f"$.block_ownership.{name}.published_by_step is "
                    f"{entry.get('published_by_step')!r}; the spec fixes {publisher!r}"
                )
    checks.append(c)

    # S37 -- THE ADOPTED-RULE REVISION IS A KEY FIELD, AND IT IS READ FROM A FILE
    #        RATHER THAN TYPED (decisions/0114 E14). It is the fourth identity
    #        dimension, and its lineage is the same as `clock_origin`'s and
    #        `producing_step`'s: a setting under which the measurement was taken
    #        that was invisible in the key. THE DIMENSION HAS ALREADY BEEN
    #        OCCUPIED -- processed/step5/adopted_rule.json carried revision-3
    #        figures against the approved revision-6 rule, and a Step 8 instance
    #        had to work around it, which is why CLAUDE.md made processed/ the
    #        eighth propagation surface.
    #
    #        The registry says WHERE the value was read from, so a reader can go
    #        and check it. A typed revision would be a second definition of the
    #        rule's version, which is the defect this study has hit most often.
    c = Check(
        "S37",
        "every arm, variant and cut entry names the adopted-rule revision it was measured "
        "under, and the registry says which file and key that value was READ FROM",
    )
    reg = inst.get("adopted_rule_revision")
    c.sites += 1
    if not isinstance(reg, dict):
        c.failures.append(
            "$.adopted_rule_revision is absent: the fourth key dimension has no registry, so "
            "each entry's revision is a claim with nothing behind it (decisions/0114 E14)"
        )
        reg = {}
    else:
        for field in ("revision", "source_file", "source_key", "source_sha256_12",
                      "read_not_typed"):
            if field not in reg:
                c.failures.append(f"$.adopted_rule_revision: missing {field}")
        if reg.get("read_not_typed") is not True:
            c.failures.append(
                "$.adopted_rule_revision.read_not_typed is not true: the revision is READ FROM "
                "the adopted-rule file at write time, never typed into this document"
            )
    merged_here = _is_merged_document(inst)
    present = reg.get("revisions_present")
    for family in ENTRY_FAMILIES:
        for i, entry in enumerate(inst.get(family) or []):
            if not isinstance(entry, dict):
                continue
            c.sites += 1
            value = entry.get("adopted_rule_revision")
            if value is None:
                c.failures.append(
                    f"$.{family}[{i}]: no adopted_rule_revision. Two runs at one "
                    f"(W, clock origin, step) setting under different rule revisions are "
                    f"DIFFERENT MEASUREMENTS, and without this field check S2 calls the "
                    f"second a duplicate of the first"
                )
            elif merged_here:
                if not isinstance(present, list) or value not in present:
                    c.failures.append(
                        f"$.{family}[{i}].adopted_rule_revision is {value!r} and is not in "
                        f"$.adopted_rule_revision.revisions_present {present!r} -- the merged "
                        f"document carries entries from several runs, so the revisions it "
                        f"holds are enumerated rather than assumed to be one"
                    )
            elif "revision" in reg and value != reg.get("revision"):
                c.failures.append(
                    f"$.{family}[{i}].adopted_rule_revision is {value!r}; this file was "
                    f"written under revision {reg.get('revision')!r}. One arm file is one "
                    f"run, and one run is one revision"
                )
    checks.append(c)

    # S38 -- A DECLARED INTERVAL BELONGS TO A STEP THAT PRODUCES IT, AND IN AN ARM
    #        FILE TO THAT FILE'S OWN STEP AND ARM (decisions/0114 E11).
    #        `$.declared_intervals` sat outside ENTRY_FAMILIES and outside
    #        TOP_LEVEL_PUBLISHER, so nothing asked whose interval an entry was and
    #        an arm file could carry another step's. OCCUPIED, in the shipped
    #        single-arm placeholder: the WINDOW-W PERCENTILE attributed to
    #        `step11`, which does not compute W.
    c = Check(
        "S38",
        "every declared interval names a producing step the spec lets publish that quantity "
        "class, and in an arm file names that file's own step and arm",
    )
    file_step_i = _producing_step(inst)
    file_arm_i = (inst.get("document_scope") or {}).get("arm")
    for i, entry in enumerate(inst.get("declared_intervals") or []):
        if not isinstance(entry, dict):
            continue
        step_of = entry.get("produced_by_step")
        arm_of = entry.get("producing_arm")
        qclass = (entry.get("ci") or {}).get("quantity_class")
        c.sites += 1
        allowed = INTERVAL_CLASS_PUBLISHERS.get(qclass)
        if allowed is None:
            c.notes.append(
                f"$.declared_intervals[{i}]: quantity class {qclass!r} names no publisher in "
                f"the external table -- it is open to any writer by construction, so only the "
                f"arm-identity clause applies to it"
            )
        elif step_of not in allowed:
            c.failures.append(
                f"$.declared_intervals[{i}]: attributed to {step_of!r}, which does not produce "
                f"a {qclass!r} interval. The spec lets {list(allowed)!r} publish that class "
                f"(decisions/0114 E11)"
            )
        if not merged_here:
            c.sites += 1
            if step_of != file_step_i or arm_of != file_arm_i:
                c.failures.append(
                    f"$.declared_intervals[{i}]: names ({step_of!r}, {arm_of!r}) in "
                    f"{file_step_i!r}'s arm-{file_arm_i!r} file. One file is one step's output "
                    f"for one arm, and an interval is a measurement like any other"
                )
    if not (inst.get("declared_intervals") or []):
        c.declared_empty = (
            "this file declares no intervals. The block is optional and the emptiness is "
            "reported rather than passed over."
        )
        c.coverage = 0
    checks.append(c)

    # S39 -- THE PUBLISHER TABLE COVERS EVERY PER-ARM BLOCK THE SCHEMA DEFINES
    #        (decisions/0114 E12). S22 iterates BLOCK_PUBLISHER and S36 iterates
    #        BLOCK_PUBLISHER, so A BLOCK THE TABLE DOES NOT NAME IS A BLOCK
    #        NEITHER OF THEM LOOKS AT: it can be written into any step's entry, in
    #        any file, and no control says a word. Nothing kept the table complete
    #        except that it happened to be, and "complete today" is not a control.
    #
    #        The two sets are compared against each other, and the exemptions --
    #        the identity fields and `headline` -- are declared in this module,
    #        outside the schema and outside the file under test.
    c = Check(
        "S39",
        "every per-arm block property the schema defines has a row in the external publisher "
        "table, and every row names a property the schema defines",
    )
    arm_entry_schema = ((ev.root.get("$defs") or {}).get("arm_entry") or {})
    props = set((arm_entry_schema.get("properties") or {}))
    if not props:
        c.failures.append(
            "$defs/arm_entry defines no properties: the closure has nothing to run against, "
            "and a check that looked at nothing is not a clean check"
        )
    blocks_in_schema = props - set(ARM_ENTRY_NON_BLOCK_PROPERTIES)
    for name in sorted(blocks_in_schema):
        c.sites += 1
        if name not in BLOCK_PUBLISHER:
            c.failures.append(
                f"$defs/arm_entry.properties.{name}: a per-arm block with NO row in the "
                f"external publisher table. S22 and S36 both iterate that table, so this "
                f"block can be written into any step's entry in any file and neither check "
                f"looks at it (decisions/0114 E12). Give it a row, or declare it a non-block "
                f"in ARM_ENTRY_NON_BLOCK_PROPERTIES with a reason"
            )
    for name in sorted(BLOCK_PUBLISHER):
        c.sites += 1
        if name not in props:
            c.failures.append(
                f"BLOCK_PUBLISHER names {name!r}, which $defs/arm_entry does not define. A row "
                f"for a block that no longer exists reads as coverage and is none"
            )
    c.notes.append(
        f"exempted as identity or headline slots, by name in this module: "
        f"{sorted(ARM_ENTRY_NON_BLOCK_PROPERTIES & props)}"
    )
    checks.append(c)

    # S40 -- THE STATISTIC IS RECORDED AS A VALUE, NOT AS A DECLARATION THAT A
    #        CHOICE EXISTS (decisions/0118). Until v1.5.0 $.bootstrap_spec listed
    #        "statistic (levels vs movements)" under `fields_not_fixed_in_spec`
    #        and each registry entry carried ONE statistic, per arm. The Human
    #        Lead fixed it as BOTH, so the registry must hold BOTH the way it
    #        holds B, the seed and the unit.
    #
    #        The partition leg is the half that stops an EMPTY
    #        `fields_not_fixed_in_spec` reading as a list nobody filled in:
    #        `fields_considered` names the universe, and the two lists must be
    #        disjoint and cover it. CLAUDE.md -- an empty result and a clean
    #        result are the same value, and only the control knows which it
    #        produced.
    #
    #        TWO THINGS ADDED AT v1.7.0 (reviewer-engineering E1 and E2 on the
    #        v1.6.0 review, ruled on by the Human Lead 2026-08-19).
    #
    #        E1 -- IT POLICED THE WRONG FIELD. Everything above reads
    #        `fields_not_fixed_in_spec` BY NAME. `spec_status` -- the field that
    #        actually carries the claim, and whose enum still offered
    #        `unfixed_at_time_of_writing` -- appeared ZERO times in this module, so
    #        an entry could declare itself unfixed while listing all four elements
    #        as fixed and validate at 41 checks, 0 failures. The status is now
    #        DERIVED from the two lists and the declaration asserted against the
    #        derivation.
    #
    #        E2 -- THE ENTRY-LEVEL FIXED LIST HAD NO PARTITION ANCHOR. One level up
    #        `fields_considered` names the universe so an empty not-fixed list is
    #        established rather than merely empty; one level down there was no such
    #        list and the only assertion was membership of `statistics`, so
    #        `fields_fixed_in_spec: ["statistics"]` -- B, the seed and the unit
    #        silently dropped -- passed. THE SAME REASONING, APPLIED ONE LEVEL
    #        DOWN: each entry declares its own universe and the two lists partition
    #        it.
    c = Check(
        "S40",
        "the bootstrap registry records the statistic as a VALUE -- both objects present in "
        "$.bootstrap_spec and in every settings entry, listed as fixed, with the fixed and "
        "not-fixed lists partitioning a declared universe at BOTH levels and each entry's "
        "`spec_status` derived from its own lists rather than declared freely",
    )
    expected_statistics = {"levels", "movements"}
    spec = inst.get("bootstrap_spec")
    if not isinstance(spec, dict):
        c.failures.append(
            "$.bootstrap_spec is absent: the one place the spec-fixed bootstrap is stated"
        )
    else:
        c.sites += 1
        got = spec.get("statistics")
        if not isinstance(got, list) or set(got) != expected_statistics:
            c.failures.append(
                f"$.bootstrap_spec.statistics is {got!r}; decisions/0118 fixes the statistic "
                f"as BOTH levels and paired movements, so the value is the pair and both "
                f"members must be present. Recording one is recording a per-arm choice the "
                f"ruling removed"
            )
        fixed = spec.get("fields_fixed_in_spec") or []
        notfixed = spec.get("fields_not_fixed_in_spec")
        considered = spec.get("fields_considered")
        if "statistics" not in fixed:
            c.failures.append(
                f"$.bootstrap_spec.fields_fixed_in_spec is {fixed!r} and does not name "
                f"`statistics`. It is fixed (decisions/0118) and must be listed with B, the "
                f"seed and the unit"
            )
        if isinstance(notfixed, list):
            for item in notfixed:
                if "statistic" in str(item).lower():
                    c.failures.append(
                        f"$.bootstrap_spec.fields_not_fixed_in_spec still names the statistic "
                        f"({item!r}). decisions/0118 fixed it; a field listed as unfixed after "
                        f"it was fixed is the stale half of a propagation, not a caveat"
                    )
        c.failures.extend(
            _partition_failures("$.bootstrap_spec", considered, fixed, notfixed))
        if isinstance(considered, list) and considered:
            c.notes.append(
                f"partition checked over {len(considered)} declared bootstrap element(s) at "
                f"$.bootstrap_spec: {sorted(set(considered))}"
            )
    registry = inst.get("bootstrap_settings") or {}
    entry_universes: list[int] = []
    for key in sorted(registry):
        entry = registry[key]
        if not isinstance(entry, dict):
            continue
        c.sites += 1
        if "statistic" in entry:
            c.failures.append(
                f"$.bootstrap_settings.{key}: carries the SINGULAR `statistic` key, which was "
                f"an arm's choice of one object. It was renamed to `statistics` at v1.6.0 and "
                f"holds both (decisions/0118)"
            )
        got = entry.get("statistics")
        if not isinstance(got, list) or set(got) != expected_statistics:
            c.failures.append(
                f"$.bootstrap_settings.{key}.statistics is {got!r}; both levels and paired "
                f"movements must be present. A run that produces only one is INCOMPLETE, not "
                f"differently designed"
            )
        e_fixed = entry.get("fields_fixed_in_spec")
        e_notfixed = entry.get("fields_not_fixed_in_spec")
        e_considered = entry.get("fields_considered")
        if "statistics" not in (e_fixed or []):
            c.failures.append(
                f"$.bootstrap_settings.{key}.fields_fixed_in_spec does not name `statistics`. "
                f"The statistic is fixed for every entry, including the show-clustered ones "
                f"whose UNIT is not fixed by decisions/0103"
            )
        # E2 -- the anchor one level down. Membership of `statistics` was the ONLY
        # assertion on this list, so an entry naming `statistics` and nothing else
        # passed while silently dropping B, the seed and the unit.
        c.failures.extend(_partition_failures(
            f"$.bootstrap_settings.{key}", e_considered, e_fixed, e_notfixed))
        if isinstance(e_considered, list) and e_considered:
            entry_universes.append(len(set(e_considered)))
        # E1 -- the field that carries the claim. Derived from this entry's own
        # two lists and asserted against what the entry declares, so the two
        # cannot disagree in silence.
        declared = entry.get("spec_status")
        derived = _derive_spec_status(e_fixed, e_notfixed)
        if declared == _RETIRED_SPEC_STATUS:
            c.failures.append(
                f"$.bootstrap_settings.{key}.spec_status is {_RETIRED_SPEC_STATUS!r}, which was "
                f"RETIRED at v1.7.0: B, the seed and the statistic are fixed for every entry by "
                f"decisions/0103 and decisions/0118, so no entry can have an empty fixed list "
                f"and the token has no reachable referent. It was reachable in practice only as "
                f"a contradiction of this entry's own lists"
            )
        elif derived is None:
            c.failures.append(
                f"$.bootstrap_settings.{key}: spec_status cannot be derived -- the entry's "
                f"fixed list is absent or empty, and no entry can have an empty fixed list "
                f"(decisions/0103, decisions/0118)"
            )
        elif declared != derived:
            c.failures.append(
                f"$.bootstrap_settings.{key}.spec_status is {declared!r}, but this entry's own "
                f"lists derive {derived!r}: fixed={sorted(e_fixed)}, "
                f"not_fixed={sorted(e_notfixed)}. The status is a SUMMARY of the lists, and a "
                f"summary that disagrees with what it summarises is the half of a propagation "
                f"nobody checked -- `spec_status` appeared zero times in this module until "
                f"v1.7.0"
            )
        c.notes.append(
            f"$.bootstrap_settings.{key}: spec_status {declared!r} derived from "
            f"{len(e_notfixed or [])} unfixed of "
            f"{len(set(e_considered)) if isinstance(e_considered, list) else 0} considered"
        )
    c.notes.append(
        f"registry entries examined: {len(registry)}; entry-level partitions checked: "
        f"{len(entry_universes)}"
    )
    checks.append(c)

    # S41 -- BOTH OBJECTS ACTUALLY APPEAR, PER PRODUCING ARM (decisions/0118).
    #        S40 checks what the registry DECLARES; this checks what the file
    #        EMITS. "Every interval declares its statistic at the point of use,
    #        AND BOTH STATISTICS APPEAR. A run that emits only one is INCOMPLETE,
    #        not merely differently designed."
    #
    #        THE OWNER KEY IS (PRODUCING STEP, ARM) SINCE v1.8.0
    #        (reviewer-engineering E3). It is taken from the payload an interval
    #        sits in or from the declared-intervals entry that names it. Keying on
    #        the ARM alone was right for an arm file and wrong for the merged
    #        document, where `sole` is Steps 10, 11 and 12 together and `a` is Step
    #        9 AND Step 13 -- so Step 13 arm `a`'s single movement discharged Step
    #        9 arm `a`'s obligation, which is this check's own reason for keying
    #        per arm, one dimension out.
    #
    #        SCOPE-AWARE SINCE v1.7.0 (Human Lead ruling, 2026-08-19): a Step 12
    #        file is not asked for intervals at all, and failing it for having none
    #        would make it manufacture two figures the spec never asked it to
    #        compute. NARROWED AT v1.8.0 TO THE EMPTY BRANCH ALONE (E4 of the same
    #        review): the exemption used to gate the per-owner missing-object
    #        branch as well, so a Step 12 file emitting forty levels-only intervals
    #        passed with a note. THE RULING'S GROUND DOES NOT REACH THAT STATE -- a
    #        file that has already computed intervals is being asked to manufacture
    #        nothing, and decisions/0118's "a run that emits only one is INCOMPLETE"
    #        applies to it directly.
    #
    #        A MERGED DOCUMENT IS STILL NEVER EXEMPT, and the reason is now the
    #        keying rather than the aggregation it used to rest on: a step that
    #        publishes no interval raises no owner key at all, so Step 12's silence
    #        inside a merge is simply absent rather than covered by another step's
    #        movement. The two facts are independent, where before the second was
    #        an artifact of the defect E3 names.
    c = Check(
        "S41",
        "both bootstrap statistics -- levels and paired movements -- appear among the "
        "intervals of every (producing step, arm) in this file",
    )
    s41_step = _producing_step(inst)
    s41_exempt = (
        None if _is_merged_document(inst)
        else INTERVALS_NOT_MANDATED_BY_STEP.get(s41_step)
    )
    by_owner: dict = {}
    for path, istep, arm, ci in _iter_cis_with_arm(inst):
        c.sites += 1
        stat = ci.get("statistic")
        if stat is None:
            c.failures.append(
                f"{path}: no statistic. Every interval declares which of the two objects it "
                f"is, at the point of use -- a level and a movement are never compared to "
                f"each other"
            )
            continue
        by_owner.setdefault((istep, arm), {}).setdefault(stat, []).append(path)
    for owner in sorted(by_owner, key=lambda t: (t[0] is None, str(t[0]),
                                                 t[1] is None, str(t[1]))):
        istep, arm = owner
        seen = set(by_owner[owner])
        missing = expected_statistics - seen
        if not missing:
            continue
        n_ivl = sum(len(v) for v in by_owner[owner].values())
        # NO EXEMPTION HERE, INCLUDING FOR STEP 12 (v1.8.0). Having published an
        # interval, a writer owes both objects: the ruling exempts a step from
        # PRODUCING intervals, not from producing them completely.
        c.failures.append(
            f"step {istep!r} arm {arm!r} declares {sorted(seen)} and none of "
            f"{sorted(missing)} across {n_ivl} interval(s). Every producing step produces "
            f"BOTH objects (decisions/0118); a run emitting one is INCOMPLETE rather than "
            f"differently designed. The Step 12 exemption does NOT reach this branch -- it "
            f"covers a step asked for no interval, and this owner published "
            f"{n_ivl} of them"
        )
    c.notes.append(
        "intervals examined per (producing step, arm) and statistic: "
        + json.dumps({f"{o[0]}/{o[1]}": {s: len(p) for s, p in sorted(m.items())}
                      for o, m in sorted(by_owner.items(),
                                         key=lambda kv: (str(kv[0][0]), str(kv[0][1])))},
                     sort_keys=True)
    )
    if not by_owner and s41_exempt is None:
        c.failures.append(
            "this file carries no interval whose owning arm is knowable, so the "
            "both-objects requirement was checked against nothing. An empty result and a "
            "clean result are the same value"
        )
    # An exempt step with no intervals is scope-empty rather than vacuous, and
    # _declare_scope_emptiness() names the restriction -- reached through
    # CHECK_SUBJECT below, the same route every other scope-empty check takes,
    # rather than through a second emptiness idiom written here.
    checks.append(c)

    _declare_scope_emptiness(inst, checks)
    return checks


# Which block each check's sites come from. Used only when a check found NO
# sites: under ONE FILE PER STEP PER ARM (decisions/0109 §1) a file legitimately
# contains none of another step's blocks, and a check with nothing to examine
# there is out of scope rather than vacuous. THE DISTINCTION IS DRAWN FROM THE
# FILE'S OWN ABSENCE RECORDS, never assumed: an emptiness with no absence record
# behind it stays VACUOUS and still fails.
CHECK_SUBJECT = {
    "S4": "bounds", "S7": "bounds", "S8": "bounds", "S9": "bounds",
    "S11": "bounds", "S20": "bounds",
    "S10": "abandonment_distribution", "S25": "abandonment_distribution",
    "S26": "abandonment_distribution",
    "S14": "waterfall",
    # S41 JOINED AT v1.7.0 (Human Lead ruling, 2026-08-19). Its subject is not a
    # block but the INTERVALS a file carries, and its warrant is not the publisher
    # table but INTERVALS_NOT_MANDATED_BY_STEP -- a step the spec asks for no
    # interval at all. Routed through here rather than declared inside the check
    # so there is one emptiness idiom in this module and not two.
    "S41": "intervals",
}


def _absence_records_for(inst: dict, subject: str) -> list[tuple[str, dict]]:
    """The explicit absence records this file carries for `subject`."""
    out: list[tuple[str, dict]] = []
    if subject == "intervals":
        # Every `ci_or_absence` slot the file filled with an ABSENCE rather than an
        # interval. This is the coverage count for S41's scope-empty branch: it is
        # what distinguishes a file that considered each interval slot and recorded
        # why there is none from a file that carries no interval slots at all.
        for path, node in _walk(inst):
            if isinstance(node, dict) and path.endswith(".ci") and _is_absence(node):
                out.append((path, node))
        return out
    if subject == "bounds":
        for base, pop, block in _iter_payloads(inst):
            for key, payload in ((block.get("by_producing_arm") or {}).get("arms") or {}).items():
                path = f"{base}.by_producing_arm.arms.{key}"
                if _is_absence(payload):
                    out.append((path, payload))
                elif isinstance(payload, dict) and _is_block_absence(payload.get("bounds")):
                    out.append((f"{path}.bounds", payload["bounds"]))
        return out
    for family in ("arms", "variants", "subpopulation_cuts"):
        for i, entry in enumerate(inst.get(family) or []):
            node = (entry or {}).get(subject)
            if _is_block_absence(node):
                out.append((f"$.{family}[{i}].{subject}", node))
    return out


def _declare_scope_emptiness(inst: dict, checks: list) -> None:
    """Turn a scope-empty check into a NAMED N/A, or leave it VACUOUS.

    CLAUDE.md: an empty result and a clean result are the same value, and only
    the control knows which it produced. So the control says which -- by quoting
    an absence record the FILE carries, or, since v1.4.0, by naming the EXTERNAL
    publisher table under which this file could not have carried the block at
    all. No record and no external warrant, no exemption.

    THE SECOND ROUTE IS THE STRONGER ONE, and it exists because the file stopped
    carrying absences for other steps' blocks: under decisions/0111 E2 an arm
    entry is one step's measurement, so another step's block is OMITTED, and the
    old route -- quote the file's own absence record -- would have had nothing to
    quote. Reading the external table instead of the file's own claim is the same
    correction decisions/0111 E4 made to S22.
    """
    file_step = _producing_step(inst)
    merged = _is_merged_document(inst)
    for c in checks:
        subject = CHECK_SUBJECT.get(c.cid)
        if subject is None or c.sites or c.failures or c.skipped_reason or c.declared_empty:
            continue
        if subject == "intervals":
            # THE WARRANT IS A STEP-LEVEL EXEMPTION, NOT A PUBLISHER ROW. The
            # block is not another step's; the spec asks THIS step for no interval
            # at all (Human Lead ruling, 2026-08-19). A step not in the table falls
            # through with no declaration and stays VACUOUS -- which, for S41, is
            # already a FAIL raised in the check itself, so an unlisted step cannot
            # reach a passing state by this route.
            reason = None if merged else INTERVALS_NOT_MANDATED_BY_STEP.get(file_step)
            if reason is None:
                continue
            records = _absence_records_for(inst, "intervals")
            c.coverage = len(records)
            if not records:
                # ZERO COVERAGE IS NOT A DECLARED EMPTINESS (v1.8.0,
                # reviewer-engineering E5). `declared_empty` used to be set
                # unconditionally, carrying the words "so the emptiness was
                # searched for rather than assumed" with nothing requiring a
                # single record to have been examined -- so a file whose headline
                # blocks are simply absent was awarded EMPTY_DECLARED for a search
                # that examined nothing. That is the rule S33 enforces on every
                # other search record and CLAUDE.md states in as many words: an
                # empty result and a clean result are the same value, and a check
                # that finds nothing because it looked nowhere must FAIL. The
                # exemption survives; what it no longer does is stand in for the
                # coverage.
                c.notes.append(
                    f"the step-level interval exemption applies to {file_step!r}, but this "
                    f"file carries NO interval-absence record: nothing was examined, so the "
                    f"emptiness is not established and this check stays VACUOUS. An exempt "
                    f"step still says where its intervals would have been"
                )
                continue
            c.declared_empty = (
                f"this file carries no interval, and is not asked for one: it is "
                f"{file_step!r}'s output, and {reason}. The requirement decisions/0118 fixes "
                f"is that a step which PRODUCES intervals produces BOTH objects; it creates "
                f"no obligation to produce any. {len(records)} interval slot(s) in this file "
                f"carry an explicit absence record rather than an interval, so the emptiness "
                f"was searched for rather than assumed. THE EXEMPTION IS THIS STEP'S ALONE and "
                f"reaches only a file with no interval at all: a step that HAS published "
                f"intervals owes both objects like any other, and every step outside "
                f"{sorted(INTERVALS_NOT_MANDATED_BY_STEP)} fails this branch."
            )
            c.notes.append(
                f"scope-empty by the step-level interval exemption: {file_step!r} is asked for "
                f"no interval; {len(records)} explicit interval-absence record(s) examined")
            continue
        records = _absence_records_for(inst, subject)
        if records:
            path, rec = records[0]
            owner = rec.get("owning_step") or rec.get("status")
            c.skipped_reason = (
                f"this file carries no {subject} to examine, and it says so: {len(records)} "
                f"explicit absence record(s), the first at {path} with status "
                f"{rec.get('status')!r} and owning step {owner!r}. Under ONE FILE PER STEP PER "
                f"ARM (decisions/0109 §1) that block arrives in its own step's file and is "
                f"merged at Step 13b. An emptiness with NO warrant behind it is not exempted "
                f"here and still reports VACUOUS."
            )
            c.notes.append(
                f"scope-empty, declared by {len(records)} absence record(s) in the file")
            continue
        publisher = BLOCK_PUBLISHER.get(subject)
        if publisher is not None and not merged and publisher != file_step:
            c.skipped_reason = (
                f"this file carries no {subject} to examine, and could not: it is "
                f"{file_step!r}'s output, the block is published by {publisher!r} in the "
                f"EXTERNAL publisher table this module holds, and under ONE FILE PER STEP PER "
                f"ARM (decisions/0109 §1) it arrives in that step's own file and is merged at "
                f"Step 13b. The warrant is the external table, not a sentence this file wrote "
                f"about itself -- a table read from the file under test could only agree with "
                f"itself (decisions/0111 E4)."
            )
            c.notes.append(
                f"scope-empty by the external publisher table: {subject} is {publisher!r}'s")


def validate_file(instance_path: str, schema_path: str) -> dict:
    with open(schema_path) as fh:
        schema = json.load(fh)
    with open(instance_path) as fh:
        inst = json.load(fh)

    ev = SchemaEvaluator(schema)
    structural_ok = ev.validate(inst, schema)
    checks = run_semantic_checks(inst, ev)

    # VACUOUS is still a failure: a check that looked at nothing and cannot say
    # why is indistinguishable from one that found nothing. EMPTY_DECLARED is
    # not, because the file states the emptiness and carries the coverage count
    # of the search that established it (reviewer-engineering F4).
    failed = [c for c in checks if c.status in ("FAIL", "VACUOUS")]
    return {
        "instance": instance_path,
        "schema": schema_path,
        "schema_validation": {
            "passed": structural_ok,
            "error_count": len(ev.errors),
            "errors": ev.errors[:40],
            "measurement_slots_applied": len(ev.measurement_sites),
        },
        "semantic_checks": [c.as_dict() for c in checks],
        "checks_total": len(checks),
        "checks_passed": sum(1 for c in checks if c.status == "PASS"),
        "checks_not_applicable": sum(1 for c in checks if c.status == "N/A"),
        "checks_empty_declared": sum(1 for c in checks if c.status == "EMPTY_DECLARED"),
        "checks_failed": len(failed),
        "ok": structural_ok and not failed,
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    instance_path = argv[1]
    schema_path = "artifacts/step8b-output-schema.json"
    if "--schema" in argv:
        schema_path = argv[argv.index("--schema") + 1]
    report = validate_file(instance_path, schema_path)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
