# Step 8 — filter waterfall and required counts (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**This is the CLEAN RERUN ordered by the Human Lead**, on `task-sheet.md` Step 8 as it now stands — the spec as amended through `decisions/0082`. **A previous attempt was terminated after writing its deliverables and before either arm confirmed them; all of its output was discarded and this run was built from the committed state.** Against this arm's last confirmed deliverables the executable changes are `0081` (**`silent_at_tau1` restored**) and `0082` (**`p_at_bound` added**), which together take the enumerated column set from 87 to **89**; everything else — `0078`'s provenance rule, `0079`'s pipeline-produced drop set and inert-position labels, `0080`'s per-invariant coverage populations — is re-executed rather than assumed. This overwrites the previous `-b` deliverables.

**Provenance — `analytics-engineer-b / Step 8 position-5 build of 2026-08-16 (CLEAN RERUN on the spec as amended through decisions/0082; W = 108, tau_pull = 2026-08-11T00:00:00Z, mandated filter order 1-7, 89 columns)`.** Every count, every waterfall figure and every invariant result below was measured on that build (`0078`, `0079` §2). Where a figure is quoted from a ruling, the ruling's own build is named instead: `position-5 build of 2026-08-13 (both arms, the run decisions/0078 labelled)`. **A count without its provenance can be correct when written and wrong when read.**

**Every figure below states its population.** There are two and they differ by construction: **APPLY = 196,654** (waterfall line 1 less D10 — the position-5 output, and what position 6 filters) and **DERIV = 147,370** (Step 5 line 4 less D10, which requires S2 evidence). Step 8 produces both (`decisions/0070` ruling 1).

**Constants.** `W = 108` days (`0026`), `H = 91` days (D10), `tau_pull = 2026-08-11T00:00:00Z` (`0011`). `tau1 = ⟦T0⟧ + W × 24h`, `tau2 = ⟦T0⟧ + (W + H) × 24h = ⟦T0⟧ + 199 days`. Every boundary test is the half-open UTC-instant form of Step 1 §2.4; `date(watched_at) <= T1` appears nowhere in the implementation. **The `W` arm grid is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days** (`0075` ruling 3, the first statement of it in any file).

## 0. Deliverables of this run

| Deliverable | Path | Note |
| :--- | :--- | :--- |
| Analysis table | `processed/step8/b/analysis_table.csv.gz` | 196,654 rows × 89 columns |
| **Position-3 drop set** | `processed/step8/b/position3_drop_set.csv.gz` | **A pipeline deliverable** (`0079` §1), written by the same run that writes the table — not a helper script's side file. D9 half (b) cannot be computed without it |
| Filter waterfall | `artifacts/step8-waterfall-b.md` / `.json` | this document |
| Invariant report | `artifacts/step8-invariants-b.md` / `.json` | |

**Why the drop set is a deliverable and not a working file:** its absence returns **0 silently**, and a zero split-artifact count reads as **evidence the artefact does not occur** rather than as a missing input. Leaving it as a helper's side file would defeat the ruling that requires it, because a side file is not a thing the next run is obliged to produce.

---

## 1. The filter order, the four inert positions, and the side output

*Measured on: b: position-5 build of 2026-08-16.*

Applied in **exactly** this order (`decisions/0029`). The final row set commutes; the per-filter sample size does not, which is the whole reason the order is mandated.

1 Step 2 frame  
2 L2 = 1 exclusion  
3 S1 completion rule  
4 contamination exclusion (Step 5)  
5 right-censoring  
6 liveness  
7 outcome assignment (two instants)  

**Waterfall line 1 is the S1-completer population, 220,107 pairs** (`0068`). No instance chooses a base. Lines 2 and 3 follow from it.

### Positions 1, 2, 3 and 7 remove zero **by construction**, and are labelled inert

**Kept, not removed** (`0079` §4): removing a position removes the check that would catch a future upstream change, and the point of a fixed order is that the waterfall is comparable across runs and across arms. **Labelled, because** an unlabelled always-zero filter reads as evidence THE RULE FOUND NOTHING when it is evidence THE RULE CANNOT FIRE -- the same defect as an unlabelled code check (0069).

| Position | Filter | Removes | Why it is inert |
| :-- | :--- | ---: | :--- |
| **1** | Step 2 frame | 0 | line 1 is already the frame |
| **2** | L2 = 1 exclusion | 0 | line 1 is already the L2 > 1 S1-completer population (0068), and 0 of 1,138 frame shows have L2 = 1 |
| **3** | S1 completion rule | 0 | same -- BUT THE RULE IS NOT INERT: it removes 58,345 pairs upstream of line 1, which is why its drop set is a deliverable |
| **7** | outcome assignment (two instants) | 0 | outcome assignment annotates and removes nothing (0046) |

**Row 3 is the one that matters.** The *position* is inert; the **rule is the study's largest single exclusion**, removing **58,345 pairs upstream of line 1**. An unlabelled always-zero filter reads as evidence **the rule found nothing** when it is evidence **the rule cannot fire** — the same defect as an unlabelled code check.

### The position-3 drop set

*Measured on: b: position-5 build of 2026-08-16.*

Written by this pipeline run to `processed/step8/b/position3_drop_set.csv.gz` (`0079` §1). Under `0068` line 1 *is* the S1-completer population, so position 3 removes **0 from the waterfall** — which is why `0075` ruling 2 as first written named an empty set, and why `0077` restated it. The set is **the pair universe less the completers: 58,345 pairs — position-3 rule, position-5 build of 2026-08-13** as ruled (`0078`), **reproduced on this build** — carrying each pair's distinct-episode counts and the show's threshold, which is what half (b) reads. It is **not** the set-membership drop rule, which is a different rule, deletes **0 records**, and is counted in records rather than pairs.

