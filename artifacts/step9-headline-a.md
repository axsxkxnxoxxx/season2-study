# Step 9 — Headline result. ARM `a`.

**Build** `step9/a/2026-08-20`, generated `2026-08-25T17:05:50Z` by `src/step9_a_2_emit.py` (sha256-12 `5ddad64fc8d4`). Machine-readable form: `artifacts/step9-headline-a.json`, written into Step 8b's schema `urn:season2-study:step8b-output-schema:1.10.0` and checked against it with `src/step8b_validate.py` before this file was written. The control's own output is a run record, not a finding of this arm's, and it is at `logs/step9/a_validate.json`.

**This is ONE ARM of a dual step.** It has not read the other arm's file or output folder, has not diffed anything, and carries no cross-arm block. `$.cross_arm_divergences` and `$.limitations` are omitted; they are the Human Lead's. The diff between the two arms is the dual control and it is the Human Lead's to run.

**Adopted rule revision `6`**, READ from `processed/step5/adopted_rule.json` at key `_SUPERSEDED_FIGURES_CORRECTED_2026_08_13.approved_rule_revision_6` (file sha256-12 `2e878460bd55`), never typed.

## 0. What this arm computed, and what it consumed

**Consumed from Step 8, not rebuilt** (`decisions/0070` rulings 1 and 7): the APPLY and DERIV populations, the filter waterfall, the liveness exclusion counts, the retained-pair counts per air period, and the D4 count. Step 8's output carries both populations and the D4 count, so there was nothing to stop on.

**Computed here:** the account-clustered bootstrap intervals, the three bounds at each arm, and the PREMIERE-ANCHORED 91-day arm, which Step 8 does not emit — its eight grid arms are all finale-anchored.

**The outcome operator was NOT re-implemented for the premiere arm.** `step8_a_lib.Arms` — the one implementation of Step 1 §7 on disk — was imported and its `t0` vector replaced with the premiere-anchored clock. Before any premiere figure was taken, the import was gated on reproducing Step 8's published finale-anchored counts: **positions 5 and 7 on both populations, the outcome-conditional position-5 view, the liveness exclusion split, and both right-censoring sub-lines — 0 mismatches.** A further **36 figures** at the two finale-anchored arms were compared against Step 8's arm table at emit time, also with 0 mismatches.

**Two populations, and every figure says which.** APPLY = 196,654 pairs at the adopted arm; DERIV = 147,370.

**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS.** Bounds are stated on the **position-5** row set; the published shares are on the **post-liveness** row set. On DERIV at the primary arm the point estimate lies **outside** its own bound — see §2.

## 1a. PRIMARY HEADLINE — W = 108 d, finale-anchored

`arm_id` **`W108_s2_finale__step9__r6`** · W = 108 d · H = 91 d · clock origin `s2_finale` · in the W grid: true · primary: true

**APPLY** — position 5 n = 196,654; post-liveness n = 195,951.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **16.7231%** | [16.1771%, 17.2999%] | 32,769 / 195,951 | τ1, 108 d |
| Started and left | **9.7177%** | [9.3459%, 10.1043%] | 19,042 / 195,951 | τ2, 199 d |
| Continued | **73.5592%** | [72.8447%, 74.2642%] | 144,140 / 195,951 | τ2, 199 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 16.6633% (32,769) | 16.9704% (33,373) | 0.3071 pp |
| Started and left | 9.6372% (18,952) | 10.0405% (19,745) | 0.4032 pp |
| — conditional sub-interval, labelled, NOT the bound | 9.6372% | 9.7333% | 0.0961 pp |
| Continued | *not published — Continued is never emitted as a point* | 73.6995% (144,933) | — |

**The three ceilings cannot all hold.** 16.9704% + 10.0405% + 73.6995% = **100.7104%** on 196,654, an excess of **0.7104 pp = 1,397 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.

**DERIV** — position 5 n = 147,370; post-liveness n = 147,271.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **6.2096%** | [5.8446%, 6.6000%] | 9,145 / 147,271 | τ1, 108 d |
| Started and left | **11.3695%** | [10.8926%, 11.8582%] | 16,744 / 147,271 | τ2, 199 d |
| Continued | **82.4208%** | [81.7935%, 83.0328%] | 121,382 / 147,271 | τ2, 199 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 6.2055% (9,145) | 6.2055% (9,145) | 0.0000 pp — **DEGENERATE** |
| Started and left | 11.3015% (16,655) | 11.4291% (16,843) | 0.1276 pp |
| — conditional sub-interval, labelled, NOT the bound | 11.3015% | 11.4291% | 0.1276 pp — coincides with the bound |
| Continued | *not published — Continued is never emitted as a point* | 82.4930% (121,570) | — |

