"""Step 8, namespace `a`. STAGE 3 of 5 — positions 6 and 7 at W = 108, and the analysis table.

GATE. Adopts nothing. Zero API calls.

Position 6 is the liveness rule (ALT-BROAD, approved 0064). Position 7 is outcome assignment at
TWO instants (0034) and removes no rows -- it annotates.

The 703 line is a POPULATION RECONCILIATION, not an invariant (0068, 0047): 703 expected on
APPLY = 196,654 (604 never-started + 99 started-and-left, 216 accounts), 99 on DERIV = 147,370
(0 + 99, 73 accounts). 604 is ALT's superseded answer and 793 is ALT-MATCHED's withdrawn one;
either would mean a superseded rule had been implemented. A mismatch is treated as a population
defect before an implementation one -- and, this being a gate, it is reported rather than
reconciled.

THE TABLE IS THE POSITION-5 ROW SET -- 196,654 rows on APPLY -- WITH `live` AND `outcome` AS
COLUMNS (Human Lead ruling, decisions/0074 ruling 1). Both readings of "one row per pair" give
identical counts, so this is a ruling and not a correction: rulings 0070/1 and 0070/7 established
that downstream CONSUMES rather than REBUILDS, and carrying the liveness result as a column is
that principle applied to the row set. Under the position-7 reading anything needing the excluded
pairs reconstructs them, and a reconstruction that agrees today is still a second definition
tomorrow -- invisible to the dual diff, because both instances would rebuild the same way.

THE COLUMN NAMES ARE FIXED BY decisions/0077 AND THE SET IS THE 89 ENUMERATED NAMES OF
decisions/0080 as extended by 0081 (`silent_at_tau1` restored) and 0082 (`p_at_bound` added). An
earlier dual run produced 88 against 87 for the same contents, all of it naming, and Step 8b
defines the schema Steps 9-13 write into DIRECTLY (0066), so the divergence would have been
inherited. Both arms' extra columns are kept: `has_s3_or_later_evidence` (D4 reads it) and
`s1_completion_used_a_post_cutoff_record` (the open D11-at-position-3 question reads it).

Output: processed/step8/a/analysis_table.csv.gz   (position-5 rows, one per user-show pair)
        processed/step8/a/position5_table.npz     (working table for the diagnostics stage)
        processed/step8/a/outcomes.json
"""
import json
import os
import re

import numpy as np
import pandas as pd

import step8_a_lib as lib

ROOT = "/Users/alyanashantel/Documents/season2-study"
P2 = os.path.join(ROOT, "processed/step2")
P4 = os.path.join(ROOT, "processed/step4")
P5 = os.path.join(ROOT, "processed/step5")
OUT = os.path.join(ROOT, "processed/step8/a")

W = 108
H = 91
DAY = 86400

# THE COLUMN SET IS ENUMERATED, NOT COUNTED -- 89 NAMES, EXACTLY THESE. Human Lead ruling,
# decisions/0080, replacing decisions/0077 SS3's COUNT; extended to 88 by decisions/0081, which
# RESTORES `silent_at_tau1`, and to 89 by decisions/0082, which ADDS `p_at_bound`. The arms
# converged on the 87 names on the previous run, but CONVERGED IS NOT SPECIFIED and nothing
# prevents the next run from diverging; Step 8b's schema is built on this vocabulary, with Steps
# 9-13 writing into it directly and no conversion layer (0066), so it is fixed BEFORE the schema
# exists. Transcribed from task-sheet.md Step 8. Emit exactly these, no more and no fewer.
# Two names stay DROPPED and both are free: `f2_in_A_H` (derivable as max_episode_in_A_H == s2_F)
# and `max_episode_in_A` (read by nothing downstream).
SPEC_COLUMNS = [
    "abandonment_point_p", "action_count_s1_checkin", "action_count_s1_other",
    "action_count_s1_scrobble", "action_count_s1_watch", "action_count_s2_checkin",
    "action_count_s2_other", "action_count_s2_scrobble", "action_count_s2_watch", "air_period",
    "cadence_boundary_distance_days", "cadence_bucket", "completers_per_year",
    "discovered_channel_a", "discovered_channel_b", "e1_internal_gap", "e1_starts_at_1",
    "e2_internal_gap", "e2_starts_at_1", "exclusion", "gap_days", "has_s3_or_later_evidence",
    "in_apply", "in_deriv", "live", "max_episode_in_A_H", "max_season_number", "n_A", "n_A_H",
    "outcome", "p_at_bound", "pool_completers", "pool_completers_proxy", "s1_E", "s1_F", "s1_L",
    "s1_aired_episodes_reported", "s1_aired_lt_listed", "s1_completion_date",
    "s1_completion_used_a_post_cutoff_record", "s1_count_disagreement",
    "s1_episode_count_reported", "s1_exposure_years", "s1_finale_date", "s1_premiere_date",
    "s1_season_first_aired", "s1_total_runtime", "s2_E", "s2_F", "s2_L",
    "s2_aired_episodes_reported", "s2_aired_lt_listed", "s2_count_disagreement",
    "s2_episode_count_reported", "s2_finale_date", "s2_finale_year", "s2_premiere_date",
    "s2_season_first_aired", "s2_span_days", "s2_total_runtime", "s2_weekly_span_days",
    "season_numbers", "seasons_returned", "show_aired_episodes", "show_airs_day",
    "show_certification", "show_comment_count", "show_country", "show_first_aired", "show_genres",
    "show_language", "show_languages", "show_rating", "show_runtime", "show_status",
    "show_subgenres", "show_trakt_id", "show_votes", "show_year", "silent_at_tau1",
    "size_quintile", "size_quintile_per_year", "size_quintile_raw_count", "t0_binding_term",
    "t0_date", "tau1", "tau2", "title", "user_idx",
]
assert len(SPEC_COLUMNS) == len(set(SPEC_COLUMNS)) == 89


