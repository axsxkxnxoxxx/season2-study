# Step 9 — headline result. **ARM `b`.**

> **CORRECTED EMISSION — 2026-08-21. ARM `b`.** This file supersedes the premiere-anchored 91-day arm of `artifacts/step9-headline-b.md`, and **only** that arm. The adopted `W108_s2_finale` arm is unchanged and is not superseded: it was verified leaf-for-leaf identical and its harness control reproduces.

> **Why.** `src/step9_b_1_compute.py` converted the premiere-anchored `T0` column to epoch seconds with `// 10 ** 9` against a `datetime64[us, UTC]` dtype, so every value was epoch-**seconds ÷ 1000** — a 1970 date. The superseded figures were correctly computed from that vector and are **kept and marked at each point of use** in the file above, because the record of what the defect produced is the evidence for the finding.

> **Provenance.** Promoted from `processed/step9/b/preview/step9-headline-b.md` (sha256:12 `6d61f241890e`) by `src/step9_b_7_emit_corrected.py` (sha256:12 `84415309ebb8`) at 2026-08-21T21:56:18Z, git `c790f3a`. **The promotion appended this header and section 10 and changed no figure and no sentence of the body.**

> **SIGNED OFF BY THE PRODUCING ARM. This arm attests that every figure in this file was produced by its own pipeline at the settings recorded beside it, and that this emission is byte-identical in every measurement to processed/step9/b/preview/, which is what this arm's corrected run wrote. No figure in this file was hand-entered and none was edited after emission.**

> **Document instance:** `step9-b-corrected-2026-08-21`. THIS IS NOT A SECOND ARM FILE. It is arm b's corrected emission of arm b's own document, and $.document_scope.arm is 'b' in both it and the file it supersedes. A merge that globbed artifacts/step9-headline-*.json on the arm field alone would pick up BOTH and could read them as two arms. THIS DOCUMENT THEREFORE CARRIES A DISTINCT INSTANCE VALUE -- 'DOCUMENT INSTANCE: step9-b-corrected-2026-08-21', at $.document_scope.note -- so the superseded file and this one are DISTINGUISHABLE rather than interchangeable. THAT IS ALL IT DOES: it makes the two tellable apart and states nothing about which a merge takes. The merge's input contract is Step 13b's, and Step 13b is the Human Lead's; an arm does not decide what the merge reads. Human Lead ruling 2, 2026-08-21.

> **Where that value lives in the JSON half.** $.document_scope carries additionalProperties: false in artifacts/step8b-output-schema.json, and its permitted keys are role, producing_step, arm, merge, also_written_by_steps, isolation_rule, note and source. A NEW KEY WOULD FAIL THE SCHEMA, and the schema is Step 8b's rather than this arm's to widen, so the instance value is carried in the permitted free-text slot -- $.document_scope.note -- with a fixed leading token 'DOCUMENT INSTANCE: ' so it can be matched exactly rather than read out of prose. REPORTED as a constraint this emission worked within, not as a preference.

---


> **This is ONE ARM'S FILE.** It carries arm `b`'s measurement and nothing else. It asserts nothing about arm `a`, about the merged document, or about the state of any other step. **The dual control is the Human Lead's DIFF between the two arm files, before the merge.**

| | |
| :--- | :--- |
| **Step** | 9, headline result — chained, dual implementation |
| **Arm** | `b` (`data-scientist-b`) |
| **Build** | `step9/b/2026-08-20` |
| **Generated** | 2026-08-21T21:56:18Z by `src/step9_b_3_emit.py` (sha256:12 `14c2938512c5`) |
| **Schema** | `1.9.0`, `urn:season2-study:step8b-output-schema:1.9.0` |
| **Adopted rule revision** | 6, **READ not typed** from `processed/step5/adopted_rule.json`, key `_SUPERSEDED_FIGURES_CORRECTED_2026_08_13.approved_rule_revision_6`, sha256:12 `2e878460bd55` |
| **API calls** | 0 |
| **Adopts** | nothing |

