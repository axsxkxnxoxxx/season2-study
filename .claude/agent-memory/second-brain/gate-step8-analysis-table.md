---
name: gate-step8-analysis-table
description: The Step 8 analysis-table gate — APPROVED 2026-08-17 (0098), gate 5 of 5, all five gates now closed. Eleven Red Team passes, ten HOLD then PROCEED; what each found, the eight published residuals, the five limitations travelling to Step 14, and the findings that falsified the review's or the ruling's own premise. Current through decisions/0098
metadata:
  type: project
---

# Step 8 — the analysis table. ***GATE APPROVED, `0098`, 2026-08-17. GATE 5 OF 5.***

**Launched `0072`, 2026-08-13, as the dual pair `analytics-engineer` / `-b`. Ruled on across
`0066`–`0098`. ELEVEN Red Team passes: ten HOLD, then PROCEED on the eleventh, 2026-08-17.**

**Why:** the gate arc is the thing the Step 18 decision log is for. The analysis will show the
numbers; this shows the judgement, including the several occasions on which a ruling or a review
was right in substance and wrong about the object it named.

**How to apply:** this is a pointer, not a source. `task-sheet.md` Step 8 and the
`analytics-engineer` pair are the spec of record; the arms' own deliverables govern on what was
measured. Where this file and those differ, **they govern** — and this file has been stale before.

---

## The state, in one block

