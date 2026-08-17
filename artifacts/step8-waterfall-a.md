# Step 8 — filter waterfall and required counts, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** (`decisions/0026`) · **H = 91 days** (D10) · **`τ_pull` = 2026-08-11T00:00:00Z** (D11, `decisions/0011`)

> **THIS IS A GATE DELIVERABLE. IT PROPOSES AND ADOPTS NOTHING.** No approval is recorded here and none is implied. **Zero API calls** — every figure is computed from data already on disk. **Counts and aggregates only**: no username, no user ID and no individual watch history appears in this file or in its `.json`.

> **Every figure below states its population.** There are two and they differ by construction: **APPLY** = Step 5 waterfall line 1 less D10 = **196,654**, which is what position 6 filters; **DERIV** = Step 5 waterfall line 4 less D10 = **147,370**, which requires S2 evidence. Step 8 produces both (`decisions/0070` ruling 1).

> **SCOPE OF THIS DELIVERABLE** (`decisions/0096` ruling 1). It asserts **this arm's own figures, its own inputs and its own limits, and nothing else.** It does not state the condition of other steps or gates, of the other arm, of the shared controls, or of the study as a whole: **this arm cannot measure those**, and a claim about them is expiry-dated from the moment it is written. **What it still carries is this arm's own defects, open items and divergences from the spec** — §8 and §9. **Anything this arm noticed on a surface it does not own was REPORTED to the Human Lead and is not published here as a finding.**

> **BUILD STAMP.** Every figure below was measured on build `a/2026-08-17-0096` unless it names a different build at the point of use (`decisions/0079` B6, extending `0078`). The build is defined once, with its stage-file hashes and its inputs, in §0. **The per-stage run record — which stages executed, their return codes and their timings — is `logs/step8_a_run.json`**, which is where this arm's build history lives.

> **The spec this run executes.** The filter order is `decisions/0029`, positions 1–7. The liveness rule is ALT-BROAD. The **position-3 drop set is a DELIVERABLE produced by this pipeline run** and is **read back** by the stage that computes D9 half (b) (`0079` B5), so a missing input fails loudly instead of publishing a silent 0. The discovery-channel overlap publishes in **all three units, each with its consumer named** (`0079` B7). The **four inert filter positions are labelled with the reason** (`0079` §4). The column set is the **89 ENUMERATED names** of `0080` §1 as extended by `0081` (`silent_at_tau1`) and `0082` (`p_at_bound`), asserted by **set equality on the names, never by count**. **Every invariant states its population and accounts for every row in it** (`0080` §3). **D9 publishes as a BOUND** — strict the floor, loose the ceiling, neither the point estimate (`0090`) — and **reports both halves under both keys** (`0078` §3). **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`0083` §2). The **records-examined denominator publishes as three readings, each naming the pipeline that produces it** (`0083` §1). The **D9 clustering universe is U1, ranked by distinct strict keys merged** (`0088` §3). The **two unasserted mandates are MEASURED for whether they are load-bearing** (`0088` §1) — §5.6a, §5.6b, and check 9 of the invariant report.

> Carried forward and unchanged: the table is the position-5 row set with `live` and `outcome` as columns (`0074`/1); both D9 keys are as defined by `0076`/3; the set-membership rule is a coverage count and not an invariant (`0074`/3); the `W` grid is fixed by `0075`/3; `p` is a CODE CHECK (`0076`/1); and the two DATA CHECKS of `0076`/2 are the only assertions here that can fail on data.

---

## 0. Provenance — what build every figure below was measured on

**A count needs its PROVENANCE, not only its POPULATION** (`decisions/0078` §2, made general by `0079` B6). `0047` fixed *which population produced this figure*; this is that rule one layer down — *which build produced it*. **A count without its provenance can be correct when written and wrong when read**, because the pipeline moved underneath it and nothing in the text says which pipeline it belongs to. **Partial application is worse than none**: two labelled figures imply the other counts and the 9 invariants did not need it.

