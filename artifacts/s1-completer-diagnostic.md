# S1-completer diagnostic — full pulled pool

**What this is:** a read-only diagnostic requested by the Human Lead. It is **not a numbered step,
not a gate, and not Step 9.** Nothing here is a proposal, no rule is adopted, and no exclusion,
window, liveness or outcome-state logic is applied.

**This supersedes the 2,134-user snapshot** of the same name (git history, commit prior to this one).
It re-runs the identical scripts on the **full pulled pool of 2,549 users** now that the Step 4 pull
has stopped, per `decisions/0013` condition 2: *pull completes → completer diagnostic re-runs on the
full pool → frame is built off stable counts.* Nothing about the method changed. §1.1 carries the
before/after delta.

**API calls made: zero.** Every number comes from files already on disk. No network request was
issued at any point.

**Aggregates and counts only.** No usernames, user IDs, or individual watch histories appear in this
file. Per-show detail is at `processed/s1-completer-diagnostic-per-show.csv` (git-ignored), which
also carries no user identifiers. Show titles are public catalogue metadata.

**Reproducible at zero API cost:** `src/diag_s1_completers_scan.py` then `src/diag_s1_completers.py`.
Full machine-readable output: `processed/s1-completer-diagnostic-summary.json`. The superseded
2,134-user outputs are preserved at `processed/diag_snapshot_2134u/`.

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

The Step 4 pull is **stopped and not running**, at 2,836 of 4,050 planned users decided
(`logs/step4_progress.json`, `finished: false`, `abnormal_stop: false`).

This diagnostic uses the **2,549 `complete` users** in `processed/step4/parsed/`. That is the
rule-conformant cohort: under `decisions/0012`, the **287** `discarded_over_tolerance` users have
their pages **discarded rather than returned as data**, and no parsed file is written for them. The
**38** users over the page-forecast cap and the **1,214** never-attempted users have no history on
disk. All of these are **absent, not empty**, and appear in no denominator here.

### Ledger reconciliation

The ledger carries 2,884 rows against 2,549 parsed files. It reconciles exactly, and nothing is
missing:

| | |
| :--- | ---: |
| Ledger rows | 2,884 |
| — `complete` rows | 2,552 |
| — `complete` **distinct users** | **2,549** |
| — `discarded_over_tolerance` | 287 |
| — `skipped_length_forecast` (over-cap, outside the 4,050 plan) | 38 |
| — `error_short_read` | 7 |
| Parsed files on disk | 2,549 |
| `complete` users with no file, or files with no `complete` row | **0** |

The 7 `error_short_read` users were each **retried and later completed** — they are in the 2,549, not
lost. Three further slugs carry two `complete` rows from a re-attempt; the parsed store keeps one
file per user, and the scan independently confirms **zero duplicate record IDs across all 2,549
users**, so no user is double-counted.

### The prefix is proportional across strata

`decisions/0009` ordered the pull so that an early stop yields a proportional prefix rather than a
biased one. It held. Bins are the ten history-volume strata; `med plays` is the median
`history_plays_reported` in the bin, so bin 0 is the lightest trackers and bin 9 the heaviest.

| Bin | Med. plays | Planned | Complete | Discarded | Undecided | Decided share | Complete share |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 616 | 405 | 264 | 20 | 121 | 70.1% | 65.2% |
| 1 | 2,368 | 405 | 257 | 27 | 121 | 70.1% | 63.5% |
| 2 | 4,052 | 405 | 250 | 34 | 121 | 70.1% | 61.7% |
| 3 | 5,804 | 405 | 254 | 30 | 121 | 70.1% | 62.7% |
| 4 | 7,840 | 405 | 258 | 26 | 121 | 70.1% | 63.7% |
| 5 | 9,971 | 405 | 240 | 44 | 121 | 70.1% | 59.3% |
| 6 | 12,433 | 405 | 253 | 31 | 121 | 70.1% | 62.5% |
| 7 | 15,970 | 405 | 265 | 18 | 122 | 69.9% | 65.4% |
| 8 | 21,357 | 405 | 261 | 22 | 122 | 69.9% | 64.4% |
| 9 | 35,336 | 405 | 247 | 35 | 123 | 69.6% | 61.0% |

