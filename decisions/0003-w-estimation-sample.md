# Decision 0003 — Estimating W: the estimation sample (Step 1 open question 2)

| | |
| :--- | :--- |
| **Decision** | **W is estimated on bucket C1 (all-at-once) shows only, per the D12 classifier, and the resulting W is applied to all shows** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-10 |
| **Closes** | Open question 2 in `artifacts/step1-outcome-definition.md` §10.1 |
| **Recorded as** | D14 in §10.0 of the same document |
| **Status** | Closed. The **value** of W is Step 6's and remains a gate. |

This decision fixes the **estimation sample**, not the number.

---

## What was decided

- **C1 is the estimation sample. C0, C2, C3 and C4 are not.**
- **The resulting W is applied to all shows.** Estimation sample and application population
  differ deliberately.
- **Refer to it by bucket name, never as "binge shows."** The two isolated Step 6 instances must
  select the same rows from the same frame without consulting each other, and a paraphrase is
  exactly where they would diverge.

## Why

On a C1 show the premiere and finale coincide, so `T0` is the moment the whole season became
available. Every lag is **non-negative by construction**, and the lag measures the one thing W
is meant to capture: how long a viewer takes to start something already sitting there.

**The alternative was withdrawn as indefensible.** An earlier draft proposed truncating negative
lags at zero across all shows. Truncation maps every live weekly viewer to a point mass at zero,
and the height of that mass is set by how many weekly shows the frame happens to contain — so W
would become an artifact of the frame's cadence composition rather than a fact about viewers.
Change the show mix, change W, with no change in behaviour. Step 6's approval bar is that the
number is defensible out loud, and that version was not.

This decision also closes the negative-lag question that travelled with it: within the C1
estimation sample there are no negative lags to truncate.

## What it costs, stated plainly

**It assumes the delay-to-start behaviour of binge viewers transfers to weekly viewers. That is
an assumption, not a finding**, and it is the price of a clean estimation sample.

Two obligations travel with the decision. Both are written into `task-sheet.md` and are
**required, not suggested**:

1. **Step 6 plots the C1-only and the all-shows lag distributions together**, so a reader can see
   how far the transfer assumption is being stretched rather than taking it on trust.
2. **Step 13 varies W over at least the range those two distributions imply.** That gap *is* the
   size of the assumption, so it is the range that tests it.

`task-sheet.md` Step 13 also now requires the **retained-row count per W arm**: the
right-censoring rule contains W, so each arm re-censors the population and the arms do **not**
share a denominator.

Whether the C1 sample is large enough to support the chosen percentile is a Step 6 question with
the data in hand, not a Step 1 question. `task-sheet.md` Step 6 requires that answer be stated.

## Addendum, 2026-08-10 — the negative mass in the all-shows plot

**D14 removes negatives from the estimation sample only.** The all-shows plot required above
still carries them, and for a weekly show the negative mass is most of the started population
rather than a tail. Step 6 is a **dual-implementation gate** and Step 13's tested range is
derived from that plot, so two instances handling the negatives differently would diverge and
the divergence would propagate into the tested range. A rule was therefore added to
`task-sheet.md` Step 6:

- **Plot the all-shows distribution signed and untruncated.** No truncation at zero, no clipping,
  no absolute values, no dropping of negative rows — truncation is the approach this decision
  already withdrew as indefensible.
- **Never read W, or the percentile that sets W, off the all-shows curve.** W comes off the C1
  curve. The all-shows curve is descriptive.
- **Report the negative mass as a count and a share of the started population, split by all five
  D12 buckets** — the split is what shows it is a cadence artifact rather than viewer behaviour.
- **Derive Step 13's range deterministically:** take the percentile used to set W on C1, read it
  on both curves, report both values. That interval is Step 13's minimum range. Stating the
  percentile once and reading it on both curves is what stops two instances producing different
  ranges.

This is Step 6 spec, not a change to D14. `artifacts/step1-outcome-definition.md` §8 records that
the gap was real and takes no position on the rule.

## Files reconciled

`task-sheet.md` Step 6 and Step 13, and `artifacts/step1-outcome-definition.md` §9, §10.0 (D14)
and §10.1 question 2, now agree. Step 6's instances receive this from `task-sheet.md` — the file
they actually read — rather than only from the definition. The §10.1 reasoning is retained,
marked as decided, because it is the warrant.
