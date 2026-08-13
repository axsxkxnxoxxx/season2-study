---
name: open-items-and-contradictions
description: Live register of open items and cross-step contradictions in the Season 2 study, each with its two conflicting sources named — re-verified 2026-08-12 after decisions/0029-0034 and the Step 1 §7 amendment, with Z1-Z3 closed and five new findings led by the stale agent definition files
metadata:
  type: project
---

# Open items and contradictions — re-verified 2026-08-12

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry names its two sources so the Human
Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it. Several close by
ordinary progress rather than by a decision.

**The decision log of record is `decisions/`** — `README.md` plus `0001`–`0020`. Where a decision
file and this memory differ, `decisions/` governs on who decided what and when; the deliverable it
approves governs on substance. I never edit `decisions/` — I report.

---

## NEW — surfaced 2026-08-12 by the pass over `0029`–`0034`, in priority order

### W1. The agent definition files were never amended, and CLAUDE.md points agents at them FIRST

**This is the sharpest finding of the pass, and it is the item-23 pattern with a third home nobody
has been updating.**

- **`CLAUDE.md`**: *"The full specification is in `task-sheet.md`. **Each agent's own steps are
  written into its definition file.** Read the task sheet **only when you need context beyond your
  own steps.**"*
- **`.claude/agents/data-scientist.md` and `data-scientist-b.md`, line 14, byte-identical in both
  halves of the next dual pair:** *"Plot the distribution of gaps between consecutive **logged
  events** per user. **Set the threshold well beyond the normal gap** … a **user** counts as live
  if they show logged activity after clock start plus W."*

**Every clause in that sentence is withdrawn.** "Set the threshold well beyond the normal gap" was
withdrawn by **`0029`**; gaps run on **insertion instants**, not logged events, by **`0021` ruling
2**; and liveness is a **pair-level** filter, not a user-level one — the scope correction the Human
Lead made directly to `task-sheet.md` Steps 7 and 9.

**And it is not confined to Step 7.** Same files, same class:

| File / line | What it says | What supersedes it |
| :--- | :--- | :--- |
| `data-scientist.md` :13 | *"Set W at the percentile where the curve **flattens**"* | Withdrawn by `0024` |
| `data-scientist.md` :12 | *"The clock starts at the later of the S2 **premiere** date and … S1 completion date"*; *"three … states **measured at clock start plus W**"* | D1 anchors on the **finale**; `0034` measures at **two** instants |
| `analytics-engineer.md` :16 | *"in a **fixed documented order**"*; *"no clock start precedes an S2 premiere"* | Order fixed by `0029`; that invariant is **vacuous** and `task-sheet.md` line 288 says so. No `A ⊆ A_H`, no `L2 = 1` exclusion, no per-air-period counts |
| `analytics-engineer.md` :12 | *"On a 403, **hard stop and report**"* | `0004`, which **`CLAUDE.md` itself already carries as amended** |

**Why this is different from Z2, which it otherwise resembles.** Z2 was a spec *omission* plus a
conflict between two artifacts. **This is the spec an agent is told to read first, carrying rules
that were explicitly withdrawn**, and both instances of the next dual pair carry the identical
withdrawn wording — so the divergence signal is zero and the agreement is on the withdrawn rule.
`0022` and `0029` both fixed exactly this shape in `task-sheet.md` and neither touched these files.

**What I do not know and am not asserting:** whether the Human Lead treats these files as live spec
or as vestigial launch briefs superseded by `task-sheet.md` in practice. `0022`, `0028`, `0029`,
`0033` and `0034` all propagated to `task-sheet.md` and **none mentions the agent files at all**,
which is consistent with either reading. **The two things that conflict are `CLAUDE.md`'s
read-order instruction and the content of the files it points at.**

### W2. `task-sheet.md` Step 10 was not amended, and `0034` changed what Step 10 computes

- **`0034` §6.2 and `artifacts/step1-outcome-definition.md`** (§Abandonment point, amended in
  place) require three things of Step 10: `p` on **`m_H = max(A_H)`**; the **direction** named —
  the 2,246 movers are the ones that got furthest, so abandonment looks **earlier** on the
  published chart; and the **`p = 1.0` residual re-reported, not carried over**, because it changes
  size under `A_H`.
- **`task-sheet.md` Step 10, lines 323–325**, unchanged: *"Plot the distribution of abandonment
  points … Separate first-episode, mid-season, near-finale … Do not claim a specific episode."*
  **None of the three appears.**

Step 10 is Chained and single-implementation, so the failure mode is **plain omission**, not silent
divergence — the same mode `0028` was written for at Step 14 and README item 29 warns about.
`0034` propagated to Steps 7, 8, 13 and 14 and stopped short of Step 10.

### W3. Two documents cite "Step 2's marginal-lag distribution" for a figure Step 2 does not contain

- **`decisions/README.md` items 40 and 41**: *"**Step 2's** marginal-lag distribution is the
  start-anchored rule's own distribution"* and *"**Step 2's** marginal p90 of **100.39** is
  pre-D11."* **`task-sheet.md` line 423** carries the same sentence in the Step 14 ledger.
- **The source says `§2`, not Step 2.** `artifacts/step1-amendment-continued-boundary.md` §21.2:
  *"**§2's** marginal-lag row is the start-anchored rule's own distribution."* That is **§2 of the
  amendment**, produced by `src/step6_completion_lag.py`.

**Step 2 is the frame ledger. It contains no lag distribution of any kind.** A reader following the
citation lands in `artifacts/step2-frame-ledger-and-distributions.md` and finds nothing. A section
mark was rendered as a step number in the **decision log of record** — the Step 18 artifact — and in
the spec Step 14 reads. Small, purely a pointer, and trivially fixable; flagged because it is
exactly the class of defect `0031` and `0034` were both written to stop.

### W4. Step 1 §10.1 question 1 turns on a diagnostic `0034` abolished, and Q1 is still open

- **`decisions/README.md` item 2**: *"Step 1 open questions 1 and 3 remain open. **The drafted
  boundary stands until decided.**"*
- **`artifacts/step1-outcome-definition.md` §10.1 Q1**, unedited: its third supporting ground is
  ***"D3 covers the strict rule's real weakness"***, and its recommendation is *"read it together
  with **D3**. **If D3 returns a high resumption share, revisit this boundary and the value of `W`
  together.**"*
- **`0034` replaced D3 with D3′** precisely because *"that quantity is now the operator itself, so
  D3 as written measures nothing."*

