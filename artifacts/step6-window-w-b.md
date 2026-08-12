# Step 6 — Derive window `W` (instance B, re-run against the amended spec)

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

| | |
| :--- | :--- |
| **Owner** | Data Scientist, instance B (`data-scientist-b`) |
| **Mode** | **GATE. Dual implementation.** Proposed, not adopted. Only the Human Lead approves. |
| **Spec** | `task-sheet.md` Step 6, as amended by `decisions/0024-w-is-the-90th-percentile.md` |
| **Date** | 2026-08-12 |
| **API calls** | **0.** Read-only against `processed/`. |
| **Code** | `src/step6_derive_w_b.py` |
| **Machine-readable** | `artifacts/step6-w-derivation-b.json` |
| **Figures** | `artifacts/step6-lag-distributions-b.png`, `artifacts/step6-lag-tail-b.png` |

---

## 1. The number

> ### `W` = the 90th percentile of the C1 lag distribution = **107.71 days**.

**One-sentence justification, as required:** `W` is set at the **90th percentile** because attribution-window practice sets the window at or slightly above the 90th percentile of the time-to-conversion distribution, with 75th to 90th the cited range, and a fixed percentile is a rule two isolated instances cannot read two ways — which "the percentile where the curve flattens" demonstrably was not.

| | Value |
| :--- | ---: |
| Percentile, fixed by `decisions/0024` | **90th** |
| C1 estimation sample | **25,120 pairs** |
| **`W`, raw 90th percentile** | **107.7135 days** |
| All-shows 90th percentile — **descriptive only, `W` is never read here** | **37.6967 days** |
| **Step 13 minimum range, same percentile on both curves** | **[37.70, 107.71] days** |
| Step 13 range, **union** with the mandated 46–107 span | **[37.70, 107.71] days** |

The union is the wider of the two intervals because [46, 107] falls entirely inside [37.70, 107.71]. **Step 13 must cover 37.70 to 107.71 days**; in whole days that is arms spanning **37 to 108**.

---

## 2. One case the spec does not decide. I am not picking it.

**`W` is 107.7135 days. The spec fixes the percentile and does not say how to render it as a whole number, and Step 1 requires a whole number.**

Step 1 §2.4 (D13) defines the window close as

> `τ1 := τ0 + W × 24h` (identically `⟦T0 + W days⟧ = ⟦T1⟧`)

The parenthetical identity **holds only if `W` is a whole number of days**. At `W = 107.7135`, `τ0 + W × 24h` lands at 17:07:24Z, which is not `⟦T1⟧` for any date `T1`. So either `W` is rounded, or the D13 identity is not satisfied — and the amended Step 6 says nothing about which.

The three available readings, all faithful:

| Reading | `W` | Direction on the headline vs. the raw value |
| :--- | ---: | :--- |
| Truncate / floor | **107** | shorter window → never-started share **up** |
| Round to nearest | **108** | longer window → never-started share **down** |
| Ceiling | **108** | same as round |

**I have not picked one, and the deliverable stands at the raw percentile, 107.7135 days.** Under dual implementation an ambiguity resolved silently by one instance is indistinguishable from a bug. If the two instances of this re-run differ by exactly one day, this is where to look first, and it is a spec gap and not a divergence in the derivation. **The Human Lead should rule on the rounding at the gate.**

Two adjacent cases that the spec *does* decide, recorded so they are not mistaken for gaps:

- **Percentile interpolation method.** All five NumPy methods land between **107.7083 and 107.7597** days. They cannot produce different whole-day values and cannot produce a diff at any granularity this study reports. Checked, immaterial, not escalated.
- **Four pairs whose first S2 watch is stamped at or after `τ_pull`.** The spec's negative-mass rule is explicit — *"no truncation, clipping, absolute values or dropped rows"* — so all four are **retained**. Reported here because Step 8 will discard them under the frozen-cutoff rule and the two steps will therefore not share a row set.

---

## 3. Populations — which number was used where

