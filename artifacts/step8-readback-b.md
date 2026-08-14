# Step 8 — read-back (instance `b`)

**This is not Step 8.** Step 8 is a gate, it is unapproved, and it has not launched. **Nothing was
built, no row was filtered, nothing was written to `processed/`, zero API calls.** What follows is the
specification *as I read it*, plus what I could not read unambiguously.

**Sources read:** `specs/step8-readback.md`; `task-sheet.md` Steps 0–13; `CLAUDE.md`; my own definition
file `.claude/agents/analytics-engineer-b.md`; `artifacts/step1-outcome-definition.md`;
`artifacts/step1-amendment-continued-boundary.md` (§5.2, §5.3, §4.2 context);
`artifacts/step5-contamination-diagnostics.md`; `artifacts/step7-gate-approval.md`;
`decisions/0004, 0011, 0017, 0021, 0026, 0027, 0029, 0033, 0034, 0042, 0047, 0048, 0054, 0062, 0064,
0066`. Read-only count checks against `processed/step2/frame.csv`, `processed/step5/pair_revision5.csv`,
`processed/step5/pair_adopted.csv`, `processed/step5/adopted_rule.json`, `raw/step3/user_pool.jsonl` —
listed in §8 with what each returned.

**Populations named throughout.** `APPLY` = 196,654 (Step 5 line 1 less D10, at `W = 108`).
`DERIV` = 147,370 (Step 5 line 4 less D10, at `W = 108`). They are different populations with different
`n` and I state which one every figure below sits on.

---

## 1. The filter order, as I would apply it

Seven positions, exactly as `decisions/0029` fixes them and `task-sheet.md` Step 8 restates them. The
final row set commutes; the per-position sample sizes do not, which is the whole reason the order is
mandated.

