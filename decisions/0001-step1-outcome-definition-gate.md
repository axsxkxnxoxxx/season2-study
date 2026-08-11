# Decision 0001 — Step 1: Outcome definition (GATE)

| | |
| :--- | :--- |
| **Decision** | Step 1, the outcome definition, is **APPROVED** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-10 |
| **Gate** | 1 of 5. The first to close. |
| **Artifact** | `artifacts/step1-outcome-definition.md` |
| **Status** | Closed. Steps downstream of the Step 1 gate are unblocked. Gates at Steps 5, 6, 7 and 8 are unaffected and still bind. |

This file is the decision log entry. `artifacts/step1-outcome-definition.md` is the operative
definition and governs wherever the two differ.

---

## What was decided

**Step 1 is approved as written.** Approval covers the document as a whole, including the items
that entered it as proposals during the three revisions: **D8, D9** (Section 10.0b) and **D10
through D13** (Section 10.0c). They were drafted by the Data Scientist under authorization to
revise, held as proposals while the gate was open, and are adopted by this approval.

Four items were decided by name.

### 1. `H = 91 days` — adopted (D10)

The post-window horizon. Right-censoring is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, and the
D3 and D8 diagnostics measure over `[τ1, τ1 + H)`.

**Why it exists:** the previous draft asserted that right-censoring at `T0 + max(W, 91)`
guaranteed 91 days of post-window observation. That is false by subtraction — the window closes
at `T1 = T0 + W`, so the guarantee is `max(0, 91 − W)` days: 61 at `W = 30`, **zero** at
`W ≥ 91`. Without a fixed horizon, D3 and D8 were not rates but exposure-weighted mixtures
whose weight was show recency, understating later-starting for recent titles.

**Cost:** the most recent `H` days of S1 completers are censored out, which moves the headline
**up**.

### 2. D12 cadence thresholds — adopted as proposed

Five exhaustive buckets `C0`–`C4`, numeric thresholds, first-match ordering. Replaces "on the
order of `(L2 − 1) × 7` days" and "near zero", which were not thresholds and left hiatus,
two-episode-premiere and multi-drop seasons unassigned in a required stratum.

The classifier gates the Step 6 estimation sample, a required Step 9 stratum and a mandatory
Step 12 candidate. The count of shows near a boundary remains a required output — it is what
tells anyone whether the convention was load-bearing.

### 3. `pull_date` — adopted in **form**, value **deliberately deferred** (D11)

A single global frozen cutoff, not per-user fetch date. `τ_pull := ⟦pull_date⟧`; records at or
after it are discarded. Constrained to be no later than the earliest per-user fetch date.

**The value is deferred until Step 4's schedule is known. This is a deferral, not an omission
or an oversight:** the constraint cannot be honoured by a value chosen before the pull is
scheduled. Setting it is a Human Lead act and no agent performs it.

**This is the one outstanding item from Step 1.** Any step that right-censors, or that computes
D3, D8 or D9, is blocked on that value — not on this gate.

### 4. Red Team finding B2 — **overruled**, recorded as accepted risk

**Objection:** a pair that watched all of S2 inside `W` and then left Trakt is excluded by the
Step 7 liveness filter as not-live, and the Step 9 bound then relabels every inactivity-excluded
pair "never started" — so a demonstrable continuer is counted as a decliner, and the filter
removes Continued pairs preferentially, shifting the population's composition.

**Ruling:** overruled. The liveness bound is deliberately worst-case. It is not an estimate and
is not presented as one; it is the ceiling of the reported floor-and-ceiling pair, and its
function is to answer "what if every excluded pair were a decliner." A bound that quietly
reclassified the pairs it could explain away would no longer be a bound.

The inflation is real, runs in the direction the bound is built to run, and is stated wherever
the bound appears.

---

## How the gate was reached

1. Drafted, then revised against Human Lead decisions **D1–D7**.
2. **Red Team returned HOLD three times.** Each revision was authorized in response.
   - **Second HOLD** — three blocking, five secondary. The structural fix was in Sections 3, 4
     and 7: season membership redefined by the season's **listed episode-number set `E`** rather
     than the numeric range `1..F`. That single change makes `|D1| ≤ L1`, `|A| ≤ L2` and
     `p ∈ (0, 1]` true **by construction** rather than by assertion. Added **D8** (post-window
     diagnostic for the "Never started" category — the one the study is named after) and **D9**
     (show splits as a known misclassification with a bound).
   - **Third HOLD** — four blocking, all about objects the document named but never made
     operational. Became **D10**–**D13**.
3. Between the second and third HOLDs, the Analytics Engineer closed the Section 3.3
   precondition with a live probe: `artifacts/step0-episode-listing-endpoint-probe.md`. The
   episode-listing endpoint authenticates on Client ID alone and supplies `E`, `L` and `F` from
   one payload. Recommended variant `GET /shows/:id/seasons?extended=episodes,full`.
4. The Human Lead amended `task-sheet.md` Steps 7 and 9 to **pair-level** liveness scoping,
   closing a dependency Step 1 had flagged but could not resolve in its own file.
5. Approved 2026-08-10.

**No agent recorded its own approval, and no agent adopted its own proposal, at any point.**

---

## What this decision does NOT close

- **`pull_date` has no value.** See above. The one outstanding item.
- **Open questions 1 and 3** in Section 10.1 remain open. Approval covers the **drafted
  boundary** each sits next to; it is not a ruling on the alternatives. Question 2 is decided
  separately (`0003`), question 4 was resolved as D9.
- **The gap hypothesis is untested.** The probe covered one show with contiguous numbering.
  Whether Trakt represents a numbering gap by **omitting** the number or by **listing a
  placeholder** is unknown. Section 3 must not be read as "gaps handled." Settling it needs a
  show with a known gap, at the point where `E` is first pulled at scale — which is not yet
  assigned to a step.
- **A provenance gap on a public artifact.** Two figures cited in Sections 2.1 and 5 — a 28
  percent play-record inflation figure and a six-week S1/S2 overlap — are numerically correct
  but trace only to an undocumented run tagged `step0-history-probe` in a machine-local log.
  There is no run record and no probe script in `src/`, unlike the other two Step 0 probes, so
  the run is not reproducible from the repo. Neither rule depends on the figure. Open.

---

## Standing record

The document carries a table of **six claims withdrawn as false** across the three revisions,
plus this accepted risk. That table is the study's record of what it has already gotten wrong
and is not to be pruned.
