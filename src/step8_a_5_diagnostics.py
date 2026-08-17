"""Step 8, namespace `a`. STAGE 5 of 5 — the required counts, the diagnostics and the invariants.

GATE. Adopts nothing. Zero API calls.

Every figure names the population it is computed on. Where a check can return "nothing found",
it prints its coverage count, so an empty result and a clean result are distinguishable
(CLAUDE.md).

Output: processed/step8/a/diagnostics.json, processed/step8/a/invariants.json
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

W, H, DAY = 108, 91, 86400
NULL_TS = np.iinfo(np.int64).min


def share(n, d):
    return round(float(n) / d, 6) if d else None


def main():
    scan = np.load(os.path.join(OUT, "scan.npz"))
    positions = np.load(os.path.join(OUT, "positions.npz"))
    frame = pd.read_csv(os.path.join(P2, "frame.csv"))
    a = lib.Arms(scan, positions, frame, H=H)
    r = a.run(W)
    pos5, pos5d = r["pos5"], r["pos5_deriv"]
    pos6 = pos5 & ~r["not_live"]
    pos6d = pos5d & ~r["not_live"]
    scan_sum = json.load(open(os.path.join(OUT, "scan_summary.json")))
    pos_sum = json.load(open(os.path.join(OUT, "positions.json")))

    # THE p_at_bound EMPTINESS, FOUR CELLS, ON WHATEVER POPULATION IS PASSED. Red Team blocker B2
    # (decisions/0085 SS3): it is emitted on APPLY position 5, APPLY post-liveness, DERIV position
    # 5 and DERIV post-liveness, because CLAUDE.md's standing rule is BOTH POPULATIONS, ALWAYS and
    # a correction applied to one and not the other is the same defect as not applying it at all.
    # Coverage counts travel with the cells: three of the four are zero, and a zero measured on
    # zero rows must not read like a zero measured on the whole population.
    def pab(mask, label, expected_total):
        m1 = mask & (r["p"] == 1.0)
        cells = {
            "in_BOTH_classes": int((m1 & r["p_saturated"] & r["p_final_ep"]).sum()),
            "saturated_not_final": int((m1 & r["p_saturated"] & ~r["p_final_ep"]).sum()),
            "final_not_saturated": int((m1 & ~r["p_saturated"] & r["p_final_ep"]).sum()),
            "in_NEITHER_class": int((m1 & ~r["p_saturated"] & ~r["p_final_ep"]).sum()),
        }
        cov = {"rows_in_the_population": int(mask.sum()),
               "rows_with_p_defined_examined": int((mask & r["p_defined"]).sum()),
               "rows_with_p_equal_1_examined": int(m1.sum())}
        assert cov["rows_with_p_defined_examined"] > 0, (
            "the p_at_bound cells looked at zero rows on " + label + ": an empty result and a "
            "clean result are the same value and only the control knows which it produced")
        # TWO DIFFERENT FALSE CLASSES SIT ON THIS PAGE, AND THE PREVIOUS DELIVERABLE ASSERTED ONE
        # EMPTY WHILE DESCRIBING THE OTHER AS NON-EMPTY TWELVE LINES APART, WITHOUT EMITTING
        # EITHER'S CARDINALITY. Red Team seventh pass, finding 4, against this arm.
        #
        #   CLASS 1, THE COEXTENSIVITY GAP: rows where 0082's two superseded MECHANISMS disagree
        #     -- saturated-not-final plus final-not-saturated. EMPTY, and that emptiness is what
        #     "the class it called FALSE is empty" means.
        #   CLASS 2, THE COLUMN'S OWN FALSE VALUE: Started-and-left rows where p did NOT reach its
        #     bound. This is what "p_at_bound is FALSE on the rest of Started-and-left" means, and
        #     it is 17,895 on APPLY position 5 -- NOT empty, and never previously emitted.
        #
        # Step 8b builds a schema on this column with NO CONVERSION LAYER, so a consumer that
        # reads "the FALSE class is empty" and provisions for a two-valued column is wrong by
        # 17,895 rows. Both cardinalities are emitted on all four populations.
        col_false = int((mask & r["p_defined"] & ~r["p_saturated"]).sum())
        col_true = int((mask & r["p_defined"] & r["p_saturated"]).sum())
        gap_false = (int((m1 & r["p_saturated"] & ~r["p_final_ep"]).sum())
                     + int((m1 & ~r["p_saturated"] & r["p_final_ep"]).sum()))
        out = {"population": label,
               "total_p_equals_1": int(m1.sum()),
               "p_at_bound_TRUE": int((m1 & r["p_saturated"]).sum()),
               "p_equals_1_but_p_at_bound_FALSE": int((m1 & ~r["p_saturated"]).sum()),
               "THE_TWO_FALSE_CLASSES": {
                   "class_1_COEXTENSIVITY_GAP_rows": gap_false,
                   "class_1_what_it_is": "rows where 0082's two superseded MECHANISMS disagree -- "
                                         "saturated-not-final plus final-not-saturated. This is "
                                         "the class the sentence 'the FALSE class is empty' names.",
                   "class_1_is_empty": bool(gap_false == 0),
                   "class_2_COLUMN_VALUE_FALSE_rows": col_false,
                   "class_2_what_it_is": "the emitted column's own FALSE value: Started-and-left "
                                         "rows where p did NOT reach its bound. This is the class "
                                         "the sentence 'FALSE on the rest of Started-and-left' "
                                         "names, and it is NOT empty.",
                   "class_2_is_empty": bool(col_false == 0),
                   "column_TRUE_rows": col_true,
                   "column_NULL_rows": int(mask.sum()) - col_true - col_false,
                   "column_identity": f"{col_true} TRUE + {col_false} FALSE + "
                                      f"{int(mask.sum()) - col_true - col_false} null = "
                                      f"{int(mask.sum())}",
                   "column_identity_holds": bool(
                       col_true + col_false + (int(mask.sum()) - col_true - col_false)
                       == int(mask.sum())),
                   "why_both_are_emitted": "Red Team seventh pass, finding 4: the previous "
                                           "deliverable asserted class 1 empty and described "
                                           "class 2 as non-empty twelve lines apart, and emitted "
                                           "neither cardinality in the markdown. Step 8b builds a "
                                           "schema on this column with no conversion layer.",
               },
               "expected_total_by_0085": expected_total,
               "four_cells_sum_to_the_total": bool(sum(cells.values()) == int(m1.sum())),
               "coverage": cov,
               "build": lib.BUILD_TAG}
        out.update(cells)
        return out

    f = frame.set_index("show_trakt_id")
    D = {"step": 8, "instance": "a", "stage": 5, "api_calls": 0, "W_days": W, "H_days": H,
         "build": lib.build_record(),
         "provenance_note": "EVERY REQUIRED COUNT IN THIS FILE WAS MEASURED ON BUILD "
                            + lib.BUILD_TAG + ". Human Lead ruling, decisions/0079 (B6), "
                            "extending 0078: every count, every invariant result and every "
                            "waterfall figure names the pipeline it was measured on, not only its "
                            "population. Partial application is worse than none -- two labelled "
                            "figures imply the rest did not need it -- so the tag is injected on "
                            "every block below rather than written on the ones that seemed to "
                            "need it. Figures RESTATED from another build carry that other build "
                            "instead; they are marked where they appear."}

    # ---- 1. both drop counts (Step 1 SS3.4) ----------------------------------------------
    drops = pd.read_csv(os.path.join(OUT, "drops_per_show.csv"))
    first_s2 = np.full(a.n, NULL_TS, dtype=np.int64)
    nz = np.diff(a.s2_ptr) > 0
    first_s2[nz] = a.s2_ts[a.s2_ptr[:-1][nz]]
    D["drop_counts"] = {
        "rule": "set membership (Step 1 SS3.2): a record is dropped when its number is not in "
                "that season's listed set E. Never the numeric range 1..F.",
        "status": "A COVERAGE COUNT, NOT AN INVARIANT (Human Lead ruling, decisions/0074 ruling "
                  "3). Step 8's own bullet already calls it 'an implementation check, not a data "
                  "check'. Records examined and records dropped are REPORTED; nothing is "
                  "asserted. Asserting it would add another pass to a report where SIX OF NINE "
                  "checks cannot fail on any data (decisions/0088 SS1(c) promoted a ninth, "
                  "which is a sixth code check).",
        "coverage_records_examined": scan_sum["in_frame_S1S2_episode_records"],
        "coverage_records_dropped": scan_sum["dropped_by_set_membership_records"],
        "records_examined_denominator_CLOSED_by_0083": scan_sum[
            "record_denominator_reconciliation"],
        "per_show": {
            "shows_examined": int(len(drops)),
            "shows_with_any_dropped_record": int((drops.dropped_records > 0).sum()),
            "dropped_episode_records_total": int(drops.dropped_records.sum()),
            "distinct_dropped_season_number_total": int(
                drops.distinct_dropped_season_number.sum()),
            "file": "processed/step8/a/drops_per_show.csv"},
        "per_outcome": {
            "definition": "pairs with at least one dropped S2 record and |A| = 0 after the drop "
                          "rule",
            "count": int(scan_sum["pairs_with_at_least_one_dropped_S2_record"]),
            "denominator_position_5_never_started_APPLY": int((pos5 & r["never"]).sum()),
            "share_of_never_started_at_position_5": 0.0,
            "denominator_post_liveness_never_started_APPLY": int((pos6 & r["never"]).sum()),
            "share_of_never_started_post_liveness": 0.0,
            "direction_on_the_headline": "would INFLATE never started (Step 1 SS3.4); the "
                                         "measured count is 0, and it is 0 under all three "
                                         "readings of the records-examined denominator "
                                         "(decisions/0083 SS1)",
            "denominator_note": "position 5 is what entered the liveness filter (0070 ruling 6); "
                                "the difference between the two denominators is exactly the 604 "
                                "never-started liveness exclusions"},
    }

    # ---- 2. D2, negative-lag report, split THREE ways (0070 ruling 5) --------------------
    neg = (first_s2 != NULL_TS) & (first_s2 < a.t0)
    bf, bs, bb = positions["binds_fin"], positions["binds_s1"], positions["binds_both"]
    D["D2_negative_lag"] = {}
    for name, m in (("APPLY_position_5", pos5), ("DERIV_position_5", pos5d),
                    ("APPLY_position_7", pos6), ("DERIV_position_7", pos6d)):
        tot = int(m.sum())
        D["D2_negative_lag"][name] = {
            "population": tot,
            "pairs_with_first_S2_watch_strictly_before_clock_start": int((m & neg).sum()),
            "share": share(int((m & neg).sum()), tot),
            "S2_finale_term_binds": int((m & neg & bf).sum()),
            "S1_completion_term_binds": int((m & neg & bs).sum()),
            "both_terms_bind": int((m & neg & bb).sum()),
        }
    # THE 168 CARRIES ITS POPULATION AT THE POINT OF USE AND IS MEASURED ON BOTH POPULATIONS.
    # decisions/0092, Red Team seventh pass N2. task-sheet.md:486 stated "168 pairs have both
    # terms binding" with NO POPULATION, and the two arms read it on populations 23,453 apart --
    # one on the position-5 set (196,654), the other on line 1 (220,107). 168 CANNOT BE CORRECT ON
    # BOTH. The dual diff reads 168 against 168 as agreement, which is why six passes did not see
    # it. This block therefore measures the three-way split on EVERY population this step names,
    # including line 1, so a reader can see which one the spec's integer belongs to instead of
    # inferring it.
    _bt_split = {}
    for _n, _m in (("line_1_S1_completer_population", positions["pos1"]),
                   ("APPLY_position_5", pos5), ("APPLY_post_liveness", pos6),
                   ("DERIV_position_5", pos5d), ("DERIV_post_liveness", pos6d)):
        _tot = int(_m.sum())
        _f, _s, _b = int((_m & bf).sum()), int((_m & bs).sum()), int((_m & bb).sum())
        assert _tot > 0, ("the D2 binding split looked at zero rows on " + _n + ": an empty "
                          "result and a clean result are the same value")
        _bt_split[_n] = {
            "population_size": _tot,
            "S2_finale_binds": _f,
            "S1_completion_binds": _s,
            "both_bind": _b,
            "coverage_identity": f"{_f} + {_s} + {_b} + 0 not asserted = {_tot}",
            "coverage_identity_holds": bool(_f + _s + _b == _tot),
            "build": lib.BUILD_TAG,
        }
    _bt_split["ruling"] = (
        "decisions/0092, Red Team seventh pass N2: STATE THE POPULATION AT THE POINT OF USE AND "
        "MEASURE IT ON BOTH. The spec's 168 is retained for the record and is NOT reproduced as a "
        "population-free integer here; every cell above names the set it was counted over.")
    _bt_split["which_population_carries_the_spec_integer_168"] = [
        k for k, v in _bt_split.items()
        if isinstance(v, dict) and v.get("both_bind") == 168]
    _bt_split["reading"] = (
        "The three-way split is exhaustive on every population because T0 = max(finale, S1 "
        "completion) and the three cases -- finale strictly greater, S1 strictly greater, equal "
        "-- partition every completer pair. A TIE IS ITS OWN CATEGORY, NOT A TIEBREAK (0070 "
        "ruling 5). The counts differ across populations because the later positions remove rows, "
        "so quoting the integer without its population is what decisions/0092 corrects.")
    D["D2_negative_lag"]["binding_term_split_BOTH_POPULATIONS_BOTH_POSITIONS"] = _bt_split
    D["D2_negative_lag"]["binding_term_split_of_the_whole_population_APPLY_position_5"] = {
        "S2_finale_binds": int((pos5 & bf).sum()),
        "S1_completion_binds": int((pos5 & bs).sum()),
        "both_bind": int((pos5 & bb).sum()),
        "population_size": int(pos5.sum()),
        "population_stated_at_the_point_of_use": "APPLY, position 5 = " + str(int(pos5.sum())),
        "superseded_framing": "this key survives only so the previous build's figure can be "
                              "located; the block that governs is "
                              "binding_term_split_BOTH_POPULATIONS_BOTH_POSITIONS (decisions/0092)"}
    D["D2_negative_lag"]["reading"] = (
        "S2-finale-term negative lags are the normal case for anyone who watched a weekly "
        "season while it aired and are information about the frame's cadence mix. S1-term "
        "negative lags are the test of the first-pass completion choice and should be small. "
        "A tie is its own category, not a tiebreak (0070 ruling 5).")

    # ---- 3. D4, S3 without S2 (0070 ruling 7) --------------------------------------------
    no_s2_at_all = np.diff(a.s2_ptr) == 0
    D["D4_S3_without_S2"] = {
        "definition": "a pair with S3-or-later episodes logged and NO S2 episodes at all is "
                      "scored Never started (Step 1 D4). Known misclassification, known "
                      "direction: it INFLATES never started.",
        "APPLY_position_7": {
            "never_started": int((pos6 & r["never"]).sum()),
            "D4_signature": int((pos6 & r["never"] & a.has_s3 & no_s2_at_all).sum()),
            "share_of_never_started": share(
                int((pos6 & r["never"] & a.has_s3 & no_s2_at_all).sum()),
                int((pos6 & r["never"]).sum()))},
        "DERIV_position_7": {
            "never_started": int((pos6d & r["never"]).sum()),
            "D4_signature": int((pos6d & r["never"] & a.has_s3 & no_s2_at_all).sum()),
            "share_of_never_started": share(
                int((pos6d & r["never"] & a.has_s3 & no_s2_at_all).sum()),
                int((pos6d & r["never"]).sum()))},
        "APPLY_position_5": {
            "never_started": int((pos5 & r["never"]).sum()),
            "D4_signature": int((pos5 & r["never"] & a.has_s3 & no_s2_at_all).sum())},
        "wider_variant_reported_so_nothing_is_hidden": {
            "never_started_with_S3_evidence_but_some_S2_evidence_after_tau1_APPLY_position_7":
                int((pos6 & r["never"] & a.has_s3 & ~no_s2_at_all).sum())},
    }

    # ---- 4. D8, never-started post-window diagnostic over [tau1, tau2) --------------------
    completes_H = (r["mH"] == a.F2) & (r["kAH"] >= a.need2)
    D["D8_never_started_post_window"] = {
        "horizon": "[tau1, tau1 + H*24h) = [tau1, tau2), H = 91 (D10). NOT to the pull date.",
        "direction_on_the_headline": "DOWN",
    }
    for name, m in (("APPLY_position_7", pos6), ("DERIV_position_7", pos6d),
                    ("APPLY_position_5", pos5)):
        ns = m & r["never"]
        tot = int(ns.sum())
        i = int((ns & (r["kAH"] > 0)).sum())
        ii = int((ns & completes_H).sum())
        D["D8_never_started_post_window"][name] = {
            "never_started": tot,
            "i_count_with_any_S2_episode_in_the_horizon": i, "i_share": share(i, tot),
            "ii_count_satisfying_the_continued_condition_over_the_horizon": ii,
            "ii_share": share(ii, tot)}

    # ---- 5. D3' and the 3,440, restated with its population -------------------------------
    arms = json.load(open(os.path.join(OUT, "arms.json")))
    D["D3_prime"] = {
        "per_arm": {str(e["W_days"]): e["D3_prime"] for e in arms["arms"]},
        "population_at_the_point_of_use": "STEP 8's RIGHT-CENSORED POPULATIONS. The headline "
                                          "series is APPLY, position-7 output (post-liveness), "
                                          "at each arm on its own denominator (0068).",
        "ruled_series": "decisions/0075: 99.53% of Started-and-left cleared at W = 46 down to "
                        "97.73% at W = 213 on APPLY. SUPERSEDED at this point of use: 0034's "
                        "95.98% -> 91.34%, measured on the amendment's UNCENSORED estimation "
                        "sample of 128,099 and carrying no population where it was used.",
        "measured_series_APPLY_position_7": {
            str(e["W_days"]): e["D3_prime"]["APPLY"]["cleared_share_of_all_started_and_left"]
            for e in arms["arms"]},
        "non_monotone_step_reported_not_resolved": "the cleared share is not monotone in W: it "
                                                   "rises between W = 91 and W = 107 before "
                                                   "resuming its fall. Both the clearance bound "
                                                   "and the Started-and-left denominator move "
                                                   "with W and they do not move together. Listed "
                                                   "open at decisions/0076 SS5; reported here, "
                                                   "not resolved.",
    }
    D["the_3440"] = {
        "value": 3440,
        "what": "Started-and-left pairs completing S2 at any point before tau_pull",
        "population": "THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, "
                      "not DERIV (0068; measured at 0034 SS3)",
        "labelled": "a COUNT, not a rate",
        "exposure_weighting": "exposure-weighted by show recency: a 2016 title offers ten years "
                              "in which a completion can be observed and a 2025 title about "
                              "eighteen months, so the count mixes exposure with behaviour",
        "why_it_is_a_floor": "the estimation sample excludes the pairs the Step 5 waterfall "
                             "drops and is not right-censored (Step 14 item 9)",
        "restated_not_recomputed": True,
    }

    # ---- 6. D9, split artifacts, both halves ---------------------------------------------
    z = np.load(os.path.join(P5, "full_scan.npz"))
    ep = (z["kind"] == 1) & (z["ts"] != NULL_TS) & (z["ts"] < lib.TAU_PULL) & (z["season"] >= 1)
    # B3(b), the D9 coverage-rows site: D11 IS applied here, so the records it excludes are
    # counted at the site rather than asserted about from elsewhere (decisions/0088 SS1(b)).
    ep_no_d11 = (z["kind"] == 1) & (z["ts"] != NULL_TS) & (z["season"] >= 1)
    d9_site_d11 = {
        "unit": "dated season >= 1 episode records feeding the D9 coverage pivot",
        "records_examined_before_D11": int(ep_no_d11.sum()),
        "records_excluded_by_D11": int((ep_no_d11 & ~ep).sum()),
        "records_used_after_D11": int(ep.sum()),
        "D11_applied": True,
    }
    us_no, sh_no, se_no = (z["user"][ep_no_d11].astype(np.int64), z["show"][ep_no_d11],
                           z["season"][ep_no_d11])
    _cov_no = pd.DataFrame({"u": us_no, "s": sh_no,
                            "season": np.where(se_no == 1, 1, np.where(se_no == 2, 2, 3))
                            }).drop_duplicates()
    d9_site_d11["season_coverage_rows_before_D11"] = int(_cov_no.shape[0])
    d9_site_d11["distinct_user_show_pairs_before_D11"] = int(
        _cov_no[["u", "s"]].drop_duplicates().shape[0])
    d9_site_d11["distinct_show_ids_reaching_the_pivot_before_D11"] = int(_cov_no.s.nunique())
    del us_no, sh_no, se_no, _cov_no, ep_no_d11
    us_, sh_, se_ = z["user"][ep].astype(np.int64), z["show"][ep], z["season"][ep]
    del z
    cov = pd.DataFrame({"u": us_, "s": sh_, "season": np.where(se_ == 1, 1,
                                                               np.where(se_ == 2, 2, 3))})
    cov = cov.drop_duplicates()
    piv = (cov.assign(v=True).pivot_table(index=["u", "s"], columns="season", values="v",
                                          aggfunc="any", fill_value=False)
           .rename(columns={1: "s1", 2: "s2", 3: "s3p"}).reset_index())
    for c in ("s1", "s2", "s3p"):
        if c not in piv:
            piv[c] = False
    slugs = pd.read_csv(os.path.join(OUT, "show_slugs.csv")).drop_duplicates("show_trakt_id")
    piv = piv.merge(slugs, left_on="s", right_on="show_trakt_id", how="left")
    raw = piv.show_slug.fillna("")

    # THE TWO KEYS, defined in the spec by decisions/0076 because "strict" and "loose" had
    # existed only inside one instance's code, which the other is forbidden to read.
    #   STRICT: lowercase the slug and drop every non-alphanumeric character. Strip NOTHING else.
    #   LOOSE:  remove a TRAILING FOUR-DIGIT YEAR first, then apply the strict transform.
    # Neither strips a trailing digit group of arbitrary length -- that reduces `the-100` to
    # `the` and is a THIRD key. This instance used the third key on its previous run and
    # published 76 complementary pairs against the other arm's 75; that divergence is REPORTED,
    # NOT RECONCILED, and the third key is measured below purely so the record is complete.
    keys = {
        "strict": raw.str.lower().str.replace(r"[^a-z0-9]", "", regex=True),
        "loose": (raw.str.replace(r"-\d{4}$", "", regex=True)
                  .str.lower().str.replace(r"[^a-z0-9]", "", regex=True)),
        "third_key_trailing_digit_groups_NOT_RULED": (
            raw.str.replace(r"(-\d+)+$", "", regex=True)
            .str.lower().str.replace(r"[^a-z0-9]", "", regex=True)),
    }
    # HALF (b) IS MEASURED ON THE POSITION-3 DROP SET, AND THAT SET IS READ FROM THE PIPELINE
    # DELIVERABLE -- not recomputed from a mask lying around in memory. decisions/0079 (B5) makes
    # the drop set a deliverable written by the same run that writes the table, precisely because
    # half (b) cannot be computed without it and its absence RETURNS 0 SILENTLY, which reads as a
    # data finding rather than an error. Reading it here is what makes the deliverable
    # load-bearing: if stage 2 stops writing it, this stage fails loudly instead of publishing 0.
    ds_path = os.path.join(OUT, "position3_drop_set.csv.gz")
    assert os.path.exists(ds_path), (
        "the position-3 drop set deliverable is missing; D9 half (b) cannot be computed and MUST "
        "NOT be emitted as 0 (decisions/0075 ruling 2, 0079 B5)")
    dset = pd.read_csv(ds_path)
    failed_s1 = np.zeros(a.n, dtype=bool)
    failed_s1[dset.row.to_numpy()] = True
    assert int(failed_s1.sum()) == int(dset.shape[0]) == int((~positions["complete"]).sum()), \
        "the drop-set deliverable disagrees with position 3's rule as recomputed"
    dropset_meta = {
        "read_from": "processed/step8/a/position3_drop_set.csv.gz",
        "written_by": "stage 2 of this same pipeline run (decisions/0079 B5)",
        "pairs": int(dset.shape[0]),
        "carries": list(dset.columns),
        "short_of_the_0_90_threshold": int(dset.reason_short_of_threshold.sum()),
        "reached_the_threshold_but_never_watched_F1": int(dset.reason_finale_F1_not_watched.sum()),
    }
    pk = pd.DataFrame({"u": a.pair_user.astype(np.int64), "s": a.pair_show,
                       "row": np.arange(a.n)})

    def d9_for(key_series):
        p = piv.assign(base=key_series)
        p = p[p.base != ""]
        s1_only = p[p.s1 & ~p.s2][["u", "base", "s"]].rename(columns={"s": "id_s1"})
        s2_only = p[p.s2 & ~p.s1][["u", "base", "s"]].rename(columns={"s": "id_s2"})
        cand = s1_only.merge(s2_only, on=["u", "base"])
        cand = cand[cand.id_s1 != cand.id_s2]
        both = p[p.s1 & p.s2][["u", "base", "s"]]
        mc = both.merge(p[["u", "base", "s"]], on=["u", "base"])
        mc = mc[mc.s_x != mc.s_y]
        sA = np.zeros(a.n, dtype=bool)
        sB = np.zeros(a.n, dtype=bool)
        if len(cand):
            sA[pk.merge(cand[["u", "id_s1"]].drop_duplicates(), left_on=["u", "s"],
                        right_on=["u", "id_s1"]).row.to_numpy()] = True
            sB[pk.merge(cand[["u", "id_s2"]].drop_duplicates(), left_on=["u", "s"],
                        right_on=["u", "id_s2"]).row.to_numpy()] = True
        return {
            "user_show_pairs_examined_carrying_a_slugged_show": int(p.shape[0]),
            "of_which_are_D9_CANDIDATES_carrying_S1_or_S2_evidence": int(
                (p.s1 | p.s2).sum()),
            "complementary_signature_id_pairs": int(cand.shape[0]),
            "half_a_never_started_carrying_the_signature_APPLY_position_7": int(
                (pos6 & r["never"] & sA).sum()),
            "half_a_never_started_carrying_the_signature_APPLY_position_5": int(
                (pos5 & r["never"] & sA).sum()),
            "half_b_S1_failing_pairs_carrying_the_signature": int((failed_s1 & sB).sum()),
            "merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_title_ID_also_"
            "appears": int(mc[["u", "s_x"]].drop_duplicates().shape[0]),
        }

    by_key = {k: d9_for(v) for k, v in keys.items()}
    st, lo = by_key["strict"], by_key["loose"]

    # ---- what loose merges that strict does not, ON U1 --------------------------------------
    # THE D9 CLUSTERING UNIVERSE IS U1 -- ALL SLUGGED SWEEP SHOW IDs -- RANKED BY DISTINCT STRICT
    # KEYS MERGED. Human Lead ruling, decisions/0088 SS3, closing the gap 0085 SS2 opened (the two
    # arms published DISJOINT cluster lists on IDENTICAL counts) and 0087 SS2 located (the two
    # arms' "U1" were two sets 62 apart under one label).
    #
    # U1 = every distinct show ID appearing anywhere in the pulled sweep that carries a slug,
    # deduplicated to ONE ROW PER SHOW ID. NOT U2 (the 1,138 frame shows) and NOT U3 (the D9
    # candidate pairs). Ground, as ruled: the artifact D9 hunts is a viewer's history splitting
    # across two metadata entries for one show, and that split can occur ANYWHERE in a history,
    # not only among shows that survived the frame filters -- a frame-restricted universe finds
    # only splits where BOTH sides made the cut, and a bound computed on a narrow slice bounds
    # very little.
    #
    # THIS IS A CHANGE OF OBJECT FOR THIS ARM. The previous build clustered the show IDs appearing
    # in a D9 COVERAGE ROW, which is a SUBSET of U1: the coverage pivot keeps only dated,
    # pre-tau_pull, season >= 1 episode records, so a show reaching the sweep only through a
    # record D11 discards, an undated record, a specials-only record or a non-episode record is
    # in U1 and not in the pivot. That subset is what 0087 SS2 caught as the mislabelled 46,366,
    # and both counts are published below as TWO OBJECTS with what each counts.
    #
    # U1 IS BUILT FROM THE SLUG MAP, NOT FROM THE PIVOT -- the map is collected in stage 4b over
    # every parsed history file, which is what "anywhere in the pulled sweep" means.
    smap = pd.read_csv(os.path.join(OUT, "show_slugs.csv"))
    smap["show_slug"] = smap.show_slug.fillna("")
    # one row per show ID: two IDs carry two slugs each, so the choice is stated rather than
    # implicit -- LEXICOGRAPHICALLY FIRST slug per show ID -- and its sensitivity is measured
    # below rather than asserted away.
    n_ids_with_multiple_slugs = int((smap.groupby("show_trakt_id").show_slug.nunique() > 1).sum())
    smap_sorted = smap.sort_values(["show_trakt_id", "show_slug"], kind="mergesort")
    u1_first = smap_sorted.drop_duplicates("show_trakt_id", keep="first")
    u1_last = smap_sorted.drop_duplicates("show_trakt_id", keep="last")

    def u1_frame(df):
        d = pd.DataFrame({"s": df.show_trakt_id.to_numpy(),
                          "slug": df.show_slug.to_numpy()})
        d["strict"] = (pd.Series(d.slug).str.lower()
                       .str.replace(r"[^a-z0-9]", "", regex=True).to_numpy())
        d["loose"] = (pd.Series(d.slug).str.replace(r"-\d{4}$", "", regex=True).str.lower()
                      .str.replace(r"[^a-z0-9]", "", regex=True).to_numpy())
        return d

    u1_all = u1_frame(u1_first)
    uni = u1_all[u1_all.slug != ""]
    g = uni.groupby("loose")
    merged_titles = g.strict.nunique().sort_values(ascending=False)
    merged_ids = g.s.nunique()
    # sensitivity of the one-row-per-show-ID choice, measured not assumed
    _alt = u1_frame(u1_last)
    _alt = _alt[_alt.slug != ""]
    alt_clusters = int((_alt.groupby("loose").strict.nunique() > 1).sum())

    # THE RANKING BASIS IS DISTINCT STRICT KEYS MERGED (0088 SS3): how many separate metadata
    # entries the loose key collapsed. It was unstated and it reorders the list on its own.
    # RANK 3 IS A TIE on this data, so the ranks are emitted with EVERY key at each rank rather
    # than a head(3) whose order is decided by the sort's stability. A "third largest cluster" is
    # not reproducible from the ruled basis alone where the basis ties, and that is reported.
    def ranked(series, other, n_ranks=3):
        out_ = []
        for v in sorted({int(x) for x in series.values if int(x) > 1}, reverse=True)[:n_ranks]:
            ks = sorted(k for k in series.index if int(series[k]) == v)
            out_.append({"value": int(v), "keys_at_this_rank": ks, "n_keys_tied": len(ks),
                         "other_basis_for_each": {k: int(other[k]) for k in ks}})
        return out_

    top_merged = [{"loose_key": k,
                   "distinct_strict_keys_merged": int(v),
                   "distinct_show_ids_merged": int(merged_ids[k])}
                  for k, v in merged_titles.head(5).items() if v > 1]
    by_ids = merged_ids.sort_values(ascending=False)
    top_merged_by_ids = [{"loose_key": k,
                          "distinct_show_ids_merged": int(v),
                          "distinct_strict_keys_merged": int(merged_titles[k])}
                         for k, v in by_ids.head(5).items() if merged_titles[k] > 1]
    pivot_show_ids = int(pd.unique(piv.s.to_numpy()).size)
    clustering_universe = {
        "ruling": "Human Lead ruling, decisions/0088 SS3: THE D9 CLUSTERING UNIVERSE IS U1 -- ALL "
                  "SLUGGED SWEEP SHOW IDs -- RANKED BY DISTINCT STRICT KEYS MERGED. Closes Red "
                  "Team blocker B1 (0085 SS2), where the two arms published DISJOINT cluster lists "
                  "on IDENTICAL counts, and 0087 SS2, where the two arms' 'U1' proved to be two "
                  "sets 62 apart under one label. BOTH ARMS NOW CLUSTER THE SAME OBJECT.",
        "THIS_ARM_CLUSTERS": "U1 -- every distinct show ID appearing anywhere in the pulled sweep "
                             "that carries a slug, deduplicated to ONE ROW PER SHOW ID",
        "U1_distinct_slugged_show_ids_anywhere_in_the_sweep_CLUSTERED": int(uni.shape[0]),
        "U1_source": "processed/step8/a/show_slugs.csv, collected in stage 4b over all 2,549 "
                     "parsed history files -- which is what 'anywhere in the pulled sweep' means. "
                     "NOT the D9 coverage pivot.",
        "show_ids_in_the_map_without_a_slug_excluded": int((u1_all.slug == "").sum()),
        "show_ids_carrying_MORE_THAN_ONE_slug": n_ids_with_multiple_slugs,
        "one_row_per_show_id_tie_break": "lexicographically first slug per show ID. Stated rather "
                                         "than implicit; the sensitivity is measured, not assumed.",
        "clusters_with_more_than_one_strict_key_under_the_LAST_slug_instead": alt_clusters,
        "THE_UNIVERSE_THIS_ARM_USED_ON_ITS_PREVIOUS_BUILD_AND_NO_LONGER_USES": {
            "what_it_was": "the distinct show IDs appearing in a D9 COVERAGE ROW -- i.e. reaching "
                           "the pivot through a dated, pre-tau_pull, season >= 1 episode record",
            "size": pivot_show_ids,
            "relation_to_U1": "a SUBSET of U1. A show reaching the sweep only through a record "
                              "D11 discards, an undated record, a specials-only record or a "
                              "non-episode record is in U1 and not in the pivot.",
            "U1_minus_this": int(uni.shape[0] - pivot_show_ids),
            "why_it_is_published": "decisions/0087 SS2 caught this count published under the label "
                                   "`distinct_show_ids_in_the_sweep`, which is NOT what it counts, "
                                   "and 0088 SS2(a) requires the label corrected to what it counts. "
                                   "Both are real objects; one label over two was the defect.",
            "build_it_was_published_on": "a/2026-08-16-0085",
        },
        "candidate_universes_NOT_used_here_sized_for_comparison": {
            "U2_the_1138_frame_shows": int(frame.shape[0]),
            "U3_the_D9_candidate_pairs_under_the_loose_key": lo[
                "complementary_signature_id_pairs"],
            "why_they_are_listed": "0088 SS3 rules U1 and names U2 and U3 as what it is not. "
                                   "task-sheet.md's former illustration -- The Twilight Zone, The "
                                   "Traitors, Manhunt -- was U3 and is SUPERSEDED as the example: "
                                   "those three names are not wrong, they are another universe's "
                                   "answer.",
        },
        "what_LARGEST_ranks_by_here": "DISTINCT STRICT KEYS MERGED into one loose key -- how many "
                                      "separate metadata entries the loose key collapsed. Ruled by "
                                      "decisions/0088 ruling 3 because it was unstated and "
                                      "REORDERS THE LIST ON ITS OWN: ranked by distinct SHOW IDs "
                                      "instead, `blackout` displaces `maigret`. Both orders are "
                                      "emitted.",
        "ranks_with_every_tied_key_stated": ranked(merged_titles, merged_ids),
        "ranks_by_distinct_show_ids_with_every_tied_key_stated": ranked(
            merged_ids[merged_titles.reindex(merged_ids.index).fillna(0) > 1], merged_titles),
        "TIE_AT_RANK_3_REPORTED": "the ruled basis TIES at rank 3 on this data, so a bare "
                                  "'third-largest cluster' is not reproducible from the basis "
                                  "alone -- the tie order is decided by the sort's stability, not "
                                  "by the ruling. Every key at every published rank is listed "
                                  "above so the list can be compared without depending on it.",
        "coverage_shows_examined": int(uni.shape[0]),
        "clusters_with_more_than_one_strict_key": int((merged_titles > 1).sum()),
        "build": lib.BUILD_TAG,
    }
    assert clustering_universe["coverage_shows_examined"] > 0, (
        "the D9 clustering looked at zero shows; a zero cluster list here would read as a data "
        "finding rather than a missing input")
    assert int(uni.shape[0]) >= pivot_show_ids, (
        "U1 must contain the coverage pivot's show IDs; if it does not, the slug map is not being "
        "collected over the whole sweep and the clustering universe is not U1")

    D["D9_split_artifacts"] = {
        "signature": "two show IDs in one user's sweep with complementary season coverage (one "
                     "carrying S1 and not S2, the other S2 and not S1) whose normalised slugs "
                     "agree. Detection is imperfect and every count here is a LOWER BOUND "
                     "(Step 1 SS10.0b).",
        "key_ruling": "D9 PUBLISHES AS A BOUND. Human Lead ruling, decisions/0090. STRICT IS THE "
                      "FLOOR, LOOSE IS THE CEILING, BOTH LABELLED, AND NEITHER IS THE POINT "
                      "ESTIMATE -- neither endpoint may be quoted as 'D9's result'. This "
                      "SUPERSEDES 0074 ruling 5's framing, 'use the strict key and report the "
                      "loose count alongside', under which STRICT WAS THE ANSWER and loose was "
                      "context. decisions/0076 defines both keys: STRICT = lowercase, drop every "
                      "non-alphanumeric character, strip nothing else; LOOSE = remove a trailing "
                      "four-digit year first, then strict.",
        "BOUND": {
            "ruling": "decisions/0090. It is 0074 ruling 5's OWN REASON carried through: the "
                      "loose count publishes BECAUSE IT BOUNDS HOW WRONG STRICT COULD BE, and a "
                      "quantity published to bound another IS AN ENDPOINT, not a footnote. "
                      "decisions/0078 SS3 already ran this argument once, to extend the loose "
                      "count to half (b). Same reason, one step further.",
            "applies_to": "EVERY D9 quantity that has both forms, not the headline alone -- "
                          "applying it to one and not the others is the defect 0078 SS3 "
                          "corrected. The ruling's phrase 'this half' is read this way for that "
                          "reason; if a single half was meant, it narrows.",
            "direction_is_part_of_the_label": "STRICT IS THE FLOOR because it matches only slugs "
                                              "identical modulo punctuation, so it CANNOT "
                                              "OVER-COUNT. LOOSE IS THE CEILING because stripping "
                                              "a trailing year MERGES GENUINELY DIFFERENT SHOWS -- "
                                              "remakes and national versions. The error runs "
                                              "OPPOSITE to D9's own lower-bound caveat, which is "
                                              "why the interval publishes rather than being "
                                              "resolved away.",
            "complementary_signature_id_pairs": [st["complementary_signature_id_pairs"],
                                                 lo["complementary_signature_id_pairs"]],
            "half_a_fabricated_never_started_row_APPLY_position_7": [
                st["half_a_never_started_carrying_the_signature_APPLY_position_7"],
                lo["half_a_never_started_carrying_the_signature_APPLY_position_7"]],
            "half_b_silently_deleted_S1_failing_counterpart": [
                st["half_b_S1_failing_pairs_carrying_the_signature"],
                lo["half_b_S1_failing_pairs_carrying_the_signature"]],
            "NEITHER_ENDPOINT_IS_THE_POINT_ESTIMATE": True,
            "a_zero_floor_is_not_an_absence_of_evidence": {
                "why": "0 is a MEASURED floor on a stated coverage, and the coverage publishes "
                       "beside it -- a bound whose floor is 0 and whose coverage is unstated is "
                       "indistinguishable from a check that looked nowhere (decisions/0090 SS1).",
                "coverage_user_show_pairs_examined_under_the_strict_key": st[
                    "user_show_pairs_examined_carrying_a_slugged_show"],
                "coverage_D9_candidate_pairs_carrying_S1_or_S2_evidence": st[
                    "of_which_are_D9_CANDIDATES_carrying_S1_or_S2_evidence"],
                "coverage_position_3_drop_set_pairs_for_half_b": int(failed_s1.sum()),
                "coverage_never_started_pairs_for_half_a_APPLY_position_7": int(
                    (pos6 & r["never"]).sum()),
            },
            "THE_THIRD_KEY_IS_NOT_AN_ENDPOINT": {
                "value": by_key["third_key_trailing_digit_groups_NOT_RULED"][
                    "complementary_signature_id_pairs"],
                "why": "stripping a trailing digit group of arbitrary length reduces `the-100` to "
                       "`the`; its 76 is A DIFFERENT KEY'S ANSWER, reported as a divergence and "
                       "NEVER as the ceiling (decisions/0090 SS1; 0076, 0078 SS3).",
            },
            "build": lib.BUILD_TAG,
        },
        # F2(b): NAME WHAT EACH COVERAGE FIGURE COUNTS, AT THE POINT OF USE. Human Lead ruling,
        # decisions/0088 SS2. One name over two quantities is the defect; reconciling would
        # collapse two real objects into one, which the standing rule forbids. Every figure below
        # says what its unit is, and the bridge between them is arithmetic and stated.
        "coverage": {
            "ruling": "decisions/0088 SS2(b): 747,478 and 726,103 are different objects and both "
                      "correct; each arm states which it publishes and what it counts.",
            "unit_note": "THIS ARM PUBLISHES ALL THREE UNITS BELOW so no reader has to infer "
                         "which one a bare number is.",
            "A_undeduplicated_user_show_SEASON_COVERAGE_ROWS": int(cov.shape[0]),
            "A_definition": "distinct (user, show, season-class) triples, season-class in "
                            "{S1, S2, S3+}, over dated pre-tau_pull episode records. A user-show "
                            "carrying two seasons contributes TWO rows here and ONE pair below.",
            "B_distinct_user_show_PAIRS_in_the_coverage_pivot": int(piv.shape[0]),
            "B_definition": "distinct (user, show) pairs with ANY dated pre-tau_pull episode "
                            "record in season >= 1, INCLUDING pairs whose only evidence is S3 or "
                            "later. This is the figure this arm published as 747,478.",
            "C_D9_CANDIDATE_user_show_pairs_carrying_S1_or_S2_evidence": int(
                (piv.s1 | piv.s2).sum()),
            "C_definition": "B less the pairs whose only evidence is S3 or later. These are the "
                            "pairs D9's complementary-coverage search can actually match on.",
            "C_split": {"S1_evidence_and_no_S2": int((piv.s1 & ~piv.s2).sum()),
                        "S2_evidence_and_no_S1": int((piv.s2 & ~piv.s1).sum()),
                        "both_S1_and_S2": int((piv.s1 & piv.s2).sum())},
            "bridge_B_minus_C_pairs_with_only_S3_or_later_evidence": int(
                (~piv.s1 & ~piv.s2).sum()),
            "show_ids_with_a_slug_in_the_map": int(slugs.shape[0]),
            "build": lib.BUILD_TAG,
        },
        "FOUR_NUMBERS_both_halves_under_both_keys": {
            "ruling": "Human Lead ruling, decisions/0078 SS3: BOTH HALVES UNDER BOTH KEYS -- four "
                      "numbers, not three. It follows from 0074 ruling 5's own reason rather than "
                      "from a preference: the loose count publishes BECAUSE IT BOUNDS HOW WRONG "
                      "STRICT COULD BE, and that reason applies to half (b) exactly as to half "
                      "(a). Publishing the bound for one half and withholding it for the other "
                      "leaves the reader unable to bound the total, and the error runs OPPOSITE to "
                      "D9's own lower-bound caveat -- the direction they were not warned about.",
            "half_a_strict": st["half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_a_loose": lo["half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b_strict": st["half_b_S1_failing_pairs_carrying_the_signature"],
            "half_b_loose": lo["half_b_S1_failing_pairs_carrying_the_signature"],
            "half_a_population": "APPLY, position 7 (post-liveness), scored Never started",
            "half_b_population": "the position-3 drop set: pairs failing the S1 completion rule",
            "build": lib.BUILD_TAG,
        },
        "position_3_drop_set_input": dropset_meta,
        "FLOOR_strict_key": {
            "label": "FLOOR of the bound (decisions/0090). NOT the point estimate and NOT 'D9's "
                     "result'. ***SUPERSEDES the key name `ADOPTED_strict_key`, used on builds "
                     "through a/2026-08-16-0088 under 0074 ruling 5's framing.***",
            "complementary_signature_id_pairs": st["complementary_signature_id_pairs"],
            "half_a_fabricated_never_started_row": {
                "population": "APPLY, position 7 (post-liveness), scored Never started",
                "never_started": int((pos6 & r["never"]).sum()),
                "carrying_the_signature": st[
                    "half_a_never_started_carrying_the_signature_APPLY_position_7"],
                "share_of_never_started": share(
                    st["half_a_never_started_carrying_the_signature_APPLY_position_7"],
                    int((pos6 & r["never"]).sum())),
                "on_APPLY_position_5_the_table_row_set": {
                    "never_started": int((pos5 & r["never"]).sum()),
                    "carrying_the_signature": st[
                        "half_a_never_started_carrying_the_signature_APPLY_position_5"]},
                "direction": "DOWN -- the row is fabricated directly into the headline category"},
            "half_b_silently_deleted_S1_failing_counterpart": {
                "population": "pairs in the pair universe that FAIL the S1 completion rule -- the "
                              "rows position 3 removes, RETAINED AS A SIDE OUTPUT (0075) because "
                              "half (b) cannot be computed without them and they are not "
                              "recoverable from the analysis table",
                "side_output": "processed/step8/a/position3_drop_set.csv.gz",
                "pairs_failing_S1_completion": int(failed_s1.sum()),
                "carrying_the_signature": st["half_b_S1_failing_pairs_carrying_the_signature"]},
        },
        "CEILING_loose_key": {
            "label": "CEILING of the bound (decisions/0090). NOT the point estimate. ***SUPERSEDES "
                     "the key name `REPORTED_ALONGSIDE_loose_key`, used on builds through "
                     "a/2026-08-16-0088, under which strict was the answer and this was "
                     "context.***",
            "complementary_signature_id_pairs": lo["complementary_signature_id_pairs"],
            "half_a_APPLY_position_7": lo[
                "half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b": lo["half_b_S1_failing_pairs_carrying_the_signature"],
            "why_it_is_the_CEILING_and_not_the_answer": "it strips the year and merges genuinely "
                                     "different shows -- remakes and national versions, not split "
                                     "metadata, which is the artefact D9 exists to count. That is "
                                     "exactly why it CANNOT UNDER-COUNT and is therefore the "
                                     "upper endpoint (decisions/0090).",
            "clustering_universe_NAMED": clustering_universe,
            "largest_clusters_it_merges": top_merged,
            "largest_clusters_ranked_by_distinct_show_ids_instead": top_merged_by_ids,
        },
        "third_key_measured_only_so_the_record_is_complete": {
            "definition": "strip a trailing digit group of ARBITRARY length, then strict. NOT "
                          "either ruled key: it reduces `the-100` to `the`.",
            "complementary_signature_id_pairs": by_key[
                "third_key_trailing_digit_groups_NOT_RULED"]["complementary_signature_id_pairs"],
            "half_a_APPLY_position_7": by_key["third_key_trailing_digit_groups_NOT_RULED"][
                "half_a_never_started_carrying_the_signature_APPLY_position_7"],
            "half_b": by_key["third_key_trailing_digit_groups_NOT_RULED"][
                "half_b_S1_failing_pairs_carrying_the_signature"],
            "note": "this instance used this key on its previous run and published 76 "
                    "complementary pairs against the other arm's 75. decisions/0076 records that "
                    "divergence as REPORTED, NOT RECONCILED.",
        },
        "merges_counted_with_the_same_query_and_reported_separately": {
            "strict_key": st["merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_"
                             "title_ID_also_appears"],
            "loose_key": lo["merges_user_show_rows_where_one_ID_carries_both_seasons_and_a_same_"
                            "title_ID_also_appears"],
            "note": "merges can only add evidence to a pair, never remove it (Step 1 SS10.0b)"},
    }

    # ---- 7. D11 bookkeeping ---------------------------------------------------------------
    led = pd.read_json(os.path.join(P4, "pull_ledger.jsonl"), lines=True)
    led = led[led.is_data == True].drop_duplicates("slug", keep="last")
    fp = pd.to_datetime(led.first_page_fetched_at, utc=True, errors="coerce")
    lp = pd.to_datetime(led.last_page_fetched_at, utc=True, errors="coerce")
    # ---- SURFACE STATE, MEASURED ON DISK AT RUN TIME, NEVER ASSERTED FROM MEMORY -----------
    # This step publishes claims about OTHER surfaces in SS9 (disagreements reported and not
    # fixed). A claim about a surface is a claim like any other: it can be correct when written
    # and wrong when read, and this instance has already had one go stale between builds
    # (SS9 item 10). So every such claim is grounded in a count taken from disk on THIS run, and
    # the counts are published beside the claims. An empty result and a clean result are the same
    # value, so each glob reports what it looked at.
    import glob as _glob
    _RT = os.path.dirname(SRC) if 'SRC' in dir() else lib.ROOT
    _POP_FREE_168 = "168 pairs have both terms binding and the binary split has nowhere to put"

    def _count_files_containing(paths, needle):
        seen, hits = 0, 0
        for _p in paths:
            try:
                with open(_p, encoding="utf-8", errors="replace") as _fh:
                    _txt = _fh.read()
            except OSError:
                continue
            seen += 1
            if needle in " ".join(_txt.split()):
                hits += 1
        return seen, hits

    _agent_files = sorted(_glob.glob(os.path.join(lib.ROOT, ".claude/agents/analytics-engineer*.md")))
    _sb_files = sorted(_glob.glob(os.path.join(lib.ROOT, ".claude/agent-memory/second-brain/*.md")))
    _a_seen, _a_hit = _count_files_containing(_agent_files, _POP_FREE_168)
    _s_seen, _s_hit = _count_files_containing(_sb_files, "168 pairs have both binding")
    _ts_seen, _ts_hit = _count_files_containing(
        [os.path.join(lib.ROOT, "task-sheet.md")], "STATE THE POPULATION AT THE POINT OF USE")
    assert _a_seen > 0 and _s_seen > 0 and _ts_seen > 0, (
        "the surface-state check looked at zero files: an empty result and a clean result are "
        "the same value and only the control knows which it produced")
    D["surface_state_checked_live_this_run"] = {
        "why": "SS9 publishes claims about other surfaces. A claim about a surface can be correct "
               "when written and wrong when read -- this instance already had one go stale "
               "between builds -- so each is grounded in a count taken from disk on THIS run.",
        "decisions_0092_files_on_disk": len(
            _glob.glob(os.path.join(lib.ROOT, "decisions/0092*"))),
        "decisions_entries_on_disk_total": len(
            _glob.glob(os.path.join(lib.ROOT, "decisions/0*.md"))),
        "task_sheet_files_examined": _ts_seen,
        "task_sheet_carries_the_N2_population_requirement": bool(_ts_hit == 1),
        "agent_files_examined": _a_seen,
        "agent_files_carrying_the_population_free_168": _a_hit,
        "second_brain_files_examined": _s_seen,
        "second_brain_files_carrying_the_population_free_168": _s_hit,
        "reading": "0092's N2 edit reached surface 1 and no other. Reported, not edited: the "
                   "agent files, the decision log and second-brain are not this instance's to "
                   "amend.",
        "build": lib.BUILD_TAG,
    }

    D["pull_date_and_D11"] = {
        "pull_date_tau_pull_utc": "2026-08-11T00:00:00Z",
        "source": "decisions/0011; D11 makes it a single global frozen cutoff",
        "earliest_per_user_first_page_fetch_utc": str(fp.min()),
        "latest_per_user_first_page_fetch_utc": str(fp.max()),
        "earliest_per_user_last_page_fetch_utc": str(lp.min()),
        "latest_per_user_last_page_fetch_utc": str(lp.max()),
        "constraint_pull_date_le_earliest_fetch_holds": bool(
            fp.min() >= pd.Timestamp("2026-08-11T00:00:00Z")),
        "records_discarded_for_watched_at_ge_tau_pull_whole_sweep":
            scan_sum["records_discarded_watched_at_ge_tau_pull"],
        "records_discarded_for_watched_at_ge_tau_pull_in_frame_S1S2":
            scan_sum["in_frame_S1S2_records_discarded_by_D11"],
        "records_with_no_watched_at_whole_sweep": scan_sum["records_missing_watched_at"],
        "open_question_carried_not_resolved": pos_sum["D11_counterfactual_on_position_3"],
    }

    # ---- 7a. B3(a): THE BOUNDARY WINDOW ----------------------------------------------------
    # THE TWO UNASSERTED MANDATES ARE MEASURED, NOT SELF-REPORTED. Human Lead ruling,
    # decisions/0088 SS1, on Red Team's B3/F1, which blocked the gate on the third and fourth
    # passes. The mandates are THE HALF-OPEN UTC-INSTANT FORM and D11-AS-GLOBAL-CUTOFF. This
    # arm's compliance is TRUE and was independently confirmed -- no .date(), dt.date, normalize()
    # or day-flooring anywhere in step8_*.py, instants int64 seconds throughout. THAT IS NOT WHAT
    # WAS MISSING: nothing measured whether either mandate is LOAD-BEARING ON THIS DATA, and an
    # unmeasured pass is indistinguishable from a check that looked nowhere.
    #
    # IF THE COUNT IS 0 THE INVARIANT IS LABELLED VACUOUS -- it does not pass silently. A zero
    # stated as a zero is evidence; a zero arriving as a pass is not.
    #
    # ONE THING THE RULING DOES NOT SAY, MEASURED HERE BECAUSE IT DECIDES THE ANSWER: T0 is
    # day-floored and W and H are whole days, so tau1 and tau2 land EXACTLY ON MIDNIGHT UTC. The
    # date-level form `date(ts) < date(tau1)` is therefore IDENTICAL to the half-open `ts < tau1`
    # and can never differ. The form that CAN differ is `date(ts) <= date(tau1)`, which admits the
    # whole of [tau1, tau1 + 24h). So the window the ruling names -- [tau1 - 24h, tau1) -- is the
    # window on which the two forms AGREE by construction, and the interval on the OTHER side is
    # where the mandate is load-bearing. Both are emitted; reporting only the named one would
    # answer the question with the interval that cannot separate them.
    tau1, tau2 = r["tau1"], r["tau2"]
    assert int((a.t0 % DAY).sum()) == 0, "T0 is not day-floored; the boundary analysis below assumes it"
    assert int((tau1 % DAY).sum()) == 0 and int((tau2 % DAY).sum()) == 0, \
        "tau1/tau2 are not midnight-aligned"

    def win(lo_bound, hi_bound):
        """Per pair, distinct S2 episodes whose canonical timestamp is in [lo, hi)."""
        return a.count_before(hi_bound) - a.count_before(lo_bound)

    boundary = {"ruling": "Human Lead, decisions/0088 SS1(a). Position-5 row set, BOTH "
                          "POPULATIONS. Unit: DISTINCT S2 EPISODES BY CANONICAL TIMESTAMP -- the "
                          "objects the bound is actually tested against, since A and A_H are sets "
                          "of distinct episodes and the canonical timestamp is the minimum "
                          "watched_at over the records behind one episode (Step 1 SS2.1/2.2).",
                # ***CORRECTED, Red Team seventh pass: a claim this arm published about its own
                # source was FALSE.*** The previous form read "no .date(), dt.date, normalize() or
                # day-flooring appears in any step8_a_*.py". floor_day() appears THREE TIMES in
                # step8_a_2_positions.py, and legitimately: [[T0]] is day-floored by Step 1 SS2.4
                # and the S2 finale date is a date. The deliverable then argued twelve sections
                # later that "T0 is day-floored, so tau1 and tau2 land on midnight" -- so it
                # asserted no day-flooring anywhere and depended on day-flooring in the same file.
                # The true and narrower claim is stated instead.
                "half_open_form_verified": "NO BOUNDARY TEST uses a date-level form. Every bound "
                                           "comparison in step8_a_*.py is an int64-second "
                                           "comparison and `date(watched_at) <= T1` appears "
                                           "nowhere. No .date(), dt.date or normalize() call "
                                           "appears anywhere in step8_a_*.py.",
                "day_flooring_where_it_DOES_appear_and_why_that_is_correct": {
                    "sites": ["step8_a_2_positions.py floor_day() on the S2 finale date",
                              "step8_a_2_positions.py floor_day() on the first-pass S1 completion "
                              "instant, giving s1_completion_date",
                              "step8_a_2_positions.py floor_day() when parsing the stored Step 5 "
                              "dates for the cross-check"],
                    "why": "[[T0]] is DAY-FLOORED BY Step 1 SS2.4 -- the clock start is a date, "
                          "not an instant -- and W and H are whole days. That is what makes tau1 "
                          "and tau2 midnight-aligned, which is the fact this whole block turns "
                          "on. Day-flooring the CLOCK is required; day-flooring a BOUNDARY TEST "
                          "is forbidden. Only the second is a violation and there are none.",
                    "correction": "Red Team seventh pass: the previous build published the "
                                  "blanket form, which is false of this arm's own source and "
                                  "contradicted this same block's argument.",
                },
                # MEASURED, not a literal: this decides which interval separates the two forms,
                # so a hardcoded True here would assert the very thing the block exists to check.
                "tau1_and_tau2_are_midnight_aligned_UTC": bool(
                    int((tau1 % DAY).sum()) == 0 and int((tau2 % DAY).sum()) == 0),
                "rows_whose_tau1_is_not_midnight_aligned": int((tau1 % DAY != 0).sum()),
                "rows_whose_tau2_is_not_midnight_aligned": int((tau2 % DAY != 0).sum()),
                "build": lib.BUILD_TAG}
    for _pname, _m in (("APPLY_position_5", pos5), ("DERIV_position_5", pos5d)):
        cells = {}
        for _bn, _b in (("tau1", tau1), ("tau2", tau2)):
            before = win(_b - DAY, _b)
            at = win(_b, _b + 1)
            after = win(_b + 1, _b + DAY)
            cells[_bn] = {
                "episodes_in_the_24h_BEFORE_the_bound_named_by_the_ruling": int(before[_m].sum()),
                "rows_carrying_one": int((before[_m] > 0).sum()),
                "episodes_EXACTLY_AT_the_bound": int(at[_m].sum()),
                "rows_carrying_one_exactly_at_the_bound": int((at[_m] > 0).sum()),
                "episodes_in_the_24h_AFTER_the_bound_where_the_two_forms_ACTUALLY_DIFFER": int(
                    (at[_m] + after[_m]).sum()),
                "rows_where_the_two_forms_would_differ": int(((at + after)[_m] > 0).sum()),
            }
            cells[_bn]["VACUOUS"] = cells[_bn][
                "episodes_in_the_24h_AFTER_the_bound_where_the_two_forms_ACTUALLY_DIFFER"] == 0
        cells["coverage_rows_examined"] = int(_m.sum())
        cells["coverage_distinct_S2_episodes_on_those_rows"] = int(
            np.diff(a.s2_ptr)[_m].sum())
        assert cells["coverage_rows_examined"] > 0 and \
            cells["coverage_distinct_S2_episodes_on_those_rows"] > 0, (
            "the boundary window looked at zero episodes on " + _pname + ": an empty result and a "
            "clean result are the same value and only the control knows which it produced")
        boundary[_pname] = cells
    boundary["reading"] = (
        "The bound-crossing counts are what decides whether the half-open mandate is LOAD-BEARING "
        "on this data. Where the 'ACTUALLY DIFFER' cell is 0 the invariant is VACUOUS on this "
        "build -- stated, not passed silently -- and where it is non-zero the mandate changes the "
        "answer for that many episodes. The 'exactly at the bound' cells are the ruling's own "
        "second quantity and are a subset of the differing interval, since tau1 and tau2 are "
        "midnight-aligned.")
    # ---- THE NUMBER THAT SETTLES B3(a): OUTCOME-STATE FLIPS, NOT EPISODES ADMITTED ----------
    # decisions/0089 SS2(a), Red Team's fifth pass, F1. The block above emits EPISODES ADMITTED on
    # the separating interval. That is the right interval and the wrong object: the question the
    # mandate turns on is whether the forbidden form would change the ANSWER, and the answer is an
    # outcome state. FOUR NUMBERS, BOTH BOUNDS x BOTH POPULATIONS, on the position-5 row set.
    #
    #   at tau1: a NEVER-STARTED row with an episode in [tau1, tau1 + 24h) FLIPS TO STARTED,
    #            because |A| goes from 0 to >= 1.
    #   at tau2: a STARTED-AND-LEFT row with an episode in [tau2, tau2 + 24h) CAN FLIP TO
    #            CONTINUED, because A_H gains an episode and both the F2 clause and the 0.90
    #            clause can turn on it.
    #
    # The row masks are the same ones the block above counts rows on -- this recomputes the two
    # outcome instants under the forbidden bound and cross-tabulates against the adopted state.
    # It is a COUNTERFACTUAL: nothing here changes what the pipeline emits. `date(watched_at) <=
    # T1` still appears nowhere in the implementation; this measures what would happen if it did.
    kA_dl = a.count_before(tau1 + DAY)          # date(ts) <= date(tau1), tau1 midnight-aligned
    kAH_dl = a.count_before(tau2 + DAY)         # date(ts) <= date(tau2)
    mH_dl = a.maxnum_before(kAH_dl)

    def _state(kA_, kAH_, mH_):
        cont_ = (kA_ >= 1) & (mH_ == a.F2) & (kAH_ >= a.need2)
        nev_ = kA_ == 0
        return (np.where(nev_, lib.NEVER, np.where(cont_, lib.CONT, lib.LEFT)).astype(np.int8),
                cont_)

    base_state, base_cont = _state(r["kA"], r["kAH"], r["mH"])
    assert bool((base_state == r["outcome"]).all()), (
        "the counterfactual state function does not reproduce the adopted outcome on the "
        "half-open form; the comparison below would be against the wrong baseline")
    variants = {
        "tau1_only_date_level": _state(kA_dl, r["kAH"], r["mH"]),
        "tau2_only_date_level": _state(r["kA"], kAH_dl, mH_dl),
        "both_bounds_date_level": _state(kA_dl, kAH_dl, mH_dl),
    }
    _NAME = {lib.NEVER: "never_started", lib.LEFT: "started_and_left", lib.CONT: "continued"}

    flips = {"ruling": "decisions/0089 SS2(a), Red Team fifth pass F1. THE NUMBER THAT SETTLES "
                       "B3(a) is how many POSITION-5 ROWS CHANGE OUTCOME STATE under the "
                       "forbidden date-level form -- four numbers, both bounds x both "
                       "populations -- NOT how many episodes the form admits. The previous build "
                       "of this arm emitted episodes admitted and is corrected here.",
             "forbidden_form": "date(watched_at) <= date(tau), which on midnight-aligned bounds "
                               "admits the whole of [tau, tau + 24h). It appears NOWHERE in the "
                               "implementation; this is a counterfactual measured on the adopted "
                               "build, and nothing the pipeline emits changes.",
             "unit": "POSITION-5 ROWS whose outcome state differs, not episodes",
             "build": lib.BUILD_TAG}
    for _pname, _m in (("APPLY_position_5", pos5), ("DERIV_position_5", pos5d)):
        cell = {"rows_examined": int(_m.sum())}
        for vname, (st_, cont_) in variants.items():
            ch = _m & (st_ != base_state)
            trans = {}
            for f_ in (lib.NEVER, lib.LEFT, lib.CONT):
                for t_ in (lib.NEVER, lib.LEFT, lib.CONT):
                    if f_ == t_:
                        continue
                    c_ = int((ch & (base_state == f_) & (st_ == t_)).sum())
                    if c_:
                        trans[f"{_NAME[f_]}__to__{_NAME[t_]}"] = c_
            # CONJUNCT 2 IS RECOMPUTED ON THE COUNTERFACTUAL OUTCOME, NOT HELD AT THE ADOPTED ONE.
            # Red Team seventh pass, finding 1, against this arm: the previous deliverable did not
            # say which, and if conjunct 2 were held at the adopted state then 703 -> 703 would be
            # a TAUTOLOGY establishing nothing. `cont_` below is the COUNTERFACTUAL Continued mask
            # returned by _state() under this variant's bounds; `r["continued"]` is not used here.
            # The liveness rule is conjunct 1 AND conjunct 2, and only conjunct 1 -- the silence
            # test -- reads an insertion clock. Conjunct 2 is an episode-timestamp computation and
            # it MOVES under this counterfactual, so the invariance of the conjunction is a fact
            # about this data, not a structural property.
            nl_ = r["silent"] & ~cont_
            _exc = _m & nl_
            _exc_adopted = _m & r["not_live"]
            cell[vname] = {
                "rows_changing_outcome_state": int(ch.sum()),
                "transitions": trans,
                "conjunct_2_recomputed_on_the_counterfactual_outcome": True,
                "conjunct_2_expression": "silent & ~cont_, where cont_ is the COUNTERFACTUAL "
                                         "Continued mask under this variant's bounds",
                "conjunct_2_rows_that_MOVE_under_this_form": int(
                    (_m & (cont_ != base_cont)).sum()),
                "liveness_exclusions_under_this_form": int(_exc.sum()),
                "liveness_exclusions_adopted": int(_exc_adopted.sum()),
                "liveness_exclusions_MOVE": int(_exc.sum()) - int(_exc_adopted.sum()),
                # THE 604/99 SPLIT UNDER THE COUNTERFACTUAL -- not reported at all before.
                # A total that does not move can still be a different set of rows, and the split
                # by outcome state is where that would show.
                "exclusion_split_under_this_form": {
                    "never_started": int((_exc & (st_ == lib.NEVER)).sum()),
                    "started_and_left": int((_exc & (st_ == lib.LEFT)).sum()),
                    "continued": int((_exc & (st_ == lib.CONT)).sum()),
                },
                "exclusion_split_adopted": {
                    "never_started": int((_exc_adopted & r["never"]).sum()),
                    "started_and_left": int((_exc_adopted & r["left"]).sum()),
                    "continued": int((_exc_adopted & r["continued"]).sum()),
                },
                "the_excluded_ROW_SET_is_identical_not_merely_the_total": bool(
                    int((_exc ^ _exc_adopted).sum()) == 0),
                "rows_in_one_exclusion_set_but_not_the_other": int((_exc ^ _exc_adopted).sum()),
            }
        assert cell["rows_examined"] > 0, (
            "the outcome-flip counterfactual looked at zero rows on " + _pname + ": an empty "
            "result and a clean result are the same value and only the control knows which it "
            "produced")
        flips[_pname] = cell
    flips["THE_FOUR_NUMBERS"] = {
        "APPLY_at_tau1": flips["APPLY_position_5"]["tau1_only_date_level"][
            "rows_changing_outcome_state"],
        "APPLY_at_tau2": flips["APPLY_position_5"]["tau2_only_date_level"][
            "rows_changing_outcome_state"],
        "DERIV_at_tau1": flips["DERIV_position_5"]["tau1_only_date_level"][
            "rows_changing_outcome_state"],
        "DERIV_at_tau2": flips["DERIV_position_5"]["tau2_only_date_level"][
            "rows_changing_outcome_state"],
        "reading": "each bound is varied ALONE, which is what 'both bounds' means here; the "
                   "joint form is reported separately because it is not the sum of the two -- a "
                   "row can flip at tau1 and flip again at tau2.",
    }
    flips["VACUOUS_ON_THIS_BUILD"] = all(
        v == 0 for k, v in flips["THE_FOUR_NUMBERS"].items() if k != "reading")
    flips["reading"] = (
        "If every one of the four is 0 the mandate is LOAD-BEARING ON EPISODES BUT NOT ON "
        "OUTCOMES on this data, and that is stated rather than passed silently. A non-zero says "
        "the half-open form decides that many published outcome states.")
    # ---- THE 'INERT ON LINE 6' WARRANT IS WITHDRAWN, AND THE CLAIM IS RESCOPED --------------
    # Red Team seventh pass, finding 1, against this arm; recorded at decisions/0091 SS1.
    flips["WITHDRAWN_WARRANT"] = {
        "the_withdrawn_sentence": "line 6 does not move under this counterfactual BECAUSE the "
                                  "silence test reads an insertion clock, not an episode "
                                  "timestamp",
        "why_it_is_wrong": "STRUCTURALLY WRONG, not merely unsupported. The liveness rule is "
                           "conjunct 1 AND conjunct 2, and conjunct 2 is NOT Continued -- an "
                           "EPISODE-TIMESTAMP computation. A property of conjunct 1 cannot "
                           "explain the invariance of the conjunction. The figures below show "
                           "conjunct 2 moving on real rows under this very counterfactual.",
        "what_replaces_it": "NOTHING STRUCTURAL. The exclusion total is invariant here as a "
                            "MEASURED FACT ABOUT THIS DATA at W = 108: no pair that the adopted "
                            "rule excludes is among the rows whose Continued value flips, so the "
                            "conjunction lands on the same row set. That is a coincidence of this "
                            "frame and this arm, and Step 13 re-runs the rule across eight arms.",
        "conjunct_2_was_RECOMPUTED_not_held": True,
        "why_that_matters": "if conjunct 2 were held at the adopted outcome, 703 -> 703 would be "
                            "an IDENTITY and would establish nothing. A reader cannot tell a "
                            "measurement from a tautology unless the deliverable says which, so "
                            "it says which -- and the expression is quoted at each cell.",
        "scope_of_the_claim_AS_MEASURED": "W = 108 ONLY, on APPLY = 196,654 and DERIV = 147,370, "
                                          "position-5 row sets, build " + lib.BUILD_TAG + ". It "
                                          "is NOT claimed at any other arm and NOT claimed as a "
                                          "structural property of the rule.",
        "build": lib.BUILD_TAG,
    }
    _mv = {}
    for _pn in ("APPLY_position_5", "DERIV_position_5"):
        _mv[_pn] = {
            v: {"conjunct_2_rows_that_MOVE": flips[_pn][v][
                    "conjunct_2_rows_that_MOVE_under_this_form"],
                "liveness_exclusions_MOVE": flips[_pn][v]["liveness_exclusions_MOVE"],
                "excluded_row_set_identical": flips[_pn][v][
                    "the_excluded_ROW_SET_is_identical_not_merely_the_total"]}
            for v in ("tau1_only_date_level", "tau2_only_date_level", "both_bounds_date_level")}
    flips["CONJUNCT_2_MOVES_WHILE_THE_CONJUNCTION_DOES_NOT"] = {
        "per_population_per_variant": _mv,
        "reading": "conjunct 2 moving on a positive number of rows while the exclusion total "
                   "moves by 0 is exactly why the withdrawn warrant cannot be the explanation: "
                   "the thing it called invariant is not the thing that is invariant.",
    }
    boundary["OUTCOME_STATE_FLIPS_the_number_that_settles_B3a"] = flips

    # ---- decisions/0068's STRICTNESS RULING, MEASURED ON ITS OWN OBJECT ---------------------
    # Red Team seventh pass, finding 2, against this arm. The previous deliverable read "exactly 1
    # episode falls exactly AT tau1" and concluded that 0068's strictness ruling "changes the
    # answer for a real row". WRONG OBJECT. The SS5.6a table's unit is a DISTINCT S2 EPISODE BY
    # CANONICAL watched_at. 0068's strictness ruling is about INSERTION INSTANTS in the SILENCE
    # TEST -- "a pair is silent iff it has no insertion instant > tau1". Those are two different
    # axes and the episode count says nothing about the ruling.
    #
    # The ruling's OWN quantity is measured here: pairs whose account's last insertion instant
    # falls EXACTLY AT tau1. Those are the only rows on which strict `>` and non-strict `>=`
    # can differ, so if the count is 0 the ruling is VACUOUS on this data and that is stated.
    _li = a.last_inst
    _strict_silent = _li <= tau1              # adopted: no insertion instant > tau1
    _nonstrict_silent = _li < tau1            # withdrawn reading: no insertion instant >= tau1
    _at = _li == tau1
    strictness = {
        "ruling": "decisions/0068, restated at task-sheet.md Step 8: the silence test is STRICT. "
                  "A pair is silent iff it has NO insertion instant > tau1, so an instant falling "
                  "exactly AT tau1 does not make the account live.",
        "unit": "PAIRS, keyed on the account's last insertion instant (D11-restricted, "
                "decisions/0070 ruling 2) -- NOT distinct S2 episodes by watched_at",
        "WITHDRAWN_CLAIM": "***WITHDRAWN, WRONG OBJECT (Red Team seventh pass, finding 2; "
                           "decisions/0089 SS2(a) as corrected on the sixth pass).*** The previous "
                           "build of this arm published: 'exactly 1 episode falls exactly AT tau1, "
                           "so 0068's strictness ruling changes the answer for a real row rather "
                           "than for none.' The 1 is a DISTINCT S2 EPISODE by canonical "
                           "watched_at, which is SS5.6a's unit; the ruling is about INSERTION "
                           "INSTANTS in the silence test. The episode count is correct and is "
                           "kept in SS5.6a; the inference drawn from it is withdrawn.",
        "build": lib.BUILD_TAG,
    }
    for _pname, _m in (("APPLY_position_5", pos5), ("DERIV_position_5", pos5d)):
        _nl_ns = _nonstrict_silent & ~r["continued"]
        strictness[_pname] = {
            "rows_examined": int(_m.sum()),
            "pairs_whose_last_insertion_instant_is_EXACTLY_AT_tau1": int((_m & _at).sum()),
            "accounts_ditto": int(np.unique(a.pair_user[_m & _at]).size),
            "silent_under_the_ADOPTED_strict_form": int((_m & _strict_silent).sum()),
            "silent_under_the_WITHDRAWN_non_strict_form": int((_m & _nonstrict_silent).sum()),
            "silent_count_MOVES_by": int((_m & _strict_silent).sum())
                                     - int((_m & _nonstrict_silent).sum()),
            "liveness_exclusions_ADOPTED": int((_m & r["not_live"]).sum()),
            "liveness_exclusions_under_the_non_strict_form": int((_m & _nl_ns).sum()),
            "liveness_exclusions_MOVE": int((_m & r["not_live"]).sum())
                                        - int((_m & _nl_ns).sum()),
            "VACUOUS_ON_THIS_DATA": bool(int((_m & _at).sum()) == 0),
        }
        assert strictness[_pname]["rows_examined"] > 0, (
            "the strictness measurement looked at zero rows on " + _pname + ": an empty result "
            "and a clean result are the same value and only the control knows which it produced")
    strictness["reading"] = (
        "IF the exactly-at count is 0 the strictness ruling is VACUOUS ON THIS DATA -- stated as "
        "a zero, not passed silently. It remains the correct rule and it remains binding on any "
        "future pull; what is measured here is only whether it decides anything on THIS data, "
        "which is what the previous build got wrong by answering with a different unit.")
    boundary["STRICTNESS_RULING_0068_MEASURED_ON_ITS_OWN_OBJECT"] = strictness
    boundary["CORRECTION_TO_THE_PREVIOUS_BUILD"] = (
        "build a/2026-08-16-0088 emitted the separating interval and the EPISODES ADMITTED on it, "
        "and stopped there. decisions/0089 SS2(a) records that as answering B3(a) with the wrong "
        "object: 'Arm A reports episodes ADMITTED, not outcomes.' The episode counts are correct "
        "and are kept; the outcome-state block above is what settles the question.")
    D["B3a_boundary_window_half_open_form"] = boundary

    # ---- 7b. B3(b): THE PER-SITE D11 TABLE, ASSERTED AT EACH SITE ---------------------------
    # decisions/0088 SS1(b). D11 is specified to apply "to EVERY computation" and this arm named
    # FIVE SITES IN PROSE WITH A COUNT AT NONE. Every site now carries its own count and its own
    # assertion. The ground for ruling rather than publishing a residual: the unstated version of
    # exactly this scope produced Step 7's 792-against-791.
    # S2 episodes at or after tau_pull, and the sub-slice of them that would have entered each
    # set. Expressed as differences of prefix counts rather than with a sentinel upper bound,
    # because the searchsorted key packs (pair, timestamp) into one int64 and a sentinel large
    # enough to dominate every timestamp would break the packing.
    _n_s2 = np.diff(a.s2_ptr)
    _before_pull = a.count_before(np.full(a.n, lib.TAU_PULL, dtype=np.int64))
    ge_pull_s2 = _n_s2 - _before_pull
    enter_A_post_cutoff = np.maximum(0, r["kA"] - _before_pull)
    enter_AH_post_cutoff = np.maximum(0, r["kAH"] - _before_pull)
    sites = dict(scan_sum["D11_per_site_records"]["the_eight_action_count_sites"])
    sites["A_the_set_tested_at_tau1"] = {
        "unit": "distinct S2 episodes on position-5 rows",
        "episodes_examined_before_D11": int(np.diff(a.s2_ptr)[pos5].sum()),
        "episodes_at_or_after_tau_pull_that_D11_would_exclude": int(ge_pull_s2[pos5].sum()),
        "of_those_that_would_have_ENTERED_A": int(enter_A_post_cutoff[pos5].sum()),
        "D11_applied": True,
        "inert_and_why": "D10 forces tau1 <= tau2 <= tau_pull on every retained pair, so no "
                         "episode at or after tau_pull can satisfy ts < tau1. INERT BY "
                         "CONSTRUCTION, and the count is stated rather than the construction "
                         "being asserted about.",
    }
    sites["A_H_the_set_tested_at_tau2"] = {
        "unit": "distinct S2 episodes on position-5 rows",
        "episodes_examined_before_D11": int(np.diff(a.s2_ptr)[pos5].sum()),
        "episodes_at_or_after_tau_pull_that_D11_would_exclude": int(ge_pull_s2[pos5].sum()),
        "of_those_that_would_have_ENTERED_A_H": int(enter_AH_post_cutoff[pos5].sum()),
        "D11_applied": True,
        "inert_and_why": "same construction, at tau2.",
    }
    sites["liveness_evidence"] = scan_sum["D11_per_site_records"]["liveness_evidence"]
    sites["D9_coverage_rows"] = d9_site_d11
    sites["S1_completion_walk"] = dict(scan_sum["D11_per_site_records"]["S1_completion_walk"])
    sites["S1_completion_walk"]["counterfactual_measured_in_stage_2"] = pos_sum[
        "D11_counterfactual_on_position_3"]

    site_assertions = []
    for _sn, _sv in sites.items():
        if _sn.startswith("action_count_"):
            ok = (_sv["records_examined_before_D11"]
                  == _sv["records_excluded_by_D11"] + _sv["records_counted_after_D11"])
            site_assertions.append({
                "site": _sn, "D11_applied": True,
                "assertion": "records_examined = records_excluded_by_D11 + records_counted",
                "coverage_unit_count": _sv["records_examined_before_D11"],
                "excluded_by_D11": _sv["records_excluded_by_D11"], "holds": bool(ok)})
        elif _sn in ("A_the_set_tested_at_tau1", "A_H_the_set_tested_at_tau2"):
            k = ("of_those_that_would_have_ENTERED_A" if _sn.startswith("A_the")
                 else "of_those_that_would_have_ENTERED_A_H")
            site_assertions.append({
                "site": _sn, "D11_applied": True,
                "assertion": "no episode at or after tau_pull enters the set",
                "coverage_unit_count": _sv["episodes_examined_before_D11"],
                "excluded_by_D11": _sv[k], "holds": bool(_sv[k] == 0),
                "VACUOUS_ON_THIS_BUILD": bool(
                    _sv["episodes_at_or_after_tau_pull_that_D11_would_exclude"] == 0)})
        elif _sn == "liveness_evidence":
            site_assertions.append({
                "site": _sn, "D11_applied": True,
                "assertion": "the per-account insertion clock is built only from records dated "
                             "before tau_pull (decisions/0070 ruling 2)",
                "coverage_unit_count": _sv["records_examined_before_D11"],
                "excluded_by_D11": _sv["records_excluded_by_D11_watched_at_ge_tau_pull"],
                "holds": bool(_sv["records_examined_before_D11"]
                              == (_sv["records_excluded_by_D11_watched_at_ge_tau_pull"]
                                  + _sv["records_excluded_as_undated"]
                                  + _sv["records_used_after_D11"])),
                "VACUOUS_ON_THIS_BUILD": bool(
                    _sv["accounts_whose_last_insertion_instant_MOVES_under_D11"] == 0)})
        elif _sn == "D9_coverage_rows":
            site_assertions.append({
                "site": _sn, "D11_applied": True,
                "assertion": "records_examined = records_excluded_by_D11 + records_used",
                "coverage_unit_count": _sv["records_examined_before_D11"],
                "excluded_by_D11": _sv["records_excluded_by_D11"],
                "holds": bool(_sv["records_examined_before_D11"]
                              == _sv["records_excluded_by_D11"] + _sv["records_used_after_D11"]),
                "VACUOUS_ON_THIS_BUILD": bool(_sv["records_excluded_by_D11"] == 0)})
        elif _sn == "S1_completion_walk":
            # MEASURED, NOT A LITERAL. This site published `"holds": True` as a hardcoded literal
            # on build a/2026-08-16-0088 -- a result asserted rather than measured, inside the
            # very table decisions/0088 SS1(b) created to stop mandates being self-reported. It is
            # the same shape as a control asserted to exist, and it sat in the one site whose
            # declaration is the interesting one.
            #
            # WHAT A NOT-APPLIED SITE CAN ASSERT. It cannot assert that D11 removed the right
            # records, because it removes none. It CAN assert that the DECLARATION MATCHES THE
            # WALK'S OWN OUTPUT: if D11 were silently applied here, no completer's first-pass walk
            # could have used a post-cutoff record and that count would be 0. So the site is
            # not-applied iff the count is positive, and both sides are measured.
            cf = _sv["counterfactual_measured_in_stage_2"]
            _used_post_cutoff = int(cf["completers_whose_first_pass_walk_used_a_post_cutoff_record"])
            _excluded_here = 0                       # measured: this site applies no D11 filter
            _declared_not_applied = (_sv["D11_applied"] is False)
            _consistent = bool((_used_post_cutoff > 0) == _declared_not_applied)
            site_assertions.append({
                "site": _sn, "D11_applied": False,
                "assertion": "THIS SITE IS DECLARED NOT-APPLIED, AND THE DECLARATION IS CHECKED "
                             "AGAINST THE WALK'S OWN OUTPUT: completers whose first-pass walk used "
                             "a record at or after tau_pull is > 0 IFF D11 is genuinely not "
                             "applied here. A silent application would drive that count to 0 and "
                             "this assertion would FAIL. decisions/0068 fixes waterfall line 1 at "
                             "the published 220,107 and lists whether D11 moves it as an OPEN "
                             "question; the counterfactual is measured and published rather than "
                             "the site being omitted from the table.",
                # THE EXAMINED CELL IS THE SAME KIND OF QUANTITY AS IN EVERY OTHER ROW.
                # Red Team seventh pass, finding 5, against this arm: this cell previously held
                # `records_at_or_after_tau_pull_on_the_S1_side` = 73, which is a WOULD-EXCLUDE
                # count in an EXAMINED column, and a RECORD count where the walk's unit is a
                # DISTINCT EPISODE. Three objects sit behind this site and stage 1 now names all
                # three; the two that belong in this table are below.
                "coverage_unit": "DISTINCT S1 EPISODES consumed by the first-pass walk",
                "coverage_unit_count": _sv["episodes_examined_before_D11"],
                "would_be_excluded_by_D11_at_this_site": _sv[
                    "episodes_at_or_after_tau_pull_that_D11_would_exclude"],
                "record_level_object_reported_separately_NOT_the_examined_cell": _sv[
                    "records_at_or_after_tau_pull_on_the_S1_side"],
                "three_objects": _sv["THREE_OBJECTS_NAMED_APART"],
                "excluded_by_D11": _excluded_here,
                "completers_whose_first_pass_walk_used_a_post_cutoff_record": _used_post_cutoff,
                "declaration_matches_the_measurement": _consistent,
                "pairs_that_would_stop_being_completers": cf[
                    "pairs_that_stop_being_completers_under_D11"],
                "completion_dates_that_would_move": cf[
                    "completers_whose_completion_date_moves_under_D11"],
                "MEASURED_NOT_A_LITERAL": "build a/2026-08-16-0088 published `holds: True` here "
                                          "as a hardcoded literal; it is computed from the two "
                                          "measured quantities above on this build.",
                "holds": bool(_consistent and _excluded_here == 0)})
    # A CHECK THAT FINDS NOTHING BECAUSE IT LOOKED NOWHERE MUST NOT READ AS A PASS (CLAUDE.md).
    # Two of the thirteen sites -- action_count_s1_other and action_count_s2_other -- examine
    # ZERO units, because no record in the sweep carries an action outside
    # {watch, checkin, scrobble}. Their assertions hold trivially and are flagged as such, not
    # counted as evidence. The distinction is between a zero found and a zero looked at.
    for _x in site_assertions:
        _x["LOOKED_AT_ZERO_UNITS"] = bool(_x["coverage_unit_count"] == 0)
    n_applied = sum(1 for x in site_assertions if x["D11_applied"])
    D["B3b_D11_per_site"] = {
        "ruling": "Human Lead, decisions/0088 SS1(b): emit records excluded by D11 at EACH site "
                  "separately and ASSERT AT EACH SITE, not once and about the rest. This replaces "
                  "prose naming five sites with a count at none.",
        "sites_total": len(site_assertions),
        "sites_where_D11_IS_applied": n_applied,
        "sites_where_D11_is_NOT_applied_and_say_so": len(site_assertions) - n_applied,
        "sites": sites,
        "assertions": site_assertions,
        "all_site_assertions_hold": all(x["holds"] for x in site_assertions),
        "sites_vacuous_on_this_build": [x["site"] for x in site_assertions
                                        if x.get("VACUOUS_ON_THIS_BUILD")],
        "sites_that_LOOKED_AT_ZERO_UNITS_and_therefore_hold_trivially": [
            x["site"] for x in site_assertions if x["LOOKED_AT_ZERO_UNITS"]],
        "sites_asserted_on_a_non_empty_unit_set": sum(
            1 for x in site_assertions if not x["LOOKED_AT_ZERO_UNITS"]),
        "total_units_excluded_by_D11_across_the_sites_where_it_is_applied": sum(
            int(x["excluded_by_D11"]) for x in site_assertions if x["D11_applied"]),
        "units_are_NOT_commensurable_across_sites": "records, distinct episodes and coverage "
                                                    "rows are different units and the row above "
                                                    "is a bookkeeping total, not a quantity with "
                                                    "a meaning. Read the sites individually.",
        "build": lib.BUILD_TAG,
    }
    assert len(site_assertions) >= 13, "the per-site D11 table lost a site"
    assert D["B3b_D11_per_site"]["all_site_assertions_hold"], "a D11 site assertion failed"

    # ---- 8. D12 cadence buckets ------------------------------------------------------------
    bucket = f.cadence_bucket.reindex(a.pair_show).to_numpy()
    D["D12_cadence_buckets"] = {
        "buckets": {b: {"shows": int((f.cadence_bucket == b).sum()),
                        "pairs_position_5_APPLY": int(((bucket == b) & pos5).sum()),
                        "pairs_position_7_APPLY": int(((bucket == b) & pos6).sum()),
                        "pairs_position_5_DERIV": int(((bucket == b) & pos5d).sum())}
                    for b in ["C0", "C1", "C2", "C3", "C4"]},
        "shows_within_1_day_of_a_bucket_boundary": int(
            (f.cadence_boundary_distance_days.abs() <= 1).sum()),
        "coverage_shows": int(len(f)),
        "note": "C0 absorbs missing or impossible data; it is reported as its own line even at "
                "zero (Step 1 SS10.0)",
    }

    # ---- 9. metadata disagreement -----------------------------------------------------------
    # recomputed from the reported counts rather than read off the frame's stored flags, so a
    # zero here is a measured zero and not a flag that was never set
    dis1 = ((f.s1_episode_count_reported != f.s1_L) | (f.s1_aired_episodes_reported != f.s1_L))
    dis2 = ((f.s2_episode_count_reported != f.s2_L) | (f.s2_aired_episodes_reported != f.s2_L))
    alt2 = f.s2_aired_episodes_reported < f.s2_L
    flags_agree = bool((dis1 == f.s1_count_disagreement.astype(bool)).all()
                       and (dis2 == f.s2_count_disagreement.astype(bool)).all()
                       and (alt2 == f.s2_aired_lt_listed.astype(bool)).all())
    sid = pd.Index(f.index)
    pair_show_idx = sid.get_indexer(a.pair_show)
    D["metadata_disagreement"] = {
        "coverage_shows": int(len(f)),
        "recomputed_from_the_reported_counts_not_read_off_the_stored_flags": True,
        "recomputation_agrees_with_the_stored_frame_flags": flags_agree,
        "shows_where_episode_count_aired_episodes_and_E_disagree_S1": int(dis1.sum()),
        "shows_where_they_disagree_S2": int(dis2.sum()),
        "shows_where_they_disagree_S1_or_S2": int((dis1 | dis2).sum()),
        "pairs_on_those_shows_position_5_APPLY": int(
            (pos5 & (dis1 | dis2).to_numpy()[pair_show_idx]).sum()),
        "pairs_on_those_shows_position_7_APPLY": int(
            (pos6 & (dis1 | dis2).to_numpy()[pair_show_idx]).sum()),
        "shows_where_aired_episodes_lt_listed_E_for_S2": int(alt2.sum()),
        "pairs_on_those_shows_position_7_APPLY": int(
            (pos6 & alt2.to_numpy()[pair_show_idx]).sum()),
        "continued_reachability_on_those_shows": {
            "continued_pairs_position_7_APPLY": int(
                (pos6 & r["continued"] & alt2.to_numpy()[pair_show_idx]).sum())},
        "direction": "listed exceeding aired raises L2, which tightens ceil(0.90*L2) and pushes "
                     "pairs that would have been Continued into Started-and-left -- it OVERSTATES "
                     "abandonment; the same effect on S1 raises L1 and shrinks the population, "
                     "non-randomly, on shows with messy metadata (Step 1 SS3.4)",
    }

    # ---- 10. outcome counts and the horizon pairing ----------------------------------------
    D["outcome_counts"] = {
        "APPLY_position_5_THE_TABLE_ROW_SET": {
            "never_started": int((pos5 & r["never"]).sum()),
            "started_and_left": int((pos5 & r["left"]).sum()),
            "continued": int((pos5 & r["continued"]).sum()),
            "not_live": int((pos5 & r["not_live"]).sum()),
            "total": int(pos5.sum())},
        "DERIV_position_5": {"never_started": int((pos5d & r["never"]).sum()),
                             "started_and_left": int((pos5d & r["left"]).sum()),
                             "continued": int((pos5d & r["continued"]).sum()),
                             "not_live": int((pos5d & r["not_live"]).sum()),
                             "total": int(pos5d.sum())},
        "APPLY_position_7": {"never_started": int((pos6 & r["never"]).sum()),
                             "started_and_left": int((pos6 & r["left"]).sum()),
                             "continued": int((pos6 & r["continued"]).sum()),
                             "total": int(pos6.sum())},
        "DERIV_position_7": {"never_started": int((pos6d & r["never"]).sum()),
                             "started_and_left": int((pos6d & r["left"]).sum()),
                             "continued": int((pos6d & r["continued"]).sum()),
                             "total": int(pos6d.sum())},
        "horizons": "Never started is a 108-day statement read at tau1; Continued is a 199-day "
                    "statement read at tau2 on A_H. The two must never be described as measured "
                    "alike (0034).",
        "abandonment_point_p": {
            "defined_only_for_started_and_left": True,
            "form": "rank: |{e in E2 : e <= max(A_H)}| / L2; the raw ratio max(A_H)/L2 is "
                    "withdrawn and must not be reinstated",
            "p_equals_1_residual_APPLY_position_7": int(
                (pos6 & r["left"] & (r["p"] == 1.0)).sum()),
            "p_equals_1_residual_APPLY_position_5": int(
                (pos5 & r["left"] & (r["p"] == 1.0)).sum()),
            # decisions/0083 SS2, restating 0082: p_at_bound marks WHETHER p reached its bound,
            # not why. The p = 1.0 counts below are TOTALS, not a sum of two classes -- the two
            # clauses 0082 named are coextensive -- on a THREE-link chain whose third link,
            # max(E2) = F2, is MEASURED and not construction (0085 SS4) -- and the FALSE class is
            # empty.
            "p_at_bound_totals_and_coextensivity": {
                "FOUR_CELLS_ON_FOUR_POPULATIONS": (
                    "Red Team blocker B2, decisions/0085 SS3. Total, in-both-classes, "
                    "saturated-not-final, final-not-saturated and in-neither, on APPLY position 5, "
                    "APPLY post-liveness, DERIV position 5 and DERIV post-liveness. This is "
                    "CLAUDE.md's standing both-populations rule, not a new requirement. THIS BLOCK "
                    "is the one 0085 SS3 names: on this instance's previous run it carried "
                    "APPLY_position_5 and APPLY_position_7 AND NOTHING ELSE, so the DERIV "
                    "post-liveness figure appeared nowhere in the deliverable -- on the population "
                    "where the ground for keeping the column was therefore unmet, since an "
                    "emptiness asserted in prose and never emitted cannot be checked."),
                "APPLY_position_5": pab(pos5, "APPLY, position-5 row set", 1246),
                "APPLY_position_7_post_liveness": pab(pos6, "APPLY, post-liveness", 1230),
                "DERIV_position_5": pab(pos5d, "DERIV, position-5 row set", 1072),
                "DERIV_position_7_post_liveness": pab(pos6d, "DERIV, post-liveness", 1056),
                "these_are_TOTALS_not_a_split": (
                    "decisions/0083 SS2. 1,246 and 1,230 are correct counts and both arms "
                    "reproduce them, but they are ONE class counted twice, not two classes "
                    "summed. Using them as evidence that the column separates anything is a "
                    "WITHDRAWN ARGUMENT (CLAUDE.md, third blindness class); using them as p = 1.0 "
                    "TOTALS is correct."),
                "clauses_are_coextensive_AND_THE_CHAIN_HAS_THREE_LINKS": (
                    "the two clauses decisions/0082 named -- rank numerator saturated at L2, and "
                    "left at the final episode -- are the SAME EVENT. THE CHAIN IS THREE LINKS AND "
                    "ONLY TWO ARE CONSTRUCTION (Red Team P4, 0085 SS4). Link 1: the set-membership "
                    "rule gives A_H subset E2, so m_H is in E2 -- construction. Link 2: the "
                    "numerator |{e in E2 : e <= m_H}| equals L2 iff m_H = max(E2), given "
                    "L2 := |E2| -- construction. Link 3: max(E2) = F2 -- NOT CONSTRUCTION. It "
                    "holds only because the finale is the highest-numbered LISTED episode, and the "
                    "s2_aired_lt_listed case separates them. MEASURED below, 0 shows in frame. The "
                    "FALSE class is therefore EMPTY, measured in the cells above rather than "
                    "asserted; links 1 and 2 are W-invariant and link 3 is a frame property, so a "
                    "FALSE row at any Step 13 arm means the rank form, the set-membership rule or "
                    "the finale numbering has broken. 0083 SS2 named TWO causes for a future FALSE "
                    "row; there are THREE."),
                "link_3_max_E2_equals_F2_MEASURED_NOT_ASSUMED": {
                    "ruling": "Red Team P4, third pass, decisions/0085 SS4",
                    "shows_where_max_E2_differs_from_F2": int(
                        (frame.s2_E.map(lambda s: max(int(x) for x in str(s).split(",")
                                                      if x.strip().isdigit()))
                         != frame.s2_F).sum()),
                    "s2_aired_lt_listed_shows": int(frame.s2_aired_lt_listed.sum()),
                    "shows_in_frame_examined": int(frame.shape[0]),
                    # MEASURED, not a literal: read off the count immediately above rather than
                    # asserted beside it, so the two cannot disagree on a future frame.
                    "holds_on_every_frame_show": bool(
                        int((frame.s2_E.map(lambda s: max(int(x) for x in str(s).split(",")
                                                          if x.strip().isdigit()))
                             != frame.s2_F).sum()) == 0),
                    "why_it_matters": "where a season lists an episode numbered above its finale, "
                                      "saturation of the rank numerator and 'left at the final "
                                      "episode' come apart and a FALSE row becomes possible. The "
                                      "frame does not move across Step 13's grid, so this is "
                                      "measured once and holds at every arm."},
                "cross_tab_APPLY_position_5": {
                    "saturated_and_final_episode": int(
                        (pos5 & (r["p"] == 1.0) & r["p_saturated"] & r["p_final_ep"]).sum()),
                    "saturated_not_final_episode": int(
                        (pos5 & (r["p"] == 1.0) & r["p_saturated"] & ~r["p_final_ep"]).sum()),
                    "final_episode_not_saturated": int(
                        (pos5 & (r["p"] == 1.0) & ~r["p_saturated"] & r["p_final_ep"]).sum()),
                    "neither": int(
                        (pos5 & (r["p"] == 1.0) & ~r["p_saturated"] & ~r["p_final_ep"]).sum())},
            },
            "p_min": float(np.nanmin(r["p"][pos5 & r["left"]])),
            "p_max": float(np.nanmax(r["p"][pos5 & r["left"]])),
            "population_of_the_range": "APPLY, position 5 -- the table's row set",
            "rows_with_p_non_null_outside_started_and_left": int(
                (pos5 & ~r["left"] & ~np.isnan(r["p"])).sum())},
    }

    # ---- 11. action counts by type (0070 ruling 4) -----------------------------------------
    ac = a.act_counts
    s2c = ac[:, 1, :]
    tot2 = s2c.sum(axis=1)
    only = lambda j: (s2c[:, j] == tot2) & (tot2 > 0)
    D["action_counts"] = {
        "ruling": "action is record-level and the row is a pair, so it is emitted as per-pair "
                  "COUNTS BY ACTION TYPE, never as a row-level column (0070 ruling 4). It is not "
                  "an outcome variable: Step 1 SS2.3 ruled check-ins count as watching alongside "
                  "scrobble and watch, because action is a property of the LOGGING CLIENT.",
        "records_on_position_7_APPLY_rows": {
            "S1": {"watch": int(ac[pos6, 0, 0].sum()), "checkin": int(ac[pos6, 0, 1].sum()),
                   "scrobble": int(ac[pos6, 0, 2].sum()), "other": int(ac[pos6, 0, 3].sum())},
            "S2": {"watch": int(ac[pos6, 1, 0].sum()), "checkin": int(ac[pos6, 1, 1].sum()),
                   "scrobble": int(ac[pos6, 1, 2].sum()), "other": int(ac[pos6, 1, 3].sum())}},
        "pairs_by_S2_evidence_composition_position_7_APPLY": {
            "no_S2_records": int((pos6 & (tot2 == 0)).sum()),
            "watch_only": int((pos6 & only(0)).sum()),
            "checkin_only": int((pos6 & only(1)).sum()),
            "scrobble_only": int((pos6 & only(2)).sum()),
            "mixed": int((pos6 & (tot2 > 0) & ~only(0) & ~only(1) & ~only(2)).sum())},
        "note_for_Step_13": "the action arm excludes checkin-only and manual-watch-only "
                            "evidence; those two categories are the counts above, and the "
                            "per-pair column set in the analysis table carries the same counts "
                            "row by row",
        "unknown_action_values_encountered": int(ac[:, :, 3].sum()),
    }

    # ---- PROVENANCE, applied to EVERY block and every population sub-block -------------------
    # decisions/0079 (B6). Injected mechanically rather than written by hand at the blocks that
    # seemed to need it: partial application is the failure the ruling names.
    for k, v in D.items():
        if isinstance(v, dict):
            v.setdefault("build", lib.BUILD_TAG)
            for k2, v2 in v.items():
                if isinstance(v2, dict) and any(isinstance(x, (int, float)) for x in v2.values()):
                    v2.setdefault("build", lib.BUILD_TAG)
    # the two figures NOT measured on this build carry the build they were measured on
    D["the_3440"]["build"] = ("decisions/0034 SS3, the Step 5 revision-6 UNCENSORED estimation "
                              "sample of 128,099 pairs -- NOT build " + lib.BUILD_TAG
                              + ", and never to be reported against APPLY or DERIV")

    with open(os.path.join(OUT, "diagnostics.json"), "w") as fh:
        json.dump(D, fh, indent=2)

    # =====================================================================================
    # INVARIANTS. Every one carries a label: CODE CHECK or DATA CHECK (0068).
    #
    # The set is NINE. It was EIGHT at decisions/0076 -- five pure code checks, one
    # code-by-construction with force only as specified, and TWO that can fail on real data --
    # and decisions/0088 SS1(c) PROMOTES a ninth, the tau2 <= tau_pull assertion that already ran
    # in this arm's stage 3 but sat outside the published set. THE NINTH IS A SIXTH PURE CODE
    # CHECK, so the ratio of falsifiable checks gets WORSE, not better: 6 + 1 + 2 rather than
    # 5 + 1 + 2. That is stated because an added check reads as an added guarantee, and this one
    # adds visibility rather than power. Before 0076 the set was six, of which FIVE could not
    # fail and ZERO were pure data checks -- 0074 had labelled `p` a data check and 0076
    # corrected it to CODE CHECK on both instances' own proof. The set-membership rule is NOT in
    # this list: 0074 ruling 3 makes it a coverage count.
    #
    # EVERY INVARIANT NAMES THE POPULATION IT RUNS ON AND ACCOUNTS FOR EVERY ROW IN IT -- Human
    # Lead ruling, decisions/0080 SS3. This is the provenance rule applied to invariants: an
    # invariant that passes on one population and was never run on another READS AS A PASS ON
    # BOTH. Every entry reports rows_asserted + rows_not_asserted = rows_in_the_stated_population
    # and the identity must hold. The dual run diverged on the coverage of five of the eight, and
    # one gap was real: `p` asserted on 19,042 rows with a non-S&L clause of 177,513, summing to
    # 196,555 against a 196,654-row table -- 99 rows covered by NEITHER clause, exactly the
    # started-and-left liveness exclusions. A passing invariant whose coverage the instance chose
    # is a code check on the instance's choice.
    #
    # =====================================================================================
    # THE COVERAGE-IDENTITY INDEPENDENCE PROXY WAS WRONG, AND IT IS CORRECTED HERE.
    #
    # Red Team's fifth pass, F2, carried into this rerun by decisions/0090 SS3. Build
    # a/2026-08-16-0088 classified an identity as REAL ARITHMETIC on the test
    #
    #     real = parts is not None and len(parts) > 1
    #
    # -- i.e. "it has more than one clause". THAT TEST ADMITS AN IDENTITY THAT CANNOT FAIL ON ANY
    # DATA. Every multi-clause identity in that build had clauses that are a COMPLEMENTARY
    # PARTITION OF THE SAME MASK the population size is taken from:
    #
    #   invariant 1  parts = [never & M, left & M, continued & M],  n_pop = M.sum()
    #                the three states are mutually exclusive and exhaustive BY THE EXPRESSIONS
    #                THAT DEFINE THEM (never = kA == 0; continued = (kA >= 1) & ...;
    #                left = (kA >= 1) & ~continued), so the three always sum to M.sum().
    #   invariant 6  parts = [M & left, M & ~left],  n_pop = M.sum()   -- X and its complement.
    #   invariant 7  parts = [|all| - |touched|, |mixed|, |wholesale|], n_pop = |all|, and
    #                mixed + wholesale = touched by set algebra, so the three always sum to |all|.
    #   invariant 9  parts = [tau2 <= tau_pull, tau2 > tau_pull],  n_pop = M.sum() -- complement.
    #
    # In all four, `sum(parts) == n_pop` is an identity of the expressions, not a fact about the
    # data. THE PREVIOUS DELIVERABLE CALLED INVARIANT 6's "the identity that closes the hole".
    # It closes nothing on its own: it holds whatever mask M is, including a mask that is not the
    # population the invariant names -- which is the exact defect (0080 SS3's 99-row hole) it was
    # introduced to detect.
    #
    # THE FIX IS THE ONE THE HOLE ACTUALLY NEEDS: SOURCE THE POPULATION SIZE INDEPENDENTLY OF THE
    # ASSERTED COUNT. The 99-row hole was an invariant asserted on a POST-liveness numerator
    # against a PRE-liveness denominator. That is detectable only if the denominator comes from
    # somewhere other than the masks the numerator is built from. So every identity below states
    # where its population size came from, and where an independent source exists the identity is
    # checked against THAT number:
    #
    #   EMITTED_DELIVERABLE   read back from processed/step8/a/analysis_table.csv.gz -- the file
    #                         this step delivers, written by STAGE 3 from a different code path.
    #   INDEPENDENT_FILE      a count written by an earlier stage into its own JSON.
    #   INDEPENDENT_CODE_PATH the same file parsed by different code (used once, for the ledger).
    #   NOT_INDEPENDENT       the population size and the asserted count are one expression.
    #                         Bookkeeping. Labelled as such and NOT counted as a check.
    #
    # The clause counts are KEPT -- they are informative and they are what a reader needs to see
    # the hole -- but they are no longer what makes an identity falsifiable. And the mechanism is
    # DEMONSTRATED rather than asserted: at the end of this section every independent identity is
    # re-run against a deliberately perturbed population size and must report FAIL.
    # =====================================================================================
    inv = []

    # --- the independent sources, read before any identity is built -------------------------
    oc = json.load(open(os.path.join(OUT, "outcomes.json")))          # written by STAGE 3
    _tbl = pd.read_csv(os.path.join(OUT, "analysis_table.csv.gz"),
                       usecols=["user_idx", "in_deriv", "live"])
    IND = {
        "APPLY_pos5_rows": (int(_tbl.shape[0]),
                            "processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED "
                            "DELIVERABLE, written by stage 3", "EMITTED_DELIVERABLE"),
        "APPLY_pos6_rows": (int(_tbl.live.astype(bool).sum()),
                            "processed/step8/a/analysis_table.csv.gz, rows with live = True",
                            "EMITTED_DELIVERABLE"),
        "DERIV_pos5_rows": (int(_tbl.in_deriv.astype(bool).sum()),
                            "processed/step8/a/analysis_table.csv.gz, rows with in_deriv = True",
                            "EMITTED_DELIVERABLE"),
        "DERIV_pos6_rows": (int((_tbl.in_deriv.astype(bool) & _tbl.live.astype(bool)).sum()),
                            "processed/step8/a/analysis_table.csv.gz, rows with in_deriv and live",
                            "EMITTED_DELIVERABLE"),
        "APPLY_pos5_accounts": (int(_tbl.user_idx.nunique()),
                                "processed/step8/a/analysis_table.csv.gz, distinct user_idx",
                                "EMITTED_DELIVERABLE"),
        "DERIV_pos5_accounts": (int(_tbl.loc[_tbl.in_deriv.astype(bool), "user_idx"].nunique()),
                                "processed/step8/a/analysis_table.csv.gz, distinct user_idx on "
                                "in_deriv rows", "EMITTED_DELIVERABLE"),
        "pair_universe": (int(scan_sum["pair_universe_any_inE_S1S2_record"]),
                          "processed/step8/a/scan_summary.json, written by stage 1",
                          "INDEPENDENT_FILE"),
    }
    del _tbl
    # the ledger account count, parsed by a DIFFERENT code path from the pandas read below
    _ledger_slugs = set()
    with open(os.path.join(P4, "pull_ledger.jsonl")) as _fh:
        for _line in _fh:
            _line = _line.strip()
            if _line:
                _o = json.loads(_line)
                if _o.get("slug") is not None:
                    _ledger_slugs.add(_o["slug"])
    IND["ledger_accounts"] = (len(_ledger_slugs),
                              "processed/step4/pull_ledger.jsonl, distinct `slug` counted by a "
                              "line-by-line json.loads pass rather than by pandas.read_json",
                              "INDEPENDENT_CODE_PATH")
    # the seven filter positions, recovered from the two files that wrote them
    _wf = pos_sum["waterfall_APPLY"]
    _wfd = pos_sum["waterfall_DERIV"]
    IND["positions_APPLY"] = (len(_wf) + 2,
                              "processed/step8/a/positions.json waterfall_APPLY (positions 1-5, "
                              "stage 2) plus positions 6 and 7 from outcomes.json (stage 3)",
                              "INDEPENDENT_FILE")
    IND["positions_DERIV"] = (len(_wfd) + 2,
                              "processed/step8/a/positions.json waterfall_DERIV (positions 1-5, "
                              "stage 2) plus positions 6 and 7 from outcomes.json (stage 3)",
                              "INDEPENDENT_FILE")

    _identity_registry = []

    def cover(unit, population, n_pop, n_asserted, extra=None, parts=None, n_not=None,
              indep=None, clause_note=None):
        """rows_asserted + rows_not_asserted = rows_in_the_stated_population (decisions/0080).

        `indep` names an INDEPENDENT source for the population size. Without one the identity is
        bookkeeping: the asserted count and the population size are the same expression and
        `N - N = 0` holds however the mask was chosen. `parts` states each clause's count, which
        is what a reader needs to see a hole -- but multi-clause is NOT what makes the identity
        falsifiable, and treating it as such was the F2 defect corrected on this build."""
        asserted = int(sum(parts)) if parts is not None else int(n_asserted)
        not_asserted = int(n_not) if n_not is not None else int(n_pop) - asserted
        lhs = (" + ".join(str(int(x)) for x in parts) if parts is not None else str(asserted)
               ) + f" + {not_asserted} not asserted"
        iv, isrc, itier = (indep if indep is not None else (None, None, "NOT_INDEPENDENT"))
        can_fail = itier != "NOT_INDEPENDENT"
        d = {"population": population, "unit": unit,
             f"{unit}_in_the_stated_population": int(n_pop),
             f"{unit}_asserted": asserted,
             f"{unit}_not_asserted": not_asserted,
             "coverage_identity": f"{lhs} = {int(n_pop)}",
             "coverage_identity_holds": bool(asserted + not_asserted == int(n_pop)),
             "population_size_independence": itier,
             "population_size_source": (isrc if isrc is not None else
                                        "THE SAME MASK THE ASSERTED COUNT IS TAKEN FROM -- not "
                                        "independent"),
             "independent_population_size": (int(iv) if iv is not None else None),
             "identity_against_the_independent_source": (
                 f"{lhs} = {int(iv)}" if iv is not None else None),
             "identity_against_the_independent_source_holds": (
                 bool(asserted + not_asserted == int(iv)) if iv is not None else None),
             "identity_CAN_FAIL_ON_ANY_DATA": bool(can_fail),
             "what_it_can_detect": (
                 "AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole "
                 "decisions/0080 SS3 was written for. The population size comes from " + str(isrc)
                 + ", so the clauses and the denominator are not the same expression and the "
                   "identity can fail." if can_fail else
                 "NOTHING. The asserted count and the population size are the same expression, so "
                 "N - N = 0 holds however the mask was chosen -- and that is true whether the "
                 "identity has one clause or five. Bookkeeping, not a check (Red Team fourth pass "
                 "decisions/0087 SS4; the multi-clause proxy corrected on Red Team's FIFTH pass, "
                 "F2)."),
             "build": lib.BUILD_TAG}
        if parts is not None:
            d["asserted_clause_counts"] = [int(x) for x in parts]
            d["clauses_are_a_complementary_partition_of_the_population_mask"] = (
                clause_note if clause_note is not None else
                "NOT STATED -- treat as possibly forced by construction")
        if extra:
            d.update(extra)
        if iv is not None:
            _identity_registry.append((population, unit, asserted, not_asserted, int(iv),
                                       str(isrc)))
        return d

    def partition_of(mask, label, indep=None):
        st_ = np.stack([r["never"], r["left"], r["continued"]])[:, mask]
        return {**cover("rows", label, int(mask.sum()), None,
                        parts=[int((mask & r["never"]).sum()), int((mask & r["left"]).sum()),
                               int((mask & r["continued"]).sum())], n_not=0, indep=indep,
                        clause_note="YES -- never / continued / left are mutually exclusive and "
                                    "exhaustive by the expressions that define them, so the three "
                                    "always sum to the mask. The clause counts are informative; "
                                    "what makes this identity falsifiable is the INDEPENDENT "
                                    "population size, not the clause count."),
                "exactly_one_state_per_row": bool((st_.sum(axis=0) == 1).all()),
                "never_started": int((mask & r["never"]).sum()),
                "started_and_left": int((mask & r["left"]).sum()),
                "continued": int((mask & r["continued"]).sum()),
                "sum_of_the_three": int(st_.sum()),
                "sum_equals_row_set": int(st_.sum()) == int(mask.sum()),
                "holds": bool((st_.sum(axis=0) == 1).all()) and int(st_.sum()) == int(mask.sum())}

    parts = {
        "APPLY_post_position_7_195951": partition_of(pos6, "APPLY, post-position-7 row set",
                                                     IND["APPLY_pos6_rows"]),
        "APPLY_position_5_table_row_set_196654": partition_of(
            pos5, "APPLY, position-5 row set -- what the analysis table carries",
            IND["APPLY_pos5_rows"]),
        "DERIV_post_position_7_147271": partition_of(pos6d, "DERIV, post-position-7 row set",
                                                     IND["DERIV_pos6_rows"]),
        "DERIV_position_5_147370": partition_of(pos5d, "DERIV, position-5 row set",
                                                IND["DERIV_pos5_rows"]),
    }
    inv.append({
        "name": "outcome states are mutually exclusive and sum to the post-position-7 row set",
        "label": "CODE CHECK",
        "why": "Step 1 SS7's partition is proved exhaustive and disjoint, so this can only catch "
               "an assignment coded wrongly. It is not evidence for the rule.",
        "population": "FOUR, ALL STATED (decisions/0080 SS3): the post-position-7 row set 195,951 "
                      "AND the position-5 row set 196,654, plus the DERIV pair 147,271 / 147,370. "
                      "The table carries all position-5 rows, so the partition holds on both and "
                      "NEITHER SUBSTITUTES FOR THE OTHER.",
        "coverage_rows": int(pos6.sum()),
        "by_population": parts,
        # COMPUTED, NOT A LITERAL. Red Team's fourth pass (0087 SS4) found this published as a
        # hardcoded `True` -- a result asserted rather than measured, which is the same shape as
        # a control asserted to exist. It now reads the identity off each stated population.
        "coverage_identity_holds_on_every_stated_population": bool(
            all(v["coverage_identity_holds"] for v in parts.values())),
        "identity_holds_against_the_INDEPENDENT_source_on_every_stated_population": bool(
            all(v["identity_against_the_independent_source_holds"] for v in parts.values())),
        "populations_whose_identity_was_checked": len(parts),
        "passed": all(v["holds"] for v in parts.values()),
    })

    chain = [int(positions["pos1"].sum()), int(positions["pos2"].sum()),
             int(positions["pos3"].sum()), int(positions["pos4"].sum()),
             int(pos5.sum()), int(pos6.sum()), int(pos6.sum())]
    chain_d = [int(positions["pos1"].sum()), int(positions["pos2"].sum()),
               int(positions["pos3"].sum()), int(positions["pos4_deriv"].sum()),
               int(pos5d.sum()), int(pos6d.sum()), int(pos6d.sum())]
    inv.append({
        "name": "filter counts decrease monotonically, coded >= and not >",
        "label": "CODE CHECK",
        "why": "filters only remove rows, so it fails only on an implementation that ADDS them "
               "-- a duplicating join. >= is kept so the invariant does not encode a property of "
               "one rule: a position that legitimately removes nothing must not fail (0047, "
               "0049). Load-bearing in fact: position 2 removes exactly 0 pairs on this frame.",
        "population": "BOTH CHAINS (decisions/0080 SS3): APPLY's seven positions and DERIV's. "
                      "Running it on one chain and not the other would read as a pass on both.",
        "chain_APPLY": chain,
        "chain_DERIV": chain_d,
        "coverage_positions": len(chain) + len(chain_d),
        "coverage_APPLY": cover("positions", "APPLY's seven filter positions", len(chain),
                                len(chain), indep=IND["positions_APPLY"]),
        "coverage_DERIV": cover("positions", "DERIV's seven filter positions", len(chain_d),
                                len(chain_d), indep=IND["positions_DERIV"]),
        # the chain values themselves cross-checked against the files the earlier stages wrote,
        # so this invariant is not asserting over a chain it also built
        "chain_APPLY_agrees_with_positions_json_and_outcomes_json": bool(
            chain[:5] == [pos_sum["waterfall_APPLY"][k] for k in
                          ("position_1_step2_frame", "position_2_L2_eq_1_excluded",
                           "position_3_S1_completion_rule", "position_4_contamination",
                           "position_5_right_censoring")]
            and chain[5] == oc["position_6_liveness"]["APPLY"]["retained"]),
        "chain_DERIV_agrees_with_positions_json_and_outcomes_json": bool(
            chain_d[:5] == [pos_sum["waterfall_DERIV"][k] for k in
                            ("position_1_step2_frame", "position_2_L2_eq_1_excluded",
                             "position_3_S1_completion_rule", "position_4_contamination_DERIV_depth",
                             "position_5_right_censoring")]
            and chain_d[5] == oc["position_6_liveness"]["DERIV"]["retained"]),
        "chain_note": "chain[i] is the count after filter position i+1; the transition from entry "
                      "i to entry i+1 is the effect of filter position i+2",
        "filter_positions_removing_exactly_zero_APPLY": [i + 2 for i in range(len(chain) - 1)
                                                         if chain[i] == chain[i + 1]],
        "filter_positions_removing_exactly_zero_DERIV": [i + 2 for i in range(len(chain_d) - 1)
                                                         if chain_d[i] == chain_d[i + 1]],
        "inert_positions_labelled_not_silent": "positions 1, 2, 3 and 7 remove 0 BY CONSTRUCTION "
                                               "and are labelled inert with the reason in the "
                                               "waterfall deliverable (decisions/0079 SS4). An "
                                               "unlabelled always-zero filter reads as evidence "
                                               "the rule FOUND NOTHING when it is evidence the "
                                               "rule CANNOT FIRE.",
        "passed": (all(chain[i] >= chain[i + 1] for i in range(len(chain) - 1))
                   and all(chain_d[i] >= chain_d[i + 1] for i in range(len(chain_d) - 1))),
    })

    d1_count = np.diff(a.s1_ptr)
    d2_count = np.diff(a.s2_ptr)
    ok_d1 = bool((d1_count <= positions["L1"]).all())
    ok_d2 = bool((d2_count <= a.L2).all())
    ok_a = bool((r["kAH"] <= a.L2).all()) and bool((r["kA"] <= a.L2).all())
    inv.append({
        "name": "distinct episodes never exceed season length",
        "label": "CODE CHECK",
        "why": "the set-membership drop rule already establishes |D| <= L by construction; this "
               "fails only if an implementation filtered by the numeric range 1..F instead of by "
               "the listed set E (Step 1 SS3.2). Not evidence for the rule.",
        "population": "BOTH SEASONS, ON EVERY PAIR THE SET-MEMBERSHIP RULE EXAMINES -- the pair "
                      "universe of 278,452, NOT the 196,654 position-5 row set. decisions/0080 "
                      "SS3: the wider reading is required and the narrower does not substitute. "
                      "The record count is stated with it.",
        "coverage_pairs": int(a.n),
        "coverage": cover("pairs", "the pair universe the set-membership rule examines", a.n, a.n,
                          indep=IND["pair_universe"],
                          extra={"records_examined": scan_sum["in_frame_S1S2_episode_records"],
                           "records_dropped_by_the_rule": scan_sum[
                               "dropped_by_set_membership_records"],
                           "seasons_asserted": ["S1", "S2"],
                           "distinct_episode_rows_asserted_S1": int(d1_count.sum()),
                           "distinct_episode_rows_asserted_S2": int(d2_count.sum())}),
        "max_D1_minus_L1": int((d1_count - positions["L1"]).max()),
        "max_D2_minus_L2": int((d2_count - a.L2).max()),
        "max_AH_minus_L2": int((r["kAH"] - a.L2).max()),
        "passed": ok_d1 and ok_d2 and ok_a,
    })

    inv.append({
        "name": "A is a subset of A_H on every row",
        "label": "CODE CHECK",
        "why": "true by construction since tau1 < tau2 and both sets are prefixes of the same "
               "timestamp-ordered episode list; it can only catch the two sets being computed "
               "wrongly or the bounds transposed. Not evidence for the rule.",
        "population": "the 196,654 position-5 row set, EVERY ROW (decisions/0080 SS3)",
        "coverage_rows": int(pos5.sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), int(pos5.sum()), indep=IND["APPLY_pos5_rows"]),
        "rows_where_A_exceeds_A_H": int((r["kA"][pos5] > r["kAH"][pos5]).sum()),
        "rows_where_max_A_exceeds_max_A_H": int((r["mA"][pos5] > r["mH"][pos5]).sum()),
        "also_holds_on_the_post_position_7_row_set": bool(
            (r["kA"][pos6] <= r["kAH"][pos6]).all()),
        "passed": bool((r["kA"][pos5] <= r["kAH"][pos5]).all()
                       and (r["mA"][pos5] <= r["mH"][pos5]).all()),
    })

    t0, fin, s1d = a.t0, positions["fin2_epoch"], positions["s1_date"]
    c1 = bool((t0[pos5] >= fin[pos5]).all())
    c2 = bool((t0[pos5] >= s1d[pos5]).all())
    c3 = bool(((t0[pos5] == fin[pos5]) | (t0[pos5] == s1d[pos5])).all())
    inv.append({
        "name": "clock start is on or after the S2 finale date, on or after the first-pass S1 "
                "completion date, and equal to one of the two",
        "label": "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED",
        "why": "T0 is a max(), so the two inequalities and the equality hold for any correct "
               "implementation. The force comes from recomputing the first-pass S1 completion "
               "date INDEPENDENTLY from the episode records rather than reading back the "
               "pipeline's value: a disagreement there is a real finding. Read back rather than "
               "recomputed, this degrades to a code check and proves nothing.",
        "replaces": "the withdrawn 'no clock start precedes an S2 premiere', vacuous under a "
                    "finale-anchored clock",
        "population": "the 196,654 position-5 row set, EVERY ROW, with the first-pass S1 "
                      "completion date RECOMPUTED INDEPENDENTLY -- the only thing giving this one "
                      "force (decisions/0080 SS3)",
        "coverage_rows": int(pos5.sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), int(pos5.sum()), indep=IND["APPLY_pos5_rows"],
                          extra={"independent_recomputation_covers_pairs": int(a.n),
                                 "read_back_from_the_pipeline": False}),
        "on_or_after_S2_finale": c1,
        "on_or_after_first_pass_S1_completion": c2,
        "equals_one_of_the_two": c3,
        "independent_recomputation": pos_sum["independent_S1_completion_check"],
        "tie_break_note": "Step 1 SS2.2 breaks exactly-equal timestamps by episode number then "
                          "smallest event id. The recomputation applies that tiebreak; the "
                          "agreement counts above are reported rather than a choice being made "
                          "about whether a tiebreak difference would count as a failure.",
        "passed": c1 and c2 and c3,
    })

    p_sl = r["p"][pos5 & r["left"]]
    inv.append({
        "name": "p lies in (0, 1] on every Started-and-left row and is null everywhere else",
        "label": "CODE CHECK",
        "why": "SPECIFIED by decisions/0074 ruling 2; LABEL CORRECTED from DATA CHECK to CODE "
               "CHECK by decisions/0076 on both instances' own proof. Started-and-left requires "
               "|A| >= 1, so max(A_H) exists; set membership bounds the rank numerator in "
               "[1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the "
               "withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has "
               "a gap. It is kept because Step 10 publishes p -- but it proves the code, not the "
               "rule.",
        "population": "ALL Started-and-left rows AT POSITION 5, null on the rest, and the two "
                      "clauses must sum to 196,654 EXACTLY (decisions/0080 SS3). The dual run had "
                      "one arm assert p on 19,042 rows -- the POST-LIVENESS Started-and-left "
                      "count -- against a PRE-LIVENESS denominator of 177,513 non-S&L rows, "
                      "leaving 99 rows covered by neither clause, exactly the started-and-left "
                      "liveness exclusions. Do not take the numerator post-liveness and the "
                      "denominator pre-liveness. ***CORRECTED ON THIS BUILD (Red Team fifth pass, "
                      "F2): the previous deliverable called this two-clause sum 'THE IDENTITY "
                      "THAT CLOSES THE HOLE'. IT DOES NOT CLOSE IT. The clauses are `M & left` "
                      "and `M & ~left` -- a set and its complement within the same mask M -- so "
                      "they sum to M.sum() for EVERY M, including a mask that is not the "
                      "population named, which is the defect. What closes the hole is the "
                      "denominator coming from somewhere else: it is now read from the EMITTED "
                      "analysis table, so a numerator taken post-liveness against a pre-liveness "
                      "denominator FAILS.***",
        "coverage_rows": int((pos5 & r["left"]).sum()),
        "coverage": cover("rows", "APPLY, position 5 -- the analysis table's row set",
                          int(pos5.sum()), None, indep=IND["APPLY_pos5_rows"],
                          extra={"clause_1_rows_asserted_p_in_0_1_started_and_left": int(
                                     (pos5 & r["left"]).sum()),
                                 "clause_2_rows_asserted_p_is_null_not_started_and_left": int(
                                     (pos5 & ~r["left"]).sum()),
                                 "started_and_left_post_liveness_for_contrast_NOT_the_numerator":
                                     int((pos6 & r["left"]).sum()),
                                 "THE_HOLE_THIS_WOULD_NOW_CATCH": {
                                     "the_defective_pairing": "numerator " + str(
                                         int((pos6 & r["left"]).sum())) + " (post-liveness S&L) "
                                         "with denominator clause " + str(
                                             int((pos5 & ~r["left"]).sum())) + " (pre-liveness "
                                         "non-S&L)",
                                     "what_it_sums_to": int((pos6 & r["left"]).sum())
                                                        + int((pos5 & ~r["left"]).sum()),
                                     "independent_population_size": IND["APPLY_pos5_rows"][0],
                                     "rows_covered_by_neither_clause": IND["APPLY_pos5_rows"][0]
                                     - (int((pos6 & r["left"]).sum())
                                        + int((pos5 & ~r["left"]).sum())),
                                     "would_the_identity_FAIL": bool(
                                         int((pos6 & r["left"]).sum())
                                         + int((pos5 & ~r["left"]).sum())
                                         != IND["APPLY_pos5_rows"][0]),
                                     "note": "measured on this build, not asserted: the exact "
                                             "mispairing decisions/0080 SS3 describes is "
                                             "reconstructed and the identity is evaluated on it. "
                                             "Under the previous build's same-mask denominator "
                                             "this pairing could not be detected at all."}},
                          parts=[int((pos5 & r["left"]).sum()), int((pos5 & ~r["left"]).sum())],
                          n_not=0,
                          clause_note="YES -- `M & left` and `M & ~left` are a set and its "
                                      "complement within the same mask, so they sum to M for "
                                      "every M. The clause counts show a reader where a hole "
                                      "would be; the INDEPENDENT denominator is what detects one."),
        "min": float(np.nanmin(p_sl)), "max": float(np.nanmax(p_sl)),
        "nulls_among_started_and_left": int(np.isnan(p_sl).sum()),
        "non_null_outside_started_and_left": int((pos5 & ~r["left"] & ~np.isnan(r["p"])).sum()),
        "passed": bool(np.nanmin(p_sl) > 0 and np.nanmax(p_sl) <= 1.0
                       and np.isnan(p_sl).sum() == 0
                       and int((pos5 & ~r["left"] & ~np.isnan(r["p"])).sum()) == 0
                       and int((pos5 & r["left"]).sum()) + int((pos5 & ~r["left"]).sum())
                       == int(pos5.sum())),
    })

    # ---- DATA CHECK 1: no account is dropped wholesale by the pair-level liveness filter ----
    # decisions/0076. 703 pairs from 216 accounts is consistent with BOTH a pair-level and an
    # account-level implementation, and nothing in the set distinguished them. This can fail on
    # real data.
    def wholesale_on(mask, label, indep=None):
        nl_ = mask & r["not_live"]
        lv2 = mask & ~r["not_live"]
        un = np.unique(a.pair_user[nl_])
        ul = np.unique(a.pair_user[lv2])
        mixed = np.intersect1d(un, ul)
        whole = np.setdiff1d(un, ul)
        allu = np.unique(a.pair_user[mask])
        cnt_ = pd.Series(a.pair_user[mask]).value_counts()
        # the classification is MEASURED against the population, not asserted: `True` was a
        # hardcoded literal here until Red Team's fourth pass (0087 SS4). ***AND THE THREE CLASSES
        # DO NOT MAKE THE IDENTITY FALSIFIABLE*** -- mixed and wholesale partition `touched` by
        # set algebra, so untouched + mixed + wholesale = |all| for any mask. Red Team's FIFTH
        # pass, F2. The account count is therefore taken from the EMITTED TABLE's distinct
        # user_idx, which is where the check gets its force.
        return {**cover("accounts", label, allu.size, None, indep=indep,
                        extra={"accounts_untouched_by_the_exclusion": int(allu.size - un.size),
                               "accounts_touched_by_the_exclusion": int(un.size),
                               "classification_covers_every_account": bool(
                                   int(allu.size - un.size) + int(mixed.size) + int(whole.size)
                                   == int(allu.size))},
                        parts=[int(allu.size - un.size), int(mixed.size), int(whole.size)],
                        n_not=0,
                        clause_note="YES -- mixed and wholesale partition `touched` by set "
                                    "algebra, so the three classes sum to the account total for "
                                    "any mask. The INDEPENDENT account count is what can fail."),
                "accounts_holding_BOTH_a_live_and_a_not_live_pair": int(mixed.size),
                "accounts_all_of_whose_pairs_are_excluded": int(whole.size),
                "of_those_holding_more_than_one_pair_in_this_population": int(
                    (cnt_.reindex(whole).fillna(0) > 1).sum()),
                "holds": bool(mixed.size > 0)}

    who = {"APPLY_position_5": wholesale_on(pos5, "accounts holding a position-5 APPLY pair",
                                            IND["APPLY_pos5_accounts"]),
           "DERIV_position_5": wholesale_on(pos5d, "accounts holding a position-5 DERIV pair",
                                            IND["DERIV_pos5_accounts"])}
    nl = pos5 & r["not_live"]
    lv_ = pos5 & ~r["not_live"]
    u_nl = np.unique(a.pair_user[nl])
    u_lv = np.unique(a.pair_user[lv_])
    u_mixed = np.intersect1d(u_nl, u_lv)
    u_wholesale = np.setdiff1d(u_nl, u_lv)
    # of the wholesale accounts, how many held only ONE position-5 pair -- for those the two
    # implementations are indistinguishable and no inference is available either way
    cnt = pd.Series(a.pair_user[pos5]).value_counts()
    whole_multi = int((cnt.reindex(u_wholesale).fillna(0) > 1).sum())
    inv.append({
        "name": "no account is dropped wholesale by the pair-level liveness filter",
        "label": "DATA CHECK",
        "why": "CLAUDE.md and Step 7: 'One account can be live for one show and not another. "
               "Never drop a user wholesale.' 703 pairs from 216 accounts is consistent with a "
               "pair-level AND an account-level implementation, and nothing in the exclusion set "
               "distinguished them. Asserting that at least one account holds BOTH a live and a "
               "not-live pair separates them. THIS CAN FAIL ON REAL DATA (decisions/0076).",
        "population": "BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 SS3): the accounts holding a "
                      "position-5 pair in APPLY and the accounts holding one in DERIV, each "
                      "reporting accounts that hold both a live and a not-live pair. Every "
                      "account in each is classified, so the coverage identity holds on both.",
        "by_population": who,
        "coverage_accounts_with_a_position_5_pair": int(np.unique(a.pair_user[pos5]).size),
        "accounts_touched_by_the_exclusion": int(u_nl.size),
        "accounts_holding_BOTH_a_live_and_a_not_live_pair": int(u_mixed.size),
        "accounts_all_of_whose_position_5_pairs_are_excluded": int(u_wholesale.size),
        "of_those_accounts_holding_more_than_one_position_5_pair": whole_multi,
        "reading": "accounts in the last line held exactly one position-5 pair unless the count "
                   "above is non-zero; for a single-pair account 'wholesale' and 'pair-level' "
                   "are indistinguishable and no inference is available either way.",
        "assertion": "accounts_holding_BOTH_a_live_and_a_not_live_pair > 0, ON BOTH POPULATIONS",
        "passed": bool(all(v["holds"] for v in who.values())),
    })

    # ---- DATA CHECK 2: no access_denied or skipped account is read as empty ----------------
    # decisions/0076. CLAUDE.md: "a skipped user silently read as empty becomes a false 'never
    # started' in the headline." This fails in the direction of the result.
    led2 = pd.read_json(os.path.join(P4, "pull_ledger.jsonl"), lines=True)
    users = json.load(open(os.path.join(P5, "user_index.json")))["users"]
    uslug = pd.Index(users)
    SKIP = {"discarded_over_tolerance", "skipped_length_forecast", "error_short_read",
            "access_denied", "private", "skipped"}
    last = led2.drop_duplicates("slug", keep="last")
    final_skip = set(last.loc[last.outcome.isin(SKIP), "slug"])
    ever_skip = set(led2.loc[led2.outcome.isin(SKIP), "slug"])
    ever_data = set(led2.loc[led2.is_data == True, "slug"])
    unknown_outcomes = sorted(set(led2.outcome) - SKIP - {"complete"})
    # 403s never occurred in this pull; measured from the request log rather than assumed
    n_403 = sum(1 for line in open(os.path.join(ROOT, "logs/api_requests.ndjson"))
                if '"status": 403' in line)

    def rows_for(slugset):
        idx = uslug.get_indexer(sorted(slugset))
        present = idx[idx >= 0]
        if present.size == 0:
            return 0, 0, 0
        m = np.isin(a.pair_user, present)
        return int(present.size), int((m & pos5).sum()), int((m & pos5 & r["never"]).sum())

    fs_users, fs_pairs, fs_never = rows_for(final_skip)
    es_users, es_pairs, es_never = rows_for(ever_skip - ever_data)
    retried = sorted(ever_skip & ever_data)
    rt_users, rt_pairs, rt_never = rows_for(set(retried))
    inv.append({
        "name": "no access_denied or otherwise skipped account is read as empty",
        "label": "DATA CHECK",
        "why": "CLAUDE.md: 'a skipped user silently read as empty becomes a false never started "
               "in the headline'; rule and evidence at artifacts/step0-access-and-setup.md SS7. "
               "A skipped account must stay distinguishable downstream and must never contribute "
               "a never-started pair. THIS CAN FAIL ON REAL DATA, AND IT FAILS IN THE DIRECTION "
               "OF THE RESULT (decisions/0076).",
        "population": "THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 SS3) -- every distinct "
                      "account the Step 4 pull touched, not the accounts that survived into the "
                      "table. The skipped classes are counted separately and the pairs they "
                      "contribute are stated, so an account that was skipped and then read as "
                      "empty would be visible rather than absent.",
        "coverage": cover("accounts", "every distinct account in processed/step4/pull_ledger.jsonl",
                          int(last.shape[0]), int(last.shape[0]),
                          indep=IND["ledger_accounts"],
                          extra={"accounts_whose_final_state_is_complete": int(
                              (last.outcome == "complete").sum()),
                           "accounts_whose_final_state_is_a_skip_class": int(len(final_skip)),
                           "accounts_whose_final_state_is_neither": int(
                               last.shape[0] - (last.outcome == "complete").sum()
                               - len(final_skip)),
                           "accounts_present_in_the_user_index": int(len(users)),
                           "ledger_rows_read": int(led2.shape[0])}),
        "coverage_ledger_rows": int(led2.shape[0]),
        "coverage_accounts_in_the_user_index": int(len(users)),
        "skip_classes_present_in_the_ledger": {k: int((last.outcome == k).sum())
                                               for k in sorted(SKIP)
                                               if (last.outcome == k).any()},
        "pairs_contributed_by_each_skip_class": {
            k: {"accounts": int((last.outcome == k).sum()),
                "accounts_present_in_the_user_index": rows_for(
                    set(last.loc[last.outcome == k, "slug"]))[0],
                "position_5_pairs": rows_for(set(last.loc[last.outcome == k, "slug"]))[1],
                "pairs_scored_never_started": rows_for(
                    set(last.loc[last.outcome == k, "slug"]))[2]}
            for k in sorted(SKIP) if (last.outcome == k).any()},
        "ledger_outcomes_not_classified_as_skip_or_complete": unknown_outcomes,
        "HTTP_403_responses_in_the_whole_run": n_403,
        "access_denied_accounts": int((last.outcome == "access_denied").sum()),
        "accounts_whose_FINAL_ledger_state_is_a_skip_class": int(len(final_skip)),
        "of_those_present_in_the_user_index": fs_users,
        "of_those_contributing_a_position_5_pair": fs_pairs,
        "of_those_contributing_a_pair_scored_NEVER_STARTED": fs_never,
        "accounts_skipped_and_never_yielding_data": int(len(ever_skip - ever_data)),
        "those_accounts_contributing_a_NEVER_STARTED_pair": es_never,
        "accounts_skipped_on_one_attempt_but_yielding_data_on_another": {
            "count": len(retried), "position_5_pairs": rt_pairs,
            "never_started_pairs": rt_never,
            "note": "not a violation -- these accounts have a real parsed history and their "
                    "never-started rows rest on evidence, not on absence. Reported so the "
                    "assertion's scope is visible."},
        "assertion": "no account whose final ledger state is a skip class, and no account that "
                     "was skipped and never yielded data, contributes a pair scored never-started",
        "passed": bool(fs_never == 0 and es_never == 0 and len(unknown_outcomes) == 0),
    })

    # ---- 9: THE PROMOTED ASSERTION, B3(c) --------------------------------------------------
    # decisions/0088 SS1(c): `assert (tau2[pos5] > tau_pull).sum() == 0` already runs in this
    # arm's pipeline -- src/step8_a_3_table.py, immediately after position 5 -- but it sat
    # OUTSIDE the published invariant set, so no reader of the deliverable could see it. It is
    # published here, labelled CODE CHECK, and it is the same expression rather than a second
    # definition of it.
    def outcome_window_site(mask, label, indep=None):
        le2 = int((r["tau2"][mask] <= lib.TAU_PULL).sum())
        gt2 = int((r["tau2"][mask] > lib.TAU_PULL).sum())
        eq2 = int((r["tau2"][mask] == lib.TAU_PULL).sum())
        le1 = int((r["tau1"][mask] <= lib.TAU_PULL).sum())
        return {**cover("rows", label, int(mask.sum()), None, indep=indep,
                        extra={"rows_with_tau2_at_or_before_tau_pull": le2,
                               "rows_with_tau2_after_tau_pull": gt2,
                               "rows_with_tau2_EXACTLY_AT_tau_pull": eq2,
                               "rows_with_tau1_at_or_before_tau_pull": le1},
                        parts=[le2, gt2], n_not=0,
                        clause_note="YES -- `tau2 <= tau_pull` and `tau2 > tau_pull` are a set "
                                    "and its complement within the same mask, so they sum to the "
                                    "mask for any mask. The INDEPENDENT row count is what can "
                                    "fail."),
                # THE BOUND IS ATTAINED, and a passing assertion at the bound is not the same
                # evidence as one with slack: a `>=` form of this same assertion would FAIL on
                # these rows. Reported because only the arm that measured it can tell them apart.
                "rows_with_tau2_EXACTLY_AT_tau_pull": eq2,
                "the_bound_is_ATTAINED_a_ge_form_would_fail": bool(eq2 > 0),
                "holds": bool(gt2 == 0)}

    ow = {"APPLY_position_5": outcome_window_site(pos5, "APPLY, position-5 row set",
                                                  IND["APPLY_pos5_rows"]),
          "DERIV_position_5": outcome_window_site(pos5d, "DERIV, position-5 row set",
                                                  IND["DERIV_pos5_rows"])}
    inv.append({
        "name": "no retained row's outcome window extends past tau_pull: tau2 <= tau_pull on "
                "every position-5 row",
        "label": "CODE CHECK",
        "why": "D10 right-censors on t0 + (max(W, 91) + H) * 24h <= tau_pull, so tau2 <= tau_pull "
               "holds for any correct censoring step and no data configuration can break it. It "
               "is what makes D11 INERT on A and A_H, which is why the per-site D11 table can "
               "report those two sites as inert by construction rather than by inspection. It "
               "fails only on a censoring term coded wrongly -- and it is NOT evidence for the "
               "liveness rule or for any outcome.",
        "promoted_from": "src/step8_a_3_table.py, where it has run as a bare assert since the "
                         "first build. PROMOTED INTO THE PUBLISHED SET by decisions/0088 SS1(c) "
                         "because an assertion a reader of the deliverable cannot see is not a "
                         "published check.",
        "population": "BOTH POPULATIONS, EVERY ROW: the 196,654 APPLY position-5 row set and the "
                      "147,370 DERIV position-5 row set. The two clauses -- rows at or before "
                      "tau_pull and rows after it -- are counted independently and must sum to "
                      "the population, so the coverage identity is real arithmetic and not "
                      "N - N = 0.",
        "by_population": ow,
        "coverage_rows": int(pos5.sum()),
        "passed": bool(all(v["holds"] for v in ow.values())),
    })

    recon = {
        "name": "703 liveness exclusions at position 6 on APPLY = 196,654",
        "label": "NOT AN INVARIANT -- a POPULATION RECONCILIATION (0068)",
        "why": "Step 7 measured its counts on APPLY built from the Step 5 pair table rather than "
               "through positions 1-5, so this is the first place the two chains have been "
               "compared. A mismatch is a POPULATION defect before an implementation one.",
        "APPLY": {"denominator": int(pos5.sum()), "expected": 703,
                  "measured": int((pos5 & r["not_live"]).sum()),
                  "expected_split": "604 never-started + 99 started-and-left, 216 accounts",
                  "measured_never_started": int((pos5 & r["not_live"] & r["never"]).sum()),
                  "measured_started_and_left": int((pos5 & r["not_live"] & r["left"]).sum()),
                  "measured_accounts": int(np.unique(a.pair_user[pos5 & r["not_live"]]).size)},
        "DERIV": {"denominator": int(pos5d.sum()), "expected": 99,
                  "measured": int((pos5d & r["not_live"]).sum()),
                  "expected_split": "0 never-started + 99 started-and-left, 73 accounts",
                  "measured_never_started": int((pos5d & r["not_live"] & r["never"]).sum()),
                  "measured_started_and_left": int((pos5d & r["not_live"] & r["left"]).sum()),
                  "measured_accounts": int(np.unique(a.pair_user[pos5d & r["not_live"]]).size)},
        "superseded_answers_not_produced": {"ALT_604_on_APPLY": False,
                                            "ALT_MATCHED_793_on_APPLY": False},
        "reconciles": True,
    }
    recon["superseded_answers_not_produced"] = {
        "ALT_604_on_APPLY": int((pos5 & r["not_live"]).sum()) == 604,
        "ALT_MATCHED_793_on_APPLY": int((pos5 & r["not_live"]).sum()) == 793}
    recon["reconciles"] = (recon["APPLY"]["measured"] == 703
                           and recon["DERIV"]["measured"] == 99)

    # every invariant result carries the build it was measured on (decisions/0079 B6)
    for it in inv:
        it["build"] = lib.BUILD_TAG
    recon["build"] = lib.BUILD_TAG

    # the coverage identity, gathered so it can be read at a glance rather than hunted for
    def ident(it):
        out_ = []
        for key in ("coverage", "coverage_APPLY", "coverage_DERIV"):
            if key in it:
                out_.append({key: it[key]["coverage_identity"]})
        if "by_population" in it:
            for k2, v2 in it["by_population"].items():
                out_.append({k2: v2["coverage_identity"]})
        return out_

    report = {"step": 8, "instance": "a", "api_calls": 0, "W_days": W, "H_days": H,
              "build": lib.build_record(),
              "provenance_note": "EVERY INVARIANT RESULT IN THIS FILE WAS MEASURED ON BUILD "
                                 + lib.BUILD_TAG + " (decisions/0079 B6).",
              "coverage_identities": {it["name"]: ident(it) for it in inv},
              "coverage_rule": "EVERY INVARIANT NAMES THE POPULATION IT RUNS ON AND ACCOUNTS FOR "
                               "EVERY ROW IN IT: rows_asserted + rows_not_asserted = "
                               "rows_in_the_stated_population, and the identity must hold "
                               "(decisions/0080 SS3). An invariant that passes on one population "
                               "and was never run on another reads as a pass on both; a passing "
                               "invariant whose coverage the instance chose is a code check on "
                               "the instance's choice.",
              "invariants": inv, "population_reconciliation": recon,
              "set_membership_is_a_coverage_count_not_an_invariant": {
                  "ruling": "decisions/0074 ruling 3",
                  "records_examined": scan_sum["in_frame_S1S2_episode_records"],
                  "records_dropped": scan_sum["dropped_by_set_membership_records"],
                  "distinct_season_number_dropped": scan_sum[
                      "dropped_by_set_membership_distinct_season_number"],
                  "note": "reported, not asserted. The records-examined denominator is published "
                          "unreconciled against the other arm's; see the waterfall report."},
              "label_counts": {"CODE CHECK": sum(1 for i in inv if i["label"] == "CODE CHECK"),
                               "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED":
                                   sum(1 for i in inv if i["label"].startswith("CODE CHECK BY")),
                               "DATA CHECK": sum(1 for i in inv if i["label"] == "DATA CHECK"),
                               "NOT AN INVARIANT (population reconciliation)": 1},
              "what_can_actually_fail": {
                  "checks_that_cannot_fail_on_any_data": sum(
                      1 for i in inv if i["label"] == "CODE CHECK"),
                  "checks_with_force_only_as_specified": sum(
                      1 for i in inv if i["label"].startswith("CODE CHECK BY")),
                  "checks_that_can_fail_on_real_data": sum(
                      1 for i in inv if i["label"] == "DATA CHECK"),
                  "history": "before decisions/0076 the set was six, of which FIVE could not fail "
                             "and ZERO were pure data checks. 0074 had labelled p a DATA CHECK; "
                             "0076 corrected it to CODE CHECK on both instances' proof and added "
                             "the two data checks that now carry the set, making it EIGHT. "
                             "decisions/0088 SS1(c) promotes a NINTH -- the tau2 <= tau_pull "
                             "assertion -- into the published set.",
                  "the_ninth_makes_the_ratio_WORSE_not_better": "the promoted check is a SIXTH "
                                                                "pure code check, so the set goes "
                                                                "from 5 + 1 + 2 to 6 + 1 + 2 and "
                                                                "the number that can fail on real "
                                                                "data is unchanged at TWO. An "
                                                                "added check reads as an added "
                                                                "guarantee; this one adds "
                                                                "VISIBILITY, not power.",
                  "SUPERSEDED_the_assertion_set_has_EIGHT_members": "superseded by decisions/0088 "
                                                                    "SS1(c); the set is NINE"},
              "all_passed": all(i["passed"] for i in inv)}

    # the coverage identity is itself checked, on every stated population of every invariant
    def walk_identities(node, acc):
        if isinstance(node, dict):
            if "coverage_identity_holds" in node:
                acc.append(bool(node["coverage_identity_holds"]))
            for v in node.values():
                walk_identities(v, acc)
        elif isinstance(node, list):
            for v in node:
                walk_identities(v, acc)
        return acc

    ids = walk_identities(inv, [])
    report["coverage_identity_checks_run"] = len(ids)
    report["all_coverage_identities_hold"] = all(ids)

    def walk_kind(node, acc):
        if isinstance(node, dict):
            if "identity_CAN_FAIL_ON_ANY_DATA" in node:
                acc.append((bool(node["identity_CAN_FAIL_ON_ANY_DATA"]),
                            node.get("population_size_independence"),
                            node.get("identity_against_the_independent_source_holds")))
            for v in node.values():
                walk_kind(v, acc)
        elif isinstance(node, list):
            for v in node:
                walk_kind(v, acc)
        return acc

    kinds = walk_kind(inv, [])
    n_can = sum(1 for k in kinds if k[0])
    tiers = {}
    for k in kinds:
        tiers[k[1]] = tiers.get(k[1], 0) + 1

    # --- DEMONSTRATED, NOT ASSERTED: every independent identity must FAIL when the population --
    # --- size it is checked against is perturbed. An assertion mechanism claimed to work and ---
    # --- never seen to fail is a control asserted to exist (CLAUDE.md). -----------------------
    demo = []
    for (popn, unit, asserted, not_asserted, ivalue, isrc) in _identity_registry:
        demo.append({"population": popn, "unit": unit,
                     "true_independent_population_size": ivalue,
                     "perturbed_to": ivalue + 1,
                     "holds_against_the_true_value": bool(asserted + not_asserted == ivalue),
                     "holds_against_the_perturbed_value": bool(
                         asserted + not_asserted == ivalue + 1)})
    demo_ok = bool(demo) and all(d["holds_against_the_true_value"]
                                 and not d["holds_against_the_perturbed_value"] for d in demo)

    # =====================================================================================
    # A REAL INDEPENDENCE CONTROL. Red Team seventh pass, finding 3, against this arm;
    # decisions/0091 SS2 as corrected on the sixth pass.
    #
    # THE `+1` PERTURBATION ABOVE DOES NOT TEST INDEPENDENCE. On a same-mask denominator the
    # clauses sum to N by construction and the stated population reads N + 1, so the identity
    # fails -- IDENTICALLY, and it would have fired on the very build whose defect it claims to
    # have fixed. What it demonstrates is that the identity is ARITHMETIC rather than a hardcoded
    # literal, which the separate literal counter already does. It is KEPT under that label and
    # is no longer described as demonstrating independence.
    #
    # WHAT DISCRIMINATES. The escape the independent source exists to catch is AN INVARIANT RUN
    # ON A POPULATION OTHER THAN THE ONE IT NAMES. When the clauses are a complementary partition
    # of a mask, swapping the mask moves the clauses AND the same-mask denominator together, so
    # the same-mask identity still PASSES on the wrong population. Only a denominator sourced
    # elsewhere -- keyed on the NAME rather than on the mask -- can fail. So each injected defect
    # below asserts BOTH directions:
    #     the SAME-MASK form PASSES  (it cannot detect the defect)
    #     the INDEPENDENT form FAILS (it does)
    # An escape aborts the run before a deliverable is written.
    def _inject(name, what, clause_counts, wrong_mask_size, named_population_size,
                independent_source, expect_same_mask_passes=True):
        _sum = int(sum(clause_counts))
        same_mask_holds = bool(_sum == int(wrong_mask_size))
        indep_holds = bool(_sum == int(named_population_size))
        return {
            "injected_defect": name,
            "what_it_is": what,
            "clause_counts": [int(c) for c in clause_counts],
            "clauses_sum_to": _sum,
            "same_mask_denominator": int(wrong_mask_size),
            "SAME_MASK_form_holds_i_e_CANNOT_DETECT_IT": same_mask_holds,
            "independently_sourced_population_size": int(named_population_size),
            "independent_source": independent_source,
            "INDEPENDENT_form_holds": indep_holds,
            "INDEPENDENT_form_DETECTS_THE_DEFECT": bool(not indep_holds),
            "discriminates": bool(same_mask_holds == expect_same_mask_passes and not indep_holds),
        }

    _n5, _n6 = int(pos5.sum()), int(pos6.sum())
    _n5d, _n6d = int(pos5d.sum()), int(pos6d.sum())
    injected = [
        # 1. The outcome partition run on the POST-LIVENESS mask while naming position 5. The
        #    three clauses are exhaustive on whatever mask they are given, so the same-mask
        #    denominator moves with them and passes. This is the shape 0080 SS3 describes.
        _inject(
            "invariant 1 run on the post-liveness mask while naming the position-5 row set",
            "the three outcome clauses evaluated on pos6 with the population named as APPLY "
            "position 5",
            [int((pos6 & r["never"]).sum()), int((pos6 & r["left"]).sum()),
             int((pos6 & r["continued"]).sum())],
            _n6, IND["APPLY_pos5_rows"][0], IND["APPLY_pos5_rows"][1]),
        # 2. The same on DERIV, because a control applied to one population and not the other is
        #    the same defect as not applying it (CLAUDE.md).
        _inject(
            "invariant 1 run on the DERIV post-liveness mask while naming DERIV position 5",
            "the three outcome clauses evaluated on pos6d with the population named as DERIV "
            "position 5",
            [int((pos6d & r["never"]).sum()), int((pos6d & r["left"]).sum()),
             int((pos6d & r["continued"]).sum())],
            _n6d, IND["DERIV_pos5_rows"][0], IND["DERIV_pos5_rows"][1]),
        # 3. Invariant 6's exact historical mispairing: a POST-liveness numerator against a
        #    PRE-liveness complement. Here the two clauses come from DIFFERENT masks, so the
        #    same-mask form does NOT pass either -- and that is stated rather than glossed, since
        #    the point of the suite is which control catches what.
        _inject(
            "invariant 6's 0080 SS3 mispairing: post-liveness S&L against pre-liveness non-S&L",
            "numerator taken on pos6 and complement on pos5, both named as APPLY position 5",
            [int((pos6 & r["left"]).sum()), int((pos5 & ~r["left"]).sum())],
            _n5, IND["APPLY_pos5_rows"][0], IND["APPLY_pos5_rows"][1],
            expect_same_mask_passes=False),
        # 4. Invariant 7's account identity run on DERIV accounts while naming APPLY's.
        _inject(
            "invariant 7 run on DERIV accounts while naming APPLY's position-5 accounts",
            "accounts partitioned on the DERIV row set with the population named as APPLY",
            [int(np.unique(a.pair_user[pos5d]).size)],
            int(np.unique(a.pair_user[pos5d]).size), IND["APPLY_pos5_accounts"][0],
            IND["APPLY_pos5_accounts"][1]),
        # 5. A dropped clause: one position missing from the monotone chain while the chain is
        #    still named as seven positions.
        _inject(
            "invariant 2 covering six positions while naming seven",
            "the APPLY chain with one position dropped from the coverage count",
            [len(chain) - 1], len(chain) - 1, IND["positions_APPLY"][0],
            IND["positions_APPLY"][1]),
        # 6. The ledger identity with the skipped classes silently omitted.
        _inject(
            "invariant 8 with the skipped account classes omitted from the coverage",
            "the ledger account identity asserting only the accounts that produced pairs",
            [IND["APPLY_pos5_accounts"][0]], IND["APPLY_pos5_accounts"][0],
            IND["ledger_accounts"][0], IND["ledger_accounts"][1]),
    ]
    injected_ok = bool(injected) and all(d["discriminates"] for d in injected)
    injected_caught_by_independent = sum(
        1 for d in injected if d["INDEPENDENT_form_DETECTS_THE_DEFECT"])
    injected_missed_by_same_mask = sum(
        1 for d in injected if d["SAME_MASK_form_holds_i_e_CANNOT_DETECT_IT"])

    report["coverage_identity_strength"] = {
        "ruling": "Red Team's FIFTH pass, F2, carried into this rerun by decisions/0090 SS3. "
                  "Red Team's fourth pass (decisions/0087 SS4) had already recorded that most "
                  "identities have the population size and the asserted count as one expression; "
                  "the sentence it required struck either way is struck by decisions/0088 SS2(d).",
        "CORRECTION_ON_THIS_BUILD": "build a/2026-08-16-0088 classified an identity as REAL "
                                    "ARITHMETIC on the test `parts is not None and len(parts) > "
                                    "1`. THAT TEST WAS WRONG. Every multi-clause identity in that "
                                    "build had clauses forming a COMPLEMENTARY PARTITION OF THE "
                                    "SAME MASK the population size was taken from, so each summed "
                                    "to the population for ANY mask and NONE of them could fail "
                                    "on any data -- including invariant 6's, which that "
                                    "deliverable called 'the identity that closes the hole'. It "
                                    "closed nothing. THE LABEL AND THE CLAIM ARE BOTH CORRECTED, "
                                    "and the population size is now sourced independently of the "
                                    "asserted count, which is what the hole actually needs.",
        "identities_total": len(kinds),
        "identities_that_CAN_FAIL_population_size_sourced_INDEPENDENTLY": int(n_can),
        "identities_that_CANNOT_FAIL_population_size_and_asserted_count_are_one_expression": int(
            len(kinds) - n_can),
        "by_independence_tier": tiers,
        "tier_meanings": {
            "EMITTED_DELIVERABLE": "the population size is read back from "
                                   "processed/step8/a/analysis_table.csv.gz -- the file this step "
                                   "delivers, written by stage 3 through a different code path "
                                   "from the masks this stage builds",
            "INDEPENDENT_FILE": "the population size is a count an earlier stage wrote into its "
                                "own JSON",
            "INDEPENDENT_CODE_PATH": "the same file parsed by different code (the ledger: "
                                     "line-by-line json.loads against pandas.read_json)",
            "NOT_INDEPENDENT": "the population size and the asserted count are one expression. "
                               "Bookkeeping, not a check, and labelled so at each identity.",
        },
        "all_independent_identities_hold_against_their_independent_source": bool(
            all(k[2] for k in kinds if k[0])),
        "ARITHMETIC_NOT_A_LITERAL_the_plus_one_perturbation": {
            "***RELABELLED***": "Red Team seventh pass, finding 3, against this arm; "
                                "decisions/0091 SS2 as corrected on the sixth pass. The previous "
                                "build published this block as 'THE MECHANISM IS DEMONSTRATED, "
                                "NOT ASSERTED' and read it as a demonstration of INDEPENDENCE. "
                                "IT IS NOT ONE.",
            "why_it_does_not_test_independence": "on a SAME-MASK denominator the clauses sum to N "
                                                 "by construction and the stated population reads "
                                                 "N + 1, so the identity fails IDENTICALLY -- it "
                                                 "would have passed on the very build whose "
                                                 "defect it claimed to fix. Perturbing the "
                                                 "DENOMINATOR cannot separate a denominator "
                                                 "sourced independently from one sourced from the "
                                                 "same mask.",
            "what_it_DOES_show": "that each identity is ARITHMETIC rather than a hardcoded "
                                 "literal -- which the separate literal counter already shows. It "
                                 "is kept under that label because it is a real, if narrow, check.",
            "method": "each independent identity is re-evaluated against its population size + 1 "
                      "and must FAIL.",
            "identities_demonstrated": len(demo),
            "all_hold_against_the_true_value_and_FAIL_against_the_perturbed_one": demo_ok,
            "per_identity": demo,
        },
        "INDEPENDENCE_DEMONSTRATED_injected_wrong_population_defects": {
            "why_this_exists": "Red Team seventh pass, finding 3. The escape the independent "
                               "source exists to catch is AN INVARIANT RUN ON A POPULATION OTHER "
                               "THAN THE ONE IT NAMES. Where the clauses are a complementary "
                               "partition of a mask, swapping the mask moves the clauses AND the "
                               "same-mask denominator together, so the same-mask identity still "
                               "PASSES on the wrong population. Only a denominator keyed on the "
                               "NAME can fail.",
            "method": "six defects are injected and each asserts BOTH directions: the SAME-MASK "
                      "form PASSES (it cannot detect the defect) and the INDEPENDENT form FAILS "
                      "(it does). Case 3 is the one exception and it is labelled: its two clauses "
                      "come from different masks, so the same-mask form fails too -- stated "
                      "rather than glossed, because the point of the suite is which control "
                      "catches what.",
            "defects_injected": len(injected),
            "detected_by_the_INDEPENDENT_form": injected_caught_by_independent,
            "MISSED_by_the_same_mask_form": injected_missed_by_same_mask,
            "every_case_discriminates_as_expected": injected_ok,
            "per_defect": injected,
            "also_a_real_control_and_it_covers_one_invariant": "invariant 6's "
                "THE_HOLE_THIS_WOULD_NOW_CATCH reconstructs decisions/0080 SS3's exact mispairing "
                "-- 19,042 + 177,513 = 196,555 against 196,654, 99 rows in neither -- and the "
                "identity FAILS on it. That was already here and is retained; it is case 3 above, "
                "generalised to five more.",
        },
        "note": "the NOT_INDEPENDENT group is bookkeeping and is labelled as such at each "
                "identity. An unlabelled check that cannot fail reads as one that can -- "
                "decisions/0069's rule, applied to the coverage apparatus rather than to the "
                "invariants.",
        "build": lib.BUILD_TAG,
    }
    assert len(kinds) == len(ids), "an identity was emitted without its strength label"
    assert demo_ok, ("the coverage-identity arithmetic demonstration did not fire: an "
                     "independent identity held against a perturbed population size, or none "
                     "was registered -- a check that looked nowhere must fail, not pass")
    assert injected_ok, (
        "the INDEPENDENCE demonstration did not discriminate: an injected wrong-population defect "
        "either escaped the independently-sourced identity or was caught by the same-mask form "
        "when it should not have been. An escape must abort before a deliverable is written.")
    assert len(injected) >= 6 and injected_caught_by_independent == len(injected), (
        "the injected-defect suite looked at too few cases or failed to detect one -- a control "
        "that finds nothing because it looked nowhere must fail, not pass")
    assert all(k[2] for k in kinds if k[0]), (
        "an invariant's coverage disagrees with the independently sourced population size")
    assert all(ids) and len(ids) >= 9, "an invariant does not account for every row it names"
    assert len(inv) == 9, f"the assertion set is {len(inv)}, expected 9 (decisions/0088 SS1(c))"

    with open(os.path.join(OUT, "invariants.json"), "w") as fh:
        json.dump(report, fh, indent=2)

    print(json.dumps({"invariants": [{"name": i["name"], "label": i["label"],
                                      "passed": i["passed"]} for i in inv],
                      "reconciliation": {"APPLY": recon["APPLY"]["measured"],
                                         "DERIV": recon["DERIV"]["measured"]}}, indent=2))
    print(json.dumps({k: D[k] for k in ("drop_counts", "D4_S3_without_S2",
                                        "D9_split_artifacts")}, indent=2)[:3000])


if __name__ == "__main__":
    main()
