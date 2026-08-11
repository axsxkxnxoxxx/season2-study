# Decision 0006 — The twelve Step 3 crawl constants

| | |
| :--- | :--- |
| **Decision** | Twelve numeric constants that determine the shape, size and cost of the user pool were fixed at crawl-design time and are recorded here. |
| **Taken by** | Analytics Engineer, inside a Chained step |
| **Authority** | **Not a Human Lead decision.** None appears in `task-sheet.md`. |
| **Date taken** | 2026-08-11, before the run |
| **Date recorded** | 2026-08-11, after the run, on Human Lead instruction |
| **Status** | **Open — recorded for visibility and ratification.** Two of the twelve carry known consequences (below). |

The task sheet specifies Step 3's *method* — two channels, tagged, no harvesting from comments on
measured shows — but no numbers. These twelve are the numbers. They are recorded because a
constant that shapes the population is a decision whether or not anyone treated it as one.

---

## The constants, as they appear in `src/step3_user_discovery.py`

```
N_SEEDS                     = 300
MAX_DEPTH                   = 3
NEIGHBOURS_PER_USER         = 100     # page 1 at limit=100; caps a hub's contribution
EXPAND_USERS_PER_ROUND      = 12      # 2 calls each -> 24 discovery calls
LIST_PAGES_PER_ROUND        = 3       # 3 discovery calls
SCREEN_CALLS_PER_ROUND      = 120
MIN_EPISODES_USABLE         = 10
MIN_ROUNDS_BEFORE_PLATEAU   = 10
PLATEAU_FRACTION_OF_PEAK    = 0.20
PLATEAU_CONSECUTIVE_ROUNDS  = 2
TARGET_USABLE               = 4000
CALL_BUDGET                 = 6500
```

Two further constants are instrumentation rather than policy and change nothing the run decides:
`STEP4_PAGE_LIMIT = 250` (the Step 4 page forecast divisor) and `STALL_UNACCOUNTED_SECONDS = 60.0`
(flags a round whose wall clock exceeds what it can account for, so a suspended machine is not read
as throttling).

`TARGET_USABLE`, `MIN_ROUNDS_BEFORE_PLATEAU`, `PLATEAU_FRACTION_OF_PEAK` and
`PLATEAU_CONSECUTIVE_ROUNDS` are also the subject of decision [0005](0005-step3-stopping-rule.md),
which is the one that departs from the task sheet.

## Seed feeds

Three were configured, at 4 pages each:

```
comments/recent/all/movies
comments/trending/all/movies
comments/updates/all/movies
```

**Only two produced seeds:** `recent` 218, `trending` 82, `updates` **0**. The 300 seeds spread
across 172 distinct films, with at most 24 seeds drawn from any one film.

## Three that carry known consequences

### `MIN_EPISODES_USABLE = 10` — not inert, but a low bar

It rejected **232 of 4,320 screened accounts (5.4 percent)**. So the floor does real work. But a
10-episode bar is a long way from "will contribute an analysis row," which requires completing some
show's S1 inside the Step 2 frame. **"4,088 usable users" is therefore a weak sufficiency claim**,
and whether the target should be expressed in analysis rows rather than usable accounts is open —
`artifacts/step3-user-discovery.md` §9 position 4.

### `SCREEN_CALLS_PER_ROUND = 120`, FIFO — creates a depth artifact

Screening ran first-in-first-out at 120 per round and did not keep pace with discovery. **1,027
eligible users were discovered and never screened.** Because the queue is FIFO, the unscreened skew
to depth 2: depth 1 was screened at roughly 80 percent of its cohort, depth 2 at roughly 36 percent.

**Any depth-stratified diagnostic must condition on *screened*, not on *eligible*,** or it will
report a screening-order effect as a depth effect. This matters for Step 11.

### `MAX_DEPTH = 3` and `NEIGHBOURS_PER_USER = 100` — never bound

Depth 3 was never reached; the frontier ended holding depth 1 and depth 2 only. Only **432 of 5,694**
discovered users were ever expanded. Both constants were chosen as anti-clique measures against a
walk converging on one tight community. **That risk did not materialise** — the observed failure is
the opposite, a walk that barely branched. Neither constant was the binding limit on anything.

## The alternative that was not taken

None of these was compared against a stated alternative at design time; they were set as "the plan's
numbers, in one place." That is the honest description, and it is why this is recorded as a decision
needing visibility rather than as a reasoned trade-off with a rejected option.

## For the Human Lead

No action is required for the pool as it stands. Two are worth a view before Step 4:
`MIN_EPISODES_USABLE` (does "usable" mean what the target assumed) and the screening-order artifact
(which constrains how Step 11's diagnostic must be computed).