**Inputs.**
- `artifacts/step8-waterfall-a.json (sha256:12 4de6946b6435)`
- `artifacts/step8-waterfall-b.json (sha256:12 e75d08e892c2)`
- `processed/step8/a/scan.npz, processed/step8/a/positions.npz (pair-level arrays for the premiere-anchored arm and the account clustering)`
- `src/step8_a_lib.py (sha256:12 1fcabc70c6d6) -- Step 8's own rule implementation, driven with a substituted T0 so the premiere arm is not a second definition`
- `processed/step2/frame.csv (S2 premiere dates, E2, L2, F2)`
- `processed/step5/adopted_rule.json (the adopted-rule revision, READ not typed)`
- `processed/step9/b/stage1_counts.json, processed/step9/b/stage2_bootstrap.json`

---

## 1. What this arm measured, and what it consumed

**CONSUMED FROM STEP 8, NOT REBUILT.** Both populations and every waterfall, liveness-exclusion and air-period figure on the adopted arm are Step 8's. Rebuilding either population would be a second definition, and a reconstruction that agrees today is still a second definition tomorrow — the dual diff cannot see it, because both instances would rebuild the same way.

**MEASURED HERE:** the confidence intervals (both objects), the three bounds and their attainable corners, the three-ceiling arithmetic, and the **whole of the premiere-anchored 91-day arm**, which no step in the spec produces. That arm is measured by driving **Step 8's own rule implementation** with a substituted `T0`, so it is the same implementation and not a second one; the harness was first run at the adopted setting and reproduced all thirteen of Step 8's consumed counts exactly before it was trusted anywhere else.

## 2. The headline

**Never started is a `W`-day statement read at `τ1`. Continued is a `W + H`-day statement read at `τ2` on `A_H`. THE TWO ARE NOT MEASURED ALIKE.** Started-and-left is *also* a null: `|A| ≥ 1` is observed, the failure to meet the Continued condition is not.

### 2.1 `W108_s2_finale__step9__r6` — W = 108 d, H = 91 d, clock origin `s2_finale`  **[PRIMARY HEADLINE]**

THE ADOPTED ARM. T0 = max(S2 finale air date, first-pass S1 completion date) -- the FINALE, not the premiere; premiere anchoring is withdrawn (Step 1 SS6). Never-started is read at tau1 = [[T0]] + 108 x 24h and Continued at tau2 = [[T0]] + 199 x 24h on A_H, so the two states are 108-day and 199-day statements and are not measured alike. Every boundary test is the half-open UTC-instant form watched_at < tau.

**APPLY** — position-5 row set **196,654**, post-liveness row set **195,951**.

| outcome | share (post-liveness) | pairs | 95% CI, **LEVEL** | width | horizon |
| :--- | ---: | ---: | :--- | ---: | ---: |
| never started | **16.7231%** | 32,769 | [16.1650%, 17.2912%] | 1.1262 pp | 108 d |
| started and left | **9.7177%** | 19,042 | [9.3485%, 10.0934%] | 0.7449 pp | 199 d |
| continued | **73.5592%** | 144,140 | [72.8442%, 74.2875%] | 1.4433 pp | 199 d |

| bound | floor | ceiling | width | on |
| :--- | ---: | ---: | ---: | :--- |
| never started | 16.6633% (32,769) | 16.9704% (33,373) | 0.3071 pp | position 5, n = 196,654 |
| started and left | 9.6372% (18,952) | 10.0405% (19,745) | 0.4032 pp | position 5, n = 196,654 |
| continued | *not published* | 73.6995% (144,933) | — | position 5, n = 196,654 |

**Conditional sub-interval on started-and-left** — a *labelled conditional*, **never the bound**: [9.6372%, 9.7333%], width 0.0961 pp. MEASURED NOT TO COINCIDE: the ceilings differ by 604 pairs (604 never-started exclusions conceded to started-and-left in the bound and not in the sub-interval), so the two intervals are different objects.

**THREE CEILINGS, AND THEY CANNOT ALL HOLD.** 16.9704% + 10.0405% + 73.6995% = **100.7104%** on 196,654 — excess **0.7104 pp = 1397 pairs**. THERE ARE THREE CEILINGS AND THEY CANNOT ALL HOLD. They are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous ones. THE MECHANISM, not just the total: each never-started exclusion appears in ALL THREE ceiling numerators -- excess 2 each -- and each started-and-left exclusion in TWO -- excess 1 each; with the 90 conceded channel pairs admitted, 2 x 604 + 99 + 90 = 1397 pairs = 0.7104 pp on APPLY. The stated expression carries the first two terms; the channel term is added here because it is not one of this block's own operands, which is why decisions/0053 SS4 leaves this identity to the writing step.

