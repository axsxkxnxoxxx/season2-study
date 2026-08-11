---
name: decision-log-step18
description: Running assembly of the Step 18 decision log — entries in the five-field format, ready to hand to the Human Lead to write into decisions/. Covers the Step 1 gate as of 2026-08-10.
metadata:
  type: project
---

# Step 18 decision log — running assembly

**Ownership:** the Human Lead owns this log and writes the files in `decisions/`. Second Brain
assembles the text and hands it over. **Never write to `decisions/` directly.** As of
2026-08-10 that folder holds only `.gitkeep` — **no gate has a decision file yet, including
the one that closed**.

**Why the format is fixed:** `task-sheet.md` Step 18 requires five fields per entry — what was
decided, what the alternatives were, why this one, what it costs, and where the Red Team or a
partner reviewer disagreed and how it was resolved. "This is the primary artifact. The analysis
shows the work. The log shows the judgment."

**How to apply:** when the Human Lead asks for the Step 1 decision file, hand them the text
below. Update this file after every gate and every result step rather than reconstructing at
the end — reconstruction is the failure this role exists to prevent.

---

## Entry 0 — the gate itself

**Decided.** Step 1, the outcome definition, is approved and adopted. `artifacts/step1-outcome-definition.md`
is the operative definition. First of five gates to close. Approved in writing by the Human
Lead, in session, 2026-08-10.

**Alternatives.** Approve as drafted; approve with named carve-outs; hold for a fourth
revision. Red Team had returned HOLD three times and each revision was authorized in response.

**Why this one.** The third revision made operational the four objects the document had named
but never defined — `H`, `pull_date`, the cadence classifier, and the boundary operator. With
those closed, the remaining disagreements were about *choices*, not about *undefined terms*,
and choices belong to the Human Lead rather than to another review round.

**Costs.** Three open questions in §10.1 remain undecided, and approval does not close them.
One value — `pull_date` — is deliberately left outstanding. The gap hypothesis is untested.
Approval was given with all three on the record rather than resolved.

**Disagreement and resolution.** Red Team HOLD ×3, all three revisions authorized and
completed. Red Team's B2 objection was **overruled** — see Entry 10.

---

## Entry 1 — clock start anchored on the S2 finale (D1)

**Decided.** `T0 = max(S2_finale_air_date, first-pass S1_completion_date)`. Human Lead.

**Alternatives.** Premiere anchoring: `T0 = max(S2_premiere_date, S1_completion_date)`.

**Why this one.** Three reasons. Step 6 already anchors the lag on the finale, so premiere
anchoring would derive `W` on one origin and apply it on another. Under premiere anchoring
"Continued" is unreachable inside any `W` shorter than the airing span — roughly 84 days for a
13-episode weekly season — so the state would be an artifact of release cadence. And premiere
anchoring scores a viewer who waits for a full season and then watches it as a decliner, which
collapses "declined" and "waiting to binge" into one number — the exact conflation this study
exists to break.

**Costs.** Unequal exposure. Elapsed opportunity to start S2 by `τ1` is `airing_span + W` for
a weekly show and `W` for a binge show, so **the never-started share is mechanically lower for
weekly titles, by construction rather than by behaviour**, and the gap scales with season
length. Paid openly: cadence becomes a required Step 9 stratum reported across all five D12
buckets, and a mandatory Step 12 candidate flagged as the one candidate with a known
mechanical driver. Binge shows are unaffected — premiere and finale coincide.

**Disagreement and resolution.** No Red Team objection to D1 itself. The consequence — that
most started users on weekly shows now have *negative* lags — became §10.1 open question 2 and
is **still open**.

---

## Entry 2 — season membership by listed set, not numeric range

**Decided.** An episode counts toward a season iff its `number` is a member of that season's
**listed episode-number set `E`**. `L := |E|`, `F := max(E)`, all from one payload.
`F := L` is forbidden. Data Scientist drafted under authorization; adopted with the document.

**Alternatives.** The previous rule: membership by the range `1..F`, dropping `number > F`,
`number < 1`, and missing fields.

**Why this one.** The range rule let through exactly the case the gap machinery existed for —
an episode numbered *inside* `1..F` but *absent* from the listed set passed all three tests.
Two things broke as a result: `|D1|` and `|A|` could exceed `L1` and `L2`, and `m = max(A)`
need not have been listed, so rank-based `p` could return 0, outside its own stated range.
Under the set rule `D1 ⊆ E1` and `A ⊆ E2` by construction, so `|D1| ≤ L1`, `|A| ≤ L2` and
`p ∈ (0, 1]` are **true by construction rather than by assertion**.

