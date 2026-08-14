# Decision 0046 — ALT is adopted: a pair is not live iff no insertion instant after `τ1` AND `|A| = 0`

| | |
| :--- | :--- |
| **Decision** | **ALT is ADOPTED.** A pair is **not live iff BOTH** the account shows no insertion instant after `τ1` **and** `|A| = 0`. `0045`'s ALT rejection is **withdrawn** — it was made on the population where ALT is zero by construction. The Step 9 bound is **[16.6633%, 16.9704%] on APPLY** (corrected by `0047`). |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's third Step 7 review, verdict HOLD, items B1–B4 |
| **Supersedes** | PF-LIMIT; `0045` §1 and §3; `0044` §1.2's DERIV arm figures for Step 13 |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 9, 13, 14, 16 and the gate checklist); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md` |
| **Status** | Closed, **with §1, §4 and §7 corrected in place by `decisions/0047`** after both arms refuted them. **Step 7's rerun is complete; the gate is OPEN pending Red Team.** |

---

## 0. Standing rule, effective now

> **Every figure in a decision entry states which population produced it, at the point of use.**
> **An entry that cites a number without its population is not propagated.**

Three consecutive entries — `0043`, `0045`, and `0045`'s own correction of `0043` — each corrected the
previous one and **each committed the same error: a figure measured on one population, quoted as
another.** The pattern is not inattention to a file. **It is reaching for the number that supports the
ruling being written rather than checking which population produced it.** The rule above is the
countermeasure, and it sits with carried-forward item 46.

**The two populations, named once and used everywhere:**

- **DERIV** — Step 5 line 4 less D10, **147,370**. **Requires S2 evidence.**
- **APPLY** — line 1 less D10, **196,654**. **What Step 8 filters at position 6.**

## 1. The adopted rule

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND `|A| = 0`.**

**The second conjunct is the ruling.** The warrant for liveness — stated in the spec since `0036` and
never contested — is that **it licenses trusting a null, and the null is `|A| = 0`.** A pair with
`|A| ≥ 1` has its outcome **directly observed**. There is no null to license, so the rule does not
reach it.

**This is the rule the stated warrant actually reaches.** PF-LIMIT reached further and the record never
said why.

**Exclusions: 0 on DERIV, 604 on APPLY.**

> **CORRECTED 2026-08-13 (`decisions/0047`), on both counts, by both arms independently.** This section
> first read: *"The DERIV zero is **forced by construction** — line 4 requires S2 evidence, so no line-4
> pair can have `|A| = 0` and no S2 record. The 604 on APPLY are **exactly** the pairs with no S2 record
> anywhere."* **The counts are right. Both explanations are wrong, and both are the `|A| = 0` versus
> "no S2 record" conflation §5 of this entry warns against.**
>
> **(a) "Exactly" is false as an equality — true only as a subset.** APPLY holds **23,260** pairs with
> no S2 record anywhere; **604 are excluded and 22,656 stay live**, because their accounts insert after
> `τ1`. **The decomposition, from instance A:** conjunct 2 (`|A| = 0`) narrows **196,654 → 33,373**;
> **conjunct 1 (no insertion after `τ1`) narrows 33,373 → 604.** **Conjunct 1 does most of the work**,
> which is why the count moves with `W` at all — the original wording credited conjunct 2 with the
> whole selection.
>
> **(b) The DERIV zero is not forced by construction.** **Line 4's `has_s2` does not imply `|A| ≥ 1`:**
> `|A|` needs an **in-`E2`** record while line 4 needs only an S2 record. **9,145 DERIV pairs are
> never-started.** Instance B found **four line-4 pairs holding S2 records with no episode number in
> `E2`**, so `|A| = 0` at every `W`; **they satisfy both conjuncts at every arm and are removed one
> position earlier by D10.** **The DERIV zero is produced by the filter order and this pull date, not by
> line 4's definition** — a fact, not a theorem.

## 2. Why PF-LIMIT is superseded — the 751 had no warrant

On APPLY, PF-LIMIT deleted **1,355** pairs. They split cleanly:

| | Pairs | Outcome basis | Warrant |
| :--- | ---: | :--- | :--- |
| No S2 record anywhere | **604** | rests entirely on the null | **`|A| = 0`** — stated, uncontested |
| Positive in-window S2 evidence | **751** | **652 directly observed (Continued); 99 NULL-BASED (Started-and-left)** | 652: none stated. **99: the same warrant that covers the 604** |

