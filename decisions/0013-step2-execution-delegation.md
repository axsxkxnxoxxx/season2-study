# Decision 0013 — Step 2 execution is delegated to an agent; the selection rules stay with the Human Lead

| | |
| :--- | :--- |
| **Decision** | An agent may **execute** Step 2 — fetch seasons, apply the written rules, assemble the frame table — under selection rules the Human Lead writes. The rules themselves are never the agent's. Delegation is **for execution only**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Amends** | `CLAUDE.md`, **Human Lead** section: "When a step names the Human Lead as owner, no agent acts on it. Do not draft it, do not prepare it, do not offer a version of it." |
| **Scope** | **Step 2 only.** Steps 14, 15, 17 and 18 are untouched and remain fully Human Lead-owned. |
| **Status** | Closed |

---

## What the rule was for

The Human Lead owns Steps 2, 14, 15, 17 and 18. Step 2 is on that list because **the frame is where
show-selection judgment gets made**, and a study whose population was chosen by an agent cannot
later say the choice was the researcher's. The rule also protects against anchoring: once an agent
has produced a frame, the Human Lead's independent view of it is no longer independent.

That reasoning is not disputed here. What this decision does is locate the line more precisely than
"the step" does.

## Where the line falls

**Judgment** is deciding which shows belong in the study and on what criterion. **Execution** is
calling `/shows/:id/seasons` once per candidate and applying a rule someone else wrote.

The anchoring risk attaches to the first and not the second. An agent that fetches season data and
applies a stated threshold is not exercising discretion over the population — the population was
already determined by the rule, and the rule is the Human Lead's. Withholding the mechanical half
buys no protection and costs the run.

So: **the Human Lead sets every selection rule, in writing, before the agent runs.** The agent
fetches, applies, and reports.

## Three conditions on the delegation

1. **No live-call work starts while the Step 4 pull is in flight.** The pull throttles at 150
   GET/min against a 200/min application ceiling; a second live agent would put the study over it.
   Step 2's fetch waits for the pull to report done. This is a standing rule for the study, not a
   one-off for this run — **concurrent live-API agents are not run.**

2. **The candidate set is recomputed on the full pool.** The ≥50-completer candidate list and the
   quintile strata currently in `processed/` were computed on 2,134 users, **58 percent of the
   pool**, while the pull was still adding to it. Completer counts only rise, so shows now below 50
   will cross it and every quintile boundary will move. The partial diagnostic is not the frame's
   basis. The sequence is: **pull completes → completer diagnostic re-runs on the full pool → frame
   is built off stable counts.**

3. **An underspecified rule is reported, not resolved.** If the agent finds a selection rule that
   does not decide a case it meets, it stops and says so. It does not pick a reading. This is the
   same discipline the dual-implementation rule rests on: an ambiguity resolved silently by the
   executor is indistinguishable from a rule the Human Lead wrote.

## What this does not change

- **Step 2 remains a Human Lead-owned step.** The owner delegated execution; the ownership, and the
  accountability for which shows are in the study, did not move.
- **The frame is still reviewable as the Human Lead's work.** `reviewer-product` fires at Step 2 on
  whether the frame matches what a roadmap would need. That review is unaffected.
- **No other Human Lead step becomes delegable by precedent.** Steps 14, 15, 17 and 18 are
  interpretation and write-up, where the judgment/execution split this decision relies on does not
  cleanly exist.
