> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — Liveness threshold and rule (instance `a3`, frozen spec)

**Status: PROPOSED, NOT ADOPTED.** Step 7 is a gate. This instance produces and stops. The Human
Lead approves and diffs the two arms.

**Date:** 2026-08-13 · **Instance:** `a3` · **API calls: 0**

**Spec read, not paraphrased:** `task-sheet.md` lines 226–275; `decisions/0038` (whole);
`decisions/0037` (whole); `decisions/0036` (whole, §2 standing, §1 basis and §3 `W`-independence
withdrawn); `artifacts/step1-outcome-definition.md` lines 685–710.

---

## 1. The proposal, in one line

> **Threshold = 632 days.** The 99th percentile of the bracketing-gap distribution on the frozen
> reference population of **152,126** pairs at `W = 108 d`, one gap per pair, raw `631.8031 d`,
> rounded **up** per `0025`.

All eight percentile conventions tested (numpy `linear`, `lower`, `higher`, `nearest`, `midpoint`,
`inverted_cdf`, `averaged_inverted_cdf`, and nearest-rank-ceiling) return `631.8031044554186` to the
digit, at **every** `W` arm. The percentile convention is not a divergence risk in this step.

## 2. The rule statement

A **user-show pair** counts as **live** if the account's insertion history brackets that pair's own
`τ1 = ⟦T0⟧ + W × 24h` with a gap shorter than the threshold.

1. Build the account's **sweep-wide** sequence of record **insertion instants** — every record in
   the account's history, other shows and movies included, not restricted to the show under study.
   The insertion instant is read from the **stored** Step 5 isotonic play-`id` curve
   (`processed/step5/calibration.npz`). **It is not refitted.**
2. Sort ascending. **Collapse runs of exactly equal instants** to one — exact equality only, no
   rounding or bucketing at any resolution. A sub-second gap between two genuinely distinct instants
   is real and retained.
3. Take the **last distinct instant at or before `τ1`** and the **first distinct instant after
   `τ1`**. Test **that one gap** and no other gap in the sweep.
4. **Live** iff both instants exist and their difference is **strictly less than 632 days**.
   **Not live** iff the difference is **632 days or more** (`≥`, per `0025` reason (a)), or there is
   **no instant after `τ1`**, or there is **no instant at or before `τ1`**.

Liveness is a **pair-level filter**. Evidence is account-wide; the test is clock-start-relative and
the clock start is pair-specific, so one account can be live for one show and not for another. **No
user is ever dropped wholesale.** The rule is anchored at `τ1`; `τ2` plays no part in it.

## 3. Counts at `W = 108 d`, threshold 632 d, on the 152,126

| Outcome | Pairs | Share of population |
| :--- | ---: | ---: |
| **Live** | **128,354** | 84.3735% |
| Not live — measured gap ≥ 632 d | 1,276 | 0.8388% |
| Not live — no insertion instant after `τ1` | 4,246 | 2.7911% |
| Not live — no insertion instant at or before `τ1` | 18,250 | 11.9967% |
| **Not live, total** | **23,772** | **15.6265%** |
| *(memo)* pairs with a measured bracketing gap | 129,630 | 85.2123% |

**Realised exclusion rate on measured-gap pairs: 0.9843%.** Slightly under the nominal 1% because
the ceiling moved 631.8031 → 632.

Derivation and application populations are identical: both are the 152,126. The Step 5 waterfall
reproduces exactly — `201,900 → 178,165 → 155,131 → 152,126 → 128,099` — and this run is on **line
4**. `T0` is defined for every pair in it; there are no undefined-clock pairs to rule on.

## 4. The bracketing-gap distribution

Days, one gap per pair, n = 129,630. Chart: `artifacts/step7-gap-distribution-a3.png`.

| p1 | p10 | p25 | median | p75 | p90 | p95 | **p99** | p99.5 | p99.9 | max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.026 | 0.276 | 0.791 | **1.882** | 6.895 | 42.80 | 124.91 | **631.80** | 1,148.6 | 2,469.4 | 3,196.3 |

Against the **pooled** distribution (25,862,249 gaps, all accounts): median `0.0000007 d`, p99
`3.4432 d`. The length bias `0037` §1 named is enormous and reproduces here: the bracketing median is
**2.7 million times** the pooled median, and **34.1%** of bracketing gaps exceed the withdrawn
pooled-99th threshold of 4 days.

---

## 5. MANDATORY DISCLOSURE 1 — the quota property

**The level is set by the exclusion rate, not by anything in the data.**

The percentile is taken on the very distribution the test is applied to. Choosing the 99th therefore
*mechanically* fixes the exclusion rate at 1% of measured-gap pairs, and the threshold is simply
whatever number delivers it. **632 days is not a point at which account behaviour changes.** It is
the price tag on a 1% quota. Any other percentile would have produced an equally self-consistent
answer at a different price:

