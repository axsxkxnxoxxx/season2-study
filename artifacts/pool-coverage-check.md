# Pool coverage check — Step 4 data on disk

> **SUPERSEDED SNAPSHOT — header added 2026-08-12.** This diagnostic was run while the Step 4 pull
> was still in flight and describes **2,134 complete users, 235 discarded, ~58% of the plan.** The
> pull was later stopped deliberately at **2,549 complete, 287 discarded, 62.9% of the plan**, and
> every count below is a floor on a superseded snapshot rather than a description of the data on
> disk. **Do not quote a figure from this file as current.**
>
> Current equivalents: `artifacts/s1-completer-diagnostic.md` (re-run on the full pulled pool, with
> its own §1.1 before/after diff) and `artifacts/step2-frame-ledger-and-distributions.md` §1.
> Retained because the coverage question it answers is not re-asked elsewhere, and because its
> single-user-show finding is cited downstream.

**What this is:** a read-only diagnostic requested by the Human Lead. It is **not a numbered step
and not a gate**. Nothing here is a proposal, and no rule is adopted.

**API calls made: zero.** Every number below comes from files already on disk under `raw/users/`.
No network request was issued at any point.

**Snapshot taken:** 2026-08-11, ~19:30 UTC. The Step 4 pull is **partial** — `logs/step4_progress.json`
last updated 17:49 UTC with `finished: false`, 2,407 users decided and 1,681 still in plan, and no
pull process was running at scan time. The directory count did not move during the scan, so the
snapshot is internally consistent.

**Aggregates and counts only.** No usernames, user IDs, or individual histories appear in this file.
The per-show table is at `processed/pool-coverage-per-show.csv` (git-ignored) and also contains no
user identifiers.

---

## 1. What is on disk, and who counts as a contributing user

`raw/users/` holds **4,319 user directories**. A directory existing is not the same as a history
being pulled. Subdirectory families present: `stats/` 4,319, `history/` 2,370, `following/` 433,
`followers/` 433, `watched/` 1 (a Step 0 probe).

Classification of all 4,319 directories, reconciled against `processed/step4/pull_ledger.jsonl`
(final outcome per slug, 2,407 distinct slugs decided):

| Class | Users | History on disk | In the coverage numbers below |
| :--- | ---: | :--- | :--- |
| `complete` — pull accepted | **2,134** | yes | yes (and reported separately as the strict cohort) |
| `discarded_over_tolerance` — pages kept, pull rejected as incomplete | **235** | yes | yes, in the "all on disk" cohort only |
| interrupted mid-pull, no ledger decision | **1** | yes, partial (81 of a forecast 150 pages) | yes, in the "all on disk" cohort only |
| `skipped_length_forecast` — over the 300-page cap, never started | **38** | no | no |
| not yet attempted — `stats/` only, still in plan | **1,911** | no | no |
| **Total** | **4,319** | | |

2,134 + 235 + 1 + 38 + 1,911 = 4,319. The Step 3/4 usable pool is 4,088 users, 4,050 eligible after
the forecast cap; the difference between 4,319 directories and 4,088 pool users is directories
created by Step 3 discovery and Step 0 probes that never entered the pull plan.

**Access-denied and non-history records: zero.**

- Grep across all **102,798** history `*.meta.json` files: **0** with `access_denied: true`, **0**
  with `ok: false`. Every persisted history page is a 2xx payload.
- The pull log agrees: `access_denied` 0, `private_or_absent` 0, `user_403_skipped` 0.
- Therefore no user in this snapshot is at risk of the failure mode the CLAUDE.md rule warns about —
  a skipped user silently read as a user with no shows. There are no skipped users yet. The 1,911
  not-yet-attempted users are **absent**, not empty, and are excluded from every denominator below.

**Users actually contributing episode data: 2,370.** Every user with a `history/` directory has at
least one episode record. **0** users have a history directory and zero episode records.

**Record volume on disk**

