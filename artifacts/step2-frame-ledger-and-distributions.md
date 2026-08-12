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
| **Frame** | **1,226 shows**, 232,958 S1-completer pairs |
| API calls | **3,320** — 2,094 on `/shows/:id/seasons?extended=episodes,full`, 1,226 on `/shows/:id?extended=full` |
| Pull result | 3,320 OK, 0 unavailable, 0 errors, 0 429s, 0 retries |
| Peak rate | 150 calls in any rolling 60s window, against a 150 throttle and a 200/min ceiling |
| Rebuild cost | **0 calls** — all bodies cached under `raw/` |

**Human Lead decisions carried in this revision (2026-08-12):** the 12 unaired-S2 shows are
excluded; per-season network is dropped as a field; air period is defined; the size quintile is cut
over the frame; `pool_completers` is recomputed on real season lengths. Each is marked where it
applies. **Nothing is held open in this document.**

---

## 1. What was called, and the rate discipline

Two passes, both one call per show, both resumable and both fully cached:

1. **Seasons** — `GET /shows/:id/seasons?extended=episodes,full`, 2,094 calls, one per candidate.
   Supplies real `E1`, `L1`, `F1`, `E2`, `L2`, `F2` and every air date.
2. **Show metadata** — `GET /shows/:id?extended=full`, 1,226 calls, **in-frame shows only.** The 868
   candidates that never reached the frame were not fetched: they are excluded, and their metadata
   would buy the study nothing for the spend.

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
| 5 | **S2 finale aired after 2025-12-31** | **60** | **1,226** |

Step 5 applies the cutoff as a half-open UTC instant, `first_aired < 2026-01-01T00:00:00Z`, per Step
1 §2.4 and D13. The finale is `F2 := max(E2)` after season 0 is filtered, per Step 1 §3.1 — a real
episode number from the payload, never a max-observed proxy.

**Step 4, resolved.** These 12 shows have a season 2 listed with episodes but no finale air date. The
inclusion rule states a condition on a date that does not exist, so the executor held them rather
than picking a reading. **The Human Lead excluded them on 2026-08-12.** All 12 report
`aired_episodes = 0` — the API's own statement that nothing in the season has aired — so they are
upcoming seasons, not measurable ones: *A Knight of the Seven Kingdoms* (550 completers),
*Dexter: Resurrection* (303), *Dune: Prophecy* (288), *Cyberpunk: Edgerunners* (262),
*All of Us Are Dead* (243), *Creature Commandos* (171), *Young Sherlock* (125), *The Institute*
(111), *Supacell* (109), *Moving* (71), *The Madison* (65), *The Celebrity Traitors* (53). Listed at
`processed/step2/excluded_s2_unaired.csv`.

Per-show audit of every rule: `processed/step2/all_candidates_scored.csv` carries all 2,094
candidates with the `exclusion` value that removed each. In-frame rows are exactly those with
`exclusion` empty.

---

## 3. Distributions, for setting structural thresholds

All over the 1,226-show frame. `decisions/0014` defers the gap-length and season-size thresholds
until these are visible; this is that input. **No threshold is proposed here.**

### 3.1 Gap length — S1 finale to S2 premiere, whole UTC calendar days

| Min | p05 | p25 | Median | p75 | p90 | p95 | Max | Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **−155** | 88.5 | 182 | **315** | 483 | 762 | 945 | **6,287** | 400.0 |

| Bucket | Shows | Share |
| :--- | ---: | ---: |
| negative | 1 | 0.1% |
| 0–89 d | 61 | 5.0% |
| 90–179 d | 241 | 19.7% |
| 180–269 d | 140 | 11.4% |
| 270–364 d | 296 | 24.1% |
| 1–1.5 y | 230 | 18.8% |
| 1.5–2 y | 119 | 9.7% |
| 2–3 y | 100 | 8.2% |
| 3–5 y | 26 | 2.1% |
| 5 y+ | 12 | 1.0% |

The single **negative gap** is *That's So Raven*: S1 finale 2004-03-06, S2 premiere 2003-10-03, a
155-day overlap. That is Trakt's season boundaries disagreeing with broadcast order, not a
computation error, and it is one show.

The long tail is real and mostly revival-shaped: the 12 shows past five years include *FLCL* (S1
finale 2001, S2 premiere 2018 — 6,287 days), *Wolf Hall* (3,546), *The Jinx* (3,325), *The Devil Is
a Part-Timer!* (3,304). A gap-length threshold is the lever that removes these.

### 3.2 Season size

| | Min | p05 | p25 | Median | p75 | p90 | p95 | Max | Mean |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **S1 episodes** | 1 | 6 | 8 | **10** | 14 | 23 | 25 | **172** | 13.2 |
| **S2 episodes** | 2 | 6 | 8 | **11** | 18 | 24 | 26 | **108** | 13.8 |

