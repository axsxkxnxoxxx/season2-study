#!/usr/bin/env python3
"""Step 9, arm b -- EMIT the corrected premiere-anchored figures into artifacts/.

Human Lead ruling, 2026-08-21: *STAMP, DO NOT DELETE.* The committed premiere
figures are SUPERSEDED, not withdrawn -- correctly produced under a defective
vector, and the record of what the defect produced is the evidence for the
finding. So both must exist: the marked originals at their own paths, and this
corrected emission beside them.

WHAT THIS SCRIPT DOES, AND WHAT IT REFUSES TO DO
------------------------------------------------
It PROMOTES processed/step9/b/preview/ into artifacts/ under distinct filenames
and adds, to each file, a supersession record, an arm signature and its own
provenance. It CHANGES NO MEASUREMENT. That is asserted rather than claimed: the
promoted JSON is compared leaf-for-leaf against its source and the run stops if
anything other than the added keys differs.

THE FILENAMES, and why they are these
-------------------------------------
    artifacts/step9-headline-corrected-2026-08-21-b.json
    artifacts/step9-headline-corrected-2026-08-21-b.md
    artifacts/step9-working-figures-corrected-2026-08-21-b.json

1. They are DISTINCT from the committed paths, so the marked originals keep
   theirs and the two are readable side by side. That is the ruling's own
   requirement.
2. The ARM TOKEN STAYS LAST. This arm's isolation rule (decisions/0123) requires
   every search to be scoped in the pattern itself, and names
   ``artifacts/step9-*-b.*`` as the scope. A name like
   ``step9-headline-b-corrected-...`` would fall OUTSIDE that pattern, so this
   arm's own scoped searches would silently miss its own corrected figures --
   and a filename that defeats the isolation control is a defect, not a
   cosmetic choice.
3. "corrected" plus the EMISSION DATE says what the file is without asserting
   that it is adopted. Adoption is the Human Lead's, not an arm's.

SECOND AUTHORISED RERUN, 2026-08-21 (Human Lead rulings 1 and 2 of that date).
  RULING 1. The previous corrected emission asserted that the un-re-censored row
  set had been "CHECKED rather than assumed" after the boolean that checked it was
  removed as vacuous. A claim of having checked is either TRUE or it is REMOVED,
  and softening it was excluded. This arm RECOMPUTED it: T0PRIME-ORDER now runs in
  the pipeline, raises, and is demonstrated FAILING on the defective vector. The
  claim is emitted by a script, so it was fixed in the script and the arm re-run --
  never by editing the file.
  RULING 2. This document now carries a DISTINCT INSTANCE VALUE in $.document_scope,
  so it and the file it supersedes are distinguishable. It states nothing about what
  a merge should take: that contract is Step 13b's, and Step 13b is the Human Lead's.
  The superseded file's $.document_scope is not touched.

THIRD AUTHORISED RERUN, 2026-08-23 (Human Lead rulings of that date, on decisions/0124).
  THE FRAME AND THE DRAW ORDER ARE FIXED and this arm did neither. It is rerun, and the
  emission COLLAPSES: ONE corrected file superseding the originals on BOTH grounds -- the
  premiere-clock unit error (decisions/0123) AND the frame and draw-order ruling
  (decisions/0124) -- and NOT a third generation. The reader gets two generations: the
  stamped originals, and this one emission naming both causes.
  THE FILENAMES ARE UNCHANGED, at the Human Lead's instruction. Reusing the path does not
  orphan the earlier reference, because the cross-arm diff record names that emission
  COMMIT-QUALIFIED. There is no third file and the old content at this path is not preserved
  here; git holds it.
  THE SCOPE OF THE SUPERSESSION WIDENS. Ground 1 reached the premiere arm only. Ground 2
  reaches EVERY CI in the file, including the ADOPTED W108_s2_finale arm's. That is expected
  under decisions/0124 SS5 and is REPORTED rather than left to pass as noise. Nothing else of
  the adopted arm moves, and `verify_against_previous()` below establishes that leaf by leaf
  instead of asserting it.

Run:  python3 src/step9_b_7_emit_corrected.py
"""

import datetime
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SRC_HEADLINE = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.json")
SRC_MD = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-headline-b.md")
SRC_WORKING = os.path.join(ROOT, "processed", "step9", "b", "preview", "step9-working-figures-b.json")

OUT_HEADLINE = os.path.join(ROOT, "artifacts", "step9-headline-corrected-2026-08-21-b.json")
OUT_MD = os.path.join(ROOT, "artifacts", "step9-headline-corrected-2026-08-21-b.md")
OUT_WORKING = os.path.join(ROOT, "artifacts", "step9-working-figures-corrected-2026-08-21-b.json")

SUPERSEDED_HEADLINE = "artifacts/step9-headline-b.json"
SUPERSEDED_MD = "artifacts/step9-headline-b.md"
SUPERSEDED_WORKING = "artifacts/step9-working-figures-b.json"

WHAT = ("THIS EMISSION SUPERSEDES %s, %s and %s ON TWO INDEPENDENT GROUNDS FOUND IN ONE STEP 9 "
        "PASS, and the two have DIFFERENT SCOPES. "
        "GROUND 1, decisions/0123 -- THE PREMIERE-CLOCK UNIT ERROR. It reaches the "
        "PREMIERE-ANCHORED 91-day arm and only that arm: every figure of that arm is superseded. "
        "GROUND 2, decisions/0124 -- THE RESAMPLING FRAME AND THE DRAW ORDER. It reaches EVERY "
        "CONFIDENCE INTERVAL IN THE FILE, on BOTH arms, INCLUDING the adopted W108_s2_finale "
        "arm, whose CI endpoints are therefore superseded too. "
        "NOTHING ELSE OF THE ADOPTED ARM MOVES: every point estimate, numerator, denominator, "
        "bound floor and ceiling, width, sub-interval, ceiling, three-ceiling sum, excess and "
        "pair count is not bootstrap-dependent, and each was verified unchanged leaf by leaf "
        "against the previous corrected emission. "
        "THE READER GETS TWO GENERATIONS AND NOT THREE: the stamped originals, and this one "
        "corrected emission naming both causes. It is a COLLAPSE, ruled by the Human Lead on "
        "2026-08-23, of what would otherwise have been a second supersession layer."
        % (SUPERSEDED_HEADLINE, SUPERSEDED_MD, SUPERSEDED_WORKING))