| | Count |
| :--- | ---: |
| History pages | 102,798 |
| Records parsed | 25,170,185 |
| Episode records | 22,630,725 (89.9%) |
| Movie records | 2,539,460 (10.1%) — excluded from everything below |
| Episode records with no show trakt id | 0 |
| Episode records with no `watched_at` | 6 |
| Unparseable or non-list payloads | 0 |

Per contributing user: mean 290.5 distinct shows (median 223, min 1, max 2,734) and mean 9,549
episode records (median 7,344, min 10, max 38,205).

**Two known duplicate-page artefacts.** Two users have extra page files on disk left by earlier
attempts at a smaller page size (one user: 15 pages at limit 100 plus 6 at limit 250; one user: a
Step 0 probe page at limit 10). They duplicate about 1,469 records, 0.006% of the total. Distinct
show counts and distinct user counts are unaffected because those are computed per user; only the
raw record totals in the table above are marginally inflated.

---

## 2. Item 1 — distinct shows

| Cohort | Contributing users | Distinct shows |
| :--- | ---: | ---: |
| All history on disk | 2,370 | **44,866** |
| `complete` only | 2,134 | **43,278** |

Shows are keyed on `show.ids.trakt`. No episode record was missing that id, so no show was collapsed
or lost to a fallback key. Adding the 236 non-`complete` users adds 1,588 shows, 3.7%.

---

## 3. Item 2 — shows by year of most recent watched episode

Per show, the maximum `watched_at` over **all** contributing users, then shows counted by the year of
that maximum. This is a pool-level recency measure: a show lands in 2026 if any one user in the pool
watched an episode of it in 2026.

Collapsed:

| Year of pool-latest watch | Shows | Share | Cumulative |
| :--- | ---: | ---: | ---: |
| pre-1990 | 308 | 0.7% | 0.7% |
| 1990–2009 | 860 | 1.9% | 2.6% |
| 2010–2014 | 1,313 | 2.9% | 5.5% |
| 2015–2019 | 5,243 | 11.7% | 17.2% |
| 2020 | 2,251 | 5.0% | 22.2% |
| 2021 | 3,138 | 7.0% | 29.2% |
| 2022 | 3,388 | 7.6% | 36.8% |
| 2023 | 3,937 | 8.8% | 45.6% |
| 2024 | 4,865 | 10.8% | 56.4% |
| 2025 | 7,081 | 15.8% | 72.2% |
| 2026 (through 11 Aug) | 12,482 | 27.8% | 100.0% |
| **Total** | **44,866** | | |

Full per-year counts:

| Year | Shows | Year | Shows | Year | Shows |
| :--- | ---: | :--- | ---: | :--- | ---: |
| 1914 | 1 | 1980 | 7 | 2004 | 52 |
| 1957 | 1 | 1981 | 2 | 2005 | 65 |
| 1960 | 2 | 1982 | 3 | 2006 | 68 |
| 1961 | 1 | 1983 | 5 | 2007 | 69 |
| 1963 | 1 | 1984 | 8 | 2008 | 79 |
| 1964 | 1 | 1985 | 6 | 2009 | 64 |
| 1965 | 1 | 1986 | 14 | 2010 | 69 |
| 1966 | 2 | 1987 | 8 | 2011 | 124 |
| 1967 | 4 | 1988 | 17 | 2012 | 189 |
| 1968 | 2 | 1989 | 12 | 2013 | 386 |
| 1969 | 2 | 1990 | 10 | 2014 | 545 |
| **1970** | **170** | 1991 | 21 | 2015 | 617 |
| 1971 | 3 | 1992 | 20 | 2016 | 797 |
| 1973 | 5 | 1993 | 23 | 2017 | 1,041 |
| 1974 | 4 | 1994 | 19 | 2018 | 1,261 |
| 1976 | 5 | 1995 | 32 | 2019 | 1,527 |
| 1977 | 4 | 1996 | 35 | 2020 | 2,251 |
| 1978 | 7 | 1997 | 28 | 2021 | 3,138 |
| 1979 | 10 | 1998 | 41 | 2022 | 3,388 |
| | | 1999 | 43 | 2023 | 3,937 |
| | | 2000 | 35 | 2024 | 4,865 |
| | | 2001 | 46 | 2025 | 7,081 |
| | | 2002 | 56 | 2026 | 12,482 |
| | | 2003 | 54 | | |

