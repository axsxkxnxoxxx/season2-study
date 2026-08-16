# Step 8 — invariant report, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** · **H = 91 days** · **Zero API calls** · **Counts only**

> **RERUN AGAINST `decisions/0085`, ordered by the Human Lead — a rerun, not an amendment.** The previous `-a` invariant report was **not patched**; nothing in it is read or carried. **Every result below is produced by one pipeline run.** **`0085` adds no invariant**: its §7 leaves B3 — the half-open UTC-instant form and D11 as a global cutoff — **carried and open, and that is a Human Lead ruling, so neither was added here.** The two rulings that reach this report are structural rather than numerical. **`0079` B6: every invariant result names the build it was measured on** — build `a/2026-08-16-0085`, defined in full in the waterfall deliverable §0. **`0080` §3: every invariant names the population it runs on and accounts for every row in it**, reporting `rows_asserted + rows_not_asserted = rows_in_the_stated_population`. **`0081` and `0082` change the column set, not the invariant set: no invariant result moves.**

> **Why that second one matters, in this report's own numbers.** `0080` §3 records that in the previous dual run one arm asserted `p` on **19,042** rows — the *post-liveness* Started-and-left count — against a *pre-liveness* non-S&L clause of **177,513**, summing to **196,555 against a 196,654-row table**. **99 rows were covered by neither clause, and those 99 are exactly the started-and-left liveness exclusions.** Neither report disclosed the gap and no control could see it. **This report states both clauses and their sum for every check** — see the coverage table below, where `p` reads **19,141 + 177,513 = 196,654** and the post-liveness 19,042 appears only as a labelled contrast.

> **EVERY INVARIANT CARRIES A LABEL** (`decisions/0068`). **A code check catches an implementation that computed something wrongly; it cannot fail on any data, and it is NOT evidence for the rule.** A report saying "all invariants passed" overstates what was verified unless it names which ones could have failed.

**Result: 8 checks ran and all passed.** **5 cannot fail on any data** (CODE CHECK); **1 is a code check by construction with force only as specified**; and **2 CAN FAIL ON REAL DATA** (DATA CHECK). The 703 line is **not an invariant** and is reported separately below as a population reconciliation.

**This set is eight, and it was six until `decisions/0076`.** That entry corrected `p` from DATA CHECK to **CODE CHECK** — the label this instance's previous deliverable already carried, and the correction *inverts* the published figure: on the pre-`0076` set the true count was **five of six unfalsifiable with ZERO pure data checks**, not "four of six". `0076` then added the two checks that can actually fail, **because the set had none**. **Neither of those two is a formality here**: check 7 separates a pair-level liveness implementation from an account-level one, which the 703-from-216-accounts figure alone cannot do, and check 8 is the one that would fail *in the direction of the result*.

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
| 7 | no account is dropped wholesale by the pair-level li… | BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 SS3): the accounts holding a position-5 pair in APPLY and the accounts holding one in DERIV, each report | APPLY_position_5 — `2422 + 0 not asserted = 2422`; DERIV_position_5 — `2402 + 0 not asserted = 2402` |
| 8 | no access_denied or otherwise skipped account is rea… | THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 SS3) -- every distinct account the Step 4 pull touched, not the accounts that survived into the t | coverage — `2874 + 0 not asserted = 2874` |

**13 coverage identities were checked and all hold: True.** The run asserts this, so a report that omitted a population could not be written by this pipeline. Build: every count in this table measured on `a/2026-08-16-0085` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0085 (Red Team third pass: B1, B2, P4 and the line-6 decomposition). The earlier 2026-08-16 build of this instance is the one 0085 reviewed; no figure moves between them, but they are different builds and are tagged apart.; see §0.

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
        - `build` = `a/2026-08-16-0085`
        - `asserted_clause_counts` = `[32769, 19042, 144140]`
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
        - `build` = `a/2026-08-16-0085`
        - `asserted_clause_counts` = `[33373, 19141, 144140]`
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
        - `build` = `a/2026-08-16-0085`
        - `asserted_clause_counts` = `[9145, 16744, 121382]`
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
        - `build` = `a/2026-08-16-0085`
        - `asserted_clause_counts` = `[9145, 16843, 121382]`
        - `exactly_one_state_per_row` = `True`
        - `never_started` = `9145`
        - `started_and_left` = `16843`
        - `continued` = `121382`
        - `sum_of_the_three` = `147370`
        - `sum_equals_row_set` = `True`
        - `holds` = `True`