def spec_columns_from_disk():
    """READ THE ENUMERATION OFF task-sheet.md AND ASSERT THE TRANSCRIPTION AGAINST IT.

    Red Team's fourth pass (decisions/0087, F5-F9 item F6) found this arm's column check weaker
    than its own prose: the report said it asserts set equality "against the spec's list" while
    the code asserted against the HAND TRANSCRIPTION above and never opened task-sheet.md. A hand
    transcription is a second copy of the enumeration, so a propagation change to the spec would
    not reach it -- and THE DUAL DIFF CANNOT CATCH A PROPAGATION FAILURE, because both arms would
    have to make the same mistake to hide it and only one has to make it to keep it. F6 is a
    carried limitation and not a ruling; this closes it rather than restating it.

    A parse that finds nothing must FAIL rather than pass (CLAUDE.md), so the extracted count is
    asserted and its coverage is returned for publication.
    """
    path = os.path.join(ROOT, "task-sheet.md")
    txt = open(path).read()
    anchor = txt.index("THE COLUMN SET IS ENUMERATED, NOT COUNTED")
    s = txt.index("`abandonment_point_p`", anchor)
    e = txt.index("`user_idx`", s) + len("`user_idx`")
    found = [t for t in re.findall(r"`([A-Za-z0-9_]+)`", txt[s:e]) if not t.isdigit()]
    uniq = sorted(set(found))
    assert len(uniq) > 0, (
        "the column enumeration was not found in task-sheet.md: this check would otherwise pass "
        "by looking nowhere")
    return uniq, {"source": "task-sheet.md, the 0080/0081/0082 enumeration block, READ AT RUN "
                            "TIME -- not the hand transcription in this file",
                  "names_parsed": len(found), "distinct_names_parsed": len(uniq),
                  "matches_the_transcription_in_this_file": sorted(uniq) == sorted(SPEC_COLUMNS),
                  "why_it_is_read_from_disk": "a hand transcription is a second copy of the "
                                              "enumeration and a propagation change to the spec "
                                              "would not reach it; the dual diff cannot catch a "
                                              "propagation failure, so only a check that opens "
                                              "the spec file can"}


SPEC_COLUMNS_ON_DISK, SPEC_COLUMNS_SOURCE = spec_columns_from_disk()
assert set(SPEC_COLUMNS_ON_DISK) == set(SPEC_COLUMNS), (
    "the transcribed column set disagrees with task-sheet.md's enumeration: "
    f"only in the spec {sorted(set(SPEC_COLUMNS_ON_DISK) - set(SPEC_COLUMNS))}, "
    f"only in this file {sorted(set(SPEC_COLUMNS) - set(SPEC_COLUMNS_ON_DISK))}")


