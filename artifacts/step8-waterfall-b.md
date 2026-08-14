# Step 8 — filter waterfall and required counts (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**This is the RERUN ordered by the Human Lead on `decisions/0077`, which no arm had executed against.** `0077` fixes the discovery-channel overlap's missing population, restates `0075` ruling 2 — which named an empty set, since position 3 removes zero rows — and fixes the column names. `0074`, `0075` and `0076` postdate the first run and are also carried. This overwrites the previous `-b` deliverables.

**Every figure below states its population.** There are two and they differ by construction: **APPLY = 196,654** (waterfall line 1 less D10 — the position-5 output, and what position 6 filters) and **DERIV = 147,370** (Step 5 line 4 less D10, which requires S2 evidence). Step 8 produces both (`decisions/0070` ruling 1).

**Constants.** `W = 108` days (`0026`), `H = 91` days (D10), `tau_pull = 2026-08-11T00:00:00Z` (`0011`). `tau1 = ⟦T0⟧ + W × 24h`, `tau2 = ⟦T0⟧ + (W + H) × 24h = ⟦T0⟧ + 199 days`. Every boundary test is the half-open UTC-instant form of Step 1 §2.4; `date(watched_at) <= T1` appears nowhere in the implementation. **The `W` arm grid is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days** (`0075` ruling 3, the first statement of it in any file).

**The analysis table is in `processed/`, not here.** `processed/step8/b/analysis_table.csv.gz`, 196,654 rows × 88 columns. Its row set is the **position-5 population**, with `live` and `outcome` carried as **columns** (`0074` ruling 1); the post-position-7 row set is `live == True` (195,951), and DERIV is `in_deriv` (147,370). The 703 excluded rows are kept **in the file** with `live = False`, so nothing downstream has to reconstruct them — a reconstruction that agrees today is still a second definition tomorrow.

**Column names follow `0077` §3 exactly**, and every adopted name is present with no superseded form beside it: `in_apply` / `in_deriv`, `tau1` / `tau2`, `n_A` / `n_A_H` / `max_episode_in_A_H` / `f2_in_A_H`, the eight `action_count_s{1,2}_*`, `discovered_channel_a` / `discovered_channel_b`, `t0_binding_term` / `t0_date` / `s1_completion_date`, and both retained extras — `has_s3_or_later_evidence` (added this run; D4 reads it) and `s1_completion_used_a_post_cutoff_record` (the open D11-at-position-3 question reads it).

**But the ruled count of 89 columns is not reachable from the names `0077` gives, and this instance emits 88.** Reported as a defect rather than worked around. `0077` §3 states the rerun produced **88 against 87 for the same contents**, keeps *both* instances' extra columns and names **two**. This instance's previous run emitted **87 including the second of those two**; adding the first gives **88**. Reaching 89 needs **one further column that `0077` does not name** — the set arithmetic on `0077`'s own figures (88 ∪ 87 = 89 ⇒ intersection 86) implies exactly one unnamed column on the other arm, and the alternative reading is that 89 was formed as 87 + 2 while that 87 already held one of the two. **An isolated instance cannot identify it from any surface it is permitted to read, and inventing a column to hit the count would produce a different 89th and make the diff worse rather than better.** The full emitted name list is in `artifacts/step8-waterfall-b.json` → `analysis_table.column_names`.

---

## 1. The filter order, and the side output it needs

Applied in **exactly** this order (`decisions/0029`). The final row set commutes; the per-filter sample size does not, which is the whole reason the order is mandated.

1 Step 2 frame  
2 L2 = 1 exclusion  
3 S1 completion rule  
4 contamination exclusion (Step 5)  
5 right-censoring  
6 liveness  
7 outcome assignment (two instants)  

**Waterfall line 1 is the S1-completer population, 220,107 pairs** (`0068`). No instance chooses a base. Lines 2 and 3 follow from it.

**Position 3's drop set is retained as a side output** (`0075` ruling 2, **restated by `0077` §2**), at `processed/step8/b/position3_drop_set.csv.gz`. Under `0068` line 1 *is* the S1-completer population, so position 3 removes **0 from the waterfall** — which is why the ruling as first written named an empty set. The restated set is **the pair universe less the completers, 58,345 PAIRS**, carrying each pair's distinct-episode counts and the show's threshold. It is **not** the set-membership drop rule, which is a different rule, deletes **0 records**, and is counted in records rather than pairs. **D9 half (b) is measured on this set**; without it that half emits zero, and a zero there reads as a data finding rather than a missing input. **This instance's first run retained exactly this set and reports the same 58,345**, so the restatement moves no figure here — it removes the choice.

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

