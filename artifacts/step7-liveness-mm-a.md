# Step 7 — Liveness rule, rerun on ALT-MATCHED (`decisions/0052`)

**Instance:** `mm_a` (namespace `a`), dual implementation.
**Status: GATE. This artifact proposes and measures. It adopts nothing and approves nothing.**
**API calls: 0.** The stored Step 5 calibration was read, never refitted (`0029`).

---

## 0. The rule as run

> **A user-show pair is NOT LIVE if and only if EITHER:**
> - **`|A| = 0` AND the account shows no insertion instant after `τ1 = ⟦T0⟧ + W × 24h`; OR**
> - **`|A| ≥ 1` AND the pair is NOT Continued AND the account shows no insertion instant after
>   `τ2 = ⟦T0⟧ + (W + H) × 24h`.**
>
> Otherwise it is live. **Each null is tested at the instant its own outcome is read.**

**Continued** is Step 1 §7 as amended by `0034`: `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`,
with `|A|` read at `τ1` and `A_H` read at `τ2`. Every boundary test is the half-open UTC-instant form
`watched_at < τ`. Distinct episodes are counted, never play events; the canonical timestamp of an
episode is the minimum `watched_at` across its records; membership is by **set** against `E2`.
Continued is the only state resting on positive evidence and is never excluded — asserted, not assumed
(0 Continued pairs removed on either population, at every arm).

`W = 108`, `H = 91`. Insertion instant is `np.interp(play_id, …)` against
`processed/step5/calibration.npz`; insertion time is not claimed `watched_at` (`0021`). The filter is
**pair-level, each pair anchored at its own `T0`** (`0034`); evidence is account-wide; **no user is
dropped wholesale** — on both populations exactly **one** account has all of its pairs excluded, and
the other 125 / 255 are excluded on one show and live on another.

**No pre-`τ1` requirement is reintroduced in any form** (`0040` §1, `0042` §3): the rule contains one
silence test per branch and no lower-side condition.

**Structural relation between the two tests, asserted in code.** `τ2 > τ1`, so silence after `τ1`
**implies** silence after `τ2`. The `τ2`-matched started-and-left branch is therefore strictly
**broader** than ALT-BROAD's `τ1` test — which is precisely why the count rises, and it is the
direction `0048` §3(b) predicted.

---

## 1. Populations — every figure below states which one produced it

The Step 5 waterfall was recomputed from `pair_revision5.csv` and **asserted** equal to the published
`201,900 / 178,165 / 155,131 / 152,126 / 128,099` before any figure was taken.

| | Definition | Pairs | Accounts |
| :--- | :--- | ---: | ---: |
| **DERIV** | Step 5 line 4 less D10. **Requires S2 evidence.** | **147,370** | 2,402 |
| **APPLY** | Step 5 line 1 less D10. **What Step 8 filters at position 6.** | **196,654** | 2,422 |

D10 is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, run at position 5, before liveness at position 6.
The `L2 = 1` exclusion was checked and is a no-op on both. The population was also asserted
bit-identical to the prior namespace-`a` ALT-BROAD run, so the reuse of its episode table, instants
and residual arrays is licensed rather than assumed; the instants were additionally **recomputed in
full** from `full_scan.npz` (27,656,813 records) and agree to **0 seconds**.

---

## 2. Exclusion counts — `0052` §1 CONFIRMED on APPLY; DERIV measured for the first time

| At `W = 108` | **DERIV** (147,370) | **APPLY** (196,654) |
| :--- | ---: | ---: |
| **Excluded pairs** | **188** | **793** |
| Excluded accounts | **126** | **256** |
| — never-started component | **0** (0 accounts) | **604** (191 accounts) |
| — started-and-left component | **188** (126 accounts) | **189** (127 accounts) |
| — continued component | 0, asserted | 0, asserted |
| Share of population | 0.1276% | 0.4032% |
| *(ALT-BROAD, superseded)* | *99* | *703* |

**`0052` §1's expectations are CONFIRMED exactly: APPLY 703 → 793, started-and-left 99 → 189.**
62 APPLY accounts contribute to both components.

**DERIV was recorded as unmeasured and is now measured: 188, all of it started-and-left, from 126
accounts.** The DERIV set was 99 under ALT-BROAD and 0 under ALT; it nearly doubles again here. The
dual control is informative on both populations, and more so than it was.

> ### DEFECT — the started-and-left component is **189 on APPLY but 188 on DERIV**, at the adopted arm
>
> Under ALT-BROAD the two populations agreed at `W = 108` (99 and 99) and diverged only at the top
> arm. **Under ALT-MATCHED they diverge at the adopted arm itself.** Any figure quoted as "the
> started-and-left component" without its population is now wrong for one of the two populations at
> the headline setting. This is `0046` §0's standing rule biting one arm earlier than before, and it
> is the specific thing `0048` §5's unlabelled series got wrong.

**How the rule selects.** ALT-BROAD's single funnel — *NOT Continued, then silent* — **does not
describe ALT-MATCHED**, because the rule is a **disjunction of two branches with different
thresholds**. Reporting it as one funnel would be a reproducibility defect.

