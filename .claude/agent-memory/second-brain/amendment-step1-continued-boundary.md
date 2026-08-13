---
name: amendment-step1-continued-boundary
description: The Step 1 §7 amendment moving Continued to τ2 = 199 days — approved as decisions/0034 after eleven Red Team rounds, the rule never broken, the anchor choice adopted with no stated ground, and the three Step 14 ledger items it created
metadata:
  type: project
---

# Step 1 §7 amended — Continued moves to `τ2`. `decisions/0034`, 2026-08-12.

**Fact of record: `decisions/0034-step1-continued-boundary-amendment.md` records the Human Lead
approving the amendment in writing on 2026-08-12.** Gate 1 was **reopened as an amendment and
re-approved** — this changes a rule Step 1 **owns**, not a premise it relied on, which is what
distinguishes it from `0030`. Full record: `artifacts/step1-amendment-continued-boundary.md`,
**revision 13**, with §11–§21 the per-round dispositions. `artifacts/step1-outcome-definition.md`
has been **amended in place** and is operative as amended.

**Why:** *"The old boundary scored a late completer as an abandoner, which was false. That is the
whole of the case, and the rest is the price of fixing it."*

## The approved rule

Never started stays at **`τ1` = 108 days**. Continued moves to **`τ2 = ⟦T0⟧ + (W + H) × 24h` = 199
days**. Definitions and the full state table live in [[glossary-terms-and-thresholds]]. Also
approved, each in the Human Lead's own terms:

- **`|A| ≥ 1` at `τ1` remains a conjunct of Continued.** Without it a day-150 starter completing by
  day 190 falls in two states.
- **Step 10's `p` uses the rank form with `m_H`.** `m_H / L2` stays withdrawn.
- **D3 is replaced by D3′**, run at **every** Step 13 arm with its own cleared count and share.
- **Liveness stays anchored at `τ1`** — it licenses trusting a null, and the null is `|A| = 0`.
  **Written into the Step 7 spec** so no isolated instance re-anchors it.
- **Step 8 gains the `A ⊆ A_H` invariant**, labelled a **code check, not a data check.**

## The figures, and what they can and cannot show

On the Step 5 estimation sample of 128,099, **with D11 applied**:

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| Before | 8,449 | 102,230 | 17,420 |
| **After** | **8,449** | **104,476** | **15,174** |

**2,246 pairs move, all in one direction.** Expressed on the published category:
**Started-and-left falls 12.9%.** Expressed on the ratio: **0.485 → 0.557, a 14.8% shift.** Both
forms are required — the ratio is what the study reports, the category count is what a chart shows.

Four properties carried the case: **monotone** (`A ⊆ A_H`), **never-started share unchanged** to
four decimals (6.5957%), **zero censoring cost** at every arm (`W + H ≤ max(W, 91) + H` is an
identity, and at `W = 108` D10's clearance **is** `τ2`), and **no new constant** (`H = 91` adopted
by name at D10).

**The invariance is a check on a structural argument, not evidence for it.** The argument is that
`|A| = 0` is untouched; the arithmetic confirms the implementation matches. It would be worthless
if the argument were wrong.

**Limits of the demonstration table, stated because it is the table a reader will trust most.**
It is not a headline. The estimation sample requires S2 evidence, so the true never-starters —
**23,735 pairs with no S2 record at all** — were removed at the waterfall's second step. All 8,449
"Never started" rows in it **did** start S2, and **8,445 hold an admissible record saying so** (both
measured, not inferred, after two revisions in which 8,445 was an upper bound presented as a count).
The sample is also **not right-censored**, so `A_H` is not fully observed for every row.

## Stated plainly, and not softened

- **It fixes 39.5% and leaves 60.5% standing.** Of **5,686** Started-and-left pairs that eventually
  complete S2, **2,246 are reclassified and 3,440 are not.** The residual is **reported, not
  resolved** — 19.75% of the old Started-and-left group, 22.67% of the new one.
- **"Never started" can include pairs that demonstrably started and finished.** Day-150 start,
  complete by day 190: `|A| = 0`. This follows from the design and is the sharpest oddity of the
  split. **D8(ii) already measures exactly this group.**

## The rule was attacked eleven times and never broken

**Every hold from revision 2 onward was against the justification prose, not the rule.** The
partition's exhaustiveness and disjointness, the `A ⊆ A_H` monotonicity, and the
`max(W, 91) + H ≥ W + H` identity held every single round. **Six of the last seven rounds
introduced fresh defects while repairing old ones** — the pattern is recorded in the artifact rather
than smoothed over, and four consecutive rounds found a ruling executed in the prose but **not in
the code**.

**Hence the strip at revision 10:** ~2,350 words cut — §1.1 and §2.2/§2.3 — on the Human Lead's
ground that *a section which has lost three arguments in three rounds is a liability regardless of
what a fourth might achieve.* Red Team's judgement that §1.1 "should not be cut" is recorded and
**was not followed**. Red Team's own verdict on the strip: *"it removed 2,350 words and introduced
no new arithmetic error, which is the first round in seven that can be said of."* §11–§18 are left
**unedited** so the history stays on the record.

## The anchor choice has NO stated ground — four attempts, four failures

**There is no argument anywhere in the live text for preferring `τ2` to `first-S2-watch + H`.**

