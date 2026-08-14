# Step 7 — Liveness rule, rerun on ALT-BROAD (`decisions/0048`)

> **PARTIALLY SUPERSEDED — stamped 2026-08-14 (`decisions/0055`). The rule is unchanged; two DERIV
> endpoints and one APPLY endpoint are not.**
>
> **This file is the deliverable for the ADOPTED rule (ALT-BROAD), and its DERIV bound is the one figure
> in it that the adopted rule no longer supports.** The corrected values were computed under the
> **reverted** ALT-MATCHED rule and sit in `step7-liveness-mm-{a,b}.md`; both `data-scientist` arms have
> since re-confirmed them from their own masks (`step7-deriv-floor-check-{a,b}.md`).
>
> | | Printed below | Adopted (`0054`, `0055`) |
> | :--- | ---: | ---: |
> | **APPLY** started-and-left bound | `[9.6830%, 10.0405%]`, width 0.3575 pp | **`[9.6372%, 10.0405%]`, width 0.4032 pp** |
> | **APPLY** Continued ceiling | 73.6537% | **73.6995%** |
> | **DERIV** started-and-left bound | `[11.3619%, 11.4291%]`, width 0.0672 pp | **`[11.3015%, 11.4291%]`, width 0.1276 pp** |
> | **DERIV** Continued ceiling | 82.4327% | **82.4930%** |
>
> **Why:** the floor must admit that the channel pairs — **90 on APPLY, 89 on DERIV**, ¬Continued, live
> only because they inserted after `τ1`, last insertion inside `(τ1, τ2]` — **may in truth be
> Continued**, since they could produce no evidence dated after that instant. **The ceilings do not
> move; the widening is one-sided.**
>
> **Everything else in this file stands**, including the exclusion counts (APPLY 703 = 604 + 99;
> DERIV 99 = 0 + 99), the never-started bound `[16.6633%, 16.9704%]`, and every point estimate.



**Instance:** `data-scientist-b`, namespace `bb_b` · **Date:** 2026-08-14 · **API calls: 0**

> **THIS IS A GATE. NOTHING HERE IS ADOPTED.** The rule statement below is the one the Human Lead
> adopted at `decisions/0048`; every figure attached to it is a proposal for the Human Lead to
> approve and to diff against the other arm. This instance adopts nothing and did not read the
> other arm's work.

Machine-readable companion: `artifacts/step7-liveness-bb-b.json`.
Row-level intermediates: `processed/step7/bb_b/`.

---

## 1. The rule, as measured

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND the pair is NOT Continued.** Otherwise it is live.

**Continued** is Step 1 §7 as amended by `0034`: `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`,
read at `τ2 = ⟦T0⟧ + (W + H) × 24h`. So conjunct (b) is satisfied by **both** Never started
(`|A| = 0`) **and** Started-and-left (`|A| ≥ 1` ∧ ¬Continued). That is the whole change from the
superseded ALT, whose conjunct (b) was `|A| = 0` alone.

Implementation: conjunct (a) is `max_over_the_account(insertion instant) ≤ τ1`, the half-open
complement of "an instant strictly after `τ1`". Insertion instants come from the **stored** Step 5
play-`id` isotonic calibration (10,918 knots), applied verbatim as
`np.interp(rid, knot_rid, knot_time)`. **The curve was read and never refitted.**

**Populations, stated once and carried at every point of use (`0046` §0):**

| | Definition | `n` at `W = 108` |
| :--- | :--- | ---: |
| **DERIV** | Step 5 waterfall line 4, less D10. Requires S2 evidence. | **147,370** |
| **APPLY** | Step 5 waterfall line 1, less D10. What Step 8 filters at position 6. | **196,654** |

Both were re-derived from `processed/step5/pair_revision5.csv` in this run. The Step 5 waterfall
recomputed to **201,900 / 178,165 / 155,131 / 152,126 / 128,099**, matching line for line, and the
201,900 line-1 keys and the line-4 flag were compared element-wise against the reused inputs before
anything else ran.