- `coverage_identity_holds_on_every_stated_population` = `True`
- `build` = `a/2026-08-16-0085`
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
    - `build` = `a/2026-08-16-0085`
- `coverage_DERIV`:
    - `population` = `DERIV's seven filter positions`
    - `unit` = `positions`
    - `positions_in_the_stated_population` = `7`
    - `positions_asserted` = `7`
    - `positions_not_asserted` = `0`
    - `coverage_identity` = `7 + 0 not asserted = 7`
    - `coverage_identity_holds` = `True`
    - `build` = `a/2026-08-16-0085`
- `chain_note` = `chain[i] is the count after filter position i+1; the transition from entry i to entry i+1 is the effect of filter position i+2`
- `filter_positions_removing_exactly_zero_APPLY` = `[2, 3, 7]`
- `filter_positions_removing_exactly_zero_DERIV` = `[2, 3, 7]`
- `inert_positions_labelled_not_silent` = `positions 1, 2, 3 and 7 remove 0 BY CONSTRUCTION and are labelled inert with the reason in the waterfall deliverable (decisions/0079 SS4). An unlabelled always-zero filter reads as evidence the rule FOUND NOTHING when it is evidence the rule CANNOT FIRE.`
- `build` = `a/2026-08-16-0085`
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
    - `build` = `a/2026-08-16-0085`
    - `records_examined` = `6065704`
    - `records_dropped_by_the_rule` = `0`
    - `seasons_asserted` = `['S1', 'S2']`
    - `distinct_episode_rows_asserted_S1` = `2860465`
    - `distinct_episode_rows_asserted_S2` = `2489811`
- `max_D1_minus_L1` = `0`
- `max_D2_minus_L2` = `0`
- `max_AH_minus_L2` = `0`
- `build` = `a/2026-08-16-0085`
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
    - `build` = `a/2026-08-16-0085`
- `rows_where_A_exceeds_A_H` = `0`
- `rows_where_max_A_exceeds_max_A_H` = `0`
- `also_holds_on_the_post_position_7_row_set` = `True`
- `build` = `a/2026-08-16-0085`
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
    - `build` = `a/2026-08-16-0085`
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
- `build` = `a/2026-08-16-0085`
- **result: PASS**

### 6. p lies in (0, 1] on every Started-and-left row and is null everywhere else

**CODE CHECK.** SPECIFIED by decisions/0074 ruling 2; LABEL CORRECTED from DATA CHECK to CODE CHECK by decisions/0076 on both instances' own proof. Started-and-left requires |A| >= 1, so max(A_H) exists; set membership bounds the rank numerator in [1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has a gap. It is kept because Step 10 publishes p -- but it proves the code, not the rule.

**Population:** ALL Started-and-left rows AT POSITION 5, null on the rest, and the two clauses must sum to 196,654 EXACTLY (decisions/0080 SS3). THIS IS THE IDENTITY THAT CLOSES THE HOLE: the dual run had one arm assert p on 19,042 rows -- the POST-LIVENESS Started-and-left count -- against a PRE-LIVENESS denominator of 177,513 non-S&L rows, leaving 99 rows covered by neither clause, exactly the started-and-left liveness exclusions. Do not take the numerator post-liveness and the denominator pre-liveness.

- `coverage_rows` = `19141`
- `coverage`:
    - `population` = `APPLY, position 5 -- the analysis table's row set`
    - `unit` = `rows`
    - `rows_in_the_stated_population` = `196654`
    - `rows_asserted` = `196654`
    - `rows_not_asserted` = `0`
    - `coverage_identity` = `19141 + 177513 + 0 not asserted = 196654`
    - `coverage_identity_holds` = `True`
    - `build` = `a/2026-08-16-0085`
    - `asserted_clause_counts` = `[19141, 177513]`
    - `clause_1_rows_asserted_p_in_0_1_started_and_left` = `19141`
    - `clause_2_rows_asserted_p_is_null_not_started_and_left` = `177513`
    - `started_and_left_post_liveness_for_contrast_NOT_the_numerator` = `19042`
