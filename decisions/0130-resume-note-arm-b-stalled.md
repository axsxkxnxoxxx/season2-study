# Decision 0130 — RESUME NOTE. Arm `b`'s session stalled mid-task and must be resumed to report.

| | |
| :--- | :--- |
| **Purpose** | ***A RESUME NOTE, not a ruling.*** **Recorded so the next session starts from state rather than reconstruction — and so that what arm `b` did is reported BY ARM `b` and not re-inferred by anyone else.** |
| **Stopped at** | **`671ce01`**, pushed to `main`. **Six of arm `b`'s files uncommitted and untouched.** |
| **Date** | 2026-08-25 |
| **Next action** | ***RESUME ARM `b`. Do not re-infer its work from its files.*** |

---

## 1. What happened

**Arm `b` was dispatched on `0129` ruling 3 — adopt the producer-hash provenance fix for its own
pipeline — together with the `STEP_ARM` pass-through sweep.** ***Its agent stalled and failed: no
progress for 600 s.*** **Its last output was *"Now I'll write the verifier — the consumer-side
comparison, with every recorded value read from the file rather than typed."***

***IT NEVER REPORTED.*** **There is no attestation of any kind for this work.**

## 2. What is on disk, and what that does and does not establish

**Uncommitted, untouched, not run by anyone else:**

| | |
| :--- | :--- |
| **modified** | `src/step9_b_8_controls.py`, `step9_b_10_pairing_evidence.py`, `step9_b_14_restamp_probe.py`, `step9_b_15_mechanism_repro.py` |
| **new** | `src/step9_b_21_provenance_verify.py` (477 lines), `src/step9_b_22_stale_producer_repro.py` (260 lines) |

**Established:** both new files **parse** and end cleanly; `check_surfaces.py` **exit 0**; **both Step 9
files validate at exit 0**; arm `b`'s own harness `step9_b_8_controls.py` **exit 0**; and ***all four of
arm `b`'s artifacts are byte-identical to `HEAD`*** — **no deliverable moved.**

***NOT ESTABLISHED, AND NOT TO BE ASSUMED:***

- **whether the ENUMERATION was completed** — *every place a producer's identity is taken on trust*, which
  was the first half of its instruction and the half that cannot be inferred from code
- ***whether the "BEFORE" direction was reproduced*** — **a consumer ACCEPTING a stale producer today.**
  **That is the direction that matters**, and a file named `…stale_producer_repro.py` existing is **not
  evidence that it was run or that it passed**
- **whether the verifier is WIRED into anything, or is a standalone file nothing calls**
- **whether the `STEP_ARM` sweep covered its other controls**

> ***FILES PARSING AND CONTROLS PASSING IS NOT THE SAME AS THE RULING BEING SATISFIED.***

## 3. ***Why nobody else may finish or characterise it***

**The obvious shortcut is to run arm `b`'s two new scripts and report the output. THAT IS FORBIDDEN, and
not on a technicality.**

**`0092`: a deliverable is attested by the arm that produced it.** ***An orchestrator who runs a script
and reports its exit code is asserting agreement, not establishing it*** — **the exact shape of the
transcription the Human Lead discarded at `0128`, and of every "corrected at the point of use" report
this study has had to withdraw.**

**And `0127` §4c: *an enumeration of accommodation sites made by anyone but the writer is an
undercount*.** **The enumeration arm `b` was asked for is of the same kind.** ***Reading its files tells
you what it wrote. It cannot tell you what it looked at and found nothing in*** — **and that
distinction is the whole content of the instruction it was given.**

## 4. How to resume

***RESUME ARM `b`'s SESSION*** so it continues with its own context and reports:

1. **what it enumerated**, and **which categories it examined and found empty** — *stated as examined,
   not omitted*
2. **both reproduction directions, RUN**, with the "before" shown accepting a stale producer
3. **where hashes are recorded and where compared, and what happens on disagreement**
4. **the `STEP_ARM` pass-through confirmation and any others found**
5. **leaf-by-leaf verification that nothing published moved** — its artifacts are currently byte-identical
   to `HEAD`, so this should be trivially clean, **and it should say so rather than have it assumed**