The spec is emphatic that two figures must not be confused, so both are stated.

| Population | Count | Used in this step? |
| :--- | ---: | :--- |
| **Analysis population** (Step 8 classifies this) | **201,900** | **No.** Named only to keep it distinct. |
| **`W` estimation sample** (Step 5 §14, Step 6 measures this) | **128,099** | **Yes** — this is the all-shows curve |
| **C1 estimation sample** = 128,099 **∩** D12 bucket C1 | **25,120** | **Yes** — `W` is read here and nowhere else |

The Step 5 waterfall was **reconstructed and asserted**, not re-derived by judgment: the script rebuilds the exact masks `src/step5_revision5.py` used and asserts the analysis population equals 201,900 and the estimation sample equals 128,099. Both assertions pass.

| Waterfall step | Pairs | Dropped |
| :--- | ---: | ---: |
| Analysis population | 201,900 | — |
| has S2 evidence | 178,165 | 23,735 |
| `T0` not contaminated | 155,131 | 23,034 |
| completing record not post-dated | 152,126 | 3,005 |
| first S2 watch clean | **128,099** | 24,027 |

**The C1 restriction is applied on top of the 128,099, not instead of it**, per the spec. C1 is **19.6%** of the estimation sample.

**"Restrict to users who did start S2" — how it was read.** Waterfall step 2 (`has S2 evidence`) already imposes it: every pair in the 128,099 has at least one distinct S2 episode whose number is a member of `E2`, with a usable timestamp. **No further filter was applied**, because any `|A| ≥ 1` test would be a function of `W` and therefore circular at the step that derives `W`.

**Cadence classification.** `cadence_bucket` is taken from `processed/step2/frame.csv` and **independently recomputed** from `(P, F_d, L2)` under the D12 first-match rule. **0 of 1,138 shows disagree.** **7** frame shows sit within 1 day of a bucket boundary, so the classifier's fragility is small and no C1 membership is in serious doubt.

**Anchoring.** `T0 = max(S2 finale date, first-pass S1 completion date)` per Step 1 §6 D1, i.e. finale-anchored for every show including weekly ones, and `τ0 = ⟦T0⟧` per §2.4. On a C1 show the premiere and finale coincide, so the finale anchoring is inert inside the estimation sample and binds only on the descriptive all-shows curve.

---

## 4. The two curves, and how far the transfer assumption is stretched

`artifacts/step6-lag-distributions-b.png`, panels A and B; `artifacts/step6-lag-tail-b.png` for the linear zoom and the percentile→days map.

Both curves are **signed and untruncated**. Nothing is clipped, no absolute value is taken, and no row is dropped.

| Percentile | C1 only (days) | All shows (days) |
| ---: | ---: | ---: |
| 1 | −88.71 | −387.35 |
| 5 | 0.08 | −138.40 |
| 10 | 0.22 | −61.02 |
| 25 | 0.69 | 0.06 |
| 50 | 1.73 | 0.72 |
| 75 | 12.80 | 1.95 |
| 85 | 45.98 | 10.60 |
| **90** | **107.71** | **37.70** |
| 95 | 322.61 | 184.39 |
| 99 | 1,155.80 | 1,008.31 |

**The transfer assumption is large and this is the measurement of it.** The same percentile read on the two curves differs by **70.0 days, a factor of 2.86**. The all-shows curve is left-shifted for a mechanical reason and not a behavioural one: under finale anchoring, anyone watching a weekly season while it airs has a negative lag, so 22.6% of the all-shows mass sits below zero and pulls every percentile down. That is exactly why `W` is not read there — and exactly why Step 13's range has to cover the gap.

**Shape of the C1 curve, for anyone who has to describe it out loud:**

| | Share of C1 pairs |
| :--- | ---: |
| lag < 0 | 2.74% |
| 0 ≤ lag < 1 day | 39.76% |
| 0 ≤ lag < 7 days | 66.25% |
| 0 ≤ lag < 30 days | 79.60% |
| lag ≥ 365 days | 4.52% |

