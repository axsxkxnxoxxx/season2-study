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
RERUN = ("**This is the RERUN ordered by the Human Lead on `decisions/0077`, which no arm had "
         "executed against.** `0077` fixes the discovery-channel overlap's missing population, "
         "restates `0075` ruling 2 — which named an empty set, since position 3 removes zero "
         "rows — and fixes the column names. `0074`, `0075` and `0076` postdate the first run "
         "and are also carried. This overwrites the previous `-b` deliverables.")


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

    DIV = divergences(R, D9, S1)

    # ==================================================================
    # WATERFALL
    # ==================================================================
    wj = {
        "artifact": "step8-waterfall-b", "instance": "analytics-engineer-b", "namespace": "b",
        "step": 8, "mode": "GATE -- proposal only, nothing adopted", "api_calls": 0,
        "run": ("RERUN on the spec as amended by decisions/0077, carrying 0074, 0075 and 0076"),
        "constants": {"W": R["W_adopted"], "H": R["H"], "tau_pull": R["tau_pull"],
                      "W_arms": R["W_arms"],
                      "W_arms_source": "decisions/0075 ruling 3 -- the grid's first statement"},
        "populations": {
            "APPLY": {"n": 196654, "definition": "waterfall line 1 less D10; the position-5 "
                                                 "output; what position 6 filters"},
            "DERIV": {"n": 147370, "definition": "Step 5 line 4 less D10; requires S2 evidence"},
        },
        "filter_order": R["filter_order"],
        "waterfall_APPLY": R["waterfall_APPLY"],
        "waterfall_DERIV": R["waterfall_DERIV"],
        "step5_waterfall_reasserted": R["step5_waterfall_reasserted"],
        "position3_drop_set_side_output": S1["position3_drop_set"],
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
    (ART / "step8-waterfall-b.json").write_text(json.dumps(wj, indent=2, default=str))

    L: list[str] = []
    A = L.append
    A("# Step 8 — filter waterfall and required counts (instance `b`)")
    A("")
    A(GATE)
    A("")
    A(RERUN)
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
    A("**The analysis table is in `processed/`, not here.** "
      "`processed/step8/b/analysis_table.csv.gz`, "
      f"{R['analysis_table']['rows']:,} rows × {R['analysis_table']['columns']} columns. "
      "Its row set is the **position-5 population**, with `live` and `outcome` carried as "
      "**columns** (`0074` ruling 1); the post-position-7 row set is `live == True` "
      f"({R['waterfall_APPLY'][6]['retained_pairs']:,}), and DERIV is `in_deriv` "
      f"({R['waterfall_DERIV'][4]['retained_pairs']:,}). The "
      f"{R['waterfall_APPLY'][5]['removed_pairs']:,} excluded rows are kept **in the "
      "file** with `live = False`, so nothing downstream has to reconstruct them — a "
      "reconstruction that agrees today is still a second definition tomorrow.")
    A("")
    cn = R["analysis_table"]["column_names_are_fixed_by_0077"]
    A("**Column names follow `0077` §3 exactly**, and every adopted name is present with no "
      "superseded form beside it: `in_apply` / `in_deriv`, `tau1` / `tau2`, `n_A` / `n_A_H` / "
      "`max_episode_in_A_H` / `f2_in_A_H`, the eight `action_count_s{1,2}_*`, "
      "`discovered_channel_a` / `discovered_channel_b`, `t0_binding_term` / `t0_date` / "
      "`s1_completion_date`, and both retained extras — `has_s3_or_later_evidence` (added this "
      "run; D4 reads it) and `s1_completion_used_a_post_cutoff_record` (the open "
      "D11-at-position-3 question reads it).")
    A("")
    A(f"**But the ruled count of {cn['count_ruled']} columns is not reachable from the names "
      f"`0077` gives, and this instance emits {cn['count_emitted']}.** Reported as a defect "
      "rather than worked around. `0077` §3 states the rerun produced **88 against 87 for the "
      "same contents**, keeps *both* instances' extra columns and names **two**. This "
      "instance's previous run emitted **87 including the second of those two**; adding the "
      "first gives **88**. Reaching 89 needs **one further column that `0077` does not name** "
      "— the set arithmetic on `0077`'s own figures (88 ∪ 87 = 89 ⇒ intersection 86) implies "
      "exactly one unnamed column on the other arm, and the alternative reading is that 89 was "
      "formed as 87 + 2 while that 87 already held one of the two. **An isolated instance "
      "cannot identify it from any surface it is permitted to read, and inventing a column to "
      "hit the count would produce a different 89th and make the diff worse rather than "
      "better.** The full emitted name list is in "
      "`artifacts/step8-waterfall-b.json` → `analysis_table.column_names`.")
    A("")
    A("---")
    A("")
    A("## 1. The filter order, and the side output it needs")
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
    p3 = S1["position3_drop_set"]
    A("**Position 3's drop set is retained as a side output** (`0075` ruling 2, **restated by "
      f"`0077` §2**), at `{p3['file']}`. Under `0068` line 1 *is* the S1-completer population, "
      "so position 3 removes **0 from the waterfall** — which is why the ruling as first "
      "written named an empty set. The restated set is **the pair universe less the "
      "completers, 58,345 PAIRS**, carrying each pair's distinct-episode counts and the show's "
      "threshold. It is **not** the set-membership drop rule, which is a different rule, "
      "deletes **0 records**, and is counted in records rather than pairs. **D9 half (b) is "
      "measured on this set**; without it that half emits zero, and a zero there reads as a "
      "data finding rather than a missing input. **This instance's first run retained exactly "
      "this set and reports the same 58,345**, so the restatement moves no figure here — it "
      "removes the choice.")
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
    A("**`processed/step5/adopted_rule.json` is now read and cross-checked, not worked "
      "around.** `0074` ruling 6 made `processed/` the eighth propagation surface and "
      "corrected that file, which had carried revision-3 figures (4,849 removed / 215,258 "
      f"retained). It now states **{cc['file_says_removed']:,} removed / "
      f"{cc['file_says_retained']:,} retained of {cc['file_says_of_total']:,}**, and this "
      f"instance measures **{cc['measured_removed']:,} / {cc['measured_retained']:,} of "
      f"{cc['measured_of_total']:,}** — agreement **{cc['agrees']}**, component by component. "
      "On the first run this file was the reason the Step 5 waterfall had to be re-asserted "
      "line by line; the re-assertion is kept, because a corrected surface is a reason to "
      "cross-check it and not a reason to stop checking.")
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
      "Step 9 rebuilding the population, which would be a second definition of it "
      "(`0070` ruling 1).")
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
    d = q["drop_counts"]
    dn = S1["drop_rule"]["denominator_note"]
    A("**This is a COVERAGE COUNT, not an invariant** (`0074` ruling 3). Records examined and "
      "records dropped are reported; nothing is asserted.")
    A("")
    A(f"- Records examined for set membership: **{d['records_examined']:,}**")
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
    A("### The denominator, all three readings")
    A("")
    A("`0074` ruling 4 publishes **6,065,704 against 6,065,610**, both reporting 0 drops, and "
      "rules the difference **reported, not reconciled**. This instance's examined count is "
      f"**{dn['this_instances_examined_count']:,}**. The other two readings on the same data "
      "are stated so the figure is not mistaken for a disagreement about the rule:")
    A("")
    A("| Reading | Records |")
    A("| :--- | ---: |")
    A(f"| in-frame S1/S2 episode records, **before any D11** | "
      f"{dn['in_frame_S1_S2_episode_records_before_any_D11']:,} |")
    A(f"| **this instance** — D11 applied to the S2 side, S1 side carried | "
      f"{dn['this_instances_examined_count']:,} |")
    A(f"| D11 applied to **both** seasons | {dn['if_D11_were_applied_to_BOTH_seasons']:,} |")
    A("")
    A("The S1 side is carried unfiltered here for one reason: `0068` rules waterfall line 1 at "
      "**220,107 as published**, and 4 pairs complete S1 only on a record `D11` would discard. "
      "**The three readings differ by 94 and by 73 records respectively, all of them "
      "post-cutoff, and all three report 0 drops.** Nothing downstream depends on the "
      "denominator. **Reported, not reconciled**, per `CLAUDE.md`.")
    A("")
    A(f"**The zero is a measured zero.** Every one of the {d['records_examined']:,} records "
      "was tested for membership in its season's listed set `E`, and none failed. The per-show "
      "file is `processed/step8/b/drop_counts_per_show.csv`. Direction had any been dropped: "
      "it would **inflate** Never started, the same direction as D4 and D9.")
    A("")
    A("## 7. D2 — negative-lag report, split THREE ways")
    A("")
    A("A tie is its own category, not a tiebreak (`0070` ruling 5). **"
      f"{q['D2_negative_lag']['tie_pairs_in_line1']} pairs in line 1 have both terms of the "
      "`max()` binding on the same date**; of those, "
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
      "so no analogue of it is computed on either population here.")
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
    A(f"Candidate `(user, show)` pairs examined across the whole sweep: "
      f"**{D9['candidate_user_show_pairs_examined']:,}** — "
      f"{D9['sides']['A_side_S1_not_S2']:,} carrying S1 and not S2, "
      f"{D9['sides']['B_side_S2_not_S1']:,} carrying S2 and not S1, "
      f"{D9['sides']['both_seasons']:,} carrying both.")
    A("")
    A("### The keys, which are now defined in the spec")
    A("")
    A("**`0074` ruling 5 ruled STRICT; `0076` §3 defined both keys**, because \"strict\" and "
      "\"loose\" had existed only inside one instance's code and the ruled key was undefined "
      "on every surface an isolated instance reads.")
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
    A("| Population / position | Never started | STRICT (ruled) | LOOSE (alongside) | "
      "Share, loose |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for k, v in D9["half_a_fabricated_never_started_rows"].items():
        A(f"| {k} | {v['never_started_n']:,} | {v['carrying_a_split_signature_STRICT']:,} | "
          f"{v['carrying_a_split_signature_LOOSE']:,} | "
          f"{v['share_of_never_started_pct_LOOSE']:.4f}% |")
    A("")
    A("### Half (b) — the silently deleted S1-failing counterparts")
    A("")
    hb = D9["half_b_silently_deleted_S1_failing_counterparts"]
    A("**Measured on position 3's retained drop set** (`0075` ruling 2). These are pairs that "
      f"{hb['why_they_are_invisible_otherwise']}.")
    A("")
    A("| | STRICT (ruled) | LOOSE (alongside) |")
    A("| :--- | ---: | ---: |")
    A(f"| B-side pairs on frame shows | {hb['STRICT']['B_side_pairs_in_frame']:,} | "
      f"{hb['LOOSE']['B_side_pairs_in_frame']:,} |")
    A(f"| of those, present in the retained position-3 drop set | "
      f"{hb['STRICT']['of_those_present_in_the_retained_position3_drop_set']:,} | "
      f"{hb['LOOSE']['of_those_present_in_the_retained_position3_drop_set']:,} |")
    A(f"| of those, in the S2-evidence-and-no-S1-evidence subset | "
      f"{hb['STRICT']['of_those_in_the_S2_evidence_and_NO_S1_evidence_subset']:,} | "
      f"{hb['LOOSE']['of_those_in_the_S2_evidence_and_NO_S1_evidence_subset']:,} |")
    A("")
    A(f"Every one of the {hb['LOOSE']['B_side_pairs_in_frame']} loose-key B-side pairs is "
      "accounted for inside the retained drop set — **which is the check that the side output "
      "is the right population and not merely a convenient one.**")
    A("")
    nf = D9["normalisation_finding"]
    A(f"**{nf['what_it_shows']}.** The largest loose clusters are "
      + ", ".join(f"`{k}` ({v})" for k, v in nf["largest_loose_clusters"].items())
      + " — remakes and national versions, not split metadata.")
    A("")
    A(f"**Why the loose count publishes even though strict is ruled:** {nf['consequence']}.")
    A("")
    A(f"Direction: {D9['direction']}.")
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
    A("## 16. Discovery channel")
    A("")
    dc = R["discovery_channel"]
    A("**Two boolean columns, not one categorical** (`0070` ruling 3). **Every overlap count "
      "states its population** (`0077` §1): `0070` ruling 3 said *\"324 users\"* and named "
      "none, and a count without its population is the shape that has recurred through this "
      "entire chain. All three populations are **measured here, not restated**:")
    A("")
    A("| Population | n | Channel A only | Channel B only | **Both** | Neither |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for k, lbl in (("step3_discovery_pool", "Step 3 discovery pool (usernames)"),
                   ("accounts_pulled_step4_complete", "Accounts pulled — Step 4 `complete`"),
                   ("accounts_in_the_APPLY_position5_population",
                    "Accounts in the APPLY position-5 population")):
        v = dc[k]
        A(f"| {lbl} | {v['n']:,} | {v['channel_A_only']:,} | {v['channel_B_only']:,} | "
          f"**{v['BOTH']:,}** | {v['NEITHER']:,} |")
    A("")
    A("**Both of `0077`'s figures reproduce exactly — 324 of 5,694 and 178 of 2,549** — and "
      "the third line is the one Step 11 actually cuts on, which neither ruling states. "
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
    A("## 17. `action` — counts by type, never a row-level column")
    A("")
    A("`action` is record-level and the row is a pair, so a single value per row would assert "
      "one action per pair, which is false (`0070` ruling 4). The table carries eight count "
      "columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the "
      "four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is this "
      "instance's choice**; the spec says \"counts by action type\" and does not fix the "
      "grain. Step 1 already ruled that check-ins count as watching alongside `scrobble` and "
      "`watch`, because `action` is a property of the logging client rather than of the "
      "viewing, so it is **not an outcome variable**. Step 13's arm reads the counts: "
      "check-in-only iff its `checkin` count is positive and `scrobble` and `watch` are zero.")
    A("")
    A("## 18. Where two faithful instances could still differ")
    A("")
    for i, s in enumerate(DIV, 1):
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
    B(RERUN)
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
    B("| # | Invariant | Label | Result |")
    B("| :-- | :--- | :--- | :--- |")
    for i, iv in enumerate(I["invariants"], 1):
        B(f"| {i} | {iv['invariant']} | **{iv['label']}** | "
          f"**{'PASS' if iv['passes'] else 'FAIL'}** |")
    B("")
    B(f"**All invariants pass: {I['all_pass']}.** For six of the eight that statement says the "
      "code computed what it was told to. It is **not** evidence for the liveness rule, for "
      "the outcome definition, or for any published share. **The two that could have failed "
      "are §7 and §8, and what they found is reported in full below rather than as a tick.**")
    B("")
    for i, iv in enumerate(I["invariants"], 1):
        B(f"## {i}. {iv['invariant']}")
        B("")
        B(f"**Label: {iv['label']}.** "
          f"{iv.get('why_it_cannot_fail_on_data', iv.get('why_it_can_fail', iv.get('what_gives_it_force', '')))}.")
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
              f"{iv['positions_removing_zero_APPLY']}")
            B("")
        for k in ("result", "checked", "independent_recomputation",
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
    wh = I["invariants"][6]["checked"]
    B(f"**Wholesale dropping.** On APPLY, **{wh['APPLY']['accounts_holding_BOTH_a_live_and_a_not_live_pair']} "
      f"of the {wh['APPLY']['accounts_supplying_at_least_one_not_live_pair']} accounts that "
      "supply a liveness exclusion also keep at least one live pair.** An account-level filter "
      "would make that number exactly zero, so this discriminates between the two "
      "implementations, which the 703-from-216 figure alone does not. The single account whose "
      "pairs are all not-live holds exactly one pair in the population, where the two "
      "implementations are indistinguishable by construction.")
    B("")
    ad = I["invariants"][7]["checked"]
    B(f"**Skipped accounts read as empty.** Zero `access_denied` and zero `private_or_absent` "
      "were recorded across the whole Step 4 pull, so the 403-skip path never fired. The "
      f"skipped accounts nevertheless exist — **{ad['accounts_by_final_outcome'].get('discarded_over_tolerance', 0)} "
      f"discarded over tolerance and {ad['accounts_by_final_outcome'].get('skipped_length_forecast', 0)} "
      "skipped on the length forecast** — and **none of them is parsed, indexed, or present in "
      "the table**: of the "
      f"{ad['accounts_in_the_parsed_sweep']:,} accounts in the parsed sweep, "
      f"{ad['parsed_accounts_whose_final_ledger_outcome_is_NOT_complete']} have a non-complete "
      f"final ledger outcome and {ad['parsed_accounts_with_no_ledger_row_at_all']} have no "
      "ledger row at all. They are **absent, not empty**, which is what the rule requires.")
    B("")
    B("## Reported and NOT asserted (1) — the set-membership drop rule")
    B("")
    cov = I["coverage_count_not_an_invariant"]
    B(f"{cov['status']}.")
    B("")
    B(f"- Records examined: **{cov['records_examined']:,}**")
    B(f"- Records dropped: **{cov['records_dropped']:,}**")
    B("")
    B("The denominator has three readings on this data and `0074` ruling 4 publishes two of "
      "them unreconciled; all three are tabulated in "
      "`artifacts/step8-waterfall-b.md` §6.")
    B("")
    B("## Reported and NOT asserted (2) — the 703 expectation")
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


def divergences(R: dict, D9: dict, S1: dict) -> list[str]:
    """Every figure in this list is READ FROM THE MEASURED OBJECTS, not typed.

    CLAUDE.md: derived figures are regenerated, not patched -- "if you find
    yourself editing a derived number by hand, that is the defect."
    """
    at = R["analysis_table"]
    cn = at["column_names_are_fixed_by_0077"]
    dn = S1["drop_rule"]["denominator_note"]
    p3 = S1["position3_drop_set"]
    dc = R["discovery_channel"]
    d3 = R["per_arm"]["APPLY"]
    k = D9["keys"]
    last = str(R["W_arms"][-1])
    return [
        f"**THE COLUMN COUNT. `0077` §3 fixes the names and states {cn['count_ruled']} "
        f"columns; this instance emits {cn['count_emitted']}.** Every name `0077` adopts is "
        "present and no superseded form is, and both retained extras are carried. The 89th is "
        "**not named anywhere an isolated instance may read**: `0077`'s own figures give "
        "88 ∪ 87 = 89, which implies one unnamed column on the other arm, unless 89 was formed "
        "as 87 + 2 while that 87 already held one of the two. **The ruling was written to stop "
        "Step 8b inheriting a column divergence, and on this reading it leaves one**, since an "
        "instance that guesses a 89th and an instance that does not both diverge from the "
        "other. Reported, not guessed at.",

        "**D11 and waterfall line 1.** `0068` rules "
        f"{S1['s1_completion']['S1_completer_pairs_line_1']:,} and leaves the D11 question "
        "open. Lines 1–3 are that figure here and would be "
        f"{S1['s1_completion']['D11_open_question']['S1_completer_pairs_if_D11_applied_to_S1_too']:,}"
        " under the other reading; lines 4–7 are identical either way, verified row by row.",

        "**The set-membership denominator.** `0074` ruling 4 publishes 6,065,704 against "
        f"6,065,610 unreconciled. This instance examines "
        f"{dn['this_instances_examined_count']:,}; the other two readings on the same data are "
        f"{dn['in_frame_S1_S2_episode_records_before_any_D11']:,} (before any D11) and "
        f"{dn['if_D11_were_applied_to_BOTH_seasons']:,} (D11 applied to both seasons). The "
        "choice follows from how D11 is applied on the S1 side, which follows from `0068`'s "
        "ruled line 1. **Reported, not reconciled**; all three drop zero records.",

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

        "**The grain of the `action` counts.** \"Per-pair counts by action type\" does not fix "
        "whether the counts are split by season. This instance splits S1 and S2, because Step "
        "13's arm needs the composition of the S2 evidence set and the S1 completion evidence "
        "separately. A pooled-count instance would report four columns rather than eight and "
        "no published figure would move.",

        "**The shape of the position-3 drop set — now ruled, and it agrees.** `0075` ruling 2 "
        "named an empty set; `0077` §2 restates it as the pair universe less the completers, "
        f"{p3['dropped_by_the_S1_completion_rule']:,} pairs, with distinct-episode counts and "
        "the show's threshold. This instance's first run had already chosen that set and "
        "reports the same count, so the restatement removes the choice without moving a "
        "figure.",

        "**The discovery-channel overlap on the population Step 11 cuts.** `0077` §1 states "
        f"{dc['step3_discovery_pool']['BOTH']} of {dc['step3_discovery_pool']['n']:,} and "
        f"{dc['accounts_pulled_step4_complete']['BOTH']} of "
        f"{dc['accounts_pulled_step4_complete']['n']:,}; both reproduce. **The overlap on the "
        "APPLY position-5 population is "
        f"{dc['accounts_in_the_APPLY_position5_population']['BOTH']} of "
        f"{dc['accounts_in_the_APPLY_position5_population']['n']:,} accounts and is stated in "
        "no ruling** — an instance reporting only the two ruled figures and one reporting the "
        "third are both faithful.",

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
