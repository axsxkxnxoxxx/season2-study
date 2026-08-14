# Step 7 — liveness rule — GATE APPROVAL, **DRAFT, UNSIGNED**

> **THIS IS A DRAFT PREPARED AT THE HUMAN LEAD'S REQUEST. IT IS NOT AN APPROVAL.**
>
> `CLAUDE.md`: *"Only the Human Lead approves, in writing, in this session"* and *"an agent never
> records its own approval."* Nothing downstream of this gate runs until the Human Lead states the
> approval themselves. **Step 8 has not launched and does not launch on this document.**
>
> The gate checklist in `decisions/README.md` is **unchanged** and still reads OPEN. It is not updated
> by anyone but the Human Lead.

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

**Approval, if given, is given with these open and published, not around them.**

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

> **Step 7 gate — liveness rule. Approved / Not approved: ______**
>
> **Approved by:** ______________  **Date:** ______________
>
> **The rule approved is ALT-BROAD as stated in §1**, with the bounds in §2 and **the residual in §4
> published rather than resolved.**
>
> **Conditions, if any:** ______________
>
> *(Item 6 is a Step 9 precondition and is not waived by approving Step 8.)*

**On approval the Human Lead — not an agent — updates `decisions/README.md`'s gate checklist and records
the approval as a decision entry.** Step 8 launches only after that.