> **CORRECTED 2026-08-13 (`decisions/0048`).** This row first read *"directly observed — 652 continued,
> 99 left."* **The 99 are not directly observed.** `|A| ≥ 1` is observed; **the failure to meet the
> Continued condition is not.** Under `0034` **only Continued rests on positive evidence**, so
> Started-and-left is a null on exit — and `τ2 > τ1` makes it structural: **a pair silent after `τ1`
> can produce no evidence in the `[τ1, τ2)` window the Continued test reads**, so it is scored "left"
> **by construction.** The 751 split **652 observed / 99 null-based**, and the warrant reaches the 99.
> `0047` corrected three claims in this entry and missed this one; Red Team's fourth review caught it.

**Deleting rows whose outcomes are observed is a denominator operation, not a liveness inference.**
Instance A measured the mechanism exactly: on DERIV the never-started **numerator is 9,145 under both
rules** — PF-LIMIT's entire effect there is the denominator falling by 751.

**A gate whose deliverable is "the rule statement" cannot close on a rule half of whose deletions have
no stated reason.** Red Team held on this three times; the third time it was dispositive, and it is
right.

## 3. `0045`'s ALT rejection is withdrawn — the error, recorded

`0045` §1 stated: *"both arms measured its exclusion set at **zero pairs** across every `W` tested."*

**That is the DERIV row.** Instance B measured both populations and separated them explicitly:

| Population | `W` = 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DERIV | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 |
| **APPLY** | **485** | 494 | 554 | 575 | 603 | **604** | 664 | **716** |

**And it is forced arithmetic, not a measurement.** ALT = PF-LIMIT ∩ `|A| = 0`, so **ALT's exclusion
set *is* PF-LIMIT's never-started exclusion set** — which **`0045` §4.2 itself states is 604 on
APPLY**, while §4.1 explains why it must be zero on DERIV. **The same entry gave two counts for the
same set and §1 took the one that is zero by construction.**

**So ALT was "rejected on effect" using a measurement taken where it cannot have an effect.** Neither
arm recommended rejection on that ground: instance A recommended **adopting** ALT; instance B
recommended against it on propagation cost and measured the real difference at **+0.065 pp on
never-started, paired clustered CI [+0.0413, +0.0947], excluding zero.**

## 4. The bound, republished on one denominator

**Under the adopted rule, on a SINGLE denominator: [16.6633%, 16.9704%] on APPLY, width 0.3071 pp.**

> **CORRECTED 2026-08-13 (`decisions/0047`).** This section first published **[16.7146%, 16.9704%]**,
> width 0.2558 pp. **That interval mixed denominators — floor on 196,050, ceiling on 196,654 — and its
> floor did not cover the case liveness exists to guard against.** If all 604 had actually started, the
> never-started share on the position-5 population is **16.6633%**, sitting **0.0513 pp below the
> published floor.** Instance B found it, reported both intervals and chose neither, and named it as
> **this entry's own §4 objection to PF-LIMIT's floor, in the same form, against the adopted rule.**
>
> **THIS IS THE THIRD CONSECUTIVE BOUND WHOSE FLOOR DID NOT COVER THE CASE THE FILTER EXISTS FOR.**
> `0043`'s ceiling landed outside the feasible set; `0045`'s floor landed outside it on the other side;
> `0046`'s floor did the same on a mixed denominator. **The recurring cause is publishing an endpoint
> computed on the filtered population against an estimand defined on the unfiltered one.** Recorded
> beside the population rule in §0, because it is the same failure in a second dimension: **an endpoint
> must state the population it is computed on and the estimand it bounds, and they must be the same
> population.**

**The ceiling equals the unfiltered share as an identity.**

> **PHRASING CORRECTED 2026-08-13 (`decisions/0049`).** This read *"the excluded set is a subset of
> never-started, so **returning every excluded pair as a decliner** reproduces the unfiltered population
> exactly."* **That is false under ALT-BROAD** — returning all 703 as decliners gives an **unattainable
> 17.3279%**, because the 99 started-and-left exclusions have `|A| ≥ 1` observed and **cannot** be
> never-started. **Step 9 reads this sentence**, which is why it is corrected rather than left.
>
> **The identity still holds, by a different route:** the ceiling returns **only the never-started
> exclusions** — the 604 — to the never-started count, and those are exactly the pairs the unfiltered
> population counts as never-started. **The route matters because ALT-BROAD's exclusion set is no
> longer a subset of never-started.** **Both endpoints are attainable.**

