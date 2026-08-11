---
name: decision-log-step18
description: Coverage map of the decision log of record in decisions/, the five-field entries it does not yet carry, and assembled text pending handoff to the Human Lead
metadata:
  type: project
---

# Step 18 decision log — coverage map and pending text

**`decisions/` is the artifact of record. This memory is not the decision log and must not
duplicate it.** Step 18 assembles from `decisions/`. My job is coverage and consistency: which
judgments have a file, which do not, and whether the files still match the artifacts.

**Ownership:** the Human Lead writes every file in `decisions/`. I hand over assembled text and
stop. I never write there and never edit an entry there — if I think one is wrong or incomplete
I report it (see [[open-items-and-contradictions]] N3, N5).

**Format, from `task-sheet.md` Step 18 — five fields per entry:** what was decided, what the
alternatives were, why this one, what it costs, and where the Red Team or a partner reviewer
disagreed and how it was resolved. "This is the primary artifact. The analysis shows the work.
The log shows the judgment."

---

## What `decisions/` holds, as of 2026-08-11

| File | Covers | Five-field completeness |
| :--- | :--- | :--- |
| `README.md` | Index, gate checklist, nine open items carried forward (item 4 struck as closed) | n/a — index |
| `0001-step1-outcome-definition-gate.md` | The Step 1 gate as a whole; **D10** `H = 91` by name, **D12** thresholds by name, **D11** `pull_date` in form with value deferred, **B2 overruled** | Full on the gate and on those four |
| `0002-step4-history-endpoint.md` | **D15** — `GET /users/:id/history`, unfiltered, one sweep per user | Full |
| `0003-w-estimation-sample.md` | **D14** — W estimated on bucket C1 only, applied to all shows | Full |
| `0004-403-handling.md` | A 403 on a user resource skips that user, bounded by two circuit breakers; any other 403 hard stops; ambiguity resolves strict. Amends `CLAUDE.md` | Full, including where it misfires in both directions |

**Gate checklist:** Step 1 closed. Steps 5, 6, 7, 8 open. Consistent across `decisions/README.md`
and `task-sheet.md` "Gate summary". Verified.

---

## Step 3 — no decision file, and why that is right but incomplete

Step 3 is **Chained with a Human Lead checkpoint**, not a gate. `CLAUDE.md` requires a decision
file only where the Human Lead decides; Step 3's four open positions (§9 of the write-up) are
undecided, so there is nothing yet to record. **Producing no decision file was correct.**

What is incomplete is the other direction. Step 3 **already took** decisions that have alternatives,
costs and a named reviewer disagreement, and they live only inside a write-up. Step 18's format
exists for exactly these. Assembled below; the Human Lead decides whether any of it ever becomes a
file.

**Substituting the stopping rule.** *Decided:* stop on `TARGET_USABLE = 4000`.
*Alternative:* the rule `task-sheet.md` Step 3 actually names — "run until usable-user yield
plateaus" — which never fired and finished at **0.314 of peak against a 0.20 trigger**.
*Why:* the target was reached and the budget was not exhausted; continuing had no stated stopping
condition. *Costs:* the pool is a **convenience sample, not a saturated one**. The frontier grew
monotonically 496 → 2,970 and never emptied in 36 rounds; depth 3 was never reached; only 432 of
5,694 users were ever expanded. Reachable users were left undiscovered in a quantity comparable to
the pool itself, so no claim about "the reachable Trakt population" is available — only about
4,088 sampled users. *Disagreement:* Engineering returned **HOLD** on the crawl code before
completion; six defects were closed, round metrics backfilled by offline replay at zero live calls
(0 mismatches over 36 rounds × 12 fields), and the edge list — previously a **spanning tree**,
acyclic by construction and therefore unable to answer Step 11's clique question at all — was
rebuilt. Resolved before the write-up. *Live caveat:* the rebuilt edge list is reported with two
different pair counts in two public artifacts ([[open-items-and-contradictions]] S3).

