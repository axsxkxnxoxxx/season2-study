# Step 8 — read-back, instance `a`

**Owner:** Analytics Engineer (`a`) · **Task:** `specs/step8-readback.md` · **Date:** 2026-08-14

> **THIS IS NOT STEP 8.** Step 8 is a gate, it is unapproved, and it has not launched. **Nothing was
> built, no row was filtered, nothing was written to `processed/`, and zero API calls were made.** The
> only computation performed was reading stored data to check counts, which the read-back spec permits
> explicitly. Every such count is marked **[checked]** and names the file it came from.
>
> **This document is a statement of the spec as I read it, plus the places I cannot read it one way.**
> It proposes nothing and adopts nothing. Where I do not know what a line means, I say I do not know
> rather than choosing a reading and presenting it as the reading.

**Sources read:** `task-sheet.md` Steps 0–18 (Step 8 and 8b in full), `CLAUDE.md`,
`.claude/agents/analytics-engineer.md`, `artifacts/step1-outcome-definition.md` (all 1,632 lines),
`decisions/0011`, `0019`, `0021`, `0029`, `0033`, `0034`, `0047`, `0048`, `0049`, `0054`, `0056`,
`0062`, `0064`, `0066`, `artifacts/step5-contamination-diagnostics.md`, `artifacts/step6-window-w-{a,b}.md`.

---

## 0. Population vocabulary used throughout

Three populations recur and they are not interchangeable. Every figure below names one.

| Label | Definition | n |
| :--- | :--- | ---: |
| **APPLY** | Step 5 waterfall **line 1** (analysis population, 201,900) less D10 right-censoring | **196,654** |
| **DERIV** | Step 5 waterfall **line 4** (completing record not post-dated, 152,126) less D10 | **147,370** |
| **Estimation sample** | Step 5 line 5, `W`'s estimation sample | 128,099 |

**[checked]** `201,900 − 196,654 = 5,246`; `152,126 − 147,370 = 4,756`. Waterfall lines from
`artifacts/step5-contamination-diagnostics.md` §"Analysis population".

**APPLY is the population Step 8 filters at position 6.** **DERIV is not produced anywhere in Step 8's
seven positions** — see §7.1, which I believe is the most consequential gap in the step.

---

## 1. The filter order, as I would apply it

`decisions/0029` §3 fixes the order exactly and gives the reason: the final row set commutes but the
per-filter sample size does not, so two faithful instances applying the same filters in different
orders report different waterfalls on an identical table and the diff cannot tell that from a bug.
`decisions/0034` then amended position 7 from "at `τ1`" to "at two instants."

| # | Filter | What it removes | What it is applied **to** |
| :-- | :--- | :--- | :--- |
| **1** | Step 2 frame | pairs on shows outside the 1,138-show frame | **the base population — WHICH THE SPEC NEVER DEFINES. See §4.1.** |
| **2** | `L2 = 1` exclusion | pairs on shows with a one-episode S2 | output of 1 |
| **3** | S1 completion rule | pairs failing `F1 ∈ D1 ∧ \|D1\| ≥ ceil(0.90 × L1)`, `D1 ⊆ E1` by set membership | output of 2 |
| **4** | Contamination exclusion (Step 5) | 16,665 all-air-date-stamped-S2 pairs + 1,542 no-S2-with-fabricated-binding-`T0` pairs | output of 3 |
| **5** | Right-censoring | pairs failing `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull` | output of 4 |
| **6** | **Liveness** | pairs that are **NOT LIVE** | output of 5 — **on APPLY this is 196,654 rows and 703 are removed** |
| **7** | Outcome assignment | **nothing — it removes no rows.** It annotates. | output of 6 |

### 1.1 Where liveness sits and what it operates on

**Position 6, after right-censoring and before outcome assignment.**

- **The unit is the user-show pair, never the account.** Evidence is account-wide (the whole sweep,
  other shows and movies included); the *test* is clock-start-relative and clock start is
  pair-specific, so one account can be live for one show and not for another. **No user is dropped
  wholesale** (Step 1 §0/§1/§9; `0064` §1).
- **The rule (ALT-BROAD, approved `0064`):** a pair is **NOT LIVE iff BOTH** (i) the account shows **no
  insertion instant after that pair's `τ1 = ⟦T0⟧ + W × 24h`**, **AND** (ii) the pair is **NOT
  Continued**. Otherwise live.
- **The silence test is anchored at `τ1` and only at `τ1`** (`0034`, `0051`, `0054`). **`τ2` does play a
  part** — conjunct (ii) *is* the Continued test, read at `τ2` on `A_H` — so **the rule reads two
  instants**. The line "`τ2` plays no part" is withdrawn (`0049` §3 item 1).
