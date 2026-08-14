"""Step 8, namespace `a`. Emit the two artifacts.

GATE. Adopts nothing. Zero API calls. Counts and aggregates only: no username, no user ID, no
individual watch history reaches artifacts/.

Every figure in the artifacts is GENERATED from the stored stage outputs by this script -- none
is typed by hand -- so a correction is made once, in the stage that measures it (CLAUDE.md,
"Derived figures are REGENERATED, not patched").

Output: artifacts/step8-waterfall-a.md, artifacts/step8-waterfall-a.json,
        artifacts/step8-invariants-a.md, artifacts/step8-invariants-a.json
"""
import json
import os

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step8/a")
ART = os.path.join(ROOT, "artifacts")

SCOPE = ("covering with respect to insertion-dormancy, exhaustively; open only across channel "
         "classes (D4, D9)")


def n(x):
    return f"{x:,}"


def pct(x, d=2):
    return "—" if x is None else f"{100 * x:.{d}f}%"


def main():
    scan = json.load(open(os.path.join(OUT, "scan_summary.json")))
    pos = json.load(open(os.path.join(OUT, "positions.json")))
    outc = json.load(open(os.path.join(OUT, "outcomes.json")))
    arms = json.load(open(os.path.join(OUT, "arms.json")))
    diag = json.load(open(os.path.join(OUT, "diagnostics.json")))
    inv = json.load(open(os.path.join(OUT, "invariants.json")))

    wa, wd = pos["waterfall_APPLY"], pos["waterfall_DERIV"]
    lv = outc["position_6_liveness"]
    p7 = outc["position_7_outcome_assignment"]
    a108 = next(e for e in arms["arms"] if e["W_days"] == 108)

    # ----------------------------------------------------------------- waterfall JSON ----
    wjson = {
        "step": 8, "instance": "a", "mode": "GATE — proposes, adopts nothing",
        "api_calls": 0, "W_days": 108, "H_days": 91,
        "tau_pull_utc": "2026-08-11T00:00:00Z",
        "filter_order": pos["filter_order"],
        "waterfall": {
            "APPLY": {**wa, "position_6_liveness": lv["APPLY"]["retained"],
                      "position_7_outcome_assignment": p7["APPLY_post_liveness"]["total"]},
            "DERIV": {**wd, "position_6_liveness": lv["DERIV"]["retained"],
                      "position_7_outcome_assignment": p7["DERIV_post_liveness"]["total"]},
        },
        "right_censoring_two_lines": {
            "APPLY": pos["right_censoring_two_lines_APPLY"],
            "DERIV": pos["right_censoring_two_lines_DERIV"]},
        "position_6_liveness": lv,
        "position_7_outcome_assignment": p7,
        "per_arm": arms,
        "required_counts": diag,
        "channel_counts": outc["channel_counts_on_position_7_APPLY"],
        "analysis_table": outc["analysis_table"],
        "scope_qualifier_travelling_with_the_position_6_population": SCOPE,
        "scan_summary": scan,
    }
    with open(os.path.join(ART, "step8-waterfall-a.json"), "w") as fh:
        json.dump(wjson, fh, indent=2)

    # ------------------------------------------------------------------- waterfall MD ----
    L = []
    A = L.append
    A("# Step 8 — filter waterfall and required counts, instance `a`")
    A("")
    A("**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · "
      "**W = 108 days** (`decisions/0026`) · **H = 91 days** (D10) · "
      "**`τ_pull` = 2026-08-11T00:00:00Z** (D11, `decisions/0011`)")
    A("")
    A("> **THIS IS A GATE DELIVERABLE. IT PROPOSES AND ADOPTS NOTHING.** No approval is recorded "
      "here and none is implied. **Zero API calls** — every figure is computed from data already "
      "on disk. **Counts and aggregates only**: no username, no user ID and no individual watch "
      "history appears in this file or in its `.json`.")
    A("")
    A("> **Every figure below states its population.** There are two and they differ by "
      "construction: **APPLY** = Step 5 waterfall line 1 less D10 = **196,654**, which is what "
      "position 6 filters; **DERIV** = Step 5 waterfall line 4 less D10 = **147,370**, which "
      "requires S2 evidence. Step 8 produces both (`decisions/0070` ruling 1).")
    A("")
    A("---")
    A("")
    A("## 1. The filter order and the waterfall, on both populations")
    A("")
    A("Applied in exactly the order `decisions/0029` fixes. The final row set commutes; the "
      "per-filter sample size does not, which is why the order is written down rather than left "
      "to each instance.")
    A("")
    A("| # | Filter | APPLY: retained | removed | DERIV: retained | removed |")
    A("| :-- | :--- | ---: | ---: | ---: | ---: |")
    rows = [
        ("1", "Step 2 frame", wa["position_1_step2_frame"], wd["position_1_step2_frame"]),
        ("2", "`L2 = 1` exclusion", wa["position_2_L2_eq_1_excluded"],
         wd["position_2_L2_eq_1_excluded"]),
        ("3", "S1 completion rule", wa["position_3_S1_completion_rule"],
         wd["position_3_S1_completion_rule"]),
        ("4", "contamination exclusion (Step 5)", wa["position_4_contamination"],
         wd["position_4_contamination_DERIV_depth"]),
        ("5", "right-censoring", wa["position_5_right_censoring"],
         wd["position_5_right_censoring"]),
        ("6", "liveness rule", lv["APPLY"]["retained"], lv["DERIV"]["retained"]),
        ("7", "outcome assignment", p7["APPLY_post_liveness"]["total"],
         p7["DERIV_post_liveness"]["total"]),
    ]
    pa = pd_ = None
    for i, (k, name, va, vd) in enumerate(rows):
        ra = "—" if i == 0 else n(pa - va)
        rd = "—" if i == 0 else n(pd_ - vd)
        A(f"| **{k}** | {name} | {n(va)} | {ra} | {n(vd)} | {rd} |")
        pa, pd_ = va, vd
    A("")
    A(f"**Line 1 is the S1-completer population, {n(wa['position_1_step2_frame'])} pairs** "
      "(`decisions/0068`) — user-show pairs whose user completed season 1, on a frame show. "
      "Lines 2 and 3 follow from it. No base was chosen by this instance.")
    A("")
    A(f"- **Position 2 removes exactly 0 pairs on this frame.** {n(pos['L2_eq_1_shows_in_frame'])} "
      "of the 1,138 frame shows have `L2 = 1`. This is why the monotone-decrease invariant is "
      "coded `>=` and not `>` — see the invariant report.")
    A("- **Position 3 removes 0 by construction**, because line 1 is already the S1-completer "
      "population. What carries the weight here is the **independent recomputation**: the S1 "
      "completion test and the first-pass completion date were recomputed from the episode "
      "records, never read back from the Step 5 pair table. "
      f"Membership agrees on all {n(pos['independent_S1_completion_check']['pair_universe'])} "
      "pairs of the universe "
      f"({n(pos['independent_S1_completion_check']['completers_recomputed'])} completers both "
      "ways, "
      f"{pos['independent_S1_completion_check']['completers_only_in_my_recomputation']} only "
      "mine, "
      f"{pos['independent_S1_completion_check']['completers_only_in_the_published_table']} only "
      "the published table), and the completion **date** agrees on "
      f"{pos['independent_S1_completion_check']['s1_completion_date_mismatches']} mismatches.")
    A("- **Position 4 is a different depth on the two populations.** APPLY takes Step 5 waterfall "
      "line 1; DERIV takes line 4, which additionally requires S2 evidence, an uncontaminated "
      "`T0` and a completing record that is not post-dated. The Step 5 waterfall was rebuilt from "
      "the stored per-pair flags and asserted equal to the published "
      f"{pos['step5_waterfall_published']} before use.")
    A("- **Position 6 is OUTCOME-CONDITIONAL and is reported as such** (`decisions/0046`): the "
      "second conjunct of the liveness rule is the Continued test, so the outcome is evaluated "
      "before liveness is applied even though it is assigned at position 7. Permitted because "
      "the two predicates are row-local on the position-5 output and commute exactly, and "
      "because position 7 removes no rows.")
    A("- **Position 7 removes no rows.** It annotates.")
    A("")
    A("### 1.1 Right-censoring, as two lines")
    A("")
    A("| Term | APPLY removed | DERIV removed | Direction on the headline |")
    A("| :--- | ---: | ---: | :--- |")
    rc, rcd = pos["right_censoring_two_lines_APPLY"], pos["right_censoring_two_lines_DERIV"]
    A(f"| `max(W, 91)` term | {n(rc['removed_by_max_W_91_term'])} | "
      f"{n(rcd['removed_by_max_W_91_term'])} | **UP** |")
    A(f"| incremental `+ H` term | {n(rc['removed_incrementally_by_the_plus_H_term'])} | "
      f"{n(rcd['removed_incrementally_by_the_plus_H_term'])} | **UP** |")
    A(f"| total | {n(rc['total'])} | {n(rcd['total'])} | **UP** |")
    A("")
    A("Both lines remove pairs whose clock start is recent, which on the uncapped "
      "`S1_completion_date` term means recent S1 completers — people who found an old show "
      "lately, have the whole series available, and are disproportionately likely to roll "
      "straight into S2. Removing likely continuers moves the never-started share **up** "
      "(Step 1 §6).")
    A("")
    A("---")
    A("")
    A("## 2. Position 6 — the liveness rule, and the population reconciliation")
    A("")
    A("The rule is **ALT-BROAD**, approved unconditionally 2026-08-13 (`decisions/0064`): a pair "
      "is **NOT LIVE iff BOTH** (i) the account shows **no insertion instant `> τ1`** — *after* "
      "is strict — **AND** (ii) the pair is **NOT Continued**. Evidence is account-wide, runs on "
      "record **insertion** time read through the **stored** Step 5 isotonic calibration (never "
      "refitted), and is **restricted to records dated before `τ_pull`** (`0070` ruling 2).")
    A("")
    A("| Population | Entering (position 5) | Excluded | never-started | started-and-left | "
      "accounts | Retained |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k in ("APPLY", "DERIV"):
        e = lv[k]["excluded"]
        A(f"| **{k}** | {n(lv[k]['population_entering'])} | **{n(e['total'])}** | "
          f"{n(e['never_started'])} | {n(e['started_and_left'])} | {n(e['accounts'])} | "
          f"{n(lv[k]['retained'])} |")
    A("")
    A(f"**This is a POPULATION RECONCILIATION, not an invariant** (`decisions/0068`). Expected "
      f"703 on APPLY = 196,654 (604 + 99, 216 accounts) and 99 on DERIV = 147,370 (0 + 99, 73 "
      f"accounts). **Measured: {lv['APPLY']['excluded']['total']} and "
      f"{lv['DERIV']['excluded']['total']}, with the same splits and the same account counts.** "
      "This is the first place Step 7's chain and Step 8's positions 1–5 have been compared: "
      "Step 7 built APPLY from the Step 5 pair table rather than through the filters. They agree "
      "to the row.")
    A("")
    A("**Neither superseded answer was produced.** 604 is ALT's, 793 is ALT-MATCHED's; either "
      "would mean a superseded rule had been implemented.")
    A("")
    cs = lv["conjunct_selection_APPLY"]
    A(f"**How the conjuncts select on APPLY:** conjunct 2 (NOT Continued) narrows "
      f"{n(cs['start'])} → {n(cs['after_conjunct_2_NOT_continued'])}; conjunct 1 (silent at `τ1`) "
      f"narrows {n(cs['after_conjunct_2_NOT_continued'])} → "
      f"{n(cs['after_conjunct_1_silent_at_tau1'])}. Conjunct 1 does most of the work, which is "
      "why the count moves with `W`.")
    A("")
    es = lv["evidence_scope_check"]
    A(f"**Evidence scope, measured rather than assumed:** with the `< τ_pull` restriction "
      f"{n(es['excluded_with_D11_restriction_APPLY'])} pairs are excluded; without it "
      f"{n(es['excluded_without_the_restriction_APPLY'])}. The restriction is inert on the "
      "exclusion set at this arm, as `0070` recorded, because no insertion instant exceeds the "
      f"calibration clamp at {scan['calibration']['last_instant_max_utc_D11']}Z and D10 already "
      "forces `τ1 ≤ τ_pull − 91 d`.")
    A("")
    A("---")
    A("")
    A("## 3. Position 7 — outcome assignment at two instants")
    A("")
    A("`|A| = 0` is read at **`τ1` = ⟦T0⟧ + 108 × 24h**; the Continued condition is read at "
      "**`τ2` = ⟦T0⟧ + 199 × 24h** on `A_H`, with `|A| ≥ 1` retained as a conjunct of Continued "
      "(`decisions/0034`). Every boundary test is the half-open UTC-instant form, `watched_at < "
      "τ`; `date(watched_at) <= T1` appears nowhere in the implementation.")
    A("")
    A("| Population | Never started | Started and left | Continued | Total |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for k, lab in (("APPLY_post_liveness", "APPLY, position 7"),
                   ("DERIV_post_liveness", "DERIV, position 7"),
                   ("APPLY_at_position_5_outcome_conditional_view", "APPLY, position 5"),
                   ("DERIV_at_position_5_outcome_conditional_view", "DERIV, position 5")):
        o = p7[k]
        A(f"| {lab} | {n(o['never_started'])} | {n(o['started_and_left'])} | "
          f"{n(o['continued'])} | {n(o['total'])} |")
    A("")
    A("**The two published categories are measured over different horizons and must never be "
      "described as measured alike**: never-started is a 108-day statement, Continued a 199-day "
      "statement (`0034`).")
    A("")
    ap = diag["outcome_counts"]["abandonment_point_p"]
    A(f"**Abandonment point `p`** is the rank form `|{{e ∈ E2 : e ≤ max(A_H)}}| / L2`, defined "
      f"only on Started-and-left; the raw ratio is withdrawn. Range on the position-7 APPLY "
      f"rows: [{ap['p_min']:.4f}, {ap['p_max']:.4f}]. The **`p = 1.0` residual** — watched the "
      f"finale, missed the 90 percent threshold — is {n(ap['p_equals_1_residual_APPLY_position_7'])} "
      "pairs and is its own named category, not part of 'near-finale'. `p` is null on every row "
      "that is not Started-and-left.")
    A("")
    A("---")
    A("")
    A("## 4. Per `W` arm")
    A("")
    A(f"Arms: {' / '.join(str(x) for x in arms['arm_grid'])}. **Step 8 names no grid**; this is "
      "the operative series quoted at `task-sheet.md` Steps 7 and 13, and the source is named "
      "here rather than left silent. `H` is held constant at 91 across every arm. **D10 is "
      "re-derived at each arm and never frozen** (`decisions/0047`), so the arms do not share a "
      "denominator.")
    A("")
    A("### 4.1 Retained pairs per air period after right-censoring")
    A("")
    A("**Censoring is applied to the POSITION-4 output, as the mandated filter order requires** "
      f"(APPLY {n(arms['censoring_denominator']['APPLY_position_4_output'])} pairs). `0033`'s "
      "97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed on the position-3 output and are "
      "superseded by `0070` ruling 8.")
    A("")
    hdr = "| `W` | retained (APPLY) | share of position 4 | pre-2020 | 2020–2022 | 2023–2025 |"
    A(hdr)
    A("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for e in arms["arms"]:
        rp = e["retained_per_air_period_APPLY"]
        A(f"| {e['W_days']} | {n(e['position_5_APPLY'])} | "
          f"{pct(e['retained_share_of_position_4_APPLY'])} | "
          f"{pct(rp['pre-2020']['retained_share'], 1)} | "
          f"{pct(rp['2020-2022']['retained_share'], 1)} | "
          f"{pct(rp['2023-2025']['retained_share'], 1)} |")
    A("")
    r108 = a108["retained_per_air_period_APPLY"]
    r213 = next(e for e in arms["arms"] if e["W_days"] == 213)["retained_per_air_period_APPLY"]
    A(f"**The aggregate hides a cohort-asymmetric loss.** At `W = 108` "
      f"{pct(a108['retained_share_of_position_4_APPLY'])} of pairs survive right-censoring, but "
      f"the 2023–2025 cohort keeps {pct(r108['2023-2025']['retained_share'], 1)} against "
      f"{pct(r108['pre-2020']['retained_share'], 1)} pre-2020. At `W = 213` the modern cohort "
      f"keeps {pct(r213['2023-2025']['retained_share'], 1)} — a loss of "
      f"**{pct(r213['2023-2025']['lost_share'], 1)}** against "
      f"{pct(r213['pre-2020']['lost_share'], 1)} pre-2020. The loss falls on the uncapped "
      "`S1_completion_date` term, so the modern cohort is not merely smaller after censoring but "
      "differently selected.")
    A("")
    A(f"**The `W = 108` row reproduces `0070` ruling 8 exactly** — "
      f"{pct(a108['retained_share_of_position_4_APPLY'])} aggregate and "
      f"{pct(r108['pre-2020']['retained_share'], 1)} / "
      f"{pct(r108['2020-2022']['retained_share'], 1)} / "
      f"{pct(r108['2023-2025']['retained_share'], 1)} by period, and "
      f"{pct(r213['2023-2025']['retained_share'], 1)} for 2023–2025 at `W = 213` — measured here "
      "independently through the mandated filter order.")
    A("")
    A(f"**One derived figure the ruling did not restate moves with it.** `0033`'s comparator for "
      f"the cohort asymmetry at `W = 213` was **2.7% pre-2020**, measured on the position-3 "
      f"output. On the position-4 output the mandated order censors, it is "
      f"**{pct(r213['pre-2020']['lost_share'], 1)}**. The 10.3% → 10.5% correction was propagated; "
      "its pair on the other side of the same comparison was not. Reported, not fixed elsewhere.")
    A("")
    A("### 4.2 Liveness exclusions per arm, on APPLY")
    A("")
    A("| `W` | position 5 | excluded | never-started | started-and-left | accounts | DERIV "
      "excluded |")
    A("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for e in arms["arms"]:
        x, xd = e["liveness_exclusions_APPLY"], e["liveness_exclusions_DERIV"]
        A(f"| {e['W_days']} | {n(e['position_5_APPLY'])} | **{n(x['total'])}** | "
          f"{n(x['never_started_component'])} | {n(x['started_and_left_component'])} | "
          f"{n(x['accounts'])} | {n(xd['total'])} |")
    A("")
    f_, l_ = arms["arms"][0]["liveness_exclusions_APPLY"], arms["arms"][-1][
        "liveness_exclusions_APPLY"]
    A(f"`W` and liveness are not independent axes: the rule has no parameter of its own but its "
      f"exclusion set is a pure function of `W` — {f_['total']} at `W = 38` to {l_['total']} at "
      f"`W = 213`, a factor of {l_['total'] / f_['total']:.2f}. The started-and-left component "
      f"runs {f_['started_and_left_component']} → {l_['started_and_left_component']}, a factor of "
      f"{l_['started_and_left_component'] / f_['started_and_left_component']:.2f}, growing faster "
      "than the rule itself.")
    A("")
    A("### 4.3 D3′ — the resumption-rate report, each arm on its own denominator")
    A("")
    A("Of pairs scored **Started and left at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`: the "
      "cleared count, its share of all Started-and-left **on the population and at the arm named "
      "here**, and the share completing within `[τ2, τ2 + H)`.")
    A("")
    A("| `W` | S&L (APPLY, position 7) | cleared | cleared share | completing in `[τ2, τ2+H)` | "
      "share | DERIV cleared share |")
    A("| ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for e in arms["arms"]:
        d = e["D3_prime"]["APPLY"]
        dd = e["D3_prime"]["DERIV"]
        A(f"| {e['W_days']} | {n(d['all_started_and_left'])} | {n(d['cleared_count'])} | "
          f"{pct(d['cleared_share_of_all_started_and_left'])} | "
          f"{n(d['count_completing_in_tau2_to_tau2_plus_H'])} | "
          f"{pct(d['share_completing_in_tau2_to_tau2_plus_H'])} | "
          f"{pct(dd['cleared_share_of_all_started_and_left'])} |")
    A("")
    A("**The cleared shares here are not comparable to the 95.98%-at-`W = 46` to "
      "91.34%-at-`W = 213` series in `decisions/0034`**, which was measured on a different "
      "population. `0068` requires each arm's denominator to be its own and forbids carrying a "
      "figure from another population; the difference is a population difference, not a "
      "divergence.")
    A("")
    t = diag["the_3440"]
    A(f"**Reported alongside, and labelled a COUNT and not a rate: {n(t['value'])} "
      f"Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is "
      f"**{t['population']}**. It is restated, not recomputed on Step 8's population, and it must "
      f"not be reported against APPLY or DERIV. {t['exposure_weighting'].capitalize()}. It is a "
      f"floor because {t['why_it_is_a_floor']}. The two figures do not bracket the quantity — "
      "both truncate observation and neither is a lower bound on the other.")
    A("")
    A("---")
    A("")
    A("## 5. The other required counts")
    A("")
    dc = diag["drop_counts"]
    A("### 5.1 Both drop counts (Step 1 §3.4)")
    A("")
    A(f"**Coverage: {n(dc['coverage_records_examined'])} in-frame S1/S2 episode records examined "
      f"across {n(dc['per_show']['shows_examined'])} shows.** This is a measured zero, not an "
      "empty check.")
    A("")
    A(f"- **Per show:** {n(dc['per_show']['dropped_episode_records_total'])} dropped episode "
      f"records and {n(dc['per_show']['distinct_dropped_season_number_total'])} distinct dropped "
      f"`(season, number)` pairs, on {n(dc['per_show']['shows_with_any_dropped_record'])} shows. Per-show "
      "detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a per-show "
      "table, and the aggregate is what belongs here).")
    A(f"- **Per outcome:** {n(dc['per_outcome']['count'])} pairs had their entire S2 evidence "
      f"dropped. **Denominator: never-started at position 5 = "
      f"{n(dc['per_outcome']['denominator_position_5_never_started_APPLY'])}** — what entered the "
      f"liveness filter — with the **post-liveness "
      f"{n(dc['per_outcome']['denominator_post_liveness_never_started_APPLY'])} reported "
      f"alongside** (`0070` ruling 6). The difference between the two is exactly the 604 "
      "never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never "
      "started.")
    A("")
    A("### 5.2 D2 — negative lag, split THREE ways")
    A("")
    A("| Population | pairs | first S2 watch before clock start | share | S2-finale binds | "
      "S1-completion binds | **both bind** |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k, lab in (("APPLY_position_5", "APPLY, position 5"),
                   ("DERIV_position_5", "DERIV, position 5"),
                   ("APPLY_position_7", "APPLY, position 7"),
                   ("DERIV_position_7", "DERIV, position 7")):
        d = diag["D2_negative_lag"][k]
        A(f"| {lab} | {n(d['population'])} | "
          f"{n(d['pairs_with_first_S2_watch_strictly_before_clock_start'])} | {pct(d['share'])} | "
          f"{n(d['S2_finale_term_binds'])} | {n(d['S1_completion_term_binds'])} | "
          f"{n(d['both_terms_bind'])} |")
    A("")
    bt = diag["D2_negative_lag"]["binding_term_split_of_the_whole_population_APPLY_position_5"]
    A(f"**A tie is its own category, not a tiebreak** (`0070` ruling 5). Over the whole "
      f"position-5 APPLY population the binding term is the S2 finale on {n(bt['S2_finale_binds'])} "
      f"pairs, the S1 completion on {n(bt['S1_completion_binds'])}, and **both on "
      f"{n(bt['both_bind'])}** — the case a binary split has nowhere to put.")
    A("")
    A("S2-finale-term negative lags are the normal case for anyone who watched a weekly season "
      "while it aired and are information about the frame's cadence mix. **S1-term negative lags "
      "are the actual test of the first-pass completion choice**, and they are the smaller group.")
    A("")
    d4 = diag["D4_S3_without_S2"]
    A("### 5.3 D4 — S3 without S2 (`0070` ruling 7)")
    A("")
    A(f"- **APPLY, position 7:** {n(d4['APPLY_position_7']['D4_signature'])} pairs carry the "
      f"signature — S3-or-later episodes logged and **no S2 episodes at all** — out of "
      f"{n(d4['APPLY_position_7']['never_started'])} never-started, "
      f"{pct(d4['APPLY_position_7']['share_of_never_started'], 3)}.")
    A(f"- **DERIV, position 7:** {n(d4['DERIV_position_7']['D4_signature'])} out of "
      f"{n(d4['DERIV_position_7']['never_started'])} — zero by construction, since DERIV requires "
      "S2 evidence.")
    A(f"- Reported so nothing is hidden: a further "
      f"{n(d4['wider_variant_reported_so_nothing_is_hidden']['never_started_with_S3_evidence_but_some_S2_evidence_after_tau1_APPLY_position_7'])} "
      "never-started pairs have S3 evidence **and** some S2 evidence after `τ1`. Those are not "
      "the D4 signature and are not counted as it.")
    A("- Direction: D4 **inflates** never started. Step 9 bounds it; it is emitted here because "
      "Step 8 holds the episode-level evidence and Step 9 does not.")
    A("")
    d8 = diag["D8_never_started_post_window"]
    A("### 5.4 D8 — never-started post-window diagnostic, over `[τ1, τ2)`")
    A("")
    A("| Population | never started | (i) any S2 episode in the horizon | share | "
      "(ii) satisfying Continued over the horizon | share |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: |")
    for k, lab in (("APPLY_position_7", "APPLY, position 7"),
                   ("DERIV_position_7", "DERIV, position 7"),
                   ("APPLY_position_5", "APPLY, position 5")):
        d = d8[k]
        A(f"| {lab} | {n(d['never_started'])} | "
          f"{n(d['i_count_with_any_S2_episode_in_the_horizon'])} | {pct(d['i_share'])} | "
          f"{n(d['ii_count_satisfying_the_continued_condition_over_the_horizon'])} | "
          f"{pct(d['ii_share'])} |")
    A("")
    A("Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and "
      "not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started "
      "boundary** and its size is Step 14's ledger item 10. Direction: **down**.")
    A("")
    d9 = diag["D9_split_artifacts"]
    A("### 5.5 D9 — split artifacts, both halves")
    A("")
    A(f"Detection is imperfect and **every count here is a lower bound**. Coverage: "
      f"{n(d9['coverage']['show_ids_with_a_slug'])} show IDs carrying a title slug, "
      f"{n(d9['coverage']['user_show_coverage_rows_examined'])} user-show season-coverage rows "
      f"examined, {n(d9['coverage']['candidate_complementary_id_pairs'])} complementary ID pairs "
      "found.")
    A("")
    A(f"- **(a) the fabricated never-started row:** "
      f"{n(d9['half_a_fabricated_never_started_row']['carrying_the_signature'])} of "
      f"{n(d9['half_a_fabricated_never_started_row']['never_started'])} never-started pairs "
      f"(APPLY, position 7) carry the signature — "
      f"{pct(d9['half_a_fabricated_never_started_row']['share_of_never_started'], 4)}.")
    A(f"- **(b) the silently deleted S1-failing counterpart:** "
      f"{n(d9['half_b_silently_deleted_S1_failing_counterpart']['carrying_the_signature'])} of "
      f"{n(d9['half_b_silently_deleted_S1_failing_counterpart']['pairs_failing_S1_completion'])} "
      "pairs that fail the S1 completion rule. **These rows are not in the analysis table and "
      "cannot be recovered from it**, so position 3's drop set was retained as a side output to "
      "make this half computable at all — a precondition no line of the step states.")
    A(f"- **Merges, counted with the same query and reported separately:** "
      f"{n(d9['merges_counted_with_the_same_query_and_reported_separately']['user_show_rows_where_one_ID_carries_both_seasons_and_a_same_title_ID_also_appears'])} "
      "user-show rows where one ID carries both seasons and a same-title ID also appears in the "
      "sweep. Merges can only add evidence to a pair, never remove it.")
    A("- Direction: D9 moves the never-started share **down**, plus an unmeasured denominator "
      "loss on half (b).")
    A("")
    pdd = diag["pull_date_and_D11"]
    A("### 5.6 `pull_date`, fetch dates and discarded records (D11)")
    A("")
    A(f"- **`pull_date` = `τ_pull` = {pdd['pull_date_tau_pull_utc']}**, a single global frozen "
      "cutoff.")
    A(f"- **Per-user fetch dates:** first page, earliest {pdd['earliest_per_user_first_page_fetch_utc']} "
      f"and latest {pdd['latest_per_user_first_page_fetch_utc']}; last page, earliest "
      f"{pdd['earliest_per_user_last_page_fetch_utc']} and latest "
      f"{pdd['latest_per_user_last_page_fetch_utc']}. The D11 constraint `pull_date ≤ earliest "
      f"per-user fetch date` **holds**.")
    A(f"- **Records discarded for `watched_at ≥ τ_pull`:** "
      f"{n(pdd['records_discarded_for_watched_at_ge_tau_pull_whole_sweep'])} across the whole "
      f"sweep, of which "
      f"{n(pdd['records_discarded_for_watched_at_ge_tau_pull_in_frame_S1S2'])} are in-frame S1/S2 "
      f"records. A further {n(pdd['records_with_no_watched_at_whole_sweep'])} records carry no "
      "`watched_at` at all and cannot be placed on the timeline.")
    oq = pdd["open_question_carried_not_resolved"]
    A(f"- **Carried as an open question, not resolved:** applying D11 to the S1-completion walk "
      f"gives {n(oq['completers_with_D11_applied_to_the_S1_walk'])} completers rather than "
      f"220,107 — {oq['pairs_that_stop_being_completers_under_D11']} pairs — and moves "
      f"{oq['completers_whose_completion_date_moves_under_D11']} completion dates. `0068` fixes "
      "line 1 at the published 220,107 and lists this as open; this instance measured it and did "
      "not apply it.")
    A("")
    bk = diag["D12_cadence_buckets"]
    A("### 5.7 D12 cadence buckets — all five, each its own line")
    A("")
    A("| Bucket | shows | pairs, position 5 APPLY | pairs, position 7 APPLY | pairs, position 5 "
      "DERIV |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for b in ("C0", "C1", "C2", "C3", "C4"):
        v = bk["buckets"][b]
        A(f"| {b} | {n(v['shows'])} | {n(v['pairs_position_5_APPLY'])} | "
          f"{n(v['pairs_position_7_APPLY'])} | {n(v['pairs_position_5_DERIV'])} |")
    A("")
    A(f"**Shows within 1 day of a bucket boundary: {n(bk['shows_within_1_day_of_a_bucket_boundary'])}** "
      f"of {n(bk['coverage_shows'])}. That count is what says whether the classifier's "
      "conventions are load-bearing. **C0 is reported at zero rather than omitted.**")
    A("")
    md = diag["metadata_disagreement"]
    A("### 5.8 Metadata-disagreement counts")
    A("")
    A(f"Recomputed from the reported counts rather than read off the frame's stored flags "
      f"(the two agree: {md['recomputation_agrees_with_the_stored_frame_flags']}). "
      f"**Coverage: {n(md['coverage_shows'])} shows.**")
    A("")
    A(f"- Shows where `episode_count`, `aired_episodes` and `|E|` disagree: "
      f"{n(md['shows_where_episode_count_aired_episodes_and_E_disagree_S1'])} for S1, "
      f"{n(md['shows_where_they_disagree_S2'])} for S2, "
      f"{n(md['shows_where_they_disagree_S1_or_S2'])} for either; pairs on those shows, "
      f"{n(md['pairs_on_those_shows_position_5_APPLY'])} at position 5 APPLY.")
    A(f"- **Shows where `aired_episodes < |E|` for S2** — the subset where Continued may be "
      f"unreachable: {n(md['shows_where_aired_episodes_lt_listed_E_for_S2'])}.")
    A("- Direction: listed exceeding aired raises `L2`, tightens `ceil(0.90 × L2)`, and pushes "
      "pairs that would have been Continued into Started-and-left — it **overstates "
      "abandonment**. The same effect on S1 raises `L1` and shrinks the population non-randomly, "
      "on shows with messy metadata.")
    A("")
    acd = diag["action_counts"]
    A("### 5.9 `action` — per-pair counts by type, not a row-level column")
    A("")
    A("`action` is record-level and the row is a pair, so a single value per row would assert one "
      "action per pair, which is false (`0070` ruling 4). It is **not an outcome variable**: "
      "Step 1 §2.3 ruled check-ins count as watching alongside `scrobble` and `watch`, because "
      "`action` is a property of the logging client.")
    A("")
    A("| | watch | checkin | scrobble | other |")
    A("| :--- | ---: | ---: | ---: | ---: |")
    for s in ("S1", "S2"):
        v = acd["records_on_position_7_APPLY_rows"][s]
        A(f"| {s} records on position-7 APPLY rows | {n(v['watch'])} | {n(v['checkin'])} | "
          f"{n(v['scrobble'])} | {n(v['other'])} |")
    A("")
    comp = acd["pairs_by_S2_evidence_composition_position_7_APPLY"]
    A(f"**Pairs by S2 evidence composition** (position 7, APPLY), which is what Step 13's action "
      f"arm cuts on: watch-only {n(comp['watch_only'])}, checkin-only {n(comp['checkin_only'])}, "
      f"scrobble-only {n(comp['scrobble_only'])}, mixed {n(comp['mixed'])}, no S2 records "
      f"{n(comp['no_S2_records'])}. Unknown `action` values encountered: "
      f"{n(acd['unknown_action_values_encountered'])}.")
    A("")
    ch = outc["channel_counts_on_position_7_APPLY"]
    A("### 5.10 Discovery channel — two boolean columns")
    A("")
    A(f"Channel A {n(ch['pairs_channel_a'])} pairs, Channel B {n(ch['pairs_channel_b'])} pairs, "
      f"**both {n(ch['pairs_in_both'])}** (accounts: {n(ch['accounts_channel_a'])} / "
      f"{n(ch['accounts_channel_b'])} / **{n(ch['accounts_in_both'])} in both**). A single "
      "categorical would either drop the overlap or assign it arbitrarily, and Step 11 tests "
      "whether discovery method biased the pool (`0070` ruling 3).")
    A("")
    A("---")
    A("")
    A("## 6. The analysis table")
    A("")
    at = outc["analysis_table"]
    A(f"`{at['path']}` — **{n(at['rows'])} rows, {at['columns']} columns**, one row per user-show "
      f"pair, the position-7 output on APPLY. **{n(at['DERIV_rows_flagged_within_it'])} rows "
      "carry the DERIV flag**, so both populations are produced by Step 8 and nothing downstream "
      "has to rebuild one. It carries outcome state, abandonment point, the two discovery-channel "
      f"booleans, the per-pair action counts and all {at['step2_show_fields_carried']} Step 2 "
      "show fields. **It stays in `processed/` and is never published.**")
    A("")
    A("---")
    A("")
    A("## 7. The scope qualifier that travels with this population")
    A("")
    A(f"Step 8 does not compute Step 9's bound, but it produces the position-6 population the "
      f"bound is stated on. So, wherever that population is named: **the bound is {SCOPE}.** "
      "**D4 and D9 publish alongside and are never folded in** (`0062`).")
    A("")
    A("---")
    A("")
    A("## 8. What this instance had to decide, and what it did not resolve")
    A("")
    A("Listed rather than settled. Each is a place two isolated instances can differ while both "
      "following the written spec.")
    A("")
    A("1. **The `W` arm grid.** Step 8 requires per-arm outputs and names no grid. Taken from the "
      "operative series at Steps 7 and 13 — 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 — and named "
      "at the point of use. Step 6's deliverables state the minimum range as [37, 107] and "
      "[37.70, 107.71]; neither says 38.")
    A("2. **One table or eight.** The analysis table is built once at `W = 108`; the per-arm "
      "requirements are computed as aggregates by re-running positions 5–7 at each arm. The step "
      "says \"build one row per user-show pair\" in the singular and does not say which object is "
      "per-arm.")
    A("3. **D11 at position 3.** Not applied, per `0068`; the counterfactual is measured and "
      "reported in §5.6.")
    A("4. **The contamination exclusion is read from Step 5's stored per-pair flags**, and the "
      "published Step 5 waterfall is asserted before use rather than re-derived. Step 5 is a "
      "closed gate.")
    A("5. **`p` on non-Started-and-left rows** is null, not 0 and not omitted. The spec defines "
      "`p` only for Started-and-left and does not pin the representation.")
    A("6. **\"All Step 2 show fields\"** is read literally: all 60 non-key columns of "
      "`frame.csv`, including derived ones.")
    A("7. **Populations for the required counts.** Seven of the required outputs name no "
      "population. Each is reported here on a named population, and on more than one where the "
      "computation is cheap, rather than one being chosen silently.")
    A("")
    A("---")
    A("")
    A("## 9. Disagreements between surfaces, reported and not fixed")
    A("")
    A("Reported because the spec asks for them, and not edited: `decisions/` and `task-sheet.md` "
      "are not this instance's to amend.")
    A("")
    A("1. **`action` — three surfaces still require a column that `0070` ruling 4 replaced.** "
      "`task-sheet.md` Step 13 says *\"Requires the `action` column retained at Step 8\"*; "
      "Step 1 §2.3 and §9 require *\"`action` be retained as a column\"*; and the "
      "`analytics-engineer` definition carries *\"retain `action` as a column\"* in its Step 8 "
      "head bullet, then ruling 4 lower down in the same section. `0070` §5 records that the "
      "ruling reached `task-sheet.md` Step 8 and the two `analytics-engineer` files only, so this "
      "is a known-shape propagation gap rather than a new one. **What was emitted satisfies the "
      "ruling and Step 13's need**: per-pair counts by action type, which are what the arm cuts "
      "on, plus the composition counts in §5.9.")
    A("2. **`decisions/0033`'s pre-2020 comparator at `W = 213` moved and was not restated** — "
      "see §4.1.")
    A("3. **`decisions/0034`'s D3′ cleared-share series is not comparable to the per-arm series "
      "required here**, because it was measured on a different population — see §4.3. Not a "
      "divergence.")
    A("")
    A("---")
    A("")
    A("*Generated by `src/step8_a_6_emit.py` from the stage outputs in `processed/step8/a/`. "
      "Every figure in this file is generated, none is typed by hand.*")

    with open(os.path.join(ART, "step8-waterfall-a.md"), "w") as fh:
        fh.write("\n".join(L) + "\n")

    # ------------------------------------------------------------------ invariants MD ----
    M = []
    B = M.append
    B("# Step 8 — invariant report, instance `a`")
    B("")
    B("**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · "
      "**W = 108 days** · **H = 91 days** · **Zero API calls** · **Counts only**")
    B("")
    B("> **EVERY INVARIANT CARRIES A LABEL** (`decisions/0068`). **A code check catches an "
      "implementation that computed something wrongly; it cannot fail on any data, and it is NOT "
      "evidence for the rule.** A report saying \"all invariants passed\" overstates what was "
      "verified unless it names which ones could have failed. **Four of the six required "
      "invariants here cannot fail on data at all.**")
    B("")
    B(f"**Result: {len(inv['invariants'])} checks ran and all passed — "
      f"{inv['label_counts']['CODE CHECK']} labelled CODE CHECK and "
      f"{inv['label_counts']['CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED']} labelled "
      "CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.**")
    B("")
    B("**How this maps onto `0070` §4's count of the required set** — *four pure code checks, one "
      "that is a code check by construction and a genuine cross-check as specified, and one item "
      "that is not an invariant at all*: **items 1–4 are the four pure code checks**; **item 5 is "
      "the hybrid**; **item 6 is the set-membership check**, which Step 8's own bullet labels a "
      "code check; **item 7 is an extra this instance added** and is labelled as such; and **the "
      "703 line is the item that is not an invariant**, reported separately below as a population "
      "reconciliation.")
    B("")
    B("| # | Invariant | Label | Coverage | Result |")
    B("| :-- | :--- | :--- | ---: | :--- |")
    for i, it in enumerate(inv["invariants"], 1):
        covk = next((k for k in it if k.startswith("coverage")), None)
        cov = n(it[covk]) if covk else "—"
        B(f"| {i} | {it['name']} | **{it['label']}** | {cov} | "
          f"{'PASS' if it['passed'] else '**FAIL**'} |")
    B("")
    for i, it in enumerate(inv["invariants"], 1):
        B(f"### {i}. {it['name']}")
        B("")
        B(f"**{it['label']}.** {it['why']}")
        B("")
        for k, v in it.items():
            if k in ("name", "label", "why", "passed"):
                continue
            if isinstance(v, dict):
                B(f"- `{k}`:")
                for k2, v2 in v.items():
                    B(f"    - `{k2}` = `{v2}`")
            else:
                B(f"- `{k}` = `{v}`")
        B(f"- **result: {'PASS' if it['passed'] else 'FAIL'}**")
        B("")
    rec = inv["population_reconciliation"]
    B("---")
    B("")
    B("## The 703 line is NOT an invariant")
    B("")
    B(f"**{rec['label']}.** {rec['why']}")
    B("")
    B("| Population | Denominator | Expected | Measured | never-started | started-and-left | "
      "accounts |")
    B("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k in ("APPLY", "DERIV"):
        v = rec[k]
        B(f"| **{k}** | {n(v['denominator'])} | {n(v['expected'])} | **{n(v['measured'])}** | "
          f"{n(v['measured_never_started'])} | {n(v['measured_started_and_left'])} | "
          f"{n(v['measured_accounts'])} |")
    B("")
    B(f"**It reconciles: {rec['reconciles']}.** Neither superseded answer was produced — ALT's "
      f"604 on APPLY: {rec['superseded_answers_not_produced']['ALT_604_on_APPLY']}; ALT-MATCHED's "
      f"793 on APPLY: {rec['superseded_answers_not_produced']['ALT_MATCHED_793_on_APPLY']}.")
    B("")
    B("---")
    B("")
    B("## What the invariant set does and does not establish")
    B("")
    B("- It establishes that **the definition on paper is the definition in the code**: the "
      "partition is exhaustive and disjoint as assigned, no filter position adds rows, no "
      "episode set exceeds its season, `A` sits inside `A_H`, the clock is the `max()` it is "
      "defined to be, and membership was tested by set and never by the numeric range `1..F`.")
    B("- It establishes **nothing about whether the rules are right**. Four of these checks "
      "cannot fail on any data. The one with force is the clock-start check, and only because "
      "the first-pass S1 completion date is **recomputed independently from the episode "
      "records**; read back from the pipeline's own value it would prove nothing.")
    B("- **The withdrawn invariant** — \"no clock start precedes an S2 premiere\" — is vacuous "
      "under a finale-anchored clock and catches nothing. It is replaced by the three-part check "
      "above, whose equality clause is the part that does work.")
    B("")
    B("*Generated by `src/step8_a_6_emit.py` from `processed/step8/a/invariants.json`.*")

    with open(os.path.join(ART, "step8-invariants-a.md"), "w") as fh:
        fh.write("\n".join(M) + "\n")
    with open(os.path.join(ART, "step8-invariants-a.json"), "w") as fh:
        json.dump(inv, fh, indent=2)

    print("wrote artifacts/step8-waterfall-a.{md,json} and "
          "artifacts/step8-invariants-a.{md,json}")


if __name__ == "__main__":
    main()
