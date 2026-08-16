# Step 8 — filter waterfall and required counts, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** (`decisions/0026`) · **H = 91 days** (D10) · **`τ_pull` = 2026-08-11T00:00:00Z** (D11, `decisions/0011`)

> **THIS IS A GATE DELIVERABLE. IT PROPOSES AND ADOPTS NOTHING.** No approval is recorded here and none is implied. **Zero API calls** — every figure is computed from data already on disk. **Counts and aggregates only**: no username, no user ID and no individual watch history appears in this file or in its `.json`.

> **Every figure below states its population.** There are two and they differ by construction: **APPLY** = Step 5 waterfall line 1 less D10 = **196,654**, which is what position 6 filters; **DERIV** = Step 5 waterfall line 4 less D10 = **147,370**, which requires S2 evidence. Step 8 produces both (`decisions/0070` ruling 1).

> **RERUN AGAINST `decisions/0088`, ordered by the Human Lead — a rerun, not an amendment.** This replaces the previous `-a` deliverable **in full**; the previous output was **not patched** and nothing in it is read or carried. **Everything below is regenerated from one pipeline run** — no figure is typed by hand. **THREE builds now exist on 2026-08-16** — the one Red Team's third pass reviewed, the `-0085` rerun its fourth pass reviewed, and this one — so they are **tagged apart**, and every figure names which.

> **The spec this run executes, and what moved since the last one that completed.** **(1)** Every count, every invariant result and every waterfall figure **carries the build it was measured on** (`0079` B6, extending `0078`) — see §0. **(2)** The **position-3 drop set is a DELIVERABLE produced by the pipeline** and is **read back by the stage that computes D9 half (b)** (`0079` B5), so a missing input fails loudly instead of publishing a silent 0. **(3)** The discovery-channel overlap **publishes in all three units, each with its consumer named** (`0079` B7). **(4)** The **four inert filter positions are labelled with the reason** (`0079` §4). **(5)** The column set is the **89 ENUMERATED names** of `0080` §1 **as extended by `0081`** — which **restores `silent_at_tau1`** — **and by `0082`**, which **adds `p_at_bound`**; asserted by set equality, never by count. **(6)** **Every invariant states its population and accounts for every row in it** (`0080` §3). **(7)** **D9 reports four numbers, not three** (`0078` §3). **(8)** **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`0083` §2, restating `0082`), and the `p = 1.0` counts are reported as **totals** — see §3.1. **(9)** The **records-examined denominator is CLOSED** (`0083` §1): all three readings publish, each naming the pipeline that produces it — see §5.1.