| Branch, on **APPLY** = 196,654 | Pairs |
| :--- | ---: |
| never started (`\|A\| = 0`) | 33,373 |
| … **and silent after `τ1`** → **excluded** | **604** |
| started and left (`\|A\| ≥ 1` ∧ ¬Continued) | 19,141 |
| … **and silent after `τ2`** → **excluded** | **189** |
| *(counterfactual: the same branch tested at `τ1`, i.e. ALT-BROAD)* | *99* |

On **DERIV** = 147,370: never started 9,145 → **0** excluded; started and left 16,843 → **188**
excluded (99 under the `τ1` test). ALT-BROAD's `196,654 → 52,514 → 703` decomposition is superseded
for this rule; the corresponding totals are silent-after-`τ1` **1,355** and silent-after-`τ2`
**2,025** on APPLY, but neither is a stage of this rule.

**Rule comparison at `W = 108`:**

| | DERIV | APPLY |
| :--- | ---: | ---: |
| PF-LIMIT (silence at `τ1` alone) | 751 | 1,355 |
| ALT (silent@`τ1` ∧ `\|A\| = 0`) | 0 | 604 |
| ALT-BROAD (silent@`τ1` ∧ ¬Continued) | 99 | 703 |
| **ALT-MATCHED (adopted)** | **188** | **793** |
| Confirmed continuers a `τ1`-silence rule would delete | 652 | 652 |
| Confirmed continuers a `τ2`-silence rule would delete | **1,019** | **1,025** |

The last row is the reason the state conjunct cannot be dropped: matching the silence test to `τ2`
makes an unconditional silence rule **57% more destructive** of positively-evidenced continuers.

**The exclusion set is not "the pairs with no S2 record anywhere."** APPLY holds 23,260 such pairs;
604 are excluded and **22,656 stay live**; and **189 excluded pairs do hold S2 records**. Subset does
not hold, equality does not hold, and any downstream check asserting either will fail on correct data.

---

## 3. The three outcome shares, under the rule and against no filter

**DERIV — 147,370 pairs, 2,402 accounts**

| | Never started | Continued | Started and left | Pairs |
| :--- | ---: | ---: | ---: | ---: |
| No liveness filter | 9,145 — **6.2055%** | 121,382 — **82.3655%** | 16,843 — **11.4291%** | 147,370 |
| **Under the rule** | 9,145 — **6.2134%** | 121,382 — **82.4707%** | 16,655 — **11.3159%** | 147,182 |
| **Movement** | **+0.0079 pp** | **+0.1052 pp** | **−0.1131 pp** | −188 |

**APPLY — 196,654 pairs, 2,422 accounts**

| | Never started | Continued | Started and left | Pairs |
| :--- | ---: | ---: | ---: | ---: |
| No liveness filter | 33,373 — **16.9704%** | 144,140 — **73.2962%** | 19,141 — **9.7333%** | 196,654 |
| **Under the rule** | 32,769 — **16.7307%** | 144,140 — **73.5930%** | 18,952 — **9.6762%** | 195,861 |
| **Movement** | **−0.2397 pp** | **+0.2968 pp** | **−0.0571 pp** | −793 |

Movements are differenced from unrounded shares; differencing the rounded ones moves the last digit.
All six paired account-clustered 95% intervals exclude zero — on APPLY, never-started
`[−0.2921, −0.1937]`, continued `[+0.2461, +0.3509]`, started-and-left `[−0.0749, −0.0400]`.

**The sign of the never-started movement is population-dependent, as `0045` §4.1 requires be carried:
UP 0.0079 pp on DERIV, DOWN 0.2397 pp on APPLY.** On DERIV the never-started share **rises while no
never-started pair is excluded** — pure denominator movement, and the clearest available illustration
of why an endpoint must be computed on the same population as its estimand (§5 below).

The started-and-left movement roughly **doubles** on both populations against ALT-BROAD
(APPLY −0.0156 → −0.0571 pp; DERIV −0.0595 → −0.1131 pp), which is the rule change doing exactly what
it was adopted to do.

---

## 4. The bounds. **State which population each one bounds.**

**Every endpoint below is on the POSITION-5 population** — APPLY 196,654, DERIV 147,370 — with a
**fixed denominator**, in exact integer arithmetic. **This is not the population the published shares
in §3 sit on**, which is post-liveness (195,861 / 147,182). See §5.

What the rule leaves unresolved, per excluded pair:

- **never-started component** (604 APPLY, 0 DERIV) — recorded Never started; `|A| = 0` is a **null**.
  Truth may be any of the three. It can only *leave* the never-started numerator and only *enter* the
  other two.
- **started-and-left component** (189 APPLY, 188 DERIV) — recorded Started and left; `|A| ≥ 1` is
  **observed**, so the pair **did** start. Truth is Started-and-left or Continued. It can only *leave*
  the started-and-left numerator and only *enter* Continued. **It cannot reach the never-started
  numerator.**

### 4.1 Bound 1 — never started. **UNCHANGED. `0052` §1 CONFIRMED.**

**APPLY, denominator 196,654:**

| | Numerator | Share |
| :--- | ---: | ---: |
| **Floor** — all 604 excluded never-started nulls in truth started | 32,769 | **16.6633%** |
| **Ceiling** — all 604 are true declines | 33,373 | **16.9704%** |
| **Width** | 604 | **0.3071 pp** |