**Eleven crawl constants set inside a chained step.** *Decided:* `TARGET_USABLE`,
`MIN_EPISODES_USABLE = 10`, the 6,500 budget, the three plateau parameters, 300 seeds, depth 3,
100 neighbours, and the per-round expansion/list/screen caps — full table in
[[glossary-terms-and-thresholds]]. *Alternative:* none stated. *Why:* not recorded anywhere.
*Costs:* `MIN_EPISODES_USABLE = 10` is the one the write-up itself flags — it makes "4,088 usable"
a weak sufficiency claim, and it removed **232** screened accounts, not the 6 the funnel prints.
*Disagreement:* none recorded. The Human Lead's own established pattern is that a threshold two
isolated instances must obey goes into `task-sheet.md`; these bind no isolated instance, but they
bind every downstream number.

**Spending 89 % of discovery calls on Channel A for 61 % of the users.** *Decided:* 864 Channel A
calls to 108 Channel B, at **5× the cost per user** (3.6 vs 18.0 users/call). *Alternative:*
weighting toward B. *Why:* the write-up's own reading — "defensible if the reason is arm
independence for Step 11 … but the trade was never stated, and on cost alone it is the opposite of
what one would choose." *Costs:* Channel B is now **exhausted** (list dedup 0.20 → 0.74–0.89 from
round 25, new eligible down to 6–24/round) — the only genuine exhaustion signal in the run — so the
cheap channel is gone and the expensive one is hub-luck, swinging 0.04 to 15.08 per call with no
trend. *Disagreement:* none recorded; the write-up raises it against itself.

**Four positions explicitly NOT taken** — §9, and they are the Human Lead's at the checkpoint:
Step 4's ~23-hour cost; Step 11 diagnostic vs Step 14 statement; population claim vs sampled-users
claim; and whether sufficiency should be expressed in analysis rows rather than usable accounts.
Whichever way each goes, each is a five-field entry.

---

## Judgments with NO file of their own — I hold the assembled text

These are adopted and operative but are covered in `0001` only as "approved with the document".
Each is a real judgment with alternatives and a cost, so each needs its own Step 18 entry. Hand
these over when the Human Lead next writes to `decisions/`.

**D1 — clock start anchored on the S2 finale, not the premiere.**
*Decided:* `T0 = max(S2_finale_air_date, first-pass S1_completion_date)`, Human Lead.
*Alternative:* premiere anchoring.
*Why:* Step 6 already anchors the lag on the finale, so premiere anchoring would derive W on one
origin and apply it on another; under premiere anchoring "Continued" is unreachable inside any W
shorter than the airing span (~84 days for a 13-episode weekly season), making the state an
artifact of cadence; and it scores a viewer who waits for a full season then binges as a decliner,
collapsing "declined" and "waiting to binge" — the exact conflation the study exists to break.
*Costs:* unequal exposure. Opportunity to start S2 by `τ1` is `airing_span + W` for weekly and `W`
for binge, so **the never-started share is mechanically lower for weekly titles by construction**,
and the gap scales with season length. Paid openly: cadence becomes a required Step 9 stratum
across all five D12 buckets and a mandatory Step 12 candidate flagged as the one candidate with a
known mechanical driver. Binge shows are unaffected.
*Disagreement:* no Red Team objection to D1 itself. Its consequence became open question 2, since
decided as D14 / `0003`.

**Season membership by listed set, not numeric range.**
*Decided:* an episode counts toward a season iff its `number` ∈ that season's listed set `E`;
`L := |E|`, `F := max(E)`, all from one payload; `F := L` forbidden.
*Alternative:* the previous rule, membership by the range `1..F`.
*Why:* the range rule let through exactly the case the gap machinery existed for — an episode
numbered inside `1..F` but absent from `E` passed all three drop tests. `|D1|` and `|A|` could
exceed `L1`/`L2`, and `m = max(A)` need not have been listed, so rank-based `p` could return 0,
outside its own stated range. Under the set rule `D1 ⊆ E1` and `A ⊆ E2` **by construction**.
*Costs:* the Step 8 invariant "distinct episodes never exceed season length" stops being a data
check and becomes an **implementation** check. Kept and relabelled. The real data check is the
drop count.
*Disagreement:* Red Team second HOLD, findings F1 and F2. Accepted in full. Two prior claims
withdrawn as false in the process.

