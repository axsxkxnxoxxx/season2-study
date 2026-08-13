# Decision 0036 — Step 7's liveness threshold is the 99th percentile, and the test applies to the gap bracketing `τ1`

| | |
| :--- | :--- |
| **Decision** | **Threshold: the 99th percentile** of the observed gap distribution, on continuous insertion instants, rounded **up**. **Shape: the test applies to the single gap bracketing the pair's `τ1`**, not to every gap in the account's sweep. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Closes** | The unruled threshold percentile (README item 30) and the unsettled rule shape (item 31) — the two things blocking Step 7 |
| **Amends** | `task-sheet.md` Step 7; `.claude/agents/data-scientist.md` and `data-scientist-b.md`, identically |
| **Status** | Closed. **Step 7 is unblocked and launches as a dual pair.** |

---

## 1. Threshold — the 99th percentile

**At the 95th, one ordinary gap in twenty trips the threshold. At the 99th it is one in a hundred.**

**A false-dead removes a pair**, and the liveness exclusion **already biases the never-started share
down** — it is bias 2 in the Step 14 ledger, because the accounts that stop logging are
disproportionately the ones that would have scored never-started. **So the conservative direction is
the higher percentile**, and it agrees with the direction `0025` already required of the rounding for
the same reason.

Measured on **continuous instant differences** and rounded **up**, per `0025`. Both were already
settled; this ruling fixes only the percentile.

**The withdrawn wording, recorded because it nearly shipped.** "Set the threshold well beyond the
normal gap" named no feature and no number. It is the same defect as Step 6's "the percentile where
the curve flattens", which cost a full dual run and produced **two honest answers 61 days apart**
(`0024`). A named percentile is reproducible across two isolated instances; a description of a curve's
shape is not.

## 2. Shape — the gap bracketing `τ1`, not the whole sweep

**The test.** For each pair, take that pair's own `τ1 = ⟦T0⟧ + W × 24h`, find the **last insertion
instant at or before `τ1`** and the **first insertion instant after `τ1`** on that account, and test
**that one gap** against the threshold.

### 2.1 Why not the whole sweep

**A whole-sweep test compounds the false-dead rate with the number of gaps.** At the 99th percentile,
each gap independently trips with probability 0.01, so an account with `n` logged gaps trips at least
once with probability `1 − 0.99ⁿ`:

| Logged gaps | Trips by chance |
| ---: | ---: |
| 10 | 9.6% |
| 50 | **39.5%** |
| 100 | 63.4% |

**This is a property of the rule's shape and no percentile fixes it.** Raising the percentile only
moves the account count at which the compounding bites — at the 99.9th, 500 gaps still trips 39% of
the time. And the failure is **selective**, not merely noisy: heavier accounts have more gaps, so a
whole-sweep test declares dead precisely the users who log the most. **That is the opposite of what
the test is for.**

### 2.2 Why this gap

**Liveness licenses trusting a null, and the null is `|A| = 0` tested at `τ1`.** The question the
filter exists to answer is whether an absence of S2 records is evidence of a decision or evidence of
an absent user. **What must be established is that the account was alive at that moment** — not that
it never went quiet across its whole history.

An account that vanished for two years in 2019 and was logging normally around `τ1` **is evidence for
the null**, not against it. A whole-sweep test throws that pair away.

This also keeps the filter aligned with what `0034` fixed: **liveness stays anchored at `τ1`**, and
`τ2` plays no part in it. The bracketing gap is `τ1`'s own neighbourhood, so the rule and its anchor
now name the same instant.

### 2.3 Edge cases, stated so two isolated instances resolve them alike

- **No insertion instant after `τ1`** — the gap is open-ended. **Not live.**
- **No insertion instant at or before `τ1`** — no pre-`τ1` evidence. **Not live.**

**Both are counted and reported separately from pairs failing on a measured gap**, because they are a
different kind of failure: one is an observed long silence, the other is an absence of evidence. A
diff that merged them would hide which one an instance had hit.

## 3. What this does not change

- **Insertion time, not claimed `watched_at`** (`0021`) — unchanged.
- **The play-`id` isotonic calibration is a required input and neither instance refits it**
  (`0029`) — unchanged, and load-bearing: two independently fitted curves would differ and the diff
  would confound a calibration difference with an implementation difference.
- **Liveness is a pair-level filter.** Evidence is account-wide — the whole sweep, other shows and
  movies included — but the test is clock-start-relative and clock start is pair-specific, so one
  account can be live for one show and dead for another. **Never drop a user wholesale.**
- ~~**The threshold is derived independently of `W`**, though the test instant is a function of it.~~
  **AMENDED 2026-08-13 (`decisions/0038`): this is withdrawn and was unsatisfiable after `0037`.** Any
  bracketing-gap reference distribution is **selected by `τ1`, which contains `W`**, so the threshold
  is a **function of `W`** and cannot be derived independently of it. Measured across the Step 13 arms:
  408 → 576 days on the clean sample, 885 → 973 on the full population. **Step 13 must refit the
  threshold per arm** and report both the threshold and the realised rate for each.

## 4. Scope

- **Step 7 launches as a dual pair** with distinct output namespaces, both instances reading this spec
  from `task-sheet.md` rather than a description of it.
- **This is a gate.** Both instances produce and stop. Neither adopts its own proposal, and the Human
  Lead diffs the numbers.
- **Zero API calls.** Step 7 runs on cached data and the stored calibration curve.