**Costs.** The Step 8 invariant "distinct episodes never exceed season length" stops being a
data check and becomes an **implementation** check — it now fails only if someone filtered by
range instead of set. Kept and relabelled rather than dropped. The real data check is the drop
count.

**Disagreement and resolution.** Red Team second HOLD, findings F1 and F2. Accepted in full
and rewritten. Two prior claims withdrawn as false in the process.

---

## Entry 3 — first-pass S1 completion date, not last-observed

**Decided.** The S1 completion date is the earliest date at which the §4 test is satisfied,
computed by a forward walk over distinct episodes.

**Alternatives.** (a) the last observed S1 timestamp, `max watched_at` over all S1 records.

**Why this one.** (a) measures the wrong event — the question is when the choice to continue
became available, not when a rewatch happened years later — and it is **biased by engagement**:
the heavier a rewatcher, the later the clock starts and the more time granted to start S2.
That grants the longest windows to the most engaged users.

**Costs.** Stated out loud rather than discovered: `(b) ≤ (a)` always, so first-pass produces
an earlier clock start, an earlier close, and therefore a **higher never-started share** — the
direction that strengthens the study's own headline. Two mitigations: the choice is defended
on the merits and not on the result, and **Step 13 must carry (a) as a robustness arm**.

**Disagreement and resolution.** Red Team pressed on whether the replacement Step 8 invariant
actually tests anything. Conceded and narrowed in the text: the two inequalities are vacuous,
the **equality clause** is what catches a last-observed implementation, and only if the check
computes the first-pass date **independently** rather than reading back the pipeline's value.
The real test of this decision is the D2 negative-lag count split by binding term, not the
invariant.

---

## Entry 4 — fixed post-window horizon, `H = 91 days` (D10)

**Decided.** `H = 91 days`, adopted **by name** at approval. Right-censoring becomes
`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`. D3 and D8 are measured over `[τ1, τ1 + H × 24h)` and
never "to the pull date". `H` is declared before Step 6 runs and is **not a function of `W`**.

**Alternatives.** Keep the prior rule, `T0 + max(W, 91) ≤ pull date`, with diagnostics measured
to the pull date.

**Why this one.** The prior guarantee was **false by subtraction**: it delivers
`max(0, 91 − W)` days of post-window observation — 61 at `W = 30`, **zero at any `W ≥ 91`** —
and Step 6 had not run, so the document could not know which side of 91 `W` falls on. Worse,
measuring to the pull date made D3 and D8 **exposure-weighted mixtures whose weight is show
recency** — ten years for a 2016 title, eighteen months for one whose S2 finale aired 31 Dec
2024. Direction: D8 understated later-starting for recent titles, so "never" looked most true
exactly where the frame is newest. 91 was chosen because it is the same quarter as the Netflix
reporting window the Step 9 arm exists to be commensurable with.

**Costs.** Clearance moves from `max(W, 91)` to `max(W, 91) + 91`. No show is lost — 31 Dec
2024 + 182 days is mid-2025. What is lost is pairs whose first-pass S1 completion falls in the
`H`-day band before the old cutoff: in an Aug 2026 pull at `W ≤ 91`, the effective cutoff moves
from about May 2026 to about Feb 2026. **These are recent S1 completers, disproportionately
likely to continue, so removing them moves the headline further up** — the flattering
direction. Priced openly: the waterfall reports the censoring removal as **two lines**, the
`max(W, 91)` term and the incremental `+ H` term, each with its direction named.

**Disagreement and resolution.** Red Team third HOLD, blocking finding B1. Accepted in full.

---

## Entry 5 — `pull_date` as a single global frozen cutoff, value deferred (D11)

**Decided.** `pull_date` is one calendar date, constant for the whole study;
`τ_pull := ⟦pull_date⟧`; every record with `watched_at ≥ τ_pull` is discarded whether or not
it was fetched. Adopted in **form**. **Value deliberately deferred** to Step 4's schedule.

**Alternatives.** Per-user fetch date. Or setting a value now.

**Why this one.** Step 4 is a multi-day unattended pull. Per-user fetch date makes
right-censoring depend on the accident of scheduling order, and a user fetched early shows an
empty tail a user fetched late does not — non-comparable across exactly the axis the
diagnostics must be constant on. The deferral is structural, not an oversight: the constraint
`pull_date ≤ earliest per-user fetch date` **cannot be honoured by a value chosen before the
pull is scheduled**.

