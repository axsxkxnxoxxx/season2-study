---
name: glossary-terms-and-thresholds
description: Live glossary of every term, threshold and constant in the Season 2 abandonment study, each tagged with the step, decision and gate that fixed it and which population its figures are on — current through decisions/0050 and the Step 7 ALT-BROAD rule (2026-08-14)
metadata:
  type: reference
---

# Glossary — terms, thresholds, and where each was set

**Current through `decisions/0050`, 2026-08-14** — Steps 3, 4, 2, 5, 6, the Step 1 §7 amendment, and
the Step 7 liveness gate (still OPEN). This is an index, not a substitute for the artifacts. Verify
against the file before acting on any row.

Status vocabulary: **FIXED** (set and gate closed) · **DEFERRED** (form fixed, value owed)
· **OPEN** (gate has not run) · **PROPOSED** (agent produced it, gate not approved).

> **Standing rule since `0046` §0, and it governs this file: EVERY FIGURE STATES WHICH POPULATION
> PRODUCED IT, at the point of use.** Extended by `0047` §3 to interval endpoints: *an endpoint
> states the population it is computed on and the estimand it bounds, and they must be the same
> population.* Both rules exist because the study broke them repeatedly — see
> [[gate-step7-liveness]].

## The five items the Human Lead named as glossary-critical

| Term | Value / status | Where set | Gate |
| :--- | :--- | :--- | :--- |
| **`W`** — the window, in days | **FIXED: `W = 108 days`.** The **ceiling** of the **90th percentile** (107.7135) of the **continuous** lag from clock start to first S2 episode, on the **C1 subset (25,120 pairs, 206 shows, 2,050 users)** of the 128,099 clean-record sample. **Applies to all pairs.** Precision: **±18 days, show-clustered** — not the decimals. **Since `0034`, `W` no longer assigns every outcome state on its own**: `τ1` assigns never-started, `τ2 = τ1 + H` assigns Continued. **Precision history: 107 (`-a`, floored) → 107.7135 (`-b`, raw) → 108 (adopted ceiling).** Neither artifact figure is the adopted value; both predate `0025`. | Rule: `0024` (percentile) + `0025` (unit and ceiling). Value: `0026`. Propagated into Steps 7, 8, 13 and both Step 6 artifacts by `0029` | **Step 6 gate, APPROVED 2026-08-12, `0026`. Gate 3 of 5** |
| **Liveness rule** | **THERE IS NO THRESHOLD. The rule is ALT-BROAD:** *a pair is **not live iff BOTH** the account shows **no insertion instant after that pair's `τ1`** AND the pair is **NOT Continued**.* A numeric threshold was derived three times (632 d, 1,293 d) and **DELETED at `0042`** — the headline could not distinguish 787 from 2,200 days. **No parameter of its own; FULLY DETERMINED BY `W`** (`0044` — "no free parameter" is withdrawn). Basis unchanged: **insertion time**, not claimed `watched_at` (`0021` ruling 2); stored play-`id` calibration a required input that **neither instance refits** (`0022`, `0029`); **pair-level, never a wholesale user drop** (`0034`). **The SILENCE test is anchored at `τ1` and only there; the Continued conjunct is read at `τ2`** (`0049` — *"`τ2` plays no part"* is withdrawn). **Do not reintroduce a pre-`τ1` requirement in any form — withdrawn twice** (`0040` §1, `0042` §3), both for contradicting gate `0021` | Rule `0048`; deletion `0042`; coupling `0044`; corrections `0043`, `0045`, `0046`, `0047`, `0049`, `0050` | **Step 7 gate, still OPEN.** Approved twice (`0039`, `0042`) and reopened twice. **Step 8 has not launched** |
| **S1 completion rule** | **FIXED.** `F1 ∈ D1` **and** `\|D1\| ≥ ceil(0.90 × L1)`, distinct episodes, membership by the listed set `E1`. Now applied against **real** `E1` from the Step 2 frame, not a proxy (`0019`). | Step 1 §4 | **Step 1 gate, APPROVED 2026-08-10** |
| **Contamination exclusion rule** | **FIXED.** Exclude **16,665** pairs whose S2 evidence is *entirely* air-date-stamped, plus **1,542** with no S2 evidence and a fabricated binding clock start. Total **18,207**; retains **201,900 of 220,107 (91.73%)**. Disjoint by construction. | Step 5 §9, revision 6 | **Step 5 gate, APPROVED 2026-08-12, `0021`. Gate 2 of 5** |
| **Filter order** | **FIXED by `0029`, ahead of the gate.** **1.** Step 2 frame → **2.** `L2 = 1` exclusion → **3.** S1 completion rule → **4.** contamination exclusion → **5.** right-censoring → **6.** liveness rule → **7.** outcome assignment **at two instants** (`\|A\| = 0` at `τ1`, Continued at `τ2`, per `0034`). **Why it had to be fixed:** the final row set commutes — every filter is row-wise — but the **required per-filter sample size does not**, so two faithful instances could report different waterfalls on an identical table and the diff could not tell that from a bug. **Contamination before right-censoring** was already required. **Right-censoring before liveness** is the one genuine choice: censoring is a property of the clock and `pull_date`, objective and behaviour-independent, so running it first measures liveness's marginal cost on a fully observable population — the number Step 9's bound needs. **Since ALT-BROAD, waterfall line 6 is OUTCOME-CONDITIONAL and must be reported as such** — the Continued test is evaluated before liveness applies. **That is permitted, and both arms proved it independently:** the two are **row-local predicates on the position-5 output and commute exactly**, and `0029`'s rationale concerns per-filter **sample size**, which cannot reach position 7 because **outcome assignment removes no rows** — positions 1–6 are filters, **position 7 is an annotation** contributing no waterfall line. **The monotone invariant is coded `>=`, not `>`** (`0047`, reason corrected by `0049`): decrease is **strict on both populations under ALT-BROAD**, and `>=` is kept anyway **so the invariant does not encode a property of one rule**. **Expect 703 at position 6; treat a mismatch as a POPULATION defect before an implementation one** — Step 7 built APPLY from the Step 5 pair table, not through positions 1–5. **Producing 604 means the withdrawn ALT was implemented, and that IS a divergence.** | `0029`; liveness spec `0046`–`0050`, written into `task-sheet.md` Step 8 | Step 8 gate, **still not approved** — the order is fixed, the gate is not. **Step 8 has never launched** |

