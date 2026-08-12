# Step 6: Derive window W — **instance A**

**Owner:** Data Scientist · **Mode:** GATE, dual implementation · **Date:** 2026-08-12
**Reviewer:** Red Team · **Approval:** Human Lead, in writing, in this session

> ## **PROPOSED: W = 107 days.**
>
> **The percentile and the reason, in one sentence:** *W is the **90th percentile** of the
> lag from clock start to first S2 episode on the C1 estimation sample, because that is where
> the coverage curve flattens — the first 107 days recruit nine in ten of everyone who ever
> started S2, while day 108 recruits fewer than one starter in two thousand and the remaining
> tenth is spread over the following ten years.*

**This is a proposal. It is not adopted.** No downstream step may use 107 until the Human Lead
approves it in writing. Step 7 has not been started and nothing here begins it.

**Zero API calls.** Everything read from disk: `processed/step5/pair_revision5.csv`,
`processed/step2/frame.csv`.

---

## 0. Filename collision — read this before diffing

Step 6 runs twice and both instances share one working tree. This instance first wrote to
`src/step6_derive_w.py`; **that file, and the artifact paths it wrote, were overwritten mid-run
by the other instance's implementation of the same step.** No file written by the other instance
was read, and nothing from it was used. Everything this instance produces now carries an
`-instance-a` / `_instance_a` suffix purely as a collision guard:

| This instance's output | Path |
| :--- | :--- |
| Code | `src/step6_derive_w_instance_a.py` |
| Chart | `artifacts/step6-lag-distribution-instance-a.png` |
| Percentile table | `artifacts/step6-lag-percentiles-instance-a.csv` |
| All figures, one JSON | `processed/step6/step6_w_instance_a.json` |

**The suffix is not a claim about which instance is which.** The Human Lead should rename both
sides to whatever the diff wants. One orphan file, `processed/step6/step6_w.json`, was deleted
after confirming it was byte-identical to this instance's namespaced copy; nothing else was
removed.

---

## 1. What W is, and what it is not

`W` is a **number of days**. The window is `[⟦T0⟧, τ1)` with `τ1 = ⟦T0⟧ + W × 24h`, half-open
per Step 1 §2.4 D13, and it is exactly `W` days long. A pair is **Never started** iff it has no
distinct S2 episode with `watched_at < τ1`.

W is **not** a claim about how long people should take. It is the point past which waiting
longer stops telling you anything: if someone has not started S2 by `T0 + W`, the evidence says
they are overwhelmingly unlikely to, and continuing to wait buys coverage at a rate of one
person in two thousand per day.

---

## 2. Population — taken, not re-derived

| | Pairs |
| :--- | ---: |
| Analysis population (Step 8's, **not this step's**) | 201,900 |
| **W estimation sample** — Step 5 §14 ruling 1 | **128,099** |
| **— restricted to D12 bucket C1 (D14) — the curve W is read off** | **25,120** |

The 128,099 is **not re-derived from principle here.** The five Boolean masks that produce it
are copied verbatim from `src/step5_revision5.py` and the script asserts both endpoints:

| Step | Pairs | Dropped |
| :--- | ---: | ---: |
| Analysis population | 201,900 | — |
| has S2 evidence | 178,165 | 23,735 |
| `T0` not contaminated | 155,131 | 23,034 |
| completing record not post-dated | 152,126 | 3,005 |
| first S2 watch clean | **128,099** | 24,027 |

The point of copying rather than re-deriving is that a divergence between the two instances then
**cannot be a population difference.** The analysis population is 201,900 and appears nowhere in
this derivation.

**The C1 restriction is applied on top of the 128,099, not instead of it** — the sample is
two-factor, cadence **and** provenance, exactly as Step 5 §14 hands it over.

### 2.1 The three spec lines that cost nothing because Step 1 already paid them

- **"Restrict to users who did start S2"** is the `has S2 evidence` line: at least one distinct
  S2 episode whose `number ∈ E2`. It is deliberately **not** Step 1 §7's `|A| > 0`, which is
  bounded by `τ1` and therefore by W — using that here would make W a function of W.
- **"Anchor the lag on the S2 finale date, not the premiere, for weekly-release shows"** is
  satisfied **by construction**: `T0 = max(S2 finale air date, first-pass S1 completion date)`
  (Step 1 §6, D1). This step re-decides nothing about the anchor.
- **Bucket membership** is read from `frame.cadence_bucket`, which Step 2 already computed under
  D12. This step does not re-classify anything, and never uses the words "binge shows".

