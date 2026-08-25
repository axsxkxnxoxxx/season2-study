"""Step 9, arm `b`, stage 3: write the arm file into Step 8b's schema.

NO CONVERSION LAYER. Every figure is written into the schema's own shapes; nothing
is emitted in a private shape and translated. Adopts nothing. Zero API calls.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = "/Users/alyanashantel/Documents/season2-study"
sys.path.insert(0, os.path.join(ROOT, "src"))
import step8b_schema as G                                              # noqa: E402

WORK = os.path.join(ROOT, "processed/step9/b")
SCHEMA = os.path.join(ROOT, "artifacts/step8b-output-schema.json")
TEMPLATE = os.path.join(ROOT, "artifacts/step8b-placeholder-arm-file.json")

ARM = "b"
STEP = "step9"
# BUMPED for the 2026-08-25 authorised emission (Human Lead rulings 1-3 of that date). A build
# tag that stays put while the emission changes is the defect decisions/0127 SS4 flagged: the
# generated stamp advances and the tag does not, so two different documents claim one build.
BUILD_TAG = "step9/b/2026-08-25"
ME = "src/step9_b_3_emit.py"

s1 = json.load(open(os.path.join(WORK, "stage1_counts.json")))
s2 = json.load(open(os.path.join(WORK, "stage2_bootstrap.json")))
tpl = json.load(open(TEMPLATE))
schema = json.load(open(SCHEMA))

w8a = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-a.json")))
w8b = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-b.json")))

B, SEED = 10000, 20260818
# THE FRAME AND THE DRAW ORDER ARE READ FROM THE STAGE THAT DREW THEM, NEVER TYPED HERE. A typed
# 2481 or a typed digest would be a second definition of what the bootstrap actually did, and it
# would go stale silently the first time the frame moved. NO DEFAULT: a missing key is a hard
# stop, because an absent frame declaration and a declared one are not the same record.
BOOT_DESIGN = s2["design"]
for _k in ("resampling_frame", "resampling_frame_n", "draw_order",
           "replicate_set_digest_sha256_12", "quantities_sharing_the_replicate_set"):
    if _k not in BOOT_DESIGN:
        raise SystemExit("HARD STOP: stage2_bootstrap.json carries no `%s`. decisions/0124 "
                         "fixes the frame and the draw order, and a file that cannot state "
                         "them at the point of use must not be emitted." % _k)
REF = "b_default"


# ---------------------------------------------------------------------------------------------
# THE POPULATION SIZES ARE READ FROM STEP 8'S APPROVED ARTIFACTS, NEVER TYPED HERE.
#
# Human Lead ruling 3, 2026-08-25. These two figures were `NPOP = {"APPLY": 196654, "DERIV":
# 147370}` -- a literal, eight lines above a block that already reads the adopted-rule revision
# rather than typing it. A RECONSTRUCTION THAT AGREES TODAY IS A SECOND DEFINITION TOMORROW, and
# a hardcoded 196,654 is a second definition of STEP 8's figure sitting inside this arm
# (decisions/0123 SS6d). `waterfall_block()` below already reads the whole waterfall out of
# `w8b`, in this same process, so the figure was available by read the entire time.
#
# AND THE CHECK IS ONE THAT CAN FAIL ON THE VECTOR IT POLICES (decisions/0123 SS3). A range test
# -- "is it a plausible pair count" -- would pass on any number of the right magnitude and could
# not tell 196,654 from 196,645. THIS IS SET MEMBERSHIP AGAINST THE SOURCE: the value is taken
# from Step 8 arm b's waterfall and required to equal Step 8 arm a's, at the same position, on
# the same population. The two are independent implementations of one gate, so a disagreement is
# reachable; src/step9_b_19_ruling_repro.py drives this function to failure and shows it naming
# the disagreement. A MISSING POSITION, A DUPLICATED ONE OR A MISSING KEY IS A HARD STOP, NEVER
# A DEFAULT.
# ---------------------------------------------------------------------------------------------
_W8A_POSITION_KEY = {5: "position_5_right_censoring", 6: "position_6_liveness",
                     7: "position_7_outcome_assignment"}


def step8_population(pop, position, _w8a=None, _w8b=None):
    """One waterfall position's retained-pair count, READ from both Step 8 arms and agreed."""
    src_b = (_w8b if _w8b is not None else w8b)
    src_a = (_w8a if _w8a is not None else w8a)
    key = "waterfall_APPLY" if pop == "APPLY" else "waterfall_DERIV"
    if key not in src_b:
        raise SystemExit("HARD STOP: artifacts/step8-waterfall-b.json carries no %r. The "
                         "population sizes are READ from Step 8, and an absent source is a "
                         "hard stop, not a reason to type the figure here." % key)
    rows = [r for r in src_b[key] if r.get("position") == position]
    if len(rows) != 1:
        raise SystemExit("HARD STOP: %s carries %d rows at position %d; expected exactly one. "
                         "A population size read from an ambiguous source is not a read."
                         % (key, len(rows), position))
    val_b = rows[0]["retained_pairs"]
    akey = _W8A_POSITION_KEY.get(position)
    try:
        val_a = src_a["waterfall"][pop][akey]
    except (KeyError, TypeError):
        raise SystemExit("HARD STOP: artifacts/step8-waterfall-a.json carries no "
                         "$.waterfall.%s.%s, so the cross-arm agreement on this population "
                         "size cannot be established. AN UNAVAILABLE CHECK IS A HARD STOP."
                         % (pop, akey))
    if val_a != val_b:
        raise SystemExit("HARD STOP: STEP 8'S TWO ARMS DISAGREE on the %s population at "
                         "waterfall position %d -- arm a says %d, arm b says %d. Step 8 is an "
                         "approved gate and its arms were diffed; a disagreement here means "
                         "this arm is reading a figure that is not settled. Reported, not "
                         "reconciled: Step 9 does not choose between them."
                         % (pop, position, val_a, val_b))
    return val_b


# POSITION 5 -- the row set every bound in this file is on, and what Step 8 filters at line 6.
NPOP = {pop: step8_population(pop, 5) for pop in ("APPLY", "DERIV")}
# POSITION 7 -- the post-liveness row set. CONVERTED TO A READ ALONGSIDE NPOP although it is
# currently referenced nowhere in this file: it is the same class of object as NPOP -- a typed
# population size owned by Step 8 -- and leaving one typed literal beside a corrected one is
# leaving a second definition in place for the first consumer that reaches for it. Reported as a
# change beyond the letter of ruling 3, which named NPOP alone.
NPOST = {pop: step8_population(pop, 7) for pop in ("APPLY", "DERIV")}

# THE ARM KEY'S REVISION DIMENSION IS READ, NEVER TYPED (decisions/0114 E14). It is the same
# value as $.adopted_rule_revision.revision because it is THE SAME READ: a typed `6` here would
# be a second definition of the rule's version, and it would go stale silently the moment an
# amendment landed, because the validator checks that a writer DECLARED read_not_typed, not that
# it did.
ADOPTED_RULE_REVISION = G._read_adopted_rule_revision()["revision"]

CONSUMED = ("CONSUMED FROM STEP 8's APPROVED ARTIFACTS, not rebuilt here: Step 9 is "
            "forbidden to rebuild DERIV or to compute D4, because a reconstruction that "
            "agrees today is still a second definition tomorrow and the dual diff cannot "
            "see it (decisions/0070 rulings 1 and 7).")


