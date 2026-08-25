# Decision 0127 — movement endpoints reach the spec surfaces; and the hard consts stay, with their cost recorded

| | |
| :--- | :--- |
| **Decision** | **Two rulings.** ***(1) THE MOVEMENT-ENDPOINT FACT REACHES THE SPEC SURFACES.*** **A writer of Steps 9–13 needs to know movement endpoints are percentage-point differences that can go negative, and no spec surface said so** — the schema said it, ***and an artifact is not a spec surface.*** ***(2) THE `const` VERSION IDENTIFIERS STAY HARD***, and the migration cost is **recorded as accepted, not discovered later.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-25 |
| **Occasioned by** | `0126`'s v1.10.0 rerun, and the arm's routing of both items to the Human Lead |
| **Status** | **FILED and PROPAGATED.** |

---

## 1. ***The fact existed only where a writer does not read***

`0126` typed a CI endpoint by its statistic: **movements on `$defs.pp`, which permits negatives; levels on `$defs.percent`, unchanged at `minimum: 0`.**

***AND THAT IS HOW THE DEFECT REACHED PUBLICATION.*** **An arm computed six negative paired movements, could not write them, published nine of eighteen intervals** — excluded by sign — **and said so.** **No spec surface told it a movement endpoint was a different quantity from a level endpoint**, because **the only place the distinction lived was the schema**, and ***a writer reads its own definition file and `task-sheet.md`, not the schema's `$defs`.***

> ***THE FACT EXISTED ONLY WHERE A WRITER DOES NOT READ.***

**The producing arm named this itself:** *"a writer of Steps 9–13 needs to know that movement endpoints are percentage-point differences, and no spec surface says so today. The schema states it, but an artifact is not a spec surface."*

**So it is written on surfaces 1–5 and 7**, in the words a writer meets before it computes anything:

> **A LEVEL endpoint is a PERCENTAGE — `[0, 100]`, and a negative one is not a possible measurement.**
> **A MOVEMENT endpoint is a PERCENTAGE-POINT DIFFERENCE — it can be zero and it can be NEGATIVE**, and
> a movement is negative wherever the filter lowers the share.
> ***NEVER DROP AN INTERVAL BECAUSE ITS SIGN WILL NOT FIT. That is cherry-picking by sign, and it is
> what happened before this was written down.***

**And `E2` is struck at `second-brain/open-items-and-contradictions.md`** — it read *"to close before the next version bump"* and **it is closed**, by `S44`.

## 2. ***The hard consts stay. The cost is the ruling, not a side effect.***

`$.schema_version` and `$.schema_id` are `const`. ***Every version bump invalidates every previously-written instance*** — v1.10.0 put both Step 9 arm files at exit 1 on two errors each, **with zero substantive failures.**

***A COMPATIBLE-VERSION TOLERANCE IS REFUSED.***

> **It would let an instance written against a DIFFERENT SHAPE validate silently, which is worse than a
> migration.** ***A loud migration is a cost. A silent shape mismatch is a defect that cannot fail.***

**This study has spent four rulings on checks that could not fail** — the vacuous preconditions, the
zero-coverage guard, the anchor that could not pass, the range window that passes on a vector wrong in
every entry. ***Buying convenience with a check that cannot fire would be the fifth, and it would be
bought deliberately.***

### ***THE COST, RECORDED SO IT IS NOT DISCOVERED AT STEP 13***

- ***EVERY BUMP INVALIDATES EVERY PRIOR INSTANCE.*** Not the changed part — **every instance, on both
  identifiers, whatever the change was.**
- ***THE COST SCALES WITH THE NUMBER OF INSTANCES, NOT THE SIZE OF THE CHANGE.*** A one-field addition
  and a total redesign cost **exactly the same per file.**
- ***STEP 13 WRITES FAR MORE FILES THAN STEP 9.*** It is **dual and varies `W` across eight arms**, and
  it varies the completion rule alongside (`0103`). **Step 9 cost two migrations. Step 13's grid will
  cost many more, and the arithmetic is the same arithmetic.**