| Position-3 drop set | Pairs |
| :--- | ---: |
| in-frame pairs with any in-`E` S1 or S2 distinct episode | 278,452 |
| of which S1 completers — **waterfall line 1** | 220,107 |
| **dropped by the S1 completion rule** | 58,345 |
| — carrying S1 evidence that fails the rule | 54,634 |
| — carrying S2 evidence and **no S1 evidence at all** | 3,711 |
| — carrying S2 evidence of any kind | 8,885 |

The 278,452 figure is one of the four readings `0068` surveyed before ruling on line 1; it reproduces here exactly, which is a cross-check on the base rather than a second candidate for it.

## 2. Waterfall — APPLY

*Measured on: b: position-5 build of 2026-08-16.*

| # | Filter | Inert | Retained pairs | Removed | Users | Shows |
| :-- | :--- | :--- | ---: | ---: | ---: | ---: |
| 1 | Step 2 frame | **INERT** | 220,107 | 0 | 2,487 | 1,138 |
| 2 | L2 = 1 exclusion | **INERT** | 220,107 | 0 | 2,487 | 1,138 |
| 3 | S1 completion rule | **INERT** | 220,107 | 0 | 2,487 | 1,138 |
| 4 | contamination exclusion (Step 5, decisions/0021) | no | 201,900 | 18,207 | 2,481 | 1,138 |
| 5 | right-censoring | no | 196,654 | 5,246 | 2,422 | 1,138 |
| 6 | liveness (ALT-BROAD, approved 0064) | no | 195,951 | 703 | 2,421 | 1,138 |
| 7 | outcome assignment (two instants) | **INERT** | 195,951 | 0 | 2,421 | 1,138 |

**Position 2 removes exactly 0 pairs and 0 shows, out of 1,138 shows examined.** That is a measured zero *and* a structural one: line 1 is already the `L2 > 1` population. **Position 3 removes 0 by construction** — but the rule (`F1 ∈ D1` and `|D1| ≥ ceil(0.90 × L1)`, first-pass) was computed independently from the record level, and it is that computation which produced line 1. This is why the monotone-decrease invariant is coded `>=` and not `>`: **four positions here legitimately remove nothing.**

**Position 4 is narrower than its name.** The adopted Step 5 rule (`0021`) is two disjoint exclusions — S2 evidence entirely air-date-stamped (16,665) and a contaminated `T0` with no S2 evidence at all (1,542) — and **not** the Step 5 estimation-sample waterfall down to 128,099. Step 5's own waterfall was re-asserted line by line before it was used: measured [201900, 178165, 155131, 152126, 128099], expected [201900, 178165, 155131, 152126, 128099].

**`processed/step5/adopted_rule.json` is read and cross-checked, not worked around.** `0074` ruling 6 made `processed/` the eighth propagation surface and corrected that file, which had carried revision-3 figures (4,849 removed / 215,258 retained). It now states **18,207 removed / 201,900 retained of 220,107**, and this instance measures **18,207 / 201,900 of 220,107** — agreement **True**, component by component.

## 3. Waterfall — DERIV

*Measured on: b: position-5 build of 2026-08-16.*

| # | Filter | Inert | Retained pairs | Removed |
| :-- | :--- | :--- | ---: | ---: |
| 1 | Step 2 frame | **INERT** | 220,107 | 0 |
| 2 | L2 = 1 exclusion | **INERT** | 220,107 | 0 |
| 3 | S1 completion rule | **INERT** | 220,107 | 0 |
| 4 | contamination exclusion, taken to Step 5 LINE 4 -- the adopted exclusion plus the three line-4 restrictions (has_s2, T0 not contaminated, completing record not post-dated) that define the DERIV base | no | 152,126 | 67,981 |
| 5 | right-censoring | no | 147,370 | 4,756 |
| 6 | liveness | no | 147,271 | 99 |
| 7 | outcome assignment | **INERT** | 147,271 | 0 |

**DERIV's position 4 is not the adopted contamination exclusion alone**, and that is stated rather than hidden: DERIV is *Step 5 line 4* less D10, and line 4 applies three further restrictions — `has_s2`, `T0` not contaminated, completing record not post-dated — none of which is a Step 8 filter position. Emitting it here is what stops Step 9 rebuilding the population, which would be a second definition of it (`0070` ruling 1).

## 4. Position 6 — liveness, and the population reconciliation

*Measured on: b: position-5 build of 2026-08-16.*

The rule is **ALT-BROAD** (`0048`, restored `0054`, **approved `0064`**): a pair is **NOT LIVE iff BOTH** the account shows no insertion instant after that pair's `tau1` **AND** the pair is **NOT Continued**. **"After" is STRICT** — silent iff no insertion instant `> tau1` (`0068`). **The evidence is restricted to records dated before `tau_pull`** (`0070` ruling 2). The stored play-`id` isotonic calibration at `processed/step5/calibration.npz` is **read and never refitted** (`0029`).

| Population | n (position 5) | Excluded | Never started | Started and left | Accounts |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY | 196,654 | 703 | 604 | 99 | 216 |
| DERIV | 147,370 | 99 | 0 | 99 | 73 |

**This reconciles exactly with the expectation** — 703 from 216 accounts on APPLY (604 + 99) and 99 from 73 accounts on DERIV (0 + 99). **It is a population reconciliation and NOT an invariant.** Neither **604** (the superseded ALT answer) nor **793** (the withdrawn ALT-MATCHED answer) was produced.

**Line 6 is OUTCOME-CONDITIONAL and is reported as such.** Conjunct 2 *is* the Continued test, read at `tau2`, so position 6 evaluates a position-7 predicate. That is permitted: `|A|` and liveness are row-local predicates on the position-5 output and commute exactly, and `0029`'s ordering rationale concerns per-filter sample size, which cannot reach position 7 because outcome assignment removes no rows — which is **position 7's inertness doing load-bearing work** rather than being a tidy footnote.

**Per-`W`-arm exclusion counts, so the `W`-coupling is visible:**

