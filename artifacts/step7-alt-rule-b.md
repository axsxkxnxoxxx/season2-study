> **SUPERSEDED — HISTORICAL RECORD ONLY. Do not cite any figure in this file as operative.**
> The Step 7 rule changed four times. This artifact predates **ALT-BROAD** (`decisions/0048`),
> the rule in force: *not live iff no insertion instant after `τ1` AND NOT Continued.*
> The current deliverables are `artifacts/step7-liveness-bb-{a,b}.{md,json}`.
> Superseded here: any numeric threshold (4 / 504 / 632 / 914 / 1,293 days), **PF-LIMIT**,
> **ALT**, the bounds `[16.7789%, 17.0355%]` and `[16.7146%, 16.9704%]`, exclusion counts
> 751 / 1,355 / 604-as-total / 0-on-DERIV, and the claim *"the exclusion set is empty on
> DERIV"* (`decisions/0049` #4 — false; it is 99). Stamped 2026-08-13 by `decisions/0051`.

# Step 7 — evaluation of Red Team's alternative liveness rule (instance **b**)

**EVALUATION ONLY. NOTHING IS ADOPTED.** The Step 7 gate is open (`decisions/0044` §4). This instance
proposes; the Human Lead rules, after both arms report independently. **Zero API calls.** The stored
Step 5 calibration was read through the frozen `b4` insertion instants and **not refitted**.

| | |
| :--- | :--- |
| **Approved rule under test** | **PF-LIMIT** — not live **iff** the account shows no insertion instant after that pair's `τ1` (`0042`) |
| **Alternative under test** | **ALT** — not live **iff** (no insertion instant after `τ1`) **AND** `\|A\| = 0` |
| **Added by this instance** | **ALT-BROAD** — not live **iff** (no insertion instant after `τ1`) **AND NOT Continued.** Nobody proposed this. It is the rule Red Team's *stated principle* selects, and it is not the rule Red Team proposed |
| **Recommendation** | **Do not adopt ALT as the liveness rule. Rule the ordering obstacle non-binding, and take Option C** — keep PF-LIMIT as the population filter and restrict the Step 9 bound to its never-started exclusions, the disposition `0043` §1.2 already offers. Reasoning in §5 |

---

## 0. The pivot: which population the question is asked on

Everything below turns on one fact that neither the proposal nor `0043` states.

**Step 5 waterfall line 4 requires `has_s2`** — at least one S2 record somewhere in the sweep. It is
the population `0042` published its **751** on, and the population whose composition (1,079 / 163 /
**40**) Red Team quoted. **Step 8 does not apply liveness to that population.** `0041` §3 and `0042` §5
name the apply population as the Step 5 analysis population less D10 — **196,654** at `W = 108`, which
this run reproduces exactly — and that set **admits pairs with no S2 record at all.**

Two populations are therefore reported throughout, never merged:

| | Definition | `n` at `W = 108` | Accounts | Never-started, unfiltered |
| :--- | :--- | ---: | ---: | ---: |
| **DERIV** | line 4 less D10 — the `0042` population | 147,370 | 2,402 | **6.2055%** |
| **APPLY** | line 1 less D10 — `0041` §3 / `0042` §5 | **196,654** | 2,422 | **16.9704%** |

**APPLY carries contaminated `T0`, post-dated and bad-first-S2 lines by construction** — that is what
`0042` §5 means by "a strict superset whose extra lines carry contaminated `T0`", and both `τ1` and
`τ2` are built from `T0`. Its levels are **not results** and must not be quoted as any. Its *contrasts
between rules* are the object of interest, and they are computed on identical rows.

---

## 1. Is the stated obstacle real?

**No, not as a dependency. Yes, as a propagation obligation.** Three separate findings.

### 1.1 The dependency graph is acyclic, and this run demonstrates it rather than asserting it

