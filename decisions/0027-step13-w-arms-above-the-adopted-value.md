# Decision 0027 — Step 13's `W` arms extend above the adopted value, at 150 and 213 days

| | |
| :--- | :--- |
| **Decision** | Step 13's `W` arms must extend **above** the adopted `W = 108`, with arms at **150** and **213** days. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 13 |
| **Closes** | `decisions/README.md` **item 28** |
| **Status** | Closed |

---

## The gap

Before this entry every mandated `W` arm topped out at or below the adopted value:

| Source | Range |
| :--- | :--- |
| The two-curve range Step 6 reports | [38, 108] |
| [0024](0024-w-is-the-90th-percentile.md), the two run-1 readings | [46, 107] |
| **Union** | **[38, 108]** |

`W = 108` sat at the **ceiling** of the span. The sensitivity would have tested `W` downward across a
factor of nearly three and upward not at all.

## Why that is the wrong shape for this particular bias

The ruling, as given:

> Extend Step 13's `W` arms above 108. Add arms at 150 and 213. **213 is the p90 among shows with 8
> or more years of exposure, which is the direction the censoring diagnostic runs. A sensitivity
> range that stops at the adopted value does not test the direction the bias points.**

Both Step 6 instances found the same thing independently: **the 90th percentile rises monotonically
with exposure.**

| Minimum exposure | C1 p90 (days) |
| :--- | ---: |
| none | **107.7** |
| ≥ 1 year | 119 |
| ≥ 2 years | 128 |
| ≥ 4 years | 146 |
| **≥ 8 years** (n = 4,141) | **213** |

`W` was derived on a population containing pairs whose exposure is shorter than `W` itself — 530 C1
pairs, 2.11%, have less. Those pairs cannot contribute a long lag because there has not been time for
one, so they **pull the percentile down**. The uncensored value is somewhere above 107.7, and 213 is
the furthest the data can put it.

**213 is an upper bound, not a rival estimate.** Exposure and cohort are not separable here: the
long-exposure subset is also an older-show, older-viewer subset, and neither instance proposed an
adjustment. That is exactly why it belongs in a sensitivity arm rather than in the derivation — an
arm asks *what if*, which is the honest form for a quantity that cannot be estimated.

**150 is included so the response is not read off two endpoints alone.** With arms at 38, 46, 108,
150 and 213 the relationship between `W` and the headline is traced rather than bracketed, and a
non-linear response — which a heavy-tailed lag distribution makes likely — becomes visible instead of
being interpolated away.

## Direction, stated so the arms are interpretable

**A larger `W` admits later starters and moves the never-started share down.** So the arms above 108
test the direction in which the reported share is most likely to be **overstated**. That matters for
Step 14, which already carries the never-started share as a floor with respect to contamination
retention ([0021](0021-step5-contamination-gate.md)) — this is a second, independent reason the same
number may be too high, and the two do not offset because they arise from different mechanisms.

## Scope

- **`W = 108` is unchanged.** [0026](0026-step6-window-w-gate.md) stands. This entry adds sensitivity
  arms; it does not re-open the gate or alter the adopted value.
- **The arms compose.** Step 13 must cover the union of the two-curve range, the [46, 107] span, and
  the new arms — effectively **38 to 213 days**, with 108 the adopted point inside it.
- **`H` stays constant across every arm**, per the existing Step 13 rule. Otherwise D3 and D8 are not
  comparable between arms.
- **Each arm re-censors the population**, per the existing Step 13 rule, so the arms do **not** share
  a denominator and the retained-row count must be reported for every one of them. This bites harder
  at the top of the range: right-censoring retains a pair only if `⟦T0⟧ + (max(W, 91) + H) × 24h ≤
  τ_pull`, so **an arm at 213 discards materially more pairs than an arm at 108**, and the headline
  moves for two reasons at once. Reporting the count per arm is what keeps those separable.
