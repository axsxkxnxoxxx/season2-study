# Decision 0069 — the seven Step 8 gaps with one correct answer are closed at the point of use

| | |
| :--- | :--- |
| **Decision** | **All seven `0068` §2a items are stated where they are used**, in `task-sheet.md` and — for the four that also appear there — in both `analytics-engineer` files. **Every Step 8 invariant is now labelled CODE CHECK or DATA CHECK**, which resolves the read-back arms' 4-of-6 against 6-of-6 split. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `0068` §2a |
| **Status** | Closed. **The eight `0068` §2b rulings are untouched and are the Human Lead's.** |

---

## 1. The seven

| # | Was | Now stated at the point of use |
| :-- | :--- | :--- |
| 1 | *"the 3,440 Started-and-left pairs"*, population unstated | **on the uncensored estimation sample of 128,099, NOT on Step 8's population** — S&L 17,420 before the amendment and 15,174 after (`0034` §3). **That is why Step 14 calls it a floor:** the sample excludes what the Step 5 waterfall drops and is not right-censored |
| 2 | *"Expect 703 liveness exclusions"*, no denominator | **on APPLY = 196,654, the position-5 output**, and **99 on DERIV = 147,370**. **The count alone could not be checked without it** |
| 3 | *"sum to the sample"* | **the post-position-7 row set** — the rows remaining after outcome assignment, the only thing the phrase can mean |
| 4 | distinct episodes ≤ season length, unlabelled | **CODE CHECK**, on the same ground as `A ⊆ A_H` — Step 8's own set-membership bullet already establishes `\|D\| ≤ L` by construction |
| 5 | D3′'s *"share of all Started-and-left"* | **on the population and at the arm named at the point of use**, never carried from another arm. **Each arm's denominator is its own** |
| 6 | *"the aggregate line above says 97.6%"* | **97.6% restated with its source** (`0030`, `0033`), **because there was no line above stating it** — the right-censoring bullet requires two lines and gives no percentage, so the figure this bullet argues against was never on the page |
| 7 | the silence test's strictness, unstated | **STRICT.** *"No insertion instant **after** `τ1`"* means **no instant `> τ1`**; an instant exactly **at** `τ1` does not make the account live |

## 2. Every invariant is labelled, and that is what resolves the split

**The read-back arms diverged: A called four of six true by construction, B called all six.** ***AMENDED 2026-08-13 (`0076`): the count in this entry is superseded.*** `0074` then specified the `p` invariant and **mislabelled it a DATA CHECK**; both Step 8 instances proved it a **CODE CHECK**, so **on the post-`0074` set of six the figure is FIVE of six, with ZERO pure data checks.** `0076` adds two genuine data checks for that reason. Both were
defensible because the spec labelled exactly one. **Now all are labelled, and the count falls out:**

| Invariant | Label |
| :--- | :--- |
| outcome states mutually exclusive, summing to the post-position-7 row set | **CODE CHECK** — Step 1 §7's partition is proved exhaustive and disjoint |
| filter counts decrease monotonically, coded `>=` | **CODE CHECK** — filters only remove rows, so it fails only on an implementation that adds them. **Load-bearing in fact: position 2 removes exactly 0 pairs on this frame**, measured independently by both instances |
| distinct episodes ≤ season length | **CODE CHECK** — `\|D\| ≤ L` by construction under set membership |
| `A ⊆ A_H` on every row | **CODE CHECK** — true by construction since `τ1 < τ2` |
| clock start relative to the S2 finale and first-pass S1 completion | **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** — `T0` is a `max()`, so the clauses hold for any correct one; **the force comes from recomputing the S1 completion date INDEPENDENTLY.** Read back rather than recomputed, it degrades to a code check and proves nothing |
| the 703 expectation | **NOT AN INVARIANT.** A **population reconciliation** — and the spec's own instruction to suspect the population before the implementation is what makes it one |

**So: four pure code checks, one that is a code check by construction and a real cross-check as
specified, and one item that is not an invariant at all.** **A counted the four. B counted six things
that cannot fail on data alone.** **Neither was wrong; the spec had not said which.**

**Why this matters beyond bookkeeping:** an unlabelled code check reads as evidence for the rule. Four
of Step 8's six assertions **cannot fail on any data**, and a report of "all invariants passed" that
does not say so overstates what was verified.

## 3. Scope

- **`task-sheet.md`** carries all seven. **Both `analytics-engineer` files** carry the four that appear
  there — the invariant set, the 97.6%, and the strict silence test — **pair verified byte-identical
  apart from `name:`.** The 3,440, the 703 denominator and D3′'s share do not appear in the agent files,
  so they were not inserted there; **checked, not assumed.**
- **The eight `0068` §2b items are untouched**: both-channel users, `action` at pair grain, D2's tied
  `max()` terms, the drop-share denominator, DERIV, D4, the `τ_pull` evidence scope, and the censoring
  order.
- **Zero API calls. Step 8 has not launched.**
