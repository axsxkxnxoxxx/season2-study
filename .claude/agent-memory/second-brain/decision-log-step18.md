---
name: decision-log-step18
description: Coverage map of the decision log of record in decisions/ (0001-0020), which judgments still have no file, and assembled five-field text pending handoff to the Human Lead
metadata:
  type: project
---

# Step 18 decision log — coverage map and pending text

**`decisions/` is the artifact of record. This memory is not the decision log and must not
duplicate it.** Step 18 assembles from `decisions/`. My job is coverage and consistency: which
judgments have a file, which do not, and whether the files still match the artifacts.

**Ownership:** the Human Lead writes every file in `decisions/`. I hand over assembled text and
stop. I never write there and never edit an entry — if I think one is wrong or incomplete I report
it ([[open-items-and-contradictions]] X2, X3, X4).

**Format, from `task-sheet.md` Step 18 — five fields per entry:** what was decided, what the
alternatives were, why this one, what it costs, and where the Red Team or a partner reviewer
disagreed and how it was resolved. *"This is the primary artifact. The analysis shows the work. The
log shows the judgment."*

---

## Coverage as of 2026-08-12 — `0001`–`0020`

| Files | Cover | Five-field completeness |
| :--- | :--- | :--- |
| `README.md` | Index, gate checklist, **19 open items** (1, 4, 12, 13, 14, 17 struck as closed) | n/a — index |
| `0001`–`0004` | Step 1 gate (incl. D10, D11, D12, B2 overruled); D15 endpoint; D14 W sample; 403 handling | Full |
| **`0005`–`0008`** | Step 3: stopping rule, twelve crawl constants, channel cost trade, seed source | Full, and each names the reviewer disagreement. **All four Open — awaiting ratification** |
| `0009`–`0012` | Step 4: pull order, tail cap, `pull_date` value, sweep completeness | Full. `0009`, `0010` and `0012` each record **the framing that was wrong and why**, which is unusually good for the "why this one" field |
| `0013`–`0020` | Step 2: delegation, no content filters, unaired S2, per-season network, air period, size quintile base, `pool_completers`, structural thresholds | Full |
| **`0021`** | **Step 5 gate closed.** The rule, four rulings made inside the gate, two standing rulings, four Step 14 limitations, three recorded errors, and what it unblocks | **Full, and it is the best-formed entry in the log** — it carries the four-round review history, the reasoning quoted verbatim, and the errors that entered rulings before being caught |
| **`0022`** | The two standing rulings propagated into `task-sheet.md` Steps 6 and 7 | Full. Notably records **who found it** and why the dual-implementation control could not have |
| **`0023`** | `0012` reviewed and upheld; three findings become Step 14 limitations | Full, and it does the harder thing: **states that Red Team was overruled on cost and not on merit**, so a future reader cannot infer the shape test was examined and found wanting |

**Gate checklist:** **Steps 1 and 5 closed. Steps 6, 7, 8 open.** Two of five.

**`0021` sets a bar for the three remaining gate entries.** It records not just the rule but the
rulings made *during* the gate, the standing rulings that outlive it, the limitations that travel
forward, and the errors that reached the Human Lead — including two that **entered rulings before
being caught**, with the note that the conclusions survived on better bases. That is the five-field
format working at full strength, and it is the model for Steps 6, 7 and 8.

**One structural improvement worth naming.** `0022` exists because a ruling recorded in two places
was still missing from the third. The log now carries the standing check as README item 23. **Every
remaining gate entry should end by naming what it propagated to `task-sheet.md`, or stating that it
propagated nothing.**

---

## What Steps 2–5 did well, as precedent for Step 18

Three practices worth naming because they make the five-field format easy to fill later:

1. **`0009`, `0010` and `0012` each record the instruction that was amended and why**, not just the
   final rule. `0010` states it explicitly: *"a cap defended by the wrong argument is a cap nobody
   can re-derive later."* That sentence is the "why this one" field doing its job.
2. **Red Team rounds 1–4 were transcribed to disk before the ruling that turned on them**, at the
   Human Lead's instruction, because the reviewer is review-only and writes no files. Without that,
   the D1 ruling would have been made against a conversation. **The "where a reviewer disagreed"
   field would otherwise have been unwritable for the entire Step 5 gate.**
3. **`0006` and `0008` were commissioned retrospectively** for choices nobody was obliged to record
   at the time. `0008` says why it is separate from `0006`: *"it is a design choice rather than a
   constant, and folding it into a list of numbers would bury it."*

---

## Judgments with NO file of their own — I hold the assembled text

Adopted and operative, but covered in `0001` only as "approved with the document." Each is a real
judgment with alternatives and a cost. Hand over when the Human Lead next writes to `decisions/`.

**D1 — clock start anchored on the S2 finale, not the premiere.** *Alternative:* premiere anchoring.
*Why:* Step 6 already anchors the lag on the finale; under premiere anchoring "Continued" is
unreachable inside any `W` shorter than the airing span, making the state an artifact of cadence;
and it scores a viewer who waits for a season then binges as a decliner — the exact conflation the
study exists to break. *Costs:* unequal exposure — opportunity to start S2 by `τ1` is
`airing_span + W` for weekly and `W` for binge, so **the never-started share is mechanically lower
for weekly titles by construction**, and the gap scales with season length. Paid openly: cadence
becomes a required Step 9 stratum and a mandatory Step 12 candidate flagged as the one candidate
with a known mechanical driver. *Disagreement:* none on D1 itself; its consequence became open
question 2, decided as D14 / `0003`. **New evidence 2026-08-12:** the frame is 29.9% C2 and 37.3%
C4, so the exposed population is most of it — D1's cost is not a corner case.

