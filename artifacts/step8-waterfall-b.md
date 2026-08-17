# Step 8 — filter waterfall and required counts (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**This is a RERUN ordered by the Human Lead**, on `task-sheet.md` Step 8 as it now stands — the spec as amended through **`decisions/0091`** and Red Team's **SEVENTH** pass. **It is a rerun, not an amendment: everything below is rebuilt from the stored data by the same pipeline that writes the table, and no previous output was patched** (`0092`'s standing rule as given to this instance — a deliverable is corrected by rerunning the arm that produced it). Against this arm's last deliverables (the 2026-08-16 `-r5` run, spec through `0090`), **four things change and all four are corrections to this arm's own work.** **(1) THE SURFACE CHECK NOW OPENS `artifacts/`, WHICH IS PROPAGATION SURFACE 6** (`step8-invariants-b.md` §16). `-r5`'s invariant report carried *"a report where six of EIGHT cannot fail on data"* **in its own body**, inside a document whose head states the set is NINE and whose surface check concludes that no surface still states the old count — **because that check opened `task-sheet.md`, this arm's definition file and `specs/step8-readback.md`, and never opened `artifacts/`.** The run now greps its own four deliverables, splits every hit into *named as superseded at the point of use* against *live*, prints its byte coverage, and **fails the run on a live one.** **(2) THE SAME CLASS, SECOND INSTANCE: `0090`'s superseded framing sat BELOW the line that strikes it** (§10). `-r5` rendered *"Why the loose count publishes EVEN THOUGH STRICT IS RULED"* — `0074` ruling 5's framing — 85 lines under §10's strike of exactly that framing. Corrected at the point of use. **(3) THE `both bind` COUNT NOW NAMES ITS POPULATION AND IS MEASURED ON BOTH** (§7a). `-r5` published the integer **168** in two deliverables under two populations 23,453 pairs apart and reconciled them nowhere. **Measured on every population here: 168 on line 1 and 168 on APPLY position 5 — both correct, the quantity is invariant across the APPLY chain — and 153 on DERIV, which had never been measured.** So the review's arithmetic premise is contradicted by this build and its provenance premise is upheld; **reported, not reconciled.** **(4) THE LABELLING SENTENCE NO LONGER CONTRADICTS ITSELF** (`step8-invariants-b.md`). `-r5` said *"SEVEN of the nine assertions CANNOT FAIL ON ANY DATA"* and then called one of the seven a genuine cross-check **because** a value is recomputed independently — which is what gives it force, and a check with force can fail. **6 of 9 cannot fail on any data; 3 can, as specified.** Every count in that paragraph is now **derived from the `label` field** rather than typed. **Two smaller repairs, both found by re-reading this arm's own output:** the per-site D11 table's **D9 row carried `null` for both its exclusion count and its assertion** while the site was counted among the twelve where D11 is applied — **backfilled and asserted at the site** (§14a(b)) — and the column-set block published **two counts and no list**, asserting a count match where the code asserts a set match; **the names are emitted.** **(5) Carried from `-r5`, re-executed not restated:** `0090`'s D9 **bound** — complementary pairs `[0, 75]`, half (a) `[0, 6]`, half (b) `[0, 27]`, **neither endpoint the point estimate**; and B3(a)'s reversed verdict on the separating interval `[τ, τ + 24h)` — **`OUTCOME_DECIDING`**, **71 APPLY rows** and **59 DERIV rows** change outcome state under the forbidden `date(watched_at) <= T1` form (`τ1` alone 52 / 45, `τ2` alone 19 / 14); and the executed negative control — **6 injected defects, 5 of 5 checkable cases caught, asserted, with the one that passes by design named.** **No population moves and no waterfall line moves.** Line 1 is **220,107**, APPLY is **196,654**, DERIV is **147,370**, position 6 removes **703** and **99**, and the column set is **89**. This overwrites the previous `-b` deliverables.

**Provenance — `analytics-engineer-b / Step 8 position-5 build of 2026-08-16-r6 (RERUN on the spec as amended through decisions/0091 and Red Team's SEVENTH pass; W = 108, tau_pull = 2026-08-11T00:00:00Z, mandated filter order 1-7, 89 columns)`.** Every count, every waterfall figure and every invariant result below was measured on that build (`0078`, `0079` §2). Where a figure is quoted from a ruling, the ruling's own build is named instead: `position-5 build of 2026-08-13 (both arms, the run decisions/0078 labelled)`. **A count without its provenance can be correct when written and wrong when read.**

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

Censored population: **the POSITION-4 output, 201,900 (the mandated order)**.

| Term | Pairs removed | Direction on the headline |
| :--- | ---: | :--- |
| `max(W, 91)` | 3,684 | **UP** on the never-started share |
| incremental `+ H` | 1,562 | **UP** on the never-started share |
| total | 5,246 | |

Both removals fall on recent S1 completers — people who found an old show lately, have the whole series available and are disproportionately likely to roll straight into S2. A single combined figure would hide the price of `H` inside a removal that predates it.

### Retained pairs per air period after right-censoring, every `W` arm

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

### The denominator — CLOSED, published as a coverage figure, all three readings with their pipelines named

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**`0083` §1 CLOSES this and amends `0074` ruling 4's routing to Step 14.** `0074` had published **6,065,704 against 6,065,610** as *reported, not reconciled*, on the ground that neither figure is wrong on its face. **That ground was right and the routing was wrong: there was never a conflict to reconcile.** The readings are points on a **one-parameter family indexed by where D11 applies**, the parameter is `0068`'s own open item, and **every member of the family drops zero records** — so the numerator is 0 three times over, the difference survives into no result, and a Step 14 limitation is an uncertainty that *does* survive into one. **`0074`'s "publish both, not one" stands and is strengthened to three.**

| Reading | D11 applied to | Records examined | Records dropped | Waterfall line 1 |
| :--- | :--- | ---: | ---: | ---: |
| **A** | nowhere | 6,065,704 | 0 | 220,107 |
| **B — this instance publishes this one** | the S2 side only | 6,065,610 | 0 | 220,107 |
| **C** | both seasons | 6,065,537 | 0 | **220,103** |

**The decomposition is exact.** D11 discards **73 in-frame S1 records** and **94 in-frame S2 records**, **167 in total**, and that split is the whole of the difference: 6,065,704 − 94 = 6,065,610, and 6,065,704 − 167 = 6,065,537. **`0074`'s 94 is the S2-side component alone**, which is the gap between readings A and B.

**The other candidate axes were checked and are all zero on this build — re-measured, not quoted.** `0083` §1 records them as zero on both arms; a figure carried from a ruling and not re-run can be correct when written and wrong when read, so all three were computed again here over the 6,065,704 records of reading A's slice: undated records **0**, exact duplicate `(user, play id)` records **0**, records with a non-positive `number` **0**. **The 94 has one cause and it is fully accounted.**

**Stated so the zeros are not read wider than they are:** across the *whole sweep* — not the in-frame S1/S2 slice the denominator counts — there are **379** undated records and **182** exact duplicate `(user, play id)` records. **None of either is in the slice**, which is why the axis is zero *for this denominator*; the sweep-level counts are given because a zero reported without its scope reads as a zero everywhere.

**Why this instance publishes reading B, stated as a reason and not a preference.** D11 says every record with `watched_at ≥ tau_pull` is discarded from **every** computation, and this instance applies it everywhere **except** the S1 completion walk. The exception is not chosen here: `0068` **rules waterfall line 1 at 220,107 as published**, and 4 pairs reach that count only on a completing record D11 would discard, so reading C cannot produce the ruled base. The coverage denominator is then a **consequence** of the record set the pipeline actually examines.

**What stays open, and it is NOT this.** Whether D11 applies to the **S1 completion walk** is `0068`'s own open item — reading C moves line 1 to **220,103**, because **4 pairs stop being completers and 0 completion dates move** (§14 measures both). **Choosing between B and C is that question, answered there, not here.** Recording it in two places is how a ruling gets made twice and diverges.

**One thing does not move under any reading: all three report 0 records dropped**, and nothing downstream reads the denominator.

**The zero is a measured zero.** Every one of the 6,065,610 records was tested for membership in its season's listed set `E`, and none failed. Direction had any been dropped: it would **inflate** Never started, the same direction as D4 and D9.

## 7. D2 — negative-lag report, split THREE ways

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

A tie is its own category, not a tiebreak (`0070` ruling 5).

### 7a. The `both bind` count, **measured on every population** — `0070` ruling 5's 168

**Unit: user-show PAIRS whose T0 = max(S2 finale, S1 completion) has both terms binding on the same UTC day.**

| Population | n | **pairs where BOTH terms bind** |
| :--- | ---: | ---: |
| `line1_220107` | 220,107 | **168** |
| `position3_220107` | 220,107 | **168** |
| `position4_201900` | 201,900 | **168** |
| `APPLY_position5_196654` | 196,654 | **168** |
| `APPLY_position6_post_liveness_195951` | 195,951 | **168** |
| `DERIV_position5_147370` | 147,370 | **153** |
| `DERIV_position6_post_liveness_147271` | 147,271 | **153** |

**This arm's own defect, corrected rather than patched.** This arm's -r4 build published the integer 168 in TWO deliverables under TWO populations -- `tie_pairs_in_line1` on waterfall line 1 (220,107) in step8-waterfall-b.md, and `rows_where_the_two_terms_are_the_same_date` on the APPLY position-5 row set (196,654) in step8-invariants-b.md -- with no line reconciling them. The populations differ by 23,453 pairs. Reported here rather than silently repaired.

