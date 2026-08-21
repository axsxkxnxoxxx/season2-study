#!/usr/bin/env python3
"""
Step 9, arm a -- WORKING-FIGURES EXTRACT.

Human Lead ruling, 2026-08-21: `processed/` is gitignored, so arm a's Step 9 counts exist in
exactly one place and are not recoverable from a clone. A transcription assembled by another
party was discarded unsigned (`0092` -- a transcription is not an attestation), so the producing
arm emits its own figures.

THIS SCRIPT COMPUTES NOTHING. It opens exactly one input --

    processed/step9/a/measured.json

-- and copies values out of it, attaching to every figure the JSON path it was copied from, so a
reader can go and check rather than trust. Where the ruling asks for a field this arm's working
output does not contain, the field is emitted as an explicit ABSENT record, never filled from
another file.

It does NOT read processed/step9/b/, any other arm's namespace, or pairs.npz -- and no emitted
field is derived from any of them. Counts and account totals only; no pair-level rows.

Output: artifacts/step9-working-figures-a.json
"""

import hashlib
import json
import os
import datetime as dt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_REL = "processed/step9/a/measured.json"
SRC = os.path.join(ROOT, SRC_REL)
OUT = os.path.join(ROOT, "artifacts", "step9-working-figures-a.json")

GENERATOR_REL = "src/step9_a_4_working_figures.py"
COMPUTE_REL = "src/step9_a_1_compute.py"

M = json.load(open(SRC))


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def mtime_of(path):
    return dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc)\
        .strftime("%Y-%m-%dT%H:%M:%SZ")


def get(path):
    """Fetch by dotted JSON path. Bar-separated bootstrap keys are handled by exact lookup."""
    node = M
    for part in path.lstrip("$").lstrip(".").split("."):
        node = node[part]
    return node


def fig(path):
    """A figure, labelled with the key it was copied from."""
    return {"value": get(path), "key": "$." + path.lstrip("$").lstrip(".")}


def absent(what, why, where_it_lives=None):
    rec = {"status": "ABSENT_FROM_WORKING_OUTPUT", "field": what, "why": why}
    if where_it_lives:
        rec["not_filled_from"] = where_it_lives
    return rec


# ---------------------------------------------------------------------------------------------
# per-arm blocks
# ---------------------------------------------------------------------------------------------
ARMS = ["W108_s2_finale", "W091_s2_finale", "W091_s2_premiere"]

# The clock origin is NOT a field of the working output. It is encoded in the arm key string and
# in `label`. Recorded that way rather than invented as a field.
CLOCK_ORIGIN_ENCODED_IN = {
    "W108_s2_finale": "s2_finale",
    "W091_s2_finale": "s2_finale",
    "W091_s2_premiere": "s2_premiere",
}


def pop_block(arm, pop):
    b = f"arms_measured.{arm}.{pop}"
    e = f"{b}.exclusions"
    c = f"{b}.channel_pairs_last_insertion_in_tau1_tau2"
    return {
        "n_position_5": fig(f"{b}.n_position_5"),
        "n_post_liveness": fig(f"{b}.n_post_liveness"),
        "accounts_position_5": fig(f"{b}.accounts_position_5"),
        "position_5_counts": {k: fig(f"{b}.position_5_counts.{k}")
                              for k in ("never_started", "started_and_left",
                                        "continued", "total")},
        "post_liveness_counts": {k: fig(f"{b}.post_liveness_counts.{k}")
                                 for k in ("never_started", "started_and_left",
                                           "continued", "total")},
        "exclusion_breakdown": {
            "total": fig(f"{e}.total"),
            "never_started_component": fig(f"{e}.never_started_component"),
            "started_and_left_component": fig(f"{e}.started_and_left_component"),
            "continued_component": fig(f"{e}.continued_component"),
            "accounts": fig(f"{e}.accounts"),
            "accounts_never_started_component": fig(f"{e}.accounts_never_started_component"),
            "accounts_started_and_left_component":
                fig(f"{e}.accounts_started_and_left_component"),
            "account_components_note": (
                "The two account components are counts of DISTINCT ACCOUNTS within each outcome "
                "component and are not required to sum to `accounts`: one account can contribute "
                "pairs to both components. No de-overlap figure was computed by this arm and "
                "none is computed here."),
        },
        "silence_test_alone": fig(f"{e}.silence_test_alone"),
        "spared_by_not_continued": fig(f"{e}.spared_by_not_continued"),
        "channel_pairs_last_insertion_in_tau1_tau2": {
            k: fig(f"{c}.{k}") for k in ("total", "started_and_left",
                                         "never_started", "accounts")},
        "conjunct_ladder": {
            "status": "NO_EXPLICIT_LADDER_FIELD_IN_WORKING_OUTPUT",
            "what_the_working_output_has_instead": (
                "Two rungs, taken in the order conjunct-1-first. `silence_test_alone` is the "
                "position-5 rows failing conjunct 1 alone (no insertion instant after that "
                "pair's tau1), source expression `(p5m & res['silent']).sum()`. "
                "`spared_by_not_continued` is the subset of those that ARE Continued and are "
                "therefore retained, source expression "
                "`(p5m & res['silent'] & res['continued']).sum()`. Both at "
                f"{COMPUTE_REL} lines 208-209."),
            "rungs_present": ["n_position_5", "silence_test_alone",
                              "spared_by_not_continued", "exclusion_breakdown.total"],
            "rung_NOT_present": (
                "The conjunct-2-first rung -- the count of position-5 rows that are NOT "
                "Continued, before conjunct 1 narrows them -- was not computed by this arm and "
                "is NOT computed here."),
        },
    }