| # | Filter | Retained pairs | Removed | Users | Shows |
| :-- | :--- | ---: | ---: | ---: | ---: |
| 1 | Step 2 frame | 220,107 | 0 | 2,487 | 1,138 |
| 2 | L2 = 1 exclusion | 220,107 | 0 | 2,487 | 1,138 |
| 3 | S1 completion rule | 220,107 | 0 | 2,487 | 1,138 |
| 4 | contamination exclusion (Step 5, decisions/0021) | 201,900 | 18,207 | 2,481 | 1,138 |
| 5 | right-censoring | 196,654 | 5,246 | 2,422 | 1,138 |
| 6 | liveness (ALT-BROAD, approved 0064) | 195,951 | 703 | 2,421 | 1,138 |
| 7 | outcome assignment (two instants) | 195,951 | 0 | 2,421 | 1,138 |

**Position 2 removes exactly 0 pairs and 0 shows, out of 1,138 shows examined.** That is a measured zero, not an empty check. **Position 3 removes 0 by construction**, because `0068` defines line 1 as the S1-completer population — but the rule (`F1 ∈ D1` and `|D1| ≥ ceil(0.90 × L1)`, first-pass) was computed independently from the record level, and it is that computation which produced line 1. This is why the monotone-decrease invariant is coded `>=` and not `>`: **two positions here legitimately remove nothing.**

**Position 4 is narrower than its name.** The adopted Step 5 rule (`0021`) is two disjoint exclusions — S2 evidence entirely air-date-stamped (16,665) and a contaminated `T0` with no S2 evidence at all (1,542) — and **not** the Step 5 estimation-sample waterfall down to 128,099. Step 5's own waterfall was re-asserted line by line before it was used: measured [201900, 178165, 155131, 152126, 128099], expected [201900, 178165, 155131, 152126, 128099].

**`processed/step5/adopted_rule.json` is now read and cross-checked, not worked around.** `0074` ruling 6 made `processed/` the eighth propagation surface and corrected that file, which had carried revision-3 figures (4,849 removed / 215,258 retained). It now states **18,207 removed / 201,900 retained of 220,107**, and this instance measures **18,207 / 201,900 of 220,107** — agreement **True**, component by component. On the first run this file was the reason the Step 5 waterfall had to be re-asserted line by line; the re-assertion is kept, because a corrected surface is a reason to cross-check it and not a reason to stop checking.

## 3. Waterfall — DERIV

| # | Filter | Retained pairs | Removed |
| :-- | :--- | ---: | ---: |
| 1 | Step 2 frame | 220,107 | 0 |
| 2 | L2 = 1 exclusion | 220,107 | 0 |
| 3 | S1 completion rule | 220,107 | 0 |
| 4 | contamination exclusion, taken to Step 5 LINE 4 -- the adopted exclusion plus the three line-4 restrictions (has_s2, T0 not contaminated, completing record not post-dated) that define the DERIV base | 152,126 | 67,981 |
| 5 | right-censoring | 147,370 | 4,756 |
| 6 | liveness | 147,271 | 99 |
| 7 | outcome assignment | 147,271 | 0 |

**DERIV's position 4 is not the adopted contamination exclusion alone**, and that is stated rather than hidden: DERIV is *Step 5 line 4* less D10, and line 4 applies three further restrictions — `has_s2`, `T0` not contaminated, completing record not post-dated — none of which is a Step 8 filter position. Emitting it here is what stops Step 9 rebuilding the population, which would be a second definition of it (`0070` ruling 1).

## 4. Position 6 — liveness, and the population reconciliation

The rule is **ALT-BROAD** (`0048`, restored `0054`, **approved `0064`**): a pair is **NOT LIVE iff BOTH** the account shows no insertion instant after that pair's `tau1` **AND** the pair is **NOT Continued**. **"After" is STRICT** — silent iff no insertion instant `> tau1` (`0068`). **The evidence is restricted to records dated before `tau_pull`** (`0070` ruling 2). The stored play-`id` isotonic calibration at `processed/step5/calibration.npz` is **read and never refitted** (`0029`).