## Step 7 — the liveness vocabulary. Gate OPEN. Full arc in [[gate-step7-liveness]]

### The candidate rules, and the status of each

| Name | Rule | Status |
| :--- | :--- | :--- |
| **ALT-BROAD** | not live iff **no insertion after `τ1`** AND **NOT Continued** | **ADOPTED, `0048`, 2026-08-14.** Gate still open pending Red Team |
| **ALT** | not live iff no insertion after `τ1` AND **`\|A\| = 0`** | **SUPERSEDED** by `0048`. Guarded one null of two |
| **PF-LIMIT** | not live iff **no insertion after `τ1`** (alone) | **SUPERSEDED** by `0046`. Deleted 751 pairs with no stated warrant |
| **ALT-MATCHED** | one silence test per null, at the instant that null is read | **RECORDED, NOT ADOPTED** (`0050` §4). The form that would close the residual 297-pair channel. Never cite it as the rule; never drop it from the record |
| *PF-BRACKET* | instant at or before `τ1` **and** one after — the literal reading of `0041` §4's withdrawn wording | **Never a candidate.** Priced at 18,903 exclusions from 1,434 of 2,402 accounts, to show what the wording cost |

**"NOT Continued" means Step 1 §7 as amended by `0034`** — the negation of
`|A| ≥ 1 ∧ F2 ∈ A_H ∧ |A_H| ≥ ceil(0.90 × L2)` — so it covers **both** Never started and
Started-and-left. **`|A| = 0` alone is the superseded ALT form.** And `|A| = 0` is §7's Never-started
condition, **not** "no S2 evidence at all" — the competing reading selects a different set.

### The two populations, named once and used everywhere (`0046` §0)

| Name | Definition | Pairs | Who reads it |
| :--- | :--- | ---: | :--- |
| **DERIV** | Step 5 waterfall **line 4 (152,126) less D10**. **Requires S2 evidence** | **147,370** | Step 7 derives here |
| **APPLY** | **line 1 (201,900) less D10**. **What Step 8 filters at position 6** | **196,654** | Step 8, Step 9, Step 13 |

**Exclusions under ALT-BROAD at `W = 108`: 99 on DERIV (73 accounts) · 703 on APPLY (216 accounts) =
604 never-started + 99 started-and-left.** Per-arm on APPLY, D10 **re-derived** at each arm:
**537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** at `W` = 38/46/77/91/107/108/150/213 — factor 1.61.
**S&L component separately: 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148 — factor 2.85, growing faster
than the rule itself.** On DERIV the top arm is **147, not 148**.

**Superseded counts, never to be restated as current:** PF-LIMIT's **751** (DERIV) and **1,355**
(APPLY); ALT's **604** total and **0 on DERIV**; ALT's per-arm **485 → 716**. *(Under ALT-BROAD, 604
survives only as the never-started **component** of 703.)*

### The bounds — Step 9, both on APPLY, both endpoints on 196,654

| Bound | Interval | Width | Over |
| :--- | :--- | ---: | :--- |
| **Never-started** | **[16.6633%, 16.9704%]** | **0.3071 pp** | the **604** never-started exclusions only |
| **Started-and-left** | **[9.6830%, 10.0405%]** | **0.3575 pp** | **ALL 703** exclusions |
| *conditional sub-interval* | *[9.6830%, 9.7333%]* | *0.0503 pp* | *the 99 only — **NOT A BOUND*** |

**The never-started ceiling equals the unfiltered share as an identity** — but **by the route
`0049` corrected:** it returns **only the 604** to the never-started count, **not** every excluded
pair. *"Returning every excluded pair as a decliner"* gives an **unattainable 17.3279%**, because the
99 have `|A| ≥ 1` observed. **ALT-BROAD's exclusion set is no longer a subset of never-started, which
is why the route matters.** Both endpoints attainable, verified in **integer** arithmetic.

**The 99-only interval is a LABELLED CONDITIONAL SUB-INTERVAL and must never be recorded as a bound.**
It is conditional on every never-started exclusion being truly never-started; **the 604 rest on an
untrusted `|A| = 0` and some may in truth have left.** The two differ by a **factor of seven**. Both
arms reached this independently and **both refused to adopt it themselves** — it would have been the
**fourth consecutive bound** with an endpoint outside the feasible set.

**Superseded bounds, retained only as history:** `0045`'s **[16.7789%, 17.0355%]** (PF-LIMIT, mixed
denominators, floor was not a floor) and `0046`'s **[16.7146%, 16.9704%]** (mixed denominators, floor
0.0513 pp above the case liveness guards against). The internally consistent PF-LIMIT interval was
[16.727%, 17.0355%].

**The bound is DEGENERATE on DERIV — [6.2055%, 6.2055%] — so the dual control is `x = x` there**
(`0050` §3). **The two ceilings cannot both hold:** 16.9704 + 10.0405 + 73.6537 = **100.66%**. They
are **alternative worst cases over the same 604 pairs, not simultaneous ones.**

### Shares and movements — APPLY, under ALT-BROAD, at `W = 108`

**16.7231 / 73.5592 / 9.7177**, summing to 100.0000. Movement against no filter: **−0.2474 / +0.2630
/ −0.0156 pp**, summing to zero. On DERIV: **+0.0042 / +0.0554 / −0.0595 pp**.

**Step 14 bias 2 is UP on DERIV and DOWN on APPLY, and the published direction is APPLY's.** The sign
is **population-scoped and both directions must be carried** (`0045` §4.1). Mechanism of the DERIV UP:
line 4 requires S2 evidence, so the 604 never-started pairs with no S2 record anywhere exist **only**
on APPLY, and excluding them is what pulls the share down there.

