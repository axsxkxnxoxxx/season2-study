> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-14 by `decisions/0051`.

# Step 7 — Evaluation of Red Team's proposed alternative liveness rule (instance `a`)

**This is an evaluation. It adopts nothing.** The Step 7 gate is open (`decisions/0043`, `0044`) and
Step 8 has not launched. The other `data-scientist` arm ran the same brief in isolation; I have not
seen its output and have not looked for it. The Human Lead rules.

| | |
| :--- | :--- |
| **Approved rule (PF-LIMIT)** | not live **iff** the account shows no insertion instant after that pair's `τ1` |
| **Proposed alternative (ALT)** | not live **iff** (no insertion instant after `τ1`) **AND** (`\|A\| = 0`) |
| **Population** | Step 5 waterfall line 4 (152,126) less D10 right-censoring = **147,370** pairs, 2,402 accounts, 1,138 shows, at `W = 108`, `H = 91` |
| **API calls** | **0** |
| **Calibration** | `processed/step7/a4/distinct_instants.npz` read unchanged. Never refitted. |

---

## The finding that governs all four answers

> **ALT's exclusion set is EMPTY. It excludes 0 pairs at `W = 108`, and 0 pairs at all 20 values of
> `W` tested between 1 and 400. All 751 of PF-LIMIT's exclusions have `|A| ≥ 1`.**

| At `W = 108` | Excluded | Accounts | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **PF-LIMIT — approved** | **751** | 166 | **0** | **652** | 99 |
| **ALT — proposed** | **0** | 0 | 0 | 0 | 0 |
| *1,293 d threshold — deleted, context only* | *1,282* | *205* | *40* | *1,079* | *163* |

The context row reproduces `decisions/0043`'s **1,079 / 163 / 40** exactly, which is what tells us
where Red Team's estimate came from and why it does not transfer.

**Red Team's "on the order of 40 pairs" is read off the deleted rule.** Those 40 never-started
exclusions come entirely from the **measured-gap branch** — the gap test `decisions/0042` removed.
PF-LIMIT has no gap test. Its exclusion set is the open-ended bucket alone, and that bucket contains
**zero** never-started pairs.

### Why, and it is not a coincidence

`no_after` says every insertion instant on the account is at or before `τ1`. Every pair on waterfall
line 4 has S2 evidence by construction (line 2 requires it). So its S2 records were **written** at or
before `τ1`, and the only way a claimed `watched_at` can land past `τ1` is post-dating — which Step 5
adoption 3 (`decisions/0021`) deliberately declined to delete.

Measured on the 751:

| | Days |
| :--- | ---: |
| Headroom `τ1 −` earliest canonical S2 timestamp — **minimum** | **47.5** |
| — median | 107.4 |
| — 1st percentile | 98.8 |
| Pairs with headroom below 1 day | **0** |
| Pairs whose earliest S2 claim post-dates the account's last insertion instant | 16 of 751 |
| — largest such post-dating observed | +20.4 |

So the channel through which ALT could ever fire exists and is measurable at up to **20 days**, and it
would need **47 days** to reach the nearest pair. This is not a knife-edge.

### The one place it does fire, reported rather than buried

At **`W = 0`** ALT excludes 6 pairs. `W = 0` is not a tested arm and is degenerate under finale
anchoring — it scores 100,175 of 147,685 pairs never-started. Reported so the emptiness is presented
as an **empirical fact over a tested range, not as a theorem**.

Separately: **4 pairs on line 4 satisfy the ALT conjunction before D10 at every tested `W ≥ 1`**, and D10
removes all 4. Their `T0` is 2026-08-10 or 2026-08-11 — within a day of the pull instant — so they are
censoring-doomed for reasons that have nothing to do with liveness. D10 is technically load-bearing
for the zero; it is not load-bearing for the conclusion.

---

## Q1 — Is the stated obstacle real?

**No. There is no dependency. The ordering is a convention, and restating it changes no row set.**

1. `|A|` is a function of `E2`, the pair's canonical S2 timestamps, `T0` and `W`. **None of those is a
   function of the liveness mask.**
2. Liveness is a function of the account's insertion instants and `τ1`. **Neither is a function of
   `|A|`.**
3. Both are **row-local predicates** on the output of position 5. Two row-local predicates commute
   exactly, so the retained row set is identical whether ALT is evaluated at position 6 or after
   position 7.
