> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — liveness threshold and rule (run tag `ds_run_1254`)

**Status: PROPOSED. This is a gate. The producing agent has not adopted it.**

**Namespace collision — read first.** During this run a second process wrote into
`processed/step7/a/` and into `src/step7_*_a.py`, overwrote one of this run's intermediate
tables, and overwrote `artifacts/step7-gap-distribution-a.png`. This run's own deliverables were
therefore moved to run-tagged filenames and the shared `-a` names were vacated. Every number below
was regenerated end to end by the single file `src/step7_a_run1254.py`, whose only outputs are
`processed/step7/a/_snapshot_ds_run_1254/` and the `-a-run1254` artifacts. **Establish which run
produced which file before diffing the two dual-implementation arms.** No number in this document
was read from any other run.

**Zero API calls.** Everything ran off `processed/step5/full_scan.npz`, the stored calibration
curve, and `processed/step5/pair_revision5.csv`.

---

## 1. Inputs, asserted not assumed

| | |
| :--- | ---: |
| Records scanned | 27,656,813 |
| — episode records | 24,893,556 |
| — movie records | 2,763,257 |
| Accounts in the scan | 2,549 |
| Step 5 waterfall reproduced | 201,900 → 178,165 → 155,131 → 152,126 → 128,099 |
| Match against the published waterfall | exact, asserted in code |

Insertion instant = `np.interp(rid, knot_rid, knot_time)` against `processed/step5/calibration.npz`.
**The curve was read, never refitted.** 6,956 records (0.025%) have a `rid` outside the knot range
and are clamped to the endpoint value by `np.interp`.

Evidence is **account-wide**: all records on the account, movies included, all actions
(watch, checkin, scrobble), no restriction to the show under study.

## 2. The gap distribution

Gap = the **continuous** difference between **consecutive insertion instants** on one account.
Not claimed `watched_at` (`0021`). Not floored to whole days before the percentile (`0029`).

27,654,264 gaps across 2,549 accounts.

| percentile | gap (days) |
| ---: | ---: |
| 50 | 0.0000006 |
| 75 | 0.0198 |
| 90 | 0.3373 |
| 95 | 0.9118 |
| **99** | **3.1606** |
| 99.5 | 5.5967 |
| 99.9 | 18.3418 |
| max | 3196.27 |

96.1% of gaps are under one day and **59.3% are under one second**, because Trakt writes records in
insert batches.

Chart: `artifacts/step7-gap-distribution-a-run1254.png` — (a) survival of the pooled gaps,
(b) the sub-30-day mass with the percentile and the ceiling marked, (c) the pooled distribution
against the bracketing gap the rule actually tests, (d) live share against threshold.

## 3. The threshold

99th percentile = **3.1606 days**, ceiling → **THRESHOLD = 4 DAYS**.

Percentile rule from `0036`; ceiling from `0025`; continuous instants from `0029`. Derived with
no input from `W`.

## 4. The rule

> A **user-show pair** counts as **live** if, on that pair's own clock, the account has an insertion
> instant at or before `τ1 = ⟦T0⟧ + 108 × 24h` and an insertion instant after `τ1`, and the gap
> between those two adjacent instants is **strictly less than 4 days**.
>
> Evidence is **account-wide**. The test is **pair-level**, because `τ1` is pair-specific: one
> account can be live for one show and not live for another, and **no user is ever dropped
> wholesale**. Insertion instants only. Anchored at `τ1`; `τ2` plays no part. **Exactly one gap is
> tested** — the one bracketing `τ1` — never every gap in the sweep.
>
> **No insertion instant after `τ1`** → the gap is open-ended → **not live**.
> **No insertion instant at or before `τ1`** → no pre-`τ1` evidence → **not live**.

## 5. Counts

**Primary population: the Step 5 analysis population, 201,900 pairs.**

| outcome | pairs | share |
| :--- | ---: | ---: |
| **Live** | **98,915** | **48.99%** |
| Not live — measured gap ≥ 4 days | 59,080 | 29.26% |
| Not live — no insertion instant after `τ1` | 5,209 | 2.58% |
| Not live — no insertion instant at or before `τ1` | 38,696 | 19.17% |
| Not live, total | 102,985 | 51.01% |

Every waterfall line, for the diff:

| population | n | live | gap-fail | no-after | no-before | live share |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Full frame | 220,107 | 100,158 | 61,664 | 5,218 | 53,067 | 45.50% |
| **Analysis population** | **201,900** | **98,915** | **59,080** | **5,209** | **38,696** | **48.99%** |
| Has S2 evidence | 178,165 | 87,691 | 50,386 | 4,253 | 35,835 | 49.22% |
| `T0` not contaminated | 155,131 | 86,832 | 45,796 | 4,253 | 18,250 | 55.97% |
| W-estimation sample | 128,099 | 82,369 | 40,572 | 4,120 | 1,038 | 64.30% |
| Analysis pop., `τ1` ≤ pull | 198,216 | 98,915 | 59,080 | 1,525 | 38,696 | 49.90% |
| Analysis pop., `τ1` > pull | 3,684 | 0 | 0 | 3,684 | 0 | 0% |
| Analysis pop., `T0` contaminated | 23,034 | 859 | 4,590 | 0 | 17,585 | 3.73% |

