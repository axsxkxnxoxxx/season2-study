# Decision 0107 — E2: one file per arm. The merge is a separate step, owned by the Human Lead.

| | |
| :--- | :--- |
| **Decision** | ***ONE FILE PER STEP PER ARM.*** ~~One file per arm; each arm writes its own document~~ ***— AMENDED by `0109` (M4/M5/M9) to §6's reading, which this entry also carried in §6 and which now governs: Step 9 writes TWO files, Step 13 TWO, Steps 10–12 ONE each, SEVEN inputs to the merge. §1's reading would require Step 10's output DUPLICATED into two arm files — two copies of one figure — and the schema rejected both readings until this was settled.*** **NO ARM WRITES INTO A DOCUMENT ANOTHER ARM WRITES INTO.** **The merged reader-facing document is produced by a separate named step — STEP 13b, owner Human Lead — after both arms have landed and been diffed.** ***The reason: arm isolation is the MECHANISM, not a side effect.*** **E3 is CLOSED BY THIS RULING rather than fixed separately. E1 is NOT moot and still needs its validator fix.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s E2 — ***"diffed IN this schema" has no writer*** |
| **Amends** | `0066` §5; the `analytics-engineer` pair; **creates `task-sheet.md` Step 13b** |
| **Status** | Open. **Step 8b reruns for the schema and validator halves. Step 9 remains blocked by E1 and levels-vs-movements.** |

---

## 1. The ruling, and why it is structural

**A merged file needs a writer that reads both arms**, and ***no arm can be that writer without
defeating what dual implementation exists to do.*** **Two instances that never see each other's work
cannot jointly produce one document** — so the schema's *"a dual step is diffed IN this schema"*
**silently answered a question it had no answer to.**

***It is the DIFF, not the merge, that is the dual control***, and the diff happens **between two files,
by the Human Lead, before the merge.**

## 2. Three claims checked before propagating — one was wrong

***The Human Lead asked for verification rather than action, and it changed the outcome on one of
three.***

**(1) E1 is NOT moot.** The ownership half is right — `cross_arm_divergences` is `human_lead`,
`may_first_writer_fill: false`, `forbidden_to_compute_here: [step9, step13]`, so it belongs to the merged
document. ***But `S17` fails any file that omits it*** (`src/step8b_validate.py:846`). **So an arm file
that correctly omits the block still fails**, and the ruling leaves the arm **forbidden to write it and
forbidden to omit it.** **E1 shrinks from a design contradiction to a validator fix; it does not
disappear.**

**(2) E3 IS moot, with one schema change.** **One slot per figure forces no reconciliation in a single
arm's file, because there is no second arm's figure in it** — `task-sheet.md:857` is satisfied by
construction. ***But the schema currently forbids the file this ruling requires***: `by_producing_arm`'s
`if/then/else` makes `dual_status: "dual"` require **both** `arms.a` and `arms.b` and forbid `sole`, so
**a dual step's per-arm file has no legal shape.**

**(3) Nothing downstream breaks.** **Step 16's brief names no combined file**; the validator is
single-file by construction. ***The one thing that breaks is the retired sentence itself.***

## 3. E3 is closed BY this ruling, not fixed separately

***Because the reconciliation `task-sheet.md:857` forbids can only occur where two arms' figures meet,
and under one-file-per-arm they never meet until Step 13b.*** **Step 13's six single-slot outputs —
the per-arm liveness series, `d3_prime`, `retained_by_air_period`, `action_type_counts`, the variant
blocks, `tested_ranges` — hold one arm's figure each in that arm's own file, which is correct.**

***Recorded as closed-by rather than fixed, because the distinction is load-bearing***: a later reader
finding E3 in the review and no separate fix would otherwise conclude it was dropped.

## 4. What the schema and validator must now do — the arm's work, not this entry's

- **`S17` skips `cross_arm_divergences` where the file's producing step is not the Human Lead.** **An
  arm file that correctly omits the block must PASS.**
- ***`dual_status` splits into TWO FACTS***: **whether the STEP is dual**, and **whether THIS FILE holds
  one arm or both.** **A dual step's single-arm file must have a legal shape that NAMES WHICH ARM it
  holds.** ***Explicitly NOT by loosening the `single_arm` branch*** — that would let a single-arm
  step's file claim two arms.
- **Retire the `$defs` sentence and its generator source.**

## 5. The claim was on FIVE assertive surfaces, not two

**The Human Lead named `0066` §5 and the `$defs` site. A grep before editing found five**, plus three
places that quote it to refute it and are legitimate.

| | |
| :--- | :--- |
| `.claude/agents/analytics-engineer{,-b}.md:542` | **retired here** |
| `decisions/0066` §5 | **retired here** |
| `artifacts/step8b-output-schema.json:1958` | **arm-owned — retired on the rerun** |
| `src/step8b_schema.py:653` | **arm-owned — the generator behind the artifact** |

***This is why the instruction to grep before finishing was the right one***: `0103`'s correction reached
two of four sites, and this claim was on **more surfaces than the ruling named.**

## 6. Step 13b

**Between Step 13 and Step 14 — it has nothing to merge until every writing step lands.** **Owner: Human
Lead. Chained. Engineering review. NOT a gate** — `CLAUDE.md` fixes the list at five and all five are
approved.

**Inputs: SEVEN FILES, one per step per arm** (`0109`) — Step 9 ×2, Step 13 ×2, and one each from Steps 10, 11 and 12, **with the
dual pairs already diffed.** **Emits one merged document against the same schema**, both arms under
`arms.{a,b}`, **plus the two blocks only it may fill** — `cross_arm_divergences` with a **real** search
record, and `limitations`. **Step 16 renders from the merged document.**

## 7. Still open, untouched by this ruling

***LEVELS-VS-MOVEMENTS.*** `0103` fixed `B` = 10,000, the seed and the account unit; **not the
statistic**, and the spec requires all three fixed identically. **Step 7's arms diverged on it — A:
movements, B: levels — so the divergence is real, not hypothetical.** **Two things attach when it is
ruled**: a check asserting both arms' `statistic` agree, as `S23` does for the inline restatement, **or
the fix is recorded and unpoliced**; and the schema's record of it as **varying per arm**, correct today
and wrong the moment it is fixed.

**Step 9 remains blocked by E1 and levels-vs-movements. Step 9 is NOT begun.**
