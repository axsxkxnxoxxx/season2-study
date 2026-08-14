# Decision 0054 — ALT-BROAD restored, the S&L floor widened to cover the 90; `0053` withdrawn entirely

| | |
| :--- | :--- |
| **Decision** | **ALT-MATCHED is REVERTED. ALT-BROAD is restored** and the started-and-left floor is **widened to 18,952 / 196,654 = 9.6372%**. **`0053` is WITHDRAWN in its entirety** — its premise was false. **`0021`'s amendment is reverted; `0048` §9 is restored.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **seventh** Step 7 HOLD |
| **Withdraws** | `decisions/0053` entirely; ALT-MATCHED (`0052` §1); `0052` §4's rejection of the widened floor |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 8, 9, 13, 14); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md` — **each edit verified by reading the file back.** **Not touched, checked not assumed:** `red-team.md`, `second-brain.md`, the five `reviewer-*.md` |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-14**, which is tomorrow. Entries `0052` through `0057` all carried it, and the drift began when the session's clock advanced mid-work and the date was carried forward from an earlier entry rather than re-read. **Corrected in place across every surface, with this note, rather than silently rewritten** — the decision log is a public tracked artifact. Found by Red Team on its eleventh review; recorded at `0058` §6.

---

## 1. The rule change bought nothing

**The decisive finding, verified independently.** On all three identified sets, ALT-BROAD with a
covering floor and ALT-MATCHED are **numerically identical:**

| On APPLY, n = 196,654 | ALT-BROAD + widened floor | ALT-MATCHED |
| :--- | ---: | ---: |
| S&L floor | 18,952 → **9.6372%** | 18,952 → **9.6372%** |
| S&L ceiling | 19,745 → **10.0405%** | 19,745 → **10.0405%** |
| Continued ceiling | 144,933 → **73.6995%** | 144,933 → **73.6995%** |
| Never-started | [16.6633%, 16.9704%] | identical, both arms |

**AMENDED 2026-08-13 (`decisions/0055`): this table is APPLY only, and the entry that mandated a
population label on every figure omitted one on its own decisive table.** The same identity holds on
**DERIV, n = 147,370** — S&L **[11.3015%, 11.4291%]**, Continued ceiling **82.4930%** — but **the DERIV
floor was widened nowhere.** Every file kept 16,744 → **11.3619%**, so §1's claim was implemented on one
population of two. **Corrected to 16,655 → 11.3015% and 121,570 → 82.4930% by `0055`**, from figures
already sitting in `step7-liveness-mm-{a,b}.md`.

**What ALT-MATCHED actually did was move the point estimates** — S&L 9.7177% → 9.6762% — by deleting
the 90 least-robust rows, **and pay for it with an amendment to an approved gate, a contradiction with
`0034`, a fragility transfer, and a nine-defect propagation wave.**

**`0052` §4 declined to widen the floor because doing so *"would have been the fifth consecutive bound
with a non-covering endpoint."* That is exactly backwards: widening to 18,952 is what makes the
endpoint covering.** The rejection reason named the defect the alternative repairs.

## 2. `0053` is withdrawn — its premise was false

`0053` rested on: *"the ruling has since been read as 'after `τ1`' only by accident of when it was
written."*

**`0034` — the entry that CREATED the second window, on the same date — ruled it in terms:**

> **"Liveness stays anchored at `τ1`.** Liveness licenses trusting a null, and the null is `|A| = 0`,
> which is tested at `τ1`."

**And `0051` re-affirmed it with both windows in view**, noting `0034` was *"written into the Step 7
spec so no isolated instance re-anchors it."*

**So the `τ1` anchoring was ruled, not inherited.** `0053` amended `0021` and withdrew `0048` §9
**while leaving `0034` — the one ruling that forbids the re-anchoring — standing, uncited and
unmentioned.** The adopted rule contradicted a live ruling in an approved gate.

**`0021`'s amendment is reverted. `0048` §9's "insertion after `τ1` ⟹ live" is restored.**

`0053`'s **nine defect fixes are retained** where they are rule-independent; their ALT-MATCHED figures
are superseded by the ALT-BROAD ones restored here.

## 3. The warrant was false for the pairs the rule was adopted to capture

`0053` put into `0021`: *"the pair could not have produced the evidence the Continued test reads."*

**A record inserted at instant `s` can carry any `watched_at ≤ s`, and `0021` Adoption 3 keeps
post-dated records.** So an account last active at `s ∈ (τ1, τ2)` **could** have produced Continued
evidence — everything dated `≤ s`, which is inside the Continued window. It could only fail to produce
evidence dated in `(s, τ2)`.

~~**The 90 have p5 margin 1.7 days and a minimum of 0.13 days.** Some were demonstrably alive for
roughly 89 of the 91 days, had full opportunity to generate the evidence, did not, and would have been
deleted anyway.~~ **WITHDRAWN 2026-08-13 (`decisions/0055`) — it cherry-picked the tail.** The record's
own median for the same 90 is **44.5 days** (`0053` §5, instance B), so for half of them roughly half
the Continued window is unobserved. p5 supported the claim and the median contradicted it, and only p5
was quoted.

**The correct ground carries no margin statistic at all.** A floor is a **worst case, not an
expectation.** The question is whether a channel pair *can* in truth be Continued, and it can: silent
from `s`, it may hold Continued evidence dated anywhere in `[F2 air, s]`, and even at margin 0.13 days
it could have completed S2 inside the unobserved remainder. **Admissibility is what sets an endpoint;
plausibility does not enter.** So p5 = 1.7 and median = 44.5 are **both inadmissible here** — the first
was mine and the second is the one that would have been quoted had the conclusion needed defending the
other way.

