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
TOP_LEVEL_PUBLISHER = {
    "tested_ranges": "step13",
    "variants": "step13",
}
# The steps that publish a headline payload of their own.
HEADLINE_PUBLISHERS = ("step9", "step13")
# The entry families whose entries name their own producing step.
ENTRY_FAMILIES = ("arms", "variants", "subpopulation_cuts")


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
    """Yield (path, arm, ci) for every interval whose owning arm is knowable.

    An interval inside a payload belongs to that payload's arm; one under
    $.declared_intervals belongs to the arm the entry names. Nothing else in the
    file carries an interval.
    """
    for base, pop, block in _iter_payloads(inst):
        for ppath, akey, payload in _iter_arm_payloads(block, base):
            arm = _owning_arm_of(payload) or akey
            for path, node in _walk(payload):
                if isinstance(node, dict) and "lower" in node and "upper" in node \
                        and "bootstrap_ref" in node:
                    yield ppath + path[1:], arm, node
    for i, entry in enumerate(inst.get("declared_intervals") or []):
        ci = entry.get("ci")
        if isinstance(ci, dict) and "bootstrap_ref" in ci:
            yield f"$.declared_intervals[{i}].ci", entry.get("producing_arm"), ci


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

    # S2 -- arm identity is unique on the declared key, AND THE KEY IS THE ONE
    #       THE FILE DECLARES. The producing step joined the key at v1.4.0
    #       (decisions/0111 E2): Step 9's W = 108 and Step 13's W = 108 are
    #       different measurements of one setting and both must exist, so a
    #       two-field key would have called the second a duplicate of the first.
    c = Check("S2", "arm identity unique on (W_days, clock_origin, producing_step), "
                    "which is the key $.arm_key declares")
    declared_key = ((inst.get("arm_key") or {}).get("fields"))
    expected_key = ["W_days", "clock_origin", "producing_step"]
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
        if merged:
            absence_needed = {"structurally_absent", "not_published",
                              "no_producer_in_spec", "superseded_for_this_purpose",
                              "not_required_by_spec", "not_a_dual_step"}
        elif single_arm_file:
            absence_needed = {"not_required_by_spec", "not_a_dual_step"}
        else:
            absence_needed = {"structurally_absent", "not_published",
                              "no_producer_in_spec", "superseded_for_this_purpose"}
        required_branches = {
            "clock_origin": ({"s2_finale", "s2_premiere"} if not single_arm_file
                             else {"s2_finale"}),
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
            "quantity_class": {"outcome_shares", "window_w_percentile"},
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
        "carries no absent block; and ceilings are absent only where the bounds are",
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
        "every interval's inline B, seed, statistic and resampling unit equal the registry "
        "entry it references",
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
        # `statistic` added at v1.3.0 (reviewer-engineering M6): B, the seed and
        # the unit are fixed by decisions/0103 and are identical in both arms, so
        # the one bootstrap field the arms actually differ on was the one field
        # this check did not compare.
        for field in ("B", "seed", "statistic", "resampling_unit"):
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
        named: dict[str, int] = {}
        for path, node in _walk(inst):
            if isinstance(node, dict) and isinstance(node.get("merged_from"), str):
                named[node["merged_from"]] = named.get(node["merged_from"], 0) + 1
        for label, (step_of, arm_of) in labels.items():
            c.sites += 1
            if label not in named:
                c.failures.append(
                    f"$.document_scope.merge.sources_merged: the source ({step_of!r}, "
                    f"{arm_of!r}) is declared as an input and NO payload names it in "
                    f"merged_from -- a merge that drops an entire declared input is the "
                    f"inverse of the one this check was written for, and it needs no forgery, "
                    f"only an omission"
                )
        # A non-arm-file source names the blocks it fills, and those blocks are
        # where its provenance has to appear: its payloads are not per-arm, so no
        # walk of the arm keys would ever reach them.
        for label, blocks in non_arm_labels.items():
            for block in blocks:
                c.sites += 1
                entries = inst.get(block)
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
        # The five keys normalised below do NOT include `convention_definition`
        # -- arm a's convention in arm a's own words -- and a forger making the
        # copy internally coherent rewrites that sentence anyway. THE MOMENT THEY
        # DO, THIS COUNT INVERTS TO 0 OF N, which is exactly what a GENUINE merge
        # of two differing arms produces. So the count separates nothing past
        # that rung, and the note below says so rather than implying a signal it
        # does not have.
        _ARM_LABELS = ("producing_arm", "merged_from", "bootstrap_ref", "statistic",
                       "convention_label")

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
                f"once these five keys are normalised: {', '.join(_ARM_LABELS)}. This is NOT a "
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
    #        silence -- the arms' settings differ on the one field the spec does
    #        not fix, so the wrong reference misreports which statistic produced
    #        a published interval.
    c = Check(
        "S32",
        "every interval references bootstrap settings produced by the arm that owns it",
    )
    registry = inst.get("bootstrap_settings") or {}
    for path, arm, ci in _iter_cis_with_arm(inst):
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
    d9 = ((inst.get("channel_classes") or {}).get("d9") or {}).get("quantities") or {}
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
            if publisher != file_step:
                c.failures.append(
                    f"$.{name}: present in {file_step!r}'s file, and this block is published "
                    f"by {publisher!r}, which writes its own file under one file per step per "
                    f"arm"
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
}


def _absence_records_for(inst: dict, subject: str) -> list[tuple[str, dict]]:
    """The explicit absence records this file carries for `subject`."""
    out: list[tuple[str, dict]] = []
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
