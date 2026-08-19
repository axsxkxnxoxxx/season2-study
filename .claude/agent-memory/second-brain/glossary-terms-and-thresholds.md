---
name: glossary-terms-and-thresholds
description: Live glossary of every term, threshold and constant in the Season 2 abandonment study, each tagged with the step, decision and gate that fixed it and which population its figures are on — current through decisions/0098 and the STEP 8 GATE APPROVAL of 2026-08-17, all five gates closed; carries the 89-name column set, the nine invariants with their coverage identities, D9's universe/keys/bound, and the false-positive trap table
metadata:
  type: reference
---

# Glossary — terms, thresholds, and where each was set

**Current through `decisions/0098`, 2026-08-17** — Steps 3, 4, 2, 5, 6, the Step 1 §7 amendment, the
**Step 7 liveness gate, APPROVED (`0064`)**, and the **Step 8 block (`0066`–`0098`), GATE APPROVED
2026-08-17 (`0098`), ELEVEN Red Team passes — ten HOLD, then PROCEED.** This is an index, not a
substitute for the artifacts. Verify against the file before acting on any row.

> ***ALL FIVE GATES ARE NOW APPROVED:*** Step 1 (`0001`, amended and re-approved at `0034`) · Step 5
> (`0021`) · Step 6 (`0026`) · Step 7 (`0064`) · **Step 8 (`0098`, gate 5 of 5, 2026-08-17,
> UNCONDITIONAL).** Record: **`artifacts/step8-gate-approval.md`**, drafted by the Analytics Engineer
> and **signed only by the Human Lead**. **Step 8b and Step 9 are UNBLOCKED and NOT LAUNCHED** — the
> handoff rule governs, and no agent begins either on the strength of the approval.
>
> **The eight §4 residuals are OPEN AND PUBLISHED and the approval is unconditional with them so.**
> ***§4 item 2 — the `logs/` provenance cost — is ACCEPTED AS RECORDED, not a correction anyone will
> close.*** Do not file it as an open item awaiting a fix; the Human Lead named why: *"a cost logged
> as a correction reads as a defect awaiting a fix, and this one is neither."* **The five §5
> limitations travel to Step 14.**

> ***FIVE RULES WERE ADDED TO `CLAUDE.md` IN THE STEP 8 BLOCK, and all five are process, not
> measurement.*** **The two added after `0094` are recorded in full below** — see
> **§THE TWO ISOLATION RULINGS (`0095`, `0096`)**, which must be read together or the pair reads as a
> contradiction. The first three:
> **artifact sign-off** (`0092`) — *no artifact is trusted without its producing arm's sign-off; a
> deliverable is corrected by RERUNNING the arm, never by hand-editing*; **a ruling is not closed until
> the artifacts carry it** (`0093`) — the arms rewrite deliverables **only on a run**, so every ruling
> since `0084` spent a window recorded-as-done and passing on all eight surfaces while both arms still
> published the superseded text; and **the citation resolver** (`0094` §4) — every four-digit decision
> citation on all eight surfaces is resolved against `decisions/`, **fails on any citation with no
> file, and fails if it finds zero citations.** It exists because **`0092` and `0094` were both cited
> before they existed**, the second **after** the first had recorded the defect and observed that no
> control could see it. ***AND IT HAPPENED A THIRD TIME: `0095` was cited in 10 files before it
> existed*** — **invisible to the resolver because `CLAUDE.md` is not one of the eight surfaces it
> scans** — and **caught only because `artifacts/` IS surface 6** and arm a's build provenance named
> the entry (`0095` §4).

> **THE STEP 8 SPEC OF RECORD IS `task-sheet.md` Step 8 AND THE `analytics-engineer` PAIR, NOT THIS
> FILE.** The 89 column names, the **NINE** invariants and their coverage populations are enumerated
> there. Where this glossary and those files differ, **they govern** — the same relation this file has
> to `src/step7_register.py`.

