> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — liveness threshold, instance A4 (rerun on `decisions/0040`)

**Status: PROPOSED, NOT ADOPTED.** This is a gate. Nothing here is adopted, Step 8 is not begun,
and this instance records no approval. Zero API calls; every number comes from cached data and the
stored Step 5 calibration curve, which is read and never refitted.

**Chart:** `artifacts/step7-gap-distribution-a4.png`
**Machine-readable:** `artifacts/step7-liveness-a4.json`
**Row-level intermediates (never leave the machine):** `processed/step7/a4/`

---

## 0. The one question that sets the number, and it is unsettled

`decisions/0040` §2 moved derivation after D10 and observed that the open-ended share then falls
below 1%, so "the 99th percentile over the **extended** set is finite, an infinite gap fails a
finite threshold on its own, and edge case (i) stops needing to be a separate ruling." That
dissolves the restriction `0039` §5 had called forced.

**But `task-sheet.md` line 266 still states the suspended entry's restriction as operative spec:**
*"The reference set is the 129,630 measured-gap pairs."* `0040` §4 corrected four superseded figures
in the task sheet and did not correct this one. **Step 8 launches off the task sheet.** This is a
defect to report, not a thing to reconcile.

The two readings give different numbers, and this is the largest lever in the step.

| Reference set | Definition | n | Threshold | Pairs excluded | Share of post-D10 population |
| :--- | :--- | ---: | ---: | ---: | ---: |
| **A — extended** (proposed) | every **tested** pair: 128,467 measured gaps + 751 open-ended carried as `+∞` | 129,218 | **1,293 d** | **1,282** | **0.870%** |
| B — measured-gap only | the finite bracketing gaps only | 128,467 | 632 d | 2,026 | 1.375% |

**A4 proposes A, 1,293 days.** `task-sheet.md` states that `decisions/` is authoritative over it
where the two disagree; `0040` postdates and suspends `0039` and reasons explicitly toward the
extended set; and A is the only reading under which the percentile is taken on the set the rule is
actually applied to, which is what `0038` §2.1 requires. **B is reported in full at every number
below, so the Human Lead can select B without a rerun.**

Candidate A delivers **0.9921%** against the set the percentile was taken on. Candidate B delivers
0.9925% of measured-gap pairs but **1.5679%** of the pairs the rule actually tests, because the
open-ended pairs are kept out of the reference and then excluded by the rule. That is the
calibrate-on-one-set-apply-to-another shape `0037` withdrew, in miniature.

---

## 1. Population — the waterfall, then D10

The published waterfall is reproduced exactly from `processed/step5/pair_revision5.csv`:

**201,900 → 178,165 → 155,131 → 152,126 → 128,099.**