### 2.2 Bucket counts

| Bucket | Shows in frame | Started pairs in the estimation sample |
| :--- | ---: | ---: |
| **C0** unclassifiable | **0** | **0** |
| **C1** all-at-once | 206 | **25,120** |
| C2 weekly | 340 | 39,680 |
| C3 faster than weekly | 167 | 18,218 |
| C4 slower than weekly | 425 | 45,081 |
| Total | 1,138 | 128,099 |

**C0 is empty** — every show in the frame classified. Reported as a count and not pooled, per
D12.

---

## 3. The lag, and the unit it is measured in

`lag = date(first S2 watched_at) − T0`, in **whole UTC calendar days**, per Step 1 §0: *"T0, T1,
lags and gaps are whole numbers of days, because W is a number of days."* This is identically
`floor((watched_at − τ0) / 24h)` and is **negative** where the first S2 watch precedes the clock
start. No rounding toward zero, no absolute value.

**The first S2 watch is the earliest record whose `number ∈ E2`** — season membership by set,
Step 1 §3.2 — which under the earliest-per-distinct-episode collapse (§2.2) is the minimum
canonical timestamp over `A`.

---

## 4. The C1 curve, and where it flattens

`artifacts/step6-lag-distribution-instance-a.png`, panel (a) and panel (c).

| Percentile | C1 lag (days) | days bought per further point |
| ---: | ---: | ---: |
| 50 | 1 | — |
| 75 | 12 | 1.0 |
| 80 | 22 | 2.0 |
| 85 | 45 | 7.0 |
| 89 | 88 | 14.0 |
| **90** | **107** | **19.0** |
| 91 | 130 | 23.0 |
| 95 | 322 | 71.0 |
| 99 | 1,155 | 418.4 |

Full table, both curves: `artifacts/step6-lag-percentiles-instance-a.csv`.

**The flattening, as a number.** Define the marginal recruitment rate at lag `d` as the share of
the C1 started population whose first S2 watch falls in the band `[d/1.3, d×1.3)`, per day of
that band. The band is **proportional to `d`**, not a fixed width, because a fixed window on a
heavy tail smears the day-0 spike — 42.5 percent of the sample — across the first fortnight and
invents a plateau that is not in the data.

| lag day | 7 | 30 | 60 | 90 | **107** | 180 | 365 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| % of C1 recruited per extra day | 1.392 | 0.214 | 0.097 | 0.059 | **0.048** | 0.025 | 0.011 |

**At W = 107 the marginal day buys 0.048 percent of the sample — one more starter in 2,071.**
Past that point an extra **week** of window moves coverage by about a third of a percentage
point (7 × 0.048 = 0.34).

**Coverage:** 90.02 percent of C1 starters, and 93.41 percent of all-shows starters, have started
by day 107.

### 4.1 The honest caveat, stated before Red Team states it

**Past roughly day 7 the C1 density is close to scale-free.** Log-log slope of the per-day rate
between consecutive bands:

| band | [7,14) | [14,30) | [30,60) | [60,90) | [90,120) | [120,180) | [180,270) | [270,365) | [365,730) | [730,1460) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| per day | 248.6 | 100.8 | 36.3 | 20.4 | 12.2 | 8.0 | 5.1 | 3.1 | 1.7 | 0.5 |
| log-log slope vs previous | — | −1.22 | −1.43 | −1.13 | −1.52 | −1.18 | −1.09 | −1.50 | −1.06 | −1.82 |

The slope sits between −1.1 and −1.5 across every decade from one week to four years. **There is
no break in the density to read.** Anyone who says "just find the elbow" should be shown panel
(c): the elbow is at about day 7, and W = 7 days is obviously not the window this study wants.

**So "the curve flattens" is a claim about the COVERAGE curve, not about a break in the
density** — about what an extra day of window buys, not about a change of regime in viewer
behaviour. That is a judgment call made against a stated criterion, and it is stated here rather
than dressed up as a data-determined break. Step 13 is what tests it, and §7 fixes the range
Step 13 must cover.

### 4.2 Why not 91, and why not 45

- **91** is Netflix's reporting window and Step 9 reports the whole headline a second time at 91
  regardless. Setting `W = 91` would collapse the study's derived number into the number it is
  arguing with, and the comparison would then be vacuous. That 107 lands near 91 is a useful
  cross-check and is **not** the reason for it.
- **45 days (P85)** is defensible on the same curve and is inside Step 13's range at the low end.
  It costs five percentage points of C1 coverage. It is not proposed, because at day 45 the
  marginal day still buys 0.135 percent — nearly three times the rate at 107 — so the curve has
  not yet flattened by the criterion in §4.