**First-pass S1 completion date, not last-observed.**
*Decided:* the earliest date at which the §4 test is satisfied, by forward walk over distinct
episodes.
*Alternative:* (a) `max watched_at` over all S1 records.
*Why:* (a) measures the wrong event — the question is when the choice to continue became
available, not when a rewatch happened — and it is **biased by engagement**: the heavier the
rewatcher, the later the clock starts and the more time granted to start S2.
*Costs:* `(b) ≤ (a)` always, so first-pass gives an earlier clock start and therefore a **higher
never-started share** — the direction that strengthens the study's own headline. Mitigations: the
choice is defended on the merits, not on the result, and **Step 13 must carry (a) as a robustness
arm** (which `task-sheet.md` Step 13 still does not name — [[open-items-and-contradictions]] O3).
*Disagreement:* Red Team pressed on whether the replacement Step 8 invariant tests anything.
Conceded and narrowed: the two inequalities are vacuous, the **equality clause** does the work,
and only if the check computes the first-pass date **independently**. The real test is D2, not the
invariant.
*Post-approval:* strengthened 2026-08-10 by observed evidence — see the pending addendum below.

**D13 — half-open UTC-instant boundaries.** Adopted with the document; `0001` does not break it
out. *Decided:* every date bound expands to a UTC midnight instant; every membership test is
half-open, closed left, open right; the in-window test is `watched_at < τ1` and nothing else.
*Alternatives:* `date(watched_at) ≤ T1`; a `23:59:59` sentinel. *Why:* "on or before `T1`"
admitted two faithful implementations one day apart on the single operator that assigns every
outcome state and feeds the Step 8 and Step 9 diffs; the half-open form makes the window exactly
`W` days and makes window and horizon tile at `τ1` without gap or overlap, which matters because
D3 and D8 are counts of events just past that boundary; a sentinel reintroduces the ambiguity at
sub-second precision, which Trakt timestamps carry. *Costs:* removes one calendar day, moving the
never-started share marginally **up**; named, not netted against the two opposing one-day effects.
*Disagreement:* Red Team third HOLD, B3. Accepted in full.

**D8 — never-started post-window diagnostic.** *Decided:* for pairs scored Never started at `τ1`,
report count and share with any distinct S2 episode in `[τ1, τ1 + H×24h)`, and the count and share
meeting the Continued condition over that horizon. Diagnostic only; no pair moves state.
*Alternative:* report nothing for that category, as the prior draft did. *Why:* "never" is the one
word in the headline a reader takes most literally, and a pair that started on day `W+1` is called
"never"; it is the same query as D3 with the state filter changed. *Costs:* it moves the headline
**down**, which is why it belongs. *Disagreement:* Red Team second HOLD, F3. Accepted; entered as
a proposal, held, adopted by the Human Lead — not self-adopted.

**D9 — show splits as a known misclassification, with a bound.** *Decided:* Step 8 reports both
halves; Step 9 reports the bound alongside the liveness bound and D4. *Alternative:* the prior
framing — a counting nuisance, count and build nothing. *Why:* a split gives `(user, ID_A)` a
complete S1 and `|A| = 0`, **fabricating a row directly into the published category**, while
`(user, ID_B)` fails S1 completion and disappears unrecorded. Structurally identical to D4, so it
gets D4's treatment. *Costs:* detection is imperfect and the count is a **lower bound**, stated
wherever it appears; reconciliation logic stays unwritten — count first, reconcile only if the
count justifies it. *Disagreement:* Red Team second HOLD, secondary finding 1. Accepted; prior
open question 4 closed and replaced. *Live caveat:* the split mechanism is asserted, not observed
— [[open-items-and-contradictions]] N4.

