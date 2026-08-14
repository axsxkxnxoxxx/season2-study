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

THE COLUMN NAMES ARE FIXED BY decisions/0077 AND THE TABLE IS 89 COLUMNS. The previous dual run
produced 88 against 87 for the same contents, all of it naming, and Step 8b defines the schema
Steps 9-13 write into DIRECTLY (0066), so the divergence would have been inherited. Both arms'
extra columns are kept: `has_s3_or_later_evidence` (D4 reads it) and
`s1_completion_used_a_post_cutoff_record` (the open D11-at-position-3 question reads it).

Output: processed/step8/a/analysis_table.csv.gz   (position-5 rows, one per user-show pair)
        processed/step8/a/position5_table.npz     (working table for the diagnostics stage)
        processed/step8/a/outcomes.json
"""
import json
import os

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

# THE COLUMN SET IS ENUMERATED, NOT COUNTED -- 87 NAMES, EXACTLY THESE. Human Lead ruling,
# decisions/0080, replacing decisions/0077 SS3's COUNT of 89. The arms converged on these names on
# the previous run, but CONVERGED IS NOT SPECIFIED and nothing prevents the next run from
# diverging; Step 8b's schema is built on this vocabulary, with Steps 9-13 writing into it
# directly and no conversion layer (0066), so it is fixed BEFORE the schema exists.
# Transcribed from task-sheet.md Step 8. Emit exactly these, no more and no fewer.
SPEC_COLUMNS = [
    "abandonment_point_p", "action_count_s1_checkin", "action_count_s1_other",
    "action_count_s1_scrobble", "action_count_s1_watch", "action_count_s2_checkin",
    "action_count_s2_other", "action_count_s2_scrobble", "action_count_s2_watch", "air_period",
    "cadence_boundary_distance_days", "cadence_bucket", "completers_per_year",
    "discovered_channel_a", "discovered_channel_b", "e1_internal_gap", "e1_starts_at_1",
    "e2_internal_gap", "e2_starts_at_1", "exclusion", "gap_days", "has_s3_or_later_evidence",
    "in_apply", "in_deriv", "live", "max_episode_in_A_H", "max_season_number", "n_A", "n_A_H",
    "outcome", "pool_completers", "pool_completers_proxy", "s1_E", "s1_F", "s1_L",
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
    "show_subgenres", "show_trakt_id", "show_votes", "show_year", "size_quintile",
    "size_quintile_per_year", "size_quintile_raw_count", "t0_binding_term", "t0_date", "tau1",
    "tau2", "title", "user_idx",
]
assert len(SPEC_COLUMNS) == len(set(SPEC_COLUMNS)) == 87


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
    extra = sorted(set(t.columns) - set(SPEC_COLUMNS))
    missing = sorted(set(SPEC_COLUMNS) - set(t.columns))
    assert not extra and not missing, f"column set differs from decisions/0080: +{extra} -{missing}"
    assert t.shape[1] == 87
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
        "column_set_ruling": "decisions/0080: the set is 87 ENUMERATED NAMES, not a count. "
                             "0077 SS3's count of 89 is REPLACED. Asserted here by SET EQUALITY "
                             "against the spec's list, since a count is satisfiable by the wrong "
                             "columns -- which is how the previous dual run produced 88 against 87 "
                             "for the same contents. Column ORDER is not specified anywhere; this "
                             "table is in construction order and the sorted list is emitted "
                             "alongside so a name diff cannot be confused with an order diff.",
        "columns_dropped_by_0080_relative_to_this_instance_previous_run": {
            "max_episode_in_A": "not read by anything downstream (0080 SS2)",
            "silent_at_tau1": "NOT A TIDY-UP AND STATED AS A REAL LOSS (0080 SS2): it is NOT "
                              "recoverable from `live` and `outcome` on Continued rows, because "
                              "`live` is true for every Continued pair regardless of silence -- "
                              "the rule's second conjunct is NOT Continued. So the count of "
                              "Continued-and-silent pairs, which is the SIZE OF THE "
                              "OUTCOME-CONDITIONING and what closed the rule objection at 0063 "
                              "SS1, can no longer be recomputed from this table. It remains "
                              "recomputable from the Step 7 masks. The count is emitted as an "
                              "AGGREGATE below so the figure itself is not lost with the column.",
        },
        "column_naming_ruling": "decisions/0077: names are FIXED, not left to the instance. "
                                "Its COUNT of 89 is superseded by decisions/0080's enumerated 87. "
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
        "column_count_note": "CLOSED by decisions/0080. 0077's adopted-name table listed "
                             "`f2_in_A_H` and its count fixed 89, which could not both be "
                             "satisfied; the enumerated 87 drops `f2_in_A_H` as derivable "
                             "(`max_episode_in_A_H == s2_F`) and this instance now matches the "
                             "list by set equality. The task-sheet bullet carrying 0077's '89 "
                             "columns' still stands next to 0080's enumerated 87 in the same "
                             "file; 0080 explicitly replaces it, and the residual is reported.",
        "surviving_aggregate_of_the_dropped_silent_at_tau1_column": {
            "what": "Continued pairs that are SILENT at tau1 -- the size of the "
                    "outcome-conditioning in the liveness rule, the figure that closed the rule "
                    "objection at decisions/0063 SS1 and publishes as a Step 14 limitation",
            "value_APPLY_position_5": int((pos5 & r["continued"] & r["silent"]).sum()),
            "value_APPLY_position_7_post_liveness": int((pos6 & r["continued"]
                                                         & r["silent"]).sum()),
            "value_DERIV_position_5": int((pos5d & r["continued"] & r["silent"]).sum()),
            "expected_by_0080": 652,
            "build": lib.BUILD_TAG,
            "why_it_is_here": "0080 drops the column and states the loss rather than burying it. "
                              "The COUNT is emitted as an aggregate so it does not vanish with the "
                              "column; what is lost is the ability to recompute it row-by-row from "
                              "the table, and that remains true.",
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