**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint in this block is on the POSITION-5 row set (196654); every published share is on the POST-LIVENESS row set (195951). On DERIV at the adopted arm the never-started point estimate lies OUTSIDE its own bound, and that is a consequence of this difference and not of an error.**

**DERIV** — position-5 row set **147,370**, post-liveness row set **147,271**.

| outcome | share (post-liveness) | pairs | 95% CI, **LEVEL** | width | horizon |
| :--- | ---: | ---: | :--- | ---: | ---: |
| never started | **6.2096%** | 9,145 | [5.8415%, 6.6054%] | 0.7639 pp | 108 d |
| started and left | **11.3695%** | 16,744 | [10.8961%, 11.8583%] | 0.9621 pp | 199 d |
| continued | **82.4208%** | 121,382 | [81.7944%, 83.0360%] | 1.2416 pp | 199 d |

| bound | floor | ceiling | width | on |
| :--- | ---: | ---: | ---: | :--- |
| never started | 6.2055% (9,145) | 6.2055% (9,145) | 0.0000 pp  *(DEGENERATE — a measured zero width, not missing data)* | position 5, n = 147,370 |
| started and left | 11.3015% (16,655) | 11.4291% (16,843) | 0.1276 pp | position 5, n = 147,370 |
| continued | *not published* | 82.4930% (121,570) | — | position 5, n = 147,370 |

**Conditional sub-interval on started-and-left** — a *labelled conditional*, **never the bound**: [11.3015%, 11.4291%], width 0.1276 pp. MEASURED TO COINCIDE: the never-started exclusion component is 0 on DERIV, so conditioning on it constrains nothing and the sub-interval is the bound. Both are [11.3015%, 11.4291%]. Stated here rather than left for a reader to notice two identical intervals.

**THREE CEILINGS, AND THEY CANNOT ALL HOLD.** 6.2055% + 11.4291% + 82.4930% = **100.1276%** on 147,370 — excess **0.1276 pp = 188 pairs**. THERE ARE THREE CEILINGS AND THEY CANNOT ALL HOLD. They are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous ones. THE MECHANISM, not just the total: each never-started exclusion appears in ALL THREE ceiling numerators -- excess 2 each -- and each started-and-left exclusion in TWO -- excess 1 each; with the 89 conceded channel pairs admitted, 2 x 0 + 99 + 89 = 188 pairs = 0.1276 pp on DERIV. The stated expression carries the first two terms; the channel term is added here because it is not one of this block's own operands, which is why decisions/0053 SS4 leaves this identity to the writing step.

**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint in this block is on the POSITION-5 row set (147370); every published share is on the POST-LIVENESS row set (147271). On DERIV at the adopted arm the never-started point estimate lies OUTSIDE its own bound, and that is a consequence of this difference and not of an error.**


### 2.2 `W091_s2_premiere__step9__r6` — W = 91 d, H = 91 d, clock origin `s2_premiere`

THE SECOND HEADLINE, at Netflix's own 91-day reporting window, so the result is commensurable with the public argument. T0' = max(S2 PREMIERE air date, first-pass S1 completion date), because Netflix's window runs from release. THIS ARM SITS ON A DIFFERENT ORIGIN FROM THE PRIMARY HEADLINE AND THE TWO ARE NOT THE SAME MEASUREMENT AT TWO WINDOW LENGTHS. It is not the finale-anchored 91-day grid arm either, which is Step 13's and is not written in this file.

**APPLY** — position-5 row set **196,654**, post-liveness row set **196,048**.

| outcome | share (post-liveness) | pairs | 95% CI, **LEVEL** | width | horizon |
| :--- | ---: | ---: | :--- | ---: | ---: |
| never started | **18.1507%** | 35,584 | [17.5572%, 18.7458%] | 1.1885 pp | 91 d |
| started and left | **13.1468%** | 25,774 | [12.7123%, 13.5876%] | 0.8753 pp | 182 d |
| continued | **68.7026%** | 134,690 | [67.9648%, 69.4707%] | 1.5059 pp | 182 d |

