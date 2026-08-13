> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — liveness rule, rerun on the rule adopted at `decisions/0046`

**Instance `a`. GATE, dual implementation. This artifact adopts nothing and approves nothing.**
Machine-readable twin: `artifacts/step7-liveness-alt-a.json`. Row-level detail:
`processed/step7/alt2_a/`. **Zero API calls.** The play-`id` calibration at
`processed/step5/calibration.npz` was **read, never refitted** — and the reused instant sequence
from the earlier run was cross-checked against an independent recomputation from that stored
curve, max absolute difference **0.0 seconds**.

**Every figure below states its population** (`0046` §0). There are two and they differ by
construction:

| | Definition | Pairs | Accounts |
| :--- | :--- | ---: | ---: |
| **DERIV** | Step 5 waterfall line 4 (152,126) less D10. **Requires S2 evidence.** | **147,370** | 2,402 |
| **APPLY** | Step 5 waterfall line 1 (201,900) less D10. **What Step 8 filters at position 6.** | **196,654** | 2,422 |

The Step 5 waterfall was **recomputed and asserted**, not quoted: `201,900 → 178,165 → 155,131 →
152,126 → 128,099`, all five lines equal to the published figures. D10 removes 4,756 from line 4
and 5,246 from line 1. Both population sizes assert exactly. The `L2 = 1` exclusion is a no-op on
both, asserted rather than assumed.

---

## 1. The rule

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant
> after that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND `|A| = 0`. Otherwise it is live.**

- **`|A| = 0` is Step 1 §7's Never-started condition** — the distinct S2 episodes whose number is
  in `E2` and whose canonical timestamp satisfies `watched_at < τ1` — **not "no S2 evidence at
  all."** The two readings select different sets; §5 below measures both, because the difference
  turns out to matter for what `0046` says about its own numbers.
- **Insertion time, not claimed `watched_at`** (`0021`). Evidence is **account-wide**, across all
  shows and seasons. The rule asks only whether *any* instant falls after `τ1`, which is
  `max(instant) > τ1` — no gap, no percentile, no sequence statistic is used or needed.
- **Pair-level, anchored at `τ1`** (`0034`). `τ2` plays no part. On APPLY, all **191** accounts
  with an excluded pair also hold live pairs; **no account is dropped wholesale.**
- **No pre-`τ1` requirement is imposed, in any form.**
- **No free parameter of its own.** The exclusion set is fully determined by `W`.

---

## 2. Exclusion counts — 0 on DERIV, 604 on APPLY, both confirmed

**At `W = 108`:**

| Population | Pairs | Excluded | Expected by `0046` | Verdict |
| :--- | ---: | ---: | ---: | :--- |
| **DERIV** | 147,370 | **0** | 0 | confirmed |
| **APPLY** | 196,654 | **604** | 604 | confirmed |

**Per `W` arm.** D10 contains `W` and runs at position 5, before liveness, so the population is
re-derived at each arm. **That reading reproduces `0046` §3's table exactly**, which settles what
that table meant.

| `W` | 38 | 46 | 60 | 77 | 91 | 100 | 107 | **108** | 125 | 150 | 180 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **DERIV excluded** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 |
| **APPLY excluded** | 485 | 494 | 527 | 554 | 575 | 592 | 603 | **604** | 625 | 664 | 683 | 716 |
| APPLY population | 197,007 | 197,007 | 197,007 | 197,007 | 197,007 | 196,829 | 196,674 | **196,654** | 196,276 | 195,689 | 194,617 | 193,270 |
| *PF-LIMIT would have excluded* | *833* | *861* | *959* | *1,073* | *1,281* | *1,327* | *1,348* | ***1,355*** | *1,373* | *1,443* | *1,519* | *1,670* |

**A reading the arm table must carry.** Freezing D10 at the adopted `W = 108` instead of
re-deriving it gives **different counts above 108** — 632 at `W = 125`, 684 at 150, 753 at 180,
**881 at 213** against 716. The two readings are within one pair of each other at and below 108
and diverge by 23% at 213, so **an arm table that does not say which reading it is, is not
reproducible.** Both are in the JSON.

