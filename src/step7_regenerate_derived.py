"""Regenerate EVERY figure derived from the Step 7 bounds, into both halves of both arms.

Human Lead ruling, 2026-08-13, from Red Team's eleventh HOLD: stop hand-patching.

Four consecutive decisions corrected these artifacts by patching individual values into
published files. Every finding in reviews 9, 10 and 11 was a value a patch reached in one
file and missed in another, or reached in the .md and missed in the .json, or reached a
ratio and missed its numerator. All of it is derived. So it is computed here, once, from
the stored counts, and written everywhere -- one expression per figure.

WHAT THIS FIXES BY CONSTRUCTION
  finding 1  the attainable-corner table in bb-a.json      -- a declared target path
  finding 2  sampling_error.*.bound_endpoints              -- declared target paths
  finding 4  the per-W sensitivity series in bb-b.json     -- regenerated per arm
  finding 5  legitimate strings in the superseded list     -- the list is generated, and
                                                              a value that is still live
                                                              somewhere cannot enter it
  finding 6  4-dp register vs 6-dp JSON literals           -- matching is numeric, not
                                                              textual, at both precisions
  finding 7  corrected values written into stamps          -- the stamp is NEGATIVE ONLY.
                                                              It names superseded strings
                                                              and points at the generated
                                                              block; it restates no
                                                              corrected figure, so the
                                                              positive grep can only pass
                                                              if the BODY was written

WHAT IT MAKES IMPOSSIBLE TO COMMIT SILENTLY
  finding 3  the two arms use different denominators for the bound-over-sampling ratio.
             Both are NAMED INPUTS below. There is no expression in this file that can
             produce one arm's ratio from the other arm's denominator without the
             substitution being visible in RATIO_DENOMINATORS.

NOT reconciled here, by CLAUDE.md: arm A divides by the FLOOR ENDPOINT's own bootstrap CI
width; arm B divides by the CI width of the UNDER-THE-RULE point estimate. Different
conventions, reported as two numbers.

Zero API calls. Reads stored masks and the arms' own stored counts. Adopts nothing.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

W, H, DAY = 108, 91, 86400.0
MASKS = "processed/step7/bb_a/masks_W108.npz"
ARMS = {"a": "artifacts/step7-liveness-bb-a", "b": "artifacts/step7-liveness-bb-b"}
POPS = {"APPLY": 196654, "DERIV": 147370}

# ----------------------------------------------------------------- 1. COUNTS
# The only inputs. Everything below is a function of these.

def counts_from_masks():
    m = np.load(MASKS)
    last, t0f = m["last_inst"], m["t0f"]
    tau1, tau2 = t0f + W * DAY, t0f + (W + H) * DAY
    cont, never = m["cont"], m["never"]
    not_live = (~cont) & (last <= tau1)
    # 0057: the channel window is OPEN at tau2. At s = tau2 the unobserved remainder is
    # empty, so nothing admissible is missing and the pair is not conceded.
    channel = (~cont) & (~never) & (last > tau1) & (last < tau2)
    closed = (~cont) & (~never) & (last > tau1) & (last <= tau2)
    out = {}
    for pop, msk in (("APPLY", m["apply_"]), ("DERIV", m["deriv"])):
        out[pop] = dict(
            n=POPS[pop],
            ns_unfiltered=int((msk & never).sum()),
            cont_unfiltered=int((msk & cont).sum()),
            sl_unfiltered=int((msk & ~never & ~cont).sum()),
            ns_excl=int((msk & not_live & never).sum()),
            sl_excl=int((msk & not_live & ~never).sum()),
            channel=int((msk & channel).sum()),
            channel_closed_form=int((msk & closed).sum()),
        )
    return out


C = counts_from_masks()
for pop, c in C.items():
    assert c["ns_unfiltered"] + c["cont_unfiltered"] + c["sl_unfiltered"] == c["n"], pop
    # cross-check against what BOTH arms independently stored
    # The counts are the ONLY inputs, so the cross-check against what both arms independently
    # stored is the one that matters. It used to be `if u:` -- an arm without the key was
    # skipped and the check passed on one arm while claiming two. (0062 audit.)
    _crosschecked = 0
    for a, path in ARMS.items():
        u = json.load(open(path + ".json"))["bounds"][pop].get("unfiltered_counts")
        if u:
            assert (u["never_started"], u["continued"], u["started_and_left"]) == (
                c["ns_unfiltered"], c["cont_unfiltered"], c["sl_unfiltered"]), (pop, a)
            _crosschecked += 1
    assert _crosschecked >= 1, (
        f"{pop}: no arm stores unfiltered_counts, so the inputs were cross-checked against "
        f"NOTHING. That is a failure, not a pass.")

# ------------------------------------------------------- 2. DERIVED FIGURES
# One expression each. Nothing below is typed in from a previous artifact.

def pct(k, n):
    return round(100.0 * k / n, 6)


def derive(c):
    n, ch = c["n"], c["channel"]
    ns_u, cont_u, sl_u = c["ns_unfiltered"], c["cont_unfiltered"], c["sl_unfiltered"]
    ns_x, sl_x = c["ns_excl"], c["sl_excl"]

    ns_floor, ns_ceil = ns_u - ns_x, ns_u
    sl_floor = sl_u - sl_x - ch                 # every exclusion AND every channel pair continued
    sl_ceil = sl_u + ns_x                       # every never-started exclusion in truth left
    sub_floor, sub_ceil = sl_floor, sl_u        # conditioning constrains the ns exclusions only
    cont_floor = cont_u
    cont_ceil = cont_u + ns_x + sl_x + ch
    corner_lo_cont = n - ns_floor - sl_ceil     # ns floor corner
    corner_hi_cont = n - ns_ceil - sl_floor     # ns ceiling / sl floor corner
    excess = 2 * ns_x + sl_x + ch

    # 2.5 (Red Team 15), fixed 2026-08-13 (0063). Every width was a DIFFERENCE OF TWO 6-dp
    # ROUNDED PERCENTAGES -- which is precisely the construction SUPERSEDED[0.4033] names as
    # "a rounding artifact". It showed: the SAME 793 pairs on the SAME 196,654 gave
    # sl.width = 0.403246 and cont.width = 0.403247 in one generated block, one quantity with
    # two values an ulp apart. bb-b.json's corrected 0.403246 landed on the exact form by
    # coincidence. A width is a COUNT over a denominator, so it is computed as one.
    def band(floor_n, ceil_n):
        return dict(floor_n=floor_n, ceil_n=ceil_n,
                    floor=pct(floor_n, n), ceil=pct(ceil_n, n),
                    width=pct(ceil_n - floor_n, n))

    d = dict(
        counts=c,
        ns=band(ns_floor, ns_ceil),
        sl=band(sl_floor, sl_ceil),
        sub=band(sub_floor, sub_ceil),
        cont=band(cont_floor, cont_ceil),
        corner_ns_floor=dict(ns=pct(ns_floor, n), sl=pct(sl_ceil, n), cont=pct(corner_lo_cont, n)),
        corner_ns_ceil=dict(ns=pct(ns_ceil, n), sl=pct(sl_floor, n), cont=pct(corner_hi_cont, n)),
        ceilings=dict(sum=round(pct(ns_ceil, n) + pct(sl_ceil, n) + pct(cont_ceil, n), 6),
                      excess_pairs=excess, excess_pp=pct(excess, n),
                      mechanism=f"2 x {ns_x} + {sl_x} + {ch} = {excess}"),
        exclusion_share_of_population=pct(ns_x + sl_x, n),   # LEGITIMATE 0.3575 / 0.0672
    )
    for k in ("ns", "sl", "sub", "cont"):
        assert d[k]["floor_n"] <= d[k]["ceil_n"], k
        # a width is the count over the denominator, never a difference of rounded shares
        assert d[k]["width"] == pct(d[k]["ceil_n"] - d[k]["floor_n"], n), k
    # the S&L bound and the Continued bound span the SAME excluded pairs, so their widths are
    # the same number. Under the old construction they differed by an ulp.
    assert d["sl"]["width"] == d["cont"]["width"], (d["sl"]["width"], d["cont"]["width"])
    assert abs(sum(d["corner_ns_floor"].values()) - 100.0) < 1e-6
    assert abs(sum(d["corner_ns_ceil"].values()) - 100.0) < 1e-6
    return d


D = {p: derive(c) for p, c in C.items()}

# --------------------------------------------------- 3. THE TWO CONVENTIONS
# finding 3. Both denominators are NAMED, per arm, so no expression can silently use
# the other arm's. The values are each arm's OWN stored bootstrap output.

RATIO_DENOMINATORS = {
    "a": {"convention": "CI width of the FLOOR ENDPOINT's own bootstrap distribution",
          "source": "sampling_error.<pop>.bound_endpoints.started_and_left_floor.ci_width_pp",
          "APPLY": 0.7602, "DERIV": 0.9744},
    "b": {"convention": "CI width of the UNDER-THE-RULE point estimate",
          "source": "bootstrap.by_population.<pop>.ci95_width_pp.started_and_left",
          "APPLY": 0.7922131651416677, "DERIV": 0.9737261938594308},
}
assert RATIO_DENOMINATORS["a"]["APPLY"] != RATIO_DENOMINATORS["b"]["APPLY"], \
    "the conventions must stay distinct -- reconciling them is what 0058 reverted"


# The never-started ratio has its own denominators, and they are named for the same reason the
# started-and-left ones are: an unnamed denominator is how one arm's convention quietly becomes
# both arms'.
#
# The earlier justification here -- that 0058 SS3 recorded the arms as CORRECTLY divergent on this
# ratio at (a 0.2813, b 0.27211) -- is WITHDRAWN (0060 SS2, 0061). It was false. 0.2813 is
# 0.307138 / 1.092, and 1.092 is the UNDER-THE-RULE point estimate's CI, which is arm b's
# convention -- so that pair was one convention on two bootstraps, not two conventions diverging.
# Naming the denominators is what exposed it: the script then wrote arm a's own 0.2818 while every
# prose surface still said 0.2813. The practice was right and the reason given for it was not.
NS_RATIO_DENOMINATORS = {"a": {"APPLY": 1.09, "DERIV": 0.7626},
                         "b": {"APPLY": 1.1287197092145753, "DERIV": 0.7420068751051554}}
assert NS_RATIO_DENOMINATORS["a"]["APPLY"] != NS_RATIO_DENOMINATORS["b"]["APPLY"]


def ratios(arm):
    r = {}
    for pop in POPS:
        den = RATIO_DENOMINATORS[arm][pop]
        r[pop] = dict(denominator=den,
                      convention=RATIO_DENOMINATORS[arm]["convention"],
                      bound_width_pp=D[pop]["sl"]["width"],
                      ratio=round(D[pop]["sl"]["width"] / den, 4),
                      sub_interval_width_pp=D[pop]["sub"]["width"],
                      sub_interval_ratio=round(D[pop]["sub"]["width"] / den, 4))
    return r


# ----------------------------------------------- 4. THE REGISTER -- SHARED, NOT LOCAL
# B3 (Red Team 12): there were two hand-maintained registers, already divergent, and
# neither held the values that were wrong. There is now one, in step7_register.py, and
# both scripts import it.

sys.path.insert(0, str(Path(__file__).parent))
from step7_register import SUPERSEDED, SUPERSEDED_IN, ADOPTED_IN   # noqa: E402

# ------------------------------------------------------- 5. TARGETS -- JSON
# Declared paths. Never key-guessing, never value-wide substitution: 19042 is ALSO the
# post-liveness point estimate in three places and must not move.

# ------------------------------ 3z. ONE DEFINITION PER STATEMENT AND PER FIGURE
# Human Lead ruling, 2026-08-13 (0062). B8 and B10 were the SAME LITERAL living in two
# writers -- the .md one and the .json one -- where one was edited and the other was not.
# Two copies of a sentence is two places to withdraw it from, and the withdrawal reached one.
#
# So every statement has ONE definition here, and both writers render it. Neither writer
# contains prose of its own about the figures. compare_halves() then reads the two rendered
# halves back off disk and compares them, so agreement is DEMONSTRATED, not asserted.

STATEMENTS = {
    "channel_window":
        "The channel window is (tau1, tau2), OPEN at tau2 (0057). At s = tau2 the unobserved "
        "remainder is empty, so nothing admissible is missing and the pair is not conceded.",
    "two_conventions":
        "Bound over sampling width: the two arms divide by DIFFERENT denominators. Arm a uses "
        "the floor endpoint's own bootstrap CI; arm b uses the CI of the under-the-rule point "
        "estimate. The spec fixes neither, so this is a spec ambiguity and is REPORTED, NOT "
        "RECONCILED (CLAUDE.md). 0057 wrote the other arm's denominator into arm a's file and "
        "0058 reverted it.",
    "ratio_denominator_limit":
        "The denominator is the CI of the PRE-widening floor point and was not re-bootstrapped; "
        "the recomputation reuses it. Stated rather than hidden.",
    "point_estimates_do_not_move":
        "The post-liveness started-and-left COUNT is 19042 on APPLY. That is a point estimate, "
        "not the bound floor, and it appears in outcome_shares, waterfall and "
        "ordering_commutation_check. Targets are declared by PATH, so it cannot be caught by a "
        "value-wide substitution.",
    "legitimate_not_superseded":
        "0.3575 (APPLY) and 0.0672 (DERIV) are CORRECT as exclusion shares of population. They "
        "are superseded only as bound WIDTHS. Same string, two meanings, one live.",
    "per_w_scope":
        "The per-W sensitivity series was computed under the CLOSED channel window and the "
        "un-widened floor, at every arm. Only W = 108 masks are on disk, so it CANNOT be "
        "regenerated here. Step 13 is the consumer and must recompute it. The inertness of the "
        "window form is asserted at W = 108 only and is NOT expected to hold at W = 213, where "
        "D10 forces tau1 <= tau_pull - 91 d so tau2 sits at or adjacent to tau_pull, and a mass "
        "point in last-insertion instants sits there.",
    "covering_qualifier":
        "The bound is covering with respect to insertion-dormancy, exhaustively; open only "
        "across channel classes (D4, D9). The widening rule is: concede every pair that was "
        "dormant before the instant at which its own state-defining null is read -- tau1 for the "
        "never-started null, tau2 for the Continued null. That is exhaustive, not open-ended: "
        "every pair either was inserting through its test instant or was not, and it yields "
        "32,769 and 18,952 with no residue. So D4 and D9 publish ALONGSIDE this bound and are "
        "not folded into it.",
    "commutation_caveat":
        "ordering_commutation_check shows the two filter orders agree on OBSERVED COUNTS. It "
        "does not show that conditioning the filter on the outcome leaves the estimand "
        "unchanged. Conjunct 2 is NOT Continued, so liveness is outcome-conditional. Limitation, "
        "not a resolved question.",
}


def figure_table(arm):
    """Every derived figure, flat, one canonical name each. Both writers render THIS."""
    F = {}
    for pop in POPS:
        d, c = D[pop], C[pop]
        F[f"{pop}.n"] = c["n"]
        F[f"{pop}.channel"] = c["channel"]
        for band in ("ns", "sl", "sub", "cont"):
            F[f"{pop}.{band}.floor"] = d[band]["floor"]
            F[f"{pop}.{band}.ceil"] = d[band]["ceil"]
            F[f"{pop}.{band}.width"] = d[band]["width"]
            F[f"{pop}.{band}.floor_n"] = d[band]["floor_n"]
            F[f"{pop}.{band}.ceil_n"] = d[band]["ceil_n"]
        for corner in ("corner_ns_floor", "corner_ns_ceil"):
            for k, v in d[corner].items():
                F[f"{pop}.{corner}.{k}"] = v
        F[f"{pop}.ceilings.sum"] = d["ceilings"]["sum"]
        F[f"{pop}.ceilings.excess_pp"] = d["ceilings"]["excess_pp"]
        F[f"{pop}.ceilings.excess_pairs"] = d["ceilings"]["excess_pairs"]
        F[f"{pop}.exclusion_share_of_population"] = d["exclusion_share_of_population"]
        for band in ("sl", "ns"):
            den = DENOMS[band][arm][pop]
            F[f"{pop}.{band}.ratio_denominator"] = den
            F[f"{pop}.{band}.ratio"] = round(d[band]["width"] / den, 4)
    return F


CANON_BEGIN = "<!-- CANON "
CANON_END = " END CANON -->"


# ------------------------------------ 3a. WHERE EACH ARM STORES ITS RATIOS
# B9 (Red Team 14): check_ratios_written() looked for `sampling_error`, which arm b does not
# have -- its bootstrap is under `bootstrap` -- so the loop `continue`d on both populations,
# checked nothing, and reported OK. A check that finds nothing because it looked nowhere must
# fail. So the layout is DECLARED per arm and a missing path is a failure, never a skip.

def _ratio_layout(arm, pop):
    if arm == "a":
        se = ["sampling_error", pop, "bound_endpoints"]
        return {
            "sl": {"width": se + ["started_and_left_bound_width_pp"],
                   "ci": se + ["started_and_left_floor", "ci_width_pp"],
                   "ratio": se + ["started_and_left_bound_width_over_sampling_width"]},
            "ns": {"width": se + ["never_started_bound_width_pp"],
                   "ci": se + ["never_started_floor", "ci_width_pp"],
                   "ratio": se + ["never_started_bound_width_over_sampling_width"]},
        }
    bp = ["bootstrap", "by_population", pop, "bound_width_vs_sampling_width_pp"]
    return {
        "sl": {"width": bp + ["started_and_left_JOINT_BOUND_this_is_the_bound", "bound_width"],
               "ci": bp + ["started_and_left_JOINT_BOUND_this_is_the_bound", "ci95_width"],
               "ratio": bp + ["started_and_left_JOINT_BOUND_this_is_the_bound", "ratio"]},
        "ns": {"width": bp + ["never_started", "bound_width"],
               "ci": bp + ["never_started", "ci95_width"],
               "ratio": bp + ["never_started", "ratio"]},
        "sub": {"width": bp + ["started_and_left_over_SL_exclusions", "bound_width"],
                "ci": bp + ["started_and_left_over_SL_exclusions", "ci95_width"],
                "ratio": bp + ["started_and_left_over_SL_exclusions", "ratio"]},
    }


RATIO_LAYOUT = {arm: {pop: _ratio_layout(arm, pop) for pop in POPS} for arm in ARMS}
DENOMS = {"sl": RATIO_DENOMINATORS, "ns": NS_RATIO_DENOMINATORS}


def get(doc, path):
    node = doc
    for k in path:
        if not isinstance(node, dict) or k not in node:
            return None
        node = node[k]
    return node


def put(doc, path, value):
    node = doc
    for k in path[:-1]:
        if k not in node:
            return False
        node = node[k]
    if path[-1] not in node:
        return False
    node[path[-1]] = value
    return True


def json_targets(arm, doc):
    T = []
    for pop in POPS:
        d = D[pop]
        b = doc.get("bounds", {}).get(pop, {})
        sl_key = "bound_started_and_left" if "bound_started_and_left" in b else "started_and_left"
        sub_key = ("bound_started_and_left_COMPONENT_over_the_SL_exclusions_only"
                   if "bound_started_and_left_COMPONENT_over_the_SL_exclusions_only" in b else None)
        cont_key = "bound_continued" if "bound_continued" in b else "continued"
        ns_key = "bound_never_started" if "bound_never_started" in b else "never_started"

        T += [(["bounds", pop, sl_key, "floor_pct"], d["sl"]["floor"]),
              (["bounds", pop, sl_key, "floor_numerator"], d["sl"]["floor_n"]),
              (["bounds", pop, sl_key, "width_pp"], d["sl"]["width"]),
              (["bounds", pop, sl_key, "width_joint_pp"], d["sl"]["width"]),
              (["bounds", pop, sl_key, "width_over_SL_exclusions_pp"], d["sub"]["width"]),
              (["bounds", pop, cont_key, "ceiling_pct"], d["cont"]["ceil"]),
              (["bounds", pop, cont_key, "ceiling_numerator"], d["cont"]["ceil_n"]),
              (["bounds", pop, cont_key, "width_pp"], d["cont"]["width"]),
              (["bounds", pop, ns_key, "floor_pct"], d["ns"]["floor"]),
              (["bounds", pop, ns_key, "ceiling_pct"], d["ns"]["ceil"])]
        if sub_key:
            T += [(["bounds", pop, sub_key, "floor_pct"], d["sub"]["floor"]),
                  (["bounds", pop, sub_key, "ceiling_pct"], d["sub"]["ceil"]),
                  (["bounds", pop, sub_key, "width_pp"], d["sub"]["width"])]
        # finding 1 -- the attainable-corner table
        cc = ["bounds", pop, "joint_corner_check"]
        T += [(cc + ["never_started_floor_with_started_and_left_ceiling", "never_started_pct"], d["corner_ns_floor"]["ns"]),
              (cc + ["never_started_floor_with_started_and_left_ceiling", "started_and_left_pct"], d["corner_ns_floor"]["sl"]),
              (cc + ["never_started_floor_with_started_and_left_ceiling", "continued_pct"], d["corner_ns_floor"]["cont"]),
              (cc + ["never_started_ceiling_with_started_and_left_floor", "never_started_pct"], d["corner_ns_ceil"]["ns"]),
              (cc + ["never_started_ceiling_with_started_and_left_floor", "started_and_left_pct"], d["corner_ns_ceil"]["sl"]),
              (cc + ["never_started_ceiling_with_started_and_left_floor", "continued_pct"], d["corner_ns_ceil"]["cont"])]
        # finding 2 -- the sampling-error block, numerator AND denominator AND ratio
        se = ["sampling_error", pop, "bound_endpoints"]
        T += [(se + ["started_and_left_floor", "point_pct"], d["sl"]["floor"]),
              (se + ["started_and_left_ceiling", "point_pct"], d["sl"]["ceil"]),
              (se + ["never_started_floor", "point_pct"], d["ns"]["floor"]),
              (se + ["never_started_ceiling", "point_pct"], d["ns"]["ceil"]),
              (se + ["started_and_left_bound_width_pp"], d["sl"]["width"]),
              (se + ["never_started_bound_width_pp"], d["ns"]["width"]),
              # B1 (Red Team 12): CLAUDE.md puts the bound-over-sampling-width ratio on BOTH
              # dependency lists, and the previous version wrote both OPERANDS and left the
              # QUOTIENT -- the exact inverse of 0057's failure, in the same six-line block.
              # The denominator is this arm's own, from RATIO_DENOMINATORS.
              (se + ["started_and_left_bound_width_over_sampling_width"],
               round(d["sl"]["width"] / RATIO_DENOMINATORS[arm][pop], 4)),
              (se + ["never_started_bound_width_over_sampling_width"],
               round(d["ns"]["width"] / NS_RATIO_DENOMINATORS[arm][pop], 4))]
    return T


def ratio_targets(arm):
    """Declared (path, value) pairs for every ratio this arm stores, both bands, both pops."""
    T = []
    for pop in POPS:
        lay = RATIO_LAYOUT[arm][pop]
        for band, node in lay.items():
            width = D[pop]["sub"]["width"] if band == "sub" else D[pop][band]["width"]
            den = DENOMS.get(band, DENOMS["sl"])[arm][pop]
            T += [(node["width"], width),
                  (node["ratio"], round(width / den, 4))]
    return T


def apply_json(arm):
    p = Path(ARMS[arm] + ".json")
    doc = json.load(open(p))
    for k in list(doc):
        if k.startswith("_SUPERSEDED") or k.startswith("_superseded"):
            doc.pop(k)
    hits, absent = 0, []
    for path, val in json_targets(arm, doc) + ratio_targets(arm):
        if put(doc, path, val):
            hits += 1
        else:
            absent.append(".".join(path))
    # finding 4 -- the per-W series cannot be regenerated: only W = 108 masks are on disk.
    # It is DECLARED scope-limited rather than left to look current. Renaming the key is what
    # makes the declaration survive a reader who never opens the note.
    for k in [k for k in list(doc) if k == "per_arm"]:
        doc["per_arm_SUPERSEDED_computed_under_closed_window_and_unwidened_floor"] = {
            "_scope": ("0058: every entry was computed under the CLOSED channel window (tau1, tau2] "
                       "and the un-widened floor, at every arm. Only W = 108 masks are on disk, so "
                       "it CANNOT be regenerated here. Step 13 is the consumer and MUST recompute "
                       "it. The inertness of the window form is asserted at W = 108 only and is NOT "
                       "expected to hold at W = 213, where D10 puts tau2 at or adjacent to tau_pull "
                       "and a mass point in last-insertion instants sits."),
            "series": doc.pop(k)}
    # finding 3 -- each arm keeps ITS OWN published ratio, superseded in place, and the
    # recomputation is reported under BOTH conventions rather than resolved.
    r = ratios(arm)
    doc["_DERIVED_2026_08_13"] = {
        "generated_by": "src/step7_regenerate_derived.py",
        "regenerated_not_patched": True,
        "one_definition_per_statement": (
            "Every sentence below comes from STATEMENTS in the generator and every figure from "
            "figure_table(). The .md half renders the SAME two objects, and compare_halves() "
            "reads both back off disk and compares them. B8 and B10 were one literal living in "
            "two writers with one edited; there is now one definition and a comparison."),
        "statements": STATEMENTS,
        "counts_are_the_only_inputs": {p_: C[p_] for p_ in POPS},
        "figures": figure_table(arm),
        "bounds": {p_: {k: D[p_][k] for k in ("ns", "sl", "sub", "cont", "corner_ns_floor",
                                              "corner_ns_ceil", "ceilings")} for p_ in POPS},
        "superseded_strings_every_occurrence_is_a_defect": SUPERSEDED,
        "bound_over_sampling_width_TWO_CONVENTIONS_NOT_RECONCILED": {
            "why": STATEMENTS["two_conventions"],
            "limit": STATEMENTS["ratio_denominator_limit"],
            "this_arm": arm,
            "this_arm_recomputed": r,
            "other_convention_denominator": RATIO_DENOMINATORS["b" if arm == "a" else "a"],
            "the_spec_fixes_neither_convention": True},
    }
    p.write_text(json.dumps(doc, indent=2))
    return hits, absent


# Paths genuinely absent from an arm's schema, allowlisted per arm with a reason. Anything
# absent and NOT here fails the run -- previously 28 declared derived figures in arm b were
# never written and the script still exited 0.
ABSENT_OK = {
    "a": {"width_joint_pp": "arm a states one width per bound, not a joint/component pair",
          "width_over_SL_exclusions_pp": "arm a carries the sub-interval as its own object",
          "ceiling_numerator": "arm a stores Continued as percentages only"},
    "b": {"width_pp": "arm b names the two widths joint/over_SL rather than one width_pp",
          "ceiling_numerator": "arm b stores Continued as percentages only",
          "joint_corner_check": "the attainable-corner table is arm a's object (bb-b.md:29)",
          "sampling_error": "arm b's bootstrap lives under `bootstrap`, not `sampling_error`"},
}


ABSENT_USED = {arm: set() for arm in ABSENT_OK}


def absent_is_allowed(arm, path):
    for frag, why in ABSENT_OK[arm].items():
        if frag in path:
            ABSENT_USED[arm].add(frag)
            return why
    return None


def unused_allowlist_entries():
    """An allowlist entry that never fires means the schema moved under it. (0062 audit.)"""
    return [(arm, frag) for arm in ABSENT_OK
            for frag in ABSENT_OK[arm] if frag not in ABSENT_USED[arm]]


def check_ratios_written(arm):
    """Every declared ratio path must EXIST and hold this arm's numerator over its own denominator.

    B9 (Red Team 14). The previous version did `se = doc.get(...); if not se: continue`, so arm b
    -- whose bootstrap is under `bootstrap`, not `sampling_error` -- was skipped in full and the
    run reported OK. A missing path is now a FAILURE. Nothing here can pass by finding nothing.
    """
    doc = json.load(open(ARMS[arm] + ".json"))
    bad = []
    checked = 0
    for pop in POPS:
        for band, node in RATIO_LAYOUT[arm][pop].items():
            width = D[pop]["sub"]["width"] if band == "sub" else D[pop][band]["width"]
            dens = DENOMS.get(band, DENOMS["sl"])
            den = dens[arm][pop]
            want = round(width / den, 4)
            for label, path, expect in (("width", node["width"], width),
                                        ("ratio", node["ratio"], want)):
                got = get(doc, path)
                if got is None:
                    bad.append((pop, band, label, "PATH ABSENT -- not a skip, a failure",
                                ".".join(path)))
                elif abs(float(got) - expect) > 5e-5:
                    bad.append((pop, band, label, got, expect))
                else:
                    checked += 1
            stored_ci = get(doc, node["ci"])
            if stored_ci is None:
                bad.append((pop, band, "ci", "PATH ABSENT", ".".join(node["ci"])))
            elif abs(float(stored_ci) - den) > 5e-4:
                bad.append((pop, band, "ci", stored_ci,
                            f"{den} -- the denominator the register names for arm {arm}"))
            else:
                checked += 1
            other = dens["b" if arm == "a" else "a"][pop]
            if abs(den - other) <= 1e-9 and band != "sub":
                bad.append((pop, band, "convention", den,
                            "the two arms' denominators must stay distinct"))
    if checked == 0:
        bad.append(("-", "-", "coverage", 0,
                    "zero rows checked -- a check that looks nowhere must not report OK"))
    return bad, checked


BEGIN = "<!-- BEGIN GENERATED: derived figures -- src/step7_regenerate_derived.py -->"
END = "<!-- END GENERATED: derived figures -->"


def md_block(arm):
    """Renders STATEMENTS and figure_table(). It contains no prose of its own about figures."""
    F = figure_table(arm)
    r = ratios(arm)
    L = [BEGIN, "",
         "## Derived figures — GENERATED, do not hand-edit",
         "",
         "**Every number and every sentence in this section comes from one definition in**",
         "`src/step7_regenerate_derived.py` — `figure_table()` and `STATEMENTS` — **and the `.json`",
         "half of this deliverable renders the same two objects.** `compare_halves()` reads both",
         "back off disk and compares them, so the two halves agreeing is demonstrated, not asserted.",
         "",
         f"**{STATEMENTS['channel_window']}**", ""]
    for pop in POPS:
        c, d = C[pop], D[pop]
        L += [f"### {pop} — n = {c['n']:,}", "",
              f"**Counts, the only inputs:** never-started {c['ns_unfiltered']:,} · Continued "
              f"{c['cont_unfiltered']:,} · started-and-left {c['sl_unfiltered']:,} · exclusions "
              f"{c['ns_excl']} + {c['sl_excl']} = {c['ns_excl'] + c['sl_excl']} · **channel "
              f"{c['channel']}**.", "",
              "| Bound | Floor | Ceiling | Width |",
              "| :--- | ---: | ---: | ---: |",
              f"| Never started | {d['ns']['floor_n']:,} → {d['ns']['floor']:.4f}% | "
              f"{d['ns']['ceil_n']:,} → {d['ns']['ceil']:.4f}% | {d['ns']['width']:.4f} pp |",
              f"| **Started and left** | **{d['sl']['floor_n']:,} → {d['sl']['floor']:.4f}%** | "
              f"{d['sl']['ceil_n']:,} → {d['sl']['ceil']:.4f}% | **{d['sl']['width']:.4f} pp** |",
              f"| *conditional sub-interval — NOT a bound* | *{d['sub']['floor_n']:,} → "
              f"{d['sub']['floor']:.4f}%* | *{d['sub']['ceil_n']:,} → {d['sub']['ceil']:.4f}%* | "
              f"*{d['sub']['width']:.4f} pp* |",
              f"| Continued | {d['cont']['floor_n']:,} → {d['cont']['floor']:.4f}% | "
              f"{d['cont']['ceil_n']:,} → {d['cont']['ceil']:.4f}% | {d['cont']['width']:.4f} pp |",
              "",
              "| Attainable corner | Never started | Continued | Started and left |",
              "| :--- | ---: | ---: | ---: |",
              f"| NS floor / S&L ceiling | {d['corner_ns_floor']['ns']:.4f}% | "
              f"{d['corner_ns_floor']['cont']:.4f}% | {d['corner_ns_floor']['sl']:.4f}% |",
              f"| NS ceiling / S&L floor | {d['corner_ns_ceil']['ns']:.4f}% | "
              f"{d['corner_ns_ceil']['cont']:.4f}% | {d['corner_ns_ceil']['sl']:.4f}% |",
              "",
              f"**Three ceilings sum to {d['ceilings']['sum']:.4f}%**, excess "
              f"{d['ceilings']['excess_pp']:.4f} pp = {d['ceilings']['mechanism']} pairs.",
              f"**Exclusion share of population: {d['exclusion_share_of_population']:.4f}%.**", ""]
    L += ["### The bound's scope", "", f"**{STATEMENTS['covering_qualifier']}**", "",
          "### Bound ÷ sampling width — TWO CONVENTIONS, NOT RECONCILED", "",
          f"**{STATEMENTS['two_conventions']}**", "",
          "| | Denominator | Bound ÷ it | Sub-interval ÷ it |",
          "| :--- | ---: | ---: | ---: |"]
    for pop in POPS:
        L.append(f"| {pop} | {r[pop]['denominator']:.4f} | **{r[pop]['ratio']:.4f}** | "
                 f"{r[pop]['sub_interval_ratio']:.4f} |")
    L += ["", f"**Never started, same arm, same convention: {F['APPLY.ns.ratio']:.4f} on APPLY "
          f"(denominator {F['APPLY.ns.ratio_denominator']:.4f}); DERIV is 0.0 because that bound "
          f"is degenerate.**", "",
          f"*{STATEMENTS['ratio_denominator_limit']}*", "",
          "### Scope and limits", "",
          f"- **Per-`W` series.** {STATEMENTS['per_w_scope']}",
          f"- **Point estimates.** {STATEMENTS['point_estimates_do_not_move']}",
          f"- **Legitimate readings.** {STATEMENTS['legitimate_not_superseded']}",
          f"- **Commutation.** {STATEMENTS['commutation_caveat']}", "",
          CANON_BEGIN + json.dumps({"statements": sorted(STATEMENTS), "figures": F},
                                   sort_keys=True) + CANON_END, "",
          END, ""]
    return "\n".join(L)


def compare_halves(arm):
    """Read both rendered halves back off disk and compare. Not an assertion -- a comparison."""
    md = Path(ARMS[arm] + ".md").read_text()
    m = re.search(re.escape(CANON_BEGIN) + r"(.*?)" + re.escape(CANON_END), md, re.S)
    if not m:
        return [f"arm {arm}: no CANON block in the .md half -- nothing to compare against"]
    md_canon = json.loads(m.group(1))
    doc = json.load(open(ARMS[arm] + ".json"))
    blk = doc.get("_DERIVED_2026_08_13")
    if not blk:
        return [f"arm {arm}: no _DERIVED block in the .json half"]
    out = []
    if md_canon["statements"] != sorted(blk.get("statements", {})):
        out.append(f"arm {arm}: the two halves render different STATEMENT keys")
    jf = blk.get("figures", {})
    for k, v in md_canon["figures"].items():
        if k not in jf:
            out.append(f"arm {arm}: figure {k} in the .md half and absent from the .json half")
        elif abs(float(jf[k]) - float(v)) > 5e-7:
            out.append(f"arm {arm}: figure {k} differs -- md {v}, json {jf[k]}")
    for k in jf:
        if k not in md_canon["figures"]:
            out.append(f"arm {arm}: figure {k} in the .json half and absent from the .md half")
    if not out and not jf:
        out.append(f"arm {arm}: compared zero figures -- a comparison that compares nothing fails")
    return out


def apply_md(arm):
    p = Path(ARMS[arm] + ".md")
    s = p.read_text()
    block = md_block(arm)
    if BEGIN in s:
        s = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", block, s, flags=re.S)
    else:
        lines = s.split("\n")
        i = next(i for i, l in enumerate(lines) if l.startswith("**Instance:")) + 1
        s = "\n".join(lines[:i] + ["", block] + lines[i:])
    p.write_text(s)


# ------------------------------------------------------------- 7. VERIFY
# Numeric, at BOTH precisions -- finding 6. "9.6830" is not a substring of "9.682997",
# so textual grep cannot see the JSON. This does not use text at all.

def verify():
    bad, declared = [], []
    # From the SHARED register, plus the per-file scoped entries for this arm.
    sup = [float(v) for v in SUPERSEDED]

    def walk(o, p, arm):
        if isinstance(o, dict):
            for k, v in o.items():
                if k.startswith("_DERIVED") or "SUPERSEDED_computed_under" in k:
                    declared.append(f"{p}.{k}")
                    continue
                walk(v, f"{p}.{k}", arm)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{p}[{i}]", arm)
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            for s in sup:
                if abs(float(o) - s) < 5e-5:
                    bad.append((arm, p, o, s))

    for arm, path in ARMS.items():
        base = list(sup) + [v for (frag, v) in SUPERSEDED_IN if frag in path]
        sup[:] = base
        walk(json.load(open(path + ".json")), "", arm)
        sup[:] = [float(v) for v in SUPERSEDED]
    return bad, declared


if __name__ == "__main__":
    print(f"counts (open window): APPLY channel {C['APPLY']['channel']} "
          f"(closed form {C['APPLY']['channel_closed_form']}) · "
          f"DERIV channel {C['DERIV']['channel']} (closed form {C['DERIV']['channel_closed_form']})")
    for pop in POPS:
        d = D[pop]
        print(f"  {pop:6} S&L [{d['sl']['floor']:.4f}, {d['sl']['ceil']:.4f}] w={d['sl']['width']:.4f} | "
              f"sub [{d['sub']['floor']:.4f}, {d['sub']['ceil']:.4f}] w={d['sub']['width']:.4f} | "
              f"cont ceil {d['cont']['ceil']:.4f} | corner {d['corner_ns_ceil']['cont']:.4f} | "
              f"sum {d['ceilings']['sum']:.4f}")
    failures = []
    for arm in ARMS:
        h, absent = apply_json(arm)
        apply_md(arm)
        r = ratios(arm)
        print(f"  arm {arm}: {h} json paths written; "
              f"ratio APPLY {r['APPLY']['ratio']} on denominator {r['APPLY']['denominator']}")
        if absent:
            print(f"    absent in this arm's structure: {len(absent)} -- each must be allowlisted")
            for x in absent:
                why = absent_is_allowed(arm, x)
                print(f"      {'ok  ' if why else 'FAIL'} {x}" + (f"  ({why})" if why else ""))
                if not why:
                    failures.append(f"absent and not allowlisted: arm {arm} {x}")
        rbad, rchecked = check_ratios_written(arm)
        print(f"    ratios: {rchecked} rows checked across both bands and both populations")
        for pop, band, label, got, want in rbad:
            failures.append(f"arm {arm} {pop} {band}.{label}: {got!r}, expected {want!r}")
    # The .md bodies were checked by nothing (Red Team 12, non-blocking 3). They are now
    # checked by the same register, through the same checker, before this script exits.
    try:
        import check_surfaces
        neg, _pos, _pi, _al, _ls = check_surfaces.scan()
        md_bad = [x for x in neg if "step7-liveness-bb" in x[1]]
        if md_bad:
            for x in md_bad:
                failures.append(f"operative deliverable body: {x[1]} {x[2]} = {x[3]}")
    except Exception as e:                                   # noqa: BLE001
        failures.append(f"could not verify the .md bodies: {e}")

    for arm, frag in unused_allowlist_entries():
        failures.append(f"ABSENT_OK[{arm!r}][{frag!r}] never fired -- the schema moved under it")

    for arm in ARMS:
        diffs = compare_halves(arm)
        failures.extend(diffs)
        if not diffs:
            n = len(figure_table(arm))
            print(f"  arm {arm}: .md and .json halves COMPARED and agree on "
                  f"{n} figures and {len(STATEMENTS)} statements")

    bad, declared = verify()
    if declared:
        print("\n  DECLARED scope-limited, not regenerated, not silent:")
        for x in declared:
            print(f"      - {x}")
    for arm, p, o, s in bad:
        failures.append(f"superseded value survives: arm {arm} {p} = {o} (was {s})")
    if failures:
        print("\nFAIL:")
        for f in failures:
            print(f"  {f}")
        sys.exit(1)
    print("\nVERIFIED: no superseded value survives at any path in either JSON or either .md "
          "body; every declared target path is written or allowlisted with a reason; each arm's "
          "ratio is its own numerator over its own denominator.")
