# Decision 0006 — Six crawl constants set inside a Chained step

| | |
| :--- | :--- |
| **Decision** | Six constants fixing the shape of the Step 3 crawl, set at design time and unchanged through the run. |
| **Taken by** | Analytics Engineer, inside a Chained step |
| **Authority** | **Not a Human Lead decision.** Unlike [0005](0005-step3-stopping-rule.md), **none of these departs from `task-sheet.md`** — the task sheet is silent on all six. Recorded because they bound the pool, not because they conflict. |
| **Pre-registered** | **Yes.** Rationale is in the module docstring of `src/step3_user_discovery.py`, written before the run. Quoted below rather than reconstructed. |
| **Where they live** | `src/step3_user_discovery.py`, one block; mirrored into `logs/step3_run.json` → `plan` and `artifacts/step3-yield-curve.json` → `plan` |
| **Date taken / recorded** | Taken 2026-08-11 before the run; recorded 2026-08-11 after it, on Human Lead instruction |
| **Status** | **Open — for ratification or dismissal at the Step 3 checkpoint** |

The task sheet specifies Step 3's *method* — two channels, tagged, no harvesting from comments on
measured shows — but no numbers. These are the numbers, recorded because a constant that shapes the
population is a decision whether or not anyone treated it as one.

---

## The constants, verbatim

```
N_SEEDS                = 300
MAX_DEPTH              = 3
NEIGHBOURS_PER_USER    = 100          # page 1 at limit=100; hub contribution capped
SCREEN_CALLS_PER_ROUND = 120
MIN_EPISODES_USABLE    = 10
CALL_BUDGET            = 6500
```

## Deliberately not in this entry

Recorded elsewhere, and listed here so nothing is counted twice:

| Constant | Where |
| :--- | :--- |
| `TARGET_USABLE = 4000` | [0005](0005-step3-stopping-rule.md) |
| `MIN_ROUNDS_BEFORE_PLATEAU = 10`, `PLATEAU_FRACTION_OF_PEAK = 0.20`, `PLATEAU_CONSECUTIVE_ROUNDS = 2` | [0005](0005-step3-stopping-rule.md), which carries the round-9 counterfactual that is their cost |
| `EXPAND_USERS_PER_ROUND = 12`, `LIST_PAGES_PER_ROUND = 3` | [0007](0007-step3-channel-cost-trade.md) — these **are** the channel allocation |
| `STEP4_PAGE_LIMIT = 250` | **Not agent-set.** Inherited from [0002](0002-step4-history-endpoint.md) / D15, which fixed `limit=250` |
| `STALL_UNACCOUNTED_SECONDS = 60.0` | Instrumentation, not policy. Flags a round whose wall clock exceeds what it can account for, so a suspended machine is not read as throttling. Changes nothing the run decides |
| `SEED_FEEDS` | **Nowhere yet.** A design choice rather than a constant, and the highest-consequence one in Step 3 — see the note at the end |

*(An earlier version of this entry listed twelve constants, folding the channel allocation and the
stopping parameters in here as well. That double-recorded them. Corrected 2026-08-11.)*

## Why each, in the agent's own pre-run words

Four of the six are framed as a single measure: *"Anti-clique measures, all chosen in advance because
a follower walk from a small seed set converges on one community if left alone."*

- **`N_SEEDS = 300`** — *"300 seeds, not a handful, spread over many different movies."* Operationalizes
  the task sheet's "seed a few hundred public profiles."
- **`NEIGHBOURS_PER_USER = 100`** — *"At most 100 neighbours taken per expanded user (page 1 at
  limit=100). A hub with 4,296 followers therefore contributes no more than 100."*
- **`MAX_DEPTH = 3`** — *"Depth capped at 3."*
- **`MIN_EPISODES_USABLE = 10`** — *"Defined operationally, because 'usable-user yield' needs it fixed
  in advance … The floor of 10 episodes is deliberately far below anything the study needs: a user
  with fewer than 10 episodes logged cannot have completed any season 1, so this pre-applies the
  frame rather than biasing it."* **That warrant is contested — see below.**
- **`CALL_BUDGET = 6500`** — *"BUDGET. A hard cap on Step 3 live calls."* No justification of 6,500
  specifically.
- **`SCREEN_CALLS_PER_ROUND = 120`** — **no stated rationale anywhere.**

## Seed feeds

Three were configured, at 4 pages each:

```
comments/recent/all/movies
comments/trending/all/movies
comments/updates/all/movies
```

**Only two produced seeds:** `recent` 218, `trending` 82, `updates` **0**. The 300 seeds spread
across 172 distinct films, with at most 24 seeds drawn from any one film.

## The alternative, and what each cost as set

No alternative was recorded for any of the six. Reconstructed, with the realized cost:

| Constant | Alternative | What it cost as set |
| :--- | :--- | :--- |
| `N_SEEDS = 300` | A smaller seed set | 10 seed calls. **Guarded a risk that did not materialise** — the walk barely branched, so the anti-clique machinery insured against the opposite of what happened |
| `NEIGHBOURS_PER_USER = 100` | Page hubs fully | **A real, directional cost — see below** |
| `MAX_DEPTH = 3` | Deeper | **Never bound.** Depth 3 never reached. Zero realized cost |
| `SCREEN_CALLS_PER_ROUND = 120` | More screening per round | **1,027 eligible users left unscreened**, skewed by FIFO order toward depth 2 |
| `MIN_EPISODES_USABLE = 10` | A higher floor, or none | Removed **232 accounts**, 5.4% of screened. Warrant contested — below |
| `CALL_BUDGET = 6500` | Higher | **Never bound.** 5,300 spent. Zero realized cost, though [0005](0005-step3-stopping-rule.md) uses it to price its alternative |