> **THIS FILE IS NOT THE REGISTER. `src/step7_register.py` is** — one register, imported by both
> `src/check_surfaces.py` and `src/step7_regenerate_derived.py` (`0059` B3: *"Two registers is one
> register plus a defect waiting"*). The trap table below is a **reading aid that mirrors it**, and
> where the two differ **the source file governs**. `0063` §3 item S7 records the stale `bb-{a,b}.md:3`
> stamp naming the glossary as canonical as a **carried defect**; this notice is the other half of it.

> **This file is PROPAGATION SURFACE 7** (`CLAUDE.md` §Propagation, added 2026-08-13). A ruling lands
> here as well as in `decisions/` and the five spec files, and **surfaces 6 (`artifacts/`) and 7 (this
> memory) were never checked before 2026-08-13.** The control is **read-back PLUS grep**: read-back
> proves the new text landed, only grep proves the old text is gone, and a file can hold both at once.
> **Stale memory here has already caused a wrong ruling** — see the ALT-MATCHED row and `0052` §2.

Status vocabulary: **FIXED** (set and gate closed) · **DEFERRED** (form fixed, value owed)
· **OPEN** (gate has not run) · **PROPOSED** (agent produced it, gate not approved).

> **Standing rule since `0046` §0, and it governs this file: EVERY FIGURE STATES WHICH POPULATION
> PRODUCED IT, at the point of use.** Extended by `0047` §3 to interval endpoints: *an endpoint
> states the population it is computed on and the estimand it bounds, and they must be the same
> population.* Both rules exist because the study broke them repeatedly — see
> [[gate-step7-liveness]].

## The five items the Human Lead named as glossary-critical

| Term | Value / status | Where set | Gate |
| :--- | :--- | :--- | :--- |
| **`W`** — the window, in days | **FIXED: `W = 108 days`.** The **ceiling** of the **90th percentile** (107.7135) of the **continuous** lag from clock start to first S2 episode, on the **C1 subset (25,120 pairs, 206 shows, 2,050 users)** of the 128,099 clean-record sample. **Applies to all pairs.** Precision: **±18 days, show-clustered** — not the decimals. **Since `0034`, `W` no longer assigns every outcome state on its own**: `τ1` assigns never-started, `τ2 = τ1 + H` assigns Continued. **Precision history: 107 (`-a`, floored) → 107.7135 (`-b`, raw) → 108 (adopted ceiling).** Neither artifact figure is the adopted value; both predate `0025`. | Rule: `0024` (percentile) + `0025` (unit and ceiling). Value: `0026`. Propagated into Steps 7, 8, 13 and both Step 6 artifacts by `0029` | **Step 6 gate, APPROVED 2026-08-12, `0026`. Gate 3 of 5** |
| **Liveness rule** | **APPROVED. THERE IS NO THRESHOLD. The rule is ALT-BROAD:** *a pair is **not live iff BOTH** the account shows **no insertion instant after that pair's `τ1`** AND the pair is **NOT Continued**.* **Silence anchored at `τ1` and ONLY at `τ1`; the channel window is `(τ1, τ2)`, OPEN at `τ2`** (`0057` §5 — `(τ1, τ2]` was **wrong, not ambiguous**: at `s = τ2` the unobserved remainder is empty, so the pair must not be conceded). **Restored by `0054` after being superseded by ALT-MATCHED at `0052` for one day.** A numeric threshold was derived three times (632 d, 1,293 d) and **DELETED at `0042`** — the headline could not distinguish 787 from 2,200 days. **No parameter of its own; FULLY DETERMINED BY `W`** (`0044` — "no free parameter" is withdrawn). Basis unchanged: **insertion time**, not claimed `watched_at` (`0021` ruling 2); stored play-`id` calibration a required input that **neither instance refits** (`0022`, `0029`); **pair-level, never a wholesale user drop** (`0034`). **The SILENCE test is anchored at `τ1` and ONLY at `τ1`** — ruled at `0034` (*"Liveness stays anchored at `τ1`. Liveness licenses trusting a null, and the null is `\|A\| = 0`, which is tested at `τ1`"*), re-affirmed at `0051` with both windows in view, and re-affirmed again at `0054`. **The Continued conjunct is read at `τ2`** (`0049` — *"`τ2` plays no part"* is withdrawn), and that is the ONLY role `τ2` has in the rule. **Do not reintroduce a pre-`τ1` requirement in any form — withdrawn twice** (`0040` §1, `0042` §3), both for contradicting gate `0021`. **Do not re-anchor the silence test at `τ2` in any form — tried once as ALT-MATCHED and reverted** (`0052` → `0054`) | Rule `0048`, restored `0054`; deletion `0042`; coupling `0044`; anchor `0034`, `0051`, `0054`; window `0057`; corrections `0043`, `0045`–`0063` | **Step 7 gate, APPROVED 2026-08-13, `0064`. Gate 4 of 5.** Record `artifacts/step7-gate-approval.md`. **UNCONDITIONAL — the §4 residual publishes with the result and is not a condition.** Approved twice before (`0039`, `0042`) and reopened twice; **fifteen Red Team reviews, fifteen HOLDs.** **Step 8 launched at `0072` and was APPROVED at `0098`, 2026-08-17 — gate 5 of 5. ALL FIVE GATES ARE CLOSED** |
| **S1 completion rule** | **FIXED.** `F1 ∈ D1` **and** `\|D1\| ≥ ceil(0.90 × L1)`, distinct episodes, membership by the listed set `E1`. Now applied against **real** `E1` from the Step 2 frame, not a proxy (`0019`). | Step 1 §4 | **Step 1 gate, APPROVED 2026-08-10** |
| **Contamination exclusion rule** | **FIXED.** Exclude **16,665** pairs whose S2 evidence is *entirely* air-date-stamped, plus **1,542** with no S2 evidence and a fabricated binding clock start. Total **18,207**; retains **201,900 of 220,107 (91.73%)**. Disjoint by construction. | Step 5 §9, revision 6 | **Step 5 gate, APPROVED 2026-08-12, `0021`. Gate 2 of 5** |
| **Filter order** | **FIXED by `0029`, ahead of the gate.** **1.** Step 2 frame → **2.** `L2 = 1` exclusion → **3.** S1 completion rule → **4.** contamination exclusion → **5.** right-censoring → **6.** liveness rule → **7.** outcome assignment **at two instants** (`\|A\| = 0` at `τ1`, Continued at `τ2`, per `0034`). **Why it had to be fixed:** the final row set commutes — every filter is row-wise — but the **required per-filter sample size does not**, so two faithful instances could report different waterfalls on an identical table and the diff could not tell that from a bug. **Contamination before right-censoring** was already required. **Right-censoring before liveness** is the one genuine choice: censoring is a property of the clock and `pull_date`, objective and behaviour-independent, so running it first measures liveness's marginal cost on a fully observable population — the number Step 9's bound needs. **Since ALT-BROAD, waterfall line 6 is OUTCOME-CONDITIONAL and must be reported as such** — the Continued test is evaluated before liveness applies. **That is permitted, and both arms proved it independently:** the two are **row-local predicates on the position-5 output and commute exactly**, and `0029`'s rationale concerns per-filter **sample size**, which cannot reach position 7 because **outcome assignment removes no rows** — positions 1–6 are filters, **position 7 is an annotation** contributing no waterfall line. **The monotone invariant is coded `>=`, not `>`** (`0047`, reason corrected by `0049`): decrease is **strict on both populations under ALT-BROAD**, and `>=` is kept anyway **so the invariant does not encode a property of one rule**. **Expect 703 at position 6; treat a mismatch as a POPULATION defect before an implementation one** — Step 7 built APPLY from the Step 5 pair table, not through positions 1–5. **Producing 604 means the withdrawn ALT was implemented, and that IS a divergence. Producing 793 means ALT-MATCHED was implemented, and that IS a divergence too** — `0053` §3 defect 2 briefly made 793 the expected count and `0054` §5 reverted it, after **both `analytics-engineer` files carried "EXPECT 793" at line 77 and "EXPECT 703" at line 88, ten lines apart, each declaring the other a divergence, identical in both copies so the dual diff could not see them, in the file Step 8 launches from** (propagation failure #13). **Branch decomposition, ALT-BROAD:** branch (i) `\|A\| = 0` → 33,373 → **604**; branch (ii) `\|A\| ≥ 1 ∧ ¬Continued` → 19,141 → **99**; total **703** | `0029`; liveness spec `0046`–`0052`, `0054`, written into `task-sheet.md` Step 8 | **Step 8 gate, APPROVED `0098`, 2026-08-17 — gate 5 of 5.** ~~*"NOT approved — the ONE REMAINING GATE"*~~ **superseded.** **Step 8 LAUNCHED at `0072`, 2026-08-13**, and ran as a dual pair plus reruns through eleven Red Team passes. **The approved waterfall: `220,107 → 220,107 → 220,107 → 201,900 → 196,654 → 195,951 → 195,951` on APPLY and `… → 152,126 → 147,370 → 147,271 → 147,271` on DERIV**, reproduced independently by both arms to the row. **`0074` then ruled the emitted table is the POSITION-5 row set, not position 7** — so the waterfall runs seven positions while the deliverable is line 5 with `live` and `outcome` as columns. **Positions 1, 2, 3 and 7 are INERT and labelled with the reason** (`0079`) |

## Step 8 — the analysis table. **GATE APPROVED, `0098`, 2026-08-17.** Full arc in [[gate-step8-analysis-table]]

**Launched `0072`, 2026-08-13, as the dual pair `analytics-engineer` / `-b`. Ruled on across
`0066`–`0098`. ELEVEN Red Team passes: ten HOLD, then PROCEED on the eleventh, 2026-08-17.**
**Builds approved: `a/2026-08-17-0096` and `b/2026-08-17-r8`, both confirmed by their producing arm.**
Full pass-by-pass arc, including which findings falsified the review's own premise, in
**[[gate-step8-analysis-table]]**.

> ***SUPERSEDED, and it was this file's text until 2026-08-17:*** ~~*"GATE NOT APPROVED … no Step 8
> proposal is adopted; every entry from `0073` on says so in terms."*~~ **True through `0097`;
> `0098` approved the gate.** *(And superseded before that: ~~"Red Team has passed twice"~~, which was
> six passes stale when found.)* **The document governs over any briefing, including the Human Lead's**
> ([[feedback-verify-against-files]]).

**What the eleven passes established, and the split is the Step 18 material.** **Passes 1–7 contested
SUBSTANCE and changed what is measured** — filter order, the invariant set's falsifiability, the
coverage identities, D9's keys and universe, `p_at_bound`'s meaning, D11's scope, the half-open
boundary form. **Passes 8–11 found almost nothing in the arithmetic and a great deal in the prose.**
The tenth pass named the generator: **arm a's waterfall was 826 lines of which roughly 120 was
measurement**, the rest build history and claims about other surfaces — *"review retires roughly three
per pass; the build adds roughly the same number"* — a **plateau with an identifiable generator.**
**`0096` removed the CATEGORY rather than the instances, and the eleventh pass returned PROCEED.**

> ***TWO MEASUREMENTS CHANGED A PUBLISHED ANSWER DURING THE SEQUENCE AND SURVIVE IN THE RESULT:***
> **the half-open UTC-instant form is OUTCOME-DECIDING** — 71 APPLY and 59 DERIV position-5 rows change
> outcome state under the forbidden `date(ts) ≤ date(τ)` form, **36 of them never-started → Continued**,
> the two ends of the headline (`0091` §1; it publishes at Step 14) — and **`0068`'s strictness ruling
> is VACUOUS on this data**, 0 pairs and 0 accounts on both populations, measured independently by both
> arms (`0089` §2(a) as amended).

### The EIGHT RESIDUALS — open, published, and the approval is unconditional with them so

**`artifacts/step8-gate-approval.md` §4. None touches a filter position, a population, a waterfall
line, an outcome count, an invariant result or a bound endpoint.**

| # | Residual |
| :-- | :--- |
| 1 | **Two files in `artifacts/` state four things that are false today** — the read-backs, stamped and allowlisted by `0097`. **Invisible to every control: the third blindness class** |
| **2** | ***THE `logs/` PROVENANCE COST — ACCEPTED AS RECORDED, NOT A CORRECTION ANYONE WILL CLOSE.*** Build history and control results now live in `logs/`, which is **git-ignored and on no propagation surface**, so **the public artifact set is no longer self-auditing on provenance.** **The knowing price of `0096` §1.** One such log already over-claims its coverage (`surfaces_not_reached: []` while four were never scanned). ***Do not file this as awaiting a fix*** |
| 3 | **Neither arm's deliverable identifies the spec revision it validated against.** Arm a does not fingerprint `task-sheet.md` at all while asserting its 89-name conformance was read off it at run time — **that referent is unrecoverable** |
| 4 | **Three cross-arm coverage divergences under identical labels** — distinct S2 episodes 2,135,938 vs 2,023,274; the D9 pivot show-ID count 46,366 vs 45,014; per-site D11 at `A`/`A_H`. **All denominators, none moving a result, resolvable only by reading each arm's mask** |
| 5 | **Six of nine invariants cannot fail on any data. The gate rests on TWO data checks and one cross-check with force.** Both arms publish the 6 + 1 + 2 split and say so plainly |
| 6 | **Two unruled spec choices, both disclosed by the arm that made them** — set-membership denominators 6,065,704 vs 6,065,610, and different D9 half-(b) grains |
| 7 | **The D9 rank-3 tie-break is unruled and the tie is occupied** — six keys at 6. Both arms list all six; **neither picked the name `0088` §3 gave** |
| 8 | **439 unread needle candidates**, deliberately **neither failed nor narrowed** (`0095` §3) |

### The FIVE LIMITATIONS that travel to Step 14 — properties, not defects (§5)

1. **The half-open form decides 71 APPLY outcomes.**
2. **Liveness is outcome-conditional**; the `NOT Continued` conjunct spares **652 on both populations**.
   **The commutation check shows the two filter orders agree on OBSERVED COUNTS; it does not show the
   estimand is unaffected.**
3. **The liveness rule is a biconditional and `0021` licenses one direction only.**
4. **ALT-BROAD leaves 297 pairs in the channel its own warrant describes** — 52.4% closed on the
   implicated set, 47.6% open.
5. **Step 9's bounds and published shares are on different populations**, and **on DERIV the point
   estimate lies outside its own identified set.**

### What the table IS

| Item | Ruling | Where |
| :--- | :--- | :--- |
| **Grain** | **The POSITION-5 row set: 196,654 rows on APPLY, with `live` and `outcome` as COLUMNS.** Not position 7. Both readings gave **identical counts** (A: 195,951 × 86 at position 7; B: 196,654 × 87 at position 5) — nothing was wrong, a choice was unstated. Ruled on `0071`'s principle: **downstream CONSUMES, it does not REBUILD**, and *"a reconstruction that agrees today is still a second definition tomorrow"*, invisible to the dual diff because both arms would rebuild the same way | `0074` §1 |
| **Waterfall line 1** | **220,107 — the S1-completer population.** Four defensible bases sat on disk (2,900,762 · 278,452 · 274,741 · 220,107) and **lines 1, 2 and 3 all moved with the choice**. Line 2 = line 1 less `L2 = 1`; line 3 = line 2 less the S1-completion failures. **No instance chooses a base.** *Open and NOT closed by it: D11 at position 3 gives **220,103**, 167 in-frame records at `watched_at ≥ τ_pull`* | `0068` §1 |
| **Both populations** | **Step 8 emits APPLY 196,654 AND DERIV 147,370**, plus **the D4 count**. Omitting either forces Step 9 to rebuild — the second-definition defect | `0070` r1, r7; `0071` |
| **Columns** | **89 ENUMERATED NAMES, not a count.** See below | `0080` → `0081` → `0082` |
| **Invariants** | **Eight: 5 code checks, 1 code-by-construction, 2 data checks.** See below | `0069`, `0074`, `0076`, `0080` |

### The COLUMN SET — 89 ENUMERATED NAMES. **THE COUNT HAS BEEN 87, 88, 89 AND 90.**

**Enumerated precisely because the count drifted.** `0077` §3 fixed **89** as a count; `0080` replaced
the count with **87 enumerated names**; `0081` restored `silent_at_tau1` → **88**; `0082` added
`p_at_bound` → **89**. **90 is the UNION** of the two arms' 87-name sets (`0080` §1) and was never
adopted. **The enumeration lives in `task-sheet.md` Step 8 (line ~336) and both `analytics-engineer`
files and governs; the copy below is a reading aid and the spec files govern over it.**
***THE 89-NAME SET IS SET-EQUAL ACROSS BOTH ARMS*** — `artifacts/step8-gate-approval.md` **§3**
(`0098` §1 states the grain, *"196,654 rows × the 89 enumerated columns on APPLY"*; the set-equality
is §3's line). **Checked at the point of citation, because a right claim under a wrong referent is
this block's most-repeated defect.**

> **THE 89 NAMES, alphabetical, as `task-sheet.md` lists them:**
> `abandonment_point_p` · `action_count_s1_checkin` · `action_count_s1_other` ·
> `action_count_s1_scrobble` · `action_count_s1_watch` · `action_count_s2_checkin` ·
> `action_count_s2_other` · `action_count_s2_scrobble` · `action_count_s2_watch` · `air_period` ·
> `cadence_boundary_distance_days` · `cadence_bucket` · `completers_per_year` ·
> `discovered_channel_a` · `discovered_channel_b` · `e1_internal_gap` · `e1_starts_at_1` ·
> `e2_internal_gap` · `e2_starts_at_1` · `exclusion` · `gap_days` · `has_s3_or_later_evidence` ·
> `in_apply` · `in_deriv` · `live` · `max_episode_in_A_H` · `max_season_number` · `n_A` · `n_A_H` ·
> `outcome` · `p_at_bound` · `pool_completers` · `pool_completers_proxy` · `s1_E` · `s1_F` · `s1_L` ·
> `s1_aired_episodes_reported` · `s1_aired_lt_listed` · `s1_completion_date` ·
> `s1_completion_used_a_post_cutoff_record` · `s1_count_disagreement` · `s1_episode_count_reported` ·
> `s1_exposure_years` · `s1_finale_date` · `s1_premiere_date` · `s1_season_first_aired` ·
> `s1_total_runtime` · `s2_E` · `s2_F` · `s2_L` · `s2_aired_episodes_reported` · `s2_aired_lt_listed` ·
> `s2_count_disagreement` · `s2_episode_count_reported` · `s2_finale_date` · `s2_finale_year` ·
> `s2_premiere_date` · `s2_season_first_aired` · `s2_span_days` · `s2_total_runtime` ·
> `s2_weekly_span_days` · `season_numbers` · `seasons_returned` · `show_aired_episodes` ·
> `show_airs_day` · `show_certification` · `show_comment_count` · `show_country` · `show_first_aired` ·
> `show_genres` · `show_language` · `show_languages` · `show_rating` · `show_runtime` · `show_status` ·
> `show_subgenres` · `show_trakt_id` · `show_votes` · `show_year` · `silent_at_tau1` · `size_quintile` ·
> `size_quintile_per_year` · `size_quintile_raw_count` · `t0_binding_term` · `t0_date` · `tau1` ·
> `tau2` · `title` · `user_idx`

**WHAT IS DELIBERATELY NOT IN IT, and why each is a ruling rather than an omission:**

| Name | Status | Why |
| :--- | :--- | :--- |
| **`f2_in_A_H`** | **DROPPED, and it is FREE** | Derivable as `max_episode_in_A_H == s2_F`. **The `A_H`-not-`AH` SPELLING ruling survives the drop; the COLUMN does not** — `task-sheet.md` marks it rather than deleting it so the spelling ruling is not lost with the column |
| **`max_episode_in_A`** | **DROPPED, and it is FREE** | **Read by nothing downstream** |
| **`silent_at_tau1`** | **ADDED by `0081`**, 87 → 88 | **The ONLY way to recompute the Continued-and-silent count, 652, from this table.** The rule's second conjunct is `NOT Continued`, so **`live` is true for every Continued pair regardless of silence** and the column is not recoverable from `live` and `outcome`. 652 closed the rule objection at `0063` §1 and is a published Step 14 limitation; its input living in Step 7's working files is **the same shape as `0079`'s drop set** |
| **`p_at_bound`** | **ADDED by `0082`**, 88 → 89 | **Marks WHETHER `p` reached its bound, NOT why** (restated `0083` §2). Kept even though its FALSE class is empty, because **Step 10 needs the spike labelled and an emptiness asserted in prose and never emitted cannot be checked** |
| *`has_s3_or_later_evidence`, `discovered_channel_a/_b`* | **IN** — both instances' extra columns kept | D4 reads the first; the channel is **two booleans, not one categorical** (`0070` r3) |

**The count moved 88 → 89 as a mechanical consequence of adding `p_at_bound`, and is stated rather
than left to be recounted.** **`88 columns` is a registered superseded NEEDLE**; **`0077`'s own 89 is
NOT this 89** — `f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. *"Matching a count is not
matching a set — assert on the names."*

- **`silent_at_tau1` is IN** (`0081`). **It is the ONLY way to recompute the Continued-and-silent count,
  652, from Step 8's table** — the liveness rule's second conjunct is `NOT Continued`, so **`live` is
  true for every Continued pair regardless of silence**, and the column is not recoverable from `live`
  and `outcome`. **652 is the outcome-conditioning size that closed Red Team's rule objection at
  `0063` §1** and publishes as a Step 14 limitation. Decisive argument: its input living in Step 7's
  working files is **the same shape as `0079`'s drop set** — a required input must not live in a
  working file.
- **`p_at_bound` MARKS WHETHER `p` REACHED ITS BOUND, NOT WHY** (`0082`, restated `0083` §2).
  **TRUE where `p` reached its bound**, null where `p` is null. ***SUPERSEDED — this bullet said:***
  ~~*a boolean separating the two meanings of `p = 1.0`: the pair left at the final episode, versus*~~
  ~~*the rank numerator saturating at `L2`; and a spike at 1.0 means two different things about*~~
  ~~*viewers.*~~ ***The two clauses are COEXTENSIVE BY CONSTRUCTION*** — set membership puts `m_H ∈ E2`, so
  the numerator is `L2` **iff** `m_H = max(E2) = F2`, which *is* "left at the final episode."
  ***CORRECTED HERE 2026-08-17 — THIS BULLET CARRIED THE EXACT SENTENCE ARM A'S DELIVERABLE WARNS
  AGAINST.*** It read ~~*"the FALSE class is EMPTY"*~~ **unqualified. TWO DIFFERENT `FALSE` CLASSES SIT
  ON THIS PAGE and only one is empty** (`artifacts/step8-waterfall-a.md` §3.1): **CLASS 1, the
  COEXTENSIVITY GAP** — rows where `0082`'s two superseded mechanisms disagree — **is 0 on all four
  populations**; **CLASS 2, the COLUMN'S OWN `FALSE` VALUE** — Started-and-left rows where `p` did not
  reach its bound — **is 17,895 on APPLY position 5** (17,812 post-liveness; DERIV 15,771 / 15,688).
  **The arm states the consequence in terms: *"a consumer that reads 'the FALSE class is empty' and
  provisions a two-valued column is wrong by 17,895 rows"*** — and **Step 8b defines the schema Steps
  9–13 write into with NO CONVERSION LAYER**, so this is a live hazard, not a wording point. **The
  emitted column is three-valued: `1,246 TRUE + 17,895 FALSE + 177,513 null = 196,654`.**
  **`p = 1.0` totals: 1,246 / 1,230 on APPLY, 1,072 / 1,056 on DERIV, all four with
  `in-both-classes = TOTAL` and 0 / 0 / 0 in the three gap cells.** ***1,246 and 1,230 ARE STILL TRUE
  BUT ARE NOT A SPLIT*** — one class counted twice, not two summed. **Citing them as
  evidence the column separates anything is a WITHDRAWN ARGUMENT — Mode I**, registered in
  `GROUNDS_WITHDRAWN` (`src/step7_register.py`). *(This read "Mode H" until 2026-08-17; **H is the
  asserted-action class, I is the withdrawn-ground class** — [[withdrawn-claims-register]].)* **Separate DATA fact, not the same argument:
  0 of 1,138 frame shows have any S2 numbering gap**, so `E2 = {1…L2}` and the rank form reduces to
  `m_H / L2`; that could be false on another frame and the coextensivity would still hold.
  **The column is KEPT** — Step 10 needs the spike labelled, and an emptiness asserted in prose and
  never emitted cannot be checked.
  ***This bullet was propagation failure #22*** (`0084`): `0083` §2 reached the table row 71 lines
  below and not this bullet, and **the phrase control could not see it because the withdrawn sentence
  wrapped across a line break** — found by instance A on the rerun, not by a control.
- **Two columns stay DROPPED, both free:** **`f2_in_A_H`** (derivable as `max_episode_in_A_H == s2_F`)
  and **`max_episode_in_A`** (read by nothing downstream).
- **Naming rule** (`0077` §3): **use the spec's own vocabulary at the point the spec defines the thing;
  where the spec does not name it, prefer the more explicit form.** Hence `in_apply` / `in_deriv`,
  `tau1` / `tau2` (**no `_utc` — every instant in this study is UTC by Step 1 §2.4, and suffixing some
  columns implies the others are not**), `n_A` / `n_A_H` / `max_episode_in_A_H` (**`AH` is not the
  spec's spelling**), `action_count_s{1,2}_{watch,scrobble,checkin,other}`, `discovered_channel_a/_b`.

### THE **NINE** INVARIANTS — labels and coverage populations

> **CORRECTED 2026-08-16: this heading said EIGHT and the assertion set is NINE.** `0088` §1(c)
> promoted `assert (tau2[pos5] > τ_pull).sum() == 0` — which had been running inside one arm's pipeline
> and sitting **outside the published set, invisible to any reader of the deliverable** — into the
> published set as **invariant 9, CODE CHECK.** **`task-sheet.md` and both agent files still read
> "EIGHT MEMBERS" when `0089` §3 found it; the NEGATIVE grep passed clean and the POSITIVE half is what
> caught it** — a figure never written returns zero hits on every superseded form of itself.
> **NINE = six pure code checks, one code-by-construction, two data checks.**
> **`six of eight`, `of eight cannot fail`, `assertion set now has eight` and `seven of the nine` are
> all registered superseded NEEDLES** (`SUPERSEDED_STRINGS`), and the matching is **case-insensitive**
> because the string actually present in one arm's deliverables three times was `six of EIGHT` — *the
> one needle written against the very defect that motivated the control could not see it, and its hits
> table showed no row for it at all, indistinguishable from a clean pass* (`0093` §5).
>
> **AND THE COVERAGE APPARATUS AROUND THEM MOSTLY CANNOT FAIL.** `0087` §4: **8 of arm a's 13
> identities are `cover(unit, pop, N, N)`** where `n_pop` and `n_asserted` are the same expression.
> `0091` §2: one arm's `real = len(parts) > 1` proxy admitted **all four** identity families, each a
> complementary partition of the mask the population size is taken from — **including the one the
> deliverable called *"the identity that closes the hole."*** ***Struck whatever else is ruled:***
> ~~*"The run asserts this, so a report that omitted a population could not be written by this
> pipeline."*~~ — **a control asserted to exist** (`0088` §2). **The dual diff could see none of it:
> both arms did it.**

**`0069` labelled every invariant CODE CHECK or DATA CHECK, and that is what resolved the dual run's
4-of-6 against 6-of-6 split.** **`p` IS A CODE CHECK** — `0074` §2 mislabelled it DATA CHECK and
`0076` §1 corrected it **on both instances' own proof** (S&L requires `|A| ≥ 1` so `m_H` exists, and
set membership bounds the rank numerator in `[1, L2]`; no data configuration puts `p` outside
`(0, 1]`). **The correction INVERTED the finding: five of six unfalsifiable with ZERO pure data
checks** — *"four of six" is SUPERSEDED and was corrected in eight places.* **The two data checks were
added because the set had none.**

> ***THE SPLIT IS 6 + 1 + 2, AND IT IS THE GATE'S OWN RESIDUAL 5.*** **SIX pure code checks** (1, 2, 3,
> 4, 6, 9) that **cannot fail on any data** · **ONE code-by-construction with force only as specified**
> (5) · **TWO that CAN FAIL ON REAL DATA** (7, 8). ***So the gate rests on TWO DATA CHECKS AND ONE
> CROSS-CHECK WITH FORCE***, and that is stated here rather than left to be recounted.
> **Both arms publish the split and say so plainly** (`0098` §3 residual 5).
>
> **Why three classes and not two** (arm a, and the spec's own sentence has the same shape):
> **collapsing the middle member into either outer class changes the answer to *what could this report
> have caught?*** — folded upward it reads as **seven that cannot fail**, folded downward as **three
> that can.** *"The sentence a reader takes away is the headline, so the middle class is published as
> its own."*
>
> ***THE NINTH MAKES THE FALSIFIABILITY RATIO WORSE, NOT BETTER.*** The promoted assertion is a
> **sixth pure CODE CHECK**, so the set went **5 + 1 + 2 → 6 + 1 + 2** and **the number that can fail on
> real data is unchanged at TWO.** It adds **visibility, not power** — which is exactly what `0088`
> §1(c) asked for, since *"an assertion a reader of the deliverable cannot see is not a published
> check."* **An added check reads as an added guarantee; this one is not one.**

| # | Invariant | Label | Stated population (`0080` §3) | Coverage identity, arm a, build `a/2026-08-17-0096` |
| :-- | :--- | :--- | :--- | :--- |
| 1 | outcome states mutually exclusive, summing to the post-position-7 row set | **CODE** | **FOUR, ALL STATED**: 195,951 and 196,654 on APPLY, 147,271 and 147,370 on DERIV | `32,769 + 19,042 + 144,140 + 0 = 195,951` · `33,373 + 19,141 + 144,140 + 0 = 196,654` · `9,145 + 16,744 + 121,382 + 0 = 147,271` · `9,145 + 16,843 + 121,382 + 0 = 147,370` |
| 2 | filter counts decrease monotonically, coded `>=` not `>` | **CODE** | **both chains**, APPLY's seven positions and DERIV's | `7 + 0 = 7` on each chain |
| 3 | `\|D\| ≤ L`, distinct episodes ≤ season length | **CODE** | **both seasons, every pair the set-membership rule examines — the PAIR UNIVERSE of 278,452, NOT the 196,654 row set** | `278,452 + 0 = 278,452` |
| 4 | `A ⊆ A_H` on every row | **CODE** | the 196,654 position-5 row set, every row | `196,654 + 0 = 196,654` |
| 5 | clock start ≥ S2 finale, ≥ first-pass S1 completion, and **equal to one of the two** | **CODE BY CONSTRUCTION, DATA CHECK AS SPECIFIED** — force comes ONLY from recomputing the S1 completion date INDEPENDENTLY | 196,654, every row, **with the first-pass date recomputed independently — the only thing giving it force** | `196,654 + 0 = 196,654` |
| 6 | `p ∈ (0, 1]` on S&L, null elsewhere | **CODE** (`0076`, correcting `0074`) | **ALL S&L rows AT POSITION 5, null on the rest, the two clauses summing to 196,654 EXACTLY** | `19,141 + 177,513 + 0 = 196,654` |
| 7 | **no account dropped wholesale by the pair-level liveness filter** | **DATA** | **BOTH POPULATIONS, IN ACCOUNTS** — accounts holding a position-5 pair in each | APPLY `2,206 + 215 + 1 + 0 = 2,422` · DERIV `2,329 + 72 + 1 + 0 = 2,402` |
| 8 | **no `access_denied` or skipped account read as empty** | **DATA** | **THE FULL ACCOUNT LEDGER, IN ACCOUNTS** — every distinct account the Step 4 pull touched, not the survivors | `2,874 + 0 = 2,874`. **Scope note, arm a: 7 accounts skipped on one attempt yielded data on another and hold 604 position-5 pairs** (119 never-started) — *not a violation; reported so the assertion's scope is visible* |
| **9** | **`tau2 ≤ τ_pull` on every position-5 row** — D11's inertness on the outcome windows | **CODE** (`0088` §1(c)) | **BOTH POPULATIONS, EVERY ROW** | APPLY `196,654 + 0 + 0 = 196,654` · DERIV `147,370 + 0 + 0 = 147,370`. **The bound is ATTAINED: 20 APPLY and 17 DERIV rows sit exactly AT `τ_pull`, so a `>=` form would FAIL** (`0089` §1) |

**15 coverage identities checked, all hold.** **The two DATA checks are not formalities:** check 7
separates a **pair-level** liveness implementation from an **account-level** one, which the
*703-from-216-accounts* figure alone cannot do; **check 8 is the one that would fail in the direction
of the result** — a skipped account read as empty becomes a false never-started in the headline.

**The set-membership drop rule is a COVERAGE COUNT, NOT AN INVARIANT** (`0074` §3) — Step 8's own
bullet already calls it *"an implementation check, not a data check."* **The 703 expectation is NOT an
invariant either** — it is a **population reconciliation** (`0069` §2).

> **EVERY INVARIANT NAMES ITS POPULATION AND REPORTS `rows_asserted + rows_not_asserted =
> rows_in_the_stated_population`** (`0080` §3). **One arm had a 99-row hole: 19,042 + 177,513 =
> 196,555 on a 196,654-row table** — numerator post-liveness, denominator pre-liveness, and **the 99
> uncovered rows are exactly the started-and-left liveness exclusions.** *"Neither report disclosed the
> gap, no control could see it, and it survived two reruns."* **Correct: 19,141 + 177,513 = 196,654.**
> **An invariant that passes on one population and was never run on another READS AS A PASS ON BOTH.**

### The four INERT positions — kept and labelled (`0079` §4)

**Positions 1 (frame), 2 (`L2 = 1`), 3 (S1 completion) and 7 (outcome assignment) each remove 0 rows.**
**Kept**, because removing a position removes the check that would catch a future upstream change.
**Labelled with the reason**, because *"an unlabelled always-zero filter reads as evidence THE RULE
FOUND NOTHING when it is evidence THE RULE CANNOT FIRE — the same defect as an unlabelled code check."*

> **Row 3 is the one that matters. Position 3's POSITION is inert while its RULE removes 58,345 pairs
> UPSTREAM of line 1 — the study's largest single exclusion, appearing in the waterfall as a `0`.**
> That is why **its drop set is a pipeline DELIVERABLE** (`0079` §1), written by the same run that
> writes the table, not a helper script's side file: **D9 half (b) is measured on those rows, and
> without them it returns 0 SILENTLY — a plausible data finding rather than an error.**

### The other Step 8 rulings, in one table

| Item | Ruling | Where |
| :--- | :--- | :--- |
| **Silence-test evidence scope** | **restricted to records dated before `τ_pull`** — applying D11 consistently, not a new rule. **Measured inert on the exclusion set (703 / 99 either way); it bites on the robustness tail**, where the 792 (A) / 791 (B) divergence lived. Now stated in **all three** places the rule is written | `0070` r2, `0071`, `0072` |
| **Silence-test strictness** | **STRICT** — no insertion instant `> τ1`; an instant exactly at `τ1` does not make the account live | `0069` item 7 |
| **Discovery channel** | **TWO BOOLEANS**, not one value. Overlap: **324 of the 5,694 discovery pool** (Step 3 seeding / Step 14 ledger item 1) · **178 of 2,549 accounts pulled** (Step 4 coverage) · **174 of 2,422 accounts and 17,783 of 196,654 pairs** on position 5 (**Step 11**). **All three publish, each with its consumer named** | `0070` r3, `0077` §1, `0079` §3 |
| **`action`** | **NOT a column — per-pair COUNTS BY TYPE.** `action` is a property of the LOGGING CLIENT, not of the viewing, so it is not an outcome variable. Step 13's arm reads the counts | `0070` r4, completed `0073` §2 |
| **D2's `max()` split** | **THREE categories** — finale binds, S1 completion binds, **both bind**. **168 pairs have both binding ON APPLY — and the count is NOT population-invariant** (`0092` §3, both arms, 2026-08-16). **APPLY is 168 at line 1 (220,107), position 4 (201,900), position 5 (196,654) AND post-liveness (195,951)** — all 168 tie pairs survive the chain — ***but DERIV IS 153*** (147,370 and 147,271), **recorded nowhere before that rerun.** ~~168 cannot be correct on both populations~~ — **WITHDRAWN: both arms' differing readings would have given 168, and the agreement was INVARIANCE, not error.** **State the population at the point of use and measure on both.** **A tie is its own category, not a tiebreak** | `0070` r5, **corrected `0092` §3** |
| **Drop denominator** | **position 5 = 33,373**, with post-liveness **32,769** alongside. The difference is exactly the 604 never-started liveness exclusions and is itself informative | `0070` r6 |
| **Filter order vs the published %** | **ORDER KEPT; the percentage moves. 10.3% → 10.5%** cohort loss, and the **pre-2020 comparator 2.7% → 3.0%**. *"Changing a filter order to preserve a published percentage is backwards."* Per-air-period: **97.40 / 97.8 / 97.4 / 95.9**, and **89.5%** for 2023–2025 at `W = 213` | `0070` r8, comparator `0073` §1 |
| **D9 keys** | ~~**STRICT ruled, LOOSE published alongside**~~ ***SUPERSEDED BY `0090`: D9 PUBLISHES AS A BOUND.*** See **§D9 — the universe, the keys and the bound** below, which is the current statement | `0074` §5, `0076` §3, `0078` §3, **superseded `0090`**; universe `0088` §3 |
| **Set-membership denominator** | **CLOSED — NOT a Step 14 limitation** (~~*"REPORTED, NOT RECONCILED … Routed to Step 14"*~~, `0074` §4). **Never a divergence**: a one-parameter family indexed by where D11 applies. D11 discards **167** in-frame S1/S2 records at or after `τ_pull` — **94 S2-side + 73 S1-side**. **A** (D11 nowhere) **6,065,704**, line 1 220,107 · **B** (S2 side only) **6,065,610**, line 1 220,107 · **C** (both) **6,065,537**, line 1 **220,103**. **All three drop 0**, so nothing downstream reads it. **Publish all three with pipelines.** The open item is `0068`'s D11-at-the-S1-walk, not this | `0074` §4, **closed `0083` §1** |
| **`p_at_bound`** | **Marks WHETHER `p` reached its bound, NOT why.** ~~`0082` §2's two mechanisms~~ are **coextensive by construction** — set membership puts `m_H ∈ E2`, so numerator `= L2` iff `m_H = max(E2) = F2`. ***THE COEXTENSIVITY-GAP CLASS (CLASS 1) IS EMPTY — 0 on all four populations. THE COLUMN'S OWN `FALSE` VALUE (CLASS 2) IS NOT: 17,895 / 17,812 / 15,771 / 15,688.*** Both arms measured 1,246/1,246/0/0 (position 5) and 1,230/1,230/0/0 (post-liveness), APPLY, 2026-08-16. **1,246 and 1,230 are TRUE but are NOT a split** — one class counted twice; citing them as separation evidence is a **withdrawn argument** (Mode H). Separate DATA fact: **0 of 1,138 frame shows have an S2 numbering gap** | `0082` §2, **restated `0083` §2** |

### D9 — the universe, the keys and the bound. **U1 is RULED (`0088` §3); the bound form is `0090`**

**THE UNIVERSE IS U1 — ALL SLUGGED SWEEP SHOW IDs — RANKED BY DISTINCT STRICT KEYS MERGED.**
Human Lead ruling, 2026-08-16 (`0088` §3). **Both arms cluster the same object: every distinct show ID
appearing anywhere in the pulled sweep that carries a slug, deduplicated to one row per show ID.**
**NOT U2** (the 1,138 frame shows) and **NOT U3** (the 75 D9 candidate pairs).

- **The ground:** the artifact D9 hunts is **a viewer's history splitting across two metadata entries
  for the same show**, and **that split can occur anywhere in a history, not only among shows that
  survived the frame filters.** A universe inside the frame **can only find splits where BOTH sides
  made the cut**, the narrowest case — *"a bound on how wrong the data might be, and a bound computed
  on a narrow slice bounds very little."*
- **It does NOT widen what D9 finds.** D9's search already ran on the whole sweep in both arms; **the
  strict and loose counts are unchanged.** What it fixes is **WHICH CLUSTERS ARE ILLUSTRATED** — the
  evidence for the loose key's only warrant — and it **makes the two arms' `U1` one defined object**
  rather than two sets **62 apart under a shared label** *(62 apart **within one arm**, `0089` §3,
  correcting `0087` §2's two-arm reading)*.
- **The ranking basis is DISTINCT STRICT KEYS MERGED** — how many separate metadata entries the loose
  key collapsed into one. **It was unstated and it reorders the list on its own:** the same universe
  under the same key, ranked by **distinct show IDs** instead, displaces `maigret` with `blackout`.
  **Name the basis at the point of use; a list without it is not reproducible.**
- **`46,428` = distinct slugged show IDs in the parsed sweep = U1**, both arms. **`46,366` is the D9
  COVERAGE PIVOT's show-ID count in arm a — a different object.** *(Residual 4 records a further
  cross-arm divergence on the pivot count, 46,366 vs 45,014.)*

**THE THREE KEYS, verbatim from `task-sheet.md`:**

| Key | Definition | Status |
| :--- | :--- | :--- |
| **STRICT** | *"lowercase the slug and drop every non-alphanumeric character. **Strip NOTHING else**"* — `re.sub(r"[^a-z0-9]", "", slug.lower())` | **THE FLOOR.** It matches only slugs identical modulo punctuation, so it **cannot over-count** |
| **LOOSE** | *"first remove a **TRAILING FOUR-DIGIT YEAR**, then apply the strict transform"* | **THE CEILING.** Stripping a trailing year **merges genuinely different shows** — remakes and national versions |
| **the THIRD key** | strips a **trailing digit group of ARBITRARY LENGTH** — which reduces `the-100` to `the` | ***NOT AN ENDPOINT.*** Its **76** is *a different key's answer*, **reported as a divergence and never as the ceiling.** One arm used it unlabelled; its half (b) is **28** against loose's 27 |

**Both keys are DEFINED IN THE SPEC** because they had existed only inside one arm's code — *"undefined
on every surface an isolated instance reads,"* so a rerun against the ruling would have reproduced the
divergence.

> ***D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS THE CEILING, BOTH LABELLED, AND NEITHER IS
> THE POINT ESTIMATE*** — **neither endpoint may be quoted as *"D9's result."*** Human Lead ruling,
> 2026-08-16 (`0090`). ***SUPERSEDES `0074` ruling 5's framing — "USE THE STRICT KEY AND REPORT THE
> LOOSE COUNT ALONGSIDE" — under which STRICT WAS THE ANSWER and loose was context.***
>
> **The ruling is `0074` r5's own reason carried one step further:** the loose count publishes **for
> exactly one stated reason — it BOUNDS HOW WRONG STRICT COULD BE** — and *"a quantity published
> because it bounds another **is an endpoint**, not a footnote."* Under the old framing **the endpoint
> was printed and the interval was not**, which invited every reader to take strict's `0` as the answer.
> *(`0078` §3 had already run this argument once, extending the loose count to half (b).)*
>
> **DIRECTION IS PART OF THE LABEL AND IT IS NOT SYMMETRIC**, and **the error runs OPPOSITE to D9's own
> lower-bound caveat**, which is why the interval publishes rather than being resolved away.

**THE BOUND APPLIES TO EVERY D9 QUANTITY WITH BOTH FORMS** — complementary pairs **`[0, 75]`**,
half (a) **`[0, 6]`**, half (b) **`[0, 27]`**. *(`0090` §2 flags this as ONE READING of *"applied to
this half,"* singular; both arms implement the broad reading and say so at the point of use, on `0078`
§3's ground that a bound for one half and a point estimate for the other **leaves the reader unable to
bound the total**. **It narrows if a single half was meant**; arm a names its §5.5 bound table as what
would change.)*

**TWO GUARDS RECORDED WITH THE RULING:**

1. **The third key is not an endpoint** (above).
2. ***A ZERO FLOOR IS NOT AN ABSENCE OF EVIDENCE.*** `0` is a **measured floor on a stated coverage**,
   and **the coverage publishes beside it, or the bound is indistinguishable from a check that looked
   nowhere.** *(And three of arm a's coverage counts were wrong, mislabelled or unreconciled at `0087`
   §2 — which is why the guard is not rhetorical.)*

**THE RANK-3 TIE-BREAK IS UNRULED AND THE TIE IS OCCUPIED — residual 7.** `secondchance` (8) and
`theisland` (7) are unique at their counts and **both arms reproduce them exactly.** **Third place is a
SIX-WAY TIE at 6** — `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor`. ***`0088` §3
named `maigret`; NEITHER ARM PICKED IT***, and one publishes `blackout` under
ascending-key-after-descending-count. **Both arms list all six; every key at every rank publishes under
both bases, so nothing is lost while it is open.** Red Team's position: **publish all six and retire
*"third-largest"* rather than invent a convention.** *"A spec gap inside the ruling that closed a spec
gap."*

**And a genuine ONE-PAIR divergence, reported not reconciled:** arm a's D9 candidate split is
`435,642 + 8,834 + 281,626 = 726,102`; arm b's is `435,643 + 8,834 + 281,626 = 726,103`. **Two classes
agree exactly; the S1-only class differs by 1.** **No entry recorded it before `0089` §3, because the
totals had been read as differing by the whole S3-only gap.**

### THE TWO ISOLATION RULINGS — `0095` and `0096`. ***READ THEM TOGETHER OR THE PAIR READS AS A CONTRADICTION***

> **`0096` ruling 2 WITHDREW PART OF `0095` §1.** Recording either alone leaves this memory asserting a
> rule the log has already narrowed — the exact shape that produced the wrong ruling at `0051` §2.

**`0095` — A CROSS-ARM CHARACTERISATION NEVER ENTERS A LAUNCH INSTRUCTION.** Recorded in `CLAUDE.md`,
2026-08-16, found by Red Team's ninth pass. **An arm's launch instruction states the SPEC and that
arm's OWN defects. It never states what the other arm does, publishes, splits, names or reports.**

- **`## Dual implementation` says neither instance sees the other's work, and A LAUNCH INSTRUCTION IS A
  WAY FOR IT TO SEE IT** — **worse than reading the folder**, because **the receiving arm is
  structurally FORBIDDEN from re-measuring what it was told.** A relayed characterisation is **a
  measurement with an expiry date its holder cannot check**, so it can only go stale.
- ***IT WENT STALE IN ONE BUILD.*** A Red Team eighth-pass characterisation of arm b's falsifiability
  headline was relayed into arm a's launch instruction; **arm a published it as an arm-against-arm
  divergence** while **arm b's current build published the same 6 + 1 + 2 split** and named exactly
  which side the third member falls on. **Arm a struck the claim entirely and did not replace it, which
  is correct — any corrected characterisation would breach the same rule.**
- ***A FABRICATED DIVERGENCE IN A GATE DELIVERABLE IS WORSE THAN A MISSED ONE:*** it pre-empts the one
  authority permitted to make cross-arm statements — **the Human Lead's diff.**
- **Where a Red Team finding is inherently comparative, the finding goes to the Human Lead and only the
  non-comparative half reaches the arm.**

**`0096` RULING 1 — A DELIVERABLE ASSERTS ONLY WHAT ITS OWN ARM MEASURED.** Human Lead, 2026-08-17, in
`CLAUDE.md`. **Its own figures, its own inputs, its own limits — and nothing else.** **Not** the state
of other steps or gates, **not** the other arm, **not** the shared controls, **not** the study as a
whole.

- **The ground: an arm CANNOT KNOW those things.** It measures a surface at one instant and publishes
  into a file **that is never re-read against the world**, so **every such claim is expiry-dated from
  birth.** **This is the `## Derived figures` provenance rule one category up** — *"a statement about a
  surface the arm does not own is unreadable the same way and worse, because it reads as a finding."*
- **Three consecutive passes found a stale one and the tenth found worse than stale:** arm a's
  deliverable told its reader `check_surfaces.py` **exits 1** when it exits **0**. **True when the arm
  measured it, false by the time it was read.** ***And arm a's behaviour was correct throughout*** — it
  reported the failure with its cause named rather than removing a citation to go green. **The defect is
  that a control's exit status was publishable in a permanent deliverable at all.**
- **Excluded concretely:** control exit statuses (to the Human Lead and to `logs/`); the disk state of
  other surfaces; build-history narration beyond a stamp and a run-record pointer; and **whether any
  step or gate is approved, including this one.**
- **Still required, because the arm measured them:** its own defects, its own open items, its own
  divergences from the spec. **An arm that notices something wrong on a surface it does not own REPORTS
  it and does not publish it as a finding.**
- **Why it is the ruling that mattered most:** the tenth pass identified the generator — arm a's
  waterfall was **826 lines of which ~120 was measurement**, and **each build appended more.**
  **Two of that pass's three blockers were regenerations of defects the ninth pass had closed.**
  **`0096` removed the CATEGORY rather than the instances.**
- ***ITS BOUNDARY WAS ONE NOTCH TOO NARROW*** (`0097` §3): it was scoped to *"a **gate deliverable**,"*
  and `artifacts/` holds two files that are not gate deliverables — **the read-backs** — where the
  expiry-dated-assertion class survived. Red Team's framing, adopted: *"the ruling was correct and its
  boundary was one notch too narrow."*

**`0096` RULING 2 — `decisions/` MAY CARRY CROSS-ARM CONTENT.** ***This WITHDRAWS `0095` §1's exclusion
of "a decision entry."***

- **The ground: a ruling has to record what each arm found in order to explain why it was ruled.**
  Forbidding cross-arm content in `decisions/` would mean **a ruling cannot cite its own evidence.**
- ***AND IT NAMES WHAT THE ISOLATION RULE IS FOR***, which the earlier form did not: **it exists to
  stop the arms COPYING EACH OTHER'S IMPLEMENTATION, not to keep a number the Human Lead has already
  ruled on out of reach.**

| Route | Status |
| :--- | :--- |
| **An UNRULED characterisation relayed into a LAUNCH INSTRUCTION** | **FORBIDDEN, unchanged** (`0095` §1) — a measurement the receiving arm **cannot check**, and it went stale in one build |
| **A RULED figure in a DECISION ENTRY** | **PERMITTED.** It has already been through the Human Lead's diff — **a spec input, not a peek at the other arm's work** |

- **The leak is made EXPLICIT rather than accidental: both `analytics-engineer` files now state that
  decision entries may contain cross-arm content**, so an arm reading `decisions/` **knows what it is
  reading and is not stumbling into a route around isolation.**
- **An arm may cite such content, naming `decisions/` as the source. It may NEVER open the other arm's
  output folder, and it may NEVER treat a cross-arm figure as something it measured.**
- ***This resolved Red Team's tenth-pass F1 in the direction it could not choose for itself*** — it
  correctly found that `0095` plugged one route and left another open, **but whether that route should
  be open is a judgement about the study's purpose, not about the text. It is open, deliberately, and
  now labelled.**

### TWO STANDING RULES THIS BLOCK ADDED

> **1. PROVENANCE — EVERY COUNT AND EVERY INVARIANT NAMES THE BUILD IT WAS MEASURED ON, not only its
> population** (`0078` §2, widened by `0079` §2). **`0047`'s rule one layer down: which BUILD produced
> it.** *"A count without its provenance can be correct when written and wrong when read, because the
> pipeline moved underneath it and nothing in the text says which pipeline it belongs to."*
>
> **PARTIAL APPLICATION IS WORSE THAN NONE.** `0078` labelled two figures; **two labelled figures imply
> the other counts and the **nine** invariants did not need it** — the reader takes the labels as marking
> the exceptional cases rather than the rule. Step 8's required-counts section alone runs to 24 bullets.
>
> **Scope limit, stated three entries running (`0078` §4, `0079` §5, `0080` §4): promoting provenance —
> or the invariant-coverage rule — to a project-wide `CLAUDE.md` control is a SEPARATE RULING AND IS
> STILL NOT TAKEN.** It is a Step 8 requirement only.

> **2. GENERATED FILES AS CHECKS — a check nobody can see is not a check** (`0082` §3, **in
> `CLAUDE.md`**). **A generated file that functions as a check is COMMITTED** — a verification living
> only in a working tree verifies nothing anyone else can rely on, and **it is invisible to all eight
> propagation surfaces, which is where the defects this project keeps finding actually hide.**
>
> **Condition, not optional: it states WHAT GENERATED IT and WHEN. A generated file without its
> provenance is worse than no file, because it is trusted.** Governs the generated artifacts that
> already exist, including `src/step7_regenerate_derived.py`'s output blocks and stamps.

### Step 8b — output schema. **Propagated at `0066`; NOT written. UNBLOCKED at `0098` and NOT LAUNCHED.**

> **`0098` §5: Step 8b and Step 9 are UNBLOCKED and NOT LAUNCHED.** `CLAUDE.md`'s handoff rule governs
> — **a chained step returns to the Human Lead before the next one starts**, and **no agent begins
> either on the strength of the approval entry or of this memory.**
>
> **Carry into the schema: `p_at_bound` IS THREE-VALUED** — `TRUE` 1,246 / `FALSE` **17,895** / null
> 177,513 on APPLY position 5. **The empty class is CLASS 1, the coextensivity gap, not the column.**

**Owner Analytics Engineer, Mode Chained, sits behind the Step 8 gate.** It **had been defined in a
prior session and existed in NO FILE** — neither `task-sheet.md` nor either agent file. Two amendments
at propagation: ~~**the key is `W` ALONE**~~ ***SUPERSEDED TWICE — `0102` added `clock_origin`, `0111` (E2) added `producing_step`; THE KEY IS ~~`(W_days, clock_origin, producing_step)`~~ — ***and a FOURTH dimension was added at `0114` (E14): `(W_days, clock_origin, producing_step, adopted_rule_revision)` (`0116`).*** What the amendment ruled — no liveness parameter in the key — stands*** (there is no liveness threshold), and **Step 9 publishes TWO
bounds on TWO populations**, never one field with a population flag. **Never-started has NO conditional
sub-interval, structurally, and the schema must SAY SO rather than omit the field — an absent field and
an inapplicable one must not look alike.** On DERIV the never-started bound is **degenerate,
`[6.2055%, 6.2055%]`**, and **a zero-width bound must not read as missing data**. **No conversion
layer** — a conversion layer is a second definition of every figure. **The placeholder must be
unmistakable as a placeholder; a placeholder that reads as data is the failure mode**, and it reaches
Step 16. **This is why the 89 names are fixed BEFORE the schema exists.**

## Step 7 — the liveness vocabulary. **Gate APPROVED, `0064`.** Full arc in [[gate-step7-liveness]]

### The candidate rules, and the status of each

| Name | Rule | Status |
| :--- | :--- | :--- |
| **ALT-BROAD** | not live iff **no insertion after `τ1`** AND **NOT Continued** | **ADOPTED `0048` → superseded by ALT-MATCHED `0052` → RESTORED `0054` → APPROVED `0064`, 2026-08-13.** The rule, **with the started-and-left floor widened to cover the 90**. **Uncontested by Red Team from review 5** |
| **ALT** | not live iff no insertion after `τ1` AND **`\|A\| = 0`** | **SUPERSEDED** by `0048`. Guarded one null of two |
| **PF-LIMIT** | not live iff **no insertion after `τ1`** (alone) | **SUPERSEDED** by `0046`. Deleted 751 pairs with no stated warrant. **`0063` §1: PF-LIMIT IS the "drop conjunct 2" alternative** — Red Team's fifteenth review proposed it as *"the one nobody has priced"*, and it was adopted at `0041`/`0042` and superseded before ALT-BROAD existed. It excludes **652 Continued pairs on evidence they demonstrably produced** |
| **ALT-MATCHED** | one silence test per null, at the instant that null is read — silence at `τ1` for never-started, at **`τ2`** for started-and-left | **PROPOSED and recorded (`0050` §4) → ADOPTED (`0052` §1) → REVERTED (`0054`).** See the full history below. **Never cite it as the rule; never drop it from the record** |
| *PF-BRACKET* | instant at or before `τ1` **and** one after — the literal reading of `0041` §4's withdrawn wording | **Never a candidate.** Priced at 18,903 exclusions from 1,434 of 2,402 accounts, to show what the wording cost |

### ALT-MATCHED — the full history, because the status line moved three times in one day

**Superseded status, never to be restated as current: "RECORDED, NOT ADOPTED (`0050` §4)".** That was
this file's entry until 2026-08-13 and it was already two rulings stale when Red Team's eighth Step 7
review found it.

| Stage | Where | What happened |
| :--- | :--- | :--- |
| **Proposed** | `0050` §4 | Named as the form that would close the residual channel, and **deliberately not adopted** |
| **Adopted** | `0052` §1 | On Red Team's **sixth** HOLD. Warrant: ALT-BROAD's own argument — *a pair silent through `[τ1, τ2)` cannot produce the evidence the Continued test reads* — **holds identically at `τ1 + ε` for any ε < 91 days**, so ALT-BROAD *"cut a continuous failure mode at one end."* Both arms reran and confirmed all three expectations: APPLY exclusions **703 → 793** (604 NS + **189** S&L, 256 accounts), never-started bound unchanged, DERIV **188** |
| **Gate amended for it** | `0053` | `0021` ruling 2 amended to *"an insertion after the window FOR THE QUESTION BEING ASKED"*; `0048` §9's *"insertion after `τ1` ⟹ live"* withdrawn |
| **REVERTED** | `0054` | On Red Team's **seventh** HOLD. **`0053` withdrawn in its entirety, `0021`'s amendment reverted, `0048` §9 restored** |

**Why it was reverted — three grounds, and the first is decisive:**

1. **It bought nothing numerically.** On **all three identified sets**, ALT-BROAD-with-a-covering-floor
   and ALT-MATCHED are **numerically identical**: S&L floor 18,952 → 9.6372%, S&L ceiling 19,745 →
   10.0405%, Continued ceiling 144,933 → 73.6995%, never-started [16.6633%, 16.9704%]. **All it moved
   was the point estimate** — S&L 9.7177% → 9.6762% — by deleting the 90 least-robust rows, **and it
   paid for that with an amendment to an approved gate.**
2. **`0053`'s premise was false.** It rested on *"the ruling has since been read as 'after `τ1`' only
   by accident of when it was written."* **`0034` — the entry that CREATED the second window, the same
   date — ruled the anchoring in terms**, and `0051` re-affirmed it with both windows in view. `0053`
   amended `0021` and withdrew `0048` §9 **while leaving `0034` standing, uncited and unmentioned.**
3. **The warrant was false for the very pairs it was adopted to capture.** A record inserted at instant
   `s` can carry any `watched_at ≤ s`, and `0021` Adoption 3 keeps post-dated records — so an account
   last active at `s ∈ (τ1, τ2)` **could** have produced Continued evidence.
   **And the continuity argument is symmetric** — it proves **no** instant in `[τ1, τ2]` is warranted,
   not that `τ2` is. `0054` §3 names the error class: *correcting a predecessor by overshooting into
   the mirror-image defect.*

> **THE MARGIN ARGUMENT IS WITHDRAWN (`0055` §2) AND MUST NOT BE RESTATED.** `0054` §3 supported
> reason 3 with *"the 90 have **p5 margin 1.7 days, minimum 0.13** — demonstrably alive for ~89 of the
> 91 days."* **That is the tail, and the record's own median for the same 90 is 44.5 days**, so for half
> of them roughly half the Continued window is unobserved. **p5 supported the claim, the median
> contradicted it, and only p5 was quoted.** Instance B reproduced **p5 = 1.6552 and median = 44.5272 on
> the same 90 pairs**, confirming the cherry-picking arithmetically.
>
> **The correct ground carries NO margin statistic at all.** A floor is a **worst case, not an
> expectation**: the question is whether a channel pair *can* in truth be Continued, and it can — even
> at margin 0.13 days it could have completed S2 inside the unobserved remainder, since the Continued
> condition reads **distinct episodes** and a single binge clears it. **Admissibility sets an endpoint;
> plausibility does not enter. p5 = 1.7 and median = 44.5 are BOTH inadmissible.** Both arms went
> further and argued the whole class out of endpoint justification — A: admissibility is **binary**,
> a margin is **continuous**, so no margin value can discharge the question (*"would the statistic at any
> value move the endpoint? If not, it is commentary"*); B: **admissibility is a property of the support,
> plausibility of the measure**, and `p5 = 1.7` removes **zero** pairs from the admissible set — and it
> would **reintroduce an unowned threshold into the one step whose history is the removal of exactly
> that shape.** Margin statistics belong in Step 14 as a statement about **resolving power** only.

**`0052` §4 declined to widen the floor because that *"would have been the fifth consecutive bound with
a non-covering endpoint."* `0054` §1: that is exactly backwards — widening to 18,952 is what MAKES the
endpoint covering.** The rejection reason named the defect the alternative repairs.

**The anchor sweep, `0054` §4 — neither arm was asked for it and it is the reason the bound is widened
rather than a cut chosen.** Exclusion count against the silence anchor, swept `τ1 → τ2`, never-started
held at `τ1` (`src/step7_anchor_sweep.py`, zero API calls):

| Days past `τ1` | 0 | 9.1 | 27.3 | 45.5 | 63.7 | 81.9 | **91.0** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY S&L | **99** | 108 | 120 | 143 | 154 | 174 | **189** |
| APPLY total | **703** | 712 | 724 | 747 | 758 | 778 | **793** |
| DERIV S&L | **99** | 108 | 120 | 143 | 154 | 174 | **188** |

**Smooth and monotone. No elbow, no plateau, no natural cut anywhere in the interval** — which is why
**neither endpoint is warranted by the data.**

**ALT-MATCHED's own figures, retained as history and never to be restated as current:** APPLY
exclusions **793** (604 + **189**, 256 accounts) · DERIV **188** · per-arm **604 / 621 / 713 / 754 /
793 / 793 / 878 / 952** · S&L component **119 / 127 / 159 / 179 / 190 / 189 / 214 / 236** (not
monotone) · coupling **1.58× total, 1.98× S&L** · frozen-D10 totals **874 / 990 / 1,192 / 1,466** ·
DERIV never-started share **6.2134%**. **`0053`'s bound-versus-sampling ratios (NS 27.4%, S&L 52.7%,
Continued 27.9%) are withdrawn** — computed off B's 0.4033 rounding artifact (`0054` §6).

**"NOT Continued" means Step 1 §7 as amended by `0034`** — the negation of
`|A| ≥ 1 ∧ F2 ∈ A_H ∧ |A_H| ≥ ceil(0.90 × L2)` — so it covers **both** Never started and
Started-and-left. **`|A| = 0` alone is the superseded ALT form.** And `|A| = 0` is §7's Never-started
condition, **not** "no S2 evidence at all" — the competing reading selects a different set.

### The two populations, named once and used everywhere (`0046` §0)

| Name | Definition | Pairs | Who reads it |
| :--- | :--- | ---: | :--- |
| **DERIV** | Step 5 waterfall **line 4 (152,126) less D10**. **Requires S2 evidence** | **147,370** | Step 7 derives here |
| **APPLY** | **line 1 (201,900) less D10**. **What Step 8 filters at position 6** | **196,654** | Step 8, Step 9, Step 13 |

**Exclusions under ALT-BROAD at `W = 108`, restored by `0054` §7: 99 on DERIV (73 accounts, 0 NS + 99
S&L) · 703 on APPLY (216 accounts) = 604 never-started + 99 started-and-left.** Per-arm on APPLY, D10
**re-derived** at each arm:
**537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** at `W` = 38/46/77/91/107/108/150/213 — factor 1.61.
**S&L component separately: 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148 — factor 2.85, growing faster
than the rule itself.** On DERIV the top arm is **147, not 148**.

**Superseded counts, never to be restated as current:** ALT's **604** total and **0 on DERIV**; ALT's
per-arm **485 → 716**. *(Under ALT-BROAD, 604 survives only as the never-started **component** of 703
— **and, separately and coincidentally, as arm a's 7-account skipped-class pair count.** See the trap
table.)*

> **CORRECTED 2026-08-16. This sentence formerly also listed PF-LIMIT's `751` (DERIV) and `1,355`
> (APPLY) as *"never to be restated as current."*** **`0085` §5 makes both MANDATORY in both arms on
> both populations** as the **silence-test-alone term** in line 6's marginal decomposition —
> `1,355 − 652 = 703` and `751 − 652 = 99`. **PF-LIMIT the RULE is superseded; the COUNT is the same
> arithmetic and is now required.** A memory row reading *"never restate"* against a spec clause
> reading *"both arms publish both"* is the shape that has already produced one wrong ruling here.

### The bounds — Step 9. STATE THE POPULATION AT EVERY USE.

**On APPLY, n = 196,654, both endpoints on that one denominator:**

| Bound | Interval | Width | Over |
| :--- | :--- | ---: | :--- |
| **Never-started** | **[16.6633%, 16.9704%]** | **0.3071 pp** | the **604** never-started exclusions only |
| **Started-and-left** | **[9.6372%, 10.0405%]** | **0.4032 pp** | **all 703 exclusions PLUS the 90 channel pairs** = 793 |
| *conditional sub-interval* | ***[9.6372%, 9.7333%]*** | ***0.0961 pp*** | *the **99 and the 90** — **NOT A BOUND**; the conditioning constrains the **604** only* |
| *~~superseded sub-interval~~* | *~~[9.6830%, 9.7333%]~~* | *~~0.0503 pp~~* | *withdrawn `0056` — correct only under the un-widened floor* |

| **Continued** | **[73.2962%, 73.6995%]** | **0.4032 pp** | 144,140 → 144,933. **Same span as the S&L bound — the same excluded pairs — so the two widths are ONE NUMBER** (`0063` §2) |

**On DERIV, n = 147,370:**

| Bound | Interval | Width | Over |
| :--- | :--- | ---: | :--- |
| **Never-started** | **[6.2055%, 6.2055%]** | **0** | **DEGENERATE** — the dual control is `x = x` here. 9,145 → 9,145 |
| **Started-and-left** | **[11.3015%, 11.4291%]** | **0.1276 pp** | 16,655 → 16,843: the 99 exclusions **plus the 89 DERIV channel pairs** = 188 |
| **Continued** | **[82.3655%, 82.4930%]** | **0.1276 pp** | 121,382 → 121,570 |

**EVERY WIDTH IS A COUNT OVER A DENOMINATOR, `(ceil_n − floor_n) / n` — never a difference of two
rounded percentages** (`0063` §2). `derive()` did the latter and produced `APPLY.sl.width 0.403246`
against `APPLY.cont.width 0.403247` — **one quantity, two values, an ulp apart, from the same 793 pairs
on the same 196,654.** The register held the diagnosis (`0.4033` is *"a rounding artifact"*) **and the
generator committed the disease.** Two asserts now enforce it, including that the S&L and Continued
widths are equal. **`bb-b.json`'s `0.403245 → 0.403246` at `0062` landed on the exact form by
coincidence, not by construction.**

### The `W` ARM GRID — 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 (`0075`)

**`0075` and `task-sheet.md` Step 13 are the FIRST statement of it in any file.** Step 6's deliverables
say `[37, 107]` and `[37.70, 107.71]`; **neither says 38.** Step 13's bullets constrain the arms without
enumerating them, and the grid travelled only as the **index of a reported series** — which is a
reading, not a specification. **Every Step 13 figure is indexed by the arm set, so two instances on
different grids produce tables that CANNOT BE DIFFED AT ALL**: a failure of the dual implementation
itself, not a wrong number inside it.

### D3′'s CLEARED SHARES — 99.53% at `W = 46` → 97.73% at `W = 213` (`0075`)

**On Step 8's right-censored populations**, measured **independently and identically by both Step 8
instances**. ***SUPERSEDED: `0034`'s 95.98% → 91.34%***, measured on the amendment's **uncensored
estimation sample** and carrying **no population at the point of use**. **Direction and shrinkage stand;
the level does not.** `0068` §2a could fix the denominator and not the level — which is why it needed a
ruling rather than a restatement.

### The bound's SCOPE QUALIFIER — it publishes WITH the bound, every time (`0062` §4)

> **The bound is covering with respect to INSERTION-DORMANCY, exhaustively; open only across CHANNEL
> CLASSES (D4, D9).**

**The rule it states:** *concede every pair dormant before the instant at which its own state-defining
null is read* — `τ1` for never-started, `τ2` for Continued. **Exhaustive, not open-ended:** every pair
either was inserting through its test instant or was not, yielding **32,769** and **18,952** with **no
residue**. **D4 and D9 publish alongside, never folded in.** It exists because pure admissibility **has
no stopping rule** (instance A, `0055` §5c), so *"covering"* full stop would be an overclaim.

**Flag any publication of the bound that omits it.** It lived **only in `decisions/` for six entries**
while Step 9 publishes the bound it qualifies; `0062` put it on all eight surfaces via `STATEMENTS`, so
it cannot be edited out of one half. **Carried defect (`0063` §3 item 2.4): it exists in FIVE wordings
across eight surfaces, and the `analytics-engineer` pair carries the FIRST CLAUSE ONLY** while
instructing that any table carrying the bound carries the qualifier. **No control catches this** — a
missing qualifier is neither a wrong number nor a withdrawn phrase; Red Team found it by grep on an idea.
The `REQUIRED_PHRASES` mirror of `WITHDRAWN_PHRASES` is the named fix and **is not built**.

### The SIX ratios — bound ÷ account-clustered sampling width. TWO CONVENTIONS, REPORTED NOT RECONCILED

**`CLAUDE.md` requires divergences be reported and not reconciled. `0057` §2 reconciled these; `0058`
REVERTED that.** The two arms divide by different denominators, so **one value is right in one arm and
wrong in the other** — which is the case `SUPERSEDED_IN` exists for, and it is why `0.5090` sat wrong in
arm a through two reviews. **The spec fixes neither convention** (residual item 9).

| | **arm a** — divides by the **floor endpoint's own bootstrap CI** | **arm b** — divides by the **CI of the under-the-rule point estimate** |
| :--- | ---: | ---: |
| **APPLY started-and-left** | **0.5304** = 0.403246 / **0.7602** | **0.5090** = 0.403246 / **0.7922** |
| **DERIV started-and-left** | **0.1309** = 0.127570 / **0.9744** | **0.1310** = 0.127570 / **0.9737** |
| **APPLY never-started** | **0.2818** = 0.307138 / **1.09** | **0.2721** = 0.307138 / **1.12872** |
| *DERIV never-started* | *0.0* | *0.0* |

**AN ARM MUST RUN ONE CONVENTION** (`0060` §1). Arm a's published **`0.2813` is SUPERSEDED IN ARM A** —
it is `0.307138 / 1.092`, and **1.092 is the under-the-rule CI, arm b's convention**, so arm a was
running two conventions in one six-line block while its S&L ratio used the floor-endpoint CI.

**The two DERIV never-started ratios are both exactly `0.0` by degeneracy and are DELIBERATELY NOT
REGISTERED** — `0.0` matches somewhere in nearly every file, so a row would flag everything and disarm
nothing. **Stated so two silently missing entries are not mistaken for an omission.**

**Withdrawn, and it was published twice:** *"the never-started ratio was correctly left divergent at
`0.2813` against `0.27211`, which is the proof this one should have been"* — **false.** That pair was
**one convention on two arms' bootstraps**, which is why it sits 0.009 apart while the genuine
two-convention pair sits 0.021 apart. **The figure cited as proof was itself an instance of the defect it
was cited to certify**, and `0060` §2 names it as *"the same failure as adopting Red Team's 73.6537%
without checking its population at `0051`."* It is now a **`WITHDRAWN_PHRASES` entry** keyed on
*"which is the proof"*. Also withdrawn: `0053`'s ratios **NS 27.4% / S&L 52.7% / Continued 27.9%**
(off `0.4033`), `0052` §6's **45%**, and `0055` §6's **50.9%** as a single reconciled figure.

**The started-and-left floor was WIDENED by `0054`, and this is the correction that matters most.**

- **Superseded, never to be restated as current: `[9.6830%, 10.0405%]`, width `0.3575 pp`** (APPLY).
  Its floor did not cover the case the rule guards against: **if the 90 channel pairs in truth
  continued, the started-and-left numerator is 18,952 and the floor is 9.6372%** — 0.0458 pp below the
  published 9.6830%, on a bound 0.3575 pp wide *(both SUPERSEDED: 9.6372% on 0.4032 pp)*. By `0047` §3's own test that was **a non-covering
  endpoint, and it would have been the fifth consecutive one**.
- **Width is `0.4032 pp`, not 0.4033.** `793 / 196,654 = 0.40325%` exactly (instance A). **`0.4033` is
  a rounding artifact differenced from rounded endpoints** (instance B), reported as an unreconciled
  divergence at `0054` §6 — **and then published by `0054` §7 itself, in the entry that named it as an
  artifact.** Recorded in [[open-items-and-contradictions]].
- **The DERIV started-and-left bound was missing everywhere until 2026-08-13** and is being propagated
  into the spec files now. Its width `188 / 147,370 = 0.12757%` covers 99 excluded + 89 channel pairs.

**The never-started ceiling equals the unfiltered share as an identity** — but **by the route
`0049` corrected:** it returns **only the 604** to the never-started count, **not** every excluded
pair. *"Returning every excluded pair as a decliner"* gives an **unattainable 17.3279%**, because the
99 have `|A| ≥ 1` observed. **ALT-BROAD's exclusion set is no longer a subset of never-started, which
is why the route matters.** Both endpoints attainable, verified in **integer** arithmetic.

**`9.6830%` IS NOT A FALSE-POSITIVE TRAP — that registration is WITHDRAWN (`0056`).** It was recorded
here and in `0055` §3 as *"both the superseded bound floor and the legitimate floor of the conditional
sub-interval."* **The second half is false.** The sub-interval's conditioning constrains the **604** and
says nothing about the **90**, so **its floor moved with the bound floor to 18,952 → 9.6372%.** Under
the adopted rule **`9.6830` has no legitimate reading anywhere** — the same status as `0.4033`.
**Registering it as exempt disarmed the grep control against the one string it most needed to catch, on
four surfaces, in the section that created the control.** Treat every hit on `9.6830` as a defect.

**The conditional sub-interval is [9.6372%, 9.7333%], width 0.0961 pp, over the 99 AND the 90, and must never be recorded as a bound.** *(It was described here as "the 99-only interval"; that description is what produced the stale floor.)*
It is conditional on every never-started exclusion being truly never-started; **the 604 rest on an
untrusted `|A| = 0` and some may in truth have left.** The two differ by a **factor of seven**. Both
arms reached this independently and **both refused to adopt it themselves** — it would have been the
**fourth consecutive bound** with an endpoint outside the feasible set.

**Superseded bounds, retained only as history:** `0045`'s **[16.7789%, 17.0355%]** (PF-LIMIT, mixed
denominators, floor was not a floor) and `0046`'s **[16.7146%, 16.9704%]** (mixed denominators, floor
0.0513 pp above the case liveness guards against). The internally consistent PF-LIMIT interval was
[16.727%, 17.0355%].

