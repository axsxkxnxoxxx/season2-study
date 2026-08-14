# Decision 0056 — the four figures derived from the started-and-left floor are corrected, and the dependency list that should have caught them is written

| | |
| :--- | :--- |
| **Decision** | **The conditional sub-interval is [9.6372%, 9.7333%], width 0.0961 pp**, and the attainable-corner table and both sampling ratios are corrected with it. **`9.6830` is REMOVED from the false-positive register — it has no legitimate reading.** **The artifact stamp is rewritten**; certifying "everything else stands" was false. **A dependency list is added to `CLAUDE.md` under `## Derived figures`.** `0055`'s three counting defects fixed, the `0021` warrant added where the never-started bound is published, and **the bootstrap specification recorded as a Step 9 blocker.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **ninth** Step 7 HOLD |
| **Amends** | `0055` §3 (register row and count), §5 (heading), §5c (an asserted action not taken); `0052` §6, struck in place |
| **Propagated to — SEVEN surfaces** | `task-sheet.md`; both `data-scientist` files; `artifacts/step7-liveness-bb-{a,b}.md`; **`second-brain`'s glossary — WHICH IS NOT SURFACE 7. Surface 7 is the DIRECTORY** (`0057`), and `open-items-and-contradictions.md` was left carrying the superseded sub-interval with a ✓ one line from the corrected bound; **`CLAUDE.md`**, which carries the dependency list. **Not touched, checked not assumed:** both `analytics-engineer` files — they hold no Step 9 figures |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-13**, which is tomorrow. Entries `0052` through `0057` all carried it, and the drift began when the session's clock advanced mid-work and the date was carried forward from an earlier entry rather than re-read. **Corrected in place across every surface, with this note, rather than silently rewritten** — the decision log is a public tracked artifact. Found by Red Team on its eleventh review; recorded at `0058` §6.

---

## 1. The defect: an endpoint moved and the figures computed from it did not

**`0055` widened the started-and-left floor and left four derived figures at their un-widened values.**
That is the same failure as `0054`, which widened APPLY and left DERIV — **one entry apart, and neither
was caught by the control written in between.**

**The conditional sub-interval is the started-and-left share *given that every never-started exclusion
is a true decline*. That conditioning constrains the 604. It says nothing about the 90.** So its floor
moves with the bound floor:

| APPLY, n = 196,654 | Published | Correct |
| :--- | ---: | ---: |
| sub-interval floor | 19,042 → 9.6830% | **18,952 → 9.6372%** |
| sub-interval ceiling | 19,141 → 9.7333% | **unchanged** |
| width | 99 / 196,654 = 0.0503 pp | **189 / 196,654 = 0.0961 pp** |

**The record had already computed this and warned about it in terms.**
`artifacts/step7-liveness-mm-a.md:217`, written for the *reverted* rule:

> **Conditional sub-interval, LABELLED and NOT the bound: [9.6372%, 9.7333%], width 0.0961 pp** … Note
> it is now **0.0961 pp wide, not `0049`'s 0.0503 pp**; Step 9 must not carry the old number.

**`9.6830%` is correct in exactly one regime — ALT-BROAD with the un-widened floor — which is the regime
`0055` §1 withdrew.** It was live on **four surfaces**: `task-sheet.md`, both `data-scientist` files,
and `second-brain`'s glossary at two lines. **All four corrected.**

**The DERIV half is correct and was not touched.** On DERIV the conditioning is **vacuous** — zero
never-started exclusions — so the bound and its sub-interval genuinely coincide at
`[11.3015%, 11.4291%]`.

## 2. The other three derived figures