def sha12(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def pct(num, den):
    return 100.0 * num / den


# ---------------------------------------------------------------------------------------------
# THE ORDERING WARRANT, NAMED WITH ITS OWN MEASUREMENT.
#
# A CLAIM OF HAVING CHECKED IS EITHER TRUE OR IT IS REMOVED. The earlier build of this file said
# the un-re-censored row set "was CHECKED rather than assumed" after the boolean that checked it
# had been removed as vacuous -- a warrant the emission no longer carried. The check now exists
# and runs in this pipeline, and the sentence NAMES IT: where it lives, what each part compares,
# how many rows it covered, and which part is the one that can fail. Every figure below is read
# out of the check's own record in stage1_counts.json; none is typed here.
# ---------------------------------------------------------------------------------------------
_T0P = s1["premiere_arm_preconditions"]["t0_prime_order_verification"]
_P1, _P2, _P3 = (_T0P["part_1_reconstruction"], _T0P["part_2_ordering"],
                 _T0P["part_3_observability"])
_T0P_WHERE = "src/step9_b_0_clock.py::verify_t0_prime_order, id T0PRIME-ORDER"
_T0P_SUMMARY = (
    "PART 1 reconstructs T0' from the frame's own s2_premiere_date STRINGS -- a source the epoch "
    "conversion never touches -- and compares it elementwise against the decoded T0' on {p1:,} "
    "pairs: {m1} mismatches. PARTS 1 AND 2 ARE ON THE FULL SCAN PAIR SET, {p1:,} pairs, which is "
    "a SUPERSET of the position-5 row sets the figures in this file are on -- {na:,} on APPLY "
    "and {nd:,} on DERIV, part 3's own coverage -- so their coverage is not an APPLY or a DERIV "
    "count and must not be "
    "read as one. PART 2 asserts T0' <= T0 elementwise on {p2:,} pairs: {v2} "
    "violations, {e:,} strictly earlier and {q:,} equal. PART 3 asserts tau2' < tau2 and "
    "tau2' <= tau_pull on the retained rows of BOTH populations -- {na:,} on APPLY and {nd:,} on "
    "DERIV, 0 violations, minimum margin {ma:.1f} days from tau2' to tau2 and {mb:.1f} days from "
    "tau2' to tau_pull on APPLY. PART 1 IS WHAT MAKES THE CHECK FAILABLE: the bare inequality is "
    "TRUE FOR THE WRONG REASON on a collapsed T0' -- max(premiere, S1 completion) is the S1 "
    "completion date for every pair when the premiere epoch decodes to 1970, and that is <= T0 "
    "unconditionally -- which is exactly what the removed boolean was. The check RAISES rather "
    "than returning a flag, and it is demonstrated FAILING on the defective vector at "
    "logs/step9_b_premiere_clock_repro.txt"
).format(p1=_P1["rows_compared"], m1=_P1["mismatches"], p2=_P2["rows_compared"],
         v2=_P2["violations"], e=_P2["pairs_strictly_earlier"], q=_P2["pairs_equal"],
         na=_P3["populations"]["APPLY"]["rows_compared"],
         nd=_P3["populations"]["DERIV"]["rows_compared"],
         ma=_P3["populations"]["APPLY"]["min_margin_days_tau2_to_tau2_prime"],
         mb=_P3["populations"]["APPLY"]["min_margin_days_tau2_prime_to_tau_pull"])

# ---------------------------------------------------------------------------------------------
# arm-level inputs
# ---------------------------------------------------------------------------------------------
ARM_SPECS = {
    "W108_s2_finale": dict(
        arm_id="W108_s2_finale__step9__r6", W=108, origin="s2_finale", primary=True,
        in_grid=True,
        origin_note=(
            "THE ADOPTED ARM. T0 = max(S2 finale air date, first-pass S1 completion date) -- "
            "the FINALE, not the premiere; premiere anchoring is withdrawn (Step 1 SS6). "
            "Never-started is read at tau1 = [[T0]] + 108 x 24h and Continued at "
            "tau2 = [[T0]] + 199 x 24h on A_H, so the two states are 108-day and 199-day "
            "statements and are not measured alike. Every boundary test is the half-open "
            "UTC-instant form watched_at < tau."),
        note=("Step 9 arm b's measurement at the adopted setting. The COUNTS on this arm are "
              "Step 8's and are consumed; the INTERVALS, the BOUNDS and the corner table are "
              "this arm's own work.")),
    "W91_s2_premiere": dict(
        arm_id="W091_s2_premiere__step9__r6", W=91, origin="s2_premiere", primary=False,
        in_grid=False,
        origin_note=(
            "THE SECOND HEADLINE, at Netflix's own 91-day reporting window, so the result is "
            "commensurable with the public argument. T0' = max(S2 PREMIERE air date, "
            "first-pass S1 completion date), because Netflix's window runs from release. THIS "
            "ARM SITS ON A DIFFERENT ORIGIN FROM THE PRIMARY HEADLINE AND THE TWO ARE NOT THE "
            "SAME MEASUREMENT AT TWO WINDOW LENGTHS. It is not the finale-anchored 91-day grid "
            "arm either, which is Step 13's and is not written in this file."),
        note=("Step 9 arm b's second headline. No step in the spec produces a waterfall, a "
              "liveness-exclusion block or an air-period retention table at a premiere-anchored "
              "arm, so those three carry the absence idiom rather than a figure invented here. "
              "The row set is the adopted arm's position-5 population and is NOT re-censored: "
              "task-sheet.md Step 9 states that both arms run on the same right-censored "
              "population, max(W, 91) + H, and T0' <= T0 for every pair, so tau2' < tau2 <= "
              "tau_pull and every retained pair is fully observable at this arm. THAT WARRANT "
              "IS CHECKED IN THIS RUN, BY T0PRIME-ORDER (%s), WHICH RAISES: %s."
              % (_T0P_WHERE, _T0P_SUMMARY))),
}


def payload(arm_key, pop):
    """One (arm, population) payload, in the schema's own shape."""
    a = s1[arm_key][pop]
    W = ARM_SPECS[arm_key]["W"]
    H = 91
    n5 = a["n_position_5"]
    n7 = a["n_post_liveness"]
    p5, p7 = a["position_5"], a["position_7"]
    exc = a["exclusions"]
    ch = s1["channel_pairs_conceded_by_the_floor"][arm_key][pop]
    ch_sal = ch["started_and_left_component"]
    ch_ns = ch["never_started_component"]
    boot = s2[arm_key][pop]
    lv = boot["levels_post_liveness_pct"]

    # ---- the three bounds, on the POSITION-5 row set --------------------------------------
    ns_floor, ns_ceil = p7["never_started"], p5["never_started"]
    sal_floor = p7["started_and_left"] - ch_sal
    sal_ceil = p7["started_and_left"] + exc["total_pairs"]
    sub_ceil = p7["started_and_left"] + exc["started_and_left_component"]
    cont_ceil = p5["continued"] + exc["total_pairs"] + ch_sal

    covered = {
        "total_pairs": exc["total_pairs"],
        "never_started_component": exc["never_started_component"],
        "started_and_left_component": exc["started_and_left_component"],
        "accounts": exc["accounts"],
        "channel_pairs_conceded_by_the_floor": ch_sal,
    }

    def endpoint(num, kind):
        return {"percent": pct(num, n5), "numerator_pairs": num, "denominator_pairs": n5,
                "population": pop, "population_n": n5, "population_label": "position 5",
                "attainable": True,
                "note": ("%s endpoint, on the POSITION-5 row set. The published shares below "
                         "are on the POST-LIVENESS row set (%d) and the two are different "
                         "populations." % (kind, n7))}

    corner_floor = {"corner": "floor",
                    "never_started_percent": pct(ns_floor, n5),
                    "started_and_left_percent": pct(sal_floor, n5),
                    "continued_percent": pct(cont_ceil, n5),
                    "note": ("every excluded pair and every conceded channel pair is in truth "
                             "Continued. A complete and consistent assignment: %d + %d + %d = "
                             "%d. It attains the never-started FLOOR, the started-and-left "
                             "FLOOR and the Continued CEILING at once."
                             % (ns_floor, sal_floor, cont_ceil, n5))}
    corner_ns_ceiling = {"corner": "ceiling",
                         "never_started_percent": pct(ns_ceil, n5),
                         "started_and_left_percent": pct(sub_ceil, n5),
                         "continued_percent": pct(p5["continued"], n5),
                         "note": ("every never-started exclusion is in truth never-started and "
                                  "every started-and-left exclusion in truth started and left; "
                                  "no channel pair is Continued. %d + %d + %d = %d."
                                  % (ns_ceil, sub_ceil, p5["continued"], n5))}
    corner_sal_ceiling = {"corner": "ceiling",
                          "never_started_percent": pct(ns_floor, n5),
                          "started_and_left_percent": pct(sal_ceil, n5),
                          "continued_percent": pct(p5["continued"], n5),
                          "note": ("every excluded pair, of both components, is in truth "
                                   "started-and-left. %d + %d + %d = %d."
                                   % (ns_floor, sal_ceil, p5["continued"], n5))}

    ns_degenerate = ns_floor == ns_ceil
    ns_bound = {
        "floor": endpoint(ns_floor, "floor"),
        "ceiling": endpoint(ns_ceil, "ceiling"),
        "width_pp": pct(ns_ceil, n5) - pct(ns_floor, n5),
        "degenerate": ns_degenerate,
        "degenerate_reason": (
            ("The never-started exclusion component is 0 on %s, so the two endpoints are one "
             "number and the width is a MEASURED ZERO, not missing data. The dual control is "
             "x = x here; the informative comparison is on APPLY." % pop)
            if ns_degenerate else None),
        "conditional_sub_interval": {
            "applicable": False, "status": "structurally_absent",
            "reason": ("The conditional sub-interval conditions on this bound's own exclusion "
                       "set, so for never-started it does not exist. The field is present and "
                       "says so: an absent field and an inapplicable one must not look alike."),
            "source": "task-sheet.md Step 8b; decisions/0066 SS3"},
        "scope_qualifier_ref": "insertion_dormancy_covering",
        "exclusions_covered": covered,
        "endpoints_attainable": True,
        "attainable_corners": [corner_floor, corner_ns_ceiling],
        "note": ("THE NEVER-STARTED FLOOR IS NOT WIDENED, although %d channel pairs on this "
                 "population are never-started, retained, NOT Continued, and have their last "
                 "insertion inside (tau1, tau2). THE REASON IS THE ANCHORING, NOT THE COUNT: "
                 "never-started is the null |A| = 0 READ AT tau1, and every one of those %d "
                 "has an insertion AFTER tau1 -- which is exactly what gate decisions/0021 "
                 "licenses. Their null is OBSERVED, not conceded. The %d started-and-left "
                 "channel pairs differ because the Continued condition they negate is read at "
                 "tau2, and they are dormant before it. The ceiling equals the unfiltered "
                 "position-5 share AS AN IDENTITY, and both endpoints are attainable."
                 % (ch_ns, ch_ns, ch_sal))}

    sal_bound = {
        "floor": endpoint(sal_floor, "floor, WIDENED"),
        "ceiling": endpoint(sal_ceil, "ceiling"),
        "width_pp": pct(sal_ceil, n5) - pct(sal_floor, n5),
        "degenerate": False,
        "degenerate_reason": None,
        "conditional_sub_interval": {
            "applicable": True,
            "floor": endpoint(sal_floor, "sub-interval floor, WIDENED"),
            "ceiling": endpoint(sub_ceil, "sub-interval ceiling"),
            "width_pp": pct(sub_ceil, n5) - pct(sal_floor, n5),
            "conditioning_text": (
                "The started-and-left share GIVEN that every never-started exclusion is a true "
                "decline. It is a LABELLED CONDITIONAL SUB-INTERVAL and never the bound: the "
                "never-started exclusions rest on an untrusted |A| = 0 and some may in truth "
                "have left, so a ceiling taken over the started-and-left exclusions alone is "
                "not a ceiling on the unconditional estimand. THE CONDITIONING CONSTRAINS THE "
                "NEVER-STARTED EXCLUSIONS AND SAYS NOTHING ABOUT THE CHANNEL PAIRS, so this "
                "floor moves with the bound floor and this width is %d / %d, not %d / %d."
                % (sub_ceil - sal_floor, n5, exc["started_and_left_component"], n5)),
            "constrains_never_started_exclusions": exc["never_started_component"],
            "says_nothing_about_channel_pairs": ch_sal,
            "coincides_with_bound": {
                "value": bool(sal_ceil == sub_ceil),
                "measured": True,
                "evidence": (
                    ("MEASURED TO COINCIDE: the never-started exclusion component is 0 on %s, "
                     "so conditioning on it constrains nothing and the sub-interval is the "
                     "bound. Both are [%.4f%%, %.4f%%]. Stated here rather than left for a "
                     "reader to notice two identical intervals."
                     % (pop, pct(sal_floor, n5), pct(sal_ceil, n5)))
                    if sal_ceil == sub_ceil else
                    ("MEASURED NOT TO COINCIDE: the ceilings differ by %d pairs (%d "
                     "never-started exclusions conceded to started-and-left in the bound and "
                     "not in the sub-interval), so the two intervals are different objects."
                     % (sal_ceil - sub_ceil, exc["never_started_component"])))}},
        "scope_qualifier_ref": "insertion_dormancy_covering",
        "exclusions_covered": covered,
        "endpoints_attainable": True,
        "attainable_corners": [corner_floor, corner_sal_ceiling],
        "note": ("THE FLOOR IS WIDENED, AND THE WIDENING IS ONE-SIDED. The retained pairs that "
                 "are NOT Continued, live only because they inserted after tau1, and whose "
                 "last insertion falls inside (tau1, tau2) -- %d on %s -- COULD PRODUCE NO "
                 "EVIDENCE DATED AFTER THAT INSTANT, so they may in truth be Continued and a "
                 "floor must admit it: %d - %d = %d. The ceiling does not move, because those "
                 "pairs are already counted as started-and-left in it. THE GROUND IS "
                 "ADMISSIBILITY, NOT PLAUSIBILITY: a floor is a worst case, so no margin "
                 "statistic enters it."
                 % (ch_sal, pop, p7["started_and_left"], ch_sal, sal_floor))}

    cont_bound = {
        "ceiling": endpoint(cont_ceil, "Continued ceiling"),
        "floor": {"status": "not_published",
                  "reason": ("Continued is never emitted as a point and no floor is published "
                             "for it. The ceiling exists because any EXCLUDED pair may in truth "
                             "be Continued; that does not license a point estimate."),
                  "source": "decisions/0050, decisions/0052",
                  "decided_by": "Human Lead"},
        "must_not_be_read_as_a_point": True,
        "scope_qualifier_ref": "insertion_dormancy_covering",
        "exclusions_covered": covered,
        "note": ("%d = %d observed Continued at position 5 + %d excluded + %d conceded channel "
                 "pairs, all over %d. It moves in lockstep with the started-and-left floor."
                 % (cont_ceil, p5["continued"], exc["total_pairs"], ch_sal, n5))}

    sum_pct = pct(ns_ceil, n5) + pct(sal_ceil, n5) + pct(cont_ceil, n5)
    excess_pairs = 2 * exc["never_started_component"] + exc["started_and_left_component"] + ch_sal
    ceilings = {
        "simultaneous": False,
        "sum_percent": sum_pct,
        "excess_pp": sum_pct - 100.0,
        "excess_pairs": excess_pairs,
        "excess_mechanism_expression": "2 * never_started_exclusions + started_and_left_exclusions",
        "note": ("THERE ARE THREE CEILINGS AND THEY CANNOT ALL HOLD. They are ALTERNATIVE WORST "
                 "CASES OVER ONE EXCLUSION SET, not simultaneous ones. THE MECHANISM, not just "
                 "the total: each never-started exclusion appears in ALL THREE ceiling "
                 "numerators -- excess 2 each -- and each started-and-left exclusion in TWO -- "
                 "excess 1 each; with the %d conceded channel pairs admitted, "
                 "2 x %d + %d + %d = %d pairs = %.4f pp on %s. The stated expression carries "
                 "the first two terms; the channel term is added here because it is not one of "
                 "this block's own operands, which is why decisions/0053 SS4 leaves this "
                 "identity to the writing step."
                 % (ch_sal, exc["never_started_component"],
                    exc["started_and_left_component"], ch_sal, excess_pairs,
                    sum_pct - 100.0, pop))}

    def ratio(width, denom_state, label):
        return {"value": width / lv[denom_state]["width_pp"],
                "convention_label": "arm_b_convention",
                "convention_definition": (
                    "arm_b_convention: the DENOMINATOR is the width of the 95% percentile "
                    "bootstrap interval on the corresponding POST-LIVENESS LEVEL for the same "
                    "outcome state, same arm and same population, resampled at the ACCOUNT "
                    "level with B = 10,000 and seed 20260818. Named rather than assumed, so "
                    "one arm's denominator cannot silently become the other's."),
                "numerator_definition": label,
                "denominator_definition": (
                    "account-clustered 95%% sampling width of the post-liveness %s level on "
                    "%s at this arm: %.6f pp" % (denom_state, pop, lv[denom_state]["width_pp"])),
                "reconciled_with_other_arm": False}

    ratios = {
        "never_started": ratio(ns_bound["width_pp"], "never_started",
                               "never-started bound width in percentage points"),
        "started_and_left": ratio(sal_bound["width_pp"], "started_and_left",
                                  "started-and-left bound width in percentage points"),
        "started_and_left_sub_interval": ratio(
            sal_bound["conditional_sub_interval"]["width_pp"], "started_and_left",
            "started-and-left conditional sub-interval width in percentage points"),
    }

    def ci(state):
        return {"level_pct": 95,
                "lower": lv[state]["lower"], "upper": lv[state]["upper"],
                "method": "percentile_bootstrap", "bootstrap_ref": REF,
                "B": B, "seed": SEED, "statistic": "levels",
                "resampling_unit": "account", "quantity_class": "outcome_shares",
                "note": ("A LEVEL, on the post-liveness row set (%d). Account-clustered "
                         "because pairs are not independent -- one account contributes many -- "
                         "so pair-level resampling would understate it. THE FRAME DRAWN IS %d "
                         "ACCOUNTS, every account with at least one pair in the position-4 "
                         "output, built once and drawn for every quantity (decisions/0124); %d "
                         "of them contribute to this population and %d are drawn and contribute "
                         "zero. THE DECLARED FRAME DESCRIBES THE DRAW AND NOT THE SUPPORT: "
                         "membership is arm-independent, the contributing subset is not, "
                         "because keep_d10 contains max(W, 91). THIS IS NOT COMPARABLE WITH A "
                         "PAIRED MOVEMENT: the movement on the same quantity is in "
                         "$.declared_intervals and is narrower by an order of magnitude."
                         % (n7, boot["n_accounts_resampling_frame"],
                            boot["n_accounts_contributing_to_this_group"],
                            boot["n_accounts_drawn_contributing_zero"]))}

    def share(state, num, horizon, note):
        return {"value_percent": pct(num, n7), "numerator_pairs": num,
                "denominator_pairs": n7, "on_population": pop, "on_population_n": n7,
                "on_population_label": "post-liveness (position 7)",
                "ci": ci(state), "is_an_observed_count_not_a_bound": True,
                "horizon_days": horizon, "note": note}

    return {
        "producing_arm": ARM,
        "written_by_step": STEP,
        "written_by": "Step 9, arm b",
        "shares": {
            "never_started": share(
                "never_started", p7["never_started"], W,
                "Never started is the null |A| = 0, read at tau1 = [[T0]] + %d x 24h. It is a "
                "%d-day statement. Continued is a %d-day statement. The two must never be "
                "described as measured alike." % (W, W, W + H)),
            "started_and_left": share(
                "started_and_left", p7["started_and_left"], W + H,
                "Started-and-left is |A| >= 1 and NOT the Continued condition, so it is "
                "assigned at tau2 = [[T0]] + %d x 24h on A_H. It is ALSO a null: the failure "
                "to meet the Continued condition is not observed, only |A| >= 1 is."
                % (W + H)),
            "continued": share(
                "continued", p7["continued"], W + H,
                "Continued is |A| >= 1 and F2 in A_H and |A_H| >= ceil(0.90 x L2), read at "
                "tau2 = [[T0]] + %d x 24h. It is the only one of the three that rests on "
                "POSITIVE evidence. This observed share does not replace the ceiling in "
                "bounds.continued, which must not be printed as a point." % (W + H))},
        "bounds": {"never_started": ns_bound, "started_and_left": sal_bound,
                   "continued": cont_bound},
        "ceilings_cannot_all_hold": ceilings,
        "bound_over_sampling_width_ratios": ratios,
        "spec_choices_this_arm_made": SPEC_CHOICES[arm_key],
    }


SPEC_CHOICES = {
    "W108_s2_finale": [
        "WHICH STEP 8 NAMESPACE WAS CONSUMED. task-sheet.md says CONSUME STEP 8's OUTPUT and "
        "never names which of Step 8's two arms supplies the pair-level tables. This arm read "
        "the approved artifacts artifacts/step8-waterfall-a.json and artifacts/step8-waterfall-"
        "b.json for every consumed figure, and processed/step8/a/ plus src/step8_a_lib.py for "
        "the pair-level arrays and the rule implementation. The library was chosen because it "
        "exposes the adopted rule as reusable code, so the premiere-anchored arm is measured by "
        "STEP 8's OWN implementation with a substituted T0 rather than by a second one. THE "
        "CHOICE IS A SPEC GAP AND IS REPORTED, NOT RECONCILED.",
        "THE ADOPTED ARM'S COUNTS ARE CONSUMED, NOT REPRODUCED AS PUBLISHED FIGURES. The "
        "harness was run at W = 108 and agreed with Step 8's artifacts on all 13 consumed "
        "counts before it was trusted at any other setting, and that agreement is recorded in "
        "processed/step9/b/stage1_counts.json. The agreement is a CONTROL; the published "
        "numbers remain Step 8's.",
        "THE SAMPLING-WIDTH CONVENTION IS NAMED. The spec forbids reconciling the two arms' "
        "conventions, so this arm states its own -- arm_b_convention, defined at every point of "
        "use -- rather than leaving a denominator to be inferred.",
        "NO WINDOW-W PERCENTILE INTERVAL IS DECLARED. Step 6 is an approved gate and its own "
        "instruction is 'Complete; do not re-derive', so this arm publishes no interval on W. "
        "Every interval in this file is an outcome-share quantity whose binding cluster is the "
        "ACCOUNT, so no interval here disagrees with its binding cluster and no disagreement "
        "record is present. W's interval is SHOW-clustered and remains Step 6's.",
    ],
    "W91_s2_premiere": [
        "THE ROW SET IS NOT RE-CENSORED AT THIS ARM. task-sheet.md Step 9 states that both "
        "headline arms run on the same right-censored population, max(W, 91) + H. This arm "
        "reads that as the adopted arm's position-5 row set rather than a D10 re-derived at the "
        "premiere origin, and the reading is CHECKED rather than assumed BY A NAMED CHECK THAT "
        "RUNS IN THIS PIPELINE AND RAISES -- " + _T0P_WHERE + ". " + _T0P_SUMMARY + ". The "
        "warrant it establishes: T0' <= T0 on every pair, so tau2' < tau2 <= tau_pull and every "
        "retained pair is fully observable at this arm. THE ALTERNATIVE READING -- re-deriving D10 at the premiere "
        "origin, which would ADMIT pairs the adopted arm censors -- IS REPORTED, NOT "
        "RECONCILED: it would put the two headlines on different denominators, which is what "
        "the sentence appears to forbid.",
        "LIVENESS IS RE-RUN AT THIS ARM'S OWN tau1. The rule is pair-level and anchored at that "
        "pair's own tau1, so a different origin gives a different silence test. The exclusion "
        "counts here are therefore this arm's measurement and NOT Step 8's 703 / 99.",
        "NO WATERFALL, LIVENESS-EXCLUSION OR AIR-PERIOD BLOCK IS WRITTEN HERE. Those three "
        "carry Step 8's figures and Step 8 builds them only at the finale-anchored arm, so a "
        "figure written here would be one no step in the spec produces. The absence idiom is "
        "used rather than an invented number.",
    ],
}


def waterfall_block(pop):
    """Step 8's waterfall, consumed. Written by Step 9; the figures are Step 8's."""
    rows = w8b["waterfall_APPLY" if pop == "APPLY" else "waterfall_DERIV"]
    names = {1: "step2_frame", 2: "L2_eq_1_exclusion", 3: "s1_completion_rule",
             4: "contamination_exclusion", 5: "right_censoring", 6: "liveness",
             7: "outcome_assignment"}
    two = w8a["right_censoring_two_lines"][pop]
    positions = []
    prev = None
    for r in rows:
        pos = r["position"]
        n_out = r["retained_pairs"]
        n_in = prev if prev is not None else n_out + r["removed_pairs"]
        entry = {"position": pos, "filter": names[pos], "n_in": n_in, "n_out": n_out,
                 "removed": n_in - n_out, "inert": bool(r.get("INERT")),
                 "inert_reason": r.get("inert_reason"),
                 "outcome_conditional": bool(r.get("outcome_conditional")),
                 "note": CONSUMED}
        if pos == 6:
            entry["note"] = (
                "OUTCOME-CONDITIONAL AND REPORTED AS SUCH: conjunct 2 IS the Continued test, "
                "read at tau2. Permitted because |A| = 0 and liveness are row-local predicates "
                "on the position-5 output and commute exactly, and position 7 removes no rows, "
                "so decisions/0029's per-filter-sample-size rationale cannot reach position 7. "
                + CONSUMED)
        if pos == 5:
            entry["sub_lines"] = [
                {"label": "removed by the max(W, 91) term",
                 "removed": two["removed_by_max_W_91_term"],
                 "n_out": n_in - two["removed_by_max_W_91_term"],
                 "note": ("Right-censoring publishes as TWO lines, not one. Both removals move "
                          "the never-started share UP: they remove recent S1 completers, who "
                          "are disproportionately likely to roll straight on. " + CONSUMED)},
                {"label": "removed incrementally by the + H term",
                 "removed": two["removed_incrementally_by_the_plus_H_term"],
                 "n_out": n_out,
                 "note": ("The incremental cost of the horizon term, over and above the "
                          "max(W, 91) term. " + CONSUMED)}]
        positions.append(entry)
        prev = n_out
    return {"population": pop, "written_by_step": STEP, "figures_owned_by_step": "step8",
            "order_ref": "decisions/0029 positions 1-7",
            "positions": positions,
            "monotone_check": {"operator": ">=", "result": True, "positions_checked": 7}}


def liveness_block(pop):
    a = s1["W108_s2_finale"][pop]["exclusions"]
    return {"total_pairs": a["total_pairs"],
            "never_started_component": a["never_started_component"],
            "started_and_left_component": a["started_and_left_component"],
            "accounts": a["accounts"],
            "silence_test_alone": a["silence_test_alone"],
            "spared_by_not_continued": a["spared_by_not_continued"],
            "identity": "silence_test_alone - spared_by_not_continued = total_pairs",
            "pair_level_not_account_level": True,
            "written_by_step": STEP, "figures_owned_by_step": "step8"}


def air_period_block(pop):
    arm = [x for x in w8a["per_arm"]["arms"] if x["W_days"] == 108][0]
    src = arm["retained_per_air_period_APPLY" if pop == "APPLY"
              else "retained_per_air_period_DERIV"]
    rows = [{"air_period": k, "retained_pairs": v["retained"],
             "entering_pairs": v["entering"],
             "retained_share_percent": 100.0 * v["retained"] / v["entering"]}
            for k, v in src.items()]
    return {"population": pop, "written_by_step": STEP, "figures_owned_by_step": "step8",
            "measured_after": "position 4 (the mandated order censors the position-4 output)",
            "rows": rows}


def block_absence(name):
    return {"block_is_absent": True, "status": "no_producer_in_spec",
            "owning_step": "step9",
            "reason": ("No step in the spec produces this block for a premiere-anchored arm. "
                       "Step 8 builds the waterfall, the liveness-exclusion counts and the "
                       "air-period retention table at the adopted finale-anchored arm only, "
                       "and Step 13's W grid is finale-anchored too. Writing %s here would be "
                       "writing a figure no step produces, so the absence is STATED rather "
                       "than left as silence." % name),
            "source": "decisions/0114 E13; decisions/0109 SS1"}


arms_out = []
for key, spec in ARM_SPECS.items():
    entry = {
        "arm_id": spec["arm_id"], "W_days": spec["W"], "H_days": 91,
        "clock_origin": spec["origin"], "clock_origin_note": spec["origin_note"],
        "producing_step": STEP, "adopted_rule_revision": ADOPTED_RULE_REVISION,
        "in_arm_grid": spec["in_grid"], "is_primary_headline": spec["primary"],
        "headline": {},
        "note": spec["note"],
    }
    for pop in ("APPLY", "DERIV"):
        entry["headline"][pop] = {
            "population": pop,
            "definition": ("Waterfall line 1 less D10 -- the population Step 8 filters at "
                           "position 6." if pop == "APPLY" else
                           "Waterfall line 4 less D10 -- requires S2 evidence."),
            "n_position_5": NPOP[pop],
            "n_post_liveness": s1[key][pop]["n_post_liveness"],
            "populations_differ_note": (
                "THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint "
                "in this block is on the POSITION-5 row set (%d); every published share is on "
                "the POST-LIVENESS row set (%d). On DERIV at the adopted arm the never-started "
                "point estimate lies OUTSIDE its own bound, and that is a consequence of this "
                "difference and not of an error." % (NPOP[pop], s1[key][pop]["n_post_liveness"])),
            "by_producing_arm": {
                "step_dual_status": "dual",
                "arms_in_this_file": "one_arm",
                "producing_step": STEP,
                "step_dual_status_source": (
                    "CLAUDE.md, Dual implementation; Step 13's duality is decisions/0103 SS3; "
                    "one file per arm is decisions/0107"),
                "arms": {ARM: payload(key, pop)},
                "arm_held": ARM,
            },
        }
    if spec["origin"] == "s2_finale":
        entry["waterfall"] = {p: waterfall_block(p) for p in ("APPLY", "DERIV")}
        entry["liveness_exclusions"] = {p: liveness_block(p) for p in ("APPLY", "DERIV")}
        entry["retained_by_air_period"] = {p: air_period_block(p) for p in ("APPLY", "DERIV")}
    else:
        entry["waterfall"] = block_absence("a waterfall")
        entry["liveness_exclusions"] = block_absence("a liveness-exclusion block")
        entry["retained_by_air_period"] = block_absence("an air-period retention table")
    arms_out.append(entry)

# ---------------------------------------------------------------------------------------------
# declared intervals -- the PAIRED MOVEMENTS. decisions/0118: both objects, both labelled.
# ---------------------------------------------------------------------------------------------
declared = []
for key in ARM_SPECS:
    for pop in ("APPLY", "DERIV"):
        mv = s2[key][pop]["paired_movements_pp"]
        stable = s2[key][pop]["movement_sign_stable"]
        for state in ("never_started", "started_and_left", "continued"):
            declared.append({
                "interval_id": "movement_%s_%s_%s_%s" % (key, pop, state, ARM),
                "quantity": (
                    "A PAIRED MOVEMENT: the change in the %s share caused by the liveness "
                    "filter at the %s arm on %s -- the post-liveness level minus the "
                    "position-5 level -- resampled as a paired delta inside each replicate, so "
                    "the same account weights produce both terms. IT IS NOT A LEVEL AND IS "
                    "NEVER COMPARED WITH ONE: the corresponding level interval is %.4f pp wide "
                    "and this movement is %.4f pp wide."
                    % (state.replace("_", " "), key, pop,
                       s2[key][pop]["levels_post_liveness_pct"][state]["width_pp"],
                       mv[state]["width_pp"])),
                "produced_by_step": STEP,
                "producing_arm": ARM,
                "ci": {"level_pct": 95, "lower": mv[state]["lower"],
                       "upper": mv[state]["upper"], "method": "percentile_bootstrap",
                       "bootstrap_ref": REF, "B": B, "seed": SEED,
                       "statistic": "movements", "resampling_unit": "account",
                       "quantity_class": "outcome_shares",
                       "note": ("A MOVEMENT. Sign stable across all %d replicates: %s. Where "
                                "the interval excludes zero but the sign is not stable across "
                                "every replicate, both facts are stated rather than one."
                                % (B, stable[state]))},
                "note": ("THE SECOND OF THE TWO OBJECTS THE SPEC FIXES (decisions/0118). Both "
                         "arms produce both objects and neither is presented as the design."),
                "source": "decisions/0118; decisions/0103",
            })

# ---------------------------------------------------------------------------------------------
# declared intervals -- the POSITION-5 LEVELS. Human Lead ruling 1, 2026-08-25.
#
# THESE TWELVE INTERVALS WERE MEASURED AND REACHED NO ARTIFACT. src/step9_b_2_bootstrap.py has
# computed `levels_position_5_pct` on every replicate since the first build; the emitter wrote
# the POST-LIVENESS level into each share's `ci` and the PAIRED MOVEMENT into
# $.declared_intervals, and the third family fell between them. A measured figure that reaches
# no artifact is this study's most-repeated defect.
#
# WHY THEY BELONG HERE AND NOT SOMEWHERE ELSE IN THE FILE. $defs/step9_payload carries
# `additionalProperties: false`, `$defs/endpoint` likewise, and neither a bound nor its floor or
# ceiling has a slot for an interval; the only interval slot inside a payload is `share.ci`,
# which is typed to a share on the POST-LIVENESS row set and is a different population. So the
# schema leaves exactly one place an interval on the position-5 row set can go, and it is the
# array that already holds this arm's paired movements. THE APPEND IS AT THE END, DELIBERATELY:
# src/step9_b_6_stamp_superseded.py resolves `$.declared_intervals[i]` by INDEX in the corrected
# emission after selecting `i` on the committed one, so prepending or interleaving would have
# re-pointed both supersession layers at the wrong entries.
#
# THEY ARE THE SAMPLING UNCERTAINTY ON THE POPULATION THE BOUNDS BOUND. Every bound in this file
# is on position 5 and every published share is post-liveness; $.arms[].headline[].
# populations_differ_note already says so, and on DERIV the never-started point estimate lies
# outside its own bound in consequence. These twelve are the only intervals in the file on the
# bounds' own row set.
# ---------------------------------------------------------------------------------------------
for key in ARM_SPECS:
    for pop in ("APPLY", "DERIV"):
        lp5 = s2[key][pop]["levels_position_5_pct"]
        lpl = s2[key][pop]["levels_post_liveness_pct"]
        bt = s2[key][pop]
        n5_here = bt["n_pairs_position_5"]
        # THE POSITION-5 SIZE THIS BOOTSTRAP RESAMPLED, AGAINST STEP 8'S OWN FIGURE. Set
        # membership against the source, not a plausibility window: if this arm's row set ever
        # stopped being Step 8's, every one of these intervals would be on a population the
        # file names wrongly, and no range test could see it.
        if n5_here != NPOP[pop]:
            raise SystemExit("HARD STOP: the bootstrap resampled %d position-5 pairs on %s at "
                             "the %s arm, and Step 8's approved waterfall says %d. An interval "
                             "cannot declare a population it was not computed on."
                             % (n5_here, pop, key, NPOP[pop]))
        for state in ("never_started", "started_and_left", "continued"):
            declared.append({
                "interval_id": "level_position5_%s_%s_%s_%s" % (key, pop, state, ARM),
                "quantity": (
                    "A LEVEL, ON THE POSITION-5 ROW SET: the %s share at the %s arm on %s over "
                    "all %s pairs, BEFORE the liveness filter -- account-clustered percentile "
                    "bootstrap. THIS IS THE SAMPLING UNCERTAINTY ON THE POPULATION THE BOUNDS "
                    "IN THIS FILE ARE ON. Every bound endpoint here is on position 5 and every "
                    "published share is on the post-liveness row set (%s); the two are "
                    "different populations, which is why the DERIV never-started point estimate "
                    "lies outside its own bound. IT IS NOT THE SAME QUANTITY AS THE LEVEL AT "
                    "$...shares.%s.ci, which is the same statistic on the OTHER population, and "
                    "IT IS NOT COMPARABLE WITH A PAIRED MOVEMENT: the movement on this quantity "
                    "is %.4f pp wide and this level is %.4f pp wide."
                    % (state.replace("_", " "), key, pop, format(n5_here, ","),
                       format(bt["n_pairs_post_liveness"], ","), state,
                       s2[key][pop]["paired_movements_pp"][state]["width_pp"],
                       lp5[state]["width_pp"])),
                "produced_by_step": STEP,
                "producing_arm": ARM,
                "ci": {"level_pct": 95, "lower": lp5[state]["lower"],
                       "upper": lp5[state]["upper"], "method": "percentile_bootstrap",
                       "bootstrap_ref": REF, "B": B, "seed": SEED,
                       "statistic": "levels", "resampling_unit": "account",
                       "quantity_class": "outcome_shares",
                       "note": ("A LEVEL on the POSITION-5 row set (%s), not the post-liveness "
                                "one (%s). Account-clustered because pairs are not independent "
                                "-- one account contributes many. THE FRAME DRAWN IS %d "
                                "ACCOUNTS, every account with at least one pair in the "
                                "position-4 output, built once and drawn for every quantity "
                                "(decisions/0124); %d of them contribute to this population "
                                "and %d are drawn and contribute zero. THE DECLARED FRAME "
                                "DESCRIBES THE DRAW AND NOT THE SUPPORT: membership is "
                                "arm-independent, the contributing subset is not, because "
                                "keep_d10 contains max(W, 91). Evaluated against the SAME "
                                "replicate set as every other interval in this file, which is "
                                "what makes the paired movement on this quantity paired. The "
                                "post-liveness level of the same state is %.4f pp wide."
                                % (format(n5_here, ","),
                                   format(bt["n_pairs_post_liveness"], ","),
                                   bt["n_accounts_resampling_frame"],
                                   bt["n_accounts_contributing_to_this_group"],
                                   bt["n_accounts_drawn_contributing_zero"],
                                   lpl[state]["width_pp"]))},
                "note": ("PUBLISHED UNDER HUMAN LEAD RULING 1, 2026-08-25. This interval was "
                         "measured on the first build and reached no artifact until now. NO "
                         "DECISION TO WITHHOLD IT WAS EVER MADE OR WRITTEN: the withholding "
                         "was a DEFAULT, NOT A CHOICE, which is why nothing in this build "
                         "could see it -- see $.notes."
                         "step9_b_twelve_intervals_were_withheld_by_default."),
                "source": "Human Lead ruling 1, 2026-08-25; decisions/0118; decisions/0103",
            })

# =============================================================================================
# WHAT A NON-PLACEHOLDER FILE MUST OVERRIDE AFTER INHERITING, AND HOW IT IS DECIDED
#
# Human Lead ruling 2, 2026-08-25. Twelve of this file's top-level blocks are inherited WHOLESALE
# from artifacts/step8b-placeholder-arm-file.json. THAT PATH IS RIGHT AND IT STAYS: it is the
# read-not-typed route by which a schema bump's own payload reaches a writer (decisions/0127 SS3),
# and retyping any of it here would be a second definition of the schema's text. The question the
# ruling asks is narrower -- WHICH inherited leaves a file whose `placeholder` flag is FALSE must
# override -- and the answer is written down as a rule with a table, not left as a judgement to be
# made again by the next writer.
#
# THE RULE. THREE TESTS, APPLIED TO EVERY INHERITED STRING LEAF:
#
#   T1  SELF-REFERENCE. Does the leaf assert something ABOUT THE FILE IT SITS IN? If it does and
#       the assertion is FALSE of this file, OVERRIDE. Two were: `reading_a_placeholder` says
#       "This file's flag is true" where $.placeholder is false, and
#       `a_ci_endpoints_type_follows_its_statistic` says the movement branch is occupied "in this
#       file" by a DECLARED TYPE FIXTURE where this file holds twelve real movement measurements,
#       six of them with a negative endpoint, and no fixture at all.
#
#   T2  SELF-CONTRADICTION. Does the leaf state a figure this file also states elsewhere, and
#       disagree with it? If so, OVERRIDE. `bootstrap_is_fixed` says the spec fixes FOUR
#       bootstrap elements; $.bootstrap_settings.b_default lists SEVEN, six lines away in the
#       emitted JSON. One definition per figure -- and a file that contradicts itself in adjacent
#       lines cannot be read at either of them.
#
#   T3  SPEC TEXT. Does the leaf describe the SCHEMA's convention rather than this instance? Then
#       KEEP IT VERBATIM, whatever it says about placeholders. $.sentinels is the block whose
#       whole job is to declare the sentinel convention so a reader can tell a sentinel from a
#       measurement, and its closing clause -- neither reserved form may appear in a file whose
#       flag is false -- is exactly what makes this file's sentinel-free state legible. Rewriting
#       it would put a second definition of the schema's convention inside an arm file.
#
# REWRITE, NEVER SUPPLEMENT. A false sentence is not corrected by adding a true one beside it;
# the reader meets whichever comes first.
#
# AND THE RULE IS A CONTROL, NOT A PARAGRAPH. Every inherited string leaf is scanned for the two
# machine-checkable signatures -- a self-reference, and a spelled-out count of fixed bootstrap
# elements -- and A LEAF THAT MATCHES AND IS NOT IN THE TABLE BELOW IS A HARD STOP, NEVER A
# DEFAULT. That is what makes the next inheritance mechanical: a placeholder that grows a
# thirteenth self-referential leaf stops this emitter until someone rules on it.
#
# decisions/0127 SS3 IS WHERE THIS WAS MISSED, AND IT IS RECORDED RATHER THAN GLOSSED. The
# v1.10.0 migration flagged `$.notes.a_ci_endpoints_type_follows_its_statistic` as MOVED,
# verified it byte-identical to the template at the same path -- and never asked whether it was
# TRUE. `MOVED` and `TRUE` are different questions and the migration only asked the first.
# =============================================================================================
INHERITED_BLOCKS = ("sentinels", "arm_key", "populations", "scope_qualifiers", "bootstrap_spec",
                    "binding_clusters", "step_duality", "block_ownership", "derived_fields",
                    "spec_choices_made_by_step_8b", "known_limits_of_this_schema", "notes")
SELF_REFERENCE = re.compile(r"(?i)\bthis file\b")
ELEMENT_COUNT = re.compile(r"(?i)\ball (one|two|three|four|five|six|seven|eight|nine) "
                           r"elements\b")
NUMBER_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9}