**So Q1's decision procedure points at a diagnostic that was superseded because the amendment
absorbed the exact quantity Q1 wanted to read.** Q1's second ground moves too: it rests on the
`p = 1.0` residual being *visible*, and `0034` §6.2 says that residual **changes size under `A_H`
and must be re-reported.**

**Q1 is not closed by `0034` and `0034` does not claim to close it.** Q1 asks *finale-plus-90 or
finale alone* — the **conjuncts**; `0034` moved the **instant**. Both conjuncts survive. But
`0034`'s own title is "the Continued boundary amendment" and Q1 is "the Continued boundary
question," and a Step 18 reader meeting both will reasonably read Q1 as disposed of. **It is not,
and its stated warrant now has a dangling term.**

### W5. Both Step 6 artifacts' new headers say more than is true, in one row

`0029` added the right header to both files — gate outcome, coverage arithmetic, *"do not take `W`
from this file."* **Z3 is closed by it.** One clause overreaches:

- **The header**: *"Everything else here — the estimation sample, the negative-mass tables, the
  precision intervals, the censoring diagnostic — **stands as written and is unaffected by the
  rendering.**"*
- **But the same artifacts publish a Step 13 minimum range** of **[37, 107]** (`-a`) and
  **[37.70, 107.71]** (`-b`), and those **are** rendered figures: under `0025`'s ceiling the
  all-shows p90 goes 37.6967 → **38** and the C1 p90 107.7135 → **108**, giving **[38, 108]**, which
  is what `0026`/`0027` use. **`task-sheet.md` Step 13 line 368 still says "Cover at least the range
  Step 6 reports."**

**Practically moot** — `0027`'s union runs to 213 and the floor is a one-day question on a
sensitivity arm — and the header's enumerated list does not name the range. Recorded because the
header's *general* clause is broader than its list and asserts non-impact for a figure the rendering
did move.

---

## CLOSED by `0029` — the three Step 6 findings, all actioned within a day

| Was | How it closed |
| :--- | :--- |
| **Z1** — Step 7's spec carried both unclosed Step 6 lessons | **CLOSED as `0029`.** *"Set the threshold well beyond the normal gap"* withdrawn for a **named percentile**, the gap fixed as a **continuous insertion-instant difference**, and the threshold **rounded up** per `0025`. The percentile is **PROPOSED at the 99th and not adopted; Step 7 must not launch until it is ruled** (README item 30). Z1's weaker second instance — Step 8's *"fixed documented order"* with no order fixed — closed in the same entry |
| **Z2** — `W = 108` in neither consuming step, while the two artifacts said 107 and 107.71 | **CLOSED as `0029`.** `W = 108` now stated in Steps 7, 8 and 13, each naming `0026` and each saying the artifacts' figures are **not** the adopted value. `0029` names it correctly as *"not an omission but a contradiction with two different wrong answers"* |
| **Z3** — the Step 6 deliverables carried pre-`0025` numbers with no forward pointer | **CLOSED as `0029`**, in the form I flagged: a header on each artifact following the S1-completer diagnostic's supersession practice. One residual clause — see **W5** |

**Worth recording for Step 18:** all three were surfaced by this role on the post-gate consistency
pass and all three were ruled on the same day, before Step 7 launched. `0029` credits
`second-brain` in its **Found by** field. That is the third such entry after `0022` and `0028`.

---

## Superseded — the Step 6 gate pass, retained for the reasoning

### Z1. Step 7's spec carried BOTH unclosed Step 6 lessons, and Step 7 is the next dual pair

**`task-sheet.md` Step 7 line 237, unamended:**

> **"Set the threshold well beyond the normal gap"**

That is the identical shape to *"set W at the percentile where the curve flattens"* — and arguably
worse. "Flattens" at least named a feature of a curve; **"well beyond" and "normal" name nothing at
all.** `0024` withdrew the first for producing two honest readings 61 days apart on inputs that
matched to the pair.

**And `0025` names Step 7 by name for the second lesson:**

> *"It applies wherever the same shape recurs. Any later step reading a percentile off a lag or
> duration and feeding it into a half-open instant test inherits the same off-by-one. **Step 7's
> liveness threshold is the immediate candidate.**"*

Step 7's rule is *"activity after that pair's clock start plus `W`, with gaps under the threshold"* —
a duration threshold feeding a boundary test. **Step 7's spec says nothing about the unit of the gap
or the rounding of the threshold**, which is exactly the gap instance B flagged and declined to
resolve at Step 6.

**README item 26 already predicts this** — *"Expect the same shape at Steps 7 and 8"* — and `0022`
and `0028` both establish the remedy: **write the ruling into the spec before the step launches.**
Step 6 spent one full dual run discovering that an undefined word cannot be diffed. **The cost of
learning it twice is a second discarded run.**

**Weaker second instance, at Step 8.** Line 257 says *"apply … in a **fixed documented order**"*
without fixing the order. Two instances can each pick an order, document it, and both be faithful.
The final row set commutes — every filter is a row-wise predicate — but **line 264 requires
"Record sample size after each filter"**, and those waterfall counts do **not** commute. So the diff
would show differing required outputs on an identical table. Lower consequence than Z1, same shape.

### Z2. `W = 108` is not in the spec of either step that consumes it

`decisions/0026` is referenced in `task-sheet.md` at **lines 406 and 414 only — both inside Step
14**. The string `108` appears once, in a Step 14 bias statement.

- **Step 8** (dual pair) says *"Apply frame, contamination exclusions, S1 completion rule, **W**,
  liveness rule, right-censoring…"* — no value.
- **Step 7** (dual pair) composes its rule with *"clock start plus **W**"* — no value.

**This is item 23's rule with the ink still wet**, and the failure mode here is not silence but
**contradiction**: an instance that goes looking will find the Step 6 deliverables, and those say
**107** (`-a`) and **107.71** (`-b`). Neither is the adopted value. **Two instances resolving the
same gap from two different artifacts of the previous gate is precisely a spec-omission divergence
that looks like an implementation divergence.**

The remedy is the one already applied twice: `0022` put the Step 5 rulings into Steps 6 and 7;
`0028` put the routed limitations into Step 14. Step 8's and Step 7's specs have not had the
equivalent for `W`.

### Z3. The two Step 6 deliverables carry pre-`0025` numbers with no forward pointer

Both are correctly marked **PROPOSED, NOT ADOPTED**, and neither claims to be the adopted value —
that framing is right and should not be changed. The issue is that they are the **public
deliverables of a closed gate** and a reader arriving at them finds:

| | Instance `-a` | Instance `-b` | Adopted |
| :--- | ---: | ---: | ---: |
| `W` | **107** | **107.71** | **108** |
| Step 13 minimum range | **[37, 107]** | **[37.70, 107.71]**, "37 to 108" | **[38, 108]** per `0026`/`0027` |

**`task-sheet.md` Step 13 line 360 says "Cover at least the range Step 6 reports"** — and what Step
6 reports is [37, 107] / [37.70, 107.71], not the [38, 108] the decisions use. Practically moot,
since `0027`'s union runs to 213 anyway and the floor is a one-day question on a sensitivity arm.

**The repo's own established practice is to annotate.** `artifacts/s1-completer-diagnostic.md` opens
with *"This supersedes the 2,134-user snapshot"*; `pool-coverage-check.md` was fixed for lacking
exactly that. A one-line header on each Step 6 artifact pointing at `0025` and `0026` would match it.

---

## Disposition of the seven findings from the 2026-08-12 pass

**Six were actioned; the seventh was actioned by being reviewed.** Recorded here so the register
stays honest about which entries closed and how, and so none is re-raised.

| Was | Status |
| :--- | :--- |
| **X1** — Step 5's two standing rulings missing from `task-sheet.md` | **CLOSED as `0022`**, before Steps 6 or 7 launched. Both rulings written into the Step 6 and Step 7 specs. The general lesson is carried as README item 23 |
| **X2** — README item 13's "159 in-frame shows with `L1 ≤ 6`" | **CLOSED — corrected to 152** |
| **X3** — `0018` publishes 1,226-frame quintile bins | **CLOSED** |
| **X4** — the authority note omits `0008` | **CLOSED — the note now reads 0005–0008** |
| **X5** — the Step 5 artifact said a review was pending that had happened | **CLOSED** — and moot, since the gate is now approved as `0021` |
| **X6** — `pool-coverage-check.md` is an unmarked superseded snapshot | **CLOSED** |
| **X7** — `0012` changed a rule inside an approved gate and had never been reviewed | **CLOSED as `0023`.** It went to Red Team, which returned **HOLD**, and the Human Lead **upheld it on cascade cost, not on merit.** Three findings became Step 14 limitations. **This is the one that produced new material** — see below |

---

## NEW — surfaced 2026-08-12 by the `0012` review

### Y1. The completeness rule's leg 1 is derived from the header leg 2 exists to distrust

- **`0012` leg 1** requires full **`page_count`** coverage, and leg 2 exists because
  `X-Pagination-Item-Count` is not an exact record count.
- **`page_count` is `ceil(item_count / 250)` — verified in all 2,839 ledger rows, zero mismatches.**
  Leg 1 is therefore computed from the header leg 2 was written to absorb.

**The consequence is structural, not cosmetic.** A **short** final page proves the sweep reached the
end of the history — the server ran out of records before it ran out of page. **A full final page
proves nothing**: the sweep stopped at the last page the bad header allowed for, while records may
still have been flowing. Leg 1 cannot distinguish them, and **Step 1 §0 says a truncated sweep "is
indistinguishable from a genuine 'never started' and lands directly in the study's headline
category."** This is the study's own named worst failure mode, and the test against it is
self-referential.

**Not a live contradiction — a recorded limitation.** The Human Lead ruled the rule stands and the
finding travels to Step 14. It is here because **`0023` explicitly says a future reader should not
infer the shape test was examined and found wanting**, and because the cascade argument that
overruled it **weakens if the pull resumes** — at which point `0023` says it should be reconsidered
rather than inherited as settled.

### Y2. A fourth bias direction is now measured, and it does not offset the others

`artifacts/step5-discard-outcome-neutrality.md`, at zero API calls on the discarded users' still-
cached raw pages (14,578 page files, all 287 users present):

| | Discarded (287) | Retained (2,549) |
| :--- | ---: | ---: |
| Completer pairs | 25,035 | 220,107 |
| **Has-any-S2 rate** | **89.78%** | **88.52%** |
| 95% CI (Wilson) | [89.40, 90.15] | [88.38, 88.65] |

**+1.27 points, 95% CI [0.87, 1.66], z = 5.98, p < 0.001.** Intervals do not overlap. Direction:
discarded users are **more** likely to have S2 evidence, so removing them pushes the never-started
share **up**. **Pooled effect 0.13 points** — the 287 carry 10.2% of the pair pool.

**The bias ledger now has four entries and they do not net out:**

| Source | Direction |
| :--- | :--- |
| Step 3 seeding (`0008`) — heavy trackers | **down** |
| Liveness exclusion | **down** |
| `0010` tail cap, 0.93% of the pool | up |
| **`0012` tolerance discard — newly measured** | **up** |
| Step 5's adopted exclusions, net | up |

**Nothing shows they cancel, and the artifact says so explicitly.** *"A small directional bias is
not the same as a safe one."* Step 14 gets each separately.

**Two guards on how this is quoted**, both from the artifact and both easy to drop:
*"Statistically clear, practically small. Both halves of that sentence are load-bearing and neither
should be quoted without the other."* And **the significance is a function of sample size as much as
effect size** — at n = 25,035 against n = 220,107 a 1.27-point gap is easily detected; the same gap
in 500 pairs would not be.

**What it does not settle:** the mechanism is unestablished; whether the same bias holds at the
**outcome** level is untestable until `W` exists, because "has any S2 evidence" is a presence count
and a **ceiling** on Started, not a state.

### Y3. The 2% tolerance was set at the aggressive end of a wide indifference band

- **`0012`** states a replay "with a maximum residual of **0.86 percent** against the 2 percent
  tolerance," which reads as 2.3× headroom over the worst observed case.
- **`artifacts/step4-pilot-counts.json`** records `max_abs_share_of_item_count: 0.11707` —
  **11.7%** — with a signed residual range of −191 to **+131**.

The pilot's p95 is 1.4% and p99 = max is 11.7% **with nothing in between**, so **any tolerance from
roughly 1.5% to 11.7% gave the identical partition of those 20 users.** The most aggressive end was
chosen, with no sensitivity table and without the choice being stated as a choice. **On the full run
there is no such gap:** the 287 discards' absolute residual share runs min 2.01%, median 3.92%, max
99.9%, with **168 (58.5%) in the 2–5% band** — a 5% tolerance would have retained 168 of them. The
threshold cuts through the middle of a continuous distribution.