> **THREE THINGS THIS ARM EMITS DIFFERENTLY FROM ITS LAST RUN, all from `decisions/0088`.** **(B3, §1 — the item that blocked the gate on Red Team's third AND fourth passes.)** The two unasserted mandates are **the half-open UTC-instant form** and **D11-as-global-cutoff** — ***not invariants 7 and 8***, which were already measured, published and labelled DATA CHECK here. **Compliance was never the gap; MEASUREMENT was.** Three things are now emitted: **(a)** the **boundary window** at `τ1` and `τ2` on both populations, with a zero labelled **VACUOUS** rather than passed silently — §5.6a; **(b)** a **per-site D11 table**, **asserted at each of 13 sites** rather than once and about the rest, replacing ***this arm's five sites named in prose with a count at none*** — §5.6b; **(c)** the existing `τ2 ≤ τ_pull` assertion **PROMOTED into the published invariant set** as check 9 — see the invariant report. **(F2, §2.)** The D9 coverage quantities are published **as separate objects with what each counts**, ***this arm's `distinct_show_ids_in_the_sweep` mislabel is corrected*** — it was the D9 coverage pivot, not the sweep — and the overstated coverage sentence in the invariant report is **STRUCK**. **(§3.)** The **D9 clustering universe is ruled to U1**, all slugged sweep show IDs, **ranked by distinct strict keys merged**; ***this arm previously clustered the coverage-pivot subset***, so **the cluster list moves** — §5.5.

> **NO POPULATION, NO RULE AND NO BOUND ENDPOINT MOVES, and every ruled D9 count reproduces** — strict 0, loose 75, third key 76, half (a) 0 and 6, half (b) 0 and 27. **What moves is the D9 CLUSTER LIST**, because the universe it is computed on was ruled and this arm's previous universe was not U1. **`0088` §3 records that D9's SEARCH already ran on the whole sweep in both arms, so the ruling does not widen what D9 finds** — it fixes **which clusters are illustrated**, which is the evidence for the loose key's only warrant.

> Carried forward and unchanged: the table is the position-5 row set with `live` and `outcome` as columns (`0074`/1); D9 uses the defined strict key with the loose count alongside (`0074`/5, `0076`/3); the set-membership rule is a coverage count and not an invariant (`0074`/3); the `W` grid is fixed by `0075`/3; `p` is a CODE CHECK (`0076`/1); and the two DATA CHECKS of `0076`/2 are the only assertions here that can fail on data.

---

## 0. Provenance — what build every figure below was measured on

**A count needs its PROVENANCE, not only its POPULATION** (`decisions/0078` §2, made general by `0079` B6). `0047` fixed *which population produced this figure*; this is that rule one layer down — *which build produced it*. **A count without its provenance can be correct when written and wrong when read**, because the pipeline moved underneath it and nothing in the text says which pipeline it belongs to. **Partial application is worse than none**: two labelled figures imply the other counts and the eight invariants did not need it.

**Build `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart..**

| Field | Value |
| :--- | :--- |
| pipeline | `src/step8_a_run.py, one run, stages 1 -> 6 in order` |
| run date (UTC) | 2026-08-16 |
| git HEAD at launch | `267cfb5`, worktree dirty: True |
| parameters | `W` = 108 d, `H` = 91 d, `τ_pull` = 2026-08-11T00:00:00Z, filter order `decisions/0029`, liveness ALT-BROAD |
| stage files (sha256, 12) | `step8_a_lib.py` 11d33fbf7b89, `step8_a_1_scan.py` baba4ebc7c95, `step8_a_2_positions.py` 9f08ac985c8c, `step8_a_3_table.py` c7ecfd8cf3f2, `step8_a_4_arms.py` 3d533b88a113, `step8_a_4b_slugs.py` 4495f8069adb, `step8_a_5_diagnostics.py` 5864b3dd030b, `step8_a_6_emit.py` 925903d50dee, `step8_a_run.py` 1e858e7bfa89 |
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

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

*Build: both columns measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

Both lines remove pairs whose clock start is recent, which on the uncapped `S1_completion_date` term means recent S1 completers — people who found an old show lately, have the whole series available, and are disproportionately likely to roll straight into S2. Removing likely continuers moves the never-started share **up** (Step 1 §6).

---

## 2. Position 6 — the liveness rule, and the population reconciliation

The rule is **ALT-BROAD**, approved unconditionally 2026-08-13 (`decisions/0064`): a pair is **NOT LIVE iff BOTH** (i) the account shows **no insertion instant `> τ1`** — *after* is strict — **AND** (ii) the pair is **NOT Continued**. Evidence is account-wide, runs on record **insertion** time read through the **stored** Step 5 isotonic calibration (never refitted), and is **restricted to records dated before `τ_pull`** (`0070` ruling 2).

| Population | Entering (position 5) | Excluded | never-started | started-and-left | accounts | Retained |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | **703** | 604 | 99 | 216 | 195,951 |
| **DERIV** | 147,370 | **99** | 0 | 99 | 73 | 147,271 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**This is a POPULATION RECONCILIATION, not an invariant** (`decisions/0068`). Expected 703 on APPLY = 196,654 (604 + 99, 216 accounts) and 99 on DERIV = 147,370 (0 + 99, 73 accounts). **Measured: 703 and 99, with the same splits and the same account counts.** This is the first place Step 7's chain and Step 8's positions 1–5 have been compared: Step 7 built APPLY from the Step 5 pair table rather than through the filters. They agree to the row.

**Neither superseded answer was produced.** 604 is ALT's, 793 is ALT-MATCHED's; either would mean a superseded rule had been implemented.

**How the conjuncts select on APPLY:** conjunct 2 (NOT Continued) narrows 196,654 → 52,514; conjunct 1 (silent at `τ1`) narrows 52,514 → 703. Conjunct 1 does most of the work, which is why the count moves with `W`.

**Evidence scope, measured rather than assumed:** with the `< τ_pull` restriction 703 pairs are excluded; without it 703. The restriction is inert on the exclusion set at this arm, as `0070` recorded, because no insertion instant exceeds the calibration clamp at 2026-08-10T20:48:00Z and D10 already forces `τ1 ≤ τ_pull − 91 d`.

### 2.1 Line 6 read as a marginal cost — both figures, on both populations

**703 is NOT the marginal cost of the silence test** — Red Team third pass, `decisions/0085` §5. **The silence test alone excludes 1,355 on APPLY; the `NOT Continued` conjunct spares 652; `1,355 − 652 = 703`.** ***This instance published 652 and not 1,355 on its previous run.*** **Derivable, so not a defect — but 1,355 is the figure that makes line 6 readable as a marginal cost, and a reader holding only 652 cannot recover it without knowing to add.** **Both, on both populations, with the identity stated:**

| Population entering line 6 | Silence test ALONE excludes | `NOT Continued` SPARES | Line 6 exclusions | Identity |
| :--- | ---: | ---: | ---: | :--- |
| APPLY, position-5 input to line 6 (196,654 rows) | **1,355** | **652** | **703** | 1,355 − 652 = 703 ✓ |
| DERIV, position-5 input to line 6 (147,370 rows) | **751** | **652** | **99** | 751 − 652 = 99 ✓ |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**The spared pairs are the Continued-and-silent ones.** They are what makes line 6 **outcome-conditional**, and they are why `silent_at_tau1` is an emitted column (`0081`): `live` is true for every Continued pair regardless of silence, so the count is not recoverable from `live` and `outcome` alone. **On DERIV the spared count is the same 652**: Continued requires S2 evidence, so every Continued-and-silent pair on APPLY is also a DERIV pair, and the two populations differ in line 6 only through the silence-alone term.

---

## 3. Position 7 — outcome assignment at two instants

`|A| = 0` is read at **`τ1` = ⟦T0⟧ + 108 × 24h**; the Continued condition is read at **`τ2` = ⟦T0⟧ + 199 × 24h** on `A_H`, with `|A| ≥ 1` retained as a conjunct of Continued (`decisions/0034`). Every boundary test is the half-open UTC-instant form, `watched_at < τ`; `date(watched_at) <= T1` appears nowhere in the implementation.

| Population | Never started | Started and left | Continued | Total |
| :--- | ---: | ---: | ---: | ---: |
| APPLY, position 7 | 32,769 | 19,042 | 144,140 | 195,951 |
| DERIV, position 7 | 9,145 | 16,744 | 121,382 | 147,271 |
| APPLY, position 5 | 33,373 | 19,141 | 144,140 | 196,654 |
| DERIV, position 5 | 9,145 | 16,843 | 121,382 | 147,370 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**The two published categories are measured over different horizons and must never be described as measured alike**: never-started is a 108-day statement, Continued a 199-day statement (`0034`).

**Abandonment point `p`** is the rank form `|{e ∈ E2 : e ≤ max(A_H)}| / L2`, defined only on Started-and-left; the raw ratio is withdrawn. Range on the table's row set (APPLY, position 5): [0.0385, 1.0000]. The **`p = 1.0` residual** — watched the finale, missed the 90 percent threshold — is 1,246 pairs on APPLY position 5 and 1,230 post-liveness, and is its own named category, not part of 'near-finale'. `p` is null on every row that is not Started-and-left.

### 3.1 `p_at_bound` — WHETHER `p` reached its bound, and the `p = 1.0` totals

**`p_at_bound` marks WHETHER `p` reached its bound, NOT WHY** — Human Lead ruling, 2026-08-16 (`decisions/0083` §2), restating `0082`. **`TRUE` where `p` is at its bound, null where `p` is null.** `0082`'s definition **by two mechanisms** is **superseded**: the two clauses are **coextensive** — on a chain of three links of which the first two are construction and the third, `max(E2) = F2`, is MEASURED (`0085` §4) — so the class it called `FALSE` is **empty** and on the adopted rank form there is only one why. **The column is kept** — Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the spike **labelled**, and **an emptiness asserted in prose and never emitted cannot be checked.**

**The `p = 1.0` counts are TOTALS, not a sum of two classes** (`0083` §2). **1,246 and 1,230 remain true and this instance reproduces them**, but they are **one class counted twice**; reading them as a split is a **withdrawn argument** (`CLAUDE.md`, third blindness class).

**FOUR CELLS ON FOUR POPULATIONS** — Red Team blocker B2, `decisions/0085` §3. **Total, in-both-classes, saturated-not-final, final-not-saturated and in-neither, on APPLY position 5, APPLY post-liveness, DERIV position 5 and DERIV post-liveness.** This is `CLAUDE.md`'s standing **both populations, always** rule, not a new requirement. ***On this instance's previous run the `p_at_bound_totals_and_coextensivity` block carried `APPLY_position_5` and `APPLY_position_7` and nothing else, so the DERIV post-liveness figure appeared nowhere*** — **on the population where the ground for keeping the column, that an emptiness asserted in prose and never emitted cannot be checked, was therefore unmet.**

| Population | `p = 1.0` TOTAL | in BOTH classes | saturated, not final | final, not saturated | in NEITHER | rows examined (`p` defined) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 5 | **1,246** | 1,246 | 0 | 0 | 0 | 19,141 |
| APPLY, post-liveness | **1,230** | 1,230 | 0 | 0 | 0 | 19,042 |
| DERIV, position 5 | **1,072** | 1,072 | 0 | 0 | 0 | 16,843 |
| DERIV, post-liveness | **1,056** | 1,056 | 0 | 0 | 0 | 16,744 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**The coverage column is not decoration.** Three of the four cells are zero on every row of this table, and **an empty result and a clean result are the same value** — the count of rows the cells were computed over is what says which this is.

**The `p = 1.0` figures are TOTALS, not a sum of two classes**, and the `TRUE` count equals the total on all four populations because the `FALSE` class is empty.

**THE CHAIN HAS THREE LINKS AND ONLY TWO ARE CONSTRUCTION** — Red Team P4, `decisions/0085` §4. ***`0083` §2 named two causes for a future `FALSE` row; there are three.***

1. **`m_H ∈ E2`** — **CONSTRUCTION.** The set-membership drop rule drops any episode whose `number` is not in `E2`, so `A_H ⊆ E2` and its maximum is a member of `E2`.
2. **`|{e ∈ E2 : e ≤ m_H}| = L2 ⟺ m_H = max(E2)`** — **CONSTRUCTION**, given `L2 := |E2|`, which the spec fixes.
3. **`max(E2) = F2`** — **NOT CONSTRUCTION.** It holds only because **the finale is the highest-numbered listed episode**, and **where a season lists an episode numbered above its finale the two separate** — the `s2_aired_lt_listed` case this step is told to count. **MEASURED, NOT ASSUMED: 0 of 1,138 frame shows have `max(E2) ≠ F2`, and 0 shows carry `s2_aired_lt_listed`.** The frame does not move across Step 13's grid, so this is measured once and holds at every arm.

**So the two clauses are coextensive, and the emptiness is measured rather than asserted.** On APPLY position 5: **1,246** rows satisfy both, **0** satisfy the numerator clause alone, **0** the final-episode clause alone, and **0** neither.

**A SECOND fact, measured and NOT the same argument:** **0 of 1,138 frame shows have any S2 numbering gap**, so `E2 = {1…L2}` everywhere, `F2 = L2`, and the rank form reduces to `m_H / L2`. **That one is DATA and could be false on another frame; the coextensivity above would still hold.** Stated separately so a construction argument is not read as a frame accident.

**Why the column is still worth emitting.** The `FALSE` class is empty because of links 1 and 2, **both `W`-invariant**, and link 3, **a frame property that does not move across Step 13's grid** — so it stays empty at every arm. **A `FALSE` row anywhere means one of the THREE has broken**, and that is a thing worth catching. `p_at_bound` is `TRUE` exactly on the `p = 1.0` rows, `FALSE` on the rest of Started-and-left, and null elsewhere.

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**The cleared-share series is 99.53% at `W = 46` down to 97.73% at `W = 213`, on APPLY** — the series `decisions/0075` fixes, reproduced here independently. **`decisions/0034`'s 95.98% → 91.34% is SUPERSEDED at this point of use**: it was measured on the amendment's **uncensored estimation sample of 128,099** and carried no population where it was used. **The direction and the shrinkage stand; the level does not.**

**Reported and not resolved: the series is not monotone in `W`.** It rises between `W = 91` (98.81%) and `W = 107` (98.84%) before resuming its fall. Both the clearance bound `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` and the Started-and-left denominator move with `W`, and they do not move together — the denominator drops faster than the cleared count between those two arms. Listed open at `decisions/0076` §5; measured here, not resolved.

**Reported alongside, and labelled a COUNT and not a rate: 3,440 Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is **THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, not DERIV (0068; measured at 0034 SS3)**. It is restated, not recomputed on Step 8's population, and it must not be reported against APPLY or DERIV. Exposure-weighted by show recency: a 2016 title offers ten years in which a completion can be observed and a 2025 title about eighteen months, so the count mixes exposure with behaviour. It is a floor because the estimation sample excludes the pairs the Step 5 waterfall drops and is not right-censored (Step 14 item 9). The two figures do not bracket the quantity — both truncate observation and neither is a lower bound on the other.

*Build: **this figure is NOT on `a/2026-08-16-0088`.** It was measured at `decisions/0034` §3 on the Step 5 revision-6 **uncensored estimation sample of 128,099 pairs**, and it is restated here rather than recomputed. **It must never be reported against APPLY or DERIV.** Saying which build a figure came from is the whole point of the provenance rule, and this is the figure in this deliverable that most needs it.*

---

## 5. The other required counts

**Every count in this section was measured on build `a/2026-08-16-0088`** unless it says otherwise at the point of use (`decisions/0079` B6). The two exceptions are marked where they appear: the **3,440** in §4.3, and the figures `0078` restates from the **position-5 build of 2026-08-13**, which are re-measured here and agree.

### 5.1 Both drop counts (Step 1 §3.4) — a COVERAGE COUNT, not an invariant

**The set-membership drop rule is reported, not asserted** (`decisions/0074` ruling 3). Step 8's own bullet already calls it *"an implementation check, not a data check"*, and asserting it would add another passing line to a report where SIX OF NINE checks cannot fail on any data.

**Coverage: 6,065,704 in-frame S1/S2 episode records examined across 1,138 shows, 0 dropped.** This is a measured zero, not an empty check.

- **Per show:** 0 dropped episode records and 0 distinct dropped `(season, number)` pairs, on 0 shows. Per-show detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a per-show table, and the aggregate is what belongs here).
- **Per outcome:** 0 pairs had their entire S2 evidence dropped. **Denominator: never-started at position 5 = 33,373** — what entered the liveness filter — with the **post-liveness 32,769 reported alongside** (`0070` ruling 6). The difference between the two is exactly the 604 never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never started.

**The records-examined denominator — CLOSED, and it publishes as a coverage figure.** Human Lead ruling, 2026-08-16 (`decisions/0083` §1). `0074` ruling 4 published **6,065,704 against 6,065,610, both reporting 0 drops**, reported unreconciled and routed to Step 14; **that routing is withdrawn and the item is closed.** **It was never a divergence**: the readings are **one family indexed by where D11 is applied**, and **`0074`'s "publish both, not one" stands and is strengthened to three, each naming the pipeline that produces it.** This instance produces **6,065,704 — reading A, D11 nowhere.**

| Reading | Where D11 is applied | Pipeline | Records examined | Drops |
| :--- | :--- | :--- | ---: | ---: |
| **A — produced here** | nowhere | `src/step8_a_run.py`, build `a/2026-08-16-0088` | **6,065,704** | 0 |
| B | S2 side only | not this instance's pipeline; recorded at `0083` §1 | 6,065,610 | 0 |
| C | both sides | not this instance's pipeline; measured here as a counterfactual | 6,065,537 | 0 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started boundary** and its size is Step 14's ledger item 10. Direction: **down**.

### 5.5 D9 — split artifacts, both halves

Detection is imperfect and **every count here is a lower bound**.

**THE COVERAGE QUANTITIES, EACH NAMED BY WHAT IT COUNTS** — Human Lead ruling, `decisions/0088` §2(b), on Red Team's F2. **`747,478` and `726,103` are different objects and both correct**, and **reconciling them would collapse two real quantities into one**, which the standing rule forbids. **One name over two quantities is the defect.** This arm publishes **all three units** so no reader has to infer which one a bare number is:

| | Unit | Count |
| :--- | :--- | ---: |
| **A** | undeduplicated user-show **SEASON-COVERAGE ROWS** — distinct `(user, show, season-class)` triples, season-class in {S1, S2, S3+} | 1,217,122 |
| **B** | distinct user-show **PAIRS** in the coverage pivot — any dated pre-`τ_pull` episode record in season ≥ 1, **including pairs whose only evidence is S3 or later** | **747,478** |
| **C** | **D9 CANDIDATE** user-show pairs — B less the S3-or-later-only pairs; the pairs the complementary-coverage search can match on | 726,102 |
| | *bridge: B − C, pairs with only S3-or-later evidence* | *21,376* |
| | show IDs carrying a title slug, in the map | 46,428 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**THE FIGURE THIS ARM PUBLISHES AS `747,478` IS B — distinct `(user, show)` PAIRS, not season-coverage rows.** ***Reported, not reconciled: `decisions/0088` §2's table characterises this arm's 747,478 as "undeduplicated user-show SEASON-COVERAGE ROWS". Measured on this build it is not — the season-coverage row count is 1,217,122, and 747,478 is the deduplicated pair count.*** The ruling's **conclusion** — two objects, both correct, do not reconcile — **holds and is applied here**; what it named as the distinguishing axis is not the axis on this arm's figures.

**And the axis that does separate them is C: 435,642 + 8,834 + 281,626 = 726,102.** **`decisions/0087` §2 and `0088` §2 record the other arm's quantity as `435,643 + 8,834 + 281,626 = 726,103`, in the same three classes.** **Two of the three classes agree exactly; the S1-evidence-and-no-S2 class differs by ONE pair**, so the two totals stand **1 apart**, not 0. ***REPORTED, NOT RECONCILED*** — and it is **not** the 21,376 S3-only pairs, which are the whole of the B-against-C gap and are accounted for above. **No entry has recorded a one-pair difference in this class**; it is stated here so the diff has it.

**The normalisation key decides the entire number, and both keys are now DEFINED in the spec** (`decisions/0074` ruling 5 adopts strict; `0076` §3 defines both, because "strict" and "loose" had existed only inside one instance's code, which the other is forbidden to read):

| Key | Definition | complementary ID pairs | half (a) | half (b) |
| :--- | :--- | ---: | ---: | ---: |
| **STRICT — ADOPTED** | lowercase, drop every non-alphanumeric character, strip nothing else | **0** | **0** | **0** |
| LOOSE — reported alongside | remove a trailing four-digit year, then strict | 75 | 6 | 27 |
| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary length, then strict | 76 | 6 | 28 |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE** (`decisions/0078` §3, closing the one live asymmetry between the arms). **This follows from `0074` ruling 5's own reason rather than from a preference:** the loose count publishes **because it bounds how wrong strict could be**, and **that reason applies to half (b) exactly as it applies to half (a)**. Publishing the bound for one half and withholding it for the other **leaves the reader unable to bound the total**, and the error runs **opposite** to D9's own lower-bound caveat — the direction they were not warned about.

| | strict (adopted) | loose (bound) |
| :--- | ---: | ---: |
| **half (a)** — fabricated never-started row | **0** | 6 |
| **half (b)** — silently deleted S1-failing counterpart | **0** | 27 |

*Build: all four numbers measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

- **(a) the fabricated never-started row, on the adopted key:** 0 of 32,769 never-started pairs (APPLY, position 7); 0 of 33,373 on the position-5 table row set.
- **(b) the silently deleted S1-failing counterpart:** 0 of 58,345 pairs that fail the S1 completion rule. **These rows are not in the analysis table and cannot be recovered from it**, so the set is a **DELIVERABLE of this pipeline run** (`decisions/0079` B5, strengthening `0075` ruling 2) — **and this section READS IT BACK from the file**, so if the stage stopped writing it this figure would **fail loudly rather than publish a 0**, which is the whole point: **a zero here reads as a data finding rather than a missing input.** **`decisions/0077` §2 RESTATES the ruling**, which as written named *"position 3's drop set"* — **an empty set**, because line 1 is already the S1-completer population and position 3 therefore removes 0 rows from the waterfall. The set is **the pair universe less the completers, 58,345 PAIRS**, and it is **not** the set-membership drop rule, which is a different rule, deletes 0 **records**, and would have put the wrong rule in the spec. This instance measured the same set before the restatement and the count is unchanged.
- **The loose count publishes because it BOUNDS HOW WRONG STRICT COULD BE**, and the error runs **opposite** to D9's own lower-bound caveat. It is not adopted because it strips the year and merges genuinely different shows -- remakes and national versions, not split metadata, which is the artefact D9 exists to count.

**THE CLUSTERING UNIVERSE IS U1, RANKED BY DISTINCT STRICT KEYS MERGED** — Human Lead ruling, `decisions/0088` §3, closing the gap Red Team's B1 opened (`0085` §2, where **the two arms published DISJOINT cluster lists on IDENTICAL counts**) and `0087` §2 located (**the two arms' "U1" were two sets 62 apart under one label**). **BOTH ARMS NOW CLUSTER THE SAME OBJECT.**

**The ground, as ruled:** the artifact D9 hunts is **a viewer's history splitting across two metadata entries for one show**, and **that split can occur anywhere in a history, not only among shows that survived the frame filters.** A frame-restricted universe finds only splits where **both sides made the cut** — the narrowest case — and **a bound computed on a narrow slice bounds very little.**

**This arm clusters U1 -- every distinct show ID appearing anywhere in the pulled sweep that carries a slug, deduplicated to ONE ROW PER SHOW ID** — **U1 = 46,428 show IDs**, read from the slug map collected over all 2,549 parsed history files, which is what *"anywhere in the pulled sweep"* means. **It is NOT U2 (the 1,138 frame shows) and NOT U3 (the 75 D9 candidate pairs).** 1,829 loose keys merge more than one strict key.

***THIS IS A CHANGE OF OBJECT FOR THIS ARM, and the corrected label is the point.*** On build `a/2026-08-16-0085` this arm clustered **the distinct show IDs appearing in a D9 COVERAGE ROW -- i.e. reaching the pivot through a dated, pre-tau_pull, season >= 1 episode record** — **46,366 show IDs** — and published that count under the label **`distinct_show_ids_in_the_sweep`**, ***which is not what it counts***. `decisions/0087` §2 caught it; `0088` §2(a) requires the label corrected to what it counts, **and its "0 carry no slug" clause was therefore computed against the wrong base**. **Both counts are real objects and both are published**: U1 is 46,428, the coverage-pivot subset is 46,366, and **U1 − pivot = 62** — shows reaching the sweep only through a record D11 discards, an undated record, a specials-only record or a non-episode record. **The subset relation is asserted in the pipeline, not assumed.**

***And the 62 is the same 62 `decisions/0087` §2 measured as the gap between the two arms' "U1"s.*** That entry recorded the arms' slugged-ID sets as **62 apart under one label**; **this arm's U1 is now the larger of the two**, and the 62 is **not an arm difference at all — it is the difference between the sweep and the coverage pivot, and both numbers were always recoverable from this arm alone**, which `0087` §2 says in its own last paragraph. **On this build the two arms should name one object; if they still differ, one has a bug and that is the finding.**

**And "largest" ranks by DISTINCT STRICT KEYS MERGED into one loose key -- how many separate metadata entries the loose key collapsed. Ruled by decisions/0088 ruling 3 because it was unstated and REORDERS THE LIST ON ITS OWN: ranked by distinct SHOW IDs instead, `blackout` displaces `maigret`. Both orders are emitted.**

| Ranked by distinct STRICT keys merged | | Ranked by distinct SHOW IDs merged | |
| :--- | ---: | :--- | ---: |
| `secondchance` | 8 | `secondchance` | 8 |
| `theisland` | 7 | `theisland` | 7 |
| `yourhonor` | 6 | `blackout` | 7 |

*Build: both cluster lists and the universe counts measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**THE RULED BASIS TIES AT RANK 3, so a bare "third-largest cluster" is not reproducible from the basis alone.** The head-of-list above is a `head(3)` whose order at rank 3 is decided by the sort's stability rather than by the ruling. **Every key at every published rank, both bases:**

| Rank value | Ranked by distinct STRICT keys merged | Ranked by distinct SHOW IDs merged |
| ---: | :--- | :--- |
| 8 | `secondchance` | `secondchance` |
| 7 | `theisland` | `blackout`, `theisland` |
| 6 | `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` | `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` |

**The basis reorders the list on its own, exactly as `0088` §3 says:** `blackout` carries **6 strict keys but 7 show IDs**, so it sits at rank 3 on one basis and rank 2 on the other, and ranking by show IDs displaces `maigret`. **`task-sheet.md`'s former illustration — The Twilight Zone, The Traitors, Manhunt — was U3 and is SUPERSEDED as the example; those three names are not wrong, they are another universe's answer.**

**One row per show ID needs a tie-break and this arm states its own:** lexicographically first slug per show ID. Stated rather than implicit; the sensitivity is measured, not assumed. **2 show IDs carry more than one slug.** Under the last slug instead the cluster count is 1,829 against 1,829 — **measured, not assumed away.**

**If the other arm names the same universe and still differs, one of us has a bug and that is the finding.** These are remakes and national versions, exactly the failure `0074` names.
- **The third key is reported for the record and is neither ruled key.** It reduces `the-100` to `the`. **This instance used it on its previous run and published 76 complementary pairs against the other arm's 75; `decisions/0076` records that divergence as REPORTED, NOT RECONCILED.** Under the now-defined keys this instance reproduces both ruled figures exactly.
- **Merges, counted with the same query and reported separately:** 20 user-show rows on the strict key (5,551 on the loose key) where one ID carries both seasons and a same-title ID also appears in the sweep. Merges can only add evidence to a pair, never remove it.
- Direction: D9 moves the never-started share **down**, plus an unmeasured denominator loss on half (b).

### 5.6 `pull_date`, fetch dates and discarded records (D11)

- **`pull_date` = `τ_pull` = 2026-08-11T00:00:00Z**, a single global frozen cutoff.
- **Per-user fetch dates:** first page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:08.519916+00:00; last page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:31.236946+00:00. The D11 constraint `pull_date ≤ earliest per-user fetch date` **holds**.
- **Records discarded for `watched_at ≥ τ_pull`:** 1,734 across the whole sweep, of which 167 are in-frame S1/S2 records. A further 379 records carry no `watched_at` at all and cannot be placed on the timeline.
- **Carried as an open question, not resolved:** applying D11 to the S1-completion walk gives 220,103 completers rather than 220,107 — 4 pairs — and moves 0 completion dates. `0068` fixes line 1 at the published 220,107 and lists this as open; this instance measured it and did not apply it.

### 5.6a The half-open form — MEASURED, not self-reported (B3(a))

**Human Lead ruling, `decisions/0088` §1, on Red Team's B3/F1, which blocked the gate on the third and fourth passes.** The two unasserted mandates are **the half-open UTC-instant form** and **D11-as-global-cutoff** — *not* invariants 7 and 8, which were already measured, published and labelled DATA CHECK. **This arm's compliance is TRUE and was independently confirmed** — no `.date()`, `dt.date`, `normalize()` or day-flooring anywhere in `step8_a_*.py`, instants int64 seconds throughout. ***That is not what was missing: nothing measured whether either mandate is LOAD-BEARING on this data, and an unmeasured pass is indistinguishable from a check that looked nowhere.***

**One thing the ruling does not say, and it decides the answer.** `T0` is day-floored and `W` and `H` are whole days, so **`τ1` and `τ2` land exactly on midnight UTC** — asserted in the pipeline, not assumed. The date-level form `date(ts) < date(τ1)` is therefore **identical** to the half-open `ts < τ1` and can never differ. **The form that CAN differ is `date(ts) ≤ date(τ1)`, which admits the whole of `[τ1, τ1 + 24h)`.** So the window the ruling names — `[τ1 − 24h, τ1)` — is the window on which the two forms **agree by construction**, and the interval on the **other** side is where the mandate is load-bearing. **Both are emitted; reporting only the named one would answer the question with the interval that cannot separate them.**

| Population | Bound | in `[τ − 24h, τ)` *(ruling's window)* | **exactly at `τ`** | **where the two forms ACTUALLY differ** | rows affected | vacuous? |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | `τ1` | 749 | **1** | **703** | 311 | no — load-bearing |
| APPLY, position 5 | `τ2` | 291 | **0** | **303** | 136 | no — load-bearing |
| DERIV, position 5 | `τ1` | 676 | **1** | **595** | 275 | no — load-bearing |
| DERIV, position 5 | `τ2` | 254 | **0** | **261** | 117 | no — load-bearing |

**Coverage:** 196,654 rows and 2,135,938 distinct S2 episodes on APPLY; 147,370 rows and 1,766,159 episodes on DERIV. **Unit: distinct S2 episodes by canonical timestamp** — the objects the bound is actually tested against, since `A` and `A_H` are sets of distinct episodes. *Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**RESULT: THE MANDATE IS LOAD-BEARING, NOT VACUOUS.** On APPLY a `date(ts) ≤ date(τ1)` form would admit **703 episodes on 311 rows** into `A`. **No cell is 0, so no invariant here is labelled vacuous** — and where a cell had been 0 it would have been **stated as a zero, not passed silently**.

> ***A COINCIDENCE, FLAGGED SO IT IS NOT MISREAD.*** The APPLY `τ1` differing-episode count is **703**, **the same integer as the 703 liveness exclusions.** **They are unrelated objects** — one counts distinct S2 episodes in a 24-hour interval, the other counts pairs removed at position 6 — **and no arithmetic connects them.** This report states it because a repeated integer in a document this size gets read as a shared quantity.

**And the ruling's own second quantity is NOT zero:** exactly **1 episode falls exactly AT `τ1`** on APPLY (and 1 on DERIV), so **`0068`'s strictness ruling — an instant *at* the bound is not *after* it — changes the answer for a real row rather than for none.**

### 5.6b D11 applied per site, asserted at each (B3(b))

**`decisions/0088` §1(b).** D11 is specified to apply *"to EVERY computation"*, and ***this arm's previous deliverable named five sites in prose with a count at none.*** **Every site now carries its own unit, its own count and its own assertion — not one assertion about the rest.** **Ground, as ruled: the unstated version of exactly this scope produced Step 7's 792-against-791.**

| Site | Unit | examined | **excluded by D11** | D11 applied? | assertion |
| :--- | :--- | ---: | ---: | :--- | :--- |
| `action_count_s1_watch` | in-frame in-E S1/S2 episode records | 2,717,040 | **49** | yes | **PASS** |
| `action_count_s1_checkin` | in-frame in-E S1/S2 episode records | 153,246 | **1** | yes | **PASS** |
| `action_count_s1_scrobble` | in-frame in-E S1/S2 episode records | 383,834 | **23** | yes | **PASS** |
| `action_count_s1_other` | in-frame in-E S1/S2 episode records | 0 | **0** | yes | **PASS** *(looked at ZERO units — holds trivially)* |
| `action_count_s2_watch` | in-frame in-E S1/S2 episode records | 2,364,954 | **52** | yes | **PASS** |
| `action_count_s2_checkin` | in-frame in-E S1/S2 episode records | 120,993 | **4** | yes | **PASS** |
| `action_count_s2_scrobble` | in-frame in-E S1/S2 episode records | 325,637 | **38** | yes | **PASS** |
| `action_count_s2_other` | in-frame in-E S1/S2 episode records | 0 | **0** | yes | **PASS** *(looked at ZERO units — holds trivially)* |
| `A_the_set_tested_at_tau1` | distinct S2 episodes on position-5 rows | 2,135,938 | **0** | yes | **PASS** |
| `A_H_the_set_tested_at_tau2` | distinct S2 episodes on position-5 rows | 2,135,938 | **0** | yes | **PASS** |
| `liveness_evidence` | records, ALL kinds and ALL shows -- the insertion clock is account-wide | 27,656,813 | **1,734** | yes | **PASS** |
| `D9_coverage_rows` | dated season >= 1 episode records feeding the D9 coverage pivot | 24,645,658 | **1,543** | yes | **PASS** |
| `S1_completion_walk` | in-frame S1 episode records | 73 | **0** | **NO — declared** | **PASS** |

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

**13 sites; D11 is applied at 12 and NOT applied at 1, which says so rather than being omitted. All 13 site assertions hold: True.** **11 of them were asserted on a NON-EMPTY unit set**; the rest are listed as having looked at zero units, because **a check that finds nothing because it looked nowhere must not read as a pass** (`CLAUDE.md`).

**Two things this measurement establishes that the prose could not.** First, **the eight `action_count_*` sites' D11 exclusions sum to exactly the 167 in-frame S1/S2 records at or after `τ_pull`** — the same 167 that indexes the closed records-examined family (`0083` §1, 94 S2-side + 73 S1-side) — **so the action counts and that denominator are the same discard, seen at two sites.** Second, **the liveness-evidence site is the only one where D11 moves an input**: **469 accounts' maximum play `id` moves under D11 and 299 accounts' last insertion instant moves with it.** **That is `0070` ruling 2's site, and it is load-bearing on this data even though the exclusion count it produces is 703 either way** — the ruling's own measured claim, now measured at the site rather than at the outcome.

**`A` and `A_H` are INERT BY CONSTRUCTION and the count is stated rather than the construction being asserted about:** 17 distinct S2 episodes on position-5 rows sit at or after `τ_pull`, and **0 of them can enter `A` or `A_H`** — because D10 forces `τ1 ≤ τ2 ≤ τ_pull` on every retained pair. **That is the invariant promoted into the published set as check 9** (`0088` §1(c)); see the invariant report.

**The S1 completion walk is the one site where D11 is NOT applied, and it says so.** 73 in-frame S1 records sit at or after `τ_pull`; applying D11 there would stop 4 pairs being completers and move 0 completion dates. **`decisions/0068` fixes waterfall line 1 at the published 220,107 and lists whether D11 moves it as an OPEN question**, so the counterfactual is measured and published rather than the site being left out of the table.

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

*Build: every figure in this table measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.*

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

`processed/step8/a/analysis_table.csv.gz` — **196,654 rows, 89 columns**, one row per user-show pair, **the POSITION-5 row set on APPLY** (`decisions/0074` ruling 1). Build: every count in this section measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.

- **`live` and `outcome` are COLUMNS, not filters.** 195,951 rows carry `live = true` and 703 carry `live = false` — the position-6 exclusions are **in the file**, not reconstructed from it. Both readings of "one row per pair" give identical counts, so this is a ruling and not a correction: **a reconstruction that agrees today is still a second definition tomorrow, and the dual diff cannot see it.**
- **147,370 rows carry the DERIV flag**, so both populations are produced by Step 8 and nothing downstream has to rebuild one.
- It carries outcome state, abandonment point, the two discovery-channel booleans, the per-pair action counts and all 60 Step 2 show fields. **It stays in `processed/` and is never published.**

**THE COLUMN SET IS ENUMERATED, NOT COUNTED — 89 NAMES, EXACTLY THESE** (`decisions/0080` §1, replacing `0077` §3's count; **extended to 88 by `0081`** and **to 89 by `0082`**). **The arms converged on the 87 names on an earlier run, but converged is not specified**, and Step 8b's schema is built on this vocabulary with Steps 9–13 writing into it **directly, with no conversion layer** (`0066`), so it is fixed **before** the schema exists. **This instance asserts SET EQUALITY against the spec's list, not a count** — a count is arithmetically satisfiable by the wrong columns, which is exactly how an earlier run produced 88 against 87 for the same contents. Column **order** is specified nowhere; this table is in construction order and the sorted list is in the `.json` so an order difference cannot be mistaken for a name difference.

**The count is 89 again after `0082`, but it is a different 89** than `0077`'s: `f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not matching a set**, which is why the assertion here is on the names.

**AND THE LIST ASSERTED AGAINST IS NOW READ OFF `task-sheet.md` AT RUN TIME** — 89 distinct names parsed from the enumeration block, matching this arm's transcription: **True**. ***This closes Red Team's fourth-pass F6*** (`decisions/0087` §5), which found this arm's report claiming set equality *"against the spec's list"* while the code asserted against **a hand transcription that never opened `task-sheet.md`**. **A transcription is a second copy of the enumeration, and a propagation change to the spec would not reach it** — and **the dual diff cannot catch a propagation failure**, so only this check can. **F6 was carried as a limitation rather than ruled; it is closed here rather than restated.** **A parse that found nothing would FAIL rather than pass**, and the parsed count is published above.

**Two names are in the set that `0080` did not have:**

- **`silent_at_tau1` — RESTORED by `decisions/0081`, and the reason is the one `0080` §2 stated when it dropped the column.** It is **not recoverable from `live` and `outcome` on Continued rows**, because `live` is true for **every** Continued pair regardless of silence — the rule's second conjunct is `NOT Continued`. **Without it the Continued-and-silent count cannot be recomputed from this table.** That count is **652** — the **size of the outcome-conditioning**, the figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation. It is **both a column and an aggregate** here (652 on APPLY position 5, 652 post-liveness, 652 on DERIV position 5), so the figure is readable without opening the table. Build: these three counts measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.
- **`p_at_bound` — added at `decisions/0082`, definition restated by `0083` §2.** It marks **WHETHER `p` reached its bound, not why.** Emitted as a **nullable** boolean: null where `p` is null, because an inapplicable value and a false one must not look alike. **`0082`'s two-mechanism definition is superseded** — the clauses are coextensive, on a three-link chain whose third link is measured and not construction (`0085` §4), and the `FALSE` class is empty — **and the column is kept anyway**, because Step 10 needs the spike labelled and because an emptiness asserted in prose and never emitted cannot be checked. §3.1.

**Two names stay dropped and both are free** (`0080` §2, unchanged by `0081` and `0082`): **`max_episode_in_A`**, read by nothing downstream, and **`f2_in_A_H`**, derivable as `max_episode_in_A_H == s2_F`. **`0083` §3b finished this one**: `0077`'s adopted-name table still listed `f2_in_A_H` beside a bullet dropping it, and the name is now **marked at the point of use rather than deleted**, so `0077`'s spelling ruling — `A_H`, not `AH` — survives without the column.

**The names themselves are `decisions/0077` §3's and were not chosen here.** Renamed from this instance's earlier run: `in_channel_*` → **`discovered_channel_a` / `discovered_channel_b`**; `in_population_APPLY` / `in_population_DERIV` → **`in_apply` / `in_deriv`**; `tau1_utc` / `tau2_utc` → **`tau1` / `tau2`**; `T0_utc_date` → **`t0_date`**; `T0_binding_term` → **`t0_binding_term`**; `s1_completion_date_utc` → **`s1_completion_date`**; `n_A_distinct_s2_before_tau1` → **`n_A`**; `n_AH_distinct_s2_before_tau2` → **`n_A_H`**; `max_episode_in_AH` → **`max_episode_in_A_H`**; `n_rec_s{1,2}_*` → **`action_count_s{1,2}_*`**. **No `_utc` suffix survives**: every instant in this study is UTC by Step 1 §2.4, and suffixing some columns implies the others are not.

**Both instances' extra columns are kept** (`0077` §3, and both are in `0080`'s enumeration): `has_s3_or_later_evidence`, which D4 reads, and **`s1_completion_used_a_post_cutoff_record`**, which the still-open D11-at-position-3 question reads. The second is computed independently here rather than assumed: the first-pass walk runs in ascending canonical-timestamp order, so the completing episode's timestamp is the maximum over the prefix consumed, and the flag is exactly `complete AND comp_ts ≥ τ_pull`. **It is true on 4 pairs of the 220,107** — the same 4 that stop being completers when D11 is applied to the S1 walk, which is the arithmetic the open question turns on. Build: that count measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0.

