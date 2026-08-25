"""Step 9, arm `a`, stage 2: write the arm file into Step 8b's schema.

NO CONVERSION LAYER. Every figure is written into the schema's own shapes from the stage-1
measurement file; nothing is emitted in a private shape and translated, because a translation is
a second definition of every figure it touches.

Writes artifacts/step9-headline-a.json and runs src/step8b_validate.py against it.
"""
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/Users/alyanashantel/Documents/season2-study"
sys.path.insert(0, os.path.join(ROOT, "src"))

import step8b_schema as G                      # noqa: E402  (the adopted-rule READER)
from step8b_validate import validate_file      # noqa: E402

MEAS = json.load(open(os.path.join(ROOT, "processed", "step9", "a", "measured.json")))
# decisions/0124 constraint (i): the frame's SUPPORT, measured per arm and per population by
# stage 7. Read, never typed -- the numbers below are this file's only statement of them and a
# typed constant would be a second definition of a figure another script measured.
FSUP = json.load(open(os.path.join(ROOT, "processed", "step9", "a", "frame_support.json")))
TMPL = json.load(open(os.path.join(ROOT, "artifacts", "step8b-placeholder-arm-file.json")))
S8ARMS = json.load(open(os.path.join(ROOT, "processed", "step8", "a", "arms.json")))
S8POS = json.load(open(os.path.join(ROOT, "processed", "step8", "a", "positions.json")))

OUT_JSON = os.path.join(ROOT, "artifacts", "step9-headline-a.json")
ARM = "a"
STEP = "step9"
B = MEAS["bootstrap_settings"]["B"]
SEED = MEAS["bootstrap_settings"]["seed"]
BREF = "a_default"
REV = G._read_adopted_rule_revision()
BUILD_TAG = "step9/a/2026-08-25"
ARM_GRID = [38, 46, 77, 91, 107, 108, 150, 213]

SRC_S8 = "decisions/0070 rulings 1 and 7; consumed from processed/step8/a/, build " \
         + S8ARMS["build"]["build_tag"]


