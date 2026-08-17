---
name: gate-step8-analysis-table
description: The Step 8 analysis-table gate — the LAST of the five and NOT APPROVED. Eight Red Team passes, every one a HOLD; what each found, what closed it, and the findings that falsified the review's or the ruling's own premise. Current through decisions/0094, 2026-08-16
metadata:
  type: project
---

# Step 8 — the analysis table. **THE LAST GATE, AND IT IS NOT APPROVED.**

**Launched `0072`, 2026-08-13, as the dual pair `analytics-engineer` / `-b`. Ruled on across
`0066`–`0094`. Eight Red Team passes. Every one a HOLD.**

**Why:** the gate arc is the thing the Step 18 decision log is for. The analysis will show the
numbers; this shows the judgement, including the several occasions on which a ruling or a review
was right in substance and wrong about the object it named.

**How to apply:** this is a pointer, not a source. `task-sheet.md` Step 8 and the
`analytics-engineer` pair are the spec of record; the arms' own deliverables govern on what was
measured. Where this file and those differ, **they govern** — and this file has been stale before.

---

## The state, in one block

- **NOT APPROVED. Nothing in `0066`–`0094` is adopted as a Step 8 result**; every entry from `0073`
  on says so in its status line.
- **Grain: the POSITION-5 row set** — 196,654 rows on APPLY with `live` and `outcome` as **columns**,
  plus DERIV 147,370 and the D4 count. Not position 7 (`0074` §1).
- **89 enumerated column names.** The count has been 87, 88, 89 and 90; **90 was the union of the two
  arms' 87-name sets and was never adopted.**
- **NINE invariants** — six pure code checks, one code-by-construction, two data checks (`0088` §1(c)
  promoted the ninth). **`0089` §3: no surface said nine, and the negative grep passed clean.**
- **Positions 1, 2, 3 and 7 are INERT and labelled with the reason.** Position 3's *rule* removes
  58,345 pairs **upstream of line 1** — the study's largest single exclusion, appearing in the
  waterfall as a `0`.
- **After the eighth pass, arm a has no blockers left** — three minor items, all against its text
  rather than its arithmetic. **Arm b carried three.**

---

## The eight Red Team passes

### Pass 1 — `0076`. The label correction that INVERTED the finding

**Found:** the dual run split 4-of-6 against 6-of-6 on how many invariants could fail. **`0074` §2 had
labelled `p ∈ (0,1]` a DATA CHECK.**

**Closed by:** `0076` §1 correcting it to **CODE CHECK**, on **both instances' own proof** — S&L
requires `|A| ≥ 1` so `m_H` exists, and set membership bounds the rank numerator in `[1, L2]`.

> **The correction inverted the finding: FIVE of six unfalsifiable, with ZERO pure data checks.**
> *"Four of six"* is superseded and was corrected in eight places. **The two DATA checks were added
> because the set had none.**

Also from this pass: `0077` (population labels, the drop set, the 89 column names, the `A_H`-not-`AH`
spelling rule) and the D9 strict / loose / third-key definitions, which **had existed only in one
arm's code — undefined on every surface an isolated instance reads.**

### Pass 2 — `0079`, `0080`. Two blockers; a 99-row hole that survived two reruns

**Found:** the column set travelled as a **count**, and the invariants named populations they did not
cover.

**Closed by:** replacing the count with **enumerated names** (`0080` §1) and requiring
**`rows_asserted + rows_not_asserted = rows_in_the_stated_population`** at every invariant (`0080` §3).

> **One arm had a 99-row hole: `19,042 + 177,513 = 196,555` on a 196,654-row table** — numerator
> post-liveness, denominator pre-liveness. **The 99 uncovered rows are exactly the started-and-left
> liveness exclusions.** *"Neither report disclosed the gap, no control could see it, and it survived
> two reruns."* Correct: **19,141 + 177,513 = 196,654.**
> **An invariant that passes on one population and was never run on another READS AS A PASS ON BOTH.**

Also: **deliverable provenance** — every count names the **build** it was measured on, not only its
population — and the **four inert positions kept and labelled**, because *"an unlabelled always-zero
filter reads as evidence THE RULE FOUND NOTHING when it is evidence THE RULE CANNOT FIRE."*

### Pass 3 — `0085`. HOLD, three blocking, four publishing

| | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | The two arms clustered **different D9 universes** and the spec named none. Disjoint largest clusters, maxima 8 against 10, **while every ruled count reconciled** | Spec now requires the universe **named at the point of use**. Re-filed from arm-against-SPEC to **arm-against-arm**, which is the dual diff |
| **B2** | The `p_at_bound` emptiness was **asserted in prose and not emitted on DERIV** in one arm — `1,056` appeared zero times in its waterfall JSON | Four cells on each of four populations. **`CLAUDE.md`'s standing rule — both populations, always — not a new requirement** |
| **B3** | The **half-open UTC-instant form** and **D11-as-global-cutoff** carry **no assertion**. Both arms self-report in prose | **CARRIED to the Human Lead.** Blocked passes 3 and 4 |
| **P3** | `0084`'s new JSON branch tested `STRUCK` against the whole string value while the `.md` branch windows it | Fixed **and demonstrated** with a proximity probe, though Red Team found the gap **empty** — because *"empty today"* is exactly how the JSON-string limit was recorded at `0060` while a defect sat in it |
| **P4** | *"By construction"* had a link that was not construction: `max(E2) = F2` holds only because the finale is the highest-numbered listed episode | **Three links, not two.** Measured, not assumed: 0 of 1,138 frame shows |
| **§5** | **703 is not the marginal cost of the silence test.** Silence alone excludes **1,355** on APPLY; `NOT Continued` spares **652**; `1,355 − 652 = 703` | Both arms now publish both, on both populations, with the identity stated. **DERIV: `751 − 652 = 99`** |

### Pass 4 — `0087`. HOLD, three blocking, six publishing. Two findings are defects in the chain's own entries

- **F1 / B3 stronger.** *"`0085` §7 carried B3 as 'no assertion.' The fourth pass establishes something
  worse: there is no MEASUREMENT either."* Both arms' compliance is **TRUE** and independently
  confirmed — **but neither reports how many rows the two forms could differ on**, so a reader cannot
  tell whether the mandate is load-bearing or vacuous. Red Team's ground: *"the unstated version of
  exactly this scope is what produced Step 7's 792-against-791."*
- **F2.** Three D9 **coverage** counts do not reconcile: arm a publishes **46,428 and 46,366 for one
  labelled quantity, 27 lines apart**; the two arms' "U1" are consequently different sets; and
  **747,478 (A) against 726,103 (B)** is reported by neither arm and no entry. **D9's ruled result is
  0 and 0, and the coverage counts are the only thing separating that from "looked nowhere."**
- **F3.** **The propagation surface numbering is INVERTED in `0083`, `0085` and `0086`.** The FILES
  edited were always right; the NUMBERS **pointed a re-verifier at the two files that were not touched
  and exempted the two that were.** *"That is the look-nowhere shape, in the entries written to fix
  propagation defects."*
- **F4.** **The coverage apparatus mostly cannot fail.** 8 of arm a's 13 identities are
  `cover(unit, pop, N, N)`; arm b hardcoded `identity_holds: True` at three and chained
  `.get(…, .get(…, True))` so **an invariant with no coverage key contributed a pass.** *The helper's
  own docstring names the failure mode.* **The dual diff cannot see any of this: both arms did it.**
- **F5–F9, carried:** `specs/step8-readback.md:3` still saying Step 8 *"has not launched"* (**and
  `specs/` is not one of the eight surfaces**); arm a's column check asserting against a **hand
  transcription** rather than the spec on disk; the **build-tag convention unstated**; the arms
  asserting invariant 3 over **different record sets** (6,065,704 against 6,065,610); three corrupt
  year-1 S1 completion dates in arm a, *"probably inert — but 'probably' is not measured."*

### Pass 5 — recorded in `0089` and `0090` §3. B3's measurement caught a real bug on the first run

> ***B3 EARNED ITS COST ON THE FIRST RUN.*** Instance B's per-site D11 table — 13 sites, applied at 12,
> **asserted at each** — found that **D11 was reaching the four `action_count_s1_*` columns with no
> ruling behind it.** ***Asserted per site, those four would have FAILED on r3.*** **A per-site
> assertion found in one run what *"D11 is applied to every computation"* had asserted in prose across
> five builds and two gate reviews.**

**Fifth-pass findings:** **F1** — the number that settles B3, the **outcome-state count on the
separating interval**, four numbers, **measured by neither arm**; and `0089`'s own claim that *"both
arms emitted both intervals"* is **FALSE of arm b**. **F2** — arm a's `real = len(parts) > 1`
independence proxy, under which three *"REAL ARITHMETIC"* identities are complementary partitions of
one mask and cannot fail, **including the one its deliverable calls "the identity that closes the hole."**

