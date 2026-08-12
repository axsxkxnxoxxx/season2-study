# Partner reviews — Step 2 (Product) and Step 4 (Engineering)

**What this is:** the record of the two partner reviews fired at Steps 2 and 4. Partner reviewers
**produce no work and own no folder** — their verdicts existed only in the session transcript and
would have been lost. Recorded here at the Human Lead's instruction, on the same reasoning that put
`artifacts/step5-red-team-reviews.md` on disk.

**Neither review approves, adopts or changes anything.** Reviewers return a position; only the Human
Lead decides. Where a finding has since been ruled on, the ruling is named — the reviews themselves
are transcribed as delivered, not edited to match what happened afterwards.

**Aggregates, counts and reasoning only.** No usernames, user IDs or individual watch histories.

| | |
| :--- | :--- |
| **Step 2 — Product Management** | *"Verdict on whether the frame matches what a roadmap would need."* **Split: proceed on the population, hold on the field inventory.** |
| **Step 4 — Engineering** | *"Throughput and failure rates."* **Split: PASS on the pull, FAIL on its record, resume feasible at ~7.8 h.** |

---

## 1. Step 2 — Product Management

**Verdict: proceed on the population, hold on the field inventory.**

> *"The population is right. The field set is not. I would sign off on which 1,138 shows are in the
> frame. I would not hand this table to a slate owner as-is, because the two axes a roadmap actually
> cuts on — what platform and how well was it received — are one unrecoverable and one thrown away
> for free."*

### What it credited

Dropping the genre filters ([0014](../decisions/0014-no-content-filters-structural-fields.md)) was
correct and it would have argued for it. **The levers a roadmap actually controls survived as
fields** — cadence bucket, gap length, S2 episode count, air period and S1 size are the four things
a release plan *sets*, all at 100% population, so the frame can answer "all-at-once versus weekly"
and "18-month gap versus 9" in principle. The 26-episode and 1,095-day caps drew no objection:
[0020](../decisions/0020-step2-structural-thresholds.md)'s insensitivity table was called "exactly
the right defence" and the C4 tilt "disclosed rather than discovered."

### Findings 1, 2 and 4 — ruled on, now [0030](../decisions/0030-frame-field-corrections.md)

**Finding 1 — `show_network` has no stable semantics.** Checked against the frame it errs in *both*
directions: Arrested Development (S2 2005) reads Netflix, Brooklyn Nine-Nine reads FOX having ended
on NBC, Community reads Yahoo! Screen. **73 of 177 Netflix-tagged shows have a pre-2020 S2 finale.**
Strictly worse than the disclosed "present-day" defect, because a present-day value has a bounded
direction of error and this has none. *Its `The Killing` example does not hold — the frame's row is
the Danish original on DR1, not the AMC remake. The other six stand.* **Ruled: dropped.**

**Finding 2 — the reception axis was free and was not taken.** `rating`, `votes`, `comment_count`,
`airs.day` and `subgenres` were already in the cached bodies. Without them *"long gaps abandon more"*
cannot be separated from *"long gaps happen to troubled shows"* — an objection raised in the first
ten minutes with no answer available. It named the objection to its own ask, that 2026 ratings are
partly caused by the outcome being studied, and answered it: `votes` is far less contaminated, and
**a disclosed confound beats an absent variable**. **Ruled: added.**

**Finding 4 — `size_quintile` is size × exposure.** A 2012 title has had fourteen years to
accumulate completers, a 2025 title four. **Ruled: separated** — and the obvious fix turned out
wrong, per-year over-correcting worse than raw under-corrected, so the primary is now the
within-cohort rank.

### Finding 3 — the ≥50 floor. Ruled as [0031](../decisions/0031-the-50-completer-floor.md)

> *"The ≥50 completer floor is the largest population rule in the study, and it is the only one with
> no decision entry and no sensitivity analysis."*

The frame is **2.6% of the shows the pool has any evidence for** — 44,617 → 2,094 → 1,138. Moving
the floor to 25 grows the candidate set **81%**; to 100 halves it. Every other threshold went
through [0014](../decisions/0014-no-content-filters-structural-fields.md)'s discipline of *look at
the distribution, then draw the line*; this one did not, while a 12-show exclusion got
[0015](../decisions/0015-step2-unaired-s2-exclusion.md) to itself.