**And the review premise is measurably false on this data — reported, not reconciled.** The finding as put to this arm is '168 cannot be correct on both'. MEASURED: IT IS CORRECT ON BOTH. Every one of the tie pairs survives positions 2 through 6 on APPLY, so the count is 168 on line 1, 168 at position 3, 168 at position 4, 168 at position 5 and 168 post-liveness. The two figures agreed because the quantity is invariant across the APPLY chain, NOT because either was measured wrongly. THE DEFECT IS REAL AND IS THE OTHER HALF OF THE FINDING: neither figure NAMED its population, and neither had ever been measured on DERIV -- where it is NOT 168. Reported, not reconciled: the arithmetic claim in the finding is contradicted by this build, the provenance claim is upheld.

**step8-invariants-b.md invariant 5's `rows_where_the_two_terms_are_the_same_date` is this quantity on the APPLY position-5 row set, computed from the INDEPENDENTLY recomputed S1 completion date rather than from the pipeline's `binds` label. Agreement between the two is therefore a cross-check and not a restatement; it is asserted at stage 3.**

### 7b. Negative-lag pairs, split three ways

| Population | n | Negative lag | share | S2 finale binds | S1 completion binds | BOTH bind |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `line1_220107` | 220,107 | 64,321 | 29.22% | 58,584 | 5,730 | 7 |
| `position3_220107` | 220,107 | 64,321 | 29.22% | 58,584 | 5,730 | 7 |
| `position4_201900` | 201,900 | 49,708 | 24.62% | 44,177 | 5,524 | 7 |
| `APPLY_position5_196654` | 196,654 | 49,403 | 25.12% | 44,177 | 5,219 | 7 |
| `APPLY_position6_post_liveness_195951` | 195,951 | 49,356 | 25.19% | 44,135 | 5,214 | 7 |
| `DERIV_position5_147370` | 147,370 | 47,500 | 32.23% | 43,249 | 4,244 | 7 |
| `DERIV_position6_post_liveness_147271` | 147,271 | 47,453 | 32.22% | 43,207 | 4,239 | 7 |

**The `BOTH bind` column here is the NEGATIVE-LAG subset and is a different quantity from §7a's** — same predicate, intersected with `first S2 record < T0`. Both are emitted because `0070` ruling 5's 168 is §7a's, and reading it off this table gives a smaller number under the same words.

**Every population the spec could mean is reported and each is labelled** (`0047`, `0078` §2). S1-term negative lags are the actual test of the first-pass choice and should be small; S2-finale-term negative lags are the normal case for anyone who watched a weekly season while it was airing, and their size is information about the frame's cadence mix rather than about data quality.

## 8. D3′ — resumption rate, every `W` arm, each denominator its own

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

Measured over `[tau1, tau1 + H) = [tau1, tau2)` — **not to the pull date**. Direction: **DOWN** on the headline.

| Population / position | Never started | (i) any S2 episode in the horizon | share | (ii) satisfies the Continued condition | share |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 2,733 | 8.19% | 1,820 | 5.45% |
| APPLY_position6_post_liveness | 32,769 | 2,733 | 8.34% | 1,820 | 5.55% |
| DERIV_position5 | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |
| DERIV_position6_post_liveness | 9,145 | 2,508 | 27.42% | 1,689 | 18.47% |

**The spec does not say whether D8 sits pre- or post-liveness**, so both are reported and labelled. D8(ii) is the only bound on the never-started boundary and its size is Step 14's ledger item 10.

## 10. D9 — split-artifact counts, both halves, **both keys**

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

Signature: one show ID carrying S1 and not S2 for that user, another carrying S2 and not S1, and the two slugs normalise to the same title key. **IMPERFECT -- Step 1 D9 states the count is a LOWER BOUND**

**Four numbers, not three** (`0078` §3): half (a) under strict and loose, half (b) under strict and loose. The requirement follows from `0074` ruling 5's own reason — the loose count publishes **because it bounds how wrong strict could be** — and that reason applies to half (b) exactly as to half (a). Publishing the bound for one half and withholding it for the other leaves the reader unable to bound the total, and **the error runs opposite to D9's own lower-bound caveat**.

Candidate `(user, show)` pairs examined across the whole sweep: **726,103** — 435,643 carrying S1 and not S2, 8,834 carrying S2 and not S1, 281,626 carrying both.

### 10z. The D9 coverage quantities — **named as separate objects, at the point of use**

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**`0088` §2.** Decisions/0088 Sec 2 -- one name over two quantities is not a divergence, and reconciling would collapse two real objects into one. Each quantity below states what it counts and over what. **747,478 and 726,103 are different objects and both correct**: undeduplicated user-show **season-coverage rows** against distinct candidate `(user, show)` **pairs** — a user-show carrying two seasons contributes **two rows and one pair**. **One name over two quantities is not a divergence, and reconciling would collapse two real objects into one.** This arm publishes **`distinct_candidate_user_show_PAIRS`** and states what each quantity counts.

| Quantity | Value | What it counts |
| :--- | ---: | :--- |
| `distinct_candidate_user_show_PAIRS` | 726,103 | distinct (user, show) PAIRS carrying at least one S1 or S2 episode record after D11, across the WHOLE SWEEP -- not the frame |
| `undeduplicated_user_show_SEASON_COVERAGE_ROWS` | 1,007,729 | (user, show, season) rows over the same universe -- a user-show carrying both seasons contributes TWO rows and ONE pair |
| `distinct_show_IDs_APPEARING_IN_A_D9_COVERAGE_ROW` | 45,014 | show IDs that appear in at least one coverage row -- i.e. that some user in the sweep has an S1 or S2 record on |
| `distinct_SLUGGED_SHOW_IDS_IN_THE_PARSED_SWEEP_the_U1_universe` | 46,428 | one row per show ID seen anywhere in processed/step4/parsed/ carrying a `show_slug` field -- the U1 universe decisions/0088 Sec 3 rules the clustering runs over |

**On the mislabel `0088` §2(a) corrects.** The pivot-side count — show IDs appearing in at least one D9 coverage row, **45,014** here — **is not the sweep**, and this arm labels it for what it is. This arm's slugged sweep set, the **U1** universe the clustering runs over, is a **different object**: **46,428** show IDs, of which 0 carry an empty slug string, built from `processed/step4/parsed/`. **`0088` §2(c): where the arms' universes differ they are two objects and are named as two — a shared label over two sets is the defect; the sets themselves may both be right.**

**And the season-coverage row count is not comparable without its mask.** This arm's **1,007,729** is over the **D11-filtered S1/S2 episode records only**. A row count taken over all seasons, or before D11, is a third object again — which is the whole point of naming it.

**D11 at this site** (`0088` §1(b)): 756 records excluded of 12,323,972 in the site's input universe; latest `watched_at` used **2026-08-10T23:59:00**; assertion holds: **True**.

### **D9 publishes as a BOUND** (`0090`) — strict is the floor, loose is the ceiling, **neither is the point estimate**

**D9 PUBLISHES AS A BOUND. STRICT IS THE FLOOR, LOOSE IS THE CEILING, both labelled, and NEITHER IS THE POINT ESTIMATE. Neither endpoint may be quoted as 'D9's result'.** ***SUPERSEDED: decisions/0074 ruling 5's framing, 'USE THE STRICT KEY AND REPORT THE LOOSE COUNT ALONGSIDE', under which STRICT WAS THE ANSWER and loose was context. The keys themselves are unchanged (0076 Sec 3).*** **The ground:** 0074 ruling 5's own reason carried through: the loose count publishes BECAUSE IT BOUNDS HOW WRONG STRICT COULD BE, and a quantity published to bound another is an ENDPOINT, not a footnote. 0078 Sec 3 already ran this argument once, to extend loose to half (b). **It applies to every D9 quantity with both forms** — complementary signature pairs, half (a) and half (b) -- applying it to one and not the others is the defect 0078 Sec 3 corrected.

| D9 quantity | **BOUND `[strict, loose]`** | Floor (STRICT) | Ceiling (LOOSE) | Point estimate |
| :--- | :---: | ---: | ---: | :--- |
| complementary signature pairs | **`[0, 75]`** | 0 | 75 | **none — `0090`** |
| half (a) fabricated never-started rows, APPLY_position5 | **`[0, 6]`** | 0 | 6 | **none — `0090`** |
| half (b) B-side pairs present in position 3's retained drop set | **`[0, 27]`** | 0 | 27 | **none — `0090`** |

**Direction is part of the label and it is not symmetric.** STRICT is the FLOOR: it matches only slugs identical modulo punctuation, so it cannot over-count. LOOSE is the CEILING: year-stripping merges remakes and national versions, so it cannot under-count. The error runs OPPOSITE to D9's own lower-bound caveat.

**A zero floor is not an absence of evidence.** Decisions/0090 -- a zero floor is not an absence of evidence. 0 is a MEASURED floor on a stated coverage, and a bound whose floor is 0 with the coverage unstated is indistinguishable from a check that looked nowhere. **The coverage beside the floor, on this build:** **726,103** candidate `(user, show)` pairs examined across **45,014** distinct show IDs, on **12,323,216** S1/S2 records surviving D11 — the WHOLE PULLED SWEEP, not the frame -- a split puts S1 under one show ID and S2 under another and only one of the two need be in the frame.

**A trailing digit group of arbitrary length reduces `the-100` to `the`. Its count is a DIFFERENT KEY'S ANSWER, reported as a divergence and never as the ceiling (0090, 0076, 0078 Sec 3).** On this build it gives **76**.

**0090 Sec 4 -- D9's own numbers do not change. What changes is which of them is presented as the answer, and this arm's r4 build presented strict as the ruled key.**

### The keys, which are now defined in the spec

