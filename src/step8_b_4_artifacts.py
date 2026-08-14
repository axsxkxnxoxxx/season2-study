"""Step 8 (instance b) -- stage 4: render the two artifacts and their JSON halves.

GATE. NOTHING IS ADOPTED HERE. This instance produces its deliverables and stops.

Counts and aggregates ONLY. No username, user id or individual watch history
reaches artifacts/. The analysis table itself stays in processed/.

Both halves of each deliverable are rendered from ONE object each, so agreement
between the .md and the .json is a property of the generator rather than a claim
(CLAUDE.md, "One definition per statement and per figure").

Out: artifacts/step8-waterfall-b.{md,json}, artifacts/step8-invariants-b.{md,json}
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
OUT = ROOT / "processed" / "step8" / "b"
ART = ROOT / "artifacts"

W_ARMS = [38, 46, 77, 91, 107, 108, 150, 213]
GATE = ("**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. "
        "This instance does not adopt its own proposal, does not begin Step 8b or Step 9, "
        "and records no approval — that is the Human Lead's alone. Zero API calls; every "
        "figure is computed from data already on disk.")


def fmt(n) -> str:
    return f"{n:,}" if isinstance(n, int) else (f"{n:.4f}" if isinstance(n, float) else str(n))


def main() -> None:
    R = json.loads((OUT / "results.json").read_text())
    I = json.loads((OUT / "invariants.json").read_text())
    D9 = json.loads((OUT / "d9.json").read_text())
    q = R["required_counts"]
    ex = R["emitted_beyond_the_required_list"]

    # ==================================================================
    # WATERFALL
    # ==================================================================
    wj = {
        "artifact": "step8-waterfall-b", "instance": "analytics-engineer-b", "namespace": "b",
        "step": 8, "mode": "GATE -- proposal only, nothing adopted", "api_calls": 0,
        "constants": {"W": R["W_adopted"], "H": R["H"], "tau_pull": R["tau_pull"],
                      "W_arms": R["W_arms"]},
        "populations": {
            "APPLY": {"n": 196654, "definition": "waterfall line 1 less D10; the position-5 "
                                                 "output; what position 6 filters"},
            "DERIV": {"n": 147370, "definition": "Step 5 line 4 less D10; requires S2 evidence"},
        },
        "filter_order": R["filter_order"],
        "waterfall_APPLY": R["waterfall_APPLY"],
        "waterfall_DERIV": R["waterfall_DERIV"],
        "step5_waterfall_reasserted": R["step5_waterfall_reasserted"],
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
        },
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
    }
    (ART / "step8-waterfall-b.json").write_text(json.dumps(wj, indent=2, default=str))

    L: list[str] = []
    A = L.append
    A("# Step 8 — filter waterfall and required counts (instance `b`)")
    A("")
    A(GATE)
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
      "in the implementation.")
    A("")
    A("**The analysis table is in `processed/`, not here.** "
      "`processed/step8/b/analysis_table.csv.gz`, "
      f"{R['analysis_table']['rows']:,} rows × {R['analysis_table']['columns']} columns. "
      "Its row set is the **position-5 population**, carrying the position-6 flag `live` and "
      "the position-7 `outcome`; the post-position-7 row set is `live == True`, DERIV is "
      "`in_deriv`. The 703 excluded rows are kept **in the file** with `live = False`, "
      "because Step 9's bound endpoints are built from their outcome states and rebuilding "
      "them downstream would be a second definition of the filter.")
    A("")
    A("---")
    A("")
    A("## 1. The filter order")
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
    A("## 2. Waterfall — APPLY")
    A("")
    A("| # | Filter | Retained pairs | Removed | Users | Shows |")
    A("| :-- | :--- | ---: | ---: | ---: | ---: |")
    for w in R["waterfall_APPLY"]:
        A(f"| {w['position']} | {w['filter']} | {w['retained_pairs']:,} | "
          f"{w['removed_pairs']:,} | {w.get('retained_users', ''):,} | "
          f"{w.get('retained_shows', ''):,} |")
    A("")
    A("**Position 2 removes exactly 0 pairs and 0 shows, out of 1,138 shows examined.** That "
      "is a measured zero, not an empty check. **Position 3 removes 0 by construction**, "
      "because `0068` defines line 1 as the S1-completer population — but the rule "
      "(`F1 ∈ D1` and `|D1| ≥ ceil(0.90 × L1)`, first-pass) was computed independently from "
      "the record level, and it is that computation which produced line 1. This is why the "
      "monotone-decrease invariant is coded `>=` and not `>`: **two positions here "
      "legitimately remove nothing.**")
    A("")
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
    A("## 3. Waterfall — DERIV")
    A("")
    A("| # | Filter | Retained pairs | Removed |")
    A("| :-- | :--- | ---: | ---: |")
    for w in R["waterfall_DERIV"]:
        A(f"| {w['position']} | {w['filter']} | {w['retained_pairs']:,} | "
          f"{w['removed_pairs']:,} |")
    A("")
    A("**DERIV's position 4 is not the adopted contamination exclusion alone**, and that is "
      "stated rather than hidden: DERIV is *Step 5 line 4* less D10, and line 4 applies three "
      "further restrictions — `has_s2`, `T0` not contaminated, completing record not "
      "post-dated — none of which is a Step 8 filter position. Emitting it here is what stops "
      "Step 9 rebuilding the population, which would be a second definition of it.")
    A("")
    A("## 4. Position 6 — liveness, and the population reconciliation")
    A("")
    A("The rule is **ALT-BROAD** (`0048`, restored `0054`, **approved `0064`**): a pair is "
      "**NOT LIVE iff BOTH** the account shows no insertion instant after that pair's `tau1` "
      "**AND** the pair is **NOT Continued**. **\"After\" is STRICT** — silent iff no "
      "insertion instant `> tau1` (`0068`). **The evidence is restricted to records dated "
      "before `tau_pull`** (`0070` ruling 2). The stored play-`id` isotonic calibration at "
      "`processed/step5/calibration.npz` is **read and never refitted** (`0029`).")
    A("")
    rec = I["population_reconciliation_703_and_99"]
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
      "which cannot reach position 7 because outcome assignment removes no rows.")
    A("")
    A("**Per-`W`-arm exclusion counts on APPLY**, so the `W`-coupling is visible:")
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
    A("**Measured on the position-4 output (201,900), which is what the mandated order "
      "censors.** `0033`'s 97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed on the "
      "**position-3** output; `0070` ruling 8 keeps the order and moves the published "
      "percentage.")
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
      f"**{c108['ALL']['retained_pct']:.2f}%**, and at `W = 213` the 2023–2025 cohort retains "
      f"**{c213['2023-2025']['retained_pct']:.2f}%** against "
      f"**{c213['pre-2020']['retained_pct']:.2f}%** pre-2020 — a **"
      f"{100 - c213['2023-2025']['retained_pct']:.1f}%** loss against "
      f"**{100 - c213['pre-2020']['retained_pct']:.1f}%**. Without this line, whether the "
      "modern cohort survives to the headline in usable numbers is invisible.")
    A("")
    A("**The comparator moved too, and the record does not say so.** `0070` corrected the "
      "2023–2025 loss from 10.3% to 10.5% when it kept the mandated order, but the pre-2020 "
      f"figure it is stated against — **2.7%** — was computed in the same superseded order "
      f"and is **{100 - c213['pre-2020']['retained_pct']:.1f}%** here. The task sheet's "
      "sentence *\"10.5% of its pairs against 2.7% pre-2020\"* therefore mixes one figure "
      "from the mandated order with one from the order it replaced. **Reported, not "
      "reconciled** — it is a propagation gap in the derived-figure list, not a disagreement "
      "about the rule.")
    A("")
    A("## 6. Drop counts — per show and per outcome")
    A("")
    d = q["drop_counts"]
    A(f"- Records examined for set membership: **{d['records_examined']:,}**")
    A(f"- Records dropped (`number ∉ E`, or a missing season/number): "
      f"**{d['records_dropped_total']:,}**")
    A(f"- Distinct dropped `(season, number)` pairs: "
      f"**{d['distinct_season_number_pairs_dropped']:,}**; shows with any drop: "
      f"**{d['shows_with_any_drop']:,}** of 1,138")
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
    A("**This zero is a measured zero.** Every one of the "
      f"{d['records_examined']:,} in-frame S1/S2 episode records surviving D11 was tested for "
      "membership in its season's listed set `E`, and none failed. The per-show file is "
      "`processed/step8/b/drop_counts_per_show.csv`. Direction had any been dropped: it would "
      "**inflate** Never started, the same direction as D4 and D9.")
    A("")
    A("## 7. D2 — negative-lag report, split THREE ways")
    A("")
    A("A tie is its own category, not a tiebreak (`0070` ruling 5). **168 pairs in line 1 have "
      "both terms of the `max()` binding on the same date**; of those, "
      f"{q['D2_negative_lag']['by_population']['position3_220107']['BOTH_terms_bind_tie']} "
      "also carry a negative lag.")
    A("")
    A("| Population | n | Negative lag | share | S2 finale binds | S1 completion binds | "
      "BOTH bind |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k, v in q["D2_negative_lag"]["by_population"].items():
        A(f"| {k} | {v['n']:,} | {v['negative_lag_pairs']:,} | {v['share_pct']:.2f}% | "
          f"{v['S2_finale_term_binds']:,} | {v['S1_completion_term_binds']:,} | "
          f"{v['BOTH_terms_bind_tie']:,} |")
    A("")
    A("**The population is not stated in the spec at the point of use**, so all four are "
      "reported and each is labelled. S1-term negative lags are the actual test of the "
      "first-pass choice and should be small; S2-finale-term negative lags are the normal "
      "case for anyone who watched a weekly season while it was airing, and their size is "
      "information about the frame's cadence mix rather than about data quality.")
    A("")
    A("## 8. D3′ — resumption rate, every `W` arm, each denominator its own")
    A("")
    A("Of pairs scored **Started and left at `tau2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ "
      "tau_pull`, the share completing within `[tau2, tau2 + H)`. **Each arm's denominator is "
      "its own and each population's is its own** (`0069` item 5).")
    A("")
    for pop in ("APPLY", "DERIV"):
        A(f"**{pop}**")
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
    t34 = q["D3prime"]["the_3440"]
    A(f"**Reported alongside and labelled a COUNT, not a rate: {t34['count']:,} "
      "Started-and-left pairs completing S2 at any point before `tau_pull`.**")
    A("")
    A(f"- **Population:** {t34['population']}.")
    A(f"- **Why Step 14 calls it a floor:** {t34['why_a_floor']}.")
    A(f"- **Exposure weighting, stated at the point of use:** {t34['exposure_weighting']}.")
    A("- **Restated, not recomputed.** The spec forbids reporting it against APPLY or DERIV, "
      "so no analogue of it is computed on either population here.")
    A("")
    A("**The measured cleared shares here do not match the 95.98% / 91.34% the task sheet "
      "quotes.** Those figures carry no population at their point of use; they are consistent "
      "with an **uncensored** sample, whose recent-`T0` pairs fail the clearance. Every "
      "figure in the table above is on the named, right-censored population at the named arm. "
      "**Reported, not reconciled.**")
    A("")
    A("## 9. D8 — never-started post-window diagnostic")
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
    A("## 10. D9 — split-artifact counts, both halves")
    A("")
    A(f"Signature: {D9['signature']}. **{D9['detection']}**")
    A("")
    A(f"- Candidate `(user, show)` pairs examined across the whole sweep: "
      f"**{D9['candidate_user_show_pairs_examined']:,}**")
    A(f"- Complementary signature pairs, **LOOSE** title key: "
      f"**{D9['complementary_signature_pairs_LOOSE_key']:,}**")
    A(f"- Complementary signature pairs, **STRICT** title key: "
      f"**{D9['complementary_signature_pairs_STRICT_key']:,}**")
    A("")
    A("| Half | Population / position | Count (loose) | Count (strict) | "
      "Share of Never started (loose) |")
    A("| :--- | :--- | ---: | ---: | ---: |")
    for k, v in D9["half_a_fabricated_never_started_rows"].items():
        A(f"| (a) fabricated Never started rows | {k} | "
          f"{v['carrying_a_split_signature_LOOSE']:,} | "
          f"{v['carrying_a_split_signature_STRICT']:,} | "
          f"{v['share_of_never_started_pct_LOOSE']:.4f}% |")
    hb = D9["half_b_silently_deleted_S1_failing_counterparts"]
    A(f"| **(b) the silent half** — in-frame pairs dropped at S1 completion carrying the same "
      f"signature | not on any retained population | {hb['in_frame_B_side_pairs_LOOSE']:,} | "
      f"{hb['in_frame_B_side_pairs_STRICT']:,} | — |")
    A("")
    nf = D9["normalisation_finding"]
    A("**The spec gives no title-normalisation rule, and the choice of one decides the whole "
      "number.** Two were run:")
    A("")
    A(f"- **loose** — {nf['loose_key']}")
    A(f"- **strict** — {nf['strict_key']}")
    A("")
    A(f"**{nf['what_it_shows']}.** The largest loose clusters are "
      + ", ".join(f"`{k}` ({v})" for k, v in nf["largest_loose_clusters"].items())
      + " — franchises with several distinct shows, not split metadata.")
    A("")
    A(f"**Consequence, stated because it runs opposite to the caveat the spec supplies:** "
      f"{nf['consequence']}.")
    A("")
    A(f"**{D9['same_title_multi_ID_groups']['count']:,} same-title multi-ID groups** were also "
      f"counted. {D9['same_title_multi_ID_groups']['note']}.")
    A("")
    A(f"Direction of half (a): {D9['direction']}.")
    A("")
    A("## 11. D4 — S3 without S2")
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
    A("| Flag | Shows | Pairs at position 4 |")
    A("| :--- | ---: | ---: |")
    for k, v in q["metadata_disagreement"]["flags"].items():
        A(f"| `{k}` | {v['shows']:,} | {v['pairs_position4']:,} |")
    A("")
    A(f"**{q['metadata_disagreement']['coverage_note'].capitalize()}.**")
    A("")
    A(f"Direction, named as required: {q['metadata_disagreement']['s2_aired_lt_listed_direction']}.")
    A("")
    A("## 14. `pull_date`, fetch window, and discarded records")
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
    A(f"{pd_['note'].capitalize()}.")
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
      "identical under both readings; only lines 1, 2 and 3 move.**")
    A("")
    A("## 15. Outcome states, channel pairs, and the scope qualifier")
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
      "— **90 started-and-left and 207 never-started on APPLY, 89 and 3 on DERIV** — and the "
      "`p = 1.0` residual "
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
      "attempted are **absent, not empty**, and none of them contributes a row.")
    A("")
    A("## 16. Discovery channel")
    A("")
    dc = R["discovery_channel"]
    A(f"**Two boolean columns, not one categorical** (`0070` ruling 3). Of the "
      f"{dc['pool_users']:,} pooled users, **324 are in both channels**; a single value would "
      "drop the overlap or assign it arbitrarily. Among the "
      f"{dc['accounts_in_the_analysis_population']:,} accounts in the analysis population: "
      f"channel A only **{dc['accounts_channel_A_only']:,}**, channel B only "
      f"**{dc['accounts_channel_B_only']:,}**, **both {dc['accounts_in_BOTH']:,}**, neither "
      f"**{dc['accounts_in_NEITHER']:,}**.")
    A("")
    A("## 17. `action` — counts by type, never a row-level column")
    A("")
    A("`action` is record-level and the row is a pair, so a single value per row would assert "
      "one action per pair, which is false (`0070` ruling 4). The table carries eight count "
      "columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the "
      "four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is this "
      "instance's choice**; the spec says \"counts by action type\" and does not fix the "
      "grain. Step 1 already ruled that check-ins count as watching alongside `scrobble` and "
      "`watch`, because `action` is a property of the logging client rather than of the "
      "viewing, so it is **not an outcome variable**.")
    A("")
    A("## 18. Where two faithful instances could still differ")
    A("")
    for i, s in enumerate(DIVERGENCES, 1):
        A(f"{i}. {s}")
    A("")
    A("---")
    A("")
    A(GATE)
    (ART / "step8-waterfall-b.md").write_text("\n".join(L) + "\n")

    # ==================================================================
    # INVARIANTS
    # ==================================================================
    (ART / "step8-invariants-b.json").write_text(json.dumps(I, indent=2, default=str))
    M: list[str] = []
    B = M.append
    B("# Step 8 — invariant report (instance `b`)")
    B("")
    B(GATE)
    B("")
    B("## How to read this report")
    B("")
    B(f"**{I['how_to_read_this_report']}**")
    B("")
    B(f"Counts: **{I['counts']['pure_code_checks']} pure code checks**, "
      f"**{I['counts']['code_check_by_construction_and_data_check_as_specified']} that is a "
      "code check by construction and a genuine cross-check as specified**, "
      f"**{I['counts']['additional_range_check_emitted']} additional range check emitted**, "
      f"and **{I['counts']['items_that_are_not_invariants']} item that is not an invariant at "
      "all** — the 703 expectation, which is a population reconciliation.")
    B("")
    B("| # | Invariant | Label | Result |")
    B("| :-- | :--- | :--- | :--- |")
    for i, iv in enumerate(I["invariants"], 1):
        B(f"| {i} | {iv['invariant']} | **{iv['label']}** | "
          f"**{'PASS' if iv['passes'] else 'FAIL'}** |")
    B("")
    B(f"**All invariants pass: {I['all_pass']}.** That statement says the code computed what "
      "it was told to. It is **not** evidence for the liveness rule, for the outcome "
      "definition, or for any published share.")
    B("")
    for i, iv in enumerate(I["invariants"], 1):
        B(f"## {i}. {iv['invariant']}")
        B("")
        B(f"**Label: {iv['label']}.** "
          f"{iv.get('why_it_cannot_fail_on_data', iv.get('what_gives_it_force', ''))}.")
        B("")
        if "why_ge_not_gt" in iv:
            B(f"**Why `>=` and not `>`:** {iv['why_ge_not_gt']}.")
            B("")
            B(f"- APPLY sequence: {iv['sequence_APPLY']}")
            B(f"- DERIV sequence: {iv['sequence_DERIV']}")
            B(f"- Positions removing exactly zero on APPLY: "
              f"{iv['positions_removing_zero_APPLY']}")
            B("")
        for k in ("result", "checked", "independent_recomputation",
                  "second_external_cross_check", "clauses_on_the_position_5_population",
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
        B(f"**Result: {'PASS' if iv['passes'] else 'FAIL'}.**")
        B("")
    B("## The 703 expectation is NOT an invariant")
    B("")
    B(f"{rec['this_is_NOT_an_invariant'].capitalize()}.")
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
    B("---")
    B("")
    B(GATE)
    (ART / "step8-invariants-b.md").write_text("\n".join(M) + "\n")
    print("wrote 4 artifacts")


DIVERGENCES = [
    "**The analysis table's row set.** The spec says \"build one row per user-show pair\" and "
    "\"write the table to `processed/`\" without naming which position's rows. This instance "
    "emits the **position-5** population with `live` and `outcome` as columns, so the "
    "post-position-7 set is a filter on it and Step 9 does not have to rebuild the 703. An "
    "instance emitting only the post-position-7 rows would be equally faithful and would "
    "produce a file with 195,951 rows. **No published count differs; the file shape does.**",

    "**D11 and waterfall line 1.** `0068` rules 220,107 and leaves the D11 question open. "
    "Lines 1–3 are 220,107 here and would be 220,103 under the other reading; lines 4–7 are "
    "identical either way, verified.",

    "**D3′'s cleared shares.** The task sheet quotes 95.98% at `W = 46` falling to 91.34% at "
    "`W = 213` with no population at the point of use. On the named, right-censored "
    "populations this instance measures 99.53% and 97.73% on APPLY. The direction and the "
    "shrinkage agree; the level does not. Reported, not reconciled.",

    "**D8's position.** Pre- or post-liveness is unstated. Both are reported.",

    "**D2's population.** Unstated at the point of use. Four are reported and each labelled.",

    "**D9's title-normalisation rule.** None is specified, and it decides the number: the "
    "strict key (no year stripping) returns **0** complementary signature pairs, the loose "
    "key (year stripped) returns **75**, and the loose key's largest clusters are remakes. "
    "Two instances choosing differently would report 6 and 0 for half (a).",

    "**The pre-2020 censoring comparator.** `0070` moved the 2023–2025 loss at `W = 213` from "
    "10.3% to 10.5% but left the 2.7% it is compared against, which was computed in the "
    "superseded order and is 3.0% under the mandated one.",

    "**The grain of the `action` counts.** \"Per-pair counts by action type\" does not fix "
    "whether the counts are split by season. This instance splits S1 and S2, because Step "
    "13's arm needs the composition of the S2 evidence set and the S1 completion evidence "
    "separately.",

    "**The waterfall's unit.** Pairs are primary; users and shows are reported alongside "
    "because position 2 is explicitly a filter on shows.",

    "**Undated records.** 379 records in the sweep carry no `watched_at`. None is an in-frame "
    "S1/S2 episode record, so they touch no outcome. They are **not** discarded by D11, which "
    "removes `watched_at >= tau_pull`; a reading that requires a record to be positively "
    "\"dated before `tau_pull`\" would drop them from the liveness evidence. Measured inert: "
    "the exclusion counts are identical either way at every arm.",

    "**DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three "
    "restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore not "
    "the adopted contamination exclusion, and is labelled as such rather than silently "
    "conflated with APPLY's.",

    "**At `W = 213` the DERIV started-and-left exclusion component is 147 while APPLY's is "
    "148.** No published figure covers DERIV per arm above `W = 108`, so this is new rather "
    "than divergent, and it is stated so it is not read as an error later.",

    "**`processed/step5/adopted_rule.json` carries revision-3 figures** (`retained 215,258`, "
    "`removed 4,849`) and is superseded by revision 6 (201,900 retained, 18,207 excluded). "
    "This instance reads the exclusion from `pair_revision5.csv` and re-asserts the Step 5 "
    "waterfall line by line before using it. `processed/` is not one of `CLAUDE.md`'s seven "
    "propagation surfaces, so the grep control does not cover the file a Step 8 "
    "implementation would reach for first.",
]

if __name__ == "__main__":
    main()
