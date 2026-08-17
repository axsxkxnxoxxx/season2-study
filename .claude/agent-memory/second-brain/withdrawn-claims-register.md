---
name: withdrawn-claims-register
description: The study's own error log — claims asserted and later withdrawn or corrected, organised by failure mode, covering Steps 1 through 8 including the liveness gate's twelve-entry cascade and the Step 8 block's withdrawal of several Human Lead rulings' premises and of one CLAUDE.md rule by another; modes A-I, with mode I the withdrawn-GROUND class that no control sees; current through decisions/0098 and the Step 8 gate approval, 2026-08-17
metadata:
  type: project
---

# Withdrawn-claims register

**Why this file exists:** every claim below was asserted confidently, survived at least one review,
and was later found false. The value is not the list — it is the **taxonomy**, because the same seven
failure modes keep recurring and each one is checkable in advance. *(The taxonomy now runs to **nine
modes, A–I**; the sentence formerly said seven.)*

**How to apply:** when reviewing any gate artifact, run all **NINE** checks below (A–I; there is no
mode letter between D and F). They are cheap and
they have all caught something. **Mode H is the one to run on `0055`–`0063` and on Step 8**, because it
is the mode that survives a review: an entry claiming a check was run reads exactly like one where it was.

## The failure modes, and the check that catches each

| # | Failure mode | The check |
| :--- | :--- | :--- |
| **A** | **Asserting a property that does not follow from the definitions given**, or naming an object without making it operational | Check every *"therefore"*, *"guarantees"* and quantitative range against the definitions **in the same document**. Check every named object for a numeric threshold. Reject "on the order of", "near zero", "approximately", "expected to be zero" |
| **B** | **Quoting a figure from a source that does not produce it.** Dominant mode in Steps 4–5, raised **four times** as B3, D3, F3 and again at round 4 | Grep the figure to a **file and a key**. An uncommitted figure is an **unverified** figure — proved when the decorative "164" was finally committed and turned out to also be **wrong** |
| **C** | **Quoting a cost against a baseline that no longer exists** | For every cost in a rejected-alternatives table, name the population it is computed on and check that population is still the adopted one |
| **D** | **A unit or order-of-magnitude error that nobody re-derived** | Sanity-check any figure that crosses a unit boundary — per-minute vs per-hour, nanoseconds vs microseconds — against a second route to the same number |
| **F** | **A figure measured on one population or configuration, quoted as if measured on another.** **Added 2026-08-13. It is the study's most frequent single error** — at least nine instances, seven of them inside the Step 7 block, and it is what `0046` §0's standing rule exists to stop | **Name the population at the point of use, every time.** For an interval endpoint, name the population it is computed on **and** the estimand it bounds, and check they are the same population (`0047` §3). Mode C is its ancestor — C is a *cost* against a dead baseline, F is *any* figure against the wrong population |
| **G** | **A stale or wrong record fed back into a ruling and adopted without being checked against the producer.** **NEW, added 2026-08-13.** Distinct from F: F is a figure quoted against the wrong population; **G is a figure a SECONDARY record says is wrong, believed over the primary output that produced it** | **Check the producer, not the summary.** Grep the arms' JSON for the key before recording any figure as unreconstructible, wrong, or unpopulated. **A figure that an independent reviewer has cleared and that you cannot reproduce is first a claim about your reconstruction.** And: **a sum that reconciles is not a split that reconciles** — check every component against a second route, not the total |
| **H** | **AN ASSERTED ACTION OR PROPERTY THAT WAS NEVER TAKEN OR NEVER HELD** — an entry saying an edit was made, a check was run, or a control has a property, when it did not. **NEW, added 2026-08-13, and it is the dominant mode of `0055`–`0063`.** *This is my classification of a pattern the entries name individually; it is not a Human Lead ruling.* Distinct from A: A over-reasons from real definitions; **H states a fact about the world that a single look would refute** | **Make the claim assert itself, or do not make it.** `0060` B5's fix is the model — four `assert _dead not in MARK.pattern` lines run at import, *"so this claim cannot go stale silently again."* And: **an empty result and a clean result are the same value.** Every check that can return "nothing found" must say whether it found nothing **or looked at nothing** (`0062`) |

| **I** | **A WITHDRAWN GROUND BUILT FROM CORRECT STATISTICS** — `CLAUDE.md`'s **THIRD BLINDNESS CLASS**, and **no control sees it.** The argument is withdrawn; the numbers in it stay true. **So there is no superseded figure for the numeric half to match, and the argument is usually paraphrased rather than quoted, so there is no phrase for the phrase half to match.** **NEW, added 2026-08-16** | **Name the statistics that remain TRUE but are no longer load-bearing**, at the point the ground is withdrawn. **The register's obligation, `0065` §3.** `GROUNDS_WITHDRAWN` in `src/step7_register.py` is the machine half; this section is the human half and **must not diverge from it** |

> ***NAMING COLLISION, SURFACED NOT RESOLVED, 2026-08-16.*** **This register has defined *Mode H* since
> 2026-08-13 as *an asserted action or property that was never taken or never held*.** **The Human
> Lead's briefing of 2026-08-16 uses *"Mode H"* for the ground-withdrawal class** — *"where an entry
> withdrew a ground rather than a figure."* **Those are two different modes and both are live in this
> stretch.** I have added the ground-withdrawal class as **Mode I** rather than renumber H, because
> **H's ten instances are cited by letter in three other memory files and in the Step 18 material.**
> **The two things that conflict are this file's Mode H definition and the briefing's use of the same
> letter. The Human Lead names the letters.**

## Mode I — withdrawn GROUNDS. **`GROUNDS_WITHDRAWN` holds THREE, not two**

> **DIVERGENCE FROM THE BRIEFING, reported per the instruction.** The briefing states
> *"`GROUNDS_WITHDRAWN` in `src/step7_register.py` now holds **two** such entries."* **It holds
> THREE** — keys `"0094 SS2"`, `"0055 SS2"` and `"0083 SS2"`, read off
> `src/step7_register.py` on 2026-08-16. **The source governs.** *(The third, `0083 SS2`, was added at
> `0083` and is the `p_at_bound` one.)*