**The stop itself is essentially perfectly proportional** — decided share runs 69.6% to 70.1% across
all ten strata. **The analysed cohort is proportional but not perfectly so**, because the discard
rate under `decisions/0012` varies by stratum: complete share runs from **59.3% (bin 5) to 65.4%
(bin 7)**, a 6.1-point spread. That is a property of the tolerance rule, not of the stop, and it was
present at any stopping point. It is small, it is not monotone in history volume, and it is stated
here so that no downstream step has to rediscover it.

### Scale

| | Count |
| :--- | ---: |
| Users | 2,549 |
| S1 + S2 episode records read | 12,323,972 |
| Distinct `(user, show, season, number)` after the §2.1/§2.2 collapse | 11,115,060 |
| Collapsed away as duplicate plays | 1,208,912 (9.81%) |
| Shows with ≥1 S1 record | 44,617 |
| Shows with ≥1 S2 record | 13,037 |
| User–show pairs with ≥1 S1 episode | 717,323 |
| **User–show pairs meeting the §4 S1-completion rule** | **537,471** (74.9% of the above) |

### 1.1 What changed against the 2,134-user snapshot

| | 2,134 users | 2,549 users | Change |
| :--- | ---: | ---: | ---: |
| Users | 2,134 | 2,549 | +19.4% |
| Distinct S1/S2 episode rows | 9,116,721 | 11,115,060 | +21.9% |
| Shows with ≥1 S1 record | 41,576 | 44,617 | +7.3% |
| S1-completer pairs | 443,922 | 537,471 | +21.1% |
| **Shows with ≥50 completers** | **1,700** | **2,094** | **+23.2%** |
| Shows with ≥25 completers | 3,246 | 3,793 | +16.9% |
| Shows with ≥100 completers | 824 | 1,038 | +26.0% |
| Item 3 pooled share, all ≥50 shows | 62.5% | 61.3% | −1.2 pt |
| Item 3 pooled share, restricted (min proxy) | 87.6% | 87.3% | −0.3 pt |

**The candidate set grew and nothing left it.** Of the 1,700 shows at ≥50 completers in the earlier
run, **all 1,700 are still at ≥50**, and **394 shows newly crossed**. Zero dropped out.

### 1.2 Correction — completer counts do not *only* rise

`decisions/0013` condition 2 reasons that "completer counts only rise" as the pool grows. **That is
not strictly true, and the mechanism is worth naming**, because it is the same proxy defect §2
describes. Adding users can raise `L1_hat` for a show, which both raises the `ceil(0.90 × L1)` bar
and moves `F1_hat` to an episode the earlier users had not watched — retroactively **un-completing**
them.

Measured over the 41,964 shows present in both runs:

| | |
| :--- | ---: |
| Shows whose completer count **fell** | **118** |
| — of those, shows whose `L1_hat` rose | 118 (all of them) |
| Total completer pairs lost | 177 |
| Shows at ≥50 completers now whose `L1_hat` rose since the earlier run | **0** |

The largest single drop is a show going from 22 completers to 1 when `L1_hat` moved 5 → 6. **Every
affected show is in the long tail** — the ≥50 set is untouched, which is why the candidate set is
monotone in practice even though the statistic is not monotone in principle.

**This does not disturb 0013's conclusion.** The instruction to recompute on the full pool was
correct, and it is now done. What changes is the reason: the recompute is needed because counts
**move**, not because they only rise. Both directions matter once a threshold is drawn on them.

---

## 2. The season-length proxy, and its direction of error

No Step 2 frame exists, so `E1` and `E2` have no real source. **Substituted, for this diagnostic
only:**

> `L1_hat := F1_hat :=` the **maximum S1 episode number observed across all 2,549 cohort users** for
> that show. `E1_hat := {1, …, L1_hat}`. Same for season 2.

**This is an approximation, and it is specifically the shape Step 1 §3.1 forbids** — `F := L`, the
§3.3 fallback, adoptable "per show or at all **only by the Human Lead**." It is used here because
the request specified it and because nothing else is available. **It is not adopted, and no numbered
step may use it without the Human Lead saying so.** §1.2 above is a direct measurement of this
proxy's instability.

### Direction of error

