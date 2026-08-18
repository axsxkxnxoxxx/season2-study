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

    # S2 -- arm identity is unique on the declared key.
    c = Check("S2", "arm identity unique on (W_days, clock_origin)")
    seen: dict[tuple, str] = {}
    for i, arm in enumerate(inst.get("arms", [])):
        c.sites += 1
        key = (arm.get("W_days"), arm.get("clock_origin"))
        if key in seen:
            c.failures.append(f"$.arms[{i}] repeats arm key {key} first seen at {seen[key]}")
        seen[key] = f"$.arms[{i}]"
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
    for qname, q in ((cc.get("d9") or {}).get("quantities") or {}).items():
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
    c = Check(
        "S17",
        "figures reported-not-reconciled hold both arms' values and are flagged; an empty "
        "list is accepted only with a search record and its coverage count",
    )
    cad = inst.get("cross_arm_divergences")
    if cad is None:
        c.failures.append(
            "$.cross_arm_divergences is absent: with no search record, an empty set of "
            "divergences cannot be told from a search nobody ran"
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
        "every confidence interval carries a bootstrap_ref AND states its B, seed and "
        "resampling unit at the point of use",
    )
    for path, node in _walk(inst):
        if isinstance(node, dict) and "lower" in node and "upper" in node and "level_pct" in node:
            c.sites += 1
            for field in ("bootstrap_ref", "B", "seed", "resampling_unit", "quantity_class"):
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
        required_branches = {
            "clock_origin": {"s2_finale", "s2_premiere"},
            "producing_arm": {"a", "b", "sole"},
            "population": {"APPLY", "DERIV"},
            "absence_status": {"structurally_absent", "not_published",
                               "no_producer_in_spec", "superseded_for_this_purpose",
                               "not_required_by_spec", "not_a_dual_step"},
            "dual_status": {"dual", "single_arm"},
            "row_set": {"position_5", "post_liveness"},
            "stratum_kind": {"all", "l2_stratum"},
            "resampling_unit": {"account"},
        }
        observed = {k: set() for k in required_branches}
        observed["clock_origin"] = {a.get("clock_origin") for a in inst.get("arms", [])}
        for base, pop, block in _iter_payloads(inst):
            observed["population"].add(pop)
            bpa = block.get("by_producing_arm") or {}
            observed["dual_status"].add(bpa.get("dual_status"))
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
        for name, need in required_branches.items():
            c.sites += 1
            missing = need - (observed[name] - {None})
            if missing:
                c.failures.append(f"branch family {name!r} never exercises {sorted(missing)}")
    checks.append(c)

    # S22 -- a block absence is disciplined, and the primary headline arm has none.
    #        The absence branches exist because three of the four per-arm blocks
    #        have no producer at a non-primary arm (reviewer-engineering F1).
    #        They must not become a way to leave the adopted arm empty.
    c = Check(
        "S22",
        "every block absence names an owning step and a reason; the primary headline arm "
        "carries no absent block; and ceilings are absent only where the bounds are",
    )
    for path, node in _walk(inst):
        if _is_block_absence(node):
            c.sites += 1
            if node.get("owning_step") is None:
                c.failures.append(f"{path}: block absence with no owning_step")
            if not isinstance(node.get("reason"), str) or len(node["reason"]) < 20:
                c.failures.append(f"{path}: block absence with no usable reason")
    for i, arm in enumerate(inst.get("arms", [])):
        if arm.get("is_primary_headline") is not True:
            continue
        for name in ("waterfall", "abandonment_distribution", "liveness_exclusions",
                     "d3_prime", "retained_by_air_period"):
            c.sites += 1
            node = arm.get(name)
            if _is_block_absence(node):
                c.failures.append(
                    f"$.arms[{i}].{name}: absent on the PRIMARY headline arm, where the spec "
                    f"does name a producer"
                )
            elif isinstance(node, dict):
                for pop, sub in node.items():
                    if _is_block_absence(sub) and name != "liveness_exclusions":
                        c.failures.append(
                            f"$.arms[{i}].{name}.{pop}: absent on the primary headline arm"
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
        "references",
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

    return checks


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