- `min` = `0.038461538461538464`
- `max` = `1.0`
- `nulls_among_started_and_left` = `0`
- `non_null_outside_started_and_left` = `0`
- `build` = `a/2026-08-16-0085`
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
        - `coverage_identity` = `2422 + 0 not asserted = 2422`
        - `coverage_identity_holds` = `True`
        - `build` = `a/2026-08-16-0085`
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
        - `coverage_identity` = `2402 + 0 not asserted = 2402`
        - `coverage_identity_holds` = `True`
        - `build` = `a/2026-08-16-0085`
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
- `build` = `a/2026-08-16-0085`
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
    - `build` = `a/2026-08-16-0085`
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
- `build` = `a/2026-08-16-0085`
- **result: PASS**

---

## The 703 line is NOT an invariant

**NOT AN INVARIANT -- a POPULATION RECONCILIATION (0068).** Step 7 measured its counts on APPLY built from the Step 5 pair table rather than through positions 1-5, so this is the first place the two chains have been compared. A mismatch is a POPULATION defect before an implementation one.

| Population | Denominator | Expected | Measured | never-started | started-and-left | accounts |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **703** | 604 | 99 | 216 |
| **DERIV** | 147,370 | 99 | **99** | 0 | 99 | 73 |

*Build: every figure in this table measured on `a/2026-08-16-0085` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0085 (Red Team third pass: B1, B2, P4 and the line-6 decomposition). The earlier 2026-08-16 build of this instance is the one 0085 reviewed; no figure moves between them, but they are different builds and are tagged apart.; see §0.*

**It reconciles: True.** Neither superseded answer was produced — ALT's 604 on APPLY: False; ALT-MATCHED's 793 on APPLY: False.

---

## What the invariant set does and does not establish

- It establishes that **the definition on paper is the definition in the code**: the partition is exhaustive and disjoint as assigned, no filter position adds rows, no episode set exceeds its season, `A` sits inside `A_H`, `p` is a rank and not the withdrawn raw ratio, and the clock is the `max()` it is defined to be.
- It establishes **almost nothing about whether the rules are right**. 5 of these checks cannot fail on any data.
- **Three checks have force.** The clock-start check, and only because the first-pass S1 completion date is **recomputed independently from the episode records** — read back from the pipeline's own value it would prove nothing. And the two `0076` data checks, which test two named failure modes of this study rather than two properties of arithmetic: an account-level liveness filter masquerading as a pair-level one, and a skipped account silently read as a never-starter.
- **The withdrawn invariant** — "no clock start precedes an S2 premiere" — is vacuous under a finale-anchored clock and catches nothing. It is replaced by the three-part check above, whose equality clause is the part that does work.
- **What check 7 found, since a passing data check should still report what it saw:** 215 of 216 accounts touched by the exclusion hold both a live and a not-live pair, and the 1 whose position-5 pairs are all excluded held exactly one such pair (0 held more than one). The filter is pair-level in fact and not only in intent.
- **What check 8 found:** 325 accounts are recorded in a skip class (discarded_over_tolerance 287, skipped_length_forecast 38), 0 HTTP 403 responses occurred in the entire run and 0 accounts are recorded `access_denied`. **None of the skipped accounts reaches the user index at all**, so none contributes a pair of any kind, let alone a never-started one. Separately, 7 accounts were skipped on one attempt and yielded data on another; they contribute 604 position-5 pairs including 119 never-started, which rest on a real parsed history and are not violations. Reported so the assertion's scope is visible rather than assumed.


*Every result in this report was measured on build `a/2026-08-16-0085` — position-5 build of 2026-08-16, instance `a`, RERUN against decisions/0085 (Red Team third pass: B1, B2, P4 and the line-6 decomposition). The earlier 2026-08-16 build of this instance is the one 0085 reviewed; no figure moves between them, but they are different builds and are tagged apart. (`decisions/0079` B6). The full build record, with stage-file hashes and the git HEAD, is in `artifacts/step8-waterfall-a.md` §0 and in the `.json` beside this file.*

*Generated by `src/step8_a_6_emit.py` from `processed/step8/a/invariants.json`.*