### THREE ceilings, not two — and 73.6537% was never a floor *(and is now SUPERSEDED by 73.6995%)*

**This is the entry that caused a wrong ruling, and the correction is the point.**

- **Superseded, never to be restated: *"the Continued FLOOR 73.6537%"*, and *"the TWO ceilings cannot
  both hold: 16.9704 + 10.0405 + 73.6537 = 100.66%"*.** That was this file's text until 2026-08-13.
- **73.6537% is the Continued CEILING on APPLY: `(144,140 + 703) / 196,654`.** It states a population
  and it reconstructs exactly. **Both arms publish it** — `bb-a.md` §5, `bb-b.md` §4.3 — and both JSONs
  carry `ceiling_pct: 73.6537…` *(SUPERSEDED by 73.6995%; both JSONs now carry it, regenerated)*. **This memory mislabelled it a floor and concluded it could not be
  reconstructed; `0051` §2 adopted that diagnosis without checking it against the arms' own JSON, and
  the resulting "correction" left `task-sheet.md` presenting Continued as a point, 73.2962%.** A Step 9
  instance reading that against its own deliverable **would have deleted a correct number.** `0052` §2
  withdrew the correction and restored the ceiling.
- **73.6537% is now itself SUPERSEDED, by `0054`, to `73.6995%` = `(144,140 + 703 + 90) / 196,654` =
  `144,933 / 196,654`** — because the same 90 that widened the started-and-left floor may in truth be
  Continued. **Superseded as an arithmetic update, not as an error.**
