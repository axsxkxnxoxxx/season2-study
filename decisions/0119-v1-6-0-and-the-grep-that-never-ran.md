# Decision 0119 — Step 8b v1.6.0 closes surface 6; and `0118`'s "verified by grep" was a grep that never ran

| | |
| :--- | :--- |
| **Decision** | **No new ruling. `0118` is implemented in the schema and `0118` §5 is CORRECTED.** **Step 8b reran as arm `a` at v1.6.0**: the statistic is a **value** in the registry, `fields_not_fixed_in_spec` is **empty and its universe declared**, and **41 checks / 90 mutations**. ***AND THE ARM FOUND MY PROPAGATION FALSE:*** `0118` §5 reported surfaces 4 and 5 as *"0 occurrences, verified by grep, not assumed"* — **the grep exited on a shell error and printed nothing, and I read the empty output as a clean one.** **A stale line stood at `:583` of both files.** **The arm also removed a cross-arm characterisation it had hard-coded into its own generator.** |
| **Recorded by** | Analytics Engineer on the v1.6.0 rerun; §2 recorded against myself |
| **Date** | 2026-08-19 |
| **Amends** | ***`0118` §5, surfaces 4 and 5*** |
| **Verified by** | `check_surfaces.py` **exit 0**, 8 surfaces, 260 files; three placeholders validate at **41 checks, 0 failures**; **the previously shipped artifacts pulled from `HEAD` now FAIL this build** — 16 / 8 / 8 schema errors plus S23, S40, S41 |
| **Status** | Open. **Surfaces 4 and 5 corrected here. v1.6.0 goes to `reviewer-engineering`. Step 9 NOT begun.** |

---

## 1. What v1.6.0 does

**`bootstrap_spec` gains `statistics: ["levels", "movements"]` as a VALUE beside `B` and the seed**,
`fields_fixed_in_spec` becomes all four, and `fields_not_fixed_in_spec` becomes `[]`. **A new
`fields_considered` names the universe those two must partition, so the empty list is ESTABLISHED
rather than merely empty** — *an empty list and an unfilled list are otherwise indistinguishable in
kind*, which is `CLAUDE.md`'s own shape and the arm's own §4(ii) against itself.

**`statistic` is RENAMED to `statistics` in every registry entry** and must hold both.
***The rename is the enforcement***: a writer emitting the old singular key fails against
`additionalProperties: false` rather than being quietly accepted with a per-arm choice nobody reads.
*(`CLAUDE.md`'s `0109` constraint applies — that loud failure depends on no absence branch existing
above the renamed key.)* **`ci.statistic` stays single-valued at the point of use, because a level and
a movement are never compared to each other.** **Every arm now emits a `paired_movement_<arm>`
interval, so the movement branch is PRODUCED rather than described.**

**`if_ruled_otherwise` is retired**, its text quoted and marked — its antecedent has occurred.

## 2. ***`0118` §5 SAID "VERIFIED BY GREP, NOT ASSUMED." THE GREP NEVER RAN.***

**Surfaces 4 and 5 carried a stale line and I published that they carried none.**

`.claude/agents/analytics-engineer.md:583` and `-b.md:583`, byte-identical:

> **Record which bootstrap settings produced each CI.** `B`, seed and levels-vs-movements differ
> between the arms and **the spec fixes none of them**, so an unfixed spec must be visible in the
> output rather than silent.

***All three clauses are false.*** `B`, the seed and the unit were fixed by `0103`; the statistic by
`0118`; **and per `0118` §2 the statistic never differed between the arms at all.**

**The mechanism, and it is worse than a missed file.** The command was

```
grep -rn "movements\|..." .claude/agents/analytics-engineer.md ... --include=*.json
```

**run under `zsh`, which glob-expands `--include=*.json` before `grep` sees it, finds no matching
file, and aborts the whole command with `no matches found`.** **`grep` never executed.** The output
was empty, **I read the empty result as a clean result, and wrote "verified by grep, not assumed"
into a decision entry.**

> ***THIS IS THE EXACT CLASS `CLAUDE.md` NAMES:*** *"An empty result and a clean result are the same
> value, and only the control knows which it produced. A check that finds nothing because it looked
> nowhere must FAIL, not pass."*

**I committed it in the same session in which I wrote that sentence into
`scan_statistic_declaration()`** — where a missing marker fails precisely so two nothings cannot
compare equal. ***The control I built has the property. The hand-check I ran beside it did not.***

**And the negative-grep half could never have caught it**, because the defect was **the checker
exiting**, not the file being clean. **What caught it was an arm reading its own definition file.**
*(Fourth consecutive entry in which the finding came from a reading agent rather than a control.)*

**Corrected on both files at the point of use, and `0118` §5's two rows are corrected in place** —
a false propagation report is worse than a missing one, because it closes the question.

