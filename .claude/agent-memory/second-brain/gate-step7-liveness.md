---
name: gate-step7-liveness
description: The Step 7 liveness gate as a narrative — four rules in succession (632d, 1293d, PF-LIMIT, ALT, ALT-BROAD), five Red Team HOLDs, nine propagation failures, the warrant that finally selected the rule, and the five-entry self-correction cascade; still OPEN as of decisions/0050
metadata:
  type: project
---

# Step 7, the liveness gate — the longest and messiest stretch of the study

**Status as of `decisions/0050`, 2026-08-14: the gate is OPEN.** Sixteen decision entries
(`0035`–`0050`), five Red Team reviews, seven dual runs, zero API calls throughout. Gate 4 of 5 has
been approved twice and reopened twice. **Step 8 has never launched.**

**Why this file exists:** the individual entries are each correct about what they decided. Only the
sequence shows what actually happened, and the sequence is the Step 18 material.

---

## The spine — four rules in succession, and none of them is the first one

| # | Rule | Where | Fate |
| :-- | :--- | :--- | :--- |
| 1 | **A numeric threshold, 632 d** — 99th percentile of the bracketing-gap distribution on the 152,126, interval [528, 787] | `0039` **APPROVED** | **SUSPENDED** by `0040` |
| 1b | **1,293 d** — same rule, extended reference set (open-ended entered as `+∞`) | `0041`, provisional | Never approved |
| 2 | **PF-LIMIT** — not live iff **no insertion after `τ1`**. Threshold **DELETED** | `0042` **APPROVED** | **SUPERSEDED** by `0046` |
| 3 | **ALT** — not live iff no insertion after `τ1` **AND `\|A\| = 0`** | `0046` | **SUPERSEDED** by `0048` |
| 4 | **ALT-BROAD** — not live iff no insertion after `τ1` **AND NOT Continued** | `0048` **ADOPTED** | Current. Gate still open |
| — | **ALT-MATCHED** — one silence test per null, at the instant that null is read | `0050` §4 | **RECORDED, NOT ADOPTED** |

**ALT-MATCHED is the form that would close the residual channel `0050` measured. It was named and
deliberately not adopted.** It must never be cited as the rule, and it must never be dropped from
the record either — it is the acknowledged remainder.

**PF-BRACKET** is a fifth name in the record and was never a candidate: it is the *literal reading*
of `0041` §4's withdrawn wording, priced at 18,903 exclusions from 1,434 of 2,402 accounts. It exists
only to show what the wording would have cost.

---

## Five Red Team HOLDs, and what each turned on

| # | Entry | What it turned on |
| :-- | :--- | :--- |
| **1** | `0040` | **`0036` §2.3(ii) contradicted an approved gate.** `0021` (gate 2 of 5) holds that any record inserted after the window closed **proves the account was alive**; `0036` ruled the "no instant at or before `τ1`" bucket **dead**. Every pair in it has instants after `τ1` **by construction**. **18,250 pairs — 76.8% of the filter's exclusions.** Nothing in `0036`–`0039` cited `0021` against it |
| **2** | `0043` | **Step 14's bias-2 sign was wrong**, in the study's central honesty artifact. The ledger said the liveness exclusion moves never-started **DOWN**; measured, it moved **UP**, because the filter preferentially deletes **confirmed continuers**. Instance B had named it — *"the filter is not selecting on the outcome it was built to protect"* — and it was not acted on until Red Team made it blocking |
| **3** | `0044` | **"No free parameter" is not what the evidence shows.** Deleting the threshold *made the coupling total*: PF-LIMIT's exclusion set **is** the open-ended bucket, a pure function of `W`, and **`W` was held at 108 for the entire sensitivity test that justified the deletion.** Plus **propagation failure #6** — neither `analytics-engineer` file stated the rule, and they are the first files the Step 8 instances read |
| **4** | `0046`, `0048` | **The not-live branch had no stated warrant.** `0021` licenses *insertion after `τ1` ⟹ live* — a **sufficient** condition, not the biconditional. Held three times; the third was dispositive. `0046` answered it by adopting a rule the warrant reaches; `0048` found the answer still stopped short |
| **5** | `0050` | **Propagation failure #9 — six defects live in all five files, produced by `0048` and `0049` themselves.** `0049`'s header asserted a five-file pass that did not happen. **Both members of every pair carried each defect identically**, so the dual diff would have shown agreement |

