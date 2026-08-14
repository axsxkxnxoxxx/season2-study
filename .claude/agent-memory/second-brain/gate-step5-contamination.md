---
name: gate-step5-contamination
description: Full arc of the Step 5 contamination gate — six revisions, four Red Team rounds (three HOLD, one PROCEED), APPROVED as decisions/0021 on 2026-08-12, the D1 challenge to Step 1 §7 that was upheld, and the two standing rulings that outlive it
metadata:
  type: project
---

# Step 5 gate — CLOSED. Gate 2 of 5.

**Fact of record: `decisions/0021-step5-contamination-gate.md` records the Human Lead approving the
Step 5 contamination exclusion rule in writing on 2026-08-12.** The deliverable is
`artifacts/step5-contamination-diagnostics.md` revision 6. The approval record in `0021` states that
no agent recorded it and no agent adopted its own proposal — the analytics-engineer produced and
revised, the red-team agent reviewed and recommended, neither approved. I do not record approvals; I
carry the fact and its citation.

**The approved rule.** Exclude the **16,665** pairs whose S2 evidence is entirely air-date-stamped;
exclude the **1,542** with no S2 evidence and a fabricated binding clock start; **retain 201,900 of
220,107 (91.73%)**; derive `W` on **128,099**. The two exclusions are **disjoint by construction** —
one set has S2 evidence, the other has none.

**Unblocks Steps 6, 7 and 8, each of which is itself an unapproved gate.** Step 6 launched
2026-08-12 as a dual pair.

**Why this arc matters more than the rule:** Step 5 is the first gate where a downstream step
challenged an **already-approved** gate and lost. How that was handled is the precedent.

## The revision series — and the exclusion figure moved five times

| | Rev 1 | Rev 2 | Rev 3 | Rev 4 | Rev 5 | **Rev 6 FINAL** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Excluded pairs | 71,235 | 24,609 | 1,542 (+ad. 3) | 18,207 | 18,207 | **18,207** |
| Share of 220,107 | 32.4% | 11.2% | 0.7% | 8.27% | 8.27% | **8.27%** |
| Retained | 148,872 | 195,498 | 215,258–218,565 | 201,900 | 201,900 | **201,900** |
| Open decisions | 3 | 3 | 2 | 2 | 1 | **none** |

**Only 18,207 / 201,900 are current.** Every other figure in that row is superseded, and revisions
1–3 quoted costs against baselines that no longer exist — Red Team E2 was raised for exactly that.

## The four rounds

| Round | Reviewed | Verdict | Findings |
| :--- | :--- | :--- | :--- |
| 1 | revision 1 | **HOLD** | B1, B2, B3 blocking; C1–C5 corrections |
| 2 | revision 3 | **HOLD** | D1, D2, D3 blocking; E1–E6 corrections |
| 3 | revision 4 | **HOLD** — "a narrow hold"; reviewer stated it would **not object to the rule on its merits** | F1, F2, F3 blocking |
| 4 | revision 6 | **PROCEED** — first non-HOLD | four corrections, all since applied |

The reviewer is read-only (Read, Grep, Glob; cannot execute code) and **wrote no files**. Rounds 1
and 2 were transcribed at the Human Lead's instruction **before the D1 ruling**, so the ruling was
made against a durable record rather than a conversation. That is the practice to keep.

### Round 1 — the rule, not the instrument

The review **credited the instrument**: the play-`id` clock is a genuine second clock, the held-out
validation is properly constructed with no leakage, PAVA is real and disclosed, the TV Time dating
is sharp. Objections were to the rule.

- **B1** — the artifact used "clock start" to mean the S1 completion instant alone, when Step 1 §6
  defines `T0` as a `max()` of two terms. `src/step5_pairs.py` never opened `s2_finale_date`. Since
  every contamination class fabricates dates **earlier**, `max()` absorbs the contamination wherever
  the fake S1 date falls at or before the finale. The headline *"one clock start in three was
  written by an import"* was a statement about one input to a `max()`, not about clock starts.
  Also named as a **spec ambiguity under the dual-implementation rule**, not a wording preference.
  Corrected cost when computed: of 71,235, **46,626 absorbed (65.5%)**, **24,609 still binding**.
