# Step 8 — invariant report (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**This is the CLEAN RERUN ordered by the Human Lead**, on `task-sheet.md` Step 8 as it now stands — the spec as amended through `decisions/0082`. **A previous attempt was terminated after writing its deliverables and before either arm confirmed them; all of its output was discarded and this run was built from the committed state.** Against this arm's last confirmed deliverables the executable changes are `0081` (**`silent_at_tau1` restored**) and `0082` (**`p_at_bound` added**), which together take the enumerated column set from 87 to **89**; everything else — `0078`'s provenance rule, `0079`'s pipeline-produced drop set and inert-position labels, `0080`'s per-invariant coverage populations — is re-executed rather than assumed. This overwrites the previous `-b` deliverables.

**Provenance — `analytics-engineer-b / Step 8 position-5 build of 2026-08-16 (CLEAN RERUN on the spec as amended through decisions/0082; W = 108, tau_pull = 2026-08-11T00:00:00Z, mandated filter order 1-7, 89 columns)`.** Every count, every waterfall figure and every invariant result below was measured on that build (`0078`, `0079` §2). Where a figure is quoted from a ruling, the ruling's own build is named instead: `position-5 build of 2026-08-13 (both arms, the run decisions/0078 labelled)`. **A count without its provenance can be correct when written and wrong when read.**

## How to read this report

**SIX of the eight assertions CANNOT FAIL ON ANY DATA. Five are pure CODE CHECKS -- the outcome partition, the monotone filter counts, |D| <= L, A subset of A_H, and p in (0, 1]. A sixth, the clock start, is a code check by construction and a genuine cross-check only because the first-pass S1 completion date is recomputed INDEPENDENTLY here. TWO can fail on real data, and both were added by decisions/0076 because before it the set had ZERO: no account dropped wholesale, and no access_denied or skipped account read as empty. 'All invariants passed' is therefore mostly a statement that the code computed what it was told to; it is NOT evidence for the liveness rule or for any published share.**

Counts: **5 pure code checks**, **1 that is a code check by construction and a genuine cross-check as specified**, and **2 that can fail on real data** — both added by `decisions/0076`, because before it the set had **zero**. **2 further items are reported and NOT asserted**: the set-membership drop rule, which is a coverage count (`0074` ruling 3), and the 703 expectation, which is a population reconciliation.

## Coverage — every invariant names its population and accounts for every row in it

**`0080` §3.** An invariant that passes on one population and was never run on another READS AS A PASS ON BOTH, and a passing invariant whose coverage the instance chose is a code check on the instance's choice.

**Every invariant below reports `rows_asserted + rows_not_asserted = rows_in_the_stated_population`, and the identity holds: True.**

**The gap this arm had, stated plainly rather than quietly fixed.** This arm's previous run asserted p on 19,042 rows (post-liveness) with a non-S&L clause on 177,513 (position-5), summing to 196,555 against a 196,654-row table. 99 rows -- exactly the started-and-left liveness exclusions -- were covered by NEITHER clause, and the report did not disclose it. Closed this run: 19,141 + 177,513 = 196,654.

