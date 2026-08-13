> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 gate-closing sensitivity diagnostic — instance `a`

> ## THIS IS NOT A STUDY RESULT AND NOT THE STEP 9 DELIVERABLE
>
> **Step 8 has not launched. It is an unapproved gate.** Step 8 is the step that builds the
> analysis table and fixes the headline population. Until it runs and is approved, **every share
> in this document is provisional in its POPULATION as well as in its status.**
>
> This document exists for one purpose, set by `decisions/0041` §4: to decide whether the
> liveness threshold is load-bearing, so the Step 7 gate can close. **The numbers below are a
> diagnostic. They are not the headline, they must not be cited as a result, and nothing here is
> adopted.** The Human Lead rules on whether the threshold survives.
>
> The population this runs on — **147,370 pairs** — is the Step 7 derivation/application
> population. `decisions/0041` §3 records that **Step 8 will apply liveness to 196,654**, a
> strict superset. The absolute shares will move. See §7.

| | |
| :--- | :--- |
| **Question** | Is the headline sensitive to the liveness threshold across its clustered interval? |
| **Answer** | **No.** Across the full interval the largest share moves **0.039 pp** — about **3% of the width the share is known to at all.** |
| **Instance** | `a` |
| **API calls** | **0** |
| **Adopts** | nothing |
| **Figure** | `artifacts/step7-sensitivity-a.png` |
| **Machine-readable** | `artifacts/step7-sensitivity-a.json` |

---

## 1. Population, asserted not assumed

The Step 5 waterfall was rebuilt from `processed/step5/pair_revision5.csv` and **asserted equal**
to the published figures before anything else ran:

```
201,900 → 178,165 → 155,131 → 152,126 → 128,099     computed == published
```

- **Reference line: line 4, the 152,126** (`decisions/0038` §2). The 152,126 → 128,099 filter
  concerns the first S2 watch, which plays no part in `τ1`; the lines above 152,126 carry
  contaminated `T0`, and both `τ1` and `τ2` are built from `T0`.
- **D10 right-censoring applied at `W = 108`, `H = 91`**, per `decisions/0040` §2, which moves
  the derivation after D10 so derivation and application populations are identical.
  Rule: `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`. Latest admissible `T0`: **2026-01-24**.

> ### **Post-D10 population this test runs on: 147,370 pairs** (152,126 less 4,756), across 1,138 shows and 2,402 accounts.

**`L2 = 1` exclusion:** asserted, not assumed. The Step 2 frame contains **zero** shows with
`s2_L = 1`, so Step 8's position-2 filter is a **measured no-op** here.

Every structural figure reproduces `decisions/0041` §1 exactly:

| Quantity | `0041` §1 | Measured here |
| :--- | ---: | ---: |
| Post-D10 population | 147,370 | **147,370** |
| Measured bracketing gap / open-ended / no instant at or before `τ1` | 128,467 / 751 / 18,152 | **128,467 / 751 / 18,152** |
| Not live at 1,293 d | 1,282 | **1,282** |
| Realised rate vs extended set | 0.9921% | **0.9921%** |
| Accounts carrying the exclusion set at 1,293 d | 205 of 2,402 | **205 of 2,402** |

One figure does not match, and it is recorded rather than quietly corrected. `0041` §4 states the
exclusion set moves **1,701 → 897**. At **T = 787** the count is **1,707**; **1,701 is the count
at T = 790**, the other arm's lower endpoint, which `0041` §1 records as Monte Carlo noise. A
six-pair difference, immaterial to the verdict.

## 2. What was recomputed and what was reused

**Reused, not recomputed** (`processed/step7/a4/pair_bracketing_W108.npz`): the per-pair
bracketing gap, and the `no instant before` / `no instant after` classification. Row alignment
against the new population table is **asserted**, not assumed — `user_idx`, `show`, and the `ref`
mask all compare equal.

**Built fresh for this test:** the outcome operator — `|A|` at `τ1`, `|A_H|` at `τ2`, `F2 ∈ A_H`,
and the canonical-timestamp rule. Because it is fresh, it was **validated on a population where
the answer is already on the record** before being used anywhere:

| On waterfall line 5 (the 128,099, no D10) | Record | Measured |
| :--- | ---: | ---: |
| Never started, before D11 | 8,445 (`0034` §5) | **8,445** |
| Never started, after D11 | 8,449 (`0034` §5) | **8,449** |
| Never-started share | 6.5957% (`0034` §2) | **6.5957%** |
| Pairs moved Started-and-left → Continued by the `0034` amendment | 2,246 | **2,246** |
| Monotone — no pair moves the other way | required by `A ⊆ A_H` | **holds** |

**Operative rules, all carried unchanged:**