***THIS IS A KNOWN COST ACCEPTED DELIBERATELY, NOT AN OVERSIGHT TO BE DISCOVERED AT STEP 13.*** **Anyone
proposing a schema change after Step 13 has written should price the migration BEFORE proposing it, and
should not read a large migration as evidence that the consts were the wrong design.**

**One mitigation is already in force and is not a tolerance:** the producing arm made `type_fixture_rule`
**placeholder-only rather than global**, so v1.10.0 cost each Step 9 file **two errors and not three** —
*"the migration is exactly what the bump itself costs."* ***Keep new requirements off the instance where
they can live on the placeholder.***

## 3. The migration ran. Both Step 9 files validate at exit 0.

**Each arm migrated its own; neither read the other's.** ***Nothing measured moved, verified by class
rather than in aggregate:*** **arm `a` — 869 numeric leaves before and after, 0 moved; 54 CI endpoints,
0 moved; 378 bound-path numerics, 0 moved.** **Arm `b` — 738 numeric leaves compared, 0 moved outside
the emission's own run record.** Both validators **exit 0, 45 checks, 0 failed**.

**Neither re-ran its bootstrap.** Arm `a` showed why it did not need to — `measured.json` still hashes
to what the committed artifact recorded as its input — and re-ran its weights selftest at **72/72
bit-exact** with both negative controls returning **0 of 72**. **Arm `b`'s ordering guard did not fire
and was shown non-vacuous**: 37 marked cells on disk against 37 the comparison produces now, 658 table
cells, and `src/step7_register.py` regenerated **byte-identical** — the migration moved no registered
value.

***THE STAMPED ORIGINALS STAY AT v1.9.0, DELIBERATELY.*** **They are the superseded record of what the
defective vector produced, and migrating them would restate a version they were not written against.**
Byte-identical to `3e8653e`, verified.

**One class of leaf moved that is not a version identifier, and the arm flagged it rather than burying
it:** three strings — `$.sentinels.rule`, `$.sentinels.type_fixture_rule` and
`$.notes.a_ci_endpoints_type_follows_its_statistic` — **inherited wholesale from the placeholder**, each
verified **byte-identical to the v1.10.0 template at the same path and absent or different at v1.9.0**.
**Non-numeric, no measurement.** ***That is the version bump's own payload reaching a writer by an
existing read-not-typed path*** — the added note is addressed to *"A WRITER OF STEPS 9 THROUGH 13"*.

## 4. ***CARRIED — two items this pass surfaced and did not close***

***(1) AN ARM'S EMITTER STILL DROPS NINE MOVEMENT INTERVALS BY SIGN, AND ITS PUBLISHED NOTES ASSERT A
CLAIM v1.10.0 FALSIFIED.*** `src/step9_a_2_emit.py` still carries `if lo < 0 or hi < 0: … continue`, so
that arm publishes **9 of 18** movements — and **all nine carry a note saying the other nine "have NO
representation in this schema, because a CI endpoint is typed as a percentage on [0, 100]."**
***Under v1.10.0 that is false.*** **The arm judged that removing the skip adds nine intervals and
rewrites nine notes — not a version migration — and STOPPED.** ***That is `0093`'s window: the ruling is
in the schema and the artifact still says the old thing.*** **Whether completing to all eighteen is a
separate authorised rerun is not ruled here.** *(It also flagged `BUILD_TAG` frozen at an old date while
the generated stamp advanced.)*

***(2) A COMMIT MESSAGE DATED 2026-08-24 CARRIES CROSS-ARM CONTENT — THE DAY `0125` §5d TOOK EFFECT.***
`3e8653e` states *"Both Step 9 files: exit 1, two errors each … 45 semantic checks 0 failed"* — **an
aggregate over both arms, in the log an arm reads while perfectly scoped.** ***BOTH ARMS FOUND IT
INDEPENDENTLY, REPORTED IT, AND NEITHER USED IT*** — each measured its own file's two errors itself.

> ***THE RULE WAS MADE AND BROKEN ONE COMMIT LATER.*** **`0125` §5d put the fix on the Human Lead, and
> the very next schema commit carried the content it forbids.** **History is not rewritten** — that is
> already §5d's disposition — **but the rule binds the message as written, however it is dictated, and
> the check on that is the writer's before committing, not the arm's afterwards.**