Derivation runs on **line 4 less D10 right-censoring** (`0038` §2, `0040` §2). D10 is
`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, with `H = 91` and `τ_pull = 2026-08-11T00:00:00Z`. At
`W = 108` that is a 199-day horizon and a latest admissible `T0` of **2026-01-24**.

| | Pairs |
| :--- | ---: |
| Frozen line 4 | 152,126 |
| Removed by D10 at `W = 108` | 4,756 |
| **Post-D10 population — derivation and application** | **147,370** (96.87%) |

### What D10 removed, by liveness class

| Class | Before D10 | After D10 | Removed |
| :--- | ---: | ---: | ---: |
| Measured bracketing gap | 129,630 | **128,467** | 1,163 |
| Open-ended — no instant after `τ1` | 4,246 | **751** | 3,495 |
| No instant at or before `τ1` | 18,250 | **18,152** | 98 |
| **Total** | **152,126** | **147,370** | **4,756** |

**Divergence from `0040` §2, reported not reconciled.** The entry anticipated **894 / 130,524 =
0.685%** open-ended after D10; A4 measures **751 / 129,218 = 0.5812%**. The anticipated figure
subtracts only the 3,352 pairs whose `τ1` is past the pull instant, i.e. it assumes D10 acts on the
open-ended bucket alone. D10's cut is 91 days stricter than `τ1 > τ_pull` and removes pairs from
every class. **`0040`'s conclusion is unaffected:** the share is well under 1%, so the extended 99th
is finite.

### Pair counts by class at `W = 108`, on the 147,370

| Class | Pairs | Disposition |
| :--- | ---: | :--- |
| Measured bracketing gap | 128,467 | tested against the threshold |
| Open-ended, no instant after `τ1` | 751 | gap is `+∞`; fails any finite threshold |
| No instant at or before `τ1` | **18,152** | **LIVE, untested** — `decisions/0021` |
| **Tested (extended) set** | **129,218** | |
| **Total** | **147,370** | |

---

## 2. `0036` §2.3(ii) is withdrawn — what the 18,152 cost

`0040` §1 reinstated `0021` (approved **gate 2 of 5**): *any record inserted after the window closed
proves the account was alive, whatever date it claims.* Every pair in this bucket has insertion
instants after `τ1` by construction.

**A4 confirms `0040`'s premise on the data: zero accounts in the sweep have no insertion instants,
and the minimum is three gaps per account.** So `0036` §2.3(ii) scored live accounts dead.

The effect on the filter is not marginal:

| | Pairs excluded by liveness |
| :--- | ---: |
| `0039` as approved, on the 152,126 | 23,772 |
| **A4, candidate A** | **1,282** |
| A4, candidate B | 2,026 |

**The liveness filter now costs about 95% less than the suspended approval had it costing.**
Step 9's liveness bound is built on this set and must be recomputed; it will be far smaller.

---

## 3. Is edge case (i) still needed as a separate ruling?

**No — and it is not needed under either candidate reference set.**

An open-ended gap is infinite. `∞ ≥ T` for every finite `T`, so the branch is arithmetic rather than
a ruling. Under candidate A the threshold is 1,293 d and under B it is 632 d; the open-ended pairs
fail both without a special case.

**What *is* still needed is a definition, not a ruling:** that an absent successor instant is scored
as an **infinite gap** rather than as *undefined*. A4 supplies that convention; the spec does not
state it. Once stated, edge case (i) can be deleted from the rule as a separate clause.

**One caveat on candidate A, stated because it bears on the choice.** The extended 99th is finite
only because the open-ended share is 0.5812%. **Above the 99.4188th percentile it is infinite**, so
that reference set carries a hard ceiling on the percentile only 0.42 points above the adopted one.
And **4 of 2,000 account-clustered bootstrap replicates (0.2%) return an infinite 99th**, because a
resample can push the open share above 1%. Candidate B has no such failure mode.

---

## 4. The bracketing-gap distribution, post-D10

One gap per pair (`0038` §3), continuous instant differences (`0029`), on distinct insertion
instants with exact ties collapsed (`0037` §4).

| | Days |
| :--- | ---: |
| min | 0.0000195 |
| p10 | 0.276 |
| p25 | 0.792 |
| **median** | **1.883** |
| p75 | 6.917 |
| p90 | 43.10 |
| p95 | 125.28 |
| **p99** | **631.803** |
| p99.5 | 1,156.62 |
| p99.9 | 2,469.35 |
| max | 3,196.27 |
| mean | 32.13 |

Sub-second share: **0**. All eight percentile conventions — seven `numpy` methods and nearest-rank
ceiling — return the same value on both candidate sets, because the selected order statistic sits
inside a tie plateau (156 pairs at 631.8031 d; 12 at 1,292.0284 d).

**The length bias `0037` named is reproduced.** Pooled gaps: median 0.0000007 d, 99th **3.4432 d**
→ 4 d. Bracketing gaps: median **1.88 d**, and **34.18%** of them exceed the pooled 99th. The record
states 34.12% on the pre-D10 152,126; the difference is the population, not the arithmetic.

---

## 5. The rule

> A **user-show pair** is **LIVE** unless the account's insertion history shows a gap of at least
> **T days** bracketing that pair's own `τ1 = ⟦T0⟧ + W × 24h`.
>
> Build the account's sweep-wide sequence of record insertion instants — **every** record, all shows
> and movies, estimated from the **stored** Step 5 isotonic play-`id` curve, read and never refitted
> — sort ascending, collapse runs of **exactly** equal instants, and take the last distinct instant
> **at or before** `τ1` and the first distinct instant **after** `τ1`.
>
> - Both exist → the bracketing gap is their difference in **continuous days**.
> - No instant **after** `τ1` → the bracketing gap is **infinite**.
> - No instant **at or before** `τ1` → the pair is **LIVE and is not tested** (`decisions/0021`).
>
> The pair is **NOT LIVE** iff the bracketing gap is **≥ T**. The test applies to that one gap and
> to **no other gap in the sweep**.
>
> Evidence is **account-wide**; the test is clock-start-relative and clock start is pair-specific,
> so one account may be live for one show and not for another. **Liveness is a pair-level filter.
> No user is ever dropped wholesale.**

`T = 1,293 d` proposed (candidate A); `T = 632 d` under candidate B. Anchored at `τ1` only — `τ2`
plays no part (`decisions/0034`).

---

## 6. Realised rate, against every denominator

| | Candidate A, `T = 1,293` | Candidate B, `T = 632` |
| :--- | ---: | ---: |
| Not live, total | **1,282** | 2,026 |
| — on a measured gap | 531 | 1,275 |
| — open-ended | 751 | 751 |
| — no pre-`τ1` instant | **0** (live) | **0** (live) |
| Live | 146,088 | 145,344 |
| Rate vs **measured-gap pairs** (128,467) | 0.4133% | **0.9925%** |
| Rate vs **tested extended set** (129,218) | **0.9921%** | 1.5679% |
| Rate vs **post-D10 population** (147,370) | 0.8699% | 1.3748% |

---

## 7. Mandatory disclosure 1 — the quota property

**The level is set by the exclusion rate, not by any feature of the data.** The percentile is taken
on the very distribution the test is applied to, so choosing the 99th mechanically fixes the
exclusion rate at 1% and the threshold is whatever number delivers it. Any percentile would have
produced a self-consistent answer.

**1,293 days is not a point where account behaviour changes. It is the 1% quota's price tag.**

| Percentile | Candidate A threshold | Candidate B threshold |
| :--- | ---: | ---: |
| 90th | 49 d | 44 d |
| 95th | 147 d | 126 d |
| 97.5th | 385 d | 283 d |
| **99th** | **1,293 d** | **632 d** |
| 99.5th | **infinite** | 1,157 d |
| 99.9th | **infinite** | 2,470 d |

This is the price of a calibrated rate and it is disclosed, not argued away (`0038` §4).

**What survives.** `0036` §1's conservative-direction argument still points **up for the gap test**:
a false-dead removes a pair, and the liveness exclusion already biases the never-started share
**down** (Step 14, bias 2). It identifies a direction, not a level. **Per `0040` §3 it is withdrawn
as a justification for the edge-case branches** — that mechanism describes accounts that *stopped*
logging, not accounts that *started late* — and it is not cited beyond the gap test anywhere in this
document.

---

## 8. Mandatory disclosure 2 — the inertness, measured on A4's population, with no invariance claimed

**Candidate A at the 99th: the measured-gap test does 531 of 1,282 exclusions — 41.42% — and the
evidence-absence branch does 751 — 58.58%.**
**Candidate B at the 99th: 1,275 of 2,026 — 62.93% — against 751 — 37.07%.**

**No invariance is claimed and none exists.** The evidence-absence count is constant in the
percentile while the gap-test count is a function of it, so the share must move:

| Percentile | A: gap-test share | B: gap-test share |
| :--- | ---: | ---: |
| 90th | 94.19% | 94.43% |
| 95th | 88.31% | 89.50% |
| 97.5th | 76.70% | 81.00% |
| **99th** | **41.42%** | **62.93%** |
| 99.5th | — (infinite) | 46.13% |
| 99.9th | — (infinite) | 10.60% |

**How this differs from the record.** `0038` §5 as corrected by `0039` published **5.37% / 94.63%**
on the pre-D10 152,126. **That figure is gone, not merely moved.** 94.63% of it was
`0036` §2.3(ii)'s 18,250-pair bucket, which `0040` §1 withdrew and returned to the population as
live, and most of the remainder was right-censoring that D10 removes. **There is no longer an
edge-case branch that dominates the filter**, and the threshold is now doing a large share of a much
smaller job.

---

## 9. The interval — account-clustered, B = 2,000

**Never report the threshold bare.** Same treatment as `W = 108 ± 18`.

| | Point | Account-clustered 95% | i.i.d. 95% | Clustered width ÷ i.i.d. width |
| :--- | ---: | :--- | :--- | ---: |
| **Candidate A** | 1,293 d | **[787, 2,200] d** | [1,210, 1,405] d | **7.2×** |
| Candidate B | 632 d | **[556, 836] d** | [632, 655] d | **12.6×** |

**B = 2,000 replicates**, seed `20260813`, `numpy` PCG64, clustering unit the **account**;
**2,100 accounts** carry tested pairs, median 47 pairs each, max 399.

**Why clustered.** One account's insertion sweep supplies the bracketing gap for every pair it owns.
Measured here: **34.53%** of measured-gap pairs share their bracketing-gap value **exactly** with at
least one other pair, largest tie group **298**, 92,564 distinct values across 128,467 pairs. The
i.i.d. interval invents an order of magnitude of precision it does not have. `0039`'s 34.4% and 298
are reproduced.

**Red Team's objection about 300 replicates is confirmed and quantified.**

| B | Candidate B interval across three seeds |
| ---: | :--- |
| 300 | [564, 741], [542, 812], [560, 804] |
| 1,000 | [559, 836], [554, 814], [539, 800] |
| 2,000 | [556, 836], [553, 829], [542, 829] |
| 4,000 | [553, 814], [554, 814], [542, 829] |

At B = 300 the upper endpoint moves **71 days on the seed alone**. At B = 2,000 it sits in 829–836.
Candidate A's upper endpoint is pinned at **2,200 across every B and seed**, which is a tie plateau,
not precision.

**Against the suspended approval.** `0039` approved 632 d with a clustered [528, 787] from B = 300.
On A4's post-D10 population at B = 2,000 the same quantity is **632 d with [556, 836]** — the point
estimate is **bit-identical** (631.8031044554186 before and after D10, because the selected order
statistic sits in a 156-pair tie plateau), and the interval moves because 300 replicates put the
endpoints on the 7th and 8th order statistics.

**A note that matters for the diff:** D10 removes 1,163 measured-gap pairs and **does not move
candidate B's threshold at all**. What `0040` changes is the **exclusion count**, not that number.

---

## 10. What the filter costs across its own interval — input for `0040` §6

`0040` §6 asks **Step 9** whether the threshold is load-bearing at all. Step 7 does not answer that;
it supplies the inputs.

| Threshold | Not live | Share of the 147,370 |
| ---: | ---: | ---: |
| 556 d (B lower) | 2,454 | 1.665% |
| **632 d (B point)** | **2,026** | **1.375%** |
| 787 d (A lower) | 1,707 | 1.158% |
| 836 d (B upper) | 1,671 | 1.134% |
| **1,293 d (A point)** | **1,282** | **0.870%** |
| 2,200 d (A upper) | 897 | 0.609% |

**Across the whole of either candidate's account-clustered interval the filter removes between 897
and 2,454 pairs of 147,370 — 0.61% to 1.67% of the population.** Whether that band moves the
headline is Step 9's measurement, not Step 7's claim.

---

## 11. Step 13 — the per-arm refit

`0038` §6: the threshold **is** a function of `W`; `W` and the threshold are **not independent
robustness axes**. Every arm re-runs **D10 at its own `W`** and refits on its own post-D10
population. **`H` is held constant at 91 across every arm.** Arms per `0027`, run as a superset so
the response is traced rather than interpolated between endpoints.

| `W` | Post-D10 pairs | Measured | Open | No-pre-`τ1` (live) | **A: T** | A: realised | A: clustered CI | **B: T** | B: realised | B: clustered CI |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- | ---: | ---: | :--- |
| 38 | 147,685 | 128,122 | 348 | 19,215 | 716 | 1.000% | [590, 914] | 589 | 1.265% | [516, 713] |
| 46 | 147,685 | 128,248 | 367 | 19,070 | 721 | 0.979% | [591, 973] | 580 | 1.274% | [508, 672] |
| 60 | 147,685 | 128,343 | 432 | 18,910 | 758 | 0.996% | [614, 1161] | 583 | 1.331% | [519, 691] |
| 75 | 147,685 | 128,485 | 517 | 18,683 | 885 | 0.987% | [651, 1285] | 590 | 1.396% | [519, 713] |
| 91 | 147,685 | 128,592 | 706 | 18,387 | 1,230 | 0.993% | [748, 1756] | 632 | 1.520% | [559, 793] |
| 107 | 147,384 | 128,476 | 745 | 18,163 | 1,287 | 0.997% | [787, 2200] | 632 | 1.563% | [556, 790] |
| **108** | **147,370** | **128,467** | **751** | **18,152** | **1,293** | **0.992%** | **[787, 2200]** | **632** | **1.568%** | **[559, 790]** |
| 120 | 147,136 | 128,422 | 731 | 17,983 | 1,300 | 0.989% | [814, 2200] | 642 | 1.559% | [573, 885] |
| 150 | 146,602 | 128,079 | 779 | 17,744 | 1,405 | 0.993% | [903, 2200] | 662 | 1.593% | [588, 909] |
| 180 | 145,845 | 127,606 | 836 | 17,403 | 1,406 | 0.963% | [927, 2470] | 692 | 1.643% | [592, 898] |
| 213 | 144,852 | 126,762 | 949 | 17,141 | 1,654 | 0.996% | [1128, 2818] | 703 | 1.736% | [606, 912] |

Realised rates are against the tested extended set. Per-arm CIs are **B = 1,000** and resample each
arm's own reference set directly; they are computed by a slightly different design from §9's
headline interval and the two are not interchangeable.

**The `W`-coupling, measured post-D10:** candidate A spans **716 → 1,654 d**, candidate B spans
**589 → 703 d**. The record's 576 → 697 was measured on the pre-D10 152,126 over a narrower arm
list; the magnitude agrees.

**D10 is flat for `W ≤ 91`**, because its horizon is `max(W, 91) + H`. Above 91 the population
shrinks with `W`, which is the cohort-asymmetric censoring loss Step 13 must report per air period.

**The counterfactual `0038` §6 exists to rule out.** Freezing candidate B's 632 d from `W = 108` and
carrying it to every arm delivers 0.843% at `W = 38` and 1.206% at `W = 213` against measured-gap
pairs — it misses its stated 1% at every arm but 91–108. A refit per arm is required, not optional.

---

## 12. Sensitivities reported, not adopted

- **Weighting.** One gap per distinct `(account, gap)` instead of one per pair gives a 99th of
  190.83 d → **191 d** on 93,075 keys, against 632 d per pair. Still the largest single lever after
  the reference-set question. **`0038` §3 fixes one gap per pair; A4 applies that.** The record's
  190 d was the pre-D10 figure.
- **The withdrawn pooled basis**, for continuity with `0037`: pooled 99th 3.4432 d → 4 d over
  25,862,249 gaps; **34.18%** of bracketing gaps exceed it.
- **The open-ended bucket post-D10 is genuine silence, not censoring.** Of the 751, **zero** have
  `τ1` past the global sweep end (2026-08-10T20:48Z) or past `τ_pull`; all 751 have `τ1` past the
  account's own last insertion instant. D10 has absorbed the censoring that inflated this bucket
  pre-D10, which is exactly what `0038` §7 predicted and `0040` §2 required.

---

## 13. Judgement calls the spec still does not settle

1. **Which reference set** — extended (1,293 d) or measured-gap-only (632 d). `0040` §2 reasons
   toward extended; `task-sheet.md` line 266 still states measured-only. **Largest lever in the
   step.** A4 proposes extended and reports both in full.
2. **`np.interp` clamping.** 1,862 records fall below the first calibration knot and 5,094 above the
   last. `np.interp` clamps them to the endpoint knot times, so they become exact ties and collapse
   under `0037`'s rule. Extrapolating or dropping them would change every number downstream. The
   spec says read the curve; it does not say what to do outside its support.
3. **An absent successor instant is scored as an infinite gap**, not as undefined. This is what
   makes edge case (i) redundant rather than a separate ruling, and it is a definition A4 supplies.
4. **Boundary: not live iff gap `≥ T`.** `0025` reason (a) implies it; no entry states it. An
   instant exactly equal to `τ1` counts as "at or before `τ1`".
5. **Derivation = application holds on the *tested* set (129,218), not on the full post-D10
   population (147,370).** The 18,152 no-pre-`τ1` pairs are in the application population and are
   unconditionally live, so they contribute no gap to the reference. `0038` §2.1's identity
   requirement is satisfiable only up to that subset, and A4 says so rather than claiming an
   identity it does not have.
6. **Per-arm D10.** D10 is a function of `W`, so each Step 13 arm re-runs it and derives on its own
   post-D10 population. Freezing D10 at `W = 108` across arms would hold the population constant
   instead. The spec requires derive-after-D10 but does not say which of these it means for the arms.
7. **Bootstrap clustering unit is the account.** A pair also belongs to a show, and show-level
   clustering is not modelled; `W`'s own interval is show-clustered.
8. **The arm list is a superset** of the brief's (38, and 60/75/91/120/180 added).
9. **The 99th percentile is not A4's call** and was not re-examined (`task-sheet.md` line 251).

---

## 14. Corroborations of the record

Reproduced exactly: the waterfall `201,900 → 178,165 → 155,131 → 152,126 → 128,099`; pooled 99th
**3.4431932062376234 d → 4 d**; median **7,812** gaps per account; measured-only 99th
**631.8031044554186 → 632 d**; largest tie group **298**; the pre-D10 class counts **129,630 /
4,246 / 18,250**.

Divergences, all attributable to the population change `0040` mandates rather than to arithmetic:
open-ended after D10 (**751 / 129,218** against the entry's 894 / 130,524); bracketing gaps
exceeding the pooled 99th (**34.18%** against 34.12%); the weighting lever (**191 d** against
190 d); the `W`-coupling (**589 → 703** against 576 → 697); the approved counts at line 267; and the
inertness split at line 248.

---

**Gate discipline.** A4 proposes and stops. Nothing is adopted, Step 8 is not begun, and the Human
Lead approves and diffs the two instances.
