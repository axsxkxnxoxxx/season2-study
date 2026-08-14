# Step 7 — Liveness rule, rerun on ALT-MATCHED (`decisions/0052`)

> **SUPERSEDED IN WHOLE — this deliverable measures the REVERTED rule.**
>
> **ALT-MATCHED was adopted at `decisions/0052` and REVERTED at `0054`.** The adopted rule is
> **ALT-BROAD**: not live iff no insertion after `τ1` **and** not Continued, silence anchored at `τ1`
> and only at `τ1`. **Nothing in this file is a current figure for the adopted rule.**
>
> **It is retained, not deleted, for two reasons.** It is the record of what the reverted rule
> produced — that is how `0054` established the two rules give **numerically identical** bounds on all
> three identified sets. And its DERIV figures (`[11.3015%, 11.4291%]`, `82.4930%`) were **computed
> here first** and were the ones `0055` carried across when `0054` widened APPLY alone.
>
> **Current deliverables: `step7-liveness-bb-{a,b}.{md,json}`**, which carry their own partial
> supersession stamp and a generated derived-figures block.



**Instance:** `data-scientist-b`, namespace `mm_b` · **Date:** 2026-08-13 · **API calls: 0**

> **THIS IS A GATE. NOTHING HERE IS ADOPTED.** The rule below is the one the Human Lead adopted at
> `decisions/0052`; every figure attached to it is a proposal for the Human Lead to approve and to
> diff against the other arm. This instance adopted nothing and did not read the other arm's work.

Machine-readable companion: `artifacts/step7-liveness-mm-b.json`.
Row-level intermediates: `processed/step7/mm_b/`.

---

## 1. The rule, as measured

> **A user-show pair is NOT LIVE if and only if EITHER:**
> - **`|A| = 0` AND the account shows no insertion instant after `τ1 = ⟦T0⟧ + W × 24h`; OR**
> - **`|A| ≥ 1` AND the pair is NOT Continued AND the account shows no insertion instant after
>   `τ2 = ⟦T0⟧ + (W + H) × 24h`.**
>
> Otherwise it is live. **Each null is tested at the instant its own outcome is read.**

**Continued** is Step 1 §7 as amended by `0034`: `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`,
read at `τ2` on `A_H`. The whole change from the superseded ALT-BROAD is the instant at which the
**started-and-left** null's silence is tested: `τ1` → `τ2`.

**`τ1 < τ2`, so "silent after `τ1`" implies "silent after `τ2`": the `τ2` test is the WEAKER one and
its set is a SUPERSET.** That is asserted in code at every arm, and it is why ALT-MATCHED's exclusion
set strictly contains ALT-BROAD's rather than trading pairs with it.

**Implementation.** "After `τ`" is read as strictly greater, matching the half-open `watched_at < τ`
convention of Step 1 §2.4, so silence is `max_over_the_account(insertion instant) ≤ τ`. Insertion
instants come from the **stored** Step 5 play-`id` isotonic calibration (10,918 knots), applied
verbatim as `np.interp(rid, knot_rid, knot_time)`. **The curve was read and never refitted.**

### Populations, stated once and carried at every point of use (`0046` §0)

| | Definition | `n` at `W = 108` |
| :--- | :--- | ---: |
| **DERIV** | Step 5 waterfall line 4, less D10. Requires S2 evidence. | **147,370** |
| **APPLY** | Step 5 waterfall line 1, less D10. What Step 8 filters at position 6. | **196,654** |

Both were re-derived from `processed/step5/pair_revision5.csv` in this run. The Step 5 waterfall
recomputed to **201,900 / 178,165 / 155,131 / 152,126 / 128,099**, matching line for line, and both
bases were asserted against it before anything else ran. Sweep: 27,656,813 records, 2,549 accounts,
2,481 of them present in line 1. No show in this frame has `L2 = 1`.

**Reuse, with the cross-check the brief requires.** The per-account maximum insertion instant, the
pair identity, `T0`, the line-4 flag, `k`, `F2`, `L2`, D10 per arm, silence-at-`τ1` per arm and the
outcome assignment per arm were all **recomputed from source in this run** and then compared
**element-wise** against this instance's own stored arrays (`processed/step7/bb_b/acct_instants.npz`,
`processed/step7/alt2_b/{pairs,outcomes}.npz`). **Every comparison is an exact match** — 2,549
accounts, 201,900 pairs, all 8 arms. Nothing was reused unverified.

---

## 2. Exclusion counts — `0052` §1's two expectations are CONFIRMED, and DERIV is measured

At `W = 108`, D10 re-derived at that arm:

| Population | `n` | **Excluded** | Never-started | Started-and-left | Accounts | Share of population |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **DERIV** | 147,370 | **188** | **0** | **188** | **126** | 0.1276% |
| **APPLY** | 196,654 | **793** | **604** | **189** | **256** | 0.4032% |