---

## 2. Exclusion counts — the prior measurement is CONFIRMED

At `W = 108`:

| Population | `n` | **Excluded** | Never-started component | Started-and-left component | Accounts | Share of population |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **DERIV** | 147,370 | **99** | **0** | **99** | **73** | 0.0672% |
| **APPLY** | 196,654 | **703** | **604** | **99** | **216** | 0.3575% |

**Both prior figures confirmed exactly: 99 from 73 accounts on DERIV, 703 from 216 accounts on
APPLY, split 604 + 99.** No Continued pair is excluded on either population — that is forced by
conjunct (b) and is asserted in code, not assumed.

**How the rule selects, on APPLY at `W = 108`** — and note this decomposition has changed from the
one the task sheet still carries for ALT:

| | Pairs |
| :--- | ---: |
| APPLY | 196,654 |
| **Conjunct (b) alone** — NOT Continued | **52,514** |
| **Conjunct (a) alone** — no insertion after `τ1` | **1,355** |
| **Both** — excluded | **703** |

Conjunct (a) is still the binding one and is still why the count moves with `W`. On DERIV the same
two numbers are 25,988 and 751, intersecting at 99.

**Composition against S2 evidence, APPLY at `W = 108`:** all **604** never-started exclusions have
**no S2 record anywhere**; all **99** started-and-left exclusions **do** hold S2 records. The two
components are cleanly separated on that axis, which is a coincidence of this pull and not a
property of the rule.

**The DERIV never-started component is 0 at every arm** — 38 through 213. Under ALT that zero *was*
the DERIV exclusion set; under ALT-BROAD the entire DERIV set is started-and-left. **This is what
makes the dual control informative for the first time: the DERIV diff is 99 against 99, not
`0 = 0`.**

---

## 3. The three outcome shares, under the rule and against no filter

**APPLY, `n` = 196,654 before liveness, 195,951 after:**

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| No filter | 16.9704% | 73.2962% | 9.7333% |
| **Under the rule** | **16.7231%** | **73.5592%** | **9.7177%** |
| Movement | **−0.2474 pp** | **+0.2630 pp** | **−0.0156 pp** |

**DERIV, `n` = 147,370 before liveness, 147,271 after:**

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| No filter | 6.2055% | 82.3655% | 11.4291% |
| **Under the rule** | **6.2096%** | **82.4208%** | **11.3695%** |
| Movement | **+0.0042 pp** | **+0.0554 pp** | **−0.0595 pp** |

**The sign of the never-started movement is population-dependent — DOWN 0.2474 pp on APPLY, UP
0.0042 pp on DERIV** — exactly as `0048` §3(a) records, and it is not a divergence.

Account-clustered bootstrap of the live shares (2,000 replicates, clusters = accounts, the rule
re-applied inside each replicate so the exclusion count is itself random, seed 20260814):

| Population | NS 95% CI | Continued 95% CI | S&L 95% CI | Exclusion count 95% CI |
| :--- | :--- | :--- | :--- | :--- |
| APPLY (2,422 accounts) | [16.155, 17.284] | [72.837, 74.321] | [9.322, 10.114] | [577, 835] |
| DERIV (2,402 accounts) | [5.852, 6.594] | [81.804, 83.035] | [10.896, 11.870] | [75, 128] |

**Every bound in §4 is narrower than the sampling width it sits inside** — the never-started bound
is 27% of the APPLY sampling width, the started-and-left bound 6% of it. That does not make the
bounds unimportant, because they are a *systematic* range and the CI is a *sampling* range, but it
must be stated wherever both are printed.

---

## 4. The two bounds

**Standing rule applied (`0047` §3): each endpoint states the population it is computed on and the
estimand it bounds, and they are the same population.** Both bounds below are computed on the
position-5 population and bound a share defined on that same population. Neither mixes
denominators.

What is and is not observed for an excluded pair, which is what fixes the endpoints:

