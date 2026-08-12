# Decision 0028 — Step 14 carries every limitation routed to it, with a seven-statement bias ledger

| | |
| :--- | :--- |
| **Decision** | `task-sheet.md` **Step 14 is amended** to carry every limitation now routing to it: a **seven-statement bias ledger**, each with its mechanism, direction and source, and **eight non-bias limitations**. The ledger statements **must not be netted**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 14 |
| **Found by** | `second-brain`, on the consistency pass following the Step 5 gate |
| **Status** | Closed |

---

## The gap

Step 14's checklist was five lines and carried **one** bias mechanism:

> State that excluding inactive users biases the never-started share downward

By the time Step 6 was approved, **seven** directional biases were known and roughly eleven distinct
limitations had been routed to Step 14 by `0008`, `0010`, `0015`, `0016`, `0017`, `0020`, `0021`,
`0023`, `0026` and `0027` — scattered across ten decision entries and four artifacts.

## Why it was amended now rather than at Step 14

This is [item 23](README.md)'s rule applied to a step where the failure mode is different, and the
difference is worth stating because it changes what the fix is for.

At Steps 6 and 7 the risk is **silent divergence**: two isolated instances read the same gap in the
spec and fill it the same way, so the dual-implementation diff reports agreement and the control
fails without a signal. That is why `0022` propagated the Step 5 rulings into the files those
instances read.

**Step 14 is Human Lead-owned and single-implementation, so there is no divergence risk at all.** The
risk is **plain omission** — a limitation decided in August, recorded in an entry nobody re-reads,
and simply not written down when the limits section is drafted months of decisions later. A
five-line checklist gives the drafter no way to know that six of the seven bias directions exist.

The propagation rule is the same either way: **write the ruling into the spec at the time of the
ruling, not at the time the step launches.**

## The bias ledger

Seven statements, each carrying mechanism, direction and source. Full text is in the task sheet.

| # | Bias | Direction | Source |
| :-- | :--- | :--- | :--- |
| 1 | Step 3 seeding toward heavy, active trackers | **down** | `0008` |
| 2 | Liveness exclusion | **down** | Step 1 §7, Step 7 |
| 3 | Tail cap, 0.93% of the pool | **up** | `0010` |
| 4 | Sweep-completeness tolerance discard, +1.27 pts | **up** | `0023` |
| 5 | Step 5 population change, net −15,123 pairs | **up** | `0021` |
| 6 | Step 5 estimator bias on the retained population | **down** | `0021` |
| 7 | A larger `W` | **down** | `0026`, `0027` |

### Why "do not net them" is a substantive instruction, not a caution

**They are not all the same kind of quantity.** Statement 5 is a *population change* — it alters what
is being estimated, and it is exact. Statement 6 is an *estimator bias on a fixed population* — it
moves the estimate, and it is bounded rather than counted. Averaging those is a category error, not
a simplification. That distinction was itself a Red Team finding at the Step 5 gate, where an earlier
revision had netted them into a single direction and reached a conclusion the arithmetic did not
support.

**Same-direction pairs do not necessarily reinforce, and opposite-direction pairs do not necessarily
cancel.** Statements 6 and 7 both point down and **compound**, because a window-width choice and a
timestamp defect are independent mechanisms. Statement 3 points up against 1 and 2 pointing down, but
at 0.93% of the pool it does not meaningfully offset them. **Only the mechanism tells you which is
which, and a netted number destroys the mechanism.**

### Two qualifiers that do not travel without their statements

- **Statement 6 is guaranteed for 8,372 pairs and assumed for 42,019.** The floor is structural for
  air-date-stamped and corrupt records, where claimed ≤ true holds by construction. It is an
  **assumption** for backfilled records — 90.1% of the affected mass — because the tag means claimed
  ≪ *insert*, not claimed < *true*. **Stating the direction without the qualifier overstates what is
  known about nine tenths of it.**
- **Statement 7's non-offset.** Statements 6 and 7 both point down, and the natural reading is that
  the second confirms the first. It does not; they are independent and they compound.

## The non-bias limitations

Eight, each with its mechanism and source, in the task sheet: the **4,988 partly-air-date pairs** and
why a `W`-dependent fix was rejected; the **flip bound of 0 to 44,458** with no point estimate
available; the **completeness rule validating itself against itself** and the better instrument
declined on cost; the **frame's skew toward larger titles** via the ≥50-completer candidate rule and
its **66.5% pre-2020** composition; **`W`'s ±18-day show-clustered interval** and the 90th
percentile's status as imported convention; the **size cap being partly a cadence threshold**, 44 of
51 removed shows being C4; **platform fragmentation not being a variable in this study**; and the
study resting on a **stopped pull at 62.9%**.

## Scope

- **No result changes.** This is a documentation amendment. No threshold, population or number moves.
- **It is a floor, not a ceiling.** Steps 7, 8 and 9 through 13 will route more limitations here.
  **Each should be added at the time of its ruling**, per item 23, rather than accumulating for a
  future sweep.
- **The Consumer Insights review at Step 14 is unaffected**, and now has the full ledger to judge the
  population against rather than a five-line summary.
