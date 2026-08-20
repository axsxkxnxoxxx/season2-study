"""Step 8b -- build the JSON schema Step 16 reads from, and its placeholder.

Owner: Analytics Engineer. Mode: Chained. Zero API calls.

Writes:
    artifacts/step8b-output-schema.json        the schema
    artifacts/step8b-placeholder.json          a MERGED-DOCUMENT instance, flagged as a
                                               placeholder; this is the shape Step 16 renders
    artifacts/step8b-placeholder-arm-file.json an ARM-FILE instance of a DUAL step (Step 9,
                                               arm a), flagged the same way
    artifacts/step8b-placeholder-sole-file.json an ARM-FILE instance of a SINGLE-ARM step
                                               (Step 11, arm `sole`), flagged the same way
    logs/step8b/validation-<stamp>.json        the validator run record for all three

All four artifacts are generated. Nothing in any of them is typed by hand at any
later point: if a value is wrong, this file is where it is corrected and all four
are rewritten together (CLAUDE.md, "Derived figures" and "Generated files that
function as checks").

The placeholder rule, stated once and enforced mechanically:

    Structure is real. Measurements are sentinels.

    Identifiers, keys, enum values, booleans, refs, spec-fixed definitions and
    the provenance block are written as they would really appear, so Step 16 can
    be built against every branch. Two families of slot are marked in the schema
    itself and enforced mechanically by src/step8b_validate.py:

      "x-measurement": true  holds -999 (counts) or -999.0 (percents and
                             percentage points) in a placeholder, and may never
                             hold either in a real file.            Check S5.
      "x-writer-text": true  a string whose content is run-specific and is
                             supplied by the step that writes it. Carries the
                             placeholder prefix in a placeholder, and may never
                             carry it in a real file.               Check S6.

    The second half of each rule is the useful one: it is what stops a leftover
    placeholder value surviving into a published file unnoticed.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(ROOT, "artifacts", "step8b-output-schema.json")
PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder.json")
ARM_PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder-arm-file.json")
SOLE_PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder-sole-file.json")
LOG_DIR = os.path.join(ROOT, "logs", "step8b")

# THE ARM LABELS S30 NORMALISES, IMPORTED RATHER THAN RESTATED
# (reviewer-engineering E3 on the v1.6.0 review). The count was typed as "five"
# in three places -- the check's own sentence and the two limit strings below --
# after v1.6.0 dropped `statistic` and left the tuple at four, and it propagated
# into all three placeholders. CLAUDE.md: one register, imported by every script
# that checks. The validator holds the tuple; this module reads it.
sys.path.insert(0, os.path.join(ROOT, "src"))
from step8b_validate import (  # noqa: E402
    ARM_LABELS_ARITY_WORD as _ARM_LABELS_ARITY_WORD,
    ARM_LABELS_NORMALISED as _ARM_LABELS_NORMALISED,
    REGISTRY_ARM_DIFFERENCE_FACT as _REGISTRY_ARM_DIFFERENCE_FACT,
)

SCHEMA_VERSION = "1.9.0"

# THE URN IS DERIVED FROM THE VERSION, NEVER TYPED BESIDE IT (v1.9.0, found by
# the coordinator on this build). `SCHEMA_ID` used to be a literal with the
# version spelled out inside it, so ONE VERSION HAD TWO DEFINITIONS -- and the
# v1.9.0 bump moved one of them. The schema then carried
# `schema_version.const = "1.9.0"` beside `schema_id.const =
# "urn:...:1.8.0"` and `$id = "urn:...:1.8.0"`, and all three placeholders
# carried the same pair.
#
# EVERY CONTROL PASSED, and the reason is worth writing down: the placeholders
# agree with the schema on each field INDEPENDENTLY -- `1.9.0` matches the
# version const, `...:1.8.0` matches the id const -- so the two identifiers were
# internally consistent and disagreed only with EACH OTHER. Nothing compared
# them, and `schema_id` is the field a consumer keys on.
#
# This is the same move as ARM_LABELS_ARITY_WORD under decisions/0120 §2 E3,
# where the word "five" was typed into a sentence beside a four-element tuple:
# a quantity that restates another quantity is derived from it, or it drifts.
# Check S42 asserts the derivation on the SCHEMA AS BUILT, so a future literal
# reintroduced here fails rather than shipping.
SCHEMA_URN_STEM = "urn:season2-study:step8b-output-schema"
SCHEMA_ID = f"{SCHEMA_URN_STEM}:{SCHEMA_VERSION}"

# WHERE THE ADOPTED-RULE REVISION IS READ FROM (decisions/0114 E14). It is the
# fourth identity dimension, and the ruling asks where the value is READ rather
# than typed. It is read HERE, from the file a Step 8 implementation reaches for
# first -- processed/step5/adopted_rule.json, CLAUDE.md's eighth propagation
# surface -- because that file is where the dimension was occupied: it carried
# REVISION-3 figures against the approved REVISION-6 rule and a Step 8 instance
# had to work around it.
#
# The file has NO first-class revision field. It names the revision only in its
# KEY NAMES (`approved_rule_revision_6`, `approved_revision_6`), so the reader
# below parses those and takes the highest, records WHICH KEY it read and the
# file's hash, and RAISES if it finds none. It does not default: a default would
# be a typed revision wearing a reader's clothes. The absence of a first-class
# field is reported to the Human Lead as a residual rather than fixed here --
# adopted_rule.json is Step 5's output and a deliverable is corrected by
# rerunning the arm that produced it (CLAUDE.md, Artifact sign-off).
ADOPTED_RULE_PATH = os.path.join(ROOT, "processed", "step5", "adopted_rule.json")
ADOPTED_RULE_REVISION_KEY_RE = r"approved_(?:rule_)?revision_(\d+)"

SENT_C = -999
SENT_P = -999.0
PH = "PLACEHOLDER — NOT A MEASUREMENT"


def ph(text: str) -> str:
    return f"{PH}: {text}"


# The adopted-rule revision, READ ONCE PER RUN from the file named above and
# cached, so that every entry in every emitted document carries one value from
# one reading. `_read_adopted_rule_revision` is defined with the other readers at
# the foot of this file; this is the accessor the builders use.
_REVISION_CACHE: dict | None = None


def _revision_record() -> dict:
    global _REVISION_CACHE
    if _REVISION_CACHE is None:
        _REVISION_CACHE = _read_adopted_rule_revision()
    return _REVISION_CACHE


def _revision() -> int:
    return _revision_record()["revision"]


# ---------------------------------------------------------------------------
# The schema
# ---------------------------------------------------------------------------

POPULATIONS = ["APPLY", "DERIV"]
FILTER_NAMES = [
    "step2_frame",
    "L2_eq_1_exclusion",
    "s1_completion_rule",
    "contamination_exclusion",
    "right_censoring",
    "liveness",
    "outcome_assignment",
]
OUTCOMES = ["never_started", "started_and_left", "continued"]
ABSENCE_STATUSES = [
    "structurally_absent",
    "not_published",
    "not_yet_written",
    "unruled",
    # Added at v1.1.0 against reviewer-engineering's F1, F3 and F5. Each names a
    # distinct reason a slot is empty, because a slot that is empty for four
    # different reasons and says so once cannot be read.
    "no_producer_in_spec",          # F1: no step in the spec produces this here.
    "superseded_for_this_purpose",  # F1: the figure exists but is superseded for this use.
    "not_a_dual_step",              # F5: this step is single-arm, so there is no per-arm split.
    "awaiting_owner_step",          # F9: the owning step has not run yet.
    "not_required_by_spec",         # F3: the spec does not ask this step for this quantity.
]

# Every step that may write into this file, plus the two non-step writers. Used
# by `written_by_step` and by $.block_ownership, so that no block is owned by
# "whoever writes first" (reviewer-engineering F9).
WRITER_STEPS = [
    "step8",
    "step8b",
    "step9",
    "step10",
    "step11",
    "step12",
    "step13",
    # Step 13b, the merged results document (task-sheet.md Step 13b, created by
    # decisions/0107). It is the ONLY step that reads both arms, and the only
    # writer permitted to be: a merged file needs a writer that reads both arms,
    # and no arm can be that writer without defeating what dual implementation
    # exists to do.
    "step13b",
    "step16",
    "human_lead",
]

# The steps the Human Lead owns among the writers above. The distinction is
# load-bearing at check S17: `cross_arm_divergences` is theirs, and a file whose
# producing step is NOT one of these is structurally forbidden to have performed
# the cross-arm search that block records (decisions/0107 §2(1), §4).
HUMAN_LEAD_STEPS = ["human_lead", "step13b"]

# WHICH STEPS ARE DUAL IS A FIXED FACT OF THE SPEC, NOT A LABEL A WRITER PICKS.
# Steps 9 and 13 run twice in isolation (CLAUDE.md, Dual implementation; Step
# 13's duality is decisions/0103 §3); Steps 10, 11 and 12 run once. Until v1.3.0
# `step_dual_status` was never read against `producing_step`, which sits two keys
# away in the same object, so a Step 9 block could DECLARE ITSELF single-arm and
# validate -- and in the merged document the dropped-arm clause is guarded on
# `step_dual_status == "dual"` and would then never fire. The loosening the split
# was written to forbid was reachable by RELABELLING rather than by widening.
# The map is fixed in the schema (const per step, inside by_producing_arm and in
# $.step_duality) and asserted again by check S31.
STEP_DUALITY = {
    "step9": "dual",
    "step10": "single_arm",
    "step11": "single_arm",
    "step12": "single_arm",
    "step13": "dual",
}
STEP_DUALITY_SOURCE = {
    "step9": "CLAUDE.md, Dual implementation; task-sheet.md Step 9",
    "step10": "CLAUDE.md, Dual implementation -- Step 10 is not in the dual list",
    "step11": "CLAUDE.md, Dual implementation -- Step 11 is not in the dual list",
    "step12": "CLAUDE.md, Dual implementation -- Step 12 is not in the dual list",
    "step13": "decisions/0103 §3, which resolved a live CLAUDE.md / task-sheet.md conflict",
}
# THE BOOTSTRAP STATISTIC IS FIXED AS BOTH (decisions/0118). Human Lead ruling,
# 2026-08-19, closing the THIRD AND LAST unfixed bootstrap element: both arms
# produce BOTH objects, both are LABELLED, and neither is presented as *the*
# design. All four elements are now fixed and identical for both arms -- B =
# 10,000, seed = 20260818, resampling unit = account for the outcome shares
# (decisions/0103), statistic = BOTH (decisions/0118).
#
# WHAT REPLACED WHAT, because the shape of the change matters more than the
# value. Until v1.5.0 this module held ARM_STATISTIC = {"a": "movements", "b":
# "levels", "sole": "levels"} -- A PER-ARM CHOICE, recorded because the spec did
# not fix it. There is no per-arm choice to record any more. The statistic is a
# VALUE THE SPEC FIXES, recorded the way B, the seed and the unit are recorded:
# at the point of use, in $.bootstrap_spec and in every $.bootstrap_settings
# entry.
#
# THE ORDER OF THIS TUPLE IS NOT MEANINGFUL AND IS NOT ASSERTED. The schema
# constrains the SET (two members, unique, both from the enum); checks S40 and
# S41 compare as sets. A ranked pair would say one is primary, and the ruling
# says NEITHER is presented as the design.
BOOTSTRAP_STATISTICS = ["levels", "movements"]

# The two names of the bootstrap elements the spec ranges over, so that
# $.bootstrap_spec's fixed and not-fixed lists can be checked as a PARTITION of
# a declared universe rather than read as two free-form arrays. An empty
# `fields_not_fixed_in_spec` is otherwise indistinguishable from a list nobody
# filled in -- CLAUDE.md, "an empty result and a clean result are the same value,
# and only the control knows which it produced". Check S40 asserts the partition.
BOOTSTRAP_FIELDS_CONSIDERED = ["B", "seed", "resampling_unit", "statistics"]

# WHICH STEP PUBLISHES EACH PER-ARM BLOCK. It is not always the step that owns
# the figure -- Step 8 owns the waterfall and Step 9 publishes it -- and under one
# file per step per arm (decisions/0109 §1) it is this map, not ownership, that
# says which file a block appears in. Since v1.4.0 it also says which ARM ENTRY a
# block appears in, because an arm entry's identity now includes its producing
# step (decisions/0111 E2).
#
# `action_type_counts` MOVED FROM step9 TO step13 at v1.4.0. decisions/0111 E1
# names it one of STEP 13's six non-headline outputs; the table said Step 9
# published it, and the disagreement was live -- the single-arm placeholder wrote
# the block while its own ownership table gave it to Step 9 (0111 §3, Q1).
BLOCK_PUBLISHER = {
    "waterfall": "step9",
    "abandonment_distribution": "step10",
    "liveness_exclusions": "step9",
    "d3_prime": "step13",
    "retained_by_air_period": "step9",
    "action_type_counts": "step13",
}

# The blocks that carry a HEADLINE payload rather than a per-arm block: an arm
# entry always has the slot, and the payload inside it is a real one only where
# that entry's producing step publishes a headline.
HEADLINE_PUBLISHERS = ("step9", "step13")

# STEP 13'S SIX NON-HEADLINE OUTPUTS (decisions/0111 E1). Each had ONE SLOT where
# TWO ARMS write, which forces the reconciliation decisions/0107 §3 forbids, so
# each takes per-arm nesting -- the same shape as its headline. The nesting is
# UNCONDITIONAL: no oneOf or anyOf may sit above a by_producing_arm container
# (decisions/0109 §4, machine-checked by S35), so a block that is not this
# entry's is OMITTED rather than wrapped in an absence branch, and check S36
# fails an entry that carries a block published by another step.
PER_ARM_NESTED_BLOCKS = (
    "d3_prime",
    "tested_ranges",
    "conclusions_surviving",
    "conclusions_not_surviving",
    "d2_recomputed_inside_this_arm",
    "action_type_counts",
)

# Top-level blocks whose publisher the spec fixes. Read by check S36's file leg.
# The registry blocks -- bootstrap settings, the population definitions, the
# sentinel scheme -- name no publisher and are not policed by it; that scope is
# stated rather than left to be inferred from a passing check.
# `subpopulation_cuts` is deliberately NOT here: Steps 11 and 12 BOTH write cuts
# into it, so the question "whose block is this?" has no single answer at the
# block level and is answered per ENTRY, by each cut's own producing_step. A
# publisher named here would have made one of the two steps' files illegal.
#
# `channel_classes` AND `discovery_channel_overlap` JOINED AT v1.5.0
# (decisions/0114 E8). They hold STEP 8's figures, and `channel_classes` was
# REQUIRED at the top level of every file: seven arm files, seven writers of a
# figure none of them produced, no precedence rule, no agreement check -- Q1's
# class at the top level and the FOURTH appearance of one-slot-vs-one-definition.
# The merged document carries them ONCE, filled at Step 13b from Step 8's
# artifact; arm files use the absence idiom. `discovery_channel_overlap` was
# checked rather than assumed and is the same shape, differing only in being
# optional, so the defect there was reachable rather than shipped.
TOP_LEVEL_PUBLISHER = {
    "tested_ranges": "step13",
    "variants": "step13",
    "channel_classes": "step13b",
    "discovery_channel_overlap": "step13b",
}

# What kind of document a file is. An ARM FILE holds one arm and is written by an
# isolated instance; the MERGED DOCUMENT holds both and is written by Step 13b.
DOCUMENT_ROLES = ["arm_file", "merged_document"]
ARMS_IN_FILE = ["one_arm", "both_arms"]

# The classes of quantity whose binding cluster the record actually states. A CI
# on a quantity class that is not here cannot be written, which is what stops a
# show-bound quantity inheriting `account` silently (decisions/0103 §2).
QUANTITY_CLASSES = ["outcome_shares", "window_w_percentile", "other_declared"]
RESAMPLING_UNITS = ["account", "show", "pair"]


def _count(desc: str) -> dict:
    return {
        "description": desc + "  [measurement slot: -999 in a placeholder]",
        "anyOf": [{"type": "integer", "minimum": 0}, {"const": SENT_C}],
        "x-measurement": True,
    }


def _percent(desc: str) -> dict:
    return {
        "description": desc + "  [measurement slot: -999.0 in a placeholder]",
        "anyOf": [{"type": "number", "minimum": 0, "maximum": 100}, {"const": SENT_P}],
        "x-measurement": True,
    }


def _text(desc: str, nullable: bool = False) -> dict:
    """A string slot whose content is run-specific and supplied by the writing step.

    Structural text -- definitions, refs, reasons that are identical in every
    file -- is deliberately NOT marked, because it is real in a placeholder too.
    """
    return {
        "type": ["string", "null"] if nullable else "string",
        "description": desc + "  [writer text: carries the placeholder prefix in a placeholder]",
        "x-writer-text": True,
    }


def _block_or_absence(props: dict, desc: str) -> dict:
    """A per-population container, or an explicit record that the whole block is absent.

    reviewer-engineering F1: three of the four required per-arm blocks have no
    producer at a non-primary arm, so requiring them unconditionally required
    more than the spec asks. The slot stays present either way, and an absence
    names the step that would have filled it.
    """
    return {
        "description": desc,
        "oneOf": [
            {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "properties": props,
            },
            {"$ref": "#/$defs/block_absence"},
        ],
    }


def _pp(desc: str) -> dict:
    return {
        "description": desc + "  [measurement slot: -999.0 in a placeholder]",
        "anyOf": [{"type": "number"}, {"const": SENT_P}],
        "x-measurement": True,
    }


def build_schema(provenance: dict | None = None) -> dict:
    d: dict = {}

    d["count"] = _count("A count of pairs, accounts or records.")
    d["percent"] = _percent("A percentage on [0, 100].")
    d["pp"] = _pp("A quantity in percentage points; may be zero or negative.")
    d["ratio"] = _pp("A dimensionless ratio.")
    d["integer_setting"] = {
        "description": "An integer run setting, e.g. a random seed."
        "  [measurement slot: -999 in a placeholder]",
        "anyOf": [{"type": "integer"}, {"const": SENT_C}],
        "x-measurement": True,
    }

    d["absence"] = {
        "type": "object",
        "description": (
            "An explicit record that a value is not here, and why. Never omit a slot and "
            "never write null: an absent field and an inapplicable one must not look alike "
            "(task-sheet.md Step 8b; decisions/0066 §3)."
        ),
        "additionalProperties": False,
        "required": ["status", "reason", "source"],
        "properties": {
            "status": {"enum": ABSENCE_STATUSES, "x-enum-id": "absence_status"},
            "reason": {"type": "string", "minLength": 20},
            "source": {"type": "string"},
            "decided_by": {"type": "string"},
        },
    }

    d["block_absence"] = {
        "type": "object",
        "description": (
            "An explicit record that a whole BLOCK is not here, naming the step that would "
            "have produced it. Added at v1.1.0 against reviewer-engineering's F1: three of "
            "the four per-arm blocks have no producer at a non-primary arm -- nothing in the "
            "spec produces a filter waterfall or an abandonment distribution for the "
            "premiere-anchored 91-day arm -- so requiring them unconditionally required more "
            "than the spec asks. The slot stays present and says who would have filled it, so "
            "'no producer' and 'not run yet' and 'superseded for this use' never look alike."
        ),
        "additionalProperties": False,
        "required": ["status", "reason", "source", "owning_step", "block_is_absent"],
        "properties": {
            "block_is_absent": {"const": True},
            "status": {
                "enum": [
                    "no_producer_in_spec",
                    "not_yet_written",
                    "superseded_for_this_purpose",
                    "structurally_absent",
                    "not_required_by_spec",
                    "awaiting_owner_step",
                    "not_a_dual_step",
                ],
                "x-enum-id": "absence_status",
            },
            "reason": {"type": "string", "minLength": 20},
            "source": {"type": "string"},
            "owning_step": {
                "oneOf": [
                    {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
                    {"const": "none"},
                ],
                "description": (
                    "The step that would write this block, or 'none' where the spec names no "
                    "producer for it here. 'none' is a finding about the spec, not a default."
                ),
            },
            "decided_by": {"type": "string"},
        },
    }

    d["search_record"] = {
        "type": "object",
        "description": (
            "What a list-shaped block searched, so that an EMPTY list and an UNSEARCHED list "
            "are distinguishable. Added at v1.1.0 against reviewer-engineering's F4: the "
            "validator treated a legitimately empty optional array as VACUOUS and failed it, "
            "which collapses 'no unreconciled divergence was found' into 'looked nowhere'. "
            "CLAUDE.md requires the control to DISTINGUISH those, so the file carries the "
            "coverage count and the checker reads it."
        ),
        "additionalProperties": False,
        "required": ["performed", "coverage_count", "what_was_searched", "owner_step"],
        "properties": {
            "performed": {
                "type": "boolean",
                "description": "False means nobody has looked yet; the list being empty says nothing.",
            },
            "coverage_count": {
                "$ref": "#/$defs/count",
                "description": (
                    "How many candidates were examined. A ZERO HERE WITH `performed` TRUE IS "
                    "ITSELF A FINDING and is now REJECTED rather than described: the schema's "
                    "own prose called it one while the file still validated, which is a "
                    "control asserted in a sentence and not built (reviewer-engineering M7). "
                    "The if/then below forbids it, and check S33 fails it with the site named."
                ),
            },
            "what_was_searched": _text("What was examined, in the writer's words."),
            "owner_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "empty_reason": {
                "type": ["string", "null"],
                "description": "Why the list is empty, required by check S17 when it is.",
                "x-writer-text": True,
            },
        },
        # A SEARCH THAT RAN AND EXAMINED NOTHING IS NOT A SEARCH. CLAUDE.md: a
        # check that finds nothing because it looked nowhere must FAIL, not pass.
        # The sentinel stays admissible, because a placeholder holds no counts.
        "if": {"properties": {"performed": {"const": True}}, "required": ["performed"]},
        "then": {
            "properties": {
                "coverage_count": {
                    "anyOf": [{"type": "integer", "minimum": 1}, {"const": SENT_C}],
                    "x-measurement": True,
                    "description": (
                        "With `performed` true this must be at least 1. Zero examined "
                        "candidates and a clean result are the same value, and only the "
                        "control knows which it produced."
                    ),
                }
            }
        },
    }

    d["endpoint"] = {
        "type": "object",
        "description": (
            "One end of a bound. Every endpoint states the population it is computed on and "
            "the size of that population, because an endpoint and the estimand it bounds must "
            "be on the same population (decisions/0047)."
        ),
        "additionalProperties": False,
        "required": [
            "percent", "numerator_pairs", "denominator_pairs",
            "population", "population_n", "population_label",
        ],
        "properties": {
            "percent": {"$ref": "#/$defs/percent"},
            "numerator_pairs": {"$ref": "#/$defs/count"},
            "denominator_pairs": {"$ref": "#/$defs/count"},
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            "population_n": {"$ref": "#/$defs/count"},
            "population_label": {
                "type": "string",
                "description": "Which row set: e.g. 'position 5' or 'post-liveness (position 7)'.",
            },
            "attainable": {"type": "boolean"},
            "note": _text("A note from the writer."),
        },
    }

    d["ci"] = {
        "type": "object",
        "description": (
            "A confidence interval. THE BOOTSTRAP IS FIXED IN ALL FOUR OF ITS ELEMENTS -- "
            "10,000 resamples, account level for the outcome shares, seed 20260818 "
            "(decisions/0103), and the statistic BOTH levels and paired movements "
            "(decisions/0118) -- and EVERY INTERVAL RECORDS ITS SEED, RESAMPLE COUNT, "
            "RESAMPLING UNIT AND STATISTIC AT THE POINT OF USE. They are written here as well "
            "as referenced, because the ruling says at the point of use and a reference is not "
            "that; check S23 asserts the inline values against the referenced registry entry, "
            "so the redundancy is checked rather than trusted. An interval is ONE of the two "
            "objects and says which; check S41 asserts that BOTH appear, PER (PRODUCING STEP, "
            "ARM), because a run that emits only one is INCOMPLETE rather than differently "
            "designed -- and the owner of an interval is a step and an arm together, since in "
            "the merged document one arm label covers several steps. ONE STEP IS EXEMPT AND "
            "THE EXEMPTION IS NAMED HERE RATHER THAN LEFT TO BE DISCOVERED: a Step 12 file "
            "mandates intervals nowhere (see $defs.ci_or_absence), so a Step 12 file carrying "
            "no interval declares that emptiness rather than failing to fill it. Human Lead "
            "ruling, 2026-08-19. THE EXEMPTION IS FROM PRODUCING INTERVALS, NOT FROM PRODUCING "
            "THEM COMPLETELY: a step that HAS published an interval owes both objects like any "
            "other, because it is then manufacturing nothing."
        ),
        "additionalProperties": False,
        "required": [
            "level_pct", "lower", "upper", "method", "bootstrap_ref",
            "B", "seed", "statistic", "resampling_unit", "quantity_class",
        ],
        "properties": {
            "level_pct": {"type": "number"},
            "lower": {"$ref": "#/$defs/percent"},
            "upper": {"$ref": "#/$defs/percent"},
            "method": {"type": "string"},
            "bootstrap_ref": {
                "type": "string",
                "description": "A key of $.bootstrap_settings. Referential integrity is check S3.",
            },
            "B": {
                "type": "integer",
                "minimum": 1,
                "description": "The resample count, at the point of use (decisions/0103).",
            },
            "seed": {
                "type": "integer",
                "description": "The seed, at the point of use. Its VALUE is arbitrary and its "
                               "FIXITY is the point: it is what makes the two arms comparable.",
            },
            "statistic": {
                "enum": BOOTSTRAP_STATISTICS,
                "x-enum-id": "bootstrap_statistic",
                "description": (
                    "WHICH OF THE TWO OBJECTS THIS INTERVAL IS, AT THE POINT OF USE. The "
                    "statistic is FIXED AS BOTH (decisions/0118): a run produces levels AND "
                    "paired movements, and this field says which one the reader is looking at. "
                    "It is single-valued HERE and plural in the registry, and that is the "
                    "distinction the ruling turns on -- A LEVEL AND A MOVEMENT ARE NEVER "
                    "COMPARED TO EACH OTHER, so an interval that did not say which it was "
                    "would be off by an order of magnitude with nothing to warn the reader. "
                    "Check S23 asserts this value is one the referenced registry entry "
                    "declares; check S41 asserts both values appear in the file, per "
                    "(producing step, arm) -- except in a file the spec asks for no interval "
                    "at all, which is Step 12's (Human Lead ruling, 2026-08-19); check S32 "
                    "asserts the referenced entry belongs to the arm that owns this payload. "
                    "NOTE THE CONSEQUENCE OF THE RULING FOR S32: "
                    + _REGISTRY_ARM_DIFFERENCE_FACT
                    + " -- and what it catches is an INCOHERENT reference rather than a "
                    "mislabel, because both sides are the writer's own declarations and a "
                    "coherent mislabel is unobservable to it."
                ),
            },
            "resampling_unit": {
                "enum": RESAMPLING_UNITS,
                "x-enum-id": "resampling_unit",
                "description": (
                    "THE BINDING CLUSTER IS NOT THE SAME FOR EVERY QUANTITY (decisions/0103 "
                    "§2). Account level is right for the outcome shares and would UNDERSTATE a "
                    "show-bound quantity such as W, whose interval is show-clustered. This is "
                    "an enum, not a constant, so a show-bound quantity says `show` rather than "
                    "inheriting `account` silently -- which was the whole mechanism the caution "
                    "relied on, and the previous schema pinned it to `account` by const."
                ),
            },
            "quantity_class": {
                "enum": QUANTITY_CLASSES,
                "x-enum-id": "quantity_class",
                "description": "A key of $.binding_clusters. Check S24 asserts the unit used "
                               "matches the binding cluster the record states for this class, "
                               "or that the disagreement is recorded and not reconciled.",
            },
            "unit_disagreement": {
                "type": "object",
                "description": (
                    "Present only where the unit used differs from the binding cluster for "
                    "this quantity class. Report a material disagreement; do not reconcile it."
                ),
                "additionalProperties": False,
                "required": ["binding_cluster", "unit_used", "material",
                             "reported_not_reconciled"],
                "properties": {
                    "binding_cluster": {"enum": RESAMPLING_UNITS, "x-enum-id": "resampling_unit"},
                    "unit_used": {"enum": RESAMPLING_UNITS, "x-enum-id": "resampling_unit"},
                    "material": {"type": "boolean"},
                    "reported_not_reconciled": {"const": True},
                    "note": _text("What the disagreement is and how large."),
                },
            },
            "note": _text("A note from the writer."),
        },
    }

    d["ci_or_absence"] = {
        "description": (
            "A confidence interval, or an explicit record that there is none. Added at "
            "v1.1.0 against reviewer-engineering's F3: the bootstrap ruling closes the "
            "'no settings exist yet' case, but a CI is still legitimately absent where the "
            "spec does not ask the writing step for one -- Step 12 lists every candidate cut "
            "and mandates intervals nowhere, and Step 13's per-arm sensitivity series is a "
            "series of shares, not of intervals. Requiring a CI everywhere would require more "
            "than the spec asks; omitting the slot would make 'not asked for' look like "
            "'forgotten'."
        ),
        "oneOf": [{"$ref": "#/$defs/ci"}, {"$ref": "#/$defs/absence"}],
    }

    d["share"] = {
        "type": "object",
        "description": (
            "An observed outcome share. This is a count on the sample, not a bound; the "
            "bounds live under the sibling `bounds` object."
        ),
        "additionalProperties": False,
        "required": [
            "value_percent", "numerator_pairs", "denominator_pairs",
            "on_population", "on_population_n", "on_population_label", "ci",
            "is_an_observed_count_not_a_bound",
        ],
        "properties": {
            "value_percent": {"$ref": "#/$defs/percent"},
            "numerator_pairs": {"$ref": "#/$defs/count"},
            "denominator_pairs": {"$ref": "#/$defs/count"},
            "on_population": {"enum": POPULATIONS, "x-enum-id": "population"},
            "on_population_n": {"$ref": "#/$defs/count"},
            "on_population_label": {"type": "string"},
            "ci": {"$ref": "#/$defs/ci_or_absence"},
            "is_an_observed_count_not_a_bound": {"const": True},
            "horizon_days": {
                "description": (
                    "The horizon the state is read over. Never-started is read at tau1 and "
                    "Continued at tau2, so the three shares are not measured alike and must "
                    "not be described as if they were."
                ),
                "anyOf": [{"type": "integer"}, {"const": SENT_C}],
                "x-measurement": True,
            },
            "note": _text("A note from the writer."),
        },
    }

    d["sub_interval_present"] = {
        "type": "object",
        "description": (
            "The conditional sub-interval: the share given that every never-started exclusion "
            "is a true decline. Its conditioning constrains the never-started exclusions and "
            "says nothing about the channel pairs, so its floor moves with the bound floor "
            "(decisions/0056)."
        ),
        "additionalProperties": False,
        "required": [
            "applicable", "floor", "ceiling", "width_pp",
            "conditioning_text", "constrains_never_started_exclusions",
            "says_nothing_about_channel_pairs", "coincides_with_bound",
        ],
        "properties": {
            "applicable": {"const": True},
            "floor": {"$ref": "#/$defs/endpoint"},
            "ceiling": {"$ref": "#/$defs/endpoint"},
            "width_pp": {"$ref": "#/$defs/pp"},
            "conditioning_text": _text("What the sub-interval conditions on."),
            "constrains_never_started_exclusions": {"$ref": "#/$defs/count"},
            "says_nothing_about_channel_pairs": {"$ref": "#/$defs/count"},
            "coincides_with_bound": {
                "type": "object",
                "description": (
                    "Whether this sub-interval coincides with its bound. Coincidence is "
                    "recorded as a measured fact, not by writing the same numbers twice "
                    "unremarked (decisions/0066 §3)."
                ),
                "additionalProperties": False,
                "required": ["value", "measured", "evidence"],
                "properties": {
                    "value": {"type": "boolean"},
                    "measured": {"const": True},
                    "evidence": _text("The evidence for the coincidence, or its absence."),
                },
            },
        },
    }

    d["sub_interval_absent"] = {
        "type": "object",
        "description": (
            "The never-started bound has no conditional sub-interval, structurally: the "
            "sub-interval conditions on that bound's own exclusion set. The field is present "
            "and says so, rather than being omitted."
        ),
        "additionalProperties": False,
        "required": ["applicable", "status", "reason", "source"],
        "properties": {
            "applicable": {"const": False},
            "status": {"const": "structurally_absent", "x-enum-id": "absence_status"},
            "reason": {"type": "string", "minLength": 20},
            "source": {"type": "string"},
        },
    }

    exclusions_covered = {
        "type": "object",
        "description": "The exclusion set this bound is taken over.",
        "additionalProperties": False,
        "required": ["total_pairs", "never_started_component", "started_and_left_component"],
        "properties": {
            "total_pairs": {"$ref": "#/$defs/count"},
            "never_started_component": {"$ref": "#/$defs/count"},
            "started_and_left_component": {"$ref": "#/$defs/count"},
            "accounts": {"$ref": "#/$defs/count"},
            "channel_pairs_conceded_by_the_floor": {"$ref": "#/$defs/count"},
        },
    }

    corner_table = {
        "type": "array",
        "description": (
            "The attainable-corner table. It is on the derived-figures list for both floors, "
            "so it has a slot rather than being recomputed by a consumer."
        ),
        "items": {
            "type": "object",
            "additionalProperties": False,
            "required": ["corner", "never_started_percent", "started_and_left_percent",
                         "continued_percent"],
            "properties": {
                "corner": {"type": "string"},
                "never_started_percent": {"$ref": "#/$defs/percent"},
                "started_and_left_percent": {"$ref": "#/$defs/percent"},
                "continued_percent": {"$ref": "#/$defs/percent"},
                "note": {"type": "string"},
            },
        },
    }

    def bound(sub_ref: str, title: str) -> dict:
        return {
            "type": "object",
            "description": title,
            "additionalProperties": False,
            "required": [
                "floor", "ceiling", "width_pp", "degenerate",
                "conditional_sub_interval", "scope_qualifier_ref", "exclusions_covered",
            ],
            "properties": {
                "floor": {"$ref": "#/$defs/endpoint"},
                "ceiling": {"$ref": "#/$defs/endpoint"},
                "width_pp": {
                    "$ref": "#/$defs/pp",
                    "description": (
                        "ceiling.percent - floor.percent. Always present. A width of 0.0 is a "
                        "measured zero-width bound and must not read as missing data; see "
                        "`degenerate`."
                    ),
                },
                "degenerate": {
                    "type": "boolean",
                    "description": "True iff the bound has zero width, i.e. floor == ceiling.",
                },
                "degenerate_reason": _text(
                    "Why the bound is degenerate. Required when `degenerate` is true.",
                    nullable=True,
                ),
                "conditional_sub_interval": {"$ref": sub_ref},
                "scope_qualifier_ref": {
                    "type": "string",
                    "description": (
                        "A key of $.scope_qualifiers. The qualifier travels with the bound "
                        "wherever the bound goes (decisions/0062); it is referenced, not "
                        "restated, so there is one definition of it."
                    ),
                },
                "exclusions_covered": exclusions_covered,
                "endpoints_attainable": {"type": "boolean"},
                "attainable_corners": corner_table,
                "note": _text("A note from the writer."),
            },
            "if": {"properties": {"degenerate": {"const": True}}, "required": ["degenerate"]},
            "then": {
                "required": ["degenerate_reason"],
                "properties": {"degenerate_reason": {"type": "string", "minLength": 20}},
            },
        }

    d["bound_no_subinterval"] = bound(
        "#/$defs/sub_interval_absent",
        "The never-started bound: floor, ceiling, and no conditional sub-interval.",
    )
    d["bound_with_subinterval"] = bound(
        "#/$defs/sub_interval_present",
        "The started-and-left bound: floor, ceiling and the conditional sub-interval.",
    )

    d["continued_bound"] = {
        "type": "object",
        "description": (
            "Continued has a ceiling, because any excluded pair may in truth be Continued. It "
            "is never emitted as a point: the floor slot holds an explicit not-published "
            "record, never a number (decisions/0050, 0052)."
        ),
        "additionalProperties": False,
        "required": ["ceiling", "floor", "must_not_be_read_as_a_point", "scope_qualifier_ref"],
        "properties": {
            "ceiling": {"$ref": "#/$defs/endpoint"},
            "floor": {"$ref": "#/$defs/absence"},
            "must_not_be_read_as_a_point": {"const": True},
            "scope_qualifier_ref": {"type": "string"},
            "exclusions_covered": exclusions_covered,
            "note": _text("A note from the writer."),
        },
    }

    d["ratio_block"] = {
        "type": "object",
        "description": (
            "A bound width divided by a sampling width. The two arms use two conventions and "
            "the spec forbids reconciling them, so the convention is a named input carried "
            "with the value (decisions/0058, 0063)."
        ),
        "additionalProperties": False,
        "required": ["value", "convention_label", "convention_definition",
                     "reconciled_with_other_arm"],
        "properties": {
            "value": {"$ref": "#/$defs/ratio"},
            "convention_label": {"type": "string"},
            "convention_definition": _text("The convention this arm uses, in its own words."),
            "numerator_definition": _text("What this arm puts in the numerator."),
            "denominator_definition": _text("What this arm puts in the denominator."),
            "reconciled_with_other_arm": {"const": False},
        },
    }

    d["ceilings_block"] = {
        "type": "object",
        "description": (
            "The three ceilings and the fact that they cannot all hold. `simultaneous` is "
            "const false in the schema, so no writer can emit three ceilings as simultaneous."
        ),
        "additionalProperties": False,
        "required": ["simultaneous", "sum_percent", "excess_pp", "excess_pairs",
                     "excess_mechanism_expression"],
        "properties": {
            "simultaneous": {"const": False},
            "sum_percent": {
                "description": "The three ceilings summed. Exceeds 100 by construction."
                "  [measurement slot: -999.0 in a placeholder]",
                "anyOf": [{"type": "number"}, {"const": SENT_P}],
                "x-measurement": True,
            },
            "excess_pp": {"$ref": "#/$defs/pp"},
            "excess_pairs": {"$ref": "#/$defs/count"},
            "excess_mechanism_expression": {
                "type": "string",
                "description": (
                    "The mechanism, not just the total: each never-started exclusion appears "
                    "in all three ceiling numerators and each started-and-left exclusion in "
                    "two."
                ),
            },
            "note": _text("A note from the writer."),
        },
    }

    d["step9_payload"] = {
        "type": "object",
        "description": (
            "Everything ONE producing arm computes for one population of one W arm. Step 9 is "
            "a dual step, and A DUAL STEP IS DIFFED BETWEEN TWO ARM FILES, BY THE HUMAN LEAD, "
            "BEFORE THE MERGE -- not inside one file. The claim that it was diffed IN this "
            "schema is RETIRED at v1.2.0 (decisions/0107): it had no writer, because two "
            "instances that never see each other's work cannot jointly produce one document, "
            "and no arm may be the merge writer without defeating what dual implementation "
            "exists to do. Each arm writes this subtree into ITS OWN file; the merged "
            "document, written by Step 13b, carries both subtrees so that where the arms "
            "legitimately differ -- the bound over sampling width ratios use two conventions "
            "-- both are held and neither is reconciled."
        ),
        "additionalProperties": False,
        "required": ["producing_arm", "written_by_step", "shares", "bounds",
                     "ceilings_cannot_all_hold", "written_by"],
        "properties": {
            "producing_arm": {
                "enum": ["a", "b", "sole"],
                "x-enum-id": "producing_arm",
                "description": (
                    "`sole` is the single-arm case. Added at v1.1.0 against "
                    "reviewer-engineering's F5: Steps 10, 11 and 12 are single-arm and were "
                    "being forced to name an `a` and a `b`. Step 9 and Step 13 are dual "
                    "(decisions/0103 §3) and use `a` and `b`."
                ),
            },
            "written_by_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": "Which step wrote this payload. Ownership is stated, never "
                               "inherited by whoever writes first (F9).",
            },
            "written_by": {"type": "string"},
            "merged_from": {
                "type": "string",
                "x-writer-text": True,
                "description": (
                    "WHICH SOURCE THIS PAYLOAD CAME FROM. Required in the merged document, "
                    "forbidden in an arm file (check S30), and it must name one of "
                    "$.document_scope.merge.sources_merged -- renamed from arm_files_merged at "
                    "v1.4.0, because the input list records SOURCES and one of them is not an "
                    "arm file at all (decisions/0111 E6). Added at v1.3.0 against "
                    "reviewer-engineering's M1: a merged document assembled from ONE arm file, "
                    "with the one payload deep-copied into the other arm's slot and relabelled, "
                    "validated clean and published that the arms agreed everywhere -- a FALSE "
                    "CLEAN in the block whose whole purpose is to report where they did not. "
                    "ISOLATION IS UNOBSERVABLE, BUT ARITY IS OBSERVABLE: two arms are two "
                    "payloads from two files, so each payload names its own file and check S30 "
                    "asserts that a block holding two arms names two DIFFERENT files."
                ),
            },
            "shares": {
                "type": "object",
                "additionalProperties": False,
                "required": OUTCOMES,
                "properties": {o: {"$ref": "#/$defs/share"} for o in OUTCOMES},
            },
            "bounds": {
                "description": (
                    "The three bounds, or a block absence. Absence is permitted because the "
                    "spec asks for the bounds at the headline arms and does not ask Step 13 "
                    "for a bound at each of its eight W arms; requiring them everywhere "
                    "requires more than the spec asks (F1). Check S22 forbids an absence here "
                    "on the primary headline arm."
                ),
                "oneOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": OUTCOMES,
                        "properties": {
                            "never_started": {"$ref": "#/$defs/bound_no_subinterval"},
                            "started_and_left": {"$ref": "#/$defs/bound_with_subinterval"},
                            "continued": {"$ref": "#/$defs/continued_bound"},
                        },
                    },
                    {"$ref": "#/$defs/block_absence"},
                ],
            },
            "ceilings_cannot_all_hold": {
                "oneOf": [
                    {"$ref": "#/$defs/ceilings_block"},
                    {"$ref": "#/$defs/block_absence"},
                ],
                "description": "Absent only where `bounds` is absent: with no ceilings there "
                               "is no three-ceiling sum. Check S22 ties the two together.",
            },
            "bound_over_sampling_width_ratios": {
                "description": (
                    "The bound-over-sampling-width ratios, or an absence. The ratios exist to "
                    "hold TWO conventions the spec forbids reconciling, so a single-arm step "
                    "has no second convention to hold against and writes an absence with the "
                    "not_a_dual_step status -- which is the status reviewer-engineering's F5 "
                    "found missing: `structurally_absent` already means something else here."
                ),
                "oneOf": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "never_started": {"$ref": "#/$defs/ratio_block"},
                            "started_and_left": {"$ref": "#/$defs/ratio_block"},
                            "started_and_left_sub_interval": {"$ref": "#/$defs/ratio_block"},
                        },
                    },
                    {"$ref": "#/$defs/absence"},
                ],
            },
            "spec_choices_this_arm_made": {
                "type": "array",
                "description": "Choices the spec does not fix, named by the arm that made them.",
                "items": _text("One choice the spec does not fix."),
            },
        },
    }

    _payload_or_absence = {
        "oneOf": [{"$ref": "#/$defs/step9_payload"}, {"$ref": "#/$defs/absence"}]
    }
    _is_dual = {
        "properties": {"step_dual_status": {"const": "dual"}},
        "required": ["step_dual_status"],
    }
    _is_single = {
        "properties": {"step_dual_status": {"const": "single_arm"}},
        "required": ["step_dual_status"],
    }
    _holds_one = {
        "properties": {"arms_in_this_file": {"const": "one_arm"}},
        "required": ["arms_in_this_file"],
    }
    _holds_both = {
        "properties": {"arms_in_this_file": {"const": "both_arms"}},
        "required": ["arms_in_this_file"],
    }
    def _by_producing_arm(payload_or_absence: dict, subject: str) -> dict:
        """One per-arm container, over any payload shape.

        FACTORED AT v1.4.0 (decisions/0111 E1). Step 13's six non-headline
        outputs each had ONE SLOT where TWO ARMS write, which forces the
        reconciliation decisions/0107 §3 forbids, so each takes the same
        container its headline takes. One factory rather than six hand-written
        objects, because six copies of one shape is six places a rule is stated
        and one place it will be forgotten -- and check S35 requires EVERY member
        of the family to be reachable without a oneOf or anyOf above it, which is
        only checkable if they are one shape.
        """
        return dict(_bpa_body, description=_bpa_body["description"] + f"  SUBJECT: {subject}",
                    properties=dict(_bpa_body["properties"],
                                    arms={
                                        "type": "object",
                                        "additionalProperties": False,
                                        "properties": {
                                            "a": payload_or_absence,
                                            "b": payload_or_absence,
                                            "sole": payload_or_absence,
                                        },
                                    }))

    _bpa_body = {
        "type": "object",
        "description": (
            "The producing arms of this block, AS TWO SEPARATE FACTS. SPLIT AT v1.2.0 under "
            "decisions/0107 §4. Until then one field, `dual_status`, carried both -- whether "
            "the STEP is dual AND whether the file holds two payloads -- so `dual` required "
            "both arms.a and arms.b and A DUAL STEP'S SINGLE-ARM FILE HAD NO LEGAL SHAPE AT "
            "ALL, while the ruling requires exactly that file. The two facts are now "
            "`step_dual_status`, a property of the STEP, and `arms_in_this_file`, a property "
            "of THIS FILE. A dual step's arm file names which arm it holds in `arm_held`; the "
            "merged document holds both under arms.a and arms.b; a single-arm step writes one "
            "payload under arms.sole. THE SINGLE-ARM BRANCH IS NOT LOOSENED BY THE SPLIT: a "
            "single-arm step may never hold two arms, which is the opposite defect and would "
            "otherwise validate silently. DUAL STEPS ARE 9 AND 13 (decisions/0103 §3); Steps "
            "10, 11 and 12 are single-arm. The field was RENAMED rather than redefined in "
            "place, so a writer still carrying the old `dual_status` fails loudly against "
            "additionalProperties instead of silently acquiring a new meaning under an "
            "unchanged key."
        ),
        "additionalProperties": False,
        "required": ["step_dual_status", "arms_in_this_file", "producing_step", "arms"],
        "properties": {
            "step_dual_status": {
                "enum": ["dual", "single_arm"],
                "x-enum-id": "step_dual_status",
                "description": (
                    "FACT ONE, ABOUT THE STEP: whether the step that wrote this block runs "
                    "twice in isolation. It does not change with the file it is written into."
                ),
            },
            "arms_in_this_file": {
                "enum": ARMS_IN_FILE,
                "x-enum-id": "arms_in_this_file",
                "description": (
                    "FACT TWO, ABOUT THIS FILE: whether this file holds one arm's payload or "
                    "both. One arm in an arm file, both only in the merged document Step 13b "
                    "produces. A dual step written into an arm file is `dual` and `one_arm` at "
                    "once, which is the combination the previous single field could not "
                    "express."
                ),
            },
            "arm_held": {
                "enum": ["a", "b", "sole"],
                "x-enum-id": "arm_held",
                "description": (
                    "WHICH arm this file holds. Required when arms_in_this_file is one_arm -- "
                    "a dual step's single-arm file must NAME the arm, not merely be shaped "
                    "like one -- and forbidden when both_arms, where the arms keys carry it "
                    "and a single name could only contradict one of them. Check S28 asserts "
                    "it against the arms keys and against $.document_scope.arm."
                ),
            },
            "producing_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": (
                    "WHICH STEP WROTE THIS BLOCK -- and, since v1.3.0, the field "
                    "`step_dual_status` is READ AGAINST IT. Duality is a fixed fact of the "
                    "spec, so the two cannot disagree: the allOf below pins each named step's "
                    "status by const."
                ),
            },
            "step_dual_status_source": {
                "type": "string",
                "description": "Where the duality is ruled. Step 13's is decisions/0103 §3, "
                               "which resolved a live CLAUDE.md / task-sheet.md conflict.",
            },
            "arms": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "a": _payload_or_absence,
                    "b": _payload_or_absence,
                    "sole": _payload_or_absence,
                },
            },
        },
        "allOf": [
            {
                # A single-arm step: one payload, under `sole`, in every kind of
                # file. This branch is NARROWED by the split, never loosened --
                # letting a single-arm step's file claim two arms is the mirror
                # defect of the one the split fixes (decisions/0107 §4).
                "if": _is_single,
                "then": {
                    "required": ["arm_held"],
                    "properties": {
                        "arms_in_this_file": {"const": "one_arm"},
                        "arm_held": {"const": "sole"},
                        "arms": {
                            "required": ["sole"],
                            "allOf": [
                                {"not": {"required": ["a"]}},
                                {"not": {"required": ["b"]}},
                            ],
                        },
                    },
                },
            },
            {
                # A dual step in an ARM FILE: exactly one of a, b, named.
                "if": {"allOf": [_is_dual, _holds_one]},
                "then": {
                    "required": ["arm_held"],
                    "properties": {
                        "arm_held": {"enum": ["a", "b"]},
                        "arms": {
                            "allOf": [
                                {"anyOf": [{"required": ["a"]}, {"required": ["b"]}]},
                                {"not": {"required": ["a", "b"]}},
                                {"not": {"required": ["sole"]}},
                            ]
                        },
                    },
                },
            },
            {
                # A dual step in the MERGED DOCUMENT: both arms, neither named
                # at block level, no `sole`.
                "if": {"allOf": [_is_dual, _holds_both]},
                "then": {
                    "not": {"required": ["arm_held"]},
                    "properties": {
                        "arms": {"required": ["a", "b"], "not": {"required": ["sole"]}},
                    },
                },
            },
        ] + [
            # DUALITY IS READ AGAINST THE STEP, NOT DECLARED FREELY (v1.3.0,
            # reviewer-engineering M2). `step_dual_status` sat two keys away from
            # `producing_step` and was never compared with it, so a Step 9 block
            # could relabel itself single_arm and validate -- and the merged
            # document's dropped-arm clause, guarded on `dual`, would then never
            # fire. The existing selftest case mutated SHAPE, which is the half
            # the split already guarded; this is the half it did not.
            {
                "if": {
                    "properties": {"producing_step": {"const": step}},
                    "required": ["producing_step"],
                },
                "then": {"properties": {"step_dual_status": {"const": status}}},
            }
            for step, status in STEP_DUALITY.items()
        ],
    }

    d["by_producing_arm"] = _by_producing_arm(
        _payload_or_absence,
        "the headline payload -- the outcome shares, the two bounds and the ratios",
    )

    d["population_block"] = {
        "type": "object",
        "description": (
            "One population of one arm. APPLY and DERIV are separate arithmetic under separate "
            "keys, never one field carrying a population flag (decisions/0066 §3)."
        ),
        "additionalProperties": False,
        "required": ["population", "definition", "n_position_5", "n_post_liveness",
                     "by_producing_arm"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            "definition": _text("The population, restated by the writer at the point of use."),
            "n_position_5": {
                "$ref": "#/$defs/count",
                "description": (
                    "The row set the bounds are stated on. Each W arm re-censors, so the arms "
                    "do not share a denominator."
                ),
            },
            "n_post_liveness": {
                "$ref": "#/$defs/count",
                "description": (
                    "The row set the published shares are stated on. It differs from "
                    "n_position_5, which is why every share and every endpoint names its own "
                    "population label."
                ),
            },
            "populations_differ_note": _text(
                "Why n_position_5 and n_post_liveness differ, in the writer's words."
            ),
            "by_producing_arm": {"$ref": "#/$defs/by_producing_arm"},
        },
    }

    d["waterfall_position"] = {
        "type": "object",
        "additionalProperties": False,
        "required": ["position", "filter", "n_in", "n_out", "removed", "inert",
                     "outcome_conditional"],
        "properties": {
            "position": {"type": "integer", "minimum": 1, "maximum": 7},
            "filter": {"enum": FILTER_NAMES, "x-enum-id": "filter"},
            "n_in": {"$ref": "#/$defs/count"},
            "n_out": {"$ref": "#/$defs/count"},
            "removed": {"$ref": "#/$defs/count"},
            "inert": {
                "type": "boolean",
                "description": (
                    "True where the position cannot fire on this frame. An unlabelled "
                    "always-zero filter reads as evidence the rule found nothing when it is "
                    "evidence the rule cannot fire (decisions/0079)."
                ),
            },
            "inert_reason": _text(
                "Why this position cannot fire. Required when `inert` is true.", nullable=True
            ),
            "outcome_conditional": {
                "type": "boolean",
                "description": "True at position 6 under the adopted liveness rule.",
            },
            "sub_lines": {
                "type": "array",
                "description": "Right-censoring publishes as two lines; they go here.",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["label", "removed"],
                    "properties": {
                        "label": _text("The label for this sub-line."),
                        "removed": {"$ref": "#/$defs/count"},
                        "n_out": {"$ref": "#/$defs/count"},
                        "note": _text("A note from the writer."),
                    },
                },
            },
            "note": _text("A note from the writer."),
        },
        "if": {"properties": {"inert": {"const": True}}, "required": ["inert"]},
        "then": {
            "required": ["inert_reason"],
            "properties": {"inert_reason": {"type": "string", "minLength": 20}},
        },
    }

    d["waterfall_block"] = {
        "type": "object",
        "description": (
            "The filter waterfall for one population of one arm, in the mandated order. The "
            "final row set commutes but the per-filter sample sizes do not, so the order is "
            "part of the figure (decisions/0029)."
        ),
        "additionalProperties": False,
        "required": ["population", "written_by_step", "order_ref", "positions",
                     "monotone_check"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "figures_owned_by_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": (
                    "WHO OWNS THE FIGURES, where that is not who writes them here. Step 8 "
                    "produces the waterfall and Step 9 publishes it into this schema; until "
                    "v1.4.0 `written_by_step` carried Step 8 while $.block_ownership said Step "
                    "9 published it, so one block answered two different questions with one "
                    "field and disagreed with the registry."
                ),
            },
            "order_ref": {"type": "string"},
            "positions": {
                "type": "array",
                "minItems": 7,
                "maxItems": 7,
                "items": {"$ref": "#/$defs/waterfall_position"},
            },
            "monotone_check": {
                "type": "object",
                "additionalProperties": False,
                "required": ["operator", "result", "positions_checked"],
                "properties": {
                    "operator": {
                        "const": ">=",
                        "description": (
                            "Coded >=, not >, so a filter position that legitimately removes "
                            "nothing does not fail an assertion (decisions/0047)."
                        ),
                    },
                    "result": {"type": "boolean"},
                    "positions_checked": {"$ref": "#/$defs/count"},
                },
            },

        },
    }

    d["p_at_bound_block"] = {
        "type": "object",
        "description": (
            "TWO DIFFERENT FALSE CLASSES. They are named apart and both are emitted. A "
            "consumer that reads 'the FALSE class is empty' and provisions a two-valued column "
            "is wrong by the whole of `column_cardinalities.false_count` (decisions/0099 §2)."
        ),
        "additionalProperties": False,
        "required": ["column_cardinalities", "coextensivity_gap", "two_classes_note"],
        "properties": {
            "column_cardinalities": {
                "type": "object",
                "description": (
                    "CLASS 2 -- the emitted column's own values. THE COLUMN IS THREE-VALUED: "
                    "TRUE on the rows where p reached its bound, FALSE on the remaining "
                    "started-and-left rows, and null everywhere p is null. All three counts "
                    "are required, so the column cannot be provisioned as two-valued."
                ),
                "additionalProperties": False,
                "required": ["true_count", "false_count", "null_count", "total_rows"],
                "properties": {
                    "true_count": {"$ref": "#/$defs/count"},
                    "false_count": {"$ref": "#/$defs/count"},
                    "null_count": {"$ref": "#/$defs/count"},
                    "total_rows": {"$ref": "#/$defs/count"},
                    "identity_holds": {"type": "boolean"},
                    "false_is_the_ordinary_case": {"const": True},
                },
            },
            "coextensivity_gap": {
                "type": "object",
                "description": (
                    "CLASS 1 -- the gap between the two mechanisms of the superseded "
                    "definition. This is the class that is empty; it is not the column's FALSE "
                    "value. Four cells plus the coverage count, because an empty result and a "
                    "clean result are the same value."
                ),
                "additionalProperties": False,
                "required": ["in_both", "saturated_not_final", "final_not_saturated",
                             "in_neither", "rows_examined"],
                "properties": {
                    "p_equals_one_total": {"$ref": "#/$defs/count"},
                    "in_both": {"$ref": "#/$defs/count"},
                    "saturated_not_final": {"$ref": "#/$defs/count"},
                    "final_not_saturated": {"$ref": "#/$defs/count"},
                    "in_neither": {"$ref": "#/$defs/count"},
                    "rows_examined": {"$ref": "#/$defs/count"},
                    "is_empty": {"type": "boolean"},
                },
            },
            "two_classes_note": _text(
                "The two FALSE classes, named apart, in the writer's words."
            ),
            "construction_links": {
                "type": "array",
                "description": (
                    "The chain has three links and only the first two are construction; the "
                    "third is a frame property and is measured (decisions/0085 §4)."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["link", "kind"],
                    "properties": {
                        "link": {"type": "string"},
                        "kind": {"enum": ["construction", "measured"], "x-enum-id": "link_kind"},
                        "measured_value": _text(
                            "What was measured for a link whose kind is `measured`.", nullable=True
                        ),
                    },
                },
            },
        },
    }

    d["abandonment_block"] = {
        "type": "object",
        "description": (
            "The abandonment distribution for one population of one arm. p is the rank form "
            "and is defined only on started-and-left rows."
        ),
        "additionalProperties": False,
        "required": ["population", "row_set", "row_set_label", "n_rows_in_row_set",
                     "written_by_step", "n_started_and_left", "p_definition", "bin_unit",
                     "histograms", "named_categories", "p_at_bound", "comparability_caveat"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            # A SINGLE-ARM STEP'S BLOCK CAME FROM A FILE TOO. Step 10 writes this
            # block, its arm is `sole` by construction, and until v1.4.0 it
            # carried no merge provenance at all -- so its declared input was
            # named by nothing and S30's new input -> payload leg had nothing to
            # find (decisions/0111 E3b).
            "merged_from": {
                "type": "string",
                "x-writer-text": True,
                "description": "Which input file this block came from; required in the merged "
                               "document and forbidden in an arm file (check S30).",
            },
            "row_set": {
                "enum": ["position_5", "post_liveness", "other"],
                "x-enum-id": "row_set",
                "description": (
                    "WHICH ROW SET THIS BLOCK IS MEASURED ON. Added at v1.1.0 against "
                    "reviewer-engineering's F2: `endpoint` and `share` both require a row-set "
                    "label and this block carried none, while Step 8 measured p_at_bound, "
                    "n_started_and_left, the histogram and the p = 1.0 residual on FOUR row "
                    "sets -- APPLY and DERIV, each at position 5 and post-liveness -- with "
                    "different values on each. A population name alone does not identify "
                    "which of the two a figure came from."
                ),
            },
            "row_set_label": {
                "type": "string",
                "description": "The row set in words, e.g. 'position 5' or "
                               "'post-liveness (position 7)'.",
            },
            "n_rows_in_row_set": {
                "$ref": "#/$defs/count",
                "description": "The size of the row set this block is measured on, so a "
                               "consumer can tell which of the four cells it is reading.",
            },
            "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "n_started_and_left": {"$ref": "#/$defs/count"},
            "p_definition": {
                "const": "p = |{e in E2 : e <= max(A_H)}| / L2",
                "description": (
                    "The rank form. p = m_H / L2 is NOT the rule and must not be reinstated."
                ),
            },
            "p_raw_ratio_form_withdrawn": {"const": True},
            "p_is_null_off_started_and_left": {"const": True},
            "bin_unit": {
                "const": "fraction_of_season",
                "description": (
                    "p is a fraction of a season, not a count of episodes. A histogram pooled "
                    "across shows with very different L2 does not have comparable bins."
                ),
            },
            "histograms": {
                "type": "array",
                "minItems": 1,
                "description": (
                    "ONE ENTRY PER STRATUM. Added at v1.1.0 against reviewer-engineering's "
                    "F7: there was one histogram slot per population per arm carrying an "
                    "`l2_stratum` label, so stratification was anticipated and could not be "
                    "expressed -- a second stratum had nowhere to go and the label could only "
                    "ever describe the single pooled histogram. Step 10 is told not to read a "
                    "p histogram across shows with very different L2 as if the bins were "
                    "comparable, which is an instruction to stratify. The unstratified case is "
                    "one entry with stratum kind `all`."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["stratum", "bin_edges_p", "counts"],
                    "properties": {
                        "stratum": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["kind", "label"],
                            "properties": {
                                "kind": {
                                    "enum": ["all", "l2_stratum", "other"],
                                    "x-enum-id": "stratum_kind",
                                },
                                "label": {"type": "string"},
                                "l2_min": {"type": ["integer", "null"]},
                                "l2_max": {"type": ["integer", "null"]},
                                "definition": _text("How this stratum is defined."),
                            },
                        },
                        "bin_edges_p": {
                            "type": "array",
                            "description": "Ascending edges on [0, 1]; len(counts) + 1 of them. "
                                           "Bin definitions are structure, not measurements. "
                                           "Check S26 asserts the two lengths agree.",
                            "items": {"type": "number"},
                        },
                        "counts": {"type": "array", "items": {"$ref": "#/$defs/count"}},
                        "n_rows": {"$ref": "#/$defs/count"},
                    },
                },
            },
            "named_categories": {
                "type": "object",
                "description": (
                    "First-episode, mid-season and near-finale drops, plus the p = 1.0 "
                    "residual, which is its own named category and is NOT part of near-finale."
                ),
                "additionalProperties": False,
                "required": ["first_episode", "mid_season", "near_finale", "p_equals_1_residual"],
                "properties": {
                    k: {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["count", "definition"],
                        "properties": {
                            "count": {"$ref": "#/$defs/count"},
                            "share_percent": {"$ref": "#/$defs/percent"},
                            "definition": _text("How this category is defined by the writer."),
                        },
                    }
                    for k in ("first_episode", "mid_season", "near_finale", "p_equals_1_residual")
                },
            },
            "p_equals_1_residual_is_separate_from_near_finale": {"const": True},
            "p_at_bound": {"$ref": "#/$defs/p_at_bound_block"},
            "amendment_shift": {
                "type": "object",
                "description": (
                    "The amendment moves the pairs that got furthest out of started-and-left, "
                    "so it shifts this chart earlier. A reader must not attribute the shift to "
                    "behaviour."
                ),
                "additionalProperties": False,
                "required": ["direction", "pairs_moved", "note"],
                "properties": {
                    "direction": {"enum": ["earlier", "later", "none"],
                                  "x-enum-id": "shift_direction"},
                    "pairs_moved": {"$ref": "#/$defs/count"},
                    "note": _text("A note from the writer."),
                },
            },
            "comparability_caveat": _text("The caveat on pooling p across shows."),
            "no_specific_episode_claimed": {"const": True},
        },
    }

    d["liveness_exclusions_block"] = {
        "type": "object",
        "description": (
            "The liveness exclusion count for this arm. The rule has no parameter of its own "
            "but is fully determined by W, so the count is reported at every arm and the "
            "coupling is visible."
        ),
        "additionalProperties": False,
        "required": ["total_pairs", "never_started_component", "started_and_left_component"],
        "properties": {
            "total_pairs": {"$ref": "#/$defs/count"},
            "never_started_component": {"$ref": "#/$defs/count"},
            "started_and_left_component": {"$ref": "#/$defs/count"},
            "accounts": {"$ref": "#/$defs/count"},
            "silence_test_alone": {
                "$ref": "#/$defs/count",
                "description": (
                    "Excluded by the silence test on its own, before the NOT Continued "
                    "conjunct spares any. Without it line 6 cannot be read as a marginal cost."
                ),
            },
            "spared_by_not_continued": {"$ref": "#/$defs/count"},
            "identity": {"type": "string"},
            "pair_level_not_account_level": {"type": "boolean"},
            "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "figures_owned_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
        },
    }

    d["d3_prime_block"] = {
        "type": "object",
        "description": (
            "D3'S CLEARED COUNT AND SHARE FOR ONE POPULATION OF ONE ARM. Added at v1.1.0 "
            "against reviewer-engineering's F6: Step 13 is required to run D3' at EVERY arm "
            "and report each arm's own cleared count and share, and the schema had nowhere to "
            "put them -- their only home was the free-string `note`, which turns a mandated "
            "per-arm figure into prose a consumer cannot read. D3's clearance contains W, so "
            "the cleared subpopulation changes with the arm and a single figure carried from "
            "the adopted arm would misdescribe every other one. The share is measured on Step "
            "8's right-censored population at THIS arm, which is why the population label is "
            "required beside it."
        ),
        "additionalProperties": False,
        "required": ["population", "cleared_count", "cleared_share_percent",
                     "population_label", "written_by_step", "producing_arm"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            # PER-ARM SINCE v1.4.0 (decisions/0111 E1): D3' is one of Step 13's
            # six non-headline outputs, and Step 13 is dual, so the payload names
            # its arm and the file it was merged from like any other.
            "producing_arm": {
                "enum": ["a", "b", "sole"],
                "x-enum-id": "producing_arm",
            },
            "merged_from": {
                "type": "string",
                "x-writer-text": True,
                "description": "Which input file this payload came from; required in the "
                               "merged document and forbidden in an arm file (check S30).",
            },
            "cleared_count": {"$ref": "#/$defs/count"},
            "cleared_share_percent": {"$ref": "#/$defs/percent"},
            "denominator_pairs": {"$ref": "#/$defs/count"},
            "population_label": {
                "type": "string",
                "description": "The right-censored population at this arm, named at the point "
                               "of use. The series is not comparable across arms without it.",
            },
            "H_days_held_constant": {
                "type": "integer",
                "description": "H is held constant across every arm that varies W, or D3' and "
                               "D8 are not comparable between arms.",
            },
            "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "note": _text("A note from the writer."),
        },
    }

    d["air_period_block"] = {
        "type": "object",
        "description": (
            "Retained pairs per air period after right-censoring, for one population of one "
            "arm. The aggregate hides a cohort-asymmetric loss, so the per-period breakdown "
            "is required at EVERY arm (decisions/0033). MOVED to the arm at v1.1.0: it used "
            "to sit inside the waterfall block, and once a waterfall may legitimately be "
            "absent -- reviewer-engineering's F1 -- a mandate required at every arm would "
            "have had nowhere to go at the arms where it is absent. It is the same figure in "
            "one place, not a second copy."
        ),
        "additionalProperties": False,
        "required": ["population", "rows", "written_by_step"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
            "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "figures_owned_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "measured_after": {
                "type": "string",
                "description": "Which filter position the retention is measured after. The "
                               "mandated order censors the position-4 output, and a count "
                               "measured after a different position is a different figure.",
            },
            "rows": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["air_period", "retained_pairs"],
                    "properties": {
                        "air_period": _text("The air period this row covers."),
                        "retained_pairs": {"$ref": "#/$defs/count"},
                        "entering_pairs": {"$ref": "#/$defs/count"},
                        "retained_share_percent": {"$ref": "#/$defs/percent"},
                    },
                },
            },
        },
    }

    d["headline"] = {
        "type": "object",
        "additionalProperties": False,
        "required": POPULATIONS,
        "properties": {p: {"$ref": "#/$defs/population_block"} for p in POPULATIONS},
    }

    # ------------------------------------------------------------------
    # STEP 13'S SIX NON-HEADLINE OUTPUTS, PER PRODUCING ARM (decisions/0111 E1).
    # Each of these had ONE SLOT where TWO ARMS write. Step 13 is dual
    # (decisions/0103 §3), so the merge would have had to drop an arm or
    # reconcile the two -- and decisions/0107 §3 forbids exactly that. The fix is
    # the same WIDENING the two earlier appearances took, because widening keeps
    # ONE DEFINITION PER FIGURE.
    #
    # THE NESTING IS UNCONDITIONAL, and that is not incidental: decisions/0109 §4
    # records that the `step_dual_status` rename fails loudly ONLY because no
    # oneOf sits above by_producing_arm, so none of these containers may be
    # wrapped in an absence branch. A block that this entry's producing step does
    # not publish is OMITTED, its publisher is named in $.block_ownership, and
    # check S36 fails an entry that carries one that is not its own.
    # ------------------------------------------------------------------
    _provenance_fields = {
        "producing_arm": {
            "enum": ["a", "b", "sole"],
            "x-enum-id": "producing_arm",
            "description": "Which arm produced this payload; it must equal the key it sits "
                           "under (check S28).",
        },
        "written_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
        "merged_from": {
            "type": "string",
            "x-writer-text": True,
            "description": (
                "Which input file this payload came from. Required in the merged document and "
                "forbidden in an arm file (check S30), and it must name one of "
                "$.document_scope.merge.sources_merged."
            ),
        },
    }

    d["action_type_counts_payload"] = {
        "type": "object",
        "description": (
            "Per-pair counts by action type, for one producing arm. `action` is record-level "
            "and the row is a pair, so there is no row-level action value (decisions/0070 "
            "ruling 4). PER-ARM SINCE v1.4.0 (decisions/0111 E1)."
        ),
        "additionalProperties": False,
        "required": ["producing_arm", "written_by_step", "counts"],
        "properties": dict(
            _provenance_fields,
            counts={
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/count"},
            },
            note=_text("A note from the writer."),
        ),
    }

    d["tested_ranges_payload"] = {
        "type": "object",
        "description": (
            "The ranges this arm actually tested. An interactive Step 16 binds its controls to "
            "these so no reader can drive it somewhere that was never tested. PER-ARM SINCE "
            "v1.4.0: two arms may test different ranges, and one slot could hold only one "
            "answer (decisions/0111 E1)."
        ),
        "additionalProperties": False,
        "required": ["producing_arm", "written_by_step", "ranges"],
        "properties": dict(
            _provenance_fields,
            ranges={
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["values"],
                    "properties": {
                        "values": {"type": "array"},
                        "min": {"type": ["number", "string", "null"]},
                        "max": {"type": ["number", "string", "null"]},
                        "source": {"type": "string"},
                    },
                },
            },
            note=_text("A note from the writer."),
        ),
    }

    d["conclusions_payload"] = {
        "type": "object",
        "description": (
            "The conclusions this arm found surviving, or not surviving, a variation. PER-ARM "
            "SINCE v1.4.0 (decisions/0111 E1): the two arms may reach different lists, and a "
            "single list would have to drop one arm's."
        ),
        "additionalProperties": False,
        "required": ["producing_arm", "written_by_step", "conclusions"],
        "properties": dict(
            _provenance_fields,
            conclusions={
                "type": "array",
                "items": _text("One conclusion, in the writing arm's words."),
            },
            note=_text("A note from the writer."),
        ),
    }

    d["d2_recomputed_payload"] = {
        "type": "object",
        "description": (
            "D2's max() split recomputed inside this variation, for one producing arm. THREE "
            "categories, not two: finale binds, S1 completion binds, both bind -- a tie is its "
            "own category, not a tiebreak, and the count is NOT population-invariant "
            "(decisions/0070 ruling 5; decisions/0092 §3). PER-ARM SINCE v1.4.0."
        ),
        "additionalProperties": False,
        "required": ["producing_arm", "written_by_step"],
        "properties": dict(
            _provenance_fields,
            finale_binds={"$ref": "#/$defs/count"},
            s1_completion_binds={"$ref": "#/$defs/count"},
            both_bind={"$ref": "#/$defs/count"},
            note=_text("A note from the writer."),
        ),
    }

    d["by_producing_arm_d3_prime"] = _by_producing_arm(
        {"oneOf": [{"$ref": "#/$defs/d3_prime_block"}, {"$ref": "#/$defs/absence"}]},
        "D3's cleared count and share at this arm, for one population",
    )
    d["by_producing_arm_action_counts"] = _by_producing_arm(
        {"oneOf": [{"$ref": "#/$defs/action_type_counts_payload"},
                   {"$ref": "#/$defs/absence"}]},
        "the per-pair counts by action type",
    )
    d["by_producing_arm_tested_ranges"] = _by_producing_arm(
        {"oneOf": [{"$ref": "#/$defs/tested_ranges_payload"}, {"$ref": "#/$defs/absence"}]},
        "the tested ranges",
    )
    d["by_producing_arm_conclusions"] = _by_producing_arm(
        {"oneOf": [{"$ref": "#/$defs/conclusions_payload"}, {"$ref": "#/$defs/absence"}]},
        "a list of conclusions surviving, or not surviving, a variation",
    )
    d["by_producing_arm_d2_recomputed"] = _by_producing_arm(
        {"oneOf": [{"$ref": "#/$defs/d2_recomputed_payload"}, {"$ref": "#/$defs/absence"}]},
        "D2's three-category max() split recomputed inside this variation",
    )

    d["arm_entry"] = {
        "type": "object",
        "description": (
            "ONE ENTRY PER (W_days, clock_origin, producing_step, adopted_rule_revision) -- see "
            "$.arm_key. THE PRODUCING STEP JOINED THE KEY AT v1.4.0 (decisions/0111 E2) AND THE "
            "ADOPTED-RULE REVISION AT v1.5.0 (decisions/0114 E14). Step 9's W = 108 and Step "
            "13's W = 108 are DIFFERENT MEASUREMENTS OF ONE SETTING and both must exist; so are "
            "two runs at one setting under different rule revisions. Each is the "
            "(W_days, clock_origin) collision one dimension further out and each takes the same "
            "fix -- ADD THE MISSING IDENTITY DIMENSION. It is NOT resolved by restricting which "
            "step may occupy a shared W value: that would make the schema decide an ownership "
            "question the spec does not, and would drop a measurement rather than hold it. AN "
            "ENTRY CARRIES THE BLOCKS ITS OWN PRODUCING STEP PUBLISHES AND NO OTHERS: "
            "$.block_ownership names each block's publisher, and check S36 fails an entry that "
            "carries one that is not its own. There is NO liveness threshold and no threshold "
            "may appear as a key."
        ),
        "additionalProperties": False,
        "required": ["arm_id", "W_days", "H_days", "clock_origin", "producing_step",
                     "adopted_rule_revision", "in_arm_grid", "headline"],
        "properties": {
            "arm_id": {"type": "string", "pattern": r"^W\d+_"},
            "adopted_rule_revision": {
                "type": "integer",
                "minimum": 1,
                "description": (
                    "THE FOURTH KEY DIMENSION (decisions/0114 E14): the revision of the adopted "
                    "contamination rule this measurement was taken under. It is READ from the "
                    "adopted-rule file at write time, never typed -- $.adopted_rule_revision "
                    "records which file and which key it came from, and check S37 asserts every "
                    "entry against it. The dimension has been occupied once already: "
                    "processed/step5/adopted_rule.json carried revision-3 figures against the "
                    "approved revision-6 rule."
                ),
            },
            "producing_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": (
                    "WHICH STEP'S MEASUREMENT THIS ENTRY IS. Part of the entry key since "
                    "v1.4.0. Step 9 and Step 13 both measure the headline at W = 108, and "
                    "before this field the two collided in one slot -- four payloads, two "
                    "slots. The blocks this entry may carry are exactly the blocks this step "
                    "publishes."
                ),
            },
            "W_days": {"type": "integer", "minimum": 1},
            "H_days": {
                "type": "integer",
                "minimum": 1,
                "description": "Held constant across every arm that varies W.",
            },
            "clock_origin": {
                "enum": ["s2_finale", "s2_premiere"],
                "x-enum-id": "clock_origin",
                "description": (
                    "Where T0 is anchored. The eight grid arms are finale-anchored. Step 9's "
                    "91-day Netflix arm is premiere-anchored and is a different measurement, "
                    "not the same one at another window length -- so it cannot share an entry "
                    "with the finale-anchored W = 91 arm."
                ),
            },
            "clock_origin_note": _text("What this arm's clock is anchored on."),
            "in_arm_grid": {"type": "boolean"},
            "is_primary_headline": {"type": "boolean"},
            "headline": {"$ref": "#/$defs/headline"},
            "waterfall": _block_or_absence(
                {p: {"$ref": "#/$defs/waterfall_block"} for p in POPULATIONS},
                "The filter waterfall, per population. Step 8 produces it; nothing in the "
                "spec produces one for a premiere-anchored arm, so the block may be an "
                "explicit absence naming that (F1). Check S22 forbids an absence on the "
                "primary headline arm WHERE A PRODUCER EXISTS AT THAT ARM, and requires one "
                "where none does -- publisher rows key on ARM IDENTITY, not producing step "
                "alone, and ABSENCE IS STATED, NEVER SILENT (decisions/0114 E13).",
            ),
            "abandonment_distribution": _block_or_absence(
                {p: {
                    "oneOf": [
                        {
                            "type": "array",
                            "minItems": 1,
                            "items": {"$ref": "#/$defs/abandonment_block"},
                            "description": "ONE ENTRY PER ROW SET (F2). The four cells the "
                                           "record requires are APPLY and DERIV, each at "
                                           "position 5 and post-liveness.",
                        },
                        {"$ref": "#/$defs/block_absence"},
                    ]
                } for p in POPULATIONS},
                "The abandonment distribution, per population, one entry per row set. Step 10 "
                "produces it at the headline arm; no step produces it at every W arm.",
            ),
            "liveness_exclusions": _block_or_absence(
                {p: {
                    "oneOf": [
                        {"$ref": "#/$defs/liveness_exclusions_block"},
                        {"$ref": "#/$defs/block_absence"},
                    ]
                } for p in POPULATIONS},
                "The liveness exclusion count, per population. The per-population slot may "
                "carry an absence in its own right: the DERIV per-arm series is recorded as "
                "SUPERSEDED FOR THIS PURPOSE, so a schema that demands a number in that slot "
                "demands a superseded one (F1).",
            ),
            "d3_prime": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "description": (
                    "D3's cleared count and share at this arm, per population (F6), PER "
                    "PRODUCING ARM since v1.4.0 (decisions/0111 E1). Step 13 is dual and runs "
                    "D3' at every arm, so one slot here would have been one slot where two "
                    "arms write. Present only in an entry whose producing step is Step 13's; "
                    "check S36 fails it anywhere else."
                ),
                "properties": {
                    p: {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["by_producing_arm"],
                        "properties": {
                            "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_d3_prime"},
                        },
                    } for p in POPULATIONS
                },
            },
            "retained_by_air_period": _block_or_absence(
                {p: {
                    "oneOf": [
                        {"$ref": "#/$defs/air_period_block"},
                        {"$ref": "#/$defs/block_absence"},
                    ]
                } for p in POPULATIONS},
                "Retained pairs per air period after right-censoring, at this arm, per "
                "population -- required at every arm because the censoring loss is "
                "cohort-asymmetric and widens with W.",
            ),
            "action_type_counts": {
                "type": "object",
                "additionalProperties": False,
                "required": ["by_producing_arm"],
                "description": (
                    "Per-pair counts by action type, aggregated, PER PRODUCING ARM since "
                    "v1.4.0 (decisions/0111 E1). `action` is record-level and the row is a "
                    "pair, so there is no row-level action value; Step 13's arm reads these "
                    "counts, and Step 13 is dual, so one slot would be one slot where two arms "
                    "write."
                ),
                "properties": {
                    "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_action_counts"},
                },
            },
            "note": _text("A note from the writer."),
        },
    }

    d["variant_entry"] = {
        "type": "object",
        "description": (
            "A Step 13 arm that varies something other than W. THE ARM ENTRY KEY IS "
            "(W_days, clock_origin, producing_step, adopted_rule_revision) -- see $.arm_key -- "
            "and NONE of its four fields distinguishes a non-W variation, so such a variation "
            "cannot be an arm entry without colliding: it lives here and names the arm it is a "
            "variation of. "
            "CORRECTED AT v1.5.0 (decisions/0114 E10). This description said 'the entry key is "
            "W alone plus the clock origin' -- THE PRE-E2 TWO-FIELD KEY, superseded by "
            "decisions/0111 E2 and again by 0114 E14, and live on propagation surface 6 while "
            "the rest of the schema carried the current one. A description is what a writer "
            "reads before it reads a check."
        ),
        "additionalProperties": False,
        "required": ["variant_id", "axis", "level", "base_arm_id", "producing_step",
                     "adopted_rule_revision", "headline"],
        "properties": {
            "variant_id": {"type": "string"},
            "adopted_rule_revision": {
                "type": "integer",
                "minimum": 1,
                "description": (
                    "The adopted-rule revision this variation was measured under, stated for "
                    "the same reason the arm entry states it (decisions/0114 E14) and asserted "
                    "against $.adopted_rule_revision by check S37."
                ),
            },
            "producing_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": (
                    "Which step's measurement this variant is, stated for the same reason an "
                    "arm entry states it (decisions/0111 E2). Every variant here is Step 13's; "
                    "the field exists so that is a fact the file records rather than one a "
                    "reader infers from the container it sits in."
                ),
            },
            "axis": {
                "enum": [
                    "s1_completion_threshold",
                    "s1_completion_date_definition",
                    "action_type_evidence",
                    "other",
                ],
                "x-enum-id": "variant_axis",
            },
            "level": {"type": "string"},
            "base_arm_id": {"type": "string"},
            "headline": {"$ref": "#/$defs/headline"},
            # ALL FOUR PER PRODUCING ARM SINCE v1.4.0 (decisions/0111 E1). Each
            # was one slot where two arms write, and Step 13 is dual.
            "d2_recomputed_inside_this_arm": {
                "type": "object",
                "additionalProperties": False,
                "required": ["by_producing_arm"],
                "properties": {
                    "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_d2_recomputed"},
                },
            },
            "d3_prime": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "description": "D3' inside this variation, where the variation re-censors "
                               "(F6), per population and per producing arm.",
                "properties": {
                    p: {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["by_producing_arm"],
                        "properties": {
                            "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_d3_prime"},
                        },
                    } for p in POPULATIONS
                },
            },
            "conclusions_surviving": {
                "type": "object",
                "additionalProperties": False,
                "required": ["by_producing_arm"],
                "properties": {
                    "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_conclusions"},
                },
            },
            "conclusions_not_surviving": {
                "type": "object",
                "additionalProperties": False,
                "required": ["by_producing_arm"],
                "properties": {
                    "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_conclusions"},
                },
            },
        },
    }

    d["subpopulation_cut"] = {
        "type": "object",
        "description": (
            "A recomputation of the headline on a subpopulation: Step 11's discovery channels "
            "and Step 12's segment cuts. Every candidate considered is written here, not only "
            "the one that showed a pattern."
        ),
        "additionalProperties": False,
        "required": ["cut_id", "dimension", "level", "base_arm_id", "producing_step",
                     "adopted_rule_revision", "headline", "candidate_considered"],
        "properties": {
            "cut_id": {"type": "string"},
            "adopted_rule_revision": {
                "type": "integer",
                "minimum": 1,
                "description": (
                    "The adopted-rule revision this cut was measured under (decisions/0114 "
                    "E14), asserted against $.adopted_rule_revision by check S37."
                ),
            },
            "producing_step": {
                "enum": WRITER_STEPS,
                "x-enum-id": "writer_step",
                "description": (
                    "Which step's measurement this cut is. Steps 11 and 12 both write cuts "
                    "here, and until v1.4.0 nothing in the file said which -- so a merge could "
                    "declare Step 12's file among its inputs while carrying nothing from it, "
                    "and no check could see the gap (decisions/0111 E3b)."
                ),
            },
            "dimension": {
                "enum": [
                    "discovery_channel",
                    "origin",
                    "gap_length_between_seasons",
                    "s1_episode_count",
                    "user_tenure",
                    "other",
                ],
                "x-enum-id": "cut_dimension",
            },
            "level": {
                "type": "string",
                "description": (
                    "For discovery_channel the levels are channel_a, channel_b, both and "
                    "neither. Discovery channel is two booleans on the analysis table, not one "
                    "categorical, so the overlap has its own level rather than being dropped "
                    "or assigned arbitrarily (decisions/0070 ruling 3)."
                ),
            },
            "base_arm_id": {"type": "string"},
            "headline": {"$ref": "#/$defs/headline"},
            "candidate_considered": {"const": True},
            "selected_by_human_lead": {"type": "boolean"},
            "agreement_kind": {
                "enum": [
                    "genuinely_similar",
                    "not_distinguishable_at_this_n",
                    "diverge",
                    "not_yet_assessed",
                ],
                "x-enum-id": "agreement_kind",
                "description": (
                    "Step 11 must state whether 'agree' means genuinely similar or merely not "
                    "distinguishable at this sample size. It is a field, not caption prose."
                ),
            },
            "agreement_statement": _text("The agreement statement, in the writer's words."),
            "where_it_holds": _text("Where the pattern holds."),
            "where_it_breaks": _text("Where the pattern breaks."),
        },
    }

    schema: dict = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": SCHEMA_ID,
        "title": "Season 2 abandonment study -- Step 16 results schema",
        "description": (
            "The single output schema. Steps 9 through 13 write into it DIRECTLY, each ARM "
            "into its own file, and STEP 16 RENDERS FROM THE MERGED DOCUMENT that Step 13b "
            "builds from those files after the Human Lead has diffed the dual pairs "
            "(decisions/0107). Both kinds of file are instances of this one schema; "
            "$.document_scope says which kind a file is, and it is the first thing to read. "
            "There is no conversion layer: a conversion layer is a second definition of every "
            "figure. Validate with src/step8b_validate.py, which implements the JSON Schema "
            "subset used here plus the cross-field checks the schema language cannot express."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "schema_id", "placeholder", "generated_by", "document_scope",
            "sentinels",
            "arm_key", "adopted_rule_revision", "arm_grid_days", "populations",
            "scope_qualifiers",
            "bootstrap_spec", "binding_clusters", "bootstrap_settings", "step_duality",
            "block_ownership",
            "channel_classes", "arms",
            "spec_choices_made_by_step_8b", "known_limits_of_this_schema",
        ],
        "properties": {
            "schema_version": {"const": SCHEMA_VERSION},
            "schema_id": {"const": SCHEMA_ID},
            "placeholder": {
                "type": "boolean",
                "description": (
                    "TOP-LEVEL FLAG A CONSUMER CANNOT MISS. True means every measurement slot "
                    "in this file holds a sentinel and nothing in it is a measurement. A "
                    "placeholder that reads as data is the failure mode."
                ),
            },
            "placeholder_notice": {
                "type": "object",
                "description": "Present iff `placeholder` is true; forbidden otherwise.",
                "additionalProperties": False,
                "required": ["banner", "is_placeholder", "do_not_publish",
                             "every_measurement_slot_is_a_sentinel"],
                "properties": {
                    "banner": {"type": "string"},
                    "is_placeholder": {"const": True},
                    "do_not_publish": {"const": True},
                    "every_measurement_slot_is_a_sentinel": {"const": True},
                    "how_to_tell": {"type": "string"},
                    "generated_for": {"type": "string"},
                },
            },
            "generated_by": {
                "type": "object",
                "description": (
                    "A committed generated file states what generated it and when; a generated "
                    "file without its provenance is worse than no file, because it is trusted."
                ),
                "additionalProperties": False,
                "required": ["generator", "generator_sha256_12", "generated_at_utc",
                             "host_step", "written_by"],
                "properties": {
                    "generator": {"type": "string"},
                    "generator_sha256_12": {"type": "string"},
                    "generated_at_utc": {"type": "string"},
                    "build_tag": {"type": "string"},
                    "git_head_short": {"type": "string"},
                    "host_step": {"type": "string"},
                    "written_by": {"type": "string"},
                    "inputs": {"type": "array", "items": {"type": "string"}},
                },
            },
            "document_scope": {
                "type": "object",
                "description": (
                    "WHAT KIND OF DOCUMENT THIS IS, AND WHOSE. Added at v1.2.0 under "
                    "decisions/0107. ONE FILE PER ARM: each arm writes its own document and NO "
                    "ARM WRITES INTO A DOCUMENT ANOTHER ARM WRITES INTO, because arm isolation "
                    "is the MECHANISM of dual implementation rather than a side effect of it. "
                    "The merged reader-facing document is produced by a separate named step -- "
                    "STEP 13b, owner Human Lead -- after both arms have landed and been "
                    "DIFFED: it is the diff, not the merge, that is the dual control, and the "
                    "diff happens between two files. Only the merged document may hold two "
                    "arms of a dual step, and only it may carry the blocks marked "
                    "merged_document_only in $.block_ownership. Checks S28 and S29 enforce "
                    "both, which is what stops an arm file masquerading as a merged one."
                ),
                "additionalProperties": False,
                "required": ["role", "producing_step", "arm", "source"],
                "properties": {
                    "role": {
                        "enum": DOCUMENT_ROLES,
                        "x-enum-id": "document_role",
                        "description": (
                            "`arm_file` -- one arm's own document, written by an isolated "
                            "instance that has not seen any other arm's work. "
                            "`merged_document` -- the Step 13b output, the only document that "
                            "reads both arms and the only one permitted to."
                        ),
                    },
                    "producing_step": {
                        "enum": WRITER_STEPS,
                        "x-enum-id": "writer_step",
                        "description": (
                            "The step whose output this document IS, which is not necessarily "
                            "the generator recorded in $.generated_by -- a placeholder is "
                            "generated by Step 8b and shows the shape of another step's "
                            "document. A merged document's producing step is a Human Lead step; "
                            "an arm file's is not, and that is the predicate check S17 uses."
                        ),
                    },
                    "arm": {
                        "enum": ["a", "b", "sole", None],
                        "x-enum-id": "document_arm",
                        "description": (
                            "Which arm this document holds: `a` or `b` for an arm of a dual "
                            "step, `sole` for a single-arm step's own document, and null in "
                            "the merged document, which holds all of them."
                        ),
                    },
                    "merge": {
                        "type": "object",
                        "description": (
                            "Present only in the merged document. Required there, because a "
                            "merged file that does not record what it merged, or that the arms "
                            "were diffed before it was built, cannot be told from an arm file "
                            "that grew an extra arm."
                        ),
                        "additionalProperties": False,
                        "required": ["owner_step", "owner_role", "sources_merged",
                                     "diff", "blocks_only_the_merge_may_fill",
                                     "source"],
                        "properties": {
                            "owner_step": {"const": "step13b"},
                            "owner_role": {"type": "string"},
                            "sources_merged": {
                                "type": "array",
                                "minItems": 1,
                                "uniqueItems": True,
                                "description": (
                                    "ONE ENTRY PER SOURCE. RENAMED FROM `arm_files_merged` AT "
                                    "v1.4.0 (decisions/0111 E6): THE INPUT LIST RECORDS "
                                    "SOURCES, NOT ONLY ARM FILES. Seven of them are arm files, "
                                    "one per step per arm (decisions/0109 §1): Step 9 writes "
                                    "two, Step 13 writes two, Steps 10, 11 and 12 write one "
                                    "each. THE EIGHTH IS STEP 14's `limitations`, which is a "
                                    "NAMED NON-ARM-FILE SOURCE WITH ITS OWN PROVENANCE ENTRY -- "
                                    "Step 14 delivers a limits section rather than a schema "
                                    "file, decisions/0109 moved Step 13b after it precisely so "
                                    "that block could be filled, and a ten-item bias ledger "
                                    "that must not be netted cannot arrive in the "
                                    "reader-facing document with no recorded provenance. It has "
                                    "NO ARM, and `arm` is null there rather than absent. The "
                                    "key was RENAMED rather than widened in place, so a merge "
                                    "still emitting the old key fails loudly against "
                                    "additionalProperties instead of silently supplying a list "
                                    "that no longer means what it says. Check S30 asserts BOTH "
                                    "directions: every payload names a declared source, AND "
                                    "every declared source is named by at least one payload."
                                ),
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["file_label", "producing_step", "arm",
                                                 "source_kind"],
                                    "properties": {
                                        "file_label": {
                                            "type": "string",
                                            "x-writer-text": True,
                                            "description": (
                                                "How this source is named. Payloads reference "
                                                "it by this label in `merged_from`."
                                            ),
                                        },
                                        "source_kind": {
                                            "enum": ["arm_file", "non_arm_file"],
                                            "x-enum-id": "source_kind",
                                            "description": (
                                                "`arm_file` -- one step's output for one arm, "
                                                "written against this schema. `non_arm_file` -- "
                                                "a source that is not a schema file at all, "
                                                "which is what Step 14's limits section is."
                                            ),
                                        },
                                        "producing_step": {
                                            "enum": WRITER_STEPS, "x-enum-id": "writer_step",
                                        },
                                        "arm": {"enum": ["a", "b", "sole", None],
                                                "x-enum-id": "producing_arm_or_none",
                                                "description": (
                                                    "The arm this source is, or null where the "
                                                    "source has none. A non-arm-file source has "
                                                    "no arm, and null says so rather than the "
                                                    "field being dropped: an absent field and "
                                                    "an inapplicable one must not look alike."
                                                )},
                                        "step_dual_status": {
                                            "enum": ["dual", "single_arm"],
                                            "x-enum-id": "step_dual_status",
                                        },
                                        "fills_blocks": {
                                            "type": "array",
                                            "items": {"type": "string"},
                                            "description": (
                                                "Which blocks of the merged document this "
                                                "source supplies. Stated for a non-arm-file "
                                                "source, whose payloads are not per-arm and so "
                                                "cannot be found by walking the arm keys."
                                            ),
                                        },
                                        "source": {"type": "string"},
                                    },
                                    "allOf": [{
                                        "if": {
                                            "properties": {
                                                "source_kind": {"const": "non_arm_file"}},
                                            "required": ["source_kind"],
                                        },
                                        "then": {
                                            "required": ["fills_blocks"],
                                            "properties": {"arm": {"const": None}},
                                        },
                                        "else": {
                                            "properties": {
                                                "arm": {"enum": ["a", "b", "sole"]}},
                                        },
                                    }],
                                },
                            },
                            "diff": {
                                "type": "object",
                                "description": (
                                    "THE DIFF, AS A RECORD RATHER THAN AS A SENTENCE. It "
                                    "replaces `diff_precedes_merge: true`, retired at v1.3.0: "
                                    "reviewer-engineering judged that flag to be doing no work, "
                                    "because it was 'not a fact the file records, a sentence "
                                    "the schema requires the file to contain' -- a const true "
                                    "that every writer emits and no reader can check. What "
                                    "replaces it is checkable: WHICH PAIRS were diffed, naming "
                                    "two DIFFERENT input files per dual step; HOW MANY figures "
                                    "were compared, which may not be zero; and HOW MANY "
                                    "divergences were found, which must equal the number of "
                                    "entries in $.cross_arm_divergences. A merge assembled "
                                    "from one arm file cannot fill this without naming a "
                                    "second file that does not exist. Check S30."
                                ),
                                "additionalProperties": False,
                                "required": ["performed_by", "pairs_diffed", "figures_compared",
                                             "divergences_found", "record"],
                                "properties": {
                                    "performed_by": {
                                        "const": "human_lead",
                                        "description": (
                                            "The diff is the Human Lead's and no arm may "
                                            "perform it: it is the diff, not the merge, that "
                                            "is the dual control."
                                        ),
                                    },
                                    "pairs_diffed": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["producing_step", "arm_a_file",
                                                         "arm_b_file"],
                                            "properties": {
                                                "producing_step": {
                                                    "enum": WRITER_STEPS,
                                                    "x-enum-id": "writer_step",
                                                },
                                                "arm_a_file": {"type": "string",
                                                               "x-writer-text": True},
                                                "arm_b_file": {"type": "string",
                                                               "x-writer-text": True},
                                                "note": _text("A note from the writer."),
                                            },
                                        },
                                    },
                                    "figures_compared": {"$ref": "#/$defs/count"},
                                    "divergences_found": {"$ref": "#/$defs/count"},
                                    "record": _text(
                                        "Where the diff itself is recorded, outside this file."
                                    ),
                                },
                            },
                            "blocks_only_the_merge_may_fill": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "source": {"type": "string"},
                        },
                    },
                    "also_written_by_steps": {
                        "type": "array",
                        "items": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
                        "description": (
                            "OTHER STEPS THAT WRITE INTO THIS FILE -- AND IN AN ARM FILE THERE "
                            "ARE NONE. Human Lead ruling, decisions/0109 §1: granularity is ONE "
                            "FILE PER STEP PER ARM, resolving decisions/0107's own §1-vs-§6 "
                            "ambiguity in favour of §6, because §1 would require Step 10's "
                            "output to be DUPLICATED into two arm files -- two copies of one "
                            "figure, the defect the no-conversion-layer rule exists to prevent. "
                            "So an arm file's list is EMPTY and check S28 asserts it, together "
                            "with the stronger clause that every payload in an arm file names "
                            "the file's own producing step. Until v1.3.0 this placeholder pair "
                            "took OPPOSITE sides of that ambiguity: the merged document listed "
                            "seven inputs (§6) while the arm file named two extra writers (§1). "
                            "A Human Lead step here would be the merge arriving through the "
                            "side door, and it fails under both readings."
                        ),
                    },
                    "isolation_rule": {"type": "string"},
                    "note": _text("A note from the writer about this document's scope."),
                    "source": {"type": "string"},
                },
                "allOf": [
                    {
                        "if": {
                            "properties": {"role": {"const": "merged_document"}},
                            "required": ["role"],
                        },
                        "then": {
                            "required": ["merge"],
                            "properties": {
                                "arm": {"const": None},
                                "producing_step": {"enum": HUMAN_LEAD_STEPS},
                            },
                        },
                        "else": {
                            "not": {"required": ["merge"]},
                            "properties": {
                                "arm": {"enum": ["a", "b", "sole"]},
                                "producing_step": {"not": {"enum": HUMAN_LEAD_STEPS}},
                            },
                        },
                    },
                ],
            },
            "sentinels": {
                "type": "object",
                "description": "Reserved values. They may appear only in a placeholder.",
                "additionalProperties": False,
                "required": ["count", "percent", "string_prefix", "rule"],
                "properties": {
                    "count": {"const": SENT_C},
                    "percent": {"const": SENT_P},
                    "string_prefix": {"const": PH},
                    "rule": {"type": "string"},
                },
            },
            "arm_key": {
                "type": "object",
                "description": (
                    "What identifies an arm entry. There is no liveness threshold: one was "
                    "derived three times and deleted, and the adopted rule is parameter-free. "
                    "The key has grown three times and each growth ADDED A SETTING THE "
                    "MEASUREMENT WAS TAKEN UNDER that the key could not see: the clock origin "
                    "(decisions/0102), the producing step (0111 E2) and the adopted-rule "
                    "revision (0114 E14)."
                ),
                "additionalProperties": False,
                "required": ["fields", "note", "no_liveness_threshold"],
                "properties": {
                    "fields": {"const": ["W_days", "clock_origin", "producing_step",
                                         "adopted_rule_revision"]},
                    "note": {"type": "string"},
                    "no_liveness_threshold": {"const": True},
                },
            },
            "adopted_rule_revision": {
                "type": "object",
                "description": (
                    "WHERE THE FOURTH KEY DIMENSION WAS READ FROM (decisions/0114 E14). The "
                    "revision is READ from the adopted-rule file at write time, never typed: a "
                    "typed revision is a second definition of the rule's version, and the "
                    "defect this study has hit most often is two definitions of one figure. "
                    "The registry names the file, the key inside it and the file's hash, so a "
                    "reader can go and check rather than trust. Check S37 asserts every arm, "
                    "variant and cut entry against it."
                ),
                "additionalProperties": False,
                "required": ["revision", "source_file", "source_key", "source_sha256_12",
                             "read_not_typed"],
                "properties": {
                    "revision": {"type": "integer", "minimum": 1},
                    "source_file": {"type": "string"},
                    "source_key": {"type": "string"},
                    "source_sha256_12": {"type": "string"},
                    "read_not_typed": {"const": True},
                    "how_it_is_read": {"type": "string"},
                    "why_it_is_in_the_key": {"type": "string"},
                    "revisions_present": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 1},
                        "minItems": 1,
                        "uniqueItems": True,
                        "description": (
                            "MERGED DOCUMENT ONLY: the revisions its entries were measured "
                            "under. The merge assembles files written at different times, so "
                            "'this document's revision' is not one number and the set is "
                            "enumerated rather than assumed away. In an arm file the field is "
                            "absent -- one file is one run, and one run is one revision."
                        ),
                    },
                    "source": {"type": "string"},
                },
            },
            "arm_grid_days": {
                "type": "array",
                "description": "The fixed W grid. Two instances on different grids produce "
                               "tables that cannot be diffed at all.",
                "items": {"type": "integer"},
                "minItems": 1,
                "uniqueItems": True,
            },
            "populations": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "properties": {
                    p: {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["label", "definition", "source"],
                        "properties": {
                            "label": {"type": "string"},
                            "definition": {"type": "string"},
                            "source": {"type": "string"},
                            "reference_n_at_the_adopted_arm": {"$ref": "#/$defs/count"},
                        },
                    }
                    for p in POPULATIONS
                },
            },
            "scope_qualifiers": {
                "type": "object",
                "description": (
                    "One definition of each qualifier, referenced from every bound. Any table "
                    "or note that carries the bound carries the qualifier."
                ),
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["text", "covering_with_respect_to", "covering_is_exhaustive",
                                 "open_across", "source"],
                    "properties": {
                        "text": {"type": "string"},
                        "covering_with_respect_to": {"type": "string"},
                        "covering_is_exhaustive": {"type": "boolean"},
                        "open_across": {"type": "array", "items": {"type": "string"}},
                        "stopping_rule": {"type": "string"},
                        "source": {"type": "string"},
                    },
                },
            },
            "bootstrap_spec": {
                "type": "object",
                "description": (
                    "WHAT THE SPEC FIXES, IN ONE PLACE. Human Lead rulings, 2026-08-18 "
                    "(decisions/0103 §1) and 2026-08-19 (decisions/0118): 10,000 resamples, "
                    "resampled at the ACCOUNT level for the outcome shares, seed 20260818, and "
                    "the statistic BOTH levels and paired movements -- identical for both arms. "
                    "ALL FOUR ELEMENTS ARE NOW FIXED; none is recorded as a per-arm choice. The "
                    "seed's VALUE is arbitrary and its FIXITY is the point -- without a fixed "
                    "seed a difference between the arms could be sampling noise rather than a "
                    "divergence, and the dual control rests on that distinction. THE STATISTIC "
                    "IS RECORDED THE WAY B AND THE SEED ARE, AS A VALUE, in `statistics` below "
                    "-- not as a declaration that a choice exists. `fields_considered` names "
                    "the universe the two lists partition, so that an EMPTY "
                    "`fields_not_fixed_in_spec` is established rather than merely empty."
                ),
                "additionalProperties": False,
                "required": ["B", "seed", "resampling_unit_for_outcome_shares", "statistics",
                             "identical_for_both_arms", "fields_considered",
                             "fields_fixed_in_spec", "fields_not_fixed_in_spec", "source"],
                "properties": {
                    "B": {"type": "integer", "minimum": 1},
                    "seed": {"type": "integer"},
                    "resampling_unit_for_outcome_shares": {
                        "enum": RESAMPLING_UNITS, "x-enum-id": "resampling_unit"
                    },
                    "statistics": {
                        "type": "array",
                        "items": {"enum": BOOTSTRAP_STATISTICS,
                                  "x-enum-id": "bootstrap_statistic"},
                        "minItems": 2,
                        "maxItems": 2,
                        "uniqueItems": True,
                        "description": (
                            "THE STATISTIC, AS A VALUE. It is BOTH objects (decisions/0118), so "
                            "the value is the pair and the shape here requires both to be "
                            "present -- a file cannot record one and call the other a design "
                            "choice. ORDER IS NOT MEANINGFUL and is not asserted: neither "
                            "object is presented as *the* design. The pair is a SET constraint "
                            "rather than a const on an ordered array, so a writer that lists "
                            "them the other way round is correct rather than wrong."
                        ),
                    },
                    "identical_for_both_arms": {"const": True},
                    "seed_value_is_arbitrary_its_fixity_is_the_point": {"const": True},
                    "fields_considered": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1,
                        "uniqueItems": True,
                        "description": (
                            "The bootstrap elements this record ranges over. The fixed and "
                            "not-fixed lists must PARTITION it -- disjoint, and together equal "
                            "to it -- which is what check S40 asserts. Without it, an empty "
                            "not-fixed list is indistinguishable from an unfilled one."
                        ),
                    },
                    "fields_fixed_in_spec": {"type": "array", "items": {"type": "string"},
                                             "uniqueItems": True},
                    "fields_not_fixed_in_spec": {
                        "type": "array",
                        "items": {"type": "string"},
                        "uniqueItems": True,
                        "description": (
                            "Which elements the spec leaves open. IT IS EMPTY AS OF v1.6.0 "
                            "(decisions/0118) and the emptiness is checked, not assumed: S40 "
                            "asserts it against `fields_considered` and asserts by name that "
                            "the statistic is not in it. The array is kept rather than removed "
                            "because a future element could reopen it, and a slot that exists "
                            "and is empty is readable where a deleted slot is not."
                        ),
                    },
                    "why_account_level": {"type": "string"},
                    "why_both_statistics": {
                        "type": "string",
                        "description": (
                            "Why BOTH rather than one. Recorded because the ruling's ground is "
                            "what makes the requirement legible: the two objects differ by an "
                            "order of magnitude, so a reader not told which one they hold is "
                            "wrong by that much."
                        ),
                    },
                    "source": {"type": "string"},
                },
            },
            "binding_clusters": {
                "type": "object",
                "description": (
                    "THE BINDING CLUSTER PER CLASS OF QUANTITY, because it is NOT the same for "
                    "every quantity (decisions/0103 §2). The outcome shares cluster by ACCOUNT "
                    "-- one account contributes many pairs, so pair-level resampling "
                    "understates the interval. W's interval is SHOW-clustered, and the spec "
                    "names the show as binding there, so account-level resampling would "
                    "UNDERSTATE it. Every CI names its quantity class, and check S24 asserts "
                    "the unit used is the binding cluster for that class or that the "
                    "disagreement is recorded and NOT reconciled. A class that is not in this "
                    "registry cannot carry a CI, which is what stops a show-bound quantity "
                    "inheriting `account` silently."
                ),
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["binding_cluster", "source"],
                    "properties": {
                        "binding_cluster": {
                            "enum": RESAMPLING_UNITS, "x-enum-id": "resampling_unit"
                        },
                        "evidence": {
                            "type": "string",
                            "description": "Cited by source, not restated as figures: a figure "
                                           "copied into a schema is a second place it lives.",
                        },
                        "source": {"type": "string"},
                    },
                },
            },
            "bootstrap_settings": {
                "type": "object",
                "description": (
                    "A registry of bootstrap settings, keyed by id, referenced from every CI "
                    "AND restated inline at each one, because the ruling requires the seed, "
                    "the resample count, the resampling unit AND THE STATISTIC at the point of "
                    "use. ALL FOUR ELEMENTS ARE FIXED BY THE SPEC (decisions/0103 for the "
                    "first three, decisions/0118 for the statistic), so no entry records a "
                    "per-arm choice on any of them. RENAMED AT v1.6.0: the entry field was "
                    "`statistic`, a single value the arms differed on; it is now `statistics`, "
                    "an array that must hold BOTH. The rename is deliberate and loud -- "
                    "`additionalProperties: false` at the entry level means a writer still "
                    "emitting the old singular key FAILS rather than being silently accepted "
                    "with a per-arm choice nobody reads."
                ),
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["B", "seed", "statistics", "resampling_unit", "producing_arm",
                                 "spec_status", "fields_considered", "fields_fixed_in_spec",
                                 "fields_not_fixed_in_spec"],
                    "properties": {
                        "B": {"type": "integer", "minimum": 1},
                        "seed": {"type": "integer"},
                        "statistics": {
                            "type": "array",
                            "items": {"enum": BOOTSTRAP_STATISTICS,
                                      "x-enum-id": "bootstrap_statistic"},
                            "minItems": 2,
                            "maxItems": 2,
                            "uniqueItems": True,
                            "description": (
                                "BOTH OBJECTS THIS BOOTSTRAP PRODUCES (decisions/0118). Plural "
                                "here and singular at each interval: the run produces both, and "
                                "each interval is one of them and says which. Check S40 asserts "
                                "both are present in every entry; check S23 asserts each "
                                "interval's single value is one of them."
                            ),
                        },
                        "resampling_unit": {
                            "enum": RESAMPLING_UNITS,
                            "x-enum-id": "resampling_unit",
                            "description": "An enum, not a constant: pinning it to `account` "
                                           "made it impossible for a show-bound quantity to "
                                           "say `show` (decisions/0103 §2).",
                        },
                        "producing_arm": {"enum": ["a", "b", "sole"],
                                          "x-enum-id": "producing_arm"},
                        "spec_status": {
                            "enum": ["fixed_in_spec", "partly_fixed_in_spec"],
                            "x-enum-id": "spec_status",
                            "description": (
                                "WHETHER THE SPEC FIXES EVERY ELEMENT OF THIS ENTRY, and it is "
                                "no longer a free label: check S40 derives it from the two "
                                "lists below and asserts the declared value against the "
                                "derivation. It was unpoliced until v1.7.0 -- `spec_status` "
                                "appeared ZERO times in the validator, which polices "
                                "`fields_not_fixed_in_spec` by name -- so an entry could "
                                "declare itself unfixed while listing all four elements as "
                                "fixed and validate clean. THE FIELD THAT CARRIES THE CLAIM IS "
                                "THE FIELD THAT MUST BE CHECKED.\n"
                                "RETIRED AT v1.7.0: `unfixed_at_time_of_writing`. Its "
                                "antecedent has occurred and it retains no legitimate referent "
                                "-- B, the seed and the statistic are fixed for EVERY entry by "
                                "decisions/0103 and decisions/0118, so no entry can have an "
                                "empty fixed list, and the token could only ever have been "
                                "written by a writer contradicting its own lists. Same "
                                "disposition `if_ruled_otherwise` took at v1.6.0: quoted here, "
                                "removed there. `partly_fixed_in_spec` STAYS and is not to be "
                                "removed -- it has a live referent in the show-clustered entry, "
                                "whose UNIT is not fixed by decisions/0103 §2."
                            ),
                        },
                        "fields_considered": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                            "uniqueItems": True,
                            "description": (
                                "THE PARTITION ANCHOR, ONE LEVEL DOWN. $.bootstrap_spec got one "
                                "at v1.6.0 so that an empty not-fixed list would be ESTABLISHED "
                                "rather than merely empty; each entry's own fixed list had no "
                                "such anchor, and the only assertion on it was membership of "
                                "`statistics` -- so an entry could carry "
                                "`fields_fixed_in_spec: [\"statistics\"]`, silently dropping B, "
                                "the seed and the unit, and pass. Same reasoning, same shape: "
                                "the fixed and not-fixed lists must partition THIS list.\n"
                                "AND THIS LIST IS ITSELF ANCHORED OUTSIDE THE FILE, since "
                                "v1.8.0: an anchor read from the entry under test could only "
                                "agree with itself, so `fields_considered: [\"statistics\"]` "
                                "partitioned perfectly while dropping the other three out of "
                                "the record entirely. Check S40 asserts this list CONTAINS "
                                "every element the spec fixes -- B, the seed, the resampling "
                                "unit and the statistic (decisions/0103, decisions/0118) -- "
                                "held in the validator and written from those rulings. A fifth "
                                "element may be considered and must then be partitioned like "
                                "any other; none of the four may be dropped."
                            ),
                        },
                        "fields_fixed_in_spec": {
                            "type": "array",
                            "items": {"type": "string"},
                            "uniqueItems": True,
                            "description": "Which of this entry's fields the spec fixes. It "
                                           "existed because `spec_status` alone could not say "
                                           "that B was fixed while the statistic was not. All "
                                           "four are fixed as of decisions/0118 for the "
                                           "account-clustered entries -- and it is kept, "
                                           "because a list that says WHICH is readable where a "
                                           "status that says `fixed_in_spec` is not, and "
                                           "because a future element would reopen the split.",
                        },
                        "fields_not_fixed_in_spec": {
                            "type": "array",
                            "items": {"type": "string"},
                            "uniqueItems": True,
                            "description": (
                                "Which of this entry's fields the spec leaves open. EMPTY on "
                                "every account-clustered entry and holding `resampling_unit` on "
                                "a show-clustered one (decisions/0103 §2). Required rather than "
                                "optional: an omitted list and an empty one are the same value "
                                "to a reader, and only one of them is a record."
                            ),
                        },
                        "note": _text("A note from the writer."),
                    },
                },
            },
            "step_duality": {
                "type": "object",
                "description": (
                    "WHICH STEPS ARE DUAL, AS A FIXED FACT OF THE SPEC. Added at v1.3.0 against "
                    "reviewer-engineering's M2. Every by_producing_arm block declares a "
                    "`step_dual_status` and a `producing_step`, two keys apart in one object, "
                    "and nothing read one against the other -- so a Step 9 block could declare "
                    "itself `single_arm` and validate, and in the merged document the clause "
                    "that catches a dropped arm is guarded on `dual` and would never fire. THE "
                    "LOOSENING THE RULING FORBADE WAS REACHABLE BY RELABELLING RATHER THAN BY "
                    "WIDENING. The statuses here are fixed by const, so the registry cannot be "
                    "relabelled either, and check S31 asserts every block against it."
                ),
                "additionalProperties": False,
                "required": sorted(STEP_DUALITY),
                "properties": {
                    step: {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["dual_status", "source"],
                        "properties": {
                            "dual_status": {"const": status, "x-enum-id": "step_dual_status"},
                            "source": {"type": "string"},
                            "note": {"type": "string"},
                        },
                    }
                    for step, status in STEP_DUALITY.items()
                },
            },
            "declared_intervals": {
                "type": "array",
                "description": (
                    "INTERVALS ON QUANTITIES THAT ARE NOT THE OUTCOME SHARES. Added at v1.3.0 "
                    "against reviewer-engineering's M10: no instance illustrated a `show`-unit "
                    "interval or the `unit_disagreement` subtree, so Step 16 would have been "
                    "built without the branches decisions/0103 §2 exists to protect -- THE "
                    "BINDING CLUSTER IS NOT THE SAME FOR EVERY QUANTITY, and a show-bound "
                    "quantity that inherits `account` silently is the failure that ruling "
                    "names. Both branches are exercised here."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["interval_id", "quantity", "produced_by_step",
                                 "producing_arm", "ci"],
                    "properties": {
                        "interval_id": {"type": "string"},
                        "quantity": _text("The quantity this interval is on."),
                        "produced_by_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
                        "producing_arm": {"enum": ["a", "b", "sole"],
                                          "x-enum-id": "producing_arm"},
                        "ci": {"$ref": "#/$defs/ci"},
                        "merged_from": {
                            "type": "string",
                            "x-writer-text": True,
                            "description": "As on a payload: which arm file this came from. "
                                           "Required in the merged document, forbidden in an "
                                           "arm file (check S30).",
                        },
                        "note": _text("A note from the writer."),
                        "source": {"type": "string"},
                    },
                },
            },
            "block_ownership": {
                "type": "object",
                "description": (
                    "WHO OWNS EACH TOP-LEVEL BLOCK. Added at v1.1.0 against "
                    "reviewer-engineering's F9: six required top-level blocks named no owner, "
                    "so Step 9 inherited them by being the first step to write the file -- "
                    "INCLUDING ONE IT IS EXPLICITLY FORBIDDEN TO COMPUTE. Step 8 holds the "
                    "episode-level evidence for D4 and Step 9 is ruled to CONSUME it, not "
                    "rebuild it (decisions/0070 rulings 1 and 7), and $.limitations belongs to "
                    "the Human Lead at Step 14, which no agent may draft. Ownership is now "
                    "stated per block, with the mode: copied from another step's output, "
                    "written by its owner, structural from Step 8b, or Human Lead only. Check "
                    "S27 asserts every top-level block present in the file has an entry here."
                ),
                "propertyNames": {
                    "type": "string",
                    "description": (
                        "A top-level block name, or a DOTTED PATH to a nested block: "
                        "`arms[].waterfall`, `channel_classes.d4`, `document_scope.merge`. "
                        "Added at v1.3.0 against reviewer-engineering's M8 -- ownership stopped "
                        "at depth 1, and `arms` hid Step 8's waterfall, Step 10's abandonment "
                        "distribution and Step 13's D3' behind ONE Step 9 entry. Check S34 "
                        "asserts an entry for every nested block the file actually carries."
                    ),
                },
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["owner_step", "owner_role", "write_mode",
                                 "may_first_writer_fill"],
                    "properties": {
                        "owner_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
                        "owner_role": {"type": "string"},
                        "write_mode": {
                            "enum": [
                                "structural_from_step_8b",
                                "copied_from_step_8_output",
                                "written_by_owner_step",
                                "human_lead_only",
                            ],
                            "x-enum-id": "write_mode",
                        },
                        "published_by_step": {
                            "enum": WRITER_STEPS,
                            "x-enum-id": "writer_step",
                            "description": (
                                "WHICH STEP TRANSCRIBES THIS BLOCK INTO THIS SCHEMA, where "
                                "that is not the owner -- the waterfall is Step 8's figure and "
                                "Step 9 publishes it. Added at v1.3.0 with the nested entries: "
                                "under one file per step per arm, 'who owns it' no longer "
                                "answers 'whose file is it in', and check S22 needs the second "
                                "answer to know which absences are legitimate in which file."
                            ),
                        },
                        "may_first_writer_fill": {
                            "type": "boolean",
                            "description": (
                                "False means a step that is not the owner may not ORIGINATE "
                                "this block's contents. Being the first step to write the file "
                                "is not a claim to a block. Where `write_mode` is "
                                "copied_from_step_8_output the writer still transcribes the "
                                "owner's figures -- that is copying, not originating, and it "
                                "is exactly what Step 9 is ruled to do with D4."
                            ),
                        },
                        "forbidden_to_compute_here": {
                            "type": "array",
                            "items": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
                            "description": "Steps that must not COMPUTE this block's contents, "
                                           "even though they may publish them.",
                        },
                        "merged_document_only": {
                            "type": "boolean",
                            "description": (
                                "True means this block may appear ONLY in the merged document "
                                "(task-sheet.md Step 13b): it is one of the blocks only the "
                                "merge may fill, and an isolated arm could not have produced "
                                "its contents without inventing them. Check S29 asserts it "
                                "against $.document_scope.role, which is what stops an arm "
                                "file masquerading as a merged one. Added at v1.2.0 "
                                "(decisions/0107)."
                            ),
                        },
                        "source": {"type": "string"},
                    },
                },
            },
            "channel_classes": {"oneOf": [{
                "type": "object",
                "description": (
                    "D4 and D9 publish ALONGSIDE the bounds and are never folded into them, so "
                    "they have their own slots (decisions/0062). BOTH ARE STEP 8's FIGURES: "
                    "Step 8 holds the episode-level evidence and Step 9 is forbidden to "
                    "recompute either, so the counts here are COPIED, and the schema says so "
                    "at the point of use (F9). "
                    "ARM FILES DO NOT CARRY THIS BLOCK (decisions/0114 E8): requiring it in "
                    "seven arm files made SEVEN WRITERS OF A FIGURE NONE OF THEM PRODUCED, "
                    "with no precedence rule and no agreement check. The MERGED DOCUMENT "
                    "carries it ONCE, filled at Step 13b from Step 8's artifact; an arm file "
                    "carries the ABSENCE IDIOM below -- the block stays required, so the "
                    "absence is STATED rather than silent. Check S36 fails a filled copy in an "
                    "arm file and fails an absence in the merged document."
                ),
                "additionalProperties": False,
                "required": ["d4", "d9"],
                "properties": {
                    "merged_from": {
                        "type": "string",
                        "description": (
                            "The source this block was filled from, named at the point of use "
                            "(decisions/0111 E6, decisions/0114 E8). It is Step 8's artifact, "
                            "which is a NON-ARM-FILE source of the merge and is declared as one "
                            "in $.document_scope.merge.sources_merged."
                        ),
                    },
                    "d4": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["definition", "published_alongside", "folded_into_bound",
                                     "counts", "computed_by", "copied_not_computed"],
                        "properties": {
                            "definition": {"type": "string"},
                            "published_alongside": {"const": True},
                            "folded_into_bound": {"const": False},
                            "computed_by": {
                                "const": "step8",
                                "description": "Step 8 emits the D4 count; Step 9 must not "
                                               "compute it (decisions/0070 ruling 7).",
                            },
                            "copied_not_computed": {"const": True},
                            "counts": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": POPULATIONS,
                                "properties": {p: {"$ref": "#/$defs/count"} for p in POPULATIONS},
                            },
                            "source": {"type": "string"},
                        },
                    },
                    "d9": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["published_alongside", "folded_into_bound", "keys",
                                     "universe", "quantities", "computed_by",
                                     "copied_not_computed"],
                        "properties": {
                            "published_alongside": {"const": True},
                            "folded_into_bound": {"const": False},
                            "computed_by": {
                                "const": "step8",
                                "description": "D9's search runs on the pulled sweep, which "
                                               "Step 8 holds and Step 9 does not.",
                            },
                            "copied_not_computed": {"const": True},
                            "keys": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["strict", "loose"],
                                "properties": {
                                    "strict": {"type": "string"},
                                    "loose": {"type": "string"},
                                    "third_key_is_not_an_endpoint": {"type": "string"},
                                },
                            },
                            "universe": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": ["label", "definition"],
                                "properties": {
                                    "label": {"type": "string"},
                                    "definition": {"type": "string"},
                                    "n_show_ids": {"$ref": "#/$defs/count"},
                                    "rank_basis": {"type": "string"},
                                    "rank_tie_break": {"$ref": "#/$defs/absence"},
                                },
                            },
                            "quantities": {
                                "type": "object",
                                "description": (
                                    "Each quantity that has both key forms publishes AS A "
                                    "BOUND: strict is the floor because it cannot over-count, "
                                    "loose is the ceiling because it merges genuinely "
                                    "different shows, and NEITHER endpoint may be quoted as "
                                    "the result. Coverage publishes beside a zero floor, or "
                                    "the bound is indistinguishable from a check that looked "
                                    "nowhere. THE THREE NAMED QUANTITIES ARE REQUIRED -- the "
                                    "record fixes exactly these three as having both key forms "
                                    "(decisions/0078, 0090), and requiring them by name is "
                                    "what stops check S16 examining an empty map and reporting "
                                    "an emptiness it cannot distinguish from a clean pass (F4)."
                                ),
                                "required": ["complementary_pairs", "half_a", "half_b"],
                                "additionalProperties": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["floor", "ceiling", "point_estimate",
                                                 "coverage"],
                                    "properties": {
                                        "floor": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["value", "key", "direction"],
                                            "properties": {
                                                "value": {"$ref": "#/$defs/count"},
                                                "key": {"const": "strict"},
                                                "direction": {"const": "cannot_over_count"},
                                            },
                                        },
                                        "ceiling": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["value", "key", "direction"],
                                            "properties": {
                                                "value": {"$ref": "#/$defs/count"},
                                                "key": {"const": "loose"},
                                                "direction": {
                                                    "const": "merges_genuinely_different_shows"
                                                },
                                            },
                                        },
                                        "point_estimate": {"$ref": "#/$defs/absence"},
                                        "coverage": {
                                            "type": "object",
                                            "additionalProperties": False,
                                            "required": ["records_examined"],
                                            "properties": {
                                                "records_examined": {"$ref": "#/$defs/count"},
                                                "records_with_a_slug": {"$ref": "#/$defs/count"},
                                                "what_was_counted": _text(
                                                    "What the coverage count counted."
                                                ),
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            }, {"$ref": "#/$defs/block_absence"}]},
            "discovery_channel_overlap": {"oneOf": [{
                "type": "array",
                "description": (
                    "The overlap in every unit, each with the consumer that needs that unit. "
                    "Picking one unit leaves another consumer holding a wrong-unit figure. "
                    "CHECKED FOR E8's SHAPE AND FOUND TO HAVE IT (decisions/0114 E8): these "
                    "are STEP 8's counts too, no publisher named them, and nothing stopped "
                    "seven arm files from each writing them. It differs from `channel_classes` "
                    "only in being optional rather than required, so the defect was REACHABLE "
                    "rather than shipped. Same fix: the merged document carries it once, "
                    "filled at Step 13b from Step 8's artifact, and an arm file that carries "
                    "the slot at all carries the absence idiom."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["unit", "numerator", "denominator", "consumer",
                                 "single_categorical_forbidden"],
                    "properties": {
                        "unit": {
                            "enum": ["discovery_pool_usernames", "accounts_pulled",
                                     "analysis_population_accounts",
                                     "analysis_population_pairs"],
                            "x-enum-id": "overlap_unit",
                        },
                        "numerator": {"$ref": "#/$defs/count"},
                        "denominator": {"$ref": "#/$defs/count"},
                        "consumer": _text("The consumer that needs this unit."),
                        "single_categorical_forbidden": {"const": True},
                        "source": {"type": "string"},
                        "merged_from": {
                            "type": "string",
                            "description": (
                                "The source this row was filled from -- Step 8's artifact, a "
                                "declared non-arm-file source of the merge (decisions/0114 E8)."
                            ),
                        },
                    },
                },
            }, {"$ref": "#/$defs/block_absence"}]},
            "derived_fields": {
                "type": "array",
                "description": (
                    "Every stored figure that is computed from another stored figure, with the "
                    "single expression it comes from and the endpoints it moves with. When an "
                    "endpoint moves, this list is checked as a set, transitively."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["field", "expression", "moves_with", "machine_checked"],
                    "properties": {
                        "field": {"type": "string"},
                        "expression": {"type": "string"},
                        "moves_with": {"type": "array", "items": {"type": "string"}},
                        "machine_checked": {
                            "type": "boolean",
                            "description": (
                                "Whether check S12 EVALUATES this identity or merely records "
                                "the declaration. Added at v1.1.0 against "
                                "reviewer-engineering's F8: S12's title claimed it recomputed "
                                "the declared derived fields while the code evaluated one "
                                "identity. S12 now evaluates every identity whose operands the "
                                "schema fixes, and asserts this flag against the set it "
                                "actually evaluated -- so the claim and the code are checked "
                                "against each other rather than the title being trusted."
                            ),
                        },
                        "checked_by": {"type": "string"},
                        "source": {"type": "string"},
                    },
                },
            },
            "cross_arm_divergences": {
                "type": "object",
                "description": (
                    "Figures where the two arms legitimately differ, WITH THE SEARCH THAT "
                    "LOOKED FOR THEM. THIS BLOCK BELONGS TO THE MERGED DOCUMENT AND MAY APPEAR "
                    "NOWHERE ELSE (decisions/0107): it is filled by Step 13b, after the Human "
                    "Lead has diffed the arm files, and an isolated arm is structurally "
                    "forbidden to have performed the search it records -- so an arm file omits "
                    "it, and check S17 does not apply there. Until v1.2.0 S17 required it in "
                    "every file, which left the arm forbidden to write it and forbidden to "
                    "omit it, and made a fabricated cross-arm search the validator's only path "
                    "to exit 0. Restructured at v1.1.0 against reviewer-engineering's "
                    "F4: it was a bare array, and the validator failed an empty one as "
                    "VACUOUS, which collapses 'the arms agreed everywhere' into 'nobody "
                    "looked'. CLAUDE.md requires a control to DISTINGUISH those and to print "
                    "its coverage, so the emptiness is now declared and counted rather than "
                    "inferred from an empty list. `reconciled` stays const false: the schema "
                    "cannot record a reconciliation the spec forbids."
                ),
                "additionalProperties": False,
                "required": ["entries", "search"],
                "properties": {
                    "search": {"$ref": "#/$defs/search_record"},
                    "entries": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["figure", "arm_a", "arm_b", "reconciled", "reason"],
                            "properties": {
                                "figure": _text("The figure the arms differ on."),
                                "arm_a": {
                                    "type": ["string", "number", "null"], "x-writer-text": True,
                                    "description": "Arm a's value or convention.",
                                },
                                "arm_b": {
                                    "type": ["string", "number", "null"], "x-writer-text": True,
                                    "description": "Arm b's value or convention.",
                                },
                                "reconciled": {"const": False},
                                "reason": _text("Why the difference is legitimate."),
                                "source": _text("Where it is recorded."),
                            },
                        },
                    },
                },
            },
            "arms": {
                "type": "array",
                "minItems": 1,
                "items": {"$ref": "#/$defs/arm_entry"},
            },
            "variants": {"type": "array", "items": {"$ref": "#/$defs/variant_entry"}},
            "subpopulation_cuts": {
                "type": "array",
                "items": {"$ref": "#/$defs/subpopulation_cut"},
            },
            "tested_ranges": {
                "type": "object",
                "additionalProperties": False,
                "required": ["by_producing_arm"],
                "description": (
                    "The ranges actually tested, PER PRODUCING ARM since v1.4.0 "
                    "(decisions/0111 E1). An interactive Step 16 binds its controls to these "
                    "so no reader can drive it somewhere that was never tested -- and the two "
                    "arms of Step 13 may not have tested the same set, which one slot could "
                    "not have said."
                ),
                "properties": {
                    "by_producing_arm": {"$ref": "#/$defs/by_producing_arm_tested_ranges"},
                },
            },
            "limitations": {
                "type": "array",
                "description": (
                    "Limitations that travel with the result, each with its source. THIS BLOCK "
                    "BELONGS TO THE HUMAN LEAD AT STEP 14 -- see $.block_ownership, where its "
                    "write_mode is human_lead_only and no step may fill it. It is listed here "
                    "because F9 found six required top-level blocks with no owner, and a step "
                    "writing this file first would otherwise inherit a block no agent may "
                    "draft."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["id", "text", "source", "merged_from"],
                    "properties": {
                        "id": _text("The limitation's identifier."),
                        "text": _text("The limitation, in the words of the step that owns it."),
                        "source": _text("Where it is stated."),
                        "direction": {"type": ["string", "null"]},
                        "may_be_netted_with_others": {"const": False},
                        "merged_from": {
                            "type": "string",
                            "x-writer-text": True,
                            "description": (
                                "WHICH SOURCE THIS LIMITATION CAME FROM, added at v1.4.0 "
                                "(decisions/0111 E6). Step 14's limits section is a NAMED "
                                "NON-ARM-FILE SOURCE with its own entry in "
                                "$.document_scope.merge.sources_merged, and this is where an "
                                "entry names it. A ten-item bias ledger that must not be "
                                "netted cannot arrive in the reader-facing document with no "
                                "recorded provenance."
                            ),
                        },
                    },
                },
            },
            "spec_choices_made_by_step_8b": {
                "type": "array",
                "description": (
                    "Every choice this schema makes that its own spec does not fix, named at "
                    "the point of use rather than left to be inferred. Each says what would "
                    "change if it were ruled the other way."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["choice", "spec_gap", "what_was_done",
                                 "if_ruled_otherwise"],
                    "properties": {
                        "choice": {"type": "string"},
                        "spec_gap": {"type": "string"},
                        "what_was_done": {"type": "string"},
                        "if_ruled_otherwise": {"type": "string"},
                        # A SENTENCE THIS RECORD ONCE ASSERTED AND HAS SINCE
                        # RETIRED, QUOTED VERBATIM AND MARKED BY THE KEY IT SITS
                        # UNDER (v1.9.0, reviewer-engineering F7). A retirement
                        # used to be written INTO the paragraph that replaced it,
                        # quoting the retired sentence in running prose. Two
                        # consequences, both bad: the sentence could be written
                        # back onto any of the eight propagation surfaces and
                        # nothing would fire, because src/check_surfaces.py's
                        # WITHDRAWN_PHRASES cannot hold a phrase that its own
                        # STRUCK marker does not exempt where it legitimately
                        # appears -- and the obvious repair, dropping the word
                        # WITHDRAWN into the paragraph, exempts EVERY phrase in
                        # that paragraph, since the marker's scope in a JSON
                        # string leaf is the whole value.
                        #
                        # A KEY IS A NARROWER MARKER THAN A WORD. decisions/0094
                        # already established that a field NAMED for a withdrawal
                        # IS the point-of-use marker -- structure, not prose -- so
                        # the retired sentence lives here, alone, and the
                        # paragraphs that replaced it stop quoting it.
                        "withdrawn_sentences": {
                            "type": "array",
                            "minItems": 1,
                            "items": {"type": "string"},
                            "description": (
                                "Sentences this record previously asserted and has retired, "
                                "quoted verbatim. THE KEY IS THE MARKER: a retired sentence "
                                "is quoted here rather than inside the paragraph that "
                                "replaced it, so the marker exempts the retired sentence and "
                                "NOTHING ELSE. A marker word dropped into a paragraph would "
                                "exempt every phrase in that paragraph, since its scope in a "
                                "JSON string leaf is the whole value -- which is why the "
                                "paragraphs here name this field by description rather than "
                                "by key."
                            ),
                        },
                    },
                },
            },
            "known_limits_of_this_schema": {
                "type": "array",
                "description": (
                    "What this schema and its validator cannot check. A limit recorded is a "
                    "limit a consumer can work around; an unrecorded one is a false assurance."
                ),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["limit", "consequence"],
                    "properties": {
                        "limit": {"type": "string"},
                        "consequence": {"type": "string"},
                        "mitigation": {"type": "string"},
                    },
                },
            },
            "notes": {"type": "object", "additionalProperties": {"type": "string"}},
        },
        "if": {"properties": {"placeholder": {"const": True}}, "required": ["placeholder"]},
        "then": {"required": ["placeholder_notice"]},
        "else": {"not": {"required": ["placeholder_notice"]}},
        "x-generated-by": provenance or {},
        "$defs": d,
    }
    return schema


# ---------------------------------------------------------------------------
# The placeholder instance
# ---------------------------------------------------------------------------

def _endpoint(pop: str, label: str, note: str) -> dict:
    return {
        "percent": SENT_P,
        "numerator_pairs": SENT_C,
        "denominator_pairs": SENT_C,
        "population": pop,
        "population_n": SENT_C,
        "population_label": label,
        "attainable": True,
        "note": ph(note),
    }


# The bootstrap the spec fixes (decisions/0103 §1). These are SETTINGS, not
# measurements: like enum values and definitions they are real in a placeholder,
# so Step 16 can be built against the shape a real interval will have.
BOOTSTRAP_B = 10000
BOOTSTRAP_SEED = 20260818


def _ci(ref: str, unit: str = "account", quantity_class: str = "outcome_shares",
        disagreement: bool = False, binding: str = "show",
        statistic: str = "levels") -> dict:
    ci = {
        "level_pct": 95,
        "lower": SENT_P,
        "upper": SENT_P,
        "method": "percentile_bootstrap",
        "bootstrap_ref": ref,
        # At the point of use, per decisions/0103 and decisions/0118: the seed,
        # the resample count, the resampling unit AND THE STATISTIC are written
        # HERE as well as referenced.
        #
        # THE STATISTIC IS NO LONGER DERIVED FROM THE ARM. Until v1.5.0 this line
        # read `ARM_STATISTIC[ref.split("_", 1)[0]]` -- the arm chose, and the
        # interval inherited. It is now a property of the INTERVAL: a run
        # produces both objects and each interval says which one it is. The
        # default is `levels` because a share is a level; a movement is passed
        # explicitly, at the one place a movement is declared.
        "B": BOOTSTRAP_B,
        "seed": BOOTSTRAP_SEED,
        "statistic": statistic,
        "resampling_unit": unit,
        "quantity_class": quantity_class,
        "note": ph(
            "the interval is a sentinel; the bootstrap settings, the unit and the quantity "
            "class are real, because the ruling requires them at the point of use"
        ),
    }
    if disagreement:
        ci["unit_disagreement"] = {
            # THE BINDING CLUSTER IS A PROPERTY OF THE QUANTITY CLASS, NOT A
            # CONSTANT. It is `show` for the window-W percentile and `account`
            # for the outcome shares, and the disagreement runs in whichever
            # direction the two differ (decisions/0103 §2).
            "binding_cluster": binding,
            "unit_used": unit,
            "material": True,
            "reported_not_reconciled": True,
            "note": ph(
                "structure only: this branch shows how an interval records a unit that "
                "differs from the binding cluster for its quantity class. It is reported and "
                "not reconciled"
            ),
        }
    return ci


def _ci_absent() -> dict:
    return {
        "status": "not_required_by_spec",
        "reason": (
            "The spec does not ask this step for an interval on this quantity: Step 13's "
            "per-arm sensitivity series is a series of shares and Step 12 lists candidate "
            "cuts without mandating intervals. The slot is present and says so, because "
            "'not asked for' and 'forgotten' must not look alike."
        ),
        "source": "task-sheet.md Steps 12 and 13; reviewer-engineering F3",
    }


def _share(pop: str, ref: str, horizon_note: str, ci_present: bool = True,
           unit: str = "account", quantity_class: str = "outcome_shares",
           disagreement: bool = False) -> dict:
    return {
        "value_percent": SENT_P,
        "numerator_pairs": SENT_C,
        "denominator_pairs": SENT_C,
        "on_population": pop,
        "on_population_n": SENT_C,
        "on_population_label": "post-liveness (position 7)",
        "ci": _ci(ref, unit, quantity_class, disagreement) if ci_present else _ci_absent(),
        "is_an_observed_count_not_a_bound": True,
        "horizon_days": SENT_C,
        "note": ph(horizon_note),
    }


def _exclusions() -> dict:
    return {
        "total_pairs": SENT_C,
        "never_started_component": SENT_C,
        "started_and_left_component": SENT_C,
        "accounts": SENT_C,
        "channel_pairs_conceded_by_the_floor": SENT_C,
    }


def _corners() -> list:
    return [
        {
            "corner": "floor",
            "never_started_percent": SENT_P,
            "started_and_left_percent": SENT_P,
            "continued_percent": SENT_P,
            "note": ph("one row per attainable corner"),
        },
        {
            "corner": "ceiling",
            "never_started_percent": SENT_P,
            "started_and_left_percent": SENT_P,
            "continued_percent": SENT_P,
            "note": ph("one row per attainable corner"),
        },
    ]


def _payload(pop: str, arm: str, degenerate_ns: bool, coincides: bool,
             step: str = "step9", bounds_present: bool = True,
             ci_present: bool = True, disagreement: bool = False) -> dict:
    ref = f"{arm}_default"
    payload: dict = {
        "producing_arm": arm,
        "written_by_step": step,
        "written_by": f"Step {step[4:]}",
        "shares": {
            "never_started": _share(pop, ref, "never-started is read at tau1",
                                    ci_present=ci_present, disagreement=disagreement),
            "started_and_left": _share(pop, ref, "started-and-left is assigned at tau2",
                                       ci_present=ci_present),
            "continued": _share(
                pop, ref,
                "Continued is read at tau2; this observed share does not replace the ceiling "
                "in bounds.continued",
                ci_present=ci_present,
            ),
        },
        "bounds": {
            "never_started": {
                "floor": _endpoint(pop, "position 5", "floor endpoint"),
                "ceiling": _endpoint(pop, "position 5", "ceiling endpoint"),
                "width_pp": SENT_P,
                "degenerate": degenerate_ns,
                "degenerate_reason": (
                    ph(
                        "structure only: this branch shows how a zero-width bound is written. "
                        "A degenerate bound is a measured zero width, not missing data, and a "
                        "consumer must render it as an interval that happens to be a point."
                    )
                    if degenerate_ns
                    else None
                ),
                "conditional_sub_interval": {
                    "applicable": False,
                    "status": "structurally_absent",
                    "reason": (
                        "The conditional sub-interval conditions on this bound's own exclusion "
                        "set, so for never-started it does not exist. The field is present and "
                        "says so: an absent field and an inapplicable one must not look alike."
                    ),
                    "source": "task-sheet.md Step 8b; decisions/0066 §3",
                },
                "scope_qualifier_ref": "insertion_dormancy_covering",
                "exclusions_covered": _exclusions(),
                "endpoints_attainable": True,
                "attainable_corners": _corners(),
                "note": ph("never-started bound"),
            },
            "started_and_left": {
                "floor": _endpoint(pop, "position 5", "floor endpoint, widened"),
                "ceiling": _endpoint(pop, "position 5", "ceiling endpoint"),
                "width_pp": SENT_P,
                "degenerate": False,
                "degenerate_reason": None,
                "conditional_sub_interval": {
                    "applicable": True,
                    "floor": _endpoint(pop, "position 5", "sub-interval floor"),
                    "ceiling": _endpoint(pop, "position 5", "sub-interval ceiling"),
                    "width_pp": SENT_P,
                    "conditioning_text": ph(
                        "the started-and-left share given that every never-started exclusion "
                        "is a true decline"
                    ),
                    "constrains_never_started_exclusions": SENT_C,
                    "says_nothing_about_channel_pairs": SENT_C,
                    "coincides_with_bound": {
                        "value": coincides,
                        "measured": True,
                        "evidence": ph(
                            "structure only: whether the sub-interval coincides with its bound "
                            "is recorded here as a measured fact, so a real file never writes "
                            "the same numbers twice unremarked"
                        ),
                    },
                },
                "scope_qualifier_ref": "insertion_dormancy_covering",
                "exclusions_covered": _exclusions(),
                "endpoints_attainable": True,
                "attainable_corners": _corners(),
                "note": ph("started-and-left bound"),
            },
            "continued": {
                "ceiling": _endpoint(pop, "position 5", "Continued ceiling"),
                "floor": {
                    "status": "not_published",
                    "reason": (
                        "Continued is never emitted as a point and no floor is published for "
                        "it. The ceiling exists because any excluded pair may in truth be "
                        "Continued; that does not license a point estimate."
                    ),
                    "source": "decisions/0050, decisions/0052",
                    "decided_by": "Human Lead",
                },
                "must_not_be_read_as_a_point": True,
                "scope_qualifier_ref": "insertion_dormancy_covering",
                "exclusions_covered": _exclusions(),
                "note": ph("Continued bound"),
            },
        },
        "ceilings_cannot_all_hold": {
            "simultaneous": False,
            "sum_percent": SENT_P,
            "excess_pp": SENT_P,
            "excess_pairs": SENT_C,
            "excess_mechanism_expression": (
                "2 * never_started_exclusions + started_and_left_exclusions"
            ),
            "note": ph(
                "the three ceilings are alternative worst cases over the same exclusion set, "
                "not simultaneous ones"
            ),
        },
        "bound_over_sampling_width_ratios": {
            "never_started": {
                "value": SENT_P,
                "convention_label": f"arm_{arm}_convention",
                "convention_definition": ph(
                    "the sampling-width convention this arm uses, named so one arm's "
                    "denominator cannot silently become the other's"
                ),
                "numerator_definition": ph("bound width in percentage points"),
                "denominator_definition": ph("account-clustered sampling width"),
                "reconciled_with_other_arm": False,
            },
            "started_and_left": {
                "value": SENT_P,
                "convention_label": f"arm_{arm}_convention",
                "convention_definition": ph("as above"),
                "numerator_definition": ph("bound width in percentage points"),
                "denominator_definition": ph("account-clustered sampling width"),
                "reconciled_with_other_arm": False,
            },
            "started_and_left_sub_interval": {
                "value": SENT_P,
                "convention_label": f"arm_{arm}_convention",
                "convention_definition": ph("as above"),
                "numerator_definition": ph("sub-interval width in percentage points"),
                "denominator_definition": ph("account-clustered sampling width"),
                "reconciled_with_other_arm": False,
            },
        },
        "spec_choices_this_arm_made": [
            ph("each choice the spec does not fix, named by the arm that made it"),
        ],
    }
    if not bounds_present:
        absent = {
            "block_is_absent": True,
            "status": "not_required_by_spec",
            "reason": (
                "The spec asks for the bounds at the headline arms. It does not ask this step "
                "for a bound at every arm of the sensitivity grid, so the slot records that "
                "rather than demanding a figure no step produces."
            ),
            "source": "task-sheet.md Step 13; reviewer-engineering F1",
            "owning_step": "step9",
        }
        payload["bounds"] = absent
        payload["ceilings_cannot_all_hold"] = dict(
            absent,
            reason=(
                "The three-ceiling sum is a function of the three ceilings, and this payload "
                "publishes no bounds, so there are no ceilings here to sum. It is absent WITH "
                "the bounds and never on its own; check S22 ties the two together."
            ),
        )
        payload.pop("bound_over_sampling_width_ratios", None)
    if arm == "sole":
        payload["bound_over_sampling_width_ratios"] = {
            "status": "not_a_dual_step",
            "reason": (
                "This step is single-arm, so there is no second sampling-width convention to "
                "hold this one against. The ratios are reported and not reconciled BETWEEN "
                "arms, which presupposes two of them; recording that here keeps 'this step is "
                "not dual' distinct from 'this quantity does not exist'."
            ),
            "source": "decisions/0058, 0063; reviewer-engineering F5",
        }
    return payload


def _payload_absent(step: str) -> dict:
    """A payload slot that is present and says why it holds no payload.

    A single-arm step's own file needs a legal spine (reviewer-engineering M9).
    Step 11 recomputes the headline ON SUBPOPULATIONS, under $.subpopulation_cuts;
    the unconditional headline is Step 9's, and a Step 11 file that restated it
    would be a second definition of one figure. So the slot is present and
    records that, rather than the file carrying a copy or omitting the spine.
    """
    return {
        "status": "not_required_by_spec",
        "reason": (
            "This file is a single-arm step's own file. The unconditional headline belongs to "
            "Step 9 and is published in Step 9's files; this step recomputes it on "
            "subpopulations, which is written under $.subpopulation_cuts. Restating Step 9's "
            "figure here would be a second definition of one figure, which is the defect the "
            "no-conversion-layer rule exists to prevent."
        ),
        "source": "task-sheet.md Steps 9 and 11; decisions/0109 §1; reviewer-engineering M9",
    }


def _population_block(pop: str, degenerate_ns: bool, coincides: bool,
                      dual: bool = True, step: str = "step9",
                      bounds_present: bool = True, ci_present: bool = True,
                      dual_arms: tuple = ("a", "b"),
                      payload_absent: bool = False) -> dict:
    """One population of one arm.

    `dual` selects between the two-arm and the single-arm shape. Steps 9 and 13
    are dual (decisions/0103 §3); Steps 10, 11 and 12 are not, and were being
    made to name an `a` and a `b` they do not have (reviewer-engineering F5).

    `dual_arms` is which of those arms THIS FILE holds, and it is the second of
    the two facts split apart at v1.2.0 (decisions/0107): one arm in an arm file,
    both only in the merged document Step 13b produces.
    """
    if dual:
        arms = {
            key: _payload(pop, key, degenerate_ns, coincides, step, bounds_present,
                          ci_present)
            for key in dual_arms
        }
    else:
        arms = {
            "sole": _payload_absent(step) if payload_absent else _payload(
                pop, "sole", degenerate_ns, coincides, step, bounds_present, ci_present),
        }
    held = list(arms)
    return {
        "population": pop,
        "definition": ph(
            "the definition of this population, restated by the writer at the point of use"
        ),
        "n_position_5": SENT_C,
        "n_post_liveness": SENT_C,
        "populations_differ_note": ph(
            "the bounds are stated on the position-5 row set and the published shares on the "
            "post-liveness row set; they are different populations and every field says which"
        ),
        "by_producing_arm": {
            "step_dual_status": "dual" if dual else "single_arm",
            "arms_in_this_file": "both_arms" if len(held) > 1 else "one_arm",
            "producing_step": step,
            "step_dual_status_source": (
                "CLAUDE.md, Dual implementation; Step 13's duality is decisions/0103 §3; "
                "one file per arm is decisions/0107"
            ),
            "arms": arms,
            **({"arm_held": held[0]} if len(held) == 1 else {}),
        },
    }


def _waterfall(pop: str) -> dict:
    inert = {1, 2, 3, 7}
    positions = []
    for i, name in enumerate(FILTER_NAMES, start=1):
        p = {
            "position": i,
            "filter": name,
            "n_in": SENT_C,
            "n_out": SENT_C,
            "removed": SENT_C,
            "inert": i in inert,
            "inert_reason": (
                ph(
                    "this position cannot fire on this frame; it is kept so that a future "
                    "upstream change is still caught, and it is labelled so a zero does not "
                    "read as the rule having found nothing"
                )
                if i in inert
                else None
            ),
            "outcome_conditional": i == 6,
            "note": ph("one entry per position, in the mandated order"),
        }
        if i == 5:
            p["sub_lines"] = [
                {"label": ph("right-censoring line 1"), "removed": SENT_C, "n_out": SENT_C,
                 "note": ph("right-censoring publishes as two lines, not one")},
                {"label": ph("right-censoring line 2"), "removed": SENT_C, "n_out": SENT_C,
                 "note": ph("right-censoring publishes as two lines, not one")},
            ]
        positions.append(p)
    return {
        "population": pop,
        # WHO WRITES IT HERE, and separately WHO OWNS THE FIGURES. Step 8 owns
        # the waterfall and Step 9 publishes it into this schema; until v1.4.0
        # this field said `step8` while $.block_ownership said Step 9 published
        # it, and the two were never read against each other.
        "written_by_step": "step9",
        "figures_owned_by_step": "step8",
        "order_ref": "decisions/0029 positions 1-7",
        "positions": positions,
        "monotone_check": {"operator": ">=", "result": True, "positions_checked": SENT_C},
    }


def _air_periods(pop: str) -> dict:
    return {
        "population": pop,
        "written_by_step": "step9",
        "figures_owned_by_step": "step8",
        "measured_after": "position 4 (the mandated order censors the position-4 output)",
        "rows": [
            {
                "air_period": ph("one row per air period"),
                "retained_pairs": SENT_C,
                "entering_pairs": SENT_C,
                "retained_share_percent": SENT_P,
            }
        ],
    }


def _abandonment(pop: str, row_set: str = "position_5") -> dict:
    edges = [round(x / 10, 1) for x in range(11)]
    labels = {
        "position_5": "position 5 (the row set the bounds are stated on)",
        "post_liveness": "post-liveness (position 7)",
    }
    return {
        "population": pop,
        # F2: the population alone does not identify the row set. Step 8 measured
        # p_at_bound, n_started_and_left, the histogram and the p = 1.0 residual
        # on four row sets with different values on each.
        "row_set": row_set,
        "row_set_label": labels[row_set],
        "n_rows_in_row_set": SENT_C,
        "written_by_step": "step10",
        "n_started_and_left": SENT_C,
        "p_definition": "p = |{e in E2 : e <= max(A_H)}| / L2",
        "p_raw_ratio_form_withdrawn": True,
        "p_is_null_off_started_and_left": True,
        "bin_unit": "fraction_of_season",
        # F7: one entry per stratum. The unstratified case is the `all` entry;
        # the second entry shows that a stratified pass has somewhere to go.
        "histograms": [
            {
                "stratum": {
                    "kind": "all",
                    "label": "all shows pooled",
                    "l2_min": None,
                    "l2_max": None,
                    "definition": ph("every started-and-left row in this row set"),
                },
                "bin_edges_p": edges,
                "counts": [SENT_C] * (len(edges) - 1),
                "n_rows": SENT_C,
            },
            {
                "stratum": {
                    "kind": "l2_stratum",
                    "label": ph("one L2 stratum; the bounds are the writer's"),
                    "l2_min": None,
                    "l2_max": None,
                    "definition": ph(
                        "structure only: p is a fraction of a season, so bins are not "
                        "comparable across shows with very different L2, and the instruction "
                        "not to pool them is an instruction to stratify"
                    ),
                },
                "bin_edges_p": edges,
                "counts": [SENT_C] * (len(edges) - 1),
                "n_rows": SENT_C,
            },
        ],
        "named_categories": {
            "first_episode": {
                "count": SENT_C,
                "share_percent": SENT_P,
                "definition": ph("first-episode drops"),
            },
            "mid_season": {
                "count": SENT_C,
                "share_percent": SENT_P,
                "definition": ph("mid-season drops"),
            },
            "near_finale": {
                "count": SENT_C,
                "share_percent": SENT_P,
                "definition": ph("near-finale drops, excluding the p = 1.0 residual"),
            },
            "p_equals_1_residual": {
                "count": SENT_C,
                "share_percent": SENT_P,
                "definition": ph(
                    "reached the final listed episode but missed the completion threshold; its "
                    "own named category, not part of near-finale"
                ),
            },
        },
        "p_equals_1_residual_is_separate_from_near_finale": True,
        "p_at_bound": {
            "column_cardinalities": {
                "true_count": SENT_C,
                "false_count": SENT_C,
                "null_count": SENT_C,
                "total_rows": SENT_C,
                "identity_holds": True,
                "false_is_the_ordinary_case": True,
            },
            "coextensivity_gap": {
                "p_equals_one_total": SENT_C,
                "in_both": SENT_C,
                "saturated_not_final": SENT_C,
                "final_not_saturated": SENT_C,
                "in_neither": SENT_C,
                "rows_examined": SENT_C,
                "is_empty": True,
            },
            "two_classes_note": ph(
                "two different FALSE classes: the coextensivity gap, which is the one the "
                "sentence 'the FALSE class is empty' names, and the column's own FALSE value, "
                "which is the ordinary started-and-left row and is large. A consumer that "
                "provisions p_at_bound as a two-valued column is wrong by the whole of "
                "column_cardinalities.false_count"
            ),
            "construction_links": [
                {"link": "m_H in E2", "kind": "construction", "measured_value": None},
                {
                    "link": "|{e in E2 : e <= m_H}| = L2  <=>  m_H = max(E2)",
                    "kind": "construction",
                    "measured_value": None,
                },
                {
                    "link": "max(E2) = F2",
                    "kind": "measured",
                    "measured_value": ph("the frame count that establishes this link"),
                },
            ],
        },
        "amendment_shift": {
            "direction": "earlier",
            "pairs_moved": SENT_C,
            "note": ph(
                "the pairs the amendment moves out of started-and-left are the ones that got "
                "furthest, so the chart shifts earlier; the shift is definitional and must not "
                "be attributed to behaviour"
            ),
        },
        "comparability_caveat": ph(
            "p is a fraction of a season, not a count of episodes; bins are not comparable "
            "across shows with very different L2, and at L2 = 2 p takes one of two values"
        ),
        "no_specific_episode_claimed": True,
    }


def _liveness(pop: str) -> dict:
    return {
        "total_pairs": SENT_C,
        "never_started_component": SENT_C,
        "started_and_left_component": SENT_C,
        "accounts": SENT_C,
        "silence_test_alone": SENT_C,
        "spared_by_not_continued": SENT_C,
        "identity": "silence_test_alone - spared_by_not_continued = total_pairs",
        "pair_level_not_account_level": True,
        "written_by_step": "step9",
        "figures_owned_by_step": "step8",
    }


def _d3_prime(pop: str, w: int, arm: str) -> dict:
    return {
        "population": pop,
        "producing_arm": arm,
        "cleared_count": SENT_C,
        "cleared_share_percent": SENT_P,
        "denominator_pairs": SENT_C,
        "population_label": ph(
            "Step 8's right-censored population at this arm; D3's clearance contains W, so "
            "the cleared subpopulation changes with the arm"
        ),
        "H_days_held_constant": 91,
        "written_by_step": "step13",
        "note": ph("one cleared count and share per arm, per population"),
    }


def _absent_block(status: str, owning_step: str, reason: str, source: str) -> dict:
    return {
        "block_is_absent": True,
        "status": status,
        "reason": reason,
        "source": source,
        "owning_step": owning_step,
    }


def _arm_id(setting_id: str, step: str, revision: int | None = None) -> str:
    """The arm entry's label: the setting, the producing step AND the revision.

    THE LABEL CARRIES THE WHOLE KEY. Entries share a setting, so a label naming
    part of the key reintroduces the collision the key exists to remove for any
    consumer that indexes by the label -- which is why the producing step went in
    at v1.4.0 and the adopted-rule revision goes in here (decisions/0114 E14).
    """
    rev = _revision() if revision is None else revision
    return f"{setting_id}__{step}__r{rev}"


def _per_arm_container(step: str, dual_arms: tuple, make_payload) -> dict:
    """One by_producing_arm container over any payload (decisions/0111 E1).

    THE SAME SHAPE THE HEADLINE TAKES. Step 13's six non-headline outputs each
    had ONE SLOT where TWO ARMS write, which forces the reconciliation
    decisions/0107 §3 forbids; the fix is the widening both earlier appearances
    of this defect took, because widening keeps ONE DEFINITION PER FIGURE.
    """
    dual = STEP_DUALITY.get(step, "dual") == "dual"
    keys = tuple(dual_arms) if dual else ("sole",)
    arms = {k: make_payload(k) for k in keys}
    held = list(arms)
    return {
        "step_dual_status": "dual" if dual else "single_arm",
        "arms_in_this_file": "both_arms" if len(held) > 1 else "one_arm",
        "producing_step": step,
        "step_dual_status_source": (
            "CLAUDE.md, Dual implementation; Step 13's duality is decisions/0103 §3; "
            "one file per arm is decisions/0107"
        ),
        "arms": arms,
        **({"arm_held": held[0]} if len(held) == 1 else {}),
    }


def _action_counts_payload(arm: str, step: str) -> dict:
    return {
        "producing_arm": arm,
        "written_by_step": step,
        "counts": {
            "s1_watch": SENT_C, "s1_scrobble": SENT_C, "s1_checkin": SENT_C, "s1_other": SENT_C,
            "s2_watch": SENT_C, "s2_scrobble": SENT_C, "s2_checkin": SENT_C, "s2_other": SENT_C,
        },
        "note": ph(
            "per-pair counts by action type, per producing arm; `action` is record-level and "
            "the row is a pair, so there is no row-level action value"
        ),
    }


def _arm(arm_id: str, w: int, origin: str, in_grid: bool, primary: bool,
         origin_note: str, step: str, dual_arms: tuple,
         blocks_have_producers: bool = True,
         deriv_liveness_superseded: bool = False) -> dict:
    """One arm entry: ONE STEP'S MEASUREMENT AT ONE (W, clock origin) SETTING.

    THE PRODUCING STEP IS PART OF THE ENTRY KEY (decisions/0111 E2). Step 9's
    W = 108 and Step 13's W = 108 are different measurements of one setting and
    BOTH MUST EXIST, so an entry names the step whose measurement it is and
    carries exactly the blocks that step publishes.

    A block another step publishes is OMITTED here rather than written as an
    absence: the per-arm containers may not sit under a oneOf (decisions/0109 §4,
    machine-checked by S35), $.block_ownership names every block's publisher, and
    check S36 fails an entry that carries a block that is not its own. That is
    the direction nothing policed -- the file was checked for writing too little
    and never for writing too much, which is how a single-arm step's placeholder
    came to write Step 13's action-type counts (decisions/0111 §3, Q1).
    """
    publishes = {name for name, pub in BLOCK_PUBLISHER.items() if pub == step}
    writes_headline = step in HEADLINE_PUBLISHERS
    dual = STEP_DUALITY.get(step, "dual") == "dual"
    arm: dict = {
        # THE LABEL CARRIES THE WHOLE KEY. Three entries share the setting
        # (W = 108, finale-anchored) and a label naming only the setting would
        # collide for any consumer that indexed by it -- which is the collision
        # decisions/0111 E2 exists to remove, reappearing in the label.
        "arm_id": _arm_id(arm_id, step),
        "W_days": w,
        "H_days": 91,
        "clock_origin": origin,
        "clock_origin_note": ph(origin_note),
        "producing_step": step,
        # THE FOURTH KEY FIELD, READ AND NOT TYPED (decisions/0114 E14).
        "adopted_rule_revision": _revision(),
        "in_arm_grid": in_grid,
        # THE ADOPTED SETTING, not a claim that this entry publishes the
        # headline: several steps measure at (108, s2_finale) and each marks it,
        # which is what lets check S22 require each entry's own blocks there.
        "is_primary_headline": primary,
        "headline": {
            "APPLY": _population_block("APPLY", degenerate_ns=False, coincides=False,
                                       dual=dual, step=step, dual_arms=dual_arms,
                                       payload_absent=not writes_headline),
            "DERIV": _population_block("DERIV", degenerate_ns=True, coincides=True,
                                       dual=dual, step=step, dual_arms=dual_arms,
                                       payload_absent=not writes_headline),
        },
    }
    if not blocks_have_producers:
        # F1, the blocking finding. At a non-primary arm on a different clock
        # origin, nothing in the spec produces a waterfall, an abandonment
        # distribution, a per-arm liveness count or a D3' figure: Step 8 builds
        # the waterfall at the adopted finale-anchored arm, Step 10 charts the
        # headline arm, and Step 13's grid is finale-anchored throughout. Each
        # slot THIS STEP would have filled stays present and names the gap.
        why = (
            "No step in the spec produces this block for a premiere-anchored arm. Step 8 "
            "builds the waterfall at the adopted finale-anchored arm, Step 10 charts the "
            "headline arm, and Step 13's W grid is finale-anchored at every one of its eight "
            "arms. The slot is present and says so rather than requiring a figure that would "
            "have to be invented."
        )
        for name in sorted(publishes):
            arm[name] = _absent_block(
                "no_producer_in_spec", "none", why,
                "task-sheet.md Steps 8, 10 and 13; reviewer-engineering F1",
            )
        arm["note"] = ph("one entry per (W, clock origin, producing step)")
        return arm

    if "waterfall" in publishes:
        arm["waterfall"] = {p: _waterfall(p) for p in POPULATIONS}
    if "abandonment_distribution" in publishes:
        # F2: one entry per row set, and the four cells the record requires are
        # APPLY and DERIV, each at position 5 and post-liveness.
        arm["abandonment_distribution"] = {
            p: [_abandonment(p, "position_5"), _abandonment(p, "post_liveness")]
            for p in POPULATIONS
        }
    if "liveness_exclusions" in publishes:
        if deriv_liveness_superseded:
            arm["liveness_exclusions"] = {
                "APPLY": _liveness("APPLY"),
                "DERIV": _absent_block(
                    "superseded_for_this_purpose", "step13",
                    "The DERIV per-arm liveness series is recorded as SUPERSEDED FOR THIS "
                    "PURPOSE: the per-arm series to report is the APPLY one, and the DERIV "
                    "figures remain correct on DERIV while being the wrong series here. A "
                    "schema that demands a number in this slot demands a superseded one.",
                    "task-sheet.md Step 13; reviewer-engineering F1",
                ),
            }
        else:
            arm["liveness_exclusions"] = {p: _liveness(p) for p in POPULATIONS}
    if "retained_by_air_period" in publishes:
        arm["retained_by_air_period"] = {p: _air_periods(p) for p in POPULATIONS}
    # THE TWO PER-ARM NESTED BLOCKS (decisions/0111 E1), both Step 13's.
    if "d3_prime" in publishes:
        arm["d3_prime"] = {
            p: {"by_producing_arm": _per_arm_container(
                step, dual_arms, lambda a, p=p: _d3_prime(p, w, a))}
            for p in POPULATIONS
        }
    if "action_type_counts" in publishes:
        arm["action_type_counts"] = {
            "by_producing_arm": _per_arm_container(
                step, dual_arms, lambda a: _action_counts_payload(a, step))
        }
    arm["note"] = ph("one entry per (W, clock origin, producing step)")
    return arm


def _block_ownership() -> dict:
    """Who owns each block -- top level AND nested (F9; extended for M8).

    Six required top-level blocks named no owner, so the first step to write the
    file inherited them -- including `channel_classes`, whose D4 count Step 9 is
    explicitly forbidden to compute, and `limitations`, which belongs to the
    Human Lead at Step 14 and which no agent may draft. Being first to write a
    file is not a claim to a block.

    AND OWNERSHIP STOPPED AT DEPTH 1, which reviewer-engineering's M8 found: one
    `arms` entry, owned by Step 9, hid Step 8's waterfall, Step 10's abandonment
    distribution and Step 13's D3' behind it. The nested rows below name those
    owners at their dotted paths, and `published_by_step` names who transcribes a
    block it does not own -- which is what check S22 needs in order to tell a
    legitimate absence in one step's file from a gap.
    """
    structural = (
        "step8b", "Analytics Engineer, Step 8b", "structural_from_step_8b", True,
        "task-sheet.md Step 8b",
    )
    rows = {
        "schema_version": structural,
        "schema_id": structural,
        "placeholder": structural,
        "placeholder_notice": structural,
        "generated_by": (
            "step8b", "whichever step writes the file, stamping its own run",
            "written_by_owner_step", True,
            "CLAUDE.md, Generated files that function as checks",
        ),
        "document_scope": (
            "step8b", "whichever step writes the file, declaring what the file IS -- one "
                      "arm's document or the merged one",
            "written_by_owner_step", True,
            "decisions/0107; task-sheet.md Step 13b",
        ),
        "sentinels": structural,
        "arm_key": structural,
        # STRUCTURAL, and the reason is worth stating: the VALUE is Step 5's, but
        # the block is a registry Step 8b defines and every writer READS its own
        # revision from the adopted-rule file rather than from another writer
        # (decisions/0114 E14).
        "adopted_rule_revision": structural,
        "arm_grid_days": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", True,
            "decisions/0075; the grid is fixed and any step may copy it",
        ),
        "populations": structural,
        "scope_qualifiers": structural,
        "bootstrap_spec": structural,
        "binding_clusters": structural,
        "bootstrap_settings": (
            "step9", "Data Scientist, Steps 9 to 13", "written_by_owner_step", True,
            "decisions/0103 §1",
        ),
        "step_duality": structural,
        "declared_intervals": (
            "step9", "Data Scientist, whichever step produces the interval",
            "written_by_owner_step", True,
            "decisions/0103 §2; reviewer-engineering M10",
        ),
        "block_ownership": structural,
        # PUBLISHER ADDED AT v1.5.0, step13b (decisions/0114 E8). Step 8 still
        # OWNS these figures; what changed is WHOSE FILE they arrive in. They
        # arrive in the merged document, once, copied from Step 8's artifact --
        # not in seven arm files, which is what "required at the top level with
        # no publisher" amounted to.
        "channel_classes": (
            "step8", "Analytics Engineer, Step 8", "copied_from_step_8_output", False,
            "decisions/0070 rulings 1 and 7; decisions/0114 E8", "step13b",
        ),
        "discovery_channel_overlap": (
            "step8", "Analytics Engineer, Step 8", "copied_from_step_8_output", False,
            "decisions/0077, 0079; decisions/0114 E8", "step13b",
        ),
        "derived_fields": structural,
        "cross_arm_divergences": (
            "step13b",
            "Human Lead, at Step 13b, who diffs the arm files and then merges them",
            "human_lead_only", False,
            "CLAUDE.md, Dual implementation; decisions/0107; task-sheet.md Step 13b",
        ),
        "arms": (
            "step9", "Data Scientist, Steps 9 and 13", "written_by_owner_step", True,
            "task-sheet.md Steps 9 and 13",
        ),
        "variants": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13", "step13",
        ),
        # NO published_by_step, deliberately: Steps 11 and 12 BOTH write cuts
        # here, so the question is answered per ENTRY by each cut's own
        # producing_step. Naming one publisher would make the other step's file
        # illegal (check S36 reads this field, and its absence is a fact about
        # the block rather than an omission).
        "subpopulation_cuts": (
            "step11", "Data Scientist, Steps 11 and 12", "written_by_owner_step", False,
            "task-sheet.md Steps 11 and 12",
        ),
        "tested_ranges": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13, 'Record the tested ranges. Step 16 needs them.'",
            "step13",
        ),
        "limitations": (
            "human_lead", "Human Lead, Step 14", "human_lead_only", False,
            "task-sheet.md Step 14; CLAUDE.md, Human Lead",
        ),
        "spec_choices_made_by_step_8b": structural,
        "known_limits_of_this_schema": structural,
        "notes": structural,
    }
    # NESTED BLOCKS (reviewer-engineering M8). `published_by_step` is the fourth
    # element where it differs from the owner: Step 8 OWNS the waterfall figures
    # and Step 9 PUBLISHES them into this schema, and under one file per step per
    # arm those are two different questions with two different answers.
    nested = {
        "arms[].headline": ("step9", "Data Scientist, Step 9", "written_by_owner_step",
                            True, "task-sheet.md Step 9", "step9"),
        "arms[].waterfall": ("step8", "Analytics Engineer, Step 8",
                             "copied_from_step_8_output", False,
                             "task-sheet.md Step 8; decisions/0029", "step9"),
        "arms[].abandonment_distribution": ("step10", "Data Scientist, Step 10",
                                            "written_by_owner_step", False,
                                            "task-sheet.md Step 10", "step10"),
        "arms[].liveness_exclusions": ("step8", "Analytics Engineer, Step 8",
                                       "copied_from_step_8_output", False,
                                       "task-sheet.md Step 8; decisions/0048", "step9"),
        "arms[].d3_prime": ("step13", "Data Scientist, Step 13", "written_by_owner_step",
                            False, "decisions/0075", "step13"),
        "arms[].retained_by_air_period": ("step8", "Analytics Engineer, Step 8",
                                          "copied_from_step_8_output", False,
                                          "decisions/0033", "step9"),
        # PUBLISHER CORRECTED AT v1.4.0, step9 -> step13 (decisions/0111 E1,
        # which names action_type_counts one of STEP 13's six non-headline
        # outputs). The old row is what the Q1 finding turned on: the single-arm
        # placeholder wrote this block while its own table gave it to Step 9, and
        # nothing checked the direction "this file wrote too much".
        "arms[].action_type_counts": ("step8", "Analytics Engineer, Step 8",
                                      "copied_from_step_8_output", False,
                                      "decisions/0070 ruling 4; decisions/0111 E1", "step13"),
        "variants[].headline": ("step13", "Data Scientist, Step 13", "written_by_owner_step",
                                False, "task-sheet.md Step 13", "step13"),
        "variants[].d3_prime": ("step13", "Data Scientist, Step 13", "written_by_owner_step",
                                False, "decisions/0075", "step13"),
        "variants[].d2_recomputed_inside_this_arm": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "decisions/0070 ruling 5", "step13"),
        # The last two of decisions/0111 E1's six, which had no ownership row at
        # all while they were arrays of strings: check S34 only demands a row for
        # a block, and a list of scalars is not one. Per-arm nesting makes them
        # blocks, and a block with no owner is owned by whoever writes first.
        "variants[].conclusions_surviving": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13; decisions/0111 E1", "step13"),
        "variants[].conclusions_not_surviving": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13; decisions/0111 E1", "step13"),
        "subpopulation_cuts[].headline": ("step11", "Data Scientist, Steps 11 and 12",
                                          "written_by_owner_step", False,
                                          "task-sheet.md Steps 11 and 12", "step11"),
        # PUBLISHER CORRECTED AT v1.5.0, step9 -> step13b (decisions/0114 E8).
        # These two rows said Step 9 publishes D4 and D9 while the block they sit
        # in was required of every file -- so the table said one writer and the
        # schema demanded seven.
        "channel_classes.d4": ("step8", "Analytics Engineer, Step 8",
                               "copied_from_step_8_output", False,
                               "decisions/0070 ruling 7; decisions/0114 E8", "step13b"),
        "channel_classes.d9": ("step8", "Analytics Engineer, Step 8",
                               "copied_from_step_8_output", False,
                               "decisions/0088 §3, 0090; decisions/0114 E8", "step13b"),
        "document_scope.merge": (
            "step13b", "Human Lead, at Step 13b, who merges the arm files",
            "human_lead_only", False, "task-sheet.md Step 13b; decisions/0107", "step13b"),
    }
    forbidden = {
        # EVERY ARM STEP, not step9 alone (decisions/0114 E8). The old rows named
        # the one step that had been caught reaching for these figures, while the
        # block was required of all seven arm files -- so six of the seven were
        # forbidden nothing and required everything.
        "channel_classes": ["step9", "step10", "step11", "step12", "step13"],
        "discovery_channel_overlap": ["step9", "step10", "step11", "step12", "step13"],
        "limitations": ["step9", "step10", "step11", "step12", "step13"],
        # Every isolated writing step, not only the two dual ones: a single-arm
        # step is just as unable to have seen another arm's file, so listing only
        # step9 and step13 would leave the others unnamed rather than permitted.
        "cross_arm_divergences": ["step9", "step10", "step11", "step12", "step13"],
    }
    # The blocks only the merge may fill (task-sheet.md Step 13b). An arm file
    # carrying one of these is an arm file masquerading as a merged document,
    # which check S29 fails.
    merged_only = ("cross_arm_divergences", "limitations", "document_scope.merge")
    out = {}
    for name, row in list(rows.items()) + list(nested.items()):
        step, role, mode, may_fill, source = row[:5]
        entry = {
            "owner_step": step,
            "owner_role": role,
            "write_mode": mode,
            "may_first_writer_fill": may_fill,
            "source": source,
        }
        if len(row) > 5:
            entry["published_by_step"] = row[5]
        if name in forbidden:
            entry["forbidden_to_compute_here"] = forbidden[name]
        entry["merged_document_only"] = name in merged_only
        out[name] = entry
    return out


def _refs_in_scope(arms_held: tuple) -> set:
    """Which bootstrap-settings entries a file of this scope can reference.

    A registry entry for an arm the file does not hold is an entry nothing points
    at, and the placeholder exists to show a shape a writer can fill rather than
    one it has to prune.
    """
    refs = set()
    for a in arms_held:
        refs.add(f"{a}_default")
        # RENAMED FROM `{arm}_window_w` AT v1.5.0. The show-clustered settings
        # are not the window-W quantity's private property: under decisions/0114
        # E11 a single-arm step may not declare a window-W interval at all, and
        # its show-clustered interval is on a different quantity. The key names
        # the UNIT, which is what the entry fixes.
        refs.add(f"{a}_show_clustered")
    return refs


# THE MERGE'S INPUT LIST RECORDS SOURCES, NOT ONLY ARM FILES (decisions/0111 E6).
# Seven are arm files, one per step per arm (decisions/0109 §1). THE EIGHTH IS
# STEP 14's `limitations`: Step 14 delivers a limits section rather than a schema
# file, so it is not one of the seven and had no way to be recorded -- and a
# ten-item bias ledger that MUST NOT BE NETTED cannot arrive in the reader-facing
# document with no recorded provenance. It has no arm.
MERGE_INPUTS = [
    ("step9", "a"), ("step9", "b"),
    ("step13", "a"), ("step13", "b"),
    ("step10", "sole"), ("step11", "sole"), ("step12", "sole"),
]
# A NINTH SOURCE AT v1.5.0, AND IT IS A CONSEQUENCE OF E8 RATHER THAN A NEW
# RULING: once `channel_classes` and `discovery_channel_overlap` are filled ONCE
# in the merged document from STEP 8's ARTIFACT, that artifact is a source, and
# decisions/0111 E6 already ruled that the input list records SOURCES rather than
# only arm files -- for exactly this reason, that a block cannot arrive in the
# reader-facing document with no recorded provenance. It has no arm.
NON_ARM_SOURCES = [
    {
        "step": "human_lead",
        "fills_blocks": ["limitations"],
        "label": "the Step 14 limits section (not a schema file, and it has no arm)",
        "source": "decisions/0111 E6; task-sheet.md Step 14 and Step 13b",
    },
    {
        "step": "step8",
        "fills_blocks": ["channel_classes", "discovery_channel_overlap"],
        "label": "the Step 8 artifact (not a schema file, and it has no arm)",
        "source": "decisions/0114 E8; decisions/0111 E6",
    },
]
NON_ARM_LABELS = {src["step"]: src["label"] for src in NON_ARM_SOURCES}


def _input_label(step: str, arm: str | None) -> str:
    if arm is None:
        return ph(NON_ARM_LABELS[step])
    return ph(f"the Step {step[4:]} arm `{arm}` file")


def _document_scope(role: str, arm: str | None, step: str) -> dict:
    """What kind of document this is, and whose (decisions/0107, 0109 §1).

    ONE FILE PER STEP PER ARM. The merged document is Step 13b's, owned by the
    Human Lead, and it is the only writer that reads both arms because no arm can
    be that writer without defeating what dual implementation exists to do.
    """
    scope: dict = {
        "role": role,
        # The step whose output this file IS. Under decisions/0109 §1 that is a
        # single step: an arm file is one step's output for one arm.
        "producing_step": "step13b" if role == "merged_document" else step,
        "arm": arm,
        # EMPTY EVERYWHERE UNDER decisions/0109 §1. In an arm file because one
        # file is one step's output for one arm; in the merged document because
        # STEP 13b IS ITS ONLY WRITER -- the other steps' payloads arrive as
        # MERGED INPUTS, enumerated once at merge.sources_merged. Listing them
        # here as well would be a second place that list lives, and would read as
        # 'these steps write into the merged file', which is what the ruling
        # forbids. The field is present and empty: an absent field and an empty
        # one must not look alike.
        "also_written_by_steps": [],
        "isolation_rule": (
            "Each arm writes its own document, and no arm writes into a document another arm "
            "writes into. Neither instance sees the other's work, asks about it, or reads its "
            "output folder. It is the DIFF, between two files, that is the dual control."
        ),
        "note": ph(
            "the file's producing step, not its generator: $.generated_by names Step 8b, "
            "because this is the placeholder that shows the shape"
        ),
        "source": "decisions/0107; task-sheet.md Step 13b; CLAUDE.md, Dual implementation",
    }
    if role == "merged_document":
        scope["merge"] = {
            "owner_step": "step13b",
            "owner_role": "Human Lead, Step 13b, merged results document",
            # EIGHT SOURCES: seven arm files, one per step per arm
            # (decisions/0109 §1), and Step 14's limits section, which is a
            # NAMED NON-ARM-FILE SOURCE with its own provenance entry
            # (decisions/0111 E6). Each names its step and its arm, so a payload
            # can be read back against the source it came from -- which is what
            # makes the arity observable -- and check S30 now reads the relation
            # in BOTH directions, so a merge that DROPS an entire declared source
            # can no longer validate clean.
            "sources_merged": [
                {
                    "file_label": _input_label(s, a),
                    "source_kind": "arm_file",
                    "producing_step": s,
                    "arm": a,
                    "step_dual_status": STEP_DUALITY[s],
                    "source": "decisions/0109 §1; task-sheet.md Step 13b",
                }
                for s, a in MERGE_INPUTS
            ] + [
                {
                    "file_label": _input_label(src["step"], None),
                    "source_kind": "non_arm_file",
                    "producing_step": src["step"],
                    "arm": None,
                    "fills_blocks": src["fills_blocks"],
                    "source": src["source"],
                }
                for src in NON_ARM_SOURCES
            ],
            "diff": {
                "performed_by": "human_lead",
                "pairs_diffed": [
                    {
                        "producing_step": s,
                        "arm_a_file": _input_label(s, "a"),
                        "arm_b_file": _input_label(s, "b"),
                        "note": ph(
                            "two files, named separately: a merge assembled from one arm file "
                            "cannot fill this pair without naming a file that does not exist"
                        ),
                    }
                    for s in sorted({s for s, a in MERGE_INPUTS if STEP_DUALITY[s] == "dual"})
                ],
                "figures_compared": SENT_C,
                "divergences_found": SENT_C,
                "record": ph("where the diff itself is recorded, outside this file"),
            },
            "blocks_only_the_merge_may_fill": ["cross_arm_divergences", "limitations"],
            "source": "task-sheet.md Step 13b; decisions/0107 §6; decisions/0109 §1",
        }
    return scope


# WHICH (SETTING, PRODUCING STEP) ENTRIES EXIST (decisions/0111 E2). An arm
# entry is ONE STEP'S MEASUREMENT AT ONE SETTING, so the same setting appears
# once per step that measures there -- Step 9's W = 108 and Step 13's W = 108 are
# both here, which is exactly what the ruling requires and what the old W-only
# key could not hold. The list is not restricted by "which step may occupy a
# shared W": that would make the schema decide an ownership question the spec
# does not.
ARM_ENTRIES = [
    # (arm_id, W, origin, in_grid, is_the_adopted_setting, producing_step,
    #  note, premiere_arm_with_no_producers, deriv_liveness_superseded)
    ("W108_s2_finale", 108, "s2_finale", True, True, "step9",
     "the adopted arm; T0 is the later of the S2 finale and the first-pass S1 completion "
     "date. This entry is STEP 9's measurement at that setting",
     False, False),
    ("W108_s2_finale", 108, "s2_finale", True, True, "step10",
     "the adopted setting again, as STEP 10's entry: it publishes the abandonment "
     "distribution here and no headline of its own, which is why its headline payload slot "
     "carries an explicit absence rather than a copy of Step 9's figure. THAT ABSENCE IS "
     "ABOUT THE HEADLINE BLOCK AND NOTHING ELSE. Step 10 measures outcome shares on this, "
     "the primary arm, under the fixed bootstrap, so it DOES publish intervals -- both "
     "objects, at $.declared_intervals -- and is held to the pair by check S41 like every "
     "other producing step (Human Lead ruling, 2026-08-20). The previous worked example "
     "showed Step 10 through the absence alone, from which a reader could only conclude that "
     "Step 10 mandates intervals nowhere, WHICH IS FALSE",
     False, False),
    ("W108_s2_finale", 108, "s2_finale", True, True, "step13",
     "the adopted setting again, as STEP 13's measurement. Step 9's W = 108 and Step 13's "
     "W = 108 are DIFFERENT MEASUREMENTS OF ONE SETTING and both exist",
     False, False),
    ("W108_s2_finale", 108, "s2_finale", True, True, "step11",
     "the adopted setting as STEP 11's entry: the arm its subpopulation cuts are computed at. "
     "The unconditional headline here is Step 9's and is not restated, so this entry's "
     "headline payload slot carries an explicit absence",
     False, False),
    ("W108_s2_finale", 108, "s2_finale", True, True, "step12",
     "the adopted setting as STEP 12's entry, for the same reason as Step 11's: its cuts name "
     "this arm as their base and the base has to resolve to an entry",
     False, False),
    ("W091_s2_finale", 91, "s2_finale", True, False, "step9",
     "a grid arm at 91 days, finale-anchored, distinct from the premiere-anchored arm; this "
     "is Step 9's entry at that setting",
     False, True),
    ("W091_s2_finale", 91, "s2_finale", True, False, "step13",
     "the same grid arm as Step 13's own measurement",
     False, False),
    ("W091_s2_premiere", 91, "s2_premiere", False, False, "step9",
     "Step 9's second headline at Netflix's own 91-day reporting window, anchored on the "
     "later of the S2 premiere and the first-pass S1 completion date; it sits on a different "
     "origin from the primary headline and the two are NOT the same measurement at two "
     "window lengths",
     True, False),
]


def _arms_for(role: str, arm: str | None, step: str, dual_arms: tuple) -> list:
    """The $.arms spine for one file, under ONE FILE PER STEP PER ARM.

    The merged document carries every producing step's entries. An ARM FILE
    carries only its own step's, because an arm entry is now identified by its
    producing step as well as by (W_days, clock_origin) -- decisions/0111 E2 --
    and one file is one step's output for one arm.

    A single-arm step's file keeps the spine with the headline payload slot
    recording why it holds no payload: the legal spine reviewer-engineering's M9
    asked for, emitted rather than described.
    """
    merged = role == "merged_document"
    if merged:
        return [
            _arm(arm_id, w, origin, in_grid, primary, note, s, dual_arms,
                 blocks_have_producers=not premiere, deriv_liveness_superseded=superseded)
            for (arm_id, w, origin, in_grid, primary, s, note, premiere, superseded)
            in ARM_ENTRIES
        ]
    mine = [e for e in ARM_ENTRIES if e[5] == step]
    if mine:
        return [
            _arm(arm_id, w, origin, in_grid, primary, note, s, dual_arms,
                 blocks_have_producers=not premiere, deriv_liveness_superseded=superseded)
            for (arm_id, w, origin, in_grid, primary, s, note, premiere, superseded) in mine
        ]
    # A single-arm step with no entry of its own in the table above -- Steps 11
    # and 12. One arm entry: the setting its cuts are computed at, which is the
    # base_arm_id those cuts name, and nothing else.
    return [
        _arm(
            "W108_s2_finale", 108, "s2_finale", True, True,
            "the arm this step's subpopulation cuts are computed at; the unconditional "
            "headline at this arm is Step 9's and is not restated here",
            step, dual_arms,
        )
    ]


# WHICH STEP MAY DECLARE AN INTERVAL ON EACH QUANTITY CLASS (decisions/0114 E11).
# W is derived at Step 6 and reported at Step 9's two window arms and across Step
# 13's grid; STEPS 10, 11 AND 12 DO NOT VARY IT. Held here and in
# src/step8b_validate.py, where check S38 reads it -- the validator's copy is the
# one that decides, for the reason S31 records: a table read from the file under
# test could only agree with itself.
#
# STEP 10 JOINED `outcome_shares` ON A HUMAN LEAD RULING, 2026-08-20: it measures
# outcome shares on the primary arm under a fixed bootstrap, which is a quantity
# with a real interval. It did NOT join `window_w_percentile` -- the ruling's
# ground is the outcome shares and Step 10 does not vary W. The reasoning is
# written out at the validator's copy, which is the one that decides.
INTERVAL_CLASS_PUBLISHERS = {
    "outcome_shares": ("step9", "step10", "step11", "step12", "step13"),
    "window_w_percentile": ("step9", "step13"),
}


# WHICH (STEP, ARM) OWNERS CARRY INTERVALS IN THE MERGED DOCUMENT (v1.8.0,
# reviewer-engineering E3). Check S41 keys on the pair, because in a merged
# document `sole` is Steps 10, 11 and 12 together and `a` is Step 9 AND Step 13 --
# so a movement declared under `a` used to discharge two steps' obligations at
# once. The merged placeholder must therefore declare a paired movement PER
# OWNER, not per arm.
#
# WHO IS ABSENT AND WHY, because an owner missing from a list reads as an
# oversight: STEP 12 lists candidate cuts and mandates intervals nowhere
# ($defs.ci_or_absence; Human Lead ruling, 2026-08-19), so its cut's shares carry
# the CI-ABSENCE form and it owes none. An owner that published a level and no
# movement WOULD fail S41, exemption or not.
#
# STEP 10 JOINED THIS LIST ON A HUMAN LEAD RULING, 2026-08-20, AND ITS PREVIOUS
# ABSENCE WAS THE DEFECT. This comment used to excuse it: "Step 10's headline
# payload in this placeholder is an absence record -- it charts the headline arm
# rather than publishing its own -- so it carries no interval and owes no
# movement." WITHDRAWN. The headline absence is about the HEADLINE BLOCK; it says
# nothing about intervals, and Step 10 measures outcome shares on the primary arm
# under the fixed bootstrap, which is a quantity with a real interval. The worked
# example showed Step 10 through that absence alone, so the only Step 10 a reader
# could see here was one that publishes no interval anywhere -- which would make
# "Step 10 mandates intervals nowhere" true of the placeholder while being false
# of Step 10.
MERGED_INTERVAL_OWNERS = (
    ("step9", "a"), ("step9", "b"),
    ("step13", "a"), ("step13", "b"),
    ("step10", "sole"), ("step11", "sole"),
)


def _interval_step_for(role: str, step: str, arm: str) -> str:
    """Whose interval an entry in this file is.

    In an arm file, the file's own step: one file is one step's output for one
    arm, and an interval is a measurement like any other (decisions/0114 E11).
    In the merged document, the step that supplied that arm's file.
    """
    if role != "merged_document":
        return step
    return "step9" if arm in ("a", "b") else "step11"


def _step8_block_absence(reason: str) -> dict:
    """The ABSENCE IDIOM an arm file uses for a block Step 13b fills (0114 E8).

    `owning_step` is `step13b`, which is where the block arrives -- not `none`,
    because a producer DOES exist for it; it is simply not this file's step.
    """
    return {
        "block_is_absent": True,
        "status": "not_required_by_spec",
        "reason": reason,
        "owning_step": "step13b",
        "source": "decisions/0114 E8; decisions/0109 §1",
    }


def _declared_intervals(role: str, step: str, arms_held: tuple) -> list:
    """The intervals this file declares, ATTRIBUTED TO A STEP THAT PRODUCES THEM.

    CORRECTED AT v1.5.0 (decisions/0114 E11). Both entries used to be the WINDOW-W
    PERCENTILE, and for the `sole` arm they were attributed to `step11` -- WHICH
    DOES NOT COMPUTE W. `$.declared_intervals` sat outside ENTRY_FAMILIES and
    outside TOP_LEVEL_PUBLISHER, so nothing asked whose interval an entry was and
    nothing caught it; the shipped single-arm placeholder and the merged
    placeholder both carried it.

    The two branches the placeholder must exercise are UNIT AGREEMENT and UNIT
    DISAGREEMENT with the class's binding cluster, and both survive the fix: a
    step that may publish a window-W interval declares that pair, and a step that
    may not declares the same pair on its own outcome-shares quantity, which is
    account-bound and so disagrees in the other direction.

    A THIRD ENTRY PER ARM AT v1.6.0 (decisions/0118): THE PAIRED MOVEMENT. The
    statistic is fixed as BOTH, so a file that declared only levels would be
    INCOMPLETE rather than differently designed -- and a branch described in prose
    and never emitted cannot be checked. Every arm therefore declares one movement
    interval as well as its levels, which is what makes check S41 non-vacuous on
    all three placeholders.
    """
    out = []
    # THE PAIRED MOVEMENT, ONE PER (STEP, ARM) OWNER (v1.8.0, E3). It used to be
    # one per ARM, which is the same thing in an arm file and is NOT in the merged
    # document, where one arm label covers several steps -- so Step 13 arm `a`'s
    # movement discharged Step 9 arm `a`'s obligation and Step 13 declared none of
    # its own. It is emitted BEFORE the branch split so that no branch can drop
    # it: the requirement is a property of the run, not of which quantities a step
    # happens to publish.
    movement_owners = (MERGED_INTERVAL_OWNERS if role == "merged_document"
                       else tuple((step, a) for a in arms_held))
    for istep, a in movement_owners:
        out.append({
            "interval_id": (f"paired_movement_{istep}_{a}" if role == "merged_document"
                            else f"paired_movement_{a}"),
            "quantity": ph(
                "a PAIRED MOVEMENT -- the difference between two configurations of the same "
                "share, resampled as a paired delta rather than as two independent levels. "
                "Which two configurations is the writer's to state; the schema requires that "
                "the object exists and is labelled"
            ),
            "produced_by_step": istep,
            "producing_arm": a,
            "ci": _ci(f"{a}_default", unit="account", quantity_class="outcome_shares",
                      statistic="movements"),
            "note": ph(
                "THE SECOND OF THE TWO OBJECTS THE SPEC FIXES (decisions/0118). A level and a "
                "movement are NEVER compared to each other: on APPLY the never-started level "
                "is an order of magnitude wider than its movement, so an unlabelled interval "
                "misleads by that much. This entry is what stops the movement branch being a "
                "shape the schema allows and nothing exercises"
            ),
            "source": "decisions/0118",
        })
    # STEP 10'S LEVELS, IN THE MERGED DOCUMENT (Human Lead ruling, 2026-08-20).
    # The movement above is emitted for every owner in MERGED_INTERVAL_OWNERS,
    # which Step 10 has now joined; this is its counterpart level, so the owner
    # `step10/sole` carries BOTH objects and S41 reaches it like any other.
    #
    # IT IS NOT REACHED BY THE `arms_held` LOOP BELOW: that loop maps an ARM to a
    # step, and in the merged document `sole` maps to Step 11 -- one arm label,
    # three single-arm steps, which is the collision S41's owner key exists for.
    # So Step 10's own quantity is written here rather than inferred from an arm.
    #
    # THE QUANTITY IS THE ONE THE RULING NAMES: the outcome shares at the primary
    # arm, account-bound, resampled at the account, so the unit agrees with the
    # binding cluster and no disagreement record is present.
    if role == "merged_document":
        out.append({
            "interval_id": "outcome_shares_step10_sole",
            "quantity": ph(
                "the outcome shares Step 10 measures at the primary arm, whose binding "
                "cluster is the ACCOUNT. Step 10 charts the headline arm and does not restate "
                "Step 9's headline figure -- but the shares it charts are measured under the "
                "fixed bootstrap and carry a real interval, which is why its headline-block "
                "absence record does not mean it publishes no interval"
            ),
            "produced_by_step": "step10",
            "producing_arm": "sole",
            "ci": _ci("sole_default", unit="account", quantity_class="outcome_shares"),
            "note": ph(
                "THE FIRST OF THE TWO OBJECTS, for an owner that used to appear in this "
                "document only as a headline absence (Human Lead ruling, 2026-08-20). Step 10 "
                "is a publisher of `outcome_shares` and is NOT exempt from the both-objects "
                "requirement; it is not a publisher of the window-W percentile, which it does "
                "not compute"
            ),
            "source": "Human Lead ruling 2026-08-20; decisions/0118; decisions/0114 E11",
        })
    for a in arms_held:
        istep = _interval_step_for(role, step, a)
        if istep in INTERVAL_CLASS_PUBLISHERS["window_w_percentile"]:
            out.append({
                "interval_id": f"window_w_percentile_{a}",
                "quantity": ph("the window W percentile, whose binding cluster is the SHOW"),
                "produced_by_step": istep,
                "producing_arm": a,
                "ci": _ci(f"{a}_show_clustered", unit="show",
                          quantity_class="window_w_percentile"),
                "note": ph(
                    "the unit agrees with the binding cluster declared for this class, so no "
                    "disagreement record is present -- this is the branch a show-bound "
                    "quantity takes when it is resampled correctly"
                ),
                "source": "decisions/0103 §2; decisions/0024, 0026",
            })
            out.append({
                "interval_id": f"window_w_percentile_account_clustered_{a}",
                "quantity": ph(
                    "the same show-bound quantity resampled at the ACCOUNT level, which "
                    "UNDERSTATES it"
                ),
                "produced_by_step": istep,
                "producing_arm": a,
                "ci": _ci(f"{a}_default", unit="account",
                          quantity_class="window_w_percentile", disagreement=True),
                "note": ph(
                    "the unit differs from the binding cluster for this class, so the "
                    "interval carries an unreconciled disagreement record: report a material "
                    "disagreement, do not reconcile it"
                ),
                "source": "decisions/0103 §2",
            })
            continue
        # A STEP THAT DOES NOT COMPUTE W. Its interval is on a quantity it does
        # produce -- the share it recomputes on its own cut -- and the two
        # branches are exercised on that instead. The disagreement runs the other
        # way here: the binding cluster for outcome shares is the ACCOUNT, so a
        # show-resampled interval is the one that must carry the record.
        out.append({
            "interval_id": f"cut_share_{a}",
            "quantity": ph(
                "a share this step recomputes on its own subpopulation, whose binding cluster "
                "is the ACCOUNT"
            ),
            "produced_by_step": istep,
            "producing_arm": a,
            "ci": _ci(f"{a}_default", unit="account", quantity_class="outcome_shares"),
            "note": ph(
                "the unit agrees with the binding cluster declared for this class, so no "
                "disagreement record is present"
            ),
            "source": "decisions/0103 §1; decisions/0114 E11",
        })
        out.append({
            "interval_id": f"cut_share_show_clustered_{a}",
            "quantity": ph(
                "the same account-bound share resampled at the SHOW level, which is not its "
                "binding cluster"
            ),
            "produced_by_step": istep,
            "producing_arm": a,
            "ci": _ci(f"{a}_show_clustered", unit="show", quantity_class="outcome_shares",
                      disagreement=True, binding="account"),
            "note": ph(
                "the unit differs from the binding cluster for this class, so the interval "
                "carries an unreconciled disagreement record: report a material disagreement, "
                "do not reconcile it"
            ),
            "source": "decisions/0103 §2; decisions/0114 E11",
        })
    return out


def _stamp_merged_from(inst: dict) -> None:
    """Name the input file every merged payload came from (M1).

    ISOLATION IS UNOBSERVABLE, BUT ARITY IS OBSERVABLE. A merged document
    assembled from ONE arm file -- one payload deep-copied into the other arm's
    slot and relabelled -- validated clean before v1.3.0 and published that the
    arms agreed everywhere. Every payload now names the file it came from, and
    check S30 asserts that a block holding two arms names two DIFFERENT files.
    """
    labels = {(s, a): _input_label(s, a) for s, a in MERGE_INPUTS}
    single_arm_steps = {s for s, a in MERGE_INPUTS if a == "sole"}

    def visit(node):
        if isinstance(node, dict):
            if "producing_arm" in node and "written_by_step" in node:
                key = (node["written_by_step"], node["producing_arm"])
                if key in labels:
                    node["merged_from"] = labels[key]
            if "producing_arm" in node and "produced_by_step" in node:
                key = (node["produced_by_step"], node["producing_arm"])
                if key in labels:
                    node["merged_from"] = labels[key]
            # A SINGLE-ARM STEP'S BLOCK HAS NO `producing_arm` FIELD AND STILL
            # CAME FROM A FILE. Step 10's abandonment distribution is the case:
            # its arm is `sole` by construction, so it was left unstamped, and
            # its declared input was therefore named by nothing. Under S30's old
            # one-way reading that was invisible (decisions/0111 E3b).
            if ("producing_arm" not in node and "merged_from" not in node
                    and node.get("written_by_step") in single_arm_steps):
                node["merged_from"] = labels[(node["written_by_step"], "sole")]
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)

    visit(inst)
    # The NON-ARM-FILE source (decisions/0111 E6): Step 14's limits section. Its
    # payloads are not per-arm, so they are stamped by the block the source
    # declares it fills rather than by walking arm keys.
    for src in NON_ARM_SOURCES:
        label = _input_label(src["step"], None)
        for block in src["fills_blocks"]:
            node = inst.get(block)
            # A NON-ARM SOURCE MAY FILL A LIST OR AN OBJECT. `limitations` is a
            # list of entries; `channel_classes` is one object. Stamping only
            # lists would have left Step 8's block unstamped, which is the
            # unnamed-source case decisions/0111 E3b closed for arm files.
            if isinstance(node, list):
                for entry in node:
                    if isinstance(entry, dict):
                        entry["merged_from"] = label
            elif isinstance(node, dict):
                node["merged_from"] = label


def build_placeholder(provenance: dict, grid: list[int],
                      role: str = "merged_document", arm: str | None = None,
                      step: str = "step13b") -> dict:
    """One placeholder instance.

    `role` selects between the two document shapes decisions/0107 creates and
    `step` selects whose file it is, because decisions/0109 §1 makes granularity
    ONE FILE PER STEP PER ARM. Three shapes are emitted: the MERGED document Step
    16 renders from, a DUAL step's arm file (Step 9, arm a) and a SINGLE-ARM
    step's own file (Step 11, arm `sole`). The third exists because a single-arm
    step's file must have a legal spine (reviewer-engineering M9) and a spine
    described in prose and never emitted cannot be checked.
    """
    merged = role == "merged_document"
    dual_arms = ("a", "b") if merged else (arm,)
    arms_held = ("a", "b", "sole") if merged else (arm,)
    holds_sole = merged or arm == "sole"
    inst: dict = {
        "schema_version": SCHEMA_VERSION,
        "schema_id": SCHEMA_ID,
        "placeholder": True,
        "placeholder_notice": {
            "banner": (
                "############  THIS FILE IS A PLACEHOLDER. IT CONTAINS NO MEASUREMENTS.  "
                "############  Every number in it is the sentinel -999 or -999.0 and every "
                "writer-supplied string is prefixed 'PLACEHOLDER — NOT A MEASUREMENT'. It "
                "exists so Step 16 can be built before results exist. DO NOT PUBLISH, DO NOT "
                "CHART, DO NOT QUOTE. A consumer that renders it will show -999% bars, which "
                "is the point.  ############"
            ),
            "is_placeholder": True,
            "do_not_publish": True,
            "every_measurement_slot_is_a_sentinel": True,
            "how_to_tell": (
                "Read $.placeholder. If it is true, nothing in this file is a measurement. "
                "The sentinel scheme is at $.sentinels and is enforced by check S5 of "
                "src/step8b_validate.py."
            ),
            "generated_for": (
                "Step 16, so the visualization can be built before results exist"
                if merged
                else f"{step}, arm {arm!r}, so that writer has its own file's shape to write "
                     f"into rather than inventing one"
            ),
        },
        "generated_by": provenance,
        "document_scope": _document_scope(role, arm, step),
        "sentinels": {
            "count": SENT_C,
            "percent": SENT_P,
            "string_prefix": PH,
            "rule": (
                "Structure is real, measurements are sentinels. Identifiers, keys, enum "
                "values, booleans, refs, definitions and the provenance block are written as "
                "they would really appear, so every branch can be built against. Every slot "
                "the schema marks x-measurement holds -999 or -999.0, and every slot it marks "
                "x-writer-text carries the string prefix. Both are reserved: neither may "
                "appear in a file whose `placeholder` flag is false, which is what stops a "
                "leftover placeholder value surviving into a published file."
            ),
        },
        "adopted_rule_revision": dict(
            _revision_record(),
            # MERGED DOCUMENT ONLY: the merge assembles files written at
            # different times, so "this document's revision" is not one number
            # and the set is enumerated. In an arm file the field is absent --
            # one file is one run, and one run is one revision.
            **({"revisions_present": [_revision()]} if merged else {}),
        ),
        "arm_key": {
            "fields": ["W_days", "clock_origin", "producing_step", "adopted_rule_revision"],
            "note": (
                "THE ADOPTED-RULE REVISION IS THE FOURTH FIELD (decisions/0114 E14), and it is "
                "READ from processed/step5/adopted_rule.json at write time rather than typed: "
                "$.adopted_rule_revision names the file, the key and the hash. Two runs at one "
                "setting under different rule revisions are DIFFERENT MEASUREMENTS, and that "
                "dimension has been occupied once already -- that file carried revision-3 "
                "figures against the approved revision-6 rule. "
                "THE PRODUCING STEP IS PART OF THE KEY (decisions/0111 E2): Step 9's W = 108 "
                "and Step 13's W = 108 are DIFFERENT MEASUREMENTS OF ONE SETTING and both "
                "exist as entries. That is the collision below, one dimension out, with the "
                "same fix -- add the missing identity dimension, never restrict which step may "
                "occupy a shared W. "
                "W alone does not identify an arm either. Step 9 reports a second 91-day headline "
                "anchored on the S2 premiere rather than the finale, and states plainly that "
                "it is not the same measurement at another window length -- so it would "
                "collide with the finale-anchored W = 91 grid arm under a W-only key. There is "
                "no liveness threshold in the key: one was derived three times and deleted, "
                "and the adopted rule is parameter-free."
            ),
            "no_liveness_threshold": True,
        },
        "arm_grid_days": grid,
        "populations": {
            "APPLY": {
                "label": "APPLY",
                "definition": (
                    "Waterfall line 1 less D10 -- the population Step 8 filters at position 6."
                ),
                "source": "task-sheet.md Step 8; decisions/0048, 0054",
                "reference_n_at_the_adopted_arm": SENT_C,
            },
            "DERIV": {
                "label": "DERIV",
                "definition": (
                    "Waterfall line 4 less D10 -- requires S2 evidence. Step 8 produces both "
                    "populations so that nothing downstream rebuilds one of them."
                ),
                "source": "task-sheet.md Step 8; decisions/0070 ruling 1",
                "reference_n_at_the_adopted_arm": SENT_C,
            },
        },
        "scope_qualifiers": {
            "insertion_dormancy_covering": {
                "text": (
                    "The bound is covering with respect to insertion-dormancy, exhaustively; "
                    "open only across channel classes (D4, D9)."
                ),
                "covering_with_respect_to": "insertion-dormancy",
                "covering_is_exhaustive": True,
                "open_across": ["D4", "D9"],
                "stopping_rule": (
                    "Concede every pair that was dormant before the instant at which its own "
                    "state-defining null is read: tau1 for the never-started null, tau2 for "
                    "the Continued null. Every pair either was inserting through its test "
                    "instant or was not, so the rule terminates with no residue."
                ),
                "source": "decisions/0062",
            }
        },
        "bootstrap_spec": {
            "B": BOOTSTRAP_B,
            "seed": BOOTSTRAP_SEED,
            "resampling_unit_for_outcome_shares": "account",
            "statistics": list(BOOTSTRAP_STATISTICS),
            "identical_for_both_arms": True,
            "seed_value_is_arbitrary_its_fixity_is_the_point": True,
            "fields_considered": list(BOOTSTRAP_FIELDS_CONSIDERED),
            "fields_fixed_in_spec": list(BOOTSTRAP_FIELDS_CONSIDERED),
            "fields_not_fixed_in_spec": [],
            "why_both_statistics": (
                "The requirement exists so the diff compares like with like, and both arms "
                "producing both objects satisfies that fully: a divergence on either object is "
                "then a real divergence rather than a design difference. Neither may be "
                "dropped, because they are DIFFERENT OBJECTS -- on APPLY the never-started "
                "level is an order of magnitude wider than its movement -- so a reader who is "
                "not told which one they are reading is wrong by that much. Same reasoning as "
                "publishing the floor and the ceiling rather than a point. The magnitudes are "
                "cited to decisions/0118 rather than restated here, because a figure copied "
                "into a schema is a second place that figure lives."
            ),
            "why_account_level": (
                "Pairs are not independent -- one account contributes many -- so pair-level "
                "resampling understates the interval. The clustering has been measured on "
                "this build and the measurement is cited rather than restated here, because a "
                "figure copied into a schema is a second place that figure lives."
            ),
            "source": "decisions/0103 §1; decisions/0118; task-sheet.md Step 9",
        },
        "binding_clusters": {
            "outcome_shares": {
                "binding_cluster": "account",
                "evidence": (
                    "Pairs cluster within accounts; the account-clustered and i.i.d. "
                    "intervals for this build's threshold are on the record at the cited "
                    "source, which is where they stay."
                ),
                "source": "decisions/0103 §1, citing decisions/0039",
            },
            "window_w_percentile": {
                "binding_cluster": "show",
                "evidence": (
                    "W's interval is show-clustered and the spec names the show as the "
                    "binding cluster there, so account-level resampling would UNDERSTATE it. "
                    "The measurements are at the cited source."
                ),
                "source": "decisions/0103 §2, citing decisions/0024 and 0026",
            },
            "other_declared": {
                "binding_cluster": "account",
                "evidence": (
                    "A class the record has not separately ruled on. A writer using it must "
                    "state why the account is binding for that quantity; the class exists so "
                    "that an undeclared quantity cannot pick up `account` by default."
                ),
                "source": "reviewer-engineering F3 residue; decisions/0103 §2",
            },
        },
        "bootstrap_settings": {k: v for k, v in {
            "a_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistics": list(BOOTSTRAP_STATISTICS),
                "resampling_unit": "account",
                "producing_arm": "a",
                "spec_status": "fixed_in_spec",
                "fields_considered": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_fixed_in_spec": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_not_fixed_in_spec": [],
                "note": ph(
                    "all four elements are fixed by the spec -- decisions/0103 for B, the seed "
                    "and the unit, decisions/0118 for the statistic -- and all four are real "
                    "here rather than sentinels. This entry no longer records a per-arm choice "
                    "on any of them"
                ),
            },
            "b_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistics": list(BOOTSTRAP_STATISTICS),
                "resampling_unit": "account",
                "producing_arm": "b",
                "spec_status": "fixed_in_spec",
                "fields_considered": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_fixed_in_spec": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_not_fixed_in_spec": [],
                # THE CLAIM IS CORRECTED, NOT MARKED. decisions/0119 §5 said S32
                # "catches an arm MISLABEL"; reviewer-engineering called that one
                # notch too strong on the v1.6.0 review and this arm agrees. S32
                # compares TWO OF THE WRITER'S OWN DECLARATIONS -- which arm a
                # payload sits under, and which arm the referenced registry entry
                # says produced it -- so what it catches is an INCOHERENT pair. A
                # writer that mislabels BOTH consistently is unobservable to it,
                # and with all four elements fixed there is no longer any settings
                # difference to expose the inconsistency either.
                "note": ph(
                    "as above, for the other arm. It is IDENTICAL to a_default except for "
                    "producing_arm, and that is what decisions/0118 did: "
                    + _REGISTRY_ARM_DIFFERENCE_FACT
                    + ", so check S32 catches an INCOHERENT arm reference -- a payload under "
                    "one arm pointing at the other arm's entry -- and no longer catches a "
                    "settings mismatch, because there is none left to catch. It does NOT catch a "
                    "COHERENT mislabel: both sides are the writer's own declarations, so a file "
                    "that labels a payload and its settings entry with the same wrong arm is "
                    "unobservable here and only the Human Lead's diff reaches it"
                ),
            },
            "sole_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistics": list(BOOTSTRAP_STATISTICS),
                "resampling_unit": "account",
                "producing_arm": "sole",
                "spec_status": "fixed_in_spec",
                "fields_considered": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_fixed_in_spec": list(BOOTSTRAP_FIELDS_CONSIDERED),
                "fields_not_fixed_in_spec": [],
                "note": ph("the single-arm steps, 10 to 12, which have no second arm to "
                           "diff against. The statistic is fixed for them too: it is a "
                           "property of the spec, not of having a counterpart arm"),
            },
            # SHOW-CLUSTERED SETTINGS, one per arm. The binding cluster is NOT
            # the same for every quantity (decisions/0103 §2): W's interval is
            # show-clustered and account-level resampling would UNDERSTATE it.
            # Without an entry whose unit is `show`, no interval could name one.
            **{
                f"{a}_show_clustered": {
                    "B": BOOTSTRAP_B,
                    "seed": BOOTSTRAP_SEED,
                    "statistics": list(BOOTSTRAP_STATISTICS),
                    "resampling_unit": "show",
                    "producing_arm": a,
                    "spec_status": "partly_fixed_in_spec",
                    # THE UNIT IS THE ONE FIELD THIS ENTRY DOES NOT INHERIT FROM
                    # THE SPEC. decisions/0103 fixes `account` for the OUTCOME
                    # SHARES specifically, so a show-bound quantity's unit is
                    # settled by its binding cluster rather than by that ruling
                    # -- which is why `spec_status` stays partly_fixed_in_spec
                    # here while the default entries became fixed_in_spec. B,
                    # the seed and the statistic are fixed for every entry.
                    "fields_considered": list(BOOTSTRAP_FIELDS_CONSIDERED),
                    "fields_fixed_in_spec": ["B", "seed", "statistics"],
                    "fields_not_fixed_in_spec": ["resampling_unit"],
                    "note": ph(
                        "the show-clustered settings for a show-bound quantity; the unit is "
                        "NOT the account here, and the ruling's per-interval unit field is "
                        "exactly what makes that visible"
                    ),
                }
                for a in ("a", "b", "sole")
            },
        }.items() if k in _refs_in_scope(arms_held)},
        "step_duality": {
            s: {
                "dual_status": STEP_DUALITY[s],
                "source": STEP_DUALITY_SOURCE[s],
                "note": (
                    "Read against by_producing_arm.producing_step by check S31. Duality is a "
                    "fixed fact of the spec, so a block cannot declare its own."
                ),
            }
            for s in sorted(STEP_DUALITY)
        },
        # M10: a show-unit interval and the unit_disagreement subtree, both
        # exercised, so Step 16 is built against the branches decisions/0103 §2
        # exists to protect rather than against the account-clustered case alone.
        "declared_intervals": _declared_intervals(role, step, arms_held),
        "block_ownership": _block_ownership(),
        # ARM FILES DO NOT CARRY THESE TWO (decisions/0114 E8). They hold STEP
        # 8's figures, and `channel_classes` was required at the top level of
        # every file -- so seven arm files each had to fill a figure none of them
        # produced, with no precedence rule and no agreement check. The merged
        # document carries them once, filled at Step 13b from Step 8's artifact,
        # and an arm file states the absence: ABSENCE STATED, NOT SILENCE, which
        # is why the slot stays present rather than being made optional.
        **({} if merged else {
            "channel_classes": _step8_block_absence(
                "D4 and D9 are STEP 8's figures and Step 9 is forbidden to recompute either. "
                "Requiring this block in seven arm files would make seven writers of one "
                "figure, with no precedence rule and no agreement check; the merged document "
                "carries it once, filled at Step 13b from Step 8's artifact."),
            "discovery_channel_overlap": _step8_block_absence(
                "The discovery-channel overlap is STEP 8's measurement, published in four "
                "units with a different consumer for each. Same shape as channel_classes, "
                "checked rather than assumed: the merged document carries it once."),
        }),
        **({"channel_classes": {
            "d4": {
                "definition": "S3 or later evidence without S2 evidence.",
                "published_alongside": True,
                "folded_into_bound": False,
                "computed_by": "step8",
                "copied_not_computed": True,
                "counts": {"APPLY": SENT_C, "DERIV": SENT_C},
                "source": "decisions/0070 ruling 7",
            },
            "d9": {
                "published_alongside": True,
                "folded_into_bound": False,
                "computed_by": "step8",
                "copied_not_computed": True,
                "keys": {
                    "strict": "lowercase the slug and drop every non-alphanumeric character",
                    "loose": "remove a trailing four-digit year first, then apply strict",
                    "third_key_is_not_an_endpoint": (
                        "A key that strips a trailing digit group of arbitrary length is a "
                        "third key, not an endpoint of this bound; its answer is reported as a "
                        "divergence."
                    ),
                },
                "universe": {
                    "label": "U1",
                    "definition": (
                        "Every distinct show ID appearing anywhere in the pulled sweep that "
                        "carries a slug, deduplicated to one row per show ID."
                    ),
                    "n_show_ids": SENT_C,
                    "rank_basis": "distinct strict keys merged",
                    "rank_tie_break": {
                        "status": "unruled",
                        "reason": (
                            "The rank ordering ties and no rule specifies the tie-break, so no "
                            "single name may be published at a tied rank; every key at the "
                            "tied rank is listed instead."
                        ),
                        "source": "decisions/0089 §2(c)",
                    },
                },
                "quantities": {
                    "complementary_pairs": _d9_quantity(),
                    "half_a": _d9_quantity(),
                    "half_b": _d9_quantity(),
                },
            },
        },
        "discovery_channel_overlap": [
            {
                "unit": "discovery_pool_usernames",
                "numerator": SENT_C,
                "denominator": SENT_C,
                "consumer": ph("Step 3's seeding-bias statement"),
                "single_categorical_forbidden": True,
                "source": "decisions/0079",
            },
            {
                "unit": "accounts_pulled",
                "numerator": SENT_C,
                "denominator": SENT_C,
                "consumer": ph("Step 4 coverage"),
                "single_categorical_forbidden": True,
                "source": "decisions/0079",
            },
            {
                "unit": "analysis_population_accounts",
                "numerator": SENT_C,
                "denominator": SENT_C,
                "consumer": ph("Step 11, which cuts the analysis population"),
                "single_categorical_forbidden": True,
                "source": "decisions/0079",
            },
            {
                "unit": "analysis_population_pairs",
                "numerator": SENT_C,
                "denominator": SENT_C,
                "consumer": ph("Step 11, in pairs rather than accounts"),
                "single_categorical_forbidden": True,
                "source": "decisions/0079",
            },
        ]} if merged else {}),
        # `machine_checked` says which of these check S12 EVALUATES rather than
        # merely records. S12 asserts the flags against the set it actually
        # evaluated, so the check's title and the check's code are compared with
        # each other instead of the title being taken on trust.
        "derived_fields": [
            {
                "field": "$..bounds.*.width_pp",
                "expression": "ceiling.percent - floor.percent",
                "moves_with": ["floor", "ceiling"],
                "machine_checked": True,
                "checked_by": "src/step8b_validate.py check S12",
                "source": "CLAUDE.md, Derived figures",
            },
            {
                "field": "$..conditional_sub_interval.width_pp",
                "expression": "conditional_sub_interval.ceiling.percent "
                              "- conditional_sub_interval.floor.percent",
                "moves_with": ["started_and_left bound floor"],
                "machine_checked": True,
                "checked_by": "src/step8b_validate.py check S12",
                "source": "CLAUDE.md, Derived figures, item 2",
            },
            {
                "field": "$..ceilings_cannot_all_hold.sum_percent",
                "expression": "never_started.ceiling.percent + started_and_left.ceiling.percent "
                              "+ continued.ceiling.percent",
                "moves_with": ["any ceiling"],
                "machine_checked": True,
                "checked_by": "src/step8b_validate.py check S12",
                "source": "CLAUDE.md, Derived figures, Any ceiling",
            },
            {
                "field": "$..ceilings_cannot_all_hold.excess_pp",
                "expression": "sum_percent - 100",
                "moves_with": ["sum_percent"],
                "machine_checked": True,
                "checked_by": "src/step8b_validate.py check S12",
                "source": "CLAUDE.md, Derived figures, Any ceiling",
            },
            {
                "field": "$..shares.*.value_percent",
                "expression": "100 * numerator_pairs / denominator_pairs",
                "moves_with": ["the retained row count"],
                "machine_checked": True,
                "checked_by": "src/step8b_validate.py check S12",
                "source": "Step 9",
            },
            {
                "field": "$..ceilings_cannot_all_hold.excess_pairs",
                "expression": "2 * never_started_exclusions + started_and_left_exclusions",
                "moves_with": ["the exclusion split"],
                "machine_checked": False,
                "checked_by": (
                    "Not evaluated: the mechanism's second term is the started-and-left "
                    "exclusions PLUS the conceded channel pairs, and the channel-pair count "
                    "is not one of this block's own operands. Declared here, checked by the "
                    "writing step."
                ),
                "source": "decisions/0053 §4",
            },
            {
                "field": "$..bound_over_sampling_width_ratios.*.value",
                "expression": "bound width / that arm's sampling width",
                "moves_with": ["the corresponding bound width"],
                "machine_checked": False,
                "checked_by": (
                    "Not evaluated: the denominator is the arm's sampling width, which the "
                    "two arms define by two conventions the spec forbids reconciling, and it "
                    "is not stored as a number in this file."
                ),
                "source": "CLAUDE.md, Derived figures, items 4 and 5",
            },
        ],
        # THE MERGED DOCUMENT ONLY. An arm file omits this block: an isolated
        # instance is forbidden to have performed the search it records, and
        # under decisions/0107 the diff happens between two files, by the Human
        # Lead, before Step 13b merges them. Check S17 does not apply to a file
        # whose producing step is not the Human Lead's, and check S29 fails one
        # that carries the block anyway.
        **({"cross_arm_divergences": {
            "search": {
                "performed": True,
                "coverage_count": SENT_C,
                "what_was_searched": ph(
                    "which figures were compared, and how many; an empty list with a coverage "
                    "count reads as 'the arms agreed across N figures', while an empty list "
                    "with performed false reads as 'nobody has looked yet' -- the distinction "
                    "the previous version could not express"
                ),
                "owner_step": "human_lead",
                "empty_reason": None,
            },
            "entries": [
                {
                    "figure": ph("the figure the two arms differ on"),
                    "arm_a": ph("arm a's value or convention"),
                    "arm_b": ph("arm b's value or convention"),
                    "reconciled": False,
                    "reason": ph(
                        "why the difference is legitimate; the spec forbids reconciling it, so "
                        "both values are held"
                    ),
                    "source": ph("the decision entry that recorded it"),
                }
            ],
        }} if role == "merged_document" else {}),
        "arms": _arms_for(role, arm, step, dual_arms),
        **({"variants": [
            {
                "variant_id": "s1_completion_threshold_90",
                "adopted_rule_revision": _revision(),
                "axis": "s1_completion_threshold",
                "level": "90_percent",
                "base_arm_id": _arm_id("W108_s2_finale", "step13"),
                "producing_step": "step13",
                # Step 13 is DUAL (decisions/0103 §3), so its payload nests per
                # producing arm exactly as Step 9's does. Its per-arm sensitivity
                # shares carry no bound and no interval, and the slots say so
                # rather than demanding figures the spec never asks it for.
                "headline": {
                    "APPLY": _population_block("APPLY", False, False, dual=True,
                                               step="step13", bounds_present=False,
                                               ci_present=False, dual_arms=dual_arms),
                    "DERIV": _population_block("DERIV", True, True, dual=True,
                                               step="step13", bounds_present=False,
                                               ci_present=False, dual_arms=dual_arms),
                },
                # ALL FOUR PER PRODUCING ARM (decisions/0111 E1). Step 13 is
                # dual, so each of these was one slot where two arms write.
                "d3_prime": {
                    p: {"by_producing_arm": _per_arm_container(
                        "step13", dual_arms, lambda a, p=p: _d3_prime(p, 108, a))}
                    for p in POPULATIONS
                },
                "d2_recomputed_inside_this_arm": {
                    "by_producing_arm": _per_arm_container(
                        "step13", dual_arms, lambda a: {
                            "producing_arm": a,
                            "written_by_step": "step13",
                            "finale_binds": SENT_C,
                            "s1_completion_binds": SENT_C,
                            "both_bind": SENT_C,
                            "note": ph(
                                "the max() split is three categories, not two: a tie is its "
                                "own category, not a tiebreak, and the count is not "
                                "population-invariant"
                            ),
                        }),
                },
                "conclusions_surviving": {
                    "by_producing_arm": _per_arm_container(
                        "step13", dual_arms, lambda a: {
                            "producing_arm": a,
                            "written_by_step": "step13",
                            "conclusions": [
                                ph("one string per conclusion that survives, in this arm's "
                                   "words")],
                        }),
                },
                "conclusions_not_surviving": {
                    "by_producing_arm": _per_arm_container(
                        "step13", dual_arms, lambda a: {
                            "producing_arm": a,
                            "written_by_step": "step13",
                            "conclusions": [
                                ph("one string per conclusion that does not survive")],
                        }),
                },
            }
        ]} if merged or step == "step13" else {}),
        # Steps 11 and 12 are single-arm steps, and under decisions/0107 and
        # 0109 §1 they write their OWN files (arm `sole`, one file per step).
        # The cuts appear in the merged document and in those files; a DUAL
        # step's arm file does not carry them, because a file is one step's
        # output for one arm and `a` and `sole` are two arms. AND STEP 11's FILE
        # HOLDS STEP 11's CUTS ONLY: `sole` is not one shared arm, it is each
        # single-arm step's own, so Step 12's cut belongs in Step 12's file and
        # in the merge.
        **({"subpopulation_cuts": [cut for cut in [
            {
                "cut_id": "discovery_channel_a",
                "adopted_rule_revision": _revision(),
                "dimension": "discovery_channel",
                "level": "channel_a",
                "base_arm_id": _arm_id("W108_s2_finale", "step11"),
                "producing_step": "step11",
                # Step 11 is SINGLE-ARM: one payload under `sole`, and the
                # dual_status field says so. It is not a dual step writing an
                # absence for an arm it never had (reviewer-engineering F5).
                "headline": {
                    "APPLY": _population_block("APPLY", False, False, dual=False,
                                               step="step11", bounds_present=False),
                    "DERIV": _population_block("DERIV", True, True, dual=False,
                                               step="step11", bounds_present=False),
                },
                "candidate_considered": True,
                "selected_by_human_lead": False,
                "agreement_kind": "not_yet_assessed",
                "agreement_statement": ph(
                    "whether the channels agree, and whether 'agree' means genuinely similar "
                    "or merely not distinguishable at this sample size"
                ),
                "where_it_holds": ph("where the pattern holds"),
                "where_it_breaks": ph("where the pattern breaks"),
            },
            {
                "cut_id": "discovery_channel_both",
                "adopted_rule_revision": _revision(),
                "dimension": "discovery_channel",
                "level": "both",
                "base_arm_id": _arm_id("W108_s2_finale", "step11"),
                "producing_step": "step11",
                "headline": {
                    "APPLY": _population_block("APPLY", False, False, dual=False,
                                               step="step11", bounds_present=False),
                    "DERIV": _population_block("DERIV", True, True, dual=False,
                                               step="step11", bounds_present=False),
                },
                "candidate_considered": True,
                "selected_by_human_lead": False,
                "agreement_kind": "not_yet_assessed",
                "agreement_statement": ph(
                    "the overlap is its own level because discovery channel is two booleans, "
                    "not one categorical"
                ),
                "where_it_holds": ph("where the pattern holds"),
                "where_it_breaks": ph("where the pattern breaks"),
            },
            # STEP 12'S OWN CUT. Steps 11 and 12 both write into this array and
            # nothing in the file said which was which, so the merged document
            # could declare Step 12's file among its inputs and carry nothing
            # from it -- which it did, and no check could see it
            # (decisions/0111 E3b). A cut now names its producing step, and check
            # S30 reads the input list in both directions.
            {
                "cut_id": "gap_length_between_seasons_long",
                "adopted_rule_revision": _revision(),
                "dimension": "gap_length_between_seasons",
                "level": ph("one level of the segment cut this step lists"),
                "base_arm_id": _arm_id("W108_s2_finale", "step12"),
                "producing_step": "step12",
                # STEP 12'S SHARES CARRY THE CI-ABSENCE FORM (v1.8.0,
                # reviewer-engineering E2/E3). The Human Lead ruled on 2026-08-19
                # that the spec asks Step 12 for no interval, on this schema's own
                # warrant at $defs.ci_or_absence -- "Step 12 lists every candidate
                # cut and mandates intervals nowhere" -- and the placeholder is
                # the shape a writer fills in. Showing Step 12 with intervals
                # would show it manufacturing the two figures the ruling exists to
                # spare it; showing it with intervals but no paired movement is a
                # shape v1.8.0's S41 rejects, because the exemption covers a step
                # asked for NO interval and not a step that published half a run.
                # So the slot is present and says "not asked for", which is what
                # $defs.ci_or_absence was added for.
                "headline": {
                    "APPLY": _population_block("APPLY", False, False, dual=False,
                                               step="step12", bounds_present=False,
                                               ci_present=False),
                    "DERIV": _population_block("DERIV", True, True, dual=False,
                                               step="step12", bounds_present=False,
                                               ci_present=False),
                },
                "candidate_considered": True,
                "selected_by_human_lead": False,
                "agreement_kind": "not_yet_assessed",
                "agreement_statement": ph(
                    "every candidate considered is written here, not only the one that showed "
                    "a pattern"
                ),
                "where_it_holds": ph("where the pattern holds"),
                "where_it_breaks": ph("where the pattern breaks"),
            },
        ] if merged or cut["producing_step"] == step]} if holds_sole else {}),
        # PER PRODUCING ARM (decisions/0111 E1), and present only where this
        # file's step publishes it: it is Step 13's, and check S36 fails a file
        # that carries a block its own ownership table gives to another step.
        **({"tested_ranges": {
            "by_producing_arm": _per_arm_container("step13", dual_arms, lambda a: {
                "producing_arm": a,
                "written_by_step": "step13",
                "ranges": {
                    "W_days": {
                        "values": grid,
                        "min": min(grid),
                        "max": max(grid),
                        "source": "decisions/0075",
                    },
                    "s1_completion_threshold_percent": {
                        "values": [90, 100],
                        "min": 90,
                        "max": 100,
                        "source": "task-sheet.md Step 13",
                    },
                    "s1_completion_date_definition": {
                        "values": ["first_pass", "last_observed"],
                        "min": None,
                        "max": None,
                        "source": "task-sheet.md Step 13; Step 1 §5",
                    },
                },
                "note": ph(
                    "the ranges this arm actually tested; Step 16 binds its controls to them "
                    "so no reader can drive it somewhere that was never tested"
                ),
            }),
        }} if merged or step == "step13" else {}),
        # THE MERGED DOCUMENT ONLY, for the same reason as cross_arm_divergences:
        # it is one of the two blocks only the merge may fill, and it belongs to
        # the Human Lead, which no agent may draft.
        **({"limitations": [
            {
                "id": ph("one entry per limitation that travels with the result"),
                "text": ph(
                    "the limitation, in the words of the step that owns it; this array is "
                    "written by its owner, not by the schema"
                ),
                "source": ph("the decision entry or artifact that states it"),
                "direction": None,
                "may_be_netted_with_others": False,
            }
        ]} if role == "merged_document" else {}),
        "spec_choices_made_by_step_8b": [
            {
                "choice": "Step 8b ran as instance `a`.",
                "spec_gap": (
                    "Step 8b is a single-arm chained step and is not in the dual-implementation "
                    "list, and the spec does not name which instance runs it."
                ),
                "what_was_done": (
                    "It was run as arm `a` on the instruction of the agent that launched it. "
                    "The choice is the launcher's, not the spec's, and there is no second "
                    "instance to diff this schema against."
                ),
                "if_ruled_otherwise": (
                    "Nothing in the schema depends on it. It is recorded because an unstated "
                    "choice is the shape that has cost this study repeatedly."
                ),
            },
            {
                "choice": (
                    "STEP 8's ARTIFACT IS DECLARED AS A NINTH MERGE SOURCE, so that the block "
                    "it fills has recorded provenance."
                ),
                "spec_gap": (
                    "decisions/0114 E8 says `channel_classes` is filled ONCE in the merged "
                    "document, at Step 13b, SOURCED FROM STEP 8's ARTIFACT. decisions/0111 E6 "
                    "fixes the merge's input list at eight sources -- seven arm files and Step "
                    "14's limits section -- and says the list records SOURCES rather than only "
                    "arm files. It does not say whether Step 8's artifact is one of them."
                ),
                "what_was_done": (
                    "It is declared as a non-arm-file source with no arm, filling "
                    "`channel_classes` and `discovery_channel_overlap`, and both blocks name it "
                    "in `merged_from`. The reason is E6's own: a block that must not be netted "
                    "cannot arrive in the reader-facing document with no recorded provenance, "
                    "and that argument does not distinguish a bias ledger from a D9 bound. "
                    "Check S30's external anchor expects it, so a merge that drops it fails."
                ),
                "if_ruled_otherwise": (
                    "If the count of eight is meant to be exact, the Step 8 row comes out of "
                    "NON_ARM_MERGE_SOURCES in src/step8b_validate.py and out of NON_ARM_SOURCES "
                    "in the generator, and the two blocks lose their merged_from stamp -- at "
                    "which point the merged document carries Step 8's figures with no recorded "
                    "source, which is the state E6 was written to end."
                ),
            },
            {
                "choice": (
                    "The adopted-rule revision is READ from processed/step5/adopted_rule.json "
                    "by parsing its KEY NAMES, because that file has no revision field."
                ),
                "spec_gap": (
                    "decisions/0114 E14 makes the revision the fourth key dimension and the "
                    "launch instruction asks where it is READ rather than typed. The file the "
                    "dimension is about carries the revision only inside key names -- "
                    "`approved_rule_revision_6`, `approved_revision_6` -- and nowhere as a "
                    "value."
                ),
                "what_was_done": (
                    "Every key in that file is scanned for the approved-revision pattern, the "
                    "highest match is taken, and the KEY IT CAME FROM is recorded beside the "
                    "file's hash in $.adopted_rule_revision. No match is a HARD STOP, not a "
                    "default: a default would be a typed revision wearing a reader's clothes. "
                    "The file itself was NOT edited to add a field -- it is Step 5's output, "
                    "and a deliverable is corrected by rerunning the arm that produced it."
                ),
                "if_ruled_otherwise": (
                    "A first-class `adopted_rule_revision` field in that file would make the "
                    "read exact instead of inferred, and the reader would name the field rather "
                    "than a pattern. Reported to the Human Lead as a residual."
                ),
            },
            {
                "choice": (
                    "The arm key is (W_days, clock_origin, producing_step, "
                    "adopted_rule_revision), not W alone."
                ),
                "spec_gap": (
                    "Step 8b says the key is W alone -- an amendment aimed at the deleted "
                    "liveness threshold. Step 9 separately requires a second 91-day headline "
                    "anchored on the S2 premiere rather than the finale, and states that it is "
                    "not the same measurement at two window lengths. The W grid already "
                    "contains a finale-anchored 91-day arm, so a W-only key collides. AND THE "
                    "SAME COLLISION RECURS ONE DIMENSION OUT: Step 9 and Step 13 both measure "
                    "at W = 108, finale-anchored -- four payloads, two slots."
                ),
                "what_was_done": (
                    "The origin, THE PRODUCING STEP and THE ADOPTED-RULE REVISION are part of "
                    "the entry key, all required on every arm entry (decisions/0111 E2, 0114 "
                    "E14). Step 9's W = 108 and Step 13's W = 108 are different measurements of "
                    "one setting and BOTH EXIST as entries; so are two runs at one setting "
                    "under different rule revisions. Check S2 asserts uniqueness on the "
                    "FOUR-field key and asserts that $.arm_key declares it. No liveness "
                    "threshold enters the key, which is what the amendment fixed."
                ),
                "if_ruled_otherwise": (
                    "It must NOT be resolved by restricting which step may occupy a shared W: "
                    "that would make the schema decide an ownership question the spec does "
                    "not, and would drop a measurement rather than hold it. If the Netflix arm "
                    "is meant to live outside the arm list, it moves to a sibling array and "
                    "`clock_origin` becomes a plain field. The collision must be resolved "
                    "somewhere; it cannot be left to the writer."
                ),
            },
            {
                "choice": "Step 13's six non-headline outputs nest per producing arm, and the "
                          "nesting is UNCONDITIONAL -- no absence branch above it.",
                "spec_gap": (
                    "decisions/0111 E1 requires d3_prime, tested_ranges, "
                    "conclusions_surviving, conclusions_not_surviving, "
                    "d2_recomputed_inside_this_arm and action_type_counts to take per-arm "
                    "nesting, because each had ONE SLOT where TWO ARMS write and Step 13 is "
                    "dual. It does not say how a file that does not publish one of them says "
                    "so, and the obvious way -- an absence branch above the container -- is "
                    "forbidden by decisions/0109 §4, which records that the step_dual_status "
                    "rename fails LOUDLY only because no oneOf sits above by_producing_arm."
                ),
                "what_was_done": (
                    "The container is required wherever the block appears, and a block the "
                    "entry's producing step does not publish is OMITTED rather than wrapped. "
                    "$.block_ownership names every block's publisher, check S22 requires an "
                    "entry to carry its own step's blocks at the adopted setting, and check "
                    "S36 forbids it any other step's. Check S35 was widened from one "
                    "container to the family of six and its dead root-side scan was fixed, so "
                    "the constraint covers every member rather than the one that existed when "
                    "it was written."
                ),
                "if_ruled_otherwise": (
                    "If an explicit absence is wanted for a block another step publishes, it "
                    "goes INSIDE the container, in the arm payload slot, where an absence "
                    "branch already exists and sits BELOW the renamed key rather than above "
                    "it. What it may not do is sit above the container."
                ),
            },
            {
                "choice": "A block another step publishes is OMITTED from an entry, and both "
                          "directions are policed.",
                "spec_gap": (
                    "Nothing said what a file does about a block it does not publish, and "
                    "until v1.4.0 only one direction was checked at all: the file was checked "
                    "for writing too LITTLE and never for writing too MUCH."
                ),
                "what_was_done": (
                    "Omission, with $.block_ownership naming the publisher, and a new check "
                    "S36 that fails an entry carrying a block its own producing step does not "
                    "publish -- the direction that let a single-arm step's placeholder ship "
                    "carrying Step 13's action-type counts while declaring five other blocks "
                    "absent on the reasoning that a copy would be a second place that figure "
                    "lives (decisions/0111 §3, Q1). The ownership row for that block was "
                    "itself wrong and is corrected: its publisher is Step 13, which is what "
                    "decisions/0111 E1 makes it."
                ),
                "if_ruled_otherwise": (
                    "If a slot is wanted for every block in every entry, the four "
                    "non-nested blocks can carry an absence again and S36 narrows to filled "
                    "blocks only. The two nested ones cannot: an absence branch above a "
                    "by_producing_arm container is what decisions/0109 §4 forbids."
                ),
            },
            {
                "choice": "The publisher table the checks read is held in the VALIDATOR, not "
                          "in the file under test.",
                "spec_gap": (
                    "decisions/0111 E4: check S22 read `ownership_map` out of the instance it "
                    "was checking, so any arm file could exempt itself from S22 by editing one "
                    "string in its own table -- and `d3_prime` and `retained_by_air_period` "
                    "had no other backstop. The spec does not say where such a table lives."
                ),
                "what_was_done": (
                    "The table moved into src/step8b_validate.py, carrying the reasoning check "
                    "S31 already recorded about duality: A TABLE READ FROM THE FILE UNDER TEST "
                    "COULD ONLY AGREE WITH ITSELF. The file's own table is still read -- and "
                    "is asserted AGAINST the external one, so a rewrite fails on the rewrite "
                    "instead of escaping through it. The same route now warrants a check's "
                    "N/A: a block missing because another step publishes it is out of scope by "
                    "the external table, not by the file's own account of itself."
                ),
                "if_ruled_otherwise": (
                    "If a publisher assignment changes, it changes in the validator and in "
                    "this generator, and the two are compared on every run. What must not "
                    "happen is the checked file being the only place it is written down."
                ),
            },
            {
                "choice": "The waterfall, the liveness exclusions and the per-air-period "
                          "retention are Step 9's entries at EVERY arm this file shows, "
                          "including the grid arm at W = 91.",
                "spec_gap": (
                    "Once an arm entry is one step's measurement (decisions/0111 E2), each "
                    "per-arm block has to sit in the entry of the step that publishes it -- and "
                    "nothing states who publishes the waterfall, the liveness exclusion count "
                    "and the retained-pair counts AT THE GRID ARMS. Step 13 runs the grid; the "
                    "publisher table assigns those three blocks to Step 9."
                ),
                "what_was_done": (
                    "The table was followed mechanically: those blocks appear in Step 9 "
                    "entries, so this file carries a Step 9 entry at W = 91 finale-anchored "
                    "alongside Step 13's. Nothing was invented to fill it -- the same blocks, "
                    "in the entry of the step the table names."
                ),
                "if_ruled_otherwise": (
                    "If the per-arm series across the W grid is Step 13's, the publisher table "
                    "changes in ONE place -- in this generator and in the validator, which "
                    "compare on every run -- and those blocks move into the Step 13 entries "
                    "that already exist at each grid arm. No figure moves and no slot is added."
                ),
            },
            {
                "choice": "The merge's input list records SOURCES, and the key was RENAMED to "
                          "`sources_merged`.",
                "spec_gap": (
                    "decisions/0111 E6: Step 14's `limitations` is a named NON-ARM-FILE source "
                    "with its own provenance entry -- an eighth source, with no arm. Step 14 "
                    "delivers a limits section rather than a schema file, so it was not one of "
                    "the seven and had no way to be recorded."
                ),
                "what_was_done": (
                    "`arm_files_merged` became `sources_merged`; each entry carries a "
                    "source_kind, an arm that is null for a non-arm-file source, and, for such "
                    "a source, the blocks it fills. Every limitations entry names it in "
                    "merged_from. The key was RENAMED rather than widened in place, so a merge "
                    "still emitting the old one fails loudly instead of silently supplying a "
                    "list that no longer means what it says."
                ),
                "if_ruled_otherwise": (
                    "If a second non-arm-file source appears -- another Human-Lead section, "
                    "say -- it is added to the same list with its own fills_blocks, and check "
                    "S30 requires its blocks to name it. Nothing else moves."
                ),
            },
            {
                "choice": "Check S30 reads the input list in BOTH directions.",
                "spec_gap": (
                    "decisions/0111 E3b: S30 checked payload -> input and never input -> "
                    "payload, so A MERGE DROPPING AN ENTIRE DECLARED INPUT VALIDATED CLEAN. "
                    "The shipped merged placeholder was occupied by exactly that: two of its "
                    "seven declared inputs were named by no payload at all."
                ),
                "what_was_done": (
                    "Every declared source must be named by at least one payload's "
                    "merged_from, and a non-arm-file source must be named by the blocks it "
                    "declares it fills. Step 10's block carried no merge provenance at all "
                    "because its arm is `sole` by construction, and Step 12's cut did not "
                    "exist in the document; both are now emitted. It is M1 inverted -- one "
                    "file supplying two arms was caught, one file supplying nothing was not, "
                    "and it needs no forgery, only an omission."
                ),
                "if_ruled_otherwise": (
                    "If a source may legitimately supply nothing, it stops being an input and "
                    "leaves the list. A declared input that supplies nothing is either a "
                    "dropped arm or a list that has drifted from the merge."
                ),
            },
            {
                "choice": "Step 9's payload is nested under a per-producing-arm key.",
                "spec_gap": (
                    "The spec says the schema must hold both arms' values where the arms "
                    "legitimately differ, and names one such figure -- the bound over sampling "
                    "width ratios. It does not say which other figures may diverge."
                ),
                "what_was_done": (
                    "Rather than guess which figures diverge, the whole Step 9 payload is "
                    "written per producing arm, so the diff is a comparison of two subtrees "
                    "and no figure has a single slot. Steps 10 to 13 are single-owner and sit "
                    "outside that nesting."
                ),
                "if_ruled_otherwise": (
                    "A narrower nesting would require naming in advance every figure allowed "
                    "to differ, which is the reconciliation the spec forbids."
                ),
            },
            {
                "choice": "Step 13's non-W arms are `variants`, and Steps 11 and 12's cuts "
                          "are `subpopulation_cuts`.",
                "spec_gap": (
                    "The spec says Steps 9 to 13 write into this schema directly with no "
                    "conversion layer, and that there is one entry per W arm. Step 13 also "
                    "varies the S1 completion threshold, the completion-date definition and "
                    "the action-type evidence, and Steps 11 and 12 recompute the headline on "
                    "subpopulations. None of those is a W arm."
                ),
                "what_was_done": (
                    "Two sibling arrays reuse the same population block, so those steps write "
                    "the same structure without a translation step."
                ),
                "if_ruled_otherwise": (
                    "Folding them into `arms` would put non-W variation into a key that is "
                    "keyed on W, and the entries could not be diffed against each other."
                ),
            },
            {
                "choice": "Population sizes are per-arm fields, not schema constants.",
                "spec_gap": (
                    "The spec states the two population sizes at the adopted arm. Each W arm "
                    "re-censors, so the arms do not share a denominator."
                ),
                "what_was_done": (
                    "The schema declares the population definitions and requires every arm to "
                    "write its own n_position_5 and n_post_liveness, and every endpoint to "
                    "name the population it is on. No study figure is hard-coded anywhere in "
                    "the schema or the placeholder, so neither can carry a stale one."
                ),
                "if_ruled_otherwise": (
                    "Pinning the sizes in the schema would make the schema a second place a "
                    "population figure lives, which is the defect the no-conversion-layer rule "
                    "exists to prevent."
                ),
            },
            {
                "choice": "The placeholder's booleans and enums are real; only measurements "
                          "and writer text are placeheld.",
                "spec_gap": (
                    "The spec requires values that cannot be mistaken for measurements, and "
                    "does not say what to do with structure -- which branch of a boolean a "
                    "placeholder should show."
                ),
                "what_was_done": (
                    "Structure is real so that every branch can be built against, including a "
                    "degenerate bound and a coinciding sub-interval. Every measurement slot is "
                    "a sentinel and every writer-text slot is prefixed, both marked in the "
                    "schema and enforced mechanically in both directions."
                ),
                "if_ruled_otherwise": (
                    "Sentinelling the booleans too would leave Step 16 unable to see the "
                    "degenerate and coincident shapes it has to render differently."
                ),
            },
            {
                "choice": "A block with no producer is written as an explicit block absence "
                          "naming the step that would have filled it.",
                "spec_gap": (
                    "The spec says each entry carries a waterfall, an abandonment "
                    "distribution and the rest. It does not say what an entry carries when no "
                    "step in the spec produces one of them: nothing builds a waterfall or an "
                    "abandonment distribution for the premiere-anchored 91-day arm, and Step "
                    "13's grid is finale-anchored at every arm."
                ),
                "what_was_done": (
                    "Those slots accept a block_absence carrying a status, a reason and an "
                    "owning step, and check S22 forbids one on the primary headline arm, "
                    "where a producer does exist. The DERIV per-arm liveness slot takes the "
                    "superseded_for_this_purpose status for the same reason."
                ),
                "if_ruled_otherwise": (
                    "If a step is assigned to produce those blocks at every arm, the absence "
                    "branch stops being reachable and S22 can be tightened to forbid it "
                    "everywhere. Requiring them today would require more than the spec asks "
                    "and force an inventing writer."
                ),
            },
            {
                "choice": "An abandonment block names its ROW SET as well as its population, "
                          "and the histograms are an array keyed by stratum.",
                "spec_gap": (
                    "The spec requires the abandonment distribution per arm and requires "
                    "every figure to state its population. It does not say that a population "
                    "is two row sets -- position 5 and post-liveness -- on which the same "
                    "quantities take different values, and it says not to pool p across shows "
                    "with very different L2 without saying where a stratified histogram goes."
                ),
                "what_was_done": (
                    "row_set, row_set_label and n_rows_in_row_set are required, and histograms "
                    "is an array whose entries carry a stratum descriptor. Checks S25 and S26 "
                    "assert distinct row sets per population and well-formed bins per stratum."
                ),
                "if_ruled_otherwise": (
                    "If only one row set is ever to be published, the array collapses to one "
                    "entry and nothing else changes; the label still has to be there, because "
                    "a figure that does not name its row set cannot be checked against another."
                ),
            },
            {
                "choice": "Dual structure is a declared status, and single-arm steps write one "
                          "payload under `sole`.",
                "spec_gap": (
                    "The spec names Steps 9 and 13 as dual and Steps 10 to 12 as single-owner, "
                    "and requires the schema to hold both arms' values where the arms "
                    "legitimately differ. It does not say what a single-arm step writes into a "
                    "per-arm container."
                ),
                "what_was_done": (
                    "by_producing_arm carries step_dual_status and producing_step, with "
                    "payloads under arms.a and arms.b when dual and arms.sole when not. A "
                    "not_a_dual_step absence status exists for the slots where the distinction "
                    "has to be recorded rather than inferred."
                ),
                "if_ruled_otherwise": (
                    "If a step's duality changes -- as Step 13's did at decisions/0103 -- only "
                    "its step_dual_status and its arms keys change, and the diff sees the "
                    "change."
                ),
            },
            {
                "choice": "The field that carried both facts was RENAMED, not redefined: "
                          "`dual_status` is now `step_dual_status`, beside a new "
                          "`arms_in_this_file`.",
                "spec_gap": (
                    "decisions/0107 §4 requires the split into two facts -- whether the STEP is "
                    "dual, and whether THIS FILE holds one arm or both -- and does not say "
                    "whether the existing key keeps its name with a narrower meaning."
                ),
                "what_was_done": (
                    "The key was renamed. Under additionalProperties: false a writer still "
                    "emitting `dual_status` fails loudly, rather than silently acquiring a new "
                    "meaning under an unchanged key -- which is the shape this study has spent "
                    "most of its entries on. The enum values are unchanged, so nothing about "
                    "which steps are dual moves."
                ),
                "if_ruled_otherwise": (
                    "Keeping the old name costs one rename here and removes the loud failure. "
                    "Nothing else depends on it: no consumer reads this file yet."
                ),
            },
            {
                "choice": "THREE placeholders are emitted: the merged document, a dual step's "
                          "arm file, and a single-arm step's own file.",
                "spec_gap": (
                    "Step 8b's deliverable list says 'placeholder file', singular, and predates "
                    "decisions/0107, which creates two document ROLES, and decisions/0109 §1, "
                    "which makes granularity one file per step per arm and so gives the "
                    "single-arm steps files of their own. The spec does not say which shape the "
                    "placeholder illustrates."
                ),
                "what_was_done": (
                    "artifacts/step8b-placeholder.json is the MERGED document, because Step 16 "
                    "renders from it and the placeholder exists so Step 16 can be built. "
                    "artifacts/step8b-placeholder-arm-file.json is a DUAL step's arm file "
                    "(Step 9, arm a). artifacts/step8b-placeholder-sole-file.json is a "
                    "SINGLE-ARM step's own file (Step 11, arm `sole`), which had been called "
                    "expressible and left unillustrated -- and an expressible shape nobody has "
                    "written is a shape the first writer fixes by example. All three validate "
                    "against this schema and all three are flagged as placeholders."
                ),
                "if_ruled_otherwise": (
                    "If only one is wanted, the merged one is the deliverable and the other two "
                    "become working files -- but then the two arm-file shapes are illustrated "
                    "nowhere, and the first writer of each fixes it by example."
                ),
            },
            {
                "choice": "A single-arm step's file keeps the `arms` spine, and its headline "
                          "slot records why it holds no payload.",
                "spec_gap": (
                    "decisions/0109 §1 gives Steps 10 to 12 files of their own. `arms` is the "
                    "spine of this schema and those steps do not produce W arms, so the ruling "
                    "requires a single-arm step's file to have a legal spine (M9) without "
                    "saying what it holds."
                ),
                "what_was_done": (
                    "The file carries ONE arm entry -- the arm its cuts are computed at, the "
                    "one its base_arm_id names -- with the headline payload slot holding an "
                    "explicit absence: the unconditional headline is Step 9's, and restating "
                    "it here would be a second definition of one figure. The five per-arm "
                    "blocks another step publishes are absences naming that step. NO absence "
                    "branch was added above by_producing_arm to achieve this: an absence branch "
                    "there would turn the loud `dual_status` rename failure into a silent "
                    "'matched 0 oneOf branches' (decisions/0109 §4), and check S35 now asserts "
                    "that the path from the root to that object carries no oneOf or anyOf."
                ),
                "if_ruled_otherwise": (
                    "If a single-arm step's file is meant to carry no `arms` at all, the "
                    "top-level requirement becomes conditional on the producing step and S2 "
                    "must declare its emptiness rather than report VACUOUS. That is a ruling, "
                    "not a schema preference."
                ),
            },
            {
                "choice": "The blocks only the merge may fill are declared in the ownership "
                          "registry, not listed in the validator.",
                "spec_gap": (
                    "task-sheet.md Step 13b names cross_arm_divergences and limitations as the "
                    "two blocks only it may fill. Nothing says how a file declares that."
                ),
                "what_was_done": (
                    "Each $.block_ownership entry carries merged_document_only, and check S29 "
                    "reads the registry rather than a list inside the checker. A third such "
                    "block is added by marking it, in one place."
                ),
                "if_ruled_otherwise": (
                    "A hard-coded list in the validator would work today and drift the moment a "
                    "block is added, with nothing to compare it against."
                ),
            },
            {
                "choice": "Every top-level block declares an owner, and D4 and D9 are marked "
                          "copied from Step 8 rather than computed where they are written.",
                "spec_gap": (
                    "The spec says Steps 9 to 13 write into this file directly. It does not "
                    "say which step owns which top-level block, so the first step to write the "
                    "file would inherit all of them -- including the D4 count it is ruled to "
                    "consume rather than compute, and the limitations list that belongs to the "
                    "Human Lead."
                ),
                "what_was_done": (
                    "$.block_ownership names an owner, a role, a write mode and whether a "
                    "non-owner may originate the contents, with forbidden_to_compute_here "
                    "where a step may publish but not compute. Check S27 asserts coverage."
                ),
                "if_ruled_otherwise": (
                    "A different assignment changes the registry and nothing else. What must "
                    "not happen is no assignment, which is what being first to write silently "
                    "resolved."
                ),
            },
            {
                "choice": "A merged payload names the arm FILE it came from, and the diff is a "
                          "record rather than a flag.",
                "spec_gap": (
                    "task-sheet.md Step 13b says the merged document carries both arms' "
                    "payloads and that the Human Lead diffs the arm files before the merge. It "
                    "does not say how the merged file EVIDENCES that two arms were merged. "
                    "Nothing did: a merged document assembled from ONE arm file, with the one "
                    "payload deep-copied into the other arm's slot and relabelled, validated "
                    "clean and published that the arms agreed everywhere."
                ),
                "what_was_done": (
                    "Isolation is unobservable, but ARITY is observable. Each input file is a "
                    "named object carrying its step and its arm; each payload names one of "
                    "them in `merged_from`; and check S30 asserts that a block holding two "
                    "arms names two DIFFERENT files, that the two arms' sampling-width "
                    "convention labels differ -- they are named inputs the spec forbids "
                    "reconciling, so one label on both arms is a reconciliation on its face -- "
                    "and that each arm's intervals reference its OWN bootstrap settings. "
                    "`diff_precedes_merge: true` is RETIRED: it was a sentence the schema "
                    "required the file to contain rather than a fact the file records. What "
                    "replaces it is checkable -- which pairs were diffed, naming two files "
                    "each; how many figures were compared, which may not be zero; and how many "
                    "divergences were found, which must equal the entry count."
                ),
                "if_ruled_otherwise": (
                    "None of this can establish that the two files were WRITTEN in isolation, "
                    "and nothing in a file can. It raises the cost of a false merge from a "
                    "copy-and-relabel to A FABRICATED INPUT FILE PLUS ONE REWRITTEN SENTENCE "
                    "-- `convention_definition`, which S30 does not normalise (decisions/0111 "
                    "§4) -- and past that rung there is no in-file signal at all. THE HUMAN "
                    "LEAD'S DIFF REMAINS THE CONTROL."
                ),
            },
            {
                "choice": "Granularity is ONE FILE PER STEP PER ARM, and a single-arm step's "
                          "file is illustrated rather than described.",
                "spec_gap": (
                    "decisions/0107 carried two readings of its own -- §1, one file per arm, "
                    "and §6, one file per step per arm -- and this schema's two placeholders "
                    "took OPPOSITE sides of it: the merged document listed seven inputs while "
                    "the arm file named two extra writers."
                ),
                "what_was_done": (
                    "decisions/0109 §1 rules §6. An arm file's also_written_by_steps is empty "
                    "and check S28 asserts that every payload in it names the file's own "
                    "producing step; blocks another step publishes are explicit absences "
                    "naming that step. A THIRD placeholder is emitted, for a single-arm step's "
                    "own file, because a legal spine asserted in prose and never emitted "
                    "cannot be checked."
                ),
                "if_ruled_otherwise": (
                    "Under §1 the arm file would carry Step 9's and Step 13's blocks together "
                    "and the merge would take three inputs. The schema expresses either; what "
                    "it may not do is hold both readings at once, which is what it did."
                ),
            },
            {
                "choice": "Duality is pinned per step, in the schema and in a registry, rather "
                          "than declared by each block.",
                "spec_gap": (
                    "CLAUDE.md fixes which steps are dual and decisions/0103 §3 rules Step 13 "
                    "dual. The schema let every block declare its own step_dual_status beside "
                    "a producing_step it was never read against."
                ),
                "what_was_done": (
                    "$.step_duality carries the map with each status fixed by const, "
                    "by_producing_arm pins the status per producing_step, and check S31 "
                    "asserts both. A Step 9 block can no longer relabel itself single_arm -- "
                    "which would have disarmed the dropped-arm clause in the merged document, "
                    "since that clause is guarded on `dual`."
                ),
                "if_ruled_otherwise": (
                    "If a step's duality changes, it changes in one place here and the const "
                    "changes with it. What must not happen is a block choosing."
                ),
            },
            {
                "choice": "A CI slot accepts an explicit absence, and every CI names a quantity "
                          "class whose binding cluster is declared.",
                "spec_gap": (
                    "The bootstrap is fixed in all four elements -- 10,000 resamples, account "
                    "level for the outcome shares, seed 20260818, statistic BOTH. The record "
                    "also states that the binding cluster is NOT the same for every quantity, "
                    "and the spec does not say which quantities must carry an interval at all: "
                    "Step 12 lists candidate cuts and Step 13's per-arm series are shares."
                ),
                "what_was_done": (
                    "resampling_unit is an enum rather than the constant `account`; every CI "
                    "restates B, the seed, the unit and the statistic at the point of use and "
                    "names a quantity class resolved against $.binding_clusters; and a CI slot "
                    "may hold an absence with the not_required_by_spec status. Checks S23 and "
                    "S24 assert the restatement matches the registry and that a unit differing "
                    "from its binding cluster carries an unreconciled disagreement record."
                ),
                "if_ruled_otherwise": (
                    "If the spec ever names a quantity that MUST carry an interval, the "
                    "absence branch narrows from 'not asked for' to a list, and S18's site set "
                    "stops being 'whatever the file wrote'. THE PREVIOUS TEXT HERE WAS RETIRED "
                    "AT v1.6.0: it read 'if levels-vs-movements is fixed later, "
                    "fields_not_fixed_in_spec shrinks and the per-arm statistic stops varying', "
                    "and its antecedent OCCURRED -- decisions/0118 fixed it, the list is empty "
                    "and there is no per-arm statistic left to vary. A conditional whose "
                    "condition has happened reads as an open question and is not one."
                ),
            },
            {
                "choice": (
                    "THE STATISTIC IS A VALUE IN THE REGISTRY, PLURAL THERE AND SINGULAR AT "
                    "EACH INTERVAL, and the schema requires both objects rather than recording "
                    "which one an arm chose."
                ),
                "spec_gap": (
                    "decisions/0118 fixes the statistic as BOTH levels and paired movements "
                    "and says a run emitting only one is incomplete. It does not say how a "
                    "document records that, and the two obvious encodings differ: a per-entry "
                    "pair, or a per-interval label with a document-level completeness rule."
                ),
                "what_was_done": (
                    "Both. $.bootstrap_spec.statistics and every $.bootstrap_settings entry's "
                    "`statistics` hold the pair -- a set constraint, two unique members from "
                    "the enum, order not asserted because neither object is the design. Each "
                    "interval's `statistic` stays single-valued, because a level and a movement "
                    "are never compared to each other and an interval that did not say which "
                    "it was would mislead by an order of magnitude. Check S40 asserts the "
                    "registry side and the partition of `fields_considered`; check S41 asserts "
                    "both objects actually appear, per (producing step, arm), with its "
                    "coverage count. "
                    "The entry field was RENAMED from `statistic` to `statistics` so that a "
                    "writer still emitting the singular key fails against "
                    "additionalProperties: false rather than being accepted silently."
                ),
                "if_ruled_otherwise": (
                    "If a run were ever permitted to emit one object -- for a quantity with no "
                    "meaningful paired counterpart, say -- S41 gains an absence branch naming "
                    "the quantity and its reason, and `statistics` loses its minItems of 2 in "
                    "favour of minItems 1 plus a stated reason. Nothing else moves: the "
                    "per-interval label is required either way."
                ),
            },
            {
                "choice": "The per-air-period retained counts sit at the ARM, not inside the "
                          "waterfall block.",
                "spec_gap": (
                    "The retained-pair counts per air period are required at every arm, and "
                    "they used to sit inside the waterfall block because Step 8 publishes them "
                    "with its waterfall. Once a waterfall may legitimately be absent at an arm "
                    "with no producer, a mandate required at every arm had nowhere to go at "
                    "exactly those arms."
                ),
                "what_was_done": (
                    "They moved to $.arms[].retained_by_air_period, per population, with the "
                    "filter position they are measured after named beside them. It is one "
                    "figure in one place, not a copy: the waterfall block no longer holds it."
                ),
                "if_ruled_otherwise": (
                    "If they are meant to be a property of the waterfall, they move back and "
                    "the waterfall stops being absent-able -- but then some step has to be "
                    "assigned to produce a waterfall at every arm."
                ),
            },
            {
                "choice": "A declared emptiness is a distinct check status, and D9's three "
                          "bounded quantities are required by name.",
                "spec_gap": (
                    "CLAUDE.md requires a control that finds nothing to say whether it found "
                    "nothing or looked at nothing. The spec does not say how a file declares "
                    "that a list is empty."
                ),
                "what_was_done": (
                    "cross_arm_divergences carries a search record with a coverage count and "
                    "an empty_reason, and the validator reports EMPTY_DECLARED rather than "
                    "VACUOUS for that case only. D9's complementary_pairs, half_a and half_b "
                    "are required properties, so its check cannot examine an empty map."
                ),
                "if_ruled_otherwise": (
                    "If a fourth D9 quantity acquires both key forms it is added by name. The "
                    "alternative -- an open map -- is what let an empty one look like a pass."
                ),
            },
            {
                # reviewer-engineering, v1.6.0 review: assessed and AGREED. This
                # WAS a spec choice and it was unrecorded, which is exactly what
                # this block exists to stop. Half of it has since been ruled on
                # and that half is recorded as a ruling, not as a choice.
                "choice": (
                    "decisions/0118'S BOTH-OBJECTS REQUIREMENT IS APPLIED TO EVERY WRITING "
                    "STEP, INCLUDING THE SINGLE-ARM STEPS 10, 11 AND 12 -- and Step 12 is then "
                    "EXEMPTED FROM CARRYING INTERVALS AT ALL by a Human Lead ruling."
                ),
                "spec_gap": (
                    "decisions/0118 is recorded in the two data-scientist files, which own "
                    "Steps 6, 7, 9 and 13. Steps 10, 11 and 12 are single-arm and their writers "
                    "never received the canonical block, so nothing in the spec says the "
                    "requirement reaches them. Extending it was an inference."
                ),
                "what_was_done": (
                    "The requirement is applied to every writing step. The GROUND is that "
                    "decisions/0118 calls a run emitting one object INCOMPLETE rather than "
                    "differently designed, and incompleteness is a property of a bootstrap "
                    "rather than of having a counterpart arm -- the same reasoning by which B, "
                    "the seed and the unit already reach the single-arm steps under "
                    "decisions/0103, which is recorded in the same two files. THE ONE EXEMPTION "
                    "IS STEP 12'S AND IT IS A RULING RATHER THAN THIS STEP'S CHOICE: the Human "
                    "Lead ruled on 2026-08-19 that Step 12 mandates intervals nowhere -- this "
                    "schema's own warrant at $defs.ci_or_absence -- so a Step 12 file carrying "
                    "no interval declares that emptiness instead of failing to fill it. AND THE "
                    "EXEMPTION IS FROM PRODUCING INTERVALS, NOT FROM PRODUCING THEM COMPLETELY: "
                    "a Step 12 file that HAS published intervals owes both objects like any "
                    "other file, because the ruling's ground is that requiring them would make "
                    "the step MANUFACTURE two figures, and a step that has already computed "
                    "them is manufacturing nothing. THE PREVIOUS VERSION OF THIS RECORD "
                    "CLAIMED THAT NEITHER CHECK BRANCHED ON THE WRITING STEP -- retired at "
                    "v1.8.0, quoted verbatim in this entry's retirement field, and it did not "
                    "hold when it was written either: the step-level exemption in this same "
                    "paragraph is exactly such a branch. AND A SECOND RULING LANDS HERE, "
                    "2026-08-20: STEP 10 IS NOT EXEMPT. It measures outcome shares on the primary arm under the fixed "
                    "bootstrap, so it publishes real intervals and owes both objects; it also "
                    "joined the outcome-shares publisher table, which it had been missing from. "
                    "The exemption still has exactly one member."
                ),
                "if_ruled_otherwise": (
                    "The counterfactual this field used to offer was retired at v1.8.0 and is "
                    "quoted verbatim in this entry's retirement field: it named a remedy that "
                    "was already half-implemented, since S41 branches on the producing step for the Step 12 "
                    "exemption, and a counterfactual that describes the current build is not a "
                    "counterfactual -- the disposition `if_ruled_otherwise` took at v1.6.0 for "
                    "the same reason. What remains true and is not a counterfactual: widening "
                    "the Step 12 exemption to another step is a ruling, not an implementation "
                    "choice, and on 2026-08-20 exactly that question was put for Step 10 and "
                    "answered NO by the Human Lead."
                ),
                # THE TWO RETIRED SENTENCES, QUOTED UNDER A KEY THAT MARKS THEM
                # (v1.9.0, reviewer-engineering F7). Neither is registered in
                # src/check_surfaces.py's WITHDRAWN_PHRASES -- that register is
                # the Human Lead's file and this arm does not edit it -- so both
                # are REPORTED for registration, and this is the shape that lets
                # them be registered without failing the three placeholders that
                # legitimately quote them.
                "withdrawn_sentences": [
                    "checks S40 and S41 do not branch on which step wrote the file",
                    "S40 and S41 gain a producing-step guard",
                ],
            },
        ],
        "known_limits_of_this_schema": [
            {
                "limit": (
                    "A DECLARATION IS NOT A COMPUTATION: THIS SCHEMA CANNOT ESTABLISH THAT A "
                    "RUN ACTUALLY BOOTSTRAPPED BOTH OBJECTS. It requires the pair in every "
                    "registry entry, requires each interval to label itself, and requires both "
                    "labels to appear per (producing step, arm) (S40, S41). A writer that "
                    "computed "
                    "levels only, wrote the pair into its registry and attached the "
                    "`movements` label to a levels interval satisfies every one of those and "
                    "validates clean. THE SCHEMA SEES WHAT A FILE SAYS ABOUT ITSELF."
                ),
                "consequence": (
                    "The requirement in decisions/0118 -- both arms produce both objects -- is "
                    "enforced here as a SHAPE, not as a fact. It is stated as a gap rather "
                    "than papered over with a const: a const asserting agreement with the "
                    "writers' canonical block would be the shape this schema already retired "
                    "once, `diff_precedes_merge`, which was not a fact the file recorded but a "
                    "sentence the schema required the file to contain."
                ),
                "mitigation": (
                    "The half that CAN be established is: src/step8b_selftest.py reads the "
                    "canonical block from both writer files, asserts the two copies are "
                    "byte-identical, asserts the block names both objects, and asserts this "
                    "schema's bootstrap_statistic enum is exactly the set the block names -- so "
                    "the schema's vocabulary is checked against the spec rather than typed "
                    "beside it. What remains open is the writer's arithmetic, which only the "
                    "Human Lead's diff of the two arms' intervals can reach."
                ),
            },
            {
                "limit": (
                    "S41 ASKS WHETHER BOTH OBJECTS APPEAR, NOT WHETHER THE RIGHT QUANTITIES "
                    "HAVE BOTH. One movement interval anywhere in a (producing step, arm) "
                    "satisfies it, even if every substantive quantity of that owner is "
                    "levels-only. The schema has no notion of which quantities must carry a "
                    "paired counterpart, because the spec names none."
                ),
                "consequence": (
                    "A file can be complete in the sense S41 checks and incomplete in the "
                    "sense a reader cares about."
                ),
                "mitigation": (
                    "Each interval names its quantity and its quantity class. If the "
                    "spec later names the quantities that must carry both, S41 gains that list "
                    "and stops being a per-arm existence test. NOTHING HERE MAKES THE PAIRING "
                    "MACHINE-CHECKABLE, and the limit below says why the readable half is "
                    "weaker than this bullet used to claim."
                ),
            },
            {
                # reviewer-engineering, v1.6.0 review: assessed and AGREED. The
                # bullet above used to close with "a movement states in `quantity`
                # which two configurations it is a movement between, so the
                # pairing is READABLE even though it is not machine-checked" --
                # which is a control asserted to exist. `quantity` is free writer
                # text and the schema's own note says "Which two configurations is
                # the writer's to state", so a movement naming neither endpoint
                # validates and reads as a movement of nothing in particular.
                "limit": (
                    "A `paired_movement_<arm>` ENTRY IS NOT ESTABLISHED TO BE A MOVEMENT OF "
                    "ANYTHING IN PARTICULAR. The schema requires the object to exist, to be "
                    "labelled `movements`, and to reference its own arm's settings. It does NOT "
                    "require it to name the two configurations it is a difference between: "
                    "`quantity` is free writer text, and this schema's own note on that field "
                    "says which two configurations is the writer's to state. So a movement "
                    "interval that names neither endpoint validates."
                ),
                "consequence": (
                    "S41's per-owner existence test can be satisfied by a movement whose "
                    "endpoints are unstated, and no reader can reconstruct what moved. This is "
                    "the SECOND-ORDER form of the limit above: that one says the right "
                    "QUANTITIES need not carry both objects; this one says the movement that "
                    "does appear need not say what it is a movement OF."
                ),
                "mitigation": (
                    "NONE IN THIS SCHEMA, stated rather than papered over. Requiring two named "
                    "configurations would need a vocabulary of configurations the spec does not "
                    "define, and inventing one here would make every writer name a pair this "
                    "schema chose -- the fabrication decisions/0118's own scope forbids. It is "
                    "published so a consumer treats an endpoint-less movement as unreadable "
                    "rather than as a measurement."
                ),
            },
            {
                "limit": (
                    "THE MERGE'S EXPECTED SOURCE LIST IS DERIVED FROM THE DUALITY TABLE, WHICH "
                    "IS ITSELF A COPY OF THE SPEC. Check S30's external anchor knows that seven "
                    "arm files and two non-arm sources are expected because STEP_DUALITY and "
                    "NON_ARM_MERGE_SOURCES in src/step8b_validate.py say so. If the spec adds a "
                    "writing step and those tables are not updated, the anchor will expect the "
                    "old set."
                ),
                "consequence": (
                    "The anchor catches a merge that declares fewer sources than the tables "
                    "know about. It cannot catch a source the tables have never heard of, and "
                    "an extra ARM FILE fails rather than being accepted."
                ),
                "mitigation": (
                    "The duality table is asserted against each file's own $.step_duality by "
                    "check S31, so a file written under a newer spec disagrees loudly with a "
                    "validator running an older one, rather than passing quietly."
                ),
            },
            {
                "limit": (
                    "THE ADOPTED-RULE REVISION IS READ BY PARSING KEY NAMES. "
                    "processed/step5/adopted_rule.json carries no first-class revision field, "
                    "so the reader scans its keys for the approved-revision pattern and takes "
                    "the highest."
                ),
                "consequence": (
                    "A revision recorded ONLY in prose in that file, or one written under a key "
                    "name that does not match the pattern, would not be seen. The reader hard "
                    "stops when it finds no match at all, so the failure mode is a stop rather "
                    "than a silent default -- but a NEWER revision recorded in an unmatched "
                    "shape would leave the older one looking current."
                ),
                "mitigation": (
                    "$.adopted_rule_revision records the exact key the value came from and the "
                    "file's hash, so the reading can be checked rather than trusted. A "
                    "first-class field in that file would remove the inference; it is reported "
                    "to the Human Lead rather than added here, because that file is Step 5's "
                    "output."
                ),
            },
            {
                "limit": (
                    "JSON Schema cannot express cross-field constraints, so floor <= ceiling, "
                    "the derived-figure identities, the waterfall arithmetic, referential "
                    "integrity of the two ref families and the sentinel discipline are checked "
                    "by src/step8b_validate.py, not by the schema."
                ),
                "consequence": (
                    "A file that validates structurally is not thereby correct. Run the "
                    "validator, not a generic JSON Schema tool."
                ),
                "mitigation": (
                    "The validator reports the number of sites each check examined. A check "
                    "that examined none and cannot say why reports VACUOUS and fails; one "
                    "whose set the file declares empty, with a coverage count, reports "
                    "EMPTY_DECLARED and does not."
                ),
            },
            {
                "limit": (
                    "The bundled validator implements a subset of JSON Schema draft 2020-12 "
                    "rather than the whole language, and the schema is restricted to that "
                    "subset. No third-party validator was available to cross-check it."
                ),
                "consequence": (
                    "A keyword outside the subset added to this schema later would be silently "
                    "ignored by the bundled validator."
                ),
                "mitigation": (
                    "The subset is listed in the validator's docstring. Adding a keyword means "
                    "implementing it there in the same change."
                ),
            },
            {
                "limit": (
                    "The ARITHMETIC halves of two checks -- the derived-figure identities "
                    "(S12) and the waterfall chaining and arithmetic (S13) -- cannot run "
                    "against a placeholder, because every operand is a sentinel. S12's other "
                    "half, which compares each derived_fields entry's machine_checked flag "
                    "against the set the code actually evaluates, DOES run here."
                ),
                "consequence": (
                    "They report N/A on the placeholder, with the number of sites they would "
                    "have examined and, for S12, what the half that ran found -- rather than "
                    "reporting a pass they did not earn."
                ),
                "mitigation": (
                    "src/step8b_selftest.py exercises them against a de-sentinelled copy and "
                    "against mutations of it, including one that breaks only the chaining "
                    "clause, so each clause is shown to have force somewhere."
                ),
            },
            {
                "limit": (
                    "The schema cannot tell whether a block absence is honest. It can require "
                    "a status, a reason and an owning step, and it can forbid an absence on "
                    "the primary headline arm, but a writer that declares a producer missing "
                    "when one exists produces a file that validates."
                ),
                "consequence": (
                    "The absence branches added for the arms with no producer are also a way "
                    "to leave a block empty. Read $.block_ownership beside any absence."
                ),
                "mitigation": (
                    "Check S22 constrains where absences may appear and ties the ceilings "
                    "block to the bounds block, so the two cannot disagree about whether a "
                    "payload published a bound."
                ),
            },
            {
                "limit": (
                    "The schema fixes the shape of a figure, never its value. It cannot tell "
                    "whether a number written into it was measured on the population the field "
                    "names."
                ),
                "consequence": (
                    "The population labels are load-bearing and are the writer's "
                    "responsibility; the validator checks only that an endpoint's stated "
                    "population matches the block it sits in."
                ),
            },
            {
                "limit": (
                    "This step is single-arm. There is no second instance and therefore no "
                    "dual diff on the schema itself."
                ),
                "consequence": (
                    "An ambiguity in the Step 8b spec that this schema resolved one way would "
                    "not show up as a divergence. The resolutions are listed under "
                    "$.spec_choices_made_by_step_8b instead."
                ),
            },
            {
                "limit": (
                    "No single file can exercise every branch, because the document ROLE and "
                    "the PRODUCING STEP are properties of the whole file and, under one file "
                    "per step per arm, they decide which blocks are in it at all. Check S21's "
                    "branch coverage is therefore restricted per file: an arm file cannot "
                    "exhibit the merged document's branches and does not pretend to."
                ),
                "consequence": (
                    "Branch coverage is a property of the SET of placeholders -- the merged "
                    "document, a dual step's arm file and a single-arm step's own file -- not "
                    "of any one of them. S21 names the families it restricted and why, so a "
                    "restricted pass cannot be read as a full one."
                ),
                "mitigation": (
                    "All three placeholders are generated by the same run and validated in it, "
                    "and the run record in logs/step8b/ carries the role, the arm and the "
                    "producing step of each file beside its result."
                ),
            },
            {
                "limit": (
                    "The schema can require an arm file to name its arm and can forbid it the "
                    "blocks only the merge may fill. It cannot tell whether the file was "
                    "actually written in isolation."
                ),
                "consequence": (
                    "Isolation is a property of how an instance was run, not of its output. "
                    "The schema removes the one path that made a fabricated cross-arm search "
                    "the only way to pass; it does not make fabrication impossible."
                ),
                "mitigation": (
                    "The diff between the two arm files is the control, and it is the Human "
                    "Lead's. Nothing in this file substitutes for it."
                ),
            },
            {
                "limit": (
                    "THE MERGE-ARITY RESIDUAL, MEASURED -- AND NARROWER THAN v1.3.0 PUBLISHED. "
                    "Check S30 rejects a merged document whose second arm is a copy of the "
                    "first when the copy keeps the first arm's merge provenance, bootstrap "
                    "references or sampling-width convention label -- three independent legs, "
                    "each of which a copy-and-relabel trips. It does NOT reject a copy in "
                    "which all of those are relabelled as well, because at that point the file "
                    "asserts that a second input file exists and nothing inside the file can "
                    "contradict it. THE PUBLISHED LIMIT STOPPED THERE, AND THE ACTUAL LIMIT IS "
                    "ONE RUNG LOWER (decisions/0111 §4): S30 normalises "
                    + _ARM_LABELS_ARITY_WORD.upper() + " keys ("
                    + ", ".join(_ARM_LABELS_NORMALISED) + ") and NOT "
                    "`convention_definition` -- one arm's sampling-width convention in that "
                    "arm's own words -- and a forger making the copy internally coherent "
                    "rewrites that sentence anyway. THE MOMENT THEY DO, the identical-payload "
                    "signal inverts to 0 of N, WHICH IS WHAT A GENUINE MERGE PRODUCES."
                ),
                "consequence": (
                    "The remaining signal is that the two payloads are identical once those "
                    + _ARM_LABELS_ARITY_WORD + " keys are normalised. S30 counts and reports "
                    "that rather than failing "
                    "it, because two arms may legitimately agree on every figure -- and in a "
                    "placeholder every measurement is a sentinel, so identity is expected. "
                    "Past the rung above, the count separates nothing: SO S30 RAISES THE COST "
                    "OF A FALSE MERGE TO A FABRICATED INPUT FILE PLUS ONE REWRITTEN SENTENCE, "
                    "AND PAST THAT THERE IS NO IN-FILE SIGNAL AT ALL."
                ),
                "mitigation": (
                    "THE DIFF REMAINS THE CONTROL PAST THAT RUNG. It is the Human Lead's, it "
                    "is between two files, and it happens before this document is built. "
                    "Nothing in this file substitutes for it, and the selftest asserts the "
                    "fully relabelled copy as a NON-failure so this limit cannot drift from "
                    "the behaviour."
                ),
            },
            {
                "limit": (
                    "A check whose sites all live in another step's blocks reports N/A in a "
                    "file that does not carry them. Until v1.4.0 it said so by QUOTING THE "
                    "FILE'S OWN ABSENCE RECORDS, and could not tell an honest absence from a "
                    "declared one. Since v1.4.0 the second route is the usual one: the block "
                    "is not in the file at all, and the warrant is the EXTERNAL publisher "
                    "table this build's validator holds, not a sentence the file wrote about "
                    "itself."
                ),
                "consequence": (
                    "The external route cannot be talked out of: a file that omits a block its "
                    "own step publishes fails check S22 rather than being exempted. The "
                    "quoting route survives for the arms with no producer in the spec, and "
                    "there a writer that declares a block absent when it should have written "
                    "it still produces a file whose checks report N/A. An emptiness with NO "
                    "warrant behind it is not exempted and still fails as VACUOUS."
                ),
                "mitigation": (
                    "Check S22 requires each arm entry to carry the blocks ITS OWN producing "
                    "step publishes at the adopted setting, and check S36 forbids it any "
                    "block another step publishes -- so neither direction is left to the "
                    "file's own account of itself."
                ),
            },
            {
                "limit": (
                    "One absence status in the enum, `awaiting_owner_step`, is exercised by no "
                    "placeholder. The shape that used it is gone: it labelled another step's "
                    "per-arm block sitting in this file as an absence naming its publisher, "
                    "and under decisions/0111 E2 an arm entry is ONE STEP'S measurement, so "
                    "another step's block is omitted rather than described."
                ),
                "consequence": (
                    "Step 16 is not built against that branch by any placeholder in this set. "
                    "The status stays in the enum because a writer may genuinely be waiting on "
                    "an owner step; every absence record renders identically, carrying a "
                    "status, a reason and an owning step."
                ),
                "mitigation": (
                    "Check S21 lists the absence statuses a file does not exercise and does "
                    "not require, so a restricted pass cannot be read as a full one."
                ),
            },
        ],
        "notes": {
            "no_conversion_layer": (
                "Steps 9 through 13 write into this file directly. There is no intermediate "
                "format and no translation step, because a conversion layer is a second "
                "definition of every figure it touches."
            ),
            "one_definition_per_figure": (
                "Where a figure would otherwise appear twice, this schema references it: the "
                "scope qualifier is defined once under $.scope_qualifiers and referenced from "
                "every bound, and bootstrap settings are defined once under "
                "$.bootstrap_settings and referenced from every interval."
            ),
            "reading_a_placeholder": (
                "Check $.placeholder before reading anything else. This file's flag is true."
            ),
            "bootstrap_is_fixed": (
                "ALL FOUR ELEMENTS ARE FIXED BY THE SPEC: the resample count, the seed, the "
                "resampling unit for the outcome shares (decisions/0103) and the statistic "
                "(decisions/0118). They are stated at $.bootstrap_spec, restated at every "
                "interval, and checked against each other. THE STATISTIC IS BOTH LEVELS AND "
                "PAIRED MOVEMENTS: a run produces both objects, the registry holds the pair, "
                "and each interval says which of the two it is. A level and a movement are "
                "never compared to each other."
            ),
            "which_steps_are_dual": (
                "Steps 9 and 13 are dual and nest their payloads per producing arm. Steps 10, "
                "11 and 12 are single-arm and write one payload under `sole`. Which of the two "
                "a block used is a field, not something a consumer has to infer from the keys."
            ),
            "an_arm_entry_is_one_steps_measurement": (
                "An arm entry is identified by (W_days, clock_origin, producing_step, "
                "adopted_rule_revision). Step 9's W = 108 and Step 13's W = 108 are different "
                "measurements of one setting and both appear, as separate entries; so are two "
                "runs at one setting under different rule revisions. The revision is READ from "
                "the adopted-rule file and $.adopted_rule_revision says which file and key. An "
                "entry carries the blocks its own producing step publishes and no others; "
                "$.block_ownership names each block's publisher, and a block missing from an "
                "entry is not a gap -- it is in the entry of the step that publishes it."
            ),
            "step_13s_non_headline_outputs_are_per_arm": (
                "d3_prime, tested_ranges, conclusions_surviving, conclusions_not_surviving, "
                "d2_recomputed_inside_this_arm and action_type_counts each nest under "
                "by_producing_arm, exactly as the headline does. Step 13 is dual, so one slot "
                "would have been one slot where two arms write -- and the merge would have had "
                "to drop an arm or reconcile them."
            ),
            "one_file_per_arm": (
                "Each arm writes its own document and no arm writes into a document another "
                "arm writes into (decisions/0107). A DUAL STEP IS DIFFED BETWEEN TWO ARM "
                "FILES, BY THE HUMAN LEAD, BEFORE THE MERGE. The merged reader-facing document "
                "is Step 13b's, owned by the Human Lead, and it is the only document that "
                "holds both arms and the only one carrying cross_arm_divergences and "
                "limitations. Read $.document_scope first: it says which kind of file this is."
            ),
            "where_the_two_conventions_are_held": (
                "Where the two arms legitimately differ -- the bound over sampling width "
                "ratios use two conventions and are REPORTED, NOT RECONCILED -- the MERGED "
                "document holds both, under arms.a and arms.b. One slot per figure would force "
                "a reconciliation the spec forbids in the merged document; in a single arm's "
                "file it forces nothing, because there is no second arm's figure in it."
            ),
        },
    }
    return inst


def _d9_quantity() -> dict:
    return {
        "floor": {"value": SENT_C, "key": "strict", "direction": "cannot_over_count"},
        "ceiling": {
            "value": SENT_C,
            "key": "loose",
            "direction": "merges_genuinely_different_shows",
        },
        "point_estimate": {
            "status": "not_published",
            "reason": (
                "This quantity publishes as a bound. Neither endpoint may be quoted as the "
                "result: strict is the floor because it cannot over-count and loose is the "
                "ceiling because it merges genuinely different shows."
            ),
            "source": "decisions/0090",
            "decided_by": "Human Lead",
        },
        "coverage": {
            "records_examined": SENT_C,
            "records_with_a_slug": SENT_C,
            "what_was_counted": ph(
                "a zero floor is not an absence of evidence; the coverage publishes beside it "
                "so the bound is distinguishable from a check that looked nowhere"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

def _sha12(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def _git_head() -> str:
    try:
        return subprocess.run(
            ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "unavailable"


def _read_adopted_rule_revision() -> dict:
    """READ the adopted contamination-rule revision; never type it.

    decisions/0114 E14 makes the revision the FOURTH identity dimension, and the
    launch instruction asks where it is read from. It is read here, from
    processed/step5/adopted_rule.json -- the first file a Step 8 implementation
    reaches for, and the file where this dimension was already occupied once.

    The file carries no first-class revision field: the revision appears only in
    KEY NAMES. So every key in the document is scanned for the approved-revision
    pattern, the highest is taken, and the KEY IT WAS READ FROM is recorded
    alongside the file's hash, so a reader can go and check. If no key matches,
    this RAISES: a default would be a typed value wearing a reader's clothes, and
    the whole point of the dimension is that it moves when the rule does.
    """
    import re
    with open(ADOPTED_RULE_PATH) as fh:
        doc = json.load(fh)
    found: list[tuple[int, str]] = []

    def walk(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                m = re.fullmatch(ADOPTED_RULE_REVISION_KEY_RE, k)
                if m:
                    found.append((int(m.group(1)), f"{path}.{k}".lstrip(".")))
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(doc)
    if not found:
        raise SystemExit(
            f"no approved-revision key found in {ADOPTED_RULE_PATH}; the adopted-rule "
            f"revision is READ, never typed (decisions/0114 E14), so this is a hard stop "
            f"rather than a default"
        )
    revision, key = max(found)
    return {
        "revision": revision,
        "source_file": os.path.relpath(ADOPTED_RULE_PATH, ROOT),
        "source_key": key,
        "source_sha256_12": _sha12(ADOPTED_RULE_PATH),
        "read_not_typed": True,
        "how_it_is_read": (
            "A WRITER CALLS src/step8b_schema.py's `_read_adopted_rule_revision()` RATHER THAN "
            "REIMPLEMENTING THIS: a second reader is a second definition of the rule's version, "
            "and two definitions of one figure is the defect this study has hit most often. "
            "Every key in the adopted-rule file is scanned for the pattern "
            f"{ADOPTED_RULE_REVISION_KEY_RE!r} and the highest match is taken; the key it came "
            "from is recorded above. The file carries no first-class revision field, which is "
            "a residual reported to the Human Lead rather than corrected here -- it is Step "
            "5's output, and a deliverable is corrected by rerunning the arm that produced it."
        ),
        "why_it_is_in_the_key": (
            "A setting under which the measurement was taken that was invisible in the key, "
            "like the clock origin and the producing step before it. If a Step 5 or Step 7 "
            "amendment lands between one step's run and another's, their entries at one "
            "setting are DIFFERENT MEASUREMENTS, and without this dimension check S2 calls "
            "the rerun a duplicate. The dimension has been occupied once already: this file "
            "carried revision-3 figures against the approved revision-6 rule."
        ),
        "source": "decisions/0114 E14; CLAUDE.md, propagation surface 8",
    }


def _read_grid() -> list[int]:
    """Read the W grid out of task-sheet.md rather than typing it here."""
    import re
    with open(os.path.join(ROOT, "task-sheet.md")) as fh:
        text = fh.read()
    m = re.search(
        r"THE `W` ARM GRID IS ([\d/ ]+) DAYS", text
    )
    if not m:
        raise SystemExit("could not read the W arm grid from task-sheet.md")
    return [int(x) for x in m.group(1).replace(" ", "").split("/") if x]


def main() -> int:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    grid = _read_grid()

    provenance = {
        "generator": "src/step8b_schema.py",
        "generator_sha256_12": _sha12(os.path.abspath(__file__)),
        "generated_at_utc": stamp,
        "build_tag": f"step8b/a/{stamp[:10]}",
        "git_head_short": _git_head(),
        "host_step": "Step 8b, output schema",
        "written_by": "Analytics Engineer, instance a",
        "inputs": [
            "task-sheet.md Step 8b (the W grid is read from Step 13 at run time)",
            "artifacts/step8b-output-schema.json",
        ],
    }

    schema_provenance = dict(provenance)
    schema_provenance["validator"] = "src/step8b_validate.py"
    schema_provenance["validator_sha256_12"] = _sha12(
        os.path.join(ROOT, "src", "step8b_validate.py")
    )
    schema_provenance["selftest"] = "src/step8b_selftest.py"
    schema_provenance["note"] = (
        "This schema is generated. Correct it in the generator and rewrite both artifacts "
        "together; do not hand-edit either file."
    )
    schema_provenance.pop("inputs", None)

    schema = build_schema(schema_provenance)
    os.makedirs(os.path.dirname(SCHEMA_PATH), exist_ok=True)
    with open(SCHEMA_PATH, "w") as fh:
        json.dump(schema, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    # THREE placeholders, one per document ROLE and per granularity (0107, 0109
    # §1). The merged one is the deliverable Step 16 builds against; the arm-file
    # one is the shape a dual step writes; the sole-file one is a single-arm
    # step's own file. Each exists so that no writer has to invent its shape.
    merged_instance = build_placeholder(provenance, grid, "merged_document", None, "step13b")
    _stamp_merged_from(merged_instance)
    emitted = [
        (PLACEHOLDER_PATH, merged_instance, "merged_document", None),
        (ARM_PLACEHOLDER_PATH,
         build_placeholder(provenance, grid, "arm_file", "a", "step9"), "arm_file", "a"),
        (SOLE_PLACEHOLDER_PATH,
         build_placeholder(provenance, grid, "arm_file", "sole", "step11"), "arm_file", "sole"),
    ]
    for path, inst, _role, _arm in emitted:
        with open(path, "w") as fh:
            json.dump(inst, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    sys.path.insert(0, os.path.join(ROOT, "src"))
    import step8b_validate as V

    reports = []
    for path, _inst, file_role, file_arm in emitted:
        rep = V.validate_file(path, SCHEMA_PATH)
        rep["document_role"] = file_role
        rep["document_arm"] = file_arm
        rep["instance_sha256_12"] = _sha12(path)
        reports.append(rep)

    report = dict(reports[0])
    report["schema_sha256_12"] = _sha12(SCHEMA_PATH)
    report["placeholder_sha256_12"] = _sha12(PLACEHOLDER_PATH)
    report["generated_at_utc"] = stamp
    report["w_grid_read_from_task_sheet"] = grid
    report["files_validated"] = [
        {
            "instance": r["instance"],
            "document_role": r["document_role"],
            "document_arm": r["document_arm"],
            "ok": r["ok"],
            "schema_errors": r["schema_validation"]["error_count"],
            "checks_failed": r["checks_failed"],
            "statuses": {c["id"]: c["status"] for c in r["semantic_checks"]},
        }
        for r in reports
    ]
    report["per_file_reports"] = reports
    report["ok"] = all(r["ok"] for r in reports)

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"validation-{stamp.replace(':', '')}.json")
    with open(log_path, "w") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")

    print(json.dumps(
        {
            "schema": SCHEMA_PATH,
            "placeholder_merged": PLACEHOLDER_PATH,
            "placeholder_arm_file": ARM_PLACEHOLDER_PATH,
            "placeholder_sole_file": SOLE_PLACEHOLDER_PATH,
            "log": log_path,
            "ok": report["ok"],
            "per_file": [
                {
                    "instance": r["instance"],
                    "role": r["document_role"],
                    "arm": r["document_arm"],
                    "ok": r["ok"],
                    "schema_errors": r["schema_validation"]["errors"][:6],
                    "measurement_slots_applied":
                        r["schema_validation"]["measurement_slots_applied"],
                    "checks_total": r["checks_total"],
                    "checks_passed": r["checks_passed"],
                    "checks_not_applicable": r["checks_not_applicable"],
                    "checks_failed": r["checks_failed"],
                    "failing": [c["id"] + " " + c["status"] for c in r["semantic_checks"]
                                if c["status"] in ("FAIL", "VACUOUS")],
                }
                for r in reports
            ],
        },
        indent=2,
    ))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