**One structural asymmetry nobody chose.** A positive residual is capped at `limit − 1 = 249`, so
**above roughly 50 pages the under-count arm cannot fire at all.** The rule presents as symmetric
and two-sided; it is one-sided on large users and a size-correlated discard on small ones. It also
discards **31 of 287** users in the direction `0012`'s own table calls *"benign, and in the safe
direction: more data than advertised, not less."*

---

## Resolved contradictions, retained for the reasoning

### X1. Both of Step 5's standing rulings were missing from the file the isolated instances read
### CLOSED as `0022`, 2026-08-12 — kept because the reasoning generalises to three remaining gates

- `artifacts/step5-contamination-diagnostics.md` §3: *"Under **ruling 2** this calibration is a
  **required input to Step 7**, which now needs an insertion time for every record."* §9.5 withdrew
  **Layer 3 entirely** — 35,861 pairs — because "its sole premise was that import noise is not
  liveness evidence, and under insertion-time liveness it **is** evidence."
- `task-sheet.md` **Step 7**, lines 231–235: *"Plot the distribution of gaps between consecutive
  logged events per user"*; the rule is written on *"logged activity"*. **Insertion time appears
  nowhere. The play-`id` calibration appears nowhere.** Both isolated Step 7 instances, reading only
  this, will derive gaps on **claimed `watched_at`.**

Two things make this worse than an ordinary omission:

1. **The dual-implementation regime cannot catch it.** Its only signal is divergence between the two
   instances. Two instances reading the same silent spec **agree** — on the wrong clock. A silent
   spec produces a clean diff, which reads as confirmation.
2. **The precedent is already established twice, by the Human Lead, for exactly this reason.** D14
   was written into `task-sheet.md` Step 6 *by bucket name* so both instances select the same rows;
   the pair-level liveness scope correction was written into Steps 7 and 9 because Step 1 could not
   fix it from inside its own file. `task-sheet.md` Step 8's preamble says outright it carries the
   obligations "because this is the file the two isolated instances read."

**Same class, one step earlier and less urgent:** ruling 1's **128,099 provenance-clean estimation
sample**. `task-sheet.md` Step 6 says only *"Restrict to users who did start S2"* plus D14's C1
restriction. The estimation sample is now **two-factor — cadence and provenance** — and only the
cadence factor is in the file. Less urgent because Step 6 runs downstream of the Step 5 gate; but if
the gate is approved without amending Step 6, the two instances will estimate `W` on a different
sample than Step 5 specified.

**Both rulings currently exist only inside an artifact for an unapproved gate.** Ruling 2 has
already been spent — it is why Layer 3 is not on the table.

### X2. `decisions/README.md` item 13 states a figure its own cited source contradicts

- **`decisions/README.md` open item 13**, closed and **ACCEPTED by the Human Lead 2026-08-12**:
  *"`min(L1) = 1` over the frame and **159 in-frame shows have `L1 ≤ 6`**"*, citing
  `artifacts/step2-frame-ledger-and-distributions.md` §3.2.
- **That §3.2** gives S1 episode buckets `1–3` = **13** and `4–6` = **139**. Total **152**.
  Independently confirmed in `processed/step2/frame-summary.json` → `s1_L_hist`.

**Likely cause, stated as a hypothesis:** 159 was computed on the **1,226-show frame**, before
`0020` removed 88 shows. 159 − 152 = 7, and the 1,095-day gap rule could plausibly account for
seven short-S1 shows. Both `0020` and item 13 are dated 2026-08-12 and their order is not recorded.

**Consequence is small and the ruling does not move** — the exposure bound is 22 accounts, and that
comes from the screen records, not from the frame. But this is a **number in the decision log of
record that its own cited section contradicts**, and that log is the Step 18 artifact.

### X3. `decisions/0018` publishes quintile bins for a frame that no longer exists

- **`0018`**: *"The **title size quintile is cut over the 1,226-show frame**"*, with the adopted
  bins tabled as **247 / 244 / 249 / 241 / 245** (sums to 1,226). `decisions/README.md`'s row for
  `0018` repeats "the 1,226-show frame."
- **`artifacts/step2-frame-ledger-and-distributions.md` §7**: `size_quintile` is
  **238 / 221 / 224 / 227 / 228** (sums to 1,138), "cut over the frame per `0018`."

**The principle survives; the numbers do not.** `0018` decided *cut over the frame, not the
candidates*, and that still holds. What changed is which frame — `0020` cut 1,226 → 1,138 on the
same day. **`0018` predicted its own invalidation in its closing section** — *"every quintile
boundary moves … a quintile label is not a stable identifier"* — and was then not updated when the
event it predicted occurred hours later. README open item 19 gestures at this but does not say the
published bins are superseded.

### X4. The README's authority note omits `0008`, the entry it most needs to name

- **`decisions/README.md`**: *"Entries 0001–0004 and 0013–0020 are Human Lead decisions. **0005–0007
  are agent-taken**, inside a Chained step, and are recorded retrospectively for ratification."*
- **`decisions/0008-step3-seed-source.md`**: *"Taken by: Analytics Engineer, inside a Chained step.
  Authority: **Not a Human Lead decision.** Status: **Open — for ratification.**"* Its second line
  calls it **"the highest-consequence agent choice in Step 3."**

The note also does not cover all twenty entries: 0001–0004 + 0005–0007 + 0013–0020 = 19. `0008` is
the one left out, and the note's stated purpose is to keep the line between "decided" and "defaulted
into" visible.

### X5. The Step 5 artifact says a review is pending that the reviews file records as complete

- **`artifacts/step5-contamination-diagnostics.md`**, header line and closing line:
  *"**Red Team reviews this revision.** Steps 6 and 7 remain blocked pending that review."*
- **`artifacts/step5-red-team-reviews.md`** §6: *"**Round 4 returned PROCEED and all four of its
  corrections have been applied.** The reviewer raised no further objection to the adopted rule on
  its merits at rounds 3 or 4."* Round 4 reviewed **revision 6**, the same revision.

The practical risk is directional and in the wrong direction: a reader of the gate artifact concludes
a review is still owed, when the reviews file says the ball is with the Human Lead. **Neither file is
wrong about the gate itself** — both correctly state it is not approved and that no agent records
approval.

### X6. `artifacts/pool-coverage-check.md` is a superseded snapshot and says nowhere that it is

- **It reports** 2,134 `complete`, **235** `discarded_over_tolerance`, 2,370 contributing users, and
  its own Limits section reads *"2,370 of 4,088 usable pool users, **58%**"* and *"no pull process
  was running at scan time."*