### Deleted thresholds — never to be quoted as operative

**4 days · 504 · 632 · 914 · 1,293.** Also 787, 790, 975, 2,200 and the interval [528, 787] as
threshold quantities. **Watch for a collision: `632` also appears legitimately as the frozen-D10
never-started COMPONENT at `W = 125`** (`0050` defect 5) — a different quantity that happens to equal
the deleted threshold. Frozen-D10 **totals** are 746 / 823 / 918 / 1,117 at `W` = 125/150/180/213, of
which **632 / 684 / 753 / 881 is the never-started component**; **125 and 180 are not in the mandated
grid**, so only 684 and 881 are comparable to it.

### Withdrawn claims that must not reappear as operative

*"no free parameter"* (`0044`) · *"`τ2` plays no part"* (`0049`) · *"the exclusion set is empty on
DERIV"* (`0049`, false in five files) · *"every liveness exclusion is never-started"* (`0050`) ·
*"751 directly observed"* (`0048` — **652 observed, 99 null-based**) · *"the 604 are exactly the
pairs with no S2 record anywhere"* (`0047` — **subset, not equality**: APPLY holds 23,260 such pairs
and 22,656 stay live) · *"the DERIV zero is forced by construction"* (`0047` — a **fact of the filter
order and this pull date**, not a theorem) · *"one ordinary gap in a hundred"* (`0037` — length bias)
· the **invariance** of the gap-test/edge-case split (`0039` — arithmetically impossible).

**Decomposition, ALT-BROAD:** APPLY **196,654 → 52,514 (¬Continued) → 703**. *(ALT's
196,654 → 33,373 → 604 is superseded and must not be implemented.)* **Conjunct 1 does most of the
work**, which is why the count moves with `W` at all.

## Decision numbering on the public record — `decisions/`

`0001` Step 1 gate · `0002` Step 4 endpoint (D15) · `0003` W estimation sample (D14) · `0004` 403
handling · `0005` Step 3 stopping rule · `0006` Step 3 crawl constants · `0007` Step 3 channel cost
· `0008` Step 3 seed source · `0009` Step 4 pull order · `0010` Step 4 tail cap · `0011` `pull_date`
· `0012` sweep completeness · `0013` Step 2 delegation · `0014` no content filters · `0015` unaired
S2 · `0016` per-season network dropped · `0017` air period · `0018` size quintile base · `0019`
`pool_completers` recomputed · `0020` structural thresholds · **`0021` Step 5 gate APPROVED** ·
**`0022` the two Step 5 rulings written into `task-sheet.md`** · **`0023` `0012` upheld after a Red
Team HOLD** · **`0024` `W` is the 90th percentile** · **`0025` lag unit and ceiling** · **`0026`
Step 6 gate APPROVED, `W = 108`** · **`0027` Step 13 arms at 150 and 213** · **`0028` Step 14
carries every routed limitation** · **`0029` `W` propagated, Step 7 threshold rule, Step 8 filter
order** · **`0030` 2025 cutoff kept + three frame field changes** · **`0031` the ≥50 floor
justified** · **`0032` Step 4 deliverables regenerated** · **`0033` Step 8 per-air-period censoring
counts** · **`0034` Step 1 §7 amended — Continued at `τ2`** · **`0035` agent definitions are live
spec, amended; Step 10 receives `0034`** · **`0036` Step 7 threshold at the 99th + the bracketing-gap
shape** · **`0037` `0036` §1's basis withdrawn; gap unit; namespaces** · **`0038` Step 7 spec frozen
— reference 152,126, one gap per pair** · **`0039` Step 7 APPROVED at 632 d — LATER SUSPENDED** ·
**`0040` gate REOPENED on Red Team HOLD; `0021` reinstated; the 18,250 returned** · **`0041`
extended reference set, provisional; no threshold approved** · **`0042` Step 7 APPROVED, threshold
DELETED, PF-LIMIT** · **`0043` bias-2 sign corrected DOWN→UP** · **`0044` "no free parameter"
withdrawn; fully determined by `W`** · **`0045` Option C bound; ALT rejected — rejection later
withdrawn** · **`0046` ALT ADOPTED; `0045`'s rejection withdrawn; the population rule** · **`0047`
`0046` §1/§4/§7 corrected; D10 re-derived per arm; `>=`** · **`0048` ALT-BROAD ADOPTED** · **`0049`
joint S&L bound; six record defects; calibration residual discharged** · **`0050` six file defects
fixed and verified; limits routed to Step 14; channel measured at 297 pairs**.