| Figure | Was | Now |
| :--- | :--- | :--- |
| **Attainable-corner table**, `bb-a.md` — the floor corner | *"All 604 are true declines; all 99 in truth continued"* → NS 16.9704%, Continued **73.3466%**, S&L **9.6830%** | *"…all 99 **and all 90 channel pairs** in truth continued"* → NS 16.9704%, Continued **73.3924%**, S&L **9.6372%**. Sum verified: `33,373 + 144,329 + 18,952 = 196,654` |
| **S&L bound ÷ sampling width**, `bb-a.md` | **0.47×** on the withdrawn 0.3575 pp | **50.9%** — `0.4032 / 0.7922` |
| **S&L bound ÷ sampling width**, `bb-b.md` | **6%** | **50.9%**. The 6% was computed on the **conditional sub-interval this arm had itself argued is not the bound** (`0052` §6), at its pre-widening width. **It understated the systematic range against sampling error by roughly 8×** |

**The other corner row is unchanged and that is stated rather than left implied** — *"all 604 started
and left; all 99 are true exits"* puts the 90 in started-and-left already.

**Reported, not reconciled:** `bb-a` published **0.47×** where `0.3575 / 0.7922 = 0.4513`. **The arm's
own figure and the reconstruction from the stated width differ**, and `0052` §6 called the
reconstruction *"A's figure"* when it is not exactly that.

## 3. `9.6830` is removed from the false-positive register

`0055` §3 registered it as legitimate — *"the floor of the conditional sub-interval over the 99"* — and
called it **"the sharpest of the six."** **It was the most damaging.**

**The premise is false: the sub-interval is not "over the 99."** Its conditioning constrains the 604,
which is why its floor moves with the bound floor. **Under the adopted rule `9.6830` has no legitimate
reading anywhere** — the same status the register gives `0.4033`.

**And the consequence is structural, not clerical. Registering a string as a false positive disarms the
grep control against it.** The exemption was granted to **the one string the control most needed to
catch, on four surfaces, permanently, in the section that created the control.** `CLAUDE.md` now says
so in general terms: register a string only when its legitimate reading is verified live **under the
adopted rule**, and withdraw the row the moment it is not.

**The register moves to one canonical location** — `second-brain`'s glossary — because it was spread
across `0055` §3, `0055` §5c and the glossary with no home, while being a precondition for a control
`CLAUDE.md` makes mandatory. **Instance B's third legitimate reading of `16,744` is now actually in
it.**

## 4. The stamp is rewritten — it certified superseded figures

The stamp added to `bb-{a,b}` closed with *"Everything else in this file stands, including the exclusion
counts, the never-started bound, and every point estimate."*

**That sentence was false for at least three figures it did not name** — the sub-interval, the corner
table, and the sampling ratio — **all three of them derived from the floor the stamp itself was
announcing had moved.** **A stamp that affirmatively certifies superseded numbers is worse than no
stamp**, because it converts a stale figure into a checked one.

**Rewritten:** it now names every derived figure in a table, ~~marks each occurrence inline~~
***— that clause was FALSE when written and is the fourth asserted-but-not-taken action in three entries; the marking was actually done by `0057`, which also bounded the claim: `0.0672%` and `0.3575%` as shares of population are legitimate and deliberately unmarked*** — and states
that **it certifies nothing beyond that table.** What is positively unchanged is **listed, not
implied** — the exclusion counts, the never-started bound, the three point estimates — and everything
else is **unverified by the stamp rather than certified by it.**

**This is propagation failure #19 and the first ever found on surface 6** — found **inside the fix added
for surface 6**, one entry after that surface was added. **U2 stands: the eighteen-count is a
surfaces-1–5 count and is not renumbered.**

## 5. The dependency list — `CLAUDE.md`, `## Derived figures`

**When a bound endpoint moves, every figure computed from it moves.** Twice in consecutive entries an
endpoint was corrected and its derived quantities left behind. So each endpoint now carries a written
list, **checked as a set whenever that endpoint moves** — not the figure that prompted the correction,
the whole set.

- **Started-and-left floor — four:** the conditional sub-interval floor; the attainable-corner table's
  floor corner and its Continued value; the bound ÷ account-clustered sampling width ratio, per arm;
  and the Continued ceiling.
- **Never-started floor — three:** the corner table's floor corner and Continued value; the ratio; the
  Continued ceiling. It has **no** sub-interval, because the sub-interval conditions on this bound's own
  exclusion set.
- **Any ceiling — three:** the three-ceiling sum and its excess, per population; the excess mechanism
  count; and the corner row that attains it.

