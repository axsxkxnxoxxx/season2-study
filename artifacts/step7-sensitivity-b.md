# Step 7 — liveness threshold sensitivity test (instance `b`)

**Required by `decisions/0041` §4. Proposed, not adopted. The Human Lead rules on whether the
threshold survives.**

---

## READ THIS FIRST — what these numbers are, and what they are not

**This is a GATE-CLOSING DIAGNOSTIC FOR STEP 7. It is NOT the Step 9 deliverable, and nothing below
is a study result.**

**Step 8 has not launched and is an unapproved gate — gate 4 of 5.** The analysis table these shares
would properly be computed on does not exist. So every share in this document is **provisional in the
population it runs on as well as in its status**, and none of them is the headline.

**The population caveat is specific and it matters.** `0041` §3 records that Step 8 applies liveness at
filter position 6 to the **analysis population less D10 — 196,654 pairs**. This test runs on the
**liveness derivation population, 147,370**, a strict subset. The *levels* below would differ on Step
8's population. **What this test reports is the MOVEMENT between settings, not the level.**

Do not quote 6.23% as a never-started share. Quote, if anything, that the threshold moves it by
**0.026 percentage points across its whole clustered interval**.

---

## 1. The question, and the answer

> **Is the outcome split sensitive to the liveness threshold across its account-clustered interval?**

**No. It is insensitive, and not marginally so.**

Across **787 d**, **1,293 d** and **2,200 d**, the largest movement in any of the three outcome shares
is **0.0323 percentage points**. Adding the parameter-free rule in its `0021`-consistent reading widens
that to **0.0386 pp**.

For scale: the account-clustered 95% interval on the never-started share at 1,293 d is **0.771 pp
wide** — **23.9 times** the entire range the threshold moves it. **The threshold's whole interval is
buried inside the sampling noise of a single setting.**

There is **one exception**, and it is not the threshold. See §5.

---

## 2. Results — three shares at four settings

Population: **147,370 pairs** (waterfall line 4, 152,126, less D10 right-censoring at `W = 108`).
`W = 108`, `H = 91`, `τ1 = ⟦T0⟧ + 108 d`, `τ2 = ⟦T0⟧ + 199 d`, outcomes per Step 1 §7 as amended by
`0034`. Everything except the liveness setting is held fixed.

| Setting | Live pairs | Never started | Continued | Started and left | Excluded |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **787 d** — interval low | 145,663 | **6.2109%** | **82.3812%** | **11.4078%** | 1,707 |
| **1,293 d** — point value | 146,088 | **6.2325%** | **82.3497%** | **11.4178%** | 1,282 |
| **2,200 d** — interval high | 146,473 | **6.2373%** | **82.3490%** | **11.4137%** | 897 |
| **Parameter-free** (`0021`-consistent) | 146,619 | **6.2373%** | **82.3427%** | **11.4201%** | 751 |
| *(no liveness filter at all)* | *147,370* | *6.2055%* | *82.3655%* | *11.4291%* | *0* |
| **Parameter-free** (literal `0041` wording) | 128,467 | **6.3043%** | **81.6832%** | **12.0124%** | 18,903 |

Counts behind the shares:

| Setting | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 d | 9,047 | 119,999 | 16,617 |
| 1,293 d | 9,105 | 120,303 | 16,680 |
| 2,200 d | 9,136 | 120,619 | 16,718 |
| Parameter-free (`0021`) | 9,145 | 120,730 | 16,744 |
| Parameter-free (literal) | 8,099 | 104,936 | 15,432 |

**Continued is a 199-day statement and never-started is a 108-day statement.** They are not measured
alike, and that must travel with any reporting of this split (Step 1 §7).

### 95% account-clustered intervals

B = 2,000, resampling the 2,402 accounts with replacement, percentile method, seed 20260813.

| Setting | Never started | Continued | Started and left |
| :--- | :--- | :--- | :--- |
| 787 d | [5.834, 6.610] | [81.748, 82.991] | [10.916, 11.896] |
| 1,293 d | [5.863, 6.634] | [81.716, 82.958] | [10.921, 11.908] |
| 2,200 d | [5.870, 6.636] | [81.717, 82.955] | [10.921, 11.897] |
| Parameter-free (`0021`) | [5.870, 6.635] | [81.711, 82.950] | [10.930, 11.906] |
| Parameter-free (literal) | [5.913, 6.738] | [81.003, 82.340] | [11.466, 12.551] |

**The four intervals in the first four rows are visually indistinguishable.** That is the finding.

---

## 3. Deltas, in percentage points

Paired — the same account resample is used for every setting within a bootstrap replicate.