**Costs.** Records fetched but discarded for `watched_at ≥ τ_pull`. That count is required in
the waterfall alongside `pull_date` and the earliest and latest per-user fetch dates — it is
the visible price of freezing the cutoff and is reported rather than absorbed. And: **every
step that right-censors or computes D3, D8 or D9 is blocked until the value exists.**

**Disagreement and resolution.** Red Team third HOLD, blocking finding B5. Accepted. The
deferral of the value was the Human Lead's own call at approval and is recorded as a decision.

---

## Entry 6 — cadence classifier with numeric thresholds (D12)

**Decided.** Five exhaustive buckets C0–C4, numeric thresholds, **first-match ordering as part
of the definition**. Adopted **by name**, as proposed. `span := F_d − P`;
`weekly_span := (L2 − 1) × 7`. C0 unclassifiable · C1 `span ≤ 1` · C2 `|span − weekly_span| ≤ 3`
· C3 `1 < span < weekly_span − 3` · C4 `span > weekly_span + 3`.

**Alternatives.** The prior wording — weekly when the span is "on the order of" `(L2−1)×7`,
binge when "near zero".

**Why this one.** Those are not thresholds and the pair is not exhaustive: a hiatus season, a
two-episode premiere, or a two-per-week drop lands in **neither** bucket. This classifier gates
the Step 6 estimation sample, a required Step 9 stratum, and a mandatory Step 12 candidate — and
a required stratum with unassigned members gets silently pooled. **Two isolated Step 6
instances reading the old sentence could legitimately produce different `W`s**, which would
surface as a spurious dual-implementation divergence.

**Costs.** The thresholds are conventions and are labelled as such — `≤ 1` rather than `= 0`
for binge because a same-day drop can straddle midnight UTC; `± 3` days for weekly because it
absorbs a change of broadcast day without reaching a full week's slip. Required alongside the
counts: **the number of shows within 1 day of any bucket boundary**, so the convention's
fragility is a visible number. C3 and C4 may not be folded into C1 or C2, and a bucket too
small for an interval is reported as a count rather than pooled.

**Disagreement and resolution.** Red Team third HOLD, blocking finding B4. Accepted in full.

---

## Entry 7 — half-open UTC-instant boundaries (D13)

**Decided.** Every date bound expands to a UTC instant at midnight; every membership test is
half-open, closed left, open right. The in-window test is **`watched_at < τ1`** and nothing
else, applied identically to `A`, D3, D8 and right-censoring. `date(watched_at) ≤ T1` is
withdrawn and must not be written.

**Alternatives.** `date(watched_at) ≤ T1`; or a `23:59:59` sentinel.

**Why this one.** The old phrase "on or before `T1`" compared a full timestamp against a date
and admitted **two faithful implementations one day apart**, on the single operator that
assigns every outcome state and feeds the Step 8 and Step 9 dual-implementation diffs. The
half-open form also makes the window exactly `W` days rather than `W + 1` calendar days, and
makes the window and the horizon tile at `τ1` without gap or overlap — which matters because
D3 and D8 are precisely counts of events just past that boundary. A sentinel would reintroduce
the ambiguity at sub-second precision, which Trakt timestamps carry.

**Costs.** Removes one calendar day from the window, moving the never-started share marginally
**up**. Named, not corrected against the two opposing one-day effects — the UTC finale skew and
`τ0 := ⟦T0⟧` — which move it **down** by comparable amounts. All three are stated; none is
netted off. All are small against any plausible `W` of tens of days.

**Disagreement and resolution.** Red Team third HOLD, blocking finding B3. Accepted in full.

---

## Entry 8 — never-started post-window diagnostic (D8)

**Decided.** For pairs scored **Never started** at `τ1`, report the count and share with any
distinct S2 episode in `[τ1, τ1 + H × 24h)`, and the count and share satisfying the Continued
condition over that horizon. Diagnostic only — **no pair moves state on account of it**.

**Alternatives.** Report nothing for the never-started category, as the prior draft did — D3
covered Started-and-left and nothing asked the same question of the category the study is
named after.

**Why this one.** "Never" is the one word in the headline a reader will take most literally,
and a pair that started S2 on day `W + 1` is called "never" by this definition. It is the same
query as D3 with the state filter changed — no new data, no new join.

**Costs.** It moves the headline **down**, which is why it belongs: reporting only bounds that
move the headline up would present the study's uncertainty as if it ran one way.

