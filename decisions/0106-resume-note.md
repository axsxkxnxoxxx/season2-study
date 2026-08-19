# Decision 0106 — RESUME NOTE. Stopped after the Step 8b v1.1.0 re-review.

| | |
| :--- | :--- |
| **Purpose** | ***A RESUME NOTE, not a ruling.*** Recorded by the Human Lead's instruction so the next session starts from state rather than from reconstruction. |
| **Stopped at** | `5a7341b` — `0105`, pushed to `main`. Working tree clean. |
| **Date** | 2026-08-18 |
| **Where the study is** | **All five gates APPROVED** — Step 1 (`0001`), Step 5 (`0021`), Step 6 (`0026`), Step 7 (`0064`), Step 8 (`0098`). **Step 8b has run twice**; schema **v1.1.0** is with `reviewer-engineering`, which returned **"yes, with named exceptions — eleven."** |
| **Next action** | ***RULE E2 FIRST.*** **E1 and E3 both depend on its answer.** |

---

## 1. What blocks what

| | blocks | needs |
| :--- | :--- | :--- |
| **E1** — `S17` requires `$.cross_arm_divergences`; `$.block_ownership` forbids Step 9 writing it. **The validator's only path to exit 0 is a cross-arm search an isolated arm is structurally forbidden to have performed** | **Step 9** | **the E2 ruling**, then validator + schema |
| **E2** — ***"diffed IN this schema" has no writer.*** `dual_status: dual` requires both `arms.a` and `arms.b`; **two isolated instances cannot jointly produce one document, and no merge owner is named** — nor could an arm be one under isolation | **Step 9** | ***HUMAN LEAD RULING: one file per arm, or a merged file with a named owner*** |
| **levels-vs-movements** — `0103` fixed `B`, the seed and the unit; **not the statistic**. The spec requires all three fixed identically | **Step 9** | **Human Lead ruling.** ***Independent of E1 and E2 — ruling it alone does not unblock Step 9*** |
| **E3** — **Step 13 is dual (`0103`) and only its HEADLINE is dual-capable.** Six other Step 13 outputs have one slot each, against `task-sheet.md:857`'s *"a schema with one slot per figure would force a reconciliation the spec forbids"* | **Step 13** | **the E2 ruling**, then schema. ***Cheap now, expensive after Step 13 runs*** |

***Three independent causes block Step 9.*** **Ruling any one alone does not unblock it.**

## 2. Not waiting on the Human Lead

**E4, E5 and E7 are agent-fixable and need no ruling.** `reviewer-engineering`'s own sizing: **E5 with E1
is "one afternoon in the validator"; E4 and E7 are "three lines each."**

- **E4** — `S22`'s advertised guard **does not cover `headline`**, so a Step 9 arm may write `bounds` and
  `ceilings_cannot_all_hold` as block absences **on the primary headline arm** and validate. Compounded:
  `is_primary_headline` is **not required**, so omitting it everywhere makes S22's primary-arm clause run
  **zero iterations while still reporting PASS** — the looked-nowhere shape **inside the control written
  against F1**.
- **E5** — **`EMPTY_DECLARED` is reachable with `coverage_count: 0`**, which the schema's own prose calls
  a finding. **A writer can reach the new terminal state dishonestly.**
- **E7** — `S22`'s liveness exemption is **one population too wide**: it exists for the **DERIV** series
  and as coded exempts **APPLY**, which `task-sheet.md:1008` mandates at every arm.

**Also carried, not blocking:** **E6** (`S24` is a **self-consistency** check — its registry is
writer-fillable — and **the schema has no CI slot a `W` percentile could occupy**), **E8** (mandated
deliverables now optional, incl. **Step 11's intervals swept in with Step 12/13's residue** and
`subpopulation_cuts` lacking the `search_record` `cross_arm_divergences` got), **E9** (`ratio_block`
stores **no operands**), **E10** (`$.block_ownership` is **a label, not a control**, closed at top level
and open where the risk is).

## 3. Two things worth carrying forward as method

