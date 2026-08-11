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
| [0005](0005-step3-stopping-rule.md) | **Step 3 stopped on `TARGET_USABLE = 4000`, not on the plateau rule `task-sheet.md` names.** The plateau rule ran 36 rounds and never fired. Agent-taken; departs from the task sheet. | 2026-08-11 | **Open — needs ratification** |
| [0006](0006-step3-crawl-constants.md) | **The twelve Step 3 crawl constants**, none of which appear in `task-sheet.md`. Two carry known consequences: the usable floor and a FIFO screening-order artifact. Agent-taken. | 2026-08-11 | **Open — needs ratification** |
| [0007](0007-step3-channel-cost-trade.md) | **Channel A took 89 percent of discovery calls at 5× the cost per user** on whole-run averages — though it was the *cheaper* channel over the last third. Defensible as buying Step 11 arm independence. Agent-taken. | 2026-08-11 | **Open — needs ratification** |
| [0008](0008-step3-seed-source.md) | **Step 3 seeded from movie-comment authors.** Satisfies the task sheet's prohibition but biases the pool toward heavy trackers — **downward on the headline**, compounding with the liveness bias. The highest-consequence agent choice in Step 3. | 2026-08-11 | **Open — needs ratification** |

**A note on authority.** Entries 0001–0004 are Human Lead decisions. **0005–0007 are agent-taken,
inside a Chained step, and are recorded retrospectively for ratification** — they shaped the
population every downstream number rests on, and a constant that shapes the population is a decision
whether or not it was treated as one at the time. They are listed here so the distinction between
"decided" and "defaulted into" stays visible.

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
9. **The 403 rule's live behaviour is still unobserved — Step 3 did not exercise it.** 5,300 calls
   produced zero 403s and zero 429s, so both 403 branches and the 429 path remain untested against
   the live API. **Step 4 is now the first exercise.** What Step 3 *did* exercise, nine times and
   successfully, is the retry-with-backoff branch (16 HTTP 5xx, 1 transport error, all recovered).
   One of the three failure paths is live-tested; two are not. ([0004](0004-403-handling.md))
10. **The pool is biased toward heavy, currently-active trackers**, direction **downward on the
    never-started share**, compounding with the liveness-exclusion bias rather than cancelling it.
    Step 11 as written cannot detect it: both channels select on public-facing activity, so
    agreement between them is not evidence of unbiasedness. Either Step 11's brief gains an
    activity-stratified diagnostic — computable from `raw/step3/` at zero further live calls — or
    Step 14 states the limitation. ([0005](0005-step3-stopping-rule.md), `artifacts/step3-user-discovery.md` §4)
11. **Step 4 costs ~210,500 calls and ~23.4 hours** of pure throttled time at the current pool,
    roughly 2.4× an earlier sampled estimate that inherited a `total_plays` bug. Whether to accept
    that or sample the pool down is unsettled. ([0006](0006-step3-crawl-constants.md))
12. ~~**`reciprocal_pairs: 1353` is a counting bug.**~~ **CLOSED 2026-08-11.** Fixed in
    `src/step3_backfill.py` and regenerated: `artifacts/step3-yield-curve.json` now reports
    **1,172**, matching an independent recount from `raw/step3/edges.jsonl`.
    `distinct_directed_pairs: 7103` was always correct. ([0007](0007-step3-channel-cost-trade.md))
13. **`MIN_EPISODES_USABLE = 10`'s warrant is unverified.** It assumes no S1 in the frame is shorter
    than 10 episodes, but Step 1 §7 retains `L1 = 1` and no minimum S1 length is set anywhere.
    **Checkable as soon as Step 2 exists: `min(L1)` over the frame.** If it fails, the excluded users
    are light trackers — downward on the headline, compounding with the seeding bias.
    ([0006](0006-step3-crawl-constants.md))
14. ~~**The Step 3 seed source has no decision entry.**~~ **CLOSED 2026-08-11** — recorded as
    [0008](0008-step3-seed-source.md).
15. **`step3_backfill.py --out-dir raw/step3` zeroes the call ledger in `state.json`**, because the
    offline replay spends no live calls. **This has happened twice** and been restored from
    `logs/step3_run.json` both times; a `ledger_note` in the file records it. Either restore after
    every regeneration or use the script's default out-dir, which does not touch that file. The
    ledger is the only record of Step 3's spend against the API budget and it is gitignored.
