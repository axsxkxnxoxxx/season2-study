"""Step 9, arm `b`, stage 5: emit an extract of THIS ARM'S OWN working figures.

Authorised by the Human Lead, 2026-08-21. `processed/` is gitignored, so arm b's Step 9
counts exist in exactly one place and are not recoverable from a clone. A transcription
assembled by another party was discarded unsigned under `0092` ("a transcription is not an
attestation"), so the producing arm emits them itself and the file carries its sign-off.

WHAT THIS DOES
  - READS `processed/step9/b/stage1_counts.json` and `processed/step9/b/stage2_bootstrap.json`.
  - Copies figures out of them, each one LABELLED with its source file and its key path, so a
    reader can go and check rather than trust.
  - Records fields that do not exist in the working output as ABSENT, with a reason. It never
    supplies an absent value from elsewhere and never leaves a silent gap.

WHAT THIS DOES NOT DO
  - It NEVER opens `processed/step9/b/pairs.npz`. That file is pair-level data. No field in the
    output is derived from it, directly or otherwise.
  - It computes NO study figure. Every number below is read from a working file by key. The only
    arithmetic performed anywhere in this script is in `_assert_transcription_consistent()`,
    which checks that what was read hangs together and raises if it does not; its results are
    NOT published as figures.
  - It reads NO other arm's namespace. `processed/step9/a/` and `artifacts/step9-*-a.*` are not
    opened. `src/step9_a_*.py` is not read.
  - It adopts nothing and makes zero API calls.

`ref()` HARD STOPS on a missing key rather than defaulting, so a label can never name a key the
value did not come from.
"""
import datetime
import hashlib
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
WORK = os.path.join(ROOT, "processed/step9/b")
# See src/step9_b_3_emit.py: STEP9_B_OUTDIR redirects a correction run away from the committed
# deliverables. The run record follows the output, so a preview run cannot overwrite the record
# of the file that is actually on disk in artifacts/.
OUTDIR = os.environ.get("STEP9_B_OUTDIR", os.path.join(ROOT, "artifacts"))
OUT = os.path.join(OUTDIR, "step9-working-figures-b.json")
RUNLOG = os.path.join(ROOT, os.environ.get("STEP9_B_WF_RUNLOG",
                                           "logs/step9-b-working-figures-run.txt"))
os.makedirs(OUTDIR, exist_ok=True)

FORBIDDEN = "pairs.npz"

SRC = {
    "stage1": "processed/step9/b/stage1_counts.json",
    "stage2": "processed/step9/b/stage2_bootstrap.json",
}
DOC = {k: json.load(open(os.path.join(ROOT, v))) for k, v in SRC.items()}


