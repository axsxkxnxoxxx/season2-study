# Decision 0118 — the bootstrap statistic is fixed as BOTH levels and paired movements; "A: movements, B: levels" is CORRECTED, not marked

| | |
| :--- | :--- |
| **Decision** | ***"BOTH, EXPLICITLY LABELLED" SATISFIES `0056` §159.*** **The statistic is FIXED as BOTH levels and paired movements, both arms, both objects labelled, neither presented as *the* design.** ***This closes the third and last unfixed bootstrap element and Step 9 is no longer blocked on the bootstrap.*** **And "A: movements, B: levels" — at three `decisions/` sites and four propagated surfaces — is CORRECTED, NOT MARKED: it was wrong when written, not superseded later.** **A control now fails if the two arms' declarations differ.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-19 |
| **Amends** | `0052` §6; `0055` §5; `0056` §8 and §159; `task-sheet.md` Step 9 and Step 8b; both `data-scientist` files |
| **Occasioned by** | Arm `a`'s own report of its Step 7 bootstrap configuration, verified against disk at `0106` §7 |
| **Verified by** | `check_surfaces.py` **exit 0**, including the new `scan_statistic_declaration()` at **2,118 characters compared byte for byte**; the two writer files **`diff` to the `name:` line alone**. ***The control was probed LIVE, not only by its selftest:*** changing `account` to `show` in one file alone drove **exit 1** with both failure modes named, and restoring it drove **exit 0** |
| **Status** | **Open — surfaces 6 and the Step 8b generator carry the superseded text and are PENDING A RERUN.** See §5. **Step 9 is NOT begun.** |

---

## 1. The ruling

***The statistic is BOTH levels and paired movements. Both arms produce both objects. Both are
labelled. Neither is presented as the design.***

**The Human Lead's reasoning, recorded as given:**

- **The requirement exists so the diff compares like with like.** **Both arms producing both objects
  satisfies that fully** — **a divergence on either object is then a real divergence rather than a
  design difference.** Fixing on one object would have discarded the other and bought no
  comparability that both does not already buy.
- **Neither may be dropped, because they are different objects.** On APPLY the never-started
  **level** is **1.09 pp** wide against a **0.098 pp** **movement** — **a factor of 11**
  (`artifacts/step7-liveness-mm-a.md:448–449`) — **so a reader must be told which one they are
  reading.** ***Same reasoning as publishing the floor and the ceiling rather than a point.***
- **It goes into the spec explicitly.** **Arm `a` arrived at both on its own judgement, which is an
  unstated convention that happened to be right** — ***the shape this build has been bitten by
  repeatedly.*** **Both `data-scientist` files state the requirement in the same words.**

***ALL THREE BOOTSTRAP ELEMENTS ARE NOW FIXED AND IDENTICAL FOR BOTH ARMS:*** `B` = **10,000**,
seed = **20260818**, resampling unit = **account** (`0103`), **statistic = BOTH** (`0118`).

## 2. "A: movements, B: levels" was never true, and is CORRECTED rather than marked

***A mark is for a claim that was true and got superseded. This one was wrong when written.***

**Arm `a` published BOTH objects on BOTH runs** — `artifacts/step7-liveness-mm-a.json:1018`
(`"reports": "LEVELS and PAIRED MOVEMENTS, both, explicitly labelled"`), and the gate-closing `bb`
run computes both as well, `processed/step7/bb_a/bootstrap.json` carrying `settings` and
`paired_delta_rule_minus_no_filter` side by side. **The arms diverged on TWO elements, `B` and the
seed — not three.**

| # | Site | Disposition |
| :-- | :--- | :--- |
| 1 | `decisions/0052-…:122` | **corrected**, correction note appended |
| 2 | `decisions/0055-…:288` | **corrected**, correction note appended |
| 3 | `decisions/0056-…:150` | **corrected**, correction note appended |
| 4 | `task-sheet.md:960` | **corrected** |
| 5 | `.claude/agents/data-scientist.md` | **corrected** |
| 6 | `.claude/agents/data-scientist-b.md` | **corrected** |
| 7 | `.claude/agent-memory/second-brain/gate-step7-liveness.md:496–498` | **corrected** |

**Site 7 is the instructive one.** That paragraph recorded, one sentence earlier, that at the `0053`
run **both** arms ran *"both levels and movements"* — **and then restated "A: movements, B: levels"
immediately below it, unreconciled.** ***The contradiction sat inside a single paragraph on the
memory surface that is fed back into rulings.***

**Seven sites, seven corrected. The count is stated because `CLAUDE.md` forbids reporting
"corrected at the point of use" without one** — `0103` reported exactly that phrase having reached
two of four.

## 3. The control, and what it can and cannot do