**Also from this pass:** `0089` §1 — `tau2 > τ_pull` is 0, **but 20 APPLY and 17 DERIV rows sit exactly
AT `τ_pull`. The bound is attained; a `>=` form would fail.** *"A passing assertion at the bound and
one with slack are not the same evidence."*

### Pass 6 — recorded as in-place amendments to `0089` and `0091`. Three withdrawals, all of this chain's own text

| | What was withdrawn | Why |
| :-- | :--- | :--- |
| **F1** | `0091` §1's warrant: *"line 6 does not move because the silence test reads an insertion clock, not an episode timestamp"* | **Structurally wrong.** The rule is conjunct 1 **AND** conjunct 2, and conjunct 2 is `NOT Continued` — an **episode-timestamp** computation that moves on 55 APPLY rows under this very counterfactual. **A property of conjunct 1 cannot explain the invariance of the conjunction.** And **it is not established that the 703 was measured at all** — if conjunct 2 was held at the adopted outcome, `703 → 703` is a **tautology** |
| **F2** | `0089` §2(a)'s *"so `0068`'s strictness ruling moves a real row in `\|A\|`"* | **Wrong object.** `0068`'s strictness is about **INSERTION instants** in the silence test; the `1` is a distinct S2 episode by canonical `watched_at`. Instance B measured the ruling's own quantity: **max insertion instant exactly at `τ1` = 0 on 196,654 rows, both populations.** ***So `0068`'s strictness ruling is VACUOUS on this data, and one arm publishes that it is load-bearing.*** **The two arms agree on every number and disagree on what the number is ABOUT** |
| **F3** | `0091` §2's *"the mechanism is DEMONSTRATED, not asserted — all 15 identities re-run against `population + 1` and must FAIL"* | **Overstated for arm a.** A `+1` perturbation **fires identically on a same-mask denominator**, so it would have passed on the very build whose defect it claims to have fixed. It tests that the identity is arithmetic rather than a literal; **it does not test INDEPENDENCE** — inside the block citing `0088` §2's strike of an asserted control |

### Pass 7 — **`0092`, which never names the pass. And the two records are numbered ONE APART**

**`0092` is the seventh-pass entry.** `artifacts/step8-waterfall-a.md:375` says so in terms —
*"`decisions/0092`, **Red Team seventh pass, N2**"* — while **`0092` itself names no pass number.**
Its content is **N2**, the `168` requirement, and it is the clearest premise-falsification in the block
(see the table below).

> ***THE PASS NUMBERING DIVERGES BETWEEN `decisions/` AND `artifacts/`.*** The `+1` perturbation
> finding is **`0091` §2's *"Red Team sixth pass, F3"*** and **`artifacts/step8-invariants-a.md:9`'s
> *"Red Team's seventh pass, finding 3"*** — **one finding, two pass numbers.** The sixth pass's
> findings exist **only as in-place amendments inside `0089` and `0091`**, which is what makes the
> offset hard to see. **Logged as R2 in [[open-items-and-contradictions]]. Not resolved.**

### Pass 8 — `0093`, `0094`. The pass that closed every blocker against arm a

**F1 is the finding that produced a `CLAUDE.md` rule.** Arm b republished *"747,478 … undeduplicated
user-show season-coverage rows"* — the characterisation `0089` §2(b) corrected **two entries earlier**
— **and contradicted itself six lines below**, its own table giving **1,007,729** for that label.

> **Root cause, `0094` §1: `0089` §2(b) reached `decisions/` and no spec surface.** The superseded
> characterisation stayed live and unmarked at `task-sheet.md:654`, `:707` and both agent files at
> `:249`. **Arm b read the spec and faithfully republished it.** ***That is `0093` in reverse: the
> ruling reached `decisions/` and not the spec, and the arm did what the spec told it.*** **Red Team
> scored it against arm b; it belongs to the propagation.**

**Arm b's other two:** **F2** — the superseded-string needles must fold into `src/step7_register.py`
and match **case-insensitively** (the needle was `six of eight`; the string present three times is
`six of EIGHT`, and **its hits table showed no row for that needle at all — indistinguishable from a
clean pass**), and its `assert` ran **after** all four artifacts were written. **F3** — the `examined`
column held pre- and post-D11 quantities in different rows.