| bound | floor | ceiling | width | on |
| :--- | ---: | ---: | ---: | :--- |
| never started | 18.0947% (35,584) | 18.3658% (36,117) | 0.2710 pp | position 5, n = 196,654 |
| started and left | 13.0686% (25,700) | 13.4144% (26,380) | 0.3458 pp | position 5, n = 196,654 |
| continued | *not published* | 68.8366% (135,370) | — | position 5, n = 196,654 |

**Conditional sub-interval on started-and-left** — a *labelled conditional*, **never the bound**: [13.0686%, 13.1434%], width 0.0748 pp. MEASURED NOT TO COINCIDE: the ceilings differ by 533 pairs (533 never-started exclusions conceded to started-and-left in the bound and not in the sub-interval), so the two intervals are different objects.

**THREE CEILINGS, AND THEY CANNOT ALL HOLD.** 18.3658% + 13.4144% + 68.8366% = **100.6168%** on 196,654 — excess **0.6168 pp = 1213 pairs**. THERE ARE THREE CEILINGS AND THEY CANNOT ALL HOLD. They are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous ones. THE MECHANISM, not just the total: each never-started exclusion appears in ALL THREE ceiling numerators -- excess 2 each -- and each started-and-left exclusion in TWO -- excess 1 each; with the 74 conceded channel pairs admitted, 2 x 533 + 73 + 74 = 1213 pairs = 0.6168 pp on APPLY. The stated expression carries the first two terms; the channel term is added here because it is not one of this block's own operands, which is why decisions/0053 SS4 leaves this identity to the writing step.

**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint in this block is on the POSITION-5 row set (196654); every published share is on the POST-LIVENESS row set (196048). On DERIV at the adopted arm the never-started point estimate lies OUTSIDE its own bound, and that is a consequence of this difference and not of an error.**

**DERIV** — position-5 row set **147,370**, post-liveness row set **147,297**.

| outcome | share (post-liveness) | pairs | 95% CI, **LEVEL** | width | horizon |
| :--- | ---: | ---: | :--- | ---: | ---: |
| never started | **7.9974%** | 11,780 | [7.5523%, 8.4578%] | 0.9056 pp | 91 d |
| started and left | **15.8157%** | 23,296 | [15.2607%, 16.3929%] | 1.1322 pp | 182 d |
| continued | **76.1869%** | 112,221 | [75.4822%, 76.8841%] | 1.4019 pp | 182 d |

| bound | floor | ceiling | width | on |
| :--- | ---: | ---: | ---: | :--- |
| never started | 7.9935% (11,780) | 7.9935% (11,780) | 0.0000 pp  *(DEGENERATE — a measured zero width, not missing data)* | position 5, n = 147,370 |
| started and left | 15.7576% (23,222) | 15.8574% (23,369) | 0.0997 pp | position 5, n = 147,370 |
| continued | *not published* | 76.2489% (112,368) | — | position 5, n = 147,370 |

**Conditional sub-interval on started-and-left** — a *labelled conditional*, **never the bound**: [15.7576%, 15.8574%], width 0.0997 pp. MEASURED TO COINCIDE: the never-started exclusion component is 0 on DERIV, so conditioning on it constrains nothing and the sub-interval is the bound. Both are [15.7576%, 15.8574%]. Stated here rather than left for a reader to notice two identical intervals.

**THREE CEILINGS, AND THEY CANNOT ALL HOLD.** 7.9935% + 15.8574% + 76.2489% = **100.0997%** on 147,370 — excess **0.0997 pp = 147 pairs**. THERE ARE THREE CEILINGS AND THEY CANNOT ALL HOLD. They are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous ones. THE MECHANISM, not just the total: each never-started exclusion appears in ALL THREE ceiling numerators -- excess 2 each -- and each started-and-left exclusion in TWO -- excess 1 each; with the 74 conceded channel pairs admitted, 2 x 0 + 73 + 74 = 147 pairs = 0.0997 pp on DERIV. The stated expression carries the first two terms; the channel term is added here because it is not one of this block's own operands, which is why decisions/0053 SS4 leaves this identity to the writing step.

**THE BOUNDS AND THE SHARES ARE ON DIFFERENT POPULATIONS. Every bound endpoint in this block is on the POSITION-5 row set (147370); every published share is on the POST-LIVENESS row set (147297). On DERIV at the adopted arm the never-started point estimate lies OUTSIDE its own bound, and that is a consequence of this difference and not of an error.**


