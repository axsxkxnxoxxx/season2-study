# Step 6 — Window `W`. PROPOSED, not adopted.

| | |
| :--- | :--- |
| **Step** | 6, derive the window `W` |
| **Owner** | Data Scientist |
| **Mode** | **GATE**, dual implementation. Two isolated instances run the same spec; the Human Lead diffs the numbers |
| **Status** | **PROPOSED.** Nothing here is adopted. The author does not adopt its own proposal and has recorded no approval |
| **Spec** | `task-sheet.md` §"Step 6: Derive window W", as amended by `decisions/0022` |
| **Inputs** | `processed/step5/pair_revision5.csv`, `processed/step2/frame.csv`. **Zero API calls** |
| **Code** | `src/step6_derive_w.py` |
| **Figures** | `artifacts/step6-lag-distributions.png` |
| **Every figure quoted below** | `artifacts/step6-w-derivation.json`, key named in §10 |
| **Isolation** | This file is **one instance's output**, not a reconciled result. A second set of Step 6 files written by the other instance exists in `artifacts/` under different filenames; its existence is visible from a directory listing, and **it was not opened, read, or compared against at any point**. The diff is the Human Lead's |

---

## 1. The number

> ## `W = 46 days`
>
> ### the **85th percentile** of the lag from clock start to first S2 episode, on the C1 estimation sample.

**The one-sentence justification, as it would be said out loud:**

> **`W` is 46 days, the 85th percentile, because that is where the coverage curve flattens: days 42–49 is the first week of window that buys less than one additional percentage point of started-user coverage, no later week buys more, and the 85th percentile is the whole percentile lying inside that week.**

At `W = 46` the window contains the first S2 episode for **85.00%** of C1 started pairs — 95% interval **[83.83, 86.09]**, clustered on shows. On the all-shows curve the same 46 days covers 90.66%, for the reason §6 gives.

`W` is read off the **C1 curve only**. The all-shows curve in §6 is descriptive and no percentile was read from it.

*(Key: `CHOSEN`, `criterion`, `bootstrap_CI_coverage_pct_at_W`.)*

---

## 2. What was measured, and on what population

**The estimation sample is taken from Step 5, not re-derived.** `src/step6_derive_w.py` copies the five Boolean masks verbatim from `src/step5_revision5.py` and **asserts** the published waterfall before it computes anything. The assertion passes exactly:

| Step | Pairs | Published in `step5-contamination-diagnostics.md` §14 |
| :--- | ---: | ---: |
| Analysis population | 201,900 | 201,900 |
| has S2 evidence | 178,165 | 178,165 |
| `T0` not contaminated | 155,131 | 155,131 |
| completing record not post-dated | 152,126 | 152,126 |
| first S2 watch clean | **128,099** | **128,099** |

**201,900 is the analysis population and is not used here.** 128,099 is the estimation sample.

**D14 applies on top of it, not instead of it.** Restricting to `cadence_bucket == "C1"` in the Step 2 frame, per the D12 classifier:

| | Pairs | Shows | Users |
| :--- | ---: | ---: | ---: |
| Estimation sample, all buckets | 128,099 | — | — |
| **C1 only — where `W` is estimated** | **25,120** | **206** | **2,050** |
| C2 | 39,680 | | |
| C3 | 18,218 | | |
| C4 | 45,081 | | |
| C0 | **0** — the frame contains no unclassifiable season | | |

**"Restrict to users who did start S2"** is satisfied by the second line of the waterfall: every pair in the sample holds S2 evidence whose episode number is a member of `E2`, and the sample additionally requires that pair's *first* S2 record to be clean.

**The lag.** `lag = (first S2 watch instant − τ0) / 86400`, in days, where `τ0 = ⟦T0⟧` is midnight UTC of `T0` and `T0 = max(S2 finale air date, S1 completion date)` per D1. **The finale anchor is inherited, not re-decided here** — `T0` is read from the column `src/step5_t0_binding.py` already computed under the approved Step 1 §6, which is why the "anchor the lag on the S2 finale date, not the premiere, for weekly-release shows" requirement holds for every bucket by construction rather than by a second implementation of `max()`.

