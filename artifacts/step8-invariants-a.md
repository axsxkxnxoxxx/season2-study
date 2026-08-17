# Step 8 — invariant report, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** · **H = 91 days** · **Zero API calls** · **Counts only**

> **SCOPE OF THIS REPORT** (`decisions/0096` ruling 1). It states **this arm's own invariant results, the populations they ran on and what they can and cannot establish** — and nothing else. **Not the other arm, not the shared controls, not the status of any step or gate.** **Every result below is produced by one pipeline run**, build `a/2026-08-17-0096`, defined in full in the waterfall deliverable §0; the per-stage run record is `logs/step8_a_run.json`.

> **WHAT THE SPEC REQUIRES OF THIS REPORT.** **`0079` B6: every invariant result names the build it was measured on.** **`0080` §3: every invariant names the population it runs on and accounts for every row in it**, reporting `rows_asserted + rows_not_asserted = rows_in_the_stated_population`. **`0068`: every invariant carries a CODE CHECK or DATA CHECK label.** **`0088` §1(c): the `τ2 ≤ τ_pull` assertion is promoted into the published set**, which takes it to nine members. **`0074` ruling 3: the set-membership drop rule is a coverage count and is NOT asserted here.**

> **WHY THE COVERAGE IDENTITY IS NOT DECORATION, in this report's own numbers.** `0080` §3 records a dual-run gap in which `p` was asserted on **19,042** rows — the *post-liveness* Started-and-left count — against a *pre-liveness* non-S&L clause of **177,513**, summing to **196,555 against a 196,654-row table**, with **99 rows covered by neither clause.** **This report states both clauses and their sum for every check** — see the coverage table below, where `p` reads **19,141 + 177,513 = 196,654** and the post-liveness 19,042 appears only as a labelled contrast.

> **EVERY INVARIANT CARRIES A LABEL** (`decisions/0068`). **A code check catches an implementation that computed something wrongly; it cannot fail on any data, and it is NOT evidence for the rule.** A report saying "all invariants passed" overstates what was verified unless it names which ones could have failed.

**Result: 9 checks ran and all passed.** **6 cannot fail on any data** (CODE CHECK); **1 is a code check by construction with force only as specified**; and **2 CAN FAIL ON REAL DATA** (DATA CHECK). The 703 line is **not an invariant** and is reported separately below as a population reconciliation.

> **THAT RESULT LINE IS THIS ARM'S OWN SPLIT AND IS ALL THIS REPORT SAYS ABOUT ANY HEADLINE; a cross-arm statement belongs to the Human Lead's diff.** **6 + 1 + 2**, **derived from the label strings in the table below and never typed.**
>
> **Why three classes and not two.** **The spec's label vocabulary has three values**, and **collapsing the middle member into either outer class changes the answer to *what could this report have caught?*** Folded upward it reads as **seven checks that cannot fail**; folded downward as **three that can**. **The sentence a reader takes away is the headline**, so the middle class is published as its own. **The spec's own sentence has that shape** — *"SIX pure code checks, one code-by-construction with force only as specified, and TWO that can fail on real data."*

**THIS SET IS NINE** (`decisions/0088` §1(c)), which **promotes the `τ2 ≤ τ_pull` assertion into the published set** — it **already ran in this arm's stage 3** (`src/step8_a_3_table.py`) but **sat outside the deliverable, so no reader could see it**. **The two checks that can fail on data are not formalities here**: check 7 separates a pair-level liveness implementation from an account-level one, which the 703-from-216-accounts figure alone cannot do, and check 8 is the one that would fail *in the direction of the result*.

> ***THE NINTH MAKES THE FALSIFIABILITY RATIO WORSE, NOT BETTER, and it is stated because an added check reads as an added guarantee.*** The promoted assertion is a **sixth pure CODE CHECK**, so the set goes from **5 + 1 + 2 to 6 + 1 + 2** and **the number that can fail on real data is unchanged at TWO**. It adds **visibility**, not power — which is what `0088` §1(c) asked for, since *"an assertion a reader of the deliverable cannot see is not a published check"*. **It is not evidence for the liveness rule or for any outcome.**

**The set-membership drop rule is NOT in this list.** `decisions/0074` ruling 3 makes it a **coverage count**: records examined and records dropped are reported in the waterfall deliverable, and nothing is asserted. Step 8's own bullet already called it *"an implementation check, not a data check"*.

| # | Invariant | Label | Result |
| :-- | :--- | :--- | :--- |
| 1 | outcome states are mutually exclusive and sum to the post-position-7 row set | **CODE CHECK** | PASS |
| 2 | filter counts decrease monotonically, coded >= and not > | **CODE CHECK** | PASS |
| 3 | distinct episodes never exceed season length | **CODE CHECK** | PASS |
| 4 | A is a subset of A_H on every row | **CODE CHECK** | PASS |
| 5 | clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equal to one of the two | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** | PASS |
| 6 | p lies in (0, 1] on every Started-and-left row and is null everywhere else | **CODE CHECK** | PASS |
| 7 | no account is dropped wholesale by the pair-level liveness filter | **DATA CHECK** | PASS |
| 8 | no access_denied or otherwise skipped account is read as empty | **DATA CHECK** | PASS |
| 9 | no retained row's outcome window extends past tau_pull: tau2 <= tau_pull on every position-5 row | **CODE CHECK** | PASS |

## Coverage — every invariant names its population and accounts for every row in it

**`decisions/0080` §3.** This is the provenance rule applied to invariants: **an invariant that passes on one population and was never run on another reads as a pass on both**, and **a passing invariant whose coverage the instance chose is a code check on the instance's choice.** The identity `asserted + not asserted = population` must hold on every stated population.

