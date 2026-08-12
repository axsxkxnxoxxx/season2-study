# Decision 0022 — The two Step 5 standing rulings are written into `task-sheet.md`, before Steps 6 or 7 launch

| | |
| :--- | :--- |
| **Decision** | The two standing rulings recorded at the Step 5 gate are **written into the task sheet's Step 6 and Step 7 specs**. They were previously recorded only in `decisions/0021` and in the Step 5 artifact, and the specs the two isolated instances actually read said nothing about them. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 6 and Step 7 |
| **Source of the rulings** | [0021](0021-step5-contamination-gate.md), the Step 5 gate approval |
| **Found by** | `second-brain`, on its first consistency pass since the Step 1 gate |
| **Status** | Closed |

---

## Why this could not wait for the steps to launch

Steps 6 and 7 are **dual implementation**. Two isolated instances receive the same written spec, and
the Human Lead diffs their numbers. `CLAUDE.md` states the reason: *"Both instances receive the same
written spec from a file. Never describe the task twice in your own words: a difference in output
would then prove nothing."*

That control catches a difference between the instances. **It cannot catch anything the spec omits**,
because both instances read the same silence and both fill it the same way.

> **Two instances reading the same silent spec will agree on the wrong clock, and the diff will
> report agreement.**

Step 7's spec said only *"plot the distribution of gaps between consecutive logged events per
user."* On claimed `watched_at` that reads a 2026 import of a 2015 season as a 2015 event and scores
a live account dead. Both instances would have done it identically, and the diff would have been
clean.

The precedent was already set twice in this study, both times for the same reason: **D14 is written
into Step 6 by bucket name** rather than as "binge shows", and the **pair-level scope of the liveness
test** is written into Step 7 in full. A ruling that changes what two isolated instances compute
belongs in the file they read.

## What was added

### Step 6 — the estimation sample

> **Derive W on the Step 5 clean-record estimation sample: 128,099 pairs.** The population that can
> answer the timing question sets the rule, and the resulting W applies to **all** pairs, including
> those the sample excludes.

Three things are stated with it, because each is a way the number could go wrong silently:

- **It composes with D14 rather than replacing it.** The C1 restriction applies *on top of* the
  128,099, not instead of it.
- **The waterfall is published** — 201,900 → 178,165 → 155,131 → 152,126 → 128,099 — and both
  instances take the population from `artifacts/step5-contamination-diagnostics.md` rather than
  re-deriving it. A re-derived population would make the diff report a population difference as an
  implementation difference.
- **201,900 and 128,099 are different numbers.** The analysis population is not the estimation
  sample, and Step 5 kept them visibly distinct for exactly this reason.

### Step 7 — the clock, and the calibration

> **Liveness runs on record INSERTION time, not on the claimed `watched_at`.** Any record inserted
> after the window closed proves the account was alive, whatever date it claims — backfilling an old
> show is still activity.

> **The play-`id` insert-time calibration is a required input, and neither instance refits it.**

The second sentence is the operative one for the dual run. The calibration is an isotonic id →
wall-clock curve fitted on `checkin` and `scrobble` records only, held out on disjoint accounts at a
median error of four minutes, stored at `processed/step5/calibration.npz` and produced by
`src/step5_calibrate.py`. **Two independently refitted curves would differ**, and the diff would then
confound a calibration difference with an implementation difference — the one thing the dual run
exists to rule out. Both instances read the stored curve.

The Step 7 gap-distribution item is also amended to say **insertion** instants rather than "logged
events", so the plotted object matches the rule.

## What this does not change

- **No threshold is set.** `W` and the liveness threshold remain unset, and Steps 6 and 7 remain
  unapproved gates. This entry fixes *what the instances compute on*, not *what they conclude*.
- **No Step 5 number moves.** 201,900 retained, 128,099 estimation sample, both as approved in
  [0021](0021-step5-contamination-gate.md).
- **Step 1 is untouched.** These are Step 5 rulings being propagated into the task sheet, not
  amendments to the approved outcome definition.

## The general lesson, recorded because it will recur

A ruling made at one gate that changes what a **later** step computes has three places it can live:
the decision log, the deliverable of the gate that made it, and **the spec the later step actually
reads**. The first two were done at Step 5 and were not enough. Three gates remain — Steps 6, 7 and
8 — and each will produce rulings with downstream reach.

**Standing check: when a gate ruling changes what a downstream step computes, propagate it to
`task-sheet.md` at the time of the ruling, not at the time the step launches.** Carried as item 23 in
`decisions/README.md`.
