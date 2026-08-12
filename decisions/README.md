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
| [0009](0009-step4-pull-order.md) | **Step 4 pulls in stratified round-robin order** over ten equal-count forecast-page bins, so any early stop leaves a prefix proportional across the full distribution. Amends an initial median-out instruction, which left a *centered* slice with no heavy users. | 2026-08-11 | Closed |
| [0010](0010-step4-tail-cap.md) | **Tail cap at 300 forecast pages**, skip whole and never truncate, with an actual-pages guard that discards mid-sweep overruns. Justified as a **circuit breaker on forecast error**, not as protection against a slow user. Excludes 0.93% of the pool; direction **upward** on the headline. | 2026-08-11 | Closed |
| [0011](0011-pull-date-value.md) | **`pull_date = 2026-08-11`**, `τ_pull = 2026-08-11T00:00:00Z`. Closes the value D11 deferred until Step 4's schedule was known. Constraint satisfied: earliest per-user fetch is 05:01:26Z. | 2026-08-11 | Closed |
| [0012](0012-sweep-completeness-rule.md) | **Sweep completeness is full `page_count` coverage plus a 2% residual tolerance**, not exact match on `item_count` — which the pilot showed is not an exact record count. Over-count, under-count and genuine cross-page duplicates are counted **separately**. **Amends [0002](0002-step4-history-endpoint.md) and an approved gate artifact.** | 2026-08-11 | Closed |
| [0013](0013-step2-execution-delegation.md) | **Step 2 execution is delegated to an agent; the selection rules stay with the Human Lead.** Judgment is which shows belong and on what criterion; execution is fetching seasons and applying a written rule. **Amends the `CLAUDE.md` Human Lead ownership rule, for Step 2 only.** Three conditions: no concurrent live-API agents, candidate set recomputed on the full pool, underspecified rules reported not resolved. | 2026-08-11 | Closed |
| [0014](0014-no-content-filters-structural-fields.md) | **No content-category filters in the Step 2 frame.** The anime and daily-strip/soap exclusions are dropped before first use — the concern was release structure, not genre, and genre is a lossy proxy for it in both directions. Release structure is recorded as **fields**; thresholds set by the Human Lead after the distributions are visible. | 2026-08-11 | **Open — thresholds not yet set** |
| [0015](0015-step2-unaired-s2-exclusion.md) | **A listed-but-unaired season 2 is not a season 2 for the frame.** 12 shows excluded, all reporting `aired_episodes = 0`. Recorded as its own ledger step rather than folded into the date cutoff, which removed 60 — collapsing them would have made the ledger say 72. Resolves the one case the selection rules did not decide. | 2026-08-12 | Closed |
| [0016](0016-per-season-network-dropped.md) | **Per-season network dropped as a field; platform fragmentation is not a variable in this study.** 0.71% populated across 6,645 season objects; one show in 2,094 carries two distinct values, read as noise and not as fragmentation. **Closes the first open problem in [0014](0014-no-content-filters-structural-fields.md); the second survives and now attaches to the show-level network**, a present-day value that must not be read as release-time availability. | 2026-08-12 | Closed |
| [0017](0017-air-period-definition.md) | **Air period := calendar year of the S2 finale, bucketed pre-2020 / 2020–2022 / 2023–2025**, bracketing the production shutdown and claiming nothing finer. Carries a confound that travels with it: **air period and cadence are strongly collinear** on this frame and are not independent cuts. | 2026-08-12 | Closed |
| [0018](0018-size-quintile-base.md) | **The title size quintile is cut over the 1,226-show frame, not the 2,094 candidates** — the quintile cuts results, and results exist only in-frame. The rejected base gave unequal bins labelled as quintiles. A quintile label is **not a stable identifier**: rebuild the frame and every boundary moves. | 2026-08-12 | Closed |
| [0019](0019-pool-completers-recomputed.md) | **`pool_completers` recomputed on real season lengths; the max-observed proxy is superseded and no result may use it.** Changes nothing on this frame — proxy `L1_hat` equals real `\|E1\|` on 1,225 of 1,226 shows — which is not a rehabilitation of the proxy generally. **Corrects the stated premise of [0013](0013-step2-execution-delegation.md) condition 2:** counts do not only rise; 118 long-tail shows fell between pool sizes. | 2026-08-12 | Closed |