- **`0052` §1 expects APPLY 703 → 793. CONFIRMED, exactly.**
- **`0052` §1 expects the started-and-left component 99 → 189. CONFIRMED, exactly.**
- **`0052` §1 records DERIV as unmeasured. MEASURED HERE: 99 → 188, from 126 accounts, of which
  0 never-started and 188 started-and-left.** The DERIV delta is **+89**, not +90; one of the 90
  pairs ALT-MATCHED adds on APPLY is not in Step 5 line 4.
- **No Continued pair is excluded on either population.** Forced by the rule's own conjuncts, and
  asserted in code rather than assumed.
- The never-started component is **unchanged at every arm on both populations** — branch (i) is
  bit-for-bit the rule ALT-BROAD already applied to that null.

### How the rule selects — two branches, not a chain

ALT-BROAD's decomposition was a chain (`¬Continued` then silence). **ALT-MATCHED does not have one**,
because the two branches test different instants. Reporting it as a chain would misdescribe it.

| APPLY, `W = 108` | Pairs |
| :--- | ---: |
| Branch (i) pool — never-started (`|A| = 0`) | 33,373 |
| → after silence at `τ1` | **604** |
| Branch (ii) pool — started-and-left (`|A| ≥ 1` ∧ ¬Continued) | 19,141 |
| → after silence at `τ2` | **189** |
| *(reference)* silence at `τ1` alone | 1,355 |
| *(reference)* silence at `τ2` alone | 2,025 |
| *(reference)* `¬Continued` alone | 52,514 |

On DERIV the branch pools are 9,145 and 16,843; silence alone is 751 at `τ1` and 1,210 at `τ2`;
`¬Continued` alone is 25,988.

**Composition against S2 evidence, APPLY:** all **604** never-started exclusions have **no S2 record
anywhere**; all **189** started-and-left exclusions **do** hold S2 records. Clean separation on that
axis, a coincidence of this pull and not a property of the rule.

**The DERIV never-started component is 0 at every arm, 38 through 213** — as under ALT-BROAD. The
DERIV exclusion set is entirely started-and-left, so **the dual control on DERIV is 188 against 188,
not `0 = 0`.**

---

## 3. The three outcome shares, under the rule and against no filter

**APPLY, `n` = 196,654 before liveness, 195,861 after:**

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| No filter | 16.9704% (33,373) | 73.2962% (144,140) | 9.7333% (19,141) |
| **Under the rule** | **16.7307%** (32,769) | **73.5930%** (144,140) | **9.6762%** (18,952) |
| Movement | **−0.2397 pp** | **+0.2968 pp** | **−0.0571 pp** |

**DERIV, `n` = 147,370 before liveness, 147,182 after:**

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| No filter | 6.2055% (9,145) | 82.3655% (121,382) | 11.4291% (16,843) |
| **Under the rule** | **6.2134%** (9,145) | **82.4707%** (121,382) | **11.3159%** (16,655) |
| Movement | **+0.0079 pp** | **+0.1052 pp** | **−0.1131 pp** |

**The sign of the never-started movement is population-dependent — DOWN 0.2397 pp on APPLY, UP
0.0079 pp on DERIV.** On DERIV nothing is removed from the never-started numerator (the component is
0) while the denominator shrinks, so the share can only rise. **That is not a divergence between
arms; it is a property of the two populations and it must be stated wherever both are printed.**

**Account-clustered bootstrap** (design in §8; B = 4,000, seed 20260815, clusters = accounts, rule
re-applied inside each replicate):

| Population | NS 95% CI | Continued 95% CI | S&L 95% CI | Exclusion count 95% CI |
| :--- | :--- | :--- | :--- | :--- |
| APPLY (2,422 accounts) | [16.183, 17.302] | [72.877, 74.322] | [9.294, 10.060] | [660, 936] |
| DERIV (2,402 accounts) | [5.852, 6.631] | [81.848, 83.101] | [10.835, 11.821] | [150, 229] |

Movements, paired within replicate, **all three sign-stable across all 4,000 replicates on both
populations**: APPLY NS [−0.2914, −0.1920], C [+0.2456, +0.3518], S&L [−0.0746, −0.0408]; DERIV NS
[+0.0062, +0.0098], C [+0.0833, +0.1288], S&L [−0.1385, −0.0896].

---

## 4. The bounds — and which population each one bounds

**Standing rule applied (`0047` §3): each endpoint states the population it is computed on and the
estimand it bounds, and they are the same population.** All bounds below are computed on the
**position-5** population and bound a share defined on that same population. Neither mixes
denominators.

**But — and this is `0052` §7, restated here at the point of use, not buried — the BOUNDS ARE ON THE
POSITION-5 POPULATION AND THE PUBLISHED SHARES ARE POST-LIVENESS. They are different populations.**

| | Bounds are on | Published shares are on |
| :--- | ---: | ---: |
| APPLY | **196,654** | 195,861 |
| DERIV | **147,370** | 147,182 |

**Containment, measured:**

