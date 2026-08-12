# S1-completer diagnostic — Step 4 snapshot

**What this is:** a read-only diagnostic requested by the Human Lead. It is **not a numbered step,
not a gate, and not Step 9.** Nothing here is a proposal, no rule is adopted, and no exclusion,
window, liveness or outcome-state logic is applied.

**API calls made: zero.** Every number comes from files already on disk. No network request was
issued at any point.

**Aggregates and counts only.** No usernames, user IDs, or individual watch histories appear in this
file. Per-show detail is at `processed/s1-completer-diagnostic-per-show.csv` (git-ignored), which
also carries no user identifiers.

**Reproducible at zero API cost:** `src/diag_s1_completers_scan.py` then `src/diag_s1_completers.py`.
Full machine-readable output: `processed/s1-completer-diagnostic-summary.json`.

---

## 0. Gate check — Step 1 is approved, and this uses the approved text

`decisions/0001-step1-outcome-definition-gate.md` records **Step 1 APPROVED by the Human Lead,
2026-08-10**, with `artifacts/step1-outcome-definition.md` as the operative document. The
S1-completion rule used below is that document's **Section 4**, quoted:

> Let `D1` = the set of **distinct** S1 episodes for that user and show **whose number is a member
> of `E1`** […] **Required:** `F1 ∈ D1` **and** `|D1| ≥ ceil(0.90 × L1)`.

Supporting rules applied as written: **§2.1** dedup on `(show.ids.trakt, season, number)` scoped to
the user, distinct episodes never play events; **§2.3** all `action` values count as watching;
**§3.1** specials are season 0 and are excluded.

### Four ways the approved text is more specific than the criterion in the request

The request phrased the criterion as "watched the S1 finale AND at least 90 percent of distinct S1
episodes." That is the same rule, but the approved text settles four things the phrasing leaves
open. **The approved text is used wherever they differ.**

| # | Request | Approved Step 1 §4 | Effect here |
| :-- | :--- | :--- | :--- |
| 1 | "90 percent of distinct S1 episodes" | denominator is `L1`, the **season length**, not the count the user watched | Used as written. The request's phrasing read literally is vacuous (every user watches 100% of what they watched). |
| 2 | "at least 90 percent" | **`ceil(0.90 × L1)`**, stated in episodes | Strict. `L1 = 8` requires all 8, because 7/8 is 87.5%. |
| 3 | membership unstated | `D1 ⊆ E1` by **set** membership, not the range `1..F1` | Immaterial under the proxy below, which makes `E1` a contiguous range by construction. Flagged because it is exactly the F1 defect Step 1 withdrew, and it will **not** be immaterial once a real `E1` exists. |
| 4 | — | `F1 := max(E1)`, and **"`F := L` is forbidden"** (§3.1) except by Human Lead adoption of the §3.3 fallback | **This diagnostic violates it, deliberately and on instruction.** See §2. |

**Not applied, because they are not this diagnostic's question and their inputs do not exist:**
`τ_pull` (still has no value — the one outstanding Step 1 item), right-censoring, the horizon `H`,
window `W` (Step 6, not approved), liveness (Step 7, not approved), Step 5 contamination exclusions
(not approved), and the three outcome states. **"Has any S2 episode at all" is not "Started" and is
not "Continued."** It is a raw presence count and must not be read as an outcome state.

---

## 1. Cohort

The Step 4 pull is **partial and was not running at scan time** (`logs/step4_progress.json`,
`finished: false`, 2,407 of 4,050 planned users decided).

This diagnostic uses the **2,134 `complete` users** in `processed/step4/parsed/`. That is the
rule-conformant cohort: under `decisions/0012`, the **235** `discarded_over_tolerance` users have
their pages **discarded rather than returned as data**, and no parsed file is written for them. The
**38** users over the page-forecast cap and the **1,681** not-yet-attempted users have no history on
disk. All of these are **absent, not empty**, and appear in no denominator here.

| | Count |
| :--- | ---: |
| Users | 2,134 |
| S1 + S2 episode records read | 10,115,630 |
| Distinct `(user, show, season, number)` after the §2.1/§2.2 collapse | 9,116,721 |
| Collapsed away as duplicate plays | 998,909 (9.87%) |
| Shows with ≥1 S1 record | 41,576 |
| Shows with ≥1 S2 record | 12,082 |
| User–show pairs with ≥1 S1 episode | 593,795 |
| **User–show pairs meeting the §4 S1-completion rule** | **443,922** (74.8% of the above) |