**Build `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096.**

**What moved on this build.** SCOPE CHANGE, NOT A FIGURE CHANGE. This build is run against decisions/0096 ruling 1: a deliverable asserts its own figures, its own inputs and its own limits, and nothing else -- not the state of other steps or gates, not the other arm, not the shared controls, not the study as a whole. What that removes from this arm's deliverables: build-history narration, claims about the disk state of surfaces this arm does not own, and control exit statuses. No population, rule, waterfall line, outcome share, bound endpoint, invariant RESULT or measured count is changed by that removal; anything that did move is reported to the Human Lead. The per-stage run record for this build is logs/step8_a_run.json.

| Field | Value |
| :--- | :--- |
| pipeline | `src/step8_a_run.py, one run, stages 1 -> 6 in order` |
| run date (UTC) | 2026-08-17 |
| git HEAD at launch | `dbd492f`, worktree dirty: True |
| parameters | `W` = 108 d, `H` = 91 d, `τ_pull` = 2026-08-11T00:00:00Z, filter order `decisions/0029`, liveness ALT-BROAD |
| stage files (sha256, 12) | `step8_a_lib.py` 1fcabc70c6d6, `step8_a_1_scan.py` d880debf714a, `step8_a_2_positions.py` 9f08ac985c8c, `step8_a_3_table.py` 543897dabdca, `step8_a_4_arms.py` 3d533b88a113, `step8_a_4b_slugs.py` 4495f8069adb, `step8_a_5_diagnostics.py` 63d75b0142a9, `step8_a_6_emit.py` 8d8fc7be7e39, `step8_a_run.py` 1e858e7bfa89 |
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
| **4** | contamination exclusion (Step 5) — **DIFFERENT DEPTH ON THE TWO POPULATIONS, see below** | 201,900 | 18,207 | 152,126 | 67,981 | no — it fires |
| **5** | right-censoring | 196,654 | 5,246 | 147,370 | 4,756 | no — it fires |
| **6** | liveness rule | 195,951 | 703 | 147,271 | 99 | no — it fires |
| **7** | outcome assignment | 195,951 | 0 | 147,271 | 0 | **INERT BY CONSTRUCTION** — it annotates and removes nothing |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

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

**DERIV's line 4 IS NOT A SINGLE FILTER, and the table above must not be read as though it were.** The row is labelled *contamination exclusion (Step 5)* on both columns, and **DERIV's removal of 67,981 is the whole of Step 5 waterfall lines 1 through 4**, not one rule firing harder. **APPLY takes Step 5 line 1; DERIV takes line 4, which is where the population is DEFINED** — DERIV requires S2 evidence, and that requirement lives inside this position. The sub-decomposition, so no reader has to infer it:

| Step 5 line | What it removes | Retained | Removed | In APPLY's line 4? | In DERIV's? |
| :--- | :--- | ---: | ---: | :--- | :--- |
| — | entering (position 3) | 220,107 | — | — | — |
| **1** | the all-airdate and 1,542 classes | 201,900 | 18,207 | **yes — this is APPLY's line 4** | yes |
| **2** | pairs with NO S2 evidence | 178,165 | 23,735 | no | **yes — this is what DEFINES DERIV** |
| **3** | contaminated `T0` | 155,131 | 23,034 | no | yes |
| **4** | post-dated completing record | 152,126 | 3,005 | no | **yes — this is DERIV's line 4** |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**So DERIV's line-4 removal of 67,981 decomposes as 18,207 contamination (the same rule APPLY applies) + 23,735 no-S2-evidence + 23,034 contaminated `T0` + 3,005 post-dated.** The Step 5 waterfall was rebuilt from the stored per-pair flags and **asserted** equal to the published [201900, 178165, 155131, 152126, 128099] before use, so this decomposition is not a reading of Step 5's deliverable — it is recomputed and checked against it.

**The DERIV column of the main table is therefore a DEPTH, not a second run of the same filter.** Both columns are correct; the single label over them was not.
- **Positions 6 and 7 are ANNOTATIONS on the table, not deletions from it.** The analysis table is the **position-5 row set** and carries `live` and `outcome` as columns (`decisions/0074` ruling 1), so lines 6 and 7 above report what the liveness rule and the outcome assignment *select*, and the rows they do not select are still in the file with `live = false`. Downstream consumes rather than rebuilds.
- **Position 6 is OUTCOME-CONDITIONAL and is reported as such** (`decisions/0046`): the second conjunct of the liveness rule is the Continued test, so the outcome is evaluated before liveness is applied even though it is assigned at position 7. Permitted because the two predicates are row-local on the position-5 output and commute exactly, and because position 7 removes no rows.
- **Position 7 removes no rows.** It annotates.

### 1.1 Right-censoring, as two lines

| Term | APPLY removed | DERIV removed | Direction on the headline |
| :--- | ---: | ---: | :--- |
| `max(W, 91)` term | 3,684 | 3,352 | **UP** |
| incremental `+ H` term | 1,562 | 1,404 | **UP** |
| total | 5,246 | 4,756 | **UP** |

*Build: both columns measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

Both lines remove pairs whose clock start is recent, which on the uncapped `S1_completion_date` term means recent S1 completers — people who found an old show lately, have the whole series available, and are disproportionately likely to roll straight into S2. Removing likely continuers moves the never-started share **up** (Step 1 §6).

---

## 2. Position 6 — the liveness rule, and the population reconciliation

The rule this step applies is **ALT-BROAD**, as specified at `decisions/0064`: a pair is **NOT LIVE iff BOTH** (i) the account shows **no insertion instant `> τ1`** — *after* is strict — **AND** (ii) the pair is **NOT Continued**. Evidence is account-wide, runs on record **insertion** time read through the **stored** Step 5 isotonic calibration (never refitted), and is **restricted to records dated before `τ_pull`** (`0070` ruling 2).

| Population | Entering (position 5) | Excluded | never-started | started-and-left | accounts | Retained |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | **703** | 604 | 99 | 216 | 195,951 |
| **DERIV** | 147,370 | **99** | 0 | 99 | 73 | 147,271 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**This is a POPULATION RECONCILIATION, not an invariant** (`decisions/0068`). Expected 703 on APPLY = 196,654 (604 + 99, 216 accounts) and 99 on DERIV = 147,370 (0 + 99, 73 accounts). **Measured: 703 and 99, with the same splits and the same account counts.** This is the first place Step 7's chain and Step 8's positions 1–5 have been compared: Step 7 built APPLY from the Step 5 pair table rather than through the filters. They agree to the row.

**Neither superseded answer was produced.** 604 is ALT's, 793 is ALT-MATCHED's; either would mean a superseded rule had been implemented.

**How the conjuncts select on APPLY:** conjunct 2 (NOT Continued) narrows 196,654 → 52,514; conjunct 1 (silent at `τ1`) narrows 52,514 → 703. Conjunct 1 does most of the work, which is why the count moves with `W`.

**Evidence scope, measured rather than assumed:** with the `< τ_pull` restriction 703 pairs are excluded; without it 703. The restriction is inert on the exclusion set at this arm, as `0070` recorded, because no insertion instant exceeds the calibration clamp at 2026-08-10T20:48:00Z and D10 already forces `τ1 ≤ τ_pull − 91 d`.

### 2.1 Line 6 read as a marginal cost — both figures, on both populations

**703 is NOT the marginal cost of the silence test** (`decisions/0085` §5). **The silence test alone excludes 1,355 on APPLY; the `NOT Continued` conjunct spares 652; `1,355 − 652 = 703`.** **1,355 is the figure that makes line 6 readable as a marginal cost, and a reader holding only 652 cannot recover it without knowing to add.** **Both, on both populations, with the identity stated:**

| Population entering line 6 | Silence test ALONE excludes | `NOT Continued` SPARES | Line 6 exclusions | Identity |
| :--- | ---: | ---: | ---: | :--- |
| APPLY, position-5 input to line 6 (196,654 rows) | **1,355** | **652** | **703** | 1,355 − 652 = 703 ✓ |
| DERIV, position-5 input to line 6 (147,370 rows) | **751** | **652** | **99** | 751 − 652 = 99 ✓ |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

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

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**The two published categories are measured over different horizons and must never be described as measured alike**: never-started is a 108-day statement, Continued a 199-day statement (`0034`).

**Abandonment point `p`** is the rank form `|{e ∈ E2 : e ≤ max(A_H)}| / L2`, defined only on Started-and-left; the raw ratio is withdrawn. Range on the table's row set (APPLY, position 5): [0.0385, 1.0000]. The **`p = 1.0` residual** — watched the finale, missed the 90 percent threshold — is 1,246 pairs on APPLY position 5 and 1,230 post-liveness, and is its own named category, not part of 'near-finale'. `p` is null on every row that is not Started-and-left.

### 3.1 `p_at_bound` — WHETHER `p` reached its bound, and the `p = 1.0` totals

> **TWO DIFFERENT `FALSE` CLASSES SIT ON THIS PAGE, AND THEY ARE NAMED APART WITH BOTH CARDINALITIES EMITTED ON ALL FOUR POPULATIONS.** One is the COEXTENSIVITY GAP and is empty; the other is the column's own `FALSE` value and is not. **Step 8b defines the schema Steps 9–13 write into with NO CONVERSION LAYER**, so a consumer that reads *"the FALSE class is empty"* and provisions a two-valued column is wrong by **17,895 rows** on APPLY position 5.

| | **CLASS 1 — the COEXTENSIVITY GAP** | **CLASS 2 — the COLUMN's own `FALSE` value** |
| :--- | :--- | :--- |
| What it is | rows where `0082`'s two **mechanisms** disagree: saturated-not-final **plus** final-not-saturated — **that two-mechanism definition is SUPERSEDED and the motive behind it is WITHDRAWN (`0083` §2)** | Started-and-left rows where **`p` did not reach its bound** |
| The sentence that names it — **both quoted from superseded/withdrawn text, neither asserted here** | *"the class `0082` called FALSE is **empty**"* | *"`p_at_bound` is FALSE on the rest of Started-and-left"* |
| Is it empty? | **YES — 0 on all four populations** | **NO — 17,895 on APPLY position 5** |
| What a `FALSE` row here would mean | one of the three construction links has broken | nothing at all — it is the ordinary case |

**`p_at_bound` marks WHETHER `p` reached its bound, NOT WHY** — Human Lead ruling, 2026-08-16 (`decisions/0083` §2), restating `0082`. **`TRUE` where `p` is at its bound, `FALSE` on the remaining Started-and-left rows, null where `p` is null.** `0082`'s definition **by two mechanisms** is **superseded**: the two clauses are **coextensive** — on a chain of three links of which the first two are construction and the third, `max(E2) = F2`, is MEASURED (`0085` §4) — so **CLASS 1** is **empty** and on the adopted rank form there is only one why. **The column is kept** — Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the spike **labelled**, and **an emptiness asserted in prose and never emitted cannot be checked.**

**The `p = 1.0` counts are TOTALS, not a sum of two classes** (`0083` §2). **1,246 and 1,230 are this instance's own measurements**, and they are **one class counted twice**; reading them as a split is a **withdrawn argument** (`CLAUDE.md`, third blindness class).

**FOUR CELLS ON FOUR POPULATIONS** (`decisions/0085` §3). **Total, in-both-classes, saturated-not-final, final-not-saturated and in-neither, on APPLY position 5, APPLY post-liveness, DERIV position 5 and DERIV post-liveness.** This is `CLAUDE.md`'s standing **both populations, always** rule, not a new requirement, and **an emptiness asserted in prose and never emitted cannot be checked** — which is why each population gets its own row rather than one standing for the rest.

| Population | `p = 1.0` TOTAL | in BOTH classes | saturated, not final | final, not saturated | in NEITHER | rows examined (`p` defined) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 5 | **1,246** | 1,246 | 0 | 0 | 0 | 19,141 |
| APPLY, post-liveness | **1,230** | 1,230 | 0 | 0 | 0 | 19,042 |
| DERIV, position 5 | **1,072** | 1,072 | 0 | 0 | 0 | 16,843 |
| DERIV, post-liveness | **1,056** | 1,056 | 0 | 0 | 0 | 16,744 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**The coverage column is not decoration.** Three of the four cells are zero on every row of this table, and **an empty result and a clean result are the same value** — the count of rows the cells were computed over is what says which this is.

**The `p = 1.0` figures are TOTALS, not a sum of two classes**, and the `TRUE` count equals the total on all four populations because **CLASS 1** is empty.

#### The emitted column's own cardinalities — `TRUE`, `FALSE`, null

**This is what a Step 8b schema has to provision for**, so it is emitted rather than left derivable.

| Population | rows | `p_at_bound` **TRUE** | `p_at_bound` **FALSE** | **null** | identity |
| :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | 196,654 | 1,246 | **17,895** | 177,513 | `1246 TRUE + 17895 FALSE + 177513 null = 196654` — holds: True |
| APPLY, post-liveness | 195,951 | 1,230 | **17,812** | 176,909 | `1230 TRUE + 17812 FALSE + 176909 null = 195951` — holds: True |
| DERIV, position 5 | 147,370 | 1,072 | **15,771** | 130,527 | `1072 TRUE + 15771 FALSE + 130527 null = 147370` — holds: True |
| DERIV, post-liveness | 147,271 | 1,056 | **15,688** | 130,527 | `1056 TRUE + 15688 FALSE + 130527 null = 147271` — holds: True |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**CLASS 1 is 0 on all four populations: True.** **CLASS 2 is not zero anywhere** — it is the ordinary Started-and-left row that left before the finale, and it is the large majority of them. **Two numbers under one word, with only one emitted, is unreadable, so both are emitted.**

*One thing worth noting rather than leaving to be spotted: the null counts on DERIV position 5 and DERIV post-liveness are **identical**. That is not a copy — DERIV's 99 liveness exclusions are **all started-and-left**, so every row the filter removes has `p` defined and none of them was null.*

**THE CHAIN HAS THREE LINKS AND ONLY TWO ARE CONSTRUCTION** (`decisions/0085` §4). **A future `FALSE` row would mean one of THREE things had broken, not two.**

1. **`m_H ∈ E2`** — **CONSTRUCTION.** The set-membership drop rule drops any episode whose `number` is not in `E2`, so `A_H ⊆ E2` and its maximum is a member of `E2`.
2. **`|{e ∈ E2 : e ≤ m_H}| = L2 ⟺ m_H = max(E2)`** — **CONSTRUCTION**, given `L2 := |E2|`, which the spec fixes.
3. **`max(E2) = F2`** — **NOT CONSTRUCTION.** It holds only because **the finale is the highest-numbered listed episode**, and **where a season lists an episode numbered above its finale the two separate** — the `s2_aired_lt_listed` case this step is told to count. **MEASURED, NOT ASSUMED: 0 of 1,138 frame shows have `max(E2) ≠ F2`, and 0 shows carry `s2_aired_lt_listed`.** The frame does not move across Step 13's grid, so this is measured once and holds at every arm.

**So the two clauses are coextensive, and the emptiness is measured rather than asserted.** On APPLY position 5: **1,246** rows satisfy both, **0** satisfy the numerator clause alone, **0** the final-episode clause alone, and **0** neither.

**A SECOND fact, measured and NOT the same argument:** **0 of 1,138 frame shows have any S2 numbering gap**, so `E2 = {1…L2}` everywhere, `F2 = L2`, and the rank form reduces to `m_H / L2`. **That one is DATA and could be false on another frame; the coextensivity above would still hold.** Stated separately so a construction argument is not read as a frame accident.

**Why the column is still worth emitting.** **CLASS 1** is empty because of links 1 and 2, **both `W`-invariant**, and link 3, **a frame property that does not move across Step 13's grid** — so it stays empty at every arm. **A CLASS 1 row anywhere means one of the THREE has broken**, and that is a thing worth catching. **The emitted column itself is three-valued**: `TRUE` exactly on the `p = 1.0` rows, `FALSE` on the remaining Started-and-left rows — **17,895 of them on APPLY position 5, not zero** — and null elsewhere. **That is CLASS 2 and it is a different object from CLASS 1, which is the empty one.**

---

## 4. Per `W` arm

**Arms: 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days**, fixed by `decisions/0075` and by `task-sheet.md` Step 13 — **not this instance's choice.** Two instances on different grids produce tables that cannot be diffed at all. `H` is held constant at 91 across every arm. **D10 is re-derived at each arm and never frozen** (`decisions/0047`), so the arms do not share a denominator.

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**The aggregate hides a cohort-asymmetric loss.** At `W = 108` 97.40% of pairs survive right-censoring, but the 2023–2025 cohort keeps 95.9% against 97.8% pre-2020. At `W = 213` the modern cohort keeps 89.5% — a loss of **10.5%** against 3.0% pre-2020. The loss falls on the uncapped `S1_completion_date` term, so the modern cohort is not merely smaller after censoring but differently selected.

**The `W = 108` row reproduces `0070` ruling 8 exactly** — 97.40% aggregate and 97.8% / 97.4% / 95.9% by period, and 89.5% for 2023–2025 at `W = 213` — measured here independently through the mandated filter order.

**The comparator on the other side of that sentence is also measured here.** `0033`'s pre-2020 comparator at `W = 213` was **2.7%** on the position-3 output; on the position-4 output the mandated order censors, this instance measures **3.0%**, which is the figure `decisions/0073` carries.

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

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

*Build: every figure in this table, at every arm, measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**The cleared-share series is 99.53% at `W = 46` down to 97.73% at `W = 213`, on APPLY** — the series `decisions/0075` fixes, measured here independently. **`decisions/0034`'s 95.98% → 91.34% is SUPERSEDED at this point of use**: it was measured on the amendment's **uncensored estimation sample of 128,099** and carried no population where it was used. **The direction and the shrinkage stand; the level does not.**

**Reported and not resolved: the series is not monotone in `W`.** It rises between `W = 91` (98.81%) and `W = 107` (98.84%) before resuming its fall. Both the clearance bound `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` and the Started-and-left denominator move with `W`, and they do not move together — the denominator drops faster than the cleared count between those two arms. Listed open at `decisions/0076` §5; measured here, not resolved.

**Reported alongside, and labelled a COUNT and not a rate: 3,440 Started-and-left pairs completing S2 at any point before `τ_pull`.** Its population is **THE UNCENSORED STEP 5 ESTIMATION SAMPLE OF 128,099 PAIRS -- not APPLY, not DERIV (0068; measured at 0034 SS3)**. It is restated, not recomputed on Step 8's population, and it must not be reported against APPLY or DERIV. Exposure-weighted by show recency: a 2016 title offers ten years in which a completion can be observed and a 2025 title about eighteen months, so the count mixes exposure with behaviour. It is a floor because the estimation sample excludes the pairs the Step 5 waterfall drops and is not right-censored (Step 14 item 9). The two figures do not bracket the quantity — both truncate observation and neither is a lower bound on the other.

*Build: **this figure is NOT on `a/2026-08-17-0096`.** It was measured at `decisions/0034` §3 on the Step 5 revision-6 **uncensored estimation sample of 128,099 pairs**, and it is restated here rather than recomputed. **It must never be reported against APPLY or DERIV.** Saying which build a figure came from is the whole point of the provenance rule, and this is the figure in this deliverable that most needs it.*

---

## 5. The other required counts

**Every count in this section was measured on build `a/2026-08-17-0096`** unless it says otherwise at the point of use (`decisions/0079` B6). The two exceptions are marked where they appear: the **3,440** in §4.3, and the figures `0078` restates from the **position-5 build of 2026-08-13**, which are re-measured here and agree.

### 5.1 Both drop counts (Step 1 §3.4) — a COVERAGE COUNT, not an invariant

**The set-membership drop rule is reported, not asserted** (`decisions/0074` ruling 3). Step 8's own bullet already calls it *"an implementation check, not a data check"*, and asserting it would add another passing line to a report where SIX OF NINE checks cannot fail on any data.

**Coverage: 6,065,704 in-frame S1/S2 episode records examined across 1,138 shows, 0 dropped.** This is a measured zero, not an empty check.

- **Per show:** 0 dropped episode records and 0 distinct dropped `(season, number)` pairs, on 0 shows. Per-show detail is in `processed/step8/a/drops_per_show.csv` (not published: it is a per-show table, and the aggregate is what belongs here).
- **Per outcome:** 0 pairs had their entire S2 evidence dropped. **Denominator: never-started at position 5 = 33,373** — what entered the liveness filter — with the **post-liveness 32,769 reported alongside** (`0070` ruling 6). The difference between the two is exactly the 604 never-started liveness exclusions. Direction, had it been non-zero: it **inflates** never started.

**The records-examined denominator publishes as a coverage figure, in three readings** (`decisions/0083` §1). The readings are **one family indexed by where D11 is applied**, and **each names the pipeline that produces it.** This instance produces **6,065,704 — reading A, D11 nowhere.**

| Reading | Where D11 is applied | Pipeline | Records examined | Drops |
| :--- | :--- | :--- | ---: | ---: |
| **A — produced here** | nowhere | `src/step8_a_run.py`, build `a/2026-08-17-0096` | **6,065,704** | 0 |
| B | S2 side only | not this instance's pipeline; recorded at `0083` §1 | 6,065,610 | 0 |
| C | both sides | not this instance's pipeline; measured here as a counterfactual | 6,065,537 | 0 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**Readings B and C drop 0 because reading A drops 0.** The dropped set measured on the full record set is **empty**, and B and C examine **subsets of it**, so their drop counts are 0 by containment rather than by assumption. **The numerator is 0 three times over.**

**The gap decomposes exactly.** D11 discards **167** in-frame S1/S2 records, of which **94 are S2-side and 73 are S1-side.** So the three readings differ by **where D11 is applied and nowhere else**: 6,065,704 with none, 6,065,610 with D11 on the S2 side, 6,065,537 with D11 on both. **The 94-record difference `decisions/0074` records is exactly the S2-side count.** Every other candidate axis is zero and was measured, not assumed:

- definition used here: episode records (kind == episode) whose show is in the Step 2 frame and whose season is 1 or 2, counted BEFORE the set-membership drop rule and BEFORE D11
- undated (`watched_at` null): **0**
- exact duplicate `(user, play id)` records: **0**
- records with a non-positive episode `number`: **0**

**Why the no-D11 reading.** The figure is the **coverage count of the set-membership drop rule** (`0074` ruling 3), so its denominator is *what that rule examined*. The rule is `number ∈ E`; **it does not read `watched_at` at all**, so every in-frame S1/S2 episode record passes under it whatever its date, and a denominator that pre-filters on a timestamp would report a smaller number than the rule actually looked at — **a check that reports having looked at fewer rows than it looked at**. D11 is a real global cutoff and it is applied everywhere it bears: on `A` and `A_H`, on the action counts, on the liveness evidence, on D9's coverage rows. **It does not bear on this one**, because this one is not a computation on the timeline.

**The three readings are not three measurements of one quantity that disagree; they are three different quantities, exactly identified**, and the 94/73 split says which is which with nothing left over. **The rule this figure is the denominator of dropped zero records under every reading.**

**A separate question, and this instance does not decide it.** Whether D11 applies to the **S1 completion walk** is `0068`'s open item: reading C moves waterfall line 1 to **220,103** because **4 pairs stop being completers** and **0 completion dates move** (§5.6). **This instance measured it and did not apply it.**

### 5.2 D2 — negative lag, split THREE ways

| Population | pairs | first S2 watch before clock start | share | S2-finale binds | S1-completion binds | **both bind** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, position 5 | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| DERIV, position 5 | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |
| APPLY, position 7 | 195,951 | 49,356 | 25.19% | 44,135 | 5,214 | 7 |
| DERIV, position 7 | 147,271 | 47,453 | 32.22% | 43,207 | 4,239 | 7 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

#### The `max()` binding term, split three ways — ON EVERY POPULATION THIS STEP NAMES

**The spec requires the population at the point of use and measurement on both** (`decisions/0092`, N2; `0070` ruling 5), so no integer below appears without the set it was counted over.

| Population | pairs | S2 finale binds | S1 completion binds | **both bind** | identity |
| :--- | ---: | ---: | ---: | ---: | :--- |
| line 1 — S1-completer population | 220,107 | 103,898 | 116,041 | **168** | `103898 + 116041 + 168 + 0 not asserted = 220107` — holds: True |
| APPLY, position 5 | 196,654 | 87,441 | 109,045 | **168** | `87441 + 109045 + 168 + 0 not asserted = 196654` — holds: True |
| APPLY, post-liveness | 195,951 | 86,854 | 108,929 | **168** | `86854 + 108929 + 168 + 0 not asserted = 195951` — holds: True |
| DERIV, position 5 | 147,370 | 68,426 | 78,791 | **153** | `68426 + 78791 + 153 + 0 not asserted = 147370` — holds: True |
| DERIV, post-liveness | 147,271 | 68,378 | 78,740 | **153** | `68378 + 78740 + 153 + 0 not asserted = 147271` — holds: True |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**A TIE IS ITS OWN CATEGORY, NOT A TIEBREAK** (`0070` ruling 5). The three cases — finale strictly later, S1 completion strictly later, **equal** — partition every completer pair, so the identity holds on every row of the table.

**THE COUNT IS INVARIANT ACROSS EVERY APPLY READING AND IS NOT POPULATION-INVARIANT.** **168 on all three APPLY readings** — line 1, position 5 and post-liveness (`line_1_S1_completer_population, APPLY_position_5, APPLY_post_liveness`) — because **no both-bind pair is removed by positions 4, 5 or 6 on APPLY**, so a bare `168` cannot say which of those three sets it was counted over. **On DERIV this instance measures 153**, which is where the population becomes visible in the integer. **`decisions/0092` §3 records that the spec carried `168` with no population at the point of use**; this instance's answer is the table above, population by population.

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

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

Measured over the fixed horizon `H`, never to the pull date, so the share is a rate and not an exposure-weighted mixture. **D8(ii) is the only bound on the never-started boundary** and its size is Step 14's ledger item 10. Direction: **down**.

### 5.5 D9 — split artifacts, both halves

Detection is imperfect and **every count here is a lower bound**.

**D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS THE CEILING, AND NEITHER IS THE POINT ESTIMATE.** Human Lead ruling, `decisions/0090`. ***`0074` ruling 5's framing is SUPERSEDED by it and is struck here, quoted only as what no longer governs — ~~"use the strict key and report the loose count alongside"~~ — under which STRICT WAS THE ANSWER and loose was context. Neither endpoint may be quoted as "D9's result".***

**It is `0074` ruling 5's own reason carried through:** the loose count publishes **because it bounds how wrong strict could be**, and **a quantity published to bound another is an endpoint, not a footnote.** `0078` §3 already ran this argument once, to extend the loose count to half (b) — **same reason, one step further.**

| D9 quantity | **bound `[floor, ceiling]`** |
| :--- | :--- |
| complementary signature ID pairs | **`[0, 75]`** |
| half (a) — the fabricated never-started row | **`[0, 6]`** |
| half (b) — the silently deleted S1-failing counterpart | **`[0, 27]`** |

*Build: all six endpoints measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**DIRECTION IS PART OF THE LABEL, and it is not symmetric.** **Strict is the FLOOR** because it matches only slugs identical modulo punctuation, so it **cannot over-count**. **Loose is the CEILING** because stripping a trailing year **merges genuinely different shows** — remakes and national versions. **The error runs opposite to D9's own lower-bound caveat**, which is why the interval publishes rather than being resolved away. **The bound applies to every D9 quantity with both forms, not the headline alone** — applying it to one and not the others is the defect `0078` §3 corrected.

**A ZERO FLOOR IS NOT AN ABSENCE OF EVIDENCE**, so the coverage publishes beside it — **a bound whose floor is 0 and whose coverage is unstated is indistinguishable from a check that looked nowhere.** The strict key was applied to **747,478 slugged user-show pairs**, of which **726,102 carry S1 or S2 evidence and are matchable**; half (a) was measured against **32,769 never-started pairs** and half (b) against **58,345 pairs in the position-3 drop set**. *Build: every coverage figure in this paragraph measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**THE THIRD KEY IS NOT AN ENDPOINT.** Its **76** is **a different key's answer** — it reduces `the-100` to `the` — and is **reported as a divergence, never as the ceiling** (`0090`; `0076`, `0078` §3).

**THE COVERAGE QUANTITIES, EACH NAMED BY WHAT IT COUNTS** (`decisions/0088` §2(b), as corrected on its axis by `0089` §2(b)). **One label over two quantities is the defect, and reconciling them would collapse two real objects into one**, which the standing rule forbids. ***The axis `0088` §2(b) named is SUPERSEDED*** — `0089` §2(b) corrects it, and the sentence that carried it is **registered as a superseded string** in `src/step7_register.py` and is deliberately **not restated here**. This arm publishes **all three of its own units** so no reader has to infer which one a bare number is:

| | Unit | Count |
| :--- | :--- | ---: |
| **A** | undeduplicated user-show **SEASON-COVERAGE ROWS** — distinct `(user, show, season-class)` triples, season-class in {S1, S2, S3+} | 1,217,122 |
| **B** | distinct user-show **PAIRS** in the coverage pivot — any dated pre-`τ_pull` episode record in season ≥ 1, **including pairs whose only evidence is S3 or later** | **747,478** |
| **C** | **D9 CANDIDATE** user-show pairs — B less the S3-or-later-only pairs; the pairs the complementary-coverage search can match on | 726,102 |
| | *bridge: B − C, pairs with only S3-or-later evidence* | *21,376* |
| | show IDs carrying a title slug, in the map | 46,428 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**THE FIGURE THIS ARM PUBLISHES AS `747,478` IS UNIT B — distinct `(user, show)` PAIRS.** ***That is `decisions/0089` §2(b)'s correction to `0088` §2(b)'s axis, and it is stated here rather than below the table.*** This arm's undeduplicated row count is a different and larger object, unit A above: 1,217,122. The ruling's **conclusion** — two objects, both correct, do not reconcile — **is applied here.**

**This arm's D9 candidate split is C: 435,642 + 8,834 + 281,626 = 726,102.** **`decisions/0089` §3 records a ONE-PAIR divergence between the arms in the S1-evidence-and-no-S2 class, reported and not reconciled**; the figure above is this arm's own measurement and the comparison is the decision log's, not this arm's. It is **not** the 21,376 S3-only pairs, which are the whole of the B-against-C gap and are accounted for above.

**The normalisation key decides the entire number, and both keys are DEFINED in the spec** (`0076` §3 defines both, because "strict" and "loose" had existed only inside one instance's code, which the other is forbidden to read):

| Key | Definition | complementary ID pairs | half (a) | half (b) |
| :--- | :--- | ---: | ---: | ---: |
| **STRICT — the FLOOR** | lowercase, drop every non-alphanumeric character, strip nothing else | **0** | **0** | **0** |
| **LOOSE — the CEILING** | remove a trailing four-digit year, then strict | **75** | **6** | **27** |
| *third key — NOT RULED, measured only* | strip a trailing digit group of arbitrary length, then strict | 76 | 6 | 28 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE** (`decisions/0078` §3). **This follows from `0074` ruling 5's own reason rather than from a preference:** the loose count publishes **because it bounds how wrong strict could be**, and **that reason applies to half (b) exactly as it applies to half (a)**. Publishing the bound for one half and withholding it for the other **leaves the reader unable to bound the total**, and the error runs **opposite** to D9's own lower-bound caveat — the direction they were not warned about.

| | strict — **FLOOR** | loose — **CEILING** |
| :--- | ---: | ---: |
| **half (a)** — fabricated never-started row | **0** | **6** |
| **half (b)** — silently deleted S1-failing counterpart | **0** | **27** |

*Build: all four numbers measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.* **Both columns are endpoints under `0090`; neither column alone is the answer.**

- **(a) the fabricated never-started row, at the FLOOR:** 0 of 32,769 never-started pairs (APPLY, position 7); 0 of 33,373 on the position-5 table row set.
- **(b) the silently deleted S1-failing counterpart:** 0 of 58,345 pairs that fail the S1 completion rule. **These rows are not in the analysis table and cannot be recovered from it**, so the set is a **DELIVERABLE of this pipeline run** (`decisions/0079` B5, strengthening `0075` ruling 2) — **and this section READS IT BACK from the file**, so if the stage stopped writing it this figure would **fail loudly rather than publish a 0**, which is the whole point: **a zero here reads as a data finding rather than a missing input.** **`decisions/0077` §2 states which set this is**: *"position 3's drop set"* names an **empty set** on this frame, because line 1 is already the S1-completer population and position 3 therefore removes 0 rows from the waterfall. The set is **the pair universe less the completers, 58,345 PAIRS**, and it is **not** the set-membership drop rule, which is a different rule and deletes 0 **records**.
- **The loose count is the CEILING because it BOUNDS HOW WRONG STRICT COULD BE**, and the error runs **opposite** to D9's own lower-bound caveat. it strips the year and merges genuinely different shows -- remakes and national versions, not split metadata, which is the artefact D9 exists to count. That is exactly why it CANNOT UNDER-COUNT and is therefore the upper endpoint (decisions/0090).

**THE CLUSTERING UNIVERSE IS U1, RANKED BY DISTINCT STRICT KEYS MERGED** (`decisions/0088` §3). **The universe and the ranking basis are named at the point of use**, because the cluster examples are the evidence for the loose key's only warrant and a list whose universe is unstated is not reproducible.

**The ground, as ruled:** the artifact D9 hunts is **a viewer's history splitting across two metadata entries for one show**, and **that split can occur anywhere in a history, not only among shows that survived the frame filters.** A frame-restricted universe finds only splits where **both sides made the cut** — the narrowest case — and **a bound computed on a narrow slice bounds very little.**

**This arm clusters U1 -- every distinct show ID appearing anywhere in the pulled sweep that carries a slug, deduplicated to ONE ROW PER SHOW ID** — **U1 = 46,428 show IDs**, read from the slug map collected over all 2,549 parsed history files, which is what *"anywhere in the pulled sweep"* means. **It is NOT U2 (the 1,138 frame shows) and NOT U3 (the 75 D9 candidate pairs).** 1,829 loose keys merge more than one strict key.

**TWO SIZED OBJECTS SIT BEHIND THE WORD "SWEEP" AND THIS ARM PUBLISHES BOTH.** U1 is 46,428; the narrower **D9 COVERAGE PIVOT** — show IDs reaching the pivot through a dated, pre-`τ_pull`, season ≥ 1 episode record — is **46,366**; and **U1 − pivot = 62**, shows reaching the sweep only through a record D11 discards, an undated record, a specials-only record or a non-episode record. **The subset relation is asserted in the pipeline, not assumed.** **The clustering here runs on U1**, and `distinct_show_ids_in_the_sweep` is not a label this arm uses for the pivot count, because the pivot is not the sweep.

**And "largest" ranks by DISTINCT STRICT KEYS MERGED into one loose key -- how many separate metadata entries the loose key collapsed. Ruled by decisions/0088 ruling 3 because it was unstated and REORDERS THE LIST ON ITS OWN: ranked by distinct SHOW IDs instead, `blackout` displaces `maigret`. Both orders are emitted.**

| Ranked by distinct STRICT keys merged | | Ranked by distinct SHOW IDs merged | |
| :--- | ---: | :--- | ---: |
| `secondchance` | 8 | `secondchance` | 8 |
| `theisland` | 7 | `theisland` | 7 |
| `yourhonor` | 6 | `blackout` | 7 |

*Build: both cluster lists and the universe counts measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**THE RULED BASIS TIES AT RANK 3, so a bare "third-largest cluster" is not reproducible from the basis alone.** The head-of-list above is a `head(3)` whose order at rank 3 is decided by the sort's stability rather than by the ruling. **Every key at every published rank, both bases:**

| Rank value | Ranked by distinct STRICT keys merged | Ranked by distinct SHOW IDs merged |
| ---: | :--- | :--- |
| 8 | `secondchance` | `secondchance` |
| 7 | `theisland` | `blackout`, `theisland` |
| 6 | `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` | `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` |

**The basis reorders the list on its own, exactly as `0088` §3 says:** `blackout` carries **6 strict keys but 7 show IDs**, so it sits at rank 3 on one basis and rank 2 on the other, and ranking by show IDs displaces `maigret`. **The U3 illustration — The Twilight Zone, The Traitors, Manhunt — is SUPERSEDED as the example by `0088` §3; those three names are not wrong, they are another universe's answer.**

**One row per show ID needs a tie-break and this arm states its own:** lexicographically first slug per show ID. Stated rather than implicit; the sensitivity is measured, not assumed. **2 show IDs carry more than one slug.** Under the last slug instead the cluster count is 1,829 against 1,829 — **measured, not assumed away.**

**The clusters the loose key merges are remakes and national versions, exactly the failure `0074` names.**
- **The third key is reported for the record and is neither ruled key.** It reduces `the-100` to `the` and gives 76 complementary pairs. **`decisions/0076` §3 defines the two ruled keys and records a 76-against-75 divergence as REPORTED, NOT RECONCILED**; under the defined keys this instance measures the floor and ceiling in the table above.
- **Merges, counted with the same query and reported separately:** 20 user-show rows on the strict key (5,551 on the loose key) where one ID carries both seasons and a same-title ID also appears in the sweep. Merges can only add evidence to a pair, never remove it.
- Direction: D9 moves the never-started share **down**, plus an unmeasured denominator loss on half (b).

### 5.6 `pull_date`, fetch dates and discarded records (D11)

- **`pull_date` = `τ_pull` = 2026-08-11T00:00:00Z**, a single global frozen cutoff.
- **Per-user fetch dates:** first page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:08.519916+00:00; last page, earliest 2026-08-11 05:01:26.447766+00:00 and latest 2026-08-11 23:10:31.236946+00:00. The D11 constraint `pull_date ≤ earliest per-user fetch date` **holds**.
- **Records discarded for `watched_at ≥ τ_pull`:** 1,734 across the whole sweep, of which 167 are in-frame S1/S2 records. A further 379 records carry no `watched_at` at all and cannot be placed on the timeline.
- **Carried as an open question, not resolved:** applying D11 to the S1-completion walk gives 220,103 completers rather than 220,107 — 4 pairs — and moves 0 completion dates. `0068` fixes line 1 at the published 220,107 and lists this as open; this instance measured it and did not apply it.

### 5.6a The half-open form — MEASURED, not self-reported (B3(a))

**`decisions/0088` §1.** The two unasserted mandates are **the half-open UTC-instant form** and **D11-as-global-cutoff** — *not* invariants 7 and 8, which are already measured, published and labelled DATA CHECK here. **This arm's compliance is TRUE**: **NO BOUNDARY TEST in `step8_a_*.py` uses a date-level form**, every bound comparison is an int64-second comparison, and `date(watched_at) <= T1` appears nowhere. ***Compliance was never the gap. Nothing measured whether either mandate is LOAD-BEARING on this data, and an unmeasured pass is indistinguishable from a check that looked nowhere.***

> **THE CLAIM IS ABOUT BOUNDARY TESTS AND IS NARROWER THAN "no day-flooring anywhere", WHICH WOULD BE FALSE OF THIS ARM.** `floor_day()` appears three times in `step8_a_2_positions.py` — on the S2 finale date, on the first-pass S1 completion instant, and when parsing the stored Step 5 dates for the cross-check. **All three are correct and required**: `⟦T0⟧` is **day-floored by Step 1 §2.4**, the clock start is a date and not an instant, and **the next paragraph of this section reasons from it.** **The distinction the mandate draws: day-flooring the CLOCK is required; day-flooring a BOUNDARY TEST is forbidden — and there are none.** No `.date()`, `dt.date` or `normalize()` call appears anywhere in `step8_a_*.py`.

**One thing the ruling does not say, and it decides the answer.** `T0` is day-floored and `W` and `H` are whole days, so **`τ1` and `τ2` land exactly on midnight UTC** — asserted in the pipeline, not assumed. The date-level form `date(ts) < date(τ1)` is therefore **identical** to the half-open `ts < τ1` and can never differ. **The form that CAN differ is `date(ts) ≤ date(τ1)`, which admits the whole of `[τ1, τ1 + 24h)`.** So the window the ruling names — `[τ1 − 24h, τ1)` — is the window on which the two forms **agree by construction**, and the interval on the **other** side is where the mandate is load-bearing. **Both are emitted; reporting only the named one would answer the question with the interval that cannot separate them.**

| Population | Bound | in `[τ − 24h, τ)` *(ruling's window)* | **exactly at `τ`** | **where the two forms ACTUALLY differ** | rows affected | vacuous? |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | `τ1` | 749 | **1** | **703** | 311 | no — load-bearing |
| APPLY, position 5 | `τ2` | 291 | **0** | **303** | 136 | no — load-bearing |
| DERIV, position 5 | `τ1` | 676 | **1** | **595** | 275 | no — load-bearing |
| DERIV, position 5 | `τ2` | 254 | **0** | **261** | 117 | no — load-bearing |

**Coverage:** 196,654 rows and 2,135,938 distinct S2 episodes on APPLY; 147,370 rows and 1,766,159 episodes on DERIV. **Unit: distinct S2 episodes by canonical timestamp** — the objects the bound is actually tested against, since `A` and `A_H` are sets of distinct episodes. *Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**RESULT: THE MANDATE IS LOAD-BEARING, NOT VACUOUS.** On APPLY a `date(ts) ≤ date(τ1)` form would admit **703 episodes on 311 rows** into `A`. **No cell is 0, so no invariant here is labelled vacuous** — and where a cell had been 0 it would have been **stated as a zero, not passed silently**.

> ***A COINCIDENCE, FLAGGED SO IT IS NOT MISREAD.*** The APPLY `τ1` differing-episode count is **703**, **the same integer as the 703 liveness exclusions.** **They are unrelated objects** — one counts distinct S2 episodes in a 24-hour interval, the other counts pairs removed at position 6 — **and no arithmetic connects them.** This report states it because a repeated integer in a document this size gets read as a shared quantity.

**The ruling's own second quantity, on this section's unit:** exactly **1 distinct S2 episode falls exactly AT `τ1`** on APPLY (and 1 on DERIV).

> **THAT EPISODE COUNT SAYS NOTHING ABOUT `0068`'s STRICTNESS RULING, AND THIS REPORT DRAWS NOTHING FROM IT.** ***`0068`'s strictness ruling is about INSERTION INSTANTS in the silence test*** — *"a pair is silent iff it has no insertion instant `> τ1`"* — **and the unit of the table above is a DISTINCT S2 EPISODE BY CANONICAL `watched_at`. Two different axes.** The ruling's own quantity is measured immediately below, on its own object.

#### `decisions/0068`'s strictness ruling, measured on ITS OWN object

**The only rows on which strict `>` and non-strict `>=` can differ are pairs whose account's last insertion instant falls EXACTLY at `τ1`.** That is the ruling's quantity, and it is what says whether the ruling decides anything on this data.

| Population | rows examined | pairs with last insertion instant **exactly at `τ1`** | accounts | silent, adopted (strict) | silent, non-strict | liveness exclusions, adopted | …non-strict | verdict |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | 196,654 | **0** | 0 | 1,355 | 1,355 | 703 | 703 | **VACUOUS ON THIS DATA** |
| DERIV, position 5 | 147,370 | **0** | 0 | 751 | 751 | 99 | 99 | **VACUOUS ON THIS DATA** |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

***RESULT: `0068`'s STRICTNESS RULING IS VACUOUS ON THIS DATA — 0 pairs on both populations.*** **Stated as a zero, not passed silently.** The rule remains correct and remains binding on any future pull; **what is measured here is whether it decides anything on THIS data, and it does not.**

#### The number that settles B3(a): OUTCOME-STATE FLIPS, not episodes admitted

**Episodes ADMITTED is not the object B3(a) turns on** (`decisions/0089` §2(a)). **The number that settles it is how many position-5 rows CHANGE OUTCOME STATE under the forbidden `date(ts) ≤ date(τ)` form — four numbers, both bounds × both populations.** The episode counts above are a different and also-reported quantity.

**A never-started row with an episode in `[τ1, τ1 + 24h)` flips to started**, because `|A|` goes from 0 to ≥ 1. **A started-and-left row with one in `[τ2, τ2 + 24h)` can flip to Continued**, because `A_H` gains an episode and both the `F2` clause and the 0.90 clause can turn on it. **Each bound is varied ALONE** — that is what "both bounds" means; the joint form is reported separately because a row can flip at `τ1` and again at `τ2`, so it is not the sum.

| Population | Bound varied | **rows changing OUTCOME STATE** | transitions | liveness exclusions under this form |
| :--- | :--- | ---: | :--- | ---: |
| APPLY, position 5 | `τ1` only | **52** | never_started → started_and_left 16, never_started → continued 36 | 703 *(adopted 703, move +0)* |
| APPLY, position 5 | `τ2` only | **19** | started_and_left → continued 19 | 703 *(adopted 703, move +0)* |
| APPLY, position 5 | *both (not the sum)* | **71** | never_started → started_and_left 16, never_started → continued 36, started_and_left → continued 19 | 703 *(adopted 703, move +0)* |
| DERIV, position 5 | `τ1` only | **45** | never_started → started_and_left 14, never_started → continued 31 | 99 *(adopted 99, move +0)* |
| DERIV, position 5 | `τ2` only | **14** | started_and_left → continued 14 | 99 *(adopted 99, move +0)* |
| DERIV, position 5 | *both (not the sum)* | **59** | never_started → started_and_left 14, never_started → continued 31, started_and_left → continued 14 | 99 *(adopted 99, move +0)* |

**THE FOUR NUMBERS: APPLY at `τ1` = 52, APPLY at `τ2` = 19, DERIV at `τ1` = 45, DERIV at `τ2` = 14.** *Build: all four measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**Coverage:** 196,654 rows on APPLY and 147,370 on DERIV — asserted non-empty, because a zero measured on zero rows is not a zero. **NOT VACUOUS: the half-open form decides published outcome states.**

**What that buys, stated as an effect on the headline and not only as a count.** On APPLY the `τ1` mandate holds **52 rows** in **never-started** that the forbidden form would move out of it — **16** to started and left, **36** to continued — and the `τ2` mandate holds **19 rows** in **started-and-left** that it would move to Continued. **Both directions run against the study's own estimand**: the forbidden form would understate never-started and understate abandonment.

#### Line 6 under the counterfactual — measured, and scoped to what was measured

> **NO PROPERTY OF CONJUNCT 1 EXPLAINS THIS, AND NONE IS OFFERED.** The liveness rule is **conjunct 1 AND conjunct 2**, and **conjunct 2 is `NOT Continued`, an episode-timestamp computation that MOVES under this counterfactual.** So the invariance of the conjunction is a measurement, not a consequence of the silence test reading an insertion clock.

**CONJUNCT 2 IS RECOMPUTED ON THE COUNTERFACTUAL OUTCOME, and this is stated because `703 → 703` would be a tautology if it were held at the adopted one.** **A reader cannot tell a measurement from an identity unless the deliverable says which.** The expression is `silent & ~cont_, where cont_ is the COUNTERFACTUAL Continued mask under this variant's bounds` — `cont_` is the counterfactual Continued mask returned by the counterfactual state function under that variant's bounds, and the adopted `continued` mask is not used in it. **It is stated at every cell of the table below, not inferred.**