| | Point (post-liveness) | Its own bound (position-5) | Inside? |
| :--- | ---: | :--- | :---: |
| APPLY never-started | 16.7307% | [16.6633%, 16.9704%] | **yes** |
| APPLY started-and-left | 9.6762% | [9.6372%, 10.0405%] | **yes** |
| APPLY Continued | 73.5930% | [73.2962%, 73.6995%] | **yes** |
| **DERIV never-started** | **6.2134%** | **[6.2055%, 6.2055%]** | **NO** |
| DERIV started-and-left | 11.3159% | [11.3015%, 11.4291%] | yes |
| DERIV Continued | 82.4707% | [82.3655%, 82.4930%] | yes |

**On APPLY containment holds by arithmetic accident. On DERIV it fails outright**, and ALT-MATCHED
makes the miss slightly larger, not smaller: the point sits **0.0079 pp** above a degenerate bound,
against 0.0042 pp under ALT-BROAD. `0052` §7's number for this is 6.2096%, which is the ALT-BROAD
post-liveness share; **under the adopted rule it is 6.2134%.** Step 9 must name which population each
bound bounds.

What is and is not observed for an excluded pair, which is what fixes every endpoint:

- The **604 branch-(i)** exclusions rest on a null (`|A| = 0`). True state ∈ {NS, S&L, Continued}.
- The **189 branch-(ii)** exclusions have **`|A| ≥ 1` directly observed**. Only the *exit* is a null.
  True state ∈ {S&L, Continued} — **they can never be never-started.**

### 4.1 Never-started bound — `0052` §1's third expectation is CONFIRMED

**APPLY: [16.6633%, 16.9704%], width 0.3071 pp, BOTH ENDPOINTS ON 196,654.**

`32,769 / 196,654` to `33,373 / 196,654`, verified on the integers. **Unchanged from ALT-BROAD and
from ALT**, because the 90 pairs ALT-MATCHED adds are all started-and-left and enter neither
endpoint. The ceiling **equals the unfiltered never-started share as an identity**; both endpoints
are attainable; the bound is complete, since no branch-(ii) exclusion can be never-started.

**DERIV: [6.2055%, 6.2055%], width 0.0000 pp — degenerate**, because the DERIV never-started
exclusion component is 0. **The never-started bound is the one place where the dual control is still
`x = x` on DERIV.** Say so where it is published.

### 4.2 Started-and-left bound — over ALL exclusions, one denominator

**APPLY: [9.6372%, 10.0405%], width 0.4033 pp, BOTH ENDPOINTS ON 196,654.**

`18,952 / 196,654` to `19,745 / 196,654`, on the integers. The floor assumes every excluded pair in
truth continued; the ceiling assumes the 189 really left **and** every one of the 604 actually
started and left.

**Not over the 189 alone.** The 604 rest on an untrusted `|A| = 0` and some may in truth have left,
so a 189-only ceiling is not a ceiling on the unconditional estimand. **Labelled conditional
sub-interval, attributable to the branch-(ii) exclusions: [9.6372%, 9.7333%], width 0.0961 pp.** It
is not the bound and must not be published as one.

> **The floor is the number the rule change was for, and it moves.** ALT-BROAD published
> **9.6830%**. `0052` §4 recorded that if its 90 un-guarded channel pairs had in truth continued the
> floor would be 9.6373% — **which would have been the fifth consecutive bound with a non-covering
> endpoint.** Under ALT-MATCHED those 90 are excluded, so **the floor is that number by
> construction: 9.6372%** (exactly 9.637231%; `0052` §4's 9.6373% comes from subtracting two rounded
> figures and is 0.0001 pp high). **The endpoint now covers the case the filter exists for.**

**DERIV: [11.3015%, 11.4291%], width 0.1276 pp**, `16,655 / 147,370` to `16,843 / 147,370`. On DERIV
the two readings coincide, because the never-started exclusion component is 0.

### 4.3 Continued bound — it has a ceiling, and the ceiling has moved

**Continued is the only state resting on positive evidence, so its floor is an identity with the
unfiltered share and all of the uncertainty is above it.** `0052` §2 restores the point that **no
Continued pair is ever EXCLUDED, and that does not license printing Continued as a point: any
EXCLUDED pair may in truth be Continued.**

**APPLY: [73.2962%, 73.6995%], width 0.4033 pp**, `144,140 / 196,654` to `144,933 / 196,654`.
**DERIV: [82.3655%, 82.4930%], width 0.1276 pp.**

