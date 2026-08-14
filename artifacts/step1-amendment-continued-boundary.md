# Amendment to Step 1 §7 — the Continued boundary moves to `τ1 + H`

> **STATUS: APPROVED by the Human Lead, 2026-08-12. Revision 13, stripped.**
> This amended the **core table of an approved gate**, through eleven Red Team rounds; §11–§21 are the
> full disposition record. **`artifacts/step1-outcome-definition.md` has been amended in place** and is
> operative as amended. Decision entry: `decisions/0034-step1-continued-boundary-amendment.md`.
> **Nothing downstream has been re-run** — Steps 8 onward have not launched.

| | |
| :--- | :--- |
| **Amends** | `artifacts/step1-outcome-definition.md` §7, the outcome-state table |
| **Reopens** | **Gate 1**, as an amendment — this changes a rule Step 1 owns, not a premise it relied on |
| **Proposed by** | Human Lead, 2026-08-12 |
| **Review** | **HOLD on revision 1**, nine items — *"I could not break the rule. I broke three sentences in it."* Disposition in §11. **PROCEED-conditional on revision 2**, two required corrections and three additions. Disposition in §12. **HOLD on revision 3**, four blocking items, three required corrections, five non-blocking. Disposition in §13. **HOLD on revision 4**, three blocking items and four required corrections. Disposition in §14. **HOLD on revision 5**, two blocking items and six required corrections. Disposition in §15. **HOLD on revision 6**, two blocking items and six required corrections. Disposition in §16. **HOLD on revision 7**, two blocking items and four required corrections. Disposition in §17. **HOLD on revision 8**, two blocking items — one a six-revision misreading of the 180-day filter — and four required corrections. Disposition in §18. **HOLD on revision 9**, three blocking items. Disposition in §19. **HOLD on revision 10**, four blocking items — all one defect, the `1,573` ruling written into item 10 and nowhere else. Disposition in §20. **HOLD on revision 12**, six items, **all inside §1.1 or pointing at it**, none load-bearing for the rule. Disposition in §21 |
| **Does NOT reopen** | Step 6 / `W = 108` / `0026`; D14; Step 5; the `L2 = 1` exclusion; **D8** |
| **Stripped at revision 10, final at revision 13** | **§1.1** (the anchor argument) and **§2.2 / §2.3** (the coverage statistic) are **cut**. §1.1 was briefly restored at revision 12 in a four-sentence form and **cut again at revision 13**, its fourth failed version. Human Lead rulings, 2026-08-12 — see the note below |

**What was cut, and why it is not hidden.** Nine review rounds could not break the rule; **every hold
from revision 2 onward was against the justification prose**, and six of the last seven rounds
introduced fresh defects while repairing old ones. **§1.1 offered four grounds across four revisions
and all four failed** — §21 has the table; §2.2 conceded in its own text that coverage "carries
nothing" once its comparator was printed. Both are **removed rather than repaired again**. §2.3 goes
with §2.2, having existed only to qualify §2.2's figure.

**§1.1 was attempted four times and all four failed. The amendment is adopted without a stated ground
for the anchor choice, and that absence is itself the honest record.** The live text therefore contains
**no argument for why `τ2` was preferred to first-S2-watch + `H`** — a reader should know that, and
§21 records what was tried. Red Team's revision-10 objection stands unanswered: §1's motivating
quotation and §5.1's asymmetry have no supporting statement. **That is a gap in the justification, not
in the rule**, which survived eleven adversarial attempts unbroken.

**The warrant for this amendment is §1, §3 and §5.2** — monotone, partition-preserving, zero censoring
cost, no new constant, and a 39.5% capture rate on the population that motivated it. Nothing that was
cut was load-bearing for it.

**The full history of what was tried and why it failed is retained in §11–§18**, which are unedited.
Disposition rows there still cite §1.1, §2.2 and §2.3 by number; those citations are historical and
the sections they name are gone.

---

## 1. The change

**`W` is doing two jobs that are different questions.** The Human Lead's reasoning, verbatim:

> `W` is a decision deadline. It answers "has enough time passed to conclude they never started."
> That is a waiting rule and 108 is right for it.
>
> Continued is a question about what someone did once they started, and 108 measured from the wrong
> anchor.

**Never started keeps its 108-day deadline. Continued moves to `τ1 + H`.**

### Replacement text for the §7 table

Everything above the table in §7 is unchanged. **One set is added, and the approved document already
defines it** — D3 defines `A_H` as *"the set `A` recomputed with the bound moved from `τ1` to
`τ1 + H × 24h`."*

Let `τ2 = ⟦T0⟧ + (W + H) × 24h`. At the approved `W = 108` and `H = 91`, **`τ2 = ⟦T0⟧ + 199 days`.**
`A_H` is the distinct S2 episodes whose number is a member of `E2` and whose canonical timestamp
satisfies `watched_at < τ2`.

| State | Condition |
| :--- | :--- |
| **Never started** | `\|A\| = 0` |
| **Continued** | `\|A\| ≥ 1` **and** `F2 ∈ A_H` **and** `\|A_H\| ≥ ceil(0.90 × L2)` |
| **Started and left** | `\|A\| ≥ 1` **and not** the Continued condition |

**The `|A| ≥ 1` conjunct in Continued is load-bearing, not redundant.** Without it, §5.4's pair —
first S2 episode on day 150, complete by day 190 — would satisfy `F2 ∈ A_H ∧ |A_H| ≥ ceil(0.90 × L2)`
with `|A| = 0` and fall in **two** states. It must not be dropped as tidying. **What it makes visible
is not free — §6.1 reports at least 1,573 such pairs — but the conjunct is not what costs them.** That
belongs to §5.1's asymmetric anchoring.

**The partition proof survives verbatim in structure**: `A = ∅` / `(A ≠ ∅ ∧ C_H)` / `(A ≠ ∅ ∧ ¬C_H)`.
No pair falls in two states or in none, so Step 8's sum-to-sample invariant is untouched. **No fourth
state, no changed denominator.**

**`A ⊆ A_H` by construction**, since `τ1 < τ2`. The change is therefore **monotone** — pairs move
Started-and-left → Continued only, never the reverse — and `A ⊆ A_H` becomes a Step 8 invariant.

**As an invariant it is a code check, not a data check**, and it must be labelled that way where Step 8
asserts it. The approved text uses exactly this language of `|D| ≤ L` in §3.2. Being true by
construction, `A ⊆ A_H` can only ever catch an implementation that computed the two sets wrongly; it
can tell you nothing about the histories. **A green assertion here is not evidence for the rule.**

## 2. Why `H`, and not a new constant

`H = 91` was adopted **by name** at the Step 1 approval (D10). It is already justified, already held
constant across Step 13's `W` arms, and explicitly **not a function of `W`** — the property a second
boundary needs.

Measured at zero API calls on the Step 5 estimation sample (`src/step6_completion_lag.py`):

| 90th percentile | C1 | All five buckets |
| :--- | ---: | ---: |
| Lag to first S2 episode — what `W` was derived on | 107.71 | 37.70 |
| Lag to completion, **from `T0`** | 166.94 | 126.99 |
| **Marginal lag, first episode → completion** | **32.01** | **100.39** |

**The third row is the start-anchored rule's own distribution**, and that is stated rather than left
for a reader to notice: it measures first S2 episode → completion, which is exactly the quantity a
`first-S2-watch + H` boundary would be set from. **This document computes the alternative rule's
evidence and uses it to grade the adopted one.** No ground for preferring the adopted anchor is offered
anywhere in this draft — see the status block and §21.

### 2.1 The marginal p90 is the figure that speaks to whether 91 days is enough

**`H` adds 91 days. The marginal p90 on the applied population is 100.39.** That is the comparison
that matters, and **`H` loses it by 10 days** — `0025` sets lag figures by ceiling, so the figure to
state is 101 against 91, not the raw 9.4.

Revision 1 claimed the marginal figures were "both comfortably inside the 91 days that `H` adds."
**That was false and is withdrawn.** It is stated first here, before anything favourable, because it
is the strongest argument against the rule and the reader is entitled to meet it first.

The median — 1.58 days on C1, 2.30 across all shows — is **not** offered as support. It is the least
informative statistic available for a tail question: it describes the bulk, and the whole question is
the tail. It is reported once, here, and not used again.

**The shortfall is not left unanswered; it is measured downstream.** The pairs `H` fails to reach are
exactly the late completers, and they are counted: **§5.2's 60.5% left standing and item 9's 3,440**
are the consequence of this ten-day gap, reported rather than argued away. **§2 does not claim `H` is
sufficient. It claims `H` is the constant already adopted by name at D10, and the residual is
published.**

*Arithmetic caution: 166.94 − 107.71 = 59.2 is **not** the marginal p90. Percentiles do not subtract;
the true marginal figure is 32.01 and was computed directly.*

## 3. What this costs — nothing in censoring

D10 already requires `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`. At `W = 108` that is **exactly `τ2`**.
Every retained pair therefore already has `A_H` fully observed.

**This holds across every Step 13 arm by construction, not by coincidence**: `τ2 = W + H ≤
max(W, 91) + H` is an identity for all `W ≥ 0`.

| | Retained pairs | Shows lost | Latest `T0` |
| :--- | ---: | ---: | :--- |
| Today | 214,858 (97.62%) | 0 | 2026-01-24 |
| **Under this amendment** | **214,858 (97.62%)** | **0** | **2026-01-24** |
| A second deadline at `W_c = 167` (rejected) | 213,480 (96.99%) | 3 | 2025-11-26 |

**No new parameter, no new gate-level derivation, no censoring cost, zero API calls.**

## 4. What it does to the numbers, and what this demonstration can and cannot show

On the Step 5 estimation sample of 128,099. **Recomputed with D11 applied — see §4.1, which is why
three of these six cells differ from revision 3.**

| | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| Before | 8,449 | 102,230 | 17,420 |
| **After** | **8,449** | **104,476** | **15,174** |

**2,246 pairs move, all in one direction.**

**Stated as the change to the published category, which is the form a reader meets it in:
Started-and-left falls 12.9%** — 17,420 → 15,174. The ratio shift in §7 is the same fact expressed on
the ratio; **this is the fact expressed on the category itself**, and one of the two is what will
appear in a chart axis or a sentence of the write-up. Neither substitutes for the other.

### The limits of this table, stated because it is the table a reader will trust most

**These are not headline numbers.** The estimation sample requires S2 evidence and excludes pairs
whose first S2 record was **backfilled** — see §4.2, which corrects what that filter actually does.

**All 8,449 "Never started" rows in this table started S2, and 8,445 of them hold an admissible
record saying so — both figures measured, not inferred.** The waterfall's second
step (178,165) requires S2 evidence, so the true never-starters — pairs with no S2 record at all —
were removed before this sample existed, **23,735 of them**. **On this sample §5.4's case is not an
edge case; it is essentially all of the Never started rows.** That is a property of the sample, not of
the rule, and it is stated so the next section is not read as reassurance it cannot give. **It is also
the reason §6.1's share is a ceiling** — that denominator is missing every pair with no S2 record.

*The gap is evidentiary, not behavioural: those pairs did start S2, but their only S2 evidence is
dated after the frozen cutoff, so under D11 they hold no admissible record. Revision 4 said "all
8,449," true of behaviour and false of admissible evidence; revision 5 inverted both; this states
each separately.*

***And 8,445 is now measured rather than derived — on the right warrant.** It is not licensed by
`s2_ev_n > 0` from the waterfall's second step: that is not the in-`E2` object this sentence needs,
and citing it would be circular against the outside-`E2` objection it answers. The warrant is the
count itself — **8,445 never-started pairs hold at least one listed `E2` episode with `watched_at <
τ_pull`**, and the residual 4 are the D11 flip four, which hold pre-`τ1` in-`E2` records by
construction.*

* Revisions 5 and 6 obtained it as `8,449 − 4`,
where the 4 was the **state-change delta** — pairs that flipped when D11 was applied. That delta is
not the count of pairs lacking an admissible record: it misses any pair whose in-`E2` records are all
post-cutoff but whose `τ1 ≤ τ_pull`, since such a pair is never-started on both bases and flips
nothing, and it misses any pair whose only S2 evidence falls **outside `E2`**. Counting admissible
in-`E2` records per pair directly catches both families. **The direct count is 4** — the two extra
families are empty on this sample — so 8,445 stands, now as a measurement. It was an upper bound
presented as a count for two revisions, and the fact that it survived does not retire the objection.*

