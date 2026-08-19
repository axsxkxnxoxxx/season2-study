# Decision 0055 — the DERIV floor is widened, the floor's ground is restated without the margin argument, and propagation gains a grep control

| | |
| :--- | :--- |
| **Decision** | **The DERIV started-and-left floor is widened to 16,655 / 147,370 = 11.3015%** and the **DERIV Continued ceiling to 121,570 / 147,370 = 82.4930%** — `0054` §1's identity was implemented on APPLY only. **The floor's margin argument is WITHDRAWN as cherry-picked**; the ground is admissibility, not plausibility. **A standing propagation control is added to `CLAUDE.md`: seven surfaces, read-back PLUS grep.** Propagation **#14–#17** fixed and three defects in `0054` corrected. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **eighth** Step 7 HOLD |
| **Amends** | `decisions/0054` §1, §3, §6, §7, §8 — in place |
| **Propagated to — SEVEN surfaces** | `task-sheet.md`; `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md`; `artifacts/`; `.claude/agent-memory/second-brain/`. **Plus `CLAUDE.md`**, which now carries the control. **Verified by grep with hit counts reported, not by reading the edits back** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-13**, which is tomorrow. Entries `0052` through `0057` all carried it, and the drift began when the session's clock advanced mid-work and the date was carried forward from an earlier entry rather than re-read. **Corrected in place across every surface, with this note, rather than silently rewritten** — the decision log is a public tracked artifact. Found by Red Team on its eleventh review; recorded at `0058` §6.

---

## 1. The DERIV floor — `0054`'s own identity, implemented on one population of two

`0054` §1 asserted numerical identity between ALT-BROAD-with-a-covering-floor and ALT-MATCHED **"on all
three identified sets."** **It widened APPLY and left DERIV alone.**

| DERIV, n = 147,370 | Derivable from the files | Correct |
| :--- | ---: | ---: |
| **S&L floor** | 16,744 → **11.3619%** | **16,655 → 11.3015%** |
| S&L ceiling | 16,843 → 11.4291% | **unchanged** |
| Width | 0.0672 pp | **0.1276 pp** |
| **Continued ceiling** | 121,481 → **82.4327%** | **121,570 → 82.4930%** |

**The channel is 89 pairs on DERIV against 90 on APPLY**, and `16,744 − 89 = 16,655`.

**Corrected on execution: the defect was an OMISSION, not a stale figure.** This entry first said the
un-widened DERIV pair was *"in every file."* **It was in none of them.** The analytics-engineer grepped
before editing and found **zero hits on every superseded form** — `11.3619`, `82.4327`, `0.0672`,
`16,744`, `121,481`, and their unformatted variants — across all five spec files. **There was no DERIV
started-and-left bound and no DERIV Continued ceiling anywhere in the spec.** The harm is identical, and
worse-shaped: only APPLY was documented as widened, so a Step 9 instance derives 16,744 → 11.3619%
itself and has nothing to contradict it.

**Both corrected numbers were already on the disk `0054` was written from** —
`artifacts/step7-liveness-mm-a.md` prints `[11.3015%, 11.4291%]` and `[82.3655%, 82.4930%]`;
`mm-b.md` prints `16,655 / 147,370` at width 0.1276 pp. They were computed under ALT-MATCHED and **not
carried across when the rule was reverted.**

**`task-sheet.md` mandates publishing DERIV bounds at Step 9**, so uncorrected this publishes a DERIV
floor **0.0604 pp above the case the filter exists to guard against** — by `0047` §3's own test, **the
sixth consecutive non-covering endpoint, created by the entry written to stop the fifth.**

**Assignment, and it is deliberate.** The correction is a **spec propagation**, so it went to
`analytics-engineer`. **Both `data-scientist` arms verify it against their own stored outputs rather
than accepting it** (`specs/step7-deriv-floor-verification.md`), because an unverified number that came
from the Human Lead is exactly the failure `0052` §2 recorded.

## 2. The floor's ground, restated — the margin argument is withdrawn

`0054` §3 refuted ALT-MATCHED's warrant with **"the 90 have p5 margin 1.7 days and a minimum of
0.13."** **That is the tail.** The record's own median for the same 90 is **44.5 days** (`0053` §5,
instance B, carried in Step 14): for half of them roughly half the Continued window is unobserved. **p5
supported the claim, the median contradicted it, and only p5 was quoted.**