- **B2** — rule P2 was costed in `rule_costs.csv` and then appeared nowhere. *"The artifact did not
  merely decline to decide the three questions it lists. It decided a fourth against, silently,
  having costed it."* P2 was **later adopted** as adoption 1.
- **B3** — Layer 4 and §8 rested on `throughput.npz`, which **nothing in `src/` wrote.**
- **C1–C5**: the 180-day "trough" is a bin-width artifact; the pair-vs-account argument is circular;
  post-dated records untagged; "duplicate accounts: none" overstates a conditional negative
  (251 accounts have <5% real-time records and are untestable).

### Round 2 — D1, the finding that reached Step 1

**Revision 3 was built on this sentence:**

> ~~"Timestamp accuracy is not a concern for this study. The outcome is whether someone watched
> season 2, not when."~~

Red Team D1: for that to hold, "Never started" would have to mean "no S2 evidence, ever." Approved
Step 1 §7 says `|A| = 0` under **`watched_at < τ1`**. **The outcome operator is a timestamp
comparison.** And Step 1's mandatory **D8** exists precisely for the population the principle says
cannot exist. The choice was named explicitly for the Human Lead:

> **(a)** amend Step 1 §7 to an ever-started definition — which **reopens gate 1** and voids `W`,
> D3, D8 and the three-state partition; or **(b)** narrow adoption 1 to pairs whose S2 evidence can
> bear the `watched_at < τ1` comparison. *"They should be told that is the choice, not 'tidy versus
> untidy timestamps.'"*

**THE RULING — Human Lead: keep §7 as approved. Gate 1 stays closed. Option (b).** Recorded reason:

> Ever-started is the wrong study for this frame. Exposure spans 55 years and 69 percent of pairs
> are pre-2020, so a to-the-pull-date rate would be a mixture weighted by show recency and newer
> titles would look worse by construction. It also collapses "started four years late" and "started
> opening week" into one row, which is the conflation this study exists to break.

**This is the most consequential thing in Step 5.** It is the same argument that produced `H = 91`
at Step 1 (D3/D8 "to the pull date" were withdrawn as exposure-weighted mixtures) — applied a
second time, by the same person, to defend the rule it produced. The revision-3 principle is
**withdrawn** and revision 6 §0 restates §7 verbatim.

**D2** — adoption 2 and the C5 ruling applied opposite logic to the same object. Both the 1,542
(excluded) and the 720 (retained) are pairs with **no S2 evidence** and an untrustworthy `T0`. For
such a pair `|A| = 0` for **every** `τ1`, so it is perfectly evaluable — "cannot be evaluated" is
wrong. What actually depends on `T0` is **right-censoring**: a fabricated-early `T0` lets a pair
**pass a censoring test it should have failed.** Re-ruled onto the censoring rationale.

**D3** — §10's headline C5 figures were not in the repository. B3 recurring, **inside the section
written to answer Red Team.**

**E1–E6**: the bias statement covered only the exclusion and not the far larger retention; the
rejected-rules table quoted costs against the abandoned Layer-2 baseline (P3 understated by 41%);
"128,099 under every reading" was unproved for R3; R3's claimed §2.3 precedent does not hold and R3
would be a rule change inside an approved gate; §8's header and percentages used different
denominators.

### Round 3 — the write-up, not the rule

- **F1** — a population change and an estimator bias were **netted into one direction**. The
  `30.2` ratio was computed as 46,642/1,542, **ignoring the 16,665**, which runs the other way and
  is 10.8× the 1,542. Against the net exclusion the ratio is **3.1**. Withdrawn.
- **F2** — 2,352 of the 7,340 partly-stamped pairs were **closeable with no `W` at all**: if the
  first S2 watch is clean, `c ≤ s ≤ S2 finale ≤ T0 < τ1`, so the clean record lands in `A` at any
  `W`. The artifact **computed the split, printed it, and then declared the whole set open.**
  Open population is **4,988 (2.27%)**, not 7,340.