**A note on authority.** Entries 0001–0004 and 0013–0019 are Human Lead decisions. **0005–0007 are agent-taken,
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

1. ~~**`pull_date` has no value.**~~ **CLOSED 2026-08-11** — set to `2026-08-11` as
   [0011](0011-pull-date-value.md). Right-censoring and D3/D8/D9 are unblocked.
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
   order that makes it harmless is not recorded. **Does not arise on the current frame
   (2026-08-12): `min(L2) = 2` and zero in-frame shows have `L2 = 1`,** so no show is
   misclassified by the ordering today. The ordering is still unwritten and the frame will change
   if the pull resumes, so this stays open. ([0019](0019-pool-completers-recomputed.md))
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
    roughly 2.4× an earlier sampled estimate that inherited a `total_plays` bug.
    **Partly addressed:** [0009](0009-step4-pull-order.md) makes an early stop survivable and
    [0010](0010-step4-tail-cap.md) trims 1.7 hours, but the run is still not expected to finish the
    pool in one window. Whether to sample the pool down remains unsettled.
    ([0006](0006-step3-crawl-constants.md))
12. ~~**`reciprocal_pairs: 1353` is a counting bug.**~~ **CLOSED 2026-08-11.** Fixed in
    `src/step3_backfill.py` and regenerated: `artifacts/step3-yield-curve.json` now reports
    **1,172**, matching an independent recount from `raw/step3/edges.jsonl`.
    `distinct_directed_pairs: 7103` was always correct. ([0007](0007-step3-channel-cost-trade.md))
13. ~~**`MIN_EPISODES_USABLE = 10`'s warrant is unverified.**~~ **CLOSED 2026-08-12 — checked against
    the frame and the retained screen records, and ACCEPTED by the Human Lead.** Verified facts, in
    the order they were asked for:
    - **What it counted.** `src/step3_user_discovery.py:953–954`, `ep_watched =
      int(episodes.get("watched") or 0); usable = ep_watched >= MIN_EPISODES_USABLE` — the
      `episodes.watched` field of `GET /users/:id/stats`, an **account-wide count of distinct
      episodes across all shows**. Not play records: the same block reads `episodes.plays`
      separately. Across all 4,319 cached stats bodies `watched < plays` in 3,523 and
      `watched == plays` in 796, **never greater**. It is **not per-show** — ten episodes across ten
      shows passes, nine inside one show fails.
    - **What it removed.** **232 accounts, and nothing else removed any.** Over 4,320 screened:
      `ok` 4,088, `below_episode_floor` **232**, `access_denied` 0, `unavailable_*` 0, `status_*` 0.
      Corroborated by `logs/step3_run.json` and `artifacts/step3-user-discovery.md` §1.
    - **What those accounts held. 210 of the 232 have `episodes_watched = 0`.** Only 22 have any
      episodes at all, the maximum being 6 (counts: 0→210, 1→5, 2→3, 3→5, 4→4, 5→1, 6→4).
    - **The warrant is still not literally true**, and that is what is being accepted rather than
      denied: `min(L1) = 1` over the frame and 159 in-frame shows have `L1 ≤ 6`, so a 6-episode
      account is not arithmetically barred from having completed an in-frame S1. **The exposure is
      at most 22 accounts, 0.5% of the 4,320 screened**, not the 232 the floor rejected.
    - **The removed accounts are fully recoverable** — slug and complete screen record for all 232
      in `raw/step3/user_pool.jsonl` and `raw/step3/state.json`, with their stats bodies already
      cached under `raw/users/*/stats/`. Recovering them costs **0 live calls**; a full history pull
      of all 232 would cost **296 pages** (30 for just the 22 with any episodes), and the forecast is
      exact at that size — observed users with a 1-page forecast read exactly 1.00 pages, 2-page
      exactly 2.00.
    - **Not recoverable:** what the crawl would have found had those accounts remained in the
      frontier as expansion sources. That path was not taken and is not reconstructible from disk.
    ([0006](0006-step3-crawl-constants.md), `artifacts/step2-frame-ledger-and-distributions.md` §3.2)