***`reviewer-engineering` owned two of the eleven as its own doing, unprompted*** — F4 under-specified
(*"I asked for empty-versus-unsearched without asking who owns the search"* → E1, E5) and F1/F3
*"correct and incomplete: each absence branch is also a hole, and I did not say where the floor was"*
→ E4, E7, E8.

***And E11 was mine***: `0103`'s propagation reached **two of four sites** while `0104` reported it
corrected, so both `data-scientist` files held the correction and *"THE BOOTSTRAP IS UNSPECIFIED"* **ten
lines apart** — reaching **the right outcome for the wrong reason**. Fixed at `0105`.

## 4. State

- **Working tree clean. `5a7341b` pushed to `main`.** All three controls pass.
- **Nothing is running.** No agent, no rerun, **Step 9 not begun.**
- ***RESUME BY RULING E2.***

---

## APPENDED 2026-08-19 — the state at `aa4a996`, and what Step 9 is now waiting on

***THE PICTURE HAS CHANGED SINCE THIS NOTE WAS WRITTEN.*** **E1, E2, E3 are closed.** **Step 8b has run
six times and is at schema v1.5.0.** **Step 13b exists as a task-sheet step, owned by the Human Lead,
sitting AFTER Step 14.**

### Levels-vs-movements is Step 9's LAST blocker

**Everything else that blocked Step 9 has been ruled or fixed.** ***This one is untouched, and it is the
Human Lead's alone.***

`0103` fixed **`B` = 10,000**, **seed `20260818`**, **unit = account**. ***It did not fix the
STATISTIC***, and **both `data-scientist` files require all three fixed identically for both arms.**
**Step 7's arms diverged on it in fact, not in theory.**

### Arm B's justification is verbatim in `0116` §5 — NOT in `0115`

`artifacts/step7-liveness-bb-b.json`, at `/bootstrap`:

> *"nonparametric bootstrap, clusters = ACCOUNTS, unit = pair. Accounts resampled with replacement from
> the accounts present in the position-5 population; **the liveness rule is RE-APPLIED inside each
> replicate, so the exclusion count is itself random**."* — `replicates: 2000`, `seed: 20260814`

*(`0115` is arm `a`'s own record of Step 8b v1.5.0 and carries none of this.)*

### Arm A's justification is PENDING ITS OWN REPORT

***Arm A has no `bootstrap` block at that path in `artifacts/step7-liveness-bb-a.json`***, and every
occurrence of *"movement"* in its deliverables is about **share movements between rules, not the
bootstrap statistic.** **Arm A has been asked to report what it ran — reporting only, forbidden to
defend or rule, and forbidden to read arm B's output or any decision entry characterising the
divergence.** **Its answer is not in yet.**

### ***THE DECISION-LOG ACCOUNT OF ARM A IS UNRELIABLE ON THE SEED***

**`0052` §122 records `20260813`. `0053` §107 records `20260815`.** ***The record disagrees with
itself***, which is why arm A was asked for the seed **as it appears in its own artifact** rather than
as recorded. ***Do not take arm A's configuration from `decisions/` without checking it against arm A's
artifact.***

### Also live

- **`reviewer-engineering` has v1.5.0** and has been aimed at whether the **four-field arm key is stated
  IDENTICALLY everywhere**, after `0114`'s propagation left the three-field key standing on four
  surfaces — **twice now, a stale arm key has been invisible to `check_surfaces.py` because it is a
  STRUCTURAL CLAIM**, and both times an arm found it.
- **The adopted-rule revision is read by PARSING KEY NAMES** in `processed/step5/adopted_rule.json`. **A
  first-class field there would remove the inference; that file is Step 5's.**
- ***An arm wrote `decisions/0115`.*** **Retained — accurate, and records no ruling — but `decisions/` is
  a surface every arm reads, and an entry written by one arm and read by the other routes around the
  Human Lead's diff** (`0116` §2).

***RESUME BY RULING LEVELS-VS-MOVEMENTS, once arm A's report is in. Step 9 is not begun.***