---

## 5. Was the C1 sample large enough to support the percentile? **Yes, for P90.**

`n = 25,120`, of which **2,507 pairs lie above P90**. Distribution-free order-statistic 95
percent intervals:

| Quantile | Value (days) | 95% CI (days) | Width as % of value |
| :--- | ---: | :--- | ---: |
| P85 | 45 | [42, 49] | ±8% |
| **P90** | **107** | **[100, 115]** | **±7%** |
| P95 | 322 | [299, 347] | ±7% |
| P99 | 1,155 | [1,074, 1,247] | ±7% |

**The sampling uncertainty in W is ±7 days.** That is an order of magnitude smaller than the
transfer-assumption range in §7 and two orders smaller than the censoring effect in §8, so
**sample size is not the binding constraint on W — the two assumptions are.** Stated that way
because "large enough" on its own would be the wrong answer to give.

---

## 6. The negative mass, and one D14 claim that the data falsifies

### 6.1 Negative mass by all five D12 buckets

Required as a count and a share of the started population, split by bucket, because that split is
the evidence that the negative mass is a **cadence artifact** and not viewer behaviour.

| Bucket | Started pairs | Negative-lag pairs | % of bucket | % of all started | Median negative lag |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **C0** | 0 | 0 | — (no shows in frame) | 0.00% | — |
| **C1** all-at-once | 25,120 | **689** | **2.74%** | 0.54% | −21 d |
| C2 weekly | 39,680 | 11,369 | 28.65% | 8.88% | −49 d |
| C3 faster than weekly | 18,218 | 7,149 | 39.24% | 5.58% | −33 d |
| C4 slower than weekly | 45,081 | 9,753 | 21.63% | 7.61% | −159 d |
| **Pooled** | **128,099** | **28,960** | **22.61%** | 22.61% | −56 d |

The reading is exactly the one D14 predicts: on C1 the release span is zero, so almost nothing
can precede the clock start; on C2/C3/C4 the season takes weeks or months to finish airing, and
anyone who watched along lands **before** the finale-anchored clock start. **C4 has the longest
spans and the deepest negative median, −159 days.** Nearly a quarter of all started pairs sit at
a negative lag, and on C3 it is two in five. This is release cadence, not behaviour, and it is
why W is estimated on C1 alone.

The all-shows curve is plotted **signed and untruncated** — panel (a) covers the full signed
support on a symlog axis; panel (b) is a linear zoom that **states its off-panel mass in
numbers** (all shows 3.3% left / 2.8% right; C1 0.8% left / 4.0% right) so an axis limit is not
mistaken for a truncation. Nothing is clipped, no absolute values are taken, no negative row is
dropped anywhere in the code.

### 6.2 **D14's non-negativity claim is FALSIFIED. This is flagged, not resolved.**

`decisions/0003` states: *"within the C1 estimation sample there are no negative lags to
truncate."*

**There are 689 of them, 2.74 percent of C1.** The claim is right about the finale term and
silent about the other one: `T0 = max(finale, S1 completion)`, and where the S1-completion term
binds **after** the first S2 watch the lag is negative on a C1 show too. These are precisely the
**S1-term negative lags** that Step 1 §5 names and that D2 exists to count — genuine parallel
viewing, not a cadence artifact.

**The spec states no rule for them, so this instance did not invent one.** The only handling the
spec ever states is the one applied: **signed, untruncated, nothing dropped**, on both curves —
truncation having been withdrawn as indefensible in `decisions/0003`. The alternative reading is
published beside it so its size is visible rather than argued about:

| Reading | C1 P90 | all-shows P90 |
| :--- | ---: | ---: |
| **Adopted — negatives kept, untruncated** | **107 d** | **37 d** |
| Negatives dropped from the curve | 113 d | 74 d |

**On C1 the reading is worth 6 days.** On the all-shows curve it is worth 37 — which is the size
of the whole transfer assumption, so **if the two instances diverge, this is the first place to
look.** It is a spec ambiguity, not a bug; it is reported and not reconciled.

---

## 7. Step 13's range — derived deterministically, and it is wide

The spec's rule: take **the same percentile** used to set W, read it on the C1 curve and on the
all-shows curve, report both. Stating the percentile once and reading it twice is what stops two
instances producing different ranges.

| Curve | n | P90 |
| :--- | ---: | ---: |
| **All shows** (descriptive only) | 128,099 | **37 days** |
| **C1 only** (W is read here) | 25,120 | **107 days** |