**`0076` §3 defined both keys**, because "strict" and "loose" had existed only inside one instance's code and were undefined on every surface an isolated instance reads. ~~**`0074` ruling 5 ruled STRICT**~~ — ***that framing is SUPERSEDED by `0090`: strict is the floor of a published bound, not the answer. The keys themselves are unchanged.***

| Key | Definition | Complementary signature pairs |
| :--- | :--- | ---: |
| `STRICT` | re.sub(r"[^a-z0-9]", "", slug.lower()) -- strip nothing else | 0 |
| `LOOSE` | remove a trailing four-digit year, then apply STRICT | 75 |
| `LOOSE_variant_any_trailing_4_digits` | 'four-digit year' read as ANY trailing four-digit group | 75 |
| `THIRD_KEY_NOT_USED` | a trailing digit group of ARBITRARY length -- reduces `the-100` to `the` | 76 |

**The two admissible readings of "a trailing four-digit year" agree on this data** — restricting the four digits to `19xx`/`20xx` and not restricting them both give 75. **The third key — a trailing digit group of arbitrary length, which reduces `the-100` to `the` — gives 76 here.** That is not a key of this study; it is measured so that the divergence `0076` describes is visible on this instance's own data rather than only in the decision log.

### Half (a) — fabricated never-started rows

| Population / position | Never started | **BOUND `[floor, ceiling]`** | floor STRICT | ceiling LOOSE | Bound as a share |
| :--- | ---: | :---: | ---: | ---: | :---: |
| APPLY_position5 | 33,373 | **`[0, 6]`** | 0 | 6 | `[0.0000%, 0.0180%]` |
| APPLY_position6_post_liveness | 32,769 | **`[0, 6]`** | 0 | 6 | `[0.0000%, 0.0183%]` |
| DERIV_position5 | 9,145 | **`[0, 0]`** | 0 | 0 | `[0.0000%, 0.0000%]` |
| DERIV_position6_post_liveness | 9,145 | **`[0, 0]`** | 0 | 0 | `[0.0000%, 0.0000%]` |

**No point estimate on any row** (`0090`). The interval is the result.

### Half (b) — the silently deleted S1-failing counterparts

**Measured on position 3's drop set** (`0075` ruling 2), which this run writes as a deliverable. These pairs carry S2 evidence and no S1 evidence, so they fail the S1 completion rule and never enter the analysis population at all. They are unreported unless counted here, and they are the counterpart of the fabricated never-started rows half (a) counts.

| | **BOUND `[floor, ceiling]`** | floor STRICT | ceiling LOOSE |
| :--- | :---: | ---: | ---: |
| B-side pairs on frame shows | **`[0, 27]`** | 0 | 27 |
| of those, present in the position-3 drop set | **`[0, 27]`** | 0 | 27 |
| of those, in the S2-evidence-and-no-S1-evidence subset | **`[0, 27]`** | 0 | 27 |

**`0078` §3 put both keys on this half; `0090` makes the pair an interval rather than an answer with a footnote.** **No point estimate on any row.**

Every one of the 27 loose-key B-side pairs is accounted for inside the drop set — **which is the check that the side output is the right population and not merely a convenient one.** **The strict zero is a computed zero on a present input, not a zero returned by a missing one**, which is the distinction `0079` §1 exists to preserve.

**The STRICT key finds ZERO complementary pairs: no two distinct show IDs in this sweep carry the same slug modulo punctuation. The entire D9 signal therefore comes from year-stripping, which CANNOT distinguish a Trakt metadata split from a REMAKE or a national version sharing a title.**

### 10a. The clustering universe — **U1, ruled, ranked by distinct strict keys merged**

**`0088` §3 RULES IT.** *The D9 clustering universe is **U1** — every distinct show ID appearing anywhere in the pulled sweep that carries a slug, deduplicated to one row per show ID — **ranked by DISTINCT STRICT KEYS MERGED**, i.e. how many separate metadata entries the loose key collapsed into one.* **NOT U2 (the 1,138 frame shows) and NOT U3 (the 75 D9 candidate pairs).** The ground is `0088`'s: the artifact D9 hunts is a history **splitting across two metadata entries**, and that can occur **anywhere in a history, not only among shows that survived the frame filters** — a frame-restricted universe finds only splits where **both sides made the cut**, and **a bound computed on a narrow slice bounds very little**.

**THIS ARM PUBLISHES `U1_all_sweep_show_ids_carrying_a_slug`, ranked on the ruled basis.** The r3 build published U3, the D9 candidate complementary pairs, on the ground that the loose key's warrant concerns exactly the pairs the two keys disagree about. 0088 Sec 3 rules otherwise and gives the reason: the artifact D9 hunts is a history splitting across two metadata entries, and THAT CAN OCCUR ANYWHERE IN A HISTORY, not only among shows that survived the frame filters -- a narrow universe finds only splits where both sides made the cut, and a bound computed on a narrow slice bounds very little. NO COUNT MOVES WITH IT: the strict and loose complementary-pair counts are unchanged, because D9's SEARCH already ran on the whole sweep in this arm. What moves is which clusters are ILLUSTRATED

| Universe | Unit | Members examined | Distinct loose keys | Max cluster | Largest clusters |
| :--- | :--- | ---: | ---: | ---: | :--- |
| `U1_all_sweep_show_ids_carrying_a_slug` **(PUBLISHED)** | distinct show IDs sharing one LOOSE key | 46,428 | 44,142 | 8 | `secondchance` (8), `theisland` (7), `blackout` (6), `hunted` (6), `maigret` (6), `missing` (6), `thefamily` (6), `yourhonor` (6) |
| `U2_the_frame_shows` | distinct show IDs sharing one LOOSE key | 1,138 | 1,123 | 2 | `charmed` (2), `doctorwho` (2), `frasier` (2), `ghosts` (2), `gossipgirl` (2), `kingdom` (2), `macgyver` (2), `manhunt` (2) |
| `U3_D9_candidate_complementary_pairs` | complementary signature ROWS (user, S1-side show, S2-side show) sharing one LOOSE key -- NOT distinct show IDs | 75 | 48 | 10 | `thetwilightzone` (10), `thetraitors` (7), `manhunt` (5), `thedevilyouknow` (2), `unsolvedmysteries` (2), `coldcasefiles` (2), `thetomandjerryshow` (2), `thesewoodsarehaunted` (2) |

**The basis needed ruling because it reorders the list on its own.** Same universe, same key, two bases:

| Ranking basis | Largest clusters |
| :--- | :--- |
| **distinct STRICT keys merged (RULED)** | `secondchance` (8), `theisland` (7), `blackout` (6), `hunted` (6), `maigret` (6), `missing` (6), `thefamily` (6), `yourhonor` (6) |
| distinct show IDs (not ruled) | `secondchance` (8), `blackout` (7), `theisland` (7), `hunted` (6), `maigret` (6), `missing` (6), `thefamily` (6), `yourhonor` (6) |

**REPORTED, NOT RECONCILED — the ruling fixes the BASIS and not the TIE-BREAK, and the tie is occupied.** `0088` §3 names the U1 top three as `secondchance` (8), `theisland` (7), `maigret` (6). **The first two are unique at their counts and this build reproduces them exactly.** The third is inside a **6-way tie at 6** — `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` — so **which name appears third is decided by a rule no surface states**. Under this arm's tie-break (ascending key, applied after descending count) it is **`blackout`**; `maigret` is equally correct under a different one. **This is a spec gap inside the ruling that closed the previous spec gap, and it is reported rather than resolved by picking the name that matches the entry.**

**U1 and U2 count DISTINCT SHOW IDS per key; U3 counts complementary signature ROWS per key. A cluster size from one is not comparable to a cluster size from another, which is a second reason the universe has to be named rather than the number quoted.** Coverage: Three universes measured, none of them an empty look: 46,428 slugged sweep show IDs, 1,138 frame shows, 75 candidate complementary pairs.

**What naming the universe located.** BOTH cluster lists decisions/0085 Sec 2 quotes are reproduced by THIS SINGLE BUILD, from two different universes. U1 (all slugged sweep show IDs), on the RULED basis of distinct strict keys merged, gives secondchance 8 and theisland 7 -- both unique at their counts -- with a maximum of 8, and a SIX-WAY TIE at 6 that contains maigret; U3 (the D9 candidate complementary pairs) gives thetwilightzone 10, thetraitors 7, manhunt 5 with a maximum of 10. Those are the two quoted lists and the two quoted maxima, with the one qualification that 0088's third U1 name sits inside a tie the ruling does not break -- see THE_TIE_BREAK_IS_NOT_RULED. **The divergence was located ON THE UNIVERSE AXIS and not in the counting -- consistent with 0085's own observation that every count around the lists reconciled. Neither arm miscounted, and 0088 Sec 3 then ruled the universe so both arms cluster one defined object.** Maxima reproduced on this build: **U1 = 8**, **U3 = 10** — `0085` §2's *"maxima 8 against 10"*, both from one run. 0088 Sec 3 also rules the RANKING BASIS, because it reorders the list on its own: U1 ranked by distinct SHOW IDS instead of distinct STRICT KEYS displaces maigret with blackout. Both rankings are emitted under each show-ID universe. Source of the quoted lists: decisions/0085 Sec 2, 0088 Sec 3 and task-sheet.md Step 8's D9 bullet -- spec surfaces this instance is required to read. No other arm's output folder was read.

**The r3 build published U3's list -- thetwilightzone 10, thetraitors 7, manhunt 5 -- which is also task-sheet.md's former illustration. SUPERSEDED as the example by 0088 Sec 3. Those names are not wrong; they are another universe's answer, and both lists are still emitted side by side in the universe table.**

