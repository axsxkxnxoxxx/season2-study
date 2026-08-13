# Step 7 — liveness rule, rerun on the adopted rule (instance **b**)

**GATE. Measured, not adopted.** This instance produces the artifact and stops. The Human Lead approves and diffs the two arms. Zero API calls.

**Every figure below names the population that produced it** (`decisions/0046` §0). The two populations are not interchangeable and differ by construction:

| Population | Definition | `n` at `W = 108` | S2 evidence required |
| :--- | :--- | ---: | :--- |
| **DERIV** | Step 5 line 4 (152,126) less D10 | **147,370** | yes, by construction |
| **APPLY** | Step 5 line 1 (201,900) less D10 | **196,654** | no — admits pairs with no S2 record |

The Step 5 waterfall was re-measured from `pair_revision5.csv` and asserted before use: [201900, 178165, 155131, 152126, 128099] for lines 1–5.

## 1. The rule statement

> A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant strictly after that pair's tau1 = [T0] + W x 24h, AND |A| = 0, where |A| = 0 is Step 1 Sec 7's Never-started condition read at tau1. Otherwise the pair is live.

`|A|` is Step 1 §7's set — distinct S2 episodes whose number is a member of `E2`, canonical timestamp (§2.2, the minimum `watched_at` across that episode's records) tested in the half-open instant form `watched_at < τ1`. `date(watched_at) <= T1` appears nowhere. `τ2` plays no part in the rule; it is used only to assign Continued.

- **Insertion time, not claimed `watched_at`** (`0021`). The insertion instant is the stored Step 5 isotonic play-`id` calibration at `processed/step5/calibration.npz`, **read and not refitted** — 10,918 knots, applied verbatim as `np.interp(rid, knot_rid, knot_time)`.
- **Pair-level, anchored at `τ1`.** Evidence is account-wide, the test is clock-start-relative, and the clock start is pair-specific. No account is dropped wholesale.
- **No pre-`τ1` requirement of any kind.** Withdrawn twice (`0040` §1, `0042` §3); not reinstated.
- **No parameter of its own.** The rule is fully determined by `W`; its exclusion set moves with `W`, and the per-arm counts are in §2.

## 2. Exclusion counts — both populations

**At `W = 108`: 0 pairs on DERIV, 604 pairs from 191 accounts on APPLY (0.3071% of APPLY).** `0046`'s expected 0 and ~604 are **confirmed**, and were measured rather than assumed.

| `W` | DERIV `n` | DERIV excluded | APPLY `n` | APPLY excluded | APPLY accounts | conjunct (a) alone, DERIV | conjunct (a) alone, APPLY |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 38 | 147,685 | 0 | 197,007 | 485 | 162 | 348 | 833 |
| 46 | 147,685 | 0 | 197,007 | 494 | 166 | 367 | 861 |
| 77 | 147,685 | 0 | 197,007 | 554 | 177 | 519 | 1073 |
| 91 | 147,685 | 0 | 197,007 | 575 | 183 | 706 | 1281 |
| 107 | 147,384 | 0 | 196,674 | 603 | 190 | 745 | 1348 |
| **108** | 147,370 | 0 | 196,654 | 604 | 191 | 751 | 1355 |
| 150 | 146,602 | 0 | 195,689 | 664 | 213 | 779 | 1443 |
| 213 | 144,852 | 0 | 193,270 | 716 | 218 | 949 | 1670 |

**Composition of the exclusions, at every arm and on both populations: 100% Never started, 0 Continued, 0 Started-and-left.** That is forced by the second conjunct and is stated here because the Step 9 bound depends on it.

**On APPLY at `W = 108`, all 604 excluded pairs hold no S2 record anywhere in the sweep** — `0046` §1's characterisation, tested and confirmed in the subset reading, at every arm. **In the set-equality reading it is false**: APPLY holds 23,260 pairs with no S2 record anywhere, of which 22,656 have an insertion instant after `τ1` and are therefore **live**. The exclusion set is a strict subset of that set, and conjunct (a) is what selects within it.

**The rule against the superseded PF-LIMIT, on APPLY at `W = 108`** — reported because the difference is the substance of `0046` §2. PF-LIMIT deletes 1,355 pairs; the adopted rule deletes 604; the difference is 751 pairs, of which **652 continued and 99 started and left** — none never-started. Those are exactly the DERIV 751.

## 3. The three outcome shares, under the rule and against no filter

**At `W = 108`.**