**Identical to ALT and to ALT-BROAD, and the reason is structural: the rule change moved only
started-and-left pairs into the exclusion set, and both endpoints depend on `k_ns` alone.** The
ceiling equals the unfiltered never-started share **as an identity**, because the ceiling numerator
*is* the unfiltered numerator over the unfiltered denominator.

**`0046` §4's phrasing of that identity remains false and gets worse.** "Returning every excluded pair
as a decliner reproduces the unfiltered population exactly" would now give **17.3737%**, which is
**not attainable**, because 189 of the exclusions are observed to have started. Do not carry that
sentence into Step 9.

On **DERIV** the bound is **degenerate: [6.2055%, 6.2055%]**, width 0, because the never-started
component is empty. The dual control on this bound is `x = x` on DERIV; the informative comparison is
on APPLY.

### 4.2 Bound 2 — started and left, **over ALL 793 exclusions, on one denominator**

**APPLY, denominator 196,654:**

| | Numerator | Share |
| :--- | ---: | ---: |
| **Floor** — all 189 excluded started-and-left nulls in truth continued | 18,952 | **9.6372%** |
| **Ceiling** — all 189 are true exits **and** all 604 never-started nulls in truth started and left | 19,745 | **10.0405%** |
| **Width** | 793 | **0.4032 pp** |

**This is the repair `0052` §4 called for, not a widening.** `0052` §4 identified **18,952 / 9.6373%**
as the floor ALT-BROAD's bound failed to cover, and noted that carrying it would have made the fifth
consecutive bound with a non-covering endpoint. Under ALT-MATCHED the 90 pairs concerned are
**excluded**, so 18,952 **is** the floor numerator and the endpoint covers the case by construction.
The ALT-BROAD interval `[9.6830%, 10.0405%]` is superseded.

> **Small record defect.** `0052` §4 gives the floor as **9.6373%**. `18,952 / 196,654 = 9.637231%`,
> which rounds to **9.6372%**. The numerator is confirmed exactly; only the fourth digit is wrong, and
> the gap it states against the published 9.6830% is **0.0458 pp**, not 0.0457 pp. Cosmetic, recorded
> because the entry states it to four decimals and Step 9 will copy it.

**Conditional sub-interval, LABELLED and NOT the bound: [9.6372%, 9.7333%], width 0.0961 pp** — the
started-and-left share *conditional on every excluded never-started null being a true decline*. Its
ceiling does not cover the case in which an excluded never-started null in truth started and left,
which is a case the filter exists to allow for. Note it is now **0.0961 pp wide, not `0049`'s
0.0503 pp**; Step 9 must not carry the old number.

On **DERIV**, denominator 147,370: **[11.3015%, 11.4291%]**, width **0.1276 pp**. Because the
never-started component is empty there, the bound and its conditional sub-interval **coincide** on
DERIV — a second place where the dual control degenerates on that population.

### 4.3 Bound 3 — **Continued has a ceiling**

**Any *excluded* pair may in truth be Continued**, and no exclusion can leave Continued, so the
ceiling is the unfiltered count plus the **whole** exclusion set.

| | APPLY (196,654) | DERIV (147,370) |
| :--- | ---: | ---: |
| **Floor** — no excluded pair is in truth Continued | 144,140 — **73.2962%** | 121,382 — **82.3655%** |
| **Ceiling** — all exclusions are in truth Continued | 144,933 — **73.6995%** | 121,570 — **82.4930%** |
| Width | 793 — 0.4032 pp | 188 — 0.1276 pp |

**`0052` §2 is confirmed on its own terms:** ALT-BROAD's Continued ceiling `(144,140 + 703) / 196,654`
recomputes to **73.6537%** exactly, so `0051`'s V7 correction was indeed wrong to call it "on no
population." **Under the adopted rule it moves to 73.6995%**, because the exclusion set is larger.
Step 9 must publish 73.6995%, not 73.6537% and not the point 73.2962%.

### 4.4 **ALL THREE CEILINGS AND THEIR SUM**

**On APPLY, 196,654 — the population Step 8 filters:**

| Ceiling | Numerator | Share |
| :--- | ---: | ---: |
| Never started | 33,373 | **16.9704%** |
| Started and left | 19,745 | **10.0405%** |
| **Continued** | 144,933 | **73.6995%** |
| **SUM** | | **100.7104%** |
| **Excess over 100** | 1,397 pairs | **0.7104 pp** |

**On DERIV, 147,370:** 6.2055% + 11.4291% + 82.4930% = **100.1276%**, excess **0.1276 pp**
(188 pairs).

**The mechanism, stated rather than left as a total.** The excluded set is counted once in **every
ceiling it could belong to**, so the three are **alternative worst cases over one set, not
simultaneous ones**. Each of the 604 never-started exclusions sits in **all three** ceiling numerators
— its recorded state, plus both states it could flow into — and contributes **2** to the excess. Each
of the 189 started-and-left exclusions sits in **two** — its recorded state and Continued — and
contributes **1**. The excess is exactly `2 × 604 + 189 = 1,397` pairs, which is 0.7104% of 196,654,
and the arithmetic was checked as integers rather than inferred from the percentages.

*(The same identity reproduces `0052` §2's figure: under ALT-BROAD `2 × 604 + 99 = 1,307`, and
`1,307 / 196,654 = 0.6646 pp`, so `16.9704 + 10.0405 + 73.6537 = 100.6646%` is right.)*

