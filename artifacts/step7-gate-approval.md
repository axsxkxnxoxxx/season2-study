# Step 7 — liveness rule — GATE APPROVAL

> **APPROVED BY THE HUMAN LEAD, 2026-08-13.** Gate 4 of 5 is closed.
>
> The Human Lead stated the approval in writing in this session, on the draft of this document, and
> directed that §6 be completed and the gate checklist ticked. **Step 8 may launch.**
>
> *Date note, recorded rather than silently adjusted: the approval is dated **2026-08-13** as the Human
> Lead gave it, while `0060`–`0063` — including `0063`, which carries the 652 measurement §3 rests on —
> are dated **2026-08-13**. Flagged to the Human Lead for confirmation or correction. The decision log
> is a public tracked artifact and `0058` §6 corrected a date drift in the other direction; neither is
> fixed here without a ruling.*

---

## 1. The rule

> **A user-show pair is NOT LIVE if and only if BOTH:**
> - **the account shows no insertion instant after `τ1 = ⟦T0⟧ + W × 24h`, AND**
> - **the pair is NOT Continued** (Step 1 §7 as amended by `0034`).
>
> Otherwise it is live. **Silence is anchored at `τ1` and only at `τ1`.** The channel window used by
> the floor widening is **`(τ1, τ2)`, open at `τ2`.**

**ALT-BROAD.** Adopted `0048`, restored `0054` after ALT-MATCHED was reverted, re-affirmed at every
entry since. **Liveness is a pair-level filter**: one account can be live for one show and not another.

**Exclusions at `W = 108`: APPLY 703 from 216 accounts (604 never-started + 99 started-and-left); DERIV
99 from 73 accounts (0 + 99).**

## 2. What the rule produces

| APPLY, n = 196,654 | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 32,769 → **16.6633%** | 33,373 → **16.9704%** | 0.3071 pp |
| **Started and left** | **18,952 → 9.6372%** | 19,745 → **10.0405%** | **0.4032 pp** |
| *conditional sub-interval — not a bound* | *18,952 → 9.6372%* | *19,141 → 9.7333%* | *0.0961 pp* |
| Continued | 144,140 → 73.2962% | 144,933 → **73.6995%** | 0.4032 pp |

| DERIV, n = 147,370 | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 9,145 → **6.2055%** | 9,145 → **6.2055%** | 0.0000 pp *(degenerate)* |
| **Started and left** | **16,655 → 11.3015%** | 16,843 → **11.4291%** | **0.1276 pp** |
| Continued | 121,382 → 82.3655% | 121,570 → **82.4930%** | 0.1276 pp |

**The three ceilings cannot all hold**: APPLY sums to **100.7104%**, excess `2 × 604 + 189 = 1,397`
pairs; DERIV to **100.1276%**, excess `188 = 99 + 89`. They are alternative worst cases over one set.

**The bound's scope, which publishes with it:** **covering with respect to insertion-dormancy,
exhaustively; open only across channel classes (D4, D9).**

## 3. What eleven consecutive reviews did not shake

**Red Team has reviewed this gate fifteen times.** From review 5 onward it has **not contested the rule
statement**, and from review 8 it has explicitly cleared the `τ1` anchoring, the ALT-MATCHED revert,
`0021`'s restoration and `0048` §9. In reviews 12, 13 and 15 it **independently recomputed the
arithmetic** — both partitions, all four widths, both attainable corners to exactly 100%, the excess
identity, and all six sampling ratios — and confirmed it each time.

**Reviews 9–15 found propagation and control defects in figures derived from an unchanged rule.** Not
one changed the rule, the population, the exclusion counts, or any bound endpoint on its own arithmetic.
They changed **where numbers were written, which numbers were checked, and whether a claim about a check
was true.** Seven entries — `0057` through `0063` — were needed for the machinery to catch up with an
analysis that had already stopped moving.