| Percentile | 90th | 95th | 97.5th | **99th** | 99.5th | 99.9th |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Threshold | 43 d | 125 d | 281 d | **632 d** | 1,149 d | 2,470 d |

The clearest evidence that the number is a quota and not a finding is that **the realised rate is
pinned at ~1% no matter what `W` is**, while the threshold that delivers it moves by 121 days:

| `W` | 46 | 77 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Threshold | 576 d | 590 d | **632 d** | 662 d | 697 d |
| Realised rate | 0.9961% | 0.9944% | **0.9843%** | 0.9847% | 0.9964% |

**This is the price of a calibrated rate, and it is disclosed rather than argued away.** The
alternative — `0036` §1's original basis — had a level anchored to typical gap behaviour and a stated
rate wrong by a factor of about 34 on this population. `0036` §1's **conservative-direction**
argument survives untouched and still points **up**: a false-dead removes a pair, and the liveness
exclusion already biases the never-started share **down** (Step 14, bias 2). It identifies a
direction. It does not identify a level, and nothing in this step does.

## 6. MANDATORY DISCLOSURE 2 — the inertness

**The threshold does almost none of the excluding.** At the proposed 99th, the measured-gap test
removes **1,276** pairs; `0036` §2.3's two evidence-absence edge cases remove **22,496**. The
threshold is **5.4%** of the liveness filter; the edge-case rulings are **94.6%**.

| Percentile | Threshold | Measured-gap exclusions | Edge-case exclusions | Measured-gap share |
| :--- | ---: | ---: | ---: | ---: |
| 90th | 43 d | 12,942 | 22,496 | 36.5% |
| 95th | 125 d | 6,463 | 22,496 | 22.3% |
| 97.5th | 281 d | 3,237 | 22,496 | 12.6% |
| **99th** | **632 d** | **1,276** | **22,496** | **5.4%** |
| 99.5th | 1,149 d | 643 | 22,496 | 2.8% |
| 99.9th | 2,470 d | 89 | 22,496 | 0.4% |

**A reader must not take the threshold to be doing work it is not doing.** Whatever the Human Lead
sets the percentile to, the liveness filter's effect is overwhelmingly the two edge-case rulings.
The consequential decisions in Step 7 were `0036` §2.3's two edge cases, not the number in §1.

### 6.1 Reported divergence from `decisions/0038` §5

`0038` §5 states the split as **3.45% / 96.55%** and says it **holds across every percentile from the
90th to the 99.9th**. On the frozen population **neither figure reproduces**, and I report it rather
than smooth it:

- **The 3.45% is the 201,900 line's, not the frozen line's.** I reproduce it there to four digits
  (0.034524) and measure **5.4%** (0.053677) on the 152,126. The figure predates `0038` §2's own
  choice of reference population.
- **The percentile-invariance claim does not hold on any waterfall line.** Measured-gap share at the
  90th / 99th / 99.9th: 201,900 → 26.4% / 3.5% / 0.1%; 155,131 → 36.7% / 5.6% / 0.6%; **152,126 →
  36.5% / 5.4% / 0.4%**; 128,099 → 70.1% / 19.1% / 2.3%. On the clean sample the measured-gap test is
  the *majority* of exclusions at the 90th, so the inertness is a property of the adopted percentile,
  not of the rule at all percentiles.

**The qualitative claim `0038` §5 was making survives:** at the adopted 99th the edge cases dominate,
on every line except 128,099. Only the specific figure and its claimed invariance do not.

---

## 7. The threshold is a function of `W` (`0038` §6), refitted per Step 13 arm

| `W` (days) | raw p99 | **Refitted threshold** | measured-gap pairs | excluded on gap | **Realised rate** | no-instant-after | no-instant-before |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 46 | 575.455 | **576 d** | 130,013 | 1,295 | 0.9961% | 2,881 | 19,232 |
| 77 | 589.511 | **590 d** | 129,929 | 1,292 | 0.9944% | 3,539 | 18,658 |
| **108** | 631.803 | **632 d** | 129,630 | 1,276 | **0.9843%** | 4,246 | 18,250 |
| 150 | 661.061 | **662 d** | 129,378 | 1,274 | 0.9847% | 4,930 | 17,818 |
| 213 | 696.021 | **697 d** | 128,567 | 1,281 | 0.9964% | 6,278 | 17,281 |

The coupling is **monotone increasing and modest on this population**: 576 → 697 days across the
arms, a 21% rise. It is far weaker than the 408 → 576 and 885 → 973 spans `0038` §6 records from the
previous run's populations, which is expected — those were measured on 128,099 and 201,900.

**Why refitting per arm is not optional.** Freezing 632 d from the `W = 108` arm and carrying it
across delivers 0.834% at `W = 46` and 1.191% at `W = 213` — it misses its stated 1% at every arm but
one, in a direction that varies. `W` and the liveness threshold are **not independent robustness
axes** and Step 13 must not present them as if they were.