- ***APPROVED, UNCONDITIONALLY, by the Human Lead, 2026-08-17.*** Record:
  **`artifacts/step8-gate-approval.md`**, **drafted by the Analytics Engineer and signed only by the
  Human Lead** — *"an agent never records its own approval."* **Builds approved: `a/2026-08-17-0096`
  and `b/2026-08-17-r8`, both confirmed by their producing arm.**
  *(Superseded, and it was this file's opening until 2026-08-17: ~~"NOT APPROVED. Nothing in
  `0066`–`0094` is adopted as a Step 8 result."~~ True through `0097`.)*
- ***ALL FIVE GATES ARE NOW APPROVED*** — Step 1 (`0001`), Step 5 (`0021`), Step 6 (`0026`), Step 7
  (`0064`), Step 8 (`0098`). **Step 8b and Step 9 are UNBLOCKED and NOT LAUNCHED.**
- **Approval is unconditional WITH eight residuals open and published**, and **§4 item 2 — the `logs/`
  provenance cost — is ACCEPTED AS RECORDED, not a correction anyone will close.** **Five limitations
  travel to Step 14.** Both lists are in [[glossary-terms-and-thresholds]] and are not duplicated here.
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
- ***THE ARITHMETIC STOPPED MOVING AT THE SEVENTH PASS.*** No pass from the eighth on found an
  arithmetic defect in either arm; the last three each **re-derived it independently and reproduced it
  to the row.** Red Team's eleventh-pass words: ***"The analysis table is right."***

---

## The eleven Red Team passes

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

### Pass 9 — `0095`. HOLD on three, **and NO ARITHMETIC DEFECT IN EITHER ARM**

**Every cross-arm figure agreed to the row.** The three findings were all in the control apparatus or
in the launch process.

| | Finding | What closed it |
| :-- | :--- | :--- |
| **F5** | **The citation resolver saw only BACKTICKED citations.** Arm b writes predominantly un-backticked — `decisions/0089 Sec 2(b)` — so **~37% of one file's citations were invisible**, and ***the founding defect would have been missed entirely in that form.*** *"Prints its coverage count"* was satisfied **to the letter while the count was blind to the class it could not see** | Anchored to citation **FORMS** after a first widening (`\b0\d{3}\b`) proved too broad and matched data. **Probed**: two un-backticked citations to nonexistent entries both caught, exit 1, file restored byte-identical |
| **F3** | **The needle register was exercised on 4 files of ONE surface** — ~4 of ~40 on surface 6, **none of 1–5, 7 or 8.** That arm's scan **opens with *"a surface check that does not open the surface the defect is on is a check that looked nowhere"* and then opened four files.** **Occupied, not hypothetical: a registered needle was live in the other arm's deliverable** — and **neither arm can fix this under isolation** | Folded into `check_surfaces.py` across all eight surfaces: **255 files, 7.0M characters** |
| **F4** | **The exemption window was measured in LINES.** `CONTEXT = 2` is ±200 characters on a hard-wrapped file and **±several thousand** on the arms' deliverables, where **137 lines exceed 400 characters.** ***The `.md` branch was NOT WRONG WHEN WRITTEN — the unit changed underneath it*** when the arms began emitting paragraph-per-line | Measured in **characters** |

> ***THE ROOT OF F1 WAS THE CHAIN'S OWN, AND IT IS STRUCTURAL — this is `0095`'s rule.*** A Red Team
> eighth-pass characterisation of **arm b's** falsifiability headline was **relayed into arm a's launch
> instruction.** Arm a published it as an **arm-against-arm divergence** — while arm b's current build
> published **the same 6 + 1 + 2 split.** **Arm a's claim was false, and under isolation it had no
> admissible way to check what it was told.** Full ruling in [[glossary-terms-and-thresholds]]
> §THE TWO ISOLATION RULINGS.
>
> ***THE NEEDLE SCAN RETURNS 441 CANDIDATES AND IS WIRED REPORT-ONLY, LABELLED "NOT YET A CONTROL."***
> Repo-wide, short needles like `793` and `97.6%` match **legitimate historical records.** *"Failing on
> 441 unread lines would block the gate on lines nobody has read; **narrowing until it passes is how a
> control gets disarmed. Neither was done.**"* **That is residual 8.**
>
> ***THE MISSING-ENTRY DEFECT, THIRD OCCURRENCE.*** `0092`, `0094` and **`0095` itself** were each
> cited before they existed; this one in **10 files**, including `CLAUDE.md` and a commit message.
> **`0094`'s resolver could not catch it because `CLAUDE.md` is not a propagation surface** — *the
> citation that would have caught it earliest was in the one file the control does not read.* **Caught
> anyway one build later, because `artifacts/` IS surface 6** and arm a's build provenance names the
> entry. ***And arm a did not remove the citation to make the control green*** — *"that is narrowing
> until it passes"* — **it reported `EXIT 1` with the cause named and left it for the Human Lead.**

### Pass 10 — `0096`. HOLD, **and it named the GENERATOR**

**This is the pass that made approval possible, and it did it by diagnosing rather than listing.**

> **Arm a's waterfall was 826 lines of which roughly 120 was measurement.** The rest was build history
> and claims about other surfaces — ***"review retires roughly three per pass; the build adds roughly
> the same number."*** **Two of this pass's three blockers were REGENERATIONS of defects the ninth pass
> had closed.** Red Team called the position **a plateau with an identifiable generator**, and said the
> class **would not exhaust under the deliverable scope then in force but would exhaust immediately
> under a narrower one.**

**Worse than stale, on the tenth pass:** arm a's deliverable told its reader `check_surfaces.py`
**exits 1** when it exits **0**. **True when the arm measured it; false by the time it was read.**
***And arm a's behaviour was correct throughout.*** **The defect is that a control's exit status was
publishable in a permanent deliverable at all.**

**`0096` RULING 1 removed the CATEGORY rather than the instances:** a deliverable asserts only what its
own arm measured. **`0096` RULING 2** answered the pass's F1 — which correctly found that `0095`
plugged one route and left another open — **in the direction it could not choose for itself**:
`decisions/` **may** carry cross-arm content, deliberately, and the arms are now told so.
***That withdraws part of `0095` §1.***

### Pass 11 — `0097`, then `0098`. ***PROCEED***

**F1: the two `artifacts/step8-readback-{a,b}.md` files state FOUR things that are false today** —
`processed/` not being a surface (it is **8 of EIGHT**), `adopted_rule.json`'s revision-3 figures,
*"Step 7 NOT approved"* (**approved at `0064`**), and Step 0's superseded 403 rule. ***No control can
see any of them*** — the **third blindness class** — and **eleven passes did not catch them.** The
eleventh found them **only because `0096` §1 drew a line these files sit outside.**

- **They are stamped AND allowlisted by name with a reason** (`0097`). **Both, because a stamp declares
  a file's STATUS and does not exempt it.**
- **Hand-stamping them is not a `0092` breach:** `0092` forbids hand-**correcting a deliverable's
  content**; **declaring a non-pipeline file non-operative is not that** — and **Red Team disputed the
  claim that these files were stranded between `0092` and `0096`, and it was right**: both already
  carried a hand-added `0086` status stamp, **so the precedent existed inside the files themselves.**
- ***`0096` §1's boundary was one notch too narrow.*** It was scoped to *"a **gate deliverable**"*, and
  `artifacts/` holds two files that are not. **Red Team's own framing, adopted:** *"the ruling was
  correct and its boundary was one notch too narrow"* — **a different diagnosis from the plateau it
  reported at the tenth pass.**
- **Neither arm ran for `0097` and neither arm's four deliverables were edited.**

---

## The approval — `0098`, and what it turned on

**`0098` / `artifacts/step8-gate-approval.md`. Approved by the Human Lead, 2026-08-17,
UNCONDITIONALLY. Gate 5 of 5. No agent recorded an approval.**

**What is approved:** the **position-5 row set, 196,654 rows × the 89 enumerated columns on APPLY**,
with **DERIV (147,370) flagged in it** and `live` and `outcome` carried as columns · **the waterfall on
both populations, reproduced independently by both arms to the row** · **nine invariants, all passing,
each naming its population and satisfying its coverage identity.**

**The distinction that carried it — and it is the same shape as `0064`'s:**

> ***Reviews 1–7 CONTESTED SUBSTANCE AND CHANGED WHAT IS MEASURED*** — the filter order, the invariant
> set's falsifiability, the coverage identities, D9's keys and universe, `p_at_bound`'s meaning, D11's
> scope, and the half-open boundary form.
>
> ***Reviews 8–11 FOUND ALMOST NOTHING IN THE ARITHMETIC AND A GREAT DEAL IN THE PROSE.***
> **`0096` removed the category rather than the instances, and the eleventh pass returned PROCEED with
> no live defect of that class inside the four gate deliverables.**

**Two measurements changed a published answer during the sequence and survive in the result:** the
**half-open UTC-instant form is OUTCOME-DECIDING** (71 APPLY / 59 DERIV rows change outcome state, 36
never-started → Continued) and **`0068`'s strictness ruling is VACUOUS on this data** (0 pairs, 0
accounts, both populations, both arms).

