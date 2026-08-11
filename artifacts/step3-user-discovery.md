# Step 3: User Discovery

**Owner:** Analytics Engineer · **Mode:** Chained · **Checkpoint:** Human Lead reviews the yield curve before Step 4 runs at full scale
**Run:** 2026-08-11 01:44:31Z → 03:40:48Z UTC, 1h 56m
**Status:** Complete. Reviewed by Engineering, which returned HOLD on the crawl code; six defects were closed and the round metrics backfilled offline before this write-up.

Counts and aggregates only. No usernames, no user IDs, no per-profile detail. The pool itself lives in `raw/step3/` and never leaves this machine.

---

## The headline of this step

**The crawl stopped because it hit its usable-user target, not because discovery converged.** The
plateau rule never fired and was not close to firing: the 3-round moving average finished at
**31.4 percent of its running peak**, against a trigger of 20 percent.

The task sheet says "run until usable-user yield plateaus." That is not what happened, and the
distinction is the whole content of this document. **The pool is 4,088 usable users. It is not a
saturated sample of the reachable graph.** Every downstream number rests on it, so the ways in
which it is a *convenience* sample rather than an *exhausted* one are set out below in full.

---

## 1. What was spent and what came back

| | |
| :--- | :--- |
| Wall clock | 1h 56m |
| Live calls | **5,300** of a 6,500 budget (10 seed, 972 discovery, 4,318 screen) |
| Rounds | 36 |
| Stop reason | `sufficiency: reached the usable-user target` (4,000) |

| Funnel | Count |
| :--- | ---: |
| Discovered | 5,694 |
| Private (excluded) | 347 |
| Deleted | 0 |
| **Eligible** | **5,347** |
| Screened | 4,320 |
| Below the 10-episode floor | **232** (5.4% of screened) |
| **Usable** | **4,088** |

`4,320 − 232 = 4,088` exactly. **The floor is not inert:** it rejected 232 accounts, which bears
directly on §9 position 4 below — `MIN_EPISODES_USABLE = 10` is doing real work, not passing
everything through.

**Failures were low but not zero, and the distinction matters for Step 4.**

| Outcome | Count |
| :--- | ---: |
| Requests sent | 5,309 |
| OK | 5,300 |
| HTTP 5xx | 16 |
| Transport errors | 1 |
| **Transient retries** | **9** (all recovered; final `errors: 0`) |
| Rate-limit pauses (429) | 0 |
| 403 — user-resource skip | 0 |
| 403 — application-level | 0 |
| Access-denied users | 0 |
| Unavailable | 0 |

**The retry-with-backoff branch of `CLAUDE.md` API discipline was exercised live, nine times,
and recovered every time.** ~20 seconds of backoff sleep in total. Of the three failure paths the
discipline defines, **one is now live-tested and two are not**: the 429 path and both 403 branches
have still never run. Decision `0004` expected Step 3 to be the first live exercise of the amended
403 rule. It was not. **Step 4 will be the first real test of both.**

Failures fell on discovery calls; every round records `screen_other_status: 0`.

Screening itself was clean: 0 access-denied, 0 unavailable, 0 below-floor failures other than the
232 genuine floor rejections.

---

## 2. Sufficiency, not plateau

The plateau rule was: *3-round moving average of new eligible users per discovery call ≤ 20 percent
of its running peak, on 2 consecutive rounds, after at least 10 rounds.*

It never triggered. Final state: moving average **3.88**, running peak **12.33**, ratio **0.314**,
consecutive rounds below threshold **0**.

**The rule came within two marginal rounds of firing a plateau that did not exist.** Rounds 7–10
decayed into a saturated pocket; the 3-round averages at rounds 9 and 10 sat within 15 percent of
the trigger. Round 11 then returned a **4–6× rebound** (Channel A yield per call 0.46 → 6.25). Had
`MIN_ROUNDS_BEFORE_PLATEAU` been 9 rather than 10, the run would have stopped at round 10 and
reported "usable-user yield flattened" immediately before the graph proved it had not.

Two structural reasons the rule is weak, both now visible in the per-round record:

- **The peak is an artifact of round 1.** Round 1 discovers the seeds' own neighbours at near-zero
  dedup — a number that can never recur. The peak is anchored there permanently, so "20 percent of
  peak" is a fixed absolute threshold rather than a relative one.