**Both counter-moving components are visible in the table.** As `W` rises, `τ1` moves later, so more
pairs lose their post-`τ1` evidence (2,881 → 6,278) and fewer lack pre-`τ1` evidence (19,232 →
17,281). The net effect on the not-live total is small; the composition change is not.

## 8. Right-censoring in the no-instant-after-`τ1` bucket

`0038` §7 records that Step 7 derives on an **uncensored** population, so this bucket is inflated by
pairs D10 removes at Step 8. Measured against the global sweep end (2026-08-10T20:48Z) and against
the pull instant (2026-08-11T00:00Z):

| `W` | no-instant-after | `τ1` past sweep end | `τ1` past pull instant | censored share |
| ---: | ---: | ---: | ---: | ---: |
| 46 | 2,881 | 2,404 | 2,388 | 83.4% |
| **108** | **4,246** | **3,367** | **3,352** | **79.3%** |
| 213 | 6,278 | 5,045 | 5,018 | 80.4% |

So roughly four in five of this bucket are **right-censoring, not silence** — the window simply
closes after the data ends. Only ~880 of the 4,246 at `W = 108` are accounts that genuinely went dark
and never returned. **Testing `τ1` against the account's own last instant is tautological** under the
bucket's definition and I do not report such a figure; the previous run's "past the end of the sweep"
number should be checked for that.

The other edge-case bucket, **18,250** at `W = 108`, matches `0037` §3's figure for the
contaminated-`T0`-excluded population exactly. `0037` §3's characterisation carries: these are
largely pairs whose window closed before the account existed on the **insertion** clock — a mismatch
between the claimed-`watched_at` clock `T0` is built from and the insertion clock liveness runs on.
It is 12.0% of the frozen population and it is the single largest component of the filter. Recorded,
not repaired; `0037` routes it to Step 14.

---

## 9. Judgement calls this instance made that the spec does not settle

Stated so the diff can attribute any divergence.

1. **Records outside the calibration curve's knot range.** `np.interp` **clamps**: 1,862 records with
   `rid` below the first knot map to the curve's start instant and 5,094 above the last knot map to
   its end. The spec names no extrapolation or exclusion rule. Clamping creates **exact** ties, which
   then collapse under `0037` §4, so the effect is bounded and small (6,956 of 27.66 M records).
   Alternatives available: linear extrapolation, or dropping the records.
2. **Boundary of the exclusion test.** Excluded iff `gap >= threshold`. Taken from `0025` reason (a),
   which reasons about "a gap at or above the threshold". `> threshold` is a defensible reading of
   `0036` §2 alone and would change no count materially, but it must be the same in both arms.
3. **`τ1` search side.** `searchsorted(..., side="right")` implements "last instant **at or before**
   `τ1`" — an instant exactly equal to `τ1` counts as *before*, matching Step 1's half-open `[⟦T0⟧,
   τ1)` convention where `τ1` itself is outside the window. No instant lands exactly on `τ1` in this
   data, so the choice is currently inert.
4. **Waterfall reconstruction constants.** `BACKFILL_D = 180`, `POSTDATE_D = -30`, taken from Step 5
   and not chosen here; the reconstruction is asserted against the published waterfall before use.
5. **Step 13 arm list.** `decisions/0027` specifies "the span 46 to 107 **plus** 150 and 213"; the
   launch prompt names five points, 46 / 77 / 108 / 150 / 213. I report those five. **77 is a
   midpoint I did not choose and 108 is outside the stated span**, so Step 13 should confirm whether
   it wants a dense sweep of the span or these five points.
6. **The threshold is reported un-adopted at a single percentile.** `0038` leaves the percentile at
   the 99th "unless the Human Lead rules otherwise on seeing the corrected reference distribution".
   The full percentile ladder is in §5 so that ruling can be made from this document.

## 10. Corroborations against the record

| Quantity | `0037` / `0038` | `a3` |
| :--- | ---: | ---: |
| Pooled p99 (gap-unit fix) | 3.4432 d → 4 d | **3.4432 d → 4 d** |
| Pooled median | 0.0000006 d | 0.0000007 d |
| Gaps per account, median | 7,812 | **7,812** |
| Bracketing median | 2.01 d | 1.88 d |
| Share exceeding pooled-99th | 37.4% | 34.1% |
| No-instant-before bucket, `T0`-clean | 18,250 | **18,250** |

The three that differ are basis differences, not arithmetic disagreements: the bracketing median and
the 37.4% were measured on the previous run's populations, and the pooled median differs in the
seventh decimal place at a reported rounding.

---

**Deliverables:** this file; `artifacts/step7-liveness-a3.json`;
`artifacts/step7-gap-distribution-a3.png`. Row-level intermediates in `processed/step7/a3/`.
Scripts: `src/step7_a3_instants.py`, `src/step7_a3_bracketing.py`, `src/step7_a3_arms.py`,
`src/step7_a3_figures.py`, `src/step7_a3_deliver.py`.

**No threshold is adopted here. Zero API calls were made. Step 8 does not launch until Step 7 is
approved.**
