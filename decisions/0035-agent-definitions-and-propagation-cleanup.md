# Decision 0035 — The agent definition files are live spec and are amended; Step 10 receives the amendment; the propagation gaps are closed

| | |
| :--- | :--- |
| **Decision** | **The agent definition files in `.claude/agents/` are live spec, not vestigial launch briefs, and are amended to the decision log.** `task-sheet.md` Step 10 receives `0034`'s three requirements. Two propagation errors and five stale expressions are corrected. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `second-brain`'s catch-up through `0034`, findings W1–W5 |
| **Amends** | `.claude/agents/data-scientist.md`, `data-scientist-b.md`, `analytics-engineer.md`, `analytics-engineer-b.md`; `task-sheet.md` Steps 10 and 13; `decisions/README.md`; `artifacts/step1-outcome-definition.md`; `artifacts/step5-contamination-diagnostics.md`; `src/step6_completion_lag.py` |
| **Status** | Closed |

---

## 1. The agent definition files are live spec — the finding, and why it mattered now

`CLAUDE.md` says each agent's steps are written into its definition file, and to **read the task sheet
only when you need context beyond your own steps.** So the definition file is what an agent reads
first. **Ten decisions propagated to `task-sheet.md` and none of them propagated to `.claude/agents/`.**

**Step 7 is the next gate, it is a dual pair, and both halves were byte-identical in the wrong state.**
`data-scientist.md` and `data-scientist-b.md` line 14 read:

> *"Plot the distribution of gaps between consecutive **logged events per user**. Set the threshold
> **well beyond the normal gap** and state where and why. Write the resulting rule: **a user** counts as
> live if they show logged activity after clock start plus W…"*

**Every clause is withdrawn**, and the failure would not have shown up as a divergence — being
identical, both instances would have made the *same* wrong choices and the diff would have been clean:

| The file said | The rule is | Set by |
| :--- | :--- | :--- |
| gaps between **logged events** | gaps between **insertion instants**, as continuous differences | `0021` ruling 2, `0029` |
| threshold **"well beyond the normal gap"** | a **named percentile**, rounded **up** | `0024`, `0025`, `0029` |
| **a user** counts as live | **a pair** counts as live — evidence is account-wide, the test is clock-start-relative | Step 7 scope correction |

**That is the whole argument for treating these files as spec.** A dual pair whose two halves read the
same stale brief produces a clean diff and a wrong answer, and the diff is the only instrument this
study has for catching a spec defect.

## 2. What was amended in each file

**Both `data-scientist` files, identically** — verified byte-identical except the `name:` field:

- **Step 1** — marked **approved and amended**, not to be re-drafted. **Premiere anchoring removed:**
  the clock starts at `T0 = max(S2 finale air date, S1 completion date)`. Set membership for S1
  completion, canonical timestamp as the minimum `watched_at`, the half-open instant form, and
  **outcome assignment at two instants**, `τ1` and `τ2`.
- **Step 6** — marked **approved at `W = 108`**. The **"percentile where the curve flattens" is
  replaced** by the 90th percentile, continuous days, ceiling rounding, C1-only estimation. **The
  artifacts state 107 and 107.7135 and neither is the adopted value.**
- **Step 7** — rewritten entirely, per the table in §1, plus: the play-`id` calibration is a required
  input **neither instance refits**; **liveness stays anchored at `τ1`** and `τ2` plays no part
  (`0034`); and the file now states that **the threshold percentile is unruled and Step 7 must not
  begin** until the Human Lead rules.
- **Step 9** — the bound is computed **on pairs, not users**; D4 and D9 reported alongside; the 91-day
  arm's separate origin (D5) named.
- **Step 10** — `0034`'s three requirements, as in §3 below.
- **Step 13** — arms are the 46–107 span **plus 150 and 213** (`0027`); hold `H` constant; **D3′ runs at
  every arm**; per-air-period retained counts at every arm (`0033`).