**The one substantive challenge to the rule since review 8 was review 15's**, and it is answered:
dropping conjunct 2 is **PF-LIMIT**, adopted at `0041` and superseded at `0046`. It would exclude **652
Continued pairs on evidence they demonstrably produced.** **The size of the outcome-conditioning is 652
on both populations, now measured** (`0063` §1).

## 4. The residual — logged, not resolved

**Approval is UNCONDITIONAL, and it is given with these open and published — not around them.**
**Confirmed by the Human Lead**, 2026-08-13, in those terms: the residual below publishes with the
result and none of it is a condition on this gate.

**Limitations of the rule** *(Step 14)*
1. **The biconditional gap.** `0021` licenses *insertion after `τ1` ⟹ live* — sufficiency only. The rule
   also asserts the converse. **ALT-BROAD narrows where that assertion is made, from PF-LIMIT's 1,355
   pairs to 703. It does not justify it.**
2. **Liveness is outcome-conditional** through conjunct 2. `ordering_commutation_check` shows the two
   filter orders agree on **observed counts**, not that the estimand is unchanged. **Size: 652.**
3. **The calibration residual**, discharged at `W = 108` only; Step 13 runs to `W = 213`.
4. **The population mismatch** — bounds on position-5, shares post-liveness; on DERIV the point estimate
   lies outside its own bound.
5. **297 pairs remain in the channel the warrant describes** — 207 never-started, whose null `0021`
   licenses, and 90 started-and-left, whom the widened floor now admits.

**Blocking Step 9, not Step 8**
6. **The bootstrap is unspecified.** The two arms diverged on `B`, seed **and** statistic. `0052` §6's
   *"now specified"* is struck. **Step 9's CIs are not diffable until all three are fixed.**
   ***Placement note:*** *"blocking Step 9, not Step 8" is **Red Team's recommendation**, from its
   twelfth review — **it is not a Human Lead ruling** and is recorded here as the recommendation it is.
   The Human Lead has not ruled on where it blocks.*

**Control defects, carried** *(`0063` §3)*
7. `compare_halves()` cannot fail; four sub-interval ratios are outside every control; the `_DERIVED`
   block is write-only; the covering qualifier exists in five wordings and the `analytics-engineer` pair
   carries one clause of it; `LEGITIMATE` disarms nothing while two registers say it does; seven smaller
   items including **the regenerator never running the phrase half**; and DF-3's closed-form window in a
   completed brief.

**Reported, not reconciled** — `CLAUDE.md`
8. Robustness survival **792 (A) against 791 (B)**, from a `τ_pull` restriction A states and B does not.
9. **The two sampling-width conventions**: arm a divides by the floor endpoint's own bootstrap CI, arm b
   by the CI of the under-the-rule point estimate. **The spec fixes neither.**

## 5. Verification standing at the time of drafting

| Control | State |
| :--- | :--- |
| `src/check_surfaces.py` | **PASS** — negative, phrase and positive halves, seven surfaces |
| `src/step7_regenerate_derived.py` | **PASS** — 84 target paths, 30 ratio rows, both halves compared |
| `src/step7_floor_extremes.py` | **11/11 CONFIRMED, 0 REFUTED** |
| Dual-implementation diff | both pairs byte-identical apart from `name:` |
| API calls, this entire chain | **zero** |

---

## 6. For the Human Lead to complete

> **Step 7 gate — liveness rule. APPROVED.**
>
> **Approved by:** the Human Lead  **Date:** 2026-08-13
>
> **The rule approved is ALT-BROAD as stated in §1**, with the bounds in §2 and **the residual in §4
> published rather than resolved.**
>
> **Conditions: NONE. The approval is unconditional.** The §4 residual is open and publishes with the
> result; it is not a condition on this gate and does not gate Step 8.
>
> *Item 6, the unspecified bootstrap, is carried as **Red Team's recommended placement** — blocking Step
> 9, not Step 8. **The Human Lead has not ruled on that placement**, and approving this gate does not
> rule on it.*

**Recorded as a decision at `decisions/0064-step7-gate-approved.md`**, and the gate checklist in
`decisions/README.md` is ticked. **Step 8 may launch.**