**`src/check_surfaces.py::scan_statistic_declaration()`.** `reviewer-engineering`'s **E11** required
that *"when it IS fixed, a check must assert both arms' `statistic` agree — or the fix will be
recorded and unpoliced."* **It is built with the ruling rather than after it.**

- **The requirement is ONE block**, delimited by `<!-- BOOTSTRAP-STATISTIC-BEGIN/END -->`, and the
  control compares the two copies **as bytes**. `CLAUDE.md`: *"Never describe the task twice in your
  own words."* **Two paraphrases of one requirement are two definitions of it.**
- **A MISSING MARKER FAILS AS LOUDLY AS A MISMATCH.** If a marker is deleted the extraction returns
  nothing, **two nothings compare equal**, and a naïve byte-identity check would report clean over
  **zero characters** — the exact shape of the three controls that reported clean while checking
  zero rows.
- **It asserts all four fixed elements by VALUE** in each copy — `10,000`, `20260818`, `account`,
  `levels and paired movements` — not by prose.
- **It prints its coverage:** files read, **characters compared**, elements asserted. Current run:
  **2/2 files, 2,118 characters, 4 elements.**
- **`_selftest_statistic_matcher()` runs on every invocation** and asserts the control fails on each
  thing it claims to catch: a changed unit, a changed `B`, a deleted marker, and **two absent
  blocks**. ***A control asserted to exist is not a control*** (`CLAUDE.md`, on the mechanism that
  never fired).

***What it cannot do:*** it checks the **spec**, not the **output**. **Whether a Step 9 run actually
emits both objects is Step 8b's schema's job**, and that half is in §5 as pending.

## 4. One rule-conflict, resolved explicitly rather than silently

**`CLAUDE.md`'s `## Cross-arm characterisations never enter a launch instruction` forbids relaying
one arm's shape into the other arm's prompt.** **The factor of 11 was measured by arm `a`.** Naming
it as arm `a`'s in `data-scientist-b.md` would be exactly that relay — **and the block must be
byte-identical, so it cannot name an arm at all.**

**Resolved under the `0096` amendment**, which admits **a ruled figure in a decision entry** as a
spec input rather than a peek: **the block states the magnitudes as the RULING's ground, with no arm
attribution, and points here.** **The attribution is recorded in this entry**, where cross-arm
content is permitted. ***Flagged rather than done quietly, because a rule routed around silently is
the failure `0095` records.***

## 5. Propagation — reached, and NOT reached

| Surface | State |
| :--- | :--- |
| **1 `task-sheet.md`** | **REACHED — 3 sites** (:914, :960, and the "specify all three" tail) |
| **2 `data-scientist.md`** | **REACHED — 4 sites** (:49, :138, :199, and the canonical block replacing :215–231) |
| **3 `data-scientist-b.md`** | **REACHED — the same 4. The two files now differ ONLY in `name:`, verified by `diff`** |
| **4 `analytics-engineer.md`** | **NOT APPLICABLE — 0 occurrences, verified by grep, not assumed** |
| **5 `analytics-engineer-b.md`** | **NOT APPLICABLE — 0 occurrences, verified** |
| **6 `artifacts/`** | ***NOT REACHED. 4 files, 7 lines*** — `step8b-output-schema.json:658,742` and the three placeholders — **still say levels-vs-movements is unfixed.** ***PENDING A STEP 8b RERUN*** |
| **7 `second-brain/`** | **REACHED — 1 site** |
| **8 `processed/`** | **NOT APPLICABLE — 0 occurrences, verified** |
| **`decisions/`** | **REACHED — 4 sites across `0052`, `0055`, `0056`** |
| **`src/step8b_schema.py`** | ***NOT REACHED — 9 lines***, including `fields_not_fixed_in_spec: ["statistic (levels vs movements)"]` at `:4764`. **It GENERATES surface 6**, so patching it without rerunning would leave generator and artifact disagreeing with nothing checking it |

***SURFACES 6 AND THE GENERATOR CARRY THE SUPERSEDED TEXT RIGHT NOW.*** This is `0093`'s window
exactly: **the ruling is propagated to every surface an agent reads and the artifacts still say the
old thing until an arm reruns.** ***This entry does not say "closed."***

**Whoever reruns Step 8b closes it by:** moving `statistic` from `fields_not_fixed_in_spec` to
`fields_fixed_in_spec`; making the schema require **both** statistics present rather than recording
a per-arm choice; and retiring `if_ruled_otherwise`, whose condition has now occurred. **A schema
version bump follows, and `read_not_typed` (§F3, still carried) can be closed in the same rerun.**

## 6. Scope

- **No figure moves. No population changes. No bound endpoint moves.** The 1.09 / 0.098 / factor-11
  figures are **cited as the ruling's ground**, not published as new measurements.
- **Zero API calls. Step 9 is NOT begun. No agent was launched.**