---

## 2. The season-length proxy, and its direction of error

No Step 2 frame exists, so `E1` and `E2` have no real source. **Substituted, for this diagnostic
only:**

> `L1_hat := F1_hat :=` the **maximum S1 episode number observed across all 2,134 cohort users** for
> that show. `E1_hat := {1, …, L1_hat}`. Same for season 2.

**This is an approximation, and it is specifically the shape Step 1 §3.1 forbids** — `F := L`, the
§3.3 fallback, adoptable "per show or at all **only by the Human Lead**." It is used here because
the request specified it and because nothing else is available. **It is not adopted, and no numbered
step may use it without the Human Lead saying so.**

### Direction of error

The request stated the direction as "it undercounts completers where no pooled user watched the
finale, and overcounts season length where a season 0 or special is misnumbered." **The first clause
runs the other way, and the correction matters because it is the larger of the two effects.** Stated
as computed:

| Mechanism | Effect on `L1_hat` | Effect on the completer count |
| :--- | :--- | :--- |
| **No pooled user reached the true finale** (S1 still airing, or a long/obscure season nobody finished) | `L1_hat` **too low** | **Over**counts. A short proxy season both lowers the `ceil(0.90 × L1)` bar and makes `F1_hat` an episode people actually reached, so users who stopped early are scored as completers. |
| **A special or mis-seasoned episode carries a high `number` inside season 1** | `L1_hat` **too high** | **Under**counts, and can drive a show to **zero** completers, because `F1_hat` is then an episode almost nobody watched. |
| Numbering gap in the real season | `E1_hat` readmits the missing number | Tightens the bar; **under**counts. Unmeasurable here — the gap hypothesis is still open in Step 1 §3.3. |

**The overcount mechanism dominates in this cohort**, because 38% of shows in the pool carry a
single user (`artifacts/pool-coverage-check.md` §4) and one user's stopping point sets the whole
season length. It is weakest exactly where most shows are, and the item 1 median below should be
read with that in mind. On the shows that carry the headline it is far better supported: on the
1,700 shows with ≥50 completers, at least 50 users independently reached `F1_hat`.

Two observable checks on the proxy, both counts only:

- **`L1_hat` on the 1,700 shows with ≥50 completers:** min 2, p25 8, **median 10**, p75 13, max 366.
  52 shows have `L1_hat ≤ 3`, 29 have `L1_hat > 30`. Spot values match known season lengths
  (Stranger Things 8, Game of Thrones 10, Breaking Bad 7, The Walking Dead 6, Black Mirror 3).
- **Still-airing risk.** Of those 1,700 shows, the proxy finale episode was first watched by the pool
  (10th percentile of first-watch dates) in **2026 for 39 shows** and **in 2025 or later for 127**.
  Those are the shows where `L1_hat` is most likely short.

---

## 3. Item 1 — S1 completers per show

Over the **41,576 shows with at least one S1 episode record**. 443,922 completer pairs in total.

| Statistic | Completers per show |
| :--- | ---: |
| Mean | 10.68 |
| **p25** | **1** |
| **Median** | **1** |
| **p75** | **5** |
| p90 | 18 |
| p95 | 41 |
| p99 | 184 |
| **Max** | **1,374** |

39,074 shows (94.0%) have ≥1 completer; **2,502 have zero.** Widening the denominator to all 41,964
shows with any S1 **or** S2 record moves nothing material (median 1, p75 5, mean 10.58).

The distribution is extremely long-tailed, and the median of 1 is a statement about the pool's long
tail of single-user shows, not about the shows this study can measure.

---

## 4. Item 2 — shows clearing each completer threshold

Over the same 41,576 shows.

| Threshold | Shows | Share of shows with any S1 |
| :--- | ---: | ---: |
| ≥1 completer | 39,074 | 94.0% |
| ≥10 | 6,640 | 16.0% |
| **≥25** | **3,246** | **7.8%** |
| **≥50** | **1,700** | **4.1%** |
| **≥100** | **824** | **2.0%** |
| ≥250 | 273 | 0.7% |

---

## 5. Item 3 — of the completers on shows with ≥50, how many have any S2 episode

**Headline, all 1,700 shows with ≥50 completers: 267,311 completers, of whom 167,015 have at least
one S2 episode — 62.5%.**

