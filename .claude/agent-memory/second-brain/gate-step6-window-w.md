---
name: gate-step6-window-w
description: Full arc of the Step 6 window gate — two dual runs, the 2.3x divergence that withdrew "flattens", the one-day divergence that fixed the lag unit and the ceiling, W=108 approved as decisions/0026, and the four things that must travel with the number
metadata:
  type: project
---

# Step 6 gate — CLOSED. Gate 3 of 5. `W = 108 days`.

**Fact of record: `decisions/0026-step6-window-w-gate.md` records the Human Lead approving
`W = 108 days` in writing on 2026-08-12.** Deliverables are `artifacts/step6-window-w-a.md` and
`artifacts/step6-window-w-b.md`, the two isolated instances. The approval record states that neither
instance approved anything. I do not record approvals; I carry the fact and its citation.

> **`W = 108`** — the **ceiling** of the **90th percentile** (107.7135) of the **continuous** lag
> from clock start to first S2 episode, on the **C1 subset — 25,120 pairs, 206 shows, 2,050 users**
> — of Step 5's 128,099 clean-record sample. **Applies to all pairs.**

`W = 108` covers **90.020%** of C1 started pairs under `watched_at < τ1`; `W = 107` covers
**89.976%** and misses the target the rule asks for.

## Two dual runs. Both found something a single run could not have.

**This is the strongest evidence the dual-implementation regime has produced, and it is the reason
to keep paying for it.** Neither finding was visible in the spec, and neither instance was wrong.

### Run 1 — `W = 46` vs `W = 107`, 61 days and a factor of 2.3 apart

The spec said *"set W at the percentile where the curve flattens"* and never defined "flattens."

| | Instance A | Instance B |
| :--- | ---: | ---: |
| Estimation sample / C1 pairs | 128,099 / **25,120** | 128,099 / **25,120** |
| C1 negatives / C2 negatives | **689** / **11,369** | **689** / **11,369** |
| "Flat" read as | first week buying < 1.0 pp coverage | marginal day buying < 0.05% of sample |
| Percentile selected | 85th | 90th |
| **`W`** | **46** | **107** |

**Every input matched to the pair. The divergence isolates to a single undefined word.** And it is
**not a parameterisation difference** — instance A's own sensitivity sweep runs 29 to 89 days across
a fourfold change in its threshold and never reaches 107. The two criteria differ **in kind**: one
measures coverage bought per *week*, the other per *day*.

**Both instances then found, independently, why the instruction could not have worked.** Past
roughly day 7 the C1 lag density is **close to scale-free — log-log slope −1.1 to −1.5 across every
decade from a week to four years.** There is no break to read. The only genuine elbow is at day 7,
and `W = 7` is plainly not the window this study wants. **The spec asked for a feature the
distribution does not have**, so any instance obeying it had to invent a criterion, and the
criterion — not the data — then set the number.

Resolved by **`0024`**: `W` is the **90th percentile**, full stop. Two properties matter more than
the value: it is **unambiguous**, so a future divergence can only be a bug; and it is **a convention
and is labelled as one**. Run 1 is preserved at commit `9c5fbd3` and its artifacts were **removed
from the working tree** so they cannot be mistaken for deliverables. Verified: no live reference to
them anywhere in the repo.

### Run 2 — `W = 107` vs `W = 107.7135`, exactly one day apart

Under the fixed percentile the two instances agreed **to fifteen significant digits on every
figure** — C1 negatives share `0.027428343949044587` on both — and diverged only on **the unit of
the lag**. The apparent disagreements were the same numbers twice:

**−3,248 is `floor(−3247.4382)`. 113 is `floor(113.9854)`. 37 is `floor(37.6967)`.**

Instance A measured whole days and verified that calendar-date difference equals
`floor(instant difference)` on every row, so its percentile was exactly 107.0 under **all eight**
standard conventions with no rounding step to disclose. Instance B measured the instant difference,
got 107.7135, and **declined to resolve the rendering, predicting the outcome exactly**: *"if the
two instances differ by exactly one day, that is the spec gap and not a derivation divergence."*

Resolved by **`0025`**: the lag is a **continuous instant difference** and `W` is the **ceiling**.

**The argument is coherence with the operator, not rounding taste.** Step 1 §2.4 / D13 fix
`τ1 = ⟦T0⟧ + W × 24h` with membership `watched_at < τ1`, so a pair is covered **iff its fractional
lag is strictly less than `W`**. Flooring records a pair whose true lag is in `[107, 108)` as "107"
while the test excludes it from a `W = 107` window. **The estimator and the operator disagree, and
the disagreement is one-directional.**

## The pattern all three findings share — README item 26

> **A convention doing work the data does not do, left unstated in the spec.**

1. "The percentile where the curve flattens" — undefined, and there was no feature to read.
2. The 90th percentile itself — imported from attribution-window practice, not selected by the data.
3. The unit of the lag and the rounding of the percentile.

