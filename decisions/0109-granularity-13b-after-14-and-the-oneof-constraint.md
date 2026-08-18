# Decision 0109 — granularity is §6; Step 13b moves after Step 14; the check-code / run-record reading

| | |
| :--- | :--- |
| **Decision** | ***GRANULARITY IS §6: ONE FILE PER STEP PER ARM.*** Step 9 writes two, Step 13 two, Steps 10–12 one each — **SEVEN inputs to the merge.** **`0107` §1 is AMENDED to match rather than left on the record.** ***STEP 13b MOVES AFTER STEP 14 and does NOT rerun.*** **`0082` and `0096` r1 govern different objects and do not conflict**: the check's **code** is committed to `src/`, its **run record** goes to `logs/`. **The `oneOf` constraint is recorded.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s M3, M4, M5, M9, M11 |
| **Amends** | `0107` §1; `task-sheet.md`'s Step 13b position and inputs |
| **Verified by** | **The M3 precondition was checked BEFORE propagating, as instructed** — see §2. `check_surfaces.py` |
| **Status** | Open. **Step 9 blocked by levels-vs-movements. M1, M2, M6, M7, M8, M10 go to the arm.** |

---

## 1. Granularity — §6, and the reason is the no-conversion-layer rule

***`0107` carried both readings and the schema rejected both.*** **§1 would require Step 10's output to
be DUPLICATED into two arm files — two copies of one figure, which is the defect class the
no-conversion-layer rule exists to prevent.** **§6 requires a single-arm step's file to have a legal
spine, which is a WIDENING** — ***and every finding in this sequence has been fixed by widening, because
widening keeps ONE DEFINITION PER FIGURE.***

**`0107` §1 is amended rather than left standing beside §6.** ***Leaving both on the record is the
defect this study has spent forty entries on***: a file holding two readings, each declaring the other
wrong, until a reader picks one.

## 2. M3 — verified before propagating, as instructed

***The Human Lead's instruction was to verify that Step 14 can write `limitations` from the arm files
and the diff WITHOUT a merged document, and to stop if it cannot.*** **It can.**

**Step 14 references `13b` and `merged` ZERO times.** It is **Human-Lead-owned**, *"Written before Step
15"*, and **its bias ledger is sourced from `decisions/` — `0028`, `0043`, `0034`, `0050`, `0052` — and
from Step 9's bounds**, which live in arm files. **Every figure it cites already exists.**

**So Step 13b moves after Step 14**, and **the reason it could not simply rerun is the sharper half**:
***two versions of one merged document is the stale-figure problem***, and at the old position the only
passing shape was **`limitations: []`** — **indistinguishable from *"there are no limitations"*, in the
block carrying the ten-item bias ledger that **must not be netted**, in the file Step 16 renders from.**
***That is a false statement to the reader, not a placeholder.***

## 3. M11 — two rules, two objects, no conflict

**`0082`: *"a check nobody can see is not a check."*** **`0096` r1: evidence about the tooling goes to
`logs/`, not `artifacts/`.**

***They govern different objects.*** **`0082` governs THE CHECK — satisfied by the code being visible in
`src/`, on a propagation surface, readable by any reviewer.** **`0096` governs THE REPORT OF HAVING RUN
IT.** **A selftest committed to `src/` with its output in `logs/` satisfies both**, and the reading is
recorded in `CLAUDE.md` so the two entries stop being read as opposed.

## 4. The constraint the reviewer named, recorded

***The `step_dual_status` rename fails loudly ONLY BECAUSE `by_producing_arm` is not inside a `oneOf`.***
**If an absence branch is ever added there** — which M9's unfixed `sole`-file spine made a plausible next
move — **a writer emitting the old `dual_status` key stops failing against `additionalProperties: false`
and instead produces a silent `matched 0 oneOf branches` at the parent.** ***The loud failure becomes an
invisible one.***

**Recorded in `CLAUDE.md` as a constraint on FUTURE EDITS**, not as a property of the current build,
**and it must be re-checked whenever an absence branch is added anywhere above a renamed key.**

## 5. To the arm, with M1 first

**M1 is the one finding that would corrupt a PUBLISHED FIGURE rather than block a step.** ***A merged
document assembled from ONE arm file currently validates and publishes that the arms agreed
everywhere*** — **a false clean**, and **it did not exist before v1.2.0.** **The split created it.**

**The reviewer's own discriminator is the one to build on**: **isolation is unobservable, but ARITY is
observable**, and **`ratio_block.convention_label` is already in the schema** — the two arms' conventions
are **named inputs that must not be reconciled**, so **two arms agreeing on that label have not been
merged from two arms.**

**Also to the arm: M2** (`step_dual_status` never checked against `producing_step`, so the forbidden
loosening is reachable by **relabelling** rather than widening), **M6** (`statistic` — the field the arms
actually differ on — has **no point-of-use restatement and no arm binding**), **M7**
(`coverage_count: 0` still passes), **M8**, **M10**.

## 6. Scope

- **Surfaces reached: `CLAUDE.md`, 1** (`task-sheet.md` — Step 13b moved and its inputs fixed), and
  **`decisions/0107`.** **The schema and validator are the arm's.**
- **Zero API calls. Step 9 NOT begun.**
