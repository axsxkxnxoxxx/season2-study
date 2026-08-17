---
name: open-items-and-contradictions
description: Live register of open items and cross-step contradictions in the Season 2 study, each with its two conflicting sources named — fourth pass 2026-08-16 through decisions/0094 and the Step 8 gate block, with R1-R9 new (including an unrecorded seventh Red Team pass and a trap-table register that lives only in this memory)
metadata:
  type: project
---

# Open items and contradictions — fourth pass, through `0094`, 2026-08-16

---

## NEW — surfaced 2026-08-16 by the catch-up pass over `0065`–`0094`

**None of these is a disposition. Each names its two conflicting sources and stops.**

> **LABEL NOTE: this pass uses `R1`–`R9`. `W1`–`W5` are TAKEN** by the 2026-08-12 pass further down
> this file (the agent-definition findings, closed by `0035`). **A register that reuses its own labels
> cannot be cited.**

### R1. My own glossary forbade two figures the Step 8 spec MANDATES. **CORRECTED HERE, logged because it is surface 7**

- **`glossary-terms-and-thresholds.md`, until 2026-08-16:** *"Superseded counts, never to be restated
  as current: **PF-LIMIT's 751 (DERIV) and 1,355 (APPLY)**."*
- **`0085` §5, and `task-sheet.md` / both `analytics-engineer` files carrying it:** *"**703 is not the
  marginal cost of the silence test.** The silence test alone excludes **1,355** on APPLY; the
  `NOT Continued` conjunct spares **652**; `1,355 − 652 = 703`. **Both arms now publish both, on both
  populations, with the identity stated.**"* Measured in both arms at `0086` §4; DERIV is
  `751 − 652 = 99`.

**Both statements are about the same arithmetic.** PF-LIMIT **the rule** is superseded; **the count**
is conjunct 1 alone, and it is now a required line-6 decomposition. **A memory row reading *"never
restate"* against a spec clause reading *"both arms publish both"* is precisely the shape that produced
the wrong ruling at `0051` §2.** **Corrected in the glossary and given a trap-table row.**

### R2. **`decisions/` and `artifacts/` NUMBER THE RED TEAM PASSES ONE APART, and the same finding carries two numbers**

> **This entry was drafted wrong and is corrected here rather than deleted.** My first draft read
> *"the seventh pass has no record anywhere."* **False** — `seventh pass` occurs **74 times across 18
> files**, including `src/`, both arms' artifacts and `task-sheet.md`. **I had grepped `*.md` in
> `decisions/` and generalised from it.** This is exactly the class the register exists to catch, and
> it is [[feedback-verify-against-files]] applied to my own draft.

**The real contradiction, and it is checkable in two lines:**

- **`decisions/0091` §2:** *"OVERSTATED FOR ARM A. Corrected 2026-08-16, **Red Team sixth pass, F3**"*
  — the `+1` perturbation that *"fires identically on a same-mask denominator, so it would have passed
  on the very build whose defect it claims to have fixed."*
- **`artifacts/step8-invariants-a.md:9`:** *"**Red Team's seventh pass, finding 3**, established that
  this arm's `+1` perturbation does not test independence and would have passed on the build whose
  defect it claimed to have fixed."*

**One finding. Two pass numbers.** And the same offset appears at the other end:
**`artifacts/step8-waterfall-a.md:375`** attributes **N2** to *"`decisions/0092`, **Red Team seventh
pass**"* — while **`0092` itself names no pass at all**, and `0093` then calls the next one *"the
**eighth** pass."*

**So `0092` IS the seventh-pass entry and does not say so**, the sixth pass's findings live only as
in-place amendments inside `0089` and `0091`, and **`decisions/` and `artifacts/` are off by one on
which pass found the `+1` item.** **The two things that conflict are `0091` §2 and
`step8-invariants-a.md:9`.** **Low consequence for any figure; high consequence for a Step 18 reader
reconstructing the review sequence, which is the artifact.** Not mine to resolve.

### R3. The Step 8 trap-table figures exist in ONE hand-maintained place, and that place is this memory

- **`CLAUDE.md`:** *"The register of known false positives is maintained in
  `.claude/agent-memory/second-brain/glossary-terms-and-thresholds.md`; the decision entry that adds or
  withdraws a row cites it."* And, separately: ***"One register, in `src/step7_register.py`, imported by
  every script that checks. Two hand-maintained copies diverged by an entry after a single use."***
- **`src/step7_register.py`** holds `LEGITIMATE`, `SUPERSEDED`, `SUPERSEDED_IN`, `ADOPTED`,
  `DECLARE_SCOPED` — **all Step 7 values.** Its Step 8 coverage is **textual only**:
  `SUPERSEDED_STRINGS` and `SURFACE6_LINE_LOCAL_CONTROLS`. **`168`, `153`, `75`, `76`, `46,428`,
  `726,102`, `1,246`, `71`, `20` and the second readings of `703` and `604` are NUMERIC entries with no
  numeric register.**

**So the Step 8 half of the trap table is a second hand-maintained register in exactly the sense `0059`
B3 forbids** — and it is the one a control cannot import. **The two things that conflict are
`CLAUDE.md`'s two rules about where the register lives.** **Raised, not resolved.**

### R4. A line-local control on `747,478` passes only off an incidental word

- **`src/step7_register.py`,** `SURFACE6_LINE_LOCAL_CONTROLS["747478_is_a_PAIR_count_not_a_ROW_count"]`:
  *"every line mentioning 747,478 must be marked as superseded, **or must characterise it as distinct
  `(user, show)` PAIRS.**"* — plus the needle `"747,478 and 726,103 are different objects"`.
- **`artifacts/step8-waterfall-a.md:434`** carries **that exact needle** and **contains no `pair`**. It
  is exempted because `SURFACE6_MARKERS` matches the word **`defect`** in the line's unrelated closing
  sentence, *"One name over two quantities is the defect."*