**Each was caught only because two isolated instances ran the same words and produced different
numbers. None would have been visible in a single run**, and the first two were not visible in the
spec either. README item 26 says to expect the same shape at Steps 7 and 8 — and it is already
there: see [[open-items-and-contradictions]] Z1.

## Four things that must travel with `W = 108`

Both instances reported all four independently.

**1. The precision is dominated by clustering, not sample size.** 25,120 pairs come from only **206
shows**, and the show is the binding cluster. iid interval ±8 days; **show-clustered [89, 125]
(A) and [89.8, 122.4] (B)**. **The defensible statement is `W = 108`, roughly ±18 days at 95% — not
the decimals.** Treating pairs as independent overstates precision by ~2.5×. No single show carries
it: the largest is 4.2% of pairs, and dropping any of the ten largest moves the p90 only 103–109.

**2. The percentile is an imported convention.** Moving from the 85th to the 90th buys **61.7
days** (46 → 107.7). Instance A's own line: *"Anyone defending 107 out loud has to be willing to say
that 88 and 130 were one percentile point away in each direction."* p85 = 46, p89 = 88, p90 = 107.7,
p91 = 130, p95 = 322.

**3. Right-censoring runs one-sided against `W`.** The p90 rises monotonically with exposure:
**107.7 → 119 (≥1 yr) → 128 (≥2) → 146 (≥4) → 213 (≥8, n = 4,141)**. 530 C1 pairs (2.11%) have less
exposure than `W` itself and cannot contribute a long lag. **213 is an upper bound, not a rival
estimate** — exposure and cohort are not separable, since the long-exposure subset is also an
older-show subset. Neither instance proposed an adjustment. **Direction: a larger `W` moves the
never-started share down.** Now tested by `0027`'s arms at 150 and 213.

**4. D14's warrant is false, and 95 negatives are unexplained.** `0003` D14 and Step 1 §9 both say
every C1 lag is non-negative **by construction**. **689 are negative (2.74% of C1)**, identical
counts from both instances: **459 bind on the S1-completion term** — `max()` can legitimately select
it on a C1 show, so **the warrant only ever covered half the operator** — and **230 bind on the
finale**, of which 135 are the known one-day UTC skew and **95 are unexplained, out to −495 days**.
Dropping all 689 moves `W` 107.71 → 113.99, about 6 days, so **not load-bearing for the number.
The warrant is false either way.** README item 24, open.

## What the two curves say about the transfer assumption

| Percentile | C1 only (25,120) | All shows (128,099) |
| ---: | ---: | ---: |
| 50 | 1.73 | 0.72 |
| 85 | 45.98 | 10.60 |
| **90** | **107.71** | **37.70** |
| 95 | 322.61 | 184.39 |
| share negative | **2.74%** | **22.61%** |

**The same percentile differs by 70.0 days, a factor of 2.86.** That gap is the size of the transfer
assumption D14 accepted, and it is mechanical rather than behavioural: under finale anchoring anyone
watching a weekly season while it airs has a negative lag. **The negative mass tracks release
cadence, not viewer behaviour** — 2.74% on C1 against 21.6% (C4), 28.7% (C2) and 39.2% (C3). C0 is
empty and is reported at zero rather than omitted.

Two-thirds of C1 starters start within a week. **The window is 108 days long because of the last few
percent, not because of the typical viewer.**

## Process facts worth keeping

- **Both instances reproduced Step 5's waterfall and *asserted* on it before computing** —
  201,900 → 178,165 → 155,131 → 152,126 → 128,099, run aborts on any mismatch. Both also
  independently recomputed the D12 classifier: **1,138 shows, 0 disagreements** with the frame.
- **Zero API calls, both instances, both runs.**
- **Distinct output namespaces are now required** (README item 25). Run 1's instances got
  byte-identical prompts — correct — but **identical default output paths and collided**; one
  instance's script was overwritten mid-run, which is why an `-instance-a` suffix in run 1 does not
  match the agent that produced it. **The namespace is not part of the task description and
  separating it does not weaken the diff.** Applies to Steps 7, 8 and 9.
- **Instance A landed on 107, one of run 1's two values, and said in its own §2 that this is
  arithmetic and not confirmation.** Computing the same percentile of the same distribution twice
  necessarily agrees. **The informative thing is a divergence**, and the reader should look for it
  in the diff against `-b`, not in the match with run 1. See [[withdrawn-claims-register]].

## One conflict between approved documents, reported and unresolved

**4 pairs in the 128,099 have a first S2 record at or after `τ_pull`**, which Step 1 D11 says must
be discarded from every computation, while Step 5 built the sample without that filter. **Both
instances found them, both retained them, and both were right to** — the spec directs taking the
population from the Step 5 artifact. **None is in C1, so `W` is unaffected** (107.0 with and
without). But Step 8 classifies on the 201,900 under the frozen cutoff, so **Step 6 and Step 8 will
not share a row set.** README item 27, open.

Related: [[glossary-terms-and-thresholds]], [[gate-step5-contamination]],
[[open-items-and-contradictions]], [[withdrawn-claims-register]], [[decision-log-step18]].