- **On DERIV the Continued ceiling is `82.4930%` = `121,570 / 147,370`.**

**The three ceilings on APPLY, and they cannot all hold:**

> **16.9704 + 10.0405 + 73.6995 = 100.7104%**

**Excess `0.7104 pp` = `1,397` pairs = `2 × 604 + 189`.** Mechanism, refined at `0053` §4 and retained
by `0054` because it is rule-independent: **each never-started exclusion appears in ALL THREE ceiling
numerators — excess 2 each — and each started-and-left exclusion in TWO — excess 1 each.** The earlier
gloss *"counted once in every ceiling"* is too coarse and is withdrawn.

**They are alternative worst cases over one set, not simultaneous ones.** The old text said *"over the
same 604 pairs"*; the set is now 604 never-started plus 189 started-and-left.

### Shares and movements — APPLY, under ALT-BROAD, at `W = 108`

**16.7231 / 73.5592 / 9.7177**, summing to 100.0000. Movement against no filter: **−0.2474 / +0.2630
/ −0.0156 pp**, summing to zero. On DERIV: **+0.0042 / +0.0554 / −0.0595 pp**.

**Step 14 bias 2 is UP on DERIV and DOWN on APPLY, and the published direction is APPLY's.** The sign
is **population-scoped and both directions must be carried** (`0045` §4.1). Mechanism of the DERIV UP:
line 4 requires S2 evidence, so the 604 never-started pairs with no S2 record anywhere exist **only**
on APPLY, and excluding them is what pulls the share down there.

