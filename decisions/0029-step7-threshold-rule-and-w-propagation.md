# Decision 0029 — `W = 108` propagated to its consuming steps, Step 7's threshold rule fixed, Step 8's filter order fixed

| | |
| :--- | :--- |
| **Decision** | Four amendments, all before Step 7 launches: **`W = 108` written into Steps 7, 8 and 13** and into both Step 6 artifacts; **Step 7's threshold rule** replaced with a named percentile, a stated gap unit and a stated rounding direction; **Step 8's filter order** fixed; **the gap defined as the interval between consecutive insertion instants.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Steps 7, 8 and 13; `artifacts/step6-window-w-a.md`; `artifacts/step6-window-w-b.md` |
| **Found by** | `second-brain`, on the consistency pass after the Step 6 gate |
| **Open** | The Step 7 percentile is **PROPOSED at the 99th** and is not adopted until the Human Lead rules |
| **Status** | Closed except for the proposed percentile |

---

## 1. `W = 108` was not in either step that consumes it, and the artifacts contradict it

This is the sharpest of the four, and it was not a silence. It was a **contradiction with two different wrong answers**.

| Where a Step 7 or Step 8 instance would look for `W` | What it found |
| :--- | :--- |
| `task-sheet.md` Step 7 | nothing — the rule composes with "clock start plus `W`" |
| `task-sheet.md` Step 8 | nothing — `W` listed among the filters |
| `artifacts/step6-window-w-a.md` | **W = 107** |
| `artifacts/step6-window-w-b.md` | **107.7135** |
| `task-sheet.md` line 411 | `W = 108` — inside **Step 14** |

Both deliverables are correct as instance derivations: the ceiling ruling ([0025](0025-lag-unit-and-ceiling.md)) came at the gate, after they ran. But nothing in either artifact said so.

**Steps 7 and 8 are both dual pairs.** Two instances resolving `W` from two different artifacts would have produced a divergence that reads as an implementation difference — and the diff cannot tell that from a bug. This is the failure mode item 23 exists for, arriving with a twist: not an omission both instances fill the same way, but a **conflict they could fill two different ways.**

**Fixed at both ends.** `W = 108` is now stated in Steps 7, 8 and 13, each naming [0026](0026-step6-window-w-gate.md) as the source and each saying explicitly that the artifacts' 107 and 107.7135 are **not** the adopted value. Both Step 6 artifacts now carry a header recording the gate outcome, the coverage arithmetic, and the instruction **"do not take `W` from this file"** — following the repo's existing practice from the S1-completer diagnostic's supersession note. Everything else in those artifacts stands; only the rendering was superseded.

## 2. Step 7's threshold rule

The prior wording — **"Set the threshold well beyond the normal gap"** — is withdrawn. It named no feature and no number. It is the same defect as Step 6's "the percentile where the curve flattens," and weaker: "flattens" at least named a property of a curve. That wording cost a full dual run and produced two honest answers **61 days apart** ([0024](0024-w-is-the-90th-percentile.md)). Step 7 is also a dual pair deriving a threshold, and [0025](0025-lag-unit-and-ceiling.md) named it as the next candidate in as many words.

Three things are now specified, matching the shape of the Step 6 fix.

### The gap is between consecutive insertion instants, measured continuously

Human Lead: *"liveness runs on insertion time, so the gap is between consecutive insertion instants, not claimed watch dates."*

This follows from the standing insertion-time ruling ([0021](0021-step5-contamination-gate.md)). **If liveness is evidence that the account is alive, the gap between two pieces of that evidence is the gap between when they were written.** A gap computed on claimed `watched_at` would read a 2026 import of a 2015 season as a 2015 event and score a live account dead. The gap is a **continuous instant difference**, not floored to whole days before the percentile is taken.

### The threshold is a named percentile — PROPOSED at the 99th

**Not adopted. The Human Lead rules before Step 7 launches.** The reasoning offered:

The threshold's job is to identify **unusual silence**, not typical behaviour. A gap below it must be unremarkable for an account that is still active, so the percentile has to sit far enough out that ordinary quiet spells do not trip it.

**The binding cost is the false-dead rate.** At the 90th percentile, one ordinary gap in ten exceeds the threshold — an account with a handful of logged gaps would be declared dead by chance alone. At the 99th, one in a hundred. The 95th is the obvious alternative at one in twenty.

**The asymmetry points the same way.** Declaring a live account dead removes a pair, and the liveness exclusion **already biases the never-started share down** (`task-sheet.md` Step 14, bias 2). A lower threshold worsens a bias already on the record; a higher one does not. Step 1 also carries an accepted risk that the Step 9 liveness bound is deliberately worst-case, so the threshold should not add avoidable exclusions beneath it.

> **A caution the percentile alone does not answer, flagged for the ruling.** If liveness requires that *no* gap in a long sweep exceeds the threshold, the false-dead rate compounds with the number of gaps: even at the 99th percentile an account with 50 logged gaps trips it with probability ≈ 1 − 0.99⁵⁰ ≈ 39%. **That is a property of the rule's shape, not of the percentile**, and no choice of percentile fixes it. Whether the test applies to a single gap, to the gap bracketing `T0 + W`, or to every gap in the sweep is not settled by the current wording and may deserve its own ruling.

### The threshold rounds UP

Per [0025](0025-lag-unit-and-ceiling.md), and **two independent reasons agree**:

1. **It delivers the percentile it claims.** If a gap at or above the threshold marks the account dead, then flooring 43.2 to 43 declares dead an account whose 43.1-day gap is *inside* the stated percentile. That is the same off-by-one flooring produced at Step 6, where `W = 107` delivered 89.976% against a rule asking for 90%.
2. **It is the conservative direction**, per the false-dead asymmetry above.

## 3. Step 8's filter order

Step 8 said apply the filters *"in a fixed documented order"* **without fixing one**. The final row set commutes, so the analysis table is unaffected — but Step 8 also requires **"sample size after each filter"**, and that does not commute. Two faithful instances applying the same filters in different orders would report **different waterfalls on an identical table**, and the diff could not distinguish that from a bug.

The order is now fixed:

> **1.** Step 2 frame → **2.** `L2 = 1` exclusion → **3.** S1 completion rule → **4.** contamination exclusion → **5.** right-censoring → **6.** liveness rule → **7.** outcome assignment at `τ1`

**Contamination before right-censoring** was already required, so that an import-stamped S1 completion date is counted as contamination rather than laundered into a censoring drop.

**Right-censoring before liveness** is the one genuine choice, and the rationale is recorded in the spec: censoring is a property of the clock and `pull_date` — objective, and independent of behaviour — while liveness is a behavioural inference. Running the objective filter first means **liveness's marginal cost is measured on a fully observable population**, which is the number Step 9's floor-and-ceiling bound needs.

## Scope

- **No result changes.** No threshold, population or number moves. `W = 108` is unchanged; this entry propagates it rather than revisiting it.
- **The Step 7 percentile is open** and Step 7 must not launch before it is ruled.
- **This is the third consecutive gate whose spec needed a convention written into it before the dual pair could run** — "flattens" at Step 6, the lag unit at Step 6, and now the gap unit, the threshold criterion and the filter order. Item 26 predicted the shape; item 23 gives the remedy. **Step 8 and Steps 9–13 should be read for the same defect before each launches, not after.**