Years with no shows are omitted. Between 1957 and 1990 the empty years are 1958, 1959, 1962, 1972
and 1975.

**Three observations on the timestamps, reported as observations only.**

1. **The 1970 spike is epoch zero.** 170 shows have a pool-latest `watched_at` of exactly
   `1970-01-01`. Pool-wide, **285,296 episode records** (1.26% of episodes) across **387 users**
   carry a `1970-01-01` timestamp, and **525,525 records** (2.32%) across **742 users** are dated
   before 1990. Every one of the 188 shows whose pool-latest is before 1971 has 1 or 2 users.
2. **No future-dated records.** Maximum `watched_at` anywhere on disk is `2026-08-11T17:07Z`, before
   the scan. Nothing is dated past the pull.
3. **6 episode records have no `watched_at` at all.**

These are surfaced because both W and the liveness rule run on timestamps. Deciding what to do about
them is Step 5 and is not touched here.

**Cross-tab, year of pool-latest watch by number of distinct users** (shows):

| Year | 1 | 2 | 3–4 | 5–9 | 10–19 | 20–49 | 50–99 | 100–249 | 250–499 | 500–999 | 1000+ | Total |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| pre-1990 | 294 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 308 |
| 1990–2009 | 771 | 72 | 17 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 860 |
| 2010–2014 | 1,070 | 167 | 67 | 8 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1,313 |
| 2015–2019 | 3,418 | 987 | 561 | 236 | 33 | 8 | 0 | 0 | 0 | 0 | 0 | 5,243 |
| 2020 | 1,191 | 499 | 313 | 201 | 42 | 5 | 0 | 0 | 0 | 0 | 0 | 2,251 |
| 2021 | 1,635 | 588 | 512 | 300 | 86 | 17 | 0 | 0 | 0 | 0 | 0 | 3,138 |
| 2022 | 1,508 | 635 | 578 | 455 | 181 | 30 | 1 | 0 | 0 | 0 | 0 | 3,388 |
| 2023 | 1,603 | 672 | 705 | 587 | 255 | 106 | 9 | 0 | 0 | 0 | 0 | 3,937 |
| 2024 | 1,771 | 823 | 827 | 749 | 463 | 210 | 21 | 1 | 0 | 0 | 0 | 4,865 |
| 2025 | 2,136 | 999 | 1,041 | 1,260 | 925 | 553 | 147 | 20 | 0 | 0 | 0 | 7,081 |
| 2026 | 1,779 | 1,012 | 1,274 | 1,804 | 1,906 | 2,195 | 1,186 | 859 | 316 | 132 | 19 | 12,482 |
| **Total** | **17,176** | **6,468** | **5,895** | **5,600** | **3,892** | **3,124** | **1,364** | **880** | **316** | **132** | **19** | **44,866** |

Of the 9,727 shows carried by 10 or more users, 68.0% were last watched in 2026 and 84.9% in 2025 or
2026. Old-latest shows are almost entirely single-user shows.

---

## 4. Item 3 — distinct users per show

**Full table: `processed/pool-coverage-per-show.csv`**, 44,866 rows, one per show, columns:
`show_trakt_id, title, show_year, users_all_on_disk, users_complete_only, episode_records,
latest_watched_at, latest_watched_year`. No user identifiers.

Summary:

| Statistic | All on disk (2,370 users) | `complete` only (2,134 users) |
| :--- | ---: | ---: |
| Shows | 44,866 | 43,278 |
| User–show pairs | 688,546 | 619,309 |
| Mean users per show | 15.35 | 14.31 |
| Median | 2 | 2 |
| p75 | 8 | 7 |
| p90 | 27 | 26 |
| p95 | 61 | 57 |
| p99 | 258 | 235 |
| Max | 1,671 | 1,503 |
| Shows with exactly 1 user | 17,176 (38.3%) | 16,755 (38.7%) |
| Shows with fewer than 5 users | 29,539 (65.8%) | 28,752 (66.4%) |
| Shows with ≥10 users | 9,727 (21.7%) | 9,114 (21.1%) |
| Shows with ≥50 users | 2,711 (6.0%) | 2,482 (5.7%) |
| Shows with ≥100 users | 1,347 (3.0%) | 1,203 (2.8%) |