### The channel figure — 52.4%, not 70.3%

**Superseded, never to be restated: *"ALT-BROAD closes 703 of 1,000 such pairs (70.3%) and leaves
29.7% open"*** (`0050` §4). **Corrected at `0052` §3.**

**That denominator pooled two categories with different coverage.** `0050` §4 reported **297 pairs** in
the channel — **207 never-started + 90 started-and-left**. **The 207 never-started pairs are not in the
gap:** never-started is the null `|A| = 0` read at **`τ1`**, and **every one of the 207 has an insertion
after `τ1`** — its null is exactly what `0021` licenses. **The warrant ALT-BROAD added implicates only
the started-and-left pairs.**

> **On the implicated set alone: ALT-BROAD closes 99 of 189 — 52.4%, leaving 47.6% open.**

**The remaining 90 are the pairs the widened floor now covers**, rather than the pairs ALT-MATCHED
deleted. Channel shape, unchanged: last insertion at median **51.4 days** past `τ1`, p90 **85.1**, max
**90.9** — filling the window.

### Deleted thresholds — never to be quoted as operative

**4 days · 504 · 632 · 914 · 1,293.** Also 787, 790, 975, 2,200 and the interval [528, 787] as
threshold quantities. **Watch for a collision: `632` also appears legitimately as the frozen-D10
never-started COMPONENT at `W = 125`** (`0050` defect 5, re-affirmed as a known false-positive trap at
`0051` §3 item 9) — a different quantity that happens to equal the deleted threshold. Frozen-D10
**totals** are 746 / 823 / 918 / 1,117 at `W` = 125/150/180/213, of which **632 / 684 / 753 / 881 is
the never-started component**; **125 and 180 are not in the mandated grid**, so only 684 and 881 are
comparable to it.

### Known false-positive traps — a blind grep produces WRONG ANSWERS on every string below

> **STRUCTURAL NOTE, 2026-08-13.** This table was previously **orphaned** — its header row sat three
> paragraphs above its data rows, so it rendered as broken. `0063` §3 item S7 records *"the glossary trap
> table is structurally orphaned"* as a carried defect. **Repaired here.** The prose that caused it now
> sits below the table, where it belongs.

> **RE-VERIFIED ROW BY ROW 2026-08-16, against the ADOPTED rule and against the current arm
> deliverables.** `CLAUDE.md`: *"Registering a string as a false positive DISARMS the control against
> it. Do it only when the legitimate reading is verified live under the adopted rule, and withdraw the
> row the moment it stops being."* Every row below was checked against a named file this pass.
> **Rows withdrawn in this pass are listed after the table, not deleted silently.**
>
> **NOTE ON SCOPE, and it is the whole reason the table grew.** Rows above the divider are **Step 7**
> and mirror `src/step7_register.py`. Rows below the divider are **Step 8** figures, and
> **`src/step7_register.py` does NOT hold them as numeric entries** — its Step 8 coverage is
> `SUPERSEDED_STRINGS` (textual needles) and `SURFACE6_LINE_LOCAL_CONTROLS`. **So for the Step 8 rows
> this table is not a mirror of anything; it is the only place they are written down**, which is
> exactly the two-registers hazard `0059` B3 forbids. **Flagged for the Human Lead, not resolved here.**

### Step 7 rows — these mirror `src/step7_register.py` and the source governs

| String | LEGITIMATE reading | ILLEGITIMATE reading |
| :--- | :--- | :--- |
| **`632`** | Frozen-D10 never-started **component** at `W = 125` (`0050` d5, `0051` §3 item 9). **Verified live** at `artifacts/step7-liveness-bb-a.md:411` | A **deleted threshold** in days. Deleted thresholds: **4 · 504 · 632 · 914 · 1,293** |
| **`703`** | **TWO readings now, both current, and they are a COINCIDENCE.** (i) ALT-BROAD's **APPLY liveness exclusion count** (604 + 99, 216 accounts). (ii) **Distinct S2 episodes in the SEPARATING interval `[τ1, τ1+24h)` on APPLY position 5** — `artifacts/step8-waterfall-a.json:2095` and `artifacts/step8-invariants-b.json:219`, **both arms**, `0089` §2(a) / `0091` §1. Reading (ii) sits beside `[τ2, τ2+24h)` = **303** and the DERIV pair **595 / 261** | Quoting (ii) as the exclusion count, or (i) as evidence about the half-open form. **They are unrelated quantities that happen to be equal** |
| **`793`** | **ALT-MATCHED's** APPLY exclusion count — history only | Anywhere as the current expected count. `0054` §5 fixed *"EXPECT 793"* in both `analytics-engineer` files |
| **`16,744`** | **Three** legitimate readings: post-liveness S&L **count** on **147,271** → 11.3695% (`bb-a.md:109`); the same count at `step7-sensitivity-b.md:76`; and the DERIV floor under **extreme NONE** in the two-extremes table | the **adopted** DERIV S&L floor — that is **16,655 → 11.3015%** |
| **`19,042`** | post-liveness started-and-left **POINT ESTIMATE** on APPLY. Also in `waterfall.APPLY_final_states` and `ordering_commutation_check` | the S&L bound **floor** — that is **18,952**. **`0057` §1: a value-wide substitution would have corrupted three point estimates and the commutation check.** The patch matched on **key as well as value** |
| **`0.0672`** | DERIV exclusion **SHARE OF POPULATION**, `99 / 147,370` = 0.0672% (`bb-a.md:65`) | the DERIV bound **width** — that is **0.1276 pp** |
| **`0.3575`** | APPLY exclusion **SHARE OF POPULATION**, `703 / 196,654` = 0.3575% (`bb-a.md:107`, `bb-b.md:93`) | the S&L bound **width** in pp — that is **0.4032**. Same string, two meanings, one live |
| **`0.5090`** | **arm b's** APPLY S&L ratio, `0.403246 / 0.7922` — **CURRENT AND CORRECT THERE** | in **arm a**, whose own is **0.5304**. `SUPERSEDED_IN`, not `SUPERSEDED` |
| **`0.2813`** | **nowhere as arm a's** — it is arm b's convention on arm a's numerator | in `bb-a`. Arm a's is **0.2818**. `SUPERSEDED_IN` |
| **`9.6830` / `11.3619` / `73.6537` / `82.4327`** | **ONLY** as the **extreme-NONE column** of the two-extremes table, and **only in `step7-deriv-floor-check-*`** — the verification arms' deliverables, which are deliberately not on the whole-file allowlist | **everywhere else, every hit is a defect.** Adopted: **9.6372 / 11.3015 / 73.6995 / 82.4930** |
| **`0.0503`** | **NOWHERE (`0057`).** It was the sub-interval width `99 / 196,654` | **every hit is a defect** — the sub-interval is `189 / 196,654` = **0.0961 pp**; the conditioning constrains the 604, not the 90 |
| **`73.3466`** | **NOWHERE (`0057`).** It was the Continued value in the attainable-corner floor row | **every hit is a defect** — with the 90 conceded the row reads **73.3924%** |
| **`0.4033`** | **NOWHERE.** It is B's rounding artifact | anywhere as the bound width — it is **0.4032** |
| **`0.4703`** | **NOWHERE.** arm a's S&L ÷ sampling ratio **pre-widening** | anywhere — it is **0.5304** |
| **`604`** | **TWO readings, both current, and they are a COINCIDENCE.** (i) the **never-started COMPONENT** of ALT-BROAD's 703 on APPLY (191 accounts). (ii) **invariant 8's scope note, arm a**: the **7 accounts skipped on one attempt but yielding data on another** hold **604 position-5 pairs** (119 of them never-started) — `artifacts/step8-invariants-a.json:628`, `0088` | **`604` as a liveness exclusion TOTAL** — that is ALT's superseded answer, and producing it at position 6 **IS a divergence** (`0046`→`0048`) |
| **`1,355`** | **CURRENT** as the **silence test ALONE on APPLY** — conjunct 1 with conjunct 2 not yet applied — in line 6's **marginal decomposition**, `1,355 − 652 = 703`, **mandated in both arms on both populations** (`0085` §5, measured `0086` §4) | **as an EXCLUSION COUNT.** It is **PF-LIMIT's superseded APPLY answer** — the same arithmetic under a rule that was replaced. **The number is the same; only the status of the rule changed** |
| **`751`** | **CURRENT** as the **silence test ALONE on DERIV**, `751 − 652 = 99` (`0085` §5, `0086` §4) | **as an EXCLUSION COUNT** — PF-LIMIT's superseded DERIV answer. Also **`"751 directly observed"` is a withdrawn claim** (`0048`: 652 observed, 99 null-based) |
| **`652`** | **CURRENT, and on BOTH populations.** Continued-and-silent pairs — what the `NOT Continued` conjunct spares. **The same 652 on APPLY and DERIV**, because Continued requires S2 evidence so every Continued-and-silent pair is a DERIV pair (`0086` §4, arm a, unprompted). It is the outcome-conditioning size that closed the rule objection at `0063` §1 and the reason `silent_at_tau1` is a column (`0081`) | reading the equality of the two populations' 652 as a coincidence — **it is structural** |
| **`90`** | the **channel pairs** the widened S&L floor covers (APPLY; **89** on DERIV) | **`step7-liveness-mm-b.md:459` flags a numeric collision with a different 90 in its own last row** — a superseded file, but the collision is real |

### Step 8 rows — **NOT in `src/step7_register.py` as numeric entries.** Added 2026-08-16

| String | LEGITIMATE reading | ILLEGITIMATE reading |
| :--- | :--- | :--- |
| **`168` / `153`** | **D2's `max()` BOTH-BIND tie count, and it is NOT population-invariant.** **168 on APPLY** — invariant across line 1 (220,107), position 4 (201,900), position 5 (196,654) **and** post-liveness (195,951). **153 on DERIV** — 147,370 and 147,271. Verified `artifacts/step8-waterfall-a.json:1311,1320` | **either figure quoted without its population.** `0092` §3's premise *"168 cannot be correct on both"* is **WITHDRAWN** — both arms' differing readings would have given 168, and the agreement was **invariance, not error**. **`153` is ALSO the ALT-MATCHED S&L component at several arms** in `step7-liveness-mm-*` (allowlisted, history), and **a 153.4 d median in `step5-contamination-diagnostics.md`** |
| **`0`** | **DELIBERATELY NOT REGISTERED, and this row exists so the omission is not read as an oversight.** `0` is D9's **strict floor** — *"a zero floor is not an absence of evidence; it is a MEASURED floor on a stated coverage"* (`0090`) — and it is also the two DERIV never-started ratios by degeneracy (`DERIV_NS_RATIOS_ARE_ZERO_BY_DEGENERACY`), the half (a) floor, the half (b) floor, and roughly every third leaf in every JSON. **A row for `0` would flag everything and disarm nothing** | **a `0` arriving as a PASS rather than as a measurement.** The coverage count is what separates D9's `0` from *"looked nowhere"*, and **three of arm a's coverage counts were wrong, mislabelled or unreconciled** at `0087` §2 |
| **`75` / `76`** | **`75` is D9's LOOSE key = the CEILING** of the published bound `[0, 75]` on complementary pairs (`0090`). **`76` is the THIRD key's answer and is NOT AN ENDPOINT** — it strips a trailing digit group of arbitrary length, reducing `the-100` to `the`; reported as a divergence only (`0076`, `0078` §3, `0090`). **`75` is also the U3 universe size.** Third key's half (b) is **28**, against loose **27** | **`76` as the ceiling**; **`75` as "D9's result"** — *neither endpoint may be quoted as D9's result* (`0090`). **`even though strict is ruled` / `the ruled key is strict` are registered superseded NEEDLES** — `0074` r5's framing, superseded by `0090` |
| **`747,478`** | **distinct `(user, show)` PAIRS in arm a's coverage pivot** — any dated pre-`τ_pull` episode record in season ≥ 1, **including S3-only pairs** (`0089` §2(b), correcting `0088` §2). Arm a's undeduplicated **ROW** count is **1,217,122**; arm b's row object over its D11-filtered slice is **1,007,729** | **season-coverage ROWS.** Covered by a **line-local control**, not a needle, because the defect is an **attribution**: `SURFACE6_LINE_LOCAL_CONTROLS["747478_is_a_PAIR_count_not_a_ROW_count"]`. **See the LIVE FINDING below the table** |
| **`726,102` / `726,103`** | **D9 candidate `(user, show)` pairs — a GENUINE ONE-PAIR DIVERGENCE, reported not reconciled.** Arm a `435,642 + 8,834 + 281,626 = 726,102`; arm b `435,643 + 8,834 + 281,626 = 726,103`. **Two classes agree exactly; the S1-only class differs by 1** (`0089` §3). `747,478 − 21,376` S3-only `= 726,102` | **`726,103` as "arm b's user-show coverage rows"** — that was `0086` §1 / `0087` §2's characterisation, superseded. **Treating the one-pair gap as the whole-S3-only gap**, which is how it stayed unrecorded |
| **`46,428` / `46,366`** | **`46,428` = distinct SLUGGED show IDs in the parsed sweep = the U1 universe** ruled at `0088` §3, both arms (`step8-waterfall-b.md:339`, `step8-waterfall-a.md:477`). **`46,366` = the D9 COVERAGE PIVOT's show-ID count**, arm a — a different object, **62 fewer, WITHIN ONE ARM** (`0089` §3, correcting `0087` §2's *"62 apart"* two-arm reading). ***And the PIVOT count itself diverges across arms — 46,366 (a) against 45,014 (b)*** — `0098` §4 residual 4: a denominator moving no result, **resolvable only by reading each arm's mask** | **`46,366` labelled `distinct_show_ids_in_the_sweep`** — arm a published both for one label 27 lines apart, and its *"0 carry no slug"* clause was computed on the wrong base (`0087` §2, fixed `0088` §2) |
| **`1,246` / `1,230`** | **`p = 1.0` TOTALS on APPLY** — position 5 and post-liveness. **DERIV is `1,072` / `1,056`.** Both arms, four cells each (`0085` §3, `0086` §4). **Correct as totals** | **as a SPLIT.** ***Mode I — a withdrawn GROUND built from correct statistics.*** The two `p_at_bound` clauses are **coextensive by construction**, so the **COEXTENSIVITY-GAP** class is empty and these are **one class counted twice, not two summed**. `GROUNDS_WITHDRAWN["0083 SS2"]`. ***AND: never read "the FALSE class is empty" as the COLUMN having no FALSE rows*** — the emitted column's own FALSE is **17,895 / 17,812 / 15,771 / 15,688**, and a schema provisioned two-valued off that sentence is wrong by 17,895 rows |
| **`71` / `59`** | **position-5 rows whose OUTCOME STATE changes under the forbidden `date(ts) ≤ date(τ)` form** — APPLY 71 (52 at `τ1` + 19 at `τ2`), DERIV 59 (45 + 14). **Both arms agree to the row.** A **COUNTERFACTUAL**, at `W = 108` only (`0091` §1) | as a figure that moves the published result. **It does not** — it is what makes the half-open mandate `OUTCOME_DECIDING` rather than vacuous. **`OCCUPIED_INERT` is the WITHDRAWN verdict** (`0089` §2(a), reversed `0091` §1) |
| **`20` / `17`** | APPLY / DERIV rows with `tau2` **exactly at** `τ_pull`. **`tau2 > τ_pull` is 0, but the bound is ATTAINED** — a `>=` form of invariant 9 would fail (`0089` §1, `0091` §3) | reading the `0` as slack. **A passing assertion at the bound and one with slack are not the same evidence** |
| **`311` / `136` / `275` / `117`** | rows holding an S2 episode in the separating interval — `τ1` / `τ2`, APPLY / DERIV (`0091` §1) | as the outcome-change count. **More rows than change state**, because most already have `\|A\| ≥ 1` or already fail Continued. **Arm b's r4 build took its verdict off 1 row of the 311** — that is what `0091` reversed |
| **`89` / `88` / `87` / `90`** | **`89` is the adopted column count and it publishes as 89 ENUMERATED NAMES, never as a count.** `88` survives **only** as the intermediate state inside `0083` §3(a)'s corrected withdrawal note; `87` is one arm's pre-`0080` set; **`90` is the UNION of the two arms' 87-name sets and was never adopted** | **`88 columns` is a registered superseded NEEDLE** (`SUPERSEDED_STRINGS`). **A count is not a set** — `0077`: *"Matching a count is not matching a set — assert on the names"* |
| **`97.6%`** | **NOWHERE as current.** It was the position-3 censoring share (`0033`) | **every hit is a defect** — it is **97.40% on position 4** (`0070` r8). Registered needle |
| **`6,065,704` / `6,065,610`** | **BOTH CURRENT, IN DIFFERENT ARMS.** The set-membership denominator is a **one-parameter family indexed by where D11 applies**: **A** (D11 nowhere) 6,065,704 · **B** (S2 side only) 6,065,610 · **C** (both) 6,065,537. **All three drop 0 and nothing downstream reads it**; all three publish with their pipelines (`0083` §1). ***The arms run different ones and that is `0098` §4 residual 6 — an UNRULED SPEC CHOICE, disclosed by the arm that made it*** | **either figure quoted as *the* denominator**, or the divergence read as an arithmetic defect. **It is a spec gap, not a bug**, and it was ~~*"reported, not reconciled, routed to Step 14"*~~ — **that routing is SUPERSEDED; `0083` §1 closed it as NOT a Step 14 limitation** |
| **`17,895` / `17,812` / `15,771` / `15,688`** | **the `p_at_bound` COLUMN's own `FALSE` count** — APPLY position 5 / post-liveness, DERIV position 5 / post-liveness. **CLASS 2, and it is NOT EMPTY** | **reading *"the FALSE class is empty"* as a statement about the COLUMN.** That sentence is about **CLASS 1, the coextensivity gap**, which is 0 on all four. **A Step 8b schema provisioned two-valued off it is wrong by 17,895 rows** |
| **`439` / `441`** | **`441`** is the needle scan's **candidate-hit count** at `0095` §3, wired **REPORT-ONLY and labelled NOT YET A CONTROL**; **`439`** is the **untriaged** count at `0096` §3 and `0098` §4 residual 8 | **treating either as a defect count.** *"Failing on 441 unread lines would block the gate on lines nobody has read; narrowing until it passes is how a control gets disarmed. Neither was done."* **Whether 441 → 439 is two triaged or two counts of one thing is NOT STATED anywhere I can find — logged as K3** |

**LIVE FINDING, 2026-08-16, not fixed by me and not mine to fix.** `artifacts/step8-waterfall-a.md:434`
carries the exact registered needle **`"747,478 and 726,103 are different objects"`**. The line is
**legitimate** — the table three lines below gives the correct axis (B = distinct user-show PAIRS =
747,478) — **but it contains no `pair`, so the line-local control's `must_contain_one_of` fails, and it
is exempted only because `SURFACE6_MARKERS` matches the word `defect`** in the unrelated closing
sentence *"One name over two quantities is the defect."* **That is the "passing only by accident" shape
`0094` §3 found twice** — a marker firing on an incidental word. **Reported to the Human Lead.**

**ROWS WITHDRAWN OR RESTATED IN THIS PASS:**

- **`703` — the row read *"Correct and current, ALT-BROAD's APPLY exclusion count"* with an empty
  illegitimate column.** That is now **wrong by omission**: a second live reading exists in both arms'
  Step 8 deliverables. **An empty illegitimate column is a blanket exemption**, which is precisely what
  the **superseded** `9.6830` registration was — `9.6830` has been **9.6372** since `0054`.
- **`604` had no row at all** and now needs one for the same reason.
- **`1,355` and `751` were listed ONLY under *"Superseded counts, never to be restated as current"*.**
  **That is now false**: `0085` §5 **mandates** both, in both arms, on both populations, as line 6's
  marginal decomposition. **See the contradiction logged in [[open-items-and-contradictions]] as W1.**

**THE `9.6830` REGISTRATION WAS WITHDRAWN AS A GLOBAL EXEMPTION (`0056`), AND THAT MATTERS.** It was
registered as *"both the superseded bound floor and the legitimate floor of the conditional
sub-interval."* **The second half is false** — the sub-interval's conditioning constrains the **604** and
says nothing about the **90**, so its floor moved with the bound floor to **9.6372%**. **Registering it
as exempt disarmed the grep control against the one string it most needed to catch, on four surfaces, in
the section that created the control.** Its **only** surviving reading is the scoped extreme-NONE one
above.

