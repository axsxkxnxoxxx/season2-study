# Step 6: Derive window W — instance `-a`

> **GATE OUTCOME — header added 2026-08-12, after this artifact was written.**
> **The approved value is `W = 108 days`** (`decisions/0026-step6-window-w-gate.md`, gate 3 of 5).
> The figure derived below is this instance's own output and **predates the ruling in
> `decisions/0025-lag-unit-and-ceiling.md`**, which fixed the lag as a continuous instant difference
> and `W` as the **ceiling** of the percentile. The true 90th percentile is **107.7135 days**; under
> the approved half-open test `watched_at < τ1` a `W` of 107 covers 89.976% of C1 started pairs and
> 108 covers 90.020%, so only the ceiling delivers the percentile the rule asks for.
>
> **Do not take `W` from this file.** Downstream steps take it from the decision entry. Everything
> else here — the estimation sample, the negative-mass tables, the precision intervals, the
> censoring diagnostic — stands as written and is unaffected by the rendering.

**Owner:** Data Scientist (instance `-a`) · **Mode:** GATE, dual implementation · **Reviewer:** Red Team
**Status:** **PROPOSED, NOT ADOPTED.** This is a gate artifact. It derives a number and stops.
No agent adopts W and no agent records approval. Step 7 has not been started.
**Date:** 2026-08-12 · **Run:** re-run against the spec as amended by `decisions/0024-w-is-the-90th-percentile.md`
**API calls:** zero. Every figure is computed from data already on disk.

---

## 1. The number

> ## **W = 107 days.**

**The one-sentence justification, as the spec requires it:**

> W is set at the **90th percentile** of the observed lag from clock start to first S2 episode on
> the C1 all-at-once estimation sample, because attribution-window practice sets the window at or
> slightly above the 90th percentile of the time-to-conversion distribution and a percentile is a
> definition two isolated instances cannot read two ways.

The percentile is **90**, and the reason it is 90 rather than 85 or 95 is that it is the
convention named in `decisions/0024`. **Nothing in this distribution selects it.** That is stated
here in the same words the decision uses, because the number has to be defensible out loud and the
honest defence is *"it is an imported convention, applied without adjustment"* — not *"the data
told us."*

| | |
| :--- | ---: |
| **W** | **107 days** |
| Estimation sample | C1 subset of the Step 5 clean-record sample |
| C1 pairs | **25,120** |
| C1 shows / users | 206 / 2,050 |
| 95% CI on the 90th percentile (iid bootstrap) | **[100, 116]** days |
| 95% CI (exact order-statistic, distribution-free) | **[100, 116]** days |
| 95% CI (cluster bootstrap on user) | [95, 122] days |
| 95% CI (cluster bootstrap on show) | [89, 125] days |
| 90th percentile read on the all-shows curve | **37 days** |
| **Step 13 minimum W range** | **[37, 107] days** |

---

## 2. On the two numbers from run 1

I was instructed not to treat 46 or 107 as a target, an anchor, or a sanity check, and I did not:
the script computes one percentile on one sample and prints it.

**It landed on 107, which is one of the two run-1 values, and that is not confirmation of
anything.** `decisions/0024` records that run 1's instance B selected the 90th percentile under the
withdrawn "flattens" wording. The amended rule *fixes* the percentile at 90. Computing the 90th
percentile of the same distribution twice and getting the same answer is arithmetic, not
agreement — it says the two runs share a population and a lag definition, which was already known
from run 1's identical intermediates. **It carries no independent evidence that 107 is right.** The
thing that would be informative is a divergence, and the reader should look for it in the diff
against instance `-b`, not in the match with run 1.

---

## 3. Population — reproduced, not re-derived

The spec directs both instances to take the population from
`artifacts/step5-contamination-diagnostics.md` §14 rather than re-derive it. The script rebuilds
that waterfall from `processed/step5/pair_revision5.csv` and **asserts** it against the published
figures; the run aborts if any line differs.

| Step | Published | Computed |
| :--- | ---: | ---: |
| Analysis population | 201,900 | **201,900** |
| has S2 evidence | 178,165 | **178,165** |
| `T0` not contaminated | 155,131 | **155,131** |
| completing record not post-dated | 152,126 | **152,126** |
| first S2 watch clean | **128,099** | **128,099** |

