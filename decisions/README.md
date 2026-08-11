# Decision log

Tracked, public, aggregates and rationale only — no usernames, user IDs, or individual watch
histories. One file per decision, numbered in the order decided.

This folder is the decision log of record. Agent memory is not the decision log: it is an
agent's working continuity and is not the artifact. Where a decision file and an agent's memory
differ, this folder governs; where a decision file and the deliverable it approves differ, the
deliverable governs on the substance and this folder governs on who decided what, and when.

Step 18 assembles the final log from these files.

| # | Decision | Decided | Status |
| :--- | :--- | :--- | :--- |
| [0001](0001-step1-outcome-definition-gate.md) | **Step 1 outcome definition APPROVED** (gate 1 of 5). `H = 91 days` and the D12 cadence thresholds adopted by name; `pull_date` adopted in form with its value deferred; Red Team B2 overruled as accepted risk. | 2026-08-10 | Closed |
| [0002](0002-step4-history-endpoint.md) | **Step 4 source is `GET /users/:id/history`, unfiltered, one sweep per user.** Replaces `/users/:id/watched/shows`, which returns no per-episode timestamps. | 2026-08-10 | Closed |
| [0003](0003-w-estimation-sample.md) | **W is estimated on bucket C1 (all-at-once) shows only**, per D12, and applied to all shows. Closes Step 1 open question 2. | 2026-08-10 | Closed |

## Gates

Five. Nothing downstream of a gate runs without written Human Lead approval at it.

- [x] **Step 1** outcome definition — approved 2026-08-10 ([0001](0001-step1-outcome-definition-gate.md))
- [ ] Step 5 contamination exclusion rule
- [ ] Step 6 window W
- [ ] Step 7 liveness threshold
- [ ] Step 8 analysis table

## Open items carried forward

Recorded here so they are not lost between steps. Each is stated in full in the decision file
that surfaced it.

1. **`pull_date` has no value.** Deliberately deferred to Step 4's scheduling. Blocks any step
   that right-censors or computes D3, D8 or D9. ([0001](0001-step1-outcome-definition-gate.md))
2. **Step 1 open questions 1 and 3** remain open. The drafted boundary stands until decided.
   ([0001](0001-step1-outcome-definition-gate.md))
3. **The gap hypothesis is untested** — whether Trakt omits a gapped episode number or lists a
   placeholder. Section 3 is not a claim that gaps are handled. Not yet assigned to a step.
   ([0001](0001-step1-outcome-definition-gate.md))
4. **Provenance gap:** the 28 percent inflation figure and the six-week overlap cited in Step 1
   §2.1 and §5 trace only to an undocumented run in a machine-local log, with no run record and
   no script in `src/`. Numerically correct; not reproducible from the repo. No rule depends on
   them. ([0001](0001-step1-outcome-definition-gate.md))
