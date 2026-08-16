# Step 8 — filter waterfall and required counts, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** (`decisions/0026`) · **H = 91 days** (D10) · **`τ_pull` = 2026-08-11T00:00:00Z** (D11, `decisions/0011`)

> **THIS IS A GATE DELIVERABLE. IT PROPOSES AND ADOPTS NOTHING.** No approval is recorded here and none is implied. **Zero API calls** — every figure is computed from data already on disk. **Counts and aggregates only**: no username, no user ID and no individual watch history appears in this file or in its `.json`.

> **Every figure below states its population.** There are two and they differ by construction: **APPLY** = Step 5 waterfall line 1 less D10 = **196,654**, which is what position 6 filters; **DERIV** = Step 5 waterfall line 4 less D10 = **147,370**, which requires S2 evidence. Step 8 produces both (`decisions/0070` ruling 1).

> **CLEAN RERUN, ordered by the Human Lead.** This replaces the previous `-a` deliverable in full and is built from the committed state; nothing from the run that was terminated mid-flight is read or relied on. **Everything below is regenerated from one pipeline run** — no figure is typed by hand and none is carried from a previous artifact.

> **The spec this run executes, and what moved since the last one that completed.** **(1)** Every count, every invariant result and every waterfall figure **carries the build it was measured on** (`0079` B6, extending `0078`) — see §0. **(2)** The **position-3 drop set is a DELIVERABLE produced by the pipeline** and is **read back by the stage that computes D9 half (b)** (`0079` B5), so a missing input fails loudly instead of publishing a silent 0. **(3)** The discovery-channel overlap **publishes in all three units, each with its consumer named** (`0079` B7). **(4)** The **four inert filter positions are labelled with the reason** (`0079` §4). **(5)** The column set is the **89 ENUMERATED names** of `0080` §1 **as extended by `0081`** — which **restores `silent_at_tau1`** — **and by `0082`**, which **adds `p_at_bound`**; asserted by set equality, never by count. **(6)** **Every invariant states its population and accounts for every row in it** (`0080` §3). **(7)** **D9 reports four numbers, not three** (`0078` §3). **(8)** **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`0083` §2, restating `0082`), and the `p = 1.0` counts are reported as **totals** — see §3.1. **(9)** The **records-examined denominator is CLOSED** (`0083` §1): all three readings publish, each naming the pipeline that produces it — see §5.1.

> **No figure this instance previously published moves.** What moves is what the figures are *called*: `0083` closed the denominator item this instance had reported as open and restated `p_at_bound`'s definition, and neither ruling changes a measured quantity here.

> Carried forward and unchanged: the table is the position-5 row set with `live` and `outcome` as columns (`0074`/1); D9 uses the defined strict key with the loose count alongside (`0074`/5, `0076`/3); the set-membership rule is a coverage count and not an invariant (`0074`/3); the `W` grid is fixed by `0075`/3; `p` is a CODE CHECK (`0076`/1); and the two DATA CHECKS of `0076`/2 are the only assertions here that can fail on data.

---

## 0. Provenance — what build every figure below was measured on

**A count needs its PROVENANCE, not only its POPULATION** (`decisions/0078` §2, made general by `0079` B6). `0047` fixed *which population produced this figure*; this is that rule one layer down — *which build produced it*. **A count without its provenance can be correct when written and wrong when read**, because the pipeline moved underneath it and nothing in the text says which pipeline it belongs to. **Partial application is worse than none**: two labelled figures imply the other counts and the eight invariants did not need it.

**Build `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`.**

| Field | Value |
| :--- | :--- |
| pipeline | `src/step8_a_run.py, one run, stages 1 -> 6 in order` |
| run date (UTC) | 2026-08-16 |
| git HEAD at launch | `0af0d92`, worktree dirty: True |
| parameters | `W` = 108 d, `H` = 91 d, `τ_pull` = 2026-08-11T00:00:00Z, filter order `decisions/0029`, liveness ALT-BROAD |
| stage files (sha256, 12) | `step8_a_lib.py` 14e28cc5d4fb, `step8_a_1_scan.py` a01904dba997, `step8_a_2_positions.py` 9f08ac985c8c, `step8_a_3_table.py` 840d7e73cb14, `step8_a_4_arms.py` 3d533b88a113, `step8_a_4b_slugs.py` 4495f8069adb, `step8_a_5_diagnostics.py` 8e3c61ba7e15, `step8_a_6_emit.py` ee39aaab9cf8, `step8_a_run.py` 4e6e8a12570a |
| inputs | `processed/step5/full_scan.npz` (size 1050960842 bytes, mtime 1786498855 (not hashed: 1.05 GB)), `calibration.npz` `2016785705db`, `pair_revision5.csv` `cd3085fc1af1`, `step2/frame.csv` `128844b09fc2`, `step4/pull_ledger.jsonl` `2c47f4537ac6` |