## 3. Both bootstrap objects — and a level is never compared with a movement

**ALL FOUR ELEMENTS ARE FIXED BY THE SPEC AND NONE IS THIS ARM'S CHOICE:** `B` = **10,000**, seed = **20260818**, resampling unit = **account**, statistic = **both levels and movements**. Every interval in this file restates them at the point of use.

**ACCOUNT LEVEL because pairs are not independent** — one account contributes many, and pair-level resampling understates the interval.

**PAIRED MOVEMENTS**, the second object: the change in each share caused by the liveness filter — post-liveness level minus position-5 level — differenced **inside each replicate**, so the same account weights produce both terms.

| arm | population | outcome | 95% CI, **MOVEMENT** | width | level width | ratio |
| :--- | :--- | :--- | :--- | ---: | ---: | ---: |
| W108_s2_finale__step9__r6 | APPLY | never started | [-0.2986, -0.2011] pp | 0.0975 pp | 1.1262 pp | **12×** |
| W108_s2_finale__step9__r6 | APPLY | started and left | [-0.0272, -0.0048] pp | 0.0224 pp | 0.7449 pp | **33×** |
| W108_s2_finale__step9__r6 | APPLY | continued | [+0.2165, +0.3146] pp | 0.0981 pp | 1.4433 pp | **15×** |
| W108_s2_finale__step9__r6 | DERIV | never started | [+0.0031, +0.0054] pp | 0.0023 pp | 0.7639 pp | **337×** |
| W108_s2_finale__step9__r6 | DERIV | started and left | [-0.0763, -0.0444] pp | 0.0318 pp | 0.9621 pp | **30×** |
| W108_s2_finale__step9__r6 | DERIV | continued | [+0.0412, +0.0709] pp | 0.0297 pp | 1.2416 pp | **42×** |
| W091_s2_premiere__step9__r6 | APPLY | never started | [-0.2623, -0.1729] pp | 0.0894 pp | 1.1885 pp | **13×** |
| W091_s2_premiere__step9__r6 | APPLY | started and left | [-0.0068, +0.0135] pp | 0.0203 pp | 0.8753 pp | **43×** |
| W091_s2_premiere__step9__r6 | APPLY | continued | [+0.1723, +0.2552] pp | 0.0829 pp | 1.5059 pp | **18×** |
| W091_s2_premiere__step9__r6 | DERIV | never started | [+0.0028, +0.0053] pp | 0.0025 pp | 0.9056 pp | **359×** |
| W091_s2_premiere__step9__r6 | DERIV | started and left | [-0.0557, -0.0293] pp | 0.0264 pp | 1.1322 pp | **43×** |
| W091_s2_premiere__step9__r6 | DERIV | continued | [+0.0265, +0.0505] pp | 0.0240 pp | 1.4019 pp | **58×** |

***A LEVEL AND A MOVEMENT ARE NEVER COMPARED TO EACH OTHER.*** The level and the movement on one quantity differ by up to an order of magnitude, so a reader who is not told which one they are reading is wrong by that much. **Both objects are labelled at the point of use and neither is presented as *the* design.**

**A property of these measurements, stated because it bears on how they may be read: a paired movement is a quantity in PERCENTAGE POINTS and it is negative wherever the liveness filter lowers a share. Six of the twelve movements this arm measured have negative endpoints.** A movement is not a percentage and must not be rendered as one.

**Every interval here is an outcome-share quantity, whose binding cluster is the ACCOUNT**, so every one of them says `account` and none inherits it silently. **No window-`W` percentile interval is declared**: `W`'s binding cluster is the **show**, account-level resampling would understate it, and Step 6 is an approved gate whose instruction is *complete; do not re-derive*. **There is therefore no unit disagreement to report in this file, and that is stated rather than left to be inferred from an absence.**

## 4. The bound's scope, published with the bound

**The bound is covering with respect to insertion-dormancy, exhaustively; open only across channel classes (D4, D9).**

**The stopping rule, so that "covering" is not a claim without one:** Concede every pair that was dormant before the instant at which its own state-defining null is read: tau1 for the never-started null, tau2 for the Continued null. Every pair either was inserting through its test instant or was not, so the rule terminates with no residue.