**No two ceilings are attainable together.** Three corner resolutions were verified to partition the
population exactly, in integer arithmetic:

| Resolution | Never started | Continued | Started and left | Sums to N |
| :--- | ---: | ---: | ---: | :---: |
| all 604 started and left; all 189 are true exits | **16.6633%** floor | 73.2962% | **10.0405%** ceiling | ✓ |
| all 604 are true declines; all 189 in truth continued | **16.9704%** ceiling | 73.3924% | **9.6372%** floor | ✓ |
| all 793 in truth continued | 16.6633% floor | **73.6995%** ceiling | 9.6372% floor | ✓ |

Every endpoint of every bound is attainable, so all three bounds are tight.

### 4.5 Scale: the bounds against sampling error

Account-clustered 95% widths on APPLY, from the bootstrap in §8. **A bound is an identified set, not
a confidence interval**; this is only how much of the endpoint is noise.

| | Bound width | Sampling width | Ratio |
| :--- | ---: | ---: | ---: |
| Never started | 0.3071 pp | 1.0910 pp | **0.28×** |
| Started and left | 0.4032 pp | 0.7621 pp | **0.53×** |
| Continued | 0.4032 pp | 1.4068 pp | **0.29×** |

Ratios are computed on the **operative** bounds, not on the conditional sub-interval —
`0052` §6 records an arm that used the sub-interval and understated the ratio by 7.5×. The
started-and-left ratio rises from 0.47× under ALT-BROAD to **0.53×** here.

---

## 5. **Which population each bound bounds — `0052` §7, confirmed and WORSENED on DERIV**

**The bounds are on the position-5 population. The published shares are post-liveness.** They are
different populations and this artifact states so at every point of use.

| | Population | Never started | Started and left | Continued |
| :--- | ---: | ---: | ---: | ---: |
| **APPLY bound** | 196,654 | [16.6633, 16.9704] | [9.6372, 10.0405] | [73.2962, 73.6995] |
| **APPLY published share** | 195,861 | 16.7307 | 9.6762 | 73.5930 |
| contained? | | **yes** | **yes** | **yes** |
| **DERIV bound** | 147,370 | [6.2055, 6.2055] | [11.3015, 11.4291] | [82.3655, 82.4930] |
| **DERIV published share** | 147,182 | **6.2134** | 11.3159 | 82.4707 |
| contained? | | **NO** | yes | yes |

**On APPLY containment holds by arithmetic accident. On DERIV it fails outright**, exactly as
`0052` §7 records — **and the failure is larger under the adopted rule.** The DERIV never-started
point estimate sits **0.0079 pp outside** its own degenerate identified set, against 0.0042 pp under
ALT-BROAD: **the rule change nearly doubles the gap**, because it removes 188 rows from the
denominator instead of 99 while removing none from the numerator.

This is a **stated limitation, not a repair.** It is not a defect in the rule; it is what happens when
an identified set on one population is printed beside a share on another. Step 9 must name which
population each bound bounds.

---

## 6. Waterfall — line 6 outcome-conditional; monotone decrease STRICT on both populations

| Position | DERIV | APPLY |
| :--- | ---: | ---: |
| 4 — contamination exclusion | 152,126 | 201,900 |
| 5 — right-censoring D10 | **147,370** (−4,756) | **196,654** (−5,246) |
| 6 — **liveness (OUTCOME-CONDITIONAL)** | **147,182** (−188) | **195,861** (−793) |
| — of which never started | 0 | 604 |
| — of which started and left | 188 | 189 |
| — of which continued | 0 | 0 |

**Line 6 must be published with that split.** **Both** disjuncts of the rule contain a position-7
outcome predicate — `|A| = 0` in one, `NOT Continued` in the other — so the removed count cannot be
stated without reference to outcome assignment, and it removes rows from two outcome states.

**Ordering.** Outcome assignment is evaluated before liveness applies. That is permitted, and it was
**checked here rather than asserted**: the surviving state counts were computed both ways — assign
then filter, and filter then assign — and are identical on both populations. Both are **row-local
predicates on the position-5 output and commute exactly**, and `0029`'s ordering rationale concerns
**per-filter sample size**, which cannot reach position 7 because **outcome assignment removes no
rows**: positions 1–6 are filters, position 7 is an annotation.

**Monotone decrease is STRICT on BOTH populations at every arm from 38 to 213** (188 and 793 at the
adopted arm, and non-zero everywhere). **Keep the `>=` coding.** Strictness is a fact about this pull
date and this rule, not a theorem — it was non-strict on DERIV under ALT and strict under ALT-BROAD —
and the invariant must not encode a property of one rule.

---

## 7. `W`-coupling per arm, started-and-left component reported separately

**D10 contains `W`, so the censored population differs per arm. Both readings are given and each names
itself** (`0047`). The mandated grid is `0027`'s 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213; 60, 100,
125 and 180 are extra and are marked off-grid.

### 7.1 D10 RE-DERIVED AT EACH ARM — the operative reading

