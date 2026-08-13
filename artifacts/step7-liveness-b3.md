# Step 7 — Liveness threshold and rule (instance b3)

**Status: PROPOSED. This is a gate. Nothing here is adopted.** The Human Lead approves and diffs
the two instances. Zero API calls; the whole step runs on cached data and the stored Step 5
calibration curve, which is read and never refitted.

**Spec read, not paraphrased:** `task-sheet.md` lines 226–275; `decisions/0038`, `0037`, `0036`;
`artifacts/step1-outcome-definition.md` lines 685–710.

---

## 1. The proposed threshold

| | |
| :--- | ---: |
| Reference distribution | bracketing gaps, one per pair |
| Reference population | **152,126** (waterfall line 4) |
| Percentile | **99th** |
| Raw value | **631.8031 days** |
| **PROPOSED THRESHOLD, ceiling** | **632 days** |
| `W` used | 108 days |

All five NumPy percentile methods return 631.8031 to the digit, so the interpolation convention
is not a lever here.

## 2. The rule

> A **user-show pair** is **live** if, on that pair's own account, the gap between the **last
> record-insertion instant at or before `τ1`** and the **first record-insertion instant after
> `τ1`** is **strictly less than 632 days**, where `τ1 = ⟦T0⟧ + 108 × 24h` and `⟦T0⟧` is the UTC
> midnight of `T0 = max(S2 finale air date, S1 completion date)`.
>
> Insertion instants come from the stored Step 5 isotonic play-`id` curve, are **account-wide** —
> every record in the sweep, other shows and movies included — are deduplicated on **exact
> equality only**, and are **never** the claimed `watched_at`.
>
> If there is **no insertion instant after `τ1`**, the pair is **not live**. If there is **no
> insertion instant at or before `τ1`**, the pair is **not live**.
>
> Liveness is a **pair-level** filter. One account can be live for one show and not for another.
> **No user is ever dropped wholesale.**

Exclusion is at `gap ≥ threshold`, the convention `0025` (a) argues the ceiling from. It makes no
difference to the count here: no gap equals 632.0 days exactly, so `≥` and `>` both exclude 1,276.

## 3. The four pair counts

| Outcome | Pairs | Share of 152,126 |
| :--- | ---: | ---: |
| **Live** | **128,354** | 84.37% |
| Not live — measured bracketing gap ≥ 632 d | **1,276** | 0.84% |
| Not live — no insertion instant after `τ1` | **4,246** | 2.79% |
| Not live — no insertion instant at or before `τ1` | **18,250** | 12.00% |
| Excluded, total | 23,772 | 15.63% |

**Realised exclusion rate on measured-gap pairs: 0.9843%** against a stated 1%. The shortfall is
the ceiling — 631.8031 rounds up to 632 and carries 156 pairs back inside. Excluding at the raw
631.8031 would remove 1,432. **Realised exclusion rate on all 152,126 pairs: 15.63%.**

`18,250` reproduces `0037` §3's figure for this bucket on the uncontaminated population exactly.

## 4. Disclosure 1 — the quota property

**Taking the percentile on the distribution the test is applied to sets the level by the exclusion
rate, not by any feature of the data.** Choosing the 99th fixes the exclusion rate at 1% of
measured-gap pairs before anything is measured. The data decides **which** pairs are excluded. It
does not decide **how many**.

632 days is not a property of viewing behaviour. It marks no elbow, no shoulder and no mode in the
gap distribution — panel A of the chart shows the bracketing distribution is smooth and heavy-tailed
right through it. Across the 90th to the 99.9th the threshold moves by a factor of **57**, from 43
days to 2,470 days, while the realised rate tracks `100 − p` exactly:

| Percentile | Threshold | Realised rate on measured-gap pairs |
| ---: | ---: | ---: |
| 90 | 43 d | 9.98% |
| 95 | 125 d | 4.99% |
| 99 | **632 d** | **0.98%** |
| 99.9 | 2,470 d | 0.07% |

Nothing in the data selects a point on that curve. **This is a quota, not a finding**, and it is
the price of a rate that is true as stated — the alternative `0037` withdrew had a level anchored
to typical gap behaviour and an advertised rate wrong by a factor of 37. Measured here on the
frozen population, that withdrawn basis would have excluded **36.96%** of measured-gap pairs
against its stated 1%.