| `W` | 38 | 46 | 77 | 91 | 107 | 108 | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, total | 537 | 550 | 633 | 664 | 701 | 703 | 789 | 864 |
| APPLY, started-and-left component | 52 | 56 | 79 | 89 | 98 | 99 | 125 | 148 |
| DERIV, total | 52 | 56 | 79 | 89 | 98 | 99 | 125 | 147 |
| APPLY, total, evidence NOT restricted to `< tau_pull` | 537 | 550 | 633 | 664 | 701 | 703 | 789 | 864 |

The last row is the measurement of `0070` ruling 2 rather than an assumption: **the `tau_pull` restriction is inert on the exclusion set at every arm**, because the largest insertion instant in the sweep is **2026-08-10T20:48:00Z** and D10 already forces `tau1 ≤ tau_pull − 91 d`. It bites on the robustness tail, not here.

## 5. Right-censoring, as two lines

*Measured on: b: position-5 build of 2026-08-16.*

Censored population: **the POSITION-4 output, 201,900 (the mandated order)**.

| Term | Pairs removed | Direction on the headline |
| :--- | ---: | :--- |
| `max(W, 91)` | 3,684 | **UP** on the never-started share |
| incremental `+ H` | 1,562 | **UP** on the never-started share |
| total | 5,246 | |

Both removals fall on recent S1 completers — people who found an old show lately, have the whole series available and are disproportionately likely to roll straight into S2. A single combined figure would hide the price of `H` inside a removal that predates it.

### Retained pairs per air period after right-censoring, every `W` arm

*Measured on: b: position-5 build of 2026-08-16.*

**Measured on the position-4 output (201,900), which is what the mandated order censors** (`0070` ruling 8). `0033`'s 97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed on the **position-3** output; the order was set at `0029` on the ground that censoring is objective and independent of behaviour, and **changing a filter order to preserve a published percentage would be backwards.**

| `W` | all | pre-2020 | 2020–2022 | 2023–2025 |
| :--- | ---: | ---: | ---: | ---: |
| 38 | 197,007 (97.58%) | 133,507 (97.90%) | 34,311 (97.52%) | 29,189 (96.18%) |
| 46 | 197,007 (97.58%) | 133,507 (97.90%) | 34,311 (97.52%) | 29,189 (96.18%) |
| 77 | 197,007 (97.58%) | 133,507 (97.90%) | 34,311 (97.52%) | 29,189 (96.18%) |
| 91 | 197,007 (97.58%) | 133,507 (97.90%) | 34,311 (97.52%) | 29,189 (96.18%) |
| 107 | 196,674 (97.41%) | 133,319 (97.76%) | 34,256 (97.36%) | 29,099 (95.88%) |
| 108 | 196,654 (97.40%) | 133,307 (97.76%) | 34,253 (97.35%) | 29,094 (95.87%) |
| 150 | 195,689 (96.92%) | 132,822 (97.40%) | 34,079 (96.86%) | 28,788 (94.86%) |
| 213 | 193,270 (95.73%) | 132,221 (96.96%) | 33,877 (96.29%) | 27,172 (89.53%) |

**The aggregate hides a cohort-asymmetric loss.** At `W = 108` the pooled retention is **97.40%** — the figure `0070` corrected from 97.6% — and the per-cohort line is **97.8 / 97.4 / 95.9**. At `W = 213` the 2023–2025 cohort retains **89.53%** against **96.96%** pre-2020 — a **10.5%** loss against **3.0%**. Both figures reproduce the task sheet's corrected pair (10.5% against 3.0%, `0070` ruling 8 and `0073` §1). Without this line, whether the modern cohort survives to the headline in usable numbers is invisible — and it is the cohort a roadmap cares about most.

## 6. Drop counts — per show and per outcome

*Measured on: b: position-5 build of 2026-08-16.*

**This is a COVERAGE COUNT, not an invariant** (`0074` ruling 3). Records examined and records dropped are reported; nothing is asserted.

- Records examined for set membership: **6,065,610**
- Pairs examined: **278,452**
- Records dropped (`number ∉ E`, or a missing season/number): **0**
- Distinct dropped `(season, number)` pairs: **0**; shows with any drop: **0** of 1,138
- **Per show**, as a distribution over the 1,138 shows examined (records dropped → shows): **0 → 1,138**. The full per-show file is `processed/step8/b/drop_counts_per_show.csv`; it is reproduced here as a distribution rather than 1,138 identical rows.
- **Per outcome**: pairs whose entire S2 evidence was dropped — **0**
  - as a share of Never started **at position 5 = 33,373**: **0.0000%**
  - reported alongside, post-liveness Never started = **32,769**: **0.0000%**

The drop count is a property of the filter, so it measures against **what entered it** — position 5 (`0070` ruling 6). The difference between the two denominators is exactly the 604 never-started liveness exclusions, and that is itself informative.

### The denominator — the open item, all three readings, and what would close it

*Measured on: b: position-5 build of 2026-08-16.*

`0074` ruling 4 publishes **6,065,704 against 6,065,610**, both reporting 0 drops, and rules the difference **reported, not reconciled**, routed to Step 14. **This instance produces 6,065,610 — reading B.** All three readings are measured on this build:

| Reading | D11 applied to | Records examined | Records dropped | Waterfall line 1 |
| :--- | :--- | ---: | ---: | ---: |
| **A** | nowhere | 6,065,704 | 0 | 220,107 |
| **B — this instance** | the S2 side only | 6,065,610 | 0 | 220,107 |
| **C** | both seasons | 6,065,537 | 0 | **220,103** |

**The decomposition, which is what decides whether this is closable.** D11 discards **73 in-frame S1 records** and **94 in-frame S2 records**, **167 in total.** `0074` ruling 4 recorded the arms' gap as **94** — that is the **S2-side component alone**, which is the difference between readings A and B. Applying D11 everywhere moves the figure by **167**, not by 94, so the two published figures are separated by one quantity and the third reading by another. **The two-figure framing understates the spread.**