| # | Filter | Applied to | Removes | Count on this data |
| :-- | :--- | :--- | :--- | ---: |
| 1 | **Step 2 frame** | the raw user-show pair universe (**undefined — see §4, F8**) | pairs on shows not in the 1,138-show frame | **unknown** |
| 2 | **`L2 = 1` exclusion** | position-1 output | pairs on shows whose S2 has one listed episode | **0 pairs, 0 shows** (verified: 0 of 1,138 frame shows have `L2 = 1`) |
| 3 | **S1 completion rule** | position-2 output | pairs failing `F1 ∈ D1` **and** `\|D1\| ≥ ceil(0.90 × L1)` | leaves **220,107** (matches Step 5 §1's "S1-completer pairs in the frame") |
| 4 | **Contamination exclusion (Step 5)** | position-3 output | the two adopted exclusions only: S2 evidence **entirely** air-date-stamped (16,665) and contaminated `T0` with **no** S2 evidence (1,542) | 220,107 − 18,207 = **201,900** (reproduced) |
| 5 | **Right-censoring** | position-4 output | pairs failing `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, `H = 91`, `τ_pull = 2026-08-11T00:00:00Z` | at `W = 108`: 201,900 − 5,246 = **196,654 = APPLY** (reproduced exactly) |
| 6 | **Liveness** | position-5 output = **APPLY, 196,654** | pairs that are NOT LIVE | **expect 703** (604 never-started + 99 started-and-left, from 216 accounts) → **195,951** |
| 7 | **Outcome assignment** | position-6 output, 195,951 | **nothing — it is an annotation, not a filter** | 195,951 |

**Position 4 is narrower than it sounds.** "Contamination exclusion (Step 5)" is the *adopted rule*
(`decisions/0021`): two disjoint exclusions, tag-only for everything else. It is **not** the Step 5
waterfall down to 128,099 — that is Step 6's estimation sample and lines 2–5 of it are `has_s2`,
`T0 not contaminated`, `completing record not post-dated`, `first S2 watch clean`, none of which is a
position-4 filter. 3,296 post-dated pairs and 23,067 contaminated-`T0`-with-S2 pairs **stay in**.

**Position 5 before position 6** is the one genuine ordering choice (`0029`): censoring is objective —
a property of the clock and `pull_date` — so running it first means liveness's marginal cost is measured
on a fully observable population, which is the number Step 9's bound needs. Contamination before
censoring is required so an import-stamped S1 completion date is counted as contamination rather than
laundered into a censoring drop.

### Where liveness sits and what it operates on

- **Position 6, on the position-5 output — APPLY, n = 196,654** at `W = 108`. Not on DERIV. DERIV is
  Step 7's derivation population and is never a Step 8 filter position.
- **The rule** (`0048`, restored `0054`, approved `0064`): *a pair is NOT LIVE **iff both** the account
  shows no insertion instant after that pair's `τ1 = ⟦T0⟧ + W × 24h`, **and** the pair is NOT Continued.*
  Otherwise live.
- **Silence is anchored at `τ1` and only at `τ1`.** No pre-`τ1` requirement in any form — withdrawn
  twice (`0040` §1, `0042` §3).
- **It is pair-level.** Evidence is account-wide — the whole sweep, other shows and movies included —
  but the test is clock-start-relative and `T0` is pair-specific. One account can be live for one show
  and not for another. **No user is ever dropped wholesale.**
- **It runs on record INSERTION time, not claimed `watched_at`** (`0021`), via the **stored** play-`id`
  isotonic calibration at `processed/step5/calibration.npz`, which **is never refitted**.
- **It is outcome-conditional, and the spec says so.** Conjunct 2 *is* the Continued test, read at
  `τ2 = ⟦T0⟧ + (W + H) × 24h` on `A_H`. So position 6 evaluates a position-7 predicate. That is
  permitted because both are row-local predicates on the position-5 output and commute exactly, and
  `0029`'s ordering rationale is about per-filter sample size, which cannot reach position 7 because
  outcome assignment removes no rows. **Waterfall line 6 must be reported as outcome-conditional.**
  Its measured size, from `0063`/`0064`: dropping conjunct 2 (= PF-LIMIT) would exclude **652** pairs
  that are Continued on evidence they demonstrably produced, on both populations.
- **Expected exclusions at `W = 108`, APPLY: 703 = 604 + 99, from 216 accounts.** **604 is the
  superseded ALT answer; 793 is the withdrawn ALT-MATCHED answer.** Any other number is a **population**
  defect before an implementation one — Step 7 measured 703 on APPLY built from the Step 5 pair table,
  not through positions 1–5, so a mismatch most likely means the frame join, the `L2 = 1` exclusion or
  the censoring differs. (I reproduced the position-5 population exactly, so that particular risk is
  smaller than the spec assumes — see §8.)

### Position 7, stated exactly

**Two instants** (`0034`). Let `A` = distinct S2 episodes with `number ∈ E2` and `watched_at < τ1`;
`A_H` = the same set recomputed at `τ2`; `τ2 = ⟦T0⟧ + (108 + 91) × 24h = ⟦T0⟧ + 199 days`.

| State | Condition |
| :--- | :--- |
| Never started | `\|A\| = 0` |
| Continued | `\|A\| ≥ 1` **and** `F2 ∈ A_H` **and** `\|A_H\| ≥ ceil(0.90 × L2)` |
| Started and left | `\|A\| ≥ 1` **and not** the Continued condition |

`|A| ≥ 1` at `τ1` **remains a conjunct of Continued** — dropping it puts a day-150 starter completing by
day 190 in two states at once. Never-started is a 108-day statement, Continued a 199-day statement, and
the two must never be described as measured alike. Every boundary test is the half-open UTC-instant form
of Step 1 §2.4; `date(watched_at) <= T1` appears nowhere.

---

## 2. Required counts, where each goes, and on which population

`artifacts/` gets counts and aggregates only; the table itself goes to `processed/`. **The population
column is where the findings are: the spec names one in three cases out of fourteen.**

| # | Required output | Destination | Population the spec states |
| :-- | :--- | :--- | :--- |
| 1 | Filter waterfall — sample size after **each** of the 7 positions | `artifacts/` | implied per position; **unit not stated** (pairs? also users, shows? position 2 is explicitly shows **and** pairs) |
| 2 | Drop count **per show**: dropped episode records and distinct dropped `(season, number)` pairs | `artifacts/` | **not stated** |
| 3 | Drop count **per outcome**: pairs whose entire S2 evidence was dropped, as a share of Never started | `artifacts/` | denominator named ("Never started"); the position it is read at is **not stated** |
| 4 | **D2** negative-lag report, split by which `max()` term binds | `artifacts/` | **not stated**; and the split is binary while the data has a third case (§4, F9) |
| 5 | **D3′** resumption: of pairs Started-and-left **at `τ2`** with `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull` — the share completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, its **share of all Started-and-left**, **per `W` arm** | `artifacts/` | subpopulation defined by the clearance; base population **not stated** |
| 6 | Alongside D3′, **labelled a count not a rate**: the **3,440** Started-and-left pairs completing at any point before `τ_pull`, with its exposure-weighting by show recency stated at the point of use | `artifacts/` | **stated nowhere, and it is not APPLY** — see §4, F5 |
| 7 | **D8** never-started post-window diagnostic, (i) any distinct S2 episode in `[τ1, τ1 + H)` and (ii) satisfying the Continued condition over that horizon; measured over `H`, **not to the pull date** | `artifacts/` | "pairs scored Never started at `τ1`" — position not stated (pre- or post-liveness) |
| 8 | **D9** split-artifact counts, **both halves**: the fabricated never-started row, and the silently deleted S1-failing counterpart | `artifacts/` | half (b) is a count over rows removed at **position 3**, so it is not on any retained population |
| 9 | **Right-censoring removal as TWO lines** — the `max(W, 91)` term and the **incremental** `+ H` term — each with its upward direction named | `artifacts/` | position-4 output, 201,900, implied by the order |
| 10 | **Retained-pair counts PER AIR PERIOD after right-censoring, for every `W` arm** (`0033`) | `artifacts/` | position-4 output implied by the order — **but the spec's own expected values are on position 3**; §4, F4 |
| 11 | `pull_date`; earliest and latest per-user fetch dates; count of records discarded for `watched_at >= τ_pull` | `artifacts/` | record-level, whole pull |
| 12 | Per-bucket show and pair counts for **all five** D12 buckets, plus shows within 1 day of a bucket boundary | `artifacts/` | frame-level (1,138 shows) and pair-level, position unstated |
| 13 | Metadata-disagreement counts, incl. the subset where `aired_episodes < \|E\|` for S2, with the direction named | `artifacts/` | frame-level |
| 14 | Invariant report (all results) | `artifacts/` | per invariant |
| 15 | The analysis table itself: one row per user-show pair, carrying outcome state, abandonment point, discovery channel, all Step 2 show fields, and **`action` retained as a column** | `processed/` | position-7 output |

**Three of these are structurally zero or near-zero on this frame and must publish their coverage, not
just a `0`** — `CLAUDE.md` is explicit that an empty result and a clean result are the same value and
only the control knows which it produced:

- **line 2 of the waterfall:** 0 pairs, 0 shows (0 of 1,138 shows have `L2 = 1`);
- **item 13:** all four disagreement flags are `False` for all 1,138 frame shows, including
  `aired_episodes < |E|` for S2 — so "0" here means "0 out of 1,138 examined";
- **item 12's C0 bucket:** 0 shows (C1 206 / C2 340 / C3 167 / C4 425), and 7 shows sit within 1 day of
  a boundary.

---

## 3. The invariants, and what would have to be true for each to fail

There are six. **Not one of them can fail on data alone.** Every one is a check on the implementation;
Step 1 §3.2 says this in as many words for two of them, and the spec labels two as code checks. I state
it for all six because it changes what a passing report means — a clean invariant report is evidence
about the code, and evidence about nothing else.

| Invariant | Fails only if… | Can it fail on data? |
| :--- | :--- | :--- |
| **Outcome states are mutually exclusive and sum to the sample** | the implementation does not evaluate the partition `A = ∅` / `(A ≠ ∅ ∧ C_H)` / `(A ≠ ∅ ∧ ¬C_H)`; e.g. it drops the `\|A\| ≥ 1` conjunct from Continued, which puts a day-150 starter completing by day 190 in two states | **No.** Exhaustive and exclusive by construction for any well-defined `A` (Step 1 §7) |
| **Filter counts decrease monotonically, coded `>=` not `>`** | a position **adds** rows — in practice a join fan-out at position 1 (duplicate show rows, or a user matching a show twice), or a row emitted twice by a checkpointed pass | **No, but it has real bite:** it is the only invariant that catches a fan-out. `>=` because a position may legitimately remove nothing — **position 2 removes exactly 0 on this frame**, so a `>` coding fails on correct data here, not hypothetically |
| **Distinct episodes never exceed season length (`\|D\| ≤ L`)** | the implementation filtered by the numeric **range** `1..F` instead of by membership in the listed set `E` | **No — code check.** True by construction under set membership (Step 1 §3.2) |
| **`A ⊆ A_H` on every row** | the two sets were computed from different evidence, or `τ2` was computed below `τ1` | **No — code check** (`0034`). True by construction since `τ1 < τ2` |
| **Set-membership drop rule enforced** | same failure as `\|D\| ≤ L` | **No — code check** |
| **Clock start: on or after the S2 finale date, on or after the first-pass S1 completion date, and equal to one of the two** | the pipeline used a **different definition of the S1 completion date** — definition (a), last-observed — for a rewatcher whose rewatch fell after the S2 finale; that value equals neither term and the equality clause fails | **No — code check**, and only if the check **computes the first-pass date independently.** Read back from the pipeline it proves nothing, because `T0 = max(...)` makes all three clauses true by construction |

Two further notes on this set:

- **The equality clause is the only part that does any work.** The two inequalities alone restate
  `max()`. This is Step 1 §5 and D6 verbatim, and it replaced the old "no clock start precedes an S2
  premiere" invariant, which is **vacuous** under a finale-anchored clock.
- **The equality clause is trivially satisfied for 168 pairs** where the two terms are the same date
  (measured, §8). For those rows the invariant cannot distinguish a first-pass from a last-observed
  implementation.

---

## 4. What is stale, ambiguous, contradictory, or impossible as written

Fifteen items. Each quotes the line, says what is wrong, and says what I would need.

**F1 — `task-sheet.md` Step 7 blesses the superseded rule's answer, in the bullet that supersedes it.**

> "**Exclusions at `W = 108`: APPLY 703 from 216 accounts (604 never-started + 99 started-and-left);
> DERIV 99 from 73 accounts (0 + 99).** Superseded: ALT-MATCHED 793/189 APPLY and 188 DERIV, ALT 604/0.
> **A Step 7 instance reporting 0 on DERIV and 604 on APPLY is correct and the two are not a
> divergence.**"

The last sentence is ALT's answer — the rule superseded at `0048` — declared correct one clause after
being named superseded. My definition file says the opposite: "604 is the superseded ALT answer … and
that IS a divergence." This is exactly the failure `CLAUDE.md` describes: an adopted figure and its
superseded predecessor live in the same file, each declaring the other wrong. It survives from `0047`,
where under ALT the DERIV zero *was* correct. **I read the adopted answer as 703/99 (`0054`, `0064`).
I need that sentence struck or a ruling that it is not operative** — it is in the file the isolated
instances read, and it licenses a wrong-rule result as "correct".

**F2 — `task-sheet.md` Step 0 still carries the superseded 403 rule.**

> "On a 403, hard stop and report. That is a block, not a throttle."

`CLAUDE.md` and `decisions/0004` amended this on 2026-08-10 to classify-before-acting with two circuit
breakers. My definition file records that this drift was fixed *in the agent files* at `0035`; the task
sheet never got the pass. Not a Step 8 line, but the read-back brief asks for disagreements and
`CLAUDE.md` wins on API discipline.

**F3 — Step 7's status is stale in two of the seven surfaces.**

`task-sheet.md` Step 7 header: "**NOT approved; seven Red Team HOLDs.**" My definition file: "**The gate
is OPEN and Step 8 does not launch until it closes**", citing `0046` as the current rule change.
`decisions/0064` and `artifacts/step7-gate-approval.md` say the gate was **approved unconditionally**
after fifteen reviews and that **Step 8 may launch**. `decisions/` wins. **Step 8 remains an unapproved
gate regardless** — that is not in question here.

**F4 — `0033`'s expected censoring numbers were computed in the opposite filter order to the one Step 8
mandates, and I can show the gap.** Measured, read-only (§8):

| At `W = 108` | Aggregate retained | pre-2020 | 2020–2022 | 2023–2025 |
| :--- | ---: | ---: | ---: | ---: |
| `0033` / `task-sheet.md` expectation | **97.6%** | **98.0%** | **97.5%** | **96.0%** |
| Censoring on the **position-3** output (220,107) — reproduces it exactly | 97.62% | 98.0% | 97.5% | 96.0% |
| Censoring on the **position-4** output (201,900), which is the mandated order | **97.40%** | **97.8%** | **97.4%** | **95.9%** |

At `W = 213` the same split: expectation 97.3 / 96.4 / **89.7**; mandated order 97.0 / 96.3 / **89.5**.
So the spec's headline claim — "the 2023–2025 cohort loses **10.3%** of its pairs at `W = 213`" — becomes
**10.5%** under its own mandated order. **An instance that follows the order will not reproduce the
numbers the order is documented with**, and may file a false defect against itself. I need to know
whether `0033`'s table is an expectation to reproduce or a superseded rendering.

**F5 — the 3,440 constant is on a population Step 8 does not build.** Step 8 requires reporting "the
3,440 Started-and-left pairs completing at any point before `τ_pull`". That figure comes from the Step 1
amendment, where the Started-and-left group is **17,420 before / 15,174 after** the amendment — on the
**128,099 uncensored estimation sample**, which the amendment states is "not right-censored". Step 8's
Started-and-left group on **APPLY** is 18,952–19,745. So the spec embeds a constant whose population is
unnamed at the point of use and is not the population Step 8 runs on — the exact defect the standing
rule from `0047` exists to prevent. **I do not know whether Step 8 is to restate 3,440 or to recompute
the analogous count on its own population.** Both readings are faithful and they produce different
numbers.

**F6 — "Retain `action` as a column" cannot support the Step 13 arm it exists for.** Step 13's arm is
"`action`-type, excluding `checkin`-only and manual-`watch`-only evidence", which needs to know, per
pair, the action composition of the **S2 evidence set** (and arguably of the S1 completion evidence,
since the completion date moves too). A pair has many records with many actions. A single `action`
column on a pair row can be: the action of the first S2 record; the modal action; the set of distinct
actions; a per-episode list; or a pair of booleans ("S2 evidence is checkin-only", "…manual-watch-only").
**All five satisfy the sentence; only some support Step 13.** This is a first-order divergence risk.

**F7 — the abandonment point is under-specified in Step 8's own text.** Step 8 says only "abandonment
point". The operative rule lives in Step 10 and Step 1 §7: **rank form, on `A_H`** —
`p = |{ e ∈ E2 : e ≤ m_H }| / L2` with `m_H = max(A_H)`, and `p = m_H / L2` explicitly **not** the rule.
An instance reading Step 8 alone could compute `m/L2` on `A` at `τ1`. On *this* frame the rank-vs-ratio
half makes no numeric difference — all 1,138 shows have `E2` contiguous from 1 — but the `A`-vs-`A_H`
half does: the amendment moved 2,246 pairs, and they are the ones that got furthest.

**F8 — the position-1 population is undefined, and it is a required waterfall line.** "Step 2 frame"
names a filter but not what it filters. Candidates, all faithful: (a) the cross product of pulled
accounts × frame shows; (b) every `(user, show)` pair with at least one episode record on a frame show;
(c) every pair with at least one **S1** record. Only the **post-position-3** count is pinned by Step 5's
220,107. **Waterfall lines 1, 2 and 3 are required outputs and are diffed**, and two instances choosing
(a) and (b) would disagree on lines 1–2 while agreeing on everything downstream. I need the position-1
row set defined.

**F9 — D2's split has a third case that exists in the data.** "Split by which term of the `max()` binds"
is binary. **168 pairs have both terms on the same date** (measured; Step 5's own pair table already
codes a `tie` class). Assigning them to `s1`, to `finale`, or to a third line are all faithful readings.
Small, but D2's whole value is that the S1-term count is small, so a rule that silently dumps 168 into
it is not harmless.

**F10 — "discovery channel" is not single-valued.** The Step 3 pool is 5,694 users: A-only 3,672, B-only
1,698, **and 324 in both** (`in_a` and `in_b` true; `channel_first` A for 77, B for 247). Step 8 must
carry "discovery channel" and Step 11 recomputes the headline **within each channel**. Carrying
`channel_first`, carrying a two-flag membership, or carrying "both" as a third value are all faithful,
and they give Step 11 different denominators.

**F11 — the liveness silence test's boundary form and evidence scope are unstated.** Two open points:
(i) is "no insertion instant **after** `τ1`" `> τ1` or `≥ τ1`? The half-open convention is fixed for
`watched_at` (D13) and the channel window is explicitly "`(τ1, τ2)`, open at `τ2`" (`0064`), so the
project does specify these — except here. (ii) Does the account-wide insertion evidence include records
whose `watched_at ≥ τ_pull`, which D11 discards? **The two Step 7 arms already diverged on exactly this**
— robustness survival 792 (A) against 791 (B), "consistent with a `≤ τ_pull` restriction A states and B
does not" (`0054` §6, carried into `0064` §4 item 8, **reported not reconciled**). The same ambiguity
reaches Step 8 position 6.

**F12 — DERIV cannot be produced by the mandated chain, and nothing says who produces it.** Step 8
filters APPLY. Step 9 and Step 8b require **both** populations, separate arithmetic, every bound field
stating its population. DERIV is Step 5 line 4 less D10, i.e. it applies restrictions position 4
deliberately does **not** apply: `has_s2`, `T0 not contaminated`, `completing record not post-dated`. I
reproduced it (178,165 → 155,131 → 152,126 → **147,370**) from the Step 5 pair tables, so it is
constructible — but only from Step 5 flags that **Step 8's row spec does not list as columns**. Either
Step 8 carries those three flags or Step 9 re-joins Step 5 itself, which is a second definition of the
population.

**F13 — the file named `adopted_rule.json` does not hold the adopted rule's numbers.**
`processed/step5/adopted_rule.json` carries revision-3 figures: `retained 215,258`, `removed 4,849`.
The approved rule is revision 6: **201,900 retained, 18,207 excluded** (`0021`, and the artifact's own
revision table). The final exclusions do reproduce cleanly from `processed/step5/pair_revision5.csv`
(16,665 + 1,542 → 201,900), so the data is fine — but the obvious file to read is superseded and
unstamped. **`processed/` is not one of `CLAUDE.md`'s seven propagation surfaces**, so the grep control
does not cover the file a Step 8 implementation would reach for first.

**F14 — "every `W` arm Step 13 tests" is defined only by reference.** Step 13 states the range
constraints (Step 6's two-curve range, the 46–107 union, plus 150 and 213) and separately prints series
"at `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213". That eight-point grid is nowhere stated as *the*
arm list in a line that says so; 125 and 180 also appear (in the frozen-D10 discussion, flagged as **not
in the mandated grid**). And it is not said whether Step 8 emits the **table** per arm or only the
per-arm **counts** (D3′, per-air-period retention, retained rows). Re-censoring at 8 arms is 8 runs of
positions 1–6; that is a scoping decision, not a detail.

**F15 — smaller, but each is a place two faithful instances differ.**
(a) The waterfall's **unit**: pairs only, or pairs + users + shows? Position 2 is explicitly shows and
pairs; the rest are silent. (b) **Cumulative retained vs removed** per line — the spec says "sample size
after each filter", which reads as retained, while the required censoring output is stated as a
*removal* in two lines. (c) **D9's split signature** relies on "show titles or `ids` indicate the same
title" — no normalization rule, and detection is stated to be imperfect and a lower bound. (d) Whether
D8 is measured on the position-5 or position-6 population — pre- or post-liveness never-starteds are
different sets, and D8(ii) is Step 14's ledger item 10. (e) The scope qualifier in my definition file
carries the headline clause but not the widening rule sentence that `0062` states with it ("concede
every pair dormant before the instant at which its own state-defining null is read"); `0064` §4 item 7
records that the `analytics-engineer` pair "carries one clause of it". I do not know whether that is the
clause meant.

---

## 5. What Step 8 requires that has moved or no longer exists

| Step 8 names | Status | It has moved to |
| :--- | :--- | :--- |
| "a fixed documented order" | **withdrawn** | the exact 7-position order (`0029` §3) — the phrase is gone from Step 8 but is still the wording in my definition file's own explanation of what was withdrawn |
| **D3** resumption report | **superseded** | **D3′** (`0034`): scored at `τ2`, cleared at `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, measured over `[τ2, τ2 + H)`, per arm. D3 "measures nothing" post-amendment |
| "no clock start precedes an S2 premiere" | **vacuous, replaced** | the three-part clock-start check with the independent first-pass recomputation (D6, Step 1 §5) |
| outcome assignment "at `τ1`" (`0029`'s own position 7) | **superseded** | **two instants** (`0034`): `\|A\| = 0` at `τ1`, Continued at `τ2` on `A_H` |
| a **liveness threshold** | **deleted** | nothing. Derived three times — 632 d, then 1,293 d — and deleted at `0042`; the rule is parameter-free. Step 8 does not name one, and must not acquire one. *(`632` is also the legitimate frozen-D10 never-started component at `W = 125`, so a blind grep gives a false positive there.)* |
| **604** as the liveness exclusion count | **superseded** | **703** (`0048`, restored `0054`, approved `0064`). 793 is ALT-MATCHED's, withdrawn |
| the never-started bound `[16.7146%, 16.9704%]` and `[9.6830%, 10.0405%]` | **superseded** | `[16.6633%, 16.9704%]` and `[9.6372%, 10.0405%]` on **APPLY**; `[6.2055%, 6.2055%]` (degenerate) and `[11.3015%, 11.4291%]` on **DERIV**. Step 8 does not compute them, but must not strip the **scope qualifier** from any note that carries them |
| "the Step 5 exclusion" as a single documented artifact | **exists under another name** | the adopted rule is `0021` + `artifacts/step5-contamination-diagnostics.md` §1; the on-disk `processed/step5/adopted_rule.json` is revision 3 (F13) |
| `W` from the Step 6 artifacts | **neither is the adopted value** | `W = 108` from `0026`. The artifacts state 107 (`-a`) and 107.7135 (`-b`), both pre-ceiling-ruling |

---

## 6. What I would have to decide myself in order to run this

Listed, **not resolved.** Each is a place the two instances can differ.

1. The **position-1 row set** (F8).
2. The **unit and direction** of each waterfall line — pairs vs pairs+users+shows; retained vs removed (F15a, F15b).
3. What **`action`** means as a pair-level column (F6).
4. Whether the **abandonment point** is the rank form on `A_H` (F7) — I would take Step 1 §7 as governing, but Step 8's own text does not say it.
5. **Discovery channel** for the 324 dual-channel users (F10).
6. **D2's tie class** (F9).
7. The **boundary form** of "no insertion instant after `τ1`", `>` or `≥` (F11i).
8. Whether liveness evidence includes records with `watched_at ≥ τ_pull` (F11ii) — the known 792/791 divergence.
9. How **clamped / uncalibratable insertion instants** are treated: `0048` §9 records 5,094 records clamped above the calibration range, pushing `max(instant)` earlier and **directly toward false exclusion**, and 22.68% of dated records claim a `watched_at` later than their own calibrated insertion instant. Nothing says what to do with a record whose instant cannot be interpolated.
10. Which **`W` arms** Step 8 runs, and whether the table or only the counts are emitted per arm (F14).
11. Whether **D8** is measured pre- or post-liveness (F15d).
12. Whether the **3,440** is restated or recomputed (F5).
13. Whether **DERIV** is Step 8's output or Step 9's re-join, and if Step 8's, which Step 5 flags become columns (F12).
14. Which file position 4 reads its exclusion from, and whether the two exclusions are **re-derived** from record-level flags or **read** as a stored pair list (F13).
15. Whether `0033`'s per-air-period expectations are targets or superseded renderings (F4).
16. The **air period** boundaries — I would take `air_period` from the frame (`0017`), which is already materialized as pre-2020 / 2020–2022 / 2023–2025; the spec names the buckets only inside `0033`'s example table.

---

## 7. What Step 8 does not ask for that I believe it needs

Given what Step 9, Step 10, Step 13 and Step 8b read out of this table:

1. **The liveness exclusion decomposed and retained as columns, not just counted.** Step 9's four bound
   endpoints are built from counts Step 8 is uniquely positioned to emit and is not asked to:
   never-started exclusions (**604** on APPLY, **0** on DERIV), started-and-left exclusions (**99** on
   both), the **90 / 89** channel pairs (retained, ¬Continued, live only by an insertion after `τ1`,
   last insertion inside the open window `(τ1, τ2)`) and the **207 / 3** never-started channel pairs,
   plus the **216 / 73** account counts. Without them Step 9 recomputes liveness — a second definition of
   the filter.
2. **The DERIV population, or the three Step 5 flags that let Step 9 build it** (F12).
3. **A `has_s2` / evidence-provenance marker per row**, for the same reason, and because D4
   (S3-without-S2) is a Step 9 bound over rows Step 8 scores Never started.
4. **The account base, and the absent accounts named as absent.** The analysable cohort is the 2,549
   `complete` accounts; the 287 `discarded_over_tolerance`, 38 over-cap and 1,214 never-attempted are
   **absent, not empty** (Step 5 §15 limit 6), and `CLAUDE.md` requires an `access_denied` user to stay
   distinguishable downstream *because a skipped user silently read as empty becomes a false "never
   started" in the headline*. Step 8's waterfall is where that becomes visible or invisible, and it is
   not a required line.
5. **The position-6 count published beside the position-5 count.** `0064` §4 item 4 records a live
   residual — "bounds on position-5, shares post-liveness" — so both denominators (196,654 and 195,951)
   must be on the face of the waterfall or Step 9 will mix them, which is the defect that produced three
   consecutive non-covering bounds.
6. **A per-arm structure that matches Step 8b's schema, keyed on `W` alone.** Step 8b is chained behind
   this step and Steps 9–13 write into the schema **directly, with no conversion layer**. If Step 8's
   waterfall is emitted in a shape the schema cannot hold, the conversion layer appears here — and "two
   definitions of one figure is the defect this study has hit most often".
7. **Coverage counts on every zero** (§2): `L2 = 1` = 0 of 1,138 shows; metadata disagreements 0 of
   1,138; C0 = 0. "A check that finds nothing because it looked nowhere must fail."
8. **The `p = 1.0` residual count**, which Step 10 must re-report on `A_H` rather than carry over. Step 8
   builds `p`; the residual is cheapest here.

---

## 8. Read-only checks I ran, and what they returned

No writes outside this file, zero API calls. These are count checks against stored data, permitted by
the brief; none of them is the deliverable.

| Check | Result |
| :--- | :--- |
| Frame size, `L2 = 1` shows | 1,138 shows; **0** with `L2 = 1`; `pool_completers` sums to **220,107**, matching Step 5 §1 |
| D12 buckets in the frame | C0 **0**, C1 **206**, C2 **340**, C3 **167**, C4 **425**; **7** shows within 1 day of a boundary |
| Metadata disagreement flags | `s1/s2_count_disagreement`, `s1/s2_aired_lt_listed` all `False` for all 1,138; `E2` contiguous from 1 for all 1,138 |
| Step 5 adopted exclusions, from `pair_revision5.csv` | all-air-date S2 **16,665**; contaminated `T0` with no S2 **1,542**; retained **201,900** — reproduces `0021` |
| Right-censoring at `W = 108` on the position-4 output | **196,654** retained = **APPLY**, exactly. 97.40% aggregate; 97.8 / 97.4 / 95.9 by air period |
| Right-censoring at `W = 108` on the position-3 output (220,107) | 214,858, 97.62%; **98.0 / 97.5 / 96.0** — reproduces `0033`'s table exactly (F4) |
| Right-censoring at `W = 213` | mandated order 95.73%, 97.0 / 96.3 / **89.5**; position-3 order 96.06%, 97.3 / 96.4 / **89.7** (= `0033`) |
| DERIV reconstruction | 201,900 → 178,165 → 155,131 → 152,126 → censored **147,370**, exactly |
| `max()` binding term | `s1` **116,041**, `finale` **103,898**, **`tie` 168** (on 220,107) |
| Step 3 pool channels | 5,694 users: A-only **3,672**, B-only **1,698**, **both 324** |
| `processed/step5/adopted_rule.json` | carries revision-3 figures (`retained 215,258`, `removed 4,849`) — superseded by revision 6 |

**What the population checks buy.** `0047` §7 warns that a Step 8 count differing from 703 is a
population defect first, because Step 7 built APPLY from the Step 5 pair table rather than through
positions 1–5. On this data those two constructions **agree exactly at position 5** (196,654), provided
position 4 is the two adopted exclusions and nothing else. That narrows what a mismatch at position 6
could mean — but it does not verify positions 1–3, whose counts nothing on disk pins except the 220,107
total.

---

## 9. What I do not know

Stated rather than resolved, per the brief.

- Whether `0033`'s per-air-period figures are targets to reproduce or a superseded rendering (F4). The
  arithmetic is unambiguous; the intent is not.
- Whether Step 8 is expected to restate the 3,440 or recompute its analogue on APPLY (F5).
- What "`action` as a column" is meant to be (F6).
- What the position-1 row set is (F8).
- Whether the scope-qualifier clause carried in my definition file is the full one `0062` states (F15e).
- Whether the sentence in F1 is live text or a survival, and therefore whether 604 is a divergence or an
  acceptable answer. **I have not resolved it and I have not implemented against either reading.**

---

**Step 8 is a gate, it is unapproved, and this document is not it. Nothing proceeds without written
approval from the Human Lead.**
