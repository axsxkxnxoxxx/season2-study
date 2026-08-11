---
name: step1-open-questions
description: The Step 1 §10.1 open questions — Q2 was decided as D14 on 2026-08-10, Q1 and Q3 remain open with their drafted defaults and recommendations
metadata:
  type: project
---

# Step 1 §10.1 — two questions still open, one decided

**Fact:** §10.1 opened with four questions. **Q4** became D9. **Q2 was decided by the Human Lead
on 2026-08-10 as D14** (decision `0003`). **Q1 and Q3 remain open**, and the Step 1 approval did
**not** close them: approval covers the drafted boundary each sits beside, not a ruling on the
alternatives.

**Why this matters:** open questions inside an approved document are easy to mistake for settled.
The document says explicitly that they are not.

**How to apply:** if a downstream step's spec depends on Q1 or Q3, name it as undecided rather
than assuming the recommendation was adopted. For Q2, the opposite: it **is** decided, and the
decision is in the file the isolated instances read.

| # | Question | Drafted default | Status |
| :--- | :--- | :--- | :--- |
| **1** | Continued boundary: S2 finale **plus** ≥90 percent, or finale alone? | Finale **and** `\|A\| ≥ ceil(0.90 × L2)` — what §7 implements | **OPEN.** Recommendation: keep finale plus 90 percent |
| **2** | How is `W` estimated when most started users have negative lags? | — | **DECIDED 2026-08-10 as D14 / `0003`:** estimate on bucket **C1 only**, apply to all shows |
| **3** | Right-censoring on `max(W, 91)`, or on `W` alone? | `max(W, 91)`, carried as `max(W, 91) + H` per D10 — §6 implements this | **OPEN.** Recommendation: keep it |
| ~~4~~ | ~~Show merges and splits~~ | — | Closed, became **D9** |

## Q1 — Continued boundary (open)

The symmetry argument from the first draft is **withdrawn**: it was false. S1 completion is
evaluated over all time and S2 completion within `W`, so the tests share arithmetic but not
quantifiers. Three grounds that do hold: finale-alone would admit the skip-to-finale viewer as
Continued, which **undercounts abandonment — the direction that flatters the study's own
headline**, and a rule should not fail toward its author's conclusion; the strict rule's cost is
*visible* as the `p = 1.0` residual reported by name at Step 10, while the lenient rule's cost is
silently absorbed into Continued; and D3 bounds the strict rule's real weakness (catching slow
finishers) with a reported number rather than an argument.

**Trigger to revisit:** a high D3 resumption share. Q1 and the value of `W` are the same problem
seen from two ends.

## Q2 — decided, and what travelled with it

**Decision:** W is estimated on **bucket C1 (all-at-once) only**, per D12, and applied to all
shows. Referred to by **bucket name, never "binge shows"** — the two isolated Step 6 instances
must select the same rows without consulting each other, and a paraphrase is where they would
diverge.

**Why:** on a C1 show premiere and finale coincide, so every lag is non-negative by construction
and the lag measures the one thing W is meant to capture. The withdrawn alternative — truncating
negative lags at zero — made W a function of the frame's cadence mix rather than of viewer
behaviour.

**Cost, stated as an assumption and not a finding:** it assumes binge viewers' delay-to-start
behaviour transfers to weekly viewers. **Two obligations travel with it, both now in
`task-sheet.md`:** Step 6 plots the C1-only and all-shows lag distributions together; Step 13
varies W over **at least** the range those two imply. Step 13 also now requires the **retained-row
count per W arm**, because the censoring rule contains W and the arms do not share a denominator.

**Residue I am still watching:** §8 of the definition was not updated and still calls the
negative-lag treatment open, and nothing specifies how negatives are handled in the **all-shows**
plot that Step 6 must now produce — which is also what defines Step 13's required range. See
[[open-items-and-contradictions]] N1.

## Q3 — right-censoring (open)

The "expected cost is zero rows" claim is **withdrawn**; it was false on the document's own
definitions. `max(W, 91)` is still recommended because the alternative computes the two headlines
on different denominators **on top of** the different origins D5 already introduces, and two
differences at once cannot be attributed. The removal count is reported unconditionally either
way with its direction named; if it is large, the right response is the limits section, not a rule
change to shrink it.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[open-items-and-contradictions]], [[decision-log-step18]].