- The **604 never-started exclusions** rest on a null (`|A| = 0`). True state ∈ {NS, S&L, Continued}.
- The **99 started-and-left exclusions** have **`|A| ≥ 1` directly observed**. Only the *exit* is a
  null. True state ∈ {S&L, Continued} — **they can never be never-started.**

### 4.1 Never-started bound — UNCHANGED from ALT

**APPLY: [16.6633%, 16.9704%], width 0.3071 pp, BOTH ENDPOINTS ON 196,654.**

`32,769 / 196,654` to `33,373 / 196,654`, verified on the integers. **Identical to the ALT bound
republished at `0047` §3.** The 99 started-and-left exclusions enter neither endpoint because
`|A| ≥ 1` is observed for all of them, so the bound is **complete** — there is no case the filter
guards against that falls outside it.

**The ceiling equals the unfiltered never-started share as an identity** (16.9704%), because
returning all 604 as decliners reproduces the position-5 population exactly. Both endpoints are
attainable.

**DERIV: [6.2055%, 6.2055%], width 0.0000 pp** — degenerate, because the DERIV never-started
exclusion component is 0. **The never-started bound is the one place where the dual control is
still `x = x` on DERIV.** Say so where it is published.

### 4.2 Started-and-left bound — NEW, and it has a judgement call in it

**This is the bound `0048` §5 makes available and requires. There are two defensible ceilings and
the spec does not choose between them. I report both and do not adopt either.**

**APPLY, denominator 196,654 for every endpoint:**

| | Floor | Ceiling | Width | What the ceiling assumes |
| :--- | ---: | ---: | ---: | :--- |
| **(i) over the 99 S&L exclusions** *(as commissioned)* | **9.6830%** | **9.7333%** | **0.0503 pp** | the 99 really left; **and that none of the 604 is S&L** |
| **(ii) joint, over all 703 exclusions** | **9.6830%** | **10.0405%** | **0.3575 pp** | the 99 really left **and** every one of the 604 actually started and left |

`19,042 / 196,654` → `19,141 / 196,654` → `19,745 / 196,654`, on the integers.

**Reading (i) is what `0048` §5 and task-sheet Step 9 literally ask for, and its ceiling is an
identity with the unfiltered started-and-left share — the exact mirror of the never-started
ceiling. But it is NOT a ceiling on the estimand it names.** The 604 have `|A| = 0` as an untrusted
null; if their accounts were alive, some of them started, and a pair that started and did not meet
the Continued condition **is** started-and-left. Reading (i)'s ceiling therefore fails the test
`0047` §3 was written to impose: *does the endpoint cover the case the filter exists for?* On the
never-started side it does. On the started-and-left side, only reading (ii) does.

**Recommendation for the gate, not a decision:** publish **(ii) [9.6830%, 10.0405%] as the bound**
and **(i) as the sub-interval attributable to the 99**, labelled as conditional. Under (ii) the
never-started and started-and-left ceilings are **not simultaneously attainable** — both consume
the same 604 pairs — and the write-up must say so rather than printing two ceilings that add up to
more than the population.

**DERIV: [11.3619%, 11.4291%], width 0.0672 pp.** On DERIV the two readings **coincide**, because
the never-started exclusion component is 0. The DERIV started-and-left bound is unambiguous and
complete, and it is the only bound in this step that is both.

### 4.3 Continued, reported for completeness

Continued is the only state resting on positive evidence, so **its floor is an identity with the
unfiltered share** and all of the uncertainty is above it: **APPLY [73.2962%, 73.6537%], width
0.3575 pp**; **DERIV [82.3655%, 82.4327%], width 0.0672 pp**. Not requested; included because the
three bounds must be read together and (ii)'s ceiling is exactly this floor's mirror.

---

## 5. The filter waterfall

Positions 1–2 belong to Step 8 and are not rebuilt here. **No show in this frame has `L2 = 1`, so
position 2 removes nothing.**

