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

**Correction, 2026-08-11: an earlier version of this entry credited Engineering with a position
that was the Analytics Engineer's own, pre-registered before the run.** The distinction matters for
a log whose purpose is attributing judgment, so it is corrected in place rather than quietly.

**What the agent pre-registered** — `src/step3_user_discovery.py`, module docstring, written before
the run:

> "Which rule actually fired is reported. If it is (2) or (3) while the yield curve is still high,
> that is the finding: the follower graph does not saturate at this scale, so pool size is a budget
> choice rather than a discovery limit. **Saying that plainly is worth more than manufacturing a
> plateau.**"

That is a pre-registration of the exact outcome that occurred, including its interpretation. The
agent did not discover this after the fact and did not dress up a budget stop as convergence.

**Engineering's distinct contribution** was the second half: that a stopping rule known in advance
to be unlikely to fire should have been put to the Human Lead **before** the run, not left to be
found in the run record afterwards. That is the substance of why this entry exists.

## The gap this entry cannot fill: why 4,000

The docstring gives a rationale for *a few thousand*:

> "SUFFICIENCY. Stop at `TARGET_USABLE` confirmed-usable users. This is a real stopping argument and
> not a budget dodge: the study needs user-show pairs, each user contributes several, and Step 11
> splits by channel and Step 12 by segment. A few thousand users is ample for all of that, while
> every additional user costs Step 4 roughly `ceil(total_plays/250)` more calls."

**Nothing anywhere states why 4,000 rather than 3,000 or 6,000.** Searched across the code, both
plan blocks and the write-up. This is a negative claim and may have been missed, but as the record
stands the magnitude is unjustified while the *kind* of argument is sound.

## The alternative, and what it would have cost

**Run until the plateau rule fires.** On the evidence, that condition may never have arrived: the
frontier grew monotonically from 496 to **2,970** and was never exhausted in any of 36 rounds. The
crawl would have run to the `CALL_BUDGET = 6500` ceiling — roughly 1,200 further calls, which at 147
calls per round is **about 8 more rounds**. Eight rounds sits well inside the observed rebound period
(rounds 7–10 decayed, round 11 rebounded 4–6×), so on the observed dynamics the plateau still would
not have fired. The crawl would have stopped on budget rather than convergence, with the graph open.
**The task sheet's stopping condition was, on this graph, not reachable within budget.**

## What follows from it

**The pool is 4,088 usable users. It is not a saturated sample of the reachable graph.** Every
downstream share rests on that distinction, and it is stated at the head of
`artifacts/step3-user-discovery.md` for the same reason.

**Consequences, not decisions** — recorded so they are not mistaken for choices. Two different
kinds, and the stronger kind matters:

- **Structurally forced by constants already recorded.** The frontier's monotonic growth was
  *guaranteed*, not merely observed: each round removes 12 users from the frontier and can add up to
  `12 × 100 = 1,200`, so growth was certain unless dedup approached 100 percent. Likewise
  `expanded_total = 432` is exactly `12 × 36`, and "only 432 of 5,694 users expanded" and "depth 3
  never reached" are the same fact restated. **None of these is evidence about the graph.** They are
  arithmetic on `EXPAND_USERS_PER_ROUND` and `NEIGHBOURS_PER_USER` ([0006](0006-step3-crawl-constants.md)).
- **Properties of the world.** Channel B's exhaustion and Channel A's hub-luck variance are genuine
  findings about the data, not positions anyone took.

## For the Human Lead

Ratify, or direct otherwise. The live question is not whether to re-run — it is **what the study
claims**. A claim about 4,088 sampled users is supported. A claim about the reachable Trakt
population is not, and the frontier is still open with budget remaining if that is the intent.
See `artifacts/step3-user-discovery.md` §9 position 3.