**Why reading B, stated as a reason and not a preference.** D11 says every record with `watched_at ≥ tau_pull` is discarded from **every** computation, and this instance applies it everywhere **except** the S1 completion walk. The exception is not chosen here: `0068` **rules waterfall line 1 at 220,107 as published**, and 4 pairs reach that count only on a completing record D11 would discard, so reading C cannot produce the ruled base. The coverage denominator is then a **consequence** of the record set the pipeline actually examines. Reading A is not available at all — it would apply D11 nowhere on either side.

**Is it closable rather than a Step 14 limitation? Yes — and the reason is the decomposition above.** The denominator is not an independent question. It is fully determined by one choice: **whether D11 is applied to the S1 completion walk** — which is exactly the question `0068` records as **OPEN** when it rules line 1 at 220,107. Close that and the denominator closes with it, in one direction or the other: **C with line 1 = 220,103, or B with line 1 = 220,107.** There is no third input and no residual judgment. **What is not closable by an arithmetic argument is the choice itself**, because it is a ruling on the base rather than a measurement — but the two arms are not disagreeing about a fact here, and both of the numbers `0074` publishes belong to the same one-bit choice. **This instance does not close it and does not reconcile it; it states what closing it would consist of.**

**One thing does not move under any reading: all three report 0 records dropped**, and nothing downstream depends on the denominator.

**The zero is a measured zero.** Every one of the 6,065,610 records was tested for membership in its season's listed set `E`, and none failed. Direction had any been dropped: it would **inflate** Never started, the same direction as D4 and D9.

## 7. D2 — negative-lag report, split THREE ways

*Measured on: b: position-5 build of 2026-08-16.*

A tie is its own category, not a tiebreak (`0070` ruling 5). **168 pairs in line 1 have both terms of the `max()` binding on the same date**; of those, 7 also carry a negative lag.

| Population | n | Negative lag | share | S2 finale binds | S1 completion binds | BOTH bind |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| position3_220107 | 220,107 | 64,321 | 29.22% | 58,584 | 5,730 | 7 |
| position4_201900 | 201,900 | 49,708 | 24.62% | 44,177 | 5,524 | 7 |
| APPLY_position5_196654 | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| DERIV_position5_147370 | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |

**The population is not stated in the spec at the point of use**, so all four are reported and each is labelled. S1-term negative lags are the actual test of the first-pass choice and should be small; S2-finale-term negative lags are the normal case for anyone who watched a weekly season while it was airing, and their size is information about the frame's cadence mix rather than about data quality.

## 8. D3′ — resumption rate, every `W` arm, each denominator its own

*Measured on: b: position-5 build of 2026-08-16.*

Of pairs scored **Started and left at `tau2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ tau_pull`, the share completing within `[tau2, tau2 + H)`. **Each arm's denominator is its own and each population's is its own** (`0069` item 5).

**APPLY** — Step 8's right-censored population at each arm

| `W` | Started-and-left | cleared | cleared share | completing | share completing |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 38 | 19,433 | 19,355 | 99.60% | 1,753 | 9.06% |
| 46 | 19,445 | 19,354 | 99.53% | 1,664 | 8.60% |
| 77 | 19,352 | 19,173 | 99.08% | 1,411 | 7.36% |
| 91 | 19,234 | 19,005 | 98.81% | 1,255 | 6.60% |
| 107 | 19,056 | 18,835 | 98.84% | 1,157 | 6.14% |
| 108 | 19,042 | 18,819 | 98.83% | 1,146 | 6.09% |
| 150 | 18,676 | 18,376 | 98.39% | 984 | 5.35% |
| 213 | 18,054 | 17,644 | 97.73% | 816 | 4.62% |

**DERIV** — Step 8's right-censored population at each arm

| `W` | Started-and-left | cleared | cleared share | completing | share completing |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 38 | 17,054 | 16,979 | 99.56% | 1,534 | 9.03% |
| 46 | 17,080 | 16,994 | 99.50% | 1,459 | 8.59% |
| 77 | 17,009 | 16,846 | 99.04% | 1,234 | 7.33% |
| 91 | 16,906 | 16,698 | 98.77% | 1,095 | 6.56% |
| 107 | 16,754 | 16,562 | 98.85% | 1,015 | 6.13% |
| 108 | 16,744 | 16,550 | 98.84% | 1,006 | 6.08% |
| 150 | 16,433 | 16,154 | 98.30% | 866 | 5.36% |
| 213 | 15,868 | 15,483 | 97.57% | 718 | 4.64% |

**The cleared-share series on APPLY is 99.53% at `W = 46` down to 97.73% at `W = 213`**, which is the series `0075` ruling 1 adopts. The superseded 95.98% → 91.34% was measured on the **amendment's uncensored estimation sample**; the population is stated here at the point of use, on Step 8's right-censored populations.

**The series is not monotone between `W = 91` (98.81%) and `W = 107` (98.84%)** — an open item at `0076` §5, reproduced here rather than smoothed. The clearance condition contains `W` twice, once in `tau2` and once in the `+ 2H` horizon, and the Started-and-left denominator is itself re-derived at every arm, so the series is not required to be monotone. **Reported, not resolved.**

**Reported alongside and labelled a COUNT, not a rate: 3,440 Started-and-left pairs completing S2 at any point before `tau_pull`.**

- **Population:** the Step 5 UNCENSORED CLEAN-RECORD ESTIMATION SAMPLE of 128,099 -- NOT APPLY and NOT DERIV. Measured at decisions/0034 Sec 3, where the Started-and-left group is 17,420 before the amendment and 15,174 after.
- **Why Step 14 calls it a floor:** that sample excludes what the Step 5 waterfall drops and is not right-censored, which is why Step 14 calls it a floor.
- **Exposure weighting, stated at the point of use:** weighted by SHOW RECENCY: 'at any point before tau_pull' gives a 2016 title about ten years of observation and a 2025 title about eight months, so it is an exposure-weighted count and not a rate.
- **Restated, not recomputed.** The spec forbids reporting it against APPLY or DERIV, so no analogue of it is computed on either population here. **Its build is `0034`'s, not this one's** — which is exactly why `0078` requires the label.