| Position | Filter | APPLY rows out | DERIV rows out |
| ---: | :--- | ---: | ---: |
| 1–2 | Step 2 frame, `L2 = 1` exclusion | *(Step 8)* | *(Step 8)* |
| 3 | S1 completion rule | 220,107 | 220,107 |
| 4 | contamination exclusion (Step 5) | 201,900 | 152,126 |
| 5 | right-censoring D10, re-derived at `W = 108` | 196,654 | 147,370 |
| **6** | **liveness (ALT-BROAD)** | **195,951** *(−703: 604 NS + 99 S&L)* | **147,271** *(−99: 0 NS + 99 S&L)* |
| 7 | outcome assignment at `τ1` and `τ2` | 195,951 *(annotation, −0)* | 147,271 *(annotation, −0)* |

**Line 6 is OUTCOME-CONDITIONAL, and under ALT-BROAD it is conditional in a stronger sense than
under ALT.** Conjunct (b) is now "NOT Continued", and Continued is read at **`τ2`**, not `τ1`. So
position 6 depends on an annotation computed at **both** instants. This is still permitted on
`0046` §5's reasoning — both are row-local predicates on the position-5 output, they commute
exactly, and `0029`'s ordering rationale is about per-filter sample size, which cannot reach
position 7 because outcome assignment removes no rows.

**Monotone decrease at line 6:**

| Population | Rows removed | Decrease |
| :--- | ---: | :--- |
| **APPLY** | 703 | **STRICT** |
| **DERIV** | 99 | **STRICT** |

**Under ALT-BROAD the empty-exclusion-set case does not arise at any tested arm on either
population.** `>=` remains the safe coding for Step 8's invariant, but **the stated reason for it —
"the derivation population, where the liveness exclusion set is empty" — is now false.** See §8.

---

## 6. `W`-coupling per arm, with the started-and-left component separated