WHY_FRAME = (
    "decisions/0124 fixed the two bootstrap elements decisions/0103 and decisions/0118 had left "
    "open. THE FRAME is every account with at least one pair in the POSITION-4 output, built "
    "ONCE, and drawn for every quantity regardless of how much it contributes -- NOT the "
    "contributing subset, because accounts the censoring rule excludes are part of the "
    "population the uncertainty is about, and drawing only contributors conditions the variance "
    "on the censoring outcome and treats survivorship as fixed. THE DRAW ORDER is ONE RNG, "
    "SEEDED ONCE PER FILE, its stream consumed continuously, with every quantity evaluated "
    "against THE SAME REPLICATE SET, not re-seeded per group -- because a per-group restart "
    "pairs a between-setting movement only WITHIN a group, and Step 13 varies W across eight "
    "arms. THIS ARM DID NEITHER: it built the frame per mask, 2,422 accounts on APPLY and 2,402 "
    "on DERIV, and constructed the RNG inside the per-group function. Both of this arm's "
    "mechanisms solved the order-independence hazard and decisions/0124 SS3 records that neither "
    "was wrong and that the spec named neither; the ruling chose between them. The before and "
    "after are MEASURED, not asserted, in src/step9_b_9_frame_repro.py -- the RNG construction "
    "site is located by parsing the module and the frames are recomputed from the masks -- run "
    "record logs/step9_b_frame_repro.txt.")

WHY = ("src/step9_b_1_compute.py converted the premiere-anchored T0 column to epoch seconds "
       "with prem.astype('int64') // 10 ** 9. The column's dtype is datetime64[us, UTC], so "
       "its integer view is MICROseconds; dividing by 10 ** 9 produced epoch-seconds / 1000 -- "
       "a 1970 date -- for every pair, in every entry, on both populations. The superseded "
       "figures were CORRECTLY COMPUTED from that vector and are kept, marked at each point of "
       "use, as the record of what the defect produced. src/step9_b_0_clock.py now reads the "
       "resolution off the dtype and cross-checks the cast elementwise; an unrecognised "
       "resolution is a hard stop, not a default.")

SIGNATURE = ("SIGNED OFF BY THE PRODUCING ARM. This arm attests that every figure in this file "
             "was produced by its own pipeline at the settings recorded beside it, and that "
             "this emission is byte-identical in every measurement to "
             "processed/step9/b/preview/, which is what this arm's corrected run wrote. No "
             "figure in this file was hand-entered and none was edited after emission.")

DOCUMENT_INSTANCE = "step9-b-corrected-2026-08-21"

NOT_A_SECOND_ARM = (
    "THIS IS NOT A SECOND ARM FILE. It is arm b's corrected emission of arm b's own document, "
    "and $.document_scope.arm is 'b' in both it and the file it supersedes. A merge that globbed "
    "artifacts/step9-headline-*.json on the arm field alone would pick up BOTH and could read "
    "them as two arms. THIS DOCUMENT THEREFORE CARRIES A DISTINCT INSTANCE VALUE -- "
    "'DOCUMENT INSTANCE: " + DOCUMENT_INSTANCE + "', at $.document_scope.note -- so the "
    "superseded file and this one are DISTINGUISHABLE rather than interchangeable. THAT IS ALL "
    "IT DOES: it makes the two tellable apart and states nothing about which a merge takes. "
    "The merge's input contract is Step 13b's, and Step 13b is the Human Lead's; an arm does "
    "not decide what the merge reads. Human Lead ruling 2, 2026-08-21.")

WHERE_THE_INSTANCE_VALUE_LIVES = (
    "$.document_scope carries additionalProperties: false in "
    "artifacts/step8b-output-schema.json, and its permitted keys are role, producing_step, arm, "
    "merge, also_written_by_steps, isolation_rule, note and source. A NEW KEY WOULD FAIL THE "
    "SCHEMA, and the schema is Step 8b's rather than this arm's to widen, so the instance value "
    "is carried in the permitted free-text slot -- $.document_scope.note -- with a fixed leading "
    "token 'DOCUMENT INSTANCE: ' so it can be matched exactly rather than read out of prose. "
    "REPORTED as a constraint this emission worked within, not as a preference.")