`|A|` is a function of `T0`, `W`, `E2`, the episode records and D11 — `|A| = |{ e ∈ E2 : `canonical
`watched_at < ⟦T0⟧ + W × 24h }|`. **No term references liveness, insertion time, or the calibration
curve.** In this run `src/step7_alt_b_2_outcomes.py` computed `|A|` and the full three-state partition
at **all eight `W` arms** with the liveness arrays not loaded, and `src/step7_alt_b_3_rules.py` then
applied liveness on top. Nothing had to be iterated, guessed, or resolved.

### 1.2 `0029`'s recorded rationale is about 5-before-6, and it is silent on 6-before-7

`0029` §3 gives exactly one rationale, and it is the one the question quotes: *"censoring is a property
of the clock and `pull_date` — objective, and independent of behaviour — while liveness is a
behavioural inference; running the objective filter first means liveness's marginal cost is measured on
a fully observable population."* **ALT satisfies that rationale unchanged** — it still runs after
right-censoring, and its marginal cost is still measured on the fully observable population.

### 1.3 Position 7 is not a filter position at all, so nothing commutes with it

This is the finding that settles it. `0029` §3 fixed the order for one stated reason: *"the final row
set commutes, but the required per-filter sample size does not."* That reason **cannot apply to
position 7**, because outcome assignment **removes no rows**. It is a total partition — asserted in
this run at every arm on both populations, `never_started + continued + started_and_left = n` exactly —
so it contributes **no line to the waterfall** and no count that could differ between two faithful
instances. Positions 1–6 are filters; **position 7 is an annotation.** "Liveness before outcome
assignment" is a statement about when a *column* is computed, not about the order of two filters, and
the defect `0029` exists to prevent is not reachable through it.

### 1.4 What it would nonetheless cost, stated as the real cost

The obstacle is not the arithmetic. It is that **`0029` says what it says**, and `0044` §3.1 has just
sharpened the propagation rule to *"the surface is five files and an entry must state which it
touched."* Restating the order means amending `0029`, `task-sheet.md` Steps 7 and 8, and all four
pipeline agent definitions — **immediately after propagation failure #6, on the gate that launches
next.** The wording that would do it, if the Human Lead wants it on the record:

> **5.** right-censoring → **6a.** compute `A` at `τ1` (annotation; removes no rows; assert the count
> is unchanged by its position) → **6b.** liveness → **7.** outcome assignment at `τ1` and `τ2`.

**Judgement call, stated:** I treat "is the ordering a convention that could be restated" as a question
about whether any *count* changes. It does not. If the Human Lead's concern is instead that a filter
defined by an outcome column is harder to *describe* in a published waterfall, that concern survives
everything above and is answered in §4.3.

---

## 2. What it would cost — measured

### 2.1 At `W = 108`, both populations

| Population | Rule | Excluded | Accts | of which NS | Cont | S&L | Never-started | Δ vs no filter |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **DERIV** | no filter | 0 | — | — | — | — | 6.2055% | — |
| | **PF-LIMIT** | **751** | 166 | **0** | 652 | 99 | **6.2373%** | **+0.0318** |
| | **ALT** | **0** | 0 | 0 | 0 | 0 | **6.2055%** | **0.0000** |
| | ALT-BROAD | 99 | 73 | 0 | 0 | 99 | 6.2096% | +0.0042 |
| **APPLY** | no filter | 0 | — | — | — | — | 16.9704% | — |
| | **PF-LIMIT** | **1,355** | 276 | **604** | 652 | 99 | **16.7789%** | **−0.1915** |
| | **ALT** | **604** | 191 | 604 | 0 | 0 | **16.7146%** | **−0.2558** |
| | ALT-BROAD | 703 | 216 | 604 | 0 | 99 | 16.7231% | −0.2474 |

Three things in that table are new to the record.

**(a) On the derivation population, ALT excludes ZERO pairs — at every `W` arm.** Not "on the order of
40." Red Team's ~40 is the never-started count inside the *threshold* rule's 1,282, and **all 40 of
them arrive through the measured-gap channel**, which PF-LIMIT deleted. PF-LIMIT's own 751 contains
**no never-started pair at all**: 652 Continued, 99 Started-and-left, and **751 of 751 carry positive
in-window S2 evidence**, not six in seven.

