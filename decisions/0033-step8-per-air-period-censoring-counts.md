# Decision 0033 — Step 8 reports retained-pair counts per air period after right-censoring; the discard-rate anomaly goes to Step 14

| | |
| :--- | :--- |
| **Decision** | **Step 8 must report retained-pair counts per air period after right-censoring**, for every `W` arm Step 13 tests, not only in aggregate. **The non-homogeneous discard rate is recorded as a Step 14 limitation, not fixed.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 8 and Step 14 |
| **Closes** | The Product review's **finding 5** ask, and disposes of the Engineering review's **finding E residual** |
| **Status** | Closed |

---

## 1. Per-air-period censoring counts — Product finding 5

Step 8 already requires right-censoring removal to be reported as two lines, the `max(W, 91)` term
and the incremental `+ H` term. **Both are aggregates, and the aggregate conceals the thing that
matters.**

At `W = 108`, censoring retains **97.6%** of pairs — a number that reads as harmless. It is not
distributed harmlessly:

| Air period | Pairs kept at `W = 108` | at `W = 213` |
| :--- | ---: | ---: |
| pre-2020 | 98.0% | **97.3%** |
| 2020–2022 | 97.5% | 96.4% |
| **2023–2025** | 96.0% | **89.7%** |

**The loss falls on the uncapped `S1_completion_date` term** and is therefore cohort-asymmetric: a
2025 title's retained pairs are only those who completed S1 by October 2025, and those are early
adopters — **the users likeliest to continue**. So the modern cohort is not merely smaller after
censoring but **differently selected**.

**Why it must be per-arm and not once.** The asymmetry *widens with `W`*, and
[0027](0027-step13-w-arms-above-the-adopted-value.md) extended the arms to 213 precisely to probe the
censoring bias. A single aggregate reported at the adopted `W` would show 97.6% and say nothing about
the arm where the modern cohort loses more than one pair in ten.

**What it costs:** one `groupby` on a table Step 8 is already building. Zero API calls, no new
privacy surface — `air_period` is a show field and the counts are aggregates.

**What it does not fix.** The reviewer was explicit that finding 5's underlying problem is not
fixable: the 2023–2025 cohort is **168 shows**, and within it the release-strategy comparison lands
in cells of **C1 45 / C2 38 / C3 59 / C4 26**. Nothing in Step 8 changes that. **This line makes the
survival visible; it does not make the cohort larger.** The reviewer's stated intention at Step 15 —
to ask whether the decision rule's action is stated at a confidence the 2023–2025 evidence supports —
stands untouched and is recorded in `artifacts/partner-reviews-steps-2-and-4.md` §1.

## 2. The discard-rate anomaly — Engineering finding E residual

The Engineering review tested whether the sweep-completeness discard rate tracks sweep size, because
if it did, the heavier remaining 30% of the pool would discard faster and the resume projection would
be wrong. **It does not**, and the test produced a different finding.

Per-bin discards across the ten history-volume strata:

| Bin | 0 | 1 | 2 | 3 | 4 | **5** | 6 | 7 | 8 | 9 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Discards | 20 | 27 | 34 | 30 | 26 | **44** | 31 | 18 | 22 | 35 |

Roughly 284 attempted per bin, pooled rate **10.1%**, range **6.3% to 15.5%**. **Bin 5 is roughly
+3 SD** on a binomial at p = 0.101, n = 284.

**The useful half of this is what it rules out.** There is **no monotone trend** across bins spanning
forecasts from 1 to 292 pages, so **sweep length is not the mechanism** — the obvious candidate, and
the one that would have mattered for pricing a resume. That is a real result and it is why ~10%
remains safe planning for the remainder.

**What is left is unidentified, and this study does not establish it.** The residual is not noise —
+3 SD is not noise — but nothing in the data distinguishes between a property of those accounts, a
property of the header behaviour on that size class, or something else.

**Why it is a limitation and not a fix.** It **compounds** with a defect already on the record: the
discard is **not outcome-neutral** ([0023](0023-step4-completeness-rule-upheld.md), +1.27 points on
has-any-S2, CI [0.87, 1.66]). A selection mechanism that is both outcome-correlated **and
unexplained** cannot be argued to be harmless — the argument would require knowing what it selects
on. Recording it is what keeps that gap visible.

**Investigating it would not be free**, which is the other half of the reason. It would mean going
back to the raw pages of the 287 discards to characterise them against the 2,549, and that is the
same class of work `0023` declined on cascade cost. The reviewer said so itself: *"a lead for the
Step 14 limitation, not a throughput problem, and I am not taking it further."*

## 3. Scope

- **No result changes.** No threshold, population or number moves. Step 8 gains a required output;
  Step 14 gains a limitation.
- **Both partner reviews are now fully disposed.** Product findings 1–5 and the Step 15 warning;
  Engineering findings A–G. The record is `artifacts/partner-reviews-steps-2-and-4.md`, and §4 of
  that file lists what remained open before this entry.
- **Step 8 has not launched.** It is an unapproved gate and a dual pair, so this line is in the spec
  the two isolated instances will read — per item 23, propagated at the time of the ruling rather
  than at launch.