> ### **Step 13 must vary W over at least [37, 107] days.**

**That interval is the size of the D14 transfer assumption**, measured rather than asserted. It
is nearly three-to-one. The assumption that binge viewers' delay-to-start behaviour carries to
weekly viewers is doing a great deal of work, and Step 13 is where it gets tested.

Both values are identical under all five numpy quantile conventions — `linear`, `lower`,
`higher`, `nearest`, `midpoint` — so neither is a rounding artifact.

**W is read off the C1 curve only.** The all-shows curve is descriptive: it exists to show the
size of the transfer assumption, and no percentile used to set W was read from it.

---

## 8. Limits, each with a direction

1. **The lag is right-censored and W is therefore a LOW estimate.** A pair whose `T0` is recent
   can only contribute a short lag, and a pair that would have started after the pull cutoff is
   absent from the sample entirely. Restricting C1 to longer-exposed pairs raises P90 sharply:

   | Minimum exposure `τ_pull − T0` | n | P85 | **P90** | P95 |
   | :--- | ---: | ---: | ---: | ---: |
   | none (as reported) | 25,120 | 45 | **107** | 322 |
   | ≥ 1 year | 23,641 | 50 | **119** | 349 |
   | ≥ 2 years | 21,547 | 55 | **128** | 371 |
   | ≥ 4 years | 16,884 | 63 | **146** | 406 |
   | ≥ 8 years | 4,141 | 93 | **213** | 522 |

   **Not corrected**, and the reason is that it cannot honestly be: the long-exposure subset is
   also an older-show, older-cohort subset, so the gap is censoring **and** cohort together and
   this step cannot separate them. The **direction** is unambiguous — the true P90 is at or above
   107 — and a higher W moves the never-started share **down**. Only 2.11 percent of C1 pairs
   (530) have less than 107 days of exposure, so the effect is in who is *missing* from the
   sample, not in who is truncated inside it.
2. **The transfer assumption is not tested here, only measured** (§7).
3. **"Flattens" is a judgment against a stated criterion, not a data-determined break** (§4.1).
4. **The 689 C1 negatives are an unruled case** (§6.2).
5. **The sample is the analysable cohort only.** 2,549 complete accounts of 4,050 planned; the
   287 discarded, 38 over-cap and 1,214 never-attempted accounts are **absent, not empty**
   (Step 5 §15 item 6).
6. **Step 5's retained contamination travels.** The estimation sample is clean by construction —
   that is what the 128,099 is — but W is applied to the 201,900, which carries 46,642 pairs with
   a contaminated first S2 watch.

---

## 9. Reproduction — per figure, per key

Read-only. **Zero API calls.** Single source file: **`src/step6_derive_w_instance_a.py`**, which
writes every figure quoted above into **`processed/step6/step6_w_instance_a.json`**. A reader can
grep any number in this artifact to exactly one key.

| Section | JSON key |
| :--- | :--- |
| §2 population and waterfall | `population` |
| §2.2 bucket counts | `frame_cadence_shows`, `estimation_sample_pairs_by_bucket` |
| §4 percentile table | `percentile_table` (also `artifacts/step6-lag-percentiles-instance-a.csv`) |
| §4 W, conventions, coverage | `W`, `coverage_at_W` |
| §4 marginal rate, §4.1 tail slopes | `flattening`, `flattening.tail_bands` |
| §5 sample adequacy and CIs | `sample_adequacy` |
| §6.1 negative mass by bucket | `negative_mass_by_D12_bucket` |
| §6.2 the two readings | `negatives_reading` |
| §7 Step 13 range | `step13_W_range` |
| §8 item 1 censoring | `censoring_sensitivity` |
| Chart | `artifacts/step6-lag-distribution-instance-a.png` |

The script **asserts** the Step 5 waterfall reproduces to `[201,900 … 128,099]` and fails loudly
if it does not, so no figure here can be computed on a silently different population.

Aggregates and counts only. Nothing keyed to a username or user ID is written to `artifacts/`.

---

## 10. Status

**GATE OPEN. W = 107 days is PROPOSED and NOT ADOPTED.**

Nothing downstream of this gate has been run. Step 7 has not been started. This instance did not
record its own approval and did not reconcile with the other instance.

**Three things the Human Lead should have in hand before approving:** the one-sentence
justification at the head of this document, the §6.2 unruled negatives — which is this
instance's most likely source of divergence — and the §8 item 1 censoring direction, because it
says the number is a floor rather than a point.
