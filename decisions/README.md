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
| [0004](0004-403-handling.md) | **A 403 on a user resource skips that user and continues**, bounded by two circuit breakers; any other 403 still hard stops; ambiguity resolves strict. Amends `CLAUDE.md` API discipline. | 2026-08-10 | Closed |

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
4. ~~**Provenance gap:** the 28 percent inflation figure and the six-week overlap cited in Step 1
   §2.1 and §5 are not reproducible from the repo.~~ **CLOSED 2026-08-10** — reproducible at zero
   live calls via `src/step0_history_probe.py`, with a run record and a public write-up. Both
   figures reproduce (28.125 percent, 5.90 weeks). It also produced a post-approval addendum to
   Step 1 §5. ([0001](0001-step1-outcome-definition-gate.md))
5. **An unobserved premise inside an approved rule:** Step 1 §2.1 asserts `episode.ids.trakt` may
   disagree with `(season, number)`; the probe shows 96 IDs, 96 pairs, zero disagreements. Not
   contradicted, unobserved — but it is the mechanism **D9's split signature** depends on.
   ([0001](0001-step1-outcome-definition-gate.md))
6. **D2 cannot size the failure the §5 addendum names.** D2 runs on the operative first-pass
   clock, where the artifact does not appear. **Expect zero, and zero is not evidence of
   rarity.** Sizing it requires D2 inside the Step 13 last-observed arm.
   ([0001](0001-step1-outcome-definition-gate.md))
7. **The `L2 = 1` / cadence-classification ordering is written nowhere.** Classification is
   available from Step 2; the `L2 = 1` exclusion happens at Step 8. At `L2 = 1` the weekly span
   is 0, which falls in bucket C2 — harmless only because those shows are excluded, and the
   order that makes it harmless is not recorded.
8. **The gap hypothesis still has no owning step** — see item 3. Visibility is not ownership.
9. **The 403 rule's live behaviour is unobserved.** No live 403 has ever been seen; the
   discriminator is inferred from endpoint path, not observed. First live exercise will be
   during Step 3 or Step 4 and should be treated as a test of the rule, not as routine.
   ([0004](0004-403-handling.md))
