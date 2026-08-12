---
name: population-chain-steps-2-3-4
description: The reconciled number chain from Step 3's 4,088 discovered users through Step 4's deliberately stopped pull to Step 2's 1,138-show frame and 220,107 pairs — every identity checked, and which cohort figures are superseded
metadata:
  type: project
---

# The population chain — every number a result rests on

**Why this file exists:** four steps each produced a cohort figure, several figures were restated as
the pull progressed, and the same quantity appears with different values in different artifacts
because they were written at different moments. This is the reconciled chain, current 2026-08-12,
with the superseded values named so they are not quoted as current.

**How to apply:** before using any user or pair count, check it against the chain below and against
the date of the artifact it came from.

## The chain

| Stage | Count | Source |
| :--- | ---: | :--- |
| Users discovered (Step 3) | 5,694 | `artifacts/step3-user-discovery.md` |
| — private | 347 | |
| — eligible | 5,347 | |
| — screened (FIFO, 120/round) | 4,320 | **1,027 eligible were never screened** |
| — rejected by `MIN_EPISODES_USABLE = 10` | 232 | the only rejection reason; `access_denied` 0 |
| **Usable pool** | **4,088** | 2,306 Channel A / 1,782 Channel B |
| — over the 300-page forecast cap, never started (`0010`) | 38 | the pool's heaviest trackers |
| **Step 4 plan** | **4,050** | |
| **Decided before the stop** | **2,836 (70.0%)** | |
| — `discarded_over_tolerance` (`0012`) | 287 | pages kept in `raw/`, **not returned as data** |
| — **`complete`** | **2,549 (62.9% of plan)** | the analysable cohort |
| **Never attempted** | 1,214 | |
| **Absent, not empty** | **1,539** = 287 + 38 + 1,214 | 2,549 + 1,539 = 4,088 ✓ |

**The pull was stopped deliberately.** `logs/step4_progress.json`: `finished: false`,
`abnormal_stop: false`. Not a failure.

## From users to pairs

| Stage | Count |
| :--- | ---: |
| S1 + S2 episode records read (2,549 users) | 12,323,972 |
| Distinct `(user, show, season, number)` after the §2.1/§2.2 collapse | 11,115,060 |
| Collapsed away as duplicate plays | 1,208,912 (**9.81%**) |
| Shows with ≥1 S1 record | 44,617 |
| User–show pairs with ≥1 S1 episode | 717,323 |
| **Pairs meeting the §4 S1-completion rule** | **537,471 (74.9%)** |
| **Shows with ≥50 completers — the candidate set** | **2,094** |
| **Step 2 frame** | **1,138 shows, 220,107 pairs** |
| Step 5 **analysis population** — APPROVED, `0021` | **201,900** |
| Step 5 **W estimation sample** — APPROVED, `0021` | **128,099** |

| Step 6 **C1 estimation subset** = C1 ∩ 128,099 (`0026`) | **25,120** — 206 shows, 2,050 users |

**201,900 and 128,099 are different numbers and `task-sheet.md` Step 6 now says so explicitly**
(`0022`). The analysis population is what Step 8 classifies; the estimation sample is what Step 6
measures `W` on, with D14's C1 restriction applied **on top of** it, not instead of it — 19.6% of
the sample. Both Step 6 instances **asserted** the full waterfall before computing and aborted on
mismatch; both reproduced all five lines exactly, and both independently recomputed the D12
classifier against the frame at **0 disagreements over 1,138 shows**.

**Pairs in the 128,099 by D12 bucket**, from both Step 6 instances, identical:
C0 **0** · C1 **25,120** · C2 **39,680** · C3 **18,218** · C4 **45,081**. Sums to 128,099 ✓.

**Four pairs in the 128,099 have a first S2 record at or after `τ_pull`** and are retained, because
Step 5 built the sample without D11's filter and the Step 6 spec directs taking the population as
published. **None is in C1.** Step 8 applies the frozen cutoff, so **Step 6 and Step 8 will not
share a row set** — README item 27, open.

## The 287 discarded users — measured, and not outcome-neutral

Their raw pages were never deleted (14,578 page files, all 287 users present), so
`artifacts/step5-discard-outcome-neutrality.md` could measure them at **zero API calls**:

| | Discarded (287) | Retained (2,549) |
| :--- | ---: | ---: |
| Completer pairs | **25,035** | **220,107** |
| Mean completers per user | 87.23 | 87.34 |
| Median | 64.0 | 71.0 |
| Users with zero completers | 5 | 62 |
| **Has-any-S2 rate** | **89.78%** | **88.52%** |

**+1.27 points, CI [0.87, 1.66], p < 0.001. Pooled effect 0.13 points** — the 287 carry 10.2% of
the combined pair pool. Direction **up** on the never-started share.

**Two method facts that make the comparison trustworthy**, both worth keeping because a difference
here could easily have been an artifact of reading from two different stores:

1. **The two extractors were cross-validated on shared users** — running the raw extractor over
   retained users, who have both a raw cache and a parsed file, gave **exact agreement on every user
   checked**: zero raw-only records, zero parsed-only, on sets up to 9,273 triples.
2. **The retained population reproduces 220,107 completer pairs exactly, by an independent path.**
   That is the strongest single confirmation the frame count has received.