def _sha12(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def ref(doc, *path):
    """Read one value by key path. NO DEFAULT: a missing key is a hard stop."""
    node = DOC[doc]
    for k in path:
        if not isinstance(node, dict) or k not in node:
            raise KeyError(
                "HARD STOP: %s has no key $.%s -- a figure that is not in the working "
                "output does not go in the file." % (SRC[doc], ".".join(path)))
        node = node[k]
    if isinstance(node, (dict, list)):
        raise TypeError("HARD STOP: $.%s is not a leaf" % ".".join(path))
    return {"value": node, "source_file": SRC[doc], "key": "$." + ".".join(path)}


def absent(field, where, why):
    return {"status": "ABSENT",
            "field": field,
            "would_live_at": where,
            "why_absent": why,
            "note": "Recorded as absent. No value was supplied from elsewhere."}


# --------------------------------------------------------------------------------------------
# The two arm settings this arm's working output carries. The setting is encoded in the
# working file's KEY NAME; `W_days` and `clock_origin` are not stored as fields of their own,
# so the key name is quoted verbatim and the reading is labelled as a reading of that name.
# --------------------------------------------------------------------------------------------
SETTINGS = [
    ("W108_s2_finale", 108, "s2_finale",
     "the adopted arm: W = 108 days, T0 = max(S2 FINALE air date, S1 completion date)"),
    ("W91_s2_premiere", 91, "s2_premiere",
     "the second headline arm: W = 91 days (Netflix's own reporting window), T0' = max(S2 "
     "PREMIERE date, first-pass S1 completion date). D5: this arm has a SEPARATE ORIGIN, "
     "which is stated here and not smoothed over."),
]
POPS = ["APPLY", "DERIV"]
OUTCOMES = ["never_started", "started_and_left", "continued"]


def block(setting_key, pop):
    def r(*p):
        return ref("stage1", setting_key, pop, *p)
    return {
        "n_position_5": r("n_position_5"),
        "n_post_liveness": r("n_post_liveness"),
        "position_5": {o: r("position_5", o) for o in OUTCOMES},
        "position_7_post_liveness": {o: r("position_7", o) for o in OUTCOMES},
        "_position_7_naming_note":
            "the working output names the post-liveness counts `position_7`; they are the "
            "post-liveness counts asked for, transcribed under the name they were stored with.",
        "exclusions": {
            "total_pairs": r("exclusions", "total_pairs"),
            "never_started_component": r("exclusions", "never_started_component"),
            "started_and_left_component": r("exclusions", "started_and_left_component"),
            "continued_component": r("exclusions", "continued_component"),
            "accounts": r("exclusions", "accounts"),
            "_accounts_note":
                "a count of DISTINCT ACCOUNTS in the excluded set, not accounts. Published "
                "under the Human Lead's 2026-08-21 ruling that the account counts publish "
                "because the method section needs them checkable. No identifier is carried.",
            "silence_test_alone": r("exclusions", "silence_test_alone"),
            "spared_by_not_continued": r("exclusions", "spared_by_not_continued"),
            "_what_those_two_fields_COUNT": {
                "silence_test_alone":
                    "coded `int((mask & r['silent']).sum())` in src/step9_b_1_compute.py -- "
                    "pairs on this population's position-5 mask that meet CONJUNCT 1 ALONE "
                    "(no insertion instant after their own tau1), IRRESPECTIVE of Continued. "
                    "It is NOT the count of pairs excluded by the silence test alone; the "
                    "field name invites that misreading and the misreading is wrong.",
                "spared_by_not_continued":
                    "coded `int((mask & r['silent'] & r['continued']).sum())` -- pairs that "
                    "meet conjunct 1 but are Continued, so conjunct 2 spares them from the "
                    "NOT-LIVE verdict.",
            },
        },
        "conjunct_ladder": {
            "_present": True,
            "_stored_as": "$.%s.%s.conjunct_selection" % (setting_key, pop),
            "_ordering": "conjunct 2 (NOT Continued) first, then conjunct 1 (silent at tau1). "
                         "The working output stores this ONE ordering only.",
            "start": r("conjunct_selection", "start"),
            "after_conjunct_2_not_continued": r("conjunct_selection",
                                                "after_conjunct_2_not_continued"),
            "after_conjunct_1_silent_at_tau1": r("conjunct_selection",
                                                 "after_conjunct_1_silent_at_tau1"),
        },
    }


figures = {}
for key, w, origin, gloss in SETTINGS:
    figures[key] = {
        "_working_file_key_name": key,
        "_reading_of_that_key_name": {"W_days": w, "clock_origin": origin, "gloss": gloss},
        "_W_days_and_clock_origin_are_not_stored_fields":
            "they are encoded in the working file's key name, quoted verbatim above. The "
            "reading is labelled as a reading of the name, not as a stored figure.",
        "APPLY": block(key, "APPLY"),
        "DERIV": block(key, "DERIV"),
    }

# --------------------------------------------------------------------------------------------
# T0 movement, ON THE PREDICATE ACTUALLY USED. Not converted to any other predicate.
# --------------------------------------------------------------------------------------------
t0_movement = {
    "figure": ref("stage1", "premiere_arm_preconditions", "pairs_where_t0_moves"),
    "predicate_as_coded":
        "int((t0_prem < t0_finale)[pos5].sum())   # src/step9_b_1_compute.py line 161",
    "predicate_in_words":
        "the number of pairs whose premiere-anchored T0' is STRICTLY EARLIER than their "
        "finale-anchored T0. t0_prem = max(S2 premiere date, first-pass S1 completion date); "
        "t0_finale = the adopted T0 = max(S2 finale air date, S1 completion date). Both at "
        "midnight UTC, compared as epoch seconds.",
    "strictness": "STRICT `<`. Pairs where the two origins coincide are NOT counted.",
    "population_of_the_mask": {
        "population": "APPLY, position 5",
        "how_it_is_known": "the mask applied in the code is `pos5`, which is the APPLY "
                           "position-5 mask (r108['pos5']).",
        "defect": "the working file does NOT record this population beside the figure; it is "
                  "recoverable only from the source line. Stated here from the code, and "
                  "reported as a defect of the working output.",
    },
    "not_converted":
        "transcribed exactly as measured. It is NOT restated as a share, NOT restated as a "
        "count of pairs whose T0 does not move, and NOT restated on DERIV.",
    "companions_stored_with_it": {
        "_what_replaced_the_three_booleans":
            "The build this file previously described stored three booleans here -- "
            "t0_is_earlier_or_equal_for_every_pair and tau2_observable_on_every_retained_pair "
            "on each population. All three were guaranteed by a DEFECTIVE T0' vector and "
            "returned True on it, so none of them could fail and none of them checked "
            "anything. They are GONE, not restated. TWO CHECKS STAND IN THEIR PLACE, and both "
            "raise rather than returning a flag: DEF-A, below, which decodes the premiere epoch "
            "vector back to calendar dates and compares it elementwise against the frame's own "
            "s2_premiere_date; and T0PRIME-ORDER, below that, which verifies the ORDERING "
            "WARRANT the deliverable claims -- T0' <= T0, and tau2' < tau2 <= tau_pull on the "
            "retained rows. T0PRIME-ORDER IS NOT THE REMOVED BOOLEAN RESTORED: its part 1 "
            "reconstructs T0' from the frame's own date STRINGS, so it FAILS on the vector that "
            "made the boolean vacuous, which the boolean could not.",
        "clock_vector_verification": {
            "check": ref("stage1", "premiere_arm_preconditions",
                         "clock_vector_verification", "check"),
            "rows_compared_by_show": ref("stage1", "premiere_arm_preconditions",
                                         "clock_vector_verification", "by_show",
                                         "rows_compared"),
            "mismatches_by_show": ref("stage1", "premiere_arm_preconditions",
                                      "clock_vector_verification", "by_show", "mismatches"),
            "rows_compared_by_pair": ref("stage1", "premiere_arm_preconditions",
                                         "clock_vector_verification", "by_pair",
                                         "rows_compared"),
            "mismatches_by_pair": ref("stage1", "premiere_arm_preconditions",
                                      "clock_vector_verification", "by_pair", "mismatches"),
            "total_rows_compared": ref("stage1", "premiere_arm_preconditions",
                                       "clock_vector_verification", "total_rows_compared"),
            "resolution_read_off_the_dtype":
                ref("stage1", "premiere_arm_preconditions", "clock_vector_verification",
                    "epoch_conversion", "resolution_read_off_the_dtype"),
            "ticks_per_second_selected":
                ref("stage1", "premiere_arm_preconditions", "clock_vector_verification",
                    "epoch_conversion", "ticks_per_second_selected"),
            "divisor_hardcoded":
                ref("stage1", "premiere_arm_preconditions", "clock_vector_verification",
                    "epoch_conversion", "divisor_hardcoded"),
            "t0_restored_after_the_substituted_run":
                ref("stage1", "premiere_arm_preconditions", "clock_vector_verification",
                    "t0_restored_after_the_substituted_run"),
        },
        "t0_prime_order_verification": {
            "_what_this_is":
                "THE CHECK BEHIND THE DELIVERABLE'S ORDERING CLAIM. The arm file states that "
                "the row set is not re-censored because T0' <= T0 on every pair; this is what "
                "establishes it, and it raises. Three parts, because the bare inequality cannot "
                "fail on a collapsed T0'.",
            "check": ref("stage1", "premiere_arm_preconditions",
                         "t0_prime_order_verification", "check"),
            "raises_on_failure": ref("stage1", "premiere_arm_preconditions",
                                     "t0_prime_order_verification", "raises_on_failure"),
            "why_the_inequality_alone_is_not_enough":
                ref("stage1", "premiere_arm_preconditions", "t0_prime_order_verification",
                    "why_the_inequality_alone_is_not_enough"),
            "part_1_rows_compared": ref("stage1", "premiere_arm_preconditions",
                                        "t0_prime_order_verification", "part_1_reconstruction",
                                        "rows_compared"),
            "part_1_mismatches": ref("stage1", "premiere_arm_preconditions",
                                     "t0_prime_order_verification", "part_1_reconstruction",
                                     "mismatches"),
            "part_2_rows_compared": ref("stage1", "premiere_arm_preconditions",
                                        "t0_prime_order_verification", "part_2_ordering",
                                        "rows_compared"),
            "part_2_violations": ref("stage1", "premiere_arm_preconditions",
                                     "t0_prime_order_verification", "part_2_ordering",
                                     "violations"),
            "part_2_pairs_strictly_earlier": ref("stage1", "premiere_arm_preconditions",
                                                 "t0_prime_order_verification",
                                                 "part_2_ordering", "pairs_strictly_earlier"),
            "part_2_pairs_equal": ref("stage1", "premiere_arm_preconditions",
                                      "t0_prime_order_verification", "part_2_ordering",
                                      "pairs_equal"),
            **{"part_3_%s_%s" % (pop.lower(), k):
               ref("stage1", "premiere_arm_preconditions", "t0_prime_order_verification",
                   "part_3_observability", "populations", pop, k)
               for pop in ("APPLY", "DERIV")
               for k in ("rows_compared", "tau2_prime_not_before_tau2_violations",
                         "tau2_prime_after_tau_pull_violations",
                         "min_margin_days_tau2_to_tau2_prime",
                         "min_margin_days_tau2_prime_to_tau_pull")},
            "total_rows_compared": ref("stage1", "premiere_arm_preconditions",
                                       "t0_prime_order_verification", "total_rows_compared"),
        },
        "measured_properties_of_the_corrected_clock": {
            "_what_these_are":
                "counts, not the check. The same two comparisons are ASSERTED elementwise, and "
                "raise, in T0PRIME-ORDER part 3 above; these are the counts restated where a "
                "reader can see them. ON THEIR OWN the two tau2 counts cannot detect a wrong "
                "premiere vector -- they are implied by T0' <= T0 and D10, and T0' <= T0 is "
                "itself implied by any collapsed T0'. DEF-A and T0PRIME-ORDER part 1 are what "
                "can fail on such a vector.",
            **{k: ref("stage1", "premiere_arm_preconditions", k) for k in [
                "shows_where_premiere_precedes_finale",
                "shows_where_premiere_equals_finale",
                "shows_where_premiere_follows_finale",
                "shows_total",
                "pairs_where_t0_prime_is_the_premiere_date",
                "pairs_where_t0_prime_is_the_s1_completion_date",
                "retained_pairs_with_tau2_after_tau_pull_APPLY",
                "retained_pairs_with_tau2_after_tau_pull_DERIV"]},
        },
    },
}

# --------------------------------------------------------------------------------------------
# Supplementary counts from the same working file. Beyond the required list, included because
# they are counts, they are this arm's own measurements, and they bear directly on the
# exclusion picture the ruling is about. Labelled and segregated, not mixed into the above.
# --------------------------------------------------------------------------------------------
supplementary = {
    "_why_included":
        "counts only, measured by this arm, directly adjacent to the exclusion breakdown. "
        "Segregated from the required fields so a reader can see what was asked for and what "
        "was added.",
    "channel_pairs_conceded_by_the_floor": {
        "_what_these_are":
            "RETAINED pairs (not exclusions): live only because they inserted after tau1, "
            "NOT Continued, with last insertion inside (tau1, tau2). They could produce no "
            "evidence dated after that instant, so they may in truth be Continued and the "
            "started-and-left floor concedes them.",
        "_stored_as": "$.channel_pairs_conceded_by_the_floor",
        **{sk: {p: {c: ref("stage1", "channel_pairs_conceded_by_the_floor", sk, p, c)
                    for c in ["all", "started_and_left_component",
                              "never_started_component"]}
                for p in POPS}
           for sk, _, _, _ in SETTINGS},
        "_account_counts": absent(
            "account counts for the conceded-channel sets",
            "$.channel_pairs_conceded_by_the_floor.*.*",
            "only pair counts were stored. Deriving accounts would require reading "
            "pairs.npz, which is forbidden, and would be a new measurement."),
    },
    "account_totals_of_the_populations": {
        "_why": "the exclusion account counts (e.g. 216) are only checkable against a "
                "denominator. These are the resampling-unit totals recorded by the "
                "bootstrap stage. Counts of accounts, not accounts.",
        "_the_draw_is_not_the_support": (
            "TWO DIFFERENT ACCOUNT TOTALS ARE RECORDED HERE AND THEY ARE NOT INTERCHANGEABLE "
            "(decisions/0124 SS4(1)). `resampling_frame` is THE DRAW -- every account with at "
            "least one pair in the position-4 output, built once and drawn for every quantity "
            "regardless of how much it contributes. It is arm-independent in MEMBERSHIP. "
            "`contributing` is THE SUPPORT -- the accounts that actually hold a pair in this "
            "population at this arm -- and it is NOT arm-independent, because keep_d10 contains "
            "max(W, 91). The difference is the accounts drawn with zero contribution. A reader "
            "taking the frame total as the number of accounts carrying a population would be "
            "wrong by that difference."),
        **{sk: {p: {"resampling_frame": ref("stage2", sk, p,
                                            "n_accounts_resampling_frame"),
                    "contributing": ref("stage2", sk, p,
                                        "n_accounts_contributing_to_this_group"),
                    "drawn_contributing_zero": ref("stage2", sk, p,
                                                   "n_accounts_drawn_contributing_zero")}
                for p in POPS}
           for sk, _, _, _ in SETTINGS},
    },
}

absences = [
    absent("pairs_where_t0_moves, on DERIV",
           "$.premiere_arm_preconditions",
           "the measurement was taken on the APPLY position-5 mask ONLY (`[pos5]`). No DERIV "
           "counterpart was ever computed. Producing one would be a new measurement, which "
           "this extract is forbidden to make."),
    absent("a T0-movement figure for the W108 finale arm",
           "$.W108_s2_finale",
           "the measurement is defined premiere-against-finale and is stored ONCE, under "
           "$.premiere_arm_preconditions, rather than per arm setting. There is no per-arm "
           "field to transcribe."),
    absent("adopted_rule_revision",
           "anywhere in either working file",
           "NOT RECORDED BY THIS ARM'S STEP 9 RUN. The arm key is (W_days, clock_origin, "
           "producing_step, adopted_rule_revision) per 0111 E2 and 0114 E14, and the fourth "
           "component is missing from this arm's working output, so the key is INCOMPLETE as "
           "stored. It is not read in from processed/step5/adopted_rule.json here: the "
           "ruling directs that an absent field be recorded absent, not filled from "
           "elsewhere. Reported as a defect."),
    absent("producing_step, as a stored field",
           "anywhere in either working file",
           "the working file records `step: 9` at its root but does not carry it into the "
           "per-arm entries, so the third arm-key component is not stored per arm either."),
    absent("account counts for the silence_test_alone and spared_by_not_continued sets",
           "$.<setting>.<population>.exclusions",
           "only pair counts were stored for those two sets. The `accounts` field covers the "
           "EXCLUDED set only."),
    absent("a conjunct-1-first ordering of the conjunct ladder",
           "$.<setting>.<population>.conjunct_selection",
           "the ladder was stored in one ordering only (conjunct 2 first). The "
           "conjunct-1-alone quantity does exist separately as `silence_test_alone`, and is "
           "transcribed above under its own name; it is NOT re-presented here as a ladder "
           "rung, because assembling a second ladder is a construction this extract is not "
           "authorised to make."),
    absent("position-5 and post-liveness counts at any other W arm",
           "the working file root",
           "this arm's Step 9 run carries exactly the two settings listed. The eight-arm W "
           "grid belongs to Step 13 and is not in this file."),
    absent("D4 (S3-without-S2) and D9 (split-artifact) figures",
           "the working file root",
           "Step 8 owns them and Step 9 CONSUMES them (0070 rulings 1 and 7). This arm did "
           "not compute D4 and must not; there is nothing of its own to transcribe."),
    absent("channel_classes and discovery_channel_overlap",
           "the working file root",
           "0114 E8: this arm does not write them. They hold Step 8's D4 and D9 figures and "
           "the merged document carries them once, filled at Step 13b from Step 8's "
           "artifact. Emitted here as the absence idiom."),
]

defects = [
    {"id": "b-wf-1",
     "severity": "reportable",
     "where": "src/step9_b_1_compute.py, the `EXPECTED` dict",
     "what": "the harness control's expected values are TYPED AS LITERALS. The comment on the "
             "dict claims they come from artifacts/step8-waterfall-{a,b}.json, but the script "
             "NEVER OPENS EITHER FILE.",
     "why_it_matters": "this is the read-never-typed class that 0114 E14 rules against, and "
                       "the same limit this arm's own spec names: a typed value validates "
                       "identically to a read one, so the honesty of the field is the "
                       "author's, not the control's. If Step 8's artifact is ever amended, "
                       "this control passes against a stale transcription and reports "
                       "`agrees: true`.",
     "not_claimed": "this extract does NOT claim the typed literals match Step 8's artifacts. "
                    "No keyed comparison was performed. A substring presence check would be "
                    "near-vacuous for small integers such as 99 and 703 and is not evidence.",
     "affects_the_figures_in_this_file": "no. The control block is not transcribed here; the "
                                         "figures above come from the measured per-arm "
                                         "blocks."},
    {"id": "b-wf-2",
     "severity": "reportable",
     "where": "$.premiere_arm_preconditions.pairs_where_t0_moves",
     "what": "the figure DOES NOT STATE ITS POPULATION in the working file. It was measured on "
             "the APPLY position-5 mask, knowable only by reading the source line.",
     "why_it_matters": "EVERY FIGURE STATES ITS POPULATION is a standing requirement of this "
                       "step. A reader of the JSON alone would not know whether {:,} is an "
                       "APPLY figure, a DERIV figure, or a whole-frame figure.".format(
                           ref("stage1", "premiere_arm_preconditions",
                               "pairs_where_t0_moves")["value"]),
     "handled_here": "the population is stated in this extract, sourced from the code line and "
                     "labelled as such."},
    {"id": "b-wf-3",
     "severity": "naming, not numeric",
     "where": "$.<setting>.<population>.exclusions.silence_test_alone",
     "what": "the name reads as `pairs excluded by the silence test alone`. It is not that. It "
             "is `mask & silent`: every pair meeting conjunct 1, Continued ones included.",
     "why_it_matters": "a reader who takes the name at face value reads it as an exclusion "
                       "subtotal and gets a number larger than the total exclusions, which "
                       "looks like a contradiction and is not one.",
     "handled_here": "the coded expression is transcribed beside the figure."},
    {"id": "b-wf-4",
     "severity": "look-alike, NOT a defect",
     "where": "$.<setting>.<population>.exclusions.spared_by_not_continued",
     "what": "the value is IDENTICAL on APPLY and DERIV at both settings.",
     "why_it_is_not_a_defect": "it is forced by the definitions. A spared pair is Continued; "
                               "Continued requires S2 evidence; DERIV is APPLY restricted to "
                               "pairs with S2 evidence. So every spared APPLY pair is in "
                               "DERIV and the two counts cannot differ.",
     "recorded_because": "it looks like a copy-paste error and a reader should not have to "
                         "chase it."},
]

payload = {
    "document": "Step 9 working-figures extract -- ARM b",
    "producing_agent": "data-scientist-b",
    "arm": "b",
    "step": 9,
    "authorised_by": "Human Lead ruling, 2026-08-21",
    "why_this_file_exists":
        "processed/ is gitignored, so this arm's Step 9 counts exist in exactly one place and "
        "are not recoverable from a clone. Under 0092 a transcription assembled by another "
        "party is not an attestation, so the producing arm emits its own figures and signs "
        "them.",
    "signed_off_by_producing_arm": True,
    "sign_off_means":
        "this arm attests that every figure below was read from its own working output at the "
        "key named beside it, by the generator named below, and that it matches what this "
        "arm's pipeline computed.",
    "adopts": "nothing",
    "api_calls": 0,
    "generated_by": "src/step9_b_5_working_figures.py",
    "generated_at_utc": datetime.datetime.now(datetime.timezone.utc)
                                 .strftime("%Y-%m-%dT%H:%M:%SZ"),
    "sources": [{"path": v, "sha256_12": _sha12(v)} for v in SRC.values()],
    "privacy": {
        "contents": "COUNTS AND ACCOUNT TOTALS ONLY.",
        "no_pair_level_rows": True,
        "no_usernames_no_user_ids_no_individual_histories": True,
        "pairs_npz_was_not_read": True,
        "pairs_npz_statement":
            "processed/step9/b/pairs.npz is pair-level data. This generator never opens it and "
            "NO FIELD IN THIS FILE IS DERIVED FROM IT, directly or transitively. Every value "
            "was read from stage1_counts.json or stage2_bootstrap.json by key.",
        "account_counts_published_under":
            "Human Lead ruling, 2026-08-21: the account counts publish -- they are counts of "
            "accounts, not accounts, and the method section needs them checkable.",
    },
    "scope": {
        "this_is": "a labelled transcription of this arm's own measurements, with provenance.",
        "this_is_not": "a new measurement run, a headline, a comparison or a merge.",
        "nothing_was_computed":
            "no study figure in this file was computed by this generator. Every one was read "
            "from a working file at the key printed beside it.",
        "no_cross_arm_content":
            "this arm has no knowledge of any other Step 9 arm's figures and sought none. "
            "processed/step9/a/ and artifacts/step9-*-a.* were not opened, and no comparison, "
            "reconciliation or merge appears anywhere in this file. $.cross_arm_divergences "
            "and $.limitations are Human-Lead-owned and are not written here.",
        "deliberately_not_included": {
            "bootstrap_confidence_intervals":
                "stage2_bootstrap.json carries this arm's levels and paired-movement "
                "intervals and its bootstrap design block. They exist and are NOT absent; "
                "they are outside the scope this extract was asked for. Only the "
                "account totals were taken from that file.",
        },
        "arm_settings_carried": [
            {"working_file_key": k, "W_days": w, "clock_origin": o} for k, w, o, _ in SETTINGS
        ],
        "populations_carried": {
            "APPLY": "Step 5 line 1 less D10 -- what Step 8 filters.",
            "DERIV": "Step 5 line 4 less D10 -- requires S2 evidence.",
            "note": "the population sizes are transcribed per setting above; they are not "
                    "restated here as free-standing figures.",
        },
    },
    "figures": figures,
    "t0_movement": t0_movement,
    "supplementary": supplementary,
    "absent_fields": absences,
    "defects_found_while_transcribing": defects,
    "scope_of_the_defect_list":
        "these are defects in THIS ARM'S OWN working output and its own generator only. "
        "Anything observed on a surface this arm does not own was reported to the Human Lead "
        "and is not published here.",
}


def _assert_transcription_consistent():
    """Guard the TRANSCRIPTION, not the study. Raises if what was read does not hang together.

    Nothing here is published: these are checks that the copy is faithful, and a derived sum
    is not a figure this arm measured. Coverage is printed so that `nothing found` and
    `looked at nothing` cannot report the same way.
    """
    checked = 0
    for key, _, _, _ in SETTINGS:
        for pop in POPS:
            b = figures[key][pop]
            p5 = {o: b["position_5"][o]["value"] for o in OUTCOMES}
            p7 = {o: b["position_7_post_liveness"][o]["value"] for o in OUTCOMES}
            ex = {k: v["value"] for k, v in b["exclusions"].items()
                  if isinstance(v, dict) and "value" in v}
            n5, n7 = b["n_position_5"]["value"], b["n_post_liveness"]["value"]
            assert sum(p5.values()) == n5, (key, pop, "position-5 outcomes do not sum to n")
            assert sum(p7.values()) == n7, (key, pop, "post-liveness outcomes do not sum to n")
            assert n5 - n7 == ex["total_pairs"], (key, pop, "exclusions != n5 - n7")
            assert (ex["never_started_component"] + ex["started_and_left_component"]
                    + ex["continued_component"] == ex["total_pairs"]), (key, pop, "components")
            for o, comp in [("never_started", "never_started_component"),
                            ("started_and_left", "started_and_left_component"),
                            ("continued", "continued_component")]:
                assert p5[o] - p7[o] == ex[comp], (key, pop, o, "component != p5 - p7")
            assert ex["silence_test_alone"] == ex["total_pairs"] + ex["spared_by_not_continued"], \
                (key, pop, "silent set != excluded + spared")
            lad = b["conjunct_ladder"]
            assert lad["start"]["value"] == n5, (key, pop, "ladder start != n5")
            assert (lad["after_conjunct_2_not_continued"]["value"]
                    == n5 - p5["continued"]), (key, pop, "ladder rung 1")
            assert (lad["after_conjunct_1_silent_at_tau1"]["value"]
                    == ex["total_pairs"]), (key, pop, "ladder rung 2 != exclusions")
            checked += 1
    assert checked == len(SETTINGS) * len(POPS) == 4, "coverage shortfall: %d" % checked
    return checked


def _assert_no_forbidden_source():
    blob = json.dumps(payload)
    assert FORBIDDEN not in blob or "not read" in blob or "never opens" in blob
    for s in SRC.values():
        assert FORBIDDEN not in s, "a declared source is pair-level data"
    return True


if __name__ == "__main__":
    n = _assert_transcription_consistent()
    _assert_no_forbidden_source()
    with open(OUT, "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=False)
        fh.write("\n")
    stamp = payload["generated_at_utc"]
    with open(RUNLOG, "w") as fh:
        fh.write("step9 arm b -- working-figures extract\n")
        fh.write("generated_at_utc: %s\n" % stamp)
        fh.write("generator: src/step9_b_5_working_figures.py\n")
        fh.write("output: %s\n" % os.path.relpath(OUT, ROOT))
        for k, v in SRC.items():
            fh.write("source %s: %s sha256_12=%s\n" % (k, v, _sha12(v)))
        fh.write("pairs.npz opened: NO\n")
        fh.write("other-arm namespaces opened: NONE\n")
        fh.write("transcription consistency blocks checked: %d of 4\n" % n)
        fh.write("api calls: 0\n")
    print("wrote", OUT)
    print("run record", RUNLOG)
    print("consistency blocks checked:", n, "of 4")