**(b) The mechanism is `has_s2`.** On APPLY, ALT's 604 exclusions are **exactly the 604 pairs with no
S2 record anywhere in the sweep.** Line 4 removes every one of them by construction, which is why ALT
is a no-op there. PF-LIMIT's 1,355 splits **751 with an S2 record / 604 without** — the 751 being
precisely the DERIV set.

**(c) PF-LIMIT's published sign is a DERIV fact and it flips on APPLY.** `0043` corrected the ledger
from DOWN to **UP** on the strength of 6.2055 → 6.2373. On the population Step 8 will actually filter,
PF-LIMIT moves never-started **DOWN 0.1915 pp** (paired clustered CI **[−0.242, −0.143]**, excluding
zero). **`0043`'s ruling is right about the pairs it names and its sign does not survive the population
change.** That is a finding against the current record independent of which rule is chosen, and it is
the same error class `0043` itself catalogues — a figure measured on one configuration read as if
measured on another.

### 2.2 Account-clustered intervals, `B = 2,000`, cluster = account

| Population | Rule | Never-started 95% CI | Width |
| :--- | :--- | :--- | ---: |
| DERIV | no filter | [5.8379, 6.6020] | 0.764 pp |
| | PF-LIMIT | [5.8705, 6.6346] | 0.764 pp |
| | ALT | [5.8379, 6.6020] | 0.764 pp |
| APPLY | no filter | [16.4440, 17.5140] | 1.070 pp |
| | PF-LIMIT | [16.2605, 17.3259] | 1.065 pp |
| | **ALT** | **[16.1939, 17.2560]** | 1.062 pp |

**Every rule-to-rule difference is far inside the sampling width and several are still statistically
distinguishable** — the nested-subset property `0042` §2 already recorded. ALT → PF-LIMIT on APPLY is
**+0.0647 pp [+0.0413, +0.0947]** on never-started, **−0.0516 [−0.0963, −0.0186]** on Continued,
**−0.0131 [−0.0288, +0.0041]** on Started-and-left. **Detectable, and about 6% of the clustered width.**
The choice between PF-LIMIT and ALT does not move the headline.

### 2.3 The `W`-coupling `0044` §1.2 requires, per rule per arm

| Population | Rule | 38 | 46 | 77 | 91 | 107 | **108** | 150 | 213 | Factor |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| DERIV | PF-LIMIT | 348 | 367 | 519 | 706 | 745 | **751** | 779 | 949 | 2.7× |
| | ALT | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | — |
| APPLY | PF-LIMIT | 833 | 861 | 1,073 | 1,281 | 1,348 | **1,355** | 1,443 | 1,670 | 2.0× |
| | **ALT** | 485 | 494 | 554 | 575 | 603 | **604** | 664 | 716 | **1.5×** |
| | ALT-BROAD | 537 | 550 | 633 | 664 | 701 | **703** | 789 | 864 | 1.6× |

**ALT mitigates `0044`'s coupling finding; it does not remove it.** The rule still has no parameter of
its own and is still fully determined by `W`, and Step 13 must still report the count per arm.

**Also on this table, and it is a propagation risk rather than a result:** `task-sheet.md` Step 7 and
`0042` state PF-LIMIT's exclusions as **751 from 166 accounts**, correctly labelled as the derivation
population. **On the population Step 8 filters, the same rule excludes 1,355 from 276 accounts.** The
two Step 8 instances will produce 1,355 and the diff against the task sheet's 751 will read as a
divergence. Whatever is decided here, that number should be carried into the Step 8 files.

### 2.4 Invariants and waterfall

Nothing breaks. **The Step 8 partition invariant, the `A ⊆ A_H` code check and monotone filter counts
all hold identically under ALT** — it removes rows, and removing rows cannot break any of them. The
only waterfall change is line 6's count (751 → 0 on DERIV; 1,355 → 604 on APPLY) and its description.