**The four-decimal invariance of the never-started share — 6.5957% before and after — is a check on a
structural argument, not evidence for it.** The argument is that `|A| = 0` is untouched and the
denominator does not move; the arithmetic confirms the implementation matches the argument. It would
be worthless as evidence if the argument were wrong.

**Any sizing of §5.4 from these figures is a floor, not an estimate** — but **not** for the reason
revisions 3 through 8 gave. See **§4.2**: the 180-day filter is a *backfill* filter, not a start-time
filter, and the floor rests on the contamination-exclusion channel instead.

**The estimation sample is not right-censored, so `A_H` is not fully observed for every row in it.**
Step 8's analysis population is censored at `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull` and this sample
is not; a pair with `T0` after 2026-01-24 has `τ2 > τ_pull`, so its Continued window runs past the
frozen cutoff and can only be partly observed. D11 bounds how wrong this can be — no record after
`τ_pull` is counted — but it does not extend the observation.

**2,246 is a floor on this account, and the argument needs a case split rather than an assertion.**
For a pair with `τ1 ≤ τ_pull`, `A` is fully observed, so its Continued-at-`τ1` status cannot change
and longer observation can only add it to the movers. For a pair with `τ1 > τ_pull`, every admissible
record precedes `τ1`, so it is scored identically at both bounds and contributes **zero** movers now
and no fewer later. **No pair can leave the 2,246; some can join it.** Revision 4 stated the
conclusion without the split, which matters because a difference of two censored quantities is not
obviously a floor.

**12.9% needed the same scrutiny and it is now closed, not merely bounded.** The ratio is
`movers / SAL_before`, and **both terms can move**, so the case split above does not carry over
unchanged. Only pairs with `τ1 > τ_pull` can change state at all — there are **3,234** of them, of
which **394** are Started-and-left at `τ1` and **4** are Never started. Longer observation can move
those 394 **out** of the denominator, raising the ratio, and can move at most **4** in, lowering it.

**The four-pair channel cannot move the published figure at the precision it is published to:**

| | Value |
| :--- | ---: |
| Published — 2,246 / 17,420 | **12.8932%** |
| Worst case — 2,246 / 17,424 | **12.8903%** |
| **Both round to** | **12.9%** |

So the caveat is **closed**. Revision 5 left it open as "a floor up to a bounded four-pair channel";
the bound is tighter than the reporting precision, which makes it not a caveat at all.

**Those four pairs are one fact appearing as three caveats, and this states it once — now verified
rather than asserted.** The four pairs whose records D11 discards (§4.1), the four whose first S2
record falls at or after `τ_pull` in the Step 6 derivations' `tau_pull_conflict` (§4.1a), and the four
in this channel are **the same four pairs**.

**Two of the three legs are forced; the third was a string literal until this revision.** The
§4.1-versus-channel identity is forced by containment — never-started under D11 is a superset of
never-started on the raw basis, the difference set has exactly four members, each requires
`τ1 > τ_pull`, and `late ∧ ¬started` is also four. **The Step 6 leg was not forced**, because Step 6
counts first-S2-record over `s1s2_scan.npz` while this script counts in-`E2` episodes over
`full_scan.npz`, and §10 records that the two scans differ by four pairs on the completer count —
containment runs the wrong way to infer equality from counts alone. **It is now reproduced — and that is the right word, not "verified."**
`step6-w-derivation-a.json` publishes only a **count**, correctly, since artifacts carry no pair
identifiers; **instance A's own set cannot be compared against.** What was done: re-derive the set
under **A's definition, on A's source (`s1s2_scan.npz`), on A's stated population (the estimation
sample)**, confirm the count matches A's published **4**, and set-compare **the reproduction** against
the D11 four. It is **4 under both the all-S2 and the in-`E2` definitions, and set-identical to the
D11 four under both.** That is the strongest check available and it is short of an identity proof.
Revision 6 rested §4.1a's decisive row on this without computing anything.

They are not in `W`'s derivation population, they move the outcome table by four rows, and they cannot
move 12.9% at all.

### 4.1 D11 was not applied before this revision, and applying it moved four pairs

**D11 (approved, §0): `τ_pull` is a single global frozen cutoff and records at or after it are
discarded from every computation.** Neither `src/eval_continued_boundary.py` nor revision 3's
`src/amendment_corrections.py` applied that filter. Both bounded only at `τ1` and `τ2`, which for a
pair with a late `T0` run **past** `τ_pull` — `T0 = max(S2 finale, S1 completion)` is uncapped — so
those pairs' Continued windows were evaluated over records D11 forbids.

**Human Lead ruling: fixed, not noted.** It touches the published table and the §7 ledger entry, so it
gets corrected in place.

| | Records | Pairs |
| :--- | ---: | ---: |
| Distinct-episode records in scope | 1,521,427 | |
| **Discarded at or after `τ_pull`** | **77** | **28 pairs touched** |

**What moved, in full:**

| | Revision 3 | **D11 applied** | Δ |
| :--- | ---: | ---: | ---: |
| Never started | 8,445 | **8,449** | **+4** |
| Continued, before | 102,234 | **102,230** | **−4** |
| Continued, after | 104,480 | **104,476** | **−4** |
| Started and left, before | 17,420 | 17,420 | 0 |
| Started and left, after | 15,174 | 15,174 | 0 |
| **Pairs moved by the amendment** | **2,246** | **2,246** | **0** |

**The amendment's own effect is unchanged.** 2,246 moves, Started-and-left falls 12.9%, and §5.2's
39.5% / 60.5% split and §5.3's 3,440 residual all stand. What moved is four pairs whose only S2
evidence was dated after the frozen cutoff: with those records discarded they have `|A| = 0` and are
**Never started**, where before they were Continued at `τ1`.

### 4.1a What D11 now covers, and what it does not — Human Lead ruling, 2026-08-12

**Disclose the scope limit; do not reopen the gates.** D11 is applied here to **one** of the two
places it bites, and §4.1 must not be read as discharging it everywhere.

| Where | D11 applied? |
| :--- | :--- |
| The S2 record set that builds `A` and `A_H` — **§4, §4.1, §5, §6.1, §6.4, §6.5, §7** | **Yes**, this revision. §5's split is re-derived and **asserted** in the script; §6.4's 3,440 is part of that split |
| **§3** — the censoring arithmetic | **Not applicable.** §3 compares `T0` against horizons and reads no records, so D11 has nothing to bite on |
| The Step 5 pair table that **defines the population** — `s2_ev_n`, `first_s2_lag_days`, the S1-completion test, and therefore `T0` | **No** |
| **§4.2's `first_s2_lag_days`** — the column its whole argument runs on | **No** — it is the Step 5 pair table, the row above. That row is load-bearing for §4.2 in a way it was not for earlier sections |
| The Step 6 completion-lag figures — §2's **second and third rows** (166.94 / 126.99 and the marginal p90 of **100.39**) | **No** — `src/step6_completion_lag.py` contains no `τ_pull` reference |
| **§9's placebo table** — `src/eval_continued_boundary.py` | **No.** It is visibly pre-D11 on its face: it reports `continued_at_tau1 = 102,234`, not 102,230 |

**What that means concretely.** The 128,099 can contain pairs whose only S2 evidence is post-cutoff —
under a fully D11-compliant waterfall they would have been removed at its second step — and
`T0 = max(S2 finale, S1 completion)` may be fixed by a post-cutoff S1 record.

**And the exposure is bounded by measurements already on disk, so the disclosure is quantified rather
than left open.**

| Bound | Value |
| :--- | :--- |
| Distinct-episode S2 records at or after `τ_pull` (this sample) | **77 records, 28 pairs** |
| Account-wide records at or after `τ_pull` — the scope §9 runs on | **1,734 of 27,656,434 — 0.006%** |
| Pairs whose **first** S2 record is at or after `τ_pull` | **4** |
| **Those 4 pairs' presence in `W`'s derivation population** | **none — `of_which_C1: 0`** |

**The last row matters most and it was already known.** **Instance A** of the Step 6 dual pair found
this exact D11 gap during the `W` derivation and reported it as `tau_pull_conflict`
(`artifacts/step6-w-derivation-a.json`). **Instance B did not test it** — it records the same 4 only
as `NOT_dropped`, with no with/without comparison. Revision 6 said "both instances measured its effect
as nil." **Only one did, and this states which.**

**The decisive fact is set membership, not a `W` value.** Instance A also reports
`W_with_them: 107.0` and `W_without_them: 107.0`, but **107.0 is not a figure this study uses** —
`0025` ruled the floored calendar-day reading a systematic off-by-one and set `W = 108` from the
continuous 107.7135, and `task-sheet.md` says outright that *"the Step 6 artifacts state 107 and
107.7135 and neither is the adopted value."* Quoting a null tested in a rejected unit proves less than
the line above it: **`of_which_C1: 0`.** `W` is read on the **C1 subset** (D14), so **none of the four
pairs is in `W`'s derivation population at all, and `W` cannot move in any unit.**

**§2's first row: no instance attribution, because none is needed.** Revision 6 said the row came
from the derivations "which did test the D11 conflict"; revision 7 reversed that to instance B. **Both
were more than the fact supports, and the second contradicted §10**, which names the row's producer as
`src/step6_completion_lag.py`. The simple true statement, and the one consistent with §10: **all three
rows of §2 come from `src/step6_completion_lag.py`, which contains no `τ_pull` reference** — the same
reason already given for rows two and three. Third attribution in three revisions; this one claims
nothing beyond the file.

**Why it is disclosed rather than fixed.** Extending D11 to the pair table moves **the Step 5
waterfall**, which sits inside an **approved gate**; extending it to the lag script moves the
distribution **`W = 108` was derived from**, inside a **second approved gate**. The correction this
revision makes is to a published figure, and `0011`'s discipline is that **a correction is computed on
the same basis as the number it corrects** — which is why the script asserts the pre-D11 waterfall
rather than recomputing it. **The limit is recorded, not argued away**, and it routes to Step 14 as
part of item 8's provenance.

**This also disposes of an artefact revision 3 mislabelled.** §10 of revision 3 described a
non-monotonicity — 4 pairs Continued at `τ1` but not at the pull bound — as "real and not a bug." **It
was a bug, and it was this one.** Under D11 those records cannot enter any computation, monotonicity
`cont_τ1 ⊆ cont_τ2 ⊆ ever` is restored, and the script now **asserts** it rather than working around
it. Revision 3's assertion that the 4 pairs were not D3′-cleared was separately **vacuous** — it
tested `cleared ∧ cont_τ1 ∧ ¬cont_τ2`, which is empty on every row unconditionally because `τ1 < τ2`.
The conclusion was true by arithmetic; the check was not a check.

### 4.2 The 180-day filter is a backfill filter, and this document misread it for six revisions

**What revisions 3 through 8 said, in five places:** *"the estimation sample truncates first-S2 lag at
180 days, so starts in `(180, 199]` are excluded by construction."* **That is false, and it was
load-bearing.**

**What the filter actually is.** `first_s2_lag_days` descends from the record-level lag built in
`src/step5_diagnose.py` as `tau − ts`, where `tau` is the record's **estimated insertion instant**
interpolated from its play `id` and `ts` is the claimed `watched_at`. It measures **how long after its
claimed watch date a record was written to Trakt.** The constant is named `BACKFILL_D`;
`src/step5_revision5.py` labels the cut `"backfilled"`; `src/step5_pairs.py`'s own comment says the
point is *"that one record's provenance."* **Step 5 named it correctly throughout — the misreading is
this document's alone, and does not touch the approved Step 5 gate.**

**Three consequences, stated because they were argued from:**

1. **Starts in `(180, 199]` are not excluded.** A pair that genuinely first watched S2 on day 185 and
   scrobbled it live has a lag near zero, and sits in the 128,099, in the 8,449, and inside the set
   eligible for the 1,575.
2. **The filter cuts at every `T0`-lag**, including a day-2 starter whose record was entered a year
   later. The excluded pairs are **not** a late-starting tail.