def main():
    scan = np.load(os.path.join(OUT, "scan.npz"))
    positions = np.load(os.path.join(OUT, "positions.npz"))
    frame = pd.read_csv(os.path.join(P2, "frame.csv"))
    a = lib.Arms(scan, positions, frame, H=H)
    r = a.run(W)

    pos5, pos5d = r["pos5"], r["pos5_deriv"]
    assert int(pos5.sum()) == 196654 and int(pos5d.sum()) == 147370

    # D11 is provably inert on A and A_H: D10 forces tau2 <= tau_pull on every retained pair
    assert int((r["tau2"][pos5] > lib.TAU_PULL).sum()) == 0, "tau2 beyond tau_pull"

    # ---- position 6: liveness ---------------------------------------------------------------
    excl = pos5 & r["not_live"]
    excl_d = pos5d & r["not_live"]
    pos6 = pos5 & ~r["not_live"]
    pos6d = pos5d & ~r["not_live"]

    def brk(mask):
        return {"total": int(mask.sum()),
                "never_started": int((mask & r["never"]).sum()),
                "started_and_left": int((mask & r["left"]).sum()),
                "continued": int((mask & r["continued"]).sum()),
                "accounts": int(np.unique(a.pair_user[mask]).size)}

    # how the two conjuncts select, on APPLY
    conj2 = pos5 & ~r["continued"]
    conj_then_1 = conj2 & r["silent"]

    # the same rule with the D11 restriction on the evidence lifted, measured not assumed
    silent_un = a.last_inst_unrestricted <= r["tau1"]
    excl_un = pos5 & silent_un & ~r["continued"]

    # ---- position 7: outcome assignment ------------------------------------------------------
    def outcomes(mask):
        return {"never_started": int((mask & r["never"]).sum()),
                "started_and_left": int((mask & r["left"]).sum()),
                "continued": int((mask & r["continued"]).sum()),
                "total": int(mask.sum())}

    res = {
        "step": 8, "instance": "a", "stage": 3, "api_calls": 0,
        "build": lib.build_record(),
        "provenance_note": "EVERY COUNT IN THIS FILE WAS MEASURED ON BUILD " + lib.BUILD_TAG
                           + " (decisions/0079 B6, extending 0078).",
        "W_days": W, "H_days": H,
        "rule": "NOT LIVE iff (no insertion instant > tau1) AND (NOT Continued); evidence "
                "restricted to records dated before tau_pull",
        "position_5_APPLY": int(pos5.sum()),
        "position_5_DERIV": int(pos5d.sum()),
        "position_6_liveness": {
            "APPLY": {"population_entering": int(pos5.sum()),
                      "excluded": brk(excl),
                      "retained": int(pos6.sum()),
                      "expected_excluded": 703},
            "DERIV": {"population_entering": int(pos5d.sum()),
                      "excluded": brk(excl_d),
                      "retained": int(pos6d.sum()),
                      "expected_excluded": 99},
            "conjunct_selection_APPLY": {
                "start": int(pos5.sum()),
                "after_conjunct_2_NOT_continued": int(conj2.sum()),
                "after_conjunct_1_silent_at_tau1": int(conj_then_1.sum()),
            },
            "evidence_scope_check": {
                "excluded_with_D11_restriction_APPLY": int(excl.sum()),
                "excluded_without_the_restriction_APPLY": int(excl_un.sum()),
                "note": "0070 ruling 2 requires the restriction; measured inert here as it was "
                        "when the ruling was made",
            },
        },
        "position_7_outcome_assignment": {
            "rows_removed": 0,
            "APPLY_post_liveness": outcomes(pos6),
            "DERIV_post_liveness": outcomes(pos6d),
            "APPLY_at_position_5_outcome_conditional_view": outcomes(pos5),
            "DERIV_at_position_5_outcome_conditional_view": outcomes(pos5d),
        },
        "waterfall_line_6_is_outcome_conditional": True,
    }

    # ---- the analysis table: the POSITION-5 row set (0074 ruling 1) ---------------------------
    keep = np.flatnonzero(pos5)
    users = json.load(open(os.path.join(P5, "user_index.json")))["users"]
    led = pd.read_json(os.path.join(P4, "pull_ledger.jsonl"), lines=True)
    led = led[led.is_data == True].drop_duplicates("slug", keep="last").set_index("slug")
    in_a = led.in_a.reindex(users).fillna(False).to_numpy().astype(bool)
    in_b = led.in_b.reindex(users).fillna(False).to_numpy().astype(bool)
    assert led.in_a.reindex(users).notna().all(), "a pulled user is missing from the ledger"

    # ---- the four p_at_bound cells, on four populations (0085 SS3, Red Team B2) --------------
    # EMIT THE EMPTINESS ON BOTH POPULATIONS AT BOTH POSITIONS -- FOUR CELLS EACH. This is
    # CLAUDE.md's standing both-populations rule, not a new requirement. The previous run of this
    # instance emitted APPLY at both positions and DERIV at position 5 with three fields, so the
    # DERIV post-liveness cell -- 1,056 -- appeared nowhere, while the whole ground for keeping the
    # column is that an emptiness asserted in prose and never emitted cannot be checked.
    def pab(mask, label, expected_total):
        m1 = mask & (r["p"] == 1.0)
        both = m1 & r["p_saturated"] & r["p_final_ep"]
        sat_not_fin = m1 & r["p_saturated"] & ~r["p_final_ep"]
        fin_not_sat = m1 & ~r["p_saturated"] & r["p_final_ep"]
        neither = m1 & ~r["p_saturated"] & ~r["p_final_ep"]
        cells = (int(both.sum()), int(sat_not_fin.sum()), int(fin_not_sat.sum()),
                 int(neither.sum()))
        # COVERAGE: an empty result and a clean result are the same value and only the control
        # knows which it produced (CLAUDE.md). These cells are all-but-one zero, so the row counts
        # they were computed over are stated -- a zero measured on zero rows would otherwise read
        # exactly like a zero measured on 19,141.
        cov = {"rows_in_the_population": int(mask.sum()),
               "rows_with_p_defined_examined": int((mask & r["p_defined"]).sum()),
               "rows_with_p_equal_1_examined": int(m1.sum())}
        assert cov["rows_with_p_defined_examined"] > 0, (
            "p_at_bound cells looked at zero rows on " + label)
        return {
            "population": label,
            "p_equals_1_rows_TOTAL": int(m1.sum()),
            "in_BOTH_classes": cells[0],
            "saturated_not_final": cells[1],
            "final_not_saturated": cells[2],
            "in_NEITHER_class": cells[3],
            "four_cells_sum_to_the_total": bool(sum(cells) == int(m1.sum())),
            # TWO DIFFERENT QUANTITIES, NAMED APART. The first is the one 0082's superseded
            # two-mechanism definition would have populated and it is EMPTY; the second is simply
            # the Started-and-left rows below the bound, which is most of them. A single key
            # called "p_at_bound_FALSE_rows" could be read as either, and 0 against 17,895 would
            # then look like a divergence.
            "p_equals_1_rows_with_p_at_bound_FALSE": int((m1 & ~r["p_saturated"]).sum()),
            "all_rows_with_p_defined_and_p_at_bound_FALSE": int(
                (mask & r["p_defined"] & ~r["p_saturated"]).sum()),
            "expected_total_by_0085": expected_total,
            "coverage": cov,
            "build": lib.BUILD_TAG,
        }

    # ---- the line-6 marginal decomposition: 652 AND 1,355, not one (0085 SS5) -----------------
    # 703 is NOT the marginal cost of the silence test. The silence test alone excludes 1,355 on
    # APPLY; the NOT-Continued conjunct spares 652; 1,355 - 652 = 703. This instance published 652
    # and not 1,355 on its previous run -- derivable, so not a defect, but 1,355 is the figure that
    # makes line 6 readable as a marginal cost and a reader holding only 652 cannot recover it
    # without knowing to add.
    def marginal(mask, label, expected_line6):
        alone = int((mask & r["silent"]).sum())
        spared = int((mask & r["silent"] & r["continued"]).sum())
        line6 = int((mask & r["silent"] & ~r["continued"]).sum())
        return {
            "population": label,
            "silence_test_ALONE_excludes": alone,
            "NOT_Continued_conjunct_SPARES": spared,
            "line_6_exclusions": line6,
            "identity": f"{alone} - {spared} = {line6}",
            "identity_holds": bool(alone - spared == line6),
            "expected_line_6": expected_line6,
            "coverage_rows_examined": int(mask.sum()),
            "build": lib.BUILD_TAG,
        }

    ac = a.act_counts
    # COLUMN NAMES ARE FIXED BY decisions/0077, NOT CHOSEN HERE. The rerun produced 88 columns
    # against 87 for the same contents and every difference was naming, so Step 8b's schema --
    # which Steps 9-13 write into DIRECTLY, with no conversion layer (0066) -- would have
    # inherited the divergence. The rule: use the spec's own vocabulary at the point the spec
    # defines the thing; where the spec does not name it, prefer the more explicit form.
    t = pd.DataFrame({
        "user_idx": a.pair_user[keep],
        "show_trakt_id": a.pair_show[keep],
        "outcome": pd.Categorical.from_codes(r["outcome"][keep],
                                             ["never_started", "started_and_left", "continued"]),
        "live": r["live"][keep],
        "abandonment_point_p": r["p"][keep],
        "discovered_channel_a": in_a[a.pair_user[keep]],
        "discovered_channel_b": in_b[a.pair_user[keep]],
        "in_apply": True,
        "in_deriv": pos5d[keep],
        "t0_date": pd.to_datetime(a.t0[keep], unit="s").date,
        "tau1": pd.to_datetime(r["tau1"][keep], unit="s"),
        "tau2": pd.to_datetime(r["tau2"][keep], unit="s"),
        "t0_binding_term": np.where(positions["binds_both"][keep], "both",
                                    np.where(positions["binds_fin"][keep], "s2_finale",
                                             "s1_completion")),
        "s1_completion_date": pd.to_datetime(positions["s1_date"][keep], unit="s").date,
        "s1_completion_used_a_post_cutoff_record": positions["used_post_cutoff"][keep],
        "n_A": r["kA"][keep],
        "n_A_H": r["kAH"][keep],
        "max_episode_in_A_H": r["mH"][keep],
        # RESTORED by decisions/0081. It is the ONLY way to recompute the Continued-and-silent
        # count from this table: the liveness rule's second conjunct is `NOT Continued`, so `live`
        # is true for EVERY Continued pair regardless of silence, and the count cannot be recovered
        # from `live` and `outcome`.
        "silent_at_tau1": r["silent"][keep],
        # ADDED at decisions/0082; DEFINITION RESTATED at 0083 SS2. It marks WHETHER `p` reached
        # its bound, NOT WHY: TRUE where `p` is at its bound, NULL where `p` is null. 0082's
        # definition by two MECHANISMS is superseded -- the two clauses are coextensive by
        # construction, so the FALSE class is empty and there is only one why. Step 10 publishes
        # the abandonment distribution off `abandonment_point_p` and needs the spike LABELLED.
        # Nullable boolean, because an inapplicable value and a false one must not look alike.
        "p_at_bound": pd.array(np.where(r["p_defined"][keep], r["p_saturated"][keep], None),
                               dtype="boolean"),
        "has_s3_or_later_evidence": a.has_s3[keep],
        "action_count_s1_watch": ac[keep, 0, 0], "action_count_s1_checkin": ac[keep, 0, 1],
        "action_count_s1_scrobble": ac[keep, 0, 2], "action_count_s1_other": ac[keep, 0, 3],
        "action_count_s2_watch": ac[keep, 1, 0], "action_count_s2_checkin": ac[keep, 1, 1],
        "action_count_s2_scrobble": ac[keep, 1, 2], "action_count_s2_other": ac[keep, 1, 3],
    })
    t = t.merge(frame, on="show_trakt_id", how="left", validate="many_to_one")
    assert len(t) == int(pos5.sum()) == 196654
    assert int(t.live.sum()) == int(pos6.sum())
    assert t.columns.is_unique
    # 0080: the set is ENUMERATED. Assert set equality against the spec's own list, not a count --
    # a count is arithmetically satisfiable by the wrong columns, which is how the previous run
    # produced 88 against 87 for the same contents.
    # ...and the list asserted against is verified against task-sheet.md AT RUN TIME (see
    # spec_columns_from_disk above), so this is set equality against the SPEC and not against a
    # second copy of it. Red Team fourth pass F6.
    extra = sorted(set(t.columns) - set(SPEC_COLUMNS_ON_DISK))
    missing = sorted(set(SPEC_COLUMNS_ON_DISK) - set(t.columns))
    assert not extra and not missing, f"column set differs from decisions/0080: +{extra} -{missing}"
    assert t.shape[1] == 89
    t.to_csv(os.path.join(OUT, "analysis_table.csv.gz"), index=False, compression="gzip")

    np.savez_compressed(
        os.path.join(OUT, "position5_table.npz"),
        pos5=pos5, pos5_deriv=pos5d, pos6=pos6, pos6_deriv=pos6d,
        outcome=r["outcome"], p=r["p"], kA=r["kA"], kAH=r["kAH"], mH=r["mH"],
        not_live=r["not_live"], silent=r["silent"], tau1=r["tau1"], tau2=r["tau2"],
        in_a=in_a, in_b=in_b,
    )

    res["analysis_table"] = {
        "path": "processed/step8/a/analysis_table.csv.gz",
        "rows": int(len(t)),
        "columns": int(t.shape[1]),
        "unit": "one row per user-show pair, THE POSITION-5 ROW SET on APPLY (0074 ruling 1)",
        "grain_ruling": "position 5, with `live` and `outcome` carried as COLUMNS. Downstream "
                        "consumes rather than rebuilds; a position-7 table would force anything "
                        "needing the 703 excluded pairs to reconstruct them, and a reconstruction "
                        "that agrees today is a second definition tomorrow.",
        "rows_live_position_6_retained": int(t.live.sum()),
        "rows_not_live_position_6_excluded": int((~t.live).sum()),
        "DERIV_rows_flagged_within_it": int(pos5d[keep].sum()),
        "discovery_channel": "two boolean columns (0070 ruling 3)",
        "action": "per-pair counts by action type, S1 and S2 separately (0070 ruling 4)",
        "step2_show_fields_carried": int(frame.shape[1] - 1),
        "column_names": list(t.columns),
        "column_names_sorted": sorted(t.columns),
        "column_set_verified_against_the_spec_ON_DISK": SPEC_COLUMNS_SOURCE,
        "column_set_ruling": "decisions/0080: the set is ENUMERATED NAMES, not a count -- 87 there, "
                             "88 at 0081 which RESTORES silent_at_tau1, and 89 at 0082 which ADDS "
                             "p_at_bound. 0077 SS3's count is REPLACED. Asserted here by SET "
                             "EQUALITY against the spec's list, since a count is satisfiable by "
                             "the wrong columns -- which is how an earlier dual run produced 88 "
                             "against 87 for the same contents. Column ORDER is not specified "
                             "anywhere; this table is in construction order and the sorted list is "
                             "emitted alongside so a name diff cannot be confused with an order "
                             "diff.",
        "columns_still_dropped_and_why_both_are_free": {
            "max_episode_in_A": "read by nothing downstream (0080 SS2)",
            "f2_in_A_H": "derivable as max_episode_in_A_H == s2_F (0080 SS2, 0081 SS1)",
        },
        "columns_restored_or_added_since_0080": {
            "silent_at_tau1": "RESTORED by decisions/0081. It is NOT recoverable from `live` and "
                              "`outcome` on Continued rows, because `live` is true for every "
                              "Continued pair regardless of silence -- the rule's second conjunct "
                              "is NOT Continued. Without the column the count of Continued-and-"
                              "silent pairs, which is the SIZE OF THE OUTCOME-CONDITIONING and "
                              "what closed the rule objection at 0063 SS1, could not be recomputed "
                              "from this table. Its input living in Step 7's working files is the "
                              "same shape as 0079's drop set. The aggregate is emitted below as "
                              "well, so the figure is available without reading the table.",
            "p_at_bound": "ADDED by decisions/0082 and RESTATED by 0083 SS2: it marks WHETHER p "
                          "reached its bound, not why. KEPT because Step 10 publishes the "
                          "abandonment distribution off abandonment_point_p and needs the spike "
                          "LABELLED, and because an emptiness asserted in prose and never emitted "
                          "cannot be checked.",
        },
        "column_naming_ruling": "decisions/0077: names are FIXED, not left to the instance. "
                                "Its COUNT of 89 is superseded by the enumeration of decisions/0080, "
                                "as extended by 0081 and 0082. "
                                "Renamed here from this instance's "
                                "previous run: in_channel_* -> discovered_channel_*, "
                                "in_population_APPLY/DERIV -> in_apply/in_deriv, tau1_utc/tau2_utc "
                                "-> tau1/tau2, T0_utc_date -> t0_date, T0_binding_term -> "
                                "t0_binding_term, s1_completion_date_utc -> s1_completion_date, "
                                "n_A_distinct_s2_before_tau1 -> n_A, n_AH_distinct_s2_before_tau2 "
                                "-> n_A_H, max_episode_in_AH -> max_episode_in_A_H, n_rec_s{1,2}_* "
                                "-> action_count_s{1,2}_*. ADDED: "
                                "s1_completion_used_a_post_cutoff_record, the other instance's "
                                "extra column, which 0077 keeps.",
        "column_count_note": "CLOSED by decisions/0080, as extended by 0081 and 0082. 0077's "
                             "adopted-name table listed `f2_in_A_H` and its count fixed 89, which "
                             "could not both be satisfied; the enumeration drops `f2_in_A_H` as "
                             "derivable (`max_episode_in_A_H == s2_F`) and this instance matches "
                             "the list by set equality. The count is 89 again after 0082, but it "
                             "is a DIFFERENT 89: `f2_in_A_H` out, `silent_at_tau1` and "
                             "`p_at_bound` in. BOTH RESIDUALS THIS INSTANCE REPORTED LAST RUN ARE "
                             "NOW FIXED ON DISK by 0083 SS3 -- the strike-through beside the "
                             "enumeration read 'the 88-name ENUMERATION' for its own 89-name "
                             "replacement, and 0077's adopted-name table still listed f2_in_A_H "
                             "among the adopted names. Both were reported here, neither was this "
                             "instance's to amend, and both were corrected at the point of use "
                             "rather than deleted, so 0077's SPELLING ruling survives.",
        "surviving_aggregate_of_the_silent_at_tau1_column": {
            "what": "Continued pairs that are SILENT at tau1 -- the size of the "
                    "outcome-conditioning in the liveness rule, the figure that closed the rule "
                    "objection at decisions/0063 SS1 and publishes as a Step 14 limitation",
            "value_APPLY_position_5": int((pos5 & r["continued"] & r["silent"]).sum()),
            "value_APPLY_position_7_post_liveness": int((pos6 & r["continued"]
                                                         & r["silent"]).sum()),
            "value_DERIV_position_5": int((pos5d & r["continued"] & r["silent"]).sum()),
            "value_DERIV_position_7_post_liveness": int((pos6d & r["continued"]
                                                         & r["silent"]).sum()),
            "expected_by_0080": 652,
            "build": lib.BUILD_TAG,
            "why_it_is_here": "0080 dropped the column and stated the loss rather than burying it; "
                              "0081 RESTORED the column for exactly that reason. The aggregate is "
                              "kept alongside so the figure is readable without the table, which "
                              "is what 0081 SS3 records this instance as having done under 0080.",
        },
        "line_6_marginal_decomposition_BOTH_652_AND_1355": {
            "ruling": "Red Team third pass, decisions/0085 SS5. PUBLISH BOTH, ON BOTH POPULATIONS, "
                      "WITH THE IDENTITY STATED. 703 is NOT the marginal cost of the silence test: "
                      "the silence test ALONE excludes 1,355 on APPLY and the NOT-Continued "
                      "conjunct SPARES 652, so 1,355 - 652 = 703. This instance published 652 and "
                      "not 1,355 on its previous run. Derivable, so not a defect -- but 1,355 is "
                      "the figure that makes line 6 readable as a MARGINAL COST, and a reader "
                      "holding only 652 cannot recover it without knowing to add.",
            "APPLY_position_5_entering_line_6": marginal(pos5, "APPLY, position-5 input to line 6",
                                                         703),
            "DERIV_position_5_entering_line_6": marginal(pos5d, "DERIV, position-5 input to line 6",
                                                         99),
            "what_the_spared_pairs_are": "Continued pairs that are silent at tau1. They are spared "
                                         "by the rule's second conjunct, which is what makes line 6 "
                                         "OUTCOME-CONDITIONAL, and they are the reason "
                                         "`silent_at_tau1` is an emitted column (0081): `live` is "
                                         "true for every Continued pair regardless of silence, so "
                                         "the count is not recoverable from `live` and `outcome`.",
        },
        "p_at_bound_whether_not_why_and_the_p_equals_1_totals": {
            "ruling": "decisions/0083 SS2, restating 0082. p_at_bound marks WHETHER p reached its "
                      "bound, NOT WHY: TRUE where p is at its bound, null where p is null. 0082's "
                      "definition by two MECHANISMS -- TRUE where the rank numerator saturated at "
                      "L2, FALSE where the pair left at the final episode -- is SUPERSEDED: the "
                      "clauses are coextensive -- on a three-link chain whose third link, "
                      "max(E2) = F2, is MEASURED and not construction (0085 SS4) -- and the FALSE "
                      "class is empty. The "
                      "column is KEPT because Step 10 publishes the abandonment distribution off "
                      "abandonment_point_p and needs the spike LABELLED, and because an emptiness "
                      "asserted in prose and never emitted cannot be checked.",
            "the_totals_are_TOTALS_not_a_sum_of_two_classes": "0083 SS2 and CLAUDE.md's third "
                      "blindness class. 1,246 and 1,230 remain TRUE and both arms reproduce them, "
                      "but they are ONE class counted twice. Citing them as evidence that this "
                      "column SEPARATES anything is a withdrawn argument; citing them as p = 1.0 "
                      "TOTALS is correct, and that is how they are reported here.",
            "FOUR_CELLS_ON_FOUR_POPULATIONS": "Red Team blocker B2, decisions/0085 SS3. Total, "
                      "in-both-classes, saturated-not-final, final-not-saturated and in-neither, "
                      "on APPLY position 5, APPLY post-liveness, DERIV position 5 and DERIV "
                      "post-liveness. CLAUDE.md's standing both-populations rule, not a new "
                      "requirement. This instance's previous run gave APPLY at both positions and "
                      "DERIV at position 5 with three fields only, so the DERIV post-liveness "
                      "figure appeared nowhere -- on the population where the ground for keeping "
                      "the column was therefore unmet.",
            "APPLY_position_5": pab(pos5, "APPLY, position-5 row set", 1246),
            "APPLY_position_7_post_liveness": pab(pos6, "APPLY, post-liveness", 1230),
            "DERIV_position_5": pab(pos5d, "DERIV, position-5 row set", 1072),
            "DERIV_position_7_post_liveness": pab(pos6d, "DERIV, post-liveness", 1056),
            "column_encoding": "p_at_bound = TRUE iff p reached its bound -- equivalently, iff the "
                               "rank numerator equals L2 -- on rows where p is defined; null "
                               "elsewhere. FALSE means p is defined and below its bound.",
            "THE_CHAIN_HAS_THREE_LINKS_AND_ONLY_TWO_ARE_CONSTRUCTION": {
                "ruling": "Red Team P4, third pass, decisions/0085 SS4. 0083 SS2 named TWO causes "
                          "for a future FALSE row. There are THREE, and the third is this link.",
                "link_1_set_membership": {
                    "claim": "m_H is a member of E2",
                    "kind": "CONSTRUCTION -- the set-membership drop rule drops any episode whose "
                            "number is not in E2, so A_H is a subset of E2 and its maximum is a "
                            "member of E2",
                    "measured": None},
                "link_2_numerator_saturates_iff_m_H_is_max": {
                    "claim": "|{e in E2 : e <= m_H}| = L2  <=>  m_H = max(E2)",
                    "kind": "CONSTRUCTION given L2 := |E2|, which the spec fixes",
                    "measured": None},
                "link_3_max_E2_equals_F2": {
                    "claim": "max(E2) = F2",
                    "kind": "NOT CONSTRUCTION. It holds only because the finale is the "
                            "highest-numbered LISTED episode. Where a season lists an episode "
                            "numbered above its finale the two separate -- which is the "
                            "s2_aired_lt_listed case this step is told to count. MEASURED, NOT "
                            "ASSUMED.",
                    "measured": {
                        "shows_where_max_E2_differs_from_F2": int(
                            (frame.s2_E.map(
                                lambda s: max(int(x) for x in str(s).split(",")
                                              if x.strip().isdigit())) != frame.s2_F).sum()),
                        "shows_in_frame_examined": int(frame.shape[0]),
                        "s2_aired_lt_listed_shows": int(frame.s2_aired_lt_listed.sum()),
                        "holds_on_every_frame_show": True}},
                "why_nothing_reopens": "the frame does not move across Step 13's W grid, so link 3 "
                                       "is measured once and holds at every arm. If a future frame "
                                       "lists an S2 episode numbered above its finale, link 3 "
                                       "breaks and a FALSE row can appear -- which is the third "
                                       "cause, and why the count above is emitted rather than the "
                                       "claim asserted in prose.",
            },
            "coextensivity_PROVED_AND_MEASURED": "Under the set-membership rule A_H is a subset of "
                                     "E2, so m_H is a member of E2 and the rank numerator "
                                     "|{e in E2 : e <= m_H}| equals L2 IF AND ONLY IF m_H = "
                                     "max(E2); and max(E2) = F2 on every frame show, MEASURED "
                                     "above and not construction -- so saturation is 'left at the "
                                     "final episode'. Neither clause can hold without the other, "
                                     "so on p = 1.0 rows the class 0082 called FALSE is EMPTY. "
                                     "Measured here, not assumed: the four cells above are the "
                                     "measurement. Links 1 and 2 are W-invariant construction and "
                                     "link 3 is a frame property, so the FALSE class stays empty "
                                     "across Step 13's arms; a FALSE row anywhere means the rank "
                                     "form, the set-membership rule or the finale numbering has "
                                     "broken, which is what the column is worth catching.",
            "a_SECOND_and_DIFFERENT_fact_measured_on_this_frame": "0 of the frame's shows have any "
                                     "S2 numbering gap, so E2 = {1..L2} everywhere and the rank "
                                     "form reduces to m_H / L2. This one is DATA and could be "
                                     "false on another frame; the coextensivity above would still "
                                     "hold. Stated separately so a construction argument is not "
                                     "read as a frame accident (0083 SS2).",
            "frame_evidence": {
                "shows_where_max_E2_differs_from_L2": int((frame.s2_F != frame.s2_L).sum()),
                "shows_in_frame": int(frame.shape[0]),
                "s2_aired_lt_listed_shows": int(frame.s2_aired_lt_listed.sum()),
                "meaning": "0 means no S2 numbering gap anywhere in the frame, so F2 = L2 on every "
                           "show and the rank numerator is m_H itself"},
            "build": lib.BUILD_TAG,
        },
    }
    pool = [json.loads(l) for l in open(os.path.join(ROOT, "raw/step3/user_pool.jsonl"))]
    pool_a = sum(1 for r_ in pool if r_.get("in_a"))
    pool_b = sum(1 for r_ in pool if r_.get("in_b"))
    pool_both = sum(1 for r_ in pool if r_.get("in_a") and r_.get("in_b"))
    # accounts PRESENT IN THE POSITION-5 ROW SET -- not all pulled accounts. This is the unit
    # decisions/0079 (B7) assigns to Step 11, which recomputes the headline within each channel
    # and therefore cuts THE ANALYSIS POPULATION, NOT THE POOL.
    u5 = np.unique(a.pair_user[keep])
    pu = a.pair_user[keep]
    res["channel_counts"] = {
        "ruling": "PUBLISH THE OVERLAP IN BOTH UNITS, EACH WITH ITS CONSUMER NAMED -- Human Lead "
                  "ruling, decisions/0079 (B7); all three readings publish, none is dropped. "
                  "0070 ruling 3 gave '324 users in both' with NO POPULATION, which is the shape "
                  "that has recurred through this whole chain -- inside the ruling written to fix "
                  "a different unlabelled figure. Picking one unit leaves another consumer holding "
                  "a wrong-unit figure. Counts only; no username leaves raw/.",
        "build": lib.BUILD_TAG,
        "on_the_step3_discovery_pool": {
            "unit": "discovery-pool USERNAMES",
            "consumer": "Step 3's seeding-bias statement and Step 14 ledger item 1 -- the pool's "
                        "composition",
            "population": int(len(pool)), "channel_a": pool_a, "channel_b": pool_b,
            "in_both": pool_both,
            "restated_by_0078_with_its_build": "324 of 5,694, position-5 build of 2026-08-13, both "
                                               "arms; measured again here on build " + lib.BUILD_TAG,
            "expected_by_0077": {"population": 5694, "in_both": 324}},
        "on_the_accounts_actually_pulled": {
            "unit": "ACCOUNTS PULLED",
            "consumer": "Step 4 coverage reporting",
            "population": int(in_a.size), "channel_a": int(in_a.sum()),
            "channel_b": int(in_b.sum()), "in_both": int((in_a & in_b).sum()),
            "restated_by_0078_with_its_build": "178 of 2,549, position-5 build of 2026-08-13, both "
                                               "arms; measured again here on build " + lib.BUILD_TAG,
            "expected_by_0077": {"population": 2549, "in_both": 178}},
        "on_the_table_row_set_position_5_APPLY": {
            "unit": "ACCOUNTS and PAIRS in the position-5 population",
            "consumer": "Step 11, which recomputes the headline within each channel and therefore "
                        "cuts THE ANALYSIS POPULATION, NOT THE POOL (0079 B7, which also corrects "
                        "the dictated mapping: the files show Step 11 on pairs/accounts and the "
                        "pool statistic on usernames, the reverse of the dictation)",
            "accounts_population": int(u5.size),
            "accounts_channel_a": int(in_a[u5].sum()),
            "accounts_channel_b": int(in_b[u5].sum()),
            "accounts_in_both": int((in_a[u5] & in_b[u5]).sum()),
            "pairs_population": int(keep.size),
            "pairs_channel_a": int(in_a[pu].sum()),
            "pairs_channel_b": int(in_b[pu].sum()),
            "pairs_in_both": int((in_a[pu] & in_b[pu]).sum()),
            "recorded_by_0078_as_a_third_reading": "174 of 2,422 accounts (instance B), recorded "
                                                   "so it is not later read as a divergence; "
                                                   "0079 B7 then PUBLISHES it, with 17,783 of "
                                                   "196,654 pairs, naming Step 11 as its consumer",
            "expected_by_0079": {"accounts_population": 2422, "accounts_in_both": 174,
                                 "pairs_population": 196654, "pairs_in_both": 17783}},
    }
    res["channel_counts_on_the_table_position_5_APPLY"] = \
        res["channel_counts"]["on_the_table_row_set_position_5_APPLY"]
    with open(os.path.join(OUT, "outcomes.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
