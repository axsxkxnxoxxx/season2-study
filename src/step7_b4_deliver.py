"""Step 7 rerun (instance b4) -- stage 6: the deliverable JSON.

READ ONLY. ZERO network calls. Counts and aggregates only.

Also runs the derive/apply check 0038 Sec 2.1 demands but that 0040 did not
close: the reference population is waterfall line 4 (152,126) less D10, while
Step 8 applies liveness at position 6 to the ANALYSIS population (201,900) less
D10. Those two are not identical, so the realised rate on the population the
rule will actually be applied to is measured and reported.

Out: artifacts/step7-liveness-b4.json
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P5 = ROOT / "processed" / "step5"
OUT = ROOT / "processed" / "step7" / "b4"
ART = ROOT / "artifacts"

W = 108
H = 91
ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
DAY = 86400.0
TAU_PULL = int(np.datetime64("2026-08-11T00:00:00", "s").astype(np.int64))
BACKFILL_D, POSTDATE_D = 180.0, -30.0


def apply_to_analysis_population(threshold: float) -> dict:
    """Realised rate on the 201,900 analysis population less D10 -- Step 8's real target."""
    p = pd.read_csv(P5 / "pair_revision5.csv")
    has_s2 = (p.s2_ev_n > 0).values
    t0c = p.t0_contaminated.values.astype(bool)
    all_air = has_s2 & (p.s2_ev_airdate.values == p.s2_ev_n.values)
    keep = ~(all_air | (t0c & ~has_s2))
    q = p[keep]
    assert len(q) == 201_900

    inst = np.load(OUT / "instants.npz")
    tau_all, offsets = inst["tau"], inst["offsets"]
    uidx = q.user_idx.values.astype(np.int64)
    t0_mid = pd.to_datetime(q.t0).values.astype("datetime64[s]").astype(np.int64)
    tau1 = t0_mid.astype(np.float64) + W * DAY
    d10 = t0_mid + (max(W, 91) + H) * 86400 <= TAU_PULL

    n = len(q)
    gap = np.full(n, np.nan)
    state = np.zeros(n, dtype=np.int8)
    order = np.argsort(uidx, kind="stable")
    i = 0
    while i < n:
        j = i
        u = uidx[order[i]]
        while j < n and uidx[order[j]] == u:
            j += 1
        sl = order[i:j]
        seq = tau_all[offsets[u]:offsets[u + 1]]
        pos = np.searchsorted(seq, tau1[sl], side="right")
        nb, na = pos == 0, pos == len(seq)
        ok = ~(nb | na)
        g = np.full(len(sl), np.nan)
        if ok.any():
            pk = pos[ok]
            g[ok] = (seq[pk] - seq[pk - 1]) / DAY
        gap[sl] = g
        st = np.zeros(len(sl), dtype=np.int8)
        st[na] = 1
        st[nb] = 2
        state[sl] = st
        i = j

    m, o, b = (state == 0) & d10, (state == 1) & d10, (state == 2) & d10
    npop = int(d10.sum())
    eg = int((gap[m] >= threshold).sum())
    return {
        "population": "analysis population 201,900 less D10 -- what Step 8 position 6 receives",
        "n_before_D10": int(n),
        "n_after_D10": npop,
        "measured_gap": int(m.sum()),
        "open_ended": int(o.sum()),
        "no_instant_at_or_before_tau1_LIVE": int(b.sum()),
        "not_live_measured_gap": eg,
        "not_live_open_ended": int(o.sum()),
        "not_live_total": eg + int(o.sum()),
        "realised_rate_vs_extended_set": (eg + int(o.sum())) / (int(m.sum()) + int(o.sum())),
        "realised_rate_vs_all_pairs": (eg + int(o.sum())) / npop,
        "stated_rate": 0.01,
    }