RESOLVED_IN_THIS_EMISSION = {
    "b-boot-1": (
        "THE RESAMPLING FRAME AND THE DRAW ORDER, corrected under decisions/0124. " + WHY_FRAME +
        " WHAT MOVED: the CI endpoints, and only the CI endpoints. All 24 intervals in this "
        "file moved -- 48 endpoints -- including the adopted W108_s2_finale arm's, which is "
        "expected under a ruling that changes the draw for every quantity in the file and is "
        "REPORTED here rather than left to pass as noise. Verified leaf by leaf against the "
        "previous corrected emission: the counts are in $.notes."
        "step9_b_leaf_verification_of_this_emission."),
    "b-md-1": (
        "A TYPED COUNT IN THE .md, NOW MEASURED. src/step9_b_4_md.py asserted 'Six of the twelve "
        "movements this arm measured have negative endpoints' as a literal. It was true of the "
        "figures it described but could not follow them if they moved -- and decisions/0124 "
        "moved every movement endpoint in this file, which is exactly the case the defect was "
        "reserved for. The sentence now COUNTS the negative-endpoint movements off the emitted "
        "$.declared_intervals rather than asserting a number, and says that it does. It was "
        "carried as open in the previous emission because an arm does not widen the scope of an "
        "authorised rerun on its own; this rerun is the one that moves the figures the sentence "
        "describes."),
    "b-emit-1": (
        "A WARRANT THIS EMISSION NOW CARRIES. The previous corrected emission stated, at "
        "$.arms[1].note and in section 9 of the .md, that the un-re-censored row set was "
        "'CHECKED rather than assumed: T0 prime <= T0 holds for every pair' -- after the boolean "
        "that checked it, t0_is_earlier_or_equal_for_every_pair, had been removed as vacuous. A "
        "CLAIM OF HAVING CHECKED IS EITHER TRUE OR IT IS REMOVED, so on the Human Lead's ruling "
        "of 2026-08-21 this arm RECOMPUTED IT rather than softening the sentence. The check is "
        "T0PRIME-ORDER, src/step9_b_0_clock.py::verify_t0_prime_order; it runs in this "
        "pipeline, it RAISES, and the sentence now names it, states what each part compares and "
        "gives its coverage. IT IS NOT THE REMOVED BOOLEAN RESTORED: the bare inequality is true "
        "for the wrong reason on a collapsed T0' and cannot fail, so part 1 reconstructs T0' "
        "from the frame's own date STRINGS, which the epoch conversion never touches. "
        "DEMONSTRATED FAILING ON THE DEFECTIVE VECTOR at logs/step9_b_premiere_clock_repro.txt "
        "section 5 -- part 1 rejects it on 155,556 of 278,452 pairs, while part 2 run alone on "
        "that same vector passes, which is the whole of the case that part 1 is what makes the "
        "replacement failable. NO FIGURE IN THIS EMISSION MOVED: the recomputation added a "
        "check and rewrote three prose fields, and every numeric leaf is unchanged."),
}

OPEN_DEFECTS = {
    "b-stamp-1": (
        "THE STAMPS ON THE SUPERSEDED ORIGINALS NAME ONE GROUND AND THERE ARE NOW TWO. "
        "src/step9_b_6_stamp_superseded.py marked the premiere-anchored arm of " +
        SUPERSEDED_HEADLINE + " and its two companions, and recorded that the adopted "
        "W108_s2_finale arm was NOT superseded. Under decisions/0124 the adopted arm's CI "
        "ENDPOINTS in those files are superseded too, on the second ground, and their stamps do "
        "not say so. THIS EMISSION DOES NOT FIX IT: the stamped originals were ruled SETTLED by "
        "the Human Lead on 2026-08-23 and this arm does not touch them; and a deliverable is "
        "corrected by rerunning its producing arm, never by hand-editing a sentence into it. "
        "REPORTED rather than repaired, and reported HERE because this file is where a reader "
        "of those originals is sent. It moves no number in this emission."),
    "how_to_read_these": (
        "This arm's own defects in this arm's own files, published with the figures rather "
        "than held back. It moves no number in this emission."),
}


# =============================================================================================
# THE LEAF-BY-LEAF VERIFICATION THAT ONLY THE INTERVALS MOVED
# =============================================================================================
# decisions/0124 SS5: "What moves in a rerun: the CI endpoints only. Every point estimate,
# numerator, denominator, bound, width, ceiling, sum and pair count is not bootstrap-dependent
# and does not move." THAT IS A CLAIM ABOUT THIS FILE AND IT IS CHECKED HERE RATHER THAN
# ASSERTED: this emission is compared, leaf for leaf, against the emission it replaces at the
# same path.
#
# TWO CLASSES OF NUMERIC LEAF MAY MOVE AND NO OTHER.
#   A. A CI ENDPOINT -- `...ci.lower` / `...ci.upper`.
#   B. A RATIO WHOSE DENOMINATOR IS A CI WIDTH -- `...ratios.<state>.value`, the
#      bound-width / account-clustered-sampling-width ratio. It is a DERIVED FIGURE OF THE
#      ENDPOINTS (CLAUDE.md, `## Derived figures`, item 4), so it moves when they do, and a
#      check that called it a stray would be wrong about its own arithmetic.
# EVERYTHING ELSE IS PROTECTED and must be identical.
#
# THE PROTECTED FAMILIES ARE NAMED AND THEIR COVERAGE IS COUNTED. A check that finds nothing
# because it looked nowhere must fail, not pass (CLAUDE.md), so each family reports how many
# leaves it actually examined and a family that matches ZERO leaves is a HARD STOP -- the
# document would then have been reorganised under the check's feet.
CI_ENDPOINT = re.compile(r"\.ci\.(lower|upper)$")
# THE PATH IS `bound_over_sampling_width_ratios`, WRITTEN OUT. A first draft of this pattern
# said `\.ratios\.` and the check HARD-STOPPED on the ten ratio leaves rather than waving them
# through as CI-derived -- which is the behaviour wanted: a classifier that does not recognise a
# path must fail loudly, not default to the permissive class.
CI_DERIVED_RATIO = re.compile(r"\.bound_over_sampling_width_ratios\.[a-z_]+\.value$")

PROTECTED_FAMILIES = {
    "point_estimates": re.compile(r"\.value_percent$"),
    "numerators": re.compile(r"\.numerator_pairs$"),
    "denominators": re.compile(r"\.(denominator_pairs|on_population_n)$"),
    "population_sizes": re.compile(r"\.(n_position_5|n_post_liveness)$"),
    "bound_endpoints": re.compile(r"\.(floor|ceiling)\.(percent|numerator_pairs)$"),
    "widths": re.compile(r"\.width_pp$"),
    "sub_interval": re.compile(r"\.conditional_sub_interval\.[a-z_]+$"),
    "three_ceiling_sum_and_excess": re.compile(r"\.(sum_percent|excess_pp|excess_pairs)$"),
    "pair_counts": re.compile(r"_pairs$"),
    "account_counts": re.compile(r"^\$.*accounts.*$"),
}