**The line is legitimate — the table three lines below gives the correct axis.** **What is not
legitimate is the route by which it passes.** **This is the "passing only by accident" shape `0094` §3
found twice**, in the same control family. **Not mine to fix.**

### R5. `0093` lists `153` among D9's numbers; every measured `153` in the current build is D2's

- **`0093` §3(a):** *"D9's numbers are **0, 75, 76, 6, 27 and 153**."*
- **Both arms' current builds:** `153` is **D2's `max()` BOTH-BIND tie count on DERIV** —
  `step8-waterfall-a.json:1311` and `:1320`, `step8-waterfall-b.json:761–762`, at 147,370 and 147,271.
  **D9's published quantities are `[0, 75]`, `[0, 6]`, `[0, 27]`, the third key's `76` and `28`, and
  the universe sizes.** **I find no D9 `153` in any current artifact.**

**Low consequence — it sits in an aside arguing a different point — but it is a figure attributed to
the wrong diagnostic in the log of record**, and `153` is exactly the figure `0092` §3 had just
established as the one nobody had recorded. **The two things that conflict are `0093` §3(a)'s list and
both arms' D9 blocks.**

### R6. A published artifact's citation-resolver coverage is one entry short of `decisions/`

- **`artifacts/step8-waterfall-a.json:2007`:** `"decisions_entries_on_disk_total": 93`, in build
  **`a/2026-08-16-0094`**.
- **`decisions/` holds 94 entries**, `0001`–`0094`, none missing.

**Consistent with `0094` §4** — the entry did not exist when the arm ran. **It is nonetheless a
coverage count published under a build tag naming an entry the count could not see**, which is the
provenance class `0078` §2 exists for. **Closes on the next rerun; recorded so it is not read as a
gap in `decisions/`.**

### R7. The Mode H letter now names two different failure modes

- **`withdrawn-claims-register.md`, since 2026-08-13:** **Mode H = an asserted action or property that
  was never taken or never held.** Ten instances in nine entries, cited by letter in three memory files.
- **The Human Lead's briefing, 2026-08-16:** *"**Mode H** matters here: where an entry withdrew a
  **ground** rather than a figure."*

**I added the ground-withdrawal class as Mode I rather than renumber H.** **The Human Lead names the
letters.** See [[withdrawn-claims-register]].

### R8. Two items carried for the Human Lead at the Step 8 gate and still open

- **The D9 tie-break** — six keys tie at 6, the arms publish different third places, both correct under
  their own rule, and **`0088` §3 named a seventh answer neither arm produced.** Red Team's position:
  publish all six and retire *"third-largest."*
- **Whether `specs/` becomes a NINTH propagation surface.** It holds the written specs handed to
  isolated instances, **nothing checks it**, and it carried *"Step 8 has not launched"* through **four**
  occurrences. Red Team's position: adopt it.

**Both are `0089` §4. Neither blocks per Red Team. Both are unruled.**

### R9. `0091` §1's residual is answered by one arm and not the other

- **Arm a, build `a/2026-08-16-0094`** (`step8-waterfall-a.json`): states at each cell whether conjunct
  2 was recomputed on the counterfactual outcome — *"if conjunct 2 were held at the adopted outcome,
  `703 → 703` would be an IDENTITY and would establish nothing. A reader cannot tell a measurement from
  a tautology unless the deliverable says which, so it says which."*
- **`0091` §1:** *"**Arm B does not report the liveness count under the counterfactual, so there is no
  second arm to settle it.**"*

**One arm has closed it; the pair has not.** **A single-arm answer is not a dual result**, and the
604/99 split under the counterfactual **is still reported nowhere.**

---

## NEW — surfaced 2026-08-13 by the pass over `0055`–`0064`

**None of these is a disposition. Each names its two conflicting sources and stops.**

### T1. A withdrawn ARGUMENT survived in this memory for nine entries, and no control could see it

- **`0055` §2 withdrew `0054` §3's margin argument as cherry-picked**, in terms: *"p5 supported the
  claim, the median contradicted it, and only p5 was quoted"* — the same 90 pairs have **p5 = 1.6552 and
  median = 44.5272**, and *"the correct ground carries no margin statistic at all."*
- **This memory carried it as live supporting reasoning in three files until 2026-08-13** —
  `glossary-terms-and-thresholds.md`, `gate-step7-liveness.md` and `withdrawn-claims-register.md`, each
  stating *"the 90 have p5 margin 1.7 days, minimum 0.13."* **Corrected in this pass.**

**Why it is worth a register entry rather than a silent fix.** It is **the B8 blindness class on surface
7**: a withdrawn *argument*, not a withdrawn figure. **It carries no superseded number** — 1.7 and 0.13
are correct statistics, withdrawn only as *grounds* — **and it is in no `WITHDRAWN_PHRASES` row**, so the
numeric half of `check_surfaces.py` sees nothing wrong and the phrase half has no key to match. **The
same shape `0062` §4 named for the covering qualifier: *"a missing qualifier is neither a wrong number nor
a withdrawn claim."*** Here it is the mirror image — a **present** claim that is neither.

**The two things that conflict are `0055` §2 and this memory's own three copies.** Whether a
`WITHDRAWN_ARGUMENTS` band should exist alongside `WITHDRAWN_PHRASES`, and whether this counts as a
numbered propagation failure on surface 7, are the Human Lead's calls.

### T2. Two files still name this glossary as the canonical register; the source says otherwise

- **`src/step7_register.py` docstring**, from `0059` B3: *"there were TWO hand-maintained registers…
  Two registers is one register plus a defect waiting. **Everything that decides whether a number is
  correct lives here and nowhere else.**"*