**Every figure in this file was measured on that build unless it carries a different one at the point of use.** Two do, and they are marked where they appear: **the 3,440**, which is on Step 5's uncensored estimation sample of 128,099 (`decisions/0034` §3), and the figures **restated** from the position-5 build of 2026-08-13 by `0078` — **58,345 pairs**, **324 of 5,694**, **178 of 2,549** — each of which is **re-measured here on this build and agrees**, which is stated rather than assumed.

---

## 1. The filter order and the waterfall, on both populations

Applied in exactly the order `decisions/0029` fixes. The final row set commutes; the per-filter sample size does not, which is why the order is written down rather than left to each instance.

| # | Filter | APPLY: retained | removed | DERIV: retained | removed | inert? |
| :-- | :--- | ---: | ---: | ---: | ---: | :--- |
| **1** | Step 2 frame | 220,107 | — | 220,107 | — | **INERT BY CONSTRUCTION** — line 1 is already the frame |
| **2** | `L2 = 1` exclusion | 220,107 | 0 | 220,107 | 0 | **INERT BY CONSTRUCTION** — line 1 is already the `L2 > 1` population, and 0 frame shows have `L2 = 1` |
| **3** | S1 completion rule | 220,107 | 0 | 220,107 | 0 | **POSITION INERT, RULE NOT** — line 1 is already the S1-completer population; the rule removes 58,345 pairs upstream of it |
| **4** | contamination exclusion (Step 5) | 201,900 | 18,207 | 152,126 | 67,981 | no — it fires |
| **5** | right-censoring | 196,654 | 5,246 | 147,370 | 4,756 | no — it fires |
| **6** | liveness rule | 195,951 | 703 | 147,271 | 99 | no — it fires |
| **7** | outcome assignment | 195,951 | 0 | 147,271 | 0 | **INERT BY CONSTRUCTION** — it annotates and removes nothing |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**Four positions remove zero BY CONSTRUCTION, and they are labelled rather than left to read as findings** (`decisions/0079` §4). **Keep them: removing a position removes the check that would catch a future upstream change**, and the point of a fixed order is that the waterfall is comparable across runs and across arms. **But an unlabelled always-zero filter reads as evidence THE RULE FOUND NOTHING when it is evidence THE RULE CANNOT FIRE** — the same defect as an unlabelled code check (`0069`).

| Position | Removed | Why it cannot fire |
| :--- | ---: | :--- |
| **1** Step 2 frame | 0 | waterfall line 1 is already the frame (decisions/0068): the base is the S1-completer population ON FRAME SHOWS, so the frame join cannot remove a row that is in the base. |
| **2** L2 = 1 exclusion | 0 | line 1 is already the L2 > 1 S1-completer population (0068) -- and 0 shows in the Step 2 frame have L2 = 1, measured, so the filter has nothing to fire on from either direction. |
| **3** S1 completion rule | 0 | the POSITION is inert for the same reason -- line 1 is already the S1-completer population. THE RULE IS NOT INERT: it removes 58,345 pairs UPSTREAM of line 1, the study's largest single exclusion, which is why its drop set is a Step 8 DELIVERABLE (0079 SS1). A `0` here is evidence the rule cannot fire at this position, never evidence it found nothing. |
| **7** outcome assignment | 0 | it ANNOTATES and removes nothing (decisions/0046); every position-6 row receives exactly one of the three states. |

**Row 3 is the one that matters.** The position is inert; **the rule is the study's largest single exclusion — it removes 58,345 pairs upstream of line 1**, which is why its drop set is a **deliverable** of this run (§6.1) and not a working file.

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

*Build: both columns measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

Both lines remove pairs whose clock start is recent, which on the uncapped `S1_completion_date` term means recent S1 completers — people who found an old show lately, have the whole series available, and are disproportionately likely to roll straight into S2. Removing likely continuers moves the never-started share **up** (Step 1 §6).

---

## 2. Position 6 — the liveness rule, and the population reconciliation

The rule is **ALT-BROAD**, approved unconditionally 2026-08-13 (`decisions/0064`): a pair is **NOT LIVE iff BOTH** (i) the account shows **no insertion instant `> τ1`** — *after* is strict — **AND** (ii) the pair is **NOT Continued**. Evidence is account-wide, runs on record **insertion** time read through the **stored** Step 5 isotonic calibration (never refitted), and is **restricted to records dated before `τ_pull`** (`0070` ruling 2).

| Population | Entering (position 5) | Excluded | never-started | started-and-left | accounts | Retained |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | **703** | 604 | 99 | 216 | 195,951 |
| **DERIV** | 147,370 | **99** | 0 | 99 | 73 | 147,271 |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

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

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**The two published categories are measured over different horizons and must never be described as measured alike**: never-started is a 108-day statement, Continued a 199-day statement (`0034`).