Two thirds of C1 starters start within a week. The window is 107.71 days long because of the last few percent, not because of the typical viewer.

---

## 5. The negative mass, by all five D12 buckets

Count and share **of the started population**, which here is the 128,099 estimation sample.

| D12 bucket | Started pairs | Negative lags | Share of that bucket | Share of all started pairs |
| :--- | ---: | ---: | ---: | ---: |
| **C0** unclassifiable | 0 | 0 | — | 0.00% |
| **C1** all-at-once | 25,120 | **689** | **2.74%** | 0.54% |
| **C2** weekly | 39,680 | **11,369** | **28.65%** | 8.88% |
| **C3** faster than weekly | 18,218 | **7,149** | **39.24%** | 5.58% |
| **C4** slower than weekly | 45,081 | **9,753** | **21.63%** | 7.61% |
| **Total** | **128,099** | **28,960** | **22.61%** | 22.61% |

**This split is the evidence the spec asked for, and it carries.** The negative share runs 2.74% on C1 against 21.6–39.2% on every bucket where the season takes calendar time to air. The negative mass tracks release cadence, not viewer behaviour. C0 is empty in this frame — no show failed classification — so the bucket is reported at zero rather than omitted.

---

## 6. The D14 warrant is false, and here is exactly how false

`decisions/0003` D14 and Step 1 §9 both state that on a C1 show every lag is **non-negative by construction**. **That is wrong against the data.** It is open item 24 in `decisions/README.md` and is not mine to repair. What I found, reported and not silently handled:

| | Count |
| :--- | ---: |
| C1 pairs with a **negative** lag | **689** (2.74% of 25,120) |
| — binding term is the **S1 completion date** | **459** |
| — binding term is the **S2 finale date** | **230** |
| — binding term is a tie | 0 |
| Of the 230 finale-binding: **within 1 day** (the known UTC finale skew, Step 1 §6) | **135** |
| Of the 230 finale-binding: **beyond 1 day — unexplained** | **95** |
| Most negative finale-binding lag | **−495.43 days** |
| Most negative C1 lag of any kind | **−3,247.44 days** |

**Why the warrant fails.** `T0` is a `max()` of two terms, and on a C1 show only one of them is pinned to the release. When the S1 completion date binds — 459 cases — a user can perfectly well have watched S2 before finishing S1, and the lag is negative with no defect involved. D14's reasoning covers the finale term only and then generalises to the whole `max()`. The 95 finale-binding cases beyond the UTC skew have **no account**: on a same-day drop nothing should be watchable up to 495 days before the season exists.

**It is not load-bearing for `W`, and that is measured rather than asserted:**

| Handling of the 689 | 90th percentile |
| :--- | ---: |
| **As specified — signed, untruncated** | **107.71 days** |
| Negatives dropped | 113.99 days (+6.27) |
| Negatives truncated to zero | 107.71 days (unchanged) |

Truncation cannot move a 90th percentile when only 2.74% of the mass is below zero. Dropping moves it 6.3 days. **The spec's handling is the one used; the alternatives are shown only to size the defect.**

---

## 7. Was the C1 sample large enough to support the 90th percentile?

**Required answer: yes for the percentile, no for the decimals.**

| | |
| :--- | ---: |
| C1 pairs | 25,120 |
| Pairs above the 90th percentile | 2,512 |
| Distinct shows | 206 |
| Distinct users | 2,050 |

95% bootstrap intervals on the 90th percentile, 2,000 iid resamples and 500 cluster resamples:

| Resampling scheme | 95% CI (days) | SD (days) |
| :--- | :--- | ---: |
| iid over pairs | **[100.5, 116.6]** | 4.0 |
| clustered by **user** (2,050 clusters) | **[93.9, 122.6]** | 7.2 |
| clustered by **show** (206 clusters) | **[89.8, 122.4]** | 8.8 |

