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

### ~~***THE DECISION-LOG ACCOUNT OF ARM A IS UNRELIABLE ON THE SEED***~~

> ***WITHDRAWN 2026-08-18, §7 below. THE PREMISE IS FALSE.*** **`0053` §107 does not record `20260815`
> as arm A's seed — it records the PAIR `(20260813, 20260815)` for the `mm` run, and both halves are
> correct on disk.** The two entries describe **two different runs**, not one run twice. **What was
> missing was the run label, not the agreement.**

~~**`0052` §122 records `20260813`. `0053` §107 records `20260815`.**~~ ***The record disagrees with
itself***, which is why arm A was asked for the seed **as it appears in its own artifact** rather than
as recorded. ***Do not take arm A's configuration from `decisions/` without checking it against arm A's
artifact.*** *(The closing instruction stands and was vindicated; the contradiction that motivated it
did not exist.)*

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

~~***RESUME BY RULING LEVELS-VS-MOVEMENTS, once arm A's report is in. Step 9 is not begun.***~~
***ARM A'S REPORT IS IN. See §7 — the ruling's premise has changed. Step 9 is not begun.***

---

## 7. Appended 2026-08-18 — arm A's report, read off disk rather than off the log

***EVERY CLAIM IN THIS SECTION WAS VERIFIED AGAINST THE FILE AND THE LINE, POST-COMPACTION, ON THE
HUMAN LEAD'S INSTRUCTION NOT TO WRITE IT FROM A SUMMARY.*** Two claims I had carried into this session
**did not survive that check and are withdrawn below.**

### 7.1 Arm A does not run "movements." It runs BOTH, and says so in its own file

| Where | What it says |
| :--- | :--- |
| `artifacts/step7-liveness-mm-a.json:1018` | `"reports": "LEVELS and PAIRED MOVEMENTS, both, explicitly labelled"` |
| `artifacts/step7-liveness-mm-a.md:436` | *"`0052` §6 records that the two arms used different designs last time and were not diffable. **This one is stated in full and both objects are reported.**"* |
| `artifacts/step7-liveness-mm-a.md:437` | `\| **Reported** \| **LEVELS *and* PAIRED MOVEMENTS, both, labelled.** Neither is presented as *the* design \|` |
| `artifacts/step7-liveness-mm-a.md:448–449` | *"On APPLY the never-started level is 1.09 pp wide while its movement is 0.098 pp wide — **a factor of 11, which is why the choice matters and why both are printed.**"* |

**And it is not only the `mm` run.** `processed/step7/bb_a/bootstrap.json` — the **gate-closing**
ALT-BROAD run — carries `by_population.<pop>.settings` (**the levels**) **and**
`by_population.<pop>.paired_delta_rule_minus_no_filter` (**the movements**, with
`paired_clustered_95_ci_pp` and `ci_excludes_zero`) **side by side.** ***Arm A has never published
movements alone.***

### 7.2 `decisions/` carries "A: movements, B: levels" at three sites, and it is wrong on BOTH halves for arm A

| Site | Text |
| :--- | :--- |
| `decisions/0052-liveness-rule-alt-matched-adopted.md:122` | *"A used B = 4,000, seed 20260813, on the **movements**; B used 2,000, seed 20260814, on the **levels**"* |
| `decisions/0055-deriv-floor-widened-and-the-grep-control.md:288` | *"A at 4,000 / 20260813 / movements, B at 2,000 / 20260814 / levels"* |
| `decisions/0056-derived-figures-and-the-dependency-list.md:150` | *"A at 4,000 / 20260813 / movements, B at 2,000 / 20260814 / levels"* |

**Wrong on both halves for arm A: not "movements" (it is both), and not "instead of levels" (it prints
the levels first).** **Propagated onward to `task-sheet.md:960`,
`.claude/agents/data-scientist.md:222`, `.claude/agents/data-scientist-b.md:222` and
`.claude/agent-memory/second-brain/gate-step7-liveness.md:498`** — **seven surfaces carrying a
characterisation of an arm that the arm's own artifact contradicts.** ~~***Not corrected here: this
is the object of the pending ruling, and correcting it is the ruling.***~~ ***RULED AND CORRECTED
2026-08-19 (`0118`): all seven sites CORRECTED, not marked — it was wrong when written, not
superseded later.*** **The statistic is fixed as BOTH levels and paired movements, both arms.**

### 7.3 ***WITHDRAWN — the seed contradiction does not exist, and neither does my "appears once"***

**I reported before compaction that `20260815` *"appears exactly once in the repository, in arm B's
source file."* THAT IS FALSE.** It appears **8 times**:

| File | Line | Whose |
| :--- | :--- | :--- |
| `artifacts/step7-liveness-mm-b.json` | `:1286` | **arm B artifact** |
| `artifacts/step7-liveness-mm-b.md` | `:143`, `:481` | **arm B artifact** |
| `src/step7_mm_b_5_bootstrap.py` | `:14`, `:41` | **arm B source** |
| `decisions/0053`, `0106`, `0116` | — | the log |