| Episodes | S1 shows | S2 shows |
| :--- | ---: | ---: |
| 1–3 | 13 | 5 |
| 4–6 | 146 | 124 |
| 7–8 | 197 | 194 |
| 9–10 | 303 | 279 |
| 11–13 | 255 | 243 |
| 14–22 | 173 | 227 |
| 23–26 | 110 | 114 |
| 27+ | 29 | 40 |

Both distributions are tight around 8–13 with a thin high tail. The 27+ tail is where daily strips
and long-run anime sit — the structures the dropped content filters were reaching for, now visible
as a number instead of a genre.

### 3.3 Cadence bucket, D12

`span := S2 finale − S2 premiere` in whole UTC days; `weekly_span := (L2 − 1) × 7`; buckets
evaluated in order, first match wins.

| Bucket | Definition | Shows | Share |
| :--- | :--- | ---: | ---: |
| **C0** Unclassifiable | `P`, `F_d` or `L2` missing, or `span < 0` | **0** | 0% |
| **C1** All-at-once | `span ≤ 1` | **214** | 17.5% |
| **C2** Weekly | `abs(span − weekly_span) ≤ 3` | **358** | 29.2% |
| **C3** Faster than weekly | `1 < span < weekly_span − 3` | **178** | 14.5% |
| **C4** Slower than weekly | `span > weekly_span + 3` | **476** | 38.8% |

C0 is empty: every in-frame show classified on real dates. S2 span itself runs min 0, p25 35,
median 70, p75 189, max 1,348 days.

**D12's required fragility count: 7 shows sit within one day of a bucket boundary** — 5 in C3, 2 in
C2 — **0.6% of the frame.** By D12's own test the thresholds are **not load-bearing**, and a Step 13
arm on them is not indicated on this evidence.

One caution on how to read a wider band. 248 shows sit within *three* days of a boundary, but 220 of
those are same-day drops (`span = 0`) whose distance is exactly 2 by construction — a same-day
release must move two days to stop being all-at-once. That is arithmetic, not metadata fragility.
The one-day figure is the meaningful one.

*Boundary distance is the smallest change in `span`, in days, that would move a show to a different
bucket, probing only spans ≥ 0 — a negative span is impossible, so treating "span − 1 would be C0"
as a flip would have counted every binge release as fragile. That defect was present in the first
run of this build and is corrected.*

### 3.4 Air period — calendar year of the S2 finale

**Defined by the Human Lead, 2026-08-12:** the calendar year of the S2 finale, bucketed to bracket
the 2020 production shutdown and nothing finer.

| Air period | Shows | Share |
| :--- | ---: | ---: |
| pre-2020 | **817** | 66.6% |
| 2020–2022 | **223** | 18.2% |
| 2023–2025 | **186** | 15.2% |

No post-2025 bucket exists by construction: ledger step 5 removes those shows. Cadence composition
differs sharply across the buckets, which is worth seeing before any threshold is drawn on either:

| Air period | C1 | C2 | C3 | C4 |
| :--- | ---: | ---: | ---: | ---: |
| pre-2020 | 84 | 254 | 73 | 406 |
| 2020–2022 | 80 | 58 | 43 | 42 |
| 2023–2025 | 50 | 46 | 62 | 28 |

Weekly (C2) and slower-than-weekly (C4) dominate the pre-2020 era; all-at-once (C1) and
faster-than-weekly (C3) are far more prevalent after it. **Air period and cadence are strongly
confounded**, and the study should not treat them as independent cuts.

### 3.5 Pool completer count, in-frame

| Min | p05 | p25 | Median | p75 | p90 | p95 | Max | Mean |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 53 | 70 | **113** | 221 | 430 | 606 | **1,662** | 190.0 |

---

## 4. `pool_completers`, recomputed on real season lengths

**Human Lead, 2026-08-12: the max-observed proxy is superseded and no result may use it.** Done.
The frame's `pool_completers` is now computed by applying the approved Step 1 §4 rule — `F1 ∈ D1`
and `|D1| ≥ ceil(0.90 × L1)`, with `D1` the distinct S1 episodes whose number is a **member** of the
real `E1` — against the real `E1`, `L1 = |E1|` and `F1 = max(E1)` now in the frame.

**The recompute changes nothing on this frame, and that is a finding rather than a null result:**

| | Proxy | Real |
| :--- | ---: | ---: |
| Total S1-completer pairs | 232,958 | **232,958** |
| Shows whose count rose | — | **0** |
| Shows whose count fell | — | **0** |
| Shows now below 50 completers | — | **0** |