- **It blends two channels with opposite dynamics** (Section 3). A collapse in one reads as a
  global plateau.

**Consequence for interpretation: the absence of a plateau is not evidence that the graph was
exhausted, and the presence of one would not have been either.** The stopping rule that actually
bound was the target count.

---

## 3. The two channels behaved nothing alike

| | Channel A (follower graph) | Channel B (public-list owners) |
| :--- | ---: | ---: |
| Discovery calls | 864 (**89%**) | 108 (**11%**) |
| New eligible users | 3,102 (61%) | 1,945 (39%) |
| Users per call | **3.6** | **18.0** |
| Yield per call, range | **0.04 – 15.08** | 2.00 – 41.67 |
| Usable users, by first channel | 2,306 | 1,782 |

324 users were reached by both channels.

### Channel B is exhausted

Channel B walks a deterministic cursor over a fixed universe of public lists. Its list-dedup rate
climbs from **0.20 at round 1 to 0.74–0.89 from round 25 onward**, and new eligible users per round
fall from 125 to **6–24**. Both feeds are near the end of their useful range: 7,066 list records
seen across `lists/popular` (3,611) and `lists/trending` (3,455), yielding 2,022 distinct owners.

**Channel B is not slowing down; it is running out.** Continuing it would cost calls at a steeply
rising price per user. This is a genuine exhaustion signal, and it is the only one in the run.

### Channel A is hub-luck, not convergence

Channel A's yield swings by a factor of ~360 round to round — 0.04 at round 15, 15.08 at round 26 —
with no trend. The pattern is not decay; it is whether the round happened to expand a
high-degree account.

This matters because it is the opposite of the failure the crawl was designed against. The
anti-clique measures (300 seeds, ≤100 neighbours per user, frontier round-robined across origin
seeds) guard against a walk **converging on one tight community**. That is not what happened.
**The walk barely branched at all**: only **432 of 5,694** discovered users were ever expanded, and
the seed set itself is only two-thirds worked through.

### The frontier grew monotonically and never drained

| | Round 1 | Round 36 |
| :--- | ---: | ---: |
| Frontier size | 496 | **2,970** |

The frontier **never emptied at any point in 36 rounds** (`frontier_exhausted: false` throughout),
and grew roughly 6× while the crawl ran. At exit it held 1,447 users at depth 1 and 1,523 at depth
2. **Depth 3 was never reached; the depth cap of 3 was never approached.**

A frontier that grows monotonically to the end means the same thing as the missing plateau, said a
second way: **the crawl was terminated with the graph wide open.** Reachable users were left
undiscovered in a quantity comparable to the pool itself.

---

## 4. Seeding bias, and its direction on the headline

**The narrow argument holds.** Seeds were the first 300 distinct public authors of comments on
**movies** (218 from `comments/recent/all/movies`, 82 from `comments/trending/all/movies`), across
172 distinct films. Movies cannot be in the Step 2 frame, which is TV shows with two or more
seasons, so **no user was selected because of anything they did on a measured show.** The task
sheet's prohibition — do not harvest usernames from comments on the shows being measured, because
that selects on the outcome — is satisfied.

**But "cannot select on the outcome" is not "does not bias the pool," and the two were treated as
equivalent when the crawl was designed.** Selecting on a covariate correlated with the outcome
biases the estimate as effectively as selecting on the outcome itself.

Movie-commenting is a strong marker of **tracking intensity**. Commenters are a small hyperactive
minority of any catalogue platform's users. Heavy trackers are more likely to continue into S2,
more likely to log their viewing completely, and more likely to survive the Step 7 liveness filter.

> **Direction: downward on the never-started share — the study's headline.**
> This runs the **same way** as the known liveness-exclusion bias that Step 14 must disclose. The
> two **compound; they do not cancel.**

Three things make this sharper than the generic "Trakt users are self-selected" caveat:

1. **Timing.** Seeds were drawn on 2026-08-11 from recency-ordered comment feeds, **27 days after
   the TV Time shutdown of 15 Jul 2026.** A recent-comment feed on that date oversamples the
   migration cohort — precisely the population Step 5's contamination rule exists to detect and
   exclude. If Step 5 removes a large slice, it removes it *after* the discovery budget is spent.