> **`73.6537%` — the figure `0052` §2 restores — is ALT-BROAD's Continued ceiling, `(144,140 + 703) /
> 196,654`. Under ALT-MATCHED it is `(144,140 + 793) / 196,654` = 73.6995%.** The restored figure is
> correct for the rule it was computed on and is **stale for the adopted one.** Whatever propagates
> this into Step 9 must carry 73.6995%, not 73.6537%.

### 4.4 ALL THREE CEILINGS, and their sum

**APPLY, `n` = 196,654:**

| Ceiling | Numerator | Share |
| :--- | ---: | ---: |
| Never-started | 33,373 | **16.9704%** |
| Started-and-left | 19,745 | **10.0405%** |
| **Continued** | 144,933 | **73.6995%** |
| **Sum** | | **100.7104%** |

**The excess is 0.7104 pp, and it is exactly 1,397 / 196,654, where 1,397 = 2 × 604 + 189.**

**The mechanism, which is what should be stated rather than the total.** Each excluded pair is
counted once in **every** ceiling its true state could belong to. A **branch-(i)** pair is compatible
with all three states, so each of the 604 appears in **all three** ceilings. A **branch-(ii)** pair
is compatible with started-and-left and Continued only, so each of the 189 appears in **two**.
Relative to the unfiltered partition, which sums to 100% exactly, the started-and-left ceiling adds
the 604 and the Continued ceiling adds the 604 and the 189 — hence 2 × 604 + 189. **The three are
ALTERNATIVE worst cases over ONE set, never simultaneous ones.** They cannot all hold and the
write-up must say so.

**DERIV, `n` = 147,370:** 6.2055% + 11.4291% + 82.4930% = **100.1276%**, excess 0.1276 pp = 188 /
147,370 = 2 × 0 + 188.

**Bound width against sampling width, on the ADOPTED bounds** (`0052` §6 records that this arm
previously published the ratio on the labelled conditional sub-interval, understating it 7.5×; the
ratio below is on the bound):

| APPLY | Bound width | Sampling width | Ratio |
| :--- | ---: | ---: | ---: |
| Never-started | 0.3071 pp | 1.1199 pp | **27.4%** |
| Started-and-left | 0.4033 pp | 0.7652 pp | **52.7%** |
| Continued | 0.4033 pp | 1.4447 pp | **27.9%** |

The bounds are a **systematic** range and the CIs a **sampling** range; they are not commensurable
and neither substitutes for the other. But the started-and-left bound is now **over half** the
sampling width, up from 45% under ALT-BROAD, and that is worth printing wherever both appear.

---

## 5. The filter waterfall

Positions 1–2 belong to Step 8 and are not rebuilt here. No show in this frame has `L2 = 1`.

| Position | Filter | APPLY rows out | DERIV rows out |
| ---: | :--- | ---: | ---: |
| 1–2 | Step 2 frame, `L2 = 1` exclusion | *(Step 8)* | *(Step 8)* |
| 3 | S1 completion rule | 220,107 | 220,107 |
| 4 | contamination exclusion (Step 5) | 201,900 | 152,126 |
| 5 | right-censoring D10, re-derived at `W = 108` | 196,654 | 147,370 |
| **6** | **liveness (ALT-MATCHED)** | **195,861** *(−793: 604 NS + 189 S&L)* | **147,182** *(−188: 0 NS + 188 S&L)* |
| 7 | outcome assignment at `τ1` and `τ2` | 195,861 *(annotation, −0)* | 147,182 *(annotation, −0)* |

**Line 6 is OUTCOME-CONDITIONAL, and under ALT-MATCHED it is conditional at BOTH instants.** Branch
(i) reads `|A| = 0` at `τ1`; branch (ii) reads `NOT Continued` at `τ2`. Both are evaluated before
liveness is applied. That is permitted on `0046` §5's reasoning — the outcome predicate and the
liveness predicate are **row-local on the position-5 output and commute exactly**, and `0029`'s
ordering rationale concerns **per-filter sample size**, which cannot reach position 7 because
**outcome assignment removes no rows**. Positions 1–6 are filters; position 7 is an annotation.
**The commutation is coded as an assertion, not assumed** — the surviving row set is computed both
ways at every arm on both populations and compared index-for-index.

**Monotone decrease at line 6:**

| Population | Rows removed at `W = 108` | Decrease | At every arm 38…213 |
| :--- | ---: | :--- | :--- |
| **APPLY** | 793 | **STRICT** | STRICT — 604 / 621 / 713 / 754 / 793 / 793 / 878 / 952 |
| **DERIV** | 188 | **STRICT** | STRICT — 119 / 127 / 159 / 179 / 188 / 188 / 213 / 235 |

**The empty-exclusion-set case does not arise at any tested arm on either population.** `>=` remains
the right coding for Step 8's invariant, but **not because this rule ever needs it** — it is kept so
the invariant does not encode a property of one rule, since another filter position may legitimately
remove nothing.

---

## 6. `W`-coupling per arm, with the started-and-left component separated

**D10 is RE-DERIVED at each arm** (`0047` §5). Right-censoring is
`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which contains `W`, so the censored population differs per
arm. **These tables are on the re-derived reading and are not comparable to any table built on a D10
frozen at `W = 108`.** `H` is held constant at 91 across every arm.

**APPLY:**

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| population `n` | 197,007 | 197,007 | 197,007 | 197,007 | 196,674 | **196,654** | 195,689 | 193,270 |
| **excluded** | **604** | **621** | **713** | **754** | **793** | **793** | **878** | **952** |
| never-started component | 485 | 494 | 554 | 575 | 603 | **604** | 664 | 716 |
| **started-and-left component** | **119** | **127** | **159** | **179** | **190** | **189** | **214** | **236** |
| accounts | 204 | 211 | 227 | 245 | 257 | 256 | 276 | 296 |
| *(superseded ALT-BROAD total)* | *537* | *550* | *633* | *664* | *701* | *703* | *789* | *864* |

