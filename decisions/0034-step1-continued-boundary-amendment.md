# Decision 0034 — Step 1 §7 amended: Continued is evaluated at `τ2 = ⟦T0⟧ + (W + H) × 24h`

| | |
| :--- | :--- |
| **Decision** | **Continued is evaluated at `τ2 = ⟦T0⟧ + (W + H) × 24h` = 199 days. Never-started stays at `τ1` = 108 days.** Gate 1 reopened as an amendment and re-approved. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `artifacts/step1-outcome-definition.md` §7 (outcome-state table, partition proof, abandonment point `p`), D3, D8's rationale line |
| **Record** | `artifacts/step1-amendment-continued-boundary.md` — revision 13, **eleven Red Team rounds**, dispositions in §11–§21 |
| **Does NOT reopen** | Step 6 / `W = 108` / `0026`; D14; Step 5; the `L2 = 1` exclusion; **D8**, which survives unchanged |
| **Status** | Closed |

---

## 1. The approved rule

Let **`τ2 = ⟦T0⟧ + (W + H) × 24h`**; at `W = 108` and `H = 91`, **`τ2 = ⟦T0⟧ + 199 days`**. Let **`A_H`**
be `A` recomputed with the bound moved from `τ1` to `τ2` — the set D3 already defined.

| State | Condition |
| :--- | :--- |
| **Never started** | `\|A\| = 0` |
| **Continued** | `\|A\| ≥ 1` **and** `F2 ∈ A_H` **and** `\|A_H\| ≥ ceil(0.90 × L2)` |
| **Started and left** | `\|A\| ≥ 1` **and not** the Continued condition |

Also approved, in the Human Lead's terms:

- **`|A| ≥ 1` at `τ1` remains a conjunct of Continued.** Without it a pair starting S2 on day 150 and
  completing by day 190 satisfies the other two conjuncts with `|A| = 0` and falls in **two** states.
- **Step 10's `p` uses the rank form with `m_H`:** `p = |{ e ∈ E2 : e ≤ m_H }| / L2`, where
  `m_H = max(A_H)`. The raw-ratio form `m_H / L2` stays withdrawn.
- **D3 is replaced by D3′**, run at **every Step 13 arm** with its own cleared count and share, with
  the exposure-weighted residual reported alongside **as a labelled count**.
- **Liveness stays anchored at `τ1`.** Liveness licenses trusting a null, and the null is `|A| = 0`,
  which is tested at `τ1`. ~~`τ2` plays no part in the liveness test.~~ **AMENDED 2026-08-13 (`0051`): under ALT-BROAD `τ2` DOES play a part** — the rule's second conjunct is the **Continued** test, read at `τ2`. **What this ruling actually fixed, and what stands, is that the SILENCE test is `τ1`-anchored**, which is what ALT-BROAD implements. The rule reads two instants: silence at `τ1`, Continued at `τ2`. **Written into the Step 7 spec so
  no isolated instance re-anchors it.**
- **Step 8 gains the `A ⊆ A_H` invariant**, asserted on every row — labelled **a code check, not a
  data check**, since it is true by construction.

## 2. Reasoning

**The old boundary scored a late completer as an abandoner, which was false.** That is the whole of
the case, and the rest is the price of fixing it.

- **2,246 pairs move, all in one direction.** `A ⊆ A_H` since `τ1 < τ2`, so the change is **monotone**
  — Started-and-left → Continued only, never the reverse.
- **The never-started share is unchanged**, to four decimal places (6.5957% before and after). That
  arithmetic is a check on a structural argument, not evidence for it.