- **The pull has since stopped for good** at 2,549 `complete` / **287** discarded / 2,836 decided /
  **62.9%** (`artifacts/s1-completer-diagnostic.md` §1).

**The comparison that makes this actionable:** the S1-completer diagnostic faced the identical
problem and handled it correctly — it opens *"This supersedes the 2,134-user snapshot"* and
preserves the old outputs at `processed/diag_snapshot_2134u/`. The coverage check got no such
header. Every distributional figure in it — 44,866 shows, the per-show user counts, the 1970 spike
at 285,296 records — is on the smaller cohort and reads as current.

### X7. `0012` changed a rule inside an approved gate and had not been put to Red Team
### CLOSED as `0023`, 2026-08-12 — reviewed, HOLD returned, rule upheld on cascade cost

The review happened and produced Y1, Y2 and Y3 above. **Red Team was not overruled on the
substance** — `0023` says so in those words; what was weighed against it was cost, and the weighing
is stated rather than implied. **Red Team also argued `0012` reaches the gate-reopening clause by
converting a categorical completeness requirement into a graded one. The Human Lead ruled the rule
stands, and `0023` states the reopening question is answered by that ruling** — the findings travel
to Step 14 rather than back to Step 1.

`0023` also closes a second-order defect: **`0012` was marked `Status: Closed` while its own header
said the Human Lead may wish to put it to Red Team.** A decision cannot be closed and pending review
at once. It is closed now, having been reviewed.

The original reasoning, retained:

- **The standing rule**, from the Step 1 approval record: *an edit that changes a **rule** reopens
  the gate; an edit that adds **evidence** does not.*
- **`0012`** changes the sweep-completeness test in `artifacts/step1-outcome-definition.md` §0 and
  in `0002` condition 2, from exact `item_count` equality to page coverage plus a 2% residual. Its
  own header says *"This changes a rule inside an approved gate artifact … the Human Lead may wish
  to put it to Red Team. Flagged, not decided."*

**The completeness *requirement* is untouched** — a truncated sweep is still never returned as data,
and the reasoning for it is unchanged. Only the *detection test* moved, and the evidence for moving
it is strong (7 of 10 pilot users failed exact equality on HTTP 200 responses; two page sizes
returned identical record sets). **This is not an objection to the change. It is that the study's own
gate-reopening rule was invoked, the exception was taken, and the review it names has not happened.**

---

## Claims whose basis moved — right conclusion, corrected reason

Five in this period. Recorded together because the pattern is now a property of the project, and
because Step 18 records *why* a decision was made, not only what it was. A conclusion that is right
for a newly-stated reason should be logged with the new reason, not the one that was in the room.

| Conclusion, unchanged | Reason that was withdrawn | Reason that holds |
| :--- | :--- | :--- |
| **Recompute `pool_completers` on the full pool** (`0013` condition 2, done in `0019`) | "completer counts only rise" | **False.** 118 shows *fell*, 177 pairs lost, when adding users raised `L1_hat` and moved `F1_hat` to an episode earlier users had not watched — retroactively un-completing them. Counts **move**. All 118 are long-tail; the ≥50 set is untouched, which is why the candidate set is monotone in practice though the statistic is not in principle |
| **C5 needs no separate ruling; the 720 are retained** | "all 425 C5 pairs with no S2 evidence are already inside the 1,542" | **False — the sets are disjoint by construction**, overlap exactly **0**, and the count is **720**, not 425. Holds instead on the insert-time bound (720 at median **1,738 d**, **7.92%** open at `W = 60`, against 40 d and 58.6% for the 1,542), which Red Team independently endorsed as the right test |
| **Exclude the 1,542** (adoption 2) | "these pairs cannot be evaluated against the definition" | **False.** With zero S2 records `\|A\| = 0` for *every* `τ1`; the pair is perfectly evaluable. Holds instead as a **right-censoring defect** — a fabricated-early `T0` lets a pair pass a censoring test it should have failed (Red Team D2) |
| **Cap the tail at 300 forecast pages** (`0010`) | "a 907-page user is roughly six hours alone" | **Wrong by a factor of 60.** At 150 GET/min a 907-call user is **6.0 minutes**; the pool's heaviest user is 6.9 minutes. Holds instead as a **circuit breaker on forecast error** — and the wrong argument would have pointed at a far more aggressive cap, which at 150 pages would have removed 5% of the pool, all from the heavy end |
| **Order the pull so an early stop is survivable** (`0009`) | median-out, "sort by pages, pull median first, work outward" | Median-out leaves a **centered** slice, not a representative one: at ten hours it pulls **no user above 73 pages** in a pool reaching 1,034. Amended before launch to **stratified round-robin**, at a named 12% throughput cost |
| **`W` is read at a percentile of the C1 lag curve** (`0024`) | "set W at the percentile where the curve **flattens**" | **The C1 density is close to scale-free past day 7** — log-log slope −1.1 to −1.5 across every decade — so there is no elbow to read and **the spec asked for a feature the distribution does not have**. Now the **90th percentile**, defended as an **imported convention** rather than as a fact about the data |
| **Keep the 2% completeness tolerance** (`0012`, upheld by `0023`) | "the pilot's maximum residual was 0.86% against a 2% tolerance" — i.e. the threshold has headroom | **The pilot max is 11.7%**, and any tolerance from ~1.5% to 11.7% partitioned the pilot identically. The rule now stands on **cascade cost** — a 0.13-point correction does not justify re-deriving cohort → frame → Step 5 rule — **explicitly not on merit**, with Red Team's finding recorded as standing |

**Two of these entered rulings before they were corrected** — the C5 disjointness error and the
insert-time bound quoted from a unit bug. Both are in [[withdrawn-claims-register]].

---

## Closed since 2026-08-11 — verified, do not re-raise