**Both `analytics-engineer` files, identically** — verified byte-identical except `name:`:

- **Step 0** — **the "on a 403, hard stop and report" rule is replaced** by the classified rule
  `CLAUDE.md` has carried since 2026-08-10: skip on a user resource with two circuit breakers, hard
  stop otherwise, ambiguity resolves strict, `X-Private-User` is **positive confirmation only**, and a
  skipped user is `access_denied` and **not** a user with no history.
- **Steps 3, 4, 5** — marked complete or approved, with the operative facts a later step needs: read
  failures from the ledger not the failure log, read spend from `api_requests.ndjson`, and
  **`first_s2_lag_days` is a backfill measure, not a start-time lag**.
- **Step 8** — **"a fixed documented order" replaced by the exact `0029` order**; outcome assignment at
  two instants; the **`A ⊆ A_H`** invariant; and **the vacuous invariant removed** — "no clock start
  precedes an S2 premiere" catches nothing under a finale-anchored clock, and is replaced by the
  three-part clock-start check that computes the S1 completion date independently.

**No other agent file carried this class of staleness.** `red-team`, `second-brain` and the five
reviewer files were checked and are clean.

## 3. Step 10 receives `0034`

`0034` §6.2 required three things of Step 10. All three were in `artifacts/step1-outcome-definition.md`
and **none was in `task-sheet.md`.** Step 10 is Chained and single-implementation, so there is no diff
to catch it — this is the plain omission `0028` was written for. Added:

- **`p` is read on `A_H` in the rank form**, `p = |{ e ∈ E2 : e ≤ m_H }| / L2` with `m_H = max(A_H)`.
  **`p = m_H / L2` is not the rule** and must not be reinstated.
- **The direction must be named:** the 2,246 pairs the amendment moves out of Started-and-left are the
  ones that got furthest, so **the amendment makes abandonment look earlier on a published chart.**
- **The `p = 1.0` residual is re-reported, not carried over** — its size changes under `A_H`.

## 4. Two propagation errors, and five stale expressions

**A section mark rendered as a step number, in the decision log of record.** `decisions/README.md`
items 40 and 41 and `task-sheet.md` Step 14 said **"Step 2's marginal-lag distribution"** and **"Step
2's marginal p90 of 100.39."** The source is **§2 of the amendment**, produced by
`src/step6_completion_lag.py`. **Step 2 is the frame ledger and contains no lag distribution.**
Corrected in all three places.

**Five stale expressions whose conclusions survive**, corrected in place rather than left to be
rediscovered:

| Where | What was stale | Why the conclusion survives |
| :--- | :--- | :--- |
| `step1-outcome-definition.md` §7, `L2 = 1` | the degeneracy stated on `A` at `τ1` | `E2 = {F2}` collapses all three conjuncts at **whichever** bound is used |
| `step1-outcome-definition.md` §5, unaired episodes | `F2 ∈ A` unsatisfiable | equally true of `F2 ∈ A_H` |
| `step5-contamination-diagnostics.md` §4, air-date stamping | the argument runs on `A` | **a fortiori**: `A ⊆ A_H`, so both conjuncts carry over |
| `task-sheet.md` Step 13 and `step1-outcome-definition.md` D10 | "D3 and D8 are not comparable" | the requirement is unchanged and now governs **D3′** |
| `src/step6_completion_lag.py` docstring | states the pre-amendment `τ1` rule as current | **it is the live provenance for §2's three rows**, so it is retained as written with the supersession named — its premise is exactly the thing this script's own finding changed |

## 5. Scope

- **No number, threshold or population moves.** Every change is a specification correction or a
  provenance label. Zero API calls; nothing was re-run.
- **The dual-pair guarantee is restored.** Both halves of each pair are byte-identical except the
  `name:` field, verified by `diff`.
- **Step 7 still does not launch.** Its threshold percentile is proposed at the 99th and remains
  **unruled**, and both definition files now say so.