def main() -> None:
    t = time.time()
    thr_j = json.load(open(OUT / "threshold.json"))
    pop_j = json.load(open(OUT / "population_meta.json"))
    inst_j = json.load(open(OUT / "instants_meta.json"))
    a = thr_j["arms"][str(W)]
    V = a["reference_set_variants"]
    THR = V["V1_extended_PRIMARY"]["threshold_days_ceiling"]
    boot = json.load(open(OUT / f"bootstrap_W{W}.json"))
    ci = boot["account_clustered"]["ci95_on_ceilinged_threshold_days"]

    arms = {}
    for w in ARMS:
        aw = thr_j["arms"][str(w)]
        vw = aw["reference_set_variants"]["V1_extended_PRIMARY"]
        bw = json.load(open(OUT / f"bootstrap_W{w}.json"))["account_clustered"]
        arms[str(w)] = {
            "W": w,
            "censoring_bound_days_max_W_91_plus_H": max(w, 91) + H,
            "population_post_D10": aw["population_post_D10"],
            "removed_by_D10": 152_126 - aw["population_post_D10"],
            "measured_gap_pairs": aw["counts"]["measured_gap"],
            "open_ended_pairs": aw["counts"]["open_ended"],
            "no_pre_instant_pairs_LIVE": aw["counts"]["no_instant_at_or_before_tau1_LIVE"],
            "raw_p99_days": vw["raw_p99_days"],
            "threshold_days": vw["threshold_days_ceiling"],
            "ci95_account_clustered": bw["ci95_on_ceilinged_threshold_days"],
            "bootstrap_replicates": bw["replicates"],
            "bootstrap_replicates_with_infinite_p99_share": bw["share_infinite"],
            "not_live_total": vw["not_live_total"],
            "not_live_measured_gap": vw["not_live_measured_gap"],
            "not_live_open_ended": vw["not_live_open_ended"],
            "realised_rate_vs_extended_set": vw["realised_rate_vs_extended_set"],
            "realised_rate_vs_measured_gap_pairs": vw["realised_rate_vs_measured_gap_pairs"],
            "realised_rate_vs_all_post_D10_pairs": vw["realised_rate_vs_all_post_D10_pairs"],
            "live_pairs": vw["live_pairs"],
            "live_share": vw["live_share"],
            "gap_test_share_of_exclusions": aw["percentile_sweep_primary_variant"]["99.0"][
                "gap_test_share_of_exclusions"],
        }

    mismatch = apply_to_analysis_population(THR)

    # how concentrated is the exclusion set? -- the reason the interval must be clustered
    zb = np.load(OUT / "bracket.npz")
    g, st, d10 = zb["gap_days_W108"], zb["state_W108"], zb["d10_W108"]
    u = zb["user_idx"]
    mm, oo = (st == 0) & d10, (st == 1) & d10
    excl_gap_mask = mm & (np.nan_to_num(g, nan=-1.0) >= THR)
    conc = {
        "accounts_in_the_post_D10_population": int(len(np.unique(u[d10]))),
        "accounts_supplying_the_gap_test_exclusions": int(len(np.unique(u[excl_gap_mask]))),
        "accounts_supplying_the_open_ended_exclusions": int(len(np.unique(u[oo]))),
        "pairs_at_exactly_the_threshold": int((g[mm] == THR).sum()),
        "pairs_spared_by_the_ceiling_rounding": int(
            ((g[mm] >= V["V1_extended_PRIMARY"]["raw_p99_days"]) & (g[mm] < THR)).sum()),
        "comment": "the whole exclusion set comes from 209 accounts of the 2,402 in the "
                   "post-D10 population (2,100 of which hold an extended-set gap), which is "
                   "why an i.i.d. interval is not admissible here",
    }

    out = {
        "instance": "data-scientist-b, namespace b4",
        "step": 7,
        "status": "PROPOSED, NOT ADOPTED. This is a gate; only the Human Lead approves.",
        "date": "2026-08-13",
        "api_calls": 0,
        "spec": [
            "decisions/0040 (gate reopened; 0036 Sec 2.3(ii) withdrawn; derive after D10)",
            "decisions/0038 (frozen spec; reference line 4; one gap per pair; quota; inertness)",
            "decisions/0037 (bracketing reference; distinct-instant gap unit)",
            "decisions/0036 Sec 2 (rule shape: the gap bracketing tau1)",
            "decisions/0029 (continuous instant differences; filter order 5 then 6)",
            "decisions/0026 (W = 108), decisions/0025 (ceiling), decisions/0021 (insertion time)",
            "decisions/0011 (tau_pull), artifacts/step1-outcome-definition.md Sec 6 and D10",
        ],

        "waterfall_assertion": {
            "expected": pop_j["waterfall_expected"],
            "measured": pop_j["waterfall_measured"],
            "asserted": pop_j["waterfall_asserted"],
            "reference_line": "line 4 -- 152,126 (0038 Sec 2)",
        },
        "D10_right_censoring": {
            "rule": "retain iff [T0] + (max(W,91) + H) x 24h <= tau_pull",
            "H": H,
            "tau_pull": "2026-08-11T00:00:00Z",
            "bound_days_at_W_108": max(W, 91) + H,
            "n_before": 152_126,
            "POST_CENSORING_COUNT": a["population_post_D10"],
            "removed": 152_126 - a["population_post_D10"],
            "removed_share": (152_126 - a["population_post_D10"]) / 152_126,
            "removed_by_class": {
                "measured_gap": 129_630 - a["counts"]["measured_gap"],
                "open_ended": 4_246 - a["counts"]["open_ended"],
                "no_pre_instant": 18_250 - a["counts"]["no_instant_at_or_before_tau1_LIVE"],
            },
            "pre_D10_classes_reproduce_the_frozen_run": {
                "measured_gap": 129_630, "open_ended": 4_246, "no_pre_instant": 18_250,
            },
        },

        "population_by_class_post_D10_at_W_108": {
            "total": a["population_post_D10"],
            "measured_bracketing_gap": a["counts"]["measured_gap"],
            "open_ended_no_instant_after_tau1": a["counts"]["open_ended"],
            "no_instant_at_or_before_tau1_LIVE_per_0021": a["counts"][
                "no_instant_at_or_before_tau1_LIVE"],
            "extended_set_the_reference": a["counts"]["measured_gap"] + a["counts"]["open_ended"],
        },

        "gap_unit": {
            "operation": "0037 Sec 4, verbatim: every record's insertion instant, sorted, runs of "
                         "EXACTLY equal instants collapsed, consecutive differences",
            "records_in_sweep": inst_j["records_in_sweep"],
            "distinct_insertion_instants": inst_j["distinct_insertion_instants"],
            "records_collapsed_by_exact_tie": inst_j["records_collapsed_by_exact_tie"],
            "accounts": inst_j["accounts"],
            "accounts_with_zero_instants": inst_j["accounts_with_zero_instants"],
            "min_gaps_per_account": inst_j["gaps_per_account"]["min"],
            "median_gaps_per_account": inst_j["gaps_per_account"]["median"],
            "calibration": inst_j["calibration"],
        },

        "reference_distribution_bracketing_gap_post_D10": a["bracketing_gap_distribution_extended"],
        "reference_distribution_measured_only": a["bracketing_gap_distribution_measured"],
        "pooled_gap_distribution_NOT_THE_REFERENCE": thr_j["pooled_gap_distribution_all_accounts"],
        "length_bias": a["length_bias"],
        "tie_structure": a["tie_structure_measured_gaps"],
        "exclusion_concentration": conc,

        "PROPOSED_THRESHOLD": {
            "percentile": 99.0,
            "reference": "the extended bracketing-gap set (measured gaps + open-ended as +inf), "
                         "one gap per pair, on the post-D10 population",
            "raw_days": V["V1_extended_PRIMARY"]["raw_p99_days"],
            "threshold_days_ceiling_per_0025": THR,
            "account_clustered_ci95_days": ci,
            "bootstrap_replicates": boot["account_clustered"]["replicates"],
            "bootstrap_endpoint_convention": boot["account_clustered"]["endpoint_convention"],
            "bootstrap_seed": boot["seed"],
            "bootstrap_accounts_resampled": boot["accounts"],
            "iid_pair_level_ci95_FOR_CONTRAST": boot[
                "iid_pair_level_FOR_CONTRAST_ONLY"]["ci95_on_ceilinged_threshold_days"],
            "iid_overstates_precision_by": boot["iid_overstates_precision_by"],
            "replicates_with_infinite_p99_share": boot["account_clustered"]["share_infinite"],
            "NEVER_REPORT_BARE": "report as a point value with the account-clustered interval, "
                                 "same treatment as W = 108 +- 18",
        },

        "RULE_STATEMENT": (
            "A user-show pair is LIVE unless its bracketing gap is at or above the threshold. "
            "For a pair with clock start T0 and window W, let tau1 = [T0] + W x 24h. On that "
            "pair's ACCOUNT, over the whole sweep -- every show and movie, not only the show "
            "under study -- take the distinct insertion instants; let b be the last instant at or "
            "before tau1 and f the first instant strictly after tau1. The bracketing gap is f - b, "
            "a continuous instant difference in days. "
            "(1) If both exist, the pair is NOT LIVE iff f - b >= threshold. "
            "(2) If no instant falls after tau1, the gap is open-ended, +inf, and the pair is NOT "
            "LIVE -- it fails any finite threshold on its own. "
            "(3) If no instant falls at or before tau1, the pair is LIVE: decisions/0021, approved "
            "gate 2 of 5, rules that any record inserted after the window closed proves the "
            "account was alive whatever date it claims. "
            "Liveness is a PAIR-level filter, never a user-level one: evidence is account-wide but "
            "tau1 is pair-specific, so one account can be live for one show and not for another. "
            "Liveness is anchored at tau1; tau2 plays no part in it (0034). Applied at Step 8 "
            "position 6, after right-censoring at position 5."
        ),

        "REALISED_RATE": {
            "against_the_extended_set_the_reference": V["V1_extended_PRIMARY"][
                "realised_rate_vs_extended_set"],
            "against_measured_gap_pairs_only": V["V1_extended_PRIMARY"][
                "realised_rate_vs_measured_gap_pairs"],
            "against_all_post_D10_pairs": V["V1_extended_PRIMARY"][
                "realised_rate_vs_all_post_D10_pairs"],
            "stated_rate": 0.01,
            "not_live_total": V["V1_extended_PRIMARY"]["not_live_total"],
            "not_live_measured_gap": V["V1_extended_PRIMARY"]["not_live_measured_gap"],
            "not_live_open_ended": V["V1_extended_PRIMARY"]["not_live_open_ended"],
            "live_pairs": V["V1_extended_PRIMARY"]["live_pairs"],
            "live_share": V["V1_extended_PRIMARY"]["live_share"],
        },

        "QUOTA_PROPERTY": (
            "Taking the percentile on the distribution the test applies to sets the level by the "
            "exclusion rate, not by any feature of the data: choosing p mechanically fixes the "
            "exclusion rate at 100 - p percent of the reference set. It is a quota, not a finding. "
            "0040 Sec 2 sharpens it: because open-ended gaps now sit INSIDE the reference set, "
            f"they consume {V['V1_extended_PRIMARY']['not_live_open_ended']} of the "
            f"{V['V1_extended_PRIMARY']['not_live_total']}-pair quota before the gap test runs, "
            "and the measured-gap test is left with what remains. That is why the threshold rose "
            "from 632 d to "
            f"{THR:.0f} d: not because gaps got longer, but because the quota got smaller."
        ),

        "INERTNESS_AS_MEASURED_ON_THIS_POPULATION": {
            "note": "MEASURED HERE, NOT CARRIED. 0040 Sec 4 withdrew the 3.45/96.55 invariance "
                    "claim as arithmetically impossible and the 5.37/94.63 figures as predating "
                    "the two changes. NO INVARIANCE IS CLAIMED.",
            "at_the_adopted_99th": {
                "gap_test_exclusions": V["V1_extended_PRIMARY"]["not_live_measured_gap"],
                "edge_case_open_ended_exclusions": V["V1_extended_PRIMARY"]["not_live_open_ended"],
                "gap_test_share": a["percentile_sweep_primary_variant"]["99.0"][
                    "gap_test_share_of_exclusions"],
                "edge_case_share": a["percentile_sweep_primary_variant"]["99.0"][
                    "edge_case_share_of_exclusions"],
            },
            "across_percentiles": a["percentile_sweep_primary_variant"],
            "what_changed": "the withdrawn edge case (ii) was 76.8% of the old filter's "
                            "exclusions; those 18,152 pairs are now LIVE, so the remaining split "
                            "is between the gap test and the open-ended bucket only.",
        },

        "EDGE_CASE_i_STILL_NEEDED_AS_A_SEPARATE_RULING": {
            "question": "0040 Sec 2: does an infinite gap simply fail a finite threshold on its own?",
            "open_ended_share_of_extended_set": a["open_ended_share_of_extended"],
            "0040_predicted": 0.00685,
            "finite_99th_over_extended_set": True,
            "answer": "NOT NEEDED AS AN EXCLUSION RULING at the 99th percentile. The extended-set "
                      "99th is finite and every open-ended gap exceeds it automatically. "
                      "STILL NEEDED AS A CONSTRUCTION RULING: something must say that an "
                      "open-ended gap enters the reference set as +inf rather than being dropped "
                      "from it -- that single choice is what moves the threshold 632 -> "
                      f"{THR:.0f} d.",
            "where_it_becomes_load_bearing_again": {
                "percentile_above_which_the_extended_p_is_infinite": a[
                    "percentile_at_which_extended_p_becomes_infinite"],
                "consequence": "above that percentile the threshold is +inf, the measured-gap test "
                               "excludes nobody, and the ONLY exclusions are the open-ended pairs "
                               "-- so the rule degenerates into edge case (i) alone.",
                "bootstrap_replicates_hitting_it_at_W_108": boot["account_clustered"][
                    "share_infinite"],
                "bootstrap_replicates_hitting_it_at_W_213": json.load(
                    open(OUT / "bootstrap_W213.json"))["account_clustered"]["share_infinite"],
            },
        },

        "REFERENCE_SET_VARIANTS_the_largest_remaining_lever": {
            "note": "0040 Sec 2 fixes the population but not the treatment of pairs with no "
                    "bracketing gap. Three readings are defensible; V1 is taken as primary "
                    "because 0040's own arithmetic (894/130,524) frames the extended set as "
                    "measured + open-ended, excluding the no-pre-instant pairs.",
            "variants": V,
        },

        "IS_THE_THRESHOLD_LOAD_BEARING_input_to_0040_Sec_6": {
            "not_live_at_ci_low": boot["account_clustered"]["not_live_at_lo"],
            "not_live_at_point": V["V1_extended_PRIMARY"]["not_live_total"],
            "not_live_at_ci_high": boot["account_clustered"]["not_live_at_hi"],
            "swing_pairs_across_the_interval": boot["account_clustered"][
                "not_live_swing_across_interval_pairs"],
            "swing_pp_of_population": boot["account_clustered"][
                "not_live_swing_across_interval_pp_of_population"],
            "share_of_population_excluded_at_point": V["V1_extended_PRIMARY"][
                "realised_rate_vs_all_post_D10_pairs"],
            "comment": "Step 9 must recompute the headline at both endpoints. The exclusion set "
                       "moves by fewer than a thousand pairs across an interval 1,410 days wide; "
                       "whether that moves the headline is Step 9's to answer, not Step 7's.",
        },

        "STEP_13_PER_ARM_REFIT": arms,

        "DERIVE_APPLY_MISMATCH_STILL_OPEN": {
            "finding": "0038 Sec 2.1 requires derivation and application populations to be "
                       "IDENTICAL. 0040 closed the D10 half of the mismatch and left the other "
                       "half open: the reference is waterfall line 4 (152,126) less D10, but "
                       "Step 8 applies liveness at position 6 to the ANALYSIS population "
                       "(201,900) less D10. Line 4 is a strict subset. This is the same defect "
                       "class 0038 Sec 2.1 names, one step milder.",
            "measured": mismatch,
            "L2_eq_1_check": "zero pairs on L2 = 1 shows in line 4, so Step 8 position 2 removes "
                             "nothing and contributes no further mismatch",
        },

        "JUDGEMENT_CALLS_THE_SPEC_DOES_NOT_SETTLE": [
            "1. Whether pairs with NO instant at or before tau1 belong in the reference "
            "distribution. They are LIVE (0021) but have no bracketing gap. V1 excludes them "
            "(primary, matching 0040's own 894/130,524 arithmetic); V3 enters them as 0. The "
            "choice moves the threshold from 1,293 d to 975 d. Largest remaining lever in the step.",
            "2. Whether the reference set includes open-ended gaps as +inf (V1) or is restricted "
            "to measured gaps (V2, 0039's basis). 0040 Sec 2 directs V1; the cost is that the "
            "threshold more than doubles, 632 -> 1,293 d, and the measured-gap test excludes 531 "
            "pairs instead of 1,275.",
            "3. Comparator direction: NOT LIVE iff gap >= threshold. 0025's reasoning implies "
            "at-or-above; the spec never states it as an operator. At 1,293 d exactly zero pairs "
            "sit on the boundary, so it does not bite here.",
            "4. Quantile method: R type-7 / numpy 'linear'. The spec names a percentile, never an "
            "estimator. Type-7 reproduces the frozen run's 631.8031 exactly.",
            "5. np.interp CLAMPS 6,956 records outside the fitted rid range (1,862 below, 5,094 "
            "above) to the endpoint instants. The calibration is a required input and is not "
            "refitted, so this is reported, not repaired. Both arms of the superseded run resolved "
            "it identically by chance (0040 Sec 7).",
            "6. D10's comparison is written '<=' and is applied as written; every other boundary "
            "in the study is half-open.",
            "7. Bootstrap endpoints: the ceilinged replicate thresholds' 2.5th taken by "
            "method='lower' and 97.5th by method='higher', so the interval is not narrowed by "
            "interpolating between adjacent replicates. B = 2,000 at the adopted arm, 1,000 "
            "elsewhere; seed recorded.",
            "8. Which W arms Step 13 runs. 0027 gives the union 38..213; the task sheet's Step 7 "
            "summary says '46 to 107 plus 150 and 213'. Eight arms are run to cover both.",
        ],

        "elapsed_s": time.time() - t,
    }

    p = ART / "step7-liveness-b4.json"
    p.write_text(json.dumps(out, indent=2, default=float))
    print("wrote", p)
    print(json.dumps(out["DERIVE_APPLY_MISMATCH_STILL_OPEN"]["measured"], indent=2))


if __name__ == "__main__":
    main()