`0036` §1's **conservative-direction** argument survives and still points up: a false-dead removes
a pair, and the liveness exclusion already biases the never-started share **down** (Step 14, bias
2). It gives a direction. **It does not identify a level.**

## 5. Disclosure 2 — the inertness

**At the proposed threshold the measured-gap test does a small minority of the filter's work.** It
excludes **1,276** pairs; `0036` §2.3's two evidence-absence edge cases exclude **22,496**.

| Source of exclusion | Pairs | Share of exclusions |
| :--- | ---: | ---: |
| Measured bracketing gap ≥ 632 d | 1,276 | **5.37%** |
| `0036` §2.3 edge cases | 22,496 | **94.63%** |

**A reader must not take the threshold to be doing work it is not doing.** The liveness filter is
overwhelmingly two rulings about *absent* evidence, not a measurement of observed silence. Whatever
the Human Lead sets the threshold to, the filter's effect on the headline will be dominated by the
18,250 pairs whose window closed before their account existed on the insertion clock.

### 5.1 Defect: the stated invariance does not reproduce

The launch brief and `decisions/0038` §5 state the split as **3.45% / 96.55%** and say it **holds
across every percentile from the 90th to the 99.9th**. **Both halves fail on the frozen
population.**

- **The level.** 3.45% was measured on a different reference population. On the 152,126 at the
  99th it is **5.37% / 94.63%**.
- **The invariance.** The share is not flat. It runs **36.52%** at the 90th, 22.32% at the 95th,
  5.37% at the 99th and **0.39%** at the 99.9th — a 93-fold range.

**The mechanism makes the invariance arithmetically impossible.** The edge-case count is
**constant in the percentile** — 22,496 at every level, because it depends only on `W` — while the
measured-gap count is `100 − p` percent of 129,630 and falls by two orders of magnitude across that
span. A ratio of a falling quantity to a fixed one cannot be invariant.

**The substantive point stands and is stated in §5 above.** The invariance is not a property of the
data and must not be published as one. Reported as a defect in `0038` §5, not repaired here.

## 6. The threshold is a function of `W` — Step 13 arms refitted

| `W` | Threshold | Measured-gap pairs | Excl. measured | No instant after `τ1` | No instant ≤ `τ1` | Live | Realised rate |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 46 | **576 d** | 130,013 | 1,295 | 2,881 | 19,232 | 128,718 | 0.996% |
| 77 | **590 d** | 129,929 | 1,292 | 3,539 | 18,658 | 128,637 | 0.994% |
| **108** | **632 d** | 129,630 | 1,276 | 4,246 | 18,250 | 128,354 | 0.984% |
| 150 | **662 d** | 129,378 | 1,274 | 4,930 | 17,818 | 128,104 | 0.985% |
| 213 | **697 d** | 128,567 | 1,281 | 6,278 | 17,281 | 127,286 | 0.996% |

Population is the same 152,126 at every arm; only `τ1` moves. The threshold rises monotonically
with `W`, **576 → 697 days**, confirming `0038` §6. `W` and the threshold are **not independent
robustness axes**: a threshold frozen at 632 would deliver its stated 1% at exactly one arm.

Note the **direction of the edge-case shift**: as `W` rises, `τ1` moves later, so the
"no instant after `τ1`" bucket grows (2,881 → 6,278) and the "no instant at or before" bucket
shrinks (19,232 → 17,281). Total exclusions rise with `W`, 23,408 → 24,840.

## 7. Corroborations against the decision log

| Quantity | Logged | Measured here | |
| :--- | ---: | ---: | :--- |
| Pooled gap median | 0.0000006 d | 0.0000007 d | agrees to logged precision |
| Pooled 99th | 3.4432 d | 3.4432 d | exact |
| Median gaps per account | 7,812 | 7,812 | exact |
| "No instant ≤ `τ1`" on uncontaminated pop. | 18,250 | 18,250 | exact |
| Bracketing share above pooled 99th | 37.4% | 36.96% | different population; agreement in kind |
| Whole-sweep trip probability, median account, 99th | ≈ 1 | 1.000 | `0037` §2 confirmed |

**Waterfall asserted:** 201,900 → 178,165 → 155,131 → **152,126** → 128,099. I am on **line 4**,
and derivation and application populations are **identical**.