**One quantity is untouched by the choice, and it is worth naming:** PF-LIMIT and ALT delete **the same
604 never-started pairs** (ALT ⊆ PF-LIMIT, and PF-LIMIT's NS exclusions are exactly ALT's set). So
**D8's never-started base, D9's split-artifact counts and every never-started diagnostic are identical
under the two rules.** They differ only by 652 Continued and 99 Started-and-left pairs — which is
another way of stating Red Team's point, and it bounds how much can turn on this.

---

## 3. What it does to the Step 9 bound

Step 9's bound is *"what the never-started share becomes if every inactivity-excluded pair is treated as
a decliner."* Both endpoints, both populations, excluded pairs returned to **numerator and denominator**
(the reading the task sheet states):

| Population | Rule | Floor | Ceiling | Width | Unfiltered | Ceiling − unfiltered |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: |
| DERIV | PF-LIMIT | 6.2373% | **6.7151%** | 0.478 pp | 6.2055% | **+0.510 pp** |
| | ALT | 6.2055% | 6.2055% | **0.000 pp** | 6.2055% | 0.000 |
| APPLY | PF-LIMIT | 16.7789% | **17.3523%** | 0.573 pp | 16.9704% | **+0.382 pp** |
| | **ALT** | 16.7146% | **16.9704%** | 0.256 pp | 16.9704% | **0.000** |

**PF-LIMIT's ceiling is not merely uninformative — it is outside the feasible set.** To reach it you
must score as decliners 751 pairs that are *observed* to have watched in-window S2 episodes, 652 of them
having watched the finale and ≥ 90% of the season by `τ2`. **No assignment of the excluded pairs
consistent with the data can produce that number.** The sharpest statement of it: on both populations
PF-LIMIT's ceiling **exceeds the share you get by applying no liveness filter at all** — by 0.510 pp on
DERIV and 0.382 pp on APPLY — while every pair it adds to the numerator is known to have started.

**ALT's ceiling equals the unfiltered share exactly, and that is an identity, not a coincidence.**
Because the excluded set is a subset of never-started, returning it whole gives back the unfiltered
population and the unfiltered count. So **every point in ALT's interval is feasible**, both endpoints
are attainable, and the bound's content is exactly *"the whole effect of the liveness filter on
never-started."* **Yes: under ALT the bound bounds the quantity it claims to.**

**On DERIV, ALT's bound is [6.2055, 6.2055].** A zero-width bound is the correct answer to *"how much
could liveness be corrupting never-started here"* on a population that contains no never-started pair on
a silent account — and it is also the plainest statement of §5's objection.

### 3.1 Option C — the same repair without changing the rule

`0043` §1.2 already offered it: *"Report it as narrow AND as bounding the wrong set, **or compute it on
the ~40 never-started exclusions instead.**"* Keeping PF-LIMIT as the population filter and restricting
the bound to its never-started exclusions gives:

| Population | Floor | Ceiling, all exclusions | **Ceiling, NS exclusions only** | Restricted width |
| :--- | ---: | ---: | ---: | ---: |
| DERIV | 6.2373% | 6.7151% | **6.2373%** | 0.000 pp |
| APPLY | 16.7789% | 17.3523% | **17.0355%** | 0.257 pp |

**This recovers the whole of Red Team's substantive complaint** — the ceiling becomes feasible, the
bound bounds pairs whose classification actually depends on the silence, and the width lands within
0.001 pp of ALT's — **with no change to the rule, the population, the filter order, or the five-file
propagation surface.** It is not identical to ALT's bound (the denominator still omits the 751), and
that difference should be stated where it is published.

---

## 4. What breaks — the case against ALT

### 4.1 It is a no-op on the population the gate was derived and reviewed on

