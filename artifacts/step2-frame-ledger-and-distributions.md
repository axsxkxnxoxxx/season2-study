# Step 2 frame — exclusion ledger, field inventory, and distributions

**Owner:** Human Lead. **Executed by agent** under `decisions/0013`, which delegates Step 2
*execution* only. Every selection rule below was written by the Human Lead and is applied as
written. **No rule here is the agent's**, and no threshold is proposed.

**Aggregates and counts only.** No usernames, user IDs or individual watch histories. Show titles
and season metadata are public catalogue data. The frame table itself is at
`processed/step2/frame.csv` (git-ignored), as instructed.

| | |
| :--- | :--- |
| Candidate set | 2,094 shows, ≥50 S1 completers on the full pulled pool |
| **Frame** | **1,138 shows**, **220,107** S1-completer pairs |
| API calls | **3,320** — 2,094 on `/shows/:id/seasons?extended=episodes,full`, 1,226 on `/shows/:id?extended=full` |
| Pull result | 3,320 OK, 0 unavailable, 0 errors, 0 429s, 0 retries |
| Peak rate | 150 calls in any rolling 60s window, against a 150 throttle and a 200/min ceiling |
| Rebuild cost | **0 calls** — all bodies cached under `raw/` |

**Human Lead decisions carried in this frame**, all 2026-08-12: the 12 unaired-S2 shows are excluded
([0015](../decisions/0015-step2-unaired-s2-exclusion.md)); per-season network is dropped as a field
([0016](../decisions/0016-per-season-network-dropped.md)); air period is defined
([0017](../decisions/0017-air-period-definition.md)); the size quintile is cut over the frame
([0018](../decisions/0018-size-quintile-base.md)); `pool_completers` is recomputed on real season
lengths ([0019](../decisions/0019-pool-completers-recomputed.md)); and the **structural thresholds
are set** ([0020](../decisions/0020-step2-structural-thresholds.md)), closing
[0014](../decisions/0014-no-content-filters-structural-fields.md).

---

## 1. What was called, and the rate discipline

Two passes, both one call per show, both resumable and both fully cached:

1. **Seasons** — `GET /shows/:id/seasons?extended=episodes,full`, 2,094 calls, one per candidate.
   Supplies real `E1`, `L1`, `F1`, `E2`, `L2`, `F2` and every air date.
2. **Show metadata** — `GET /shows/:id?extended=full`, 1,226 calls, on the shows that survived the
   date rules. The 868 candidates already excluded were not fetched.

Rate compliance was verified against the persisted throttle ring rather than asserted: the maximum
number of requests in **any** rolling 60-second window was **150**, exactly the configured throttle
and 50 below Trakt's documented 200/min ceiling. The run's own `shows_per_min` counter read as high
as 318 early in the first pass. That is a cumulative-average artifact — the limiter front-loads a
full 150-call window, then blocks ~33 seconds — and **not** a breach. It is recorded here because
the raw counter misleads anyone reading `logs/step2_seasons_progress.json` directly.

Run records: `logs/step2_seasons_run.json`, `logs/step2_shows_run.json`.

---

## 2. Exclusion ledger

Rules in the order the Human Lead wrote them. Season 0 is filtered inside every show rather than
excluding shows, so it is not a ledger step: **878 of the 2,094 candidates carried a season 0**, and
it was dropped from every episode set, length, and date computation.

| # | Rule | Removed | Remaining |
| :-- | :--- | ---: | ---: |
| 0 | **Candidate set:** shows with ≥50 S1 completers, full-pool diagnostic | — | **2,094** |
| 1 | Seasons payload not retrieved (unavailable / error) | **0** | 2,094 |
| 2 | No season 1 in the payload | **0** | 2,094 |
| 3 | **No real season 2** | **796** | 1,298 |
| 4 | **S2 listed but unaired** — no finale air date, `aired_episodes = 0` | **12** | 1,286 |
| 5 | **S2 finale aired after 2025-12-31** | **60** | 1,226 |
| 6 | **Season over 26 episodes (S1 or S2)** | **51** | 1,175 |
| 7 | **Gap over 1,095 days** (S1 finale → S2 premiere) | **37** | **1,138** |
| 8 | Gap not computable | **0** | 1,138 |

