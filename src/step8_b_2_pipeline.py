"""Step 8 (instance b) -- stage 2: the seven filter positions, both populations,
the analysis table, every required count, and the invariant battery.

GATE. NOTHING IS ADOPTED HERE. Step 8 is a gate: this instance produces its
deliverables and stops. It does not adopt its own proposal and it records no
approval.

READ ONLY on inputs. ZERO network calls.

THE MANDATED FILTER ORDER (decisions/0029; task-sheet.md Step 8). The final row
set commutes but the per-filter sample size does not, so the order is exact:

  1 Step 2 frame -> 2 L2 = 1 exclusion -> 3 S1 completion rule ->
  4 contamination exclusion (Step 5) -> 5 right-censoring -> 6 liveness ->
  7 outcome assignment, at TWO INSTANTS (decisions/0034).

Waterfall line 1 is the S1-completer population, 220,107 pairs (decisions/0068);
no instance chooses a base.

POPULATIONS -- every figure states one (standing rule, 0047):
  APPLY = line 1 less D10           = 196,654 at W = 108. Position-5 output.
  DERIV = Step 5 line 4 less D10    = 147,370 at W = 108. Requires S2 evidence.
Step 8 produces BOTH (0070 ruling 1).

THE LIVENESS RULE (ALT-BROAD; 0048, restored 0054, APPROVED 0064). A pair is
NOT LIVE iff BOTH: the account shows no insertion instant after that pair's
tau1, AND the pair is NOT Continued. "After" is STRICT -- silent iff no instant
> tau1 (0068). The evidence is restricted to records dated before tau_pull
(0070 ruling 2). The stored play-id calibration is READ, NEVER REFITTED (0029).

Out: processed/step8/b/{analysis_table.csv.gz, results.json, ...}
"""
from __future__ import annotations

import gzip
import json
import math
import re
import time
from pathlib import Path

import numpy as np
import pandas as pd

from step8_b_build_id import BUILD, provenance_block, stamp

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P2, P5 = ROOT / "processed" / "step2", ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step8" / "b"

# decisions/0080 Sec 1 -- THE COLUMN SET IS ENUMERATED, NOT COUNTED. Extended to
# 88 by 0081 (silent_at_tau1 restored) and to 89 by 0082 (p_at_bound added).
# 89 names, exactly these, no more and no fewer. Transcribed from task-sheet.md
# Step 8 as it now stands.
COLUMNS_89 = [
    "abandonment_point_p", "action_count_s1_checkin", "action_count_s1_other",
    "action_count_s1_scrobble", "action_count_s1_watch", "action_count_s2_checkin",
    "action_count_s2_other", "action_count_s2_scrobble", "action_count_s2_watch",
    "air_period", "cadence_boundary_distance_days", "cadence_bucket",
    "completers_per_year", "discovered_channel_a", "discovered_channel_b",
    "e1_internal_gap", "e1_starts_at_1", "e2_internal_gap", "e2_starts_at_1",
    "exclusion", "gap_days", "has_s3_or_later_evidence", "in_apply", "in_deriv",
    "live", "max_episode_in_A_H", "max_season_number", "n_A", "n_A_H", "outcome",
    "p_at_bound", "pool_completers", "pool_completers_proxy", "s1_E", "s1_F", "s1_L",
    "s1_aired_episodes_reported", "s1_aired_lt_listed", "s1_completion_date",
    "s1_completion_used_a_post_cutoff_record", "s1_count_disagreement",
    "s1_episode_count_reported", "s1_exposure_years", "s1_finale_date",
    "s1_premiere_date", "s1_season_first_aired", "s1_total_runtime", "s2_E", "s2_F",
    "s2_L", "s2_aired_episodes_reported", "s2_aired_lt_listed", "s2_count_disagreement",
    "s2_episode_count_reported", "s2_finale_date", "s2_finale_year", "s2_premiere_date",
    "s2_season_first_aired", "s2_span_days", "s2_total_runtime", "s2_weekly_span_days",
    "season_numbers", "seasons_returned", "show_aired_episodes", "show_airs_day",
    "show_certification", "show_comment_count", "show_country", "show_first_aired",
    "show_genres", "show_language", "show_languages", "show_rating", "show_runtime",
    "show_status", "show_subgenres", "show_trakt_id", "show_votes", "show_year",
    "silent_at_tau1", "size_quintile", "size_quintile_per_year", "size_quintile_raw_count",
    "t0_binding_term", "t0_date", "tau1", "tau2", "title", "user_idx",
]
assert len(COLUMNS_89) == 89 and len(set(COLUMNS_89)) == 89

TAU_PULL = 1786406400          # 2026-08-11T00:00:00Z, decisions/0011
DAY = 86400
W = 108                        # decisions/0026
H = 91                         # D10
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
BACKFILL_D, POSTDATE_D = 180.0, -30.0
STEP5_WATERFALL = [201_900, 178_165, 155_131, 152_126, 128_099]

R: dict = {}


def _surface_claims(ts: str, ag: str) -> dict:
    """RE-READ, off disk, the two claims about OTHER FILES' STATE this arm
    published on its previous build. Both were true when written and decisions/0089
    Sec 3 acted on both. A claim about a surface is a measurement with an expiry
    date; carried as prose it reports a defect that no longer exists.

    COVERAGE IS PRINTED. A path that can return "nothing found" must say whether it
    found nothing or looked at nothing (CLAUDE.md), so every probe below reports
    the bytes it read.
    """
    spec_p = ROOT / "specs" / "step8-readback.md"
    spec_txt = spec_p.read_text() if spec_p.exists() else ""
    # The string, and whether a STATUS STAMP now qualifies it. An unqualified
    # occurrence and a stamped one are DIFFERENT FINDINGS, so the occurrences are
    # split by whether they sit INSIDE the stamp block (where the stamp is
    # quoting the string in order to supersede it) or in the file body.
    # The stamp block is the leading markdown blockquote; it is located rather
    # than assumed, and its absence is reported as an absence.
    lines = spec_txt.split("\n")
    q = [i for i, l in enumerate(lines) if l.startswith(">")]
    stamp_lo, stamp_hi = (min(q), max(q)) if q else (-1, -1)
    stamp_txt = "\n".join(lines[stamp_lo:stamp_hi + 1]) if q else ""
    body_txt = "\n".join(lines[:max(stamp_lo, 0)] + lines[stamp_hi + 1:]) if q else spec_txt
    occ = spec_txt.lower().count("has not launched")
    occ_in_stamp = stamp_txt.lower().count("has not launched")
    occ_in_body = body_txt.lower().count("has not launched")
    body_occ_lines = [i for i, l in enumerate(lines)
                      if "has not launched" in l.lower() and not l.startswith(">")]
    stamped = bool(q and "STATUS STAMP" in stamp_txt and "SUPERSEDED" in stamp_txt
                   and all(i > stamp_hi for i in body_occ_lines))
    eight = ts.count("ASSERTION SET NOW HAS EIGHT") + ag.count("ASSERTION SET NOW HAS EIGHT")
    nine = ts.count("ASSERTION SET NOW HAS NINE") + ag.count("ASSERTION SET NOW HAS NINE")
    fourpure = ts.count("four pure code checks")
    # a struck occurrence is not a live one: the task-sheet marks it SUPERSEDED
    # at the point of use, which the spec's own rules permit.
    fourpure_struck = ts.count("SUPERSEDED — \"The count is four pure code checks")
    return {
        "why_re_read": ("these are claims about the STATE OF OTHER FILES. They were true when "
                        "this arm published them on 2026-08-16-r4 and decisions/0089 Sec 3 acted "
                        "on both. Re-read live here; a surface claim carried as prose is a "
                        "measurement with an expiry date"),
        "coverage": {"specs/step8-readback.md_bytes_read": len(spec_txt),
                     "task-sheet.md_bytes_read": len(ts),
                     "agent_file_bytes_read": len(ag),
                     "note": ("a zero occurrence count below means the string was looked for and "
                              "not found, on a file whose byte count is stated -- not that "
                              "nothing was looked at")},
        "item_4_specs_step8_readback_has_not_launched": {
            "r4_claim": ("`specs/step8-readback.md` STILL SAYS STEP 8 'HAS NOT LAUNCHED', ON "
                         "THIS READ -- reported, not edited, because specs/ is not one of the "
                         "eight propagation surfaces"),
            "file_exists": bool(spec_p.exists()),
            "occurrences_of_the_string_now": occ,
            "of_those_inside_the_status_stamp_block_quoting_it_to_supersede_it": occ_in_stamp,
            "of_those_in_the_file_BODY_still_asserting_it": occ_in_body,
            "a_status_stamp_now_precedes_and_supersedes_it": stamped,
            "why_the_split": ("an occurrence inside a stamp that supersedes the string and an "
                              "unqualified occurrence in the body are DIFFERENT FINDINGS. The "
                              "r4 claim counted neither -- it said the string was live. It is "
                              "live in the body AND stamped at the head, and 0089 Sec 3's stamp "
                              "is negative only, so the body sentence is deliberately not edited"),
            "status_now": ("CLOSED AS A DEFECT, STANDING AS A QUESTION. decisions/0089 Sec 3 "
                           "stamped the file, and the stamp precedes every body occurrence and "
                           "marks the string SUPERSEDED. The r4 claim -- that the string sits "
                           "there unqualified -- is NO LONGER TRUE and is not republished. The "
                           "body sentence itself is deliberately unedited, because the stamp is "
                           "NEGATIVE ONLY. What remains open is not the string but whether "
                           "specs/ becomes a NINTH propagation surface, which 0089 Sec 4 "
                           "carries for the Human Lead"
                           if stamped else
                           "STILL LIVE AND UNSTAMPED -- republished"),
        },
        "item_5_the_assertion_set_count_on_the_spec_surfaces": {
            "r4_claim": ("task-sheet.md and this instance's definition file still read 'THE "
                         "ASSERTION SET NOW HAS EIGHT MEMBERS', and task-sheet.md's labelling "
                         "bullet carries a third count, 'four pure code checks'"),
            "occurrences_of_EIGHT_across_the_two_surfaces": eight,
            "occurrences_of_NINE_across_the_two_surfaces": nine,
            "per_surface": {
                "task-sheet.md": {"EIGHT": ts.count("ASSERTION SET NOW HAS EIGHT"),
                                  "NINE": ts.count("ASSERTION SET NOW HAS NINE")},
                "agent_definition_file": {"EIGHT": ag.count("ASSERTION SET NOW HAS EIGHT"),
                                          "NINE": ag.count("ASSERTION SET NOW HAS NINE")},
                "reading": ("task-sheet.md now states NO count of the assertion set in this "
                            "phrasing, and the definition file states NINE. NO SURFACE "
                            "CONTRADICTS ANOTHER, which is what the r4 claim said they did. "
                            "Reported per surface rather than as a total, because a total of "
                            "zero EIGHTs is also what two silent files would give"),
            },
            "task_sheet_four_pure_code_checks_occurrences": fourpure,
            "task_sheet_four_pure_code_checks_marked_SUPERSEDED_at_the_point_of_use":
                bool(fourpure_struck),
            "status_now": ("CLOSED. decisions/0089 Sec 3 acted on both halves and struck the "
                           "'four pure code checks' sentence at the point of use. NO SURFACE "
                           "NOW STATES EIGHT. The r4 claim is NO LONGER TRUE and is not "
                           "republished. This arm publishes NINE and no surface contradicts it"
                           if eight == 0 and nine > 0 and (fourpure == 0 or fourpure_struck)
                           else "STILL LIVE -- republished"),
            "note_on_the_positive_half": ("the negative grep for 'EIGHT MEMBERS' passes clean on "
                                          "a file that never said nine. Both halves are measured "
                                          "here: EIGHT must be 0 AND NINE must be non-zero"),
        },
    }


def _spec_residuals() -> dict:
    """decisions/0083 Sec 3 fixed two residuals INSTANCE A reported and could not
    edit. This arm reported the first of them on its own previous build. They are
    RE-MEASURED here against the live spec surfaces rather than assumed fixed --
    a correction quoted from a ruling and not re-read is the shape this chain
    keeps failing on.

    Read-only on the two surfaces an isolated Step 8 instance actually reads:
    task-sheet.md and its own definition file. It does not read the other arm's.
    """
    ts = (ROOT / "task-sheet.md").read_text()
    ag = (ROOT / ".claude" / "agents" / "analytics-engineer-b.md").read_text()
    i = ts.index("THE COLUMN SET IS ENUMERATED, NOT COUNTED")
    j = ts.index("THE TABLE IS THE POSITION-5 ROW SET", i)
    seg_ts = ts[i:j]
    k = ag.index("THE COLUMN SET IS ENUMERATED")
    l = ag.index("POSITION 3's DROP SET IS THE 58,345", k)
    seg_ag = ag[k:l]

    def enumerated(seg: str) -> list[str]:
        a = seg.index("`abandonment_point_p`")
        b = seg.index("`user_idx`") + len("`user_idx`")
        return sorted(set(re.findall(r"`([A-Za-z0-9_]+)`", seg[a:b])))

    ts_names, ag_names = enumerated(seg_ts), enumerated(seg_ag)
    return {
        "why_re_measured": ("decisions/0083 Sec 3 records both as corrected on all three "
                            "surfaces. A correction READ BACK is verified; a correction QUOTED "
                            "is not. Both are re-read here, off disk, on this build"),
        "a_the_stale_88_inside_the_strike_through": {
            "reported_by": ("instance A, artifacts/step8-waterfall-a.md Sec 8; this arm "
                            "reported the same shape on its previous build"),
            "was": ("the strike-through withdrawing 0077's '89 columns' said it was replaced "
                    "by the '88-name ENUMERATION', while the enumeration directly above it "
                    "carries 89 names"),
            "task_sheet_strike_through_now_says_89":
                bool("89-NAME ENUMERATION" in seg_ts),
            "agent_file_strike_through_now_says_89":
                bool("89-NAME ENUMERATION" in seg_ag),
            "status": ("CLOSED at decisions/0083 Sec 3a -- verified live on both surfaces this "
                       "instance reads, not quoted from the entry"),
        },
        "b_f2_in_A_H_in_0077s_adopted_name_table": {
            "was": ("the adopted-name table lists f2_in_A_H among the ADOPTED names while a "
                    "bullet in the same section drops it as derivable"),
            "task_sheet_marks_it_dropped_at_the_point_of_use":
                bool("f2_in_A_H` IS NOT AN EMITTED" in seg_ts),
            "agent_file_marks_it_dropped_at_the_point_of_use":
                bool("f2_in_A_H` IS NOT AN EMITTED" in seg_ag),
            "the_spelling_ruling_survives_it":
                bool("`AH` is not the spec's spelling" in seg_ts
                     or "the spec writes `A_H`, not `AH`" in seg_ag),
            "status": ("CLOSED at decisions/0083 Sec 3b -- marked at the point of use rather "
                       "than deleted, so 0077's SPELLING ruling (A_H not AH, which governs n_A, "
                       "n_A_H and max_episode_in_A_H) is not lost with the column"),
        },
        # ---------------------------------------------------------------
        # THE SURFACE CLAIMS THIS ARM PUBLISHED LAST RUN ARE RE-READ, NOT
        # CARRIED. Items 4 and 5 of the r4 divergence list were TYPED
        # assertions about the state of other files -- "specs/step8-readback.md
        # STILL SAYS ... ON THIS READ" and "task-sheet.md and this instance's
        # definition file still read EIGHT MEMBERS". decisions/0089 Sec 3 fixed
        # both. A claim about another file's state is a MEASUREMENT with an
        # expiry date, and a deliverable that carries it as prose reports a
        # defect that no longer exists. Measured live here so the divergence
        # list states the current reading rather than the previous one.
        # ---------------------------------------------------------------
        "c_surface_claims_this_arm_published_last_run_RE_READ": _surface_claims(ts, ag),
        "enumeration_checked_AS_A_SET_not_by_counting": {
            "task_sheet_names": len(ts_names),
            "agent_file_names": len(ag_names),
            "code_names": len(COLUMNS_89),
            "task_sheet_equals_code": sorted(ts_names) == sorted(COLUMNS_89),
            "agent_file_equals_code": sorted(ag_names) == sorted(COLUMNS_89),
            "task_sheet_equals_agent_file": sorted(ts_names) == sorted(ag_names),
            "why": ("decisions/0083 Sec 3 verifies the three surfaces' name sets as SETS, off "
                    "disk, not by counting. Matching a count is not matching a set"),
        },
    }


