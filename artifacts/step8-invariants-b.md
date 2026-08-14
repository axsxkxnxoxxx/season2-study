# Step 8 — invariant report (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

**This is the RERUN ordered by the Human Lead on `decisions/0077`, which no arm had executed against.** `0077` fixes the discovery-channel overlap's missing population, restates `0075` ruling 2 — which named an empty set, since position 3 removes zero rows — and fixes the column names. `0074`, `0075` and `0076` postdate the first run and are also carried. This overwrites the previous `-b` deliverables.

## How to read this report

**SIX of the eight assertions CANNOT FAIL ON ANY DATA. Five are pure CODE CHECKS -- the outcome partition, the monotone filter counts, |D| <= L, A subset of A_H, and p in (0, 1]. A sixth, the clock start, is a code check by construction and a genuine cross-check only because the first-pass S1 completion date is recomputed INDEPENDENTLY here. TWO can fail on real data, and both were added by decisions/0076 because before it the set had ZERO: no account dropped wholesale, and no access_denied or skipped account read as empty. 'All invariants passed' is therefore mostly a statement that the code computed what it was told to; it is NOT evidence for the liveness rule or for any published share.**

Counts: **5 pure code checks**, **1 that is a code check by construction and a genuine cross-check as specified**, and **2 that can fail on real data** — both added by `decisions/0076`, because before it the set had **zero**. **2 further items are reported and NOT asserted**: the set-membership drop rule, which is a coverage count (`0074` ruling 3), and the 703 expectation, which is a population reconciliation.

| # | Invariant | Label | Result |
| :-- | :--- | :--- | :--- |
| 1 | outcome states are mutually exclusive and sum to the POST-POSITION-7 row set | **CODE CHECK** | **PASS** |
| 2 | filter counts decrease monotonically -- CODED AS `>=`, NOT `>` | **CODE CHECK** | **PASS** |
| 3 | distinct episodes never exceed season length (|D| <= L) | **CODE CHECK** | **PASS** |
| 4 | A is a subset of A_H on every row | **CODE CHECK** | **PASS** |
| 5 | clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equals one of those two | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** | **PASS** |
| 6 | abandonment point p is in (0, 1] on every Started-and-left row, null elsewhere | **CODE CHECK** | **PASS** |
| 7 | NO ACCOUNT IS DROPPED WHOLESALE BY THE PAIR-LEVEL LIVENESS FILTER -- the count of accounts holding BOTH a live and a not-live pair is > 0 | **DATA CHECK** | **PASS** |
| 8 | NO access_denied OR SKIPPED ACCOUNT IS READ AS EMPTY -- no account recorded access_denied, over-tolerance or otherwise skipped contributes a pair scored never-started | **DATA CHECK** | **PASS** |

**All invariants pass: True.** For six of the eight that statement says the code computed what it was told to. It is **not** evidence for the liveness rule, for the outcome definition, or for any published share. **The two that could have failed are §7 and §8, and what they found is reported in full below rather than as a tick.**

## 1. outcome states are mutually exclusive and sum to the POST-POSITION-7 row set

**Label: CODE CHECK.** Step 1 Sec 7's partition A = empty / (A non-empty and C_H) / (A non-empty and not C_H) is proved exhaustive and disjoint, so this can only catch an assignment coded wrongly -- e.g. dropping the |A| >= 1 conjunct from Continued, which would put a day-150 starter completing by day 190 in two states at once.

**result**

```json
{
  "APPLY": {
    "post_position_7_rows": 195951,
    "never_started": 32769,
    "continued": 144140,
    "started_and_left": 19042,
    "sum": 195951,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "passes": true
  },
  "DERIV": {
    "post_position_7_rows": 147271,
    "never_started": 9145,
    "continued": 121382,
    "started_and_left": 16744,
    "sum": 147271,
    "rows_in_two_states": 0,
    "rows_in_no_state": 0,
    "passes": true
  }
}
```

**Result: PASS.**

## 2. filter counts decrease monotonically -- CODED AS `>=`, NOT `>`

**Label: CODE CHECK.** filters only remove rows, so this fails only on an implementation that ADDS them -- a duplicating join, most likely.

**Why `>=` and not `>`:** the invariant must not encode a property of one rule: a filter position that legitimately removes nothing must not fail an assertion. It is load-bearing IN FACT here -- position 2 removes exactly 0 pairs on this frame, and so does position 3.

- APPLY sequence: [220107, 220107, 220107, 201900, 196654, 195951, 195951]
- DERIV sequence: [220107, 220107, 220107, 152126, 147370, 147271, 147271]
- Positions removing exactly zero on APPLY: [2, 3, 7]

**Result: PASS.**

## 3. distinct episodes never exceed season length (|D| <= L)

**Label: CODE CHECK.** Step 8's own set-membership drop rule already establishes |D| <= L by construction -- an episode whose number is not in the season's listed set E is dropped, so D is a subset of E. It fails only if an implementation filtered by the numeric RANGE 1..F instead of by membership in E.