**Authority split.** `0001–0004` and `0009–0050` are Human Lead. **`0005–0008` are agent-taken and
still Open, awaiting ratification.** **`0029` and `0041` are the only non-Closed entries** — `0029`
was Open on the Step 7 percentile (**now moot: the percentile was ruled at `0036` and the whole
threshold deleted at `0042`**, so `0029`'s open clause has been overtaken rather than closed);
`0041` is Open by its own status line.

**Two index defects in `decisions/README.md` as of 2026-08-14:** it carries **no row for `0050`**,
and its authority note still reads **"0001–0004 and 0013–0033."** See
[[open-items-and-contradictions]].

## Step 6 — how `W` is derived, and the conventions inside it

| Term | Value / rule | Where |
| :--- | :--- | :--- |
| **The percentile** | **90th.** *"Attribution-window practice sets the window at or slightly above the 90th percentile of the time-to-conversion distribution, with 75th to 90th the cited range."* **Imported convention, not selected by the data**, and labelled as such wherever it appears. Moving to the 85th buys **61.7 days** (46 vs 107.7) | `0024` |
| **The withdrawn wording** | ~~"set W at the percentile where the curve flattens"~~ — **withdrawn.** The C1 density is close to scale-free past day 7 (log-log slope −1.1 to −1.5 across every decade), so the spec asked for a feature the distribution does not have | `0024` |
| **The lag** | **Continuous instant difference**, signed and untruncated. Not floored to whole days | `0025` |
| **The rendering** | **`W` is the CEILING of the percentile.** A pair is covered iff its fractional lag is `< W`, so flooring is a **systematic one-directional off-by-one against the operator**. 107 covers 89.976%, 108 covers 90.020% | `0025` |
| **Applies wherever the shape recurs** | Any later step reading a percentile off a lag or duration and feeding it into a half-open instant test inherits the same off-by-one. **`0025` names Step 7's liveness threshold as the immediate candidate** | `0025` |
| **C1 estimation subset** | **25,120 pairs = C1 ∩ 128,099**, 19.6% of the sample, from **206 shows and 2,050 users** | `0026` |
| **`W`'s precision** | **±18 days at 95%, show-clustered.** iid ±8 is wrong — 206 shows is the binding cluster, and treating pairs as independent overstates precision ~2.5× | `0026` |
| **All-shows p90** | **37.6967 → 38** under the ceiling rule. **Descriptive only; `W` is never read here.** The 70.0-day gap between the two curves is the measured size of D14's transfer assumption | `0026` |
| **Step 13 `W` arms** | Union of the two-curve range **[38, 108]**, the run-1 span **[46, 107]**, and the new arms at **150 and 213** — effectively **38 to 213**, with 108 inside rather than at the ceiling. **`H` constant across every arm; each arm re-censors, so the arms do NOT share a denominator** and the retained-row count is required per arm | `0027`, composing with `0024` |
| **`213`** | The C1 p90 among pairs with **≥8 years of exposure** (n = 4,141). **An upper bound, not a rival estimate** — exposure and cohort are not separable | `0026`, `0027` |

## Clock, window, horizon — TWO boundaries since `0034`

| Symbol | Definition | Where | Status |
| :--- | :--- | :--- | :--- |
| `T0` | `max(S2_finale_air_date, first-pass S1_completion_date)`. **Carries a behavioural term:** the `S1_completion_date` arm binds on **116,041 of 220,107 pairs — 52.7%** (`processed/step5/t0_binding.json`). Any claim that `T0` is exogenous is false and was withdrawn twice | Step 1 §6, D1; binding counts via `0034` | FIXED |
| `⟦T0⟧` | The **UTC midnight of the date** of `T0`. `τ0 = ⟦T0⟧` | §2.4, D13 | FIXED |
| **`τ1`** | **`⟦T0⟧ + W × 24h` = `⟦T0⟧ + 108 days`.** Assigns **never started** (`\|A\| = 0`); is the **liveness SILENCE anchor** and the **only** instant the silence test reads | §2.4, D13; value `0026`; anchor role `0034` | **FIXED** |
| **`τ2`** | **`⟦T0⟧ + (W + H) × 24h` = `⟦T0⟧ + 199 days`** at `W = 108`, `H = 91`. Assigns **Continued**. Moves with `W` automatically — at the `W = 213` arm, `τ2 = ⟦T0⟧ + 304 days`, exactly the clearance `0027` already priced. **Since `0048` it is also read by the liveness rule's second conjunct** | Step 1 §7 as amended; `0034`; liveness role `0048`, `0049` | **FIXED** |
| **The liveness rule reads TWO instants** | **Silence at `τ1`, Continued at `τ2`.** *"`τ2` plays no part"* is **WITHDRAWN** (`0049` defect 1) — it was true of PF-LIMIT and is false of ALT-BROAD, whose second conjunct **is** the Continued test. **What survives, and is what the withdrawn line meant: the SILENCE test is anchored at `τ1` and only there.** Since `τ2 > τ1`, ALT-BROAD at `τ1` is **strictly narrower** than a `τ2`-matched form — the conservative version, introducing no new anchor | `0048` §3(b), `0049` | **FIXED** |
| **`A`** | Distinct S2 episodes with `number ∈ E2` and `watched_at < τ1`, over `(−∞, τ1)` — **one-sided, no lower bound** | Step 1 §7 | FIXED |
| **`A_H`** | **`A` recomputed with the bound moved from `τ1` to `τ2`** — the set **D3 already defined**, which is why the amendment introduces no new object. **`A ⊆ A_H` by construction** since `τ1 < τ2`, so the amendment is **monotone**: pairs move Started-and-left → Continued only, never back. Asserted at Step 8 **as a code check, not a data check** — being true by construction it can only catch an implementation that computed the two sets wrongly, and a green assertion is not evidence for the rule | D3's original text; promoted to the operator by `0034` | **FIXED** |
| In-window test | **`watched_at < τ1`** (and `< τ2` for `A_H`). Strict, half-open, instants only, on both boundaries | §2.4, D13 | FIXED |
| `H` | **91 days**, fixed, **not a function of `W`**, held constant across every Step 13 arm. Adopted **by name** at the Step 1 approval (D10) — which is why `τ2` introduces **no new constant**. **`H` loses the comparison it is measured against by 10 days:** the marginal p90 (first S2 episode → completion) is **100.39**, i.e. **101 under `0025`'s ceiling, against 91**. The shortfall is not argued away — it is exactly what item 9's 3,440 residual counts | §6, D10; marginal p90 from `src/step6_completion_lag.py` | FIXED |
| Right-censoring | retain iff **`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`**. **This is exactly `τ2` at `W = 108`**, so every retained pair already has `A_H` fully observed and the amendment's censoring cost is **zero**. Holds at **every** arm, because `W + H ≤ max(W, 91) + H` is an identity | §6, D10; identity in `0034` §3 | FIXED in form |
| **`m_H`** | **`max(A_H)`.** Step 10's abandonment point is the **rank form** `p = \|{ e ∈ E2 : e ≤ m_H }\| / L2`, `m` replaced by `m_H` and nothing else changed. **`p = m_H / L2` is NOT the rule** — the raw-ratio form stays withdrawn (`L2` is a count, `m` an episode number; with an `E2` gap it can exceed 1). `p` is defined **only on Started-and-left**, which is now assigned on `A_H` | Step 1 §Abandonment point as amended; `0034` | **FIXED** |
| **D8(ii)** | The count and share of pairs **satisfying the Continued condition** — `F2 ∈ A_H` and `\|A_H\| ≥ ceil(0.90 × L2)` — with `\|A\| = 0`. Already required by the approved text, so **D8 needed no amendment**; what changed is that it is now **the only bound on the never-started boundary**. Size: **1,575 on the estimation sample, 1,573 after right-censoring**, against 8,449 scored Never started. **The count is a FLOOR and the 18.64% share is a CEILING** — different populations, never combined | Step 1 D8; sized by `0034` §6.1, routed as ledger item 10 | FIXED |
| **D3′** | Replaces **D3**, which measured nothing once its quantity became the operator. *Of pairs scored Started-and-left **at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, report the **share** completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its **share of all Started-and-left**.* **Runs at EVERY Step 13 arm** — the clearance contains `W`, so the cleared set shrinks 95.98% (`W = 46`) → 94.82% (108) → 91.34% (213), and shows absent from the subset run 5 → 9 → 18. **Reported alongside, labelled a COUNT and not a rate:** the 3,440 completing at any point before `τ_pull`, with its exposure-weighting by show recency stated at the point of use. **The two do NOT bracket the quantity** — both truncate observation and neither is a lower bound | `0034` §6.4, written into `task-sheet.md` Step 8 | **FIXED** |
| **`pull_date` / `τ_pull`** | **`pull_date = 2026-08-11`, `τ_pull = 2026-08-11T00:00:00Z`.** Every record with `watched_at ≥ τ_pull` is discarded. | **`0011`, Human Lead 2026-08-11** | **FIXED — D11's deferred value is now closed** |

`0011`'s constraint check: earliest per-user fetch instant **2026-08-11T05:01:26Z ≥ τ_pull** ✓.
Consequence carried in `0011`: the discarded tail is ~1 day for early-fetched users and ~2 for
late-fetched ones, so **the discarded-record count is not evenly distributed across the pool.**

## Step 2 frame — the population every result is computed on

**Owner Human Lead, execution delegated to an agent under `0013`.** Artifact:
`artifacts/step2-frame-ledger-and-distributions.md`.

**Frame: 1,138 shows, 220,107 S1-completer pairs.** Candidate set 2,094 shows (≥50 completers).
Exclusion ledger, in the order the rules were written:

| # | Rule | Removed | Remaining |
| :-- | :--- | ---: | ---: |
| 0 | Candidate set, ≥50 S1 completers | — | 2,094 |
| 3 | No real season 2 | 796 | 1,298 |
| 4 | S2 listed but unaired (`aired_episodes = 0`) — **`0015`** | 12 | 1,286 |
| 5 | S2 finale aired after 2025-12-31 (`first_aired < 2026-01-01T00:00:00Z`, half-open per D13) | 60 | **1,226** |
| 6 | Season over **26 episodes** (S1 or S2) — **`0020`** | 51 | 1,175 |
| 7 | Gap over **1,095 days** (S1 finale → S2 premiere) — **`0020`** | 37 | **1,138** |

Rules 1, 2 and 8 removed 0. Rules 6 and 7 overlap on exactly 1 show, so order is immaterial.
**Season 0 is filtered inside every show, never used to exclude one** — 878 candidates carried one.

### Structural thresholds — `0020`, Human Lead 2026-08-12

- **No minimum season size.** `ceil(0.90 × L1)` already scales per show. `L1 = 1` and `L1 = 2` are
  retained; `min(L1) = 1`, `min(L2) = 2`, so **no in-frame show has `L2 = 1`**.
- **Max 26 episodes** on either season. 26 is the traditional full broadcast season; the cut is
  insensitive from 26 to 40 (1.1–2.4% of pairs). **22 was rejected** at 196 shows / 13.8% of pairs.
- **Max 1,095-day gap** (3 years). The empty `3 y+` bucket is the cap made visible.
- Combined cost **88 shows, 12,851 pairs, 5.5%.**
- **The size cap is partly a cadence threshold: 44 of its 51 shows are C4.** C4 falls 476 → 425.
  A C4 result is computed on a population stripped of its longest-running titles.

### Other Step 2 definitions

| Term | Definition | Where |
| :--- | :--- | :--- |
| **Air period** | **Calendar year of the S2 finale**, bucketed **pre-2020 / 2020–2022 / 2023–2025**, bracketing the production shutdown. Frame: 757 / 213 / 168. **Strongly collinear with cadence — not an independent cut.** | `0017` |
| **Size quintile** | Cut over **the frame**, not the 2,094 candidates, on the **recomputed** `pool_completers`. Frame bins **238 / 221 / 224 / 227 / 228**. **A quintile label is not a stable identifier** — rebuild the frame and every boundary moves. | `0018` (see [[open-items-and-contradictions]] X3: `0018` still publishes the superseded 1,226-frame bins) |
| **`pool_completers`** | Step 1 §4 applied against **real** `E1`, `L1 = \|E1\|`, `F1 = max(E1)`. **The max-observed proxy is superseded and no result may use it.** Changes nothing on this frame (proxy = real on 1,225 of 1,226). | `0019` |
| **No content filters** | Anime and daily-strip/soap exclusions **dropped before first use.** The concern was release structure, not genre. Release structure is recorded as **fields**, thresholds set separately. The jp shows that left (92 → 60) left via the 26-episode cap, not by genre or country. | `0014`, Closed 2026-08-12 |
| **Per-season network** | **DROPPED as a field.** 47 of 6,645 season objects populated (0.71%); one show in 2,094 with two distinct values, read as noise. **Platform fragmentation is not a variable in this study** — no result may control for it, stratify on it, or rule it out. | `0016` |
| **`show_network`** | Show-level, 100% populated, 150 distinct — but it records **today's** network. **Must not be used as a release-time availability measure.** Descriptive only. | `0016`, README open item 18(b), still open |

**D12 as applied on the real frame:** C0 **0** · C1 206 (18.1%) · C2 340 (29.9%) · C3 167 (14.7%)
· C4 425 (37.3%). **Fragility count: 7 shows within one day of a bucket boundary, 0.6%** — by
D12's own test the thresholds are **not load-bearing** and a Step 13 arm on them is not indicated.
(238 sit within three days, but 220 of those are same-day drops at distance exactly 2 by
construction. **The one-day figure is the meaningful one.**)

## Step 5 — contamination vocabulary. PROPOSED, gate not approved.

**Artifact `artifacts/step5-contamination-diagnostics.md`, revision 6, FINAL.** Reviews in
`artifacts/step5-red-team-reviews.md`. See [[gate-step5-contamination]] for the arc.

### Layer 1 record tags — no rows dropped. Required by Step 7 and Step 8.

| Tag | Definition |
| :--- | :--- |
| `corrupt` | `watched_at` absent or pre-1990 |
| `backfilled` | `τ_ins(id) − watched_at > 180 d` |
| `airdate_stamped` | `(show, season, episode, instant)` tuple shared by **≥5 unrelated accounts** |
| `postdated` | `watched_at` more than **30 d after** insert |
| `clean` | none of the above |

**The 180-day threshold is a conservative judgment, not a data-determined break.** Per-day density
is monotone decreasing throughout; revision 1's "trough" was a bin-width artifact (Red Team C1).
**The only real break after 1 day is at 7 days.**

### The instrument — the play-`id` insert-time calibration

The Trakt play `id` is a global auto-increment assigned at **write** time, so it orders records by
insertion regardless of what `watched_at` claims. Fitted on `checkin` and `scrobble` only (a bulk
import mints `watch` rows), monotonised by **isotonic regression (PAVA)**, not a cumulative max.
**Held-out validation** (fit on even-indexed accounts, test on 2,185,696 real-time records of
odd-indexed accounts, no account in both): **median lag +0.003 d, 90.5% within one day.** Residual
error runs slightly **early**, so the diagnostic **under-flags**. Zero API calls.
Artefacts: `processed/step5/calibration.npz`, `record_lag.npz`.

### The insert-time bound

*A viewer cannot log an episode before watching it*, so a record's insert instant is an **upper
bound** on when it was truly watched. Latest defensible clock start:
`T0_latest = max(S2_finale_date, date(max τ_ins over the S1 completion evidence))`.
**Correct basis: the completion prefix, with the `max()` in force.**

| Population | Pairs | Median elapsed at `T0_latest` | Open at `W = 60` |
| :--- | ---: | ---: | ---: |
| The **1,542** (excluded) | 1,542 | **40.0 d** | **58.6%** |
| The **720** (C5, no S2, retained) | 720 | **1,738 d** | **7.92%** |
| — the 425, two-class | 425 | 1,717 | 13.4% |
| — the 295, air-date class | 295 | 1,762 | 0.0% |
| Every pair with no S2 evidence | 25,277 | 1,532 | 11.3% |

**`1,738 d / 7.92%` is the figure to use for the 720.** "Median 2,150 d / 8.1%" is **withdrawn** —
it came from a unit bug plus the wrong basis. See [[withdrawn-claims-register]].

### The two populations — Step 5 ruling 1

> **W is derived from clean records only, then applied to everyone.**

| Population | Pairs | Who reads it |
| :--- | ---: | :--- |
| **Analysis population** | **201,900** | Step 8 classifies these |
| **W estimation sample** | **128,099. Determinate.** | Step 6, which applies D14's C1 restriction **on top** |

Waterfall, monotone by construction: 201,900 → has S2 evidence 178,165 → `T0` not contaminated
155,131 → completing record not post-dated 152,126 → **first S2 watch clean 128,099**.

The analysis population **deliberately** retains 23,067 pairs with a fabricated `T0`, 46,642 whose
first S2 watch is contaminated, and 3,296 whose completing record is post-dated.

### Post-dating — the four readings, and why they are moot

**Adoption 3 was DROPPED (revision 6).** No pair is deleted for post-dating; records are tagged and
kept out of the W sample. The four readings are four ways to apply a rule that no longer exists.
Recorded because the **directions differ and a table ordered by retention alone hides that**:

| Reading | Retained | Bias direction |
| :--- | ---: | :--- |
| **Adopted — tag only, delete nothing** | **201,900** | neutral |
| P, delete the pair | 198,604 | never-started **down** |
| R1b, drop every post-dated S1 record | 198,817 | down |
| R1n, drop only the completing record | 199,957 | down |
| R3, re-date to insertion time | 201,900 | never-started **up** (median completion shift **−198.7 d**) |

The adopted rule coincides with R3 in **retained set**, not in method: R3 rewrites timestamps, the
adopted rule only tags them. That distinction is what avoids E4 — §2.2 (canonical timestamp = the
**minimum `watched_at`**) is untouched, and no re-dating bias is introduced. R3 would also have been
a **selective** re-dating: if `τ_ins` were trustworthy for 3,307 post-dated records it would be
trustworthy for 8,001,189 backfilled ones, where substitution moves completion much **later**.

### Contamination scale, for reference

| Class | Records | Share of 27,656,631 |
| :--- | ---: | ---: |
| Backfill >180 d | 8,001,189 | 28.9% |
| Air-date-stamped (mode 3) | 2,021,537 | 7.3% |
| Corrupt, pre-1990 (369,590 at exactly 1970-01-01) | 690,774 | 2.5% |
| Undated | 379 | 0.001% |
| **Union** | **8,831,718** | **31.9%** |

**Mode 3, air-date stamping**, was not previously identified: exact top of hour, seven days apart,
00:00–05:00 UTC, **up to 198 accounts sharing a single instant** (corrected from an uncommitted and
wrong "164"). **TV Time is a minority of the problem** — only 31.7% of backfill was written after
2026-06-01; the rest is eleven years of ordinary onboarding backfill. The shutdown wave is
3,115,531 records over four weeks (11.3% of the store) against a ~174,000 baseline, an **excess of
2.94 M records = 10.6%**.

## Step 3 crawl constants — agent-set, `0006`, Open awaiting ratification

**Source `src/step3_user_discovery.py:169-191`.** Full table retained; the load-bearing ones:

| Constant | Value | Note |
| :--- | :--- | :--- |
| `TARGET_USABLE` | **4,000** | The rule that actually stopped the run — **not** the plateau rule `task-sheet.md` names, which ran 36 rounds and never fired (final ratio 0.314 against a 0.20 trigger). `0005` |
| **`MIN_EPISODES_USABLE`** | **10** | `episodes.watched` from `GET /users/:id/stats` — an **account-wide** distinct-episode count, **not per-show**. Ten episodes across ten shows passes; nine inside one show fails. Removed **232** accounts and nothing else removed any. **Warrant accepted as not literally true** (README item 13, closed 2026-08-12): `min(L1) = 1` and 152 in-frame shows have `L1 ≤ 6`, so exposure is **at most 22 accounts, 0.5% of the 4,320 screened** — 210 of the 232 had zero episodes. All 232 recoverable at **0 live calls** |
| `call_budget` / plateau rule | 6,500 / 3-round MA ≤ 0.20 of peak on 2 consecutive rounds after ≥10 | budget 5,300 spent; plateau never fired |
| `n_seeds_target` / `max_depth` | 300 / 3 | Seeds = **movie-comment authors**, 172 distinct films, `0008`. Depth 3 never reached |
| `step4_page_limit` | 250 | matches `limit=250` in `0002` |

## Step 4 — the pull, and the rules that governed it

**Source: `GET /users/:id/history`, unfiltered, one sweep per user** (D15 / `0002`). One sweep is
one logical **pass**, not one call; throughput is estimated in **pages**.

| Term | Value | Where |
| :--- | :--- | :--- |
| **Pull order** | **Stratified round-robin** over ten equal-count forecast-page bins, one user per bin in turn, deterministic within bins. Amends an initial **median-out** instruction, which left a *centered* slice with **no user above 73 pages** at ten hours in a pool reaching 1,034. Cost: **~12% fewer users/hour**, accepted explicitly. | `0009` |
| **Tail cap** | **300 forecast pages**, skip whole, never truncate — **plus an actual-pages guard** that discards mid-sweep overruns. Excludes **38 users, 0.93%**, keeps 92.8% of pages. Justified as a **circuit breaker on forecast error**, not as protection against a slow user. Direction **upward** on the headline. | `0010` |
| **Sweep completeness rule** | **Full `X-Pagination-Page-Count` coverage plus a residual within 2% of `X-Pagination-Item-Count`.** Exact equality is **not** required — the pilot failed 7 of 10 on residuals from −97 to +20, and under exact equality the study would discard ~70% of its pool. **Amends `0002` condition 2 and Step 1 §0 — a rule inside an approved gate.** **Reviewed by Red Team 2026-08-12, which returned HOLD; UPHELD by the Human Lead on cascade cost, not on merit (`0023`).** Three findings became Step 14 limitations. | `0012`, upheld by `0023` |
| **Over-tolerance users** | Pages **discarded, logged, never truncated**, and must stay distinguishable downstream exactly as `access_denied` does. **287 users on the final ledger**; their raw pages remain cached, which is what made the neutrality check possible at zero API cost | `0012` |

**`0012` requires three behaviours counted separately, never collapsed into the tolerance:** header
**over-count** (benign, 256 of the 287), header **under-count** (benign and in the safe direction —
**31 of 287**, corrected from a mid-run "24 of 235"), and duplicate records.

**The third is misattributed in `0012` and the correction is in `0023`.** `0012` cites "5 duplicates
in 14,236 records" as **cross-page** duplicates. Instrumentation records
`cross_page_duplicate_records: 0 users, 0 records` across 2,137 users and 22,725,090 records.
**Cross-page duplicates have never been observed in either run.** What does occur is **within-page**:
147 records, the same `id` twice on one page, meaning a 250-slot page carried 249 distinct records.
That behaviour **is not a required output, is described nowhere, and has no stated interpretation.**

**Proof that the residuals are not truncation:** page-count and item-count headers were identical on
every page of every sweep; and re-sweeping one user at `limit=100` returned the **identical record
set in identical order** as the cached `limit=250` sweep — 1,459 distinct records both ways, while
both headers reported 1,460.

### What `0023` established about the 2% tolerance, and what did not change

**Nothing in the study moves.** Cohort 2,549, frame 1,138 shows, 220,107 pairs, 201,900 retained,
128,099 estimation sample — all stand. The tolerance was not touched and nothing was re-run.

**Three findings now travel to Step 14 as limitations:**

1. **The rule validates itself against itself.** Leg 1 gates on `page_count`, which is
   **`ceil(item_count / 250)` in all 2,839 ledger rows, zero mismatches** — so it is derived from
   the very header leg 2 exists to absorb. A **short** final page proves the sweep reached the end;
   a **full** final page proves nothing, and leg 1 cannot tell them apart.
2. **The discard is NOT outcome-neutral.** Measured at zero API cost on the discarded users' cached
   raw pages: has-any-S2 **89.78% (discarded) vs 88.52% (retained)**, **+1.27 points, 95% CI [0.87,
   1.66], z = 5.98, p < 0.001**, intervals non-overlapping. **Direction: up** on the never-started
   share, **compounding with the seeding and liveness biases rather than offsetting them.**
   **Pooled effect 0.13 points** (88.52% → 88.65%), because the 287 carry 10.2% of the pair pool.
   *Statistically clear, practically small — neither half may be quoted without the other.*
3. **Red Team's final-page shape test** — every interior page full at `limit`, final page strictly
   between 0 and `limit` — would discriminate **exactly** rather than by calibration, at **~2,800
   calls, ~19 minutes, and no re-pull**. **Declined on cascade cost, not on merit.** If the pull
   ever resumes, the cascade argument weakens and the shape test should be reconsidered rather than
   inherited as settled.

**The ruling's stated reason, in full:** tolerance → cohort size → completer counts per show → which
shows clear ≥50 → the candidate set → the frame → the structural thresholds → the 220,107 pairs →
the approved Step 5 rule computed on them. **A 0.13-point correction at the far end does not justify
re-deriving that chain.**

**How the 2% was actually set, recorded in `0023`.** The pilot's p95 is **1.4%** and p99 = max is
**11.7%**, with nothing in between, so **every tolerance from ~1.5% to 11.7% split those 20 users
identically** — and the most aggressive end of that band was chosen, with no sensitivity table and
without the choice being stated as a choice. **On the full run there is no such gap:** absolute
residual share over the 287 discards runs min 2.01%, median 3.92%, max 99.9%, with **168 (58.5%) in
the 2–5% band** — so a 5% tolerance would have retained 168 of the 287. The threshold cuts through
the middle of a continuous distribution.

**One structural asymmetry nobody chose.** Accumulated records can never exceed
`limit × page_count`, so a positive residual is capped at **249**. **Above roughly 50 pages the
under-count arm cannot fire at all.** The rule presents as a symmetric two-sided threshold; it is a
one-sided test on large users and a size-correlated discard on small ones. It also discards **31 of
287** users in the direction `0012`'s own table calls *"benign, and in the safe direction."*

## The population chain — every number a result rests on

See [[population-chain-steps-2-3-4]] for the reconciliations. Headline figures:

**4,088 usable users** → 4,050 in plan after the 38 over-cap → **pull stopped at 2,836 decided
(70.0%)** → **2,549 `complete`** (287 discarded over tolerance) → 44,617 shows with an S1 record →
**2,094 candidates** at ≥50 completers → **1,138-show frame, 220,107 pairs** → Step 5 proposes
**201,900 analysis population** and **128,099 W estimation sample**.

## Standing rule — when a post-approval edit reopens a gate

**An edit that changes a *rule* reopens the gate; an edit that adds *evidence* for a rule already
adopted does not.** Fixed 2026-08-10 in the Step 1 approval record. **`0012` is the first edit that
fails this test and was recorded as a Human Lead amendment anyway** — README open item 15 flags it
as not yet put to Red Team.

## Probe figures — n = 1, existence proofs, NOT rates

Play-record inflation **28.125%** (123 records, 96 distinct pairs, 27 surplus records, **25**
episodes duplicated — 27 and 25 answer different questions and are both right). S1/S2 overlap
**41.31 d under definition (a)**, inverting to **360.73 d of separation under (b)**. 64 pages per
user at `limit=250`. `episode.ids.trakt` disagreement with `(season, number)`: **untested**, not
confirmed — and the Step 2 frame's four absolute-numbering shows have since been removed by the
26-episode cap, though their finding stands (100% overlap on all four; the **withdrawn `1..F`
range form would have failed on all four**).

## Season membership, outcome states, counting rules

Unchanged from Step 1 and still governing.

`E` = the **listed episode-number set**; `L := |E|`; `F := max(E)`. **`F := L` is forbidden**
except by Human Lead adoption of the §3.3 fallback. Source `GET /shows/:id/seasons?extended=
episodes,full`, one call per show. `show.aired_episodes` is **never** used.

### The outcome states, POST-AMENDMENT — `0034`, 2026-08-12

| State | Condition |
| :--- | :--- |
| **Never started** | `\|A\| = 0` — decided at **`τ1`, 108 days** |
| **Continued** | `\|A\| ≥ 1` **and** `F2 ∈ A_H` **and** `\|A_H\| ≥ ceil(0.90 × L2)` — decided at **`τ2`, 199 days** |
| **Started and left** | `\|A\| ≥ 1` **and not** the Continued condition |

**The pre-amendment Continued row read `|A| ≥ 1 ∧ F2 ∈ A ∧ |A| ≥ ceil(0.90 × L2)`, evaluated at
`τ1`. That is superseded.** Any live use of that form is stale — see
[[open-items-and-contradictions]].

**The `|A| ≥ 1` conjunct is load-bearing, not tidying.** Without it, a pair first watching S2 on
day 150 and completing by day 190 satisfies the other two conjuncts with `|A| = 0` and falls in
**two** states. It **makes the cost visible; it does not cause it** — the cost belongs to the
asymmetric anchoring, and D8(ii) is that asymmetry measured. Attributing 1,575 to the conjunct was
withdrawn.

**Partition proof survives verbatim in structure:** `A = ∅` / `(A ≠ ∅ ∧ C_H)` / `(A ≠ ∅ ∧ ¬C_H)`.
No fourth state, no changed denominator, Step 8's sum-to-sample invariant untouched.

**Continued is a 199-day statement while never-started is a 108-day statement, and the two must
never be described as measured alike.** This appears wherever the split is reported, not in a
footnote.

Abandonment point `p = |{e ∈ E2 : e ≤ m_H}| / L2` where `m_H = max(A_H)` — rank-based, defined only
for Started-and-left. **Direction Step 10 must name:** the 2,246 pairs leaving Started-and-left are
the ones that got furthest, so abandonment looks **earlier** on the published chart, and the
`p = 1.0` residual **changes size under `A_H` and must be re-reported, not carried over.**

Counting: **distinct episodes, never play events**, dedup key `(show.ids.trakt, season, number)`
scoped to the user; **canonical timestamp = minimum `watched_at`**; **all `action` values count as
watching**, `checkin` included, with `action` retained as a column.

## Required diagnostics fixed at Step 1 — unchanged

D2 negative-lag split by binding term · D3 resumption over `[τ1, τ1 + H)` · D4 S3-without-S2 bound ·
D8 never-started post-window · D9 split-artifact counts · liveness bound (**up**) · right-censoring
removal as **two lines** · dropped-S2-evidence count. `L2 = 1` shows excluded at Step 8 (**moot on
the current frame — `min(L2) = 2`**).

Related: [[gate-step1-outcome-definition]], [[gate-step5-contamination]],
[[population-chain-steps-2-3-4]], [[open-items-and-contradictions]], [[withdrawn-claims-register]],
[[decision-log-step18]].
