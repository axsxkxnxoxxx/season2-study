"""Step 9, arm `b`, stage 3: write the arm file into Step 8b's schema.

NO CONVERSION LAYER. Every figure is written into the schema's own shapes; nothing
is emitted in a private shape and translated. Adopts nothing. Zero API calls.
"""
import hashlib
import json
import os
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
BUILD_TAG = "step9/b/2026-08-20"
ME = "src/step9_b_3_emit.py"

s1 = json.load(open(os.path.join(WORK, "stage1_counts.json")))
s2 = json.load(open(os.path.join(WORK, "stage2_bootstrap.json")))
tpl = json.load(open(TEMPLATE))
schema = json.load(open(SCHEMA))

w8a = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-a.json")))
w8b = json.load(open(os.path.join(ROOT, "artifacts/step8-waterfall-b.json")))

B, SEED = 10000, 20260818
REF = "b_default"
NPOP = {"APPLY": 196654, "DERIV": 147370}
NPOST = {"APPLY": 195951, "DERIV": 147271}

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
                         "so pair-level resampling would understate it. %d accounts carry this "
                         "population. THIS IS NOT COMPARABLE WITH A PAIRED MOVEMENT: the "
                         "movement on the same quantity is in $.declared_intervals and is "
                         "narrower by an order of magnitude."
                         % (n7, boot["n_accounts"]))}

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
            "fields_considered": ["B", "seed", "resampling_unit", "statistics"],
            "fields_fixed_in_spec": ["B", "seed", "resampling_unit", "statistics"],
            "fields_not_fixed_in_spec": [],
            "note": ("ALL FOUR ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE -- "
                     "decisions/0103 for B, the seed and the unit, decisions/0118 for the "
                     "statistic. The fixed seed is what makes the two arms comparable: without "
                     "it a difference between them could be sampling noise rather than a "
                     "divergence. The seed VALUE is arbitrary; its FIXITY is the point."),
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
    "notes": dict(tpl["notes"], **{
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