14. ~~**The Step 3 seed source has no decision entry.**~~ **CLOSED 2026-08-11** — recorded as
    [0008](0008-step3-seed-source.md).
15. **A rule inside the approved Step 1 gate was amended without Red Team review.**
    [0012](0012-sweep-completeness-rule.md) changes the completeness test in Step 1 §0. The gate's
    own approval record says a rule change reopens the gate. Recorded as a Human Lead amendment;
    **not yet put to Red Team.** Worth settling before results are computed.
16. **`step3_backfill.py --out-dir raw/step3` zeroes the call ledger in `state.json`**, because the
    offline replay spends no live calls. **This has happened twice** and been restored from
    `logs/step3_run.json` both times; a `ledger_note` in the file records it. Either restore after
    every regeneration or use the script's default out-dir, which does not touch that file. The
    ledger is the only record of Step 3's spend against the API budget and it is gitignored.
17. **The Step 2 structural thresholds are deferred, not skipped.** Until the Human Lead sets them,
    the frame carries **no exclusion on gap length and no exclusion on season size**. Consequence,
    stated now rather than discovered later: **any headline computed before those thresholds are set
    is provisional** — it runs over a population still containing whatever release structures the
    candidate set happens to hold, including the ones the dropped content filters were reaching for.
    Usable for diagnostics and for seeing the distributions; not the study's result.
    ([0014](0014-no-content-filters-structural-fields.md))
18. **Platform fragmentation — problem (a) CLOSED 2026-08-12, problem (b) still open and relocated.**
    ~~(a) it is not established whether Trakt exposes a **per-season** network.~~ **Measured: it does,
    and it is empty — 0.71% populated across 6,645 season objects, one show in 2,094 with two
    distinct values.** Dropped as a field per 0014's own resolution rule, recorded as
    [0016](0016-per-season-network-dropped.md). **Platform fragmentation is not a variable in this
    study**; no result may control for it, stratify on it, or rule it out.
    **(b) survives, and now attaches to a different field.** The show-level `network` pulled on
    2026-08-12 is 100% populated with 150 distinct values, and it records **today's** network — a
    title that moved services between seasons shows only its current one. **`show_network` must not
    be used as a release-time availability measure.** Retained as a descriptive field only.
    ([0014](0014-no-content-filters-structural-fields.md), [0016](0016-per-season-network-dropped.md))
19. **The Step 2 frame is built on a stopped pull, and every frame-derived boundary moves if it
    resumes.** The candidate set rests on 2,549 users, 62.9% of plan. The stop is proportional across
    all ten strata (decided share 69.6–70.1%), but the *analysed* cohort is proportional only to
    within 6.1 points, because the [0012](0012-sweep-completeness-rule.md) discard rate varies by
    stratum (complete share 59.3% in bin 5 to 65.4% in bin 7). Consequences that are not yet
    decisions: the ≥50 candidate rule was applied to **proxy** counts and has not been re-applied to
    the recomputed ones ([0019](0019-pool-completers-recomputed.md)); **size quintile boundaries are
    valid only against the frame they were cut on** ([0018](0018-size-quintile-base.md)); and the
    frame is systematically older than the catalogue, 66.6% of it with an S2 finale before 2020
    ([0015](0015-step2-unaired-s2-exclusion.md)).