| Population | Filter | `n` | Never started | Continued | Started and left |
| :--- | :--- | ---: | ---: | ---: | ---: |
| DERIV | no filter | 147,370 | 6.2055% (9,145) | 82.3655% (121,382) | 11.4291% (16,843) |
| DERIV | **adopted rule** | 147,370 | 6.2055% (9,145) | 82.3655% (121,382) | 11.4291% (16,843) |
| APPLY | no filter | 196,654 | 16.9704% (33,373) | 73.2962% (144,140) | 9.7333% (19,141) |
| APPLY | **adopted rule** | 196,050 | 16.7146% (32,769) | 73.5221% (144,140) | 9.7633% (19,141) |

**Movement against no filter — DERIV: 0.0000 pp on all three shares, because the exclusion set is empty. APPLY: never-started -0.2558 pp, continued +0.2258 pp, started-and-left +0.0300 pp.**

**Account-clustered bootstrap, `B` = 2,000, accounts resampled with replacement, percentile 2.5/97.5, one resample per replicate shared by both rules so the delta is paired.**

| Population | Filter | Never started 95% CI | width |
| :--- | :--- | :--- | ---: |
| DERIV | NO_FILTER | [5.8379%, 6.6020%] | 0.7641 pp |
| DERIV | ADOPTED | [5.8379%, 6.6020%] | 0.7641 pp |
| APPLY | NO_FILTER | [16.4440%, 17.5140%] | 1.0700 pp |
| APPLY | ADOPTED | [16.1939%, 17.2560%] | 1.0621 pp |

On **APPLY** the paired delta on never-started is **-0.2559 pp, 95% CI [-0.3074, -0.2077], excluding zero** — the rule's effect is small but not noise. On **DERIV** the delta is exactly zero in every replicate, because the same empty set is removed in each.

## 4. The Step 9 liveness bound

**On APPLY at `W = 108`: [16.7146%, 16.9704%], width 0.2558 pp, both endpoints on the single denominator 196,654.** This reproduces `0046` §4.

**The ceiling equals the unfiltered never-started share as an identity — confirmed, and confirmed on the integers rather than on the rounded percentages.** Every excluded pair is never-started, so returning all of them to the denominator as decliners restores the unfiltered population exactly: 32,769 + 604 = 33,373 over 196,050 + 604 = 196,654. The ceiling is therefore not an assumption about the excluded pairs so much as a restatement of the population before the filter ran. **Read §4.1 before quoting the floor**: the two endpoints do not sit on the same denominator, and which estimand is being bounded decides whether the floor is a floor.

**On DERIV the bound is degenerate: [6.2055%, 6.2055%], width 0.0000 pp**, because nothing is excluded. A bound of zero width is not a strong result; it is the absence of an exclusion set.

**Set the width against the sampling width.** On APPLY the bound is 0.2558 pp wide against an account-clustered 95% interval of 1.0700 pp on the same share — about 24% of it. The liveness uncertainty is real but is not what dominates the headline's precision.

| `W` | APPLY floor | APPLY ceiling | width pp |
| ---: | ---: | ---: | ---: |
| 38 | 19.3459% | 19.5445% | 0.1986 |
| 46 | 18.8461% | 19.0496% | 0.2035 |
| 77 | 17.5248% | 17.7567% | 0.2319 |
| 91 | 17.1097% | 17.3517% | 0.2419 |
| 107 | 16.7404% | 16.9956% | 0.2553 |
| 108 | 16.7146% | 16.9704% | 0.2558 |
| 150 | 15.9426% | 16.2278% | 0.2852 |
| 213 | 15.0602% | 15.3749% | 0.3147 |

### 4.1 What the floor is a floor of — a finding, flagged for the Human Lead

**The two endpoints sit on two denominators: the floor on 196,050 live pairs, the ceiling on the full 196,654.** That is the same shape `0046` §4 rejected in PF-LIMIT's published interval, and the substantive half of that objection carries over.

If the estimand is **the never-started share among pairs the filter retains**, [16.7146%, 16.9704%] is exactly right and the ceiling is the identity described above.

If the estimand is **the never-started share on the whole position-5 population** — the quantity Step 9's headline reads as "of users who completed S1" — then the excluded 604 pairs are still in the denominator with unknown status, and the feasible range on the single denominator 196,654 is **[16.6633%, 16.9704%], width 0.3071 pp**. **The published floor sits +0.0513 pp above the low end of that range, so it is not a floor for it** — if every excluded pair had in fact started S2, which is the exact case liveness exists to guard against, the share is 16.6633%, below the published floor. This is `0046` §4's own objection to PF-LIMIT's floor, in the same form, against the adopted rule.

