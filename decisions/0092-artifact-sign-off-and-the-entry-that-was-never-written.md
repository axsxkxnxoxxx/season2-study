# Decision 0092 — no artifact is trusted without its producing arm's sign-off; and the entry stating that rule was never written

| | |
| :--- | :--- |
| **Decision** | **NO ARTIFACT IS TRUSTED WITHOUT ITS PRODUCING ARM'S SIGN-OFF.** **A deliverable is corrected by RERUNNING the arm that produced it, never by hand-editing the file.** Recorded in `CLAUDE.md`. ***AND THIS ENTRY DID NOT EXIST UNTIL NOW*** — the rule was written into `CLAUDE.md` and committed under the label `0092` with **no file in `decisions/`**, found by instance A. **Its N2 propagation also reached surface 1 only, and its premise is measurably wrong on APPLY.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-16 |
| **Occasioned by** | The Human Lead's ruling that hand-editing a deliverable puts unsigned text into it; the omission and the three defects, all found by instance A on the rerun |
| **Amends** | Its own prior form — a rule with no entry, a propagation with one surface, and a false premise |
| **Verified by** | `check_surfaces.py` **PASS** |
| **Status** | Open. **Step 8 is NOT approved.** Propagation of §3's correction is **pending arm b's completion** — see §5 |

---

## 1. The rule

> **No artifact is trusted without its producing arm's sign-off. A deliverable is corrected by rerunning
> the arm that produced it, never by hand-editing the file.**

**Hand-editing puts unsigned text into a signed deliverable**, and `artifacts/` is what Red Team reads,
what Step 9 consumes, and **propagation surface 6.**

**It holds even when the change is labelling only and no figure moves — *especially* then**, because that
is exactly when hand-editing looks harmless. **The producing arm is the only party that can attest the
text matches what its pipeline computed**; an editor who did not run the pipeline is **asserting**
agreement rather than establishing it.

**It is the `## Derived figures` rule one level up.** Derived figures are **regenerated, not patched**;
deliverables are **rerun, not patched.** The scripts already refuse to hand-patch a number. **This
refuses to hand-patch a sentence.**

## 2. The entry did not exist, which is the rule's own failure mode

**The rule went into `CLAUDE.md` and was committed under the label `0092`. No file was written to
`decisions/`.** Instance A found it: **0 matches on disk.**

**A ruling recorded in one place and cited from another is exactly what `CLAUDE.md` opens by forbidding**
— *"recorded only in `decisions/` is not recorded"* — **and this is that rule inverted: recorded
everywhere except `decisions/`.** The commit message described an entry that did not exist, so every
citation of `0092` pointed at nothing.

**No control could see it.** `check_surfaces.py` checks the eight surfaces for wrong and withdrawn
content; **it does not check that a cited entry exists.** Found by a reading agent, as the last six have
been.

## 3. Its N2 premise is wrong on APPLY, and the real gap is elsewhere — instance A

**Propagated:** *"the two arms read 168 on populations 23,453 apart … 168 cannot be correct on both."*

***Measured by instance A: 168 is correct on line 1 (220,107), position 5 (196,654) AND post-liveness
(195,951) on APPLY.*** **The two arms' readings would both have given 168.** **The premise fails.**

**What is real, and no entry records it: DERIV measures 153.** **That** is the population-dependence the
requirement should have been written against — **APPLY is invariant across all three readings and DERIV
is not.**

**The requirement itself stands and is strengthened**: state the population at the point of use **and
measure on both populations**, because **the count is invariant on one and not the other**, and a
figure quoted without its population is 168 or 153 depending on a fact the reader cannot see.

## 4. Two further defects of mine, both instance A's finding

- **The N2 edit reached surface 1 only.** `task-sheet.md` carries the correction; **both
  `analytics-engineer` files still carry the population-free 168**, and they are the files the isolated
  instances read. **Verified: 1 occurrence in each agent file, 0 copies of the correction.**
- **`task-sheet.md`'s `0088` §1 asserts *"no `.date()`, `dt.date`, `normalize()` or day-flooring
  anywhere in `step8_*.py`"* about BOTH arms. It is false of arm A.** The claim came from Red Team's
  fourth pass and I recorded it as verified of both. **Corrected by that arm at the point of use; the
  spec's copy is corrected in §5's pass.**

## 5. Propagation is deliberately deferred, and why

**§3's correction and §4's first item are NOT yet on surfaces 4–5.** **Arm b is mid-run and reads those
files.** Editing them now would give one arm a partially-updated spec and produce a divergence that is
an artifact of the edit rather than of the implementations — **which is the shape the dual control exists
to detect and would be corrupted by.**

**They land when arm b reports, before any further rerun.** **Recorded here rather than left to memory**,
because a deferred propagation that is not written down is how the covering qualifier went six entries
reaching no agent file.

## 6. Scope

- **No rule change to the measurement, no population change, no figure moves.**
- **Surfaces reached: `CLAUDE.md`** (the rule) and **1** (`task-sheet.md`, N2's requirement). **4–5
  deferred, per §5.** **6, 8: both arms rerun.**
- **Zero API calls.**
