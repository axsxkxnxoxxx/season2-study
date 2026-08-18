# Decision 0110 — M1's false clean is closed with its residual published; five more findings closed; three placeholders

| | |
| :--- | :--- |
| **Decision** | **No new ruling. Step 8b v1.3.0.** ***M1 — the merged document assembled from ONE arm file — was REPRODUCED against the committed pre-fix build, then fixed, and the fix DEMONSTRATED against exactly that file.*** **A residual survives at the third rung and is PUBLISHED rather than closed by assertion.** **M2, M6, M7, M8, M10 closed. `diff_precedes_merge` RETIRED rather than kept.** **The spec named one placeholder; `0109`'s granularity makes three legal shapes, and the spec is amended here — not by the arm.** |
| **Recorded by** | Analytics Engineer, on arm `a`'s Step 8b rerun |
| **Date** | 2026-08-18 |
| **Verified by** | **All three placeholders validate at exit 0**; **57 selftest cases all have force**; `check_surfaces.py` |
| **Status** | Open. **Step 9 blocked by levels-vs-movements. The M1 residual is published and open.** |

---

## 1. M1 — reproduced first, which is what made the fix checkable

***The arm reproduced the false clean against the COMMITTED pre-fix build***, extracted to a scratch
directory so it is reproducible: every two-arm block's `arms.a` payload deep-copied into `arms.b` with
the arm labels changed — **8 blocks**. Result: **`schema_valid: true`, 0 of 29 checks failing**, and the
file publishing a `cross_arm_divergences` entry **as if two arms had been compared.**

***The discriminator was TESTED, not assumed.*** **Arity is observable where isolation is not**, and the
fix rests on it: each merge input now names its `producing_step` and `arm`; each payload names the input
it came from; and **`S30`** asserts that a two-arm block names **two different files**, that the arms'
**`ratio_block.convention_label` differ** wherever both are present, that the diff record **compares a
non-zero number of figures** and **its divergence count equals the published entry count**, and that **an
arm file may claim no merge provenance at all.**

***THE LADDER, AND THE RESIDUAL IS THE POINT.***

| rung | outcome |
| :--- | :--- |
| naive copy | **rejected — S30 and S32** |
| copy with bootstrap refs, `statistic` and convention labels relabelled | **rejected — S30** |
| **copy with merge provenance ALSO relabelled** | ***PASSES*** |

**At the third rung the file asserts a second input exists and nothing inside it can contradict that.**
**Published in `known_limits_of_this_schema`**, with S30 reporting the one remaining signal as a
**non-failing note** — payload pairs byte-identical once arm labels are normalised — **and the selftest
asserting it as a REQUIRED NON-FAILURE, so the published limit cannot drift from the behaviour.**

***That last clause is the part worth keeping***: a limitation that is only prose drifts from the code
that produces it. **This one is pinned by a test.**

**`diff_precedes_merge` is RETIRED**, not kept — *"a sentence the schema requires the file to contain"*
— and replaced by **`merge.diff`** carrying facts a check can reach: **`pairs_diffed` (two named files
per dual step), `figures_compared` (may not be zero), `divergences_found` (must equal the entry count)**.
**The old key now fails loudly against `additionalProperties: false`.**

## 2. The other five, and one is a control for a constraint

- **M2** — duality pinned **three ways**: a required `$.step_duality` registry with each status `const`,
  `if/then` inside `by_producing_arm` per step, and **`S31`**, which asserts against **the spec's map held
  in the validator — not read from the file under test.** ***The selftest mutation is a pure RELABEL,
  shape untouched*** — the half the earlier case did not cover, which is exactly why M2 existed.
- **M6** — `statistic` added to `$defs/ci`'s required set and to S23's compared fields, and **`S32`**
  asserts every interval references a registry entry **whose `producing_arm` owns the payload.**
  ***This records what each arm used and decides nothing about levels vs movements*** — closable
  without pre-empting the open ruling, as intended.
- **M7** — **`S33`**: `performed: true` with `coverage_count: 0` **fails**, at every search record and at
  D9's `records_examined` beside a published bound, **plus a structural `if/then`.**
- **M8** — `block_ownership` now carries **dotted paths for 14 nested blocks**, plus a new
  **`published_by_step`**, because *"who owns it"* and *"whose file does it arrive in"* became two
  questions under §6.
- **M10** — a `declared_intervals` block illustrating **a `show`-unit CI and the `unit_disagreement`
  subtree**, and **S21 now REQUIRES** the `show` unit in all three files. **Step 16 can no longer be
  built without the branches `0103` §2 exists to protect.**

***And `S35` is a control for the constraint `0109` §4 recorded***: it **walks the schema graph and fails
if any `oneOf`/`anyOf` sits between the root and `by_producing_arm`** — **exercised by mutating the
schema itself**, adding precisely the absence branch M9 might have tempted. **A recorded constraint that
now has a test is no longer a note anyone has to remember.**

## 3. The arm file was the one that was wrong

**`0108` §2 reported the arm took §1's reading. Both artifacts shipped, on opposite sides** — and
**`0109` ruled §6**, so **the ARM FILE was wrong**: it carried `also_written_by_steps: ["step8","step13"]`
and `variants`. **It is now Step 9 arm a's file alone**, with blocks another step publishes written as
**`awaiting_owner_step` absences naming the publisher.**

**S22 is now scoped by publisher**, so an absence fails only where the file's own step publishes the
block — **and a check whose sites all live in another step's blocks reports N/A QUOTING THE FILE'S OWN
ABSENCE RECORDS**, while **an emptiness with no record behind it still reports VACUOUS.**

## 4. Three placeholders — the spec named one, and that is this entry's job

**`0109` fixed granularity at one file per step per arm, which makes THREE legal shapes.** **The arm
emitted all three and correctly did NOT amend its own spec** — *"propagating a ruling into its own spec
is not an arm's to do"*, the same judgement it made at `0108` §1. **Amended here, on `task-sheet.md` and
both `analytics-engineer` files.**

***A role with no placeholder is a shape Step 16 would be built without***, which is the reason the spec
required one to begin with.

## 5. Open

- ***THE M1 RESIDUAL.*** **A fully relabelled copy passes.** **No in-file control can close it** — **the
  Human Lead's diff between two files remains the control**, which is what `0107` said the diff was for.
- ***LEVELS-VS-MOVEMENTS***, untouched. **Step 9's blocker.**
- **Zero API calls. Step 9 NOT begun.**
