# Decision 0038 — Step 7's spec is frozen: reference population 152,126, one gap per pair, the quota and the inertness disclosed, the `W`-coupling accepted

| | |
| :--- | :--- |
| **Decision** | **Reference population: the 152,126** (waterfall line 4), with **derivation and application populations identical**. **Weighting: one gap per pair.** The **quota property** and the **inertness** are **stated plainly in the deliverable**. The **`W`-coupling is accepted** and the contradicting requirement withdrawn; **Step 13 refits per arm**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Amends** | `task-sheet.md` Step 7 and Step 13; **`decisions/0036` §3**; `.claude/agents/data-scientist.md` and `data-scientist-b.md`, identically |
| **Occasioned by** | The Step 7 rerun of 2026-08-13. Both arms agreed on every number and diverged on one unsettled spec question |
| **Status** | Closed. **Step 7 reruns on the frozen spec.** |

---

## 1. What the rerun's diff actually showed

**There was no arithmetic disagreement.** Instance A proposed **504 d**, instance B proposed **914 d**,
and **each independently computed the other's figure as its own alternative** — to the digit. The gap
was one unsettled question: **which population's bracketing gaps form the reference.**

| Reference population | Threshold |
| :--- | ---: |
| 128,099 clean sample | 504 d |
| **152,126 — adopted** | *(to be measured on the rerun)* |
| 201,900 analysis population | 914 d |

Both arms also reproduced the shared corroborations exactly: pooled median 0.0000006 d, bracketing
median 2.01 d, the **37.3936%** realised rate under the withdrawn basis, and the 38,696 / 5,209 / 1,038
buckets. **The gap-unit fix from `0037` §4 held** — both landed on 3.4432 d for the pooled 99th, the
figure that had previously split them four days apart.

## 2. Reference population: the 152,126, and it is instance A's own counter-argument

A proposed 128,099 and then named the better case against itself: **the 152,126 → 128,099 filter
concerns the FIRST S2 WATCH**, which **plays no part in `τ1` or in liveness**. Conditioning the
liveness reference on it excludes pairs for a reason unrelated to what liveness measures.

The lines above 152,126 are excluded for the opposite reason: **178,165 and 201,900 carry contaminated
`T0`**, and **`τ1` is built from `T0`**, so a reference measured there is selected by a clock the rule
depends on being sound.

**152,126 is the only line whose exclusions are all relevant to liveness and none of whose inclusions
are contaminated on the clock liveness uses.**

### 2.1 Derivation and application populations must be identical

**Instance A demonstrated the cost of splitting them: derive on 128,099, apply to 201,900, and the rule
delivers 2.28% against a stated 1%.** That is **a milder recurrence of the exact defect `0037`
withdrew** — calibrate on one distribution, apply to another. **A calibrated rate is only calibrated on
the population it was calibrated on.** Derive on the 152,126 and apply to the 152,126.

## 3. Weighting: one gap per pair

Not one per distinct `(account, gap)`. **Both arms independently flagged weighting as the largest
single lever in the step** — it moved the threshold to 159 d in one arm and 202 d in the other, a
bigger swing than the percentile choice. **The rule is applied per pair, so the reference is weighted
per pair.**

## 4. The quota property is accepted and disclosed

**Taking the percentile on the distribution the test applies to means the level is set by the exclusion
rate rather than by any feature of the data.** Choosing `p` mechanically fixes the exclusion rate at
`100 − p`% of measured-gap pairs. Instance A's phrasing: *"a quota rather than a finding."* Both arms
found it independently.

**That is the price of a calibrated rate, and it is disclosed rather than argued away.** The
alternative — `0036` §1's original basis — had a level anchored to typical gap behaviour and a **stated
rate that was wrong by a factor of 37**. Between a number identified by nothing and a number whose
advertised property is false, this study takes the first and says so.

**`0036` §1's conservative-direction argument survives and still points up**, but it no longer
identifies a level. **The deliverable must state this plainly.**

## 5. The inertness is accepted and disclosed

> **CORRECTED 2026-08-13 (`decisions/0039`).** As first written this section said *"the measured-gap
> test does 3.45% of the exclusions and the edge cases 96.55% — and this holds across every percentile
> from the 90th to the 99.9th."* **Both figures were wrong and the invariance claim was impossible.**
> 3.45% was measured on the **201,900** line, which §2 of this same entry had just replaced with the
> **152,126**. Both Step 7 arms found this independently on the frozen run.

**On the frozen population at the adopted 99th percentile: the measured-gap test does 5.37% of the
exclusions and `0036` §2.3's evidence-absence edge cases do 94.63%.**

**The invariance claim is WITHDRAWN. The share cannot be invariant, as a matter of arithmetic.** The
edge-case count is **constant in the percentile** — 22,496, a function of `W` alone — while the
gap-test count is `100 − p` of the 129,630 measured-gap pairs. The share therefore moves with `p` by
construction:

| Percentile | Gap-test exclusions | Edge cases | Gap-test share |
| :--- | ---: | ---: | ---: |
| 90th | ~12,963 | 22,496 | **36.5%** |
| **99th — adopted** | **1,276** | **22,496** | **5.37%** |
| 99.9th | ~130 | 22,496 | **0.4%** |

A 93-fold range. On the 128,099 line the gap test is the **majority** of exclusions at the 90th (70.1%),
so the original claim fails on every waterfall line, not merely on this one.

**The qualitative point stands at the adopted percentile, and it is what must be published.** **The
threshold is not doing most of the work** — at the 99th, `0036` §2.3's two edge-case rulings drive
roughly nineteen exclusions in twenty. A reader must not take the threshold to be doing work it is not
doing. **The deliverable states this plainly; it does not state invariance.**

## 6. The `W`-coupling is accepted; the contradicting requirement is withdrawn

`task-sheet.md` line 235 required *"do not use `W` as an input to the derivation"* and `0036` §3 said
the threshold was *"derived independently of `W`."* **After `0037` both were unsatisfiable**: any
bracketing-gap reference is selected by `τ1`, and `τ1` contains `W`.

**Both are withdrawn rather than left standing.** The threshold **is** a function of `W`, and the spec
now says so. Measured across the Step 13 arms: **408 → 576 days** on the clean sample, **885 → 973** on
the full population.

**Step 13 must refit the threshold per arm and report BOTH the refitted threshold AND the realised
exclusion rate for each.** `W` and the liveness threshold are **not independent robustness axes** and
must not be presented as if they were — a single frozen threshold would fail to deliver its stated rate
at every arm but one.

## 7. Recorded from the rerun, not ruled on

- **3,700 of the 5,209 "no instant after `τ1`" pairs (71%) have `τ1` past the end of the sweep** —
  right-censoring, not silence. Instance B measures 3,684 against the pull date; the difference is
  definitional, not a contradiction. **Step 7 derives on an uncensored population**, so this bucket is
  inflated by pairs D10 would already have removed at Step 8, where `0029` fixes right-censoring at
  position 5 and liveness at 6. *(Instance A reported the order as unwritten; it is written, in `0029`
  and `task-sheet.md` Step 8. A's substantive point stands.)*
- **The median account has 7,812 gaps** under the distinct-instants operation, against 8,247 under the
  withdrawn record-pair counting. **`0037` §2's strengthening holds either way.**

## 8. Scope

- **No threshold is adopted.** Step 7 remains an unapproved gate.
- **Zero API calls.**
- Step 8 does not launch until Step 7 is approved.