| # | Invariant | Population(s) as specified | Identity |
| :-- | :--- | :--- | :--- |
| 1 | outcome states are mutually exclusive and sum to the… | FOUR, ALL STATED (decisions/0080 SS3): the post-position-7 row set 195,951 AND the position-5 row set 196,654, plus the DERIV pair 147,271 / 147,370 | APPLY_post_position_7_195951 — `32769 + 19042 + 144140 + 0 not asserted = 195951`; APPLY_position_5_table_row_set_196654 — `33373 + 19141 + 144140 + 0 not asserted = 196654`; DERIV_post_position_7_147271 — `9145 + 16744 + 121382 + 0 not asserted = 147271`; DERIV_position_5_147370 — `9145 + 16843 + 121382 + 0 not asserted = 147370` |
| 2 | filter counts decrease monotonically, coded >= and n… | BOTH CHAINS (decisions/0080 SS3): APPLY's seven positions and DERIV's | coverage_APPLY — `7 + 0 not asserted = 7`; coverage_DERIV — `7 + 0 not asserted = 7` |
| 3 | distinct episodes never exceed season length… | BOTH SEASONS, ON EVERY PAIR THE SET-MEMBERSHIP RULE EXAMINES -- the pair universe of 278,452, NOT the 196,654 position-5 row set | coverage — `278452 + 0 not asserted = 278452` |
| 4 | A is a subset of A_H on every row… | the 196,654 position-5 row set, EVERY ROW (decisions/0080 SS3) | coverage — `196654 + 0 not asserted = 196654` |
| 5 | clock start is on or after the S2 finale date, on or… | the 196,654 position-5 row set, EVERY ROW, with the first-pass S1 completion date RECOMPUTED INDEPENDENTLY -- the only thing giving this one force (de | coverage — `196654 + 0 not asserted = 196654` |
| 6 | p lies in (0, 1] on every Started-and-left row and i… | ALL Started-and-left rows AT POSITION 5, null on the rest, and the two clauses must sum to 196,654 EXACTLY (decisions/0080 SS3) | coverage — `19141 + 177513 + 0 not asserted = 196654` |
| 7 | no account is dropped wholesale by the pair-level li… | BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 SS3): the accounts holding a position-5 pair in APPLY and the accounts holding one in DERIV, each report | APPLY_position_5 — `2206 + 215 + 1 + 0 not asserted = 2422`; DERIV_position_5 — `2329 + 72 + 1 + 0 not asserted = 2402` |
| 8 | no access_denied or otherwise skipped account is rea… | THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 SS3) -- every distinct account the Step 4 pull touched, not the accounts that survived into the t | coverage — `2874 + 0 not asserted = 2874` |
| 9 | no retained row's outcome window extends past tau_pu… | BOTH POPULATIONS, EVERY ROW: the 196,654 APPLY position-5 row set and the 147,370 DERIV position-5 row set | APPLY_position_5 — `196654 + 0 + 0 not asserted = 196654`; DERIV_position_5 — `147370 + 0 + 0 not asserted = 147370` |

**15 coverage identities were checked and all hold: True.** Build: every count in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.

> ***STRUCK, whatever else is ruled*** (`decisions/0088` §2(d)): ~~*"The run asserts this, so a report that omitted a population could not be written by this pipeline."*~~ **It is a control asserted to exist.**

> **A MULTI-CLAUSE IDENTITY IS NOT AUTOMATICALLY ONE THAT CAN FAIL.** A test of the form `len(parts) > 1` — *"it has more than one clause"* — ***admits an identity that cannot fail on any data***, because clauses forming a **complementary partition of the same mask the population size was taken from** sum to the population **for any mask**: invariant 1's `never / left / continued` are exhaustive by the expressions that define them; invariant 6's are `M & left` and `M & ~left`; invariant 7's `mixed` and `wholesale` partition `touched` by set algebra; invariant 9's are `τ2 ≤ τ_pull` and its complement. **Each of those holds whatever mask `M` is — including a mask that is NOT the population named, which is the defect** `0080` §3 introduced the identity to detect.

**THE FIX IS THE ONE THE HOLE ACTUALLY NEEDS: the population size is now sourced INDEPENDENTLY of the asserted count.** The 99-row hole was a numerator taken **post-liveness** against a denominator taken **pre-liveness**; that is detectable only if the denominator comes from somewhere other than the masks the numerator is built from. So **15 of the 15 identities now take their population size from a different file**, and **0 remain in the cannot-fail class, labelled bookkeeping at the point of use** *(the label stays in the code and in the schema whether or not any identity is in that class on this build — a class that happens to be empty today must still be nameable tomorrow)*. **Every identity carries its tier in the `.json` at `population_size_independence` and `what_it_can_detect`** — an unlabelled check that cannot fail reads as one that can (`0069`, applied to the coverage apparatus rather than to the invariants).

| Independence tier | Source | What the identity can detect | count |
| :--- | :--- | :--- | ---: |
| `EMITTED_DELIVERABLE` | `analysis_table.csv.gz`, written by stage 3 | **an invariant run on a population other than the one it names** | 11 |
| `INDEPENDENT_FILE` | an earlier stage's own JSON | **an invariant run on a population other than the one it names** | 3 |
| `INDEPENDENT_CODE_PATH` | the same file parsed by different code | **a parse or dedup disagreement in the population size** | 1 |

*Build: every count in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

#### The `+1` perturbation — ***IT DOES NOT TEST INDEPENDENCE***

> ***THIS BLOCK IS NOT A DEMONSTRATION OF INDEPENDENCE AND IS NOT PUBLISHED AS ONE*** (`decisions/0091` §2). **On a same-mask denominator the clauses sum to `N` by construction and the stated population reads `N + 1`, so the identity fails — IDENTICALLY, whether or not the denominator was sourced independently.** Perturbing the **denominator** cannot separate the two cases. **The control that can is immediately below.**

