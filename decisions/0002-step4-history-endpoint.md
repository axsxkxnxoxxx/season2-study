# Decision 0002 — Step 4 source endpoint

| | |
| :--- | :--- |
| **Decision** | The watch-history source is **`GET /users/:id/history`, unfiltered, one sweep per user** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-10 |
| **Closes** | The blocking finding in `artifacts/step0-access-and-setup.md` §0, listed as open item 1 in §6 |
| **Recorded as** | D15 in `artifacts/step1-outcome-definition.md` §10.0; §0 of the same document |
| **Status** | Closed. Step 4 is unblocked on this item. |

---

## What was rejected, and why

The original Step 0 design was **one call per user** to `/users/:id/watched/shows`, on the
premise that it returns the full watched library with per-episode timestamps. The Analytics
Engineer probed it and **both halves of the premise were wrong**:

1. **It paginates**, and `limit` is silently clamped at 250. A request for `limit=1000` returned
   `X-Pagination-Limit: 250`.
2. **It carries no per-episode timestamps at all.** Four parameter variants were tried — none,
   `extended=full`, `limit=1`, `limit=1000` — and every record returned the same five keys:
   `plays`, `last_watched_at`, `last_updated_at`, `reset_at`, `show`. No `seasons` key, no
   `episodes` key. For a third-party public profile under Client-ID-only auth the endpoint
   returns a **show-level aggregate**.

That is disqualifying rather than inconvenient. Step 1 defines S1 completion as the S1 finale
plus 90 percent of S1 episodes, the abandonment point as the highest S2 episode watched, and
requires counting **distinct episodes** rather than play events. None of it is computable from a
per-show play count. A single `last_watched_at` also cannot separate an S1 completion date from
an S2 start date, which is what the clock start is built from — and being the *most recent*
watch, it is precisely the timestamp class Step 5 exists to distrust.

The Analytics Engineer stopped and reported rather than substituting an endpoint. Correct: this
is a design decision.

## What the decision fixes

- **Unfiltered.** The endpoint mixes `type: episode` with `type: movie`, and Step 7 liveness
  draws on the whole sweep as **account-wide evidence**. Filtering server-side would destroy the
  liveness input. Outcome measurement uses only `type: episode` records for the show in question;
  the filtering happens locally, after the sweep.
- **`action` is retained, not filtered.** Step 5's contamination diagnostics run on it.
- **Per-episode `watched_at` timestamps** — the property `watched/shows` lacked.

## Two conditions travel with it

**1. "One sweep" is one logical pass, NOT one call.** The history endpoint paginates, and more
heavily than `watched/shows` did: a probe profile returned `item_count = 15812` at
`page_count = 1582` with `limit=10`, which is roughly **64 pages at `limit=250` for a single
user**. Step 4 throughput must be estimated in **pages, not users**. The one-call-per-user
assumption that the Step 0 finding disproved for `watched/shows` must not be reintroduced here.

**2. The sweep must be COMPLETE, and this is a correctness requirement rather than a performance
one.** Records return newest-first, so a truncated sweep is **indistinguishable from a genuine
"never started"** and lands directly in the study's headline category. Capping pages at Step 4
would silently manufacture the result. Enforcement is Step 4's and Step 8's; the dependency is
recorded in Step 1 §0 because it is the definition that it breaks.

> **Amended 2026-08-11 — [0012](0012-sweep-completeness-rule.md).** The requirement stands; the
> **test** for it changed. Completeness is full `X-Pagination-Page-Count` coverage plus a residual
> within 2 percent of `X-Pagination-Item-Count`, not exact equality with that header — which the
> Step 4 pilot showed is not an exact count of the records the endpoint returns.

## Files reconciled

`artifacts/step0-access-and-setup.md` §0 and §6, and `artifacts/step1-outcome-definition.md` §0
and §10.0, now agree. The original Step 0 finding is preserved unedited beneath the resolution
box, because it is the warrant for this decision.