Steps 6 and 7 are the structural thresholds set in
[0020](../decisions/0020-step2-structural-thresholds.md). **No minimum season size is applied** —
Step 1 §4's `ceil(0.90 × L1)` already scales to the real per-show length, so a short season needs no
floor. The two rules overlap on exactly **1** show, so applying them in the other order gives the
same frame.

Step 5 applies the cutoff as a half-open UTC instant, `first_aired < 2026-01-01T00:00:00Z`, per Step
1 §2.4 and D13. The finale is `F2 := max(E2)` after season 0 is filtered, per Step 1 §3.1 — a real
episode number from the payload, never a max-observed proxy.

Per-show audit of every rule: `processed/step2/all_candidates_scored.csv` carries all 2,094
candidates with the `exclusion` value that removed each. In-frame rows are exactly those with
`exclusion` empty.

---

## 3. Distributions

All over the final 1,138-show frame, **after** the structural thresholds.

### 3.1 Gap length — S1 finale to S2 premiere, whole UTC calendar days

| Min | p05 | p25 | Median | p75 | p90 | p95 | Max | Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **−155** | 109 | 191 | **315** | 468 | 699 | 833 | **1,085** | 364.9 |

| Bucket | Shows | Share |
| :--- | ---: | ---: |
| negative | 1 | 0.1% |
| 0–89 d | 36 | 3.2% |
| 90–179 d | 225 | 19.8% |
| 180–269 d | 134 | 11.8% |
| 270–364 d | 293 | 25.7% |
| 1–1.5 y | 230 | 20.2% |
| 1.5–2 y | 119 | 10.5% |
| 2–3 y | 100 | 8.8% |
| 3 y+ | **0** | — |

The 3-year cap is visible as the empty tail. The single **negative gap** is retained, no lower bound
having been set: *That's So Raven*, S1 finale 2004-03-06, S2 premiere 2003-10-03 — Trakt's season
boundaries disagreeing with broadcast order, not a computation error.

### 3.2 Season size

| | Min | p25 | Median | p75 | p90 | Max | Mean |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **S1 episodes** | **1** | 8 | **10** | 13 | 22 | **26** | 12.2 |
| **S2 episodes** | **2** | 8 | **10** | 16 | 22 | **26** | 12.9 |

| Episodes | S1 shows | S2 shows |
| :--- | ---: | ---: |
| 1–3 | 13 | 5 |
| 4–6 | 139 | 115 |
| 7–8 | 188 | 187 |
| 9–10 | 298 | 272 |
| 11–13 | 236 | 229 |
| 14–22 | 167 | 222 |
| 23–26 | 97 | 108 |
| 27+ | **0** | **0** |

**The frame retains `L1 = 1` and `L1 = 2`** by decision: no minimum was set. At `L1 = 1` the Step 1
completion rule reduces to "watched the single episode," which is the rule behaving as written.

### 3.3 Cadence bucket, D12

`span := S2 finale − S2 premiere` in whole UTC days; `weekly_span := (L2 − 1) × 7`; buckets
evaluated in order, first match wins.

| Bucket | Definition | Shows | Share |
| :--- | :--- | ---: | ---: |
| **C0** Unclassifiable | `P`, `F_d` or `L2` missing, or `span < 0` | **0** | 0% |
| **C1** All-at-once | `span ≤ 1` | **206** | 18.1% |
| **C2** Weekly | `abs(span − weekly_span) ≤ 3` | **340** | 29.9% |
| **C3** Faster than weekly | `1 < span < weekly_span − 3` | **167** | 14.7% |
| **C4** Slower than weekly | `span > weekly_span + 3` | **425** | 37.3% |

C0 is empty: every in-frame show classified on real dates. S2 span runs min 0, p25 35, median 63,
p75 168, max 875 days.