**Red Team's standing contribution here is not a number. It is that four of the five HOLDs were
against the *record*, not the *rule*** — a contradicted gate, a wrong sign, an overclaimed property,
and unpropagated text. Only HOLD 4 attacked the rule itself, and it is the one that changed it twice.

---

## Why the threshold was deleted — the headline could not tell 787 from 2,200 days

| Setting | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 d | 6.2109% | 82.3812% | 11.4078% |
| 1,293 d | 6.2325% | 82.3497% | 11.4178% |
| 2,200 d | 6.2373% | 82.3490% | 11.4137% |
| Parameter-free | 6.2373% | 82.3427% | 11.4201% |

**Max movement across all four: 0.026 / 0.038 / 0.012 pp — about 3% of the account-clustered
sampling width** (0.78 / 1.25 / 0.99 pp at B = 4,000). A continuous 30–4,000 day sweep moves nothing
beyond 0.243 pp. **Both arms produced these independently and identically to four decimal places.**

**These levels are on DERIV and are NOT results.** `0042` §5 and README item 47 both say so: Step 8
applies liveness to APPLY, whose extra lines carry contaminated `T0`. **The absolute shares move; the
flatness finding does not**, because the exclusion sets are under 1% of the population either way.

**One delta is statistically distinguishable and still immaterial:** the paired clustered CI for
787→2,200 on never-started is [+0.008, +0.046] pp, excluding zero, because nested subsets give
near-zero paired variance. **Detectable, not material** — instance A reported both facts rather than
the convenient one.

**The deeper reason is the quota property** (`0038` §4): a percentile of the distribution the test is
applied to sets the level **by the exclusion rate, not by any feature of the data**. Instance A:
*"a quota rather than a finding."* **There was never a number to find.**

**What the three derivations bought** (`0042` §7): deriving it three times is what established that
it does not matter. Along the way the same work exposed a rule contradicting an approved gate on
76.8% of its exclusions, a reference distribution calibrated on one population and applied to
another, an impossible invariance claim, and a wording that reinstated a withdrawn rule.

---

## The warrant that finally selected the rule

This is the one argument in the whole sequence that did analytical work, and it is short:

> **Liveness licenses trusting a null.** A pair whose outcome rests on positive evidence has nothing
> for liveness to protect.
>
> **Under `0034` only Continued rests on positive evidence** — `F2 ∈ A_H` and
> `|A_H| ≥ ceil(0.90 × L2)`.
>
> **Never started is a null.** **Started-and-left is ALSO a null — on exit.** `|A| ≥ 1` is observed;
> the *failure to meet the Continued condition* is not.
>
> **And it is structural, not incidental: `τ2 > τ1`**, so a pair silent after `τ1` is silent after
> `τ2` and **can produce no evidence anywhere in the `[τ1, τ2)` window the Continued test reads.**
> It is scored "left" **by construction** — the exact failure liveness exists to prevent, applied to
> the second headline category.

**This is why the gate ended where it did.** PF-LIMIT reached past the warrant (751 deletions with no
stated reason); ALT stopped short of it (guarded one null of two); ALT-BROAD is the rule the warrant
reaches. `0048` §4 puts it symmetrically: *"a gate whose deliverable is 'the rule statement' cannot
close on a rule half of whose deletions have no stated reason"* — **and it applies equally to a rule
that stops short of its own stated reason.**

**The warrant is an argument, not a measurement.** Instance B said so in those words, and it is why
Red Team's item 2 is **narrowed, not closed**, and now sits in Step 14 as a limitation: `0021`
licenses one direction of a biconditional. ALT-BROAD narrows where the unlicensed assertion is made
from 1,355 pairs to 703. **It does not justify it.**

---

## Nine propagation failures, and the three standing controls they produced

**A ruling lands in a decision entry and not in the file the agents read.** README item 46, which
still says "five times now."

