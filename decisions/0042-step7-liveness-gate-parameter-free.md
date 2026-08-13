# Decision 0042 — Step 7 gate approved with NO free parameter: a pair is not live iff the account shows no insertion instant after `τ1`

| | |
| :--- | :--- |
| **Decision** | **APPROVED. The threshold is DELETED.** A user-show pair is **not live if and only if the account shows no insertion instant after that pair's `τ1`.** **No numeric parameter.** `0041` §4's parameter-free wording is **withdrawn** and replaced by **PF-LIMIT**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Gate** | **4 of 5 — CLOSED.** Step 1 ✓, Step 5 ✓, Step 6 ✓, **Step 7 ✓**, Step 8 outstanding |
| **Supersedes** | `0039` (suspended), the 632 d and 1,293 d proposals, `0041` §4's wording |
| **Status** | Closed. **Step 8 is unblocked.** |

---

## 1. The approved rule

> **A user-show pair is NOT LIVE if and only if the account shows no insertion instant after that
> pair's `τ1 = ⟦T0⟧ + W × 24h`. Otherwise it is live.**

**There is no threshold and no free parameter.** Everything else stands: insertion time not claimed
`watched_at` (`0021`); the stored calibration curve read and never refitted (`0029`); a **pair-level**
filter anchored at `τ1`, never a user-level drop (`0034`).

**Exclusions on the derivation population — line 4 less D10, 147,370 pairs: 751 pairs from 166
accounts, 0.51%.**

## 2. Why the threshold was deleted

**It was derived three times — 632 d, then 1,293 d — and the headline cannot tell the difference.**

| Setting | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 d | 6.2109% | 82.3812% | 11.4078% |
| 1,293 d | 6.2325% | 82.3497% | 11.4178% |
| 2,200 d | 6.2373% | 82.3490% | 11.4137% |
| **Parameter-free — adopted** | **6.2373%** | **82.3427%** | **11.4201%** |

**Max movement across all four settings: 0.026 / 0.038 / 0.012 pp** — about **3% of the account-clustered
sampling width** (0.78 / 1.25 / 0.99 pp at B = 4,000). **A continuous 30–4,000 day sweep moves nothing
beyond 0.243 pp.** Both arms produced these figures independently and identically to four decimal
places.

**One delta is statistically distinguishable and still immaterial**: the paired clustered CI for
787→2,200 on never-started is **[+0.008, +0.046] pp**, excluding zero, because nested subsets give
near-zero paired variance. **Detectable, not material** — instance A reported both facts rather than
the convenient one.

**The deeper reason is the quota property** (`0038` §4). A percentile of the distribution the test is
applied to sets the level **by the exclusion rate, not by any feature of the data**. There was never a
number to find. **Deleting it removes a parameter that was never identified, at a cost the study can
measure and which is smaller than its own sampling noise.**

## 3. `0041` §4's wording is withdrawn — the error was mine and both arms caught it

`0041` §4 worded the parameter-free rule as *"an instant at or before `τ1` **and** one after it."*

**That reinstated `0036` §2.3(ii) verbatim** — the rule `0040` §1 had withdrawn one entry earlier for
contradicting **approved gate `0021`**, which holds that any record inserted after the window closed
proves the account was alive. **I drafted it in the entry and then propagated it a second time into
the launch instruction**, so both arms received it twice.

**Both arms computed both readings and reconciled neither, which was correct** — a spec contradiction
is not an implementation choice.

| Reading | Excluded | Accounts | vs 1,293 d |
| :--- | ---: | ---: | :--- |
| **PF-LIMIT — adopted** | 751 | 166 | — |
| PF-BRACKET — the literal text | **18,903** | **1,434 of 2,402** | Continued **−0.67 pp**, Started-and-left **+0.59 pp**; paired clustered CIs [−0.88, −0.47] and [+0.45, +0.75], both excluding zero |

**Instance A's verdict is the one that matters and it is on the record:** *"Deleting the threshold does
not close the gate with no free parameter — it relocates the judgement to a choice twenty times more
consequential than the value it replaces."* **That choice is now made explicitly rather than by
wording.**

**Do not reintroduce a pre-`τ1` requirement in any form.** It has been withdrawn twice.

## 4. The filter as a whole is nearly inert, and Step 9's bound rests on it

**Against no liveness filter at all**, the approved rule moves the three shares by **0.027 / 0.016 /
0.011 pp** — smaller than the third significant figure of every share, and roughly **2% of the
clustered sampling width**.

**Step 9's liveness bound is computed on 751 pairs from 166 accounts.** So **the bound is narrow
because the filter is nearly inert, not because the inference is tight**, and Step 14 carries that
statement with its measured size. Instance A raised it unprompted, noting it was not the question it
had been asked.

## 5. The shares are provisional in population, not only in status

**Step 8 has not launched.** It applies liveness at position 6 to the **analysis population less D10 —
196,654** — a strict superset whose extra lines carry **contaminated `T0`**, and **both `τ1` and `τ2`
are built from `T0`**.

**The absolute shares will move at Step 8. The flatness finding will not.** The curve is flat because
the exclusion sets are **0.51–0.87%** of the population, which survives enlarging the denominator —
instance A's defence, and it is the right one. **The sensitivity verdict is about the shape of a curve;
the levels in §2 are not results and must not be quoted as any.**

Carried forward accordingly.

## 6. Corrections to the record

- **`0041` §4's "1,701 → 897" is corrected to "1,707 → 897", 810 pairs.** 1,701 is the count at 790 d —
  instance B's interval endpoint — while the entry's own endpoint is A's 787 d. **The two arms'
  intervals had been mixed.** Six pairs, immaterial to every conclusion, corrected rather than left.
- **`0039` remains suspended**, with its errors marked in place.

## 7. What the three derivations bought

The threshold is deleted, so the work that produced it might look wasted. **It was not.** Deriving it
three times is what established that **it does not matter** — and that finding is only available
because the derivations were done properly enough to be trusted. Along the way the same work exposed
**a rule that contradicted an approved gate on 76.8% of its exclusions**, **a reference distribution
calibrated on one population and applied to another**, **an impossible invariance claim**, and **a
wording that reinstated a withdrawn rule**. None of those would have surfaced from a rule adopted
because it sounded reasonable.

## 8. Scope and sequence

- **This approval was given before Red Team reviewed the step**, as at Step 6 and at the suspended
  `0039`. **Red Team reviews on the merits and a hold reopens the gate.**
- **Zero API calls**, across all five runs of this step.
- **Step 8 is unblocked.** It is a gate and a dual pair, and it has not launched.
