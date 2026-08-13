# Decision 0039 — Step 7 gate approved: the liveness threshold is 632 days, reported with an account-clustered interval of [528, 787]

| | |
| :--- | :--- |
| **Decision** | **APPROVED. The liveness threshold is 632 days**, the 99th percentile of the bracketing-gap distribution on the 152,126, one gap per pair, ceiling per `0025`. **Reported as 632 d with an account-clustered interval of [528, 787], never as a point estimate.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Gate** | **4 of 5.** Step 1 ✓, Step 5 ✓, Step 6 ✓, **Step 7 ✓**, Step 8 outstanding |
| **Also** | Corrects `decisions/0038` §5; records the reference set, the right-censoring refinement |
| **Status** | Closed. **Step 8 is unblocked.** |

---

## 1. The approved rule

> A **user-show pair** counts as **live** if the account has a distinct insertion instant **at or
> before** its own `τ1 = ⟦T0⟧ + W × 24h`, **and** one **after** it, **and** the gap between them is
> **strictly less than 632 days**.

- **Threshold 632 days**, raw 99th percentile 631.8031, ceiling per `0025`.
- **Reference and application population: the 152,126** (waterfall line 4), identical by `0038` §2.1.
- **Weighting: one gap per pair.** **Gap unit: distinct insertion instants**, `0037` §4.
- **Liveness runs on insertion time** (`0021`), reading the stored play-`id` calibration, **never
  refitted**.
- **Liveness is a pair-level filter, anchored at `τ1`** (`0034`). One account can be live for one show
  and dead for another. **Never drop a user wholesale.**
- **Edge cases** (`0036` §2.3): no instant after `τ1`, or none at or before it, is **not live**, each
  counted and reported separately.

**Counts on the 152,126 at `W = 108`:** live **128,354** (84.37%); not live on a measured gap
**1,276**; no instant after `τ1` **4,246**; no instant at or before `τ1` **18,250**. Realised exclusion
rate **0.9843%** of measured-gap pairs.

## 2. The dual run agreed on everything

**Both arms produced identical figures on every published number** — threshold, raw percentile, all
four counts, the realised rate, and all five Step 13 arms with their rates. Both reported every
percentile convention agreeing to the digit.

**That is what the frozen spec bought.** Three runs earlier the arms were four days apart on the gap
unit; two runs earlier 410 days apart on the reference population. Each divergence was a spec
ambiguity, and each was closed by naming the operation rather than describing it.

## 3. The threshold is reported with an interval, not as a point

> **632 days, account-clustered 95% interval [528, 787].**

**The i.i.d. interval is [632, 645] and it overstates precision by roughly twentyfold.** Gaps within an
account are not independent: **34.4% of pairs share their bracketing gap value exactly with another
pair**, and the largest tie group is **298 pairs**. One account's quiet spell is one event, however
many of its pairs it brackets.

**Same treatment as `W`.** `W = 108` is reported with a **±18-day show-clustered** interval for the
same reason. **Neither number may be published bare**, and downstream text must not imply a precision
the clustering does not support. Found by instance B.

## 4. `0038` §5 is corrected

Both arms found it independently. **The original section was wrong twice:**

- **The level was the wrong population's.** 3.45% / 96.55% was measured on the **201,900** line, which
  `0038` §2 had just replaced with the **152,126**. On the frozen population it is **5.37% gap-test and
  94.63% edge cases** at the adopted 99th.
- **The invariance claim is impossible and is withdrawn.** The edge-case count is **constant in the
  percentile** — 22,496, a function of `W` alone — while the gap-test count is `100 − p` of the 129,630
  measured-gap pairs. **The share ranges 36.5% (90th) → 5.37% (99th) → 0.4% (99.9th)**, a 93-fold
  spread, and on the 128,099 line the gap test is the **majority** of exclusions at the 90th.

**The qualitative point stands at the adopted percentile and is what gets published: the threshold is
not doing most of the work.** At the 99th, `0036` §2.3's two edge-case rulings drive roughly nineteen
exclusions in twenty.

## 5. The reference set is the 129,630 measured-gap pairs

**Open-ended gaps cannot be treated as infinite.** They are **3.17%** of the extended set, so a 99th
percentile taken over it **would itself be infinite** and the threshold would not exist. The reference
is therefore the pairs that have a measured bracketing gap, and the edge cases are handled by `0036`
§2.3's rulings rather than by the percentile. Found by instance B.

**This is why the realised rate has two denominators**, and both are reported: 0.9843% of measured-gap
pairs, 15.63% of all pairs.

## 6. The right-censoring refinement

**Roughly 79% of the "no instant after `τ1`" bucket is right-censoring, not silence.** Instance A
measures 3,367 of 4,246 against the sweep end; instance B measures 3,352 against the pull date. The
difference is definitional.

**Only about 880 accounts genuinely went dark** inside the observed span.

**This supersedes `0038` §7's figure**, which instance A showed may have been tautological: testing
`τ1` against the account's *own* last instant is true by the bucket's definition, at 100% by
construction. Measured against an external reference it is ~79%.

**Step 7 derives on an uncensored population**, so this bucket is inflated by pairs D10 removes at Step
8, where `0029` fixes right-censoring at position 5 and liveness at 6.

## 7. What is disclosed and not argued away

- **The quota property** (`0038` §4). The level is set by the exclusion rate, not by any feature of the
  data. Across the 90th–99.9th the threshold moves by a factor of 57 while the realised rate tracks
  `100 − p` exactly. **The data selects which pairs, never how many.**
- **The inertness** (§4 above).
- **The `W`-coupling** (`0038` §6). Refit per arm: **576 / 590 / 632 / 662 / 697 days**, rates
  0.996 / 0.994 / 0.984 / 0.985 / 0.996%. **Freezing 632 across arms delivers 0.834% at `W = 46` and
  1.191% at `W = 213`** — missing its stated rate at every arm but one, in a varying direction.

## 8. Scope and sequence

- **This approval was given before Red Team reviewed the step**, which is **out of sequence** — the
  same order the Step 6 gate ran in. Red Team reviews on its merits regardless, and a hold reopens the
  gate.
- **Zero API calls**, across all three runs of this step.
- **Step 8 is unblocked** but has not launched. It is a gate and a dual pair.
