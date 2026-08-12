# Decision 0025 — The lag is a continuous instant difference and `W` is the ceiling of the percentile

| | |
| :--- | :--- |
| **Decision** | The lag is measured as a **continuous instant difference**, not floored to whole days, and **`W` is the CEILING** of the resulting percentile. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 6 |
| **Occasioned by** | Step 6 run 2, in which two isolated instances differed by exactly one day and neither was wrong |
| **Status** | Closed |

---

## What run 2 found

The re-run against the fixed 90th-percentile rule ([0024](0024-w-is-the-90th-percentile.md)) produced
**identical computations and one divergent convention.**

| | Instance A | Instance B |
| :--- | ---: | ---: |
| C1 pairs | 25,120 | 25,120 |
| C1 negative lags | 689 | 689 |
| — share of C1 | 0.027428343949044587 | 0.027428343949044587 |
| — s1-term / finale-term | 459 / 230 | 459 / 230 |
| Most negative lag | −3,248 | −3,247.4382 |
| `W` if negatives dropped | 113 | 113.9854 |
| All-shows p90 | 37 | 37.6967 |
| **`W`** | **107** | **107.7135** |

**Every figure matches to fifteen significant digits.** The apparent disagreements are the same
numbers under two units: −3,248 is `floor(−3247.4382)`, 113 is `floor(113.9854)`, 37 is
`floor(37.6967)`.

Instance A measured the lag in **whole days** — and verified that calendar-date difference equals
`floor(instant difference)` on every row — so its percentile was exactly 107.0 under all eight
standard conventions, with no rounding step to disclose. Instance B measured the **instant
difference**, got 107.7135, and flagged the integer rendering as a spec gap it declined to resolve,
predicting the outcome exactly: *"if the two instances differ by exactly one day, that is the spec
gap and not a derivation divergence."*

Both readings were faithful. The spec said "the observed lag distribution" and never said in what
unit it is observed.

## The ruling, and why it is not a tie-break

> `W = 108`. Take the ceiling of the fractional percentile, not the floor.
>
> The true p90 is 107.7135. Under the approved half-open test a pair is inside the window only if its
> fractional lag is less than `W`, so `W = 107` covers 89.976 percent and `W = 108` covers 90.020
> percent. The rule says 90th percentile, and only 108 delivers it. Floor introduces a systematic
> off-by-one against the test the window is evaluated by.

The argument is about **coherence with the operator**, not about rounding taste. Step 1 §2.4 and D13
fix the window as `τ1 = ⟦T0⟧ + W × 24h` with membership `watched_at < τ1`. A pair is therefore
covered **iff its fractional lag is strictly less than `W`**. Flooring the lag records a pair whose
true lag is in `[107, 108)` as "107" while the test excludes it from a `W = 107` window. The
estimator and the operator disagree, and the disagreement is one-directional.

Measured on the C1 sample:

| `W` | C1 started pairs inside the window |
| ---: | ---: |
| 107 | **89.976%** |
| **108** | **90.020%** |

**The floor misses the percentile the rule asks for. The ceiling delivers it.**

## Scope

- **The signed, untruncated rule is unchanged.** The percentile is still taken on the distribution as
  it stands — no truncation, no clipping, no absolute values, no dropped rows. This entry fixes the
  *unit* and the *rendering*, not the population.
- **It applies wherever the same shape recurs.** Any later step reading a percentile off a lag or
  duration and feeding it into a half-open instant test inherits the same off-by-one. Step 7's
  liveness threshold is the immediate candidate.
- **`W` itself is approved separately**, as [0026](0026-step6-window-w-gate.md). This entry is the
  rule; that entry is the number.

## The pattern this is the third instance of

Three consecutive Step 6 findings have the same shape: **a convention doing work the data does not
do, left unstated in the spec.**

1. "The percentile where the curve flattens" — undefined, and the C1 density is close to scale-free
   past day 7, so there was no feature to read. Two instances, 61 days apart.
   ([0024](0024-w-is-the-90th-percentile.md))
2. The 90th percentile itself — imported from attribution-window practice, not selected by the data,
   and labelled as such. ([0024](0024-w-is-the-90th-percentile.md))
3. The unit of the lag and the rounding of the percentile — this entry. One day.

Each was caught because two isolated instances ran the same words and produced different numbers.
**None would have been visible in a single run**, and the first two were not visible in the spec
either. Carried as item 26 in `decisions/README.md`.