**Disagreement and resolution.** Red Team second HOLD, blocking finding F3. Accepted. Entered
as a proposal, held, and adopted by the Human Lead with the document on 2026-08-10 — not
self-adopted.

---

## Entry 9 — show splits as a known misclassification, with a bound (D9)

**Decided.** Step 8 reports both halves — pairs scored Never started carrying a split
signature, and pairs dropped at S1 completion carrying the same signature. Step 9 reports the
split-artifact bound alongside the liveness bound and D4.

**Alternatives.** The prior framing: treat splits as a counting nuisance, count at Step 8,
build nothing.

**Why this one.** A split does not merely miscount. If Trakt split a show's metadata between a
user's viewing and our pull, pair `(user, ID_A)` has a complete S1 and `|A| = 0` and **scores
Never started** — a fabricated row **directly into the published category** — while
`(user, ID_B)` fails S1 completion and disappears from the population unrecorded. That is
structurally identical to D4, so it gets D4's treatment.

**Costs.** Detection is imperfect and the count is a **lower bound**, stated wherever the
number appears. Reconciliation logic — merging split pairs back into one row — remains
unwritten: count first, reconcile only if the count justifies it. Merges are the mirror case,
less dangerous, counted with the same query and reported separately.

**Disagreement and resolution.** Red Team second HOLD, secondary finding 1. Accepted; the
prior open question 4 was closed and replaced by this.

---

## Entry 10 — the liveness bound stays inflated (Red Team B2 overruled)

**Decided.** **Overruled. Do not fix.** Recorded as an accepted risk in the table at the head
of `artifacts/step1-outcome-definition.md`.

**Alternatives.** Reclassify inactivity-excluded pairs that show complete in-window S2 viewing,
so the bound does not count demonstrable continuers as decliners.

**Why this one.** The bound is deliberately worst-case. It is not an estimate and is not
presented as one; it is the ceiling of the reported floor-and-ceiling pair, and its whole
function is to answer "what if every excluded pair were a decliner." **A bound that quietly
reclassified the pairs it could explain away would no longer be a bound.**

**Costs.** The inflation is real. It runs in the direction the bound is built to run, and it is
stated wherever the bound appears. Counterweight: Step 9 also reports bounds that move the
headline **down** — D4, D9, and the dropped-S2-evidence count — so the study's uncertainty is
not presented as running one way.

**Disagreement and resolution.** This *is* the disagreement. Red Team returned HOLD on B2; the
Human Lead overruled and recorded the objection, the ruling, and the reason on the public
record rather than deleting the objection.

---

## Entry 11 — liveness is a pair-level filter (scope correction)

**Decided.** Liveness **evidence** is account-wide; the liveness **test** is `τ1`-relative and
`τ1` is pair-specific, so liveness is a **pair-level** filter. One account can be live for one
show and not another. Dropping a user wholesale is forbidden. The Step 9 bound is over
inactivity-excluded **pairs**, not users.

**Alternatives.** The prior reading — liveness as "a statement about the account", which
appeared in three places across two drafts.

**Why this one.** It was simply mis-scoped, and the mis-scoping would have removed whole
accounts on a test that only ever applied to one of their shows.

**Costs.** None to the definition. The cost was procedural: Step 1 could not fix it alone,
because the two isolated Step 7 instances read `task-sheet.md`, not the definition. **The Human
Lead amended `task-sheet.md` Steps 7 and 9 directly on 2026-08-10.** Consequence worth
recording: a scope divergence between the two Step 7 instances is now a **bug, not a spec
ambiguity**.

**Disagreement and resolution.** Raised in review, accepted, and closed in the file the
implementers actually read. Step 1 had earlier asserted this as fact while the task sheet still
said "user"; that assertion was unbacked when made, was withdrawn, and was restated only after
the underlying file changed.

---

## Entries still missing — flag when the Human Lead next writes to `decisions/`

1. **The Step 4 endpoint choice.** `artifacts/step1-outcome-definition.md` §0 records `GET /users/:id/history` as decided by the Human Lead; `artifacts/step0-access-and-setup.md` §6 still lists that decision as open and blocking. Nothing in `decisions/`. See [[open-items-and-contradictions]] C1.
2. **The three §10.1 open questions**, when ruled — the Continued boundary, the Step 6 estimation sample, and the right-censoring rule. Each currently carries a Data Scientist recommendation and a decision from nobody.
3. **`pull_date`'s value**, when set.

Related: [[gate-step1-outcome-definition]], [[glossary-terms-and-thresholds]],
[[open-items-and-contradictions]], [[withdrawn-claims-register]].