def _numeric(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def verify_against_previous(prev_path, new_doc, label, require_all_families=True,
                            extra_ci_derived=(), ignore_prefixes=()):
    """Compare this emission against the one it replaces at the same path, leaf for leaf."""
    if not os.path.exists(prev_path):
        return {"status": "NO_PREVIOUS_EMISSION_AT_THIS_PATH",
                "note": ("There is nothing at %s to compare against, so this emission's "
                         "only-the-intervals-moved claim is NOT established here. Stated rather "
                         "than passed over: an empty comparison and a clean one are the same "
                         "value, and only the check knows which it produced."
                         % os.path.relpath(prev_path, ROOT))}
    with open(prev_path, "rb") as fh:
        prev_bytes = fh.read()
    prev = json.loads(prev_bytes)
    a, b = dict(leaves(prev)), dict(leaves(new_doc))
    # A SUBTREE MAY BE EXCLUDED ONLY WHERE THIS FUNCTION IS CALLED BEFORE IT IS BUILT, and the
    # exclusion is DECLARED in the output so it cannot hide anything. The working-figures
    # comparison runs while `_emission` is still being constructed, so every one of the previous
    # file's `_emission` leaves would otherwise be reported as LOST -- 18 false losses in a field
    # whose whole purpose is to make a real loss visible. No prefix under which a FIGURE lives is
    # ever passed here.
    if ignore_prefixes:
        a = {p: v for p, v in a.items() if not any(p.startswith(x) for x in ignore_prefixes)}
        b = {p: v for p, v in b.items() if not any(p.startswith(x) for x in ignore_prefixes)}
    common = [p for p in a if p in b]

    ci_rx = [CI_ENDPOINT, CI_DERIVED_RATIO] + [re.compile(x) for x in extra_ci_derived]

    def is_ci(p):
        return any(rx.search(p) for rx in ci_rx)

    num_common = [p for p in common if _numeric(a[p]) and _numeric(b[p])]
    moved_num = [p for p in num_common if a[p] != b[p]]
    endpoints = [p for p in moved_num if CI_ENDPOINT.search(p)]
    derived = [p for p in moved_num if is_ci(p) and not CI_ENDPOINT.search(p)]
    stray = [p for p in moved_num if not is_ci(p)]

    families = {}
    empty_families = []
    for name, rx in PROTECTED_FAMILIES.items():
        hits = [p for p in num_common if rx.search(p) and not is_ci(p)]
        fam_moved = [p for p in hits if a[p] != b[p]]
        families[name] = {"leaves_examined": len(hits), "leaves_moved": len(fam_moved),
                          "moved_paths": sorted(fam_moved)[:10]}
        if not hits:
            empty_families.append(name)
            if require_all_families:
                sys.exit("HARD STOP: %s -- protected family %r matched ZERO leaves. A family "
                         "that looks at nothing reports the same value as one that finds "
                         "nothing, and this check must not pass by looking nowhere."
                         % (label, name))
    if len(empty_families) == len(PROTECTED_FAMILIES):
        sys.exit("HARD STOP: %s -- EVERY protected family matched zero leaves. The check looked "
                 "at nothing and would have reported clean." % label)

    if stray:
        sys.exit("HARD STOP: %s -- %d numeric leaf/leaves moved that are neither a CI endpoint "
                 "nor a ratio derived from one. decisions/0124 SS5 says the CI endpoints ONLY "
                 "move in this rerun; anything else means the ruling changed more than an "
                 "interval. Paths: %s" % (label, len(stray), stray[:10]))

    moved_str = [p for p in common if isinstance(a[p], str) and a[p] != b[p]]
    # LEAVES THAT EXIST IN ONE FILE AND NOT THE OTHER ARE NOT "UNCHANGED", AND A COMPARISON THAT
    # ONLY WALKS THE INTERSECTION CANNOT SEE THEM. They are counted and listed, because a figure
    # that disappears is as much a movement as one that changes value.
    lost = sorted(p for p in a if p not in b)
    added = sorted(p for p in b if p not in a)
    return {
        "status": "VERIFIED",
        "compared_against": os.path.relpath(prev_path, ROOT),
        "compared_against_sha256_12": sha12_bytes(prev_bytes),
        # `generated_by` is an OBJECT in the headline and a STRING in the working-figures
        # extract. Read defensively rather than assuming one shape: a crash here would leave the
        # headline written and the other two files not, which is exactly the half-emitted state
        # this promotion must never produce.
        "compared_against_generated_at_utc":
            (prev.get("generated_by") or {}).get("generated_at_utc")
            if isinstance(prev.get("generated_by"), dict) else None,
        "leaves_in_previous": len(a),
        "leaves_in_this_emission": len(b),
        "leaves_compared": len(common),
        "numeric_leaves_compared": len(num_common),
        "numeric_leaves_moved": len(moved_num),
        "moved_that_are_ci_endpoints": len(endpoints),
        "moved_that_are_ratios_derived_from_a_ci_width": len(derived),
        "moved_that_are_neither": len(stray),
        "every_moved_numeric_leaf_is_a_ci_endpoint_or_derived_from_one": not stray,
        "protected_families": families,
        "protected_families_matching_no_leaf_in_this_document": empty_families,
        "protected_families_matching_no_leaf_note": (
            "NAMED, NOT PASSED OVER. A family with no leaf in this document is a family this "
            "document does not carry -- the working-figures extract holds a different selection "
            "of figures from the headline -- and it is listed so the coverage is readable rather "
            "than inferred from a total. Every family matching zero would be a hard stop."),
        "protected_numeric_leaves_examined":
            sum(f["leaves_examined"] for f in families.values()),
        "protected_numeric_leaves_moved": sum(f["leaves_moved"] for f in families.values()),
        "string_leaves_moved": len(moved_str),
        "string_leaves_moved_paths": sorted(moved_str),
        "leaves_present_in_the_previous_emission_and_absent_here": len(lost),
        "leaves_present_here_and_absent_from_the_previous_emission": len(added),
        "subtrees_excluded_from_this_comparison": list(ignore_prefixes),
        "subtrees_excluded_why": (
            "DECLARED, not silent. A subtree is excluded only where this check runs before that "
            "subtree is built -- the working-figures `_emission` block -- so its leaves would "
            "otherwise be counted as losses that did not happen. No prefix under which a FIGURE "
            "lives is excluded."
            if ignore_prefixes else "None. Every leaf of both files was compared."),
        "leaves_absent_here_paths": lost,
        "leaves_added_here_numeric_paths": [p for p in added if _numeric(b[p])],
        "what_the_added_and_absent_leaves_are": (
            "A COMPARISON THAT WALKS ONLY THE INTERSECTION CANNOT SEE A FIGURE THAT DISAPPEARS, "
            "so they are counted here rather than left out. In this emission they are ONE "
            "STRUCTURAL CHANGE plus this run's own added records. THE STRUCTURAL CHANGE: "
            "`account_totals_of_the_populations.<arm>.<population>` used to hold ONE account "
            "number and now holds THREE -- `resampling_frame` (the DRAW, 2,481), `contributing` "
            "(the SUPPORT, which is the number the single slot used to hold) and "
            "`drawn_contributing_zero` (their difference). decisions/0124 SS4(1) requires it: one "
            "slot cannot carry two account totals that differ, and the old slot's value is "
            "preserved unchanged as `contributing`. NO FIGURE MOVED; a figure was disambiguated "
            "and two were added beside it."),
        "what_the_moved_strings_are": (
            "PROSE AND PROVENANCE, not figures. They are (i) interval notes and `quantity` "
            "sentences that RESTATE a CI width inside their text, which moves when the endpoint "
            "does; (ii) `denominator_definition`, which prints the account-clustered sampling "
            "width; (iii) the generator sha, timestamp and git head; and (iv) the frame and "
            "draw-order text this rerun adds at the point of use. Every numeric leaf they "
            "restate is itself in the moved-endpoint list above."),
        "not_established_here": (
            "This compares THIS FILE against ITS OWN PREVIOUS EMISSION. It says nothing about "
            "the other arm, which this arm does not see, and nothing about the stamped "
            "originals, which are settled and untouched."),
    }


def sha12_bytes(b):
    return hashlib.sha256(b).hexdigest()[:12]


def sha12(path):
    with open(path, "rb") as fh:
        return sha12_bytes(fh.read())


def leaves(obj, prefix="$"):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, prefix + "." + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, "%s[%d]" % (prefix, i))
    else:
        yield prefix, obj