**DERIV:**

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| population `n` | 147,685 | 147,685 | 147,685 | 147,685 | 147,384 | **147,370** | 146,602 | 144,852 |
| **excluded** | **119** | **127** | **159** | **179** | **188** | **188** | **213** | **235** |
| never-started component | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 |
| started-and-left component | 119 | 127 | 159 | 179 | 188 | **188** | 213 | 235 |
| accounts | 88 | 93 | 108 | 120 | 127 | 126 | 136 | 153 |
| *(superseded ALT-BROAD total)* | *52* | *56* | *79* | *89* | *98* | *99* | *125* | *147* |

**Not monotone in `W`.** At `W` = 107 → 108 the APPLY started-and-left component falls 190 → 189 and
the DERIV one is flat at 188, because D10 is re-derived and the population shrinks 196,674 → 196,654.
**The series is a function of two things that both move with `W`**, and reporting it as a clean
coupling would be wrong.

**Coupling factors, `W` = 38 → 213, on APPLY: total 1.58×, never-started component 1.48×,
started-and-left component 1.98×.** On DERIV the total coupling is 1.97×.

> **`0052` §8 and task-sheet Step 13 carry ALT-BROAD's coupling — total 1.61×, started-and-left
> 2.85×. Both go stale under the adopted rule.** The started-and-left coupling **falls** from 2.85×
> to 1.98×, because ALT-MATCHED more than doubles the base at `W = 38` (52 → 119) while adding
> proportionally less at the top (148 → 236). The rule is **less** `W`-coupled in its own second
> component than the rule it replaces, not more.

**Never-started bound per arm, APPLY** (both endpoints on that arm's own `n`; unchanged from
ALT-BROAD at every arm):

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| floor % | 19.2983 | 18.7988 | 17.4755 | 17.0598 | 16.6890 | **16.6633** | 15.8885 | 15.0044 |
| ceiling % | 19.5445 | 19.0496 | 17.7567 | 17.3517 | 16.9956 | **16.9704** | 16.2278 | 15.3749 |

**Started-and-left bound per arm, APPLY, over ALL that arm's exclusions:**

| `W` | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| floor % | 9.8301 | 9.8342 | 9.7824 | 9.7174 | 9.6424 | **9.6372** | 9.4982 | 9.2958 |
| ceiling % | 10.1367 | 10.1494 | 10.1443 | 10.1001 | 10.0456 | **10.0405** | 9.9469 | 9.7884 |

**Continued ceiling per arm, APPLY:** 70.8716 / 71.3670 / 72.7421 / 73.2228 / 73.6686 / **73.6995** /
74.6133 / 75.6998.

### The frozen-D10 reading, because the record carries it

`task-sheet.md` Step 7 and `0050` state that freezing D10 at `W = 108` gives APPLY totals **746 / 823
/ 918 / 1,117** at `W` = 125 / 150 / 180 / 213, of which the never-started **component** is 632 / 684
/ 753 / 881. **Those totals are ALT-BROAD's and are now stale.** Under ALT-MATCHED, frozen D10, on
APPLY:

| `W` | 125 | 150 | 180 | 213 |
| :--- | ---: | ---: | ---: | ---: |
| **total** | **874** | **990** | **1,192** | **1,466** |
| never-started component | 632 | 684 | 753 | 881 |
| started-and-left component | 242 | 306 | 439 | 585 |

**The never-started component 632 / 684 / 753 / 881 is unchanged and is still a component, not a
total.** The re-derived reading at the same arms is 835 / 878 / 917 / 952 — and 878 and 952 reproduce
the `W` = 150 and 213 entries of the main table exactly, which is the cross-check that the two
readings were built the same way. **125 and 180 are not in the mandated grid.** An arm table that
does not name the reading is not reproducible.

---

## 7. The channel: `0052` §3's 90 are closed, and no analogous channel remains

**Basis check first.** `0050` §4's channel measurement is reproduced **exactly** on APPLY at
`W = 108`, from an independently rebuilt population:

| APPLY | `0050` | measured here |
| :--- | ---: | ---: |
| Not-Continued | 52,514 | **52,514** |
| Live only by the silence conjunct | 51,811 | **51,811** |
| **Channel — last insertion inside `(τ1, τ2)`** | **297** | **297** |
| — never-started | 207 | **207** |
| — **started-and-left** | **90** | **90** |
| ALT-BROAD exclusions | 703 | **703** |

Channel last-insertion sits at a median of **51.4 days** past `τ1`, p90 **85.1**, max **90.9** —
filling the window, as `0050` reported.

### Does ALT-MATCHED close the 90?

> **Yes: 90 of 90, 100%.** And the 90 started-and-left pairs ALT-MATCHED newly excludes are
> **exactly** the channel's started-and-left set — verified by index equality, not by count equality.
> On DERIV the analogous set is **89 of 89, 100%**.

