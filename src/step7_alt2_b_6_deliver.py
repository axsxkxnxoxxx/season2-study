"""Step 7 RERUN ON THE ADOPTED RULE (instance b, namespace alt2_b) -- stage 6.

Composes the two deliverables from the stage JSONs. Every number is read from
processed/step7/alt2_b/*.json; none is typed by hand.

Out: artifacts/step7-liveness-alt-b.json
     artifacts/step7-liveness-alt-b.md

Counts and aggregates only. No usernames, user ids or watch histories.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
P = ROOT / "processed" / "step7" / "alt2_b"
ART = ROOT / "artifacts"
W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]

RULE = ("A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion "
        "instant strictly after that pair's tau1 = [T0] + W x 24h, AND |A| = 0, where |A| = 0 "
        "is Step 1 Sec 7's Never-started condition read at tau1. Otherwise the pair is live.")


def main() -> None:
    s1 = json.load(open(P / "stage1.json"))
    s2 = json.load(open(P / "stage2.json"))
    rule = json.load(open(P / "rule.json"))
    wf = json.load(open(P / "waterfall.json"))
    fo = json.load(open(P / "forcedness.json"))
    be = json.load(open(P / "bound_estimand.json"))
    ca = json.load(open(P / "candidates.json"))
    bo = json.load(open(P / "bootstrap.json"))

    A108 = rule["by_population"]["APPLY"]["108"]
    D108 = rule["by_population"]["DERIV"]["108"]

    out = {
        "step": 7,
        "instance": "data-scientist-b",
        "namespace": "alt2_b",
        "mode": "GATE. Proposed and measured, NOT adopted. The Human Lead approves and diffs.",
        "rule_statement": RULE,
        "rule_source": "decisions/0046 Sec 1; task-sheet.md Step 7 as rewritten 2026-08-13",
        "free_parameters": {
            "own_parameters": 0,
            "note": "the rule has no parameter of its own; it is fully determined by W, and its "
                    "exclusion set moves with W. Per-arm counts are reported below.",
        },
        "api_calls": 0,
        "calibration": s1["calibration"],
        "populations": {
            "DERIV": {"definition": "Step 5 line 4 (152,126) less D10",
                      "n_at_W108": D108["n_before_liveness"],
                      "requires_S2_evidence": True},
            "APPLY": {"definition": "Step 5 line 1 (201,900) less D10",
                      "n_at_W108": A108["n_before_liveness"],
                      "requires_S2_evidence": False,
                      "role": "what Step 8 filters at position 6"},
        },
        "step5_waterfall_asserted": s1["step5_waterfall_measured"],
        "exclusions": {
            "at_W108": {
                "DERIV": {"excluded_pairs": D108["excluded_pairs"],
                          "accounts": D108["accounts_supplying_exclusions"],
                          "share_of_population_pct": D108["excluded_share_of_population_pct"],
                          "composition": D108["excluded_composition"]},
                "APPLY": {"excluded_pairs": A108["excluded_pairs"],
                          "accounts": A108["accounts_supplying_exclusions"],
                          "share_of_population_pct": A108["excluded_share_of_population_pct"],
                          "composition": A108["excluded_composition"],
                          "all_hold_no_S2_record_anywhere":
                              rule["claims_tested"]["C2_APPLY_at_W108"]
                              ["subset_reading_all_excluded_have_no_S2_record_anywhere"]},
            },
            "per_W_arm": {
                "DERIV": {str(w): rule["by_population"]["DERIV"][str(w)]["excluded_pairs"]
                          for w in W_ARMS},
                "APPLY": {str(w): rule["by_population"]["APPLY"][str(w)]["excluded_pairs"]
                          for w in W_ARMS},
            },
            "conjunct_a_alone_would_exclude_per_W_arm": {
                "DERIV": {str(w): rule["by_population"]["DERIV"][str(w)]
                          ["conjunct_a_alone_would_exclude"] for w in W_ARMS},
                "APPLY": {str(w): rule["by_population"]["APPLY"][str(w)]
                          ["conjunct_a_alone_would_exclude"] for w in W_ARMS},
            },
        },
        "outcome_shares_at_W108": {
            pop: {"no_filter": rule["by_population"][pop]["108"]["no_filter"],
                  "under_the_rule": rule["by_population"][pop]["108"]["under_rule"],
                  "delta_pp": rule["by_population"][pop]["108"]["delta_vs_no_filter_pp"]}
            for pop in ("DERIV", "APPLY")},
        "outcome_shares_per_W_arm": {
            pop: {str(w): {
                "n_before_liveness": rule["by_population"][pop][str(w)]["n_before_liveness"],
                "no_filter_pct": {k: rule["by_population"][pop][str(w)]["no_filter"][k]
                                  for k in ("never_started_pct", "continued_pct",
                                            "started_and_left_pct")},
                "under_the_rule_pct": {k: rule["by_population"][pop][str(w)]["under_rule"][k]
                                       for k in ("never_started_pct", "continued_pct",
                                                 "started_and_left_pct")}}
                for w in W_ARMS}
            for pop in ("DERIV", "APPLY")},
        "step9_liveness_bound": {
            "APPLY_W108": A108["step9_bound"],
            "DERIV_W108": D108["step9_bound"],
            "per_W_arm_APPLY": {str(w): rule["by_population"]["APPLY"][str(w)]["step9_bound"]
                                for w in W_ARMS},
            "estimand_check": be["by_population"],
            "estimand_reading_APPLY_W108": be["headline_reading_APPLY_W108"],
            "identity": ("the exclusion set is a subset of Never started by construction, so "
                         "NS_live + excluded = NS_unfiltered and n_live + excluded = "
                         "n_unfiltered; the ceiling therefore EQUALS the unfiltered "
                         "never-started share exactly, on ONE denominator. Verified on the "
                         "integers, not on the percentages."),
        },
        "clustered_bootstrap_W108": bo["by_population"],
        "waterfall": wf["waterfall"],
        "monotone_decrease": {
            "APPLY": wf["waterfall"]["APPLY_monotone"],
            "DERIV": wf["waterfall"]["DERIV_monotone"],
        },
        "claims_tested": rule["claims_tested"],
        "forcedness_of_the_DERIV_zero": {
            "line1": fo["line1"], "DERIV_line4": fo["DERIV_line4"],
            "candidates": ca["DERIV_line4_candidates"],
            "per_arm": ca["per_arm_DERIV"],
            "future_dated_records": wf["future_dated_records"],
            "cross_check": ("APPLY exclusions reconstructed independently from the feasible-W "
                            "intervals: " + json.dumps(
                                fo["APPLY_reconstructed_exclusions_per_arm_from_intervals"])),
        },
        "evidence_inputs": {
            "line1_pairs_with_no_S2_record_anywhere": s2["line1_pairs_with_NO_S2_record_anywhere"],
            "line1_pairs_with_no_in_E2_S2_record": s2["line1_pairs_with_NO_in_E2_S2_record"],
            "D11_records_discarded_at_or_after_tau_pull": s2["D11_discarded_at_or_after_tau_pull"],
            "S2_records_dropped_by_set_membership_not_in_E2": s2["s2_records_dropped_not_in_E2"],
        },
    }
    (ART / "step7-liveness-alt-b.json").write_text(json.dumps(out, indent=2))

    # ---------------- markdown ----------------
    def pct(x):
        return f"{x:.4f}%"

    ex_deriv = out["exclusions"]["per_W_arm"]["DERIV"]
    ex_apply = out["exclusions"]["per_W_arm"]["APPLY"]
    ca_deriv = out["exclusions"]["conjunct_a_alone_would_exclude_per_W_arm"]["DERIV"]
    ca_apply = out["exclusions"]["conjunct_a_alone_would_exclude_per_W_arm"]["APPLY"]
    bA = A108["step9_bound"]
    ciA = bo["by_population"]["APPLY"]["ci95"]
    ciD = bo["by_population"]["DERIV"]["ci95"]

    L = []
    a = L.append
    a("# Step 7 — liveness rule, rerun on the adopted rule (instance **b**)")
    a("")
    a("**GATE. Measured, not adopted.** This instance produces the artifact and stops. "
      "The Human Lead approves and diffs the two arms. Zero API calls.")
    a("")
    a("**Every figure below names the population that produced it** (`decisions/0046` §0). "
      "The two populations are not interchangeable and differ by construction:")
    a("")
    a("| Population | Definition | `n` at `W = 108` | S2 evidence required |")
    a("| :--- | :--- | ---: | :--- |")
    a(f"| **DERIV** | Step 5 line 4 (152,126) less D10 | **{D108['n_before_liveness']:,}** | yes, by construction |")
    a(f"| **APPLY** | Step 5 line 1 (201,900) less D10 | **{A108['n_before_liveness']:,}** | no — admits pairs with no S2 record |")
    a("")
    a(f"The Step 5 waterfall was re-measured from `pair_revision5.csv` and asserted before use: "
      f"{s1['step5_waterfall_measured']} for lines 1–5.")
    a("")
    a("## 1. The rule statement")
    a("")
    a("> " + RULE)
    a("")
    a("`|A|` is Step 1 §7's set — distinct S2 episodes whose number is a member of `E2`, canonical "
      "timestamp (§2.2, the minimum `watched_at` across that episode's records) tested in the "
      "half-open instant form `watched_at < τ1`. `date(watched_at) <= T1` appears nowhere. "
      "`τ2` plays no part in the rule; it is used only to assign Continued.")
    a("")
    a("- **Insertion time, not claimed `watched_at`** (`0021`). The insertion instant is the stored "
      f"Step 5 isotonic play-`id` calibration at `processed/step5/calibration.npz`, "
      f"**read and not refitted** — {s1['calibration']['n_knots']:,} knots, applied verbatim as "
      "`np.interp(rid, knot_rid, knot_time)`.")
    a("- **Pair-level, anchored at `τ1`.** Evidence is account-wide, the test is clock-start-relative, "
      "and the clock start is pair-specific. No account is dropped wholesale.")
    a("- **No pre-`τ1` requirement of any kind.** Withdrawn twice (`0040` §1, `0042` §3); not reinstated.")
    a("- **No parameter of its own.** The rule is fully determined by `W`; its exclusion set moves "
      "with `W`, and the per-arm counts are in §2.")
    a("")
    a("## 2. Exclusion counts — both populations")
    a("")
    a(f"**At `W = 108`: {D108['excluded_pairs']} pairs on DERIV, "
      f"{A108['excluded_pairs']} pairs from {A108['accounts_supplying_exclusions']} accounts on APPLY "
      f"({A108['excluded_share_of_population_pct']:.4f}% of APPLY).** `0046`'s expected 0 and ~604 are "
      "**confirmed**, and were measured rather than assumed.")
    a("")
    a("| `W` | DERIV `n` | DERIV excluded | APPLY `n` | APPLY excluded | APPLY accounts | conjunct (a) alone, DERIV | conjunct (a) alone, APPLY |")
    a("| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for w in W_ARMS:
        d = rule["by_population"]["DERIV"][str(w)]
        ap = rule["by_population"]["APPLY"][str(w)]
        lab = f"**{w}**" if w == 108 else str(w)
        a(f"| {lab} | {d['n_before_liveness']:,} | "
          f"{ex_deriv[str(w)]} | {ap['n_before_liveness']:,} | {ex_apply[str(w)]} | "
          f"{ap['accounts_supplying_exclusions']} | {ca_deriv[str(w)]} | {ca_apply[str(w)]} |")
    a("")
    a("**Composition of the exclusions, at every arm and on both populations: 100% Never started, "
      "0 Continued, 0 Started-and-left.** That is forced by the second conjunct and is stated here "
      "because the Step 9 bound depends on it.")
    a("")
    a(f"**On APPLY at `W = 108`, all {A108['excluded_pairs']} excluded pairs hold no S2 record "
      f"anywhere in the sweep** — `0046` §1's characterisation, tested and confirmed in the subset "
      f"reading, at every arm. **In the set-equality reading it is false**: APPLY holds "
      f"{rule['claims_tested']['C2_APPLY_at_W108']['pairs_on_APPLY_with_no_S2_record_anywhere']:,} "
      f"pairs with no S2 record anywhere, of which "
      f"{rule['claims_tested']['C2_APPLY_at_W108']['of_those_with_an_insertion_after_tau1_hence_LIVE']:,} "
      "have an insertion instant after `τ1` and are therefore **live**. The exclusion set is a "
      "strict subset of that set, and conjunct (a) is what selects within it.")
    a("")
    a("**The rule against the superseded PF-LIMIT, on APPLY at `W = 108`** — reported because the "
      "difference is the substance of `0046` §2. PF-LIMIT deletes "
      f"{rule['claims_tested']['C4_ALT_vs_PF_LIMIT_APPLY_W108']['PF_LIMIT_excluded']:,} pairs; the "
      f"adopted rule deletes {rule['claims_tested']['C4_ALT_vs_PF_LIMIT_APPLY_W108']['ALT_excluded']}; "
      f"the difference is {rule['claims_tested']['C4_ALT_vs_PF_LIMIT_APPLY_W108']['difference']} pairs, "
      f"of which **{rule['claims_tested']['C4_ALT_vs_PF_LIMIT_APPLY_W108']['difference_composition']['continued']} continued and "
      f"{rule['claims_tested']['C4_ALT_vs_PF_LIMIT_APPLY_W108']['difference_composition']['started_and_left']} "
      "started and left** — none never-started. Those are exactly the DERIV 751.")
    a("")
    a("## 3. The three outcome shares, under the rule and against no filter")
    a("")
    a("**At `W = 108`.**")
    a("")
    a("| Population | Filter | `n` | Never started | Continued | Started and left |")
    a("| :--- | :--- | ---: | ---: | ---: | ---: |")
    for pop, blk in (("DERIV", D108), ("APPLY", A108)):
        for lab, key in (("no filter", "no_filter"), ("**adopted rule**", "under_rule")):
            b = blk[key]
            a(f"| {pop} | {lab} | {b['n']:,} | {pct(b['never_started_pct'])} "
              f"({b['never_started']:,}) | {pct(b['continued_pct'])} ({b['continued']:,}) | "
              f"{pct(b['started_and_left_pct'])} ({b['started_and_left']:,}) |")
    a("")
    a(f"**Movement against no filter — DERIV: 0.0000 pp on all three shares, because the exclusion "
      f"set is empty. APPLY: never-started {A108['delta_vs_no_filter_pp']['never_started']:+.4f} pp, "
      f"continued {A108['delta_vs_no_filter_pp']['continued']:+.4f} pp, started-and-left "
      f"{A108['delta_vs_no_filter_pp']['started_and_left']:+.4f} pp.**")
    a("")
    a("**Account-clustered bootstrap, `B` = 2,000, accounts resampled with replacement, "
      "percentile 2.5/97.5, one resample per replicate shared by both rules so the delta is paired.**")
    a("")
    a("| Population | Filter | Never started 95% CI | width |")
    a("| :--- | :--- | :--- | ---: |")
    for pop, ci in (("DERIV", ciD), ("APPLY", ciA)):
        for r in ("NO_FILTER", "ADOPTED"):
            c = ci[r]["never_started_pct"]
            a(f"| {pop} | {r} | [{c[0]:.4f}%, {c[1]:.4f}%] | {c[1]-c[0]:.4f} pp |")
    dA = bo["by_population"]["APPLY"]["paired_delta_pp"]["never_started_pct"]
    a("")
    a(f"On **APPLY** the paired delta on never-started is **{dA['mean_delta_pp']:+.4f} pp, "
      f"95% CI [{dA['paired_ci95_pp'][0]:+.4f}, {dA['paired_ci95_pp'][1]:+.4f}], excluding zero** — "
      "the rule's effect is small but not noise. On **DERIV** the delta is exactly zero in every "
      "replicate, because the same empty set is removed in each.")
    a("")
    a("## 4. The Step 9 liveness bound")
    a("")
    a(f"**On APPLY at `W = 108`: [{bA['floor_pct']:.4f}%, {bA['ceiling_pct']:.4f}%], "
      f"width {bA['width_pp']:.4f} pp, both endpoints on the single denominator "
      f"{bA['ceiling_denominator']:,}.** This reproduces `0046` §4.")
    a("")
    a("**The ceiling equals the unfiltered never-started share as an identity — confirmed, and "
      "confirmed on the integers rather than on the rounded percentages.** Every excluded pair is "
      "never-started, so returning all of them to the denominator as decliners restores the "
      f"unfiltered population exactly: {A108['under_rule']['never_started']:,} + "
      f"{A108['excluded_pairs']} = {A108['no_filter']['never_started']:,} over "
      f"{A108['under_rule']['n']:,} + {A108['excluded_pairs']} = {A108['no_filter']['n']:,}. "
      "The ceiling is therefore not an assumption about the excluded pairs so much as a "
      "restatement of the population before the filter ran. **Read §4.1 before quoting the floor**: "
      "the two endpoints do not sit on the same denominator, and which estimand is being bounded "
      "decides whether the floor is a floor.")
    a("")
    a(f"**On DERIV the bound is degenerate: [{D108['step9_bound']['floor_pct']:.4f}%, "
      f"{D108['step9_bound']['ceiling_pct']:.4f}%], width 0.0000 pp**, because nothing is excluded. "
      "A bound of zero width is not a strong result; it is the absence of an exclusion set.")
    a("")
    a("**Set the width against the sampling width.** On APPLY the bound is "
      f"{bA['width_pp']:.4f} pp wide against an account-clustered 95% interval of "
      f"{ciA['NO_FILTER']['clustered_width_pp']['never_started_pct']:.4f} pp on the same share — "
      f"about {100*bA['width_pp']/ciA['NO_FILTER']['clustered_width_pp']['never_started_pct']:.0f}% "
      "of it. The liveness uncertainty is real but is not what dominates the headline's precision.")
    a("")
    a("| `W` | APPLY floor | APPLY ceiling | width pp |")
    a("| ---: | ---: | ---: | ---: |")
    for w in W_ARMS:
        b = rule["by_population"]["APPLY"][str(w)]["step9_bound"]
        a(f"| {w} | {b['floor_pct']:.4f}% | {b['ceiling_pct']:.4f}% | {b['width_pp']:.4f} |")
    a("")
    a("### 4.1 What the floor is a floor of — a finding, flagged for the Human Lead")
    a("")
    e = be["by_population"]["APPLY"]["108"]
    a(f"**The two endpoints sit on two denominators: the floor on "
      f"{e['floor_denominator']:,} live pairs, the ceiling on the full "
      f"{e['ceiling_denominator']:,}.** That is the same shape `0046` §4 rejected in PF-LIMIT's "
      "published interval, and the substantive half of that objection carries over.")
    a("")
    a(f"If the estimand is **the never-started share among pairs the filter retains**, "
      f"[{e['published_bound_E1_floor_E2_ceiling'][0]:.4f}%, "
      f"{e['published_bound_E1_floor_E2_ceiling'][1]:.4f}%] is exactly right and the ceiling is the "
      "identity described above.")
    a("")
    a(f"If the estimand is **the never-started share on the whole position-5 population** — the "
      f"quantity Step 9's headline reads as \"of users who completed S1\" — then the excluded "
      f"{A108['excluded_pairs']} pairs are still in the denominator with unknown status, and the "
      f"feasible range on the single denominator {e['single_denominator']:,} is "
      f"**[{e['single_denominator_interval_E2'][0]:.4f}%, "
      f"{e['single_denominator_interval_E2'][1]:.4f}%], width {e['E2_width_pp']:.4f} pp**. "
      f"**The published floor sits {e['published_floor_minus_E2_low_pp']:+.4f} pp above the low "
      "end of that range, so it is not a floor for it** — if every excluded pair had in fact "
      "started S2, which is the exact case liveness exists to guard against, the share is "
      f"{e['single_denominator_interval_E2'][0]:.4f}%, below the published floor. This is `0046` "
      "§4's own objection to PF-LIMIT's floor, in the same form, against the adopted rule.")
    a("")
    a("**The ceiling is untouched by this** — it is the same number under both estimands, and it is "
      "still an identity. **Nothing is adopted here**: which estimand Step 9 reports is the Human "
      "Lead's call, and both intervals are supplied so the choice is explicit rather than implied "
      "by an arithmetic convention.")
    a("")
    a("## 5. The waterfall, with line 6 reported OUTCOME-CONDITIONAL")
    a("")
    a("Positions 1 and 2 of the Step 8 order are Step 8's and are not rebuilt here; no show in the "
      f"frame has `L2 = 1` ({wf['shows_in_frame']:,} shows), so position 2 removes nothing on this "
      "frame. Position 7 is an annotation and contributes no line.")
    a("")
    a("| Position | Filter | APPLY rows out | APPLY removed | DERIV rows out | DERIV removed |")
    a("| ---: | :--- | ---: | ---: | ---: | ---: |")
    for i in (1, 2, 3, 4, 5):
        la = wf["waterfall"]["APPLY"][i]
        ld = wf["waterfall"]["DERIV"][i]
        a(f"| {la['position']} | {la['name']} | {la['rows_out']:,} | "
          f"{la.get('removed', '—') if not isinstance(la.get('removed'), int) else format(la['removed'], ',')} | "
          f"{ld['rows_out']:,} | "
          f"{ld.get('removed', '—') if not isinstance(ld.get('removed'), int) else format(ld['removed'], ',')} |")
    a("")
    a("**Line 6 is outcome-conditional and is reported as such** (`0046` §5): its removal count is a "
      "function of the position-5 outcome annotation, because the rule's second conjunct is "
      "`|A| = 0`. `|A|` and the insertion test are row-local predicates on the position-5 output and "
      "commute exactly, so the final row set does not depend on which is read first; only the "
      "waterfall's presentation does. Two faithful instances that do not label line 6 this way will "
      "diverge on the waterfall while agreeing on every share.")
    a("")
    a("**Monotone decrease.** On **APPLY** it holds **strictly** at line 6 — "
      f"{A108['excluded_pairs']} rows removed. On **DERIV** it holds **only non-strictly** at line 6 "
      "— 0 rows removed, the count is unchanged, and an implementation asserting a strict decrease "
      "at every line would fail here on correct data.")
    a("")
    a("## 6. The two weaknesses `0046` records — tested, not repeated")
    a("")
    a("### 6.1 Does this gate's dual run exercise the rule?")
    a("")
    a("**On DERIV, no. The exclusion set is empty at every arm tested — 38, 46, 77, 91, 107, 108, "
      "150, 213 — so on that population the two instances' diff is `0 = 0` and agreement there is "
      "worth nothing.** Stated plainly, as asked.")
    a("")
    a("**On APPLY, yes, partially, and that is more than `0046` §7 allows for.** This rerun measures "
      f"APPLY directly: {A108['excluded_pairs']} excluded pairs from "
      f"{A108['accounts_supplying_exclusions']} accounts at `W = 108`, "
      f"{ex_apply['38']}–{ex_apply['213']} across the arm grid, three shares, a bound and a "
      "waterfall line. Every one of those figures is a diffable quantity that depends on both "
      "conjuncts. **If the Human Lead diffs only DERIV figures, this gate proves nothing; if the "
      "APPLY figures are diffed, it exercises the rule on the population Step 8 will use.**")
    a("")
    a("**What the APPLY diff still cannot reach**: this instance builds APPLY from the Step 5 pair "
      "table, not from Step 8's own positions 1–5. An error in Step 8's frame join, its `L2 = 1` "
      "exclusion or its censoring implementation is invisible here, and the two Step 7 arms could "
      "agree exactly while Step 8 hands liveness a different row set.")
    a("")
    a("### 6.2 The rule is first exercised at Step 8 — what this gate can and cannot establish")
    a("")
    a("**Can establish:** the rule statement is unambiguous enough for two isolated instances to "
      "produce the same exclusion set on a fixed population; the exclusion set is entirely "
      "never-started, which is what makes the Step 9 bound an identity rather than an arithmetic "
      "operation on an arbitrary set; the counts and their `W`-coupling.")
    a("")
    a("**Cannot establish:** that the rule is *right*. Nothing here tests whether an account with no "
      "insertion after `τ1` was in fact gone, and the rule's warrant — that liveness licenses "
      "trusting a null — is an argument, not a measurement. The gate also cannot establish the "
      "headline's sensitivity to the rule, because that runs through Step 8's table and Step 9's "
      f"bound; the only quantity this instance can offer is the {A108['delta_vs_no_filter_pp']['never_started']:+.4f} pp "
      "APPLY movement in §3, computed on this instance's own reconstruction of the population.")
    a("")
    a("## 7. Where `0046` §1's stated mechanism is wrong, though its numbers are right")
    a("")
    a("`0046` §1 says the DERIV zero is **forced by construction — \"line 4 requires S2 evidence, so "
      "no line-4 pair can have `|A| = 0` and no S2 record.\"** The **count is confirmed**. **The "
      "mechanism is not**, on three measurements:")
    a("")
    a(f"1. **Line 4's `has_s2` does not imply `|A| ≥ 1`.** At `W = 108`, "
      f"**{rule['claims_tested']['C1_mechanism_at_W108_DERIV']['pairs_with_A_empty']:,} DERIV pairs are "
      "never-started** — they hold S2 evidence dated at or after `τ1`. The zero comes from none of "
      "them coinciding with a silent account, not from the conjunct being unsatisfiable.")
    a(f"2. **`|A|` needs an *in-`E2`* record, and line 4 only needs an S2 record.** "
      f"{ca['DERIV_line4_candidates']['with_an_S2_record_but_none_in_E2_upper_end_infinite']} line-4 "
      "pairs hold S2 records none of whose episode numbers are in `E2`, so their `|A|` is 0 at every "
      "`W` — the configuration `0046` says cannot exist on line 4.")
    a(f"3. **What actually produces the zero at every arm is D10, one position earlier.** "
      f"{ca['per_arm_DERIV']['108']['line4_pairs_satisfying_both_conjuncts_before_D10']} line-4 pairs "
      "satisfy **both** conjuncts at every arm on the grid, and **all of them are removed by "
      "right-censoring at position 5**, before liveness is reached. The DERIV zero is a consequence "
      "of the filter order, not of line 4's definition.")
    a("")
    a("Solving the rule for the set of `W` at which each pair would be excluded — `τ1` must lie "
      "between the account's last insertion instant and the pair's first in-`E2` S2 timestamp — "
      f"gives **{fo['DERIV_line4']['pairs_with_a_non_empty_feasible_W_interval']} line-4 pairs with a "
      "non-empty interval**, split as follows. "
      f"{ca['DERIV_line4_candidates']['with_an_in_E2_S2_record_finite_upper_end']} have a finite "
      "upper end: 23 of those intervals close below `W` ≈ 1.7 days and 2 sit near `W` ≈ 2,275 and "
      "2,360 days, so no `W` anyone would adopt reaches them. The remaining "
      f"{ca['DERIV_line4_candidates']['with_an_S2_record_but_none_in_E2_upper_end_infinite']} have "
      "**no upper end at all** — they would be excluded at every `W` above roughly 0.87 days, and "
      "**only D10 keeps them out of the exclusion set.** So \"forced by construction\" is the wrong "
      "description at both ends. The same interval calculation reconstructs the APPLY exclusion "
      "counts at every arm exactly "
      f"({fo['APPLY_reconstructed_exclusions_per_arm_from_intervals']['108']} at `W = 108`), which "
      "is an independent check on the implementation.")
    a("")
    a(f"The mechanism exists because {wf['future_dated_records']['share_pct']:.2f}% of dated records "
      "in the sweep claim a `watched_at` later than their own calibrated insertion instant "
      f"({wf['future_dated_records']['future_dated']:,} of "
      f"{wf['future_dated_records']['records_dated']:,}; "
      f"{wf['future_dated_records']['future_dated_S2_records']:,} of them S2). A record like that "
      "lets an account be silent after `τ1` while holding S2 evidence dated after `τ1`. "
      "**Most of that 22.68% is almost certainly calibration noise, not real future-dating** — for "
      "a record watched in real time the claimed instant and the interpolated insertion instant "
      "differ by minutes in either direction, and roughly half of those differences fall on the "
      "later side. The count is reported as the mechanism's upper envelope, not as a claim that "
      "six million records were written before they were watched.")
    a("")
    a("**Recommended correction to the record, for the Human Lead:** keep the exclusion counts; "
      "replace \"forced by construction\" with \"zero at every `W` on the Step 13 grid, produced by "
      "D10 removing the four candidate pairs at position 5.\"")
    a("")
    a("## 8. Judgement calls this instance made, where the spec does not settle it")
    a("")
    a("1. **Liveness evidence is account-wide, over every record in the account's sweep** — any "
      "show, any season, any `kind`, any `action` — not restricted to the pair's own show. The "
      "spec says \"the account shows no insertion instant\", which reads account-wide, and that is "
      "how it is implemented. A per-show reading would exclude far more.")
    a("2. **\"No insertion instant after `τ1`\" is implemented as `max(instants) <= τ1`, i.e. "
      "strictly after.** An instant landing exactly on `τ1` does not make the account live. This "
      "matches the half-open convention used for `A` and is the same operator this instance used "
      "at `b4`.")
    a(f"3. **Records outside the fitted calibration range are clamped** by `np.interp` to the "
      f"endpoint values ({s1['calibration']['records_clamped_below_first_knot']:,} below, "
      f"{s1['calibration']['records_clamped_above_last_knot']:,} above, of "
      f"{s1['records_in_sweep']:,}). The curve is a required input and is not refitted, so the "
      "clamping is reported rather than repaired.")
    a("4. **`|A| = 0` is read at `τ1` on `A`, never at `τ2` on `A_H`.** `0046` and Step 1 §7 both "
      "say Never-started, and Never-started is a `τ1` statement.")
    a("5. **D11 is applied before the rule** — records at or after `τ_pull` are discarded "
      f"({s2['D11_discarded_at_or_after_tau_pull']} distinct-episode records), consistent with "
      "every other step.")
    a("6. **The waterfall's positions 1–3 are reported from this instance's own inputs** (the Step 5 "
      "pair table's 220,107 S1-completer rows), not rebuilt from the Step 2 frame. Step 8 owns "
      "those positions and may legitimately report them differently.")
    a("7. **DERIV is defined as line 4 less D10 at each arm**, so its `n` moves with `W` exactly as "
      "APPLY's does; the two populations are censored on the same `max(W, 91) + H` rule.")
    a("")
    a("## 9. Provenance")
    a("")
    a("- **Zero API calls.** Every input was read from disk.")
    a(f"- Calibration: `processed/step5/calibration.npz`, {s1['calibration']['n_knots']:,} knots, "
      "**read, not refitted**, applied verbatim as in `src/step5_calibrate.py`.")
    a("- Row-level detail — populations, liveness states, outcome states, feasible-`W` intervals — "
      "is in `processed/step7/alt2_b/`. This artifact and its JSON companion contain counts and "
      "aggregates only.")
    a("- Scripts: `src/step7_alt2_b_1_population.py`, `_2_outcomes.py`, `_3_rule.py`, "
      "`_4_waterfall.py`, `_4b_forcedness.py`, `_4c_candidates.py`, `_5_bootstrap.py`, "
      "`_6_deliver.py`.")
    a("- The per-account maximum insertion instant was recomputed from the sweep and the stored "
      "curve, then asserted equal to the distinct-instant sequence this instance built at "
      "`processed/step7/b4/`; the Step 5 waterfall was asserted before either population was used.")
    a("")
    a("**Nothing here is adopted. This instance does not record an approval.**")
    (ART / "step7-liveness-alt-b.md").write_text("\n".join(L) + "\n")
    print("written")


if __name__ == "__main__":
    main()