- **It runs on record INSERTION time, not claimed `watched_at`** (`0021` standing ruling 2), via the
  **stored isotonic play-`id` calibration at `processed/step5/calibration.npz`, which is NEVER
  refitted** (`0029`).
- **Do not reintroduce a pre-`τ1` requirement in any form** — withdrawn twice (`0040` §1, `0042` §3).

**On APPLY at `W = 108` this removes 703 pairs from 216 accounts: 604 never-started + 99
started-and-left.** How the two conjuncts select: conjunct (ii) narrows `196,654 → 52,514`; conjunct
(i) narrows `52,514 → 703`, so **conjunct (i) does most of the work**, which is why the count moves
with `W` (`0047` §2, `0049` §3 item 5).

**604 is ALT's superseded answer. 793 is ALT-MATCHED's withdrawn answer.** Producing either means a
superseded rule was implemented and **that is a divergence**. For any other number, the standing
instruction is to treat it as a **population** defect before an implementation one (`0047` §7,
`0054`).

### 1.2 Position 6 is outcome-conditional, and position 7 therefore does not stand alone

Conjunct (ii) is `NOT Continued`, so the outcome must be **evaluated** before liveness is applied even
though it is **assigned** at position 7. The spec requires waterfall line 6 to be **reported as
outcome-conditional** (`0046`, propagated to Step 7 and Step 8). The permission rests on two claims,
both of which I read as true and neither of which I am asked to re-derive: `|A|` and liveness are
row-local predicates on the position-5 output and **commute exactly**; and `0029`'s ordering rationale
is about per-filter sample size, which cannot reach position 7 because **outcome assignment removes no
rows**.

**What that permission does not cover, and Step 14 says so** (`0058`): the commutation check is a
statement about **counts on the observed sample**. It is **not** a demonstration that conditioning the
filter on the outcome leaves the estimand unchanged. That publishes as a limitation.

**Practical consequence for the implementation, which the spec does not spell out:** positions 6 and 7
are not separable passes. `A` (at `τ1`) and `A_H` (at `τ2`) must both exist at position 5's output.

---

## 2. Required counts, reports and diagnostics — and the population each is computed over

**Everything below goes to `artifacts/` and is counts/aggregates only, except the analysis table
itself, which goes to `processed/`.** The privacy rule is unambiguous and I have no question about it.

| # | Required output | Where | **Population it is computed over** |
| :-- | :--- | :--- | :--- |
| 1 | Sample size after each filter (the waterfall) | `artifacts/` | positions 1–7, each on the previous output. **Line 1's base is undefined — §4.1** |
| 2 | Drop count **per show** — dropped episode records and distinct dropped `(season, number)` | `artifacts/` | **NOT STATED.** Which position? Drops happen at record level before any pair filter |
| 3 | Drop count **per outcome** — pairs whose entire S2 evidence was dropped, as a share of Never started | `artifacts/` | **NOT STATED.** "Share of Never started" implies position 7 on APPLY, but the numerator is a record-level event |
| 4 | **D2** negative-lag report, split by which term of `max()` binds | `artifacts/` | **NOT STATED.** "a share of the population" — which population? |
| 5 | **D3′** resumption rate: of pairs Started-and-left **at `τ2`** with `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, the share completing in `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its **share of all Started-and-left** | `artifacts/` | a **cleared subset** of position-7 Started-and-left. **Per `W` arm, each arm its own cleared count and share.** The base "all Started-and-left" is presumably APPLY position 7, not stated |
| 6 | The **3,440** Started-and-left pairs completing at any point before `τ_pull`, **labelled a count and not a rate**, with its exposure-weighting by show recency stated at the point of use | `artifacts/` | **INCOHERENT AS WRITTEN — §4.4.** 3,440 is a figure measured on the Step 1 amendment's sample, not on Step 8's population |
| 7 | **D8** never-started post-window diagnostic, (i) count/share with any S2 episode in `[τ1, τ2)`, (ii) count/share satisfying Continued over that horizon | `artifacts/` | pairs scored **Never started at `τ1`**. Population not stated; APPLY position 7 is the only reading I can construct |
| 8 | **D9** split-artifact counts, **both halves**: (a) never-started rows carrying a split signature, (b) pairs **dropped at S1 completion** carrying the same signature | `artifacts/` | (a) position 7; **(b) is measured on rows position 3 REMOVED** — see §4.6 |
| 9 | Right-censoring removal as **TWO lines** — the `max(W, 91)` term and the **incremental** `+ H` term — each with its upward direction named | `artifacts/` | position 4's output (i.e. 201,900 on the published chain) |
| 10 | **Retained-pair counts PER AIR PERIOD after right-censoring, for every `W` arm Step 13 tests** (`0033`) | `artifacts/` | position 5 output, split by the show field `air_period`, **per arm** |
| 11 | `pull_date`; **earliest and latest per-user fetch dates**; count of records discarded for `watched_at ≥ τ_pull` | `artifacts/` | **NOT STATED** — all records in the sweep, or in-frame S1/S2 records only? The two differ by orders of magnitude |
| 12 | Per-bucket show and pair counts for all five D12 buckets `C0`–`C4`, plus shows within 1 day of a bucket boundary | `artifacts/` | **NOT STATED.** Which waterfall position are the pair counts on? |
| 13 | Metadata-disagreement counts, incl. the subset where `aired_episodes < \|E\|` for S2, with the direction named | `artifacts/` | shows and pairs on those shows; position not stated |
| 14 | Invariant results, all of them | `artifacts/` | per §3 |
| 15 | The analysis table | `processed/` | position 7 output |