arms_out = {}
for arm in ARMS:
    a = f"arms_measured.{arm}"
    rc = f"{a}.right_censoring_two_lines"
    arms_out[arm] = {
        "label": fig(f"{a}.label"),
        "W_days": fig(f"{a}.W_days"),
        "H_days": fig(f"{a}.H_days"),
        "clock_origin": {
            "value": CLOCK_ORIGIN_ENCODED_IN[arm],
            "key": f"$.arms_measured.{arm} (arm key string) and $.arms_measured.{arm}.label",
            "note": ("The working output carries NO separate clock_origin field. The origin is "
                     "encoded in the arm key and repeated in `label`; it is transcribed from "
                     "those, not supplied from another file."),
        },
        "right_censoring_two_lines": {
            pop: {k: fig(f"{rc}.{pop}.{k}")
                  for k in ("n_in_position_4", "removed_by_max_W_91_term",
                            "removed_incrementally_by_the_plus_H_term")}
            for pop in ("APPLY", "DERIV")},
        "APPLY": pop_block(arm, "APPLY"),
        "DERIV": pop_block(arm, "DERIV"),
    }

# The premiere arm's population is the primary arm's row set (reading (a)); its censoring lines
# are its own. Stated inside the arm rather than left for a reader to trip over.
arms_out["W091_s2_premiere"]["population_reading"] = {
    "value": "reading_a_shared_population",
    "source": f"{COMPUTE_REL} lines 223-226 (arm_block(r91p, r108['pos5'], r108['pos5_deriv']))",
    "note": ("This arm's outcome and exclusion counts are measured ON THE W=108 FINALE ARM'S "
             "POSITION-5 ROW SET, per reading (a) of 'both arms run on the same right-censored "
             "population' (D10). Its `right_censoring_two_lines` sub-block, however, is computed "
             "from the arm's OWN W=91 run, so the two lines in that sub-block do not reduce "
             "position 4 to this arm's `n_position_5`. Both readings are measured -- see "
             "`d10_reading_ambiguity` below. Recorded as a defect of this arm's working output "
             "in `defects_found_while_transcribing`."),
}