# path -> (verdict, why). OVERRIDE means this emitter replaces the leaf outright.
INHERITED_TEXT_TABLE = {
    "$.notes.reading_a_placeholder":
        ("OVERRIDE", "T1: asserts this file's placeholder flag is true; it is false."),
    "$.notes.a_ci_endpoints_type_follows_its_statistic":
        ("OVERRIDE", "T1: says the movement branch is occupied in this file by a declared type "
                     "fixture; this file holds twelve real movements, six with a negative "
                     "endpoint, and no fixture."),
    "$.notes.bootstrap_is_fixed":
        ("OVERRIDE", "T2: states a FOUR-element count; $.bootstrap_settings.b_default lists "
                     "seven fields."),
    "$.spec_choices_made_by_step_8b[25].spec_gap":
        ("KEEP_AND_REPORT",
         "T2 TRIPS AND T3 GOVERNS. It states a FOUR-element count for the bootstrap, which "
         "decisions/0124 and decisions/0125 overtook, and this file fixes seven. But "
         "$.spec_choices_made_by_step_8b is a DATED RECORD of the gaps Step 8b faced and the "
         "choices it made against them -- not a present-tense statement to a reader -- and the "
         "four-element sentence was TRUE WHEN IT WAS WRITTEN. Rewriting it would falsify "
         "another step's record of its own reasoning, which is a different thing from "
         "correcting a false statement about this file. It is therefore KEPT VERBATIM AND "
         "REPORTED TO THE HUMAN LEAD: a stale figure on a shared surface is reported by an arm "
         "and repaired by its owner (CLAUDE.md). The distinction from $.notes.bootstrap_is_fixed "
         "is not ownership -- both blocks are owner_step step8b and both are "
         "may_first_writer_fill -- it is that a NOTE speaks to the reader in the present tense "
         "and a RECORD speaks about a past moment."),
    "$.notes.no_conversion_layer":
        ("KEEP", "T3: 'this file' means a file of this kind. True of this one."),
    "$.derived_fields[6].checked_by":
        ("KEEP", "T3: true of this file -- the cross-arm ratio is not stored as a number here."),
    "$.spec_choices_made_by_step_8b[7].choice":
        ("KEEP", "T3: Step 8b's record of Step 8b's own choice, describing the placeholder it "
                 "built. Not a claim about this instance, and not this arm's to rewrite."),
    "$.spec_choices_made_by_step_8b[7].what_was_done":
        ("KEEP", "T3: as above -- the W = 91 finale-anchored entry it describes is the "
                 "placeholder's, not this file's."),
    "$.spec_choices_made_by_step_8b[17].spec_gap":
        ("KEEP", "T3: 'THIS FILE' names the general case the spec does not resolve."),
    "$.spec_choices_made_by_step_8b[17].if_ruled_otherwise":
        ("KEEP", "T3: Step 8b's own consequence analysis, not a claim about this instance."),
    "$.spec_choices_made_by_step_8b[21].spec_gap":
        ("KEEP", "T3: quotes the spec's own wording about Steps 9-13."),
    "$.known_limits_of_this_schema[12].mitigation":
        ("KEEP", "T3: true of this file -- nothing here substitutes for the Human Lead's diff."),
    "$.known_limits_of_this_schema[13].mitigation":
        ("KEEP", "T3: true of this file, and a limit of the schema rather than of this run."),
    "$.known_limits_of_this_schema[15].limit":
        ("KEEP", "T3: a limit the schema records against itself."),
}