**What it DOES show, and it is kept under that label:** that each identity is **arithmetic rather than a hardcoded literal**. Each of the **15** independent identities is re-evaluated against **its population size + 1** and must report FAIL. **All hold against the true value and fail against the perturbed one: True.** *The separate literal counter already shows the same thing, which is why this is a narrow check and not the one that matters.*

#### The control that DOES test independence — injected wrong-population defects

**The escape the independent source exists to catch is AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES.** Where an identity's clauses are a complementary partition of a mask, **swapping the mask moves the clauses AND the same-mask denominator together**, so the same-mask identity still **PASSES** on the wrong population. **Only a denominator keyed on the NAME rather than on the mask can fail.** So each defect below asserts **both directions**.

| # | Injected defect | clauses sum to | same-mask denominator | **same-mask form: can it detect it?** | independent source | **independent form: does it detect it?** |
| ---: | :--- | ---: | ---: | :--- | ---: | :--- |
| 1 | invariant 1 run on the post-liveness mask while naming the position-5 row set | 195,951 | 195,951 | **NO — it passes** | 196,654 | **YES** |
| 2 | invariant 1 run on the DERIV post-liveness mask while naming DERIV position 5 | 147,271 | 147,271 | **NO — it passes** | 147,370 | **YES** |
| 3 | invariant 6's 0080 SS3 mispairing: post-liveness S&L against pre-liveness non-S&L | 196,555 | 196,654 | yes | 196,654 | **YES** |
| 4 | invariant 7 run on DERIV accounts while naming APPLY's position-5 accounts | 2,402 | 2,402 | **NO — it passes** | 2,422 | **YES** |
| 5 | invariant 2 covering six positions while naming seven | 6 | 6 | **NO — it passes** | 7 | **YES** |
| 6 | invariant 8 with the skipped account classes omitted from the coverage | 2,422 | 2,422 | **NO — it passes** | 2,874 | **YES** |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**6 defects injected; 6 detected by the independently-sourced identity; 5 of them INVISIBLE to the same-mask form.** **Every case discriminates as expected: True**, and **the run asserts it**, so an escape aborts before a deliverable is written. ***Case 3 is the labelled exception***: its two clauses come from different masks, so the same-mask form fails on it too — stated rather than glossed, **because the point of the suite is which control catches what**.

**Case 3 is also the control this arm already had, and `0091` §2 credits it as real:** invariant 6's `THE_HOLE_THIS_WOULD_NOW_CATCH` reconstructs `0080` §3's exact mispairing — **19,042 + 177,513 = 196,555 against 196,654, 99 rows in neither** — and the identity **fails**. **What was missing is that it covered ONE invariant.** The five other cases extend it, and they are the ones the same-mask form cannot see.

| Identity shape | What it can detect |
| :--- | :--- |
| **population size from the same mask as the asserted count** — with one clause or with five | **Nothing.** `N − N = 0`, and a complementary partition of `M` sums to `M` for every `M` |
| **population size from an independent source** | **An invariant run on a population other than the one it names**, which is the 99-row hole `0080` §3 was written for |

> **What invariant 6 would now catch, measured rather than described.** Pairing the post-liveness Started-and-left numerator with the pre-liveness non-S&L clause — the exact mispairing `0080` §3 records — is reconstructed on this build and evaluated against the emitted table's row count; the identity **fails**, and the rows covered by neither clause are reported. **Under a same-mask denominator that pairing could not be detected at all.** See invariant 6's `THE_HOLE_THIS_WOULD_NOW_CATCH` below.

### 1. outcome states are mutually exclusive and sum to the post-position-7 row set

**CODE CHECK.** Step 1 SS7's partition is proved exhaustive and disjoint, so this can only catch an assignment coded wrongly. It is not evidence for the rule.

**Population:** FOUR, ALL STATED (decisions/0080 SS3): the post-position-7 row set 195,951 AND the position-5 row set 196,654, plus the DERIV pair 147,271 / 147,370. The table carries all position-5 rows, so the partition holds on both and NEITHER SUBSTITUTES FOR THE OTHER.