## 9. D8 — never-started post-window diagnostic

*Measured on: b: position-5 build of 2026-08-16.*

Measured over `[tau1, tau1 + H) = [tau1, tau2)` — **not to the pull date**. Direction: **DOWN** on the headline.

| Population / position | Never started | (i) any S2 episode in the horizon | share | (ii) satisfies the Continued condition | share |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 2,733 | 8.19% | 1,820 | 5.45% |
| APPLY_position6_post_liveness | 32,769 | 2,733 | 8.34% | 1,820 | 5.55% |
| DERIV_position5 | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |
| DERIV_position6_post_liveness | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |

**The spec does not say whether D8 sits pre- or post-liveness**, so both are reported and labelled. D8(ii) is the only bound on the never-started boundary and its size is Step 14's ledger item 10.

## 10. D9 — split-artifact counts, both halves, **both keys**

*Measured on: b: position-5 build of 2026-08-16.*

Signature: one show ID carrying S1 and not S2 for that user, another carrying S2 and not S1, and the two slugs normalise to the same title key. **IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND**

**Four numbers, not three** (`0078` §3): half (a) under strict and loose, half (b) under strict and loose. The requirement follows from `0074` ruling 5's own reason — the loose count publishes **because it bounds how wrong strict could be** — and that reason applies to half (b) exactly as to half (a). Publishing the bound for one half and withholding it for the other leaves the reader unable to bound the total, and **the error runs opposite to D9's own lower-bound caveat**.

Candidate `(user, show)` pairs examined across the whole sweep: **726,103** — 435,643 carrying S1 and not S2, 8,834 carrying S2 and not S1, 281,626 carrying both.

### The keys, which are now defined in the spec

**`0074` ruling 5 ruled STRICT; `0076` §3 defined both keys**, because "strict" and "loose" had existed only inside one instance's code and the ruled key was undefined on every surface an isolated instance reads.

| Key | Definition | Complementary signature pairs |
| :--- | :--- | ---: |
| `STRICT` | re.sub(r"[^a-z0-9]", "", slug.lower()) -- strip nothing else | 0 |
| `LOOSE` | remove a trailing four-digit year, then apply STRICT | 75 |
| `LOOSE_variant_any_trailing_4_digits` | 'four-digit year' read as ANY trailing four-digit group | 75 |
| `THIRD_KEY_NOT_USED` | a trailing digit group of ARBITRARY length -- reduces `the-100` to `the` | 76 |

**The two admissible readings of "a trailing four-digit year" agree on this data** — restricting the four digits to `19xx`/`20xx` and not restricting them both give 75. **The third key — a trailing digit group of arbitrary length, which reduces `the-100` to `the` — gives 76 here.** That is not a key of this study; it is measured so that the divergence `0076` describes is visible on this instance's own data rather than only in the decision log.

### Half (a) — fabricated never-started rows

| Population / position | Never started | STRICT (ruled) | LOOSE (alongside) | Share, loose |
| :--- | ---: | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 0 | 6 | 0.0180% |
| APPLY_position6_post_liveness | 32,769 | 0 | 6 | 0.0183% |
| DERIV_position5 | 9,145 | 0 | 0 | 0.0000% |
| DERIV_position6_post_liveness | 9,145 | 0 | 0 | 0.0000% |

### Half (b) — the silently deleted S1-failing counterparts

**Measured on position 3's drop set** (`0075` ruling 2), which this run writes as a deliverable. These pairs carry S2 evidence and no S1 evidence, so they fail the S1 completion rule and never enter the analysis population at all. They are unreported unless counted here, and they are the counterpart of the fabricated never-started rows half (a) counts.

| | STRICT (ruled) | LOOSE (alongside) |
| :--- | ---: | ---: |
| B-side pairs on frame shows | 0 | 27 |
| of those, present in the position-3 drop set | 0 | 27 |
| of those, in the S2-evidence-and-no-S1-evidence subset | 0 | 27 |

Every one of the 27 loose-key B-side pairs is accounted for inside the drop set — **which is the check that the side output is the right population and not merely a convenient one.** **The strict zero is a computed zero on a present input, not a zero returned by a missing one**, which is the distinction `0079` §1 exists to preserve.

**The STRICT key finds ZERO complementary pairs: no two distinct show IDs in this sweep carry the same slug modulo punctuation. The entire D9 signal therefore comes from year-stripping, which CANNOT distinguish a Trakt metadata split from a REMAKE or a national version sharing a title.** The largest loose clusters are `thetwilightzone` (10), `thetraitors` (7), `manhunt` (5), `thedevilyouknow` (2), `unsolvedmysteries` (2), `coldcasefiles` (2), `thetomandjerryshow` (2), `thesewoodsarehaunted` (2) — remakes and national versions, not split metadata.

**Why the loose count publishes even though strict is ruled:** The loose count BOUNDS HOW WRONG STRICT COULD BE, and the error runs OPPOSITE to D9's own lower-bound caveat: D9 warns that its count misses splits, while the loose key catches non-splits. Both directions are live and neither number is a measured split rate.

Direction: half (a) INFLATES Never started; half (b) removes a pair that should have been in the population. Step 9 bounds D9 and publishes it ALONGSIDE, never folded in.

## 11. D4 — S3 without S2

*Measured on: b: position-5 build of 2026-08-16.*

Pairs scored Never started that carry S3-or-later episode records on that show and **no S2 episode record at all**. Emitted here because Step 8 holds the episode-level evidence and Step 9 does not (`0070` ruling 7). Direction: **inflates** Never started; Step 9 bounds it and publishes it **alongside**, never folded in.