**D4 and D9 publish ALONGSIDE these bounds and are never folded into them.** They are **Step 8's** figures; this arm does not write them and does not recompute them. `$.channel_classes` and `$.discovery_channel_overlap` carry the absence idiom here and are filled once, at Step 13b, from Step 8's own artifact.

## 5. Attainable corners

**The three ceilings are ALTERNATIVE WORST CASES OVER ONE EXCLUSION SET, not simultaneous ones.** Each corner below is a complete and consistent assignment of every excluded and conceded pair, and sums to the position-5 population exactly.

**W108_s2_finale__step9__r6 · APPLY**

| corner | never started | started and left | continued |
| :--- | ---: | ---: | ---: |
| never started bound, floor | 16.6633% | 9.6372% | 73.6995% |
| never started bound, ceiling | 16.9704% | 9.7333% | 73.2962% |
| started and left bound, ceiling | 16.6633% | 10.0405% | 73.2962% |

**W108_s2_finale__step9__r6 · DERIV**

| corner | never started | started and left | continued |
| :--- | ---: | ---: | ---: |
| never started bound, floor | 6.2055% | 11.3015% | 82.4930% |
| never started bound, ceiling | 6.2055% | 11.4291% | 82.3655% |

**W091_s2_premiere__step9__r6 · APPLY**

| corner | never started | started and left | continued |
| :--- | ---: | ---: | ---: |
| never started bound, floor | 18.0947% | 13.0686% | 68.8366% |
| never started bound, ceiling | 18.3658% | 13.1434% | 68.4909% |
| started and left bound, ceiling | 18.0947% | 13.4144% | 68.4909% |

**W091_s2_premiere__step9__r6 · DERIV**

| corner | never started | started and left | continued |
| :--- | ---: | ---: | ---: |
| never started bound, floor | 7.9935% | 15.7576% | 76.2489% |
| never started bound, ceiling | 7.9935% | 15.8574% | 76.1491% |

## 6. Bound width against sampling width

**The convention is NAMED, because the two arms' sampling-width conventions are named inputs and reconciling them is a spec decision, not an arm's.** `arm_b_convention`: the denominator is the width of the 95% percentile-bootstrap interval on the corresponding **post-liveness level** for the same outcome state, arm and population, account-clustered at the fixed settings. **`reconciled_with_other_arm: false` at every point of use.**

| arm | population | quantity | ratio |
| :--- | :--- | :--- | ---: |
| W108_s2_finale__step9__r6 | APPLY | never started | 0.2727 |
| W108_s2_finale__step9__r6 | APPLY | started and left | 0.5414 |
| W108_s2_finale__step9__r6 | APPLY | started and left sub interval | 0.1290 |
| W108_s2_finale__step9__r6 | DERIV | never started | 0.0000 |
| W108_s2_finale__step9__r6 | DERIV | started and left | 0.1326 |
| W108_s2_finale__step9__r6 | DERIV | started and left sub interval | 0.1326 |
| W091_s2_premiere__step9__r6 | APPLY | never started | 0.2280 |
| W091_s2_premiere__step9__r6 | APPLY | started and left | 0.3950 |
| W091_s2_premiere__step9__r6 | APPLY | started and left sub interval | 0.0854 |
| W091_s2_premiere__step9__r6 | DERIV | never started | 0.0000 |
| W091_s2_premiere__step9__r6 | DERIV | started and left | 0.0881 |
| W091_s2_premiere__step9__r6 | DERIV | started and left sub interval | 0.0881 |

## 7. `$.arm_grid_days` is NOT this arm's block

$.arm_grid_days IS STEP 13's BLOCK. It is required at the root of every file and block_ownership marks it may_first_writer_fill, so THIS ARM FILLED IT AS FIRST WRITER AND IT IS NOT ITS OWN. The eight values are COPIED from the Human Lead's ruling at decisions/0075; they are not a measurement taken here and Step 9 varies nothing across them. Step 13 is dual, so a value neither of its arms wrote must be visible as such at the diff rather than inferred.

Values as filled: `[38, 46, 77, 91, 107, 108, 150, 213]`.

## 8. What this arm declined to write, and why