| Population | n (position 5) | Excluded | Never started | Started and left | Accounts |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY | 196,654 | 703 | 604 | 99 | 216 |
| DERIV | 147,370 | 99 | 0 | 99 | 73 |

**This reconciles exactly with the expectation** — 703 from 216 accounts on APPLY (604 + 99) and 99 from 73 accounts on DERIV (0 + 99). **It is a population reconciliation and NOT an invariant.** Neither **604** (the superseded ALT answer) nor **793** (the withdrawn ALT-MATCHED answer) was produced.

**Line 6 is OUTCOME-CONDITIONAL and is reported as such.** Conjunct 2 *is* the Continued test, read at `tau2`, so position 6 evaluates a position-7 predicate. That is permitted: `|A|` and liveness are row-local predicates on the position-5 output and commute exactly, and `0029`'s ordering rationale concerns per-filter sample size, which cannot reach position 7 because outcome assignment removes no rows.

**Per-`W`-arm exclusion counts, so the `W`-coupling is visible:**

| `W` | 38 | 46 | 77 | 91 | 107 | 108 | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, total | 537 | 550 | 633 | 664 | 701 | 703 | 789 | 864 |
| APPLY, started-and-left component | 52 | 56 | 79 | 89 | 98 | 99 | 125 | 148 |
| DERIV, total | 52 | 56 | 79 | 89 | 98 | 99 | 125 | 147 |
| APPLY, total, evidence NOT restricted to `< tau_pull` | 537 | 550 | 633 | 664 | 701 | 703 | 789 | 864 |

The last row is the measurement of `0070` ruling 2 rather than an assumption: **the `tau_pull` restriction is inert on the exclusion set at every arm**, because the largest insertion instant in the sweep is **2026-08-10T20:48:00Z** and D10 already forces `tau1 ≤ tau_pull − 91 d`. It bites on the robustness tail, not here.

## 5. Right-censoring, as two lines

Censored population: **the POSITION-4 output, 201,900 (the mandated order)**.

| Term | Pairs removed | Direction on the headline |
| :--- | ---: | :--- |
| `max(W, 91)` | 3,684 | **UP** on the never-started share |
| incremental `+ H` | 1,562 | **UP** on the never-started share |
| total | 5,246 | |

Both removals fall on recent S1 completers — people who found an old show lately, have the whole series available and are disproportionately likely to roll straight into S2. A single combined figure would hide the price of `H` inside a removal that predates it.

### Retained pairs per air period after right-censoring, every `W` arm

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

**This is a COVERAGE COUNT, not an invariant** (`0074` ruling 3). Records examined and records dropped are reported; nothing is asserted.

- Records examined for set membership: **6,065,610**
- Records dropped (`number ∉ E`, or a missing season/number): **0**
- Distinct dropped `(season, number)` pairs: **0**; shows with any drop: **0** of 1,138
- **Per show**, as a distribution over the 1,138 shows examined (records dropped → shows): **0 → 1,138**. The full per-show file is `processed/step8/b/drop_counts_per_show.csv`; it is reproduced here as a distribution rather than 1,138 identical rows.
- **Per outcome**: pairs whose entire S2 evidence was dropped — **0**
  - as a share of Never started **at position 5 = 33,373**: **0.0000%**
  - reported alongside, post-liveness Never started = **32,769**: **0.0000%**

The drop count is a property of the filter, so it measures against **what entered it** — position 5 (`0070` ruling 6). The difference between the two denominators is exactly the 604 never-started liveness exclusions, and that is itself informative.

### The denominator, all three readings

`0074` ruling 4 publishes **6,065,704 against 6,065,610**, both reporting 0 drops, and rules the difference **reported, not reconciled**. This instance's examined count is **6,065,610**. The other two readings on the same data are stated so the figure is not mistaken for a disagreement about the rule:

| Reading | Records |
| :--- | ---: |
| in-frame S1/S2 episode records, **before any D11** | 6,065,704 |
| **this instance** — D11 applied to the S2 side, S1 side carried | 6,065,610 |
| D11 applied to **both** seasons | 6,065,537 |

The S1 side is carried unfiltered here for one reason: `0068` rules waterfall line 1 at **220,107 as published**, and 4 pairs complete S1 only on a record `D11` would discard. **The three readings differ by 94 and by 73 records respectively, all of them post-cutoff, and all three report 0 drops.** Nothing downstream depends on the denominator. **Reported, not reconciled**, per `CLAUDE.md`.

