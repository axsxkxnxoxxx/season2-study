# Step 7 — Liveness threshold and rule, instance `a`

**Status: PROPOSED. This is a gate. Nothing here is adopted.** Instance `a` of a dual pair.
Date 2026-08-13. **API calls: 0.**

Spec: `task-sheet.md` Step 7 lines 226–254, as ruled by `decisions/0036`. Percentile per `0036`,
continuous instants per `0029`, ceiling per `0025`, insertion time per `0021`, `τ1` anchor per `0034`,
`W = 108` per `0026`. Chart: `artifacts/step7-gap-distribution-a.png`.

---

## 1. The threshold

| | |
| :--- | ---: |
| Percentile (`0036`) | **99th** |
| Raw 99th percentile of the gap distribution | **3.1606 days** |
| 95% CI on the 99th percentile (order statistics) | 3.1503 – 3.1719 days |
| Rounded **up** (`0025`) | **4 days** |

Derived **independently of `W`**; `W` enters only the test instant.

## 2. The gap distribution it was read off

Gap = interval between consecutive insertion instants on one account, as a **continuous instant
difference in days, not floored** (`0029`). Insertion instant = `np.interp(rid, knot_rid, knot_time)`
against the **stored** Step 5 isotonic curve. **The curve was read, never refitted.**

| | |
| :--- | ---: |
| Records | 27,656,813 |
| Accounts | 2,549 |
| Gaps | 27,654,264 |
| Gaps per account — median / mean / max | 8,247 / 10,849 / 60,945 |
| Zero-length gaps | 1,792,015 (6.48%) |

| Percentile | 50 | 75 | 90 | 95 | 98 | **99** | 99.5 | 99.9 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gap (days) | 0.0000 | 0.020 | 0.337 | 0.912 | 1.914 | **3.161** | 5.597 | 18.342 |

Ordering is by `rid`, the global auto-increment assigned at insert; the curve is monotone, so this is
also the order of the instants. 1,862 records fall below the curve's first knot and 5,094 above its
last; `np.interp` clamps both, as the spec's formula prescribes.

## 3. The rule

> A user-show pair counts as **live** if, on that pair's own `τ1 = ⟦T0⟧ + 108 × 24h`, the interval
> between the **last insertion instant at or before `τ1`** and the **first insertion instant after
> `τ1`** on that account is **strictly less than 4 days**.
>
> Insertion instants are **account-wide** evidence — every record in the sweep, all shows and all
> movies, not restricted to the show under study.
>
> **No insertion instant after `τ1`** → the gap is open-ended → **not live**.
> **No insertion instant at or before `τ1`** → no pre-`τ1` evidence → **not live**.
>
> The test is on that **one bracketing gap**, never on every gap in the sweep.
>
> The filter is **pair-level**. One account can be live for one show and not live for another, and no
> user is ever dropped wholesale.

Comparison direction is `≥ threshold → not live`, taken from `0025`'s own worked example ("if the test
excludes a gap at or above the threshold…"), not chosen here.

## 4. Counts

Applied to the **Step 5 analysis population, 201,900 pairs** across 2,481 accounts. The Step 5
waterfall was recomputed and asserted before use: 201,900 → 178,165 → 155,131 → 152,126 → 128,099,
exact match.

| Outcome | Pairs | Share |
| :--- | ---: | ---: |
| **Live** | **98,915** | 48.99% |
| Not live — measured gap ≥ 4 days | 59,080 | 29.26% |
| Not live — no insertion instant **after** `τ1` | 5,209 | 2.58% |
| Not live — no insertion instant **at or before** `τ1` | 38,696 | 19.17% |
| **Not live, total** | **102,985** | 51.01% |

**The filter is genuinely pair-level, and measurably so.** 1,949 accounts have at least one live pair,
2,469 have at least one not-live pair, and **1,937 accounts are mixed** — live for one show, not live
for another. A user-level filter would have been a different object.

## 5. Four things the spec did not settle, and one it did not anticipate

**(a) Which gaps the reference distribution pools.** The spec says "the observed gap distribution" and
does not say how accounts are weighted. Three readings, all defensible:

| Variant | Raw p99 | Ceiling |
| :--- | ---: | ---: |
| **A. All consecutive records, gap-weighted (adopted)** | 3.1606 d | **4 d** |
| B. Consecutive *distinct* insertion instants, gap-weighted | 3.4432 d | **4 d** |
| C. All consecutive records, **account**-equal-weighted | 6.9047 d | **7 d** |

A is the literal reading: every record is an insertion, so every consecutive pair is a gap. **A and B
agree after the ceiling**, so the dedupe question does not move the answer. **C does not** — it lands
at 7 days, because pooling by gap lets the heaviest accounts dominate a distribution that is supposed
to describe *an account*. If instance `b` reports 7, that is this choice and not a bug.

**(b) Which population the rule is counted on.** Applied to waterfall line 1, the 201,900-pair analysis
population. Lines 2–5 are Step 5's *`W`-estimation* filters and have no bearing on liveness.

**(c) Which accounts the reference distribution is estimated on.** All 2,549 swept accounts, not the
2,481 that carry a pair.

**(d) `⟦T0⟧`.** UTC midnight opening the `T0` calendar date, per Step 1 §2.4's half-open form.