| `W` | Grid | DERIV pop | **DERIV excl.** | ns | sl | APPLY pop | **APPLY excl.** | ns | **sl** | APPLY accts | *(ALT-BROAD)* |
| ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | ✓ | 147,685 | **119** | 0 | 119 | 197,007 | **604** | 485 | **119** | 204 | *537* |
| 46 | ✓ | 147,685 | **127** | 0 | 127 | 197,007 | **621** | 494 | **127** | 211 | *550* |
| 60 | | 147,685 | 143 | 0 | 143 | 197,007 | 670 | 527 | 143 | 219 | *592* |
| 77 | ✓ | 147,685 | **159** | 0 | 159 | 197,007 | **713** | 554 | **159** | 227 | *633* |
| 91 | ✓ | 147,685 | **179** | 0 | 179 | 197,007 | **754** | 575 | **179** | 245 | *664* |
| 100 | | 147,518 | 185 | 0 | 185 | 196,829 | 778 | 592 | 186 | 253 | *686* |
| 107 | ✓ | 147,384 | **188** | 0 | 188 | 196,674 | **793** | 603 | **190** | 257 | *701* |
| **108** | ✓ | **147,370** | **188** | **0** | **188** | **196,654** | **793** | **604** | **189** | **256** | *703* |
| 125 | | 147,049 | 209 | 0 | 209 | 196,276 | 835 | 625 | 210 | 273 | *736* |
| 150 | ✓ | 146,602 | **213** | 0 | 213 | 195,689 | **878** | 664 | **214** | 276 | *789* |
| 180 | | 145,845 | 232 | 0 | 232 | 194,617 | 917 | 683 | 234 | 286 | *818* |
| 213 | ✓ | 144,852 | **235** | 0 | 235 | 193,270 | **952** | 716 | **236** | 296 | *864* |

**Mandated grid, APPLY: 604 / 621 / 713 / 754 / 793 / 793 / 878 / 952.**
**Started-and-left component, APPLY: 119 / 127 / 159 / 179 / 190 / 189 / 214 / 236.**
**Mandated grid, DERIV: 119 / 127 / 159 / 179 / 188 / 188 / 213 / 235, all of it started-and-left.**
*(ALT-BROAD's 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864 and 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148
are reproduced exactly as the superseded comparator, and must not be ordered under the adopted rule.)*

**The `W`-coupling changes materially and Step 13's characterisation must change with it.** The whole
rule couples **1.58×** across the grid on APPLY (604 → 952) against ALT-BROAD's 1.61×. But the
started-and-left component couples **1.98×**, **not the 2.85× the record carries** for ALT-BROAD. The
component still grows faster than the rule it sits in, but the gap narrows from *nearly double* to
about 25% — because ALT-MATCHED already captures at the low arms most of what ALT-BROAD only reached
at the high ones.

> **Two readings of the per-arm table that will otherwise look like bugs.**
> **(a) The APPLY started-and-left component is NOT monotone in `W`:** it is **190 at `W = 107` and
> 189 at `W = 108`.** Two effects run against each other — D10 re-derivation shrinks the population as
> `W` rises (196,674 → 196,654, 20 pairs), while a later `τ1` moves pairs between outcome states. The
> total is flat across those two arms (793 / 793) with the components trading 603/190 → 604/189.
> **(b) DERIV and APPLY disagree on the started-and-left component at most arms** (188 vs 190 at 107,
> 188 vs 189 at 108, 213 vs 214 at 150, 235 vs 236 at 213), where under ALT-BROAD they agreed
> everywhere except the top arm. An unlabelled series is now wrong in more places.

### 7.2 D10 FROZEN AT `W = 108` — the other reading, so the two are not confused

| `W` | 38 | 46 | 77 | 91 | 107 | 108 | 125 | 150 | 180 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, total | 598 | 614 | 706 | 742 | 790 | 793 | 874 | **990** | 1,192 | **1,466** |
| APPLY, **ns component** | 484 | 493 | 553 | 574 | 603 | 604 | **632** | **684** | **753** | **881** |
| APPLY, sl component | 114 | 121 | 153 | 168 | 187 | 189 | 242 | 306 | 439 | 585 |
| DERIV, total (all sl) | 114 | 121 | 153 | 168 | 186 | 188 | 240 | 298 | 420 | 560 |

**The never-started component under the frozen reading is rule-invariant and reproduces `0047` §5 /
`0050` exactly: 632 / 684 / 753 / 881 at `W` = 125 / 150 / 180 / 213.** **The frozen TOTALS are not:
they are 874 / 990 / 1,192 / 1,466 under ALT-MATCHED, against `0050`'s ALT-BROAD 746 / 823 / 918 /
1,117**, which `task-sheet.md` Step 7 and Step 13 currently carry as operative. Only `W` = 150 and 213
are in the mandated grid; 125 and 180 are off-grid and are included here only so the record's figures
can be reproduced with their arms attached.

---

## 8. Bootstrap — **design stated explicitly**, because the spec does not fix it

`0052` §6 records that the two arms used different designs last time and were not diffable. This one
is stated in full and both objects are reported.

| | |
| :--- | :--- |
| **Unit** | **account.** Accounts resampled with replacement; **all** of an account's pairs travel with it, because liveness evidence is account-wide even though the filter is pair-level |
| **Replicates** | **B = 4,000** |
| **Seed** | **20260813**, `numpy.random.default_rng` — the same seed and B as every prior namespace-`a` Step 7 run, so rows are comparable line for line |
| **Interval** | percentile, 2.5 / 97.5 |
| **Reported** | **LEVELS *and* PAIRED MOVEMENTS, both, labelled.** Neither is presented as *the* design |