| Population | Bound varied | conjunct 2 rows that **MOVE** | exclusions, this form | exclusions, adopted | **never-started** | **started-and-left** | excluded ROW SET identical? |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | `τ1` only | **36** | 703 | 703 | 604 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |
| APPLY, position 5 | `τ2` only | **19** | 703 | 703 | 604 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |
| APPLY, position 5 | both | **55** | 703 | 703 | 604 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |
| DERIV, position 5 | `τ1` only | **31** | 99 | 99 | 0 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |
| DERIV, position 5 | `τ2` only | **14** | 99 | 99 | 0 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |
| DERIV, position 5 | both | **45** | 99 | 99 | 0 | 99 | True *(symdiff 0; cf∖adopted 0, adopted∖cf 0)* |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**THE 604/99 SPLIT UNDER THE COUNTERFACTUAL IS THE COLUMN PAIR ABOVE**, on both populations. **The measurement goes further than the total: the excluded ROW SET is identical, not merely its cardinality** — symmetric difference **0** on every variant and both populations.

#### The symmetric difference confirms the arithmetic; it is not independent evidence

> **A SYMMETRIC DIFFERENCE OF 0 IS NOT STRONGER HERE THAN THE UNCHANGED TOTAL, AND THIS REPORT DOES NOT CLAIM IT IS.** It would be stronger under an arbitrary perturbation. It is not under this one, and the reason is measured below rather than argued.

