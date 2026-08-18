"""Step 8b -- does each check have force?

A check that has never failed is not evidence that anything is right; it may be
a check that cannot fail. This script takes the emitted placeholder, applies one
targeted mutation per check, and asserts that the check FAILS on the mutated
file and PASSES on the unmutated one.

It also runs the two checks that are N/A on a placeholder -- the derived-figure
arithmetic and the waterfall monotonicity -- against a de-sentinelled copy, so
they are exercised somewhere rather than reported N/A and never run.

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

SCHEMA_PATH = os.path.join(ROOT, "artifacts", "step8b-output-schema.json")
PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder.json")
# The ARM-FILE placeholder (decisions/0107). Half of the v1.2.0 behaviour is only
# observable on a file that is not the merged document: S17 skipping, S29's
# prohibition, and S28's one-file-per-arm clause.
ARM_PLACEHOLDER_PATH = os.path.join(ROOT, "artifacts", "step8b-placeholder-arm-file.json")
LOG_DIR = os.path.join(ROOT, "logs", "step8b")


def _first_payload(inst: dict) -> dict:
    return inst["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["a"]


def _first_abandonment(inst: dict) -> dict:
    return inst["arms"][0]["abandonment_distribution"]["APPLY"][0]


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
        if arm["waterfall"].get("block_is_absent"):
            continue
        for pop, w in arm["waterfall"].items():
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
    "S13": lambda i: _set(i["arms"][0]["waterfall"]["APPLY"]["positions"][3], "removed", 7),
    "S14": lambda i: _set(i["arms"][0]["waterfall"]["APPLY"]["positions"][0],
                          "inert_reason", None),
    "S15": lambda i: _set(i["channel_classes"]["d4"], "folded_into_bound", True),
    "S16": lambda i: i["channel_classes"]["d9"]["quantities"]["half_a"].pop("coverage"),
    "S17": lambda i: _set(i["cross_arm_divergences"]["entries"][0], "reconciled", True),
    "S18": lambda i: _first_payload(i)["shares"]["continued"]["ci"].pop("bootstrap_ref"),
    "S19": lambda i: _set(_first_payload(i)["bounds"]["continued"]["floor"], "reason", "no"),
    "S20": lambda i: _set(_first_payload(i)["bounds"]["never_started"], "degenerate", True),
    "S21": lambda i: i["arms"].__setitem__(
        2, _set(copy.deepcopy(i["arms"][2]), "clock_origin", "s2_finale")),
    # v1.1.0 -- one mutation per check added against reviewer-engineering's
    # findings, so that none of them is a check that cannot fail.
    "S22": lambda i: _set(
        i["arms"][0], "waterfall",
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
}

# Extra mutations that target a SECOND clause of a check whose first clause is
# already exercised above. Keyed by the check they must break.
EXTRA_MUTATIONS = {
    "S12/machine_checked_flags": ("S12", "placeholder", lambda i: _set(
        i["derived_fields"][0], "machine_checked", False)),
    "S13/chaining": ("S13", "real", lambda i: _set(
        i["arms"][0]["waterfall"]["APPLY"]["positions"][3], "n_in", 4242)),
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
}

# The case the ruling names in as many words: an arm file that correctly OMITS
# $.cross_arm_divergences must not fail. Before v1.2.0 it did, and the only path
# to exit 0 was a cross-arm search an isolated arm cannot honestly have run.
ARM_REQUIRED_NON_FAILURES = {
    "S17/arm_file_omitting_it_passes": ("S17", lambda i: i),
    "S29/arm_file_omitting_it_passes": ("S29", lambda i: i),
}

# Cases that must NOT fail. F4 is the reason this section exists: a legitimately
# empty list, declared as empty with its coverage count, must be distinguishable
# from a list nobody searched -- and the way to prove the distinction is live is
# to assert that one of them passes while the other fails.
REQUIRED_NON_FAILURES = {
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

    real = _make_real(placeholder)

    def run(inst: dict) -> dict:
        ev = V.SchemaEvaluator(schema)
        ev.validate(inst, schema)
        checks = V.run_semantic_checks(inst, ev)
        return {
            "semantic_checks": [c.as_dict() for c in checks],
            "schema_errors": len(ev.errors),
        }

    baseline_ph = run(placeholder)
    baseline_real = run(real)
    baseline_arm = run(arm_file)

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

    # Cases that must NOT fail: an emptiness the file declares, with its coverage
    # count, is a finding rather than an omission (reviewer-engineering F4).
    non_failures = []
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
    for label, (cid, mutate) in REQUIRED_NON_FAILURES.items():
        mutated = copy.deepcopy(placeholder)
        mutate(mutated)
        after = _status_of(run(mutated), cid)
        non_failures.append({
            "case": label,
            "check": cid,
            "status_after": after,
            "must_not_fail": True,
            "ok": after not in ("FAIL", "VACUOUS"),
        })

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
        "mutations": results,
        "required_non_failures": non_failures,
        "required_non_failures_violated": non_failure_failures,
        "checks_shown_to_have_force": len(results) - len(without_force),
        "checks_total_exercised": len(results),
        "checks_without_force": without_force,
        "checks_na_on_the_real_copy": na_on_real,
        "ok": not without_force and not non_failure_failures,
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
        "required_non_failures_violated": non_failure_failures,
        "baseline_placeholder_failures": [
            k for k, v in record["baseline_placeholder"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
        "baseline_real_failures": [
            k for k, v in record["baseline_real_copy"]["statuses"].items()
            if v in ("FAIL", "VACUOUS")],
    }, indent=2))
    return 0 if record["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