**The 207 never-started pairs in ALT-BROAD's channel are not closed, and are not supposed to be.**
`0052` §3's correction is confirmed on the data: never-started is the null `|A| = 0` **read at `τ1`**,
and every one of the 207 has an insertion after `τ1` — exactly the evidence `0021` licenses. They are
not in the gap, which is why the closure denominator is the started-and-left set alone and why the
rate is **100%** rather than `0050`'s 70.3% over the pooled 297. (On DERIV the never-started half of
ALT-BROAD's channel is 3 pairs; they also stay live.)

### Does any analogous channel remain?

> **No. Zero on both branches, on both populations.**

| APPLY, `W = 108` | Live only by silence | Residual channel |
| :--- | ---: | ---: |
| Branch (i), never-started | 32,769 | **0** |
| Branch (ii), started-and-left | 18,952 | **0** |

**And it is zero by construction, which is the point of the rule change.** The channel is the
interval between the **silence instant** and the **read instant**. ALT-BROAD's was 91 days wide for
the started-and-left null. ALT-MATCHED makes the two instants the same for each null, so the interval
is empty — **there is no ε left to slide along.** `0052` §1's diagnosis, that ALT-BROAD's failure
mode was continuous in the silence instant and cut at one end, is confirmed, and the cut is now at
the only instant that closes it.

**Zero residual is not the same as "no pair is near the boundary", and the two must not be
conflated.** Live pairs, distance of last insertion past their own instant:

| APPLY | within 1 day | within 7 days | within 30 days | median |
| :--- | ---: | ---: | ---: | ---: |
| Branch (i), past `τ1` (n = 32,769) | 2 | 9 | 55 | 1,795.9 d |
| Branch (ii), past `τ2` (n = 18,952) | 2 | 28 | 90 | 1,930.3 d |

*(The 90 in the last row is a numeric coincidence with the 90 closed pairs — a different set. Do not
read them as the same 90.)* **The retention side is far from the boundary**: fewer than 0.5% of live
pairs on either branch sit within 30 days of flipping.

**What this does NOT close: the biconditional gap.** `0021` licenses *insertion after the instant ⟹
live* as a **sufficient** condition; the rule also asserts the converse. **ALT-MATCHED narrows
nothing about that** and it stays a Step 14 limitation.

---

## 8. Bootstrap design, stated in full

`0052` §6 records that the two arms' bootstraps were not diffable last time — A used B = 4,000, seed
20260813, on the **movements**; B used 2,000, seed 20260814, on the **levels** — and that the spec
fixes neither. **This arm therefore states its design and reports BOTH, so it is diffable against
either design the other arm may have chosen.**

| | |
| :--- | :--- |
| Cluster unit | **account (user)** — liveness evidence is account-wide, so a pair is not an independent unit |
| Resampling | `n_accounts` drawn **with replacement**, multinomial over the account index; all of an account's pairs travel together |
| Replicates `B` | **4,000** |
| Seed | **20260815**, `numpy.random.default_rng` |
| Interval | percentile, 2.5 / 97.5 |
| Rule | **re-applied inside every replicate**, so the exclusion count is itself random |
| Reported | **both LEVELS and MOVEMENTS**; movements paired within replicate |

Implementation note, because it affects nothing but should be visible: every reported quantity is a
count of rows in a category and the rule is row-local, so a replicate is **exactly** a weighted sum
of per-account category counts. No row-level resampling is approximated.

---

## 9. Residual sensitivity — the rule change makes the exclusion set MORE fragile

The calibration is **read, never refitted**; the ladder below is a sensitivity **shift** applied to
each account's maximum instant, not a refit. `+δ` means the true insertion was later than the curve
says — the direction `src/step5_calibrate.py` states the curve errs in — which makes accounts more
live.

**Margins, APPLY at `W = 108`**, measured against **each pair's own silence instant** (`τ1` for
branch (i), `τ2` for branch (ii)) — small means fragile:

| | p0 | p5 | p25 | p50 | p75 | p95 | p100 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all 793 | 0.01 | 11.9 | 72.2 | **168.1** | 320.5 | 656.4 | 1167.6 |
| the 604 never-started | 0.01 | 17.7 | 87.2 | **202.5** | 385.0 | 711.4 | 1167.6 |
| the 189 started-and-left | 0.13 | 5.1 | 45.9 | **97.6** | 174.7 | 257.9 | 480.7 |
| — the 99 ALT-BROAD already had | 91.07 | 99.7 | 126.9 | **172.3** | 198.1 | 339.7 | 480.7 |
| — **the 90 ALT-MATCHED adds** | **0.13** | **1.7** | **18.4** | **44.5** | **62.1** | **85.3** | **89.9** |

> **The 90 pairs ALT-MATCHED adds are, by construction, the ones sitting closest to their own
> boundary.** Their margin is bounded above by `H = 91` days — asserted in code, max measured 89.9 —
> because a pair enters the added set only if its last insertion fell inside `(τ1, τ2)`. **Median
> 44.5 days against the 604's 202.5.** ALT-MATCHED closes the construction channel and pays for it by
> taking in exactly the pairs whose exclusion the calibration residual could most easily overturn.
> **That is the honest cost of the rule change and it belongs in Step 14.**