**Pair-level, confirmed empirically.** Of 2,481 users in the analysis population, **1,937 are live
for some shows and not live for others**. A user-level filter is not available even as an
approximation.

## 6. Three things flagged for the gate

**6.1 The bracketing gap is length-biased, so the failure rate is 37%, not 1%.**
`0036` §1 argues the percentile as "at the 99th it is one in a hundred." That holds for a
**uniformly drawn** gap. The rule in §2 does not draw uniformly: it takes the gap **containing a
fixed instant**, and a long gap covers more calendar time, so it is far likelier to contain `τ1`.
Measured here: pooled median gap 0.0000006 days; **bracketing** median 2.01 days; 75th percentile
9.03 days; **37.4% of the 157,995 pairs with a measured gap fail the 4-day threshold**. The two
rulings are individually sound and their interaction is not what §1's arithmetic describes. Raising
the percentile does not repair it either — see §7.

**6.2 A fifth of the analysis population fails for having no pre-`τ1` evidence at all.**
38,696 pairs (19.2%) have no insertion instant at or before `τ1`: the account's Trakt record begins
*after* `τ1`. That is the expected interaction of `0021` (insertion time) with an old `T0` — a user
who finished S1 in 2014 and joined Trakt in 2019 has no insertion evidence in 2014 whatever they
claim. The class collapses to 1,038 in the 128,099 sample and to 18,250 once contaminated `T0` is
excluded, so it is dominated by early or corrupt `T0` — but it is not empty in the clean sample.

**6.3 The unit of the gap distribution is not settled by the spec and it moves the threshold.**
Adopted here: **one gap per consecutive pair of records**, the literal reading of "consecutive
insertion instants". Because 59.3% of those gaps are sub-second batch spacing, the pooled
distribution is dominated by within-batch structure. Reading "instants" as **distinct** instants
instead (dedup to the second) gives 11,994,497 gaps, a 99th percentile of **6.03 days** and a
threshold of **7 days**. This is the most likely source of a dual-run divergence.

## 7. Sensitivity, recorded for Step 13

| percentile | threshold (days) | live pairs of 201,900 | live share |
| ---: | ---: | ---: | ---: |
| 90 | 1 | 55,015 | 27.25% |
| 95 | 1 | 55,015 | 27.25% |
| 97.5 | 2 | 78,633 | 38.95% |
| **99** | **4** | **98,915** | **48.99%** |
| 99.5 | 6 | 109,517 | 54.24% |
| 99.9 | 19 | 128,560 | 63.68% |

Live share against a threshold grid, same population: 1d 27.2%, 2d 38.9%, 3d 45.0%, **4d 49.0%**,
6d 54.2%, 8d 57.7%, 12d 60.8%, 19d 63.7%, 30d 66.2%, 45d 68.0%, 60d 69.4%, 90d 70.8%, 120d 72.0%,
180d 73.5%, 365d 75.7%. The curve is flat in no region — the live share is a smooth function of the
threshold over three orders of magnitude, so **there is no natural threshold to be found in this
data**, which is exactly why `0036` named a percentile instead of a shape.

## 8. Judgement calls this run made that the spec did not settle

1. **Unit of the gap distribution** — per record pair (adopted) vs per distinct insertion instant. 4 days vs 7 days. See §6.3.
2. **Accounts contributing to the distribution** — all 2,549 in the scan, unrestricted.
3. **Percentile interpolation** — numpy default linear on the pooled continuous gaps.
4. **Unit the ceiling is taken in** — whole days, matching Step 6. `0025` says "take the ceiling of the percentile" without naming a unit; a ceiling in seconds would give 3.1606 days ≈ 273,073 s and a materially different rule.
5. **Comparison sense** — live iff gap **strictly** < threshold, not live at gap ≥ threshold, taken from `0025` reason (a) ("excludes a gap at or above the threshold").
6. **Reporting population** — the 201,900 analysis population is primary; every waterfall line is reported beside it, since Step 7 does not say which population the rule's counts are quoted on.
7. **Edge-case precedence** — an account with zero records in the scan is counted under *no instant at or before `τ1`*.
8. **Right-censoring is not filtered here.** 3,684 pairs have `τ1` after the 2026-08-11 pull instant and are structurally not live. That is D10's business in Step 9, not Step 7's, but the count is reported so it is not read as behaviour.
9. **`np.interp` clamps** rather than extrapolates outside the knot range; 6,956 records, 0.025%.

## 9. Files

- Chart — `artifacts/step7-gap-distribution-a-run1254.png`
- Machine-readable — `artifacts/step7-liveness-a-run1254.json`
- Code, single self-contained file — `src/step7_a_run1254.py`
- Full results — `processed/step7/a/_snapshot_ds_run_1254/results.json`
- Row-level detail, never public — `processed/step7/a/_snapshot_ds_run_1254/pair_liveness_ds_run_1254.csv`