- `coverage_rows` = `195951`
- `by_population`:
    - `APPLY_post_position_7_195951`:
        - `population` = `APPLY, post-position-7 row set`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `195951`
        - `rows_asserted` = `195951`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `32769 + 19042 + 144140 + 0 not asserted = 195951`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows with live = True`
        - `independent_population_size` = `195951`
        - `identity_against_the_independent_source` = `32769 + 19042 + 144140 + 0 not asserted = 195951`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows with live = True, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[32769, 19042, 144140]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- never / continued / left are mutually exclusive and exhaustive by the expressions that define them, so the three always sum to the mask. The clause counts are informative; what makes this identity falsifiable is the INDEPENDENT population size, not the clause count.`
        - `exactly_one_state_per_row` = `True`
        - `never_started` = `32769`
        - `started_and_left` = `19042`
        - `continued` = `144140`
        - `sum_of_the_three` = `195951`
        - `sum_equals_row_set` = `True`
        - `holds` = `True`
    - `APPLY_position_5_table_row_set_196654`:
        - `population` = `APPLY, position-5 row set -- what the analysis table carries`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `196654`
        - `rows_asserted` = `196654`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `33373 + 19141 + 144140 + 0 not asserted = 196654`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3`
        - `independent_population_size` = `196654`
        - `identity_against_the_independent_source` = `33373 + 19141 + 144140 + 0 not asserted = 196654`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[33373, 19141, 144140]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- never / continued / left are mutually exclusive and exhaustive by the expressions that define them, so the three always sum to the mask. The clause counts are informative; what makes this identity falsifiable is the INDEPENDENT population size, not the clause count.`
        - `exactly_one_state_per_row` = `True`
        - `never_started` = `33373`
        - `started_and_left` = `19141`
        - `continued` = `144140`
        - `sum_of_the_three` = `196654`
        - `sum_equals_row_set` = `True`
        - `holds` = `True`
    - `DERIV_post_position_7_147271`:
        - `population` = `DERIV, post-position-7 row set`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `147271`
        - `rows_asserted` = `147271`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `9145 + 16744 + 121382 + 0 not asserted = 147271`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows with in_deriv and live`
        - `independent_population_size` = `147271`
        - `identity_against_the_independent_source` = `9145 + 16744 + 121382 + 0 not asserted = 147271`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows with in_deriv and live, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[9145, 16744, 121382]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- never / continued / left are mutually exclusive and exhaustive by the expressions that define them, so the three always sum to the mask. The clause counts are informative; what makes this identity falsifiable is the INDEPENDENT population size, not the clause count.`
        - `exactly_one_state_per_row` = `True`
        - `never_started` = `9145`
        - `started_and_left` = `16744`
        - `continued` = `121382`
        - `sum_of_the_three` = `147271`
        - `sum_equals_row_set` = `True`
        - `holds` = `True`
    - `DERIV_position_5_147370`:
        - `population` = `DERIV, position-5 row set`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `147370`
        - `rows_asserted` = `147370`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `9145 + 16843 + 121382 + 0 not asserted = 147370`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows with in_deriv = True`
        - `independent_population_size` = `147370`
        - `identity_against_the_independent_source` = `9145 + 16843 + 121382 + 0 not asserted = 147370`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows with in_deriv = True, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[9145, 16843, 121382]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- never / continued / left are mutually exclusive and exhaustive by the expressions that define them, so the three always sum to the mask. The clause counts are informative; what makes this identity falsifiable is the INDEPENDENT population size, not the clause count.`
        - `exactly_one_state_per_row` = `True`
        - `never_started` = `9145`
        - `started_and_left` = `16843`
        - `continued` = `121382`
        - `sum_of_the_three` = `147370`
        - `sum_equals_row_set` = `True`
        - `holds` = `True`
- `coverage_identity_holds_on_every_stated_population` = `True`
- `identity_holds_against_the_INDEPENDENT_source_on_every_stated_population` = `True`
- `populations_whose_identity_was_checked` = `4`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 2. filter counts decrease monotonically, coded >= and not >

**CODE CHECK.** filters only remove rows, so it fails only on an implementation that ADDS them -- a duplicating join. >= is kept so the invariant does not encode a property of one rule: a position that legitimately removes nothing must not fail (0047, 0049). Load-bearing in fact: position 2 removes exactly 0 pairs on this frame.

**Population:** BOTH CHAINS (decisions/0080 SS3): APPLY's seven positions and DERIV's. Running it on one chain and not the other would read as a pass on both.

- `chain_APPLY` = `[220107, 220107, 220107, 201900, 196654, 195951, 195951]`
- `chain_DERIV` = `[220107, 220107, 220107, 152126, 147370, 147271, 147271]`
- `coverage_positions` = `14`
- `coverage_APPLY`:
    - `population` = `APPLY's seven filter positions`
    - `unit` = `positions`
    - `positions_in_the_stated_population` = `7`
    - `positions_asserted` = `7`
    - `positions_not_asserted` = `0`
    - `coverage_identity` = `7 + 0 not asserted = 7`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `INDEPENDENT_FILE`
    - `population_size_source` = `processed/step8/a/positions.json waterfall_APPLY (positions 1-5, stage 2) plus positions 6 and 7 from outcomes.json (stage 3)`
    - `independent_population_size` = `7`
    - `identity_against_the_independent_source` = `7 + 0 not asserted = 7`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/positions.json waterfall_APPLY (positions 1-5, stage 2) plus positions 6 and 7 from outcomes.json (stage 3), so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
- `coverage_DERIV`:
    - `population` = `DERIV's seven filter positions`
    - `unit` = `positions`
    - `positions_in_the_stated_population` = `7`
    - `positions_asserted` = `7`
    - `positions_not_asserted` = `0`
    - `coverage_identity` = `7 + 0 not asserted = 7`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `INDEPENDENT_FILE`
    - `population_size_source` = `processed/step8/a/positions.json waterfall_DERIV (positions 1-5, stage 2) plus positions 6 and 7 from outcomes.json (stage 3)`
    - `independent_population_size` = `7`
    - `identity_against_the_independent_source` = `7 + 0 not asserted = 7`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/positions.json waterfall_DERIV (positions 1-5, stage 2) plus positions 6 and 7 from outcomes.json (stage 3), so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
- `chain_APPLY_agrees_with_positions_json_and_outcomes_json` = `True`
- `chain_DERIV_agrees_with_positions_json_and_outcomes_json` = `True`
- `chain_note` = `chain[i] is the count after filter position i+1; the transition from entry i to entry i+1 is the effect of filter position i+2`
- `filter_positions_removing_exactly_zero_APPLY` = `[2, 3, 7]`
- `filter_positions_removing_exactly_zero_DERIV` = `[2, 3, 7]`
- `inert_positions_labelled_not_silent` = `positions 1, 2, 3 and 7 remove 0 BY CONSTRUCTION and are labelled inert with the reason in the waterfall deliverable (decisions/0079 SS4). An unlabelled always-zero filter reads as evidence the rule FOUND NOTHING when it is evidence the rule CANNOT FIRE.`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 3. distinct episodes never exceed season length

**CODE CHECK.** the set-membership drop rule already establishes |D| <= L by construction; this fails only if an implementation filtered by the numeric range 1..F instead of by the listed set E (Step 1 SS3.2). Not evidence for the rule.

