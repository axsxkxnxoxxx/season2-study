---
name: gate-step1-outcome-definition
description: Full arc of the Step 1 outcome-definition gate — three Red Team HOLDs, four revisions, what approval on 2026-08-10 did and did not cover, and the post-approval addendum that did not reopen it
metadata:
  type: project
---

# Step 1 gate — APPROVED 2026-08-10. First of five gates to close.

**Fact:** the Step 1 outcome definition was approved in writing by the Human Lead in session
on 2026-08-10. `task-sheet.md` "Gate summary" carries the checked box. The document is
`artifacts/step1-outcome-definition.md` and it carries the approval record at its head.

**Why this arc is worth carrying:** the gate took four drafts and three Red Team HOLDs, and
the interesting part is not the final text — that is in the repo — but *what the process
proved about how this study fails*. It fails by naming objects it never makes operational,
and by asserting properties that do not follow from the definitions given. Eleven such claims
were caught and withdrawn or corrected. See [[withdrawn-claims-register]].

**How to apply:** treat Step 1 as settled and downstream of it as unblocked. Do **not** treat
the remaining open questions in §10.1 — **1 and 3** — or `pull_date`, as settled by it. The four remaining gates
(5, 6, 7, 8) are unaffected and still bind.

## The arc, in order

1. Drafted, then revised against Human Lead decisions **D1–D7**.
2. **First HOLD** → authorized revision.
3. **Second HOLD** — three blocking, five secondary. Structural fix in §§3, 4, 7: season membership redefined by the **listed episode-number set `E`** rather than the numeric range `1..F`. That one change makes `|D1| ≤ L1`, `|A| ≤ L2` and `p ∈ (0, 1]` true **by construction rather than by assertion**. Added **D8** (never-started post-window diagnostic) and **D9** (show splits as a known misclassification with a bound).
4. Between the second and third HOLDs, the Analytics Engineer ran a live probe closing the §3.3 precondition — `artifacts/step0-episode-listing-endpoint-probe.md`. Episode listing authenticates on Client ID alone and supplies `E`, `L`, `F` from one payload. Recommended variant `GET /shows/:id/seasons?extended=episodes,full`.
5. **Third HOLD** — four blocking, all about objects the document named but never made operational: **D10** (fixed horizon `H`, replacing a guarantee that was false by subtraction), **D11** (`pull_date` as a single global frozen cutoff, not per-user fetch date), **D12** (five-bucket numeric cadence classifier replacing "on the order of" and "near zero"), **D13** (half-open UTC-instant boundaries replacing the one-day-ambiguous "on or before `T1`").
6. The Human Lead amended `task-sheet.md` Steps 7 and 9 to **pair-level liveness scoping**, closing a dependency Step 1 had flagged but could not resolve from inside its own file. Verified: the task sheet now reads "user-show pair" at Step 7 and "inactivity-excluded **pair**" at Step 9.
7. **Approval, 2026-08-10.**

## What approval covered, precisely

| Item | Disposition at approval |
| :--- | :--- |
| `H = 91 days` (D10) | Adopted **by name** |
| D12 cadence thresholds | Adopted **by name**, as proposed |
| `pull_date` (D11) | Adopted in **form only**. Value **deliberately deferred** to Step 4's schedule |
| D8, D9, D13 | Adopted **with the document** |
| Red Team B2 | **Overruled**, recorded as accepted risk |
| §10.1 open questions 1, 2, 3 | **Not closed by approval.** It covers the drafted boundary each sits beside, not a ruling on the alternatives. **Q2 was decided separately later the same day** as D14 / decision `0003` |

## After approval, same day — what moved without reopening the gate

| Event | Effect on the gate |
| :--- | :--- |
| **D15 / `0002`** — Step 4 source is `GET /users/:id/history` | None. Closes a Step 0 blocker; Step 1 §0 already presupposed it |
| **D14 / `0003`** — W estimated on bucket C1 only | Closes §10.1 Q2. Two obligations written into `task-sheet.md` Steps 6 and 13 |
| **Provenance closed** — `artifacts/step0-history-endpoint-probe.md` | None. Both cited figures reproduce at zero live calls |
| **Section 5 post-approval addendum** | **None. Evidence only.** The S1/S2 overlap inverts under the §2.2 dedup — 41.31 days of overlap under definition (a), **360.73 days of separation** under (b) — so it is a rewatch artifact and (a) yields a **negative clock start on a real profile**. Strengthens the existing warrant for first-pass completion and for D2. No rule, threshold, definition or required output changed; **the gate remains APPROVED** |

**The standing rule this established, and it generalises:** an edit that changes a **rule**
reopens the gate; an edit that adds **evidence** for a rule already adopted does not. It is stated
in the approval record itself. Apply it at the remaining four gates.

**The `pull_date` deferral is a decision, not an omission.** The reason is structural: the
constraint `pull_date ≤ earliest per-user fetch date` cannot be honoured by a value chosen
before the pull is scheduled. Recorded that way at the head of the document and again in §11.

## The B2 overrule

**Objection (Red Team):** the liveness bound is inflated. A pair that binged all of S2 inside
`W` and then left Trakt is excluded by the Step 7 liveness filter as not-live, and the Step 9
bound then relabels every inactivity-excluded pair "never started" — so a demonstrable
continuer is counted as a decliner.

**Ruling (Human Lead): overruled, do not fix.** The bound is deliberately worst-case. It is
not an estimate and is not presented as one; it is the ceiling of the reported
floor-and-ceiling pair, and its function is to answer "what if every excluded pair were a
decliner." **A bound that reclassified the pairs it could explain away would no longer be a
bound.** The inflation is real, runs in the direction the bound is built to run, and is
stated wherever the bound appears.

**Why this ruling is load-bearing downstream:** Step 9 reports bounds in **both** directions —
liveness bound up; D4, D9 and the dropped-S2-evidence count down. If anyone later proposes
"fixing" the liveness bound, this is settled and the reasoning is on the record.

## Process property the study should keep

No agent adopted its own proposal at any point. D8–D13 originate as Red Team findings,
drafted into the document by the Data Scientist under authorization to revise, held as
proposals, adopted only by the Human Lead. The provenance is kept in §§10.0b and 10.0c
deliberately. Worth preserving as a pattern at the remaining four gates.

Related: [[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[decision-log-step18]], [[withdrawn-claims-register]].