All five match exactly.

**The C1 restriction composes on top**, per the spec and `decisions/0003` D14: the estimation
sample is `C1 ∩ 128,099` = **25,120 pairs**. The analysis population is 201,900 and is a different
number; it is not used anywhere in this step.

**"Restrict to users who did start S2"** is already the second line of that waterfall — a pair
enters only if it has at least one S2 record whose number is a member of `E2`. The alternative
reading, "started S2 *within the window*", is circular at this step because the window is what is
being derived, and it is not available.

### D12 buckets, recomputed independently

The classifier was recomputed from `s2_premiere_date`, `s2_finale_date` and `s2_L` with first-match
ordering exactly as Step 1 §10.0 states it, and cross-checked against the frame's own
`cadence_bucket` column: **1,138 shows, 0 disagreements.** No show falls in C0. **7 shows sit
within 1 day of a bucket boundary**, so the thresholds are not load-bearing at this frame size.

| Bucket | Shows | Pairs in the 128,099 |
| :--- | ---: | ---: |
| C0 unclassifiable | 0 | 0 |
| **C1 all-at-once** | **206** | **25,120** |
| C2 weekly | 340 | 39,680 |
| C3 faster than weekly | 167 | 18,218 |
| C4 slower than weekly | 425 | 45,081 |

---

## 4. The lag, and why its definition is not a second free choice

Lag = `date(first S2 watch) − T0`, in whole UTC calendar days, **signed and untruncated**.

`T0` is a calendar date and `⟦T0⟧` is midnight, so the calendar-date difference and
`floor((watched_at − ⟦T0⟧) / 24h)` are **identically equal**, for negative values as well as
positive. The script checks this on every row and it holds on all 128,099. So the two faithful
readings of "the lag in whole days" cannot produce a divergence here.

No truncation, no clipping, no absolute values, no dropped rows — on either curve.

---

## 5. What the distributions look like

`artifacts/step6-lag-distributions-a.png`, four panels: signed symlog density, the ECDF the
percentile is read off, a 0–180-day linear detail, and the log-log survival curve.

| | C1 only (n=25,120) | All shows (n=128,099) |
| :--- | ---: | ---: |
| min | −3,248 | −4,276 |
| p10 | 0 | −62 |
| p25 | 0 | 0 |
| median | 1 | 0 |
| p75 | 12 | 1 |
| p85 | 45 | 10 |
| **p90** | **107** | **37** |
| p95 | 322 | 184 |
| max | 3,927 | 11,724 |
| share at exactly 0 | 39.8% | 45.4% |
| share ≤ 7 days | 70.3% | 83.7% |
| share negative | 2.7% | 22.6% |

**The shape is the whole reason the old wording failed, and panel (d) shows it.** Past roughly day
7 the survival curve is a near-straight line on log-log across three decades. There is no elbow
between day 7 and day 4,000 to read a window off. 70% of C1 starters start inside a week, and the
percentile then walks up a scale-free tail: p85 = 45, p89 = 88, **p90 = 107**, p91 = 130,
p95 = 322. **The five points from p85 to p90 cost 62 days.** Anyone defending 107 out loud has to be
willing to say that 88 and 130 were one percentile point away in each direction, and that the only
thing choosing between them is the convention in `decisions/0024`.

**The 37 on the all-shows curve is descriptive and W was never read off it.** It is reported
because the spec requires the same percentile on both curves to fix Step 13's range.

---

## 6. The negative mass

Required as a count and a share of the started population, split by all five D12 buckets. The
denominator is the **plotted population, 128,099** — the same rows the all-shows curve draws.

| Bucket | Pairs | Negative-lag pairs | Share of bucket | Share of 128,099 | Most negative |
| :--- | ---: | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | — | — | — |
| **C1 all-at-once** | 25,120 | **689** | **2.74%** | 0.54% | −3,248 d |
| C2 weekly | 39,680 | 11,369 | 28.65% | 8.88% | −4,091 d |
| C3 faster than weekly | 18,218 | 7,149 | 39.24% | 5.58% | −3,651 d |
| C4 slower than weekly | 45,081 | 9,753 | 21.63% | 7.61% | −4,276 d |
| **Total** | **128,099** | **28,960** | **22.61%** | — | |

