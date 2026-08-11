# Decision 0011 — `pull_date = 2026-08-11`

| | |
| :--- | :--- |
| **Decision** | The global frozen cutoff `pull_date` is **2026-08-11**. `τ_pull := 2026-08-11T00:00:00Z`. Every record with `watched_at ≥ τ_pull` is discarded. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Closes** | The one item [0001](0001-step1-outcome-definition-gate.md) left outstanding: D11 was adopted in **form** only, with its **value** deliberately deferred until Step 4's schedule was known. |
| **Status** | Closed |

---

## Why it could not be set earlier

D11 fixes `pull_date` as a single global constant rather than a per-user fetch date, because per-user
fetch dates make right-censoring user-dependent and the D3/D8/D9 diagnostics non-comparable. It
carries one constraint:

> **`pull_date` must be no later than the earliest per-user fetch date.**

That constraint cannot be honoured by a value chosen before the pull is scheduled, which is why the
deferral was recorded as a decision rather than an omission. **Step 4 beginning is what unblocked
it.**

## The constraint is satisfied

The earliest per-user fetch instant recorded in the Step 4 pilot ledger is
**2026-08-11T05:01:26Z**.

`τ_pull = 2026-08-11T00:00:00Z ≤ 2026-08-11T05:01:26Z` ✓

Every user is therefore observed at or after the cutoff, so every retained history is complete
through `τ_pull`. Users fetched later in the run — the full sweep is projected at ~22 hours and will
extend into 2026-08-12 — only strengthen this: a later fetch observes strictly more, and the cutoff
discards the excess.

## What now depends on it

Unblocked by this value: right-censoring (Section 6 of the outcome definition), and the **D3**,
**D8** and **D9** diagnostics, all of which reference the pull date.

**Required in the Step 8 waterfall**, per D11: the value of `pull_date`, the earliest and latest
per-user fetch dates, and the count of records discarded for `watched_at ≥ τ_pull`.

## One thing to watch when the count is reported

`τ_pull` floors to UTC midnight on the first day of the pull, so the discarded tail is roughly
**one day of watch activity for early-fetched users and roughly two for late-fetched ones**. That is
by design — a single global cutoff is what makes users comparable, and the alternative was rejected
in D11. But the discarded-record count is not evenly distributed across the pool, and it should not
be read as one.
