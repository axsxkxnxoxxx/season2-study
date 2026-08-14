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
        "silent_at_tau1": r["silent"][keep],
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
        "max_episode_in_A": r["mA"][keep],
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
    assert t.shape[1] == 89, f"the column set is fixed at 89 by 0077; this is {t.shape[1]}"
    assert t.columns.is_unique
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
        "column_naming_ruling": "decisions/0077: names are FIXED, not left to the instance, and "
                                "the table is 89 columns. Renamed here from this instance's "
                                "previous run: in_channel_* -> discovered_channel_*, "
                                "in_population_APPLY/DERIV -> in_apply/in_deriv, tau1_utc/tau2_utc "
                                "-> tau1/tau2, T0_utc_date -> t0_date, T0_binding_term -> "
                                "t0_binding_term, s1_completion_date_utc -> s1_completion_date, "
                                "n_A_distinct_s2_before_tau1 -> n_A, n_AH_distinct_s2_before_tau2 "
                                "-> n_A_H, max_episode_in_AH -> max_episode_in_A_H, n_rec_s{1,2}_* "
                                "-> action_count_s{1,2}_*. ADDED: "
                                "s1_completion_used_a_post_cutoff_record, the other instance's "
                                "extra column, which 0077 keeps.",
        "column_count_note": "0077's adopted-name table also lists `f2_in_A_H`. This instance has "
                             "no such column and adding one would make 90, against the 89 the "
                             "same ruling fixes; 89 is reachable from this instance's 88 only by "
                             "adding exactly the one extra column named for the other arm. The "
                             "quantity is carried as `max_episode_in_A_H`, and `F2 in A_H` is "
                             "exactly `max_episode_in_A_H == s2_F`, a Step 2 frame field already "
                             "on the row. REPORTED, NOT RECONCILED.",
    }
    pool = [json.loads(l) for l in open(os.path.join(ROOT, "raw/step3/user_pool.jsonl"))]
    pool_a = sum(1 for r_ in pool if r_.get("in_a"))
    pool_b = sum(1 for r_ in pool if r_.get("in_b"))
    pool_both = sum(1 for r_ in pool if r_.get("in_a") and r_.get("in_b"))
    res["channel_counts"] = {
        "note": "0070 ruling 3 gave '324 users in both' with NO POPULATION; decisions/0077 states "
                "both figures and both populations. They are not a divergence -- they are two "
                "populations. Counts only; no username leaves raw/.",
        "on_the_step3_discovery_pool": {
            "population": int(len(pool)), "channel_a": pool_a, "channel_b": pool_b,
            "in_both": pool_both, "expected_by_0077": {"population": 5694, "in_both": 324}},
        "on_the_accounts_actually_pulled": {
            "population": int(in_a.size), "channel_a": int(in_a.sum()),
            "channel_b": int(in_b.sum()), "in_both": int((in_a & in_b).sum()),
            "expected_by_0077": {"population": 2549, "in_both": 178}},
        "on_the_table_row_set_position_5_APPLY": {
            "pairs_channel_a": int(in_a[a.pair_user[keep]].sum()),
            "pairs_channel_b": int(in_b[a.pair_user[keep]].sum()),
            "pairs_in_both": int((in_a[a.pair_user[keep]] & in_b[a.pair_user[keep]]).sum()),
            "accounts_channel_a": int(in_a.sum()), "accounts_channel_b": int(in_b.sum()),
            "accounts_in_both": int((in_a & in_b).sum())},
    }
    res["channel_counts_on_the_table_position_5_APPLY"] = \
        res["channel_counts"]["on_the_table_row_set_position_5_APPLY"]
    with open(os.path.join(OUT, "outcomes.json"), "w") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