def assert_only_added(src, out, allowed_prefixes, label, allowed_modified=()):
    """No measurement may move between the source and the emission.

    `allowed_modified` names, EXHAUSTIVELY AND BY PATH, the leaves this promotion is permitted to
    rewrite. It exists for one leaf -- $.document_scope.note, which carries the instance value --
    and every such leaf must additionally be ADDITIVE: the source text has to survive inside the
    new one. A path not on the list is a hard stop whether or not it holds a number, so the
    permission cannot quietly widen into a figure.
    """
    a, b = dict(leaves(src)), dict(leaves(out))
    moved = [p for p in a if p in b and a[p] != b[p]]
    stray_moved = [p for p in moved if p not in allowed_modified]
    not_additive = [p for p in moved if p in allowed_modified
                    and not (isinstance(a[p], str) and isinstance(b[p], str) and a[p] in b[p])]
    lost = [p for p in a if p not in b]
    added = [p for p in b if p not in a]
    stray = [p for p in added if not any(p.startswith(x) for x in allowed_prefixes)]
    if stray_moved or not_additive or lost or stray:
        sys.exit("HARD STOP: %s -- the emission is not its source. moved=%s not_additive=%s "
                 "lost=%s stray=%s"
                 % (label, stray_moved[:5], not_additive[:5], lost[:5], stray[:5]))
    return {"leaves_compared": len(a), "leaves_moved_outside_the_declared_list": 0,
            "leaves_lost": 0, "keys_added_by_this_promotion": len(added),
            "leaves_rewritten_by_this_promotion": sorted(moved),
            "rewrites_verified_additive": True}


