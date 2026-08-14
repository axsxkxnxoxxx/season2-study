# Step 7 verification — the DERIV started-and-left floor and Continued ceiling

**Instance `a`.** `specs/step7-deriv-floor-verification.md`. **Zero API calls.**
**Not a gate, not a rerun, not a rule change.** The rule is unchanged: **ALT-BROAD** — a pair is
not live iff **both** the account shows no insertion instant after `τ1` **and** the pair is not
Continued; silence anchored at `τ1` and only at `τ1`. `W = 108`, `H = 91`.

**Every figure below states the population that produced it.**
**APPLY** = Step 5 line 1 less D10 = **196,654** pairs. **DERIV** = Step 5 line 4 less D10 =
**147,370** pairs. Both denominators were read off the masks, not asserted.

---

## 1. Verdict: the proposed DERIV correction is CONFIRMED in every row

| DERIV, n = 147,370 | Proposed | **Mine** | Verdict |
| :--- | ---: | ---: | :--- |
| channel count | 89 | **89** | **CONFIRMED** |
| S&L floor, extreme ALL | 16,655 → 11.3015% | **16,655 → 11.301486%** | **CONFIRMED** |
| S&L floor, extreme NONE | 16,744 → 11.3619% | **16,744 → 11.361878%** | **CONFIRMED** |
| S&L ceiling | 16,843 → 11.4291% *(unchanged between extremes)* | **16,843 → 11.429056%, unchanged** | **CONFIRMED** |
| Continued ceiling, extreme ALL | 121,570 → 82.4930% | **121,570 → 82.493045%** | **CONFIRMED** |

The adopted **DERIV** started-and-left bound is therefore **[11.301486%, 11.429056%]**, width
**0.127570 pp**, floor `16,655 / 147,370`, ceiling `16,843 / 147,370` — matching
`decisions/0055` §1 and the current `task-sheet.md`.

**How this was verified, and why the distinction matters.** Every figure was computed from
instance `a`'s own stored `W = 108` ALT-BROAD masks, `processed/step7/bb_a/masks_W108.npz`, by
`src/step7_df_a_floor_check.py`. **No proposed value appears in that script as an assertion.**
The proposal is loaded as data and compared afterwards, so a mismatch surfaces as a printed
**REFUTED** row rather than as a crash. That was deliberate: the script the proposal itself was
computed with, `src/step7_floor_extremes.py`, carries `assert d["floor_extreme_ALL_continued"]
["count"] == 16655` and four sibling asserts, so it has no path by which it could ever have
reported a refutation. I neither ran it nor took anything from its output. See defect **D-2**.

## 2. Both populations, side by side

| | APPLY | DERIV |
| :--- | ---: | ---: |
| **n (pairs)** | **196,654** | **147,370** |
| Exclusions — total / never-started / started-and-left | 703 / 604 / 99 | 99 / 0 / 99 |
| Excluded accounts | 216 | 73 |
| **Channel pairs** | **90** | **89** |
| Retained (post-liveness) started-and-left | 19,042 | 16,744 |
| **S&L floor, extreme NONE Continued** | 19,042 → 9.682997% | 16,744 → 11.361878% |
| **S&L floor, extreme ALL Continued — ADOPTED** | **18,952 → 9.637231%** | **16,655 → 11.301486%** |
| **Floor movement between extremes** | **0.045766 pp** | **0.060392 pp** |
| **S&L ceiling** *(does not move)* | 19,745 → 10.040477% | 16,843 → 11.429056% |
| **Bound width** | **0.403246 pp** | **0.127570 pp** |
| **Continued ceiling, extreme NONE** | 144,843 → 73.653727% | 121,481 → 82.432653% |
| **Continued ceiling, extreme ALL — ADOPTED** | **144,933 → 73.699493%** | **121,570 → 82.493045%** |
| Never-started bound | [16.663277%, 16.970415%] | **[6.205469%, 6.205469%] — degenerate** |

**The APPLY width is 0.403246 pp → 0.4032 pp**, confirming `0055` §5's correction of `0054` §7's
0.4033 (a rounding artifact). `19,745 − 18,952 = 793`; `793 / 196,654 = 0.403246%`.

**The three ceilings, and they still cannot all hold.**