### 6.1 The position-3 drop set — a DELIVERABLE of this run, not a side file

`processed/step8/a/position3_drop_set.csv.gz` — **58,345 pairs, the pairs that FAIL the S1 completion rule.** **Human Lead ruling, `decisions/0079` B5:** it is **named in the deliverable list**, **written by the same pipeline run that writes the table** (stage 2 of `src/step8_a_run.py`), and carries **each pair's distinct-episode counts and the show's threshold**, which is what D9 half (b) reads.

- **It is read back, not merely written.** The stage that computes half (b) loads this file and asserts it against position 3's recomputed rule (58,345 rows agreeing to the row). **If it were missing, that stage fails loudly instead of publishing 0** — which is the failure `0075` ruling 2 exists to prevent, since **a zero here reads as a data finding rather than a missing input.** A helper script's side file is not a thing the next run is obliged to produce; a stage of this run is.
- **Columns:** `row`, `user_idx`, `show_trakt_id`, `n_distinct_s1_episodes`, `n_distinct_s2_episodes`, `s1_L`, `s1_F`, `s1_completion_threshold_ceil_0_90_L1`, `s2_L`, `reason_short_of_threshold`, `reason_finale_F1_not_watched`.
- **Why the pairs fail:** 57,518 never reached `ceil(0.90 × L1)` distinct S1 episodes; 827 reached the threshold but never watched the S1 finale `F1`.
- **It is the pair universe less the completers — position 3's RULE, not its waterfall line**, which is 0 by construction (`0077` §2). It is **not** the set-membership drop rule, which is a different rule and deletes 0 **records**.
- Build: all four counts in this subsection measured on `a/2026-08-16-0088` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0088 (B3 measured: the boundary window and the per-site D11 table; F2: the D9 coverage quantities named as separate objects and the mislabel corrected; the D9 clustering universe ruled to U1, ranked by distinct strict keys merged). The earlier 2026-08-16 builds of this instance -- `a/2026-08-16-0085` and the pre-0085 run -- are what Red Team's third and fourth passes reviewed. NO POPULATION AND NO RULE MOVES between them; what moves is the D9 CLUSTER LIST, because the universe it is computed on was ruled and this instance's previous universe was the D9 coverage pivot rather than the sweep. They are different builds and are tagged apart.; see §0. **`0078` restates the 58,345 as *position-3 rule, position-5 build of 2026-08-13*; it is re-measured here on this build and agrees.**

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
12. **NEW, and it is `decisions/0088`'s own propagation gap: `0088` §1(c) takes the assertion set from EIGHT to NINE, and no surface says nine.** **Surfaces 4 and 5** — `.claude/agents/analytics-engineer.md` and `-b.md`, both edited by `0088` — still read ***"THE ASSERTION SET NOW HAS EIGHT MEMBERS"***, and **surface 1**, `task-sheet.md`, still reads ***"The set is now EIGHT"***. **The negative half of the grep control passes clean here**, because eight is not a superseded *figure* until the ninth lands; **the POSITIVE half is what catches it, and "nine" appears on no surface** — which is exactly the failure mode `CLAUDE.md` records the analytics-engineer as having added the positive half for. **Reported, not edited: `task-sheet.md` and the agent files are not this instance's to amend.**
13. **NEW: `task-sheet.md`'s invariant-labelling bullet still carries the PRE-`0076` count.** It reads *"The count is four pure code checks, one that is a code check by construction … and one item that is not an invariant at all"* — the **six-member** reading, which `0076` superseded and `task-sheet.md:995` itself calls superseded 280 lines lower. **One file, two counts, each declaring the other wrong** — the exact shape `CLAUDE.md` describes. **Reported, not edited.**
14. **NEW: `decisions/0088` §2 characterises THIS ARM's 747,478 as *"undeduplicated user-show SEASON-COVERAGE ROWS"*. Measured on this build it is not** — it is **distinct `(user, show)` PAIRS**; the season-coverage row count is a different and larger number, published in §5.5. **The ruling's conclusion is right and is applied** — two objects, both correct, do not reconcile — **but the axis it names is not the axis.** ***`0088` §4 records that all three of its own rulings named the wrong referent; this is a fourth instance of the same shape, in the entry that documents it.*** **Reported, not reconciled.**
15. **NEW, and it is a genuine ARM-AGAINST-ARM divergence of ONE PAIR.** `0087` §2 and `0088` §2 record the other arm's D9 candidate-pair split as **`435,643 + 8,834 + 281,626 = 726,103`**. This arm measures **`435,642 + 8,834 + 281,626 = 726,102`** in the same three classes — **two classes agree exactly and the S1-evidence-and-no-S2 class differs by 1.** **It is not the S3-only bridge**, which is accounted for separately in §5.5. **No entry has recorded a one-pair difference here**, because the two published totals were read as differing by the whole S3-only gap. ***REPORTED, NOT RECONCILED.***
16. **NEW: the ruled ranking basis TIES at rank 3, so the illustration is not fully determined by it.** `0088` §3 names `secondchance` (8), `theisland` (7), `maigret` (6) — and this arm reproduces the first two exactly, **but SIX loose keys tie at 6** and which of them appears third is decided by the sort's stability, not by the ruling. **Every key at every published rank is listed in §5.5 under both bases**, so the list is comparable without depending on the tie order. **Reported, not resolved.**
17. **CARRIED, `0087` F5, now the FOURTH occurrence of the string: `specs/step8-readback.md:3` still says Step 8 *"has not launched"*.** `0086` §3 stamped the two artifacts generated from that file and missed the source. **The structural half is unchanged: `specs/` is not one of `CLAUDE.md`'s eight propagation surfaces, so no control looks at it.** **Reported, not edited.**

---

*Generated by `src/step8_a_6_emit.py` from the stage outputs in `processed/step8/a/`. Every figure in this file is generated, none is typed by hand.*