- **`artifacts/step7-liveness-bb-{a,b}.md:3`**, the hand stamp: recorded at **`0063` §3 item S7** as
  *"stale and names the glossary as canonical register — **B3's two-registers defect reinstated in
  prose**, outside `BEGIN…END`, carrying no number and no phrase so no control sees it."*

**Carried by `0063` as an outstanding control defect, not fixed.** Recorded here because **the other half
of it was mine**: this glossary's trap table was headed *"REGISTER — canonical location"* until
2026-08-13. **That half is corrected** — the table now states that `src/step7_register.py` governs and
the glossary mirrors it. **The `artifacts/` half is untouched and is not mine to touch.**

### T3. The approval and the entry its central figure rests on are dated a day apart

- **`artifacts/step7-gate-approval.md`** and **`decisions/0064`**: dated **2026-08-13**, *"as stated by
  the Human Lead."*
- **`decisions/0060`–`0063`**: dated **2026-08-13** — **including `0063`, which carries the 652
  measurement the approval's §3 rests on.**

**Already flagged in the approval itself**, which records it rather than silently adjusting it and says
neither is fixed without a ruling, since **`0058` §6 corrected a date drift in the other direction** (all
of `0052`–`0057` had been dated a day ahead). **Noted here so it is not lost between the artifact and the
log.** **Not mine to resolve.**

### T4. The propagation-failure count is still stated against five surfaces in every consuming file

- **`0057` §7:** *"All eighteen numbered propagation failures were found on surfaces 1–5… **The count is
  not renumbered — 18 is a true count of surfaces 1–5 — but it must never be published as a total**,
  which is how it reads without the bullet now in Step 14."*
- **`0044` §3.1, README item 46, `0050`, `0052` §5, `0054` §5** all count against **five surfaces**, and
  **README item 46 still reads "five times now."**