That number is structurally misleading on its own and must not be quoted without the split below.
**624 of the 1,700 shows have no season 2 in the data at all** — limited series and one-season
shows, where zero is arithmetic rather than behaviour. Chernobyl (909 completers) and WandaVision
(902) are in that group.

| | Shows | Completers | With ≥1 S2 episode | Share |
| :--- | ---: | ---: | ---: | ---: |
| All shows ≥50 completers | 1,700 | 267,311 | 167,015 | **62.5%** |
| — of which: **no S2 observed at all** | 624 | 75,872 | 0 | 0% by construction |
| — of which: **S2 observed** | **1,076** | **191,439** | **167,015** | **87.2%** |

Across the 1,076 shows that have an S2, the per-show share of completers with any S2 episode:

| p10 | p25 | Median | p75 | p90 | Min | Max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 70.1% | 82.0% | **90.4%** | 95.4% | 97.2% | 0.8% | 100% |

**Read this as a ceiling on "started S2," not as a measurement of it.** It carries no window, no
liveness filter, no contamination exclusion and no clock; a single S2 episode watched years later,
or backfilled at import, counts here.

---

## 6. Item 4 — restricted to shows whose S2 finished airing on or before 31 Dec 2025

### How the proxy was derived

No air dates are on disk. Substituted:

> **Proxy S2-finale air date := the earliest `watched_at` on the S2 finale episode
> (`number = L2_hat`, `season = 2`) across all 2,134 cohort users.** A show is in the restricted set
> when that instant is **before 2026-01-01T00:00:00Z** (Step 1 §2.4 half-open form).

Shows with **no S2 record at all are not in the restricted set** — with no S2 finale there is nothing
to date. That is not only a date filter: it removes all 624 one-season shows from item 3, which is
most of the jump from 62.5% to 87.6% below.

### Direction of error — two mechanisms, running opposite ways

1. **Late bias, structural.** Nobody watches an episode before it airs, so the earliest pooled watch
   is at or after the true air date. A show whose S2 finale aired in, say, November 2025 but which
   no pooled user watched until 2026 is **wrongly excluded**. This **undercounts** qualifying shows,
   and it bites hardest on obscure shows with few watchers.
2. **Early bias, from contamination, and it is large and measured.** A minimum is the single most
   fragile statistic against backfilled and epoch-zero timestamps. **1,856 of the 12,082 shows with
   an S2 (15.4%) have a pooled-minimum finale watch before 1990, and 1,446 sit at exactly
   1970-01-01.** Every one of the top ten shows by completers shows a 1970-01-01 minimum. Those
   shows are **wrongly included** if their S2 finale actually aired in 2026.

Within the 9,116,721 distinct S1/S2 episode rows in scope: **138,453 carry exactly 1970-01-01**,
**240,702 (2.64%) predate 1990**, and 6 have no `watched_at`.

**A robustness variant is reported alongside, not instead.** Replacing the minimum with the **10th
percentile** of the pooled first-watch dates of the S2 finale blunts mechanism 2 while keeping
mechanism 1. The two proxies disagree on **33 of 12,082 shows**, all in the same direction:

| Over 12,082 shows with any S2 | Shows |
| :--- | ---: |
| In the restricted set under **both** proxies | 11,542 |
| **Min only** — admitted by the minimum, rejected by p10 | 33 |
| p10 only | 0 |
| In neither | 507 |
| Of the "min only" shows: minimum predates 1990 **and** p10 falls in 2026 — an unambiguous false inclusion | **31** |

So the contamination is real and its effect on this boundary is bounded at **about 33 shows, 0.3% of
shows with an S2**. Fifteen percent of shows carry a corrupt minimum; almost all of them would have
qualified anyway.

### The three figures, restricted set

Primary column is the minimum proxy, as specified. The p10 column is the robustness variant.

**Restricted set size:** 11,575 shows (11,209 with S1 records) under the minimum; 11,542 (11,176)
under p10.

**Item 1 — completers per show, restricted:**

| Statistic | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| Shows | 11,209 | 11,176 |
| Total completers | 252,240 | 246,833 |
| Mean | 22.50 | 22.09 |
| p25 | 1 | 1 |
| **Median** | **3** | **3** |
| p75 | 10 | 10 |
| p90 | 46 | 45 |
| **Max** | **1,374** | 1,374 |

**Item 2 — thresholds, restricted:**

| Threshold | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| ≥1 | 10,753 | 10,720 |
| ≥10 | 2,943 | 2,911 |
| **≥25** | **1,747** | 1,716 |
| **≥50** | **1,060** | 1,034 |
| **≥100** | **588** | 570 |
| ≥250 | 221 | 211 |

