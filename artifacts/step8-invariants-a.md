# Step 8 — invariant report, instance `a`

**Owner:** Analytics Engineer (`a`) · **Mode:** GATE, dual implementation · **W = 108 days** · **H = 91 days** · **Zero API calls** · **Counts only**

> **EVERY INVARIANT CARRIES A LABEL** (`decisions/0068`). **A code check catches an implementation that computed something wrongly; it cannot fail on any data, and it is NOT evidence for the rule.** A report saying "all invariants passed" overstates what was verified unless it names which ones could have failed. **Four of the six required invariants here cannot fail on data at all.**

**Result: 7 checks ran and all passed — 6 labelled CODE CHECK and 1 labelled CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.**

**How this maps onto `0070` §4's count of the required set** — *four pure code checks, one that is a code check by construction and a genuine cross-check as specified, and one item that is not an invariant at all*: **items 1–4 are the four pure code checks**; **item 5 is the hybrid**; **item 6 is the set-membership check**, which Step 8's own bullet labels a code check; **item 7 is an extra this instance added** and is labelled as such; and **the 703 line is the item that is not an invariant**, reported separately below as a population reconciliation.

| # | Invariant | Label | Coverage | Result |
| :-- | :--- | :--- | ---: | :--- |
| 1 | outcome states are mutually exclusive and sum to the post-position-7 row set | **CODE CHECK** | 195,951 | PASS |
| 2 | filter counts decrease monotonically, coded >= and not > | **CODE CHECK** | 7 | PASS |
| 3 | distinct episodes never exceed season length | **CODE CHECK** | 278,452 | PASS |
| 4 | A is a subset of A_H on every row | **CODE CHECK** | 195,951 | PASS |
| 5 | clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equal to one of the two | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** | 195,951 | PASS |
| 6 | the set-membership drop rule is enforced | **CODE CHECK** | 6,065,704 | PASS |
| 7 | EXTRA, not required by the spec: p lies in (0, 1] on every Started-and-left row and is null everywhere else | **CODE CHECK** | 19,042 | PASS |

### 1. outcome states are mutually exclusive and sum to the post-position-7 row set

**CODE CHECK.** Step 1 SS7's partition is proved exhaustive and disjoint, so this can only catch an assignment coded wrongly. It is not evidence for the rule.

- `coverage_rows` = `195951`
- `exactly_one_state_per_row` = `True`
- `sum_equals_row_set` = `True`
- **result: PASS**

### 2. filter counts decrease monotonically, coded >= and not >

**CODE CHECK.** filters only remove rows, so it fails only on an implementation that ADDS them -- a duplicating join. >= is kept so the invariant does not encode a property of one rule: a position that legitimately removes nothing must not fail (0047, 0049). Load-bearing in fact: position 2 removes exactly 0 pairs on this frame.

- `chain_APPLY` = `[220107, 220107, 220107, 201900, 196654, 195951, 195951]`
- `coverage_positions` = `7`
- `chain_note` = `chain_APPLY[i] is the count after filter position i+1; the transition from entry i to entry i+1 is the effect of filter position i+2`
- `filter_positions_removing_exactly_zero` = `[2, 3, 7]`
- **result: PASS**

### 3. distinct episodes never exceed season length

**CODE CHECK.** the set-membership drop rule already establishes |D| <= L by construction; this fails only if an implementation filtered by the numeric range 1..F instead of by the listed set E (Step 1 SS3.2). Not evidence for the rule.

- `coverage_pairs` = `278452`
- `max_D1_minus_L1` = `0`
- `max_AH_minus_L2` = `0`
- **result: PASS**

### 4. A is a subset of A_H on every row

**CODE CHECK.** true by construction since tau1 < tau2 and both sets are prefixes of the same timestamp-ordered episode list; it can only catch the two sets being computed wrongly or the bounds transposed. Not evidence for the rule.

- `coverage_rows` = `195951`
- `rows_where_A_exceeds_A_H` = `0`
- `rows_where_max_A_exceeds_max_A_H` = `0`
- **result: PASS**

### 5. clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equal to one of the two

**CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED.** T0 is a max(), so the two inequalities and the equality hold for any correct implementation. The force comes from recomputing the first-pass S1 completion date INDEPENDENTLY from the episode records rather than reading back the pipeline's value: a disagreement there is a real finding. Read back rather than recomputed, this degrades to a code check and proves nothing.

- `replaces` = `the withdrawn 'no clock start precedes an S2 premiere', vacuous under a finale-anchored clock`
- `coverage_rows` = `195951`
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
- **result: PASS**

### 6. the set-membership drop rule is enforced

**CODE CHECK.** an implementation check, not a data check (Step 1 SS3.2). The data check is the drop count, reported in diagnostics.json.

- `coverage_records_examined` = `6065704`
- `records_surviving_with_number_outside_E` = `0`
- `dropped_records` = `0`
- **result: PASS**

### 7. EXTRA, not required by the spec: p lies in (0, 1] on every Started-and-left row and is null everywhere else

**CODE CHECK.** secured by the set rule (A subset E2, so max(A_H) is in E2); it catches the withdrawn raw-ratio form max(A_H)/L2, which can exceed 1 where S2 numbering has a gap.

- `coverage_rows` = `19042`
- `min` = `0.038461538461538464`
- `max` = `1.0`
- `nulls_among_started_and_left` = `0`
- `non_null_outside_started_and_left` = `0`
- **result: PASS**

---

## The 703 line is NOT an invariant

**NOT AN INVARIANT -- a POPULATION RECONCILIATION (0068).** Step 7 measured its counts on APPLY built from the Step 5 pair table rather than through positions 1-5, so this is the first place the two chains have been compared. A mismatch is a POPULATION defect before an implementation one.

| Population | Denominator | Expected | Measured | never-started | started-and-left | accounts |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **703** | 604 | 99 | 216 |
| **DERIV** | 147,370 | 99 | **99** | 0 | 99 | 73 |

**It reconciles: True.** Neither superseded answer was produced — ALT's 604 on APPLY: False; ALT-MATCHED's 793 on APPLY: False.

---

## What the invariant set does and does not establish

- It establishes that **the definition on paper is the definition in the code**: the partition is exhaustive and disjoint as assigned, no filter position adds rows, no episode set exceeds its season, `A` sits inside `A_H`, the clock is the `max()` it is defined to be, and membership was tested by set and never by the numeric range `1..F`.
- It establishes **nothing about whether the rules are right**. Four of these checks cannot fail on any data. The one with force is the clock-start check, and only because the first-pass S1 completion date is **recomputed independently from the episode records**; read back from the pipeline's own value it would prove nothing.
- **The withdrawn invariant** — "no clock start precedes an S2 premiere" — is vacuous under a finale-anchored clock and catches nothing. It is replaced by the three-part check above, whose equality clause is the part that does work.

*Generated by `src/step8_a_6_emit.py` from `processed/step8/a/invariants.json`.*