**Abandonment point `p`** is the rank form `|{e ∈ E2 : e ≤ max(A_H)}| / L2`, defined only on Started-and-left; the raw ratio is withdrawn. Range on the table's row set (APPLY, position 5): [0.0385, 1.0000]. The **`p = 1.0` residual** — watched the finale, missed the 90 percent threshold — is 1,246 pairs on APPLY position 5 and 1,230 post-liveness, and is its own named category, not part of 'near-finale'. `p` is null on every row that is not Started-and-left.

### 3.1 `p_at_bound` — WHETHER `p` reached its bound, and the `p = 1.0` totals

**`p_at_bound` marks WHETHER `p` reached its bound, NOT WHY** — Human Lead ruling, 2026-08-16 (`decisions/0083` §2), restating `0082`. **`TRUE` where `p` is at its bound, null where `p` is null.** `0082`'s definition **by two mechanisms** is **superseded**: the two clauses are **coextensive by construction**, so the class it called `FALSE` is **empty** and on the adopted rank form there is only one why. **The column is kept** — Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the spike **labelled**, and **an emptiness asserted in prose and never emitted cannot be checked.**

**The `p = 1.0` counts are TOTALS, not a sum of two classes** (`0083` §2). **1,246 and 1,230 remain true and this instance reproduces them**, but they are **one class counted twice**; reading them as a split is a **withdrawn argument** (`CLAUDE.md`, third blindness class).

| Population | `p = 1.0` rows, TOTAL | `p_at_bound` `TRUE` | `p = 1.0` with `p_at_bound` `FALSE` |
| :--- | ---: | ---: | ---: |
| APPLY, position 5 | 1,246 | 1,246 | 0 |
| APPLY, position 7 | 1,230 | 1,230 | 0 |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**The two clauses are coextensive BY CONSTRUCTION, and it is measured here rather than asserted.** Under the set-membership rule `A_H ⊆ E2`, so `m_H ∈ E2`, and therefore `|{e ∈ E2 : e ≤ m_H}| = L2` **if and only if** `m_H = max(E2) = F2` — which *is* "left at the final episode". **Neither clause can hold without the other.** On APPLY position 5: **1,246** rows satisfy both, **0** satisfy the numerator clause alone, **0** the final-episode clause alone, and **0** neither.

**A SECOND fact, measured and NOT the same argument:** **0 of 1,138 frame shows have any S2 numbering gap**, so `E2 = {1…L2}` everywhere, `F2 = L2`, and the rank form reduces to `m_H / L2`. **That one is DATA and could be false on another frame; the coextensivity above would still hold.** Stated separately so a construction argument is not read as a frame accident.

**Why the column is still worth emitting.** The `FALSE` class is empty because of the rank form and the set-membership rule, **both of which are `W`-invariant**, so it stays empty across Step 13's arms. **A `FALSE` row anywhere means one of the two has broken**, and that is a thing worth catching. `p_at_bound` is `TRUE` exactly on the `p = 1.0` rows, `FALSE` on the rest of Started-and-left, and null elsewhere.

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**The cleared-share series is 99.53% at `W = 46` down to 97.73% at `W = 213`, on APPLY** — the series `decisions/0075` fixes, reproduced here independently. **`decisions/0034`'s 95.98% → 91.34% is SUPERSEDED at this point of use**: it was measured on the amendment's **uncensored estimation sample of 128,099** and carried no population where it was used. **The direction and the shrinkage stand; the level does not.**

**Reported and not resolved: the series is not monotone in `W`.** It rises between `W = 91` (98.81%) and `W = 107` (98.84%) before resuming its fall. Both the clearance bound `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` and the Started-and-left denominator move with `W`, and they do not move together — the denominator drops faster than the cleared count between those two arms. Listed open at `decisions/0076` §5; measured here, not resolved.

**Reported alongside, and labelled a COUNT and not a rate: 3,440 Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is **THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, not DERIV (0068; measured at 0034 SS3)**. It is restated, not recomputed on Step 8's population, and it must not be reported against APPLY or DERIV. Exposure-weighted by show recency: a 2016 title offers ten years in which a completion can be observed and a 2025 title about eighteen months, so the count mixes exposure with behaviour. It is a floor because the estimation sample excludes the pairs the Step 5 waterfall drops and is not right-censored (Step 14 item 9). The two figures do not bracket the quantity — both truncate observation and neither is a lower bound on the other.

*Build: **this figure is NOT on `a/2026-08-16`.** It was measured at `decisions/0034` §3 on the Step 5 revision-6 **uncensored estimation sample of 128,099 pairs**, and it is restated here rather than recomputed. **It must never be reported against APPLY or DERIV.** Saying which build a figure came from is the whole point of the provenance rule, and this is the figure in this deliverable that most needs it.*

---

## 5. The other required counts

**Every count in this section was measured on build `a/2026-08-16`** unless it says otherwise at the point of use (`decisions/0079` B6). The two exceptions are marked where they appear: the **3,440** in §4.3, and the figures `0078` restates from the **position-5 build of 2026-08-13**, which are re-measured here and agree.

