# Step 7 — Liveness rule, rerun on ALT-BROAD (`decisions/0048`)

> **PARTIALLY SUPERSEDED — `decisions/0054`, `0055`, `0056`, `0057`, `0058`. The rule is unchanged.**
>
> **This stamp is NEGATIVE ONLY. It restates no corrected figure** — `0058`, from Red Team finding 7:
> a stamp containing the corrected string guarantees the positive grep passes whether or not the body
> was fixed. **The corrected figures are in the GENERATED block below**, written from the stored
> counts by `src/step7_regenerate_derived.py`, which then verifies numerically, at both precisions,
> that no superseded value survives anywhere in this deliverable.
>
> **Every occurrence of these strings in the prose below is superseded**, and each is marked inline:
> `9.6830` · `0.0503` · `0.3575` *(as a bound WIDTH)* · `73.3466` · `73.6537` · `11.3619` ·
> `0.0672` *(as a bound WIDTH)* · `82.4327` · `0.4033`.
>
> **Two of those strings have a LEGITIMATE reading in this file and are deliberately NOT marked
> there:** `0.3575%` and `0.0672%` as **shares of population** — `703 / 196,654` and `99 / 147,370`.
> Same string, two meanings, one live. **The register is in `second-brain`'s glossary.**
>
> **What is positively unchanged is listed, not implied:** the exclusion counts (APPLY 703 = 604 + 99;
> DERIV 99 = 0 + 99), the never-started bound, and the three outcome **point estimates** — including
> `started_and_left = 19,042` on APPLY, which is a **point estimate, not the bound floor**, and does
> not move. **This stamp certifies nothing else.**

**Instance:** `bb_a` (namespace `a`), dual implementation.

<!-- BEGIN GENERATED: derived figures -- src/step7_regenerate_derived.py -->

## Derived figures — GENERATED, do not hand-edit

**Every number in this section is a function of the counts below and is written by
`src/step7_regenerate_derived.py`.** It exists because four consecutive decisions
corrected these artifacts by patching individual values, and every finding in Red Team
reviews 9–11 was a value a patch reached in one place and missed in another.

**The channel window is `(τ1, τ2)`, OPEN at `τ2`** (`0057`).

### APPLY — n = 196,654

**Counts, the only inputs:** never-started 33,373 · Continued 144,140 · started-and-left 19,141 · exclusions 604 + 99 = 703 · **channel 90**.

| Bound | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 32,769 → 16.6633% | 33,373 → 16.9704% | 0.3071 pp |
| **Started and left** | **18,952 → 9.6372%** | 19,745 → 10.0405% | **0.4032 pp** |
| *conditional sub-interval — NOT a bound* | *18,952 → 9.6372%* | *19,141 → 9.7333%* | *0.0961 pp* |
| Continued | 144,140 → 73.2962% | 144,933 → 73.6995% | 0.4032 pp |

| Attainable corner | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| NS floor / S&L ceiling | 16.6633% | 73.2962% | 10.0405% |
| NS ceiling / S&L floor | 16.9704% | 73.3924% | 9.6372% |

**Three ceilings sum to 100.7104%**, excess 0.7104 pp = 2 x 604 + 99 + 90 = 1397 pairs.
**Exclusion share of population: 0.3575%** — this is where `0.3575` is CORRECT, and it is why that string is not in the superseded list.

### DERIV — n = 147,370

**Counts, the only inputs:** never-started 9,145 · Continued 121,382 · started-and-left 16,843 · exclusions 0 + 99 = 99 · **channel 89**.

| Bound | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 9,145 → 6.2055% | 9,145 → 6.2055% | 0.0000 pp |
| **Started and left** | **16,655 → 11.3015%** | 16,843 → 11.4291% | **0.1276 pp** |
| *conditional sub-interval — NOT a bound* | *16,655 → 11.3015%* | *16,843 → 11.4291%* | *0.1276 pp* |
| Continued | 121,382 → 82.3655% | 121,570 → 82.4930% | 0.1276 pp |

| Attainable corner | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| NS floor / S&L ceiling | 6.2055% | 82.3655% | 11.4291% |
| NS ceiling / S&L floor | 6.2055% | 82.4930% | 11.3015% |

**Three ceilings sum to 100.1276%**, excess 0.1276 pp = 2 x 0 + 99 + 89 = 188 pairs.
**Exclusion share of population: 0.0672%** — this is where `0.0672` is CORRECT, and it is why that string is not in the superseded list.

### Bound ÷ sampling width — TWO CONVENTIONS, NOT RECONCILED