## Where a reviewer disagreed: on these six, nobody did

Engineering returned HOLD on the crawl code, but the amendment header records its scope: *"The plan
above is unchanged. None of the stopping thresholds, the seeding strategy or the channel design is
touched here. What changed is what the run RECORDS and how it EXITS."* The HOLD produced six defect
fixes, the metric backfill and the edge-list rebuild. **It did not challenge any constant in this
entry**, and recording it here as disagreement would borrow [0005](0005-step3-stopping-rule.md)'s
reviewer.

One objection was raised after the run, by the Second Brain, and it is unresolved.

## Four that carry known consequences

### `MIN_EPISODES_USABLE = 10` — the stated warrant rests on a premise Step 1 does not grant

It rejected **232 of 4,320 screened accounts (5.4 percent)**, so the floor does real work.

**But its justification is stated as a certainty and is not one.** The docstring claims *"a user with
fewer than 10 episodes logged cannot have completed any season 1, so this pre-applies the frame
rather than biasing it."* That requires every S1 in the Step 2 frame to be at least 10 episodes.
`artifacts/step1-outcome-definition.md` §7 **excludes `L2 = 1` but retains `L1 = 1`**, and neither
Step 1 nor `task-sheet.md` Step 2 sets a minimum S1 length. Under `|D1| ≥ ceil(0.90 × L1)`, a show
with `L1 = 6` is completed at six distinct episodes.

**Checkable the moment Step 2 exists: `min(L1)` over the frame, ≥ 10 or not.** Until then the warrant
is *unverified*, not wrong. If it fails, the excluded users are light trackers — **downward on the
never-started share**, compounding with the seeding bias rather than cancelling it.

**This is the strongest ratification candidate after [0005](0005-step3-stopping-rule.md)**, for a
reason beyond its warrant: `MIN_EPISODES_USABLE` has no task-sheet anchor, yet it *defines a word the
task sheet's own stopping rule depends on*. "Run until usable-user yield plateaus" was not evaluable
until the agent supplied a meaning for "usable."

Separately, a 10-episode bar is a long way from "will contribute an analysis row," which needs S1
completion on a show inside the frame. **"4,088 usable users" is a weak sufficiency claim** —
`artifacts/step3-user-discovery.md` §9 position 4.

### `NEIGHBOURS_PER_USER = 100` — biases the graph statistic in a known direction

Truncating every account at page 1 systematically under-represents hub connectivity, so **any
clustering or clique statistic Step 11 computes will read less connected than reality.** That is the
same statistic the edge-list rebuild existed to make answerable, so the bias should be stated
alongside it rather than discovered later.

### `SCREEN_CALLS_PER_ROUND = 120`, FIFO — creates a depth artifact

Screening ran first-in-first-out at 120 per round and did not keep pace with discovery. **1,027
eligible users were discovered and never screened.** Because the queue is FIFO, the unscreened skew
to depth 2: depth 1 was screened at roughly 80 percent of its cohort, depth 2 at roughly 36 percent.

**Any depth-stratified diagnostic must condition on *screened*, not on *eligible*,** or it will
report a screening-order effect as a depth effect. This matters for Step 11.

### `MAX_DEPTH = 3` — never bound

Depth 3 was never reached; the frontier ended holding depth 1 and depth 2 only. Chosen as an
anti-clique measure against a walk converging on one tight community. **That risk did not
materialise** — the observed failure is the opposite, a walk that barely branched.

**A caution on reading this as evidence.** "Only 432 of 5,694 users expanded" and "depth 3 never
reached" are not findings about the graph. They are arithmetic:
`expanded_total = 432 = EXPAND_USERS_PER_ROUND × rounds = 12 × 36`. See
[0005](0005-step3-stopping-rule.md) on consequences that are structurally forced rather than
observed.

## Where these constants sit against the task sheet

A three-way split, offered as a criterion rather than an answer:

- **Operationalizes an instruction the task sheet gives but underspecifies:** `N_SEEDS = 300` for
  "a few hundred"; the three plateau parameters in [0005](0005-step3-stopping-rule.md) for "until
  yield plateaus."
- **Replaces an instruction the task sheet states:** `TARGET_USABLE` only — that is
  [0005](0005-step3-stopping-rule.md), the sole member of this class.
- **No task-sheet anchor at all:** `MAX_DEPTH`, `NEIGHBOURS_PER_USER`, `SCREEN_CALLS_PER_ROUND`,
  `MIN_EPISODES_USABLE`, `CALL_BUDGET`, and the two in [0007](0007-step3-channel-cost-trade.md).

`MIN_EPISODES_USABLE` sits awkwardly across the split, for the reason given above.

## Not recorded anywhere yet, and it should be: the seed source

**`SEED_FEEDS` — movie-comment authors — is the highest-consequence agent choice in Step 3**, and it
appears in none of these three entries. It drives the whole of `artifacts/step3-user-discovery.md`
§4: the tracking-intensity bias, its downward direction on the headline, and the TV Time
migration-cohort timing that collides with Step 5.

It is deliberately not folded in here, because it is a design choice rather than a constant and
folding it in would bury it. It is pre-registered and defended in the docstring, which also
pre-builds a remedy: *"`seed_source` and `depth` are recorded per user and depth-0 users can be
excluded wholesale at Step 11 if the Human Lead wants that."* **Recommend it gets its own entry.**

## For the Human Lead

No action is required for the pool as it stands. Three are worth a view before Step 4:
`MIN_EPISODES_USABLE` (its warrant is unverified and checkable against Step 2's `min(L1)`),
`NEIGHBOURS_PER_USER` (it biases Step 11's connectivity statistic downward), and the
screening-order artifact (it constrains how any depth-stratified diagnostic must be computed).