**What both arms reproduce independently, per the approval §3:** the four outcome rows on both
populations · `p_at_bound` **1,246 / 1,230 / 1,072 / 1,056** with **all four emptiness cells 0** and
**FALSE 17,895 / 17,812 / 15,771 / 15,688** · **D2's 168 on APPLY and 153 on DERIV** · the position-3
drop set of **58,345** · channel overlap in all four units · **D3′ 99.53% → 97.73%** · the eight-arm
exclusion series and its started-and-left component · the boundary window and its flips · **D9 as a
bound, `[0, 75]`, `[0, 6]`, `[0, 27]`** · **2,874 ledger accounts** · **invariant 9's 20 and 17 rows
exactly at `τ_pull`.** **The 89-name column set is SET-EQUAL across the arms.**

**Why approval is defensible now, in the approval's own terms:** *"Every blocker from the sixth pass
onward was a claim about what a check establishes, or text about a surface the arm does not own —
never a number."* **Six of the eight residuals are corrections that need no arm; two are unruled spec
choices already disclosed by both arms.**

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

## The FIVE rules this block put into `CLAUDE.md`

*(This heading said THREE until 2026-08-17. `0095` and `0096` ruling 1 added two more, and **`0096`
ruling 2 withdrew part of `0095` §1** — rules 4 and 5 must be read together. Full text in
[[glossary-terms-and-thresholds]] §THE TWO ISOLATION RULINGS.)*

4. **A cross-arm characterisation never enters a launch instruction** (`0095`). **A launch instruction
   is a way for an arm to see the other arm's work, and it is worse than reading the folder, because
   the receiving arm is structurally forbidden from re-measuring what it was told.**
5. **A deliverable asserts only what its own arm measured** (`0096` r1) — **the provenance rule applied
   to STATEMENTS rather than FIGURES** — with **`decisions/` explicitly permitted to carry cross-arm
   content** (`0096` r2), because **a ruling has to cite its own evidence**, and because the isolation
   rule exists **to stop the arms copying each other's IMPLEMENTATION, not to keep a ruled number out
   of reach.**

### The first three

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

## What is still open AFTER the gate