**Arm a's three, all minor and all against its text:** **F6** a hardcoded conclusion string
contradicted by its own live counts; **F7** its falsifiability headline **differs from arm b's on the
same nine labels with neither arm flagging it**; **F8** the symmetric-difference-0 warrant, one notch
stronger than the monotonicity allows.

> **F7 is a live, unreconciled divergence and it is worth carrying into Step 18.**
> `artifacts/step8-invariants-a.md` §…: the nine labels are the same in both arms and every per-check
> label reconciles. **What differs is the SHAPE OF THE HEADLINE OVER THEM** — arm a publishes a
> **three-way** split (**6 + 1 + 2**, derived from the label strings and never typed); arm b publishes
> a **two-way** split. ***The dual diff cannot see it***: both headlines sit over an identical label
> set with identical per-check results, **so neither arm flagged it through eight passes.**
> **Reported, not reconciled. The Human Lead diffs.**

---

## The findings that falsified the review's or the ruling's OWN premise

**This is the pattern the Step 18 log should carry, because it recurs and because the substance was
sound almost every time.** `0088` §4 calls it *"the sixth occurrence, and the first with a working
countermeasure."*

| # | The premise as stated | What measurement found | Where |
| :-- | :--- | :--- | :--- |
| **N2 — the clearest case** | *"The two arms read **168** on populations 23,453 apart … **168 cannot be correct on both.**"* | **168 is correct on line 1 (220,107), position 5 (196,654) AND post-liveness (195,951) on APPLY.** Both arms' differing readings would have given 168. **The agreement was INVARIANCE, not error.** ***What is real and no entry recorded: DERIV measures 153.*** **The requirement stands and is strengthened** — state the population **and measure on both**, because the count is invariant on one and not the other | `0092` §3 |
| B3's referent | The ruling identified B3's two mandates as **invariants 7 and 8** | **They are not.** 7 and 8 are already measured, already published, already labelled DATA CHECK, and **Red Team's fourth pass praised exactly them.** *"The reasoning given for the ruling describes a state that does not exist."* **The substance — measure rather than publish a residual — applies unchanged to the actual two mandates** | `0088` §1 |
| F2's axis | The ruling described 747,478 and 726,103 as **"show IDs against frame IDs"** | **Neither is a show-ID count and neither is frame-restricted.** Both are user-show quantities over the whole sweep. **The conclusion holds on a stronger footing than the reason given** | `0088` §2 |
| The D9 universe | The ruling named the universe **"U3"** | **U3 is the 75 candidate pairs — the narrowest.** The reasoning identified **U1 four separate ways** and *"the letter contradicted all four."* **Confirmed with the Human Lead before propagating rather than resolved by inference** — a rerun on the wrong universe would have cost a cycle and produced a Red Team pass on the wrong object | `0088` §3 |
| B3's window | `0088` §1(a) named the boundary window **`[τ1 − 24h, τ1)`** | **That is the interval on which the two forms AGREE.** `T0` is day-floored so `τ1`/`τ2` are midnight-aligned. **The separating interval is `[τ1, τ1 + 24h)`.** An arm answering with the named window alone would have returned a result on the interval that cannot separate the forms | `0089` §2(a) |
| The B3 verdict | `0089` §2(a) adopted **`OCCUPIED_INERT`** | ***Not merely unsupported — FALSE.*** Computed on **1 row of the 311**. Recomputed: **`OUTCOME_DECIDING`, 71 APPLY / 59 DERIV rows change state, 36 of them never-started → Continued — the two ends of the headline** | `0091` §1 |
| `0092`'s own cause | The rule was adopted against **hand-patching** of deliverables | ***Neither arm hand-patched anything.*** Working tree clean, every artifact pipeline-generated. **`0092`'s sign-off rule has not been violated by either arm at any point.** *"A rule adopted against a misdiagnosed cause protects nothing"* — hence `0093`, which names the cause the evidence supports: **not unsigned text, STALE text** | `0093` §4 |
| The 30-pair bound | A directed item named *"the 30-pair bound restated with the population Red Team names"* | **There is no 30-pair bound.** The only `30` matched in either artifact is **a substring of `1,230`**. ***Third occurrence of a `30` cited with no referent*** | `0093` §3(a) |
| D4's withdrawn word | A directed item named *"D4's withdrawn word in both artifacts"* | **Zero withdrawn, superseded or struck wording anywhere near D4 in either artifact.** Second occurrence | `0093` §3(b) |
| The reconciliation claim | `0086` §1: *"every D9 count still reconciles across both arms"* | **FALSE as written. RESTRICTED, not deleted**, to the **five ruled counts**; **three coverage counts do not.** *"My own parenthetical compounded it — both numbers are recoverable from arm A alone. It was never the arm-against-arm comparison it read as"* | `0087` §2 |