### 5.1 Both drop counts (Step 1 §3.4) — a COVERAGE COUNT, not an invariant

**The set-membership drop rule is reported, not asserted** (`decisions/0074` ruling 3). Step 8's own bullet already calls it *"an implementation check, not a data check"*, and asserting it would add another passing line to a report where five of eight checks cannot fail on any data.

**Coverage: 6,065,704 in-frame S1/S2 episode records examined across 1,138 shows, 0 dropped.** This is a measured zero, not an empty check.

- **Per show:** 0 dropped episode records and 0 distinct dropped `(season, number)` pairs, on 0 shows. Per-show detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a per-show table, and the aggregate is what belongs here).
- **Per outcome:** 0 pairs had their entire S2 evidence dropped. **Denominator: never-started at position 5 = 33,373** — what entered the liveness filter — with the **post-liveness 32,769 reported alongside** (`0070` ruling 6). The difference between the two is exactly the 604 never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never started.

**The records-examined denominator — CLOSED, and it publishes as a coverage figure.** Human Lead ruling, 2026-08-16 (`decisions/0083` §1). `0074` ruling 4 published **6,065,704 against 6,065,610, both reporting 0 drops**, reported unreconciled and routed to Step 14; **that routing is withdrawn and the item is closed.** **It was never a divergence**: the readings are **one family indexed by where D11 is applied**, and **`0074`'s "publish both, not one" stands and is strengthened to three, each naming the pipeline that produces it.** This instance produces **6,065,704 — reading A, D11 nowhere.**

| Reading | Where D11 is applied | Pipeline | Records examined | Drops |
| :--- | :--- | :--- | ---: | ---: |
| **A — produced here** | nowhere | `src/step8_a_run.py`, build `a/2026-08-16` | **6,065,704** | 0 |
| B | S2 side only | not this instance's pipeline; recorded at `0083` §1 | 6,065,610 | 0 |
| C | both sides | not this instance's pipeline; measured here as a counterfactual | 6,065,537 | 0 |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**Readings B and C drop 0 because reading A drops 0.** The dropped set measured on the full record set is **empty**, and B and C examine **subsets of it**, so their drop counts are 0 by containment rather than by assumption. **The numerator is 0 three times over, which is why nothing downstream reads the denominator** and why this closes.

**The gap decomposes exactly.** D11 discards **167** in-frame S1/S2 records, of which **94 are S2-side and 73 are S1-side.** So the three readings differ by **where D11 is applied and nowhere else**: 6,065,704 with none, 6,065,610 with D11 on the S2 side, 6,065,537 with D11 on both. **The 94-record difference `0074` reported is exactly the S2-side count.** Every other candidate axis is zero and was measured, not assumed:

- definition used here: episode records (kind == episode) whose show is in the Step 2 frame and whose season is 1 or 2, counted BEFORE the set-membership drop rule and BEFORE D11
- undated (`watched_at` null): **0**
- exact duplicate `(user, play id)` records: **0**
- records with a non-positive episode `number`: **0**

**Why the no-D11 reading.** The figure is the **coverage count of the set-membership drop rule** (`0074` ruling 3), so its denominator is *what that rule examined*. The rule is `number ∈ E`; **it does not read `watched_at` at all**, so every in-frame S1/S2 episode record passes under it whatever its date, and a denominator that pre-filters on a timestamp would report a smaller number than the rule actually looked at — **a check that reports having looked at fewer rows than it looked at**. D11 is a real global cutoff and it is applied everywhere it bears: on `A` and `A_H`, on the action counts, on the liveness evidence, on D9's coverage rows. **It does not bear on this one**, because this one is not a computation on the timeline.

**Why it closes rather than routing to Step 14.** A Step 14 limitation is an uncertainty that **survives into a result**, and this one touches none — the rule it is the denominator of **dropped zero records under every reading**. The three readings are not three measurements of one quantity that disagree; they are **three different quantities, exactly identified**, and the 94/73 split says which is which with nothing left over.

**What stays open is NOT this.** Whether D11 applies to the **S1 completion walk** is `0068`'s own open item: reading C moves waterfall line 1 to **220,103** because **4 pairs stop being completers** and **0 completion dates move** (§5.6). **That question is answered there, not here** — recording it in two places is how a ruling gets made twice and diverges.

### 5.2 D2 — negative lag, split THREE ways

| Population | pairs | first S2 watch before clock start | share | S2-finale binds | S1-completion binds | **both bind** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 5 | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| DERIV, position 5 | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |
| APPLY, position 7 | 195,951 | 49,356 | 25.19% | 44,135 | 5,214 | 7 |
| DERIV, position 7 | 147,271 | 47,453 | 32.22% | 43,207 | 4,239 | 7 |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

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

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started boundary** and its size is Step 14's ledger item 10. Direction: **down**.

### 5.5 D9 — split artifacts, both halves

Detection is imperfect and **every count here is a lower bound**. Coverage: 46,428 show IDs carrying a title slug, 747,478 user-show season-coverage rows examined.