# ---------------------------------------------------------------------------------------------
# T0 movement, on the predicate this arm actually used
# ---------------------------------------------------------------------------------------------
d = "d10_reading_ambiguity"
t0_movement = {
    "what_this_is": (
        "This arm's measurement of what moving T0 from the S2 finale to the S2 premiere does. "
        "Transcribed ON THE PREDICATE THIS ARM USED and NOT converted to any other predicate."),
    "predicate_used": {
        "expression": "t0_premiere == t0_finale",
        "reading": "the two clocks COINCIDE on the pair",
        "source": f"{COMPUTE_REL} line 242",
        "both_sides_are": ("floor-day epoch seconds; t0_finale from Step 8's positions.npz "
                           "['t0'], t0_premiere = max(floor_day(s2_premiere_date), s1_date), "
                           f"{COMPUTE_REL} lines 75-81"),
    },
    "pairs_where_the_two_clocks_coincide": fig(f"{d}.pairs_where_the_two_clocks_coincide"),
    "premiere_t0_never_later_than_finale_t0": fig(f"{d}.premiere_t0_never_later_than_finale_t0"),
    "NOT_CONVERTED": (
        "The complement -- 'pairs on which T0 moves' -- is NOT stated. It is not in this arm's "
        "working output, and its denominator is not either (see the population record below), so "
        "any complement would be a new measurement. Per the ruling, none is made."),
    "population_of_the_two_figures_above": absent(
        "population label for `pairs_where_the_two_clocks_coincide` and "
        "`premiere_t0_never_later_than_finale_t0`",
        ("The working output records no population for these two. Their source expressions run "
         "over the FULL pair vector loaded from Step 8's scan.npz, before any position filter -- "
         "so the base is neither APPLY (196,654) nor DERIV (147,370). The size of that base is "
         "not recorded in the working output and is NOT computed here.")),
    "d10_reading_counts": {
        k: fig(f"{d}.{k}") for k in (
            "reading_a_shared_population_APPLY", "reading_b_premiere_anchored_d10_APPLY",
            "in_b_not_in_a_APPLY", "in_a_not_in_b_APPLY",
            "reading_a_shared_population_DERIV", "reading_b_premiere_anchored_d10_DERIV",
            "in_b_not_in_a_DERIV", "in_a_not_in_b_DERIV")},
    "censoring_set_identical_premiere_vs_finale_at_W91": {
        "APPLY": fig(f"{d}.censoring_set_identical_premiere_vs_finale_at_W91_APPLY"),
        "DERIV": fig(f"{d}.censoring_set_identical_premiere_vs_finale_at_W91_DERIV"),
    },
    "so_the_353_and_315_are_the_W_term_not_the_origin": {
        "value": get(f"{d}.so_the_353_and_315_are_the_W_term_not_the_origin"),
        "key": f"$.{d}.so_the_353_and_315_are_the_W_term_not_the_origin",
        "WARNING": ("NOT A MEASUREMENT. This key is a hardcoded `True` literal in "
                    f"{COMPUTE_REL} line 251. Its measured support is the two "
                    "`censoring_set_identical_*` booleans above, which ARE computed. Transcribed "
                    "as it stands, marked as an asserted constant."),
    },
}

# ---------------------------------------------------------------------------------------------
# bootstrap settings (settings and one account total; the INTERVALS are deliberately not copied)
# ---------------------------------------------------------------------------------------------
bs = "bootstrap_settings"
bootstrap = {
    "settings": {k: fig(f"{bs}.{k}") for k in (
        "B", "seed", "resampling_unit", "statistics", "frame_accounts",
        "frame_definition", "movement_configurations", "ci_level_pct", "method")},
    "intervals_not_copied_here": {
        "status": "PRESENT_IN_WORKING_OUTPUT_BUT_DELIBERATELY_NOT_RE-EMITTED",
        "where_they_are_in_the_working_output": (
            "$.bootstrap, keyed '<arm>|<population>|<outcome>', each carrying level.lower, "
            "level.upper, movement.lower, movement.upper, point_level, point_movement."),
        "why_not_here": (
            "They are already published, by this arm, in artifacts/step9-headline-a.json, which "
            "is not gitignored. The ruling's rescue reason -- figures recoverable from nowhere "
            "but this machine -- does not apply to them, and re-emitting them would create a "
            "second slot for a figure that already has one."),
    },
}