`0040` §2 ranked one requirement first — *"the derivation and application populations must be
identical"* — and moved derivation after D10 to satisfy it. **Adopting ALT re-opens that wound in a new
shape:** on DERIV it excludes **0 pairs at every arm**, so the Step 7 gate would close on a rule with
**no measured effect on the population Step 7 measures.** Its entire behaviour lives on the Step 8
population, which is **behind an unapproved gate and has not been built.** Every APPLY figure in this
document is *my reconstruction* of that population and could move when Step 8 runs.

### 4.2 It makes Step 7's dual-implementation control vacuous

Step 7's deliverable is *"the rule statement and the excluded counts."* Under ALT both arms report
**0 and 0**, and agree. `0040` §7 already recorded that exact agreement on this step is weak evidence;
**agreement on zero is no evidence at all.** The numbers that need two independent implementations then
move to Step 8, whose two instances were handed the PF-LIMIT text three entries ago (`0044` §3).

### 4.3 The analysis population becomes outcome-conditional, and one stratum is screened differently

Under PF-LIMIT the population is describable without reference to any outcome: *pairs whose account
shows insertion activity after the window closed.* Under ALT it is *pairs whose account shows insertion
activity after the window closed, **or** which have in-window S2 evidence* — still statable, but the
liveness screen now falls on the **never-started stratum only**. Any statistic that compares
never-started against the other two states (D8, D9, Step 11's channel split, Step 12's segment cuts) is
then computed on strata screened by different criteria. **Measured, this is smaller than it sounds** —
§2.4 — but it must be written into Step 14 rather than discovered by a reader.

### 4.4 Red Team's principle over-shoots the rule Red Team proposes

The stated warrant is *"liveness can only serve its purpose on pairs whose outcome is inferred from
absence."* **Continued is the only state established by positive evidence alone.** Started-and-left is
positive on entry (`|A| ≥ 1`) and **inferred from absence on exit** — the finale and the 90% threshold
are *not* observed by `τ2`, and an account that goes dark after `τ1` is exactly an account whose
unlogged completion would be invisible. So the principle selects **ALT-BROAD**, not ALT. And ALT-BROAD
does **not** have the clean sign: on DERIV it moves never-started **UP** (+0.0042 pp), because deleting
Started-and-left pairs raises the other two shares. **"Unambiguous DOWN sign" is a property of ALT's
specific conjunct, not of the argument offered for it.**

### 4.5 The DOWN sign is an arithmetic identity, not evidence

ALT deletes only never-started pairs, so the never-started share can only fall. **That is true before
any data is read.** It restores the conservative-direction argument by construction — which is a weaker
thing than restoring it as a finding, and it means the rule can never correct a bias running the other
way. It also reinstates `task-sheet.md` bias 2's "compounds with bias 1", which `0043` §1.2 had just
converted to "offsets it, trivially." The ledger must be re-corrected a second time if ALT is adopted.

### 4.6 It does not supply the missing warrant, which is `0044` §4's actual open item

`0021` licenses *"insertion after `τ1` → live"*, a **sufficient** condition. **ALT is still a
biconditional** — it still asserts that silence after `τ1` licenses deleting a pair. It narrows *where*
that assertion is made from 1,355 pairs to 604. **It does not justify it.** The open item survives
either choice, and neither arm's arithmetic can close it.

### 4.7 A wording ambiguity that must be settled before either arm implements it

`|A| = 0` admits three faithful readings: `|A| = 0` at `τ1`, `|A_H| = 0` at `τ2`, and "NOT Continued."
**Measured: the first two select the identical 604 pairs at every arm on both populations** — every
never-started pair on a silent account has no S2 record at all, so the bound makes no difference. **That
is a fact about this data, not a construction**, and the spec must still name `τ1` explicitly, matching
Step 1 §7's never-started condition. The third reading is ALT-BROAD and differs by 99 pairs.

---

## 5. Recommendation, stated as a recommendation

**On the merits of the bound, Red Team is right and PF-LIMIT is wrong.** PF-LIMIT's Step 9 ceiling is
infeasible on both populations, it exceeds the no-filter share while adding only pairs known to have
started, and `0043` §1.2's "meaningless, not merely uninformative" is the correct assessment. That
should be recorded whatever else is decided.

