# Decision 0045 — PF-LIMIT is kept, ALT is rejected, the Step 9 bound is restricted to never-started exclusions, and `0043` is corrected three ways

| | |
| :--- | :--- |
| **Decision** | **PF-LIMIT is KEPT. ALT is REJECTED** — both arms measured its exclusion set at **zero pairs** across every `W` tested. **The Step 9 bound is restricted to PF-LIMIT's never-started exclusions** — **[16.7789%, 17.0355%]** on the application population. **`0043` is corrected three ways.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's Step 7 blocking item 2, evaluated independently by both `data-scientist` arms |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 9, 14); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md` |
| **Status** | Closed. **Step 7 returns to Red Team.** |

---

## 1. ALT is rejected: it fires on nothing

> **ALT: not live iff (no insertion instant after `τ1`) AND (`|A| = 0`).**

**Both arms measured its exclusion set at ZERO pairs** — instance A across 20 values of `W` from 1 to
400, instance B across all eight mandated arms. Neither saw the other's work.

| At `W = 108`, derivation population | Excluded | Never | Continued | Left |
| :--- | ---: | ---: | ---: | ---: |
| **PF-LIMIT — kept** | 751 | **0** | 652 | 99 |
| **ALT — rejected** | **0** | 0 | 0 | 0 |
| *1,293 d — deleted* | *1,282* | *40* | *1,079* | *163* |

**Red Team's "on the order of 40" was read off the deleted 1,293-day rule.** Those 40 arrived entirely
through the measured-gap branch `0042` removed. **Under the approved rule the never-started exclusion
count is zero.**

**Not a knife-edge.** Instance A measured minimum headroom across the 751 — `τ1` minus earliest
canonical S2 timestamp — at **47.5 days**, median 107.4, against a maximum observed post-dating of
**+20.4 days**. The channel that would have to fire for ALT to bite does not reach.

## 2. The obstacle was not real, and that is recorded separately from the rejection

**Red Team flagged its own alternative as possibly unimplementable inside `0029`'s filter order —
liveness at position 6, outcome assignment at 7. Both arms established that it is not an obstacle:**

- **Instance A:** `|A|` and liveness are **row-local predicates on the position-5 output, and row-local
  predicates commute exactly.**
- **Instance B:** `0029` fixed the order because *"the final row set commutes, but the required
  per-filter sample size does not."* **That cannot apply to position 7, because outcome assignment
  removes no rows** — positions 1–6 are filters, **position 7 is an annotation** and contributes no
  waterfall line. The defect `0029` exists to prevent is unreachable through 6-versus-7.
- Both note `0029`'s recorded rationale is about **censoring before liveness**, which ALT satisfies
  unchanged.

**So ALT was rejected on effect, not on feasibility**, and the distinction matters: **the ordering is
not a barrier to any future outcome-conditional filter**, and instance B notes the question recurs at
Step 13. What ALT would have cost is a **defence obligation for no effect** — a stated rule firing on
nothing still has to be justified, and Red Team's item 2 (the not-live branch's missing warrant) would
have remained open with it.

**Both arms argued against their own recommendation**, which is why this ruling has the evidence it
needs. Instance A recommended adopting ALT and named that it *"empties the unwarranted branch without
warranting it"*, makes its DOWN direction true by construction, and **zeroes the per-arm column `0044`
added to make the `W`-coupling visible**. Instance B recommended Option C and named that **Red Team's
own principle selects ALT-BROAD, not ALT** — started-and-left's exit is equally inferred from absence —
**and ALT-BROAD's sign is UP.**

## 3. Option C: the bound is restricted to never-started exclusions

> **Compute the Step 9 liveness bound only over the liveness exclusions scored NEVER STARTED.**
> **On the application population: [16.7789%, 17.0355%], width 0.257 pp.**

**Why the old form was not a bound.** It treated every excluded pair as a decliner. But **all 751
derivation-population exclusions have positive in-window S2 evidence and 652 are confirmed
continuers.** Treating a confirmed continuer as a decliner is not conservative — it is arithmetic on a
set chosen for a reason unrelated to the uncertainty being bounded, **and it put the ceiling outside
the feasible set**: 6.7151% against an unfiltered 6.2055%, which instance A sized at **0.62× the
clustered sampling width of the share it bounds.**

**Restricting to the never-started exclusions makes both endpoints attainable** — the excluded set is a
subset of never-started, so the ceiling equals the unfiltered share as an identity — **and lands within
0.001 pp of the width ALT would have produced**, while touching no rule, population, filter order or
agent file. Instance B's construction; `0043` §1.2 had already gestured at it.

## 4. `0043` is corrected three ways

**`0043` was written to fix a sign error and introduced three of its own.** Both arms found them.

### 4.1 The sign is population-scoped, and the published direction is the other one

| Population | Unfiltered | PF-LIMIT | Direction |
| :--- | ---: | ---: | :--- |
| **Derivation** — line 4 less D10, 147,370 | 6.2055% | 6.2373% | **UP 0.032 pp** |
| **Application** — line 1 less D10, **196,654, what Step 8 filters** | 16.9704% | 16.7789% | **DOWN 0.192 pp** |

**Mechanism: line 4 requires S2 evidence.** The **604** never-started pairs with **no S2 record
anywhere** exist only on the application population, and excluding them is what pulls the share down
there. **`0043` published the derivation-population direction as though it were the study's.** Instance
B: *"same error class `0043` itself catalogues."*

**Both directions are now carried, with the mechanism**, and the application direction is the published
one.

### 4.2 The "~40 never-started exclusions" remedy is unexecutable and is withdrawn

`0043` §1.2 said to compute the bound *"on the ~40 never-started exclusions instead."* **That count is
zero** under the approved rule; the ~40 belonged to the deleted rule. Instance A: *"the seventh
instance, inside the entry correcting the sixth."* **Replaced by Option C**, which is well defined
because the application population does contain 604 such pairs.

### 4.3 "Six in seven have positive S2 evidence" merged two claims and understated one

**Seven in seven of the 751 have positive S2 evidence. Six in seven — 652 — are confirmed continuers.**

## 5. The 751/1,355 discrepancy is pre-empted, not left to be discovered

**`task-sheet.md` recorded "751 pairs from 166 accounts" without saying which population.** Step 8
applies the same rule to **196,654** and will produce **1,355 from 276**. Against the old spec **that
correct result would have read as a divergence** — and Step 8 is a dual pair whose entire instrument is
the diff.

**Both counts are now stated in all five files, with the reason**, and the `analytics-engineer`
definitions say explicitly that **reporting 1,355 is correct.**

## 6. What remains open

**Red Team's item 2 — the not-live branch has no stated warrant — is NOT closed by this entry.** `0021`
licenses *"insertion after `τ1` → live"*, a sufficient condition, not the biconditional PF-LIMIT
adopts. Rejecting ALT does not supply the missing argument; instance A was explicit that ALT would not
have supplied it either.

**Step 7 returns to Red Team.** Step 8 does not launch.

## 7. Scope

- **No rule, population or filter order changes.** One bound is narrowed, one alternative rejected,
  three published claims corrected, one count disambiguated.
- **Zero API calls.**