# ---------------------------------------------------------------------------------------------
# absences and defects
# ---------------------------------------------------------------------------------------------
absences = [
    absent("conjunct_ladder (as a named field)",
           ("No key of that name exists at any path in the working output. The two rungs that do "
            "exist are transcribed per population under `conjunct_ladder` in each arm block. The "
            "missing rung -- position-5 rows that are NOT Continued, taken before conjunct 1 -- "
            "was never computed by this arm and is not computed here.")),
    absent("adopted_rule_revision",
           ("The fourth component of the arm key (W_days, clock_origin, producing_step, "
            "adopted_rule_revision) is not in the working output, so the arm key cannot be "
            "completed from this file alone."),
           ("artifacts/step9-headline-a.json at $.adopted_rule_revision, where this arm recorded "
            "it -- READ, not typed, via step8b_schema._read_adopted_rule_revision() at "
            "src/step9_a_2_emit.py line 33. Pointed at, deliberately NOT copied across, because "
            "the ruling forbids filling an absent field from elsewhere.")),
    absent("clock_origin (as a field)",
           ("Encoded in the arm key string and in `label`. Transcribed from those into each arm "
            "block, with that provenance stated at the point of use.")),
    absent("population label on the two T0-movement booleans/counts",
           "See t0_movement.population_of_the_two_figures_above."),
    absent("base size of the T0-movement predicate",
           ("The count of pairs the `t0_premiere == t0_finale` comparison ran over is not "
            "recorded. Not computed here.")),
    absent("outcome-level counts for the liveness-EXCLUDED set beyond the three components",
           ("The working output carries total / never_started / started_and_left / continued "
            "components and two account components, and nothing further -- no per-show, "
            "per-channel or per-episode breakdown of the excluded set exists in it.")),
]

defects = [
    {
        "id": "A-WF-1",
        "severity": "labelling, material to a reader",
        "where": "$.arms_measured.W091_s2_premiere.right_censoring_two_lines",
        "what": (
            "Inside one arm block, the censoring lines and the population counts describe "
            "DIFFERENT row sets. The two lines are computed from the arm's own W=91 premiere run "
            "(APPLY 3,384 + 1,509 off 201,900 -> 197,007), while `n_position_5` for the same arm "
            "is 196,654, the W=108 finale row set, because the arm is measured under reading (a). "
            "Neither number is wrong for its own reading; the block does not say they are "
            "different readings, so a reader who subtracts the two lines from position 4 does not "
            "land on the arm's own n_position_5. Same shape on DERIV: 3,083 + 1,358 off 152,126 "
            "-> 147,685, against n_position_5 = 147,370."),
        "not_fixed_here": (
            "This extract transcribes; it does not correct. The correction is a rerun of the arm, "
            "per 0092. Flagged in the arm block itself as `population_reading`."),
    },
    {
        "id": "A-WF-2",
        "severity": "control coverage",
        "where": "$.import_gate.mismatches",
        "what": (
            "The import gate emits an empty mismatch list and NO coverage count, so from the file "
            "alone a clean result and a result that compared nothing are the same value -- the "
            "condition CLAUDE.md requires every such path to distinguish."),
    },
    {
        "id": "A-WF-3",
        "severity": "control coverage",
        "where": f"{COMPUTE_REL} lines 150-157, the import-gate comparison loop",
        "what": (
            "The comparison is ONE-DIRECTIONAL: it iterates this arm's keys and tests "
            "`if kk in theirs`, so keys Step 8 published that this arm did not reproduce are "
            "never compared and never reported as uncovered. Concretely uncompared: "
            "liveness_exclusions_APPLY.continued, liveness_exclusions_DERIV.continued, "
            "right_censoring_two_lines_APPLY.total, right_censoring_two_lines_DERIV.total. "
            "Visible in the working output as an asymmetry between "
            "$.import_gate.reproduced and $.import_gate.step8_published."),
    },
    {
        "id": "A-WF-4",
        "severity": "asserted-not-measured",
        "where": "$.d10_reading_ambiguity.so_the_353_and_315_are_the_W_term_not_the_origin",
        "what": ("A hardcoded `True` in the source sits in a measurement block among measured "
                 "booleans, and is indistinguishable from one on inspection of the JSON. Its "
                 "grounds are measured; the field is not."),
    },
    {
        "id": "A-WF-5",
        "severity": "labelling",
        "where": ("$.d10_reading_ambiguity.pairs_where_the_two_clocks_coincide and "
                  ".premiere_t0_never_later_than_finale_t0"),
        "what": ("Every other count in this arm's working output is population-scoped; these two "
                 "are not, and their base is a third row set (the full scan pair vector) that "
                 "the file never names or sizes."),
    },
    {
        "id": "A-WF-6",
        "severity": "carried text, not this arm's measurement",
        "where": ("$.import_gate.step8_published.right_censoring_two_lines_*."
                  "direction_on_the_headline"),
        "what": ("Prose copied from Step 8's artifact sits inside this arm's working output. It "
                 "is Step 8's claim, not a measurement of this arm, and it is not transcribed "
                 "into this extract."),
    },
]