| # | Invariant | Label | Stated population | Coverage | Result |
| :-- | :--- | :--- | :--- | :--- | :--- |
| 1 | outcome states are mutually exclusive and sum to the POST- | **CODE CHECK** | BOTH ROW SETS ON BOTH POPULATIONS (decisions/0080 Sec 3, row 1): the 196,654 A… | APPLY_position5_row_set: 196,654 + 0 = 196,654; APPLY_post_position_7_live_subset: 195,951 + 0 = 195,951; DERIV_position5_row_set: 147,370 + 0 = 147,370; DERIV_post_position_7_live_subset: 147,271 + 0 = 147,271 | **PASS** |
| 2 | filter counts decrease monotonically -- CODED AS `>=`, NOT | **CODE CHECK** | BOTH CHAINS (decisions/0080 Sec 3, row 2): APPLY's seven positions and DERIV's… | 7 positions on each chain, 6 transitions asserted on each | **PASS** |
| 3 | distinct episodes never exceed season length (|D| <= L) | **CODE CHECK** | BOTH SEASONS, every pair the set-membership rule examines (decisions/0080 Sec … | 278,452 pairs × both seasons, 6,065,610 records | **PASS** |
| 4 | A is a subset of A_H on every row | **CODE CHECK** | the 196,654 APPLY position-5 row set, EVERY ROW (decisions/0080 Sec 3, row 4) | 196,654 + 0 = 196,654 rows | **PASS** |
| 5 | clock start is on or after the S2 finale date, on or after | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** | the 196,654 APPLY position-5 row set, EVERY ROW, with the first-pass S1 comple… | 196,654 + 0 = 196,654 rows | **PASS** |
| 6 | abandonment point p is in (0, 1] on every Started-and-left | **CODE CHECK** | ALL Started-and-left rows AT POSITION 5, null on the rest -- and the two must … | 19,141 + 0 + 177,513 = 196,654 rows | **PASS** |
| 7 | NO ACCOUNT IS DROPPED WHOLESALE BY THE PAIR-LEVEL LIVENESS | **DATA CHECK** | BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 Sec 3, row 7): the accounts in A… | APPLY: 2,422 + 0 = 2,422 accounts; DERIV: 2,402 + 0 = 2,402 accounts | **PASS** |
| 8 | NO access_denied OR SKIPPED ACCOUNT IS READ AS EMPTY -- no | **DATA CHECK** | THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 Sec 3, row 8), with the s… | 2,874 + 0 = 2,874 accounts | **PASS** |

**All invariants pass: True.** For six of the eight that statement says the code computed what it was told to. It is **not** evidence for the liveness rule, for the outcome definition, or for any published share. **The two that could have failed are §7 and §8, and what they found is reported in full below rather than as a tick.**

## 1. outcome states are mutually exclusive and sum to the POST-POSITION-7 row set

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK.** Step 1 Sec 7's partition A = empty / (A non-empty and C_H) / (A non-empty and not C_H) is proved exhaustive and disjoint, so this can only catch an assignment coded wrongly -- e.g. dropping the |A| >= 1 conjunct from Continued, which would put a day-150 starter completing by day 190 in two states at once.

**Population (`0080` §3):** BOTH ROW SETS ON BOTH POPULATIONS (decisions/0080 Sec 3, row 1): the 196,654 APPLY position-5 row set the table carries AND the 195,951 post-position-7 live subset, and the DERIV pair 147,370 / 147,271. Neither substitutes for the other -- an invariant that passes on one population and was never run on another READS AS A PASS ON BOTH.

**coverage**

```json
{
  "unit": "rows",
  "identity_required": "rows_asserted + rows_not_asserted = rows_in_the_stated_population",
  "holds_on_every_stated_population": true
}
```

**result**

```json
{
  "APPLY_position5_row_set": {
    "rows_in_the_stated_population": 196654,
    "never_started": 33373,
    "continued": 144140,
    "started_and_left": 19141,
    "sum": 196654,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "rows_asserted": 196654,
    "rows_not_asserted": 0,
    "coverage_identity_holds": true,
    "passes": true
  },
  "APPLY_post_position_7_live_subset": {
    "rows_in_the_stated_population": 195951,
    "never_started": 32769,
    "continued": 144140,
    "started_and_left": 19042,
    "sum": 195951,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "rows_asserted": 195951,
    "rows_not_asserted": 0,
    "coverage_identity_holds": true,
    "passes": true
  },
  "DERIV_position5_row_set": {
    "rows_in_the_stated_population": 147370,
    "never_started": 9145,
    "continued": 121382,
    "started_and_left": 16843,
    "sum": 147370,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "rows_asserted": 147370,
    "rows_not_asserted": 0,
    "coverage_identity_holds": true,
    "passes": true
  },
  "DERIV_post_position_7_live_subset": {
    "rows_in_the_stated_population": 147271,
    "never_started": 9145,
    "continued": 121382,
    "started_and_left": 16744,
    "sum": 147271,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "rows_asserted": 147271,
    "rows_not_asserted": 0,
    "coverage_identity_holds": true,
    "passes": true
  }
}
```

**Result: PASS.**

## 2. filter counts decrease monotonically -- CODED AS `>=`, NOT `>`

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK.** filters only remove rows, so this fails only on an implementation that ADDS them -- a duplicating join, most likely.

