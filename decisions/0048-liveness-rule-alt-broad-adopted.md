# Decision 0048 — ALT-BROAD is adopted: a pair is not live iff no insertion instant after `τ1` AND not Continued

| | |
| :--- | :--- |
| **Decision** | **ALT-BROAD is ADOPTED.** A pair is **not live iff BOTH** the account shows no insertion instant after `τ1` **and** the pair is **not Continued**. The `\|A\| = 0` form is superseded: **the warrant reaches Started-and-left too.** `0046` §2's table is corrected; `0047` §5's figures get their arms; five stale `task-sheet.md` lines are fixed. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Occasioned by** | Red Team's fourth Step 7 review, verdict HOLD |
| **Supersedes** | ALT (`0046` §1); `0046` §2's outcome-basis table |
| **Status** | Closed. **Step 7 reruns on ALT-BROAD. The gate is OPEN.** |

---

## 1. The adopted rule

> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND the pair is NOT Continued.**

## 2. Why the warrant reaches Started-and-left

**Liveness licenses trusting a null. Under `0034` there are two nulls, not one.**

| State | Basis |
| :--- | :--- |
| Never started — `\|A\| = 0` | **null** |
| **Continued** — `\|A\| ≥ 1` ∧ `F2 ∈ A_H` ∧ `\|A_H\| ≥ ceil(0.90 × L2)` | **the only state resting on positive evidence** |
| Started and left — `\|A\| ≥ 1` ∧ ¬Continued | **null on exit.** `\|A\| ≥ 1` is observed; **the failure to meet the Continued condition is not** |

**And it is structural, not incidental.** `τ2 > τ1`, so **a pair silent after `τ1` is silent after `τ2`
and can produce no evidence anywhere in the `[τ1, τ2)` window the Continued test reads.** It is scored
**"left" by construction** — the exact failure liveness exists to prevent, applied to the second
headline category.

**This study is "never started versus started and quit." Both halves need the guard.** ALT guarded one.

## 3. Both of instance B's objections to ALT-BROAD fail

B recommended ALT over ALT-BROAD on two grounds. **Neither survives, and Red Team dismantled both.**

**(a) "ALT-BROAD's sign is population-dependent."** True — UP 0.0042 pp on DERIV, DOWN 0.2474 pp on
APPLY — **and irrelevant.** `0045` §4.1 established that signs are population-scoped and both must be
carried; `0046` §0 made stating the population a standing rule. **Choosing the rule whose sign is
stable is choosing the number that flatters the ruling — the exact behaviour `0046` §0 names as this
chain's recurring cause.**

**And B refuted its own argument elsewhere in the same artifact:** it called ALT's clean DOWN sign *"an
arithmetic identity, not evidence… it means the rule can never correct a bias running the other way."*
**The record adopted ALT partly on an identity the same arm called non-evidence, and rejected
ALT-BROAD for lacking it.**

**(b) "Its `τ1`-anchored silence test is mismatched to a `τ2`-read state."** **Backwards.** Since
`τ2 > τ1`, *no insertion after `τ1`* ⟹ *no insertion after `τ2`*, so **ALT-BROAD at `τ1` is strictly
narrower than a `τ2`-matched form.** It is the **conservative** version, uses the silence test the rule
already computes, introduces no new anchor, and does not touch `0034` §6.3's liveness anchoring.

## 4. `0046` §2's table is corrected

It read: *"Positive in-window S2 evidence | 751 | **directly observed** — 652 continued, 99 left."*

**652 are directly observed. 99 are not.** The 751 split **652 observed / 99 null-based**, and **the
warrant reaches the 99.** `0047` corrected three claims in `0046` and missed this one.

`0046` §2's own dispositive sentence — *"a gate whose deliverable is 'the rule statement' cannot close
on a rule half of whose deletions have no stated reason"* — **applies symmetrically to a rule that
stops short of its own stated reason.**

## 5. What changes, and what does not

| | ALT (superseded) | **ALT-BROAD (adopted)** |
| :--- | ---: | ---: |
| Exclusions, **DERIV** | 0 | **99**, from 73 accounts |
| Exclusions, **APPLY** | 604, 191 accounts | **703**, from 216 accounts |
| Composition, APPLY | 604 NS | **604 NS + 99 S&L** |
| Per-arm, APPLY | 485 → 716 | **537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** |
| **Never-started bound** | [16.6633%, 16.9704%] | **identical** |
| **DERIV dual diff** | **`0 = 0`** | **99 against 99, on 73 accounts** |

**The never-started bound is unchanged because the 99 are Started-and-left and enter neither
endpoint.** Width 0.3071 pp, both endpoints on 196,654, ceiling equal to the unfiltered share as an
identity.