| Mechanism | Effect on `L1_hat` | Effect on the completer count |
| :--- | :--- | :--- |
| **No pooled user reached the true finale** (S1 still airing, or a long/obscure season nobody finished) | `L1_hat` **too low** | **Over**counts. A short proxy season both lowers the `ceil(0.90 × L1)` bar and makes `F1_hat` an episode people actually reached, so users who stopped early are scored as completers. |
| **A special or mis-seasoned episode carries a high `number` inside season 1** | `L1_hat` **too high** | **Under**counts, and can drive a show to **zero** completers, because `F1_hat` is then an episode almost nobody watched. |
| Numbering gap in the real season | `E1_hat` readmits the missing number | Tightens the bar; **under**counts. Unmeasurable here — the gap hypothesis is still open in Step 1 §3.3. |

**The overcount mechanism dominates in this cohort**, because **37.6% of shows with any S1 record
carry a single user** and 51.7% carry two or fewer; one user's stopping point then sets the whole
season length. It is weakest exactly where most shows are, and the item 1 median below should be
read with that in mind. On the shows that carry the headline it is far better supported: on the
2,094 shows with ≥50 completers, at least 50 users independently reached `F1_hat`.

Two observable checks on the proxy, both counts only:

- **`L1_hat` on the 2,094 shows with ≥50 completers:** min 1, p25 8, **median 10**, p75 13, max 366.
  76 shows have `L1_hat ≤ 3`, 40 have `L1_hat > 30`. Spot values match known season lengths
  (Stranger Things 8, Game of Thrones 10, Breaking Bad 7, The Walking Dead 6, Black Mirror 3).
  The single `L1_hat = 1` show is Æon Flux (1991), whose first season is a run of dialogue-free
  shorts — plausible as data, and exactly the shape a structural field in Step 2 would want to see.
- **Still-airing risk.** Of those 2,094 shows, the proxy finale episode was first watched by the pool
  (10th percentile of first-watch dates) in **2026 for 51 shows** and **in 2025 or later for 162**.
  Those are the shows where `L1_hat` is most likely short.

---

## 3. Item 1 — S1 completers per show

Over the **44,617 shows with at least one S1 episode record**. 537,471 completer pairs in total.

| Statistic | Completers per show |
| :--- | ---: |
| Mean | 12.05 |
| **p25** | **1** |
| **Median** | **2** |
| **p75** | **5** |
| p90 | 20 |
| p95 | 46 |
| p99 | 208 |
| **Max** | **1,662** |

41,970 shows (94.1%) have ≥1 completer; **2,647 have zero.** Widening the denominator to all 45,015
shows with any S1 **or** S2 record moves nothing material (median 1, p75 5, mean 11.94).

The distribution is extremely long-tailed. The median moved 1 → 2 on the larger pool, which is a
statement about the pool's long tail of single-user shows, not about the shows this study can
measure.

---

## 4. Item 2 — shows clearing each completer threshold

Over the same 44,617 shows.

| Threshold | Shows | Share of shows with any S1 | (2,134-user run) |
| :--- | ---: | ---: | ---: |
| ≥1 completer | 41,970 | 94.1% | 39,074 |
| ≥10 | 7,643 | 17.1% | 6,640 |
| **≥25** | **3,793** | **8.5%** | 3,246 |
| **≥50** | **2,094** | **4.7%** | 1,700 |
| **≥100** | **1,038** | **2.3%** | 824 |
| ≥250 | 361 | 0.8% | 273 |

---

## 5. Item 3 — of the completers on shows with ≥50, how many have any S2 episode

**Headline, all 2,094 shows with ≥50 completers: 343,599 completers, of whom 210,681 have at least
one S2 episode — 61.3%.**

That number is structurally misleading on its own and must not be quoted without the split below.
**817 of the 2,094 shows have no season 2 in the data at all** — limited series and one-season
shows, where zero is arithmetic rather than behaviour. Chernobyl (1,084 completers) and WandaVision
(1,073) are in that group.

| | Shows | Completers | With ≥1 S2 episode | Share |
| :--- | ---: | ---: | ---: | ---: |
| All shows ≥50 completers | 2,094 | 343,599 | 210,681 | **61.3%** |
| — of which: **no S2 observed at all** | 817 | 101,299 | 0 | 0% by construction |
| — of which: **S2 observed** | **1,277** | **242,300** | **210,681** | **87.0%** |

Across the 1,277 shows that have an S2, the per-show share of completers with any S2 episode:

| p10 | p25 | Median | p75 | p90 | Min | Max |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 69.5% | 81.0% | **90.4%** | 95.3% | 97.3% | 0.4% | 100% |

**Read this as a ceiling on "started S2," not as a measurement of it.** It carries no window, no
liveness filter, no contamination exclusion and no clock; a single S2 episode watched years later,
or backfilled at import, counts here.