The reason is direct and checkable: **the proxy `L1_hat` equals the real `|E1|` on 1,225 of the
1,226 in-frame shows.** That is exactly what the diagnostic predicted for this population — on a
show with ≥50 completers, at least 50 users independently reached the true finale, so
max-observed and true season length coincide. The proxy was never trustworthy in the long tail (the
diagnostic measured 118 shows moving between pool sizes), and it is not being rehabilitated
generally. On *this* frame it happens to have been exact.

The single exception is **Star Trek: Prodigy**: real `L1 = 19` with `F1 = 20` — 19 episodes numbered
up to 20, the one internal-gap season in the frame — against a proxy `L1_hat` of 20. Both give a bar
of 18 episodes and the same finale, so its count is 74 either way.

`pool_completers_proxy` is retained as a column so the two are diffable without a rerun.

**One thing this does not do, and it is a Human Lead call.** The ≥50 candidate rule was applied to
the *proxy* counts. It has **not** been re-applied to the recomputed counts. On this frame the
question is moot — zero shows fall below 50 — but the rule's basis is worth stating rather than
leaving implied.

---

## 5. Field inventory

### 5.1 Show-level metadata — pulled, and fully populated

`GET /shows/:id?extended=full`, 1,226 calls. Every field the Human Lead asked for is present and
effectively complete:

| Field | Non-null | Distinct values |
| :--- | ---: | ---: |
| `country` (origin) | 1,226 (100%) | 23 |
| `language` | 1,226 (100%) | 16 |
| `languages` | 1,226 (100%) | 68 combinations |
| `genres` | 1,226 (100%) | 477 combinations |
| `network` (show level) | 1,226 (100%) | **150** |
| `status` | 1,226 (100%) | 3 |
| `year`, `first_aired`, `aired_episodes` | 1,226 (100%) | — |
| `runtime` | 1,224 (99.8%) | 59 |
| `certification` | 1,199 (97.8%) | 7 |

Shape of the frame on those fields, as context for any later cut:

- **Country:** us 908, gb 127, jp 92, ca 32, au 10, kr 9, es 7, de 7, and 15 others.
- **Language:** en 1,086, ja 91, es 9, ko 9, de 7, no 5, and 10 others.
- **Network:** Netflix 182, CBS 57, NBC 57, ABC 54, HBO 53, FOX 49, Prime Video 42, The CW 34,
  BBC One 30, Hulu 28, and 140 more.
- **Status:** ended 743, canceled 328, returning series 155.
- **Top genres:** drama 772, comedy 494, fantasy 375, science-fiction 345, action 326, adventure
  299, crime 247, mystery 212, animation 128, **anime 91**.
- **Certification:** TV-MA 535, TV-14 448, TV-PG 131, TV-Y7 55, TV-G 27, NR 2, TV-Y 1.

**All of these are fields, not filters.** Nothing above removed a show. In particular the 91
anime-tagged and 92 Japanese-origin shows are in the frame, per `decisions/0014`.

**"Platform" has no distinct representation.** The show object carries `network` and nothing else
that names a service; there is no separate distributor or platform field. `network` is the closest
available and is recorded under its own name rather than relabelled.

### 5.2 Per-season network — DROPPED as a field

**Human Lead, 2026-08-12: dropped.** `decisions/0014`'s resolution rule is *"if it cannot be
measured, it is dropped as a field and the limitation is stated."* The measurement:

| | |
| :--- | ---: |
| Season objects seen, season 0 excluded, all 2,094 fetched shows | 6,645 |
| Of those, `network` non-null | **47 (0.71%)** |
| Shows with zero distinct season-level networks | 2,080 |
| Shows with exactly one | 13 |
| Shows with **two or more** | **1** |

The columns `s1_network` and `s2_network` are **removed from the frame table.** The evidence is
retained in `processed/step2/frame-summary.json` so the decision stays auditable.

**The limitation, stated as 0014 requires.** Per-season platform is not measurable from this API.
The concept "this show's seasons were split across services" has no representation in the data, so
**platform fragmentation is not a variable in this study** and no result may claim to control for
it, stratify on it, or rule it out. Exactly one show in 2,094 carries two distinct season-level
network values; that is a count consistent with noise and is **not** read as fragmentation here.

This closes the first of the two open problems in `decisions/0014` §"platform fragmentation is
unverified." **The second survives and applies to the show-level `network` pulled in §5.1:** that
field records *today's* network, and a title that moved services between seasons shows only its
current one. A present-day value is not evidence about what a viewer faced at release, so
`show_network` must not be used as a release-time availability measure either.

### 5.3 Dates

S1 premiere, S1 finale, S2 premiere, S2 finale and both season-level `first_aired` values are
**100% non-null across the frame.** Episode-level dates are used throughout: premiere is the
`first_aired` of the episode numbered `min(E)`, finale the `first_aired` of `max(E)`. Season-level
`first_aired` is recorded alongside but unused, so the two can be diffed later without a refetch.

---