4. **Position 7 is not a filter.** Outcome assignment *labels* rows; it does not drop them — the
   `L2 = 1` drop is position 2. An ordering constraint between a filter and a labelling step
   constrains only which is *computed* first, and computation order is free when neither reads the
   other's output.
5. **`0029`'s recorded rationale does not reach this case.** It says censoring is objective and
   independent of behaviour while liveness is a behavioural inference, so *"running the objective
   filter first means liveness's marginal cost is measured on a fully observable population."* That
   argument is about **censoring before liveness**. It says nothing about liveness before outcome
   assignment. Red Team's framing of its own obstacle is more cautious than the record requires.

**What genuinely does not commute** is the thing `0029` fixed the order for in the first place: the
**reported per-filter sample size**. Under ALT, waterfall line 6 becomes an outcome-conditional count,
and the spec must say so explicitly or two faithful instances will report it differently while
agreeing on every share.

---

## Q2 — What would it cost?

| Setting | Never started | Continued | Started and left | Pairs |
| :--- | ---: | ---: | ---: | ---: |
| No liveness filter | 6.2055% | 82.3655% | 11.4291% | 147,370 |
| **PF-LIMIT — approved** | **6.2373%** | **82.3427%** | **11.4201%** | 146,619 |
| **ALT — proposed** | **6.2055%** | **82.3655%** | **11.4291%** | **147,370** |
| *1,293 d — deleted* | *6.2325%* | *82.3497%* | *11.4178%* | *146,088* |

**ALT is numerically identical to no liveness filter at all**, to every decimal place, because its
exclusion set is empty.

**PF-LIMIT → ALT, paired account-clustered, B = 4,000:**

| | Delta | 95% CI | Excludes zero | As a share of the sampling width |
| :--- | ---: | :--- | :--- | ---: |
| Never started | **−0.0318 pp** | [−0.0464, −0.0204] | **yes** | 4.1% |
| Continued | +0.0228 pp | [−0.0076, +0.0619] | no | 1.8% |
| Started and left | +0.0090 pp | [−0.0171, +0.0315] | no | 0.9% |

Same shape as the finding that justified deleting the threshold: **detectable, not material.** The
never-started delta is distinguishable from zero only because the two settings are nested subsets of
the same pairs, which gives near-zero paired variance.

**PF-LIMIT's never-started effect is denominator-only.** The numerator is **9,145 under both** — the
filter removes no never-started pair. Its entire +0.0318 pp is the denominator falling by 751.
`decisions/0043`'s UP sign is confirmed, and its mechanism is now exact rather than inferred.

### Invariants and waterfall touched

| | PF-LIMIT | ALT |
| :--- | :--- | :--- |
| Step 8 waterfall line 6 | 147,370 → 146,619 (−751) | 147,370 → 147,370 (**0**) |
| Filter counts decrease monotonically | strict | **holds non-strictly only** |
| States mutually exclusive, sum to sample | unaffected | unaffected |
| `A ⊆ A_H` | unaffected | unaffected |
| D3′, D8, D9, per-air-period counts | shifted by the 751 | equal to the no-filter values |

**The monotone-decrease invariant is a concrete hazard.** An instance coding it as strict `<` fails
the assertion on a legitimate no-op. The spec must state non-strict.

### `W`-coupling — the column `decisions/0044` §1.2 requires

`H` held constant at 91 in every arm.

| `W` | 38 | 46 | 60 | 75 | 91 | **108** | 125 | 150 | 180 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **PF-LIMIT excluded** | 348 | 367 | 432 | 517 | 706 | **751** | 748 | 779 | 836 | **949** |
| **ALT excluded** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |
| Post-D10 population | 147,685 | 147,685 | 147,685 | 147,685 | 147,685 | 147,370 | 147,049 | 146,602 | 145,845 | 144,852 |

The PF-LIMIT row reproduces `0044`'s **348 / 432 / 706 / 751 / 779 / 949** exactly at the six arms that
entry publishes. **The dip at `W = 125` (748 < 751) is real and is D10, not the rule** — the population
shrinks faster than the open-ended bucket grows across that step.

**Under ALT the `W`-coupling vanishes**, because there is nothing to couple. That is a genuine
property, and it is also the loss described in Q4.

---

## Q3 — What does it do to the Step 9 bound?

The bound is the never-started share if every inactivity-excluded **pair** is treated as a decliner.