| | APPLY, n = 196,654 | DERIV, n = 147,370 |
| :--- | ---: | ---: |
| Never-started ceiling | 33,373 → 16.970415% | 9,145 → 6.205469% |
| Started-and-left ceiling | 19,745 → 10.040477% | 16,843 → 11.429056% |
| Continued ceiling | 144,933 → 73.699493% | 121,570 → 82.493045% |
| **Sum** | **100.710385%** | **100.127570%** |
| Excess pairs | **1,397** = 2×604 + 99 + 90 | **188** = 2×0 + 99 + 89 |

Both excesses reproduce exactly. **`2 × 604 + 189 = 1,397 → 0.7104 pp` on APPLY**, as the record
states. The **DERIV** analogue, which the record does not currently state anywhere, is
**`99 + 89 = 188 → 0.1276 pp`** — and it is numerically equal to the DERIV bound width, because
with no never-started exclusions each of the 188 pairs is double-counted exactly once.
They remain **alternative worst cases over one set, not simultaneous ones.**

## 3. Checks the confirmation rests on

**The rule and the states were rebuilt from primitives, not trusted.** All pass:
the three states partition the rows; `never ≡ |A| = 0`; `left ≡ ¬Continued ∧ |A| ≥ 1`;
`no_after ≡ last_inst ≤ τ1`; the rebuilt rule `(¬Continued) ∧ (last_inst ≤ τ1)` is **identical**
to the stored exclusion mask; the exclusion components partition the exclusions; no Continued
pair is excluded; `τ2 > τ1` on every row.

**The one primitive the channel count actually turns on was recomputed from source.**
`src/step7_df_a_instant_recheck.py` re-derives the per-account last insertion instant from
`processed/step5/full_scan.npz` (27,656,813 records, 2,549 accounts) against the **stored** Step 5
calibration — read, never refitted (`0029`). **Max absolute difference against the stored column:
0.0 seconds**, and the channel counts and exclusion counts are unchanged on both populations
(APPLY 90 / 703; DERIV 89 / 99). This is not a rerun: it re-derives one column, so that the
confirmed channel count does not rest on a stored intermediate being correct.

**Scope limit, stated rather than glossed.** What I verified is the arithmetic and the predicate
logic on instance `a`'s masks, plus that one primitive. **I did not rebuild the Step 1 outcome
assignment**, which is what `cont`, `never` and `t0f` come from; rebuilding it would be a rerun
and none was ordered. If the outcome masks are wrong, this verification would not see it.

## 4. Question 1 — does the endpoint move between the extremes?

**Yes, on both populations, so the choice is not numerically empty.**

- **APPLY, n = 196,654: the started-and-left floor moves 0.045766 pp** (19,042 → 18,952).
- **DERIV, n = 147,370: it moves 0.060392 pp** (16,744 → 16,655). **The movement is larger on
  DERIV** — one fewer channel pair over a denominator 25% smaller.
- **The started-and-left ceiling does not move at all — 0.000000 pp on both populations.** The
  widening is strictly one-sided, exactly as `0054` §3 and `0055` §2 state, because the channel
  pairs are already counted as started-and-left in the ceiling.
- **The Continued ceiling moves in lockstep with the floor**, by the same 0.045766 pp on APPLY
  and 0.060392 pp on DERIV, in the opposite direction.

So the choice is consequential for **two** of the four endpoints and empty for the other two.
On DERIV the uncorrected floor sat **0.060392 pp above** the case the filter exists to guard
against, and the uncorrected Continued ceiling **0.060392 pp below** it.

## 5. Question 2 — is the widened floor the right endpoint, and does any margin statistic belong?

### 5.1 The widened floor is the right endpoint

**Yes, on the ground stated, and the ground is sufficient without any supplement.**

A bound of this kind reports an **identified set**: the range of values of the estimand consistent
with what the data can and cannot show. Its endpoints are therefore fixed by **admissibility** —
which resolutions the evidence fails to rule out — and by nothing else.