| # | The miss | Caught by |
| :-- | :--- | :--- |
| 1 | Ten decisions to `task-sheet.md`, none to `.claude/agents/` | `second-brain`, `0035` |
| 2 | `0034`'s three Step 10 requirements: in the approved text, in no spec | `second-brain`, `0035` |
| 3 | `0036` applied to the Step 7 bullet body, not its "NOT LAUNCHED — UNRULED" header | instance A |
| 4 | `0039` corrected `0038` §5 and not `task-sheet.md` line 248 | Red Team, `0040` |
| 5 | `0040` corrected four task-sheet figures and **missed line 266 — the one that sets the threshold** | both arms |
| 6 | Neither `analytics-engineer` file stated the liveness rule — **the files Step 8 reads first** | Red Team, `0044` |
| 7 | The withdrawn "vary the liveness threshold" survived in the two files `0044` had itself named | `0046` |
| 8 | Five stale `task-sheet.md` lines, incl. **line 332 carrying the superseded bound as operative Step 9 instruction** | `0048` |
| 9 | **Six defects in all five files, produced by `0048` and `0049`**; `0049`'s header claimed a pass that did not happen | Red Team, `0050` |

**The three controls, each added because the same failure recurred somewhere new:**

1. **Item 46's five-file surface** (`0044` §3.1). *The propagation surface is `task-sheet.md` plus
   the four pipeline agent definitions, and an entry that changes a rule must state which of the five
   it touched and which it deliberately did not.* **A ruling that names no files has not been
   propagated, whatever the entry says.**
2. **`0046` §0's population rule.** *Every figure in a decision entry states which population
   produced it, at the point of use. An entry that cites a number without its population is not
   propagated.* Written after three consecutive entries each corrected the previous one and **each
   committed the same error.** Extended by `0047` §3 to interval endpoints: *an endpoint states the
   population it is computed on and the estimand it bounds, and they must be the same population.*
3. **`0049` §6's agent-launch snapshot practice.** An agent's definition is **snapshotted at
   launch**, so a file edited and an agent launched in the same turn can disagree and **the agent
   cannot see it is holding an old copy.** *Every launch prompt for a spec-bearing step states the
   operative rule verbatim and tells the instance that where its definition disagrees with
   `decisions/` or the on-disk `task-sheet.md`, the on-disk file wins.* **The launch prompt, not the
   definition file, is the authority at launch.**

**`0050` §0 adds the fourth, unnamed but practised:** every edit verified by reading the file back,
with the verification in the transcript. It exists because `0049` recorded a pass it had not done.

> **The dual-implementation control cannot catch this class at all.** Both halves of every pair
> carried each `0050` defect identically. `0035` §1 is the general statement: *a dual pair whose two
> halves read the same stale brief produces a clean diff and a wrong answer.*

---

## Repeated self-correction failure — five consecutive entries, each correcting its predecessor and each introducing a defect

**This is the pattern most worth carrying into Step 18, because it is a property of the process and
not of any one entry.**

| Entry | Corrected | Introduced |
| :--- | :--- | :--- |
| `0042` | `0041` §4's wording | §4 quoted **the deleted 1,293-day rule's** deltas as the approved rule's |
| `0043` | `0042` §4's deltas, and bias 2's sign | Published the **DERIV** direction as the study's; prescribed a remedy on "~40 never-started exclusions" that **are zero**; merged two claims into "six in seven" |
| `0045` | `0043`, three ways | Rejected ALT on **the DERIV row, where ALT is zero by construction**; published a bound that **mixed denominators** and whose floor was not a floor |
| `0046` | `0045`'s rejection and its bound | §1's two explanations both wrong; §4's bound **mixed denominators again**; §7 too pessimistic; §2's table called 99 null-based pairs "directly observed" |
| `0047` | `0046` §1, §4, §7 | **Missed `0046` §2's "751 directly observed"** — caught one entry later by Red Team's fourth review |

**Instance A's line, from inside `0045`: *"the seventh instance, inside the entry correcting the
sixth."*** The named error class is **a figure measured on one configuration or population, quoted as
if measured on another** — `0038` §5, `0039` §2, `0039` §6, `0042` §4, `0043` §2, `0045` §4.1, and on.

**`0046` §0 names the cause and it is not inattention:** *"It is reaching for the number that
supports the ruling being written rather than checking which population produced it."*

**Three consecutive bounds had an endpoint outside the feasible set** (`0047` §3): `0043`'s ceiling,
`0045`'s floor on the other side, `0046`'s floor on a mixed denominator. **The fourth was refused —
by both arms, independently, before the ruling** (`0049` §2). Instance A named the stake: the narrow
S&L reading *"would have made this the fourth consecutive bound failing that exact test."* **The
standing rule worked before it could be broken a fourth time, and it worked in the arms rather than
in the ruling.** That is the one clean win in this sequence and Step 18 should say so.

---

## What the dual runs actually bought, and what they did not

**`0040` §7 is the honest statement and it should survive into the write-up:**

