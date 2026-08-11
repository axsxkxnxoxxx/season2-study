# Decision 0005 — Step 3 stopped on a usable-user target, not on the plateau rule the task sheet names

| | |
| :--- | :--- |
| **Decision** | Step 3 terminated on `TARGET_USABLE = 4000`. The plateau rule the task sheet specifies was implemented, ran for all 36 rounds, and never fired. |
| **Taken by** | Analytics Engineer, inside a Chained step, at crawl-design time |
| **Authority** | **Not a Human Lead decision.** Taken under the latitude a Chained step gives its owner. **Recorded here for ratification, because it departs from `task-sheet.md`.** |
| **Date taken** | 2026-08-11, before the run |
| **Date recorded** | 2026-08-11, after the run, on Human Lead instruction |
| **Status** | **Open — awaiting ratification at the Step 3 checkpoint** |

---

## What the task sheet says, verbatim

`task-sheet.md` Step 3:

> `- [ ] Run until usable-user yield plateaus`

That is the only stopping condition the task sheet gives. **`TARGET_USABLE` appears nowhere in it.**

## What was implemented

Both rules, with sufficiency reached first:

```
TARGET_USABLE               = 4000
CALL_BUDGET                 = 6500
MIN_ROUNDS_BEFORE_PLATEAU   = 10
PLATEAU_FRACTION_OF_PEAK    = 0.20
PLATEAU_CONSECUTIVE_ROUNDS  = 2
```

Plateau rule as coded: *3-round moving average of new eligible users per discovery call ≤ 20 percent
of its running peak, on 2 consecutive rounds, after at least 10 rounds.*

## What happened

`stop_reason: "sufficiency: reached the usable-user target"`, at 4,088 usable users, 5,300 calls,
36 rounds.

The plateau rule finished at **ratio_to_peak 0.314** against a 0.20 trigger, with
`consecutive_below: 0`. **It was never close at the end and it never fired.**

## The disagreement on the record

**Engineering review returned HOLD on the crawl code** before the run completed, and made two
findings that bear directly on this decision:

1. **It predicted this outcome.** Projecting from observed rates, Engineering concluded sufficiency
   would fire first at ~5,300 calls and the plateau rule would not fire at all. That is exactly what
   happened, to the call.
2. **The plateau rule cannot distinguish a plateau from a stall.** Rounds 7–10 decayed into a
   saturated pocket, bringing the 3-round average within 15 percent of the trigger; **round 11 then
   rebounded 4–6×**. Had `MIN_ROUNDS_BEFORE_PLATEAU` been 9 rather than 10, the run would have
   stopped at round 10 and reported a plateau that did not exist.

Engineering's position was that stating plainly that the plateau would not fire is better than
manufacturing one — and that this should have been put to the Human Lead **before** the run rather
than discovered in the run record afterwards. That is the substance of why this entry exists.

## The alternative, and what it would have cost

**Run until the plateau rule fires.** On the evidence, that condition may never have arrived: the
frontier grew monotonically from 496 to **2,970** and was never exhausted in any of 36 rounds. The
crawl would have run to the `CALL_BUDGET = 6500` ceiling — roughly 1,200 further calls — and stopped
on budget rather than on convergence, with the graph still open. The task sheet's stopping condition
was, on this graph, not reachable within budget.

## What follows from it

**The pool is 4,088 usable users. It is not a saturated sample of the reachable graph.** Every
downstream share rests on that distinction, and it is stated at the head of
`artifacts/step3-user-discovery.md` for the same reason.

**Consequences, not decisions** — recorded so they are not mistaken for choices: Channel B's
exhaustion, Channel A's hub-luck variance, and the monotonically growing frontier are all *results*
observed after the fact, not positions anyone took.

## For the Human Lead

Ratify, or direct otherwise. The live question is not whether to re-run — it is **what the study
claims**. A claim about 4,088 sampled users is supported. A claim about the reachable Trakt
population is not, and the frontier is still open with budget remaining if that is the intent.
See `artifacts/step3-user-discovery.md` §9 position 3.