**Population:** BOTH SEASONS, ON EVERY PAIR THE SET-MEMBERSHIP RULE EXAMINES -- the pair universe of 278,452, NOT the 196,654 position-5 row set. decisions/0080 SS3: the wider reading is required and the narrower does not substitute. The record count is stated with it.

- `coverage_pairs` = `278452`
- `coverage`:
    - `population` = `the pair universe the set-membership rule examines`
    - `unit` = `pairs`
    - `pairs_in_the_stated_population` = `278452`
    - `pairs_asserted` = `278452`
    - `pairs_not_asserted` = `0`
    - `coverage_identity` = `278452 + 0 not asserted = 278452`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `INDEPENDENT_FILE`
    - `population_size_source` = `processed/step8/a/scan_summary.json, written by stage 1`
    - `independent_population_size` = `278452`
    - `identity_against_the_independent_source` = `278452 + 0 not asserted = 278452`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/scan_summary.json, written by stage 1, so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
    - `records_examined` = `6065704`
    - `records_dropped_by_the_rule` = `0`
    - `seasons_asserted` = `['S1', 'S2']`
    - `distinct_episode_rows_asserted_S1` = `2860465`
    - `distinct_episode_rows_asserted_S2` = `2489811`
- `max_D1_minus_L1` = `0`
- `max_D2_minus_L2` = `0`
- `max_AH_minus_L2` = `0`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 4. A is a subset of A_H on every row

**CODE CHECK.** true by construction since tau1 < tau2 and both sets are prefixes of the same timestamp-ordered episode list; it can only catch the two sets being computed wrongly or the bounds transposed. Not evidence for the rule.

**Population:** the 196,654 position-5 row set, EVERY ROW (decisions/0080 SS3)

- `coverage_rows` = `196654`
- `coverage`:
    - `population` = `APPLY, position 5 -- the analysis table's row set`
    - `unit` = `rows`
    - `rows_in_the_stated_population` = `196654`
    - `rows_asserted` = `196654`
    - `rows_not_asserted` = `0`
    - `coverage_identity` = `196654 + 0 not asserted = 196654`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `EMITTED_DELIVERABLE`
    - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3`
    - `independent_population_size` = `196654`
    - `identity_against_the_independent_source` = `196654 + 0 not asserted = 196654`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3, so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
- `rows_where_A_exceeds_A_H` = `0`
- `rows_where_max_A_exceeds_max_A_H` = `0`
- `also_holds_on_the_post_position_7_row_set` = `True`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 5. clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equal to one of the two

**CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.** T0 is a max(), so the two inequalities and the equality hold for any correct implementation. The force comes from recomputing the first-pass S1 completion date INDEPENDENTLY from the episode records rather than reading back the pipeline's value: a disagreement there is a real finding. Read back rather than recomputed, this degrades to a code check and proves nothing.

**Population:** the 196,654 position-5 row set, EVERY ROW, with the first-pass S1 completion date RECOMPUTED INDEPENDENTLY -- the only thing giving this one force (decisions/0080 SS3)

- `replaces` = `the withdrawn 'no clock start precedes an S2 premiere', vacuous under a finale-anchored clock`
- `coverage_rows` = `196654`
- `coverage`:
    - `population` = `APPLY, position 5 -- the analysis table's row set`
    - `unit` = `rows`
    - `rows_in_the_stated_population` = `196654`
    - `rows_asserted` = `196654`
    - `rows_not_asserted` = `0`
    - `coverage_identity` = `196654 + 0 not asserted = 196654`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `EMITTED_DELIVERABLE`
    - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3`
    - `independent_population_size` = `196654`
    - `identity_against_the_independent_source` = `196654 + 0 not asserted = 196654`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3, so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
    - `independent_recomputation_covers_pairs` = `278452`
    - `read_back_from_the_pipeline` = `False`
- `on_or_after_S2_finale` = `True`
- `on_or_after_first_pass_S1_completion` = `True`
- `equals_one_of_the_two` = `True`
- `independent_recomputation`:
    - `what` = `the S1 completion test and first-pass date recomputed from the episode records, never read back from processed/step5/pair_revision5.csv`
    - `pair_universe` = `278452`
    - `completers_recomputed` = `220107`
    - `completers_in_the_published_pair_table` = `220107`
    - `agreement_on_membership_over_the_universe` = `278452`
    - `completers_only_in_my_recomputation` = `0`
    - `completers_only_in_the_published_table` = `0`
    - `s1_completion_date_mismatches` = `0`
    - `T0_mismatches` = `0`
    - `stored_dates_unparseable_s1_then_t0` = `[0, 0]`
    - `pairs_whose_S1_completion_date_is_a_corrupt_year_1_timestamp` = `3`
- `tie_break_note` = `Step 1 SS2.2 breaks exactly-equal timestamps by episode number then smallest event id. The recomputation applies that tiebreak; the agreement counts above are reported rather than a choice being made about whether a tiebreak difference would count as a failure.`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 6. p lies in (0, 1] on every Started-and-left row and is null everywhere else

**CODE CHECK.** SPECIFIED by decisions/0074 ruling 2; LABEL CORRECTED from DATA CHECK to CODE CHECK by decisions/0076 on both instances' own proof. Started-and-left requires |A| >= 1, so max(A_H) exists; set membership bounds the rank numerator in [1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has a gap. It is kept because Step 10 publishes p -- but it proves the code, not the rule.

**Population:** ALL Started-and-left rows AT POSITION 5, null on the rest, and the two clauses must sum to 196,654 EXACTLY (decisions/0080 SS3). The dual run had one arm assert p on 19,042 rows -- the POST-LIVENESS Started-and-left count -- against a PRE-LIVENESS denominator of 177,513 non-S&L rows, leaving 99 rows covered by neither clause, exactly the started-and-left liveness exclusions. Do not take the numerator post-liveness and the denominator pre-liveness. THE TWO-CLAUSE SUM ALONE DOES NOT CLOSE THAT HOLE: the clauses are `M & left` and `M & ~left` -- a set and its complement within the same mask M -- so they sum to M.sum() for EVERY M, including a mask that is not the population named, which is the defect. What closes it is the denominator coming from somewhere else: it is read from the EMITTED analysis table, so a numerator taken post-liveness against a pre-liveness denominator FAILS.

- `coverage_rows` = `19141`
- `coverage`:
    - `population` = `APPLY, position 5 -- the analysis table's row set`
    - `unit` = `rows`
    - `rows_in_the_stated_population` = `196654`
    - `rows_asserted` = `196654`
    - `rows_not_asserted` = `0`
    - `coverage_identity` = `19141 + 177513 + 0 not asserted = 196654`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `EMITTED_DELIVERABLE`
    - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3`
    - `independent_population_size` = `196654`
    - `identity_against_the_independent_source` = `19141 + 177513 + 0 not asserted = 196654`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3, so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
    - `asserted_clause_counts` = `[19141, 177513]`
    - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- `M & left` and `M & ~left` are a set and its complement within the same mask, so they sum to M for every M. The clause counts show a reader where a hole would be; the INDEPENDENT denominator is what detects one.`
    - `clause_1_rows_asserted_p_in_0_1_started_and_left` = `19141`
    - `clause_2_rows_asserted_p_is_null_not_started_and_left` = `177513`
    - `started_and_left_post_liveness_for_contrast_NOT_the_numerator` = `19042`
    - `THE_HOLE_THIS_WOULD_NOW_CATCH`:
        - `the_defective_pairing` = `numerator 19042 (post-liveness S&L) with denominator clause 177513 (pre-liveness non-S&L)`
        - `what_it_sums_to` = `196555`
        - `independent_population_size` = `196654`
        - `rows_covered_by_neither_clause` = `99`
        - `would_the_identity_FAIL` = `True`
        - `note` = `measured on this build, not asserted: the exact mispairing decisions/0080 SS3 describes is reconstructed and the identity is evaluated on it. Under a same-mask denominator this pairing could not be detected at all.`
