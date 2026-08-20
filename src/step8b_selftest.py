"""Step 8b -- does each check have force?

A check that has never failed is not evidence that anything is right; it may be
a check that cannot fail. This script takes the emitted placeholder, applies one
targeted mutation per check, and asserts that the check FAILS on the mutated
file and PASSES on the unmutated one.

It also runs the two checks that are N/A on a placeholder -- the derived-figure
arithmetic and the waterfall monotonicity -- against a de-sentinelled copy, so
they are exercised somewhere rather than reported N/A and never run.

Three baselines, one per emitted placeholder: the merged document, a dual step's
arm file and a single-arm step's own file. One mutation family is applied to the
SCHEMA rather than to an instance, because S35's subject is the schema. And one
case is asserted as a REQUIRED NON-FAILURE with its own note: the fully
relabelled false merge, which passes -- it is the residual this build publishes,
and asserting it here stops the published limit drifting from the behaviour.

One case is not a mutation at all: the STATISTIC VOCABULARY LINK, added at v1.6.0
(decisions/0118). It reads the canonical bootstrap-statistic block off both writer
files, asserts the two copies are byte-identical, asserts the block names all four
fixed elements BY VALUE, and asserts this schema's bootstrap_statistic enum is
exactly the set the block names. It exists because the schema's tokens were typed
here and agreed with the spec by inspection only. A missing marker FAILS -- two
nothings compare equal, and a clean report over zero characters is the shape
CLAUDE.md names.

Writes its record to logs/step8b/selftest-<stamp>.json. Exit 0 iff every check
was shown to have force AND the vocabulary link holds.

    python3 src/step8b_selftest.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import step8b_validate as V  # noqa: E402
import step8b_schema as G  # noqa: E402
import step8b_run_stamp as RS  # noqa: E402
# THE BLOCK EXTRACTION AND THE FOUR REQUIRED ELEMENTS ARE IMPORTED, NOT COPIED
# (reviewer-engineering H2/E5 on the v1.6.0 review). This module used to hold its
# own _extract_block(), its own BEGIN/END markers and its own BLOCK_MUST_NAME
# tuple -- a second and third copy of one rule, and they ALREADY DISAGREED with
# check_surfaces.py on where the END marker is searched from: a quoted END marker
# in prose made one control report "END precedes BEGIN" and exit 1 while this one
# found the real block and reported ok. TWO CONTROLS, OPPOSITE VERDICTS, ONE FILE.
# CLAUDE.md: one register, imported by every script that checks -- and the fix for
# a duplicated-register finding must not introduce another.
import check_surfaces as CS  # noqa: E402

# THE SIX BLOCKS decisions/0111 E1 GAVE PER-ARM NESTING. Their ONE-ARM form is
# what decisions/0114 ratifies as closing HERE rather than in a fourth
# placeholder file: reviewer-engineering established the shape is representable
# and policed, so what was missing is an EXAMPLE, not a shape.
PER_ARM_NESTED_BLOCKS = (
    "d3_prime",
    "tested_ranges",
    "conclusions_surviving",
    "conclusions_not_surviving",
    "d2_recomputed_inside_this_arm",
    "action_type_counts",
)

SCHEMA_PATH = os.path.join(ROOT, "artifacts", "step8b-output-schema.json")
PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder.json")
# The ARM-FILE placeholder (decisions/0107). Half of the v1.2.0 behaviour is only
# observable on a file that is not the merged document: S17 skipping, S29's
# prohibition, and S28's one-file-per-arm clause.
ARM_PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder-arm-file.json")
# A SINGLE-ARM step's own file (Step 11, arm `sole`). Added at v1.3.0 with the
# granularity ruling (decisions/0109 §1): one file per step per arm, so a
# single-arm step's file must have a legal spine, and a spine described in prose
# and never emitted cannot be checked.
SOLE_PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder-sole-file.json")
LOG_DIR = os.path.join(ROOT, "logs", "step8b")


def _arm_with(inst: dict, block: str) -> dict:
    """The first arm entry that carries `block`.

    AN ARM ENTRY IS ONE STEP'S MEASUREMENT AT ONE SETTING since v1.4.0
    (decisions/0111 E2), so the waterfall, the abandonment distribution and D3'
    now sit in three DIFFERENT entries of the merged document. Indexing arms[0]
    and reaching for any of them was correct only while one entry held them all.
    """
    for arm in inst["arms"]:
        if block in arm and not arm[block].get("block_is_absent"):
            return arm
    raise KeyError(f"no arm entry carries {block}")


def _first_payload(inst: dict) -> dict:
    return inst["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["a"]


def _first_abandonment(inst: dict) -> dict:
    return _arm_with(inst, "abandonment_distribution")["abandonment_distribution"]["APPLY"][0]


def _first_ci(inst: dict) -> dict:
    return _first_payload(inst)["shares"]["never_started"]["ci"]


def _desentinel(node, seen=None):
    """Replace every sentinel with a plausible value, so the arithmetic checks run."""
    if isinstance(node, dict):
        return {k: _desentinel(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_desentinel(v) for v in node]
    if node == V.SENTINEL_COUNT or node == V.SENTINEL_PERCENT:
        return 0
    if isinstance(node, str) and node.startswith(V.PLACEHOLDER_PREFIX):
        return node[len(V.PLACEHOLDER_PREFIX) + 2:] or "text"
    return node


def _fix_ceilings(payload: dict) -> None:
    """Make the three-ceiling arithmetic consistent in the de-sentinelled copy."""
    bounds = payload.get("bounds") or {}
    cch = payload.get("ceilings_cannot_all_hold")
    if bounds.get("block_is_absent") or not isinstance(cch, dict) or cch.get("block_is_absent"):
        return
    total = 0.0
    for outcome in ("never_started", "started_and_left", "continued"):
        ceiling = (bounds.get(outcome) or {}).get("ceiling") or {}
        if isinstance(ceiling.get("percent"), (int, float)):
            total += ceiling["percent"]
    cch["sum_percent"] = total
    cch["excess_pp"] = total - 100


def _make_real(inst: dict) -> dict:
    """A structurally valid file flagged as real data, with consistent arithmetic."""
    real = _desentinel(copy.deepcopy(inst))
    real["placeholder"] = False
    real.pop("placeholder_notice", None)
    real["sentinels"] = inst["sentinels"]  # the reserved-value declaration stays literal
    # _desentinel maps every count to 0, and 0 is exactly what two of the v1.3.0
    # checks exist to reject: a search that ran and examined nothing, and a diff
    # that compared nothing. A real file has real counts, so they are set here --
    # and the divergence count is set from the entry list rather than typed, so
    # the identity the check asserts is not hand-maintained in two places.
    cad = real.get("cross_arm_divergences")
    if isinstance(cad, dict):
        n_entries = len(cad.get("entries") or [])
        cad.setdefault("search", {})["coverage_count"] = 17
        merge = (real.get("document_scope") or {}).get("merge")
        if isinstance(merge, dict) and isinstance(merge.get("diff"), dict):
            merge["diff"]["figures_compared"] = 17
            merge["diff"]["divergences_found"] = n_entries
    for q in (((real.get("channel_classes") or {}).get("d9") or {})
              .get("quantities") or {}).values():
        cov = (q or {}).get("coverage")
        if isinstance(cov, dict):
            cov["records_examined"] = 12345
            cov["records_with_a_slug"] = 12345
    for arm in real["arms"]:
        for pop, block in arm["headline"].items():
            for key, payload in block["by_producing_arm"]["arms"].items():
                bounds = payload.get("bounds") or {}
                if bounds.get("block_is_absent"):
                    continue
                for bname, bnode in bounds.items():
                    if "width_pp" not in bnode:
                        continue
                    bnode["floor"]["percent"] = 10.0
                    bnode["ceiling"]["percent"] = 12.0
                    bnode["width_pp"] = 2.0
                    bnode["degenerate"] = False
                    bnode["degenerate_reason"] = None
                    sub = bnode.get("conditional_sub_interval")
                    if isinstance(sub, dict) and sub.get("applicable") is True:
                        sub["floor"]["percent"] = 10.0
                        sub["ceiling"]["percent"] = 11.0
                        sub["width_pp"] = 1.0
                _fix_ceilings(payload)
        wf = arm.get("waterfall")
        if not isinstance(wf, dict) or wf.get("block_is_absent"):
            continue
        for pop, w in wf.items():
            n = 1000
            for p in w["positions"]:
                p["n_in"] = n
                p["n_out"] = n - 10
                p["removed"] = 10
                n = p["n_out"]
    for node in (real.get("variants", []) + real.get("subpopulation_cuts", [])):
        for pop, block in node["headline"].items():
            for key, payload in block["by_producing_arm"]["arms"].items():
                bounds = payload.get("bounds") or {}
                if bounds.get("block_is_absent"):
                    continue
                for bname, bnode in bounds.items():
                    if "width_pp" not in bnode:
                        continue
                    bnode["floor"]["percent"] = 10.0
                    bnode["ceiling"]["percent"] = 12.0
                    bnode["width_pp"] = 2.0
                    bnode["degenerate"] = False
                    bnode["degenerate_reason"] = None
                    sub = bnode.get("conditional_sub_interval")
                    if isinstance(sub, dict) and sub.get("applicable") is True:
                        sub["floor"]["percent"] = 10.0
                        sub["ceiling"]["percent"] = 11.0
                        sub["width_pp"] = 1.0
                _fix_ceilings(payload)
    return real


MUTATIONS = {
    "S1": lambda i: i.pop("placeholder_notice"),
    "S2": lambda i: i["arms"].append(copy.deepcopy(i["arms"][0])),
    "S3": lambda i: _set(_first_payload(i)["shares"]["never_started"]["ci"],
                         "bootstrap_ref", "no_such_settings"),
    "S4": lambda i: _set(_first_payload(i)["bounds"]["never_started"],
                         "scope_qualifier_ref", "no_such_qualifier"),
    "S5": lambda i: _set(_first_payload(i)["shares"]["never_started"],
                         "value_percent", 16.7231),
    "S6": lambda i: _set(_first_payload(i)["bounds"]["never_started"], "note",
                         "a real note that lost its prefix"),
    "S7": lambda i: _set(
        _first_payload(i)["bounds"]["never_started"]["conditional_sub_interval"],
        "applicable", True),
    "S8": lambda i: _set(_first_payload(i)["bounds"]["continued"], "floor",
                         {"status": None}),
    "S9": lambda i: _first_payload(i)["ceilings_cannot_all_hold"].pop("excess_pairs"),
    "S10": lambda i: _first_abandonment(i)["p_at_bound"][
        "column_cardinalities"].pop("false_count"),
    "S11": lambda i: _set(_first_payload(i)["bounds"]["never_started"]["floor"],
                          "population", "DERIV"),
    "S12": lambda i: _set(_first_payload(i)["bounds"]["never_started"], "width_pp", 99.0),
    "S13": lambda i: _set(_arm_with(i, "waterfall")["waterfall"]["APPLY"]["positions"][3],
                          "removed", 7),
    "S14": lambda i: _set(_arm_with(i, "waterfall")["waterfall"]["APPLY"]["positions"][0],
                          "inert_reason", None),
    "S15": lambda i: _set(i["channel_classes"]["d4"], "folded_into_bound", True),
    "S16": lambda i: i["channel_classes"]["d9"]["quantities"]["half_a"].pop("coverage"),
    "S17": lambda i: _set(i["cross_arm_divergences"]["entries"][0], "reconciled", True),
    "S18": lambda i: _first_payload(i)["shares"]["continued"]["ci"].pop("bootstrap_ref"),
    "S19": lambda i: _set(_first_payload(i)["bounds"]["continued"]["floor"], "reason", "no"),
    "S20": lambda i: _set(_first_payload(i)["bounds"]["never_started"], "degenerate", True),
    "S21": lambda i: [
        _set(a, "clock_origin", "s2_finale") for a in i["arms"]
        if a.get("clock_origin") == "s2_premiere"],
    # v1.1.0 -- one mutation per check added against reviewer-engineering's
    # findings, so that none of them is a check that cannot fail.
    "S22": lambda i: _set(
        _arm_with(i, "waterfall"), "waterfall",
        {"block_is_absent": True, "status": "no_producer_in_spec",
         "reason": "an absence written onto the primary headline arm, where a producer exists",
         "source": "selftest", "owning_step": "step8"}),
    "S23": lambda i: _set(_first_ci(i), "B", 5),
    "S24": lambda i: _set(_first_ci(i), "quantity_class", "window_w_percentile"),
    "S25": lambda i: _set(_first_abandonment(i), "row_set", "post_liveness"),
    "S26": lambda i: _first_abandonment(i)["histograms"][0]["bin_edges_p"].pop(),
    "S27": lambda i: i["block_ownership"].pop("arms"),
    # v1.2.0 -- one mutation per check added against decisions/0107.
    "S28": lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"], "arms_in_this_file", "one_arm"),
    "S29": lambda i: i.pop("cross_arm_divergences"),
    # v1.3.0 -- one mutation per check added against decisions/0109 and
    # reviewer-engineering's M1, M2, M6, M7, M8 and M10.
    #
    # S30 IS THE FINDING ITSELF, in its naive form: arm b's payload is a
    # deep copy of arm a's, relabelled. Before v1.3.0 the whole file validated
    # and published that the arms agreed everywhere.
    "S30": lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"],
        "b", _relabel_arm(copy.deepcopy(
            i["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["a"]), level=1)),
    # M2: RELABELLING, not widening. The shape is untouched -- a Step 9 block
    # simply declares itself single-arm, which is what disarms the merged
    # document's dropped-arm clause.
    "S31": lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"],
        "step_dual_status", "single_arm"),
    # M6: arm a's interval pointing at arm b's settings, which differ on the one
    # bootstrap field the spec does not fix.
    "S32": lambda i: _set(_first_ci(i), "bootstrap_ref", "b_default"),
    # M7: a search that ran and examined nothing.
    "S33": lambda i: _set(i["cross_arm_divergences"]["search"], "coverage_count", 0),
    # M8: ownership at depth 1 only.
    "S34": lambda i: i["block_ownership"].pop("arms[].abandonment_distribution"),
    # v1.4.0 -- decisions/0111. S36 IS THE Q1 FINDING ITSELF: a block written
    # into an entry whose producing step does not publish it. Only absences were
    # policed before, so the file was checked for writing too little and never
    # for writing too much.
    "S36": lambda i: _set(
        _arm_with(i, "waterfall"), "action_type_counts",
        copy.deepcopy(_arm_with(i, "action_type_counts")["action_type_counts"])),
    # v1.5.0 -- decisions/0114.
    #
    # E14: an entry measured under a revision the file does not account for. This
    # is the case the fourth key dimension exists for, in its simplest form: two
    # runs at one setting under different rule revisions are DIFFERENT
    # MEASUREMENTS, and a document that carries one without saying so is a
    # document whose key lies about what it holds.
    "S37": lambda i: _set(i["arms"][0], "adopted_rule_revision", 3),
    # E11: an interval attributed to a step that does not produce that quantity.
    # THE SHIPPED PLACEHOLDERS WERE OCCUPIED BY THIS -- the window-W percentile
    # attributed to `step11`, which does not compute W.
    #
    # THE CLASS MOVED TO `window_w_percentile` AT v1.9.0, AND THE CONTROL IS WHAT
    # FOUND IT. This mutation used to attribute an OUTCOME-SHARES interval to
    # `step10`; the Human Lead ruling of 2026-08-20 makes Step 10 a legal
    # publisher of that class, so the mutation stopped failing and the selftest
    # reported S38 in `checks_without_force`. The window-W percentile is the class
    # Step 10 did NOT join -- it does not vary W -- so this is the same finding on
    # the row that is still false, and it now exercises the asymmetry the ruling
    # created rather than the one it removed. The entry is located by PREDICATE:
    # an index would move with the placeholder, and a mutation that cannot be
    # applied is itself a finding here.
    "S38": lambda i: _set(_first_interval_of_class(i, "window_w_percentile"),
                          "produced_by_step", "step10"),
    # v1.6.0 -- decisions/0118.
    #
    # S40 IS THE STALE STATE ITSELF, reconstructed: the registry recording ONE
    # statistic per arm, which is what every emitted artifact carried until this
    # version. It is the shape the ruling removed -- a per-arm choice where the
    # spec now fixes a value.
    "S40": lambda i: _set(i["bootstrap_settings"]["a_default"], "statistics", ["movements"]),
    # S41: a file that DECLARES both objects and EMITS one. The registry is
    # untouched, so S40 still passes and only S41 can catch it -- which is the
    # whole reason the two are separate checks. This is "a run that emits only
    # one", the state decisions/0118 calls INCOMPLETE rather than differently
    # designed.
    "S41": lambda i: [
        _set(e["ci"], "statistic", "levels")
        for e in i["declared_intervals"] if isinstance(e.get("ci"), dict)],
}


# WHAT THE REGISTRY COMPARISON LEAVES OUT, AND WHY (v1.9.0,
# reviewer-engineering F5). Declared with a reason rather than implied by a
# whitelist of what to include: an exclusion has to be argued for, and a field
# nobody thought about must join the comparison rather than fall out of it.
REGISTRY_FIELDS_EXCLUDED_FROM_THE_COMPARISON = {
    "note": "free writer prose at the point of use. Two entries of one class carry different "
            "sentences about themselves and that is not a settings difference -- it is the "
            "only field in the registry whose content is expected to vary per entry",
}

# WHAT MAY DIFFER BETWEEN TWO ENTRIES OF ONE QUANTITY CLASS. Written from
# decisions/0118 and V.REGISTRY_ARM_DIFFERENCE_FACT's own claim: with all four
# bootstrap elements fixed and identical across the arms, two entries of one
# class differ ONLY in which arm they belong to. Held here rather than derived,
# so that a registry drifting apart on any other field fails this selftest.
REGISTRY_FIELDS_THAT_MAY_DIFFER_WITHIN_A_CLASS = {"producing_arm"}


# THE MALFORMED HEADLINE SHAPES (v1.9.0, reviewer-engineering F1). Not mutations
# in the has-force sense -- they break the file's TYPES rather than its content,
# so what they exercise is the validator's ability to report at all. All three
# were reproduced through validate_file() on the shipped merged placeholder
# before the guard was written; all three raised.
#
# A FOURTH SHAPE IS DELIBERATELY ABSENT: `headline` set to an EMPTY list never
# raised, because `node.get("headline") or {}` treats it as falsy. Recorded so
# the omission is a finding rather than a gap.
MALFORMED_HEADLINES = {
    # `.items()` on a block-absence record yields the BOOL `True` as a block.
    "headline_is_a_block_absence_record":
        lambda i: i["arms"][0].__setitem__("headline", {"block_is_absent": True}),
    # one population block replaced by a string.
    "headline_population_is_a_string":
        lambda i: i["arms"][0]["headline"].__setitem__("APPLY", "PLACEHOLDER"),
    # a non-empty list has no `.items()` at all.
    "headline_is_a_nonempty_list":
        lambda i: i["arms"][0].__setitem__("headline", [{"APPLY": {}}]),
}


def _first_interval_of_class(inst: dict, quantity_class: str) -> dict:
    """The first `$.declared_intervals` entry on a given quantity class.

    BY PREDICATE, NOT BY INDEX (v1.9.0). A mutation that names
    `declared_intervals[0]` mutates whatever the generator happens to emit first,
    so the CLASS it exercises drifts with the placeholder rather than being
    chosen. Raises when there is none: the harness records an unapplied mutation
    as a finding, which is the right answer for a fixture whose subject has
    vanished.
    """
    for entry in inst.get("declared_intervals") or []:
        if (entry.get("ci") or {}).get("quantity_class") == quantity_class:
            return entry
    raise AssertionError(
        f"no $.declared_intervals entry on quantity class {quantity_class!r}: this mutation "
        f"has no subject in the fixture"
    )


def _relabel_arm(node, level: int):
    """Relabel a copied arm-a payload as arm b, at three degrees of effort.

    level 1 relabels the arm only; level 2 also relabels the bootstrap
    references and the sampling-width convention labels; level 3 also relabels
    the merge provenance. The three are the M1 forgery ladder, and the point of
    running all three is to show WHICH rung the check stops at.

    THE STATISTIC LEFT THE LADDER AT v1.6.0 (decisions/0118), and it left because
    the ruling took it out rather than because the ladder was wrong. Level 2 used
    to rewrite `statistic` to "levels", because arm a's statistic was "movements"
    and arm b's was "levels" and a coherent forgery had to change it. The
    statistic is now fixed as BOTH for every arm, so it is no longer an
    arm-distinguishing label and rewriting it would CHANGE THE OBJECT rather than
    relabel the arm -- turning a movement interval into a levels one. THE FORGERY
    IS ONE FIELD CHEAPER THAN IT WAS: the arms' bootstrap records now differ only
    in `producing_arm`. That is a real consequence of fixing the statistic and it
    is recorded here rather than left to be inferred from a ladder that still
    passes.
    """
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in ("producing_arm", "arm_held") and v == "a":
                out[k] = "b"
            elif k == "bootstrap_ref" and level >= 2 and isinstance(v, str):
                out[k] = v.replace("a_", "b_", 1)
            elif k == "convention_label" and level >= 2 and isinstance(v, str):
                out[k] = v.replace("arm_a", "arm_b")
            elif k == "merged_from" and level >= 3 and isinstance(v, str):
                out[k] = v.replace("arm `a`", "arm `b`")
            else:
                out[k] = _relabel_arm(v, level)
        return out
    if isinstance(node, list):
        return [_relabel_arm(v, level) for v in node]
    return node


def _forge_merge(inst: dict, level: int) -> dict:
    """Assemble the merged document's second arm from the first arm's payload."""
    def visit(node):
        if isinstance(node, dict):
            bpa = node.get("by_producing_arm")
            if isinstance(bpa, dict) and set(bpa.get("arms") or {}) == {"a", "b"}:
                bpa["arms"]["b"] = _relabel_arm(copy.deepcopy(bpa["arms"]["a"]), level)
            for v in node.values():
                visit(v)
        elif isinstance(node, list):
            for v in node:
                visit(v)
    visit(inst)
    return inst

def _drop_source(inst: dict, step: str, arm: str | None) -> dict:
    """Drop a declared merge source AND every payload that named it.

    THE POINT IS THAT NOTHING INSIDE THE FILE CONTRADICTS ANYTHING ELSE IN IT
    afterwards: the declared list and the payloads close against each other, and
    only a table held OUTSIDE the file can see that a source is missing
    (decisions/0114, E9/E15).
    """
    srcs = inst["document_scope"]["merge"]["sources_merged"]
    dropped = [s for s in srcs
               if s.get("producing_step") == step and s.get("arm") == arm]
    labels = {s["file_label"] for s in dropped}
    inst["document_scope"]["merge"]["sources_merged"] = [s for s in srcs if s not in dropped]

    def prune(node):
        if isinstance(node, dict):
            for v in node.values():
                prune(v)
        elif isinstance(node, list):
            for v in list(node):
                if isinstance(v, dict) and v.get("merged_from") in labels:
                    node.remove(v)
                else:
                    prune(v)

    for family in ("arms", "variants", "subpopulation_cuts"):
        inst[family] = [e for e in inst.get(family, [])
                        if e.get("producing_step") != step]
    inst["declared_intervals"] = [d for d in inst.get("declared_intervals", [])
                                  if d.get("produced_by_step") != step]
    prune(inst)
    return inst


def _mention_only(inst: dict) -> dict:
    """A declared source whose ONLY appearance is a $.declared_intervals entry.

    Leg (e) walked every node carrying a `merged_from` string, so a reference to
    a file discharged the requirement that a payload came from it.
    """
    label = None
    for s in inst["document_scope"]["merge"]["sources_merged"]:
        if s.get("producing_step") == "step10":
            label = s["file_label"]
    inst["arms"] = [a for a in inst["arms"] if a.get("producing_step") != "step10"]
    template = copy.deepcopy(inst["declared_intervals"][0])
    template.update({
        "interval_id": "mention_only",
        "produced_by_step": "step10",
        "producing_arm": "sole",
        "merged_from": label,
    })
    inst["declared_intervals"].append(template)
    return inst


def _narrow_registry(inst: dict) -> dict:
    """Report a MOVEMENT against a registry entry that declares only levels.

    S23's statistic clause is a MEMBERSHIP test since v1.6.0 (decisions/0118), so
    the mutation that breaks it has to shrink the referenced entry -- there is no
    single registry statistic left to disagree with. Both edits are needed
    together: an interval labelled `movements` and an entry that does not declare
    it. S40 fails on the same file, which is expected and irrelevant: the runner
    reads only the target check's status.
    """
    ci = _first_ci(inst)
    ci["statistic"] = "movements"
    inst["bootstrap_settings"][ci["bootstrap_ref"]]["statistics"] = ["levels"]
    return inst


# Extra mutations that target a SECOND clause of a check whose first clause is
# already exercised above. Keyed by the check they must break.
EXTRA_MUTATIONS = {
    "S12/machine_checked_flags": ("S12", "placeholder", lambda i: _set(
        i["derived_fields"][0], "machine_checked", False)),
    "S13/chaining": ("S13", "real", lambda i: _set(
        _arm_with(i, "waterfall")["waterfall"]["APPLY"]["positions"][3], "n_in", 4242)),
    "S17/empty_and_unsearched": ("S17", "placeholder", lambda i: _set(
        _set(i["cross_arm_divergences"], "entries", []),
        "search", dict(i["cross_arm_divergences"]["search"], performed=False))),
    "S18/inline_settings": ("S18", "placeholder", lambda i: _first_ci(i).pop("seed")),
    # v1.6.0, decisions/0118: the statistic is required AT THE POINT OF USE, so
    # an interval that carries a bootstrap_ref and no statistic must fail. It
    # could not before -- S18 did not ask for the field, because until the
    # statistic was fixed there was nothing to hold a writer to.
    "S18/inline_statistic": ("S18", "placeholder", lambda i: _first_ci(i).pop("statistic")),
    # S23's SECOND clause, added at v1.6.0: the comparison is MEMBERSHIP now, so
    # the mutation that breaks it is a statistic the referenced entry does not
    # declare -- not a mismatch with a single registry value, which no longer
    # exists.
    "S23/statistic_not_in_registry": ("S23", "placeholder", lambda i: _narrow_registry(i)),
    # S40's PARTITION clause, which is the half that makes an EMPTY
    # fields_not_fixed_in_spec mean something. Dropping `statistics` from the
    # fixed list leaves it in neither list, so the two no longer cover the
    # declared universe.
    "S40/partition_of_fields_considered": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_spec"], "fields_fixed_in_spec", ["B", "seed", "resampling_unit"])),
    # S40's THIRD clause: the statistic listed as UNFIXED after it was fixed --
    # the exact string this rerun exists to remove from seven artifact lines.
    "S40/statistic_listed_as_unfixed": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_spec"], "fields_not_fixed_in_spec",
        ["statistic (levels vs movements)"])),
    # S40's RENAME clause: a writer emitting the old singular key. The schema's
    # additionalProperties: false catches it structurally; this asserts the
    # SEMANTIC check names it too, so the diagnosis is the rename rather than
    # "unexpected property".
    "S40/singular_statistic_key_survives": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_default"], "statistic", "movements")),
    # v1.7.0 -- reviewer-engineering E1 and E2 on the v1.6.0 review.
    #
    # E1, THE FINDING ITSELF: `spec_status` carried the claim and NOTHING READ IT.
    # An entry declaring itself unfixed while listing all four elements as fixed
    # validated at 41 checks, 0 failures. The retired token is asserted separately
    # from a merely wrong one, because the schema enum catches the first
    # structurally and this asserts the SEMANTIC check names it too -- so the
    # diagnosis is the retirement rather than "not one of the allowed values".
    "S40/spec_status_retired_token": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_default"], "spec_status", "unfixed_at_time_of_writing")),
    "S40/spec_status_contradicts_its_own_lists": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_default"], "spec_status", "partly_fixed_in_spec")),
    # And the mirror: an entry whose lists say partly while it declares fixed.
    "S40/spec_status_fixed_while_a_field_is_open": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_show_clustered"], "spec_status", "fixed_in_spec")),
    # E2, THE FINDING ITSELF: the ENTRY-level fixed list had no partition anchor,
    # so `["statistics"]` -- B, the seed and the unit silently dropped -- passed on
    # the one assertion there was, membership of `statistics`.
    "S40/entry_fixed_list_drops_three_elements": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_default"], "fields_fixed_in_spec", ["statistics"])),
    # The anchor itself removed: without it the entry declares no universe, and an
    # empty not-fixed list is indistinguishable from an unfilled one.
    "S40/entry_universe_not_declared": ("S40", "placeholder", lambda i: _set(
        i["bootstrap_settings"]["a_default"], "fields_considered", [])),
    # v1.8.0 -- reviewer-engineering E4 on the v1.7.0 review. THE ANCHOR WAS READ
    # OUT OF THE ENTRY UNDER TEST. E2's fix required the two lists to partition
    # `fields_considered`, and `fields_considered` is the writer's own free list --
    # so an entry declaring a universe of ONE element partitioned it perfectly and
    # dropped B, the seed and the unit out of the record entirely. decisions/0111
    # E4 -- a table read from the file under test could only agree with itself --
    # REINSTALLED BY THE FIX FOR E2, which is the same hole the first S41 fixture
    # had and caught. Both levels get a mutation, because the anchor is applied at
    # both and a check written once can still be called once.
    "S40/entry_universe_narrowed_to_agree_with_itself": ("S40", "placeholder", lambda i: _set(
        _set(_set(i["bootstrap_settings"]["a_default"], "fields_considered", ["statistics"]),
             "fields_fixed_in_spec", ["statistics"]),
        "fields_not_fixed_in_spec", [])),
    "S40/spec_universe_narrowed_to_agree_with_itself": ("S40", "placeholder", lambda i: _set(
        _set(_set(i["bootstrap_spec"], "fields_considered", ["statistics"]),
             "fields_fixed_in_spec", ["statistics"]),
        "fields_not_fixed_in_spec", [])),
    # THE SINGLE-ARM BRANCH IS NOT LOOSENED BY THE SPLIT (decisions/0107 §4). A
    # single-arm step's block claiming two arms is the mirror defect of the one
    # v1.2.0 fixes, and it must fail rather than validate silently.
    "S28/single_arm_step_claims_two_arms": ("S28", "placeholder", lambda i: _set(
        _set(i["subpopulation_cuts"][0]["headline"]["APPLY"]["by_producing_arm"],
             "arms_in_this_file", "both_arms"),
        "arms", {"a": copy.deepcopy(
            i["subpopulation_cuts"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["sole"]),
            "b": copy.deepcopy(
            i["subpopulation_cuts"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["sole"])})),
    # A merged document that carries only one arm of a DUAL step has dropped an
    # arm, and the diff it exists to publish cannot be there.
    "S28/merged_document_drops_an_arm": ("S28", "placeholder", lambda i: _set(
        _set(i["arms"][0]["headline"]["APPLY"]["by_producing_arm"], "arms_in_this_file",
             "one_arm"),
        "arm_held", "a")),
    # THE M1 FORGERY LADDER. Rung 1 is the finding as reported; rung 2 is the
    # same copy with its bootstrap references and convention labels relabelled.
    # Both must be rejected. Rung 3 -- merge provenance relabelled too -- is the
    # published residual and is NOT asserted here, because it passes: at that
    # point the file asserts a second input file exists, and nothing inside it
    # can contradict that.
    "S30/false_merge_naive_copy": ("S30", "placeholder", lambda i: _forge_merge(i, 1)),
    "S30/false_merge_refs_relabelled": ("S30", "placeholder", lambda i: _forge_merge(i, 2)),
    # The merge declares one input file for two arms of a dual step.
    "S30/one_input_file_for_two_arms": ("S30", "placeholder", lambda i: _set(
        i["document_scope"]["merge"], "sources_merged",
        [dict(e, arm="b") if e["arm"] == "a" and e["producing_step"] == "step9" else e
         for e in i["document_scope"]["merge"]["sources_merged"]])),
    # A diff whose two sides are the same file is not a diff.
    "S30/diff_against_itself": ("S30", "placeholder", lambda i: _set(
        i["document_scope"]["merge"]["diff"]["pairs_diffed"][0], "arm_b_file",
        i["document_scope"]["merge"]["diff"]["pairs_diffed"][0]["arm_a_file"])),
    # The registry itself relabelled, rather than one block (M2).
    "S31/registry_relabelled": ("S31", "placeholder", lambda i: _set(
        i["step_duality"]["step13"], "dual_status", "single_arm")),
    # M7's second site: a bound published on zero records examined.
    "S33/d9_zero_coverage": ("S33", "real", lambda i: _set(
        _set(i["channel_classes"]["d9"]["quantities"]["half_a"]["coverage"],
             "records_examined", 0),
        "records_with_a_slug", 0)),
    # M8's second clause: a per-arm block that does not say who publishes it.
    "S34/publisher_not_named": ("S34", "placeholder", lambda i: i["block_ownership"][
        "arms[].waterfall"].pop("published_by_step")),
    # v1.4.0 -- decisions/0111.
    #
    # E3b, THE FINDING ITSELF AND IT NEEDS NO FORGERY: drop the one payload that
    # names a declared input, and the merge has an input supplying nothing. Under
    # S30's old one-way reading this validated clean.
    "S30/declared_input_named_by_no_payload": ("S30", "placeholder", lambda i: _set(
        i, "subpopulation_cuts",
        [c for c in i["subpopulation_cuts"] if c.get("producing_step") != "step12"])),
    # E6: the non-arm-file source is declared and its block does not name it.
    "S30/non_arm_source_not_named_by_its_block": ("S30", "placeholder", lambda i: [
        e.pop("merged_from") for e in i["limitations"]]),
    # E2: the producing step dropped out of the declared key, which is how two
    # steps' measurements at one setting would start colliding again.
    "S2/producing_step_dropped_from_the_key": ("S2", "placeholder", lambda i: _set(
        i["arm_key"], "fields", ["W_days", "clock_origin"])),
    # E2's second half: the LABEL. Several entries share a setting now, so an
    # arm_id that names only the setting reintroduces the collision for any
    # consumer that indexes by it.
    "S2/arm_id_label_collides": ("S2", "placeholder", lambda i: _set(
        i["arms"][1], "arm_id", i["arms"][0]["arm_id"])),
    # And a reference a consumer cannot follow: a variant or cut whose base arm
    # names no entry. The label changed shape at v1.4.0, so a stale reference is
    # exactly the failure to guard.
    "S2/base_arm_id_names_no_entry": ("S2", "placeholder", lambda i: _set(
        i["variants"][0], "base_arm_id", "W108_s2_finale")),
    # E4: the file rewrites its OWN ownership table. Before v1.4.0 S22 read that
    # table out of the file under test, so this was the whole of a self-exemption.
    "S22/self_exempting_ownership_table": ("S22", "placeholder", lambda i: _set(
        i["block_ownership"]["arms[].retained_by_air_period"],
        "published_by_step", "step13")),
    # E1: a second member of the by_producing_arm family reached through a branch
    # keyword. S35 guarded one member of six before v1.4.0.
    "S36/variant_carries_another_steps_block": ("S36", "placeholder", lambda i: _set(
        i["subpopulation_cuts"][0], "d3_prime",
        copy.deepcopy(_arm_with(i, "d3_prime")["d3_prime"]))),
    # v1.5.0 -- decisions/0114.
    #
    # E9/E15, THE FINDING ITSELF AND IT NEEDS NO FORGERY: drop a declared source
    # AND the payloads it supplied, so the file closes against itself. Every leg
    # of S30 before v1.5.0 read the declared list against this file's own
    # payloads, so a merge declaring five of eight sources validated clean. The
    # anchor is derived from STEP_DUALITY, outside the file.
    "S30/declares_a_subset_of_the_expected_sources": ("S30", "placeholder", lambda i: _drop_source(
        i, "step12", "sole")),
    # E9/E15's second half: leg (e) proved MENTION, not CONTRIBUTION. A
    # declared_intervals entry references a file; it is not a payload from one,
    # and it used to discharge the requirement on its own.
    "S30/mention_is_not_contribution": ("S30", "placeholder", _mention_only),
    # E8: a filled copy of Step 8's block in the merged document's own file is
    # legal; an ABSENCE there is not, because every other file states the absence
    # and the figure would then be nowhere.
    "S36/merged_document_states_the_absence_instead_of_filling_it": (
        "S36", "placeholder", lambda i: _set(
            i, "channel_classes",
            {"block_is_absent": True, "status": "not_required_by_spec",
             "reason": "an absence written where the block is actually published",
             "owning_step": "step13b", "source": "selftest"})),
    # E14's second clause: the registry that says where the revision was READ
    # from, without which each entry's revision is a claim with nothing behind it.
    "S37/registry_absent": ("S37", "placeholder", lambda i: i.pop("adopted_rule_revision")),
    "S37/typed_not_read": ("S37", "placeholder", lambda i: _set(
        i["adopted_rule_revision"], "read_not_typed", False)),
}

# Cases exercised against the ARM-FILE placeholder rather than the merged one.
# Half of the v1.2.0 behaviour is invisible on the merged document.
ARM_MUTATIONS = {
    # An arm file that CARRIES the block still fails: S17's requirement is
    # skipped for an arm file, the prohibition is not.
    "S17/arm_file_carries_the_merge_only_block": ("S17", lambda i: _set(
        i, "cross_arm_divergences",
        {"search": {"performed": True, "coverage_count": 3, "owner_step": "human_lead",
                    "what_was_searched": "a search an isolated arm could not have run",
                    "empty_reason": None},
         "entries": []})),
    "S29/arm_file_carries_the_merge_only_block": ("S29", lambda i: _set(
        i, "limitations",
        [{"id": "x", "text": "a Human Lead block an arm file may not carry",
          "source": "selftest", "direction": None, "may_be_netted_with_others": False}])),
    # One file per arm: a block holding an arm other than the file's own.
    "S28/arm_file_holds_another_arm": ("S28", lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"], "arm_held", "b")),
    # The merge arriving through the side door: a Human Lead step named among an
    # arm file's writers.
    "S28/arm_file_written_by_a_human_lead_step": ("S28", lambda i: _set(
        i["document_scope"], "also_written_by_steps", ["step8", "step13", "step13b"])),
    # ONE FILE PER STEP PER ARM (decisions/0109 §1), the half that was unchecked:
    # another step's payload in this step's file.
    "S28/arm_file_holds_another_steps_payload": ("S28", lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"], "producing_step", "step13")),
    "S28/arm_file_names_a_second_writer": ("S28", lambda i: _set(
        i["document_scope"], "also_written_by_steps", ["step13"])),
    # An arm file was merged from nothing, so it may not claim to have been.
    "S30/arm_file_claims_merge_provenance": ("S30", lambda i: _set(
        i["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["a"],
        "merged_from", "some other arm's file")),
    # v1.5.0 -- decisions/0114 E8. THE FINDING ITSELF: an arm file that FILLS
    # Step 8's block instead of stating its absence. `channel_classes` was
    # REQUIRED at the top level of every file, so this was not a thing a writer
    # had to reach for -- it was the only legal shape, and seven arm files each
    # had to produce it.
    "S36/arm_file_fills_step_8s_block": ("S36", lambda i: _set(
        i, "channel_classes",
        {"d4": {"definition": "a copy of Step 8's D4 count made by an arm",
                "published_alongside": True, "folded_into_bound": False,
                "computed_by": "step8", "copied_not_computed": True,
                "counts": {"APPLY": V.SENTINEL_COUNT, "DERIV": V.SENTINEL_COUNT}},
         "d9": {"published_alongside": True, "folded_into_bound": False,
                "computed_by": "step8", "copied_not_computed": True,
                "keys": {"strict": "s", "loose": "l"},
                "universe": {"label": "U1", "definition": "d"},
                "quantities": {}}})),
    "S36/arm_file_fills_the_overlap_block": ("S36", lambda i: _set(
        i, "discovery_channel_overlap",
        [{"unit": "accounts_pulled", "numerator": V.SENTINEL_COUNT,
          "denominator": V.SENTINEL_COUNT,
          "consumer": "PLACEHOLDER — NOT A MEASUREMENT: a copy made by an arm",
          "single_categorical_forbidden": True}])),
    # decisions/0114 E11: an arm file carrying ANOTHER STEP's interval, at its own
    # arm, so no bootstrap-arm control fires instead and this clause is the only
    # thing that can catch it.
    "S38/arm_file_carries_another_steps_interval": ("S38", lambda i: _set(
        i["declared_intervals"][0], "produced_by_step", "step13")),
    # decisions/0114 E14: one arm file is one run, and one run is one revision.
    "S37/arm_file_entry_disagrees_with_its_own_registry": ("S37", lambda i: _set(
        i["arms"][0], "adopted_rule_revision", 3)),
    # decisions/0114 E13, THE OTHER SIDE OF THE RULING, and it must keep failing:
    # ABSENCE STATED, NOT SILENCE. The figure stops being required at an arm
    # where no step produces it; the RECORD does not.
    "S22/silence_where_the_absence_is_legal": ("S22", lambda i: [
        (a.__setitem__("is_primary_headline", a.get("clock_origin") == "s2_premiere"),
         [a.pop(b, None) for b in ("waterfall", "liveness_exclusions",
                                   "retained_by_air_period")]
         if a.get("clock_origin") == "s2_premiere" else None)
        for a in i["arms"]]),
}

# Cases exercised against the SINGLE-ARM step's own file. THE Q1 FINDING SHIPPED
# IN THIS FILE: it declared five blocks absent on the reasoning that "writing a
# copy here would be a second place that figure lives", and then wrote
# `action_type_counts`, which its own ownership table marks published_by_step
# step9, may_first_writer_fill false. Both mutations below are that file as it
# shipped, reconstructed on the current one.
SOLE_MUTATIONS = {
    "S36/sole_file_writes_another_steps_per_arm_block": ("S36", lambda i: _set(
        i["arms"][0], "action_type_counts",
        {"by_producing_arm": {
            "step_dual_status": "dual", "arms_in_this_file": "one_arm",
            "producing_step": "step13", "arm_held": "a",
            "arms": {"a": {"producing_arm": "a", "written_by_step": "step13",
                           "counts": {"s1_watch": V.SENTINEL_COUNT}}}}})),
    "S36/sole_file_writes_another_steps_top_level_block": ("S36", lambda i: _set(
        i, "tested_ranges",
        {"by_producing_arm": {
            "step_dual_status": "dual", "arms_in_this_file": "one_arm",
            "producing_step": "step13", "arm_held": "a",
            "arms": {"a": {"producing_arm": "a", "written_by_step": "step13",
                           "ranges": {"W_days": {"values": [108]}}}}}})),
}

# Mutations applied to the SCHEMA rather than to an instance. S35 exists to
# machine-check the constraint decisions/0109 §4 records -- that no oneOf or
# anyOf sits above $defs/by_producing_arm, because that is the only reason the
# `dual_status` rename fails loudly -- and a constraint about the schema can only
# be shown to have force by breaking the schema.
SCHEMA_MUTATIONS = {
    # v1.9.0 -- A HALF-DONE VERSION BUMP, found by the coordinator on this build.
    # `SCHEMA_ID` was a literal with the version spelled out inside it, so one
    # version had two definitions and the v1.9.0 bump moved only one: the schema
    # shipped `schema_version.const = "1.9.0"` beside `schema_id.const` and `$id`
    # at `...:1.8.0`, and all three placeholders carried the same pair.
    #
    # NO CONTROL SAW IT, and that is the point of this fixture. An instance is
    # checked against each const SEPARATELY, so the placeholders agreed with the
    # schema on both fields; the two identifiers were internally consistent and
    # disagreed only with EACH OTHER. The subject is therefore the SCHEMA -- and
    # like S35's, breaking the instance could never show this check has force.
    #
    # THE MUTATION IS THE DEFECT ITSELF, RECONSTRUCTED: bump one identifier and
    # leave the other. The generator now derives the URN from the version, so
    # this state is unreachable from that side; this asserts the other side.
    "S42/version_bumped_in_one_identifier_only": (
        "S42",
        lambda s: s["properties"]["schema_version"].__setitem__("const", "9.9.9")),
    # And the mirror: the URN moved while the version const stayed. Both halves,
    # because a check that catches a bump in one direction only is half a check.
    "S42/urn_bumped_while_the_version_const_stayed": (
        "S42",
        lambda s: s.__setitem__("$id", s["$id"].rsplit(":", 1)[0] + ":9.9.9")),
    "S35/absence_branch_added_above_the_renamed_key": ("S35", lambda s: s["$defs"].__setitem__(
        "headline",
        {"oneOf": [dict(s["$defs"]["headline"]), {"$ref": "#/$defs/block_absence"}]})),
    # v1.4.0: THE FAMILY, NOT ONE MEMBER. decisions/0111 E1 gave five more blocks
    # the same container, and a constraint that guarded one of six would have had
    # five ways around it -- which is exactly the temptation the widening creates,
    # since an absence branch above one of the new containers is the obvious way
    # to express "this block is not this entry's".
    # v1.4.0: THE ROOT-SIDE SCAN, WHICH WAS DEAD CODE. It was handed a bare
    # PROPERTY MAP, and _scan recurses only into schema KEYWORDS, so it followed
    # nothing and returned at once. This mutation reaches a container through a
    # branch keyword on the ROOT side only -- inlined at a top-level property
    # rather than through $defs -- so it is caught by the fixed call and by
    # nothing else.
    "S35/branch_on_the_root_side_only": (
        "S35",
        lambda s: s["properties"].__setitem__(
            "arms",
            {"oneOf": [dict(s["properties"]["arms"]),
                       {"$ref": "#/$defs/by_producing_arm"}]})),
    "S35/absence_branch_added_above_a_new_family_member": (
        "S35",
        lambda s: s["$defs"]["arm_entry"]["properties"].__setitem__(
            "d3_prime",
            {"oneOf": [dict(s["$defs"]["arm_entry"]["properties"]["d3_prime"]),
                       {"$ref": "#/$defs/block_absence"}]})),
    # v1.5.0 -- decisions/0114 E12. A PER-ARM BLOCK ADDED TO THE SCHEMA WITH NO
    # ROW IN THE PUBLISHER TABLE. S22 iterates that table and S36 iterates that
    # table, so before v1.5.0 the new block fell through both in silence and
    # could be written into any step's entry in any file. Like S35, the subject
    # is the SCHEMA, so only a schema mutation can show the check has force.
    "S39/per_arm_block_with_no_publisher_row": (
        "S39",
        lambda s: s["$defs"]["arm_entry"]["properties"].__setitem__(
            "unpublished_block", {"type": "object"})),
    # And the other direction: a row for a block the schema no longer defines,
    # which reads as coverage and is none.
    "S39/publisher_row_for_a_block_that_does_not_exist": (
        "S39",
        lambda s: s["$defs"]["arm_entry"]["properties"].pop("waterfall")),
}

# The case the ruling names in as many words: an arm file that correctly OMITS
# $.cross_arm_divergences must not fail. Before v1.2.0 it did, and the only path
# to exit 0 was a cross-arm search an isolated arm cannot honestly have run.
ARM_REQUIRED_NON_FAILURES = {
    "S17/arm_file_omitting_it_passes": ("S17", lambda i: i),
    "S29/arm_file_omitting_it_passes": ("S29", lambda i: i),
    # decisions/0114 E13, THE RULING ITSELF, asserted as a NON-failure. Where the
    # schema's own text says NO PRODUCER EXISTS -- a premiere-anchored arm, at
    # which Step 8 builds no waterfall, Step 10 charts nothing and Step 13's grid
    # does not reach -- an absence record is LEGAL EVEN AT A PRIMARY ENTRY, and
    # S22 rejected it. Publisher rows key on ARM IDENTITY, not producing step
    # alone. The mirror case, silence in the same place, is asserted as a FAILURE
    # in ARM_MUTATIONS above.
    "S22/legal_absence_at_a_premiere_anchored_primary_entry": ("S22", lambda i: [
        i["arms"][k].__setitem__("is_primary_headline",
                                 i["arms"][k].get("clock_origin") == "s2_premiere")
        for k in range(len(i["arms"]))] and i),
}

# Cases that must NOT fail. F4 is the reason this section exists: a legitimately
# empty list, declared as empty with its coverage count, must be distinguishable
# from a list nobody searched -- and the way to prove the distinction is live is
# to assert that one of them passes while the other fails.
REQUIRED_NON_FAILURES = {
    # THE E2 WIDENING, ASSERTED AS A NON-FAILURE. Two steps' measurements at ONE
    # (W, clock origin) setting must both be able to exist: that is the whole of
    # decisions/0111 E2, and a key that called the second a duplicate would have
    # forced the schema to decide which step may occupy a shared W. The merged
    # baseline already holds several entries at the adopted setting, so this case
    # is the UNMUTATED file -- and main() asserts the count is greater than one,
    # because a non-failure on a file with nothing to collide would prove nothing.
    "S2/two_steps_at_one_setting_is_not_a_duplicate": ("S2", lambda i: i),
    "S17/empty_but_declared": ("S17", lambda i: _set(
        _set(i["cross_arm_divergences"], "entries", []),
        "search", dict(i["cross_arm_divergences"]["search"],
                       performed=True, coverage_count=17,
                       empty_reason="every compared figure agreed between the arms"))),
}

# Which mutations must be applied to the real-data copy rather than the placeholder,
# because the check they target is N/A on a placeholder.
REAL_ONLY = {"S12", "S13"}
# S5 and S6 are two-sided; the placeholder side is exercised above and the
# real-file side is exercised by leaving a sentinel in the real copy.
REAL_SIDE = {"S5": "sentinel_in_a_real_file", "S6": "prefix_in_a_real_file"}


def _set(node, key, value):
    node[key] = value
    return node


def _synthetic_step13_arm_file() -> dict:
    """A STEP 13 ARM FILE, built here rather than emitted as a fourth placeholder.

    THE RATIFICATION (decisions/0114 §4). Step 13 is dual (decisions/0103 §3) and
    writes one file per arm, so the ONE-ARM form of the six per-arm nested blocks
    is a legal shape of this schema -- and no emitted file illustrated it: the
    merged placeholder holds both arms, the Step 9 arm file holds none of the
    six, and the single-arm file's `sole` container is a different branch again.

    reviewer-engineering established the shape is REPRESENTABLE and POLICED, so
    what was missing was an EXAMPLE. It is built from the same generator the
    deliverables come from -- not hand-written -- so it cannot drift from them,
    and it is not written to artifacts/, so the deliverable count stays at three.
    """
    provenance = {
        "generator": "src/step8b_selftest.py, via src/step8b_schema.build_placeholder",
        "generator_sha256_12": "selftest0000",
        "generated_at_utc": "2026-01-01T00:00:00Z",
        "host_step": "Step 8b, output schema",
        "written_by": "Analytics Engineer, instance a -- selftest fixture, not a deliverable",
    }
    return G.build_placeholder(provenance, G._read_grid(), "arm_file", "a", "step13")


# ---------------------------------------------------------------------------
# The schema's statistic vocabulary, CHECKED AGAINST THE WRITERS' SPEC
# ---------------------------------------------------------------------------
#
# decisions/0118 puts the canonical wording of the bootstrap-statistic
# requirement in ONE place: the block between BOOTSTRAP-STATISTIC-BEGIN and
# BOOTSTRAP-STATISTIC-END in the two writer files, byte-identical in both.
# src/check_surfaces.py::scan_statistic_declaration() polices THE SPEC. Nothing
# policed the relation between that block and THIS SCHEMA -- the schema's enum
# tokens were typed here and agreed with the block by inspection.
#
# THIS IS NOT A CONST ASSERTING AGREEMENT. It reads the block off disk and
# compares. A const in the schema saying "the statistic is both" would be the
# shape this schema already retired once (`diff_precedes_merge`): not a fact the
# file records, a sentence the schema requires the file to contain. What is left
# open after this runs -- whether a writer's arithmetic actually produced both
# objects -- is published as a known limit rather than closed by decoration.
# IMPORTED, NOT RESTATED. src/check_surfaces.py holds THE definition of the writer
# file list, the markers, the extraction and the four required elements; this
# module had a second copy of the middle three and a third of the last.
WRITER_FILES = tuple(os.path.join(ROOT, f) for f in CS.STAT_WRITERS)


def _extract_block(path: str) -> tuple[str | None, str | None]:
    """The canonical block off disk, via check_surfaces.extract_block().

    THE RULE IS NOT RESTATED HERE. Marker arity, marker exactness, the search
    origin of the END marker and the minimum-length floor all live in the one
    implementation; this wrapper only supplies the bytes and prefixes the path to
    whatever that implementation says went wrong.
    """
    if not os.path.exists(path):
        return None, f"{path} does not exist"
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    block, err = CS.extract_block(text)
    return (None, f"{path}: {err}") if err else (block, None)


def _enum_tokens(node, want: str, out: set) -> set:
    """Every `enum` carried by a node tagged with this x-enum-id, anywhere."""
    if isinstance(node, dict):
        if node.get("x-enum-id") == want and isinstance(node.get("enum"), list):
            out |= set(node["enum"])
        for v in node.values():
            _enum_tokens(v, want, out)
    elif isinstance(node, list):
        for v in node:
            _enum_tokens(v, want, out)
    return out


_STAT_CLAUSE_LABEL = "statistic = BOTH levels and paired movements"


def _tokens_named_by_the_block(block: str) -> tuple[list[str], str | None]:
    """The statistic vocabulary the CANONICAL BLOCK names, derived from the block.

    The expectation used to be typed here as `["levels", "movements"]` -- a third
    copy of a rule that already had two (reviewer-engineering E5). It is now read
    off the block's own assertion, via the pattern check_surfaces.py holds: the
    clause `statistic = BOTH levels and paired movements` is split on " and " and
    the qualifier `paired` stripped, which is exactly how the enum tokens relate
    to the writers' words.

    A DERIVATION THAT YIELDS NOTHING MUST FAIL, NOT PASS: if the block is reworded
    the parse returns an error rather than an empty set, because an empty expected
    set would make every enum agree with it.
    """
    pat = CS.STAT_REQUIRED[_STAT_CLAUSE_LABEL][0]
    m = pat.search(CS.WS.sub(" ", block))
    if m is None:
        return [], ("the canonical block does not carry the statistic clause, so this schema's "
                    "enum has nothing to be checked against")
    tail = m.group(0).split("BOTH", 1)[1]
    toks = sorted({p.strip().removeprefix("paired ").strip() for p in tail.split(" and ")} - {""})
    if len(toks) != 2:
        return toks, (f"the statistic clause parsed to {toks!r}, which is not the two objects "
                      f"decisions/0118 fixes -- the block has been reworded and this derivation "
                      f"no longer reads it")
    return toks, None


# WHICH STEPS THE 2026-08-19 RULING EXEMPTS FROM S41'S EMPTY BRANCH -- WRITTEN
# FROM THE RULING, NOT READ FROM THE VALIDATOR. The exemption is Step 12's alone,
# on the schema's own warrant that Step 12 mandates intervals nowhere. Held here
# so that widening V.INTERVALS_NOT_MANDATED_BY_STEP FAILS this selftest instead of
# moving the expectation with the behaviour, which is what the first form of this
# fixture did.
# THE EXPECTED S41 STATUS PER PRODUCING STEP, PINNED EXACTLY (v1.8.0,
# reviewer-engineering E5). The fixture used to assert only
# `(status in ("FAIL", "VACUOUS")) == must_fail`, under which `step12` reporting
# PASS or N/A kept it green while the table decisions/0120 §1 publishes became
# false. The status IS the finding, so the status is what is asserted.
#
# ONE DEFINITION: the exempt set is derived from this table rather than typed
# beside it, and it is written FROM THE RULING -- Step 12 alone -- not read from
# V.INTERVALS_NOT_MANDATED_BY_STEP, which is the table under test.
S41_EMPTY_BRANCH_EXPECTED = {
    "step9": "FAIL",
    "step10": "FAIL",
    "step11": "FAIL",
    "step12": "EMPTY_DECLARED",
    "step13": "FAIL",
}
S41_EXEMPT_BY_RULING = {s for s, v in S41_EMPTY_BRANCH_EXPECTED.items()
                        if v == "EMPTY_DECLARED"}

# A FILE THAT PUBLISHES BOTH OBJECTS PASSES S41, FOR EVERY PRODUCING STEP.
# Written from the requirement, not from the behaviour: decisions/0118 fixes the
# statistic as BOTH, and S41 asks only that both appear per (producing step, arm).
# The exempt step is no exception in this direction either -- Step 12 MAY publish
# and, having published completely, passes like anyone else. Without this row the
# fixture asserted only the failing states, and a check that only ever fails is
# indistinguishable from one that always fails.
S41_PUBLISHES_BOTH_EXPECTED = {s: "PASS" for s in S41_EMPTY_BRANCH_EXPECTED}

# STEP 10'S INTERVAL OBLIGATION -- WRITTEN FROM THE HUMAN LEAD'S RULING OF
# 2026-08-20, NOT DERIVED FROM EITHER TABLE.
#
# THE RULING, RECORDED AS GIVEN: Step 10 measures outcome shares on the primary
# arm under a fixed bootstrap, which is a quantity with a real interval, so
# exempting it would assert that Step 10 mandates intervals nowhere -- FALSE --
# while the Step 12 exemption rests on that same clause being TRUE of Step 12.
# Step 10 therefore JOINS V.INTERVAL_CLASS_PUBLISHERS["outcome_shares"] and does
# NOT join V.INTERVALS_NOT_MANDATED_BY_STEP.
#
# THESE ARE PINS, NOT DERIVATIONS. The expectations below are typed from the
# ruling; the validator's tables are then read and compared against them, so
# removing `step10` from the publisher table or adding it to the exemption table
# FAILS this selftest instead of moving the expectation along with the behaviour.
# That is decisions/0111 E4 -- a table read from the file under test could only
# agree with itself -- and this build has reinstalled it twice.
STEP10_BY_THE_RULING = {
    "publishes_outcome_shares": True,
    "exempt_from_intervals": False,
    "omits_intervals": "FAIL",
    "publishes_both_objects": "PASS",
    "publishes_levels_only": "FAIL",
}

_NO_INTERVAL_ABSENCE = {
    "status": "not_required_by_spec",
    "reason": "SELFTEST FIXTURE: this writing step is not asked for an interval at this slot.",
    "source": "src/step8b_selftest.py, the S41 scope fixture",
}


def _relabel_producing_step(inst: dict, step: str) -> dict:
    """Make every measurement in `inst` this step's, in place.

    `produced_by_step` and `written_by_step` JOINED THIS AT v1.8.0
    (reviewer-engineering E3): S41 now keys on (producing step, arm), and a
    fixture that relabelled only the entry-level `producing_step` would leave its
    intervals attributed to whatever step the placeholder was built for -- so the
    fixture would exercise a step it did not name.
    """
    inst["document_scope"]["producing_step"] = step
    for fam in ("arms", "variants", "subpopulation_cuts"):
        for e in inst.get(fam) or []:
            if "producing_step" in e:
                e["producing_step"] = step
    for _, bpa in V._iter_containers(inst):
        if "producing_step" in bpa:
            bpa["producing_step"] = step
        for payload in (bpa.get("arms") or {}).values():
            if isinstance(payload, dict) and "producing_step" in payload:
                payload["producing_step"] = step

    def walk(node):
        if isinstance(node, dict):
            for key in ("written_by_step", "produced_by_step"):
                if key in node:
                    node[key] = step
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(inst)
    return inst


def _file_with_no_intervals(base: dict, step: str, record_absences: bool = True) -> dict:
    """An arm file of `step` that carries no interval.

    Built from the single-arm placeholder rather than typed, so the fixture is
    the shipped shape with one thing changed. Every `ci` holding a bootstrap_ref
    becomes an absence record and $.declared_intervals empties, which is exactly
    the state S41's empty branch judges.

    `record_absences=False` IS THE ZERO-COVERAGE SHAPE (v1.8.0,
    reviewer-engineering E5): the `ci` slots are removed rather than filled with
    an absence, so the file says nothing about where its intervals would have
    been. That is the state that used to be awarded EMPTY_DECLARED with a reason
    asserting "the emptiness was searched for rather than assumed" over a search
    that examined nothing -- and it must now be VACUOUS FOR EVERY STEP, THE
    EXEMPT ONE INCLUDED, because the exemption excuses the intervals and not the
    coverage.
    """
    inst = copy.deepcopy(base)

    def walk(node):
        if isinstance(node, dict):
            for k, v in list(node.items()):
                if k == "ci" and isinstance(v, dict) and "bootstrap_ref" in v:
                    if record_absences:
                        node[k] = dict(_NO_INTERVAL_ABSENCE)
                    else:
                        del node[k]
                else:
                    walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(inst)
    inst["declared_intervals"] = []
    return _relabel_producing_step(inst, step)


def _file_with_levels_only(base: dict, step: str) -> dict:
    """An arm file of `step` that PUBLISHES intervals and only ever labels them
    `levels`.

    THE BRANCH NO FIXTURE REACHED (v1.8.0, reviewer-engineering E2). The
    exemption used to gate this branch as well as the empty one, so a Step 12
    file emitting forty levels-only intervals collected a "RESTRICTED, NOT FULL"
    note and PASSED with sites > 0 and zero failures -- and nothing in either
    direction exercised it. The ruling's ground is that requiring intervals would
    make Step 12 MANUFACTURE two figures; a file that has already computed them
    is manufacturing nothing, so decisions/0118's "a run that emits only one is
    INCOMPLETE" reaches it directly and it must FAIL FOR EVERY STEP.
    """
    inst = copy.deepcopy(base)

    def walk(node):
        if isinstance(node, dict):
            if "bootstrap_ref" in node and "statistic" in node:
                node["statistic"] = "levels"
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(inst)
    return _relabel_producing_step(inst, step)


def _file_publishing_both_objects(base: dict, step: str) -> dict:
    """An arm file of `step` that publishes intervals and labels both objects.

    THE PASSING SIDE (v1.9.0, Human Lead ruling 2026-08-20). Every S41 fixture
    before this one drove the check to a FAILING state, so nothing established
    that a step CAN satisfy it -- and the ruling that put Step 10 under the
    requirement is owed a demonstration that Step 10 can discharge it, not only
    that it can breach it. The single-arm placeholder already carries both
    objects, so this is the shipped shape with one thing changed: whose it is.
    """
    return _relabel_producing_step(copy.deepcopy(base), step)


def _one_steps_intervals_levels_only(base: dict, step: str) -> dict:
    """The MERGED document with ONE step's intervals relabelled `levels`.

    THE FIXTURE THAT DISCRIMINATES THE OWNER KEY (v1.9.0, reviewer-engineering
    F2). Nothing committed distinguished keying S41 on (producing step, arm) from
    keying it on the arm: MUTATIONS["S41"] strips movements from EVERY owner, so
    it fails identically under both, and reverting the owner key -- undoing E3
    entirely -- left this selftest at exit 0. The discriminating shape existed and
    was measured, but it lived in a run record under logs/, which never leaves
    this machine. A check nobody can see is not a check (CLAUDE.md,
    decisions/0082).

    THE SHAPE, AND WHY IT DISCRIMINATES: in the merged document one arm label
    covers several producing steps -- `a` is Step 9 AND Step 13 -- so stripping
    the movements from Step 13 alone leaves arm `a` still carrying Step 9's
    movement. Aggregated by ARM the file reads complete; aggregated by (STEP,
    ARM) Step 13 has published twelve levels and no movement. The fixture asserts
    BOTH halves, so it fails if the file stops being discriminating as well as if
    the check stops discriminating.
    """
    inst = copy.deepcopy(base)
    targets = [ci for _p, istep, _a, ci in V._iter_cis_with_arm(inst)
               if istep == step and "statistic" in ci]
    if not targets:
        raise AssertionError(f"no interval is attributed to {step!r} in this fixture")
    for ci in targets:
        ci["statistic"] = "levels"
    return inst


def _statistic_vocabulary_link(schema: dict) -> dict:
    """Tie this schema's statistic vocabulary to the writers' canonical block.

    THE RULE ITSELF IS check_surfaces.stat_verdict(). This function supplies the
    two files' bytes to it and adds the one thing that control cannot see: whether
    THIS SCHEMA's enum is the vocabulary the block names.
    """
    failures = []
    blocks = {}
    for path in WRITER_FILES:
        block, why = _extract_block(path)
        if block is None:
            failures.append(why)
        else:
            blocks[path] = block

    # Byte-identity, the four elements by value and the forbidden reversals: ONE
    # implementation, called with the file contents rather than restated.
    texts = []
    for path in WRITER_FILES:
        try:
            with open(path, encoding="utf-8") as fh:
                texts.append(fh.read())
        except OSError:
            texts.append("")
    verdict, chars = CS.stat_verdict(*texts) if len(texts) == 2 else (["fewer than two writer "
                                                                      "files"], 0)
    failures.extend(verdict)
    identical = None
    if len(blocks) == len(WRITER_FILES):
        values = list(blocks.values())
        identical = values[0] == values[1]

    tokens = sorted(_enum_tokens(schema, "bootstrap_statistic", set()))
    expected: list[str] = []
    if blocks:
        block = next(iter(blocks.values()))
        expected, why = _tokens_named_by_the_block(block)
        if why:
            failures.append(why)
        elif tokens != expected:
            failures.append(
                f"this schema's bootstrap_statistic enum is {tokens!r}, but the canonical block "
                f"names {expected!r}: the schema's vocabulary and the writers' requirement have "
                f"drifted"
            )
    return {
        "what": "the schema's statistic vocabulary, compared against the canonical block in "
                "the two writer files (decisions/0118). The extraction, the byte-identity rule "
                "and the four required elements are IMPORTED from src/check_surfaces.py; "
                "nothing here restates them",
        "files_read": len(blocks),
        "files_expected": len(WRITER_FILES),
        "characters_compared": chars,
        "byte_identical": identical,
        "elements_asserted_by_value": sorted(CS.STAT_REQUIRED),
        "schema_enum_tokens": tokens,
        "tokens_derived_from_the_block": expected,
        "failures": failures,
        # A MISSING BLOCK IS A FAILURE, NOT A SKIP: coverage is asserted, so this
        # cannot report clean over zero characters.
        "ok": not failures and chars > 0 and len(blocks) == len(WRITER_FILES),
    }


def _status_of(report: dict, cid: str) -> str:
    for c in report["semantic_checks"]:
        if c["id"] == cid:
            return c["status"]
    return "MISSING"


def main() -> int:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(SCHEMA_PATH) as fh:
        schema = json.load(fh)
    with open(PLACEHOLDER_PATH) as fh:
        placeholder = json.load(fh)
    with open(ARM_PLACEHOLDER_PATH) as fh:
        arm_file = json.load(fh)
    with open(SOLE_PLACEHOLDER_PATH) as fh:
        sole_file = json.load(fh)

    real = _make_real(placeholder)

    def run(inst: dict, use_schema: dict | None = None) -> dict:
        ev = V.SchemaEvaluator(use_schema or schema)
        ev.validate(inst, use_schema or schema)
        checks = V.run_semantic_checks(inst, ev)
        return {
            "semantic_checks": [c.as_dict() for c in checks],
            "schema_errors": len(ev.errors),
        }

    baseline_ph = run(placeholder)
    baseline_real = run(real)
    baseline_arm = run(arm_file)
    baseline_sole = run(sole_file)

    # THE RATIFIED FOURTH SHAPE, EXERCISED HERE AND NOT EMITTED (decisions/0114
    # §4). A Step 13 arm file: dual step, one arm, which is the only shape in
    # which the six per-arm nested blocks appear in their ONE-ARM form.
    step13_arm = _synthetic_step13_arm_file()
    baseline_step13 = run(step13_arm)
    one_arm_form = {}
    containers = {}
    for path, bpa in V._iter_containers(step13_arm):
        containers[path] = bpa
    for block in PER_ARM_NESTED_BLOCKS:
        found = [(p, b) for p, b in containers.items() if f".{block}." in p + "."]
        one_arm_form[block] = {
            "containers_found": len(found),
            "all_one_arm": all(b.get("arms_in_this_file") == "one_arm" for _, b in found),
            "arms_held": sorted({b.get("arm_held") for _, b in found}),
            "arm_keys": sorted({k for _, b in found for k in (b.get("arms") or {})}),
            "producing_steps": sorted({b.get("producing_step") for _, b in found}),
        }
    step13_record = {
        "what": "a STEP 13 ARM FILE -- dual step, one arm -- built from the generator inside "
                "this selftest rather than emitted as a fourth placeholder (decisions/0114 §4)",
        "schema_errors": baseline_step13["schema_errors"],
        "statuses": {c["id"]: c["status"] for c in baseline_step13["semantic_checks"]},
        "failures": [c["id"] for c in baseline_step13["semantic_checks"]
                     if c["status"] in ("FAIL", "VACUOUS")],
        "one_arm_form_of_the_six_blocks": one_arm_form,
    }
    step13_ok = (
        baseline_step13["schema_errors"] == 0
        and not step13_record["failures"]
        and all(v["containers_found"] > 0 and v["all_one_arm"]
                and v["arm_keys"] == ["a"] and v["producing_steps"] == ["step13"]
                for v in one_arm_form.values())
    )
    step13_record["ok"] = step13_ok

    # THE STEP 12 INTERVAL EXEMPTION, AND THAT IT DOES NOT WIDEN. Human Lead
    # ruling, 2026-08-19. S41's empty branch failed unconditionally, so a Step 12
    # arm file failed for not carrying intervals the spec never asks it for -- the
    # schema's own warrant says "Step 12 lists every candidate cut and mandates
    # intervals nowhere", and requiring them would make the writing step
    # manufacture two figures, one a paired movement between configurations the
    # spec does not name.
    #
    # AN EXEMPTION THAT QUIETLY COVERS FIVE STEPS WHEN IT WAS GRANTED TO ONE IS
    # THE SHAPE THIS STUDY KEEPS FINDING, so the four steps that must STILL fail
    # are asserted here beside the one that must pass. This is the demonstration,
    # committed rather than reported: a check nobody can see is not a check
    # (CLAUDE.md, decisions/0082).
    #
    # THE EXPECTATION IS HELD HERE, NOT READ FROM THE TABLE UNDER TEST. Written
    # from the ruling: Step 12 alone. Deriving it from
    # V.INTERVALS_NOT_MANDATED_BY_STEP was the first form of this fixture and it
    # was a NO-OP -- adding `step9` to that table moved the expectation with the
    # behaviour and the selftest still reported ok, which is decisions/0111 E4's
    # "a table read from the file under test could only agree with itself",
    # reached through code rather than through a file. Found by probing the
    # control live rather than by reading it.
    #
    # THREE SHAPES SINCE v1.8.0, NOT ONE (reviewer-engineering E2 and E5). The
    # empty branch was the only one any fixture reached, so the exemption's SECOND
    # site -- the per-owner missing-object branch -- was exercised in neither
    # direction, and a zero-coverage emptiness was awarded EMPTY_DECLARED with
    # nothing asserting otherwise. The statuses are PINNED rather than bucketed:
    # `(status in ("FAIL", "VACUOUS")) == must_fail` kept the fixture green while
    # a PASS or an N/A would have made the published table false.
    s41_scope = {}
    for step in sorted(S41_EMPTY_BRANCH_EXPECTED):
        want = S41_EMPTY_BRANCH_EXPECTED[step]
        declared = _status_of(run(_file_with_no_intervals(sole_file, step)), "S41")
        # THE SAME FILE WITH NO ABSENCE RECORDS: nothing was examined, so no step
        # may reach a passing state, exempt or not. The two failing states are
        # DIFFERENT and both are pinned: an exempt step falls through to VACUOUS,
        # having nothing to declare its emptiness with, while a non-exempt step
        # collects the check's own explicit failure and reports FAIL.
        want_unsearched = "VACUOUS" if step in S41_EXEMPT_BY_RULING else "FAIL"
        unsearched = _status_of(
            run(_file_with_no_intervals(sole_file, step, record_absences=False)), "S41")
        # A FILE THAT PUBLISHED INTERVALS AND LABELLED THEM ALL `levels`: the
        # exemption does not reach this, for any step.
        levels_only = _status_of(run(_file_with_levels_only(sole_file, step)), "S41")
        # THE PASSING SIDE (v1.9.0). A file that published both objects must PASS,
        # for every step. Every other shape here drives S41 to a failing state, so
        # without this row the fixture could not tell a check that discriminates
        # from one that always fails.
        want_both = S41_PUBLISHES_BOTH_EXPECTED[step]
        both = _status_of(run(_file_publishing_both_objects(sole_file, step)), "S41")
        s41_scope[step] = {
            "no_intervals_absences_recorded": {"expected": want, "got": declared,
                                               "ok": declared == want},
            "no_intervals_zero_coverage": {"expected": want_unsearched, "got": unsearched,
                                           "ok": unsearched == want_unsearched},
            "levels_only_intervals": {"expected": "FAIL", "got": levels_only,
                                      "ok": levels_only == "FAIL"},
            "publishes_both_objects": {"expected": want_both, "got": both,
                                       "ok": both == want_both},
            "exempt_by_the_ruling": step in S41_EXEMPT_BY_RULING,
        }
        s41_scope[step]["ok"] = all(
            s41_scope[step][k]["ok"] for k in
            ("no_intervals_absences_recorded", "no_intervals_zero_coverage",
             "levels_only_intervals", "publishes_both_objects"))
    s41_record = {
        "what": "S41 per producing step, on FOUR fixtures: a file whose every interval is an "
                "explicit absence record, the same file with the slots simply gone, a file "
                "that published intervals and labelled every one of them `levels`, and a file "
                "that published both objects. Step 12 is exempt from CARRYING intervals; it is "
                "exempt from neither of the failing states, and an exemption that widens is "
                "the defect. The fourth fixture is the passing side: without it every shape "
                "here drives S41 to a failing state",
        "expected_statuses": dict(S41_EMPTY_BRANCH_EXPECTED),
        "exempt_by_the_ruling": sorted(S41_EXEMPT_BY_RULING),
        "exempt_in_the_validator": sorted(V.INTERVALS_NOT_MANDATED_BY_STEP),
        "tables_agree": set(V.INTERVALS_NOT_MANDATED_BY_STEP) == S41_EXEMPT_BY_RULING,
        "by_step": s41_scope,
        "statuses": {s: v["no_intervals_absences_recorded"]["got"]
                     for s, v in s41_scope.items()},
        "zero_coverage_statuses": {s: v["no_intervals_zero_coverage"]["got"]
                                   for s, v in s41_scope.items()},
        "levels_only_statuses": {s: v["levels_only_intervals"]["got"]
                                 for s, v in s41_scope.items()},
        "publishes_both_objects_statuses": {s: v["publishes_both_objects"]["got"]
                                            for s, v in s41_scope.items()},
        "ok": (all(v["ok"] for v in s41_scope.values()) and len(s41_scope) == 5
               and set(V.INTERVALS_NOT_MANDATED_BY_STEP) == S41_EXEMPT_BY_RULING),
    }

    # STEP 10'S INTERVAL OBLIGATION, DEMONSTRATED IN BOTH DIRECTIONS (Human Lead
    # ruling, 2026-08-20). The ruling puts Step 10 under the both-objects
    # requirement and into the outcome-shares publisher table, on the ground that
    # it measures outcome shares on the primary arm under a fixed bootstrap. A
    # ruling that only ever made a file FAIL would be half-demonstrated, so both
    # sides are asserted: Step 10 omitting intervals FAILS, Step 10 publishing
    # both objects PASSES.
    #
    # THE EXPECTATIONS ARE TYPED FROM THE RULING, ABOVE, AND THE TABLES ARE READ
    # AND COMPARED AGAINST THEM. Deriving them from V.INTERVAL_CLASS_PUBLISHERS
    # or V.INTERVALS_NOT_MANDATED_BY_STEP would make the fixture agree with
    # whatever those tables say -- decisions/0111 E4, which this build has
    # reinstalled twice and which a third time would be inexcusable.
    step10_record = {
        "what": "Step 10's interval obligation under the Human Lead ruling of 2026-08-20, "
                "with the expectations written FROM the ruling and the validator's two tables "
                "read and compared against them. Both directions: a Step 10 file that omits "
                "intervals must FAIL, and one that publishes both objects must PASS",
        "ruling": dict(STEP10_BY_THE_RULING),
        "publisher_table_outcome_shares": list(
            V.INTERVAL_CLASS_PUBLISHERS.get("outcome_shares", ())),
        "publisher_table_window_w_percentile": list(
            V.INTERVAL_CLASS_PUBLISHERS.get("window_w_percentile", ())),
        "exempt_in_the_validator": sorted(V.INTERVALS_NOT_MANDATED_BY_STEP),
        "publishes_outcome_shares":
            "step10" in V.INTERVAL_CLASS_PUBLISHERS.get("outcome_shares", ()),
        "exempt_from_intervals": "step10" in V.INTERVALS_NOT_MANDATED_BY_STEP,
        # NOT A SECOND READING OF THE RULING -- REPORTED, NOT ASSERTED. The ruling
        # names the OUTCOME SHARES; whether it reaches the window-W percentile is
        # the arm's assessment, reported to the Human Lead, and Step 10 is left
        # out of that class because it does not vary W. Recorded here so the
        # asymmetry is visible rather than inferred from a table.
        "window_w_percentile_membership_is_reported_not_ruled": {
            "step10_in_window_w_percentile":
                "step10" in V.INTERVAL_CLASS_PUBLISHERS.get("window_w_percentile", ()),
            "why": "the ruling's ground is the outcome shares; W is derived at Step 6 and "
                   "reported at Step 9's window arms and across Step 13's grid, and Step 10 "
                   "charts the headline arm without varying W. Reported to the Human Lead, "
                   "not decided here",
        },
        "omits_intervals": s41_scope["step10"]["no_intervals_absences_recorded"]["got"],
        "publishes_both_objects": s41_scope["step10"]["publishes_both_objects"]["got"],
        "publishes_levels_only": s41_scope["step10"]["levels_only_intervals"]["got"],
    }
    step10_record["ok"] = (
        step10_record["publishes_outcome_shares"]
        == STEP10_BY_THE_RULING["publishes_outcome_shares"]
        and step10_record["exempt_from_intervals"]
        == STEP10_BY_THE_RULING["exempt_from_intervals"]
        and step10_record["omits_intervals"] == STEP10_BY_THE_RULING["omits_intervals"]
        and step10_record["publishes_both_objects"]
        == STEP10_BY_THE_RULING["publishes_both_objects"]
        and step10_record["publishes_levels_only"]
        == STEP10_BY_THE_RULING["publishes_levels_only"]
    )

    # THE OWNER KEY IS (PRODUCING STEP, ARM) (v1.8.0, reviewer-engineering E3).
    # In the merged document `sole` is Steps 10, 11 and 12 together and `a` is
    # Step 9 AND Step 13, so keying on the arm let one step's movement discharge
    # another step's obligation. The assertion is on the MERGED placeholder, the
    # only shape in which the two keyings differ at all: every owner that carries
    # an interval carries both objects, and at least two distinct steps share one
    # arm label -- without which this fixture would pass on a file where the
    # distinction cannot arise.
    owners: dict = {}
    for _p, istep, arm, ci in V._iter_cis_with_arm(placeholder):
        owners.setdefault((istep, arm), set()).add(ci.get("statistic"))
    arms_with_two_steps = sorted(
        {a for a in {o[1] for o in owners}
         if len({o[0] for o in owners if o[1] == a}) > 1})
    s41_owner_record = {
        "what": "S41's owner key on the merged placeholder: one entry per (producing step, "
                "arm), each carrying both objects. Keying on the arm alone would collapse "
                "these rows and let one step's paired movement stand in for another's",
        "owners": {f"{s}/{a}": sorted(v) for (s, a), v in
                   sorted(owners.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1])))},
        "owner_count": len(owners),
        "arm_labels": sorted({str(o[1]) for o in owners}),
        "arm_labels_covering_more_than_one_step": arms_with_two_steps,
        "every_owner_carries_both_objects": all(
            v == {"levels", "movements"} for v in owners.values()),
        "ok": (len(owners) > len({o[1] for o in owners})
               and bool(arms_with_two_steps)
               and all(v == {"levels", "movements"} for v in owners.values())),
    }

    # THE OWNER KEY, DISCRIMINATED (v1.9.0, reviewer-engineering F2). The record
    # above measures the owners and asserts that each carries both objects; it
    # does NOT distinguish the two keyings, because it builds its own owner map
    # and never runs S41 on a file where the keyings disagree. Reverting
    # `by_owner.setdefault((istep, arm), ...)` to `(None, arm)` -- undoing E3 --
    # left the whole selftest at exit 0.
    #
    # This is the file where they disagree: Step 13's intervals relabelled
    # `levels`, Step 9's left alone. Under the arm key, arm `a` carries Step 9's
    # movement and reads complete; under the (step, arm) key, Step 13 published
    # twelve levels and no movement and FAILS. BOTH HALVES ARE ASSERTED -- that
    # the file is discriminating (every ARM still carries both objects) and that
    # S41 fails it anyway -- so this cannot pass by the fixture quietly ceasing to
    # discriminate.
    keyed = _one_steps_intervals_levels_only(placeholder, "step13")
    by_arm: dict = {}
    for _p, _istep, arm, ci in V._iter_cis_with_arm(keyed):
        by_arm.setdefault(arm, set()).add(ci.get("statistic"))
    by_step_arm: dict = {}
    for _p, istep, arm, ci in V._iter_cis_with_arm(keyed):
        by_step_arm.setdefault((istep, arm), set()).add(ci.get("statistic"))
    arm_keyed_would_pass = all(v == {"levels", "movements"} for v in by_arm.values())
    step_arm_keyed_sees_a_gap = any(v != {"levels", "movements"}
                                    for v in by_step_arm.values())
    s41_keying_record = {
        "what": "the fixture on which the two candidate owner keys DISAGREE: one step's "
                "intervals relabelled `levels` inside the merged document, where one arm "
                "label covers several producing steps. Keying on the arm alone cannot see it; "
                "keying on (producing step, arm) fails it",
        "step_relabelled_levels_only": "step13",
        "aggregated_by_arm": {str(a): sorted(v) for a, v in sorted(by_arm.items(), key=str)},
        "aggregated_by_step_and_arm": {f"{k[0]}/{k[1]}": sorted(v) for k, v in
                                       sorted(by_step_arm.items(), key=str)},
        "every_arm_still_carries_both_objects": arm_keyed_would_pass,
        "some_step_arm_owner_carries_one": step_arm_keyed_sees_a_gap,
        "expected_s41_status": "FAIL",
        "s41_status": _status_of(run(keyed), "S41"),
        "note": "the arm-keyed aggregation is computed here to establish that the fixture is "
                "DISCRIMINATING, not to re-implement the check: it is what an arm-keyed S41 "
                "would have seen, and it carries both objects for every arm",
    }
    s41_keying_record["ok"] = (
        s41_keying_record["s41_status"] == "FAIL"
        and arm_keyed_would_pass
        and step_arm_keyed_sees_a_gap
    )

    # A MALFORMED FILE IS REPORTED ON, NOT CRASHED ON (v1.9.0,
    # reviewer-engineering F1). `_iter_payloads` walked the headline unguarded
    # while the other two iterators guarded theirs, so three shapes raised an
    # AttributeError out of validate_file() -- and the schema errors are computed
    # on the line above the semantic checks, so real structural findings were
    # computed and thrown away with the report. Each shape must now come back as a
    # REPORT that fails on the schema.
    # THROUGH THE REAL ENTRY POINT, on a temporary file: V.validate_file() is
    # where the traceback replaced the report, and the shorter run() helper above
    # would exercise the same walk without exercising the entry point that has to
    # survive it.
    malformed = {}
    for label, mutate in MALFORMED_HEADLINES.items():
        broken = copy.deepcopy(placeholder)
        fh = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        try:
            mutate(broken)
            json.dump(broken, fh)
            fh.close()
            rep = V.validate_file(fh.name, SCHEMA_PATH)
            malformed[label] = {
                "raised": None,
                "schema_errors": rep["schema_validation"]["error_count"],
                "schema_passed": rep["schema_validation"]["passed"],
                "semantic_checks_run": rep["checks_total"],
            }
        except Exception as exc:  # noqa: BLE001 -- the finding IS the exception
            malformed[label] = {"raised": f"{type(exc).__name__}: {exc}"}
        finally:
            fh.close()
            os.unlink(fh.name)
        malformed[label]["ok"] = (
            malformed[label].get("raised") is None
            and (malformed[label].get("schema_errors") or 0) > 0
            and malformed[label].get("schema_passed") is False
            and (malformed[label].get("semantic_checks_run") or 0) > 0
        )
    malformed_record = {
        "what": "three malformed headline shapes, run through validate_file() -- the real "
                "entry point, on a temporary file. Each must return a REPORT naming schema "
                "errors, not raise: the structural errors are computed on the line above the "
                "semantic checks, so a traceback throws away findings already made",
        "shapes": malformed,
        "ok": bool(malformed) and all(v["ok"] for v in malformed.values()),
    }

    # THE PARTITION UNIVERSE IS ANCHORED OUTSIDE THE FILE (v1.8.0,
    # reviewer-engineering E4), and the anchor has two copies by design: the
    # validator's, written from decisions/0103 and decisions/0118, decides; the
    # generator's is what gets written into a file. They are asserted equal HERE
    # so that widening one alone fails rather than passing quietly -- the same
    # shape as `tables_agree` above, and the reason S31 gives for not deriving an
    # expectation from the table under test.
    anchor_record = {
        "what": "the four bootstrap elements the spec fixes, compared between the validator's "
                "anchor and the generator's emitted list",
        "validator_anchor": sorted(V.BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC),
        "generator_list": sorted(G.BOOTSTRAP_FIELDS_CONSIDERED),
        "ok": (set(V.BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC)
               == set(G.BOOTSTRAP_FIELDS_CONSIDERED)
               and len(V.BOOTSTRAP_ELEMENTS_FIXED_BY_SPEC) == 4),
    }

    # ONE REGISTRY FACT, ONE RENDERING (v1.8.0, reviewer-engineering E7). It had
    # three: this module's docstring, the generator's schema description and a
    # placeholder note, and two of them disagreed about whether `resampling_unit`
    # is an arm difference. THE DISK IS THE ARBITER and it is read here rather
    # than quoted: entries of the same quantity class must differ from each other
    # in `producing_arm` alone, and the unit must vary between classes and not
    # between arms.
    #
    # TWO DEFECTS IN THIS FIXTURE, FIXED AT v1.9.0 (reviewer-engineering F5).
    #
    # (a) IT COMPARED FOUR FIELDS AND CLAIMED TO COMPARE ALL OF THEM. The tuple
    # was ("B", "seed", "resampling_unit", "statistics"), so a differing
    # `spec_status` -- or `fields_fixed_in_spec`, or any field added later --
    # reported `[]` and `ok: true` under a `what` that said it measured which
    # fields ACTUALLY differ. Reproduced: setting `b_default.spec_status` to
    # `partly_fixed_in_spec` left the record clean. The comparison is now over the
    # UNION of the keys the entries carry, minus an EXCLUSION LIST DECLARED WITH
    # ITS REASON -- a new field joins the comparison by existing, which is the
    # only version of this check that stays true as the registry grows.
    #
    # (b) `ok` NEVER REQUIRED A COMPARISON TO HAVE HAPPENED. On a registry with
    # one entry per class the loops run zero comparisons and every clause holds
    # vacuously -- reproduced by deleting the `b_` and `sole_` entries, which left
    # `ok: true`. That is the H3 shape decisions/0120 §3 names: an assertion that
    # cannot fail. The comparison count is now computed, reported and required to
    # be non-zero.
    #
    # AND THE EXPECTED ANSWER CHANGES WITH THE WIDENING: entries of one class
    # differ in `producing_arm` and in nothing else, so the differing set is
    # {"producing_arm"} rather than empty. That IS the fact
    # V.REGISTRY_ARM_DIFFERENCE_FACT states; the old empty answer only looked like
    # agreement because the field the fact is about was outside the comparison.
    reg = placeholder.get("bootstrap_settings") or {}
    by_class: dict = {}
    for key, entry in reg.items():
        by_class.setdefault(key.split("_", 1)[1], {})[key] = entry
    compared_fields = sorted(
        {f for cls in by_class.values() for e in cls.values() for f in e}
        - set(REGISTRY_FIELDS_EXCLUDED_FROM_THE_COMPARISON))
    classes_with_two_or_more = sorted(c for c, e in by_class.items() if len(e) > 1)
    comparisons = sum(len(cls) for c, cls in by_class.items()
                      if len(cls) > 1) * len(compared_fields)
    differing_within_class = sorted({
        f for cls in by_class.values() if len(cls) > 1 for f in compared_fields
        if len({json.dumps(e.get(f), sort_keys=True) for e in cls.values()}) > 1})
    units_by_class = {cls: sorted({e.get("resampling_unit") for e in entries.values()})
                      for cls, entries in by_class.items()}
    registry_fact_record = {
        "what": "the registry fact, measured on the merged placeholder rather than restated: "
                "which fields actually differ between the entries of one quantity class. The "
                "comparison is over the UNION of the keys the entries carry, less a declared "
                "exclusion list, so a field added to the registry joins it by existing",
        "classes": {c: sorted(e) for c, e in by_class.items()},
        "fields_compared": compared_fields,
        "fields_excluded_from_the_comparison":
            dict(REGISTRY_FIELDS_EXCLUDED_FROM_THE_COMPARISON),
        "classes_with_two_or_more_entries": classes_with_two_or_more,
        "field_comparisons_made": comparisons,
        "fields_differing_between_arms_within_a_class": differing_within_class,
        "expected_fields_differing": sorted(REGISTRY_FIELDS_THAT_MAY_DIFFER_WITHIN_A_CLASS),
        "resampling_unit_by_class": units_by_class,
        "the_one_rendering": V.REGISTRY_ARM_DIFFERENCE_FACT,
        "ok": (set(differing_within_class)
               == REGISTRY_FIELDS_THAT_MAY_DIFFER_WITHIN_A_CLASS
               and len(by_class) > 1
               and len(classes_with_two_or_more) > 1
               and comparisons > 0
               and len({tuple(u) for u in units_by_class.values()}) > 1),
    }

    results = []
    for cid, mutate in MUTATIONS.items():
        base_name = "real" if cid in REAL_ONLY else "placeholder"
        base = real if cid in REAL_ONLY else placeholder
        before = _status_of(baseline_real if cid in REAL_ONLY else baseline_ph, cid)
        mutated = copy.deepcopy(base)
        try:
            mutate(mutated)
        except Exception as exc:  # a mutation that cannot be applied is itself a finding
            results.append({"check": cid, "applied_to": base_name, "error": str(exc),
                            "has_force": False})
            continue
        after = _status_of(run(mutated), cid)
        results.append({
            "check": cid,
            "applied_to": base_name,
            "status_before": before,
            "status_after": after,
            "has_force": before == "PASS" and after in ("FAIL", "VACUOUS"),
        })

    # Second clauses of checks whose first clause is already exercised.
    for label, (cid, base_name, mutate) in EXTRA_MUTATIONS.items():
        base = real if base_name == "real" else placeholder
        before = _status_of(baseline_real if base_name == "real" else baseline_ph, cid)
        mutated = copy.deepcopy(base)
        try:
            mutate(mutated)
        except Exception as exc:
            results.append({"check": label, "applied_to": base_name, "error": str(exc),
                            "has_force": False})
            continue
        after = _status_of(run(mutated), cid)
        results.append({
            "check": label,
            "applied_to": base_name,
            "status_before": before,
            "status_after": after,
            "has_force": after in ("FAIL", "VACUOUS"),
        })

    # The arm-file cases (decisions/0107).
    for label, (cid, mutate) in ARM_MUTATIONS.items():
        before = _status_of(baseline_arm, cid)
        mutated = copy.deepcopy(arm_file)
        try:
            mutate(mutated)
        except Exception as exc:
            results.append({"check": label, "applied_to": "arm_file", "error": str(exc),
                            "has_force": False})
            continue
        after = _status_of(run(mutated), cid)
        results.append({
            "check": label,
            "applied_to": "arm_file",
            "status_before": before,
            "status_after": after,
            "has_force": after in ("FAIL", "VACUOUS"),
        })

    # The single-arm file's cases (decisions/0111 §3, Q1).
    for label, (cid, mutate) in SOLE_MUTATIONS.items():
        before = _status_of(baseline_sole, cid)
        mutated = copy.deepcopy(sole_file)
        try:
            mutate(mutated)
        except Exception as exc:
            results.append({"check": label, "applied_to": "sole_file", "error": str(exc),
                            "has_force": False})
            continue
        after = _status_of(run(mutated), cid)
        results.append({
            "check": label,
            "applied_to": "sole_file",
            "status_before": before,
            "status_after": after,
            "has_force": after in ("FAIL", "VACUOUS"),
        })

    # Schema-level cases (S35). The constraint is about the SCHEMA, so breaking
    # the instance could never show it has force.
    for label, (cid, mutate) in SCHEMA_MUTATIONS.items():
        before = _status_of(baseline_ph, cid)
        mutated_schema = copy.deepcopy(schema)
        try:
            mutate(mutated_schema)
        except Exception as exc:
            results.append({"check": label, "applied_to": "schema", "error": str(exc),
                            "has_force": False})
            continue
        after = _status_of(run(placeholder, mutated_schema), cid)
        results.append({
            "check": label,
            "applied_to": "schema",
            "status_before": before,
            "status_after": after,
            "has_force": after in ("FAIL", "VACUOUS"),
        })

    # Cases that must NOT fail: an emptiness the file declares, with its coverage
    # count, is a finding rather than an omission (reviewer-engineering F4).
    non_failures = []
    # THE PUBLISHED RESIDUAL OF M1, asserted as a NON-failure so that the limit
    # this build publishes is the limit it actually has. Rung 3 of the forgery
    # ladder relabels the merge provenance as well, and at that point the file
    # asserts a second input file exists; nothing inside it can contradict that.
    forged3 = _forge_merge(copy.deepcopy(placeholder), 3)
    non_failures.append({
        "case": "S30/false_merge_fully_relabelled_is_the_published_residual",
        "check": "S30",
        "status_after": _status_of(run(forged3), "S30"),
        "must_not_fail": True,
        "ok": _status_of(run(forged3), "S30") not in ("FAIL", "VACUOUS"),
        "note": (
            "This case PASSES, and that is the residual published in "
            "$.known_limits_of_this_schema. It is asserted here so the limit cannot drift "
            "from the behaviour."
        ),
    })
    for label, (cid, mutate) in ARM_REQUIRED_NON_FAILURES.items():
        mutated = copy.deepcopy(arm_file)
        mutate(mutated)
        after = _status_of(run(mutated), cid)
        non_failures.append({
            "case": label,
            "check": cid,
            "applied_to": "arm_file",
            "status_after": after,
            "must_not_fail": True,
            "ok": after not in ("FAIL", "VACUOUS"),
        })
    shared_settings = {}
    for a in placeholder["arms"]:
        shared_settings.setdefault((a["W_days"], a["clock_origin"]), []).append(
            a.get("producing_step"))
    most_shared = max((len(v) for v in shared_settings.values()), default=0)
    for label, (cid, mutate) in REQUIRED_NON_FAILURES.items():
        mutated = copy.deepcopy(placeholder)
        mutate(mutated)
        after = _status_of(run(mutated), cid)
        entry = {
            "case": label,
            "check": cid,
            "status_after": after,
            "must_not_fail": True,
            "ok": after not in ("FAIL", "VACUOUS"),
        }
        if cid == "S2":
            # A non-failure on a file with nothing to collide proves nothing.
            entry["steps_sharing_one_setting"] = {
                f"W{w}_{o}": steps for (w, o), steps in shared_settings.items()
                if len(steps) > 1
            }
            entry["max_steps_at_one_setting"] = most_shared
            entry["ok"] = entry["ok"] and most_shared > 1
        non_failures.append(entry)

    # The two-sided half of S5 and S6: a sentinel or a prefixed string left in a
    # file flagged as real data must fail.
    for cid, label in REAL_SIDE.items():
        mutated = copy.deepcopy(real)
        if cid == "S5":
            _set(_first_payload(mutated)["shares"]["never_started"], "value_percent",
                 V.SENTINEL_PERCENT)
        else:
            _set(_first_payload(mutated)["bounds"]["never_started"], "note",
                 f"{V.PLACEHOLDER_PREFIX}: left behind")
        results.append({
            "check": f"{cid}/{label}",
            "applied_to": "real",
            "status_before": _status_of(baseline_real, cid),
            "status_after": _status_of(run(mutated), cid),
            "has_force": _status_of(run(mutated), cid) == "FAIL",
        })

    vocab_link = _statistic_vocabulary_link(schema)

    without_force = [r["check"] for r in results if not r["has_force"]]
    na_on_real = [c["id"] for c in baseline_real["semantic_checks"] if c["status"] == "N/A"]

    non_failure_failures = [n["case"] for n in non_failures if not n["ok"]]

    # EVERY CHECK THAT EXISTS IS EXERCISED BY SOMETHING HERE. Without this, a
    # check added to the validator and to no mutation table is silently
    # unexercised, and this script's headline count still reads "N of N with
    # force" -- the count of what it happened to try, not of what exists. That is
    # the shape CLAUDE.md names: an empty result and a clean result are the same
    # value, and only the control knows which it produced.
    exercised = {r["check"].split("/")[0] for r in results}
    all_check_ids = {c["id"] for c in baseline_ph["semantic_checks"]}
    unexercised = sorted(all_check_ids - exercised)

    record = {
        "generated_at_utc": stamp,
        "generator": "src/step8b_selftest.py",
        # A RUN RECORD NAMES THE BUILD IT RAN ON (v1.9.0, reviewer-engineering F4
        # on the rerun record). Every selftest log until now carried a timestamp
        # and no commit, and `logs/` is gitignored, so nothing placed a result in
        # the history. The stamp names both sides of the run and leaves the side
        # it cannot know NULL rather than repeating the other.
        "build": RS.build_stamp(
            os.environ.get("STEP8B_REPRODUCED_ON") or RS.head_short(),
            "the build this selftest ran on. STEP8B_REPRODUCED_ON carries the pre-edit HEAD "
            "when a run sets it; otherwise both sides are the same commit and "
            "`head_equals_reproduced_on` says so",
        ),
        "schema": SCHEMA_PATH,
        "instance": PLACEHOLDER_PATH,
        "baseline_placeholder": {
            "schema_errors": baseline_ph["schema_errors"],
            "statuses": {c["id"]: c["status"] for c in baseline_ph["semantic_checks"]},
        },
        "baseline_real_copy": {
            "schema_errors": baseline_real["schema_errors"],
            "statuses": {c["id"]: c["status"] for c in baseline_real["semantic_checks"]},
        },
        "baseline_arm_file": {
            "instance": ARM_PLACEHOLDER_PATH,
            "schema_errors": baseline_arm["schema_errors"],
            "statuses": {c["id"]: c["status"] for c in baseline_arm["semantic_checks"]},
        },
        "baseline_sole_file": {
            "instance": SOLE_PLACEHOLDER_PATH,
            "schema_errors": baseline_sole["schema_errors"],
            "statuses": {c["id"]: c["status"] for c in baseline_sole["semantic_checks"]},
        },
        "step13_arm_file_fixture": step13_record,
        "s41_interval_exemption_scope": s41_record,
        "s41_owner_key": s41_owner_record,
        "s41_owner_key_discriminating_fixture": s41_keying_record,
        "step10_interval_obligation": step10_record,
        "malformed_headline_shapes": malformed_record,
        "bootstrap_partition_anchor": anchor_record,
        "registry_arm_difference_fact": registry_fact_record,
        "statistic_vocabulary_link": vocab_link,
        "mutations": results,
        "required_non_failures": non_failures,
        "required_non_failures_violated": non_failure_failures,
        "checks_defined_but_never_exercised": unexercised,
        "baseline_failures_anywhere": {
            "placeholder": [k for k, v in
                            {c["id"]: c["status"] for c in baseline_ph["semantic_checks"]}.items()
                            if v in ("FAIL", "VACUOUS")],
            "arm_file": [k for k, v in
                         {c["id"]: c["status"] for c in baseline_arm["semantic_checks"]}.items()
                         if v in ("FAIL", "VACUOUS")],
            "sole_file": [k for k, v in
                          {c["id"]: c["status"] for c in baseline_sole["semantic_checks"]}.items()
                          if v in ("FAIL", "VACUOUS")],
        },
        "checks_shown_to_have_force": len(results) - len(without_force),
        "checks_total_exercised": len(results),
        "checks_without_force": without_force,
        "checks_na_on_the_real_copy": na_on_real,
        "ok": (not without_force and not non_failure_failures and not unexercised
               and step13_ok and vocab_link["ok"] and s41_record["ok"]
               and s41_owner_record["ok"] and s41_keying_record["ok"]
               and step10_record["ok"] and malformed_record["ok"]
               and anchor_record["ok"] and registry_fact_record["ok"]),
    }

    os.makedirs(LOG_DIR, exist_ok=True)
    path = os.path.join(LOG_DIR, f"selftest-{stamp.replace(':', '')}.json")
    with open(path, "w") as fh:
        json.dump(record, fh, indent=2)
        fh.write("\n")

    print(json.dumps({
        "log": path,
        "ok": record["ok"],
        "checks_shown_to_have_force": record["checks_shown_to_have_force"],
        "checks_total_exercised": record["checks_total_exercised"],
        "checks_without_force": without_force,
        "checks_defined_but_never_exercised": unexercised,
        "step13_arm_file_fixture_ok": step13_ok,
        "step13_arm_file_failures": step13_record["failures"],
        "s41_interval_exemption_scope": {
            "ok": s41_record["ok"],
            "exempt_by_the_ruling": s41_record["exempt_by_the_ruling"],
            "exempt_in_the_validator": s41_record["exempt_in_the_validator"],
            "tables_agree": s41_record["tables_agree"],
            "expected_statuses": s41_record["expected_statuses"],
            "statuses": s41_record["statuses"],
            "zero_coverage_statuses": s41_record["zero_coverage_statuses"],
            "levels_only_statuses": s41_record["levels_only_statuses"],
            "publishes_both_objects_statuses":
                s41_record["publishes_both_objects_statuses"],
        },
        "s41_owner_key": {
            "ok": s41_owner_record["ok"],
            "owners": s41_owner_record["owners"],
            "arm_labels_covering_more_than_one_step":
                s41_owner_record["arm_labels_covering_more_than_one_step"],
        },
        "s41_owner_key_discriminating_fixture": {
            "ok": s41_keying_record["ok"],
            "step_relabelled_levels_only": s41_keying_record["step_relabelled_levels_only"],
            "aggregated_by_arm": s41_keying_record["aggregated_by_arm"],
            "every_arm_still_carries_both_objects":
                s41_keying_record["every_arm_still_carries_both_objects"],
            "expected_s41_status": s41_keying_record["expected_s41_status"],
            "s41_status": s41_keying_record["s41_status"],
        },
        "step10_interval_obligation": {
            "ok": step10_record["ok"],
            "ruling": step10_record["ruling"],
            "publisher_table_outcome_shares":
                step10_record["publisher_table_outcome_shares"],
            "publisher_table_window_w_percentile":
                step10_record["publisher_table_window_w_percentile"],
            "exempt_in_the_validator": step10_record["exempt_in_the_validator"],
            "omits_intervals": step10_record["omits_intervals"],
            "publishes_both_objects": step10_record["publishes_both_objects"],
            "publishes_levels_only": step10_record["publishes_levels_only"],
        },
        "malformed_headline_shapes": {
            "ok": malformed_record["ok"],
            "shapes": {k: {"raised": v.get("raised"),
                           "schema_errors": v.get("schema_errors"),
                           "semantic_checks_run": v.get("semantic_checks_run")}
                       for k, v in malformed_record["shapes"].items()},
        },
        "bootstrap_partition_anchor": {
            "ok": anchor_record["ok"],
            "validator_anchor": anchor_record["validator_anchor"],
            "generator_list": anchor_record["generator_list"],
        },
        "registry_arm_difference_fact": {
            "ok": registry_fact_record["ok"],
            "fields_compared": registry_fact_record["fields_compared"],
            "field_comparisons_made": registry_fact_record["field_comparisons_made"],
            "classes_with_two_or_more_entries":
                registry_fact_record["classes_with_two_or_more_entries"],
            "fields_differing_between_arms_within_a_class":
                registry_fact_record["fields_differing_between_arms_within_a_class"],
            "expected_fields_differing": registry_fact_record["expected_fields_differing"],
            "resampling_unit_by_class": registry_fact_record["resampling_unit_by_class"],
        },
        "statistic_vocabulary_link": {
            "ok": vocab_link["ok"],
            "files_read": f"{vocab_link['files_read']}/{vocab_link['files_expected']}",
            "characters_compared": vocab_link["characters_compared"],
            "byte_identical": vocab_link["byte_identical"],
            "schema_enum_tokens": vocab_link["schema_enum_tokens"],
            "failures": vocab_link["failures"],
        },
        "required_non_failures_violated": non_failure_failures,
        "baseline_placeholder_failures": [
            k for k, v in record["baseline_placeholder"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
        "baseline_real_failures": [
            k for k, v in record["baseline_real_copy"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
        "baseline_arm_file_failures": [
            k for k, v in record["baseline_arm_file"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
        "baseline_sole_file_failures": [
            k for k, v in record["baseline_sole_file"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
    }, indent=2))
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