**Why it cannot be stronger here.** The date-level form **RELAXES** both bounds, so per row `|A|` and `|A_H|` can only **grow**. **All three Continued conjuncts are monotone non-decreasing in them** — `|A| ≥ 1` in `|A|`; `|A_H| ≥ ⌈0.90·L2⌉` in `|A_H|`; and `m_H = F2` because set membership bounds `m_H ≤ F2`, so it can only **reach** `F2` and never leave it. **So `Continued` only turns ON, `NOT Continued` only turns OFF, and the exclusion set `silent ∧ ¬Continued` can only SHRINK.** **A row can LEAVE the exclusion set and none can ENTER it**, so **an unchanged TOTAL already forces an identical SET.** The symmetric difference of **0** therefore **confirms the arithmetic**; it is not an independent fact about the two sets.

**MEASURED, NOT ARGUED — every clause of that reasoning is a count on this build.**

| Population | rows examined | `\|A\|` decreased | `\|A_H\|` decreased | `m_H` decreased | rows with `m_H > F2` | Continued turned OFF (τ1 / τ2 / both) |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| APPLY, position 5 | 196,654 | 0 | 0 | 0 | 0 | 0 / 0 / 0 |
| DERIV, position 5 | 147,370 | 0 | 0 | 0 | 0 | 0 / 0 / 0 |