def _string_leaves(node, path):
    if isinstance(node, dict):
        for k, v in node.items():
            for r in _string_leaves(v, "%s.%s" % (path, k)):
                yield r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            for r in _string_leaves(v, "%s[%d]" % (path, i)):
                yield r
    elif isinstance(node, str):
        yield path, node


def audit_inherited_text(template, overridden, n_fixed_elements):
    """HARD-STOP unless every inherited leaf that trips a signature has a written verdict."""
    scanned = matched = 0
    verdicts = {"OVERRIDE": [], "KEEP": [], "KEEP_AND_REPORT": []}
    for block in INHERITED_BLOCKS:
        if block not in template:
            raise SystemExit("HARD STOP: the placeholder carries no %r, so this emitter cannot "
                             "audit what it inherits from it." % block)
        for path, text in _string_leaves(template[block], "$." + block):
            scanned += 1
            if not (SELF_REFERENCE.search(text) or ELEMENT_COUNT.search(text)):
                continue
            matched += 1
            if path not in INHERITED_TEXT_TABLE:
                raise SystemExit(
                    "HARD STOP: %s is inherited from the placeholder, asserts something about "
                    "the file it sits in or states a count of fixed bootstrap elements, and "
                    "carries NO VERDICT in INHERITED_TEXT_TABLE. A non-placeholder file must "
                    "say whether it overrides it. AN UNCLASSIFIED LEAF IS A HARD STOP, NEVER A "
                    "DEFAULT.\n    %r" % (path, text[:200]))
            verdict, _ = INHERITED_TEXT_TABLE[path]
            verdicts[verdict].append(path)
            if verdict == "OVERRIDE" and path not in overridden:
                raise SystemExit(
                    "HARD STOP: %s is ruled OVERRIDE and this emitter does not override it. A "
                    "verdict recorded and not applied is worse than no verdict: it reads as "
                    "having been handled." % path)
    for path in INHERITED_TEXT_TABLE:
        if path.startswith("$.notes.") and INHERITED_TEXT_TABLE[path][0] == "OVERRIDE" \
                and path.split(".")[2] not in template["notes"]:
            raise SystemExit("HARD STOP: %s is ruled OVERRIDE but no longer exists in the "
                             "placeholder. A verdict on a leaf that is gone is stale." % path)
    if matched == 0:
        raise SystemExit("HARD STOP: the inherited-text audit matched ZERO leaves across %d "
                         "scanned. An empty result and a clean result are the same value, and "
                         "the placeholder is known to carry self-referential text." % scanned)
    return {"template": os.path.relpath(TEMPLATE, ROOT),
            "template_sha256_12": sha12(TEMPLATE),
            "blocks_inherited_wholesale": list(INHERITED_BLOCKS),
            "string_leaves_scanned": scanned,
            "leaves_tripping_a_signature": matched,
            "overridden_by_this_file": sorted(verdicts["OVERRIDE"]),
            "kept_verbatim": sorted(verdicts["KEEP"]),
            "kept_verbatim_and_reported_to_the_human_lead":
                sorted(verdicts["KEEP_AND_REPORT"]),
            "verdict_reasons": {k: v[1] for k, v in sorted(INHERITED_TEXT_TABLE.items())},
            "unclassified_is_a_hard_stop": True,
            "n_bootstrap_elements_fixed_by_spec_measured_here": n_fixed_elements}