**One denominator caveat, stated in the artifact and easy to lose:** the retained *per-user*
statistics are over **2,520 users, not 2,549** — 29 retained users carry no S1 or S2 record on any
in-frame show. Adding them as zeros moves the comparison **toward greater similarity**, not less.
The pair-level rates are unaffected; their denominator is pairs.

## The prefix is proportional — `0009` held, with one caveat

`0009` ordered the pull in stratified round-robin so an early stop leaves a proportional prefix.
Over the ten history-volume bins:

- **The stop itself is essentially perfectly proportional** — decided share runs **69.6% to 70.1%**
  across all ten strata.
- **The analysed cohort is proportional only to within 6.1 points** — `complete` share runs **59.3%
  (bin 5) to 65.4% (bin 7)**, because the **`0012` discard rate varies by stratum**. That is a
  property of the tolerance rule, not of the stop, and it was present at any stopping point.

**Proportional is not unbiased.** A prefix is proportional on **forecast page count and nothing
else**. It carries the seeding bias (`0008`), the liveness exclusion, and the fact that the pool is
a convenience sample. Any early-stop result is a **prefix of a biased pool, not a sample of Trakt.**

## Superseded cohort figures — do not quote as current

| Figure | Where it still appears | Superseded by |
| :--- | :--- | :--- |
| **2,134 `complete`, 235 discarded, 2,370 contributing, "58% of the pool"** | `artifacts/pool-coverage-check.md` throughout — **not marked superseded** | 2,549 / 287 / 62.9% |
| **1,700 shows at ≥50 completers**, 443,922 completer pairs | the 2,134-user S1-completer diagnostic, preserved at `processed/diag_snapshot_2134u/` | 2,094 shows, 537,471 pairs — the artifact **explicitly supersedes itself**, which is the right handling |
| **Frame 2,094 candidates → 1,226 → 1,138** | `0018` still publishes 1,226-frame quintile bins | `0020` cut it to 1,138 the same day |
| Step 4 cost **~86,000 calls** | — | **~210,500 calls / 23.4 h**; the old figure divided `total_plays`, absent from 77% of stats bodies |

## Identities checked — PASS, do not re-derive

- Step 4 ledger: 2,552 `complete` rows (2,549 distinct users) + 287 + 38 + 7 `error_short_read` =
  **2,884 rows**. The 7 short-reads were each **retried and completed** — they are inside the 2,549.
  Three slugs carry two `complete` rows; **zero duplicate record IDs across all 2,549 users.**
- Step 2 ledger: 2,094 − 796 − 12 − 60 − 51 − 37 = **1,138** ✓. API calls 2,094 + 1,226 = **3,320**,
  0 errors, 0 429s, peak **150** requests in any rolling 60 s window, verified against the persisted
  throttle ring rather than asserted. (The run's own `shows_per_min` counter read as high as 318 —
  a cumulative-average artifact of a front-loaded limiter window, **not** a breach.)
- Every Step 2 distribution sums to 1,138: cadence 206+340+167+425; air period 757+213+168; size
  quintile 238+221+224+227+228; S1 size buckets 13+139+188+298+236+167+97; S2 size buckets
  5+115+187+272+229+222+108; gap buckets 1+36+225+134+293+230+119+100. All ✓.
- Air-period × cadence cross-tab reconciles on both margins ✓.
- Step 5: binding terms 116,041 + 103,898 + 168 = **220,107** ✓. Pairs with no S2 evidence
  220,107 − 194,830 = **25,277** ✓. 194,830 − 16,665 = **178,165** ✓. 25,277 − 1,542 = **23,735**,
  matching the waterfall drop ✓. 220,107 − 18,207 = **201,900 = 91.73%** ✓.
  Net population change 16,665 − 1,542 = **15,123 up** ✓. Floor guarantee 4,988 + 3,384 = **8,372**
  ✓, against 42,019 assumed.
- Step 5 §4 action table (`watch` 22,597,404 + `checkin` 1,133,846 + `scrobble` 3,234,228 =
  26,965,478) is the record store **minus corrupt and undated**: 26,965,478 + 690,774 + 379 =
  **27,656,631** exactly. The basis is not stated in the table but the arithmetic is coherent.
- TV Time: 3,115,531 / 27,656,631 = 11.3% (the **wave**); excess 3,115,531 − 174,000 = 2,941,531 =
  **10.6%** (the **store**). Both figures now attached to the right quantity — round 4's correction
  is applied.
- The 720's sub-rows reconcile to the **corrected** bound: 425 × 13.4% ≈ 57 ≈ 720 × 7.92%.
  `processed/step5/revision4.json` was regenerated and carries 1,738 / 1,717 / 1,762, so §16's
  routing of those figures to `revision4.json` is **correct**, not stale. Checked directly.

## Two structural facts about this pool that do not go away

1. **Coverage is thin almost everywhere.** 38.3% of the 44,866 shows on disk carry exactly one
   user; 65.8% carry fewer than five. Concentration: the top 1,000 shows hold 46.1% of user–show
   pairs. The ≥50-completer bar is what makes the frame measurable.
2. **The frame is systematically older than the catalogue** — **66.5% of in-frame shows have an S2
   finale before 2020**, a direct consequence of the 2025-12-31 cutoff plus the ≥50-completer bar.
   The Human Lead's Step 5 ruling cites "69 percent of pairs are pre-2020" — a **pairs** base, not
   the shows base; the two are different numbers and both are right.

Related: [[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[gate-step5-contamination]], [[decision-log-step18]].