| Rule | Floor | Ceiling | Width | Ceiling 95% CI | Inflation as a multiple of the never-started sampling width |
| :--- | ---: | ---: | ---: | :--- | ---: |
| **PF-LIMIT** | 6.2373% | **6.7151%** | **0.4778 pp** | [6.2885, 7.1618] | **0.62×** |
| **ALT** | 6.2055% | 6.2055% | **0.0000 pp** | [5.8409, 6.6035] | 0.00× |
| *1,293 d — deleted* | *6.2325%* | *7.0482%* | *0.8157 pp* | *[6.6002, 7.5194]* | *1.06×* |

**Under PF-LIMIT the bound does not bound the quantity it claims to.** Of its 751 pairs, **751 carry
positive S2 evidence at `τ1`** and **652 are confirmed continuers**. Zero are never-started. Treating
a confirmed continuer as a decliner is an arithmetic operation on a set chosen for a reason unrelated
to the uncertainty being bounded, and it inflates the headline by **0.62× the clustered sampling width
of the share it is a bound on** — not a rounding artefact.

**Under ALT the bound is exactly right and exactly nil.** Every excluded pair would by construction be
a `|A| = 0` pair, so returning it as a decliner is the correct maximal reading; there are none, so the
ceiling equals the floor. **It bounds the right quantity and the quantity is zero.**

### A correction the ruling needs

`decisions/0043` §1.2 states *"roughly six in seven of the 751 have positive S2 evidence"* and offers
the remedy *"or compute it on the ~40 never-started exclusions instead."*

- **Seven in seven** of the 751 have positive S2 evidence. Six in seven (652, 86.8%) are confirmed
  *continuers* — the two claims were merged.
- **The remedy cannot be executed.** The approved rule's never-started exclusion count is **0**, not
  ~40. The 40 belong to the deleted 1,293-day rule's measured-gap branch.

This is the same error class `0043` §2 itself logs as the sixth instance — **a figure measured on one
configuration quoted as if measured on another.** This is the seventh, and it sits inside the entry
that exists to correct the sixth.

---

## Q4 — What breaks?

### Against ALT

- **It does not supply the missing warrant.** Red Team's open item 2 is that the not-live branch has
  no warrant from `0021`, which licenses only the *sufficient* condition "insertion after `τ1` →
  live." **ALT empties the branch; it does not warrant it.** The frame is a stopped pull (2,549 of
  4,050 users); if it resumes, the branch can become non-empty and the gap returns unresolved.
- **Its direction is true by construction, not by measurement.** ALT's exclusion set is a subset of
  Never-started, so it can only move the share DOWN. That restores the ledger's original sign — but
  the conservative-direction argument `0040` §3 withdrew comes back as a **tautology**, with the
  direction built into the rule rather than found in the data. Step 14 must say so, or it republishes
  a withdrawn argument in a new form.
- **A filter that excludes nothing cannot be shown to be working.** PF-LIMIT's 751 exclusions are at
  least auditable. ALT's zero is consistent both with "no account silence corrupts any null" and with
  "the rule is mis-specified and never fires." Only the margin diagnostic in this document separates
  those two, and **no step currently requires it**.
- **It zeroes the column `0044` §1.2 added.** That entry made Step 13 report the exclusion count per
  `W` arm so the coupling is visible in the output rather than only in the log. Under ALT the column
  is zeros at every arm. The coupling genuinely vanishes — but a reader comparing against `0044`'s
  348–949 table must be told why, or the zeros read as a bug.
- **It complicates an order that has already been fixed once.** Row sets commute, but position 6 would
  read a quantity produced at position 7 and the documented chain stops being linear. `0029` fixed the
  order precisely because the per-filter sample size does not commute; three gate reruns have gone to
  defects of this class.
- **Dual-implementation exposure.** ALT needs the spec to state (i) that waterfall line 6 is
  outcome-conditional, (ii) that the monotone-decrease invariant is non-strict, and (iii) which
  reading of `|A| = 0` is meant. Absent any of the three, two faithful instances diverge on the
  waterfall while agreeing on every share — the exact failure `0029` §3 exists to prevent.

### Against PF-LIMIT

- Its analysis population has **652 confirmed continuers deleted for a reason unrelated to
  continuing**. The published Continued share then sits on a denominator from which known continuers
  were removed by a behavioural inference that could not have been wrong about them.
- Its Step 9 bound inflates never-started by **0.4778 pp, 0.62× the sampling width**, entirely out of
  pairs with positive S2 evidence.
- Its never-started effect is denominator-only, so **it protects the null it exists to protect on not
  one pair in this population**.