**Population (`0080` §3):** BOTH CHAINS (decisions/0080 Sec 3, row 2): APPLY's seven positions and DERIV's seven.

**Why `>=` and not `>`:** the invariant must not encode a property of one rule: a filter position that legitimately removes nothing must not fail an assertion. It is load-bearing IN FACT here -- position 2 removes exactly 0 pairs on this frame, and so does position 3.

- APPLY sequence: [220107, 220107, 220107, 201900, 196654, 195951, 195951]
- DERIV sequence: [220107, 220107, 220107, 152126, 147370, 147271, 147271]
- Positions removing exactly zero on APPLY: [2, 3, 7] — **the four inert positions**, labelled in `artifacts/step8-waterfall-b.md` §1

**coverage**

```json
{
  "unit": "filter positions",
  "APPLY": {
    "positions_in_the_chain": 7,
    "transitions_asserted": 6,
    "transitions_not_asserted": 0
  },
  "DERIV": {
    "positions_in_the_chain": 7,
    "transitions_asserted": 6,
    "transitions_not_asserted": 0
  },
  "identity_holds": true
}
```

**Result: PASS.**

## 3. distinct episodes never exceed season length (|D| <= L)

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK.** Step 8's own set-membership drop rule already establishes |D| <= L by construction -- an episode whose number is not in the season's listed set E is dropped, so D is a subset of E. It fails only if an implementation filtered by the numeric RANGE 1..F instead of by membership in E.

**Population (`0080` §3):** BOTH SEASONS, every pair the set-membership rule examines (decisions/0080 Sec 3, row 3). The narrower reading -- S2 only on the 196,654 table rows -- DOES NOT SUBSTITUTE and is reported as a subset below, not as the check.

**coverage**

```json
{
  "unit": "pairs, and the records behind them",
  "pairs_in_the_stated_population": 278452,
  "pairs_asserted_S1": 278452,
  "pairs_asserted_S2": 278452,
  "pairs_not_asserted": 0,
  "identity_holds": true,
  "records_examined_by_the_set_membership_rule": 6065610,
  "pairs_examined_by_the_set_membership_rule": 278452,
  "records_dropped": 0
}
```

**checked**

```json
{
  "S1_pairs_violating_|D1|_>_L1": 0,
  "S2_pairs_violating_|D2|_>_L2": 0,
  "max_|D1|_minus_L1": 0,
  "max_|D2|_minus_L2": 0,
  "narrower_reading_reported_not_substituted": {
    "rows_examined": 196654,
    "rows_violating_|A_H|_>_L2": 0,
    "max_|A_H|_minus_L2": 0,
    "rows_with_|A|_>_|A_H|": 0
  }
}
```

**Result: PASS.**

## 4. A is a subset of A_H on every row

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK.** true by construction since tau1 < tau2 and both sets are prefixes of the same instant-ordered episode list; it can only catch the two sets being computed from different evidence, or tau2 computed below tau1.

**Population (`0080` §3):** the 196,654 APPLY position-5 row set, EVERY ROW (decisions/0080 Sec 3, row 4).

**coverage**

```json
{
  "unit": "rows",
  "rows_in_the_stated_population": 196654,
  "rows_asserted": 196654,
  "rows_not_asserted": 0,
  "identity_holds": true
}
```

**checked**

```json
{
  "rows_examined": 196654,
  "rows_with_|A|_>_|A_H|": 0,
  "rows_with_tau2_<=_tau1": 0
}
```

**Result: PASS.**

## 5. clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equals one of those two

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.** the first-pass S1 completion date is RECOMPUTED here by a second, independent implementation -- a literal per-pair walk over the records, not the vectorised rank computation the pipeline uses, and not read back from any stored value. Read back rather than recomputed it degrades to a code check and proves nothing, because T0 = max() makes all three clauses true of any correct max().

**Population (`0080` §3):** the 196,654 APPLY position-5 row set, EVERY ROW, with the first-pass S1 completion date RECOMPUTED INDEPENDENTLY -- which is the only thing giving this one force (decisions/0080 Sec 3, row 5).

**coverage**

```json
{
  "unit": "rows",
  "rows_in_the_stated_population": 196654,
  "rows_asserted": 196654,
  "rows_not_asserted": 0,
  "rows_not_asserted_reason": "rows the independent walk does not complete; if this is non-zero the two implementations disagree on the completer SET and that is itself the finding",
  "identity_holds": true
}
```