Concentration of the 688,546 user–show pairs: top 100 shows hold 12.1%, top 500 hold 33.5%, top
1,000 hold 46.1%, top 5,000 hold 77.1%.

**Top 30 shows by distinct users** (all on disk). "Latest watch" is the date only, pool-wide maximum.

| # | Show | Show year | Users (all) | Users (complete) | Episode records | Latest watch |
| ---: | :--- | ---: | ---: | ---: | ---: | :--- |
| 1 | Stranger Things | 2016 | 1,671 | 1,503 | 60,744 | 2026-08-10 |
| 2 | Game of Thrones | 2011 | 1,636 | 1,464 | 138,092 | 2026-08-11 |
| 3 | Breaking Bad | 2008 | 1,426 | 1,278 | 91,957 | 2026-08-11 |
| 4 | Black Mirror | 2011 | 1,353 | 1,228 | 30,593 | 2026-08-10 |
| 5 | The Boys | 2019 | 1,335 | 1,189 | 45,648 | 2026-08-09 |
| 6 | Squid Game | 2021 | 1,269 | 1,138 | 21,209 | 2026-08-08 |
| 7 | The Last of Us | 2023 | 1,205 | 1,071 | 16,484 | 2026-08-07 |
| 8 | The Walking Dead | 2010 | 1,191 | 1,070 | 152,146 | 2026-08-11 |
| 9 | Chernobyl | 2019 | 1,104 | 1,000 | 6,092 | 2026-08-08 |
| 10 | The Mandalorian | 2019 | 1,095 | 972 | 23,664 | 2026-08-09 |
| 11 | Loki | 2021 | 1,092 | 973 | 11,354 | 2026-08-08 |
| 12 | WandaVision | 2021 | 1,092 | 978 | 10,468 | 2026-08-08 |
| 13 | Westworld | 2016 | 1,089 | 974 | 30,107 | 2026-08-09 |
| 14 | Sherlock | 2010 | 1,083 | 971 | 13,489 | 2026-08-11 |
| 15 | House of the Dragon | 2022 | 1,062 | 956 | 22,150 | 2026-08-11 |
| 16 | Rick and Morty | 2013 | 1,050 | 938 | 79,008 | 2026-08-11 |
| 17 | Mr. Robot | 2015 | 1,039 | 934 | 32,650 | 2026-08-11 |
| 18 | Marvel's Daredevil | 2015 | 1,030 | 915 | 34,260 | 2026-08-10 |
| 19 | The Witcher | 2019 | 1,002 | 912 | 19,531 | 2026-08-07 |
| 20 | Wednesday | 2022 | 979 | 889 | 11,945 | 2026-08-10 |
| 21 | Fallout | 2024 | 976 | 877 | 12,454 | 2026-08-10 |
| 22 | Severance | 2022 | 974 | 880 | 16,730 | 2026-08-11 |
| 23 | The Big Bang Theory | 2007 | 957 | 858 | 250,469 | 2026-08-10 |
| 24 | Friends | 1994 | 956 | 861 | 213,548 | 2026-08-11 |
| 25 | Better Call Saul | 2015 | 938 | 831 | 49,801 | 2026-08-10 |
| 26 | The Office | 2005 | 935 | 833 | 163,701 | 2026-08-11 |
| 27 | Dexter | 2006 | 932 | 833 | 83,407 | 2026-08-10 |
| 28 | True Detective | 2014 | 911 | 816 | 18,716 | 2026-08-08 |
| 29 | Lost | 2004 | 901 | 814 | 103,247 | 2026-08-10 |
| 30 | Dark | 2017 | 894 | 808 | 19,168 | 2026-08-11 |

