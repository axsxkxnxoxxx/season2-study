# Step 8 — analysis table. GATE APPROVAL

> ***APPROVED BY THE HUMAN LEAD, 2026-08-17. GATE 5 OF 5 IS CLOSED, AND ALL FIVE GATES ARE NOW
> APPROVED.*** **The approval is UNCONDITIONAL**, given with the eight §4 residuals **open and
> published**, and with §4 item 2 — the `logs/` provenance cost — **accepted as recorded, not carried
> as a correction anyone will close.** **The five limitations in §5 travel to Step 14.**
>
> **This file was drafted by the Analytics Engineer and signed only by the Human Lead**, per
> `CLAUDE.md`: *"An agent never records its own approval."* **§7 carries the sign-off.**

| | |
| :--- | :--- |
| **Gate** | Step 8, the analysis table — **gate 5 of 5** |
| **Owner** | Analytics Engineer, dual implementation (`analytics-engineer`, `analytics-engineer-b`) |
| **Approves** | **Human Lead, and only the Human Lead** |
| **Red Team** | **ELEVEN passes. Ten HOLD, then PROCEED on the eleventh, 2026-08-17** |
| **Builds under review** | `a/2026-08-17-0096` and `b/2026-08-17-r8`, both **confirmed by their producing arm** |
| **Status** | **APPROVED, 2026-08-17, unconditionally. Gate 5 of 5 CLOSED.** |

---

## 1. What is being approved

**The analysis table: the position-5 row set, 196,654 rows × the 89 enumerated columns on APPLY, with
DERIV (147,370) flagged in it, and `live` and `outcome` carried as columns.**

**The waterfall, both populations, reproduced independently by both arms to the row:**

| position | APPLY | DERIV |
| :--- | ---: | ---: |
| 1 Step 2 frame · 2 `L2 = 1` · 3 S1 completion — **all inert** | 220,107 | 220,107 |
| 4 contamination exclusion | **201,900** | **152,126** |
| 5 right-censoring | **196,654** | **147,370** |
| 6 liveness (ALT-BROAD, `0064`) | **195,951** | **147,271** |
| 7 outcome assignment — **inert** | 195,951 | 147,271 |

**Liveness excludes 703 from 216 accounts on APPLY (604 never-started + 99 started-and-left) and 99 from
73 accounts on DERIV (0 + 99).** **Line 6's marginal decomposition: `1,355 − 652 = 703` and
`751 − 652 = 99`.**

**Nine invariants, all passing, each naming its population, each satisfying
`rows_asserted + rows_not_asserted = rows_in_the_stated_population`.**

## 2. What the eleven passes established

**Reviews 1–7 contested the deliverable's substance** — the filter order, the invariant set's
falsifiability, the coverage identities, D9's keys and universe, `p_at_bound`'s meaning, D11's scope,
and the half-open boundary form. **They changed what is measured and what is asserted.**

**Reviews 8–11 found almost nothing in the arithmetic and a great deal in the prose.** The tenth pass
named why: **a deliverable of which roughly 120 of 826 lines was measurement**, the remainder
expiry-dated assertions in a static file — *"review retires roughly three per pass; the build adds
roughly the same number."* **It called the position a plateau with an identifiable generator.**

**`0096` removed the category rather than the instances**, and the eleventh pass returned **PROCEED**
with **no live defect of that class inside the four gate deliverables.**

**Two measurements changed a published answer during this sequence, and both survive in the result:**

- **The half-open UTC-instant form is OUTCOME-DECIDING, not inert** — **71 APPLY and 59 DERIV
  position-5 rows change outcome state** under the forbidden date-level form, **36 of them
  never-started → Continued**. It publishes at Step 14.
- **`0068`'s strictness ruling is VACUOUS on this data** — 0 pairs, 0 accounts, both populations,
  measured independently by both arms.

## 3. What both arms reproduce independently

**Every ruled figure**, checked by Red Team on the eleventh pass and by the Human Lead's diff:
the four outcome rows on both populations · `p_at_bound` 1,246 / 1,230 / 1,072 / 1,056 with **all four
emptiness cells 0** and FALSE 17,895 / 17,812 / 15,771 / 15,688 · D2's 168 on APPLY and **153 on DERIV**
· the position-3 drop set of 58,345 · channel overlap in all four units · D3′ 99.53% → 97.73% · the
eight-arm exclusion series and its started-and-left component · the boundary window and its flips ·
D9 as a bound, `[0, 75]`, `[0, 6]`, `[0, 27]` · 2,874 ledger accounts · invariant 9's 20 and 17 rows
**exactly at** `τ_pull`.

**The 89-name column set is set-equal across the arms.**