**The coverage curve.** `F(w) = P(lag < w)` — a **strict** inequality, so that `F(W)` is exactly the share of started pairs whose first S2 episode falls inside the half-open window `[τ0, τ0 + W×24h)` of Step 1 §2.4 D13. `date(watched_at) ≤ T1` appears nowhere.

*(Key: `population`.)*

---

## 3. Where the curve flattens

The C1 coverage curve gains 66 points in its first week and then decays. The gain per additional week:

| Week | Days | Coverage at end | Gain in the week |
| ---: | :--- | ---: | ---: |
| 0 | 0–7 | 68.997% | 66.254 pp |
| 1 | 7–14 | 75.924% | 6.927 pp |
| 2 | 14–21 | 79.494% | 3.571 pp |
| 3 | 21–28 | 81.791% | 2.297 pp |
| 4 | 28–35 | 83.360% | 1.569 pp |
| 5 | 35–42 | 84.451% | 1.091 pp |
| **6** | **42–49** | **85.426%** | **0.975 pp** ← first week under 1 pp, and no later week exceeds it |
| 7 | 49–56 | 86.302% | 0.876 pp |
| 8 | 56–63 | 86.911% | 0.609 pp |
| 9 | 63–70 | 87.611% | 0.701 pp |
| 12 | 84–91 | 89.156% | 0.470 pp |
| 19 | 133–140 | 91.342% | 0.275 pp |

**The criterion, stated once and applied identically everywhere in this step:**

> Walk `F(w)` in consecutive 7-day blocks from day 0. The curve has **flattened** at the first block whose coverage gain is below **1.0 percentage point** and which **no later block exceeds**. `W` is the whole percentile of the lag distribution lying inside that block, and `W` in days is that percentile's value rounded **up** to a whole day.

Block 6 is that block. Exactly one whole percentile falls inside it: **P85 = 45.975 days → `W` = 46**.

**Why weekly blocks and not a daily slope.** The one-day slope on this curve crosses 0.10 pp/day downward at day 56 and back **upward** at day 66. A "first day the slope drops below x" rule is therefore not reproducible on this data — two instances smoothing differently would land in different places — while a 7-day block rule is, and it matches the weekly grid the frame's release cadence actually sits on.

*(Keys: `weekly_gain_C1`, `criterion`.)*

---

## 4. How load-bearing the 1.0 pp/week convention is

**The threshold is a convention and is published as one.** Sweeping it:

| Threshold | Flattening block | Percentile | `W` |
| ---: | :--- | ---: | ---: |
| 2.00 pp/week | days 28–35 | 82 | 29 d |
| 1.50 pp/week | days 35–42 | 84 | 39 d |
| **1.00 pp/week** | **days 42–49** | **85** | **46 d** |
| 0.75 pp/week | days 63–70 | 87 | 65 d |
| 0.50 pp/week | days 84–91 | 89 | 89 d |
| 0.25 pp/week | days 147–154 | — | — (no whole percentile falls inside that block) |

**Read this honestly: the percentile is stable and the day count is not.** Across a four-fold change in the threshold the percentile moves from 82 to 89 — seven points — while `W` moves from 29 days to 89 days, a factor of three. That is not an instability in the method; it is the shape of the distribution. The tail is heavy, so small changes in the coverage target buy large changes in days. **Anyone defending `W = 46` out loud has to be willing to say that 39 and 65 were also available and that the choice between them was a judgment call about how much coverage is enough, not a fact the data settled.**

One consequence, offered as a consequence and **not** as a reason for the value: **right-censoring under D10 keys on `max(W, 91)`, so every candidate in the 29–89 day range retains exactly the same rows.** Choosing inside that range costs nothing in sample and cannot be defended or attacked on sample-size grounds.

*(Key: `criterion_threshold_sweep`.)*

---

## 5. Was the C1 sample large enough to support the percentile?