def sha12(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def r6(x):
    return round(float(x), 6)


def pct(num, den):
    return r6(100.0 * num / den)


# ---------------------------------------------------------------------------------------------
# arm identity
# ---------------------------------------------------------------------------------------------
ARMS_SPEC = [
    dict(key="W108_s2_finale", arm_id=f"W108_s2_finale__{STEP}__r{REV['revision']}",
         W=108, origin="s2_finale", in_grid=True, primary=True,
         s8key=108, has_producer=True,
         origin_note=(
             "The adopted arm. T0 is the later of the S2 finale air date and the first-pass S1 "
             "completion date, W = 108 d (decisions/0026), H = 91 d, so tau1 = T0 + 108 d and "
             "tau2 = T0 + 199 d. This entry is Step 9's measurement at that setting; Step 13's "
             "entry at the same W is a different measurement and occupies its own key.")),
    dict(key="W091_s2_finale", arm_id=f"W091_s2_finale__{STEP}__r{REV['revision']}",
         W=91, origin="s2_finale", in_grid=True, primary=False,
         s8key=91, has_producer=True,
         origin_note=(
             "The finale-anchored 91-day arm. It is NOT the Netflix arm: it holds the origin "
             "fixed at the S2 finale and moves only the window, so that the difference between "
             "the primary arm and the premiere-anchored 91-day arm can be split into a window "
             "part and an origin part instead of being read as one movement. The spec asks "
             "Step 9 for two headlines; this third entry is a supporting measurement and is "
             "labelled as one.")),
    dict(key="W091_s2_premiere", arm_id=f"W091_s2_premiere__{STEP}__r{REV['revision']}",
         W=91, origin="s2_premiere", in_grid=False, primary=False,
         s8key=None, has_producer=False,
         origin_note=(
             "Netflix's own 91-day reporting window, so the result is commensurable with the "
             "public argument. T0 is the later of the S2 PREMIERE air date and the first-pass "
             "S1 completion date, because Netflix's window runs from release. THIS ARM SITS ON "
             "A DIFFERENT ORIGIN FROM THE PRIMARY HEADLINE AND THE TWO ARE NOT THE SAME "
             "MEASUREMENT AT TWO WINDOW LENGTHS. It is run on the primary arm's right-censored "
             "row set, which is what 'both arms run on the same right-censored population, "
             "max(W, 91) + H' asks for; the alternative reading and its cost are stated in "
             "spec_choices_this_arm_made at the primary arm.")),
]

POP_DEF = {
    "APPLY": ("APPLY: waterfall line 1 less D10 -- the S1-completer pair population on frame "
              "shows, right-censored, with no requirement of S2 evidence. It is the population "
              "the liveness filter is applied to, and it is Step 8's figure, not this arm's."),
    "DERIV": ("DERIV: waterfall line 4 less D10 -- the same population restricted to pairs "
              "carrying S2 evidence. Step 8 emits it so that nothing downstream rebuilds it; "
              "this arm consumes it and does not."),
}


# ---------------------------------------------------------------------------------------------
# the pieces
# ---------------------------------------------------------------------------------------------
def endpoint(num, den, pop, label, attainable, note):
    return {"percent": pct(num, den), "numerator_pairs": int(num), "denominator_pairs": int(den),
            "population": pop, "population_n": int(den), "population_label": label,
            "attainable": attainable, "note": note}


def ci_level(arm_key, pop, outcome):
    b = MEAS["bootstrap"][f"{arm_key}|{pop}|{outcome}"]["level"]
    return {"level_pct": 95, "lower": r6(b["lower"]), "upper": r6(b["upper"]),
            "method": "percentile_bootstrap", "bootstrap_ref": BREF, "B": B, "seed": SEED,
            "statistic": "levels", "resampling_unit": "account",
            "quantity_class": "outcome_shares",
            "note": ("The LEVEL of this share. Percentile interval over 10,000 resamples of "
                     "ACCOUNTS -- pairs are not independent, one account contributes many, and "
                     "pair-level resampling would understate this width. It is not comparable "
                     "with a paired movement: see $.declared_intervals.")}


HORIZON = {"never_started": None, "started_and_left": None, "continued": None}

SHARE_NOTE = {
    "never_started": ("|A| = 0, read at tau1. It is a 108-day statement at the primary arm and "
                      "a 91-day one at the other two, and it is NOT measured like Continued."),
    "started_and_left": ("|A| >= 1 and not the Continued condition. The Continued condition it "
                         "negates is read at tau2, so this state is settled at tau2 even though "
                         "entry into it is settled at tau1."),
    "continued": ("|A| >= 1 and F2 in A_H and |A_H| >= ceil(0.90 x L2), read at tau2. This is "
                  "an observed count on the post-liveness row set; it does NOT replace the "
                  "ceiling in bounds.continued, which is on the position-5 row set."),
}


def shares_block(arm_key, pop, m, W):
    c7 = m[pop]["post_liveness_counts"]
    n7 = m[pop]["n_post_liveness"]
    out = {}
    for outcome in ("never_started", "started_and_left", "continued"):
        out[outcome] = {
            "value_percent": pct(c7[outcome], n7),
            "numerator_pairs": c7[outcome], "denominator_pairs": n7,
            "on_population": pop, "on_population_n": n7,
            "on_population_label": "post-liveness (position 7)",
            "ci": ci_level(arm_key, pop, outcome),
            "is_an_observed_count_not_a_bound": True,
            "horizon_days": W if outcome == "never_started" else W + 91,
            "note": SHARE_NOTE[outcome],
        }
    return out


QUAL = "insertion_dormancy_covering"


def bounds_block(pop, m):
    d = m[pop]
    n = d["n_position_5"]
    c5 = d["position_5_counts"]
    ex = d["exclusions"]
    ch = d["channel_pairs_last_insertion_in_tau1_tau2"]
    ns5, sl5, ct5 = c5["never_started"], c5["started_and_left"], c5["continued"]
    ex_ns, ex_sl, ex_t = (ex["never_started_component"], ex["started_and_left_component"],
                          ex["total"])
    ch_sl, ch_ns = ch["started_and_left"], ch["never_started"]
    LBL = "position 5"

    ns_floor_n, ns_ceil_n = ns5 - ex_ns, ns5
    sl_floor_n, sl_ceil_n = sl5 - ex_sl - ch_sl, sl5 + ex_ns
    sub_ceil_n = sl5
    ct_ceil_n = ct5 + ex_t + ch_sl

    # THE CORNERS. Each is a COMPLETE allocation of the conceded pairs, so its three values sum
    # to 100 exactly -- which is what makes a corner attainable rather than merely arithmetic.
    #   face      nothing conceded: every scored state at face value
    #   all_sl    the never-started exclusions are in truth started-and-left
    #   sl_floor  the started-and-left exclusions and the conceded retained pairs are Continued
    #   all_ct    both of the above concessions taken at once
    corner_face = (pct(ns5, n), pct(sl5, n), pct(ct5, n))
    corner_all_sl = (pct(ns_floor_n, n), pct(sl_ceil_n, n), pct(ct5, n))
    corner_sl_floor = (pct(ns5, n), pct(sl_floor_n, n), pct(ct5 + ex_sl + ch_sl, n))
    corner_all_ct = (pct(ns_floor_n, n), pct(sl_floor_n, n), pct(ct_ceil_n, n))
    for label, corner in (("face", corner_face), ("all_sl", corner_all_sl),
                          ("sl_floor", corner_sl_floor), ("all_ct", corner_all_ct)):
        assert abs(sum(corner) - 100.0) < 1e-3, (label, corner, sum(corner))

    def corner_row(name, trio, note):
        return {"corner": name, "never_started_percent": trio[0],
                "started_and_left_percent": trio[1], "continued_percent": trio[2], "note": note}

    ns_degen = (ex_ns == 0)
    ns_bound = {
        "floor": endpoint(ns_floor_n, n, pop, LBL, True,
                          "Every never-started liveness exclusion is in truth a started pair."),
        "ceiling": endpoint(ns_ceil_n, n, pop, LBL, True,
                            "Every never-started liveness exclusion is in truth a decline. "
                            "This ceiling equals the unfiltered never-started share on this "
                            "row set as an IDENTITY, not as a coincidence."),
        "width_pp": r6(pct(ns_ceil_n, n) - pct(ns_floor_n, n)),
        "degenerate": ns_degen,
        "degenerate_reason": (
            ("The never-started component of the liveness exclusion set is zero on this "
             "population, so the floor and the ceiling are the same number. This is a MEASURED "
             "zero width, not missing data, and the dual control is x = x here: the informative "
             "comparison between the two arms is on APPLY.") if ns_degen else None),
        "conditional_sub_interval": {
            "applicable": False, "status": "structurally_absent",
            "reason": ("The conditional sub-interval conditions on this bound's own exclusion "
                       "set, so for never-started it does not exist. The slot is present and "
                       "says so, because an absent field and an inapplicable one must not look "
                       "alike."),
            "source": "task-sheet.md Step 8b; decisions/0066 §3"},
        "scope_qualifier_ref": QUAL,
        "exclusions_covered": {
            "total_pairs": ex_ns, "never_started_component": ex_ns,
            "started_and_left_component": 0,
            "accounts": ex["accounts_never_started_component"],
            "channel_pairs_conceded_by_the_floor": 0},
        "endpoints_attainable": True,
        "attainable_corners": [
            corner_row("floor", corner_all_sl,
                       f"The {ex_ns} never-started exclusions are in truth started-and-left. "
                       f"This is the SAME corner that attains the started-and-left CEILING, "
                       f"which is why those two endpoints are not independent."),
            corner_row("ceiling", corner_face,
                       "Nothing conceded: every scored state taken at face value. The three "
                       "values sum to 100 exactly, which is what makes the corner attainable.")],
        "note": (
            f"THE FLOOR IS NOT WIDENED, although {ch_ns} retained pairs on this population are "
            f"scored never-started and had their last insertion inside (tau1, tau2). The reason "
            f"is the ANCHORING, not the count: never-started is the null |A| = 0 READ AT tau1, "
            f"and every one of those pairs has an insertion after tau1 -- which is exactly what "
            f"gate decisions/0021 licenses, an insertion after the window closed proving the "
            f"account was alive. Their null is OBSERVED, not conceded. The pairs conceded by "
            f"the started-and-left floor differ because the Continued condition THEY negate is "
            f"read at tau2, and they are dormant before it."),
    }

    sl_bound = {
        "floor": endpoint(sl_floor_n, n, pop, LBL, True,
                          "WIDENED. Every started-and-left liveness exclusion, and every "
                          "retained pair that is not Continued, is live only because it "
                          "inserted after tau1, and had its last insertion inside (tau1, tau2), "
                          "is in truth Continued."),
        "ceiling": endpoint(sl_ceil_n, n, pop, LBL, True,
                            "Every never-started liveness exclusion is in truth a pair that "
                            "started and left."),
        "width_pp": r6(pct(sl_ceil_n, n) - pct(sl_floor_n, n)),
        "degenerate": False, "degenerate_reason": None,
        "conditional_sub_interval": {
            "applicable": True,
            "floor": endpoint(sl_floor_n, n, pop, LBL, True,
                              "The same widened floor: the conditioning constrains the "
                              "never-started exclusions and says nothing about the conceded "
                              "channel pairs, so this floor moves with the bound floor."),
            "ceiling": endpoint(sub_ceil_n, n, pop, LBL, True,
                                "Under the conditioning the never-started exclusions add "
                                "nothing, so the ceiling is the scored count itself."),
            "width_pp": r6(pct(sub_ceil_n, n) - pct(sl_floor_n, n)),
            "conditioning_text": (
                "The started-and-left share GIVEN that every never-started liveness exclusion "
                "is a true decline. It is a LABELLED CONDITIONAL SUB-INTERVAL and never the "
                "bound: the excluded never-started pairs rest on an untrusted |A| = 0 and some "
                "may in truth have left, so a ceiling that assumes otherwise is not a ceiling "
                "on the unconditional estimand."),
            "constrains_never_started_exclusions": ex_ns,
            "says_nothing_about_channel_pairs": ch_sl,
            "coincides_with_bound": {
                "value": bool(ex_ns == 0), "measured": True,
                "evidence": (
                    f"Measured: the never-started exclusion component on this population is "
                    f"{ex_ns}. The sub-interval ceiling is {sl5} pairs and the bound ceiling is "
                    f"{sl_ceil_n}; the two floors are the same {sl_floor_n} by construction. "
                    + ("They COINCIDE, because there is no never-started exclusion for the "
                       "conditioning to constrain."
                       if ex_ns == 0 else
                       "They do NOT coincide."))},
        },
        "scope_qualifier_ref": QUAL,
        "exclusions_covered": {
            "total_pairs": ex_t, "never_started_component": ex_ns,
            "started_and_left_component": ex_sl, "accounts": ex["accounts"],
            "channel_pairs_conceded_by_the_floor": ch_sl},
        "endpoints_attainable": True,
        "attainable_corners": [
            corner_row("floor", corner_sl_floor,
                       f"The {ex_sl} started-and-left exclusions and the {ch_sl} conceded "
                       f"retained pairs are in truth Continued, and the never-started "
                       f"exclusions are true declines, so never-started sits at its CEILING "
                       f"here."),
            corner_row("ceiling", corner_all_sl,
                       f"The {ex_ns} never-started exclusions are all in truth started and "
                       f"left. This corner attains the never-started FLOOR at the same time."),
            corner_row("floor_with_both_concessions", corner_all_ct,
                       f"A second corner attaining the same floor: the {ex_t} excluded pairs "
                       f"AND the {ch_sl} conceded retained pairs are all Continued. It attains "
                       f"the never-started floor and the Continued CEILING as well, which is "
                       f"the plainest demonstration that the three ceilings are alternatives.")],
        "note": ("Taken over ALL liveness exclusions, not over the started-and-left component "
                 "alone, and widened on the floor side only -- the conceded pairs are already "
                 "counted as started-and-left in the ceiling. The ground for the widening is "
                 "ADMISSIBILITY, not plausibility: a floor is a worst case, so no margin "
                 "statistic enters it."),
    }

    ct_bound = {
        "ceiling": endpoint(ct_ceil_n, n, pop, LBL, True,
                            "Every excluded pair, and every conceded retained pair, is in truth "
                            "Continued."),
        "floor": {"status": "not_published",
                  "reason": ("Continued is never emitted as a point and no floor is published "
                             "for it. The ceiling exists because any EXCLUDED pair may in truth "
                             "be Continued; that does not license a point estimate."),
                  "source": "decisions/0050; decisions/0052 §2",
                  "decided_by": "Human Lead"},
        "must_not_be_read_as_a_point": True,
        "scope_qualifier_ref": QUAL,
        "exclusions_covered": {
            "total_pairs": ex_t, "never_started_component": ex_ns,
            "started_and_left_component": ex_sl, "accounts": ex["accounts"],
            "channel_pairs_conceded_by_the_floor": ch_sl},
        "note": (f"The {ch_ns} retained never-started pairs whose last insertion falls inside "
                 f"(tau1, tau2) do NOT enter this numerator: Continued requires |A| >= 1 and "
                 f"their |A| = 0 is observed at tau1 on a live account, so they cannot be "
                 f"Continued however the dormancy is read."),
    }

    sum_pct = pct(ns_ceil_n + sl_ceil_n + ct_ceil_n, n)
    ceilings = {
        "simultaneous": False,
        "sum_percent": sum_pct,
        "excess_pp": r6(sum_pct - 100.0),
        "excess_pairs": int(2 * ex_ns + ex_sl + ch_sl),
        "excess_mechanism_expression":
            "2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs",
        "note": (f"THE THREE CEILINGS CANNOT ALL HOLD. Each never-started exclusion appears in "
                 f"ALL THREE ceiling numerators -- excess 2 each -- and each started-and-left "
                 f"exclusion in TWO, excess 1 each; the {ch_sl} conceded retained pairs enter "
                 f"the Continued ceiling while remaining in the never-started and "
                 f"started-and-left ceilings' own row set, excess 1 each. On this population "
                 f"that is 2 x {ex_ns} + {ex_sl} + {ch_sl} = {2 * ex_ns + ex_sl + ch_sl} pairs. "
                 f"They are ALTERNATIVE WORST CASES OVER ONE SET, not simultaneous ones."),
    }
    return {"never_started": ns_bound, "started_and_left": sl_bound,
            "continued": ct_bound}, ceilings


CONV = "arm_a_convention__account_clustered_level_ci_width_same_population_same_arm"
CONV_DEF = ("This arm divides a bound width by the width of the account-clustered percentile "
            "bootstrap interval on the LEVEL of the SAME outcome, on the SAME population and "
            "the SAME W arm. Both are in percentage points, so the ratio is dimensionless. It "
            "is a named input, not a fact about the study: the two arms may divide by different "
            "denominators and the spec forbids reconciling them.")


def ratios_block(arm_key, pop, m, bounds):
    def w(outcome):
        b = MEAS["bootstrap"][f"{arm_key}|{pop}|{outcome}"]["level"]
        return b["upper"] - b["lower"]

    def blk(numerator_pp, outcome, numdef):
        if numerator_pp == 0:
            numdef += (" It is ZERO on this population because the bound is degenerate, so the "
                       "ratio is a measured zero and not a missing value.")
        return {"value": r6(numerator_pp / w(outcome)),
                "convention_label": CONV, "convention_definition": CONV_DEF,
                "numerator_definition": numdef,
                "denominator_definition": (
                    f"The width of the 95% account-clustered percentile bootstrap interval on "
                    f"the LEVEL of the {outcome.replace('_', ' ')} share, {pop}, this arm."),
                "reconciled_with_other_arm": False}

    return {
        "never_started": blk(bounds["never_started"]["width_pp"], "never_started",
                             "The never-started bound width, in percentage points."),
        "started_and_left": blk(bounds["started_and_left"]["width_pp"], "started_and_left",
                                "The started-and-left bound width, in percentage points."),
        "started_and_left_sub_interval": blk(
            bounds["started_and_left"]["conditional_sub_interval"]["width_pp"],
            "started_and_left",
            "The conditional sub-interval width, in percentage points."),
    }


# Every paired movement this arm measured, in the order it is published. Built here rather than
# at the emission site below because SPEC_CHOICES states how many of them carry a negative
# endpoint, and a typed count would be a second definition of a figure this file computes.
MOVEMENTS = [(spec, pop, outcome,
              r6(MEAS["bootstrap"][f"{spec['key']}|{pop}|{outcome}"]["movement"]["lower"]),
              r6(MEAS["bootstrap"][f"{spec['key']}|{pop}|{outcome}"]["movement"]["upper"]))
             for spec in ARMS_SPEC
             for pop in ("APPLY", "DERIV")
             for outcome in ("never_started", "started_and_left", "continued")]
N_MOVEMENTS = len(MOVEMENTS)
N_MOVEMENTS_NEGATIVE = sum(1 for *_x, lo, hi in MOVEMENTS if lo < 0 or hi < 0)

# The frame's MEMBERSHIP and its SUPPORT, read from stage 7 rather than typed. decisions/0124
# constraint (i): membership is arm-independent, support is not, and a field that declares the
# frame arm-independent without saying which of the two it means is the claim 0124 was written
# to stop.
FRAME_MEMBERSHIP = FSUP["frame_membership_accounts"]
SUPPORT_P5 = {pop: [FSUP["support"][f"{s['key']}|{pop}|p5"]["contributing_accounts"]
                    for s in ARMS_SPEC] for pop in ("APPLY", "DERIV")}
SUPPORT_ARM_ORDER = " / ".join(s["key"] for s in ARMS_SPEC)


def _series(pop):
    return " / ".join(f"{n:,}" for n in SUPPORT_P5[pop])


SPEC_CHOICES = [
    "THE FRAME, THE DRAW ORDER AND THE DRAW MECHANISM ARE FIXED BY THE SPEC, and this arm "
    "records no choice on any of them: decisions/0124 fixes the resampling frame and the draw "
    "order, decisions/0125 fixes the mechanism. WHAT THIS ARM COMPLIES WITH, STATED SO THE DIFF "
    "CAN SEE IT: the frame is every account with at least one pair in the POSITION-4 output, "
    f"built once and drawn for every quantity regardless of how much it contributes -- "
    f"{FRAME_MEMBERSHIP:,} accounts; one generator seeded once per file, its stream consumed "
    "continuously and never re-seeded per group, so every quantity is evaluated against the "
    "same replicate set; and the draw is numpy.random.default_rng at seed 20260818 calling "
    "rng.integers(0, n_frame, size=(m, n_frame)), with the weights formed by counting the drawn "
    "indices. WHAT THE SPEC LEAVES OPEN, AND IS THIS ARM'S CHOICE, IS THE CHUNKING AND ONE "
    "KEYWORD. decisions/0125 SS3 deliberately does not specify the chunk, on the ground that a "
    "spec element earns its place by determining the output; this arm used 200, and the "
    "replicate-set selftest redraws at a different chunk and gets a bit-identical matrix, so "
    "the choice is measured inert rather than assumed to be. THIS ARM ALSO PASSES "
    "`dtype=np.int64` TO rng.integers, WHICH THE CALL 0125 NAMES DOES NOT CARRY. It is a "
    "deviation from the named mechanism, it is measured inert on this build -- a redraw at the "
    "same seed without the keyword is bit-identical -- and it is REPORTED AND LEFT VISIBLE "
    "rather than quietly conformed, because 0125's own point is that an inert-looking mechanism "
    "difference is the thing that survived three successive fixings of this spec.",

    "WHICH TWO CONFIGURATIONS THE PAIRED MOVEMENT IS BETWEEN IS THE WRITER'S TO STATE, and the "
    "schema says so. This arm's movement is POST-LIVENESS (position 7) MINUS the "
    "outcome-conditional POSITION-5 view of the same share, on the same population and arm, "
    "resampled as one paired delta -- that is, what the liveness filter does to the headline. "
    "If ruled otherwise the movements change meaning entirely; the levels do not move.",

    "'BOTH ARMS RUN ON THE SAME RIGHT-CENSORED POPULATION, max(W, 91) + H' HAS TWO READINGS AT "
    "THE PREMIERE-ANCHORED ARM, and this arm took the first. Reading (a): the 91-day arm is "
    "measured on the primary arm's position-5 row set, censored at max(108, 91) + 91 = 199 d. "
    "Reading (b): D10 is re-derived at W = 91, censoring at 182 d. MEASURED, not assumed: "
    "reading (b) is a strict superset -- 197,007 against 196,654 on APPLY and 147,685 against "
    "147,370 on DERIV, with 0 pairs in (a) and not in (b) -- so the choice moves 353 and 315 "
    "pairs. AND THE DIFFERENCE IS THE W TERM, NOT THE ORIGIN: the premiere-anchored and "
    "finale-anchored censoring sets at W = 91 are IDENTICAL, because the Step 2 frame caps the "
    "S2 finale at 2025-12-31, earlier than the binding cutoff, so T0's max() is decided by the "
    "S1 completion date on every pair the cutoff can reach and that term does not move with the "
    "origin. Reported, not reconciled.",

    "THIS FILE FILLS $.arm_grid_days, WHICH IT DOES NOT OWN. The block's owner is step13 and "
    "the schema requires it at the top level, so as first writer this arm filled it with the "
    "eight values the Human Lead ruled at decisions/0075 -- 38 / 46 / 77 / 91 / 107 / 108 / 150 "
    "/ 213. IT IS NOT THIS ARM'S FIGURE: it is transcribed from that ruling, not measured here, "
    "and Step 13 is dual, so a value neither of Step 13's arms wrote must be visible as such at "
    "the diff rather than inferred.",

    f"SIGN DOES NOT GOVERN PUBLICATION: ALL {N_MOVEMENTS} OF THIS ARM'S PAIRED-MOVEMENT "
    f"INTERVALS ARE IN $.declared_intervals, AND {N_MOVEMENTS_NEGATIVE} OF THEM CARRY A "
    f"NEGATIVE ENDPOINT. A CI endpoint's type follows its statistic: a MOVEMENT endpoint is a "
    f"percentage-point difference, typed $defs.pp, which may be zero and may be negative, and "
    f"it is negative wherever the liveness filter LOWERS the share; a LEVEL endpoint is a "
    f"percentage on [0, 100], typed $defs.percent, where a negative value is not a possible "
    f"measurement. No interval was dropped by sign, clamped or re-signed. If the two endpoint "
    f"types were ever collapsed into one, this arm would either have to withhold "
    f"{N_MOVEMENTS_NEGATIVE} measurements or publish a level that cannot exist.",

    "ONE NOTE OF STEP 8b's WAS DROPPED RATHER THAN CARRIED OR REWRITTEN. $.notes is Step 8b's "
    "structural block, carried verbatim here, and its `reading_a_placeholder` entry reads "
    "\"Check $.placeholder before reading anything else. This file's flag is true.\" That is "
    "FALSE in a real file. Rewriting it would put this arm's words inside another step's block; "
    "carrying it would publish a false sentence. It is omitted, and the omission is named here "
    "so it is visible at the diff rather than inferred from a missing key.",

    "THE THIRD ARM IS A SUPPORTING MEASUREMENT, NOT A THIRD HEADLINE. The spec asks Step 9 for "
    "the headline at W and again at 91 days on the premiere origin. This file also carries the "
    "finale-anchored 91-day arm, so that the premiere arm's movement can be split into a window "
    "part and an origin part rather than read as one. It is labelled in_arm_grid and not "
    "primary, and every figure in it is Step 8's at that arm, reproduced here and agreeing "
    "exactly.",
]


# ---------------------------------------------------------------------------------------------
# per-arm entries
# ---------------------------------------------------------------------------------------------
def waterfall(pop, m, s8arm):
    n1 = S8POS[f"waterfall_{pop}"]["position_1_step2_frame"]
    p4 = m["right_censoring_two_lines"][pop]["n_in_position_4"]
    two = m["right_censoring_two_lines"][pop]
    p5 = m[pop]["n_position_5"]
    p6 = m[pop]["n_post_liveness"]
    ex = m[pop]["exclusions"]["total"]
    inert1 = ("Waterfall line 1 is already the frame: the base is the S1-completer pair "
              "population ON FRAME SHOWS, so the frame join cannot remove a row that is in the "
              "base. A zero here is evidence the rule CANNOT FIRE, never that it found nothing.")
    inert2 = ("Line 1 is already the L2 > 1 population and no show in the Step 2 frame has "
              "L2 = 1, so the filter has nothing to fire on from either direction.")
    inert3 = ("The POSITION is inert because line 1 is already the S1-completer population. THE "
              "RULE IS NOT INERT: it removes 58,345 pairs upstream of line 1, the study's "
              "largest single exclusion.")
    inert7 = ("Outcome assignment ANNOTATES and removes nothing: every position-6 row receives "
              "exactly one of the three states.")
    pos = [
        dict(position=1, filter="step2_frame", n_in=n1, n_out=n1, removed=0, inert=True,
             inert_reason=inert1, outcome_conditional=False),
        dict(position=2, filter="L2_eq_1_exclusion", n_in=n1, n_out=n1, removed=0, inert=True,
             inert_reason=inert2, outcome_conditional=False),
        dict(position=3, filter="s1_completion_rule", n_in=n1, n_out=n1, removed=0, inert=True,
             inert_reason=inert3, outcome_conditional=False),
        dict(position=4, filter="contamination_exclusion", n_in=n1, n_out=p4, removed=n1 - p4,
             inert=False, inert_reason=None, outcome_conditional=False),
        dict(position=5, filter="right_censoring", n_in=p4, n_out=p5, removed=p4 - p5,
             inert=False, inert_reason=None, outcome_conditional=False,
             sub_lines=[
                 dict(label="removed by the max(W, 91) term alone",
                      removed=two["removed_by_max_W_91_term"],
                      n_out=p4 - two["removed_by_max_W_91_term"],
                      note="Right-censoring publishes as two lines, not one."),
                 dict(label="removed incrementally by the + H term",
                      removed=two["removed_incrementally_by_the_plus_H_term"], n_out=p5,
                      note="The incremental cost of the horizon on top of the window term."),
             ]),
        dict(position=6, filter="liveness", n_in=p5, n_out=p6, removed=ex, inert=False,
             inert_reason=None, outcome_conditional=True,
             note=("OUTCOME-CONDITIONAL. The adopted rule's second conjunct is NOT Continued, "
                   "so line 6 cannot be read without the outcome. |A| = 0 is evaluated before "
                   "liveness applies, which is permitted because both are row-local predicates "
                   "on the position-5 output and commute exactly.")),
        dict(position=7, filter="outcome_assignment", n_in=p6, n_out=p6, removed=0, inert=True,
             inert_reason=inert7, outcome_conditional=False),
    ]
    mono = all(pos[i]["n_out"] <= pos[i]["n_in"] for i in range(7))
    return {"population": pop, "written_by_step": STEP, "figures_owned_by_step": "step8",
            "order_ref": "decisions/0029 positions 1-7", "positions": pos,
            "monotone_check": {"operator": ">=", "result": bool(mono), "positions_checked": 7}}


def air_period(pop, s8arm):
    key = f"retained_per_air_period_{pop}"
    denom = S8ARMS["censoring_denominator"][f"{pop}_position_4_by_air_period"]
    rows = []
    for period, v in s8arm[key].items():
        rows.append({"air_period": period, "retained_pairs": v["retained"],
                     "entering_pairs": denom[period],
                     "retained_share_percent": pct(v["retained"], denom[period])})
    return {"population": pop, "written_by_step": STEP, "figures_owned_by_step": "step8",
            "measured_after": "position 4 (the mandated order censors the position-4 output)",
            "rows": rows}


NO_PRODUCER = {
    "block_is_absent": True, "status": "no_producer_in_spec",
    "reason": ("No step in the spec produces this block for a premiere-anchored arm. Step 8 "
               "builds the waterfall at the adopted finale-anchored arm, Step 10 charts the "
               "headline arm, and Step 13's W grid is finale-anchored at every one of its eight "
               "arms. The slot is present and says so rather than carrying a figure that would "
               "have to be invented here."),
    "source": "task-sheet.md Steps 8, 10 and 13; decisions/0114 E13",
    "owning_step": "none"}

# Every figure this file publishes at a finale-anchored arm is Step 8's. That claim is
# ESTABLISHED here rather than asserted: this arm's own recomputation is compared against Step
# 8's published arm table, and a mismatch is a hard stop.
S8_AGREEMENT = []
for _spec in ARMS_SPEC:
    if _spec["s8key"] is None:
        continue
    _m = MEAS["arms_measured"][_spec["key"]]
    _s8 = [x for x in S8ARMS["arms"] if x["W_days"] == _spec["s8key"]][0]
    for _pop in ("APPLY", "DERIV"):
        pairs = [(f"position_5_{_pop}", _m[_pop]["n_position_5"], _s8[f"position_5_{_pop}"])]
        for _k, _v in _s8[f"liveness_exclusions_{_pop}"].items():
            pairs.append((f"liveness_{_pop}.{_k}", _m[_pop]["exclusions"][_k], _v))
        for _k, _v in _s8[f"position_7_{_pop}"].items():
            pairs.append((f"position_7_{_pop}.{_k}", _m[_pop]["post_liveness_counts"][_k], _v))
        for _name, _mine, _theirs in pairs:
            if _mine != _theirs:
                raise SystemExit(f"STEP 8 AGREEMENT FAILED at W={_spec['s8key']}: "
                                 f"{_name}: mine {_mine} != step8 {_theirs}")
            S8_AGREEMENT.append(_name)
print(f"step 8 agreement: {len(S8_AGREEMENT)} figures compared at the two finale-anchored "
      f"arms, 0 mismatches")

arms_out = []
for spec in ARMS_SPEC:
    m = MEAS["arms_measured"][spec["key"]]
    s8arm = ([x for x in S8ARMS["arms"] if x["W_days"] == spec["s8key"]][0]
             if spec["s8key"] else None)
    headline = {}
    for pop in ("APPLY", "DERIV"):
        bounds, ceilings = bounds_block(pop, m)
        payload = {
            "producing_arm": ARM, "written_by_step": STEP, "written_by": "Step 9, arm a",
            "shares": shares_block(spec["key"], pop, m, spec["W"]),
            "bounds": bounds,
            "ceilings_cannot_all_hold": ceilings,
            "bound_over_sampling_width_ratios": ratios_block(spec["key"], pop, m, bounds),
        }
        if spec["primary"] and pop == "APPLY":
            payload["spec_choices_this_arm_made"] = SPEC_CHOICES
        headline[pop] = {
            "population": pop, "definition": POP_DEF[pop],
            "n_position_5": m[pop]["n_position_5"],
            "n_post_liveness": m[pop]["n_post_liveness"],
            "populations_differ_note": (
                f"THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint "
                f"in this block is stated on the POSITION-5 row set, n = "
                f"{m[pop]['n_position_5']}; every published share is on the POST-LIVENESS row "
                f"set, n = {m[pop]['n_post_liveness']}. They differ by the "
                f"{m[pop]['exclusions']['total']} pairs the liveness filter removes, and a "
                f"point estimate is therefore not guaranteed to lie inside its own bound."),
            "by_producing_arm": {
                "step_dual_status": "dual", "arms_in_this_file": "one_arm",
                "producing_step": STEP,
                "step_dual_status_source": ("CLAUDE.md, Dual implementation; task-sheet.md "
                                            "Step 9; one file per arm is decisions/0107"),
                "arms": {ARM: payload}, "arm_held": ARM},
        }
    entry = {
        "arm_id": spec["arm_id"], "W_days": spec["W"], "H_days": 91,
        "clock_origin": spec["origin"], "clock_origin_note": spec["origin_note"],
        "producing_step": STEP, "adopted_rule_revision": REV["revision"],
        "in_arm_grid": spec["in_grid"], "is_primary_headline": spec["primary"],
        "headline": headline,
    }
    if spec["has_producer"]:
        entry["waterfall"] = {p: waterfall(p, m, s8arm) for p in ("APPLY", "DERIV")}
        entry["liveness_exclusions"] = {
            p: {"total_pairs": m[p]["exclusions"]["total"],
                "never_started_component": m[p]["exclusions"]["never_started_component"],
                "started_and_left_component": m[p]["exclusions"]["started_and_left_component"],
                "accounts": m[p]["exclusions"]["accounts"],
                "silence_test_alone": m[p]["exclusions"]["silence_test_alone"],
                "spared_by_not_continued": m[p]["exclusions"]["spared_by_not_continued"],
                "identity": "silence_test_alone - spared_by_not_continued = total_pairs",
                "pair_level_not_account_level": True,
                "written_by_step": STEP, "figures_owned_by_step": "step8"}
            for p in ("APPLY", "DERIV")}
        entry["retained_by_air_period"] = {p: air_period(p, s8arm) for p in ("APPLY", "DERIV")}
    else:
        entry["waterfall"] = dict(NO_PRODUCER)
        entry["liveness_exclusions"] = dict(NO_PRODUCER)
        entry["retained_by_air_period"] = dict(NO_PRODUCER)
    entry["note"] = (
        f"One entry per (W_days, clock_origin, producing_step, adopted_rule_revision). This is "
        f"{STEP}'s measurement at W = {spec['W']} d on the {spec['origin']} clock under adopted "
        f"rule revision {REV['revision']}.")
    arms_out.append(entry)


# ---------------------------------------------------------------------------------------------
# declared intervals: the paired movements that this schema can represent
# ---------------------------------------------------------------------------------------------
declared = []
for spec, pop, outcome, lo, hi in MOVEMENTS:
    iid = f"liveness_movement__{spec['key']}__{pop}__{outcome}__{ARM}"
    declared.append({
        "interval_id": iid,
        "quantity": (
            f"A PAIRED MOVEMENT: the {outcome.replace('_', ' ')} share on {pop} at this "
            f"arm, post-liveness MINUS its outcome-conditional position-5 value, "
            f"resampled as one paired delta on the same accounts rather than as two "
            f"independent levels. It is what the liveness filter does to this share."),
        "produced_by_step": STEP, "producing_arm": ARM,
        "ci": {"level_pct": 95, "lower": lo, "upper": hi,
               "method": "percentile_bootstrap", "bootstrap_ref": BREF, "B": B,
               "seed": SEED, "statistic": "movements", "resampling_unit": "account",
               "quantity_class": "outcome_shares",
               "note": ("A MOVEMENT, not a level. It is roughly an order of magnitude "
                        "narrower than the level of the same share, so the two must "
                        "never be compared with each other.")},
        "note": (
            f"One of the two objects the spec fixes (decisions/0118). A MOVEMENT IS A "
            f"PERCENTAGE-POINT DIFFERENCE, NOT A LEVEL: it may be zero and it may be "
            f"NEGATIVE, and it is negative wherever the liveness filter LOWERS this share. "
            f"Its endpoints are typed $defs.pp for that reason, while a level's are typed "
            f"$defs.percent on [0, 100]. All {N_MOVEMENTS} of this arm's paired movements "
            f"are published here whatever their sign; {N_MOVEMENTS_NEGATIVE} carry a "
            f"negative endpoint, and none was dropped, clamped or re-signed."),
        "source": "decisions/0118; decisions/0126; decisions/0103 §1",
    })

# ---------------------------------------------------------------------------------------------
# the document
# ---------------------------------------------------------------------------------------------
inst = {
    "schema_version": TMPL["schema_version"],
    "schema_id": TMPL["schema_id"],
    "placeholder": False,
    "generated_by": {
        "generator": "src/step9_a_2_emit.py",
        "generator_sha256_12": sha12(os.path.join(ROOT, "src", "step9_a_2_emit.py")),
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "build_tag": BUILD_TAG,
        "git_head_short": subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"],
                                         capture_output=True, text=True).stdout.strip(),
        "host_step": "Step 9, headline result",
        "written_by": "Data Scientist, instance a",
        "inputs": [
            "processed/step9/a/measured.json (this arm's stage 1, "
            + sha12(os.path.join(ROOT, "processed", "step9", "a", "measured.json")) + ")",
            "processed/step8/a/outcomes.json, arms.json, positions.json (Step 8's figures)",
            "artifacts/step8b-output-schema.json",
            "artifacts/step8b-placeholder-arm-file.json (the arm-file shape)",
        ],
    },
    "document_scope": {
        "role": "arm_file", "producing_step": STEP, "arm": ARM,
        "also_written_by_steps": [],
        "isolation_rule": TMPL["document_scope"]["isolation_rule"],
        "note": ("This arm has not read the other arm's file or output folder, has not diffed "
                 "anything, and has written no cross-arm block. The diff is the Human Lead's."),
        "source": "decisions/0107; CLAUDE.md, Dual implementation",
    },
    "sentinels": TMPL["sentinels"],
    "arm_key": TMPL["arm_key"],
    "adopted_rule_revision": {k: REV[k] for k in
                              ("revision", "source_file", "source_key", "source_sha256_12",
                               "read_not_typed", "how_it_is_read", "why_it_is_in_the_key",
                               "source")},
    "arm_grid_days": ARM_GRID,
    "populations": {
        p: {**{k: v for k, v in TMPL["populations"][p].items()
               if k != "reference_n_at_the_adopted_arm"},
            "reference_n_at_the_adopted_arm":
                MEAS["arms_measured"]["W108_s2_finale"][p]["n_position_5"]}
        for p in ("APPLY", "DERIV")},
    "scope_qualifiers": TMPL["scope_qualifiers"],
    "bootstrap_spec": TMPL["bootstrap_spec"],
    "binding_clusters": TMPL["binding_clusters"],
    "bootstrap_settings": {
        BREF: {
            "B": B, "seed": SEED, "statistics": ["levels", "movements"],
            "resampling_unit": "account", "producing_arm": ARM, "spec_status": "fixed_in_spec",
            # SEVEN ELEMENTS, NOT FOUR. decisions/0124 fixed the resampling frame and the draw
            # order and decisions/0125 fixed the draw mechanism; a universe that still names
            # only four leaves three fixed elements out of the record entirely, and the
            # partition then holds over a universe this writer chose. The schema's own anchor
            # says a fifth element may be added and none of the original four may be dropped.
            "fields_considered": ["B", "seed", "resampling_unit", "statistics",
                                  "resampling_frame", "draw_order", "draw_mechanism"],
            "fields_fixed_in_spec": ["B", "seed", "resampling_unit", "statistics",
                                     "resampling_frame", "draw_order", "draw_mechanism"],
            "fields_not_fixed_in_spec": [],
            "note": ("Every element is fixed by the spec and identical for both arms -- "
                     "decisions/0103 for B, the seed and the unit, decisions/0118 for the "
                     "statistic, decisions/0124 for the resampling frame and the draw order, "
                     "decisions/0125 for the draw mechanism. THIS ENTRY RECORDS NO PER-ARM "
                     "CHOICE ON ANY OF THEM. THE FRAME IS ARM-INDEPENDENT IN ITS MEMBERSHIP AND "
                     "NOT IN ITS SUPPORT, and this sentence describes the DRAW: the same "
                     f"{FRAME_MEMBERSHIP:,} accounts are drawn at every arm in this file, "
                     "because the position-4 output does not contain W. The CONTRIBUTING subset "
                     "does move with the arm, because the censoring rule carries max(W, 91): at "
                     f"position 5, over {SUPPORT_ARM_ORDER}, it is {_series('APPLY')} on APPLY "
                     f"and {_series('DERIV')} on DERIV. Accounts that are drawn and contribute "
                     "nothing are part of the population the uncertainty is about and are not "
                     "dropped from the frame; the per-arm, per-population table is in this "
                     "arm's .md and in artifacts/step9-working-figures-a.json, measured by "
                     "src/step9_a_7_frame_support.py."),
        }},
    "step_duality": TMPL["step_duality"],
    "declared_intervals": declared,
    "block_ownership": TMPL["block_ownership"],
    "channel_classes": TMPL["channel_classes"],
    "discovery_channel_overlap": TMPL["discovery_channel_overlap"],
    "derived_fields": TMPL["derived_fields"],
    "arms": arms_out,
    "spec_choices_made_by_step_8b": TMPL["spec_choices_made_by_step_8b"],
    "known_limits_of_this_schema": TMPL["known_limits_of_this_schema"],
    # $.notes is Step 8b's structural block and is carried verbatim -- EXCEPT for
    # `reading_a_placeholder`, whose text is "This file's flag is true." That is FALSE in a real
    # file. It is DROPPED rather than rewritten: rewriting would put this arm's words into
    # another step's block, and carrying it would publish a false sentence.
    "notes": {k: v for k, v in TMPL["notes"].items() if k != "reading_a_placeholder"},
}

