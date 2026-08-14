# Step 8 — invariant report (instance `b`)

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.

## How to read this report

**FOUR of the six assertions are pure CODE CHECKS and CANNOT FAIL ON ANY DATA. A fifth is a code check by construction and a genuine cross-check only because the S1 completion date is recomputed independently. 'All invariants passed' therefore says the code computed what it was told to; it is NOT evidence for the rule (decisions/0068, 0070 Sec 4).**

Counts: **4 pure code checks**, **1 that is a code check by construction and a genuine cross-check as specified**, **1 additional range check emitted**, and **1 item that is not an invariant at all** — the 703 expectation, which is a population reconciliation.

| # | Invariant | Label | Result |
| :-- | :--- | :--- | :--- |
| 1 | outcome states are mutually exclusive and sum to the POST-POSITION-7 row set | **CODE CHECK** | **PASS** |
| 2 | filter counts decrease monotonically -- CODED AS `>=`, NOT `>` | **CODE CHECK** | **PASS** |
| 3 | distinct episodes never exceed season length (|D| <= L) | **CODE CHECK** | **PASS** |
| 4 | A is a subset of A_H on every row | **CODE CHECK** | **PASS** |
| 5 | clock start is on or after the S2 finale date, on or after the first-pass S1 completion date, and equals one of those two | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** | **PASS** |
| 6 | abandonment point p is in (0, 1] on every Started-and-left row | **CODE CHECK** | **PASS** |

**All invariants pass: True.** That statement says the code computed what it was told to. It is **not** evidence for the liveness rule, for the outcome definition, or for any published share.

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
  "rows_examined": 196654,
  "records_failing_membership_at_stage_1": 0,
  "records_examined_at_stage_1": 6065610
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
  "set_identity": "the two implementations return the SAME 220,107 (user, show) keys -- checked as a set, not only as a count"
}
```

**second external cross check**

```json
{
  "against": "processed/step5/pair_revision5.csv s1_completion_date, built by a different pipeline at Step 5",
  "pairs_compared": 220103,
  "mismatches": 0
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

## 6. abandonment point p is in (0, 1] on every Started-and-left row

**Label: CODE CHECK.** set membership makes A a subset of E2, so max(A_H) is in E2 and the rank numerator is at least 1 and at most L2. It fails only on the withdrawn raw-ratio form p = m_H / L2, which can exceed 1 where S2 numbering has a gap.

**checked**

```json
{
  "rows_examined": 19042,
  "min": 0.038461538461538464,
  "max": 1.0,
  "rows_out_of_range": 0,
  "rows_with_p_not_computed": 0
}
```

Form: `p = |{e in E2 : e <= m_H}| / L2, rank form, read on A_H (0034)`.

**Result: PASS.**

## The 703 expectation is NOT an invariant

It is a population reconciliation, and the spec's own instruction to suspect the population before the implementation is what makes it one.

| Population | Denominator | Expected | Measured | Expected split | Measured split | Expected accounts | Measured accounts |
| :--- | ---: | ---: | ---: | :--- | :--- | ---: | ---: |
| APPLY | 196,654 | 703 | 703 | [604, 99] | [604, 99] | 216 | 216 |
| DERIV | 147,370 | 99 | 99 | [0, 99] | [0, 99] | 73 | 73 |

**Reconciles: True.** Neither superseded answer was produced — not **604** (ALT) and not **793** (ALT-MATCHED, withdrawn). Had the count differed, the spec's own instruction is to treat it as a **population** defect before an implementation one; the population was in fact re-derived through positions 1–5 and reproduces 196,654 and 147,370 exactly.

---

**Step 8 is a GATE and this document is a PROPOSAL.** Nothing here is adopted. This instance does not adopt its own proposal, does not begin Step 8b or Step 9, and records no approval — that is the Human Lead's alone. Zero API calls; every figure is computed from data already on disk.
