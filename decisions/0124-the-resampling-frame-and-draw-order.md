# Decision 0124 — the resampling frame and the draw order are fixed

| | |
| :--- | :--- |
| **Decision** | ***THE FRAME IS EVERY ACCOUNT WITH AT LEAST ONE PAIR IN THE POSITION-4 OUTPUT, BUILT ONCE, AND DRAWN FOR EVERY QUANTITY REGARDLESS OF HOW MUCH IT CONTRIBUTES. THE DRAW ORDER IS ONE RNG SEEDED ONCE PER FILE, ITS STREAM CONSUMED CONTINUOUSLY, WITH EVERY QUANTITY EVALUATED AGAINST THE SAME REPLICATE SET. NOT RE-SEEDED PER GROUP.*** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-23 |
| **Amends** | `0103` and `0118`, which fixed `B`, the seed, the unit and the statistic **and left these two open** |
| **Occasioned by** | `0123`'s cross-arm diff: **24 CI endpoints differing under one fixed seed** |
| **Status** | **FILED and PROPAGATED.** ***One arm must rerun; the cost is stated in §5 and the rerun is NOT authorised by this entry.*** |

---

## 1. The ruling

**The frame:** every account with **at least one pair in the position-4 output**, built **once**, and **drawn for every quantity regardless of how much it contributes.**

**The draw order:** **one RNG, seeded once per file**, its stream **consumed continuously**, with **every quantity evaluated against the same replicate set.** ***Not re-seeded per group.***

## 2. Why the frame is not the contributing subset

***Accounts the censoring rule excludes are part of the population the uncertainty is ABOUT.*** **Drawing only the contributing subset conditions the variance on the censoring outcome and treats survivorship as fixed.**

**The censoring is not a fact about the world; it is a fact about the observation window.** An account whose every pair fell outside `max(W, 91) + H` **could have contributed** and did not, and **the interval is supposed to express how much the answer would move if the sample had come out differently** — which includes coming out with that account inside.

**Measured, so the size of the thing being fixed is on the record:** at `W = 108`, **59 accounts on APPLY and 79 on DERIV are drawn and contribute zero** — 2.38% and 3.18% of the frame. **58 contribute zero at all six arm-population settings.** All 59 of the APPLY zero-contributors **hold position-4 pairs, every one removed by D10**: 1,068 pairs, 1,043 by the `max(W, 91)` term and 25 by `+H`.

## 3. Why the stream is shared rather than restarted

***BOTH ARMS ALREADY SOLVED THE ORDER-INDEPENDENCE HAZARD*** — that an interval must not depend on the order the intervals happen to be computed in — **by opposite mechanisms: one shared stream across all columns, or one identical stream restarted per group.** **Neither was wrong and the spec named neither.**

***THE RULING TAKES THE SHARED STREAM, because it is the design that supports a BETWEEN-SETTING movement*** — a difference between two settings is paired at the account level only if both settings are drawn on **the same resampled accounts**, and a per-group restart guarantees that **only within a group.** ***Step 13 is dual and varies `W` across eight arms***, so between-setting differences are exactly what it will need.

**An unfixed draw order also makes the fixed seed decorative:** both arms used `20260818` and drew different replicate sets, **which is the failure fixing the seed exists to prevent.**

## 4. Two findings that survive the ruling

***(1) A FRAME THAT IS ARM-INDEPENDENT IN MEMBERSHIP IS NOT ARM-INDEPENDENT IN SUPPORT.*** `keep_d10`
contains `max(W, 91)`, **so the contributing subset moves with `W` even when the drawn frame does not.**
Measured: membership **2,481 at every arm**, while the contributing subset is **2,422 / 2,423 / 2,422**
on APPLY and **2,402 / 2,407 / 2,402** on DERIV across three arms.
***ANY FIELD DECLARING THE FRAME ARM-INDEPENDENT MUST SAY IT DESCRIBES THE DRAW AND NOT THE SUPPORT.***
*"The declared field describes the draw; it does not describe the support."*

***(2) AN APPLY-MINUS-DERIV DELTA CANNOT BE PAIRED AT THE ACCOUNT LEVEL under any design where the two
populations have different frames.*** Different `n_acc` means a different-shaped weight matrix, and
**the same replicate index does not denote the same resampled accounts.** ***NOTHING PUBLISHED CROSSES
THAT LINE.*** **Recorded as a CONSTRAINT ON STEP 13**, which is dual and nests per arm.

## 5. Who must rerun, and what it costs — ***the rerun is NOT authorised here***

**Assessed against each arm's committed source. Stated as an assessment, not as an arm's attestation.**

| | frame | draw order | obliged to rerun |
| :--- | :--- | :--- | :--- |
| **arm `a`** | position-4 accounts, built once, 2,481, drawn for every quantity | one RNG seeded once per file, continuous stream, 48 columns against one replicate set | ***NO*** |
| **arm `b`** | **per mask**, 2,422 APPLY / 2,402 DERIV | **re-seeded per group**, one `multinomial` call per group | ***YES*** |

**What moves in a rerun: the CI endpoints only.** Every point estimate, numerator, denominator, bound,
width, ceiling, sum and pair count is **not bootstrap-dependent** and does not move.
**Scope: 12 level intervals and 12 paired movements — 48 endpoints — across 2 arm settings × 2
populations × 3 states.**

***THE COST THAT IS NOT THE COMPUTE.*** **A rerun supersedes figures inside `step9-headline-corrected-2026-08-21-b.json`,
which is itself the correction of a superseded file** (`0123`). **So it creates a SECOND supersession
layer**: the stamped originals, the corrected emission whose CI endpoints then become superseded, and a
further emission. ***A reader would face three generations of one arm's premiere figures.*** **That is a
question about publication shape, not about the bootstrap, and it is the Human Lead's.**

**Also to be re-established after any rerun:** arm `b`'s own pairing evidence — it verified all 12
movements paired **by reproducing published endpoints from the recorded weights**, and those weights
change.

## 6. Scope

- ***The `$defs/ci` percent-vs-pp typing is NOT ruled here.*** Still open, still the Human Lead's.
- **The Step 13b merge input contract is not ruled here.**
- **`0123`'s preserved sensitivity measurement is what this ruling makes unreproducible**, which is why
  it was preserved before the ruling rather than after.
- **Zero API calls. Step 10 not begun. No rerun performed.**
