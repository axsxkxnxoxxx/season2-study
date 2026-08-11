# Decision 0012 — Sweep completeness is judged by `page_count`, with a 2% residual tolerance

| | |
| :--- | :--- |
| **Decision** | A sweep is complete when **every page reported by `X-Pagination-Page-Count` has been read**, and the residual between accumulated records and `X-Pagination-Item-Count` is **within 2%**. Exact equality with the item-count header is no longer required. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Amends** | [0002](0002-step4-history-endpoint.md) condition 2, and `artifacts/step1-outcome-definition.md` §0 |
| **Status** | Closed |

> **This changes a rule inside an approved gate artifact.** Step 1 was approved on 2026-08-10 and its
> approval record states that a future edit changing a *rule* reopens the gate. This edit does change
> a rule. It is recorded here as a Human Lead amendment rather than treated as a clarification, and
> **the Human Lead may wish to put it to Red Team** before results are computed. Flagged, not decided.

---

## What the old rule was, and why it existed

`0002` condition 2 and Step 1 §0 both require the sweep to be **complete**, on this reasoning:
records return newest-first, so **a truncated sweep is indistinguishable from a genuine "never
started" and lands directly in the study's headline category.** That reasoning is untouched by this
decision. What changes is only how completeness is *detected*.

The implementation enforced completeness by requiring accumulated records to equal
`X-Pagination-Item-Count` exactly.

## Why exact equality is the wrong test for this endpoint

The Step 4 pilot pulled 10 users across all ten strata, 387 calls, every response HTTP 200.
**Seven of ten failed the exact-equality test.** Residuals: −1, −5, −26, −97, −32, −12 and **+20**.

**It is not truncation**, on two independent proofs:

1. **The history was not moving underneath the pull.** `X-Pagination-Page-Count` and
   `X-Pagination-Item-Count` were identical on **every page** of every sweep, including one of 105
   pages. A history growing mid-sweep would show them drift.
2. **Two different page sizes returned the same records.** Re-sweeping one user at `limit=100` (15
   pages) returned the **identical record set in identical order** as the cached `limit=250` sweep
   (6 pages) — **1,459 distinct records both ways**, while both reported 1,460. Both sweeps are on
   disk and the comparison is reproducible at zero API cost.

`X-Pagination-Item-Count` is therefore not an exact count of the records this endpoint returns. A
rule keying on it rejects healthy sweeps, and under it the study would discard roughly 70 percent of
its pool for a header discrepancy.

Replaying the same cached pages under the adopted rule takes the pilot from **3 complete to 10
complete**, 12,126 → 95,167 records, with a maximum residual of **0.86 percent** against the 2
percent tolerance.

## The three behaviours must be counted separately, not absorbed

**Explicitly required by the Human Lead: the tolerance must not silently collapse three different
things into one number.** Each is classified and counted on its own in the run report:

| Behaviour | What it is | Status for this study |
| :--- | :--- | :--- |
| **Header over-count** | Accumulated < `item_count`. The header claims more records than the endpoint returns | **Benign.** An artifact of Trakt's counting, not missing data — proved by the two-page-size comparison |
| **Header under-count** | Accumulated > `item_count`. Observed at **+20** on one pilot user | **Benign** for the same reason, and in the safe direction: more data than advertised, not less |
| **Genuine cross-page duplicate records** | The same record `id` returned on more than one page. Observed at **5 duplicates in 14,236 records** on one pilot user | **Real data behaviour, not a header artifact.** Handled downstream by distinct-episode counting (Step 1 §2.2), but it is a property of the API that must be **visible as its own number rather than absorbed into a tolerance** |

The third is the one the tolerance would otherwise hide. It is already handled — Step 1 counts
distinct episodes rather than play events, and that rule exists precisely so duplicate records cannot
inflate anything — but "already handled downstream" is not a reason to stop measuring it.

## Users outside the tolerance

**Discarded, logged, and never truncated.** A user whose residual exceeds 2 percent has its pages
discarded rather than returned as data, exactly as a mid-sweep 403 does under
[0004](0004-403-handling.md) and an over-length sweep does under
[0010](0010-step4-tail-cap.md).

**It must remain distinguishable downstream in the same way `access_denied` is** — a distinct
outcome, never folded into `unavailable`, never folded into any skip category, and never represented
by an empty result. All of these outcomes can carry zero episodes; only `complete` means the user
watched nothing.

## Required outputs

- Counts of **header over-count**, **header under-count**, and **cross-page duplicate records**,
  reported **separately**, with the duplicate count given as both affected users and affected records.
- The residual distribution across the pool, so the 2 percent tolerance can be judged against what
  was actually observed rather than against the pilot's ten users.
- The count of users discarded for exceeding the tolerance, reported separately from every other
  skip and failure category.

## What this decision does not change

The completeness *requirement* stands: a partial sweep is never returned as data, and page reading is
never capped for any reason other than [0010](0010-step4-tail-cap.md). Only the test for whether a
sweep is complete has changed, from an exact header match to full page coverage plus a bounded
residual.
