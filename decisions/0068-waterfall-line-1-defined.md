# Decision 0068 — waterfall line 1 is 220,107; and a survey of everything else Step 8 names without defining

| | |
| :--- | :--- |
| **Decision** | **Waterfall line 1 is the S1-completer population: 220,107 pairs.** Lines 2 and 3 follow from it. **No instance chooses a base.** §2 is a **survey, reported and NOT resolved**, of every other place Step 8 names a count, population or operation without defining it at the point of use. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 read-back; instance A found line 1 |
| **Status** | Closed as to line 1. **§2 is open and is the Human Lead's.** |

---

## 1. Line 1

**The spec named no base, and four defensible readings sit on disk:** 2,900,762 (the frame
cross-product), 278,452 (any S1-or-S2 record on a frame show), 274,741 (any S1 record), **220,107**
(`pool_completers`). **Lines 1, 2 and 3 all moved with the choice.**

**Two faithful instances would have reported different waterfalls on an identical table** — which is
precisely what the fixed filter order exists to prevent, **one position upstream of where that fix
reached.**

**Ruled: 220,107, the population the study is defined over** — user-show pairs whose user completed
season 1. **Line 2 is line 1 less the `L2 = 1` shows; line 3 is line 2 less the pairs failing the S1
completion rule.**

**Not resolved by this ruling:** instance A measured that applying D11 at position 3 **as Step 1
requires** gives **220,103** — 167 in-frame records carry `watched_at ≥ τ_pull` and
`src/step2_build_frame.py` never touches the timestamp column. **The base is 220,107 as published;
whether D11 moves it is a separate open question.**

## 2. The survey — reported, not resolved

**Everything below is a place Step 8 refers to a count, population or operation without defining it at
the point of use. Nothing here is decided.**

### 2a. One correct answer — the record already fixes it; the spec just does not say so where it is used

| # | The line | What is undefined | Where the answer is |
| :-- | :--- | :--- | :--- |
| 1 | *"the 3,440 Started-and-left pairs completing at any point before `τ_pull`"* | **which population** | `0034` §3 measured it on the amendment's **uncensored estimation sample (128,099)**, and Step 14 calls it a **floor** for that reason. **It is not the count on Step 8's population.** Both arms flagged it |
| 2 | *"Expect 703 liveness exclusions at position 6"* | **the denominator** | **APPLY = 196,654**, the position-5 output. The bullet gives the numerator and the position but never the `n` the reader needs to check it |
| 3 | *"outcome states are mutually exclusive and sum to the sample"* | **which sample** | the **post-position-7 row set**. "The sample" appears nowhere else in the step |
| 4 | *"distinct episodes never exceed season length"* | whether it is a **data check or a code check** | Step 8's own set-membership bullet says **`\|D\| ≤ L` holds by construction** under set membership. **The `A ⊆ A_H` invariant is labelled a code check and this one is not** — and the two instances diverged here, A calling four of six true-by-construction and B calling all six |
| 5 | *"report the **share** … and its **share of all Started-and-left**"* (D3′) | **which Started-and-left, on which population, at which arm** | the arm's own population at `τ2`; D3′ is already required to run per arm with its own cleared count |
| 6 | *"the aggregate line above says 97.6% of pairs survive censoring"* | **there is no such line above** | the right-censoring bullet requires two lines and states no percentage. The figure is imported from `0030`/`0033` and never restated where it is used |
| 7 | the liveness silence test's **`>` vs `≥`** | strict or non-strict at `τ1` | the rule says *"no insertion instant **after** `τ1`"* — strict. **Determinable from the rule text**; the spec never says it in the step that applies it |

### 2b. Needs a ruling — the record does not fix it

| # | The line | The question |
| :-- | :--- | :--- |
| 8 | *"Include per row: … discovery channel"* | **324 of 5,694 users are in BOTH channels** (instance B). A single-valued column is not well-defined. Precedence, a multi-valued field, or a both-channels category? |
| 9 | *"Retain `action` as a column — Step 13 has an arm that needs it"* | **`action` is record-level; the row is a pair** (instance B). Which record's action, or what aggregation? Step 13's arm cannot be built until this is answered |
| 10 | *"Negative-lag report (D2), split by which term of the `max()` binds"* | **168 pairs have BOTH terms binding** (instance B) and the split as written is binary. Ties go where? |
| 11 | *"per outcome — pairs whose entire S2 evidence was dropped, reported as a **share of Never started**"* | **which Never started** — position-5 (33,373) or the retained post-liveness set (32,769)? The two differ by exactly the never-started exclusions, and the choice changes the reported share |
| 12 | **DERIV is required by Step 9 and Step 8b and no Step 8 position produces it** | DERIV is Step 5 line 4 less D10; **none of line 4's three restrictions is a Step 8 position**. Does Step 8 emit DERIV, or does Step 9 rebuild it? Instance A says Step 8 as written emits APPLY only; instance B says DERIV rebuilds to 147,370 to the row. **Reported as a divergence, not reconciled** |
| 13 | **D4 has no count anywhere in Step 8** | Step 9 must bound it and Step 8b reserves a slot for it. Does Step 8 produce it? |
| 14 | the liveness silence test's **`τ_pull` evidence scope** | whether insertion evidence is restricted to `≤ τ_pull`. **This is already a live divergence** — it produced the reported-not-reconciled **792 (A) against 791 (B)** at Step 7, and Step 8 inherits it unstated |
| 15 | **the censoring-order discrepancy** *(already on the Human Lead's list)* | `0033`'s table reproduces on the **position-3** output (97.6 / 98.0 / 97.5 / 96.0, 89.7% at `W = 213`) and **not** on the position-4 output the mandated order requires (97.40 / 97.8 / 97.4 / 95.9, 89.5%). The documented **10.3% loss becomes 10.5%** |

**Two of these — 12 and 14 — are places where the two instances have already diverged or would.** The
rest are places where they *could*, which is the same thing one run later.