**The zero is a measured zero.** Every one of the 6,065,610 records was tested for membership in its season's listed set `E`, and none failed. The per-show file is `processed/step8/b/drop_counts_per_show.csv`. Direction had any been dropped: it would **inflate** Never started, the same direction as D4 and D9.

## 7. D2 — negative-lag report, split THREE ways

A tie is its own category, not a tiebreak (`0070` ruling 5). **168 pairs in line 1 have both terms of the `max()` binding on the same date**; of those, 7 also carry a negative lag.

| Population | n | Negative lag | share | S2 finale binds | S1 completion binds | BOTH bind |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| position3_220107 | 220,107 | 64,321 | 29.22% | 58,584 | 5,730 | 7 |
| position4_201900 | 201,900 | 49,708 | 24.62% | 44,177 | 5,524 | 7 |
| APPLY_position5_196654 | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| DERIV_position5_147370 | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |

**The population is not stated in the spec at the point of use**, so all four are reported and each is labelled. S1-term negative lags are the actual test of the first-pass choice and should be small; S2-finale-term negative lags are the normal case for anyone who watched a weekly season while it was airing, and their size is information about the frame's cadence mix rather than about data quality.

## 8. D3′ — resumption rate, every `W` arm, each denominator its own

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
- **Restated, not recomputed.** The spec forbids reporting it against APPLY or DERIV, so no analogue of it is computed on either population here.

## 9. D8 — never-started post-window diagnostic

Measured over `[tau1, tau1 + H) = [tau1, tau2)` — **not to the pull date**. Direction: **DOWN** on the headline.

| Population / position | Never started | (i) any S2 episode in the horizon | share | (ii) satisfies the Continued condition | share |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 2,733 | 8.19% | 1,820 | 5.45% |
| APPLY_position6_post_liveness | 32,769 | 2,733 | 8.34% | 1,820 | 5.55% |
| DERIV_position5 | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |
| DERIV_position6_post_liveness | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |

**The spec does not say whether D8 sits pre- or post-liveness**, so both are reported and labelled. D8(ii) is the only bound on the never-started boundary and its size is Step 14's ledger item 10.

## 10. D9 — split-artifact counts, both halves

Signature: one show ID carrying S1 and not S2 for that user, another carrying S2 and not S1, and the two slugs normalise to the same title key. **IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND**

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

**Measured on position 3's retained drop set** (`0075` ruling 2). These are pairs that these pairs carry S2 evidence and no S1 evidence, so they fail the S1 completion rule and never enter the analysis population at all. They are unreported unless counted here, and they are the counterpart of the fabricated never-started rows half (a) counts.

| | STRICT (ruled) | LOOSE (alongside) |
| :--- | ---: | ---: |
| B-side pairs on frame shows | 0 | 27 |
| of those, present in the retained position-3 drop set | 0 | 27 |
| of those, in the S2-evidence-and-no-S1-evidence subset | 0 | 27 |

Every one of the 27 loose-key B-side pairs is accounted for inside the retained drop set — **which is the check that the side output is the right population and not merely a convenient one.**

**The STRICT key finds ZERO complementary pairs: no two distinct show IDs in this sweep carry the same slug modulo punctuation. The entire D9 signal therefore comes from year-stripping, which CANNOT distinguish a Trakt metadata split from a REMAKE or a national version sharing a title.** The largest loose clusters are `thetwilightzone` (10), `thetraitors` (7), `manhunt` (5), `thedevilyouknow` (2), `unsolvedmysteries` (2), `coldcasefiles` (2), `thetomandjerryshow` (2), `thesewoodsarehaunted` (2) — remakes and national versions, not split metadata.

**Why the loose count publishes even though strict is ruled:** The loose count BOUNDS HOW WRONG STRICT COULD BE, and the error runs OPPOSITE to D9's own lower-bound caveat: D9 warns that its count misses splits, while the loose key catches non-splits. Both directions are live and neither number is a measured split rate.

Direction: half (a) INFLATES Never started; half (b) removes a pair that should have been in the population. Step 9 bounds D9 and publishes it ALONGSIDE, never folded in.

## 11. D4 — S3 without S2

