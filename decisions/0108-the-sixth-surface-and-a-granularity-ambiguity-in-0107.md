# Decision 0108 — Step 8b v1.2.0; the sixth assertive surface; and an ambiguity in `0107` that is mine

| | |
| :--- | :--- |
| **Decision** | **No new ruling. Step 8b v1.2.0 implements `0107` and closes E1, E2 and E3's schema half.** ***Arm `a` found a SIXTH assertive surface for the retired claim — `task-sheet.md:857`, this step's own spec bullet — and correctly declined to edit it.*** **Retired here.** ***And it found that `0107` §1 and §6 read differently on file granularity. That ambiguity is mine and is carried for the Human Lead.*** |
| **Recorded by** | Analytics Engineer, on arm `a`'s Step 8b rerun |
| **Date** | 2026-08-18 |
| **Verified by** | Both document shapes validate at **exit 0**; **41 mutation cases all have force**; `check_surfaces.py` **exit 0** |
| **Status** | Open. **Step 9 blocked by levels-vs-movements. E1 closed. E2, E3 closed.** |

---

## 1. The sixth surface

**`0107` §5 found FIVE assertive sites and noted the ruling had named four.** ***There were six.***
`task-sheet.md:857` — *"The two arms of a dual step write the same schema and are diffed in it"* —
**is Step 8b's own spec bullet.**

***The arm found it and did not edit it***, on the ground that **propagating a ruling into its own spec
is not an arm's to do.** **That is the correct call**, and it is the second time in this sequence that
grepping past the named sites found more of them.

**Retired here, first clause only.** **The second clause — one slot per figure forces a reconciliation
the spec forbids — stands, scoped to the MERGED document**, which is exactly `0107` §3's reasoning.

## 2. An ambiguity in `0107`, and it is mine

***`0107` §1 says "each ARM writes its own document." `0107` §6 lists inputs as "Step 9 ×2, Step 13 ×2,
and the single-arm files from Steps 10–12" — which reads as one file per STEP per arm.*** **Both satisfy
the ruling's reason**, since neither lets an arm write into another arm's document. **The reason does not
disambiguate, and I wrote both.**

**The arm took §1's literal reading** — arm a's Step 9 and Step 13 payloads share arm a's one file — with
`document_scope.producing_step` naming the step that owns the `$.arms` spine and `also_written_by_steps`
naming the rest, **plus a check that no Human Lead step may appear in an arm file's writer list.**
**Recorded in `$.spec_choices_made_by_step_8b` with what changes under the other reading**, and it notes
**the validator's predicate does not move either way.**

***This bears directly on Step 13b's input contract and is carried for the Human Lead.***

## 3. What v1.2.0 does, verified rather than asserted

**Two document kinds against one definition**, with **`$.document_scope` as the first thing a reader
consults**: an **arm file** that names its arm, and the **Step 13b merged document** holding both arms
and the two blocks only the merge may fill.

**E1.** **The arm verified the contradiction on the pre-change build before touching it** — with
`cross_arm_divergences` removed, schema validation passed and **S17 alone failed**, so the only exit-0
path was a fabricated search. **Now S17's predicate is *the file's producing step is a Human Lead
step***. **An arm file omitting the block reports N/A with the reason; an arm file CARRYING it still
FAILS** — ***skipping the requirement is not permitting the fabrication***, and both halves are
exercised in the selftest.

**E2/E3.** **The arm verified the old shape was illegal**: stripping `arms.b` from every dual block
produced **8 schema errors**, confirming a dual step's single-arm file had no legal shape.
**`step_dual_status`** (about the STEP) and **`arms_in_this_file`** (about THIS FILE) are now separate,
with **`arm_held` required when `one_arm`.**

***And the `single_arm` branch was NARROWED, not loosened***, as the ruling required: it forces
`one_arm` + `arm_held: "sole"` + exactly `arms.sole`, and the selftest case
`single_arm_step_claims_two_arms` **fails as required.**

***One judgement worth keeping:*** the arm **renamed** `dual_status` rather than redefining it, **so a
writer still emitting the old key fails loudly against `additionalProperties: false` rather than
silently acquiring a new meaning.** **That is the stale-figure problem solved at the key level.**

## 4. Carried

- ***The `0107` §1 vs §6 granularity ambiguity*** (§2) — **the Human Lead's.**
- **A single-arm step's own file is expressible but not illustrated**: `$.arms` is a required spine and
  Steps 10–12 produce no `W` arms, **so what their file's spine holds is unfixed.**
- ***LEVELS-VS-MOVEMENTS***, untouched, still recorded as varying per arm. **Step 9's remaining blocker.**
- **A structural limit the arm records in the file**: the schema can forbid an arm file the merge-only
  blocks, **but isolation is a property of how an instance was RUN, not of its output.** ***The diff
  remains the control.***

## 5. Scope

- **Surfaces reached: 1** (`task-sheet.md:857`) and **6** (both artifacts, plus a new arm-file
  placeholder). **Zero API calls. Step 9 NOT begun.**
