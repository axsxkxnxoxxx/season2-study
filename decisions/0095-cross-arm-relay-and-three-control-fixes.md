# Decision 0095 — a cross-arm characterisation must never enter a launch instruction; F3/F4/F5 closed

| | |
| :--- | :--- |
| **Decision** | **An arm's launch instruction states the SPEC and that arm's OWN defects. It never states what the other arm publishes.** Recorded in `CLAUDE.md`. **A relayed cross-arm characterisation routes around the isolation rule and is worse than reading the folder, because the receiving arm is structurally forbidden from re-measuring it.** Red Team's ninth-pass **F5** (citation resolver blind to un-backticked citations), **F3** (needle register exercised on 4 files of one surface) and **F4** (exemption window measured in lines on paragraph-per-line files) are closed. ***AND THIS ENTRY WAS MISSING FOR A DAY — the THIRD occurrence.*** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-16 (entry written 2026-08-17) |
| **Occasioned by** | Red Team's **ninth** Step 8 pass: HOLD on three, **no arithmetic defect in either arm**, every cross-arm figure agreeing to the row |
| **Amends** | `CLAUDE.md` `## Dual implementation`, by enforcement; `src/check_surfaces.py` |
| **Verified by** | `check_surfaces.py`, `step7_regenerate_derived.py`, `step7_floor_extremes.py` |
| **Status** | Open. **Step 8 is NOT approved.** |

---

## 1. F1's root was mine, and it is structural

**I relayed Red Team's eighth-pass characterisation of arm b's falsifiability headline into arm a's
launch instruction.** Arm a published it as an **arm-against-arm divergence** — while arm b's `r7` build
publishes **the same 6 + 1 + 2 split** and names exactly which side the third member falls on and why.
**Arm a's claim was false, and under isolation it had no admissible way to check what it was told.**

**`## Dual implementation` says neither instance sees the other's work. A LAUNCH INSTRUCTION IS A WAY
FOR IT TO SEE IT** — and it is **worse than reading the folder**, because the receiving arm is
**structurally forbidden from re-measuring the claim.** A relayed characterisation is **a measurement
with an expiry date its holder cannot check**, so it can only go stale. **It went stale in one build.**

**A fabricated divergence in a gate deliverable is worse than a missed one:** it pre-empts the one
authority permitted to make cross-arm statements — **the Human Lead's diff.**

**The rule, in `CLAUDE.md`:** a launch instruction states the spec and the arm's own defects, **never**
what the other arm does, publishes, splits, names or reports — not from a Red Team pass, not from a
decision entry, not from a prior run's report. **Where a Red Team finding is inherently comparative, the
finding goes to the Human Lead and only the non-comparative half reaches the arm.**

**Arm a struck the claim entirely and did not replace it**, which is correct: any corrected
characterisation would breach the same rule.

## 2. F5 — the citation resolver saw only backticked citations

`0094`'s resolver matched `` `0NNN` `` only. **Arm b writes predominantly un-backticked** —
`decisions/0089 Sec 2(b)`, `0088 Sec 3` — so roughly **37% of one file's citations were invisible**, and
**the founding defect would have been missed entirely in that form.** *"Prints its coverage count"* was
satisfied to the letter **while the count was blind to the class it could not see.**

**First widening was too broad** — a bare `\b0\d{3}\b` matched `0000` and `0096` in data. **Now anchored
to citation FORMS**: `decisions/0NNN`, `` `0NNN` ``, and `0NNN` followed by `§` / `SS` / `Sec` /
`ruling`. **Probed**: two un-backticked citations to nonexistent entries are both caught, exit 1, file
restored byte-identical.

## 3. F3 and F4 — the needle register, and the unit it was windowed in

**F3.** `SUPERSEDED_STRINGS` and `SURFACE6_LINE_LOCAL_CONTROLS` were exercised **only by one arm's own
emitter, over its own four artifacts** — about **4 of ~40 files on surface 6**, and **none of surfaces
1–5, 7 or 8.** That arm's scan opens with *"a surface check that does not open the surface the defect is
on is a check that looked nowhere"* and then opened four files. **Occupied, not hypothetical**: a
registered needle was live in the other arm's deliverable. **Neither arm can fix this under isolation**;
it belongs in the shared control. **Folded into `check_surfaces.py` across all eight surfaces — 255
files, 7.0M characters.**

**F4.** The exemption window was measured in **lines**. `CONTEXT = 2` is ±200 characters on a
hard-wrapped file and **±several thousand** on the arms' deliverables, where **137 lines exceed 400
characters** and single paragraphs run to thousands. **Same defect the JSON branch was fixed for** — and
the `.md` branch was **not wrong when written**: *the unit changed underneath it* when the arms began
emitting paragraph-per-line. **Now measured in characters.**

***The needle scan returns 441 candidate hits ***CORRECTED 2026-08-17 (`0100`): THIS IS A LIVE MEASUREMENT, NOT A FIXED FIGURE.*** It counts candidate hits across every file on all eight surfaces, so **it moves whenever the repository moves** — 441 at `0095`, 439 at `0096` after one arm removed two of its own, and **442 as measured today**. ***The three numbers were never in conflict; quoting a live scan as a constant is the defect***, and it is `0096` §1's own lesson — a measurement published as though it were permanent. **Read the count from the scan, never from an entry.** It is wired REPORT-ONLY, labelled NOT YET A CONTROL.***
The needles were authored for one arm's four artifacts; repo-wide, short ones like `793` and `97.6%`
match **legitimate historical records**. **Failing on 441 unread lines would block the gate on lines
nobody has read; narrowing until it passes is how a control gets disarmed. Neither was done**, and the
triage is an open item.

## 4. The missing-entry defect, third occurrence

***`0092`, `0094`, and now this entry were each cited before they existed.*** This one was cited in
**10 files** — `CLAUDE.md`, the commit message of `0479ffb`, and both halves of arm a's four
deliverables, whose provenance names the entry they were launched against.

**`0094`'s resolver could not catch it, and arm a diagnosed why: the resolver scans the eight
propagation surfaces, and `CLAUDE.md` is not one of them.** The citation that would have caught it
earliest was in the one file the control does not read.

**It was caught anyway**, one build later, because **`artifacts/` IS surface 6** and arm a's build
provenance names `0095` — so the arm's own deliverable pulled the citation into coverage.

***Arm a did not remove the citation to make the control green***, and said so: *"that is narrowing until
it passes."* **It reported `EXIT 1` with the cause named and left it for the Human Lead.** That is the
correct handling of a control that fails for a reason outside the arm's remit.

**Carried, not fixed here:** whether `CLAUDE.md` — and `specs/`, still open from Red Team's **fifth** pass ***(citation kept; see `0100` for the canonical sequence, against which some intermediate citations in this chain are off by one)*** —
join the propagation surfaces. **Both are the Human Lead's**, and the resolver's blind spot is now
measured rather than argued.

## 5. Scope

- **No population change, no figure moves, no rule change to the measurement.** Arm a's rebuild moved
  **0 of 316** numeric leaves in the invariant JSON and **4 of 1,697** in the waterfall, all four in the
  live block that measures **the repository**, not the data.
- **Surfaces reached:** `CLAUDE.md` (the isolation rule), `src/` (the three control fixes), and
  **6, 8 for arm a** by its confirmed rebuild.
- **Zero API calls.**