**Standing consequence, no ruling needed:** ***a shell that can abort before the tool runs makes an
empty result unreadable.*** **Check the exit status, or use `--` / quote the pattern, or run the
scan through `check_surfaces.py`, which reports its coverage count.** `CLAUDE.md` already says
*"check with `src/check_surfaces.py`, not with `grep`."*

## 3. The arm's own defect, and it is the same rule from the other end

***v1.5.0 hard-coded `ARM_STATISTIC = {"a": "movements", "b": "levels", "sole": "levels"}`*** and
derived every placeholder interval's statistic from it. **Per `0118` §2 that split was never true**,
and **the build shipped it into three artifacts.**

***It reached the arm from surface 4, not from a prompt.*** **That is `0095`'s failure arriving
through a spec file rather than a launch instruction** — a characterisation of the other arm that the
receiving arm is structurally forbidden to re-measure. **The rule names launch instructions; the
route that actually fired was an agent definition.** Removed; the module now records the ruling and
names what it replaced.

**And the reason this rerun was needed at all, in the arm's words: no mutation in the prior table
targeted `bootstrap_spec`.** **The seven stale lines were TEXT, and the numeric controls cannot see
text.** **S40 now carries four mutations against that block.**

## 4. The honest answer to the Human Lead's question, and NO `const` was added

***"Can the schema carry a statistic that contradicts the writers' canonical block?" — YES.***
Published in `known_limits_of_this_schema`:

- **(a) A declaration is not a computation.** A writer that bootstrapped **levels only**, wrote the
  pair into its registry, and attached the `movements` label to a levels interval **validates clean.**
  **The schema sees what a file says about itself; `0118` is enforced as a SHAPE, not as a FACT.**
- **(b) `S41` asks whether both objects APPEAR, not whether the right quantities have both.** One
  movement interval anywhere in an arm satisfies it. **The spec names no quantities that must carry a
  paired counterpart, so there is no list to check against.**
- **(c) Vocabulary drift** — the enum tokens were typed and agreed by inspection.

**(c) is now closed as a CHECK rather than a constant:** the selftest **reads the canonical block off
both writer files**, asserts byte-identity, asserts all four elements by value, and asserts **this
schema's enum is exactly the set the block names** — **a missing marker fails.** *(This is the block
being read rather than restated, which is the same move `read_not_typed` only declares. F3 stays
carried and out of scope, by instruction.)*

***No `const` asserting agreement was added***, on the `diff_precedes_merge` precedent: **a sentence
the schema requires the file to contain is not a fact the file records.**

## 5. One consequence the arm reported rather than leaving to be inferred

**With all four elements fixed and identical, two `bootstrap_settings` entries now differ ONLY in
`producing_arm`.** So **`S32` catches an arm MISLABEL and no longer catches a settings MISMATCH —
there is none left to catch**, and **`statistic` left the `S30` forgery ladder and `_ARM_LABELS`**,
because normalising it away **would now hide a real divergence about which object an arm reported.**
***The forged-merge is one field cheaper than it was.*** **A control whose force narrows silently is
how a passing check stops meaning what its name says.**

## 6. Propagation

| Surface | State |
| :--- | :--- |
| **1 `task-sheet.md`** | **Reached at `0118`; re-verified, 1 hit, marked at the point of use** |
| **2–3 `data-scientist{,-b}.md`** | **Reached at `0118`; re-verified, 1 hit each, corrected. Canonical block read at 2,118 chars** |
| **4–5 `analytics-engineer{,-b}.md`** | ***NOT REACHED BY `0118` — 1 stale line each. CORRECTED HERE. §2*** |
| **6 `artifacts/`** | ***REACHED — this run's purpose. 0 stale occurrences; the 3 residual hits are retirement notes naming retired text as retired*** |
| **7 `second-brain/`** | **0 occurrences, verified** |
| **8 `processed/`** | **0 occurrences, verified** |
| **`src/step8b_schema.py`** | **Reached — 0 of the 9 lines remain. The 2 surviving `ARM_STATISTIC` strings are comments naming it as superseded** |

**Counts, stated because a report without one is what `0118` §5 was:** validator **39 → 41**;
selftest **83 → 90 mutations, 0 removed, 0 changed status**, `checks_defined_but_never_exercised: []`;
three placeholders at **41 checks, 0 failures**; `check_surfaces.py` **exit 0** over **260 files**.
**Open and unchanged by this run: the needle register's 442 untriaged candidates.**

## 7. Scope

- **No figure moves. No population changes. Zero API calls. Step 9 NOT begun.**
- **v1.6.0 goes to `reviewer-engineering`**, aimed at whether anything else in the schema still
  asserts a Step 9 blocker `0118` cleared, and at whether `scan_statistic_declaration()`'s
  byte-identity check has a hole its selftest does not exercise.
