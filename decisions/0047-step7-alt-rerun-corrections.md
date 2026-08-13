# Decision 0047 — `0046` §1, §4 and §7 corrected after the ALT rerun; D10 is re-derived per arm; Step 8's monotone invariant is `>=`

| | |
| :--- | :--- |
| **Decision** | **`0046` §1, §4 and §7 are corrected** — all three refuted by both arms independently. **The bound is republished on a single denominator: [16.6633%, 16.9704%], width 0.3071 pp.** **D10 is re-derived at each `W` arm.** **Step 8's monotone invariant is `>=`.** **604 is carried into the Step 8 diff as an expected value**, and a mismatch is a population defect first. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 7 ALT rerun. Both arms agreed on every published figure and refuted three claims in the entry that adopted the rule |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 8, 9); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md` |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. What the rerun agreed on

**Every published figure matched across both arms.**

| | Both arms |
| :--- | ---: |
| Exclusions, **DERIV** | **0** at every arm |
| Exclusions, **APPLY**, `W = 108` | **604**, from 191 accounts, 0.3071% |
| Per-arm, **APPLY** | 485 / 494 / 554 / 575 / 603 / **604** / 664 / 716 |
| Shares, **APPLY**, under the rule | 16.7146 / 73.5221 / 9.7633 |
| Movement vs no filter, **APPLY** | −0.2558 / +0.2258 / +0.0300 pp |
| Composition of exclusions | **100% Never started**, both populations, every arm |

**Both verified the ceiling identity on integers rather than floats** — `32,769 + 604 = 33,373` over
`196,050 + 604 = 196,654`. Both re-asserted the Step 5 waterfall before use, read the calibration
without refitting, and cross-checked the instant sequence against an independent recomputation.

**Instance B added an independent implementation check**: it solved the rule for each pair's feasible
`W` interval — 29 line-4 pairs have a non-empty one — and **reconstructed the APPLY exclusion counts at
every arm exactly** from that calculation.

## 2. `0046` §1 corrected — both explanations were wrong, the counts were right

**Neither error changes a number. Both are the `|A| = 0` versus "no S2 record" conflation that §5 of
the same entry warns against.**

**(a) "Exactly the pairs with no S2 record anywhere" is false as an equality.** APPLY holds **23,260**
such pairs; **604 are excluded and 22,656 stay live**, because their accounts insert after `τ1`. **True
as a subset only.**

**The decomposition, from instance A:**

| | |
| :--- | ---: |
| APPLY | 196,654 |
| **Conjunct 2** — `\|A\| = 0` | **33,373** |
| **Conjunct 1** — no insertion after `τ1` | **604** |

**Conjunct 1 does most of the work**, which is why the count moves with `W` at all. The original
wording credited conjunct 2 with the whole selection.

**(b) "The DERIV zero is forced by construction" is a non-sequitur.** **Line 4's `has_s2` does not imply
`|A| ≥ 1`** — `|A|` needs an **in-`E2`** record while line 4 needs only an S2 record. **9,145 DERIV
pairs are never-started.** Instance B found **four line-4 pairs holding S2 records with no episode
number in `E2`**, so `|A| = 0` at every `W`; **they satisfy both conjuncts at every arm and are removed
one position earlier by D10.**

**The DERIV zero is produced by the filter order and this pull date. It is a fact, not a theorem**, and
it would not survive a different `pull_date`.

## 3. `0046` §4 corrected — and this is the third bound in a row with the same defect

**Republished: [16.6633%, 16.9704%] on APPLY, width 0.3071 pp, on one denominator.**

`0046` published **[16.7146%, 16.9704%]**, floor on 196,050 and ceiling on 196,654. **If all 604 had
actually started — the exact case liveness guards against — the never-started share on the position-5
population is 16.6633%, sitting 0.0513 pp below the published floor.**

**Instance B found it, reported both intervals, chose neither, and named it as `0046` §4's own
objection to PF-LIMIT's floor, in the same form, against the adopted rule.**

> **THIS IS THE THIRD CONSECUTIVE BOUND WHOSE FLOOR OR CEILING DID NOT COVER THE CASE THE FILTER
> EXISTS FOR.** `0043`'s ceiling landed outside the feasible set; `0045`'s floor landed outside it on
> the other side; `0046`'s floor did the same on a mixed denominator.
>
> **The recurring cause is publishing an endpoint computed on the filtered population against an
> estimand defined on the unfiltered one.** It is `0046` §0's population rule in a second dimension.
>
> **Standing rule, added here: an interval endpoint states the population it is computed on and the
> estimand it bounds, and they must be the same population.**

## 4. `0046` §7 corrected — it was too pessimistic

It read *"Step 7's own dual run cannot exercise the rule… the rule is first exercised at Step 8."*

**Instance B refuted that. The rule is exercised now, on APPLY** — 604 exclusions from 191 accounts,
per-arm counts, three shares, a bound and a waterfall line, **all depending on both conjuncts.**

**What is true is narrower, and is the operative warning: only the APPLY figures carry information, and
DERIV's diff is literally `0 = 0` at every arm.** If the two instances are diffed on DERIV numbers, the
gate's dual control proves nothing about the rule.

**What the gate still cannot establish**, from both arms: that Step 8's position-6 population is the one
reconstructed here — both built APPLY from the Step 5 pair table, not through Step 8's positions 1–5 —
that two implementations of the rule agree, or, in instance B's words, **that the rule is right: "its
warrant is an argument, not a measurement."**

## 5. D10 is re-derived at each arm, and the spec names it

Instance A produced **both** tables. The per-arm counts reproduce `0046` §3 **only if D10 is re-derived
at each arm**; **freezing D10 at `W = 108` gives 632 / 684 / 753 / 881 — at `W` = 125 / 150 / 180 / 213** *(arms attached 2026-08-14 by `0048`; stated without them, a Step 13 instance would pair 632/684 with arms 150/213 and report a false divergence).* **Note 125 and 180 are NOT in the mandated grid** — `0027`'s arms are 38/46/77/91/107/108/150/213 — so only the 150 and 213 entries, **684 and 881**, are comparable to it.

**Right-censoring is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which contains `W`**, so the censored
population differs per arm and the frozen reading is not the same experiment.

**An arm table that does not name the reading is not reproducible.** The spec now names it.

## 6. Step 8's monotone invariant is `>=`

**Decrease is strict at line 6 on APPLY and only non-strict on DERIV**, where the exclusion set is
empty. **Both arms found this independently, and both said the same thing: an implementation asserting
strict decrease everywhere fails on correct data.**

## 7. 604 is an expected value for the Step 8 diff, and a mismatch is a population defect first

**Instance A's suggestion, adopted.** Step 7 measured 604 on APPLY but **built that population from the
Step 5 pair table rather than through Step 8's positions 1–5.**

**So a different count at Step 8 most likely means the frame join, the `L2 = 1` exclusion or the
censoring differs — not that the liveness rule was coded wrong. Check the population first.**

## 8. Scope

- **No rule change.** Three explanations corrected, one interval republished, three spec obligations
  added.
- **Zero API calls.**
- **Step 7 goes to Red Team. Step 8 does not launch.**