---

## 6. Item 4 — restricted to shows whose S2 finished airing on or before 31 Dec 2025

### How the proxy was derived

No air dates are on disk. Substituted:

> **Proxy S2-finale air date := the earliest `watched_at` on the S2 finale episode
> (`number = L2_hat`, `season = 2`) across all 2,549 cohort users.** A show is in the restricted set
> when that instant is **before 2026-01-01T00:00:00Z** (Step 1 §2.4 half-open form).

Shows with **no S2 record at all are not in the restricted set** — with no S2 finale there is nothing
to date. That is not only a date filter: it removes all 817 one-season shows from item 3, which is
most of the jump from 61.3% to 87.3% below.

### Direction of error — two mechanisms, running opposite ways

1. **Late bias, structural.** Nobody watches an episode before it airs, so the earliest pooled watch
   is at or after the true air date. A show whose S2 finale aired in, say, November 2025 but which
   no pooled user watched until 2026 is **wrongly excluded**. This **undercounts** qualifying shows,
   and it bites hardest on obscure shows with few watchers.
2. **Early bias, from contamination, and it is large and measured.** A minimum is the single most
   fragile statistic against backfilled and epoch-zero timestamps. **2,167 of the 13,037 shows with
   an S2 (16.6%) have a pooled-minimum finale watch before 1990, and 1,649 sit at exactly
   1970-01-01.** Every one of the top ten shows by completers shows a 1970-01-01 minimum. Those
   shows are **wrongly included** if their S2 finale actually aired in 2026.

Within the 11,115,060 distinct S1/S2 episode rows in scope: **173,326 carry exactly 1970-01-01**,
**307,726 (2.77%) predate 1990**, and 6 have no `watched_at`.

**A robustness variant is reported alongside, not instead.** Replacing the minimum with the **10th
percentile** of the pooled first-watch dates of the S2 finale blunts mechanism 2 while keeping
mechanism 1. The two proxies disagree on **34 of 13,037 shows**, all in the same direction:

| Over 13,037 shows with any S2 | Shows |
| :--- | ---: |
| In the restricted set under **both** proxies | 12,455 |
| **Min only** — admitted by the minimum, rejected by p10 | 34 |
| p10 only | 0 |
| In neither | 548 |
| Of the "min only" shows: minimum predates 1990 **and** p10 falls in 2026 — an unambiguous false inclusion | **34** |

So the contamination is real and its effect on this boundary is bounded at **34 shows, 0.3% of shows
with an S2**. Sixteen percent of shows carry a corrupt minimum; almost all of them would have
qualified anyway. On the larger pool every "min only" show is now an unambiguous false inclusion
(34 of 34, against 31 of 33 before).

### The three figures, restricted set

Primary column is the minimum proxy, as specified. The p10 column is the robustness variant.

**Restricted set size:** 12,489 shows (12,114 with S1 records) under the minimum; 12,455 (12,080)
under p10.

**Item 1 — completers per show, restricted:**

| Statistic | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| Shows | 12,114 | 12,080 |
| Total completers | 306,786 | 300,085 |
| Mean | 25.33 | 24.84 |
| p25 | 1 | 1 |
| **Median** | **3** | **3** |
| p75 | 11 | 11 |
| p90 | 52 | 51 |
| **Max** | **1,662** | 1,662 |

**Item 2 — thresholds, restricted:**

| Threshold | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| ≥1 | 11,640 | 11,606 |
| ≥10 | 3,286 | 3,252 |
| **≥25** | **1,973** | 1,939 |
| **≥50** | **1,258** | 1,228 |
| **≥100** | **723** | 703 |
| ≥250 | 285 | 275 |

**Item 3 — completers with any S2, on restricted shows with ≥50 completers:**

| | Min proxy | p10 proxy |
| :--- | ---: | ---: |
| Shows | 1,258 | 1,228 |
| Completers | 239,842 | 233,276 |
| With ≥1 S2 episode | 209,418 | 205,150 |
| **Pooled share** | **87.3%** | **87.9%** |
| Per-show share, median | 90.5% | 90.8% |
| Per-show share, p25 / p75 | 81.4% / 95.3% | 82.2% / 95.4% |
| Per-show share, min / max | 0.4% / 100% | 0.4% / 100% |
| Shows with zero S2 completers | 0 | 0 |