2. **The obvious remedy is cosmetic.** Excluding depth-0 users removes 300 of 5,694. Depth-1 users
   are *followers of commenters*, and follower graphs are homophilous, so the selection propagates
   rather than being confined to the seeds. Usable users by depth: **290 at depth 0, 1,393 at depth
   1, 623 at depth 2, 1,782 with no depth** (Channel B).
3. **Step 11 as specified cannot detect this.** Channel A selects on public social activity;
   Channel B selects on public list authorship. **Both select on public-facing activity.** A ≈ B is
   the likely result, and it would read as "no discovery bias" when it actually means two draws
   from the same biased frame agree. **Agreement between the two channels is not evidence of
   unbiasedness.**

**A measurable mitigation exists and is not yet specified.** Screening already records
`followers`, `following`, `episodes_watched`, `joined_at`, `total_plays` and progress fields per
user. The activity distribution of the pool is therefore measurable, and a depth- or
activity-stratified diagnostic would put a number on the bias rather than leaving it as a caveat.
Whether to add it to Step 11's brief, or to state the limitation in Step 14 instead, is the Human
Lead's call.

---

## 5. What the pool is, stated plainly

**4,088 usable users, tagged by channel, reached in 1h 56m for 5,300 calls.** It is:

- **A convenience sample, not a saturated one.** The frontier was 2,970 and growing at exit.
- **Biased toward heavy, currently-active trackers**, in the same direction as the liveness
  caveat, by a mechanism Step 11 as written cannot see.
- **Not one clique** — but also not a wide walk. 432 users expanded, depth ≤ 2 reached, **7,103
  distinct directed follow relationships** (see §7 on which edge count to use).
- **Weakly "usable."** `MIN_EPISODES_USABLE = 10` is a low bar. 4,088 usable users is not 4,088
  users who will contribute analysis rows, since a row requires completing some show's S1 within
  the Step 2 frame.

**A note on Channel A's cost.** It consumed 89 percent of discovery calls for 61 percent of the
eligible users, at 5× the cost per user of Channel B. That is defensible if the reason is arm
independence for Step 11 — two channels selecting differently is the point — but the trade was
never stated, and on cost alone it is the opposite of what one would choose.

---

## 6. What Step 4 will cost, corrected

`step4_pages_forecast` was computed per screened user from `total_plays`. **That field is absent
from 77 percent of cached `users/:id/stats` bodies** — Trakt returns two payload shapes — and for
those users the forecast silently read as exactly **1 page**. It has been corrected to
`episodes.plays + movies.plays`, which matched `total_plays` in 549 of 549 bodies where both were
present.

**Aggregated over all 4,088 usable users:**

| Statistic | Pages per user |
| :--- | ---: |
| Mean | **51.5** (sd 58.8) |
| Min / p25 / median / p75 | 1 / 17 / 36 / 66 |
| p90 / p95 / p99 / max | 109 / 151 / 289 / **1,034** |

**Total: 210,500 pages ≈ 210,500 calls ≈ 23.4 hours** of pure throttled time at 150 calls/minute —
realistically longer once latency and any overnight suspend are included. The top decile of users
holds **35.2 percent** of all pages.

An earlier estimate of ~86,000 calls was drawn from a 220-user sample that inherited the
`total_plays` bug. **The corrected figure is roughly 2.4× that.** This is the number the Step 3
checkpoint exists to produce, and it materially changes what Step 4 is.

---

## 7. Provenance recorded for Step 11

Step 11 checks discovery bias and cannot be reconstructed after the budget is spent. Recorded in
`raw/step3/`:

| File | Records | Contents |
| :--- | ---: | :--- |
| `user_pool.jsonl` | 5,694 | Pool with `channel_first`, `in_a`, `in_b`, `depth`, `origin_seed`, screen results |
| `edges.jsonl` | 7,426 | **Full edge list** — 3,909 via `followers`, 3,517 via `following`. See the note below on which pair count Step 11 should use |
| `seed_provenance.jsonl` | 300 | Feed, page and film per seed; 172 distinct films, max 24 seeds from one film |
| `channel_b_provenance.jsonl` | 7,066 | Feed, list id, owner; 2,022 distinct owners, max 1,405 lists held by one owner |
| `yield_curve.jsonl` | 36 | Per-round record, 81 fields |