Pairs scored Never started that carry S3-or-later episode records on that show and **no S2 episode record at all**. Emitted here because Step 8 holds the episode-level evidence and Step 9 does not (`0070` ruling 7). Direction: **inflates** Never started; Step 9 bounds it and publishes it **alongside**, never folded in.

| Population / position | Never started | S3-without-S2 | Share |
| :--- | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 428 | 1.2825% |
| APPLY_position6_post_liveness | 32,769 | 426 | 1.3000% |
| DERIV_position5 | 9,145 | 0 | 0.0000% |
| DERIV_position6_post_liveness | 9,145 | 0 | 0.0000% |

**The DERIV zero is structural, not a measurement of nothing**: DERIV requires S2 evidence, and a D4 pair has none by definition.

## 12. D12 — per-bucket show and pair counts, all five buckets

| Bucket | Shows | Pairs, position 4 | Pairs, APPLY position 5 | Pairs, DERIV position 5 |
| :--- | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | 0 | 0 |
| C1 | 206 | 41,246 | 40,365 | 29,493 |
| C2 | 340 | 60,532 | 58,811 | 44,500 |
| C3 | 167 | 28,398 | 27,573 | 20,783 |
| C4 | 425 | 71,724 | 69,905 | 52,594 |

**Shows within 1 day of a bucket boundary: 7** of 1,138 examined. **C0 = 0 of 1,138 shows examined** — a measured zero, not an unexamined one.

## 13. Metadata-disagreement counts

| Flag | Shows | Pairs at position 4 |
| :--- | ---: | ---: |
| `s1_count_disagreement` | 0 | 0 |
| `s2_count_disagreement` | 0 | 0 |
| `s1_aired_lt_listed` | 0 | 0 |
| `s2_aired_lt_listed` | 0 | 0 |

**Every flag is 0 of 1,138 shows examined, not 0 because nothing was looked at.**

Direction, named as required: a listed-but-unaired S2 episode raises L2, which tightens ceil(0.90 x L2) and pushes real completers out of Continued into Started-and-left -- it OVERSTATES abandonment; where F2 never aired, Continued is unreachable on that show.

## 14. `pull_date`, fetch window, and discarded records

- `pull_date` = **2026-08-11**, `tau_pull` = **2026-08-11T00:00:00Z**
- Earliest per-user fetch: **2026-08-11T05:01:26.447766+00:00**
- Latest per-user fetch: **2026-08-11T23:10:31.236946+00:00**
- Records discarded for `watched_at >= tau_pull`: **1,734**, of which **167** are in-frame S1/S2 episode records

The discarded tail is about one day of activity for early-fetched users and about two for late-fetched ones; it is not evenly distributed.

### The D11 open question, measured rather than assumed

`0068` rules line 1 at **220,107 as published** and records separately as **OPEN** whether D11 moves it. Measured here: applying D11 to the S1 completion walk as well gives **220,103**, a difference of **4** pairs. **All 4 are removed at position 5 under either reading** — checked row by row, not argued — because their first-pass completion instant is at or after `tau_pull`, so `T0` is at or after 2026-08-10 and D10 removes them. **Lines 4 through 7 and every published figure are identical under both readings; only lines 1, 2 and 3 move.**

## 15. Outcome states, channel pairs, and the scope qualifier

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

## 16. Discovery channel

**Two boolean columns, not one categorical** (`0070` ruling 3). **Every overlap count states its population** (`0077` §1): `0070` ruling 3 said *"324 users"* and named none, and a count without its population is the shape that has recurred through this entire chain. All three populations are **measured here, not restated**:

| Population | n | Channel A only | Channel B only | **Both** | Neither |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Step 3 discovery pool (usernames) | 5,694 | 3,672 | 1,698 | **324** | 0 |
| Accounts pulled — Step 4 `complete` | 2,549 | 1,436 | 935 | **178** | 0 |
| Accounts in the APPLY position-5 population | 2,422 | 1,349 | 899 | **174** | 0 |

**Both of `0077`'s figures reproduce exactly — 324 of 5,694 and 178 of 2,549** — and the third line is the one Step 11 actually cuts on, which neither ruling states. Step 11 tests whether discovery method biased the pool, so a single categorical value would either DROP the overlap or assign it arbitrarily, and the arbitrary assignment would be invisible in the dual diff. Two flags let Step 11 cut on either channel or on the overlap.