| Entry | The argument withdrawn | **Still TRUE, no longer load-bearing** | Why it is not load-bearing |
| :--- | :--- | :--- | :--- |
| **`0055` §2** | the widened S&L floor is warranted because the 90 channel pairs had full opportunity to produce evidence — ***"p5 margin 1.7 days, minimum 0.13"*** | **1.7 · 0.13 · 1.6552 · 44.5272 · 44.5** | **Cherry-picked the tail.** The same 90 have **median 44.5**. **A floor is a worst case; admissibility sets the endpoint and plausibility does not enter.** *"The correct ground carries NO margin statistic at all"* |
| **`0083` §2** | `p_at_bound` decomposes the `p = 1.0` spike, evidenced by the **1,246 / 1,230** totals *"splitting"* into two classes | **1,246 · 1,230** *(and DERIV's **1,072 · 1,056**)* | **Both are correct counts and both arms reproduce them, but they are ONE CLASS COUNTED TWICE, not two summed.** The FALSE class is **empty by construction**. **Citing them as separation evidence is the withdrawn argument; citing them as `p = 1.0` TOTALS is correct** |
| **`0094` §2** | arm a's **symmetric-difference-0** warrant, published as strictly stronger evidence than the unchanged exclusion total — *"a total that does not move can still be a different set of rows, and that is what the symmetric difference rules out"* | **0 · 703 · 99 · 55 · 45** | **TRUE of an arbitrary perturbation, FALSE of this one.** Relaxing either bound only **adds** episodes to `A` and `A_H`, and both Continued conjuncts are **monotone in `A_H`**, so a row can only **leave** the exclusion set. **An unchanged total ALREADY forces set equality.** The symmetric difference **confirms the arithmetic; it is not independent evidence.** Red Team eighth pass, F8 |

**The class was named by a reading agent, not by a control, and it survived in THIS memory across three
files and nine entries** before `0055` §2's instance was found. **A checker for it would be a prose
checker.** What stands in for one is the obligation above.

### Mode I candidates from `0089`–`0091` that are **NOT** in `GROUNDS_WITHDRAWN` — read off the source 2026-08-17

> ***I am NOT extending the table above with these.*** `src/step7_register.py` is the machine half and
> **the source governs**; a human half listing five where the source holds three is the two-registers
> defect `0059` B3 forbids, committed by me. **Listed as candidates, for the Human Lead.**

| Entry | The GROUND withdrawn | **Still TRUE, no longer load-bearing** |
| :--- | :--- | :--- |
| **`0091` §1** | *"line 6 does not move at all — 703 on APPLY and 99 on DERIV under every form — **because the silence test reads an insertion clock, not an episode timestamp**"* | **703 · 99 · 55 · 45.** **The warrant is structurally wrong** — conjunct 2 is `NOT Continued`, an **episode-timestamp** computation that moves on 55 APPLY rows under this very counterfactual — **and it is not established the 703 was measured at all** |
| **`0089` §2(a)** | *"exactly 1 episode falls AT `τ1`, **so `0068`'s strictness ruling moves a real row in `\|A\|`**"* | **1** — *"exactly 1 episode falls at `τ1`"* is **established, both arms, both populations.** **What is withdrawn is its use**: `0068`'s strictness is about **INSERTION instants**, a different axis, and the ruling's own quantity measures **0** |

**Both are the recurring shape — *right in substance about a number, wrong about the object it names* —
and both leave a true statistic behind with no superseded value for the numeric half to match.**
*(`GROUNDS_WITHDRAWN["0094 SS2"]`'s `still_true` list is `[0, 703, 99, 55, 45]` — **the same figures**,
under a different argument. One statistic, two withdrawn grounds, one registered.)*

> **AND A SMALL ONE IN THE SOURCE ITSELF, reported not fixed:** `GROUNDS_WITHDRAWN["0083 SS2"]`'s
> `why_not_load_bearing` says ***"The FALSE class is empty by construction."*** **In context it means
> CLASS 1, the coextensivity gap.** **Out of context it is the sentence
> `artifacts/step8-waterfall-a.md` §3.1 warns is wrong by 17,895 rows.** **`src/` is not mine to
> edit** — see K2 in [[open-items-and-contradictions]], where the same sentence was **live in this
> memory** until 2026-08-17.

## Mode H — the instances, and there are ten in nine entries

**`0049`'s header** asserted a five-file propagation pass that did not happen (`0050` opens by saying
so) · **`0052` §6** *"unreconciled and now specified"* — the bootstrap **was never specified in any
file** · **`0055` §5a** *"is stamped, not rewritten"*, asserting a step deliberately held · **`0055`
§5c** added a register row **that was not added** · **`0056` §4** *"every occurrence below is
superseded, and each is marked inline"* — **false in both files**, with the withdrawn bound under an
**OPERATIVE** heading and as an arm's **recommendation** · **`0057` §1** *"fifteen values corrected in
each file, listed and verified individually"* — **false**, a key whitelist walked past three regions ·
**`0058` §3** *"Reverted"* — reverted in the entry and **not in the body** · **`0059` §2** *"`MARK` no
longer matches `corrected`, `register`, `legitimate` or `ADOPTED`"* — **all four were still there**, a
string replace that failed to match and was not asserted on · **`0060` §1** *"the run fails if any
written quotient is not this arm's numerator over this arm's denominator"* — **true for arm a only** ·
**`0062` §3** *"every derived figure"* — **false by four** (`0063` §3 item 2.2).

**Three of these were named at the time as *"the third consecutive blocker of that exact shape"*
(`0060` B5), *"the fourth asserted-but-not-taken action in three entries, and this one was inside the
correction for the third"* (`0057` §2), and *"a fourth docstring asserting a code property the code
lacked"* (`0062` §4).** The mode was visible to the participants and kept recurring anyway, which is
why it belongs in the taxonomy rather than in the narrative.

**And the deepest instance is a limit recorded as hypothetical while it was live:** `0060` §6 wrote the
JSON-string gap down as *"not a defect today."* **It was already a defect on the day it was recorded** —
B8 was live in a `.json` string under `_DERIVED` and in `.md` prose carrying no numbers, in all four
operative deliverables (`0061`). **Recording a gap as harmless is not the same as checking whether it is.**

---

## `0095`–`0098` — the last stretch. **A `CLAUDE.md` rule withdrawn by another, and a divergence that never existed**

### The withdrawals

| What was withdrawn | Where | Note |
| :--- | :--- | :--- |
| ***A `CLAUDE.md` RULE, BY ANOTHER `CLAUDE.md` RULE.*** `0095` §1 forbade cross-arm content reaching an arm *"not from a Red Team pass, **not from a decision entry**, not from a prior run's report."* **The DECISION-ENTRY exclusion is withdrawn** | `0095` §1, withdrawn `0096` r2 | **The ground, as given: a ruling has to record what each arm found in order to explain why it was ruled — forbidding cross-arm content in `decisions/` would mean A RULING CANNOT CITE ITS OWN EVIDENCE.** ***And the withdrawal names what the isolation rule is FOR***, which the earlier form did not: **to stop the arms copying each other's IMPLEMENTATION**, not to keep a ruled number out of reach. **The launch-instruction half stands, unchanged.** ***Record the two together or the pair reads as a contradiction*** |
| **Arm a's published arm-against-arm falsifiability divergence** — a two-way/three-way split against arm b | `0095` §1 | ***THE DIVERGENCE DID NOT EXIST.*** Arm b's current build published **the same 6 + 1 + 2 split** and named which side the third member falls on. **The claim came from a Red Team characterisation RELAYED INTO ARM A'S LAUNCH INSTRUCTION**, and **under isolation arm a had no admissible way to check what it was told.** ***A fabricated divergence in a gate deliverable is worse than a missed one: it pre-empts the one authority permitted to make cross-arm statements — the Human Lead's diff.*** **Arm a struck the claim entirely and did not replace it**, which is correct — any corrected characterisation breaches the same rule |
| ***"`check_surfaces.py` EXITS 1"*** — in a permanent deliverable, when it exits 0 | `0096` §1 | **True when the arm measured it; false by the time it was read.** ***Arm a's behaviour was correct throughout*** — it reported the failure with its cause named rather than removing a citation to go green. ***The defect is that a control's exit status was publishable in a permanent deliverable at all*** |
| **Four statements in `artifacts/step8-readback-{a,b}.md`** — *"`processed/` is not one of the SEVEN surfaces"*, `adopted_rule.json`'s **215,258 / 4,849**, *"Step 7 NOT approved; seven HOLDs"*, *"Step 0 still carries the superseded 403 rule"* | `0097` §1 | **All four were TRUE on 2026-08-14 and are false now.** ***No control can see any of them*** — the **third blindness class.** **Eleven passes did not catch them**; the eleventh found them only because `0096` §1 drew a line these files sit outside. **Named in a stamp rather than corrected, because these files have NO PRODUCING PIPELINE and `0092` corrects a deliverable by rerunning its arm** |
| **The claim that the read-backs were *"stranded between `0092` and `0096`"*** | `0097` §2 | **Red Team disputed it and was right:** both files **already carried a hand-added `0086` status stamp**, *"so the precedent for a hand-applied status stamp on these exact files existed in the files."* **`0092` forbids hand-CORRECTING a deliverable's content; declaring a non-pipeline file non-operative is not that** |
| **`0096` §1's SCOPE** — *"a **gate deliverable**"* | narrowed by `0097` §3 | ***One notch too narrow.*** `artifacts/` holds two files that are not gate deliverables, **and the expiry-dated-assertion class survived in exactly those two.** Red Team's own framing, adopted: *"the ruling was correct and its boundary was one notch too narrow"* — **a different diagnosis from the plateau it reported one pass earlier** |

### The one thing in this stretch that is NOT a withdrawal and must not be filed as one

> ***Gate residual 2 — the `logs/` provenance cost — is ACCEPTED AS RECORDED.*** Build history and
> control results now live in `logs/`, git-ignored and on no propagation surface, so **the public
> artifact set is no longer self-auditing on provenance.** **That is the knowing price of `0096` §1**,
> and the Human Lead stated why it is not a follow-up: ***"a cost logged as a correction reads as a
> defect awaiting a fix, and this one is neither."***