**The correct ground carries no margin statistic at all.** A floor is a **worst case, not an
expectation.** The question is whether a channel pair *can* in truth be Continued, and it can — silent
from `s`, it may hold Continued evidence dated anywhere in `[F2 air, s]`, and even at margin 0.13 days
it could have completed S2 inside the unobserved remainder. **Admissibility sets an endpoint;
plausibility does not enter.** **p5 = 1.7 and median = 44.5 are both inadmissible**, and the median is
the figure that would have been quoted had the conclusion needed defending the other way.

**Measured first, because the alternative was that the choice is numerically empty**
(`src/step7_floor_extremes.py`, zero API calls, channel counts and both endpoints asserted against the
arms' figures):

| | n | channel | floor, NONE Continued | floor, ALL Continued | **movement** | ceiling |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | **90** | 19,042 → 9.6830% | **18,952 → 9.6372%** | **0.0458 pp** | 19,745 → 10.0405% |
| **DERIV** | 147,370 | **89** | 16,744 → 11.3619% | **16,655 → 11.3015%** | **0.0604 pp** | 16,843 → 11.4291% |

**The endpoint moves on both populations**, so the choice is consequential — and it is still decided by
admissibility, not by the size of the movement. **The widening is one-sided: the ceiling does not
move**, since the 90 are already counted as started-and-left in it; the **Continued** ceiling moves in
lockstep with the floor.

## 3. Propagation gains a grep control, and a seventh surface

**Read-back plus grep. Read-back alone is not verification.** Written into `CLAUDE.md` under
`## Propagation`.

**Reading an edit back proves the new text landed. Only grep proves the old text is gone** — and a file
can hold both at once. **Three consecutive failures were exactly that**, an adopted figure and its
superseded predecessor live in the same file, sometimes ten lines apart, each declaring the other
wrong. `0054`'s header says *"each edit verified by reading the file back,"* and that claim was true
and useless.

**The surface is seven, not five.** `artifacts/` and `.claude/agent-memory/second-brain/` were never
checked. **`0052` §2 records that stale `second-brain` memory already produced a wrong ruling** —
73.6537% mislabelled as a "Continued floor", adopted without checking the arms' JSON, published as
`0051` §2, and it would have driven a Step 9 instance to delete a correct number.

**And the dual diff cannot catch any of this.** Both members of a pair are byte-identical by design, so
an error written into both is invisible to it. **Propagation is checked by grep, never by the diff.**

**The negative grep is not sufficient on its own, and this run proved it.** A figure that was never
written **returns zero hits on every superseded form of itself.** Had the analytics-engineer run only
the mandated grep, it would have reported a clean pass on a file set that contained the defect. **So the
control gains a positive counterpart: grep the CORRECTED string and require non-zero.** A defect has two
shapes — the wrong figure present and the right figure missing — and the negative half sees only the
first. **Added to `CLAUDE.md` by the agent that found it**, on its first run under the control.

**A grep hit is not a defect until the line is read**, and the register of known false positives now has
**six rows** *(the entry first said "four"; corrected by `0056`, which also **withdraws the `9.6830` row
as wrong** — see there)*:

| String | Legitimate reading | Superseded reading |
| :--- | :--- | :--- |
| **632** | frozen-D10 never-started component at `W = 125` (`0051` §3 item 9) | a deleted liveness threshold |
| **703 / 793** | **703** is the adopted APPLY exclusion count | **793** is ALT-MATCHED's |
| **16,744** | post-liveness started-and-left **count** on **147,271** → 11.3695% (`bb-a.md:109`) | the un-widened DERIV floor on **147,370** → 11.3619% |
| **0.0672** | DERIV exclusion **share of population**, `99 / 147,370` = 0.0672% (`bb-a.md:65`) | the un-widened DERIV bound **width** in pp |
| ~~**9.6830**~~ | ***ROW WITHDRAWN (`0056`) — there is no legitimate reading.*** The sub-interval's conditioning constrains the **604**, not the 90, so **its floor moved with the bound floor to 9.6372%** | **every** occurrence is superseded |
| **0.4033** | **none — it has no legitimate use anywhere** | B's rounding artifact for the APPLY bound width |

**The `9.6830` row was wrong and is withdrawn by `0056`.** It was called "the sharpest of the six"; it
was the most damaging. **Registering it as exempt disarmed the grep control against the one string it
most needed to catch, on four surfaces, in the section that created the control.** The claim that the
sub-interval is "over the 99" is what produced it: **the conditioning constrains the 604.**

**`16,744` and `0.0672` were found by the analytics-engineer** in the artifacts sweep and **both turn on
population** — which is why the standing rule that every figure states its population at the point of
use is also what makes the grep control usable. **`9.6830` and `0.4033` were found by `second-brain`**,
and `9.6830` is the sharpest of the six: it is **the same estimand at two scopes**, superseded over the
703 and correct over the 99, so only the surrounding interval distinguishes them.

## 4. Propagation #14 through #17

| # | Where | What was there | Fixed to |
| :-- | :--- | :--- | :--- |
| **14** | `task-sheet.md` Step 7, **28 lines below the line restoring it** | *"'Anchored at `τ1` and only at `τ1`' is WITHDRAWN — an instance following it reproduces 703 instead of 793"* | The anchoring restored, ALT-MATCHED's per-branch form named as withdrawn, **703 correct and 793 a divergence** |
| **15** | `task-sheet.md` Step 13 | ALT-BROAD's series **537 … 864 labelled "ALT-MATCHED"**, and the **1.5× coupling** that `0052` §8 recorded as fixed in three files | Series relabelled **ALT-BROAD**, coupling **1.61×**, ALT-MATCHED's own series named as superseded |
| **16** | **Both `data-scientist` files, byte-identical** | `[9.6830%, 10.0405%]` width 0.3575; `1,307` / `100.6646%`; and **"Continued 73.6537% (73.6995% was ALT-MATCHED's, withdrawn)"** | The adopted bound, `1,397` / **100.7104%**, and **73.6995% as the adopted ceiling** |
| **17** | `task-sheet.md` Step 14, four bullets | ALT-MATCHED's limitations published as current, citing withdrawn `0053`; the **70.3%** channel figure; and PF-LIMIT's **0.032 pp** restated four lines above the sentence forbidding it | Re-scoped to the restored rule; **52.4%** restored; DERIV **+0.0042 pp** |

**#16 is the severe one.** It told an instance the **adopted** Continued ceiling was *"ALT-MATCHED's,
withdrawn"* — an instance following it deletes a correct number, which is `0052` §2's failure exactly.
**Both copies carried it identically, so the diff structurally could not see it**, and `CLAUDE.md` sends
the agent to its definition file first.

**Two of #17's bullets were not merely stale but false under the restored rule.** D10 admits
`τ2 = τ_pull`, so ALT-MATCHED had 20 pairs with a zero-length post-`τ2` window and 2 excluded by
construction — **at `τ1` that cannot arise**, because D10 forces `τ1 ≤ τ_pull − 91 days`. And clamping,
recorded as **not** inert at `τ2`, **is** inert at `τ1`: the clamp value postdates every D10-surviving
`τ1`. `0053` ruled the old form *"must not be restated"*; at `τ1` the old form is the correct one.

**And `0049` §6's launch-snapshot control did not cover this.** It governs **the rule**. **The bound is
not the rule** — the third control added to the propagation problem does not reach the thing that broke.

## 5. Four defects in `0054`, corrected in place

*(This heading said "Three" above four bullets; corrected by `0056`.)*

- **§1's identity table carried no population label** — in the entry whose own standing rule is that
  every figure states which population produced it at the point of use. It was APPLY.
- **§7 published width 0.4033 pp** — B's rounding artifact, differenced from rounded endpoints —
  **four paragraphs after §6 withdrew B's 52.7% for being one.** `793 / 196,654 = 0.40325`, so **the
  width is 0.4032 pp.**
- **§7's width 0.4033 survived in `task-sheet.md`** after being fixed in `0054` §7 — the correction
  landed in the decision entry and not in the file an agent reads, which is the failure this entry
  exists to control, committed inside it. **Found by the analytics-engineer, which declined to fix it
  because its brief said not to touch the APPLY figures, and reported it instead.** Corrected to
  **0.4032 pp**.
- **§8's *"every figure for both rules is already on record"* is false for 18,952.** It is on record
  only as **ALT-MATCHED's floor over 793 exclusions**; **no arm has asserted it as the floor over
  ALT-BROAD's retained set**, and both operative deliverables still print 9.6830%. A
  dual-implementation step adopted a bound **neither instance had reproduced.** The arithmetic is the
  same either way; the assurance is not, which is why §1's verification was ordered.

## 5a. What was deliberately not touched

**The `analytics-engineer` pair carries no started-and-left bound, no Continued ceiling and no Step 9
content**, and was left unedited. **Step 9 belongs to `data-scientist`.** Writing Step 9 bound figures
into a Step 8 spec would create a surface with no consumer and invite a Step 8 instance to publish
bounds it does not own. Their APPLY/DERIV population statements already carry both labels side by side
and are correct. **Reported as a judgement rather than made silently**, which is the right shape.

**`artifacts/` is stale in four lines and is NOT YET STAMPED.** `step7-liveness-bb-{a,b}.md` carry the
un-widened DERIV bound `[11.3619%, 11.4291%]` and Continued ceiling `[82.3655%, 82.4327%]`. **The
exposure is worth stating plainly: the `mm` files hold the correct DERIV figures and the `bb` files hold
the wrong ones, and the `bb` pair is the one named for the adopted rule.** The arms' own deliverables
disagree with each other in the direction opposite to which rule is adopted.

**The stamp is deliberately held until both verification arms report**, so neither reads the corrected
figures out of its own earlier deliverable instead of recomputing them. **This sentence first read
*"is stamped, not rewritten,"* which asserted a step that had not been taken** — instance B caught it
and reported the grep control failing on both halves there. **That is the error this entry exists to
control, committed inside it for the second time**, after the `0.4033` width at §5.

## 5c. Both `data-scientist` arms CONFIRM the correction, and both refuse the margin argument

**All five DERIV rows confirmed by both instances, independently, from their own `W = 108` ALT-BROAD
masks. Nothing refuted.** Channel **89**; floor extreme-ALL **16,655 → 11.3015%**; floor extreme-NONE
16,744 → 11.3619%; ceiling 16,843 → 11.4291%, **unchanged between extremes**; Continued ceiling
**121,570 → 82.4930%**. APPLY reproduces at 90 / 18,952 / 19,745 / 144,933. **The endpoint moves — A
gives 0.060392 pp DERIV and 0.045766 pp APPLY, B gives 0.0604 and 0.0458 — and the S&L ceiling moves
0.000000 pp on both.**

**Instance A's confirmation is independent in code**, not only in execution: no proposed value is
asserted in its script, the proposal is loaded as data and a mismatch prints `REFUTED`. It also
re-derived the primitive the channel turns on — the per-account last insertion instant — from
`full_scan.npz` against the stored calibration, **max abs diff 0.0 s**. It declined to rebuild the Step
1 outcome masks, **naming that as a rerun that was not ordered**, and stated it as a scope limit.

**Instance B adds the figure that makes the defect legible: on DERIV the 89 are 47.3% of the entire
bound width.** The un-widened DERIV floor was missing **nearly half its own uncertainty.**

**Both arms go further than §2 and argue the whole CLASS out of endpoint justification**, and they are
right:

- **A:** admissibility is **binary** and a margin is **continuous**, so no margin value can discharge
  the question. **At 0.13 days the Continued condition is still satisfiable** — it reads distinct
  episodes, and a single binge clears it. **Admitting the class admits the selection, and the selection
  demonstrably happened.** Its test: *would the statistic at any value move the endpoint? If not, it is
  commentary.* Margin statistics belong in the limitations narrative as a statement about **resolving
  power.**
- **B:** the same conclusion by a different route — **admissibility is a property of the support,
  plausibility of the measure**, and `p5 = 1.7` **removes zero pairs from the admissible set.** It
  reproduced **p5 = 1.6552 and median = 44.5272 on the same 90 pairs**, confirming the cherry-picking
  charge arithmetically, and notes the argument would **reintroduce an unowned threshold into the one
  step whose history is the removal of exactly that shape.**

**Routed, not acted on (instance A):** pure admissibility **has no stopping rule**, so the honest claim
is that the bound is covering **with respect to the identified channels**, not covering full stop —
which is why **D4 and D9 must stay published alongside rather than folded in.** To Step 14.

**D-2, against this entry's own measurement.** `src/step7_floor_extremes.py` **reads instance `a`'s
masks only and hardcodes its conclusions as asserts**, so §2's "measured" table was **single-instance
with no refutation path** — it could confirm and could not refute. **Both arms have now recomputed it
independently**, which is what the table needed and did not have when it was written.

**A spec ambiguity both arms found independently, which is the dual run working.** The channel window is
written **`(τ1, τ2]`** in `specs/step7-deriv-floor-verification.md` item 1 and **`(τ1, τ2)`** in its
Background, in `task-sheet.md` and in both definition files. **Both arms measured it inert at `W = 108`
— zero pairs sit exactly at `τ2`, verified rather than assumed — and both reported it unspecified rather
than picking one.** It is a load-bearing predicate and **is not resolved here.**

**Named so they cannot later be mistaken for endpoints (instance B):** a joint-state reading of the
ceiling question yields **16,754 / 19,655.** They are not bound endpoints.

~~**Added to the false-positive register (instance B): a third legitimate reading of `16,744`** at
`artifacts/step7-sensitivity-b.md:76`.~~ **CORRECTED (`0056`): it was NOT added.** Row 3 of the register
named one reading. **This entry asserted a completed action that was not taken — the §5a failure, in the
same entry, for the third time.** The third reading is now in the register, which lives in
`second-brain`'s glossary.

**Two DERIV figures the record stated nowhere (instance A), now in the spec:** the three-ceiling sum is
**100.1276% on 147,370**, excess **0.1276 pp = 188 = 99 + 89**. **The excess equals the bound width on
DERIV** because the never-started exclusion component is 0 there, so each of the 188 is double-counted
exactly once. **The coincidence is DERIV-only** and does not carry to APPLY.

## 5b. Three findings from `second-brain`, recorded without disposition

**1. Its APPLY split was wrong by one in each direction, and that is what produced V7.** It carried
never-started 33,373 / **Continued 144,141** / **S&L 19,140**; the arms carry **144,140 / 19,141**
(`0052` §2's `(144,140 + 703) / 196,654`, `0053` §3 item 8's branch-(ii) count). **Both sum to 196,654,
so its arithmetic check passed and the split never did.** On 144,141 the Continued ceiling computes to
**73.6542%**, not 73.6537% — **which is exactly why the figure looked unreconstructible**, and is the
whole mechanism of the wrong ruling at `0051` §2. Confirmed here: `19,141 + 604 = 19,745 → 10.0405%`,
and `33,373 + 19,141 + 144,140 = 196,654`.

**2. `0054` §7 published the artifact `0054` §6 withdrew** — logged as U1, already corrected in §5
above. It names this as the **fourth** instance of the same self-referential shape, after `0051` §2,
`0052` §5 → `0054` §5, and `0053` §3 item 7.

**3. U2 — every propagation failure count in the record is stated against FIVE surfaces.** `0044` §3.1,
README item 46, `0050`, `0052` §5 and `0054` §5 all count against five, and **all eighteen failures were
found on surfaces 1–5.** **The failure rate on `artifacts/` and on `second-brain`'s memory is
unmeasured, not zero** — the nine unstamped Step 7 deliverables are the first named instance on surface
6. **Whether the count is restated against seven is not decided here.**

## 6. What Red Team clears, and what stays a limitation

**It does not contest the rule statement, the `τ1`-only anchoring, the revert's ground, `0021`'s
in-place restoration, `0048` §9's restoration, or the APPLY bound's arithmetic.**

**Closable over, all routed to Step 14 and none repaired here:** the biconditional gap (`0021` licenses
sufficiency only); the calibration residual tail and its `W = 108`-only scope; arm-wide residual
stability; Step 8's position-6 population reconstruction; and the population mismatch, on which the
DERIV point estimate lies outside its own bound.

**Still unspecified and reported, not reconciled:** the two bootstraps differ in `B` and seed —
A at 4,000 / 20260813, B at 2,000 / 20260814 — and **the spec fixes neither** while Step 9 must
attach confidence intervals.

> ***CORRECTED, NOT MARKED, 2026-08-19 (`0118` §2): the STATISTIC half of this pairing was NEVER TRUE. Arm `a` published BOTH levels and paired movements — on the `bb` gate-closing run and on the `mm` run alike. A mark is for a claim that was true and got superseded; this one was wrong when written. The arms diverged on TWO elements, `B` and the seed.*** **All are now fixed** — `B` = 10,000, seed 20260818 (`0103`), statistic = BOTH
> (`0118`). `0052` §6 called this *"unreconciled
and now specified"*; **it is not specified in any file.**

**Also carried:** the robustness-survival divergence **792 (A) against 791 (B)** from a `τ_pull`
restriction A states and B does not, and `0052` §6's bound-versus-sampling ratio **45%**, which is
**50.9%** under the widened bound and is not updated in either arm.

## 7. Scope

- **No rule change.** ALT-BROAD stands, silence anchored at `τ1`.
- **No rerun.** One endpoint corrected on one population, one ground restated, four propagations and
  three defects.
- **Zero API calls**, including `src/step7_floor_extremes.py`.
- **Step 8 does not launch.**