**Levels** are the three shares under the rule and under no filter, each with its own CI. **Movements**
are the paired delta (rule minus no filter) computed **inside** each replicate; that is the right
object for "did the filter move the headline", because the two settings share the resampled accounts
and the difference is far less variable than either level. On APPLY the never-started level is
1.09 pp wide while its movement is 0.098 pp wide — a factor of 11, which is why the choice matters and
why both are printed.

**APPLY, under the rule:** never started 16.7307% `[16.1830, 17.2739]`; continued 73.5930%
`[72.8944, 74.3012]`; started and left 9.6762% `[9.3097, 10.0718]`.
**DERIV, under the rule:** 6.2134% `[5.8481, 6.6134]`; 82.4707% `[81.8265, 83.0766]`; 11.3159%
`[10.8375, 11.8097]`.

**A bound is an identified set, not a confidence interval.** The bootstrap says only how much of each
endpoint is sampling noise. All six bound endpoints were bootstrapped, each on the position-5
denominator of its own replicate; the ratios are in §4.5.

---

## 9. The channel — `0052` §3's is CLOSED; the analogue is empty by construction

**What a channel is, stated so the measurement is checkable.** ALT-BROAD's warrant is that a pair
silent after `τ1` can produce no evidence in `[τ1, τ2)`, the window the Continued test reads, and so
is scored "left" **by construction**. `0052` §1 observes the warrant holds identically for a pair
silent after `τ1 + ε` for any `ε < H`. The channel is therefore **the pairs the rule leaves LIVE whose
last insertion falls strictly between the instant the silence test uses and the instant the outcome is
read.**

**ALT-BROAD's channel, reproduced exactly on APPLY:**

| | Pairs |
| :--- | ---: |
| Not Continued | 52,514 |
| Live only by the `τ1` conjunct | 51,811 |
| **Channel — last insertion inside `(τ1, τ2)`** | **297** |
| — never started | 207 |
| — **started and left** | **90** |

Last insertion in the channel sits at a median **51.4 days** past `τ1`, p90 85.1, max 90.9 — filling
the window. `0050` §4's pooled 70.3% and **`0052` §3's corrected 52.4% both reproduce to the digit**,
and `0052` §3's correction is confirmed to be the right one: the 207 never-started pairs are **not**
in the gap, because their null is `|A| = 0` read at `τ1` and every one of them has an insertion after
`τ1` — exactly what `0021` licenses. On the implicated set alone ALT-BROAD closed 99 of 189.

**ALT-MATCHED closes the remaining 90: 90 of 90, 100%, 0 still live.** On DERIV the same measurement
gives 89 of 89.

**The analogous channel under ALT-MATCHED is 0 on both populations, and it is empty BY CONSTRUCTION,
not by this pull date.** The silence instant and the reading instant now **coincide** for each null,
so the open interval between them is degenerate — there is no `ε` for the continuity argument to run
over. Measured at 0 for both branches on both populations.

**What the rule now trusts on the thinnest evidence** — live pairs whose only post-reading-instant
insertion is barely past it. On APPLY: 2 never-started pairs within one day of `τ1` and 9 within a
week; 2 started-and-left pairs within one day of `τ2` and 28 within a week. These are live and their
nulls are trusted; `0021`'s sufficient condition is met at the instant that matters for each.

### 9.1 A NEW channel the rule change opens, on the other side — **report this**