- Outcome assignment at **two instants** (`decisions/0034`): never-started is
  `|A| = 0` at **`τ1 = ⟦T0⟧ + 108 × 24h`**; Continued is
  `|A| ≥ 1` **and** `F2 ∈ A_H` **and** `|A_H| ≥ ceil(0.90 × L2)`, on `A_H` at
  **`τ2 = ⟦T0⟧ + 199 × 24h`**; Started-and-left is the remainder. The `|A| ≥ 1` conjunct is
  retained — without it a day-150 starter completing by day 190 falls in two states.
- **Continued is a 199-day statement and never-started is a 108-day statement.** They are not
  measured alike and are not described as though they were.
- Every boundary test is the **half-open UTC-instant form** `watched_at < τ`.
  `date(watched_at) <= T1` appears nowhere.
- **Distinct episodes**, never play events; canonical timestamp is the **minimum `watched_at`**
  across the episode's records.
- Membership by **set** against `E2`, never by the range `1..F2`.
- **No drop flag** — it is OAuth Required and unavailable. All three states are inferred from
  episode-level history.
- **Liveness stays anchored at `τ1`. `τ2` plays no part in it** (`decisions/0034`).
- The **stored** Step 5 isotonic play-`id` calibration curve is read. **It is not refitted.**
- D11 applied: 179 S2 records discarded globally. On this population D10 already guarantees
  `τ2 ≤ τ_pull`, so D11 cannot bite on `A` or `A_H`; it is applied and reported rather than
  assumed inert.

## 3. The result

**Shares of live pairs, at each setting.** Excluded pairs are dropped, not bounded — the
floor-and-ceiling bound is a Step 9 obligation and this diagnostic does not discharge it (§7).

| Setting | Live pairs | Excluded | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **T = 787 d** (interval lower) | 145,663 | 1,707 | **6.2109%** | **82.3812%** | **11.4078%** |
| **T = 1,293 d** (point value) | 146,088 | 1,282 | **6.2325%** | **82.3497%** | **11.4178%** |
| **T = 2,200 d** (interval upper) | 146,473 | 897 | **6.2373%** | **82.3490%** | **11.4137%** |
| **Parameter-free** (see §4) | 146,619 | 751 | **6.2373%** | **82.3427%** | **11.4201%** |
| *(context)* no liveness filter at all | 147,370 | 0 | *6.2055%* | *82.3655%* | *11.4291%* |

Counts behind the point value: never started **9,105**, continued **120,303**, started and left
**16,680**.

**Deltas, in percentage points.**

| Comparison | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 → 1,293 | +0.0216 | −0.0315 | +0.0100 |
| 1,293 → 2,200 | +0.0048 | −0.0007 | −0.0041 |
| **787 → 2,200 (full clustered interval)** | **+0.0264** | **−0.0322** | **+0.0059** |
| 1,293 → parameter-free | +0.0048 | −0.0070 | +0.0023 |
| **max − min across all four settings** | **0.0264** | **0.0385** | **0.0123** |

### 3.1 Against what those deltas should be read

A movement in percentage points means nothing until it is set against how precisely the share is
known at all. **Account-clustered bootstrap, B = 4,000, seed 20260813**, resampling the 2,402
accounts — clustered rather than i.i.d. for the same reason the threshold itself carries a
clustered interval. Three alternate seeds are reported in the JSON; the interval is stable to
within 0.02 pp.

| Share at T = 1,293 | Point | 95% account-clustered CI | Width | Threshold span | **Span as a share of the width** |
| :--- | ---: | :--- | ---: | ---: | ---: |
| Never started | 6.2325% | [5.8591, 6.6357] | 0.777 pp | 0.026 pp | **3.4%** |
| Continued | 82.3497% | [81.7085, 82.9552] | 1.247 pp | 0.039 pp | **3.1%** |
| Started and left | 11.4178% | [10.9267, 11.9127] | 0.986 pp | 0.012 pp | **1.2%** |

**The entire clustered interval of the threshold moves the shares by roughly one thirtieth of
their own sampling width.**

### 3.2 The three settings are three points on a flat curve

The threshold was swept continuously from **30 to 4,000 days** on a 5-day grid so the flatness is
demonstrated rather than inferred from three chosen points (top three panels of the figure).

- Over the clustered interval **787–2,200 d**: never started moves **0.030 pp**, continued
  **0.045 pp**, started and left **0.017 pp**.
- Over the **whole 30–4,000 d sweep** — a range no one has proposed — the largest movement is
  **0.243 pp**, still a fifth of the sampling width.

### 3.3 One delta is statistically distinguishable from zero, and it is still negligible