| Was | Item | How it closed |
| :--- | :--- | :--- |
| **O1 / S7** | `pull_date` had no value | **`0011`: `pull_date = 2026-08-11`, `τ_pull = 2026-08-11T00:00:00Z`.** Constraint verified — earliest per-user fetch 05:01:26Z. Right-censoring, D3, D8, D9 unblocked. `0011` carries S7's cost concern as a named consequence: the discarded tail is ~1 day for early-fetched users and ~2 for late-fetched, so **the discarded-record count is not evenly distributed and must not be read as if it were** |
| **N1** | Step 1 §8 read as though question 2 were open, and nothing stated how negatives are handled in the all-shows plot | **Both halves closed, verified line by line.** §8 now reads "It is now **DECIDED as D14**". `task-sheet.md` Step 6 now carries a full **"Rule for the negative mass in the all-shows plot"**: plot signed and untruncated, do not clip or drop; **never read W off the all-shows curve**; report negative mass split by all five D12 buckets; **derive Step 13's range deterministically** by reading the same percentile on both curves. The dual-implementation divergence risk N1 identified is closed at the source |
| **S3** | `reciprocal_pairs: 1353` vs a recount of 1,172 | **README item 12: fixed in `src/step3_backfill.py` and regenerated. 1,172 confirmed.** My per-record double-count hypothesis was correct |
| **S9** | `MIN_EPISODES_USABLE = 10`'s warrant unverified | **README item 13, closed and ACCEPTED 2026-08-12.** The warrant is **not literally true** and that is what was accepted, not denied: `min(L1) = 1`, so a 6-episode account is not arithmetically barred from an in-frame S1 completion. **Exposure at most 22 accounts, 0.5% of the 4,320 screened** — 210 of the 232 rejected had zero episodes. All 232 recoverable at **0 live calls**; a full history pull of all 232 costs 296 pages. **Not** recoverable: what the crawl would have found had they stayed in the frontier. (One figure inside the closure is contradicted — X2) |
| **S10** | README not updated for `0005` | `0005`–`0020` all indexed; open items renumbered to 19. (One gap remains — X4) |
| **S1, S2, S4, S5, S6, S8** | Step 3 write-up items | Absorbed into `0005`–`0008` and README items 10 and 11. **S5/S6 survive as README item 10**, below |
| **O5** | critical path | Superseded — see the current path below |

---

## OPEN — carried forward

### O2. The gap hypothesis is untested and still belongs to no step

Whether Trakt represents a numbering gap by **omitting** the number or by **listing a placeholder**
is unowned. `decisions/README.md` items 3 and 8 both carry it; item 8 exists to say **visibility is
not ownership.**

**One observation now exists, in the benign direction, n = 1.**
`artifacts/step2-frame-ledger-and-distributions.md` §6 finds **exactly one in-frame show with an
internal `E1` gap** — Star Trek: Prodigy, 19 episodes numbered to 20 — and **zero** with an internal
`E2` gap. Nineteen listed for a maximum of twenty means Trakt **omitted** the number rather than
listing a placeholder, which is the branch that leaves `L := |E|` correct. The artifact's own
wording is right: *"remains near-untested."* One show is not the answer; it is one data point, and
it is the first.

**A second Step 2 finding retires part of the original worry.** The four absolute-numbering shows
(*Naruto*, *Naruto Shippūden*, *One Piece*, *Hunter x Hunter*) had histories using the **same**
absolute numbers as the metadata — 100% overlap on all four — so **set membership handles that shape
and the withdrawn `1..F` range form would have failed on all four.** All four have since left the
frame via the 26-episode cap, so the evidence stands but the exposure is gone.

### O4. The `L2 = 1` / cadence-classification ordering is still written nowhere

At `L2 = 1`, `weekly_span = 0`, so `span ∈ {2, 3}` falls through C1 into **C2 "weekly"** under D12
first-match ordering — harmless only because `L2 = 1` shows are excluded, and the exclusion happens
at Step 8 while classification is available from Step 2.

**Does not arise on the current frame: `min(L2) = 2`, zero in-frame shows at `L2 = 1`.** Carried
because the ordering is still unwritten and **the frame changes if the pull resumes.** README item 7.

### README item 10 — the pool's bias, and the diagnostic that cannot detect it

Two mechanisms running the **same** way, **compounding rather than cancelling**, both pushing the
never-started share **down**:

- **Seeding** (`0008`): movie-commenting marks tracking intensity; heavy trackers are likelier to
  continue to S2, to log completely, and to survive the Step 7 liveness filter. Seeds were drawn
  **27 days after the TV Time shutdown** from recency-ordered feeds, so the frame oversamples the
  migration cohort **Step 5 exists to exclude** — and Step 5 removes it *after* the discovery budget
  is spent.
- **Liveness exclusion**, which `task-sheet.md` Step 14 already carries as its one downward bias.

**Step 11 as written cannot clear the study, only fail it.** Both channels select on public-facing
activity, so **agreement between them is not evidence of unbiasedness**, and agreement is the likely
outcome. The remedy is computable from `raw/step3/` at **zero further live calls** — but any such
diagnostic **must condition on *screened*, not *eligible***, or FIFO screening order (1,027 eligible
users never screened, skewed toward depth 2) reads as a depth effect.

**Direction check — PASS.** The liveness *bound* moves the headline **up**; the liveness *exclusion*
moves it **down**. Those are consistent, and it is the pair that is easiest to get backwards.

**Now three exclusions with declared directions, and they do not all run the same way:** seeding
**down**, liveness **down**, the `0010` tail cap **up** (0.93%, negligible in magnitude but named
because every other exclusion is), and Step 5's adopted exclusions **up** on net (ten Started pairs
removed per Never-started pair).

### README item 11 — Step 4 is not expected to finish the pool, and the pull is stopped

~210,500 calls, ~23.4 h. `0009` makes an early stop survivable and `0010` trims 1.7 h. **Whether to
resume or to sample the pool down remains unsettled**, and everything frame-derived moves if it
resumes (README item 19): the ≥50 candidate rule, every size-quintile boundary, the structural
threshold counts.

### README item 18(b) — `show_network` is a present-day value

Problem (a) is closed: per-season network **does** exist on the API and is **empty** — 0.71%
populated, dropped as a field (`0016`). **Platform fragmentation is not a variable in this study**;
no result may control for it, stratify on it, or rule it out. Problem (b) survives and has moved to
a different field: show-level `network` is 100% populated but records **today's** network, so a
title that moved services between seasons shows only its current one. **Must not be read as
release-time availability.**

### README item 2 — Step 1 §10.1 open questions 1 and 3

Still open. The Continued boundary and the right-censoring rule. Each carries a Data Scientist
recommendation and a decision from nobody. See [[step1-open-questions]].

### README item 24 — D14's warrant is false and 95 negatives have no account

`0003` D14 and Step 1 §9 both state every C1 lag is non-negative **by construction**. **689 are
negative**, identical counts from both Step 6 instances. **459 bind on the S1-completion term** —
`max()` can select it on a C1 show, so the warrant only ever covered half the operator — and **230
bind on the finale**, of which 135 are the known one-day UTC skew and **95 are unexplained, out to
−495 days**. On a same-day drop nothing should be watchable 495 days before the season exists.

