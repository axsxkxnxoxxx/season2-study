# Decision 0010 — Step 4 tail cap: 300 forecast pages, skip whole, never truncate

| | |
| :--- | :--- |
| **Decision** | A user whose `step4_pages_forecast` exceeds **300** is **skipped entirely** and logged. A user whose **actual** page count exceeds 300 mid-sweep has its partial pages **discarded** and is logged as skipped. **Never truncated, in either case.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Applies to** | Step 4, before launch |
| **Status** | Closed |

---

## The original framing was wrong on its central number, and it is worth recording why

**The Human Lead's brief justified the cap as protection against a single slow user:** *"A 907-page
user is roughly six hours alone."*

**At 150 GET/minute, a 907-call user is 6.0 minutes.** The heaviest user in the final pool is
**1,034 pages = 6.9 minutes**. Six hours is the figure you get at **150 calls per hour**, and the
23.4-hour whole-pool estimate is computed at 150/minute — so the two cannot both hold. 210,500 calls
at 150/hour would be 58 days.

**Consequence: no single user can stall the run**, and the rationale in the original framing does not
support a cap. The decision survives on different grounds, below. This is recorded rather than
quietly corrected because a cap defended by the wrong argument is a cap nobody can re-derive later —
and the wrong argument would have pointed at a much more aggressive threshold.

## The justification that does hold: a circuit breaker on forecast error

`step4_pages_forecast` is derived from `total_plays`, a field **absent from 77 percent of cached
`users/:id/stats` bodies**. That gap already put a **2.4× error** into a published Step 4 estimate
(~86,000 calls against a true ~210,500) before it was caught.

So the forecast is not trustworthy at the individual level, and **a user whose true page count far
exceeds its forecast is entirely plausible.** The cap bounds what a wrong forecast can cost. It is
protection against **the estimate**, not against the users — which is why it must apply to *actual*
pages as well as forecast ones, and why the threshold is set for negligible exclusion rather than for
maximum time saved.

## Why 300

| Cap | Users excluded | Share of pool | Hours saved | Worst user |
| ---: | ---: | ---: | ---: | ---: |
| 150 | 206 | 5.04% | 5.4 | 1.0 min |
| 200 | 101 | 2.47% | 3.4 | 1.3 min |
| 250 | 61 | 1.49% | 2.4 | 1.7 min |
| **300 (adopted)** | **38** | **0.93%** | **1.7** | **2.0 min** |
| 400 | 7 | 0.17% | 0.5 | 2.7 min |

300 sits just above p99 (289). It excludes **under 1 percent of the pool**, keeps **92.8 percent of
the pages**, and bounds any single user at 2.0 minutes against a 6.9-minute observed worst case.

**Why not lower.** Below 250 the exclusion stops being negligible. At 150 it removes 5 percent of
users, **all of them from the heavy end**, which is a real change in the pool's composition bought
for 5.4 hours. Under the circuit-breaker rationale — as opposed to the withdrawn
single-slow-user one — buying hours is not what the cap is for.

## The rule has two halves and needs both

**(a) Forecast cap — skip before pulling.** `step4_pages_forecast > 300` → the user is never started,
and is logged with its forecast.

**(b) Actual-pages guard — discard, never truncate.** If actual pages exceed 300 mid-sweep, **discard
the pages already read** and log the user as skipped.

**Half (b) is what makes the decision coherent.** Without it, the rule fails precisely on the
mis-forecast users it exists to catch, and leaves a truncated sweep behind. Per
`artifacts/step1-outcome-definition.md` §0, **a truncated sweep is indistinguishable from a genuine
"never started" and lands directly in the study's headline category.** The discarded pages remain in
`raw/` for any later resume; only the user's *result* is withheld.

**The machinery already exists.** The mid-sweep 403 handling built for
[0004](0004-403-handling.md) discards partial pages and raises rather than returning an incomplete
sweep. The tail guard reuses that path.

## Skipped-for-length must stay distinguishable downstream

Explicitly required by the Human Lead: **the same treatment `access_denied` gets.** A skipped user is
not a user with no history, and must never be readable as one.

That means a distinct outcome value — not folded into `unavailable`, not folded into
`access_denied`, and not represented by an empty result. Step 8 must be able to separate *skipped for
length* from *pulled and genuinely never started*, because conflating them puts a fabricated row in
the headline.

## Direction on the headline

**Upward.** Excluded users are the heaviest trackers, who are more likely to have continued into S2,
more likely to log completely, and more likely to survive the Step 7 liveness filter. Removing them
removes disproportionately many *Continued* rows and raises the never-started share.

**This runs opposite to the biases already on the record.** The seeding bias
([0008](0008-step3-seed-source.md)) and the liveness exclusion both push the headline **down**; this
pushes it **up**, so it partially offsets rather than compounding. At 0.93 percent the magnitude is
negligible either way — but the direction is named here because every other exclusion in this study
is, and because at a cap of 150 it would not have been negligible.

**Required outputs:** the count of users skipped by the forecast cap; the count skipped by the
actual-pages guard, reported **separately**, since that second number is the direct measure of how
wrong `step4_pages_forecast` is; their total forecast pages; and the direction named alongside.