> **Exact agreement between the two arms is WEAK evidence of correctness.** Every published quantity
> is a deterministic function of frozen inputs — the same cached sweep, the same stored calibration
> neither arm refits, an exactly-specified collapse rule, a named percentile, a named population.
> **Agreement was `0038`'s design goal.** It confirms the spec is unambiguous; **it cannot confirm
> the spec is right.**

**What the diffs did buy, in order:** 4 days apart on the gap unit (`0037` §4) → 410 days apart on
the reference population, 504 vs 914 (`0038` §1) → 787 vs 790 on a bootstrap endpoint, inside
measured seed noise (`0041`) → exact agreement thereafter. **Each divergence was a spec ambiguity,
and each was closed by naming the operation rather than describing it.**

**Under ALT the DERIV diff was literally `0 = 0` at every arm from 38 to 213** — on the population
Step 7 is defined, derived and reviewed on. Red Team's formulation: *a gate cannot close on `0 = 0`
when a measured alternative, selected by the gate's own stated warrant, makes the control informative
and has never been ruled on.* **ALT-BROAD makes it 99 against 99 on 73 accounts — informative for the
first time in this step.**

**The never-started bound is still degenerate on DERIV — [6.2055%, 6.2055%] — so that control is
`x = x` there** (`0050` §3). The informative comparison is on APPLY.

**Both arms repeatedly argued against their own recommendations**, which is the reason the rulings
had the evidence they needed: A recommended adopting ALT and named that it *"empties the unwarranted
branch without warranting it"*; B recommended against ALT-BROAD and had already refuted its own
argument elsewhere in the same artifact, calling ALT's clean sign *"an arithmetic identity, not
evidence."*

---

## Two things recorded and not repaired

- **The 38,696 clock-mismatch bucket** (`0037` §3). `T0` is built from claimed `watched_at`; liveness
  runs on insertion time. The median pair's `τ1` falls **1,578 days before the account's first-ever
  insertion instant**, and 8,037 pairs have `τ1` before the calibration curve starts. **These are not
  absent users — they are pairs whose window closed before the account existed on the insertion
  clock.** Routed to Step 14. Note this bucket was subsequently *returned to the population* by
  `0040` §1, so its residue is a limitation, not an exclusion.
- **The un-guarded channel, 297 pairs** (`0050` §4). The warrant holds identically for a pair silent
  after `τ1 + ε` for any ε < 91 days — **the failure mode is continuous and the rule cuts it at one
  end.** ALT-BROAD closes **703 of 1,000 such pairs (70.3%) and leaves 29.7% open**; last insertion
  in the channel sits at median 51.4 days past `τ1`, p90 85.1, max 90.9 — filling the window. **The
  90 started-and-left pairs in it are treated as observed by the new S&L bound.**

## The calibration residual — discharged, with its limit

`0049` §5, the last item standing under the rule's first conjunct, which **is** a comparison between
an interpolated instant and `τ1`.

- **22.68%** of dated records (6,271,584 of 27,656,434) claim a `watched_at` **later** than their own
  calibrated insertion instant.
- **Clamping is inert — a clean discharge.** Clamp value **2026-08-10T20:48Z**, while D10 forces
  `τ1 ≤ 2026-05-12` at every arm, so **0 of 66,961 APPLY pairs on clamped accounts are excluded.**
- **Sound at the mass, not in the tail.** Residual is **bimodal**: median ≈ 0.02 d, p90 ≈ 0.107 d,
  upper tail 77–125 d. At the ~91% mass the exclusion set is stable (703 → [701, 703]); at ±7 d,
  [686, 717]; **at ±124.6 d, [414, 1284].**
- **Direction-only cross-check: 700 of 703 APPLY exclusions survive and none is created.** Only 3 of
  703 excluded pairs' accounts claim any `watched_at` after `τ1`.
- **The stated limit: the started-and-left component is the fragile one.** Median margin **81.3 days**
  against **202.5** for never-started, spans **19×** under tail residual against 2.5×, and **525 of
  703 sit on accounts whose last record is a `watch`, where the residual is not directly measurable.**
- **All stability figures are `W = 108` only.** Step 13 runs to `W = 213`, where the exclusion set is
  864 and the S&L component 148.

Related: [[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[decision-log-step18]], [[withdrawn-claims-register]], [[gate-step5-contamination]],
[[amendment-step1-continued-boundary]].