| Comparison | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 → 1,293 | **+0.0216** | **−0.0316** | **+0.0099** |
| 1,293 → 2,200 | **+0.0048** | **−0.0007** | **−0.0041** |
| **787 → 2,200 (whole interval)** | **+0.0264** | **−0.0323** | **+0.0059** |
| 1,293 → parameter-free (`0021`) | +0.0047 | −0.0070 | +0.0023 |
| 1,293 → parameter-free (literal) | +0.0718 | **−0.6664** | **+0.5946** |

**Largest absolute delta across the clustered interval: 0.0323 pp.**
**Largest including the `0021`-consistent parameter-free rule: 0.0386 pp.**

Two of the interval deltas are distinguishable from zero at B = 2,000 — 787 → 2,200 on never-started,
paired CI `[+0.0085, +0.0467]`, and on Continued, `[−0.0648, −0.0006]`. **They are detectable and they
are trivial**, which is the point: with 147,370 pairs a paired comparison can resolve a movement three
orders of magnitude smaller than anything that could change a published conclusion.

**Every delta across the interval is smaller than the third significant figure of every share.** None
of them would change a rounded published number, a chart, or a sentence.

---

## 4. Why it is insensitive — four mechanisms, all measured

1. **The exclusion set is tiny and it barely moves.** Across the whole interval it goes **1,707 → 897
   pairs — a swing of 810, or 0.55% of the population.** A set that size cannot move a share built on
   147,370 by more than hundredths of a point. This is Red Team's point in `0040` §6, now measured on
   the outcome shares rather than on the pair count.

2. **The pairs the threshold excludes are not the never-started ones.** At 1,293 d, of 1,282 excluded
   pairs **1,079 are Continued, 163 Started-and-left, and 40 Never started.** The marginal exclusions
   as the threshold loosens are overwhelmingly Continued pairs, so removing or restoring them
   reweights the split almost not at all. **The filter is not selecting on the outcome it was built
   to protect.**

3. **The quota property bites exactly as disclosed.** The threshold is a percentile *of the
   distribution the test applies to*, so its level is set by the exclusion rate rather than by any
   feature of the data. Moving the percentile moves a quota, and **the quota is under 1.2% at every
   setting tested.**

4. **The open-ended edge case dominates at every setting and is invariant in the threshold.** 751
   exclusions come from pairs with no insertion instant after `τ1`. At **2,200 d those 751 are 84% of
   all exclusions and the measured-gap test contributes 146.** The threshold is doing almost none of
   the work at the top of its own interval.

| Setting | Excluded by the measured-gap test | Excluded by the open-ended edge case |
| :--- | ---: | ---: |
| 787 d | 956 | 751 |
| 1,293 d | 531 | 751 |
| 2,200 d | 146 | 751 |
| Parameter-free (`0021`) | 0 | 751 |

**`0041` §2.1's degeneracy caveat is visible here as a limit.** Above the 99.4188th percentile the
extended-set percentile is itself infinite and the rule collapses into the open-ended case alone —
which *is* the parameter-free column. **2,200 d is already close enough to that limit that
parameter-free and 2,200 d agree to within 0.001 pp on every share.**

---

## 5. The one exception, and it is not the threshold

**The LITERAL reading of the parameter-free rule moves the split by up to 0.698 pp** — twenty times
the threshold's entire range, and the only material movement anywhere in this test.

`0041` §4 words the parameter-free rule as *"the account has insertion evidence bracketing `τ1`"*, and
the task restates it as *"a distinct insertion instant at or before `τ1` **and** one after it."* **Read
literally, that scores DEAD the 18,152 pairs with no instant at or before `τ1`** — 12.3% of the
population.

**That is precisely the withdrawn edge case (ii).** `0040` §1 withdrew it for contradicting `0021`,
an approved gate: *any record inserted after the window closed proves the account was alive, whatever
date it claims.*

**So there are two parameter-free rules, and `decisions/` points both ways on 18,152 pairs.**

| Reading | Excluded | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: | ---: |
| `0021`-consistent — not live only if open-ended | 751 | 6.2373% | 82.3427% | 11.4201% |
| Literal `0041` §4 wording — also not live if no pre-`τ1` instant | 18,903 | 6.3043% | 81.6832% | 12.0124% |

**Reported as a defect, per the standing instruction that `decisions/` is authoritative and a
disagreement between rulings is a defect to report rather than reconcile.** Instance `b` does not
reconcile it.

**The consequence for the gate is direct.** If the Human Lead deletes the threshold and adopts the
parameter-free rule, **which reading is adopted matters roughly twenty times more than the threshold
ever did.** The `0021`-consistent reading is the one that follows from an approved gate; the literal
wording reinstates a withdrawn edge case. This is now the largest live choice in Step 7.