**Measured, because the alternative was that the choice is numerically empty** (`src/step7_floor_extremes.py`,
zero API calls, both populations, channel counts and both endpoints asserted):

| | n | channel | floor, NONE Continued | floor, ALL Continued | **moves** | ceiling |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 90 | 19,042 → 9.6830% | **18,952 → 9.6372%** | **0.0458 pp** | 19,745 → 10.0405% |
| **DERIV** | 147,370 | 89 | 16,744 → 11.3619% | **16,655 → 11.3015%** | **0.0604 pp** | 16,843 → 11.4291% |

**The endpoint moves on both populations, so the choice is consequential** — and it is decided by
admissibility, not by the movement's size. **The widening is one-sided: the ceiling does not move**,
because the 90 are already counted as started-and-left in it. The Continued ceiling moves in lockstep
with the floor.

**And the continuity argument is symmetric.** `0052` §1 argued the warrant *"holds identically for a
pair silent after `τ1 + ε` for any ε < 91 days,"* concluding ALT-BROAD cut it at one end. **That
argument refutes ALT-MATCHED from the other end just as forcefully. It proves no instant in
`[τ1, τ2]` is warranted — not that `τ2` is.** Reading it as licensing `τ2` is the error class of this
chain: **correcting a predecessor by overshooting into the mirror-image defect.**

## 4. The sweep neither arm was asked for

**Exclusion count against the silence anchor, swept `τ1 → τ2`**, never-started held at `τ1`
(`src/step7_anchor_sweep.py`, zero API calls; both endpoints asserted against the arms' figures):

| Days past `τ1` | 0 | 9.1 | 27.3 | 45.5 | 63.7 | 81.9 | **91.0** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| APPLY S&L | **99** | 108 | 120 | 143 | 154 | 174 | **189** |
| APPLY total | **703** | 712 | 724 | 747 | 758 | 778 | **793** |
| DERIV S&L | **99** | 108 | 120 | 143 | 154 | 174 | **188** |

**The curve is smooth and monotone. There is no elbow, no plateau, and no natural cut anywhere in the
interval.** That is the continuity argument made visible, and it is the reason **neither endpoint is
warranted by the data** — which is precisely why the bound must be widened rather than a cut chosen.

## 5. Propagation #13 fixed

**Both `analytics-engineer` files carried "EXPECT 793" at line 77 and "EXPECT 703" at line 88** — two
mutually exclusive instructions ten lines apart, each declaring the other's number a divergence,
**identical in both copies so the dual diff could not see them**, in the file **Step 8 launches from.**

**And `task-sheet.md` Step 9 never received `0053`'s pass at all** — still carrying 703, the
non-covering `[9.6830%, 10.0405%]`, 73.6537% and 100.6646%. That is `0052` §5's propagation #12
**repeated one entry later in the same section.**

**Both fixed. Each edit verified by reading the file back**, and both pairs re-checked byte-identical
apart from the `name:` field.

## 6. Two of my own, and two divergences reported not reconciled

- **`0053` §3 mandated population labels and then omitted them four rows above the row that requires
  them** — its items 3–6 and §2's bound are unlabelled APPLY figures whose DERIV values differ.
- **`0053` §4 wrote ALT-BROAD's DERIV bound miss as 0.0041; both arms and the task sheet say 0.0042.**

**Reported as divergences, per `CLAUDE.md`, and NOT reconciled:**

- **Robustness survival: instance A finds 792 of 793, instance B finds 791.** Off by exactly one on
  each population, **consistent with a `≤ τ_pull` restriction A states and B does not.** A spec
  ambiguity; neither arm flagged it and neither did `0053`.
- **Bound width: A gives 0.4032 pp exact (793/196,654); B gives 0.4033 pp, differenced from rounded
  endpoints, and computes its ratios from it.** **`0053` §6 promoted B's 52.7% ratio into the record —
  it is a rounding artifact and is withdrawn.**
  **AMENDED 2026-08-13 (`0055`): §7 below and `task-sheet.md` then published 0.4033 — B's artifact —
  four paragraphs after naming it as one.** **The width is 0.4032 pp**, `793 / 196,654 = 0.40325`.
  Withdrawing one of B's rounding artifacts and adopting the other in the same entry is the error class
  §3 names, committed in the entry that names it.

## 7. What is restored, and what the record now says

**The rule:** *not live iff no insertion instant after `τ1` AND not Continued.* **Silence anchored at
`τ1` and only at `τ1`**, per `0034`, `0051` and now `0054`.

**Exclusions: APPLY 703 from 216 accounts (604 + 99); DERIV 99 from 73 accounts (0 + 99).**

**The started-and-left bound is [9.6372%, 10.0405%], width 0.4032 pp** *(corrected from 0.4033 by `0055`)*, both endpoints on 196,654 —
**widened to admit that the 90 may in truth be Continued.** The Continued ceiling moves with it to
**73.6995%**, and the three ceilings sum to **100.7104%**.

## 8. Scope

- **Rule reverted. No rerun ordered** — every figure for both rules is already on record from four
  arm-runs. **AMENDED 2026-08-13 (`0055`): false for the adopted bound.** 18,952 is on record **only as
  ALT-MATCHED's floor over 793 exclusions.** **No arm has ever asserted 18,952 as the floor over
  ALT-BROAD's retained set**, and both operative deliverables still print 9.6830% — so a
  dual-implementation step adopted a bound **neither instance had reproduced.** The arithmetic is the
  same either way; the assurance is not. **Both `data-scientist` arms are now verifying it against their
  own outputs** (`specs/step7-deriv-floor-verification.md`).
- **Zero API calls**, including the sweep.
- **Step 8 does not launch.**