**Every clause holds on both populations: `True`.** And the subset direction is emitted per variant beside the symmetric difference — `rows_excluded_by_the_COUNTERFACTUAL_but_not_by_the_ADOPTED_rule` is **0** everywhere, which is the direction monotonicity forbids from being anything else. *Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**WHAT THE INVARIANCE IS: A MEASURED FACT ABOUT THIS DATA AT `W = 108`, NOT A STRUCTURE.** **No pair the adopted rule excludes is among the rows whose Continued value flips.** **Under the monotonicity above, that statement and "the total does not move" are the same fact and not two.** **It remains a property of this frame at this arm, not of the rule.**

**SCOPE OF THE CLAIM, AS MEASURED: W = 108 ONLY, on APPLY = 196,654 and DERIV = 147,370, position-5 row sets, build a/2026-08-17-0096. It is NOT claimed at any other arm and NOT claimed as a structural property of the rule.** **Step 13 re-runs the rule across eight arms**, and nothing here says what it will find there.

> **This is a COUNTERFACTUAL.** `date(watched_at) <= T1` still appears nowhere in the implementation, and nothing this pipeline emits changes. The counterfactual state function is asserted to reproduce the adopted outcome exactly on the half-open form before any comparison is made, so the baseline cannot be the thing that differs.

### 5.6b D11 applied per site, asserted at each (B3(b))