**(e) The one the spec did not anticipate — the reference distribution and the test statistic are not
the same object.** The threshold is the 99th percentile of a *typical* gap, but the tested gap is the
one that **brackets `τ1`**, and a longer gap is more likely to contain any given instant. The tested
gap is therefore **length-biased**, and the "one in a hundred" calibration in `0036` §1 does not
transfer to it:

| | median | p75 | p90 | p95 |
| :--- | ---: | ---: | ---: | ---: |
| Bracketing gap (157,995 measured) | 2.01 d | 9.03 d | 81.3 d | 240.5 d |

**37.4% of measured bracketing gaps sit at or above the 4-day threshold, not 1%.** This is a property
of the rule's shape, exactly as the whole-sweep compounding was. **It is reported, not repaired** —
repairing it would mean choosing a different reference distribution, which is a Human Lead ruling.

## 6. Two findings the Human Lead should see before approving

**The `no instant at or before τ1` bucket is a clock mismatch, not an absent user, and it is 19% of
pairs.** `T0` is built from **claimed** `watched_at` dates; liveness runs on **insertion** instants.
An account that imported an old history has a `τ1` years before it ever wrote a record. In this bucket
the median pair's `τ1` falls **1,578 days before the account's first-ever insertion instant** (p25 608,
p75 2,745). 8,037 of the 38,696 have a `τ1` earlier than the calibration curve's own start,
2012-12-02, where no insertion instant can exist by construction. `0036` §2.3 rules these **not live**,
and that ruling is applied here unchanged — but the bucket is measuring the gap between two clocks, and
it is the largest single not-live category after the measured gap.

The `no instant after τ1` bucket behaves as intended by comparison: 3,684 of the 5,209 are pairs whose
`τ1` postdates the 2026-08-11 pull instant, which is structural right-censoring; the remaining **1,525**
are accounts that genuinely wrote nothing after `τ1` (median 72 days from last insertion to `τ1`).
On the `τ1`-observable subset (198,216 pairs) the counts are 98,915 / 59,080 / 1,525 / 38,696.

**`0036`'s compounding argument is far stronger than the numbers it was written with.** The ruling
illustrates the whole-sweep failure with accounts of 10, 50 and 100 gaps. The **median account here has
8,247 gaps**, at which a whole-sweep test trips with probability `1 − 0.99^8247 ≈ 1`. The bracketing-gap
shape was not merely the better choice; a whole-sweep test would have declared essentially every account
dead. This corroborates the ruling and is recorded because the ruling's worked example understates it by
two orders of magnitude.

## 7. Threshold sensitivity, for Step 13

Live / not-live-on-a-measured-gap, at the ceiling of each percentile, `W` held at 108:

| Percentile | 90 | 95 | 97 | 98 | **99** | 99.5 | 99.9 | 99.99 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Threshold (d) | 1 | 1 | 2 | 2 | **4** | 6 | 19 | 136 |
| Live | 55,015 | 55,015 | 78,633 | 78,633 | **98,915** | 109,517 | 128,560 | 146,473 |
| Not live, measured gap | 102,980 | 102,980 | 79,362 | 79,362 | **59,080** | 48,478 | 29,435 | 11,522 |

The two no-evidence buckets are invariant to the threshold: 5,209 and 38,696 at every row.

## 8. Integrity warning — a concurrent process wrote into this instance's namespace

**During this run, a process other than this instance created, overwrote and deleted files in
`artifacts/` and in `processed/step7/a/`.** Observed, with timestamps:

- Scripts this instance did not write appeared in `src/`: `step7_figs_a.py`, `step7_liveness_a.py`.
  **They were not read**, to avoid contaminating a dual run with another implementation's choices.
- Outputs this instance did not write appeared in `processed/step7/a/`: `gap_distribution.json`,
  `rule_counts.json`, `sensitivity.json`, `gaps_days.npy`, `insertion_instants_sorted.npy`,
  `user_sorted.npy`, and a `_snapshot_ds_run_1254/` directory.
- `artifacts/step7-gap-distribution-a.png` was **overwritten** by that process.
- `artifacts/step7-liveness-a.json`, written by this instance, was **deleted** by that process, and
  `step7-liveness-a-run1254.json` and `step7-gap-distribution-a-run1254.png` appeared in its place.

**The `-run1254` files are not this instance's output and must not be diffed as instance `a`.** They
were not read.

**What was done about it.** This instance's three scripts were checked and are unmodified. The entire
chain was then **re-run from scratch into an isolated directory**, `processed/step7/a/verify_ds/`, and
reproduced every number in this document exactly — threshold `3.1605649852752755` → 4 days, counts
98,915 / 59,080 / 5,209 / 38,696, Step 5 waterfall asserted. **Every figure above comes from that
isolated re-run.** Duplicate copies of both deliverables are held in
`processed/step7/a/verify_ds/`.

**The Human Lead should establish what that process is before diffing the dual pair.** If it is
instance `b` writing to the wrong letter, the dual run's isolation is broken and Step 7 needs relaunching.

## 9. Provenance

`processed/step7/a/verify_ds/` holds the run these numbers come from, produced by
`src/step7_gaps_a.py`, `src/step7_threshold_a.py`, `src/step7_rule_a.py`. Row-level detail is
`processed/step7/a/verify_ds/pair_liveness.csv`, which carries `user_idx` and **stays out of
`artifacts/` and `decisions/`**. No usernames, user IDs or watch histories appear in this file or in
`artifacts/step7-liveness-a.json`.