**At `W = 108`, PF-LIMIT on APPLY = 1,355 = 604 + 751**, and the 751 split 652 confirmed
continuers / 99 started-and-left, all with `|A| ≥ 1`. The adopted rule reaches none of them.
This reproduces `0046` §2 on the population `0046` §2 names.

---

## 3. The three outcome shares, under the rule and against no filter at all

Never-started is tested at `τ1`; Continued at `τ2 = ⟦T0⟧ + (W + H) × 24h` on `A_H` (`0034`).
**Continued is a 199-day statement and never-started a 108-day statement; they are not measured
alike.** Intervals are account-clustered percentile bootstrap, B = 4,000, seed 20260813, accounts
resampled with replacement and all their pairs travelling with them.

### DERIV — 147,370 pairs, 2,402 accounts

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| **No filter at all** | 9,145 · **6.2055%** | 121,382 · **82.3655%** | 16,843 · **11.4291%** |
| **Under the adopted rule** | 9,145 · **6.2055%** | 121,382 · **82.3655%** | 16,843 · **11.4291%** |
| Delta | **0.0000 pp** | **0.0000 pp** | **0.0000 pp** |
| Clustered 95% CI (either) | [5.8409, 6.6035] | [81.7202, 82.9647] | [10.9438, 11.9195] |

**The two rows are the same row.** The exclusion set is empty, so on the derivation population
the rule is not a filter at all.

### APPLY — 196,654 pairs, 2,422 accounts

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| **No filter at all** (196,654) | 33,373 · **16.9704%** | 144,140 · **73.2962%** | 19,141 · **9.7333%** |
| CI | [16.4097, 17.5131] | [72.5926, 74.0162] | [9.3685, 10.1318] |
| **Under the adopted rule** (196,050) | 32,769 · **16.7146%** | 144,140 · **73.5221%** | 19,141 · **9.7633%** |
| CI | [16.1656, 17.2581] | [72.8231, 74.2325] | [9.3983, 10.1624] |
| **Paired delta** | **−0.2558 pp** [−0.3083, −0.2086] | **+0.2258 pp** [+0.1844, +0.2728] | **+0.0300 pp** [+0.0243, +0.0362] |

All three paired intervals exclude zero. **That is not a behavioural finding: the Continued and
Started-and-left numerators are byte-identical under the two settings — 144,140 and 19,141 — so
every movement is the denominator falling by 604 and the never-started numerator falling with
it.** The rule is a pure denominator-and-numerator operation on one state, which is exactly what
"the excluded set is a subset of never-started" means.

---

## 4. The Step 9 liveness bound, and the ceiling identity

**On APPLY: floor 16.714614%, ceiling 16.970415%, width 0.2558 pp.** This reproduces `0046` §4's
**[16.7146%, 16.9704%]**.

**The ceiling equals the unfiltered never-started share as an identity, and this run tests it
rather than asserting it** — by exact integer cross-multiplication, not a float comparison:
`(32,769 + 604) × 196,654 == 33,373 × (196,050 + 604)`. **True.** It holds because the excluded
set is a subset of never-started, so returning every excluded pair as a decliner reproduces the
unfiltered population exactly, numerator and denominator alike. **Both endpoints are attainable**:
the floor is the case where every excluded pair would have started, the ceiling the case where
none would.

**On DERIV: floor = ceiling = 6.2055%, width 0.** There is nothing to bound.

**Set against sampling error, on APPLY:** the bound is **0.2558 pp** wide against an
account-clustered 95% interval of **1.0924 pp** on the share it bounds — the bound is **23.4% of
the sampling width**, not a rounding error and not the dominant uncertainty. Ceiling with its own
interval: 16.9704% [16.4097, 17.5131].

---

## 5. The waterfall, with line 6 outcome-conditional

Filter order `0029`: 4 contamination → 5 right-censoring → 6 liveness → 7 outcome assignment.

| | DERIV | APPLY |
| :--- | ---: | ---: |
| Position 4 output (contamination exclusion) | 152,126 | 201,900 |
| Position 5 output (right-censoring, D10) | 147,370 | 196,654 |
| **Position 6 output (liveness)** | **147,370** | **196,050** |
| Position 6 removed | **0** | **604** |