**`0055` §5b logged this as U2 and `0057` §7 carried it to Step 14 as measured and non-zero at three
(#19, #20, #21). Whether the count should be restated against seven surfaces was explicitly left
undecided** — *"not decided here"* (`0055`), *"the count is not renumbered"* (`0057`). **It is the Human
Lead's call and it is still open.** The two things that conflict are `0057` §7's counting rule and README
item 46's wording.

### T5. V8's nine superseded artifacts are now handled by an ALLOWLIST, not by a forward pointer

- **V8, below:** nine superseded Step 7 deliverables in `artifacts/` publish 632 d, 1,293 d, PF-LIMIT and
  ALT as their proposals **with no header naming what superseded them**, and `step7-liveness-alt-a.md`
  line 162 carries *"the exclusion set is empty on DERIV at every arm from 38 to 213"* — **the exact
  claim `0049` defect #4 called false in five files** — live and unmarked in a public artifact.
- **`src/step7_register.py` `WHOLLY_SUPERSEDED_FILES`** now names each of them by name with a reason,
  e.g. `"step7-liveness-alt-a": "the ALT rule, superseded by ALT-BROAD (0048)"`.

**These are different remedies for different readers and only one of them has been applied.** The
allowlist tells **the control** to stop flagging the file; **a header would tell a HUMAN reader the file
is superseded and by what.** `0029` put such a header on both Step 6 artifacts and
`artifacts/s1-completer-diagnostic.md` opens with one, so the repo's own practice exists. **The two
things that conflict are `WHOLLY_SUPERSEDED_FILES`'s coverage and the files' own unmarked headers.**
**Recorded, not disposed** — V8 may well be intended to stay open now that Step 7 is closed.

---

## STATUS of U1 and U2, re-checked 2026-08-13

- **U1 (`0054` §7 published the superseded `0.4033` rounding artifact its own §6 named): APPEARS ACTIONED.** `0055` §5
  corrected `0054` §7 in place to **0.4032 pp**, and separately found **the same artifact had survived in
  `task-sheet.md`** after being fixed in the decision entry — *"the correction landed in the decision
  entry and not in the file an agent reads, which is the failure this entry exists to control, committed
  inside it."* **Found by the `analytics-engineer`, which declined to fix it because its brief said not
  to touch the APPLY figures, and reported it instead.** `0.4033` is now a `SUPERSEDED` row with
  successor `0.4032`. **The two-arm divergence itself still stands unreconciled, correctly** — it is the
  ratio conventions, residual item 9.
- **U2 (surfaces 6 and 7 added after the count was fixed): CARRIED, and now measured.** See **T4**.

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry names its two sources so the Human
Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it. Several close by
ordinary progress rather than by a decision.

**The decision log of record is `decisions/`** — `README.md` plus `0001`–`0064`. Where a decision
file and this memory differ, `decisions/` governs on who decided what and when; the deliverable it
approves governs on substance. I never edit `decisions/` — I report.

**And where an ARM'S OWN OUTPUT differs from my reconstruction, the arm's output governs.** Added
2026-08-13 after V7. **A figure I cannot reproduce is first a claim about my reconstruction.** Check
the arms' JSON by key before recording a figure as unreconstructible — that is the same check mode B
has demanded four times, and it is why `0052` §2 exists.

---

## NEW — surfaced 2026-08-13 by the pass over `0051`–`0054`

### U1. `0054` publishes the rounding artifact its own §6 names as one

- **`0054` §6**, reporting an unreconciled divergence: *"Bound width: **A gives 0.4032 pp exact
  (793/196,654)**; B gives **0.4033 pp, differenced from rounded endpoints**, and computes its ratios
  from it. `0053` §6 promoted B's 52.7% ratio into the record — **it is a rounding artifact and is
  withdrawn**."*
- **`0054` §7, one page later:** *"The started-and-left bound is [9.6372%, 10.0405%], **width 0.4033
  pp**, both endpoints on 196,654."*

**The two things that conflict are `0054` §6 and `0054` §7, inside one entry.** `793 / 196,654 =
0.40325%`, so **0.4032 is the exact figure** and §7 states the artifact. **Same shape as `0052` §2's
own finding one entry earlier** — a correcting entry restating the thing it corrected — and the
divergence is one `CLAUDE.md` requires be reported and **not** reconciled, so the arms' disagreement
stands; only the entry's own choice of endpoint is at issue.

### U2. Surfaces 6 and 7 were added to `CLAUDE.md` after eleven propagation failures, not before

- **`CLAUDE.md` §Propagation, added 2026-08-13:** seven surfaces, of which **6 is `artifacts/`** and
  **7 is `.claude/agent-memory/second-brain/`**, with the note on 7: *"it is fed back into rulings, and
  stale memory has already caused a wrong one."*
- **Every propagation-failure count in the record — `0044` §3.1, README item 46, `0050`, `0052` §5,
  `0054` §5 — is stated against the FIVE-file surface.** Failures #1–#13 were all counted, found and
  fixed on surfaces 1–5.

**Not a contradiction of substance — a scope that changed after the count was fixed.** Recorded
because **the failure rate on surfaces 6 and 7 is unmeasured, not zero**: `artifacts/` carries nine
unstamped superseded Step 7 deliverables (**V8**, still live as far as I have checked), and surface 7
carried a two-generations-stale rule status into a ruling. **Whether the thirteen-failure count should
be restated against seven surfaces is the Human Lead's call, not mine.**

---

## The `0035`–`0050` pass — V1–V11. Most were actioned by `0051`. Re-checked 2026-08-13.

**Context for all of these: the propagation surface has now failed TWENTY-TWO times** *(21 through
`0064`; **`#22` is `0084`**, in the Step 8 block)*. **`#1`–`#18` is a
SURFACES-1–5 count and must never be published as a total** (`0057` §7); **#19 and #20 are on surface 6,
#21 is on surface 7 — this memory.** **Both halves of every dual pair have carried each defect
identically**, so the dual-implementation diff cannot catch this class at all. Full arc in
[[gate-step7-liveness]].

> **Status re-check, 2026-08-13, by grep only, during a window in which the spec files are being
> edited by others — so these readings may be mid-flight and none is a disposition.**
>
> - **V1 (ALT's 485 → 716 series ordered at Step 13):** both `data-scientist` files now read *"ALT's
>   485 → 716 series is SUPERSEDED and must not be ordered — it was still here at line 122 while…"*.
>   **Appears actioned.**
> - **V2 (`decisions/README.md` has no row for `0050`):** the index now matches `0050`–`0054`.
>   **Appears actioned.**
> - **V3 (gate checklist states PF-LIMIT as the rule): CLOSED, verified 2026-08-13.** `decisions/README.md`
>   line 93 now reads *"**Step 7** liveness rule — **APPROVED by the Human Lead, 2026-08-13** ([0064]…).
>   **ALT-BROAD: not live iff no insertion after `τ1` AND NOT Continued**, silence anchored at `τ1` and
>   only at `τ1`, channel window `(τ1, τ2)` open… **Approval is UNCONDITIONAL with the §4 residual open
>   and published**"*, with both bounds and both exclusion counts. **The PF-LIMIT sentence is gone and
>   the box is ticked.** The Step 5 line also records the `0053` amendment and its same-day withdrawal.
>   **Step 8 is the one unticked box.**
> - **V4 (README items 30/31 unstruck):** item 30 now carries `~~…~~ **CLOSED**`. **Appears actioned.**
> - **V7:** **not open — it was wrong.** See below.
> - **V5, V6, V8–V11:** not re-verified this pass. **V8 in particular is now surface 6 of seven**
>   (`CLAUDE.md` §Propagation) and its nine unstamped Step 7 deliverables are the first named instance
>   of a surface the count never covered.

### V1. Both `data-scientist` files order ALT's superseded per-arm series at Step 13

**The sharpest finding of the pass. It is `0050` defect #4, fixed in three places and surviving in a
fourth — in the same two files, seventy lines below the corrected copy.**

- **`.claude/agents/data-scientist.md` and `data-scientist-b.md`, line 122 (Step 13), byte-identical
  in both halves:** *"**report the liveness exclusion count per `W` arm on APPLY** — **485 at
  `W = 38` to 716 at 213** (`0046`)."*
- **The same two files, line 68 (Step 7):** *"**537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** at
  `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 (`0048`)."*
- **`task-sheet.md` line 417 (Step 13):** the ALT-BROAD series, followed by *"**(ALT's 485 → 716
  series is superseded and must not be ordered.)**"*

**So the instruction the task sheet explicitly forbids is the instruction the agent definition file
gives, for the same step, on the same population.** `0050` §1 defect 4 recorded this exact string —
*"Report the **ALT** exclusion count per arm: 485 to 716"* — as *"self-contradictory on its face, in
`task-sheet.md` and both `data-scientist` files"* and fixed it. **The Step 7 occurrence was fixed;
the Step 13 occurrence in both files was not.**

**Why it matters more than its size.** Step 13 is Chained and single-implementation, so the failure
mode is **plain omission with no diff to catch it** — the same mode `0028` was written for and W2
was. And `CLAUDE.md` sends the agent to its definition file **first**. A Step 13 instance following
line 122 reports the superseded ALT series and, per `0048` §7's own warning about unlabelled arm
tables, **would file a false divergence against anything computed from the task sheet.**

**The two things that conflict: `data-scientist.md` line 122 and `task-sheet.md` line 417.**

### V2. `decisions/README.md` has no index row for `0050`

- **The index table ends at `0049`** (line 63). Every entry from `0001` has a row.
- **`decisions/0050-step7-propagation-pass-and-channel-measurement.md` exists**, is Closed, and is
  the entry that fixed six defects across all five propagation files, routed three limitations into
  Step 14, and measured the 297-pair channel.

**The decision log of record does not index its own most recent entry, and that log is the Step 18
artifact.** `0050` is also the only source for the 297-pair channel measurement and for the
two-ceilings sentence — a reader working from the index alone reaches neither.

### V3. The README's gate checklist states PF-LIMIT as the rule, two rule changes late

- **`decisions/README.md` line 78:** *"**Step 7** liveness rule — **RULE CHANGED to ALT 2026-08-13
  ([0046]); reruns pending, gate OPEN.** Previously approved **with NO free parameter** ([0042]).
  **A pair is not live iff the account shows no insertion instant after `τ1`.**"*
- **`decisions/0048`:** ALT-BROAD adopted 2026-08-13 — *not live iff no insertion after `τ1` **AND
  NOT Continued**.* **`0044`** withdrew *"no free parameter."*

**The sentence quoted as the rule is PF-LIMIT**, superseded twice — by ALT at `0046` and by
ALT-BROAD at `0048`. **The gate status (OPEN) is right; the rule is two generations stale**, and this
is the checklist a reader consults to learn what was decided. Same class as `0048` §6's line 332,
one file over.

### V4. README items 30 and 31 read as live blockers on a step that has run five times

- **`decisions/README.md` item 30, unstruck:** *"The Step 7 liveness percentile is proposed at the
  99th and not ruled. **Step 7 must not launch until it is.**"* **Item 31, unstruck:** *"The liveness
  rule's shape is unsettled… Whether the test applies to a **single** gap, to the gap **bracketing
  `T0 + W`**, or to **every** gap in the sweep is not settled."*
- **`decisions/0036`'s own header:** *"**Closes:** The unruled threshold percentile (README item 30)
  and the unsettled rule shape (item 31) — the two things blocking Step 7."*

**Both were closed by name, by the entry that unblocked the step, and neither was struck.** Item 31
is doubly stale: the shape question was settled at `0036` §2 (the bracketing gap), and **the
percentile it turns on was deleted entirely at `0042`.** Every other closed item in that list carries
a `~~strikethrough~~` and a CLOSED note, so the convention exists and was not applied.

### V5. `task-sheet.md` Step 14 bias 2 restates a figure it withdraws four lines below

**This is `0050` defect #1's exact shape — fixed for one figure, live for another, inside the bullet
`0050` rewrote.**

- **Line 453:** *"Applying liveness moves the never-started share **from 6.2055% to 6.2373% — UP by
  0.032 pp.**"*
- **Line 456, three lines below:** *"**DERIV** … **UP 0.0042 pp**, 6.2055% → **6.2096%**."*
- **Line 457, four lines below:** *"the figures −0.2558 (ALT) and **−0.192 / 0.032 (PF-LIMIT)** are
  all **withdrawn and must not be restated.**"*

**6.2373% and 0.032 pp are PF-LIMIT's DERIV figures.** The bullet states them as the measurement,
gives a different DERIV measurement three lines later, and then forbids restating the first one.
`0050` §1 caught precisely this — *"seventeen lines below, the same section said −0.2558 must not be
restated"* — and corrected the `−0.2558` instance while leaving the `0.032` instance in the lead
sentence.

**Step 14 is the study's central honesty artifact and this is its bias ledger.**

### V6. The same bullet describes PF-LIMIT as "the approved rule"

- **`task-sheet.md` line 459:** *"the threshold rule's 1,282-pair exclusion set, of which **the
  approved rule's 751** are the open-ended subset."* **Line 461:** *"**seven in seven of the 751**
  have positive S2 evidence, and **six in seven — 652** — are confirmed continuers… **Report the
  bound over the never-started exclusions only** (`0045`, Option C)."*
- **`decisions/0048`:** ALT-BROAD is the adopted rule; **PF-LIMIT is superseded**, and its exclusion
  set on DERIV was 751. **`0048` §6** recorded line 444 — *"'Option C' and 'seven in seven of the
  751' — PF-LIMIT as operative"* — as **superseded and fixed**.
- **`0049` §2 and `task-sheet.md` line 341** require a **second** bound **over all 703**.

**The text `0048` §6 recorded as fixed is present without a supersession marker**, and line 461's
instruction ("the never-started exclusions only") is the pre-`0049` disposition. Also **`0048` §4
corrected "751 directly observed" to 652 observed / 99 null-based**, and line 461's "seven in seven /
six in seven" framing is the merged form `0045` §4.3 was written to split.

### V7. WRONG, AND IT CAUSED A WRONG RULING. Corrected 2026-08-13 by `0052` §2 and `0054`.

**This entry is retained in full because it is the study's clearest case of stale memory being fed
back into a ruling. It is not an open item. It is a closed error of mine.**

**What was true AS OF `0052`, and is now SUPERSEDED — all figures in this paragraph are the
pre-widening ones** (`0058`; the adopted Continued ceiling is **73.6995%** = `(144,140 + 703 + 90) /
196,654`, and the three ceilings sum to **100.7104%**). **73.6537% was the Continued CEILING on APPLY:
`(144,140 + 703) / 196,654`.** It states a population, it reconstructs exactly, both deliverables
published it, and both JSONs carried `ceiling_pct: 73.6537…` *(SUPERSEDED — both now carry 73.6995,
regenerated from the counts by `0059`)*. So the original sentence was right and
**the sum was THREE ceilings, not two**: 16.9704 + 10.0405 + 73.6537 = 100.6646%. **The postmortem's
point is the mislabelling, not the value, and the value has since moved.**

**What I got wrong, in three steps.**

1. I recorded it as *"the Continued **floor**"* — **it was never a floor** — and reasoned from the
   floor reading that a floor above the point estimate is anomalous.
2. My reconstruction used **144,141** for Continued; the arms use **144,140**. On 144,141 the ceiling
   is 73.6542% and does not match, which is what made it look unreconstructible.
3. I concluded *"I could not reconstruct it, and it is the one figure with no stated population."*
   **I did not check the arms' JSON, where the figure and its key were sitting.**

**What it cost.** **`0051` §2 adopted this diagnosis without checking it against the arms' own JSON**
and asserted *"73.6537% is on no population"* *(the figure is itself SUPERSEDED by 73.6995%, `0054`)* — `0052` §2 calls that *"the exact failure `0046` §0
exists to prevent, committed in the entry that corrected two other instances of it"* — **and
attributed the number to Red Team while doing so.** The correction was worse than the error: it left
`task-sheet.md` presenting Continued as a **point, 73.2962%**, with the parenthetical *"no Continued
pair is ever excluded."* **That parenthetical is true and does not license it: Continued has a ceiling
precisely because any EXCLUDED pair may in truth be Continued.** **A Step 9 instance reading the
corrected line against its own deliverable would have hit a direct contradiction and deleted a correct
number.** `0051` §2 is withdrawn in full.

**What is true now.** **73.6537% is itself superseded to `73.6995%` = `144,933 / 196,654` =
`(144,140 + 703 + 90) / 196,654`** (`0053` §4, retained by `0054`), because the same 90 that widened
the started-and-left floor may in truth be Continued. **On DERIV the Continued ceiling is `82.4930%` =
`121,570 / 147,370`.** **The three ceilings sum to 100.7104%**, excess **0.7104 pp = 1,397 pairs =
2 × 604 + 189** — each never-started exclusion in all three numerators, each started-and-left exclusion
in two. **`100.66%` is superseded and must not be restated.**

**The lesson, and it is the reason this stays in the register:** `0050` §5 recorded that **Red Team
re-derived the arithmetic independently and cleared it**, and I flagged it anyway on the strength of my
own failed reconstruction. **A figure that an independent reviewer has cleared and that I cannot
reproduce is first a claim about my reconstruction, not about the figure.** The check that would have
settled it — grep the arms' JSON for the key — is the same check mode B has demanded four times.

### V8. Eight generations of Step 7 deliverables sit in `artifacts/` with no forward pointer

**This is Z3 at Step 7, and `0029` already established the remedy.**

- **`artifacts/` holds twenty Step 7 markdown deliverables** across the runs labelled *(none)*, `2`,
  `3`, `4`, `sensitivity`, `alt-rule`, `liveness-alt` and `liveness-bb` — **only the `bb` pair is
  ALT-BROAD.** The rest publish **632 d**, **1,293 d**, **PF-LIMIT** and **ALT** as their proposals.
- **Grepped `step7-liveness-a*.md` for `0048`, `0049`, `0050` and `ALT-BROAD`: zero matches.** No
  superseded generation points forward.

**Every one is correctly headed "PROPOSED, NOT ADOPTED", and that framing is right and should not be
changed** — the issue is that they are the **public deliverables of a gate whose rule changed four
times**, with no header naming what superseded them. Concretely:
`artifacts/step7-liveness-alt-a.md` line 162 reads *"The exclusion set is empty on DERIV at **every
arm from 38 to 213**"* — the exact claim **`0049` defect #4 called false in five files** — live and
unmarked in a public artifact. Same file, line 37: *"`τ2` plays no part"*, withdrawn by `0049` #1.

**The repo's own practice is to annotate:** `0029` put a header on **both** Step 6 artifacts, and
`artifacts/s1-completer-diagnostic.md` opens *"This supersedes the 2,134-user snapshot."* **Nine
superseded Step 7 artifacts got no such header.**

### V9. `decisions/0034` still states the clause `0049` withdrew
### CLOSED, verified 2026-08-13 — amended in place with a marker, exactly as `0048` §8 requires

**`decisions/0034` line 35 now reads:** *"~~`τ2` plays no part in the liveness test.~~ **AMENDED
2026-08-13 (`0051`): under ALT-BROAD `τ2` DOES play a part** — the rule's second conjunct is the
**Continued** test, read at `τ2`. **What this ruling actually fixed, and what stands, is that the SILENCE
test is `τ1`-anchored**, which is what ALT-BROAD implements. The rule reads two instants: silence at
`τ1`, Continued at `τ2`."* **Strikethrough plus marker plus the surviving substance — the convention was
applied.** Original entry retained below for the reasoning.

- **`decisions/0034` line 35:** *"…which is tested at `τ1`. **`τ2` plays no part in the liveness
  test.** Written into the Step 7 spec so…"*
- **`decisions/0049` defect #1:** *"`task-sheet.md`'s **'`τ2` plays no part'** — **false under
  ALT-BROAD**, since the second conjunct **is** the Continued test, read at `τ2`. **Withdrawn.**"*

**The clause was withdrawn from `task-sheet.md` and not from the gate document that originated it.**
`0034` is an **approved gate amendment** and `0048` §8 sets the convention: `decisions/` entries are
*"amended only in place, with markers."* Six other entries carry exactly such markers; this one does
not.

**Substance survives and should be stated when this is raised:** `0034` §6.3's actual ruling — that
the **silence test** is anchored at `τ1` — is intact and is what ALT-BROAD implements. Only the
sentence's scope is now too broad. **Low consequence, but `0034` is the document a Step 18 reader
opens to learn the anchoring ruling.**

### V10. README item 46 undercounts its own pattern by four, and is missing the third control

- **`decisions/README.md` item 46:** *"A ruling lands in a decision entry and not in the file the
  agents read — **five times now**"*, sharpened *"after a **sixth** instance"* and extended twice
  through `0047`.
- **The actual count is nine:** #7 (`0046` §6, the withdrawn instruction surviving in the two files
  `0044` had itself named), #8 (`0048` §6, five stale task-sheet lines including **line 332 carrying
  a superseded bound as operative Step 9 instruction**), #9 (`0050` header, **six defects live in
  all five files, produced by `0048` and `0049` themselves**).
- **And `0049` §6 added a third control that item 46 does not carry:** the **agent-launch snapshot
  hazard** — a definition is snapshotted at launch, so a file edited and an agent launched in the
  same turn disagree and **the agent cannot see it is holding an old copy**. `0049` calls it *"the
  third control added to the propagation problem"* and names the practice: **the launch prompt, not
  the definition file, is the authority at launch.**

**The item exists to make the countermeasure a standing obligation. It is the one place a future
reader learns the surface has failed — and it understates the failure rate by nearly half.**

### V11. `0029`'s Open status is overtaken rather than closed

- **`decisions/0029` is recorded Open** *"on the Step 7 percentile only"*, and README item 30 repeats
  it.
- **`0036` ruled the percentile (99th); `0042` deleted the threshold entirely.** There is no
  percentile to rule.

**Not a contradiction of substance — a status that no longer describes anything.** Flagged because
`0029` and `0041` are the only non-Closed entries in a fifty-entry log, and one of the two is open on
a question that no longer exists. **The other, `0041`, is Open by its own status line** and was
superseded by `0042` the same day.

---

## CLOSED by `0035` — four of the five findings from the 2026-08-12 pass

| Was | How it closed |
| :--- | :--- |
| **W1** — the agent definition files were never amended, and `CLAUDE.md` points agents at them first | **CLOSED as `0035`**, in the strongest available form: *"the agent definition files are **live spec**, not vestigial launch briefs."* All four pipeline files amended; both pairs verified byte-identical apart from `name:`. **`0035` §1 adopted the argument I raised** — *"a dual pair whose two halves read the same stale brief produces a clean diff and a wrong answer, and the diff is the only instrument this study has for catching a spec defect."* The surface is now formally **five files** (item 46, sharpened at `0044` §3.1). **Residue: V1**, a Step 13 line in the same two files |
| **W2** — `task-sheet.md` Step 10 never received `0034` | **CLOSED as `0035` §3.** All three requirements added: `p` on `A_H` in the rank form, the earlier-shifting direction named, the `p = 1.0` residual re-reported. Verified present at `task-sheet.md` lines 365–367 and in both `data-scientist` files |
| **W3** — "Step 2's marginal-lag distribution" for a figure Step 2 does not contain | **CLOSED as `0035` §4**, corrected in all three places. `task-sheet.md` line 480 now reads *"**§2 of the amendment** — not Step 2, which is the frame ledger and has no lag distribution"* |
| **W5** — the Step 6 headers' "unaffected by the rendering" clause overreaches | **CLOSED as README item 44**, which states the finding in the register's own terms |
| **W4** — Q1's warrant turns on D3, which `0034` abolished | **STILL OPEN.** Carried as README item 43. `0035` did not reach it and does not claim to. See [[step1-open-questions]] |

**`0035` credits `second-brain` in its *Occasioned by* field — the fourth such entry after `0022`,
`0028` and `0029`.** Recorded without comment: the role is continuity, and the log is the Human
Lead's.

---

## Superseded — the `0029`–`0034` pass of 2026-08-12, retained for the reasoning

**W1, W2, W3 and W5 are CLOSED by `0035` (table above). W4 is still open.** The original text is kept
because W1's argument became `0035`'s stated ground for treating the agent files as spec.

### W1. The agent definition files were never amended, and CLAUDE.md points agents at them FIRST
### CLOSED as `0035`, 2026-08-13

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

### Critical path, updated 2026-08-13 after `0064`

Steps 1 (amended and re-approved), 3, 4 (stopped), 2, 5, 6 and **7** are done. **FOUR gates closed of
five. STEP 8 IS THE ONLY GATE LEFT AND IT MAY NOW LAUNCH.** **Step 7 ran nine times and is
APPROVED** (`0064`, Human Lead, 2026-08-13, **unconditionally, residual published**) — approved at
`0039` and suspended, approved at `0042` and reopened, rule changed at `0046`, at `0048`, at `0052`,
**changed back at `0054`**, and approved a third and final time after **fifteen Red Team reviews, all
fifteen HOLD.** **Reviews 1–8 contested the rule; reviews 9–15 contested the record, and not one of
them changed the rule, the population, the exclusion counts or any bound endpoint.**

**The rule is ALT-BROAD**, restored and approved: *not live iff no insertion instant after `τ1` **AND**
not Continued.* **Silence anchored at `τ1` and only at `τ1`** (`0034`, `0051`, `0054`); **the channel
window is `(τ1, τ2)`, OPEN at `τ2`** (`0057`). **The
started-and-left bound is widened** to cover the 90 APPLY / 89 DERIV channel pairs that may in truth be
Continued: **APPLY [9.6372%, 10.0405%]**, **DERIV [11.3015%, 11.4291%]**. **Gate 2 (`0021`) was
amended by `0053` and the amendment reverted by `0054` the same day** — it stands as approved.

**When Step 8 does launch** it is a dual pair on **APPLY = 196,654** (line 1 less D10), the Layer 1
record tags, `W = 108`, the `0029` filter order with **liveness at position 6 and outcome assignment
at 7**, the `A ⊆ A_H` invariant, the `>=` monotone invariant, **line 6 reported as
outcome-conditional**, and **703 as the expected exclusion count — a mismatch is a population defect
before an implementation one. Producing 604 means ALT was implemented; producing 793 means ALT-MATCHED
was; both ARE divergences.** It also still inherits item 27's four-pair conflict.

**The one thing to watch has now been paid for THIRTEEN times, and the surface is SEVEN files**, not
five and not three. **Four standing controls exist and each was written after the same failure
recurred somewhere new:** item 46's file-surface rule, `0046` §0's population rule, `0049` §6's
launch-snapshot practice, and **`CLAUDE.md` §Propagation's seven surfaces with read-back PLUS grep.**
**Surfaces 6 (`artifacts/`) and 7 (this memory) were never checked before 2026-08-13**, and surface 7
is where a two-generations-stale entry was fed back into a ruling. Full arc in
[[gate-step7-liveness]].

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

### Verified 2026-08-13, on the checks the Human Lead named for the `0035`–`0050` pass

- **Both dual pairs are byte-identical apart from the `name:` field. PASS.**
  `data-scientist.md` / `data-scientist-b.md` differ only at line 2; `analytics-engineer.md` /
  `analytics-engineer-b.md` likewise. Read in full and compared line by line, not sampled.
  **Note the pairs are identical *including* V1's defect** — which is the point `0035` §1 makes:
  identical halves in the wrong state produce a clean diff and a wrong answer.
- **No file states PF-LIMIT or ALT as the operative rule.** All five propagation files carry
  ALT-BROAD's biconditional with both conjuncts. The one exception is **`decisions/README.md`'s gate
  checklist (V3)**, which is the index rather than a spec file.
- **The deleted thresholds appear only as history.** `4 / 504 / 632 / 914 / 1,293` occur in the five
  files exclusively inside "derived three times and deleted" statements. **One collision to watch:
  `632` is also the legitimate frozen-D10 never-started COMPONENT at `W = 125`** (`0050` defect 5) —
  same digits, different quantity, and `0048` §7 already shows how an unlabelled arm figure produces
  a false divergence.
- **Both superseded bounds are labelled.** `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]` appear
  in `task-sheet.md` line 340 and both `data-scientist` files only under an explicit *superseded*
  marker with the reason (mixed denominators; floor not a floor).
- **The withdrawn claims are absent from all five files as operative text.** *"no free parameter"*,
  *"`τ2` plays no part"*, *"the exclusion set is empty on DERIV"*, *"every liveness exclusion is
  never-started"*, *"751 directly observed"* — each is either absent, or present under a withdrawal
  marker, or (in both `data-scientist` files) present in the **negated** corrective form *"NOT every
  liveness exclusion is never-started."* Surviving instances are in `artifacts/` (**V8**) and in
  `decisions/0034` (**V9**).
- **`604` is used correctly everywhere in the five files** — as the never-started **component** of
  703, and as the **superseded ALT total** with both `analytics-engineer` files stating that
  producing 604 at Step 8 **is** a divergence.

**The arithmetic reconciles exactly, checked independently rather than accepted:**

- **APPLY**: never-started 33,373 / Continued **144,140** / S&L **19,141** = **196,654** ✓
  **CORRECTED 2026-08-13.** This list previously read *"144,141 / 19,140"* — **two off-by-ones that
  cancelled in the sum, so the total checked out and the split did not.** That is what defeated my
  reconstruction of the Continued ceiling and produced V7. **The correct split is forced by three
  independent figures that reconcile only on 144,140 / 19,141:** the Continued ceiling
  `(144,140 + 703)/196,654 = 73.6537%` *(SUPERSEDED — the adopted ceiling is 73.6995%; the
  reconciliation argument is unaffected because it turns on the split, not the widening)*, the S&L
  ceiling `19,141 + 604 = 19,745 → 10.0405%`, and
  `0053` §3 item 8's branch (ii) count of **19,141**. **A sum that reconciles is not a split that
  reconciles — check every component against a second route, not the total.**
- **Shares under the rule** on 195,951: 16.7231 + 73.5592 + 9.7177 = **100.0000** ✓, and each share
  back-computes to its integer count ✓
- **Movements** −0.2474 + 0.2630 − 0.0156 = **0.0000** ✓
- **Never-started bound**: ceiling 16.9704% × 196,654 = **33,373**; floor = (33,373 − 604)/196,654 =
  **16.6633%**; width **0.3071 pp = 604/196,654** ✓ — **both endpoints on one denominator**
- **S&L bound, WIDENED by `0054`**: **[9.6372%, 10.0405%]**, width **0.4032 pp = 793/196,654** ✓
  (floor numerator 18,952, ceiling numerator 19,745). Conditional sub-interval width
  ~~**0.0503 pp = 99/196,654** ✓~~ **CORRECTED (`0057`): 0.0961 pp = 189/196,654**, floor **18,952 →
  9.6372%**. **The conditioning constrains the 604 and says nothing about the 90**, so the sub-interval
  floor moves with the bound floor. **The ✓ on the superseded value is the defect**: the corrected bound
  and its withdrawn sub-interval sat one line apart, each blessed. **Superseded: width 0.3575 pp = 703/196,654, floor 9.6830%** — a **non-covering**
  endpoint, which is exactly what the widening repairs.
- **S&L bound on DERIV**: **[11.3015%, 11.4291%]**, width **0.1276 pp = 188/147,370** ✓ (99 exclusions
  + 89 channel pairs). **This bound was missing from every surface until 2026-08-13.**
- **Three ceilings on APPLY**: 16.9704 + 10.0405 + **73.6995** = **100.7104%** ✓; excess
  **0.7104 pp = 1,397 = 2 × 604 + 189** ✓
- **DERIV/APPLY consistency**: 152,126 − 147,370 = 4,756 removed by D10; 201,900 − 196,654 = 5,246.
  Line 4 ⊂ line 1 and 4,756 ≤ 5,246 ✓
- **The Continued ceiling reconstructs exactly** — `(144,140 + 703)/196,654 = 73.6537%` and
  `(144,140 + 703 + 90)/196,654 = 73.6995%` ✓. **V7's "does not reconstruct" is withdrawn.**

### Verified 2026-08-12 and still standing. Arithmetic in [[population-chain-steps-2-3-4]].

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
