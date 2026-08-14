# Decision 0049 — The joint started-and-left bound is adopted; six record defects corrected; the calibration residual is discharged

| | |
| :--- | :--- |
| **Decision** | **The started-and-left bound is [9.6830%, 10.0405%], width 0.3575 pp, over ALL 703 exclusions.** The 99-only reading is a **labelled conditional sub-interval, never the bound.** **Six record defects corrected.** The **calibration residual is discharged with its limit stated.** The `>=` invariant is **kept with its reason corrected.** The **agent-launch snapshot hazard** is closed. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 7 ALT-BROAD rerun. **Both arms confirmed every figure and both independently refused a bound that would have failed the standing rule** |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 8, 9); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md`. **Not touched, checked not assumed:** `red-team.md`, `second-brain.md`, the five `reviewer-*.md` — none carries liveness spec |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. Both arms confirmed every figure

| | Both arms, `W = 108` |
| :--- | ---: |
| **DERIV** exclusions | **99** from 73 accounts — 0 NS + 99 S&L |
| **APPLY** exclusions | **703** from 216 — **604 NS** (191 accounts) **+ 99 S&L** (73) |
| Per-arm, APPLY, D10 re-derived | 537 / 550 / 633 / 664 / 701 / **703** / 789 / 864 |
| S&L component, APPLY | 52 / 56 / 79 / 89 / 98 / **99** / 125 / 148 |
| Shares, APPLY | 16.7231 / 73.5592 / 9.7177 |
| Movement, APPLY | **−0.2474 / +0.2630 / −0.0156** pp |
| Movement, DERIV | +0.0042 / +0.0554 / −0.0595 pp |
| **Never-started bound** | **[16.6633%, 16.9704%]**, width 0.3071 pp, both endpoints on 196,654 |

Both re-asserted the Step 5 waterfall before any figure, both **cross-checked reused arrays against
source at bit-equality**, both verified the bounds in **integer arithmetic**. Instance A adds that **48
APPLY accounts appear in both components** and reproduces `0047` §5's frozen-D10 figures at their
arms.

## 2. The started-and-left bound: all 703, not the 99

> **[9.6830%, 10.0405%], width 0.3575 pp, both endpoints on 196,654.**

**Why not the 99 alone.** They are the pairs whose *exit* rests on a null — but **the 604 rest on an
untrusted `|A| = 0`, and some of them may in truth have started and left.** A ceiling built on the 99
omits that case and **is not a ceiling on the unconditional estimand.**

**The 99-only interval — [9.6830%, 9.7333%], width 0.0503 pp — is published as a labelled conditional
sub-interval**, conditional on every never-started exclusion being truly never-started. **Never as the
bound. The two differ by a factor of seven.**

**Both arms reached this independently and both refused to adopt it themselves.** Instance A named the
stake exactly: the narrow reading *"would have made this the fourth consecutive bound failing that
exact test."* **The standing rule from `0047` §3 worked before it could be broken a fourth time**, and
it worked in the arms rather than in the ruling.

## 3. Six record defects corrected

| # | Defect | Correction |
| :-- | :--- | :--- |
| **1** | `task-sheet.md`'s **"`τ2` plays no part"** — **false under ALT-BROAD**, since the second conjunct **is** the Continued test, read at `τ2` | Withdrawn. **The rule reads two instants: silence at `τ1`, Continued at `τ2`.** What the line meant, and what survives: **the SILENCE test is anchored at `τ1` and only there** |
| **2** | **`0046` §4's identity phrasing** — *"returning every excluded pair as a decliner reproduces the unfiltered population"* — gives an **unattainable 17.3279%** under ALT-BROAD, because the 99 have `\|A\| ≥ 1` observed and cannot be never-started. **Step 9 reads that sentence** | Corrected. **The identity holds by a different route:** the ceiling returns only the **604** to the never-started count. **The route matters because ALT-BROAD's exclusion set is no longer a subset of never-started** |
| **3** | `task-sheet.md` quoted **ALT's movements under an ALT-BROAD heading**, and called a conditional interval width a share movement | Measured figures substituted; **the superseded ALT and PF-LIMIT figures are named so they are not restated** |
| **4** | **"the exclusion set is empty on DERIV"** — false in **five files** | Corrected in all five. **Decrease is STRICT on both populations at every arm** |
| **5** | `task-sheet.md` carried **ALT's decomposition** `196,654 → 33,373 → 604` | **ALT-BROAD: 196,654 → 52,514 → 703** |
| **6** | **`0048` §5's S&L series was unlabelled APPLY**, and **DERIV gives 147 at `W = 213`, not 148** | Labelled, with the DERIV value stated. **An unlabelled series would have read as a divergence** — the standing rule in its fourth dimension |

## 4. The `>=` invariant is kept, and its reason is corrected

`0047` §6 required `>=` because decrease was **non-strict on DERIV under ALT**, where the exclusion set
was empty. **Under ALT-BROAD decrease is strict on both populations at every arm**, so that reason no
longer applies.

**`>=` is kept anyway, for a better reason: the invariant must not encode a property of one rule.** A
filter position that legitimately removes nothing must not fail an assertion, and Step 13's arms and
Step 8's other positions can produce exactly that.

## 5. The calibration residual is discharged, with its limit stated

**This was `0048` §9's un-actioned item and the last thing standing under the rule's first conjunct**,
which is a comparison between an interpolated instant and `τ1`.

**Confirmed by both arms:** **22.68%** of dated records claim a `watched_at` later than their own
calibrated insertion instant (6,271,584 of 27,656,434), and **5,094** records are clamped above the
range.

**Clamping is inert, and this is a clean discharge.** The clamp value is **2026-08-10T20:48Z**, while
**D10 forces `τ1 ≤ 2026-05-12` at every arm** — so of the **66,961** APPLY pairs on clamped accounts,
**zero are excluded.**

**Stability: sound at the mass, not in the tail.**

- The residual is **bimodal** — median ≈ **0.02 d (~30 min)**, p90 ≈ 0.107 d, **but the upper tail runs
  to 77–125 d** depending on estimator; the two arms differ there, which is itself a property of a
  bimodal distribution rather than a divergence.
- **At the residual covering ~91% of records the exclusion set is stable:** 703 → [701, 703]; at ±7 d,
  [686, 717]. **In the tail it is not:** ±124.6 d gives [414, 1284].
- **Excluded-pair margins are large:** APPLY median `τ1 − max(instant)` ≈ **171–203 days**, with **only
  1 pair inside the residual median** and 17 within a week.
- **Under a direction-only correction, 700 of 703 APPLY and 97 of 99 DERIV exclusions survive, and none
  is created.** A calibration-independent cross-check: **only 3 of 703 excluded pairs' accounts claim
  any `watched_at` after `τ1`.**

**The stated limit, and it is the component this ruling added.** The **S&L component is the fragile
one**: median margin **81.3 days** against **202.5** for the never-started, it spans **19×** under tail
residual against the never-started's 2.5×, and **525 of 703 sit on accounts whose last record is a
`watch`, where the residual is not directly measurable.** **Recorded, not repaired**, and it routes to
Step 14 with the S&L bound.

## 6. The agent-launch snapshot hazard is closed

**Instance A reported that its launched copy of `data-scientist.md` carried superseded ALT text while
the on-disk file was correct.** Nothing ran on stale text — the launch prompt carried the operative
rule verbatim — **but that was luck of drafting, not a control.**

**The mechanism:** an agent's definition is snapshotted when it launches. A file edited and an agent
launched in the same turn can disagree, and **the agent cannot see that it is holding an old copy.**

> **Standing practice, effective now.** Every launch prompt for a spec-bearing step **states the
> operative rule verbatim** and **tells the instance that where its own definition disagrees with
> `decisions/` or the on-disk `task-sheet.md`, the on-disk file wins and the disagreement is a defect
> to report.** The launch prompt, not the definition file, is the authority at launch.

This is the **third** control added to the propagation problem, after item 46's five-file surface and
`0046` §0's population rule. **All three exist because the same failure kept recurring in a new place.**

## 7. Scope

- **No rule change.** One bound adopted, six records corrected, one item discharged, one hazard closed.
- **Zero API calls.**
- **Step 7 goes to Red Team. Step 8 does not launch.**
