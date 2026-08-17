"""Step 8 (instance b) -- stage 4: render the two artifacts and their JSON halves.

GATE. NOTHING IS ADOPTED HERE. This instance produces its deliverables and stops.

Counts and aggregates ONLY. No username, user id or individual watch history
reaches artifacts/. The analysis table itself stays in processed/.

Both halves of each deliverable are rendered from ONE object each, so agreement
between the .md and the .json is a property of the generator rather than a claim
(CLAUDE.md, "One definition per statement and per figure").

decisions/0079 Sec 2: EVERY count, EVERY invariant result and EVERY waterfall
figure carries the BUILD it was measured on -- not two of them. Partial
application is worse than none, because two labelled figures imply the rest did
not need it. The label is emitted from step8_b_build_id.BUILD rather than typed.

Out: artifacts/step8-waterfall-b.{md,json}, artifacts/step8-invariants-b.{md,json}
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from step8_b_build_id import BUILD, BUILD_SHORT, RULED_BUILD, provenance_block

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step8" / "b"
ART = ROOT / "artifacts"

W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]

# =====================================================================
# PROPAGATION SURFACE 6 -- artifacts/ -- IS OPENED BY THIS ARM'S OWN RUN.
#
# Red Team seventh pass, finding 1, against this arm: the -r4 invariant report
# carried "a report where six of EIGHT cannot fail on data" IN ITS OWN BODY,
# 800 lines below a head that states the set is NINE, and 200 lines below a
# surface check CONCLUDING that no surface still states the old count. That
# check opened task-sheet.md, this arm's definition file and specs/step8-
# readback.md. IT DID NOT OPEN artifacts/. CLAUDE.md numbers artifacts/ as
# propagation surface 6 and says all eight are checked on every edit.
#
# The same finding names a second instance of the same class in the same run:
# "Why the loose count publishes even though STRICT IS RULED" -- 0074 ruling 5's
# framing, which 0090 supersedes -- sitting 85 lines BELOW the line that strikes
# exactly that framing.
#
# So the run now greps its OWN deliverables. Two rules from CLAUDE.md govern it:
#   * "A grep hit is not a defect until you read the line." A string named as
#     superseded AT THE POINT OF USE is legitimate; an unqualified one is not.
#     So every hit is classified by whether its line carries a supersession
#     marker, and only UNMARKED hits fail.
#   * "And grep the corrected string too, requiring non-zero" -- a figure that
#     was never written returns zero hits on every superseded form of itself.
#
# COVERAGE IS PRINTED. An empty result and a clean result are the same value.
#
# ================== TWO CORRECTIONS THIS RUN, Red Team eighth pass, F2 =======
#
# (1) THE REGISTER MOVED TO src/step7_register.py, WHICH IS THE ONLY REGISTER.
#     CLAUDE.md: "One register, in src/step7_register.py, imported by every
#     script that checks. Two hand-maintained copies diverged by an entry after
#     a single use, and neither held the values that were wrong." The -r6 build
#     kept a SECOND hand-maintained register here, which is the arrangement that
#     rule exists against. Nothing is defined locally now; it is imported.
#
# (2) MATCHING IS CASE-INSENSITIVE. This is the defect, and it is exact: the
#     -r6 needle was the lower-case `six of eight`, while the string actually
#     present in this arm's deliverables -- THREE TIMES -- is `six of EIGHT`.
#     `str.count` is case-sensitive, so the ONE NEEDLE WRITTEN AGAINST THE VERY
#     DEFECT THAT MOTIVATED THIS CONTROL could not see it, and its hits table
#     carried no row for that needle. A control that cannot see its own founding
#     defect is indistinguishable from a clean pass, which is precisely
#     CLAUDE.md's "an empty result and a clean result are the same value".
from step7_register import (  # noqa: E402  -- the ONE register
    SUPERSEDED_STRINGS,
    NEEDLES_WITHDRAWN,
    SURFACE6_MARKERS,
    SURFACE6_LINE_LOCAL_CONTROLS,
    surface6_needle_count,
    surface6_line_is_marked,
)

REGISTER_SOURCE = "src/step7_register.py"
REGISTER_IS_SINGLE = ("CLAUDE.md -- one register, imported by every script that checks. This "
                      "module defines no needles of its own; it imports them, so a second "
                      "hand-maintained copy cannot drift from the first")

# THE SCANNER'S OWN OUTPUT CONTAINS EVERY NEEDLE IT SEARCHES FOR. That is
# unavoidable -- a register of superseded strings is a list of superseded
# strings. It is handled by making the register's own lines SELF-MARKING rather
# than by exempting a block: CLAUDE.md is explicit that "a file-level stamp
# declares a file's STATUS, never its individual values", and exempting a region
# by line range is the same move one level down. Every line the register emits
# carries the word SUPERSEDED, so it is classified by the same rule as every
# other line and no range is skipped.
REGISTER_MARK = "SUPERSEDED_STRING_REGISTER"


# The matcher and the marker test both live in the ONE register and are
# imported above. `_count_bounded` is retained as a thin alias so the call sites
# read the same, but it now resolves to the case-insensitive implementation.
_count_bounded = surface6_needle_count


def surface6_scan(files: dict) -> dict:
    """Grep this arm's OWN artifacts -- propagation surface 6 -- both halves.

    `files` maps a published path to its full text. Returns per-file hit counts
    split into MARKED (named as superseded at the point of use, which CLAUDE.md
    permits) and UNMARKED (a live occurrence, which is the defect).
    """
    sentinel = _sentinel_test()
    lloc = _line_local_controls(files)
    per_file = {}
    unmarked_total = 0
    for path, txt in files.items():
        lines = txt.split("\n")
        hits = []
        for needle, what, replacement in SUPERSEDED_STRINGS:
            marked = unmarked = 0
            unmarked_lines = []
            for i, ln in enumerate(lines):
                n = _count_bounded(ln, needle)
                if not n:
                    continue
                if surface6_line_is_marked(ln):
                    marked += n
                else:
                    unmarked += n
                    unmarked_lines.append(i + 1)
            # EVERY needle gets a row, INCLUDING a zero one. Red Team's eighth
            # pass, F2: `six of EIGHT` is present three times and the hits table
            # showed NO ROW for that needle -- because a needle with no matches
            # was simply omitted, so "the needle found nothing" and "the needle
            # is not in the table" looked identical, which is CLAUDE.md's empty-
            # against-clean rule at the row level.
            hits.append({REGISTER_MARK + "__string": needle,
                         "what_it_is": what, "replaced_by": replacement,
                         "marked_as_superseded_at_the_point_of_use": marked,
                         "UNMARKED_LIVE_OCCURRENCES": unmarked,
                         "total_occurrences": marked + unmarked,
                         "unmarked_line_numbers": unmarked_lines})
            unmarked_total += unmarked
        per_file[path] = {
            "bytes_read": len(txt),
            "lines_read": len(lines),
            "strings_searched": len(SUPERSEDED_STRINGS),
            "rows_emitted": len(hits),
            "strings_with_any_occurrence": sum(1 for h in hits if h["total_occurrences"]),
            "strings_with_ZERO_occurrences": sum(1 for h in hits
                                                 if not h["total_occurrences"]),
            "hits": hits,
            "unmarked_live_occurrences": sum(
                h["UNMARKED_LIVE_OCCURRENCES"] for h in hits),
        }
    return {
        "rule": ("CLAUDE.md -- there are EIGHT propagation surfaces and all eight are checked "
                 "on every edit. artifacts/ is SURFACE 6: 'deliverables carrying superseded "
                 "figures are stamped, not left to be read as current'"),
        "why_this_exists": (
            "Red Team seventh pass, finding 1, against THIS ARM: the -r5 invariant report "
            "published a superseded assertion-set count IN ITS OWN BODY, inside a document "
            "whose head states the correct count and whose surface check concludes that no "
            "surface still states the old one. That check opened task-sheet.md, this arm's "
            "definition file and specs/step8-readback.md -- IT NEVER OPENED artifacts/. The "
            "same run carried a second instance of the same class: 0090's superseded framing "
            "sitting below the line that strikes it. A surface check that does not open the "
            "surface the defect is on is a check that looked nowhere"),
        "a_hit_is_not_a_defect_until_the_line_is_read": (
            "CLAUDE.md. A string named as SUPERSEDED at the point of use is legitimate and is "
            "counted separately; an unqualified occurrence is a live defect. Only UNMARKED "
            "occurrences fail this run"),
        "coverage": {p: {"bytes_read": v["bytes_read"], "lines_read": v["lines_read"]}
                     for p, v in per_file.items()},
        # ONE LINE, so the register classifies itself under the same rule as
        # every other line rather than being exempted by range.
        REGISTER_MARK + "__strings_searched":
            " | ".join(s[0] for s in SUPERSEDED_STRINGS),
        "strings_searched_count": len(SUPERSEDED_STRINGS),
        "NEEDLES_TRIED_AND_WITHDRAWN_each_naming_the_stronger_control": NEEDLES_WITHDRAWN,
        "withdrawing_a_needle_disarms_the_control_against_it": (
            "CLAUDE.md, exactly. It is done here for two strings and only because the legitimate "
            "reading is verified LIVE on this build under the adopted rule, and because each is "
            "covered by a SET assertion or a structural assertion that a substring test cannot "
            "express. Both replacements are asserted in this run and fail it if they break"),
        "the_numeric_boundary_rule": (
            "a needle beginning with a digit is not counted when it sits inside a longer number. "
            "This control caught itself on its first run: the SUPERSEDED needle `793` matched "
            "inside `\"retained_pct\": 95.867931...`. It NARROWS THE MATCH RULE and disarms no "
            "string"),
        "how_the_register_avoids_failing_its_own_check": (
            "a register of superseded strings necessarily contains every superseded string. It "
            "is NOT exempted by line range -- CLAUDE.md forbids a file-level or block-level "
            "exemption, because 'a file-level stamp declares a file's STATUS, never its "
            "individual values'. Instead every line this register emits carries the token "
            "SUPERSEDED, so it is classified by exactly the same rule as every other line. The "
            "cost is stated: any line containing a marker word passes, so the control is a "
            "marker-word control and not a semantic one"),
        "THE_REGISTER_IS_THE_ONE_REGISTER": {
            "source": REGISTER_SOURCE,
            "rule": REGISTER_IS_SINGLE,
            "CORRECTED_THIS_RUN": ("the -r6 build kept a SECOND hand-maintained register inside "
                                   "this module. CLAUDE.md requires ONE, in src/step7_register.py, "
                                   "imported by every script that checks -- the rule exists "
                                   "because two copies diverged by an entry after a single use "
                                   "and neither held the values that were wrong. Red Team eighth "
                                   "pass, F2"),
            "needles_now_defined_in_this_module": 0,
        },
        "MATCHING_IS_CASE_INSENSITIVE": {
            "CORRECTED_THIS_RUN": (
                "the -r6 matcher was `str.count`, which is CASE-SENSITIVE, against the "
                "lower-case needle `six of eight`. The string actually present in this arm's "
                "deliverables is `six of EIGHT`, three times. THE ONE NEEDLE WRITTEN AGAINST THE "
                "DEFECT THAT MOTIVATED THIS CONTROL COULD NOT SEE IT, and its hits table carried "
                "no row for it. Red Team eighth pass, F2"),
            "markers_are_compared_case_insensitively_too": True,
            "marker_count": len(SURFACE6_MARKERS),
        },
        "SENTINEL_TEST_the_matcher_can_see_its_own_needles": sentinel,
        "NEGATIVE_CONTROL_the_gate_is_EXECUTED_not_asserted": _negative_control(),
        "LINE_LOCAL_CONTROLS_where_a_substring_needle_cannot_express_the_defect": lloc,
        "per_file": per_file,
        "UNMARKED_LIVE_OCCURRENCES_TOTAL": unmarked_total,
        "passes": (unmarked_total == 0 and sentinel["all_needles_findable"]
                   and all(v["passes"] for v in lloc.values())
                   and _negative_control()["all_behave_as_required"]),
        "empty_vs_clean": (
            "this result is CLEAN, not EMPTY, and the evidence is the SENTINEL TEST rather than "
            "an incidental non-zero count: every needle is run against a synthetic line "
            "containing it in an inverted case and must be found. The -r6 build claimed "
            "'the marked-occurrence counts are non-zero, which proves the needles are findable' "
            "-- that is a claim about SOME needles and it was FALSE OF THE ONE THAT MATTERED. "
            "Bytes and lines actually read are stated per file, and every needle carries a row "
            "even when its count is zero"),
    }


def _negative_control() -> dict:
    """Inject each defect this control exists to catch and require that it FAILS.

    `CLAUDE.md`: "A control asserted to exist is not a control." The `-r6`
    build's surface check reported clean on a file set containing the string it
    was built for, and nothing in the deliverable distinguished that from a real
    pass. So each case below is a synthetic file the scanner is actually run
    over, and the recorded result is whether the scanner CAUGHT it.

    Case 3 is the one that matters: the SAME text with an unmarked superseded
    string is caught here and was NOT caught by the case-sensitive matcher.
    """
    def run(text):
        r = _one_file_scan(text)
        return r
    cases = {
        "A_unmarked_superseded_string_lower_case": {
            "planted": "the set has six of eight members that cannot fail",
            "must_be": "CAUGHT",
        },
        "B_unmarked_superseded_string_MIXED_case_the_r6_blind_spot": {
            "planted": "a report where six of EIGHT cannot fail on data",
            "must_be": "CAUGHT",
        },
        "C_the_SAME_string_named_as_superseded_at_the_point_of_use": {
            "planted": "~~six of EIGHT cannot fail~~ SUPERSEDED by NINE",
            "must_be": "NOT_CAUGHT -- legitimate under CLAUDE.md",
        },
        "D_a_clean_line": {
            "planted": "the assertion set has NINE members",
            "must_be": "NOT_CAUGHT",
        },
    }
    out = {}
    for name, c in cases.items():
        unmarked = run(c["planted"])
        caught = unmarked > 0
        expected = c["must_be"].startswith("CAUGHT")
        out[name] = {"expected": c["must_be"], "unmarked_hits": unmarked,
                     "caught": caught, "behaves_as_required": caught == expected,
                     "case_sensitive_r6_matcher_would_have_caught":
                         sum(c["planted"].count(n) for n, _w, _r in SUPERSEDED_STRINGS) > 0
                         and not surface6_line_is_marked(c["planted"])}
    return {
        "why": ("CLAUDE.md -- a control asserted to exist is not a control, and an empty result "
                "and a clean result are the same value. The gate is run over synthetic text "
                "carrying each defect and each legitimate form, and the result recorded is what "
                "it DID, not what it is claimed to do"),
        "cases_run": len(out),
        "cases_behaving_as_required": sum(1 for v in out.values() if v["behaves_as_required"]),
        "all_behave_as_required": all(v["behaves_as_required"] for v in out.values()),
        "THE_R6_BLIND_SPOT_case_B": (
            "case B is the exact string Red Team reports three times in this arm's -r6 "
            "deliverables. This matcher catches it; the -r6 matcher's own column in this table "
            "records whether it would have"),
        "cases": out,
    }


def _one_file_scan(text: str) -> int:
    """Unmarked live occurrences in one piece of text. Shared by the scanner and
    the negative control, so the control tests the code the gate runs."""
    total = 0
    for ln in text.split("\n"):
        if surface6_line_is_marked(ln):
            continue
        for needle, _w, _r in SUPERSEDED_STRINGS:
            total += surface6_needle_count(ln, needle)
    return total


def _line_local_controls(files: dict) -> dict:
    """Controls a substring needle cannot express, from the ONE register.

    The 747,478 defect is an ATTRIBUTION -- "it is a season-coverage ROW count"
    -- and it survives rewording, markdown emphasis inside the sentence, and
    reordering. A needle for one phrasing sits at zero forever while the claim
    returns in another. So: every line mentioning the figure must be MARKED as
    superseded, or must characterise it as PAIRS.

    COVERAGE IS PRINTED, and a control that examined no lines FAILS: if the
    figure appears nowhere the control states that it looked at zero lines
    rather than reporting a pass.
    """
    out = {}
    for name, spec in SURFACE6_LINE_LOCAL_CONTROLS.items():
        examined, ok, bad = 0, 0, []
        for path, txt in files.items():
            for i, ln in enumerate(txt.split("\n")):
                if spec["needle"] not in ln:
                    continue
                examined += 1
                low = ln.lower()
                if surface6_line_is_marked(ln):
                    ok += 1
                elif (any(w in low for w in spec["must_contain_one_of"])
                      and not any(w in low for w in spec["must_not_contain"])):
                    ok += 1
                else:
                    bad.append({"file": path, "line": i + 1, "text": ln[:220]})
        out[name] = {
            "rule": spec["rule"], "ruling": spec["ruling"],
            "why_not_a_needle": spec["why_not_a_needle"],
            "lines_examined": examined, "lines_conforming": ok,
            "LINES_FAILING": bad,
            "coverage_is_printed": (
                f"{examined} lines mention the {spec['needle']} distinct-pairs figure across "
                "the four artifacts, and each was read. A control that examined none of them "
                "reports zero coverage and FAILS rather than passing (CLAUDE.md)"),
            "examined_nothing": examined == 0,
            "passes": examined > 0 and not bad,
        }
    return out


def _sentinel_test() -> dict:
    """Prove the matcher can find each needle -- in a case it does not appear in.

    CLAUDE.md: "An empty result and a clean result are the same value, and only
    the control knows which it produced. A check that finds nothing because it
    looked nowhere must FAIL, not pass."

    The -r6 control had no such test. Its needle `six of eight` returned 0 on a
    file containing `six of EIGHT` three times, and 0 was reported as clean. A
    control asserted to work is not a control that works, so this executes the
    failure rather than describing it: each needle is planted in a line whose
    case is inverted from the register's, and must still be found.
    """
    # EVERY LINE THIS TEST EMITS IS SELF-MARKING. A sentinel test for a register
    # of superseded strings necessarily contains every superseded string, and
    # CLAUDE.md forbids exempting it by block or by line range: "a file-level
    # stamp declares a file's STATUS, never its individual values". So each key
    # and each value carrying a needle is prefixed with the register token and
    # is classified by exactly the same rule as every other line. This module's
    # register already worked that way; the sentinel test is new and had to be
    # brought under it -- caught by the gate on its first run, before any write.
    rows = {}
    for needle, _what, _repl in SUPERSEDED_STRINGS:
        planted = "prefix " + needle.upper() + " suffix"
        rows[REGISTER_MARK + "__" + needle] = {
            "planted_line_case": "UPPER",
            "found": surface6_needle_count(planted, needle),
            "case_sensitive_str_count_would_find": planted.count(needle),
        }
    # The founding case, executed rather than asserted.
    demo_line = "a report where six of EIGHT cannot fail on data"
    return {
        "why": ("a control that cannot see its own founding defect is indistinguishable from a "
                "clean pass. Executed, not described"),
        "every_line_below_is_SELF_MARKING": (
            "a sentinel test for a register of superseded strings contains every superseded "
            "string. It is not exempted by block or by line range -- CLAUDE.md forbids that -- "
            "so each key and each needle-bearing value carries the register token and is "
            "classified by the same rule as every other line"),
        "needles_tested": len(rows),
        "all_needles_findable": all(v["found"] > 0 for v in rows.values()),
        "needles_a_CASE_SENSITIVE_matcher_would_MISS_on_this_test": [
            k for k, v in rows.items() if v["case_sensitive_str_count_would_find"] == 0],
        "THE_FOUNDING_CASE": {
            REGISTER_MARK + "__line": demo_line,
            REGISTER_MARK + "__needle": "six of eight",
            "case_insensitive_matcher_finds": surface6_needle_count(demo_line, "six of eight"),
            "the_r6_case_sensitive_matcher_found": demo_line.count("six of eight"),
            "reading": ("the -r6 control returned 0 on this line and published that 0 as a "
                        "clean result. This is the exact string Red Team reports three times "
                        "in this arm's deliverables with no row in its hits table"),
        },
        "rows": rows,
    }


def surface6_positive(files: dict, required: list) -> dict:
    """The POSITIVE half. CLAUDE.md, added by this agent's own predecessor run:
    "a figure that was never written returns zero hits on every superseded form
    of itself", so the negative grep passes clean on a file that never said the
    right thing either. Every corrected string must be PRESENT."""
    out = {}
    for needle, why in required:
        n = sum(txt.count(needle) for txt in files.values())
        out[needle] = {"occurrences_across_the_emitted_artifacts": n,
                       "required": "non-zero", "why": why, "present": n > 0}
    return {
        "rule": ("CLAUDE.md -- 'And grep the corrected string too, requiring non-zero.' The "
                 "negative half sees only one of a defect's two shapes: the wrong figure "
                 "PRESENT. It is blind to the right figure MISSING"),
        "matching_is_CASE_SENSITIVE_here_and_that_is_deliberate": (
            "the negative half is case-INsensitive because a superseded string in an unexpected "
            "case must still be caught; this half is case-SENSITIVE because a corrected string "
            "written in an unexpected case FAILS the run loudly rather than passing silently. "
            "The two halves fail in opposite directions and each is set to fail safe"),
        "checks": out,
        "all_present": all(v["present"] for v in out.values()),
    }
GATE = ("**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. "
        "This instance does not adopt its own proposal, does not begin Step 8b or Step 9, "
        "and records no approval — that is the Human Lead's alone. Zero API calls; every "
        "figure is computed from data already on disk.")
def rerun_note(R: dict, D9: dict, I: dict) -> str:
    """The lead paragraph, with its claims READ FROM THE MEASURED OBJECTS.

    The previous build typed this paragraph, and it then asserted a boundary
    verdict ("not vacuous — the tau1 boundary is occupied") that was computed on
    the wrong interval, and a spec vintage that has since moved. A summary that
    is typed is a second definition of every figure in it.
    """
    fn = R["B3_the_two_unasserted_mandates"]["a_boundary_window"][
        "THE_FOUR_NUMBERS_THAT_SETTLE_B3"]
    vs = R["B3_the_two_unasserted_mandates"]["a_boundary_window"]["by_population"][
        "APPLY_position5"]["VERDICT_STATE"]
    pf = D9["PUBLICATION_FORM_decisions_0090"]["bounds"]
    ng = I["invariant_coverage_rule"]["AUDIT_can_each_identity_actually_fail"][
        "THE_FAILURE_IS_EXECUTED_NOT_DESCRIBED"]
    wf = {w["position"]: w for w in R["waterfall_APPLY"]}
    t168 = R["required_counts"]["D2_negative_lag"]["THE_168_MEASURED_ON_EVERY_POPULATION"][
        "by_population"]
    lb = I["counts"]
    return (
        "**This is a RERUN ordered by the Human Lead**, on `task-sheet.md` Step 8 as it now "
        "stands — the spec as amended through **`decisions/0093`** and Red Team's **EIGHTH** "
        "pass. **It is a rerun, not an amendment: everything below is rebuilt from the stored "
        "data by the same pipeline that writes the table, and no previous output was patched** "
        "(`0092` — a deliverable is corrected by rerunning the arm that produced it). "
        "**`0093` IS WHY THIS RUN EXISTS AND THIS ARM IS WHAT OCCASIONED IT:** *a ruling "
        "recorded in `decisions/` and propagated to the spec is NOT closed; it is closed when "
        "the ARTIFACTS carry it* — and the arms only rewrite their deliverables **on a run**, so "
        "`0089` §2(b) sat recorded, propagated and passing every control for two entries while "
        "**this arm's deliverables went on publishing the text it corrected.** "
        "**Red Team's eighth pass found NO ARITHMETIC DEFECT in this arm. All three of its "
        "findings are in machinery this arm emitted, and all three are corrected here.** "
        "**(1) F1 — THE `747,478` CHARACTERISATION** (§10z). `-r6` republished `0088` §2(b)'s "
        "axis — *747,478 as undeduplicated season-coverage **rows*** — **which `0089` §2(b) had "
        "corrected two entries earlier to distinct `(user, show)` **pairs***, and **this arm's "
        "own table six lines below contradicted it**, giving "
        f"**{D9['COVERAGE_QUANTITIES_EACH_NAMED']['undeduplicated_user_show_SEASON_COVERAGE_ROWS']['value']:,}** "
        "for that label. Corrected at the point of use, with `0093` §3(c)'s relation stated: "
        "**747,478 distinct pairs less the 21,376 S3-only is 726,102 against this arm's "
        f"{D9['candidate_user_show_pairs_examined']:,}** — the one-pair divergence both arms "
        "already report. **Reported, not reconciled.** "
        "**(2) F2 — THE SURFACE-6 CONTROL COULD NOT SEE THE STRING CLASS IT WAS BUILT FOR** "
        "(§16). Its matching was **case-sensitive** and its needle was the lower-case "
        "`six of eight`, while the string present in this arm's deliverables — **three times** — "
        "is `six of EIGHT`. **The one needle written against the very defect that motivated the "
        "control returned zero, and zero was published as clean.** Three repairs: matching is "
        "**case-insensitive**, and the claim is now **executed** by a sentinel test rather than "
        "asserted; the needles moved into **`src/step7_register.py`, the ONE register**, which "
        "`CLAUDE.md` requires and which `-r6` duplicated in a second hand-maintained copy; and "
        "**the gate now runs on the final bytes BEFORE the write** — `-r6` wrote all four "
        "artifacts to propagation surface 6 and asserted afterwards, so the check could report "
        "a live superseded string but not prevent it reaching the surface. "
        "**(3) F3 — THE PER-SITE D11 `examined` COLUMN HELD TWO QUANTITIES** (§14a(b)): "
        "post-exclusion at `A`, `A_H` and the eight `action_count_*` sites, pre-exclusion at the "
        "liveness and D9 sites. **The vacuity test keyed on it**, so a site whose entire input "
        "was post-cutoff would have reported `examined = 0` and been labelled **VACUOUS** — "
        "*\"this site examined 0 records\"* — **having examined and excluded everything.** Every "
        "row now carries **input universe before D11** and **counted after D11**, each in the "
        "site's own unit, and vacuity keys on the input universe. "
        "**Carried from `-r6`, re-executed not restated:** `0090`'s D9 **bound** — "
        f"complementary pairs `{pf['complementary_signature_pairs']['BOUND']}`, half (a) "
        f"`{pf['half_a_APPLY_position5']['BOUND']}`, half (b) "
        f"`{pf['half_b_present_in_the_position3_drop_set']['BOUND']}`, **neither endpoint the "
        "point estimate**; and B3(a)'s reversed verdict on the separating interval "
        f"`[τ, τ + 24h)` — **`{vs}`**, "
        f"**{fn['APPLY_position5_both_bounds_relaxed']} APPLY rows** and "
        f"**{fn['DERIV_position5_both_bounds_relaxed']} DERIV rows** change outcome state under "
        "the forbidden `date(watched_at) <= T1` form (`τ1` alone "
        f"{fn['APPLY_position5_tau1_relaxed']} / {fn['DERIV_position5_tau1_relaxed']}, `τ2` "
        f"alone {fn['APPLY_position5_tau2_relaxed']} / {fn['DERIV_position5_tau2_relaxed']}); "
        f"and the executed negative control — **{ng['cases_run']} injected defects, "
        f"{ng['cases_caught']} of {ng['cases_whose_control_is_checkable']} checkable cases "
        "caught, asserted, with the one that passes by design named.** "
        "**No population moves, no waterfall line moves and no published figure moves.** Line 1 "
        f"is **{wf[1]['retained_pairs']:,}**, APPLY is **{wf[5]['retained_pairs']:,}**, DERIV is "
        "**147,370**, position 6 removes **703** and **99**, and the column set is **89**. "
        f"**The `both bind` split, measured on every population as `0092` §3 requires:** "
        f"{t168['line1_220107']} on line 1, {t168['APPLY_position5_196654']} on APPLY position 5 "
        f"— invariant across the APPLY chain — and {t168['DERIV_position5_147370']} on DERIV. "
        f"**The assertion set: {lb['cannot_fail_on_any_data']} of {lb['assertions_total']} "
        f"cannot fail on any data, {lb['can_fail_on_data_as_specified']} can as specified**, "
        "every count derived from the `label` field rather than typed. "
        "**This overwrites the previous `-b` deliverables, which is the only way `0093` closes.**")
PROV = (f"**Provenance — `{BUILD}`.** Every count, every waterfall figure and every invariant "
        "result below was measured on that build (`0078`, `0079` §2). Where a figure is quoted "
        f"from a ruling, the ruling's own build is named instead: `{RULED_BUILD}`. "
        "**A count without its provenance can be correct when written and wrong when read.**")
MEAS = f"*Measured on: {BUILD_SHORT}.*"


def cap1(s: str) -> str:
    """Upper-case the first character only. `str.capitalize()` lower-cases the
    rest, which turns S2 into s2 and D11 into d11 inside quoted text."""
    return s[:1].upper() + s[1:]


def main() -> None:
    R = json.loads((OUT / "results.json").read_text())
    I = json.loads((OUT / "invariants.json").read_text())
    D9 = json.loads((OUT / "d9.json").read_text())
    S1 = json.loads((OUT / "stage1.json").read_text())
    q = R["required_counts"]
    ex = R["emitted_beyond_the_required_list"]
    rec = I["population_reconciliation_703_and_99"]

    # the per-show drop count, as a DISTRIBUTION -- the required count belongs in
    # artifacts/, and 1,138 identical rows would be noise rather than a count.
    import csv
    hist: dict[str, int] = {}
    with open(OUT / "drop_counts_per_show.csv") as fh:
        for row in csv.DictReader(fh):
            hist[row["dropped_records"]] = hist.get(row["dropped_records"], 0) + 1
    q["drop_counts"]["per_show_distribution_records_dropped_to_shows"] = \
        {k: v for k, v in sorted(hist.items(), key=lambda kv: int(kv[0]))}
    q["drop_counts"]["shows_examined"] = sum(hist.values())

    RR = rerun_note(R, D9, I)
    DIV = divergences(R, D9, S1, I)

    # ==================================================================
    # WATERFALL
    # ==================================================================
    wj = {
        "artifact": "step8-waterfall-b", "instance": "analytics-engineer-b", "namespace": "b",
        "step": 8, "mode": "GATE -- proposal only, nothing adopted", "api_calls": 0,
        "run": ("RERUN on the spec as amended through decisions/0093, carrying 0068-0093 and "
                "Red Team's EIGHTH pass"),
        "provenance": provenance_block(),
        "deliverables_of_this_run": {
            "analysis_table": "processed/step8/b/analysis_table.csv.gz",
            "position3_drop_set": ("processed/step8/b/position3_drop_set.csv.gz -- A "
                                   "DELIVERABLE PRODUCED BY THE PIPELINE (decisions/0079 Sec 1), "
                                   "written by the same run that writes the table. D9 half (b) "
                                   "cannot be computed without it and its absence returns 0 "
                                   "SILENTLY"),
            "filter_waterfall": "artifacts/step8-waterfall-b.{md,json}",
            "invariant_report": "artifacts/step8-invariants-b.{md,json}",
            "supporting_processed_outputs": [
                "processed/step8/b/results.json", "processed/step8/b/stage1.json",
                "processed/step8/b/invariants.json", "processed/step8/b/d9.json",
                "processed/step8/b/drop_counts_per_show.csv"],
        },
        "constants": {"W": R["W_adopted"], "H": R["H"], "tau_pull": R["tau_pull"],
                      "W_arms": R["W_arms"],
                      "W_arms_source": "decisions/0075 ruling 3 -- the grid's first statement"},
        "populations": {
            "APPLY": {"n": 196654, "definition": "waterfall line 1 less D10; the position-5 "
                                                 "output; what position 6 filters"},
            "DERIV": {"n": 147370, "definition": "Step 5 line 4 less D10; requires S2 evidence"},
        },
        "filter_order": R["filter_order"],
        "inert_positions": R["inert_positions"],
        "waterfall_APPLY": R["waterfall_APPLY"],
        "waterfall_DERIV": R["waterfall_DERIV"],
        "step5_waterfall_reasserted": R["step5_waterfall_reasserted"],
        "position3_drop_set_deliverable": S1["position3_drop_set"],
        "set_membership_coverage_count": S1["drop_rule"],
        "liveness": {
            "rule": ("NOT LIVE iff BOTH (no insertion instant > tau1) AND (NOT Continued). "
                     "ALT-BROAD, decisions/0048, restored 0054, APPROVED 0064"),
            "silence_test_is_strict": "silent iff no insertion instant > tau1 (0068)",
            "evidence_scope": R["liveness_inputs"]["evidence_scope"],
            "calibration": R["liveness_inputs"]["calibration"],
            "max_insertion_instant_utc": R["liveness_inputs"]["max_insertion_instant_utc"],
            "tau_pull_restriction_is_inert_on_the_exclusion_set": {
                str(w): {"restricted": R["per_arm"]["APPLY"][str(w)]["liveness_excluded"],
                         "unrestricted": R["per_arm"]["APPLY"][str(w)][
                             "liveness_excluded_under_unrestricted_evidence"]}
                for w in W_ARMS},
            "per_arm_APPLY": {str(w): R["per_arm"]["APPLY"][str(w)]["liveness_excluded"]
                              for w in W_ARMS},
            "per_arm_APPLY_started_and_left_component": {
                str(w): R["per_arm"]["APPLY"][str(w)]["liveness_excluded_started_and_left"]
                for w in W_ARMS},
            "per_arm_DERIV": {str(w): R["per_arm"]["DERIV"][str(w)]["liveness_excluded"]
                              for w in W_ARMS},
            "measured_on_build": BUILD,
        },
        "population_reconciliation_703_and_99": rec,
        "outcome_states": {p: {"position5": ex[p]["states_position5"],
                               "position7": R["per_arm"][p]["108"]["states_at_position7"]}
                           for p in ("APPLY", "DERIV")},
        "required_counts": q,
        "D9_split_artifact": D9,
        "censoring_per_air_period_per_W_arm": R["censoring_per_air_period"],
        "emitted_beyond_the_required_list": ex,
        "discovery_channel": R["discovery_channel"],
        "analysis_table": R["analysis_table"],
        "scope_qualifier": ex["scope_qualifier_of_the_Step_9_bound"],
        "where_two_faithful_instances_could_still_differ": DIV,
    }
    # NO EARLY WRITE. The -r6 build wrote this file here, ~2,000 lines before
    # the surface-6 gate ran, so ungated bytes reached propagation surface 6 and
    # were only overwritten if the run got that far. All four files are written
    # once, together, AFTER the gate.

    L: list[str] = []
    A = L.append
    A("# Step 8 — filter waterfall and required counts (instance `b`)")
    A("")
    A(GATE)
    A("")
    A(RR)
    A("")
    A(PROV)
    A("")
    A("**Every figure below states its population.** There are two and they differ by "
      "construction: **APPLY = 196,654** (waterfall line 1 less D10 — the position-5 output, "
      "and what position 6 filters) and **DERIV = 147,370** (Step 5 line 4 less D10, which "
      "requires S2 evidence). Step 8 produces both (`decisions/0070` ruling 1).")
    A("")
    A(f"**Constants.** `W = {R['W_adopted']}` days (`0026`), `H = 91` days (D10), "
      f"`tau_pull = {R['tau_pull']}` (`0011`). `tau1 = ⟦T0⟧ + W × 24h`, "
      f"`tau2 = ⟦T0⟧ + (W + H) × 24h = ⟦T0⟧ + 199 days`. Every boundary test is the "
      "half-open UTC-instant form of Step 1 §2.4; `date(watched_at) <= T1` appears nowhere "
      "in the implementation. **The `W` arm grid is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 "
      "days** (`0075` ruling 3, the first statement of it in any file).")
    A("")
    A("## 0. Deliverables of this run")
    A("")
    A("| Deliverable | Path | Note |")
    A("| :--- | :--- | :--- |")
    A("| Analysis table | `processed/step8/b/analysis_table.csv.gz` | "
      f"{R['analysis_table']['rows']:,} rows × {R['analysis_table']['columns']} columns |")
    A("| **Position-3 drop set** | `processed/step8/b/position3_drop_set.csv.gz` | "
      "**A pipeline deliverable** (`0079` §1), written by the same run that writes the table — "
      "not a helper script's side file. D9 half (b) cannot be computed without it |")
    A("| Filter waterfall | `artifacts/step8-waterfall-b.md` / `.json` | this document |")
    A("| Invariant report | `artifacts/step8-invariants-b.md` / `.json` | |")
    A("")
    A("**Why the drop set is a deliverable and not a working file:** its absence returns **0 "
      "silently**, and a zero split-artifact count reads as **evidence the artefact does not "
      "occur** rather than as a missing input. Leaving it as a helper's side file would defeat "
      "the ruling that requires it, because a side file is not a thing the next run is obliged "
      "to produce.")
    A("")
    A("---")
    A("")
    A("## 1. The filter order, the four inert positions, and the side output")
    A("")
    A(MEAS)
    A("")
    A("Applied in **exactly** this order (`decisions/0029`). The final row set commutes; the "
      "per-filter sample size does not, which is the whole reason the order is mandated.")
    A("")
    for s in R["filter_order"]:
        A(f"{s}  ")
    A("")
    A("**Waterfall line 1 is the S1-completer population, 220,107 pairs** (`0068`). No "
      "instance chooses a base. Lines 2 and 3 follow from it.")
    A("")
    ip = R["inert_positions"]
    A("### Positions 1, 2, 3 and 7 remove zero **by construction**, and are labelled inert")
    A("")
    A(f"**Kept, not removed** (`0079` §4): {ip['why_kept']}. **Labelled, because** "
      f"{ip['why_labelled']}.")
    A("")
    A("| Position | Filter | Removes | Why it is inert |")
    A("| :-- | :--- | ---: | :--- |")
    for pos in (1, 2, 3, 7):
        w = R["waterfall_APPLY"][pos - 1]
        A(f"| **{pos}** | {w['filter']} | {w['removed_pairs']} | {ip['reasons'][str(pos)]} |")
    A("")
    A("**Row 3 is the one that matters.** The *position* is inert; the **rule is the study's "
      "largest single exclusion**, removing **58,345 pairs upstream of line 1**. An unlabelled "
      "always-zero filter reads as evidence **the rule found nothing** when it is evidence "
      "**the rule cannot fire** — the same defect as an unlabelled code check.")
    A("")
    p3 = S1["position3_drop_set"]
    A("### The position-3 drop set")
    A("")
    A(MEAS)
    A("")
    A(f"Written by this pipeline run to `{p3['file']}` (`0079` §1). Under `0068` line 1 *is* the "
      "S1-completer population, so position 3 removes **0 from the waterfall** — which is why "
      "`0075` ruling 2 as first written named an empty set, and why `0077` restated it. The set "
      "is **the pair universe less the completers: 58,345 pairs — position-3 rule, position-5 "
      "build of 2026-08-13** as ruled (`0078`), **reproduced on this build** — carrying each "
      "pair's distinct-episode counts and the show's threshold, which is what half (b) reads. "
      "It is **not** the set-membership drop rule, which is a different rule, deletes **0 "
      "records**, and is counted in records rather than pairs.")
    A("")
    A("| Position-3 drop set | Pairs |")
    A("| :--- | ---: |")
    A(f"| in-frame pairs with any in-`E` S1 or S2 distinct episode | "
      f"{p3['in_frame_pairs_with_ANY_in_E_S1_or_S2_distinct_episode']:,} |")
    A(f"| of which S1 completers — **waterfall line 1** | {p3['of_which_S1_completers_line_1']:,} |")
    A(f"| **dropped by the S1 completion rule** | {p3['dropped_by_the_S1_completion_rule']:,} |")
    A(f"| — carrying S1 evidence that fails the rule | "
      f"{p3['dropped_carrying_S1_evidence_that_fails_the_rule']:,} |")
    A(f"| — carrying S2 evidence and **no S1 evidence at all** | "
      f"{p3['dropped_carrying_S2_evidence_and_NO_S1_evidence']:,} |")
    A(f"| — carrying S2 evidence of any kind | "
      f"{p3['dropped_carrying_S2_evidence_at_all']:,} |")
    A("")
    A("The 278,452 figure is one of the four readings `0068` surveyed before ruling on line 1; "
      "it reproduces here exactly, which is a cross-check on the base rather than a second "
      "candidate for it.")
    A("")
    A("## 2. Waterfall — APPLY")
    A("")
    A(MEAS)
    A("")
    A("| # | Filter | Inert | Retained pairs | Removed | Users | Shows |")
    A("| :-- | :--- | :--- | ---: | ---: | ---: | ---: |")
    for w in R["waterfall_APPLY"]:
        A(f"| {w['position']} | {w['filter']} | {'**INERT**' if w.get('INERT') else 'no'} | "
          f"{w['retained_pairs']:,} | "
          f"{w['removed_pairs']:,} | {w.get('retained_users', ''):,} | "
          f"{w.get('retained_shows', ''):,} |")
    A("")
    A("**Position 2 removes exactly 0 pairs and 0 shows, out of 1,138 shows examined.** That "
      "is a measured zero *and* a structural one: line 1 is already the `L2 > 1` population. "
      "**Position 3 removes 0 by construction** — but the rule (`F1 ∈ D1` and "
      "`|D1| ≥ ceil(0.90 × L1)`, first-pass) was computed independently from the record level, "
      "and it is that computation which produced line 1. This is why the monotone-decrease "
      "invariant is coded `>=` and not `>`: **four positions here legitimately remove nothing.**")
    A("")
    cc = R["step5_waterfall_reasserted"]["adopted_rule_json_cross_check"]
    A("**Position 4 is narrower than its name.** The adopted Step 5 rule (`0021`) is two "
      "disjoint exclusions — S2 evidence entirely air-date-stamped "
      f"({R['waterfall_APPLY'][3]['removed_all_S2_evidence_air_date_stamped']:,}) and a "
      "contaminated `T0` with no S2 evidence at all "
      f"({R['waterfall_APPLY'][3]['removed_contaminated_T0_with_no_S2_evidence']:,}) — and "
      "**not** the Step 5 estimation-sample waterfall down to 128,099. Step 5's own waterfall "
      f"was re-asserted line by line before it was used: measured "
      f"{R['step5_waterfall_reasserted']['measured']}, expected "
      f"{R['step5_waterfall_reasserted']['expected']}.")
    A("")
    A("**`processed/step5/adopted_rule.json` is read and cross-checked, not worked "
      "around.** `0074` ruling 6 made `processed/` the eighth propagation surface and "
      "corrected that file, which had carried revision-3 figures (4,849 removed / 215,258 "
      f"retained). It now states **{cc['file_says_removed']:,} removed / "
      f"{cc['file_says_retained']:,} retained of {cc['file_says_of_total']:,}**, and this "
      f"instance measures **{cc['measured_removed']:,} / {cc['measured_retained']:,} of "
      f"{cc['measured_of_total']:,}** — agreement **{cc['agrees']}**, component by component.")
    A("")
    A("## 3. Waterfall — DERIV")
    A("")
    A(MEAS)
    A("")
    A("| # | Filter | Inert | Retained pairs | Removed |")
    A("| :-- | :--- | :--- | ---: | ---: |")
    for w in R["waterfall_DERIV"]:
        A(f"| {w['position']} | {w['filter']} | {'**INERT**' if w.get('INERT') else 'no'} | "
          f"{w['retained_pairs']:,} | {w['removed_pairs']:,} |")
    A("")
    A("**DERIV's position 4 is not the adopted contamination exclusion alone**, and that is "
      "stated rather than hidden: DERIV is *Step 5 line 4* less D10, and line 4 applies three "
      "further restrictions — `has_s2`, `T0` not contaminated, completing record not "
      "post-dated — none of which is a Step 8 filter position. Emitting it here is what stops "
      "Step 9 rebuilding the population, which would be a second definition of it "
      "(`0070` ruling 1).")
    A("")
    A("## 4. Position 6 — liveness, and the population reconciliation")
    A("")
    A(MEAS)
    A("")
    A("The rule is **ALT-BROAD** (`0048`, restored `0054`, **approved `0064`**): a pair is "
      "**NOT LIVE iff BOTH** the account shows no insertion instant after that pair's `tau1` "
      "**AND** the pair is **NOT Continued**. **\"After\" is STRICT** — silent iff no "
      "insertion instant `> tau1` (`0068`). **The evidence is restricted to records dated "
      "before `tau_pull`** (`0070` ruling 2). The stored play-`id` isotonic calibration at "
      "`processed/step5/calibration.npz` is **read and never refitted** (`0029`).")
    A("")
    A("| Population | n (position 5) | Excluded | Never started | Started and left | Accounts |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for p in ("APPLY", "DERIV"):
        r = rec[p]
        A(f"| {p} | {r['denominator']:,} | {r['measured']:,} | {r['measured_split'][0]:,} | "
          f"{r['measured_split'][1]:,} | {r['measured_accounts']:,} |")
    A("")
    A("**This reconciles exactly with the expectation** — 703 from 216 accounts on APPLY "
      "(604 + 99) and 99 from 73 accounts on DERIV (0 + 99). **It is a population "
      "reconciliation and NOT an invariant.** Neither **604** (the superseded ALT answer) nor "
      "**793** (the withdrawn ALT-MATCHED answer) was produced.")
    A("")
    A("**Line 6 is OUTCOME-CONDITIONAL and is reported as such.** Conjunct 2 *is* the "
      "Continued test, read at `tau2`, so position 6 evaluates a position-7 predicate. That "
      "is permitted: `|A|` and liveness are row-local predicates on the position-5 output and "
      "commute exactly, and `0029`'s ordering rationale concerns per-filter sample size, "
      "which cannot reach position 7 because outcome assignment removes no rows — which is "
      "**position 7's inertness doing load-bearing work** rather than being a tidy footnote.")
    A("")
    A("**Per-`W`-arm exclusion counts, so the `W`-coupling is visible:**")
    A("")
    A("| `W` | " + " | ".join(str(w) for w in W_ARMS) + " |")
    A("| :--- | " + " | ".join("---:" for _ in W_ARMS) + " |")
    A("| APPLY, total | " + " | ".join(
        str(R["per_arm"]["APPLY"][str(w)]["liveness_excluded"]) for w in W_ARMS) + " |")
    A("| APPLY, started-and-left component | " + " | ".join(
        str(R["per_arm"]["APPLY"][str(w)]["liveness_excluded_started_and_left"])
        for w in W_ARMS) + " |")
    A("| DERIV, total | " + " | ".join(
        str(R["per_arm"]["DERIV"][str(w)]["liveness_excluded"]) for w in W_ARMS) + " |")
    A("| APPLY, total, evidence NOT restricted to `< tau_pull` | " + " | ".join(
        str(R["per_arm"]["APPLY"][str(w)]["liveness_excluded_under_unrestricted_evidence"])
        for w in W_ARMS) + " |")
    A("")
    A("The last row is the measurement of `0070` ruling 2 rather than an assumption: **the "
      "`tau_pull` restriction is inert on the exclusion set at every arm**, because the "
      f"largest insertion instant in the sweep is "
      f"**{R['liveness_inputs']['max_insertion_instant_utc']}Z** and D10 already forces "
      "`tau1 ≤ tau_pull − 91 d`. It bites on the robustness tail, not here.")
    A("")
    A("## 5. Right-censoring, as two lines")
    A("")
    A(MEAS)
    A("")
    rc = q["right_censoring_two_lines"]
    A(f"Censored population: **{rc['population_censored']}**.")
    A("")
    A("| Term | Pairs removed | Direction on the headline |")
    A("| :--- | ---: | :--- |")
    A(f"| `max(W, 91)` | {rc['line_a_max_W_91_term']:,} | **UP** on the never-started share |")
    A(f"| incremental `+ H` | {rc['line_b_incremental_plus_H_term']:,} | **UP** on the "
      "never-started share |")
    A(f"| total | {rc['total']:,} | |")
    A("")
    A("Both removals fall on recent S1 completers — people who found an old show lately, have "
      "the whole series available and are disproportionately likely to roll straight into S2. "
      "A single combined figure would hide the price of `H` inside a removal that predates it.")
    A("")
    A("### Retained pairs per air period after right-censoring, every `W` arm")
    A("")
    A(MEAS)
    A("")
    A("**Measured on the position-4 output (201,900), which is what the mandated order "
      "censors** (`0070` ruling 8). `0033`'s 97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed "
      "on the **position-3** output; the order was set at `0029` on the ground that censoring "
      "is objective and independent of behaviour, and **changing a filter order to preserve a "
      "published percentage would be backwards.**")
    A("")
    A("| `W` | all | pre-2020 | 2020–2022 | 2023–2025 |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for w in W_ARMS:
        c = R["censoring_per_air_period"][str(w)]
        A(f"| {w} | {c['ALL']['retained_after_censoring']:,} "
          f"({c['ALL']['retained_pct']:.2f}%) | "
          f"{c['pre-2020']['retained_after_censoring']:,} "
          f"({c['pre-2020']['retained_pct']:.2f}%) | "
          f"{c['2020-2022']['retained_after_censoring']:,} "
          f"({c['2020-2022']['retained_pct']:.2f}%) | "
          f"{c['2023-2025']['retained_after_censoring']:,} "
          f"({c['2023-2025']['retained_pct']:.2f}%) |")
    A("")
    c108 = R["censoring_per_air_period"]["108"]
    c213 = R["censoring_per_air_period"]["213"]
    A(f"**The aggregate hides a cohort-asymmetric loss.** At `W = 108` the pooled retention is "
      f"**{c108['ALL']['retained_pct']:.2f}%** — the figure `0070` corrected from 97.6% — and "
      f"the per-cohort line is **{c108['pre-2020']['retained_pct']:.1f} / "
      f"{c108['2020-2022']['retained_pct']:.1f} / {c108['2023-2025']['retained_pct']:.1f}**. "
      f"At `W = 213` the 2023–2025 cohort retains "
      f"**{c213['2023-2025']['retained_pct']:.2f}%** against "
      f"**{c213['pre-2020']['retained_pct']:.2f}%** pre-2020 — a **"
      f"{100 - c213['2023-2025']['retained_pct']:.1f}%** loss against "
      f"**{100 - c213['pre-2020']['retained_pct']:.1f}%**. Both figures reproduce the task "
      "sheet's corrected pair (10.5% against 3.0%, `0070` ruling 8 and `0073` §1). Without "
      "this line, whether the modern cohort survives to the headline in usable numbers is "
      "invisible — and it is the cohort a roadmap cares about most.")
    A("")
    A("## 6. Drop counts — per show and per outcome")
    A("")
    A(MEAS)
    A("")
    d = q["drop_counts"]
    dn = S1["drop_rule"]["denominator_note"]
    A("**This is a COVERAGE COUNT, not an invariant** (`0074` ruling 3). Records examined and "
      "records dropped are reported; nothing is asserted.")
    A("")
    A(f"- Records examined for set membership: **{d['records_examined']:,}**")
    A(f"- Pairs examined: **{S1['drop_rule']['pairs_examined']:,}**")
    A(f"- Records dropped (`number ∉ E`, or a missing season/number): "
      f"**{d['records_dropped_total']:,}**")
    A(f"- Distinct dropped `(season, number)` pairs: "
      f"**{d['distinct_season_number_pairs_dropped']:,}**; shows with any drop: "
      f"**{d['shows_with_any_drop']:,}** of {d['shows_examined']:,}")
    A(f"- **Per show**, as a distribution over the {d['shows_examined']:,} shows examined "
      "(records dropped → shows): "
      + ", ".join(f"**{k} → {v:,}**"
                  for k, v in d["per_show_distribution_records_dropped_to_shows"].items())
      + ". The full per-show file is `processed/step8/b/drop_counts_per_show.csv`; it is "
        "reproduced here as a distribution rather than 1,138 identical rows.")
    A(f"- **Per outcome**: pairs whose entire S2 evidence was dropped — "
      f"**{d['per_outcome_pairs_whose_entire_S2_evidence_was_dropped']:,}**")
    A(f"  - as a share of Never started **at position 5 = "
      f"{d['denominator_never_started_at_position5']:,}**: "
      f"**{d['share_of_never_started_at_position5_pct']:.4f}%**")
    A(f"  - reported alongside, post-liveness Never started = "
      f"**{d['denominator_never_started_post_liveness']:,}**: "
      f"**{d['share_of_never_started_post_liveness_pct']:.4f}%**")
    A("")
    A("The drop count is a property of the filter, so it measures against **what entered it** "
      "— position 5 (`0070` ruling 6). The difference between the two denominators is exactly "
      "the 604 never-started liveness exclusions, and that is itself informative.")
    A("")
    A("### The denominator — CLOSED, published as a coverage figure, all three readings with "
      "their pipelines named")
    A("")
    A(MEAS)
    A("")
    A("**`0083` §1 CLOSES this and amends `0074` ruling 4's routing to Step 14.** `0074` had "
      "published **6,065,704 against 6,065,610** as *reported, not reconciled*, on the ground "
      "that neither figure is wrong on its face. **That ground was right and the routing was "
      "wrong: there was never a conflict to reconcile.** The readings are points on a "
      "**one-parameter family indexed by where D11 applies**, the parameter is `0068`'s own "
      "open item, and **every member of the family drops zero records** — so the numerator is 0 "
      "three times over, the difference survives into no result, and a Step 14 limitation is an "
      "uncertainty that *does* survive into one. **`0074`'s \"publish both, not one\" stands and "
      "is strengthened to three.**")
    A("")
    dc_ = dn["decomposition_of_the_full_D11_effect"]
    ax = S1["drop_rule"]["other_candidate_axes_for_the_denominator_difference"]
    A("| Reading | D11 applied to | Records examined | Records dropped | Waterfall line 1 |")
    A("| :--- | :--- | ---: | ---: | ---: |")
    A(f"| **A** | nowhere | {dn['READING_A_no_D11_anywhere']:,} | 0 | 220,107 |")
    A(f"| **B — this instance publishes this one** | the S2 side only | "
      f"{dn['READING_B_D11_on_the_S2_side_only_THIS_INSTANCE']:,} | 0 | 220,107 |")
    A(f"| **C** | both seasons | {dn['READING_C_D11_on_both_seasons']:,} | 0 | **220,103** |")
    A("")
    A(f"**The decomposition is exact.** D11 discards "
      f"**{dc_['records_D11_discards_on_the_S1_side']} in-frame S1 records** and "
      f"**{dc_['records_D11_discards_on_the_S2_side']} in-frame S2 records**, "
      f"**{dc_['total']} in total**, and that split is the whole of the difference: "
      f"{dn['READING_A_no_D11_anywhere']:,} − "
      f"{dc_['records_D11_discards_on_the_S2_side']} = "
      f"{dn['READING_B_D11_on_the_S2_side_only_THIS_INSTANCE']:,}, and "
      f"{dn['READING_A_no_D11_anywhere']:,} − {dc_['total']} = "
      f"{dn['READING_C_D11_on_both_seasons']:,}. **`0074`'s 94 is the S2-side component alone**, "
      "which is the gap between readings A and B.")
    A("")
    A("**The other candidate axes were checked and are all zero on this build — re-measured, "
      "not quoted.** `0083` §1 records them as zero on both arms; a figure carried from a "
      "ruling and not re-run can be correct when written and wrong when read, so all three were "
      f"computed again here over the {ax['records_examined']:,} records of reading A's slice: "
      f"undated records **{ax['undated_records_in_the_slice']}**, exact duplicate "
      f"`(user, play id)` records **{ax['exact_duplicate_user_play_id_records_in_the_slice']}**, "
      f"records with a non-positive `number` "
      f"**{ax['records_with_a_non_positive_number_in_the_slice']}**. **The 94 has one cause and "
      "it is fully accounted.**")
    A("")
    A(f"**Stated so the zeros are not read wider than they are:** across the *whole sweep* — "
      f"not the in-frame S1/S2 slice the denominator counts — there are "
      f"**{ax['undated_records_in_the_whole_sweep']}** undated records and "
      f"**{ax['exact_duplicate_user_play_id_records_in_the_whole_sweep']}** exact duplicate "
      "`(user, play id)` records. **None of either is in the slice**, which is why the axis is "
      "zero *for this denominator*; the sweep-level counts are given because a zero reported "
      "without its scope reads as a zero everywhere.")
    A("")
    A("**Why this instance publishes reading B, stated as a reason and not a preference.** D11 "
      "says every record with `watched_at ≥ tau_pull` is discarded from **every** computation, "
      "and this instance applies it everywhere **except** the S1 completion walk. The exception "
      "is not chosen here: `0068` **rules waterfall line 1 at 220,107 as published**, and 4 "
      "pairs reach that count only on a completing record D11 would discard, so reading C "
      "cannot produce the ruled base. The coverage denominator is then a **consequence** of the "
      "record set the pipeline actually examines.")
    A("")
    A("**What stays open, and it is NOT this.** Whether D11 applies to the **S1 completion "
      "walk** is `0068`'s own open item — reading C moves line 1 to **220,103**, because **4 "
      "pairs stop being completers and 0 completion dates move** (§14 measures both). "
      "**Choosing between B and C is that question, answered there, not here.** Recording it in "
      "two places is how a ruling gets made twice and diverges.")
    A("")
    A("**One thing does not move under any reading: all three report 0 records dropped**, and "
      "nothing downstream reads the denominator.")
    A("")
    A(f"**The zero is a measured zero.** Every one of the {d['records_examined']:,} records "
      "was tested for membership in its season's listed set `E`, and none failed. Direction "
      "had any been dropped: it would **inflate** Never started, the same direction as D4 "
      "and D9.")
    A("")
    A("## 7. D2 — negative-lag report, split THREE ways")
    A("")
    A(MEAS)
    A("")
    t168 = q["D2_negative_lag"]["THE_168_MEASURED_ON_EVERY_POPULATION"]
    A("A tie is its own category, not a tiebreak (`0070` ruling 5).")
    A("")
    A("### 7a. The `both bind` count, **measured on every population** — `0070` ruling 5's 168")
    A("")
    A(f"**Unit: {t168['unit']}.**")
    A("")
    A("| Population | n | **pairs where BOTH terms bind** |")
    A("| :--- | ---: | ---: |")
    for k, v in q["D2_negative_lag"]["by_population"].items():
        A(f"| `{k}` | {v['n']:,} | **"
          f"{v['BOTH_terms_bind_tie_ALL_pairs_not_only_negative_lag']:,}** |")
    A("")
    A("**This arm's own defect, corrected rather than patched.** "
      f"{cap1(t168['THIS_ARMS_OWN_DEFECT_CORRECTED'])}.")
    A("")
    A("**And the review premise is measurably false on this data — reported, not reconciled.** "
      f"{cap1(t168['AND_THE_REVIEW_PREMISE_IS_MEASURABLY_FALSE_ON_THIS_DATA'])}.")
    A("")
    A(f"**{t168['invariant_5_reports_the_same_quantity_on_its_own_population']}.**")
    A("")
    A("### 7b. Negative-lag pairs, split three ways")
    A("")
    A("| Population | n | Negative lag | share | S2 finale binds | S1 completion binds | "
      "BOTH bind |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k, v in q["D2_negative_lag"]["by_population"].items():
        A(f"| `{k}` | {v['n']:,} | {v['negative_lag_pairs']:,} | {v['share_pct']:.2f}% | "
          f"{v['S2_finale_term_binds']:,} | {v['S1_completion_term_binds']:,} | "
          f"{v['BOTH_terms_bind_tie']:,} |")
    A("")
    A("**The `BOTH bind` column here is the NEGATIVE-LAG subset and is a different quantity "
      "from §7a's** — same predicate, intersected with `first S2 record < T0`. Both are "
      "emitted because `0070` ruling 5's 168 is §7a's, and reading it off this table gives a "
      "smaller number under the same words.")
    A("")
    A("**Every population the spec could mean is reported and each is labelled** (`0047`, "
      "`0078` §2). S1-term negative lags are the actual test of the "
      "first-pass choice and should be small; S2-finale-term negative lags are the normal "
      "case for anyone who watched a weekly season while it was airing, and their size is "
      "information about the frame's cadence mix rather than about data quality.")
    A("")
    A("## 8. D3′ — resumption rate, every `W` arm, each denominator its own")
    A("")
    A(MEAS)
    A("")
    A("Of pairs scored **Started and left at `tau2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ "
      "tau_pull`, the share completing within `[tau2, tau2 + H)`. **Each arm's denominator is "
      "its own and each population's is its own** (`0069` item 5).")
    A("")
    for pop in ("APPLY", "DERIV"):
        A(f"**{pop}** — Step 8's right-censored population at each arm")
        A("")
        A("| `W` | Started-and-left | cleared | cleared share | completing | share completing |")
        A("| :--- | ---: | ---: | ---: | ---: | ---: |")
        for w in W_ARMS:
            x = q["D3prime"]["per_arm"][pop][str(w)]
            A(f"| {w} | {x['started_and_left_at_this_arm_on_this_population']:,} | "
              f"{x['cleared_count']:,} | "
              f"{x['cleared_share_of_started_and_left_pct']:.2f}% | "
              f"{x['completing_within_the_horizon']:,} | {x['share_completing_pct']:.2f}% |")
        A("")
    a46 = q["D3prime"]["per_arm"]["APPLY"]["46"]["cleared_share_of_started_and_left_pct"]
    a213 = q["D3prime"]["per_arm"]["APPLY"]["213"]["cleared_share_of_started_and_left_pct"]
    A(f"**The cleared-share series on APPLY is {a46:.2f}% at `W = 46` down to {a213:.2f}% at "
      "`W = 213`**, which is the series `0075` ruling 1 adopts. The superseded 95.98% → 91.34% "
      "was measured on the **amendment's uncensored estimation sample**; the population is "
      "stated here at the point of use, on Step 8's right-censored populations.")
    A("")
    a91 = q["D3prime"]["per_arm"]["APPLY"]["91"]["cleared_share_of_started_and_left_pct"]
    a107 = q["D3prime"]["per_arm"]["APPLY"]["107"]["cleared_share_of_started_and_left_pct"]
    A(f"**The series is not monotone between `W = 91` ({a91:.2f}%) and `W = 107` "
      f"({a107:.2f}%)** — an open item at `0076` §5, reproduced here rather than smoothed. The "
      "clearance condition contains `W` twice, once in `tau2` and once in the `+ 2H` horizon, "
      "and the Started-and-left denominator is itself re-derived at every arm, so the series "
      "is not required to be monotone. **Reported, not resolved.**")
    A("")
    t34 = q["D3prime"]["the_3440"]
    A(f"**Reported alongside and labelled a COUNT, not a rate: {t34['count']:,} "
      "Started-and-left pairs completing S2 at any point before `tau_pull`.**")
    A("")
    A(f"- **Population:** {t34['population']}.")
    A(f"- **Why Step 14 calls it a floor:** {t34['why_a_floor']}.")
    A(f"- **Exposure weighting, stated at the point of use:** {t34['exposure_weighting']}.")
    A("- **Restated, not recomputed.** The spec forbids reporting it against APPLY or DERIV, "
      "so no analogue of it is computed on either population here. **Its build is `0034`'s, "
      "not this one's** — which is exactly why `0078` requires the label.")
    A("")
    A("## 9. D8 — never-started post-window diagnostic")
    A("")
    A(MEAS)
    A("")
    A("Measured over `[tau1, tau1 + H) = [tau1, tau2)` — **not to the pull date**. Direction: "
      "**DOWN** on the headline.")
    A("")
    A("| Population / position | Never started | (i) any S2 episode in the horizon | share | "
      "(ii) satisfies the Continued condition | share |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for k, v in q["D8_never_started_post_window"]["by_population_and_position"].items():
        A(f"| {k} | {v['never_started_n']:,} | {v['i_any_S2_episode_in_tau1_to_tau2']:,} | "
          f"{v['i_share_pct']:.2f}% | "
          f"{v['ii_satisfies_the_Continued_condition_over_the_horizon']:,} | "
          f"{v['ii_share_pct']:.2f}% |")
    A("")
    A("**The spec does not say whether D8 sits pre- or post-liveness**, so both are reported "
      "and labelled. D8(ii) is the only bound on the never-started boundary and its size is "
      "Step 14's ledger item 10.")
    A("")
    A("## 10. D9 — split-artifact counts, both halves, **both keys**")
    A("")
    A(MEAS)
    A("")
    A(f"Signature: {D9['signature']}. **{D9['detection']}**")
    A("")
    A("**Four numbers, not three** (`0078` §3): half (a) under strict and loose, half (b) under "
      "strict and loose. The requirement follows from `0074` ruling 5's own reason — the loose "
      "count publishes **because it bounds how wrong strict could be** — and that reason "
      "applies to half (b) exactly as to half (a). Publishing the bound for one half and "
      "withholding it for the other leaves the reader unable to bound the total, and **the "
      "error runs opposite to D9's own lower-bound caveat**.")
    A("")
    A(f"Candidate `(user, show)` pairs examined across the whole sweep: "
      f"**{D9['candidate_user_show_pairs_examined']:,}** — "
      f"{D9['sides']['A_side_S1_not_S2']:,} carrying S1 and not S2, "
      f"{D9['sides']['B_side_S2_not_S1']:,} carrying S2 and not S1, "
      f"{D9['sides']['both_seasons']:,} carrying both.")
    A("")
    cq = D9["COVERAGE_QUANTITIES_EACH_NAMED"]
    A("### 10z. The D9 coverage quantities — **named as separate objects, at the point of use**")
    A("")
    A(MEAS)
    A("")
    _c747 = cq["THE_747478_CHARACTERISATION_WAS_CORRECTED_BY_0089_Sec_2b"]
    A(f"**`0088` §2.** {cap1(cq['ruling'])}. **One name over two quantities is not a "
      "divergence, and reconciling would collapse two real objects into one.** This arm "
      f"publishes **`{cq['THIS_ARM_PUBLISHES_AS_ITS_HEADLINE']}`** and states what each "
      "quantity counts.")
    A("")
    A("***CORRECTED THIS RUN, AND IT IS THIS ARM'S OWN DEFECT.*** **Red Team's eighth pass, F1 "
      "— the finding that occasioned `decisions/0093`.** This arm's `-r6` deliverables "
      "republished `0088` §2(b)'s characterisation — ~~*\"747,478 and 726,103 are different "
      "objects and both correct: undeduplicated user-show **season-coverage rows** against "
      "distinct candidate `(user, show)` **pairs**\"*~~ — **which `0089` §2(b) had corrected two "
      "entries earlier**, and **the table six lines below contradicted it**, giving "
      f"**{cq['undeduplicated_user_show_SEASON_COVERAGE_ROWS']['value']:,}** for that label.")
    A("")
    A(f"**The correction.** {cap1(_c747['the_correction'])}. "
      f"**{cap1(_c747['so_the_two_figures_are_the_SAME_KIND_of_object'])}.**")
    A("")
    A(f"**The relation `0093` §3(c) publishes:** {_c747['the_relation_decisions_0093_Sec_3c_publishes']}. "
      f"**{cap1(_c747['where_these_numbers_come_from'])}.**")
    A("")
    A(f"**Why this is recorded rather than quietly fixed.** "
      f"{cap1(_c747['why_this_is_recorded_rather_than_silently_fixed'])}. **`0089` §2(b) is "
      "implemented IN THIS ARM'S ARTIFACTS as of this run, not only in the spec this instance "
      "read.**")
    A("")
    A("| Quantity | Value | What it counts |")
    A("| :--- | ---: | :--- |")
    for k in ("distinct_candidate_user_show_PAIRS",
              "undeduplicated_user_show_SEASON_COVERAGE_ROWS",
              "distinct_show_IDs_APPEARING_IN_A_D9_COVERAGE_ROW",
              "distinct_SLUGGED_SHOW_IDS_IN_THE_PARSED_SWEEP_the_U1_universe"):
        v = cq[k]
        A(f"| `{k}` | {v['value']:,} | {v['counts']} |")
    A("")
    A("**On the mislabel `0088` §2(a) corrects.** The pivot-side count — show IDs appearing in "
      f"at least one D9 coverage row, **{cq['distinct_show_IDs_APPEARING_IN_A_D9_COVERAGE_ROW']['value']:,}** "
      "here — **is not the sweep**, and this arm labels it for what it is. This arm's slugged "
      "sweep set, the **U1** universe the clustering runs over, is a **different object**: "
      f"**{cq['distinct_SLUGGED_SHOW_IDS_IN_THE_PARSED_SWEEP_the_U1_universe']['value']:,}** show "
      "IDs, of which "
      f"{cq['distinct_SLUGGED_SHOW_IDS_IN_THE_PARSED_SWEEP_the_U1_universe']['of_which_the_slug_string_is_empty']} "
      "carry an empty slug string, built from `processed/step4/parsed/`. **`0088` §2(c): where "
      "the arms' universes differ they are two objects and are named as two — a shared label "
      "over two sets is the defect; the sets themselves may both be right.**")
    A("")
    A("**And the season-coverage row count is not comparable without its mask.** This arm's "
      f"**{cq['undeduplicated_user_show_SEASON_COVERAGE_ROWS']['value']:,}** is over the "
      "**D11-filtered S1/S2 episode records only**. A row count taken over all seasons, or "
      "before D11, is a third object again — which is the whole point of naming it. "
      f"**{cap1(cq['undeduplicated_user_show_SEASON_COVERAGE_ROWS']['IT_IS_NOT_THE_747478_FIGURE'])}.**")
    A("")
    ds = D9["D11_site"]
    A(f"**D11 at this site** (`0088` §1(b)): {ds['records_excluded_by_D11']:,} records excluded "
      f"of {ds['records_in_the_sites_input_universe']:,} "
      f"in the site's input universe; latest `watched_at` used **{ds['latest_watched_at_used_utc']}**; "
      f"assertion holds: **{ds['assertion_holds']}**.")
    A("")
    # -----------------------------------------------------------------
    # decisions/0090 -- D9 PUBLISHES AS A BOUND. This section leads with the
    # interval, because under 0090 the interval IS the result.
    # -----------------------------------------------------------------
    pf = D9["PUBLICATION_FORM_decisions_0090"]
    A("### **D9 publishes as a BOUND** (`0090`) — strict is the floor, loose is the ceiling, "
      "**neither is the point estimate**")
    A("")
    A(f"**{cap1(pf['ruling'])}.** ***SUPERSEDED: {pf['supersedes']}.*** "
      f"**The ground:** {pf['ground']}. **It applies to every D9 quantity with both forms** — "
      f"{pf['applies_to_every_quantity_with_both_forms']}.")
    A("")
    A("| D9 quantity | **BOUND `[strict, loose]`** | Floor (STRICT) | Ceiling (LOOSE) | Point "
      "estimate |")
    A("| :--- | :---: | ---: | ---: | :--- |")
    for k, v in pf["bounds"].items():
        A(f"| {v['quantity']} | **`[{v['floor_STRICT']}, {v['ceiling_LOOSE']}]`** | "
          f"{v['floor_STRICT']} | {v['ceiling_LOOSE']} | **none — `0090`** |")
    A("")
    _hd = pf["bounds"]["complementary_signature_pairs"]
    A(f"**Direction is part of the label and it is not symmetric.** {_hd['direction']}.")
    A("")
    A(f"**A zero floor is not an absence of evidence.** {cap1(_hd['why_the_coverage_is_here'])}. "
      "**The coverage beside the floor, on this build:** "
      f"**{_hd['COVERAGE_BESIDE_THE_FLOOR']['candidate_user_show_pairs_examined']:,}** candidate "
      f"`(user, show)` pairs examined across "
      f"**{_hd['COVERAGE_BESIDE_THE_FLOOR']['distinct_show_ids_appearing_in_a_coverage_row']:,}** "
      "distinct show IDs, on "
      f"**{_hd['COVERAGE_BESIDE_THE_FLOOR']['records_used_after_D11']:,}** S1/S2 records "
      f"surviving D11 — {_hd['COVERAGE_BESIDE_THE_FLOOR']['universe']}.")
    A("")
    A(f"**{cap1(pf['THE_THIRD_KEY_IS_NOT_AN_ENDPOINT'])}.** On this build it gives "
      f"**{pf['THE_THIRD_KEYS_ANSWER_NOT_AN_ENDPOINT']['complementary_signature_pairs']}**.")
    A("")
    A(f"**{cap1(pf['NO_COUNT_MOVES_WITH_THIS_RULING'])}.**")
    A("")
    A("### The keys, which are now defined in the spec")
    A("")
    A("**`0076` §3 defined both keys**, because \"strict\" and \"loose\" had existed only inside "
      "one instance's code and were undefined on every surface an isolated instance reads. "
      "~~**`0074` ruling 5 ruled STRICT**~~ — ***that framing is SUPERSEDED by `0090`: strict is "
      "the floor of a published bound, not the answer. The keys themselves are unchanged.***")
    A("")
    A("| Key | Definition | Complementary signature pairs |")
    A("| :--- | :--- | ---: |")
    for k, v in D9["keys"].items():
        A(f"| `{k}` | {v['definition']} | {v['complementary_signature_pairs']:,} |")
    A("")
    A("**The two admissible readings of \"a trailing four-digit year\" agree on this data** — "
      "restricting the four digits to `19xx`/`20xx` and not restricting them both give "
      f"{D9['keys']['LOOSE']['complementary_signature_pairs']}. **The third key — a trailing "
      "digit group of arbitrary length, which reduces `the-100` to `the` — gives "
      f"{D9['keys']['THIRD_KEY_NOT_USED']['complementary_signature_pairs']} here.** That is "
      "not a key of this study; it is measured so that the divergence `0076` describes is "
      "visible on this instance's own data rather than only in the decision log.")
    A("")
    A("### Half (a) — fabricated never-started rows")
    A("")
    A("| Population / position | Never started | **BOUND `[floor, ceiling]`** | floor STRICT | "
      "ceiling LOOSE | Bound as a share |")
    A("| :--- | ---: | :---: | ---: | ---: | :---: |")
    for k, v in D9["half_a_fabricated_never_started_rows"].items():
        bd = v["BOUND_decisions_0090"]
        sh = v["BOUND_as_a_share_of_never_started_pct"]
        A(f"| {k} | {v['never_started_n']:,} | **`[{bd['floor_STRICT']}, "
          f"{bd['ceiling_LOOSE']}]`** | {v['carrying_a_split_signature_STRICT']:,} | "
          f"{v['carrying_a_split_signature_LOOSE']:,} | "
          f"`[{sh[0]:.4f}%, {sh[1]:.4f}%]` |")
    A("")
    A("**No point estimate on any row** (`0090`). The interval is the result.")
    A("")
    A("### Half (b) — the silently deleted S1-failing counterparts")
    A("")
    hb = D9["half_b_silently_deleted_S1_failing_counterparts"]
    A("**Measured on position 3's drop set** (`0075` ruling 2), which this run writes as a "
      f"deliverable. {cap1(hb['why_they_are_invisible_otherwise'])}.")
    A("")
    _hbb = hb["BOUND_decisions_0090"]
    A("| | **BOUND `[floor, ceiling]`** | floor STRICT | ceiling LOOSE |")
    A("| :--- | :---: | ---: | ---: |")
    A(f"| B-side pairs on frame shows | "
      f"**`[{_hbb['B_side_pairs_in_frame']['floor_STRICT']}, "
      f"{_hbb['B_side_pairs_in_frame']['ceiling_LOOSE']}]`** | "
      f"{hb['STRICT']['B_side_pairs_in_frame']:,} | "
      f"{hb['LOOSE']['B_side_pairs_in_frame']:,} |")
    A(f"| of those, present in the position-3 drop set | "
      f"**`[{_hbb['present_in_the_retained_position3_drop_set']['floor_STRICT']}, "
      f"{_hbb['present_in_the_retained_position3_drop_set']['ceiling_LOOSE']}]`** | "
      f"{hb['STRICT']['of_those_present_in_the_retained_position3_drop_set']:,} | "
      f"{hb['LOOSE']['of_those_present_in_the_retained_position3_drop_set']:,} |")
    A(f"| of those, in the S2-evidence-and-no-S1-evidence subset | "
      f"**`[{_hbb['in_the_S2_and_no_S1_subset']['floor_STRICT']}, "
      f"{_hbb['in_the_S2_and_no_S1_subset']['ceiling_LOOSE']}]`** | "
      f"{hb['STRICT']['of_those_in_the_S2_evidence_and_NO_S1_evidence_subset']:,} | "
      f"{hb['LOOSE']['of_those_in_the_S2_evidence_and_NO_S1_evidence_subset']:,} |")
    A("")
    A("**`0078` §3 put both keys on this half; `0090` makes the pair an interval rather than an "
      "answer with a footnote.** **No point estimate on any row.**")
    A("")
    A(f"Every one of the {hb['LOOSE']['B_side_pairs_in_frame']} loose-key B-side pairs is "
      "accounted for inside the drop set — **which is the check that the side output is the "
      "right population and not merely a convenient one.** **The strict zero is a computed "
      "zero on a present input, not a zero returned by a missing one**, which is the "
      "distinction `0079` §1 exists to preserve.")
    A("")
    nf = D9["normalisation_finding"]
    A(f"**{nf['what_it_shows']}.**")
    A("")
    A("### 10a. The clustering universe — **U1, ruled, ranked by distinct strict keys merged**")
    A("")
    cl = nf["clustering_universes"]
    A("**`0088` §3 RULES IT.** *The D9 clustering universe is **U1** — every distinct show ID "
      "appearing anywhere in the pulled sweep that carries a slug, deduplicated to one row per "
      "show ID — **ranked by DISTINCT STRICT KEYS MERGED**, i.e. how many separate metadata "
      "entries the loose key collapsed into one.* **NOT U2 (the 1,138 frame shows) and NOT U3 "
      "(the 75 D9 candidate pairs).** The ground is `0088`'s: the artifact D9 hunts is a "
      "history **splitting across two metadata entries**, and that can occur **anywhere in a "
      "history, not only among shows that survived the frame filters** — a frame-restricted "
      "universe finds only splits where **both sides made the cut**, and **a bound computed on "
      "a narrow slice bounds very little**.")
    A("")
    A(f"**THIS ARM PUBLISHES `{cl['PUBLISHED_UNIVERSE']}`, ranked on the ruled basis.** "
      f"{cap1(cl['CHANGED_FROM_THIS_ARMS_PREVIOUS_BUILD'])}")
    A("")
    A("| Universe | Unit | Members examined | Distinct loose keys | Max cluster | "
      "Largest clusters |")
    A("| :--- | :--- | ---: | ---: | ---: | :--- |")
    for k, v in cl["universes"].items():
        lst = ", ".join(f"`{a}` ({b})" for a, b in v["largest_clusters"].items())
        star = " **(PUBLISHED)**" if k == cl["PUBLISHED_UNIVERSE"] else ""
        A(f"| `{k}`{star} | {v['unit']} | {v['members_examined']:,} | "
          f"{v['distinct_loose_keys']:,} | {v['max_cluster_size']} | {lst} |")
    A("")
    u1 = cl["universes"]["U1_all_sweep_show_ids_carrying_a_slug"]
    alt = u1["ALTERNATE_BASIS_ranked_by_distinct_show_IDs"]
    A("**The basis needed ruling because it reorders the list on its own.** Same universe, same "
      "key, two bases:")
    A("")
    A("| Ranking basis | Largest clusters |")
    A("| :--- | :--- |")
    A("| **distinct STRICT keys merged (RULED)** | "
      + ", ".join(f"`{a}` ({b})" for a, b in u1["largest_clusters"].items()) + " |")
    A("| distinct show IDs (not ruled) | "
      + ", ".join(f"`{a}` ({b})" for a, b in alt["largest_clusters"].items()) + " |")
    A("")
    tb = u1["THE_TIE_BREAK_IS_NOT_RULED"]
    A(f"**REPORTED, NOT RECONCILED — the ruling fixes the BASIS and not the TIE-BREAK, and the "
      f"tie is occupied.** `0088` §3 names the U1 top three as `secondchance` (8), `theisland` "
      f"(7), `maigret` (6). **The first two are unique at their counts and this build "
      f"reproduces them exactly.** The third is inside a "
      f"**{tb['keys_tied_at_the_third_place_count']}-way tie at "
      f"{tb['third_place_count']}** — "
      + ", ".join(f"`{x}`" for x in tb["tied_keys"]) +
      f" — so **which name appears third is decided by a rule no surface states**. Under this "
      f"arm's tie-break ({tb['this_arms_tie_break']}) it is **`{tb['this_arms_third_name']}`**; "
      "`maigret` is equally correct under a different one. **This is a spec gap inside the "
      "ruling that closed the previous spec gap, and it is reported rather than resolved by "
      "picking the name that matches the entry.**")
    A("")
    A(f"**{cap1(cl['note_the_unit_differs_between_universes'])}.** Coverage: "
      f"{cap1(cl['coverage'])}.")
    A("")
    wn = cl["WHAT_NAMING_THE_UNIVERSE_LOCATES"]
    A(f"**What naming the universe located.** {wn['finding']}. **{cap1(wn['what_it_means'])}.** "
      f"Maxima reproduced on this build: **U1 = {wn['reproduced_U1_max']}**, "
      f"**U3 = {wn['reproduced_U3_max']}** — `0085` §2's *\"maxima 8 against 10\"*, both from "
      f"one run. {cap1(wn['and_the_basis_matters_too'])}. Source of the quoted lists: "
      f"{wn['quoted_lists_source']}.")
    A("")
    A(f"**{cap1(nf['THE_LIST_THIS_REPLACES'])}.**")
    A("")
    A("**No count moves with the ruling.** D9's **search** already ran on the whole sweep in "
      "this arm — 726,103 candidate pairs — so the strict and loose complementary-pair counts "
      "are unchanged at **0** and **75**. What the ruling fixes is **which clusters are "
      "illustrated**, which is the evidence for the loose key's only warrant.")
    A("")
    A(f"**Why the interval publishes rather than a point estimate:** {nf['consequence']}. "
      "**Neither endpoint is the answer** (`0090`): strict is the **floor**, loose is the "
      "**ceiling**. ***Corrected this run (Red Team seventh pass, finding 1, second half): "
      "`-r5` rendered this line as \"Why the loose count publishes EVEN THOUGH STRICT IS "
      "RULED\" — `0074` ruling 5's framing, which `0090` supersedes — and it sat "
      "well below the line in §10 that strikes exactly that framing. Same file, same class of "
      "defect as the assertion-set count: the replacement above, the superseded text below.***")
    A("")
    A(f"Direction: {D9['direction']}.")
    A("")
    A("## 11. D4 — S3 without S2")
    A("")
    A(MEAS)
    A("")
    A("Pairs scored Never started that carry S3-or-later episode records on that show and "
      "**no S2 episode record at all**. Emitted here because Step 8 holds the episode-level "
      "evidence and Step 9 does not (`0070` ruling 7). Direction: **inflates** Never started; "
      "Step 9 bounds it and publishes it **alongside**, never folded in.")
    A("")
    A("| Population / position | Never started | S3-without-S2 | Share |")
    A("| :--- | ---: | ---: | ---: |")
    for k, v in q["D4_S3_without_S2"]["by_population_and_position"].items():
        A(f"| {k} | {v['never_started_n']:,} | {v['S3_without_S2_pairs']:,} | "
          f"{v['share_of_never_started_pct']:.4f}% |")
    A("")
    A("**The DERIV zero is structural, not a measurement of nothing**: DERIV requires S2 "
      "evidence, and a D4 pair has none by definition.")
    A("")
    A("## 12. D12 — per-bucket show and pair counts, all five buckets")
    A("")
    A(MEAS)
    A("")
    A("| Bucket | Shows | Pairs, position 4 | Pairs, APPLY position 5 | "
      "Pairs, DERIV position 5 |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for bk, v in q["D12_cadence_buckets"]["buckets"].items():
        A(f"| {bk} | {v['shows']:,} | {v['pairs_position4']:,} | "
          f"{v['pairs_APPLY_position5']:,} | {v['pairs_DERIV_position5']:,} |")
    A("")
    A(f"**Shows within 1 day of a bucket boundary: "
      f"{q['D12_cadence_buckets']['shows_within_1_day_of_a_bucket_boundary']}** of "
      f"{q['D12_cadence_buckets']['shows_examined']:,} examined. **C0 = 0 of 1,138 shows "
      "examined** — a measured zero, not an unexamined one.")
    A("")
    A("## 13. Metadata-disagreement counts")
    A("")
    A(MEAS)
    A("")
    A("| Flag | Shows | Pairs at position 4 |")
    A("| :--- | ---: | ---: |")
    for k, v in q["metadata_disagreement"]["flags"].items():
        A(f"| `{k}` | {v['shows']:,} | {v['pairs_position4']:,} |")
    A("")
    A(f"**{cap1(q['metadata_disagreement']['coverage_note'])}.**")
    A("")
    A(f"Direction, named as required: {q['metadata_disagreement']['s2_aired_lt_listed_direction']}.")
    A("")
    A("## 14. `pull_date`, fetch window, and discarded records")
    A("")
    A(MEAS)
    A("")
    pd_ = q["pull_date_and_fetch_window"]
    A(f"- `pull_date` = **{pd_['pull_date']}**, `tau_pull` = **{pd_['tau_pull']}**")
    A(f"- Earliest per-user fetch: **{pd_['earliest_per_user_fetch']}**")
    A(f"- Latest per-user fetch: **{pd_['latest_per_user_fetch']}**")
    A(f"- Records discarded for `watched_at >= tau_pull`: "
      f"**{pd_['records_discarded_for_watched_at_ge_tau_pull']:,}**, of which "
      f"**{pd_['of_which_in_frame_S1_or_S2_episode_records']}** are in-frame S1/S2 episode "
      "records")
    A("")
    A(f"{cap1(pd_['note'])}.")
    A("")
    A("### The D11 open question, measured rather than assumed")
    A("")
    o = q["D11_open_question"]
    A(f"`0068` rules line 1 at **{o['line_1_as_ruled']:,} as published** and records "
      "separately as **OPEN** whether D11 moves it. Measured here: applying D11 to the S1 "
      f"completion walk as well gives **{o['line_1_if_D11_is_applied_to_the_S1_completion_walk_too']:,}**, "
      f"a difference of **{o['pairs_affected']}** pairs. "
      f"**All {o['pairs_affected']} are removed at position 5 under either reading** — "
      "checked row by row, not argued — because "
      "their first-pass completion instant is at or after `tau_pull`, so `T0` is at or after "
      "2026-08-10 and D10 removes them. **Lines 4 through 7 and every published figure are "
      "identical under both readings; only lines 1, 2 and 3 move.** The table column "
      "`s1_completion_used_a_post_cutoff_record` is what carries this question downstream.")
    A("")
    cmpx = o["completer_set_comparison"]
    A(f"**Both halves of `0083` §1's statement are measured here, not quoted.** Reading C "
      f"**removes {cmpx['in_B_and_NOT_in_C_pairs_that_stop_being_completers']} pairs** from the "
      f"completer set and **adds {cmpx['in_C_and_NOT_in_B']}**; of the "
      f"{cmpx['common_pairs_examined']:,} pairs common to both readings, "
      f"**{cmpx['of_those_whose_first_pass_completion_DATE_MOVES']} have a first-pass "
      "completion date that moves.** The second half matters on its own: the count alone would "
      "not establish that no *surviving* pair's clock start changes, and a moved clock start is "
      "what would push the difference past lines 1–3 into the published figures.")
    A("")
    # ------------------------------------------------------------------
    # 14a. B3 -- decisions/0088 Sec 1
    # ------------------------------------------------------------------
    b3 = R["B3_the_two_unasserted_mandates"]
    A("## 14a. B3 — the two unasserted mandates, **measured, not self-reported**")
    A("")
    A(MEAS)
    A("")
    A(f"**`0088` §1.** {cap1(b3['ruling'])}. **The ground:** {b3['ground']}.")
    A("")
    A("### (a) The boundary window — **the SEPARATING interval, corrected by `0089` §2(a)**")
    A("")
    bw = b3["a_boundary_window"]
    A(f"{cap1(bw['what_it_measures'])}. **{cap1(bw['compliance_self_report'])}.**")
    A("")
    A(f"**THE INTERVAL WAS WRONG ON THIS ARM'S PREVIOUS BUILD, AND SO WAS THE VERDICT TAKEN "
      f"OFF IT.** {cap1(bw['THE_INTERVAL_WAS_CORRECTED'])}.")
    A("")
    A("| Population | Unit | **`[τ1, τ1+24h)` SEPARATING** | **`[τ2, τ2+24h)` SEPARATING** | "
      "`[τ1−24h, τ1)` agreeing | `[τ2−24h, τ2)` agreeing | at `τ1` | at `τ2` | Examined |")
    A("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for pk, pv in bw["by_population"].items():
        de = pv["DISTINCT_EPISODES_the_form_the_outcome_assignment_reads"]
        rr = pv["RAW_RECORDS_the_ruling's_own_word"]
        A(f"| {pk} | distinct S2 episodes (what `|A|` counts) | "
          f"**{de['SEPARATING_in_[tau1, tau1_plus_24h)']:,}** | "
          f"**{de['SEPARATING_in_[tau2, tau2_plus_24h)']:,}** | "
          f"{de['AGREEING_in_[tau1_minus_24h, tau1)']:,} | "
          f"{de['AGREEING_in_[tau2_minus_24h, tau2)']:,} | "
          f"{de['exactly_at_tau1']} | {de['exactly_at_tau2']} | "
          f"{de['episodes_examined']:,} |")
        A(f"| {pk} | raw in-E2 S2 records | "
          f"**{rr['SEPARATING_in_[tau1, tau1_plus_24h)']:,}** | "
          f"**{rr['SEPARATING_in_[tau2, tau2_plus_24h)']:,}** | "
          f"{rr['AGREEING_in_[tau1_minus_24h, tau1)']:,} | "
          f"{rr['AGREEING_in_[tau2_minus_24h, tau2)']:,} | "
          f"{rr['exactly_at_tau1']} | {rr['exactly_at_tau2']} | {rr['records_examined']:,} |")
    A("")
    for pk, pv in bw["by_population"].items():
        lv = pv["LIVENESS_EVIDENCE_at_tau1"]
        A(f"- **{pk}, the STRICT silence test's own boundary** — max insertion instant in "
          f"`[τ1−24h, τ1)`: **{lv['max_insertion_instant_in_[tau1_minus_24h, tau1)']}**; "
          f"exactly at `τ1`: **{lv['max_insertion_instant_exactly_at_tau1']}**, on "
          f"{lv['rows_examined']:,} rows. **A different axis from the one above** — "
          f"{lv['why_this_one_is_here']}.")
    A("")
    A("#### The four numbers that settle B3 — **rows changing OUTCOME STATE**")
    A("")
    fn = bw["THE_FOUR_NUMBERS_THAT_SETTLE_B3"]
    A(f"{cap1(fn['definition'])}. **The forbidden form is computed only here,** "
      f"{fn['the_forbidden_form_is_computed_ONLY_here']}.")
    A("")
    A("| Population | `τ1` relaxed | `τ2` relaxed | **both — the full forbidden form** | Rows |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for pk, pv in bw["by_population"].items():
        wd = pv["WHAT_THE_FORM_DECIDES"]
        A(f"| {pk} | **{wd['tau1_relaxed_only']['rows_changing_outcome_state']}** | "
          f"**{wd['tau2_relaxed_only']['rows_changing_outcome_state']}** | "
          f"**{wd['BOTH_bounds_relaxed_the_full_forbidden_form']['rows_changing_outcome_state']}**"
          f" | {wd['tau1_relaxed_only']['rows_examined']:,} |")
    A("")
    for pk, pv in bw["by_population"].items():
        wd = pv["WHAT_THE_FORM_DECIDES"]
        tr = ", ".join(f"**{k}** {v}" for k, v in
                       wd["BOTH_bounds_relaxed_the_full_forbidden_form"]["transitions"].items())
        A(f"- **{pk} transitions under the full forbidden form:** {tr}. Rows holding an S2 "
          f"episode in the separating interval: "
          f"**{wd['rows_with_an_S2_episode_in_the_SEPARATING_interval_at_tau1']}** at `τ1` and "
          f"**{wd['rows_with_an_S2_episode_in_the_SEPARATING_interval_at_tau2']}** at `τ2` — "
          f"more rows than change state, because most already have `|A| ≥ 1` or already fail "
          f"the Continued test.")
    A("")
    for pk, pv in bw["by_population"].items():
        wd = pv["WHAT_THE_FORM_DECIDES"]
        a_, b_, j_ = (wd["tau1_relaxed_only"]["rows_changing_outcome_state"],
                      wd["tau2_relaxed_only"]["rows_changing_outcome_state"],
                      wd["BOTH_bounds_relaxed_the_full_forbidden_form"][
                          "rows_changing_outcome_state"])
        A(f"- **{pk} — the two per-bound counts sum to the joint one on this data: "
          f"{a_} + {b_} = {j_} — {a_ + b_ == j_}.** **Measured, not assumed.** They need not: a "
          "row moved out of never-started by the `τ1` relaxation could be moved again by the "
          "`τ2` one, and that row would be counted once in the joint form and twice in the "
          "sum. **No row does both here**, which is why the joint count is reported as its own "
          "number rather than left to be added.")
    A("")
    for pk, pv in bw["by_population"].items():
        A(f"- **{pk} — `{pv['VERDICT_STATE']}`.** {pv['VERDICT']}.")
    A("")
    A("**THE MANDATE IS LOAD-BEARING ON THE RESULT, AND THAT IS THE FINDING.** `0088` §1(a) "
      "instructs that a zero be **labelled vacuous rather than passed silently**. It is not "
      "zero, and it is not inert either: the forbidden `date(watched_at) <= T1` form would move "
      f"**{fn['APPLY_position5_both_bounds_relaxed']} rows on APPLY** and "
      f"**{fn['DERIV_position5_both_bounds_relaxed']} on DERIV** into a different outcome state. "
      "**Three states, not two:** an empty separating interval, an occupied one that decides no "
      "outcome, and an occupied one that decides one. **This build is the third**, and this "
      "arm's previous build published the second — because it measured the interval on which "
      "the two forms *agree* plus the single instant at `τ1`, and read a verdict about "
      "disagreement off it. **That is corrected here, not carried.**")
    A("")
    A("**Reconciled with what the decision log records of the other arm, without reading its "
      "output.** `0089` §2(a) quotes 703 episodes on 311 rows at `τ1` and 303 on 136 at `τ2` on "
      "APPLY, 595/275 and 261/117 on DERIV. **This build measures the same six numbers** — the "
      "table and the bullets above. **Those figures were taken from `decisions/0089`, a spec "
      "surface this instance is required to read, not from the other arm's folder.** **The "
      "outcome-state counts are new: `0089` §2(a) records them as measured by neither arm.**")
    A("")
    A("### (b) The per-site D11 table — **asserted at each site, not once and about the rest**")
    A("")
    ps = b3["b_per_site_D11_table"]
    _vac = ps["EVERY_SITE_CARRIES_A_BOOLEAN_ASSERTION_AND_AN_EXAMINED_COUNT"][
        "sites_whose_pass_is_VACUOUS_zero_coverage"]
    A(f"{cap1(ps['what_it_measures'])}. **{ps['sites_counted']} sites; D11 applied at "
      f"{ps['sites_where_D11_is_applied']}"
      + (f", of which {len(_vac)} had ZERO records ENTER them and their passes are VACUOUS"
         if _vac else "") + ".**")
    A("")
    _tq = ps["THE_EXAMINED_COLUMN_HELD_TWO_QUANTITIES_AND_NOW_HOLDS_TWO_COLUMNS"]
    A("***CORRECTED THIS RUN — Red Team's eighth pass, F3, against this arm.*** "
      f"{cap1(_tq['finding'])}. **{cap1(_tq['why_it_was_load_bearing_and_not_cosmetic'])}.** "
      f"**The fix:** {_tq['the_fix']}.")
    A("")
    A(f"**Units are not uniform and that is stated per row.** {cap1(_tq['units_are_not_uniform_and_that_is_stated_per_row'])}. "
      f"**And the S1-walk row has `before = after`** — {_tq['the_S1_walk_row_has_before_EQUAL_TO_after']}.")
    A("")
    A("| Site | D11 applied | **INPUT UNIVERSE, before D11** | **counted, after D11** | "
      "Records excluded | Unit | Coverage state | Assertion holds |")
    A("| :--- | :---: | ---: | ---: | ---: | :--- | :--- | :--- |")
    for s in ps["sites"]:
        # NO RENDER-TIME PATCH. The -r5 build filled the D9 row HERE, in the
        # renderer, from d9.json -- so the .md showed a number and the published
        # .json showed `null`, two definitions of one row with only one visible
        # to a JSON reader. The backfill now happens in the PIPELINE, at stage 3,
        # and this renderer reads whatever the table holds.
        exc = "—" if s["records_excluded_by_D11"] is None else f"{s['records_excluded_by_D11']:,}"
        _pre = s.get("records_in_the_INPUT_UNIVERSE_before_D11")
        _post = s.get("records_COUNTED_after_D11")
        pre = "**— NONE STATED**" if not isinstance(_pre, int) else f"{_pre:,}"
        post = "**— NONE STATED**" if not isinstance(_post, int) else f"{_post:,}"
        cs = s.get("coverage_state") or "**— NONE STATED**"
        if s.get("assertion_is_VACUOUS_zero_coverage"):
            ah = "**VACUOUS — nothing entered**"
        elif s["assertion_holds"] is None:
            ah = "**— NOT ASSERTED**"
        elif s["assertion_holds"]:
            ah = "**yes**"
        else:
            ah = "**NO — by design, see below**"
        nm = s["site"].replace("|", "\\|")
        A(f"| `{nm}` | {'yes' if s['d11_applied'] else '**no**'} | {pre} | {post} | {exc} | "
          f"{s['unit'].replace('|', chr(92) + '|')} | `{cs}` | {ah} |")
    A("")
    ev = ps["EVERY_SITE_CARRIES_A_BOOLEAN_ASSERTION_AND_AN_EXAMINED_COUNT"]
    A(f"**Every row carries a boolean assertion, an INPUT-UNIVERSE count and a counted-after-D11 "
      f"count** — {ev['sites_with_a_boolean_assertion']} of {ev['sites']}, "
      f"{ev['sites_with_an_INPUT_UNIVERSE_count']} of {ev['sites']} and "
      f"{ev['sites_with_a_COUNTED_after_D11_count']} of {ev['sites']}, **each asserted.** "
      f"**Coverage states:** "
      + "; ".join(f"`{k}` **{len(v)}**" for k, v in ev["coverage_states"].items())
      + f". **Vacuity now keys on the INPUT UNIVERSE: {ev['VACUITY_NOW_KEYS_ON_THE_INPUT_UNIVERSE']}.** "
      f"**{cap1(ev['why'])}.**")
    A("")
    if ev["sites_FULLY_EXCLUDED_which_are_NOT_vacuous"]:
        A("**`FULLY_EXCLUDED`, and it is NOT vacuous:** "
          + ", ".join(f"`{x}`" for x in ev["sites_FULLY_EXCLUDED_which_are_NOT_vacuous"])
          + ". **Their entire input universe was at or after `τ_pull` and D11 removed all of "
            "it.** On the previous build these rows would have printed `examined = 0` and been "
            "labelled **VACUOUS** — *\"this site examined 0 records\"* — at the sites where D11 "
            "did **the most** work. That inversion is Red Team's F3, and it runs in the "
            "direction of a false pass.")
        A("")
    else:
        A("**No site is `FULLY_EXCLUDED` on this build** — no site's entire input universe sits "
          "at or after `τ_pull`. **Stated as a measured zero, not passed silently:** the class "
          "exists in the code and is empty on this data, which is what makes the previous "
          "build's single column a **latent** inversion rather than a live wrong number. "
          "**The defect was in what the label would have said, and no published figure moves.**")
        A("")
    A("***Corrected this run.*** **The `D9 coverage rows` row published `null` for BOTH its "
      "exclusion count and its assertion in `-r5`'s `results.json`**, while the site was counted "
      "among the twelve where D11 is applied — **a row listed as asserted and carrying no "
      "assertion.** The number was in `d9.json` the whole time, and the `.md` filled it *in the "
      "renderer*, so the two halves of one deliverable disagreed and only the JSON reader could "
      "see it. **The backfill is now a pipeline step (stage 3), asserted at the site**, and the "
      "renderer patches nothing.")
    A("")
    if ev["sites_whose_pass_is_VACUOUS_zero_coverage"]:
        A("***And a pass on an empty site is labelled VACUOUS rather than printed as a "
          "pass.*** " + ", ".join(f"`{x}`" for x in ev["sites_whose_pass_is_VACUOUS_zero_coverage"])
          + " had **0** records **enter** them, so their assertions are true of the empty set and are **not "
          "evidence that D11 is applied there**. The examined count was printed on the previous "
          "build — that half of the rule was met — but `assertion_holds: true` read identically "
          "at a site with 2.7 million records and at a site with none. **A check that finds "
          "nothing because it looked nowhere must fail, not pass** (`CLAUDE.md`; `0088` §1(a) "
          "says the same of the boundary window).")
        A("")
    ns = ps["THE_EXCLUSION_COLUMN_IS_NOT_SUMMABLE_AND_THE_ROWS_ARE_NOT_DISJOINT"]
    A(f"**The `Records excluded` column is NOT summable and its rows are NOT disjoint.** "
      f"{cap1(ns['why'])}. **Units present:** "
      + "; ".join(f"*{u}*" for u in ns["units_present"]) + f". **Overlaps:** {ns['overlaps']}.")
    A("")
    A("**And the identity that makes the two new columns a MEASUREMENT rather than a relabel, "
      "asserted.** At the eight `action_count_*` sites both columns and the exclusion column are "
      "in the same unit, so **input universe − counted = excluded** must hold exactly: "
      f"**{ns['identity_before_minus_after_equals_excluded_at_the_8_action_sites']}**. "
      "**This is the check that catches an input universe measured on an already-filtered "
      "array** — which it did, on this run, before any write: the first attempt measured the "
      "S2 sites' universe on the post-mask array and reported an already-post-exclusion number "
      "under the label *before D11*, **the F3 defect one level down, on the S2 side only.** "
      f"**Where the identity does NOT hold, and why:** {ns['where_the_identity_does_NOT_hold_and_why']}.")
    A("")
    A(f"**The two figures that DO sum, asserted:** {ns['the_two_figures_that_DO_sum']} — "
      f"S1 side **{ns['identity_s1_side']}**, S2 side **{ns['identity_s2_side']}**, total "
      f"**{ns['identity_total']}**.")
    A("")
    A(f"**Site names are this arm's own and are not a ruled vocabulary — reported, not "
      f"reconciled.** {ps['SITE_NAMES_ARE_THIS_ARMS_OWN_AND_ARE_NOT_A_RULED_VOCABULARY']}.")
    A("")
    A("**The one site where D11 is not applied is the S1 completion walk**, and the `no` there "
      "is the **correct reported state, not a failure**: `0068` rules waterfall line 1 at "
      "**220,107 as published**, that value needs the pairs whose first-pass completion rests "
      "on a post-cutoff record, and whether D11 applies to the walk is `0068`'s own **open** "
      "item. Three different objects sit behind it and are named separately — **73 records**, "
      "**72 distinct episodes**, **60 episodes whose *canonical* instant is post-cutoff**.")
    A("")
    ch = ps["pairs_whose_action_counts_moved"]
    A(f"**THIS RUN CHANGES SOMETHING, AND THE PER-SITE ASSERTION IS WHAT EXPOSED IT.** "
      f"{cap1(ps['THIS_RUNS_OWN_CHANGE'])}. **Size of the change:** "
      f"{ch['in_the_record_universe']} pairs in the record universe, of which "
      f"**{ch['of_those_present_in_the_APPLY_position5_row_set']} are in the APPLY position-5 "
      f"row set** and {ch['of_those_present_in_the_DERIV_position5_row_set']} in DERIV's; "
      f"columns affected: {', '.join('`' + c + '`' for c in ch['columns_affected'])}. "
      f"{cap1(ch['no_other_column_moves'])} — **line 1 is 220,107 and position 5 is 196,654 on "
      "this build, unchanged.**")
    A("")
    A("### (c) The promoted assertion — published, labelled **CODE CHECK**")
    A("")
    pr = b3["c_the_promoted_assertion"]
    A(f"**`{pr['assertion']}`.** {cap1(pr['ruling'])}. It is **invariant 9** in "
      "`artifacts/step8-invariants-b.md`.")
    A("")
    A("| Population | Rows examined | `tau2 > tau_pull` | `tau2` **exactly at** `tau_pull` | "
      "Latest `tau2` |")
    A("| :--- | ---: | ---: | ---: | :--- |")
    for pk, pv in pr["by_population"].items():
        A(f"| {pk} | {pv['rows_examined']:,} | {pv['rows_with_tau2_gt_tau_pull']} | "
          f"{pv['rows_with_tau2_EXACTLY_at_tau_pull']} | {pv['latest_tau2_utc']} |")
    A("")
    A(f"**{cap1(pr['the_bound_is_ATTAINED_not_slack'])}.**")
    A("")
    A("## 15. Outcome states, channel pairs, and the scope qualifier")
    A("")
    A(MEAS)
    A("")
    A("| Population | Position | Never started | Continued | Started and left | Total |")
    A("| :--- | :--- | ---: | ---: | ---: | ---: |")
    for p in ("APPLY", "DERIV"):
        for posn in ("position5", "position7"):
            s = wj["outcome_states"][p][posn]
            A(f"| {p} | {posn} | {s['never_started']:,} | {s['continued']:,} | "
              f"{s['started_and_left']:,} | "
              f"{s['never_started'] + s['continued'] + s['started_and_left']:,} |")
    A("")
    A("**Never started is a 108-day statement and Continued is a 199-day statement.** The two "
      "published categories are measured over different horizons and must never be described "
      "as measured alike.")
    A("")
    A("**Emitted beyond the required list** (`processed/step8/b/results.json`, "
      "`emitted_beyond_the_required_list`), because Step 9 and Step 10 would otherwise "
      "rebuild them: the liveness exclusions decomposed, the insertion-dormancy channel pairs "
      f"— **{ex['APPLY']['insertion_dormancy_channel_pairs']['started_and_left']} "
      f"started-and-left and "
      f"{ex['APPLY']['insertion_dormancy_channel_pairs']['never_started']} never-started on "
      f"APPLY, {ex['DERIV']['insertion_dormancy_channel_pairs']['started_and_left']} and "
      f"{ex['DERIV']['insertion_dormancy_channel_pairs']['never_started']} on DERIV** — and "
      "the `p = 1.0` residual "
      f"({ex['APPLY']['p_equals_1_residual_post_position_7']:,} on APPLY, "
      f"{ex['DERIV']['p_equals_1_residual_post_position_7']:,} on DERIV, post-position-7).")
    A("")
    A(f"**The scope qualifier travels with anything that carries the Step 9 bound**: "
      f"{ex['scope_qualifier_of_the_Step_9_bound']}.")
    A("")
    A("**The account base.** "
      f"{ex['account_base']['accounts_in_the_sweep']:,} accounts are in the sweep and "
      f"{ex['account_base']['accounts_reaching_the_position_5_population']:,} reach the "
      "position-5 population. Accounts that were skipped, discarded over tolerance or never "
      "attempted are **absent, not empty** — asserted as a data check, not assumed; see "
      "`artifacts/step8-invariants-b.md` §8.")
    A("")
    A("## 16. Discovery channel — every unit, each with its consumer")
    A("")
    A(MEAS)
    A("")
    dc = R["discovery_channel"]
    A("**Two boolean columns, not one categorical** (`0070` ruling 3). **Publish the overlap "
      "in every unit, each with its consumer named** (`0079` §3) — **picking one leaves "
      "another consumer holding a wrong-unit figure.** `0070` ruling 3 said *\"324 users\"* "
      "and named no population, which is the shape that has recurred through this entire "
      "chain, in the ruling written to fix a different unlabelled figure.")
    A("")
    A("| Unit | n | Channel A only | Channel B only | **Both** | Neither | Consumer |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | :--- |")
    rows = [
        ("step3_discovery_pool", "Discovery-pool **usernames**",
         "Step 3's seeding-bias statement; **Step 14 ledger item 1** — the pool's composition"),
        ("accounts_pulled_step4_complete", "**Accounts pulled** (Step 4 `complete`)",
         "**Step 4 coverage reporting**"),
        ("accounts_in_the_APPLY_position5_population",
         "**Accounts** in the position-5 population",
         "**Step 11** — it recomputes the headline within each channel, so it cuts the "
         "analysis population, not the pool"),
        ("PAIRS_in_the_APPLY_position5_population", "**Pairs** in the position-5 population",
         "**Step 11** — the headline is over pairs on the position-5 row set"),
    ]
    for key, lbl, consumer in rows:
        v = dc[key]
        A(f"| {lbl} | {v['n']:,} | {v['channel_A_only']:,} | {v['channel_B_only']:,} | "
          f"**{v['BOTH']:,}** | {v['NEITHER']:,} | {consumer} |")
    A("")
    A("**All four readings reproduce the ruled figures exactly** — 324 of 5,694 usernames, 178 "
      "of 2,549 accounts pulled, and 174 of 2,422 accounts / 17,783 of 196,654 pairs in the "
      "position-5 population (`0078`, `0079` §3). `0079` corrects the mapping as dictated: "
      "**Step 11 takes the position-5 population, and the 5,694 is the pool statistic** — the "
      "reverse of the ruling's first wording, and the files show the reverse. "
      f"{dc['why_two_flags']}.")
    A("")
    pv = dc["pool_file_rows_vs_distinct_slugs"]
    A(f"**One measured detail, so it is not mistaken later for a disagreement about the "
      f"population.** The pool file holds **{pv['rows']:,} rows** and "
      f"**{pv['distinct_slugs_case_insensitive']:,} distinct slugs case-insensitively**: one "
      "account appears as two case variants, one flagged channel B and one flagged both. "
      "**The published population is the row count, 5,694, and the overlap is 324 under both "
      "readings**, so nothing moves — measured rather than assumed inert.")
    A("")
    A("## 17. The column set — 89 enumerated names")
    A("")
    A(MEAS)
    A("")
    cn = R["analysis_table"]["column_set_is_ENUMERATED"]
    A(f"**`0080` §1 enumerates the column set rather than counting it, `0081` extends it to 88 "
      f"and `0082` to {cn['names_ruled']}.** This instance emits **{cn['names_emitted']}**, "
      f"exact-match to the enumerated list: **{cn['exact_match_to_the_enumerated_list']}**, and "
      "in the enumerated order. The full list is in `artifacts/step8-waterfall-b.json` → "
      "`analysis_table.column_names`. **Converged is not specified**, and Step 8b's schema is "
      "built on this vocabulary, so it is fixed before the schema exists.")
    A("")
    A("**Changed from this arm's last confirmed run: nothing.** `0083` does not move the column "
      "set — it restates what `p_at_bound` *means* (§18), which selects the identical rows. "
      "**The two free drops stand** — `f2_in_A_H` is derivable as "
      "`max_episode_in_A_H == s2_F`, and `max_episode_in_A` is read by nothing downstream. The "
      "87-name build is two builds back and is named here so it is not read as current.")
    A("")
    rr = cn["residuals_this_arm_reported_last_run_RE_MEASURED"]
    ra, rb, rs = (rr["a_the_stale_88_inside_the_strike_through"],
                  rr["b_f2_in_A_H_in_0077s_adopted_name_table"],
                  rr["enumeration_checked_AS_A_SET_not_by_counting"])
    A("**The two residuals `0083` §3 fixed — RE-READ OFF DISK, not assumed.** A correction read "
      "back is verified; a correction quoted from the entry that made it is not.")
    A("")
    A("| Residual | `task-sheet.md` | this arm's definition file |")
    A("| :--- | :--- | :--- |")
    A(f"| (a) the strike-through now names the **89**-name enumeration as its replacement | "
      f"**{ra['task_sheet_strike_through_now_says_89']}** | "
      f"**{ra['agent_file_strike_through_now_says_89']}** |")
    A(f"| (b) `f2_in_A_H` is marked **dropped at the point of use** in `0077`'s adopted-name "
      f"table | **{rb['task_sheet_marks_it_dropped_at_the_point_of_use']}** | "
      f"**{rb['agent_file_marks_it_dropped_at_the_point_of_use']}** |")
    A(f"| (b′) `0077`'s **spelling** ruling (`A_H`, not `AH`) survives the column's removal | "
      f"**{rb['the_spelling_ruling_survives_it']}** | "
      f"**{rb['the_spelling_ruling_survives_it']}** |")
    A("")
    A(f"**And the enumeration is checked as a SET, not by counting** — `task-sheet.md` "
      f"{rs['task_sheet_names']} names, this arm's definition file {rs['agent_file_names']}, "
      f"this pipeline {rs['code_names']}; spec == code **{rs['task_sheet_equals_code']}**, "
      f"definition file == code **{rs['agent_file_equals_code']}**, and the two surfaces agree "
      f"with each other **{rs['task_sheet_equals_agent_file']}**. **Matching a count is not "
      "matching a set.**")
    A("")
    # ------------------------------------------------------------------
    # THE TWO SURFACE CLAIMS THIS ARM PUBLISHED LAST RUN, RE-READ.
    # A claim about another file's state is a measurement with an expiry
    # date. Carried as prose it reports a defect that has since been fixed.
    # ------------------------------------------------------------------
    sc = rr["c_surface_claims_this_arm_published_last_run_RE_READ"]
    s4, s5 = (sc["item_4_specs_step8_readback_has_not_launched"],
              sc["item_5_the_assertion_set_count_on_the_spec_surfaces"])
    A("**And the two SURFACE CLAIMS this arm published last run are re-read, not carried.** "
      f"{cap1(sc['why_re_read'])}.")
    A("")
    A("| Claim published on `-r4` | Measured now | Status |")
    A("| :--- | :--- | :--- |")
    A(f"| *\"`specs/step8-readback.md` still says Step 8 has not launched\"* | string occurs "
      f"**{s4['occurrences_of_the_string_now']}**× — "
      f"**{s4['of_those_inside_the_status_stamp_block_quoting_it_to_supersede_it']}** inside the "
      f"status stamp that supersedes it, "
      f"**{s4['of_those_in_the_file_BODY_still_asserting_it']}** in the body; the stamp precedes "
      f"every body occurrence: **{s4['a_status_stamp_now_precedes_and_supersedes_it']}** | "
      f"{s4['status_now']} |")
    _ps = s5["per_surface"]
    A(f"| *\"both spec surfaces still read THE ASSERTION SET NOW HAS EIGHT MEMBERS\"* | "
      f"`task-sheet.md` EIGHT **{_ps['task-sheet.md']['EIGHT']}** / NINE "
      f"**{_ps['task-sheet.md']['NINE']}**; definition file EIGHT "
      f"**{_ps['agent_definition_file']['EIGHT']}** / NINE "
      f"**{_ps['agent_definition_file']['NINE']}**; *\"four pure code checks\"* marked "
      f"SUPERSEDED at the point of use: "
      f"**{s5['task_sheet_four_pure_code_checks_marked_SUPERSEDED_at_the_point_of_use']}** | "
      f"{s5['status_now']} |")
    A("")
    A(f"**Reported per surface, not as a total** — {_ps['reading']}.")
    A("")
    A(f"**Coverage, so a zero is a zero found and not a file unopened** (`CLAUDE.md`): "
      f"`specs/step8-readback.md` **{sc['coverage']['specs/step8-readback.md_bytes_read']:,}** "
      f"bytes, `task-sheet.md` **{sc['coverage']['task-sheet.md_bytes_read']:,}**, this arm's "
      f"definition file **{sc['coverage']['agent_file_bytes_read']:,}**. "
      f"**{cap1(s5['note_on_the_positive_half'])}.**")
    A("")
    A("**`silent_at_tau1` is the column that was worth restoring, and the reason is not "
      "symmetry.** It is **not recoverable from `live` and `outcome` on Continued rows** — "
      "`live` is true for every Continued pair *regardless of silence*, because the rule's "
      "second conjunct is `NOT Continued`. Without it, **the Continued-and-silent count cannot "
      "be recomputed from Step 8's table**; §20 below reports that count as an aggregate as "
      "well, so the figure survives independently of the column.")
    A("")
    A("## 18. `p_at_bound` — it marks WHETHER `p` reached its bound, not WHY")
    A("")
    A(MEAS)
    A("")
    pab = q["p_at_bound"]
    A("**`0083` §2 restates the column and this instance emits the restated form.** "
      "`p_at_bound` is **TRUE where `p` reached its bound**, **null where `p` is null**. "
      "**It does not say why, because on the adopted form there is only one why.**")
    A("")
    A("***SUPERSEDED — `0082` §2's definition by two mechanisms:*** *\"TRUE where the rank "
      "numerator saturated at `L2`, FALSE where the pair left at the final episode.\"* **Those "
      "clauses are coextensive by construction and the FALSE class is empty.** The proof is one "
      "line of the adopted form: `p = |{e ∈ E2 : e ≤ m_H}| / L2`, and the set-membership drop "
      "rule puts `m_H ∈ E2`, so the numerator equals `L2` **iff** no listed episode exceeds "
      "`m_H`, **iff** `m_H = max(E2) = F2` — which *is* \"left at the final episode.\" "
      "**Neither clause can hold without the other.**")
    A("")
    tl = pab["the_chain_has_THREE_links_only_two_are_construction"]
    A("***THE CHAIN HAS THREE LINKS AND ONLY THE FIRST IS CONSTRUCTION*** — `0085` §4, Red "
      "Team P4. `0083` §2 named **two** causes for a future FALSE row; **there are three.**")
    A("")
    A("| Link | Status | Measured |")
    A("| :--- | :--- | :--- |")
    l1, l2 = tl["link_1_numerator_eq_L2_iff_m_H_eq_max_E2"], tl["link_2_max_E2_eq_F2"]
    A(f"| `numerator = L2` ⟺ `m_H = max(E2)` | **CONSTRUCTION**, given `L2 := |E2|`, which the "
      f"spec fixes | shows where `L2 ≠ |E2|`: **{l1['shows_where_L2_differs_from_len_E2']}** |")
    A(f"| `max(E2) = F2` | ***NOT CONSTRUCTION — DATA.*** It needs the finale to be the "
      f"highest-numbered listed episode | shows where `max(E2) ≠ s2_F`: "
      f"**{l2['shows_where_max_E2_differs_from_F2']}**; where `max(E2) ≠ L2`: "
      f"**{l2['shows_where_max_E2_differs_from_L2']}**; `s2_aired_lt_listed`: "
      f"**{l2['s2_aired_lt_listed_shows']}** shows |")
    A("")
    A(f"**Measured, not assumed: {l2['shows_where_max_E2_differs_from_F2']} of "
      f"{l2['shows_examined']:,} frame shows separate the two** — {l2['coverage']}. **Where a "
      "season lists an episode numbered above its finale the two would separate** — that is "
      "the `s2_aired_lt_listed` case this step is told to count, and it is "
      f"**{l2['s2_aired_lt_listed_shows']} shows in frame.** Does it reopen across Step 13's "
      f"`W` grid? {cap1(tl['does_it_reopen_across_Step_13_W_grid'])}.")
    A("")
    A("**The three causes of a future FALSE row:**")
    for i, s in enumerate(tl["three_causes_of_a_future_FALSE_row_not_two"], 1):
        A(f"{i}. {s}")
    A("")
    A("**The `p = 1.0` counts, reported AS TOTALS.**")
    A("")
    A("| Population / position | rows with `p = 1.0` (TOTAL) | `p_at_bound` TRUE | "
      "`p_at_bound` FALSE (`p < 1`) | `p_at_bound` null | rows account for the population |")
    A("| :--- | ---: | ---: | ---: | ---: | :--- |")
    for k, v in pab["totals_by_population_and_position"].items():
        A(f"| {k} | **{v['rows_with_p_equal_1_0_TOTAL']:,}** | {v['p_at_bound_TRUE']:,} | "
          f"{v['rows_with_p_below_1_0_p_at_bound_FALSE']:,} | "
          f"{v['rows_with_p_null_p_at_bound_null']:,} | **{v['coverage_identity']}** |")
    A("")
    A("**The totals reproduce the ruling exactly — 1,246 at position 5 and 1,230 post-liveness "
      "on APPLY.** ***They are NOT a split.*** They are correct counts, but they are **one "
      "class counted twice, not two classes summed**, and **using them as evidence that the "
      "column separates anything is a withdrawn argument** (`CLAUDE.md`, third blindness class; "
      "registered at `src/step7_register.py` → `GROUNDS_WITHDRAWN[\"0083 SS2\"]`). "
      "***Also withdrawn at `0083` §2, and it is a MOTIVE rather than a figure:*** `0082` §2's "
      "claim that the spike carries two viewer-level readings the column must disambiguate. "
      "**On the adopted rank form the spike means one thing.**")
    A("")
    co = pab["coextensivity_check_the_emptiness_is_EMITTED_not_asserted_in_prose"]
    A("**The emptiness is EMITTED, not asserted in prose** — an emptiness asserted in prose and "
      "never emitted cannot be checked. Both mechanisms are computed separately and all four "
      "cells reported, **on BOTH POPULATIONS AT BOTH POSITIONS — four cells each on four "
      "populations** (`0085` §3, Red Team blocker B2). **This is `CLAUDE.md`'s standing "
      "both-populations rule, not a new requirement.** ***One arm emitted APPLY only, and "
      "`1,056` appeared nowhere in its deliverable — while the whole ground for keeping the "
      "column is that an emptiness asserted in prose and never emitted cannot be checked. On "
      "DERIV that ground was unmet.***")
    A("")
    A("| Population / position | rows examined (total) | in BOTH classes | saturated, not "
      "final | final, not saturated | in NEITHER |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for k, v in co["by_population_and_position"].items():
        A(f"| {k} | {v['rows_examined']:,} | **{v['in_BOTH_classes']:,}** | "
          f"{v['saturated_not_final']:,} | {v['final_not_saturated']:,} | "
          f"{v['in_NEITHER']:,} |")
    A("")
    A("**Coverage, per population, because an empty result and a clean result are the same "
      "value and only the control knows which it produced:** "
      + ", ".join(f"{k} {v:,} rows"
                  for k, v in co["coverage"]["rows_examined_per_population"].items())
      + f". Populations examined: **{co['coverage']['populations_examined']}**. Looked "
      f"nowhere: **{co['coverage']['looked_nowhere']}**.")
    A("")
    exp = pab["expected_emptiness_cells_from_the_ruling_BOTH_POPULATIONS"]
    A("**The ruling's stated cells, for comparison against the measured table above:** "
      + ", ".join(f"{k} `{v}`" for k, v in exp.items() if k != "source") + ".")
    A("")
    A("**Which FALSE class is empty, said explicitly, because two different ones are on this "
      "page.** The empty one is `0082`'s **mechanism** class — rows *final but not saturated*, "
      "and its mirror *saturated but not final* — both **0** on every population above. The "
      "`p_at_bound` FALSE in the totals table is a different thing entirely: it is the "
      "**17,895 Started-and-left rows with `p < 1`** on APPLY at position 5, and it is large by "
      "construction. **The mechanism class stays empty through Step 13's `W` grid** — the rank "
      "form and set membership are both `W`-invariant — **so a non-zero cell anywhere means one "
      "of them has broken, and that is worth catching.**")
    A("")
    sf = pab["a_SECOND_fact_DATA_not_construction"]
    A(f"**A second fact, measured and NOT the same argument: "
      f"{sf['shows_with_an_S2_numbering_gap']} of {sf['shows_examined']:,} frame shows have any "
      "S2 numbering gap**, so `E2 = {1…L2}` everywhere and the rank form reduces to "
      "`m_H / L2`. ***That one is DATA and could be false on another frame; the coextensivity "
      "above would still hold.*** It is stated separately because collapsing them would make a "
      "construction argument look like a frame accident.")
    A("")
    A("**The column is KEPT, and the reason changes.** Not because it decomposes the spike — it "
      "does not — but because **Step 10 publishes the abandonment distribution off "
      "`abandonment_point_p` and needs the spike labelled**, and because **an emptiness "
      "asserted in prose and never emitted cannot be checked.**")
    A("")
    A("## 19. `action` — counts by type, never a row-level column")
    A("")
    A(MEAS)
    A("")
    A("`action` is record-level and the row is a pair, so a single value per row would assert "
      "one action per pair, which is false (`0070` ruling 4). The table carries eight count "
      "columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the "
      "four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is fixed by "
      "`0080`'s enumeration**, which names all eight. Step 1 already ruled that check-ins "
      "count as watching alongside `scrobble` and `watch`, because `action` is a property of "
      "the logging client rather than of the viewing, so it is **not an outcome variable**. "
      "Step 13's arm reads the counts: check-in-only iff its `checkin` count is positive and "
      "`scrobble` and `watch` are zero.")
    A("")
    A("## 20. Continued-and-silent — the count `silent_at_tau1` exists to preserve")
    A("")
    A(MEAS)
    A("")
    cs = q["continued_and_silent"]
    A("**Emitted as an aggregate as well as a column**, so the figure survives independently of "
      "either. `live` is TRUE for every Continued pair **regardless of silence**, because the "
      "liveness rule's second conjunct is `NOT Continued` — so this count is what the second "
      "conjunct is worth, and it is **the size of the outcome-conditioning at waterfall line "
      "6**: the pairs the conjunct **saves** from exclusion.")
    A("")
    A("| Population (position 5) | Continued | **Continued and silent at `tau1`** | "
      "silent at `tau1`, all rows | silent and NOT Continued = the exclusions |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for k, v in cs["by_population"].items():
        A(f"| {k} | {v['continued']:,} | **{v['continued_and_silent_at_tau1']:,}** | "
          f"{v['silent_at_tau1_all_rows']:,} | "
          f"{v['silent_and_not_continued_the_liveness_exclusions']:,} |")
    A("")
    md = cs["LINE_6_MARGINAL_DECOMPOSITION"]
    A("### 20a. The line-6 marginal decomposition — **both figures, not one**")
    A("")
    A("***`703` IS NOT THE MARGINAL COST OF THE SILENCE TEST*** (`0085` §5, Red Team third "
      "pass). The silence test **alone** excludes **1,355** on APPLY; the `NOT Continued` "
      "conjunct **spares 652**; `1,355 − 652 = 703`. ***One arm published 652 and not 1,355.*** "
      "**Derivable, so not a defect — but 1,355 is the figure that makes line 6 readable as a "
      "marginal cost**, and a reader holding only 652 cannot recover it without knowing to "
      "add. **Both publish, on both populations, with the identity stated.**")
    A("")
    A("**Identity: `silence test alone − NOT-Continued spares = line-6 exclusions`.**")
    A("")
    A("| Population (position 5) | rows examined | silence test **alone** would exclude | "
      "`NOT Continued` **spares** | **line-6 exclusions** | identity holds |")
    A("| :--- | ---: | ---: | ---: | ---: | :--- |")
    for k, v in md["by_population"].items():
        A(f"| {k} | {v['rows_examined']:,} | **{v['silence_test_alone_would_exclude']:,}** | "
          f"**{v['NOT_Continued_conjunct_spares']:,}** | "
          f"**{v['line_6_exclusions']:,}** | **{v['identity_holds']}** |")
    A("")
    A(f"Coverage: {md['coverage']}.")
    A("")
    A("**This reproduces the published 652 and the published 1,355** — 652 is the figure that "
      "closed the rule objection at `0063` §1 and publishes as a Step 14 limitation; 1,355 is "
      "what makes line 6 legible. **DERIV's Continued-and-silent count is the same 652**, "
      "because every one of those pairs carries S2 evidence by definition of Continued, so "
      "**DERIV's silence-alone figure differs from APPLY's by exactly the never-started "
      "silent pairs DERIV does not carry.**")
    A("")
    A("## 21. Where two faithful instances could still differ — plus what `0083`, `0085` and "
      "`0088` closed, and the one gap `0088` opened")
    A("")
    A(MEAS)
    A("")
    A("**Three kinds of item are in this list and each says which it is.** *(a)* **Genuinely "
      "open** at the spec level — reported, never reconciled here. *(b)* **CLOSED** by "
      "`decisions/0083`, `0085` or `0088`, kept in the list because a previous build published "
      "them as live and **a closure that silently disappears from the report is "
      "indistinguishable from an item that was never raised**; each states what closed it and "
      "what was **re-measured rather than quoted**. *(c)* **NEWLY OPEN** — item 2, the "
      "**tie-break** `0088` §3 left unspecified inside the very ruling that fixed the ranking "
      "basis. **`0085` §7's B3 is no longer carried: `0088` §1 rules it and this arm has "
      "implemented all three parts** (§14a). **Items 1, 2 and 4 are reported, not reconciled**, "
      "which is the standing rule for the dual run.")
    A("")
    for i, s in enumerate(DIV, 1):
        A(f"{i}. {s}")
    A("")
    A("---")
    A("")
    A(GATE)

    # ==================================================================
    # INVARIANTS
    # ==================================================================
    M: list[str] = []
    B = M.append
    B("# Step 8 — invariant report (instance `b`)")
    B("")
    B(GATE)
    B("")
    B(RR)
    B("")
    B(PROV)
    B("")
    B("## How to read this report")
    B("")
    B(f"**{I['how_to_read_this_report']}**")
    B("")
    c = I["counts"]
    B(f"Counts: **{c['pure_code_checks']} pure code checks**, "
      f"**{c['code_check_by_construction_and_data_check_as_specified']} that is a code check "
      "by construction and a genuine cross-check as specified**, and "
      f"**{c['genuine_data_checks']} that can fail on real data** — both added by "
      f"`decisions/0076`, because before it the set had **zero**. "
      f"**{c['items_reported_but_not_asserted']} further items are reported and NOT "
      "asserted**: the set-membership drop rule, which is a coverage count (`0074` ruling 3), "
      "and the 703 expectation, which is a population reconciliation.")
    B("")
    B("**THE SET IS NINE, NOT EIGHT.** "
      f"{c['the_set_moved_from_EIGHT_to_NINE_at_0088']}.")
    B("")
    _s5 = c["the_surface_count_this_arm_reported_last_run_IS_RE_READ_NOT_CARRIED"]
    B("**And the surface count this arm reported last run is RE-READ, not carried.** `-r4` "
      "published that `task-sheet.md` and this instance's definition file *\"still say THE "
      "ASSERTION SET NOW HAS EIGHT MEMBERS\"*. **That was true when written and `0089` §3 acted "
      f"on it.** Re-read off disk on this build: *EIGHT* occurs "
      f"**{_s5['occurrences_of_EIGHT_across_the_two_surfaces']}** times across the two surfaces, "
      f"*NINE* occurs **{_s5['occurrences_of_NINE_across_the_two_surfaces']}**, and "
      "`task-sheet.md`'s *\"four pure code checks\"* sentence is marked SUPERSEDED at the point "
      f"of use: **{_s5['task_sheet_four_pure_code_checks_marked_SUPERSEDED_at_the_point_of_use']}**. "
      f"{cap1(_s5['status_now'])}. **{cap1(_s5['note_on_the_positive_half'])}.**")
    B("")
    B("**What invariant 9 does and does not buy.** `no position-5 row has tau2 > tau_pull` is "
      "true by D10's own definition of position 5, so it is a **code check** and it is not "
      "evidence for anything about the data. What promoting it buys is **visibility**: it ran "
      "before and no reader of this deliverable could see it, which is the same defect as an "
      "unlabelled code check one level up. **And it is not slack** — rows sit with `tau2` "
      "**exactly at** `tau_pull`, so a `>=` form of the same assertion would fail. See "
      "`artifacts/step8-waterfall-b.md` §14a(c).")
    B("")
    cr = I["invariant_coverage_rule"]
    B("## Coverage — every invariant names its population and accounts for every row in it")
    B("")
    B(f"**`0080` §3.** {cap1(cr['why'])}.")
    B("")
    B("**Every invariant below reports `rows_asserted + rows_not_asserted = "
      "rows_in_the_stated_population`, and the identity holds: "
      f"{cr['identity_holds_on_every_invariant']}.**")
    B("")
    B(f"**The gap this arm had, stated plainly rather than quietly fixed.** "
      f"{cap1(cr['the_gap_this_arm_had'])}.")
    B("")
    B("| # | Invariant | Label | Stated population | Coverage | Result |")
    B("| :-- | :--- | :--- | :--- | :--- | :--- |")
    for i, iv in enumerate(I["invariants"], 1):
        cov = iv.get("coverage", {})
        if "identity_arithmetic" in cov:
            cs = f"{cov['identity_arithmetic']} {cov['unit']}"
            if "rows_asserted_in_range_clause" in cov:
                cs += (f" (asserted = {cov['rows_asserted_in_range_clause']:,} in-range + "
                       f"{cov['rows_asserted_null_clause']:,} null)")
        elif "rows_in_the_stated_population" in cov:
            cs = (f"{cov.get('rows_asserted', 0):,} + {cov.get('rows_not_asserted', 0):,}"
                  f" = {cov['rows_in_the_stated_population']:,} {cov['unit']}")
        elif "pairs_in_the_stated_population" in cov:
            cs = (f"{cov['pairs_asserted_S1']:,} pairs × both seasons, "
                  f"{cov['records_examined_by_the_set_membership_rule']:,} records")
        elif "accounts_in_the_stated_population" in cov:
            cs = (f"{cov['accounts_asserted']:,} + {cov['accounts_not_asserted']:,} = "
                  f"{cov['accounts_in_the_stated_population']:,} accounts")
        elif cov.get("unit") == "filter positions":
            cs = "7 positions on each chain, 6 transitions asserted on each"
        elif i == 1:
            cs = "; ".join(f"{k}: {v['rows_asserted']:,} + {v['rows_not_asserted']:,} = "
                           f"{v['rows_in_the_stated_population']:,}"
                           for k, v in iv["result"].items())
        elif i == 7:
            cs = "; ".join(f"{k}: {v['accounts_asserted']:,} + {v['accounts_not_asserted']:,} "
                           f"= {v['accounts_in_the_stated_population']:,} accounts"
                           for k, v in iv["checked"].items())
        elif "per_population" in cov:
            cs = "; ".join(f"{k}: {v['identity_arithmetic']}"
                           for k, v in cov["per_population"].items())
        else:
            cs = "both populations, every row / account — see §" + str(i)
        pop = str(iv.get("population", ""))
        pop = (pop[:78] + "…") if len(pop) > 78 else pop
        B(f"| {i} | {iv['invariant'][:58].replace('|', chr(92) + '|')} | **{iv['label']}** | "
          f"{pop.replace('|', chr(92) + '|')} | {cs} | "
          f"**{'PASS' if iv['passes'] else 'FAIL'}** |")
    B("")
    _lb = I["counts"]
    B(f"**All invariants pass: {I['all_pass']}.** For **{_lb['cannot_fail_on_any_data']} of the "
      f"{_lb['assertions_total']}** — the pure code checks — that statement says only that the "
      "code computed what it was told to. It is **not** evidence for the liveness rule, for "
      "the outcome definition, or for any published share. "
      f"**{_lb['can_fail_on_data_as_specified']} could have failed on data as specified: "
      "§7 and §8, the two DATA CHECKS, and §5, the clock start** — which is a code check by "
      "construction but **recomputes the first-pass S1 completion date INDEPENDENTLY**, and two "
      "implementations can disagree on real records. **What they found is reported in full "
      "below rather than as a tick.** ***Corrected this run (Red Team seventh pass, finding 3): "
      "`-r5` published \"for seven of the nine\" here and, in the invariant report's own head, "
      "\"SEVEN of the nine assertions CANNOT FAIL ON ANY DATA\" followed by a clause calling one "
      "of the seven a genuine cross-check BECAUSE a value is independently recomputed. Those "
      "cannot both hold. Every number in this paragraph is now DERIVED FROM THE `label` FIELD "
      "of the emitted invariants, not typed.***")
    B("")
    au = cr["AUDIT_can_each_identity_actually_fail"]
    B("### Can these identities actually fail? — **audited, because most of them could not**")
    B("")
    B(f"**`0088` §2(d) strikes an overstated sentence** — ~~*\"The run asserts this, so a report "
      "that omitted a population could not be written by this pipeline\"*~~ — **as a control "
      "asserted to exist**, on the ground that **8 of 13 coverage identities had the population "
      "size and the asserted count as the same expression** — *that 8-of-13 is the figure the "
      "ruling cites and is not this arm's own measurement.* **The same shape held here, and "
      "worse: three identities were hardcoded `True` literals, and the aggregate chained "
      "`.get(..., .get(..., .get(..., True)))`, so an invariant carrying no coverage key at all "
      "contributed a pass.**")
    B("")
    B(f"**Rebuilt this run.** Every identity is arithmetic on measured counts, and **the "
      "population size is sourced from a different file than the asserted count** — the "
      "emitted analysis table, the Step 4 ledger, stage 1's own pair count, or the mandated "
      "seven-position order. Result on this build: "
      f"**{au['identities_whose_two_sides_are_independent_expressions']} of "
      f"{cr['invariants_total']} identities have independently sourced sides**, "
      f"**{au['identities_that_are_literals']} are literals**, and "
      f"**{cr['invariants_carrying_a_coverage_identity']} of {cr['invariants_total']} "
      "invariants carry a coverage identity at all** — with no default: "
      f"`{cr['how_the_aggregate_is_computed']}`.")
    B("")
    B("| Population-size source used |")
    B("| :--- |")
    for s in au["population_size_sources_used"]:
        B(f"| {s}… |")
    B("")
    # --------------------------------------------------------------
    # THE NEGATIVE CONTROL, PUBLISHED AS WHAT RAN.
    # --------------------------------------------------------------
    ng = au["THE_FAILURE_IS_EXECUTED_NOT_DESCRIBED"]
    B("### The negative control — **executed, not described**")
    B("")
    B(f"**{cap1(ng['why_this_block_exists'])}.** {cap1(ng['run_through'])}.")
    B("")
    B("| # | Injected defect | Which control | It returned | Caught |")
    B("| ---: | :--- | :--- | :---: | :--- |")
    for i, cse in enumerate(ng["cases"], 1):
        which, got = "`cover_ok`", cse.get("cover_ok_returned")
        if "aggregate_returned" in cse:
            which, got = "the published aggregate expression", cse["aggregate_returned"]
        if "independent_identity_returned" in cse:
            which = "`_independent_identity` (`cover_ok` passes it, by design)"
            got = cse["independent_identity_returned"]
        cau = ("**yes**" if cse["control_caught_it"] else "**NO**") \
            if cse["control_caught_it"] is not None else "n/a — passes by design"
        B(f"| {i} | {cse['case']} | {which} | `{got}` | {cau} |")
    B("")
    B(f"**{ng['cases_run']} cases run; {ng['cases_whose_control_is_checkable']} have a "
      f"checkable control; {ng['cases_caught']} caught; "
      f"{len(ng['cases_NOT_caught'])} not caught.** "
      f"**The run asserts `all_checkable_cases_caught` — {ng['all_checkable_cases_caught']} — "
      "so an injected defect that got through would abort this pipeline before a deliverable "
      f"was written.** {cap1(ng['coverage_note'])}.")
    B("")
    B("**The case that passes by design is named rather than hidden:** "
      f"*{ng['two_cases_PASS_BY_DESIGN_and_are_named'][0]}*. `cover_ok` cannot distinguish a "
      "hardcoded `True` from a computed one at that interface, which is exactly why the separate "
      f"literal counter exists and reads **{au['identities_that_are_literals']}**.")
    B("")
    B("**Why this replaces a sentence.** The previous build published a field named "
      "`what_a_failure_would_look_like` — a description of the failure this apparatus would "
      "catch — and `0089` §1 recorded it as *demonstrating failing*. **It was not demonstrated.** "
      "`CLAUDE.md`: *a control asserted to exist is not a control*, and that file records a "
      "property withdrawn because *the mechanism never fired*, found by reading the code rather "
      "than the claim. **The same reading applied here found the same shape in this arm's own "
      "deliverable.**")
    B("")
    for i, iv in enumerate(I["invariants"], 1):
        B(f"## {i}. {iv['invariant']}")
        B("")
        B(MEAS)
        B("")
        B(f"**Label: {iv['label']}.** "
          f"{iv.get('why_it_cannot_fail_on_data', iv.get('why_it_can_fail', iv.get('what_gives_it_force', '')))}.")
        B("")
        if "population" in iv:
            B(f"**Population (`0080` §3):** {iv['population']}.")
            B("")
        if "label_note" in iv:
            B(f"**On the label:** {iv['label_note']}.")
            B("")
        if "why_ge_not_gt" in iv:
            B(f"**Why `>=` and not `>`:** {iv['why_ge_not_gt']}.")
            B("")
            B(f"- APPLY sequence: {iv['sequence_APPLY']}")
            B(f"- DERIV sequence: {iv['sequence_DERIV']}")
            B(f"- Positions removing exactly zero on APPLY: "
              f"{iv['positions_removing_zero_APPLY']} — **the four inert positions**, labelled "
              "in `artifacts/step8-waterfall-b.md` §1")
            B("")
        for k in ("coverage", "result", "checked", "independent_recomputation",
                  "clauses_on_the_position_5_population",
                  "the_equality_clause_cannot_discriminate_on"):
            if k in iv:
                B(f"**{k.replace('_', ' ')}**")
                B("")
                B("```json")
                B(json.dumps(iv[k], indent=2))
                B("```")
                B("")
        if "form" in iv:
            B(f"Form: `{iv['form']}`.")
            B("")
        if "reading" in iv:
            B(f"**Reading:** {iv['reading']}.")
            B("")
        B(f"**Result: {'PASS' if iv['passes'] else 'FAIL'}.**")
        B("")
    B("## What the two data checks actually found")
    B("")
    B(MEAS)
    B("")
    wh = I["invariants"][6]["checked"]
    B(f"**Wholesale dropping.** On APPLY, **{wh['APPLY']['accounts_holding_BOTH_a_live_and_a_not_live_pair']} "
      f"of the {wh['APPLY']['accounts_supplying_at_least_one_not_live_pair']} accounts that "
      "supply a liveness exclusion also keep at least one live pair**; on DERIV, "
      f"**{wh['DERIV']['accounts_holding_BOTH_a_live_and_a_not_live_pair']} of "
      f"{wh['DERIV']['accounts_supplying_at_least_one_not_live_pair']}**. An account-level "
      "filter would make both numbers exactly zero, so this discriminates between the two "
      "implementations, which the 703-from-216 figure alone does not. The single account whose "
      "pairs are all not-live holds exactly one pair in the population, where the two "
      "implementations are indistinguishable by construction.")
    B("")
    ad = I["invariants"][7]["checked"]
    adc = I["invariants"][7]["coverage"]
    B(f"**Skipped accounts read as empty.** Zero `access_denied` and zero `private_or_absent` "
      "were recorded across the whole Step 4 pull, so the 403-skip path never fired. The "
      "skipped accounts nevertheless exist, and `0080` §3 requires them counted **separately, "
      "in accounts, with the pairs they contribute stated**:")
    B("")
    B("| Final ledger outcome | Accounts | Present in the parsed sweep | Pairs contributed | "
      "of those, never-started |")
    B("| :--- | ---: | ---: | ---: | ---: |")
    for k, v in adc["by_final_ledger_outcome"].items():
        B(f"| `{k}`{' — **skipped class**' if v['is_a_skipped_class'] else ''} | "
          f"{v['accounts_in_the_ledger']:,} | {v['of_those_present_in_the_parsed_sweep']:,} | "
          f"{v['pairs_contributed_to_the_APPLY_position5_population']:,} | "
          f"{v['of_those_pairs_scored_NEVER_STARTED']:,} |")
    B("")
    B(f"**{adc['accounts_asserted']:,} of {adc['accounts_in_the_stated_population']:,} ledger "
      f"accounts asserted, {adc['accounts_not_asserted']:,} not** — and "
      f"{adc['a_second_class_checked_separately']['parsed_accounts_with_no_ledger_row_at_all']} "
      "parsed accounts have no ledger row at all, counted separately so that no account is "
      "covered by no class. **The skipped classes contribute "
      f"{adc['skipped_classes_total_pairs_contributed']} pairs and "
      f"{adc['skipped_classes_total_never_started_pairs_contributed']} never-started pairs.** "
      "They are **absent, not empty**, which is what the rule requires — and this is the one "
      "check that **fails in the direction of the result** if it fails.")
    B("")
    B("## Reported and NOT asserted (1) — the set-membership drop rule")
    B("")
    B(MEAS)
    B("")
    cov = I["coverage_count_not_an_invariant"]
    B(f"{cov['status']}.")
    B("")
    B(f"- Records examined: **{cov['records_examined']:,}**")
    B(f"- Records dropped: **{cov['records_dropped']:,}**")
    B("")
    B("**The denominator is CLOSED** (`0083` §1, amending `0074` ruling 4's routing to Step "
      "14). It has three readings on this data, they are one one-parameter family indexed by "
      "where D11 applies, and **every member drops zero records** — so the numerator is 0 under "
      "all three and the difference survives into no result. All three publish as a **coverage "
      "figure with its pipeline named**, tabulated in `artifacts/step8-waterfall-b.md` §6; this "
      "instance publishes reading B.")
    B("")
    B("## Reported and NOT asserted (2) — the 703 expectation")
    B("")
    B(MEAS)
    B("")
    B(f"{cap1(rec['this_is_NOT_an_invariant'])}.")
    B("")
    B("| Population | Denominator | Expected | Measured | Expected split | Measured split | "
      "Expected accounts | Measured accounts |")
    B("| :--- | ---: | ---: | ---: | :--- | :--- | ---: | ---: |")
    for p in ("APPLY", "DERIV"):
        r = rec[p]
        B(f"| {p} | {r['denominator']:,} | {r['expected']:,} | {r['measured']:,} | "
          f"{r['expected_split']} | {r['measured_split']} | {r['expected_accounts']} | "
          f"{r['measured_accounts']} |")
    B("")
    B(f"**Reconciles: {rec['reconciles']}.** Neither superseded answer was produced — not "
      "**604** (ALT) and not **793** (ALT-MATCHED, withdrawn). Had the count differed, the "
      "spec's own instruction is to treat it as a **population** defect before an "
      "implementation one; the population was in fact re-derived through positions 1–5 and "
      "reproduces 196,654 and 147,370 exactly.")
    B("")

    # ==================================================================
    # PROPAGATION SURFACE 6 -- THIS ARM GREPS ITS OWN DELIVERABLES.
    # Scanned BEFORE the write, on the assembled text of all four files; the
    # section this produces is then appended, and the whole thing is RE-SCANNED
    # OFF DISK below, so the report's own text is covered too.
    # ==================================================================
    PRE = {"artifacts/step8-waterfall-b.md": "\n".join(L),
           "artifacts/step8-waterfall-b.json": json.dumps(wj, indent=2, default=str),
           "artifacts/step8-invariants-b.md": "\n".join(M),
           "artifacts/step8-invariants-b.json": json.dumps(I, indent=2, default=str)}
    POSITIVE_REQUIRED = [
        ("NINE", "the current assertion-set count (0088 Sec 1c)"),
        ("196,654", "APPLY, the position-5 row set"),
        ("147,370", "DERIV"),
        ("220,107", "waterfall line 1 (0068)"),
        ("703", "the position-6 exclusion count on APPLY"),
        ("97.40", "the right-censoring survival share on the position-4 output (0070 r8)"),
        ("99.53", "D3prime at W = 46 on Step 8's right-censored APPLY (0075)"),
        ("97.73", "D3prime at W = 213 on Step 8's right-censored APPLY (0075)"),
        ("89", "the enumerated column count (0080/0081/0082)"),
        ("secondchance", "U1's largest cluster (0088 Sec 3)"),
        ("1,355", "the silence test alone, APPLY (0085 Sec 5)"),
        ("652", "the NOT-Continued conjunct's spare, APPLY (0081, 0085 Sec 5)"),
    ]
    # The two replacements the withdrawn needles point at, ASSERTED HERE so the
    # withdrawal is covered by a live control rather than by a sentence.
    _nf = D9["normalisation_finding"]
    _ill = list(_nf["largest_loose_clusters"].keys())
    _repl = {
        "ruled_illustration_is_U1": {
            "published_illustration_top_two": _ill[:2],
            "expected_under_0088_Sec_3": ["secondchance", "theisland"],
            "universe_named_at_the_point_of_use": "U1" in _nf[
                "THE_UNIVERSE_THIS_LIST_IS_MEASURED_OVER"],
            "ranking_basis_named_at_the_point_of_use": "DISTINCT STRICT KEYS MERGED" in _nf[
                "THE_UNIVERSE_THIS_LIST_IS_MEASURED_OVER"],
            "holds": (_ill[:2] == ["secondchance", "theisland"]
                      and "U1" in _nf["THE_UNIVERSE_THIS_LIST_IS_MEASURED_OVER"]
                      and "DISTINCT STRICT KEYS MERGED" in _nf[
                          "THE_UNIVERSE_THIS_LIST_IS_MEASURED_OVER"]),
        },
        "column_set_is_asserted_on_NAMES_not_on_a_count": {
            "exact_match_to_the_enumerated_list": R["analysis_table"][
                "column_set_is_ENUMERATED"]["exact_match_to_the_enumerated_list"],
            "emitted_in_the_enumerated_order": R["analysis_table"][
                "column_set_is_ENUMERATED"]["emitted_in_the_enumerated_order"],
            "f2_in_A_H_is_absent_from_the_emitted_columns": "f2_in_A_H" not in R[
                "analysis_table"]["column_set_is_ENUMERATED"]["names_emitted_LIST"],
            "holds": (R["analysis_table"]["column_set_is_ENUMERATED"][
                "exact_match_to_the_enumerated_list"]
                and "f2_in_A_H" not in R["analysis_table"][
                    "column_set_is_ENUMERATED"]["names_emitted_LIST"]),
        },
    }
    assert _repl["ruled_illustration_is_U1"]["holds"], (
        "the published D9 illustration is not U1's ranked list, or its universe/basis is "
        "unnamed -- the control that replaces the withdrawn `thetwilightzone` needle")
    assert _repl["column_set_is_asserted_on_NAMES_not_on_a_count"]["holds"], (
        "the emitted column set does not match the 89 enumerated names -- the control that "
        "replaces the withdrawn `f2_in_A_H` needle")

    scan = surface6_scan(PRE)
    scan["THE_CONTROLS_THAT_REPLACE_THE_WITHDRAWN_NEEDLES"] = _repl
    posi = surface6_positive(PRE, POSITIVE_REQUIRED)
    I["surface_6_self_check_artifacts"] = {"negative_half": scan, "positive_half": posi,
                                           "measured_on_build": BUILD}
    B("---")
    B("")
    B("## 16. Propagation surface 6 — **this run greps its own deliverables**")
    B("")
    B(MEAS)
    B("")
    B(f"**{cap1(scan['why_this_exists'])}.**")
    B("")
    B(f"**{cap1(scan['rule'])}.** {cap1(scan['a_hit_is_not_a_defect_until_the_line_is_read'])}.")
    B("")
    _cs = scan["MATCHING_IS_CASE_INSENSITIVE"]
    _rg = scan["THE_REGISTER_IS_THE_ONE_REGISTER"]
    _sn = scan["SENTINEL_TEST_the_matcher_can_see_its_own_needles"]
    B("***THREE CORRECTIONS TO THIS CONTROL THIS RUN — Red Team's eighth pass, F2, all against "
      "this arm.***")
    B("")
    B(f"**(i) THE MATCHING WAS CASE-SENSITIVE AND COULD NOT SEE ITS OWN FOUNDING STRING.** "
      f"{cap1(_cs['CORRECTED_THIS_RUN'])}. **It is now case-insensitive, needles and markers "
      "both**, and the claim is no longer asserted — it is **executed**: every one of the "
      f"**{_sn['needles_tested']}** needles is planted in a line of inverted case and must be "
      f"found. **All findable: {_sn['all_needles_findable']}.** "
      f"**{len(_sn['needles_a_CASE_SENSITIVE_matcher_would_MISS_on_this_test'])} of "
      f"{_sn['needles_tested']} would be MISSED by the `-r6` case-sensitive matcher on that "
      "test.** On the founding line itself — *\"a report where six of EIGHT cannot fail on "
      f"data\"* — this matcher finds **{_sn['THE_FOUNDING_CASE']['case_insensitive_matcher_finds']}** "
      f"and `-r6`'s found **{_sn['THE_FOUNDING_CASE']['the_r6_case_sensitive_matcher_found']}**, "
      "and published that zero as a clean result.")
    B("")
    B(f"**(ii) THERE WERE TWO REGISTERS.** {cap1(_rg['CORRECTED_THIS_RUN'])}. **The needles now "
      f"live in `{_rg['source']}` and this module defines "
      f"{_rg['needles_now_defined_in_this_module']} of its own.** {cap1(_rg['rule'])}.")
    B("")
    B("**(iii) THE ASSERTION FIRED AFTER THE WRITE.** `-r6` wrote all four artifacts to disk "
      "and asserted afterwards — so a failure left the superseded text **on propagation surface "
      "6**, and the check could report the defect but not prevent it. **The gate now runs on "
      "the final assembled bytes IN MEMORY, before any write**, and the bytes on disk are then "
      "verified by hash to be the bytes that passed it. **Read-back plus grep**, with the hash "
      "as the read-back half.")
    B("")
    B("| File | bytes | lines | needles searched | rows emitted | with ≥1 hit | **with ZERO "
      "hits** | **unmarked live** |")
    B("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for p, v in scan["per_file"].items():
        B(f"| `{p}` | {v['bytes_read']:,} | {v['lines_read']:,} | {v['strings_searched']} | "
          f"{v['rows_emitted']} | {v['strings_with_any_occurrence']} | "
          f"{v['strings_with_ZERO_occurrences']} | **{v['unmarked_live_occurrences']}** |")
    B("")
    B(f"**Unmarked live occurrences across all four files: "
      f"{scan['UNMARKED_LIVE_OCCURRENCES_TOTAL']}. Passes: {scan['passes']}.**")
    B("")
    B(f"**This is a CLEAN result, not an EMPTY one.** {cap1(scan['empty_vs_clean'])}.")
    B("")
    B("**Every needle carries a row, including a ZERO row.** `-r6` omitted a needle with no "
      "matches, so *\"the needle found nothing\"* and *\"the needle is not in the table\"* "
      "looked identical — which is `CLAUDE.md`'s empty-against-clean rule at the row level, and "
      "is how a needle that could not match anything showed as an absence rather than a zero. "
      "**Aggregated over the four files; the per-file split is in the JSON half:**")
    B("")
    B("| SUPERSEDED string | what it is | replaced by | marked at the point of use | "
      "**unmarked** |")
    B("| :--- | :--- | :--- | ---: | ---: |")
    _agg = {}
    for p, v in scan["per_file"].items():
        for h in v["hits"]:
            k = h[REGISTER_MARK + "__string"]
            a = _agg.setdefault(k, {"what": h["what_it_is"], "repl": h["replaced_by"],
                                    "m": 0, "u": 0})
            a["m"] += h["marked_as_superseded_at_the_point_of_use"]
            a["u"] += h["UNMARKED_LIVE_OCCURRENCES"]
    for k, a in _agg.items():
        B(f"| SUPERSEDED — `{k}` | {a['what']} | {a['repl']} | {a['m']} | **{a['u']}** |")
    B("")
    B("**Two needles were tried and WITHDRAWN, and withdrawing one disarms the control against "
      "it** (`CLAUDE.md`). Each names the stronger control that covers it, and **both "
      "replacements are asserted in this run and fail it if they break:**")
    B("")
    B("| Withdrawn needle | why it fired | covered instead by | holds |")
    B("| :--- | :--- | :--- | :--- |")
    for nd, v in scan["NEEDLES_TRIED_AND_WITHDRAWN_each_naming_the_stronger_control"].items():
        _h = _repl[v["verified_live_this_run"]]["holds"]
        B(f"| SUPERSEDED — `{nd}` | {v['why_it_fired']} | {v['covered_instead_by']} | "
          f"**{_h}** |")
    B("")
    _nc = scan["NEGATIVE_CONTROL_the_gate_is_EXECUTED_not_asserted"]
    B("**The gate is EXECUTED, not asserted.** `CLAUDE.md`: *a control asserted to exist is not "
      "a control.* `-r6`'s surface check reported clean on a file set containing the very string "
      "it was built for, and nothing in the deliverable distinguished that from a real pass. "
      f"**{_nc['cases_run']} synthetic cases are run through the gate and "
      f"{_nc['cases_behaving_as_required']} behave as required "
      f"({_nc['all_behave_as_required']}):**")
    B("")
    B("| Case | planted | required | unmarked hits | caught | as required | would `-r6` have "
      "caught it |")
    B("| :--- | :--- | :--- | ---: | :---: | :---: | :---: |")
    for nm, v in _nc["cases"].items():
        _pl = {"A_unmarked_superseded_string_lower_case": "an unmarked needle, lower case",
               "B_unmarked_superseded_string_MIXED_case_the_r6_blind_spot":
                   "the same needle in MIXED case — the `-r6` blind spot",
               "C_the_SAME_string_named_as_superseded_at_the_point_of_use":
                   "the same string struck and named superseded at the point of use",
               "D_a_clean_line": "a clean line"}[nm]
        B(f"| `{nm}` | {_pl} | {v['expected']} | {v['unmarked_hits']} | "
          f"{v['caught']} | **{v['behaves_as_required']}** | "
          f"{v['case_sensitive_r6_matcher_would_have_caught']} |")
    B("")
    B(f"**{cap1(_nc['THE_R6_BLIND_SPOT_case_B'])}.**")
    B("")
    B("**And one control a substring needle cannot express.** The `747,478` defect Red Team's "
      "eighth pass F1 found is an **attribution** — *\"it is a season-coverage ROW count\"* — "
      "which survives rewording, markdown emphasis inside the sentence, and reordering. **A "
      "needle for one phrasing sits at zero forever while the claim returns in another.** So "
      "the rule is line-local:")
    B("")
    B("| Control | rule | lines examined | conforming | **failing** | passes |")
    B("| :--- | :--- | ---: | ---: | ---: | :--- |")
    for nm, v in scan[
            "LINE_LOCAL_CONTROLS_where_a_substring_needle_cannot_express_the_defect"].items():
        B(f"| `{nm}` | {v['rule']} | {v['lines_examined']} | {v['lines_conforming']} | "
          f"**{len(v['LINES_FAILING'])}** | **{v['passes']}** |")
    B("")
    B("**Coverage is printed and a control that examined nothing FAILS.** "
      + " ".join(cap1(v["coverage_is_printed"]) + "." for v in scan[
          "LINE_LOCAL_CONTROLS_where_a_substring_needle_cannot_express_the_defect"].values()))
    B("")
    B(f"**And a numeric-boundary rule, which this control found on itself.** "
      f"{cap1(scan['the_numeric_boundary_rule'])}.")
    B("")
    B(f"**How the register avoids exempting itself.** "
      f"{cap1(scan['how_the_register_avoids_failing_its_own_check'])}.")
    B("")
    B(f"**The positive half.** {cap1(posi['rule'])}. **All present: "
      f"{posi['all_present']}.**")
    B("")
    B("| Corrected string | occurrences | why it must be present |")
    B("| :--- | ---: | :--- |")
    for needle, v in posi["checks"].items():
        B(f"| `{needle}` | {v['occurrences_across_the_emitted_artifacts']:,} | {v['why']} |")
    B("")
    B("**What this check does NOT do.** It is a *string* control. It cannot see a **withdrawn "
      "argument built from correct statistics** — `CLAUDE.md`'s third blindness class — and it "
      "does not walk numeric leaves inside JSON at a tolerance, which is `src/check_surfaces.py`'s "
      "job across all eight surfaces. **It closes exactly one hole: this arm's own deliverables "
      "were never opened by this arm's own surface check.**")
    B("")
    B("---")
    B("")
    B(GATE)

    # ==================================================================
    # THE GATE RUNS BEFORE THE WRITE. Red Team eighth pass, F2.
    #
    # The -r6 build wrote all four artifacts to disk FIRST and asserted
    # afterwards. artifacts/ is propagation SURFACE 6, so a failing assertion
    # left the superseded text ON THE SURFACE and stopped the process after the
    # damage -- the check could report the defect but could not prevent it,
    # which is the opposite of what a gate is for. And a partially-failed run
    # leaves four signed-looking deliverables behind with nothing marking them.
    #
    # So: the FINAL bytes are assembled in memory, scanned there, asserted
    # there, and only then written. Afterwards the bytes on disk are compared
    # to the gated bytes by hash -- read-back plus grep (CLAUDE.md), where the
    # hash is the read-back half and the scan above is the grep half.
    FINAL = {
        "artifacts/step8-waterfall-b.md": "\n".join(L) + "\n",
        "artifacts/step8-waterfall-b.json": json.dumps(wj, indent=2, default=str),
        "artifacts/step8-invariants-b.md": "\n".join(M) + "\n",
        "artifacts/step8-invariants-b.json": json.dumps(I, indent=2, default=str),
    }
    gate = surface6_scan(FINAL)
    print(f"  surface 6 GATE, on the final bytes BEFORE the write: "
          f"{sum(v['bytes_read'] for v in gate['per_file'].values()):,} bytes, "
          f"{gate['UNMARKED_LIVE_OCCURRENCES_TOTAL']} unmarked live occurrences, "
          f"sentinel all-findable="
          f"{gate['SENTINEL_TEST_the_matcher_can_see_its_own_needles']['all_needles_findable']}")
    for p, v in gate["per_file"].items():
        if v["unmarked_live_occurrences"]:
            for h in v["hits"]:
                if h["UNMARKED_LIVE_OCCURRENCES"]:
                    print(f"    {p}: {h[REGISTER_MARK + '__string']!r} unmarked at lines "
                          f"{h['unmarked_line_numbers']}")
    assert gate["SENTINEL_TEST_the_matcher_can_see_its_own_needles"]["all_needles_findable"], (
        "the surface-6 matcher cannot find one of its own needles in a planted line -- the "
        "control looked nowhere and would have reported clean")
    assert gate["passes"], (
        "a superseded string is live and unqualified in this arm's artifacts -- propagation "
        "surface 6. NOTHING HAS BEEN WRITTEN: the gate runs on the final bytes before the write")
    gpos = surface6_positive(FINAL, POSITIVE_REQUIRED)
    assert gpos["all_present"], (
        "a corrected string is ABSENT from the artifacts about to be written -- the negative "
        "grep passes clean on a file that never said the right thing (CLAUDE.md). NOTHING HAS "
        "BEEN WRITTEN")

    for rel, txt in FINAL.items():
        (ART / rel.split("/")[-1]).write_text(txt)

    # READ-BACK: the bytes on disk are the bytes that passed the gate.
    _bad = [rel for rel, txt in FINAL.items()
            if hashlib.sha256((ART / rel.split("/")[-1]).read_bytes()).hexdigest()
            != hashlib.sha256(txt.encode()).hexdigest()]
    assert not _bad, f"written bytes differ from the gated bytes at {_bad}"
    print(f"  read-back: 4/4 artifacts byte-identical to the text the gate passed")
    print("wrote 4 artifacts")


def divergences(R: dict, D9: dict, S1: dict, I: dict) -> list[str]:
    """Every figure in this list is READ FROM THE MEASURED OBJECTS, not typed.

    CLAUDE.md: derived figures are regenerated, not patched -- "if you find
    yourself editing a derived number by hand, that is the defect."
    """
    at = R["analysis_table"]
    cn = at["column_set_is_ENUMERATED"]
    dn = S1["drop_rule"]["denominator_note"]
    p3 = S1["position3_drop_set"]
    dc = R["discovery_channel"]
    d3 = R["per_arm"]["APPLY"]
    k = D9["keys"]
    last = str(R["W_arms"][-1])
    cl = D9["normalisation_finding"]["clustering_universes"]
    tl = R["required_counts"]["p_at_bound"]["the_chain_has_THREE_links_only_two_are_construction"]
    b3 = R["B3_the_two_unasserted_mandates"]
    tie = cl["universes"]["U1_all_sweep_show_ids_carrying_a_slug"]["THE_TIE_BREAK_IS_NOT_RULED"]
    bwA = b3["a_boundary_window"]["by_population"]["APPLY_position5"]
    chg = b3["b_per_site_D11_table"]["pairs_whose_action_counts_moved"]
    _sc = R["analysis_table"]["column_set_is_ENUMERATED"][
        "residuals_this_arm_reported_last_run_RE_MEASURED"][
        "c_surface_claims_this_arm_published_last_run_RE_READ"]
    sc4 = _sc["item_4_specs_step8_readback_has_not_launched"]
    sc5 = _sc["item_5_the_assertion_set_count_on_the_spec_surfaces"]
    d9b = D9["PUBLICATION_FORM_decisions_0090"]
    neg = I["invariant_coverage_rule"]["AUDIT_can_each_identity_actually_fail"][
        "THE_FAILURE_IS_EXECUTED_NOT_DESCRIBED"]
    return [
        "**`0090` — D9 NOW PUBLISHES AS A BOUND, AND THIS ARM'S PREVIOUS BUILD PUBLISHED A "
        "RULED KEY.** Strict is the **floor**, loose is the **ceiling**, **neither is the point "
        "estimate**, and the interval applies to every D9 quantity that has both forms: "
        f"complementary signature pairs **{d9b['bounds']['complementary_signature_pairs']['BOUND']}**, "
        f"half (a) **{d9b['bounds']['half_a_APPLY_position5']['BOUND']}** on APPLY position 5, "
        f"half (b) **{d9b['bounds']['half_b_present_in_the_position3_drop_set']['BOUND']}**. "
        "**No D9 count moves** — `0090` §4 says so and this build confirms it — **what moves is "
        "which of them is presented as the answer.** `-r4` published *\"ruled key: STRICT, with "
        "the loose count reported alongside\"*; that framing is superseded at the point of use "
        "in §10. **The third key's "
        f"{d9b['THE_THIRD_KEYS_ANSWER_NOT_AN_ENDPOINT']['complementary_signature_pairs']} is not "
        "an endpoint** — it is a different key's answer, reported as a divergence. **The "
        "coverage publishes beside the zero floor** so the bound is distinguishable from a check "
        "that looked nowhere.",

        "**THE NEGATIVE CONTROL IS NOW EXECUTED, NOT DESCRIBED — AND THIS ARM'S OWN CLAIM WAS "
        "THE DEFECT.** `-r4` published a field named `what_a_failure_would_look_like`, a "
        "**sentence** about the failure the rebuilt coverage apparatus would catch, and `0089` "
        "§1 recorded it as *\"demonstrating failing\"*. **It was described, not demonstrated** — "
        "`CLAUDE.md`: *a control asserted to exist is not a control*, a rule that file records "
        "as having been broken by a mechanism that *\"never fired\"*. **Replaced by "
        f"{neg['cases_run']} injected defects run through the SAME `cover()`, `cover_ok()` and "
        "`_independent_identity()` the published invariants go through, and through the SAME "
        f"aggregate expression: {neg['cases_caught']} of {neg['cases_whose_control_is_checkable']} "
        "checkable cases caught, and the run asserts it — an injected defect that got through "
        "would abort before a deliverable was written.** **One case passes by design and is "
        f"named rather than hidden: {neg['two_cases_PASS_BY_DESIGN_and_are_named'][0]}**, which "
        "`cover_ok` cannot distinguish from a computed `True` and which the separate "
        "literal-counter catches instead.",
        "**THE D9 CLUSTERING UNIVERSE IS NOW RULED — U1 — AND THIS ARM CHANGED TO IT.** "
        "`0088` §3 closes what `0085` §2 opened and `0086` §1 located. This arm published **U3** "
        "on its previous build and now publishes "
        f"**`{cl['PUBLISHED_UNIVERSE']}`**, ranked on the ruled basis, **distinct strict keys "
        "merged**. **No count moves with it** — D9's search already ran on the whole sweep here, "
        "so strict is **0** and loose is **75** either way; what moves is **which clusters are "
        "illustrated**, which is the evidence for the loose key's only warrant. All three "
        "candidate universes are still measured side by side (§10a) so an arm on another one is "
        "diffable without a rerun, and **the units differ between them** — U1 and U2 count "
        "distinct show IDs per key, U3 counts complementary signature rows.",

        "**BUT THE TIE-BREAK IS NOT RULED, AND THE TIE IS OCCUPIED. REPORTED, NOT RECONCILED.** "
        "`0088` §3 names the U1 top three as `secondchance` (8), `theisland` (7), `maigret` (6). "
        "**The first two are unique at their counts and reproduce exactly on this build.** The "
        f"third sits inside a **{tie['keys_tied_at_the_third_place_count']}-way tie at "
        f"{tie['third_place_count']}** — "
        + ", ".join(f"`{x}`" for x in tie["tied_keys"]) +
        f" — so the third name is decided by a rule **no surface states**. Under this arm's "
        f"tie-break ({tie['this_arms_tie_break']}) it is **`{tie['this_arms_third_name']}`**; "
        "`maigret` is equally correct under another. **This is a spec gap inside the ruling "
        "that closed the previous spec gap, and it is reported rather than resolved by picking "
        "the name that matches the entry.**",

        "**B3(a) WAS MEASURED ON THE WRONG SET LAST RUN, AND CORRECTING IT REVERSES THIS ARM'S "
        "OWN VERDICT.** `0089` §2(a) corrects `0088` §1(a): `T0` is day-floored, so `τ1` and "
        "`τ2` are midnight-aligned and `[τ − 24h, τ)` is the interval on which the half-open and "
        "date-level forms **agree**. **The separating interval is `[τ, τ + 24h)`, and this arm's "
        "`-r4` deliverable did not emit it** — it published the ruled window and the single "
        "instant at `τ1`, then read `OCCUPIED_INERT` and *\"no outcome state differs\"* off "
        f"**1 row of {bwA['WHAT_THE_FORM_DECIDES']['rows_with_an_S2_episode_in_the_SEPARATING_interval_at_tau1']}**. "
        "**Measured on the right set (§14a): the verdict is "
        f"`{bwA['VERDICT_STATE']}`.** On APPLY the separating interval holds "
        f"**{bwA['DISTINCT_EPISODES_the_form_the_outcome_assignment_reads']['SEPARATING_in_[tau1, tau1_plus_24h)']:,}** "
        "distinct S2 episodes at `τ1` and "
        f"**{bwA['DISTINCT_EPISODES_the_form_the_outcome_assignment_reads']['SEPARATING_in_[tau2, tau2_plus_24h)']:,}** "
        "at `τ2`, and **the forbidden form moves "
        f"{b3['a_boundary_window']['THE_FOUR_NUMBERS_THAT_SETTLE_B3']['APPLY_position5_both_bounds_relaxed']} "
        "APPLY rows and "
        f"{b3['a_boundary_window']['THE_FOUR_NUMBERS_THAT_SETTLE_B3']['DERIV_position5_both_bounds_relaxed']} "
        "DERIV rows into a different outcome state.** **The mandate is load-bearing on the "
        "RESULT, not merely on `|A|`.** **No published figure of this build moves** — the "
        "forbidden form is computed as a counterfactual and nowhere else — **but the previous "
        "verdict is withdrawn, not amended.**",

        "**B3(b) AND B3(c) STAND FROM THE PREVIOUS RUN AND ARE RE-EXECUTED.** "
        "**(b) The per-site table exposed a real gap in this arm's own previous build**: the "
        "S1-side D11 carry-through — which has a ruling behind it **only** for the completion "
        "walk, because `0068` publishes line 1 at 220,107 — was also reaching the four "
        "`action_count_s1_*` columns, where nothing exempts it. **D11 is applied there now.** "
        f"**{chg['in_the_record_universe']} pairs move in the record universe, "
        f"{chg['of_those_present_in_the_APPLY_position5_row_set']} of them in the APPLY "
        "position-5 row set**, and **no waterfall line, outcome share or invariant moves with "
        "them**. **(c) The `tau2 <= tau_pull` assertion is promoted into the published set as "
        "invariant 9** — and **it is not slack**: rows sit with `tau2` exactly at `τ_pull`.",

        "**THE TWO SURFACE CLAIMS THIS ARM PUBLISHED LAST RUN ARE BOTH NO LONGER TRUE, AND THEY "
        "ARE RE-READ RATHER THAN CARRIED.** A claim about the state of another file is a "
        "**measurement with an expiry date**; republished as prose it reports a defect that has "
        "since been fixed, which is the stale-figure problem one level up. Both were re-read off "
        f"disk on this build. **(4) `specs/step8-readback.md`** — the string *\"has not "
        f"launched\"* occurs **{sc4['occurrences_of_the_string_now']}** time(s), "
        f"**{sc4['of_those_inside_the_status_stamp_block_quoting_it_to_supersede_it']}** of them "
        f"inside the status stamp that supersedes it and "
        f"**{sc4['of_those_in_the_file_BODY_still_asserting_it']}** in the body, and the **stamp "
        f"precedes every body occurrence: "
        f"{sc4['a_status_stamp_now_precedes_and_supersedes_it']}** (`0089` §3, negative only — "
        "the body sentence is deliberately unedited). "
        f"{cap1(sc4['status_now'])}. **(5) The assertion-set count** "
        f"— *\"ASSERTION SET NOW HAS EIGHT\"* occurs "
        f"**{sc5['occurrences_of_EIGHT_across_the_two_surfaces']}** times across `task-sheet.md` "
        f"and this arm's definition file, *\"NINE\"* occurs "
        f"**{sc5['occurrences_of_NINE_across_the_two_surfaces']}**, and `task-sheet.md`'s "
        f"*\"four pure code checks\"* sentence is now **marked SUPERSEDED at the point of use: "
        f"{sc5['task_sheet_four_pure_code_checks_marked_SUPERSEDED_at_the_point_of_use']}**. "
        f"{cap1(sc5['status_now'])}. **Both halves are measured** — "
        f"{sc5['note_on_the_positive_half']} — and the bytes read are reported, so a zero here "
        "is a zero found and not a file unopened. **What remains open on item 4 is not the "
        "string but whether `specs/` becomes a NINTH propagation surface**, carried for the "
        "Human Lead at `0089` §4.",

        "**THE COEXTENSIVITY CHAIN HAS THREE LINKS, NOT TWO — and the third is DATA.** "
        "`0085` §4 (Red Team P4): `numerator = L2 ⟺ m_H = max(E2)` is construction given "
        "`L2 := |E2|`, but **`max(E2) = F2` is not** — it needs the finale to be the "
        "highest-numbered listed episode, and the `s2_aired_lt_listed` case separates them. "
        "**Measured here, not assumed: "
        f"{tl['link_2_max_E2_eq_F2']['shows_where_max_E2_differs_from_F2']} of "
        f"{tl['link_2_max_E2_eq_F2']['shows_examined']:,} frame shows separate them**, and "
        f"`s2_aired_lt_listed` is "
        f"{tl['link_2_max_E2_eq_F2']['s2_aired_lt_listed_shows']} shows. ***`0083` §2 named "
        "TWO causes for a future FALSE row; there are THREE.*** No value moves; listed "
        "because the previous build's proof asserted a data premise as construction.",
    ] + [
        f"**THE TWO RESIDUALS THIS ARM AND INSTANCE A REPORTED ARE CLOSED, AND THE CLOSURE WAS "
        f"RE-READ RATHER THAN QUOTED.** `0083` §3 fixed the stale `88` inside the strike-through "
        f"and `f2_in_A_H`'s survival in `0077`'s adopted-name table. Both were re-read off disk "
        f"on this build (§17): the strike-through names the "
        f"{cn['names_ruled']}-name enumeration on both surfaces this instance reads, "
        f"`f2_in_A_H` is marked dropped at the point of use on both, `0077`'s **spelling** "
        f"ruling survives the column's removal, and the three name sets are identical **as "
        f"sets**. **Nothing here is open; it is listed because a closure that is quoted and not "
        f"re-read is the shape this chain keeps failing on.**",

        "**`p_at_bound` IS RULED, AND THE RULING REMOVED THE CHOICE THIS ITEM USED TO NAME.** "
        "`0083` §2 restates the column as marking **WHETHER** `p` reached its bound, not WHY, "
        "and withdraws `0082` §2's two-mechanism definition — the clauses are coextensive by "
        "construction, so the mechanism form never defined a column. **Both mechanisms are "
        "still computed separately here and all four cells emitted** (§18), because the "
        "emptiness is only checkable if it is emitted. **The two `p = 1.0` totals are reported "
        "as TOTALS, not as a split** — reading them as a split is a registered withdrawn "
        "argument. No value moves and no choice remains; listed so the *previous* framing is "
        "not read as still live.",

        "**D11 and waterfall line 1.** `0068` rules "
        f"{S1['s1_completion']['S1_completer_pairs_line_1']:,} and leaves the D11 question "
        "open. Lines 1–3 are that figure here and would be "
        f"{S1['s1_completion']['D11_open_question']['S1_completer_pairs_if_D11_applied_to_S1_too']:,}"
        " under the other reading; lines 4–7 are identical either way, verified row by row.",

        "**The set-membership denominator — CLOSED, and this arm publishes reading B.** `0083` "
        "§1 amends `0074` ruling 4: the difference was never a divergence, the three readings "
        "are one one-parameter family indexed by where D11 applies, and **every member drops "
        "zero records**, so it survives into no result and is not a Step 14 limitation. This "
        f"instance produces **{dn['READING_B_D11_on_the_S2_side_only_THIS_INSTANCE']:,}** — D11 "
        "on the S2 side, the S1 side carried because `0068` rules line 1 at 220,107 as "
        f"published; the others are {dn['READING_A_no_D11_anywhere']:,} (D11 nowhere) and "
        f"{dn['READING_C_D11_on_both_seasons']:,} (D11 on both). The decomposition is "
        f"{dn['decomposition_of_the_full_D11_effect']['records_D11_discards_on_the_S1_side']} "
        "S1-side + "
        f"{dn['decomposition_of_the_full_D11_effect']['records_D11_discards_on_the_S2_side']} "
        f"S2-side = {dn['decomposition_of_the_full_D11_effect']['total']}, so `0074`'s 94 is "
        "the S2-side component alone. **What remains open is `0068`'s own item** — whether D11 "
        "applies to the S1 completion walk — **and it is answered there, not here.** Listed "
        "because all three readings publish with their pipelines named, so no arm's figure is "
        "later read as a divergence.",

        "**D3′'s cleared shares are not monotone between `W = 91` and `W = 107`** — "
        f"{d3['91']['D3prime']['cleared_share_of_started_and_left_pct']:.2f}% then "
        f"{d3['107']['D3prime']['cleared_share_of_started_and_left_pct']:.2f}% on APPLY. An "
        "open item at `0076` §5, reproduced rather than smoothed.",

        "**D8's position.** Pre- or post-liveness is unstated. Both are reported.",

        "**D2's population.** Unstated at the point of use. Four are reported and each "
        "labelled.",

        "**D9's third key.** The spec now defines strict and loose (`0076` §3). On this data "
        "the third key — a trailing digit group of arbitrary length — gives "
        f"**{k['THIRD_KEY_NOT_USED']['complementary_signature_pairs']}** complementary "
        f"signature pairs against loose's **{k['LOOSE']['complementary_signature_pairs']}**, "
        "reproducing the divergence `0076` describes. It is measured and not used.",

        "**The grain of D9 half (b).** `0078` §3 requires both halves under both keys, which "
        "is done; but the unit of half (b) is not fixed. This instance reports **B-side pairs "
        "on frame shows**, then how many of them sit inside the position-3 drop set, which is "
        "the only reading on which the drop set is load-bearing.",

        "**The provenance string itself.** `0078` and `0079` §2 require every count to name "
        "the build it was measured on, and fix no format. This instance emits one build "
        "identifier plus an input fingerprint (size and mtime of every input) and a SHA-256 of "
        "its own pipeline sources. **A different arm will phrase the label differently and no "
        "figure moves**; what matters is that both arms label everything rather than two "
        "figures.",

        "**The shape of the position-3 drop set — ruled, and it agrees.** `0075` ruling 2 "
        "named an empty set; `0077` §2 restates it as the pair universe less the completers, "
        f"{p3['dropped_by_the_S1_completion_rule']:,} pairs, with distinct-episode counts and "
        "the show's threshold. This instance reported the same count on the previous build, so "
        "the restatement removes the choice without moving a figure.",

        "**The discovery-channel overlap, now published in every unit.** `0079` §3 names three "
        f"and this instance measures four numbers: {dc['step3_discovery_pool']['BOTH']} of "
        f"{dc['step3_discovery_pool']['n']:,} pool usernames, "
        f"{dc['accounts_pulled_step4_complete']['BOTH']} of "
        f"{dc['accounts_pulled_step4_complete']['n']:,} accounts pulled, "
        f"{dc['accounts_in_the_APPLY_position5_population']['BOTH']} of "
        f"{dc['accounts_in_the_APPLY_position5_population']['n']:,} accounts and "
        f"{dc['PAIRS_in_the_APPLY_position5_population']['BOTH']:,} of "
        f"{dc['PAIRS_in_the_APPLY_position5_population']['n']:,} pairs in the position-5 "
        "population. All four reproduce the ruled figures.",

        "**The waterfall's unit.** Pairs are primary; users and shows are reported alongside "
        "because position 2 is explicitly a filter on shows.",

        f"**Undated records.** {S1['D11']['records_with_no_watched_at']} records in the sweep "
        "carry no `watched_at`. None is an in-frame S1/S2 episode record, so they touch no "
        "outcome. They are **not** discarded by D11, which removes `watched_at >= tau_pull`; a "
        "reading that requires a record to be positively \"dated before `tau_pull`\" would "
        "drop them from the liveness evidence. Measured inert: the exclusion counts are "
        "identical either way at every arm.",

        "**DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three "
        "restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore "
        "not the adopted contamination exclusion, and is labelled as such rather than silently "
        "conflated with APPLY's.",

        f"**At `W = {last}` the DERIV started-and-left exclusion component is "
        f"{R['per_arm']['DERIV'][last]['liveness_excluded_started_and_left']} while APPLY's is "
        f"{R['per_arm']['APPLY'][last]['liveness_excluded_started_and_left']}.** No published "
        "figure covers DERIV per arm above `W = 108`, so this is new rather than divergent, "
        "and it is stated so it is not read as an error later.",
    ]


if __name__ == "__main__":
    main()