**What `0045` published, and why it was wrong.** It gave **[16.7789%, 17.0355%]** for PF-LIMIT under
"Option C" and claimed the same identity.

- **It mixed denominators** — floor on 195,299, ceiling on 195,903.
- **Its floor was not a floor.** If all 604 had actually started — **the exact case liveness exists to
  guard against** — the share is **16.727%**, *below* the published floor and outside the interval.
- **The identity claim was false for PF-LIMIT.** It is a property of ALT. **Instance B said so in the
  section the number was lifted from:** *"It is not identical to ALT's bound (the denominator still
  omits the 751), and that difference should be stated where it is published."*

**The internally consistent PF-LIMIT interval was [16.727%, 17.0355%], width 0.308 pp** — 20% wider
than published, and republished here for the record even though PF-LIMIT is superseded. **The old
ceiling was rejected for landing outside the feasible set; the replacement floor landed outside it on
the other side.**

## 5. The ordering question, settled

**`|A| = 0` is evaluated before liveness applies, and that is permitted.** Both arms proved it
independently:

- **Row-local predicates on the position-5 output commute exactly** (instance A).
- **`0029` fixed the filter order because "the final row set commutes, but the required per-filter
  sample size does not" — and that cannot reach position 7, because outcome assignment removes no
  rows.** Positions 1–6 are filters; **position 7 is an annotation** contributing no waterfall line
  (instance B).

**Two consequences the spec now carries**, both raised by the arms:

- **Waterfall line 6 becomes outcome-conditional and must be reported as such**, or two faithful
  instances diverge on the waterfall while agreeing on every share.
- **The monotone-decrease invariant holds only non-strictly** where the exclusion set is empty — which
  it is, on DERIV.

**`|A| = 0` means Step 1 §7's Never-started condition, not "no S2 evidence at all."** The competing
reading selects a different set.

## 6. The five-file pass, executed

| Correction | Where |
| :--- | :--- |
| The adopted rule, both populations, both exclusion counts | all five |
| **Withdrawn "vary the liveness threshold"** — still live in both `data-scientist` files after `0044` withdrew it | `data-scientist.md`, `-b.md` |
| **Step 7 headed "APPROVED … with NO free parameter … Complete"** while both `analytics-engineer` files said the gate was open | `data-scientist.md`, `-b.md` |
| `0044` §1.2's per-arm exclusion count, which had reached **no** agent file | `data-scientist.md`, `-b.md` |
| **`task-sheet.md`'s "this is the ruling the whole rule now rests on"** — declared untrue by `0043` §3, survived two entries | `task-sheet.md` |
| **Step 13's coupling figures corrected to APPLY** — 833 → 1,670, factor 2.0; the 348 → 949 figures were DERIV | `task-sheet.md`, both `data-scientist` |
| Step 16's interactive control, the gate checklist, the sensitivity-test item, the derive/apply limitation | `task-sheet.md` |

**Propagation failure #7 was the withdrawn instruction surviving in the two files `0044` §2 had itself
named** as the place an instance *"would have tried to execute it."*

## 7. What this costs, stated

**Step 7's dual run exercises the rule on APPLY, and not at all on DERIV.**

> **CORRECTED 2026-08-13 (`decisions/0047`): this section was too pessimistic.** It first read *"Step 7's
> own dual run cannot exercise the rule… the rule is first exercised at Step 8."* **Instance B refuted
> that: the rule is exercised now, on APPLY** — 604 exclusions from **191 accounts**, per-arm counts
> 485–716, the three shares, the bound and a waterfall line, **all depending on both conjuncts.**
>
> **What is true is narrower and is the operative warning: only the APPLY figures carry information, and
> DERIV's diff is literally `0 = 0` at every arm.** If the two instances are diffed on DERIV numbers,
> the gate's dual control proves nothing about the rule. That is a real weakness of the adopted
rule and it is recorded rather than argued away — instance A raised it as an argument against ALT, and
the ruling accepts it because the alternative is a rule that deletes 751 rows on no stated warrant.

**Red Team's item 2 is closed by adopting a rule the stated warrant reaches**, not by writing a warrant
for PF-LIMIT's extra 751.

## 8. Scope

- **Step 7 reruns on ALT as a dual pair. The gate is OPEN and Step 8 does not launch.**
- **Zero API calls.**