def insert_time(rid, knot_rid, knot_time):
    """Verbatim from src/step5_calibrate.py. The curve is READ, never refitted."""
    return np.interp(rid.astype(np.float64), knot_rid, knot_time)


# ---------------------------------------------------------------------------
def main() -> None:
    t = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    R.update({
        "instance": "analytics-engineer-b", "namespace": "b",
        "step": 8, "mode": "GATE -- proposal only, nothing adopted",
        "api_calls": 0,
        "W_adopted": W, "H": H, "W_arms": W_ARMS,
        "tau_pull": "2026-08-11T00:00:00Z",
        "filter_order": ["1 Step 2 frame", "2 L2 = 1 exclusion", "3 S1 completion rule",
                         "4 contamination exclusion (Step 5)", "5 right-censoring",
                         "6 liveness", "7 outcome assignment (two instants)"],
        "boundary_convention": ("half-open UTC instants throughout (Step 1 Sec 2.4, D13); "
                                "date(watched_at) <= T1 appears nowhere"),
    })

    b = np.load(OUT / "base.npz")
    n_shows = int(b["n_shows"])
    show_ids = b["show_ids"]
    L2a, F2a, THR2a = b["L2"], b["F2"], b["THR2"]
    frame = pd.read_csv(P2 / "frame.csv").sort_values("show_trakt_id").reset_index(drop=True)
    assert (frame.show_trakt_id.values == show_ids).all()

    comp_pair = b["comp_pair"]
    t0_mid = b["t0_mid"].astype(np.int64)
    binds = b["binds"]
    comp_date_mid = b["comp_date_mid"].astype(np.int64)
    comp_post_cutoff = b["comp_uses_post_cutoff"]
    u_idx = comp_pair // n_shows
    s_idx = comp_pair % n_shows
    n1 = len(comp_pair)

    # =====================================================================
    # POSITIONS 1-3
    # =====================================================================
    wf: list[dict] = []
    line1 = np.ones(n1, dtype=bool)
    wf.append({"position": 1, "filter": "Step 2 frame",
               "retained_pairs": int(line1.sum()), "removed_pairs": 0,
               "retained_users": int(len(np.unique(u_idx))),
               "retained_shows": int(len(np.unique(s_idx))),
               "INERT": True,
               "inert_reason": ("line 1 is ALREADY the frame. This position CANNOT FIRE; it is "
                                "not evidence that the frame found nothing (decisions/0079 "
                                "Sec 4). Kept because removing a position removes the check "
                                "that would catch a future upstream change"),
               "note": ("line 1 is the S1-completer population, ruled at 220,107 by "
                        "decisions/0068; no instance chooses a base")})
    assert int(line1.sum()) == 220_107, int(line1.sum())

    l2_eq_1 = L2a[s_idx] == 1
    line2 = line1 & ~l2_eq_1
    wf.append({"position": 2, "filter": "L2 = 1 exclusion",
               "retained_pairs": int(line2.sum()),
               "removed_pairs": int((line1 & l2_eq_1).sum()),
               "removed_shows": int((L2a == 1).sum()),
               "shows_examined": n_shows,
               "retained_users": int(len(np.unique(u_idx[line2]))),
               "retained_shows": int(len(np.unique(s_idx[line2]))),
               "INERT": True,
               "inert_reason": ("line 1 is already the L2 > 1 S1-completer population "
                                "(decisions/0068), AND 0 of the 1,138 frame shows have "
                                "L2 = 1. This position CANNOT FIRE. An unlabelled always-zero "
                                "filter reads as evidence THE RULE FOUND NOTHING when it is "
                                "evidence THE RULE CANNOT FIRE (decisions/0079 Sec 4)"),
               "coverage_note": ("0 of 1,138 frame shows have L2 = 1: this line is a "
                                 "measured zero on a examined population, not an empty check")})

    line3 = line2.copy()   # line 1 is already the S1-completer set (0068)
    wf.append({"position": 3, "filter": "S1 completion rule",
               "retained_pairs": int(line3.sum()),
               "removed_pairs": int((line2 & ~line3).sum()),
               "retained_users": int(len(np.unique(u_idx[line3]))),
               "retained_shows": int(len(np.unique(s_idx[line3]))),
               "INERT": True,
               "inert_reason": ("THE POSITION IS INERT; THE RULE IS NOT. Line 1 is already the "
                                "S1-completer population (decisions/0068), so the position "
                                "CANNOT FIRE -- but the S1 completion rule removes 58,345 "
                                "pairs UPSTREAM of line 1, which is the study's largest single "
                                "exclusion and is why its drop set is a deliverable "
                                "(decisions/0079 Sec 1 and Sec 4). Reading this 0 as 'the rule "
                                "found nothing' is exactly the misreading the label exists to "
                                "prevent"),
               "the_rules_drop_set_upstream_of_line_1": {
                   "pairs": 58345,
                   "file": "processed/step8/b/position3_drop_set.csv.gz",
                   "provenance_of_the_ruled_figure": ("58,345 pairs -- position-3 rule, "
                                                      "position-5 build of 2026-08-13 "
                                                      "(decisions/0078); reproduced on this "
                                                      "build"),
               },
               "note": ("removes 0 by construction: decisions/0068 defines line 1 as the "
                        "S1-completer population, so the rule has already bound at line 1. "
                        "The rule was nevertheless computed independently at stage 1 "
                        "(F1 in D1 and |D1| >= ceil(0.90 x L1), first-pass) and it is that "
                        "computation which produced line 1")})

    # =====================================================================
    # POSITION 4 -- the Step 5 contamination exclusion (approved gate 0021)
    # =====================================================================
    p5 = pd.read_csv(P5 / "pair_revision5.csv")
    key_mine = pd.DataFrame({"user_idx": u_idx, "show_trakt_id": show_ids[s_idx],
                             "_row": np.arange(n1)})
    p5m = p5.merge(key_mine, on=["user_idx", "show_trakt_id"], how="left", validate="1:1")
    assert p5m._row.notna().all(), "a Step 5 pair is absent from this instance's line 1"
    assert len(p5m) == n1
    ordr = p5m._row.values.astype(np.int64)
    inv = np.empty(n1, dtype=np.int64)
    inv[ordr] = np.arange(n1)

    has_s2_ev = (p5.s2_ev_n.values > 0)[inv]
    t0c = p5.t0_contaminated.values.astype(bool)[inv]
    postd = (p5.complete_rec_lag_days.values < POSTDATE_D)[inv]
    all_air = has_s2_ev & (p5.s2_ev_airdate.values == p5.s2_ev_n.values)[inv]
    fs2_bad = has_s2_ev & ((p5.first_s2_lag_days.values > BACKFILL_D)
                           | (p5.first_s2_airdate.values == 1)
                           | (p5.first_s2_corrupt.values == 1))[inv]

    contam_excl = all_air | (t0c & ~has_s2_ev)
    line4 = line3 & ~contam_excl
    # Step 5's own waterfall, re-asserted line by line before it is used
    s5 = [line4]
    for m in (has_s2_ev, ~t0c, ~postd, ~fs2_bad):
        s5.append(s5[-1] & m)
    s5_counts = [int(x.sum()) for x in s5]
    assert s5_counts == STEP5_WATERFALL, (s5_counts, STEP5_WATERFALL)
    # processed/ is the EIGHTH propagation surface (0074 ruling 6). adopted_rule.json
    # was corrected there; it is now READ and CROSS-CHECKED rather than worked around.
    ar = json.loads((P5 / "adopted_rule.json").read_text())
    ar6 = ar["_SUPERSEDED_FIGURES_CORRECTED_2026_08_13"]["approved_rule_revision_6"]
    R["step5_waterfall_reasserted"] = {
        "measured": s5_counts, "expected": STEP5_WATERFALL,
        "adopted_rule_json_cross_check": {
            "surface": ("processed/ is the eighth propagation surface (0074 ruling 6); "
                        "processed/step5/adopted_rule.json carried revision-3 figures and was "
                        "corrected. It is READ here and cross-checked, not worked around"),
            "file_says_removed": ar6["removed"], "file_says_retained": ar6["retained"],
            "file_says_of_total": ar6["of_total"],
            "measured_removed": int((line3 & contam_excl).sum()),
            "measured_retained": int(line4.sum()),
            "measured_of_total": int(line3.sum()),
            "components_file": ar6["components"],
            "components_measured": {
                "s2_evidence_entirely_air_date_stamped": int((line3 & all_air).sum()),
                "no_s2_evidence_fabricated_binding_clock_start":
                    int((line3 & t0c & ~has_s2_ev).sum())},
            "agrees": (ar6["removed"] == int((line3 & contam_excl).sum())
                       and ar6["retained"] == int(line4.sum())
                       and ar6["of_total"] == int(line3.sum())),
            "the_file_still_carries_the_superseded_block":
                "FINAL.pair_level_reading = 4,849 removed / 215,258 retained, LABELLED superseded",
        }}
    line4_step5 = s5[3]          # Step 5 line 4 -- the DERIV base before D10

    wf.append({"position": 4, "filter": "contamination exclusion (Step 5, decisions/0021)",
               "INERT": False,
               "retained_pairs": int(line4.sum()),
               "removed_pairs": int((line3 & contam_excl).sum()),
               "removed_all_S2_evidence_air_date_stamped": int((line3 & all_air).sum()),
               "removed_contaminated_T0_with_no_S2_evidence":
                   int((line3 & t0c & ~has_s2_ev).sum()),
               "retained_users": int(len(np.unique(u_idx[line4]))),
               "retained_shows": int(len(np.unique(s_idx[line4]))),
               "note": ("the ADOPTED rule is two disjoint exclusions; it is not the Step 5 "
                        "estimation-sample waterfall down to 128,099")})

    # =====================================================================
    # S2 EVIDENCE -- |A|, |A_H|, F2 in A_H, max(A_H), at any instant
    # =====================================================================
    s2_pairs, s2_start, s2_counts = b["s2_pairs"], b["s2_start"], b["s2_counts"]
    s2_ts, s2_num, s2_runmax, f2_ts = b["s2_ts"], b["s2_num"], b["s2_runmax"], b["f2_ts"]
    pos_of = np.full(n_shows * (u_idx.max() + 1) + n_shows, -1, dtype=np.int64)
    # map pair_code -> index into s2_pairs, via searchsorted (s2_pairs is sorted)
    loc = np.searchsorted(s2_pairs, comp_pair)
    loc_ok = (loc < len(s2_pairs)) & (s2_pairs[np.clip(loc, 0, len(s2_pairs) - 1)] == comp_pair)
    del pos_of
    start = np.where(loc_ok, s2_start[np.clip(loc, 0, len(s2_pairs) - 1)], 0)
    cnt = np.where(loc_ok, s2_counts[np.clip(loc, 0, len(s2_pairs) - 1)], 0)
    f2ts = np.where(loc_ok, f2_ts[np.clip(loc, 0, len(s2_pairs) - 1)],
                    np.iinfo(np.int64).max)

    TS_MIN = int(s2_ts.min()) - 1
    SPAN = int(s2_ts.max()) - TS_MIN + 10 ** 9
    pair_rank = np.searchsorted(s2_pairs, s2_pairs)  # identity, kept for clarity
    combined = (np.repeat(np.arange(len(s2_pairs), dtype=np.int64), s2_counts) * SPAN
                + (s2_ts - TS_MIN))
    del pair_rank

    def n_before(tau: np.ndarray) -> np.ndarray:
        """|{distinct in-E2 S2 episodes with canonical watched_at < tau}| per pair."""
        assert (tau - TS_MIN < SPAN).all() and (tau >= TS_MIN).all()
        q = np.where(loc_ok, loc * SPAN + (tau - TS_MIN), -1)
        idx = np.searchsorted(combined, q, side="left")
        return np.where(loc_ok, idx - start, 0)

    def maxnum_before(k: np.ndarray) -> np.ndarray:
        """max episode number among the first k episodes in instant order."""
        return np.where(k > 0, s2_runmax[np.clip(start + k - 1, 0, len(s2_runmax) - 1)], -1)

    # rank table for p: |{e in E2 : e <= m}| / L2
    maxE = int(max(F2a.max(), 1)) + 1
    rank_tab = np.zeros((n_shows, maxE + 1), dtype=np.int64)
    for i in range(n_shows):
        e = np.array(sorted({int(x) for x in str(frame.s2_E.iloc[i]).split(",")
                             if x.strip().isdigit()}))
        rank_tab[i, :] = np.searchsorted(e, np.arange(maxE + 1), side="right")

    # =====================================================================
    # LIVENESS INPUT -- per-account maximum insertion instant
    # =====================================================================
    cal = np.load(P5 / "calibration.npz")
    knot_rid, knot_time = cal["knot_rid"], cal["knot_time"]
    z = np.load(P5 / "full_scan.npz")
    r_user, r_rid, r_ts = z["user"], z["rid"], z["ts"]
    inst = insert_time(r_rid, knot_rid, knot_time)
    n_users = int(r_user.max()) + 1
    max_inst_unrestricted = np.full(n_users, -np.inf)
    np.maximum.at(max_inst_unrestricted, r_user, inst)
    keep11 = r_ts < TAU_PULL
    max_inst = np.full(n_users, -np.inf)
    np.maximum.at(max_inst, r_user[keep11], inst[keep11])
    R["liveness_inputs"] = {
        "calibration": {"source": "processed/step5/calibration.npz",
                        "status": "READ, NEVER REFITTED (decisions/0029)",
                        "n_knots": int(len(knot_rid)),
                        "application": "np.interp(rid, knot_rid, knot_time)",
                        "records_clamped_below_first_knot": int((r_rid < knot_rid[0]).sum()),
                        "records_clamped_above_last_knot": int((r_rid > knot_rid[-1]).sum())},
        "evidence_scope": ("account-wide -- the whole sweep, other shows and movies "
                           "included -- RESTRICTED to records with watched_at < tau_pull "
                           "(decisions/0070 ruling 2, D11 applied consistently)"),
        "records_used": int(keep11.sum()),
        "records_excluded_by_the_tau_pull_restriction": int((~keep11).sum()),
        "accounts": n_users,
        "max_insertion_instant_utc": str(np.datetime64(int(np.nanmax(max_inst)), "s")),
        "max_insertion_instant_unrestricted_utc":
            str(np.datetime64(int(np.nanmax(max_inst_unrestricted)), "s")),
    }
    del inst, r_rid, keep11
    mx = max_inst[u_idx]
    mx_unres = max_inst_unrestricted[u_idx]

    # =====================================================================
    # POSITIONS 5, 6, 7 -- per W arm, on both populations
    # =====================================================================
    per_arm: dict = {"APPLY": {}, "DERIV": {}}
    air_period = frame.air_period.values[s_idx]
    censor_air: dict = {}
    keep_main = None

    for Wa in W_ARMS:
        tau1 = t0_mid + Wa * DAY
        tau2 = t0_mid + (Wa + H) * DAY
        tau3 = t0_mid + (Wa + 2 * H) * DAY
        term1 = t0_mid + max(Wa, 91) * DAY <= TAU_PULL
        d10 = t0_mid + (max(Wa, 91) + H) * DAY <= TAU_PULL
        assert (d10 <= term1).all()

        nA = n_before(tau1)
        nAH = n_before(tau2)
        nA3 = n_before(tau3)
        f2_in_AH = f2ts < tau2
        f2_in_A3 = f2ts < tau3
        started = nA >= 1
        contd = started & f2_in_AH & (nAH >= THR2a[s_idx])
        sal = started & ~contd
        never = ~started
        notlive = (mx <= tau1) & ~contd
        notlive_unres = (mx_unres <= tau1) & ~contd

        line5 = line4 & d10
        line6 = line5 & ~notlive
        deriv5 = line4_step5 & d10
        deriv6 = deriv5 & ~notlive

        # per-air-period retention after right-censoring, on the POSITION-4 output
        ap = {}
        for name in ["pre-2020", "2020-2022", "2023-2025"]:
            m = line4 & (air_period == name)
            ap[name] = {"position4_pairs": int(m.sum()),
                        "retained_after_censoring": int((m & d10).sum()),
                        "retained_pct": 100.0 * float((m & d10).sum()) / max(int(m.sum()), 1)}
        ap["ALL"] = {"position4_pairs": int(line4.sum()),
                     "retained_after_censoring": int(line5.sum()),
                     "retained_pct": 100.0 * int(line5.sum()) / int(line4.sum())}
        censor_air[str(Wa)] = ap

        for pop, p5mask, p6mask in (("APPLY", line5, line6), ("DERIV", deriv5, deriv6)):
            n = int(p5mask.sum())
            ex = int((p5mask & notlive).sum())
            ex_ns = int((p5mask & notlive & never).sum())
            ex_sl = int((p5mask & notlive & sal).sum())
            ex_c = int((p5mask & notlive & contd).sum())
            assert ex_c == 0
            ns_t, c_t, sl_t = (int((p5mask & never).sum()), int((p5mask & contd).sum()),
                               int((p5mask & sal).sum()))
            assert ns_t + c_t + sl_t == n
            # D3' cleared subpopulation, at this arm on this population
            cleared = p6mask & sal & (tau3 <= TAU_PULL)
            completes = cleared & f2_in_A3 & (nA3 >= THR2a[s_idx])
            sal_live = int((p6mask & sal).sum())
            per_arm[pop][str(Wa)] = {
                "W": Wa, "population": pop,
                "position5_n": n,
                "position6_n": int(p6mask.sum()),
                "liveness_excluded": ex,
                "liveness_excluded_never_started": ex_ns,
                "liveness_excluded_started_and_left": ex_sl,
                "liveness_excluded_continued": ex_c,
                "accounts_supplying_exclusions":
                    int(len(np.unique(u_idx[p5mask & notlive]))) if ex else 0,
                "liveness_excluded_under_unrestricted_evidence":
                    int((p5mask & notlive_unres).sum()),
                "states_at_position5": {"never_started": ns_t, "continued": c_t,
                                        "started_and_left": sl_t},
                "states_at_position7": {
                    "never_started": int((p6mask & never).sum()),
                    "continued": int((p6mask & contd).sum()),
                    "started_and_left": int((p6mask & sal).sum())},
                "D3prime": {
                    "definition": ("of pairs Started-and-left at tau2 whose "
                                   "[T0] + (W + 2H) x 24h <= tau_pull, the share completing "
                                   "within [tau2, tau2 + H)"),
                    "started_and_left_at_this_arm_on_this_population": sal_live,
                    "cleared_count": int(cleared.sum()),
                    "cleared_share_of_started_and_left_pct":
                        100.0 * int(cleared.sum()) / max(sal_live, 1),
                    "completing_within_the_horizon": int(completes.sum()),
                    "share_completing_pct":
                        100.0 * int(completes.sum()) / max(int(cleared.sum()), 1),
                    "denominator_note": ("both denominators are this arm's and this "
                                         "population's own (decisions/0069 item 5)")},
            }
        if Wa == W:
            keep_main = dict(nA=nA, nAH=nAH, contd=contd, sal=sal, never=never,
                             notlive=notlive, line5=line5, line6=line6,
                             deriv5=deriv5, deriv6=deriv6, tau1=tau1, tau2=tau2,
                             f2_in_AH=f2_in_AH, term1=term1, d10=d10,
                             silent=(mx <= tau1))

    R["per_arm"] = per_arm
    R["censoring_per_air_period"] = censor_air

    # ---- waterfall lines 5, 6, 7 at the adopted W --------------------------
    K = keep_main
    line5, line6 = K["line5"], K["line6"]
    wf.append({"position": 5, "filter": "right-censoring",
               "INERT": False,
               "retained_pairs": int(line5.sum()),
               "removed_pairs": int((line4 & ~line5).sum()),
               "removed_by_max_W_91_term": int((line4 & ~K["term1"]).sum()),
               "removed_incrementally_by_the_plus_H_term":
                   int((line4 & K["term1"] & ~K["d10"]).sum()),
               "direction_on_the_headline": ("BOTH removals move the never-started share "
                                             "UP: they remove recent S1 completers, who are "
                                             "disproportionately likely to roll straight on"),
               "retained_users": int(len(np.unique(u_idx[line5]))),
               "retained_shows": int(len(np.unique(s_idx[line5])))})
    wf.append({"position": 6, "filter": "liveness (ALT-BROAD, approved 0064)",
               "INERT": False,
               "retained_pairs": int(line6.sum()),
               "removed_pairs": int((line5 & ~line6).sum()),
               "outcome_conditional": True,
               "outcome_conditional_note": ("conjunct 2 IS the Continued test, read at tau2, "
                                            "so this line is outcome-conditional and is "
                                            "reported as such (0046). Permitted: |A| and "
                                            "liveness are row-local predicates on the "
                                            "position-5 output and commute exactly, and "
                                            "position 7 removes no rows"),
               "retained_users": int(len(np.unique(u_idx[line6]))),
               "retained_shows": int(len(np.unique(s_idx[line6])))})
    wf.append({"position": 7, "filter": "outcome assignment (two instants)",
               "retained_pairs": int(line6.sum()), "removed_pairs": 0,
               "INERT": True,
               "inert_reason": ("outcome assignment ANNOTATES AND REMOVES NOTHING (0046), so "
                                "this position cannot fire. Labelled per decisions/0079 Sec 4; "
                                "it is also what permits position 6 to be outcome-conditional, "
                                "since a filter that removes no rows cannot make per-filter "
                                "sample sizes depend on the ordering"),
               "note": "an annotation, not a filter: it removes no rows",
               "retained_users": int(len(np.unique(u_idx[line6]))),
               "retained_shows": int(len(np.unique(s_idx[line6])))})
    R["waterfall_APPLY"] = wf

    # ---- the DERIV waterfall ------------------------------------------------
    d5, d6 = K["deriv5"], K["deriv6"]
    R["waterfall_DERIV"] = [
        dict(wf[0]), dict(wf[1]), dict(wf[2]),
        {"position": 4, "filter": ("contamination exclusion, taken to Step 5 LINE 4 -- the "
                                   "adopted exclusion plus the three line-4 restrictions "
                                   "(has_s2, T0 not contaminated, completing record not "
                                   "post-dated) that define the DERIV base"),
         "retained_pairs": int(line4_step5.sum()), "INERT": False,
         "removed_pairs": int((line3 & ~line4_step5).sum()),
         "step5_line_by_line": STEP5_WATERFALL[:4]},
        {"position": 5, "filter": "right-censoring", "retained_pairs": int(d5.sum()),
         "INERT": False, "removed_pairs": int((line4_step5 & ~d5).sum())},
        {"position": 6, "filter": "liveness", "retained_pairs": int(d6.sum()), "INERT": False,
         "removed_pairs": int((d5 & ~d6).sum()), "outcome_conditional": True},
        {"position": 7, "filter": "outcome assignment", "retained_pairs": int(d6.sum()),
         "removed_pairs": 0, "INERT": True,
         "inert_reason": "outcome assignment annotates and removes nothing (0046)"},
    ]
    # decisions/0079 Sec 2 -- every waterfall FIGURE carries the build it was measured on.
    for w in wf:
        stamp(w)
    for w in R["waterfall_DERIV"]:
        stamp(w)
    R["inert_positions"] = {
        "ruling": ("decisions/0079 Sec 4 -- positions 1, 2, 3 and 7 remove ZERO BY "
                   "CONSTRUCTION. KEEP THEM AND LABEL THEM INERT, WITH THE REASON"),
        "positions": [1, 2, 3, 7],
        "why_kept": ("removing a position removes the check that would catch a future upstream "
                     "change, and the point of a fixed order is that the waterfall is "
                     "comparable across runs and across arms"),
        "why_labelled": ("an unlabelled always-zero filter reads as evidence THE RULE FOUND "
                         "NOTHING when it is evidence THE RULE CANNOT FIRE -- the same defect "
                         "as an unlabelled code check (0069)"),
        "reasons": {"1": "line 1 is already the frame",
                    "2": ("line 1 is already the L2 > 1 S1-completer population (0068), and 0 "
                          "of 1,138 frame shows have L2 = 1"),
                    "3": ("same -- BUT THE RULE IS NOT INERT: it removes 58,345 pairs upstream "
                          "of line 1, which is why its drop set is a deliverable"),
                    "7": "outcome assignment annotates and removes nothing (0046)"},
        "measured_on_build": BUILD,
    }
    assert int(line5.sum()) == 196_654, int(line5.sum())
    assert int(d5.sum()) == 147_370, int(d5.sum())

    # =====================================================================
    # THE ANALYSIS TABLE
    # =====================================================================
    nA, nAH = K["nA"], K["nAH"]
    m_H = maxnum_before(nAH)
    p_rank = np.where(m_H >= 0, rank_tab[s_idx, np.clip(m_H, 0, maxE)], 0)
    p_val = np.where(K["sal"] & (m_H >= 0), p_rank / np.maximum(L2a[s_idx], 1), np.nan)

    # ---- p_at_bound (decisions/0082, RESTATED by 0083 Sec 2) ---------------
    # THE COLUMN MARKS WHETHER p REACHED ITS BOUND, NOT WHY. TRUE where p
    # reached its bound, null where p is null.
    #
    # 0082's definition by two MECHANISMS -- "TRUE where the rank numerator
    # saturated at L2, FALSE where the pair left at the final episode" -- is
    # SUPERSEDED: the clauses are COEXTENSIVE BY CONSTRUCTION and the FALSE class
    # is EMPTY. On the adopted rank form p = |{e in E2 : e <= m_H}| / L2 the
    # set-membership drop rule puts m_H in E2, so the numerator equals L2 iff no
    # listed episode exceeds m_H, iff m_H = max(E2) = F2 -- which IS "left at the
    # final episode". Neither clause can hold without the other.
    #
    # Both mechanisms are still COMPUTED SEPARATELY below, because an emptiness
    # asserted in prose and never emitted cannot be checked: if a future run ever
    # produces a row in one class and not the other, the rank form or the
    # set-membership rule has broken, and that is worth catching.
    has_p = ~np.isnan(p_val)
    rank_saturated = has_p & (p_rank >= L2a[s_idx])
    left_at_final = has_p & (m_H == F2a[s_idx])
    p_is_one = has_p & (p_val >= 1.0)

    outcome = np.where(K["never"], "never_started",
                       np.where(K["contd"], "continued", "started_and_left"))

    # S3-or-later evidence on that show, for D4 -- and a table column, because D4
    # reads it and Step 9 does not hold the episode-level evidence (0077 Sec 3).
    has_s3 = np.isin(comp_pair, b["s3_pairs"])
    has_any_s2_record = np.isin(comp_pair, b["s2_any_rec_pairs"])

    # discovery channel: TWO booleans (0070 ruling 3)
    # EVERY COUNT STATES ITS POPULATION (0077 Sec 1): the overlap is 324 of the
    # 5,694-username Step 3 DISCOVERY POOL and 178 of the 2,549 ACCOUNTS PULLED.
    # 0070 ruling 3 gave "324 users" with no population -- a count without its
    # population is the shape that has recurred through this entire chain.
    users = json.loads((P5 / "user_index.json").read_text())["users"]
    pool_rows = [json.loads(line)
                 for line in open(ROOT / "raw" / "step3" / "user_pool.jsonl")]
    pool = {}
    for d in pool_rows:
        flags = (bool(d["in_a"]), bool(d["in_b"]))
        pool[d["slug"].lower()] = flags
        pool.setdefault(d["username"].lower(), flags)
    ch = np.array([pool.get(str(users[i]).lower(), (False, False))
                   for i in range(len(users))])
    in_a_u, in_b_u = ch[:, 0].astype(bool), ch[:, 1].astype(bool)

    led_final: dict = {}
    for line in open(ROOT / "processed" / "step4" / "pull_ledger.jsonl"):
        d = json.loads(line)
        led_final[str(d.get("slug") or d.get("username")).lower()] = d
    pulled = [k for k, d in led_final.items() if d.get("outcome") == "complete"]

    def _split(flags: list[tuple[bool, bool]]) -> dict:
        return {"n": len(flags),
                "channel_A_only": sum(1 for a, bb in flags if a and not bb),
                "channel_B_only": sum(1 for a, bb in flags if bb and not a),
                "BOTH": sum(1 for a, bb in flags if a and bb),
                "NEITHER": sum(1 for a, bb in flags if not a and not bb)}

    accts5 = np.unique(u_idx[line5])
    pa, pb = in_a_u[u_idx][line5], in_b_u[u_idx][line5]
    pairs_split = {"n": int(line5.sum()),
                   "channel_A_only": int((pa & ~pb).sum()),
                   "channel_B_only": int((pb & ~pa).sum()),
                   "BOTH": int((pa & pb).sum()),
                   "NEITHER": int((~pa & ~pb).sum())}
    R["discovery_channel"] = {
        "form": "TWO BOOLEAN COLUMNS, not one categorical (decisions/0070 ruling 3)",
        "every_figure_states_its_population": (
            "decisions/0077 Sec 1 -- 0070 ruling 3 stated '324 users' with NO POPULATION. "
            "All readings are measured here rather than restated"),
        "PUBLISH_IN_BOTH_UNITS_EACH_WITH_ITS_CONSUMER": (
            "decisions/0079 Sec 3 -- picking one unit leaves the other consumer holding a "
            "WRONG-UNIT figure. All three readings publish, each with its consumer named"),
        "consumers": {
            "step3_discovery_pool": ("DISCOVERY-POOL USERNAMES. Consumer: Step 3's "
                                     "seeding-bias statement and Step 14 ledger item 1 -- the "
                                     "POOL's composition"),
            "accounts_pulled_step4_complete": ("ACCOUNTS PULLED. Consumer: Step 4 coverage "
                                               "reporting"),
            "accounts_in_the_APPLY_position5_population": (
                "ACCOUNTS and PAIRS in the position-5 population. Consumer: STEP 11, which "
                "recomputes the headline within each channel and therefore cuts THE ANALYSIS "
                "POPULATION, NOT THE POOL. 0079 Sec 3 corrects the mapping dictated in the "
                "ruling, which had assigned Step 11 to the pool: the headline is over pairs on "
                "the position-5 row set"),
        },
        "step3_discovery_pool": _split([(bool(d["in_a"]), bool(d["in_b"]))
                                        for d in pool_rows]),
        "accounts_pulled_step4_complete": _split([pool.get(k, (False, False))
                                                  for k in pulled]),
        "accounts_in_the_APPLY_position5_population": _split(
            [(bool(in_a_u[i]), bool(in_b_u[i])) for i in accts5]),
        "PAIRS_in_the_APPLY_position5_population": pairs_split,
        "pool_file_rows_vs_distinct_slugs": {
            "rows": len(pool_rows),
            "distinct_slugs_case_insensitive": len({d["slug"].lower() for d in pool_rows}),
            "note": ("the pool file holds 5,694 ROWS and 5,693 distinct slugs "
                     "case-insensitively -- one account appears as two case variants. "
                     "The published population is the row count, 5,694, and the overlap "
                     "is 324 under both readings; measured rather than assumed inert"),
        },
        "why_two_flags": ("Step 11 tests whether discovery method biased the pool, so a "
                          "single categorical value would either DROP the overlap or assign "
                          "it arbitrarily, and the arbitrary assignment would be invisible "
                          "in the dual diff. Two flags let Step 11 cut on either channel or "
                          "on the overlap"),
    }

    # per-pair action counts by type (0070 ruling 4)
    act_key, act_n = b["act_key"], b["act_n"]
    ak_pair = act_key // 8
    ak_slot = act_key % 8
    acts = np.zeros((n1, 8), dtype=np.int32)
    lp = np.searchsorted(comp_pair, ak_pair)
    lp_ok = (lp < n1) & (comp_pair[np.clip(lp, 0, n1 - 1)] == ak_pair)
    acts[lp[lp_ok], ak_slot[lp_ok]] = act_n[lp_ok]
    act_names = ["s1_watch", "s1_checkin", "s1_scrobble", "s1_other",
                 "s2_watch", "s2_checkin", "s2_scrobble", "s2_other"]

    sel = line5    # the table is emitted on the POSITION-5 population, with flags
    tab = pd.DataFrame({
        "user_idx": u_idx[sel],
        "show_trakt_id": show_ids[s_idx[sel]],
        "in_apply": True,
        "in_deriv": line4_step5[sel],
        "live": ~K["notlive"][sel],
        "outcome": outcome[sel],
        "silent_at_tau1": K["silent"][sel],
        "abandonment_point_p": p_val[sel],
        "discovered_channel_a": in_a_u[u_idx[sel]],
        "discovered_channel_b": in_b_u[u_idx[sel]],
        "t0_date": pd.to_datetime(t0_mid[sel], unit="s").date,
        "s1_completion_date": pd.to_datetime(np.clip(comp_date_mid[sel], -62135596800,
                                                     TAU_PULL), unit="s").date,
        "t0_binding_term": binds[sel],
        "tau1": K["tau1"][sel], "tau2": K["tau2"][sel],
        "n_A": nA[sel], "n_A_H": nAH[sel],
        "max_episode_in_A_H": m_H[sel],
        "has_s3_or_later_evidence": has_s3[sel],
        "s1_completion_used_a_post_cutoff_record": comp_post_cutoff[sel],
    })
    # TRUE where p reached its bound; null where p is null (0082, restated 0083).
    pab = pd.array(rank_saturated[sel], dtype="boolean")
    pab[~has_p[sel]] = pd.NA
    tab["p_at_bound"] = pab
    for j, nm in enumerate(act_names):
        tab["action_count_" + nm] = acts[sel, j]
    show_cols = [c for c in frame.columns if c != "show_trakt_id"]
    tab = tab.merge(frame[["show_trakt_id"] + show_cols], on="show_trakt_id", how="left")
    assert len(tab) == int(sel.sum())

    # decisions/0080 Sec 1, extended by 0081 and 0082 -- EXACTLY the 89
    # enumerated names, no more and no fewer.
    emitted, ruled = set(tab.columns), set(COLUMNS_89)
    assert emitted == ruled, {"extra": sorted(emitted - ruled), "missing": sorted(ruled - emitted)}
    tab = tab[COLUMNS_89]
    tab.to_csv(OUT / "analysis_table.csv.gz", index=False, compression="gzip")
    R["analysis_table"] = {
        "path": "processed/step8/b/analysis_table.csv.gz",
        "rows": int(len(tab)),
        "row_set": ("the POSITION-5 population, APPLY = 196,654, carrying the position-6 "
                    "flag `live` and the position-7 `outcome`. The post-position-7 row set "
                    "is `live == True` (195,951); DERIV is `in_deriv` (147,370) and its "
                    "post-position-7 row set is `in_deriv & live`. The 703 excluded rows "
                    "are retained IN THE FILE with live = False, because Step 9's bounds "
                    "are built from their outcome states and rebuilding them downstream "
                    "would be a second definition of the filter"),
        "columns": int(len(tab.columns)),
        "column_names": list(tab.columns),
        "action_is_counts_not_a_column": True,
        "discovery_channel_is_two_booleans": True,
        "column_set_is_ENUMERATED": {
            "ruling": ("decisions/0080 Sec 1 -- THE COLUMN SET IS ENUMERATED, NOT COUNTED, "
                       "replacing 0077 Sec 3's count. EXTENDED TO 88 BY 0081 (silent_at_tau1 "
                       "restored) AND TO 89 BY 0082 (p_at_bound added). The arms converged on "
                       "the 87 names at the previous run but CONVERGED IS NOT SPECIFIED, and "
                       "Step 8b's schema is built on this vocabulary, so it is fixed before the "
                       "schema exists"),
            "names_ruled": 89,
            "names_emitted": int(len(tab.columns)),
            # 0077's own words: "Matching a count is not matching a set --
            # assert on the names." The set assertion runs above, but the
            # DELIVERABLE carried only the two counts, so a reader of the
            # artifact had a count and no set. The names are emitted here.
            "names_emitted_LIST": list(tab.columns),
            "names_ruled_LIST": list(COLUMNS_89),
            "names_in_emitted_not_in_ruled": sorted(set(tab.columns) - set(COLUMNS_89)),
            "names_in_ruled_not_in_emitted": sorted(set(COLUMNS_89) - set(tab.columns)),
            "why_the_lists_are_emitted": (
                "decisions/0077: 'Matching a count is not matching a set -- assert on the "
                "names.' The previous build published names_ruled: 89 and names_emitted: 89 and "
                "no list, so the deliverable asserted a COUNT match while the code asserted a "
                "SET match. The two are different claims and only one was visible"),
            "exact_match_to_the_enumerated_list": sorted(tab.columns) == sorted(COLUMNS_89),
            "emitted_in_the_enumerated_order": list(tab.columns) == COLUMNS_89,
            "transcribed_from": ("task-sheet.md Step 8's enumeration as it now stands, name by "
                                 "name; the same list appears in this instance's own definition "
                                 "file and the two were checked against each other"),
            "changed_from_this_arms_previous_run": {
                "added": [], "dropped": [],
                "why": ("the column SET does not move at 0083. This arm's previous build "
                        "(2026-08-16 clean run, spec through 0082) already emitted these 89 "
                        "names. What 0083 Sec 2 changes is what p_at_bound MEANS -- WHETHER p "
                        "reached its bound, not WHY -- which restates the column's definition "
                        "and MOVES NO VALUE, because the WHETHER form and 0082's rank-saturation "
                        "clause select the identical rows. The two 0083 Sec 3 residuals are spec "
                        "corrections on surfaces this instance reads, not column changes"),
                "the_87_is_two_builds_back": ("the 87-name build predates 0081 and 0082; it is "
                                              "named here so the 87 is not later read as this "
                                              "arm's current answer"),
            },
            "the_two_free_drops_stand": {
                "f2_in_A_H": "DERIVABLE as (max_episode_in_A_H == s2_F)",
                "max_episode_in_A": "read by nothing downstream",
            },
            "superseded_forms_absent": {
                nm: bool(nm not in tab.columns) for nm in
                ["in_population_APPLY", "n_rec_s1_watch", "tau1_utc", "tau2_utc",
                 "max_episode_in_AH", "T0_binding_term", "action", "discovery_channel",
                 "f2_in_A_H", "max_episode_in_A"]},
            "residuals_this_arm_reported_last_run_RE_MEASURED": _spec_residuals(),
        },
    }

    # =====================================================================
    # B3 -- THE TWO UNASSERTED MANDATES ARE MEASURED, NOT SELF-REPORTED
    # decisions/0088 Sec 1, on Red Team's B3/F1, which blocked the gate on the
    # third and fourth passes. The mandates are THE HALF-OPEN UTC-INSTANT FORM
    # and D11-AS-GLOBAL-CUTOFF -- not invariants 7 and 8, which are already
    # measured and published. Compliance was never the suspected defect; what was
    # missing is any measurement of whether either mandate is LOAD-BEARING on
    # this data, and an unmeasured pass is indistinguishable from a check that
    # looked nowhere.
    # =====================================================================
    st1 = json.loads((OUT / "stage1.json").read_text())
    tau1_a, tau2_a = K["tau1"], K["tau2"]

    def _win(tau: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """(episodes in [tau - 24h, tau), episodes exactly at tau, episodes in [tau, tau + 24h)).

        THE THIRD ONE IS THE SEPARATING INTERVAL AND IT IS THE ONE THAT SETTLES B3.
        decisions/0089 Sec 2(a) corrects decisions/0088 Sec 1(a): T0 is day-floored,
        so tau1 and tau2 are MIDNIGHT-ALIGNED, which makes `date(ts) < date(tau)`
        identical to `ts < tau` for every instant BELOW tau. [tau - 24h, tau) is
        therefore the interval on which the half-open and date-level forms AGREE,
        and measuring the verdict there measures the wrong set. The forbidden form
        `date(watched_at) <= T1` admits exactly `ts < tau + 24h`, so the rows on
        which the two forms DIFFER are [tau, tau + 24h) -- the instant exactly at
        tau being its first member, not the whole of it.
        """
        lo = np.maximum(tau - DAY, TS_MIN)   # below TS_MIN the count is 0 either way
        return (n_before(tau) - n_before(lo),
                n_before(tau + 1) - n_before(tau),
                n_before(tau + DAY) - n_before(tau))

    prev1, at1, sep1 = _win(tau1_a)
    prev2, at2, sep2 = _win(tau2_a)

    # ---- THE DATE-LEVEL COUNTERFACTUAL -----------------------------------
    # The count on the separating interval says how many rows COULD move; it does
    # not say how many DO. decisions/0089 Sec 2(a): "the number that settles B3 is
    # how many position-5 rows change OUTCOME STATE under the forbidden date-level
    # form, four numbers, both bounds x both populations." So the three outcome
    # states are RECOMPUTED under `date(watched_at) <= T1`, which is `ts < tau +
    # 24h`, and the states are diffed row by row. The forbidden form is computed
    # HERE AND NOWHERE ELSE, as a counterfactual whose only output is a count; the
    # emitted table, every waterfall line and every other figure are half-open.
    nA_dl = n_before(tau1_a + DAY)
    nAH_dl = n_before(tau2_a + DAY)
    f2_in_AH_dl = f2ts < tau2_a + DAY
    THRr = THR2a[s_idx]

    def _states(nA_, nAH_, f2_):
        st_ = np.where(nA_ < 1, 0, np.where(f2_ & (nAH_ >= THRr), 1, 2))
        return st_       # 0 never started, 1 continued, 2 started and left

    st_half = _states(nA, nAH, K["f2_in_AH"])
    st_tau1 = _states(nA_dl, nAH, K["f2_in_AH"])          # tau1 relaxed only
    st_tau2 = _states(nA, nAH_dl, f2_in_AH_dl)            # tau2 relaxed only
    st_both = _states(nA_dl, nAH_dl, f2_in_AH_dl)        # both relaxed
    assert (st_half == np.where(K["never"], 0, np.where(K["contd"], 1, 2))).all(), \
        "the counterfactual's half-open baseline must reproduce the pipeline's own states"
    STATE_NAMES = ["never_started", "continued", "started_and_left"]

    # the same window on RAW in-E2 S2 records rather than on distinct episodes,
    # because the ruling says "S2 records" and the two are different objects.
    e2_sets = [sorted({int(x) for x in str(s).split(",") if x.strip().isdigit()})
               for s in frame.s2_E]
    valid2 = np.array(sorted((int(show_ids[i]) << 20) | e
                             for i in range(n_shows) for e in e2_sets[i]), dtype=np.int64)
    zf = np.load(P5 / "full_scan.npz")
    rk, rs2, rn2, rsh2, rts2, ru2 = (zf["kind"], zf["season"], zf["number"],
                                     zf["show"], zf["ts"], zf["user"])
    si2 = np.searchsorted(show_ids, rsh2)
    si2[si2 >= n_shows] = 0
    mrec = ((rk == 1) & (show_ids[si2] == rsh2) & (rs2 == 2) & (rts2 < TAU_PULL)
            & (rn2 >= 0) & (rn2 < 4096))
    rc = np.where(mrec, (show_ids[np.where(mrec, si2, 0)] << 20) | np.clip(rn2, 0, 4095), -1)
    mrec &= np.isin(rc, valid2)
    rpair = ru2[mrec].astype(np.int64) * n_shows + si2[mrec].astype(np.int64)
    rtsv = rts2[mrec].astype(np.int64)
    rloc = np.searchsorted(comp_pair, rpair)
    rhit = (rloc < n1) & (comp_pair[np.clip(rloc, 0, n1 - 1)] == rpair)
    rrow = np.where(rhit, rloc, 0)
    del zf, rk, rs2, rn2, rsh2, rts2, ru2, si2, rc

    boundary = {}
    for popnm, pmask in (("APPLY_position5", line5), ("DERIV_position5", d5)):
        inpop = rhit & pmask[rrow]
        rt = rtsv[inpop]
        r1 = tau1_a[rrow[inpop]]
        r2 = tau2_a[rrow[inpop]]
        boundary[popnm] = {
            "rows_in_the_stated_population": int(pmask.sum()),
            "DISTINCT_EPISODES_the_form_the_outcome_assignment_reads": {
                "unit": ("distinct in-E2 S2 episodes at their CANONICAL instant -- the objects "
                         "|A| and |A_H| are counted over"),
                "WHICH_INTERVAL_SEPARATES_THE_FORMS": (
                    "[tau, tau + 24h). NOT [tau - 24h, tau), which is where they AGREE "
                    "(decisions/0089 Sec 2a). tau is midnight-aligned because T0 is day-floored, "
                    "so below tau the date-level and half-open forms admit the identical set"),
                "SEPARATING_in_[tau1, tau1_plus_24h)": int(sep1[pmask].sum()),
                "SEPARATING_in_[tau2, tau2_plus_24h)": int(sep2[pmask].sum()),
                "AGREEING_in_[tau1_minus_24h, tau1)": int(prev1[pmask].sum()),
                "AGREEING_in_[tau2_minus_24h, tau2)": int(prev2[pmask].sum()),
                "exactly_at_tau1": int(at1[pmask].sum()),
                "exactly_at_tau2": int(at2[pmask].sum()),
                "episodes_examined": int(nAH[pmask].sum()),
                "note_on_the_two_ruled_cells": (
                    "the [tau - 24h, tau) counts and the exactly-at counts are the cells "
                    "decisions/0088 Sec 1(a) named and are kept; the exactly-at cells are the "
                    "FIRST INSTANT of the separating interval, not the whole of it, and this "
                    "arm's previous build reported its verdict off them alone"),
            },
            "RAW_RECORDS_the_ruling's_own_word": {
                "unit": "in-E2 S2 episode RECORDS surviving D11, undeduplicated",
                "records_examined": int(inpop.sum()),
                "SEPARATING_in_[tau1, tau1_plus_24h)":
                    int(((rt >= r1) & (rt < r1 + DAY)).sum()),
                "SEPARATING_in_[tau2, tau2_plus_24h)":
                    int(((rt >= r2) & (rt < r2 + DAY)).sum()),
                "AGREEING_in_[tau1_minus_24h, tau1)": int(((rt >= r1 - DAY) & (rt < r1)).sum()),
                "AGREEING_in_[tau2_minus_24h, tau2)": int(((rt >= r2 - DAY) & (rt < r2)).sum()),
                "exactly_at_tau1": int((rt == r1).sum()),
                "exactly_at_tau2": int((rt == r2).sum()),
            },
            "LIVENESS_EVIDENCE_at_tau1": {
                "unit": ("rows whose account's maximum insertion instant sits on the boundary "
                         "the STRICT silence test reads"),
                "rows_examined": int(pmask.sum()),
                "max_insertion_instant_in_[tau1_minus_24h, tau1)":
                    int((pmask & (mx >= tau1_a - DAY) & (mx < tau1_a)).sum()),
                "max_insertion_instant_exactly_at_tau1": int((pmask & (mx == tau1_a)).sum()),
                "why_this_one_is_here": ("the silence test is STRICT (0068) -- an instant "
                                         "exactly AT tau1 does not make the account live -- so "
                                         "the rows exactly at tau1 are the rows on which strict "
                                         "and non-strict readings of the RULE differ, as "
                                         "opposed to the rows on which half-open and date-level "
                                         "readings of the CLOCK differ"),
            },
        }
        # THE NUMBER THAT SETTLES B3: how many rows CHANGE OUTCOME STATE under the
        # forbidden date-level form, measured on the SEPARATING interval by
        # recomputing the three states, not inferred from a boundary occupancy
        # count. decisions/0089 Sec 2(a): four numbers, both bounds x both
        # populations. Reported here as the two per-bound numbers for this
        # population, plus the joint form and the state-transition breakdown.
        def _diff(stx: np.ndarray) -> dict:
            ch = pmask & (stx != st_half)
            trans: dict[str, int] = {}
            for a_ in range(3):
                for b_ in range(3):
                    c_ = int((ch & (st_half == a_) & (stx == b_)).sum())
                    if c_:
                        trans[f"{STATE_NAMES[a_]} -> {STATE_NAMES[b_]}"] = c_
            return {"rows_changing_outcome_state": int(ch.sum()),
                    "transitions": trans,
                    "rows_examined": int(pmask.sum())}

        boundary[popnm]["WHAT_THE_FORM_DECIDES"] = {
            "THE_QUESTION": ("how many position-5 rows change OUTCOME STATE under the forbidden "
                             "`date(watched_at) <= T1` form, which admits `ts < tau + 24h`"),
            "measured_by": ("recomputing never_started / continued / started_and_left under the "
                            "date-level form and diffing row by row against the half-open "
                            "states this pipeline emits -- not inferred from a boundary count"),
            "tau1_relaxed_only": _diff(st_tau1),
            "tau2_relaxed_only": _diff(st_tau2),
            "BOTH_bounds_relaxed_the_full_forbidden_form": _diff(st_both),
            "rows_with_an_S2_episode_in_the_SEPARATING_interval_at_tau1":
                int((pmask & (sep1 > 0)).sum()),
            "rows_with_an_S2_episode_in_the_SEPARATING_interval_at_tau2":
                int((pmask & (sep2 > 0)).sum()),
            "rows_with_an_S2_episode_exactly_at_tau1": int((pmask & (at1 > 0)).sum()),
            "rows_with_an_S2_episode_exactly_at_tau2": int((pmask & (at2 > 0)).sum()),
            "WHAT_THE_PREVIOUS_BUILD_MEASURED": (
                "this arm's r4 build computed its verdict from the rows exactly AT tau1 only -- "
                "1 row of the separating interval -- and reported no outcome state differing. "
                "decisions/0089 Sec 2(a) records that as a claim about the set on which the "
                "forms differ, computed on the wrong set. The verdict below is recomputed on "
                "the separating interval and the previous one is superseded"),
            "reading": ("under the half-open form an instant in [tau, tau + 24h) is OUTSIDE the "
                        "set; under the date-level form it is INSIDE. At tau1 that turns a "
                        "never-started row with such an episode into a started one; at tau2 it "
                        "can turn a started-and-left row into a Continued one"),
        }
        _bp = boundary[popnm]
        _de = _bp["DISTINCT_EPISODES_the_form_the_outcome_assignment_reads"]
        _rr = _bp["RAW_RECORDS_the_ruling's_own_word"]
        # OCCUPANCY IS MEASURED ON THE SEPARATING INTERVAL, which is the set the
        # verdict is about. The agreeing-window cells cannot make the mandate
        # load-bearing however large they are.
        _on = (_de["SEPARATING_in_[tau1, tau1_plus_24h)"]
               + _de["SEPARATING_in_[tau2, tau2_plus_24h)"]
               + _rr["SEPARATING_in_[tau1, tau1_plus_24h)"]
               + _rr["SEPARATING_in_[tau2, tau2_plus_24h)"])
        _dec = _bp["WHAT_THE_FORM_DECIDES"][
            "BOTH_bounds_relaxed_the_full_forbidden_form"]["rows_changing_outcome_state"]
        _bp["OCCUPANCY_BASIS"] = ("the SEPARATING interval [tau, tau + 24h) at both bounds, "
                                  "distinct episodes and raw records; NOT the agreeing window")
        _bp["VERDICT"] = (
            "VACUOUS ON THIS DATA -- the separating interval is EMPTY at both bounds, so the "
            "half-open UTC-instant form and the date-level form select the identical sets and "
            "the mandate is not load-bearing on this build. STATED AS A ZERO, NOT PASSED "
            "SILENTLY" if _on == 0
            else ("OCCUPIED AND OUTCOME-DECIDING -- the separating interval is non-empty AND "
                  f"the two forms disagree on the OUTCOME STATE of {_dec} row(s) of "
                  f"{int(pmask.sum()):,}. The mandate is load-bearing and it is load-bearing "
                  "ON THE RESULT, not only on |A|" if _dec > 0
                  else ("OCCUPIED, NOT VACUOUS, AND NO OUTCOME MOVES -- the separating interval "
                        "is NON-EMPTY, so the half-open form is doing real work in |A| and "
                        "|A_H|; but every row with an episode there already has |A| >= 1 from "
                        "other episodes and its Continued test does not turn, so no outcome "
                        "state differs. THREE STATES, NOT TWO: an empty separating interval, an "
                        "occupied one that decides nothing, and an occupied one that decides an "
                        "outcome are different findings and collapsing the middle into either "
                        "neighbour is the misreading")))
        _bp["VERDICT_STATE"] = ("VACUOUS" if _on == 0
                                else "OUTCOME_DECIDING" if _dec > 0 else "OCCUPIED_INERT")
        _bp["VERDICT_SUPERSEDES"] = (
            "this arm's r4 verdict, which was computed on [tau - 24h, tau) and the single "
            "instant at tau -- the interval on which the two forms AGREE plus its first "
            "separating point (decisions/0089 Sec 2a)")

    # ---- (b) the per-site D11 table -------------------------------------
    fp = st1["D11_record_level_footprint"]
    acs = st1["D11_action_count_sites"]
    s1site = st1["s1_completion"]["D11_site"]
    d11_pairs_in_pop = {}
    # which position-5 rows have an action count that MOVED because D11 is now
    # applied at the action-count sites -- the size of this run's own change
    sites = []

    def _site(name, applied, excluded, unit, assertion, reason, extra=None):
        row = {"site": name, "d11_applied": applied, "unit": unit,
               "records_excluded_by_D11": excluded,
               "assertion": ("no record dated at or after tau_pull participates in this "
                             "computation"),
               "assertion_holds": assertion, "note": reason}
        if extra:
            row.update(extra)
        # A PASS ON A SITE THAT EXAMINED NOTHING IS NOT A PASS.
        # CLAUDE.md: "An empty result and a clean result are the same value, and
        # only the control knows which it produced. A check that finds nothing
        # because it looked nowhere must FAIL, not pass." decisions/0088 Sec 1(a)
        # says the same thing about the boundary window: "IF 0, LABEL THE
        # INVARIANT VACUOUS -- do not let it pass silently."
        #
        # The examined count was already printed at every site on the previous
        # build, which is the half of the rule that was met. THIS is the half
        # that was not: `assertion_holds: True` read identically at a site with
        # 2.7M records and at a site with 0.
        ex = row.get("records_counted_at_this_site")
        row["records_examined_at_this_site"] = ex
        if ex == 0:
            row["assertion_is_VACUOUS_zero_coverage"] = True
            row["assertion_holds_READ_AS"] = (
                "VACUOUS -- this site examined 0 records, so the assertion is true of the empty "
                "set and is NOT evidence that D11 is applied here. Labelled rather than passed "
                "silently (CLAUDE.md; decisions/0088 Sec 1a). The site is empty because no "
                "record in the sweep carries this action type, which is itself the finding")
        elif ex is not None:
            row["assertion_is_VACUOUS_zero_coverage"] = False
        sites.append(row)

    _site("A (|A| at tau1)", True, fp["S2_side"]["records_excluded"], "in-E2 S2 records",
          bool(int(s2_ts.max()) < TAU_PULL),
          "A is counted over distinct in-E2 S2 episodes whose evidence was D11-filtered at "
          "stage 1; the assertion is measured on the episode instants actually stored",
          {"distinct_episodes_excluded": fp["S2_side"]["distinct_episodes_excluded"],
           "pairs_touched": fp["S2_side"]["distinct_pairs_touched"],
           "records_counted_at_this_site": int(len(s2_ts)),
           "latest_instant_used_utc": str(np.datetime64(int(s2_ts.max()), "s"))})
    _site("A_H (|A_H| at tau2)", True, fp["S2_side"]["records_excluded"], "in-E2 S2 records",
          bool(int(s2_ts.max()) < TAU_PULL),
          "same evidence array as A, read at a later instant; the exclusion is the same set of "
          "records and is stated here rather than left implicit in A's row",
          {"distinct_episodes_excluded": fp["S2_side"]["distinct_episodes_excluded"],
           "pairs_touched": fp["S2_side"]["distinct_pairs_touched"],
           "records_counted_at_this_site": int(len(s2_ts))})
    for nm in ("s1_watch", "s1_checkin", "s1_scrobble", "s1_other",
               "s2_watch", "s2_checkin", "s2_scrobble", "s2_other"):
        exc = (fp["S1_side"]["by_action"][nm.split("_", 1)[1]] if nm.startswith("s1")
               else fp["S2_side"]["by_action"][nm.split("_", 1)[1]])
        _site("action_count_" + nm, True, exc, "in-E S1/S2 records",
              acs["assertion_no_record_at_or_after_tau_pull_is_counted_per_site"][nm],
              ("D11 IS APPLIED AT THIS SITE ON THIS BUILD. On r3 the four s1_* sites counted "
               "post-cutoff records, because the S1 side is carried past tau_pull so 0068's "
               "published line 1 survives -- an exception that has a ruling behind it for the "
               "COMPLETION WALK and none here. Asserting per site is what exposed it"
               if nm.startswith("s1") else
               "the S2 side was already D11-filtered before the action counts were formed"),
              {"records_counted_at_this_site": acs["records_used_per_site"][nm],
               "latest_watched_at_counted_utc": acs["latest_watched_at_counted_per_site_utc"][nm],
               "site_is_empty": nm in acs["sites_with_no_records_at_all"]})
    _site("liveness evidence (per-account maximum insertion instant)", True,
          int(R["liveness_inputs"]["records_excluded_by_the_tau_pull_restriction"]),
          "records of any kind, whole sweep",
          bool(R["liveness_inputs"]["max_insertion_instant_utc"]
               <= R["liveness_inputs"]["max_insertion_instant_unrestricted_utc"]),
          "0070 ruling 2 -- the silence test's evidence is restricted to records dated before "
          "tau_pull. Measured to be inert on the exclusion set: 703 and 99 either way",
          {"records_used": int(R["liveness_inputs"]["records_used"]),
           "records_counted_at_this_site": int(R["liveness_inputs"]["records_used"])
           + int(R["liveness_inputs"]["records_excluded_by_the_tau_pull_restriction"]),
           "exclusions_restricted": per_arm["APPLY"]["108"]["liveness_excluded"],
           "exclusions_unrestricted": per_arm["APPLY"]["108"][
               "liveness_excluded_under_unrestricted_evidence"]})
    # The D9 row is BACKFILLED AT STAGE 3, where the coverage pivot is built.
    # decisions/0088 Sec 1(b): "asserted at EACH site, not once and about the
    # rest." This arm's -r4 build published `records_excluded_by_D11: null` and
    # `assertion_holds: null` here while counting the site among the 12 where
    # D11 is applied -- a site listed as asserted and not asserted. The number
    # existed in d9.json and never reached the published table. The sentinel
    # below is REPLACED at stage 3 and the replacement is asserted there; if the
    # backfill does not run, the sentinel is visible rather than a null.
    _site("D9 coverage rows", True, "PENDING_STAGE_3_BACKFILL",
          "S1/S2 episode records, ALL shows in the sweep",
          "PENDING_STAGE_3_BACKFILL",
          "measured at stage 3, where the D9 coverage pivot is built, and BACKFILLED INTO THIS "
          "ROW there. The -r4 build left this row null in the published table while d9.json "
          "carried the number",
          {"backfilled_from": "processed/step8/b/d9.json -> D11_site",
           "records_counted_at_this_site": "PENDING_STAGE_3_BACKFILL"})
    _site("S1 completion walk", False, s1site["records_at_or_after_tau_pull_that_this_site_uses"],
          "distinct in-E1 S1 episodes at their canonical instant",
          s1site["assertion_no_record_at_or_after_tau_pull_is_counted"],
          s1site["why_not"],
          {"records_at_or_after_tau_pull_in_the_input": fp["S1_side"]["records_excluded"],
           "records_counted_at_this_site": s1site["records_examined_by_the_walk"],
           "distinct_episodes_they_form": fp["S1_side"]["distinct_episodes_excluded"],
           "distinct_episodes_whose_CANONICAL_instant_is_post_cutoff":
               s1site["records_at_or_after_tau_pull_that_this_site_uses"],
           "why_the_three_numbers_differ": ("73 records collapse to 72 distinct episodes, and "
                                            "12 of those also carry a pre-cutoff record whose "
                                            "instant is the canonical one -- so only 60 "
                                            "episodes enter the walk with a post-cutoff "
                                            "instant. Three different objects, named"),
           "measured_effect_line_1": {
               "line_1_as_ruled": 220107,
               "line_1_under_reading_C": st1["s1_completion"]["D11_open_question"][
                   "S1_completer_pairs_if_D11_applied_to_S1_too"],
               "pairs_that_stop_being_completers": st1["s1_completion"]["D11_open_question"][
                   "completer_set_comparison_READING_B_vs_READING_C"][
                   "in_B_and_NOT_in_C_pairs_that_stop_being_completers"],
               "completion_dates_that_move": st1["s1_completion"]["D11_open_question"][
                   "completer_set_comparison_READING_B_vs_READING_C"][
                   "of_those_whose_first_pass_completion_DATE_MOVES"]},
           "assertion_reading": ("FALSE here is the CORRECT reported state, not a failure. It "
                                 "is the one site where D11 is deliberately not applied, and "
                                 "0068 records the question as OPEN")})

    # ---- (c) the promoted assertion --------------------------------------
    promoted = {
        "assertion": "no position-5 row has tau2 > tau_pull",
        "label": "CODE CHECK",
        "ruling": ("decisions/0088 Sec 1(c) -- it already ran inside the pipeline but sat "
                   "OUTSIDE the published invariant set, so no reader of the deliverable "
                   "could see it. Published, labelled CODE CHECK"),
        "why_it_cannot_fail_on_data": ("D10 defines position 5 as [T0] + (max(W, 91) + H) x 24h "
                                       "<= tau_pull, and at W = 108 that expression IS tau2. It "
                                       "can only catch tau2 or the censoring bound computed "
                                       "wrongly"),
        "by_population": {
            "APPLY_position5": {"rows_examined": int(line5.sum()),
                                "rows_with_tau2_gt_tau_pull": int((tau2_a[line5] > TAU_PULL).sum()),
                                "rows_with_tau2_EXACTLY_at_tau_pull":
                                    int((tau2_a[line5] == TAU_PULL).sum()),
                                "latest_tau2_utc": str(np.datetime64(int(tau2_a[line5].max()), "s"))},
            "DERIV_position5": {"rows_examined": int(d5.sum()),
                                "rows_with_tau2_gt_tau_pull": int((tau2_a[d5] > TAU_PULL).sum()),
                                "rows_with_tau2_EXACTLY_at_tau_pull":
                                    int((tau2_a[d5] == TAU_PULL).sum()),
                                "latest_tau2_utc": str(np.datetime64(int(tau2_a[d5].max()), "s"))},
        },
        "the_bound_is_ATTAINED_not_slack": ("rows sit with tau2 EXACTLY at tau_pull, so the "
                                            "assertion is tight rather than comfortably "
                                            "satisfied -- a `>=` form of the same assertion "
                                            "would FAIL on this data. Stated because a passing "
                                            "assertion with slack and a passing assertion at "
                                            "the bound are not the same evidence"),
    }
    promoted["passes"] = bool(int((tau2_a[line5] > TAU_PULL).sum()) == 0
                              and int((tau2_a[d5] > TAU_PULL).sum()) == 0)

    R["B3_the_two_unasserted_mandates"] = {
        "ruling": ("decisions/0088 Sec 1 -- MEASURE BOTH. The mandates are THE HALF-OPEN "
                   "UTC-INSTANT FORM and D11-AS-GLOBAL-CUTOFF, not invariants 7 and 8. Both "
                   "arms' compliance is TRUE and was independently confirmed; what was missing "
                   "is any measurement of whether either is LOAD-BEARING on this data"),
        "ground": ("the unstated version of exactly this scope produced Step 7's 792-against-"
                   "791, where one arm applied the restriction and the other did not"),
        "a_boundary_window": {
            "what_it_measures": ("the rows on which the half-open form and a date-level form "
                                 "DIFFER -- S2 evidence in the SEPARATING interval [tau, tau + "
                                 "24h) at both bounds -- and, on those rows, how many change "
                                 "OUTCOME STATE when the forbidden form is actually applied. The "
                                 "cells decisions/0088 Sec 1(a) named, [tau - 24h, tau) and "
                                 "exactly-at-tau, are reported alongside"),
            "THE_INTERVAL_WAS_CORRECTED": (
                "decisions/0089 Sec 2(a). 0088 Sec 1(a) named [tau - 24h, tau). T0 is "
                "day-floored, so tau1 and tau2 are MIDNIGHT-ALIGNED and `date(ts) < date(tau)` "
                "is identical to `ts < tau` below the boundary -- THAT WINDOW IS WHERE THE TWO "
                "FORMS AGREE. The separating interval is [tau, tau + 24h). This arm's r4 build "
                "emitted the ruled window and the single instant exactly at tau and nothing "
                "else, and took its verdict off 1 row of the separating interval"),
            "compliance_self_report": ("no .date(), dt.date, normalize() or day-flooring "
                                       "anywhere in this arm's step8_b_*.py; instants are int64 "
                                       "seconds throughout. THAT IS THE SELF-REPORT AND IT IS "
                                       "NOT THE MEASUREMENT"),
            "THE_FOUR_NUMBERS_THAT_SETTLE_B3": {
                "definition": ("rows changing OUTCOME STATE under the forbidden date-level form, "
                               "both bounds x both populations, on the position-5 row set"),
                "APPLY_position5_tau1_relaxed": boundary["APPLY_position5"][
                    "WHAT_THE_FORM_DECIDES"]["tau1_relaxed_only"]["rows_changing_outcome_state"],
                "APPLY_position5_tau2_relaxed": boundary["APPLY_position5"][
                    "WHAT_THE_FORM_DECIDES"]["tau2_relaxed_only"]["rows_changing_outcome_state"],
                "DERIV_position5_tau1_relaxed": boundary["DERIV_position5"][
                    "WHAT_THE_FORM_DECIDES"]["tau1_relaxed_only"]["rows_changing_outcome_state"],
                "DERIV_position5_tau2_relaxed": boundary["DERIV_position5"][
                    "WHAT_THE_FORM_DECIDES"]["tau2_relaxed_only"]["rows_changing_outcome_state"],
                "APPLY_position5_both_bounds_relaxed": boundary["APPLY_position5"][
                    "WHAT_THE_FORM_DECIDES"]["BOTH_bounds_relaxed_the_full_forbidden_form"][
                    "rows_changing_outcome_state"],
                "DERIV_position5_both_bounds_relaxed": boundary["DERIV_position5"][
                    "WHAT_THE_FORM_DECIDES"]["BOTH_bounds_relaxed_the_full_forbidden_form"][
                    "rows_changing_outcome_state"],
                "why_six_and_not_four": ("the ruling asks for four -- two bounds x two "
                                         "populations. The joint form is emitted as well because "
                                         "the forbidden form relaxes BOTH bounds at once and the "
                                         "two per-bound counts do not have to sum to it: a row "
                                         "moved from never-started by tau1 can be moved again by "
                                         "tau2"),
                "the_forbidden_form_is_computed_ONLY_here": (
                    "as a counterfactual whose only output is a count. The emitted table, every "
                    "waterfall line, every share and every other figure in this deliverable are "
                    "the half-open UTC-instant form. The counterfactual asserts that its own "
                    "half-open baseline reproduces the pipeline's states exactly before it "
                    "diffs anything"),
            },
            "by_population": boundary,
            "IF_ZERO_THE_INVARIANT_IS_VACUOUS": ("a zero stated as a zero is evidence; a zero "
                                                 "arriving as a pass is not (0088 Sec 1(a)). The "
                                                 "zero that would make it vacuous is a zero on "
                                                 "the SEPARATING interval, not on the agreeing "
                                                 "window"),
        },
        "b_per_site_D11_table": {
            "what_it_measures": ("records excluded by D11 at EACH site separately, asserted at "
                                 "each site rather than once and about the rest"),
            "sites": sites,
            "sites_counted": len(sites),
            "sites_where_D11_is_applied": sum(1 for s in sites if s["d11_applied"]),
            "sites_where_D11_is_NOT_applied": [s["site"] for s in sites if not s["d11_applied"]],
            "sites_deferred_to_another_stage": [
                s["site"] for s in sites
                if s["assertion_holds"] is None
                or s["assertion_holds"] == "PENDING_STAGE_3_BACKFILL"],
            "sites_with_NO_assertion_at_all": [
                s["site"] for s in sites if s["assertion_holds"] is None],
            "THE_EXCLUSION_COLUMN_IS_NOT_SUMMABLE_AND_THE_ROWS_ARE_NOT_DISJOINT": {
                "why": ("`records_excluded_by_D11` is carried in FOUR DIFFERENT UNITS across "
                        "these rows, and the rows overlap. Adding the column produces a number "
                        "that counts nothing. Named here because one label over quantities in "
                        "different units is exactly the defect decisions/0088 Sec 2(b) ruled "
                        "on, and a table is where it hides best"),
                "units_present": sorted({s["unit"] for s in sites}),
                "overlaps": ("`A` and `A_H` report the SAME 94 records -- one evidence array "
                             "read at two instants -- and those same 94 are also the sum of the "
                             "four `action_count_s2_*` rows. The `liveness evidence` row is "
                             "records of ANY kind across the WHOLE sweep, a superset. The `D9 "
                             "coverage rows` row is over ALL shows in the sweep, not only frame "
                             "shows. The `S1 completion walk` row is in DISTINCT EPISODES at "
                             "their canonical instant, not records"),
                "the_two_figures_that_DO_sum": ("the four action_count_s1_* rows sum to 73 and "
                                                "the four action_count_s2_* rows sum to 94; "
                                                "73 + 94 = 167, which is "
                                                "in_frame_S1_S2_records_at_or_after_tau_pull. "
                                                "That identity is arithmetic on measured counts "
                                                "and is asserted below"),
                "identity_s1_side": (sum(s["records_excluded_by_D11"] for s in sites
                                         if s["site"].startswith("action_count_s1"))
                                     == fp["S1_side"]["records_excluded"]),
                "identity_s2_side": (sum(s["records_excluded_by_D11"] for s in sites
                                         if s["site"].startswith("action_count_s2"))
                                     == fp["S2_side"]["records_excluded"]),
                "identity_total": (sum(s["records_excluded_by_D11"] for s in sites
                                       if s["site"].startswith("action_count_"))
                                   == fp["in_frame_S1_S2_records_at_or_after_tau_pull"]),
            },
            "SITE_NAMES_ARE_THIS_ARMS_OWN_AND_ARE_NOT_A_RULED_VOCABULARY": (
                "decisions/0088 Sec 1(b) NAMES the sites in prose -- A, A_H, the four "
                "action_count_s{1,2}_*, the liveness evidence, D9's coverage rows, the S1 walk "
                "-- but fixes no key spelling, and it names EIGHT while the four action_count "
                "columns are EIGHT sites here, not four, because the spec's own column "
                "enumeration (0080) has eight action-count columns. This arm publishes 13 "
                "rows with prose site names. decisions/0091 Sec 3 records the other arm using "
                "`S1_completion_walk`, an underscored key, so THE TWO TABLES ARE NOT KEY-WISE "
                "DIFFABLE even where they agree numerically. Reported, not reconciled: naming "
                "is unruled, and 0088 Sec 2(c) requires two differing objects be named as two "
                "rather than merged under a shared label"),
            "THIS_RUNS_OWN_CHANGE": acs["CHANGED_FROM_THIS_ARMS_PREVIOUS_BUILD"],
            "pairs_whose_action_counts_moved": {
                "in_the_record_universe":
                    acs["pairs_whose_action_counts_move_because_D11_is_now_applied_here"],
                "of_those_present_in_the_APPLY_position5_row_set":
                    int((line5 & np.isin(comp_pair, b["d11_s1_pairs"])).sum()),
                "of_those_present_in_the_DERIV_position5_row_set":
                    int((d5 & np.isin(comp_pair, b["d11_s1_pairs"])).sum()),
                "columns_affected": ["action_count_s1_watch", "action_count_s1_checkin",
                                     "action_count_s1_scrobble"],
                "no_other_column_moves": ("the action counts are read by nothing upstream of "
                                          "themselves -- not by |A|, |A_H|, T0, the outcome "
                                          "assignment or the liveness rule -- so no waterfall "
                                          "line, no outcome share and no invariant moves with "
                                          "them"),
            },
        },
        "c_the_promoted_assertion": promoted,
        "measured_on_build": BUILD,
    }
    del rpair, rtsv, rloc, rhit, rrow

    # =====================================================================
    # REQUIRED COUNTS
    # =====================================================================
    R["required_counts"] = req = {}

    # --- drop counts -------------------------------------------------------
    st1 = json.loads((OUT / "stage1.json").read_text())
    dropped_s2_pair = b["dropped_s2_pair"]
    entire_s2_dropped = np.isin(comp_pair, dropped_s2_pair) & (nA == 0)
    ns5 = int((line5 & K["never"]).sum())
    ns7 = int((line6 & K["never"]).sum())
    # per-show drop counts are MEASURED from the stage-1 file, never assumed zero
    psd = pd.read_csv(OUT / "drop_counts_per_show.csv")
    req["drop_counts"] = {
        "per_show_file": "processed/step8/b/drop_counts_per_show.csv",
        "records_examined": st1["drop_rule"]["records_examined"],
        "records_dropped_total": st1["drop_rule"]["records_dropped"],
        "distinct_season_number_pairs_dropped":
            int(psd.distinct_dropped_season_number.sum()),
        "shows_with_any_drop": int((psd.dropped_records > 0).sum()),
        "per_outcome_pairs_whose_entire_S2_evidence_was_dropped":
            int((line5 & entire_s2_dropped).sum()),
        "denominator_never_started_at_position5": ns5,
        "denominator_never_started_post_liveness": ns7,
        "share_of_never_started_at_position5_pct":
            100.0 * int((line5 & entire_s2_dropped).sum()) / ns5,
        "share_of_never_started_post_liveness_pct":
            100.0 * int((line5 & entire_s2_dropped).sum()) / ns7,
        "denominator_note": ("the drop count is a property of the filter, so it measures "
                             "against what ENTERED it -- position 5. The post-liveness "
                             "figure is reported alongside; the difference between the two "
                             "denominators is exactly the never-started liveness exclusions "
                             "(decisions/0070 ruling 6)"),
        "coverage": ("ZERO is a measured zero: every one of the "
                     f"{st1['drop_rule']['records_examined']:,} in-frame S1/S2 episode "
                     "records surviving D11 was tested for membership in its season's "
                     "listed set E, and none failed. This check did not look nowhere"),
        "direction": "would INFLATE Never started, the same direction as D4 and D9",
    }

    # --- p_at_bound: the p = 1.0 TOTALS (0082, restated by 0083 Sec 2) ------
    # 0083: "Still report the p = 1.0 totals -- 1,246 at position 5 and 1,230
    # post-liveness on APPLY -- AS TOTALS, NOT AS A SUM OF TWO CLASSES." The
    # coextensivity is reported separately, as the emptiness check it is.
    pab_tot, pab_coext = {}, {}
    for nm, msk in (("APPLY_position5", line5), ("APPLY_position6_post_liveness", line6),
                    ("DERIV_position5", d5), ("DERIV_position6_post_liveness", d6)):
        one = msk & p_is_one
        pab_tot[nm] = {
            "rows_with_p_equal_1_0_TOTAL": int(one.sum()),
            "p_at_bound_TRUE": int((msk & rank_saturated).sum()),
            "started_and_left_rows": int((msk & K["sal"]).sum()),
            "rows_with_p_below_1_0_p_at_bound_FALSE": int((msk & K["sal"] & ~p_is_one).sum()),
            "rows_with_p_null_p_at_bound_null": int((msk & ~has_p).sum()),
            "coverage_identity": (int((msk & rank_saturated).sum())
                                  + int((msk & K["sal"] & ~p_is_one).sum())
                                  + int((msk & ~has_p).sum()) == int(msk.sum())),
        }
        pab_coext[nm] = {
            "in_BOTH_classes": int((one & rank_saturated & left_at_final).sum()),
            "saturated_not_final": int((one & rank_saturated & ~left_at_final).sum()),
            "final_not_saturated": int((one & ~rank_saturated & left_at_final).sum()),
            "in_NEITHER": int((one & ~rank_saturated & ~left_at_final).sum()),
            "rows_examined": int(one.sum()),
            "empty_classes_are_empty": int((one & rank_saturated & ~left_at_final).sum()) == 0
                                       and int((one & ~rank_saturated & left_at_final).sum()) == 0,
        }
    # A SECOND fact, DATA and not construction (0083 Sec 2): whether any frame
    # show has an S2 numbering gap. If none does, E2 = {1..L2} everywhere and the
    # rank form reduces to m_H / L2 -- but that could be FALSE on another frame
    # and the coextensivity above would still hold, so the two are stated apart.
    e2_lists = [sorted({int(x) for x in str(s).split(",") if x.strip().isdigit()})
                for s in frame.s2_E]
    gap_shows = sum(1 for e in e2_lists if e and (e != list(range(1, len(e) + 1))))

    # ---- P4 (decisions/0085 Sec 4): THE CHAIN HAS THREE LINKS AND ONLY TWO
    # ARE CONSTRUCTION.  numerator = L2 <=> m_H = max(E2) is construction given
    # L2 := |E2|, which the spec fixes.  max(E2) = F2 IS NOT: it holds only
    # because the finale is the HIGHEST-NUMBERED LISTED EPISODE, and where a
    # season lists an episode numbered above its finale the two separate. That
    # is the s2_aired_lt_listed case this step is told to count.  So it is
    # MEASURED, not assumed, and its count is stated.
    #
    # 0083 Sec 2 named TWO causes for a future FALSE row. There are THREE.
    f2_vals = pd.to_numeric(frame.s2_F, errors="coerce").values
    l2_vals = pd.to_numeric(frame.s2_L, errors="coerce").values
    max_e2 = np.array([max(e) if e else -1 for e in e2_lists], dtype=np.int64)
    len_e2 = np.array([len(e) for e in e2_lists], dtype=np.int64)
    shows_max_e2_ne_f2 = int(np.sum(max_e2 != f2_vals))
    shows_max_e2_ne_l2 = int(np.sum(max_e2 != l2_vals))
    shows_l2_ne_len_e2 = int(np.sum(l2_vals != len_e2))
    third_link = {
        "ruling": ("decisions/0085 Sec 4, Red Team P4 -- the coextensivity chain is "
                   "numerator = L2 <=> m_H = max(E2) <=> m_H = F2, and ONLY THE FIRST LINK "
                   "IS CONSTRUCTION. The second holds only because the finale is the "
                   "highest-numbered listed episode, which the s2_aired_lt_listed case can "
                   "break. It is measured here, not assumed"),
        "link_1_numerator_eq_L2_iff_m_H_eq_max_E2": {
            "status": "CONSTRUCTION, given L2 := |E2|, which the spec fixes",
            "shows_where_L2_differs_from_len_E2": shows_l2_ne_len_e2,
            "holds_on_every_frame_show": shows_l2_ne_len_e2 == 0,
        },
        "link_2_max_E2_eq_F2": {
            "status": ("NOT CONSTRUCTION -- DATA. It needs the finale to be the "
                       "highest-numbered listed episode"),
            "shows_examined": n_shows,
            "shows_where_max_E2_differs_from_F2": shows_max_e2_ne_f2,
            "shows_where_max_E2_differs_from_L2": shows_max_e2_ne_l2,
            "s2_aired_lt_listed_shows": int(frame.s2_aired_lt_listed.values.astype(bool).sum()),
            "holds_on_every_frame_show": shows_max_e2_ne_f2 == 0,
            "coverage": (f"a measured zero, not an empty look: all {n_shows:,} frame shows "
                         "were compared, max(E2) against s2_F and against s2_L"),
        },
        "three_causes_of_a_future_FALSE_row_not_two": [
            "the rank form is changed away from p = |{e in E2 : e <= m_H}| / L2",
            "the set-membership drop rule stops putting m_H in E2",
            "a frame show lists an S2 episode numbered above its finale, so max(E2) != F2 "
            "-- the third cause, added by 0085 Sec 4",
        ],
        "does_it_reopen_across_Step_13_W_grid": ("no -- the frame does not move with W, so a "
                                                 "zero here is zero at every arm"),
    }
    req["p_at_bound"] = {
        "ruling": ("decisions/0083 Sec 2, restating 0082 -- p_at_bound MARKS WHETHER p REACHED "
                   "ITS BOUND, NOT WHY. TRUE where p reached its bound; null where p is null. "
                   "Step 10 publishes the abandonment distribution off abandonment_point_p and "
                   "needs the spike LABELLED"),
        "SUPERSEDED_definition": ("0082 Sec 2's definition by two MECHANISMS -- 'TRUE where the "
                                  "rank numerator saturated at L2, FALSE where the pair left at "
                                  "the final episode'. The clauses are COEXTENSIVE BY "
                                  "CONSTRUCTION and the FALSE class is EMPTY, so the mechanism "
                                  "form does not define a column"),
        "the_proof_is_one_line": ("p = |{e in E2 : e <= m_H}| / L2, and the set-membership drop "
                                  "rule puts m_H in E2. So the numerator equals L2 IFF no listed "
                                  "episode exceeds m_H, IFF m_H = max(E2) = F2 -- which IS 'left "
                                  "at the final episode'. Neither clause can hold without the "
                                  "other. BUT THE CHAIN HAS THREE LINKS AND ONLY THE FIRST IS "
                                  "CONSTRUCTION (0085 Sec 4) -- see "
                                  "the_chain_has_THREE_links_only_two_are_construction"),
        "the_chain_has_THREE_links_only_two_are_construction": third_link,
        "totals_not_a_split": ("decisions/0083 Sec 2 -- the p = 1.0 counts are reported AS "
                               "TOTALS. 1,246 and 1,230 are correct counts and both arms "
                               "reproduce them, but they are ONE CLASS COUNTED TWICE, NOT TWO "
                               "CLASSES SUMMED. Citing them as evidence that the column "
                               "separates anything is a WITHDRAWN ARGUMENT (CLAUDE.md, third "
                               "blindness class; registered at src/step7_register.py "
                               "GROUNDS_WITHDRAWN['0083 SS2'])"),
        "expected_totals_from_the_ruling": {"position5_APPLY": 1246,
                                            "post_liveness_APPLY": 1230},
        "expected_emptiness_cells_from_the_ruling_BOTH_POPULATIONS": {
            "source": ("decisions/0085 Sec 3, Red Team blocker B2 -- the emptiness is emitted "
                       "on BOTH populations at BOTH positions, four cells each. This is "
                       "CLAUDE.md's standing both-populations rule, not a new requirement. "
                       "One arm emitted APPLY only and 1,056 appeared nowhere in its "
                       "deliverable, while the whole ground for keeping the column is that an "
                       "emptiness asserted in prose and never emitted cannot be checked"),
            "APPLY_position5": "1,246 / 0 / 0 / 0",
            "APPLY_post_liveness": "1,230 / 0 / 0 / 0",
            "DERIV_position5": "1,072 / 0 / 0 / 0",
            "DERIV_post_liveness": "1,056 / 0 / 0 / 0",
        },
        "totals_by_population_and_position": pab_tot,
        "coextensivity_check_the_emptiness_is_EMITTED_not_asserted_in_prose": {
            "why": ("an emptiness asserted in prose and never emitted cannot be checked "
                    "(decisions/0083 Sec 2). Both mechanisms are computed separately and the "
                    "four cells are reported. The FALSE class stays empty across Step 13's W "
                    "grid because the rank form and set membership are both W-invariant, so a "
                    "non-empty cell anywhere means one of them has broken"),
            "populations_required": ("FOUR, by decisions/0085 Sec 3 -- APPLY position 5, APPLY "
                                     "post-liveness, DERIV position 5, DERIV post-liveness. "
                                     "Emitting APPLY alone leaves the DERIV emptiness asserted "
                                     "in prose and never emitted, which is the one thing the "
                                     "column is kept to prevent"),
            "by_population_and_position": pab_coext,
            "all_populations_agree_row_for_row":
                all(v["empty_classes_are_empty"] for v in pab_coext.values()),
            "coverage": {
                "why": ("an empty result and a clean result are the same value and only the "
                        "control knows which it produced -- so each cell states how many rows "
                        "it LOOKED AT, on each of the four required populations"),
                "rows_examined_per_population": {nm: int(v["rows_examined"])
                                                 for nm, v in pab_coext.items()},
                "populations_examined": len(pab_coext),
                "looked_nowhere": any(v["rows_examined"] == 0 for v in pab_coext.values()),
            },
        },
        "a_SECOND_fact_DATA_not_construction": {
            "statement": ("frame shows with any S2 numbering gap -- if zero, E2 = {1..L2} "
                          "everywhere and the rank form reduces to m_H / L2"),
            "shows_examined": n_shows,
            "shows_with_an_S2_numbering_gap": int(gap_shows),
            "why_stated_separately": ("this one is DATA and could be false on another frame; "
                                      "the coextensivity above would still hold. Collapsing "
                                      "them would make a construction argument look like a "
                                      "frame accident (decisions/0083 Sec 2)"),
        },
        "why_the_column_is_KEPT": ("not because it decomposes the spike -- it does not -- but "
                                   "because Step 10 publishes the abandonment distribution off "
                                   "abandonment_point_p and needs the spike LABELLED, and "
                                   "because an emptiness asserted in prose and never emitted "
                                   "cannot be checked"),
    }

    # --- Continued-and-silent, the count silent_at_tau1 exists to preserve --
    req["continued_and_silent"] = {
        "why_it_is_here": ("decisions/0081 -- `live` is TRUE for every Continued pair "
                           "REGARDLESS of silence, because the liveness rule's second conjunct "
                           "is NOT Continued. The Continued-and-silent count is therefore not "
                           "recoverable from `live` and `outcome`, and silent_at_tau1 is "
                           "restored to the table so it can be recomputed from Step 8's own "
                           "output. It is ALSO emitted here as an aggregate so the figure "
                           "survives independently of the column"),
        "definition": ("Continued pairs whose account shows NO insertion instant > tau1 -- the "
                       "silence test, strict, evidence restricted to records dated before "
                       "tau_pull"),
        "published_figures_it_reproduces_BOTH_NOT_ONE": {
            "silence_test_alone_APPLY": 1355,
            "NOT_Continued_conjunct_spares_APPLY": 652,
            "line_6_exclusions_APPLY": 703,
            "ruling": ("decisions/0085 Sec 5, Red Team third pass -- 703 IS NOT THE MARGINAL "
                       "COST OF THE SILENCE TEST. The silence test alone excludes 1,355 on "
                       "APPLY and the NOT Continued conjunct spares 652, so 1,355 - 652 = 703. "
                       "One arm published 652 and not 1,355. Derivable, so not a defect -- but "
                       "1,355 is the figure that makes line 6 readable as a marginal cost, and "
                       "a reader holding only 652 cannot recover it without knowing to add. "
                       "BOTH publish, on BOTH populations, WITH THE IDENTITY STATED"),
        },
        "by_population": {
            nm: {"continued": int((msk & K["contd"]).sum()),
                 "continued_and_silent_at_tau1": int((msk & K["contd"] & K["silent"]).sum()),
                 "silent_at_tau1_all_rows": int((msk & K["silent"]).sum()),
                 "silent_and_not_continued_the_liveness_exclusions":
                     int((msk & K["silent"] & ~K["contd"]).sum())}
            for nm, msk in (("APPLY_position5", line5), ("DERIV_position5", d5))},
        "LINE_6_MARGINAL_DECOMPOSITION": {
            "why": ("decisions/0085 Sec 5 -- line 6 removes 703 pairs on APPLY, and a reader "
                    "given only that number reads it as the cost of the silence test. It is "
                    "not. The silence test ALONE would remove every silent pair; the rule's "
                    "second conjunct (NOT Continued) then hands back every Continued one. The "
                    "decomposition is what makes line 6 readable as a marginal cost"),
            "identity": ("silence_test_alone - NOT_Continued_conjunct_spares = "
                         "line_6_exclusions"),
            "by_population": {
                nm: {
                    "silence_test_alone_would_exclude": int((msk & K["silent"]).sum()),
                    "NOT_Continued_conjunct_spares": int((msk & K["silent"] & K["contd"]).sum()),
                    "line_6_exclusions": int((msk & K["silent"] & ~K["contd"]).sum()),
                    "identity_holds": (int((msk & K["silent"]).sum())
                                       - int((msk & K["silent"] & K["contd"]).sum())
                                       == int((msk & K["silent"] & ~K["contd"]).sum())),
                    "rows_examined": int(msk.sum()),
                }
                for nm, msk in (("APPLY_position5", line5), ("DERIV_position5", d5))},
            "coverage": ("both populations, every position-5 row of each; neither cell is an "
                         "empty look"),
        },
        "what_it_measures": ("the size of the outcome-conditioning at waterfall line 6 -- the "
                             "pairs the rule's second conjunct SAVES from exclusion. It closed "
                             "the rule objection at 0063 Sec 1 and publishes as a Step 14 "
                             "limitation"),
    }

    # --- D2, split THREE ways ----------------------------------------------
    first_s2 = np.where(loc_ok, s2_ts[np.clip(start, 0, len(s2_ts) - 1)],
                        np.iinfo(np.int64).max)
    neg = loc_ok & (first_s2 < t0_mid)
    d2 = {}
    for nm, msk, base in (("line1_220107", line1, line1),
                          ("position3_220107", line3, line3),
                          ("position4_201900", line4, line4),
                          ("APPLY_position5_196654", line5, line5),
                          ("APPLY_position6_post_liveness_195951", line6, line6),
                          ("DERIV_position5_147370", d5, d5),
                          ("DERIV_position6_post_liveness_147271", d6, d6)):
        tot = int(base.sum())
        d2[nm] = {
            "population": nm, "n": tot,
            "negative_lag_pairs": int((msk & neg).sum()),
            "share_pct": 100.0 * int((msk & neg).sum()) / tot,
            "S2_finale_term_binds": int((msk & neg & (binds == "finale")).sum()),
            "S1_completion_term_binds": int((msk & neg & (binds == "s1")).sum()),
            "BOTH_terms_bind_tie": int((msk & neg & (binds == "tie")).sum()),
            # 0070 ruling 5's own figure -- ALL pairs whose two max() terms bind,
            # not only the negative-lag ones. THIS is the 168, and it is measured
            # on every population rather than published once with none named.
            "BOTH_terms_bind_tie_ALL_pairs_not_only_negative_lag":
                int((msk & (binds == "tie")).sum()),
        }
    _tie_by_pop = {k: v["BOTH_terms_bind_tie_ALL_pairs_not_only_negative_lag"]
                   for k, v in d2.items()}
    req["D2_negative_lag"] = {
        "split": "THREE categories -- finale binds, S1 completion binds, BOTH bind "
                 "(decisions/0070 ruling 5). A tie is its own category, not a tiebreak",
        "THE_168_MEASURED_ON_EVERY_POPULATION": {
            "ruling": ("task-sheet.md Step 8, D2 bullet, as amended by Red Team's SEVENTH pass "
                       "finding N2: 0070 ruling 5 published '168 pairs have both terms binding' "
                       "WITH NO POPULATION. STATE THE POPULATION AT THE POINT OF USE AND "
                       "MEASURE IT ON BOTH. This is the standing provenance rule (0047, 0078 "
                       "Sec 2), not a new requirement"),
            "by_population": _tie_by_pop,
            "unit": "user-show PAIRS whose T0 = max(S2 finale, S1 completion) has both terms "
                    "binding on the same UTC day",
            "THIS_ARMS_OWN_DEFECT_CORRECTED": (
                "this arm's -r4 build published the integer 168 in TWO deliverables under TWO "
                "populations -- `tie_pairs_in_line1` on waterfall line 1 (220,107) in "
                "step8-waterfall-b.md, and `rows_where_the_two_terms_are_the_same_date` on the "
                "APPLY position-5 row set (196,654) in step8-invariants-b.md -- with no line "
                "reconciling them. The populations differ by 23,453 pairs. Reported here rather "
                "than silently repaired"),
            "AND_THE_REVIEW_PREMISE_IS_MEASURABLY_FALSE_ON_THIS_DATA": (
                "the finding as put to this arm is '168 cannot be correct on both'. MEASURED: "
                "IT IS CORRECT ON BOTH. Every one of the tie pairs survives positions 2 through "
                "6 on APPLY, so the count is 168 on line 1, 168 at position 3, 168 at position "
                "4, 168 at position 5 and 168 post-liveness. The two figures agreed because the "
                "quantity is invariant across the APPLY chain, NOT because either was measured "
                "wrongly. THE DEFECT IS REAL AND IS THE OTHER HALF OF THE FINDING: neither "
                "figure NAMED its population, and neither had ever been measured on DERIV -- "
                "where it is NOT 168. Reported, not reconciled: the arithmetic claim in the "
                "finding is contradicted by this build, the provenance claim is upheld"),
            "the_number_that_was_never_measured": (
                "DERIV. The tie count on DERIV position 5 is emitted in by_population above and "
                "differs from 168, which is what makes the missing population label load-bearing "
                "rather than cosmetic"),
            "invariant_5_reports_the_same_quantity_on_its_own_population": (
                "step8-invariants-b.md invariant 5's "
                "`rows_where_the_two_terms_are_the_same_date` is this quantity on the APPLY "
                "position-5 row set, computed from the INDEPENDENTLY recomputed S1 completion "
                "date rather than from the pipeline's `binds` label. Agreement between the two "
                "is therefore a cross-check and not a restatement; it is asserted at stage 3"),
        },
        "by_population": d2,
        "reading": ("S1-term negative lags are the test of the first-pass choice and should "
                    "be small; S2-finale-term negative lags are the normal case for anyone "
                    "who watched a weekly season while it aired"),
    }

    # --- D3' is per arm, already in R["per_arm"]; the 3,440 restated --------
    req["D3prime"] = {
        "per_arm": {pop: {k: v["D3prime"] for k, v in per_arm[pop].items()}
                    for pop in ("APPLY", "DERIV")},
        "the_3440": {
            "count": 3440,
            "label": "A COUNT, NOT A RATE",
            "population": ("the Step 5 UNCENSORED CLEAN-RECORD ESTIMATION SAMPLE of 128,099 "
                           "-- NOT APPLY and NOT DERIV. Measured at decisions/0034 Sec 3, "
                           "where the Started-and-left group is 17,420 before the amendment "
                           "and 15,174 after"),
            "why_a_floor": ("that sample excludes what the Step 5 waterfall drops and is not "
                            "right-censored, which is why Step 14 calls it a floor"),
            "exposure_weighting": ("weighted by SHOW RECENCY: 'at any point before tau_pull' "
                                   "gives a 2016 title about ten years of observation and a "
                                   "2025 title about eight months, so it is an "
                                   "exposure-weighted count and not a rate"),
            "restated_not_recomputed": ("decisions/0069 item 1 and task-sheet.md forbid "
                                        "reporting it against APPLY or DERIV"),
        },
    }

    # --- D8 ----------------------------------------------------------------
    tau1, tau2 = K["tau1"], K["tau2"]
    any_in_horizon = nAH > nA
    cont_over_horizon = K["f2_in_AH"] & (nAH >= THR2a[s_idx])
    d8 = {}
    for nm, msk in (("APPLY_position5", line5), ("APPLY_position6_post_liveness", line6),
                    ("DERIV_position5", d5), ("DERIV_position6_post_liveness", d6)):
        ns = msk & K["never"]
        n = int(ns.sum())
        d8[nm] = {"never_started_n": n,
                  "i_any_S2_episode_in_tau1_to_tau2": int((ns & any_in_horizon).sum()),
                  "i_share_pct": 100.0 * int((ns & any_in_horizon).sum()) / max(n, 1),
                  "ii_satisfies_the_Continued_condition_over_the_horizon":
                      int((ns & cont_over_horizon).sum()),
                  "ii_share_pct": 100.0 * int((ns & cont_over_horizon).sum()) / max(n, 1)}
    req["D8_never_started_post_window"] = {
        "measured_over": "[tau1, tau1 + H) = [tau1, tau2), H = 91 days -- NOT to the pull date",
        "by_population_and_position": d8,
        "direction": "DOWN on the headline",
        "note": ("the spec does not say whether D8 sits pre- or post-liveness, so both are "
                 "reported and labelled. D8(ii) is the only bound on the never-started "
                 "boundary and its size is Step 14 ledger item 10"),
    }

    # --- D4 ----------------------------------------------------------------
    # has_s3 / has_any_s2_record are computed once, above, and are also emitted
    # as the table column `has_s3_or_later_evidence` (0077 Sec 3).
    d4mask = K["never"] & has_s3 & ~has_any_s2_record
    d4 = {}
    for nm, msk in (("APPLY_position5", line5), ("APPLY_position6_post_liveness", line6),
                    ("DERIV_position5", d5), ("DERIV_position6_post_liveness", d6)):
        ns = int((msk & K["never"]).sum())
        d4[nm] = {"never_started_n": ns, "S3_without_S2_pairs": int((msk & d4mask).sum()),
                  "share_of_never_started_pct": 100.0 * int((msk & d4mask).sum()) / max(ns, 1)}
    req["D4_S3_without_S2"] = {
        "definition": ("pairs scored Never started that carry S3-or-later episode records on "
                       "that show and NO S2 episode record at all"),
        "by_population_and_position": d4,
        "direction": "INFLATES Never started; Step 9 bounds it and publishes it ALONGSIDE",
        "emitted_here_because": ("Step 8 holds the episode-level evidence and Step 9 does "
                                 "not; leaving it out forces a second definition "
                                 "(decisions/0070 ruling 7)"),
    }

    # --- right-censoring, two lines ---------------------------------------
    req["right_censoring_two_lines"] = {
        "population_censored": "the POSITION-4 output, 201,900 (the mandated order)",
        "line_a_max_W_91_term": int((line4 & ~K["term1"]).sum()),
        "line_b_incremental_plus_H_term": int((line4 & K["term1"] & ~K["d10"]).sum()),
        "total": int((line4 & ~K["d10"]).sum()),
        "direction_line_a": "UP on the never-started share",
        "direction_line_b": "UP on the never-started share",
        "why_two_lines": ("a single combined figure would hide the price of H inside a "
                          "removal that predates it (D10)"),
    }

    # --- per-bucket D12 counts --------------------------------------------
    cad = frame.cadence_bucket.values
    bnd = frame.cadence_boundary_distance_days.values
    req["D12_cadence_buckets"] = {
        "buckets": {bk: {"shows": int((cad == bk).sum()),
                         "pairs_position4": int((line4 & (cad[s_idx] == bk)).sum()),
                         "pairs_APPLY_position5": int((line5 & (cad[s_idx] == bk)).sum()),
                         "pairs_DERIV_position5": int((d5 & (cad[s_idx] == bk)).sum())}
                    for bk in ["C0", "C1", "C2", "C3", "C4"]},
        "shows_within_1_day_of_a_bucket_boundary":
            int(np.nansum(np.abs(pd.to_numeric(bnd, errors="coerce").astype(float)) <= 1)),
        "shows_examined": n_shows,
        "coverage_note": "C0 = 0 of 1,138 shows examined, a measured zero",
    }

    # --- metadata disagreement --------------------------------------------
    dis = {}
    for c in ["s1_count_disagreement", "s2_count_disagreement",
              "s1_aired_lt_listed", "s2_aired_lt_listed"]:
        v = frame[c].values.astype(bool)
        dis[c] = {"shows": int(v.sum()),
                  "pairs_position4": int((line4 & v[s_idx]).sum())}
    req["metadata_disagreement"] = {
        "shows_examined": n_shows,
        "flags": dis,
        "s2_aired_lt_listed_direction": ("a listed-but-unaired S2 episode raises L2, which "
                                         "tightens ceil(0.90 x L2) and pushes real completers "
                                         "out of Continued into Started-and-left -- it "
                                         "OVERSTATES abandonment; where F2 never aired, "
                                         "Continued is unreachable on that show"),
        "coverage_note": ("every flag is 0 of 1,138 shows EXAMINED, not 0 because nothing "
                          "was looked at"),
    }

    # --- pull_date and fetch dates ----------------------------------------
    fetched = []
    for line in open(ROOT / "processed" / "step4" / "pull_ledger.jsonl"):
        d = json.loads(line)
        if d.get("first_page_fetched_at"):
            fetched.append((d["first_page_fetched_at"], d.get("last_page_fetched_at")))
    firsts = sorted(x[0] for x in fetched)
    lasts = sorted(x[1] for x in fetched if x[1])
    req["pull_date_and_fetch_window"] = {
        "pull_date": "2026-08-11", "tau_pull": "2026-08-11T00:00:00Z",
        "earliest_per_user_fetch": firsts[0], "latest_per_user_fetch": lasts[-1],
        "users_with_a_fetch_recorded": len(fetched),
        "records_discarded_for_watched_at_ge_tau_pull":
            st1["D11"]["records_discarded_watched_at_ge_tau_pull"],
        "of_which_in_frame_S1_or_S2_episode_records":
            st1["records"]["in_frame_S1_S2_episode_records_dropped_by_D11"],
        "constraint": "tau_pull <= the earliest per-user fetch instant",
        "note": ("the discarded tail is about one day of activity for early-fetched users "
                 "and about two for late-fetched ones; it is not evenly distributed"),
    }

    # --- the D11 open question, with its downstream effect measured --------
    _dq = st1["s1_completion"]["D11_open_question"]
    _cmp = _dq["completer_set_comparison_READING_B_vs_READING_C"]
    req["D11_open_question"] = {
        "line_1_as_ruled": 220107,
        "line_1_if_D11_is_applied_to_the_S1_completion_walk_too":
            _dq["S1_completer_pairs_if_D11_applied_to_S1_too"],
        "pairs_affected": _cmp["in_B_and_NOT_in_C_pairs_that_stop_being_completers"],
        "completer_set_comparison": _cmp,
        "completion_dates_that_move_among_the_surviving_pairs":
            _cmp["of_those_whose_first_pass_completion_DATE_MOVES"],
        "all_four_are_removed_at_position_5_under_either_reading":
            bool((~line5[comp_post_cutoff]).all()),
        "lines_4_to_7_are_identical_under_both_readings": True,
        "why": ("their first-pass completion instant is at or after tau_pull, so T0 is at or "
                "after 2026-08-10 and D10 removes them at position 5. Under the other "
                "reading they never reach position 4 at all"),
        "status": "decisions/0068 rules the base at 220,107 AND records this as OPEN",
    }

    R["required_counts"] = req

    # =====================================================================
    # EMITTED BEYOND THE REQUIRED LIST -- because Step 9 and Step 10 would
    # otherwise have to rebuild them, and two definitions of one figure is the
    # defect this study has hit most often (0058, 0061, 0062).
    # =====================================================================
    channel = (mx > K["tau1"]) & (mx < K["tau2"])     # last insertion inside (tau1, tau2)
    extras = {"_why": ("not required by Step 8. Emitted because Step 9's bound endpoints and "
                       "Step 10's residual are built from them, and rebuilding them "
                       "downstream would be a second definition")}
    for pop, p5mask, p6mask in (("APPLY", line5, line6), ("DERIV", d5, d6)):
        live = p6mask
        ch = live & ~K["contd"] & channel
        extras[pop] = {
            "position5_n": int(p5mask.sum()),
            "position7_n": int(p6mask.sum()),
            "states_position5": {"never_started": int((p5mask & K["never"]).sum()),
                                 "continued": int((p5mask & K["contd"]).sum()),
                                 "started_and_left": int((p5mask & K["sal"]).sum())},
            "liveness_exclusions": {
                "never_started": int((p5mask & K["notlive"] & K["never"]).sum()),
                "started_and_left": int((p5mask & K["notlive"] & K["sal"]).sum()),
                "accounts": int(len(np.unique(u_idx[p5mask & K["notlive"]]))),
            },
            "insertion_dormancy_channel_pairs": {
                "definition": ("RETAINED pairs, NOT Continued, live only by an insertion "
                               "after tau1, whose LAST insertion falls inside the open "
                               "window (tau1, tau2)"),
                "started_and_left": int((ch & K["sal"]).sum()),
                "never_started": int((ch & K["never"]).sum()),
                "why_the_never_started_component_does_not_widen_that_bound":
                    ("the never-started null |A| = 0 is read at tau1 and every one of these "
                     "pairs has an insertion AFTER tau1, so its null is OBSERVED, not "
                     "conceded. The started-and-left pairs differ because the Continued "
                     "condition they negate is read at tau2 and they are dormant before it"),
            },
            "p_equals_1_residual_post_position_7":
                int((p6mask & K["sal"] & (p_val >= 1.0)).sum()),
        }
    extras["scope_qualifier_of_the_Step_9_bound"] = (
        "covering with respect to INSERTION-DORMANCY, exhaustively; open only across "
        "CHANNEL CLASSES (D4, D9). D4 and D9 publish alongside and are never folded in. "
        "Step 8 does not compute the bound, but it produces the position-6 population the "
        "bound is stated on, so any table or note carrying the bound carries this qualifier "
        "(decisions/0062)")

    # the account base: absent accounts are ABSENT, not empty
    outc: dict = {}
    for line in open(ROOT / "processed" / "step4" / "pull_ledger.jsonl"):
        o = json.loads(line).get("outcome")
        outc[o] = outc.get(o, 0) + 1
    extras["account_base"] = {
        "accounts_in_the_sweep": int(n_users),
        "accounts_reaching_the_position_5_population": int(len(np.unique(u_idx[line5]))),
        "pull_ledger_outcomes": outc,
        "note": ("accounts that were skipped, discarded over tolerance or never attempted are "
                 "ABSENT, not empty. CLAUDE.md requires an access_denied user to stay "
                 "distinguishable downstream, because a skipped user silently read as empty "
                 "becomes a false 'never started' in the headline. No such account "
                 "contributes a row to this table"),
    }
    R["emitted_beyond_the_required_list"] = extras

    np.savez(OUT / "masks.npz", line1=line1, line2=line2, line3=line3, line4=line4,
             line4_step5=line4_step5, line5=line5, line6=line6, deriv5=d5, deriv6=d6,
             never=K["never"], contd=K["contd"], sal=K["sal"], notlive=K["notlive"],
             nA=nA, nAH=nAH, p=p_val, u_idx=u_idx, s_idx=s_idx, comp_pair=comp_pair,
             t0_mid=t0_mid, tau1=tau1, tau2=tau2, binds=binds,
             has_s3=has_s3, has_any_s2_record=has_any_s2_record,
             silent=K["silent"], rank_saturated=rank_saturated, p_is_one=p_is_one,
             in_a=in_a_u[u_idx], in_b=in_b_u[u_idx], m_H=m_H,
             first_s2=first_s2, loc_ok=loc_ok, comp_date_mid=comp_date_mid)

    # =====================================================================
    # PROVENANCE -- decisions/0078 and 0079 Sec 2. EVERY count group, EVERY
    # waterfall figure and EVERY per-arm result names the build it was measured
    # on. Partial application is worse than none: two labelled figures imply the
    # rest did not need it.
    # =====================================================================
    R["provenance"] = provenance_block()
    for k, v in R.items():
        if isinstance(v, dict) and k != "provenance":
            stamp(v)
    for v in req.values():
        if isinstance(v, dict):
            stamp(v)
    for pop in ("APPLY", "DERIV"):
        for arm in W_ARMS:
            stamp(per_arm[pop][str(arm)])
    for arm in W_ARMS:
        stamp(censor_air[str(arm)])

    R["elapsed_s"] = time.time() - t
    (OUT / "results.json").write_text(json.dumps(R, indent=2, default=str))
    print(json.dumps({k: R[k] for k in ("waterfall_APPLY", "waterfall_DERIV")},
                     indent=2, default=str))
    a = per_arm["APPLY"]["108"]
    d = per_arm["DERIV"]["108"]
    print(f"\nAPPLY n={a['position5_n']:,} excluded {a['liveness_excluded']} "
          f"= {a['liveness_excluded_never_started']} NS + "
          f"{a['liveness_excluded_started_and_left']} SL from "
          f"{a['accounts_supplying_exclusions']} accounts")
    print(f"DERIV n={d['position5_n']:,} excluded {d['liveness_excluded']} "
          f"= {d['liveness_excluded_never_started']} NS + "
          f"{d['liveness_excluded_started_and_left']} SL from "
          f"{d['accounts_supplying_exclusions']} accounts")
    print(f"({time.time()-t:.1f}s)")


if __name__ == "__main__":
    main()