A third variant, the minimum computed after discarding pre-1990 records, is in the JSON
(`item4_min_ge1990`: 1,239 shows ≥50, 87.6% pooled). It moves nothing and it is **worse**, not
better: it drops 247 shows whose only finale watches predate 1990, and some of those are genuinely
old shows that belong in the restricted set. Reported for completeness, not recommended.

The restricted set also drops the still-airing-S2 problem only partially: **49 of the 1,277 shows
with ≥50 completers and an observed S2 have an S2 finale-proxy p10 first-watch in 2026**, and 90 in
2025 or later.

---

## 7. What was done with the known anomalies

Per the brief, these are handled as needed for this diagnostic and **no general cleaning rule is
proposed or applied.** That is Step 5's, and Step 5 is an unapproved gate.

- **Epoch-zero and pre-1990 timestamps (173,326 and 307,726 distinct rows in scope).** **Not
  excluded from anything.** Items 1, 2 and 3 do not read timestamps at all — the §4 completion rule
  is pure set membership and "has any S2 episode" is a presence test — so those items are **immune
  to this anomaly by construction**, which is the cleanest available handling. Timestamps enter only
  in item 4's air-date proxy, and there the effect is **exposed with a second proxy and quantified**
  (§6) rather than corrected away.
- **6 records with no `watched_at`.** Retained as watched episodes for items 1–3: Step 1 §2.3
  conditions on whether the episode was viewed, not on whether the date is usable. Excluded from the
  item 4 proxy derivation, where an absent date carries no information. Six records against 11.1
  million cannot move any figure here.
- **Re-attempted users.** Ten users carry two ledger rows (seven retried from `error_short_read`,
  three re-attempted after a `complete`). The parsed store holds **one file per user**, and the scan
  confirms **zero duplicate record `id`s across all 2,549 users**. Independently, the §2.1
  distinct-episode collapse — which removed 1,208,912 duplicate plays, 9.81% — would have made any
  leftover inert regardless.
- **Bulk-import contamination generally, and TV Time.** Untouched. No account was flagged, excluded
  or down-weighted. Every figure above includes whatever backfill is in the data.

---

## 8. Limits

1. **The pull is stopped short, not complete.** 2,549 of 4,050 planned users, 62.9%; 2,836 decided,
   70.0%. The stop is proportional across all ten strata (§1), so these are not a biased subsample in
   the way an unordered prefix would be — but they are still a subsample, and absolute counts will
   grow if the pull resumes.
2. **The analysed cohort is proportional to within 6.1 points, not exactly** (§1). The
   `decisions/0012` discard rate varies by history-volume stratum.
3. **The season-length proxy is the dominant uncertainty** and it is not signed at the pool level
   (§2). §1.2 measures it moving counts in both directions between runs. Every completer count is
   proxy-dependent. Nothing here survives contact with a real Step 2 frame unchanged.
4. **No contamination adjustment.** The Step 5 gate is not approved and nothing was excluded.
5. **No frame, no window, no liveness, no outcome states, no `τ_pull`.** "Has any S2 episode" is a
   presence count, not "Started," and the 87.3% in §6 is not an abandonment result of any kind.
6. **The 38 over-cap users are the pool's heaviest trackers** and are absent by rule, which depresses
   the tail of both the per-show completer count and the show count at every threshold.
7. **Selection.** The pool comes from a follower-graph and list-owner crawl (Step 3), not from a
   probability sample of Trakt users.
8. **2,797 shows in the scan have no title** in the join source, which was built on the earlier pool.
   All are long-tail shows new to this run; **all 2,094 shows at ≥50 completers have titles**, so no
   candidate-set row is affected. Counts never depend on the join.

---

## 9. Files

| File | Contents |
| :--- | :--- |
| `artifacts/s1-completer-diagnostic.md` | this file. Counts and aggregates only |
| `processed/s1-completer-diagnostic-per-show.csv` | 45,015 rows, one per show: proxy season lengths, completers, completers with any S2, both date proxies. No user identifiers |
| `processed/s1-completer-diagnostic-summary.json` | every figure above, machine-readable |
| `processed/s1s2_scan.npz` | the S1/S2 record extract the analysis runs on |
| `processed/diag_snapshot_2134u/` | the superseded 2,134-user outputs, kept for the §1.1 diff |
| `src/diag_s1_completers_scan.py`, `src/diag_s1_completers.py` | the two scripts, re-runnable at zero API cost |
