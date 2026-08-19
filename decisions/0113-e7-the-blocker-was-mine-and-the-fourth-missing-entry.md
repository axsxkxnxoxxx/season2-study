# Decision 0113 — E7: `0109`–`0111` never reached the writers. And `0112` was cited before it existed — the fourth time.

| | |
| :--- | :--- |
| **Decision** | **No new ruling.** ***E7 is the blocker and it is MINE: `0109`, `0110` and `0111` never reached surfaces 2, 3 or 7 — the files Step 9's and Step 13's writers actually read.*** They carried **the superseded two-field arm key**, described per-arm nesting **for the headline only**, and **pointed at the MERGED placeholder as the shape to write against.** **Fixed on all four surfaces.** ***And `0112` was committed under its label and never written — the FOURTH occurrence.*** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-19 |
| **Occasioned by** | `reviewer-engineering`'s fourth Step 8b review: **not clear for Step 13b**, on one blocker that is not in the schema |
| **Amends** | `0111` §5's propagation report; `task-sheet.md:818`; the `data-scientist` pair; the glossary |
| **Status** | Open. **E8–E15 are carried. Step 9 blocked by levels-vs-movements, which remains the Human Lead's.** |

---

## 1. E7 — the schema was right and the spec the writers read was not

***`reviewer-engineering`'s framing is exact***: *"The schema, validator and placeholders are in good
shape. What blocks is that `0111` reached three of the eight surfaces, and the two it missed are the two
that Step 9's and Step 13's writers actually read."*

**Measured: `.claude/agents/data-scientist{,-b}.md` contained ZERO occurrences of `0109`, `0110`, `0111`,
`producing_step`, `d3_prime` or `action_type_counts`.** Three specific consequences, each verified:

| what they said | what it would have done |
| :--- | :--- |
| *"keyed on `(W_days, clock_origin)` — NOT `W` alone"* | **the superseded TWO-field key.** Step 9 and Step 13 both write at `W = 108` and `W = 91` — **four payloads, two slots. E2's exact symptom.** |
| *"Step 13's payload nests per producing arm exactly as Step 9's does"* | true of the **headline** only. **E1's six non-headline blocks appear in neither file.** |
| *"`artifacts/step8b-placeholder.json` … the shape to write against"* | ***that is the MERGED placeholder.*** **They write ARM FILES.** **A Step 9 arm built against it fails S17, S28, S29 and S30 on its first run.** |

**Fixed on surfaces 1, 2, 3 and 7.** Both `data-scientist` files now carry the **three-field key**, the
**six non-headline blocks**, **one file per step per arm**, **eight merge sources**, and ***the correct
placeholder — with `step8b-placeholder-sole-file.json` named for Steps 10–12.***

## 2. `0111` §5 stated the surfaces it reached and NOT the ones it did not

**It read: *"Surfaces reached: 1 and 4–5."* It did not say 2, 3 and 7 were pending.**

***`CLAUDE.md`, verbatim: "A propagation report that lists six surfaces and omits that two carry stale
text is the defect this rule exists to stop."*** **That is this, one entry after `0093` made the honest
form mandatory.**

***And no control could see it.*** **The arm key is a STRUCTURAL CLAIM — not a number, not a registered
withdrawn phrase — so `check_surfaces.py` passed clean on all eight surfaces while two of them carried a
superseded key.** ***`CLAUDE.md`'s third blindness class, live, on the ruling under review.***

## 3. `0112` — the fourth missing entry

***Committed under its label, never written.*** After `0092`, `0094` and `0095`. **Written now.**

***The citation resolver `0094` built could not catch it***, and the reason is worth stating precisely:
**it resolves citations on the eight surfaces, and `0112` was cited only in a COMMIT MESSAGE and in a
review brief.** **Neither is a surface, and neither should be** — **but the resolver's silence is
therefore not evidence that an entry exists.**

**The pattern, four times now: the commit message is written with the label before the entry is.** **The
cheap discipline is to write the entry first and let the commit cite something that exists.**

## 4. Carried — eight findings, and two need rulings BEFORE Step 9 runs

| | |
| :--- | :--- |
| **E8** | ***Q1's asymmetry survives at the TOP LEVEL.*** **`channel_classes` is REQUIRED, carries measurements, is owned by `step8` with `may_first_writer_fill: false`, has no `published_by_step` and no `TOP_LEVEL_PUBLISHER` row.** **So all seven arm files must fill Step 8's D4 and D9 figures — seven copies of one figure, no precedence rule, no agreement check.** **The instance was fixed; the class was not.** |
| **E13** | ***Human Lead ruling, and `reviewer-engineering` says take it BEFORE Step 9 runs***: `BLOCK_PUBLISHER` now makes S22 **require** `waterfall` / `liveness_exclusions` / `retained_by_air_period` wherever a `step9` entry is primary — **including a premiere-anchored arm, where the schema's own text says no producer exists.** |
| **E14** | ***A FOURTH identity dimension: the adopted-rule revision the measurement was taken under.*** **Every dimension so far was a setting invisible in the key** — `(W)` → `(W, clock_origin)` → `(W, clock_origin, producing_step)`. **`processed/adopted_rule.json` already carried revision-3 figures against a revision-6 rule once.** **Widen, or record as a known limit.** |
| **E9, E15** | **`S30` has no EXTERNAL anchor** — a merge declaring five of eight sources validates clean, and leg (e) proves **mention, not contribution.** **`STEP_DUALITY` already holds the material to derive the expected eight.** |
| **E10** | **`variant_entry`'s description still carries the pre-E2 two-field key**, live on surface 6. **Arm-owned — a rerun, not a hand-edit.** |
| **E11** | **`declared_intervals` sits outside `ENTRY_FAMILIES` and `TOP_LEVEL_PUBLISHER`.** ***Occupied***: the sole-file placeholder attributes **the window-`W` percentile to `step11`**, which does not compute `W`. |
| **E12** | **A per-arm block missing a `BLOCK_PUBLISHER` row falls through both S22 and S36 silently.** **Complete today; nothing keeps it so.** |

**On the six blocks' one-arm form, `reviewer-engineering` confirms the shape is REPRESENTABLE and
policed** — the branch exists and `_iter_containers` walks every container — **so what is missing is an
example, not a shape.** ***Its recommendation, which I endorse: close it in the SELFTEST rather than by
adding a fourth placeholder***, since fixing surfaces 2 and 3 was required anyway and turns it into a
documentation gap rather than a build gap.

## 5. Scope

- **Surfaces reached: 1, 2–3, 7.** **4–5 needed no change.** **6 and `src/` are the arm's — E10, E11,
  E12, E9, E15.**
- **Zero API calls. Step 9 NOT begun.**
