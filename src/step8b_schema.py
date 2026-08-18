"""Step 8b -- build the JSON schema Step 16 reads from, and its placeholder.

Owner: Analytics Engineer. Mode: Chained. Zero API calls.

Writes:
    artifacts/step8b-output-schema.json   the schema
    artifacts/step8b-placeholder.json     an instance of it, flagged as a placeholder
    logs/step8b/validation-<stamp>.json   the validator run record

Both artifacts are generated. Nothing in either is typed by hand at any later
point: if a value is wrong, this file is where it is corrected and both files
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
LOG_DIR = os.path.join(ROOT, "logs", "step8b")

SCHEMA_VERSION = "1.1.0"
SCHEMA_ID = "urn:season2-study:step8b-output-schema:1.1.0"

SENT_C = -999
SENT_P = -999.0
PH = "PLACEHOLDER — NOT A MEASUREMENT"


def ph(text: str) -> str:
    return f"{PH}: {text}"


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
    "step16",
    "human_lead",
]

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
                "description": "How many candidates were examined. A zero here with performed "
                               "true is itself a finding: the search looked at nothing.",
            },
            "what_was_searched": _text("What was examined, in the writer's words."),
            "owner_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "empty_reason": {
                "type": ["string", "null"],
                "description": "Why the list is empty, required by check S17 when it is.",
                "x-writer-text": True,
            },
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
            "A confidence interval. THE BOOTSTRAP IS FIXED -- 10,000 resamples, account level "
            "for the outcome shares, seed 20260818 (decisions/0103) -- and EVERY INTERVAL "
            "RECORDS ITS SEED, RESAMPLE COUNT AND RESAMPLING UNIT AT THE POINT OF USE. They "
            "are written here as well as referenced, because the ruling says at the point of "
            "use and a reference is not that; check S23 asserts the inline values equal the "
            "referenced registry entry, so the redundancy is checked rather than trusted. "
            "Levels-vs-movements is NOT fixed by that ruling and stays visible per arm."
        ),
        "additionalProperties": False,
        "required": [
            "level_pct", "lower", "upper", "method", "bootstrap_ref",
            "B", "seed", "resampling_unit", "quantity_class",
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
            "Everything one producing arm computes for one population of one W arm. Step 9 is "
            "a dual step and is diffed IN this schema, so each arm writes its own subtree and "
            "no figure has a single slot that would force a reconciliation."
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
    d["by_producing_arm"] = {
        "type": "object",
        "description": (
            "The producing arms of this block. RESTRUCTURED at v1.1.0 against "
            "reviewer-engineering's F5. Previously both `a` and `b` were required everywhere, "
            "which pushed dual structure into single-arm steps and left them writing an "
            "absence record whose available statuses all said something false: "
            "`structurally_absent` already means 'this quantity does not exist here', and "
            "nothing meant 'this step is not dual'. Now `dual_status` says which kind of step "
            "wrote the block, and the payloads sit under `arms`: `a` and `b` when dual, a "
            "single `sole` when not. DUAL STEPS ARE 9 AND 13 (decisions/0103 §3); Steps 10, "
            "11 and 12 are single-arm."
        ),
        "additionalProperties": False,
        "required": ["dual_status", "producing_step", "arms"],
        "properties": {
            "dual_status": {
                "enum": ["dual", "single_arm"],
                "x-enum-id": "dual_status",
                "description": "Whether the step that wrote this block runs twice in isolation.",
            },
            "producing_step": {"enum": WRITER_STEPS, "x-enum-id": "writer_step"},
            "dual_status_source": {
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
        "if": {"properties": {"dual_status": {"const": "dual"}}, "required": ["dual_status"]},
        "then": {
            "properties": {
                "arms": {"required": ["a", "b"], "not": {"required": ["sole"]}},
            }
        },
        "else": {
            "properties": {
                "arms": {
                    "required": ["sole"],
                    "not": {"anyOf": [{"required": ["a"]}, {"required": ["b"]}]},
                },
            }
        },
    }

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
                     "population_label", "written_by_step"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
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

    d["arm_entry"] = {
        "type": "object",
        "description": (
            "One entry per W arm. The entry key is (W_days, clock_origin) -- see "
            "$.arm_key for why the origin is part of it. There is NO liveness threshold and "
            "no threshold may appear as a key."
        ),
        "additionalProperties": False,
        "required": ["arm_id", "W_days", "H_days", "clock_origin", "in_arm_grid",
                     "headline", "waterfall", "abandonment_distribution",
                     "liveness_exclusions", "d3_prime", "retained_by_air_period"],
        "properties": {
            "arm_id": {"type": "string", "pattern": r"^W\d+_"},
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
                "primary headline arm.",
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
            "d3_prime": _block_or_absence(
                {p: {
                    "oneOf": [
                        {"$ref": "#/$defs/d3_prime_block"},
                        {"$ref": "#/$defs/block_absence"},
                    ]
                } for p in POPULATIONS},
                "D3's cleared count and share at this arm, per population (F6). Step 13 runs "
                "D3' at every arm; an arm no step re-runs it at carries an absence.",
            ),
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
                "description": (
                    "Per-pair counts by action type, aggregated. `action` is record-level and "
                    "the row is a pair, so there is no row-level action value; Step 13's arm "
                    "reads these counts."
                ),
                "additionalProperties": {"$ref": "#/$defs/count"},
            },
            "note": _text("A note from the writer."),
        },
    }

    d["variant_entry"] = {
        "type": "object",
        "description": (
            "A Step 13 arm that varies something other than W. The entry key is W alone plus "
            "the clock origin, so a non-W variation cannot be an arm entry without colliding; "
            "it lives here and names the arm it is a variation of."
        ),
        "additionalProperties": False,
        "required": ["variant_id", "axis", "level", "base_arm_id", "headline"],
        "properties": {
            "variant_id": {"type": "string"},
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
            "d2_recomputed_inside_this_arm": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "finale_binds": {"$ref": "#/$defs/count"},
                    "s1_completion_binds": {"$ref": "#/$defs/count"},
                    "both_bind": {"$ref": "#/$defs/count"},
                    "note": _text("A note from the writer."),
                },
            },
            "d3_prime": _block_or_absence(
                {p: {
                    "oneOf": [
                        {"$ref": "#/$defs/d3_prime_block"},
                        {"$ref": "#/$defs/block_absence"},
                    ]
                } for p in POPULATIONS},
                "D3' inside this variation, where the variation re-censors (F6).",
            ),
            "conclusions_surviving": {
                "type": "array", "items": _text("One conclusion that survives this variation.")
            },
            "conclusions_not_surviving": {
                "type": "array", "items": _text("One conclusion that does not survive.")
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
        "required": ["cut_id", "dimension", "level", "base_arm_id", "headline",
                     "candidate_considered"],
        "properties": {
            "cut_id": {"type": "string"},
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
            "The single output schema. Steps 9 through 13 write into it DIRECTLY and Step 16 "
            "reads it. There is no conversion layer: a conversion layer is a second definition "
            "of every figure. Validate with src/step8b_validate.py, which implements the "
            "JSON Schema subset used here plus the cross-field checks the schema language "
            "cannot express."
        ),
        "type": "object",
        "additionalProperties": False,
        "required": [
            "schema_version", "schema_id", "placeholder", "generated_by", "sentinels",
            "arm_key", "arm_grid_days", "populations", "scope_qualifiers",
            "bootstrap_spec", "binding_clusters", "bootstrap_settings", "block_ownership",
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
                    "derived three times and deleted, and the adopted rule is parameter-free."
                ),
                "additionalProperties": False,
                "required": ["fields", "note", "no_liveness_threshold"],
                "properties": {
                    "fields": {"const": ["W_days", "clock_origin"]},
                    "note": {"type": "string"},
                    "no_liveness_threshold": {"const": True},
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
                    "WHAT THE SPEC FIXES, IN ONE PLACE. Human Lead ruling, 2026-08-18 "
                    "(decisions/0103 §1): 10,000 resamples, resampled at the ACCOUNT level for "
                    "the outcome shares, seed 20260818, identical for both arms. The seed's "
                    "VALUE is arbitrary and its FIXITY is the point -- without a fixed seed a "
                    "difference between the arms could be sampling noise rather than a "
                    "divergence, and the dual control rests on that distinction. "
                    "LEVELS-VS-MOVEMENTS IS NOT FIXED BY THAT RULING and is recorded here as "
                    "still unfixed, per arm in $.bootstrap_settings, so an unfixed spec stays "
                    "visible rather than silent."
                ),
                "additionalProperties": False,
                "required": ["B", "seed", "resampling_unit_for_outcome_shares",
                             "identical_for_both_arms", "fields_fixed_in_spec",
                             "fields_not_fixed_in_spec", "source"],
                "properties": {
                    "B": {"type": "integer", "minimum": 1},
                    "seed": {"type": "integer"},
                    "resampling_unit_for_outcome_shares": {
                        "enum": RESAMPLING_UNITS, "x-enum-id": "resampling_unit"
                    },
                    "identical_for_both_arms": {"const": True},
                    "seed_value_is_arbitrary_its_fixity_is_the_point": {"const": True},
                    "fields_fixed_in_spec": {"type": "array", "items": {"type": "string"}},
                    "fields_not_fixed_in_spec": {"type": "array", "items": {"type": "string"}},
                    "why_account_level": {"type": "string"},
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
                    "the resample count and the resampling unit AT THE POINT OF USE. B, the "
                    "seed and the unit are now fixed by the spec (decisions/0103); "
                    "levels-vs-movements is not, and differs between the arms, so it stays "
                    "visible here."
                ),
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["B", "seed", "statistic", "resampling_unit", "producing_arm",
                                 "spec_status", "fields_fixed_in_spec"],
                    "properties": {
                        "B": {"type": "integer", "minimum": 1},
                        "seed": {"type": "integer"},
                        "statistic": {"enum": ["levels", "movements"],
                                      "x-enum-id": "bootstrap_statistic"},
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
                            "enum": ["fixed_in_spec", "unfixed_at_time_of_writing",
                                     "partly_fixed_in_spec"],
                            "x-enum-id": "spec_status",
                        },
                        "fields_fixed_in_spec": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Which of this entry's fields the spec fixes. "
                                           "`spec_status` alone cannot say that B is fixed "
                                           "while the statistic is not.",
                        },
                        "note": _text("A note from the writer."),
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
                        "source": {"type": "string"},
                    },
                },
            },
            "channel_classes": {
                "type": "object",
                "description": (
                    "D4 and D9 publish ALONGSIDE the bounds and are never folded into them, so "
                    "they have their own slots (decisions/0062). BOTH ARE STEP 8's FIGURES: "
                    "Step 8 holds the episode-level evidence and Step 9 is forbidden to "
                    "recompute either, so the counts here are COPIED, and the schema says so "
                    "at the point of use (F9)."
                ),
                "additionalProperties": False,
                "required": ["d4", "d9"],
                "properties": {
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
            },
            "discovery_channel_overlap": {
                "type": "array",
                "description": (
                    "The overlap in every unit, each with the consumer that needs that unit. "
                    "Picking one unit leaves another consumer holding a wrong-unit figure."
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
                    },
                },
            },
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
                    "LOOKED FOR THEM. Restructured at v1.1.0 against reviewer-engineering's "
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
                "description": (
                    "The ranges actually tested. An interactive Step 16 binds its controls to "
                    "these so no reader can drive it somewhere that was never tested."
                ),
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
                    "required": ["id", "text", "source"],
                    "properties": {
                        "id": _text("The limitation's identifier."),
                        "text": _text("The limitation, in the words of the step that owns it."),
                        "source": _text("Where it is stated."),
                        "direction": {"type": ["string", "null"]},
                        "may_be_netted_with_others": {"const": False},
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
        disagreement: bool = False) -> dict:
    ci = {
        "level_pct": 95,
        "lower": SENT_P,
        "upper": SENT_P,
        "method": "percentile_bootstrap",
        "bootstrap_ref": ref,
        # At the point of use, per decisions/0103: the seed, the resample count
        # and the resampling unit are written HERE as well as referenced.
        "B": BOOTSTRAP_B,
        "seed": BOOTSTRAP_SEED,
        "resampling_unit": unit,
        "quantity_class": quantity_class,
        "note": ph(
            "the interval is a sentinel; the bootstrap settings, the unit and the quantity "
            "class are real, because the ruling requires them at the point of use"
        ),
    }
    if disagreement:
        ci["unit_disagreement"] = {
            "binding_cluster": "show",
            "unit_used": unit,
            "material": False,
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


def _population_block(pop: str, degenerate_ns: bool, coincides: bool,
                      dual: bool = True, step: str = "step9",
                      bounds_present: bool = True, ci_present: bool = True) -> dict:
    """One population of one arm.

    `dual` selects between the two-arm and the single-arm shape. Steps 9 and 13
    are dual (decisions/0103 §3); Steps 10, 11 and 12 are not, and were being
    made to name an `a` and a `b` they do not have (reviewer-engineering F5).
    """
    if dual:
        arms = {
            "a": _payload(pop, "a", degenerate_ns, coincides, step, bounds_present,
                          ci_present),
            "b": _payload(pop, "b", degenerate_ns, coincides, step, bounds_present,
                          ci_present),
        }
    else:
        arms = {
            "sole": _payload(pop, "sole", degenerate_ns, coincides, step, bounds_present,
                             ci_present),
        }
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
            "dual_status": "dual" if dual else "single_arm",
            "producing_step": step,
            "dual_status_source": (
                "CLAUDE.md, Dual implementation; Step 13's duality is decisions/0103 §3"
            ),
            "arms": arms,
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
        "written_by_step": "step8",
        "order_ref": "decisions/0029 positions 1-7",
        "positions": positions,
        "monotone_check": {"operator": ">=", "result": True, "positions_checked": SENT_C},
    }


def _air_periods(pop: str) -> dict:
    return {
        "population": pop,
        "written_by_step": "step13",
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
        "written_by_step": "step13",
    }


def _d3_prime(pop: str, w: int) -> dict:
    return {
        "population": pop,
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


def _arm(arm_id: str, w: int, origin: str, in_grid: bool, primary: bool,
         origin_note: str, blocks_have_producers: bool = True,
         deriv_liveness_superseded: bool = False) -> dict:
    arm: dict = {
        "arm_id": arm_id,
        "W_days": w,
        "H_days": 91,
        "clock_origin": origin,
        "clock_origin_note": ph(origin_note),
        "in_arm_grid": in_grid,
        "is_primary_headline": primary,
        "headline": {
            "APPLY": _population_block("APPLY", degenerate_ns=False, coincides=False),
            "DERIV": _population_block("DERIV", degenerate_ns=True, coincides=True),
        },
    }
    if not blocks_have_producers:
        # F1, the blocking finding. At a non-primary arm on a different clock
        # origin, nothing in the spec produces a waterfall, an abandonment
        # distribution, a per-arm liveness count or a D3' figure: Step 8 builds
        # the waterfall at the adopted finale-anchored arm, Step 10 charts the
        # headline arm, and Step 13's grid is finale-anchored throughout. Each
        # slot stays present and names the gap.
        why = (
            "No step in the spec produces this block for a premiere-anchored arm. Step 8 "
            "builds the waterfall at the adopted finale-anchored arm, Step 10 charts the "
            "headline arm, and Step 13's W grid is finale-anchored at every one of its eight "
            "arms. The slot is present and says so rather than requiring a figure that would "
            "have to be invented."
        )
        for name in ("waterfall", "abandonment_distribution", "liveness_exclusions",
                     "d3_prime", "retained_by_air_period"):
            arm[name] = _absent_block(
                "no_producer_in_spec", "none", why,
                "task-sheet.md Steps 8, 10 and 13; reviewer-engineering F1",
            )
        arm["action_type_counts"] = {}
        arm["note"] = ph("one entry per arm")
        return arm

    arm["waterfall"] = {p: _waterfall(p) for p in POPULATIONS}
    arm["abandonment_distribution"] = {
        # F2: one entry per row set, and the four cells the record requires are
        # APPLY and DERIV, each at position 5 and post-liveness.
        p: [_abandonment(p, "position_5"), _abandonment(p, "post_liveness")]
        for p in POPULATIONS
    }
    if deriv_liveness_superseded:
        arm["liveness_exclusions"] = {
            "APPLY": _liveness("APPLY"),
            "DERIV": _absent_block(
                "superseded_for_this_purpose", "step13",
                "The DERIV per-arm liveness series is recorded as SUPERSEDED FOR THIS "
                "PURPOSE: the per-arm series to report is the APPLY one, and the DERIV "
                "figures remain correct on DERIV while being the wrong series here. A schema "
                "that demands a number in this slot demands a superseded one.",
                "task-sheet.md Step 13; reviewer-engineering F1",
            ),
        }
    else:
        arm["liveness_exclusions"] = {p: _liveness(p) for p in POPULATIONS}
    arm["d3_prime"] = {p: _d3_prime(p, w) for p in POPULATIONS}
    arm["retained_by_air_period"] = {p: _air_periods(p) for p in POPULATIONS}
    arm.update({
        "action_type_counts": {
            "s1_watch": SENT_C, "s1_scrobble": SENT_C, "s1_checkin": SENT_C, "s1_other": SENT_C,
            "s2_watch": SENT_C, "s2_scrobble": SENT_C, "s2_checkin": SENT_C, "s2_other": SENT_C,
        },
        "note": ph("one entry per arm"),
    })
    return arm


def _block_ownership() -> dict:
    """Who owns each top-level block (reviewer-engineering F9).

    Six required top-level blocks named no owner, so the first step to write the
    file inherited them -- including `channel_classes`, whose D4 count Step 9 is
    explicitly forbidden to compute, and `limitations`, which belongs to the
    Human Lead at Step 14 and which no agent may draft. Being first to write a
    file is not a claim to a block.
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
        "sentinels": structural,
        "arm_key": structural,
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
        "block_ownership": structural,
        "channel_classes": (
            "step8", "Analytics Engineer, Step 8", "copied_from_step_8_output", False,
            "decisions/0070 rulings 1 and 7",
        ),
        "discovery_channel_overlap": (
            "step8", "Analytics Engineer, Step 8", "copied_from_step_8_output", False,
            "decisions/0077, 0079",
        ),
        "derived_fields": structural,
        "cross_arm_divergences": (
            "human_lead", "Human Lead, who diffs the arms", "written_by_owner_step", False,
            "CLAUDE.md, Dual implementation",
        ),
        "arms": (
            "step9", "Data Scientist, Steps 9 and 13", "written_by_owner_step", True,
            "task-sheet.md Steps 9 and 13",
        ),
        "variants": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13",
        ),
        "subpopulation_cuts": (
            "step11", "Data Scientist, Steps 11 and 12", "written_by_owner_step", False,
            "task-sheet.md Steps 11 and 12",
        ),
        "tested_ranges": (
            "step13", "Data Scientist, Step 13", "written_by_owner_step", False,
            "task-sheet.md Step 13, 'Record the tested ranges. Step 16 needs them.'",
        ),
        "limitations": (
            "human_lead", "Human Lead, Step 14", "human_lead_only", False,
            "task-sheet.md Step 14; CLAUDE.md, Human Lead",
        ),
        "spec_choices_made_by_step_8b": structural,
        "known_limits_of_this_schema": structural,
        "notes": structural,
    }
    forbidden = {
        "channel_classes": ["step9"],
        "discovery_channel_overlap": ["step9"],
        "limitations": ["step9", "step10", "step11", "step12", "step13"],
        "cross_arm_divergences": ["step9", "step13"],
    }
    out = {}
    for name, (step, role, mode, may_fill, source) in rows.items():
        entry = {
            "owner_step": step,
            "owner_role": role,
            "write_mode": mode,
            "may_first_writer_fill": may_fill,
            "source": source,
        }
        if name in forbidden:
            entry["forbidden_to_compute_here"] = forbidden[name]
        out[name] = entry
    return out


