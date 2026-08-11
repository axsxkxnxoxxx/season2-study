# Access probe: the episode-listing endpoint

**Owner:** Analytics Engineer (Step 0 infrastructure) · **Mode:** access probe, not a gate
**Date:** 2026-08-10
**Closes:** the open precondition in `artifacts/step1-outcome-definition.md` Section 3.3 —
whether a listed episode-number set `E` is obtainable on the Client ID alone.

**This document does not modify, adopt, or interpret Step 1.** Step 1 is an unapproved gate.
It reports what the API returned. Whether `E` becomes a Step 2 field or a separate pull remains
the Human Lead's call, per Section 3.3 and Section 11.

**Result: the precondition is met. The Section 3.3 fallback is not required.**

---

## 1. What was asked and what was called

Section 3.3 names two variants. Both were called live, on one third-party show
(`breaking-bad`), with the Client ID alone and no OAuth. Nothing was iterated.

| # | Call | Status | Network |
| :--- | :--- | :--- | :--- |
| 1 | `GET /shows/:id/seasons/1` (variant A, no `extended`) | **200** | live |
| 2 | `GET /shows/:id/seasons?extended=episodes` (variant B) | **200** | live |
| 3 | `GET /shows/:id/seasons?extended=episodes,full` (variant B + counts) | **200** | live |
| 4 | `GET /shows/:id/seasons/2/episodes?extended=full` | **200** | re-fetched, see §6 |

Call 3 is not a third variant. Section 3.4 requires flagging shows where `episode_count`,
`aired_episodes` and `|E|` disagree, and that is only checkable if the season-level counts and
the episode list arrive in one payload. Call 3 tests whether they do.

No 403. No 429. No 5xx. No transport errors. `X-Ratelimit` was absent on every response, which
matches Step 0: Trakt emits it on a 429 only. `Retry-After` absent throughout. Peak spend during
the probe was 4 calls in the 60-second window against a 150 cap and a 200 ceiling.

Run record: `logs/step1_episode_listing_probe.json`. Per-call log: `logs/api_requests.ndjson`.
Bodies: `raw/shows/breaking-bad/seasons/`. Probe script: `src/step1_episode_listing_probe.py`.

---

## 2. Does authentication hold on Client ID alone

**Yes. HTTP 200 on all four calls with `trakt-api-key` only and no OAuth token.** The
episode-listing endpoints behave as OAuth Optional on public show metadata, the same as the
endpoints settled at Step 0.

## 3. Is `E` derivable, and are `L` and `F` from the same payload

**Yes to both, on both variants.**

Every episode object carries an integer `number` and an integer `season`. Under variant A the
episode object is `{ids, number, season, title}`; under variant B it is the same minimal shape
nested in an `episodes` array on each season object. So `E` is read directly, `L := |E|` and
`F := max(E)` are computed from that one list, and Section 3.3's "they cannot disagree with each
other" requirement is satisfied structurally, not by a cross-check.

Observed on the probe show, all three variants agreeing exactly:

| Season | `E` | `L = |E|` | `F = max(E)` |
| :--- | :--- | :--- | :--- |
| 1 | 1–7 | 7 | 7 |
| 2 | 1–13 | 13 | 13 |

Zero records with a missing or non-integer `number`, zero duplicate numbers within a payload,
zero episodes whose `season` field disagreed with the season they were returned under.

## 4. Which variant to use

**Variant B with `extended=episodes,full`: `GET /shows/:id/seasons?extended=episodes,full`.**

| | Variant A `/seasons/:season` | Variant B `?extended=episodes` | Variant B `?extended=episodes,full` |
| :--- | :--- | :--- | :--- |
| Calls per show for S1 **and** S2 | **2** | **1** | **1** |
| Per-episode `number` | yes | yes | yes |
| Season-level `episode_count` / `aired_episodes` | not requested | **absent** | **present** |
| Episode-level `first_aired` | no | no | yes |
| Body size, probe show | 1.1 KB per season | 12 KB all seasons | 62 KB all seasons |

Three reasons for B-with-full:

1. **Call count is the constrained resource, not bytes.** The rate limit is 1000 GET per 5
   minutes. Variant A doubles the call cost of the show frame for no additional information.
2. **It is the only variant that supports the Section 3.4 disagreement check.**
   `extended=episodes` alone returns season objects of `{ids, number, episodes}` — no
   `episode_count`, no `aired_episodes` — so a show whose counts disagree with `|E|` could not be
   flagged from that payload without a second call, which reintroduces the two-source problem
   Section 3 exists to remove.
3. **One payload covers both seasons plus the cross-check**, so `E1`, `L1`, `F1`, `E2`, `L2`,
   `F2` and the flag all come from a single show, single pull, as Section 3.3 requires.

## 5. Implementation notes that affect how `E` is built

- **No pagination anywhere.** No `X-Pagination-*` header was returned on any variant. These
  endpoints return one complete body. A paginated fetch helper that requires those headers will
  raise on them; the plain single GET is correct.
- **Season 0 is returned and must be filtered.** `?extended=episodes` returned six seasons,
  numbered 0 through 5, with Specials as season 0 carrying a full ten-episode list. Section 3.1
  excludes specials, so `E` is built after dropping `number == 0` at the season level. Nothing in
  the payload marks it as special other than the season number.
- **`|E|` tracks the *listed* set, which can exceed the *aired* set.** On the probe show, season
  0 returned `episode_count = 10`, `aired_episodes = 8`, and `|E| = 10`: two listed-but-unaired
  specials are in the list. Seasons 1 through 5 had all three equal. This is exactly the Section
  3.4 case and it is real, not hypothetical. The frame requires S2 to have finished airing on or
  before 31 Dec 2024, so `episode_count == aired_episodes == |E|` should hold for in-frame S1 and
  S2; the check should still be run and counted, because it is now cheap.
- **`extended=episodes` without `full` gives a minimal episode object.** Sufficient for `E`, `L`
  and `F`, and nothing else. If only the set is wanted, it is a fifth the size.
- **Episode-level `first_aired` arrives with `full`**, on the same payload as `E`. Recorded as an
  observation only. Whether the show frame sources air dates there is Step 2's, which is the
  Human Lead's.

## 6. Cost accounting, stated plainly

The probe was budgeted at three network calls and spent four. `raw/shows/breaking-bad/seasons/2/
episodes` was already on disk from Step 0 and was requested expecting a free cache hit; the
client refused to serve it because its cache record predates the current meta schema version, and
re-fetched. That is the client's documented stale-entry behaviour working as written, not a
discipline breach, and the overshoot is one call. It is recorded here rather than rounded off.

## 7. What this probe does **not** establish

- **One show, contiguous numbering.** Breaking Bad has no numbering gap, so the probe confirms
  the *shape and the auth*, not that a gapped season is represented the way Section 3 assumes.
  The gap machinery remains untested against a real gap. Sizing that is a frame-wide count, not
  an access question, and it belongs wherever `E` is first pulled at scale.
- **Absent or out-of-range seasons were not requested.** A show with no season 2, or a season
  index that does not exist, was not probed; that costs calls and is a data question, not an auth
  question. Under variant B it does not arise as a separate request in any case — a missing
  season is simply absent from the returned list.
- **Nothing about `W`, liveness, contamination, or the filter order.** Out of scope.