**D12's required fragility count: 7 shows sit within one day of a bucket boundary, 0.6% of the
frame.** By D12's own test the thresholds are **not load-bearing**, and a Step 13 arm on them is not
indicated on this evidence. (238 sit within three days, but 220 of those are same-day drops whose
distance is exactly 2 by construction — arithmetic, not fragility. The one-day figure is the
meaningful one.)

**C4 fell from 476 to 425 because of the size cap, not because of cadence.** 44 of the 51 shows the
26-episode rule removed were C4. See §3.5.

### 3.4 Air period — calendar year of the S2 finale

| Air period | Shows | Share |
| :--- | ---: | ---: |
| pre-2020 | **757** | 66.5% |
| 2020–2022 | **213** | 18.7% |
| 2023–2025 | **168** | 14.8% |

**Air period and cadence remain strongly confounded** and must not be treated as independent cuts:

| Air period | C1 | C2 | C3 | C4 |
| :--- | ---: | ---: | ---: | ---: |
| pre-2020 | 83 | 248 | 67 | 359 |
| 2020–2022 | 78 | 54 | 41 | 40 |
| 2023–2025 | 45 | 38 | 59 | 26 |

### 3.5 What the thresholds removed, and the cadence tilt

| Rule | Shows | Pairs | Share of pairs |
| :--- | ---: | ---: | ---: |
| Season over 26 episodes | 51 | 5,644 | 2.4% |
| Gap over 1,095 days | 37 | 7,207 | 3.1% |
| **Combined** (1 overlap) | **88** | **12,851** | **5.5%** |

**The size cap is not cadence-neutral.** Of its 51 shows, **44 are C4**, 6 are C3, 1 is C2 and
**none is C1** — a long season stretches the premiere-to-finale span, and D12 classifies on that
span. Recorded in [0020](../decisions/0020-step2-structural-thresholds.md) and repeated here because
it changes how a C4 result may be read:

> C4 is a required Step 9 stratum and it drops from 476 to 425 shows. **A C4 headline must not be
> read as a statement about slow-release shows in general** — the longest-running titles have been
> removed from it. C4 is also where abandonment is most likely to be **exposure-driven** rather than
> preference-driven, since a season taking a year to release gives a viewer more opportunity to
> lapse for reasons unrelated to the show.

### 3.6 Pool completer count, in-frame

| Min | p05 | p25 | Median | p75 | p90 | p95 | Max | Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 53 | 71 | **115** | 232 | 437 | 614 | **1,662** | 193.4 |

---

## 4. `pool_completers`, recomputed on real season lengths

Per [0019](../decisions/0019-pool-completers-recomputed.md), the max-observed proxy is **superseded
and no result may use it.** `pool_completers` is computed by applying the approved Step 1 §4 rule —
`F1 ∈ D1` and `|D1| ≥ ceil(0.90 × L1)`, with `D1` the distinct S1 episodes whose number is a
**member** of the real `E1` — against the real `E1`, `L1 = |E1|` and `F1 = max(E1)`.

**The recompute changes nothing on this frame**: 220,107 pairs either way, 0 shows up, 0 shows down,
0 falling below 50. The reason is direct — **the proxy `L1_hat` equals the real `|E1|` on 1,225 of
the 1,226 shows** that reached this stage, which is what the diagnostic predicted for shows with
≥50 completers. It is **not** a rehabilitation of the proxy generally; it was never trustworthy in
the long tail. `pool_completers_proxy` is retained as a column so the two stay diffable.

**Not re-applied:** the ≥50 candidate rule was applied to the proxy counts and has not been
re-applied to the recomputed ones. Moot here — zero shows fall below 50 — but stated rather than
implied.

---

## 5. Field inventory

### 5.1 Show-level metadata — pulled, and fully populated

`GET /shows/:id?extended=full`. Over the final 1,138-show frame:

| Field | Non-null | Distinct |
| :--- | ---: | ---: |
| `country` (origin) | 1,138 (100%) | — |
| `language` / `languages` | 1,138 (100%) | — |
| `genres` | 1,138 (100%) | — |
| `network` (show level) | 1,138 (100%) | 150 |
| `status` | 1,138 (100%) | 3 |
| `year`, `first_aired`, `aired_episodes` | 1,138 (100%) | — |
| `runtime` | 1,136 (99.8%) | — |
| `certification` | 1,112 (97.7%) | 7 |