**Both populations are separate lists with separate arithmetic**, and a correction applied to one and
not the other is the same defect as not applying it at all — which is exactly what `0054` did. **Rows
are added, never removed.**

## 6. `0055`'s three counting defects

- **§3 said the register "has four entries" above a table with six rows.** Corrected to six, and the
  table is now five after the `9.6830` withdrawal — stated here rather than left to be recounted.
- **§5's heading said "Three defects in `0054`" above four bullets.** Corrected.
- **§5c claimed instance B's third reading of `16,744` was "added to the register." It was not.**
  **That is an asserted-but-not-taken action for the third time in one entry**, after §5a's stamp claim
  and the `0.4033` propagation. **It is now actually added.**

## 7. The `0021` warrant, where the never-started bound is published

Instance B measured the channel's never-started component — **207 on APPLY, 3 on DERIV** — and published
it with no reason given for why it does not lower the never-started floor. **It does not, and the
reason is the anchoring, not the count.**

**Never-started is the null `|A| = 0`, read at `τ1`, and every one of the 207 has an insertion after
`τ1`** — which is exactly what gate `0021` licenses: *an insertion after the window closed proves the
account was alive.* **Their null is observed, not conceded.** The 90 differ because the **Continued**
condition they negate is read at **`τ2`**, and they are dormant before it.

**The warrant existed only at Step 14 while `task-sheet.md` published the bound with no such clause.**
It is now stated at the point of publication and in both `data-scientist` files — **without it, a reader
who has seen the started-and-left widening reopens this bound.**

## 8. The bootstrap is a Step 9 blocker

**The two Step 7 arms diverged on all three of `B`, seed and statistic** — A at 4,000 / 20260813 /
movements, B at 2,000 / 20260814 / levels — **and a dual step whose confidence intervals are built three
different ways produces a divergence that proves nothing.**

**`0052` §6 recorded this as "unreconciled and now specified." It was never specified: the string
"bootstrap" appears ZERO times in `task-sheet.md`, `CLAUDE.md` and all four pipeline agent files.**
**That claim is struck in place** — a completed action asserted and not taken, the same class as `0055`
§5a and §5c. **This is the fourth instance of that shape in three entries.**

**Recorded as blocking Step 9, not Step 8.** The resampling unit is the **account** (clustered,
`0044`); `B`, the seed and levels-versus-movements **must be fixed identically for both arms in the spec
before Step 9 runs**, and both `data-scientist` files now instruct an instance to **say so and stop**
rather than choose.

## 9. What Red Team clears, and what it added

**It does not contest the rule, the `τ1` anchoring, the revert, `0021`'s restoration or `0048` §9 — for
the fourth consecutive review.** It **verified the DERIV floor independently** rather than accepting
either arm: `16,655 / 147,370 = 11.301486%`, width `188 / 147,370 = 0.127570 pp`, `188 = 99 + 89`,
Continued ceiling 82.493045%, three DERIV ceilings summing 100.1276%. **It endorses the admissibility
ground and instance A's test** — *would the statistic at any value move the endpoint? If not, it is
commentary.*

**It improved on instance A's "no stopping rule" caveat rather than routing it, and the improvement is
adopted.** The widening rule the arithmetic implements is statable in one line:

> **Concede every pair that was dormant before the instant at which its own state-defining null is
> read** — `τ1` for the never-started null, `τ2` for the Continued null.

**That is exhaustive, not open-ended.** It yields `33,373 − 604 = 32,769` and `19,141 − 189 = 18,952`
with **no residue**, because every pair either was inserting through its test instant or was not. **So
the honest claim is narrower and stronger than "covering with respect to the identified channels":
covering with respect to insertion-dormancy, exhaustively; open only across channel classes (D4, D9).**

## 10. Scope

- **No rule change.** ALT-BROAD stands, silence anchored at `τ1`.
- **No rerun.** Four derived figures, one register row, one stamp, three counting defects, one warrant,
  one blocker recorded.
- **Zero API calls.**
- **Step 8 does not launch.**