**No count moves with the ruling.** D9's **search** already ran on the whole sweep in this arm — 726,103 candidate pairs — so the strict and loose complementary-pair counts are unchanged at **0** and **75**. What the ruling fixes is **which clusters are illustrated**, which is the evidence for the loose key's only warrant.

**Why the interval publishes rather than a point estimate:** The loose count BOUNDS HOW WRONG STRICT COULD BE, and the error runs OPPOSITE to D9's own lower-bound caveat: D9 warns that its count misses splits, while the loose key catches non-splits. Both directions are live and neither number is a measured split rate. **Neither endpoint is the answer** (`0090`): strict is the **floor**, loose is the **ceiling**. ***Corrected this run (Red Team seventh pass, finding 1, second half): `-r4` rendered this line as "Why the loose count publishes EVEN THOUGH STRICT IS RULED" — `0074` ruling 5's framing, which `0090` supersedes — and it sat well below the line in §10 that strikes exactly that framing. Same file, same class of defect as the assertion-set count: the replacement above, the superseded text below.***

Direction: half (a) INFLATES Never started; half (b) removes a pair that should have been in the population. Step 9 bounds D9 and publishes it ALONGSIDE, never folded in.

## 11. D4 — S3 without S2

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

Pairs scored Never started that carry S3-or-later episode records on that show and **no S2 episode record at all**. Emitted here because Step 8 holds the episode-level evidence and Step 9 does not (`0070` ruling 7). Direction: **inflates** Never started; Step 9 bounds it and publishes it **alongside**, never folded in.

| Population / position | Never started | S3-without-S2 | Share |
| :--- | ---: | ---: | ---: |
| APPLY_position5 | 33,373 | 428 | 1.2825% |
| APPLY_position6_post_liveness | 32,769 | 426 | 1.3000% |
| DERIV_position5 | 9,145 | 0 | 0.0000% |
| DERIV_position6_post_liveness | 9,145 | 0 | 0.0000% |

**The DERIV zero is structural, not a measurement of nothing**: DERIV requires S2 evidence, and a D4 pair has none by definition.

## 12. D12 — per-bucket show and pair counts, all five buckets

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

| Bucket | Shows | Pairs, position 4 | Pairs, APPLY position 5 | Pairs, DERIV position 5 |
| :--- | ---: | ---: | ---: | ---: |
| C0 | 0 | 0 | 0 | 0 |
| C1 | 206 | 41,246 | 40,365 | 29,493 |
| C2 | 340 | 60,532 | 58,811 | 44,500 |
| C3 | 167 | 28,398 | 27,573 | 20,783 |
| C4 | 425 | 71,724 | 69,905 | 52,594 |

**Shows within 1 day of a bucket boundary: 7** of 1,138 examined. **C0 = 0 of 1,138 shows examined** — a measured zero, not an unexamined one.

## 13. Metadata-disagreement counts

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

| Flag | Shows | Pairs at position 4 |
| :--- | ---: | ---: |
| `s1_count_disagreement` | 0 | 0 |
| `s2_count_disagreement` | 0 | 0 |
| `s1_aired_lt_listed` | 0 | 0 |
| `s2_aired_lt_listed` | 0 | 0 |

**Every flag is 0 of 1,138 shows EXAMINED, not 0 because nothing was looked at.**

Direction, named as required: a listed-but-unaired S2 episode raises L2, which tightens ceil(0.90 x L2) and pushes real completers out of Continued into Started-and-left -- it OVERSTATES abandonment; where F2 never aired, Continued is unreachable on that show.

## 14. `pull_date`, fetch window, and discarded records

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

- `pull_date` = **2026-08-11**, `tau_pull` = **2026-08-11T00:00:00Z**
- Earliest per-user fetch: **2026-08-11T05:01:26.447766+00:00**
- Latest per-user fetch: **2026-08-11T23:10:31.236946+00:00**
- Records discarded for `watched_at >= tau_pull`: **1,734**, of which **167** are in-frame S1/S2 episode records

The discarded tail is about one day of activity for early-fetched users and about two for late-fetched ones; it is not evenly distributed.

### The D11 open question, measured rather than assumed

`0068` rules line 1 at **220,107 as published** and records separately as **OPEN** whether D11 moves it. Measured here: applying D11 to the S1 completion walk as well gives **220,103**, a difference of **4** pairs. **All 4 are removed at position 5 under either reading** — checked row by row, not argued — because their first-pass completion instant is at or after `tau_pull`, so `T0` is at or after 2026-08-10 and D10 removes them. **Lines 4 through 7 and every published figure are identical under both readings; only lines 1, 2 and 3 move.** The table column `s1_completion_used_a_post_cutoff_record` is what carries this question downstream.

**Both halves of `0083` §1's statement are measured here, not quoted.** Reading C **removes 4 pairs** from the completer set and **adds 0**; of the 220,103 pairs common to both readings, **0 have a first-pass completion date that moves.** The second half matters on its own: the count alone would not establish that no *surviving* pair's clock start changes, and a moved clock start is what would push the difference past lines 1–3 into the published figures.

## 14a. B3 — the two unasserted mandates, **measured, not self-reported**

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**`0088` §1.** Decisions/0088 Sec 1 -- MEASURE BOTH. The mandates are THE HALF-OPEN UTC-INSTANT FORM and D11-AS-GLOBAL-CUTOFF, not invariants 7 and 8. Both arms' compliance is TRUE and was independently confirmed; what was missing is any measurement of whether either is LOAD-BEARING on this data. **The ground:** the unstated version of exactly this scope produced Step 7's 792-against-791, where one arm applied the restriction and the other did not.

### (a) The boundary window — **the SEPARATING interval, corrected by `0089` §2(a)**

The rows on which the half-open form and a date-level form DIFFER -- S2 evidence in the SEPARATING interval [tau, tau + 24h) at both bounds -- and, on those rows, how many change OUTCOME STATE when the forbidden form is actually applied. The cells decisions/0088 Sec 1(a) named, [tau - 24h, tau) and exactly-at-tau, are reported alongside. **No .date(), dt.date, normalize() or day-flooring anywhere in this arm's step8_b_*.py; instants are int64 seconds throughout. THAT IS THE SELF-REPORT AND IT IS NOT THE MEASUREMENT.**

**THE INTERVAL WAS WRONG ON THIS ARM'S PREVIOUS BUILD, AND SO WAS THE VERDICT TAKEN OFF IT.** Decisions/0089 Sec 2(a). 0088 Sec 1(a) named [tau - 24h, tau). T0 is day-floored, so tau1 and tau2 are MIDNIGHT-ALIGNED and `date(ts) < date(tau)` is identical to `ts < tau` below the boundary -- THAT WINDOW IS WHERE THE TWO FORMS AGREE. The separating interval is [tau, tau + 24h). This arm's r4 build emitted the ruled window and the single instant exactly at tau and nothing else, and took its verdict off 1 row of the separating interval.

| Population | Unit | **`[τ1, τ1+24h)` SEPARATING** | **`[τ2, τ2+24h)` SEPARATING** | `[τ1−24h, τ1)` agreeing | `[τ2−24h, τ2)` agreeing | at `τ1` | at `τ2` | Examined |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY_position5 | distinct S2 episodes (what `|A|` counts) | **703** | **303** | 749 | 291 | 1 | 0 | 2,023,274 |
| APPLY_position5 | raw in-E2 S2 records | **1,042** | **428** | 951 | 359 | 1 | 0 | 2,444,815 |
| DERIV_position5 | distinct S2 episodes (what `|A|` counts) | **595** | **261** | 676 | 254 | 1 | 0 | 1,668,088 |
| DERIV_position5 | raw in-E2 S2 records | **883** | **385** | 875 | 318 | 1 | 0 | 2,034,990 |

- **APPLY_position5, the STRICT silence test's own boundary** — max insertion instant in `[τ1−24h, τ1)`: **7**; exactly at `τ1`: **0**, on 196,654 rows. **A different axis from the one above** — the silence test is STRICT (0068) -- an instant exactly AT tau1 does not make the account live -- so the rows exactly at tau1 are the rows on which strict and non-strict readings of the RULE differ, as opposed to the rows on which half-open and date-level readings of the CLOCK differ.
- **DERIV_position5, the STRICT silence test's own boundary** — max insertion instant in `[τ1−24h, τ1)`: **6**; exactly at `τ1`: **0**, on 147,370 rows. **A different axis from the one above** — the silence test is STRICT (0068) -- an instant exactly AT tau1 does not make the account live -- so the rows exactly at tau1 are the rows on which strict and non-strict readings of the RULE differ, as opposed to the rows on which half-open and date-level readings of the CLOCK differ.

#### The four numbers that settle B3 — **rows changing OUTCOME STATE**

Rows changing OUTCOME STATE under the forbidden date-level form, both bounds x both populations, on the position-5 row set. **The forbidden form is computed only here,** as a counterfactual whose only output is a count. The emitted table, every waterfall line, every share and every other figure in this deliverable are the half-open UTC-instant form. The counterfactual asserts that its own half-open baseline reproduces the pipeline's states exactly before it diffs anything.

| Population | `τ1` relaxed | `τ2` relaxed | **both — the full forbidden form** | Rows |
| :--- | ---: | ---: | ---: | ---: |
| APPLY_position5 | **52** | **19** | **71** | 196,654 |
| DERIV_position5 | **45** | **14** | **59** | 147,370 |