with open(OUT_JSON, "w") as fh:
    json.dump(inst, fh, indent=1)
    fh.write("\n")

report = validate_file(OUT_JSON, os.path.join(ROOT, "artifacts", "step8b-output-schema.json"))
print(json.dumps({k: report[k] for k in
                  ("checks_total", "checks_passed", "checks_not_applicable",
                   "checks_empty_declared", "checks_failed", "ok")}, indent=1))
print("schema errors:", report["schema_validation"]["error_count"],
      "measurement slots:", report["schema_validation"]["measurement_slots_applied"])
for e in report["schema_validation"]["errors"][:20]:
    print("  SCHEMA:", e)
for c in report["semantic_checks"]:
    if c["status"] in ("FAIL", "VACUOUS"):
        print("  ", c["id"], c["status"], c["title"])
        for f in c["failures"][:6]:
            print("      -", f)
_mv_declared = [d for d in declared if d["ci"]["statistic"] == "movements"]
_mv_negative = [d for d in _mv_declared
                if d["ci"]["lower"] < 0 or d["ci"]["upper"] < 0]
print("paired movements measured:", N_MOVEMENTS,
      "| published in $.declared_intervals:", len(_mv_declared),
      "| of those, carrying a negative endpoint:", len(_mv_negative))
if len(_mv_declared) != N_MOVEMENTS:
    raise SystemExit(f"SIGN-BLIND EMISSION FAILED: {N_MOVEMENTS} movements measured, "
                     f"{len(_mv_declared)} published. No interval may be withheld.")
for d in _mv_negative:
    print("    negative endpoint, published:", d["interval_id"],
          [d["ci"]["lower"], d["ci"]["upper"]])
with open(os.path.join(ROOT, "logs", "step9", "a_validate.json"), "w") as fh:
    json.dump(report, fh, indent=1)
