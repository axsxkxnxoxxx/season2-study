# Decision 0064 — Step 7 approved: ALT-BROAD, unconditionally, with the residual published

| | |
| :--- | :--- |
| **Decision** | **The Step 7 liveness gate is APPROVED. Gate 4 of 5 is closed.** The rule is **ALT-BROAD**: not live iff **no insertion instant after `τ1` AND not Continued**, silence anchored at `τ1` and only at `τ1`, channel window `(τ1, τ2)` open. **The approval is UNCONDITIONAL and the §4 residual is open and published, not resolved.** |
| **Decided by** | **Human Lead**, in writing, in this session |
| **Date** | **2026-08-13**, as stated by the Human Lead |
| **Record** | `artifacts/step7-gate-approval.md` — §6 completed, DRAFT marker removed |
| **Occasioned by** | Fifteen Red Team reviews; the rule uncontested from review 5 and cleared on measurement at review 15 |
| **Status** | Closed. **Step 8 may launch.** |

---

## 1. The approved rule

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> `τ1 = ⟦T0⟧ + W × 24h`, AND the pair is NOT Continued** (Step 1 §7 as amended by `0034`).
>
> **Silence is anchored at `τ1` and only at `τ1`** (`0034`, `0051`, `0054`). **The channel window used
> by the floor widening is `(τ1, τ2)`, open at `τ2`** (`0057`).

**Liveness is a pair-level filter.** Evidence is account-wide; the test is clock-start-relative and the
clock start is pair-specific. One account can be live for one show and not another. **No user is ever
dropped wholesale.**

**Exclusions at `W = 108`: APPLY 703 from 216 accounts (604 never-started + 99 started-and-left);
DERIV 99 from 73 accounts (0 + 99).**

**The bounds** — APPLY on 196,654, DERIV on 147,370:

| | Never started | Started and left | Continued ceiling |
| :--- | :--- | :--- | ---: |
| **APPLY** | [16.6633%, 16.9704%] | **[9.6372%, 10.0405%]**, width 0.4032 pp | 73.6995% |
| **DERIV** | [6.2055%, 6.2055%] *(degenerate)* | **[11.3015%, 11.4291%]**, width 0.1276 pp | 82.4930% |

**Covering with respect to insertion-dormancy, exhaustively; open only across channel classes (D4, D9).**

## 2. Two amendments the Human Lead made to the draft's own wording

**1. The bootstrap placement is Red Team's recommendation, not a ruling.** *"Blocking Step 9, not
Step 8"* came from Red Team's twelfth review, and the draft carried it as though it were settled.
**The Human Lead has not ruled on where the unspecified bootstrap blocks**, and approving this gate does
not rule on it. Recorded in the approval as the recommendation it is.

**2. The approval is unconditional, and the framing is the Human Lead's.** The draft said approval
*"is given with these open and published, not around them"* — the Human Lead **confirmed that framing
rather than accepting it as the drafter's**. **Conditions: none.** The §4 residual publishes with the
result and is not a condition on this gate.

## 3. What the approval rests on

**Red Team reviewed this gate fifteen times and returned HOLD fifteen times.** The distinction that
matters for approval is *what* it held on:

- **Reviews 1–8 contested the rule**, and changed what is measured: the bias-2 sign correction, the
  withdrawal of *"no free parameter"*, the derivation and then **deletion** of the numeric threshold,
  four rule generations (PF-LIMIT → ALT → ALT-BROAD → ALT-MATCHED → ALT-BROAD restored), the **widened
  floor**, and the `τ1` anchoring.
- **Reviews 9–15 found propagation and control defects in figures derived from an unchanged rule.**
  **Not one changed the rule, the population, the exclusion counts, or any bound endpoint on its own
  arithmetic.** They changed where numbers were written, which numbers were checked, and whether a claim
  about a check was true.

**From review 5 the rule statement was not contested.** From review 8 Red Team explicitly cleared the
`τ1` anchoring, the ALT-MATCHED revert, `0021`'s restoration and `0048` §9. **In reviews 12, 13 and 15
it independently recomputed the arithmetic** — both partitions, all four widths, both attainable corners
to exactly 100%, the excess identity, all six sampling ratios — and confirmed it each time.

**The one substantive challenge to the rule after review 8 was review 15's, and it closed on
measurement** (`0063` §1). Dropping conjunct 2 is **PF-LIMIT**, adopted `0041`, superseded `0046`; it
would exclude **652 Continued pairs on evidence they demonstrably produced**. **The size of the
outcome-conditioning is 652 on both populations, and it is now measured rather than argued.**

## 4. The residual is published, not resolved

**Full list in `artifacts/step7-gate-approval.md` §4.** In summary: the **biconditional gap**
(`0021` licenses sufficiency only); **outcome-conditionality, size 652**; the **calibration residual**
discharged at `W = 108` only; the **population mismatch**, on which the DERIV point estimate lies
outside its own bound; **297 pairs remaining in the channel** the warrant describes; the **unspecified
bootstrap**; the **carried control defects** at `0063` §3; and two items **reported not reconciled** —
robustness survival **792 (A) against 791 (B)**, and the **two sampling-width conventions**, which the
spec fixes neither of.

## 5. Scope

- **Gate 4 of 5 is closed. Step 8 may launch** — it is itself a gate and a dual pair.
- **Step 1, Step 5, Step 6 and Step 7 are approved. Step 8 is the remaining gate.**
- **Zero API calls** in the approval.