- **`$.cross_arm_divergences`** — `human_lead_only`, merged-document-only, and `forbidden_to_compute_here` for `step9`. **This arm cannot see the other arm, so it could only fabricate a search record.** Step 13b fills it with a real one.
- **`$.limitations`** — Human-Lead-only. Step 14's, and a non-arm-file merge source.
- **`$.channel_classes` / `$.discovery_channel_overlap`** — Step 8's D4, D9 and channel overlap. Requiring them in seven arm files would make seven writers of a figure none of them produced. **Absence idiom emitted.**
- **`$.variants` / `$.tested_ranges` / `$.subpopulation_cuts`** — Steps 13, 13 and 11/12.
- **`arms[].abandonment_distribution`** (Step 10), **`arms[].d3_prime`** and **`arms[].action_type_counts`** (Step 13) — not this step's blocks.
- **The finale-anchored 91-day grid arm** — that is Step 13's arm, not Step 9's second headline, and the two would collide under a `W`-only key. This file carries the **premiere-anchored** 91-day arm only.
- **A waterfall, a liveness-exclusion block and an air-period table at the premiere-anchored arm** — no step in the spec produces them there. **Absence stated, not silence.**

## 9. This arm's own spec choices and open items

**W108_s2_finale__step9__r6**

- WHICH STEP 8 NAMESPACE WAS CONSUMED. task-sheet.md says CONSUME STEP 8's OUTPUT and never names which of Step 8's two arms supplies the pair-level tables. This arm read the approved artifacts artifacts/step8-waterfall-a.json and artifacts/step8-waterfall-b.json for every consumed figure, and processed/step8/a/ plus src/step8_a_lib.py for the pair-level arrays and the rule implementation. The library was chosen because it exposes the adopted rule as reusable code, so the premiere-anchored arm is measured by STEP 8's OWN implementation with a substituted T0 rather than by a second one. THE CHOICE IS A SPEC GAP AND IS REPORTED, NOT RECONCILED.
- THE ADOPTED ARM'S COUNTS ARE CONSUMED, NOT REPRODUCED AS PUBLISHED FIGURES. The harness was run at W = 108 and agreed with Step 8's artifacts on all 13 consumed counts before it was trusted at any other setting, and that agreement is recorded in processed/step9/b/stage1_counts.json. The agreement is a CONTROL; the published numbers remain Step 8's.
- THE SAMPLING-WIDTH CONVENTION IS NAMED. The spec forbids reconciling the two arms' conventions, so this arm states its own -- arm_b_convention, defined at every point of use -- rather than leaving a denominator to be inferred.
- NO WINDOW-W PERCENTILE INTERVAL IS DECLARED. Step 6 is an approved gate and its own instruction is 'Complete; do not re-derive', so this arm publishes no interval on W. Every interval in this file is an outcome-share quantity whose binding cluster is the ACCOUNT, so no interval here disagrees with its binding cluster and no disagreement record is present. W's interval is SHOW-clustered and remains Step 6's.

**W091_s2_premiere__step9__r6**