**The finding the spec asked for is item-shaped and repeats:** of the fifteen required outputs, **only
items 5, 9 and 10 state their population unambiguously.** Items 2, 3, 4, 7, 11, 12 and 13 do not, and
every one of them is a number a diff will compare. This is the same class of defect `0047` §3 made a
standing rule about at the endpoint level — *"an endpoint states the population it is computed on and
the estimand it bounds, and they must be the same population"* — reappearing one level down, at the
diagnostic level, where the rule was never applied.

---

## 3. The invariants, and what would have to be true for each to fail

Six are required. **Four cannot fail on any data**; the spec already labels two of those as code
checks and I would label all four that way.

### 3.1 Outcome states are mutually exclusive and sum to the sample

**Cannot fail on data.** Step 1 §7 proves the partition `A = ∅` / `(A ≠ ∅ ∧ C_H)` / `(A ≠ ∅ ∧ ¬C_H)`
is exclusive and exhaustive for any well-defined `A`, and §3.2's set-membership rule is what makes `A`
well-defined.

**It can fail on an implementation, and there is a named population that would trip it.** Drop the
`|A| ≥ 1` conjunct from Continued and a pair that starts S2 after `τ1` and completes by `τ2` satisfies
`F2 ∈ A_H ∧ |A_H| ≥ ceil(0.90 × L2)` with `|A| = 0` — landing in **both** Never started and Continued.
Step 14 ledger item 10 sizes that population at **1,573 pairs after right-censoring** (`0034` §4). So
this is a code check with real teeth, and I would report it as one rather than as evidence about the
data.

### 3.2 Filter counts decrease monotonically — **coded `>=`, not `>`**

**Fails only if a filter position *increases* the row count**, which on this pipeline means a
fan-out: joining the frame or the Step 2 show fields on a key that is not unique per show, or a
per-record join leaking into a per-pair table.

**Why `>=` and not `>` — the reason changed but the coding did not** (`0047` §6 → `0049` §4). The
original reason was that the DERIV exclusion set was empty under ALT, making decrease non-strict.
**Under ALT-BROAD decrease is strict at line 6 on both populations at every arm** — 703 APPLY, 99
DERIV — so that reason is gone. `>=` is kept for a better one: **the invariant must not encode a
property of one rule**, and a filter position that legitimately removes nothing must not fail an
assertion.

**That case is not hypothetical on this data. [checked]** `processed/step2/frame.csv`: of 1,138 frame
shows, **zero have `s2_L = 1`** (the minimum is 2, on one show). **Position 2 removes 0 shows and 0
pairs**, so line 2 equals line 1 exactly. Under `>` the invariant would fail on correct data at the
second position of the chain.

### 3.3 Distinct episodes never exceed season length

**Cannot fail on data.** Step 1 §3.2: under set membership `D1 ⊆ E1` and `A ⊆ E2` by construction, so
`|D1| ≤ L1` and `|A| ≤ L2`. Step 1 §3.2 says so in terms — *"it is a code check, not a data check. The
data check is the drop count below."*

**Fails only if the implementation filtered by the numeric range `1..F` instead of by the listed set
`E`** — which is precisely the F1 defect the set rule was adopted to prevent.

### 3.4 `A ⊆ A_H` on every row

**Cannot fail on data.** `τ1 < τ2` and `A_H` is `A` with the bound moved outward, so containment is
definitional. **The spec labels it a code check and says why** (`0034`, Step 8 line 320): it can only
catch an implementation that computed the two sets wrongly and **is not evidence for the rule**.