**This is the evidence the split was asked for.** The negative share is 2.7% where the season drops
at once and 22–39% everywhere else. A weekly viewer's negative lag is not a data defect and not a
behaviour: `T0` is the finale date, so watching a season while it airs puts the first episode
before the clock start by construction, and the size of the effect scales with the airing span.
That is exactly why D14 estimates W on C1 and exactly why the all-shows curve cannot be estimated
on. `artifacts/step6-negative-mass-a.png` plots it.

A supplementary split on the 178,165 started pairs of the *analysis* population (which carries
contaminated timestamps) is in the JSON under
`negative_mass_supplementary_denominator_178165`; the pattern is the same. It is labelled
supplementary and is not the required figure.

---

## 7. The C1 negatives: a warrant that is false, reported and not repaired

`decisions/0003` D14 and Step 1 §9 both state that on a C1 show *"every lag is non-negative by
construction."* **That is false on this data**, and it is carried as open item 24 in
`decisions/README.md`. It is not mine to repair. What I find:

| | |
| :--- | ---: |
| C1 pairs with a negative lag | **689** (2.74% of C1) |
| of which the **S1-completion** term of `max()` binds | **459** |
| of which the **S2-finale** term binds | **230** |
| exactly −1 day | 188 |
| worse than −1 day | 501 |
| most negative | −3,248 days |

The 459 are not a contradiction of the warrant so much as a hole in it: on a C1 show `max()` can
still select the S1 completion date, and a user who watched S2 before finishing S1 then gets a
negative lag. The warrant only ever covered the finale term. **The 230 finale-term negatives are
the ones with no account.** Some are the known one-day UTC air-date skew; the rest are not
explained by anything in this step, and −3,248 days is not a skew.

**They are kept.** The spec says the percentile is taken on the signed, untruncated distribution as
it stands. For the record, and not as an alternative: dropping all 689 would move the 90th
percentile from **107 to 113**. So the defect is worth about 6 days and is not load-bearing for W —
but the warrant is still wrong and 230 pairs still have no explanation.

---

## 8. Was the C1 sample large enough to support the percentile?

**For the percentile as a sample statistic: yes, comfortably.** For the percentile as a statement
about viewers: less comfortably, and the reason is clustering, not size.

- 25,120 pairs, of which **2,512 sit in the top decile** the estimate is read off.
- The exact distribution-free order-statistic interval and the iid bootstrap agree to the day:
  **[100, 116]**, ±8 days.
- But those 25,120 pairs come from only **206 shows and 2,050 users**, and pairs cluster inside
  both. Resampling **users** widens the interval to **[95, 122]**; resampling **shows** widens it
  to **[89, 125]**. The show-clustered interval is the honest one and it is roughly ±18 days.
- No single show carries the estimate: the largest contributes 1,063 pairs (4.2%), and dropping
  any of the ten largest one at a time moves the 90th percentile only between **103 and 109**.

**Verdict: the sample supports a 90th percentile to about ±18 days at 95% confidence.** It would
not support a 99th percentile, and it should not be quoted to a precision the interval does not
carry. **107 is a point estimate with an interval of roughly 89 to 125 days**, and the write-up
should say so wherever the number appears.

---

## 9. What would move this number, stated before anyone asks

**a. The convention.** ±1 percentile point is −19/+23 days. This is the largest single lever and it
is a choice, not a measurement.

**b. Exposure, and this one runs in a known direction.** The estimation sample is conditioned on
having started S2 by `τ_pull`, so a pair whose `T0` is recent can only appear in it with a short
lag. The 90th percentile within strata of elapsed time since `T0`:

| Elapsed since `T0` | Pairs | p90 |
| :--- | ---: | ---: |
| < 1 year | 1,479 | 12 d |
| 1–2 years | 2,094 | 37 d |
| 2–4 years | 4,663 | 78 d |
| 4–8 years | 12,743 | 128 d |
| ≥ 8 years | 4,141 | **213 d** |

