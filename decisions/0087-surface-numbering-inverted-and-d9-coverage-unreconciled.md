# Decision 0087 — the surface numbering was inverted in three entries; `0086` §1's reconciliation claim is false and is restricted

| | |
| :--- | :--- |
| **Decision** | **No new ruling. Two corrections to my own record, plus Red Team's fourth-pass findings carried.** **The propagation surface numbering is INVERTED in `0083`, `0085` and `0086`** — all three call the `analytics-engineer` pair *surfaces 2–3*, where `CLAUDE.md` numbers it **4–5**. **Corrected in place with a note in each.** **`0086` §1's *"every D9 count still reconciles across both arms"* is FALSE as written and is RESTRICTED** to the five ruled counts; **three coverage counts do not reconcile.** **B3 still blocks and is the Human Lead's**, now in a stronger form. |
| **Recorded by** | Analytics Engineer, on Red Team's fourth-pass HOLD |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's **fourth** Step 8 gate review: **HOLD**, three blocking, six publishing. **F3 and F2 are defects in this chain's own entries** |
| **Amends** | `0083` §4, `0085` §8, `0086` §2/§3/§6 (surface numbers); `0086` §1 (the reconciliation sentence and the U1 parenthetical) |
| **Verified by** | `check_surfaces.py` **PASS**; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **11/11 CONFIRMED** |
| **Status** | Open. **Step 8 is NOT approved. Three items block, all three the Human Lead's.** |

---

## 1. The surface numbering was inverted, in three consecutive entries

`CLAUDE.md` numbers the eight surfaces: **1** `task-sheet.md`, **2–3** the `data-scientist` pair, **4–5**
the `analytics-engineer` pair, **6** `artifacts/`, **7** `second-brain`, **8** `processed/`.

**`0083` §4, `0085` §8 and `0086` §2/§3/§6 all have 2–3 and 4–5 the wrong way round.** Red Team found it
in `0086`; **it was in the two entries before it as well**, which the review did not reach.

**The files edited were always the right ones.** Every propagation in this chain landed on
`.claude/agents/analytics-engineer{,-b}.md`, and the pair was verified byte-identical apart from `name:`
after each. **What was wrong is the numbers naming them.**

**Why that is not clerical.** Each entry's propagation record is what a re-verifier greps against. As
written, it **points at the two files that were not touched and exempts the two that were** — `0086` §6
literally reads *"Surfaces 4–5 … not applicable"* about the only two files it edited. **A re-verifier
either files a false failure against the `data-scientist` pair or accepts a clean grep on files that were
never in scope.** That is the look-nowhere shape, **in the entries written to fix propagation defects.**

**Corrected in place, with a note in each, as `0058` §6 did** — the decision log is tracked and public,
and a number that quietly changes is worth less than one that visibly did.

## 2. `0086` §1's reconciliation sentence is false as written

**Red Team was asked to test the claim, and it does not hold.**

**The FIVE RULED counts do reconcile**, and that is the whole of what was verified: strict **0**, loose
**75**, third key **76**, half (a) **0 and 6**, half (b) **0 and 27**. **The sentence generalised past
them.**

**THREE COVERAGE counts do not:**

1. **Arm A publishes two values for one labelled quantity, 27 lines apart in one section** —
   **46,428** at `step8-waterfall-a.md:323` and **46,366** at `:350`. The second comes from the **D9
   coverage pivot**, not the sweep, and is **mislabelled as the sweep**; its *"0 carry no slug"* clause is
   therefore computed on the wrong base.
2. **The two arms' "U1" are consequently two different sets, 62 IDs apart.** Arm B's map is keyed over
   the parsed sweep at **46,428**; arm A's is show IDs appearing in a coverage row at **46,366**.
   **Naming "U1" does not identify the object**, so **the axis `0086` §1 claims to have located is
   located only to the first digit** — the divergence is one level narrower than that section says.
3. **The user-show coverage rows are unreconciled — 747,478 (A) against 726,103 (B)** (the latter as
   435,643 + 8,834 + 281,626). **Neither arm mentions the other's quantity, and no entry lists it.**

**Why these are not bookkeeping. D9's ruled result is 0 and 0.** The coverage counts are **the only thing
separating that from "looked nowhere"** — which is the rule this study wrote after three controls
reported clean while checking zero rows. **Three of those counts are wrong, mislabelled, or
unreconciled.**

**And my own parenthetical compounded it.** `0086` §1 recorded *"U1 — 46,366 arm A / 46,428 arm B"* as
though it were one universe with an incidental arm difference. **Both numbers are recoverable from arm A
alone.** It was never the arm-against-arm comparison it read as.

**RESTRICTED, not deleted.** The sentence now states the five it checked and lists the three it did not.

## 3. B3 — still blocking, and Red Team's fourth pass makes it stronger

**`0085` §7 carried B3 as "no assertion." The fourth pass establishes something worse: there is no
MEASUREMENT either.**

- **The half-open form.** Red Team independently confirmed both arms' self-report — no `.date()`,
  `dt.date`, `normalize()` or day-flooring anywhere in `step8_*.py`; instants are int64 seconds
  throughout. **The claim is true.** **But neither arm reports how many rows the two forms could differ
  on** — no count of S2 records in `[τ1 − 24h, τ1)`, none exactly at `τ1`, none at the `τ2` boundary.
  **So a reader cannot tell whether the mandate is load-bearing on this data or vacuous.**
