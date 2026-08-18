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

Every check reports the number of sites it examined. A check that finds nothing
because it looked nowhere reports VACUOUS and counts as a failure, per
CLAUDE.md: "an empty result and a clean result are the same value, and only the
control knows which it produced."

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
    def __init__(self, cid: str, title: str):
        self.cid = cid
        self.title = title
        self.sites = 0
        self.failures: list[str] = []
        self.skipped_reason: str | None = None

    @property
    def status(self) -> str:
        if self.skipped_reason is not None:
            return "N/A"
        if self.sites == 0:
            return "VACUOUS"
        return "FAIL" if self.failures else "PASS"

    def as_dict(self) -> dict:
        return {
            "id": self.cid,
            "title": self.title,
            "status": self.status,
            "sites_examined": self.sites,
            "failures": self.failures[:20],
            "failure_count": len(self.failures),
            "not_applicable_reason": self.skipped_reason,
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
        for arm_key, payload in (block.get("by_producing_arm") or {}).items():
            bounds = (payload or {}).get("bounds")
            if not isinstance(bounds, dict):
                continue
            ns = bounds.get("never_started", {}).get("conditional_sub_interval")
            sl = bounds.get("started_and_left", {}).get("conditional_sub_interval")
            if isinstance(ns, dict):
                c.sites += 1
                if ns.get("applicable") is not False:
                    c.failures.append(f"{base}.by_producing_arm.{arm_key}: never-started sub-interval is not marked inapplicable")
                if not isinstance(ns.get("reason"), str) or len(ns.get("reason", "")) < 20:
                    c.failures.append(f"{base}.by_producing_arm.{arm_key}: never-started sub-interval carries no reason")
            if isinstance(sl, dict):
                c.sites += 1
                if sl.get("applicable") is not True:
                    c.failures.append(f"{base}.by_producing_arm.{arm_key}: started-and-left sub-interval is not marked applicable")
                if "coincides_with_bound" not in sl:
                    c.failures.append(f"{base}.by_producing_arm.{arm_key}: started-and-left sub-interval does not record coincidence")
    checks.append(c)

    # S8 -- Continued is never emitted as a point: it carries a ceiling and its
    #       floor slot is an explicit not-published record, not a number.
    c = Check("S8", "Continued carries a ceiling and no floor value")
    for base, pop, block in _iter_payloads(inst):
        for arm_key, payload in (block.get("by_producing_arm") or {}).items():
            cont = ((payload or {}).get("bounds") or {}).get("continued")
            if not isinstance(cont, dict):
                continue
            c.sites += 1
            if "ceiling" not in cont:
                c.failures.append(f"{base}.by_producing_arm.{arm_key}: Continued has no ceiling")
            floor = cont.get("floor")
            absence_statuses = (
                "structurally_absent", "not_published", "not_yet_written", "unruled",
            )
            if (
                not isinstance(floor, dict)
                or floor.get("status") not in absence_statuses
                or "percent" in floor
            ):
                c.failures.append(
                    f"{base}.by_producing_arm.{arm_key}: the Continued floor is not an explicit "
                    f"absence record -- Continued must never be emitted as a point"
                )
    checks.append(c)

    # S9 -- three ceilings are never presented as simultaneous.
    c = Check("S9", "the three-ceiling block records that they cannot all hold")
    for base, pop, block in _iter_payloads(inst):
        for arm_key, payload in (block.get("by_producing_arm") or {}).items():
            cch = (payload or {}).get("ceilings_cannot_all_hold")
            if not isinstance(cch, dict):
                continue
            c.sites += 1
            if cch.get("simultaneous") is not False:
                c.failures.append(f"{base}.by_producing_arm.{arm_key}: simultaneous is not false")
            for field in ("sum_percent", "excess_pp", "excess_pairs"):
                if field not in cch:
                    c.failures.append(f"{base}.by_producing_arm.{arm_key}: missing {field}")
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
        for arm_key, payload in (block.get("by_producing_arm") or {}).items():
            bounds = (payload or {}).get("bounds") or {}
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
                            f"{base}.by_producing_arm.{arm_key}.bounds.{bname}.{ename}: "
                            f"population {enode.get('population')!r} != enclosing {pop!r}"
                        )
    checks.append(c)

    # S12 -- derived fields recompute. Arithmetic is not checkable on sentinels,
    #        so on a placeholder this reports the sites it WOULD check.
    c = Check("S12", "declared derived fields recompute from their stated expression")
    decl = inst.get("derived_fields", [])
    if is_placeholder:
        n = 0
        for base, pop, block in _iter_payloads(inst):
            for arm_key, payload in (block.get("by_producing_arm") or {}).items():
                bounds = (payload or {}).get("bounds") or {}
                n += sum(1 for b in bounds.values() if isinstance(b, dict) and "width_pp" in b)
        c.skipped_reason = (
            f"instance is a placeholder: all measurement slots hold sentinels, so no arithmetic "
            f"identity can be evaluated. {n} bound-width sites and {len(decl)} declared derived "
            f"fields would be checked on a real file."
        )
    else:
        for base, pop, block in _iter_payloads(inst):
            for arm_key, payload in (block.get("by_producing_arm") or {}).items():
                bounds = (payload or {}).get("bounds") or {}
                for bname, bnode in bounds.items():
                    if not isinstance(bnode, dict) or "width_pp" not in bnode:
                        continue
                    fl = (bnode.get("floor") or {}).get("percent")
                    ce = (bnode.get("ceiling") or {}).get("percent")
                    if not isinstance(fl, (int, float)) or not isinstance(ce, (int, float)):
                        continue
                    c.sites += 1
                    if abs((ce - fl) - bnode["width_pp"]) > 5e-4:
                        c.failures.append(
                            f"{base}.by_producing_arm.{arm_key}.bounds.{bname}: "
                            f"width_pp {bnode['width_pp']} != ceiling - floor {ce - fl}"
                        )
                    if fl > ce:
                        c.failures.append(
                            f"{base}.by_producing_arm.{arm_key}.bounds.{bname}: floor exceeds ceiling"
                        )
    checks.append(c)

    # S13 -- the waterfall is non-increasing under >=, and n_in/n_out/removed agree.
    c = Check("S13", "waterfall positions are non-increasing (>=) and removed = n_in - n_out")
    if is_placeholder:
        n = sum(
            len((w or {}).get("positions", []))
            for arm in inst.get("arms", [])
            for w in (arm.get("waterfall") or {}).values()
        )
        c.skipped_reason = (
            f"instance is a placeholder: position counts are sentinels. {n} waterfall positions "
            f"would be checked on a real file."
        )
    else:
        for i, arm in enumerate(inst.get("arms", [])):
            for pop, w in (arm.get("waterfall") or {}).items():
                prev = None
                for p in (w or {}).get("positions", []):
                    c.sites += 1
                    n_in, n_out = p.get("n_in"), p.get("n_out")
                    if isinstance(n_in, int) and isinstance(n_out, int):
                        if p.get("removed") != n_in - n_out:
                            c.failures.append(
                                f"$.arms[{i}].waterfall.{pop} position {p.get('position')}: "
                                f"removed != n_in - n_out"
                            )
                        if prev is not None and not (prev >= n_out):
                            c.failures.append(
                                f"$.arms[{i}].waterfall.{pop} position {p.get('position')}: "
                                f"count increased"
                            )
                        prev = n_out
    checks.append(c)

    # S14 -- an inert filter position states that it is inert and why.
    c = Check("S14", "every waterfall position marked inert carries a reason")
    for i, arm in enumerate(inst.get("arms", [])):
        for pop, w in (arm.get("waterfall") or {}).items():
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

    # S17 -- cross-arm figures the spec forbids reconciling are held twice.
    c = Check("S17", "figures reported-not-reconciled hold both arms' values and are flagged")
    for i, d in enumerate(inst.get("cross_arm_divergences", [])):
        c.sites += 1
        for field in ("figure", "arm_a", "arm_b", "reconciled", "reason"):
            if field not in d:
                c.failures.append(f"$.cross_arm_divergences[{i}]: missing {field}")
        if d.get("reconciled") is not False:
            c.failures.append(f"$.cross_arm_divergences[{i}]: reconciled is not false")
    checks.append(c)

    # S18 -- every CI names the bootstrap settings that produced it.
    c = Check("S18", "every confidence interval carries a bootstrap_ref")
    for path, node in _walk(inst):
        if isinstance(node, dict) and "lower" in node and "upper" in node and "level_pct" in node:
            c.sites += 1
            if "bootstrap_ref" not in node:
                c.failures.append(f"{path}: confidence interval with no bootstrap_ref")
    checks.append(c)

    # S19 -- every explicit absence record names a status and a reason.
    c = Check("S19", "every absence record states a status and a reason, so absent != inapplicable")
    for path, node in _walk(inst):
        if not (isinstance(node, dict) and "status" in node and node.get("status") in
                ("structurally_absent", "not_published", "not_yet_written", "unruled")):
            continue
        c.sites += 1
        if not isinstance(node.get("reason"), str) or len(node["reason"]) < 20:
            c.failures.append(f"{path}: absence record with no usable reason")
    checks.append(c)

    # S20 -- a degenerate (zero-width) bound says so, so it cannot read as missing data.
    c = Check("S20", "a bound marked degenerate carries a reason; width is present either way")
    for base, pop, block in _iter_payloads(inst):
        for arm_key, payload in (block.get("by_producing_arm") or {}).items():
            for bname, bnode in ((payload or {}).get("bounds") or {}).items():
                if not isinstance(bnode, dict) or "degenerate" not in bnode:
                    continue
                c.sites += 1
                if "width_pp" not in bnode:
                    c.failures.append(f"{base}.{arm_key}.bounds.{bname}: no width_pp")
                if bnode["degenerate"] is True and not bnode.get("degenerate_reason"):
                    c.failures.append(
                        f"{base}.{arm_key}.bounds.{bname}: degenerate with no reason"
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
            "producing_arm": {"a", "b"},
            "population": {"APPLY", "DERIV"},
            "absence_status": {"structurally_absent", "not_published"},
        }
        observed = {
            "clock_origin": {a.get("clock_origin") for a in inst.get("arms", [])},
            "producing_arm": set(),
            "population": set(),
            "absence_status": set(),
        }
        for base, pop, block in _iter_payloads(inst):
            observed["population"].add(pop)
            observed["producing_arm"] |= set((block.get("by_producing_arm") or {}).keys())
        for _, node in _walk(inst):
            if isinstance(node, dict) and node.get("status") in (
                "structurally_absent", "not_published", "not_yet_written", "unruled"
            ):
                observed["absence_status"].add(node["status"])
        for name, need in required_branches.items():
            c.sites += 1
            missing = need - (observed[name] - {None})
            if missing:
                c.failures.append(f"branch family {name!r} never exercises {sorted(missing)}")
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