**Two directed items at `0085` §1 also had no referent** — the 89-vs-88 column count (**already correct,
corrected by `0083` §3, committed before the arms launched**) and invariant 7's population (**invariant
7 runs on ACCOUNTS, and re-anchoring it to the post-liveness set would make it compare a set with
itself and it could no longer fail**). **Fifth occurrence of the pattern.** `0085` §1 is the first
entry to **check before acting** and report the figures and their file and line, which is the
countermeasure the Human Lead asked for.

---

## The three rules this block put into `CLAUDE.md`

1. **Artifact sign-off** (`0092`). *No artifact is trusted without its producing arm's sign-off; a
   deliverable is corrected by **rerunning** the arm, never by hand-editing.* **It is the derived-figures
   rule one level up** — the scripts already refuse to hand-patch a number; **this refuses to
   hand-patch a sentence.**
2. **A ruling is not closed until the artifacts carry it** (`0093`). **The arms rewrite deliverables
   only on a RUN**, so every ruling since `0084` spent a window recorded-as-done, **passing on all eight
   surfaces, while both arms still published the superseded text.** *"The honest propagation report
   names both halves: which surfaces are reached, and which AWAIT A RUN."*
3. **The citation resolver** (`0094` §4). Every four-digit decision citation on all eight surfaces is
   resolved against `decisions/`; it **prints its coverage count**, **fails on any citation with no
   file**, and **fails if it finds zero citations.**

> **`0092` AND `0094` WERE BOTH CITED BEFORE THEY EXISTED** — `0092` written into `CLAUDE.md` and
> committed with **no file in `decisions/`**, cited from everywhere else; `0094` cited **8 times** with
> no file, **the second occurrence in three entries, after `0092` §2 had recorded the first and
> observed that no control could see it.** *"A gap recorded and left open is a gap that recurs."*
> **`0092` is `CLAUDE.md`'s opening rule inverted: recorded everywhere except `decisions/`.**

---

## What is still open at the gate

| Item | Whose |
| :--- | :--- |
| **The D9 tie-break.** `secondchance` (8) and `theisland` (7) are unique; **six keys tie at 6** and the arms publish different third places, both correct under their own rule. **`0088` §3 named `maigret`; neither arm picked it.** *A spec gap inside the ruling that closed a spec gap* | **Human Lead.** Red Team's position: publish all six and retire *"third-largest"* |
| **Whether `specs/` becomes a NINTH propagation surface.** It holds the written specs handed to isolated instances, **nothing checks it**, and it carried *"Step 8 has not launched"* through four occurrences | **Human Lead.** Red Team's position: adopt it |
| **The one-pair D9 divergence** — `435,642` against `435,643` on the S1-only class, the other two classes agreeing exactly | Reported, not reconciled |
| **`0090` §2's flagged reading** of *"this half"* — implemented as **every** D9 quantity with both forms | Both arms say so at the point of use; narrows if a single half was meant |
| **F7 — the falsifiability headline shape**, three-way against two-way over an identical nine-label set | Reported, not reconciled. **The dual diff cannot see it** |
| **`0091` §1's residual** — whether conjunct 2 was recomputed on the counterfactual outcome or held at the adopted one. **Arm a's `0094` build now states which, at each cell** (`step8-waterfall-a.json`, *"if conjunct 2 were held at the adopted outcome, 703 → 703 would be an IDENTITY and would establish nothing"*). **Arm b does not report the liveness count under the counterfactual, so there is no second arm to settle it** | Open |
| **`0068`'s D11-at-the-S1-walk.** Reading C moves line 1 to **220,103** — 4 pairs stop being completers, 0 completion dates move | `0068`'s own open item, **not** the set-membership denominator, which `0083` §1 closed |

**Related:** [[glossary-terms-and-thresholds]] · [[gate-step7-liveness]] ·
[[open-items-and-contradictions]] · [[withdrawn-claims-register]] · [[decision-log-step18]]