**D10 is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`. At `W = 108` that is `T0 + 199d ≤ τ_pull`, and
`τ2 = T0 + 199d` — so `τ2 ≤ τ_pull` with EQUALITY attainable.** A pair at the censoring boundary has a
**zero-length window** in which the insertion that would prove its liveness could be observed. The
`τ1` test never has this problem: `τ_pull − τ1 ≥ H = 91 days` at every arm.

| APPLY | |
| :--- | ---: |
| Pairs with a **zero-length** post-`τ2` observation window | **20** |
| … post-`τ2` window under 7 days | 123 |
| … post-`τ2` window under 30 days | 688 |
| **Excluded started-and-left pairs with a zero-length window** | **2** |
| … with under 7 days | 6 |
| … with under 30 days | 18 |

On DERIV: 17 / 102 / 556 and **2** / 6 / 17. **Two excluded pairs on each population are excluded by
construction** — no observation window existed in which they could have been found live. It is 2 of
793, so it does not move any figure in this artifact, but it is a channel the rule change **opens**
and it did not exist under ALT-BROAD. It is reported, not repaired.

### 9.2 The tension with `0048` §9's gloss on gate `0021` — **for the Human Lead, not for this instance**

**`0021`'s own text** is *"any record inserted **after the window closed** proves the account was
alive."* For the started-and-left null the reading window closes at `τ2`, so **ALT-MATCHED is faithful
to that text** — arguably more so than ALT-BROAD, which tested a `τ2`-read state against a `τ1` window.

**But `0048` §9 GLOSSED `0021` as "insertion after `τ1` ⟹ live", as a sufficient condition.** Under
that gloss, **90 of the 793 APPLY exclusions contradict a gate**: they are declared NOT LIVE despite
showing an insertion after `τ1`. On DERIV it is **89 of 188 — 47.3% of the whole exclusion set.**

**Under ALT-BROAD this count was 0 on both populations**, so the two readings of `0021` never had to
be told apart. **They do now, and the DERIV share makes it material rather than marginal.** Which
reading governs is a gate question. This instance measures it and does not settle it.

---

## 10. Margins and residual robustness of the NEW exclusion set

The rule compares an **interpolated** instant against a threshold; if the curve reads **early**, a
live account is scored silent and the pair is **falsely excluded**. The residual *distribution* is a
property of the curve and the records and does not change with the rule — the stored figures stand
(22.6768% of dated records claim a `watched_at` later than their calibrated instant, median gap
0.0205 d; fit-family residual median |r| 0.0195 d, 91.5% within a day; held-out median lag 0.0026 d).
**What changes is the set it is applied to**, so the tests are re-run.

**Margin = each pair's own threshold minus its last instant** — `τ1` for the never-started branch,
**`τ2`** for the started-and-left branch. An exclusion survives any residual correction smaller than
its own margin.

| | DERIV (188) | APPLY (793) |
| :--- | ---: | ---: |
| min | 0.1333 d | **0.0137 d** |
| p25 / **median** / p75 | 46.6 / **98.8** / 174.9 d | 72.2 / **168.1** / 320.5 d |
| never-started component, median (vs `τ1`) | — | 202.5 d |
| started-and-left component, median (vs **`τ2`**) | **98.8 d** | **97.6 d** |
| within 0.0195 d | 0 | 1 |
| within 1 d | 2 | 3 |
| within 7 d | 12 | 24 |
| within 30 d | 35 | 85 |

**The started-and-left margins are ~91 days larger than under ALT-BROAD**, because they are measured
against `τ2`. The set is correspondingly more robust, not less.

**A. Uniform shift `+δ`** (a positive `δ` corrects a curve reading early, so it can only remove
exclusions). APPLY: 793 → 792 at δ = 0.0195 d, 790 at 1 d, **769 at 7 d (97.0% retained)**, 708 at
30 d, 477 at 124.6 d. DERIV: 188 → 176 at 7 d, 153 at 30 d, 78 at 124.6 d.

**B. Non-parametric correction — the strongest test, needing no magnitude assumption.** A genuine
record cannot be inserted before it was watched, so the true instant is at least
`max(interp(max rid), max dated watched_at ≤ τ_pull)`.

| | DERIV | APPLY |
| :--- | ---: | ---: |
| Pairs whose account instant moved later | 59,501 | 79,370 |
| Median move where moved | 0.026 d | 0.026 d |
| **Exclusions surviving** | **188 of 188 — 100.00%** | **792 of 793 — 99.87%** |
| Lost | 0 | 1 (never-started) |
| **New exclusions created** | **0** | **0** |

**The exclusion set is more stable under plausible residual than ALT-BROAD's was** (which lost 2 of 99
on DERIV and 3 of 703 on APPLY). The never-started component — the component the Step 9 never-started
bound rests on — moves 604 → 603, shifting the floor by roughly 0.0005 pp against a width of
0.3071 pp.

**Where the residual cannot be measured directly.** Of the 793 APPLY exclusions, **575 sit on accounts
whose own last record is an import `watch`**, whose `watched_at` carries no information about
insertion time; only **218** sit on accounts whose last record is a checkin or scrobble, where the
residual at exactly the point the rule reads is directly measurable. For the 575, A and B above are
the whole of the evidence. On DERIV the split is 110 import / 78 fit-family.

**The calibration clamp is no longer inert, and this is a change.** Under ALT-BROAD the clamp was
inert because the clamp time `2026-08-10T20:48Z` exceeds **every** `τ1` the rule can read, so 0 of 703
exclusions sat on a clamped account. **That argument does not transfer to `τ2`, which can run to
`τ_pull` — later than the clamp time.** Measured: 6 pairs on clamped accounts have `τ2` past the clamp
time, and **1 excluded pair on each population now sits on a clamped account** (a started-and-left
exclusion). One pair of 793 is immaterial to every figure here; the *argument* that retired the clamp
concern is what has stopped working, and Step 14 should carry that rather than the conclusion.

---

## 11. Judgement calls the spec does not settle, stated

1. **"After `τ`" is read strictly**, so silence is `max(instant) ≤ τ`; a tie does not prove liveness.
   The rule now reads two thresholds, so ties were checked at **both**: **0 pairs** on either
   population lie within one second of `τ1` or of `τ2`. Non-load-bearing.
2. **`max(instant)` is computed as `interp(max rid)`**, valid because `np.interp` is monotone
   non-decreasing in `rid`; cross-checked against the stored per-account sequence at 0 seconds.
3. **Insertion evidence is account-wide** (all shows, all seasons) per `0021`; the **test** is
   pair-level per `0034`.
4. **The exclusion set is reported as a disjunction of two branches, not as a funnel.** ALT-BROAD's
   `population → NOT Continued → silent` decomposition does not describe a rule whose branches use
   different thresholds, and reporting one would not be reproducible against an arm that reports two.
5. **Bootstrap design** — account cluster, B = 4,000, seed 20260813, percentile interval, **levels and
   paired movements both reported.** The spec fixes none of these; §8 states all of them so the diff
   is meaningful.
6. **Bound 2 is published on the unconditional estimand**, with the "over the started-and-left
   exclusions only" interval demoted to a labelled conditional sub-interval.
7. **Arms.** `0027`'s grid plus 60, 100, 125 and 180; the last two only so `0047` §5's frozen figures
   can be reproduced with their arms attached. Marked off-grid everywhere.
8. **The calibration residual is measured in-sample on the fit family**, because refitting is
   forbidden; this understates the error and the stored held-out figures are quoted beside it.
9. **The stability tests in §10 are run at `W = 108` only.** Arm-wide residual stability is not
   claimed. (`0052` §9 records this as closable and already in Step 14.)

---

## 12. Defects found in the record — reported, not reconciled

- **D-1. The started-and-left component is 189 on APPLY and 188 on DERIV at the ADOPTED arm.** Under
  ALT-BROAD the two agreed at `W = 108`. Any unlabelled "the started-and-left component" figure is now
  wrong for one population at the headline setting. It also disagrees at `W` = 107, 150 and 213.
- **D-2. `0052` §4's floor is stated as 9.6373%; it is 9.6372%** (`18,952 / 196,654 = 9.637231%`), and
  the gap it quotes against 9.6830% is 0.0458 pp, not 0.0457 pp. Numerator confirmed exactly.
- **D-3. `task-sheet.md` Step 7 and Step 13 carry ALT-BROAD's per-arm series as operative** — 537 /
  550 / 633 / 664 / 701 / 703 / 789 / 864, the component 52 / … / 148, the 2.85× factor, the
  1.61× coupling, and the frozen totals 746 / 823 / 918 / 1,117. **Under the adopted rule these are
  604 / 621 / 713 / 754 / 793 / 793 / 878 / 952; the component 119 / … / 236; 1.98×; 1.58×; and 874 /
  990 / 1,192 / 1,466.** A Step 13 instance following the file computes ALT-BROAD.
- **D-4. `task-sheet.md` Step 7's decomposition line — `196,654 → 52,514 → 703` — does not describe
  ALT-MATCHED at all.** The rule has two branches with different thresholds; there is no single funnel.
- **D-5. `task-sheet.md` Step 9's three-ceilings line is stale in two places.** Started-and-left
  ceiling is unchanged at 10.0405%, but **Continued's ceiling moves 73.6537% → 73.6995%** and **the sum
  moves 100.6646% → 100.7104%**. Its conditional sub-interval **[9.6830%, 9.7333%], width 0.0503 pp,
  becomes [9.6372%, 9.7333%], width 0.0961 pp**, and its started-and-left bound floor moves
  9.6830% → 9.6372%.
- **D-6. `0048` §9's gloss on `0021` and `0021`'s own text now select different rules.** See §9.2:
  the gloss makes 90 APPLY / 89 DERIV exclusions contradict a gate; the text does not. Under
  ALT-BROAD the count was 0 and the ambiguity was invisible.
- **D-7. The clamp argument in the record is now unsound**, though its conclusion survives at 1 pair.
  See §10.
- **D-8. This instance's own definition file was snapshotted before `0052`** and carries ALT-BROAD
  throughout — the `|A| = 0`-conjunct framing, 703 / 99, the per-arm 537–864 series and the 2.85×
  factor. **The on-disk `task-sheet.md` and `decisions/` were treated as authoritative**, and the
  launch prompt carried the correct rule, so nothing was run on the stale text. Recorded because a
  dual pair launched from cached definitions could diverge for a reason that is an artifact of the
  record — this is `0052` §5's propagation failure #12 in a different dimension.

---

## 13. What this gate still cannot establish

- **That the rule is right.** Its warrant is an argument, not a measurement. The biconditional gap
  narrows but does not close: `0021` licenses *"insertion after the window closed ⟹ live"* as a
  **sufficient** condition; the rule is a **biconditional**, and the converse is asserted.
  **ALT-MATCHED makes the argument tighter on one side and opens a question on the other** (§9.2).
- **That Step 8's position-6 population is the one reconstructed here.** APPLY was built from the
  Step 5 pair table, not through Step 8's positions 1–5. **793 on APPLY is an expected value for the
  Step 8 diff; a mismatch is a POPULATION defect first** (`0047` §7) — check the frame join, the
  `L2 = 1` exclusion and the censoring before suspecting the rule.
- **That the `τ2` silence test is observable for every pair it is applied to.** For 20 APPLY pairs it
  is not, and 2 of them are excluded (§9.1).
- **Arm-wide residual stability** (§11.9).
- **That two implementations agree.** That is the Human Lead's diff against the other instance, which
  this one has not seen and has not looked for.

---

## 14. Files

| Path | Contents |
| :--- | :--- |
| `artifacts/step7-liveness-mm-a.json` | every figure in this document, machine-readable |
| `artifacts/step7-liveness-mm-a.md` | this document |
| `processed/step7/mm_a/` | population, instants, arms, bounds, checks, channel, margins, bootstrap |
| `src/step7_mm_a_1_population.py` … `_9_deliver.py` | the nine stages, in order |

No usernames, user IDs or individual watch histories appear in `artifacts/`. Row-level masks and the
per-account instant arrays stay in `processed/`.

**Gate. Nothing here is adopted. Returned to the Human Lead.**
