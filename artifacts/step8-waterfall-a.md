# Step 8 — filter waterfall and required counts, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** (`decisions/0026`) · **H = 91 days** (D10) · **`τ_pull` = 2026-08-11T00:00:00Z** (D11, `decisions/0011`)

> **THIS IS A GATE DELIVERABLE. IT PROPOSES AND ADOPTS NOTHING.** No approval is recorded here and none is implied. **Zero API calls** — every figure is computed from data already on disk. **Counts and aggregates only**: no username, no user ID and no individual watch history appears in this file or in its `.json`.

> **Every figure below states its population.** There are two and they differ by construction: **APPLY** = Step 5 waterfall line 1 less D10 = **196,654**, which is what position 6 filters; **DERIV** = Step 5 waterfall line 4 less D10 = **147,370**, which requires S2 evidence. Step 8 produces both (`decisions/0070` ruling 1).

> **RERUN.** This replaces the previous `-a` deliverable in full. `decisions/0074`, `0075` and `0076` all postdate that run, so several objects they rule on existed in one arm or neither. What changed here: **the table is now the position-5 row set with `live` and `outcome` as columns** (`0074`/1); **D9 uses the defined strict key with the loose count alongside** (`0074`/5, `0076`/3); **the set-membership rule is a coverage count and no longer an invariant** (`0074`/3); **position 3's drop set is retained as a side output** (`0075`/2); **the `W` grid is no longer this instance's choice** (`0075`/3); **`p` is labelled a CODE CHECK** (`0076`/1 — the label this instance's previous deliverable already had); and **two DATA CHECKS are added** (`0076`/2), which are the first assertions in this report that can fail on data.

---

## 1. The filter order and the waterfall, on both populations

Applied in exactly the order `decisions/0029` fixes. The final row set commutes; the per-filter sample size does not, which is why the order is written down rather than left to each instance.

| # | Filter | APPLY: retained | removed | DERIV: retained | removed |
| :-- | :--- | ---: | ---: | ---: | ---: |
| **1** | Step 2 frame | 220,107 | — | 220,107 | — |
| **2** | `L2 = 1` exclusion | 220,107 | 0 | 220,107 | 0 |
| **3** | S1 completion rule | 220,107 | 0 | 220,107 | 0 |
| **4** | contamination exclusion (Step 5) | 201,900 | 18,207 | 152,126 | 67,981 |
| **5** | right-censoring | 196,654 | 5,246 | 147,370 | 4,756 |
| **6** | liveness rule | 195,951 | 703 | 147,271 | 99 |
| **7** | outcome assignment | 195,951 | 0 | 147,271 | 0 |

**Line 1 is the S1-completer population, 220,107 pairs** (`decisions/0068`) — user-show pairs whose user completed season 1, on a frame show. Lines 2 and 3 follow from it. No base was chosen by this instance.

- **Position 2 removes exactly 0 pairs on this frame.** 0 of the 1,138 frame shows have `L2 = 1`. This is why the monotone-decrease invariant is coded `>=` and not `>` — see the invariant report.
- **Position 3 removes 0 by construction**, because line 1 is already the S1-completer population. What carries the weight here is the **independent recomputation**: the S1 completion test and the first-pass completion date were recomputed from the episode records, never read back from the Step 5 pair table. Membership agrees on all 278,452 pairs of the universe (220,107 completers both ways, 0 only mine, 0 only the published table), and the completion **date** agrees on 0 mismatches.
- **Position 4 is a different depth on the two populations.** APPLY takes Step 5 waterfall line 1; DERIV takes line 4, which additionally requires S2 evidence, an uncontaminated `T0` and a completing record that is not post-dated. The Step 5 waterfall was rebuilt from the stored per-pair flags and asserted equal to the published [201900, 178165, 155131, 152126, 128099] before use.
- **Positions 6 and 7 are ANNOTATIONS on the table, not deletions from it.** The analysis table is the **position-5 row set** and carries `live` and `outcome` as columns (`decisions/0074` ruling 1), so lines 6 and 7 above report what the liveness rule and the outcome assignment *select*, and the rows they do not select are still in the file with `live = false`. Downstream consumes rather than rebuilds.
- **Position 6 is OUTCOME-CONDITIONAL and is reported as such** (`decisions/0046`): the second conjunct of the liveness rule is the Continued test, so the outcome is evaluated before liveness is applied even though it is assigned at position 7. Permitted because the two predicates are row-local on the position-5 output and commute exactly, and because position 7 removes no rows.
- **Position 7 removes no rows.** It annotates.

### 1.1 Right-censoring, as two lines

| Term | APPLY removed | DERIV removed | Direction on the headline |
| :--- | ---: | ---: | :--- |
| `max(W, 91)` term | 3,684 | 3,352 | **UP** |
| incremental `+ H` term | 1,562 | 1,404 | **UP** |
| total | 5,246 | 4,756 | **UP** |

Both lines remove pairs whose clock start is recent, which on the uncapped `S1_completion_date` term means recent S1 completers — people who found an old show lately, have the whole series available, and are disproportionately likely to roll straight into S2. Removing likely continuers moves the never-started share **up** (Step 1 §6).

---

## 2. Position 6 — the liveness rule, and the population reconciliation

The rule is **ALT-BROAD**, approved unconditionally 2026-08-13 (`decisions/0064`): a pair is **NOT LIVE iff BOTH** (i) the account shows **no insertion instant `> τ1`** — *after* is strict — **AND** (ii) the pair is **NOT Continued**. Evidence is account-wide, runs on record **insertion** time read through the **stored** Step 5 isotonic calibration (never refitted), and is **restricted to records dated before `τ_pull`** (`0070` ruling 2).

| Population | Entering (position 5) | Excluded | never-started | started-and-left | accounts | Retained |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | **703** | 604 | 99 | 216 | 195,951 |
| **DERIV** | 147,370 | **99** | 0 | 99 | 73 | 147,271 |

**This is a POPULATION RECONCILIATION, not an invariant** (`decisions/0068`). Expected 703 on APPLY = 196,654 (604 + 99, 216 accounts) and 99 on DERIV = 147,370 (0 + 99, 73 accounts). **Measured: 703 and 99, with the same splits and the same account counts.** This is the first place Step 7's chain and Step 8's positions 1–5 have been compared: Step 7 built APPLY from the Step 5 pair table rather than through the filters. They agree to the row.

**Neither superseded answer was produced.** 604 is ALT's, 793 is ALT-MATCHED's; either would mean a superseded rule had been implemented.

**How the conjuncts select on APPLY:** conjunct 2 (NOT Continued) narrows 196,654 → 52,514; conjunct 1 (silent at `τ1`) narrows 52,514 → 703. Conjunct 1 does most of the work, which is why the count moves with `W`.

**Evidence scope, measured rather than assumed:** with the `< τ_pull` restriction 703 pairs are excluded; without it 703. The restriction is inert on the exclusion set at this arm, as `0070` recorded, because no insertion instant exceeds the calibration clamp at 2026-08-10T20:48:00Z and D10 already forces `τ1 ≤ τ_pull − 91 d`.

---

## 3. Position 7 — outcome assignment at two instants

`|A| = 0` is read at **`τ1` = ⟦T0⟧ + 108 × 24h**; the Continued condition is read at **`τ2` = ⟦T0⟧ + 199 × 24h** on `A_H`, with `|A| ≥ 1` retained as a conjunct of Continued (`decisions/0034`). Every boundary test is the half-open UTC-instant form, `watched_at < τ`; `date(watched_at) <= T1` appears nowhere in the implementation.

| Population | Never started | Started and left | Continued | Total |
| :--- | ---: | ---: | ---: | ---: |
| APPLY, position 7 | 32,769 | 19,042 | 144,140 | 195,951 |
| DERIV, position 7 | 9,145 | 16,744 | 121,382 | 147,271 |
| APPLY, position 5 | 33,373 | 19,141 | 144,140 | 196,654 |
| DERIV, position 5 | 9,145 | 16,843 | 121,382 | 147,370 |

**The two published categories are measured over different horizons and must never be described as measured alike**: never-started is a 108-day statement, Continued a 199-day statement (`0034`).

**Abandonment point `p`** is the rank form `|{e ∈ E2 : e ≤ max(A_H)}| / L2`, defined only on Started-and-left; the raw ratio is withdrawn. Range on the table's row set (APPLY, position 5): [0.0385, 1.0000]. The **`p = 1.0` residual** — watched the finale, missed the 90 percent threshold — is 1,246 pairs on APPLY position 5 and 1,230 post-liveness, and is its own named category, not part of 'near-finale'. `p` is null on every row that is not Started-and-left.

---

## 4. Per `W` arm

**Arms: 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days**, fixed by `decisions/0075` and by `task-sheet.md` Step 13 — **the first statement of the grid anywhere, and no longer an instance's choice.** It had previously travelled only as the *index of a reported series*, which is a reading and not a specification; two instances on different grids produce tables that cannot be diffed at all. `H` is held constant at 91 across every arm. **D10 is re-derived at each arm and never frozen** (`decisions/0047`), so the arms do not share a denominator.

### 4.1 Retained pairs per air period after right-censoring

**Censoring is applied to the POSITION-4 output, as the mandated filter order requires** (APPLY 201,900 pairs). `0033`'s 97.6 / 98.0 / 97.5 / 96.0 and 89.7% were computed on the position-3 output and are superseded by `0070` ruling 8.

| `W` | retained (APPLY) | share of position 4 | pre-2020 | 2020–2022 | 2023–2025 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | 197,007 | 97.58% | 97.9% | 97.5% | 96.2% |
| 46 | 197,007 | 97.58% | 97.9% | 97.5% | 96.2% |
| 77 | 197,007 | 97.58% | 97.9% | 97.5% | 96.2% |
| 91 | 197,007 | 97.58% | 97.9% | 97.5% | 96.2% |
| 107 | 196,674 | 97.41% | 97.8% | 97.4% | 95.9% |
| 108 | 196,654 | 97.40% | 97.8% | 97.4% | 95.9% |
| 150 | 195,689 | 96.92% | 97.4% | 96.9% | 94.9% |
| 213 | 193,270 | 95.73% | 97.0% | 96.3% | 89.5% |

**The aggregate hides a cohort-asymmetric loss.** At `W = 108` 97.40% of pairs survive right-censoring, but the 2023–2025 cohort keeps 95.9% against 97.8% pre-2020. At `W = 213` the modern cohort keeps 89.5% — a loss of **10.5%** against 3.0% pre-2020. The loss falls on the uncapped `S1_completion_date` term, so the modern cohort is not merely smaller after censoring but differently selected.

**The `W = 108` row reproduces `0070` ruling 8 exactly** — 97.40% aggregate and 97.8% / 97.4% / 95.9% by period, and 89.5% for 2023–2025 at `W = 213` — measured here independently through the mandated filter order.

**The comparator on the other side of that sentence is also reproduced.** `0033`'s pre-2020 comparator at `W = 213` was **2.7%**, measured on the position-3 output; on the position-4 output the mandated order censors it is **3.0%**. `0070` moved the 10.3% and left the 2.7%, so the sentence briefly carried two orders at once; **`decisions/0073` corrected it, after both Step 8 instances found it independently.** Measured here again through the mandated order, and it agrees.

### 4.2 Liveness exclusions per arm, on APPLY

| `W` | position 5 | excluded | never-started | started-and-left | accounts | DERIV excluded |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | 197,007 | **537** | 485 | 52 | 177 | 52 |
| 46 | 197,007 | **550** | 494 | 56 | 182 | 56 |
| 77 | 197,007 | **633** | 554 | 79 | 197 | 79 |
| 91 | 197,007 | **664** | 575 | 89 | 207 | 89 |
| 107 | 196,674 | **701** | 603 | 98 | 215 | 98 |
| 108 | 196,654 | **703** | 604 | 99 | 216 | 99 |
| 150 | 195,689 | **789** | 664 | 125 | 243 | 125 |
| 213 | 193,270 | **864** | 716 | 148 | 253 | 147 |

`W` and liveness are not independent axes: the rule has no parameter of its own but its exclusion set is a pure function of `W` — 537 at `W = 38` to 864 at `W = 213`, a factor of 1.61. The started-and-left component runs 52 → 148, a factor of 2.85, growing faster than the rule itself.

### 4.3 D3′ — the resumption-rate report, each arm on its own denominator

Of pairs scored **Started and left at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`: the cleared count, its share of all Started-and-left **on the population and at the arm named here**, and the share completing within `[τ2, τ2 + H)`.

**POPULATION: Step 8's RIGHT-CENSORED populations — APPLY, the position-7 output at each arm, each arm on its own denominator** (`decisions/0075`, `0068`). Stated here and in every field of the `.json`, because the gap this closes was a level measured on a different population and carrying no population at the point of use.

| `W` | S&L (APPLY, position 7) | cleared | cleared share | completing in `[τ2, τ2+H)` | share | DERIV cleared share |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | 19,433 | 19,355 | 99.60% | 1,753 | 9.06% | 99.56% |
| 46 | 19,445 | 19,354 | 99.53% | 1,664 | 8.60% | 99.50% |
| 77 | 19,352 | 19,173 | 99.08% | 1,411 | 7.36% | 99.04% |
| 91 | 19,234 | 19,005 | 98.81% | 1,255 | 6.60% | 98.77% |
| 107 | 19,056 | 18,835 | 98.84% | 1,157 | 6.14% | 98.85% |
| 108 | 19,042 | 18,819 | 98.83% | 1,146 | 6.09% | 98.84% |
| 150 | 18,676 | 18,376 | 98.39% | 984 | 5.35% | 98.30% |
| 213 | 18,054 | 17,644 | 97.73% | 816 | 4.62% | 97.57% |

**The cleared-share series is 99.53% at `W = 46` down to 97.73% at `W = 213`, on APPLY** — the series `decisions/0075` fixes, reproduced here independently. **`decisions/0034`'s 95.98% → 91.34% is SUPERSEDED at this point of use**: it was measured on the amendment's **uncensored estimation sample of 128,099** and carried no population where it was used. **The direction and the shrinkage stand; the level does not.**

**Reported and not resolved: the series is not monotone in `W`.** It rises between `W = 91` (98.81%) and `W = 107` (98.84%) before resuming its fall. Both the clearance bound `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` and the Started-and-left denominator move with `W`, and they do not move together — the denominator drops faster than the cleared count between those two arms. Listed open at `decisions/0076` §5; measured here, not resolved.

**Reported alongside, and labelled a COUNT and not a rate: 3,440 Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is **THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, not DERIV (0068; measured at 0034 SS3)**. It is restated, not recomputed on Step 8's population, and it must not be reported against APPLY or DERIV. Exposure-weighted by show recency: a 2016 title offers ten years in which a completion can be observed and a 2025 title about eighteen months, so the count mixes exposure with behaviour. It is a floor because the estimation sample excludes the pairs the Step 5 waterfall drops and is not right-censored (Step 14 item 9). The two figures do not bracket the quantity — both truncate observation and neither is a lower bound on the other.

---

## 5. The other required counts

### 5.1 Both drop counts (Step 1 §3.4) — a COVERAGE COUNT, not an invariant

**The set-membership drop rule is reported, not asserted** (`decisions/0074` ruling 3). Step 8's own bullet already calls it *"an implementation check, not a data check"*, and asserting it would add another passing line to a report where five of eight checks cannot fail on any data.

**Coverage: 6,065,704 in-frame S1/S2 episode records examined across 1,138 shows, 0 dropped.** This is a measured zero, not an empty check.

- **Per show:** 0 dropped episode records and 0 distinct dropped `(season, number)` pairs, on 0 shows. Per-show detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a per-show table, and the aggregate is what belongs here).
- **Per outcome:** 0 pairs had their entire S2 evidence dropped. **Denominator: never-started at position 5 = 33,373** — what entered the liveness filter — with the **post-liveness 32,769 reported alongside** (`0070` ruling 6). The difference between the two is exactly the 604 never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never started.

**The records-examined denominator is published UNRECONCILED** (`decisions/0074` ruling 4): **6,065,704 from this instance against 6,065,610 from the other arm, both reporting 0 drops.** Neither is wrong on its face and nothing downstream depends on it. The decomposition is given so the gap can be localised rather than left as a bare pair of numbers:

- definition used here: episode records (kind == episode) whose show is in the Step 2 frame and whose season is 1 or 2, counted BEFORE the set-membership drop rule and BEFORE D11
- undated (`watched_at` null): **0**
- discarded by D11 (`watched_at ≥ τ_pull`): **167** → 6,065,537 after D11
- exact duplicate `(user, play id)` records: **0**
- records with a non-positive episode `number`: **0**

**None of those axes produces the 94-record gap.** The D11 restriction moves the figure by **167**, not 94; the other three are zero. **Red Team's non-blocking finding that the predicted gap is 167 rather than 94 is consistent with this measurement.** Reported, not reconciled, and routed to Step 14 by `0074`.

### 5.2 D2 — negative lag, split THREE ways

| Population | pairs | first S2 watch before clock start | share | S2-finale binds | S1-completion binds | **both bind** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 5 | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| DERIV, position 5 | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |
| APPLY, position 7 | 195,951 | 49,356 | 25.19% | 44,135 | 5,214 | 7 |
| DERIV, position 7 | 147,271 | 47,453 | 32.22% | 43,207 | 4,239 | 7 |

**A tie is its own category, not a tiebreak** (`0070` ruling 5). Over the whole position-5 APPLY population the binding term is the S2 finale on 87,441 pairs, the S1 completion on 109,045, and **both on 168** — the case a binary split has nowhere to put.

S2-finale-term negative lags are the normal case for anyone who watched a weekly season while it aired and are information about the frame's cadence mix. **S1-term negative lags are the actual test of the first-pass completion choice**, and they are the smaller group.

### 5.3 D4 — S3 without S2 (`0070` ruling 7)

- **APPLY, position 7:** 426 pairs carry the signature — S3-or-later episodes logged and **no S2 episodes at all** — out of 32,769 never-started, 1.300%.
- **DERIV, position 7:** 0 out of 9,145 — zero by construction, since DERIV requires S2 evidence.
- Reported so nothing is hidden: a further 5,004 never-started pairs have S3 evidence **and** some S2 evidence after `τ1`. Those are not the D4 signature and are not counted as it.
- Direction: D4 **inflates** never started. Step 9 bounds it; it is emitted here because Step 8 holds the episode-level evidence and Step 9 does not.

### 5.4 D8 — never-started post-window diagnostic, over `[τ1, τ2)`

| Population | never started | (i) any S2 episode in the horizon | share | (ii) satisfying Continued over the horizon | share |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 7 | 32,769 | 2,733 | 8.34% | 1,820 | 5.55% |
| DERIV, position 7 | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |
| APPLY, position 5 | 33,373 | 2,733 | 8.19% | 1,820 | 5.45% |

Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started boundary** and its size is Step 14's ledger item 10. Direction: **down**.

### 5.5 D9 — split artifacts, both halves

Detection is imperfect and **every count here is a lower bound**. Coverage: 46,428 show IDs carrying a title slug, 747,478 user-show season-coverage rows examined.

**The normalisation key decides the entire number, and both keys are now DEFINED in the spec** (`decisions/0074` ruling 5 adopts strict; `0076` §3 defines both, because "strict" and "loose" had existed only inside one instance's code, which the other is forbidden to read):

| Key | Definition | complementary ID pairs | half (a) | half (b) |
| :--- | :--- | ---: | ---: | ---: |
| **STRICT — ADOPTED** | lowercase, drop every non-alphanumeric character, strip nothing else | **0** | **0** | **0** |
| LOOSE — reported alongside | remove a trailing four-digit year, then strict | 75 | 6 | 27 |
| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary length, then strict | 76 | 6 | — |

- **(a) the fabricated never-started row, on the adopted key:** 0 of 32,769 never-started pairs (APPLY, position 7); 0 of 33,373 on the position-5 table row set.
- **(b) the silently deleted S1-failing counterpart:** 0 of 58,345 pairs that fail the S1 completion rule. **These rows are not in the analysis table and cannot be recovered from it**, so **position 3's drop set is retained as a side output** (`decisions/0075` ruling 2) — without it this half emits zero or fails, **and a zero here reads as a data finding rather than a missing input.**
- **The loose count publishes because it BOUNDS HOW WRONG STRICT COULD BE**, and the error runs **opposite** to D9's own lower-bound caveat. It is not adopted because it strips the year and merges genuinely different shows -- remakes and national versions, not split metadata, which is the artefact D9 exists to count. Measured here: its largest merged clusters are `secondchance` (8 distinct strict keys), `theisland` (7 distinct strict keys), `maigret` (6 distinct strict keys) — remakes and national versions, exactly the failure `0074` names.
- **The third key is reported for the record and is neither ruled key.** It reduces `the-100` to `the`. **This instance used it on its previous run and published 76 complementary pairs against the other arm's 75; `decisions/0076` records that divergence as REPORTED, NOT RECONCILED.** Under the now-defined keys this instance reproduces both ruled figures exactly.
- **Merges, counted with the same query and reported separately:** 20 user-show rows on the strict key (5,551 on the loose key) where one ID carries both seasons and a same-title ID also appears in the sweep. Merges can only add evidence to a pair, never remove it.
- Direction: D9 moves the never-started share **down**, plus an unmeasured denominator loss on half (b).

### 5.6 `pull_date`, fetch dates and discarded records (D11)

- **`pull_date` = `τ_pull` = 2026-08-11T00:00:00Z**, a single global frozen cutoff.
- **Per-user fetch dates:** first page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:08.519916+00:00; last page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:31.236946+00:00. The D11 constraint `pull_date ≤ earliest per-user fetch date` **holds**.
- **Records discarded for `watched_at ≥ τ_pull`:** 1,734 across the whole sweep, of which 167 are in-frame S1/S2 records. A further 379 records carry no `watched_at` at all and cannot be placed on the timeline.
- **Carried as an open question, not resolved:** applying D11 to the S1-completion walk gives 220,103 completers rather than 220,107 — 4 pairs — and moves 0 completion dates. `0068` fixes line 1 at the published 220,107 and lists this as open; this instance measured it and did not apply it.

### 5.7 D12 cadence buckets — all five, each its own line

| Bucket | shows | pairs, position 5 APPLY | pairs, position 7 APPLY | pairs, position 5 DERIV |
| :--- | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | 0 | 0 |
| C1 | 206 | 40,365 | 40,231 | 29,493 |
| C2 | 340 | 58,811 | 58,583 | 44,500 |
| C3 | 167 | 27,573 | 27,306 | 20,783 |
| C4 | 425 | 69,905 | 69,831 | 52,594 |

**Shows within 1 day of a bucket boundary: 7** of 1,138. That count is what says whether the classifier's conventions are load-bearing. **C0 is reported at zero rather than omitted.**

### 5.8 Metadata-disagreement counts

Recomputed from the reported counts rather than read off the frame's stored flags (the two agree: True). **Coverage: 1,138 shows.**

- Shows where `episode_count`, `aired_episodes` and `|E|` disagree: 0 for S1, 0 for S2, 0 for either; pairs on those shows, 0 at position 5 APPLY.
- **Shows where `aired_episodes < |E|` for S2** — the subset where Continued may be unreachable: 0.
- Direction: listed exceeding aired raises `L2`, tightens `ceil(0.90 × L2)`, and pushes pairs that would have been Continued into Started-and-left — it **overstates abandonment**. The same effect on S1 raises `L1` and shrinks the population non-randomly, on shows with messy metadata.

### 5.9 `action` — per-pair counts by type, not a row-level column

`action` is record-level and the row is a pair, so a single value per row would assert one action per pair, which is false (`0070` ruling 4). It is **not an outcome variable**: Step 1 §2.3 ruled check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the logging client.

| | watch | checkin | scrobble | other |
| :--- | ---: | ---: | ---: | ---: |
| S1 records on position-7 APPLY rows | 2,253,911 | 135,295 | 319,554 | 0 |
| S2 records on position-7 APPLY rows | 2,032,204 | 117,560 | 294,457 | 0 |

**Pairs by S2 evidence composition** (position 7, APPLY), which is what Step 13's action arm cuts on: watch-only 130,431, checkin-only 4,557, scrobble-only 12,484, mixed 25,823, no S2 records 22,656. Unknown `action` values encountered: 0.

### 5.10 Discovery channel — two boolean columns

On the table's row set (APPLY, position 5): Channel A 126,269 pairs, Channel B 88,168 pairs, **both 17,783** (accounts: 1,614 / 1,113 / **178 in both**). A single categorical would either drop the overlap or assign it arbitrarily, and Step 11 tests whether discovery method biased the pool (`0070` ruling 3).

**`0070` ruling 3's figure is 324 users in both; this instance measures 178. That is a population difference, not a divergence.** The 324 is on the **Step 3 discovery pool of 5,694 usernames**; 178 is on the **2,549 accounts whose history was actually pulled** before Step 4 stopped at 62.9% of plan. Stated so the two are not read as a disagreement.

---

## 6. The analysis table

`processed/step8/a/analysis_table.csv.gz` — **196,654 rows, 88 columns**, one row per user-show pair, **the POSITION-5 row set on APPLY** (`decisions/0074` ruling 1).

- **`live` and `outcome` are COLUMNS, not filters.** 195,951 rows carry `live = true` and 703 carry `live = false` — the position-6 exclusions are **in the file**, not reconstructed from it. Both readings of "one row per pair" give identical counts, so this is a ruling and not a correction: **a reconstruction that agrees today is still a second definition tomorrow, and the dual diff cannot see it.**
- **147,370 rows carry the DERIV flag**, so both populations are produced by Step 8 and nothing downstream has to rebuild one.
- It carries outcome state, abandonment point, the two discovery-channel booleans, the per-pair action counts and all 60 Step 2 show fields. **It stays in `processed/` and is never published.**

**Side outputs, also in `processed/step8/a/` and also never published:** `position3_dropset.npz` — the rows the S1 completion rule removes, retained because D9 half (b) is measured on them (`decisions/0075` ruling 2); `position5_table.npz`, the per-arm working table; `drops_per_show.csv`; `show_slugs.csv`.

---

## 7. The scope qualifier that travels with this population

Step 8 does not compute Step 9's bound, but it produces the position-6 population the bound is stated on. So, wherever that population is named: **the bound is covering with respect to insertion-dormancy, exhaustively; open only across channel classes (D4, D9).** **D4 and D9 publish alongside and are never folded in** (`0062`).

---

## 8. What this instance had to decide, and what it did not resolve

Listed rather than settled. Each is a place two isolated instances can differ while both following the written spec.

1. **~~The `W` arm grid.~~ CLOSED by `decisions/0075` ruling 3.** The grid is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days, stated in that entry and in `task-sheet.md` Step 13. This instance no longer chooses it. (It is the same grid this instance chose and named on its previous run, so nothing measured moves.)
2. **One table or eight.** The analysis table is built once at `W = 108`; the per-arm requirements are computed as aggregates by re-running positions 5–7 at each arm. The step says "build one row per user-show pair" in the singular and does not say which object is per-arm.
3. **D11 at position 3.** Not applied, per `0068`; the counterfactual is measured and reported in §5.6.
4. **The contamination exclusion is read from Step 5's stored per-pair flags**, and the published Step 5 waterfall is asserted before use rather than re-derived. Step 5 is a closed gate.
5. **`p` on non-Started-and-left rows** is null, not 0 and not omitted. The spec defines `p` only for Started-and-left and does not pin the representation.
6. **"All Step 2 show fields"** is read literally: all 60 non-key columns of `frame.csv`, including derived ones.
7. **Populations for the required counts.** Seven of the required outputs name no population. Each is reported here on a named population, and on more than one where the computation is cheap, rather than one being chosen silently.
8. **D3′'s denominator is the position-7 (post-liveness) Started-and-left set**, which is what reproduces `0075`'s ruled series. The position-5 figures are emitted alongside in the `.json` so the choice is visible and neither reading is hidden.
9. **The set half (b) is measured on.** `0075` retains "position 3's drop set". On this frame position 3 removes **0 rows from the waterfall**, because line 1 is already the S1-completer population; the set the rule *deletes* is the pair universe less the completers, 58,345 pairs. That is what was retained and measured, since a set of size zero would make half (b) unmeasurable rather than zero.

---

## 9. Disagreements between surfaces, reported and not fixed

Reported because the spec asks for them, and not edited: `decisions/` and `task-sheet.md` are not this instance's to amend.

1. **~~`action` as a column~~ — CLOSED.** The previous `-a` run reported three surfaces still requiring a row-level `action` column that `0070` ruling 4 had replaced. All three are now marked: `task-sheet.md` Step 13 (by `0073`), Step 1 §2.3 and §9 (by `0073` and `0076` §4), and the `analytics-engineer` head bullet. **Nothing emitted changed** — per-pair counts by action type, which is what Step 13's arm reads.
2. **~~`decisions/0033`'s pre-2020 comparator at `W = 213`~~ — CLOSED by `0073`.** The comparator is now 3.0%, and this instance measures 3.0% independently through the mandated order.
3. **~~`decisions/0034`'s D3′ cleared-share series~~ — CLOSED by `0075`.** The ruled series is now 99.53% → 97.73% with its population stated; this instance reproduces it — see §4.3.
4. **The 94-record denominator remains OPEN and is published unreconciled** — see §5.1. This instance's decomposition shows the gap is not D11 (which is 167), not undated records, not duplicates and not malformed episode numbers.
5. **D3′ is not monotone in `W`** between the 91 and 107 arms — see §4.3. Measured, not resolved.
6. **`task-sheet.md` Step 8's open D11 question at position 3 is untouched** — applying D11 to the S1 walk gives 220,103 rather than the published 220,107. Measured in §5.6, not applied.

---

*Generated by `src/step8_a_6_emit.py` from the stage outputs in `processed/step8/a/`. Every figure in this file is generated, none is typed by hand.*
