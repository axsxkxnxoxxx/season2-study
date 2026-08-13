# Step 7 — liveness threshold, instance b4 (rerun on the reopened gate)

**PROPOSED, NOT ADOPTED.** This is gate 4 of 5. This instance produces the artifact and stops. It does
not adopt its own proposal and it does not begin Step 8. Dual implementation: the Human Lead diffs this
against the other arm. **Zero API calls.**

| | |
| :--- | :--- |
| **Instance** | `data-scientist-b`, namespace `b4` |
| **Date** | 2026-08-13 |
| **Spec** | `decisions/0040` (gate reopened), `0038` (frozen spec), `0037`, `0036` §2, `0029`, `0026`, `0025`, `0021`, `0011`; `artifacts/step1-outcome-definition.md` §6 and D10 |
| **Proposed threshold** | **1,293 days**, account-clustered 95% interval **[790, 2200]**, B = 2,000 |
| **Data** | `processed/step5/full_scan.npz` (27,656,813 records), `processed/step5/calibration.npz` (read, not refitted), `processed/step5/pair_revision5.csv` |
| **Chart** | `artifacts/step7-liveness-b4-gap-distribution.png` |
| **Machine-readable** | `artifacts/step7-liveness-b4.json` |
| **Row-level** | `processed/step7/b4/` — never leaves this machine |

---

## 1. The headline, and the one sentence that explains it

**The threshold is 1,293 days, not 632.** The number did not move because the data changed. It moved
because `0040` put the open-ended gaps *inside* the reference distribution, and they now consume most
of the 1% quota before the measured-gap test gets to run.

| | Superseded run (`0039`) | This run |
| :--- | ---: | ---: |
| Derivation population | 152,126 (uncensored) | **147,370** (152,126 less D10) |
| Reference set | 129,630 measured gaps only | **129,218 = 128,467 measured + 751 open-ended as `+∞`** |
| Raw 99th percentile | 631.8031 d | **1292.0284 d** |
| **Threshold, ceiling per `0025`** | 632 d | **1,293 d** |
| Pairs excluded by a measured gap | 1,276 | **531** |
| Pairs excluded as open-ended | 4,246 | **751** |
| Pairs excluded for no pre-`τ1` evidence | 18,250 | **0 — they are LIVE (`0021`)** |
| **Total not live** | 23,772 (15.63% of 152,126) | **1,282 (0.87% of 147,370)** |

**The filter went from removing one pair in six to removing one in a hundred and fifteen.**

---

## 2. Waterfall assertion and the post-D10 count

Asserted in code, `src/step7_b4_bracket.py::build_population`, and the run aborts if it fails:

**201,900 → 178,165 → 155,131 → 152,126 → 128,099** ✓

The reference line is **line 4, the 152,126** (`0038` §2). D10 is then applied on top, per `0040` §2,
because liveness runs at Step 8 position 6 and right-censoring at position 5 (`0029`).