- **F3** — the reproducibility certification was **false, third occurrence**. *"A gate artifact that
  falsely certifies its own reproducibility is worse than one that makes no such claim — the false
  certificate defeats the check the Human Lead would otherwise run."*

### Round 4 — PROCEED

Scoped by the Human Lead to two items: grep-verify F3 is closed, and confirm F1's recomputation.
All thirteen figures passed both halves. **But the certification overclaimed a fourth time**, in
four ways — including a blanket "no figure is produced outside `src/`" falsified by a decorative
"up to 164 accounts share one instant."

> **PROCEED.** … The rule is sound, the population is determinate, and every residual is a sentence
> rather than a number — with the single exception of "164", which is decorative. Holding here
> would be scrupulosity, not review.

**Committing the decorative 164 revealed it was also wrong — the true maximum is 198.** It had been
the maximum over the first 4,000 of 155,626 groups in an exploratory shell. `mode3_flags.npz` is
byte-identical after recomputation. **An uncommitted figure was also an unverified one, which is
what B3, D3 and F3 were all about.** That is the lesson, not the number.

Round 4 also found the **gap inside F1's own derivation** — see the floor qualifier below.

## The four rulings made inside the gate — all now closed in `0021`

1. **D1 — Step 1 §7 stands, gate 1 is not reopened.** The revision-3 principle is withdrawn.
2. **Adoption 1 narrowed to option (b)** — the stamp classifies the pair by itself **only where all
   S2 evidence carries it**. 16,665 out, the 23,067 with no guaranteed direction retained.
3. **Adoption 2 re-ruled onto the censoring rationale** — not "cannot be evaluated."
4. **Adoption 3 dropped.** *"A post-dated record is an inaccurate timestamp on an episode that was
   watched, which is protected everywhere else in this rule."* This is what made the `W` sample
   **determinate at 128,099** — removed by the ruling, not resolved by argument.

## The two standing rulings that outlive the gate — and are now in the task sheet

Both are Human Lead rulings made **during** Step 5, and both bind steps that are not Step 5.

1. **Ruling 1 — "W is derived on clean records and applied to all."** Produces two populations:
   analysis **201,900**, W estimation sample **128,099**. Step 6 applies D14's C1 restriction **on
   top**, so the estimation sample is **two-factor: cadence and provenance.** `0021` notes this is
   **the same shape as the already-approved D14**, where `W` is estimated on C1 only and applied to
   every show — one transfer assumption, applied twice on different axes.
2. **Ruling 2 — liveness runs on record insertion time, not claimed watch date.** *"Any record
   inserted after the window closed proves the account was alive, whatever date it claims —
   backfilling an old show is still activity."* This **withdrew Layer 3** (35,861 pairs) whose sole
   premise was that import noise is not liveness evidence. It makes the play-`id` calibration a
   **required input to Step 7**, not a Step 5 diagnostic.

   > **Ruling 2 was AMENDED and the amendment REVERTED, both on 2026-08-14.** `0053` amended it to
   > *"an insertion after the window FOR THE QUESTION BEING ASKED proves the account was alive for
   > that question"* — one window per null, `τ1` for never-started and `τ2` for started-and-left —
   > on the premise that *"after the window closed"* was written when there was one window and had
   > since been read as *"after `τ1`"* **only by accident.** **`0054` withdrew `0053` in its entirety
   > and reverted the amendment.** The premise was false: **`0034`, the entry that created the second
   > window on the same date, ruled *"Liveness stays anchored at `τ1`"*** and `0051` re-affirmed it
   > with both windows in view. **`0053` amended this gate while leaving `0034` standing, uncited and
   > unmentioned.** **Ruling 2 stands exactly as approved**, and `0048` §9's *"insertion after `τ1` ⟹
   > live"* is restored.
   >
   > **Two things Step 18 should take from it.** First, the study's own gate-reopening rule was
   > invoked correctly — `0053` **stated** it was an amendment to an approved gate rather than a
   > gloss, which is the behaviour `0012` failed to show. Second, **stating it was not enough**: the
   > check that would have stopped it is *"which live rulings does this amendment contradict,"* and
   > nobody ran it until Red Team's seventh Step 7 HOLD.
   >
   > **`0021` Adoption 3 became load-bearing in the revert.** It keeps post-dated records, so a
   > record inserted at instant `s` can carry any `watched_at ≤ s` — which is what falsifies `0053`'s
   > warrant that a pair silent from `s ∈ (τ1, τ2)` *"could not have produced the evidence the
   > Continued test reads."* It could; only evidence dated in `(s, τ2)` was out of reach.