| Rev | Ground offered | How it failed |
| :--- | :--- | :--- |
| **6** | **Exogeneity** — `τ2` contains no behavioural term | **False.** `S1_completion_date` binds `T0` on **116,041 / 220,107 = 52.7%** of pairs |
| **7** | **Temporal position** — the behavioural term is realised before the window opens | **Does not bind.** `|A| ≥ 1` at `τ1` means D10 already imposes the clearance |
| **8** | **Arm comparability** — a per-pair horizon breaks holding `H` constant | **False.** That line governs `H`'s *value* across arms; **no window changes length** |
| **12** | **Choice at a stated price** — the start anchor gives equal exposure, `τ2` does not | **False and backwards.** A starter has lag `< 108`, so `τ2` allows `199 − lag > 91` for **every** starter — the "price" is **dispersion, not deficit** — and item 9's set **grows** under the start anchor |

**Three things in the document point at the alternative and are unanswered:** §1's motivating
quotation (*"108 measured from the wrong anchor"*), §2's marginal-lag row — **which is the
start-anchored rule's own distribution**, so the document computes the alternative's evidence and
uses it to grade the adopted rule — and §5.1's asymmetry, disclosed as mandatory with nothing saying
why it was accepted.

> **"This absence is the honest record and is not to be repaired by a fifth attempt without new
> evidence."** An unstated ground is a gap a reader can see and weigh; four stated grounds that did
> not survive review would have been worse, and three were published before being withdrawn.

## Two review findings that changed figures elsewhere

**1. D11 was not being applied.** `τ_pull` is a global frozen cutoff and records at or after it are
discarded from every computation; neither `eval_continued_boundary.py` nor the correction script
applied it. Applied: **77 records discarded, 28 pairs touched**, never-started **8,445 → 8,449**,
Continued −4 at both bounds. **2,246 and 12.9% did not move.** Ruled **fixed, not noted**, because
it touched a published table. **The scope limit is disclosed, not chased:** D11 is *not* applied to
the Step 5 pair table (`first_s2_lag_days`, `s2_ev_n`, `T0`) or to `step6_completion_lag.py`, and
extending it would move an approved waterfall and the distribution `W = 108` came from. Bounded at
77 records / 28 pairs in-sample and **1,734 of 27,656,434 account-wide, 0.006%**. README item 41.

**2. `first_s2_lag_days` is a BACKFILL measure**, `tau − ts` — a record's estimated insertion instant
minus its claimed `watched_at` — **not a start-time filter.** The draft misread it for **six
revisions** and argued from it in two ledger entries. **Step 5 named it correctly throughout, so the
approved Step 5 gate is untouched.** The floors now rest on the **contamination-exclusion channel:
50,066 pairs**, not 73,801 — the 23,735 dropped at the waterfall's second step have `A_H = ∅` and
can enter no numerator, so they are the **ceiling** channel, not the floor one. README item 42.

**The four pairs are one fact appearing as three caveats.** §4.1's D11 four, Step 6's
`tau_pull_conflict` four, and the 12.9%-channel four are the **same four pairs** — reproduced under
instance A's definition, source and population, set-identical under both the all-S2 and in-`E2`
readings. **`of_which_C1: 0`**, so none is in `W`'s derivation population and `W` cannot move in any
unit. (Quoting instance A's `W_with/without: 107.0` proves less, because 107.0 is a figure this
study does not use.)

## Step 14 — items 8, 9 and 10. They publish together and are never netted.

| # | Mechanism | Direction | Size |
| :--- | :--- | :--- | :--- |
| **8** | The Continued boundary at `τ1 + H` — a **definitional change** | **none claimed against truth** | 2,246 pairs; ratio 0.485 → 0.557; SAL −12.9% |
| **9** | Late completers beyond `τ2`, left scored as abandoners | ratio **DOWN** | **3,440**, a floor |
| **10** | Never-started at 108 while Continued is at 199 | ratio **UP** | **1,575** on the estimation sample, **1,573** after censoring; a **floor for D8's population**. 18.64% is a **CEILING** |

**Item 8 is a third kind of quantity** — not a population change and not an estimator bias. The
population is identical and no estimate is biased; the old rule was *defining* the ratio
differently. `0028`'s no-netting rule **extends to boundary corrections unchanged**, and item 8 may
not be combined with `0031`'s censoring asymmetry or `0023`'s discard non-neutrality either.

**Items 9 and 10 are counterweights and their counts are NOT commensurable.** Item 9 acts on the
ratio's **denominator**, item 10 on its **numerator** — counts stand ~2.2 : 1, ratio effects
~1.6 : 1 — so subtracting one from the other produces a number that means nothing. **Reporting
either alone puts one half of the asymmetry in front of the reader**, which is the
netting-by-omission `0028` exists to stop.

**No corrected never-started count or ratio is given.** Both known channels push the **same** way
and neither is measured, so a corrected figure would be wrong in a known direction by an unknown
amount. The printed values **6,874 / 5.37% / 0.453** were removed at revision 8 and must not
resurface. **Item 10 is not a cost of adopting** — those pairs are Never started under the
pre-amendment rule too; `A_H` is what makes them **measurable**.

## Three loops worth remembering

1. **`0034` is the third consecutive time a ruling was executed in prose and not in code** — and
   revision 4's C2 recurred verbatim one round after being closed, in the same file.
2. **A "correction" is not discharged until the script and its JSON carry it.** `1,573` had no
   producer anywhere in the repository for a full round.
3. **The strip is a usable precedent:** when a justification section has failed review repeatedly,
   cutting it and recording the absence beat repairing it a fourth time — and Red Team named that
   exit itself.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[step1-open-questions]], [[open-items-and-contradictions]], [[withdrawn-claims-register]],
[[decision-log-step18]].