| Population / position | Never started | S3-without-S2 | Share |
| :--- | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 428 | 1.2825% |
| APPLY_position6_post_liveness | 32,769 | 426 | 1.3000% |
| DERIV_position5 | 9,145 | 0 | 0.0000% |
| DERIV_position6_post_liveness | 9,145 | 0 | 0.0000% |

**The DERIV zero is structural, not a measurement of nothing**: DERIV requires S2 evidence, and a D4 pair has none by definition.

## 12. D12 — per-bucket show and pair counts, all five buckets

*Measured on: b: position-5 build of 2026-08-16.*

| Bucket | Shows | Pairs, position 4 | Pairs, APPLY position 5 | Pairs, DERIV position 5 |
| :--- | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | 0 | 0 |
| C1 | 206 | 41,246 | 40,365 | 29,493 |
| C2 | 340 | 60,532 | 58,811 | 44,500 |
| C3 | 167 | 28,398 | 27,573 | 20,783 |
| C4 | 425 | 71,724 | 69,905 | 52,594 |

**Shows within 1 day of a bucket boundary: 7** of 1,138 examined. **C0 = 0 of 1,138 shows examined** — a measured zero, not an unexamined one.

## 13. Metadata-disagreement counts

*Measured on: b: position-5 build of 2026-08-16.*

| Flag | Shows | Pairs at position 4 |
| :--- | ---: | ---: |
| `s1_count_disagreement` | 0 | 0 |
| `s2_count_disagreement` | 0 | 0 |
| `s1_aired_lt_listed` | 0 | 0 |
| `s2_aired_lt_listed` | 0 | 0 |

**Every flag is 0 of 1,138 shows EXAMINED, not 0 because nothing was looked at.**

Direction, named as required: a listed-but-unaired S2 episode raises L2, which tightens ceil(0.90 x L2) and pushes real completers out of Continued into Started-and-left -- it OVERSTATES abandonment; where F2 never aired, Continued is unreachable on that show.

## 14. `pull_date`, fetch window, and discarded records

*Measured on: b: position-5 build of 2026-08-16.*

- `pull_date` = **2026-08-11**, `tau_pull` = **2026-08-11T00:00:00Z**
- Earliest per-user fetch: **2026-08-11T05:01:26.447766+00:00**
- Latest per-user fetch: **2026-08-11T23:10:31.236946+00:00**
- Records discarded for `watched_at >= tau_pull`: **1,734**, of which **167** are in-frame S1/S2 episode records

The discarded tail is about one day of activity for early-fetched users and about two for late-fetched ones; it is not evenly distributed.

### The D11 open question, measured rather than assumed

`0068` rules line 1 at **220,107 as published** and records separately as **OPEN** whether D11 moves it. Measured here: applying D11 to the S1 completion walk as well gives **220,103**, a difference of **4** pairs. **All 4 are removed at position 5 under either reading** — checked row by row, not argued — because their first-pass completion instant is at or after `tau_pull`, so `T0` is at or after 2026-08-10 and D10 removes them. **Lines 4 through 7 and every published figure are identical under both readings; only lines 1, 2 and 3 move.** The table column `s1_completion_used_a_post_cutoff_record` is what carries this question downstream.

## 15. Outcome states, channel pairs, and the scope qualifier

*Measured on: b: position-5 build of 2026-08-16.*

| Population | Position | Never started | Continued | Started and left | Total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| APPLY | position5 | 33,373 | 144,140 | 19,141 | 196,654 |
| APPLY | position7 | 32,769 | 144,140 | 19,042 | 195,951 |
| DERIV | position5 | 9,145 | 121,382 | 16,843 | 147,370 |
| DERIV | position7 | 9,145 | 121,382 | 16,744 | 147,271 |

**Never started is a 108-day statement and Continued is a 199-day statement.** The two published categories are measured over different horizons and must never be described as measured alike.

**Emitted beyond the required list** (`processed/step8/b/results.json`, `emitted_beyond_the_required_list`), because Step 9 and Step 10 would otherwise rebuild them: the liveness exclusions decomposed, the insertion-dormancy channel pairs — **90 started-and-left and 207 never-started on APPLY, 89 and 3 on DERIV** — and the `p = 1.0` residual (1,230 on APPLY, 1,056 on DERIV, post-position-7).

**The scope qualifier travels with anything that carries the Step 9 bound**: covering with respect to INSERTION-DORMANCY, exhaustively; open only across CHANNEL CLASSES (D4, D9). D4 and D9 publish alongside and are never folded in. Step 8 does not compute the bound, but it produces the position-6 population the bound is stated on, so any table or note carrying the bound carries this qualifier (decisions/0062).

**The account base.** 2,549 accounts are in the sweep and 2,422 reach the position-5 population. Accounts that were skipped, discarded over tolerance or never attempted are **absent, not empty** — asserted as a data check, not assumed; see `artifacts/step8-invariants-b.md` §8.

## 16. Discovery channel — every unit, each with its consumer

*Measured on: b: position-5 build of 2026-08-16.*

**Two boolean columns, not one categorical** (`0070` ruling 3). **Publish the overlap in every unit, each with its consumer named** (`0079` §3) — **picking one leaves another consumer holding a wrong-unit figure.** `0070` ruling 3 said *"324 users"* and named no population, which is the shape that has recurred through this entire chain, in the ruling written to fix a different unlabelled figure.

| Unit | n | Channel A only | Channel B only | **Both** | Neither | Consumer |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| Discovery-pool **usernames** | 5,694 | 3,672 | 1,698 | **324** | 0 | Step 3's seeding-bias statement; **Step 14 ledger item 1** — the pool's composition |
| **Accounts pulled** (Step 4 `complete`) | 2,549 | 1,436 | 935 | **178** | 0 | **Step 4 coverage reporting** |
| **Accounts** in the position-5 population | 2,422 | 1,349 | 899 | **174** | 0 | **Step 11** — it recomputes the headline within each channel, so it cuts the analysis population, not the pool |
| **Pairs** in the position-5 population | 196,654 | 108,486 | 70,385 | **17,783** | 0 | **Step 11** — the headline is over pairs on the position-5 row set |