**THE EXEMPTION SCOPING WAS ITSELF BROKEN, AND ONLY THE FIX MAKES THESE ROWS TRUE (`0060` B6).**
`EXTREME_NONE_READINGS` guarded four values on a line matching `extreme[_ ]NONE` — but **the general
`DECLARE` branch three lines above already contained `extreme[_ ]NONE`, so the value-scoped branch could
never change an outcome.** *"The register documented it as a CONTEXT exemption, not a value exemption;
the code did neither."* The phrase was disarming the control against the SUPERSEDED values `0.0503`, `0.4033`, `0.4703` and the
scoped `0.5090` / `0.0690` — **values the two-extremes table has nothing to do with** — and the same held
for `un-?widened`, `_scope`, `share_of_population`, `proposed_pct`. **The general branch is deleted;
`DECLARE_SCOPED` is keyed by FILE and by VALUE.** JSON **path** markers are separated into
`DECLARE_JSON_PATH` and applied to paths only, **because a path is structure and a line is a claim.**

**MATCH NUMERICALLY, NOT TEXTUALLY (`0058`).** These rows are written at 4 dp and the JSON deliverables
store 6-dp literals, so `9.6830` is **not** a substring of `9.682997`. **`src/check_surfaces.py` parses
every number-shaped token on all **EIGHT** surfaces and compares at a tolerance** — the only form of this
check that can see the `.json` halves. **Six superseded values survived Red Team review 11 there
precisely because their registered form rounds UP.**

**A LINE CARRYING BOTH A SUPERSEDED VALUE AND ITS SUCCESSOR IS SELF-DECLARING** — it is narrating the
transition, which is what a record is for (`SUCCESSOR`). **The rule runs on the EMITTING LINE, not a
±2-line window** (`0060` B7): the adopted 6-dp width `0.403246` is within tolerance of `0.4032` and
appears in every bound table, so a window let the superseded `0.4033` self-declare from two lines away. *"A successor two
lines away is a coincidence; on the same line it is a sentence."*

**KNOWN LIMIT, recorded not closed (`0060` §6, amended `0061`):** both controls walk **numeric leaves
only**, so a superseded **number** inside a JSON **string** is invisible to `json_numbers()` and
`verify()`. Recorded as *"not a defect today"* — and it **was already a defect on the day it was
recorded**. Partially closed: `WITHDRAWN_PHRASES` is now checked against `.md` text **and** JSON string
values. **Recording a gap as harmless is not the same as checking whether it is.**

### WITHDRAWN PHRASES — prose, not numbers. `src/step7_register.py`, added `0061`

**A numeric control cannot see a withdrawn claim, and this chain withdraws claims as often as it corrects
figures.** Each is a fragment; every occurrence outside a strikethrough or withdrawal note is a defect.

| Phrase key | What it claimed |
| :--- | :--- |
| *"which is the proof"* | the `0.2813` / `0.27211` divergence proved the S&L reconciliation wrong. **False** — one convention on two bootstraps. Withdrawn `0060` §2 |
| *"retained in place above and marked superseded"* | a hard-coded literal nothing checked and that was false. Withdrawn from the JSON half at `0059` and **still emitted into the `.md` half** |
| *"everything else in this file stands"* | a stamp that **affirmatively certified superseded figures**. Withdrawn `0056` §4 |
| *"cannot enter the list"* | the `LIVE_ELSEWHERE` mechanism, **which never fired**. Withdrawn `0059` |
| *"unreconciled and now specified"* | `0052` §6 on the bootstrap spec. **It was never specified in any file.** Struck `0056` §8 |

**B8 is why this half exists.** A withdrawn sentence was struck **in the three places a human had typed
it and left in the one place a SCRIPT types it**, so the generator wrote it back to all four operative
files on every run. **Both controls were structurally blind:** the `.md` form carries **no numbers**, and
the `.json` form is a **string under `_DERIVED`**, which `verify()` skips by key. `bb-a.md` therefore
contradicted itself inside one file — line 77, inside the block headed *"GENERATED, do not hand-edit"*,
**asserted** it; line 316, in hand prose 240 lines lower, **struck** it.

**Carried defect (`0063` §3 item S6, the one the Human Lead named as first to fix): THE REGENERATOR NEVER
RUNS THE PHRASE HALF** — *"the thing that wrote B8 into four files still does not check for withdrawn
phrases after writing."*

### The EIGHT propagation surfaces — `CLAUDE.md` §Propagation

> **CORRECTED 2026-08-16: this section said SEVEN. `CLAUDE.md` has said EIGHT since `0074` §…, which
> added `processed/` as surface 8** — *"the first file an implementation reaches for"*, after
> `adopted_rule.json` carried revision-3 figures against the approved revision-6 rule and a Step 8
> instance had to work around it. **My own file was one surface short of the control it describes.**
>
> **AND THE NUMBERING WAS INVERTED IN THREE DECISION ENTRIES** — `0083` §4, `0085` §8 and `0086`
> §2/§3/§6 all called the `analytics-engineer` pair *surfaces 2–3*. `CLAUDE.md` numbers **2–3 the
> `data-scientist` pair, 4–5 the `analytics-engineer` pair.** **The FILES edited were always right; the
> NUMBERS naming them pointed a re-verifier at the two files that were not touched.** Corrected in
> place in all three by `0087` §1. **`decisions/` is NOT one of the eight surfaces** (`0087` §8), and
> **`specs/` is not either — Red Team's F5, carried for the Human Lead at `0089` §4 item 2**, after it
> carried *"Step 8 has not launched"* through four occurrences with nothing checking it.
>
> ***`CLAUDE.md` IS NOT A SURFACE EITHER, AND THAT HAS NOW COST SOMETHING*** (`0095` §4). The citation
> resolver **scans the eight propagation surfaces**, so when `0095` was cited before it existed —
> **the THIRD missing-entry occurrence, in 10 files** — **the citation that would have caught it
> earliest was in the one file the control does not read.** It was caught one build later **only
> because `artifacts/` IS surface 6** and arm a's build provenance names the entry. **Whether `specs/`
> and `CLAUDE.md` join the surfaces is carried, unruled, for the Human Lead** (`0095` §4, `0096` §3).

**A ruling lands in `decisions/` AND in every file an agent reads. Recorded only in `decisions/` is not
recorded.** All eight are checked on every edit:

| # | Surface | Note |
| :--- | :--- | :--- |
| 1 | `task-sheet.md` | |
| 2–3 | `.claude/agents/data-scientist.md`, `data-scientist-b.md` | Byte-identical by design |
| 4–5 | `.claude/agents/analytics-engineer.md`, `analytics-engineer-b.md` | The files Step 8 launches from |
| **6** | **`artifacts/`** | Deliverables carrying superseded figures are **stamped**, not left to read as current. **Never checked before 2026-08-13.** *Carried defect: still suffix-filtered while 7 was fixed (`0063` §3, S-items)* |
| **7** | **`.claude/agent-memory/second-brain/`** — **THE DIRECTORY, NOT ONE FILE IN IT** (`0057` §6) | **This memory. It is fed back into rulings, and stale memory here has already caused a wrong one** (`0052` §2). **Never checked before 2026-08-13**, and it is what Red Team's **eighth** Step 7 review found |
| **8** | **`processed/`** (`0074`) | **The first file an implementation reaches for.** `adopted_rule.json` carried revision-3 figures against the approved revision-6 rule while no control covered it. **Data tables are data; the FIGURES live in the metadata files**, and large tables are skipped by size and **listed, never silently.** `PROCESSED_NEVER_EXEMPT = ("adopted_rule.json",)` — in code, not by remembering |

**Surface 7 is the DIRECTORY.** `0056` propagated to *"`second-brain`'s glossary"* and reported it as a
surface. **The glossary was corrected; `open-items-and-contradictions.md` was not**, and it carried the
corrected bound and its withdrawn sub-interval **one line apart, both blessed with a check mark** — that
is **propagation failure #21**. *"A propagation was scoped to a file and reported as a surface."*
`0062` further found `SURFACES["7 second-brain"]` **globbed `*.md` only, so a `.json` in this directory
was outside the control entirely**; it now globs every file.

**TWENTY-TWO numbered propagation failures — `#22` is `0084`**, the `p_at_bound` bullet `0083` §2
reached 71 lines below and not at the bullet itself, **invisible to the phrase control because the
withdrawn sentence wrapped across a line break**, found by instance A on a rerun and not by a control.
**`#1`–`#18` are a SURFACES-1–5 COUNT and MUST NEVER BE
PUBLISHED AS A TOTAL** (`0057` §7). They were found on surfaces 1–5 because those were the only surfaces
checked; **6 and 7 were added after the count was fixed**, and their failure rate was recorded as
*"unmeasured, not zero."* **It is now measured and non-zero at three:**

| # | Where | What |
| :-- | :--- | :--- |
| **19** | surface 6 | the stamp that **certified superseded figures** — found **inside the fix added for surface 6** |
| **20** | surface 6 | **both `.json` halves left behind** while the `.md` halves were corrected |
| **21** | surface 7 | `open-items-and-contradictions.md`'s **blessed sub-interval** |

**The count is not renumbered — 18 is a true count of surfaces 1–5 — but it reads as a total without the
Step 14 bullet, and whether to restate it against EIGHT surfaces is the Human Lead's call — still
open, and it has now been open across two gates.**

**Read-back PLUS grep. Read-back alone is not verification.** Reading an edit back proves the new text
landed; **only grep proves the old text is gone**, and a file can hold both at once — three consecutive
propagation failures were exactly that, an adopted figure and its superseded predecessor in the same
file, sometimes ten lines apart, each declaring the other wrong.

**AND THE NEGATIVE GREP IS NOT SUFFICIENT ALONE (`0055` §3).** **A figure that was never written returns
zero hits on every superseded form of itself** — the DERIV bound existed on **no** surface, so a mandated
negative grep reported a clean pass on a file set containing the defect. **So: grep the CORRECTED string
too and require NON-ZERO.** A defect has two shapes — the wrong figure present and the right figure
missing — and the negative half sees only the first.

**A GREP HIT IS NOT A DEFECT UNTIL THE LINE IS READ.** Run the trap table above first.

### The machinery, and why hand-patching was abandoned

**Four consecutive decisions corrected these artifacts by hand-patching individual values, and every
finding in reviews 9, 10 and 11 was a value a patch reached in one file and missed in another** — or
reached in the `.md` and missed in the `.json`, or **reached a ratio and missed its numerator**.
*"Eleven entries of one error class is a method that cannot converge"* (`0058` §1).

| File | What it is |
| :--- | :--- |
| **`src/step7_register.py`** | **THE single register** (`0059` B3). Four entry kinds — `SUPERSEDED` (wrong everywhere) · `SUPERSEDED_IN` (wrong in one file, right in another) · `ADOPTED` / `ADOPTED_IN` · `LEGITIMATE` (looks superseded, is not; **registering one DISARMS the control against it**, so each carries its reason). Plus `WITHDRAWN_PHRASES`, `WHOLLY_SUPERSEDED_FILES`, `DECLARE_SCOPED` |
| **`src/step7_regenerate_derived.py`** | Writes **every** derived figure into **both halves of both arms from ONE EXPRESSION EACH**. 84 target paths, 30 ratio rows |
| **`src/check_surfaces.py`** | Replaces textual grep — **numeric matching at both precisions** across all **EIGHT** surfaces, **plus a withdrawn-phrase half**, a positive half, and (since `0094` §4) a **citation resolver** that fails on any cited decision entry with no file and fails if it finds zero citations. ***THREE FIXES AT `0095`:*** the resolver **saw only BACKTICKED citations** — arm b writes predominantly un-backticked, so **~37% of one file's citations were invisible and the founding defect would have been missed entirely in that form**; it is now anchored to citation **FORMS** (`decisions/0NNN`, `` `0NNN` ``, and `0NNN` followed by `§`/`SS`/`Sec`/`ruling`) after a bare `\b0\d{3}\b` matched data. **The NEEDLE register was exercised on 4 files of ONE surface** (~4 of ~40 on surface 6, none of 1–5, 7 or 8) and is now run repo-wide — **255 files, 7.0M characters**. **The exemption window was measured in LINES** on files where 137 lines exceed 400 characters — now in **characters**; *the `.md` branch was not wrong when written, **the unit changed underneath it*** when the arms began emitting paragraph-per-line |
| **`src/step7_register.py`** — the two read-backs | **`artifacts/step8-readback-{a,b}.md` are stamped AND allowlisted BY NAME with a reason** (`0097`). **Both mechanisms, because a stamp declares a file's STATUS and does not exempt it** — the rule that once exempted 19 `.md` and 16 `.json` files. **These are historical read-backs with NO PRODUCING PIPELINE, so `0092` cannot correct them by rerunning an arm.** Four statements in them expired: *"`processed/` is not one of the SEVEN surfaces"* (it is **surface 8 of EIGHT**), `adopted_rule.json`'s revision-3 figures, *"Step 7 NOT approved; seven HOLDs"* (**approved `0064`**), and *"Step 0 still carries the superseded 403 rule"*. ***No control can see any of them*** — the third blindness class; **eleven Red Team passes did not catch them**, and the eleventh found them only because `0096` §1 drew a line these files sit outside |
| **`src/step7_floor_extremes.py`** | The two-extremes / channel verification. **11/11 CONFIRMED, 0 REFUTED**. Its surviving `assert at_tau2 == 0` is now **a compared row with a verdict**, not an assertion |

**THE WHOLE-FILE EXEMPTION IS DELETED (`0059` B2).** The old rule — any file with `SUPERSEDED` in its
first 45 lines is exempt in whole — **exempted 19 `.md` and 16 `.json` files, the entire Step 7 artifact
set including both OPERATIVE deliverables**, and it is why a wrong ratio survived a passing check. A file
is exempt **only by name, in the source, with a reason**, and **`step7-liveness-bb-{a,b}` are NOT
exemptible** — they are only *partially* superseded. **A stamp 300 lines above a value is not the point
of use.**

> ### **A CHECK THAT FINDS NOTHING BECAUSE IT LOOKED NOWHERE MUST FAIL (`0062`).**
>
> `check_ratios_written()` skipped **arm b in full** and reported OK: it read `sampling_error`, arm b
> stores its bootstrap under `bootstrap`, and `ABSENT_OK["b"]` allowlisted the absence — so it **checked
> zero rows and returned an empty failure list, which reads identically to "everything is right."**
> `0060` §1's coverage claim was **true for one arm of two**.
>
> **The pattern in one sentence: an empty result and a clean result are the same value, and only the
> control knows which it produced.** Four more of the same shape were found and closed —
> `except Exception: return []` on file reads (a file that fails to parse contributes zero numbers and
> the scan passes); the input cross-check's `if u:`; an `ABSENT_OK` entry that never fires; and surface
> 7's `*.md`-only glob. **Every place that can return "nothing found" now says whether it found nothing
> OR looked at nothing.** Coverage is printed every run.
>
> **This was the third control in six entries that reported clean while looking at nothing.**

**ONE DEFINITION PER STATEMENT AND PER FIGURE (`0062` §3).** `STATEMENTS` holds 8 sentences,
`figure_table()` holds 72 figures; **both writers render those two objects and neither contains prose of
its own about the figures.** `compare_halves()` reads both rendered halves **off disk** and compares key
by key, **failing on comparing zero figures.** *Carried defect (`0063` §3 item 2.1): `compare_halves()`
CANNOT FAIL as built* — both sides are `figure_table(arm)` serialized twice in one process from the same
`D`, and it does not compare the `.md` a reader sees.

**THE DEPENDENCY LISTS CLOSE TRANSITIVELY, TO FIXPOINT (`0057` §3).** When an endpoint moves, check its
list **and the list of every figure on that list**. `0056`'s lists were **one hop deep and the gap had
already bitten**: `1,307 / 100.6646%` left live in both `data-scientist` files was **failure #16, "the
severe one," two hops from the floor.** *"The list written to prevent #16's class did not reach #16."*

**The dual diff cannot catch a propagation failure.** Both members of a pair are byte-identical by
design, so an error written into both is invisible to it. *(This paragraph appeared twice in this file
until 2026-08-16 — one definition per statement, including here.)*

### Withdrawn claims that must not reappear as operative

*"no free parameter"* (`0044`) · *"`τ2` plays no part"* (`0049`) · *"the exclusion set is empty on
DERIV"* (`0049`, false in five files) · *"every liveness exclusion is never-started"* (`0050`) ·
*"751 directly observed"* (`0048` — **652 observed, 99 null-based**) · *"the 604 are exactly the
pairs with no S2 record anywhere"* (`0047` — **subset, not equality**: APPLY holds 23,260 such pairs
and 22,656 stay live) · *"the DERIV zero is forced by construction"* (`0047` — a **fact of the filter
order and this pull date**, not a theorem) · *"one ordinary gap in a hundred"* (`0037` — length bias)
· the **invariance** of the gap-test/edge-case split (`0039` — arithmetically impossible) ·
*"73.6537% is on no population"* (`0051` §2 — **it is the Continued ceiling on 196,654**, withdrawn by
`0052` §2) · *"the silence test is anchored at `τ1` and only at `τ1`" being false* (`0053` §3 item 1 —
**withdrawn with `0053`; the clause is true and restored**) · **`0053`'s amended reading of `0021`**
(*"an insertion after the window FOR THE QUESTION BEING ASKED"* — reverted by `0054`) ·
*"the pair could not have produced the evidence the Continued test reads"* (`0053` — **false**: a
record inserted at `s` can carry any `watched_at ≤ s` and `0021` Adoption 3 keeps post-dated records).

**Decomposition, ALT-BROAD:** APPLY **196,654 → 52,514 (¬Continued) → 703**. *(ALT's
196,654 → 33,373 → 604 is superseded and must not be implemented.)* **Conjunct 1 does most of the
work**, which is why the count moves with `W` at all.

**APPLY at position 5, the decomposition every bound is computed on:** never-started **33,373** +
Continued **144,140** + started-and-left **19,141** = **196,654** ✓. **Corrected 2026-08-13** — this
file previously carried **144,141 / 19,140**, two off-by-ones that cancelled in the sum and so passed
the arithmetic check. The correct split is forced by three independent figures that all reconcile only
on 144,140 / 19,141: the Continued ceiling `(144,140 + 703)/196,654 = 73.6537%` *(SUPERSEDED — the
  adopted ceiling is 73.6995%; the reconciliation turns on the split, not the widening)* (`0052` §2), the S&L
ceiling `19,141 + 604 = 19,745 → 10.0405%`, and `0053` §3 item 8's branch (ii) count of **19,141**.

## Decision numbering on the public record — `decisions/`

