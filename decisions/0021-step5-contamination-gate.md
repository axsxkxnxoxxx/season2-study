# Decision 0021 — Step 5 contamination exclusion rule APPROVED (gate 2 of 5)

| | |
| :--- | :--- |
| **Decision** | **Step 5 is approved.** The contamination exclusion rule below is adopted. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Gate** | 2 of 5. Unblocks Steps 6, 7 and 8, each of which is itself an unapproved gate |
| **Deliverable** | `artifacts/step5-contamination-diagnostics.md`, revision 6 |
| **Review** | Red Team, **four rounds**. Rounds 1–3 HOLD, round 4 **PROCEED** with four corrections, all applied before approval. Full record at `artifacts/step5-red-team-reviews.md` |
| **Status** | Closed |

> **Approval record.** Approval was given by the Human Lead in writing in this session, on
> 2026-08-12. No agent recorded it on its own authority and no agent adopted its own proposal. The
> analytics-engineer produced and revised the artifact; the red-team agent reviewed it and
> recommended; neither approved it.

---

## The approved rule

Applied to the 220,107 S1-completer pairs of the Step 2 frame.

| | Pairs |
| :--- | ---: |
| **Exclude:** S2 evidence **entirely air-date-stamped** | **16,665** |
| **Exclude:** no S2 evidence **and** a fabricated binding clock start | **1,542** |
| **Retained analysis population** | **201,900 of 220,107 — 91.73%** |
| **`W` estimation sample** | **128,099** |

The two exclusions are **disjoint by construction** — one set has S2 evidence, the other has none —
so they add without overlap. The analysis population and the estimation sample are **different
populations** and must stay visibly distinct downstream.

**The first exclusion rests on a deterministic mechanism, not on untidiness.** An air-date stamp
writes the episode's original broadcast instant, and for an S2 episode that instant is
`≤ S2 finale ≤ T0 < τ1` by construction. Such a record therefore lands in `A` on its own and forces
`|A| ≥ 1`, so the pair cannot score Never started whatever the viewer did. Where **all** S2 evidence
carries the stamp, the timestamp classifies the pair by itself.

**The second rests on a censoring defect.** A fabricated-early `T0` lets a pair pass the Step 1 D10
right-censoring test it should have failed. On the insert-time bound these pairs have a median of
**40 days** of elapsed observation and **58.63% are still inside an open window at `W = 60`**.

**Everything else is retained**, including 23,067 contaminated pairs that hold S2 evidence, because
their contamination carries no guaranteed direction.

---

## Four rulings made during the gate

### D1 — Step 1 §7 stands. Gate 1 is not reopened.

Red Team found that a governing principle in an earlier revision — *"timestamp accuracy is not a
concern; the outcome is whether someone watched season 2, not when"* — **contradicted the approved
Step 1 §7**, which defines **Never started** as `|A| = 0` where `A` requires `watched_at < τ1`. The
outcome operator is a timestamp comparison, and D8 exists precisely to count never-started pairs
that *do* hold S2 evidence dated after `τ1`.

**Ruled: keep Step 1 §7 as approved.** Reasoning, as given:

> Ever-started is the wrong study for this frame. Exposure spans 55 years and 69 percent of pairs
> are pre-2020, so a to-the-pull-date rate would be a mixture weighted by show recency and newer
> titles would look worse by construction. It also collapses "started four years late" and "started
> opening week" into one row, which is the conflation this study exists to break.

The principle is withdrawn. Everything in the rule is justified against Step 1 §7.

### Adoption 1 — narrowed to option (b)

The stamp classifies the pair by itself **only where all S2 evidence carries it**. The 16,665 are
excluded; the 23,067 whose contamination has no guaranteed direction are retained.

### Adoption 2 — re-ruled onto the censoring rationale

The 1,542 were first excluded as "cannot be evaluated." That reason is wrong: a pair with zero S2
records has `|A| = 0` for **every** `τ1` and is perfectly evaluable. **They are excluded because a
fabricated-early `T0` lets them pass a censoring test they should fail** — a censoring defect, not
an evaluability defect.

### Adoption 3 — dropped

A proposed exclusion of post-dated records is **not adopted**. Reasoning, as given:

> A post-dated record is an inaccurate timestamp on an episode that was watched, which is protected
> everywhere else in this rule.

Post-dated records are **tagged** in Layer 1 and **kept out of the `W` estimation sample**; no pair
is deleted for post-dating, and 3,296 such pairs remain in the analysis population. This also closed
an indeterminacy Red Team had identified: with the re-dating reading no longer a candidate, the `W`
estimation sample is **determinate at 128,099** — removed by the ruling, not resolved by argument,
because nothing about the data changed.

---

## Two standing rulings that outlive Step 5

1. **`W` is derived on clean records and applied to all.** The population that can answer the timing
   question sets the rule; the rule applies broadly. Same shape as the already-approved D14, where
   `W` is estimated on C1 shows only and applied to every show.