- **APPLY_position5 transitions under the full forbidden form:** **never_started -> continued** 36, **never_started -> started_and_left** 16, **started_and_left -> continued** 19. Rows holding an S2 episode in the separating interval: **311** at `τ1` and **136** at `τ2` — more rows than change state, because most already have `|A| ≥ 1` or already fail the Continued test.
- **DERIV_position5 transitions under the full forbidden form:** **never_started -> continued** 31, **never_started -> started_and_left** 14, **started_and_left -> continued** 14. Rows holding an S2 episode in the separating interval: **275** at `τ1` and **117** at `τ2` — more rows than change state, because most already have `|A| ≥ 1` or already fail the Continued test.

- **APPLY_position5 — the two per-bound counts sum to the joint one on this data: 52 + 19 = 71 — True.** **Measured, not assumed.** They need not: a row moved out of never-started by the `τ1` relaxation could be moved again by the `τ2` one, and that row would be counted once in the joint form and twice in the sum. **No row does both here**, which is why the joint count is reported as its own number rather than left to be added.
- **DERIV_position5 — the two per-bound counts sum to the joint one on this data: 45 + 14 = 59 — True.** **Measured, not assumed.** They need not: a row moved out of never-started by the `τ1` relaxation could be moved again by the `τ2` one, and that row would be counted once in the joint form and twice in the sum. **No row does both here**, which is why the joint count is reported as its own number rather than left to be added.

- **APPLY_position5 — `OUTCOME_DECIDING`.** OCCUPIED AND OUTCOME-DECIDING -- the separating interval is non-empty AND the two forms disagree on the OUTCOME STATE of 71 row(s) of 196,654. The mandate is load-bearing and it is load-bearing ON THE RESULT, not only on |A|.
- **DERIV_position5 — `OUTCOME_DECIDING`.** OCCUPIED AND OUTCOME-DECIDING -- the separating interval is non-empty AND the two forms disagree on the OUTCOME STATE of 59 row(s) of 147,370. The mandate is load-bearing and it is load-bearing ON THE RESULT, not only on |A|.

**THE MANDATE IS LOAD-BEARING ON THE RESULT, AND THAT IS THE FINDING.** `0088` §1(a) instructs that a zero be **labelled vacuous rather than passed silently**. It is not zero, and it is not inert either: the forbidden `date(watched_at) <= T1` form would move **71 rows on APPLY** and **59 on DERIV** into a different outcome state. **Three states, not two:** an empty separating interval, an occupied one that decides no outcome, and an occupied one that decides one. **This build is the third**, and this arm's previous build published the second — because it measured the interval on which the two forms *agree* plus the single instant at `τ1`, and read a verdict about disagreement off it. **That is corrected here, not carried.**

**Reconciled with what the decision log records of the other arm, without reading its output.** `0089` §2(a) quotes 703 episodes on 311 rows at `τ1` and 303 on 136 at `τ2` on APPLY, 595/275 and 261/117 on DERIV. **This build measures the same six numbers** — the table and the bullets above. **Those figures were taken from `decisions/0089`, a spec surface this instance is required to read, not from the other arm's folder.** **The outcome-state counts are new: `0089` §2(a) records them as measured by neither arm.**

### (b) The per-site D11 table — **asserted at each site, not once and about the rest**

Records excluded by D11 at EACH site separately, asserted at each site rather than once and about the rest. **13 sites; D11 applied at 12, of which 2 examined ZERO records and their passes are VACUOUS.**

| Site | D11 applied | **Records EXAMINED** | Records excluded | Unit | Assertion holds |
| :--- | :---: | ---: | ---: | :--- | :--- |
| `A (\|A\| at tau1)` | yes | 2,489,729 | 94 | in-E2 S2 records | **yes** |
| `A_H (\|A_H\| at tau2)` | yes | 2,489,729 | 94 | in-E2 S2 records | **yes** |
| `action_count_s1_watch` | yes | 2,716,991 | 49 | in-E S1/S2 records | **yes** |
| `action_count_s1_checkin` | yes | 153,245 | 1 | in-E S1/S2 records | **yes** |
| `action_count_s1_scrobble` | yes | 383,811 | 23 | in-E S1/S2 records | **yes** |
| `action_count_s1_other` | yes | 0 | 0 | in-E S1/S2 records | **VACUOUS — 0 examined** |
| `action_count_s2_watch` | yes | 2,364,902 | 52 | in-E S1/S2 records | **yes** |
| `action_count_s2_checkin` | yes | 120,989 | 4 | in-E S1/S2 records | **yes** |
| `action_count_s2_scrobble` | yes | 325,599 | 38 | in-E S1/S2 records | **yes** |
| `action_count_s2_other` | yes | 0 | 0 | in-E S1/S2 records | **VACUOUS — 0 examined** |
| `liveness evidence (per-account maximum insertion instant)` | yes | 27,656,813 | 1,734 | records of any kind, whole sweep | **yes** |
| `D9 coverage rows` | yes | 12,323,972 | 756 | S1/S2 episode records, ALL shows in the sweep, not only frame shows | **yes** |
| `S1 completion walk` | **no** | 2,860,465 | 60 | distinct in-E1 S1 episodes at their canonical instant | **NO — by design, see below** |

**Every row carries a boolean assertion and an examined count** — 13 of 13 and 13 of 13. **CLAUDE.md -- a check that finds nothing because it looked nowhere must FAIL, not pass, and every path that can return 'nothing found' states whether it found nothing or looked at nothing. The examined count was printed at every site on the previous build; what was missing is (i) any assertion at the D9 site and (ii) any marking that a pass on an EMPTY site is vacuous.**

***Corrected this run.*** **The `D9 coverage rows` row published `null` for BOTH its exclusion count and its assertion in `-r5`'s `results.json`**, while the site was counted among the twelve where D11 is applied — **a row listed as asserted and carrying no assertion.** The number was in `d9.json` the whole time, and the `.md` filled it *in the renderer*, so the two halves of one deliverable disagreed and only the JSON reader could see it. **The backfill is now a pipeline step (stage 3), asserted at the site**, and the renderer patches nothing.

***And a pass on an empty site is now labelled VACUOUS rather than printed as a pass.*** `action_count_s1_other`, `action_count_s2_other` examined **0** records, so their assertions are true of the empty set and are **not evidence that D11 is applied there**. The examined count was printed on the previous build — that half of the rule was met — but `assertion_holds: true` read identically at a site with 2.7 million records and at a site with none. **A check that finds nothing because it looked nowhere must fail, not pass** (`CLAUDE.md`; `0088` §1(a) says the same of the boundary window).

**The `Records excluded` column is NOT summable and its rows are NOT disjoint.** `records_excluded_by_D11` is carried in FOUR DIFFERENT UNITS across these rows, and the rows overlap. Adding the column produces a number that counts nothing. Named here because one label over quantities in different units is exactly the defect decisions/0088 Sec 2(b) ruled on, and a table is where it hides best. **Units present:** *S1/S2 episode records, ALL shows in the sweep*; *distinct in-E1 S1 episodes at their canonical instant*; *in-E S1/S2 records*; *in-E2 S2 records*; *records of any kind, whole sweep*. **Overlaps:** `A` and `A_H` report the SAME 94 records -- one evidence array read at two instants -- and those same 94 are also the sum of the four `action_count_s2_*` rows. The `liveness evidence` row is records of ANY kind across the WHOLE sweep, a superset. The `D9 coverage rows` row is over ALL shows in the sweep, not only frame shows. The `S1 completion walk` row is in DISTINCT EPISODES at their canonical instant, not records.

**The two figures that DO sum, asserted:** the four action_count_s1_* rows sum to 73 and the four action_count_s2_* rows sum to 94; 73 + 94 = 167, which is in_frame_S1_S2_records_at_or_after_tau_pull. That identity is arithmetic on measured counts and is asserted below — S1 side **True**, S2 side **True**, total **True**.

**Site names are this arm's own and are not a ruled vocabulary — reported, not reconciled.** decisions/0088 Sec 1(b) NAMES the sites in prose -- A, A_H, the four action_count_s{1,2}_*, the liveness evidence, D9's coverage rows, the S1 walk -- but fixes no key spelling, and it names EIGHT while the four action_count columns are EIGHT sites here, not four, because the spec's own column enumeration (0080) has eight action-count columns. This arm publishes 13 rows with prose site names. decisions/0091 Sec 3 records the other arm using `S1_completion_walk`, an underscored key, so THE TWO TABLES ARE NOT KEY-WISE DIFFABLE even where they agree numerically. Reported, not reconciled: naming is unruled, and 0088 Sec 2(c) requires two differing objects be named as two rather than merged under a shared label.

**The one site where D11 is not applied is the S1 completion walk**, and the `no` there is the **correct reported state, not a failure**: `0068` rules waterfall line 1 at **220,107 as published**, that value needs the pairs whose first-pass completion rests on a post-cutoff record, and whether D11 applies to the walk is `0068`'s own **open** item. Three different objects sit behind it and are named separately — **73 records**, **72 distinct episodes**, **60 episodes whose *canonical* instant is post-cutoff**.

**THIS RUN CHANGES SOMETHING, AND THE PER-SITE ASSERTION IS WHAT EXPOSED IT.** YES, and it is reported rather than reconciled. The r3 build computed the eight action counts on `m12`, which carries the S1 side past tau_pull so that decisions/0068's published line 1 of 220,107 survives. That carry-through has a ruling behind it FOR THE COMPLETION WALK and none for the action counts. decisions/0088 Sec 1(b)'s per-site assertion is what made the difference visible: asserted at each site, the four action_count_s1_* sites would have FAILED on r3. **Size of the change:** 44 pairs in the record universe, of which **4 are in the APPLY position-5 row set** and 4 in DERIV's; columns affected: `action_count_s1_watch`, `action_count_s1_checkin`, `action_count_s1_scrobble`. The action counts are read by nothing upstream of themselves -- not by |A|, |A_H|, T0, the outcome assignment or the liveness rule -- so no waterfall line, no outcome share and no invariant moves with them — **line 1 is 220,107 and position 5 is 196,654 on this build, unchanged.**