`0001` Step 1 gate · `0002` Step 4 endpoint (D15) · `0003` W estimation sample (D14) · `0004` 403
handling · `0005` Step 3 stopping rule · `0006` Step 3 crawl constants · `0007` Step 3 channel cost
· `0008` Step 3 seed source · `0009` Step 4 pull order · `0010` Step 4 tail cap · `0011` `pull_date`
· `0012` sweep completeness · `0013` Step 2 delegation · `0014` no content filters · `0015` unaired
S2 · `0016` per-season network dropped · `0017` air period · `0018` size quintile base · `0019`
`pool_completers` recomputed · `0020` structural thresholds · **`0021` Step 5 gate APPROVED** ·
**`0022` the two Step 5 rulings written into `task-sheet.md`** · **`0023` `0012` upheld after a Red
Team HOLD** · **`0024` `W` is the 90th percentile** · **`0025` lag unit and ceiling** · **`0026`
Step 6 gate APPROVED, `W = 108`** · **`0027` Step 13 arms at 150 and 213** · **`0028` Step 14
carries every routed limitation** · **`0029` `W` propagated, Step 7 threshold rule, Step 8 filter
order** · **`0030` 2025 cutoff kept + three frame field changes** · **`0031` the ≥50 floor
justified** · **`0032` Step 4 deliverables regenerated** · **`0033` Step 8 per-air-period censoring
counts** · **`0034` Step 1 §7 amended — Continued at `τ2`** · **`0035` agent definitions are live
spec, amended; Step 10 receives `0034`** · **`0036` Step 7 threshold at the 99th + the bracketing-gap
shape** · **`0037` `0036` §1's basis withdrawn; gap unit; namespaces** · **`0038` Step 7 spec frozen
— reference 152,126, one gap per pair** · **`0039` Step 7 APPROVED at 632 d — LATER SUSPENDED** ·
**`0040` gate REOPENED on Red Team HOLD; `0021` reinstated; the 18,250 returned** · **`0041`
extended reference set, provisional; no threshold approved** · **`0042` Step 7 APPROVED, threshold
DELETED, PF-LIMIT** · **`0043` bias-2 sign corrected DOWN→UP** · **`0044` "no free parameter"
withdrawn; fully determined by `W`** · **`0045` Option C bound; ALT rejected — rejection later
withdrawn** · **`0046` ALT ADOPTED; `0045`'s rejection withdrawn; the population rule** · **`0047`
`0046` §1/§4/§7 corrected; D10 re-derived per arm; `>=`** · **`0048` ALT-BROAD ADOPTED** · **`0049`
joint S&L bound; six record defects; calibration residual discharged** · **`0050` six file defects
fixed and verified; limits routed to Step 14; channel measured at 297 pairs** · **`0051` V1–V7 and
housekeeping — its §2 "V7 correction" was WRONG and is withdrawn by `0052`** · **`0052` ALT-MATCHED
ADOPTED; `0051` §2 withdrawn; channel corrected to 52.4%** · **`0053` `0021` amended for two windows —
WITHDRAWN IN ITS ENTIRETY by `0054`** · **`0054` ALT-BROAD RESTORED, the S&L floor widened, `0053`
withdrawn, `0021`'s amendment reverted, `0048` §9 restored** · **`0055` the DERIV floor widened, the
margin argument withdrawn, the grep control and the seventh surface** · **`0056` the four derived
figures corrected, `9.6830` de-registered, the dependency list** · **`0057` the JSON halves, transitive
lists, the channel window fixed OPEN, surface 7 is the DIRECTORY** · **`0058` regeneration replaces
hand-patching; the two ratio conventions REPORTED not reconciled; the dates corrected** · **`0059` one
register; the whole-file exemption deleted; the quotient is a target path** · **`0060` arm a runs one
convention (`0.2818`); the exemptions scoped per file and per value** · **`0061` withdrawn claims are
emitted by the generator; the register holds PHRASES** · **`0062` a check that looks nowhere must FAIL;
one definition per statement; the covering qualifier propagated to eight surfaces** · **`0063` widths
from counts; the rule objection closed on measurement (652); the residual logged** · **`0064` STEP 7
GATE APPROVED — ALT-BROAD, UNCONDITIONAL, residual published**.

**The Step 8 block:** `0065` dates corrected + the third blindness class · `0066` Step 8b schema
propagated · `0067` `0064` propagated · **`0068` waterfall line 1 = 220,107** · `0069` seven spec gaps
· **`0070` eight Step 8 rulings** · `0071` `data-scientist` pass · `0072` rule scope in all three
places — **Step 8 LAUNCHES** · `0073` comparator · **`0074` six rulings + the EIGHTH surface** ·
`0075` D3′/D9 side-output/the `W` grid · **`0076` `p` is a CODE check** · `0077` population labels,
drop set, column names · `0078` provenance + two withdrawn rulings · `0079` deliverable provenance,
units, inert positions · **`0080` columns ENUMERATED + invariant coverage** · **`0081`
`silent_at_tau1` restored** · **`0082` `p_at_bound` + generated files as checks** · `0083` denominator
closed, `p_at_bound` restated · `0084` propagation **#22** + wrapped-phrase blindness · `0085` Red
Team B1/B2/P4 + two unsourced items · `0086` D9 universe located · `0087` surface numbering INVERTED ·
**`0088` three rulings — B3 measured, F2 two objects, D9 universe = U1** · `0089` B3 caught a real bug
· **`0090` D9 PUBLISHES AS A BOUND** · **`0091` half-open is OUTCOME-DECIDING** · **`0092` artifact
sign-off** · **`0093` a ruling is not closed until the artifacts carry it** · **`0094` citation
resolver** · **`0095` cross-arm relay forbidden in a launch instruction** · **`0096` deliverable scope
+ the `decisions/` route** · `0097` read-backs stamped and allowlisted · ***`0098` STEP 8 GATE
APPROVED — gate 5 of 5, ALL FIVE CLOSED***.

### `0064` — the approval, and what it turned on

**APPROVED by the Human Lead in writing, 2026-08-13. Record: `artifacts/step7-gate-approval.md`.
Gate 4 of 5 closed.** ~~Step 8 may launch and is the remaining gate.~~ ***SUPERSEDED: Step 8 was
APPROVED at `0098`, 2026-08-17. Gate 5 of 5, and all five are closed.***

**Red Team reviewed fifteen times and returned HOLD fifteen times.** The division that carried the
approval:

- **Reviews 1–8 contested the RULE** and changed what is measured: the bias-2 sign correction, the
  withdrawal of *"no free parameter"*, the derivation and **deletion** of the numeric threshold, four
  rule generations, the widened floor, the `τ1` anchoring.
- **Reviews 9–15 found PROPAGATION AND CONTROL defects in figures derived from an UNCHANGED rule. Not
  one changed the rule, the population, the exclusion counts, or any bound endpoint on its own
  arithmetic.** They changed **where numbers were written, which numbers were checked, and whether a
  claim about a check was true.** *"Seven entries were needed for the machinery to catch up with an
  analysis that had already stopped moving."*

**From review 5 the rule statement was not contested. From review 8 Red Team explicitly cleared the `τ1`
anchoring, the ALT-MATCHED revert, `0021`'s restoration and `0048` §9. In reviews 12, 13 and 15 it
independently RECOMPUTED the arithmetic** — both partitions, all four widths, both attainable corners to
exactly 100%, the excess identity, all six sampling ratios — **and confirmed it each time.**

**The last substantive challenge, review 15's, closed ON MEASUREMENT** (`0063` §1). Its premise —
*"not one of the four rules drops conjunct 2"* — **is false: PF-LIMIT IS the no-conjunct-2 rule**, and
`0045` §1's table has given its DERIV split as `751 = 0 NS + 652 Continued + 99 S&L` since `0045`.
**The 652 Red Team asked for was already printed in the record.**

| | n | ALT-BROAD | **cont ∧ silent** | no conjunct 2 | growth |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **652** | **1,355** | 1.93× |
| **DERIV** | 147,370 | 99 | **652** | **751** | 7.59× |

**Dropping conjunct 2 excludes 652 Continued pairs on evidence they demonstrably produced.** Liveness
exists to stop a null being trusted; **Continued is not a null**, and excluding a pair whose positive
evidence is in hand is the one thing the rule cannot coherently do. **What survives is the size of the
outcome-conditioning: 652 on BOTH populations** — 0.3315% of APPLY, 0.4424% of DERIV — **measured rather
than argued**, publishing as a Step 14 limitation.

**Two amendments the Human Lead made to the drafted approval:**

1. **The bootstrap placement is RED TEAM'S RECOMMENDATION, not a ruling.** *"Blocking Step 9, not Step
   8"* came from review 12 and the draft carried it as settled. **The Human Lead has not ruled on where
   the unspecified bootstrap blocks**, and approving the gate does not rule on it.
2. **The approval is UNCONDITIONAL, and the framing is the Human Lead's own** — they **confirmed**
   *"given with these open and published, not around them"* **rather than accepting it as the drafter's**.

**Open and flagged, not fixed:** the approval is dated **2026-08-13** as the Human Lead gave it, while
`0060`–`0063` — **including `0063`, which carries the 652 the approval's §3 rests on** — are dated
**2026-08-13**. The approval record flags this to the Human Lead for confirmation or correction and
**does not fix it without a ruling**, `0058` §6 having corrected a date drift in the other direction.

### The residual — PUBLISHED, not resolved. Nine items, `artifacts/step7-gate-approval.md` §4

**The approval is unconditional. None of this is a condition on the gate and none of it gates Step 8.**
**Confirmed by the Human Lead in those terms:** the residual **publishes with the result.**

**Limitations of the rule (Step 14):** **1.** the **biconditional gap** — `0021` licenses *insertion
after `τ1` ⟹ live*, sufficiency only; ALT-BROAD **narrows** where the converse is asserted from
PF-LIMIT's 1,355 to 703 and **does not justify it**. **2.** liveness is **outcome-conditional** through
conjunct 2; `ordering_commutation_check` shows the two filter orders agree on **observed counts, not that
the estimand is unchanged** — **size 652**. **3.** the **calibration residual**, discharged at `W = 108`
only, while Step 13 runs to 213. **4.** the **population mismatch** — bounds on position-5, shares
post-liveness, and **on DERIV the point estimate lies outside its own bound**. **5.** **297 pairs remain
in the channel** the warrant describes — 207 never-started, whose null `0021` licenses, and 90
started-and-left, whom the widened floor now admits.

**Blocking Step 9, not Step 8 — RED TEAM'S RECOMMENDATION, NOT a Human Lead ruling:** **6.** the
**bootstrap is unspecified**; the two arms diverged on `B`, seed **and** statistic; `0052` §6's *"now
specified"* is struck; **Step 9's CIs are not diffable until all three are fixed.**

**Control defects, carried (`0063` §3):** **7.** `compare_halves()` cannot fail; **four sub-interval
ratios are outside every control** and arm a's is checked by nothing; the `_DERIVED` block is
**write-only**; the covering qualifier exists in **five wordings** and the `analytics-engineer` pair
carries **one clause**; `LEGITIMATE` disarms nothing while two registers say it does; seven smaller items
including **the regenerator never running the phrase half**; and DF-3's closed-form window
`(τ1, τ2]` still in `specs/step7-deriv-floor-verification.md`'s Background, **a completed task's brief**,
where inertness is **not** expected at `W = 213` — which is Step 13's grid.

**Reported, not reconciled — `CLAUDE.md`:** **8.** robustness survival **792 (A) against 791 (B)**, off
by exactly one on each population, consistent with a `≤ τ_pull` restriction **A states and B does not**;
**neither arm flagged it.** **9.** **the two sampling-width conventions. The spec fixes neither.**

**Verification standing at the time of drafting:** `check_surfaces.py` **PASS** (negative, phrase and
positive halves, seven surfaces) · `step7_regenerate_derived.py` **PASS** (84 target paths, 30 ratio
rows, both halves compared) · `step7_floor_extremes.py` **11/11 CONFIRMED, 0 REFUTED** · both dual pairs
**byte-identical apart from `name:`** · **zero API calls in the entire `0055`–`0064` chain.**

**`0053` is the only entry in the log withdrawn in its entirety.** Its **nine defect fixes are
retained** where they are rule-independent; their ALT-MATCHED figures are superseded.