**Item 3 — completers with any S2, on restricted shows with ≥50 completers:**

| | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| Shows | 1,060 | 1,034 |
| Completers | 189,379 | 184,180 |
| With ≥1 S2 episode | 165,898 | 162,545 |
| **Pooled share** | **87.6%** | **88.3%** |
| Per-show share, median | 90.6% | 90.8% |
| Per-show share, p25 / p75 | 82.1% / 95.4% | 82.9% / 95.5% |
| Per-show share, min / max | 29.6% / 100% | 29.6% / 100% |
| Shows with zero S2 completers | 0 | 0 |

A third variant, the minimum computed after discarding pre-1990 records, is in the JSON
(`item4_min_ge1990`: 1,043 shows ≥50, 87.9% pooled). It moves nothing and it is **worse**, not
better: it drops 216 shows whose only finale watches predate 1990, and some of those are genuinely
old shows that belong in the restricted set. Reported for completeness, not recommended.

The restricted set also drops the still-airing-S2 problem only partially: **42 of the 1,076 shows
with ≥50 completers and an observed S2 have an S2 finale-proxy p10 first-watch in 2026**, and 78 in
2025 or later.

---

## 7. What was done with the known anomalies

Per the brief, these are handled as needed for this diagnostic and **no general cleaning rule is
proposed or applied.** That is Step 5's, and Step 5 is an unapproved gate.

- **Epoch-zero and pre-1990 timestamps (138,453 and 240,702 distinct rows in scope).** **Not
  excluded from anything.** Items 1, 2 and 3 do not read timestamps at all — the §4 completion rule
  is pure set membership and "has any S2 episode" is a presence test — so those items are **immune
  to this anomaly by construction**, which is the cleanest available handling. Timestamps enter only
  in item 4's air-date proxy, and there the effect is **exposed with a second proxy and quantified**
  (§6) rather than corrected away.
- **6 records with no `watched_at`.** Retained as watched episodes for items 1–3: Step 1 §2.3
  conditions on whether the episode was viewed, not on whether the date is usable. Excluded from the
  item 4 proxy derivation, where an absent date carries no information. Six records against 9.1
  million cannot move any figure here.
- **Leftover duplicate page files for two users.** **They did not enter this diagnostic at all.**
  The parsed store is written only from the pages of an accepted sweep, and the scan confirmed
  **zero duplicate record `id`s across all 2,134 users**. Independently, the §2.1 distinct-episode
  collapse — which removed 998,909 duplicate plays, 9.87% — would have made them inert regardless.
- **Bulk-import contamination generally, and TV Time.** Untouched. No account was flagged, excluded
  or down-weighted. Every figure above includes whatever backfill is in the data.

---

## 8. Limits

1. **Partial pull.** 2,134 of 4,050 planned users, 53%. Absolute counts will grow; the ≥25/≥50/≥100
   show counts are floors on this snapshot and nothing else.
2. **The season-length proxy is the dominant uncertainty** and it is not signed at the pool level
   (§2). Every completer count is proxy-dependent. Nothing here survives contact with a real Step 2
   frame unchanged.
3. **No contamination adjustment.** The Step 5 gate is not approved and nothing was excluded.
4. **No frame, no window, no liveness, no outcome states, no `τ_pull`.** "Has any S2 episode" is a
   presence count, not "Started," and the 87.6% in §6 is not an abandonment result of any kind.
5. **The 38 over-cap users are the pool's heaviest trackers** and are absent by rule, which depresses
   the tail of both the per-show completer count and the show count at every threshold.
6. **Selection.** The pool comes from a follower-graph and list-owner crawl (Step 3), not from a
   probability sample of Trakt users.

---

## 9. Files

| File | Contents |
| :--- | :--- |
| `artifacts/s1-completer-diagnostic.md` | this file. Counts and aggregates only |
| `processed/s1-completer-diagnostic-per-show.csv` | 41,964 rows, one per show: proxy season lengths, completers, completers with any S2, both date proxies. No user identifiers |
| `processed/s1-completer-diagnostic-summary.json` | every figure above, machine-readable |
| `processed/s1s2_scan.npz` | the S1/S2 record extract the analysis runs on |
| `src/diag_s1_completers_scan.py`, `src/diag_s1_completers.py` | the two scripts, re-runnable at zero API cost |