**Its roadmap point is the one that survives the ruling:** *"a slate's genuinely hard renewal calls
cluster in the marginal performer, not the top 2.6%."* Step 14's "no result generalises to them" is
correct disclosure but is doing a great deal of work.

It asked for the entry and one number, not for the floor to move. **The entry exists; the number —
what the frame looks like at ≥25 — does not, and cannot without 1,699 API calls.**

### Finding 5 — the recent cohort is thin, and thin in a compounding way. NOT RULED

| S2 finale year | Shows |
| ---: | ---: |
| 2023 | 72 |
| 2024 | 59 |
| **2025** | **37** |

The 2023–2025 bucket is **168 shows**, and within it the release-strategy comparison a roadmap would
act on has cells of **C1 45 / C2 38 / C3 59 / C4 26**.

[0017](../decisions/0017-air-period-definition.md) already discloses the era–cadence confound. What
is **not** on the record is that the within-era comparison — the only way around that confound —
lands in cells this small. And a third term compounds it: **the ≥50 floor is a higher bar for recent
titles**, so the modern cohort is *differently selected*, not merely smaller. The frame write-up
attributes the age skew entirely to the exclusion of unaired and recent second seasons; **that is
not the whole mechanism.**

On right-censoring it declined to overstate: with `τ_pull = 2026-08-11`, `W = 108` and `H = 91`,
retention needs `T0 ≤ 2026-01-24`, and only ~10 in-frame shows have an S2 finale in Oct–Dec 2025. At
the `W = 213` arm those ~10 drop out. **What it could not compute was the uncapped
`S1_completion_date` term** — subsequently measured and now carried by
[0030](../decisions/0030-frame-field-corrections.md): the 2023–2025 cohort loses **10.3%** of its
pairs at `W = 213` against **2.7%** pre-2020, survivors skewing to early adopters.

**Its ask, unactioned:** Step 8's waterfall mandates per-bucket counts for the five D12 cadence
buckets but **not per-`air_period` retained-pair counts after right-censoring**. Adding that line is
free and is the only way to see whether the modern cohort survives to the headline in usable
numbers. It routed the request to the Step 8 gate.

### Its Step 15 warning — a stated intention, not a Step 2 objection

> *"Finding 5 cannot be fixed and should therefore bind Step 15. The modern cohort is 168 shows with
> single-digit-to-40s cells on the release-strategy cut. When I review the decision rule, I will be
> asking whether its action is stated at a confidence the 2023–2025 evidence actually supports, or
> whether it is a pre-2020 finding wearing a streaming-era label. That is a fair warning about what
> I will be looking for, not a Step 2 objection."*

### The inconsistency it flagged without holding on it

That the approved Step 1 said **31 Dec 2024** in five places while the frame was built at
**2025-12-31**, calling it *"README open item 23's exact failure mode."* **Since resolved** — Step 1
carries a post-approval addendum, `task-sheet.md` Step 2 is corrected, and the margin is recorded at
24 days ([0030](../decisions/0030-frame-field-corrections.md)).

---

## 2. Step 4 — Engineering

**Verdict: PASS on the pull, FAIL on its record, resume feasible.**

> *"The Step 0 contract held under 126,391 live requests. Throttle correct and binding, retry
> correct, resume correct, nothing re-requested, no silent drops. The failure profile is genuinely
> good and I have no objection to it."*

### A — the Step 4 deliverables were stale. BLOCKING. Since fixed

`logs/step4_run.json` and `logs/step4_pull_log.json` — the files `task-sheet.md` names as Step 4's
deliverable — were both written at `20:12:56` by a **`--max-users 3` run**:

| | Stale | Actual |
| :--- | ---: | ---: |
| complete | 2,137 | **2,549** |
| discarded_over_tolerance | 235 | **287** |
| users decided | 2,410 | **2,874** |
| live calls | 102,735 | **126,145** |

Cause: the record-writers fire only from `main()`'s `finally`, and neither long run reached it.

**It also corrected a claim this project had been repeating.** *"'It exited cleanly' is not supported
by the artifacts. It stopped safely — the fsynced append-only ledger, the atomic progress file and
the raw cache all held, and no data was lost. That is a different claim from exiting cleanly, and
only the first one is true."* `step4_progress.json` carries `finished: false, stop_reason: null`, and
both console logs end mid-stream with no exit line.