def assert_element_counts_agree(document, n_fixed_elements):
    """No leaf of the FINISHED document may state a fixed-element count that is not the one
    this file measured. This is the T2 test, run over the emitted bytes rather than over the
    template, so an override that got the number wrong fails here too.

    EXACTLY ONE CLASS IS EXEMPT AND IT IS EXEMPT BY NAME, NOT BY PATTERN: a leaf carrying the
    KEEP_AND_REPORT verdict, which is another step's dated record of its own reasoning. The
    exemption is a WRITTEN ROW with a reason, its count is returned and published, and it names
    the exact path -- registering a string as a false positive disarms the control against it
    (CLAUDE.md), so the disarming is one path wide and visible in the emitted file rather than
    a regex that would quietly widen.
    """
    exempt = {p for p, (v, _) in INHERITED_TEXT_TABLE.items() if v == "KEEP_AND_REPORT"}
    checked, exempted = 0, 0
    for path, text in _string_leaves(document, "$"):
        for m in ELEMENT_COUNT.finditer(text):
            said = NUMBER_WORDS[m.group(1).lower()]
            if path in exempt:
                exempted += 1
                if said == n_fixed_elements:
                    raise SystemExit(
                        "HARD STOP: %s is exempted from the element-count test as a stale "
                        "record, and it now AGREES with this file at %d. An exemption whose "
                        "reason has expired must be withdrawn, not left standing."
                        % (path, n_fixed_elements))
                continue
            checked += 1
            if said != n_fixed_elements:
                raise SystemExit(
                    "HARD STOP: %s says %r while this file fixes %d bootstrap elements. One "
                    "definition per figure." % (path, m.group(0), n_fixed_elements))
    if checked == 0:
        raise SystemExit("HARD STOP: zero element-count claims were examined, so 'they all "
                         "agree' reports that nothing was looked at.")
    return {"claims_checked": checked, "claims_exempted": exempted,
            "exempt_paths": sorted(exempt)}


