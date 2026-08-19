# Decision 0116 — the three-field key marked on four surfaces; and an arm wrote a decision entry

| | |
| :--- | :--- |
| **Decision** | **No new ruling.** ***`0114`'s propagation ADDED the four-field key and LEFT THE THREE-FIELD KEY STANDING on four surfaces — in three of them BELOW its own replacement.*** **`0113` §2's defect, one entry later.** **Marked at the point of use on all four.** ***AND `decisions/0115` was written by an ARM.*** **Its content is accurate and is retained; the boundary is the finding.** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-19 |
| **Occasioned by** | Arm `a`'s Step 8b v1.5.0 report, which flagged the stale key itself and correctly did not edit it |
| **Amends** | `0114`'s propagation |
| **Status** | Open. **Step 9's last blocker is levels-vs-movements, which is the Human Lead's.** |

---

## 1. The key, marked — and the arm found it, not a control

**`0114` added `adopted_rule_revision` as a fourth dimension. It wrote the four-field key in new text and
left four three-field statements standing**, at `task-sheet.md:820` and `:879`,
`.claude/agents/analytics-engineer{,-b}.md:525`, and the glossary — ***and in three of them the
superseded text sits BELOW its replacement.***

***This is `0113` §2 one entry later.*** **I recorded that a propagation report must name what it did
NOT reach, then made a propagation that left the superseded text in place beside what replaced it.**

***And `check_surfaces.py` cannot see it, for the same reason as last time***: **an arm key is a
STRUCTURAL CLAIM — not a number, not a registered withdrawn phrase.** ***Second consecutive entry where
the third blindness class hid a stale key from every control.*** **The arm found it, as it found the
last one.**

**Marked at the point of use on all four surfaces**, and the arm ***correctly did not edit them***:
*"propagating a ruling into the spec an arm reads is not an arm's to do"* — the same judgement it made
at `0108` §1 and `0110`.

## 2. An arm wrote `decisions/0115`

***`decisions/` is not an arm's folder.*** **`CLAUDE.md` gives each agent a named output folder, and the
decision log is where rulings and their records live.** **Arm `a` wrote `0115` directly.**

***The content is accurate — I checked it against the run, and it records no ruling and claims no
approval*** (*"No new ruling"*, `Recorded by: Analytics Engineer, arm a`). ***It is retained*** rather
than deleted, because deleting a truthful record to enforce a boundary would lose the record.

**But the boundary is real and is stated here rather than left implicit:** ***an arm reports to the
Human Lead, and the Human Lead's agent writes the entry.*** **The reason is not ceremony — it is that
`decisions/` is a surface every arm READS**, and `0096` r2 permits cross-arm content there precisely
because it has passed through the Human Lead's diff. ***An entry written by one arm and read by the
other routes around that.***

**Nothing in `0115` does route around it** — it describes only its own work. **The rule is stated for
the next one, which might not.**

## 3. What v1.5.0 closed, in the arm's own record

**`0114`'s E8, E13, E14 are IN THE ARTIFACTS**, which is where `0093` says a ruling closes. **E9/E15,
E10, E11, E12 each reproduced on the v1.4.0 build in a scratch tree — *re-runnable rather than
asserted* — then fixed, then demonstrated.** **39 checks, 0 failures; 83 mutations all with force;
no check defined-but-unexercised.**

***The ratification is honoured***: a synthetic Step 13 arm file inside the selftest carries all six
blocks in one-arm form. **No fourth placeholder. `0110`'s count of three stands.**

***And the fixture surfaced two defects while being built***, both fixed: **S21's required branch
families were keyed on role alone, so a Step 13 arm file failed for holding exactly what the spec asks
of it**; and **the selftest's headline counted what it TRIED, not what EXISTS** — it now fails on any
check defined and never exercised. ***A test harness that could not tell an unexercised check from a
passing one is the look-nowhere defect inside the thing that measures force.***

## 4. Carried

- ***The adopted-rule revision is read by PARSING KEY NAMES.*** `_read_adopted_rule_revision()` scans
  `processed/step5/adopted_rule.json` for `approved_(?:rule_)?revision_(\d+)` and takes the highest —
  reading **6** from `_SUPERSEDED_FIGURES_CORRECTED_2026_08_13.approved_rule_revision_6`. **A newer
  revision under a non-matching key would leave the older one looking current.** **A first-class field
  in that file removes the inference — it is Step 5's output, so the arm reported rather than edited.**
  **No match is a hard stop, never a default.**
- **The expected merge-source set is derived from a table that is a COPY of the spec.** **It catches a
  merge declaring fewer sources than the table knows; it cannot catch a source the table has never heard
  of.** **`S31` asserts the table against each file's own `$.step_duality`, so a newer-spec file
  disagrees loudly.**
- ***LEVELS-VS-MOVEMENTS***, and see §5.

## 5. The levels-vs-movements justifications, as they exist on disk

***Reported without resolution, and no arm was asked.***

**Arm B stated one.** `artifacts/step7-liveness-bb-b.json`, at `/bootstrap`:

> *"nonparametric bootstrap, clusters = ACCOUNTS, unit = pair. Accounts resampled with replacement from
> the accounts present in the position-5 population; **the liveness rule is RE-APPLIED inside each
> replicate, so the exclusion count is itself random**."* — `replicates: 2000`, `seed: 20260814`

***Arm A has no counterpart block.*** **`artifacts/step7-liveness-bb-a.json` carries no `bootstrap`
object at that path**, and every occurrence of *"movement"* in arm A's deliverables —
`step7-liveness-bb-a.md:225`, `:554`, `:558`, `step7-liveness-mm-a.md:161`, `:163`, `:166` — **is about
SHARE MOVEMENTS BETWEEN RULES, not the bootstrap statistic.**

***So the pairing "A: movements, B: levels" exists in `decisions/` and not in arm A's deliverable***:
`0052` §122, `0055` §288, `0056` §150. ~~**And those entries disagree on the seed** — `0053` §107 reads
*"and movements, seeds stated (20260813 and 20260815)"* against `0052`'s `20260813`.~~

> ***THE SEED HALF IS WITHDRAWN, 2026-08-18, `0106` §7.*** **`0053` §107's pair is `(20260813,
> 20260815)` for the `mm` run and is CORRECT on disk; `0052` §122's `(20260813, 20260814)` is the `bb`
> run and is also correct.** **Different runs, not a contradiction.** ***The first half of this
> paragraph — that "A: movements, B: levels" exists in `decisions/` and not in arm A's deliverable —
> STANDS, and is now stronger: arm A reports BOTH on both runs.***

**Arm A's actual configuration and reasoning would have to come from arm A reporting what it ran**,
which is a measurement of its own past work rather than a ruling — **and `0095` makes a launch
instruction a live hazard here, so it is not done without the Human Lead's word.**

## 6. Scope

- **Surfaces reached: 1, 4–5, 7.** **Zero API calls. Step 9 NOT begun.**