**Yes for the 85th percentile, and no for anything further into the tail.** That answer needs the clustering to be taken seriously: 25,120 pairs are not 25,120 independent observations. They come from **206 shows** (median 79 pairs per show, max 1,063) and **2,050 users** (median 9 pairs per user, max 88).

95% bootstrap intervals on the C1 percentile, in days, resampling clusters with replacement, B = 2,000, seed 20260812:

| Percentile | Point | Cluster = show | Cluster = user | i.i.d. pairs |
| ---: | ---: | :--- | :--- | :--- |
| P50 | 1.73 d | [1.49, 1.90] | [1.59, 1.83] | [1.67, 1.78] |
| P75 | 12.80 d | [10.86, 14.97] | [11.43, 14.26] | [11.95, 13.64] |
| **P85** | **45.98 d** | **[38.19, 53.97]** | **[40.32, 51.89]** | [42.81, 49.29] |
| P90 | 107.71 d | [90.75, 125.86] | [94.89, 122.30] | [100.47, 116.64] |
| P95 | 322.61 d | [283.48, 359.89] | [286.35, 366.86] | [297.74, 348.34] |

Stated plainly:

- **The sample locates the 85th percentile to about ±8 days** once show clustering is respected — `W` is 46 with a defensible range of roughly 38 to 54 on sampling grounds alone. Treating the pairs as independent would have claimed ±3 days, which would have been an overstatement by a factor of about 2.5.
- **The sample does not support a percentile deeper than about the 90th.** P95 carries an interval 76 days wide. Had the flattening criterion selected the 95th percentile, this section would have had to say the sample could not support it.
- **The coverage at a fixed `W = 46` is much better determined than the percentile's location in days**: 85.00% [83.83, 86.09] show-clustered. This is the same heavy tail seen from the other side — coverage is precise, the day count that delivers it is not.

*(Keys: `bootstrap_CI_days_C1`, `bootstrap_CI_coverage_pct_at_W`, `population`.)*

---

## 6. The two curves together, and the size of the transfer assumption

`artifacts/step6-lag-distributions.png`, panels A and B, carry C1 and all shows on the same axes. **The all-shows distribution is plotted SIGNED and UNTRUNCATED**: no truncation at zero, no clipping, no absolute values, no dropped negative rows. Panel A's outermost bins accumulate all mass beyond ±120/180 days so that nothing is invisible, and panel B's ECDF is drawn over the full signed support on a symlog axis, from the most negative lag observed to the most positive.

**The negative mass, by all five D12 buckets, over the 128,099 started pairs of the estimation sample:**

| Bucket | Started pairs | Negative lags | Share | Of those, finale-term | S1-term |
| :--- | ---: | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | — | — | — |
| **C1 all-at-once** | 25,120 | **689** | **2.74%** | 230 (33.4%) | 459 |
| **C2 weekly** | 39,680 | **11,369** | **28.65%** | 10,447 (91.9%) | 921 |
| **C3 faster than weekly** | 18,218 | **7,149** | **39.24%** | 6,839 (95.7%) | 307 |
| **C4 slower than weekly** | 45,081 | **9,753** | **21.63%** | 8,230 (84.4%) | 1,521 |
| **All** | **128,099** | **28,960** | **22.61%** | | |

**That split is the evidence the spec asked for, and it says what it was expected to say.** In the three non-binge buckets between 84% and 96% of the negative mass is **finale-term** — pairs whose clock start is the S2 finale air date and who watched an episode while the season was still airing. That is ordinary live viewing of a weekly show, not viewer behaviour that a window could ever capture, and it is a property of the release schedule. In C1, where premiere and finale coincide, the negative share collapses to 2.74% and two thirds of what remains is **S1-term** — genuine out-of-order viewing, which is D2's small expected group.

**The size of the transfer assumption, in one line:** the 85th percentile is **45.98 days on C1** and **10.60 days on all shows**. D14's assumption is that binge viewers' delay-to-start behaviour transfers to weekly viewers; the two curves are what that assumption is being asked to bridge, and the bridge is a factor of four.

*(Keys: `negative_mass_by_D12_bucket`, `percentiles_days`, `figure`.)*