**Authority split.** `0001–0004` and `0009–0050` are Human Lead. **`0005–0008` are agent-taken and
still Open, awaiting ratification.** **`0029` and `0041` are the only non-Closed entries** — `0029`
was Open on the Step 7 percentile (**now moot: the percentile was ruled at `0036` and the whole
threshold deleted at `0042`**, so `0029`'s open clause has been overtaken rather than closed);
`0041` is Open by its own status line.

**Two index defects in `decisions/README.md` as of 2026-08-13:** it carries **no row for `0050`**,
and its authority note still reads **"0001–0004 and 0013–0033."** See
[[open-items-and-contradictions]].

## Step 6 — how `W` is derived, and the conventions inside it

| Term | Value / rule | Where |
| :--- | :--- | :--- |
| **The percentile** | **90th.** *"Attribution-window practice sets the window at or slightly above the 90th percentile of the time-to-conversion distribution, with 75th to 90th the cited range."* **Imported convention, not selected by the data**, and labelled as such wherever it appears. Moving to the 85th buys **61.7 days** (46 vs 107.7) | `0024` |
| **The withdrawn wording** | ~~"set W at the percentile where the curve flattens"~~ — **withdrawn.** The C1 density is close to scale-free past day 7 (log-log slope −1.1 to −1.5 across every decade), so the spec asked for a feature the distribution does not have | `0024` |
| **The lag** | **Continuous instant difference**, signed and untruncated. Not floored to whole days | `0025` |
| **The rendering** | **`W` is the CEILING of the percentile.** A pair is covered iff its fractional lag is `< W`, so flooring is a **systematic one-directional off-by-one against the operator**. 107 covers 89.976%, 108 covers 90.020% | `0025` |
| **Applies wherever the shape recurs** | Any later step reading a percentile off a lag or duration and feeding it into a half-open instant test inherits the same off-by-one. **`0025` names Step 7's liveness threshold as the immediate candidate** | `0025` |
| **C1 estimation subset** | **25,120 pairs = C1 ∩ 128,099**, 19.6% of the sample, from **206 shows and 2,050 users** | `0026` |
| **`W`'s precision** | **±18 days at 95%, show-clustered.** iid ±8 is wrong — 206 shows is the binding cluster, and treating pairs as independent overstates precision ~2.5× | `0026` |
| **All-shows p90** | **37.6967 → 38** under the ceiling rule. **Descriptive only; `W` is never read here.** The 70.0-day gap between the two curves is the measured size of D14's transfer assumption | `0026` |
| **Step 13 `W` arms** | Union of the two-curve range **[38, 108]**, the run-1 span **[46, 107]**, and the new arms at **150 and 213** — effectively **38 to 213**, with 108 inside rather than at the ceiling. **`H` constant across every arm; each arm re-censors, so the arms do NOT share a denominator** and the retained-row count is required per arm | `0027`, composing with `0024` |
| **`213`** | The C1 p90 among pairs with **≥8 years of exposure** (n = 4,141). **An upper bound, not a rival estimate** — exposure and cohort are not separable | `0026`, `0027` |

## Clock, window, horizon — TWO boundaries since `0034`

| Symbol | Definition | Where | Status |
| :--- | :--- | :--- | :--- |
| `T0` | `max(S2_finale_air_date, first-pass S1_completion_date)`. **Carries a behavioural term:** the `S1_completion_date` arm binds on **116,041 of 220,107 pairs — 52.7%** (`processed/step5/t0_binding.json`). Any claim that `T0` is exogenous is false and was withdrawn twice | Step 1 §6, D1; binding counts via `0034` | FIXED |
| `⟦T0⟧` | The **UTC midnight of the date** of `T0`. `τ0 = ⟦T0⟧` | §2.4, D13 | FIXED |
| **`τ1`** | **`⟦T0⟧ + W × 24h` = `⟦T0⟧ + 108 days`.** Assigns **never started** (`\|A\| = 0`); is the **liveness SILENCE anchor** and the **only** instant the silence test reads | §2.4, D13; value `0026`; anchor role `0034` | **FIXED** |
| **`τ2`** | **`⟦T0⟧ + (W + H) × 24h` = `⟦T0⟧ + 199 days`** at `W = 108`, `H = 91`. Assigns **Continued**. Moves with `W` automatically — at the `W = 213` arm, `τ2 = ⟦T0⟧ + 304 days`, exactly the clearance `0027` already priced. **Since `0048` it is also read by the liveness rule's second conjunct** | Step 1 §7 as amended; `0034`; liveness role `0048`, `0049` | **FIXED** |
| **The liveness rule reads TWO instants** | **Silence at `τ1`, Continued at `τ2`.** *"`τ2` plays no part"* is **WITHDRAWN** (`0049` defect 1) — it was true of PF-LIMIT and is false of ALT-BROAD, whose second conjunct **is** the Continued test. **What survives, and is what the withdrawn line meant: the SILENCE test is anchored at `τ1` and only there.** Since `τ2 > τ1`, ALT-BROAD at `τ1` is **strictly narrower** than a `τ2`-matched form — the conservative version, introducing no new anchor | `0048` §3(b), `0049` | **FIXED** |
| **`A`** | Distinct S2 episodes with `number ∈ E2` and `watched_at < τ1`, over `(−∞, τ1)` — **one-sided, no lower bound** | Step 1 §7 | FIXED |
| **`A_H`** | **`A` recomputed with the bound moved from `τ1` to `τ2`** — the set **D3 already defined**, which is why the amendment introduces no new object. **`A ⊆ A_H` by construction** since `τ1 < τ2`, so the amendment is **monotone**: pairs move Started-and-left → Continued only, never back. Asserted at Step 8 **as a code check, not a data check** — being true by construction it can only catch an implementation that computed the two sets wrongly, and a green assertion is not evidence for the rule | D3's original text; promoted to the operator by `0034` | **FIXED** |
| In-window test | **`watched_at < τ1`** (and `< τ2` for `A_H`). Strict, half-open, instants only, on both boundaries | §2.4, D13 | FIXED |
| `H` | **91 days**, fixed, **not a function of `W`**, held constant across every Step 13 arm. Adopted **by name** at the Step 1 approval (D10) — which is why `τ2` introduces **no new constant**. **`H` loses the comparison it is measured against by 10 days:** the marginal p90 (first S2 episode → completion) is **100.39**, i.e. **101 under `0025`'s ceiling, against 91**. The shortfall is not argued away — it is exactly what item 9's 3,440 residual counts | §6, D10; marginal p90 from `src/step6_completion_lag.py` | FIXED |
| Right-censoring | retain iff **`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`**. **This is exactly `τ2` at `W = 108`**, so every retained pair already has `A_H` fully observed and the amendment's censoring cost is **zero**. Holds at **every** arm, because `W + H ≤ max(W, 91) + H` is an identity | §6, D10; identity in `0034` §3 | FIXED in form |
| **`m_H`** | **`max(A_H)`.** Step 10's abandonment point is the **rank form** `p = \|{ e ∈ E2 : e ≤ m_H }\| / L2`, `m` replaced by `m_H` and nothing else changed. **`p = m_H / L2` is NOT the rule** — the raw-ratio form stays withdrawn (`L2` is a count, `m` an episode number; with an `E2` gap it can exceed 1). `p` is defined **only on Started-and-left**, which is now assigned on `A_H` | Step 1 §Abandonment point as amended; `0034` | **FIXED** |
| **D8(ii)** | The count and share of pairs **satisfying the Continued condition** — `F2 ∈ A_H` and `\|A_H\| ≥ ceil(0.90 × L2)` — with `\|A\| = 0`. Already required by the approved text, so **D8 needed no amendment**; what changed is that it is now **the only bound on the never-started boundary**. Size: **1,575 on the estimation sample, 1,573 after right-censoring**, against 8,449 scored Never started. **The count is a FLOOR and the 18.64% share is a CEILING** — different populations, never combined | Step 1 D8; sized by `0034` §6.1, routed as ledger item 10 | FIXED |
| **D3′** | Replaces **D3**, which measured nothing once its quantity became the operator. *Of pairs scored Started-and-left **at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, report the **share** completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its **share of all Started-and-left**.* **Runs at EVERY Step 13 arm** — the clearance contains `W`, so the cleared set shrinks 95.98% (`W = 46`) → 94.82% (108) → 91.34% (213), and shows absent from the subset run 5 → 9 → 18. **Reported alongside, labelled a COUNT and not a rate:** the 3,440 completing at any point before `τ_pull`, with its exposure-weighting by show recency stated at the point of use. **The two do NOT bracket the quantity** — both truncate observation and neither is a lower bound | `0034` §6.4, written into `task-sheet.md` Step 8 | **FIXED** |
| **`pull_date` / `τ_pull`** | **`pull_date = 2026-08-11`, `τ_pull = 2026-08-11T00:00:00Z`.** Every record with `watched_at ≥ τ_pull` is discarded. | **`0011`, Human Lead 2026-08-11** | **FIXED — D11's deferred value is now closed** |

`0011`'s constraint check: earliest per-user fetch instant **2026-08-11T05:01:26Z ≥ τ_pull** ✓.
Consequence carried in `0011`: the discarded tail is ~1 day for early-fetched users and ~2 for
late-fetched ones, so **the discarded-record count is not evenly distributed across the pool.**

## Step 2 frame — the population every result is computed on

**Owner Human Lead, execution delegated to an agent under `0013`.** Artifact:
`artifacts/step2-frame-ledger-and-distributions.md`.

**Frame: 1,138 shows, 220,107 S1-completer pairs.** Candidate set 2,094 shows (≥50 completers).
Exclusion ledger, in the order the rules were written:

| # | Rule | Removed | Remaining |
| :-- | :--- | ---: | ---: |
| 0 | Candidate set, ≥50 S1 completers | — | 2,094 |
| 3 | No real season 2 | 796 | 1,298 |
| 4 | S2 listed but unaired (`aired_episodes = 0`) — **`0015`** | 12 | 1,286 |
| 5 | S2 finale aired after 2025-12-31 (`first_aired < 2026-01-01T00:00:00Z`, half-open per D13) | 60 | **1,226** |
| 6 | Season over **26 episodes** (S1 or S2) — **`0020`** | 51 | 1,175 |
| 7 | Gap over **1,095 days** (S1 finale → S2 premiere) — **`0020`** | 37 | **1,138** |

Rules 1, 2 and 8 removed 0. Rules 6 and 7 overlap on exactly 1 show, so order is immaterial.
**Season 0 is filtered inside every show, never used to exclude one** — 878 candidates carried one.

### Structural thresholds — `0020`, Human Lead 2026-08-12

- **No minimum season size.** `ceil(0.90 × L1)` already scales per show. `L1 = 1` and `L1 = 2` are
  retained; `min(L1) = 1`, `min(L2) = 2`, so **no in-frame show has `L2 = 1`**.
- **Max 26 episodes** on either season. 26 is the traditional full broadcast season; the cut is
  insensitive from 26 to 40 (1.1–2.4% of pairs). **22 was rejected** at 196 shows / 13.8% of pairs.
- **Max 1,095-day gap** (3 years). The empty `3 y+` bucket is the cap made visible.
- Combined cost **88 shows, 12,851 pairs, 5.5%.**
- **The size cap is partly a cadence threshold: 44 of its 51 shows are C4.** C4 falls 476 → 425.
  A C4 result is computed on a population stripped of its longest-running titles.

### Other Step 2 definitions

| Term | Definition | Where |
| :--- | :--- | :--- |
| **Air period** | **Calendar year of the S2 finale**, bucketed **pre-2020 / 2020–2022 / 2023–2025**, bracketing the production shutdown. Frame: 757 / 213 / 168. **Strongly collinear with cadence — not an independent cut.** | `0017` |
| **Size quintile** | Cut over **the frame**, not the 2,094 candidates, on the **recomputed** `pool_completers`. Frame bins **238 / 221 / 224 / 227 / 228**. **A quintile label is not a stable identifier** — rebuild the frame and every boundary moves. | `0018` (see [[open-items-and-contradictions]] X3: `0018` still publishes the superseded 1,226-frame bins) |
| **`pool_completers`** | Step 1 §4 applied against **real** `E1`, `L1 = \|E1\|`, `F1 = max(E1)`. **The max-observed proxy is superseded and no result may use it.** Changes nothing on this frame (proxy = real on 1,225 of 1,226). | `0019` |
| **No content filters** | Anime and daily-strip/soap exclusions **dropped before first use.** The concern was release structure, not genre. Release structure is recorded as **fields**, thresholds set separately. The jp shows that left (92 → 60) left via the 26-episode cap, not by genre or country. | `0014`, Closed 2026-08-12 |
| **Per-season network** | **DROPPED as a field.** 47 of 6,645 season objects populated (0.71%); one show in 2,094 with two distinct values, read as noise. **Platform fragmentation is not a variable in this study** — no result may control for it, stratify on it, or rule it out. | `0016` |
| **`show_network`** | Show-level, 100% populated, 150 distinct — but it records **today's** network. **Must not be used as a release-time availability measure.** Descriptive only. | `0016`, README open item 18(b), still open |

**D12 as applied on the real frame:** C0 **0** · C1 206 (18.1%) · C2 340 (29.9%) · C3 167 (14.7%)
· C4 425 (37.3%). **Fragility count: 7 shows within one day of a bucket boundary, 0.6%** — by
D12's own test the thresholds are **not load-bearing** and a Step 13 arm on them is not indicated.
(238 sit within three days, but 220 of those are same-day drops at distance exactly 2 by
construction. **The one-day figure is the meaningful one.**)

## Step 5 — contamination vocabulary. PROPOSED, gate not approved.

**Artifact `artifacts/step5-contamination-diagnostics.md`, revision 6, FINAL.** Reviews in
`artifacts/step5-red-team-reviews.md`. See [[gate-step5-contamination]] for the arc.

### Layer 1 record tags — no rows dropped. Required by Step 7 and Step 8.

| Tag | Definition |
| :--- | :--- |
| `corrupt` | `watched_at` absent or pre-1990 |
| `backfilled` | `τ_ins(id) − watched_at > 180 d` |
| `airdate_stamped` | `(show, season, episode, instant)` tuple shared by **≥5 unrelated accounts** |
| `postdated` | `watched_at` more than **30 d after** insert |
| `clean` | none of the above |

**The 180-day threshold is a conservative judgment, not a data-determined break.** Per-day density
is monotone decreasing throughout; revision 1's "trough" was a bin-width artifact (Red Team C1).
**The only real break after 1 day is at 7 days.**

### The instrument — the play-`id` insert-time calibration

The Trakt play `id` is a global auto-increment assigned at **write** time, so it orders records by
insertion regardless of what `watched_at` claims. Fitted on `checkin` and `scrobble` only (a bulk
import mints `watch` rows), monotonised by **isotonic regression (PAVA)**, not a cumulative max.
**Held-out validation** (fit on even-indexed accounts, test on 2,185,696 real-time records of
odd-indexed accounts, no account in both): **median lag +0.003 d, 90.5% within one day.** Residual
error runs slightly **early**, so the diagnostic **under-flags**. Zero API calls.
Artefacts: `processed/step5/calibration.npz`, `record_lag.npz`.

### The insert-time bound

*A viewer cannot log an episode before watching it*, so a record's insert instant is an **upper
bound** on when it was truly watched. Latest defensible clock start:
`T0_latest = max(S2_finale_date, date(max τ_ins over the S1 completion evidence))`.
**Correct basis: the completion prefix, with the `max()` in force.**

| Population | Pairs | Median elapsed at `T0_latest` | Open at `W = 60` |
| :--- | ---: | ---: | ---: |
| The **1,542** (excluded) | 1,542 | **40.0 d** | **58.6%** |
| The **720** (C5, no S2, retained) | 720 | **1,738 d** | **7.92%** |
| — the 425, two-class | 425 | 1,717 | 13.4% |
| — the 295, air-date class | 295 | 1,762 | 0.0% |
| Every pair with no S2 evidence | 25,277 | 1,532 | 11.3% |

**`1,738 d / 7.92%` is the figure to use for the 720.** "Median 2,150 d / 8.1%" is **withdrawn** —
it came from a unit bug plus the wrong basis. See [[withdrawn-claims-register]].

### The two populations — Step 5 ruling 1

> **W is derived from clean records only, then applied to everyone.**

| Population | Pairs | Who reads it |
| :--- | ---: | :--- |
| **Analysis population** | **201,900** | Step 8 classifies these |
| **W estimation sample** | **128,099. Determinate.** | Step 6, which applies D14's C1 restriction **on top** |

Waterfall, monotone by construction: 201,900 → has S2 evidence 178,165 → `T0` not contaminated
155,131 → completing record not post-dated 152,126 → **first S2 watch clean 128,099**.

The analysis population **deliberately** retains 23,067 pairs with a fabricated `T0`, 46,642 whose
first S2 watch is contaminated, and 3,296 whose completing record is post-dated.

### Post-dating — the four readings, and why they are moot

**Adoption 3 was DROPPED (revision 6).** No pair is deleted for post-dating; records are tagged and
kept out of the W sample. The four readings are four ways to apply a rule that no longer exists.
Recorded because the **directions differ and a table ordered by retention alone hides that**:

| Reading | Retained | Bias direction |
| :--- | ---: | :--- |
| **Adopted — tag only, delete nothing** | **201,900** | neutral |
| P, delete the pair | 198,604 | never-started **down** |
| R1b, drop every post-dated S1 record | 198,817 | down |
| R1n, drop only the completing record | 199,957 | down |
| R3, re-date to insertion time | 201,900 | never-started **up** (median completion shift **−198.7 d**) |

The adopted rule coincides with R3 in **retained set**, not in method: R3 rewrites timestamps, the
adopted rule only tags them. That distinction is what avoids E4 — §2.2 (canonical timestamp = the
**minimum `watched_at`**) is untouched, and no re-dating bias is introduced. R3 would also have been
a **selective** re-dating: if `τ_ins` were trustworthy for 3,307 post-dated records it would be
trustworthy for 8,001,189 backfilled ones, where substitution moves completion much **later**.

### Contamination scale, for reference

| Class | Records | Share of 27,656,631 |
| :--- | ---: | ---: |
| Backfill >180 d | 8,001,189 | 28.9% |
| Air-date-stamped (mode 3) | 2,021,537 | 7.3% |
| Corrupt, pre-1990 (369,590 at exactly 1970-01-01) | 690,774 | 2.5% |
| Undated | 379 | 0.001% |
| **Union** | **8,831,718** | **31.9%** |

**Mode 3, air-date stamping**, was not previously identified: exact top of hour, seven days apart,
00:00–05:00 UTC, **up to 198 accounts sharing a single instant** (corrected from an uncommitted and
wrong "164"). **TV Time is a minority of the problem** — only 31.7% of backfill was written after
2026-06-01; the rest is eleven years of ordinary onboarding backfill. The shutdown wave is
3,115,531 records over four weeks (11.3% of the store) against a ~174,000 baseline, an **excess of
2.94 M records = 10.6%**.

## Step 3 crawl constants — agent-set, `0006`, Open awaiting ratification

**Source `src/step3_user_discovery.py:169-191`.** Full table retained; the load-bearing ones:

| Constant | Value | Note |
| :--- | :--- | :--- |
| `TARGET_USABLE` | **4,000** | The rule that actually stopped the run — **not** the plateau rule `task-sheet.md` names, which ran 36 rounds and never fired (final ratio 0.314 against a 0.20 trigger). `0005` |
| **`MIN_EPISODES_USABLE`** | **10** | `episodes.watched` from `GET /users/:id/stats` — an **account-wide** distinct-episode count, **not per-show**. Ten episodes across ten shows passes; nine inside one show fails. Removed **232** accounts and nothing else removed any. **Warrant accepted as not literally true** (README item 13, closed 2026-08-12): `min(L1) = 1` and 152 in-frame shows have `L1 ≤ 6`, so exposure is **at most 22 accounts, 0.5% of the 4,320 screened** — 210 of the 232 had zero episodes. All 232 recoverable at **0 live calls** |
| `call_budget` / plateau rule | 6,500 / 3-round MA ≤ 0.20 of peak on 2 consecutive rounds after ≥10 | budget 5,300 spent; plateau never fired |
| `n_seeds_target` / `max_depth` | 300 / 3 | Seeds = **movie-comment authors**, 172 distinct films, `0008`. Depth 3 never reached |
| `step4_page_limit` | 250 | matches `limit=250` in `0002` |

## Step 4 — the pull, and the rules that governed it

**Source: `GET /users/:id/history`, unfiltered, one sweep per user** (D15 / `0002`). One sweep is
one logical **pass**, not one call; throughput is estimated in **pages**.

| Term | Value | Where |
| :--- | :--- | :--- |
| **Pull order** | **Stratified round-robin** over ten equal-count forecast-page bins, one user per bin in turn, deterministic within bins. Amends an initial **median-out** instruction, which left a *centered* slice with **no user above 73 pages** at ten hours in a pool reaching 1,034. Cost: **~12% fewer users/hour**, accepted explicitly. | `0009` |
| **Tail cap** | **300 forecast pages**, skip whole, never truncate — **plus an actual-pages guard** that discards mid-sweep overruns. Excludes **38 users, 0.93%**, keeps 92.8% of pages. Justified as a **circuit breaker on forecast error**, not as protection against a slow user. Direction **upward** on the headline. | `0010` |
| **Sweep completeness rule** | **Full `X-Pagination-Page-Count` coverage plus a residual within 2% of `X-Pagination-Item-Count`.** Exact equality is **not** required — the pilot failed 7 of 10 on residuals from −97 to +20, and under exact equality the study would discard ~70% of its pool. **Amends `0002` condition 2 and Step 1 §0 — a rule inside an approved gate.** **Reviewed by Red Team 2026-08-12, which returned HOLD; UPHELD by the Human Lead on cascade cost, not on merit (`0023`).** Three findings became Step 14 limitations. | `0012`, upheld by `0023` |
| **Over-tolerance users** | Pages **discarded, logged, never truncated**, and must stay distinguishable downstream exactly as `access_denied` does. **287 users on the final ledger**; their raw pages remain cached, which is what made the neutrality check possible at zero API cost | `0012` |

**`0012` requires three behaviours counted separately, never collapsed into the tolerance:** header
**over-count** (benign, 256 of the 287), header **under-count** (benign and in the safe direction —
**31 of 287**, corrected from a mid-run "24 of 235"), and duplicate records.

**The third is misattributed in `0012` and the correction is in `0023`.** `0012` cites "5 duplicates
in 14,236 records" as **cross-page** duplicates. Instrumentation records
`cross_page_duplicate_records: 0 users, 0 records` across 2,137 users and 22,725,090 records.
**Cross-page duplicates have never been observed in either run.** What does occur is **within-page**:
147 records, the same `id` twice on one page, meaning a 250-slot page carried 249 distinct records.
That behaviour **is not a required output, is described nowhere, and has no stated interpretation.**

**Proof that the residuals are not truncation:** page-count and item-count headers were identical on
every page of every sweep; and re-sweeping one user at `limit=100` returned the **identical record
set in identical order** as the cached `limit=250` sweep — 1,459 distinct records both ways, while
both headers reported 1,460.

### What `0023` established about the 2% tolerance, and what did not change

**Nothing in the study moves.** Cohort 2,549, frame 1,138 shows, 220,107 pairs, 201,900 retained,
128,099 estimation sample — all stand. The tolerance was not touched and nothing was re-run.

**Three findings now travel to Step 14 as limitations:**

1. **The rule validates itself against itself.** Leg 1 gates on `page_count`, which is
   **`ceil(item_count / 250)` in all 2,839 ledger rows, zero mismatches** — so it is derived from
   the very header leg 2 exists to absorb. A **short** final page proves the sweep reached the end;
   a **full** final page proves nothing, and leg 1 cannot tell them apart.
2. **The discard is NOT outcome-neutral.** Measured at zero API cost on the discarded users' cached
   raw pages: has-any-S2 **89.78% (discarded) vs 88.52% (retained)**, **+1.27 points, 95% CI [0.87,
   1.66], z = 5.98, p < 0.001**, intervals non-overlapping. **Direction: up** on the never-started
   share, **compounding with the seeding and liveness biases rather than offsetting them.**
   **Pooled effect 0.13 points** (88.52% → 88.65%), because the 287 carry 10.2% of the pair pool.
   *Statistically clear, practically small — neither half may be quoted without the other.*
3. **Red Team's final-page shape test** — every interior page full at `limit`, final page strictly
   between 0 and `limit` — would discriminate **exactly** rather than by calibration, at **~2,800
   calls, ~19 minutes, and no re-pull**. **Declined on cascade cost, not on merit.** If the pull
   ever resumes, the cascade argument weakens and the shape test should be reconsidered rather than
   inherited as settled.

**The ruling's stated reason, in full:** tolerance → cohort size → completer counts per show → which
shows clear ≥50 → the candidate set → the frame → the structural thresholds → the 220,107 pairs →
the approved Step 5 rule computed on them. **A 0.13-point correction at the far end does not justify
re-deriving that chain.**

**How the 2% was actually set, recorded in `0023`.** The pilot's p95 is **1.4%** and p99 = max is
**11.7%**, with nothing in between, so **every tolerance from ~1.5% to 11.7% split those 20 users
identically** — and the most aggressive end of that band was chosen, with no sensitivity table and
without the choice being stated as a choice. **On the full run there is no such gap:** absolute
residual share over the 287 discards runs min 2.01%, median 3.92%, max 99.9%, with **168 (58.5%) in
the 2–5% band** — so a 5% tolerance would have retained 168 of the 287. The threshold cuts through
the middle of a continuous distribution.

**One structural asymmetry nobody chose.** Accumulated records can never exceed
`limit × page_count`, so a positive residual is capped at **249**. **Above roughly 50 pages the
under-count arm cannot fire at all.** The rule presents as a symmetric two-sided threshold; it is a
one-sided test on large users and a size-correlated discard on small ones. It also discards **31 of
287** users in the direction `0012`'s own table calls *"benign, and in the safe direction."*

## The population chain — every number a result rests on

See [[population-chain-steps-2-3-4]] for the reconciliations. Headline figures:

**4,088 usable users** → 4,050 in plan after the 38 over-cap → **pull stopped at 2,836 decided
(70.0%)** → **2,549 `complete`** (287 discarded over tolerance) → 44,617 shows with an S1 record →
**2,094 candidates** at ≥50 completers → **1,138-show frame, 220,107 pairs** → Step 5 proposes
**201,900 analysis population** and **128,099 W estimation sample**.

## Standing rule — when a post-approval edit reopens a gate

**An edit that changes a *rule* reopens the gate; an edit that adds *evidence* for a rule already
adopted does not.** Fixed 2026-08-10 in the Step 1 approval record. **`0012` is the first edit that
fails this test and was recorded as a Human Lead amendment anyway** — README open item 15 flags it
as not yet put to Red Team.

## Probe figures — n = 1, existence proofs, NOT rates

Play-record inflation **28.125%** (123 records, 96 distinct pairs, 27 surplus records, **25**
episodes duplicated — 27 and 25 answer different questions and are both right). S1/S2 overlap
**41.31 d under definition (a)**, inverting to **360.73 d of separation under (b)**. 64 pages per
user at `limit=250`. `episode.ids.trakt` disagreement with `(season, number)`: **untested**, not
confirmed — and the Step 2 frame's four absolute-numbering shows have since been removed by the
26-episode cap, though their finding stands (100% overlap on all four; the **withdrawn `1..F`
range form would have failed on all four**).

## Season membership, outcome states, counting rules

Unchanged from Step 1 and still governing.

`E` = the **listed episode-number set**; `L := |E|`; `F := max(E)`. **`F := L` is forbidden**
except by Human Lead adoption of the §3.3 fallback. Source `GET /shows/:id/seasons?extended=
episodes,full`, one call per show. `show.aired_episodes` is **never** used.

### The outcome states, POST-AMENDMENT — `0034`, 2026-08-12

| State | Condition |
| :--- | :--- |
| **Never started** | `\|A\| = 0` — decided at **`τ1`, 108 days** |
| **Continued** | `\|A\| ≥ 1` **and** `F2 ∈ A_H` **and** `\|A_H\| ≥ ceil(0.90 × L2)` — decided at **`τ2`, 199 days** |
| **Started and left** | `\|A\| ≥ 1` **and not** the Continued condition |

**The pre-amendment Continued row read `|A| ≥ 1 ∧ F2 ∈ A ∧ |A| ≥ ceil(0.90 × L2)`, evaluated at
`τ1`. That is superseded.** Any live use of that form is stale — see
[[open-items-and-contradictions]].

**The `|A| ≥ 1` conjunct is load-bearing, not tidying.** Without it, a pair first watching S2 on
day 150 and completing by day 190 satisfies the other two conjuncts with `|A| = 0` and falls in
**two** states. It **makes the cost visible; it does not cause it** — the cost belongs to the
asymmetric anchoring, and D8(ii) is that asymmetry measured. Attributing 1,575 to the conjunct was
withdrawn.

**Partition proof survives verbatim in structure:** `A = ∅` / `(A ≠ ∅ ∧ C_H)` / `(A ≠ ∅ ∧ ¬C_H)`.
No fourth state, no changed denominator, Step 8's sum-to-sample invariant untouched.

**Continued is a 199-day statement while never-started is a 108-day statement, and the two must
never be described as measured alike.** This appears wherever the split is reported, not in a
footnote.

Abandonment point `p = |{e ∈ E2 : e ≤ m_H}| / L2` where `m_H = max(A_H)` — rank-based, defined only
for Started-and-left. **Direction Step 10 must name:** the 2,246 pairs leaving Started-and-left are
the ones that got furthest, so abandonment looks **earlier** on the published chart, and the
`p = 1.0` residual **changes size under `A_H` and must be re-reported, not carried over.**

Counting: **distinct episodes, never play events**, dedup key `(show.ids.trakt, season, number)`
scoped to the user; **canonical timestamp = minimum `watched_at`**; **all `action` values count as
watching**, `checkin` included, with `action` retained as a column.

## Required diagnostics fixed at Step 1 — unchanged

D2 negative-lag split by binding term · D3 resumption over `[τ1, τ1 + H)` · D4 S3-without-S2 bound ·
D8 never-started post-window · D9 split-artifact counts · liveness bound (**up**) · right-censoring
removal as **two lines** · dropped-S2-evidence count. `L2 = 1` shows excluded at Step 8 (**moot on
the current frame — `min(L2) = 2`**).

Related: [[gate-step1-outcome-definition]], [[gate-step5-contamination]],
[[population-chain-steps-2-3-4]], [[open-items-and-contradictions]], [[withdrawn-claims-register]],
[[decision-log-step18]].