**On the rule, I recommend against adopting ALT**, in three parts:

1. **Rule the ordering obstacle non-binding, and record why** — §1.3, that position 7 removes no rows
   and therefore has no waterfall line to permute. That finding is worth an entry regardless of the
   outcome, because it will recur at Step 13.
2. **Do not adopt ALT.** It is a no-op on the only population Step 7 has, its dual-implementation
   diff would be `0 = 0`, and it buys a change of **0.065 pp** on never-started — 6% of the clustered
   sampling width — at the cost of an amendment to `0029` and a six-file propagation pass immediately
   after propagation failure #6.
3. **Take Option C** (§3.1): keep PF-LIMIT as the population filter, and **restrict the published Step 9
   bound to its never-started exclusions.** This is the disposition `0043` §1.2 already put on the
   table; it makes the bound feasible and correctly targeted, it lands within 0.001 pp of ALT's width,
   and it touches no rule, no population, no filter order and no agent file.

**If the Human Lead prefers the rule change anyway**, then ALT — not ALT-BROAD — is the right form
despite §4.4, because ALT-BROAD's sign is population-dependent and its `τ1`-anchored silence test is
mismatched to a `τ2`-read state. In that case the spec must say `|A| = 0` **at `τ1`**, the order must be
restated as in §1.4, and §2.3's per-arm counts must go into Step 13.

**And independent of all of it, two things need fixing now:** `0043`'s UP sign is a DERIV fact that
**reverses on the Step 8 population** (§2.1c), and `task-sheet.md`'s "751 pairs from 166 accounts" will
be **1,355 from 276** when Step 8 applies the same rule (§2.3).

---

## 6. Every judgement call I had to make

1. **Two populations, not one.** The proposal and `0043` are stated on line 4; Step 8 applies to line 1
   less D10. I report both and merge nothing. **APPLY is my reconstruction** — it reproduces `0041`
   §3's 196,654 exactly, which is the only cross-check available, and Step 8 may still differ.
2. **APPLY's contaminated lines are not repaired.** `0042` §5 says they carry contaminated `T0` and
   both `τ1` and `τ2` are built from it. Its absolute levels are not results.
3. **`|A| = 0` read at `τ1`,** matching Step 1 §7's never-started condition. The `τ2` reading is
   measured too and selects the same 604.
4. **ALT-BROAD is mine.** No one proposed it. It is included because the principle offered for ALT
   selects it, and excluding it would have let §4.4 go unmeasured.
5. **Liveness state recomputed as `max(insertion instants) ≤ τ1`**, and asserted equal to `b4`'s stored
   `searchsorted(side="right")` state on all eight arms on all 152,126 line-4 rows.
6. **The calibration is read, never refitted.** `b4`'s 6,956 clamped records (0.025%) are carried
   forward with their judgement call intact.
7. **`H` held at 91 at every `W` arm**, per Step 13.
8. **The bound returns excluded pairs to the denominator as well as the numerator.** A numerator-only
   reading exists and is not what Step 9 says.
9. **Bootstrap:** account-clustered, `B = 2,000`, percentile, one resample shared across rules within a
   replicate so deltas are paired. Same convention as `sens_b`; **not** the same draws as any other run.
10. **`L2 = 1` is empty on line 1** (0 pairs), so Step 8's position-2 exclusion changes nothing here and
    no variant was needed.
11. **I did not read, list or reference any `a`-namespace path.**

---

**Row-level detail:** `processed/step7/alt_b/` (`pairs.npz`, `outcomes.npz`, `rules.json`,
`variants.json`, `bootstrap.json`, `stage1.json`, `stage2.json`).
**Machine-readable summary:** `artifacts/step7-alt-rule-b.json`.
**Code:** `src/step7_alt_b_1_population.py` … `src/step7_alt_b_6_deliver.py`.