**Fails if** the two sets were built with different membership or dedup rules, or the bounds were
transposed. Note it holds trivially on every Never-started row, where `A = ∅`.

### 3.5 Clock start: on or after the S2 finale date, on or after the first-pass S1 completion date, and **equal to one of the two**

This replaces the withdrawn "no clock start precedes an S2 premiere", which is **vacuous under a
finale-anchored clock and catches nothing** (Step 1 §5, D6).

**The two inequalities alone are also vacuous** — they restate `max()`. **The equality clause is the
whole check**, and it only does work **if the check computes the first-pass S1 completion date
independently rather than reading back the pipeline's value.** The spec says this in both places
(`task-sheet.md` Step 8; Step 1 §5, §9). What it catches: a **last-observed** S1 implementation, whose
clock start for a rewatcher whose rewatch postdates the S2 finale equals neither candidate date.

**One thing I cannot tell from the spec:** whether a mismatch between the independent recomputation
and the pipeline's value on a *tie-break* (Step 1 §2.2 breaks exactly-equal timestamps by episode
number then smallest event `id`) counts as a failure or as an artifact of running the walk twice. The
spec does not say. I would report both counts rather than choose.

### 3.6 The set-membership drop rule

Labelled by the spec as **an implementation check, not a data check** — `|D| ≤ L` holds by
construction under set membership. Same status as 3.3, of which it is really the enforcement half.

---

## 4. What is stale, ambiguous, contradictory, or impossible as written

Ordered by how much it moves a number a diff would compare.

### 4.1 **Waterfall line 1 has no defined base population.** This is the largest one.

> `task-sheet.md` Step 8: *"**1.** Step 2 frame → …"* and *"Record sample size after each filter."*

"Step 2 frame" names a **filter**, not the set it filters. Four bases are constructible from what is on
disk and all four are defensible readings:

| Candidate base for line 1 | n | **[checked]** source |
| :--- | ---: | :--- |
| Cross product, 2,549 users × 1,138 frame shows | **2,900,762** | arithmetic |
| Pairs with any S1-or-S2 record on a frame show | **278,452** | `processed/s1s2_scan.npz` |
| Pairs with any S1 record on a frame show | **274,741** | `processed/s1s2_scan.npz` |
| S1-completer pairs on frame shows (`pool_completers`) | **220,107** | `processed/step2/frame.csv` |

**They differ by more than an order of magnitude, and lines 1, 2 and 3 of the published waterfall all
move with the choice.** Only the last coincides with a downstream anchor, and choosing it collapses
positions 1–3 into one line, which the fixed order exists to prevent. **This is exactly the failure
`0029` §3 fixed the order to avoid, one step earlier in the chain than the fix reached.**

I do not know which is meant and I will not pick one.

### 4.2 **Applying D11 as Step 1 requires gives a position-3 line that is not 220,107.**

Step 1 D11 is categorical: *"Every record with `watched_at ≥ τ_pull` is discarded from every
computation in this document, whether or not it was fetched."* `τ_pull = 2026-08-11T00:00:00Z`
(`0011`).

**[checked]** `src/step2_build_frame.py` computes `pool_completers` from `s1s2_scan.npz` and **never
touches the timestamp column** — `TAU_PULL` appears in that file only in the exposure-years
calculation. And the records exist: **167 in-frame S1/S2 records carry `watched_at ≥ τ_pull`, on 81
pairs (73 S1, 94 S2).**

**[checked]** Recomputing S1 completion under the approved Step 1 §4 rule on the same scan:

| | S1-completer pairs on frame shows |
| :--- | ---: |
| Without the D11 filter (what the frame publishes) | **220,107** |
| With the D11 filter (what Step 1 D11 requires) | **220,103** |

**Four pairs.** Small, but the chain downstream of it is stated as exact numbers: position 4 is
expected at 201,900, position 5 at 196,654, and position 6 at exactly 703 with the instruction that a
mismatch is a **population defect**. An instance that honours D11 and an instance that reads the
frame's `pool_completers` produce different lines 3, 4 and 5 and possibly a different line 6, and
**both are faithful to a written rule.** The spec does not say which rule wins.

I flag this as a defect in the record rather than a discrepancy to fix: `decisions/0034` §5 recorded
the same class of finding — *"D11 was not being applied"* — inside the amendment scripts, and the
published populations 220,107 / 201,900 / 196,654 all sit upstream of that discovery.

### 4.3 **The step is written at one `W` and required to report at eight, and never says which object is per-arm.**