**independent recomputation**

```json
{
  "pairs_the_independent_walk_completes": 220107,
  "line_1_pairs": 220107,
  "line_1_pairs_the_walk_also_completes": 220107,
  "line_1_pairs_the_walk_does_NOT_complete": 0,
  "agreement_on_the_completion_DATE": 220107,
  "disagreements": 0,
  "set_identity": "the two implementations return the SAME (user, show) key set -- checked as a set, not only as a count"
}
```

**clauses on the position 5 population**

```json
{
  "rows_examined": 196654,
  "T0_on_or_after_the_S2_finale_date": 196654,
  "T0_on_or_after_the_first_pass_S1_completion_date": 196654,
  "T0_equals_one_of_the_two": 196654,
  "violations": 0
}
```

**the equality clause cannot discriminate on**

```json
{
  "rows_where_the_two_terms_are_the_same_date": 168,
  "why": "for those rows the invariant cannot tell a first-pass implementation from a last-observed one"
}
```

**Result: PASS.**

## 6. abandonment point p is in (0, 1] on every Started-and-left row, null elsewhere

*Measured on: b: position-5 build of 2026-08-16.*

**Label: CODE CHECK.** Started-and-left requires |A| >= 1, so m_H exists; and set membership makes A_H a subset of E2, so the rank numerator |{e in E2 : e <= m_H}| lies in [1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the withdrawn raw-ratio form p = m_H / L2, which can exceed 1 where S2 numbering has a gap.

**Population (`0080` §3):** ALL Started-and-left rows AT POSITION 5, null on the rest -- and the two must sum to the 196,654 position-5 row set EXACTLY (decisions/0080 Sec 3, row 6). DO NOT TAKE THE NUMERATOR POST-LIVENESS AND THE DENOMINATOR PRE-LIVENESS.

**On the label:** decisions/0074 specified this invariant and labelled it DATA CHECK; decisions/0076 CORRECTED the label to CODE CHECK on both instances' own proof. This instance labelled it a code check before the correction and states the same proof.

**coverage**

```json
{
  "unit": "rows",
  "rows_in_the_stated_population": 196654,
  "rows_asserted_in_range_clause": 19141,
  "rows_asserted_null_clause": 177513,
  "rows_not_asserted": 0,
  "identity_holds": true,
  "corrected_this_run": "this arm's previous run asserted the range clause on the POST-LIVENESS 19,042 while the null clause ran on the position-5 177,513 -- 196,555 against a 196,654-row table, with 99 rows covered by NEITHER clause. Those 99 are exactly the started-and-left liveness exclusions. That gap is what decisions/0080 Sec 3 was written on, and it is closed here",
  "started_and_left_rows_post_liveness_for_reference": 19042
}
```

**checked**

```json
{
  "rows_examined": 19141,
  "min": 0.038461538461538464,
  "max": 1.0,
  "rows_out_of_range": 0,
  "rows_with_p_not_computed": 0,
  "non_started_and_left_rows_examined": 177513,
  "non_started_and_left_rows_that_are_NOT_null": 0
}
```

Form: `p = |{e in E2 : e <= m_H}| / L2, rank form, read on A_H (0034)`.

**Result: PASS.**

## 7. NO ACCOUNT IS DROPPED WHOLESALE BY THE PAIR-LEVEL LIVENESS FILTER -- the count of accounts holding BOTH a live and a not-live pair is > 0

*Measured on: b: position-5 build of 2026-08-16.*

**Label: DATA CHECK.** 703 pairs from 216 accounts is consistent with a pair-level AND an account-level implementation, and nothing in the exclusion set distinguishes them. An account-level filter would make this count exactly ZERO. CLAUDE.md and Step 7: 'One account can be live for one show and not another. Never drop a user wholesale.' This can fail on real data.

**Population (`0080` §3):** BOTH POPULATIONS, IN ACCOUNTS (decisions/0080 Sec 3, row 7): the accounts in APPLY's position-5 row set and the accounts in DERIV's, each reporting accounts holding both a live and a not-live pair.

**coverage**

```json
{
  "unit": "accounts",
  "identity_required": "accounts_asserted + accounts_not_asserted = accounts_in_the_stated_population",
  "holds_on_both_populations": true
}
```

**checked**

```json
{
  "APPLY": {
    "accounts_in_the_stated_population": 2422,
    "accounts_asserted": 2422,
    "accounts_not_asserted": 0,
    "coverage_identity_holds": true,
    "accounts_holding_only_live_pairs": 2206,
    "pairs_in_the_stated_population": 196654,
    "accounts_supplying_at_least_one_not_live_pair": 216,
    "accounts_holding_BOTH_a_live_and_a_not_live_pair": 215,
    "accounts_all_of_whose_pairs_are_not_live": 1,
    "of_those_accounts_the_number_holding_exactly_one_pair": 1,
    "max_pairs_held_by_an_all_not_live_account": 1,
    "not_live_pairs": 703,
    "pairs_held_by_the_excluding_accounts": 15300
  },
  "DERIV": {
    "accounts_in_the_stated_population": 2402,
    "accounts_asserted": 2402,
    "accounts_not_asserted": 0,
    "coverage_identity_holds": true,
    "accounts_holding_only_live_pairs": 2329,
    "pairs_in_the_stated_population": 147370,
    "accounts_supplying_at_least_one_not_live_pair": 73,
    "accounts_holding_BOTH_a_live_and_a_not_live_pair": 72,
    "accounts_all_of_whose_pairs_are_not_live": 1,
    "of_those_accounts_the_number_holding_exactly_one_pair": 1,
    "max_pairs_held_by_an_all_not_live_account": 1,
    "not_live_pairs": 99,
    "pairs_held_by_the_excluding_accounts": 4410
  }
}
```

**Reading:** the accounts whose pairs are ALL not-live are not a counter-example: they are mostly accounts holding a single pair in the population, for which the two implementations are indistinguishable by construction.

**Result: PASS.**

## 8. NO access_denied OR SKIPPED ACCOUNT IS READ AS EMPTY -- no account recorded access_denied, over-tolerance or otherwise skipped contributes a pair scored never-started

*Measured on: b: position-5 build of 2026-08-16.*

**Label: DATA CHECK.** CLAUDE.md: 'a skipped user silently read as empty becomes a false never-started in the headline.' A join that treats an absent history as an empty one produces exactly this, and it FAILS IN THE DIRECTION OF THE RESULT, which is the worst direction available. Rule and evidence at artifacts/step0-access-and-setup.md Sec 7.

**Population (`0080` §3):** THE FULL ACCOUNT LEDGER, IN ACCOUNTS (decisions/0080 Sec 3, row 8), with the skipped classes counted separately and the pairs they contribute stated.

**coverage**

```json
{
  "unit": "accounts",
  "accounts_in_the_stated_population": 2874,
  "accounts_asserted": 2874,
  "accounts_not_asserted": 0,
  "identity_holds": true,
  "by_final_ledger_outcome": {
    "complete": {
      "accounts_in_the_ledger": 2549,
      "of_those_present_in_the_parsed_sweep": 2549,
      "pairs_contributed_to_the_APPLY_position5_population": 196654,
      "of_those_pairs_scored_NEVER_STARTED": 33373,
      "is_a_skipped_class": false
    },
    "discarded_over_tolerance": {
      "accounts_in_the_ledger": 287,
      "of_those_present_in_the_parsed_sweep": 0,
      "pairs_contributed_to_the_APPLY_position5_population": 0,
      "of_those_pairs_scored_NEVER_STARTED": 0,
      "is_a_skipped_class": true
    },
    "skipped_length_forecast": {
      "accounts_in_the_ledger": 38,
      "of_those_present_in_the_parsed_sweep": 0,
      "pairs_contributed_to_the_APPLY_position5_population": 0,
      "of_those_pairs_scored_NEVER_STARTED": 0,
      "is_a_skipped_class": true
    }
  },
  "skipped_classes_total_pairs_contributed": 0,
  "skipped_classes_total_never_started_pairs_contributed": 0,
  "a_second_class_checked_separately": {
    "parsed_accounts_with_no_ledger_row_at_all": 0,
    "why": "an account present in the parsed sweep but absent from the ledger would be covered by no ledger class, so it is counted rather than assumed empty"
  }
}
```

**checked**

```json
{
  "step4_ledger_accounts": 2874,
  "accounts_by_final_outcome": {
    "skipped_length_forecast": 38,
    "discarded_over_tolerance": 287,
    "complete": 2549
  },
  "step4_pull_log_access_denied": 0,
  "step4_pull_log_private_or_absent": 0,
  "accounts_in_the_parsed_sweep": 2549,
  "parsed_accounts_whose_final_ledger_outcome_is_NOT_complete": 0,
  "parsed_accounts_with_no_ledger_row_at_all": 0,
  "such_accounts_contributing_ANY_pair_to_the_position_5_population": 0,
  "such_accounts_contributing_a_NEVER_STARTED_pair": 0
}
```

**Reading:** zero access_denied and zero private_or_absent were recorded in the whole Step 4 pull, so the 403-skip path never fired. The skipped and over-tolerance accounts DO exist -- 287 discarded over tolerance and 38 skipped on the length forecast -- and none of them is parsed, indexed or present in the table. They are ABSENT, not empty, which is what the rule requires.

**Result: PASS.**

## What the two data checks actually found

*Measured on: b: position-5 build of 2026-08-16.*

**Wholesale dropping.** On APPLY, **215 of the 216 accounts that supply a liveness exclusion also keep at least one live pair**; on DERIV, **72 of 73**. An account-level filter would make both numbers exactly zero, so this discriminates between the two implementations, which the 703-from-216 figure alone does not. The single account whose pairs are all not-live holds exactly one pair in the population, where the two implementations are indistinguishable by construction.

**Skipped accounts read as empty.** Zero `access_denied` and zero `private_or_absent` were recorded across the whole Step 4 pull, so the 403-skip path never fired. The skipped accounts nevertheless exist, and `0080` §3 requires them counted **separately, in accounts, with the pairs they contribute stated**:

| Final ledger outcome | Accounts | Present in the parsed sweep | Pairs contributed | of those, never-started |
| :--- | ---: | ---: | ---: | ---: |
| `complete` | 2,549 | 2,549 | 196,654 | 33,373 |
| `discarded_over_tolerance` — **skipped class** | 287 | 0 | 0 | 0 |
| `skipped_length_forecast` — **skipped class** | 38 | 0 | 0 | 0 |

**2,874 of 2,874 ledger accounts asserted, 0 not** — and 0 parsed accounts have no ledger row at all, counted separately so that no account is covered by no class. **The skipped classes contribute 0 pairs and 0 never-started pairs.** They are **absent, not empty**, which is what the rule requires — and this is the one check that **fails in the direction of the result** if it fails.

## Reported and NOT asserted (1) — the set-membership drop rule

*Measured on: b: position-5 build of 2026-08-16.*

A COVERAGE COUNT, NOT AN INVARIANT (decisions/0074 ruling 3). Step 8's own bullet calls it 'an implementation check, not a data check'. Reported, not asserted -- asserting it would add another pass to a report where six of eight cannot fail on data.

- Records examined: **6,065,610**
- Records dropped: **0**

The denominator has three readings on this data and `0074` ruling 4 publishes two of them unreconciled; all three are tabulated in `artifacts/step8-waterfall-b.md` §6.

## Reported and NOT asserted (2) — the 703 expectation

*Measured on: b: position-5 build of 2026-08-16.*

It is a POPULATION RECONCILIATION, and the spec's own instruction to suspect the population before the implementation is what makes it one.

| Population | Denominator | Expected | Measured | Expected split | Measured split | Expected accounts | Measured accounts |
| :--- | ---: | ---: | ---: | :--- | :--- | ---: | ---: |
| APPLY | 196,654 | 703 | 703 | [604, 99] | [604, 99] | 216 | 216 |
| DERIV | 147,370 | 99 | 99 | [0, 99] | [0, 99] | 73 | 73 |

**Reconciles: True.** Neither superseded answer was produced — not **604** (ALT) and not **793** (ALT-MATCHED, withdrawn). Had the count differed, the spec's own instruction is to treat it as a **population** defect before an implementation one; the population was in fact re-derived through positions 1–5 and reproduces 196,654 and 147,370 exactly.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