*(The 99's margin here, median 172.3 days, is **not comparable** to the 81.3 days `0050` §2 routed
into Step 14: that was measured against `τ1` and this is measured against `τ2`, and 81.3 + 91 =
172.3. The reference instant changed with the rule. A side-by-side would be a false movement.)*

**Stability ladder, APPLY at `W = 108`, base 793 = 604 + 189:**

| δ (days) | ±0.107 | ±1 | ±7 | ±30 | ±124.6 | ±287.5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| total, later → earlier | 792 → 793 | 790 → 797 | **769 → 830** | **708 → 938** | **477 → 1,669** | 223 → 4,248 |
| S&L component | 189 → 189 | 187 → 191 | **177 → 217** | **153 → 279** | **78 → 670** | 9 → 1,653 |

**Verdict, unchanged in shape from the ALT-BROAD run and worse in degree.** The exclusion set is
**stable under the residual that applies to ~91% of records** — at ±0.107 days (the fit family's p90
`|residual|`) it moves 793 → [792, 793]; at ±1 day [790, 797]. **It is not stable under the heavy
tail**: at ±124.6 days it runs [477, 1,669]. **And the started-and-left component degrades faster
than the never-started component at every step** — at ±7 days it moves −6.3%/+14.8% against the
never-started component's −2.0%/+1.5%. Under ALT-BROAD the same ±7 comparison was −5.1%/+5.1% on the
S&L component. **The added 90 are the reason.**

**A calibration-independent cross-check.** Do the excluded pairs' accounts hold **any** record whose
*claimed* `watched_at` is after that pair's own silence instant? A claim after the instant is either
a backdated-forward claim, which `0021` requires be ignored, or calibration error; this cannot
separate them, so it is an **upper bound on the exclusions the residual could overturn, not an
estimate**, and it does **not** reintroduce a claimed-`watched_at` test into the rule.

> **2 of 793 on APPLY (1 branch-(i), 1 branch-(ii)); 1 of 188 on DERIV.** For 791 of 793 excluded
> pairs the account is silent after its own instant on *both* clocks.

---

## 10. Defects found in the record — reported, not reconciled

`decisions/` is authoritative and any disagreement with `task-sheet.md` or with my definition file is
a defect to report. **Nine. The first two would make an instance implement the superseded rule, and
the third would make Step 8 file a false divergence.**

1. **`task-sheet.md` Step 7, bullet at line 263: "the SILENCE test is anchored at `τ1` and only at
   `τ1`" and "The rule reads two instants: silence at `τ1`, Continued at `τ2`." BOTH FALSE under
   ALT-MATCHED**, and both sit ~27 lines below the correct ALT-MATCHED rule statement in the same
   file. **The adopted rule reads silence at `τ1` for one null and at `τ2` for the other.** An
   instance that took this bullet literally implements ALT-BROAD and reproduces 703. This is the
   single most dangerous line in the file.
2. **`.claude/agents/data-scientist-b.md` line 42 still heads Step 7 "RULE CHANGED 2026-08-13
   (`decisions/0046`)"**, twelve characters above a correctly propagated `0052` rule statement.
   `0052` §8 records that exactly this mode-line defect was corrected in `task-sheet.md`; **it was
   not corrected in the agent definition.** The same file's line 66 also still says liveness is
   "**anchored at `τ1`**" without qualification.
3. **`task-sheet.md` Step 8, "Expect 703 liveness exclusions at position 6, `W = 108` — 604
   never-started plus 99 started-and-left."** Under the adopted rule it is **793 = 604 + 189**. **This
   is the file Step 8's two isolated instances read**, and the bullet instructs them to treat a
   mismatch as a *population* defect before an implementation one — so a correct Step 8 would be sent
   hunting a non-existent frame-join bug.
4. **Stale ALT-BROAD figures presented as current in both `task-sheet.md` Step 7 and
   `data-scientist-b.md`:** "99 on DERIV (73 accounts), 703 on APPLY (216 accounts)" → measured **188
   (126 accounts) and 793 (256 accounts)**; the chain decomposition "196,654 → 52,514 → 703" → the
   adopted rule **has no chain**, it has two branches; "Monotone decrease is STRICT … 703 and 99" →
   still strict, wrong counts.
5. **The per-arm series `537 / 550 / 633 / 664 / 701 / 703 / 789 / 864` and the started-and-left
   series `52 / 56 / 79 / 89 / 98 / 99 / 125 / 148` are ALT-BROAD's**, and appear in `task-sheet.md`
   Steps 7 and 13 and in `data-scientist-b.md` twice. Under ALT-MATCHED they are **604 / 621 / 713 /
   754 / 793 / 793 / 878 / 952** and **119 / 127 / 159 / 179 / 190 / 189 / 214 / 236**.
6. **The "factor of 2.85" and the "1.61× coupling" both go stale**, and they move in *opposite*
   directions from what the record implies: total coupling falls 1.61× → 1.58×, and the
   started-and-left coupling falls **2.85× → 1.98×**. `0052` §8 corrected 1.5× to 1.61× **in the
   same entry that changed the rule and invalidated 1.61×.**
