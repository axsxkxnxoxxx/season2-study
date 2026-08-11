# Access probe: the history endpoint, and the two figures Step 1 cites

**Owner:** Analytics Engineer (Step 0 infrastructure) · **Mode:** access probe, not a gate
**Date:** 2026-08-10
**Closes:** a provenance gap. `artifacts/step1-outcome-definition.md` attributes two empirical
figures to "the Step 0 probe" — the duplicate-inflation figure in Section 2.1 and the S1/S2
overlap in Section 5 — and neither appeared in any public Step 0 artifact. This document
records what was pulled, what was computed, and what reproduces.

**This document does not modify, adopt, or interpret Step 1.** Step 1 is an approved gate and is
not edited here. Where a reproduced number differs from the number as printed, the difference is
reported in §6 and left to the Human Lead.

**Result: both figures reproduce from cached responses, at zero live calls.**

---

## 1. Provenance: where the numbers actually came from

Both figures come from **one run and one response**. The run was tagged `step0-history-probe` in
`logs/api_requests.ndjson` on 2026-08-10 at 21:02 UTC. Unlike the other two Step 0 probes it was
committed with no script and no run record, which is why the figures were cited but not
reproducible. This document and `src/step0_history_probe.py` are the retrospective record.

The run made **two** GETs, both HTTP 200 on the Client ID alone with no OAuth:

| # | Call | Status | Purpose |
| :--- | :--- | :--- | :--- |
| 1 | `GET /users/:id/history/shows/:show_id?limit=250&page=1` | **200** | one user, one show, complete play history |
| 2 | `GET /users/:id/history?limit=10&page=1` | **200** | unfiltered shape and pagination headers |

No 403. No 429. No 5xx. No transport errors. `X-Ratelimit` absent on both, `Retry-After` absent
on both, which matches the Step 0 finding that Trakt emits `X-Ratelimit` on a 429 only. The
original run spent 2 calls against a 150/min throttle and a 200/min ceiling.

**Both cited figures are computed from call 1 alone.** Call 2 contributes only the pagination
figure in §5. There is no second source run to find.

**Subject.** One public profile, described neutrally throughout: a heavy user, roughly 15,800
total history items. One show: a single long-running scripted drama with more than two seasons,
watched to completion, with rewatching. The profile is not named, the show is not named, and no
watch dates or episode-level listings appear in this document. That material stays in
`logs/step0_history_probe.json` and `raw/`, which never leave the machine.

**n = 1.** Everything below is one profile and one show. See §7.

---

## 2. Section 2.1, duplicate inflation: **reproduces exactly**

Dedup key `(season, number)`, scoped to the one show, which is the show-scoped form of the
Section 2.1 key `(show.ids.trakt, season, number)`.

| Quantity | Value |
| :--- | :--- |
| Play records returned | **123** |
| Distinct `(season, number)` pairs | **96** |
| Surplus records | **27** |
| Inflation, records ÷ distinct | **1.28125**, i.e. **28.125 %** |
| Episodes appearing in more than one record | **25** |
| Records for the most-duplicated episode | 3 |
| Multiplicity distribution | 71 episodes at ×1, 23 at ×2, 2 at ×3 |
| Distinct history record `id`s | 123, i.e. every record is a distinct event, not a paging artifact |
| Record `action` values | 121 `scrobble`, 1 `watch`, 1 `checkin` |

**Rule this supports:** Section 2.1, count distinct episodes and never play events. A play-event
count would overstate this profile's progress through this show by 28 %, which is enough to move
a user across the 90 % S1 completion threshold in Section 4 on its own.

**Two readings worth stating, because both are easy to get wrong.**

- **27 surplus records, 25 duplicated episodes.** These are not the same number and both are
  correct. Two episodes appear three times, so 25 distinct episodes account for 27 extra records.
- **The 96 is derived from the user's history, not from show metadata.** The show's own
  `aired_episodes` field also reads 96 on this payload. That is a coincidence of a completionist
  profile, not the source of the figure. Section 2.1's rule stands independently of it, and
  Section 1 of the definition is explicit that `show.aired_episodes` is not used.

**One check the definition asks for, run here because it was free.** Section 2.1 says
`episode.ids.trakt` is not canonical and may disagree with `(season, number)`. On this payload it
does not disagree: 96 distinct episode Trakt IDs against 96 distinct pairs, and no pair mapping
to more than one ID. The rule is not contradicted; it is simply untested by this profile, and the
disagreement case Section 2.1 provides for was not observed here.

---

## 3. Section 5, the S1/S2 overlap: **reproduces, at 5.90 weeks**

| Quantity | Value |
| :--- | :--- |
| First S2 watch precedes last S1 watch | **yes** |
| Overlap | **41.31 days = 5.90 weeks** |
| S1 play records / distinct S1 episodes | 24 / 12 |
| S2 play records / distinct S2 episodes | 25 / 12 |

"About six weeks" is 41.31 days rounded. The direction and the order of magnitude are exactly as
Section 5 states: on this profile, histories are **not monotonic**.

**Rule this supports:** Section 5, definition **(b)**, first-pass completion, over definition
**(a)**, `max(watched_at)` over S1.

