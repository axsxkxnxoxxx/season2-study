# Decision 0093 — a ruling is not closed until the artifacts carry it

| | |
| :--- | :--- |
| **Decision** | **A ruling recorded in `decisions/` and propagated to the spec is NOT closed. It is closed when the ARTIFACTS carry it.** Recorded in `CLAUDE.md`. **The mechanism is structural: the arms only rewrite their deliverables on a RUN**, so every ruling since `0084` has spent a window recorded-as-done, passing on all eight surfaces, while both arms still published the superseded text. **A decision entry must not say "closed" while the artifacts are stale; it names what is propagated and what is PENDING A RERUN.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's eighth Step 8 pass — F1 is arm b publishing a characterisation `0089` §2(b) corrected two entries earlier |
| **Verified by** | `check_surfaces.py` **PASS** |
| **Status** | Open. **Step 8 is NOT approved. Both arms rerun; three items are arm b's and three are arm a's.** |

---

## 1. The rule, and why it is not a lapse

**Every ruling lands in `decisions/`, reaches `task-sheet.md` and both agent files the same hour, and
the propagation control passes on all eight surfaces — while `artifacts/` still says the old thing.**
The arms rewrite deliverables **only on a run**, so the window is structural, not carelessness.

**It is the sign-off rule seen from the other end.** A deliverable is corrected only by rerunning its
arm; therefore a ruling is closed only after that rerun. **Together they close the loop that
hand-editing would otherwise short-circuit.**

**The honest propagation report names both halves:** which surfaces are reached, and which **await a
run**. A report listing six surfaces while omitting that two carry stale text is the defect this rule
stops.

## 2. What occasioned it, and it is exact

**Red Team F1:** arm b republished *"747,478 … undeduplicated user-show season-coverage rows"* — the
characterisation **`0089` §2(b) corrected two entries earlier** — and **contradicted itself six lines
below**, its own table giving **1,007,729** for that label. **Arm b had read `0089`; it cites it in two
sections.** The ruling was in `decisions/`, in the spec, and not in the arm's emitters.

## 3. Two of the four listed items have no referent — checked, not propagated

**(a) *"the 30-pair bound restated with the population Red Team names."*** **There is no 30-pair bound.**
Red Team's eighth pass names none; no artifact contains one. **The only `30` matched in either artifact
is a substring of `1,230`**, the `p = 1.0` post-liveness count. ***Third occurrence of a `30` cited with
no referent*** — the earlier two were *"the withdrawn `0 = 75 = 30` identity"*, and D9's numbers are
0, 75, 76, 6 and 27. ***CORRECTED 2026-08-16 by `second-brain`: this sentence listed `153` among them. `153` is D2's DERIV both-bind tie count — `step8-waterfall-a.json:1311,1320` — and there is no D9 `153`. An entry written to correct a referent carried a referent error of its own.***

**(b) *"D4's withdrawn word in both artifacts."*** **Zero withdrawn, superseded or struck wording appears
anywhere near D4 in either artifact** — measured on the current build, both files. **Second occurrence.**

**(c) and (d) are real and are the same finding.** *"The two arms' figures for the same quantity given
their objects"* and *"the stale text"* are both **F1**. The true relation Red Team publishes:
**arm a's 747,478 distinct pairs, less the 21,376 S3-only, is 726,102 against arm b's 726,103** — the
one-pair divergence both arms already report. **Fixed by the rerun, in the emitters.**

## 4. The hand-patching premise is false, and it was checked

***Neither arm hand-patched anything.*** Both reran their pipelines; **the working tree is clean and
every artifact is pipeline-generated.** Arm a changed four `step8_a_*.py` files, arm b six
`step8_b_*.py` files, and **no artifact carries an edit outside a run.**

**`0092`'s sign-off rule has not been violated by either arm at any point.** It remains untested, which
is the correct state for a rule whose case has not arisen — **and it is why `0093` is worth having:
the failure that keeps recurring is not unsigned text, it is STALE text, and the sign-off rule does not
reach it.**

**Recorded because a rule adopted against a misdiagnosed cause protects nothing.** `0093` names the
cause the evidence supports.

## 5. The rerun's scope

**Arm b — three, all Red Team's:** F1's characterisation at the point of use; **F2**, whose needles must
fold into `src/step7_register.py` and match **case-insensitively** — `six of EIGHT` is present three
times and its hits table shows no row for that needle, *the one needle written against the defect that
motivated the control* — and whose `assert` currently runs **after** all four artifacts are written;
**F3**, the `examined` column holding pre- and post-D11 quantities in different rows.

**Arm a — three, all minor:** F6's hardcoded conclusion string, now contradicted by its own live counts;
F7's falsifiability headline, which differs from arm b's on the same nine labels with **neither arm
flagging it**; F8's symmetric-difference-0 warrant, which is one notch stronger than the monotonicity
allows.

**`0092` §5's two Human Lead items are already done** — the surface 4–5 splice repaired and surface 7
reached — and **`0093` is the reason they were not enough on their own.**

## 6. Scope

- **No population change, no figure moves.** **Surfaces reached: `CLAUDE.md`.** **6 and 8 PENDING BOTH
  ARMS**, stated per this entry's own rule.
- **Zero API calls.**