**The edge list was previously a spanning tree.** Only the first parent edge per user was kept,
which is acyclic by construction and therefore could not answer Step 11's "is the pool one clique"
question at all. It was backfilled from cached bodies at zero live calls.

> **Which edge count to use, because each row carries two directions and they are not the same
> graph.** Every record has `(src, dst)` — the **crawl traversal** direction, who was expanded and
> who was found — and `(follower, followee)` — the **actual social** direction.
>
> | Reading | Distinct directed pairs | Reciprocal pairs |
> | :--- | ---: | ---: |
> | `(follower, followee)` — the social graph | **7,103** | 1,172 |
> | `(src, dst)` — crawl traversal | 6,166 | 235 |
>
> **Step 11 wants the social graph, 7,103.** The traversal reading is an artifact of walk order:
> it counts a mutual follow as reciprocal only if the crawl happened to expand both endpoints,
> which is why its reciprocity is ~5× lower and meaningless as a clustering signal.
>
> **One figure is unresolved.** `artifacts/step3-yield-curve.json` reports
> `reciprocal_pairs: 1353` where recomputation from `edges.jsonl` gives **1,172**. The two do not
> reconcile and `distinct_directed_pairs: 7103` agrees exactly, so the discrepancy is isolated to
> the reciprocity statistic. It is flagged rather than silently resolved, and **Step 11 should
> recompute reciprocity from `edges.jsonl` rather than reading it from the yield curve.** An
> earlier version of this write-up quoted the traversal figures without saying which reading they
> were, which is the error this note exists to prevent.

---

## 8. Method notes, and one honest gap

**Round metrics were backfilled by offline replay** of the crawl against the cache, using a session
whose only network method raises. **0 live calls, 5,302 cache hits, verified at 0 mismatches over
36 rounds × 12 fields** against what the live run recorded. Every round record carries
`metrics_source` and a per-field source map.

**One round looked like throttling and was not.** Round 8 recorded 2,796 seconds wall clock against
a single 2,697-second inter-request gap — 96.5 percent of the round — with zero 429s. That is a
suspended machine, not the API. The clock decomposition now distinguishes throttle sleep,
rate-limit sleep, backoff sleep, in-request time and unaccounted time, so this cannot be misread at
the checkpoint.

**Not recoverable: per-round throttle sleep seconds.** The client did not record it, and it cannot
be derived from the request log without assuming the throttle's own behaviour. It is left `null`
and marked `not_recoverable` rather than estimated. The measured largest-gap figure answers the
question it was wanted for. The client records it going forward.

---

## 9. For the Human Lead at the checkpoint

Four positions, none of which are the Analytics Engineer's to take:

1. **Step 4 costs ~210,000 calls and ~23 hours** at the current pool, ~2.4× the earlier estimate.
   Whether that is acceptable, or whether the pool should be sampled down, is a scoping decision.
2. **The pool is biased toward heavy active trackers, downward on the headline, compounding with
   the liveness caveat.** Either add an activity-stratified diagnostic to Step 11's brief, or state
   the limitation explicitly in Step 14. Step 11 as written will not surface it.
3. **The stop was sufficiency, not convergence.** If the study wants a claim about the reachable
   Trakt population rather than about 4,088 sampled users, the frontier is still open and the
   budget is not the binding constraint — the framing is.
4. **`MIN_EPISODES_USABLE = 10` makes "4,088 usable" a weak sufficiency claim.** Whether the target
   should be expressed in analysis rows rather than usable accounts is worth settling before
   Step 4, not after. The floor did reject 232 accounts (§1), so it is not inert — but a 10-episode
   bar is still a long way from "will contribute an analysis row," which needs S1 completion on a
   show inside the Step 2 frame.
5. **1,027 eligible users were discovered and never screened** (5,347 − 4,320). Extending the pool
   without any new discovery would cost ~1,027 screen calls. Because screening ran FIFO at 120 per
   round, **the unscreened are disproportionately depth 2** — depth 1 was screened at ~80 percent
   of its cohort against depth 2 at ~36 percent. **Any depth-stratified diagnostic must condition
   on screened, not on eligible**, or it will report a screening-order effect as a depth effect.

---

**Deliverables:** yield curve in `artifacts/step3-yield-curve.json` and `.csv` (counts only); pool,
edge list and provenance in `raw/step3/` (machine-local); run record in `logs/step3_run.json`.