**All four readings reproduce the ruled figures exactly** — 324 of 5,694 usernames, 178 of 2,549 accounts pulled, and 174 of 2,422 accounts / 17,783 of 196,654 pairs in the position-5 population (`0078`, `0079` §3). `0079` corrects the mapping as dictated: **Step 11 takes the position-5 population, and the 5,694 is the pool statistic** — the reverse of the ruling's first wording, and the files show the reverse. Step 11 tests whether discovery method biased the pool, so a single categorical value would either DROP the overlap or assign it arbitrarily, and the arbitrary assignment would be invisible in the dual diff. Two flags let Step 11 cut on either channel or on the overlap.

**One measured detail, so it is not mistaken later for a disagreement about the population.** The pool file holds **5,694 rows** and **5,693 distinct slugs case-insensitively**: one account appears as two case variants, one flagged channel B and one flagged both. **The published population is the row count, 5,694, and the overlap is 324 under both readings**, so nothing moves — measured rather than assumed inert.

## 17. The column set — 89 enumerated names

*Measured on: b: position-5 build of 2026-08-16.*

**`0080` §1 enumerates the column set rather than counting it, `0081` extends it to 88 and `0082` to 89.** This instance emits **89**, exact-match to the enumerated list: **True**, and in the enumerated order. The full list is in `artifacts/step8-waterfall-b.json` → `analysis_table.column_names`. **The arms converged on the 87 names last run, but converged is not specified**, and Step 8b's schema is built on this vocabulary, so it is fixed before the schema exists.

**Changed from this arm's last confirmed run:** `silent_at_tau1` and `p_at_bound` are **added**; nothing is dropped. **The two free drops stand** — `f2_in_A_H` is derivable as `max_episode_in_A_H == s2_F`, and `max_episode_in_A` is read by nothing downstream.

**`silent_at_tau1` is the column that was worth restoring, and the reason is not symmetry.** It is **not recoverable from `live` and `outcome` on Continued rows** — `live` is true for every Continued pair *regardless of silence*, because the rule's second conjunct is `NOT Continued`. Without it, **the Continued-and-silent count cannot be recomputed from Step 8's table**; §20 below reports that count as an aggregate as well, so the figure survives independently of the column.

**Reported defect in the spec, not worked around.** task-sheet.md Step 8's struck bullet reads 'SUPERSEDED -- the count is replaced by the ENUMERATION above (0080, extended to 88 by 0081)', while the enumeration above it carries 89 names and its own heading says 89 (0082). The '88' inside the strike-through is stale by one ruling. It is INSIDE a strike-through and the live enumeration is unambiguous, so it changes nothing here -- REPORTED rather than silently resolved, because the same shape (a superseded count left standing beside its replacement) is what 0081 Sec 2 was written about.

## 18. `p_at_bound` — and the two meanings it separates are the same set

*Measured on: b: position-5 build of 2026-08-16.*

**`0082` §2 adds a boolean separating the two meanings of `p = 1.0`**: the rank numerator **saturated at `L2`**, or the pair **left at the final episode**. Step 10 publishes the abandonment distribution off `abandonment_point_p`, so a spike at 1.0 must be separable. The column is emitted **TRUE on the rank-saturation reading**, which is the phrase the ruling uses, **FALSE otherwise**, and **null where `p` is null**.

| Population / position | rows with `p = 1.0` | `p_at_bound` TRUE | `p_at_bound` FALSE | cross-check: `m_H == s2_F` | classes sum |
| :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY_position5 | 1,246 | 1,246 | 0 | 1,246 | **True** |
| APPLY_position6_post_liveness | 1,230 | 1,230 | 0 | 1,230 | **True** |
| DERIV_position5 | 1,072 | 1,072 | 0 | 1,072 | **True** |
| DERIV_position6_post_liveness | 1,056 | 1,056 | 0 | 1,056 | **True** |

**The totals reproduce the ruling exactly — 1,246 at position 5 and 1,230 post-liveness on APPLY — and the two classes sum to them.**

**And the measured finding is that the two meanings are the same set, by construction rather than by accident.** On the adopted **rank** form `p = |{e ∈ E2 : e ≤ m_H}| / L2`, set membership puts `m_H ∈ E2`, so the numerator equals `L2` **iff** no listed episode exceeds `m_H`, **iff** `m_H = max(E2) = F2` — which *is* "left at the final episode." Both readings were computed separately here and agree row for row: **1,246 and 1,246.** So the FALSE class is **empty by construction**, and the column separates nothing on this data.

**The two meanings are distinguishable only under the withdrawn raw-ratio form** `p = m_H / L2`, where a numbering gap makes `F2 > L2` and the ratio can saturate somewhere other than the finale. That form was withdrawn at the Step 1 gate and must not be reinstated. **Reported, not resolved: the column is emitted as ruled, and its degeneracy is stated so Step 10 does not read an all-TRUE column as a finding.**

## 19. `action` — counts by type, never a row-level column

*Measured on: b: position-5 build of 2026-08-16.*

`action` is record-level and the row is a pair, so a single value per row would assert one action per pair, which is false (`0070` ruling 4). The table carries eight count columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is fixed by `0080`'s enumeration**, which names all eight. Step 1 already ruled that check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the logging client rather than of the viewing, so it is **not an outcome variable**. Step 13's arm reads the counts: check-in-only iff its `checkin` count is positive and `scrobble` and `watch` are zero.

## 20. Continued-and-silent — the count `silent_at_tau1` exists to preserve

*Measured on: b: position-5 build of 2026-08-16.*

**Emitted as an aggregate as well as a column**, so the figure survives independently of either. `live` is TRUE for every Continued pair **regardless of silence**, because the liveness rule's second conjunct is `NOT Continued` — so this count is what the second conjunct is worth, and it is **the size of the outcome-conditioning at waterfall line 6**: the pairs the conjunct **saves** from exclusion.