**D10:** retain iff `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, `H = 91`, `τ_pull = 2026-08-11T00:00:00Z`.
At `W = 108` the bound is 199 days.

| | Pairs |
| :--- | ---: |
| Waterfall line 4 | 152,126 |
| Removed by D10 | **4,756** (3.13%) |
| **POST-CENSORING COUNT — derivation and application population** | **147,370** |

Removed by class: 1,163 measured-gap, 3,495 open-ended, 98 no-pre-`τ1`. **D10 removes 82.3% of the
open-ended bucket** — that bucket was mostly right-censoring, not silence, exactly as `0038` §7 and
`task-sheet.md` recorded.

**Pre-D10 the three classes reproduce the frozen run exactly — 129,630 / 4,246 / 18,250 — so the
divergence from `0039` is entirely attributable to the two spec changes and not to the pipeline.**

### Post-D10 population by class, `W = 108`

| Class | Pairs | Disposition |
| :--- | ---: | :--- |
| Measured bracketing gap | **128,467** | tested against the threshold |
| No insertion instant after `τ1` — open-ended, `+∞` | **751** | not live; fails any finite threshold on its own |
| No insertion instant at or before `τ1` | **18,152** | **LIVE per `0021`** — `0036` §2.3(ii) withdrawn |
| **Total** | **147,370** | |
| *of which the reference set (the "extended set")* | *129,218* | |

---

## 3. The two changes, checked rather than assumed

### 3.1 `0036` §2.3(ii) is withdrawn and the pairs are returned

18,152 post-D10 pairs have no insertion instant at or before `τ1`. Every one of them has instants
*after* `τ1` — the sweep contains **zero accounts with no instants and a minimum of three gaps per
account**, which this run reconfirms. `0021`, approved gate 2 of 5, rules that **any record inserted
after the window closed proves the account was alive**. They are live.

### 3.2 The open-ended share after D10

`0040` §2 predicted roughly **0.685%** and asked for it to be checked, not assumed.

**Measured: 751 / 129,218 = 0.5812%.** Below 1%, so the conclusion holds, but **the predicted figure is
not reproduced and the difference has a cause.** `0040`'s 894 / 130,524 was obtained by subtracting the
3,352 pairs whose `τ1` is past the pull instant from the uncensored extended set. That is a subset of
what D10 removes: D10 also removes pairs whose `τ1` is *before* the pull instant but within `H` of it,
and it removes 1,163 measured-gap pairs the subtraction leaves in. The full rule gives 751 / 129,218.

---

## 4. The reference distribution

One gap per pair (`0038` §3), on the post-D10 population, bracketing `τ1` (`0036` §2).

| Quantile | Pooled gaps (all 25,862,249) | Measured bracketing gaps (128,467) | Extended set (129,218) |
| :--- | ---: | ---: | ---: |
| median | 0.0000007 d | 1.8830 d | 1.8948 d |
| 75th | 0.0251 d | 6.9167 d | 7.0177 d |
| 90th | 0.4060 d | 43.10 d | 48.96 d |
| **99th** | **3.4432 d** | **631.8031 d** | **1292.0284 d** |
| max finite | 3196.27 d | 3196.27 d | 3196.27 d |

**The length bias `0037` §1 identified is reconfirmed.** The bracketing median is 2.7 million times the
pooled median, and **36.98%** of bracketing gaps exceed the pooled 99th percentile — 1% by construction
for a uniformly drawn gap.

> **`0040` §5's contradiction, resolved.** The superseded run's two artifacts published **34.1%** and
> **36.96%** for this quantity and both blamed "a different population." It is neither a population
> difference nor a computational one: it is the **comparator**. Against the raw pooled 99th (3.4432 d)
> the share is **36.977%**; against its ceiling (4 d) it is **34.184%**. Both are stated here so the
> next reader does not have to rediscover it.

**Gap unit** (`0037` §4, exact): every record's insertion instant, sorted ascending, runs of exactly
equal instants collapsed — exact equality only, no rounding at any resolution — then consecutive
differences. 27,656,813 records → **25,864,798 distinct instants** (1,792,015 collapsed, 6.48%), median
**7,812 gaps per account**, minimum 3. The insertion instant is the stored Step 5 isotonic play-`id`
curve, **read and not refitted**.

---

## 5. The proposed threshold

**99th percentile of the extended bracketing-gap set, rounded UP (`0025`).**

| | |
| :--- | ---: |
| Raw 99th percentile | **1292.0284 d** |
| **Threshold (ceiling)** | **1,293 days** |
| **Account-clustered 95% interval** | **[790, 2200] days** |
| Bootstrap replicates | **2,000** (accounts resampled with replacement; seed 20260813 + W, recorded in the JSON) |
| Replicates whose 99th was infinite | 0.25% (5 of 2,000) |
| i.i.d. pair-level interval, for contrast only | [1210, 1405] |
| **Precision the i.i.d. interval overstates** | **7.2×** |

**Never report it bare.** Same treatment as `W = 108 ± 18`.

**Why clustering is not optional here.** 34.53% of measured-gap pairs share their bracketing gap value
with another pair, largest tie group **298** — and the 99th percentile sits inside a plateau of **156
identical values**, which is why the measured-only 99th is `631.8031044554` both before and after D10
despite 1,163 pairs being removed. More sharply: **the 531 gap-test exclusions come from 43 accounts and
the 751 open-ended from 166 accounts — 205 distinct accounts out of the 2,402 in the population.** An i.i.d.
interval treats 1,282 exclusions as 1,282 independent draws when they are roughly 209.

The ceiling rounding is not cosmetic: it spares **12 pairs** that sit between 1292.0284 and 1293.

---

## 6. The rule

> A user-show pair is **live** unless its bracketing gap is at or above the threshold.
>
> For a pair with clock start `T0` and window `W`, let `τ1 = ⟦T0⟧ + W × 24h`. On that pair's
> **account** — the whole sweep, every show and movie, not only the show under study — take the
> distinct insertion instants. Let `b` be the last instant **at or before** `τ1` and `f` the first
> instant **strictly after** `τ1`. The bracketing gap is `f − b`, a continuous instant difference in
> days.
>
> 1. **Both exist:** the pair is **not live** iff `f − b ≥ threshold`.
> 2. **No instant after `τ1`:** the gap is open-ended, `+∞`, and the pair is **not live**.
> 3. **No instant at or before `τ1`:** the pair is **LIVE** (`0021`).
>
> **Liveness is a pair-level filter, never a user-level one.** Evidence is account-wide but `τ1` is
> pair-specific, so one account can be live for one show and not for another. **No user is ever dropped
> wholesale on a liveness test.** Liveness is anchored at `τ1`; `τ2` plays no part in it (`0034`).
> Applied at Step 8 position 6, after right-censoring at position 5.

### Realised rate

| Denominator | Pairs | Rate |
| :--- | ---: | ---: |
| **The extended set — what the percentile was taken on** | 1,282 / 129,218 | **0.9921%** |
| Measured-gap pairs only | 531 / 128,467 | **0.4133%** |
| All post-D10 pairs | 1,282 / 147,370 | **0.8699%** |

**Live: 146,088 of 147,370 = 99.130%.**

The stated rate is delivered on the set the percentile was taken on, and only on that set. That is the
whole content of `0038` §2.1.

---

## 7. Two things stated plainly, because `0038` requires it

### 7.1 The quota property

**Taking the percentile on the distribution the test applies to sets the level by the exclusion rate,
not by any feature of the data.** Choosing `p` mechanically fixes the exclusion rate at `100 − p`% of
the reference set. It is a quota, not a finding. Nothing about 1,293 days describes viewer behaviour;
it is the number at which exactly 1% of the reference set falls above.

**`0040` sharpens this rather than softening it.** Because open-ended gaps now sit inside the reference
set, they claim **751 of the 1,282-pair quota — 58.6% of it — before the gap test runs at all.** The
threshold's rise from 632 d to 1,293 d is a consequence of the quota shrinking, not of any gap getting
longer. Fold an automatically-excluded bucket into the reference and the tested bucket must give up
ground; that is arithmetic, not evidence.

`0036` §1's conservative-direction argument still points up but identifies no level. Per `0040` §3 it
is **not** cited for the edge-case branches: bias 2 concerns accounts that *stopped* logging, and the
returned 18,152 are accounts that *started late*.

### 7.2 The inertness — measured here, and no invariance claimed

`0040` §4 withdrew the 3.45% / 96.55% figures and the claim that they hold across every percentile,
which is arithmetically impossible. It also flagged 5.37% / 94.63% as predating both changes. **Both of
those are now wrong again, in the opposite direction.**

**Measured on this population at the adopted 99th percentile:**

| | Exclusions | Share |
| :--- | ---: | ---: |
| **Measured-gap test** | **531** | **41.42%** |
| **Edge case (i), open-ended** | **751** | **58.58%** |

The old finding was that the threshold did roughly one exclusion in twenty. **It now does two in five.**
The withdrawn edge case (ii) was 76.8% of the old filter's work; removing it left the threshold a much
larger share of a much smaller total.

**The share still moves with the percentile and no invariance is claimed:**

| Percentile | Threshold | Gap test | Open-ended | Gap-test share |
| :--- | ---: | ---: | ---: | ---: |
| 90th | 49 d | 12,165 | 751 | 94.19% |
| 95th | 147 d | 5,674 | 751 | 88.31% |
| 97.5th | 385 d | 2,472 | 751 | 76.70% |
| **99th — proposed** | **1,293 d** | **531** | **751** | **41.42%** |
| 99.5th | ∞ | 0 | 751 | 0.00% |
| 99.9th | ∞ | 0 | 751 | 0.00% |

---

## 8. Is edge case (i) still needed as a separate ruling?

`0040` §2 asked. **The answer is in two parts and only one of them is "no."**

**As an exclusion ruling: NO.** The open-ended share is 0.5812%, below 1%, so the extended-set 99th
percentile is finite (1,293 d) and **every open-ended gap fails it automatically.** No separate ruling
is required to exclude those 751 pairs.

**As a construction ruling: YES, and it is now load-bearing in a way it was not before.** Something must
say that an open-ended gap enters the reference set **as `+∞`** rather than being dropped from it.
That single choice — not the exclusion — is what moves the threshold from 632 d to 1,293 d and the
gap-test exclusions from 1,275 to 531.

**And the "no" has a boundary.** Above the **99.4188th** percentile the extended-set percentile is
itself infinite; the measured-gap test then excludes nobody and the rule degenerates into edge case (i)
alone. **The 99th is 0.42 percentile points from that cliff.** In the account-clustered bootstrap
**0.25% of replicates land past it at `W = 108`, and 2.80% at `W = 213`.** The finiteness that makes
the ruling unnecessary is a property of this population at this percentile, not a general one.

---

## 9. Step 13 — the threshold refitted per arm

`W` and the threshold are **not independent axes** (`0038` §6). Each arm re-censors under D10 with
`max(W, 91) + H`, so the arms do not share a denominator. `H = 91` is held constant throughout. Arms
cover `0027`'s union, 38 to 213.

| `W` | D10 bound | Post-D10 | Measured | Open-ended | Raw 99th | **Threshold** | Clustered 95% CI | Gap-test excl. | Open excl. | Realised (ext.) | Realised (all) | Gap-test share |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- | ---: | ---: | ---: | ---: | ---: |
| 38 | 182 | 147,685 | 128,122 | 348 | 715.45 | **716** | [591, 973] | 937 | 348 | 1.0002% | 0.8701% | 72.92% |
| 46 | 182 | 147,685 | 128,248 | 367 | 720.47 | **721** | [591, 982] | 892 | 367 | 0.9789% | 0.8525% | 70.85% |
| 77 | 182 | 147,685 | 128,606 | 519 | 884.85 | **885** | [632, 1293] | 760 | 519 | 0.9905% | 0.8660% | 59.42% |
| 91 | 182 | 147,685 | 128,592 | 706 | 1229.01 | **1,230** | [721, 1766] | 578 | 706 | 0.9931% | 0.8694% | 45.02% |
| 107 | 198 | 147,384 | 128,476 | 745 | 1286.52 | **1,287** | [787, 1766] | 544 | 745 | 0.9975% | 0.8746% | 42.20% |
| **108** | **199** | **147,370** | **128,467** | **751** | **1292.03** | **1,293** | **[790, 2200]** | **531** | **751** | **0.9921%** | **0.8699%** | **41.42%** |
| 150 | 241 | 146,602 | 128,079 | 779 | 1404.67 | **1,405** | [898, 2470] | 501 | 779 | 0.9933% | 0.8731% | 39.14% |
| 213 | 304 | 144,852 | 126,762 | 949 | 1653.42 | **1,654** | [1097, 2937] | 323 | 949 | 0.9960% | 0.8781% | 25.39% |

Bootstrap `B = 2,000` at the adopted arm and 1,000 at the others; all seeds recorded in the JSON.

**Three things to read off this table.**

1. **The coupling is strong and monotone: 716 → 1,654 days across the arms, a factor of 2.3.** A single
   frozen threshold would deliver its stated rate at exactly one arm.
2. **The realised rate is ~1% at every arm by construction.** That is the quota property visible as a
   flat column — it is not evidence the rule is stable.
3. **The gap test's share of the work collapses as `W` rises: 72.9% at `W = 38`, 25.4% at `W = 213`.**
   A later `τ1` runs off the end of more accounts' histories, so the open-ended bucket grows and the
   threshold's share of the exclusions falls. This is the strongest single argument against treating
   the threshold as a stable parameter of the data.

---

## 10. Input to `0040` §6 — is the threshold load-bearing?

Step 9 owns the headline; this is the Step 7 half of the answer.

| | Threshold | Not live | Share of population |
| :--- | ---: | ---: | ---: |
| Interval low | 790 d | 1,701 | 1.154% |
| **Point** | **1,293 d** | **1,282** | **0.870%** |
| Interval high | 2,200 d | 897 | 0.609% |

**Across an interval 1,410 days wide the exclusion set moves by 804 pairs — 0.55 percentage points of
the population.** For the headline to be sensitive to the threshold, those 804 pairs would have to
differ from the population by tens of percentage points in outcome mix. That is Step 9's measurement,
not this instance's, and `0040` §6 requires it to be made.

**Stated for the record: this instance sees no basis in Step 7's own numbers for preferring a published
threshold with an interval to `0040` §6's alternative — "the account has insertion evidence bracketing
`τ1`", with no free parameter.** That rule is the 751-pair open-ended exclusion alone, which is 58.6% of
what the full rule does. The remaining 41.4% costs one derived constant, one bootstrap interval 1,410
days wide, and the quota property. The choice is the Human Lead's.

---

## 11. Defects and open questions this run found

### 11.1 The derive/apply mismatch is only half closed — and it is measurable

`0038` §2.1 ranks "derivation and application populations must be identical" first. `0040` §2 closed the
D10 half of it. **The other half is still open and nothing in the record addresses it.**

The reference is **waterfall line 4 (152,126) less D10**. Step 8 applies liveness at position 6 to the
**analysis population (201,900) less D10**. Line 4 is a strict subset — it additionally requires S2
evidence, uncontaminated `T0`, and a non-postdated completing record.

**Measured, applying the proposed 1,293 d threshold to the population Step 8 will actually hand it:**

| | |
| :--- | ---: |
| Analysis population less D10 | 196,654 |
| Measured gap / open-ended / no-pre-`τ1` (live) | 156,711 / 1,355 / 38,588 |
| Not live | 2,279 (924 by gap, 1,355 open-ended) |
| **Realised rate vs the extended set** | **1.4418%** |
| Stated rate | 1.0000% |

**That is the same defect class `0038` §2.1 names — calibrate on one distribution, apply to another —
one step milder than the 2.28% it cites.** It is not repaired here because repairing it means either
re-deriving on the 201,900 (which `0038` §2 forbids: those lines carry contaminated `T0`, and `τ1` is
built from `T0`) or restricting Step 8's liveness filter to line 4 (which no decision authorises).
**Reported, not repaired.** Checked and clean: zero pairs in line 4 sit on an `L2 = 1` show, so Step 8
position 2 contributes no further mismatch.

### 11.2 Judgement calls the spec still does not settle

1. **Whether the 18,152 no-pre-`τ1` pairs belong in the reference distribution.** They are live and have
   no bracketing gap. **This is the largest remaining lever in the step.** Excluding them (V1, taken as
   primary because `0040`'s own `894 / 130,524` arithmetic frames the extended set as measured plus
   open-ended) gives **1,293 d**; entering them as 0 gives **975 d**.
2. **Whether the reference includes open-ended gaps as `+∞`** (V1, `0040` §2's direction) **or is
   restricted to measured gaps** (V2, `0039`'s basis, **632 d**). See §8.
3. **Comparator direction.** Not live iff gap **≥** threshold. `0025`'s reasoning implies at-or-above;
   no decision states it as an operator. Zero pairs sit exactly on 1,293 d, so it does not bite here.
4. **Quantile estimator.** R type-7 / numpy `linear`. The spec names a percentile, never an estimator.
   Type-7 reproduces the frozen run's 631.8031 exactly, which is the check that it is the same choice
   the superseded run made.
5. **`np.interp` clamps 6,956 records** outside the fitted `rid` range (1,862 below the first knot,
   5,094 above the last) to the endpoint instants. The curve is a required input and is not refitted, so
   this is reported, not repaired. `0040` §7 notes both arms of the superseded run resolved it
   identically **by chance**, and that it would have changed every downstream number otherwise.
6. **D10's comparison is written `≤`** and is applied as written, though every other boundary in the
   study is half-open (D13).
7. **Bootstrap endpoint convention.** 2.5th of the ceilinged replicate thresholds by `method='lower'`,
   97.5th by `method='higher'`, so the interval is not narrowed by interpolating between adjacent
   replicates. `B = 2,000` adopted arm, 1,000 elsewhere; seeds in the JSON.
8. **Which `W` arms Step 13 runs.** `0027` gives the union 38–213; the Step 7 summary in
   `task-sheet.md` says "46 to 107 plus 150 and 213". Eight arms are run to cover both readings.

**All eight are stated rather than resolved, per the gate's terms.** Items 1 and 2 together span
632 d to 1,293 d — wider than the bootstrap interval, and not a sampling question.

---

## 12. Reproduction

| Stage | Script | Output |
| :--- | :--- | :--- |
| 1 — distinct insertion instants | `src/step7_b4_instants.py` | `processed/step7/b4/instants.npz` |
| 2 — population, D10, bracketing gaps | `src/step7_b4_bracket.py` | `processed/step7/b4/bracket.npz` |
| 3 — threshold, rates, inertness | `src/step7_b4_threshold.py` | `processed/step7/b4/threshold.json` |
| 4 — account-clustered bootstrap | `src/step7_b4_bootstrap.py` | `processed/step7/b4/bootstrap_W*.json` |
| 5 — chart | `src/step7_b4_figures.py` | `artifacts/step7-liveness-b4-gap-distribution.png` |
| 6 — deliverable | `src/step7_b4_deliver.py` | `artifacts/step7-liveness-b4.json` |

Every figure in this document is produced by committed code and read from those outputs. **Zero API
calls at any stage.** No usernames, user IDs or individual watch histories appear in this file, in the
JSON, or in the chart.