Step 8 fixes `W = 108`. But three required outputs are per-arm: **D3′ at every Step 13 arm**,
**retained-pair counts per air period for every `W` arm** (`0033`), and — by `0047` §5 — **D10 must be
re-derived at each arm, never frozen.** Right-censoring, `τ1`, `τ2` and the liveness exclusion set all
contain `W`, so a per-arm figure requires re-running **positions 5, 6 and 7** per arm.

Two things are undefined:

1. **Is the analysis table itself built once at `W = 108`, or once per arm?** "Build one row per
   user-show pair" is singular; the per-arm requirements are not.
2. **What is the arm grid?** Step 8 never lists it. Step 13 gives four constraints (below/above 108;
   cover Step 6's C1-vs-all-shows range; span 46–107; include 150 and 213) and the *operative* series
   quoted at Steps 7 and 13 is **38 / 46 / 77 / 91 / 107 / 108 / 150 / 213**. But **[checked]** the two
   Step 6 deliverables state the minimum range as **[37, 107]** (`step6-window-w-a.md` §11) and
   **[37.70, 107.71], "in whole days, arms spanning 37 to 108"** (`step6-window-w-b.md`). **Neither
   says 38.** And Step 8 explicitly instructs *"take the number from the decision entry, not from the
   artifacts"* for `W` itself — leaving no authoritative source for the grid at all.

### 4.4 **"the 3,440 Started-and-left pairs" is a figure, not an instruction, and it cannot be both.**

> Step 8: *"Report alongside, **labelled a count and not a rate**, the 3,440 Started-and-left pairs
> completing at any point before `τ_pull`…"*

**3,440 was measured on the Step 1 amendment's sample** — `0034` §3: of 5,686 Started-and-left pairs
that eventually complete S2, 2,246 reclassify and 3,440 do not. Step 14 item 9 states plainly that
**3,440 is a floor** because *"the estimation sample excludes pairs the Step 5 waterfall drops, and it
is not right-censored."*

Step 8's population is APPLY position 7 — right-censored, contamination-excluded, liveness-filtered.
**The count on Step 8's population is therefore not 3,440 and cannot be.** One instance restates the
constant; the other recomputes and reports a different number; both are reading the same sentence.
I do not know which is wanted.

### 4.5 **"Expect 703 at position 6" carries a caveat that the spec states and then does not act on.**

`0047` §7 and `0049` are explicit: Step 7 measured its counts on APPLY **built from the Step 5 pair
table, not through Step 8's positions 1–5.** `0064` §4 keeps this on the published residual list —
*"the population mismatch"* — and `0047` §4 records what the gate **cannot** establish: *"that Step 8's
position-6 population is the one reconstructed here."*

So 703 is an expectation whose warrant is that two chains ought to agree, and **Step 8 is the first
place that has ever been tested.** That is fine and is what the instruction says. What is not defined
is **what I do if it does not match**: "treat it as a POPULATION defect before an implementation one"
tells me how to diagnose, not whether to stop, and Step 8 is a gate at which I must not adopt.

**One thing I can say from checking rather than arguing.** The two chains can only agree if position 2
removes nothing, because Step 5's 201,900 was never `L2 = 1`-filtered. **[checked]** it removes
nothing on this frame (§3.2), so that particular joint is sound. **[checked]** the contamination
exclusion reproduces exactly from `processed/step5/pair_revision5.csv`: all-air-date-S2 pairs
**16,665**, no-S2-with-contaminated-`T0` **1,542**, retained **201,900**, on a base of 220,107 rows.

### 4.6 **D9's second half is measured on rows that position 3 deleted.**

> *"Split-artifact counts (D9), both halves: the fabricated never-started row and the silently deleted
> S1-failing counterpart."*

Half (b) is, by Step 1 §10.0b's own construction, *"pairs dropped at S1 completion"* — pairs that
**disappear from the population entirely, unreported**. They are not in the analysis table and cannot
be recovered from it. **The pipeline must retain position 3's drop set as a side output for this to be
computable at all**, and no line in Step 8 says so. Nothing here is impossible; it is a requirement
whose precondition is unwritten, and an implementation that streams the filters and keeps only
survivors satisfies every other line in the step and cannot produce this one.

### 4.7 **Two things the outcome table needs that the spec does not pin.**

- **`p` is defined only for Started-and-left** (Step 1 §7). The step says "include per row:
  abandonment point." Null, empty, `0`, and "computed anyway for every started pair" are all
  constructible. `p` is read on `A_H` in the **rank** form, `p = |{e ∈ E2 : e ≤ m_H}| / L2`;
  `m_H / L2` is withdrawn and must not be reinstated.
- **"discovery channel" is single-valued in the schema and not in the data. [checked]**
  `raw/step3/user_pool.jsonl`, 5,694 users: `in_a` only **3,672**, `in_b` only **1,698**, **both
  324**. The pool carries `channel_first` (a deterministic tiebreak) *and* two membership flags.
  Step 11 recomputes the headline "separately within Channel A and Channel B", which reads like
  overlapping membership, not a partition. One column or two is a spec decision, and 324 users'
  pairs land differently depending on it.

### 4.8 **Stale gate status, in `task-sheet.md` and in my own definition file.**

`decisions/0064` closed the Step 7 gate on 2026-08-13 — *"Gate 4 of 5 is closed. Step 8 may launch."*
**[checked]** the string `0064` appears in `task-sheet.md` exactly once, inside a Step 8b
parenthetical. Everything else still reads as though the gate were open:

| Surface | What it says | Status |
| :--- | :--- | :--- |
| `task-sheet.md` Step 7 header | *"GATE. … **NOT approved; seven Red Team HOLDs.**"* | **stale** — `0064` records fifteen reviews and an unconditional approval |
| `task-sheet.md` Gate summary | Steps **5, 6 and 7 all unchecked** | **stale** — approved at `0021`, `0026`, `0064` |
| `.claude/agents/analytics-engineer.md` (mine) | *"The gate is OPEN and Step 8 does not launch until it closes."* | **stale** — same |

Per the read-back rules the on-disk files win over my definition; here the on-disk `task-sheet.md` is
**also** behind `decisions/`, so `decisions/0064` governs and the other two are propagation defects on
surfaces 1 and 4 (and, by the byte-identical-pair rule, presumably 5). **This does not change what I
did:** Step 8 is unapproved on its own account and this task is a read-back, not Step 8.

### 4.9 **`task-sheet.md` Step 0 still carries the superseded 403 rule.**

> Step 0: *"On a 403, hard stop and report. That is a block, not a throttle."*

`CLAUDE.md` — authoritative on API discipline — carries the classified rule amended 2026-08-10, and my
own definition file carries it correctly. **The task sheet does not.** No Step 8 consequence (Step 8
makes no calls), reported because the read-back rules ask for disagreements between surfaces.

### 4.10 **A stale file in `processed/` that a Step 8 implementer would reach for by name.**

**[checked]** `processed/step5/adopted_rule.json` publishes `"analysis_population": 215,258`,
`"removed": 4,849` and a 97.8% retention — **the revision-4/5 figures, superseded by the approved rule
that retains 201,900**. The file's name is the one an implementer told to "take the contamination
exclusion from Step 5" would open first. `processed/` is **not one of `CLAUDE.md`'s seven propagation
surfaces**, so the grep control cannot see this and never will.

### 4.11 Smaller ambiguities, listed rather than argued

- **Which contamination artifact is authoritative** — re-derive the rule, or read the stored flags?
  My definition says Step 5 is complete and must not be re-derived; `task-sheet.md` Step 8 says only
  "contamination exclusion (Step 5)".
- **Does D11 apply to the liveness evidence?** Position 6 tests **insertion** instants, but D11
  discards records by **`watched_at`**. A record with `watched_at ≥ τ_pull` was certainly inserted
  after every retained pair's `τ1` (D10 forces `τ1 ≤ 2026-05-12` at `W = 108`), so discarding it can
  flip a pair from live to not-live. **[checked]** 167 such in-frame records exist on 81 pairs. Both
  readings are defensible and the exclusion count depends on the choice.
- **"all Step 2 show fields"** is 60 columns in `frame.csv`, including derived ones
  (`size_quintile`, `pool_completers`, `cadence_boundary_distance_days`). "All" literally is a
  reading; "the fields Step 2 was asked to collect" is another.
- **`action` retained as a column** is required, but `action` is a **record-level** attribute and the
  table is **pair-level**. A set, a per-episode map, or a derived flag ("checkin-only",
  "manual-watch-only") are all constructible; Step 13's arm needs the third, and the spec asks for the
  column, not the shape.

---

## 5. What Step 8 names that has moved, been superseded, or no longer exists

| What Step 8 (or its inputs) names | Status | What it moved to, and where |
| :--- | :--- | :--- |
| *"a fixed documented order"* | **withdrawn** | the exact seven-position order (`0029` §3) |
| Outcome assignment **"at `τ1`"** | **superseded** | **two instants**: `\|A\| = 0` at `τ1`, Continued at `τ2` on `A_H` (`0034`) |
| **D3** | **superseded** | **D3′** — Started-and-left **at `τ2`**, on a `(W + 2H)`-cleared subset, per arm (`0034`). *`artifacts/step1-outcome-definition.md` §9's Step 8 handoff still says "the required resumption-rate report (D3)"* |
| *"no clock start precedes an S2 premiere"* | **vacuous, replaced** | the three-part clock-start check with the equality clause (D6) |
| `p = m / L2`, and `p = m_H / L2` | **withdrawn** | rank form on `A_H` (Step 1 §7, `0034`) |
| `date(watched_at) <= T1` | **withdrawn, must not be written** | half-open UTC instants, `watched_at < τ1` (D13, Step 1 §2.4) |
| The **liveness threshold** | **DELETED** | nothing. Derived three times — 632 d, then 1,293 d — and deleted at `0042`; the adopted rule is **parameter-free** (`0048`, approved `0064`). Step 8 never references it, and correctly |
| **604** liveness exclusions on APPLY | **superseded (ALT)** | **703** = 604 NS + 99 S&L, 216 accounts (`0048`, restored `0054`) |
| **793** liveness exclusions on APPLY | **withdrawn (ALT-MATCHED)** | **703** (`0054`). Producing 793 **is a divergence** |
| *"the exclusion set is empty on DERIV"* | **false, corrected in five files** | **99 on DERIV**, 73 accounts; decrease strict on both populations (`0049` §3 item 4) |
| *"`τ2` plays no part"* in liveness | **withdrawn** | the rule reads two instants; **silence** stays at `τ1` (`0049` §3 item 1, `0054`) |
| `[16.7146%, 16.9704%]`, and `[9.6830%, 10.0405%]`, and `9.6830%` anywhere | **superseded** | `[16.6633%, 16.9704%]` and `[9.6372%, 10.0405%]` on APPLY (`0047` §3, `0054`, `0056`). `9.6830` has **no legitimate reading under the adopted rule** and was removed from the false-positive register |
| **`W = 107`** and **`107.7135`** in the Step 6 artifacts | **superseded** | **`W = 108`**, from `0026`. Step 8 says take it from the decision entry, not the artifacts |
| Step 7 gate "OPEN" / "NOT approved" | **superseded** | **approved, `0064`** — §4.8 |
| Step 0 "403 → hard stop, always" in `task-sheet.md` | **superseded** | the classified rule in `CLAUDE.md` — §4.9 |

**One caution I would carry into any grep of my own output:** `632` is both the deleted liveness
threshold **and** the legitimate frozen-D10 never-started component at `W = 125` (`0051` §3, restated
at `0066` §2). A blind search for the deleted threshold produces a false positive there.

---

## 6. What I would have to decide myself in order to run this

**Listed, not resolved.** Each is a place two isolated instances can differ while both following the
written spec.

1. **The base population for waterfall line 1** (§4.1) — four candidates, 220,107 to 2,900,762.
2. **Whether D11 is applied when computing S1 completion** (§4.2) — 220,103 or 220,107 at line 3.
3. **Whether D11 is applied to the liveness evidence** (§4.11) — affects the 703.
4. **Whether the contamination exclusion is re-derived or read from Step 5's stored flags**, and if
   read, from which of the several `processed/step5/pair_*.csv` tables.
5. **Whether the analysis table is built once at `W = 108` or once per arm** (§4.3).
6. **The arm grid** — 38/46/77/91/107/108/150/213, or [37, 107], or "37 to 108" (§4.3).
7. **Whether "3,440" is restated or recomputed** (§4.4).
8. **The population for each of the seven required counts that does not name one** (§2) — D2's
   denominator, the two drop counts' position, D8's population, the discarded-record count's scope,
   the D12 bucket pair counts' position, the metadata-disagreement pair counts' position.
9. **Discovery channel as one column or two** (§4.7) — 324 dual-channel users.
10. **`p`'s representation for non-Started-and-left rows** (§4.7).
11. **`action`'s representation in a pair-level table** (§4.11).
12. **"all Step 2 show fields"** — literally all 60, or the fields Step 2 was asked to collect.
13. **Whether a clock-start invariant mismatch arising from a tie-break counts as a failure** (§3.5).
14. **What "treat a 703 mismatch as a population defect" obliges me to do** — diagnose and continue,
    or stop and report (§4.5). Step 8 is a gate, so I would stop; the spec does not say so.
15. **Whether the waterfall reports one chain or two** — APPLY only, or APPLY and DERIV side by side
    (§7.1).

---

## 7. What Step 8 does not ask for, that Step 9 and Step 8b will read out of my output

### 7.1 **DERIV.** Step 9 and Step 8b both require it on every bound. Step 8's seven filters do not produce it.

This is the one I would raise first.

**Step 8b** requires both bounds *"on APPLY (n = 196,654) **and** DERIV (n = 147,370)… separate
arithmetic, never one field with a population flag"*, plus the three-ceiling sum and excess **per
population**. **Step 9** publishes, on DERIV: never-started `[6.2055%, 6.2055%]` (degenerate),
started-and-left `[11.3015%, 11.4291%]`, Continued ceiling `82.4930%`, sum `100.1276%`.

**DERIV is Step 5 waterfall line 4 less D10** — that is, pairs restricted to *has S2 evidence* **and**
*`T0` not contaminated* **and** *completing record not post-dated*. **None of those three restrictions
is one of Step 8's seven filter positions.** Step 8 as written produces APPLY and only APPLY. Either
Step 9 rebuilds DERIV from the Step 5 tables itself — which is the population-mismatch problem `0064`
§4 already publishes as an open residual, reproduced one step later — or Step 8 must emit it, and
nothing tells me to.

**[checked]** the arithmetic Step 9 will need is consistent and reproduces exactly: on DERIV
`9,145 / 147,370 = 6.2055%`, `16,655 / 147,370 = 11.3015%`, `16,843 / 147,370 = 11.4291%`,
`121,570 / 147,370 = 82.4930%`, sum `100.1276%`, excess `188 = 99 + 89`. On APPLY
`33,373 / 196,654 = 16.9704%`, `18,952 / 196,654 = 9.6372%`, `19,745 / 196,654 = 10.0405%`,
`144,933 / 196,654 = 73.6995%`, sum `100.7104%`, excess `1,397 = 2 × 604 + 189`. **What is missing is
not the arithmetic. It is the row set on my side of the handoff.**

### 7.2 **D4 (S3-without-S2) has no count anywhere in Step 8.**

Step 9 must report the D4 bound *"alongside the liveness bound"* (Step 1 D4, `0062`), and Step 8b
requires a **schema slot** for it: *"D4 and D9 publish alongside and are never folded in."* **Step 8's
required-counts list includes D9 and not D4.** So does Step 1 §9's Step 8 handoff. The D4 signature —
a pair with S3-or-later episodes logged and no S2 episodes at all — is computable only from
episode-level history joined to the pair table, which is Step 8's object and nobody else's.

### 7.3 **The bound's scope qualifier is a Step 8-adjacent obligation with no Step 8 line.**

My own definition file and `0062` are explicit: *"Step 8 does not compute the bound, but it produces
the position-6 population the bound is stated on, so any table or note that carries the bound carries
the qualifier"* — **covering with respect to insertion-dormancy, exhaustively; open only across channel
classes (D4, D9).** `task-sheet.md` Step 8 contains no such line. If my waterfall or invariant report
names 196,654 as the population a bound is stated on, the qualifier must travel with it, and Step 8's
own text would not have told me that.

### 7.4 **The three outcome counts are never required as an output.**

Step 8 requires "sample size after each filter" and an invariant that the states "sum to the sample".
The three state counts themselves — the thing every downstream step reads — appear only implicitly.
Step 8b's schema wants **shares**, and shares are Step 9's; but the **counts** are position 7's and
nothing asks for them.

### 7.5 **Nothing carries the pairing that makes the headline honest.**

`0034` requires, wherever the split is reported, that **Continued is a 199-day statement while
never-started is a 108-day statement, and the two must never be described as measured alike.** The
filter waterfall is a table a reader will read as a single measurement at a single horizon. Step 8's
text does not require the horizon to be stated on it.

### 7.6 **Two smaller ones.**

- **Step 13's `action` arm** needs `checkin`-only and manual-`watch`-only *distinguishable*, not merely
  `action` "retained". §4.11.
- **Step 11** needs the channel split to survive to position 7 in whatever form it will actually cut
  on. §4.7.

---

## 8. What I did not do

- **I did not execute Step 8.** No table, no filters, no API calls, nothing written to `processed/`.
- **I did not fix anything.** `task-sheet.md`, the agent definition files and every decision entry are
  untouched, including the three stale gate-status lines in §4.8 and the stale Step 0 403 rule in
  §4.9, which I report rather than edit.
- **I did not read the other instance's output folder** and did not look for it.
- **I did not resolve any item in §6.** They are listed as the divergence surface they are.

---

**Status: read-back complete. Step 8 remains an unapproved gate and has not launched.**