---

## 6. Population, asserted

| Waterfall line | Expected | Measured |
| :--- | ---: | ---: |
| 1 | 201,900 | 201,900 |
| 2 | 178,165 | 178,165 |
| 3 | 155,131 | 155,131 |
| **4 — the reference (`0038` §2)** | **152,126** | **152,126** |
| 5 | 128,099 | 128,099 |

**D10 right-censoring** — retain iff `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, `H = 91`,
`τ_pull = 2026-08-11T00:00:00Z`, bound 199 days at `W = 108`:

**152,126 − 4,756 = `147,370` — the post-D10 count this test runs on.**
**2,402 accounts, 1,138 shows.**

Liveness classes at `W = 108`: measured gap **128,467**; open-ended **751**; no instant at or before
`τ1` **18,152**. **All four figures reproduce `0041` §1 exactly**, and the row identity of this
population against `processed/step7/b4/bracket.npz` is asserted in code, not assumed.

**D11** — records at or after `τ_pull` discarded: 80 distinct-episode records, 31 pairs touched.
**The three-state partition is asserted to sum to the sample**, and `A ⊆ A_H` is asserted rowwise.

---

## 7. Judgement calls the spec does not settle

| # | Call | Note |
| :--- | :--- | :--- |
| **J1** | **Population = line 4 less D10 = 147,370.** | It is the liveness derivation *and* application population inside Step 7. **Step 8 would settle this differently: `0041` §3 puts liveness on the analysis population less D10, 196,654 — a strict superset — where 1,293 d delivers 1.4418% against a stated 1%.** Whether the insensitivity carries to that population is **not tested here and cannot be**, because Step 8 has not run. |
| **J2** | **Two readings of the parameter-free rule, both reported, neither adopted.** | See §5. The only material movement in the test. Reported as a defect. |
| **J3** | **Outcomes computed once, before any liveness filter; liveness applied as a row mask.** | Liveness cannot change a pair's state, only whether it is counted. This makes the four settings exactly comparable and removes any chance of drift between them. |
| **J4** | **Interval: account-clustered bootstrap, B = 2,000, seed 20260813, percentile method, paired across settings.** | Gaps within an account are not independent — the reason `0039` required a clustered interval. **B and the seed are instance choices the spec does not fix**, and `0040` §6 flagged bootstrap endpoints as the one place the arms did uncrosschecked independent work. |
| **J5** | **`L2 = 1` exclusion is vacuous here.** | **Zero pairs on line 4 sit on an `L2 = 1` show**, so Step 8's filter-position-2 exclusion removes nothing and cannot be a source of divergence. Stated rather than left to be wondered about. |
| **J6** | **`np.interp` clamping of 6,956 records outside the fitted calibration knot range, inherited unchanged.** | The curve is a required input and is **read, not refitted**. The spec does not state how to treat records outside the fitted `rid` range. `0040` §6 named this as a lever that would have changed every downstream number had it been resolved otherwise. **Reported, not repaired.** |
| **J7** | **2,200 d taken as given.** | This instance's own `B = 2,000` clustered interval is not `[787, 2200]`; the endpoints are the Human Lead's and are used verbatim, not re-derived. **The test is more conservative for it** — 2,200 d is wider than anything measured here, and the split still does not move. |
| **J8** | **The degeneracy caveat travels with this test.** | `0041` §2.1. At the limit the rule *is* the parameter-free column, which is why 2,200 d and parameter-free agree to 0.001 pp. |

---

## 8. What this test does not establish

- **It does not establish that these shares are correct.** They are computed on a population Step 8 has
  not defined, at a gate that is not approved.
- **It does not establish that liveness as a whole is inert — only that the THRESHOLD is.** The
  open-ended edge case removes 751 pairs at every setting and no percentile choice touches it.
- **It does not test sensitivity to `W`.** `W` is held at 108 throughout, as instructed. The threshold
  is a **function of `W`** (`0038`), so each Step 13 arm has its own threshold and its own interval.
- **It does not resolve the derive/apply mismatch** recorded in `0041` §3, which goes to Step 14 at its
  measured size.

---

## 9. Files

- `artifacts/step7-sensitivity-b.json` — every count, share, interval and delta in machine form
- `processed/step7/sens_b/` — `pairs.npz`, `outcomes.npz`, `sensitivity.json`, stage logs (row-level,
  never leaves this machine)
- `src/step7_sens_b_1_population.py`, `_2_outcomes.py`, `_3_sensitivity.py`, `_4_deliver.py`

**Zero API calls.** Everything reads cached data and the stored Step 5 calibration curve, which is read
and not refitted.

**Nothing is adopted.**