- THE ROW SET IS NOT RE-CENSORED AT THIS ARM. task-sheet.md Step 9 states that both headline arms run on the same right-censored population, max(W, 91) + H. This arm reads that as the adopted arm's position-5 row set rather than a D10 re-derived at the premiere origin, and the reading is CHECKED rather than assumed BY A NAMED CHECK THAT RUNS IN THIS PIPELINE AND RAISES -- src/step9_b_0_clock.py::verify_t0_prime_order, id T0PRIME-ORDER. PART 1 reconstructs T0' from the frame's own s2_premiere_date STRINGS -- a source the epoch conversion never touches -- and compares it elementwise against the decoded T0' on 278,452 pairs: 0 mismatches. PARTS 1 AND 2 ARE ON THE FULL SCAN PAIR SET, 278,452 pairs, which is a SUPERSET of the position-5 row sets the figures in this file are on -- 196,654 on APPLY and 147,370 on DERIV, part 3's own coverage -- so their coverage is not an APPLY or a DERIV count and must not be read as one. PART 2 asserts T0' <= T0 elementwise on 278,452 pairs: 0 violations, 126,082 strictly earlier and 152,370 equal. PART 3 asserts tau2' < tau2 and tau2' <= tau_pull on the retained rows of BOTH populations -- 196,654 on APPLY and 147,370 on DERIV, 0 violations, minimum margin 17.0 days from tau2' to tau2 and 17.0 days from tau2' to tau_pull on APPLY. PART 1 IS WHAT MAKES THE CHECK FAILABLE: the bare inequality is TRUE FOR THE WRONG REASON on a collapsed T0' -- max(premiere, S1 completion) is the S1 completion date for every pair when the premiere epoch decodes to 1970, and that is <= T0 unconditionally -- which is exactly what the removed boolean was. The check RAISES rather than returning a flag, and it is demonstrated FAILING on the defective vector at logs/step9_b_premiere_clock_repro.txt. The warrant it establishes: T0' <= T0 on every pair, so tau2' < tau2 <= tau_pull and every retained pair is fully observable at this arm. THE ALTERNATIVE READING -- re-deriving D10 at the premiere origin, which would ADMIT pairs the adopted arm censors -- IS REPORTED, NOT RECONCILED: it would put the two headlines on different denominators, which is what the sentence appears to forbid.
- LIVENESS IS RE-RUN AT THIS ARM'S OWN tau1. The rule is pair-level and anchored at that pair's own tau1, so a different origin gives a different silence test. The exclusion counts here are therefore this arm's measurement and NOT Step 8's 703 / 99.
- NO WATERFALL, LIVENESS-EXCLUSION OR AIR-PERIOD BLOCK IS WRITTEN HERE. Those three carry Step 8's figures and Step 8 builds them only at the finale-anchored arm, so a figure written here would be one no step in the spec produces. The absence idiom is used rather than an invented number.

**One further reading, reported and not reconciled.** The Step 9 instruction says to report the S3-without-S2 bound (D4) and the split-artifact bound (D9) ALONGSIDE the liveness bound, while decisions/0114 E8 forbids an arm file to write $.channel_classes at all. Both are followed here: the block carries the absence idiom, and the ALONGSIDE relation survives in $.scope_qualifiers, which records that the bound is covering with respect to insertion-dormancy exhaustively and OPEN ONLY ACROSS D4 AND D9. The tension is REPORTED, NOT RECONCILED.


## 10. Defects in this emission, found by this arm

**Neither moves a number in this file.** They are published with the figures rather than held back.

### Open

- **`b-md-1`.** A TYPED COUNT IN THE .md. src/step9_b_4_md.py asserts 'Six of the twelve movements this arm measured have negative endpoints' as a literal. It is true of the figures in this emission, but it is ASSERTED rather than measured, so it cannot follow the figures if they move. Same class as the carried finding b-wf-1. STILL NOT FIXED: the rerun of 2026-08-21 was authorised for b-emit-1, and an arm does not widen the scope of an authorised rerun on its own. REPORTED so the count is not read as measured.

### Resolved in this emission

- **`b-emit-1`.** A WARRANT THIS EMISSION NOW CARRIES. The previous corrected emission stated, at $.arms[1].note and in section 9 of the .md, that the un-re-censored row set was 'CHECKED rather than assumed: T0 prime <= T0 holds for every pair' -- after the boolean that checked it, t0_is_earlier_or_equal_for_every_pair, had been removed as vacuous. A CLAIM OF HAVING CHECKED IS EITHER TRUE OR IT IS REMOVED, so on the Human Lead's ruling of 2026-08-21 this arm RECOMPUTED IT rather than softening the sentence. The check is T0PRIME-ORDER, src/step9_b_0_clock.py::verify_t0_prime_order; it runs in this pipeline, it RAISES, and the sentence now names it, states what each part compares and gives its coverage. IT IS NOT THE REMOVED BOOLEAN RESTORED: the bare inequality is true for the wrong reason on a collapsed T0' and cannot fail, so part 1 reconstructs T0' from the frame's own date STRINGS, which the epoch conversion never touches. DEMONSTRATED FAILING ON THE DEFECTIVE VECTOR at logs/step9_b_premiere_clock_repro.txt section 5 -- part 1 rejects it on 155,556 of 278,452 pairs, while part 2 run alone on that same vector passes, which is the whole of the case that part 1 is what makes the replacement failable. NO FIGURE IN THIS EMISSION MOVED: the recomputation added a check and rewrote three prose fields, and every numeric leaf is unchanged.