---

## 5. Item 4 — distribution of the per-show user count

All history on disk: 44,866 shows, 688,546 user–show pairs.

| Distinct users | Shows | Share of shows | User–show pairs | Share of pairs |
| :--- | ---: | ---: | ---: | ---: |
| 1 | 17,176 | 38.28% | 17,176 | 2.49% |
| 2 | 6,468 | 14.42% | 12,936 | 1.88% |
| 3–4 | 5,895 | 13.14% | 19,921 | 2.89% |
| 5–9 | 5,600 | 12.48% | 36,886 | 5.36% |
| 10–19 | 3,892 | 8.67% | 52,809 | 7.67% |
| 20–49 | 3,124 | 6.96% | 96,221 | 13.97% |
| 50–99 | 1,364 | 3.04% | 95,417 | 13.86% |
| 100–249 | 880 | 1.96% | 134,280 | 19.50% |
| 250–499 | 316 | 0.70% | 110,911 | 16.11% |
| 500–999 | 132 | 0.29% | 89,165 | 12.95% |
| 1000+ | 19 | 0.04% | 22,824 | 3.31% |
| **Total** | **44,866** | **100%** | **688,546** | **100%** |

`complete` users only: 43,278 shows, 619,309 user–show pairs.

| Distinct users | Shows | Share of shows | User–show pairs | Share of pairs |
| :--- | ---: | ---: | ---: | ---: |
| 1 | 16,755 | 38.71% | 16,755 | 2.71% |
| 2 | 6,300 | 14.56% | 12,600 | 2.03% |
| 3–4 | 5,697 | 13.16% | 19,311 | 3.12% |
| 5–9 | 5,412 | 12.51% | 35,757 | 5.77% |
| 10–19 | 3,675 | 8.49% | 49,713 | 8.03% |
| 20–49 | 2,957 | 6.83% | 90,222 | 14.57% |
| 50–99 | 1,279 | 2.96% | 88,350 | 14.27% |
| 100–249 | 798 | 1.84% | 121,337 | 19.59% |
| 250–499 | 281 | 0.65% | 97,666 | 15.77% |
| 500–999 | 115 | 0.27% | 76,657 | 12.38% |
| 1000+ | 9 | 0.02% | 10,941 | 1.77% |
| **Total** | **43,278** | **100%** | **619,309** | **100%** |

The two cohorts have the same shape. Dropping the 236 non-`complete` users moves no share-of-shows
bucket by more than 0.43 points. The one visible difference is in share of pairs at 1000+, 3.31%
against 1.77%, which is arithmetic rather than substance: a smaller cohort puts fewer shows over the
1,000-user line (19 against 9). Nothing in this coverage picture depends on whether those users are
kept.

---

## 6. How the numbers were produced, and their limits

- Source: every `raw/users/<slug>/history/*.json` payload file, `.meta.json` files excluded from
  parsing and used only for the access-denied and endpoint checks. Cohort labels come from
  `processed/step4/pull_ledger.jsonl` (last entry per slug) and `processed/step4/pull_order.jsonl`.
- Records with `type != "episode"` are excluded. Movies never enter any count.
- Duplicate records within a user do not affect items 1, 3, or 4 (distinct shows, distinct users) or
  item 2 (a maximum), so no record-level de-duplication was applied. It does affect the raw record
  totals in §1, by the ~1,469 records noted there.
- Reconciliation check: on-disk page counts match the ledger's `pages_read` for every user with a
  history directory except the two duplicate-page cases already described.

**Limits.** This is a coverage snapshot of a partial pull: 2,370 of 4,088 usable pool users, 58%. The
remaining 1,681 planned users are absent, not empty, and every denominator here excludes them. The
38 users over the 300-page forecast cap are the heaviest trackers in the pool and are absent by rule,
which will depress the heavy tail of both the per-user show count and the per-show user count. None
of these numbers are contamination-adjusted, frame-restricted, or filtered by any Step 5, 6, 7, or 8
rule — none of which exist yet or are proposed here.