> **Line 6 is OUTCOME-CONDITIONAL and must be reported as such** (`0046` §5). The rule's second
> conjunct *is* an outcome condition, so the line-6 count cannot be stated without reference to
> position 7. Every pair it removes is scored Never started; it removes nothing from Continued or
> Started-and-left. Two faithful instances that label this line as an ordinary filter will diverge
> on the waterfall while agreeing on every share.

**Monotone decrease.** **Non-strict on DERIV** — 147,370 → 147,370, the exclusion set is empty.
**Strict on APPLY** — 196,654 → 196,050. **The Step 8 invariant "filter counts decrease
monotonically" must be coded `>=`, not `>`,** or it fails on a correct DERIV run.

---

## 6. The two weaknesses `0046` records, tested

### 6.1 "Step 7's own dual run may not exercise the rule at all" — **CONFIRMED on DERIV**

The exclusion set is empty on DERIV at **every arm from 38 to 213**. On the derivation population
this step's diff is **`0 = 0`**, and no implementation difference in the rule could show up in it.
Said plainly: **if the two instances only compare DERIV numbers, this gate's dual control proves
nothing about the rule.**

**The diff is not vacuous overall.** Both arms can be diffed on APPLY: the 604, the twelve-arm
table, the three shares, the bound endpoints, and the waterfall line. Those are the figures worth
diffing.

### 6.2 "The rule is first exercised at Step 8" — what this gate can and cannot establish

**Can:** that the rule is well defined and computable with no free parameter of its own; that its
exclusion set is 0 / 604 at `W = 108` and rises monotonically with `W` on APPLY; that its
exclusions are all Never started, which is what makes the Step 9 ceiling an identity with both
endpoints attainable; and that the headline moves 0.2558 pp, which is 23.4% of the clustered
sampling width.

**Cannot:** (i) that **Step 8's position-6 population is the one reconstructed here.** APPLY was
rebuilt from Step 5 outputs; Step 8 builds it through positions 1–5 of its own pipeline, and any
difference at any position moves the 604. (ii) that two independent implementations of the rule
agree, because on DERIV there is nothing to disagree about. (iii) anything about the rule's
behaviour on pairs Step 8 scores differently from this reconstruction — **the second conjunct is
an outcome, so the rule's exclusion set is only as stable as the outcome assignment feeding it.**

**Recommendation.** Carry the 604, the arm table and the outcome-conditional line 6 into the Step 8
diff as expected values, and treat a Step 8 position-6 count other than 604 as a **population**
defect until proven otherwise, not a liveness defect.

---

## 7. Two findings against `decisions/0046` itself

### Finding 1 — "the 604 are exactly the pairs with no S2 record anywhere" is **refuted as stated**

`0046` §1 and §3 both say it. Measured on APPLY:

| | Pairs |
| :--- | ---: |
| Pairs with no S2 record anywhere (Step 5 flag) | **23,260** |
| Pairs with zero distinct in-`E2` S2 episodes | 23,260 (the same set) |
| Pairs with `\|A\| = 0` at `τ1` | 33,373 |
| **Excluded by the rule** | **604** |
| No-S2-record pairs that stay **LIVE** | **22,656** |

The 604 are a **subset** of the no-S2-record pairs — verified, no excluded pair carries an S2
record — but they are not that set. **22,656 pairs with no S2 record anywhere remain live**,
because their accounts insert records after `τ1`. The correct statement is: **the 604 are exactly
those no-S2-record pairs whose account shows no insertion instant after `τ1`.**

**Why it matters beyond wording.** As written, `0046` credits the second conjunct with the whole
selection. In fact the second conjunct narrows 196,654 → 33,373 and **the first conjunct does the
rest, 33,373 → 604.** A reader who takes §1 at face value would expect the rule to be `W`-invariant
— and the arm table shows it is not.

### Finding 2 — the DERIV zero is **confirmed as a count** and **not forced by construction**