**The figure is stronger than it looks, and the reproduction shows why.** The overlap is computed
over *all* S1 play records, which is definition (a) exactly — the definition Section 5 argues
against. Recomputing the same comparison after the Section 2.2 collapse, one timestamp per
distinct episode and the earliest wins:

| Comparison | Last S1 → first S2 |
| :--- | :--- |
| Definition (a), all S1 play records | first S2 **precedes** last S1 by 41.31 days |
| Section 2.2 collapse, earliest per distinct episode | first S2 **follows** last S1 by 360.73 days |

The overlap is entirely a rewatch artifact. The profile finished S1 once, started S2 about a year
later, and rewatched part of S1 while S2 was in progress. Definition (a) would place this user's
S1 completion date **after** the event it is supposed to precede, and the clock start built on it
in Section 5 would be negative. Definition (b) puts completion where it belongs and the ordering
is restored. That inversion, not the six weeks by itself, is the empirical warrant.

---

## 4. Order of the two rules

The reproduction makes the dependency explicit: the Section 2.2 earliest-timestamp collapse is
what removes the overlap, and the Section 2.1 distinct-episode rule is what makes the collapse
well defined. The counting rules are prior to the S1 completion date, which is how the definition
already orders them. Nothing here proposes a change.

---

## 5. Pagination, the third figure from the same run

Section 1 of the definition quotes "roughly 64 pages per user at `limit=250`" from this same
probe profile. It reproduces: `X-Pagination-Item-Count` reads **15,812** on the unfiltered
history, and 15,812 ÷ 250 = 64 pages. Also observed on call 2, and relevant to Step 4:

- **`/users/:id/history` mixes types.** The first page returned 7 episode records and 3 movie
  records. A `type` filter or a post-filter is required before any episode logic runs.
- **Record shape**, unfiltered: `action`, `episode`, `id`, `show`, `type`, `watched_at`, matching
  what Section 1 of the definition describes.
- **64 pages is one heavy profile, not a mean.** It sizes a worst case for Step 4 throughput. It
  is not an average and should not be multiplied by a user count.

---

## 6. Cited versus reproduced, stated plainly

| Figure | As printed in Step 1 | Reproduced | Verdict |
| :--- | :--- | :--- | :--- |
| Play records | 123 | 123 | exact |
| Distinct `(season, number)` pairs | 96 | 96 | exact |
| Inflation | "28 percent" | 28.125 % | consistent, rounded down |
| Episodes appearing more than once | 25 | 25 | exact |
| S1/S2 overlap | "six weeks" | 5.90 weeks (41.31 days) | consistent, rounded up |
| Pages per user at `limit=250` | "roughly 64" | 64 | exact |

**No figure fails to reproduce, and no figure contradicts the document.** The only gaps are
rounding, in both cases in the direction that makes the printed number rounder rather than
larger. Two notes are for the Human Lead's judgement, not corrections:

1. Section 2.1 prints "28 percent"; the value is 28.125 %.
2. Section 5 prints "six weeks"; the value is 5.90 weeks. The document states it as a flat figure
   rather than an approximation.

Neither changes any rule either sentence supports. **`artifacts/step1-outcome-definition.md` was
not edited.** It is an approved gate artifact and any amendment is the Human Lead's.

---

## 7. Cost accounting, and what this probe does **not** establish

**Cost: zero live calls.** The reproduction ran entirely from `raw/`. Both cache entries were
checked for the client's stale-meta rule *before* any request was issued — the rule that cost the
episode-listing probe an unbudgeted call — and both were found at the current meta schema
version, so neither would be silently re-fetched. The script refuses to run at all if a request
would go live, unless `--allow-live` is passed explicitly. It was not passed. Client counters for
the reproduction: `requests_sent: 0`, `served_from_cache: 2`, `errors: 0`, throttle spend 0.

What this does not establish:

- **n = 1, on both figures.** One profile, one show. These are existence proofs that duplicate
  records and non-monotonic histories are real and material. They are **not rates**. Nothing in
  this document supports "28 % inflation" or "six-week overlaps" as population quantities, and no
  downstream step should read them that way. The share of history that is duplicated or
  backfilled across the user pool is Step 5's question, on Step 3's sample.
- **Nothing about backfill or contamination.** The duplicate records here are ordinary rewatch
  and re-scrobble behaviour on one profile. The TV Time import problem is a different mechanism
  and is Step 5's, which is a gate and has not run.
- **Nothing about `W`, liveness, the filter order, or the frame.** Out of scope.
- **No third-party generalisation of the pagination figure.** See §5.

---

## Reproduce it

```
.venv/bin/python src/step0_history_probe.py <public-username>
```

Zero network calls when the cache is warm; it stops rather than going live if it is not. The
username is an argument and is not hard-coded, retained, or written to `artifacts/`.

| | |
| :--- | :--- |
| Probe script | `src/step0_history_probe.py` |
| Run record | `logs/step0_history_probe.json` |
| Per-call log | `logs/api_requests.ndjson`, run tag `step0-history-probe` |
| Cached bodies | `raw/users/…/history/` |

The Client ID is loaded from `.env` at runtime by the client and appears in no code file, no log,
and no artifact.