# --- THE THREE OVERRIDES. Written out in full; none of them supplements an inherited sentence.
NOTE_OVERRIDES = {
    "reading_a_placeholder": (
        "Check $.placeholder before reading anything else. THIS FILE'S FLAG IS FALSE: every "
        "measurement slot holds a measurement, no slot holds the -999 or -999.0 sentinel, and "
        "no string carries the placeholder prefix. The inherited text at this key said the flag "
        "was true, which was the placeholder speaking about itself; it is REWRITTEN here rather "
        "than supplemented, because a false sentence is not corrected by a true one beside it. "
        "$.sentinels still states the sentinel convention verbatim, and that is what lets a "
        "reader confirm this paragraph rather than take it."),
    "a_ci_endpoints_type_follows_its_statistic": (
        "v1.10.0, Human Lead ruling 2026-08-24, AND A WRITER OF STEPS 9 THROUGH 13 NEEDS IT. A "
        "`levels` interval's endpoints are PERCENTAGES on [0, 100]. A `movements` interval's "
        "endpoints are PERCENTAGE-POINT DIFFERENCES and MAY BE NEGATIVE -- a paired movement is "
        "a difference between two configurations of one share, and the sign is the direction. "
        "The two forms are the same field under different types, selected by "
        "$.declared_intervals[].ci.statistic, so THE STATISTIC LABEL IS LOAD-BEARING ON THE TYPE "
        "and not only on the reading. $defs/percent was NOT widened to admit negatives: that "
        "would let a level interval carry a negative endpoint, which is not a possible "
        "measurement, and would trade a defect that fails loudly for one that cannot fail at "
        "all. IN THIS FILE THE MOVEMENT BRANCH IS OCCUPIED BY REAL MEASUREMENTS AND BY NO "
        "FIXTURE: twelve paired movements, six of them carrying a negative endpoint, every one "
        "a measurement of this study. The inherited text said the branch was occupied here by a "
        "DECLARED TYPE FIXTURE; that is the placeholder describing itself, it is false of a file "
        "whose flag is false, and it is REWRITTEN rather than supplemented. A fixture may appear "
        "ONLY in a placeholder -- $.sentinels.type_fixture_rule states that convention and is "
        "kept verbatim -- and this file declares none."),
    "bootstrap_is_fixed": (
        "ALL SEVEN ELEMENTS ARE FIXED BY THE SPEC: the resample count, the seed and the "
        "resampling unit for the outcome shares (decisions/0103), the statistic (decisions/0118), "
        "the RESAMPLING FRAME and the DRAW ORDER (decisions/0124), and the DRAW MECHANISM "
        "(decisions/0125). They are stated at $.bootstrap_spec and at $.bootstrap_settings, "
        "restated at every interval, and checked against each other. THE STATISTIC IS BOTH "
        "LEVELS AND PAIRED MOVEMENTS: a run produces both objects, the registry holds the pair, "
        "and each interval says which of the two it is. A level and a movement are never "
        "compared to each other. The inherited text at this key said FOUR, which was true when "
        "decisions/0118 closed the third element and was overtaken by decisions/0124 and "
        "decisions/0125; it disagreed with $.bootstrap_settings.b_default six lines below it in "
        "the emitted JSON, and it is REWRITTEN rather than supplemented."),
}
# THE SEVEN IS COUNTED, NOT TYPED. It is len() of the very list $.bootstrap_settings publishes,
# so the note and the block cannot drift apart -- which is the defect T2 caught in the inherited
# text and would be no better for being made here.
FIELDS_FIXED_IN_SPEC = ["B", "seed", "resampling_unit", "statistics",
                        "resampling_frame", "draw_order", "draw_mechanism"]
_N_FIXED_ELEMENTS = len(FIELDS_FIXED_IN_SPEC)
_INHERITED_AUDIT = audit_inherited_text(
    tpl, {"$.notes." + k for k in NOTE_OVERRIDES}, _N_FIXED_ELEMENTS)

