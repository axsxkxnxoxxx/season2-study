# Decision 0098 — STEP 8 GATE APPROVED. Gate 5 of 5 is closed, and all five gates are approved.

| | |
| :--- | :--- |
| **Decision** | **STEP 8, the analysis table, is APPROVED by the Human Lead, 2026-08-17, UNCONDITIONALLY.** **Gate 5 of 5 is closed and all five gates are now approved.** The **eight §4 residuals are OPEN AND PUBLISHED**, and approval is unconditional with them so. **The `logs/` provenance cost is ACCEPTED AS RECORDED, not carried as a correction anyone will close.** **The five §5 limitations travel to Step 14.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-17 |
| **Record** | `artifacts/step8-gate-approval.md` |
| **Red Team** | **ELEVEN passes. Ten HOLD, then PROCEED on the eleventh, 2026-08-17** |
| **Builds approved** | `a/2026-08-17-0096` and `b/2026-08-17-r8`, both **confirmed by their producing arm** |
| **Status** | **CLOSED. Step 8b and Step 9 are unblocked and NOT launched.** |

---

## 1. What is approved

**The analysis table** — the position-5 row set, **196,654 rows × the 89 enumerated columns on APPLY**,
with **DERIV (147,370)** flagged in it, `live` and `outcome` carried as columns.

**The waterfall**, both populations, reproduced independently by both arms to the row:
**220,107 → 220,107 → 220,107 → 201,900 → 196,654 → 195,951 → 195,951** on APPLY and
**… → 152,126 → 147,370 → 147,271 → 147,271** on DERIV. **Liveness excludes 703 from 216 accounts on
APPLY (604 + 99) and 99 from 73 on DERIV (0 + 99)**, with `1,355 − 652 = 703` and `751 − 652 = 99`.

**Nine invariants, all passing**, each naming its population and satisfying its coverage identity.

## 2. What the eleven passes established, and the distinction matters

***Reviews 1 through 7 CONTESTED SUBSTANCE AND CHANGED WHAT IS MEASURED.*** The filter order, the
invariant set's falsifiability, the coverage identities, D9's keys and universe, `p_at_bound`'s meaning,
D11's scope, and the half-open boundary form.

***Reviews 8 through 11 found ALMOST NOTHING IN THE ARITHMETIC AND A GREAT DEAL IN THE PROSE.***
**The tenth pass named the generator**: a deliverable of which roughly **120 of 826 lines** was
measurement, the remainder expiry-dated assertions in a static file — *"review retires roughly three per
pass; the build adds roughly the same number."* It reported the position a **plateau**, and said the
class would not exhaust under the deliverable scope then in force but would exhaust immediately under a
narrower one.

***`0096` REMOVED THE CATEGORY RATHER THAN THE INSTANCES***, and **the eleventh pass returned PROCEED**
with no live defect of that class inside the four gate deliverables. **Its words: *"The analysis table is
right."***

**Two measurements changed a published answer during the sequence and survive in the result:**
**the half-open UTC-instant form is OUTCOME-DECIDING** — 71 APPLY and 59 DERIV position-5 rows change
outcome state under the forbidden date-level form, **36 of them never-started → Continued** — and
**`0068`'s strictness ruling is VACUOUS on this data**, 0 pairs and 0 accounts on both populations,
measured independently by both arms.

## 3. The eight residuals, open and published

**Approval is unconditional WITH these open, and they are listed in `artifacts/step8-gate-approval.md`
§4 so it is given in view of them rather than around them.** None touches a filter position, a
population, a waterfall line, an outcome count, an invariant result or a bound endpoint.

**Two files stating four expired things** (`0097`, stamped and allowlisted) · **the `logs/` provenance
cost** · **neither arm identifying the spec revision it validated against** · **three cross-arm coverage
divergences under identical labels** · **six of nine invariants unfalsifiable, the gate resting on two
data checks and one cross-check with force** · **two unruled spec choices, both disclosed** · **the D9
rank-3 tie-break** · **439 unread needle candidates.**

***Item 2 is ACCEPTED AS RECORDED, and the Human Lead named why it is not a follow-up:*** build history
and control results now live in `logs/`, which is **git-ignored and on no propagation surface**, so
**the public artifact set is no longer self-auditing on provenance.** **That is the knowing price of
`0096` §1.** **A cost logged as a correction reads as a defect awaiting a fix, and this one is neither.**

## 4. The five limitations travel to Step 14

The **half-open form deciding 71 APPLY outcomes**; **liveness being outcome-conditional** with the
`NOT Continued` conjunct sparing **652** on both populations, and the commutation check showing the
filter orders agree on **observed counts** without showing the estimand unaffected; **the rule being a
biconditional `0021` licenses one direction of**; **ALT-BROAD leaving 297 pairs in the channel its own
warrant describes**, 52.4% closed and 47.6% open; and **Step 9's bounds and published shares being on
different populations**, with the DERIV point estimate lying **outside its own identified set**.

## 5. Scope

- **All five gates are now approved**: Step 1 (`0001`), Step 5 (`0021`), Step 6 (`0026`), Step 7
  (`0064`), **Step 8 (this entry)**.
- **Step 8b and Step 9 are UNBLOCKED and NOT LAUNCHED.** `CLAUDE.md`'s handoff rule governs: **a chained
  step returns to the Human Lead before the next one starts**, and no agent begins either on the
  strength of this entry.
- **No agent recorded an approval.** The record was drafted by the Analytics Engineer and **signed only
  by the Human Lead**.
- **Zero API calls.**