7. **The frozen-D10 totals `746 / 823 / 918 / 1,117` go stale** → **874 / 990 / 1,192 / 1,466**. The
   never-started component 632 / 684 / 753 / 881 is unchanged and is still a component.
8. **`73.6537%` is stale.** `0052` §2 correctly restores it as the Continued ceiling and correctly
   insists Continued is not a point — but it is **ALT-BROAD's** ceiling. Under the adopted rule it is
   **73.6995%**, and the three-ceiling sum is **100.7104%**, not 100.6646%. `data-scientist-b.md`
   line 99 carries 73.6537% inside the Step 9 obligation `0052` §5 was written to propagate — **the
   propagation landed and the number inside it did not survive the rule change.**
9. **`data-scientist-b.md` Step 9 still specifies the started-and-left bound as "[9.6830%, 10.0405%],
   width 0.3575 pp" over "ALL 703 exclusions", and the sub-interval as "[9.6830%, 9.7333%]".** Under
   ALT-MATCHED: **[9.6372%, 10.0405%], width 0.4033 pp**, over all **793**; sub-interval **[9.6372%,
   9.7333%]**. The same file's `0052` §7 bullet quotes the DERIV point estimate as **6.2096%**, which
   is ALT-BROAD's; it is **6.2134%**.

**One further record note, minor:** `0052` §4 gives the prospective floor as 9.6373%. The exact value
is **9.637231%**, i.e. **9.6372%** at four decimals; §4's figure was obtained by subtracting two
already-rounded numbers. The substantive claim — that the floor moves 0.0458 pp down and that this is
the endpoint the rule change repairs — is confirmed.

---

## 11. Judgement calls the spec does not settle — every one, stated

1. **"No insertion instant after `τ`" is implemented as `max(instant) ≤ τ`** — "after" read as
   strictly greater, matching the half-open `watched_at < τ` convention of Step 1 §2.4. Applied
   identically at both instants.
2. **The started-and-left bound is reported over ALL 793 exclusions on one denominator**, with the
   branch-(ii)-only interval **labelled conditional**. The brief settles this; recorded because it is
   the choice that most changes the width.
3. **Margins are measured against each pair's own silence instant**, not against a single instant.
   Mixing them would misdescribe both components and would manufacture an apparent movement in the
   99's margin that is purely a change of reference point. Stated at the point of use.
4. **The residual ladder** — 0.02 / 0.107 / 1 / 7 / 30 / 124.6 / 287.5 days — is my choice, carried
   over from this instance's ALT-BROAD run, taken from the measured fit-family `|residual|`
   percentiles plus three round anchors. No ladder is specified.
5. **The residual percentiles quoted in §9's provenance are in-sample** and therefore optimistic; the
   held-out figure is **quoted** from `calibration_meta.json`, never recomputed, because recomputing
   it means refitting, which is barred.
6. **D10 is re-derived per arm as the operative reading**; the frozen reading is reported **only**
   because `task-sheet.md` carries stale frozen figures that would otherwise produce a false Step 13
   divergence. Both are labelled at the point of use.
7. **The bootstrap clusters on accounts and reports both levels and movements** — §8.
8. **The Continued bound is reported in full**, not because it was requested as a bound but because
   the brief requires all three ceilings and because printing two ceilings without the third invites
   the reader to add numbers that cannot simultaneously hold.
9. **The channel is generalised** from `0050` §4's ALT-BROAD-specific form to "live only by the
   silence conjunct, with last insertion before the instant at which that pair's own outcome is
   read." That generalisation is what makes the question "does an analogous channel remain?"
   answerable at all; a narrower reading would trivially return zero without measuring anything.
10. **Everything was recomputed from source and then compared element-wise to stored arrays**, rather
    than reused with a spot check. The brief asks for reuse with a cross-check; I took the stronger
    form because it costs seconds.

---

## 12. What this gate still cannot establish

- **That the rule is right.** Its warrant is an argument — that started-and-left is a null on exit,
  and that a null must be tested at the instant it is read — not a measurement. Nothing here tests
  it. What is measured is that the argument's own failure mode, the channel, is now empty.
- **The biconditional gap stands** (§7). `0021` licenses a sufficient condition; the rule asserts the
  converse. ALT-MATCHED does not narrow this and does not justify it.
- **That the exclusion set survives calibration failure.** It survives calibration *noise*; §9 shows
  the component the rule change adds is the exposed one, and it is more exposed than ALT-BROAD's.
- **That Step 8's position-6 population is the one reconstructed here.** APPLY was built from the
  Step 5 pair table, not through Step 8's positions 1–5. **793 should be carried into the Step 8 diff
  as the expected value — not 703 — and a mismatch treated as a population defect before an
  implementation one** (`0047` §7).
- **That two implementations of the rule agree.** That is the Human Lead's diff. On DERIV it is a
  real test — 188 against 188 — everywhere except the never-started bound, where DERIV remains
  degenerate at [6.2055%, 6.2055%] and the comparison is still `x = x`.