**D10 is RE-DERIVED at each arm** (`0047` §5). Right-censoring is
`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which contains `W`, so the censored population differs
per arm. **This table is on the re-derived reading. It is not comparable to any table built on a
D10 frozen at `W = 108`.** `H` is held constant at 91 across every arm.

**APPLY:**

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| population `n` | 197,007 | 197,007 | 197,007 | 197,007 | 196,674 | **196,654** | 195,689 | 193,270 |
| **excluded** | **537** | **550** | **633** | **664** | **701** | **703** | **789** | **864** |
| never-started component | 485 | 494 | 554 | 575 | 603 | **604** | 664 | 716 |
| **started-and-left component** | **52** | **56** | **79** | **89** | **98** | **99** | **125** | **148** |
| accounts | 177 | 182 | 197 | 207 | 215 | 216 | 243 | 253 |

**DERIV:**

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| population `n` | 147,685 | 147,685 | 147,685 | 147,685 | 147,384 | **147,370** | 146,602 | 144,852 |
| **excluded** | **52** | **56** | **79** | **89** | **98** | **99** | **125** | **147** |
| never-started component | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 |
| started-and-left component | 52 | 56 | 79 | 89 | 98 | **99** | 125 | **147** |
| accounts | 44 | 48 | 61 | 68 | 72 | 73 | 90 | 96 |

**Coupling factors, `W` = 38 → 213, on APPLY: total 1.61×, never-started component 1.48×,
started-and-left component 2.85×.** `0048` §5's "factor of 2.85 against ALT's own 1.5×" is
**confirmed**, on APPLY.

**Never-started bound per arm, APPLY** (both endpoints on that arm's own `n`):

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| floor % | 19.2983 | 18.7988 | 17.4755 | 17.0598 | 16.6890 | **16.6633** | 15.8885 | 15.0044 |
| ceiling % | 19.5445 | 19.0496 | 17.7567 | 17.3517 | 16.9956 | **16.9704** | 16.2278 | 15.3749 |

**Started-and-left bound per arm, APPLY, reading (i)** — over that arm's own S&L exclusions:

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| floor % | 9.8641 | 9.8702 | 9.8230 | 9.7631 | 9.6891 | **9.6830** | 9.5437 | 9.3413 |
| ceiling % | 9.8905 | 9.8986 | 9.8631 | 9.8083 | 9.7390 | **9.7333** | 9.6076 | 9.4179 |

---

## 7. The calibration residual, bounded — `0048` §9's un-actioned item

Conjunct (a) is an inequality between an **interpolated** instant and an exact `τ1`. The exclusion
set inherits the calibration's error. This section measures that error and asks whether the
exclusion set survives it. **Nothing was refitted.**

### 7.1 The residual has no single scale — it is bimodal

Measured on the fit family (checkin + scrobble, dated, `≤ τ_pull`; 4,367,583 records), whose
`watched_at` **is** their insert time by construction, as `|insert_time(rid) − watched_at|` in days.
This is an **in-sample** residual and therefore optimistic; it does not speak for `watch` rows,
which the curve was deliberately not fitted on and which are the majority of the store.

| | p50 | p75 | p90 | p95 | p97.5 | p99 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| `|residual|`, days | **0.0195** | 0.0422 | **0.107** | **124.6** | 287.5 | 472.9 |

**91.5% of fit records sit inside one day and 90% inside 2.6 hours; the top ~8% sit in the hundreds
of days.** The stored held-out validation — quoted from `calibration_meta.json`, **not** recomputed,
because recomputing it means refitting — gives median 0.0026 d and 90.6% inside 7 days, consistent
with this shape.

**`0048` §9's 22.68% is CONFIRMED exactly: 6,271,584 of 27,656,434 dated records claim a
`watched_at` later than their own calibrated insertion instant.** Their excess is also bimodal —
p50 **0.021 days** (30 minutes, i.e. ordinary scrobble-write latency and bin resolution), but p95
**77.5 days** and p99 **470.6 days**. The 22.68% headline conflates a benign majority with a small,
severe tail, and it should not be quoted as a single error scale in either direction.

### 7.2 Clamping — the concern is real in direction and NULL in effect here

**`0048` §9's 5,094 is CONFIRMED**: 5,094 records sit above the last knot and are pinned by
`np.interp` to `knot_time[-1]`, which pushes their instant **earlier** and therefore **toward false
exclusion**. 1,862 more sit below the first knot.

681 of 2,549 accounts have their **maximum** insertion instant set by a clamped record — and only
the maximum enters conjunct (a).

**But the clamp value is `2026-08-10T20:48:00Z`, which is later than `τ1` for every pair that
survives D10** — D10 requires `⟦T0⟧ + (max(W,91) + H) × 24h ≤ τ_pull`, so `τ1 ≤ τ_pull − 91 days`.
An account whose maximum is clamped is therefore **live for every pair it holds**.

> **Measured: 0 excluded pairs sit on a clamped-maximum account, on either population, at
> `W = 108`.** The 5,094 clamped records cannot produce a false exclusion at any tested arm.
> **`0048` §9's clamping item is discharged: correct in sign, zero in effect on this exclusion set.**

### 7.3 Margins — how close the decisions actually are

**Excluded pairs, `τ1 − max(instant)` in days, APPLY at `W = 108`** (how far below `τ1` the
account's last insertion sits — small means fragile):

| | p0 | p5 | p25 | p50 | p75 | p95 | p100 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all 703 | 0.014 | 15.8 | 74.8 | **170.9** | 350.3 | 676.4 | 1167.6 |
| the 604 NS | 0.014 | 17.7 | 87.2 | **202.5** | 385.0 | 711.4 | 1167.6 |
| the 99 S&L | 0.070 | 8.7 | 35.9 | **81.3** | 107.1 | 248.7 | 389.7 |

**The started-and-left component sits at roughly half the margin of the never-started component and
has a far shorter tail. The part of the rule `0048` adds is the less robust part**, and that is the
single most important finding in this section.

**Near-miss live pairs** — live *only* by conjunct (a), i.e. not Continued with an insertion after
`τ1` — `max(instant) − τ1` in days, APPLY: n = 51,811, minimum **0.75 days**, p50 1,861.9 days. Only
**2** sit within 1 day of flipping and **14** within 7 days. **The retention side is far from the
boundary.**

### 7.4 Is the exclusion set stable? Yes at the residual that covers 91% of records, no at the tail

Every account's maximum instant shifted by ±δ and the rule re-applied. **+δ = "the true insertion
was later than the curve says", which is the direction `step5_calibrate.py` states the curve errs
in ("the estimate is therefore mildly EARLY"), and it makes accounts more live.**

**APPLY at `W = 108`, base 703 = 604 NS + 99 S&L:**

| δ (days) | ±0.02 | ±0.107 | ±1 | ±7 | ±30 | ±124.6 | ±287.5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| later (fewer) | 702 | **701** | 701 | 686 | 635 | 414 | 218 |
| earlier (more) | 703 | **703** | 705 | 717 | 784 | 1,284 | 3,695 |
| S&L component, later→earlier | 99–99 | 98–99 | 98–99 | **94–104** | **80–125** | **15–285** | **4–1,100** |

**DERIV at `W = 108`, base 99:** ±0.107 d → [98, 99]; ±7 d → [94, 104]; ±30 d → [80, 126]; ±124.6 d
→ [15, 296]; ±287.5 d → [4, 1,233].

> **Verdict. The exclusion set is STABLE under the residual that applies to ~91% of records:**
> at ±0.107 days (p90 `|residual|`) it moves **703 → [701, 703]** on APPLY and **99 → [98, 99]** on
> DERIV. At ±1 day it is [701, 705] / [98, 99]. At ±7 days it is [686, 717] / [94, 104] — under 5%.
>
> **It is NOT stable under the heavy tail.** At ±124.6 days (p95 `|residual|`) APPLY runs
> [414, 1,284]. **And the started-and-left component degrades faster than the never-started
> component at every step**: at ±30 days the NS component moves ±9% while the S&L component moves
> −19%/+26%; at ±124.6 days NS spans 2.5× while S&L spans 19×.
>
> **A residual in the hundreds of days is not a calibration error in the ordinary sense** — it is
> the signature of contaminated records inside the fit family, which is a Step 5 property. But the
> rule cannot tell the two apart, so the honest statement is: **the exclusion set is robust to
> calibration noise and is not robust to calibration failure, and the second component of the rule
> is the exposed one.**

### 7.5 A calibration-independent cross-check

Do the excluded pairs' accounts hold **any** record whose *claimed* `watched_at` is after `τ1`? A
claim after `τ1` on an account with no insertion after `τ1` is either a backdated-forward claim —
which `0021` rules must be ignored — or calibration error. It cannot separate them, so it is an
**upper bound on the exclusions the residual could overturn, not an estimate**.

> **3 of 703 on APPLY (1 NS, 2 S&L); 2 of 99 on DERIV.** For 700 of 703 excluded pairs, the account
> is silent after `τ1` on *both* clocks. **This is a diagnostic and does not reintroduce a claimed-
> `watched_at` test into the rule.**

---

## 8. Defects found in the record — reported, not reconciled

The instruction is that `decisions/` is authoritative and any disagreement with `task-sheet.md` is a
defect to report. Five, and the first two would change an implementation.

1. **`task-sheet.md` Step 7: "`τ2` plays no part." FALSE under the adopted rule.** Conjunct (b) is
   "NOT Continued", and Continued is read at `τ2` (`0034`). `τ2` is now load-bearing in the rule
   itself. **My reading, applied here: `τ2` plays no part in the *silence test*, which stays
   anchored at `τ1`; it necessarily enters conjunct (b) through the Continued definition.** An
   instance that took the line literally would either read Continued at `τ1` — a different rule — or
   stop.
2. **`task-sheet.md` Step 7: "the monotone-decrease invariant holds only NON-STRICTLY where the
   exclusion set is empty, which it is on DERIV." FALSE under ALT-BROAD** — DERIV's exclusion set is
   99. **Step 8's corresponding bullet carries the same stale claim** ("only NON-STRICT on the
   derivation population, where the liveness exclusion set is empty"). `>=` is still the right
   coding; its stated justification no longer holds anywhere.
3. **`task-sheet.md` Step 7's "How the rule selects" paragraph is ALT's decomposition, not
   ALT-BROAD's** — it says conjunct 2 narrows 196,654 → 33,373 and conjunct 1 narrows 33,373 → 604.
   Under ALT-BROAD conjunct (b) narrows **196,654 → 52,514** and conjunct (a) narrows that to
   **703**. The adjacent bullet "**`|A| = 0` means Step 1 §7's Never-started condition**" is still
   true as a definition but is no longer a conjunct, and sitting where it does it reads as one.
4. **`0048` §5's started-and-left series "52 / 56 / 79 / 89 / 98 / 99 / 125 / 148" does not state its
   population** — the standing rule from `0046` §0 that the same entry invokes. **It is APPLY. On
   DERIV the series is identical except at the top arm: 147, not 148.** One pair at `W = 213` is
   excluded on APPLY and is not in line 4.
5. **`task-sheet.md` Step 9 asks for the second bound "over the 99" without saying whether the 604
   also feed its ceiling.** That is the unresolved judgement call in §4.2 and it changes the width
   by a factor of 7 (0.0503 pp vs 0.3575 pp).

---

## 9. Judgement calls the spec does not settle — every one, stated

1. **The started-and-left ceiling: over the 99, or over all 703.** §4.2. Both reported, neither
   adopted. This is the one that matters.
2. **"No insertion instant after `τ1`" implemented as `max(instant) ≤ τ1`** — "after" read as
   strictly greater, matching the half-open `watched_at < τ1` convention of Step 1 §2.4.
3. **`τ2` enters conjunct (b) but not conjunct (a).** Defect 1 above; this is the reading I applied.
4. **The residual ladder** — 0.02 / 0.107 / 1 / 7 / 30 / 124.6 / 287.5 days — is my choice, taken
   from the measured `|residual|` percentiles plus two round anchors. No ladder is specified.
5. **The residual is measured in-sample.** The held-out figure is **quoted** from
   `calibration_meta.json`, never recomputed, because recomputing it requires refitting, which is
   barred. The in-sample residual is optimistic and I have said so at the point of use.
6. **`D10` re-derived per arm**, per `0047` §5. The frozen-at-108 reading is a different experiment
   and is not reported here at all, to avoid a table that could be mistaken for it.
7. **The bootstrap clusters on accounts, not on shows or pairs**, because liveness evidence is
   account-wide; the rule is re-applied inside each replicate so the exclusion count is random.
   2,000 replicates, seed 20260814.
8. **The Continued bound is reported although not requested** (§4.3), because printing an NS ceiling
   and an S&L ceiling without it invites the reader to add two non-simultaneously-attainable numbers.
9. **Inputs reused, not recomputed.** Conjunct (a), D10 per arm and the per-arm outcome assignment
   come from this instance's own ALT rerun at `processed/step7/alt2_b/`. None of them is the rule;
   `0048` changed conjunct (b) only. Row identity and the line-4 flag were re-derived from
   `pair_revision5.csv` and compared element-wise before use.

---

## 10. What this gate still cannot establish

- **That the rule is right.** Its warrant is an argument — that Started-and-left is a null on exit —
  not a measurement. Nothing here tests it.
- **`0048` §9's narrowing stands.** `0021` licenses "insertion after `τ1` ⟹ live" as a **sufficient**
  condition; the rule is a **biconditional**. This step narrows where the converse is asserted; it
  does not justify it.
- **That Step 8's position-6 population is the one reconstructed here.** APPLY was built from the
  Step 5 pair table, not through Step 8's positions 1–5. **703 should be carried into the Step 8
  diff as an expected value, and a mismatch treated as a population defect before an implementation
  one** (`0047` §7).
- **That two implementations of the rule agree.** That is the Human Lead's diff, and on DERIV it is
  now a real test — 99 against 99 — for the first time in this chain. **Except on the never-started
  bound, where DERIV remains degenerate at [6.2055%, 6.2055%] and the comparison is still `x = x`.**