**Both were written into `task-sheet.md` as `0022` on 2026-08-12, before Steps 6 or 7 launched.**
Step 6 now names the 128,099 sample, states that it **composes with D14 rather than replacing it**,
publishes the waterfall, and says outright that **201,900 and 128,099 are different numbers**. Step 7
now names insertion time as the clock, amends the gap-distribution item to say **insertion instants**
rather than "logged events", and adds the clause that carries the most weight for the dual run:

> **The play-`id` insert-time calibration is a required input, and neither instance refits it.**

**Two independently refitted isotonic curves would differ**, and the diff would then confound a
calibration difference with an implementation difference — the one thing the dual run exists to rule
out. Both instances read the stored curve at `processed/step5/calibration.npz`.

**The general lesson, README item 23:** *when a gate ruling changes what a downstream step computes,
propagate it to `task-sheet.md` at the time of the ruling, not at the time the step launches.*
Because **the dual-implementation diff cannot catch a spec omission** — both instances read the same
silence and agree on the wrong answer, and the diff reports agreement. Three gates remain and each
will produce rulings with downstream reach.

## The four limitations that travel to Step 14 — not decisions

1. **4,988 partly-air-date-stamped pairs** retained, each holding an S2 record inside the window by
   construction and each being that pair's **earliest** S2 evidence.
2. **Adoption 1's "entirely" boundary is practical, not principled.** It excludes on a guarantee
   that 4,988 retained pairs also carry. The 2,352 closure reduced the inconsistency; it did not
   remove it.
3. **Two bias statements that must not be netted.** (a) An **exact** population change whose net is
   **up** — 16,665 Started pairs removed against 1,542 Never-started, ten to one. (b) A separate
   **estimator bias** whose direction is **down**, making the reported never-started share a
   **floor**, bounded above at ~22% of retained pairs with **no point estimate**.
   **The floor carries a qualifier that must be published with it:** structurally guaranteed for
   **8,372** retained pairs (air-date-stamped and pre-1990 corrupt) and **assumed** for the other
   **42,019 (90.1%)** — because `backfilled` means claimed ≪ **insert**, not claimed < **true**. A
   user who watched in 2015, imported in 2026, and whose import wrote 2018 produces a backfilled
   record **later** than truth, running *against* the floor. Red Team round 4 named the conflation
   precisely: §7 applies the early-skew premise to **observed claimed date vs the finale**, both on
   disk and checkable; §13.2 applies it to **claimed vs true**, and the true date is what the
   contamination destroyed.
4. **Modes the instrument cannot see** — same-day bulk-marking (**38.2%** of surviving distinct
   episode-days sit on a day carrying >48 distinct episodes), a `T0` too early when the finale
   binds, and the cohort's **1,539 absent accounts**.

## Shape 3, and why the analysis population must not be a function of `W`

Three shapes were available for the 4,988: exclude now, exclude none, or defer the test to Step 8
where `W` exists. **The Human Lead rejected the third:**

> Leave the 4,988 open and state it in Step 14. Do not make the analysis population a function of
> `W`. Shape 3 would break the dual-implementation control, which is worth more than recovering 2.3
> percent.

**The cost that avoids:** if the population were a function of `W`, then whenever the two Step 6
instances return different `W` — *the entire reason Step 6 is run twice* — the two Step 8 instances
would classify **different populations**, and the diff would confound an implementation difference
with a population difference. **A population that moves with the parameter under test cannot test
the parameter.** This generalises to every future proposal that makes a filter depend on a
downstream-derived value.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[open-items-and-contradictions]], [[withdrawn-claims-register]], [[decision-log-step18]].