**This arm (`a`) divides by the CI width of the FLOOR ENDPOINT's own bootstrap distribution.** The other arm divides by the CI width of the UNDER-THE-RULE point estimate. **The spec fixes neither, so this is a spec ambiguity and is reported, not resolved** — `0057` wrote the other arm's denominator into this file and `0058` reverted it. *(A sentence here cited the never-started ratio as proof of correct divergence. **Withdrawn by `0061`: it was false** — that pair was one convention on two bootstraps, and it was itself an instance of the defect it was cited to certify.)*

| | Denominator | Bound ÷ it | Sub-interval ÷ it |
| :--- | ---: | ---: | ---: |
| APPLY | 0.7602 | **0.5304** | 0.1264 |
| DERIV | 0.9744 | **0.1309** | 0.1309 |

*(A sentence here claimed the arm's own published ratio was **retained in place above and marked superseded**. **Withdrawn by `0061`** — it was the same hard-coded literal `0059` removed from the JSON half after finding that nothing checked it and it was false, and it is false on its face for arm `b`, whose published ratio IS its current one. It survived in the `.md` writer because the numeric controls cannot see a claim.)* **The limit that IS real and is stated rather than hidden: the denominator above is the CI of the PRE-widening floor point and was not re-bootstrapped; the recomputation reuses it.**

### Per-`W` series — NOT regenerated, and that is a scope statement

**The per-`W` sensitivity series in this deliverable was computed under the CLOSED channel window `(τ1, τ2]` and under the un-widened floor, at every arm.** It is not recomputed here because only `W = 108` masks are on disk. **Step 13 is the consumer and must recompute it**, and it must not be read as current at any arm.

**The inertness of the window form is asserted at `W = 108` only** (open 90 vs closed 90 on APPLY; open 89 vs closed 89 on DERIV). **It is NOT expected to hold at `W = 213`**, where D10 forces `τ1 ≤ τ_pull − 91 d` so `τ2` sits at or adjacent to `τ_pull`, and a mass point in last-insertion instants sits there. (`src/step7_floor_extremes.py`, `0057` §5.)

<!-- END GENERATED: derived figures -->

**Status: GATE. This artifact proposes and measures. It adopts nothing and approves nothing.**
**API calls: 0.** The stored Step 5 calibration was read, never refitted.

---

## 0. The rule as run

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND the pair is NOT Continued.**

**Continued** is Step 1 §7 as amended by `0034`: `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`,
with `|A|` read at `τ1` and `A_H` read at `τ2 = ⟦T0⟧ + (W + H) × 24h`. Every boundary test is the
half-open UTC-instant form `watched_at < τ`. Distinct episodes are counted, never play events, with
the canonical timestamp of an episode the minimum `watched_at` across its records, and membership by
**set** against `E2`.

Conjunct 2 therefore selects **both nulls** and only the nulls:

| State | Basis | Reached by the rule |
| :--- | :--- | :--- |
| Never started, `\|A\| = 0` | null | yes |
| Started and left, `\|A\| ≥ 1` ∧ ¬Continued | **null on exit** — `\|A\| ≥ 1` is observed, the failure to meet the Continued condition is not | yes |
| Continued | the only state resting on positive evidence | never |

Insertion instant is `np.interp(play_id, …)` against `processed/step5/calibration.npz`. Insertion time
is not claimed `watched_at` (`0021`). The filter is **pair-level, anchored at that pair's `τ1`**
(`0034`); evidence is account-wide; **no user is ever dropped wholesale**. `W = 108`, `H = 91`.

**Tie convention (judgement call, spec-silent).** "After `τ1`" is read strictly, so NOT LIVE requires
`max(instant) ≤ τ1`. Measured to be non-load-bearing: **0 pairs on either population** have a last
instant equal to `τ1` or within one second of it.

---

## 1. Populations — every figure below states which one produced it

The Step 5 waterfall was recomputed from `pair_revision5.csv` and asserted equal to the published
`201,900 / 178,165 / 155,131 / 152,126 / 128,099` before any figure was taken.

| | Definition | Pairs | Accounts |
| :--- | :--- | ---: | ---: |
| **DERIV** | Step 5 line 4 less D10. **Requires S2 evidence.** | **147,370** | 2,402 |
| **APPLY** | Step 5 line 1 less D10. **What Step 8 filters at position 6.** | **196,654** | 2,422 |

D10 is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, run at position 5, **before** liveness at position 6.
The `L2 = 1` exclusion was checked and is a no-op on both populations.

---

## 2. Exclusion counts — prior measurement CONFIRMED

**The claim put to this rerun was 99 on DERIV from 73 accounts and 703 on APPLY from 216. Both are
confirmed exactly, on pairs and on accounts.**

| At `W = 108` | **DERIV** (147,370) | **APPLY** (196,654) |
| :--- | ---: | ---: |
| **Excluded pairs** | **99** | **703** |
| Excluded accounts | **73** | **216** |
| — never-started component | **0** (0 accounts) | **604** (191 accounts) |
| — started-and-left component | **99** (73 accounts) | **99** (73 accounts) |
| — continued component | 0, by construction | 0, by construction |
| Share of population *(these two are the LEGITIMATE readings of `0.0672` and `0.3575` — registered false positives; do not "correct" them)* | 0.0672% | 0.3575% |

48 accounts on APPLY contribute to **both** components. On both populations, exactly **one** account
has every one of its pairs excluded; the other 72 / 215 are excluded on one show and live on another.
That is `0034`'s pair-level anchoring doing visible work, and it is why the rule must not be
implemented at user level.

**How the rule selects, under ALT-BROAD** (this differs from the ALT decomposition the record carries):

| | DERIV | APPLY |
| :--- | ---: | ---: |
| Population | 147,370 | 196,654 |
| After conjunct 2, **NOT Continued** | 25,988 | **52,514** |
| After both conjuncts | **99** | **703** |
| Conjunct 1 alone (no insertion after `τ1`) | 751 | 1,355 |

**Conjunct 1 still does almost all of the work** — that is why the count moves with `W` at all.

**The exclusion set is NOT a subset of "pairs with no S2 record anywhere" under ALT-BROAD.** APPLY holds
23,260 such pairs; 604 are excluded and **22,656 stay live**; and **99 excluded pairs do hold S2
records**, by definition of the started-and-left component. Under ALT the subset relation held. It no
longer does, and any downstream check asserting it will fail on correct data.

**Rule comparison at `W = 108`:**

| | DERIV | APPLY |
| :--- | ---: | ---: |
| PF-LIMIT (silence alone) | 751 | 1,355 |
| ALT (silent ∧ `\|A\| = 0`) | 0 | 604 |
| **ALT-BROAD (silent ∧ ¬Continued)** | **99** | **703** |
| Confirmed continuers PF-LIMIT would have deleted | 652 | 652 |

**The dual control is informative for the first time.** Under ALT the DERIV diff was literally `0 = 0`
at every arm; here it is **99 against 99, from 73 accounts**.

---

## 3. The three outcome shares, under the rule and against no filter

**DERIV — 147,370 pairs**

| | Never started | Continued | Started and left | Pairs |
| :--- | ---: | ---: | ---: | ---: |
| No liveness filter | 9,145 — **6.2055%** | 121,382 — **82.3655%** | 16,843 — **11.4291%** | 147,370 |
| **Under the rule** | 9,145 — **6.2096%** | 121,382 — **82.4208%** | 16,744 — **11.3695%** | 147,271 |
| **Movement** | **+0.0042 pp** | **+0.0554 pp** | **−0.0595 pp** | −99 |

**APPLY — 196,654 pairs**

| | Never started | Continued | Started and left | Pairs |
| :--- | ---: | ---: | ---: | ---: |
| No liveness filter | 33,373 — **16.9704%** | 144,140 — **73.2962%** | 19,141 — **9.7333%** | 196,654 |
| **Under the rule** | 32,769 — **16.7231%** | 144,140 — **73.5592%** | 19,042 — **9.7177%** | 195,951 |
| **Movement** | **−0.2474 pp** | **+0.2630 pp** | **−0.0156 pp** | −703 |

Movements are differenced from unrounded shares; differencing the rounded ones moves the last digit.
All six paired account-clustered 95% intervals (B = 4,000, seed 20260813, accounts resampled with all
their pairs) exclude zero — on APPLY, never-started `[−0.2995, −0.2010]`, started-and-left
`[−0.0272, −0.0046]`.

**Note the DERIV never-started share RISES while no never-started pair is excluded.** That is pure
denominator movement, and it is the clearest available illustration of why an endpoint must be
computed on the same population as its estimand.

**`0048` §3's two signed figures are reproduced exactly: UP 0.0042 pp on DERIV, DOWN 0.2474 pp on
APPLY.** The sign is population-dependent, as the entry says.

---

## 4. Bound 1 — never started, on ONE denominator, unchanged from ALT

**Estimand:** the share of the **position-5 APPLY population, 196,654 pairs**, whose true state is
Never started. **Both endpoints are computed on that same 196,654.**

| | Numerator | Share |
| :--- | ---: | ---: |
| **Floor** — all 604 excluded never-started nulls in truth started | 32,769 | **16.6633%** |
| **Ceiling** — all 604 are true declines | 33,373 | **16.9704%** |
| **Width** | 604 | **0.3071 pp** |

**Identical to the ALT bound `[16.6633%, 16.9704%]` published at `0047` §3, and the reason is
structural: the 99 started-and-left exclusions have `|A| ≥ 1` OBSERVED, so they cannot enter either
endpoint.** The never-started component of ALT-BROAD's exclusion set *is* ALT's exclusion set.

**The identity claim needs restating, and this is a defect in the record.** The ceiling still equals
the unfiltered never-started share, because the ceiling numerator is the unfiltered numerator over the
unfiltered denominator. But `0046` §4's *phrasing* — "returning every excluded pair as a decliner
reproduces the unfiltered population exactly" — **is false under ALT-BROAD**. Returning all 703 as
decliners gives 17.3279%, which is **not attainable**, because 99 of them are observed to have started.
That phrasing was a property of ALT and must not be carried into Step 9 unedited.

On **DERIV** the bound is degenerate: the never-started component is 0, so floor = ceiling =
**6.2055%** on 147,370, width 0 pp.

---

## 5. Bound 2 — started and left. NEW, and the estimand question is the whole of it

`0048` §5 requires "a second bound on the started-and-left share, over the 99". **Taking that
literally produces an interval that is not a bound**, and this section says so before publishing
anything.

Under the rule, per excluded pair, what is unresolved is:

- **the 604 never-started nulls** — truth may be Never started, Started-and-left **or** Continued. They
  can only *leave* the never-started numerator and can only *enter* the other two.
- **the 99 started-and-left nulls** — `|A| ≥ 1` is observed, so the pair **did** start. Truth is
  Started-and-left or Continued. They can only *leave* the started-and-left numerator.

So the started-and-left numerator on APPLY ranges over **19,141 − 99 = 19,042** to
**19,141 + 604 = 19,745**.

**OPERATIVE — Bound 2, started and left, APPLY, denominator 196,654:**

| | Numerator | Share |
| :--- | ---: | ---: |
| ~~**Floor** — all 99 in truth continued~~ ***SUPERSEDED `0056`*** | ~~19,042~~ **18,952** | ~~**9.6830%**~~ **9.6372%** |
| **Ceiling** — all 99 are true exits **and** all 604 in truth started and left | 19,745 | **10.0405%** |
| ~~**Width**~~ ***SUPERSEDED `0056`*** | ~~703~~ **793** | ~~**0.3575 pp**~~ **0.4032 pp** |

On **DERIV**, denominator 147,370: ~~**[11.3619%, 11.4291%]**, width **0.0672 pp**~~ ***SUPERSEDED (`0055`): [11.3015%, 11.4291%], width 0.1276 pp*** — narrow because the
never-started component is empty there, so only the 99 float.

***SUPERSEDED (`decisions/0056`): the conditional sub-interval is [9.6372%, 9.7333%], width 0.0961 pp,
over the 99 AND the 90.*** The conditioning constrains the **604** and says nothing about the 90, so the
sub-interval floor moves with the bound floor. **`9.6830%` has no legitimate reading under the adopted
rule.** The paragraph below is the original text and its reasoning about the CEILING stands unchanged.

~~**The "over the 99 only" interval is [9.6830%, 9.7333%], width 0.0503 pp** — and it is NOT a bound on the
unconditional estimand.~~ Its ceiling does not cover the case in which an excluded never-started null
in truth started and left, which is a case the filter exists precisely to allow for. Publishing it as
*the* second bound would be **the fourth consecutive bound in this chain whose endpoint fails to cover
the case the filter guards against** — `0043`'s ceiling, `0045`'s floor, `0046`'s floor, and then this.
It is published here **only** as the decomposition of Bound 2's lower half, and labelled as a bound on
a **conditional** estimand: the started-and-left share *given* that every never-started null is a true
decline.

**Both bounds are simultaneously tight, and the corners are attainable resolutions of the same
population** (each verified to sum to 196,654 exactly, in integer arithmetic):

| Resolution | Never started | Continued | Started and left | |
| :--- | ---: | ---: | ---: | :--- |
| All 604 started and left; all 99 are true exits | **16.6633%** (floor) | 73.2962% | **10.0405%** (ceiling) | unchanged — the 90 are already started-and-left here |
| All 604 are true declines; all 99 **and all 90 channel pairs** in truth continued | **16.9704%** (ceiling) | **73.3924%** | **9.6372%** (floor) | *corrected `0056`* |
| ~~All 604 are true declines; all 99 in truth continued~~ | ~~16.9704%~~ | ~~73.3466%~~ | ~~9.6830%~~ | ***SUPERSEDED*** — omits the 90 |

**Bound 3, Continued, for completeness:** ***SUPERSEDED (`0054`, `0055`): APPLY [73.2962%, 73.6995%],
DERIV [82.3655%, 82.4930%]*** — both ceilings move with the floor, since the same 90 / 89 may be
Continued. ~~APPLY [73.2962%, 73.6537%], DERIV [82.3655%, 82.4327%].~~ Continued is the only state no exclusion can leave; both other states can
only flow into it.

**The bounds are identified sets, not confidence intervals.** For scale, on APPLY the never-started
bound is **0.28×** the account-clustered sampling width of the share it bounds, and the
started-and-left bound is ~~**0.47×**~~ ***SUPERSEDED (`0056`)*** — that ratio was computed on the
withdrawn 0.3575 pp width. ~~**On the adopted 0.4032 pp bound over the 0.7922 pp account-clustered
width the ratio is 0.5090, i.e. 50.9%.**~~ ***STRUCK (`0059`): `0.7922` IS THE OTHER ARM'S
DENOMINATOR.*** **This arm divides by the floor endpoint's own bootstrap CI, `0.7602`, giving
`0.4032 / 0.7602 = 0.5304`** — see the generated block above, which is written from this arm's own
inputs. **The two arms use different conventions, the spec fixes neither, and the divergence is
REPORTED not reconciled** (`CLAUDE.md`).
~~The never-started ratio was correctly left divergent at `0.2813` against `0.27211` in these same
files, which is the proof this one should have been.~~ ***WITHDRAWN (`0060`): that sentence was false
and was itself an instance of the defect it was cited to certify.*** **`0.2813` is `0.307138 / 1.092`,
and `1.092` is the UNDER-THE-RULE point estimate's CI — the OTHER arm's convention.** So `0.2813`
against `0.27211` was **one convention on two arms' bootstraps**, not two conventions diverging, which
is why they sit 0.009 apart while the genuine two-convention pair sits 0.021 apart. **Arm a was running
two conventions in one six-line block.** **This arm's never-started ratio is now `0.307138 / 1.09 =
0.2818` on its own floor-endpoint CI**, matching its started-and-left convention, and the genuinely
divergent pair is **0.2818 (a) against 0.2721 (b)**.
**Sampling error still dominates, but by roughly half as much as originally stated.**

---

## 6. Waterfall — line 6 is outcome-conditional, and the monotone rationale has gone stale

| Position | DERIV | APPLY |
| :--- | ---: | ---: |
| 4 — contamination exclusion | 152,126 | 201,900 |
| 5 — right-censoring D10 | **147,370** (−4,756) | **196,654** (−5,246) |
| 6 — **liveness (OUTCOME-CONDITIONAL)** | **147,271** (−99) | **195,951** (−703) |
| — of which never started | 0 | 604 |
| — of which started and left | 99 | 99 |
| — of which continued | 0 | 0 |

**Line 6 must be published with that split.** Conjunct 2 is "NOT Continued", a position-7 outcome
predicate, so the removed count cannot be stated without reference to outcome assignment — and under
ALT-BROAD it removes rows from **two** outcome states, not one. An implementation reporting line 6 as a
single number is not reproducible against one that reports the split.

**Ordering.** Outcome assignment is evaluated before liveness applies. That is permitted: both are
**row-local predicates on the position-5 output and commute exactly** — checked here, not asserted, by
computing the surviving state counts both ways on both populations (identical). `0029`'s ordering
rationale concerns per-filter sample size, which cannot reach position 7, because **outcome assignment
removes no rows.**

> ### DEFECT — `0047` §6 and `task-sheet.md` line 261 are stale
>
> Both read: *the monotone-decrease invariant holds only NON-STRICTLY where the exclusion set is empty,
> **which it is on DERIV.*** **Under ALT-BROAD the DERIV exclusion set is not empty — it is 99 — and
> decrease is STRICT on both populations at every arm tested (38 through 213).**
>
> The `>=` invariant adopted at `0047` §6 should be **kept**, because strictness is a fact about this
> pull date rather than a theorem. But its stated reason no longer holds, and an implementation that
> reads the reason rather than the invariant will assert the wrong thing.

---

## 7. `W`-coupling per arm, started-and-left component reported separately

**D10 contains `W`, so the censored population differs per arm. Both readings are given and each names
itself** (`0047` §5). The mandated grid is `0027`'s 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213; 60, 100,
125 and 180 are extra, and 125 and 180 are the two off-grid arms `0047` §5 quoted without their arms.

**D10 RE-DERIVED AT EACH ARM — the operative reading**

| `W` | Grid | DERIV pop | DERIV excl. | ns | **sl** | APPLY pop | **APPLY excl.** | ns | **sl** | APPLY accounts |
| ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | ✓ | 147,685 | 52 | 0 | 52 | 197,007 | **537** | 485 | 52 | 177 |
| 46 | ✓ | 147,685 | 56 | 0 | 56 | 197,007 | **550** | 494 | 56 | 182 |
| 60 | | 147,685 | 65 | 0 | 65 | 197,007 | 592 | 527 | 65 | 188 |
| 77 | ✓ | 147,685 | 79 | 0 | 79 | 197,007 | **633** | 554 | 79 | 197 |
| 91 | ✓ | 147,685 | 89 | 0 | 89 | 197,007 | **664** | 575 | 89 | 207 |
| 100 | | 147,518 | 94 | 0 | 94 | 196,829 | 686 | 592 | 94 | 211 |
| 107 | ✓ | 147,384 | 98 | 0 | 98 | 196,674 | **701** | 603 | 98 | 215 |
| **108** | ✓ | **147,370** | **99** | **0** | **99** | **196,654** | **703** | **604** | **99** | **216** |
| 125 | | 147,049 | 111 | 0 | 111 | 196,276 | 736 | 625 | 111 | 233 |
| 150 | ✓ | 146,602 | 125 | 0 | 125 | 195,689 | **789** | 664 | 125 | 243 |
| 180 | | 145,845 | 135 | 0 | 135 | 194,617 | 818 | 683 | 135 | 243 |
| 213 | ✓ | 144,852 | **147** | 0 | **147** | 193,270 | **864** | 716 | **148** | 253 |

**`0048` §5's APPLY row is reproduced exactly: 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864.**
The started-and-left component runs **52 / 56 / 79 / 89 / 98 / 99 / 125 / 148** on APPLY — a factor of
**2.85** across the grid against the whole rule's **1.61×**, so the component `0048` added grows
faster than the rule it was added to. On DERIV the exclusion set is **entirely** that component, and it
runs **52 / 56 / 79 / 89 / 98 / 99 / 125 / 147**.

> ### DEFECT — `0048` §5's started-and-left series is the APPLY reading and does not say so
>
> At `W = 213` the component is **148 on APPLY but 147 on DERIV**. At every other mandated arm the two
> populations agree, which is exactly what makes the single unlabelled series look safe. It is the
> standing rule of `0046` §0 in the same dimension the entry itself corrected at §7.

**D10 FROZEN AT `W = 108` — the other reading, reported so the two are not confused**

| `W` | 38 | 46 | 77 | 91 | 107 | 108 | 125 | 150 | 180 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY, total | 536 | 549 | 632 | 662 | 701 | 703 | 746 | 823 | 918 | 1,117 |
| APPLY, **ns component** | 484 | 493 | 553 | 574 | 603 | 604 | **632** | **684** | **753** | **881** |
| APPLY, sl component | 52 | 56 | 79 | 88 | 98 | 99 | 114 | 139 | 165 | 236 |
| DERIV, total | 52 | 56 | 79 | 88 | 98 | 99 | 114 | 139 | 165 | 234 |

**`0047` §5's frozen figures 632 / 684 / 753 / 881 are reproduced exactly, and they are the
never-started component at `W` = 125 / 150 / 180 / 213** — confirming `0048` §7's arm attribution.
Under ALT-BROAD the frozen totals at those arms are **746 / 823 / 918 / 1,117**. Only 150 and 213 are in
the mandated grid.

---

## 8. Bounding the calibration residual for the excluded set

Required by `0048` §9 and not previously done. Conjunct 1 is a comparison between an **interpolated**
instant and `τ1`; if the curve reads **early**, a live account is scored silent and the pair is
**falsely excluded**. Both facts on the record were re-measured here rather than assumed.

**Both instance-B measurements are CONFIRMED to the digit.**

| Claim | Measured |
| :--- | :--- |
| 22.68% of dated records claim a `watched_at` later than their own calibrated instant, 6,271,584 of 27,656,434 | **6,271,584 of 27,656,434 = 22.6768%. CONFIRMED.** |
| 5,094 records clamped above the calibration range | **5,094. CONFIRMED.** (also 1,862 clamped below) |

**But the size of the discrepancy is what bears weight, and it was never stated.** For the 6.27M records
claiming a later `watched_at`, the gap is **median 0.0205 days — about 30 minutes** — p75 0.046 d, p90
0.141 d. It only becomes large in a thin tail: p95 77.5 d, p99 470.6 d. The same shape holds for the
calibration residual measured on the fit family (checkin + scrobble, where `watched_at` *is* the
insertion time): **median |r| 0.0195 d, p90 |r| 0.107 d, 91.5% within one day**, against a tail of
p95 124.6 d and p99 472.9 d. The stored held-out figures agree on the core: median lag 0.0026 d,
90.6% within seven days. *(In-sample caveat: the stored curve was fitted on this family, so these
residuals understate the true error; the held-out figures are the honest ones and they are quoted.)*

**The clamp concern is real in principle and INERT here.** Clamped records receive the last knot time,
**2026-08-10T20:48Z**. D10 forces `τ1 ≤ τ_pull − H × 24h = 2026-05-12` at **every** arm, so a clamped
account's instant is later than any `τ1` the rule can read and the account is **live everywhere**.
Checked directly: 66,961 APPLY pairs sit on clamped accounts and **0 of them are excluded**.

### 8.1 Margins — how far the exclusions sit from the boundary

`τ1 − max(instant)`, in days, for excluded pairs. An exclusion survives any residual correction smaller
than its own margin.

| | DERIV (99) | APPLY (703) |
| :--- | ---: | ---: |
| min | 0.0699 d | **0.0137 d** |
| p25 / **median** / p75 | 35.9 / **81.3** / 107.1 d | 74.8 / **170.9** / 350.3 d |
| never-started component, median | — | **202.5 d** |
| started-and-left component, median | **81.3 d** | **81.3 d** |
| within 0.0195 d (residual median) | **0** | **1** |
| within 1 d | 1 | 2 |
| within 7 d | 5 | 17 |
| within 30 d | 19 | 68 |
| within 90 d | 56 | 210 |

The opposite direction, `max(instant) − τ1` for the **live** pairs that could flip — live **and not
Continued**, since a Continued pair fails conjunct 2 whatever the instant does — has minimum
**0.75 d** on APPLY and **1.07 d** on DERIV, median about 1,860 / 2,020 days. **2 live APPLY pairs sit
within a day of the boundary and 14 within a week.**

### 8.2 Uniform shift, and the non-parametric correction

**A. Uniform shift `+δ` on every instant** — a positive `δ` corrects a curve reading early, so it can
only remove exclusions. APPLY exclusions:

| `δ` (days) | 0 | 0.0195 | 0.107 | 1 | 7 | 30 | 77.5 | 124.6 | 365 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Excluded | **703** | 702 | 701 | 701 | 686 | 635 | 523 | 414 | 163 |
| Retained | — | 99.9% | 99.7% | 99.7% | 97.6% | 90.3% | 74.4% | 58.9% | 23.2% |

At the residual's **median** the set moves by one pair; at a full **week** it retains 97.6%. It only
degrades under shifts of tens to hundreds of days — i.e. under the tail, not the body, of the residual.
**DERIV's 99 are less robust:** 94 at `δ = 7 d`, 80 at 30 d, 15 at 124.6 d.

**B. Non-parametric correction — the strongest test, and it needs no magnitude assumption at all.** A
genuine record cannot be inserted before it was watched, so for every dated record the true insertion
instant is at least `max(interp(rid), watched_at)`. Taking the account-wide maximum of that lower bound
absorbs the entire 22.68% finding in one step:

`last_inst' = max( interp(max rid), max dated watched_at ≤ τ_pull )`

| | DERIV | APPLY |
| :--- | ---: | ---: |
| Pairs whose account instant moved later | 59,501 | 79,370 |
| Median move, where moved | 0.026 d | 0.026 d |
| **Exclusions after correction** | **97 of 99 (97.98%)** | **700 of 703 (99.57%)** |
| Lost | 2 (both started-and-left) | 3 (1 never-started, 2 started-and-left) |
| **New exclusions created** | **0** | **0** |

**Verdict: the exclusion set is stable under plausible residual.** Under the correction that requires
only the residual's *direction* and no assumption about its size, **99.57% of the APPLY set and 97.98%
of the DERIV set survive, and not one new exclusion is created.** The never-started component — the
component the Step 9 never-started bound rests on — moves from 604 to 603, which shifts the bound's
floor by roughly 0.0005 pp against a width of 0.3071 pp.

**Where the residual cannot be measured directly, and this is the honest limit of the test.** Of the 703
excluded APPLY pairs, **525 sit on accounts whose own last record is a `watch`** — the import family,
whose `watched_at` carries no information about insertion time — and only **178 on accounts whose last
record is a checkin or scrobble**. For those 178 the residual **at exactly the point the rule reads** is
directly measurable and tight: p5 −0.143 d, median +0.001 d, p95 +0.023 d. *(One account shows
+4,347 d — the curve reading **late**, which pushes toward false liveness, not false exclusion, and the
pair is excluded anyway.)* For the 525 the uniform-shift and non-parametric tests above are the whole of
the evidence.

---

## 9. Judgement calls the spec does not settle, stated

1. **"After `τ1`" is strict** — a tie does not prove liveness. 0 ties on either population, so this is
   non-load-bearing.
2. **`max(instant)` is computed as `interp(max rid)`**, valid because `np.interp` is monotone
   non-decreasing in `rid`. Cross-checked against the stored per-account instant sequence: max absolute
   difference 0 seconds.
3. **Insertion evidence is account-wide** (all shows, all seasons) per `0021`; the *test* is
   pair-level per `0034`.
4. **Arms.** `0027`'s grid plus 60, 100, 125 and 180. 125 and 180 are included only so `0047` §5's
   frozen figures can be reproduced with their arms attached; they are marked off-grid everywhere.
5. **The calibration residual is measured in-sample on the fit family**, because refitting is
   forbidden. This understates the error and is labelled at every point of use; the stored held-out
   figures are quoted beside it.
6. **The non-parametric correction (§8.2 B) assumes only that a record is not inserted before it is
   watched.** Records dated at or after `τ_pull` are excluded from it, consistent with D11.
7. **The stability tests are run at `W = 108` only.** They are not repeated at every arm; the margin
   distribution would have to be re-read per arm to claim arm-wide stability, and this artifact does
   not claim it.
8. **Bound 2 is published on the unconditional estimand**, with the literal "over the 99" interval
   demoted to a labelled decomposition. The spec's wording admits the narrower reading; §5 argues the
   narrower reading is not a bound.

---

## 10. Defects found in the record — reported, not reconciled

- **D-1. `0047` §6 and `task-sheet.md` line 261 are stale.** "The exclusion set is empty, which it is
  on DERIV" is false under ALT-BROAD: it is 99, and decrease is strict on both populations at every
  tested arm. Keep the `>=` invariant; fix its stated reason.
- **D-2. `0048` §5's started-and-left series `52 / … / 148` is the APPLY reading, unlabelled.** DERIV
  gives **147** at `W = 213`. A figure without its population, in the entry that made stating the
  population a standing rule.
- **D-3. `0046` §4's identity phrasing does not survive the rule change.** "Returning every excluded
  pair as a decliner reproduces the unfiltered population exactly" was a property of ALT. Under
  ALT-BROAD it yields 17.3279%, which is unattainable. The ceiling identity itself holds, by a
  different route (§4). Step 9 reads this sentence.
- **D-4. `task-sheet.md` line 466 quotes ALT's share movements under an ALT-BROAD heading.** It gives
  `−0.2558 / +0.2258 / +0.0300 pp`; **measured under ALT-BROAD on APPLY the three shares move
  `−0.2474 / +0.2630 / −0.0156 pp`.** It also says "the 99 move the started-and-left share by roughly
  0.05 pp" — ~~0.0503 pp~~ ***the conditional sub-interval is 0.0961 pp wide (`0056`)***, a different quantity from
  the share movement, which is **−0.0156 pp**. **The point stands; the number was superseded when the floor widened.**
- **D-5. `task-sheet.md` lines 253 and 262 still describe conjunct 2 as `|A| = 0`,** and give ALT's
  decomposition `196,654 → 33,373 → 604`. Under ALT-BROAD conjunct 2 is "NOT Continued" and the
  decomposition is `196,654 → 52,514 → 703`. An instance following those lines computes ALT.
- **D-6. This instance was launched with a `data-scientist.md` copy that still carried the superseded
  ALT rule** — `|A| = 0`, "0 on DERIV, 604 on APPLY", per-arm 485–716, "every liveness exclusion is
  never-started by construction". **The file on disk has been updated per `0048` §8 and is correct**;
  the launch prompt also carried the correct rule, so nothing was run on the stale text. Recorded
  because a dual pair launched from cached definitions could diverge for a reason that is an artifact
  of the record.

---

## 11. What this gate still cannot establish

- **That the rule is right.** Its warrant is an argument, not a measurement. `0048` §9's narrowing of
  Red Team item 2 stands: `0021` licenses "insertion after `τ1` ⟹ live" as a **sufficient** condition;
  the rule is a **biconditional**, and the converse is asserted, not established.
- **That Step 8's position-6 population is the one reconstructed here.** APPLY was built from the Step 5
  pair table, not through Step 8's positions 1–5. **703 on APPLY is an expected value for the Step 8
  diff; a mismatch is a population defect first** (`0047` §7) — check the frame join, the `L2 = 1`
  exclusion and the censoring before suspecting the rule.
- **That two implementations agree.** That is the Human Lead's diff against instance `b`, which this
  instance has not seen and has not looked for.
- **Arm-wide residual stability** (§9.7).

---

## 12. Files

| Path | Contents |
| :--- | :--- |
| `artifacts/step7-liveness-bb-a.json` | every figure in this document, machine-readable |
| `artifacts/step7-liveness-bb-a.md` | this document |
| `processed/step7/bb_a/` | population, instants, arms, bounds, checks, residual, stability, bootstrap |
| `src/step7_bb_a_1_population.py` … `_8_deliver.py` | the eight stages, in order |

No usernames, user IDs or individual watch histories appear in `artifacts/`. Row-level masks and the
per-account instant arrays stay in `processed/`.

**Gate. Nothing here is adopted. Returned to the Human Lead.**
