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

SCHEMA_VERSION = "1.0.0"
SCHEMA_ID = "urn:season2-study:step8b-output-schema:1.0.0"

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
ABSENCE_STATUSES = ["structurally_absent", "not_published", "not_yet_written", "unruled"]


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
            "A confidence interval, with the bootstrap settings that produced it named by "
            "reference. The spec fixes none of B, the seed or levels-vs-movements, so the "
            "unfixed spec is visible in the output rather than silent (task-sheet.md Step 8b)."
        ),
        "additionalProperties": False,
        "required": ["level_pct", "lower", "upper", "method", "bootstrap_ref"],
        "properties": {
            "level_pct": {"type": "number"},
            "lower": {"$ref": "#/$defs/percent"},
            "upper": {"$ref": "#/$defs/percent"},
            "method": {"type": "string"},
            "bootstrap_ref": {
                "type": "string",
                "description": "A key of $.bootstrap_settings. Referential integrity is check S3.",
            },
            "note": _text("A note from the writer."),
        },
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
            "ci": {"$ref": "#/$defs/ci"},
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
        "required": ["producing_arm", "shares", "bounds", "ceilings_cannot_all_hold",
                     "written_by"],
        "properties": {
            "producing_arm": {"enum": ["a", "b"], "x-enum-id": "producing_arm"},
            "written_by": {"type": "string"},
            "shares": {
                "type": "object",
                "additionalProperties": False,
                "required": OUTCOMES,
                "properties": {o: {"$ref": "#/$defs/share"} for o in OUTCOMES},
            },
            "bounds": {
                "type": "object",
                "additionalProperties": False,
                "required": OUTCOMES,
                "properties": {
                    "never_started": {"$ref": "#/$defs/bound_no_subinterval"},
                    "started_and_left": {"$ref": "#/$defs/bound_with_subinterval"},
                    "continued": {"$ref": "#/$defs/continued_bound"},
                },
            },
            "ceilings_cannot_all_hold": {"$ref": "#/$defs/ceilings_block"},
            "bound_over_sampling_width_ratios": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "never_started": {"$ref": "#/$defs/ratio_block"},
                    "started_and_left": {"$ref": "#/$defs/ratio_block"},
                    "started_and_left_sub_interval": {"$ref": "#/$defs/ratio_block"},
                },
            },
            "spec_choices_this_arm_made": {
                "type": "array",
                "description": "Choices the spec does not fix, named by the arm that made them.",
                "items": _text("One choice the spec does not fix."),
            },
        },
    }

    d["by_producing_arm"] = {
        "type": "object",
        "description": (
            "Both arms of the dual step, side by side. Both keys are required: an arm that has "
            "not run writes an explicit absence record, so 'not yet run' and 'agrees with the "
            "other arm' cannot look alike."
        ),
        "additionalProperties": False,
        "required": ["a", "b"],
        "properties": {
            "a": {"oneOf": [{"$ref": "#/$defs/step9_payload"}, {"$ref": "#/$defs/absence"}]},
            "b": {"oneOf": [{"$ref": "#/$defs/step9_payload"}, {"$ref": "#/$defs/absence"}]},
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
        "required": ["population", "order_ref", "positions", "monotone_check"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
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
            "retained_by_air_period": {
                "type": "array",
                "description": (
                    "Retained pairs per air period after right-censoring. The aggregate hides "
                    "a cohort-asymmetric loss, so the per-period breakdown is required "
                    "(decisions/0033)."
                ),
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
        "required": ["population", "n_started_and_left", "p_definition", "bin_unit",
                     "histogram", "named_categories", "p_at_bound", "comparability_caveat"],
        "properties": {
            "population": {"enum": POPULATIONS, "x-enum-id": "population"},
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
            "histogram": {
                "type": "object",
                "additionalProperties": False,
                "required": ["bin_edges_p", "counts"],
                "properties": {
                    "bin_edges_p": {
                        "type": "array",
                        "description": "Ascending edges on [0, 1]; len(counts) + 1 of them. "
                                       "Bin definitions are structure, not measurements.",
                        "items": {"type": "number"},
                    },
                    "counts": {"type": "array", "items": {"$ref": "#/$defs/count"}},
                    "l2_stratum": {"type": ["string", "null"]},
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
                     "liveness_exclusions"],
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
            "waterfall": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "properties": {p: {"$ref": "#/$defs/waterfall_block"} for p in POPULATIONS},
            },
            "abandonment_distribution": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "properties": {p: {"$ref": "#/$defs/abandonment_block"} for p in POPULATIONS},
            },
            "liveness_exclusions": {
                "type": "object",
                "additionalProperties": False,
                "required": POPULATIONS,
                "properties": {p: {"$ref": "#/$defs/liveness_exclusions_block"}
                               for p in POPULATIONS},
            },
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
            "bootstrap_settings", "channel_classes", "arms",
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
            "bootstrap_settings": {
                "type": "object",
                "description": (
                    "A registry of bootstrap settings, keyed by id and referenced from every "
                    "CI. B, the seed and levels-vs-movements differ between the arms and the "
                    "spec fixes none of them, so the unfixed spec is visible here."
                ),
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["B", "seed", "statistic", "resampling_unit", "producing_arm",
                                 "spec_status"],
                    "properties": {
                        "B": {"$ref": "#/$defs/count"},
                        "seed": {"$ref": "#/$defs/integer_setting"},
                        "statistic": {"enum": ["levels", "movements"],
                                      "x-enum-id": "bootstrap_statistic"},
                        "resampling_unit": {"const": "account"},
                        "producing_arm": {"enum": ["a", "b"], "x-enum-id": "producing_arm"},
                        "spec_status": {
                            "enum": ["fixed_in_spec", "unfixed_at_time_of_writing"],
                            "x-enum-id": "spec_status",
                        },
                        "note": _text("A note from the writer."),
                    },
                },
            },
            "channel_classes": {
                "type": "object",
                "description": (
                    "D4 and D9 publish ALONGSIDE the bounds and are never folded into them, so "
                    "they have their own slots (decisions/0062)."
                ),
                "additionalProperties": False,
                "required": ["d4", "d9"],
                "properties": {
                    "d4": {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["definition", "published_alongside", "folded_into_bound",
                                     "counts"],
                        "properties": {
                            "definition": {"type": "string"},
                            "published_alongside": {"const": True},
                            "folded_into_bound": {"const": False},
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
                                     "universe", "quantities"],
                        "properties": {
                            "published_alongside": {"const": True},
                            "folded_into_bound": {"const": False},
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
                                    "nowhere."
                                ),
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
                    "required": ["field", "expression", "moves_with"],
                    "properties": {
                        "field": {"type": "string"},
                        "expression": {"type": "string"},
                        "moves_with": {"type": "array", "items": {"type": "string"}},
                        "source": {"type": "string"},
                    },
                },
            },
            "cross_arm_divergences": {
                "type": "array",
                "description": (
                    "Figures where the two arms legitimately differ. Both values are held; "
                    "`reconciled` is const false, so the schema cannot record a reconciliation "
                    "the spec forbids."
                ),
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
                "description": "Limitations that travel with the result, each with its source.",
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


def _ci(ref: str) -> dict:
    return {
        "level_pct": 95,
        "lower": SENT_P,
        "upper": SENT_P,
        "method": "percentile_bootstrap",
        "bootstrap_ref": ref,
        "note": ph("the interval is a sentinel; the settings reference is real"),
    }


def _share(pop: str, ref: str, horizon_note: str) -> dict:
    return {
        "value_percent": SENT_P,
        "numerator_pairs": SENT_C,
        "denominator_pairs": SENT_C,
        "on_population": pop,
        "on_population_n": SENT_C,
        "on_population_label": "post-liveness (position 7)",
        "ci": _ci(ref),
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


def _payload(pop: str, arm: str, degenerate_ns: bool, coincides: bool) -> dict:
    ref = f"{arm}_default"
    return {
        "producing_arm": arm,
        "written_by": "Step 9",
        "shares": {
            "never_started": _share(pop, ref, "never-started is read at tau1"),
            "started_and_left": _share(pop, ref, "started-and-left is assigned at tau2"),
            "continued": _share(
                pop, ref,
                "Continued is read at tau2; this observed share does not replace the ceiling "
                "in bounds.continued",
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


def _population_block(pop: str, degenerate_ns: bool, coincides: bool) -> dict:
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
            "a": _payload(pop, "a", degenerate_ns, coincides),
            "b": _payload(pop, "b", degenerate_ns, coincides),
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
        "order_ref": "decisions/0029 positions 1-7",
        "positions": positions,
        "monotone_check": {"operator": ">=", "result": True, "positions_checked": SENT_C},
        "retained_by_air_period": [
            {
                "air_period": ph("one row per air period"),
                "retained_pairs": SENT_C,
                "entering_pairs": SENT_C,
                "retained_share_percent": SENT_P,
            }
        ],
    }


def _abandonment(pop: str) -> dict:
    edges = [round(x / 10, 1) for x in range(11)]
    return {
        "population": pop,
        "n_started_and_left": SENT_C,
        "p_definition": "p = |{e in E2 : e <= max(A_H)}| / L2",
        "p_raw_ratio_form_withdrawn": True,
        "p_is_null_off_started_and_left": True,
        "bin_unit": "fraction_of_season",
        "histogram": {
            "bin_edges_p": edges,
            "counts": [SENT_C] * (len(edges) - 1),
            "l2_stratum": None,
        },
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


def _arm(arm_id: str, w: int, origin: str, in_grid: bool, primary: bool,
         origin_note: str) -> dict:
    return {
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
        "waterfall": {p: _waterfall(p) for p in POPULATIONS},
        "abandonment_distribution": {p: _abandonment(p) for p in POPULATIONS},
        "liveness_exclusions": {
            p: {
                "total_pairs": SENT_C,
                "never_started_component": SENT_C,
                "started_and_left_component": SENT_C,
                "accounts": SENT_C,
                "silence_test_alone": SENT_C,
                "spared_by_not_continued": SENT_C,
                "identity": "silence_test_alone - spared_by_not_continued = total_pairs",
                "pair_level_not_account_level": True,
            }
            for p in POPULATIONS
        },
        "action_type_counts": {
            "s1_watch": SENT_C, "s1_scrobble": SENT_C, "s1_checkin": SENT_C, "s1_other": SENT_C,
            "s2_watch": SENT_C, "s2_scrobble": SENT_C, "s2_checkin": SENT_C, "s2_other": SENT_C,
        },
        "note": ph("one entry per arm"),
    }


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
        "bootstrap_settings": {
            "a_default": {
                "B": SENT_C,
                "seed": SENT_C,
                "statistic": "movements",
                "resampling_unit": "account",
                "producing_arm": "a",
                "spec_status": "unfixed_at_time_of_writing",
                "note": ph(
                    "B, the seed and levels-vs-movements are recorded per arm because the spec "
                    "fixes none of them; an unfixed spec is visible here rather than silent"
                ),
            },
            "b_default": {
                "B": SENT_C,
                "seed": SENT_C,
                "statistic": "levels",
                "resampling_unit": "account",
                "producing_arm": "b",
                "spec_status": "unfixed_at_time_of_writing",
                "note": ph("as above, for the other arm"),
            },
        },
        "channel_classes": {
            "d4": {
                "definition": "S3 or later evidence without S2 evidence.",
                "published_alongside": True,
                "folded_into_bound": False,
                "counts": {"APPLY": SENT_C, "DERIV": SENT_C},
                "source": "decisions/0070 ruling 7",
            },
            "d9": {
                "published_alongside": True,
                "folded_into_bound": False,
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
        "derived_fields": [
            {
                "field": "$..bounds.*.width_pp",
                "expression": "ceiling.percent - floor.percent",
                "moves_with": ["floor", "ceiling"],
                "source": "CLAUDE.md, Derived figures",
            },
            {
                "field": "$..conditional_sub_interval.width_pp",
                "expression": "conditional_sub_interval.ceiling.percent "
                              "- conditional_sub_interval.floor.percent",
                "moves_with": ["started_and_left bound floor"],
                "source": "CLAUDE.md, Derived figures, item 2",
            },
            {
                "field": "$..ceilings_cannot_all_hold.sum_percent",
                "expression": "never_started.ceiling.percent + started_and_left.ceiling.percent "
                              "+ continued.ceiling.percent",
                "moves_with": ["any ceiling"],
                "source": "CLAUDE.md, Derived figures, Any ceiling",
            },
            {
                "field": "$..ceilings_cannot_all_hold.excess_pp",
                "expression": "sum_percent - 100",
                "moves_with": ["sum_percent"],
                "source": "CLAUDE.md, Derived figures, Any ceiling",
            },
            {
                "field": "$..ceilings_cannot_all_hold.excess_pairs",
                "expression": "2 * never_started_exclusions + started_and_left_exclusions",
                "moves_with": ["the exclusion split"],
                "source": "decisions/0053 §4",
            },
            {
                "field": "$..bound_over_sampling_width_ratios.*.value",
                "expression": "bound width / that arm's sampling width",
                "moves_with": ["the corresponding bound width"],
                "source": "CLAUDE.md, Derived figures, items 4 and 5",
            },
            {
                "field": "$..shares.*.value_percent",
                "expression": "100 * numerator_pairs / denominator_pairs",
                "moves_with": ["the retained row count"],
                "source": "Step 9",
            },
        ],
        "cross_arm_divergences": [
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
            ),
            _arm(
                "W091_s2_premiere", 91, "s2_premiere", False, False,
                "Step 9's second headline at Netflix's own 91-day reporting window, anchored "
                "on the later of the S2 premiere and the first-pass S1 completion date; it "
                "sits on a different origin from the primary headline and the two are NOT the "
                "same measurement at two window lengths",
            ),
        ],
        "variants": [
            {
                "variant_id": "s1_completion_threshold_90",
                "axis": "s1_completion_threshold",
                "level": "90_percent",
                "base_arm_id": "W108_s2_finale",
                "headline": {
                    "APPLY": _population_block("APPLY", False, False),
                    "DERIV": _population_block("DERIV", True, True),
                },
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
                "headline": {
                    "APPLY": _population_block("APPLY", False, False),
                    "DERIV": _population_block("DERIV", True, True),
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
                    "APPLY": _population_block("APPLY", False, False),
                    "DERIV": _population_block("DERIV", True, True),
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
                    "The validator reports the number of sites each check examined, and a "
                    "check that examined none reports VACUOUS rather than passing."
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
                    "Two checks -- the derived-figure identities and the waterfall arithmetic "
                    "-- cannot run against a placeholder, because every operand is a sentinel."
                ),
                "consequence": (
                    "They report N/A on the placeholder, with the number of sites they would "
                    "have examined, rather than reporting a pass they did not earn."
                ),
                "mitigation": (
                    "src/step8b_selftest.py exercises them against a de-sentinelled copy and "
                    "against a mutation of it, so they are shown to have force somewhere."
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