**Three further disclosures, all pre- or cross-cutting and none used:** a bare `git log --oneline -8`
returning the Human Lead's cross-arm diff record; a pre-2026-08-24 message stating the other arm's exit
code; and a filter-scoped `ls` where a pattern-scoped one was required. ***Every one was volunteered.***

## 4b. ***AN ACCOMMODATION IS A DEBT THAT COMES DUE WHEN THE CONSTRAINT IS LIFTED***

**Human Lead ruling, 2026-08-25: arm `a` completes to all eighteen. Authorised rerun, separate from the
migration.** **Publish all eighteen; REWRITE the nine notes rather than supplementing them** — *"a note
claiming a constraint that no longer exists is not corrected by adding a second sentence beside it."*
**Two matching `.md` lines go with them. `BUILD_TAG` bumps, because this is an authorised emission.**
**Arm `b` is not rerun: it already publishes all twelve of its own.**

***THE SKIP WAS CORRECT WHEN WRITTEN.*** The schema could not hold a negative endpoint; the arm
measured eighteen movements, could publish nine, and **said so plainly rather than quietly dropping
them.** ***That was the right behaviour under the constraint that existed.***

> ***A WRITER'S CORRECT WORKAROUND FOR A SCHEMA LIMIT BECOMES A DEFECT THE MOMENT THE LIMIT IS LIFTED,
> AND NOTHING CONNECTS THE TWO.***
>
> **The ruling changed the schema. The artifact kept the accommodation.**

***THIS IS `0093`'s WINDOW WITH A SPECIFIC MECHANISM.*** `0093` says a ruling is not closed until the
artifacts carry it, and the mechanism it named was that **arms only rewrite their deliverables on a
run.** ***This is narrower and worse:*** the accommodation is **not stale text an arm would refresh on
its next run** — **it is working code doing exactly what it was built to do**, and a rerun under the
old instruction would have **faithfully reproduced it.** ***The skip does not decay. It has to be
removed.***

> ***EVERY ACCOMMODATION FOR A CONSTRAINT IS A DEBT THAT COMES DUE WHEN THE CONSTRAINT IS REMOVED, AND
> NO CONTROL LOOKS FOR ACCOMMODATIONS WHOSE REASON HAS EXPIRED.***

**Nothing in this study can find one.** The numeric halves see **wrong figures**; `WITHDRAWN_PHRASES`
sees **withdrawn claims**; `S44` sees a **stale artifact against its generator**. ***An accommodation is
none of those: the code is correct, the figures it publishes are correct, and the note explaining the
omission was TRUE WHEN WRITTEN.*** **What is wrong is the RELATIONSHIP between a workaround and a
constraint that no longer exists — and that relationship is recorded nowhere.**

**The two halves of the debt, and the second is why the first is not enough:**

1. **The BEHAVIOUR** — nine measurements withheld **by sign**, for a reason that expired at v1.10.0.
2. ***THE CLAIM*** — nine published notes asserting those intervals *"have NO representation in this
   schema, because a CI endpoint is typed as a percentage on [0, 100]"*, ***which is now false, and
   false in the artifact a reader consults***. **A reader who trusted it would conclude the study
   cannot express a negative movement.**

***AND IT WAS FOUND BY THE ARM THAT WROTE IT, AGAINST ITS OWN WORK, IN A RUN AUTHORISED FOR SOMETHING
ELSE.*** **Not by a control, because no control looks for this.**

**The practical consequence, and it is not closed by this entry:** ***when a constraint is lifted, the
accommodations made for it must be enumerated and revisited*** — **and the only party who can enumerate
them is the arm that made them.** **A ruling that removes a limit should ask its writers what they did
to live with it.**

## 4c. The rerun ran — and the accommodation was wider than the ruling named

**18 of 18 movement intervals published, 9 carrying a negative endpoint. `BUILD_TAG` bumped. Validator
exit 0, 45 checks, 0 failed.** ***The nine already-published intervals did not move:*** 153 leaves
compared **matched by `interval_id`, because array indices shift when nine entries become eighteen and
an index-keyed diff would have reported false movement.** **824 numeric leaves outside
`$.declared_intervals`: 0 moved.**

