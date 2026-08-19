# Decision 0114 — E8, E13, E14: three rulings and a ratification

| | |
| :--- | :--- |
| **Decision** | ***E8: arm files do not carry `channel_classes`*** — the merged document carries it once, filled at Step 13b from Step 8's artifact; arm files use the absence idiom. ***E13: publisher rows key on ARM IDENTITY, not producing step alone*** — where the schema's text says no producer exists, an absence is legal and `S22` must accept it. ***E14: the adopted-rule revision joins the key as a FOURTH identity dimension.*** **RATIFIED: the one-arm form closes in the SELFTEST; `0110`'s count of three stands.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-19 |
| **Occasioned by** | `reviewer-engineering`'s fourth Step 8b review |
| **Verified by** | **E14's premise checked BEFORE ruling, as instructed** — see §3 |
| **Status** | Open. **Arm-side set to the arm. Step 9's last blocker after this set is levels-vs-movements, which is the Human Lead's.** |

---

## 1. E8 — the fourth appearance of one-slot-vs-one-definition

**`channel_classes` holds Step 8's D4 and D9 figures.** **Requiring it in seven arm files creates SEVEN
WRITERS OF A FIGURE NONE OF THEM PRODUCED.**

***That is Q1's class at the top level*** — the instance was fixed at `0112` and **the class was not** —
***and it is the FOURTH appearance of one-slot-vs-one-definition***, after `0107` §4, `0109` and `0111`
E1. **Each time the fix has been to put the figure in exactly one place and give every other location
the absence idiom.**

**The merged document carries it ONCE, filled at Step 13b, sourced from Step 8's artifact. Arm files
state an absence.**

## 2. E13 — the schema's text and its control disagree, and the text is right

**`BLOCK_PUBLISHER` makes `S22` REQUIRE `waterfall`, `liveness_exclusions` and
`retained_by_air_period` wherever a `step9` entry is primary** — ***including a premiere-anchored arm,
where the schema's own text says nothing produces one.***

***Publisher rows key on ARM IDENTITY, not producing step alone.*** **Where no producer exists, an
absence record is LEGAL and the control must accept it.**

***And the ruling's own phrase is the operative constraint: ABSENCE STATED, NOT SILENCE.*** **The record
stays required; what stops being required is a figure no step makes.** **That keeps the distinction this
study has spent four entries protecting — an empty result and a clean result are not the same value.**

## 3. E14 — verified before ruling, and the premise is stronger than assumed

**The key becomes `(W_days, clock_origin, producing_step, adopted_rule_revision)`.**

***Same lineage as the two before it***: `clock_origin` (`0102`) and `producing_step` (`0111` E2) were
each **a setting under which the measurement was taken that was invisible in the key.** **This is the
third.**

***AND IT HAS ALREADY BEEN OCCUPIED.*** **`processed/step5/adopted_rule.json` carried REVISION-3 figures
against the approved REVISION-6 rule, and a Step 8 instance had to work around it** — which is why
`CLAUDE.md` made `processed/` surface 8 in the first place.

***Checked rather than assumed, as the ruling required: NO revision key exists anywhere in ANY of the
three placeholders.*** **It is ABSENT, not carried incorrectly** — so this **adds** a dimension rather
than correcting one, and there is no superseded value to register.

## 4. Ratified

***The six blocks' one-arm form closes in the SELFTEST. No fourth placeholder. `0110`'s count of three
stands.***

**`reviewer-engineering` established the shape is REPRESENTABLE and POLICED** — the `dual` + `one_arm`
branch exists, and `_iter_containers` walks every container, so `S28`, `S30` and `S31` reach it whether
or not a file illustrates it. ***What is missing is an EXAMPLE, not a shape*** — **and a synthetic Step
13 arm file built inside the selftest closes it without reopening a deliverable count.**

## 5. To the arm

**E9/E15, E10, E11, E12** — **each reproduced before fixed, each fix demonstrated to reject exactly the
reproduced file.** ***The standing method, and it is what turned M1 from an assertion into a ladder.***

## 6. Scope

- **Surfaces reached: 1, 2–3, 4–5.** **6 and `src/` are the arm's.**
- **Zero API calls. Step 9 NOT begun.**
