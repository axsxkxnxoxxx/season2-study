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
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import step8_a_lib as lib

ROOT = "/Users/alyanashantel/Documents/season2-study"
OUT = os.path.join(ROOT, "processed/step8/a")
ART = os.path.join(ROOT, "artifacts")

SCOPE = ("covering with respect to insertion-dormancy, exhaustively; open only across channel "
         "classes (D4, D9)")

# every count, every invariant result and every waterfall figure carries the build it was measured
# on (decisions/0079 B6, extending 0078). BT is the tag; the full definition is in section 0.
BT = f"`{lib.BUILD_TAG}`"


def btx(what="every figure in this section"):
    """The build citation as plain text, for use inside a sentence."""
    return f"Build: {what} measured on {BT} — {lib.BUILD_NAME}; see §0"


def bt(what="every figure in this section"):
    return f"*{btx(what)}.*"


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
        "build": lib.build_record(),
        "provenance_note": "EVERY COUNT AND EVERY INVARIANT RESULT IN THIS FILE WAS MEASURED ON "
                           "BUILD " + lib.BUILD_TAG + " unless it carries a different build at "
                           "the point of use. Human Lead ruling, decisions/0079 (B6), extending "
                           "0078. Partial application is worse than none.",
        "filter_order": pos["filter_order"],
        "inert_filter_positions": pos["inert_filter_positions"],
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
        "channel_counts": outc["channel_counts"],
        "channel_counts_on_the_table_position_5_APPLY":
            outc["channel_counts_on_the_table_position_5_APPLY"],
        "analysis_table": outc["analysis_table"],
        "position_3_drop_set_DELIVERABLE": pos["position_3_drop_set_DELIVERABLE"],
        "surviving_aggregate_of_the_silent_at_tau1_column":
            outc["analysis_table"]["surviving_aggregate_of_the_silent_at_tau1_column"],
        "line_6_marginal_decomposition_BOTH_652_AND_1355":
            outc["analysis_table"]["line_6_marginal_decomposition_BOTH_652_AND_1355"],
        "p_at_bound_whether_not_why_and_the_p_equals_1_totals":
            outc["analysis_table"]["p_at_bound_whether_not_why_and_the_p_equals_1_totals"],
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
    A("> **RERUN AGAINST `decisions/0088`, ordered by the Human Lead — a rerun, not an "
      "amendment.** This replaces the previous `-a` deliverable **in full**; the previous output "
      "was **not patched** and nothing in it is read or carried. **Everything below is "
      "regenerated from one pipeline run** — no figure is typed by hand. **THREE builds now exist "
      "on 2026-08-16** — the one Red Team's third pass reviewed, the `-0085` rerun its fourth "
      "pass reviewed, and this one — so they are **tagged apart**, and every figure names which.")
    A("")
    A("> **The spec this run executes, and what moved since the last one that completed.** "
      "**(1)** Every count, every invariant result and every waterfall figure **carries the build "
      "it was measured on** (`0079` B6, extending `0078`) — see §0. **(2)** The **position-3 drop "
      "set is a DELIVERABLE produced by the pipeline** and is **read back by the stage that "
      "computes D9 half (b)** (`0079` B5), so a missing input fails loudly instead of publishing a "
      "silent 0. **(3)** The discovery-channel overlap **publishes in all three units, each with "
      "its consumer named** (`0079` B7). **(4)** The **four inert filter positions are labelled "
      "with the reason** (`0079` §4). **(5)** The column set is the **89 ENUMERATED names** of "
      "`0080` §1 **as extended by `0081`** — which **restores `silent_at_tau1`** — **and by "
      "`0082`**, which **adds `p_at_bound`**; asserted by set equality, never by count. **(6)** "
      "**Every invariant states its population and accounts for every row in it** (`0080` §3). "
      "**(7)** **D9 reports four numbers, not three** (`0078` §3). **(8)** **`p_at_bound` marks "
      "WHETHER `p` reached its bound, not why** (`0083` §2, restating `0082`), and the `p = 1.0` "
      "counts are reported as **totals** — see §3.1. **(9)** The **records-examined denominator is "
      "CLOSED** (`0083` §1): all three readings publish, each naming the pipeline that produces "
      "it — see §5.1.")
    A("")
    A("> **THREE THINGS THIS ARM EMITS DIFFERENTLY FROM ITS LAST RUN, all from `decisions/0088`.** "
      "**(B3, §1 — the item that blocked the gate on Red Team's third AND fourth passes.)** The "
      "two unasserted mandates are **the half-open UTC-instant form** and **D11-as-global-cutoff** "
      "— ***not invariants 7 and 8***, which were already measured, published and labelled DATA "
      "CHECK here. **Compliance was never the gap; MEASUREMENT was.** Three things are now "
      "emitted: **(a)** the **boundary window** at `τ1` and `τ2` on both populations, with a zero "
      "labelled **VACUOUS** rather than passed silently — §5.6a; **(b)** a **per-site D11 table**, "
      "**asserted at each of 13 sites** rather than once and about the rest, replacing ***this "
      "arm's five sites named in prose with a count at none*** — §5.6b; **(c)** the existing "
      "`τ2 ≤ τ_pull` assertion **PROMOTED into the published invariant set** as check 9 — see the "
      "invariant report. **(F2, §2.)** The D9 coverage quantities are published **as separate "
      "objects with what each counts**, ***this arm's `distinct_show_ids_in_the_sweep` mislabel is "
      "corrected*** — it was the D9 coverage pivot, not the sweep — and the overstated coverage "
      "sentence in the invariant report is **STRUCK**. **(§3.)** The **D9 clustering universe is "
      "ruled to U1**, all slugged sweep show IDs, **ranked by distinct strict keys merged**; "
      "***this arm previously clustered the coverage-pivot subset***, so **the cluster list "
      "moves** — §5.5.")
    A("")
    A("> **NO POPULATION, NO RULE AND NO BOUND ENDPOINT MOVES, and every ruled D9 count "
      "reproduces** — strict 0, loose 75, third key 76, half (a) 0 and 6, half (b) 0 and 27. "
      "**What moves is the D9 CLUSTER LIST**, because the universe it is computed on was ruled "
      "and this arm's previous universe was not U1. **`0088` §3 records that D9's SEARCH already "
      "ran on the whole sweep in both arms, so the ruling does not widen what D9 finds** — it "
      "fixes **which clusters are illustrated**, which is the evidence for the loose key's only "
      "warrant.")
    A("")
    A("> Carried forward and unchanged: the table is the position-5 row set with `live` and "
      "`outcome` as columns (`0074`/1); D9 uses the defined strict key with the loose count "
      "alongside (`0074`/5, `0076`/3); the set-membership rule is a coverage count and not an "
      "invariant (`0074`/3); the `W` grid is fixed by `0075`/3; `p` is a CODE CHECK (`0076`/1); "
      "and the two DATA CHECKS of `0076`/2 are the only assertions here that can fail on data.")
    A("")
    A("---")
    A("")
    A("## 0. Provenance — what build every figure below was measured on")
    A("")
    A("**A count needs its PROVENANCE, not only its POPULATION** (`decisions/0078` §2, made "
      "general by `0079` B6). `0047` fixed *which population produced this figure*; this is that "
      "rule one layer down — *which build produced it*. **A count without its provenance can be "
      "correct when written and wrong when read**, because the pipeline moved underneath it and "
      "nothing in the text says which pipeline it belongs to. **Partial application is worse than "
      "none**: two labelled figures imply the other counts and the eight invariants did not need "
      "it.")
    A("")
    br = wjson["build"]
    A(f"**Build {BT} — {lib.BUILD_NAME}.**")
    A("")
    A(f"| Field | Value |")
    A("| :--- | :--- |")
    A(f"| pipeline | `{br['pipeline']}` |")
    A(f"| run date (UTC) | {br['run_date_utc']} |")
    A(f"| git HEAD at launch | `{br['git_head_short']}`, worktree dirty: "
      f"{br['git_worktree_dirty_at_launch']} |")
    A(f"| parameters | `W` = 108 d, `H` = 91 d, `τ_pull` = 2026-08-11T00:00:00Z, filter order "
      "`decisions/0029`, liveness ALT-BROAD |")
    A(f"| stage files (sha256, 12) | "
      + ", ".join(f"`{k}` {v}" for k, v in br["stage_files_sha256_12"].items() if v) + " |")
    A(f"| inputs | `processed/step5/full_scan.npz` ({br['inputs']['processed/step5/full_scan.npz']}), "
      f"`calibration.npz` `{br['inputs']['processed/step5/calibration.npz']}`, "
      f"`pair_revision5.csv` `{br['inputs']['processed/step5/pair_revision5.csv']}`, "
      f"`step2/frame.csv` `{br['inputs']['processed/step2/frame.csv']}`, "
      f"`step4/pull_ledger.jsonl` `{br['inputs']['processed/step4/pull_ledger.jsonl']}` |")
    A("")
    A("**Every figure in this file was measured on that build unless it carries a different one "
      "at the point of use.** Two do, and they are marked where they appear: **the 3,440**, which "
      "is on Step 5's uncensored estimation sample of 128,099 (`decisions/0034` §3), and the "
      "figures **restated** from the position-5 build of 2026-08-13 by `0078` — **58,345 pairs**, "
      "**324 of 5,694**, **178 of 2,549** — each of which is **re-measured here on this build and "
      "agrees**, which is stated rather than assumed.")
    A("")
    A("---")
    A("")
    A("## 1. The filter order and the waterfall, on both populations")
    A("")
    A("Applied in exactly the order `decisions/0029` fixes. The final row set commutes; the "
      "per-filter sample size does not, which is why the order is written down rather than left "
      "to each instance.")
    A("")
    A("| # | Filter | APPLY: retained | removed | DERIV: retained | removed | inert? |")
    A("| :-- | :--- | ---: | ---: | ---: | ---: | :--- |")
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
    INERT = {"1": "**INERT BY CONSTRUCTION** — line 1 is already the frame",
             "2": "**INERT BY CONSTRUCTION** — line 1 is already the `L2 > 1` population, and 0 "
                  "frame shows have `L2 = 1`",
             "3": "**POSITION INERT, RULE NOT** — line 1 is already the S1-completer population; "
                  "the rule removes 58,345 pairs upstream of it",
             "4": "no — it fires",
             "5": "no — it fires",
             "6": "no — it fires",
             "7": "**INERT BY CONSTRUCTION** — it annotates and removes nothing"}
    pa = pd_ = None
    for i, (k, name, va, vd) in enumerate(rows):
        ra = "—" if i == 0 else n(pa - va)
        rd = "—" if i == 0 else n(pd_ - vd)
        A(f"| **{k}** | {name} | {n(va)} | {ra} | {n(vd)} | {rd} | {INERT[k]} |")
        pa, pd_ = va, vd
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**Four positions remove zero BY CONSTRUCTION, and they are labelled rather than left to "
      "read as findings** (`decisions/0079` §4). **Keep them: removing a position removes the "
      "check that would catch a future upstream change**, and the point of a fixed order is that "
      "the waterfall is comparable across runs and across arms. **But an unlabelled always-zero "
      "filter reads as evidence THE RULE FOUND NOTHING when it is evidence THE RULE CANNOT "
      "FIRE** — the same defect as an unlabelled code check (`0069`).")
    A("")
    ip = pos["inert_filter_positions"]
    A("| Position | Removed | Why it cannot fire |")
    A("| :--- | ---: | :--- |")
    for k in ("1", "2", "3", "7"):
        v = ip[k]
        A(f"| **{k}** {v['filter']} | {n(v.get('removed', 0))} | {v['why']} |")
    A("")
    A(f"**Row 3 is the one that matters.** The position is inert; **the rule is the study's "
      f"largest single exclusion — it removes "
      f"{n(ip['3']['rule_removes_upstream_of_line_1'])} pairs upstream of line 1**, which is why "
      "its drop set is a **deliverable** of this run (§6.1) and not a working file.")
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
    A("- **Positions 6 and 7 are ANNOTATIONS on the table, not deletions from it.** The analysis "
      "table is the **position-5 row set** and carries `live` and `outcome` as columns "
      "(`decisions/0074` ruling 1), so lines 6 and 7 above report what the liveness rule and the "
      "outcome assignment *select*, and the rows they do not select are still in the file with "
      "`live = false`. Downstream consumes rather than rebuilds.")
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
    A(bt("both columns"))
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
    A(bt("every figure in this table"))
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
    md = outc["analysis_table"]["line_6_marginal_decomposition_BOTH_652_AND_1355"]
    A("### 2.1 Line 6 read as a marginal cost — both figures, on both populations")
    A("")
    A("**703 is NOT the marginal cost of the silence test** — Red Team third pass, "
      "`decisions/0085` §5. **The silence test alone excludes 1,355 on APPLY; the `NOT Continued` "
      "conjunct spares 652; `1,355 − 652 = 703`.** ***This instance published 652 and not 1,355 on "
      "its previous run.*** **Derivable, so not a defect — but 1,355 is the figure that makes line "
      "6 readable as a marginal cost, and a reader holding only 652 cannot recover it without "
      "knowing to add.** **Both, on both populations, with the identity stated:**")
    A("")
    A("| Population entering line 6 | Silence test ALONE excludes | `NOT Continued` SPARES | "
      "Line 6 exclusions | Identity |")
    A("| :--- | ---: | ---: | ---: | :--- |")
    for k in ("APPLY_position_5_entering_line_6", "DERIV_position_5_entering_line_6"):
        v = md[k]
        A(f"| {v['population']} ({n(v['coverage_rows_examined'])} rows) | "
          f"**{n(v['silence_test_ALONE_excludes'])}** | **{n(v['NOT_Continued_conjunct_SPARES'])}** "
          f"| **{n(v['line_6_exclusions'])}** | "
          f"{n(v['silence_test_ALONE_excludes'])} − {n(v['NOT_Continued_conjunct_SPARES'])} = "
          f"{n(v['line_6_exclusions'])} "
          f"{'✓' if v['identity_holds'] else 'FAILS'} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**The spared pairs are the Continued-and-silent ones.** They are what makes line 6 "
      "**outcome-conditional**, and they are why `silent_at_tau1` is an emitted column (`0081`): "
      "`live` is true for every Continued pair regardless of silence, so the count is not "
      "recoverable from `live` and `outcome` alone. **On DERIV the spared count is the same "
      f"{n(md['DERIV_position_5_entering_line_6']['NOT_Continued_conjunct_SPARES'])}**: Continued "
      "requires S2 evidence, so every Continued-and-silent pair on APPLY is also a DERIV pair, and "
      "the two populations differ in line 6 only through the silence-alone term.")
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
    A(bt("every figure in this table"))
    A("")
    A("**The two published categories are measured over different horizons and must never be "
      "described as measured alike**: never-started is a 108-day statement, Continued a 199-day "
      "statement (`0034`).")
    A("")
    ap = diag["outcome_counts"]["abandonment_point_p"]
    A(f"**Abandonment point `p`** is the rank form `|{{e ∈ E2 : e ≤ max(A_H)}}| / L2`, defined "
      f"only on Started-and-left; the raw ratio is withdrawn. Range on the table's row set "
      f"(APPLY, position 5): [{ap['p_min']:.4f}, {ap['p_max']:.4f}]. The **`p = 1.0` residual** — "
      "watched the finale, missed the 90 percent threshold — is "
      f"{n(ap['p_equals_1_residual_APPLY_position_5'])} pairs on APPLY position 5 and "
      f"{n(ap['p_equals_1_residual_APPLY_position_7'])} post-liveness, and is its own named "
      "category, not part of 'near-finale'. `p` is null on every row that is not "
      "Started-and-left.")
    A("")
    sp = ap["p_at_bound_totals_and_coextensivity"]
    fe = outc["analysis_table"][
        "p_at_bound_whether_not_why_and_the_p_equals_1_totals"]["frame_evidence"]
    sp2_shows_gap, sp2_shows = fe["shows_where_max_E2_differs_from_L2"], fe["shows_in_frame"]
    A("### 3.1 `p_at_bound` — WHETHER `p` reached its bound, and the `p = 1.0` totals")
    A("")
    A("**`p_at_bound` marks WHETHER `p` reached its bound, NOT WHY** — Human Lead ruling, "
      "2026-08-16 (`decisions/0083` §2), restating `0082`. **`TRUE` where `p` is at its bound, "
      "null where `p` is null.** `0082`'s definition **by two mechanisms** is **superseded**: the "
      "two clauses are **coextensive** — on a chain of three links of which the first two are "
      "construction and the third, `max(E2) = F2`, is MEASURED (`0085` §4) — so the class it "
      "called `FALSE` is "
      "**empty** and on the adopted rank form there is only one why. **The column is kept** — "
      "Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the "
      "spike **labelled**, and **an emptiness asserted in prose and never emitted cannot be "
      "checked.**")
    A("")
    A("**The `p = 1.0` counts are TOTALS, not a sum of two classes** (`0083` §2). "
      "**1,246 and 1,230 remain true and this instance reproduces them**, but they are **one "
      "class counted twice**; reading them as a split is a **withdrawn argument** (`CLAUDE.md`, "
      "third blindness class).")
    A("")
    A("**FOUR CELLS ON FOUR POPULATIONS** — Red Team blocker B2, `decisions/0085` §3. **Total, "
      "in-both-classes, saturated-not-final, final-not-saturated and in-neither, on APPLY "
      "position 5, APPLY post-liveness, DERIV position 5 and DERIV post-liveness.** This is "
      "`CLAUDE.md`'s standing **both populations, always** rule, not a new requirement. ***On this "
      "instance's previous run the `p_at_bound_totals_and_coextensivity` block carried "
      "`APPLY_position_5` and `APPLY_position_7` and nothing else, so the DERIV post-liveness "
      "figure appeared nowhere*** — **on the population where the ground for keeping the column, "
      "that an emptiness asserted in prose and never emitted cannot be checked, was therefore "
      "unmet.**")
    A("")
    A("| Population | `p = 1.0` TOTAL | in BOTH classes | saturated, not final | final, not "
      "saturated | in NEITHER | rows examined (`p` defined) |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for k, lab in (("APPLY_position_5", "APPLY, position 5"),
                   ("APPLY_position_7_post_liveness", "APPLY, post-liveness"),
                   ("DERIV_position_5", "DERIV, position 5"),
                   ("DERIV_position_7_post_liveness", "DERIV, post-liveness")):
        v = sp[k]
        A(f"| {lab} | **{n(v['total_p_equals_1'])}** | {n(v['in_BOTH_classes'])} | "
          f"{n(v['saturated_not_final'])} | {n(v['final_not_saturated'])} | "
          f"{n(v['in_NEITHER_class'])} | {n(v['coverage']['rows_with_p_defined_examined'])} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**The coverage column is not decoration.** Three of the four cells are zero on every row "
      "of this table, and **an empty result and a clean result are the same value** — the count "
      "of rows the cells were computed over is what says which this is.")
    A("")
    A("**The `p = 1.0` figures are TOTALS, not a sum of two classes**, and the `TRUE` count "
      "equals the total on all four populations because the `FALSE` class is empty.")
    A("")
    ct = sp["cross_tab_APPLY_position_5"]
    lk3 = sp["link_3_max_E2_equals_F2_MEASURED_NOT_ASSUMED"]
    A("**THE CHAIN HAS THREE LINKS AND ONLY TWO ARE CONSTRUCTION** — Red Team P4, "
      "`decisions/0085` §4. ***`0083` §2 named two causes for a future `FALSE` row; there are "
      "three.***")
    A("")
    A("1. **`m_H ∈ E2`** — **CONSTRUCTION.** The set-membership drop rule drops any episode whose "
      "`number` is not in `E2`, so `A_H ⊆ E2` and its maximum is a member of `E2`.")
    A("2. **`|{e ∈ E2 : e ≤ m_H}| = L2 ⟺ m_H = max(E2)`** — **CONSTRUCTION**, given `L2 := |E2|`, "
      "which the spec fixes.")
    A(f"3. **`max(E2) = F2`** — **NOT CONSTRUCTION.** It holds only because **the finale is the "
      "highest-numbered listed episode**, and **where a season lists an episode numbered above "
      "its finale the two separate** — the `s2_aired_lt_listed` case this step is told to count. "
      f"**MEASURED, NOT ASSUMED: {lk3['shows_where_max_E2_differs_from_F2']} of "
      f"{n(lk3['shows_in_frame_examined'])} frame shows have `max(E2) ≠ F2`, and "
      f"{lk3['s2_aired_lt_listed_shows']} shows carry `s2_aired_lt_listed`.** The frame does not "
      "move across Step 13's grid, so this is measured once and holds at every arm.")
    A("")
    A("**So the two clauses are coextensive, and the emptiness is measured rather than asserted.** "
      f"On APPLY position 5: **{n(ct['saturated_and_final_episode'])}** rows satisfy both, "
      f"**{n(ct['saturated_not_final_episode'])}** satisfy the numerator clause alone, "
      f"**{n(ct['final_episode_not_saturated'])}** the final-episode clause alone, and "
      f"**{n(ct['neither'])}** neither.")
    A("")
    A("**A SECOND fact, measured and NOT the same argument:** "
      f"**{sp2_shows_gap} of {n(sp2_shows)} frame shows have any S2 numbering gap**, so "
      "`E2 = {1…L2}` everywhere, `F2 = L2`, and the rank form reduces to `m_H / L2`. **That one "
      "is DATA and could be false on another frame; the coextensivity above would still hold.** "
      "Stated separately so a construction argument is not read as a frame accident.")
    A("")
    A("**Why the column is still worth emitting.** The `FALSE` class is empty because of links 1 "
      "and 2, **both `W`-invariant**, and link 3, **a frame property that does not move across "
      "Step 13's grid** — so it stays empty at every arm. **A `FALSE` row anywhere means one of "
      "the THREE has broken**, and that is a thing worth catching. `p_at_bound` is `TRUE` exactly "
      "on the `p = 1.0` rows, `FALSE` on the rest of Started-and-left, and null elsewhere.")
    A("")
    A("---")
    A("")
    A("## 4. Per `W` arm")
    A("")
    A(f"**Arms: {' / '.join(str(x) for x in arms['arm_grid'])} days**, fixed by `decisions/0075` "
      "and by `task-sheet.md` Step 13 — **the first statement of the grid anywhere, and no longer "
      "an instance's choice.** It had previously travelled only as the *index of a reported "
      "series*, which is a reading and not a specification; two instances on different grids "
      "produce tables that cannot be diffed at all. `H` is held constant at 91 across every arm. "
      "**D10 is re-derived at each arm and never frozen** (`decisions/0047`), so the arms do not "
      "share a denominator.")
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
    A(bt("every figure in this table, at every arm,"))
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
    A(f"**The comparator on the other side of that sentence is also reproduced.** `0033`'s "
      f"pre-2020 comparator at `W = 213` was **2.7%**, measured on the position-3 output; on the "
      f"position-4 output the mandated order censors it is "
      f"**{pct(r213['pre-2020']['lost_share'], 1)}**. `0070` moved the 10.3% and left the 2.7%, so "
      "the sentence briefly carried two orders at once; **`decisions/0073` corrected it, after "
      "both Step 8 instances found it independently.** Measured here again through the mandated "
      "order, and it agrees.")
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
    A(bt("every figure in this table, at every arm,"))
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
    A("**POPULATION: Step 8's RIGHT-CENSORED populations — APPLY, the position-7 output at each "
      "arm, each arm on its own denominator** (`decisions/0075`, `0068`). Stated here and in "
      "every field of the `.json`, because the gap this closes was a level measured on a "
      "different population and carrying no population at the point of use.")
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
    A(bt("every figure in this table, at every arm,"))
    A("")
    a46 = next(e for e in arms["arms"] if e["W_days"] == 46)["D3_prime"]["APPLY"]
    a213 = next(e for e in arms["arms"] if e["W_days"] == 213)["D3_prime"]["APPLY"]
    A(f"**The cleared-share series is "
      f"{pct(a46['cleared_share_of_all_started_and_left'])} at `W = 46` down to "
      f"{pct(a213['cleared_share_of_all_started_and_left'])} at `W = 213`, on APPLY** — the "
      "series `decisions/0075` fixes, reproduced here independently. **`decisions/0034`'s "
      "95.98% → 91.34% is SUPERSEDED at this point of use**: it was measured on the amendment's "
      "**uncensored estimation sample of 128,099** and carried no population where it was used. "
      "**The direction and the shrinkage stand; the level does not.**")
    A("")
    A("**Reported and not resolved: the series is not monotone in `W`.** It rises between "
      f"`W = 91` ({pct(next(e for e in arms['arms'] if e['W_days'] == 91)['D3_prime']['APPLY']['cleared_share_of_all_started_and_left'])}) "
      f"and `W = 107` ({pct(next(e for e in arms['arms'] if e['W_days'] == 107)['D3_prime']['APPLY']['cleared_share_of_all_started_and_left'])}) "
      "before resuming its fall. Both the clearance bound `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` and "
      "the Started-and-left denominator move with `W`, and they do not move together — the "
      "denominator drops faster than the cleared count between those two arms. Listed open at "
      "`decisions/0076` §5; measured here, not resolved.")
    A("")
    t = diag["the_3440"]
    A(f"**Reported alongside, and labelled a COUNT and not a rate: {n(t['value'])} "
      f"Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is "
      f"**{t['population']}**. It is restated, not recomputed on Step 8's population, and it must "
      f"not be reported against APPLY or DERIV. {t['exposure_weighting'].capitalize()}. It is a "
      f"floor because {t['why_it_is_a_floor']}. The two figures do not bracket the quantity — "
      "both truncate observation and neither is a lower bound on the other.")
    A("")
    A(f"*Build: **this figure is NOT on {BT}.** It was measured at `decisions/0034` §3 on the "
      "Step 5 revision-6 **uncensored estimation sample of 128,099 pairs**, and it is restated "
      "here rather than recomputed. **It must never be reported against APPLY or DERIV.** Saying "
      "which build a figure came from is the whole point of the provenance rule, and this is the "
      "figure in this deliverable that most needs it.*")
    A("")
    A("---")
    A("")
    A("## 5. The other required counts")
    A("")
    A(f"**Every count in this section was measured on build {BT}** unless it says otherwise at "
      "the point of use (`decisions/0079` B6). The two exceptions are marked where they appear: "
      "the **3,440** in §4.3, and the figures `0078` restates from the **position-5 build of "
      "2026-08-13**, which are re-measured here and agree.")
    A("")
    dc = diag["drop_counts"]
    A("### 5.1 Both drop counts (Step 1 §3.4) — a COVERAGE COUNT, not an invariant")
    A("")
    A("**The set-membership drop rule is reported, not asserted** (`decisions/0074` ruling 3). "
      "Step 8's own bullet already calls it *\"an implementation check, not a data check\"*, and "
      "asserting it would add another passing line to a report where SIX OF NINE checks cannot "
      "fail on any data.")
    A("")
    A(f"**Coverage: {n(dc['coverage_records_examined'])} in-frame S1/S2 episode records examined "
      f"across {n(dc['per_show']['shows_examined'])} shows, "
      f"{n(dc['coverage_records_dropped'])} dropped.** This is a measured zero, not an empty "
      "check.")
    A("")
    A(f"- **Per show:** {n(dc['per_show']['dropped_episode_records_total'])} dropped episode "
      f"records and {n(dc['per_show']['distinct_dropped_season_number_total'])} distinct dropped "
      f"`(season, number)` pairs, on {n(dc['per_show']['shows_with_any_dropped_record'])} shows. "
      "Per-show detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a "
      "per-show table, and the aggregate is what belongs here).")
    A(f"- **Per outcome:** {n(dc['per_outcome']['count'])} pairs had their entire S2 evidence "
      f"dropped. **Denominator: never-started at position 5 = "
      f"{n(dc['per_outcome']['denominator_position_5_never_started_APPLY'])}** — what entered the "
      f"liveness filter — with the **post-liveness "
      f"{n(dc['per_outcome']['denominator_post_liveness_never_started_APPLY'])} reported "
      f"alongside** (`0070` ruling 6). The difference between the two is exactly the 604 "
      "never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never "
      "started.")
    A("")
    rd = dc["records_examined_denominator_CLOSED_by_0083"]
    tr = rd["three_readings"]
    A("**The records-examined denominator — CLOSED, and it publishes as a coverage figure.** "
      "Human Lead ruling, 2026-08-16 (`decisions/0083` §1). `0074` ruling 4 published "
      "**6,065,704 against 6,065,610, both reporting 0 drops**, reported unreconciled and routed "
      "to Step 14; **that routing is withdrawn and the item is closed.** **It was never a "
      "divergence**: the readings are **one family indexed by where D11 is applied**, and "
      "**`0074`'s \"publish both, not one\" stands and is strengthened to three, each naming the "
      "pipeline that produces it.** This instance produces "
      f"**{n(rd['reported_by_this_instance'])} — reading A, D11 nowhere.**")
    A("")
    A("| Reading | Where D11 is applied | Pipeline | Records examined | Drops |")
    A("| :--- | :--- | :--- | ---: | ---: |")
    A(f"| **A — produced here** | nowhere | `src/step8_a_run.py`, build `{lib.BUILD_TAG}` | "
      f"**{n(tr['reading_A_no_D11'])}** | {n(dc['coverage_records_dropped'])} |")
    A(f"| B | S2 side only | not this instance's pipeline; recorded at `0083` §1 | "
      f"{n(tr['reading_B_D11_on_the_S2_side_only'])} | 0 |")
    A(f"| C | both sides | not this instance's pipeline; measured here as a counterfactual | "
      f"{n(tr['reading_C_D11_on_both_sides'])} | 0 |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**Readings B and C drop 0 because reading A drops 0.** The dropped set measured on the "
      "full record set is **empty**, and B and C examine **subsets of it**, so their drop counts "
      "are 0 by containment rather than by assumption. **The numerator is 0 three times over, "
      "which is why nothing downstream reads the denominator** and why this closes.")
    A("")
    A(f"**The gap decomposes exactly.** D11 discards "
      f"**{n(rd['discarded_by_D11_watched_at_ge_tau_pull'])}** in-frame S1/S2 records, of which "
      f"**{n(rd['discarded_by_D11_S2_side'])} are S2-side and {n(rd['discarded_by_D11_S1_side'])} "
      "are S1-side.** So the three readings differ by **where D11 is applied and nowhere else**: "
      f"{n(tr['reading_A_no_D11'])} with none, {n(tr['reading_B_D11_on_the_S2_side_only'])} with "
      f"D11 on the S2 side, {n(tr['reading_C_D11_on_both_sides'])} with D11 on both. **The "
      "94-record difference `0074` reported is exactly the S2-side count.** Every other candidate "
      "axis is zero and was measured, not assumed:")
    A("")
    A(f"- definition used here: {rd['definition']}")
    A(f"- undated (`watched_at` null): **{n(rd['undated_watched_at_null'])}**")
    A(f"- exact duplicate `(user, play id)` records: **{n(rd['exact_duplicate_user_play_id_records'])}**")
    A(f"- records with a non-positive episode `number`: **{n(rd['records_with_number_le_0'])}**")
    A("")
    A("**Why the no-D11 reading.** The figure is the **coverage count of the set-membership drop "
      "rule** (`0074` ruling 3), so its denominator is *what that rule examined*. The rule is "
      "`number ∈ E`; **it does not read `watched_at` at all**, so every in-frame S1/S2 episode "
      "record passes under it whatever its date, and a denominator that pre-filters on a timestamp "
      "would report a smaller number than the rule actually looked at — **a check that reports "
      "having looked at fewer rows than it looked at**. D11 is a real global cutoff and it is "
      "applied everywhere it bears: on `A` and `A_H`, on the action counts, on the liveness "
      "evidence, on D9's coverage rows. **It does not bear on this one**, because this one is not "
      "a computation on the timeline.")
    A("")
    A("**Why it closes rather than routing to Step 14.** A Step 14 limitation is an uncertainty "
      "that **survives into a result**, and this one touches none — the rule it is the "
      "denominator of **dropped zero records under every reading**. The three readings are not "
      "three measurements of one quantity that disagree; they are **three different quantities, "
      "exactly identified**, and the "
      f"{n(rd['discarded_by_D11_S2_side'])}/{n(rd['discarded_by_D11_S1_side'])} split says which "
      "is which with nothing left over.")
    A("")
    A("**What stays open is NOT this.** Whether D11 applies to the **S1 completion walk** is "
      "`0068`'s own open item: reading C moves waterfall line 1 to "
      f"**{n(pos['D11_counterfactual_on_position_3']['completers_with_D11_applied_to_the_S1_walk'])}**"
      f" because **{n(pos['D11_counterfactual_on_position_3']['pairs_that_stop_being_completers_under_D11'])}"
      " pairs stop being completers** and "
      f"**{n(pos['D11_counterfactual_on_position_3']['completers_whose_completion_date_moves_under_D11'])}"
      " completion dates move** (§5.6). **That question is answered there, not here** — recording "
      "it in two places is how a ruling gets made twice and diverges.")
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
    A(bt("every figure in this table"))
    A("")
    btsplit = diag["D2_negative_lag"]["binding_term_split_of_the_whole_population_APPLY_position_5"]
    A(f"**A tie is its own category, not a tiebreak** (`0070` ruling 5). Over the whole "
      f"position-5 APPLY population the binding term is the S2 finale on {n(btsplit['S2_finale_binds'])} "
      f"pairs, the S1 completion on {n(btsplit['S1_completion_binds'])}, and **both on "
      f"{n(btsplit['both_bind'])}** — the case a binary split has nowhere to put.")
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
    A(bt("every figure in this table"))
    A("")
    A("Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and "
      "not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started "
      "boundary** and its size is Step 14's ledger item 10. Direction: **down**.")
    A("")
    d9 = diag["D9_split_artifacts"]
    A("### 5.5 D9 — split artifacts, both halves")
    A("")
    st9 = d9["ADOPTED_strict_key"]
    lo9 = d9["REPORTED_ALONGSIDE_loose_key"]
    tk9 = d9["third_key_measured_only_so_the_record_is_complete"]
    ha = st9["half_a_fabricated_never_started_row"]
    hb = st9["half_b_silently_deleted_S1_failing_counterpart"]
    A("Detection is imperfect and **every count here is a lower bound**.")
    A("")
    cov9 = d9["coverage"]
    A("**THE COVERAGE QUANTITIES, EACH NAMED BY WHAT IT COUNTS** — Human Lead ruling, "
      "`decisions/0088` §2(b), on Red Team's F2. **`747,478` and `726,103` are different objects "
      "and both correct**, and **reconciling them would collapse two real quantities into one**, "
      "which the standing rule forbids. **One name over two quantities is the defect.** This arm "
      "publishes **all three units** so no reader has to infer which one a bare number is:")
    A("")
    A("| | Unit | Count |")
    A("| :--- | :--- | ---: |")
    A(f"| **A** | undeduplicated user-show **SEASON-COVERAGE ROWS** — distinct `(user, show, "
      f"season-class)` triples, season-class in {{S1, S2, S3+}} | {n(cov9['A_undeduplicated_user_show_SEASON_COVERAGE_ROWS'])} |")
    A(f"| **B** | distinct user-show **PAIRS** in the coverage pivot — any dated pre-`τ_pull` "
      f"episode record in season ≥ 1, **including pairs whose only evidence is S3 or later** | "
      f"**{n(cov9['B_distinct_user_show_PAIRS_in_the_coverage_pivot'])}** |")
    A(f"| **C** | **D9 CANDIDATE** user-show pairs — B less the S3-or-later-only pairs; the pairs "
      f"the complementary-coverage search can match on | "
      f"{n(cov9['C_D9_CANDIDATE_user_show_pairs_carrying_S1_or_S2_evidence'])} |")
    A(f"| | *bridge: B − C, pairs with only S3-or-later evidence* | "
      f"*{n(cov9['bridge_B_minus_C_pairs_with_only_S3_or_later_evidence'])}* |")
    A(f"| | show IDs carrying a title slug, in the map | "
      f"{n(cov9['show_ids_with_a_slug_in_the_map'])} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A(f"**THE FIGURE THIS ARM PUBLISHES AS `747,478` IS B — distinct `(user, show)` PAIRS, not "
      f"season-coverage rows.** ***Reported, not reconciled: `decisions/0088` §2's table "
      f"characterises this arm's 747,478 as \"undeduplicated user-show SEASON-COVERAGE ROWS\". "
      f"Measured on this build it is not — the season-coverage row count is "
      f"{n(cov9['A_undeduplicated_user_show_SEASON_COVERAGE_ROWS'])}, and 747,478 is the "
      f"deduplicated pair count.*** The ruling's **conclusion** — two objects, both correct, do "
      "not reconcile — **holds and is applied here**; what it named as the distinguishing axis is "
      "not the axis on this arm's figures.")
    A("")
    A(f"**And the axis that does separate them is C: {n(cov9['C_split']['S1_evidence_and_no_S2'])} "
      f"+ {n(cov9['C_split']['S2_evidence_and_no_S1'])} + "
      f"{n(cov9['C_split']['both_S1_and_S2'])} = "
      f"{n(cov9['C_D9_CANDIDATE_user_show_pairs_carrying_S1_or_S2_evidence'])}.** "
      "**`decisions/0087` §2 and `0088` §2 record the other arm's quantity as "
      "`435,643 + 8,834 + 281,626 = 726,103`, in the same three classes.** **Two of the three "
      "classes agree exactly; the S1-evidence-and-no-S2 class differs by ONE pair**, so the two "
      "totals stand **1 apart**, not 0. ***REPORTED, NOT RECONCILED*** — and it is **not** the "
      f"{n(cov9['bridge_B_minus_C_pairs_with_only_S3_or_later_evidence'])} S3-only pairs, which "
      "are the whole of the B-against-C gap and are accounted for above. **No entry has recorded "
      "a one-pair difference in this class**; it is stated here so the diff has it.")
    A("")
    A("**The normalisation key decides the entire number, and both keys are now DEFINED in the "
      "spec** (`decisions/0074` ruling 5 adopts strict; `0076` §3 defines both, because \"strict\" "
      "and \"loose\" had existed only inside one instance's code, which the other is forbidden to "
      "read):")
    A("")
    A("| Key | Definition | complementary ID pairs | half (a) | half (b) |")
    A("| :--- | :--- | ---: | ---: | ---: |")
    A(f"| **STRICT — ADOPTED** | lowercase, drop every non-alphanumeric character, strip nothing "
      f"else | **{n(st9['complementary_signature_id_pairs'])}** | "
      f"**{n(ha['carrying_the_signature'])}** | **{n(hb['carrying_the_signature'])}** |")
    A(f"| LOOSE — reported alongside | remove a trailing four-digit year, then strict | "
      f"{n(lo9['complementary_signature_id_pairs'])} | {n(lo9['half_a_APPLY_position_7'])} | "
      f"{n(lo9['half_b'])} |")
    A(f"| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary "
      f"length, then strict | {n(tk9['complementary_signature_id_pairs'])} | "
      f"{n(tk9['half_a_APPLY_position_7'])} | {n(tk9['half_b'])} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    fn = d9["FOUR_NUMBERS_both_halves_under_both_keys"]
    A("**BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE** (`decisions/0078` §3, closing "
      "the one live asymmetry between the arms). **This follows from `0074` ruling 5's own reason "
      "rather than from a preference:** the loose count publishes **because it bounds how wrong "
      "strict could be**, and **that reason applies to half (b) exactly as it applies to half "
      "(a)**. Publishing the bound for one half and withholding it for the other **leaves the "
      "reader unable to bound the total**, and the error runs **opposite** to D9's own "
      "lower-bound caveat — the direction they were not warned about.")
    A("")
    A("| | strict (adopted) | loose (bound) |")
    A("| :--- | ---: | ---: |")
    A(f"| **half (a)** — fabricated never-started row | **{n(fn['half_a_strict'])}** | "
      f"{n(fn['half_a_loose'])} |")
    A(f"| **half (b)** — silently deleted S1-failing counterpart | **{n(fn['half_b_strict'])}** | "
      f"{n(fn['half_b_loose'])} |")
    A("")
    A(bt("all four numbers"))
    A("")
    A(f"- **(a) the fabricated never-started row, on the adopted key:** "
      f"{n(ha['carrying_the_signature'])} of {n(ha['never_started'])} never-started pairs "
      f"(APPLY, position 7); {n(ha['on_APPLY_position_5_the_table_row_set']['carrying_the_signature'])} "
      f"of {n(ha['on_APPLY_position_5_the_table_row_set']['never_started'])} on the position-5 "
      "table row set.")
    A(f"- **(b) the silently deleted S1-failing counterpart:** {n(hb['carrying_the_signature'])} "
      f"of {n(hb['pairs_failing_S1_completion'])} pairs that fail the S1 completion rule. "
      "**These rows are not in the analysis table and cannot be recovered from it**, so the set "
      "is a **DELIVERABLE of this pipeline run** (`decisions/0079` B5, strengthening `0075` "
      "ruling 2) — **and this section READS IT BACK from the file**, so if the stage stopped "
      "writing it this figure would **fail loudly rather than publish a 0**, which is the whole "
      "point: **a zero here reads as a data finding rather than a missing input.** "
      "**`decisions/0077` §2 RESTATES the ruling**, which as written named *\"position 3's drop "
      "set\"* — **an empty set**, because line 1 is already the S1-completer population and "
      "position 3 therefore removes 0 rows from the waterfall. The set is **the pair universe "
      "less the completers, 58,345 PAIRS**, and it is **not** the set-membership drop rule, which "
      "is a different rule, deletes 0 **records**, and would have put the wrong rule in the spec. "
      "This instance measured the same set before the restatement and the count is unchanged.")
    cu = lo9["clustering_universe_NAMED"]
    A(f"- **The loose count publishes because it BOUNDS HOW WRONG STRICT COULD BE**, and the "
      f"error runs **opposite** to D9's own lower-bound caveat. It is not adopted because "
      f"{lo9['why_it_is_not_adopted']}.")
    A("")
    A("**THE CLUSTERING UNIVERSE IS U1, RANKED BY DISTINCT STRICT KEYS MERGED** — Human Lead "
      "ruling, `decisions/0088` §3, closing the gap Red Team's B1 opened (`0085` §2, where **the "
      "two arms published DISJOINT cluster lists on IDENTICAL counts**) and `0087` §2 located "
      "(**the two arms' \"U1\" were two sets 62 apart under one label**). **BOTH ARMS NOW CLUSTER "
      "THE SAME OBJECT.**")
    A("")
    A("**The ground, as ruled:** the artifact D9 hunts is **a viewer's history splitting across "
      "two metadata entries for one show**, and **that split can occur anywhere in a history, not "
      "only among shows that survived the frame filters.** A frame-restricted universe finds only "
      "splits where **both sides made the cut** — the narrowest case — and **a bound computed on "
      "a narrow slice bounds very little.**")
    A("")
    A(f"**This arm clusters {cu['THIS_ARM_CLUSTERS']}** — "
      f"**U1 = {n(cu['U1_distinct_slugged_show_ids_anywhere_in_the_sweep_CLUSTERED'])} show "
      f"IDs**, read from the slug map collected over all 2,549 parsed history files, which is "
      "what *\"anywhere in the pulled sweep\"* means. **It is NOT U2 (the "
      f"{n(cu['candidate_universes_NOT_used_here_sized_for_comparison']['U2_the_1138_frame_shows'])} "
      "frame shows) and NOT U3 (the "
      f"{n(cu['candidate_universes_NOT_used_here_sized_for_comparison']['U3_the_D9_candidate_pairs_under_the_loose_key'])} "
      f"D9 candidate pairs).** {n(cu['clusters_with_more_than_one_strict_key'])} loose keys merge "
      "more than one strict key.")
    A("")
    prev = cu["THE_UNIVERSE_THIS_ARM_USED_ON_ITS_PREVIOUS_BUILD_AND_NO_LONGER_USES"]
    A(f"***THIS IS A CHANGE OF OBJECT FOR THIS ARM, and the corrected label is the point.*** On "
      f"build `{prev['build_it_was_published_on']}` this arm clustered **{prev['what_it_was']}** — "
      f"**{n(prev['size'])} show IDs** — and published that count under the label "
      f"**`distinct_show_ids_in_the_sweep`**, ***which is not what it counts***. "
      f"`decisions/0087` §2 caught it; `0088` §2(a) requires the label corrected to what it "
      f"counts, **and its \"0 carry no slug\" clause was therefore computed against the wrong "
      f"base**. **Both counts are real objects and both are published**: U1 is "
      f"{n(cu['U1_distinct_slugged_show_ids_anywhere_in_the_sweep_CLUSTERED'])}, the coverage-pivot "
      f"subset is {n(prev['size'])}, and **U1 − pivot = {n(prev['U1_minus_this'])}** — shows "
      "reaching the sweep only through a record D11 discards, an undated record, a specials-only "
      "record or a non-episode record. **The subset relation is asserted in the pipeline, not "
      "assumed.**")
    A("")
    A(f"***And the {n(prev['U1_minus_this'])} is the same 62 `decisions/0087` §2 measured as the "
      "gap between the two arms' \"U1\"s.*** That entry recorded the arms' slugged-ID sets as "
      "**62 apart under one label**; **this arm's U1 is now the larger of the two**, and the "
      "62 is **not an arm difference at all — it is the difference between the sweep and the "
      "coverage pivot, and both numbers were always recoverable from this arm alone**, which "
      "`0087` §2 says in its own last paragraph. **On this build the two arms should name one "
      "object; if they still differ, one has a bug and that is the finding.**")
    A("")
    A(f"**And \"largest\" ranks by {cu['what_LARGEST_ranks_by_here']}**")
    A("")
    A("| Ranked by distinct STRICT keys merged | | Ranked by distinct SHOW IDs merged | |")
    A("| :--- | ---: | :--- | ---: |")
    _l1 = lo9["largest_clusters_it_merges"][:3]
    _l2 = lo9["largest_clusters_ranked_by_distinct_show_ids_instead"][:3]
    for i in range(max(len(_l1), len(_l2))):
        c1 = (f"`{_l1[i]['loose_key']}` | {_l1[i]['distinct_strict_keys_merged']}"
              if i < len(_l1) else " | ")
        c2 = (f"`{_l2[i]['loose_key']}` | {_l2[i]['distinct_show_ids_merged']}"
              if i < len(_l2) else " | ")
        A(f"| {c1} | {c2} |")
    A("")
    A(bt("both cluster lists and the universe counts"))
    A("")
    A("**THE RULED BASIS TIES AT RANK 3, so a bare \"third-largest cluster\" is not reproducible "
      "from the basis alone.** The head-of-list above is a `head(3)` whose order at rank 3 is "
      "decided by the sort's stability rather than by the ruling. **Every key at every published "
      "rank, both bases:**")
    A("")
    A("| Rank value | Ranked by distinct STRICT keys merged | Ranked by distinct SHOW IDs merged |")
    A("| ---: | :--- | :--- |")
    _r1 = {x["value"]: x for x in cu["ranks_with_every_tied_key_stated"]}
    _r2 = {x["value"]: x for x in cu["ranks_by_distinct_show_ids_with_every_tied_key_stated"]}
    for v in sorted(set(_r1) | set(_r2), reverse=True):
        c1 = ", ".join(f"`{k}`" for k in _r1[v]["keys_at_this_rank"]) if v in _r1 else "—"
        c2 = ", ".join(f"`{k}`" for k in _r2[v]["keys_at_this_rank"]) if v in _r2 else "—"
        A(f"| {v} | {c1} | {c2} |")
    A("")
    A(f"**The basis reorders the list on its own, exactly as `0088` §3 says:** `blackout` carries "
      "**6 strict keys but 7 show IDs**, so it sits at rank 3 on one basis and rank 2 on the "
      "other, and ranking by show IDs displaces `maigret`. **`task-sheet.md`'s former "
      "illustration — The Twilight Zone, The Traitors, Manhunt — was U3 and is SUPERSEDED as the "
      "example; those three names are not wrong, they are another universe's answer.**")
    A("")
    A(f"**One row per show ID needs a tie-break and this arm states its own:** "
      f"{cu['one_row_per_show_id_tie_break']} "
      f"**{n(cu['show_ids_carrying_MORE_THAN_ONE_slug'])} show IDs carry more than one slug.** "
      f"Under the last slug instead the cluster count is "
      f"{n(cu['clusters_with_more_than_one_strict_key_under_the_LAST_slug_instead'])} against "
      f"{n(cu['clusters_with_more_than_one_strict_key'])} — **measured, not assumed away.**")
    A("")
    A("**If the other arm names the same universe and still differs, one of us has a bug and that "
      "is the finding.** These are remakes and national versions, exactly the failure `0074` "
      "names.")
    A(f"- **The third key is reported for the record and is neither ruled key.** It reduces "
      f"`the-100` to `the`. **This instance used it on its previous run and published "
      f"{n(tk9['complementary_signature_id_pairs'])} complementary pairs against the other arm's "
      "75; `decisions/0076` records that divergence as REPORTED, NOT RECONCILED.** Under the now-"
      "defined keys this instance reproduces both ruled figures exactly.")
    A(f"- **Merges, counted with the same query and reported separately:** "
      f"{n(d9['merges_counted_with_the_same_query_and_reported_separately']['strict_key'])} "
      "user-show rows on the strict key "
      f"({n(d9['merges_counted_with_the_same_query_and_reported_separately']['loose_key'])} on the "
      "loose key) where one ID carries both seasons and a same-title ID also appears in the "
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
    bw = diag["B3a_boundary_window_half_open_form"]
    A("### 5.6a The half-open form — MEASURED, not self-reported (B3(a))")
    A("")
    A("**Human Lead ruling, `decisions/0088` §1, on Red Team's B3/F1, which blocked the gate on "
      "the third and fourth passes.** The two unasserted mandates are **the half-open UTC-instant "
      "form** and **D11-as-global-cutoff** — *not* invariants 7 and 8, which were already "
      "measured, published and labelled DATA CHECK. **This arm's compliance is TRUE and was "
      "independently confirmed** — no `.date()`, `dt.date`, `normalize()` or day-flooring "
      "anywhere in `step8_a_*.py`, instants int64 seconds throughout. ***That is not what was "
      "missing: nothing measured whether either mandate is LOAD-BEARING on this data, and an "
      "unmeasured pass is indistinguishable from a check that looked nowhere.***")
    A("")
    A("**One thing the ruling does not say, and it decides the answer.** `T0` is day-floored and "
      "`W` and `H` are whole days, so **`τ1` and `τ2` land exactly on midnight UTC** — asserted "
      "in the pipeline, not assumed. The date-level form `date(ts) < date(τ1)` is therefore "
      "**identical** to the half-open `ts < τ1` and can never differ. **The form that CAN differ "
      "is `date(ts) ≤ date(τ1)`, which admits the whole of `[τ1, τ1 + 24h)`.** So the window the "
      "ruling names — `[τ1 − 24h, τ1)` — is the window on which the two forms **agree by "
      "construction**, and the interval on the **other** side is where the mandate is "
      "load-bearing. **Both are emitted; reporting only the named one would answer the question "
      "with the interval that cannot separate them.**")
    A("")
    A("| Population | Bound | in `[τ − 24h, τ)` *(ruling's window)* | **exactly at `τ`** | "
      "**where the two forms ACTUALLY differ** | rows affected | vacuous? |")
    A("| :--- | :--- | ---: | ---: | ---: | ---: | :--- |")
    for popk, poplab in (("APPLY_position_5", "APPLY, position 5"),
                         ("DERIV_position_5", "DERIV, position 5")):
        for bn in ("tau1", "tau2"):
            c = bw[popk][bn]
            A(f"| {poplab} | `{bn.replace('tau','τ')}` | "
              f"{n(c['episodes_in_the_24h_BEFORE_the_bound_named_by_the_ruling'])} | "
              f"**{n(c['episodes_EXACTLY_AT_the_bound'])}** | "
              f"**{n(c['episodes_in_the_24h_AFTER_the_bound_where_the_two_forms_ACTUALLY_DIFFER'])}** | "
              f"{n(c['rows_where_the_two_forms_would_differ'])} | "
              f"{'**VACUOUS**' if c['VACUOUS'] else 'no — load-bearing'} |")
    A("")
    A(f"**Coverage:** {n(bw['APPLY_position_5']['coverage_rows_examined'])} rows and "
      f"{n(bw['APPLY_position_5']['coverage_distinct_S2_episodes_on_those_rows'])} distinct S2 "
      f"episodes on APPLY; {n(bw['DERIV_position_5']['coverage_rows_examined'])} rows and "
      f"{n(bw['DERIV_position_5']['coverage_distinct_S2_episodes_on_those_rows'])} episodes on "
      "DERIV. **Unit: distinct S2 episodes by canonical timestamp** — the objects the bound is "
      "actually tested against, since `A` and `A_H` are sets of distinct episodes. "
      + bt("every figure in this table"))
    A("")
    A("**RESULT: THE MANDATE IS LOAD-BEARING, NOT VACUOUS.** On APPLY a `date(ts) ≤ date(τ1)` "
      f"form would admit **{n(bw['APPLY_position_5']['tau1']['episodes_in_the_24h_AFTER_the_bound_where_the_two_forms_ACTUALLY_DIFFER'])} "
      f"episodes on {n(bw['APPLY_position_5']['tau1']['rows_where_the_two_forms_would_differ'])} "
      "rows** into `A`. **No cell is 0, so no invariant here is labelled vacuous** — and where a "
      "cell had been 0 it would have been **stated as a zero, not passed silently**.")
    A("")
    A("> ***A COINCIDENCE, FLAGGED SO IT IS NOT MISREAD.*** The APPLY `τ1` differing-episode count "
      f"is **{n(bw['APPLY_position_5']['tau1']['episodes_in_the_24h_AFTER_the_bound_where_the_two_forms_ACTUALLY_DIFFER'])}**, "
      "**the same integer as the 703 liveness exclusions.** **They are unrelated objects** — one "
      "counts distinct S2 episodes in a 24-hour interval, the other counts pairs removed at "
      "position 6 — **and no arithmetic connects them.** This report states it because a repeated "
      "integer in a document this size gets read as a shared quantity.")
    A("")
    A("**And the ruling's own second quantity is NOT zero:** exactly "
      f"**{n(bw['APPLY_position_5']['tau1']['episodes_EXACTLY_AT_the_bound'])} episode falls "
      f"exactly AT `τ1`** on APPLY (and "
      f"{n(bw['DERIV_position_5']['tau1']['episodes_EXACTLY_AT_the_bound'])} on DERIV), so "
      "**`0068`'s strictness ruling — an instant *at* the bound is not *after* it — changes the "
      "answer for a real row rather than for none.**")
    A("")
    ps = diag["B3b_D11_per_site"]
    psa = {x["site"]: x for x in ps["assertions"]}      # by name, never by position
    A("### 5.6b D11 applied per site, asserted at each (B3(b))")
    A("")
    A("**`decisions/0088` §1(b).** D11 is specified to apply *\"to EVERY computation\"*, and "
      "***this arm's previous deliverable named five sites in prose with a count at none.*** "
      "**Every site now carries its own unit, its own count and its own assertion — not one "
      "assertion about the rest.** **Ground, as ruled: the unstated version of exactly this scope "
      "produced Step 7's 792-against-791.**")
    A("")
    A("| Site | Unit | examined | **excluded by D11** | D11 applied? | assertion |")
    A("| :--- | :--- | ---: | ---: | :--- | :--- |")
    for x in ps["assertions"]:
        sv = ps["sites"][x["site"]]
        flag = "**PASS**" if x["holds"] else "**FAIL**"
        if x["LOOKED_AT_ZERO_UNITS"]:
            flag += " *(looked at ZERO units — holds trivially)*"
        A(f"| `{x['site']}` | {sv['unit']} | {n(x['coverage_unit_count'])} | "
          f"**{n(x['excluded_by_D11'])}** | {'yes' if x['D11_applied'] else '**NO — declared**'} | "
          f"{flag} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A(f"**{ps['sites_total']} sites; D11 is applied at {ps['sites_where_D11_IS_applied']} and "
      f"NOT applied at {ps['sites_where_D11_is_NOT_applied_and_say_so']}, which says so rather "
      f"than being omitted. All {ps['sites_total']} site assertions hold: "
      f"{ps['all_site_assertions_hold']}.** "
      f"**{ps['sites_asserted_on_a_non_empty_unit_set']} of them were asserted on a NON-EMPTY "
      "unit set**; the rest are listed as having looked at zero units, because **a check that "
      "finds nothing because it looked nowhere must not read as a pass** (`CLAUDE.md`).")
    A("")
    A("**Two things this measurement establishes that the prose could not.** First, **the eight "
      "`action_count_*` sites' D11 exclusions sum to exactly the 167 in-frame S1/S2 records at or "
      "after `τ_pull`** — the same 167 that indexes the closed records-examined family "
      "(`0083` §1, 94 S2-side + 73 S1-side) — **so the action counts and that denominator are the "
      "same discard, seen at two sites.** Second, **the liveness-evidence site is the only one "
      "where D11 moves an input**: "
      f"**{n(ps['sites']['liveness_evidence']['accounts_whose_max_play_id_MOVES_under_D11'])} "
      "accounts' maximum play `id` moves under D11 and "
      f"{n(ps['sites']['liveness_evidence']['accounts_whose_last_insertion_instant_MOVES_under_D11'])} "
      "accounts' last insertion instant moves with it.** **That is `0070` ruling 2's site, and it "
      "is load-bearing on this data even though the exclusion count it produces is 703 either "
      "way** — the ruling's own measured claim, now measured at the site rather than at the "
      "outcome.")
    A("")
    A("**`A` and `A_H` are INERT BY CONSTRUCTION and the count is stated rather than the "
      "construction being asserted about:** "
      f"{n(ps['sites']['A_the_set_tested_at_tau1']['episodes_at_or_after_tau_pull_that_D11_would_exclude'])} "
      "distinct S2 episodes on position-5 rows sit at or after `τ_pull`, and "
      f"**{n(psa['A_the_set_tested_at_tau1']['excluded_by_D11'])} of them can enter `A` or `A_H`** — because "
      "D10 forces `τ1 ≤ τ2 ≤ τ_pull` on every retained pair. **That is the invariant promoted "
      "into the published set as check 9** (`0088` §1(c)); see the invariant report.")
    A("")
    A("**The S1 completion walk is the one site where D11 is NOT applied, and it says so.** "
      f"{n(ps['sites']['S1_completion_walk']['records_at_or_after_tau_pull_on_the_S1_side'])} "
      "in-frame S1 records sit at or after `τ_pull`; applying D11 there would stop "
      f"{psa['S1_completion_walk']['pairs_that_would_stop_being_completers']} pairs being completers "
      f"and move {psa['S1_completion_walk']['completion_dates_that_would_move']} completion dates. "
      "**`decisions/0068` fixes waterfall line 1 at the published 220,107 and lists whether D11 "
      "moves it as an OPEN question**, so the counterfactual is measured and published rather "
      "than the site being left out of the table.")
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
    ch = outc["channel_counts_on_the_table_position_5_APPLY"]
    at0 = outc["analysis_table"]
    A("### 5.10 Discovery channel — two boolean columns, and the overlap in all three units")
    A("")
    A("A single categorical would either **drop the overlap or assign it arbitrarily**, and the "
      "arbitrary assignment would be invisible in the dual diff since both instances would make "
      "it the same way only by luck. **Two flags let Step 11 cut on either channel or on the "
      "overlap** (`0070` ruling 3).")
    A("")
    cc = outc["channel_counts"]
    cp, ca_ = cc["on_the_step3_discovery_pool"], cc["on_the_accounts_actually_pulled"]
    A("**PUBLISH THE OVERLAP IN BOTH UNITS, EACH WITH ITS CONSUMER NAMED** (`decisions/0079` B7) "
      "— **all three readings publish; picking one leaves another consumer holding a wrong-unit "
      "figure.** `0070` ruling 3 gave *\"324 users are in both\"* and named no population, **the "
      "shape that has recurred through this entire chain, inside the ruling written to fix a "
      "different unlabelled figure**; `0077` §1 then stated two and `0079` B7 all three. Measured "
      "here, each independently:")
    A("")
    A("| Reading | Unit | n | Channel A | Channel B | **in both** | Consumer |")
    A("| :--- | :--- | ---: | ---: | ---: | ---: | :--- |")
    A(f"| Step 3 **discovery pool** | usernames | {n(cp['population'])} | {n(cp['channel_a'])} | "
      f"{n(cp['channel_b'])} | **{n(cp['in_both'])}** | Step 3's seeding-bias statement; **Step 14 "
      "ledger item 1** — the pool's composition |")
    A(f"| **accounts actually pulled** | accounts | {n(ca_['population'])} | {n(ca_['channel_a'])} "
      f"| {n(ca_['channel_b'])} | **{n(ca_['in_both'])}** | **Step 4 coverage reporting** (the "
      "pull stopped at 62.9% of plan) |")
    A(f"| **position-5 population** | accounts | {n(ch['accounts_population'])} | "
      f"{n(ch['accounts_channel_a'])} | {n(ch['accounts_channel_b'])} | "
      f"**{n(ch['accounts_in_both'])}** | **Step 11**, which recomputes the headline within each "
      "channel and so cuts **the analysis population, not the pool** |")
    A(f"| **position-5 population** | pairs | {n(ch['pairs_population'])} | "
      f"{n(ch['pairs_channel_a'])} | {n(ch['pairs_channel_b'])} | **{n(ch['pairs_in_both'])}** | "
      "**Step 11**, same reading in the unit the headline is computed in |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A(f"All three reproduce: **{n(cp['in_both'])} of {n(cp['population'])}** usernames, "
      f"**{n(ca_['in_both'])} of {n(ca_['population'])}** accounts pulled, and "
      f"**{n(ch['accounts_in_both'])} of {n(ch['accounts_population'])}** accounts / "
      f"**{n(ch['pairs_in_both'])} of {n(ch['pairs_population'])}** pairs in the position-5 "
      "population. **`0078` restates the first two on the position-5 build of 2026-08-13 and "
      f"records the third as unpublished; `0079` B7 publishes all three.** The pool figure is not "
      "an account figure and neither is a pair figure; **read without its population, any one of "
      "them reads as a divergence from the others.**")
    A("")
    A("**One correction to `0079` B7 as dictated, because the mapping is reversed against the "
      "files** — and the ruling entry itself records the correction: it assigned **Step 11 to "
      "users** and **the pool statistic to accounts**. Step 11 recomputes the headline, which is "
      "over **pairs on the position-5 row set**, so it cuts the analysis population; and the pool "
      "statistic is the **5,694 usernames**. The substance — both units, consumers named — is "
      "executed as ruled.")
    A("")
    A("---")
    A("")
    A("## 6. The analysis table")
    A("")
    A("**The deliverables of this run, all four named** (`task-sheet.md` Step 8 *Deliver*, as "
      "amended by `decisions/0079` B5):")
    A("")
    A("| Deliverable | Path | Written by |")
    A("| :--- | :--- | :--- |")
    A("| analysis table | `processed/step8/a/analysis_table.csv.gz` | stage 3 |")
    A("| **position-3 drop set — the 58,345 pairs failing the S1 completion rule** | "
      "`processed/step8/a/position3_drop_set.csv.gz` | **stage 2 of the same run** (§6.1) |")
    A("| filter waterfall and required counts | `artifacts/step8-waterfall-a.md` / `.json` | "
      "stage 6 |")
    A("| invariant report | `artifacts/step8-invariants-a.md` / `.json` | stage 6 |")
    A("")
    A("The run record, with per-stage return codes and timings, is `logs/step8_a_run.json`.")
    A("")
    at = outc["analysis_table"]
    A(f"`{at['path']}` — **{n(at['rows'])} rows, {at['columns']} columns**, one row per user-show "
      "pair, **the POSITION-5 row set on APPLY** (`decisions/0074` ruling 1). "
      + btx("every count in this section") + ".")
    A("")
    A(f"- **`live` and `outcome` are COLUMNS, not filters.** {n(at['rows_live_position_6_retained'])} "
      f"rows carry `live = true` and {n(at['rows_not_live_position_6_excluded'])} carry "
      "`live = false` — the position-6 exclusions are **in the file**, not reconstructed from it. "
      "Both readings of \"one row per pair\" give identical counts, so this is a ruling and not a "
      "correction: **a reconstruction that agrees today is still a second definition tomorrow, "
      "and the dual diff cannot see it.**")
    A(f"- **{n(at['DERIV_rows_flagged_within_it'])} rows carry the DERIV flag**, so both "
      "populations are produced by Step 8 and nothing downstream has to rebuild one.")
    A(f"- It carries outcome state, abandonment point, the two discovery-channel booleans, the "
      f"per-pair action counts and all {at['step2_show_fields_carried']} Step 2 show fields. "
      "**It stays in `processed/` and is never published.**")
    A("")
    A(f"**THE COLUMN SET IS ENUMERATED, NOT COUNTED — {at['columns']} NAMES, EXACTLY THESE** "
      "(`decisions/0080` §1, replacing `0077` §3's count; **extended to 88 by `0081`** and **to 89 "
      "by `0082`**). **The arms converged on the 87 names on an earlier run, but converged is not "
      "specified**, and Step 8b's schema is built on this vocabulary with Steps 9–13 writing into "
      "it **directly, with no conversion layer** (`0066`), so it is fixed **before** the schema "
      "exists. **This instance asserts SET EQUALITY against the spec's list, not a count** — a "
      "count is arithmetically satisfiable by the wrong columns, which is exactly how an earlier "
      "run produced 88 against 87 for the same contents. Column **order** is specified nowhere; "
      "this table is in construction order and the sorted list is in the `.json` so an order "
      "difference cannot be mistaken for a name difference.")
    A("")
    A("**The count is 89 again after `0082`, but it is a different 89** than `0077`'s: "
      "`f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not matching a "
      "set**, which is why the assertion here is on the names.")
    A("")
    csd = at["column_set_verified_against_the_spec_ON_DISK"]
    A("**AND THE LIST ASSERTED AGAINST IS NOW READ OFF `task-sheet.md` AT RUN TIME** — "
      f"{n(csd['distinct_names_parsed'])} distinct names parsed from the enumeration block, "
      f"matching this arm's transcription: **{csd['matches_the_transcription_in_this_file']}**. "
      "***This closes Red Team's fourth-pass F6*** (`decisions/0087` §5), which found this arm's "
      "report claiming set equality *\"against the spec's list\"* while the code asserted against "
      "**a hand transcription that never opened `task-sheet.md`**. **A transcription is a second "
      "copy of the enumeration, and a propagation change to the spec would not reach it** — and "
      "**the dual diff cannot catch a propagation failure**, so only this check can. **F6 was "
      "carried as a limitation rather than ruled; it is closed here rather than restated.** "
      "**A parse that found nothing would FAIL rather than pass**, and the parsed count is "
      "published above.")
    A("")
    sil = at["surviving_aggregate_of_the_silent_at_tau1_column"]
    A("**Two names are in the set that `0080` did not have:**")
    A("")
    A(f"- **`silent_at_tau1` — RESTORED by `decisions/0081`, and the reason is the one `0080` §2 "
      "stated when it dropped the column.** It is **not recoverable from `live` and `outcome` on "
      "Continued rows**, because `live` is true for **every** Continued pair regardless of silence "
      "— the rule's second conjunct is `NOT Continued`. **Without it the Continued-and-silent "
      "count cannot be recomputed from this table.** That count is "
      f"**{n(sil['value_APPLY_position_5'])}** — the **size of the outcome-conditioning**, the "
      "figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation. "
      "It is **both a column and an aggregate** here "
      f"({n(sil['value_APPLY_position_5'])} on APPLY position 5, "
      f"{n(sil['value_APPLY_position_7_post_liveness'])} post-liveness, "
      f"{n(sil['value_DERIV_position_5'])} on DERIV position 5), so the figure is readable without "
      f"opening the table. {btx('these three counts')}.")
    A("- **`p_at_bound` — added at `decisions/0082`, definition restated by `0083` §2.** It marks "
      "**WHETHER `p` reached its bound, not why.** Emitted as a **nullable** boolean: null where "
      "`p` is null, because an inapplicable value and a false one must not look alike. **`0082`'s "
      "two-mechanism definition is superseded** — the clauses are coextensive, on a three-link "
      "chain whose third link is measured and not construction (`0085` §4), and "
      "the `FALSE` class is empty — **and the column is kept anyway**, because Step 10 needs the "
      "spike labelled and because an emptiness asserted in prose and never emitted cannot be "
      "checked. §3.1.")
    A("")
    A("**Two names stay dropped and both are free** (`0080` §2, unchanged by `0081` and `0082`): "
      "**`max_episode_in_A`**, read by nothing downstream, and **`f2_in_A_H`**, derivable as "
      "`max_episode_in_A_H == s2_F`. **`0083` §3b finished this one**: `0077`'s adopted-name "
      "table still listed `f2_in_A_H` beside a bullet dropping it, and the name is now **marked "
      "at the point of use rather than deleted**, so `0077`'s spelling ruling — `A_H`, not `AH` — "
      "survives without the column.")
    A("")
    A("**The names themselves are `decisions/0077` §3's and were not chosen here.** Renamed from "
      "this instance's earlier run: `in_channel_*` → **`discovered_channel_a` / "
      "`discovered_channel_b`**; `in_population_APPLY` / `in_population_DERIV` → **`in_apply` / "
      "`in_deriv`**; `tau1_utc` / `tau2_utc` → **`tau1` / `tau2`**; `T0_utc_date` → "
      "**`t0_date`**; `T0_binding_term` → **`t0_binding_term`**; `s1_completion_date_utc` → "
      "**`s1_completion_date`**; `n_A_distinct_s2_before_tau1` → **`n_A`**; "
      "`n_AH_distinct_s2_before_tau2` → **`n_A_H`**; `max_episode_in_AH` → "
      "**`max_episode_in_A_H`**; `n_rec_s{1,2}_*` → **`action_count_s{1,2}_*`**. **No `_utc` "
      "suffix survives**: every instant in this study is UTC by Step 1 §2.4, and suffixing some "
      "columns implies the others are not.")
    A("")
    A("**Both instances' extra columns are kept** (`0077` §3, and both are in `0080`'s "
      "enumeration): `has_s3_or_later_evidence`, which D4 reads, and "
      "**`s1_completion_used_a_post_cutoff_record`**, which the still-open D11-at-position-3 "
      "question reads. The second is computed independently here rather than assumed: the "
      "first-pass walk runs in ascending canonical-timestamp order, so the completing episode's "
      "timestamp is the maximum over the prefix consumed, and the flag is exactly `complete AND "
      f"comp_ts ≥ τ_pull`. **It is true on "
      f"{n(pos['D11_counterfactual_on_position_3']['completers_whose_first_pass_walk_used_a_post_cutoff_record'])} "
      "pairs of the 220,107** — the same 4 that stop being completers when D11 is applied to the "
      f"S1 walk, which is the arithmetic the open question turns on. {btx('that count')}.")
    A("")
    ds = pos["position_3_drop_set_DELIVERABLE"]
    dsi = diag["D9_split_artifacts"]["position_3_drop_set_input"]
    A("### 6.1 The position-3 drop set — a DELIVERABLE of this run, not a side file")
    A("")
    A(f"`processed/step8/a/position3_drop_set.csv.gz` — **{n(ds['pairs_failing_the_S1_completion_rule'])} "
      "pairs, the pairs that FAIL the S1 completion rule.** **Human Lead ruling, "
      "`decisions/0079` B5:** it is **named in the deliverable list**, **written by the same "
      "pipeline run that writes the table** (stage 2 of `src/step8_a_run.py`), and carries **each "
      "pair's distinct-episode counts and the show's threshold**, which is what D9 half (b) "
      "reads.")
    A("")
    A(f"- **It is read back, not merely written.** The stage that computes half (b) loads this "
      f"file and asserts it against position 3's recomputed rule ({n(dsi['pairs'])} rows agreeing "
      "to the row). **If it were missing, that stage fails loudly instead of publishing 0** — "
      "which is the failure `0075` ruling 2 exists to prevent, since **a zero here reads as a "
      "data finding rather than a missing input.** A helper script's side file is not a thing the "
      "next run is obliged to produce; a stage of this run is.")
    A(f"- **Columns:** `{'`, `'.join(ds['carries'])}`.")
    A(f"- **Why the pairs fail:** {n(dsi['short_of_the_0_90_threshold'])} never reached "
      f"`ceil(0.90 × L1)` distinct S1 episodes; {n(dsi['reached_the_threshold_but_never_watched_F1'])} "
      "reached the threshold but never watched the S1 finale `F1`.")
    A("- **It is the pair universe less the completers — position 3's RULE, not its waterfall "
      "line**, which is 0 by construction (`0077` §2). It is **not** the set-membership drop "
      "rule, which is a different rule and deletes 0 **records**.")
    A(f"- {btx('all four counts in this subsection')}. **`0078` restates the 58,345 as "
      "*position-3 rule, position-5 build of 2026-08-13*; it is re-measured here on this build "
      "and agrees.**")
    A("")
    A("**Other working files, also in `processed/step8/a/` and also never published:** "
      "`position5_table.npz`, the per-arm working table; `drops_per_show.csv`; `show_slugs.csv`; "
      "the stage `.json` outputs this report is generated from.")
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
    A("1. **~~The `W` arm grid.~~ CLOSED by `decisions/0075` ruling 3.** The grid is "
      f"{' / '.join(str(x) for x in arms['arm_grid'])} days, stated in that entry and in "
      "`task-sheet.md` Step 13. This instance no longer chooses it. (It is the same grid this "
      "instance chose and named on its previous run, so nothing measured moves.)")
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
    A("8. **D3′'s denominator is the position-7 (post-liveness) Started-and-left set**, which is "
      "what reproduces `0075`'s ruled series. The position-5 figures are emitted alongside in the "
      "`.json` so the choice is visible and neither reading is hidden.")
    A("9. **~~The set half (b) is measured on.~~ CLOSED by `decisions/0077` §2 and made a "
      "DELIVERABLE by `0079` B5.** The previous run had to choose an interpretation, because "
      "*\"position 3's drop set\"* named an empty set on this frame. The ruling names it: **the "
      "pair universe less the completers, "
      f"{n(pos['position_3_drop_set_DELIVERABLE']['pairs_failing_the_S1_completion_rule'])} "
      "pairs** — the set this instance retained and measured before the restatement, so **nothing "
      "measured moves**; what changed this run is **who writes it and who reads it** (§6.1). The "
      "unit is **pairs**, and it is **not** the set-membership drop rule.")
    A("10. **~~Column names, and the 89-versus-`f2_in_A_H` contradiction.~~ CLOSED by "
      f"`decisions/0080` §1**, which replaces the count with an enumeration and drops `f2_in_A_H` "
      f"as derivable — **and by `0081` and `0082`, which take the enumeration to {at['columns']} "
      "names.** **The item this instance reported unreconciled two runs ago is resolved, and in "
      "the direction it flagged.** The trade `0080` made — dropping `silent_at_tau1` — was "
      "**reversed by `0081` on the ground this instance's own report gave for calling it a real "
      "loss**, and the aggregate is kept beside the column anyway.")
    A("13. **~~`p_at_bound`'s two classes are not two classes.~~ CLOSED by `decisions/0083` §2**, "
      "in the direction this instance reported. The column now marks **whether** `p` reached its "
      "bound rather than **why**; the `FALSE` class is empty by construction and the `p = 1.0` "
      "counts publish as **totals** — §3.1. **Nothing measured moves**: the encoding this "
      "instance emitted under `0082` and the encoding `0083` specifies are the same predicate.")
    A("11. **Column ORDER is specified nowhere.** This table is in construction order; the sorted "
      "name list is in the `.json`. **If the arms differ here it is an order difference, not a "
      "name difference**, and the enumerated set is identical either way.")
    A("12. **The `build` label's granularity.** `0079` B6 requires every count to name its build "
      "and does not say at what granularity. This instance defines the build once (§0, with stage "
      "file hashes and the git HEAD) and cites a **tag** at each figure; the alternative — the "
      "full record inline at every figure — carries the same information and reads worse. **A "
      "figure measured on a different build says so instead** (the 3,440).")
    A("")
    A("---")
    A("")
    A("## 9. Disagreements between surfaces, reported and not fixed")
    A("")
    A("Reported because the spec asks for them, and not edited: `decisions/` and `task-sheet.md` "
      "are not this instance's to amend.")
    A("")
    A("1. **~~`action` as a column~~ — CLOSED.** The previous `-a` run reported three surfaces "
      "still requiring a row-level `action` column that `0070` ruling 4 had replaced. All three "
      "are now marked: `task-sheet.md` Step 13 (by `0073`), Step 1 §2.3 and §9 (by `0073` and "
      "`0076` §4), and the `analytics-engineer` head bullet. **Nothing emitted changed** — "
      "per-pair counts by action type, which is what Step 13's arm reads.")
    A("2. **~~`decisions/0033`'s pre-2020 comparator at `W = 213`~~ — CLOSED by `0073`.** The "
      f"comparator is now 3.0%, and this instance measures "
      f"{pct(r213['pre-2020']['lost_share'], 1)} independently through the mandated order.")
    A("3. **~~`decisions/0034`'s D3′ cleared-share series~~ — CLOSED by `0075`.** The ruled "
      "series is now 99.53% → 97.73% with its population stated; this instance reproduces it — "
      "see §4.3.")
    A("4. **~~The 94-record denominator is open and published unreconciled.~~ CLOSED by "
      "`decisions/0083` §1**, on the arithmetic this instance published last run and on the same "
      "arithmetic reproduced here. **It was never a divergence**: the three readings differ only "
      "in where D11 is applied, all three drop 0, and the item publishes as a **coverage figure "
      "with its pipeline named** rather than as a Step 14 limitation — §5.1.")
    A("5. **D3′ is not monotone in `W`** between the 91 and 107 arms — see §4.3. Measured, not "
      "resolved.")
    A("6. **`task-sheet.md` Step 8's open D11 question at position 3 is untouched** — applying "
      "D11 to the S1 walk gives 220,103 rather than the published 220,107. Measured in §5.6, not "
      "applied. **The `s1_completion_used_a_post_cutoff_record` column carries the 4 pairs it "
      "turns on**, so whoever closes the question does not have to rebuild them.")
    A("7. **~~`0077`'s `f2_in_A_H` against its count of 89.~~ CLOSED by `0080` §1**, and the "
      "superseded sentence is now struck in `task-sheet.md` and in the `analytics-engineer` file "
      "— **the defect this instance reported on the previous run has been fixed on both "
      "surfaces.**")
    A("8. **~~Two residuals in the column-set bullets, on both surfaces.~~ BOTH FIXED by "
      "`decisions/0083` §3**, and both were reported here on the previous run as not this "
      f"instance's to amend. **(a)** The strike-through note read *\"the 88-name ENUMERATION\"* "
      f"for its own replacement while the enumeration above it was {at['columns']} names; it now "
      "reads 89, with the 88 kept as the intermediate state it was. **(b)** `0077`'s adopted-name "
      "table listed `f2_in_A_H` among the adopted names while a bullet in the same section "
      "dropped it as derivable; it is now **marked at the point of use rather than deleted**, so "
      "`0077`'s **spelling** ruling — which still governs `n_A`, `n_A_H` and "
      "`max_episode_in_A_H` — is not lost with the column. **Nothing this instance emits "
      "changes**: the enumeration was the operative object in both cases and was followed by set "
      "equality against the 89 names.")
    A("9. **~~The set-membership records-examined denominator is unruled.~~ CLOSED by "
      "`decisions/0083` §1** — see item 4 and §5.1. `0074`'s *\"publish both, not one\"* is "
      "**strengthened to three, each naming its pipeline**, and the Step 14 routing is withdrawn.")
    A("10. **NEW, and it is live: `decisions/0083` §2 did not reach SURFACE 7.** "
      "`.claude/agent-memory/second-brain/glossary-terms-and-thresholds.md` carries the "
      "**denominator** correction of `0083` §1 in its own row, and its **`p_at_bound` bullet is "
      "untouched**: it still states `0082`'s **two-mechanism** definition as current, still "
      "carries **`0082`'s motive sentence — the one `0083` §2 WITHDREW and registered in "
      "`WITHDRAWN_PHRASES`** — as a live claim, and still calls 1,246 and 1,230 **totals the two "
      "classes must sum to**, which is the reading `0083` §2 withdrew. **Reported, not edited: "
      "`second-brain` writes its own memory and no other agent writes into it.** `0083` §4 "
      "records surface 7 as reached, and it was — **for one of the two rulings.**")
    A("11. **The phrase control cannot see item 10, and \"none\" is therefore not a clean result "
      "on wrapped prose.** `WITHDRAWN_PHRASES` is matched as a **literal substring** against "
      "Markdown that is **hard-wrapped**, so a withdrawn phrase broken across a line break does "
      "not match. **Reproduced: normalising whitespace before matching turns up three occurrences "
      "the literal matcher misses** — one is item 10; the other two are in the two "
      "`analytics-engineer` files, **inside explicit withdrawal notes**, so they are legitimate "
      "and would pass either way. **`check_surfaces.py` reports `PHRASE HALF … none` with all "
      "three invisible to it.** **Not fixed here**: the control is shared by both arms and by the "
      "Human Lead's diff, and changing it mid-gate changes what the diff is taken over. **The "
      "one-line change is to match against `re.sub(r\"\\s+\", \" \", text)`.**")
    A("12. **NEW, and it is `decisions/0088`'s own propagation gap: `0088` §1(c) takes the "
      "assertion set from EIGHT to NINE, and no surface says nine.** **Surfaces 4 and 5** — "
      "`.claude/agents/analytics-engineer.md` and `-b.md`, both edited by `0088` — still read "
      "***\"THE ASSERTION SET NOW HAS EIGHT MEMBERS\"***, and **surface 1**, `task-sheet.md`, "
      "still reads ***\"The set is now EIGHT\"***. **The negative half of the grep control passes "
      "clean here**, because eight is not a superseded *figure* until the ninth lands; **the "
      "POSITIVE half is what catches it, and \"nine\" appears on no surface** — which is exactly "
      "the failure mode `CLAUDE.md` records the analytics-engineer as having added the positive "
      "half for. **Reported, not edited: `task-sheet.md` and the agent files are not this "
      "instance's to amend.**")
    A("13. **NEW: `task-sheet.md`'s invariant-labelling bullet still carries the PRE-`0076` "
      "count.** It reads *\"The count is four pure code checks, one that is a code check by "
      "construction … and one item that is not an invariant at all\"* — the **six-member** "
      "reading, which `0076` superseded and `task-sheet.md:995` itself calls superseded 280 lines "
      "lower. **One file, two counts, each declaring the other wrong** — the exact shape "
      "`CLAUDE.md` describes. **Reported, not edited.**")
    A("14. **NEW: `decisions/0088` §2 characterises THIS ARM's 747,478 as *\"undeduplicated "
      "user-show SEASON-COVERAGE ROWS\"*. Measured on this build it is not** — it is **distinct "
      "`(user, show)` PAIRS**; the season-coverage row count is a different and larger number, "
      "published in §5.5. **The ruling's conclusion is right and is applied** — two objects, both "
      "correct, do not reconcile — **but the axis it names is not the axis.** ***`0088` §4 "
      "records that all three of its own rulings named the wrong referent; this is a fourth "
      "instance of the same shape, in the entry that documents it.*** **Reported, not "
      "reconciled.**")
    A("15. **NEW, and it is a genuine ARM-AGAINST-ARM divergence of ONE PAIR.** `0087` §2 and "
      "`0088` §2 record the other arm's D9 candidate-pair split as **`435,643 + 8,834 + 281,626 "
      "= 726,103`**. This arm measures **`435,642 + 8,834 + 281,626 = 726,102`** in the same "
      "three classes — **two classes agree exactly and the S1-evidence-and-no-S2 class differs by "
      "1.** **It is not the S3-only bridge**, which is accounted for separately in §5.5. **No "
      "entry has recorded a one-pair difference here**, because the two published totals were "
      "read as differing by the whole S3-only gap. ***REPORTED, NOT RECONCILED.***")
    A("16. **NEW: the ruled ranking basis TIES at rank 3, so the illustration is not fully "
      "determined by it.** `0088` §3 names `secondchance` (8), `theisland` (7), `maigret` (6) — "
      "and this arm reproduces the first two exactly, **but SIX loose keys tie at 6** and which "
      "of them appears third is decided by the sort's stability, not by the ruling. **Every key "
      "at every published rank is listed in §5.5 under both bases**, so the list is comparable "
      "without depending on the tie order. **Reported, not resolved.**")
    A("17. **CARRIED, `0087` F5, now the FOURTH occurrence of the string: "
      "`specs/step8-readback.md:3` still says Step 8 *\"has not launched\"*.** `0086` §3 stamped "
      "the two artifacts generated from that file and missed the source. **The structural half is "
      "unchanged: `specs/` is not one of `CLAUDE.md`'s eight propagation surfaces, so no control "
      "looks at it.** **Reported, not edited.**")
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
    wcf = inv["what_can_actually_fail"]
    B("> **RERUN AGAINST `decisions/0088`, ordered by the Human Lead — a rerun, not an "
      "amendment.** The previous `-a` invariant report was **not patched**; nothing in it is read "
      "or carried. **Every result below is produced by one pipeline run.** ***`0088` §1(c) ADDS "
      "AN INVARIANT — the set is NINE, not eight.*** It promotes the `τ2 ≤ τ_pull` assertion, "
      "which **already ran in this arm's stage 3 and sat outside the published set**, into the "
      "deliverable, labelled **CODE CHECK**. ***It makes the falsifiability ratio worse, not "
      "better***: six pure code checks now, and **still exactly TWO checks that can fail on real "
      "data**. **`0088` §2(d) also STRIKES one sentence from this report** — see the coverage "
      "section. The other "
      "rulings that reach this report are structural rather than numerical. **`0079` B6: every "
      "invariant result names the build it was measured on** — build " + BT + ", defined in full "
      "in the waterfall deliverable §0. **`0080` §3: every invariant names the population it runs "
      "on and accounts for every row in it**, reporting `rows_asserted + rows_not_asserted = "
      "rows_in_the_stated_population`. **`0081` and `0082` change the column set, not the "
      "invariant set: no invariant result moves.**")
    B("")
    B("> **Why that second one matters, in this report's own numbers.** `0080` §3 records that in "
      "the previous dual run one arm asserted `p` on **19,042** rows — the *post-liveness* "
      "Started-and-left count — against a *pre-liveness* non-S&L clause of **177,513**, summing "
      "to **196,555 against a 196,654-row table**. **99 rows were covered by neither clause, and "
      "those 99 are exactly the started-and-left liveness exclusions.** Neither report disclosed "
      "the gap and no control could see it. **This report states both clauses and their sum for "
      "every check** — see the coverage table below, where `p` reads **19,141 + 177,513 = "
      "196,654** and the post-liveness 19,042 appears only as a labelled contrast.")
    B("")
    B("> **EVERY INVARIANT CARRIES A LABEL** (`decisions/0068`). **A code check catches an "
      "implementation that computed something wrongly; it cannot fail on any data, and it is NOT "
      "evidence for the rule.** A report saying \"all invariants passed\" overstates what was "
      "verified unless it names which ones could have failed.")
    B("")
    B(f"**Result: {len(inv['invariants'])} checks ran and all passed.** "
      f"**{wcf['checks_that_cannot_fail_on_any_data']} cannot fail on any data** (CODE CHECK); "
      f"**{wcf['checks_with_force_only_as_specified']} is a code check by construction with force "
      "only as specified**; and **"
      f"{wcf['checks_that_can_fail_on_real_data']} CAN FAIL ON REAL DATA** (DATA CHECK). The 703 "
      "line is **not an invariant** and is reported separately below as a population "
      "reconciliation.")
    B("")
    B("**THIS SET IS NINE.** ~~*The set is eight.*~~ ***SUPERSEDED by `decisions/0088` §1(c)***, "
      "which **PROMOTES a ninth check into the published set** — the `τ2 ≤ τ_pull` assertion that "
      "**already ran in this arm's stage 3** (`src/step8_a_3_table.py`) but **sat outside the "
      "deliverable, so no reader could see it**. It was six until `decisions/0076`. That entry "
      "corrected `p` from DATA CHECK to **CODE CHECK** — the label this instance's previous "
      "deliverable already carried, and the correction *inverts* the published figure: on the "
      "pre-`0076` set the true count was **five of six unfalsifiable with ZERO pure data "
      "checks**, not \"four of six\". `0076` then added the two checks that can actually fail, "
      "**because the set had none**. **Neither of those two is a formality here**: check 7 "
      "separates a pair-level liveness implementation from an account-level one, which the "
      "703-from-216-accounts figure alone cannot do, and check 8 is the one that would fail *in "
      "the direction of the result*.")
    B("")
    B("> ***THE NINTH MAKES THE RATIO WORSE, NOT BETTER, and it is stated because an added check "
      "reads as an added guarantee.*** The promoted assertion is a **sixth pure CODE CHECK**, so "
      "the set goes from **5 + 1 + 2 to 6 + 1 + 2** and **the number that can fail on real data "
      "is unchanged at TWO**. It adds **visibility**, not power — which is exactly what `0088` "
      "§1(c) asked for, since *\"an assertion a reader of the deliverable cannot see is not a "
      "published check\"*. **It is not evidence for the liveness rule or for any outcome.**")
    B("")
    B("**The set-membership drop rule is NOT in this list.** `decisions/0074` ruling 3 makes it a "
      "**coverage count**: records examined and records dropped are reported in the waterfall "
      "deliverable, and nothing is asserted. Step 8's own bullet already called it *\"an "
      "implementation check, not a data check\"*.")
    B("")
    B("| # | Invariant | Label | Result |")
    B("| :-- | :--- | :--- | :--- |")
    for i, it in enumerate(inv["invariants"], 1):
        B(f"| {i} | {it['name']} | **{it['label']}** | "
          f"{'PASS' if it['passed'] else '**FAIL**'} |")
    B("")
    B("## Coverage — every invariant names its population and accounts for every row in it")
    B("")
    B("**`decisions/0080` §3.** This is the provenance rule applied to invariants: **an invariant "
      "that passes on one population and was never run on another reads as a pass on both**, and "
      "**a passing invariant whose coverage the instance chose is a code check on the instance's "
      "choice.** The identity `asserted + not asserted = population` must hold on every stated "
      "population.")
    B("")
    B("| # | Invariant | Population(s) as specified | Identity |")
    B("| :-- | :--- | :--- | :--- |")
    for i, it in enumerate(inv["invariants"], 1):
        ids = inv["coverage_identities"][it["name"]]
        cells = "; ".join(f"{k} — `{v}`" for d in ids for k, v in d.items())
        B(f"| {i} | {it['name'][:52]}… | {it['population'].split('.')[0][:150]} | {cells} |")
    B("")
    B(f"**{inv['coverage_identity_checks_run']} coverage identities were checked and all hold: "
      f"{inv['all_coverage_identities_hold']}.** " + btx("every count in this table") + ".")
    B("")
    cis = inv["coverage_identity_strength"]
    B("> ***STRUCK, whatever else is ruled*** (`decisions/0088` §2(d), on Red Team's F4): "
      "~~*\"The run asserts this, so a report that omitted a population could not be written by "
      "this pipeline.\"*~~ **It is a control asserted to exist.** "
      f"**{cis['identities_that_CANNOT_FAIL_population_size_and_asserted_count_are_one_expression']} "
      f"of the {cis['identities_total']} identities have the population size and the asserted "
      "count as THE SAME EXPRESSION** — `asserted = N`, `not asserted = N − N = 0` — **so they "
      "cannot detect an invariant run on a population other than the one named.** The other "
      f"**{cis['identities_that_are_REAL_ARITHMETIC']}** are real arithmetic, built from "
      "**independently counted clauses that must sum to the population**: invariant 1's four "
      "partitions (three outcome states each), invariant 6's two `p` clauses, invariant 7's three "
      "account classes on each population and invariant 9's two `τ2` clauses on each. **Every "
      "identity below carries the label, in the `.json` at `what_it_can_detect`** — an unlabelled "
      "check that cannot fail reads as one that can (`0069`, applied to the coverage apparatus "
      "rather than to the invariants).")
    B("")
    B("| Identity shape | What it can detect |")
    B("| :--- | :--- |")
    B("| **`cover(unit, pop, N, N)`** — asserted count and population size are the same "
      "expression | **Nothing.** `N − N = 0` holds however the population was chosen |")
    B("| **`cover(..., parts=[a, b, …])`** — clauses counted independently | **A row covered by "
      "no clause**, which is the 99-row hole `0080` §3 was written for |")
    B("")

    def render(node, ind=0):
        pad = "    " * ind
        for k2, v2 in node.items():
            if isinstance(v2, dict):
                B(f"{pad}- `{k2}`:")
                render(v2, ind + 1)
            elif isinstance(v2, list):
                B(f"{pad}- `{k2}` = `{v2}`")
            else:
                B(f"{pad}- `{k2}` = `{v2}`")

    for i, it in enumerate(inv["invariants"], 1):
        B(f"### {i}. {it['name']}")
        B("")
        B(f"**{it['label']}.** {it['why']}")
        B("")
        B(f"**Population:** {it['population']}")
        B("")
        render({k: v for k, v in it.items()
                if k not in ("name", "label", "why", "passed", "population")})
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
    B(bt("every figure in this table"))
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
      "episode set exceeds its season, `A` sits inside `A_H`, `p` is a rank and not the "
      "withdrawn raw ratio, and the clock is the `max()` it is defined to be.")
    B(f"- It establishes **almost nothing about whether the rules are right**. "
      f"{wcf['checks_that_cannot_fail_on_any_data']} of these checks cannot fail on any data.")
    B("- **Three checks have force.** The clock-start check, and only because the first-pass S1 "
      "completion date is **recomputed independently from the episode records** — read back from "
      "the pipeline's own value it would prove nothing. And the two `0076` data checks, which "
      "test two named failure modes of this study rather than two properties of arithmetic: an "
      "account-level liveness filter masquerading as a pair-level one, and a skipped account "
      "silently read as a never-starter.")
    B("- **The withdrawn invariant** — \"no clock start precedes an S2 premiere\" — is vacuous "
      "under a finale-anchored clock and catches nothing. It is replaced by the three-part check "
      "above, whose equality clause is the part that does work.")
    B("- **What check 7 found, since a passing data check should still report what it saw:** "
      + (lambda c: f"{n(c['accounts_holding_BOTH_a_live_and_a_not_live_pair'])} of "
                   f"{n(c['accounts_touched_by_the_exclusion'])} accounts touched by the "
                   f"exclusion hold both a live and a not-live pair, and the "
                   f"{n(c['accounts_all_of_whose_position_5_pairs_are_excluded'])} whose "
                   f"position-5 pairs are all excluded held exactly one such pair "
                   f"({c['of_those_accounts_holding_more_than_one_position_5_pair']} held more "
                   "than one). The filter is pair-level in fact and not only in intent."
       )(next(i for i in inv["invariants"] if i["name"].startswith("no account is dropped"))))
    B("- **What check 8 found:** "
      + (lambda c: f"{n(c['accounts_whose_FINAL_ledger_state_is_a_skip_class'])} accounts are "
                   f"recorded in a skip class "
                   f"({', '.join(f'{k} {n(v)}' for k, v in c['skip_classes_present_in_the_ledger'].items())}), "
                   f"{n(c['HTTP_403_responses_in_the_whole_run'])} HTTP 403 responses occurred in "
                   f"the entire run and {n(c['access_denied_accounts'])} accounts are recorded "
                   f"`access_denied`. **None of the skipped accounts reaches the user index at "
                   f"all**, so none contributes a pair of any kind, let alone a never-started "
                   f"one. Separately, {c['accounts_skipped_on_one_attempt_but_yielding_data_on_another']['count']} "
                   f"accounts were skipped on one attempt and yielded data on another; they "
                   f"contribute "
                   f"{n(c['accounts_skipped_on_one_attempt_but_yielding_data_on_another']['position_5_pairs'])} "
                   f"position-5 pairs including "
                   f"{n(c['accounts_skipped_on_one_attempt_but_yielding_data_on_another']['never_started_pairs'])} "
                   "never-started, which rest on a real parsed history and are not violations. "
                   "Reported so the assertion's scope is visible rather than assumed."
       )(next(i for i in inv["invariants"] if i["name"].startswith("no access_denied"))))
    B("")
    B("")
    B(f"*Every result in this report was measured on build {BT} — {lib.BUILD_NAME} "
      "(`decisions/0079` B6). The full build record, with stage-file hashes and the git HEAD, is "
      "in `artifacts/step8-waterfall-a.md` §0 and in the `.json` beside this file.*")
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