6. **both control exit statuses, run after its last edit**
7. **any defect in its own work**

**If it cannot reconstruct what it had done, it says so and starts that part again.** ***A restart that
is declared is worth more than a continuation that is guessed.***

## 5. State

- **`HEAD` `671ce01`.** **`0129` filed and indexed**; **arm `a`'s half of ruling 3 done and attested.**
- **Rulings 1 and 2 of `0129` recorded and closed.**
- **Carried, unauthorised:** arm `a`'s second producer records its path but not its hash; **fixing it
  moves two published leaves.**
- **Carried from `0128` §3c:** ***the `git status` channel is closed by `0129`, but the family is not.***
  **`0128` predicted a fifth and was right within the day; there is no reason to think five is the
  number.**
- **Zero API calls. STEP 10 NOT BEGUN.**

---

## 6. ***PAUSE NOTE — appended 2026-08-30. THE PROJECT IS PAUSED.***

**Appended by Human Lead instruction.** ~~Six of arm `b`'s files uncommitted and untouched~~
***NO LONGER TRUE AS OF `4a176d0`*** — see below. **The header row's `Stopped at` is superseded by this
section; nothing else in §§1–5 is.**

### 6a. What moved, and what did not

**Arm `b`'s six files are COMMITTED at `4a176d0`** — four modified, two new — **exactly as they stood.**
***They were not run, not opened, not tidied.*** **The commit preserves them and asserts nothing about
them**, and its message says so in the terms `0130` was written in: *not verified, not wired, enumeration
not confirmed, reproduction not run.*

***COMMITTING IS NOT ATTESTING.*** **§§2 and 3 stand unchanged and still govern**: files parsing and
controls passing is not the same as the ruling being satisfied, and **no other party may close arm `b`'s
half.** The only thing that changed is that the work is now **preserved** rather than **at risk in a
working tree.**

### 6b. Paused as of 2026-08-30, at this `HEAD`, with **STEP 10 NOT BEGUN**

**The pause point is `4a176d0` plus this entry.** **Step 10 has not been started**, and the standing
prohibition on beginning it is unchanged by the pause.

### 6c. ***THE THREE CARRIED ITEMS***

1. ***ARM `b`'s UNFINISHED HALF OF `0129` RULING 3.*** **The provenance fix is adopted on arm `a` and
   attested; on arm `b` it is unreported.** **What is on disk is partial work of unknown extent** — §2's
   list of what is *not* established is the live list. **Closed only by arm `b` resuming and reporting.**

2. ***ARM `a`'s SECOND PRODUCER RECORDS ITS PATH BUT NOT ITS HASH.*** `src/step9_a_7_frame_support.py`.
   ***FIXING IT MOVES TWO PUBLISHED LEAVES***, which is why it was not fixed in the same pass — **it is
   a deliverable change and therefore a rerun, not an edit** (`0092`). ***AWAITING A RULING.***

3. ***THE DIFF NEEDS REDOING.*** **Arm `b` published twelve intervals it had previously withheld and arm
   `a` completed to all eighteen, rewriting nine notes.** ***THOSE HAVE NEVER BEEN COMPARED.*** **The
   diff on the record predates both**, so **the cross-arm state is currently unknown rather than
   agreed** — and an unrun diff is not a clean one. ***The diff is the Human Lead's and no agent
   performs it***, so it is carried here as a Human Lead item, not an agent task.

### 6d. What resuming looks like

***RESUME ARM `b` FIRST. EVERYTHING ELSE IS DOWNSTREAM OF IT.***

**Item 3 cannot be run before item 1**, because a diff taken while one arm's half of a live ruling is
unreported would compare **a settled arm against an unsettled one** and would have to be taken again.
**Item 2 is a rerun of arm `a` that will move two published leaves**, so ruling on it *after* arm `b`
reports keeps the two arms' deliverables moving in a known order rather than crossing.

**So: §4's seven-item report, from arm `b`, in its own words. Then item 2's ruling. Then the diff.**
***And the diff is taken over BOTH arms as they then stand, not patched forward from the one on the
record.***