**The three ceilings cannot all hold.** 6.2055% + 11.4291% + 82.4930% = **100.1276%** on 147,370, an excess of **0.1276 pp = 188 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.


## 1b. SUPPORTING — W = 91 d, finale-anchored

`arm_id` **`W091_s2_finale__step9__r6`** · W = 91 d · H = 91 d · clock origin `s2_finale` · in the W grid: true · primary: false

**APPLY** — position 5 n = 197,007; post-liveness n = 196,343.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **17.1175%** | [16.5619%, 17.7048%] | 33,609 / 196,343 | τ1, 91 d |
| Started and left | **9.7961%** | [9.4227%, 10.1850%] | 19,234 / 196,343 | τ2, 182 d |
| Continued | **73.0864%** | [72.3617%, 73.7994%] | 143,500 / 196,343 | τ2, 182 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 17.0598% (33,609) | 17.3517% (34,184) | 0.2919 pp |
| Started and left | 9.7169% (19,143) | 10.1001% (19,898) | 0.3832 pp |
| — conditional sub-interval, labelled, NOT the bound | 9.7169% | 9.8083% | 0.0914 pp |
| Continued | *not published — Continued is never emitted as a point* | 73.2233% (144,255) | — |

**The three ceilings cannot all hold.** 17.3517% + 10.1001% + 73.2233% = **100.6751%** on 197,007, an excess of **0.6751 pp = 1,330 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.

**DERIV** — position 5 n = 147,685; post-liveness n = 147,596.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **6.6824%** | [6.2991%, 7.0944%] | 9,863 / 147,596 | τ1, 91 d |
| Started and left | **11.4542%** | [10.9779%, 11.9438%] | 16,906 / 147,596 | τ2, 182 d |
| Continued | **81.8633%** | [81.2227%, 82.4931%] | 120,827 / 147,596 | τ2, 182 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 6.6784% (9,863) | 6.6784% (9,863) | 0.0000 pp — **DEGENERATE** |
| Started and left | 11.3857% (16,815) | 11.5076% (16,995) | 0.1219 pp |
| — conditional sub-interval, labelled, NOT the bound | 11.3857% | 11.5076% | 0.1219 pp — coincides with the bound |
| Continued | *not published — Continued is never emitted as a point* | 81.9359% (121,007) | — |

**The three ceilings cannot all hold.** 6.6784% + 11.5076% + 81.9359% = **100.1219%** on 147,685, an excess of **0.1219 pp = 180 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.


## 1c. NETFLIX ARM — W = 91 d, PREMIERE-anchored

`arm_id` **`W091_s2_premiere__step9__r6`** · W = 91 d · H = 91 d · clock origin `s2_premiere` · in the W grid: false · primary: false

**APPLY** — position 5 n = 196,654; post-liveness n = 196,048.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **18.1507%** | [17.5632%, 18.7551%] | 35,584 / 196,048 | τ1, 91 d |
| Started and left | **13.1468%** | [12.7069%, 13.5897%] | 25,774 / 196,048 | τ2, 182 d |
| Continued | **68.7026%** | [67.9508%, 69.4438%] | 134,690 / 196,048 | τ2, 182 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 18.0947% (35,584) | 18.3658% (36,117) | 0.2710 pp |
| Started and left | 13.0686% (25,700) | 13.4144% (26,380) | 0.3458 pp |
| — conditional sub-interval, labelled, NOT the bound | 13.0686% | 13.1434% | 0.0748 pp |
| Continued | *not published — Continued is never emitted as a point* | 68.8366% (135,370) | — |

**The three ceilings cannot all hold.** 18.3658% + 13.4144% + 68.8366% = **100.6168%** on 196,654, an excess of **0.6168 pp = 1,213 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.

**DERIV** — position 5 n = 147,370; post-liveness n = 147,297.

| Outcome | Share (post-liveness) | 95% CI, LEVEL, account-clustered | pairs | read at |
| :--- | ---: | :--- | ---: | :--- |
| Never started | **7.9974%** | [7.5591%, 8.4547%] | 11,780 / 147,297 | τ1, 91 d |
| Started and left | **15.8157%** | [15.2578%, 16.3841%] | 23,296 / 147,297 | τ2, 182 d |
| Continued | **76.1869%** | [75.4778%, 76.8804%] | 112,221 / 147,297 | τ2, 182 d |