The channel pairs are exactly the pairs for which the evidence fails to rule out Continued. They
are `¬Continued`, `|A| ≥ 1`, and their account fell silent at some instant `s ∈ (τ1, τ2]`. The
Continued test reads distinct S2 episodes with `watched_at < τ2`. A record inserted at `s` can
carry any `watched_at ≤ s` and `0021` Adoption 3 retains post-dated records — so the channel pair
**could** have produced evidence dated `≤ s`, and did not. What it **could not** have produced is
evidence dated in `(s, τ2)`, because there was no insertion after `s` to carry it. That window is
unobserved. A pair scored started-and-left on an unobserved window **may in truth be Continued**,
and a floor on the started-and-left share is a worst case, so it must concede them. It does:
`16,744 − 89 = 16,655` on **DERIV**, `19,042 − 90 = 18,952` on **APPLY**.

**`0052` §4's refusal is backwards, and worth restating in the form that shows why.** It declined
to widen because that "would have been the fifth consecutive bound with a non-covering endpoint."
A bound is non-covering when its floor is **too high** — when it excludes an admissible
resolution. Widening lowers the floor. Widening is the repair, and refusing it on the ground that
too many endpoints have failed to cover is refusing the fix because the bug recurs.

### 5.2 No margin statistic belongs in an endpoint's justification. I would exclude the class

**My position, and I hold it generally, not just for these 89 pairs.**

**First, it is a category error.** Admissibility is binary; a margin is continuous. There is no
value of the residual window at which an admissible resolution becomes inadmissible, so no margin
statistic can ever discharge the question an endpoint asks. The Continued condition is
`F2 ∈ A_H ∧ |A_H| ≥ ceil(0.90 × L2)` on **distinct** episodes — a condition a single binge
satisfies in hours. At a residual margin of 0.13 days it is still satisfiable. The set of margins
at which the concession becomes unnecessary is **empty**, not merely small. A statistic whose
every possible value yields the same answer is not evidence for that answer.

**Second, admitting the class admits the selection, and the selection already happened here.**
`0054` §3 quoted p5 = 1.7 days and a minimum of 0.13. `0055` §2 found the median for the same 90
pairs is 44.5 days. **Both are true statistics of one set, and they point opposite ways.** Once a
justification may cite a margin, the author chooses which one, and the choice was made in the
direction of the conclusion already reached. This is not a hypothetical bias — it is one
occurrence, caught once, in this chain. The only rule that survives contact with that is a rule
that admits none of them, because a rule requiring "both tails" merely relocates the discretion to
which tails.

**Third, the loss is asymmetric.** A margin-tightened floor buys **0.0604 pp** on DERIV and
**0.0458 pp** on APPLY. What it spends is the study's central claim — that the judgment calls are
honest and inspectable, which is the argument Step 16's interactive option exists to make. Trading
credibility for 0.06 pp is a bad trade at any exchange rate, and it is a worse trade in a chain
where an endpoint has now failed to cover **six consecutive times**.

**Where margin statistics do belong — I am not arguing they are worthless.** They belong in the
**limitations and sensitivity** narrative, as a description of *how informative* the bound is:
"the width is driven by 89 pairs, half of which have roughly half the Continued window
unobserved" is a true and useful sentence, and the correct place for the median 44.5. That is a
claim about the data's resolving power, not about where an endpoint sits. **The test is: would the
statistic, at any value, change the endpoint? If no, it is commentary — publish it beside the
bound, never inside its justification.** Both p5 = 1.7 and median = 44.5 fail that test as
justification and pass it as commentary.

**One consequence I should name rather than leave implicit.** Pure admissibility has no natural
stopping point: bounds widen monotonically as further admissible channels are identified, and
nothing in the current record says when the search is complete. This channel was found because
someone thought to look for it. **So the honest claim is that the bound is covering with respect
to the identified channels, not covering full stop** — which is also why the task sheet is right
to require the **D4 S3-without-S2** and **D9 split-artifact** bounds to be published *alongside*
the liveness bound rather than folded into it. I recommend that wording be attached wherever the
bound is published. Routing this to Step 14 rather than acting on it.

---

## 6. Defects found. **None fixed** — reported only, per the spec

