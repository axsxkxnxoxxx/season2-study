# Decision 0050 — The six file defects are fixed and verified; the residual limits are routed; the un-guarded channel is measured at 297 pairs

| | |
| :--- | :--- |
| **Decision** | **Six file defects corrected and each verified on disk**, not recorded as done. **The residual limits, the biconditional gap and the un-guarded channel are routed into `task-sheet.md` Step 14** — recording a limit only in `decisions/` is not recording it. **Step 9 gains the two-ceilings sentence and the DERIV degeneracy note.** **The channel Red Team asked about is measured: 297 pairs.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Occasioned by** | Red Team's fifth Step 7 review, verdict HOLD — **propagation failure #9, live in all five files, produced by `0048` and `0049`** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 0. Why this entry does not claim a propagation pass

**`0049`'s header asserted a five-file pass that did not happen**, and Red Team found six defects across
all five files. **Every edit in this entry was verified by reading the file back after writing it**, and
the verification is in the transcript rather than in a sentence here.

**Both members of every pair carried each defect identically**, so the dual-implementation diff would
have shown agreement. **It cannot catch this class at all** — which is why these blocked rather than
waited.

## 1. The six defects

| # | Defect | Fixed |
| :-- | :--- | :--- |
| **1** | **Step 14's bias-2 entry: four clauses, four falsehoods.** "The exclusion set is entirely never-started" (it is 604 + 99); "0 excluded on DERIV" (99); "no movement on DERIV" (**UP 0.0042 pp**); "DOWN 0.2558 pp on APPLY" (**−0.2474**). **And seventeen lines below, the same section said −0.2558 must not be restated.** | Bullet rewritten on ALT-BROAD figures, with the superseded PF-LIMIT and ALT numbers named as withdrawn |
| **2** | Both `data-scientist` files carried **ALT's `196,654 → 33,373 → 604`**, eleven lines under an ALT-BROAD rule statement. **An instance following it implements `\|A\| = 0`.** `0049` fixed this in `task-sheet.md` only | **`196,654 → 52,514 → 703`**, with ALT's marked superseded |
| **3** | Both `data-scientist` files: *"every liveness exclusion is never-started by construction"* — **false; 99 of 703 are not.** This is the sentence instance A reported as stale, and `0049` §6 closed the snapshot hazard **on the arm's unverified claim that the file was correct** | Corrected; the never-started bound is stated as taken over the **604** only |
| **4** | *"Report the **ALT** exclusion count per arm: 485 to 716"* — **self-contradictory on its face**, in `task-sheet.md` and both `data-scientist` files | **537 / 550 / 633 / 664 / 701 / 703 / 789 / 864**, factor 1.61, with the S&L component reported separately |
| **5** | **The frozen-D10 figures 632 / 684 / 753 / 881 are the never-started COMPONENT, not totals.** Totals are **746 / 823 / 918 / 1,117**. `0048` §7 re-blessed them while attaching arms and **did not notice the rule change had made them a component** — the precise failure that section was written to prevent | Both stated, component labelled as such |
| **6** | Both `analytics-engineer` files: **"Reporting 604 is correct and is not a divergence"** beside **"EXPECT 703"**, with a **doubled em-dash edit scar** from swapping numbers into a sentence written for ALT. **These are the files Step 8's instances read** | Rewritten: **604 is the superseded ALT answer, and producing it IS a divergence** |

## 2. The limits are routed into Step 14, where limits are published

**Red Team's formulation, adopted: *"'Recorded, not repaired' is a legitimate way to close a gate;
recording it only in a `decisions/` entry is not."*** None of the following appeared in any file an
agent reads.

- **The calibration residual**, with the 22.68%, the inert clamp, the ~91%-mass stability, the tail
  instability, the direction-only survival of 700 of 703, and **the started-and-left component named as
  the fragile one** — median margin 81.3 days against 202.5, spanning 19× under tail residual against
  2.5×, with 525 of 703 on accounts whose last record is a `watch`.