# ---------------------------------------------------------------------------------------------
# assemble
# ---------------------------------------------------------------------------------------------
doc = {
    "schema_version": schema["properties"]["schema_version"]["const"],
    "schema_id": schema["properties"]["schema_id"]["const"],
    "placeholder": False,
    "generated_by": {
        "generator": ME,
        "generator_sha256_12": sha12(os.path.join(ROOT, ME)),
        "generated_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "build_tag": BUILD_TAG,
        "git_head_short": subprocess.run(
            ["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True).stdout.strip(),
        "host_step": "Step 9, headline result",
        "written_by": "Data Scientist, arm b",
        "inputs": [
            "artifacts/step8-waterfall-a.json (sha256:12 %s)"
            % sha12(os.path.join(ROOT, "artifacts/step8-waterfall-a.json")),
            "artifacts/step8-waterfall-b.json (sha256:12 %s)"
            % sha12(os.path.join(ROOT, "artifacts/step8-waterfall-b.json")),
            "processed/step8/a/scan.npz, processed/step8/a/positions.npz "
            "(pair-level arrays for the premiere-anchored arm and the account clustering)",
            "src/step8_a_lib.py (sha256:12 %s) -- Step 8's own rule implementation, driven "
            "with a substituted T0 so the premiere arm is not a second definition"
            % sha12(os.path.join(ROOT, "src/step8_a_lib.py")),
            "processed/step2/frame.csv (S2 premiere dates, E2, L2, F2)",
            "processed/step5/adopted_rule.json (the adopted-rule revision, READ not typed)",
            "processed/step9/b/stage1_counts.json, processed/step9/b/stage2_bootstrap.json",
        ],
    },
    "document_scope": {
        "role": "arm_file",
        "producing_step": STEP,
        "arm": ARM,
        "also_written_by_steps": [],
        "isolation_rule": (
            "Each arm writes its own document, and no arm writes into a document another arm "
            "writes into. Neither instance sees the other's work, asks about it, or reads its "
            "output folder. It is the DIFF, between two files, that is the dual control."),
        "note": ("This file is Step 9 arm b's measurement and asserts nothing about arm a, "
                 "about the merged document, or about any other step's state. "
                 "$.cross_arm_divergences and $.limitations are deliberately absent: the first "
                 "is the Human Lead's diff record and this arm cannot see the other arm, so it "
                 "could only fabricate one; the second is Human-Lead-only."),
        "source": "decisions/0107; task-sheet.md Step 13b; CLAUDE.md, Dual implementation",
    },
    "sentinels": tpl["sentinels"],
    "arm_key": tpl["arm_key"],
    "adopted_rule_revision": G._read_adopted_rule_revision(),
    "arm_grid_days": [38, 46, 77, 91, 107, 108, 150, 213],
    "populations": {
        "APPLY": dict(tpl["populations"]["APPLY"], reference_n_at_the_adopted_arm=NPOP["APPLY"]),
        "DERIV": dict(tpl["populations"]["DERIV"], reference_n_at_the_adopted_arm=NPOP["DERIV"]),
    },
    "scope_qualifiers": tpl["scope_qualifiers"],
    "bootstrap_spec": tpl["bootstrap_spec"],
    "binding_clusters": tpl["binding_clusters"],
    "bootstrap_settings": {
        REF: {
            "B": B, "seed": SEED, "statistics": ["levels", "movements"],
            "resampling_unit": "account", "producing_arm": ARM,
            "spec_status": "fixed_in_spec",
            "fields_considered": list(FIELDS_FIXED_IN_SPEC),
            "fields_fixed_in_spec": list(FIELDS_FIXED_IN_SPEC),
            "fields_not_fixed_in_spec": [],
            # The word SEVEN is a literal and is CHECKED rather than templated:
            # assert_element_counts_agree() walks the finished document and hard-stops on any
            # element-count claim that is not len(FIELDS_FIXED_IN_SPEC). A control that catches
            # drift is better than a substitution that hides whether drift is possible.
            "note": ("ALL SEVEN ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE -- "
                     "decisions/0103 for B, the seed and the unit, decisions/0118 for the "
                     "statistic, decisions/0124 for the FRAME and the DRAW ORDER, decisions/0125 "
                     "for the DRAW MECHANISM. THE MECHANISM IS THE GENERATOR "
                     "numpy.random.default_rng, THE CALL rng.integers(0, n_frame, size=(m, "
                     "n_frame)), AND WEIGHTS FORMED BY COUNTING THE DRAWN INDICES -- those four "
                     "things and nothing else; the CHUNKING is not a spec element, because CHUNK "
                     "200, CHUNK 500 and a single call give identical arrays under one seed. "
                     "This arm previously drew with `multinomial`, which satisfied decisions/0124 "
                     "literally and STILL produced a different replicate set, since the two "
                     "samplers consume the stream differently: the distribution was right either "
                     "way and the realisation was not the same. The frame is "
                     "every account with at least one pair in the position-4 output (%d), built "
                     "once and drawn for every quantity regardless of how much it contributes; "
                     "the draw order is one RNG seeded once per file, its stream consumed "
                     "continuously, with all %d intervals in this file evaluated against ONE "
                     "replicate set (digest %s). THE FRAME FIELD DESCRIBES THE DRAW AND NOT THE "
                     "SUPPORT (decisions/0124 SS4(1)): membership is arm-independent, the "
                     "contributing subset is not, because keep_d10 contains max(W, 91) -- the "
                     "per-population contributing counts are stated at each interval. The fixed "
                     "seed is what makes the two arms comparable: without it a difference "
                     "between them could be sampling noise rather than a divergence. The seed "
                     "VALUE is arbitrary; its FIXITY is the point -- and an unfixed draw order "
                     "or an unfixed mechanism makes a fixed seed decorative, which is why "
                     "decisions/0124 fixes the one and decisions/0125 the other."
                     % (BOOT_DESIGN["resampling_frame_n"],
                        BOOT_DESIGN["quantities_sharing_the_replicate_set"],
                        BOOT_DESIGN["replicate_set_digest_sha256_12"])),
        },
    },
    "step_duality": tpl["step_duality"],
    "declared_intervals": declared,
    "block_ownership": tpl["block_ownership"],
    "channel_classes": {
        "block_is_absent": True, "status": "not_required_by_spec",
        "reason": ("D4 and D9 are STEP 8's figures and Step 9 is forbidden to recompute "
                   "either. Requiring this block in seven arm files would make seven writers "
                   "of one figure, with no precedence rule and no agreement check; the merged "
                   "document carries it once, filled at Step 13b from Step 8's artifact. The "
                   "bounds in this file still publish ALONGSIDE D4 and D9 rather than folding "
                   "them in -- $.scope_qualifiers records that the covering claim is open "
                   "across exactly those two channel classes."),
        "owning_step": "step13b",
        "source": "decisions/0114 E8; decisions/0117; decisions/0109 SS1"},
    "discovery_channel_overlap": {
        "block_is_absent": True, "status": "not_required_by_spec",
        "reason": ("The discovery-channel overlap is STEP 8's measurement, published in four "
                   "units with a different consumer for each. Same shape as channel_classes: "
                   "the merged document carries it once."),
        "owning_step": "step13b",
        "source": "decisions/0114 E8; decisions/0117; decisions/0109 SS1"},
    "derived_fields": tpl["derived_fields"],
    "arms": arms_out,
    "spec_choices_made_by_step_8b": tpl["spec_choices_made_by_step_8b"],
    "known_limits_of_this_schema": tpl["known_limits_of_this_schema"],
    "notes": dict(tpl["notes"], **NOTE_OVERRIDES, **{
        "step9_b_twelve_intervals_were_withheld_by_default": (
            "TWELVE MEASURED INTERVALS REACHED NO ARTIFACT UNTIL 2026-08-25, AND NO DECISION TO "
            "WITHHOLD THEM WAS EVER MADE OR WRITTEN. THE WITHHOLDING WAS A DEFAULT, NOT A "
            "CHOICE -- AND THAT IS WHY NOTHING IN THIS BUILD COULD SEE IT. "
            "src/step9_b_2_bootstrap.py has computed `levels_position_5_pct` on every replicate "
            "since the first build. The emitter wrote the POST-LIVENESS level into each share's "
            "`ci` and the PAIRED MOVEMENT into $.declared_intervals, and the third family fell "
            "between the two without anyone deciding it should. There is no note, no spec "
            "choice, no divergence and no open defect recording a reason, because there was no "
            "reason to record: nothing was decided. "
            "A WITHDRAWAL LEAVES A TRACE AND A DEFAULT LEAVES NONE. The controls in this study "
            "look for wrong figures, withdrawn claims and stale artifacts; every one of those is "
            "something a writer DID. This was something no writer did, and it is invisible to "
            "all three -- the file validated clean at 45 checks with 0 failed both before and "
            "after, because a schema can check what is in a file and cannot check what a writer "
            "never put there (decisions/0127 SS4d records the same gap from the other side, "
            "where an arm withheld nine intervals DELIBERATELY and said so). "
            "IT IS THE QUANTITY THAT SPEAKS TO THE GAP THIS FILE ALREADY NAMES. Every bound here "
            "is on the position-5 row set and every published share is post-liveness; "
            "$.arms[].headline[].populations_differ_note says so, and on DERIV the never-started "
            "point estimate lies outside its own bound in consequence. These twelve are the only "
            "intervals in the file on the bounds' own population, so the file named the gap and "
            "omitted the measurement of it. "
            "Published under Human Lead ruling 1, 2026-08-25, at $.declared_intervals, twelve "
            "intervals and twenty-four endpoints. No figure already published moved."),
        "step9_b_what_a_non_placeholder_file_overrides_after_inheriting": (
            "TWELVE TOP-LEVEL BLOCKS ARE INHERITED WHOLESALE from %s. THAT PATH IS RIGHT AND IT "
            "STAYS -- it is the read-not-typed route by which a schema bump's own payload "
            "reaches a writer (decisions/0127 SS3), and retyping any of it here would be a "
            "second definition of the schema's text. WHAT A FILE WHOSE `placeholder` FLAG IS "
            "FALSE MUST OVERRIDE IS DECIDED BY A WRITTEN RULE, NOT PER LEAF. "
            "T1 SELF-REFERENCE: a leaf asserting something about the file it sits in, which is "
            "false of this file, is OVERRIDDEN. T2 SELF-CONTRADICTION: a leaf stating a figure "
            "this file also states elsewhere, and disagreeing with it, is OVERRIDDEN. T3 SPEC "
            "TEXT: a leaf describing the SCHEMA's convention rather than this instance is KEPT "
            "VERBATIM, whatever it says about placeholders -- $.sentinels is the block whose job "
            "is to declare the sentinel convention so a reader can tell a sentinel from a "
            "measurement, and rewriting it would put a second definition of that convention "
            "inside an arm file. "
            "REWRITTEN, NEVER SUPPLEMENTED: %s. KEPT VERBATIM: %d further leaf(-ves) that trip a "
            "signature. %d string leaves scanned, %d tripped, and A LEAF THAT TRIPS AND CARRIES "
            "NO VERDICT IS A HARD STOP -- so a placeholder that grows a thirteenth "
            "self-referential leaf stops this emitter until someone rules on it, which is what "
            "makes the next inheritance mechanical rather than a fresh judgement. "
            "decisions/0127 SS3 IS WHERE THIS WAS MISSED: the v1.10.0 migration flagged "
            "$.notes.a_ci_endpoints_type_follows_its_statistic as MOVED, verified it "
            "byte-identical to the template at the same path, and never asked whether it was "
            "TRUE. MOVED AND TRUE ARE DIFFERENT QUESTIONS, and the migration asked only the "
            "first."
            "A THIRD VERDICT EXISTS AND ONE LEAF CARRIES IT: %s is KEPT VERBATIM AND REPORTED "
            "TO THE HUMAN LEAD. It states a FOUR-element count for the bootstrap, which "
            "decisions/0124 and decisions/0125 overtook and this file contradicts at seven -- "
            "but $.spec_choices_made_by_step_8b is a DATED RECORD of another step's reasoning "
            "rather than a present-tense statement to a reader, and the sentence was true when "
            "it was written. An arm reports a stale figure on a surface it does not own; it "
            "does not repair it. The distinction from $.notes.bootstrap_is_fixed is NOT "
            "ownership -- both blocks are owner_step step8b and both are may_first_writer_fill "
            "-- it is note versus record. THIS EXEMPTION IS ONE PATH WIDE, WRITTEN AS A ROW "
            "WITH A REASON, AND IT WITHDRAWS ITSELF: the emitter hard-stops if the exempted "
            "leaf ever comes to AGREE, because an exemption whose reason has expired is a "
            "control disarmed for nothing."
            % (os.path.relpath(TEMPLATE, ROOT),
               ", ".join(_INHERITED_AUDIT["overridden_by_this_file"]),
               len(_INHERITED_AUDIT["kept_verbatim"]),
               _INHERITED_AUDIT["string_leaves_scanned"],
               _INHERITED_AUDIT["leaves_tripping_a_signature"],
               ", ".join(_INHERITED_AUDIT[
                   "kept_verbatim_and_reported_to_the_human_lead"]))),
        "step9_b_resampling_frame_draw_order_and_draw_mechanism": (
            "THE FRAME IS %d ACCOUNTS -- every account with at least one pair in the POSITION-4 "
            "output, built ONCE, and DRAWN FOR EVERY QUANTITY regardless of how much it "
            "contributes (decisions/0124). It is NOT the contributing subset: accounts the "
            "censoring rule excludes are part of the population the uncertainty is about, and "
            "drawing only contributors conditions the variance on the censoring outcome and "
            "treats survivorship as fixed. At the adopted arm %d accounts are drawn and "
            "contribute zero on APPLY and %d on DERIV; every one of them held position-4 pairs "
            "and every one of those pairs was removed by D10. "
            "THE DRAW ORDER IS ONE RNG, SEEDED ONCE PER FILE, its stream consumed CONTINUOUSLY, "
            "with all %d intervals in this file evaluated against THE SAME REPLICATE SET "
            "(digest %s) -- NOT re-seeded per group, because a per-group restart pairs a "
            "between-setting movement only WITHIN a group and Step 13 varies W across eight "
            "arms. "
            "THE DRAW MECHANISM IS THE GENERATOR numpy.random.default_rng, THE CALL "
            "rng.integers(0, n_frame, size=(m, n_frame)), AND WEIGHTS FORMED BY COUNTING THE "
            "DRAWN INDICES (decisions/0125) -- four things, and the chunking is not one of them, "
            "since CHUNK 200, CHUNK 500 and a single call give identical arrays under one seed. "
            "It is named because satisfying the draw ORDER does not determine the draw: this arm "
            "drew with `multinomial` under one module-scope RNG seeded once, which met "
            "decisions/0124 in full and still produced a different replicate set. "
            "THE FRAME DECLARATION DESCRIBES THE DRAW AND NOT THE SUPPORT (decisions/0124 "
            "SS4(1)): membership is %d at every arm and on both populations, while the "
            "contributing subset is %d on APPLY and %d on DERIV and moves with W, because "
            "keep_d10 contains max(W, 91). "
            "ONE FRAME SERVES BOTH POPULATIONS here, since the position-4 DERIV rows are a "
            "subset of the position-4 APPLY rows; decisions/0124 SS4(2)'s constraint -- that an "
            "APPLY-minus-DERIV delta cannot be paired at the account level where the two "
            "populations have different frames -- is recorded, and NO SUCH DELTA IS PUBLISHED "
            "IN THIS FILE."
            % (BOOT_DESIGN["resampling_frame_n"],
               s2["W108_s2_finale"]["APPLY"]["n_accounts_drawn_contributing_zero"],
               s2["W108_s2_finale"]["DERIV"]["n_accounts_drawn_contributing_zero"],
               BOOT_DESIGN["quantities_sharing_the_replicate_set"],
               BOOT_DESIGN["replicate_set_digest_sha256_12"],
               BOOT_DESIGN["resampling_frame_n"],
               s2["W108_s2_finale"]["APPLY"]["n_accounts_contributing_to_this_group"],
               s2["W108_s2_finale"]["DERIV"]["n_accounts_contributing_to_this_group"])),
        "step9_b_arm_grid_days_is_not_this_arms_block": (
            "$.arm_grid_days IS STEP 13's BLOCK. It is required at the root of every file and "
            "block_ownership marks it may_first_writer_fill, so THIS ARM FILLED IT AS FIRST "
            "WRITER AND IT IS NOT ITS OWN. The eight values are COPIED from the Human Lead's "
            "ruling at decisions/0075; they are not a measurement taken here and Step 9 varies "
            "nothing across them. Step 13 is dual, so a value neither of its arms wrote must be "
            "visible as such at the diff rather than inferred."),
        "step9_b_which_step8_namespace_was_consumed": (
            "task-sheet.md says CONSUME STEP 8's OUTPUT and does not name which of Step 8's two "
            "arms supplies the pair-level tables. This arm read both approved waterfall "
            "artifacts for every consumed figure and processed/step8/a/ plus src/step8_a_lib.py "
            "for the pair-level arrays and the rule implementation. The unnamed choice is a "
            "spec gap, reported and not reconciled."),
        "step9_b_no_show_bound_interval_is_published_here": (
            "Every interval in this file is an outcome-share quantity, whose binding cluster is "
            "the ACCOUNT, so every one of them says `account` and none inherits it silently. NO "
            "WINDOW-W PERCENTILE INTERVAL IS DECLARED: W's binding cluster is the SHOW and "
            "account-level resampling would understate it, and Step 6 is an approved gate whose "
            "instruction is 'Complete; do not re-derive'. There is therefore no unit "
            "disagreement to report in this file, and that is stated rather than left to be "
            "inferred from an absence."),
        "step9_b_d4_and_d9_publish_alongside": (
            "The Step 9 instruction says to report the S3-without-S2 bound (D4) and the "
            "split-artifact bound (D9) ALONGSIDE the liveness bound, while decisions/0114 E8 "
            "forbids an arm file to write $.channel_classes at all. Both are followed here: the "
            "block carries the absence idiom, and the ALONGSIDE relation survives in "
            "$.scope_qualifiers, which records that the bound is covering with respect to "
            "insertion-dormancy exhaustively and OPEN ONLY ACROSS D4 AND D9. The tension is "
            "REPORTED, NOT RECONCILED."),
    }),
}

# THE T2 TEST, RUN OVER THE FINISHED DOCUMENT rather than over the template: an override that
# got the number wrong would fail here too. It hard-stops on zero coverage, because "they all
# agree" and "nothing was looked at" are the same value otherwise.
_ELEMENT_CLAIMS_CHECKED = assert_element_counts_agree(doc, _N_FIXED_ELEMENTS)

# EVERY MEASURED INTERVAL IS PUBLISHED, AND THAT IS ASSERTED, NOT LEFT TO A DEFAULT.
# Human Lead ruling 1, 2026-08-25. Twelve position-5 level intervals were measured on every
# build and reached no artifact, and NOTHING COULD SEE IT: the validator passes identically on a
# file that omits them, because a schema checks what is in a file and cannot check what a writer
# never put there. So this emitter counts the interval families stage 2 produced and requires
# each one to appear in the emitted document. A family that grows in the bootstrap and is not
# emitted here now stops the run.
_MEASURED = {}
for _k in ARM_SPECS:
    for _p in ("APPLY", "DERIV"):
        for _fam in ("levels_position_5_pct", "levels_post_liveness_pct", "paired_movements_pp"):
            _MEASURED[_fam] = _MEASURED.get(_fam, 0) + len(s2[_k][_p][_fam])
_emitted_endpoints = set()
for _iv in doc["declared_intervals"]:
    _emitted_endpoints.add((_iv["ci"]["lower"], _iv["ci"]["upper"]))
for _a in doc["arms"]:
    for _p in ("APPLY", "DERIV"):
        for _sh in _a["headline"][_p]["by_producing_arm"]["arms"][ARM]["shares"].values():
            _emitted_endpoints.add((_sh["ci"]["lower"], _sh["ci"]["upper"]))
_unpublished = []
for _k in ARM_SPECS:
    for _p in ("APPLY", "DERIV"):
        for _fam in ("levels_position_5_pct", "levels_post_liveness_pct", "paired_movements_pp"):
            for _st, _v in s2[_k][_p][_fam].items():
                if (_v["lower"], _v["upper"]) not in _emitted_endpoints:
                    _unpublished.append("%s.%s.%s.%s" % (_k, _p, _fam, _st))
if _unpublished:
    raise SystemExit(
        "HARD STOP: %d interval(s) measured in processed/step9/b/stage2_bootstrap.json reach no "
        "slot in this document. A MEASURED FIGURE THAT REACHES NO ARTIFACT IS THIS STUDY'S "
        "MOST-REPEATED DEFECT, and withholding one by default is invisible to every control "
        "here. If an omission is deliberate it is declared, never silent: %s"
        % (len(_unpublished), _unpublished[:6]))
if sum(_MEASURED.values()) == 0:
    raise SystemExit("HARD STOP: the completeness check found zero measured intervals, so it "
                     "reports that it looked nowhere rather than that nothing is missing.")

# THE TWO GUARDS' COVERAGE IS PUBLISHED, NOT JUST COMPUTED. A check whose coverage nobody can
# read is a check a reader has to take on trust, and this emission exists because a measured
# figure sat in a working file and reached no artifact.
doc["notes"]["step9_b_emission_guards_and_their_coverage"] = (
    "TWO GUARDS RUN IN THIS EMITTER AND BOTH HARD-STOP ON ZERO COVERAGE. "
    "(1) THE ELEMENT-COUNT AGREEMENT TEST walked every string leaf of the finished document and "
    "checked %d spelled-out claim(s) about how many bootstrap elements the spec fixes against "
    "the %d fields listed at $.bootstrap_settings.b_default.fields_fixed_in_spec; %d claim(s) "
    "were exempted, by written row and by exact path, at %s -- another step's dated record of "
    "its own reasoning, kept verbatim and reported rather than rewritten. The exemption "
    "withdraws itself: the run hard-stops if the exempted leaf ever comes to agree. "
    "(2) THE EMISSION-COMPLETENESS GUARD took every interval "
    "processed/step9/b/stage2_bootstrap.json measured -- %d across three families, "
    "levels on the position-5 row set, levels on the post-liveness row set and paired "
    "movements -- and required each one's endpoints to appear in this document. A family that "
    "grows in the bootstrap and is not emitted here now stops the run. IT EXISTS BECAUSE THE "
    "SCHEMA CANNOT: Step 8b's validator returns ok on a file that omits a measured interval, "
    "since a schema checks what is in a file and cannot check what a writer never put there."
    % (_ELEMENT_CLAIMS_CHECKED["claims_checked"], _N_FIXED_ELEMENTS,
       _ELEMENT_CLAIMS_CHECKED["claims_exempted"],
       ", ".join(_ELEMENT_CLAIMS_CHECKED["exempt_paths"]),
       sum(_MEASURED.values())))

# OUTPUT DIRECTORY, OVERRIDABLE. Default is artifacts/, which is where a signed run writes.
# A CORRECTION RUN whose figures have not yet been seen by the Human Lead sets STEP9_B_OUTDIR to
# a working directory, so a committed deliverable is never overwritten by a run nobody has
# looked at. The file NAME never changes, so the preview and the deliverable are the same object
# written to two places rather than two objects.
OUTDIR = os.environ.get("STEP9_B_OUTDIR", os.path.join(ROOT, "artifacts"))
os.makedirs(OUTDIR, exist_ok=True)
out = os.path.join(OUTDIR, "step9-headline-b.json")
with open(out, "w") as fh:
    json.dump(doc, fh, indent=1, ensure_ascii=True)
print("wrote", out, os.path.getsize(out), "bytes")