## 8. Sensitivities, reported and not adopted

- **Weighting.** One gap per distinct `(account, gap)` instead of one per pair gives 94,031 gaps
  and a threshold of **190 days**, which would exclude **3.53%** of measured-gap pairs. `0038` §3
  rules one-per-pair; the alternative is recorded because it remains the largest single lever in
  the step. The mechanism is measurable: **34.4%** of pairs share their bracketing gap value
  exactly with at least one other pair, and the largest such group is **298** pairs — accounts with
  many shows whose `τ1` all land in one silence.
- **Bootstrap.** i.i.d. over pairs: 95% CI **[631.80, 645.08] d**, sd 3.56 d. The lower bound
  equals the point estimate because that quantile sits on a tie group. Clustered by account — the
  honest unit, since gaps within an account are not independent — the CI widens to
  **[528.04, 786.71] d**. **The account-clustered interval is the one to read**, and it spans 259
  days: the threshold is far less precisely determined than the point estimate suggests.

## 9. What the two buckets actually are

- **No instant after `τ1` (4,246).** **3,352 of them — 78.9% — have `τ1` after the pull date.**
  That is **right-censoring, not silence**: the window closes after the data ends. Step 7 derives
  on an uncensored population, and `0029` places right-censoring at Step 8 position 5 and liveness
  at 6, so this bucket is inflated here by pairs D10 removes before liveness ever runs. Only 894
  are genuine post-`τ1` silence within the observed span.
- **No instant at or before `τ1` (18,250).** The median pair's `τ1` falls **1,809 days before**
  its account's first-ever insertion instant, and **5,291 have `τ1` before the calibration curve
  even starts (2012-12-02)**. Per `0037` §3 these are **not absent users**; they are pairs whose
  window closed before the account existed on the insertion clock, because `T0` is built from
  claimed `watched_at` while liveness runs on insertion time. Recorded, not repaired; it routes to
  Step 14.

## 10. Judgement calls the frozen spec still does not settle

Stated so the diff can attribute any divergence.

1. **The reference set is the measured-gap pairs only (129,630), not all 152,126.** Edge-case pairs
   contribute no gap. Treating "no instant after `τ1`" as an infinite gap is **not available**:
   those pairs are 3.17% of the extended set, so the 99th percentile would be infinite. The choice
   is forced, but the spec does not say it.
2. **Exclusion at `≥` threshold**, from `0025` (a)'s wording. Zero-impact here.
3. **The ceiling is taken on the value in days**, giving whole-day thresholds. Ceiling at any finer
   resolution would give 631.8032 d and 1,432 exclusions.
4. **"Every record in the account's sweep" is read literally** — all 27,656,813 records, both
   `kind` values and all actions. No restriction to episodes, to the show under study, or to
   real-time actions.
5. **The calibration curve is applied verbatim as `np.interp`**, per `step5_calibrate.insert_time`,
   which **clamps** outside the knot range. 1,862 records fall below the first knot and 5,094 above
   the last (0.025% together); each clamped run collapses to a single instant under the exact-tie
   rule. The curve is a required input and is not refitted, so this is reported rather than fixed.
6. **Ties collapse within an account only.** Equal instants on two different accounts are two
   instants. `0037` §4 says "for each account", which implies this but does not state it.
7. **Percentile interpolation is NumPy's default `linear`.** All five methods agree to the digit
   here, so this cannot be the source of a diff.

## 11. Provenance

- Chart: `artifacts/step7-gap-distribution-b3.png`
- Machine-readable: `artifacts/step7-liveness-b3.json`
- Row-level, kept out of `artifacts/`: `processed/step7/b3/instants.npz`,
  `processed/step7/b3/bracket.npz`, `processed/step7/b3/pair_liveness_W108.csv`,
  `processed/step7/b3/threshold.json`, `processed/step7/b3/diagnostics.json`,
  `processed/step7/b3/population_meta.json`, `processed/step7/b3/instants_meta.json`
- Scripts: `src/step7_b3_instants.py`, `src/step7_b3_bracket.py`, `src/step7_b3_threshold.py`,
  `src/step7_b3_diag.py`, `src/step7_b3_figures.py`
- 27,656,813 records → 25,864,798 distinct insertion instants (6.48% collapsed by exact tie) →
  25,862,249 pooled gaps across 2,549 accounts.