- **Country:** us 862, gb 121, jp 60, ca 31, au 9, kr 8, es 7, no 6, and others.
- **Language:** en 1,032, ja 59, es 9, ko 8, and others.
- **Network:** Netflix 177, CBS 56, NBC 56, HBO 51, ABC 50, FOX 47, and 144 more.
- **Status:** ended 672, canceled 326, returning series 140.
- **Top genres:** drama 742, comedy 452, fantasy 329, science-fiction 316, action 286, adventure 262.

**All of these are fields, not filters.** Nothing above removed a show, and no content-category
filter exists per [0014](../decisions/0014-no-content-filters-structural-fields.md). The Japanese
and anime-tagged shows that left the frame were removed by the **26-episode structural cap**, not by
genre or country: jp falls 92 → 60 because long-run series exceed 26 episodes a season.

**"Platform" has no distinct representation.** The show object carries `network` and nothing else
that names a service; there is no separate distributor or platform field.

### 5.2 Per-season network — DROPPED as a field

Per [0016](../decisions/0016-per-season-network-dropped.md). The measurement, over all 2,094 fetched
shows: **47 of 6,645 season objects carry a network, 0.71%**; 2,080 shows have zero distinct
season-level networks, 13 have one, and **1 has two or more**. Columns `s1_network` and `s2_network`
are removed from the frame table; the counts are retained in `frame-summary.json`.

**The limitation, as `decisions/0014` requires.** Per-season platform is not measurable from this
API. **Platform fragmentation is not a variable in this study** — no result may control for it,
stratify on it, or rule it out. The single show with two distinct season networks is a count
consistent with noise and is **not** read as fragmentation.

**The show-level `network` carries the second, unresolved problem.** It records *today's* network,
so a title that moved services between seasons shows only its current one. **`show_network` must not
be used as a release-time availability measure.** Descriptive field only.

### 5.3 Dates

S1 premiere, S1 finale, S2 premiere, S2 finale and both season-level `first_aired` values are
**100% non-null across the frame.** Premiere is the `first_aired` of the episode numbered `min(E)`,
finale that of `max(E)`. Season-level `first_aired` is recorded but unused, so the two can be diffed
without a refetch.

---

## 6. Metadata integrity checks (Step 1 §3.4, required)

| Check | In-frame shows |
| :--- | ---: |
| S1 `episode_count` / `aired_episodes` / `|E1|` disagree | **0** |
| S2 `episode_count` / `aired_episodes` / `|E2|` disagree | **0** |
| S2 `aired_episodes < |E2|` — where **Continued** may be unreachable | **0** |
| S1 `aired_episodes < |E1|` | **0** |

**All three agree on every in-frame show for both seasons.** The listed-but-unaired hazard §3.4
raised does not reach this frame — the 31 Dec 2025 cutoff removed it, the mechanism §3.4 predicted
but explicitly declined to assume. Verified rather than expected.

### Episode numbering

| | In-frame shows |
| :--- | ---: |
| E1 has an internal gap | **1** (Star Trek: Prodigy — 19 episodes numbered to 20) |
| E2 has an internal gap | 0 |
| E1 does not start at episode 1 | 0 |
| E2 does not start at episode 1 | **0** |

**The four absolute-numbering shows are no longer in the frame.** *Naruto*, *Naruto Shippūden*,
*One Piece* and *Hunter x Hunter* were all removed by the 26-episode cap. The finding they produced
still stands as evidence and is recorded here so it is not lost: their histories used the **same**
absolute numbers as the metadata, 100% overlap on all four (21/21, 16/16, 52/52, 74/74), so Step 1
§4's **set-membership** form handles that shape correctly, whereas the **withdrawn `1..F` range
form would have failed on all four**, scoring every S2 episode out of range.

The Step 1 §3.3 gap hypothesis remains near-untested: one in-frame show has an internal S1 gap and
none has an internal S2 gap.