- **D11.** Arm A states in prose that D11 is applied at **five sites** and gives **a count at none of
  them.** Its one real assertion —
  `assert int((r["tau2"][pos5] > lib.TAU_PULL).sum()) == 0` at `src/step8_a_3_table.py:98` — covers
  **D11's inertness on the outcome windows only**, and sits **outside the published invariant set.**
  **Arm A's own "promotion rather than new work" is accurate for one site of six.**

**Three ways offered to close it**, and the choice is a ruling: emit the boundary-window count and label
the invariant **vacuous** if it is 0 rather than passing silently; emit a **per-site D11 table** asserted
at each site; and **promote `step8_a_3_table.py:98` into the published set** with a CODE CHECK label.

**Red Team's ground for blocking:** *"the unstated version of exactly this scope is what produced Step
7's 792-against-791."*

## 4. F4 — the coverage apparatus mostly cannot fail. CARRIED, and one sentence must go either way

**`0080` §3 built the coverage identities because a gap hid 99 rows. Red Team's finding is that the
apparatus mostly cannot detect that gap.**

**8 of arm A's 13 identities are `cover(unit, pop, N, N)`** — `not_asserted = N − N = 0`, and `n_pop` and
`n_asserted` are **the same expression**, so **the identity cannot detect an invariant asserted on a
population other than the one named.** Only invariant 1's four partitions and invariant 6 are real
arithmetic — **5 of 13**. **The helper's own docstring names the failure mode** and it is then called
without `parts` at invariants 2, 3, 4, 5, 7 and 8.

**Two hardcoded literals published as results:**
`"coverage_identity_holds_on_every_stated_population": True` (`step8_a_5_diagnostics.py:774`) and
`"classification_covers_every_account": True` (`:949`). **Arm B is worse in one respect** —
`identity_holds: True` hardcoded at invariants 2, 4 and 7, and an aggregate chaining
`.get(..., .get(..., .get(..., True)))`, so **an invariant with no coverage key contributes a pass**, with
no coverage count printed. **Arm A does print one and asserts on it, which is the correct shape.**

**The dual diff cannot see any of this: both arms did it.**

***One sentence must be struck whatever is ruled***, because it is a control asserted to exist:

> ~~*"The run asserts this, so a report that omitted a population could not be written by this
> pipeline."*~~

**Credit where Red Team gave it:** both arms label 5-of-8 and 6-of-8 unfalsifiable **prominently**, and
both data checks report what they saw. **The labels are right. The coverage apparatus is what
overstates.**

## 5. F5–F9 — carried as limitations

| # | Finding | Note |
| :-- | :--- | :--- |
| **F5** | **`specs/step8-readback.md:3` still says Step 8 *"has not launched."*** `0086` §3 stamped the two artifacts **generated from this file** and missed the source. **Third occurrence of the string.** Structural half: **`specs/` is not one of the eight surfaces**, so nothing checks it | **Stamp it, and either add `specs/` as a surface or record why not** |
| **F6** | **Arm A's column check is weaker than its prose.** It says it asserts set equality *"against the spec's list"*; the code asserts against a **hand transcription** at `step8_a_3_table.py:61-84` and **never opens `task-sheet.md`.** Arm B does read the enumeration off disk | **Only the dual diff protects arm A — and the dual diff cannot catch a propagation failure** |
| **F7** | **Build-tag convention unstated**; free text, and the Human Lead's diff cannot key on it. Arm A's git HEAD is recorded `b860956, worktree dirty: True` — **the commit does not identify the code** | **Fix a format before Step 13 runs eight arms on both populations** |
| **F8** | **The arms assert invariant 3 over different record sets** — 6,065,704 (A) against 6,065,610 (B), because each publishes a different D11 reading. `0083` §1 closed that as a **coverage-figure** family; **this is the coverage of an ASSERTED INVARIANT differing across arms, which is a different object**, and neither arm says so at the invariant | **`0083` §1's closure does not reach this** |
| **F9** | **Three corrupt year-1 S1 completion dates**, arm A only, direction unstated. Probably inert — the `max()` makes `T0` the S2 finale — **but "probably" is not measured** | Also carried at `0084`-era P1 |

## 6. On the remit Red Team was given

**Filter order — no objection, fourth review running.** Both arms apply 1→7 as mandated; contamination
before censoring before liveness; **DERIV's position 4 is a materially different filter from APPLY's and
both arms say so.** Stated plainly: **positions 1, 2, 3 and 7 remove zero, so on this data the order
constrains exactly one real decision — 4→5→6**, and both arms label the inertness with reasons.

**Invariant labels — no objection.** Eight assertions, correctly labelled, **both DATA CHECKS real and
both reporting what they found.** The objection is F1 and F4, not the labels.

## 7. What blocks, and it is all the Human Lead's

1. **B3** — a ruling, plus either the boundary-window and per-site D11 measurements or B3 published as a
   named residual **with the measurement gap stated.** Not the current position, where the mandate is
   claimed satisfied and nothing measures it.
2. **F2** — arm A's `distinct_show_ids_in_the_sweep` label corrected, the two U1s named as two objects,
   and 747,478 against 726,103 reported or reconciled. **`0086` §1's sentence is already restricted here.**
3. **F3** — **done in this entry**, and wider than the review found.

## 8. Scope

- **No rule change, no population change, no figure moves.** No `CLAUDE.md` dependency list is touched.
- **Surfaces reached: NONE.** This entry corrects `decisions/` only. **`decisions/` is not one of the
  eight surfaces**, which is worth stating rather than leaving implicit — **the corrections in §1 and §2
  are to the RECORD, and no agent-read file carried either defect.**
- **Zero API calls.**
- **No rerun launched.** F2's arm-side corrections and B3 both need rulings first, and rerunning
  before them would produce a fifth build against an unchanged spec.