Stated plainly rather than buried. The **paired** account-clustered CI for the 787 → 2,200 delta
on never-started is **[+0.008, +0.046] pp and excludes zero.** The settings are nested subsets of
the same pairs, so the paired delta has almost no variance and a 0.026 pp movement is resolvable.

**Detectable is not material.** 0.026 pp is 3.4% of the width the share itself is known to. Both
facts belong in the record; neither cancels the other.

## 4. The parameter-free rule has two readings, and this instance reconciles neither

**This is a spec contradiction, not an implementation choice, and it is reported rather than
resolved.**

`decisions/0041` §4 states the parameter-free rule as *"the account has insertion evidence
bracketing `τ1`"* — expanded in the launch instruction as *"a distinct insertion instant at or
before `τ1` and one after it."* **Read literally, the "at or before" conjunct reinstates
`decisions/0036` §2.3's second edge case**, which `decisions/0040` §1 **withdrew** for
contradicting approved gate `0021` — the ruling that returned the 18,152 pairs to the population
on the ground that any record inserted after the window closed proves the account was alive.

Both readings are computed:

| Reading | Not live iff | Excluded | Accounts touched | Never started | Continued | Started and left |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| **PF-LIMIT** — the `T → ∞` limit of the threshold rule as `0040` leaves it | no instant **after** `τ1` | 751 | 166 | 6.2373% | 82.3427% | 11.4201% |
| **PF-BRACKET** — the literal text | no instant after `τ1` **or** none at or before it | **18,903** | **1,434** | 6.3043% | 81.6832% | 12.0124% |

**PF-LIMIT is the row in §3.** It is the coherent endpoint of the family: as `T → ∞` the
threshold rule's exclusions converge to edge case (i) alone, and the 787 / 1,293 / 2,200 /
parameter-free settings then form one monotone sequence.

**PF-BRACKET is a different rule.** It excludes **25× more pairs** and touches **1,434 of 2,402
accounts** rather than 166. Relative to the 1,293 d threshold rule it moves Continued by
**−0.67 pp** and Started-and-left by **+0.59 pp** — paired clustered CIs **[−0.88, −0.47]** and
**[+0.45, +0.75]**, both excluding zero, and both **an order of magnitude larger than anything
the threshold does across its entire interval.**

> **Consequence for the gate: deleting the threshold does not on its own close it.** If the
> threshold goes, **which parameter-free rule is meant still has to be ruled on**, and that
> choice is roughly twenty times more consequential than the threshold value it replaces. The
> two readings differ by whether `0021` or `0036` §2.3(ii) governs the 18,152, and `0040` §1 has
> already ruled on that once.

## 5. Why the curve is flat — the mechanism, not just the number

The threshold is inert on this population **by construction**, and the figure's fourth panel
shows it:

| At T = 1,293 d | Pairs | Share of exclusions |
| :--- | ---: | ---: |
| Excluded on a **measured gap ≥ T** | 531 | 41.4% |
| Excluded on **absent evidence** (edge case (i)) | 751 | 58.6% |
| **Total not live** | **1,282** | **0.87% of 147,370** |

The edge-case count is **constant in `T`**; only the gap-test count moves. Across the whole
interval the gap test's contribution runs **956 → 146 pairs**, so the threshold's entire range of
authority is **810 pairs, 0.55% of the population**, concentrated in **fewer than 280 of 2,402
accounts**. A filter that small cannot move a share far, whatever value it takes.

**No invariance is claimed** for the 41.4 / 58.6 split. It is a measured figure on this
population at this percentile, and it moves with the percentile by arithmetic
(`decisions/0040` §4).

**Quota property, stated plainly and not argued away** (`decisions/0038`): taking the percentile
on the distribution the test applies to means **the level is set by the exclusion rate rather
than by any feature of the data.** Choosing `p` mechanically fixes the exclusion rate at
`100 − p`% of the reference set. That is the price of a calibrated rate, and it is disclosed.

**Degeneracy caveat, carried wherever the threshold is** (`decisions/0041` §2.1): above the
**99.4188th** percentile the extended-set percentile is **itself infinite** and the rule collapses
into edge case (i) alone — 0.25% of bootstrap replicates at `W = 108`, **2.80% at `W = 213`**.
The **PF-LIMIT row above is exactly that collapse**, computed rather than described.

## 6. The finding, stated for the ruling