- `min` = `0.038461538461538464`
- `max` = `1.0`
- `nulls_among_started_and_left` = `0`
- `non_null_outside_started_and_left` = `0`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 7. no account is dropped wholesale by the pair-level liveness filter

**DATA CHECK.** CLAUDE.md and Step 7: 'One account can be live for one show and not another. Never drop a user wholesale.' 703 pairs from 216 accounts is consistent with a pair-level AND an account-level implementation, and nothing in the exclusion set distinguished them. Asserting that at least one account holds BOTH a live and a not-live pair separates them. THIS CAN FAIL ON REAL DATA (decisions/0076).

**Population:** BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 SS3): the accounts holding a position-5 pair in APPLY and the accounts holding one in DERIV, each reporting accounts that hold both a live and a not-live pair. Every account in each is classified, so the coverage identity holds on both.

- `by_population`:
    - `APPLY_position_5`:
        - `population` = `accounts holding a position-5 APPLY pair`
        - `unit` = `accounts`
        - `accounts_in_the_stated_population` = `2422`
        - `accounts_asserted` = `2422`
        - `accounts_not_asserted` = `0`
        - `coverage_identity` = `2206 + 215 + 1 + 0 not asserted = 2422`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, distinct user_idx`
        - `independent_population_size` = `2422`
        - `identity_against_the_independent_source` = `2206 + 215 + 1 + 0 not asserted = 2422`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, distinct user_idx, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[2206, 215, 1]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- mixed and wholesale partition `touched` by set algebra, so the three classes sum to the account total for any mask. The INDEPENDENT account count is what can fail.`
        - `accounts_untouched_by_the_exclusion` = `2206`
        - `accounts_touched_by_the_exclusion` = `216`
        - `classification_covers_every_account` = `True`
        - `accounts_holding_BOTH_a_live_and_a_not_live_pair` = `215`
        - `accounts_all_of_whose_pairs_are_excluded` = `1`
        - `of_those_holding_more_than_one_pair_in_this_population` = `0`
        - `holds` = `True`
    - `DERIV_position_5`:
        - `population` = `accounts holding a position-5 DERIV pair`
        - `unit` = `accounts`
        - `accounts_in_the_stated_population` = `2402`
        - `accounts_asserted` = `2402`
        - `accounts_not_asserted` = `0`
        - `coverage_identity` = `2329 + 72 + 1 + 0 not asserted = 2402`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, distinct user_idx on in_deriv rows`
        - `independent_population_size` = `2402`
        - `identity_against_the_independent_source` = `2329 + 72 + 1 + 0 not asserted = 2402`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, distinct user_idx on in_deriv rows, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[2329, 72, 1]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- mixed and wholesale partition `touched` by set algebra, so the three classes sum to the account total for any mask. The INDEPENDENT account count is what can fail.`
        - `accounts_untouched_by_the_exclusion` = `2329`
        - `accounts_touched_by_the_exclusion` = `73`
        - `classification_covers_every_account` = `True`
        - `accounts_holding_BOTH_a_live_and_a_not_live_pair` = `72`
        - `accounts_all_of_whose_pairs_are_excluded` = `1`
        - `of_those_holding_more_than_one_pair_in_this_population` = `0`
        - `holds` = `True`
