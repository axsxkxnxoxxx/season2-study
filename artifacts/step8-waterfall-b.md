# Step 8 — filter waterfall and required counts (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**Every figure below states its population.** There are two and they differ by construction: **APPLY = 196,654** (waterfall line 1 less D10 — the position-5 output, and what position 6 filters) and **DERIV = 147,370** (Step 5 line 4 less D10, which requires S2 evidence). Step 8 produces both (`decisions/0070` ruling 1).

**Constants.** `W = 108` days (`0026`), `H = 91` days (D10), `tau_pull = 2026-08-11T00:00:00Z` (`0011`). `tau1 = ⟦T0⟧ + W × 24h`, `tau2 = ⟦T0⟧ + (W + H) × 24h = ⟦T0⟧ + 199 days`. Every boundary test is the half-open UTC-instant form of Step 1 §2.4; `date(watched_at) <= T1` appears nowhere in the implementation.

**The analysis table is in `processed/`, not here.** `processed/step8/b/analysis_table.csv.gz`, 196,654 rows × 87 columns. Its row set is the **position-5 population**, carrying the position-6 flag `live` and the position-7 `outcome`; the post-position-7 row set is `live == True`, DERIV is `in_deriv`. The 703 excluded rows are kept **in the file** with `live = False`, because Step 9's bound endpoints are built from their outcome states and rebuilding them downstream would be a second definition of the filter.

---

## 1. The filter order

Applied in **exactly** this order (`decisions/0029`). The final row set commutes; the per-filter sample size does not, which is the whole reason the order is mandated.

1 Step 2 frame  
2 L2 = 1 exclusion  
3 S1 completion rule  
4 contamination exclusion (Step 5)  
5 right-censoring  
6 liveness  
7 outcome assignment (two instants)  

**Waterfall line 1 is the S1-completer population, 220,107 pairs** (`0068`). No instance chooses a base. Lines 2 and 3 follow from it.

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

**DERIV's position 4 is not the adopted contamination exclusion alone**, and that is stated rather than hidden: DERIV is *Step 5 line 4* less D10, and line 4 applies three further restrictions — `has_s2`, `T0` not contaminated, completing record not post-dated — none of which is a Step 8 filter position. Emitting it here is what stops Step 9 rebuilding the population, which would be a second definition of it.

## 4. Position 6 — liveness, and the population reconciliation

The rule is **ALT-BROAD** (`0048`, restored `0054`, **approved `0064`**): a pair is **NOT LIVE iff BOTH** the account shows no insertion instant after that pair's `tau1` **AND** the pair is **NOT Continued**. **"After" is STRICT** — silent iff no insertion instant `> tau1` (`0068`). **The evidence is restricted to records dated before `tau_pull`** (`0070` ruling 2). The stored play-`id` isotonic calibration at `processed/step5/calibration.npz` is **read and never refitted** (`0029`).

| Population | n (position 5) | Excluded | Never started | Started and left | Accounts |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY | 196,654 | 703 | 604 | 99 | 216 |
| DERIV | 147,370 | 99 | 0 | 99 | 73 |

**This reconciles exactly with the expectation** — 703 from 216 accounts on APPLY (604 + 99) and 99 from 73 accounts on DERIV (0 + 99). **It is a population reconciliation and NOT an invariant.** Neither **604** (the superseded ALT answer) nor **793** (the withdrawn ALT-MATCHED answer) was produced.

**Line 6 is OUTCOME-CONDITIONAL and is reported as such.** Conjunct 2 *is* the Continued test, read at `tau2`, so position 6 evaluates a position-7 predicate. That is permitted: `|A|` and liveness are row-local predicates on the position-5 output and commute exactly, and `0029`'s ordering rationale concerns per-filter sample size, which cannot reach position 7 because outcome assignment removes no rows.

**Per-`W`-arm exclusion counts on APPLY**, so the `W`-coupling is visible:

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

**Measured on the position-4 output (201,900), which is what the mandated order censors.** `0033`'s 97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed on the **position-3** output; `0070` ruling 8 keeps the order and moves the published percentage.

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

**The aggregate hides a cohort-asymmetric loss.** At `W = 108` the pooled retention is **97.40%**, and at `W = 213` the 2023–2025 cohort retains **89.53%** against **96.96%** pre-2020 — a **10.5%** loss against **3.0%**. Without this line, whether the modern cohort survives to the headline in usable numbers is invisible.