- **Labelled `W = 108` only**, per instance A's own judgement call. **Step 13 runs to `W = 213`, where
  the exclusion set is 864 and the S&L component 148.**
- **The biconditional gap.** `0021` licenses *insertion after `τ1` ⟹ live*, a **sufficient** condition;
  the rule also asserts the converse. **ALT-BROAD narrows where that assertion is made from 1,355 pairs
  to 703. It does not justify it.** Open across five reviews, now recorded as a limitation.

## 3. Step 9 gains two sentences

**The two ceilings cannot both hold.**

> **FIGURE CORRECTED 2026-08-14 (`decisions/0051`).** This section first read *"16.9704 + 10.0405 +
> **73.6537** = **100.66%**."* **73.6537% matches no population.** It was taken from Red Team's review
> and propagated without checking — **the exact failure `0046` §0's standing rule exists to prevent,
> committed in the entry that routed that rule into Step 14.**

| On APPLY, n = 196,654 | Count | Share |
| :--- | ---: | ---: |
| Never-started ceiling | 33,373 | **16.9704%** |
| Started-and-left ceiling | 19,745 | **10.0405%** |
| **Continued** — no Continued pair is ever excluded | **144,140** | **73.2962%** |
| **Sum** | | **100.3071%** |

**The excess is 0.3071 pp, and it is exactly 604 / 196,654.** That is the mechanism, and it is what
should be stated rather than the total: **the same 604 pairs are counted once in each ceiling.** They
are **alternative worst cases over one set, not simultaneous ones.** Instance B asked for this and
neither `0048` nor `0049` carried it.

**The never-started bound is degenerate on DERIV** — [6.2055%, 6.2055%] — **so the dual control is
`x = x` there**, and the informative comparison is on APPLY.

## 4. The channel is measured: 297 pairs

Red Team's query, and it did not ask for the rule to change.

**The warrant is that a pair silent after `τ1` can produce no evidence in `[τ1, τ2)` and is scored
"left" by construction. That holds identically for a pair silent after `τ1 + ε` for any ε < 91 days** —
the failure mode is continuous and **the rule cuts it at one end.**

Measured on APPLY at `W = 108`, reproducing the 703 exclusions exactly as a check on basis:

| | Pairs |
| :--- | ---: |
| Not-Continued | 52,514 |
| Live **only** by conjunct 1 (¬Continued, inserted after `τ1`) | 51,811 |
| **Channel — of those, last insertion inside `(τ1, τ2)`** | **297** |
| — never-started | 207 |
| — **started-and-left** | **90** |
| ALT-BROAD exclusions | 703 |

**ALT-BROAD closes 703 of 1,000 such pairs — 70.3% — and leaves 29.7% open.** Last insertion in the
channel sits at a median of **51.4 days** past `τ1`, p90 **85.1**, max **90.9** — filling the window.

**So the answer to Red Team's question is "most of the channel, not a corner" — and the residual is not
nil.** The 90 started-and-left pairs in it are **treated as observed by the new S&L bound**, which is
the specific consequence worth carrying, and it is now in Step 14.

**No rule change is proposed.** ALT-MATCHED — one silence test per null at the instant that null is
read — is recorded as the form that would close the remainder, and is not adopted.

## 5. What Red Team cleared

It re-derived the arithmetic independently: the shares sum to 100.0000 filtered and unfiltered, the
movements sum to zero, both corner resolutions sum to 196,654. **"[9.6830%, 10.0405%] is correct and its
warrant is correct."** The conditional sub-interval **cannot be misread as the bound**. And it declined
to hold on the residual: the direction-only test *"assumes only that a record is not inserted before it
is watched, needs no magnitude, and 700 of 703 survive with zero created."*

## 6. Scope

- **No rule change. No rerun.** Every figure both arms produced stands.
- **Zero API calls** — the channel measurement reused the arms' stored masks and reproduced the 703 as
  a basis check.
- **Step 8 does not launch.**