- `coverage_accounts_with_a_position_5_pair` = `2422`
- `accounts_touched_by_the_exclusion` = `216`
- `accounts_holding_BOTH_a_live_and_a_not_live_pair` = `215`
- `accounts_all_of_whose_position_5_pairs_are_excluded` = `1`
- `of_those_accounts_holding_more_than_one_position_5_pair` = `0`
- `reading` = `accounts in the last line held exactly one position-5 pair unless the count above is non-zero; for a single-pair account 'wholesale' and 'pair-level' are indistinguishable and no inference is available either way.`
- `assertion` = `accounts_holding_BOTH_a_live_and_a_not_live_pair > 0, ON BOTH POPULATIONS`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 8. no access_denied or otherwise skipped account is read as empty

**DATA CHECK.** CLAUDE.md: 'a skipped user silently read as empty becomes a false never started in the headline'; rule and evidence at artifacts/step0-access-and-setup.md SS7. A skipped account must stay distinguishable downstream and must never contribute a never-started pair. THIS CAN FAIL ON REAL DATA, AND IT FAILS IN THE DIRECTION OF THE RESULT (decisions/0076).

**Population:** THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 SS3) -- every distinct account the Step 4 pull touched, not the accounts that survived into the table. The skipped classes are counted separately and the pairs they contribute are stated, so an account that was skipped and then read as empty would be visible rather than absent.

- `coverage`:
    - `population` = `every distinct account in processed/step4/pull_ledger.jsonl`
    - `unit` = `accounts`
    - `accounts_in_the_stated_population` = `2874`
    - `accounts_asserted` = `2874`
    - `accounts_not_asserted` = `0`
    - `coverage_identity` = `2874 + 0 not asserted = 2874`
    - `coverage_identity_holds` = `True`
    - `population_size_independence` = `INDEPENDENT_CODE_PATH`
    - `population_size_source` = `processed/step4/pull_ledger.jsonl, distinct `slug` counted by a line-by-line json.loads pass rather than by pandas.read_json`
    - `independent_population_size` = `2874`
    - `identity_against_the_independent_source` = `2874 + 0 not asserted = 2874`
    - `identity_against_the_independent_source_holds` = `True`
    - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
    - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step4/pull_ledger.jsonl, distinct `slug` counted by a line-by-line json.loads pass rather than by pandas.read_json, so the clauses and the denominator are not the same expression and the identity can fail.`
    - `build` = `a/2026-08-17-0096`
    - `accounts_whose_final_state_is_complete` = `2549`
    - `accounts_whose_final_state_is_a_skip_class` = `325`
    - `accounts_whose_final_state_is_neither` = `0`
    - `accounts_present_in_the_user_index` = `2549`
    - `ledger_rows_read` = `2884`
- `coverage_ledger_rows` = `2884`
- `coverage_accounts_in_the_user_index` = `2549`
- `skip_classes_present_in_the_ledger`:
    - `discarded_over_tolerance` = `287`
    - `skipped_length_forecast` = `38`
- `pairs_contributed_by_each_skip_class`:
    - `discarded_over_tolerance`:
        - `accounts` = `287`
        - `accounts_present_in_the_user_index` = `0`
        - `position_5_pairs` = `0`
        - `pairs_scored_never_started` = `0`
    - `skipped_length_forecast`:
        - `accounts` = `38`
        - `accounts_present_in_the_user_index` = `0`
        - `position_5_pairs` = `0`
        - `pairs_scored_never_started` = `0`
- `ledger_outcomes_not_classified_as_skip_or_complete` = `[]`
- `HTTP_403_responses_in_the_whole_run` = `0`
- `access_denied_accounts` = `0`
- `accounts_whose_FINAL_ledger_state_is_a_skip_class` = `325`
- `of_those_present_in_the_user_index` = `0`
- `of_those_contributing_a_position_5_pair` = `0`
- `of_those_contributing_a_pair_scored_NEVER_STARTED` = `0`
- `accounts_skipped_and_never_yielding_data` = `325`
- `those_accounts_contributing_a_NEVER_STARTED_pair` = `0`
- `accounts_skipped_on_one_attempt_but_yielding_data_on_another`:
    - `count` = `7`
    - `position_5_pairs` = `604`
    - `never_started_pairs` = `119`
    - `note` = `not a violation -- these accounts have a real parsed history and their never-started rows rest on evidence, not on absence. Reported so the assertion's scope is visible.`
- `assertion` = `no account whose final ledger state is a skip class, and no account that was skipped and never yielded data, contributes a pair scored never-started`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

### 9. no retained row's outcome window extends past tau_pull: tau2 <= tau_pull on every position-5 row

**CODE CHECK.** D10 right-censors on t0 + (max(W, 91) + H) * 24h <= tau_pull, so tau2 <= tau_pull holds for any correct censoring step and no data configuration can break it. It is what makes D11 INERT on A and A_H, which is why the per-site D11 table can report those two sites as inert by construction rather than by inspection. It fails only on a censoring term coded wrongly -- and it is NOT evidence for the liveness rule or for any outcome.

**Population:** BOTH POPULATIONS, EVERY ROW: the 196,654 APPLY position-5 row set and the 147,370 DERIV position-5 row set. The two clauses -- rows at or before tau_pull and rows after it -- are counted independently and must sum to the population, so the coverage identity is real arithmetic and not N - N = 0.