**The comparator moved too, and the record does not say so.** `0070` corrected the 2023–2025 loss from 10.3% to 10.5% when it kept the mandated order, but the pre-2020 figure it is stated against — **2.7%** — was computed in the same superseded order and is **3.0%** here. The task sheet's sentence *"10.5% of its pairs against 2.7% pre-2020"* therefore mixes one figure from the mandated order with one from the order it replaced. **Reported, not reconciled** — it is a propagation gap in the derived-figure list, not a disagreement about the rule.

## 6. Drop counts — per show and per outcome

- Records examined for set membership: **6,065,610**
- Records dropped (`number ∉ E`, or a missing season/number): **0**
- Distinct dropped `(season, number)` pairs: **0**; shows with any drop: **0** of 1,138
- **Per outcome**: pairs whose entire S2 evidence was dropped — **0**
  - as a share of Never started **at position 5 = 33,373**: **0.0000%**
  - reported alongside, post-liveness Never started = **32,769**: **0.0000%**

The drop count is a property of the filter, so it measures against **what entered it** — position 5 (`0070` ruling 6). The difference between the two denominators is exactly the 604 never-started liveness exclusions, and that is itself informative.

**This zero is a measured zero.** Every one of the 6,065,610 in-frame S1/S2 episode records surviving D11 was tested for membership in its season's listed set `E`, and none failed. The per-show file is `processed/step8/b/drop_counts_per_show.csv`. Direction had any been dropped: it would **inflate** Never started, the same direction as D4 and D9.

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

**APPLY**

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

**DERIV**

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

**Reported alongside and labelled a COUNT, not a rate: 3,440 Started-and-left pairs completing S2 at any point before `tau_pull`.**

- **Population:** the Step 5 UNCENSORED CLEAN-RECORD ESTIMATION SAMPLE of 128,099 -- NOT APPLY and NOT DERIV. Measured at decisions/0034 Sec 3, where the Started-and-left group is 17,420 before the amendment and 15,174 after.
- **Why Step 14 calls it a floor:** that sample excludes what the Step 5 waterfall drops and is not right-censored, which is why Step 14 calls it a floor.
- **Exposure weighting, stated at the point of use:** weighted by SHOW RECENCY: 'at any point before tau_pull' gives a 2016 title about ten years of observation and a 2025 title about eight months, so it is an exposure-weighted count and not a rate.
- **Restated, not recomputed.** The spec forbids reporting it against APPLY or DERIV, so no analogue of it is computed on either population here.

**The measured cleared shares here do not match the 95.98% / 91.34% the task sheet quotes.** Those figures carry no population at their point of use; they are consistent with an **uncensored** sample, whose recent-`T0` pairs fail the clearance. Every figure in the table above is on the named, right-censored population at the named arm. **Reported, not reconciled.**

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

- Candidate `(user, show)` pairs examined across the whole sweep: **726,103**
- Complementary signature pairs, **LOOSE** title key: **75**
- Complementary signature pairs, **STRICT** title key: **0**

| Half | Population / position | Count (loose) | Count (strict) | Share of Never started (loose) |
| :--- | :--- | ---: | ---: | ---: |
| (a) fabricated Never started rows | APPLY_position5 | 6 | 0 | 0.0180% |
| (a) fabricated Never started rows | APPLY_position6_post_liveness | 6 | 0 | 0.0183% |
| (a) fabricated Never started rows | DERIV_position5 | 0 | 0 | 0.0000% |
| (a) fabricated Never started rows | DERIV_position6_post_liveness | 0 | 0 | 0.0000% |
| **(b) the silent half** — in-frame pairs dropped at S1 completion carrying the same signature | not on any retained population | 27 | 0 | — |

**The spec gives no title-normalisation rule, and the choice of one decides the whole number.** Two were run:

- **loose** — trailing four-digit year stripped, then non-alphanumerics stripped
- **strict** — non-alphanumerics stripped only -- no year stripping

**The STRICT key finds ZERO complementary pairs: no two distinct show IDs in this sweep carry the same slug modulo punctuation. The entire D9 signal therefore comes from year-stripping, which CANNOT distinguish a Trakt metadata split from a REMAKE or a national version sharing a title.** The largest loose clusters are `thetwilightzone` (10), `thetraitors` (7), `manhunt` (5), `thedevilyouknow` (2), `unsolvedmysteries` (2), `coldcasefiles` (2), `thetomandjerryshow` (2), `thesewoodsarehaunted` (2) — franchises with several distinct shows, not split metadata.

**Consequence, stated because it runs opposite to the caveat the spec supplies:** The loose counts are an UPPER bound on detected candidates, not evidence that splits occurred. D9's own lower-bound caveat concerns splits this signature misses; this finding concerns non-splits it catches. Both directions are live and the numbers must not be read as a measured split rate.