# ---------------------------------------------------------------------------------------------
# emit
# ---------------------------------------------------------------------------------------------
doc = {
    "what_this_file_is": (
        "An EVIDENCE EXTRACT of Step 9 arm a's own working figures, emitted by arm a. It is NOT "
        "a Step 8b schema arm file and does not validate against that schema; arm a's schema arm "
        "file is artifacts/step9-headline-a.json. It contains counts and account totals only."),
    "why_it_exists": (
        "processed/ is gitignored per CLAUDE.md's folder table, so these counts exist in one "
        "place and are not recoverable from a clone. Human Lead ruling, 2026-08-21: a "
        "transcription assembled by another party is not an attestation (0092), so the producing "
        "arm emits its own figures under its own sign-off."),
    "produced_by": {
        "step": 9,
        "arm": "a",
        "generator": GENERATOR_REL,
        "generator_sha256_12": sha256_of(os.path.join(ROOT, GENERATOR_REL))[:12]
        if os.path.exists(os.path.join(ROOT, GENERATOR_REL)) else None,
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "api_calls_made": fig("api_calls"),
        "method": ("Mechanical copy out of one input file, with the source key attached to every "
                   "figure. No arithmetic is performed on any transcribed value."),
    },
    "source": {
        "working_file": SRC_REL,
        "working_file_sha256": sha256_of(SRC),
        "working_file_sha256_12": sha256_of(SRC)[:12],
        "working_file_mtime_utc": mtime_of(SRC),
        "produced_by_script": COMPUTE_REL,
        "produced_by_script_sha256_12": sha256_of(os.path.join(ROOT, COMPUTE_REL))[:12],
        "step": fig("step"), "instance": fig("instance"), "stage": fig("stage"),
        "tau_pull_utc": fig("tau_pull_utc"), "H_days": fig("H_days"),
        "step8_inputs_consumed": {k: {"value": v, "key": f"$.consumed_from_step8.{k}"}
                                  for k, v in get("consumed_from_step8").items()},
        "reading_key": ("Every figure below is an object {value, key}. `key` is the JSON path in "
                        "the working file named above; `value` is byte-for-byte what is at that "
                        "path."),
    },
    "isolation_and_privacy": {
        "pairs_npz_read": False,
        "other_arm_namespace_read": False,
        "statement": (
            "processed/step9/b/ was not opened, artifacts/step9-headline-b.* was not opened, and "
            "pairs.npz was not read by this extract or by anything it reports. No field in this "
            "file is derived from any of them. Every figure is a count of pairs, a count of "
            "accounts, a setting, or a boolean; there are no pair-level rows, no usernames, no "
            "user IDs and no individual histories."),
        "account_totals_published_under": (
            "Human Lead ruling, 2026-08-21: the account counts publish -- they are counts of "
            "accounts, not accounts, and the method section needs them checkable."),
    },
    "scope_of_this_extract": {
        "arm_settings_carried": [
            {"arm_key_fragment": a,
             "W_days": get(f"arms_measured.{a}.W_days"),
             "clock_origin": CLOCK_ORIGIN_ENCODED_IN[a],
             "producing_step": 9,
             "adopted_rule_revision": "ABSENT -- see absent_fields"}
            for a in ARMS],
        "populations_carried": ["APPLY", "DERIV"],
        "not_done_here": ("No comparison, no reconciliation, no merge. This arm has no knowledge "
                          "of any other arm's figures and sought none."),
    },
    "arms": arms_out,
    "t0_movement": t0_movement,
    "bootstrap": bootstrap,
    "absent_fields": absences,
    "defects_found_while_transcribing": defects,
    "sign_off": {
        "by": "data-scientist, arm a -- the arm that produced the figures",
        "attests": ("Every value in this file was copied by the named generator out of the named "
                    "working file at the named hash. Nothing was typed from memory, nothing was "
                    "recomputed, and nothing was supplied from another file."),
        "does_not_attest": ("Anything about another arm, another step, the shared controls, or "
                            "the state of any surface this arm does not own."),
    },
}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w") as f:
    json.dump(doc, f, indent=1)
    f.write("\n")

print("wrote", OUT)
print("source", SRC_REL, sha256_of(SRC)[:12])
print("arms", ARMS)
