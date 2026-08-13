# Decision 0041 — The reference set is the extended set, provisionally; no threshold is approved until the Step 9 sensitivity test runs

| | |
| :--- | :--- |
| **Decision** | **Reference set: the EXTENDED set** — measured-gap pairs plus open-ended entered as `+∞` — **provisional.** **Neither 632 nor 1,293 is approved.** The **Step 9 sensitivity test runs first**, at **787 and 2,200 days**, and decides whether the threshold survives at all. The derive/apply mismatch is **recorded, not repaired**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 7 corrected-spec dual run. Both arms proposed 1,293 d and both declined to reconcile the spec contradiction that sets it |
| **Amends** | `task-sheet.md` Step 7 line 266 and Step 14 |
| **Status** | Open. **The Step 7 gate stays open pending the sensitivity test.** |

---

## 1. What the corrected-spec run showed

**Both arms proposed 1,293 days** (raw 1292.0284) and agreed on every structural figure: post-D10
population **147,370**; classes **128,467 / 751 / 18,152 live**; total not live **1,282**, down from
23,772; realised rate **0.9921%**; inertness **41.42% / 58.58%**; bootstrap **B = 2,000**.

**One divergence, and it is Monte Carlo noise:** the clustered interval's lower endpoint, **787 (A)**
against **790 (B)**, inside instance A's own measurement that at B = 2,000 the endpoint moves ~7 days
on the seed alone. Both arms carry both figures.

**Instance B confirmed the pre-D10 classes reproduce the frozen run exactly** — 129,630 / 4,246 /
18,250 — so **every change traces to `0040`'s two rulings and not to the pipeline.**

**Why the threshold moved, in B's words:** *the number rose because open-ended gaps now sit inside the
reference set, where they consume 751 of the 1,282-pair quota before the gap test runs.* **Not because
gaps got longer.**

**`0040` §2's predicted 0.685% was wrong and the measured figure is 0.5812%.** The prediction took Red
Team's `894 / 130,524`, which subtracts the 3,352 `τ1`-past-pull pairs — **a subset of what D10 actually
removes.** The conclusion holds; the arithmetic was loose.

## 2. Reference set: the extended set, provisionally

**`task-sheet.md` line 266 still carried the suspended `0039` §5 restriction verbatim** — *"the
reference set is the 129,630 measured-gap pairs; open-ended gaps cannot be treated as infinite"* —
**reasoning opposite to `0040` §2**, which is what makes the percentile finite. Both arms flagged it and
**both declined to reconcile it**, correctly: it is a spec contradiction, not an implementation choice.

**Corrected. An absent successor instant enters the reference as `+∞`.**

**This is a construction ruling, not an exclusion ruling.** An infinite gap fails any finite threshold
on its own, so edge case (i) is not needed to exclude anything — only to define how open-ended enters.
**And that definition alone is what moves the number:**

| Reference composition | Threshold |
| :--- | ---: |
| Measured-gap only | 632 d |
| Intermediate reading | 975 d |
| **Extended set — adopted, provisionally** | **1,293 d** |

**Wider than the sampling interval**, which is why it needed settling before anything could be
approved.

### 2.1 The degeneracy caveat, carried wherever the threshold is

**Above the 99.4188th percentile the extended-set percentile is itself infinite** and the rule
**collapses into edge case (i) alone.** At `W = 108` that is **0.25%** of bootstrap replicates; **at
`W = 213` it is 2.80%.** Both arms measured it. It travels with the threshold in every downstream
statement.

## 3. The derive/apply mismatch is recorded, not repaired

**`0040` closed half of it. The other half is structural and cannot be closed inside Step 7.**

The reference is line 4 less D10 — **147,370**. Step 8 applies liveness at position 6 to the **analysis
population less D10 — 196,654**, a strict superset. **Applying 1,293 d there delivers 1.4418% against a
stated 1%.**

**Instance B is right that it is not repairable here.** Re-deriving on the 201,900 is **forbidden by
`0038` §2** — those lines carry contaminated `T0`, and `τ1` is built from `T0`. Restricting Step 8 to
line 4 is **unauthorised** and would change the analysis population to suit a diagnostic.

**It goes to Step 14 with its measured size: 1.4418% delivered against a stated 1%.** Same defect class
as `0038` §2.1's own 2.28% example, one step milder.

## 4. No threshold is approved. The Step 9 sensitivity test runs first

**Both arms report that Step 7's own numbers give no basis for preferring a published threshold to the
parameter-free rule**, and the evidence is theirs:

- **Across the full clustered interval the exclusion set moves 1,707 → 897 pairs** — **810 pairs,
  0.55pp of the population.** *(Corrected 2026-08-13 by `0042`: 1,701 is the count at 790 d, instance
  B's interval endpoint; at 787 d — instance A's, and the endpoint this entry uses — it is 1,707. The
  two arms' endpoints had been mixed.)*
- **The entire exclusion set comes from 205 accounts of 2,402.**

> **Recompute the headline at 787 days and at 2,200 days**, alongside the point value.
>
> - **If the three outcome shares are insensitive: DELETE the threshold** and adopt the parameter-free
>   rule — ~~**"the account has insertion evidence bracketing `τ1`"**~~ — and **the gate closes with no free
>   parameter.**
>
>   **WORDING WITHDRAWN 2026-08-13 (`0042`).** *"An instant at or before `τ1` and one after it"*
>   **reinstated `0036` §2.3(ii) verbatim** — the rule `0040` §1 had just withdrawn for contradicting
>   approved gate `0021`. **It was drafted here and propagated a second time into the launch
>   instruction**, and both arms caught it. The adopted rule is **PF-LIMIT**: a pair is **not live iff
>   the account shows no insertion instant AFTER `τ1`**. See `0042` §2.
> - **If sensitive: approve 1,293 d with its interval**, and the interval propagates into the headline
>   as a sensitivity range.

**This test is a gate-closing diagnostic for Step 7. It is NOT the Step 9 deliverable**, and its output
must not be cited as a result: **Step 8 has not launched and is an unapproved gate**, so any headline
computed now is provisional in the population it runs on as well as in its status.

## 5. The propagation failure has now happened five times

**A ruling lands in a decision entry and not in the file the agents read.** Each instance was caught
downstream — by an agent or by Red Team — rather than at the point of the edit:

| # | The miss | Caught by |
| :--- | :--- | :--- |
| 1 | Ten decisions propagated to `task-sheet.md`, none to `.claude/agents/` | `second-brain`, `0035` |
| 2 | `0034`'s three Step 10 requirements: in the approved text, in no spec | `second-brain`, `0035` |
| 3 | `0036` applied to the Step 7 bullet body, not its "NOT LAUNCHED — UNRULED" header | instance A |
| 4 | `0039` corrected `0038` §5 and not `task-sheet.md` line 248, plus three superseded figures | Red Team, `0040` |
| 5 | `0040` corrected four task-sheet figures and missed line 266 — **the one that sets the threshold** | both arms |

**The pattern is not carelessness about any one file; it is that the decision entry feels like the
place a ruling lands, and it is not.** `CLAUDE.md` points agents at their definition file first and
`task-sheet.md` second; **neither is `decisions/`.** Recorded as carried-forward item 46 so the
countermeasure is a standing obligation rather than a resolution to be more careful.

## 6. Scope

- **The Step 7 gate stays open.** Nothing is adopted.
- **Step 8 does not launch.**
- **Zero API calls**, here and for the sensitivity test.