| Bound (on position 5) | Floor | Ceiling | Width |
| :--- | ---: | ---: | ---: |
| Never started | 7.9935% (11,780) | 7.9935% (11,780) | 0.0000 pp — **DEGENERATE** |
| Started and left | 15.7576% (23,222) | 15.8574% (23,369) | 0.0997 pp |
| — conditional sub-interval, labelled, NOT the bound | 15.7576% | 15.8574% | 0.0997 pp — coincides with the bound |
| Continued | *not published — Continued is never emitted as a point* | 76.2489% (112,368) | — |

**The three ceilings cannot all hold.** 7.9935% + 15.8574% + 76.2489% = **100.0997%** on 147,370, an excess of **0.0997 pp = 147 pairs**. Mechanism: `2 * never_started_exclusions + started_and_left_exclusions + conceded_channel_pairs`. They are alternative worst cases over one set, not simultaneous ones.


## 2. Four things a reader will otherwise get wrong

**(a) The never-started floor is NOT widened, although 207 retained never-started pairs on APPLY (and 3 on DERIV) had their last insertion inside (τ1, τ2).** The reason is the ANCHORING, not the count. Never started is the null `|A| = 0` **read at τ1**, and every one of those pairs has an insertion after τ1 — which is exactly what gate `decisions/0021` licenses. Their null is OBSERVED, not conceded. The 90 pairs the started-and-left floor concedes on APPLY (89 on DERIV) differ because the **Continued** condition they negate is read at **τ2**, and they are dormant before it.

**(b) The bound's scope publishes with the bound.** It is covering with respect to INSERTION-DORMANCY, **exhaustively** — every pair either was inserting through its own test instant or was not — and **open only across the channel classes D4 and D9**, which publish ALONGSIDE and are never folded in. D4 and D9 are Step 8's figures and are not restated here: under `decisions/0114` E8 they are carried ONCE, in the merged document at Step 13b, and this file emits the absence idiom for them rather than becoming a seventh writer of a figure it did not produce.

**(c) On DERIV the never-started bound is DEGENERATE — [6.2055%, 6.2055%] — so the dual control is `x = x` there.** The informative comparison between the two arms is on APPLY. And the published DERIV never-started share, **6.2096%**, lies **outside** that bound by 0.0042 pp — not an error: the bound is on position 5 (n = 147,370) and the share is post-liveness (n = 147,271).

**(c2) The attainable corners, primary arm.** Each row is a COMPLETE allocation of the conceded pairs, so its three values sum to exactly 100 — which is what makes an endpoint *attainable* rather than merely arithmetic. Note that the never-started FLOOR corner and the started-and-left CEILING corner are the SAME corner: those two endpoints are not independent.

*APPLY, on position 5, n = 196,654*

| Corner | Never started | Started and left | Continued | sum |
| :--- | ---: | ---: | ---: | ---: |
| never_started floor | 16.6633% | 10.0405% | 73.2962% | 100.0000% |
| never_started ceiling | 16.9704% | 9.7333% | 73.2962% | 100.0000% |
| started_and_left floor | 16.9704% | 9.6372% | 73.3924% | 100.0000% |
| started_and_left floor_with_both_concessions | 16.6633% | 9.6372% | 73.6995% | 100.0000% |

*DERIV, on position 5, n = 147,370*

| Corner | Never started | Started and left | Continued | sum |
| :--- | ---: | ---: | ---: | ---: |
| never_started floor | 6.2055% | 11.4291% | 82.3655% | 100.0000% |
| started_and_left floor | 6.2055% | 11.3015% | 82.4930% | 100.0000% |

**(d) The three states are not measured alike.** Never started is a 108-day statement at the primary arm; Continued is a 199-day one. Every share above carries its own horizon.

## 3. The 91-day arm sits on a DIFFERENT ORIGIN, and the two are not one measurement at two window lengths

Netflix's window runs from **release**, so that arm is anchored on the later of the S2 PREMIERE date and the first-pass S1 completion date. The primary arm is anchored on the FINALE. **They are two measurements, not one measurement at two window lengths**, and the movement between them mixes a window change with an origin change. That is why this file also carries the finale-anchored 91-day arm — it holds the origin fixed and moves only the window, so the two effects can be separated:

| APPLY, never-started share (post-liveness) | value |
| :--- | ---: |
| W = 108, finale (primary) | 16.7231% |
| W = 91, finale — the WINDOW moved | 17.1175% |
| W = 91, premiere — the ORIGIN then moved | 18.1507% |

So of the +1.4276 pp between the primary headline and the Netflix arm, +0.3944 pp is the window and +1.0332 pp is the origin. **The origin is the larger term.** Reporting the Netflix arm as 'the same result at a shorter window' would attribute all of it to the window.