**Worth ≤6 days of `W`, so not load-bearing for the number, but the warrant is false either way and
the 95 are an unexplained timestamp or metadata defect Step 8 should expect to meet again.** Open.

### README item 27 — Step 6 and Step 8 will not share a row set

**4 pairs in the 128,099 have a first S2 record at or after `τ_pull`.** Step 1 D11 says every such
record is discarded from every computation; Step 5 built the sample without that filter. Both Step 6
instances found them and both retained them, **correctly** — the spec directs taking the population
from the Step 5 artifact, and re-deriving it would have been the larger error. **None is in C1, so
`W` is unaffected** (107.0 with and without, verified rather than assumed). **Step 8 classifies on
the 201,900 under the frozen cutoff.** Unresolved, and it lands at Step 8.

### README item 25 — dual instances need distinct output namespaces

Run 1's two instances got byte-identical prompts — **correct, and it must stay that way** — but
identical default output paths, and collided: one instance's script was overwritten mid-run. **The
namespace is not part of the task description and separating it does not weaken the diff.** Applies
to Steps 7 and 9 (`data-scientist` / `-b`) and Step 8 (`analytics-engineer` / `-b`). No output was
lost, and the identical inputs are themselves evidence the collision never reached the computation.

### Critical path, updated 2026-08-12 after `0034`

Steps 1 (amended and re-approved), 3, 4 (stopped), 2, 5 and 6 are done. **Three gates closed of
five.** **Step 7 is next** — dual pair, spec now fixed by `0029` and `0034`, needs the stored
calibration and must not refit it, liveness anchored at `τ1`. **It is BLOCKED on one ruling: the
liveness percentile is proposed at the 99th and not adopted** (README item 30), and `0029` says
Step 7 must not launch until it is. Then Step 8 (dual, on the 201,900, the Layer 1 record tags,
`W = 108`, the `0029` filter order and the `A ⊆ A_H` invariant), which also inherits item 27's
four-pair conflict.

**The one thing to watch at each remaining gate** is unchanged and has now been paid for four times:
a ruling that changes what a downstream step computes has **three** homes — the decision log, the
gate's own deliverable, and **the spec the later step actually reads.** W1 argues there is a
**fourth**, the agent definition files, and that it has never been updated once.

### Stale pre-amendment expressions — conclusions survive, wording does not

Grepped every `.md` and `.py` for the pre-amendment Continued condition. **No live rule anywhere
still evaluates Continued at `τ1` on `A`.** `artifacts/step1-outcome-definition.md` §7 is amended in
place, `task-sheet.md` Steps 1, 7, 8, 13 and 14 all carry `τ2`, and the old row is quoted only under
an explicit **"Superseded by this amendment"** label. Five residues, none of which changes an
outcome:

| Where | Text | Status |
| :--- | :--- | :--- |
| `step1-outcome-definition.md` :875 | §7 opens *"Measured at the window close `τ1`"* | Half-true; the amendment block follows three lines later |
| `step1-outcome-definition.md` :935 | The `L2 = 1` degeneracy: *"`\|A\| ≥ 1 ⟺ F2 ∈ A ⟺` the Continued condition"* | **Conclusion still holds.** At `L2 = 1`, `A ⊆ {F2}`, so `\|A\| ≥ 1 ⟹ F2 ∈ A ⊆ A_H` and `\|A_H\| ≥ 1`. Moot on this frame — `min(L2) = 2` |
| `step1-outcome-definition.md` :516 | Listed-but-unaired S2 episode makes *"`F2 ∈ A` unsatisfiable"* | Holds a fortiori on `A_H` — the episode never aired at either bound |
| `step5-contamination-diagnostics.md` :59, `step5-red-team-reviews.md` :193 | The air-date-stamping argument runs on `F2 ∈ A` and `\|A\| ≥ ceil(0.90 × L2)` | **Holds a fortiori.** A fully stamped season lands before `T0 < τ1 < τ2`, and `A ⊆ A_H`, so it still scores Continued. An **approved gate** quoting a superseded form of the condition, with the direction unaffected |
| `step1-outcome-definition.md` :1157, `task-sheet.md` :372 | *"Hold `H` constant … otherwise **D3** and D8 are not comparable between arms"* | **D3** is superseded by **D3′**. Notably this exact line was the basis of failed anchor ground (b) at revision 8 |
| `src/step6_completion_lag.py` :9–12 | Docstring: *"Step 1 sec 7 makes **W** govern TWO boundaries"* and prints the pre-amendment Continued row | Its **output is unaffected** — it measures the completion instant at an unbounded horizon. But `0034` §10 names this file as the live provenance of §2's three rows, so a live-provenance script describes a superseded rule |

**The one thing to watch at each remaining gate**, from README item 23: a ruling that changes what a
downstream step computes has three homes — the decision log, the gate's own deliverable, and **the
spec the later step actually reads**. At Step 5 the first two were done and were not enough.

### 403 and 429 — one of three failure paths is live-tested

README item 9. **Step 4 has now run** and, per `artifacts/pool-coverage-check.md` §1, saw
`access_denied` **0**, `private_or_absent` **0**, `user_403_skipped` **0** across 102,798 persisted
history pages, every one a 2xx payload. **So Step 4 did not exercise the 403 rule either**, and
README item 9's wording — *"Step 4 is now the first exercise"* — is stale in the same way its
predecessor was. The retry-with-backoff branch remains the only live-tested path.

### N2, N4, N6 — carried unchanged, not re-verified this pass

N2 (D2 computed on definition (b) cannot count the (a)-style failure the §5 addendum points at;
**expect zero, and zero is not evidence of rarity** — now also README item 6). N4 (the
`episode.ids.trakt` disagreement mechanism is asserted and unobserved, and it is the mechanism D9's
split signature depends on — README item 5). N6 (the Step 0 file index is stale). Last verified
2026-08-11.

---

## Checks that PASS — recorded so they are not re-litigated

Verified 2026-08-12. Arithmetic reconciliations are in [[population-chain-steps-2-3-4]].

Verified after `0034`, on the three checks the Human Lead named:

- **No live use of the superseded `W` figures.** Every occurrence of 107 / 107.7135 / 37.6967 in the
  repo is one of four legitimate kinds: the Step 6 artifacts stating **their own** outputs under a
  header saying not to take `W` from them; `0024` and `0025` citing them as the divergence they
  resolved; `task-sheet.md` Steps 7, 8 and 13 citing them **to say they are not the adopted value**;
  and `0024`'s **[46, 107] Step 13 span mandate**, which is a range requirement and not a value.
  **Nothing quotes either as adopted.** The one clause that overreaches is W5.
- **No live citation of the cut §1.1 / §2.2 / §2.3.** Every reference sits in the §11–§21 disposition
  tables, which cite them by number as **history** — correct and intended — or in the status block,
  which states outright that they are cut and records the cut-restore-cut sequence. The one
  forward-facing pointer, §6.5's note, was corrected to name the **pre-strip** §1.1 explicitly.
  `src/amendment_corrections.py` retains the keys renamed `HISTORY_…_CUT_AT_REVISION_10`, so §11–§18
  stay reproducible without the figures reading as live.
- **`0034`'s zero-censoring claim survives Q3 being open.** Q3 asks `max(W, 91)` versus `W` alone.
  The identity `W + H ≤ max(W, 91) + H` holds under **either** answer, and at the adopted `W = 108`
  the two coincide exactly. They diverge only on the **low** Step 13 arms — at `W = 46`,
  `max(46, 91) = 91 ≠ 46` — where the retained population is **larger** under the adopted answer, so
  `A_H` stays fully observed either way. **Q3 cannot threaten the amendment.**

Verified after the Step 6 gate:

- **No live reference anywhere in the repo to the run-1 Step 6 artifacts.** Grepped every
  `step6-window-w` / `step6-lag` / `step6-w-derivation` / `instance-a` string: ten files, all of
  them either the current `-a` / `-b` deliverables, their sources, or decision entries citing run 1
  as history at commit `9c5fbd3`. **Removing them from the working tree was clean.**
- **`task-sheet.md` Step 14 is fully amended** — seven numbered bias statements each with mechanism,
  direction and source, eight non-bias limitations, and a preamble arguing *why* they must not be
  netted. **No description of Step 14 as a five-line checklist survives anywhere.**
- **`task-sheet.md` Step 13 carries all three arm mandates** — the two-curve range, the [46, 107]
  span with the reason it survives the definition being fixed, and the 150/213 arms with the
  direction named. `H` constant and the per-arm retained-row count are both still there.
- **The Step 6 population arithmetic reconciles.** Bucket pairs sum to 128,099; C1 ∩ 128,099 =
  25,120 = 19.6%; both instances' negative-mass tables are identical to the pair across all five
  buckets; 28,960 / 128,099 = 22.61% ✓.
- **220,107 completer pairs reproduce exactly by an independent path.** The discard-neutrality check
  recomputed the retained population's completers from a separate extractor and hit the figure
  carried by Step 2 and by the approved Step 5 rule. **The strongest single confirmation the frame
  count has received**, and it arrived as a by-product of a check aimed at something else.
- **The two record extractors agree exactly.** Raw-page and parsed-store extraction diffed on shared
  users gives zero raw-only and zero parsed-only records, on sets up to 9,273 triples — so the
  discarded-vs-retained comparison is not an artifact of reading from two stores.
- **Step 5's rule composes correctly with Step 1's filter order.** Adoption 2 excludes 1,542 pairs
  *on a censoring rationale*, applied as a **contamination** exclusion — and `task-sheet.md` Step 8
  requires contamination to run **before** right-censoring precisely so *"an import-stamped S1
  completion date is counted as contamination rather than laundered into a censoring drop."* The
  Step 5 rule is the first live instance of that ordering doing what it was written to do. Not a
  contradiction — a confirmation.
- **The §16 routing of the 720's bound figures to `revision4.json` is correct, not stale.** I
  checked the file directly: `processed/step5/revision4.json` was regenerated and carries **1,738 /
  1,717 / 1,762**, the corrected values. The 425 and 295 sub-rows also reconcile to the corrected
  **7.92%**, not the withdrawn 8.06%. **This was the obvious place for the unit bug to have survived
  and it did not.**
- **No superseded Step 5 exclusion figure is quoted as current.** The revision table labels 71,235
  / 24,609 / 1,542 as history; §9.5 recosts every rejected candidate on the adopted population and
  says so; §8 gives **both** denominators so the E6 correction is checkable.
- **"Clock start" is now used uniformly.** The B1 collision is fixed: Step 5 §7 states *"`T0` is the
  clock start; **S1 completion date** and **finale term** are its two inputs; **binding term** is
  whichever `max()` selects."* Grepped every `.md` in the repo — no remaining use of "clock start"
  to mean the S1 completion instant alone.
- **Step 2's rate discipline was verified, not asserted** — max **150** requests in any rolling 60 s
  window, checked against the persisted throttle ring. The run's own `shows_per_min` counter reading
  318 is a cumulative-average artifact of a front-loaded limiter and **not** a breach; the artifact
  says so, which is the right handling of a misleading counter.
- **Step 2's metadata integrity checks all return 0.** `episode_count` / `aired_episodes` / `|E|`
  agree on every in-frame show for both seasons. The listed-but-unaired hazard §3.4 predicted does
  not reach the frame — removed by the 31 Dec 2025 cutoff, **verified rather than expected.**
- **Privacy boundary intact.** All 2,549 usernames tested against every file in `artifacts/` and
  `decisions/`; only `right` and `orphan` match, both ordinary English words. Step 2 shows titles,
  which are public catalogue metadata. Account-keyed material stays in `processed/step5/` and
  `raw/`.
- **Zero API calls in Step 5 and all six of its revisions**, and zero in both diagnostics. The
  request log's last entry is the Step 2 shows pull; no `step5` run label exists. Step 2's rebuild
  cost is **0 calls** — all bodies cached.
- **`0012`'s residuals are not truncation**, on two independent proofs: page-count and item-count
  headers identical on every page of every sweep including one of 105 pages; and a `limit=100`
  re-sweep returned the **identical record set in identical order** as the cached `limit=250` sweep,
  1,459 distinct records both ways against a header claiming 1,460.
- **D12's fragility test passes on real data.** 7 shows within one day of a bucket boundary, 0.6% —
  so by D12's own test the thresholds are **not load-bearing** and a Step 13 arm on them is not
  indicated. The 238-within-three-days figure is not the right one: 220 of those are same-day drops
  whose distance is exactly 2 by construction.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[gate-step5-contamination]], [[population-chain-steps-2-3-4]], [[decision-log-step18]],
[[withdrawn-claims-register]], [[step1-open-questions]].