The gradient is monotone and large. **Selection and cohort effects are not separable here** — older
shows differ in kind, not just in exposure — so this is not a correction and 213 is not a rival
estimate. What it does establish is the **direction**: the pooled 107 is pulled down by
short-exposure pairs, so if it is wrong it is more likely too low than too high. A higher W moves
the never-started share **down**. This is the concern `decisions/0024` records as unresolved, and
this run does not resolve it either.

**c. Percentile convention: not a lever.** All eight standard readings — linear, lower, higher,
nearest, midpoint, inverted CDF, averaged inverted CDF, and nearest-rank `ceil(0.9n)` — return
**exactly 107.0** on C1 and **exactly 37.0** on the all-shows curve. W is an integer without
rounding. A divergence with instance `-b` therefore cannot be a percentile-convention artifact.

---

## 10. One conflict found between approved documents, reported rather than resolved

**Four pairs in the 128,099 have a first S2 record timestamped at or after `τ_pull`**
(`2026-08-11T00:00:00Z`). Step 1 D11 says every record with `watched_at ≥ τ_pull` is discarded from
every computation; the Step 5 sample was built without that filter. The spec directs Step 6 to take
the population from the Step 5 artifact, so I retained them and did not re-derive.

**Nil effect, verified rather than assumed:** none of the four is in C1, and the 90th percentile is
107.0 with them and 107.0 without them. Reported because it is a real inconsistency between two
approved documents, not because it changes anything here. It may matter at Step 8, which
classifies on the 201,900.

Nothing else in the amended spec was undecided at the point of use. No case was resolved by picking
a reading.

---

## 11. Step 13's minimum W range

Per the spec's deterministic rule — the same percentile read on both curves:

| Curve | 90th percentile |
| :--- | ---: |
| C1 only | **107 days** |
| All shows (all five buckets, same 128,099) | **37 days** |

> **Step 13 minimum W range: [37, 107] days.**

`decisions/0024` separately requires the W arms to span **46 to 107**, and requires the **union**
of the two rather than whichever is wider. The union is **[37, 107] days**, which already contains
46. Step 13 should also carry an arm above 107 — the reader will ask about the exposure gradient in
§9b, and a range whose ceiling is the point estimate cannot answer them — but that is a Step 13
proposal, not a Step 6 output, and it is not adopted here.

---

## 12. Files and reproduction

Every figure in this document is produced by one committed script and is greppable to one key.

| Output | Path |
| :--- | :--- |
| This write-up | `artifacts/step6-window-w-a.md` |
| Lag distributions, four panels | `artifacts/step6-lag-distributions-a.png` |
| Negative mass by D12 bucket | `artifacts/step6-negative-mass-a.png` |
| All figures, machine-readable | `artifacts/step6-w-derivation-a.json` |
| Source | `src/step6_derive_w_a.py` |
| Pair-keyed lags (stays out of `artifacts/`) | `processed/step6/a/lags.csv` |

| Section | JSON key |
| :--- | :--- |
| §1 W, CIs, conventions | `W` |
| §3 waterfall | `step5_waterfall_reproduced` |
| §3 buckets | `d12_recomputation` |
| §4 lag definition | `lag_definition_check` |
| §5 shapes and percentile sensitivity | `shape_C1`, `shape_all_shows`, `percentile_sensitivity_*` |
| §6 negative mass | `negative_mass_by_bucket_on_the_plotted_population` |
| §7 C1 negatives | `C1_negative_lags_defect` |
| §8 adequacy | `C1_sample_adequacy` |
| §9b exposure | `C1_exposure_diagnostic` |
| §10 `τ_pull` | `tau_pull_conflict` |
| §11 range | `step13_minimum_W_range` |

Inputs, all read-only: `processed/step5/pair_revision5.csv`, `processed/step2/frame.csv`.
Random seeds are fixed in the source (`20260812`) so both bootstraps are reproducible.

**No usernames, user IDs or individual watch histories appear in this file, in either figure, or in
the JSON.** Counts and aggregates only. The pair-keyed table is in `processed/`.

---

## 13. Status

**Step 6 is an unapproved gate.** This artifact proposes `W = 107 days` and stops. A second
instance ran the same spec in isolation; I have not seen its output and have not looked for it. The
Human Lead diffs the numbers, Red Team reviews, and nothing downstream — Step 7 included — runs
until the Human Lead approves in writing.