3. **Item 10's "channel 1" does not exist in the form described**, and it was the whole reason
   revision 8 gave for withholding a corrected value.

**The honest replacement, which preserves the conclusion.** Both 1,575 and 3,440 remain **floors**, via
the **contamination-exclusion channel**: the Step 5 waterfall drops **50,066** pairs at steps three
through five — 23,034 + 3,005 + 24,027 — and those pairs are present in the population these
quantities are reported on. **That channel runs the same direction as the D8-population channel, not
opposite to it.**

**50,066, not 73,801, and the difference matters.** The waterfall drops 73,801 in total, but the
**23,735** removed at its **second** step have **no S2 evidence at all**, so `A_H = ∅` and they can
enter **neither** numerator. They are the **ceiling** channel — where §6.1 and item 10 use them
correctly — and counting them here would put the same pairs in a role they structurally cannot fill.

**The channel's sign is not in doubt; its magnitude is.** A **count** of pairs satisfying a predicate
is monotone in the population — readmitting pairs cannot remove any of the 1,575, whatever clocks they
would carry. Revision 10 framed the readmission channel as a threat to the floor's *sign*, citing the
24,027 with untrustworthy first-S2 timestamps and the 23,034 with contaminated `T0`. **Those bear on
magnitude, not sign**, and the framing is withdrawn: an air-date-stamped pair readmitted as a starter
simply fails to join the numerator, which leaves the count where it was.

**The threat that is real is right-censoring, and it is measured.** Of the 1,575, **2** have
`τ2 > τ_pull` and are removed from any censored population, leaving **1,573**. That is the one channel
this round that actually reduced the count, and revision 10 omitted it from this section while casting
doubt on a channel that is solid.

**Provenance note.** This section's whole argument runs on `first_s2_lag_days`, which lives in the
**Step 5 pair table** — the row §4.1a's scope table marks as **not** D11-filtered. That row is
load-bearing here in a way it was not before.

**So the reason for withholding a corrected value changes, and the withholding does not.** Revision 8
withheld because two channels supposedly opposed. **They do not oppose — both run the same way, and
neither is measured.** A corrected count or ratio would therefore be wrong in a known direction by an
unknown amount, which is a stronger reason to withhold than the one it replaces.

## 5. Four things stated plainly, and not softened

**5.1 Continued is a 199-day statement while never-started is a 108-day statement.** The two headline
categories are measured over different horizons. This must appear wherever the split is reported —
not in a footnote. D5 already carries a precedent for stating an asymmetric anchor out loud.

**5.2 The amendment fixes 39.5% of the problem that motivated it, and leaves 60.5% standing.**
Of the **5,686** Started-and-left pairs that eventually complete S2, **2,246 are reclassified and
3,440 are not.** That is the honest one-line summary of what this buys.

**5.3 The residual is 3,440 pairs — reported, not resolved.** As a share of the **old**
Started-and-left group (17,420) that is **19.75%**; as a share of the **new** group (15,174) it is
**22.67%**. Both denominators are named because the two figures describe the same pairs. Reporting
this is mandatory, not optional.

**5.4 "Never started" can include pairs that demonstrably started and finished.** First S2 episode on
day 150, complete by day 190: `|A| = 0`, so **Never started**. This follows from the design —
never-started is a deadline about *starting* — and it is the sharpest oddity of the split.
**D8(ii) already measures exactly this group** (§6.1).

## 6. Downstream

### 6.1 D8 survives unchanged — and revision 1's cross-reference was wrong

Revision 1 said D8 "is measuring precisely the group §5.3 names" — the day-150 case, which
revision 2 renumbered to **§5.4**. **That was imprecise and is
corrected.** D8 has two parts, and the approved text already carries both:

> **(i)** the count and share with **any** distinct S2 episode in `[τ1, τ1 + H × 24h)`
> **(ii)** the count and share **satisfying the Continued condition** — `F2 ∈ A_H` and
> `|A_H| ≥ ceil(0.90 × L2)` — over that same horizon.

**D8(i) is the superset. D8(ii) is exactly §5.4's group.** So the split Red Team asked to be required
is **already required by the approved document**, and **D8 needs no amendment at all** — only this
corrected cross-reference. D8's importance increases: it becomes the only bound on the never-started
boundary.

**One line of D8's *rationale* does not survive, though the rule does.** The approved text prints D8
beside D3 as its **symmetric counterpart**. After this amendment they are no longer symmetric: **D8
measures over `[τ1, τ2)` and D3′ over `[τ2, τ2 + H)`** — adjacent windows on the same axis, not
mirror images. The rule is unchanged; the sentence describing why it sits where it does needs one
correction on adoption.

**D8(ii) sizes the asymmetric anchoring of §5.1, and revision 3 attributed it to the wrong clause.**
Revision 3 called it "the price of the `|A| ≥ 1` conjunct." **That is withdrawn.** Dropping the
conjunct would not deliver these pairs to Continued — it would make the definition **non-partitioning**,
so they would fall in two states at once. The conjunct **makes the cost visible; it does not cause
it.** The cost belongs to what §5.1 names: **Never started is a 108-day statement while Continued is
a 199-day statement**, and D8(ii) is that asymmetry measured.

The set is the pairs satisfying `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)` with `|A| = 0`:

> **1,575 pairs on the estimation sample, 1,573 after right-censoring, against 8,449 scored Never
> started — 18.64%.**

**The count is a floor and the share is a ceiling. They are not the same kind of number and must not
be reported as though they were.**

- **1,575 on the estimation sample; 1,573 after right-censoring** — 2 pairs have `τ2 > τ_pull`.
  **1,573 is a FLOOR for D8's population, not the count on it**, via the contamination-exclusion
  channel: **50,066** pairs are dropped at waterfall steps three through five and are present in the
  population D8 runs on. **Not** the full 73,801 — the 23,735 dropped at step two have no S2 evidence,
  so `A_H = ∅` and they can enter no numerator. **Not** via the 180-day filter either, which revisions
  3 through 8 misread — see §4.2.
- **18.64% is a CEILING.** 8,449 is never-started **on the estimation sample**, which requires S2
  evidence. **D8 runs on a population whose denominator also contains the pairs with no S2 record at
  all — 23,735 were removed at the waterfall's second step** (§4). On D8's own population the
  numerator holds and the denominator grows sharply, so **the true share is materially lower.**

**So the sentence "nearly one in five never-started pairs demonstrably finished S2" is not available,
and revision 3 should not have written it.** It was the most quotable line in the document and it was
off by a large factor against the population a reader would take it to describe.

**What stands is the count.** At least 1,573 pairs scored Never started demonstrably finished S2 by
day 199 — a real, non-trivial consequence of anchoring never-started at 108 days, stated as a number
rather than an argument. It is not a defect to be fixed here: moving the never-started boundary is a
different amendment and is not proposed. **D8 is where its true share gets measured**, which is the
substantive reason D8's importance rises under this amendment.

### 6.2 Step 10's `p` — the rank form, not the ratio

Revision 1 wrote `p = max(A_H) / L2`. **That reinstated a formula §7 explicitly withdrew after a
prior Red Team hold**, because `L2` is a count and `m` an episode number, so `m / L2` can exceed 1
where S2 numbering has a gap. It is listed in Step 1's withdrawn-claims table. Withdrawn again here.

**Required text:** let `m_H = max(A_H)`. Then

> `p = |{ e ∈ E2 : e ≤ m_H }| / L2`

— the approved rank form, with `m` replaced by `m_H` and nothing else changed. `p` remains defined
only on Started-and-left, which is now assigned on `A_H`.

**Direction, which must be named.** The 2,246 pairs leaving Started-and-left are **the ones that got
furthest**, so removing them shifts the abandonment distribution **earlier**. Step 10 reports
first-episode / mid-season / near-finale drops, so **the amendment makes abandonment look earlier on
a published chart.** The `p = 1.0` residual that §7 requires as its own named category also changes
size under `A_H` and must be re-reported, not carried over.

### 6.3 Liveness stays anchored at `τ1`. This is now explicit.

Outcome assignment happens at two instants, so an instance could reasonably re-anchor liveness at
`τ2`. **It must not.** Human Lead ruling:

> Liveness stays anchored at `τ1`. Liveness licenses trusting a null and the null is `|A| = 0`,
> which is tested at `τ1`.

**Step 7's rule is unchanged: a pair is live on activity after its clock start plus `W`.** `τ2` plays
no part in the liveness test. Written here so no Step 7 instance re-anchors it — Step 7 launches
next, and this is exactly the class of silence that cost Step 6 a full dual run.

### 6.4 D3 is replaced by D3′, with the residual reported alongside

D3 currently reports, of pairs scored Started-and-left **at `τ1`**, the share completing over
`[τ1, τ1 + H)`. **That quantity is now the operator itself**, so D3 as written measures nothing.

Revision 1 offered two repairs and **both were rejected**: moving D3's horizon whole would have
required censoring to clear 290 days, giving a latest `T0` of 2025-10-25 against a frame capped at
2025-12-31 — **−67 days, and shows lost**, trading away the amendment's best property. Reporting the
residual to `τ_pull` alone is exposure-weighted by show recency, the precise defect D10 abolished.

**The rejection of the first rested on a conflation**: D3's *data requirement* is not a *population
filter*. A diagnostic may run on a cleared subset without censoring the analysis population.

**Adopted — D3′:**

> Of pairs scored **Started and left** at `τ2` **whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`**, report the
> **share** completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its
> **share of all Started-and-left**. Counts and shares only, to `artifacts/`.
>
> **D3′ runs at every Step 13 `W` arm, and each arm reports its own cleared count and share.** The
> clearance contains `W`, so the subpopulation is arm-specific and a single figure carried from the
> adopted arm would misdescribe every other one. See §6.5.

This is a fixed-horizon **rate** — D10's guarantee preserved — at **zero censoring cost**: the
headline population is untouched and no shows are lost. Its own selection skews old; that is why the
subpopulation count and share are reported rather than the rate alone. **D10's objection was not to
exposure dependence as such, but to exposure dependence concealed inside a pooled rate.**

**Reported alongside, and labelled a count rather than a rate:**

> The **3,440** Started-and-left pairs completing S2 at any point before `τ_pull`, with its
> exposure-weighting by show recency stated at the point of use.

**The two do not bracket the quantity, and revision 2's claim that they did is withdrawn.** Both truncate observation, one at `τ2 + H` and one at `τ_pull`, and neither is a lower
bound. They are **a fixed-horizon rate and an exposure-weighted count, reported together so the
truncation is visible** — not a floor and a ceiling. This study does use genuine floor-and-ceiling
pairs at Step 9 and for the flip and liveness bounds; **this is not one of them**, and calling it one
would borrow a rigour it does not have. Neither alone satisfies D10; both together do, honestly.

### 6.5 Step 8 and Step 13

**Step 8** gains one invariant — assert `A ⊆ A_H` on every row — and evaluates two instants at
position 7. **The `0029` filter order is otherwise unchanged, and its rationale survives the
amendment**: `0029` grounds right-censoring-before-liveness on censoring being *"a property of the
clock and `pull_date` — objective, and independent of behaviour"*, and `τ2` adds only the constant `H`
to a clock `0029` already covers. **Nothing about the second instant makes the filter behavioural that
was not already true of the first.**

*Revision 5 paraphrased `0029` here as "both `τ1` and `τ2` are functions of `T0`, `W` and `H`, so
right-censoring remains objective and independent of behaviour." **That is not `0029`'s text and its
substance is false** — `T0 = max(S2_finale_air_date, S1_completion_date)` carries a behavioural term,
the `S1_completion_date` one, which binds on **52.7% of pairs** (`processed/step5/t0_binding.json`).
Corrected here. The same paraphrase also appeared in the **pre-strip §1.1**, cut at revision 10; the
briefly restored §1.1 of revision 12 made no such claim and was itself cut at revision 13.*

**Step 13's operator is unchanged in form.** `τ2 = τ1 + H` moves with `W` automatically; at the
`W = 213` arm `τ2 = ⟦T0⟧ + 304 days`, exactly the clearance `0027` already priced.

**D3′ is not unchanged in form, and revision 2 said it was.** The sentence "Step 13 is unchanged in
form" was true of the operator and **false of the diagnostic**. D3′ conditions on
`⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, which **contains `W`** — so as `W` rises the clearance lengthens,
the latest admissible `T0` moves earlier, and **the cleared subpopulation shrinks**. Per arm, on the
estimation sample:

| Arm | Clearance | Latest `T0` admitted | Cleared Started-and-left | Share | **Shows lost** |
| :--- | ---: | :--- | ---: | ---: | ---: |
| `W = 46` (lowest arm) | 228 d | 2025-12-26 | 14,734 | **95.98%** | 5 (0.45%) |
| `W = 77` | 259 d | 2025-11-25 | 14,632 | 95.40% | 7 (0.63%) |
| **`W = 108` (adopted)** | **290 d** | **2025-10-25** | **14,388** | **94.82%** | **9 (0.80%)** |
| `W = 150` | 332 d | 2025-09-13 | 14,058 | 93.65% | 13 (1.16%) |
| `W = 213` | 395 d | **2025-07-12** | 13,501 | **91.34%** | **18 (1.61%)** |

**Shows lost is reported because §6.4's rejection turned on it.** §6.4 rejected moving D3's horizon
whole partly on "**−67 days, and shows lost**," and D3′ imposes that same 290-day clearance at the
adopted arm — so the draft owed the figure it rejected the alternative over. It is **9 shows of the
1,120 represented in Started-and-left at `W = 108`, rising to 18 at `W = 213`.**

**The two are not the same loss, and the distinction is the whole reason D3′ was adopted.** §6.4's
3 shows were lost from the **analysis population** — gone from the headline, from Step 10, from every
downstream cut. D3′'s 9 are absent from **one diagnostic's subset** while the analysis population is
untouched. **A diagnostic may run on a cleared subset; a headline may not be censored to feed one.**

