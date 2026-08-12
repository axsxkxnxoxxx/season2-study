# Decision 0032 — The Step 4 deliverables are regenerated; the pull stopped safely, not cleanly; the resume cost is restated

| | |
| :--- | :--- |
| **Decision** | The stale Step 4 deliverables are **regenerated at zero API calls**. The pull is recorded as having stopped **safely, not cleanly**. The true resume cost is **~70,000 live calls and ~7.8 hours**, not the 4.28 hours the progress file reports. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Occasioned by** | `reviewer-engineering`'s Step 4 review, finding A (blocking) and finding B |
| **Record of the review** | `artifacts/partner-reviews-steps-2-and-4.md` |
| **Status** | Closed |

---

## 1. What was stale

`logs/step4_run.json` and `logs/step4_pull_log.json` — the files `task-sheet.md` names as **Step 4's
deliverable** — were both written at `20:12:56` by a **`--max-users 3` run**, and had been read as
the record of the pull ever since.

| | Stale deliverable | Actual, from `state.json` + ledger |
| :--- | ---: | ---: |
| complete | 2,137 | **2,549** |
| `discarded_over_tolerance` | 235 | **287** |
| users decided | 2,410 | **2,874** |
| live calls recorded | 102,735 | **126,145** |

**Stale by 464 decided users and 23,410 calls.**

**Mechanism.** `write_pull_log` and `write_run_record` fire only from `main()`'s `finally` block.
Neither long run reached it, so the last file written was the one from a three-user run that *did*
terminate normally. The canonical state was never wrong — `processed/step4/state.json` and the
append-only ledger carried the true counts throughout. **Only the published record was wrong**, which
is the worse failure of the two: a reader with no access to `processed/` had no way to know.

## 2. The fix, and its cost

**`--max-users 0`.** `_should_stop()` evaluates `users_attempted_this_run >= 0`, which is true at the
first check, and that check sits **before any sweep begins** — so the run stops on a committed
condition, writes both records from the real state, and touches the network zero times.

**Verified rather than assumed:** `logs/api_requests.ndjson` held **138,431** lines before the run
and **138,431** after. Both files now read **2,549 / 287 / 2,874 / 126,145**, with
`stop_reason: "reached --max-users 0"` and `live_calls_this_run: 0`.

**These files live in `logs/`, which the study's file rules keep off git.** The fix is on disk and is
not in version control, by design.

## 3. The pull stopped safely. It did not exit cleanly.

This corrects a characterisation that had been repeated throughout the project, including in the
session that ran the pull.

**What the artifacts actually show:** `logs/step4_progress.json` carries `finished: false` and
`stop_reason: null`; `step4_full_console.log` ends at rank 2368 and `step4_resume_console.log` at
rank 2836, both mid-stream with no exit line; and the `finally` block that would have written the
run record never ran. A deliberate interrupt would have printed
`interrupted; the user in progress was not written to the ledger` and written the record. **It did
not.**

**What did hold, and why "safely" is the right word:** the fsynced append-only ledger, the atomic
progress file and the raw cache all survived. **No data was lost, no user was silently dropped, and
nothing was double-counted.** The 7 `error_short_read` users were retried to `complete`; the
interrupted user left 81 cached pages and no ledger row, which is exactly the designed behaviour.

**The distinction is not pedantry.** "Exited cleanly" implies the run's own record is trustworthy,
and it was the untrustworthy record that this entry exists to fix. Recording the pull as clean is
what let a stale deliverable sit unexamined.

## 4. The resume cost is ~70,000 calls and ~7.8 hours

`step4_progress.json` reports `projected_hours_remaining: 4.28`. **That number is wrong by roughly
1.8× and should not be used to price a resume.**

**Two structural faults**, both in `write_progress()`:

1. **It was computed from 8 users over 100 seconds**, of which 123 pages were served from cache and
   were therefore free. A rate measured over a sample that small, and partly over free work, is not
   a rate.
2. **It is user-count based.** Under `decisions/0009`'s stratified round-robin the untouched users
   are systematically **the heavier half of every bin**, which a users-per-hour figure cannot see.
   Observed mean pages per user: **43.3** across the first 2,372, **50.5** across the next 464, and
   **~58** implied for the remaining 1,214.

**Restated cost: ~70,000 live calls, ~7.8 hours** at the 150/min throttle, which
`logs/throttle/budget.json` confirms is the binding constraint — its stamp ring shows a repeating
60-second cycle of ~150 calls in a 14–18 second burst followed by a ~42 second wait.

**Settled exactly, at zero API calls**, by summing `forecast_pages` over `processed/step4/pull_order.jsonl`
rows with `pull_rank >= 2836`. That sum has not been computed and the figure above remains an
estimate.

**Projected outcome if resumed:** the discard rate shows no monotone trend across bins spanning
forecasts of 1 to 292 pages, so ~10% is safe planning for the remainder and a completed pull would
reach **~3,640 of 4,050, about 89.9%**.

## 5. What this entry does not do

- **It does not resume the pull.** Whether to resume is the Human Lead's, and the hazards the review
  raised — an exclude file with no expiry, disk unmeasured anywhere, and a 27-hour Sabbath window a
  7.8-hour run does not fit before a Friday-evening start — are unaddressed.
- **It changes no number in the study.** The cohort is 2,549 users, the frame 1,138 shows, the
  analysis population 201,900 pairs. Only the published record of how they were obtained changed.
- **It does not correct the two remaining record defects**, which are carried to Step 14 instead —
  the call ledger's 246-call under-count and the failure log's 14 duplicate rows. Both are recorded
  as limitations rather than fixed, because both are provenance defects rather than data defects and
  neither moves a result.

## 6. What the review passed, and it should be on the record

The engineering verdict on the pull itself was **PASS**, and the failure profile is the strongest
operational evidence this study has:

- **Zero 429s and zero 403s across the entire project.** No 401/404, no pagination drift.
- **3 transient events in 126,391 requests — 24 ppm** — being 2 HTTP 500s on one user and 1 read
  timeout, all recovered on the first retry with ~2.4 s backoff.
- **Zero unrecovered errors.** The 7 short reads were all recovered.
- The Step 0 contract held under 126,391 live requests: throttle correct and binding, retry correct,
  resume correct, nothing re-requested, no silent drops.