**`decisions/0088` §1(b).** D11 is specified to apply *"to EVERY computation"*. **Every site carries its own unit, its own count and its own assertion — not one assertion about the rest.** **Ground, as ruled: the unstated version of exactly this scope produced Step 7's 792-against-791.**

> **THE `examined` COLUMN IS ONE KIND OF QUANTITY IN EVERY ROW: the units the site CONSUMES before D11.** The distinction matters at `S1_completion_walk`, where three different objects could each be called "the number" — a **record** count of post-cutoff candidates, a **would-exclude** count, and the **distinct episodes** the walk examines. **All three are named** — see below the table.

| Site | Unit | examined | **excluded by D11** | *would exclude if applied* | D11 applied? | assertion |
| :--- | :--- | ---: | ---: | ---: | :--- | :--- |
| `action_count_s1_watch` | in-frame in-E S1/S2 episode records | 2,717,040 | **49** | — | yes | **PASS** |
| `action_count_s1_checkin` | in-frame in-E S1/S2 episode records | 153,246 | **1** | — | yes | **PASS** |
| `action_count_s1_scrobble` | in-frame in-E S1/S2 episode records | 383,834 | **23** | — | yes | **PASS** |
| `action_count_s1_other` | in-frame in-E S1/S2 episode records | 0 | **0** | — | yes | **PASS** *(looked at ZERO units — holds trivially)* |
| `action_count_s2_watch` | in-frame in-E S1/S2 episode records | 2,364,954 | **52** | — | yes | **PASS** |
| `action_count_s2_checkin` | in-frame in-E S1/S2 episode records | 120,993 | **4** | — | yes | **PASS** |
| `action_count_s2_scrobble` | in-frame in-E S1/S2 episode records | 325,637 | **38** | — | yes | **PASS** |
| `action_count_s2_other` | in-frame in-E S1/S2 episode records | 0 | **0** | — | yes | **PASS** *(looked at ZERO units — holds trivially)* |
| `A_the_set_tested_at_tau1` | distinct S2 episodes on position-5 rows | 2,135,938 | **0** | — | yes | **PASS** |
| `A_H_the_set_tested_at_tau2` | distinct S2 episodes on position-5 rows | 2,135,938 | **0** | — | yes | **PASS** |
| `liveness_evidence` | records, ALL kinds and ALL shows | 27,656,813 | **1,734** | — | yes | **PASS** |
| `D9_coverage_rows` | dated season >= 1 episode records feeding the D9 coverage pivot | 24,645,658 | **1,543** | — | yes | **PASS** |
| `S1_completion_walk` | DISTINCT S1 EPISODES | 2,860,465 | **0** | 60 | **NO — declared** | **PASS** |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**Every `examined` cell above is the same kind of quantity: units the site consumes before D11.** The *would exclude if applied* column is populated only where the site does not apply D11.