---

## The Step 8 block, `0066`–`0094` — **a great many withdrawals, and several are the Human Lead's own rulings**

**The distinguishing feature of this block: almost every withdrawal is of the CHAIN'S OWN TEXT, and
almost every one was found by a READING AGENT rather than by a control** — including several inside the
control apparatus itself.

### Withdrawn RULINGS and ruling premises — Mode A / Mode B / Mode F

| What was withdrawn | Where | Note |
| :--- | :--- | :--- |
| ***"the two arms read 168 on populations 23,453 apart … 168 cannot be correct on both"*** | `0092` §3 | **The premise fails.** 168 is correct on **all three** APPLY readings; **DERIV measures 153**, and no entry recorded that. **The requirement survives and is strengthened.** *(This is a Human Lead ruling's premise, measured false by an instance)* |
| **`0092`'s cause** — that deliverables were being **hand-patched** | `0093` §4 | ***Neither arm hand-patched anything.*** *"`0092`'s sign-off rule has not been violated by either arm at any point. It remains untested, which is the correct state for a rule whose case has not arisen"* — **and a rule adopted against a misdiagnosed cause protects nothing** |
| **B3's referent** — *"the two are invariants 7 and 8"* | `0088` §1 | **They are not.** 7 and 8 were already measured, published and praised. *"The reasoning describes a state that does not exist."* **Substance unaffected** |
| **F2's axis** — *"show IDs against frame IDs"* | `0088` §2 | Neither is a show-ID count; neither is frame-restricted |
| **The D9 universe named as "U3"** | `0088` §3 | **The reasoning identified U1 four separate ways and the letter contradicted all four.** Put back to the Human Lead rather than inferred |
| **`maigret` as D9's third-largest cluster** | `0088` §3, struck `0089` §2(c) | **A SIX-WAY TIE at 6.** *"A spec gap inside the ruling that closed a spec gap."* **Both arms reported it independently and neither picked the name the entry gave** |
| **The boundary window `[τ1 − 24h, τ1)`** | `0088` §1(a), corrected `0089` §2(a) | **It is the interval on which the two forms AGREE** |
| ***"the 30-pair bound"*** and ***"D4's withdrawn word"*** | `0093` §3 | **Two directed items with NO REFERENT.** *Third* occurrence of a `30` with no referent — **the only `30` in either artifact is a substring of `1,230`** — and *second* of the D4 one |
| **`0074` ruling 5's framing** — *"use the STRICT key and report the loose count alongside"*, under which **strict was the answer** | superseded `0090` | **D9 publishes as a BOUND: strict is the FLOOR, loose is the CEILING, NEITHER is the point estimate.** Needles: `strict is ruled`, `even though strict is ruled`, `the ruled key is strict` |

### Withdrawn MEASUREMENTS and verdicts — Mode F / Mode H

| What was withdrawn | Where | Note |
| :--- | :--- | :--- |
| **`OCCUPIED_INERT`** as B3(a)'s verdict | `0089` §2(a), reversed `0091` §1 | ***Not merely unsupported — FALSE.*** Computed on **1 row of the 311**. Correct: **`OUTCOME_DECIDING`, 71 APPLY / 59 DERIV**, 36 of them **never-started → Continued** |
| ***"Both arms emitted both intervals rather than only the one ruled"*** | `0089` §2(a), corrected fifth pass | **FALSE of arm b**, which emitted the ruled window and the single instant at `τ1` and nothing else |
| ***"so `0068`'s strictness ruling moves a real row in `\|A\|`"*** | `0089` §2(a), withdrawn sixth pass | **WRONG OBJECT.** `0068`'s strictness is about **insertion instants**; the 1 is a distinct S2 episode by `watched_at`. Measured on the ruling's own quantity: **0 on 196,654, both populations** — ***the strictness ruling is VACUOUS on this data, and one arm publishes that it is load-bearing*** |
| ***"line 6 does not move at all … because the silence test reads an insertion clock, not an episode timestamp"*** | `0091` §1, withdrawn sixth pass | **Structurally wrong** — conjunct 2 is `NOT Continued`, an **episode-timestamp** computation moving on **55 APPLY rows** under this very counterfactual. **And it is not established the 703 was measured at all**: if conjunct 2 was held at the adopted outcome, `703 → 703` is a **tautology** |
| ***"all 15 identities re-run against `population + 1` and must FAIL"*** as a demonstration of **independence** | `0091` §2, corrected sixth pass | **Overstated for arm a.** A `+1` perturbation **fires identically on a same-mask denominator**, so it would have passed on the very build whose defect it claims to have fixed. **Arm b's IS a real control** — 6 injected defects, and **case 4 is the one that actually tests independence** |
| ***"every D9 count still reconciles across both arms"*** | `0086` §1, **RESTRICTED** `0087` §2 | **Five ruled counts reconcile; three coverage counts do not.** *"Restricted, not deleted"* |
| ***"U1 — 46,366 arm A / 46,428 arm B"*** as an arm-against-arm difference | `0086` §1, corrected `0087` §2 / `0089` §3 | **Both numbers are recoverable from arm A alone.** *"It was never the arm-against-arm comparison it read as"* — **62 apart WITHIN one arm** |
| ***"747,478 … undeduplicated user-show SEASON-COVERAGE ROWS"*** | `0088` §2, corrected `0089` §2(b) | **Distinct `(user, show)` PAIRS.** Arm a's row count is **1,217,122**; arm b's is **1,007,729** over a different mask. **The label was taken from the previous artifact's own key — which was itself part of what F2 flagged as mislabelled** |

### Withdrawn CONTROLS — a control asserted to exist

- ***"The run asserts this, so a report that omitted a population could not be written by this
  pipeline."*** **STRUCK whatever else is ruled** (`0087` §4, `0088` §2). **8 of 13 coverage identities
  are `cover(unit, pop, N, N)`** where the population size and the asserted count are **the same
  expression**. Arm b additionally hardcoded `identity_holds: True` at three invariants and chained
  `.get(…, .get(…, True))` so **an invariant with no coverage key contributed a pass.**
- ***`real = len(parts) > 1`*** as an independence proxy — **admitted all four identity families**,
  each a complementary partition of the mask the population size is taken from, **including the one the
  deliverable called *"the identity that closes the hole."***
- **Three hardcoded literals published as results**, one of them `"holds": True` **inside the per-site
  D11 table `0088` §1(b) created precisely so mandates would stop being self-reported** (`0091` §3).
  **`0087` §4 found hardcoded `True` in one arm; it reappeared in the other arm's brand-new table one
  entry later.**
- ***"reached surface 1 and no other"*** — arm a's **hardcoded** propagation reading, published beside
  live counts a rerun could contradict, **and did.** `WITHDRAWN_PHRASES`, `0094` §2.

### The two claims withdrawn from `CLAUDE.md` itself in the wider block

- **`LIVE_ELSEWHERE`** — *"a value still live somewhere cannot enter the superseded list, because the
  list is generated."* ***Withdrawn: the mechanism never fired.*** The filter compared against a list
  that never contained the values in question, **so it was a no-op.** *"A control asserted to exist is
  not a control, and this one was found by reading the code rather than the claim."*
- **The claim that `0092` §2's defect was controlled.** It was not, and **`0094` was cited 8 times with
  no file — the second occurrence in three entries.** *"A gap recorded and left open is a gap that
  recurs."* **Now controlled by the citation resolver.**

---

## Mode G — the one instance, and it is this role's own

**`second-brain`'s memory recorded the Continued CEILING 73.6537% as a *"Continued floor"* and
concluded it *"cannot be reconstructed and states no population."*** Registered as open item V7.

**It was wrong three ways.** It was never a floor. It reconstructs exactly —
`(144,140 + 703) / 196,654` — and **both arms publish it**, `bb-a.md` §5 and `bb-b.md` §4.3, with
**both JSONs carrying `ceiling_pct: 73.6537…`**. And my reconstruction failed only because my own
APPLY split carried **144,141 / 19,140** where the arms carry **144,140 / 19,141** — **two
off-by-ones that cancelled in the sum**, so the total checked out and the split never did.

**What it cost, and this is why the mode exists.** **`0051` §2 adopted the diagnosis without checking
it against the arms' own JSON**, asserted *"73.6537% is on no population,"* and **attributed the
number to Red Team while doing so.** `0052` §2: *"the exact failure `0046` §0 exists to prevent,
committed in the entry that corrected two other instances of it."* **The correction was worse than the
error** — it left `task-sheet.md` presenting Continued as a **point, 73.2962%**, and **a Step 9
instance reading that against its own deliverable would have deleted a correct number.** `0051` §2 is
withdrawn in full.

**And the deeper finding, from Red Team's eighth Step 7 review:** `second-brain`'s memory is a
**seventh propagation surface that was never checked.** Five were; **`artifacts/` and this memory were
not.** `CLAUDE.md` §Propagation now names all seven and requires **read-back plus grep**.

> **Mode G's lesson, stated so it survives this incident:** *this memory is an index, not a source. It
> is fed back into rulings, so a wrong entry here is a wrong ruling waiting for someone in a hurry.*
> **Where this memory and an arm's own output differ, the arm governs.**

---

## Mode A — the original family, from Step 1

Twelve rows sit at the head of `artifacts/step1-outcome-definition.md`: **eleven withdrawn or
corrected claims plus one accepted risk (B2).** Recounted against the file; the table must not be
pruned. Six are false-by-construction:

| Claim | Why it was false |
| :--- | :--- |
| `p ∈ (0, 1]` follows from `p = m / L2` | Not when `F2 > L2`. Fixed by making `p` rank-based |
| Rank-based `p` is safe because out-of-set episodes are dropped upstream | The old drop rule caught `number > F`, `number < 1` and missing fields — an episode numbered *inside* `1..F` but *absent* from the listed set survived all three |
| Right-censoring at `T0 + max(W, 91)` guarantees 91 days of post-window observation | **False by subtraction.** The guarantee is `max(0, 91 − W)`: **zero** at any `W ≥ 91`. Fixed by declaring `H` |
| D3 and D8 measured "to the pull date" are rates | Exposure-weighted mixtures weighted by **show recency**. Fixed by the constant horizon `H` |
| "On or before `T1`" is a single unambiguous operator | Ambiguous by one day, on the operator that assigns **every** outcome state |
| A show is weekly when its span is "on the order of" `(L2−1)×7` | Not thresholds and not exhaustive; a required stratum with unassigned members gets silently pooled |

Five framing corrections: entry/exit are **not** symmetric (S1 evaluated over all time, S2 within
`W`); right-censoring does **not** cost zero rows; truncating negative lags at zero was withdrawn
because it made `W` a function of the frame's cadence mix; "pull date needs no definition" was
load-bearing in four places; **liveness is a pair-level filter**, not a statement about the account.

### Mode A continued into Steps 3–5

| Claim | Where | Correction |
| :--- | :--- | :--- |
| *"A user with fewer than 10 episodes logged **cannot** have completed any season 1"* | `src/step3_user_discovery.py:43-45` | **Not true.** `min(L1) = 1` over the frame. Stated as a certainty and is not one. Accepted rather than fixed — exposure bounded at 22 accounts |
| *"Timestamp accuracy is not a concern for this study. The outcome is whether someone watched season 2, not when."* | Step 5 revision 3, its **governing principle** | **Withdrawn.** It described an ever-started study. Step 1 §7 makes the outcome operator a **timestamp comparison**, `\|A\| = 0` under `watched_at < τ1`. Red Team D1 |
| *"These pairs cannot be evaluated against the definition"* (the 1,542) | Step 5 revision 3 | **False.** With zero S2 records `\|A\| = 0` for every `τ1`. Re-ruled onto a **censoring** defect. Red Team D2 |
| *"The whole 7,340 partly-stamped population is unanswerable until `W` exists"* | Step 5 revision 4 §12 | **False for 2,352 of them** — if the first S2 watch is clean, `c ≤ s ≤ finale ≤ T0 < τ1` at any `W`. The artifact **computed the split, printed it, and then declared the whole set open.** Red Team F2 |
| *"128,099 under every reading"* | Step 5 revision 3 | Proved for two readings, **false for R3**, which grows the sample to **131,043**. Withdrawn rather than defended. Red Team E3 |
| R3's precedent is Step 1 §2.3 | Step 5 revision 3 | §2.3 governs *which records count as watching* and says nothing about timestamps. The operative rule is **§2.2**. Red Team E4 |
| *"Completer counts only rise"* as the pool grows | `decisions/0013` condition 2 | **118 shows fell**, 177 pairs lost. Counts **move**. Corrected by `0019` — the instruction was right, the reason was wrong |
| *"On a C1 show every lag is non-negative **by construction**"* | **`decisions/0003` D14 and Step 1 §9** — i.e. inside an approved gate and an approved decision | **False on the data. 689 C1 lags are negative**, identical counts from both Step 6 instances. The warrant reasons about the **finale term** and then generalises to the whole `max()`: **459 bind on the S1-completion term**, where a user who watched S2 before finishing S1 gets a negative lag with no defect involved. **230 bind on the finale**, which should be impossible under C1 — 135 are the known one-day UTC skew and **95 have no account, out to −495 days**. Worth ≤6 days of `W`. README item 24, **still open** |
| *"Set W at the percentile where the curve **flattens**"* | `task-sheet.md` Step 6, the original wording | **Withdrawn by `0024`.** The C1 density is **close to scale-free past day 7**, log-log slope −1.1 to −1.5 across every decade, so **there is no break to read**. Two isolated instances produced 46 and 107 from identical inputs. Textbook mode A — an instruction naming a feature the object does not have |
| *"There is a real trough between 7 and 180 days"* | Step 5 revision 1 | A **bin-width artifact**; per-day density is monotone decreasing throughout. 180 days is a conservative judgment, not a data-determined break. The only real break is at **7 days**. Red Team C1 |
| *"Duplicate accounts: none found"* / *"ten duplicate accounts"* | Step 5 revisions 1–2 | The ten were **mode-3 artifacts**. The negative is **conditional** — an import-only duplicate leaves no real-time records and 251 accounts are untestable. Red Team C4 |
| *"Every retained pair has a clock start with a real logging date behind it"* | Step 5 revision 1 | Overclaim; pairs reach the completion threshold through an ordering that includes fabricated dates. Red Team C5 |
| *"The best account rule leaves 21.1% on a fabricated clock start, the pair rule 0%"* | Step 5 revision 1 | **Circular** — the pair rule is *defined* as removing exactly those pairs. Red Team C2 |

### Mode A at the Step 1 §7 amendment — eleven rounds, and the rule was never the thing that broke

**The amendment survived eleven adversarial attempts unbroken.** Every one of these is a withdrawn
**justification**, which is the point: mode A is a failure of *warrant*, not of *rule*. Full arc in
[[amendment-step1-continued-boundary]].

| Claim | Where | Why it was false |
| :--- | :--- | :--- |
| **Four successive grounds for the anchor choice** — exogeneity, temporal position, arm comparability, choice-at-a-price | §1.1, revisions 6, 7, 8, 12 | **All four failed on the study's own recorded figures.** `T0` is behavioural on **52.7%** of pairs; D10 already imposes the clearance; no diagnostic window changes length; and `τ2` gives every starter **more** than 91 days, so the "price" ran backwards. **§1.1 was cut and the amendment adopted with no stated ground** |
| *"Both marginal figures are comfortably inside the 91 days `H` adds"* | Revision 1 §2 | **False.** The marginal p90 is **100.39** — **101 against 91** under `0025`'s ceiling. `H` **loses** the comparison by 10 days. Stated first, before anything favourable |
| *"Nearly one in five never-started pairs demonstrably finished S2"* | Revision 3 §6.1 | **A ceiling labelled a floor**, on a denominator §4 disqualified three paragraphs earlier. 8,449 excludes the **23,735** pairs with no S2 record, which belong in D8's denominator. *"The most quotable line in the document and it was off by a large factor"* |
| *"1,575 is the price of the `\|A\| ≥ 1` conjunct"* | Revision 3 | **False.** Dropping the conjunct makes the definition **non-partitioning**, not more generous. Reattributed to the asymmetric anchoring — the conjunct **makes the cost visible; it does not cause it** |
| *"They bracket the quantity"* — of the coverage pair, and again of D3′ and its companion count | Revisions 2–3 | **Both truncate observation and neither is a lower bound.** "Bracket" dropped in both places. This study does use genuine floor-and-ceiling pairs; **this is not one**, and calling it one borrows a rigour it does not have |
| *"The estimation sample truncates first-S2 lag at 180 days, so starts in `(180, 199]` are excluded by construction"* | **Five places across six revisions**, and load-bearing in two ledger entries | **`first_s2_lag_days` is a BACKFILL measure** — insertion instant minus claimed `watched_at`. A day-185 live scrobbler has a lag near zero and **is** in the sample. **Step 5 named it correctly throughout**; the misreading was the amendment's alone |
| *"The corrected values are upper bounds"* — **6,874 / 5.37% / 0.453** | Revisions 6–8 | **Ran backwards on both of its own channels**, reinstating in numeric form the overstatement §6.1 had withdrawn. **All three values deleted**, from the prose, the script and the JSON |
| *"The correction lands at 0.453, below item 8's pre-amendment 0.485"* | Revision 7 | **Not like-for-like** — those pairs are Never started under the approved rule too, so the comparable figure is 0.395. Removed |
| *"The valid comparison is count against count"* — item 9's 3,440 against item 10's 1,575 | Revision 8 | **Not commensurable.** Item 9 acts on the ratio's **denominator**, item 10 on its **numerator**. Deleted, **not replaced** |
| *"Item 10's floor is 1,575 on the population D8 runs on"* | Revision 9 | **Three populations conflated as two.** 1,575 (estimation sample), **1,573** (less right-censoring), and D8's own, **not computed**. 1,573 is a **floor for** D8's population, not the count on it |
| *"8,445 hold an admissible record"* | Revisions 5–6 | Obtained as `8,449 − 4` where the 4 was a **state-change delta**, missing two families of pair. **Recomputed directly: still 4, so 8,445 stands — now measured.** *"Surviving does not retire the objection"* |
| *"Both Step 6 instances measured its effect on `W` as nil"* | Revision 6 | **Only instance A tested it.** B recorded the same 4 as `NOT_dropped` with no with/without comparison. Attribution corrected three times across three revisions before landing on *"claims nothing beyond the file"* |
| *"The 4 pairs Continued at `τ1` but not at the pull bound are real and not a bug"* | Revision 3 §10 | **It was a bug — the missing D11 filter.** The accompanying assertion was **vacuous**: it tested `cleared ∧ cont_τ1 ∧ ¬cont_τ2`, empty on every row unconditionally because `τ1 < τ2`. *"The conclusion was true by arithmetic; the check was not a check"* |
| *"`0029` grounds censoring on both `τ1` and `τ2` being functions of `T0`, `W` and `H`"* | Revisions 5, §6.5 and pre-strip §1.1 | **Not `0029`'s text and false in substance.** `0029`'s actual ground is *"a property of the clock and `pull_date`."* `T0` carries a behavioural term |

### The pattern the amendment adds to the taxonomy

**Four consecutive rounds found a ruling executed in the prose and not in the code** —
`amendment_corrections.py` and its JSON kept publishing withdrawn keys, and revision 4's **C2
recurred verbatim** one round after being closed in the same file. `1,573` had **no producer
anywhere in the repository** for a full round after being ruled.

> **Mode B's lesson generalises: a correction is not discharged until the script and its JSON carry
> it.** Grepping the prose is not the check; grepping the producer is.

**And the remedy, which is now precedent.** When §1.1 had failed three rounds, the Human Lead **cut
it** rather than repairing it a fourth time — *"a section which has lost three arguments in three
rounds is a liability regardless of what a fourth might achieve."* Red Team's own verdict on the
strip: *"it removed 2,350 words and introduced no new arithmetic error, which is the first round in
seven that can be said of."*

### Mode A at the Step 7 liveness gate — the rule broke four times, and so did its warrants

**Unlike the Step 1 amendment, here the *rule* broke too.** Full arc in [[gate-step7-liveness]].

| Claim | Where | Why it was false |
| :--- | :--- | :--- |
| *"At the 95th, one ordinary gap in twenty trips the threshold; at the 99th **it is one in a hundred**"* | `0036` §1 — the entry that set the threshold | **True of a uniformly drawn gap, false of the gap the rule tests.** The bracketing gap is **length-biased** (inspection paradox): **37.4%** of measured bracketing gaps exceeded the pooled-99th threshold, and the 99.9th still fails 27%. **The calibration was performed on one distribution and applied to another.** Found by **both arms independently and in the same terms**. Instance A's formulation is now the record's: *"the reference distribution and the test statistic are not the same object"* |
| *"If there is **no insertion instant at or before `τ1`**, the pair is **not live**"* | `0036` §2.3(ii) | **Contradicted approved gate `0021`**, which holds that any record inserted after the window closed **proves the account was alive.** Every pair in that bucket has instants after `τ1` **by construction** — the run records zero accounts with no instants and a minimum of three gaps per account. **18,250 pairs, 76.8% of the filter's exclusions.** Nothing in `0036`–`0039` cited `0021` against it, and `0037` §3 diagnosed the mechanism correctly and then **routed it to Step 14 as a limitation — the wrong disposition for a rule that overrides an approved gate** |
| *"The measured-gap test does **3.45%** of the exclusions and the edge cases 96.55% — and **this holds across every percentile** from the 90th to the 99.9th"* | `0038` §5 | **Wrong twice.** The level was measured on the **201,900**, which §2 of the same entry had just replaced with the 152,126. And **the invariance is arithmetically impossible**: the edge-case count is **constant in the percentile** (22,496, a function of `W` alone) while the gap-test count is `100 − p` of 129,630, so the share **must** move — 36.5% → 5.37% → 0.4%, a **93-fold range**. Both arms found it independently |
| *"The threshold is **derived independently of `W`**"*, and `task-sheet.md`'s *"do not use `W` as an input to the derivation"* | `0036` §3, `task-sheet.md` line 235 | **Unsatisfiable after `0037`.** Any bracketing-gap reference is selected by `τ1`, and **`τ1` contains `W`**. Both withdrawn rather than left standing |
| *"An instant at or before `τ1` **and** one after it"* as the parameter-free rule | `0041` §4 | **Reinstated `0036` §2.3(ii) verbatim** — the rule `0040` §1 had withdrawn **one entry earlier** for contradicting `0021`. **Drafted in the entry and then propagated a second time into the launch instruction**, so both arms received it twice. Priced at **18,903 exclusions from 1,434 of 2,402 accounts**. *"Do not reintroduce a pre-`τ1` requirement in any form"* — **withdrawn twice** |
| *"There is no threshold and **no free parameter**"* | `0042` §1 — the entry that closed the gate | **Deleting the threshold did not decouple anything — it made the coupling total.** The exclusion set **is** the open-ended bucket, a pure function of `W`, running **348 → 949 pairs on DERIV** across the mandated arms. **And `W` was held at 108 for the entire sensitivity test that justified the deletion.** The honest wording is *"no parameter of its own; fully determined by `W`"* |
| *"Excluding pairs that fail the liveness test removes accounts that stopped logging, which are **disproportionately the ones that would have scored never-started**"* — bias 2's **DOWN** direction | `task-sheet.md` Step 14, and **every defence of erring high** from `0036` §1 through `0039` §7 | **Measured false.** The filter preferentially deletes **confirmed continuers** — a Continued pair carries positive episode-level evidence that later silence cannot corrupt, so there is nothing for liveness to protect and the rule deletes it anyway. Of the threshold rule's 1,282 exclusions: **1,079 Continued, 163 S&L, 40 Never started.** Separately, `0040` §3: the mechanism **describes accounts that stopped and the 18,250 were accounts that started late**, so it only ever covered ~9% of the filter |
| *"Both arms measured ALT's exclusion set at **zero pairs** across every `W` tested"* → ALT rejected | `0045` §1 | **That is the DERIV row, where ALT is zero by construction.** ALT = PF-LIMIT ∩ `|A| = 0`, so **ALT's exclusion set *is* PF-LIMIT's never-started exclusion set** — which **`0045` §4.2 itself puts at 604 on APPLY.** *"The same entry gave two counts for the same set and §1 took the one that is zero by construction."* **ALT was rejected on effect using a measurement taken where it cannot have an effect** |
| *"751 pairs with **directly observed** outcomes — 652 continued, 99 left"* | `0046` §2, the table that justified adopting ALT | **652 are directly observed. 99 are not.** `|A| ≥ 1` is observed; **the failure to meet the Continued condition is not.** Under `0034` only Continued rests on positive evidence. `0047` corrected three claims in `0046` and **missed this one**; Red Team's fourth review caught it, and it is what made ALT-BROAD necessary |
| *"The 604 are **exactly** the pairs with no S2 record anywhere"* and *"the DERIV zero is **forced by construction**"* | `0046` §1 | **Counts right, both explanations wrong**, and both are the `|A| = 0` versus "no S2 record" conflation **§5 of the same entry warns against**. APPLY holds **23,260** such pairs and **22,656 stay live** — subset, not equality. And `has_s2` does **not** imply `|A| ≥ 1`: **9,145 DERIV pairs are never-started**, four line-4 pairs satisfy both conjuncts at every arm and are removed by D10. **The zero is a fact of the filter order and this pull date, not a theorem** |
| *"Returning **every excluded pair** as a decliner reproduces the unfiltered population exactly"* — the ceiling identity | `0046` §4 | **False under ALT-BROAD**: it gives an **unattainable 17.3279%**, because the 99 S&L exclusions have `|A| ≥ 1` observed and **cannot** be never-started. **The identity still holds by a different route** — the ceiling returns **only the 604**. Corrected rather than left because **Step 9 reads this sentence** |
| *"Step 7's own dual run **cannot exercise the rule**… the rule is first exercised at Step 8"* | `0046` §7 | **Too pessimistic and refuted by instance B.** The rule **is** exercised on APPLY. **What is true is narrower and is the operative warning: only the APPLY figures carry information, and DERIV's diff is literally `0 = 0` at every arm** |
| *"73.6537% is on no population"* | `0051` §2 | **It is the Continued ceiling on 196,654** — `(144,140 + 703)/196,654` — and **both arms publish it, both JSONs carry the key.** Withdrawn by `0052` §2. **Mode G**, above |
| *"The ruling has since been read as 'after `τ1`' only by accident of when it was written"* | `0053` §1 — the premise of an **amendment to an approved gate** | **False. `0034` — the entry that CREATED the second window, the same date — ruled it in terms: *"Liveness stays anchored at `τ1`."*** `0051` re-affirmed it with both windows in view. **`0053` amended `0021` and withdrew `0048` §9 while leaving `0034` standing, uncited and unmentioned**, so the adopted rule contradicted a live ruling in an approved gate. **`0053` withdrawn in its entirety by `0054`** — the only entry in the log so withdrawn |
| *"The pair could not have produced the evidence the Continued test reads"* — the warrant written into `0021` | `0053` §1 | **False for the pairs the rule was adopted to capture.** A record inserted at `s` can carry any `watched_at ≤ s`, and **`0021` Adoption 3 keeps post-dated records** — so an account last active at `s ∈ (τ1, τ2)` **could** have produced Continued evidence, failing only for evidence dated in `(s, τ2)`. **Do NOT restate the p5-margin support — see the next row** |
| *"The 90 have **p5 margin 1.7 days, minimum 0.13** — demonstrably alive for ~89 of the 91 days"* — the support offered for the row above | `0054` §3, and **restated in this memory until 2026-08-13** | **WITHDRAWN AS CHERRY-PICKED (`0055` §2). That is the tail; the record's own median for the same 90 is 44.5 days**, so for half of them roughly half the Continued window is unobserved. **p5 supported the claim, the median contradicted it, and only p5 was quoted.** Instance B reproduced **p5 = 1.6552, median = 44.5272 on the same 90 pairs.** **The correct ground carries NO margin statistic at all**: a floor is a **worst case, not an expectation**, and even at 0.13 days the Continued condition — which reads **distinct episodes** — is satisfiable by a single binge. **Admissibility sets an endpoint; plausibility does not enter. Both figures are inadmissible.** Both arms argued the whole **class** out of endpoint justification: admissibility is **binary** and a margin **continuous** (A), it is a property of the **support** not the **measure** (B), and `p5 = 1.7` **removes zero pairs from the admissible set** — while reintroducing *"an unowned threshold into the one step whose history is the removal of exactly that shape."* **The median is the figure that would have been quoted had the conclusion needed defending the other way** |
| *"Not one of the four rules drops conjunct 2 — it is the alternative nobody has priced"* | Red Team's **fifteenth** review, the last substantive challenge to the rule | **False. PF-LIMIT IS the no-conjunct-2 rule**, adopted `0041`/`0042` and superseded `0046`/`0048` — *"the rule family was tested against exactly this alternative, before ALT-BROAD existed."* **And the 652 it asked for had been printed since `0045` §1**, whose table gives PF-LIMIT's DERIV split as `751 = 0 NS + 652 Continued + 99 S&L`. **Closed on measurement** (`0063` §1): dropping conjunct 2 excludes **652 Continued pairs on evidence they demonstrably produced**, which is the one thing a liveness rule cannot coherently do. **What survives is real and is now measured: the outcome-conditioning is 652 on BOTH populations** |
| *"ALT-BROAD cut a continuous failure mode at one end, so cut it at `τ2` instead"* | `0052` §1 | **The continuity argument is symmetric and refutes ALT-MATCHED from the other end just as forcefully. It proves NO instant in `[τ1, τ2]` is warranted — not that `τ2` is.** Confirmed by a sweep neither arm was asked for: **smooth, monotone, no elbow, no plateau** |
| *"Widening the floor would have been the FIFTH consecutive bound with a non-covering endpoint"* — the stated reason for preferring ALT-MATCHED | `0052` §4 | **Exactly backwards. Widening to 18,952 is what MAKES the endpoint covering** (`0054` §1). **The rejection reason named the defect the alternative repairs** |
| *"`task-sheet.md`'s 'the silence test is anchored at `τ1` and only at `τ1`' is false"* | `0053` §3 defect 1 | **Withdrawn with `0053`. The clause is TRUE and is restored** — `0034`, `0051`, `0054` |

### Mode F's signature at Step 7 — nine instances, and the diagnosis

`0038` §5 (level on the wrong waterfall line) · `0039` §2 (*"identical on every published number"*
against two artifacts publishing 34.1% and 36.96%) · `0039` §6 (**a divergence invented between arms
that agreed** — A reported both figures and B's matched one exactly; the ~880 are **pairs, not
accounts**) · `0042` §4 (the **deleted** 1,293-day rule's deltas given the subject *"the approved
rule"*) · `0043` §1 (the **DERIV** direction published as the study's) · `0043` §1.2 (a remedy
prescribed on *"the ~40 never-started exclusions"* **that are zero** under the approved rule) ·
`0045` §1 (above) · `0045`/`0046` §4 (**two consecutive bounds with mixed denominators**) · `0048` §7
(frozen-D10 figures **stated without the arms that produced them**, which would make a Step 13
instance file a false divergence).

> **`0046` §0's diagnosis, and it is the durable sentence:** *"The pattern is not inattention to a
> file. **It is reaching for the number that supports the ruling being written rather than checking
> which population produced it.**"*

**Three consecutive bounds had an endpoint outside the feasible set** — `0043`'s ceiling, `0045`'s
floor on the other side, `0046`'s floor on a mixed denominator. **The fourth was refused, by both
arms independently, before the ruling.** Instance A named the stake: the narrow S&L reading *"would
have made this the fourth consecutive bound failing that exact test."* **The standing rule worked
before it could be broken a fourth time, and it worked in the arms rather than in the ruling** — the
one clean win in the block.

### The pattern the Step 7 block adds to the taxonomy

**Five consecutive entries each corrected their predecessor and each introduced a defect doing it**
(`0042` → `0043` → `0045` → `0046` → `0047`) — **and it did not stop at five. `0051` → `0052` →
`0053` continued it, three entries and three more defects.** The amendment's lesson was *a correction
is not discharged until the script and its JSON carry it*. **Step 7's is harder:**

> **A correcting entry is the highest-risk place in the log to introduce an error**, because it is
> written at speed, under a blocking review, and by someone reaching for the number that fixes the
> thing in front of them. **Every correction should be re-derived from its population, not lifted
> from the artifact that reported it** — `0042` §4 and `0043` §2 are the same failure, one lifting a
> sentence from instance A and changing its subject.

**And `0054` §3 adds a second shape the first eleven entries did not show:**

> **Correcting a predecessor by overshooting into the mirror-image defect.** `0052` answered *"ALT-BROAD
> cut a continuous failure mode at one end"* by **cutting it at the other end** — on an argument that,
> read symmetrically, proves **neither** end is warranted. The anchor sweep (`0054` §4) made it
> visible: **smooth and monotone from `τ1` to `τ2`, no elbow, no plateau, no natural cut.**

**The self-referential instances are worth naming individually, because there are now four:**

| Entry | Named the defect | And then committed it |
| :--- | :--- | :--- |
| `0051` | Corrected two instances of *"figure quoted without checking its population"* | **§2 did exactly that**, on `second-brain`'s summary instead of the arms' JSON |
| `0052` | §5 recorded propagation **#12** — a ruling reaching `task-sheet.md` and neither `data-scientist` file | **`0054` §5: #13 is the same failure in the same section, one entry later** |
| `0053` | §3 item 7 **mandated a population label at every use** | **§2 and items 3–6 are unlabelled APPLY figures whose DERIV values differ** — four rows above the row requiring them |
| `0054` | §6 named **0.4033** as a rounding artifact and withdrew a ratio computed from it | **§7 published the bound width as 0.4033** |

---

## Mode B — figures quoted from sources that do not produce them

**Raised four separate times, each time inside work written to answer the previous occurrence.**

1. **B3, round 1.** Layer 4, the bot table and §8 all rested on `days_over_48` from
   `processed/step5/throughput.npz` — **written by nothing in `src/`.** It also disagreed with the
   version-controlled measure: 1,970 / 580 / 39 committed against 2,183 / 844 / 175 published, and
   a 50→48 threshold change cannot take a count from 580 to 844. Once committed, the bot count fell
   **175 → 126** — exactly the import inflation the code claimed to control for.
2. **D3, round 2.** §10's headline C5 figures were not in the repository; the named derivation
   (`step5_rule_costs_v2.py`) **computes no shift at all**. The committed three-class median of
   **29.5 d** — the least alarming figure available — was **absent**, while the artifact led with
   153.4 d. *B3 recurring, inside the section written to answer Red Team.*
3. **F3, round 3.** Revision 4 **affirmatively certified** that every figure came from committed
   code. False for **nine**, two of them the same rows D3 was about. *"A gate artifact that falsely
   certifies its own reproducibility is worse than one that makes no such claim — the false
   certificate defeats the check the Human Lead would otherwise run."*
4. **Round 4, fourth occurrence.** Revision 5's replacement blanket sentence — *"No figure in this
   artifact is produced outside `src/`"* — was falsified by a single decorative figure, "up to
   **164** accounts share one instant." The reviewer called it decorative and said holding on it
   would be scrupulosity.

**Committing the 164 revealed it was also wrong. The true maximum is 198** — 164 had been the
maximum over the **first 4,000 of 155,626** qualifying groups in an exploratory shell.
`mode3_flags.npz` is byte-identical after recomputation, so nothing downstream moved.

> **This is the load-bearing lesson of Step 5: an uncommitted figure is an unverified figure.**
> It was raised four times, dismissed once as decorative, and the decorative one was wrong.

**The fix that finally worked** is not a promise: revision 6 §16 is a **routing table — per section,
per key, exhaustive, no blanket claim** — so any figure greps to exactly one file and one key.

---

## Mode C — costs quoted against baselines that no longer exist

- **E2.** P2's "+16,632" and P3's "+29,858" were computed on the 195,498 Layer-2 survivors, and
  **Layer 2 is not adopted.** On the adopted population they are 16,665 and **50,533** — P3
  understated by **41%**, in the one table that tells the Human Lead what was refused.
- **E6 / revision 3's "40,720 / 23.7%".** Header quoted the full population; percentages were
  computed on the abandoned Layer-2 survivor subset. Dividing the same numerator by the full
  denominator gives 20.9%, which **mixes two bases**. Withdrawn; **32.5% and 26.2%** are the figures
  on the two populations that actually exist, and both denominators are now published.
- **The 30 : 1 ratio (F1).** `46,642 / 1,542`, **ignoring the 16,665** — a removal running the other
  way and itself **10.8×** the 1,542. Against the net exclusion the ratio is **3.1**. "Thirty times
  larger" and "dominant" were not established. Its numerator is also an **upper bound on pairs at
  risk, not a count of flips**. Round 2's "roughly 26 times larger" (E1) is the same error one
  revision earlier.
- **§5's 11.3%.** Attached to the **excess** when it is the share of the **full wave**; present since
  revision 1 and repeated through revision 5. The excess is **10.6%**. Both figures are now attached
  to the quantities they belong to.
- **Step 4's ~86,000 calls.** Divided `total_plays`, **absent from 77% of `users/:id/stats` bodies**,
  so most users forecast as exactly one page. True figure **~210,500**, a **2.4×** error, and it is
  what `0010` cites as the reason a forecast-error circuit breaker is needed at all.
- **`0012`'s "24 of 235 under-count discards."** Read from a **mid-run snapshot of 2,372 users.** On
  the final ledger it is **31 of 287**. Same class as E2 — a figure computed on a population that
  had moved by the time it was published. Corrected in `0023`.
- **Step 4's published deliverables, for the whole life of the project until `0032`.**
  `logs/step4_run.json` and `logs/step4_pull_log.json` — the files `task-sheet.md` **names as Step
  4's deliverable** — were written by a **`--max-users 3` run** and read **2,137 complete / 235
  discarded / 2,410 decided / 102,735 calls** against the true **2,549 / 287 / 2,874 / 126,145**.
  **Stale by 464 decided users and 23,410 calls.** The record-writers fire only from `main()`'s
  `finally` block and neither long run reached it. **The canonical state was never wrong** —
  `state.json` and the append-only ledger held throughout. *"Only the published record was wrong,
  which is the worse failure of the two: a reader with no access to `processed/` had no way to
  know."* `0032`.
- **Step 1's right-censoring margin, on two figures at once.** Step 1 said the frame caps the S2
  finale at **2024-12-31** in five places (it is **2025**) and computed its horizon as **182 days**
  (it is **199** — line 823 assumed `max(W, 91) = 91` against the adopted `W = 108`). **The
  conclusion survives; the margin does not:** ~13 months of clearance becomes **24 days**. Zero
  shows are lost, but `W` is **±18 days** show-clustered, so **the slack is now smaller than the
  uncertainty in the number consuming it.** Corrected by **addendum, not by editing approved text**,
  because Step 1 *relies* on the cutoff and Step 2 *sets* it. `0030`.
- **`show_network` as "a present-day value."** `0016` disclosed it that way and `0030` **supersedes
  that as too generous**: it errs in **both** directions — *Arrested Development* (FOX, 2005) tagged
  **Netflix**, *Community* (NBC, 2011) tagged **Yahoo! Screen**, which no longer exists. *"Not
  present-day, not release-time, and not consistently either"* — strictly worse than the disclosed
  defect, because a present-day value has a bounded direction of error and this has none. **Dropped
  rather than warned**: *"a field that cannot be used is safer absent than present."*

### The sharpest instance: an indifference band quoted as headroom

**`0012` states a replay "with a maximum residual of 0.86 percent against the 2 percent tolerance."**
`artifacts/step4-pilot-counts.json` records `max_abs_share_of_item_count: 0.11707` — **11.7%** —
with a signed range of −191 to +131. **A reader of `0012` alone concludes the tolerance carries 2.3×
headroom over the worst observed case. It never did.**

Worse than a wrong number: the pilot's p95 is **1.4%** and p99 = max is **11.7%** with nothing
between, so **every tolerance from ~1.5% to 11.7% gave the identical partition of those 20 users.**
The quoted figure was not evidence for 2% over any alternative — it was a coincidence of where the
band happened to be read. **The most aggressive end of the band was chosen, with no sensitivity
table, and the choice was not stated as a choice.** On the full run the gap does not exist: 168 of
the 287 discards (58.5%) sit in the 2–5% band. `0023`.

### A claim attached to a phenomenon that has never been observed

**`0012`'s third required output cites "5 duplicates in 14,236 records" as *genuine cross-page
duplicate records*** and builds a required-output obligation on them. Instrumentation records
`cross_page_duplicate_records: 0 affected users, 0 affected records` across 2,137 users and
22,725,090 records. **Cross-page duplicates have never been observed in either run.**

The anomaly that *does* occur is **within-page** — 147 records, the same `id` twice on one page,
meaning a 250-slot page carried 249 distinct records. It is **not a required output, is described
nowhere, and has no stated interpretation.** So the rule mandates measuring something that does not
happen while the thing that does happen is unmeasured and unexplained. Corrected in `0023`; the
adopted rule is unchanged.

---

## Mode D — unit and order-of-magnitude errors

Both of these reached the Human Lead and one entered a ruling.

**"A 907-page user is roughly six hours alone."** At the study's **150 GET/minute** throttle a
907-call user is **6.0 minutes**; the pool's heaviest user is 1,034 pages = **6.9 minutes**. Six
hours is what you get at **150 calls per hour** — and the 23.4-hour whole-pool estimate is computed
at 150/minute, so the two cannot both hold (210,500 calls at 150/hour would be **58 days**).
**Consequence: no single user can stall the run**, so the tail cap has no defence as protection
against a slow user. `0010` records the correction rather than quietly fixing it, because **a cap
defended by the wrong argument is a cap nobody can re-derive later** — and the wrong argument
pointed at a much more aggressive threshold.

**"Median 2,150 days, 8.1%" for the 720.** Quoted as canonical and **written into the D1-round
ruling**. It required **two** departures from the correct basis, and the cause of the second was a
unit bug: **`.astype("int64")` on a tz-aware datetime returns microseconds in the pandas version in
use**, so dividing by 1e9 placed every S2 finale in **January 1970** and the `max()` against it was
**silently inert.**

| Basis for the bound | `max()` with finale | Median elapsed | Open at `W = 60` |
| :--- | :--- | ---: | ---: |
| **Completion prefix — the figure to use** | **yes** | **1,738 d** | **7.92%** |
| Completion prefix | no | 2,190 d | 7.92% |
| Any S1 record | yes | 1,728 d | 8.06% |
| Any S1 record | **no — what was quoted** | **2,150 d** | **8.06%** |

**Caught from arithmetic alone:** `max(finale, x) ≥ x` can only push `T0` **later** and elapsed
**smaller**, so 2,150 > 1,738 is impossible with the `max()` in force on the same set. The finale
term binds for **61.8%** of the 720, which is why its absence moves the median by ~450 days.

**The first correction to this was itself wrong** — it claimed the `max()` had been included and only
the basis differed. Recorded because a correction that is not re-derived is just another claim.

**`projected_hours_remaining: 4.28` for the Step 4 resume.** Wrong by roughly **1.8×** — the true
cost is **~70,000 live calls and ~7.8 hours**. Two structural faults, both in `write_progress()`:
it was measured over **8 users in 100 seconds**, of which **123 pages were served from cache and
were therefore free**, and it is **user-count based**, so it is blind to `0009`'s stratified
round-robin leaving the untouched users as **the heavier half of every bin** (43.3 → 50.5 → ~58
mean pages per user across the three tranches). **The exact figure is one summation over
`pull_order.jsonl` at zero API calls and has not been computed.** `0032`, README item 37.

**"The pull exited cleanly."** Repeated throughout the project, including in the session that ran
it. `step4_progress.json` carries `finished: false` and `stop_reason: null`; both console logs end
mid-stream with no exit line; the `finally` block never ran. **The right word is "safely, not
cleanly"** — the fsynced ledger, atomic progress file and raw cache all survived, no data was lost
and nothing was double-counted. **The distinction is not pedantry:** *"'exited cleanly' implies the
run's own record is trustworthy, and it was the untrustworthy record that this entry exists to fix.
Recording the pull as clean is what let a stale deliverable sit unexamined."* `0032`.

---

---

## Mode E — a coincidence that would have read as corroboration

**Not an error. A claim correctly refused before anyone made it**, and the clearest example in the
study of an agent declining a result that flattered it.

Step 6 run 2's instance A produced **`W = 107`**, which is also one of the two values run 1 produced.
The obvious reading is that two independent runs converged. **Instance A's own §2 refuses it:**

> *"It landed on 107 … and that is not confirmation of anything. … Computing the 90th percentile of
> the same distribution twice and getting the same answer is arithmetic, not agreement — it says the
> two runs share a population and a lag definition, which was already known from run 1's identical
> intermediates. **It carries no independent evidence that 107 is right.** The thing that would be
> informative is a divergence."*

`0026` records the same point. **The check this generalises to:** when a re-run reproduces an earlier
number, ask whether the two computations could have differed. If the rule fixes the statistic and the
sample, agreement is entailed and carries no information. **Only a divergence is evidence, and the
dual-implementation regime exists to produce divergences, not agreements.**

The same logic sits behind `0024`'s deeper point: **making a definition unambiguous does not make the
result insensitive to it.** Fixing "flattens" to "90th percentile" removed the *disagreement*; it did
not remove the *dependence*, which is why Step 13 must still span 46 to 107.

## The three errors that originated in the main session and reached the Human Lead

Caught by the analytics-engineer. **Two entered rulings.**

1. **C5 reported as 4,188 against the artifact's 5,694**, on the basis that
   `pair_contamination.csv` had no column for air-date-stamped S1 evidence. **It does** —
   `s1_ev_airdate`, added in revision 2, after the header had been read. 5,694 is correct; 4,188 is
   the two-class subset.
2. **"All 425 C5 pairs with no S2 evidence are already inside the 1,542."** **False. The sets are
   disjoint by construction** — C5 requires a *clean* completing record, the 1,542 a *contaminated*
   binding one. Overlap is exactly **0** and the correct count is **720**. **The ruling that C5
   needs no separate ruling cited this claim as half its basis.**
3. **The 2,150 d / 8.1% figure above**, quoted as canonical into a ruling. Method-dependent and
   produced by the unit bug.

**All three conclusions survive**, on evidence Red Team independently endorsed as the right test.
**The stated bases did not.** See [[open-items-and-contradictions]] "Claims whose basis moved."

---

## Step 3's three, closed

Funnel floor line printed **6** when the true total was **232** (a per-round column summed wrongly
into a funnel row). *"Zero errors"* when the run had **16 HTTP 5xx, 1 transport error, 9 transient
retries** — all recovered, which is why the retry-with-backoff branch is the one live-tested failure
path. `reciprocal_pairs: 1353` was a **per-record double count**; the true value is **1,172**, since
fixed and regenerated.

## The one accepted risk

The liveness bound is inflated, and it stays that way by Human Lead ruling. A bound that
reclassified the pairs it could explain away would no longer be a bound. Full reasoning in
[[gate-step1-outcome-definition]].

## One premise still asserted and unobserved

That Trakt metadata merges and splits make `episode.ids.trakt` disagree with `(season, number)`.
Zero disagreements on the probe profile — **not contradicted, untested.** The same mechanism
underwrites D9's split signature. [[open-items-and-contradictions]] N4.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[gate-step5-contamination]], [[open-items-and-contradictions]].