**checked**

```json
{
  "max_|A_H|_minus_L2": 0,
  "rows_violating": 0,
  "rows_examined": 196654
}
```

**Result: PASS.**

## 4. A is a subset of A_H on every row

**Label: CODE CHECK.** true by construction since tau1 < tau2 and both sets are prefixes of the same instant-ordered episode list; it can only catch the two sets being computed from different evidence, or tau2 computed below tau1.

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

**Label: CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.** the first-pass S1 completion date is RECOMPUTED here by a second, independent implementation -- a literal per-pair walk over the records, not the vectorised rank computation the pipeline uses, and not read back from any stored value. Read back rather than recomputed it degrades to a code check and proves nothing, because T0 = max() makes all three clauses true of any correct max().

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

**Label: CODE CHECK.** Started-and-left requires |A| >= 1, so m_H exists; and set membership makes A_H a subset of E2, so the rank numerator |{e in E2 : e <= m_H}| lies in [1, L2]. NO data configuration puts p outside (0, 1]. It fails only on the withdrawn raw-ratio form p = m_H / L2, which can exceed 1 where S2 numbering has a gap.

**On the label:** decisions/0074 specified this invariant and labelled it DATA CHECK; decisions/0076 CORRECTED the label to CODE CHECK on both instances' own proof. This instance labelled it a code check before the correction and states the same proof.

**checked**

```json
{
  "rows_examined": 19042,
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

**Label: DATA CHECK.** 703 pairs from 216 accounts is consistent with a pair-level AND an account-level implementation, and nothing in the exclusion set distinguishes them. An account-level filter would make this count exactly ZERO. CLAUDE.md and Step 7: 'One account can be live for one show and not another. Never drop a user wholesale.' This can fail on real data.

**checked**

```json
{
  "APPLY": {
    "accounts_supplying_at_least_one_not_live_pair": 216,
    "accounts_holding_BOTH_a_live_and_a_not_live_pair": 215,
    "accounts_all_of_whose_pairs_are_not_live": 1,
    "of_those_accounts_the_number_holding_exactly_one_pair": 1,
    "max_pairs_held_by_an_all_not_live_account": 1,
    "not_live_pairs": 703,
    "pairs_held_by_the_excluding_accounts": 15300
  },
  "DERIV": {
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

**Label: DATA CHECK.** CLAUDE.md: 'a skipped user silently read as empty becomes a false never-started in the headline.' A join that treats an absent history as an empty one produces exactly this, and it FAILS IN THE DIRECTION OF THE RESULT, which is the worst direction available. Rule and evidence at artifacts/step0-access-and-setup.md Sec 7.

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

**Wholesale dropping.** On APPLY, **215 of the 216 accounts that supply a liveness exclusion also keep at least one live pair.** An account-level filter would make that number exactly zero, so this discriminates between the two implementations, which the 703-from-216 figure alone does not. The single account whose pairs are all not-live holds exactly one pair in the population, where the two implementations are indistinguishable by construction.

**Skipped accounts read as empty.** Zero `access_denied` and zero `private_or_absent` were recorded across the whole Step 4 pull, so the 403-skip path never fired. The skipped accounts nevertheless exist — **287 discarded over tolerance and 38 skipped on the length forecast** — and **none of them is parsed, indexed, or present in the table**: of the 2,549 accounts in the parsed sweep, 0 have a non-complete final ledger outcome and 0 have no ledger row at all. They are **absent, not empty**, which is what the rule requires.

## Reported and NOT asserted (1) — the set-membership drop rule

A COVERAGE COUNT, NOT AN INVARIANT (decisions/0074 ruling 3). Step 8's own bullet calls it 'an implementation check, not a data check'. Reported, not asserted -- asserting it would add another pass to a report where six of eight cannot fail on data.

- Records examined: **6,065,610**
- Records dropped: **0**

The denominator has three readings on this data and `0074` ruling 4 publishes two of them unreconciled; all three are tabulated in `artifacts/step8-waterfall-b.md` §6.

## Reported and NOT asserted (2) — the 703 expectation

It is a population reconciliation, and the spec's own instruction to suspect the population before the implementation is what makes it one.

| Population | Denominator | Expected | Measured | Expected split | Measured split | Expected accounts | Measured accounts |
| :--- | ---: | ---: | ---: | :--- | :--- | ---: | ---: |
| APPLY | 196,654 | 703 | 703 | [604, 99] | [604, 99] | 216 | 216 |
| DERIV | 147,370 | 99 | 99 | [0, 99] | [0, 99] | 73 | 73 |

**Reconciles: True.** Neither superseded answer was produced — not **604** (ALT) and not **793** (ALT-MATCHED, withdrawn). Had the count differed, the spec's own instruction is to treat it as a **population** defect before an implementation one; the population was in fact re-derived through positions 1–5 and reproduces 196,654 and 147,370 exactly.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