`0046` §1: *"The DERIV zero is forced by construction — line 4 requires S2 evidence, so no line-4
pair can have `|A| = 0` and no S2 record."*

The count is 0 at every arm tested. **The reason given is a non-sequitur, and it is the exact
conflation §5 of the same entry warns against:** the second conjunct is `|A| = 0`, not "no S2
record". **9,145 DERIV pairs — 6.2055% — satisfy `|A| = 0`.** What produces the zero is the
**first** conjunct: every one of those 9,145 accounts inserts a record after `τ1`. The margins:

| Days from `τ1` to the account's last insertion instant, over the 9,145 | min | p1 | p5 | median |
| :--- | ---: | ---: | ---: | ---: |
| | **23.9** | 189.3 | 433.2 | 2,183.9 |

One pair sits within 30 days of tripping the rule and three within 90. That is an empirical zero
with a margin, not a theorem.

**And D10 is load-bearing for it.** With right-censoring suppressed, **four line-4 pairs satisfy
both conjuncts at every arm from 38 to 213** — pairs Step 5 flags as having S2 records but whose
records leave no distinct in-`E2` episode after the §3.2 membership drop and D11, so `|A| = 0` at
every `W`. **They are exactly the case `0046` says cannot exist.** D10 removes them at position 5,
before liveness at position 6, so the **operative** count is 0. **The DERIV zero is a fact about
this pull date, not a property of the rule.** A later pull, a different `H`, or any change to D10
could make it 4 — and then Step 7's dual diff would stop being `0 = 0` on DERIV.

---

## 8. Judgement calls this spec does not settle

1. **The tie at `τ1`.** "After `τ1`" is read strictly, so NOT LIVE requires `max instant ≤ τ1`;
   an instant landing exactly on `τ1` does not prove liveness. **Measured non-load-bearing: zero
   pairs on either population have their last instant within one second of `τ1`.**
2. **Only the last instant matters.** The rule asks whether *any* instant falls after `τ1`, which
   is `max(instant) > τ1`. No gap statistic is computed anywhere in this run.
3. **Per-arm D10 in the arm table**, because D10 contains `W`. Both readings reported; they differ
   above `W = 108`.
4. **"No S2 record anywhere" has two readings** — Step 5's `has_S2` flag, and zero distinct in-`E2`
   episodes after D11. They coincide on APPLY at 23,260 and differ on line 1 before D10, 23,735
   against 23,739. **The four-pair difference is load-bearing for finding 2** and is reported
   rather than smoothed.
5. **The unfiltered comparator** is the position-5 output with position 6 skipped, on the same
   population — not the pre-censoring line.
6. **Bootstrap design** is not specified: B = 4,000, seed 20260813, account-clustered, matching the
   earlier Step 7 runs so the rows are comparable.
7. **Arm list** is `0046` §3's eight arms plus 60, 100, 125 and 180 to fill the Step 13 span
   (`0027`).
8. **APPLY here is a reconstruction** of Step 8's position-6 input from Step 5 outputs, not Step 8's
   own table.

---

## 9. Reproduction

| Stage | Script | Output |
| :--- | :--- | :--- |
| 1 populations | `src/step7_alt2_a_1_population.py` | `processed/step7/alt2_a/population.{npz,json}` |
| 2 S2 episode table | `src/step7_alt2_a_2_episodes.py` | `processed/step7/alt2_a/episodes_line1.{npz,json}` |
| 3 insertion instants | `src/step7_alt2_a_3_instants.py` | `processed/step7/alt2_a/last_instant.{npz,json}` |
| 4 arms, shares, bound | `src/step7_alt2_a_4_arms.py` | `processed/step7/alt2_a/arms.json`, `masks_W108.npz` |
| 5 clustered intervals | `src/step7_alt2_a_5_boot.py` | `processed/step7/alt2_a/bootstrap.json` |
| 6 checks and waterfall | `src/step7_alt2_a_6_checks.py` | `processed/step7/alt2_a/checks.json` |
| 7 artifact | `src/step7_alt2_a_7_deliver.py` | `artifacts/step7-liveness-alt-a.json` |

**This is a gate. Nothing here is adopted, and Step 8 does not launch on it.**