**The ceiling is untouched by this** — it is the same number under both estimands, and it is still an identity. **Nothing is adopted here**: which estimand Step 9 reports is the Human Lead's call, and both intervals are supplied so the choice is explicit rather than implied by an arithmetic convention.

## 5. The waterfall, with line 6 reported OUTCOME-CONDITIONAL

Positions 1 and 2 of the Step 8 order are Step 8's and are not rebuilt here; no show in the frame has `L2 = 1` (1,138 shows), so position 2 removes nothing on this frame. Position 7 is an annotation and contributes no line.

| Position | Filter | APPLY rows out | APPLY removed | DERIV rows out | DERIV removed |
| ---: | :--- | ---: | ---: | ---: | ---: |
| 3 | S1 completion rule | 220,107 | — | 220,107 | — |
| 4 | contamination exclusion (Step 5) | 201,900 | — | 152,126 | — |
| 5 | right-censoring D10 at W = 108 | 196,654 | — | 147,370 | — |
| 6 | liveness (adopted rule) | 196,050 | 604 | 147,370 | 0 |
| 7 | outcome assignment at tau1 and tau2 | 196,050 | 0 | 147,370 | 0 |

**Line 6 is outcome-conditional and is reported as such** (`0046` §5): its removal count is a function of the position-5 outcome annotation, because the rule's second conjunct is `|A| = 0`. `|A|` and the insertion test are row-local predicates on the position-5 output and commute exactly, so the final row set does not depend on which is read first; only the waterfall's presentation does. Two faithful instances that do not label line 6 this way will diverge on the waterfall while agreeing on every share.

**Monotone decrease.** On **APPLY** it holds **strictly** at line 6 — 604 rows removed. On **DERIV** it holds **only non-strictly** at line 6 — 0 rows removed, the count is unchanged, and an implementation asserting a strict decrease at every line would fail here on correct data.

## 6. The two weaknesses `0046` records — tested, not repeated

### 6.1 Does this gate's dual run exercise the rule?

**On DERIV, no. The exclusion set is empty at every arm tested — 38, 46, 77, 91, 107, 108, 150, 213 — so on that population the two instances' diff is `0 = 0` and agreement there is worth nothing.** Stated plainly, as asked.

**On APPLY, yes, partially, and that is more than `0046` §7 allows for.** This rerun measures APPLY directly: 604 excluded pairs from 191 accounts at `W = 108`, 485–716 across the arm grid, three shares, a bound and a waterfall line. Every one of those figures is a diffable quantity that depends on both conjuncts. **If the Human Lead diffs only DERIV figures, this gate proves nothing; if the APPLY figures are diffed, it exercises the rule on the population Step 8 will use.**

**What the APPLY diff still cannot reach**: this instance builds APPLY from the Step 5 pair table, not from Step 8's own positions 1–5. An error in Step 8's frame join, its `L2 = 1` exclusion or its censoring implementation is invisible here, and the two Step 7 arms could agree exactly while Step 8 hands liveness a different row set.

### 6.2 The rule is first exercised at Step 8 — what this gate can and cannot establish

**Can establish:** the rule statement is unambiguous enough for two isolated instances to produce the same exclusion set on a fixed population; the exclusion set is entirely never-started, which is what makes the Step 9 bound an identity rather than an arithmetic operation on an arbitrary set; the counts and their `W`-coupling.

**Cannot establish:** that the rule is *right*. Nothing here tests whether an account with no insertion after `τ1` was in fact gone, and the rule's warrant — that liveness licenses trusting a null — is an argument, not a measurement. The gate also cannot establish the headline's sensitivity to the rule, because that runs through Step 8's table and Step 9's bound; the only quantity this instance can offer is the -0.2558 pp APPLY movement in §3, computed on this instance's own reconstruction of the population.

## 7. Where `0046` §1's stated mechanism is wrong, though its numbers are right

`0046` §1 says the DERIV zero is **forced by construction — "line 4 requires S2 evidence, so no line-4 pair can have `|A| = 0` and no S2 record."** The **count is confirmed**. **The mechanism is not**, on three measurements:

1. **Line 4's `has_s2` does not imply `|A| ≥ 1`.** At `W = 108`, **9,145 DERIV pairs are never-started** — they hold S2 evidence dated at or after `τ1`. The zero comes from none of them coinciding with a silent account, not from the conjunct being unsatisfiable.
2. **`|A|` needs an *in-`E2`* record, and line 4 only needs an S2 record.** 4 line-4 pairs hold S2 records none of whose episode numbers are in `E2`, so their `|A|` is 0 at every `W` — the configuration `0046` says cannot exist on line 4.
3. **What actually produces the zero at every arm is D10, one position earlier.** 4 line-4 pairs satisfy **both** conjuncts at every arm on the grid, and **all of them are removed by right-censoring at position 5**, before liveness is reached. The DERIV zero is a consequence of the filter order, not of line 4's definition.

Solving the rule for the set of `W` at which each pair would be excluded — `τ1` must lie between the account's last insertion instant and the pair's first in-`E2` S2 timestamp — gives **29 line-4 pairs with a non-empty interval**, split as follows. 25 have a finite upper end: 23 of those intervals close below `W` ≈ 1.7 days and 2 sit near `W` ≈ 2,275 and 2,360 days, so no `W` anyone would adopt reaches them. The remaining 4 have **no upper end at all** — they would be excluded at every `W` above roughly 0.87 days, and **only D10 keeps them out of the exclusion set.** So "forced by construction" is the wrong description at both ends. The same interval calculation reconstructs the APPLY exclusion counts at every arm exactly (604 at `W = 108`), which is an independent check on the implementation.

The mechanism exists because 22.68% of dated records in the sweep claim a `watched_at` later than their own calibrated insertion instant (6,271,584 of 27,656,434; 922,504 of them S2). A record like that lets an account be silent after `τ1` while holding S2 evidence dated after `τ1`. **Most of that 22.68% is almost certainly calibration noise, not real future-dating** — for a record watched in real time the claimed instant and the interpolated insertion instant differ by minutes in either direction, and roughly half of those differences fall on the later side. The count is reported as the mechanism's upper envelope, not as a claim that six million records were written before they were watched.

**Recommended correction to the record, for the Human Lead:** keep the exclusion counts; replace "forced by construction" with "zero at every `W` on the Step 13 grid, produced by D10 removing the four candidate pairs at position 5."

## 8. Judgement calls this instance made, where the spec does not settle it

1. **Liveness evidence is account-wide, over every record in the account's sweep** — any show, any season, any `kind`, any `action` — not restricted to the pair's own show. The spec says "the account shows no insertion instant", which reads account-wide, and that is how it is implemented. A per-show reading would exclude far more.
2. **"No insertion instant after `τ1`" is implemented as `max(instants) <= τ1`, i.e. strictly after.** An instant landing exactly on `τ1` does not make the account live. This matches the half-open convention used for `A` and is the same operator this instance used at `b4`.
3. **Records outside the fitted calibration range are clamped** by `np.interp` to the endpoint values (1,862 below, 5,094 above, of 27,656,813). The curve is a required input and is not refitted, so the clamping is reported rather than repaired.
4. **`|A| = 0` is read at `τ1` on `A`, never at `τ2` on `A_H`.** `0046` and Step 1 §7 both say Never-started, and Never-started is a `τ1` statement.
5. **D11 is applied before the rule** — records at or after `τ_pull` are discarded (80 distinct-episode records), consistent with every other step.
6. **The waterfall's positions 1–3 are reported from this instance's own inputs** (the Step 5 pair table's 220,107 S1-completer rows), not rebuilt from the Step 2 frame. Step 8 owns those positions and may legitimately report them differently.
7. **DERIV is defined as line 4 less D10 at each arm**, so its `n` moves with `W` exactly as APPLY's does; the two populations are censored on the same `max(W, 91) + H` rule.

## 9. Provenance

- **Zero API calls.** Every input was read from disk.
- Calibration: `processed/step5/calibration.npz`, 10,918 knots, **read, not refitted**, applied verbatim as in `src/step5_calibrate.py`.
- Row-level detail — populations, liveness states, outcome states, feasible-`W` intervals — is in `processed/step7/alt2_b/`. This artifact and its JSON companion contain counts and aggregates only.
- Scripts: `src/step7_alt2_b_1_population.py`, `_2_outcomes.py`, `_3_rule.py`, `_4_waterfall.py`, `_4b_forcedness.py`, `_4c_candidates.py`, `_5_bootstrap.py`, `_6_deliver.py`.
- The per-account maximum insertion instant was recomputed from the sweep and the stored curve, then asserted equal to the distinct-instant sequence this instance built at `processed/step7/b4/`; the Step 5 waterfall was asserted before either population was used.

**Nothing here is adopted. This instance does not record an approval.**