**5,997 same-title multi-ID groups** were also counted. NOT a merge count. These are (user, show) rows where the user's sweep carries another show ID with the same LOOSE title key, and the largest clusters are Doctor Who, The Office and Avatar -- remakes and national versions, not merges. Reported so the figure is not mistaken for one. Merges proper can only ADD evidence to a pair, never remove it.

Direction of half (a): DOWN on the never-started share; Step 9 bounds it and publishes it alongside.

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

**The account base.** 2,549 accounts are in the sweep and 2,422 reach the position-5 population. Accounts that were skipped, discarded over tolerance or never attempted are **absent, not empty**, and none of them contributes a row.

## 16. Discovery channel

**Two boolean columns, not one categorical** (`0070` ruling 3). Of the 5,694 pooled users, **324 are in both channels**; a single value would drop the overlap or assign it arbitrarily. Among the 2,422 accounts in the analysis population: channel A only **1,349**, channel B only **899**, **both 174**, neither **0**.

## 17. `action` — counts by type, never a row-level column

`action` is record-level and the row is a pair, so a single value per row would assert one action per pair, which is false (`0070` ruling 4). The table carries eight count columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is this instance's choice**; the spec says "counts by action type" and does not fix the grain. Step 1 already ruled that check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the logging client rather than of the viewing, so it is **not an outcome variable**.

## 18. Where two faithful instances could still differ

1. **The analysis table's row set.** The spec says "build one row per user-show pair" and "write the table to `processed/`" without naming which position's rows. This instance emits the **position-5** population with `live` and `outcome` as columns, so the post-position-7 set is a filter on it and Step 9 does not have to rebuild the 703. An instance emitting only the post-position-7 rows would be equally faithful and would produce a file with 195,951 rows. **No published count differs; the file shape does.**
2. **D11 and waterfall line 1.** `0068` rules 220,107 and leaves the D11 question open. Lines 1–3 are 220,107 here and would be 220,103 under the other reading; lines 4–7 are identical either way, verified.
3. **D3′'s cleared shares.** The task sheet quotes 95.98% at `W = 46` falling to 91.34% at `W = 213` with no population at the point of use. On the named, right-censored populations this instance measures 99.53% and 97.73% on APPLY. The direction and the shrinkage agree; the level does not. Reported, not reconciled.
4. **D8's position.** Pre- or post-liveness is unstated. Both are reported.
5. **D2's population.** Unstated at the point of use. Four are reported and each labelled.
6. **D9's title-normalisation rule.** None is specified, and it decides the number: the strict key (no year stripping) returns **0** complementary signature pairs, the loose key (year stripped) returns **75**, and the loose key's largest clusters are remakes. Two instances choosing differently would report 6 and 0 for half (a).
7. **The pre-2020 censoring comparator.** `0070` moved the 2023–2025 loss at `W = 213` from 10.3% to 10.5% but left the 2.7% it is compared against, which was computed in the superseded order and is 3.0% under the mandated one.
8. **The grain of the `action` counts.** "Per-pair counts by action type" does not fix whether the counts are split by season. This instance splits S1 and S2, because Step 13's arm needs the composition of the S2 evidence set and the S1 completion evidence separately.
9. **The waterfall's unit.** Pairs are primary; users and shows are reported alongside because position 2 is explicitly a filter on shows.
10. **Undated records.** 379 records in the sweep carry no `watched_at`. None is an in-frame S1/S2 episode record, so they touch no outcome. They are **not** discarded by D11, which removes `watched_at >= tau_pull`; a reading that requires a record to be positively "dated before `tau_pull`" would drop them from the liveness evidence. Measured inert: the exclusion counts are identical either way at every arm.
11. **DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore not the adopted contamination exclusion, and is labelled as such rather than silently conflated with APPLY's.
12. **At `W = 213` the DERIV started-and-left exclusion component is 147 while APPLY's is 148.** No published figure covers DERIV per arm above `W = 108`, so this is new rather than divergent, and it is stated so it is not read as an error later.
13. **`processed/step5/adopted_rule.json` carries revision-3 figures** (`retained 215,258`, `removed 4,849`) and is superseded by revision 6 (201,900 retained, 18,207 excluded). This instance reads the exclusion from `pair_revision5.csv` and re-asserts the Step 5 waterfall line by line before using it. `processed/` is not one of `CLAUDE.md`'s seven propagation surfaces, so the grep control does not cover the file a Step 8 implementation would reach for first.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