**The finale-anchored 91-day arm is a SUPPORTING measurement, not a third headline.** Every figure in it is Step 8's at that arm, reproduced here and agreeing exactly.

## 4. The bootstrap, and both of its objects

**B = 10,000 · seed 20260818 · resampling unit ACCOUNT · statistic BOTH levels and paired movements.** All four fixed by the spec (`decisions/0103`, `decisions/0118`) and identical for both arms; this arm records no choice on any of them. Every interval in the JSON restates all four at its point of use.

**Account level, not pair level**: pairs are not independent — one account contributes many — so pair-level resampling would understate every width above. The resampling frame is the **2,481 accounts** contributing at least one pair to the position-4 output; one frame and one draw serve the whole file, which is what makes every movement below genuinely PAIRED.

**No interval in this file is show-clustered**, because this arm computes no show-bound quantity: `W` was derived at Step 6 and is not re-derived here. Every interval declares `quantity_class: outcome_shares` and `resampling_unit: account`, which is the binding cluster the record states for that class, so there is no unit disagreement to report.

**A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER.** The movement below is **post-liveness MINUS the outcome-conditional position-5 value of the same share**, resampled as one paired delta on the same accounts — what the liveness filter does to the headline. On APPLY at the primary arm the never-started LEVEL is 1.1228 pp wide and its MOVEMENT is 0.0987 pp wide — a factor of about eleven, which is how far wrong a reader goes who is not told which one they are looking at.

### All eighteen paired movements

**Nine of these cannot be written into the JSON.** `$defs.percent` types a CI endpoint as a percentage on [0, 100] and a paired movement is SIGNED, so an interval with a negative endpoint has no legal representation in the schema. The nine with non-negative endpoints are in `$.declared_intervals`; all eighteen are here. Marked **†** where the JSON cannot carry it. **This is reported, not reconciled** — no figure was clamped, re-signed or dropped.

| Arm | Population | Outcome | Movement (point) | 95% CI, MOVEMENT | in JSON |
| :--- | :--- | :--- | ---: | :--- | :---: |
| W108_s2_finale | APPLY | Never started | -0.2474 pp | [-0.2991, -0.2004] pp | † no |
| W108_s2_finale | APPLY | Started and left | -0.0156 pp | [-0.0275, -0.0048] pp | † no |
| W108_s2_finale | APPLY | Continued | +0.2630 pp | [+0.2155, +0.3146] pp | yes |
| W108_s2_finale | DERIV | Never started | +0.0042 pp | [+0.0031, +0.0054] pp | yes |
| W108_s2_finale | DERIV | Started and left | -0.0595 pp | [-0.0766, -0.0445] pp | † no |
| W108_s2_finale | DERIV | Continued | +0.0554 pp | [+0.0413, +0.0713] pp | yes |
| W091_s2_finale | APPLY | Never started | -0.2342 pp | [-0.2843, -0.1886] pp | † no |
| W091_s2_finale | APPLY | Started and left | -0.0122 pp | [-0.0235, -0.0020] pp | † no |
| W091_s2_finale | APPLY | Continued | +0.2463 pp | [+0.2010, +0.2966] pp | yes |
| W091_s2_finale | DERIV | Never started | +0.0040 pp | [+0.0029, +0.0053] pp | yes |
| W091_s2_finale | DERIV | Started and left | -0.0534 pp | [-0.0696, -0.0392] pp | † no |
| W091_s2_finale | DERIV | Continued | +0.0493 pp | [+0.0363, +0.0643] pp | yes |
| W091_s2_premiere | APPLY | Never started | -0.2151 pp | [-0.2624, -0.1726] pp | † no |
| W091_s2_premiere | APPLY | Started and left | +0.0034 pp | [-0.0072, +0.0133] pp | † no |
| W091_s2_premiere | APPLY | Continued | +0.2117 pp | [+0.1718, +0.2557] pp | yes |
| W091_s2_premiere | DERIV | Never started | +0.0040 pp | [+0.0028, +0.0053] pp | yes |
| W091_s2_premiere | DERIV | Started and left | -0.0417 pp | [-0.0557, -0.0296] pp | † no |
| W091_s2_premiere | DERIV | Continued | +0.0377 pp | [+0.0268, +0.0504] pp | yes |

## 5. Divergences between the spec and what this arm could write — REPORTED, NOT RECONCILED

**D1. The schema cannot represent a signed interval, and the spec fixes a signed statistic.** `decisions/0118` fixes the statistic as BOTH levels and paired movements, and check S41 requires both to appear per (producing step, arm). A paired movement is a difference of two shares and is signed; `$defs.percent`, which types `ci.lower` and `ci.upper`, admits only [0, 100] (or the placeholder sentinel). Nine of this arm's eighteen movement intervals have a negative endpoint and are therefore unwritable. S41 is satisfied by the nine that happen to be non-negative — which means **the control passes for an arithmetic accident**, not because the file is complete.

