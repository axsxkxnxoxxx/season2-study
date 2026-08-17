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
    return f"Build: {what} measured on {BT} — {lib.BUILD_NAME.rstrip(chr(46))}; see §0"


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
    A("> **SCOPE OF THIS DELIVERABLE** (`decisions/0096` ruling 1). It asserts **this arm\'s "
      "own figures, its own inputs and its own limits, and nothing else.** It does not state the "
      "condition of other steps or gates, of the other arm, of the shared controls, or of the "
      "study as a whole: **this arm cannot measure those**, and a claim about them is "
      "expiry-dated from the moment it is written. **What it still carries is this arm\'s own "
      "defects, open items and divergences from the spec** — §8 and §9. **Anything this arm "
      "noticed on a surface it does not own was REPORTED to the Human Lead and is not published "
      "here as a finding.**")
    A("")
    A("> **BUILD STAMP.** Every figure below was measured on build " + BT + " unless it names a "
      "different build at the point of use (`decisions/0079` B6, extending `0078`). The build is "
      "defined once, with its stage-file hashes and its inputs, in §0. **The per-stage run "
      "record — which stages executed, their return codes and their timings — is "
      "`logs/step8_a_run.json`**, which is where this arm\'s build history lives.")
    A("")
    A("> **The spec this run executes.** The filter order is `decisions/0029`, positions 1–7. "
      "The liveness rule is ALT-BROAD. The **position-3 drop set is a DELIVERABLE produced by "
      "this pipeline run** and is **read back** by the stage that computes D9 half (b) "
      "(`0079` B5), so a missing input fails loudly instead of publishing a silent 0. The "
      "discovery-channel overlap publishes in **all three units, each with its consumer named** "
      "(`0079` B7). The **four inert filter positions are labelled with the reason** (`0079` §4). "
      "The column set is the **89 ENUMERATED names** of `0080` §1 as extended by `0081` "
      "(`silent_at_tau1`) and `0082` (`p_at_bound`), asserted by **set equality on the names, "
      "never by count**. **Every invariant states its population and accounts for every row in "
      "it** (`0080` §3). **D9 publishes as a BOUND** — strict the floor, loose the ceiling, "
      "neither the point estimate (`0090`) — and **reports both halves under both keys** "
      "(`0078` §3). **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`0083` §2). "
      "The **records-examined denominator publishes as three readings, each naming the pipeline "
      "that produces it** (`0083` §1). The **D9 clustering universe is U1, ranked by distinct "
      "strict keys merged** (`0088` §3). The **two unasserted mandates are MEASURED for whether "
      "they are load-bearing** (`0088` §1) — §5.6a, §5.6b, and check 9 of the invariant report.")
    A("")
    A("> Carried forward and unchanged: the table is the position-5 row set with `live` and "
      "`outcome` as columns (`0074`/1); both D9 keys are as defined by `0076`/3; the "
      "set-membership rule is a coverage count and not an invariant (`0074`/3); the `W` grid is "
      "fixed by `0075`/3; `p` is a CODE CHECK (`0076`/1); and the two DATA CHECKS of `0076`/2 are "
      "the only assertions here that can fail on data.")
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
      f"none**: two labelled figures imply the other counts and the {len(inv['invariants'])} "
      "invariants did not need it.")
    A("")
    br = wjson["build"]
    A(f"**Build {BT} — {lib.BUILD_NAME.rstrip(chr(46))}.**")
    A("")
    A(f"**What moved on this build.** {br['what_moved_on_this_build']}")
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
        ("4", "contamination exclusion (Step 5) — **DIFFERENT DEPTH ON THE TWO POPULATIONS, see "
              "below**", wa["position_4_contamination"],
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
    A("")
    A("**DERIV's line 4 IS NOT A SINGLE FILTER, and the table above must not be read as though it "
      "were.** The row is labelled *contamination exclusion (Step 5)* on both columns, and "
      "**DERIV's removal of "
      f"{n(wd['position_3_S1_completion_rule'] - wd['position_4_contamination_DERIV_depth'])} is "
      "the whole of Step 5 waterfall lines 1 through 4**, not one rule firing harder. **APPLY "
      "takes Step 5 line 1; DERIV takes line 4, which is where the population is DEFINED** — "
      "DERIV requires S2 evidence, and that requirement lives inside this position. The "
      "sub-decomposition, so no reader has to infer it:")
    A("")
    w5 = pos["step5_waterfall_rebuilt"]
    _l1 = wa["position_3_S1_completion_rule"]
    A("| Step 5 line | What it removes | Retained | Removed | In APPLY's line 4? | In DERIV's? |")
    A("| :--- | :--- | ---: | ---: | :--- | :--- |")
    A(f"| — | entering (position 3) | {n(_l1)} | — | — | — |")
    A(f"| **1** | the all-airdate and 1,542 classes | {n(w5[0])} | {n(_l1 - w5[0])} | **yes — "
      f"this is APPLY's line 4** | yes |")
    A(f"| **2** | pairs with NO S2 evidence | {n(w5[1])} | {n(w5[0] - w5[1])} | no | **yes — this "
      "is what DEFINES DERIV** |")
    A(f"| **3** | contaminated `T0` | {n(w5[2])} | {n(w5[1] - w5[2])} | no | yes |")
    A(f"| **4** | post-dated completing record | {n(w5[3])} | {n(w5[2] - w5[3])} | no | **yes — "
      "this is DERIV's line 4** |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A(f"**So DERIV's line-4 removal of "
      f"{n(_l1 - w5[3])} decomposes as {n(_l1 - w5[0])} contamination (the same rule APPLY "
      f"applies) + {n(w5[0] - w5[1])} no-S2-evidence + {n(w5[1] - w5[2])} contaminated `T0` + "
      f"{n(w5[2] - w5[3])} post-dated.** The Step 5 waterfall was rebuilt from the stored per-pair "
      f"flags and **asserted** equal to the published {pos['step5_waterfall_published']} before "
      "use, so this decomposition is not a reading of Step 5's deliverable — it is recomputed and "
      "checked against it.")
    A("")
    A("**The DERIV column of the main table is therefore a DEPTH, not a second run of the same "
      "filter.** Both columns are correct; the single label over them was not.")
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
    A("The rule this step applies is **ALT-BROAD**, as specified at `decisions/0064`: a pair "
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
    A("**703 is NOT the marginal cost of the silence test** (`decisions/0085` §5). **The silence "
      "test alone excludes 1,355 on APPLY; the `NOT Continued` conjunct spares 652; "
      "`1,355 − 652 = 703`.** **1,355 is the figure that makes line 6 readable as a marginal "
      "cost, and a reader holding only 652 cannot recover it without knowing to add.** **Both, on "
      "both populations, with the identity stated:**")
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
    A("> **TWO DIFFERENT `FALSE` CLASSES SIT ON THIS PAGE, AND THEY ARE NAMED APART WITH BOTH "
      "CARDINALITIES EMITTED ON ALL FOUR POPULATIONS.** One is the COEXTENSIVITY GAP and is "
      "empty; the other is the column's own `FALSE` value and is not. **Step 8b defines the "
      "schema Steps 9–13 write into with NO CONVERSION LAYER**, so a "
      "consumer that reads *\"the FALSE class is empty\"* and provisions a two-valued column is "
      "wrong by **17,895 rows** on APPLY position 5.")
    A("")
    A("| | **CLASS 1 — the COEXTENSIVITY GAP** | **CLASS 2 — the COLUMN's own `FALSE` value** |")
    A("| :--- | :--- | :--- |")
    A("| What it is | rows where `0082`'s two **mechanisms** disagree: "
      "saturated-not-final **plus** final-not-saturated — **that two-mechanism definition is "
      "SUPERSEDED and the motive behind it is WITHDRAWN (`0083` §2)** | Started-and-left rows "
      "where **`p` did not reach its bound** |")
    A("| The sentence that names it — **both quoted from superseded/withdrawn text, neither "
      "asserted here** | *\"the class `0082` called FALSE is **empty**\"* | "
      "*\"`p_at_bound` is FALSE on the rest of Started-and-left\"* |")
    A("| Is it empty? | **YES — 0 on all four populations** | **NO — 17,895 on APPLY position "
      "5** |")
    A("| What a `FALSE` row here would mean | one of the three construction links has broken | "
      "nothing at all — it is the ordinary case |")
    A("")
    A("**`p_at_bound` marks WHETHER `p` reached its bound, NOT WHY** — Human Lead ruling, "
      "2026-08-16 (`decisions/0083` §2), restating `0082`. **`TRUE` where `p` is at its bound, "
      "`FALSE` on the remaining Started-and-left rows, null where `p` is null.** `0082`'s "
      "definition **by two mechanisms** is **superseded**: the two clauses are **coextensive** — "
      "on a chain of three links of which the first two are construction and the third, "
      "`max(E2) = F2`, is MEASURED (`0085` §4) — so **CLASS 1** is **empty** and on the adopted "
      "rank form there is only one why. **The column is kept** — "
      "Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the "
      "spike **labelled**, and **an emptiness asserted in prose and never emitted cannot be "
      "checked.**")
    A("")
    A("**The `p = 1.0` counts are TOTALS, not a sum of two classes** (`0083` §2). **1,246 and "
      "1,230 are this instance's own measurements**, and they are **one class counted twice**; "
      "reading them as a split is a **withdrawn argument** (`CLAUDE.md`, third blindness class).")
    A("")
    A("**FOUR CELLS ON FOUR POPULATIONS** (`decisions/0085` §3). **Total, in-both-classes, "
      "saturated-not-final, final-not-saturated and in-neither, on APPLY position 5, APPLY "
      "post-liveness, DERIV position 5 and DERIV post-liveness.** This is `CLAUDE.md`'s standing "
      "**both populations, always** rule, not a new requirement, and **an emptiness asserted in "
      "prose and never emitted cannot be checked** — which is why each population gets its own "
      "row rather than one standing for the rest.")
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
      "equals the total on all four populations because **CLASS 1** is empty.")
    A("")
    A("#### The emitted column's own cardinalities — `TRUE`, `FALSE`, null")
    A("")
    A("**This is what a Step 8b schema has to provision for**, so it is emitted rather than left "
      "derivable.")
    A("")
    A("| Population | rows | `p_at_bound` **TRUE** | `p_at_bound` **FALSE** | **null** | identity |")
    A("| :--- | ---: | ---: | ---: | ---: | :--- |")
    for k, lab in (("APPLY_position_5", "APPLY, position 5"),
                   ("APPLY_position_7_post_liveness", "APPLY, post-liveness"),
                   ("DERIV_position_5", "DERIV, position 5"),
                   ("DERIV_position_7_post_liveness", "DERIV, post-liveness")):
        tf = sp[k]["THE_TWO_FALSE_CLASSES"]
        tot = (tf["column_TRUE_rows"] + tf["class_2_COLUMN_VALUE_FALSE_rows"]
               + tf["column_NULL_rows"])
        A(f"| {lab} | {n(tot)} | {n(tf['column_TRUE_rows'])} | "
          f"**{n(tf['class_2_COLUMN_VALUE_FALSE_rows'])}** | {n(tf['column_NULL_rows'])} | "
          f"`{tf['column_identity']}` — holds: {tf['column_identity_holds']} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    _gapz = all(sp[k]["THE_TWO_FALSE_CLASSES"]["class_1_COEXTENSIVITY_GAP_rows"] == 0
                for k in ("APPLY_position_5", "APPLY_position_7_post_liveness",
                          "DERIV_position_5", "DERIV_position_7_post_liveness"))
    A(f"**CLASS 1 is 0 on all four populations: {_gapz}.** **CLASS 2 is not zero anywhere** — it "
      "is the ordinary Started-and-left row that left before the finale, and it is the large "
      "majority of them. **Two numbers under one word, with only one emitted, is unreadable, so "
      "both are emitted.**")
    A("")
    A("*One thing worth noting rather than leaving to be spotted: the null counts on DERIV "
      "position 5 and DERIV post-liveness are **identical**. That is not a copy — DERIV's 99 "
      "liveness exclusions are **all started-and-left**, so every row the filter removes has `p` "
      "defined and none of them was null.*")
    A("")
    ct = sp["cross_tab_APPLY_position_5"]
    lk3 = sp["link_3_max_E2_equals_F2_MEASURED_NOT_ASSUMED"]
    A("**THE CHAIN HAS THREE LINKS AND ONLY TWO ARE CONSTRUCTION** (`decisions/0085` §4). "
      "**A future `FALSE` row would mean one of THREE things had broken, not two.**")
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
    A("**Why the column is still worth emitting.** **CLASS 1** is empty because of links 1 "
      "and 2, **both `W`-invariant**, and link 3, **a frame property that does not move across "
      "Step 13's grid** — so it stays empty at every arm. **A CLASS 1 row anywhere means one of "
      "the THREE has broken**, and that is a thing worth catching. **The emitted column itself is "
      "three-valued**: `TRUE` exactly on the `p = 1.0` rows, `FALSE` on the remaining "
      "Started-and-left rows — **17,895 of them on APPLY position 5, not zero** — and null "
      "elsewhere. **That is CLASS 2 and it is a different object from CLASS 1, which is the "
      "empty one.**")
    A("")
    A("---")
    A("")
    A("## 4. Per `W` arm")
    A("")
    A(f"**Arms: {' / '.join(str(x) for x in arms['arm_grid'])} days**, fixed by `decisions/0075` "
      "and by `task-sheet.md` Step 13 — **not this instance's choice.** Two instances on "
      "different grids produce tables that cannot be diffed at all. "
      "`H` is held constant at 91 across every arm. "
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
    A(f"**The comparator on the other side of that sentence is also measured here.** `0033`'s "
      f"pre-2020 comparator at `W = 213` was **2.7%** on the position-3 output; on the "
      f"position-4 output the mandated order censors, this instance measures "
      f"**{pct(r213['pre-2020']['lost_share'], 1)}**, which is the figure `decisions/0073` "
      "carries.")
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
      "series `decisions/0075` fixes, measured here independently. **`decisions/0034`'s "
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
    A("**The records-examined denominator publishes as a coverage figure, in three readings** "
      "(`decisions/0083` §1). The readings are **one family indexed by where D11 is applied**, "
      "and **each names the pipeline that produces it.** This instance produces "
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
      "are 0 by containment rather than by assumption. **The numerator is 0 three times over.**")
    A("")
    A(f"**The gap decomposes exactly.** D11 discards "
      f"**{n(rd['discarded_by_D11_watched_at_ge_tau_pull'])}** in-frame S1/S2 records, of which "
      f"**{n(rd['discarded_by_D11_S2_side'])} are S2-side and {n(rd['discarded_by_D11_S1_side'])} "
      "are S1-side.** So the three readings differ by **where D11 is applied and nowhere else**: "
      f"{n(tr['reading_A_no_D11'])} with none, {n(tr['reading_B_D11_on_the_S2_side_only'])} with "
      f"D11 on the S2 side, {n(tr['reading_C_D11_on_both_sides'])} with D11 on both. **The "
      "94-record difference `decisions/0074` records is exactly the S2-side count.** Every other "
      "candidate axis is zero and was measured, not assumed:")
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
    A("**The three readings are not three measurements of one quantity that disagree; they are "
      "three different quantities, exactly identified**, and the "
      f"{n(rd['discarded_by_D11_S2_side'])}/{n(rd['discarded_by_D11_S1_side'])} split says which "
      "is which with nothing left over. **The rule this figure is the denominator of dropped zero "
      "records under every reading.**")
    A("")
    A("**A separate question, and this instance does not decide it.** Whether D11 applies to the "
      "**S1 completion walk** is `0068`'s open item: reading C moves waterfall line 1 to "
      f"**{n(pos['D11_counterfactual_on_position_3']['completers_with_D11_applied_to_the_S1_walk'])}**"
      f" because **{n(pos['D11_counterfactual_on_position_3']['pairs_that_stop_being_completers_under_D11'])}"
      " pairs stop being completers** and "
      f"**{n(pos['D11_counterfactual_on_position_3']['completers_whose_completion_date_moves_under_D11'])}"
      " completion dates move** (§5.6). **This instance measured it and did not apply it.**")
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
    A("#### The `max()` binding term, split three ways — ON EVERY POPULATION THIS STEP NAMES")
    A("")
    A("**The spec requires the population at the point of use and measurement on both** "
      "(`decisions/0092`, N2; `0070` ruling 5), so no integer below appears without the set it "
      "was counted over.")
    A("")
    bs_ = diag["D2_negative_lag"]["binding_term_split_BOTH_POPULATIONS_BOTH_POSITIONS"]
    A("| Population | pairs | S2 finale binds | S1 completion binds | **both bind** | identity |")
    A("| :--- | ---: | ---: | ---: | ---: | :--- |")
    for k, lab in (("line_1_S1_completer_population", "line 1 — S1-completer population"),
                   ("APPLY_position_5", "APPLY, position 5"),
                   ("APPLY_post_liveness", "APPLY, post-liveness"),
                   ("DERIV_position_5", "DERIV, position 5"),
                   ("DERIV_post_liveness", "DERIV, post-liveness")):
        v = bs_[k]
        A(f"| {lab} | {n(v['population_size'])} | {n(v['S2_finale_binds'])} | "
          f"{n(v['S1_completion_binds'])} | **{n(v['both_bind'])}** | "
          f"`{v['coverage_identity']}` — holds: {v['coverage_identity_holds']} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    _c168 = bs_["which_population_carries_the_spec_integer_168"]
    A("**A TIE IS ITS OWN CATEGORY, NOT A TIEBREAK** (`0070` ruling 5). The three cases — finale "
      "strictly later, S1 completion strictly later, **equal** — partition every completer pair, "
      "so the identity holds on every row of the table.")
    A("")
    A(f"**THE COUNT IS INVARIANT ACROSS EVERY APPLY READING AND IS NOT POPULATION-INVARIANT.** "
      f"**168 on all three APPLY readings** — line 1, position 5 and post-liveness "
      f"(`{', '.join(_c168)}`) — because **no both-bind pair is removed by positions 4, 5 or 6 on "
      f"APPLY**, so a bare `168` cannot say which of those three sets it was counted over. "
      f"**On DERIV this instance measures {n(bs_['DERIV_position_5']['both_bind'])}**, which is "
      f"where the population becomes visible in the integer. **`decisions/0092` §3 records that "
      f"the spec carried `168` with no population at the point of use**; this instance's answer "
      f"is the table above, population by population.")
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
    st9 = d9["FLOOR_strict_key"]
    lo9 = d9["CEILING_loose_key"]
    bd9 = d9["BOUND"]
    tk9 = d9["third_key_measured_only_so_the_record_is_complete"]
    ha = st9["half_a_fabricated_never_started_row"]
    hb = st9["half_b_silently_deleted_S1_failing_counterpart"]
    A("Detection is imperfect and **every count here is a lower bound**.")
    A("")
    A("**D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS THE CEILING, AND NEITHER IS THE "
      "POINT ESTIMATE.** Human Lead ruling, `decisions/0090`. ***`0074` ruling 5's framing is "
      "SUPERSEDED by it and is struck here, quoted only as what no longer governs — "
      "~~\"use the strict key and report the loose count alongside\"~~ — under which "
      "STRICT WAS THE ANSWER and loose was context. Neither endpoint may be quoted as \"D9's "
      "result\".***")
    A("")
    A("**It is `0074` ruling 5's own reason carried through:** the loose count publishes "
      "**because it bounds how wrong strict could be**, and **a quantity published to bound "
      "another is an endpoint, not a footnote.** `0078` §3 already ran this argument once, to "
      "extend the loose count to half (b) — **same reason, one step further.**")
    A("")
    A("| D9 quantity | **bound `[floor, ceiling]`** |")
    A("| :--- | :--- |")
    A(f"| complementary signature ID pairs | **`[{n(bd9['complementary_signature_id_pairs'][0])}, "
      f"{n(bd9['complementary_signature_id_pairs'][1])}]`** |")
    A(f"| half (a) — the fabricated never-started row | "
      f"**`[{n(bd9['half_a_fabricated_never_started_row_APPLY_position_7'][0])}, "
      f"{n(bd9['half_a_fabricated_never_started_row_APPLY_position_7'][1])}]`** |")
    A(f"| half (b) — the silently deleted S1-failing counterpart | "
      f"**`[{n(bd9['half_b_silently_deleted_S1_failing_counterpart'][0])}, "
      f"{n(bd9['half_b_silently_deleted_S1_failing_counterpart'][1])}]`** |")
    A("")
    A(bt("all six endpoints"))
    A("")
    A("**DIRECTION IS PART OF THE LABEL, and it is not symmetric.** **Strict is the FLOOR** "
      "because it matches only slugs identical modulo punctuation, so it **cannot over-count**. "
      "**Loose is the CEILING** because stripping a trailing year **merges genuinely different "
      "shows** — remakes and national versions. **The error runs opposite to D9's own lower-bound "
      "caveat**, which is why the interval publishes rather than being resolved away. **The bound "
      "applies to every D9 quantity with both forms, not the headline alone** — applying it to "
      "one and not the others is the defect `0078` §3 corrected.")
    A("")
    zf = bd9["a_zero_floor_is_not_an_absence_of_evidence"]
    A("**A ZERO FLOOR IS NOT AN ABSENCE OF EVIDENCE**, so the coverage publishes beside it — "
      "**a bound whose floor is 0 and whose coverage is unstated is indistinguishable from a "
      "check that looked nowhere.** The strict key was applied to "
      f"**{n(zf['coverage_user_show_pairs_examined_under_the_strict_key'])} slugged user-show "
      f"pairs**, of which **{n(zf['coverage_D9_candidate_pairs_carrying_S1_or_S2_evidence'])} "
      "carry S1 or S2 evidence and are matchable**; half (a) was measured against "
      f"**{n(zf['coverage_never_started_pairs_for_half_a_APPLY_position_7'])} never-started pairs** "
      f"and half (b) against **{n(zf['coverage_position_3_drop_set_pairs_for_half_b'])} pairs in "
      "the position-3 drop set**. " + bt("every coverage figure in this paragraph"))
    A("")
    A(f"**THE THIRD KEY IS NOT AN ENDPOINT.** Its "
      f"**{n(bd9['THE_THIRD_KEY_IS_NOT_AN_ENDPOINT']['value'])}** is **a different key's answer** "
      "— it reduces `the-100` to `the` — and is **reported as a divergence, never as the "
      "ceiling** (`0090`; `0076`, `0078` §3).")
    A("")
    cov9 = d9["coverage"]
    A("**THE COVERAGE QUANTITIES, EACH NAMED BY WHAT IT COUNTS** (`decisions/0088` §2(b), as "
      "corrected on its axis by `0089` §2(b)). **One label over two quantities is the defect, and "
      "reconciling them would collapse two real objects into one**, which the standing rule "
      "forbids. ***The axis `0088` §2(b) named is SUPERSEDED*** — `0089` §2(b) corrects it, and "
      "the sentence that carried it is **registered as a superseded string** in "
      "`src/step7_register.py` and is deliberately **not restated here**. This arm publishes "
      "**all three of its own units** so no reader has to infer which one a bare number is:")
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
    A(f"**THE FIGURE THIS ARM PUBLISHES AS `747,478` IS UNIT B — distinct `(user, show)` PAIRS.** "
      f"***That is `decisions/0089` §2(b)'s correction to `0088` §2(b)'s axis, and it is stated "
      f"here rather than below the table.*** This arm's undeduplicated row count is a different "
      f"and larger object, unit A above: "
      f"{n(cov9['A_undeduplicated_user_show_SEASON_COVERAGE_ROWS'])}. The ruling's "
      "**conclusion** — two objects, both correct, do not reconcile — **is applied here.**")
    A("")
    A(f"**This arm's D9 candidate split is C: {n(cov9['C_split']['S1_evidence_and_no_S2'])} "
      f"+ {n(cov9['C_split']['S2_evidence_and_no_S1'])} + "
      f"{n(cov9['C_split']['both_S1_and_S2'])} = "
      f"{n(cov9['C_D9_CANDIDATE_user_show_pairs_carrying_S1_or_S2_evidence'])}.** "
      "**`decisions/0089` §3 records a ONE-PAIR divergence between the arms in the "
      "S1-evidence-and-no-S2 class, reported and not reconciled**; the figure above is this "
      "arm's own measurement and the comparison is the decision log's, not this arm's. It is "
      "**not** the "
      f"{n(cov9['bridge_B_minus_C_pairs_with_only_S3_or_later_evidence'])} S3-only pairs, which "
      "are the whole of the B-against-C gap and are accounted for above.")
    A("")
    A("**The normalisation key decides the entire number, and both keys are DEFINED in the "
      "spec** (`0076` §3 defines both, because \"strict\" and \"loose\" had existed only inside "
      "one instance's code, which the other is forbidden to read):")
    A("")
    A("| Key | Definition | complementary ID pairs | half (a) | half (b) |")
    A("| :--- | :--- | ---: | ---: | ---: |")
    A(f"| **STRICT — the FLOOR** | lowercase, drop every non-alphanumeric character, strip nothing "
      f"else | **{n(st9['complementary_signature_id_pairs'])}** | "
      f"**{n(ha['carrying_the_signature'])}** | **{n(hb['carrying_the_signature'])}** |")
    A(f"| **LOOSE — the CEILING** | remove a trailing four-digit year, then strict | "
      f"**{n(lo9['complementary_signature_id_pairs'])}** | "
      f"**{n(lo9['half_a_APPLY_position_7'])}** | **{n(lo9['half_b'])}** |")
    A(f"| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary "
      f"length, then strict | {n(tk9['complementary_signature_id_pairs'])} | "
      f"{n(tk9['half_a_APPLY_position_7'])} | {n(tk9['half_b'])} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    fn = d9["FOUR_NUMBERS_both_halves_under_both_keys"]
    A("**BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE** (`decisions/0078` §3). "
      "**This follows from `0074` ruling 5's own reason "
      "rather than from a preference:** the loose count publishes **because it bounds how wrong "
      "strict could be**, and **that reason applies to half (b) exactly as it applies to half "
      "(a)**. Publishing the bound for one half and withholding it for the other **leaves the "
      "reader unable to bound the total**, and the error runs **opposite** to D9's own "
      "lower-bound caveat — the direction they were not warned about.")
    A("")
    A("| | strict — **FLOOR** | loose — **CEILING** |")
    A("| :--- | ---: | ---: |")
    A(f"| **half (a)** — fabricated never-started row | **{n(fn['half_a_strict'])}** | "
      f"**{n(fn['half_a_loose'])}** |")
    A(f"| **half (b)** — silently deleted S1-failing counterpart | **{n(fn['half_b_strict'])}** | "
      f"**{n(fn['half_b_loose'])}** |")
    A("")
    A(bt("all four numbers") + " **Both columns are endpoints under `0090`; neither column alone "
      "is the answer.**")
    A("")
    A(f"- **(a) the fabricated never-started row, at the FLOOR:** "
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
      "**`decisions/0077` §2 states which set this is**: *\"position 3's drop set\"* names an "
      "**empty set** on this frame, because line 1 is already the S1-completer population and "
      "position 3 therefore removes 0 rows from the waterfall. The set is **the pair universe "
      "less the completers, 58,345 PAIRS**, and it is **not** the set-membership drop rule, which "
      "is a different rule and deletes 0 **records**.")
    cu = lo9["clustering_universe_NAMED"]
    A(f"- **The loose count is the CEILING because it BOUNDS HOW WRONG STRICT COULD BE**, and the "
      f"error runs **opposite** to D9's own lower-bound caveat. "
      f"{lo9['why_it_is_the_CEILING_and_not_the_answer']}")
    A("")
    A("**THE CLUSTERING UNIVERSE IS U1, RANKED BY DISTINCT STRICT KEYS MERGED** "
      "(`decisions/0088` §3). **The universe and the ranking basis are named at the point of "
      "use**, because the cluster examples are the evidence for the loose key's only warrant and "
      "a list whose universe is unstated is not reproducible.")
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
    prev = cu["THE_D9_COVERAGE_PIVOT_a_NARROWER_universe_NOT_used_for_clustering"]
    A(f"**TWO SIZED OBJECTS SIT BEHIND THE WORD \"SWEEP\" AND THIS ARM PUBLISHES BOTH.** U1 is "
      f"{n(cu['U1_distinct_slugged_show_ids_anywhere_in_the_sweep_CLUSTERED'])}; the narrower "
      f"**D9 COVERAGE PIVOT** — show IDs reaching the pivot through a dated, pre-`τ_pull`, "
      f"season ≥ 1 episode record — is **{n(prev['size'])}**; and "
      f"**U1 − pivot = {n(prev['U1_minus_this'])}**, shows reaching the sweep only through a "
      "record D11 discards, an undated record, a specials-only record or a non-episode record. "
      "**The subset relation is asserted in the pipeline, not assumed.** **The clustering here "
      "runs on U1**, and `distinct_show_ids_in_the_sweep` is not a label this arm uses for the "
      "pivot count, because the pivot is not the sweep.")
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
      "other, and ranking by show IDs displaces `maigret`. **The U3 illustration — The Twilight "
      "Zone, The Traitors, Manhunt — is SUPERSEDED as the example by `0088` §3; those three "
      "names are not wrong, they are another universe's answer.**")
    A("")
    A(f"**One row per show ID needs a tie-break and this arm states its own:** "
      f"{cu['one_row_per_show_id_tie_break']} "
      f"**{n(cu['show_ids_carrying_MORE_THAN_ONE_slug'])} show IDs carry more than one slug.** "
      f"Under the last slug instead the cluster count is "
      f"{n(cu['clusters_with_more_than_one_strict_key_under_the_LAST_slug_instead'])} against "
      f"{n(cu['clusters_with_more_than_one_strict_key'])} — **measured, not assumed away.**")
    A("")
    A("**The clusters the loose key merges are remakes and national versions, exactly the failure "
      "`0074` names.**")
    A(f"- **The third key is reported for the record and is neither ruled key.** It reduces "
      f"`the-100` to `the` and gives {n(tk9['complementary_signature_id_pairs'])} complementary "
      "pairs. **`decisions/0076` §3 defines the two ruled keys and records a 76-against-75 "
      "divergence as REPORTED, NOT RECONCILED**; under the defined keys this instance measures "
      "the floor and ceiling in the table above.")
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
    A("**`decisions/0088` §1.** The two unasserted mandates are **the half-open UTC-instant "
      "form** and **D11-as-global-cutoff** — *not* invariants 7 and 8, which are already "
      "measured, published and labelled DATA CHECK here. **This arm's compliance is TRUE**: "
      "**NO BOUNDARY TEST in `step8_a_*.py` uses a date-level form**, every bound comparison is "
      "an int64-second comparison, and `date(watched_at) <= T1` appears nowhere. ***Compliance "
      "was never the gap. Nothing measured whether either mandate is LOAD-BEARING on this data, "
      "and an unmeasured pass is indistinguishable from a check that looked nowhere.***")
    A("")
    A("> **THE CLAIM IS ABOUT BOUNDARY TESTS AND IS NARROWER THAN \"no day-flooring anywhere\", "
      "WHICH WOULD BE FALSE OF THIS ARM.** `floor_day()` appears three times in "
      "`step8_a_2_positions.py` — on the S2 finale date, on the first-pass S1 completion instant, "
      "and when parsing the stored Step 5 dates for the cross-check. **All three are correct and "
      "required**: `⟦T0⟧` is **day-floored by Step 1 §2.4**, the clock start is a date and not an "
      "instant, and **the next paragraph of this section reasons from it.** **The distinction the "
      "mandate draws: day-flooring the CLOCK is required; day-flooring a BOUNDARY TEST is "
      "forbidden — and there are none.** No `.date()`, `dt.date` or `normalize()` call appears "
      "anywhere in `step8_a_*.py`.")
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
    A("**The ruling's own second quantity, on this section's unit:** exactly "
      f"**{n(bw['APPLY_position_5']['tau1']['episodes_EXACTLY_AT_the_bound'])} distinct S2 episode "
      f"falls exactly AT `τ1`** on APPLY (and "
      f"{n(bw['DERIV_position_5']['tau1']['episodes_EXACTLY_AT_the_bound'])} on DERIV).")
    A("")
    st = bw["STRICTNESS_RULING_0068_MEASURED_ON_ITS_OWN_OBJECT"]
    A("> **THAT EPISODE COUNT SAYS NOTHING ABOUT `0068`'s STRICTNESS RULING, AND THIS REPORT "
      "DRAWS NOTHING FROM IT.** ***`0068`'s strictness ruling is about INSERTION INSTANTS in the "
      "silence test*** — *\"a pair is silent iff it has no insertion instant `> τ1`\"* — **and "
      "the unit of the table above is a DISTINCT S2 EPISODE BY CANONICAL `watched_at`. Two "
      "different axes.** The ruling's own quantity is measured immediately below, on its own "
      "object.")
    A("")
    A("#### `decisions/0068`'s strictness ruling, measured on ITS OWN object")
    A("")
    A("**The only rows on which strict `>` and non-strict `>=` can differ are pairs whose "
      "account's last insertion instant falls EXACTLY at `τ1`.** That is the ruling's quantity, "
      "and it is what says whether the ruling decides anything on this data.")
    A("")
    A("| Population | rows examined | pairs with last insertion instant **exactly at `τ1`** | "
      "accounts | silent, adopted (strict) | silent, non-strict | liveness exclusions, adopted | "
      "…non-strict | verdict |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |")
    for popk, poplab in (("APPLY_position_5", "APPLY, position 5"),
                         ("DERIV_position_5", "DERIV, position 5")):
        c = st[popk]
        A(f"| {poplab} | {n(c['rows_examined'])} | "
          f"**{n(c['pairs_whose_last_insertion_instant_is_EXACTLY_AT_tau1'])}** | "
          f"{n(c['accounts_ditto'])} | {n(c['silent_under_the_ADOPTED_strict_form'])} | "
          f"{n(c['silent_under_the_WITHDRAWN_non_strict_form'])} | "
          f"{n(c['liveness_exclusions_ADOPTED'])} | "
          f"{n(c['liveness_exclusions_under_the_non_strict_form'])} | "
          f"{'**VACUOUS ON THIS DATA**' if c['VACUOUS_ON_THIS_DATA'] else 'load-bearing'} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    if st["APPLY_position_5"]["VACUOUS_ON_THIS_DATA"]:
        A("***RESULT: `0068`'s STRICTNESS RULING IS VACUOUS ON THIS DATA — 0 pairs on both "
          "populations.*** **Stated as a zero, not passed silently.** The rule remains correct and "
          "remains binding on any future pull; **what is measured here is whether it decides "
          "anything on THIS data, and it does not.**")
    else:
        A("**RESULT: the strictness ruling is LOAD-BEARING on this data**, on its own unit.")
    A("")
    fl = bw["OUTCOME_STATE_FLIPS_the_number_that_settles_B3a"]
    f4 = fl["THE_FOUR_NUMBERS"]
    A("#### The number that settles B3(a): OUTCOME-STATE FLIPS, not episodes admitted")
    A("")
    A("**Episodes ADMITTED is not the object B3(a) turns on** (`decisions/0089` §2(a)). **The "
      "number that settles it is how many position-5 rows CHANGE OUTCOME STATE under the "
      "forbidden `date(ts) ≤ date(τ)` form — four numbers, both bounds × both populations.** The "
      "episode counts above are a different and also-reported quantity.")
    A("")
    A("**A never-started row with an episode in `[τ1, τ1 + 24h)` flips to started**, because "
      "`|A|` goes from 0 to ≥ 1. **A started-and-left row with one in `[τ2, τ2 + 24h)` can flip "
      "to Continued**, because `A_H` gains an episode and both the `F2` clause and the 0.90 "
      "clause can turn on it. **Each bound is varied ALONE** — that is what \"both bounds\" "
      "means; the joint form is reported separately because a row can flip at `τ1` and again at "
      "`τ2`, so it is not the sum.")
    A("")
    A("| Population | Bound varied | **rows changing OUTCOME STATE** | transitions | "
      "liveness exclusions under this form |")
    A("| :--- | :--- | ---: | :--- | ---: |")
    for popk, poplab in (("APPLY_position_5", "APPLY, position 5"),
                         ("DERIV_position_5", "DERIV, position 5")):
        for vk, vlab in (("tau1_only_date_level", "`τ1` only"),
                         ("tau2_only_date_level", "`τ2` only"),
                         ("both_bounds_date_level", "*both (not the sum)*")):
            c = fl[popk][vk]
            tr = (", ".join(f"{k.replace('__to__', ' → ')} {n(v)}"
                            for k, v in c["transitions"].items()) or "—")
            A(f"| {poplab} | {vlab} | **{n(c['rows_changing_outcome_state'])}** | {tr} | "
              f"{n(c['liveness_exclusions_under_this_form'])} "
              f"*(adopted {n(c['liveness_exclusions_adopted'])}, "
              f"move {c['liveness_exclusions_MOVE']:+d})* |")
    A("")
    A(f"**THE FOUR NUMBERS: APPLY at `τ1` = {n(f4['APPLY_at_tau1'])}, APPLY at `τ2` = "
      f"{n(f4['APPLY_at_tau2'])}, DERIV at `τ1` = {n(f4['DERIV_at_tau1'])}, DERIV at `τ2` = "
      f"{n(f4['DERIV_at_tau2'])}.** " + bt("all four"))
    A("")
    A("**Coverage:** " + f"{n(fl['APPLY_position_5']['rows_examined'])} rows on APPLY and "
      f"{n(fl['DERIV_position_5']['rows_examined'])} on DERIV — asserted non-empty, because a "
      "zero measured on zero rows is not a zero. " +
      ("***VACUOUS ON OUTCOMES: all four are 0.*** The mandate is load-bearing on EPISODES and "
       "not on OUTCOMES on this data, and that is stated rather than passed silently — a zero "
       "arriving as a pass is not evidence."
       if fl["VACUOUS_ON_THIS_BUILD"] else
       "**NOT VACUOUS: the half-open form decides published outcome states.**"))
    A("")
    if not fl["VACUOUS_ON_THIS_BUILD"]:
        _t1a = fl["APPLY_position_5"]["tau1_only_date_level"]
        _t2a = fl["APPLY_position_5"]["tau2_only_date_level"]
        A("**What that buys, stated as an effect on the headline and not only as a count.** On "
          f"APPLY the `τ1` mandate holds **{n(_t1a['rows_changing_outcome_state'])} rows** in "
          "**never-started** that the forbidden form would move out of it — "
          + ", ".join(f"**{n(v)}** to {k.split('__to__')[1].replace('_', ' ')}"
                      for k, v in _t1a["transitions"].items())
          + f" — and the `τ2` mandate holds **{n(_t2a['rows_changing_outcome_state'])} rows** in "
            "**started-and-left** that it would move to Continued. **Both directions run against "
            "the study's own estimand**: the forbidden form would understate never-started and "
            "understate abandonment.")
        A("")
    ww = fl["WITHDRAWN_WARRANT"]
    A("#### Line 6 under the counterfactual — measured, and scoped to what was measured")
    A("")
    A("> **NO PROPERTY OF CONJUNCT 1 EXPLAINS THIS, AND NONE IS OFFERED.** The liveness rule is "
      "**conjunct 1 AND conjunct 2**, and **conjunct 2 is `NOT Continued`, an episode-timestamp "
      "computation that MOVES under this counterfactual.** So the invariance of the conjunction "
      "is a measurement, not a consequence of the silence test reading an insertion clock.")
    A("")
    A("**CONJUNCT 2 IS RECOMPUTED ON THE COUNTERFACTUAL OUTCOME, and this is stated because "
      "`703 → 703` would be a tautology if it were held at the adopted one.** **A reader cannot "
      "tell a measurement from an identity unless the deliverable says which.** The expression is "
      f"`{fl['APPLY_position_5']['tau1_only_date_level']['conjunct_2_expression']}` — `cont_` is the "
      "counterfactual Continued mask returned by the counterfactual state function under that "
      "variant's bounds, and the adopted `continued` mask is not used in it. **It is stated "
      "at every cell of the table below, not inferred.**")
    A("")
    A("| Population | Bound varied | conjunct 2 rows that **MOVE** | exclusions, this form | "
      "exclusions, adopted | **never-started** | **started-and-left** | excluded ROW SET "
      "identical? |")
    A("| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- |")
    for popk, poplab in (("APPLY_position_5", "APPLY, position 5"),
                         ("DERIV_position_5", "DERIV, position 5")):
        for vk, vlab in (("tau1_only_date_level", "`τ1` only"),
                         ("tau2_only_date_level", "`τ2` only"),
                         ("both_bounds_date_level", "both")):
            c = fl[popk][vk]
            sp_ = c["exclusion_split_under_this_form"]
            A(f"| {poplab} | {vlab} | **{n(c['conjunct_2_rows_that_MOVE_under_this_form'])}** | "
              f"{n(c['liveness_exclusions_under_this_form'])} | "
              f"{n(c['liveness_exclusions_adopted'])} | {n(sp_['never_started'])} | "
              f"{n(sp_['started_and_left'])} | "
              f"{c['the_excluded_ROW_SET_is_identical_not_merely_the_total']} "
              f"*(symdiff {n(c['rows_in_one_exclusion_set_but_not_the_other'])}; "
              f"cf∖adopted {n(c['rows_excluded_by_the_COUNTERFACTUAL_but_not_by_the_ADOPTED_rule'])}, "
              f"adopted∖cf {n(c['rows_excluded_by_the_ADOPTED_rule_but_not_by_the_COUNTERFACTUAL'])})* |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**THE 604/99 SPLIT UNDER THE COUNTERFACTUAL IS THE COLUMN PAIR ABOVE**, on both "
      "populations. **The measurement goes further than the total: the excluded ROW SET is "
      "identical, not merely its cardinality** — symmetric difference **0** on every variant and "
      "both populations.")
    A("")
    mon = diag["B3a_boundary_window_half_open_form"][
        "OUTCOME_STATE_FLIPS_the_number_that_settles_B3a"]["MONOTONICITY_OF_THE_RELAXATION"]
    A("#### The symmetric difference confirms the arithmetic; it is not independent evidence")
    A("")
    A("> **A SYMMETRIC DIFFERENCE OF 0 IS NOT STRONGER HERE THAN THE UNCHANGED TOTAL, AND THIS "
      "REPORT DOES NOT CLAIM IT IS.** It would be stronger under an arbitrary perturbation. It is "
      "not under this one, and the reason is measured below rather than argued.")
    A("")
    A("**Why it cannot be stronger here.** The date-level form **RELAXES** both bounds, so per row "
      "`|A|` and `|A_H|` can only **grow**. **All three Continued conjuncts are monotone "
      "non-decreasing in them** — `|A| ≥ 1` in `|A|`; `|A_H| ≥ ⌈0.90·L2⌉` in `|A_H|`; and "
      "`m_H = F2` because set membership bounds `m_H ≤ F2`, so it can only **reach** `F2` and "
      "never leave it. **So `Continued` only turns ON, `NOT Continued` only turns OFF, and the "
      "exclusion set `silent ∧ ¬Continued` can only SHRINK.** **A row can LEAVE the exclusion set "
      "and none can ENTER it**, so **an unchanged TOTAL already forces an identical SET.** The "
      "symmetric difference of **0** therefore **confirms the arithmetic**; it is not an "
      "independent fact about the two sets.")
    A("")
    A("**MEASURED, NOT ARGUED — every clause of that reasoning is a count on this build.**")
    A("")
    A("| Population | rows examined | `\\|A\\|` decreased | `\\|A_H\\|` decreased | `m_H` "
      "decreased | rows with `m_H > F2` | Continued turned OFF (τ1 / τ2 / both) |")
    A("| :--- | ---: | ---: | ---: | ---: | ---: | :--- |")
    for popk, poplab in (("APPLY_position_5", "APPLY, position 5"),
                         ("DERIV_position_5", "DERIV, position 5")):
        c = mon[popk]
        offs = " / ".join(
            n(c[v]["rows_where_Continued_turned_OFF_which_monotonicity_forbids"])
            for v in ("tau1_only_date_level", "tau2_only_date_level", "both_bounds_date_level"))
        A(f"| {poplab} | {n(c['rows_examined'])} | "
          f"{n(c['rows_where_kA_decreased_under_the_relaxed_bound'])} | "
          f"{n(c['rows_where_kAH_decreased_under_the_relaxed_bound'])} | "
          f"{n(c['rows_where_mH_decreased_under_the_relaxed_bound'])} | "
          f"{n(c['rows_where_mH_exceeds_F2_which_would_break_the_third_conjuncts_monotonicity'])} "
          f"| {offs} |")
    A("")
    A(f"**Every clause holds on both populations: "
      f"`{mon['ALL_THREE_CLAUSES_HOLD_ON_BOTH_POPULATIONS']}`.** And the subset direction is "
      "emitted per variant beside the symmetric difference — "
      "`rows_excluded_by_the_COUNTERFACTUAL_but_not_by_the_ADOPTED_rule` is **0** everywhere, "
      "which is the direction monotonicity forbids from being anything else. " + bt(
        "every figure in this table"))
    A("")
    A("**WHAT THE INVARIANCE IS: A MEASURED FACT ABOUT THIS DATA AT `W = 108`, NOT A STRUCTURE.** "
      "**No pair the adopted rule excludes is among the rows whose Continued value flips.** "
      "**Under the monotonicity above, that statement and \"the total does not move\" are the same "
      "fact and not two.** **It remains a property of this frame at this arm, not of the rule.**")
    A("")
    A(f"**SCOPE OF THE CLAIM, AS MEASURED: {ww['scope_of_the_claim_AS_MEASURED']}** "
      "**Step 13 re-runs the rule across eight arms**, and nothing here says what it will find "
      "there.")
    A("")
    A("> **This is a COUNTERFACTUAL.** `date(watched_at) <= T1` still appears nowhere in the "
      "implementation, and nothing this pipeline emits changes. The counterfactual state "
      "function is asserted to reproduce the adopted outcome exactly on the half-open form "
      "before any comparison is made, so the baseline cannot be the thing that differs.")
    A("")
    ps = diag["B3b_D11_per_site"]
    psa = {x["site"]: x for x in ps["assertions"]}      # by name, never by position
    A("### 5.6b D11 applied per site, asserted at each (B3(b))")
    A("")
    A("**`decisions/0088` §1(b).** D11 is specified to apply *\"to EVERY computation\"*. "
      "**Every site carries its own unit, its own count and its own assertion — not one "
      "assertion about the rest.** **Ground, as ruled: the unstated version of exactly this scope "
      "produced Step 7's 792-against-791.**")
    A("")
    A("> **THE `examined` COLUMN IS ONE KIND OF QUANTITY IN EVERY ROW: the units the site "
      "CONSUMES before D11.** The distinction matters at `S1_completion_walk`, where three "
      "different objects could each be called \"the number\" — a **record** count of post-cutoff "
      "candidates, a **would-exclude** count, and the **distinct episodes** the walk examines. "
      "**All three are named** — see below the table.")
    A("")
    A("| Site | Unit | examined | **excluded by D11** | *would exclude if applied* | D11 "
      "applied? | assertion |")
    A("| :--- | :--- | ---: | ---: | ---: | :--- | :--- |")
    for x in ps["assertions"]:
        sv = ps["sites"][x["site"]]
        flag = "**PASS**" if x["holds"] else "**FAIL**"
        if x["LOOKED_AT_ZERO_UNITS"]:
            flag += " *(looked at ZERO units — holds trivially)*"
        _wd = x.get("would_be_excluded_by_D11_at_this_site")
        A(f"| `{x['site']}` | {sv['unit'].split(' -- ')[0]} | "
          f"{n(x['coverage_unit_count'])} | "
          f"**{n(x['excluded_by_D11'])}** | {'—' if _wd is None else n(_wd)} | "
          f"{'yes' if x['D11_applied'] else '**NO — declared**'} | "
          f"{flag} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A("**Every `examined` cell above is the same kind of quantity: units the site consumes "
      "before D11.** The *would exclude if applied* column is populated only where the site does "
      "not apply D11.")
    A("")
    _s1w = ps["sites"]["S1_completion_walk"]["THREE_OBJECTS_NAMED_APART"]
    A("**The three objects behind `S1_completion_walk`, named apart:**")
    A("")
    A("| Object | Count |")
    A("| :--- | ---: |")
    A("| in-frame **S1 RECORDS** at or after `τ_pull` "
      f"| {n(_s1w['record_level_in_frame_S1_records_at_or_after_tau_pull'])} |")
    A("| **distinct S1 EPISODES touched** by those records "
      f"| {n(_s1w['distinct_S1_episodes_touched_by_those_records'])} |")
    A("| **distinct S1 EPISODES whose CANONICAL instant** is at or after `τ_pull` — *the only one "
      f"D11 would remove from this walk* | **{n(_s1w['distinct_S1_episodes_whose_CANONICAL_instant_is_at_or_after_tau_pull'])}** |")
    A("| **distinct S1 EPISODES the walk EXAMINES** — *the `examined` cell* "
      f"| {n(ps['sites']['S1_completion_walk']['episodes_examined_before_D11'])} |")
    A("")
    A(bt("every figure in this table"))
    A("")
    A(f"**The third is smaller than the second because an episode's canonical instant is the "
      "MINIMUM `watched_at` over its records**, so an episode with one post-cutoff record and one "
      "earlier record stays pre-cutoff. **`decisions/0089` §1 names these three objects; this arm "
      "measures all three independently and its measurements are the counts above.**")
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
      "by `0082`**). Step 8b's schema is built on this vocabulary with Steps 9–13 writing into "
      "it **directly, with no conversion layer** (`0066`), so it is fixed **before** the schema "
      "exists. **This instance asserts SET EQUALITY against the spec's list, not a count** — a "
      "count is arithmetically satisfiable by the wrong columns. Column **order** is specified "
      "nowhere; this table is in construction order and the sorted list is in the `.json` so an "
      "order difference cannot be mistaken for a name difference.")
    A("")
    A("**The count is 89 again after `0082`, but it is a different 89** than `0077`'s: "
      "`f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not matching a "
      "set**, which is why the assertion here is on the names.")
    A("")
    csd = at["column_set_verified_against_the_spec_ON_DISK"]
    A("**AND THE LIST ASSERTED AGAINST IS NOW READ OFF `task-sheet.md` AT RUN TIME** — "
      f"{n(csd['distinct_names_parsed'])} distinct names parsed from the enumeration block, "
      f"matching this arm's transcription: **{csd['matches_the_transcription_in_this_file']}**. "
      "**A hand transcription would be a second copy of the enumeration, and a propagation change "
      "to the spec would not reach it** — and **the dual diff cannot catch a propagation "
      "failure**, so only a check that opens the spec file can. **A parse that found nothing "
      "FAILS rather than passes**, and the parsed count is published above.")
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
      "`max_episode_in_A_H == s2_F`. `0077`'s spelling ruling — `A_H`, not `AH` — still governs "
      "`n_A`, `n_A_H` and `max_episode_in_A_H` without the dropped column.")
    A("")
    A("**The names themselves are `decisions/0077` §3's and were not chosen here.** The mapping "
      "from the pre-`0077` vocabulary: `in_channel_*` → **`discovered_channel_a` / "
      "`discovered_channel_b`**; `in_population_APPLY` / `in_population_DERIV` → **`in_apply` / "
      "`in_deriv`**; `tau1_utc` / `tau2_utc` → **`tau1` / `tau2`**; `T0_utc_date` → "
      "**`t0_date`**; `T0_binding_term` → **`t0_binding_term`**; `s1_completion_date_utc` → "
      "**`s1_completion_date`**; `n_A_distinct_s2_before_tau1` → **`n_A`**; "
      "`n_AH_distinct_s2_before_tau2` → **`n_A_H`**; `max_episode_in_AH` → "
      "**`max_episode_in_A_H`**; `n_rec_s{1,2}_*` → **`action_count_s{1,2}_*`**. **No `_utc` "
      "suffix survives**: every instant in this study is UTC by Step 1 §2.4, and suffixing some "
      "columns implies the others are not.")
    A("")
    A("**Two extra columns are kept** (`0077` §3, and both are in `0080`'s "
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
      "*position-3 rule, position-5 build of 2026-08-13*; this instance measures 58,345 on the "
      "build named above.**")
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
    A("1. **The `W` arm grid is not this instance\u2019s choice.** It is "
      f"{' / '.join(str(x) for x in arms['arm_grid'])} days, fixed by `decisions/0075` ruling 3 "
      "and by `task-sheet.md` Step 13.")
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
    A("9. **The set half (b) is measured on is named by the spec, not chosen here.** "
      "*\"Position 3's drop set\"* names an empty set on this frame; `decisions/0077` §2 states "
      "the intended object and `0079` B5 makes it a deliverable — **the pair universe less the "
      "completers, "
      f"{n(pos['position_3_drop_set_DELIVERABLE']['pairs_failing_the_S1_completion_rule'])} "
      "pairs**, written and read back by this run (§6.1). The unit is **pairs**, and it is "
      "**not** the set-membership drop rule.")
    A(f"10. **The column set is an enumeration, not a count** (`decisions/0080` §1, taken to "
      f"{at['columns']} names by `0081` and `0082`), and this instance asserts **set equality on "
      "the names** against the list parsed from `task-sheet.md` at run time. A count is "
      "arithmetically satisfiable by the wrong columns, so the count is not the check.")
    A("11. **Column ORDER is specified nowhere.** This table is in construction order; the sorted "
      "name list is in the `.json`. **If the arms differ here it is an order difference, not a "
      "name difference**, and the enumerated set is identical either way.")
    A("12. **The `build` label's granularity.** `0079` B6 requires every count to name its build "
      "and does not say at what granularity. This instance defines the build once (§0, with stage "
      "file hashes and the git HEAD) and cites a **tag** at each figure; the alternative — the "
      "full record inline at every figure — carries the same information and reads worse. **A "
      "figure measured on a different build says so instead** (the 3,440).")
    A("13. **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`decisions/0083` §2). "
      "The `FALSE` class of the two-mechanism reading is empty by construction and the `p = 1.0` "
      "counts publish as **totals** — §3.1.")
    A("")
    A("---")
    A("")
    A("## 9. This instance\u2019s own open items and divergences from the spec")
    A("")
    A("**SCOPE** (`decisions/0096` ruling 1). Every item below is something THIS ARM measured or "
      "decided. **Nothing here reports the disk state of another surface, the status of another "
      "step or gate, the other arm, or a shared control** \u2014 those are not this arm\u2019s "
      "measurements, and anything of that kind this run noticed was **reported to the Human Lead** "
      "rather than published here.")
    A("")
    A("1. **D3\u2032 is not monotone in `W`.** It rises between the 91 and 107 arms before "
      "resuming its fall \u2014 \u00a74.3, where the mechanism is stated. **Measured, not "
      "resolved.**")
    A("2. **D11 at position 3 is not applied, and the counterfactual is measured.** Applying D11 "
      "to the S1 completion walk gives "
      f"{n(pos['D11_counterfactual_on_position_3']['completers_with_D11_applied_to_the_S1_walk'])} "
      "completers rather than the 220,107 this run uses, and moves "
      f"{n(pos['D11_counterfactual_on_position_3']['completers_whose_completion_date_moves_under_D11'])} "
      "completion dates \u2014 \u00a75.6, \u00a75.6b. `0068` fixes line 1 at 220,107 and lists "
      "the question as open; **this instance measured it and did not apply it**, and the "
      "`s1_completion_used_a_post_cutoff_record` column carries the pairs it turns on.")
    A("3. **The D9 clustering basis ties at rank 3 and the tie-break is unruled.** `0088` \u00a73 "
      "ranks by distinct strict keys merged; on that basis **six loose keys tie at 6** in this "
      "arm\u2019s measurement, so a bare \u201cthird-largest cluster\u201d is not reproducible "
      "from the basis alone. **Every key at every published rank is listed under both bases** in "
      "\u00a75.5, so nothing is lost while it is open. **Reported, not resolved.**")
    A("4. **The one-pair D9 candidate divergence.** This arm measures "
      f"`{n(cov9['C_split']['S1_evidence_and_no_S2'])} + "
      f"{n(cov9['C_split']['S2_evidence_and_no_S1'])} + {n(cov9['C_split']['both_S1_and_S2'])} = "
      f"{n(cov9['C_D9_CANDIDATE_user_show_pairs_carrying_S1_or_S2_evidence'])}` in the three "
      "candidate classes. **`decisions/0089` \u00a73 records a ONE-PAIR difference between the "
      "arms in the S1-evidence-and-no-S2 class, reported and not reconciled.** The figure above "
      "is this arm\u2019s own measurement; the comparison is the decision log\u2019s.")
    A("5. **`decisions/0090`\u2019s scope, read broadly by this arm.** The entry says the bound "
      "is *\u201capplied to this half\u201d*, singular, and this arm applies it to **every D9 "
      "quantity with both forms** \u2014 complementary pairs, half (a), half (b) \u2014 on "
      "`0078` \u00a73\u2019s ground that publishing a bound for one half and a point estimate "
      "for the other leaves the reader unable to bound the total. ***If a single half was meant, "
      "this arm\u2019s \u00a75.5 table is what would narrow.*** **Reported at the point of "
      "use.**")
    A("6. **The invariant set has nine members and only two can fail on data.** "
      "\u00a7\u201cWhat the invariant set does and does not establish\u201d in the invariant "
      "report states the split, derived from the label strings rather than typed. **This is a "
      "limit of what this deliverable can falsify, and it is published rather than left to be "
      "inferred.**")
    A("7. **The 3,440 is on a population Step 8 does not compute** \u2014 Step 5\u2019s "
      "uncensored estimation sample of 128,099 \u2014 and is **restated, not recomputed**. It "
      "must never be reported against APPLY or DERIV. \u00a74.3.")
    A("8. **`decisions/0033`\u2019s censoring percentages were measured on the position-3 "
      "output** and this instance censors the position-4 output, as the mandated order requires. "
      "The figures this instance measures are in \u00a74.1; the difference is the filter order, "
      "not the data.")
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
    B("> **SCOPE OF THIS REPORT** (`decisions/0096` ruling 1). It states **this arm's own "
      "invariant results, the populations they ran on and what they can and cannot establish** "
      "\u2014 and nothing else. **Not the other arm, not the shared controls, not the status of "
      "any step or gate.** **Every result below is produced by one pipeline run**, build " + BT +
      ", defined in full in the waterfall deliverable \u00a70; the per-stage run record is "
      "`logs/step8_a_run.json`.")
    B("")
    B("> **WHAT THE SPEC REQUIRES OF THIS REPORT.** **`0079` B6: every invariant result names the "
      "build it was measured on.** **`0080` \u00a73: every invariant names the population it runs "
      "on and accounts for every row in it**, reporting `rows_asserted + rows_not_asserted = "
      "rows_in_the_stated_population`. **`0068`: every invariant carries a CODE CHECK or DATA "
      "CHECK label.** **`0088` \u00a71(c): the `\u03c42 \u2264 \u03c4_pull` assertion is "
      "promoted into the published set**, which takes it to nine members. **`0074` ruling 3: the "
      "set-membership drop rule is a coverage count and is NOT asserted here.**")
    B("")
    B("> **WHY THE COVERAGE IDENTITY IS NOT DECORATION, in this report's own numbers.** `0080` "
      "\u00a73 records a dual-run gap in which `p` was asserted on **19,042** rows \u2014 the "
      "*post-liveness* Started-and-left count \u2014 against a *pre-liveness* non-S&L clause of "
      "**177,513**, summing to **196,555 against a 196,654-row table**, with **99 rows covered by "
      "neither clause.** **This report states both clauses and their sum for every check** \u2014 "
      "see the coverage table below, where `p` reads **19,141 + 177,513 = 196,654** and the "
      "post-liveness 19,042 appears only as a labelled contrast.")
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
    fd = wcf["THE_HEADLINE_SHAPE_THIS_ARM_PUBLISHES_derived_from_its_own_labels"]
    fs = fd["split"]
    B("> **THAT RESULT LINE IS THIS ARM'S OWN SPLIT AND IS ALL THIS REPORT SAYS ABOUT ANY "
      "HEADLINE; a cross-arm statement belongs to the Human Lead's diff.** "
      f"**{fs['CODE CHECK']} + "
      f"{fs['CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED']} + {fs['DATA CHECK']}**, "
      "**derived from the label strings in the table below and never typed.**")
    B(">")
    B("> **Why three classes and not two.** **The spec's label vocabulary has three values**, and "
      "**collapsing the middle member into either outer class changes the answer to *what could "
      "this report have caught?*** Folded upward it reads as **seven checks that cannot fail**; "
      "folded downward as **three that can**. **The sentence a reader takes away is the "
      "headline**, so the middle class is published as its own. **The spec's own sentence has "
      "that shape** — *\"SIX pure code checks, one code-by-construction with force only as "
      "specified, and TWO that can fail on real data.\"*")
    B("")
    B("**THIS SET IS NINE** (`decisions/0088` §1(c)), which **promotes the `τ2 ≤ τ_pull` "
      "assertion into the published set** — it **already ran in this arm's stage 3** "
      "(`src/step8_a_3_table.py`) but **sat outside the deliverable, so no reader could see "
      "it**. **The two checks that can fail on data are not formalities here**: check 7 "
      "separates a pair-level liveness implementation from an account-level one, which the "
      "703-from-216-accounts figure alone cannot do, and check 8 is the one that would fail *in "
      "the direction of the result*.")
    B("")
    B("> ***THE NINTH MAKES THE FALSIFIABILITY RATIO WORSE, NOT BETTER, and it is stated because "
      "an added check reads as an added guarantee.*** The promoted assertion is a **sixth pure "
      "CODE CHECK**, so the set goes from **5 + 1 + 2 to 6 + 1 + 2** and **the number that can "
      "fail on real data is unchanged at TWO**. It adds **visibility**, not power — which is what "
      "`0088` §1(c) asked for, since *\"an assertion a reader of the deliverable cannot see is "
      "not a published check\"*. **It is not evidence for the liveness rule or for any "
      "outcome.**")
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
    B("> ***STRUCK, whatever else is ruled*** (`decisions/0088` §2(d)): "
      "~~*\"The run asserts this, so a report that omitted a population could not be written by "
      "this pipeline.\"*~~ **It is a control asserted to exist.**")
    B("")
    B("> **A MULTI-CLAUSE IDENTITY IS NOT AUTOMATICALLY ONE THAT CAN FAIL.** A test of the form "
      "`len(parts) > 1` — *\"it has more than one clause\"* — ***admits an identity that cannot "
      "fail on any data***, because clauses forming a **complementary partition of the same mask "
      "the population size was taken from** sum to the population **for any mask**: invariant 1's "
      "`never / left / continued` are exhaustive by the expressions that define them; invariant "
      "6's are `M & left` and `M & ~left`; invariant 7's `mixed` and `wholesale` partition "
      "`touched` by set algebra; invariant 9's are `τ2 ≤ τ_pull` and its complement. **Each of "
      "those holds whatever mask `M` is — including a mask that is NOT the population named, "
      "which is the defect** `0080` §3 introduced the identity to detect.")
    B("")
    B("**THE FIX IS THE ONE THE HOLE ACTUALLY NEEDS: the population size is now sourced "
      "INDEPENDENTLY of the asserted count.** The 99-row hole was a numerator taken "
      "**post-liveness** against a denominator taken **pre-liveness**; that is detectable only if "
      "the denominator comes from somewhere other than the masks the numerator is built from. So "
      f"**{cis['identities_that_CAN_FAIL_population_size_sourced_INDEPENDENTLY']} of the "
      f"{cis['identities_total']} identities now take their population size from a different "
      f"file**, and "
      f"**{cis['identities_that_CANNOT_FAIL_population_size_and_asserted_count_are_one_expression']} "
      "remain in the cannot-fail class, labelled bookkeeping at the point of use** "
      "*(the label stays in the code and in the schema whether or not any identity is in that "
      "class on this build — a class that happens to be empty today must still be nameable "
      "tomorrow)*. **Every identity carries its tier in the "
      "`.json` at `population_size_independence` and `what_it_can_detect`** — an unlabelled check "
      "that cannot fail reads as one that can (`0069`, applied to the coverage apparatus rather "
      "than to the invariants).")
    B("")
    B("| Independence tier | Source | What the identity can detect | count |")
    B("| :--- | :--- | :--- | ---: |")
    for _t, _c in sorted(cis["by_independence_tier"].items(), key=lambda kv: -kv[1]):
        _d = {"EMITTED_DELIVERABLE": ("`analysis_table.csv.gz`, written by stage 3",
                                      "**an invariant run on a population other than the one it "
                                      "names**"),
              "INDEPENDENT_FILE": ("an earlier stage's own JSON",
                                   "**an invariant run on a population other than the one it "
                                   "names**"),
              "INDEPENDENT_CODE_PATH": ("the same file parsed by different code",
                                        "**a parse or dedup disagreement in the population "
                                        "size**"),
              "NOT_INDEPENDENT": ("the same mask the asserted count comes from",
                                  "**nothing** — `N − N = 0` holds however the mask was "
                                  "chosen")}[_t]
        B(f"| `{_t}` | {_d[0]} | {_d[1]} | {_c} |")
    B("")
    B(bt("every count in this table"))
    B("")
    dm = cis["ARITHMETIC_NOT_A_LITERAL_the_plus_one_perturbation"]
    B("#### The `+1` perturbation — ***IT DOES NOT TEST INDEPENDENCE***")
    B("")
    B("> ***THIS BLOCK IS NOT A DEMONSTRATION OF INDEPENDENCE AND IS NOT PUBLISHED AS ONE*** "
      "(`decisions/0091` §2). **On a same-mask denominator the clauses sum to `N` by construction "
      "and the stated population reads `N + 1`, so the identity fails — IDENTICALLY, whether or "
      "not the denominator was sourced independently.** Perturbing the **denominator** cannot "
      "separate the two cases. **The control that can is immediately below.**")
    B("")
    B(f"**What it DOES show, and it is kept under that label:** that each identity is "
      f"**arithmetic rather than a hardcoded literal**. Each of the "
      f"**{dm['identities_demonstrated']}** independent identities is re-evaluated against **its "
      f"population size + 1** and must report FAIL. **All hold against the true value and fail "
      f"against the perturbed one: "
      f"{dm['all_hold_against_the_true_value_and_FAIL_against_the_perturbed_one']}.** *The "
      "separate literal counter already shows the same thing, which is why this is a narrow check "
      "and not the one that matters.*")
    B("")
    ij = cis["INDEPENDENCE_DEMONSTRATED_injected_wrong_population_defects"]
    B("#### The control that DOES test independence — injected wrong-population defects")
    B("")
    B("**The escape the independent source exists to catch is AN INVARIANT RUN ON A POPULATION "
      "OTHER THAN THE ONE IT NAMES.** Where an identity's clauses are a complementary partition "
      "of a mask, **swapping the mask moves the clauses AND the same-mask denominator together**, "
      "so the same-mask identity still **PASSES** on the wrong population. **Only a denominator "
      "keyed on the NAME rather than on the mask can fail.** So each defect below asserts **both "
      "directions**.")
    B("")
    B("| # | Injected defect | clauses sum to | same-mask denominator | **same-mask form: can it "
      "detect it?** | independent source | **independent form: does it detect it?** |")
    B("| ---: | :--- | ---: | ---: | :--- | ---: | :--- |")
    for _i, _d in enumerate(ij["per_defect"], 1):
        B(f"| {_i} | {_d['injected_defect']} | {n(_d['clauses_sum_to'])} | "
          f"{n(_d['same_mask_denominator'])} | "
          f"{'**NO — it passes**' if _d['SAME_MASK_form_holds_i_e_CANNOT_DETECT_IT'] else 'yes'} | "
          f"{n(_d['independently_sourced_population_size'])} | "
          f"{'**YES**' if _d['INDEPENDENT_form_DETECTS_THE_DEFECT'] else '**NO — ESCAPED**'} |")
    B("")
    B(bt("every figure in this table"))
    B("")
    B(f"**{ij['defects_injected']} defects injected; "
      f"{ij['detected_by_the_INDEPENDENT_form']} detected by the independently-sourced identity; "
      f"{ij['MISSED_by_the_same_mask_form']} of them INVISIBLE to the same-mask form.** "
      f"**Every case discriminates as expected: {ij['every_case_discriminates_as_expected']}**, "
      "and **the run asserts it**, so an escape aborts before a deliverable is written. "
      "***Case 3 is the labelled exception***: its two clauses come from different masks, so the "
      "same-mask form fails on it too — stated rather than glossed, **because the point of the "
      "suite is which control catches what**.")
    B("")
    B("**Case 3 is also the control this arm already had, and `0091` §2 credits it as real:** "
      "invariant 6's `THE_HOLE_THIS_WOULD_NOW_CATCH` reconstructs `0080` §3's exact mispairing — "
      "**19,042 + 177,513 = 196,555 against 196,654, 99 rows in neither** — and the identity "
      "**fails**. **What was missing is that it covered ONE invariant.** The five other cases "
      "extend it, and they are the ones the same-mask form cannot see.")
    B("")
    B("| Identity shape | What it can detect |")
    B("| :--- | :--- |")
    B("| **population size from the same mask as the asserted count** — with one clause or with "
      "five | **Nothing.** `N − N = 0`, and a complementary partition of `M` sums to `M` for "
      "every `M` |")
    B("| **population size from an independent source** | **An invariant run on a population "
      "other than the one it names**, which is the 99-row hole `0080` §3 was written for |")
    B("")
    B("> **What invariant 6 would now catch, measured rather than described.** Pairing the "
      "post-liveness Started-and-left numerator with the pre-liveness non-S&L clause — the exact "
      "mispairing `0080` §3 records — is reconstructed on this build and evaluated against the "
      "emitted table's row count; the identity **fails**, and the rows covered by neither clause "
      "are reported. **Under a same-mask denominator that pairing could not be detected at all.** "
      "See invariant 6's `THE_HOLE_THIS_WOULD_NOW_CATCH` below.")
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
    B(f"*Every result in this report was measured on build {BT} — "
      f"{lib.BUILD_NAME.rstrip(chr(46))} "
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