---

## 7. The `W` range Step 13 must cover

Derived deterministically, by taking **the one percentile used to set `W`** and reading it on both curves:

| Curve | 85th percentile |
| :--- | ---: |
| C1 only | 45.98 d |
| All shows, signed and untruncated | 10.60 d |

> **Step 13's minimum tested range for `W` is 11 to 46 whole days.**

This is a **minimum**, not a recommendation. It is the interval the transfer assumption spans, and Step 13 is free to test wider — §4 above suggests it should, since the criterion's own sensitivity reaches 89 days on the C1 curve, well outside this interval.

*(Key: `step13_W_range`.)*

---

## 8. What the spec does not decide. Reported, not resolved.

Under dual implementation an ambiguity resolved silently is indistinguishable from a bug, so each of these is named with the reading taken and the size of the difference it makes.

### 8.1 D14 says C1 lags cannot be negative. **689 of them are.** — for the Human Lead

D14, and Step 1 §9, both state that on a C1 show every lag is non-negative by construction. **That is not true of the data, and the reason is structural rather than a data defect:** the guarantee holds for the **finale term** of `max()`, and `max()` can select the **S1-completion term** on a C1 show just as it can on any other. A user who watched S2 before finishing S1 has a negative lag whatever the cadence.

| | Pairs |
| :--- | ---: |
| C1 negative lags | **689** (2.74% of the C1 sample) |
| of which **S1-term** — genuine out-of-order viewing, median lag −46.1 d | 459 |
| of which **finale-term** — impossible under C1 and therefore an artifact | 230 |
|  · within 1 day, i.e. the known one-day UTC finale skew of Step 1 §0 | 135 |
|  · beyond 1 day, minimum −495.4 d — unexplained metadata or timestamp defect | **95** |

**No rule anywhere covers these**, because D14 assumed the case away. The anti-truncation rule in the Step 6 spec is written for the all-shows plot.

**The reading taken:** every row is kept at its actual signed value and nothing is repaired, which is the only treatment with textual support — truncation was withdrawn as indefensible and no replacement was authorised. **What the alternatives would cost:**

| Treatment of the C1 negatives | n | P85 | `W` |
| :--- | ---: | ---: | ---: |
| **Kept, signed and untouched (the figure above)** | 25,120 | **45.98 d** | **46** |
| Only the 95 structurally impossible ones dropped | 25,025 | 46.58 d | 47 |
| All 689 negatives dropped | 24,431 | 48.87 d | 49 |

The choice moves `W` by at most 3 days, which is inside the sampling interval of §5, so **it is not load-bearing for the number** — but it is a real defect in D14's stated warrant, and the 95 impossible records are a data-quality finding that Step 8 should expect to meet again.

### 8.2 Three conventions the spec leaves open, each fixed explicitly

| # | Silence | Reading taken | Why it could matter to the diff |
| ---: | :--- | :--- | :--- |
| 1 | The threshold that defines "flattens" | 1.0 pp per 7-day block, first block under it that no later block exceeds | §4 sweep: 82nd–89th percentile, 29–89 days. **This is the single largest degree of freedom in the step** |
| 2 | `W` must be a whole number of days; P85 is 45.975 | round **up** to 46 | ±1 day; rounding down gives 45 and 84.98% coverage |
| 3 | Percentile interpolation | `numpy.percentile`, linear | sub-day on a sample this size |
| 4 | What "all shows" means in the paired plot | the 128,099 estimation sample **without** the C1 restriction | the alternative reading — the 201,900 analysis population — is not computable: a lag requires a clean `T0` and a clean first S2 watch, which is what the estimation sample *is* |

*(Keys: `spec_silence_sensitivity`, `C1_negatives_diagnostic`, `criterion_threshold_sweep`.)*

---

## 9. Limits