**The three objects behind `S1_completion_walk`, named apart:**

| Object | Count |
| :--- | ---: |
| in-frame **S1 RECORDS** at or after `τ_pull` | 73 |
| **distinct S1 EPISODES touched** by those records | 72 |
| **distinct S1 EPISODES whose CANONICAL instant** is at or after `τ_pull` — *the only one D11 would remove from this walk* | **60** |
| **distinct S1 EPISODES the walk EXAMINES** — *the `examined` cell* | 2,860,465 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**The third is smaller than the second because an episode's canonical instant is the MINIMUM `watched_at` over its records**, so an episode with one post-cutoff record and one earlier record stays pre-cutoff. **`decisions/0089` §1 names these three objects; this arm measures all three independently and its measurements are the counts above.**

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

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

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

`processed/step8/a/analysis_table.csv.gz` — **196,654 rows, 89 columns**, one row per user-show pair, **the POSITION-5 row set on APPLY** (`decisions/0074` ruling 1). Build: every count in this section measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.

- **`live` and `outcome` are COLUMNS, not filters.** 195,951 rows carry `live = true` and 703 carry `live = false` — the position-6 exclusions are **in the file**, not reconstructed from it. Both readings of "one row per pair" give identical counts, so this is a ruling and not a correction: **a reconstruction that agrees today is still a second definition tomorrow, and the dual diff cannot see it.**
- **147,370 rows carry the DERIV flag**, so both populations are produced by Step 8 and nothing downstream has to rebuild one.
- It carries outcome state, abandonment point, the two discovery-channel booleans, the per-pair action counts and all 60 Step 2 show fields. **It stays in `processed/` and is never published.**