**D-1 — SEVERE. My own operative deliverable, `artifacts/step7-liveness-bb-a.md`, still publishes
the superseded non-covering endpoints on BOTH populations, and carries no stamp.**
It prints, unqualified: the APPLY floor **19,042 → 9.6830%** and width **0.3575 pp** (lines 181,
183), the **DERIV** bound **[11.3619%, 11.4291%]** at width **0.0672 pp** (line 185), the APPLY
floor again at line 203, and the Continued ceilings **APPLY [73.2962%, 73.6537%], DERIV
[82.3655%, 82.4327%]** (line 206) — ***all SUPERSEDED; the adopted ceilings are 73.6995% and
82.4930% (`0054`, `0055`)***. **The string `0055` does not appear anywhere in the file.**
***Actioned `0059`: `bb-{a,b}` are stamped, their derived figures are regenerated from the counts
by `src/step7_regenerate_derived.py`, and `src/check_surfaces.py` now checks the operative pair
value by value rather than exempting it on a stamp.***
`0055`'s own header lists `artifacts/` as one of seven propagated surfaces and §5a states the
artifacts would be *"stamped, not rewritten."* **The stamp did not land on this file.** `bb` is the
pair named for the adopted rule, which is exactly the file a reader would trust. Two of the
figures — 9.6830% and 11.3619% — are floors above the case the filter exists to guard against, and
73.6537% is the pre-widening Continued ceiling that `0055` propagation **#16** was written to
correct in the agent definitions. `task-sheet.md` and both `data-scientist` definition files are
**correct**; the defect is confined to the artifact. **I did not edit it.**

**D-2 — The proposal's own computation had no refutation path, and was single-instance.**
`src/step7_floor_extremes.py` reads `processed/step7/bb_a/masks_W108.npz` — **instance `a`'s masks
only**. So `0054` §3's table, introduced as *"Measured, because the alternative was that the choice
is numerically empty"*, and `0055` §2's identical table, are **one instance's measurement presented
inside a dual-implementation step**. Separately, lines 72–78 hardcode the conclusions as
`assert`s, so the script could only ever crash, never report a divergence. Both facts argue that
`0055` §1 was right to order this verification; I record them so the record does not later read
that table as having been dually produced. Confirming the numbers does not retroactively make that
table dual — this deliverable and its counterpart do.

**D-3 — The verification spec defines the channel window two different ways.**
`specs/step7-deriv-floor-verification.md` says **`(τ1, τ2]`** in "What to compute" item 1 and
*"inside `(τ1, τ2)`"* in Background; `task-sheet.md` line 350 and both `data-scientist` files use
**`(τ1, τ2)`**. **Immaterial at `W = 108`: zero pairs have a last insertion instant exactly at
`τ2` on either population**, so both readings give 90 on APPLY and 89 on DERIV, and I verified
this rather than assuming it. But it is an unresolved ambiguity in a load-bearing predicate, in
the same chain that has twice been bitten by half-open boundary drift (D13, `0034`). It should be
fixed to one form. **Not fixed here.**

**D-4 — no disagreement found between my snapshotted definition and the on-disk authorities.**
Checked as instructed. `task-sheet.md`, `CLAUDE.md` and `decisions/` agree with my snapshotted
`data-scientist.md` on every figure this task touches, and the on-disk `data-scientist.md` carries
`0055` §1's supersession notice at lines 105–106 exactly as snapshotted. Nothing to report.

**Disclosure.** My defect sweep was a repo-wide grep for the superseded strings and it incidentally
surfaced two lines of `artifacts/step7-liveness-bb-b.md`. I did not open that file, did not read
`processed/step7/bb_b` or `mm_b`, and **no figure from any `b` artifact entered any computation
here** — every number in this document derives from `processed/step7/bb_a/masks_W108.npz`,
`processed/step5/full_scan.npz` and `processed/step5/calibration.npz`.

---

## 7. Files

| Path | Contents |
| :--- | :--- |
| `artifacts/step7-deriv-floor-check-a.md` | this document |
| `artifacts/step7-deriv-floor-check-a.json` | every figure above, machine-readable |
| `processed/step7/df_a/floor_check.json` | full working output, both populations |
| `processed/step7/df_a/instant_recheck.json` | independent last-insertion recomputation |
| `src/step7_df_a_floor_check.py` | the verification; no proposed value asserted |
| `src/step7_df_a_instant_recheck.py` | last-insertion re-derivation from Step 5 source |
| `src/step7_df_a_emit.py` | JSON emitter, so no figure is retyped |

**Zero API calls in all three scripts.** Aggregates and counts only; no usernames, user IDs or
individual histories appear in this file or its JSON.