### (c) The promoted assertion — published, labelled **CODE CHECK**

**`no position-5 row has tau2 > tau_pull`.** Decisions/0088 Sec 1(c) -- it already ran inside the pipeline but sat OUTSIDE the published invariant set, so no reader of the deliverable could see it. Published, labelled CODE CHECK. It is **invariant 9** in `artifacts/step8-invariants-b.md`.

| Population | Rows examined | `tau2 > tau_pull` | `tau2` **exactly at** `tau_pull` | Latest `tau2` |
| :--- | ---: | ---: | ---: | :--- |
| APPLY_position5 | 196,654 | 0 | 20 | 2026-08-11T00:00:00 |
| DERIV_position5 | 147,370 | 0 | 17 | 2026-08-11T00:00:00 |

**Rows sit with tau2 EXACTLY at tau_pull, so the assertion is tight rather than comfortably satisfied -- a `>=` form of the same assertion would FAIL on this data. Stated because a passing assertion with slack and a passing assertion at the bound are not the same evidence.**

## 15. Outcome states, channel pairs, and the scope qualifier

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

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

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**`0080` §1 enumerates the column set rather than counting it, `0081` extends it to 88 and `0082` to 89.** This instance emits **89**, exact-match to the enumerated list: **True**, and in the enumerated order. The full list is in `artifacts/step8-waterfall-b.json` → `analysis_table.column_names`. **Converged is not specified**, and Step 8b's schema is built on this vocabulary, so it is fixed before the schema exists.

**Changed from this arm's last confirmed run: nothing.** `0083` does not move the column set — it restates what `p_at_bound` *means* (§18), which selects the identical rows. **The two free drops stand** — `f2_in_A_H` is derivable as `max_episode_in_A_H == s2_F`, and `max_episode_in_A` is read by nothing downstream. The 87-name build is two builds back and is named here so it is not read as current.

**The two residuals `0083` §3 fixed — RE-READ OFF DISK, not assumed.** A correction read back is verified; a correction quoted from the entry that made it is not.

| Residual | `task-sheet.md` | this arm's definition file |
| :--- | :--- | :--- |
| (a) the strike-through now names the **89**-name enumeration as its replacement | **True** | **True** |
| (b) `f2_in_A_H` is marked **dropped at the point of use** in `0077`'s adopted-name table | **True** | **True** |
| (b′) `0077`'s **spelling** ruling (`A_H`, not `AH`) survives the column's removal | **True** | **True** |

**And the enumeration is checked as a SET, not by counting** — `task-sheet.md` 89 names, this arm's definition file 89, this pipeline 89; spec == code **True**, definition file == code **True**, and the two surfaces agree with each other **True**. **Matching a count is not matching a set.**

**And the two SURFACE CLAIMS this arm published last run are re-read, not carried.** These are claims about the STATE OF OTHER FILES. They were true when this arm published them on 2026-08-16-r4 and decisions/0089 Sec 3 acted on both. Re-read live here; a surface claim carried as prose is a measurement with an expiry date.

| Claim published on `-r4` | Measured now | Status |
| :--- | :--- | :--- |
| *"`specs/step8-readback.md` still says Step 8 has not launched"* | string occurs **2**× — **1** inside the status stamp that supersedes it, **1** in the body; the stamp precedes every body occurrence: **True** | CLOSED AS A DEFECT, STANDING AS A QUESTION. decisions/0089 Sec 3 stamped the file, and the stamp precedes every body occurrence and marks the string SUPERSEDED. The r4 claim -- that the string sits there unqualified -- is NO LONGER TRUE and is not republished. The body sentence itself is deliberately unedited, because the stamp is NEGATIVE ONLY. What remains open is not the string but whether specs/ becomes a NINTH propagation surface, which 0089 Sec 4 carries for the Human Lead |
| *"both spec surfaces still read THE ASSERTION SET NOW HAS EIGHT MEMBERS"* | `task-sheet.md` EIGHT **0** / NINE **0**; definition file EIGHT **0** / NINE **1**; *"four pure code checks"* marked SUPERSEDED at the point of use: **True** | CLOSED. decisions/0089 Sec 3 acted on both halves and struck the 'four pure code checks' sentence at the point of use. NO SURFACE NOW STATES EIGHT. The r4 claim is NO LONGER TRUE and is not republished. This arm publishes NINE and no surface contradicts it |

**Reported per surface, not as a total** — task-sheet.md now states NO count of the assertion set in this phrasing, and the definition file states NINE. NO SURFACE CONTRADICTS ANOTHER, which is what the r4 claim said they did. Reported per surface rather than as a total, because a total of zero EIGHTs is also what two silent files would give.

**Coverage, so a zero is a zero found and not a file unopened** (`CLAUDE.md`): `specs/step8-readback.md` **4,342** bytes, `task-sheet.md` **143,808**, this arm's definition file **50,837**. **The negative grep for 'EIGHT MEMBERS' passes clean on a file that never said nine. Both halves are measured here: EIGHT must be 0 AND NINE must be non-zero.**

**`silent_at_tau1` is the column that was worth restoring, and the reason is not symmetry.** It is **not recoverable from `live` and `outcome` on Continued rows** — `live` is true for every Continued pair *regardless of silence*, because the rule's second conjunct is `NOT Continued`. Without it, **the Continued-and-silent count cannot be recomputed from Step 8's table**; §20 below reports that count as an aggregate as well, so the figure survives independently of the column.

## 18. `p_at_bound` — it marks WHETHER `p` reached its bound, not WHY

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**`0083` §2 restates the column and this instance emits the restated form.** `p_at_bound` is **TRUE where `p` reached its bound**, **null where `p` is null**. **It does not say why, because on the adopted form there is only one why.**

***SUPERSEDED — `0082` §2's definition by two mechanisms:*** *"TRUE where the rank numerator saturated at `L2`, FALSE where the pair left at the final episode."* **Those clauses are coextensive by construction and the FALSE class is empty.** The proof is one line of the adopted form: `p = |{e ∈ E2 : e ≤ m_H}| / L2`, and the set-membership drop rule puts `m_H ∈ E2`, so the numerator equals `L2` **iff** no listed episode exceeds `m_H`, **iff** `m_H = max(E2) = F2` — which *is* "left at the final episode." **Neither clause can hold without the other.**

***THE CHAIN HAS THREE LINKS AND ONLY THE FIRST IS CONSTRUCTION*** — `0085` §4, Red Team P4. `0083` §2 named **two** causes for a future FALSE row; **there are three.**

| Link | Status | Measured |
| :--- | :--- | :--- |
| `numerator = L2` ⟺ `m_H = max(E2)` | **CONSTRUCTION**, given `L2 := |E2|`, which the spec fixes | shows where `L2 ≠ |E2|`: **0** |
| `max(E2) = F2` | ***NOT CONSTRUCTION — DATA.*** It needs the finale to be the highest-numbered listed episode | shows where `max(E2) ≠ s2_F`: **0**; where `max(E2) ≠ L2`: **0**; `s2_aired_lt_listed`: **0** shows |

**Measured, not assumed: 0 of 1,138 frame shows separate the two** — a measured zero, not an empty look: all 1,138 frame shows were compared, max(E2) against s2_F and against s2_L. **Where a season lists an episode numbered above its finale the two would separate** — that is the `s2_aired_lt_listed` case this step is told to count, and it is **0 shows in frame.** Does it reopen across Step 13's `W` grid? No -- the frame does not move with W, so a zero here is zero at every arm.

**The three causes of a future FALSE row:**
1. the rank form is changed away from p = |{e in E2 : e <= m_H}| / L2
2. the set-membership drop rule stops putting m_H in E2
3. a frame show lists an S2 episode numbered above its finale, so max(E2) != F2 -- the third cause, added by 0085 Sec 4

**The `p = 1.0` counts, reported AS TOTALS.**

| Population / position | rows with `p = 1.0` (TOTAL) | `p_at_bound` TRUE | `p_at_bound` FALSE (`p < 1`) | `p_at_bound` null | rows account for the population |
| :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY_position5 | **1,246** | 1,246 | 17,895 | 177,513 | **True** |
| APPLY_position6_post_liveness | **1,230** | 1,230 | 17,812 | 176,909 | **True** |
| DERIV_position5 | **1,072** | 1,072 | 15,771 | 130,527 | **True** |
| DERIV_position6_post_liveness | **1,056** | 1,056 | 15,688 | 130,527 | **True** |

**The totals reproduce the ruling exactly — 1,246 at position 5 and 1,230 post-liveness on APPLY.** ***They are NOT a split.*** They are correct counts, but they are **one class counted twice, not two classes summed**, and **using them as evidence that the column separates anything is a withdrawn argument** (`CLAUDE.md`, third blindness class; registered at `src/step7_register.py` → `GROUNDS_WITHDRAWN["0083 SS2"]`). ***Also withdrawn at `0083` §2, and it is a MOTIVE rather than a figure:*** `0082` §2's claim that the spike carries two viewer-level readings the column must disambiguate. **On the adopted rank form the spike means one thing.**