def build_placeholder(provenance: dict, grid: list[int]) -> dict:
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
            "generated_for": "Step 16, so the visualization can be built before results exist",
        },
        "generated_by": provenance,
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
        "arm_key": {
            "fields": ["W_days", "clock_origin"],
            "note": (
                "W alone does not identify an arm. Step 9 reports a second 91-day headline "
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
            "identical_for_both_arms": True,
            "seed_value_is_arbitrary_its_fixity_is_the_point": True,
            "fields_fixed_in_spec": ["B", "seed", "resampling_unit"],
            "fields_not_fixed_in_spec": ["statistic (levels vs movements)"],
            "why_account_level": (
                "Pairs are not independent -- one account contributes many -- so pair-level "
                "resampling understates the interval. The clustering has been measured on "
                "this build and the measurement is cited rather than restated here, because a "
                "figure copied into a schema is a second place that figure lives."
            ),
            "source": "decisions/0103 §1; task-sheet.md Step 9",
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
        "bootstrap_settings": {
            "a_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistic": "movements",
                "resampling_unit": "account",
                "producing_arm": "a",
                "spec_status": "partly_fixed_in_spec",
                "fields_fixed_in_spec": ["B", "seed", "resampling_unit"],
                "note": ph(
                    "B, the seed and the unit are fixed by decisions/0103 and are real here; "
                    "levels-vs-movements is NOT fixed by it and still differs between the "
                    "arms, so it stays visible rather than silent"
                ),
            },
            "b_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistic": "levels",
                "resampling_unit": "account",
                "producing_arm": "b",
                "spec_status": "partly_fixed_in_spec",
                "fields_fixed_in_spec": ["B", "seed", "resampling_unit"],
                "note": ph("as above, for the other arm; the statistic differs and that is "
                           "the unfixed part of the spec showing through"),
            },
            "sole_default": {
                "B": BOOTSTRAP_B,
                "seed": BOOTSTRAP_SEED,
                "statistic": "levels",
                "resampling_unit": "account",
                "producing_arm": "sole",
                "spec_status": "partly_fixed_in_spec",
                "fields_fixed_in_spec": ["B", "seed", "resampling_unit"],
                "note": ph("the single-arm steps, 10 to 12, which have no second arm to "
                           "diff against"),
            },
        },
        "block_ownership": _block_ownership(),
        "channel_classes": {
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
        ],
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
        "cross_arm_divergences": {
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
        },
        "arms": [
            _arm(
                "W108_s2_finale", 108, "s2_finale", True, True,
                "the adopted arm; T0 is the later of the S2 finale and the first-pass S1 "
                "completion date",
            ),
            _arm(
                "W091_s2_finale", 91, "s2_finale", True, False,
                "a grid arm at 91 days, finale-anchored, distinct from the premiere-anchored "
                "arm below",
                deriv_liveness_superseded=True,
            ),
            _arm(
                "W091_s2_premiere", 91, "s2_premiere", False, False,
                "Step 9's second headline at Netflix's own 91-day reporting window, anchored "
                "on the later of the S2 premiere and the first-pass S1 completion date; it "
                "sits on a different origin from the primary headline and the two are NOT the "
                "same measurement at two window lengths",
                blocks_have_producers=False,
            ),
        ],
        "variants": [
            {
                "variant_id": "s1_completion_threshold_90",
                "axis": "s1_completion_threshold",
                "level": "90_percent",
                "base_arm_id": "W108_s2_finale",
                # Step 13 is DUAL (decisions/0103 §3), so its payload nests per
                # producing arm exactly as Step 9's does. Its per-arm sensitivity
                # shares carry no bound and no interval, and the slots say so
                # rather than demanding figures the spec never asks it for.
                "headline": {
                    "APPLY": _population_block("APPLY", False, False, dual=True,
                                               step="step13", bounds_present=False,
                                               ci_present=False),
                    "DERIV": _population_block("DERIV", True, True, dual=True,
                                               step="step13", bounds_present=False,
                                               ci_present=False),
                },
                "d3_prime": {p: _d3_prime(p, 108) for p in POPULATIONS},
                "d2_recomputed_inside_this_arm": {
                    "finale_binds": SENT_C,
                    "s1_completion_binds": SENT_C,
                    "both_bind": SENT_C,
                    "note": ph(
                        "the max() split is three categories, not two: a tie is its own "
                        "category, not a tiebreak, and the count is not population-invariant"
                    ),
                },
                "conclusions_surviving": [ph("one string per conclusion that survives")],
                "conclusions_not_surviving": [ph("one string per conclusion that does not")],
            }
        ],
        "subpopulation_cuts": [
            {
                "cut_id": "discovery_channel_a",
                "dimension": "discovery_channel",
                "level": "channel_a",
                "base_arm_id": "W108_s2_finale",
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
                "dimension": "discovery_channel",
                "level": "both",
                "base_arm_id": "W108_s2_finale",
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
        ],
        "tested_ranges": {
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
        "limitations": [
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
        ],
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
                "choice": "The arm key is (W_days, clock_origin), not W alone.",
                "spec_gap": (
                    "Step 8b says the key is W alone -- an amendment aimed at the deleted "
                    "liveness threshold. Step 9 separately requires a second 91-day headline "
                    "anchored on the S2 premiere rather than the finale, and states that it is "
                    "not the same measurement at two window lengths. The W grid already "
                    "contains a finale-anchored 91-day arm, so a W-only key collides."
                ),
                "what_was_done": (
                    "The origin is part of the entry key and is a required enum on every arm. "
                    "No liveness threshold enters the key, which is what the amendment fixed."
                ),
                "if_ruled_otherwise": (
                    "If the Netflix arm is meant to live outside the arm list, it moves to a "
                    "sibling array and `clock_origin` becomes a plain field. The collision "
                    "must be resolved somewhere; it cannot be left to the writer."
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
                    "by_producing_arm carries dual_status and producing_step, with payloads "
                    "under arms.a and arms.b when dual and arms.sole when not. A "
                    "not_a_dual_step absence status exists for the slots where the distinction "
                    "has to be recorded rather than inferred."
                ),
                "if_ruled_otherwise": (
                    "If a step's duality changes -- as Step 13's did at decisions/0103 -- only "
                    "its dual_status and its arms keys change, and the diff sees the change."
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
                "choice": "A CI slot accepts an explicit absence, and every CI names a quantity "
                          "class whose binding cluster is declared.",
                "spec_gap": (
                    "The bootstrap is now fixed at 10,000 resamples, account level, seed "
                    "20260818. The record also states that the binding cluster is NOT the same "
                    "for every quantity, and the spec does not say which quantities must carry "
                    "an interval at all: Step 12 lists candidate cuts and Step 13's per-arm "
                    "series are shares."
                ),
                "what_was_done": (
                    "resampling_unit is an enum rather than the constant `account`; every CI "
                    "restates B, the seed and the unit at the point of use and names a "
                    "quantity class resolved against $.binding_clusters; and a CI slot may "
                    "hold an absence with the not_required_by_spec status. Checks S23 and S24 "
                    "assert the restatement matches the registry and that a unit differing "
                    "from its binding cluster carries an unreconciled disagreement record."
                ),
                "if_ruled_otherwise": (
                    "If levels-vs-movements is fixed later, bootstrap_spec's "
                    "fields_not_fixed_in_spec shrinks and the per-arm statistic stops varying. "
                    "It is recorded as unfixed because the ruling that fixed the other three "
                    "did not fix it."
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
        ],
        "known_limits_of_this_schema": [
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
                "The resample count, the resampling unit for the outcome shares and the seed "
                "are fixed by the spec and are stated at $.bootstrap_spec, restated at every "
                "interval, and checked against each other. The statistic -- levels versus "
                "movements -- is NOT fixed, and differs between the arms."
            ),
            "which_steps_are_dual": (
                "Steps 9 and 13 are dual and nest their payloads per producing arm. Steps 10, "
                "11 and 12 are single-arm and write one payload under `sole`. Which of the two "
                "a block used is a field, not something a consumer has to infer from the keys."
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

    placeholder = build_placeholder(provenance, grid)
    with open(PLACEHOLDER_PATH, "w") as fh:
        json.dump(placeholder, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    sys.path.insert(0, os.path.join(ROOT, "src"))
    import step8b_validate as V

    report = V.validate_file(PLACEHOLDER_PATH, SCHEMA_PATH)
    report["schema_sha256_12"] = _sha12(SCHEMA_PATH)
    report["placeholder_sha256_12"] = _sha12(PLACEHOLDER_PATH)
    report["generated_at_utc"] = stamp
    report["w_grid_read_from_task_sheet"] = grid

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"validation-{stamp.replace(':', '')}.json")
    with open(log_path, "w") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")

    print(json.dumps(
        {
            "schema": SCHEMA_PATH,
            "placeholder": PLACEHOLDER_PATH,
            "log": log_path,
            "ok": report["ok"],
            "schema_validation_passed": report["schema_validation"]["passed"],
            "schema_errors": report["schema_validation"]["errors"][:10],
            "measurement_slots_applied": report["schema_validation"]["measurement_slots_applied"],
            "checks_total": report["checks_total"],
            "checks_passed": report["checks_passed"],
            "checks_not_applicable": report["checks_not_applicable"],
            "checks_failed": report["checks_failed"],
            "failing": [c["id"] + " " + c["status"] for c in report["semantic_checks"]
                        if c["status"] in ("FAIL", "VACUOUS")],
        },
        indent=2,
    ))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