**The magnitude is mild — 95.98% to 91.34% across the full arm span** *(**SUPERSEDED by `0075`: 99.53% → 97.73% on Step 8's right-censored populations; this table's figures are on the amendment's uncensored estimation sample. The direction and the shrinkage stand; the level does not**)* **— and the selection is not.** At
`W = 213` the cleared set admits no pair whose `T0` falls after **12 July 2025**, which excludes
**all but the first twelve days of H2 2025**. That is precisely the cohort `0027` added the 213 arm to probe: the arm exists to
test whether the censoring bias against modern titles changes the answer, and D3′ at that arm is
**blind to the second half of the most recent year in the frame.**

**This does not invalidate D3′ or the arm.** D3′ remains a fixed-horizon rate at every arm, which is
its entire purpose, and `0033` already requires Step 8 to report retained pairs per air period per arm
— so the modern-cohort loss is visible in the arm's own output. **What it forbids is reading D3′'s
figure at a high arm as a statement about the whole population.** The cleared count and share are
reported per arm so that reading is not available.

**Two qualifications on the table itself.** It is computed on the **uncensored** estimation sample,
whereas the arms as they actually run are already censored to `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`
— so **these shares are conservative** relative to the arms in production. And **part of the H2-2025
blindness at `W = 213` belongs to D10 censoring, not to D3′**: that arm's analysis population is
already cut at `T0 ≤ 2025-10-11`, so D3′'s further cut to 2025-07-12 is an increment on an existing
loss, not the whole of it. Neither qualification changes the ruling; both change what the table means.

**Two isolated Step 13 instances would resolve this silence differently** — one running D3′ once at
the adopted `W`, one running it per arm — and that is the exact failure `0024`, `0025` and Red Team's
item 7 all concern. It is written into the spec here rather than discovered by a divergence.

## 7. Step 14 — three entries, not one

`0028` requires every directional mechanism in the ledger with its mechanism, direction and source,
stated separately and **never netted**. **Human Lead rulings, 2026-08-12: this amendment contributes
three entries, not one.** Revision 3 wrote a single entry carrying the definitional change and its
residual together — **the netting `0028` forbids, committed inside one entry.** Revision 5 then split
those two but routed only the residual, leaving the opposing mechanism to a diagnostic — **the same
omission in the other direction.** All three:

> **8. The Continued boundary at `τ1 + H` — a definitional change. No direction is claimed against
> truth.** Evaluating Continued at `τ2 = ⟦T0⟧ + 199 days` rather than `τ1` reclassifies pairs that
> completed S2 between day 108 and day 199 from **Started and left** to **Continued**. Never-started
> is untouched, so **the never-started share does not move** — but the ratio the study exists to
> produce does: never-started : started-and-left goes **0.485 → 0.557** on the estimation sample, a
> **14.8% shift**, and **Started-and-left itself falls 12.9%, from 17,420 to 15,174.** Both are
> stated: the ratio is what the study reports, the category count is what a chart shows.
> **Neither figure is an error bar.** The old boundary and the new one are each exact measurements of
> their own definition; what changed is which question is being answered. **Continued is a 199-day
> statement while never-started is a 108-day statement**, and the two must not be described as
> measured alike. (Step 1 §7 as amended)

> **9. Late completers beyond `τ2` — biases the ratio DOWN; at least 3,440 pairs.** The amendment
> reclassifies the late completers it can see and **leaves the rest scored as abandoners**. Of the
> **5,686** Started-and-left pairs that eventually complete S2, **2,246 are reclassified and 3,440 are
> not** — **19.75%** of the old Started-and-left group, **22.67%** of the new one. **Direction: these
> pairs continued and are counted as having left, so started-and-left is overstated and the ratio
> understated.** **3,440 is a floor**, twice over: the estimation sample excludes pairs the Step 5
> waterfall drops, which are present in the population this is reported on, and the sample is not
> right-censored, so pairs **not** in the 3,440 can still join it under longer observation. (Every pair **in** the 3,440 has `τ2 < τ_pull` by construction — a pair can only
> be a late completer if its `τ2` precedes the cutoff — so their own `A_H` is fully observed. The floor
> is about who is missing, not about who is counted.)
> Measured by **D3′** as a fixed-horizon rate on a cleared subpopulation, reported per Step 13 arm,
> with the exposure-weighted count beside it (§6.4). (Step 1 §7 as amended)

> **10. The never-started boundary at `τ1` while Continued is decided at `τ2` — biases the ratio UP;
> at least 1,573 pairs.** Never started is decided at **108 days** and Continued at **199** (§5.1). A
> pair that starts S2 after `τ1` and completes by `τ2` satisfies `F2 ∈ A_H` and
> `|A_H| ≥ ceil(0.90 × L2)` but has `|A| = 0`, so it is scored **Never started** — a pair that
> demonstrably continued. **Direction: never-started is overstated and the ratio with it.**
>
> **Size: 1,575 pairs on the estimation sample; 1,573 after right-censoring.** The other 2 have
> `τ2 > τ_pull`. **Three populations are involved and the entry names all three rather than conflating
> two**: the estimation sample (1,575), the estimation sample less right-censoring (**1,573**), and
> **D8's own population, which is not computed** — it differs from the estimation sample by censoring
> *and* the 50,066 *and* the 23,735 *and* Step 7 liveness. **1,573 is a floor for D8's population, not
> the count on it.**
>
> **As a share it is 18.64% of the 8,449 scored Never started, and that share is a CEILING** — 8,449 is
> never-started **on the estimation sample**, which requires S2 evidence, whereas the pairs with no S2
> record at all, **23,735 of them**, were removed at the waterfall's second step and belong in D8's
> denominator. **The count and the share are computed on different populations**, which is why they are
> stated separately and not combined.
>
> **The count is a floor** via the contamination-exclusion channel: **50,066** pairs are dropped at
> waterfall steps three through five and are present in the population D8 runs on. **Not** the full
> 73,801 — the 23,735 at step two have `A_H = ∅` and can enter no numerator. The channel's
> contribution is non-negative **only if readmitted pairs are classified on the clocks they would then
> carry**; §4.2 states that assumption and its two exceptions.
>
> **No corrected never-started count or ratio is given.** Both known channels — contamination exclusion
> and D8's larger population — push the corrected quantity the **same** way, and **neither is
> measured**, so a single corrected figure would be wrong in a known direction by an unknown amount.
> *(Revisions 6–8 printed 6,874 / 5.37% / 0.453, then justified withholding them by an opposition
> between channels. **The opposition did not exist** — it rested on reading the 180-day backfill filter
> as a start-time filter. See §4.2.)*
>
> **Item 9's count and item 10's count are not commensurable and must not be netted.** Item 9's 3,440
> acts on the ratio's **denominator**; item 10's 1,573 acts on its **numerator**. The counts stand
> about 2.2 : 1 and their effects on the ratio about 1.6 : 1, so subtracting one from the other
> produces a number that means nothing. **Report both, in their own terms, and do not summarise them
> as a net.**
>
> **This bias is not created by the amendment.** Those 1,575 pairs have `|A| = 0` and are Never started
> **under the approved rule too**. What the amendment supplies is `A_H`, the instrument that makes them
> **measurable**. Item 10 is a disclosure the amendment enables, not a cost it imposes — so it must not
> be read as a price of adoption, and it is **not** to be compared against item 8's pre-amendment
> ratio, which is not a like-for-like comparison for the same reason.
>
> **It is the counterweight to item 9 and must be published beside it.** Item 9 moves the ratio down on
> 3,440 pairs; item 10 moves it up on 1,573. **Reporting either alone puts one half of §5.1's
> asymmetry in front of the reader**, which is the netting-by-omission `0028` exists to stop.
> Measured by **D8(ii)**, the only bound on this boundary. (Step 1 §7 as amended)

### 7.1 The ledger now carries a third kind of quantity, and no-netting extends to it

`0028` was written for two kinds of entry: **population changes** — a filter that removes pairs — and
**estimator biases** — a mechanism that pushes a measured quantity off the truth. **Item 8 is
neither.** It is a **boundary correction**: the population is identical and no estimate is biased. The
old rule was not mismeasuring the ratio so much as *defining it differently* — it scored a late
completer as an abandoner.

**Item 9 is an ordinary estimator bias, and separating it from 8 is the point of the split.** Revision
3 argued that a boundary correction "has no answer" to *how far off is the number* — and then, in the
same entry, gave one: 3,440 pairs, direction named, running the same way. **A quantity with a named
direction and a measured size is an estimator bias under `0028`'s own taxonomy**, and §5.2's phrase
"fixes 39.5% of that **problem**" presupposes a target outside either definition. Both things are
true; they are true of **different quantities**, and revision 3's error was housing them in one entry.

- **Item 8** answers *what changed*. No direction against truth, because both definitions measure
  exactly what they define.
- **Item 9** answers *how far off the new number still is*. Direction named, size measured, floor
  stated.

**`0028`'s no-netting rule extends to boundary corrections unchanged, and this is now explicit.**
Item 8 is **not** to be combined with any bias entry — specifically not with the censoring asymmetry
of `0031` or the discard non-neutrality of `0023`, even though all three move the same headline — and
**item 9 is not to be folded back into item 8**, which is precisely what revision 3 did.

**And item 8 does not move the never-started share at all** — that share is invariant to four decimal
places (§4). An entry that moves the ratio while leaving one of its two components fixed is exactly
the kind that a netted ledger would render invisible.

## 8. What is preserved

- **`W = 108`, Step 6, `0026`, `0024`, `0025`, D14.** `W` becomes correctly scoped to the boundary it
  was measured on; the Step 6 finding is a **scoping correction**, not a re-derivation.
- **The §7 partition proof**, verbatim in structure.
- **D13's half-open instant convention**, on both boundaries.
- **`0029`'s filter-order rationale** — censoring is *"a property of the clock and `pull_date`"*, its actual ground. **Not** "right-censoring's objectivity" unqualified, which §6.5 of this document strikes: `T0` carries a behavioural term binding on **52.7%** of pairs.
- **D8 entirely** — see §6.1.
- **Step 5, the `L2 = 1` exclusion, Step 2's frame.**

## 9. The rejected instrument, recorded

The Human Lead's earlier proposal — decide Continued by whether the account showed activity after its
last S2 episode — was evaluated independently by Red Team and by a `data-scientist` instance. **Both
rejected the instrument while accepting the diagnosis.** The decisive evidence was a placebo:

| δ | quiet among **Continued** | quiet among **Started-and-left** | RR |
| ---: | ---: | ---: | ---: |
| 30 d | **2.53%** | **2.62%** | **1.036** (z = 0.70) |
| 180 d | 0.59% | 1.03% | 1.73 |

At the tolerance with volume it does not discriminate; where it discriminates it moves 179 pairs of
17,420. It reclassifies **77 of the 5,686** motivating cases, is degenerate at its literal reading
(one pair per account, 1.13% ceiling, 100 observed), and asserts intent against Step 14's
"no causal claim about why."

**The distinction it drew — chose to stop versus left the platform — is real and is not discarded.**
It is recommended as a **reported cut on Started-and-left** at Step 12 or Step 13.

## 10. Provenance

| | |
| :--- | :--- |
| §2's table, §2.1 | `src/step6_completion_lag.py` → `processed/step6/completion_lag.json` |
| **§3** | **`src/eval_continued_boundary.py` → `processed/step7_eval/continued_boundary_eval.json`, key `right_censoring_cost`.** Revision 5 cited the Step 6 JSON, which contains none of 214,858 / 97.62% / 213,480 / 96.99% / 3 shows. **§3's "Latest `T0`" column is in no JSON at all** — 2026-01-24 and 2025-11-26 are hand-computed as `τ_pull − 199 d` and `τ_pull − 258 d`. Both verify; both were unsourced in a table whose job is sourcing |
| §5, §9 | `src/eval_continued_boundary.py` → `processed/step7_eval/continued_boundary_eval.json` |
| **§4, §4.1, §4.2, §6.1, §6.5, §7** | **`src/amendment_corrections.py` → `processed/step7_eval/amendment_corrections.json`** |
| All three | Step 5 waterfall asserted (201,900 → 178,165 → 155,131 → 152,126 → 128,099); **zero API calls** |

**`src/eval_continued_boundary.py` is superseded for §4's table.** It does not apply D11, so its
outcome counts are the pre-filter ones (§4.1). **Its §5 split — 5,686 / 2,246 / 3,440 and the 39.5%
capture rate — was re-derived under D11 and is asserted in `src/amendment_corrections.py`.** **§9's
placebo table was not.** Revision 4 claimed both were; only one was. The placebo figures — 2.53% /
2.62%, RR 1.036, z = 0.70, 179 pairs, 77 of 5,686, the 1.13% degeneracy ceiling — still stand on
unfiltered records. They are **unaffected in kind, not re-measured.**

*Revision 5 bounded this with the **77** records and that was **the wrong scope.** 77 counts
distinct-episode S2 records **inside the estimation sample**, whereas §9's placebo runs on
**account-wide insertion instants** over every record in `full_scan.npz` and anchors on the **max** S2
insertion instant — precisely the records nearest the cutoff. The correct bound, measured this
revision: **1,734 account-wide records at or after `τ_pull`, of 27,656,434 — 0.006%.** §9's argument is
a rejection turning on a null result at 30 days (RR 1.036, z = 0.70), which 1,734 records across 2,549
accounts cannot create. **That is a reason to expect no change, not evidence of none.***

**One provenance note, because it cost a figure.** `src/amendment_corrections.py` reads
`processed/step5/full_scan.npz`, the source `eval_continued_boundary.py` used — **not**
`processed/s1s2_scan.npz`, which `step6_completion_lag.py` uses. The two differ by 4 pairs on the
completer count, and **a correction to a published number must be computed on the same basis as the
number it corrects.**

**A second note, on what "completes ever" actually is.** Under D11 it is simply the Continued
condition at an unbounded horizon, and `cont_τ1 ⊆ cont_τ2 ⊆ ever` **holds and is asserted**. Revision
3 described the operator as `Continued at τ1 ∨ Continued at τ_pull` and called the resulting
non-monotonicity "real and not a bug." **Both statements were wrong** — the disjunction it actually
ran included `cont_τ2`, and the non-monotonicity was the missing D11 filter. §4.1 has the disposition.

## 11. Disposition of Red Team's nine items on revision 1

| # | Finding | Disposition |
| :-- | :--- | :--- |
| 1 | §2 claimed 32 and 101 "both comfortably inside the 91 days `H` adds" — 100.39 is not | **Corrected.** Claim withdrawn; replaced by the 96.81% coverage characteristic (§2) |
| 2 | §6's D8 claim was false | **Corrected, and the finding partly reversed.** D8(ii) already *is* the completion version, so the split is already required by the approved text and **D8 needs no amendment** (§6.1) |
| 3 | §6 reinstated the withdrawn `p = m / L2` | **Corrected.** Rank form restored with `m_H` (§6.2) |
| 4 | Headline ratio moves ~15%, no direction named | **Added.** Routed to Step 14, 0.485 → 0.557 — as item **8** in revision 2, split into items **8 and 9** at revision 4 (§7) |
| 5 | Capture rate absent | **Added.** 39.5% fixed, 60.5% standing (§5.2) |
| 6 | Step 10's direction not named | **Added.** Abandonment shifts **earlier**; `p = 1.0` residual re-reported (§6.2) |
| 7 | Liveness anchor left open with Step 7 next | **Closed by ruling.** Liveness stays at `τ1` (§6.3) |
| 8 | §4's demonstration cannot bear its weight | **Added.** 8,445 of 8,449 never-started rows started S2 (99.95%, corrected at revision 5); invariance is a structural check, not evidence; §5.4 sizing is a floor (§4) |
| 9 | §5.2 mixed denominators unlabelled | **Corrected.** Both named (§5.3) |
| — | **D3** — both repairs rejected, D3′ proposed | **Adopted**, with the residual reported alongside as a labelled count (§6.4) |

## 12. Disposition of Red Team's items on revision 2 — verdict **PROCEED**, conditional

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **1** | **Required.** 96.81% is exposure-weighted and §2 did not say so, while §6.4 demands that disclosure for the count it is built from | **Corrected at revision 3, then superseded at revision 4.** §2.2 gives the fixed-horizon **99.13%** with its basis in full and 96.81% labelled exposure-weighted — but the section is **demoted**, both figures are **upper bounds rather than a bracket**, and the `τ1` comparator is now printed beside them. See §13 items 3 and 4 |
| **2** | **Required.** D3′'s scope under Step 13 is unspecified; its clearance contains `W` | **Closed by ruling.** D3′ runs at **every** arm, each reporting its own cleared count and share (§6.4). §6.5 gains the per-arm table, states the 95.98% → 91.34% shrinkage, and names the `W = 213` exclusion of all H2 2025 |
| 3 | §2 implied the coverage rate was derived the way `W` was | **Corrected.** §2.2 states plainly that 99.13% is an operating characteristic of a chosen boundary, not a percentile, and that the 90th-percentile convention is not its standard |
| 4 | The median is the least informative statistic for a tail question | **Corrected.** §2.1 leads with the marginal p90 of **100.39** and the fact that `H` loses to it by **10 days** under `0025`'s ceiling; the median is reported once and explicitly not used as support |
| 5 | Started-and-left falls 12.9% and neither §4 nor §7 says so | **Added** to both — §4 and item 8 (§7) |
| 6 | The ledger now carries a third kind of quantity; no-netting should be restated as extending to it | **Added** as §7.1, with the forbidden pairings named. **Revision 4 goes further**: the residual is no longer *inside* item 8 but a separate item 9 (§13 item 5) |
| 7 | *Suggested, not required.* D8(ii) is precisely the set excluded from Continued by the `\|A\| ≥ 1` conjunct alone | **Adopted at revision 3, and its attribution reversed at revision 4.** The count **1,575** stands as a floor; the share is a **ceiling**, and the cost belongs to §5.1's anchoring, not to the conjunct (§13 item 6) |
| — | Its own revision-1 **item 2** | **Conceded by Red Team without qualification** — *"D8(ii) is exactly §5.4's group. The split was already required, D8 needs no amendment, and my item 2 was a misreading of the approved document."* Recorded because a reviewer's withdrawn finding belongs on the record beside its upheld ones |

**One figure changed between the report of these corrections and revision 3.** The fixed-horizon
coverage was first computed as **98.07%** on a denominator that included pairs with `|A| = 0`. That
contradicts §2's own stated population and is **withdrawn**; on starters the figure is **99.13%**. The
rejected basis is not hidden — it is §2.3, where the 1.06-point gap is used to make the point that a
coverage figure without its basis is not a fact.

## 13. Disposition of Red Team's items on revision 3 — verdict **HOLD**

Red Team could not break the rule at a third attempt: *"the partition is exhaustive and disjoint,
`A ⊆ A_H` makes it monotone, `max(W,91) + H ≥ W + H` is an identity so censoring cost is genuinely
zero at every arm."* **All seven items are against the justification, and four are consequences of
revision 3's own additions.** Four were ruled on by the Human Lead, 2026-08-12.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **1** | **Blocking.** §6.1's "nearly one in five" is a ceiling labelled a floor, on a denominator §4 disqualifies three paragraphs earlier | **Ruled: restate as count-floor / share-ceiling.** §6.1 now separates them — **1,575 is a floor**, **18.64% is a ceiling** because 8,449 excludes the 23,735 pairs with no S2 record. The "one in five" sentence is **withdrawn** |
| **1b** | **Blocking.** 1,575 is not the price of the `\|A\| ≥ 1` conjunct — dropping it makes the definition non-partitioning, not more generous | **Ruled: reattributed** to §5.1's asymmetric anchoring. §1 and §6.1 both corrected |
| **2** | **Blocking.** §2.2's headline sentence misdescribes its own denominator: "completers visible in a fixed 91-day window past `τ2`" names 865, not 99,873 | **Corrected.** The denominator is stated as **99,873 completers visible by `τ2 + H`, within a fixed 290 days of `T0`** (§2.2) |
| **3** | **Blocking.** "They bracket the quantity" is false — both hold the numerator fixed and truncate the denominator, so **both are upper bounds** | **Ruled: "bracket" dropped**, in §2.2 **and** in §6.4 where the same claim was made of D3′ and its companion count. The Q1→Q4 exposure evidence (19.33% → 41.03%) is cited for non-convergence |
| **4** | **Blocking.** The statistic §2.2 says carries the rule awards **94.73%** to the rejected boundary; it buys 2.1 points | **Ruled: §2.2 demoted.** Coverage is an operating characteristic with the `τ1` comparator printed beside it — **96.92% vs 99.13%, +2.21 points** fixed-horizon; 94.73% vs 96.81% exposure-weighted. **The warrant is §1, §3 and §5.2**, stated as such. **Revision 5 added the self-consistent construction, where the gap is 1.37 — see §14 C4; the two tables are two constructions, not two answers** |
| **5** | **Required.** §7.1 contradicts §5.2 — a quantity with a named direction and measured size is an estimator bias under `0028`'s taxonomy | **Ruled: the entry splits.** Item **8** is the definitional change, no direction claimed; item **9** is the late-completer residual, direction named, **3,440 pairs**, a floor. §7.1 states that folding 9 into 8 is the netting `0028` forbids — which revision 3 did |
| **6** | **Required.** §10's assert is vacuous, and the non-monotonicity is misdiagnosed: **D11 is never applied**, and it is the actual cause | **Ruled: applied and re-run, not noted.** §4.1 is new. **77 records discarded, 28 pairs touched**; never-started 8,445 → **8,449**, Continued −4 at both bounds; **2,246 and 12.9% unchanged.** Monotonicity is now asserted rather than worked around. §4 gains the fourth caveat on right-censoring |
| **7** | **Required.** Six stale `§5.3` cross-references, in a section that exists to fix a stale cross-reference | **Corrected** — §1, §4, §6.1 ×2 and the revision-1 quotation, which is now dated rather than renumbered silently |
| — | *Non-blocking.* §6.5 passes, but D3′ should report **shows lost** per arm since §6.4's rejection turned on it | **Added.** **5 / 7 / 9 / 13 / 18** across the arms, with the distinction stated: §6.4's 3 shows left the **analysis population**, D3′'s 9 are absent from **one diagnostic's subset** |
| — | *Non-blocking.* §6.5's table is on the uncensored sample; part of the `W = 213` blindness is D10's, not D3′'s | **Added** as two qualifications on the table (§6.5) |
| — | *Non-blocking.* §2.3's rejected basis carries **2,675** `\|A\| = 0` pairs, not 1,115 | **Corrected.** 1,560 in the numerator, 1,115 in the window (§2.3) |
| — | *Non-blocking.* `A ⊆ A_H` is a **code check, not a data check**, per the approved §3.2 language | **Added** to §1 |
| — | *Non-blocking.* D8 is no longer "the symmetric counterpart to D3" — the windows are adjacent, not mirrored | **Added** to §6.1. The rule is unchanged; one line of its printed rationale needs correction on adoption |
| — | *Non-blocking.* §2.1's 9.4-day shortfall is **10** under `0025`'s ceiling | **Corrected** (§2.1) |

## 14. Disposition of Red Team's items on revision 4 — verdict **HOLD**

A fourth attempt on the rule, and a fourth failure to break it: *"The partition is exhaustive and
disjoint, `A ⊆ A_H` is monotone by construction, `max(W,91)+H ≥ W+H` is an identity so the
zero-censoring claim holds at every arm."* **All four Human Lead rulings were confirmed executed.**
Its summary of what remained: *"Executing two of them broke three sentences."* Three of the seven
items below are defects revision 4 introduced while applying revision 3's rulings.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking.** §4's "All 8,449 Never started rows started S2" is false — §4.1 falsified it in the same revision. The figure is 8,445 / 8,449 | **Corrected** to **99.95%**, with the four D11 pairs named as the exceptions (§4) |
| **B2** | **Blocking.** §10 claimed §9's placebo table was re-derived under D11. It was not — only the §5 split was | **Corrected.** §10 now says **unaffected in kind, not re-measured**, and gives the reason to expect no change while stating that is not evidence of none |
| **B3** | **Blocking.** D11 is applied to the record set only, not to the Step 5 pair table or the Step 6 lag script, and the document reads as a discharge | **Ruled: disclose, do not reopen.** §4.1a is new — a scope table naming what D11 covers and what it does not, that **§2.1's 100.39 is pre-D11**, and that the fix would move an approved waterfall and the distribution `W = 108` came from |
| **C1** | §6.5's "already cut at `T0 ≤ 2025-10-08`" contradicts the approved text, which gives **2025-10-11** at `W = 213` | **Corrected.** New in revision 4, inside a qualification added under a ruling |
| **C2** | `src/amendment_corrections.py` and its JSON still read "8,445" beside a computed 8,449 | **Corrected** in the script; JSON regenerated |
| **C3** | Item 9's "floor, twice over" describes the counted pairs, not the uncounted ones — every pair in the 3,440 has `τ2 < τ_pull` and fully observed `A_H` | **Corrected.** The clause now says the floor is about **who is missing, not who is counted** |
| **C4** | §2.2's shared denominator is anchored past the **adopted** bound and flatters it; self-consistently the gap is **1.37 points, not 2.21** | **Added.** Both constructions are printed, and their disagreement is made the argument: *a statistic whose measured advantage depends on which horizon anchors the denominator is not a warrant* |
| — | *Question 5.* §4's floor caveat holds for 2,246 but not, as written, for 12.9% — both terms of a ratio can move | **Corrected.** 2,246 now carries the case split it needed. **12.9% is restated as a floor only up to a bounded four-pair channel** — of the 3,234 pairs with `τ1 > τ_pull`, 394 can leave the denominator and at most **4** can enter |
| — | *Questions 2, 3, 4.* The comparator smuggles in no difference; the 8/9 split does prevent the netting; the floor/ceiling restatement is correct and does not understate | **Confirmed, no action.** Recorded because three clean answers on a HOLD are part of the record |

### 14.1 The anchor question — ruled and adopted

Red Team observes that **the anchor the document never considers is the one §1's own quotation points
at** — *"what someone did once they started."* `τ1 + H` does not implement that; it remains anchored
at `T0`. The start-anchored rule is **first-S2-watch + `H`**, and §2's marginal-lag table *is* that
distribution — so this draft computes the evidence for the start-anchored rule and uses it to grade a
`T0`-anchored one.

**Red Team argues the start-anchored rule should be rejected, on a ground this draft never states:**
it makes the classification boundary **a function of behaviour**, which breaks the `0029` filter-order
rationale §6.5 relies on — *"both `τ1` and `τ2` are functions of `T0`, `W` and `H`, so right-censoring
remains objective and independent of behaviour."* Under a first-watch anchor, when a pair's Continued
window closes depends on when the user chose to start, and censoring stops being exogenous.

It calls this *"the strongest argument the amendment has for its anchor and the only one that answers
§5.1's conceded asymmetry head-on"* and says it belongs in §1.

**Human Lead ruling, 2026-08-12: adopted.** It is now **§1.1**, placed with the change it justifies
rather than in a disposition table. Revision 5 states the concession first — that `τ1 + H` does not
literally implement "once they started," and that §2's marginal-lag table is the *start-anchored*
rule's distribution — then gives the exogeneity ground for rejecting the start anchor, ties it to
`0029`'s filter-order rationale and to §9's precedent, and notes that re-anchoring would not close the
ten-day shortfall against the marginal p90 either. §5.1's asymmetry is named there as the price of
keeping both boundaries functions of `T0`, `W` and `H` alone.

## 15. Disposition of Red Team's items on revision 5 — verdict **HOLD**

A fifth attempt on the rule and a fifth failure to break it. It also verified the D11 implementation
rather than taking it on trust: the script takes the canonical per-episode minimum **before** applying
the `< τ_pull` mask, and **the two commute** — if the minimum is at or after `τ_pull`, every record for
that episode is, so the episode drops entirely. **Both blocking items were in what the previous round
added**, which is now the third consecutive round where the corrections generated the defects.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking.** §1.1's ground is false: `τ2` **does** contain a behavioural term — `S1_completion_date` binds `T0` for **116,041 of 220,107 pairs, 52.7%** — and the claim contradicts a limitation already routed to Step 14 | **Ruled: adopt the temporal-position regrounding.** §1.1 withdraws the claim, prints the binding counts, quotes the routed limitation, and rejects the start anchor because first-S2-watch is realised **inside** the classification window and is the variable separating Continued from Started-and-left, while `T0`'s behavioural term is realised **before** it, is the study's entry criterion, and has its selection cost **already measured and routed** |
| **B1b** | **Blocking.** The sentence attributed to `0029` in §1.1 **and** §6.5 is not `0029`'s text, and the substitution is exactly the false claim | **Corrected in both.** `0029`'s actual ground — *"censoring is a property of the clock and `pull_date`"* — is quoted, `T0`'s absence from that list is noted, and `0029`'s rationale is restored to its real scope: **right-censoring before liveness**, not before outcome assignment |
| **B2** | **Blocking.** Three directional mechanisms are measured and §7 routes two. The never-started late-starter mechanism has direction and size and goes only to a diagnostic | **Ruled: third entry added.** **Item 10** — never-started decided at 108 while Continued is decided at 199, ratio **UP**, floor **1,575** pairs. Named in the entry as **the counterweight to item 9**, which must not be published without it. *(The corrected values it originally carried — 6,874 / 5.37% / 0.453 — were removed at revision 8; see §17 B1.)* |
| **C1** | §4.1a's scope table is incomplete in both columns — omits §5 from Yes, §9 from No, §3 entirely | **Corrected.** Five rows now, including **§3 as not-applicable** (it reads no records) and **§9 as No**, with the tell that makes it visible: §9 reports `continued_at_tau1 = 102,234`, not 102,230 |
| **C2** | §10's provenance row for §3 points at the wrong JSON; the "Latest `T0`" column is in no JSON at all | **Corrected.** §3 now cites `continued_boundary_eval.json`'s `right_censoring_cost`, and the hand-computed column is **labelled as hand-computed** |
| **C3** | §4's corrected sentence is false in the other direction — all 8,449 **did** start S2; four lack an *admissible* record | **Corrected.** Behaviour and admissible evidence are now stated separately: **all 8,449 started S2, 8,445 hold an admissible record saying so** |
| **C4** | §4.1a's disclosure is vaguer than the evidence on disk | **Corrected and quantified.** Four bounds printed, the decisive one being that both Step 6 instances already found this gap and measured its effect on `W` as **nil — 107.0 with the 4 pairs and 107.0 without** |
| **C5** | §10's "77 records" reassurance for §9 uses the wrong record scope | **Corrected and re-measured.** §9 runs account-wide; the right bound is **1,734 of 27,656,434 records — 0.006%** |
| **C6** | §2.2's two constructions are right as arithmetic and inverted as argument — after the demotion a *smaller* advantage supports the section's case | **Corrected.** The honesty ranking is dropped; each construction's own property is stated — the shared denominator isolates the boundary but grades `τ1` on a longer window, the self-consistent one is fairer but moves both terms — and the disagreement is stated to run **with** the demotion |
| — | *Non-blocking.* The four-pair channel can be **closed**, not bounded: 12.8903% vs 12.8932%, both round to 12.9% | **Closed.** And the three separate caveats — §4.1's D11 four, Step 6's `tau_pull_conflict` four, and the channel's four — are stated as **one fact about the same four pairs** |
| — | *Non-blocking.* `W = 213` admits `T0` to 2025-07-12, so it excludes all **but the first twelve days** of H2 2025 | **Corrected** (§6.5) |
| — | *Non-blocking.* §13 summarises the comparator as +2.21 with no pointer to §14's 1.37 | **Cross-referenced**, with the note that the two are two constructions, not two answers |

**Confirmed clean by Red Team, and recorded:** revision 4's C1–C4 all executed as described; §6.5's
2025-10-11 exact at 304 days back from `τ_pull`; the 0.485 → 0.557 ratio and 14.8% shift verify; the
arm table matches `sec6_5_D3prime_by_step13_arm` row for row; `8,445` no longer appears in the script
or the JSON.

## 16. Disposition of Red Team's items on revision 6 — verdict **HOLD**

A sixth attempt on the rule and a sixth failure to break it. Its arithmetic pass this round was the
widest yet — roughly twenty figures re-derived, including the whole §6.5 arm table row for row, the
`0029` text and the `task-sheet.md` cohort-asymmetry quotation as verbatim, and the worst-case
direction of the four-pair channel. **Both blocking items were again in what the previous round added
— the fourth consecutive round with that pattern**, and it is recorded here rather than smoothed over.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking.** §1.1's regrounded selection argument does not bind. Because `\|A\| ≥ 1` at `τ1`, `first_watch + H < ⟦T0⟧ + 199 ≤ τ_pull` is **already imposed by D10**, so the start anchor introduces no censoring the study does not already run — and the "unmeasured cost" row asserts an asymmetry that does not exist | **Ruled: withdraw it, adopt two grounds that bind.** §1.1 now records the dominance argument as the reason the previous ground failed, then rests on **(a)** a per-pair horizon destroying the common clock, which leaves §5.1's "199-day versus 108-day" framing with no referent, and **(b)** `task-sheet.md`'s requirement that `H` be held constant *"otherwise D3 and D8 are not comparable between arms"*, which a per-pair horizon breaks **inside** a single arm. The undefined-on-never-started point is recorded but not leaned on |
| **B2** | **Blocking.** §4's "8,445 hold an admissible record" is `8,449 − 4` where the 4 is a **state-change delta**, missing pairs whose in-`E2` records are all post-cutoff with `τ1 ≤ τ_pull`, and pairs whose only S2 evidence falls outside `E2`. It is an upper bound stated as a count | **Ruled: compute it.** Admissible in-`E2` records are now counted per pair directly, which catches both families. **The direct count is 4** — both extra families are empty on this sample — so **8,445 stands, now measured.** §4 records that it was an upper bound presented as a count for two revisions and that surviving does not retire the objection |
| **C1** | "Both Step 6 instances measured its effect on `W` as nil" is false — `step6-w-derivation-b.json` has no with/without `W` | **Corrected.** §4.1a now names **instance A only**, and states that B recorded the same 4 solely as `NOT_dropped` |
| **C2** | §4.1a prints `W = 107.0`, the floored unit `0025` rejected and `task-sheet.md` says is not the adopted value | **Corrected.** The decisive fact is now **`of_which_C1: 0`** — `W` is read on the C1 subset per D14, so none of the four pairs is in `W`'s derivation population and **`W` cannot move in any unit.** 107.0 is labelled as instance A's pre-`0025` figure |
| **C3** | "The same four pairs" is two-thirds proved and one-third a string literal; the Step 6 leg was never computed, and it is what licenses §4.1a's decisive row | **Computed.** The Step 6 set is **4 under both the all-S2 and in-`E2` definitions**, its intersection with the D11 four is **4**, and the sets are **identical**. §4 states which legs are forced by containment and which was not |
| **C4** | §4.1a's scope table is still incomplete — §1.1's own new binding counts come from the pre-D11 pair table, §2's **second** row is equally pre-D11, §6.4 appears nowhere; and the note reverses which instance tested | **Corrected, third attempt.** All three added. **The attribution is reversed back:** 107.71347 / 37.69667 are **instance B's** and B did **not** test; instance A, which did, reports 107.0 / 37.0 |
| **C5** | §1.1's appeal to §9's precedent is unsupported — §9 records four grounds and anchor position is not among them | **Dropped.** The consistency appeal is gone rather than back-filled into §9 |
| **C6** | Item 10's "its share is a ceiling" dangles in a standalone ledger entry, and the printed corrected values are upper bounds | **Partly corrected at revision 7, then superseded at revision 8.** The floor and ceiling labels stand with both reasons; the upper-bound claim was **wrong in both directions** and the corrected values are now **removed entirely** — see §17 B1 |
| **N1** | Item 10's correction lands at **0.453**, below item 8's pre-amendment **0.485** | **Stated at revision 7, withdrawn at revision 8.** The comparison is **not like-for-like** — those pairs are Never started under the approved rule too, so the comparable pre-amendment figure is 0.395, not 0.485. Both numbers are removed; 8, 9 and 10 must still be read together |
| **N2** | §7's header misdescribes item 10's parentage — those pairs are Never started under the approved rule too | **Corrected in the entry.** The amendment does not create the bias; `A_H` makes it **measurable**. Item 10 is a disclosure the amendment enables, not a cost it imposes |
| **N3** | §4.1a's "bounded by measurements already on disk" names two channels and bounds one | Open. The `T0`-fixed-by-post-cutoff-S1 channel is bounded only loosely by the 1,734 account-wide figure, which is labelled as §9's scope rather than offered as that bound |

## 17. Disposition of Red Team's items on revision 7 — verdict **HOLD**

A seventh attempt on the rule and a seventh failure to break it. **Both blocking items were again in
what the previous round added — the fifth consecutive round with that pattern**, and it is recorded
plainly rather than smoothed over. Red Team also confirmed that **revision 6's B2 is genuinely
discharged**: a flipped pair must have every pre-`τ1` in-`E2` record at or after `τ_pull`, which forces
`τ_pull < τ1`, which forbids any admissible in-`E2` record — so the flip four are contained in the
no-admissible-record four, and at a count of 4 both extra families are empty.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking.** Item 10's "the corrected values are upper bounds" runs **backwards on both of its own channels**. Un-truncating the 180-day rule adds to never-started faster than to 1,575; moving to D8's population adds 23,735 to the denominator and nothing to the numerator, taking 18.64% to ~4.9%. It reinstates in numeric form the overstatement §6.1 withdrew | **Ruled: drop the corrected values entirely.** **6,874, 5.37% and 0.453 are removed.** Item 10 carries the **1,575 count with both labels** and states that **no single corrected value can be given** because the two channels run in opposite directions, with the D8 channel **about four times** the other |
| **B1b** | **Blocking.** "The correction lands at 0.453, below item 8's pre-amendment 0.485" compares a corrected post-amendment ratio against an uncorrected pre-amendment one, when item 10 itself says these pairs are Never started under the approved rule too. Like-for-like is **0.395** | **Ruled: removed.** Item 10 now states explicitly that it is **not** to be compared against item 8's pre-amendment ratio, and why |
| **B2** | **Blocking.** Ground (b) is false: **D8's window is fixed by D10 at `[τ1, τ1 + H × 24h)`** and a start-anchored D3′ would still measure 91 days, so no window changes length. And `task-sheet.md` line 370 governs **`H`'s value across arms**, which a start anchor leaves at 91 — the requirement is not engaged | **Ruled: ground (b) withdrawn.** §1.1 records why it failed and rests on **ground (a) alone**. The offered D3′-clearance replacement is **not adopted** — it would be the fourth ground in four revisions, and Red Team itself flagged that it inherits the 52.7% rebuttal |
| **C1** | **Required.** Ground (a) is circular — defending `τ2` because the alternative invalidates the disclosure written for `τ2` — and one-sided, printing the alternative's spread but never the adopted rule's | **Corrected.** §1.1 now prints the **mirror**: under `τ2` the day-2 starter gets **197 days** from first watch and the day-107 starter **92**. It states that the adopted rule **does not remove per-pair heterogeneity but moves which quantity is held fixed**, that the residual heterogeneity has a **direction** subsumed in item 9, and it concedes that a start-anchored rule **would still be disclosable** — the claim is narrowed to the common calendar origin |
| **C2** | **Required.** §2's first row has its third attribution in three revisions and the latest contradicts §10 | **Corrected, and it now claims nothing beyond the file.** **All three rows of §2 come from `src/step6_completion_lag.py`, which contains no `τ_pull` reference.** No instance attribution |
| **C3** | **Required.** The same-four Step 6 leg is a **reproduction**, not an identity check — A's artifact publishes only a count | **Restated as such**, in the draft and in the script's own output key. Re-derived under **A's definition, source and population**; count matches A's published 4; the **reproduction** is set-identical to the D11 four **under both the all-S2 and in-`E2` definitions** — the second set-comparison was a bare count in revision 7 and is now tested |
| **C4** | **Required.** The script's warrant for "all 8,449 started S2" cites `s2_ev_n > 0`, which is circular against the outside-`E2` objection it answers | **Corrected in both.** The warrant is the computed count — 8,445 hold a listed `E2` episode with `watched_at < τ_pull`, and the residual 4 are the flip four |
| — | *Open.* **N3** — the `T0`-fixed-by-post-cutoff-S1 channel is bounded only loosely by the 1,734 account-wide figure | Still open, and still recorded as open |

## 18. Disposition of Red Team's items on revision 8 — verdict **HOLD**

An eighth attempt on the rule and an eighth failure to break it. **This round produced the most
consequential finding of the whole sequence, and it was not about the rule** — it was a misreading of
a Step 5 column that this document repeated in five places across six revisions, and argued from in
two ledger entries.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B2** | **Blocking, and substantive.** `first_s2_lag_days` is a **backfill** measure — `tau − ts`, the record's estimated insertion instant minus its claimed `watched_at` — not a `T0`-to-first-watch lag. So "the sample truncates first-S2 lag at 180 days, excluding starts in `(180, 199]`" is **false**, and it was the stated basis for §6.1's floor, item 9's first floor leg, and item 10's entire reason for withholding a corrected value | **Ruled: fix it.** **§4.2 is new** and states what the filter is, cites `step5_diagnose.py`, `step5_revision5.py` and `step5_pairs.py`, and lists the three consequences. All five sites corrected. **The floors survive on the contamination-exclusion channel** — 73,801 pairs dropped across the Step 5 waterfall, present in the population these quantities are reported on — **which runs the same direction as the D8-population channel, not opposite to it.** Recorded that **Step 5 named the filter correctly throughout**, so the approved gate is untouched |
| **B2b** | The correction removes the stated reason for withholding a corrected value | **Ruled: the values stay withheld, on the correct reason.** Item 10 now says plainly that **both known channels run the same way and neither is measured**, so a corrected figure would be wrong in a **known direction by an unknown amount**. Revision 8's channel-opposition argument, and the uncomputed "about four times," are gone |
| **B1** | **Blocking.** Revision 8's ruling was executed in the prose only. `src/amendment_corrections.py` still computed and published `never_started_if_corrected: 6874`, `never_started_share_if_corrected_pct: 5.37` and `ratio_if_corrected: 0.453`, under a key naming them as item 10's corrected values — and §10 routes §7 to that JSON. `ratio_before: 0.557` was additionally mislabelled, being the **post**-amendment ratio | **Corrected in the script, not only the draft.** All three keys **deleted**, the mislabelled key deleted, and a module note records why no corrected value is computed. Red Team notes this is **revision 4's C2 recurring verbatim** — same file, one round after being closed there — and that is recorded rather than smoothed over |
| **C1** | "The two channels run in opposite directions" is contradicted by its own next two sentences | **Gone with B2b.** No opposition is claimed |
| **C2** | "About four times" is computed nowhere in this study | **Removed.** Channel 1's magnitude is unmeasured, so no ratio to channel 2 can be stated |
| **C3** | "Roughly 4.9%" is a partial population adjustment — a further **50,066** pairs leave at waterfall steps three through five and are equally present in D8's population | **Removed with the rest of that paragraph.** The floor/ceiling labels carry the point without a figure that understates the denominator |
| **C4** | **Ground (a) is false as written.** There is no common calendar instant: `T0` is pair-specific and behavioural on 52.7% of pairs, which §1.1 proves three paragraphs earlier. Constancy of *offset* is available under either anchor | **Ruled: §1.1 becomes a choice at a stated price.** "Rejected" and "common calendar origin" are struck. What stands: **`τ2` measures the Continued boundary from the same origin the never-started boundary uses**, so both published categories sit on **one clock at 108 and 199**, while a start anchor uses **two origins**. The price is stated — **the start anchor gives every starter equal exposure and `τ2` does not** — and both costs are routed, to **item 10** and **item 9** |
| **C5** | Item 10 carries a weaker floor basis than item 9, in a §7 whose purpose is preventing netting-by-omission | **Corrected.** Item 10 now carries **both** legs — contamination exclusion **and** the sample not being right-censored, which admits never-started pairs in the `τ1 ≤ τ_pull < τ2` band |
| — | *Answer to the standing question.* Dropping the corrected values does **not** leave a Step 14 reader unable to size item 10 — but the entry never named the comparison that is valid | **One sentence added:** the valid comparison is **count against count on one sample — item 9's 3,440 down against item 10's at least 1,575 up, both floors** |
| — | *Open.* **N3** — the `T0`-fixed-by-post-cutoff-S1 channel is bounded only loosely | Still open, and still recorded as open |

## 19. Disposition of Red Team's items on revision 9, and the strip

A ninth attempt on the rule and a ninth failure to break it. **Revision 9 also produced the first
correction-to-a-correction in this sequence to survive Red Team's check intact**: it re-derived the
backfill semantics from `src/step5_diagnose.py` rather than accepting §4.2's citation, and confirmed
both the reading and the conclusion that the approved Step 5 gate is untouched. It independently
verified the waterfall composition, so **the contamination-exclusion channel is real.**

**Human Lead ruling, 2026-08-12: strip the draft.** Every hold from revision 2 onward was against the
justification prose rather than the rule, and six of the last seven rounds introduced fresh defects
while repairing old ones. **§1.1 and §2.2 / §2.3 are cut** — about 2,350 words — rather than repaired
a fourth time. §11–§18 are left unedited so the history stays on the record.

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking.** The false 180-day sentence was **still live** in `src/amendment_corrections.py` and the regenerated JSON — the file §10 names as §6.1's and item 10's provenance. Prose fixed, script not: revision 8's B1 recurring | **Corrected in the script and the JSON regenerated.** The key is replaced by the contamination-exclusion basis, with a comment recording the misreading |
| **B2** | **Blocking.** Item 10's two floor legs are on **incompatible populations** — leg 1 targets D8's censored population, leg 2 names exactly the pairs censoring deletes — and nothing forced the 1,575 to survive censoring, so the count could **fall** | **Ruled: state the measured number.** Computed: **2** of the 1,575 have `τ2 > τ_pull`, so **1,573 survive on D8's population**, and item 10 now leads with 1,573. The defect was real in logic and **0.13%** in magnitude. Red Team's related point stands and is recorded: **item 9 has no such defect**, because a late completer must complete before `τ_pull`, so revision 9's "same two legs" symmetry was false |
| **B3** | **Blocking.** "The valid comparison is count against count" is not valid — item 9's 3,440 acts on the ratio's **denominator**, item 10's on its **numerator**. Counts stand ~2.2 : 1, ratio effects ~1.6 : 1, and the sentence invites netting them | **Ruled: deleted, not replaced.** Item 10 now states that the two counts are **not commensurable and must not be netted**, gives both standings, and says subtracting one from the other produces a number that means nothing |
| **C1** | **73,801 is the wrong count-floor channel; the operative figure is 50,066.** The 23,735 dropped at the waterfall's second step have no S2 evidence, so `A_H = ∅` and they can enter neither numerator — they are the **ceiling** channel | **Ruled: corrected** in §4.2, §6.1 and item 10, with the reconciliation printed (23,034 + 3,005 + 24,027) and the structural reason the 23,735 cannot fill that role |
| **C2** | The channel's non-negativity is asserted, not shown — readmitting an air-date-stamped record makes its first S2 `watched_at` the air date, typically **before** `τ1`, landing it in the denominator | **Stated as an assumption** in §4.2, with both exceptions named — the 24,027 with untrustworthy first-S2 timestamps and the 23,034 with contaminated `T0` |
| **C3** | Item 10's floor and ceiling are computed on different populations and the entry does not say so | **Corrected.** The entry now says so explicitly and keeps the two figures separate |
| **C4** | §4.2 must cross-reference §4.1a, since `first_s2_lag_days` sits in the pre-D11 Step 5 pair table | **Added**, and §4.1a's scope table row is re-pointed from the now-cut §1.1 to §4.2 |
| **C5, C6** | Both concern §1.1 — that it leads with its weakest ground, and that "routed to item 9" overstates what item 9 measures | **Moot.** §1.1 is cut. Red Team's judgement that the section "should not be cut" is recorded and was **not** followed: the Human Lead's ground is that a section which has lost three arguments in three rounds is a liability regardless of what a fourth might achieve |
| — | *Open.* **N3** — the `T0`-fixed-by-post-cutoff-S1 channel is bounded only loosely | Still open, and still recorded as open |

**What the strip does not touch.** The §7 replacement table and its partition proof, §3's censoring
cost, §4's numbers with the §4.1 / §4.1a / §4.2 corrections, §5's four plain statements, §6's
downstream consequences — including **§6.3's liveness anchor**, which Step 7 needs — and ledger items
8, 9 and 10. **No adopted rule, threshold or number was removed.**

## 20. Disposition of Red Team's items on revision 10

**"The strip worked. It removed 2,350 words and introduced no new arithmetic error, which is the first
round in seven that can be said of."** Its hold was on one defect with four faces: **the `1,573`
ruling was written into item 10 and into nothing else.**

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | **Blocking. `1,573` has no producer** — it appears nowhere in the repository, `amendment_corrections.py` contains no `τ2 > τ_pull` mask, and the JSON §10 cites still published `floor_pairs: 1575`. Fourth consecutive round of a ruling executed in the prose and not the code | **Corrected.** The mask is now in the script and the JSON carries `on_estimation_sample: 1575`, `surviving_right_censoring: 1573`, `lost_to_right_censoring: 2`. **The number now has a producer** |
| **B2** | **Blocking.** Item 10 claimed 1,573 was "the count on the population D8 runs on" two paragraphs before saying the 50,066 are *also* in that population. D8's population differs from the estimation sample by censoring **and** the 50,066 **and** the 23,735 **and** Step 7 liveness — 1,573 is a **third** population, named as neither | **Corrected.** Item 10 and §6.1 now name **all three**: estimation sample (1,575), less right-censoring (**1,573**), and **D8's own population, not computed**. **1,573 is a floor for D8's population, not the count on it** |
| **B3** | **Blocking.** §6.1 and §1 were not corrected — §6.1 still read "at least 1,575 … in the population D8 runs on," the same incompatible-population defect, at the site a write-up will read | **Corrected in both**, with the three-population framing carried across |
| **B4** | **Blocking.** The deleted "valid comparison is COUNT vs COUNT" sentence was still live in the script and the JSON | **Deleted there too**, with a comment recording why: item 9 acts on the ratio's denominator and item 10 on its numerator |
| **C2** | §10's provenance table still listed §2.2 and §2.3 as live sections | **Corrected**; §4.2 added |
| **C3** | §2 now states that `H` loses the decisive comparison by 10 days with nothing answering it | **Connected.** §2.1 now says the shortfall is **measured downstream** — §5.2's 60.5% and item 9's 3,440 are its consequence — and that §2 does not claim `H` is sufficient |
| **C4** | §4.2's non-negativity paragraph is misconceived: a **count** is monotone in the population, so readmission cannot remove any of the 1,575; the cited exceptions bear on magnitude, not sign. Meanwhile the one channel that genuinely reduced the count — censoring removing 2 — was omitted | **Corrected and inverted.** §4.2 now says the channel's **sign is not in doubt, its magnitude is**, withdraws the sign framing, and names right-censoring as the real reduction |
| **C5** | §8 asserts "right-censoring's objectivity" as preserved, which §6.5 of the same document strikes | **Corrected** to `0029`'s actual ground — *"a property of the clock and `pull_date`"* — with the 52.7% qualification |
| **C6** | The script's docstring and `res["what"]` still described revisions 2–5, and it still emitted keys for the cut §2.2 / §2.3 | **Corrected.** The keys are retained but renamed `HISTORY_…_CUT_AT_REVISION_10` rather than deleted, so §11–§18's figures stay reproducible |
| — | *Verified clean by Red Team:* **50,066 and its reconciliation** (23,735 / 23,034 / 3,005 / 24,027, steps 3–5 summing to 50,066); the 180-day string genuinely discharged in the script; **§6.3's liveness anchor survived the strip intact**, so Step 7 is unblocked on that point; no coverage figure leaked outside §11–§18 | Recorded |
| — | *Open.* **N3** | Still open |

### 20.1 The restored four sentences — applied at revision 12, cut again at revision 13

Red Team asks that **~4 sentences of the cut §1.1 be restored** — not the three failed rejection
grounds, but the **choice-at-a-stated-price form** produced by the §18-C4 ruling: `τ2` measures the
Continued boundary from the same origin the never-started boundary uses, so both published categories
sit on one clock at 108 and 199, while a start anchor uses two origins; the price is that the start
anchor gives every starter equal exposure and `τ2` does not; both costs are routed to items 9 and 10.

**Its argument:** after the strip the draft contains **no statement anywhere in its live text** about
why `τ2` was chosen over first-S2-watch + `H`, while containing three things that point at the
alternative — §1's motivating quotation (*"108 measured from the wrong anchor"*), §2's marginal-lag
table, **which is the start-anchored rule's own distribution**, and §5.1's asymmetry stated as
mandatory disclosure with nothing saying why it was accepted. It holds that cutting three failed
grounds is defensible but cutting the surviving ruled statement leaves §1's quotation and §5.1
orphaned.

**Restored at revision 12, then cut again at revision 13** when Red Team showed the restored sentence
was false on its own arithmetic. See §21.

## 21. §1.1 was attempted four times, all four failed, and the amendment is adopted without it

**Human Lead ruling, 2026-08-12: adopt with §1.1 held open**, taking the exit Red Team itself named —
*"the rule and §2 through §8 are adoptable as they stand. Every one of my items is inside §1.1 or is a
stale pointer to it. Adopting the amendment with §1.1 held open, rather than holding the amendment for
§1.1, is available and I would not object to it."*

### 21.1 The four attempts

| Revision | The ground offered | How it failed |
| :--- | :--- | :--- |
| **6** | **Exogeneity** — `τ2` contains no behavioural term, so a start anchor would introduce selection | **False.** `T0 = max(S2_finale_air_date, S1_completion_date)`, and the `S1_completion_date` term **binds on 116,041 of 220,107 pairs — 52.7%** (`processed/step5/t0_binding.json`). It also contradicted a limitation already routed to Step 14 |
| **7** | **Temporal position** — the behavioural term is realised before the window opens, so censoring on first-watch would select on the outcome | **Does not bind.** Because `\|A\| ≥ 1` at `τ1`, `first_watch + H < ⟦T0⟧ + 199 ≤ τ_pull` is **already imposed by D10**. The start anchor introduces no censoring the study does not already run |
| **8** | **Arm comparability** — a per-pair horizon breaks `task-sheet.md`'s requirement to hold `H` constant | **False.** That line governs **`H`'s value across arms**, which a start anchor leaves at 91. D8's window is fixed by D10 at `[τ1, τ1 + H × 24h)`; a start-anchored D3′ still measures 91 days. **No window changes length** |
| **12** | **Choice at a stated price** — the start anchor gives every starter equal exposure, which `τ2` does not; the cost routes to item 9 | **False, and backwards.** A starter has lag `< 108`, so `τ2`'s allowance is `199 − lag > 91` for **every** starter — `τ2` gives strictly **more** exposure than the alternative, so the "price" is **dispersion, not deficit**. And item 9's set **grows** under the start anchor, so it measures a quantity choosing `τ2` *reduces* and cannot be that cost's destination |

**The pattern is worth naming.** Each version was reviewed, found unsound on the study's own recorded
figures, replaced — and the replacement failed on a different mechanism. **The rule survived eleven
adversarial attempts across the same rounds.** The failures were never about the boundary; they were
about the attempt to justify choosing its anchor.

### 21.2 What the amendment is adopted without

**There is no stated ground anywhere in the live text for preferring `τ2 = ⟦T0⟧ + (W + H) × 24h` to
`first-S2-watch + H`.** Three things in the document point at the alternative and are not answered:

1. **§1's motivating quotation** — *"Continued is a question about what someone did once they started,
   and 108 measured from the wrong anchor"* — and the adopted rule keeps that anchor, adding a constant.
2. **§2's marginal-lag row is the start-anchored rule's own distribution**, now labelled as such in §2.
3. **§5.1's 199-versus-108 asymmetry** is disclosed as mandatory with nothing saying why it was accepted.

**This absence is the honest record and is not to be repaired by a fifth attempt without new evidence.**
An unstated ground is a gap a reader can see and weigh. Four successive stated grounds that did not
survive review would have been worse, and three of them were published before being withdrawn.

### 21.3 Disposition of revision 12's items

| # | Finding | Disposition |
| :-- | :--- | :--- |
| **B1** | The restored price clause is false in direction, and its item-9 routing runs backwards | **Ruled: §1.1 cut.** Both the clause and the routing go with it |
| **R2** | The `[92, 197]` spread omits pre-`T0` starters — approved §7 gives `A` **no lower bound** and approved §5 expects those users to be *"a large share of started users"*; a weekly premiere viewer gets **283** days, so the true spread is `(91, 283+]` | **Moot with the cut**, and recorded because it shows the printed spread understated the price **in the direction that flattered the adopted rule** |
| **R3** | §1.1's "costs... routed to item 10" collides with item 10's own *"not a cost it imposes"* | **Moot with the cut.** Item 10's text is unchanged and correct |
| **R4** | The status block said the cut sections "are gone" ten lines after saying §1.1 was restored | **Corrected**, and the block now records the full sequence: cut at 10, restored at 12, cut at 13 |
| **R5** | §6.5's note read *"§1.1, which revision 10 cut"*, which was stale once §1.1 was live | **Corrected** to name the **pre-strip** §1.1 and record that the revision-12 §1.1 made no such claim |
| **R6** | 197 and 92 were hand-computed with no §10 provenance row | **Moot with the cut.** No unsourced figure remains in the live text |
| **N1** | §2's marginal-lag table is not labelled as the start-anchored rule's own distribution — the one orphan the restoration never addressed | **Applied.** §2 now states it, and states that this document computes the alternative's evidence and uses it to grade the adopted rule |

### 21.4 Status

**Everything Red Team named as adoptable stands unedited**: the §7 replacement table and its partition
proof, §3's censoring cost, §4's numbers with the §4.1 / §4.1a / §4.2 corrections, §5's four
statements, §6's downstream consequences — including **§6.3's liveness anchor**, which Step 7 needs —
§7's ledger items 8, 9 and 10, and §8's preservation list.

**Approved by the Human Lead, 2026-08-12.** Recorded in `decisions/0034-step1-continued-boundary-amendment.md`.