def main():
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    me = sha12(os.path.abspath(__file__))
    try:
        head = subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        head = None

    report = {
        "run": "Step 9, arm b -- EMIT the corrected premiere figures",
        "recorded_at_utc": now,
        "authorised_by": "Human Lead ruling, 2026-08-21.",
        "generator": "src/step9_b_7_emit_corrected.py",
        "generator_sha256_12": me,
        "git_head_short": head,
        "adopts": "nothing",
        "api_calls": 0,
        "supersedes": WHAT,
        "why": WHY,
        "second_authorised_rerun_2026_08_21": {
            "ruling_1": "b-emit-1. RECOMPUTED, not softened and not struck. See "
                        "$.resolved_in_this_emission.",
            "ruling_2": "the instance value. See $.document_instance.",
            "figures_that_moved": "NONE. The rerun added a check and rewrote three prose "
                                  "fields in the emitted JSON; every numeric leaf, on both "
                                  "arms and in every declared interval, is unchanged.",
        },
        "third_authorised_rerun_2026_08_23": {
            "ruling": "decisions/0124 -- the resampling frame and the draw order are fixed. "
                      "This arm did neither and was obliged to rerun.",
            "publication_shape": "COLLAPSE, ruled. ONE corrected file superseding the "
                                 "originals on BOTH grounds, at the SAME PATHS, and NOT a "
                                 "third generation. The reader gets two generations: the "
                                 "stamped originals, and this emission naming both causes.",
            "figures_that_moved": "THE CI ENDPOINTS, and the ratios derived from a CI width. "
                                  "Nothing else. Established leaf by leaf against the previous "
                                  "emission at the same path -- see $.leaf_verification -- "
                                  "rather than asserted.",
            "the_adopted_arm_moved_too": "REPORTED, NOT LET PASS AS NOISE. decisions/0124 "
                                         "changes the draw for EVERY quantity in the file, so "
                                         "the adopted W108_s2_finale arm's CI endpoints move "
                                         "as well as the premiere arm's. That is expected "
                                         "under decisions/0124 SS5 and it is not a defect.",
            "what_this_arm_did_before": WHY_FRAME,
        },
        "resolved_in_this_emission": RESOLVED_IN_THIS_EMISSION,
        "open_in_this_emission": OPEN_DEFECTS,
        "filenames_and_why": {
            "headline_json": "artifacts/step9-headline-corrected-2026-08-21-b.json",
            "headline_md": "artifacts/step9-headline-corrected-2026-08-21-b.md",
            "working_figures_json": "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
            "distinct_paths": "so the marked originals keep theirs and both are readable side by side",
            "arm_token_last": ("this arm's isolation rule names artifacts/step9-*-b.* as its "
                               "search scope; a name with the arm token in the middle would "
                               "fall outside it, and a filename that defeats the isolation "
                               "control is a defect"),
            "corrected_plus_date": "says what the file is without asserting that it is adopted",
        },
    }

    # ---- headline JSON -----------------------------------------------------
    src_bytes = open(SRC_HEADLINE, "rb").read()
    doc = json.loads(src_bytes)
    src_doc = json.loads(src_bytes)

    notes = doc["notes"]
    notes["step9_b_this_emission_supersedes"] = WHAT
    notes["step9_b_why_it_supersedes"] = WHY
    notes["step9_b_emission_provenance"] = (
        "PROMOTED from processed/step9/b/preview/step9-headline-b.json (sha256:12 %s) into "
        "artifacts/ by src/step9_b_7_emit_corrected.py (sha256:12 %s) at %s, git %s. The "
        "promotion added the $.notes keys prefixed step9_b_this_emission / "
        "step9_b_why_it_supersedes / step9_b_emission / step9_b_arm_signature / "
        "step9_b_not_a_second_arm_file / step9_b_where_the_instance_value_lives / "
        "step9_b_open_defect_ / step9_b_resolved_defect_, and REWROTE EXACTLY ONE EXISTING "
        "LEAF -- $.document_scope.note, to carry this document's instance value, additively, "
        "with the source text surviving inside the new one and the addition asserted to be "
        "additive. NOTHING ELSE CHANGED; every measurement is leaf-for-leaf identical to that "
        "source and the promotion asserts it numerically rather than claiming it. "
        "$.generated_by still names the generator that computed the figures, which is not "
        "this script."
        % (sha12_bytes(src_bytes), me, now, head))
    notes["step9_b_arm_signature"] = SIGNATURE
    notes["step9_b_not_a_second_arm_file"] = NOT_A_SECOND_ARM
    notes["step9_b_where_the_instance_value_lives"] = WHERE_THE_INSTANCE_VALUE_LIVES
    notes["step9_b_why_it_supersedes_ground_2_frame_and_draw_order"] = WHY_FRAME

    # THE LEAF-BY-LEAF VERIFICATION, TAKEN BEFORE THIS FILE OVERWRITES ITS PREDECESSOR AT THE
    # SAME PATH. It must run here, against OUT_HEADLINE as it currently stands on disk, because
    # after the write the predecessor is gone.
    leafver = verify_against_previous(OUT_HEADLINE, doc, "headline JSON")
    report["leaf_verification"] = {"headline_json": leafver}
    notes["step9_b_leaf_verification_of_this_emission"] = (
        "decisions/0124 SS5 says the CI ENDPOINTS ONLY move in this rerun. THAT IS CHECKED HERE, "
        "NOT ASSERTED: this emission was compared leaf for leaf against the emission it replaces "
        "at this same path (%s, sha256:12 %s, generated %s). %d leaves compared, of which %d are "
        "numeric; %d numeric leaves moved -- %d CI endpoints and %d ratios whose DENOMINATOR is "
        "an account-clustered CI width and which therefore move with the endpoints by "
        "construction (CLAUDE.md, derived figures, item 4). %d moved that are neither, and a "
        "single one would have been a hard stop. %d protected numeric leaves were examined "
        "across %d named families -- point estimates, numerators, denominators, population "
        "sizes, bound floors and ceilings, widths, the conditional sub-interval, the "
        "three-ceiling sum and its excess, pair counts and account counts -- and %d of them "
        "moved; a family matching zero leaves is a hard stop, so the check cannot pass by "
        "looking nowhere. %d string leaves moved: interval notes and `quantity` sentences that "
        "restate a width, `denominator_definition`, the frame and draw-order text added at the "
        "point of use, and the generator sha, timestamp and git head."
        % (leafver.get("compared_against"), leafver.get("compared_against_sha256_12"),
           leafver.get("compared_against_generated_at_utc"),
           leafver.get("leaves_compared", 0), leafver.get("numeric_leaves_compared", 0),
           leafver.get("numeric_leaves_moved", 0),
           leafver.get("moved_that_are_ci_endpoints", 0),
           leafver.get("moved_that_are_ratios_derived_from_a_ci_width", 0),
           leafver.get("moved_that_are_neither", 0),
           leafver.get("protected_numeric_leaves_examined", 0),
           len(leafver.get("protected_families", {})),
           leafver.get("protected_numeric_leaves_moved", 0),
           leafver.get("string_leaves_moved", 0))
        if leafver.get("status") == "VERIFIED" else
        "NOT ESTABLISHED. " + leafver.get("note", ""))
    notes["step9_b_the_adopted_arm_moved_too"] = (
        "STATED RATHER THAN LEFT TO PASS AS NOISE. decisions/0124 changes the DRAW for every "
        "quantity in this file, so the ADOPTED W108_s2_finale arm's CI endpoints move as well "
        "as the premiere arm's. That is expected under decisions/0124 SS5 -- which scopes the "
        "rerun at 12 level intervals and 12 paired movements, 48 endpoints, across 2 arm "
        "settings x 2 populations x 3 states -- and it is NOT a defect. NOTHING ELSE OF THE "
        "ADOPTED ARM MOVES, and $.notes.step9_b_leaf_verification_of_this_emission gives the "
        "counts that establish it.")
    for k, v in OPEN_DEFECTS.items():
        notes["step9_b_open_defect_" + k.replace("-", "_")] = v
    for k, v in RESOLVED_IN_THIS_EMISSION.items():
        notes["step9_b_resolved_defect_" + k.replace("-", "_")] = v

    # THE INSTANCE VALUE. It names THIS document as the corrected instance and does nothing
    # else: it makes the superseded file and this one distinguishable, and says nothing about
    # which a merge takes. $.document_scope forbids additional properties, so it goes in the
    # permitted `note` slot behind a fixed token, APPENDED rather than substituted.
    doc["document_scope"]["note"] = (
        "DOCUMENT INSTANCE: " + DOCUMENT_INSTANCE + ". This document is arm b's CORRECTED "
        "emission of arm b's own Step 9 document, superseding the premiere-anchored arm of "
        + SUPERSEDED_HEADLINE + ". The value is here so the two are distinguishable; what is "
        "done with that is the Human Lead's, at Step 13b. " + doc["document_scope"]["note"])

    report["headline_json"] = assert_only_added(
        src_doc, doc, ("$.notes.step9_b_this_emission", "$.notes.step9_b_why_it_supersedes",
                       "$.notes.step9_b_emission", "$.notes.step9_b_arm_signature",
                       "$.notes.step9_b_not_a_second_arm_file",
                       "$.notes.step9_b_where_the_instance_value_lives",
                       "$.notes.step9_b_leaf_verification_of_this_emission",
                       "$.notes.step9_b_the_adopted_arm_moved_too",
                       "$.notes.step9_b_open_defect_",
                       "$.notes.step9_b_resolved_defect_"), "headline JSON",
        allowed_modified=("$.document_scope.note",))
    report["document_instance"] = {
        "value": DOCUMENT_INSTANCE,
        "where": "$.document_scope.note, behind the fixed token 'DOCUMENT INSTANCE: '",
        "why_not_a_new_key": WHERE_THE_INSTANCE_VALUE_LIVES,
        "what_it_does_not_do": "it states nothing about which file a merge takes; the merge's "
                               "input contract is Step 13b's and Step 13b is the Human Lead's",
        "superseded_file_untouched": True,
    }
    # NOT WRITTEN HERE. Every file is written at the END, after every verification on every file
    # has passed -- see `pending` below. A first run of this build crashed between the headline
    # write and the working-figures verification and left ONE of the three files replaced,
    # which also destroys the comparison the next run depends on, because each file is verified
    # against ITS OWN PREDECESSOR AT ITS OWN PATH. A half-emitted set is worse than no emission.
    pending = []
    pending.append((OUT_HEADLINE, json.dumps(doc, indent=2, ensure_ascii=False) + "\n"))
    report["headline_json"]["source_sha256_12"] = sha12_bytes(src_bytes)

    # ---- working-figures JSON ---------------------------------------------
    wsrc_bytes = open(SRC_WORKING, "rb").read()
    wdoc = json.loads(wsrc_bytes)
    wsrc = json.loads(wsrc_bytes)
    wdoc["_emission"] = {
        "document": "Step 9 working-figures extract -- ARM b -- CORRECTED EMISSION",
        "document_instance": DOCUMENT_INSTANCE,
        "document_instance_note": NOT_A_SECOND_ARM,
        "supersedes": SUPERSEDED_WORKING,
        "what_it_supersedes": WHAT,
        "why": WHY,
        "why_ground_2_frame_and_draw_order": WHY_FRAME,
        # The working-figures extract carries a DIFFERENT SELECTION of figures from the
        # headline, so a family with no leaf here is named rather than treated as a hard stop;
        # every family matching zero still is one. Its transcribed interval endpoints do not sit
        # under a `ci` object, so their path shape is declared explicitly instead of being
        # smuggled in as a stray.
        "leaf_verification_against_the_previous_emission_at_this_path":
            verify_against_previous(
                OUT_WORKING, wdoc, "working-figures JSON", require_all_families=False,
                extra_ci_derived=(r"\.(levels_post_liveness_pct|levels_position_5_pct|"
                                  r"paired_movements_pp)\.[a-z_]+\.(lower|upper|width_pp)$",
                                  r"\.sampling_width[a-z_]*$",
                                  r"_ratio[a-z_]*$"),
                ignore_prefixes=("$._emission",)),
        "arm_signature": SIGNATURE,
        "promoted_from": "processed/step9/b/preview/step9-working-figures-b.json",
        "promoted_from_sha256_12": sha12_bytes(wsrc_bytes),
        "promoted_by": "src/step9_b_7_emit_corrected.py",
        "promoted_by_sha256_12": me,
        "promoted_at_utc": now,
        "git_head_short": head,
        "promotion_changed_no_measurement": (
            "asserted numerically, not claimed: every leaf of the source is present here with "
            "the same value, and the only added key is this one."),
        "open_defects_in_this_emission": OPEN_DEFECTS,
        "resolved_in_this_emission": RESOLVED_IN_THIS_EMISSION,
        "privacy": "COUNTS AND ACCOUNT TOTALS ONLY. processed/step9/b/pairs.npz was not read.",
    }
    report["working_json"] = assert_only_added(wsrc, wdoc, ("$._emission",),
                                               "working-figures JSON")
    pending.append((OUT_WORKING, json.dumps(wdoc, indent=2, ensure_ascii=False) + "\n"))
    report["working_json"]["source_sha256_12"] = sha12_bytes(wsrc_bytes)

    # ---- headline .md ------------------------------------------------------
    md_bytes = open(SRC_MD, "rb").read()
    md = md_bytes.decode()
    header = "\n".join([
        "> **CORRECTED EMISSION. ARM `b`.** This file supersedes `" + SUPERSEDED_MD + "` **on "
        "two independent grounds found in one Step 9 pass**, and the two have **different "
        "scopes**. There are **two generations and not three**: the stamped originals, and this "
        "one emission naming both causes.",
        "",
        "> **Ground 1 — `decisions/0123`, the premiere-clock unit error.** It reaches the "
        "**premiere-anchored 91-day arm and only that arm**, where every figure is superseded. "
        "`src/step9_b_1_compute.py` converted the premiere-anchored `T0` column to epoch seconds "
        "with `// 10 ** 9` against a `datetime64[us, UTC]` dtype, so every value was "
        "epoch-**seconds ÷ 1000** — a 1970 date. The superseded figures were correctly computed "
        "from that vector and are **kept and marked at each point of use** in the file above, "
        "because the record of what the defect produced is the evidence for the finding.",
        "",
        "> **Ground 2 — `decisions/0124`, the resampling frame and the draw order.** It reaches "
        "**every confidence interval in this file, on both arms, including the adopted "
        "`W108_s2_finale` arm**, whose CI endpoints are therefore superseded too. " + WHY_FRAME,
        "",
        "> **What moved, and what did not.** **The CI endpoints, and the ratios whose "
        "denominator is a CI width. Nothing else.** Every point estimate, numerator, "
        "denominator, bound floor and ceiling, width, sub-interval, ceiling, three-ceiling sum, "
        "excess and pair count is **not bootstrap-dependent** and is **unchanged**. That is "
        "**established leaf by leaf** against the previous emission at this path, not asserted; "
        "the counts are in the JSON half at "
        "`$.notes.step9_b_leaf_verification_of_this_emission`. **The adopted arm moving is "
        "expected under `decisions/0124` §5 and is reported rather than left to pass as noise.**",
        "",
        "> **Provenance.** Promoted from `processed/step9/b/preview/step9-headline-b.md` "
        "(sha256:12 `" + sha12_bytes(md_bytes) + "`) by "
        "`src/step9_b_7_emit_corrected.py` (sha256:12 `" + me + "`) at " + now +
        ", git `" + str(head) + "`. **The promotion appended this header and section 10 and "
        "changed no figure and no sentence of the body.** The body itself was regenerated by "
        "this arm's pipeline under `decisions/0124`; it was not edited.",
        "",
        "> **" + SIGNATURE + "**",
        "",
        "> **Document instance:** `" + DOCUMENT_INSTANCE + "`. " + NOT_A_SECOND_ARM,
        "",
        "> **Where that value lives in the JSON half.** " + WHERE_THE_INSTANCE_VALUE_LIVES,
        "",
        "---",
        "",
    ])
    lines = md.split("\n")
    # After the title line, so the document still opens with its own heading.
    out_md = "\n".join([lines[0], ""] + header.split("\n") + lines[1:])
    out_md += "\n".join([
        "",
        "## 10. Defects in this emission, found by this arm",
        "",
        "**None of them moves a number in this file.** They are published with the figures "
        "rather than held back.",
        "",
        "### Open",
        "",
    ] + ["- **`%s`.** %s\n" % (k, v) for k, v in sorted(OPEN_DEFECTS.items())
         if k != "how_to_read_these"] + [
        "### Resolved in this emission",
        "",
    ] + ["- **`%s`.** %s\n" % (k, v) for k, v in sorted(RESOLVED_IN_THIS_EMISSION.items())] + [
        "",
    ])
    # The body must survive verbatim. The title is lifted above the header, so
    # the check is made in two pieces rather than one.
    title, body = lines[0], "\n".join(lines[1:])
    if title not in out_md or body.strip() not in out_md:
        sys.exit("HARD STOP: the promoted .md does not contain its source body verbatim.")

    pending.append((OUT_MD, out_md))

    # ---- ALL THREE FILES, WRITTEN ONLY NOW ---------------------------------
    # Every verification on every file has passed. Nothing above this line touched artifacts/.
    for path, payload in pending:
        with open(path, "w") as fh:
            fh.write(payload)
    report["emission_is_all_or_nothing"] = {
        "files_written": [os.path.relpath(p, ROOT) for p, _ in pending],
        "why": ("Every file is written after EVERY verification on EVERY file has passed. A "
                "crash between two writes leaves one of the three replaced and the other two "
                "not -- and because each file is verified against ITS OWN PREDECESSOR AT ITS "
                "OWN PATH, it also destroys the comparison the next run depends on. This "
                "happened once on this build and is what the ordering now prevents."),
    }
    report["headline_json"]["emitted_sha256_12"] = sha12(OUT_HEADLINE)
    report["working_json"]["emitted_sha256_12"] = sha12(OUT_WORKING)

    report["headline_md"] = {
        "source_sha256_12": sha12_bytes(md_bytes),
        "emitted_sha256_12": sha12(OUT_MD),
        "source_body_preserved_verbatim": True,
        "added": "a provenance/supersession header after the title, and section 10.",
    }

    out = os.path.join(ROOT, "logs", "step9_b_emit_corrected_run.json")
    with open(out, "w") as fh:
        json.dump(report, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps(report, indent=1, ensure_ascii=False))
    print("\nrun record: logs/step9_b_emit_corrected_run.json")


if __name__ == "__main__":
    main()