**D2. `both arms run on the same right-censored population, max(W, 91) + H` has two readings at the premiere-anchored arm**, and they differ by a measured amount. Reading (a), taken here: the 91-day arm runs on the primary arm's position-5 row set, censored at max(108, 91) + 91 = 199 d. Reading (b): D10 re-derived at W = 91, censoring at 182 d. Measured: (b) is a strict superset — 197,007 against 196,654 on APPLY and 147,685 against 147,370 on DERIV, with 0 pairs in (a) and not in (b). The choice moves 353 pairs on APPLY and 315 on DERIV.

  **And the difference is the W term, not the origin.** The premiere-anchored and finale-anchored censoring sets at W = 91 are **identical, measured on both populations** — because the Step 2 frame caps the S2 finale at 2025-12-31, which is earlier than the binding cutoff, so T0's `max()` is decided by the S1 completion date on every pair the cutoff can reach, and that term does not move with the origin. A reader would reasonably have expected the origin to matter here; it does not, and that is measured rather than assumed.

**D3. The spec fixes four bootstrap elements and not the resampling FRAME or the DRAW ORDER.** Two arms that draw from different account sets, or consume one seeded generator in a different order, produce different intervals from the same fixed seed — which is the failure fixing the seed exists to prevent. This arm's choice is named in `$.arms[0].headline.APPLY.by_producing_arm.arms.a.spec_choices_this_arm_made`.

**D4. `arm_grid_days` is owned by Step 13, required at the top level, and was filled by this file as first writer.** See §6.

## 6. `arm_grid_days` — filled here, and NOT this arm's block

`$.arm_grid_days` is **[38, 46, 77, 91, 107, 108, 150, 213]**. The schema requires it at the top level; `$.block_ownership` gives its owner as **step13** with `may_first_writer_fill: true`. **This file filled it as first writer and it is not this arm's figure**: the eight values are transcribed from the Human Lead's ruling at `decisions/0075`, not measured here. Step 13 is dual, so a value neither of Step 13's arms wrote must be visible as such at the diff rather than inferred — which is why it is stated here, in `spec_choices_this_arm_made`, and in this arm's report.

## 7. Blocks this arm DECLINED to write

| Block | Owner | Why not written here |
| :--- | :--- | :--- |
| `$.cross_arm_divergences` | step13b, human-lead-only | This arm cannot see the other arm, so it could only fabricate the search record. Omitted; Step 13b fills it with a real one. |
| `$.limitations` | human_lead | Human-Lead-only, Step 14. No agent may draft it. |
| `$.channel_classes` (D4, D9) | step8, published at step13b | Step 8's figures. Seven arm files filling it would make seven writers of a figure none of them produced. Absence idiom emitted. |
| `$.discovery_channel_overlap` | step8, published at step13b | Same shape, same reason. |
| `$.variants`, `$.tested_ranges` | step13 | Step 13's, and not this arm's to originate. |
| `$.subpopulation_cuts` | step11 | Step 11's. |
| `arms[].abandonment_distribution` | step10 | Step 10's; omitted rather than absence-stated, because under one file per step per arm an arm entry carries its own step's blocks only. |
| `arms[].d3_prime`, `arms[].action_type_counts` | step13 | Step 13's. |
| `$.notes.reading_a_placeholder` | step8b | Its text asserts `$.placeholder` is true, which is false here. Dropped rather than rewritten: rewriting would put this arm's words inside another step's block. Named in `spec_choices_this_arm_made`. |
| `waterfall`, `liveness_exclusions`, `retained_by_air_period` **at the premiere arm** | none | No step in the spec produces these at a premiere-anchored arm. Block-absence records emitted with `owning_step: none`, which is a finding about the spec and not a default. |

## 8. Provenance, and what this file does NOT report

**This deliverable asserts this arm's own figures, its own inputs and its own limits, and nothing else.** It carries no statement about the other arm, about other steps or gates, about the state of any shared control, or about the disk state of any surface this arm does not own. Those are measured at an instant and would be published forever. **The validator's check counts and exit status are a control's output, not this arm's measurement**, and they are in `logs/step9/a_validate.json` and in this arm's report to the Human Lead — not here.

*Every count in this file was measured on build `step9/a/2026-08-20`. Step 8's figures carry Step 8's build tag, `a/2026-08-17-0096`, which is recorded in `processed/step9/a/measured.json` together with the sha256-12 of every file consumed.*