**THE COLUMN SET IS ENUMERATED, NOT COUNTED — 89 NAMES, EXACTLY THESE** (`decisions/0080` §1, replacing `0077` §3's count; **extended to 88 by `0081`** and **to 89 by `0082`**). Step 8b's schema is built on this vocabulary with Steps 9–13 writing into it **directly, with no conversion layer** (`0066`), so it is fixed **before** the schema exists. **This instance asserts SET EQUALITY against the spec's list, not a count** — a count is arithmetically satisfiable by the wrong columns. Column **order** is specified nowhere; this table is in construction order and the sorted list is in the `.json` so an order difference cannot be mistaken for a name difference.

**The count is 89 again after `0082`, but it is a different 89** than `0077`'s: `f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not matching a set**, which is why the assertion here is on the names.

**AND THE LIST ASSERTED AGAINST IS NOW READ OFF `task-sheet.md` AT RUN TIME** — 89 distinct names parsed from the enumeration block, matching this arm's transcription: **True**. **A hand transcription would be a second copy of the enumeration, and a propagation change to the spec would not reach it** — and **the dual diff cannot catch a propagation failure**, so only a check that opens the spec file can. **A parse that found nothing FAILS rather than passes**, and the parsed count is published above.

**Two names are in the set that `0080` did not have:**

- **`silent_at_tau1` — RESTORED by `decisions/0081`, and the reason is the one `0080` §2 stated when it dropped the column.** It is **not recoverable from `live` and `outcome` on Continued rows**, because `live` is true for **every** Continued pair regardless of silence — the rule's second conjunct is `NOT Continued`. **Without it the Continued-and-silent count cannot be recomputed from this table.** That count is **652** — the **size of the outcome-conditioning**, the figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation. It is **both a column and an aggregate** here (652 on APPLY position 5, 652 post-liveness, 652 on DERIV position 5), so the figure is readable without opening the table. Build: these three counts measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.
- **`p_at_bound` — added at `decisions/0082`, definition restated by `0083` §2.** It marks **WHETHER `p` reached its bound, not why.** Emitted as a **nullable** boolean: null where `p` is null, because an inapplicable value and a false one must not look alike. **`0082`'s two-mechanism definition is superseded** — the clauses are coextensive, on a three-link chain whose third link is measured and not construction (`0085` §4), and the `FALSE` class is empty — **and the column is kept anyway**, because Step 10 needs the spike labelled and because an emptiness asserted in prose and never emitted cannot be checked. §3.1.

**Two names stay dropped and both are free** (`0080` §2, unchanged by `0081` and `0082`): **`max_episode_in_A`**, read by nothing downstream, and **`f2_in_A_H`**, derivable as `max_episode_in_A_H == s2_F`. `0077`'s spelling ruling — `A_H`, not `AH` — still governs `n_A`, `n_A_H` and `max_episode_in_A_H` without the dropped column.

**The names themselves are `decisions/0077` §3's and were not chosen here.** The mapping from the pre-`0077` vocabulary: `in_channel_*` → **`discovered_channel_a` / `discovered_channel_b`**; `in_population_APPLY` / `in_population_DERIV` → **`in_apply` / `in_deriv`**; `tau1_utc` / `tau2_utc` → **`tau1` / `tau2`**; `T0_utc_date` → **`t0_date`**; `T0_binding_term` → **`t0_binding_term`**; `s1_completion_date_utc` → **`s1_completion_date`**; `n_A_distinct_s2_before_tau1` → **`n_A`**; `n_AH_distinct_s2_before_tau2` → **`n_A_H`**; `max_episode_in_AH` → **`max_episode_in_A_H`**; `n_rec_s{1,2}_*` → **`action_count_s{1,2}_*`**. **No `_utc` suffix survives**: every instant in this study is UTC by Step 1 §2.4, and suffixing some columns implies the others are not.

**Two extra columns are kept** (`0077` §3, and both are in `0080`'s enumeration): `has_s3_or_later_evidence`, which D4 reads, and **`s1_completion_used_a_post_cutoff_record`**, which the still-open D11-at-position-3 question reads. The second is computed independently here rather than assumed: the first-pass walk runs in ascending canonical-timestamp order, so the completing episode's timestamp is the maximum over the prefix consumed, and the flag is exactly `complete AND comp_ts ≥ τ_pull`. **It is true on 4 pairs of the 220,107** — the same 4 that stop being completers when D11 is applied to the S1 walk, which is the arithmetic the open question turns on. Build: that count measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.

### 6.1 The position-3 drop set — a DELIVERABLE of this run, not a side file

`processed/step8/a/position3_drop_set.csv.gz` — **58,345 pairs, the pairs that FAIL the S1 completion rule.** **Human Lead ruling, `decisions/0079` B5:** it is **named in the deliverable list**, **written by the same pipeline run that writes the table** (stage 2 of `src/step8_a_run.py`), and carries **each pair's distinct-episode counts and the show's threshold**, which is what D9 half (b) reads.

- **It is read back, not merely written.** The stage that computes half (b) loads this file and asserts it against position 3's recomputed rule (58,345 rows agreeing to the row). **If it were missing, that stage fails loudly instead of publishing 0** — which is the failure `0075` ruling 2 exists to prevent, since **a zero here reads as a data finding rather than a missing input.** A helper script's side file is not a thing the next run is obliged to produce; a stage of this run is.
- **Columns:** `row`, `user_idx`, `show_trakt_id`, `n_distinct_s1_episodes`, `n_distinct_s2_episodes`, `s1_L`, `s1_F`, `s1_completion_threshold_ceil_0_90_L1`, `s2_L`, `reason_short_of_threshold`, `reason_finale_F1_not_watched`.
- **Why the pairs fail:** 57,518 never reached `ceil(0.90 × L1)` distinct S1 episodes; 827 reached the threshold but never watched the S1 finale `F1`.
- **It is the pair universe less the completers — position 3's RULE, not its waterfall line**, which is 0 by construction (`0077` §2). It is **not** the set-membership drop rule, which is a different rule and deletes 0 **records**.
- Build: all four counts in this subsection measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0. **`0078` restates the 58,345 as *position-3 rule, position-5 build of 2026-08-13*; this instance measures 58,345 on the build named above.**

**Other working files, also in `processed/step8/a/` and also never published:** `position5_table.npz`, the per-arm working table; `drops_per_show.csv`; `show_slugs.csv`; the stage `.json` outputs this report is generated from.

---

## 7. The scope qualifier that travels with this population

Step 8 does not compute Step 9's bound, but it produces the position-6 population the bound is stated on. So, wherever that population is named: **the bound is covering with respect to insertion-dormancy, exhaustively; open only across channel classes (D4, D9).** **D4 and D9 publish alongside and are never folded in** (`0062`).

---

## 8. What this instance had to decide, and what it did not resolve

Listed rather than settled. Each is a place two isolated instances can differ while both following the written spec.

1. **The `W` arm grid is not this instance’s choice.** It is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days, fixed by `decisions/0075` ruling 3 and by `task-sheet.md` Step 13.
2. **One table or eight.** The analysis table is built once at `W = 108`; the per-arm requirements are computed as aggregates by re-running positions 5–7 at each arm. The step says "build one row per user-show pair" in the singular and does not say which object is per-arm.
3. **D11 at position 3.** Not applied, per `0068`; the counterfactual is measured and reported in §5.6.
4. **The contamination exclusion is read from Step 5's stored per-pair flags**, and the published Step 5 waterfall is asserted before use rather than re-derived. Step 5 is a closed gate.
5. **`p` on non-Started-and-left rows** is null, not 0 and not omitted. The spec defines `p` only for Started-and-left and does not pin the representation.
6. **"All Step 2 show fields"** is read literally: all 60 non-key columns of `frame.csv`, including derived ones.
7. **Populations for the required counts.** Seven of the required outputs name no population. Each is reported here on a named population, and on more than one where the computation is cheap, rather than one being chosen silently.
8. **D3′'s denominator is the position-7 (post-liveness) Started-and-left set**, which is what reproduces `0075`'s ruled series. The position-5 figures are emitted alongside in the `.json` so the choice is visible and neither reading is hidden.
9. **The set half (b) is measured on is named by the spec, not chosen here.** *"Position 3's drop set"* names an empty set on this frame; `decisions/0077` §2 states the intended object and `0079` B5 makes it a deliverable — **the pair universe less the completers, 58,345 pairs**, written and read back by this run (§6.1). The unit is **pairs**, and it is **not** the set-membership drop rule.
10. **The column set is an enumeration, not a count** (`decisions/0080` §1, taken to 89 names by `0081` and `0082`), and this instance asserts **set equality on the names** against the list parsed from `task-sheet.md` at run time. A count is arithmetically satisfiable by the wrong columns, so the count is not the check.
11. **Column ORDER is specified nowhere.** This table is in construction order; the sorted name list is in the `.json`. **If the arms differ here it is an order difference, not a name difference**, and the enumerated set is identical either way.
12. **The `build` label's granularity.** `0079` B6 requires every count to name its build and does not say at what granularity. This instance defines the build once (§0, with stage file hashes and the git HEAD) and cites a **tag** at each figure; the alternative — the full record inline at every figure — carries the same information and reads worse. **A figure measured on a different build says so instead** (the 3,440).
13. **`p_at_bound` marks WHETHER `p` reached its bound, not why** (`decisions/0083` §2). The `FALSE` class of the two-mechanism reading is empty by construction and the `p = 1.0` counts publish as **totals** — §3.1.

---

## 9. This instance’s own open items and divergences from the spec

**SCOPE** (`decisions/0096` ruling 1). Every item below is something THIS ARM measured or decided. **Nothing here reports the disk state of another surface, the status of another step or gate, the other arm, or a shared control** — those are not this arm’s measurements, and anything of that kind this run noticed was **reported to the Human Lead** rather than published here.

1. **D3′ is not monotone in `W`.** It rises between the 91 and 107 arms before resuming its fall — §4.3, where the mechanism is stated. **Measured, not resolved.**
2. **D11 at position 3 is not applied, and the counterfactual is measured.** Applying D11 to the S1 completion walk gives 220,103 completers rather than the 220,107 this run uses, and moves 0 completion dates — §5.6, §5.6b. `0068` fixes line 1 at 220,107 and lists the question as open; **this instance measured it and did not apply it**, and the `s1_completion_used_a_post_cutoff_record` column carries the pairs it turns on.
3. **The D9 clustering basis ties at rank 3 and the tie-break is unruled.** `0088` §3 ranks by distinct strict keys merged; on that basis **six loose keys tie at 6** in this arm’s measurement, so a bare “third-largest cluster” is not reproducible from the basis alone. **Every key at every published rank is listed under both bases** in §5.5, so nothing is lost while it is open. **Reported, not resolved.**
4. **The one-pair D9 candidate divergence.** This arm measures `435,642 + 8,834 + 281,626 = 726,102` in the three candidate classes. **`decisions/0089` §3 records a ONE-PAIR difference between the arms in the S1-evidence-and-no-S2 class, reported and not reconciled.** The figure above is this arm’s own measurement; the comparison is the decision log’s.
5. **`decisions/0090`’s scope, read broadly by this arm.** The entry says the bound is *“applied to this half”*, singular, and this arm applies it to **every D9 quantity with both forms** — complementary pairs, half (a), half (b) — on `0078` §3’s ground that publishing a bound for one half and a point estimate for the other leaves the reader unable to bound the total. ***If a single half was meant, this arm’s §5.5 table is what would narrow.*** **Reported at the point of use.**
6. **The invariant set has nine members and only two can fail on data.** §“What the invariant set does and does not establish” in the invariant report states the split, derived from the label strings rather than typed. **This is a limit of what this deliverable can falsify, and it is published rather than left to be inferred.**
7. **The 3,440 is on a population Step 8 does not compute** — Step 5’s uncensored estimation sample of 128,099 — and is **restated, not recomputed**. It must never be reported against APPLY or DERIV. §4.3.
8. **`decisions/0033`’s censoring percentages were measured on the position-3 output** and this instance censors the position-4 output, as the mandated order requires. The figures this instance measures are in §4.1; the difference is the filter order, not the data.

---

*Generated by `src/step8_a_6_emit.py` from the stage outputs in `processed/step8/a/`. Every figure in this file is generated, none is typed by hand.*