| Population (position 5) | Continued | **Continued and silent at `tau1`** | silent at `tau1`, all rows | silent and NOT Continued = the exclusions |
| :--- | ---: | ---: | ---: | ---: |
| APPLY_position5 | 144,140 | **652** | 1,355 | 703 |
| DERIV_position5 | 121,382 | **652** | 751 | 99 |

**This reproduces the published 652** — the figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation. On APPLY the silence test alone would exclude 1,355 pairs; the `NOT Continued` conjunct cuts that to 703 by sparing 652 Continued pairs. **DERIV's Continued-and-silent count is the same 652**, because every one of those pairs carries S2 evidence by definition of Continued.

## 21. Where two faithful instances could still differ

*Measured on: b: position-5 build of 2026-08-16.*

1. **THE COLUMN SET IS ENUMERATED AT 89, AND ONE STALE COUNT SURVIVES INSIDE A STRIKE-THROUGH.** `task-sheet.md` Step 8's struck bullet reads *"the count is replaced by the ENUMERATION above (`0080`, extended to 88 by `0081`)"* while the enumeration above it carries 89 names and its own heading says 89 (`0082`). **The '88' is stale by one ruling.** It is inside a strike-through and the live enumeration is unambiguous, so this instance emits the 89 enumerated names and nothing moves — but this is the third occurrence of the shape `0081` §2 was written about, a superseded count left standing beside its replacement in the file an isolated instance reads cold. Reported.
2. **`p_at_bound` SEPARATES TWO CLASSES THAT ARE THE SAME SET.** `0082` §2 defines TRUE as the rank numerator saturated at `L2` and FALSE as the pair having left at the final episode. Under the adopted rank form with set membership, `m_H ∈ E2`, so the numerator is `L2` **iff** `m_H = max(E2) = F2` — the two definitions select the identical rows, measured here at 1,246 and 1,246. **The FALSE class is empty by construction.** The column is emitted on the reading the ruling names, and a second instance that emits it on the other reading gets the identical column — so this cannot produce a diff, but it can produce two different *justifications*, and the degeneracy is what Step 10 needs told. Reported, not resolved.
3. **D11 and waterfall line 1.** `0068` rules 220,107 and leaves the D11 question open. Lines 1–3 are that figure here and would be 220,103 under the other reading; lines 4–7 are identical either way, verified row by row.
4. **The set-membership denominator — the open item, and it is CLOSABLE.** `0074` ruling 4 publishes 6,065,704 against 6,065,610 unreconciled and routes it to Step 14. This instance produces **6,065,610** — D11 on the S2 side, the S1 side carried because `0068` rules line 1 at 220,107 as published. The other readings are 6,065,704 (D11 nowhere) and 6,065,537 (D11 on both). **The decomposition is 73 S1-side records + 94 S2-side = 167**, so `0074`'s 94 is the S2-side component alone and the two-figure framing understates the spread. **The denominator is not an independent question**: it is fully determined by whether D11 applies to the S1 completion walk, which is `0068`'s own OPEN item. Closing that closes this — reading C with line 1 = 220,103, or reading B with line 1 = 220,107. **Reported, not reconciled here**; all three drop zero records and nothing downstream depends on the denominator.
5. **D3′'s cleared shares are not monotone between `W = 91` and `W = 107`** — 98.81% then 98.84% on APPLY. An open item at `0076` §5, reproduced rather than smoothed.
6. **D8's position.** Pre- or post-liveness is unstated. Both are reported.
7. **D2's population.** Unstated at the point of use. Four are reported and each labelled.
8. **D9's third key.** The spec now defines strict and loose (`0076` §3). On this data the third key — a trailing digit group of arbitrary length — gives **76** complementary signature pairs against loose's **75**, reproducing the divergence `0076` describes. It is measured and not used.
9. **The grain of D9 half (b).** `0078` §3 requires both halves under both keys, which is done; but the unit of half (b) is not fixed. This instance reports **B-side pairs on frame shows**, then how many of them sit inside the position-3 drop set, which is the only reading on which the drop set is load-bearing.
10. **The provenance string itself.** `0078` and `0079` §2 require every count to name the build it was measured on, and fix no format. This instance emits one build identifier plus an input fingerprint (size and mtime of every input) and a SHA-256 of its own pipeline sources. **A different arm will phrase the label differently and no figure moves**; what matters is that both arms label everything rather than two figures.
11. **The shape of the position-3 drop set — ruled, and it agrees.** `0075` ruling 2 named an empty set; `0077` §2 restates it as the pair universe less the completers, 58,345 pairs, with distinct-episode counts and the show's threshold. This instance reported the same count on the previous build, so the restatement removes the choice without moving a figure.
12. **The discovery-channel overlap, now published in every unit.** `0079` §3 names three and this instance measures four numbers: 324 of 5,694 pool usernames, 178 of 2,549 accounts pulled, 174 of 2,422 accounts and 17,783 of 196,654 pairs in the position-5 population. All four reproduce the ruled figures.
13. **The waterfall's unit.** Pairs are primary; users and shows are reported alongside because position 2 is explicitly a filter on shows.
14. **Undated records.** 379 records in the sweep carry no `watched_at`. None is an in-frame S1/S2 episode record, so they touch no outcome. They are **not** discarded by D11, which removes `watched_at >= tau_pull`; a reading that requires a record to be positively "dated before `tau_pull`" would drop them from the liveness evidence. Measured inert: the exclusion counts are identical either way at every arm.
15. **DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore not the adopted contamination exclusion, and is labelled as such rather than silently conflated with APPLY's.
16. **At `W = 213` the DERIV started-and-left exclusion component is 147 while APPLY's is 148.** No published figure covers DERIV per arm above `W = 108`, so this is new rather than divergent, and it is stated so it is not read as an error later.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