## 6. Metadata integrity checks (Step 1 §3.4, required)

| Check | In-frame shows |
| :--- | ---: |
| S1 `episode_count` / `aired_episodes` / `|E1|` disagree | **0** |
| S2 `episode_count` / `aired_episodes` / `|E2|` disagree | **0** |
| S2 `aired_episodes < |E2|` — the subset where **Continued** may be unreachable | **0** |
| S1 `aired_episodes < |E1|` | **0** |

**All three agree on every in-frame show for both seasons.** The listed-but-unaired hazard §3.4
raised, and which the Step 0 probe found on the probe show's season 0, does **not** reach this
frame — the 31 Dec 2025 cutoff removed it, which is the mechanism §3.4 predicted but explicitly
declined to assume. It is now verified rather than expected.

### Episode numbering — a real finding, and it is benign

Two properties are recorded separately because conflating them hides the interesting one:

| | In-frame shows |
| :--- | ---: |
| E1 has an internal gap | **1** (Star Trek: Prodigy) |
| E2 has an internal gap | 0 |
| E1 does not start at episode 1 | 0 |
| **E2 does not start at episode 1** | **4** |

The four are *Naruto* (E2 = 53–104), *Naruto Shippūden* (33–53), *One Piece* (62–77) and *Hunter x
Hunter* (63–136) — long-run series numbered **absolutely across seasons** rather than restarting
each season.

**Checked against the watch data, at zero API cost: the histories use the same absolute numbers,
with 100% overlap on all four shows** (21/21, 16/16, 52/52, 74/74 distinct S2 numbers matching
`E2`). So Step 1 §4's set-membership form handles them correctly. **The withdrawn `1..F` range form
would have failed on all four**, scoring every S2 episode out of range — the first empirical case
where that withdrawn defect would have bitten, and an argument for the version that was kept.

The Step 1 §3.3 gap hypothesis remains near-untested: one in-frame show has an internal S1 gap and
none has an internal S2 gap.

---

## 7. Size quintile

**Human Lead, 2026-08-12: cut over the frame of 1,226, not the 2,094 candidates** — the quintile
exists to cut results, and results exist only for in-frame shows. Single column, `size_quintile`,
on the recomputed `pool_completers`.

| Q1 | Q2 | Q3 | Q4 | Q5 |
| ---: | ---: | ---: | ---: | ---: |
| 247 | 244 | 249 | 241 | 245 |

---

## 8. Frame contents

`processed/step2/frame.csv`, 1,226 rows. Every column is a **field, not a filter** — nothing below
was used to include or exclude a show except the five ledger rules in §2.

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

1. **The frame inherits the stopped pull.** The candidate set is defined on 2,549 users, 62.9% of
   the plan. It is proportional across all ten strata to within 6.1 points
   (`artifacts/s1-completer-diagnostic.md` §1), but a resumed pull would push more shows over 50
   completers and the frame would grow. The 2,094 → 1,226 ratio would not necessarily hold.
2. **No structural threshold is applied.** Per `decisions/0014` the frame carries no gap-length and
   no season-size exclusion, so **any headline computed on it is provisional** and must not be
   reported as the study's result. §3.1 and §3.2 are the input for setting those.
3. **Platform fragmentation is not a variable in this study** (§5.2), and `show_network` is a
   present-day value that must not be read as release-time availability.
4. **Air period and cadence are strongly confounded** (§3.4) and must not be treated as independent
   cuts.
5. **The ≥50 candidate rule was applied on proxy counts** and has not been re-applied to the
   recomputed ones (§4). Moot on this frame — zero shows fall below 50 — but stated rather than
   implied.
6. **Titles are shown; they are public catalogue metadata.** No user-level data appears here or in
   the frame table.

---

## 10. Files

| File | Contents | Location |
| :--- | :--- | :--- |
| `artifacts/step2-frame-ledger-and-distributions.md` | this file | public |
| `processed/step2/frame.csv` | the frame, 1,226 rows | local |
| `processed/step2/all_candidates_scored.csv` | all 2,094 candidates with the rule that removed each | local |
| `processed/step2/excluded_s2_unaired.csv` | the 12 unaired-S2 shows | local |
| `processed/step2/frame-summary.json` | every figure above, machine-readable | local |
| `processed/step2/seasons_extract.jsonl.gz`, `shows_extract.jsonl.gz` | trimmed payloads | local |
| `processed/step2/seasons_ledger.jsonl`, `shows_ledger.jsonl` | one row per fetched show | local |
| `raw/shows/` | untouched API bodies; rebuild costs 0 calls | local |
| `src/step2_seasons_pull.py`, `src/step2_shows_pull.py`, `src/step2_build_frame.py` | the three passes | — |
| `logs/step2_seasons_run.json`, `logs/step2_shows_run.json` | run records, rate and error counters | local |
