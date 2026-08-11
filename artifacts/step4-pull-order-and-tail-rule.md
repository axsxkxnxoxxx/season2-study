# Step 4: pull order and tail rule — proposal

**Prepared for:** Human Lead, before Step 4 launches
**Status:** **Proposal. Neither decision is recorded in `decisions/` yet**, because both premises
changed under checking and the ruling is yours.
**Basis:** 4,088 usable users, 210,500 forecast pages, 23.4 hours at the 150 GET/minute throttle.

Two corrections come first, because each changes what the decision should be.

---

## Correction 1 — the tail is not six hours. It is seven minutes.

The brief states *"a 907-page user is roughly six hours alone."* At the study's throttle of
**150 GET/minute**, a 907-call user is **6.0 minutes**. The heaviest user in the final pool is
**1,034 pages = 6.9 minutes**.

Six hours is what you get from **150 calls per hour**. The 23.4-hour whole-pool figure is computed
at 150/minute and is correct, so the two cannot both be right — 210,500 calls at 150/hour would be
58 days.

**Consequence: no single user can stall the run.** The worst case in the pool is under seven
minutes. The tail rule cannot be justified as protection against one user eating the window,
because that risk does not exist. It can still be justified — on different grounds, set out in
Decision 2 below — but the grounds change, and so does the right cap.

## Correction 2 — median-out does not produce a representative sample

The stated goal is that an early stop *"leave a representative sample rather than an arbitrary
slice."* Median-out does not do that. It leaves a **centered** slice, which is a different thing.

Simulated against the real distribution, at a 10-hour cut-off:

| Order | Users pulled | Mean pages | p95 seen | **Heaviest user seen** |
| :--- | ---: | ---: | ---: | ---: |
| **Median-out** | 2,349 | 38.3 | 67 | **73** |
| Stratified round-robin | 2,069 | 43.5 | 126 | **151** |
| Ascending (worst case) | 3,132 | 28.7 | 62 | 68 |
| **The pool itself** | 4,088 | **51.5** | **151** | **1,034** |

**After ten hours, median-out has not pulled a single user above 73 pages** — in a pool that reaches
1,034. It works outward symmetrically in rank, so it truncates *both* tails at once, and it does so
on the exact axis that matters: page count is a proxy for tracking intensity, which is a proxy for
the outcome. A sample containing no heavy trackers is not representative of a population that
contains them.

Median-out does deliver what it was reaching for — it beats ascending order, it is deterministic and
reproducible, and it front-loads cheaper-than-mean users so more users land per hour. The flaw is
only in the tails, and it is fixable without giving any of that up.

**Recommended amendment: stratified round-robin.** Sort by forecast pages, cut into ten equal-count
bins, then take one user from each bin in turn. Deterministic, reproducible, and **every prefix is
proportional across the whole distribution including both tails**. The cost is real and small: 2,069
users at ten hours against median-out's 2,349, because it spends some of the window on heavy users
rather than avoiding them. That is the point — those users are the sample's evidence about the heavy
end.

---

## Decision 1 — pull order

**As instructed:** sort by corrected forecast page count, pull median first, work outward.
**Recommended instead:** stratified round-robin over ten equal-count bins.

Both are deterministic and both beat an arbitrary slice. The difference appears only if the run
stops early — which is the case the decision exists for.

| | Median-out | Stratified |
| :--- | :--- | :--- |
| Prefix is unbiased on page count | Approximately, in rank | **Yes, by construction** |
| Prefix contains heavy users | **No** | Yes, proportionally |
| Users per hour early | Higher | ~12% lower |
| Deterministic / reproducible | Yes | Yes |

**Ruling needed.** If the study will report on whatever fraction completes, take stratified. If the
run is expected to finish the pool, the orders converge and median-out's throughput edge wins.

---

## Decision 2 — tail rule

**Recommended cap: 300 forecast pages, skip-not-truncate.**

| Cap | Users excluded | Share of pool | Hours saved | Worst user |
| ---: | ---: | ---: | ---: | ---: |
| 150 | 206 | 5.04% | 5.4 | 1.0 min |
| 200 | 101 | 2.47% | 3.4 | 1.3 min |
| 250 | 61 | 1.49% | 2.4 | 1.7 min |
| **300** | **38** | **0.93%** | **1.7** | **2.0 min** |
| 400 | 7 | 0.17% | 0.5 | 2.7 min |

### Why 300, given the tail is only seven minutes

The cap is no longer a defence against a single slow user. Its remaining justification is **a
circuit breaker on forecast error**, and that one is sound.

The forecast is derived from `total_plays`, a field **absent from 77 percent of cached stats
bodies** — a bug that already put a 2.4× error into the published Step 4 estimate. A user whose true
page count is far above forecast is entirely possible, and the cap bounds what a wrong forecast can
cost. At 300 that bound is 2.0 minutes per user against a 6.9-minute observed worst case.

300 also sits just above p99 (289), so it excludes **under 1 percent of the pool** and keeps
**92.8 percent of the pages**. Below 250 the exclusion stops being negligible: at 150 it removes
5 percent of users, all of them the heaviest trackers, which is a real composition change bought for
5.4 hours.

### The rule needs two halves, not one

**(a) Forecast cap — skip before pulling.** Any user with `step4_pages_forecast > 300` is skipped
whole, never started, and logged with its forecast.

**(b) Actual-pages guard — discard, never truncate.** If a user's *actual* page count exceeds 300
mid-sweep, **discard the pages already read and log the user as skipped.** Without this half, (a)
fails exactly when it matters — on the mis-forecast users it exists to catch — and leaves a
truncated sweep, which per Step 1 §0 is indistinguishable from a genuine "never started" and lands
in the headline.

**The machinery already exists.** The mid-sweep 403 handling built for decision `0004` discards
partial pages and raises rather than returning an incomplete sweep. The tail guard should reuse that
path, and skipped-for-length users must be as distinguishable downstream as `access_denied` users
are — a distinct outcome, never folded into "no history."

### Direction on the headline

**Upward.** Excluded users are the heaviest trackers. Heavy trackers are more likely to have
continued into S2, more likely to log completely, and more likely to survive the Step 7 liveness
filter — so removing them removes disproportionately many *Continued* rows and raises the
never-started share.

**This runs opposite to the two biases already on the record.** The seeding bias
([0008](../decisions/0008-step3-seed-source.md)) and the liveness exclusion both push the headline
*down*; this pushes it *up*, so it partially offsets rather than compounding. At 0.93 percent the
magnitude is negligible in either direction. **At a cap of 150 it would not be** — 5 percent of the
heaviest users is a composition change worth reporting, which is the strongest argument against the
aggressive cap.

**Required output either way:** the count of users skipped for length, their total forecast pages,
and the direction named — the same treatment every other exclusion in this study gets.

---

## What I am not doing

Not recording either decision in `decisions/`, not modifying the pool, and not launching Step 4.
Decision 1 needs your ruling between the instructed order and the recommended amendment; Decision 2
was a proposal by construction and the six-hour correction changes its rationale.