**The load-bearing half survives: ZERO namespace-`a` files carry it.** `20260813` is arm A's seed in
every namespace-`a` artifact and source — `step7-liveness-mm-a.json:1014`,
`processed/step7/bb_a/bootstrap.json`, `step7-liveness-bb-a.md:220`, `step7-liveness-alt-a.json:520`,
`step7-alt-rule-a.json:1397`, `step7-liveness-a4.json:418`.

***AND `0053` §107 IS NOT A MISATTRIBUTION.*** `git log -S 20260815` puts its first appearance at
**`fafb443`, the same commit that created `step7-liveness-mm-b.json` and `0053` itself.** So §107's
*"Both B = 4,000 … seeds stated (20260813 and 20260815)"* describes the **`mm` (ALT-MATCHED) run**,
where `mm-a` is `4000 / 20260813` and `mm-b` is `4000 / 20260815` — **both halves correct on disk.**
`0052`/`0055`/`0056` describe the **`bb` (ALT-BROAD, gate-closing) run**, where `bb-b` is
`2000 / 20260814` (`step7-liveness-bb-b.json:338`) — **also correct.**

> ***The two entries were never in conflict. They label two different runs and neither says which.***
> **The real defect is an unlabelled run**, and it produced a fabricated contradiction that stood in
> this note and in `0116` §5 until the files were read. *(`0053` is separately **withdrawn in its
> entirety** by `0054`, which no reader of §107 was told.)*

**This is the third blindness class**, `CLAUDE.md`: **a withdrawn ARGUMENT built from correct
statistics.** `20260813`, `20260814` and `20260815` are each correct where they appear; **the wrong
thing was the use of them.** **Registered as grounds-withdrawn, not as a superseded figure** — there
is no wrong number for `check_surfaces.py` to match.

### 7.4 Arm A's two self-reported gaps — both confirmed

**(a) The gate-closing deliverable has no bootstrap block at all.**
`artifacts/step7-liveness-bb-a.json` has **23 top-level keys and `bootstrap` is not among them**;
`grep -c seed` on that file returns **0**. The settings exist — `processed/step7/bb_a/bootstrap.json`
carries `B: 4000, seed: 20260813, unit: account, resample, caveat` — **so this is an EMITTER gap, not
a design gap**, and it is why `0116` §5 concluded arm A had no statistic on record. *(The `.md` half
states it once, at `step7-liveness-bb-a.md:220`; the `.json` half states it nowhere — **one object,
two renderings, and only one carries it**, which is the `CLAUDE.md` "one definition per figure" shape.)*

**(b) `B` is not uniform across namespace-`a`, and arm A's own claim of uniformity is half false.**
`step7-liveness-mm-a.md:439` reads *"the same seed and **B** as every prior namespace-`a` Step 7 run."*
**True of the seed. False of `B`:** `artifacts/step7-liveness-a4.json:417` carries
`ACCOUNT_CLUSTERED_BOOTSTRAP.replicates: 2000` against `4000` at `mm-a` and `bb_a`. **Arm A found this
in its own deliverable and reported it.**

### 7.5 Carried, agent-side, unchanged: `read_not_typed` is an unchecked `const: true`

`artifacts/step8b-output-schema.json:529` declares `"read_not_typed": {"const": true}`;
`src/step8b_validate.py:2759` asserts only `reg.get("read_not_typed") is not True`. **Both check that
the writer DECLARED it, never that it happened** — the agent files say so in as many words at
`.claude/agents/data-scientist.md:121` and `-b.md:121`. `0117` §F3 names it as
**`diff_precedes_merge` reintroduced one version after its retirement.** **Unlike that one, the
checkable fact is on disk and the reader already exists** — `source_file`, `source_key` and
`source_sha256_12` are all required fields, so the validator can open the file and compare instead of
believing. ***Not fixed here; no ruling is required for it and none has been asked for.***

### 7.6 State at the time of writing

**`HEAD` = `1499257`** (`0117`: E8 and E14 reached zero of surfaces 2 and 3), branch `main`, **working
tree clean before this note. Nothing is running** — no agent, no background job, zero API calls this
session.

### 7.7 ***What the pending ruling is now actually about***

**It is no longer "adopt arm A's statistic or arm B's."** Arm A prints both and labels them; **the
spec's requirement is that the statistic be *fixed identically for both arms*, and "both, labelled" is
a candidate answer to that, not a third position.** ***The Human Lead's ruling is whether "both,
explicitly labelled" satisfies `0056` §159's "must be fixed identically for both arms in the spec
before Step 9 runs" — and if it does, whether the three sites in §7.2 are corrected or marked.***

> ***ANSWERED 2026-08-19 (`0118`): IT DOES.*** **The statistic is fixed as BOTH levels and paired
> movements, both arms, both labelled, neither presented as the design.** **All three bootstrap
> elements are now fixed and identical, and Step 9 is no longer blocked on the bootstrap.**

***STEP 9 IS NOT BEGUN. NOTHING ELSE STARTED.***
