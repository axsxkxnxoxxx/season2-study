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

## 5. Scope

- **No figure moves. This entry adds no control and changes no measurement.**
- **The version-only reruns of both Step 9 arms are ruled separately and run under this same instruction; nothing of theirs moves but the two identifiers.**
- **Zero API calls. Step 10 not begun.**