> **The headline is insensitive to the liveness threshold across its account-clustered interval,
> and across a range far wider than that interval.**
>
> - Across **787 → 2,200 d** the three shares move **0.026, 0.032 and 0.006 pp**.
> - The largest movement across **all four** settings is **0.039 pp**, about **3% of the 95%
>   account-clustered sampling width** of the share it moves.
> - Over a **30 → 4,000 d** sweep the largest movement is **0.243 pp**, a fifth of that width.
> - The threshold's entire range of authority is **810 pairs**, **0.55% of the population**, in
>   fewer than **280 of 2,402 accounts**.
>
> On `decisions/0041` §4's own stated criterion — *"if the three outcome shares are insensitive:
> delete the threshold"* — **the condition is met.**
>
> **Two things the Human Lead should weigh against simply deleting it, both from this same test:**
>
> 1. **Deleting the threshold does not remove the free parameter; it relocates the judgement.**
>    §4's two parameter-free readings differ by **0.67 pp** on Continued — twenty times the
>    threshold's whole interval. The gate closes with no free parameter only if the ruling also
>    says **which** parameter-free rule is meant.
> 2. **The same evidence indicts the whole filter, not only its parameter.** Liveness at 1,293 d
>    moves the shares **0.027 / 0.016 / 0.011 pp** against **no liveness filter at all**. That is
>    a fact about the filter, and it is not this test's question — but it is on the record now
>    and Step 9's liveness bound is built on this filter.

## 7. Judgement calls the spec does not settle

Every one of these was decided by this instance, not by the spec.

1. **Population: waterfall line 4 less D10 = 147,370.** `decisions/0040` §2 and `0038` §2.1
   require derivation and application populations to be identical, and this is the population the
   threshold under test was derived on. **What Step 8 would do differently:** Step 8's analysis
   population is **196,654** (`0041` §3), a strict superset including waterfall lines above
   152,126 — **which carry contaminated `T0`, and both `τ1` and `τ2` are built from `T0`**, so
   every outcome state computed there runs off a contaminated clock. **The absolute shares in §3
   will move at Step 8.** The *sensitivity verdict* is a statement about the flatness of a curve,
   and the curve is flat because the exclusion sets are 0.61–0.87% of the population — a property
   that survives enlarging the denominator, and if anything strengthens.
2. **Parameter-free rule computed under both readings, neither adopted.** §4. Reconciling a spec
   contradiction silently is what the dual-run discipline exists to prevent.
3. **Threshold comparator is `gap ≥ T`**, so a gap exactly equal to `T` is not live. Carried from
   the a4 derivation, where the ceiling ruling (`0025`) is justified by precisely this comparator.
   It does not bind: at T = 787 the strict-inequality reading gives the identical 1,707.
4. **Confidence intervals were computed although `0041` §4 asks only for shares and deltas** —
   "insensitive" is a claim about size and needs a yardstick. Account-clustered, B = 4,000, three
   alternate seeds, in direct response to Red Team's criticism of the 300-replicate interval
   (`0040` §6). **The verdict rests on the point deltas, which are bootstrap-free.**
5. **Shares computed on pairs; excluded pairs dropped, not bounded.** Liveness is a pair-level
   filter so the excluded set is a set of user-show pairs. **Step 9 requires a floor-and-ceiling
   bound on that set and this diagnostic does not discharge it.** A bound would widen the reported
   range at every setting; it would not change the ranking or the flatness.
6. **Sweep range 30–4,000 d on a 5-day grid.** Chosen to run past the point where the gap test
   excludes nothing at all. Context only.
7. **`L2 = 1` filter not applied as a separate step** — asserted a measured no-op (§1).
8. **D11 applied to S2 records** and its bite reported rather than assumed inert (§2).

## 8. What this test does not answer

- **Whether the parameter-free rule is right.** It shows only that the threshold's *value* does
  not change the shares — an argument against publishing a free parameter, not an argument for
  any particular replacement.
- **Whether liveness is warranted at all.** §6 note 2 raises it; deciding it is not this test's
  remit.
- **The derive/apply mismatch.** `0041` §3 records it as **recorded, not repaired**: 1,293 d
  applied to Step 8's 196,654 delivers **1.4418% against a stated 1%**. It goes to Step 14.
- **Anything downstream.** The 91-day arm, Channel A vs Channel B, the segment cut, the
  abandonment distribution, the S3-without-S2 bound (D4), the split-artifact bound (D9) and the
  liveness bound are Steps 9 through 13. **None has run.**

---

**Files.** Figure `artifacts/step7-sensitivity-a.png`; machine-readable
`artifacts/step7-sensitivity-a.json`; intermediates and row-level detail
`processed/step7/sens_a/` (never leaves this machine); scripts `src/step7_sens_a_pop.py`,
`step7_sens_a_outcomes.py`, `step7_sens_a_apply.py`, `step7_sens_a_boot.py`,
`step7_sens_a_fig.py`, `step7_sens_a_check.py`, `step7_sens_a_emit.py`.

**Zero API calls. Nothing is adopted.**