1. **The transfer assumption is an assumption, not a finding.** `W` is estimated on 206 all-at-once shows and applied to 1,138. §6 quantifies the stretch; it does not justify it. D14 accepted this cost explicitly.
2. **Observation length truncates the tail slightly.** 1.51% of C1 pairs have fewer than 46 days between `T0` and the pull cutoff, and 1.95% fewer than 91 days. A pair observed for fewer than `W` days cannot exhibit a lag of `W`, so coverage at `W` is very slightly overstated and the true percentile value very slightly larger. Median C1 exposure is 1,915 days, so the effect is small — but it is one-directional and it grows for any larger `W` a robustness arm tries.
3. **This is a stopped pull.** 2,549 complete users of 4,050 planned. Every count here moves if the pull resumes.
4. **206 shows is a small show-level sample** and nothing here controls for what kind of show ends up in C1 — era, platform, genre and season length are uncontrolled, and the show-clustered interval in §5 is the only place that composition enters the arithmetic.
5. **Everything upstream of the lag is inherited.** Distinct episodes not play events, earliest timestamp per episode, set membership in `E2`, first-pass S1 completion, `T0 = max(...)`: all computed by Step 5's committed pair reconstruction under approved Step 1 rules. This step re-derives none of them, which is deliberate — a second implementation of `T0` would put a difference into the dual diff that has nothing to do with `W`.
6. **The Step 5 limitations travel with the sample.** In particular, the estimation sample is clean-record by construction, so it is not a random subset of the study population; it is the subset that can answer a timing question. Ruling 1 accepted exactly that trade.

*(Key: `exposure_check_C1`.)*

---

## 10. Reproduction

**Read-only. Zero API calls.** Run: `.venv/bin/python src/step6_derive_w.py`.

Every figure in this document maps to one key of `artifacts/step6-w-derivation.json`, which `src/step6_derive_w.py` writes. Nothing here was computed in a shell that is not committed.

| Section | Key in `step6-w-derivation.json` |
| :--- | :--- |
| §1 `W`, percentile, coverage at `W` | `CHOSEN`, `bootstrap_CI_coverage_pct_at_W` |
| §2 waterfall, bucket counts, C1 shows and users | `population` |
| §3 weekly gain table, criterion, flattening block | `weekly_gain_C1`, `criterion` |
| §4 threshold sweep | `criterion_threshold_sweep` |
| §5 bootstrap intervals | `bootstrap_CI_days_C1`, `bootstrap_CI_coverage_pct_at_W` |
| §6 negative mass by bucket and binding term | `negative_mass_by_D12_bucket` |
| §6 P85 on both curves, all quoted percentiles | `percentiles_days` |
| §7 Step 13 range | `step13_W_range` |
| §8.1 C1 negatives, and the three treatments | `C1_negatives_diagnostic`, `spec_silence_sensitivity` |
| §9 exposure | `exposure_check_C1` |
| coverage at other candidate windows | `coverage_at_candidate_W` |
| all-shows weekly gains | `weekly_gain_all_shows_first10` |

| File | Role | Git |
| :--- | :--- | :--- |
| `src/step6_derive_w.py` | the whole step | tracked |
| `artifacts/step6-w-derivation.json` | every quoted figure | tracked, aggregates only |
| `artifacts/step6-lag-distributions.png` | the four-panel figure | tracked, aggregates only |
| `processed/step6/pair_lag.csv` | pair-level lags, **keyed to users — never leaves this machine** | ignored |

The script **asserts** the Step 5 waterfall and the presence of a whole percentile inside the flattening block, and fails rather than proceeding if either moves.

---

## 11. Status

**This is a gate and this document is a proposal.** `W` is not set. No downstream step may take 46 days from this file. Step 7 has not begun and its threshold must be derived without using `W` as an input.

On written approval by the Human Lead, this fixes `W` for Step 8's filter order, Step 9's headline, the liveness rule's evaluation point in Step 7, and the range Step 13 must cover.

**Two things the Human Lead should decide with the number, not after it:**

1. **§8.1** — whether C1 negative lags are kept, since D14's warrant says they do not exist. Worth at most 3 days of `W`, but the warrant is wrong either way.
2. **§4** — whether 1.0 percentage point per week is the right definition of "flat". It is the largest free parameter in the step and it moves `W` between 29 and 89 days.