**The emptiness is EMITTED, not asserted in prose** — an emptiness asserted in prose and never emitted cannot be checked. Both mechanisms are computed separately and all four cells reported, **on BOTH POPULATIONS AT BOTH POSITIONS — four cells each on four populations** (`0085` §3, Red Team blocker B2). **This is `CLAUDE.md`'s standing both-populations rule, not a new requirement.** ***One arm emitted APPLY only, and `1,056` appeared nowhere in its deliverable — while the whole ground for keeping the column is that an emptiness asserted in prose and never emitted cannot be checked. On DERIV that ground was unmet.***

| Population / position | rows examined (total) | in BOTH classes | saturated, not final | final, not saturated | in NEITHER |
| :--- | ---: | ---: | ---: | ---: | ---: |
| APPLY_position5 | 1,246 | **1,246** | 0 | 0 | 0 |
| APPLY_position6_post_liveness | 1,230 | **1,230** | 0 | 0 | 0 |
| DERIV_position5 | 1,072 | **1,072** | 0 | 0 | 0 |
| DERIV_position6_post_liveness | 1,056 | **1,056** | 0 | 0 | 0 |

**Coverage, per population, because an empty result and a clean result are the same value and only the control knows which it produced:** APPLY_position5 1,246 rows, APPLY_position6_post_liveness 1,230 rows, DERIV_position5 1,072 rows, DERIV_position6_post_liveness 1,056 rows. Populations examined: **4**. Looked nowhere: **False**.

**The ruling's stated cells, for comparison against the measured table above:** APPLY_position5 `1,246 / 0 / 0 / 0`, APPLY_post_liveness `1,230 / 0 / 0 / 0`, DERIV_position5 `1,072 / 0 / 0 / 0`, DERIV_post_liveness `1,056 / 0 / 0 / 0`.

**Which FALSE class is empty, said explicitly, because two different ones are on this page.** The empty one is `0082`'s **mechanism** class — rows *final but not saturated*, and its mirror *saturated but not final* — both **0** on every population above. The `p_at_bound` FALSE in the totals table is a different thing entirely: it is the **17,895 Started-and-left rows with `p < 1`** on APPLY at position 5, and it is large by construction. **The mechanism class stays empty through Step 13's `W` grid** — the rank form and set membership are both `W`-invariant — **so a non-zero cell anywhere means one of them has broken, and that is worth catching.**

**A second fact, measured and NOT the same argument: 0 of 1,138 frame shows have any S2 numbering gap**, so `E2 = {1…L2}` everywhere and the rank form reduces to `m_H / L2`. ***That one is DATA and could be false on another frame; the coextensivity above would still hold.*** It is stated separately because collapsing them would make a construction argument look like a frame accident.

**The column is KEPT, and the reason changes.** Not because it decomposes the spike — it does not — but because **Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the spike labelled**, and because **an emptiness asserted in prose and never emitted cannot be checked.**

## 19. `action` — counts by type, never a row-level column

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

`action` is record-level and the row is a pair, so a single value per row would assert one action per pair, which is false (`0070` ruling 4). The table carries eight count columns — `action_count_s1_watch`, `_s1_checkin`, `_s1_scrobble`, `_s1_other` and the four S2 equivalents — over the pair's in-`E` records. **The S1/S2 split is fixed by `0080`'s enumeration**, which names all eight. Step 1 already ruled that check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the logging client rather than of the viewing, so it is **not an outcome variable**. Step 13's arm reads the counts: check-in-only iff its `checkin` count is positive and `scrobble` and `watch` are zero.

## 20. Continued-and-silent — the count `silent_at_tau1` exists to preserve

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**Emitted as an aggregate as well as a column**, so the figure survives independently of either. `live` is TRUE for every Continued pair **regardless of silence**, because the liveness rule's second conjunct is `NOT Continued` — so this count is what the second conjunct is worth, and it is **the size of the outcome-conditioning at waterfall line 6**: the pairs the conjunct **saves** from exclusion.

| Population (position 5) | Continued | **Continued and silent at `tau1`** | silent at `tau1`, all rows | silent and NOT Continued = the exclusions |
| :--- | ---: | ---: | ---: | ---: |
| APPLY_position5 | 144,140 | **652** | 1,355 | 703 |
| DERIV_position5 | 121,382 | **652** | 751 | 99 |

### 20a. The line-6 marginal decomposition — **both figures, not one**

***`703` IS NOT THE MARGINAL COST OF THE SILENCE TEST*** (`0085` §5, Red Team third pass). The silence test **alone** excludes **1,355** on APPLY; the `NOT Continued` conjunct **spares 652**; `1,355 − 652 = 703`. ***One arm published 652 and not 1,355.*** **Derivable, so not a defect — but 1,355 is the figure that makes line 6 readable as a marginal cost**, and a reader holding only 652 cannot recover it without knowing to add. **Both publish, on both populations, with the identity stated.**

**Identity: `silence test alone − NOT-Continued spares = line-6 exclusions`.**

| Population (position 5) | rows examined | silence test **alone** would exclude | `NOT Continued` **spares** | **line-6 exclusions** | identity holds |
| :--- | ---: | ---: | ---: | ---: | :--- |
| APPLY_position5 | 196,654 | **1,355** | **652** | **703** | **True** |
| DERIV_position5 | 147,370 | **751** | **652** | **99** | **True** |

Coverage: both populations, every position-5 row of each; neither cell is an empty look.

**This reproduces the published 652 and the published 1,355** — 652 is the figure that closed the rule objection at `0063` §1 and publishes as a Step 14 limitation; 1,355 is what makes line 6 legible. **DERIV's Continued-and-silent count is the same 652**, because every one of those pairs carries S2 evidence by definition of Continued, so **DERIV's silence-alone figure differs from APPLY's by exactly the never-started silent pairs DERIV does not carry.**

## 21. Where two faithful instances could still differ — plus what `0083`, `0085` and `0088` closed, and the one gap `0088` opened

*Measured on: b: position-5 build of 2026-08-16-r6 (spec through 0091 + Red Team 7).*

**Three kinds of item are in this list and each says which it is.** *(a)* **Genuinely open** at the spec level — reported, never reconciled here. *(b)* **CLOSED** by `decisions/0083`, `0085` or `0088`, kept in the list because a previous build published them as live and **a closure that silently disappears from the report is indistinguishable from an item that was never raised**; each states what closed it and what was **re-measured rather than quoted**. *(c)* **NEWLY OPEN** — item 2, the **tie-break** `0088` §3 left unspecified inside the very ruling that fixed the ranking basis. **`0085` §7's B3 is no longer carried: `0088` §1 rules it and this arm has implemented all three parts** (§14a). **Items 1, 2 and 4 are reported, not reconciled**, which is the standing rule for the dual run.