- `promoted_from` = `src/step8_a_3_table.py, where it has run as a bare assert since the first build. PROMOTED INTO THE PUBLISHED SET by decisions/0088 SS1(c) because an assertion a reader of the deliverable cannot see is not a published check.`
- `by_population`:
    - `APPLY_position_5`:
        - `population` = `APPLY, position-5 row set`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `196654`
        - `rows_asserted` = `196654`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `196654 + 0 + 0 not asserted = 196654`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3`
        - `independent_population_size` = `196654`
        - `identity_against_the_independent_source` = `196654 + 0 + 0 not asserted = 196654`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows -- the EMITTED DELIVERABLE, written by stage 3, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[196654, 0]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- `tau2 <= tau_pull` and `tau2 > tau_pull` are a set and its complement within the same mask, so they sum to the mask for any mask. The INDEPENDENT row count is what can fail.`
        - `rows_with_tau2_at_or_before_tau_pull` = `196654`
        - `rows_with_tau2_after_tau_pull` = `0`
        - `rows_with_tau2_EXACTLY_AT_tau_pull` = `20`
        - `rows_with_tau1_at_or_before_tau_pull` = `196654`
        - `the_bound_is_ATTAINED_a_ge_form_would_fail` = `True`
        - `holds` = `True`
    - `DERIV_position_5`:
        - `population` = `DERIV, position-5 row set`
        - `unit` = `rows`
        - `rows_in_the_stated_population` = `147370`
        - `rows_asserted` = `147370`
        - `rows_not_asserted` = `0`
        - `coverage_identity` = `147370 + 0 + 0 not asserted = 147370`
        - `coverage_identity_holds` = `True`
        - `population_size_independence` = `EMITTED_DELIVERABLE`
        - `population_size_source` = `processed/step8/a/analysis_table.csv.gz, rows with in_deriv = True`
        - `independent_population_size` = `147370`
        - `identity_against_the_independent_source` = `147370 + 0 + 0 not asserted = 147370`
        - `identity_against_the_independent_source_holds` = `True`
        - `identity_CAN_FAIL_ON_ANY_DATA` = `True`
        - `what_it_can_detect` = `AN INVARIANT RUN ON A POPULATION OTHER THAN THE ONE IT NAMES -- the 99-row hole decisions/0080 SS3 was written for. The population size comes from processed/step8/a/analysis_table.csv.gz, rows with in_deriv = True, so the clauses and the denominator are not the same expression and the identity can fail.`
        - `build` = `a/2026-08-17-0096`
        - `asserted_clause_counts` = `[147370, 0]`
        - `clauses_are_a_complementary_partition_of_the_population_mask` = `YES -- `tau2 <= tau_pull` and `tau2 > tau_pull` are a set and its complement within the same mask, so they sum to the mask for any mask. The INDEPENDENT row count is what can fail.`
        - `rows_with_tau2_at_or_before_tau_pull` = `147370`
        - `rows_with_tau2_after_tau_pull` = `0`
        - `rows_with_tau2_EXACTLY_AT_tau_pull` = `17`
        - `rows_with_tau1_at_or_before_tau_pull` = `147370`
        - `the_bound_is_ATTAINED_a_ge_form_would_fail` = `True`
        - `holds` = `True`
- `coverage_rows` = `196654`
- `build` = `a/2026-08-17-0096`
- **result: PASS**

---

## The 703 line is NOT an invariant

**NOT AN INVARIANT -- a POPULATION RECONCILIATION (0068).** Step 7 measured its counts on APPLY built from the Step 5 pair table rather than through positions 1-5, so this is the first place the two chains have been compared. A mismatch is a POPULATION defect before an implementation one.

| Population | Denominator | Expected | Measured | never-started | started-and-left | accounts |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **703** | 604 | 99 | 216 |
| **DERIV** | 147,370 | 99 | **99** | 0 | 99 | 73 |

*Build: every figure in this table measured on `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096; see §0.*

**It reconciles: True.** Neither superseded answer was produced — ALT's 604 on APPLY: False; ALT-MATCHED's 793 on APPLY: False.

---

## What the invariant set does and does not establish

- It establishes that **the definition on paper is the definition in the code**: the partition is exhaustive and disjoint as assigned, no filter position adds rows, no episode set exceeds its season, `A` sits inside `A_H`, `p` is a rank and not the withdrawn raw ratio, and the clock is the `max()` it is defined to be.
- It establishes **almost nothing about whether the rules are right**. 6 of these checks cannot fail on any data.
- **Three checks have force.** The clock-start check, and only because the first-pass S1 completion date is **recomputed independently from the episode records** — read back from the pipeline's own value it would prove nothing. And the two `0076` data checks, which test two named failure modes of this study rather than two properties of arithmetic: an account-level liveness filter masquerading as a pair-level one, and a skipped account silently read as a never-starter.
- **The withdrawn invariant** — "no clock start precedes an S2 premiere" — is vacuous under a finale-anchored clock and catches nothing. It is replaced by the three-part check above, whose equality clause is the part that does work.
- **What check 7 found, since a passing data check should still report what it saw:** 215 of 216 accounts touched by the exclusion hold both a live and a not-live pair, and the 1 whose position-5 pairs are all excluded held exactly one such pair (0 held more than one). The filter is pair-level in fact and not only in intent.
- **What check 8 found:** 325 accounts are recorded in a skip class (discarded_over_tolerance 287, skipped_length_forecast 38), 0 HTTP 403 responses occurred in the entire run and 0 accounts are recorded `access_denied`. **None of the skipped accounts reaches the user index at all**, so none contributes a pair of any kind, let alone a never-started one. Separately, 7 accounts were skipped on one attempt and yielded data on another; they contribute 604 position-5 pairs including 119 never-started, which rest on a real parsed history and are not violations. Reported so the assertion's scope is visible rather than assumed.


*Every result in this report was measured on build `a/2026-08-17-0096` — position-5 build of 2026-08-17, instance `a`, run against decisions/0096 (`decisions/0079` B6). The full build record, with stage-file hashes and the git HEAD, is in `artifacts/step8-waterfall-a.md` §0 and in the `.json` beside this file.*

*Generated by `src/step8_a_6_emit.py` from `processed/step8/a/invariants.json`.*