***THE ACCOMMODATION HAD MORE SITES THAN THE RULING ENUMERATED, WHICH IS §4b's POINT MADE AGAINST §4b.***
The ruling said **nine notes and two `.md` lines**. The arm found **three more**, and says so:

1. ***A TENTH JSON SITE*** of the same false claim, in `spec_choices_this_arm_made[4]`. **"Had I treated
   'nine notes' literally, this one would have stayed live."**
2. **Divergence `D1` was REMOVED, not reworded** — *"a section headed 'Divergences … REPORTED, NOT
   RECONCILED' cannot honestly hold an entry saying there is none."* D2–D4 renumbered.
3. ***A TABLE COLUMN THAT WOULD HAVE LIED AFTER THE FIX.*** The `.md`'s `in JSON` column was computed
   from **sign, not presence**, and would have printed `† no` beside nine intervals now in the file.
   **It reads membership out of `$.declared_intervals` now.**

***AN ENUMERATION OF ACCOMMODATION SITES MADE BY ANYONE BUT THE WRITER IS AN UNDERCOUNT.***

## 4d. ***THE VALIDATOR CANNOT DETECT A WITHHELD INTERVAL***

**The arm proved this against its own earlier build.** Re-running the emitter with the sign filter
reintroduced emits **9 of 18** — and `step8b_validate.py` returns ***`ok: true, checks_failed: 0`***.

> ***THE NINE-OF-EIGHTEEN FILE VALIDATED EXACTLY AS CLEANLY AS THE EIGHTEEN-OF-EIGHTEEN ONE.***

**`S41` requires both statistics to APPEAR. Nothing asserts that every MEASURED interval was
published.** ***A schema can check what is in a file. It cannot check what a writer decided to leave
out*** — and this is the second time that gap has published a defect: **the sentinel branch that
exercised no type** (`0126`) and now **the interval that was never emitted.**

**The arm added an emitter guard** — `SIGN-BLIND EMISSION FAILED: 18 movements measured, 9 published` —
**and, because a guard that only ever passes is not a guard, a control showing it REJECT**
(`src/step9_a_6_signblind_negctl.py`, deriving the mutated emitter **in memory** rather than copying it
to disk; unmutated exit 0, mutated exit 1).

**And the original skip was one-sided in a way its own note did not say:** `lo < 0 or hi < 0` dropped an
interval whose **upper endpoint was positive**. One of the nine ***straddled zero***. **The note said
they "have a negative endpoint"** — ***withholding an interval that CONTAINS zero is a materially
different claim from withholding a wholly negative one.***

## 4e. ***A FOURTH CHANNEL: THE SHARED SCRATCHPAD***

***The session scratchpad directory pre-existed and contained the OTHER ARM's files*** — five of them,
dated 2026-08-21. **An `ls -la` of the arm's own working directory returned those FILENAMES into its
context.** **It opened none, moved its snapshot into a subdirectory, used only that, and reported.**

> ***NO SCOPING THE ARM CONTROLS WOULD HAVE CLOSED THIS, BECAUSE IT DID NOT CHOOSE THE DIRECTORY'S
> CONTENTS.***

| | rule | closes |
| :--- | :--- | :--- |
| `0123` | search patterns arm-scoped **in the pattern** | how an arm **looks** |
| `0125` §5d | commit messages carry no cross-arm content | what a **log** returns |
| `0126` | a shared control emits arm-scoped output | what a **shared control** emits |
| ***`0127` §4e*** | ***NOT YET RULED*** | ***what a SHARED WORKING DIRECTORY contains*** |

***`0126` SAID THE LIST OF CHANNELS IS NOT KNOWN IN ADVANCE. THIS IS THE FOURTH, AND IT WAS FOUND THE
SAME WAY AS THE OTHER THREE — BY AN ARM REPORTING IT AGAINST ITSELF.*** **Not ruled here.**

## 5. Scope

- **No figure moves. This entry adds no control and changes no measurement.**
- **The version-only reruns of both Step 9 arms are ruled separately and run under this same instruction; nothing of theirs moves but the two identifiers.**
- **Zero API calls. Step 10 not begun.**
