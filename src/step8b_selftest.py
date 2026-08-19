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

Writes its record to logs/step8b/selftest-<stamp>.json. Exit 0 iff every check
was shown to have force.

    python3 src/step8b_selftest.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import step8b_validate as V  # noqa: E402
import step8b_schema as G  # noqa: E402

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
    "S38": lambda i: _set(i["declared_intervals"][0], "produced_by_step", "step10"),
}


def _relabel_arm(node, level: int):
    """Relabel a copied arm-a payload as arm b, at three degrees of effort.

    level 1 relabels the arm only; level 2 also relabels the bootstrap
    references, the statistic and the sampling-width convention labels; level 3
    also relabels the merge provenance. The three are the M1 forgery ladder, and
    the point of running all three is to show WHICH rung the check stops at.
    """
    if isinstance(node, dict):
        out = {}
        for k, v in node.items():
            if k in ("producing_arm", "arm_held") and v == "a":
                out[k] = "b"
            elif k == "bootstrap_ref" and level >= 2 and isinstance(v, str):
                out[k] = v.replace("a_", "b_", 1)
            elif k == "statistic" and level >= 2:
                out[k] = "levels"
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
               and step13_ok),
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
