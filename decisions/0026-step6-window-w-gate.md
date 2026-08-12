# Decision 0026 — Step 6 window `W` APPROVED at 108 days (gate 3 of 5)

| | |
| :--- | :--- |
| **Decision** | **Step 6 is approved. `W = 108 days`.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Gate** | 3 of 5. Unblocks Step 7 and Step 8, each itself an unapproved gate |
| **Deliverables** | `artifacts/step6-window-w-a.md` and `artifacts/step6-window-w-b.md`, the two isolated instances |
| **Rule** | 90th percentile ([0024](0024-w-is-the-90th-percentile.md)), continuous lag, ceiling ([0025](0025-lag-unit-and-ceiling.md)) |
| **Status** | Closed |

> **Approval record.** Approval was given by the Human Lead in writing in this session, on
> 2026-08-12. No agent recorded it on its own authority and no agent adopted its own proposal. Two
> isolated `data-scientist` instances produced the deliverables; neither approved anything.

---

## The number

> **`W = 108 days`** — the ceiling of the 90th percentile of the continuous lag from clock start to
> first S2 episode, on the **C1 subset (25,120 pairs)** of Step 5's **128,099** clean-record
> estimation sample.

The true percentile is **107.7135 days**. `W = 108` covers **90.020%** of C1 started pairs under the
approved test `watched_at < τ1`; `W = 107` covers 89.976% and misses the target.

**`W` applies to all pairs**, not only to C1. Estimation sample and application population differ
deliberately, per D14 and as restated in `task-sheet.md` Step 6.

## What the dual run established

Run 2's two instances agreed on **every figure to fifteen significant digits** and differed only in
the lag unit, which [0025](0025-lag-unit-and-ceiling.md) has now fixed. That agreement is the
evidence for the number: the derivation is not one instance's arithmetic.

- C1 subset: **25,120 pairs, 206 shows, 2,050 users**
- Both instances reproduced Step 5's waterfall (201,900 → 178,165 → 155,131 → 152,126 → 128,099) and
  asserted on it before computing
- **Zero API calls**, both instances

## What travels with the number

**Four things the Human Lead should carry forward with `W`, all reported by both instances.**

### 1. The precision is dominated by clustering, not sample size

25,120 pairs come from only **206 shows**, and the show is the binding cluster. The iid interval is
about ±8 days; the show-clustered interval is **[89, 125]** (instance A) and **[89.8, 122.4]**
(instance B). **The defensible statement is `W = 108`, roughly ±18 days at 95%** — not the decimals.
Treating pairs as independent would overstate precision by roughly 2.5×.

### 2. The percentile is an imported convention, not a property of the data

The C1 survival curve is close to scale-free past about day 7 — log-log slope −1.1 to −1.5 across
every decade from a week to four years. Moving from the 85th percentile to the 90th buys **61.7
days**. Nothing in the distribution selects 90; it comes from attribution-window practice
([0024](0024-w-is-the-90th-percentile.md)) and is labelled as such wherever it appears.

### 3. Right-censoring runs one-sided against `W`

The 90th percentile rises monotonically with exposure: **107.7 → 119 (≥1 yr) → 128 (≥2) → 146 (≥4) →
213 (≥8, n = 4,141)**. Exposure and cohort are not separable on the data, so **213 is an upper bound,
not a rival estimate.** Neither instance proposed an adjustment. Direction: **a larger `W` moves the
never-started share down.**

Consequence for Step 13, flagged by instance A as a proposal only: the mandated arms currently span
46 to 107 ([0024](0024-w-is-the-90th-percentile.md)) plus the two-curve range, which now reads
**[38, 108]** under the ceiling rule. **`W = 108` sits at the top of that span**, so the sensitivity
does not currently test above the adopted value. Whether Step 13 gains an arm above 108 is not
decided here.

### 4. D14's warrant is false, and 95 negatives are unexplained

`decisions/0003` D14 and Step 1 §9 both assert every C1 lag is non-negative by construction.
**689 are negative (2.74% of C1)**, found with identical counts by both instances: **459** bind on
the S1-completion term — `max()` can legitimately select it on a C1 show, so the warrant only ever
covered half the operator — and **230** bind on the finale, of which 135 are the known one-day UTC
skew and **95 are unexplained, out to −495 days**. Dropping all 689 would move `W` from 107.71 to
113.99, about 6 days, so it is **not load-bearing for the number**. The warrant is false either way.
Carried as open item 24.

## One conflict between approved documents, reported and not resolved

Both instances found that **4 pairs in the 128,099 have a first S2 record at or after `τ_pull`**,
which Step 1 D11 says must be discarded from every computation, while Step 5 built the sample
without that filter. Both retained them, because the spec directs taking the population from the
Step 5 artifact.

**None is in C1, so `W` is unaffected.** But Step 8 classifies on the 201,900 and will apply the
frozen cutoff, so **Step 6 and Step 8 will not share a row set.** Neither instance resolved it and
neither should have. Recorded as open item 27.

## What this unblocks

| Step | Takes from Step 6 |
| :--- | :--- |
| **Step 7** — liveness threshold | `W` is not an input to the derivation, per its own spec, but the liveness *rule* composes with `W`: a pair is live on activity after its clock start **plus `W`** |
| **Step 8** — analysis table | `W = 108` sets `τ1 = ⟦T0⟧ + 108 × 24h`, the operator that assigns every outcome state |
| **Step 13** — robustness | arms spanning at least [38, 108] ∪ [46, 107]; see §3 on whether that is enough |

Steps 7 and 8 are unapproved gates. Step 7 runs twice under `data-scientist` and `data-scientist-b`;
Step 8 runs twice under `analytics-engineer` and `analytics-engineer-b`. **Both pairs need distinct
output namespaces** per open item 25.

**The frame `W` was derived on remains a stopped pull** — 2,549 users of 4,050 planned. If it
resumes, the estimation sample grows and `W` is re-derived.