**Season membership by listed set, not numeric range.** *Alternative:* the range `1..F`. *Why:* the
range rule let through the exact case the gap machinery existed for. Under the set rule `D1 ⊆ E1`
and `A ⊆ E2` **by construction**. *Costs:* the Step 8 invariant "distinct episodes never exceed
season length" stops being a data check and becomes an **implementation** check. *Disagreement:*
Red Team second HOLD, F1 and F2, accepted in full. **Now vindicated on real data:** four
absolute-numbering shows in the candidate set used the same absolute numbers in history and
metadata, 100% overlap on all four, and **the withdrawn range form would have failed on all four.**

**First-pass S1 completion date, not last-observed.** *Alternative:* `max watched_at` over all S1
records. *Why:* (a) measures the wrong event and is **biased by engagement**. *Costs:* `(b) ≤ (a)`
always, so first-pass gives a **higher never-started share** — the direction that strengthens the
study's own headline, which is why the choice is defended on the merits and why **Step 13 must carry
(a) as a robustness arm** (`task-sheet.md` Step 13 now does, line 361). *Disagreement:* Red Team
pressed on whether the replacement Step 8 invariant tests anything; conceded and narrowed — the two
inequalities are vacuous, the **equality clause** does the work, and only if the check computes the
first-pass date **independently**.

**D13 — half-open UTC-instant boundaries.** *Alternatives:* `date(watched_at) ≤ T1`; a `23:59:59`
sentinel. *Why:* "on or before `T1`" admitted two faithful implementations one day apart on the
single operator that assigns every outcome state; the half-open form makes the window exactly `W`
days and makes window and horizon tile at `τ1` without gap or overlap. *Costs:* removes one calendar
day, moving the never-started share marginally **up**; named, not netted. *Disagreement:* Red Team
third HOLD, B3, accepted in full. **In live use:** Step 2's 2025-12-31 cutoff is applied as
`first_aired < 2026-01-01T00:00:00Z`, citing D13.

**D8 — never-started post-window diagnostic.** *Alternative:* report nothing for that category.
*Why:* "never" is the one word in the headline a reader takes most literally, and a pair that
started on day `W+1` is called "never." *Costs:* moves the headline **down**, which is why it
belongs. *Disagreement:* Red Team second HOLD, F3; entered as a proposal, held, adopted by the Human
Lead. **D8 later became load-bearing in a way nobody planned:** Red Team's D1 cited its existence as
proof that Step 1 §7 is a timestamp rule, which is what defeated the revision-3 principle.

**D9 — show splits as a known misclassification, with a bound.** *Why:* a split gives one ID a
complete S1 and `|A| = 0`, **fabricating a row directly into the published category**, while the
other disappears unrecorded. *Costs:* detection is imperfect and the count is a **lower bound**;
reconciliation logic stays unwritten. *Disagreement:* Red Team second HOLD, accepted. *Live caveat:*
the split mechanism is asserted, not observed.

**Liveness is a pair-level filter (scope correction).** *Why:* it was mis-scoped and would have
removed whole accounts on a test that only ever applied to one of their shows. *Costs:* none to the
definition; the cost was procedural — **the Human Lead amended `task-sheet.md` Steps 7 and 9
directly**, so a scope divergence between the two Step 7 instances is now a **bug, not a spec
ambiguity**. **This is the precedent [[open-items-and-contradictions]] X1 turns on.**

---

## Still with no decision file at all

1. **§10.1 open questions 1 and 3**, when ruled — the Continued boundary and the right-censoring
   rule. Each carries a Data Scientist recommendation and a decision from nobody.
3. **The gap hypothesis**, if and when it is assigned an owner (README items 3 and 8).
4. **Ratification of `0005`–`0008`**, which are the only Open entries in the log.
5. **Whether to resume the Step 4 pull or sample the pool down** (README items 11 and 19). Every
   frame-derived boundary moves if it resumes.
6. **Step 11's brief vs Step 14's limitation** (README item 10) — the seeding-bias diagnostic.

## One misattribution risk to keep watching

`0005` credits Engineering's HOLD with the position that *"stating plainly that the plateau would
not fire is better than manufacturing one."* That sentence is **the agent's own, pre-registered** at
`src/step3_user_discovery.py:76` **before the run**. Engineering's distinct contribution was that it
**should have gone to the Human Lead before the run**. Do not let the log credit the reviewer with
the agent's foresight, or the agent with the reviewer's objection. **The same care applies to Step
5:** revision 1 §3 already said air-date stamping was "the strongest possible 'continued' signal"
and would "inflate Continued" — revision 3 reversed it, and Red Team D1 restored it. **Red Team
recovered a position the artifact had itself held and abandoned**, which is a different contribution
from originating it, and the artifact says so.

Related: [[gate-step1-outcome-definition]], [[gate-step5-contamination]],
[[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[withdrawn-claims-register]], [[population-chain-steps-2-3-4]], [[step1-open-questions]].