**The normalisation key decides the entire number, and both keys are now DEFINED in the spec** (`decisions/0074` ruling 5 adopts strict; `0076` §3 defines both, because "strict" and "loose" had existed only inside one instance's code, which the other is forbidden to read):

| Key | Definition | complementary ID pairs | half (a) | half (b) |
| :--- | :--- | ---: | ---: | ---: |
| **STRICT — ADOPTED** | lowercase, drop every non-alphanumeric character, strip nothing else | **0** | **0** | **0** |
| LOOSE — reported alongside | remove a trailing four-digit year, then strict | 75 | 6 | 27 |
| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary length, then strict | 76 | 6 | 28 |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

**BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE** (`decisions/0078` §3, closing the one live asymmetry between the arms). **This follows from `0074` ruling 5's own reason rather than from a preference:** the loose count publishes **because it bounds how wrong strict could be**, and **that reason applies to half (b) exactly as it applies to half (a)**. Publishing the bound for one half and withholding it for the other **leaves the reader unable to bound the total**, and the error runs **opposite** to D9's own lower-bound caveat — the direction they were not warned about.

| | strict (adopted) | loose (bound) |
| :--- | ---: | ---: |
| **half (a)** — fabricated never-started row | **0** | 6 |
| **half (b)** — silently deleted S1-failing counterpart | **0** | 27 |

*Build: all four numbers measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

- **(a) the fabricated never-started row, on the adopted key:** 0 of 32,769 never-started pairs (APPLY, position 7); 0 of 33,373 on the position-5 table row set.
- **(b) the silently deleted S1-failing counterpart:** 0 of 58,345 pairs that fail the S1 completion rule. **These rows are not in the analysis table and cannot be recovered from it**, so the set is a **DELIVERABLE of this pipeline run** (`decisions/0079` B5, strengthening `0075` ruling 2) — **and this section READS IT BACK from the file**, so if the stage stopped writing it this figure would **fail loudly rather than publish a 0**, which is the whole point: **a zero here reads as a data finding rather than a missing input.** **`decisions/0077` §2 RESTATES the ruling**, which as written named *"position 3's drop set"* — **an empty set**, because line 1 is already the S1-completer population and position 3 therefore removes 0 rows from the waterfall. The set is **the pair universe less the completers, 58,345 PAIRS**, and it is **not** the set-membership drop rule, which is a different rule, deletes 0 **records**, and would have put the wrong rule in the spec. This instance measured the same set before the restatement and the count is unchanged.
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

### 5.10 Discovery channel — two boolean columns, and the overlap in all three units

A single categorical would either **drop the overlap or assign it arbitrarily**, and the arbitrary assignment would be invisible in the dual diff since both instances would make it the same way only by luck. **Two flags let Step 11 cut on either channel or on the overlap** (`0070` ruling 3).

**PUBLISH THE OVERLAP IN BOTH UNITS, EACH WITH ITS CONSUMER NAMED** (`decisions/0079` B7) — **all three readings publish; picking one leaves another consumer holding a wrong-unit figure.** `0070` ruling 3 gave *"324 users are in both"* and named no population, **the shape that has recurred through this entire chain, inside the ruling written to fix a different unlabelled figure**; `0077` §1 then stated two and `0079` B7 all three. Measured here, each independently:

| Reading | Unit | n | Channel A | Channel B | **in both** | Consumer |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| Step 3 **discovery pool** | usernames | 5,694 | 3,996 | 2,022 | **324** | Step 3's seeding-bias statement; **Step 14 ledger item 1** — the pool's composition |
| **accounts actually pulled** | accounts | 2,549 | 1,614 | 1,113 | **178** | **Step 4 coverage reporting** (the pull stopped at 62.9% of plan) |
| **position-5 population** | accounts | 2,422 | 1,523 | 1,073 | **174** | **Step 11**, which recomputes the headline within each channel and so cuts **the analysis population, not the pool** |
| **position-5 population** | pairs | 196,654 | 126,269 | 88,168 | **17,783** | **Step 11**, same reading in the unit the headline is computed in |

*Build: every figure in this table measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.*

All three reproduce: **324 of 5,694** usernames, **178 of 2,549** accounts pulled, and **174 of 2,422** accounts / **17,783 of 196,654** pairs in the position-5 population. **`0078` restates the first two on the position-5 build of 2026-08-13 and records the third as unpublished; `0079` B7 publishes all three.** The pool figure is not an account figure and neither is a pair figure; **read without its population, any one of them reads as a divergence from the others.**

**One correction to `0079` B7 as dictated, because the mapping is reversed against the files** — and the ruling entry itself records the correction: it assigned **Step 11 to users** and **the pool statistic to accounts**. Step 11 recomputes the headline, which is over **pairs on the position-5 row set**, so it cuts the analysis population; and the pool statistic is the **5,694 usernames**. The substance — both units, consumers named — is executed as ruled.

---

## 6. The analysis table

**The deliverables of this run, all four named** (`task-sheet.md` Step 8 *Deliver*, as amended by `decisions/0079` B5):

| Deliverable | Path | Written by |
| :--- | :--- | :--- |
| analysis table | `processed/step8/a/analysis_table.csv.gz` | stage 3 |
| **position-3 drop set — the 58,345 pairs failing the S1 completion rule** | `processed/step8/a/position3_drop_set.csv.gz` | **stage 2 of the same run** (§6.1) |
| filter waterfall and required counts | `artifacts/step8-waterfall-a.md` / `.json` | stage 6 |
| invariant report | `artifacts/step8-invariants-a.md` / `.json` | stage 6 |

The run record, with per-stage return codes and timings, is `logs/step8_a_run.json`.

`processed/step8/a/analysis_table.csv.gz` — **196,654 rows, 89 columns**, one row per user-show pair, **the POSITION-5 row set on APPLY** (`decisions/0074` ruling 1). Build: every count in this section measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.

- **`live` and `outcome` are COLUMNS, not filters.** 195,951 rows carry `live = true` and 703 carry `live = false` — the position-6 exclusions are **in the file**, not reconstructed from it. Both readings of "one row per pair" give identical counts, so this is a ruling and not a correction: **a reconstruction that agrees today is still a second definition tomorrow, and the dual diff cannot see it.**
- **147,370 rows carry the DERIV flag**, so both populations are produced by Step 8 and nothing downstream has to rebuild one.
- It carries outcome state, abandonment point, the two discovery-channel booleans, the per-pair action counts and all 60 Step 2 show fields. **It stays in `processed/` and is never published.**

**THE COLUMN SET IS ENUMERATED, NOT COUNTED — 89 NAMES, EXACTLY THESE** (`decisions/0080` §1, replacing `0077` §3's count; **extended to 88 by `0081`** and **to 89 by `0082`**). **The arms converged on the 87 names on an earlier run, but converged is not specified**, and Step 8b's schema is built on this vocabulary with Steps 9–13 writing into it **directly, with no conversion layer** (`0066`), so it is fixed **before** the schema exists. **This instance asserts SET EQUALITY against the spec's list, not a count** — a count is arithmetically satisfiable by the wrong columns, which is exactly how an earlier run produced 88 against 87 for the same contents. Column **order** is specified nowhere; this table is in construction order and the sorted list is in the `.json` so an order difference cannot be mistaken for a name difference.

**The count is 89 again after `0082`, but it is a different 89** than `0077`'s: `f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not matching a set**, which is why the assertion here is on the names.

**Two names are in the set that `0080` did not have:**

- **`silent_at_tau1` — RESTORED by `decisions/0081`, and the reason is the one `0080` §2 stated when it dropped the column.** It is **not recoverable from `live` and `outcome` on Continued rows**, because `live` is true for **every** Continued pair regardless of silence — the rule's second conjunct is `NOT Continued`. **Without it the Continued-and-silent count cannot be recomputed from this table.** That count is **652** — the **size of the outcome-conditioning**, the figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation. It is **both a column and an aggregate** here (652 on APPLY position 5, 652 post-liveness, 652 on DERIV position 5), so the figure is readable without opening the table. Build: these three counts measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.
- **`p_at_bound` — added at `decisions/0082`, definition restated by `0083` §2.** It marks **WHETHER `p` reached its bound, not why.** Emitted as a **nullable** boolean: null where `p` is null, because an inapplicable value and a false one must not look alike. **`0082`'s two-mechanism definition is superseded** — the clauses are coextensive by construction and the `FALSE` class is empty — **and the column is kept anyway**, because Step 10 needs the spike labelled and because an emptiness asserted in prose and never emitted cannot be checked. §3.1.

**Two names stay dropped and both are free** (`0080` §2, unchanged by `0081` and `0082`): **`max_episode_in_A`**, read by nothing downstream, and **`f2_in_A_H`**, derivable as `max_episode_in_A_H == s2_F`. **`0083` §3b finished this one**: `0077`'s adopted-name table still listed `f2_in_A_H` beside a bullet dropping it, and the name is now **marked at the point of use rather than deleted**, so `0077`'s spelling ruling — `A_H`, not `AH` — survives without the column.

**The names themselves are `decisions/0077` §3's and were not chosen here.** Renamed from this instance's earlier run: `in_channel_*` → **`discovered_channel_a` / `discovered_channel_b`**; `in_population_APPLY` / `in_population_DERIV` → **`in_apply` / `in_deriv`**; `tau1_utc` / `tau2_utc` → **`tau1` / `tau2`**; `T0_utc_date` → **`t0_date`**; `T0_binding_term` → **`t0_binding_term`**; `s1_completion_date_utc` → **`s1_completion_date`**; `n_A_distinct_s2_before_tau1` → **`n_A`**; `n_AH_distinct_s2_before_tau2` → **`n_A_H`**; `max_episode_in_AH` → **`max_episode_in_A_H`**; `n_rec_s{1,2}_*` → **`action_count_s{1,2}_*`**. **No `_utc` suffix survives**: every instant in this study is UTC by Step 1 §2.4, and suffixing some columns implies the others are not.

**Both instances' extra columns are kept** (`0077` §3, and both are in `0080`'s enumeration): `has_s3_or_later_evidence`, which D4 reads, and **`s1_completion_used_a_post_cutoff_record`**, which the still-open D11-at-position-3 question reads. The second is computed independently here rather than assumed: the first-pass walk runs in ascending canonical-timestamp order, so the completing episode's timestamp is the maximum over the prefix consumed, and the flag is exactly `complete AND comp_ts ≥ τ_pull`. **It is true on 4 pairs of the 220,107** — the same 4 that stop being completers when D11 is applied to the S1 walk, which is the arithmetic the open question turns on. Build: that count measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0.

### 6.1 The position-3 drop set — a DELIVERABLE of this run, not a side file

`processed/step8/a/position3_drop_set.csv.gz` — **58,345 pairs, the pairs that FAIL the S1 completion rule.** **Human Lead ruling, `decisions/0079` B5:** it is **named in the deliverable list**, **written by the same pipeline run that writes the table** (stage 2 of `src/step8_a_run.py`), and carries **each pair's distinct-episode counts and the show's threshold**, which is what D9 half (b) reads.

- **It is read back, not merely written.** The stage that computes half (b) loads this file and asserts it against position 3's recomputed rule (58,345 rows agreeing to the row). **If it were missing, that stage fails loudly instead of publishing 0** — which is the failure `0075` ruling 2 exists to prevent, since **a zero here reads as a data finding rather than a missing input.** A helper script's side file is not a thing the next run is obliged to produce; a stage of this run is.
- **Columns:** `row`, `user_idx`, `show_trakt_id`, `n_distinct_s1_episodes`, `n_distinct_s2_episodes`, `s1_L`, `s1_F`, `s1_completion_threshold_ceil_0_90_L1`, `s2_L`, `reason_short_of_threshold`, `reason_finale_F1_not_watched`.
- **Why the pairs fail:** 57,518 never reached `ceil(0.90 × L1)` distinct S1 episodes; 827 reached the threshold but never watched the S1 finale `F1`.
- **It is the pair universe less the completers — position 3's RULE, not its waterfall line**, which is 0 by construction (`0077` §2). It is **not** the set-membership drop rule, which is a different rule and deletes 0 **records**.
- Build: all four counts in this subsection measured on `a/2026-08-16` — position-5 build of 2026-08-16, instance `a`; see §0. **`0078` restates the 58,345 as *position-3 rule, position-5 build of 2026-08-13*; it is re-measured here on this build and agrees.**

**Other working files, also in `processed/step8/a/` and also never published:** `position5_table.npz`, the per-arm working table; `drops_per_show.csv`; `show_slugs.csv`; the stage `.json` outputs this report is generated from.

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
9. **~~The set half (b) is measured on.~~ CLOSED by `decisions/0077` §2 and made a DELIVERABLE by `0079` B5.** The previous run had to choose an interpretation, because *"position 3's drop set"* named an empty set on this frame. The ruling names it: **the pair universe less the completers, 58,345 pairs** — the set this instance retained and measured before the restatement, so **nothing measured moves**; what changed this run is **who writes it and who reads it** (§6.1). The unit is **pairs**, and it is **not** the set-membership drop rule.
10. **~~Column names, and the 89-versus-`f2_in_A_H` contradiction.~~ CLOSED by `decisions/0080` §1**, which replaces the count with an enumeration and drops `f2_in_A_H` as derivable — **and by `0081` and `0082`, which take the enumeration to 89 names.** **The item this instance reported unreconciled two runs ago is resolved, and in the direction it flagged.** The trade `0080` made — dropping `silent_at_tau1` — was **reversed by `0081` on the ground this instance's own report gave for calling it a real loss**, and the aggregate is kept beside the column anyway.
13. **~~`p_at_bound`'s two classes are not two classes.~~ CLOSED by `decisions/0083` §2**, in the direction this instance reported. The column now marks **whether** `p` reached its bound rather than **why**; the `FALSE` class is empty by construction and the `p = 1.0` counts publish as **totals** — §3.1. **Nothing measured moves**: the encoding this instance emitted under `0082` and the encoding `0083` specifies are the same predicate.
11. **Column ORDER is specified nowhere.** This table is in construction order; the sorted name list is in the `.json`. **If the arms differ here it is an order difference, not a name difference**, and the enumerated set is identical either way.
12. **The `build` label's granularity.** `0079` B6 requires every count to name its build and does not say at what granularity. This instance defines the build once (§0, with stage file hashes and the git HEAD) and cites a **tag** at each figure; the alternative — the full record inline at every figure — carries the same information and reads worse. **A figure measured on a different build says so instead** (the 3,440).

---

## 9. Disagreements between surfaces, reported and not fixed

Reported because the spec asks for them, and not edited: `decisions/` and `task-sheet.md` are not this instance's to amend.

1. **~~`action` as a column~~ — CLOSED.** The previous `-a` run reported three surfaces still requiring a row-level `action` column that `0070` ruling 4 had replaced. All three are now marked: `task-sheet.md` Step 13 (by `0073`), Step 1 §2.3 and §9 (by `0073` and `0076` §4), and the `analytics-engineer` head bullet. **Nothing emitted changed** — per-pair counts by action type, which is what Step 13's arm reads.
2. **~~`decisions/0033`'s pre-2020 comparator at `W = 213`~~ — CLOSED by `0073`.** The comparator is now 3.0%, and this instance measures 3.0% independently through the mandated order.
3. **~~`decisions/0034`'s D3′ cleared-share series~~ — CLOSED by `0075`.** The ruled series is now 99.53% → 97.73% with its population stated; this instance reproduces it — see §4.3.
4. **~~The 94-record denominator is open and published unreconciled.~~ CLOSED by `decisions/0083` §1**, on the arithmetic this instance published last run and on the same arithmetic reproduced here. **It was never a divergence**: the three readings differ only in where D11 is applied, all three drop 0, and the item publishes as a **coverage figure with its pipeline named** rather than as a Step 14 limitation — §5.1.
5. **D3′ is not monotone in `W`** between the 91 and 107 arms — see §4.3. Measured, not resolved.
6. **`task-sheet.md` Step 8's open D11 question at position 3 is untouched** — applying D11 to the S1 walk gives 220,103 rather than the published 220,107. Measured in §5.6, not applied. **The `s1_completion_used_a_post_cutoff_record` column carries the 4 pairs it turns on**, so whoever closes the question does not have to rebuild them.
7. **~~`0077`'s `f2_in_A_H` against its count of 89.~~ CLOSED by `0080` §1**, and the superseded sentence is now struck in `task-sheet.md` and in the `analytics-engineer` file — **the defect this instance reported on the previous run has been fixed on both surfaces.**
8. **~~Two residuals in the column-set bullets, on both surfaces.~~ BOTH FIXED by `decisions/0083` §3**, and both were reported here on the previous run as not this instance's to amend. **(a)** The strike-through note read *"the 88-name ENUMERATION"* for its own replacement while the enumeration above it was 89 names; it now reads 89, with the 88 kept as the intermediate state it was. **(b)** `0077`'s adopted-name table listed `f2_in_A_H` among the adopted names while a bullet in the same section dropped it as derivable; it is now **marked at the point of use rather than deleted**, so `0077`'s **spelling** ruling — which still governs `n_A`, `n_A_H` and `max_episode_in_A_H` — is not lost with the column. **Nothing this instance emits changes**: the enumeration was the operative object in both cases and was followed by set equality against the 89 names.
9. **~~The set-membership records-examined denominator is unruled.~~ CLOSED by `decisions/0083` §1** — see item 4 and §5.1. `0074`'s *"publish both, not one"* is **strengthened to three, each naming its pipeline**, and the Step 14 routing is withdrawn.
10. **NEW, and it is live: `decisions/0083` §2 did not reach SURFACE 7.** `.claude/agent-memory/second-brain/glossary-terms-and-thresholds.md` carries the **denominator** correction of `0083` §1 in its own row, and its **`p_at_bound` bullet is untouched**: it still states `0082`'s **two-mechanism** definition as current, still carries **`0082`'s motive sentence — the one `0083` §2 WITHDREW and registered in `WITHDRAWN_PHRASES`** — as a live claim, and still calls 1,246 and 1,230 **totals the two classes must sum to**, which is the reading `0083` §2 withdrew. **Reported, not edited: `second-brain` writes its own memory and no other agent writes into it.** `0083` §4 records surface 7 as reached, and it was — **for one of the two rulings.**
11. **The phrase control cannot see item 10, and "none" is therefore not a clean result on wrapped prose.** `WITHDRAWN_PHRASES` is matched as a **literal substring** against Markdown that is **hard-wrapped**, so a withdrawn phrase broken across a line break does not match. **Reproduced: normalising whitespace before matching turns up three occurrences the literal matcher misses** — one is item 10; the other two are in the two `analytics-engineer` files, **inside explicit withdrawal notes**, so they are legitimate and would pass either way. **`check_surfaces.py` reports `PHRASE HALF … none` with all three invisible to it.** **Not fixed here**: the control is shared by both arms and by the Human Lead's diff, and changing it mid-gate changes what the diff is taken over. **The one-line change is to match against `re.sub(r"\s+", " ", text)`.**

---

*Generated by `src/step8_a_6_emit.py` from the stage outputs in `processed/step8/a/`. Every figure in this file is generated, none is typed by hand.*