> ***THE APPROVAL IS UNCONDITIONAL AND THESE ARE OPEN AND PUBLISHED. Approval was given IN VIEW of
> them, not around them.*** **None of them touches a filter position, a population, a waterfall line,
> an outcome count, an invariant result or a bound endpoint.**
>
> ***AND ONE OF THE EIGHT IS NOT AN OPEN ITEM AT ALL: residual 2, the `logs/` provenance cost, is
> ACCEPTED AS RECORDED.*** **Do not file it as awaiting a fix.** The Human Lead's reason: **build
> history and control results now live in `logs/`, which is git-ignored and on no propagation surface,
> so the public artifact set is no longer self-auditing on provenance** — *"the knowing price of `0096`
> §1"* — and *"a cost logged as a correction reads as a defect awaiting a fix, and this one is
> neither."* **One such log already over-claims its own coverage** (`surfaces_not_reached: []` while
> four were never scanned).

| Item | Whose |
| :--- | :--- |
| **Two files in `artifacts/` state four expired things** — the read-backs, stamped and allowlisted (`0097`), **invisible to every control** | Residual 1. **Closed by the stamp as far as it can be closed**; the *class* has no control |
| **Neither arm identifies the spec revision it validated against.** Arm a does not fingerprint `task-sheet.md` at all while asserting its 89-name conformance was read off it at run time — **that referent is unrecoverable** | Residual 3 |
| **Three cross-arm coverage divergences under identical labels** — distinct S2 episodes 2,135,938 / 2,023,274; D9 pivot show-IDs 46,366 / 45,014; per-site D11 at `A`/`A_H`. **All denominators** | Residual 4. **Resolvable only by reading each arm's mask** |
| **Six of nine invariants cannot fail on any data** — the gate rests on **two data checks and one cross-check with force** | Residual 5. **Both arms publish the 6 + 1 + 2 split and say so plainly** |
| **Two unruled spec choices, both disclosed** — set-membership denominators 6,065,704 / 6,065,610 and different D9 half-(b) grains | Residual 6 |
| **439 unread needle candidates**, deliberately neither failed nor narrowed | Residual 8. **Red Team's proposal, carried not ruled: scope the register per needle to the file set it was authored for and FAIL on that scope, reporting repo-wide without failing** — *"not narrowing, because the authored scope IS the original scope"* |
| **Whether `specs/` AND `CLAUDE.md` become propagation surfaces** | **Human Lead, unruled.** Red Team's position on `specs/`: adopt it. **`CLAUDE.md`'s absence is now measured rather than argued** — it is why the third missing-entry occurrence was invisible to the resolver |
| **The D9 tie-break.** `secondchance` (8) and `theisland` (7) are unique; **six keys tie at 6** and the arms publish different third places, both correct under their own rule. **`0088` §3 named `maigret`; neither arm picked it.** *A spec gap inside the ruling that closed a spec gap* | **Residual 7. Human Lead.** Red Team's position: publish all six and retire *"third-largest"*. ***AND THE SUPERSEDED NAMING IS STILL LIVE ON SURFACES 1, 4 AND 5*** — see K1 in [[open-items-and-contradictions]] |
| **The one-pair D9 divergence** — `435,642` against `435,643` on the S1-only class, the other two classes agreeing exactly | Reported, not reconciled |
| **`0090` §2's flagged reading** of *"this half"* — implemented as **every** D9 quantity with both forms | Both arms say so at the point of use; narrows if a single half was meant |
| **F7 — the falsifiability headline shape**, three-way against two-way over an identical nine-label set | Reported, not reconciled. **The dual diff cannot see it** |
| **`0091` §1's residual** — whether conjunct 2 was recomputed on the counterfactual outcome or held at the adopted one. **Arm a's `0094` build now states which, at each cell** (`step8-waterfall-a.json`, *"if conjunct 2 were held at the adopted outcome, 703 → 703 would be an IDENTITY and would establish nothing"*). **Arm b does not report the liveness count under the counterfactual, so there is no second arm to settle it** | Open |
| **`0068`'s D11-at-the-S1-walk.** Reading C moves line 1 to **220,103** — 4 pairs stop being completers, 0 completion dates move | `0068`'s own open item, **not** the set-membership denominator, which `0083` §1 closed |

**Related:** [[glossary-terms-and-thresholds]] · [[gate-step7-liveness]] ·
[[open-items-and-contradictions]] · [[withdrawn-claims-register]] · [[decision-log-step18]]