## 4. What is being accepted, and it is not nothing

***Eight residuals publish with this gate. Approval is given WITH them in view, not around them.***

1. **Two files in `artifacts/` state four things that are false today** — the read-backs, now stamped
   and allowlisted (`0097`). **Invisible to every control**: the third blindness class.
2. **Build history and control results now live in `logs/`, which is git-ignored and on no propagation
   surface.** ***The public artifact set is no longer self-auditing on provenance.*** **This is the
   knowing price of `0096` §1**, and one such log already over-claims its own coverage
   (`surfaces_not_reached: []` while four were never scanned).
3. **Neither arm's deliverable identifies the spec revision it was validated against.** Arm a does not
   fingerprint `task-sheet.md` at all, while asserting its 89-name conformance was read off it at run
   time. **That referent is unrecoverable.**
4. **Three cross-arm coverage divergences under identical labels** — distinct S2 episodes
   (2,135,938 vs 2,023,274), the D9 pivot show-ID count (46,366 vs 45,014), and per-site D11 at
   `A`/`A_H`. **All denominators, none moving a result, resolvable only by reading each arm's mask.**
5. **Nine invariants, six of which cannot fail on any data.** **The gate rests on TWO data checks and
   one cross-check with force.** Both arms publish the 6 + 1 + 2 split and say so plainly.
6. **The arms publish different set-membership denominators** (6,065,704 vs 6,065,610) **and different
   D9 half-(b) grains** — both unruled spec choices, both disclosed by the arm that made them.
7. **The D9 rank-3 tie-break is unruled and the tie is occupied** — six keys at 6. Both arms list all
   six; neither picked the name `0088` §3 gave.
8. **439 unread needle candidates**, deliberately neither failed nor narrowed.

**None of these touches a filter position, a population, a waterfall line, an outcome count, an invariant
result or a bound endpoint.**

## 5. Limitations that travel with the result

**Not defects — properties of the measurement, carried to Step 14.**

- **The half-open form decides 71 APPLY outcomes** (§2).
- **Liveness is outcome-conditional**; the `NOT Continued` conjunct spares **652** on both populations.
  **The commutation check shows the two filter orders agree on OBSERVED COUNTS; it does not show the
  estimand is unaffected.**
- **The liveness rule is a biconditional and `0021` licenses one direction only.**
- **ALT-BROAD leaves 297 pairs in the channel its own warrant describes** — 52.4% closed on the
  implicated set, 47.6% open.
- **Step 9's bounds and published shares are on different populations**, and on DERIV the point estimate
  lies **outside** its own identified set.

## 6. Why approval is defensible now

**The analysis table has been reproduced to the row by two isolated implementations across three
consecutive Red Team passes, and no pass since the seventh has found an arithmetic defect in either
arm.** Red Team's eleventh-pass words: ***"The analysis table is right."***

**Every blocker from the sixth pass onward was a claim about what a check establishes, or text about a
surface the arm does not own — never a number.** `0096` removed that category from the operative
deliverables, and the eleventh pass confirmed it gone from all four.

**The residuals in §4 are real and are listed so that approval is given in view of them.** Six of the
eight are corrections that need no arm; two are unruled spec choices already disclosed by both arms.

## 7. Human Lead sign-off

> ***"Step 8 is approved by the Human Lead, 2026-08-17. Gate 5 of 5 is closed."***
>
> ***"Approval is unconditional with the eight §4 residuals open and published, and with the `logs/`
> provenance cost accepted as recorded rather than carried as a correction anyone will close. The five
> limitations in §5 travel to Step 14."***

- [x] **Step 8 is approved by the Human Lead, date: 2026-08-17**
- [x] **The eight residuals in §4 are OPEN AND PUBLISHED, and approval is unconditional with them so**
- [x] **§4 item 2 — the `logs/` provenance cost — is ACCEPTED AS RECORDED, not a correction anyone will
      close.** ***Stated explicitly because a cost logged as a follow-up reads as a defect awaiting a
      fix, and this one is neither.***
- [x] **The five limitations in §5 travel to Step 14**

**GATE 5 OF 5 IS CLOSED. ALL FIVE GATES ARE APPROVED** — Step 1 (`0001`), Step 5 (`0021`), Step 6
(`0026`), Step 7 (`0064`), Step 8 (`0098`).

**What this unblocks:** Step 8b (output schema, Chained) and Step 9 (results). **`CLAUDE.md`'s handoff
rule still governs** — a chained step returns to the Human Lead before the next one starts, and **no
agent begins either on the strength of this file.**

**Signed by the Human Lead, 2026-08-17. Drafted by the Analytics Engineer, which recorded no approval of
its own.**