**Liveness is a pair-level filter (scope correction).** *Decided:* evidence account-wide, test
`τ1`-relative and `τ1` pair-specific, so the filter is pair-level; dropping a user wholesale is
forbidden; the Step 9 bound is over inactivity-excluded **pairs**. *Alternative:* the prior
reading, "a statement about the account", which appeared in three places across two drafts. *Why:*
it was simply mis-scoped and would have removed whole accounts on a test that only ever applied to
one of their shows. *Costs:* none to the definition; the cost was procedural — Step 1 could not fix
it alone because the isolated Step 7 instances read `task-sheet.md`. **The Human Lead amended
`task-sheet.md` Steps 7 and 9 directly.** Consequence: a scope divergence between the two Step 7
instances is now a **bug, not a spec ambiguity**. *Disagreement:* raised in review, accepted,
closed in the file the implementers read. Step 1 had earlier asserted this as fact while the task
sheet still said "user"; that assertion was unbacked, was withdrawn, and was restated only after
the file changed.

---

## PENDING — assembled text for a post-approval addendum to `0001`

Hand to the Human Lead. It is theirs to write, edit, or reject. Status is the load-bearing part:
**evidence, not a decision.**

> ## Post-approval addendum — 2026-08-10
> **Status: evidence only. No rule, threshold, definition or required output changed. The gate
> remains APPROVED.** An edit that changed a *rule* would reopen the gate. This one does not.
>
> **What was added.** `artifacts/step1-outcome-definition.md` Section 5 now records a finding
> from `artifacts/step0-history-endpoint-probe.md`. The six-week S1/S2 overlap cited in that
> section was computed over **all S1 play records** — definition **(a)**, the definition Section 5
> argues against. Recomputed after the Section 2.2 earliest-per-distinct-episode collapse, the
> comparison **inverts**: **41.31 days of overlap under (a), 360.73 days of separation under (b).**
>
> **What it establishes.** The overlap is **entirely a rewatch artifact**. Under definition (a)
> this profile's S1 completion date lands *after* its first S2 watch — **a negative clock start on
> a real, non-hypothetical profile**, not a constructed example. It is the first observed instance
> of the failure the D2 negative-lag diagnostic exists to count.
>
> **What it changes.** Nothing. It **strengthens the existing warrant** for two things already
> decided and already in the document: first-pass completion (definition (b), Section 5) and the
> D2 negative-lag diagnostic. Both were adopted on the merits before this was observed. The D2
> row in Section 10.0 is annotated "warrant strengthened, no change to the rule."
>
> **Scope limit, carried so it is not overread.** **One profile, one show.** It establishes that
> the failure mode is real and reachable. It does **not** establish how common it is.
>
> **One consequence worth recording for whoever computes D2.** D2 is computed on the operative
> clock, which is definition (b), and under (b) a rewatch cannot move the clock start. This
> profile's lag under (b) is **+360.73 days**, so it will **not** appear in the primary D2 count,
> and neither will any other (a)-style rewatch artifact. D2 under (b) measures genuine parallel
> viewing, which is a different and useful quantity. **A zero in the primary D2 count is not
> evidence that this failure mode is rare.** Sizing it would require D2 recomputed inside the
> Step 13 last-observed arm, which no step currently requires.
>
> **Provenance.** The run is now reproducible at zero live calls: `src/step0_history_probe.py`,
> `logs/step0_history_probe.json`, write-up at `artifacts/step0-history-endpoint-probe.md`.

**Both corrections I flagged alongside this text are now made** — `0001` bullet 4 is struck as
CLOSED with the three reproduction paths, and the Standing record reads twelve rows / eleven
withdrawn or corrected / plus B2, with a footnote recording the earlier conflation. Nothing
outstanding on either.

---

## Still with no decision file at all

1. **`pull_date`'s value**, when set. Deferred, not omitted. Now actionable — Step 4's size is
   known ([[open-items-and-contradictions]] S7).
2. **§10.1 open questions 1 and 3**, when ruled — the Continued boundary and the right-censoring
   rule. Each carries a Data Scientist recommendation and a decision from nobody.
3. **The gap hypothesis**, if and when it is assigned an owner.
4. **Step 3's four checkpoint positions**, when ruled, and the three already-taken judgments above.

Related: [[gate-step1-outcome-definition]], [[glossary-terms-and-thresholds]],
[[open-items-and-contradictions]], [[withdrawn-claims-register]], [[step1-open-questions]].
