# Decision 0070 — eight Step 8 rulings, and the invariant finding routed to Step 14

| | |
| :--- | :--- |
| **Decision** | **All eight `0068` §2b items ruled and propagated at the point of use.** Step 8 emits **both populations** and the **D4 count**; the silence test is restricted to records **before `τ_pull`**; discovery channel becomes **two booleans**; `action` becomes **per-pair counts by type**; D2 splits **three ways**; the drop denominator is **position 5** with post-liveness alongside; and **the filter order is KEPT while the published percentage moves — 10.3% → 10.5%.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 read-back; `0068` §2b listed all eight as needing a ruling |
| **Status** | Closed. **Step 8 has not launched.** |

---

## 1. The eight

| # | Ruling | The reason that decides it |
| :-- | :--- | :--- |
| **1** | **Step 8 produces BOTH populations** — APPLY 196,654 and DERIV 147,370 | Step 9 bounds both and 8b reserves fields for both, so **APPLY alone forces something downstream to rebuild DERIV — a second definition of one population, the defect this study has hit most often** (`0058`, `0061`, `0062`). **Instance B already rebuilt it to the row from Step 8's own inputs** |
| **2** | **The silence test's evidence is restricted to records dated before `τ_pull`** | **Applying an existing ruling consistently, not a new one.** **D11, approved at the Step 1 gate, makes `τ_pull` a global frozen cutoff and discards records at or after it from EVERY computation** — and the silence test is a computation. **The unstated version produced the 792/791 split at Step 7** |
| **3** | **Discovery channel is two boolean columns** | **324 users are in both**, and Step 11 tests whether discovery method biased the pool, so one value **drops the overlap or assigns it arbitrarily**. Two flags let Step 11 cut on either channel or on the overlap |
| **4** | **`action` is not row-level — emit per-pair counts by action type** | It is record-level and the row is a pair. **Step 1 already ruled check-ins count as watching alongside `scrobble` and `watch`, because `action` is a property of the LOGGING CLIENT rather than of the viewing** — so it is **not an outcome variable.** Counts serve Step 13 without asserting one action per pair |
| **5** | **D2's `max()` split is three categories** — finale binds, S1 completion binds, both bind | **168 pairs have both terms binding and the binary split has nowhere to put them.** **A tie is its own category, not a tiebreak** |
| **6** | **Drop denominator is position 5 = 33,373**, post-liveness **32,769** alongside | The drop count is a property of the filter, so it measures against **what entered it**. **The difference is exactly the 604 never-started liveness exclusions and is itself informative** |
| **7** | **Emit the D4 count** | Step 9 must bound it and 8b reserves a slot, so omitting it **forces Step 9 to compute it — a second definition again.** Step 8 holds the episode-level evidence; Step 9 does not |
| **8** | **Keep the mandated filter order; restate the figure as 10.5%** | The order was set at `0029` on the stated ground that **censoring is objective and independent of behaviour while contamination is not**, and **the 10.3% predates it.** **Changing a filter order to preserve a published percentage is backwards** |

## 2. Ruling 2 measured before ruling — it does not disturb the approved gate

**Checked rather than assumed, because Step 7 is an approved gate and this ruling touches its rule:**
restricting the silence test's evidence to `< τ_pull` leaves **exclusions at 703 on APPLY and 99 on
DERIV, unchanged.** No insertion instant exceeds the clamp at **2026-08-10T20:48Z**, and D10 already
forces `τ1 ≤ τ_pull − 91 d`, so the restriction is **inert on the exclusion set**. **It bites on the
robustness tail, which is where the 792/791 divergence lived.**

## 3. Ruling 8's arithmetic, since it moves a published number

`0033`'s **97.6 / 98.0 / 97.5 / 96.0** and **89.7%** for 2023–2025 at `W = 213` were computed on the
**position-3** output (220,107). **The mandated order censors the position-4 output (201,900)**, giving
**97.40 / 97.8 / 97.4 / 95.9** and **89.5%** — and **the 10.3% cohort loss becomes 10.5%.** Measured by
instance B, read-only.

**Corrected in three places**, including **Step 14's cohort-asymmetry bullet**, which carried the 10.3%
independently of Step 8 and would otherwise have contradicted it.

## 4. The invariant finding, routed to Step 14

~~**Four of Step 8's six assertions cannot fail on any data**~~ ***AMENDED (`0076`): FIVE of six, and ZERO pure data checks*** — `0074` specified the `p` invariant and **mislabelled it DATA CHECK**, and both Step 8 instances proved it a code check. **A report stating that all invariants
passed overstates what was verified unless it names which ones could have failed** — and until `0076` added two, **none of them could.** The outcome
partition, the monotone filter counts, distinct-episodes-vs-season-length and `A ⊆ A_H` are **code
checks**. The clock-start check is a code check by construction and a real cross-check **only because
the S1 completion date must be recomputed independently.** The 703 expectation is **not an invariant**
but a population reconciliation.

**An unlabelled code check reads as evidence FOR THE RULE when it is only evidence that the code
computed what it was told to** — and this study's invariant set is four-sixths of that.

## 5. Which surfaces each reached, and which it deliberately did not

**REACHED — all eight, identically:** `task-sheet.md` Step 8, `.claude/agents/analytics-engineer.md`,
`.claude/agents/analytics-engineer-b.md`. **Pair verified byte-identical apart from `name:`.**
**Ruling 8 additionally reached `task-sheet.md` Step 14**, and **the invariant finding reached Step 14
only**, which is where it belongs.

**DELIBERATELY NOT REACHED, and this is the part to read:**

| Surface | Why not | **What still needs a pass** |
| :--- | :--- | :--- |
| **both `data-scientist` files** | This ruling was scoped to `task-sheet.md` and the `analytics-engineer` pair | **Rulings 1 and 7 change what Step 9 RECEIVES.** Step 9 must no longer rebuild DERIV or compute D4, because Step 8 now emits both — **and neither `data-scientist` file has been told.** **Left undone, Step 9 builds the second definition rulings 1 and 7 exist to prevent** |
| **`task-sheet.md` Step 7 and both `data-scientist` files** | same scope | **Ruling 2 states the silence test's evidence scope**, and the rule statement lives in Step 7 and in the `data-scientist` pair. **Measured inert on the exclusion counts, so nothing published moves — but Step 13 re-runs the rule at eight arms and the scope is unstated there** |
| **`artifacts/`** | **checked, not assumed.** Every `10.3%` and `97.6%` occurrence is in a **completed deliverable that was correct for the order it used**, or in the read-back that found the discrepancy | none |
| **`.claude/agent-memory/second-brain/`** | **checked, not assumed** — zero occurrences of either figure | none |

**The two omissions above are named rather than left to be discovered.** They are the same shape as the
covering qualifier, which went six entries reaching no agent file, and as `0064`, which approved a gate
and reached none.

## 6. Scope

- **Eight rulings, one Step 14 routing, one published percentage corrected.**
- **Zero API calls**, including the ruling-2 check.
- **Step 8 has not launched.**