The pair-level sample is ample; the **binding constraint is 206 shows, not 25,120 pairs**, and the honest interval is the show-clustered one. Concentration is moderate rather than alarming: the largest show is 4.2% of pairs, the top 20 are 34.8%, and it takes 37 shows to reach half the sample.

**So `W` is defensible to roughly ±9 days and no further.** Quoting 107.71 to two decimals states more precision than 206 shows can support. The decimals are carried in this document because the rounding question in §2 is open, not because they are meaningful.

---

## 8. Two things that would make this number wrong, stated before anyone asks

**8.1 The percentile is a convention and nothing in the data selects it.** Panel D of the main figure is the evidence: the C1 survival curve is close to a straight line on log-log axes from about day 7 outward, so there is no elbow, no shoulder, and nothing to read. Moving the convention inside its own cited 75th-to-90th range moves `W` by more than the whole quantity:

| Percentile | `W` (days) |
| ---: | ---: |
| 75 | 12.80 |
| 80 | 22.36 |
| 85 | 45.98 |
| **90** | **107.71** |
| 95 | 322.61 |

**Moving from the 85th to the 90th buys 61.7 days.** Anyone defending 107.71 out loud has to be willing to say that the 85th percentile was equally available and would have given 46, and that the choice between them is imported practice rather than a fact about this data. `decisions/0024` says this itself and labels the convention as a convention; this section is the same statement with the numbers attached.

**8.2 The upper tail is right-censored, and the censoring runs against `W`.** A pair observed for fewer than `W` days cannot exhibit a lag above `W`. **530 C1 pairs (2.11%) have less exposure than `W` itself.** Restricting to progressively longer-observed pairs moves the 90th percentile up:

| Minimum exposure | C1 pairs | 90th percentile (days) |
| :--- | ---: | ---: |
| none (as specified) | 25,120 | **107.71** |
| ≥ 1 year | 23,637 | 119.26 |
| ≥ 2 years | 21,545 | 128.07 |
| ≥ 4 years | 16,882 | 146.03 |
| ≥ 8 years | 4,141 | 213.04 |
| ≥ 12 years | 119 | 177.23 |

**This does not change `W` and no adjustment is proposed.** Longer-exposure pairs are also older shows, so exposure and cohort are not separable with what is on disk, and the movement above is an **upper bound** on the censoring effect rather than an estimate of it. The direction is worth naming because it is one-sided: **a larger `W` moves the never-started share down**, so 107.71 is, if anything, a conservative read of the delay distribution and the headline never-started share derived from it is if anything too high. Carry to Step 14.

---

## 9. Handoffs

- **Step 13** takes the range **[37.70, 107.71] days** as its minimum `W` coverage — the 90th percentile read on the C1 curve and on the all-shows curve, plus the mandated 46–107 span, which is contained inside it. In whole days, arms spanning **37 to 108**.
- **Step 16**, if interactive, bounds the `W` control to whatever Step 13 records, not to this range directly.
- **Step 14** takes §6 (D14's false warrant, 95 unexplained C1 negatives), §7 (206 shows is the binding sample constraint), §8.1 (the percentile is imported practice) and §8.2 (right-censoring, one-sided, direction named).

## 10. Reproduction

One committed script, `src/step6_derive_w_b.py`, produces every figure and every number in this document. It reads `processed/step5/pair_revision5.csv` and `processed/step2/frame.csv`, makes **zero network calls**, and asserts both Step 5 population figures and the D12 recomputation before computing anything. Bootstrap seed 20260812.

User-keyed intermediates are written to `processed/step6/b/` (`c1_lags.csv`, `all_lags.csv`) and stay there. This document and the two figures contain counts and aggregates only.

---

## 11. Status

**PROPOSED. Not adopted.** This is a gate. I do not adopt my own proposal, I do not record approval, and I do not begin Step 7. A second instance ran the same spec in isolation; I have not read its output and have not reconciled with it. **The Human Lead diffs the numbers, rules on the rounding question in §2, and approves or does not.**