2. **Liveness runs on record insertion time, not claimed watch date.** Any record inserted after the
   window closed proves the account was alive, whatever date it claims — backfilling an old show is
   still activity.

   > **AMENDED 2026-08-14 (`decisions/0053`) — an amendment to an approved gate, not a clarification.**
   >
   > **This ruling was written when there was ONE window.** "After the window closed" was unambiguous
   > then. **The Step 1 §7 amendment (`0034`) created two** — never-started is read at `τ1`, Continued
   > at `τ2` — and the ruling has since been read as "after `τ1`" **only by accident of when it was
   > written.**
   >
   > **The amended reading: an insertion after the window FOR THE QUESTION BEING ASKED proves the
   > account was alive for that question.**
   >
   > - **Never-started is read at `τ1`**, so activity after `τ1` licenses its null.
   > - **Started-and-left is read at `τ2`**, so activity after `τ1` but silence from before `τ2` does
   >   **not** license it — **the pair could not have produced the evidence the Continued test reads.**
   >
   > **That is what this ruling meant with one window, and it is what ALT-MATCHED implements**
   > (`0052`). **`0048` §9's gloss — "insertion after `τ1` ⟹ live" — is WITHDRAWN**: it was a
   > one-window reading carried into a two-window rule.
   >
   > **Measured consequence:** under ALT-MATCHED **90 APPLY and 89 DERIV exclusions show an insertion
   > after `τ1`** — 47.3% of DERIV's whole exclusion set. Under the withdrawn gloss every one of them
   > would have been forced live; under the amended reading they are correctly not live, because their
   > silence begins before `τ2`.

3. **The flip bound is weak: 0 to 44,458 at `W = 60`**, 22.0% of the retained population. The
   insert-time test rules out only ~5% of candidates, because a backfilled record is by definition
   written long after the date it claims. **No point estimate exists and none should be inferred.**
4. **The exclusion bias is not neutral and its direction is known.** The population change is exact:
   1,542 removed pushes never-started **down**, 16,665 removed pushes it **up**, **net up by 15,123
   pairs**. The estimator bias on the retained population runs **down**. These are different kinds
   of quantity — a population change and an estimator bias — and **must not be netted into a single
   direction.**

---

## Three errors recorded rather than corrected silently

All three originated in the main session, not in the deliverable. Two of them entered rulings before
being caught, which is why they are on the record rather than quietly fixed.

1. **The C5 count** was reported as 4,188 against the artifact's 5,694, on the stated basis that a
   column for air-date-stamped S1 evidence did not exist. It did — it had been added one revision
   earlier, after the header was read. **5,694 is correct.**
2. **"All 425 C5 pairs with no S2 evidence are already inside the 1,542"** was false. The two sets
   are **disjoint by construction** — C5 requires a clean completing record, the 1,542 a
   contaminated binding one — and the correct count is **720**. A ruling cited this claim as half
   its basis. The conclusion survived on the insert-time evidence, which is a different and better
   basis.
3. **The insert-time bound quoted for the 720 — "median 2,150 days, 8.1%" — was wrong.** The cause
   was a unit bug: `.astype("int64")` on a tz-aware datetime returns **microseconds** in the pandas
   version in use, so dividing by 1e9 placed every S2 finale date in **January 1970** and the
   `max()` with the finale term was silently inert. The figure to use is **1,738 d / 7.92%**. A
   ruling cited the wrong one; the conclusion holds under every variant of the bound.

Full detail and the corrected four-cell grid: `artifacts/step5-red-team-reviews.md` §5.

**A pattern worth carrying forward.** A related class of defect recurred three times inside this
gate: figures printed in the artifact that no committed code produced. When the last such figure was
finally committed, it turned out to be **wrong as well as uncited** — a maximum of 198, not the 164
that had been printed, the 164 having come from the first 4,000 of 155,626 groups in an exploratory
shell. An uncommitted figure is also an unverified one.

---

## What this unblocks

| Step | Takes from Step 5 |
| :--- | :--- |
| **Step 6** — window `W` | the **128,099** estimation sample, with D14's C1-only restriction applied on top |
| **Step 7** — liveness threshold | the play-`id` insert-time calibration, as a **required input** under the standing ruling |
| **Step 8** — analysis table | the **201,900** analysis population and the Layer 1 record tags |

Steps 6, 7 and 8 are themselves unapproved gates. Steps 6, 7 and 9 run twice under
`data-scientist` and `data-scientist-b`; Step 8 runs twice under `analytics-engineer` and
`analytics-engineer-b`. Nothing downstream of those gates runs without written approval at each.

**The frame this rule applies to remains a stopped pull** — 2,549 users of 4,050 planned, 62.9%,
proportional across all ten strata to within 6.1 points. If the pull resumes, the frame grows and
every count in this entry is recomputed.
