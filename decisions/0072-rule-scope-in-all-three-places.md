# Decision 0072 — ruling 2's evidence scope reaches Step 7's `THE RULE` block; Step 8 launches

| | |
| :--- | :--- |
| **Decision** | **`0070`'s ruling 2 is added to `task-sheet.md` Step 7's `THE RULE` block**, so the silence test's evidence scope now lives in **all three places the rule is written down** rather than two. **Step 8 launches as a dual pair.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `0071` §3 named this as the last open gap |
| **Status** | Closed. **Step 8 is LAUNCHED — a gate, and it produces and stops.** |

---

## 1. The gap, and why one sentence in one more place mattered

**The rule is written down in three places:** `task-sheet.md` Step 7's `THE RULE` block, both
`data-scientist` files, and — as the rule Step 8 applies — `task-sheet.md` Step 8 and the
`analytics-engineer` pair.

**Ruling 2 reached the second and third and not the first.** `0071` §3 named it rather than closing it
quietly.

**Why it was not cosmetic: `STEP 13 READS THIS BLOCK`** when it re-runs the rule across **eight `W`
arms**. **An asymmetry between two written copies of one rule is exactly what produced the original
792/791 divergence** — one arm applied the `τ_pull` restriction, the other did not, and neither was
wrong against the text it read.

**Added, with the ground and the measurement:** D11 makes `τ_pull` a global frozen cutoff and the
silence test is a computation; **exclusions are 703 on APPLY and 99 on DERIV either way**, so the
restriction is **inert on the exclusion set and bites on the robustness tail.** **The strict reading of
"after `τ1`" is stated in the same block**, since it had the same one-of-three problem.

## 2. Step 8, launched

**Dual pair, namespaces assigned explicitly in the prompt — `a` and `b`** — because `0036` recorded a
collision when instances were left to infer their own, and `0035` had by then made the definition files
byte-identical by design.

**Both instances are pointed at `task-sheet.md` Step 8 itself. Neither prompt paraphrases the step.**
`CLAUDE.md`: *"Both instances receive the same written spec from a file. Never describe the task twice
in your own words: a difference in output would then prove nothing."* **No spec file was written for
this launch, deliberately — one would have been a second definition of the step**, which is the defect
rulings 1 and 7 exist to prevent, committed at the moment of launching them.

**Step 8 is a GATE.** Each instance produces its deliverables and **stops**. **Neither adopts its own
proposal, neither begins Step 8b or Step 9, and approval is the Human Lead's alone.**

## 3. Scope

- **`task-sheet.md` Step 7 only.** The other four surfaces already carried ruling 2 from `0070` and
  `0071`; **checked, not assumed.**
- **No figure moves.** The scope was measured inert at `0070` §2.
- **Zero API calls in this entry.** Step 8 itself runs on cached data.