**Resolved 2026-08-12** by the fix it proposed — a `--max-users 0` invocation, which stops on a
committed condition at **zero API calls**. Both files now read 2,549 / 287 / 2,874 / 126,145 with
`stop_reason: "reached --max-users 0"`, verified against an unchanged request-log line count.

### B — the resume estimate on disk is wrong by ~1.8×. NOT RULED

`projected_hours_remaining: 4.28` was computed from **8 users over 100 seconds**, 123 of whose pages
were free cache hits, and it is **user-count based** — so it cannot see that under stratified
round-robin the untouched users are systematically the heavier half of every bin. Observed mean
pages/user: **43.3** over the first 2,372, **50.5** over the next 464, **~58** implied for the
remainder.

**Its estimate: ~70,000 calls, ~7.8 hours** at 150/min. Settled exactly by summing `forecast_pages`
over `pull_order.jsonl` rows with `pull_rank >= 2836`.

### C — the live-call ledger under-counts real API spend. NOT RULED

**126,391 requests actually sent** (126,390 responses + 1 transport error) against **126,145**
recorded. **Gap: 246.** A run killed mid-sweep never writes the ledger row, but its calls were
already sent; 81 of the 246 are the interrupted user, confirmed against cached pages.

The module documents three guards for *"the live-call ledger cannot be zeroed by an offline
replay."* All three hold. **None addresses this one.** *"For API-discipline purposes the
authoritative spend figure is the `api_requests.ndjson` count, not `live_calls_recorded`. 0.2%
today; the mechanism is unbounded."*

### D — the failure log is not partitioned by state dir. NOT RULED

`logs/step4_failures.ndjson` holds **301** rows: 287 discards plus **14** short-read rows — seven
users written twice, once live and once by an offline replay. The canonical ledger has **7**, all
since recovered. `OfflineGuard` protects the ledger and `state.json` from replays; it does **not**
protect the failure log or the API log, both pinned to `LOGS_DIR` regardless of `--state-dir`.
Reading that file as a failure count gives 301; the truth is 287 terminal discards and zero
unrecovered errors.

### E — the failure rates themselves. NO OBJECTION

- **Zero 429s ever. Zero 403s ever.** No 401/404, no pagination drift, across the whole project.
- **2 HTTP 500s and 1 read timeout**, all recovered on retry attempt 1 with ~2.4 s backoff —
  **3 transient events in 126,391 requests, 24 ppm.**
- 7 `error_short_read`, all under the superseded `exact` rule, all now `complete`. **Zero
  unrecovered errors.**
- 287 discards = **10.1%** of 2,836 attempted, stable against 9.9% at the 2,372 mark.

**It tested whether the discard rate tracks sweep size**, because if it did the heavier remaining
30% would discard faster and the resume projection would be wrong. Per-bin discards, bins 0→9:
**20, 27, 34, 30, 26, 44, 31, 18, 22, 35** over ~284 attempted per bin — range 6.3%–15.5%, **no
monotone trend** across forecasts from 1 to 292 pages. So ~10% is safe planning and a resume projects
to **~3,640 of 4,050, ~89.9%**.

But it is **not homogeneous**: bin 5 at 15.5% is roughly **+3 SD** on a binomial at p = 0.101,
n = 284. *"Something other than sweep length drives the discard. That is a lead for the Step 14
limitation, not a throughput problem, and I am not taking it further."*

### F — resume hazards, in its order. NOT RULED

1. **The exclude file** holds one slug with no expiry. Resume with the flag and the ceiling is 1,213
   and that user is never decided; resume without it and its 81 cached pages finish the sweep at
   near-zero marginal cost. *"Either is defensible; silently inheriting the flag is not."*
2. **Disk is unmeasured** anywhere in the run record, progress file or artifact. `_write_cache`
   raises `OSError`, which is not a `TraktClientError`, so it escapes every handler and lands in
   `main()`'s bare `except Exception` — and the `finally` then attempts three more disk writes.
   **A disk-full ends the run with a traceback and no run record: the same signature already on
   disk.**
3. **Sabbath.** The default `FRI 17:30–SAT 20:30` window is 27 hours; a ~7.8 h run does not fit
   before a Friday-evening start, and the run does not restart itself afterwards.