### What ALT damages that PF-LIMIT does not

**Nothing measurable.** On this population ALT is a strict no-op, so every count, share, invariant and
downstream diagnostic equals the no-liveness-filter value. Every cost listed above is a cost to the
**specification and to what the study may claim**, not to any number.

---

## Judgement calls

1. **Reading of `|A| = 0`.** Taken as Step 1 §7's Never-started condition — the set `A` at `τ1` —
   because Red Team's framing invokes the outcome and the filter-order position of outcome assignment.
   The competing reading, "the pair has no S2 evidence at all in the record," gives a **different
   set**: 4 line-4 pairs have no distinct in-`E2` S2 episode at any bound, against 9,145 with
   `|A| = 0` at `τ1`. **If the Human Lead means the second reading, the numbers here do not apply.**
2. **`W` arms.** `0027`'s span plus 150 and 213, with 38, 91 and 108 added so the table lines up with
   `0044`'s, plus a fine sweep 0–400 to test for a knife-edge. `H` held constant at 91 throughout.
3. **`W = 0` reported but treated as out of scope**, with its 6 exclusions stated rather than dropped.
4. **Floor and ceiling.** Floor read as the rule's own point estimate; ceiling as every excluded pair
   returned to the denominator and counted never-started. The task sheet names the ceiling explicitly
   and leaves the floor implicit.
5. **Bootstrap design copied, not re-designed.** B = 4,000, seed 20260813, resampling the 2,402
   accounts — identical to the gate-closing run so the rows are comparable. **This is deliberately not
   an independent design choice, and these intervals therefore corroborate nothing about the interval
   method.**
6. **Outcomes computed for all rows before either filter.** Necessary to report the exclusion sets'
   composition at all, since PF-LIMIT deletes pairs before outcome assignment. Legitimate because
   outcome assignment is row-local — and it is the same computation Q1 is about.
7. **States recomputed, not read from cache**, and asserted equal to the cached `pair_states`, so this
   run does not inherit an error from the earlier one.
8. **`no_after` computed in closed form** (account's last insertion instant `≤ τ1`) and asserted equal
   to the cached `searchsorted` result at `W = 108` on all 152,126 line-4 rows.
9. **No 91-day arm.** Step 9's second headline has a separate origin (D5) and is a Step 9 deliverable;
   Step 8 has not launched.
10. **These shares are provisional in population as well as in status** (`0042` §5). Step 8 applies
    liveness to the analysis population less D10 — 196,654 — a strict superset carrying contaminated
    `T0`. The absolute levels will move. The emptiness finding rests on a mechanism, not a level.

---

## Recommendation — stated as a recommendation. Nothing here is adopted.

**1. The alternative's diagnosis is correct and its remedy is null.** ALT excludes 0 pairs at all 20
tested values of `W` between 1 and 400, so adopting it is numerically identical to deleting the
liveness filter. **I
recommend adopting ALT rather than deleting the filter**, on one ground: the frame is a stopped pull,
and a stated rule that currently fires on nothing survives the frame growing, whereas a deleted filter
does not. **If it is adopted, the artifact must say in plain words that it excludes zero pairs on this
data.** A reader told "a liveness filter was applied" would otherwise be misled, and that is the same
misdescription `0044` §1.1 withdrew "no free parameter" for.

**2. Independent of which rule is chosen: the Step 9 liveness bound should not be published in its
current form.** Under PF-LIMIT it adds 751 pairs — 652 confirmed continuers, zero never-started — to
the never-started numerator, inflating the share by 0.4778 pp, 0.62× its own sampling width.
`decisions/0043` already called it *"meaningless, not merely uninformative"*; the measurement here is
that **the set it bounds contains zero pairs of the kind it claims to bound**, and that `0043`'s own
remedy cannot be executed because the count is 0 rather than ~40.

**3. Red Team's item 2 stays open under either rule.**

---

## Files

| | |
| :--- | :--- |
| This document | `artifacts/step7-alt-rule-a.md` |
| Machine-readable, all evidence inlined | `artifacts/step7-alt-rule-a.json` |
| Row-level intermediates | `processed/step7/alt_a/` |
| Scripts | `src/step7_alt_a_1_core.py`, `_2a_episodes.py`, `_2b_arms.py`, `_3_margins.py`, `_3b_d10.py`, `_4_boot.py`, `_5_deliver.py` |

Counts and aggregates only in `artifacts/`. No usernames, user IDs or individual watch histories.