**The dual control becomes informative for the first time in this step.** Under ALT the DERIV diff was
literally `0 = 0` at every arm from 38 to 213 — the population Step 7 is defined on, derived on and
reviewed on. **Red Team's formulation: a gate cannot close on `0 = 0` when a measured alternative,
selected by the gate's own stated warrant, makes the control informative and has never been ruled on.**

**A second bound becomes available and is now required** (Step 9): on the **started-and-left** share,
over the 99. **None exists today.**

**And the un-guarded channel ALT left open grows faster than the rule does** — the S&L component runs
**52 / 56 / 79 / 89 / 98 / 99 / 125 / 148** across the arms **on APPLY** *(population label added by `0049`)*, a factor of **2.85** against the rule's own ~1.5–1.6× `W`-coupling. **On DERIV the top arm is 147, not 148** — both arms measured it, and an unlabelled series would have read as a divergence. Under ALT that was an unmeasured gap widening with `W`; under ALT-BROAD it is inside
the rule and reported per arm.

## 6. Five stale `task-sheet.md` lines fixed — propagation failure #8

**`0047`'s header claimed propagation to Steps 7, 8 and 9. Step 9 never got the pass.**

| Line | Was | Now |
| :--- | :--- | :--- |
| **332** | **`[16.7146%, 16.9704%]` as the operative Step 9 instruction** — while **both `data-scientist` files mark it superseded**, and Step 9 is a dual pair reading both | `[16.6633%, 16.9704%]`, both endpoints on 196,654, with the two superseded intervals recorded |
| 333 | `0045`'s floor refutation sitting under a floor refuted the same way | folded into the superseded-intervals note |
| 444 | "Option C" and "seven in seven of the 751" — PF-LIMIT as operative | superseded |
| **458** | **PF-LIMIT on DERIV described as the approved rule** — 0.032 / 0.023 / 0.009 pp, 751 of 147,370 — contradicting line 441 four bullets above | ALT-BROAD's figures, with the superseded ones named |
| **459** | **"The rule is first exercised at Step 8"** — the exact sentence `0047` §4 corrects, verbatim, still operative | corrected; the DERIV diff is now 99 vs 99 |

**Line 332 was the serious one:** two Step 9 instances would have read one bound from the task sheet
and a different one from their own definition files, resolved it differently, and produced **a
divergence that is an artifact of the record** — the precise failure `0045` §5 was written to pre-empt.

## 7. `0047` §5's figures get their arms

*"Freezing D10 at `W = 108` gives 632 / 684 / 753 / 881 at the upper arms"* — **the arms are
`W` = 125 / 150 / 180 / 213**, and **125 and 180 are not in the mandated grid**. Stated without them, a
Step 13 instance would pair 632/684 with arms 150/213 and **report a false divergence**. Only **684 and
881** are comparable to the mandated arms.

**This is the standing rule in a third dimension: a figure stated without the arm that produced it.**

## 8. The five-file pass — what was touched, and what deliberately was not

**Touched:** `task-sheet.md` (Steps 7, 8, 9, 13, 14); `.claude/agents/data-scientist.md`;
`data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md`. Both pairs verified
byte-identical apart from the `name:` field.

**Deliberately not touched, and why:** `red-team.md`, `second-brain.md` and the five `reviewer-*.md`
files **carry no liveness specification** — they were checked at `0035` and again here. `decisions/`
entries other than those named above are historical record and are amended only in place, with markers.

## 9. What remains open

**Red Team's item 2 is narrowed, not closed.** `0021` licenses *"insertion after `τ1` ⟹ live"* as a
**sufficient** condition; the rule is a biconditional. **`0046` §7 declared the item closed and that
overstated what was bought** — instance B said so directly: *"It narrows where that assertion is made…
It does not justify it."*

> **§9's gloss was withdrawn by `0053` and is RESTORED by `0054`.** `0053`'s premise — that `0021`
> predated the second window — is false; `0034` created that window and ruled liveness anchored at
> `τ1` in the same entry. **"Insertion after `τ1` ⟹ live" stands.**

**Un-actioned and required before this gate closes:** **22.68% of dated records claim a `watched_at`
later than their own calibrated insertion instant**, and the rule's first conjunct **is** a comparison
between an interpolated instant and `τ1`. **Nobody has bounded the calibration residual for the excluded
set.** Also **5,094 records are clamped above the calibration range**, which pushes `max(instant)`
earlier and **directly toward false exclusion**.

## 10. Scope

- **Rule change.** Both arms rerun on ALT-BROAD.
- **Zero API calls.**
- **Step 8 does not launch.**