1. **`0090` — D9 NOW PUBLISHES AS A BOUND, AND THIS ARM'S PREVIOUS BUILD PUBLISHED A RULED KEY.** Strict is the **floor**, loose is the **ceiling**, **neither is the point estimate**, and the interval applies to every D9 quantity that has both forms: complementary signature pairs **[0, 75]**, half (a) **[0, 6]** on APPLY position 5, half (b) **[0, 27]**. **No D9 count moves** — `0090` §4 says so and this build confirms it — **what moves is which of them is presented as the answer.** `-r4` published *"ruled key: STRICT, with the loose count reported alongside"*; that framing is superseded at the point of use in §10. **The third key's 76 is not an endpoint** — it is a different key's answer, reported as a divergence. **The coverage publishes beside the zero floor** so the bound is distinguishable from a check that looked nowhere.
2. **THE NEGATIVE CONTROL IS NOW EXECUTED, NOT DESCRIBED — AND THIS ARM'S OWN CLAIM WAS THE DEFECT.** `-r4` published a field named `what_a_failure_would_look_like`, a **sentence** about the failure the rebuilt coverage apparatus would catch, and `0089` §1 recorded it as *"demonstrating failing"*. **It was described, not demonstrated** — `CLAUDE.md`: *a control asserted to exist is not a control*, a rule that file records as having been broken by a mechanism that *"never fired"*. **Replaced by 6 injected defects run through the SAME `cover()`, `cover_ok()` and `_independent_identity()` the published invariants go through, and through the SAME aggregate expression: 5 of 5 checkable cases caught, and the run asserts it — an injected defect that got through would abort before a deliverable was written.** **One case passes by design and is named rather than hidden: identity_holds hardcoded True with no arithmetic behind it**, which `cover_ok` cannot distinguish from a computed `True` and which the separate literal-counter catches instead.
3. **THE D9 CLUSTERING UNIVERSE IS NOW RULED — U1 — AND THIS ARM CHANGED TO IT.** `0088` §3 closes what `0085` §2 opened and `0086` §1 located. This arm published **U3** on its previous build and now publishes **`U1_all_sweep_show_ids_carrying_a_slug`**, ranked on the ruled basis, **distinct strict keys merged**. **No count moves with it** — D9's search already ran on the whole sweep here, so strict is **0** and loose is **75** either way; what moves is **which clusters are illustrated**, which is the evidence for the loose key's only warrant. All three candidate universes are still measured side by side (§10a) so an arm on another one is diffable without a rerun, and **the units differ between them** — U1 and U2 count distinct show IDs per key, U3 counts complementary signature rows.
4. **BUT THE TIE-BREAK IS NOT RULED, AND THE TIE IS OCCUPIED. REPORTED, NOT RECONCILED.** `0088` §3 names the U1 top three as `secondchance` (8), `theisland` (7), `maigret` (6). **The first two are unique at their counts and reproduce exactly on this build.** The third sits inside a **6-way tie at 6** — `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` — so the third name is decided by a rule **no surface states**. Under this arm's tie-break (ascending key, applied after descending count) it is **`blackout`**; `maigret` is equally correct under another. **This is a spec gap inside the ruling that closed the previous spec gap, and it is reported rather than resolved by picking the name that matches the entry.**
5. **B3(a) WAS MEASURED ON THE WRONG SET LAST RUN, AND CORRECTING IT REVERSES THIS ARM'S OWN VERDICT.** `0089` §2(a) corrects `0088` §1(a): `T0` is day-floored, so `τ1` and `τ2` are midnight-aligned and `[τ − 24h, τ)` is the interval on which the half-open and date-level forms **agree**. **The separating interval is `[τ, τ + 24h)`, and this arm's `-r4` deliverable did not emit it** — it published the ruled window and the single instant at `τ1`, then read `OCCUPIED_INERT` and *"no outcome state differs"* off **1 row of 311**. **Measured on the right set (§14a): the verdict is `OUTCOME_DECIDING`.** On APPLY the separating interval holds **703** distinct S2 episodes at `τ1` and **303** at `τ2`, and **the forbidden form moves 71 APPLY rows and 59 DERIV rows into a different outcome state.** **The mandate is load-bearing on the RESULT, not merely on `|A|`.** **No published figure of this build moves** — the forbidden form is computed as a counterfactual and nowhere else — **but the previous verdict is withdrawn, not amended.**
6. **B3(b) AND B3(c) STAND FROM THE PREVIOUS RUN AND ARE RE-EXECUTED.** **(b) The per-site table exposed a real gap in this arm's own previous build**: the S1-side D11 carry-through — which has a ruling behind it **only** for the completion walk, because `0068` publishes line 1 at 220,107 — was also reaching the four `action_count_s1_*` columns, where nothing exempts it. **D11 is applied there now.** **44 pairs move in the record universe, 4 of them in the APPLY position-5 row set**, and **no waterfall line, outcome share or invariant moves with them**. **(c) The `tau2 <= tau_pull` assertion is promoted into the published set as invariant 9** — and **it is not slack**: rows sit with `tau2` exactly at `τ_pull`.
7. **THE TWO SURFACE CLAIMS THIS ARM PUBLISHED LAST RUN ARE BOTH NO LONGER TRUE, AND THEY ARE RE-READ RATHER THAN CARRIED.** A claim about the state of another file is a **measurement with an expiry date**; republished as prose it reports a defect that has since been fixed, which is the stale-figure problem one level up. Both were re-read off disk on this build. **(4) `specs/step8-readback.md`** — the string *"has not launched"* occurs **2** time(s), **1** of them inside the status stamp that supersedes it and **1** in the body, and the **stamp precedes every body occurrence: True** (`0089` §3, negative only — the body sentence is deliberately unedited). CLOSED AS A DEFECT, STANDING AS A QUESTION. decisions/0089 Sec 3 stamped the file, and the stamp precedes every body occurrence and marks the string SUPERSEDED. The r4 claim -- that the string sits there unqualified -- is NO LONGER TRUE and is not republished. The body sentence itself is deliberately unedited, because the stamp is NEGATIVE ONLY. What remains open is not the string but whether specs/ becomes a NINTH propagation surface, which 0089 Sec 4 carries for the Human Lead. **(5) The assertion-set count** — *"ASSERTION SET NOW HAS EIGHT"* occurs **0** times across `task-sheet.md` and this arm's definition file, *"NINE"* occurs **1**, and `task-sheet.md`'s *"four pure code checks"* sentence is now **marked SUPERSEDED at the point of use: True**. CLOSED. decisions/0089 Sec 3 acted on both halves and struck the 'four pure code checks' sentence at the point of use. NO SURFACE NOW STATES EIGHT. The r4 claim is NO LONGER TRUE and is not republished. This arm publishes NINE and no surface contradicts it. **Both halves are measured** — the negative grep for 'EIGHT MEMBERS' passes clean on a file that never said nine. Both halves are measured here: EIGHT must be 0 AND NINE must be non-zero — and the bytes read are reported, so a zero here is a zero found and not a file unopened. **What remains open on item 4 is not the string but whether `specs/` becomes a NINTH propagation surface**, carried for the Human Lead at `0089` §4.
8. **THE COEXTENSIVITY CHAIN HAS THREE LINKS, NOT TWO — and the third is DATA.** `0085` §4 (Red Team P4): `numerator = L2 ⟺ m_H = max(E2)` is construction given `L2 := |E2|`, but **`max(E2) = F2` is not** — it needs the finale to be the highest-numbered listed episode, and the `s2_aired_lt_listed` case separates them. **Measured here, not assumed: 0 of 1,138 frame shows separate them**, and `s2_aired_lt_listed` is 0 shows. ***`0083` §2 named TWO causes for a future FALSE row; there are THREE.*** No value moves; listed because the previous build's proof asserted a data premise as construction.
9. **THE TWO RESIDUALS THIS ARM AND INSTANCE A REPORTED ARE CLOSED, AND THE CLOSURE WAS RE-READ RATHER THAN QUOTED.** `0083` §3 fixed the stale `88` inside the strike-through and `f2_in_A_H`'s survival in `0077`'s adopted-name table. Both were re-read off disk on this build (§17): the strike-through names the 89-name enumeration on both surfaces this instance reads, `f2_in_A_H` is marked dropped at the point of use on both, `0077`'s **spelling** ruling survives the column's removal, and the three name sets are identical **as sets**. **Nothing here is open; it is listed because a closure that is quoted and not re-read is the shape this chain keeps failing on.**
10. **`p_at_bound` IS RULED, AND THE RULING REMOVED THE CHOICE THIS ITEM USED TO NAME.** `0083` §2 restates the column as marking **WHETHER** `p` reached its bound, not WHY, and withdraws `0082` §2's two-mechanism definition — the clauses are coextensive by construction, so the mechanism form never defined a column. **Both mechanisms are still computed separately here and all four cells emitted** (§18), because the emptiness is only checkable if it is emitted. **The two `p = 1.0` totals are reported as TOTALS, not as a split** — reading them as a split is a registered withdrawn argument. No value moves and no choice remains; listed so the *previous* framing is not read as still live.
11. **D11 and waterfall line 1.** `0068` rules 220,107 and leaves the D11 question open. Lines 1–3 are that figure here and would be 220,103 under the other reading; lines 4–7 are identical either way, verified row by row.
12. **The set-membership denominator — CLOSED, and this arm publishes reading B.** `0083` §1 amends `0074` ruling 4: the difference was never a divergence, the three readings are one one-parameter family indexed by where D11 applies, and **every member drops zero records**, so it survives into no result and is not a Step 14 limitation. This instance produces **6,065,610** — D11 on the S2 side, the S1 side carried because `0068` rules line 1 at 220,107 as published; the others are 6,065,704 (D11 nowhere) and 6,065,537 (D11 on both). The decomposition is 73 S1-side + 94 S2-side = 167, so `0074`'s 94 is the S2-side component alone. **What remains open is `0068`'s own item** — whether D11 applies to the S1 completion walk — **and it is answered there, not here.** Listed because all three readings publish with their pipelines named, so no arm's figure is later read as a divergence.
13. **D3′'s cleared shares are not monotone between `W = 91` and `W = 107`** — 98.81% then 98.84% on APPLY. An open item at `0076` §5, reproduced rather than smoothed.
14. **D8's position.** Pre- or post-liveness is unstated. Both are reported.
15. **D2's population.** Unstated at the point of use. Four are reported and each labelled.
16. **D9's third key.** The spec now defines strict and loose (`0076` §3). On this data the third key — a trailing digit group of arbitrary length — gives **76** complementary signature pairs against loose's **75**, reproducing the divergence `0076` describes. It is measured and not used.
17. **The grain of D9 half (b).** `0078` §3 requires both halves under both keys, which is done; but the unit of half (b) is not fixed. This instance reports **B-side pairs on frame shows**, then how many of them sit inside the position-3 drop set, which is the only reading on which the drop set is load-bearing.
18. **The provenance string itself.** `0078` and `0079` §2 require every count to name the build it was measured on, and fix no format. This instance emits one build identifier plus an input fingerprint (size and mtime of every input) and a SHA-256 of its own pipeline sources. **A different arm will phrase the label differently and no figure moves**; what matters is that both arms label everything rather than two figures.
19. **The shape of the position-3 drop set — ruled, and it agrees.** `0075` ruling 2 named an empty set; `0077` §2 restates it as the pair universe less the completers, 58,345 pairs, with distinct-episode counts and the show's threshold. This instance reported the same count on the previous build, so the restatement removes the choice without moving a figure.
20. **The discovery-channel overlap, now published in every unit.** `0079` §3 names three and this instance measures four numbers: 324 of 5,694 pool usernames, 178 of 2,549 accounts pulled, 174 of 2,422 accounts and 17,783 of 196,654 pairs in the position-5 population. All four reproduce the ruled figures.
21. **The waterfall's unit.** Pairs are primary; users and shows are reported alongside because position 2 is explicitly a filter on shows.
22. **Undated records.** 379 records in the sweep carry no `watched_at`. None is an in-frame S1/S2 episode record, so they touch no outcome. They are **not** discarded by D11, which removes `watched_at >= tau_pull`; a reading that requires a record to be positively "dated before `tau_pull`" would drop them from the liveness evidence. Measured inert: the exclusion counts are identical either way at every arm.
23. **DERIV's position 4.** DERIV is Step 5 *line 4* less D10, and line 4 applies three restrictions that are not Step 8 filter positions. Its waterfall line 4 is therefore not the adopted contamination exclusion, and is labelled as such rather than silently conflated with APPLY's.
24. **At `W = 213` the DERIV started-and-left exclusion component is 147 while APPLY's is 148.** No published figure covers DERIV per arm above `W = 108`, so this is new rather than divergent, and it is stated so it is not read as an error later.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