**One measured detail, so it is not mistaken later for a disagreement about the population.** The pool file holds **5,694 rows** and **5,693 distinct slugs case-insensitively**: one account appears as two case variants, one flagged channel B and one flagged both. **The published population is the row count, 5,694, and the overlap is 324 under both readings**, so nothing moves — measured rather than assumed inert.

## 17. `action` — counts by type, never a row-level column

`action` is record-level and the row is a pair, so a single value per row would assert one action per pair, which is false (`0070` ruling 4). The table carries eight count columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is this instance's choice**; the spec says "counts by action type" and does not fix the grain. Step 1 already ruled that check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the logging client rather than of the viewing, so it is **not an outcome variable**. Step 13's arm reads the counts: check-in-only iff its `checkin` count is positive and `scrobble` and `watch` are zero.

## 18. Where two faithful instances could still differ

1. **THE COLUMN COUNT. `0077` §3 fixes the names and states 89 columns; this instance emits 88.** Every name `0077` adopts is present and no superseded form is, and both retained extras are carried. The 89th is **not named anywhere an isolated instance may read**: `0077`'s own figures give 88 ∪ 87 = 89, which implies one unnamed column on the other arm, unless 89 was formed as 87 + 2 while that 87 already held one of the two. **The ruling was written to stop Step 8b inheriting a column divergence, and on this reading it leaves one**, since an instance that guesses a 89th and an instance that does not both diverge from the other. Reported, not guessed at.
2. **D11 and waterfall line 1.** `0068` rules 220,107 and leaves the D11 question open. Lines 1–3 are that figure here and would be 220,103 under the other reading; lines 4–7 are identical either way, verified row by row.
3. **The set-membership denominator.** `0074` ruling 4 publishes 6,065,704 against 6,065,610 unreconciled. This instance examines 6,065,610; the other two readings on the same data are 6,065,704 (before any D11) and 6,065,537 (D11 applied to both seasons). The choice follows from how D11 is applied on the S1 side, which follows from `0068`'s ruled line 1. **Reported, not reconciled**; all three drop zero records.
4. **D3′'s cleared shares are not monotone between `W = 91` and `W = 107`** — 98.81% then 98.84% on APPLY. An open item at `0076` §5, reproduced rather than smoothed.
5. **D8's position.** Pre- or post-liveness is unstated. Both are reported.
6. **D2's population.** Unstated at the point of use. Four are reported and each labelled.
7. **D9's third key.** The spec now defines strict and loose (`0076` §3). On this data the third key — a trailing digit group of arbitrary length — gives **76** complementary signature pairs against loose's **75**, reproducing the divergence `0076` describes. It is measured and not used.
8. **The grain of the `action` counts.** "Per-pair counts by action type" does not fix whether the counts are split by season. This instance splits S1 and S2, because Step 13's arm needs the composition of the S2 evidence set and the S1 completion evidence separately. A pooled-count instance would report four columns rather than eight and no published figure would move.
9. **The shape of the position-3 drop set — now ruled, and it agrees.** `0075` ruling 2 named an empty set; `0077` §2 restates it as the pair universe less the completers, 58,345 pairs, with distinct-episode counts and the show's threshold. This instance's first run had already chosen that set and reports the same count, so the restatement removes the choice without moving a figure.
10. **The discovery-channel overlap on the population Step 11 cuts.** `0077` §1 states 324 of 5,694 and 178 of 2,549; both reproduce. **The overlap on the APPLY position-5 population is 174 of 2,422 accounts and is stated in no ruling** — an instance reporting only the two ruled figures and one reporting the third are both faithful.
11. **The waterfall's unit.** Pairs are primary; users and shows are reported alongside because position 2 is explicitly a filter on shows.
12. **Undated records.** 379 records in the sweep carry no `watched_at`. None is an in-frame S1/S2 episode record, so they touch no outcome. They are **not** discarded by D11, which removes `watched_at >= tau_pull`; a reading that requires a record to be positively "dated before `tau_pull`" would drop them from the liveness evidence. Measured inert: the exclusion counts are identical either way at every arm.
13. **DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore not the adopted contamination exclusion, and is labelled as such rather than silently conflated with APPLY's.
14. **At `W = 213` the DERIV started-and-left exclusion component is 147 while APPLY's is 148.** No published figure covers DERIV per arm above `W = 108`, so this is new rather than divergent, and it is stated so it is not read as an error later.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
