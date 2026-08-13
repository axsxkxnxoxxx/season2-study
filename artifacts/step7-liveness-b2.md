> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — liveness threshold, instance `b2` (rerun on the corrected reference distribution)

**Status: PROPOSAL. This is a gate. Nothing here is adopted.** The Human Lead approves and diffs the
two instances. Zero API calls; everything below runs on cached data and the stored Step 5 calibration
curve, which was read and not refitted.

| | |
| :--- | :--- |
| Spec | `task-sheet.md` Step 7; `decisions/0036` §2 (unchanged); `decisions/0037` (withdraws `0036` §1's basis, fixes the gap unit) |
| `W` used only to place `τ1` | 108 days (`decisions/0026`) |
| Step 5 waterfall reproduced and asserted | 201,900 → 178,165 → 155,131 → 152,126 → 128,099 |
| Chart | `artifacts/step7-gap-distribution-b2.png` |
| Machine-readable | `artifacts/step7-liveness-b2.json` |
| Row-level detail (not public) | `processed/step7/b2/` |

---

## 1. The proposed threshold

> **99th percentile of the bracketing-gap distribution = 913.3559 days → ceiling → `THRESHOLD = 914 days`.**

Bootstrap 95% interval on the 99th percentile (400 resamples, seed 20260813): **907.16 – 959.28 days**,
i.e. 908 – 960 after ceiling. The point estimate is not sharp at the third significant figure.

## 2. The rule statement

> A **user-show pair** counts as **live** if, on the account's whole sweep — every record it has,
> other shows and movies included — there is an insertion instant at or before that pair's
> `τ1 = ⟦T0⟧ + 108 × 24h` **and** an insertion instant after it, **and** the difference between those
> two instants is **strictly under 914 days**.
>
> A pair is **not live** if that bracketing gap is **914 days or more**, or if there is **no insertion
> instant after `τ1`**, or if there is **no insertion instant at or before `τ1`**.
>
> Liveness runs on **insertion instants**, never on claimed `watched_at` (`decisions/0021`). It is
> anchored at **`τ1` only**; `τ2` plays no part (`decisions/0034`). It is a **pair-level** filter: the
> evidence is account-wide but the test instant is pair-specific, so **no user is ever dropped
> wholesale**. On this data 1,647 of 2,481 accounts (66.4%) come out live for some of their pairs and
> not live for others — the pair-level property is not theoretical here, it is the majority case.

## 3. The gap unit (`decisions/0037` §4), applied exactly

| | |
| ---: | :--- |
| Records in the sweep | 27,656,813 |
| Distinct insertion instants after collapsing runs of **exactly** equal instants | 25,864,798 |
| Records collapsed | 1,792,015 (6.48%) |
| Accounts | 2,549 |
| Median gaps per account | 7,812 |

No rounding, no bucketing, no per-second or per-day dedupe. Sub-second gaps between genuinely distinct
instants were retained. Insertion instant = `np.interp(rid, knot_rid, knot_time)` on the stored curve.

**Reproducibility check on the fixed unit.** The pooled 99th percentile under this operation comes out
at **3.4432 d → 4 days**, which is exactly the figure `0037` §4 records instance A reading in the
previous run. The ambiguity that produced a four-day divergence appears to be closed.

## 4. Pooled versus bracketing — what the correction does

| | Pooled (withdrawn basis) | Bracketing (corrected basis) |
| :--- | ---: | ---: |
| n | 25,862,249 gaps | 157,995 gaps |
| Median | 0.0000007 d | **2.0101 d** |
| 75th | 0.0251 d | **9.0346 d** |
| 99th | **3.4432 d** | **913.3559 d** |
| Threshold after ceiling | 4 d | **914 d** |

**Realised failure rate on measured-gap pairs:**

| Threshold | Failure rate |
| :--- | ---: |
| Pooled 99th, 4 d (the withdrawn basis) | **37.3936%** |
| **Bracketing 99th, 914 d (proposed)** | **0.9937%** |

The 37.3936% reproduces the 37.4% published in `0037` §1 to the reported precision, on the corrected
gap unit. **The correction does what it was meant to do: the stated rate and the delivered rate now
agree.** Raising the reference to the test statistic's own distribution moves the failure rate from
37.4% to 0.99%, and the threshold from 4 days to 914.

For contrast, no pooled percentile repairs this: the pooled 99.9th (20 d) still fails 18.21% and the
pooled 99.99th (145 d) still fails 7.01%.

## 5. Rule application — the four counts, reported separately

**On the 201,900-pair analysis population, at `W = 108` and threshold 914 days:**

| Class | Pairs | Share |
| :--- | ---: | ---: |
| **Live** | **156,425** | 77.48% |
| Not live — measured gap ≥ threshold | **1,570** | 0.78% |
| Not live — no insertion instant **after** `τ1` | **5,209** | 2.58% |
| Not live — no insertion instant **at or before** `τ1` | **38,696** | 19.17% |
| Not live, total | 45,475 | 22.52% |

**On the Step 5 clean estimation sample (128,099):** live 122,560 (95.68%); measured-gap failures 381;
no instant after `τ1` 4,120; no instant at or before `τ1` 1,038.

Failing measured gaps are not marginal: their minimum is 923.1 days, median 1,405.8, maximum 3,196.3.
Nothing sits just above the threshold, so the ceiling from 913.36 to 914 changes no pair's class.

## 6. Findings that the Human Lead needs before ruling

### 6.1 The percentile has stopped being an estimate and become a quota

Under the withdrawn basis the percentile was measured on one distribution and applied to another —
that was the defect. Under the corrected basis it is measured on **the same** distribution it is
applied to, and the consequence is arithmetic: **choosing percentile `p` sets the exclusion rate to
`100 − p` percent of measured-gap pairs, whatever the data look like.** The threshold is no longer
identified by any feature of the distribution; only the exclusion rate is being chosen, and the
threshold is whatever number delivers it.

| Percentile | Threshold (d) | Realised failure rate |
| ---: | ---: | ---: |
| 90 | 82 | 9.95% |
| 95 | 241 | 4.99% |
| 97.5 | 471 | 2.50% |
| **99** | **914** | **0.99%** |
| 99.5 | 1,405 | 0.50% |
| 99.9 | 2,937 | 0.02% |

This is not an argument against the correction — the correction is right, and `0036` §1's arithmetic
was wrong. It is a statement of what is left to decide. **`0036` §1's conservative-direction argument
survives intact and points the same way**: a false-dead removes a pair and the liveness exclusion
already biases the never-started share down, so the higher percentile is the conservative one. I make
no recommendation beyond reporting the grid; the 99th is what the spec names and what I computed.

### 6.2 At 914 days the threshold is close to inert, and the edge cases do the work

914 days means an account that went silent for two and a half years across `τ1` still counts live.
Of the 45,475 pairs the filter excludes, **3.45% fail on a measured gap and 96.55% fail for absence of
evidence** — the two edge-case rules in `0036` §2.3, which the threshold does not touch. Whatever
percentile is chosen between the 90th and the 99.9th, the filter's behaviour is dominated by the edge
cases, not by the threshold. That is worth knowing before the threshold is debated further.

### 6.3 The corrected reference distribution is a function of `W`, and the spec says it must not be

`task-sheet.md` Step 7 line 235 says "Derive the threshold independently. Do not use `W` as an input
to the derivation," and `0036` §3 repeats it: "the threshold is derived independently of `W`, though
the test instant is a function of it." **That separation no longer holds.** `0037` §1 makes the
reference distribution the set of gaps bracketing `τ1`, and `τ1 = ⟦T0⟧ + W × 24h`. The reference
distribution is therefore selected by `W`, so the threshold is a function of `W` by construction.

Measured — the 99th percentile of the bracketing distribution at each Step 13 `W` arm:

| `W` | 46 | 77 | 91 | 108 | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 99th percentile (d) | 884.85 | 897.12 | 911.46 | **913.36** | 962.77 | 972.72 |
| Threshold (d) | 885 | 898 | 912 | **914** | 963 | 973 |

The dependence is real but mild — 10% across a 46-to-213 span — so this is a **specification conflict
to be resolved, not a numerical emergency**. It matters most for Step 13: if the threshold is refitted
at each `W` arm the robustness check varies two things at once, and if it is held at 914 the stated
1% rate is not delivered at the other arms. **I flag it and do not resolve it.**

### 6.4 Right-censoring is inside the "no instant after `τ1`" bucket

**3,684 of the 5,209** pairs with no insertion instant after `τ1` have a `τ1` that falls **after the
pull date** (2026-08-11, `decisions/0011`). There cannot be an instant after `τ1` for those pairs;
that is censoring, not silence. The rule as written scores them not live and I applied it as written.
Recorded, not repaired — it belongs with D10's right-censored population at Step 9.

### 6.5 The 38,696 bucket reproduces `0037` §3

19.17% of the analysis population, falling to 1,038 in the 128,099 clean sample. Same figures as the
previous run. `0037` §3 already routes this to Step 14 as a clock-mismatch limitation; nothing here
changes it.

## 7. Judgement calls the spec did not settle

Each of these is a place where an honest second instance could have gone the other way. They are
reported rather than resolved, because that is what the dual run is for.

1. **Which population's bracketing gaps form the reference distribution.** The spec names the
   bracketing distribution but not whose. I took the **full 201,900 analysis population**, on the
   reasoning that "the rate the rule delivers" (`0037` §1) is a rate over the population the rule is
   applied to. The alternatives move the threshold a long way:

   | Reference population | Measured-gap pairs | 99th (d) | Threshold (d) |
   | :--- | ---: | ---: | ---: |
   | **Analysis population, 201,900 (taken)** | 157,995 | 913.36 | **914** |
   | Clean-`T0` subset | 149,257 | 701.51 | 702 |
   | Step 5 estimation sample, 128,099 | 122,941 | 503.08 | 504 |

   Contaminated `T0` places `τ1` in the wrong place and lands it in long gaps, so including those pairs
   inflates the threshold by roughly 30%. **If the other instance chose the clean subset or the 128,099
   sample, the diff will show 702 or 504 and that is a spec ambiguity, not a bug.**

2. **Weighting: one gap per pair, or one per distinct gap.** I weighted **per pair**, because the rule
   is applied per pair and the delivered rate is a per-pair rate. Deduplicating to distinct
   `(account, gap)` gives n = 111,456, a 99th percentile of 201.90 → **202 days**, which would fail
   5.59% of pairs. **This is the largest single divergence risk in this step: 914 versus 202.**

3. **Strict versus inclusive comparison.** I read "gaps under the threshold" (task sheet) and "excludes
   a gap at or above the threshold" (`0025`) as **live iff gap < threshold**. Immaterial here — the
   smallest failing gap is 923.1 days — but it must be stated.

4. **Percentile estimator.** `numpy` default, linear interpolation between order statistics. At
   n = 157,995 the choice of estimator is worth well under a day; it is stated because it is not
   specified.

5. **Ceiling to whole days.** `0025` says ceiling but not to what unit. I ceiled to **whole days**,
   following Step 6's precedent and `0037` §4's own "3.4432 d → 4 days" phrasing. Ceiling to the
   continuous unit would be a no-op.

6. **Calibration outside the curve's support.** `np.interp` clamps. 1,862 records sit below the
   curve's first knot and 5,094 above its last; all of them take the endpoint instant. Because the
   collapse rule is exact equality, the clamped records within an account collapse to a single instant,
   which is the behaviour I would want, but it is an artefact of clamping rather than a decision.

7. **The stated rate is conditional.** 0.99% is the failure rate **among pairs that have a measured
   gap** (157,995), not among the 201,900. Pairs with no measured gap cannot enter a distribution of
   gaps, so the percentile cannot speak to them. Against the whole population the measured-gap failure
   rate is 0.78%.

8. **The reference distribution was computed at `W = 108`,** the adopted value — see §6.3.

## 8. Compliance

- **Zero API calls.**
- Calibration curve **read, not refitted**.
- Step 5 waterfall asserted in code; the run aborts on drift.
- `artifacts/` holds counts and aggregates only. Row-level output is in `processed/step7/b2/`.
- Threshold derived, not adopted. This instance did not read, list or reference any other instance's
  output.

**Scripts:** `src/step7_b2_instants.py`, `src/step7_b2_bracket.py`, `src/step7_b2_threshold.py`,
`src/step7_b2_diag.py`, `src/step7_b2_emit.py`.