4. **Delay cost, not a defect.** `τ_pull` and the D11 constraint survive a later resume, but every
   day widens the earliest-to-latest fetch spread beyond the current 15 hours.

### G — two settled items, from the throughput angle

- [0023](../decisions/0023-step4-completeness-rule-upheld.md) declined the final-page shape test on
  cascade cost at ~2,800 calls. **If the pull resumes at all, that is 4% of the calls and 4% of the
  wall-clock of the resume itself.** It explicitly did not reopen the cascade argument: *"The cost
  half is not an engineering constraint at this scale and should not be read as one."*
- **All 287 discards keep their pages** under the current schema version, so re-deciding every one
  under a changed tolerance is `--retry-outcomes discarded_over_tolerance` at **zero API cost** —
  including the 31 positive-residual discards `0023` flags as removed in the direction `0012` itself
  calls safe. *"That option is free for what is on disk and only for what is on disk. It does not
  extend to the 1,214 never attempted."*

---

## 3. Independent verification by the main session

Checked directly against the repository, not taken on either reviewer's word.

| Claim | Result |
| :--- | :--- |
| Netflix-tagged shows / pre-2020 S2 finale | **177 / 73** — exact |
| `show_network` errs in both directions | **Confirmed** — six of seven examples; `The Killing` is the Danish original and does not hold |
| Recent cohort by S2 finale year | 2023 **72**, 2024 **59**, 2025 **37** — exact |
| 2023–2025 cadence cells | C1 45 / C2 38 / C3 59 / C4 26 — exact |
| Q5 composition, raw count | frame 14.8% vs Q5 **12.3%** — exact |
| ≥50 floor has its own decision entry | **No** — appeared only inside 0014, 0019, 0023 |
| Step 1 says 31 Dec 2024 | **5 occurrences** — confirmed |
| Step 4 deliverables stale | **Confirmed** — 2,137/235/2,410/102,735 against 2,549/287/2,874/126,145 |
| Requests actually sent in Step 4 | **126,391** (126,390 + 1 transport error) vs 126,145 recorded — **gap 246**, exact |
| `step4_failures.ndjson` row count | **301** = 287 discards + 14 short-read rows for 7 users — exact |
| Regeneration cost | **0 live calls** — request-log line count unchanged at 138,431 |

---

## 4. What is outstanding

**Ruled and closed:** product findings 1, 2 and 4 ([0030](../decisions/0030-frame-field-corrections.md));
product finding 3 ([0031](../decisions/0031-the-50-completer-floor.md)); the 2024/2025 inconsistency
([0030](../decisions/0030-frame-field-corrections.md)); engineering finding A, fixed 2026-08-12.

**Not ruled:**

1. **Product finding 5** — the recent cohort is 168 shows with cells of 26–59 on the release-strategy
   cut, and the ≥50 floor makes it *differently selected* rather than merely smaller. Its concrete
   ask: **add per-`air_period` retained-pair counts after right-censoring to Step 8's waterfall.**
   Free, and the only way to see whether the modern cohort survives to the headline.
2. **The Step 15 warning** — the reviewer has stated it will ask whether the decision rule's action
   is stated at a confidence the 2023–2025 evidence supports.
3. **Engineering B** — the resume estimate on disk remains 4.28 hours against a measured ~7.8.
4. **Engineering C** — the call ledger under-counts by 246 and the mechanism is unbounded.
5. **Engineering D** — the failure log is not partitioned by state dir and reads 301 against 287.
6. **Engineering F** — the exclude-file expiry, unmeasured disk, and the Sabbath window all bear on
   any resume.
7. **Engineering E's residual** — the discard rate is not homogeneous across bins (bin 5 at +3 SD),
   and sweep length is not what drives it.

---

## 5. Files

| File | Contents |
| :--- | :--- |
| `artifacts/partner-reviews-steps-2-and-4.md` | this file |
| `artifacts/step5-red-team-reviews.md` | the four adversarial reviews, recorded on the same reasoning |
| `artifacts/step2-frame-ledger-and-distributions.md` | the Step 2 deliverable under review |
| `artifacts/step4-pull-order-and-tail-rule.md` | the Step 4 deliverable under review |
| `logs/step4_run.json`, `logs/step4_pull_log.json` | regenerated 2026-08-12 at zero API calls |
