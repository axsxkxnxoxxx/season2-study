---
name: step1-open-questions
description: The three §10.1 open questions the Step 1 approval did NOT close, each with its drafted default, its recommendation, and which downstream step it blocks
metadata:
  type: project
---

# The three open questions Step 1 approval did not close

**Fact:** `artifacts/step1-outcome-definition.md` §10.1 carries three open questions. The
approval on 2026-08-10 **covers the drafted boundary each question sits beside — it is not a
ruling on the alternatives.** Each carries a recommendation from the Data Scientist and a
decision from nobody. Until the Human Lead decides, the drafted boundary is what the document
says and what any implementation follows.

**Why this matters:** these are easy to mistake for settled, because they sit inside an
approved document. The document says explicitly that they are not. Two of the three touch
gates that have not run.

**How to apply:** if a downstream step's spec appears to depend on one of these, say so and
name it as undecided rather than assuming the recommendation was adopted.

| # | Question | Drafted default | Recommendation | Blocks |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Continued boundary: S2 finale **plus** ≥90 percent, or finale alone? | Finale **and** `\|A\| ≥ ceil(0.90 × L2)` — this is what §7 implements | Keep finale plus 90 percent | Nothing immediately; interacts with D3 |
| **2** | How is `W` estimated when most started users have negative lags? | **None. There is no drafted default in the body** — §8 says the treatment "stays open" | Estimate on **bucket C1 (all-at-once) only**, then apply to all shows | **Step 6, a dual-implementation gate** |
| **3** | Right-censoring on `max(W, 91)`, or on `W` alone? | `max(W, 91)`, now carried as `max(W, 91) + H` per D10 — §6 implements this | Keep `max(W, 91) + H` | Step 8, mildly |

*(A fourth question — Trakt show merges and splits — was closed and became D9.)*

## Q1 — Continued boundary

The symmetry argument used in the first draft is **withdrawn**: it was false. S1 completion is
evaluated over all time and S2 completion within `W`, so the tests share arithmetic but not
quantifiers. Three grounds that do hold: finale-alone would admit the skip-to-finale viewer as
Continued, which **undercounts abandonment — the direction that flatters the study's own
headline**, and a rule should not fail toward its author's conclusion; the strict rule's cost
is *visible* as the `p = 1.0` residual reported by name at Step 10, whereas the lenient rule's
cost is silently absorbed into Continued; and D3 bounds the strict rule's real weakness
(catching slow finishers) with a reported number rather than an argument.

**Trigger to revisit:** a high D3 resumption share. Q1 and the value of `W` are the same
problem seen from two ends.

## Q2 — the Step 6 estimation sample. This is the urgent one.

The truncate-at-zero recommendation from an earlier draft is **withdrawn**: truncation maps
every live weekly viewer to a point mass at zero whose height is set by how many weekly shows
the frame happens to contain, so `W` would become an artifact of the frame's cadence
composition. Change the show mix, change `W`, with no change in behaviour. Not defensible out
loud, which is the bar Step 6 has to clear.

The recommendation is stated as a **bucket name (C1)** rather than as the words "binge shows"
precisely so the two isolated Step 6 instances select the same rows without consulting each
other.

**What it would cost if adopted:** it assumes the delay-to-start behaviour of binge viewers
transfers to weekly viewers — an assumption, not a finding. Two things should accompany it: the
C1-only and all-shows lag distributions plotted together, and a Step 13 arm over the range the
two imply. Whether C1 is large enough to support the percentile is Step 6's question with data
in hand.

**Why it is urgent:** `task-sheet.md` Step 6 — which is what the two isolated instances
actually read — specifies all shows, not C1-only. See [[open-items-and-contradictions]] C5.

## Q3 — right-censoring

The "expected cost is zero rows" claim is **withdrawn**; it was false on the document's own
definitions. `max(W, 91)` is still recommended because the alternative computes the two
headlines on different denominators **on top of** the different origins D5 already introduces,
and two differences at once cannot be attributed. The removal count is reported unconditionally
either way with its direction named; if it is large, the right response is the limits section,
not a rule change to shrink it.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[open-items-and-contradictions]], [[decision-log-step18]].