---

## 7. Size quintile

Cut over the frame per [0018](../decisions/0018-size-quintile-base.md), on the recomputed
`pool_completers`. Single column, `size_quintile`.

| Q1 | Q2 | Q3 | Q4 | Q5 |
| ---: | ---: | ---: | ---: | ---: |
| 238 | 221 | 224 | 227 | 228 |

---

## 8. Frame contents

`processed/step2/frame.csv`, 1,138 rows. Every column is a **field, not a filter** — nothing below
was used to include or exclude a show except the ledger rules in §2.

**Identity and size:** `show_trakt_id`, `title`, `show_year`, `pool_completers`,
`pool_completers_proxy`, `size_quintile`.
**Season structure:** `s1_L`, `s1_F`, `s1_E`, `s2_L`, `s2_F`, `s2_E`, reported `episode_count` and
`aired_episodes` for both seasons, `s1_total_runtime`, `s2_total_runtime`, `seasons_returned`,
`season_numbers`, `max_season_number`.
**Dates and release shape:** `s1_premiere_date`, `s1_finale_date`, `s2_premiere_date`,
`s2_finale_date`, both season-level `first_aired`, `s2_finale_year`, `air_period`, `gap_days`,
`s2_span_days`, `s2_weekly_span_days`, `cadence_bucket`, `cadence_boundary_distance_days`.
**Show metadata:** `show_country`, `show_language`, `show_languages`, `show_genres`, `show_network`,
`show_status`, `show_runtime`, `show_certification`, `show_aired_episodes`, `show_first_aired`.
**Integrity flags:** the four §3.4 disagreement flags, `e1_starts_at_1`, `e2_starts_at_1`,
`e1_internal_gap`, `e2_internal_gap`.

---

## 9. Limits

1. **The frame inherits the stopped pull.** The candidate set rests on 2,549 users, 62.9% of plan.
   It is proportional across all ten strata to within 6.1 points
   (`s1-completer-diagnostic.md` §1), but a resumed pull would push more shows over 50 completers
   and the frame would grow. The thresholds are population-independent; these counts are not.
2. **The size cap is partly a cadence threshold** (§3.5), falling 44/51 on C4. A C4 result is
   computed on a population stripped of its longest-running titles.
3. **Air period and cadence are strongly confounded** (§3.4) and are not independent cuts.
4. **Platform fragmentation is not a variable in this study** (§5.2), and `show_network` is a
   present-day value that must not be read as release-time availability.
5. **The ≥50 candidate rule was applied on proxy counts** and has not been re-applied to the
   recomputed ones (§4). Moot on this frame.
6. **A headline computed on this frame is no longer provisional on the structural-threshold ground**
   named in [0014](../decisions/0014-no-content-filters-structural-fields.md), which is now closed.
   It remains provisional on every unapproved gate: **Step 5 contamination, Step 6 window `W`,
   Step 7 liveness and Step 8 analysis table.** Nothing downstream of those runs without written
   approval.
7. **Titles are shown; they are public catalogue metadata.** No user-level data appears here or in
   the frame table.

---

## 10. Files

| File | Contents | Location |
| :--- | :--- | :--- |
| `artifacts/step2-frame-ledger-and-distributions.md` | this file | public |
| `processed/step2/frame.csv` | the frame, 1,138 rows | local |
| `processed/step2/all_candidates_scored.csv` | all 2,094 candidates with the rule that removed each | local |
| `processed/step2/excluded_s2_unaired.csv` | the 12 unaired-S2 shows | local |
| `processed/step2/frame-summary.json` | every figure above, machine-readable | local |
| `processed/step2/seasons_extract.jsonl.gz`, `shows_extract.jsonl.gz` | trimmed payloads | local |
| `raw/shows/` | untouched API bodies; rebuild costs 0 calls | local |
| `src/step2_seasons_pull.py`, `src/step2_shows_pull.py`, `src/step2_build_frame.py` | the three passes | — |
| `logs/step2_seasons_run.json`, `logs/step2_shows_run.json` | run records, rate and error counters | local |