- **Censoring cost is zero and no shows are lost.** D10 already requires
  `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which at `W = 108` is exactly `τ2`, and
  `W + H ≤ max(W, 91) + H` is an identity — so this holds at **every** Step 13 arm by construction.
- **No new constant.** `H = 91` was adopted by name at the Step 1 approval (D10), is already held
  constant across Step 13's arms, and is explicitly not a function of `W`.

## 3. Stated plainly, and not softened

- **It fixes 39.5% of the misclassification and leaves 60.5% standing.** Of the 5,686
  Started-and-left pairs that eventually complete S2, **2,246 are reclassified and 3,440 are not.**
  The residual is **reported, not resolved** — 19.75% of the old Started-and-left group, 22.67% of
  the new one.
- **Continued is a 199-day statement while never-started is a 108-day statement, and the two must not
  be described as measured alike.** This appears wherever the split is reported, not in a footnote.
- **There is no stated ground for preferring `τ2` to first-S2-watch + `H`.** Four were attempted
  across revisions 6, 7, 8 and 12 and **all four failed review** — exogeneity (false: `T0`'s
  `S1_completion_date` term binds on **52.7%** of pairs), temporal position (does not bind: D10
  already imposes the clearance), arm comparability (false: no diagnostic window changes length), and
  choice-at-a-price (false and backwards: `τ2` gives every starter **more** than 91 days, and item
  9's set **grows** under the start anchor). **That absence is recorded rather than papered over**
  (`artifacts/step1-amendment-continued-boundary.md` §21).

## 4. Step 14 — three ledger entries, published together, never netted

`0028` requires every directional mechanism stated separately. This amendment contributes **three**,
and **none may be netted against another**:

| # | Mechanism | Direction | Size |
| :--- | :--- | :--- | :--- |
| **8** | The Continued boundary at `τ1 + H` — a **definitional change**, no direction claimed against truth | ratio **0.485 → 0.557**, a 14.8% shift; Started-and-left falls **12.9%** | 2,246 pairs |
| **9** | Late completers beyond `τ2`, left scored as abandoners | ratio **DOWN** | **3,440**, a floor |
| **10** | Never-started decided at 108 while Continued is decided at 199 | ratio **UP** | **1,575** on the estimation sample, **1,573** after right-censoring; a floor for D8's population. Share 18.64% is a **ceiling** |

**Items 9 and 10 are counterweights and must publish together.** Their counts are **not
commensurable** — item 9 acts on the ratio's denominator, item 10 on its numerator — so subtracting
one from the other produces a number that means nothing. **No corrected never-started count or ratio
is given**, because both known channels push the same way and neither is measured.

**Item 10 is not a cost of adopting.** Those pairs are Never started under the pre-amendment rule too;
`A_H` is what makes them **measurable**.

## 5. What the review found that was not about the rule

**The rule survived eleven adversarial attempts unbroken** — the partition, the `A ⊆ A_H`
monotonicity, and the `max(W, 91) + H ≥ W + H` identity held every round. Every hold from revision 2
onward was against the justification prose, and two findings changed figures elsewhere:

- **D11 was not being applied.** `τ_pull` is a global frozen cutoff and records at or after it are
  discarded from every computation; neither `eval_continued_boundary.py` nor the correction script
  applied that filter. Applied: **77 records discarded, 28 pairs touched**, never-started 8,445 →
  **8,449**. **2,246 and 12.9% did not move.** The scope limit is disclosed rather than chased into
  Step 5 and Step 6, which are approved gates (`artifacts/step1-amendment-continued-boundary.md`
  §4.1a).
- **`first_s2_lag_days` is a backfill measure, not a start-time filter.** This document read it as
  the latter for six revisions and argued from it in two ledger entries. **Step 5 named it correctly
  throughout**, so the approved Step 5 gate is untouched. The floors now rest on the
  contamination-exclusion channel — 50,066 pairs, not 73,801, since the 23,735 dropped at the
  waterfall's second step have `A_H = ∅` and can enter no numerator.

## 6. Scope

- **Nothing downstream has been re-run.** Step 8 has not launched; it is an unapproved gate and a dual
  pair, so this rule is in the spec both isolated instances will read.
- **Step 7 has not launched** and its liveness percentile remains unruled.
- **Zero API calls.** Every figure comes from `src/amendment_corrections.py`,
  `src/eval_continued_boundary.py` and `src/step6_completion_lag.py` on cached data.
