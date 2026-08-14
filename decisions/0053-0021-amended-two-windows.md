# Decision 0053 — `0021` is amended for two windows; `0048` §9's gloss withdrawn; nine defects fixed

| | |
| :--- | :--- |
| **Decision** | **`0021` is AMENDED — an amendment to an approved gate, not a clarification.** *"After the window closed"* was written when there was **one** window; there are now two. **The amended reading is per question: an insertion after the window FOR THE QUESTION BEING ASKED proves the account was alive for that question.** **`0048` §9's "insertion after `τ1` ⟹ live" is WITHDRAWN.** Nine defects fixed, two of my stale figures corrected, one limitation added. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Amends** | **`decisions/0021` ruling 2 — gate 2 of 5**; `0048` §9; `0052` §2, §4, §7 |
| **Occasioned by** | The Step 7 ALT-MATCHED rerun. **Both arms confirmed all three of `0052`'s expectations**, and instance A measured a conflict with `0021`'s gloss |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 8, 9, 13, 14); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md`. **Not touched, checked not assumed:** `red-team.md`, `second-brain.md`, the five `reviewer-*.md` |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. `0021` is amended, not glossed

**`0021` ruling 2 reads: *"Any record inserted after the window closed proves the account was alive."***

**It was written when there was ONE window.** "After the window closed" was unambiguous then. **The
Step 1 §7 amendment (`0034`) created two** — never-started read at `τ1`, Continued at `τ2` — and the
ruling has since been read as *"after `τ1`"* **only by accident of when it was written.**

> **The amended reading: an insertion after the window FOR THE QUESTION BEING ASKED proves the account
> was alive for that question.**
>
> - **Never-started is read at `τ1`**, so activity after `τ1` licenses its null.
> - **Started-and-left is read at `τ2`**, so activity after `τ1` but silence from before `τ2` does
>   **not** license it — **the pair could not have produced the evidence the Continued test reads.**

**That is what `0021` meant with one window, and it is what ALT-MATCHED implements.**

**This is recorded as an amendment to an approved gate.** `0021` was approved after four Red Team
rounds; a ruling of that standing is not reinterpreted by a downstream entry's gloss. **`0048` §9's
"insertion after `τ1` ⟹ live" is withdrawn** — a one-window reading carried into a two-window rule.

**The measured stake, from instance A: under ALT-MATCHED 90 APPLY and 89 DERIV exclusions show an
insertion after `τ1` — 47.3% of DERIV's entire exclusion set.** Under the withdrawn gloss every one
would have been forced live. **That count was 0 under ALT-BROAD**, which is why the conflict surfaced
only now.

## 2. The rerun confirmed every expectation

**Both arms, independently, and both stating they confirmed rather than assumed:**

| | `0052` expected | Measured, both arms |
| :--- | ---: | ---: |
| APPLY exclusions | 793 | **793** = 604 NS + **189** S&L, 256 accounts |
| S&L component | 189 | **189** |
| Never-started bound | unchanged | **[16.6633%, 16.9704%]** |
| **DERIV** — recorded as unmeasured | — | **188**, all S&L, 126 accounts |

**The repair worked.** The started-and-left bound is **[9.6372%, 10.0405%]**, and instance B states it
exactly: **the floor "lands on 9.6372% by construction, which is exactly the non-covering endpoint
`0052` §4 identified; it is now covered."**

**ALT-MATCHED closes 90 of 90**, and **instance B confirmed it by index equality, not merely by count** —
the newly-excluded set *is* the channel set. **The residual channel is 0 on both branches by
construction:** the silence instant and the reading instant now coincide, so **there is no ε for the
continuity argument.**

## 3. Nine defects fixed

| # | Defect | Fixed to |
| :-- | :--- | :--- |
| 1 | **`task-sheet.md`: "the silence test is anchored at `τ1` and only at `τ1`"** — false, and instance B is explicit that **an instance following it reproduces 703** | Anchored **per branch**: `τ1` for never-started, `τ2` for started-and-left |
| 2 | **Step 8's "Expect 703 … 604 + 99"** with a mismatch to be treated as a population defect | **793 = 604 + 189**, 256 accounts, and **producing 703 IS a divergence** |
| 3 | Per-arm series carried ALT-BROAD's | **604 / 621 / 713 / 754 / 793 / 793 / 878 / 952** |
| 4 | S&L component series | **119 / 127 / 159 / 179 / 190 / 189 / 214 / 236** — **not monotone, because D10 is re-derived** |
| 5 | Coupling factors | **1.58× total, 1.98× S&L — both FALL** from ALT-BROAD's 1.61× and 2.85× |
| 6 | Frozen-D10 totals | **874 / 990 / 1,192 / 1,466** (746 / 823 / 918 / 1,117 was ALT-BROAD's) |
| 7 | **The S&L component is 189 on APPLY and 188 on DERIV** — under ALT-BROAD both were 99, so unlabelled was safe; **now it is wrong at the adopted arm** | Population labelled at every use |
| 8 | **The `196,654 → 52,514 → 703` funnel does not describe a two-branch rule** | **Branch (i)**: `\|A\| = 0` → 33,373 → **604**. **Branch (ii)**: `\|A\| ≥ 1 ∧ ¬Continued` → 19,141 → **189**. Total **793** |
| 9 | **The clamp-inertness argument does not hold at `τ2`** — **1 excluded pair now sits on a clamped account, up from 0** | Restated; the old form must not be reused |

## 4. Two of my figures corrected, and the ceiling mechanism refined

- **`0052` §4's floor: 9.6373% → 9.6372%.** Numerator 18,952, confirmed by both arms.
- **`0052` §7's population-mismatch figure: 6.2096% → 6.2134%.** The former is ALT-BROAD's. **And the
  mismatch worsened: the DERIV point estimate now lies outside its own bound by 0.0079 pp, nearly
  double ALT-BROAD's 0.0041.**
- **The excess mechanism was too coarse.** *"Counted once in each ceiling"* is wrong. **Each
  never-started exclusion appears in ALL THREE ceiling numerators — excess 2 each — and each
  started-and-left exclusion in TWO — excess 1 each.** So `2 × 604 + 189 = 1,397` pairs = **0.7104 pp**,
  and the three ceilings sum to **100.7104%**. **Continued's ceiling moves 73.6537% → 73.6995%.**

## 5. Two new limitations, both routed to Step 14

**The rule is more correct and more fragile, and both publish together.** Instance B: **the 90 pairs
ALT-MATCHED adds are by construction the ones closest to their own boundary** — margin bounded above by
`H` = 91 days, **median 44.5 days against the 604's 202.5.** **At ±7 days of calibration residual the
started-and-left component moves −6.3% / +14.8%, against −5.1% / +5.1% under ALT-BROAD.**

**D10 admits `τ2 = τ_pull`**, so **20 APPLY pairs have a zero-length post-`τ2` observation window and 2
are excluded by construction** — they cannot show an insertion after `τ2` because there is no time in
which to. Small, structural, reported not repaired. (Instance A.)

## 6. What the run also demonstrated

**The launch-snapshot control worked.** Both arms reported their definition files were snapshotted
before `0052` and **treated the on-disk files as authoritative throughout** — `0049` §6's practice
doing exactly its job.

**The bootstraps are diffable for the first time.** Both **B = 4,000**, account-clustered, both levels
and movements, seeds stated (20260813 and 20260815). Instance B adds the bound-versus-sampling ratios
on the **adopted** bound: NS **27.4%**, S&L **52.7%**, Continued **27.9%**.

**Monotone decrease is strict on both populations at every arm**, and both arms asserted the
commutation of the two branches index-for-index.

## 7. Scope

- **No rule change.** `0021`'s reading is amended to what it meant with one window.
- **Zero API calls.**
- **Step 8 does not launch.**
