# Season 2 Abandonment Study: Task Sheet

## Context for anyone picking this up cold

The industry is arguing about why second seasons lose audience. Every public number is an aggregate that cannot tell the difference between a person who never started season 2 and a person who started and quit. Those are opposite problems requiring opposite fixes. This study measures the split at the individual level using public Trakt watch histories.

**Definition of done:** a published write-up with a live link, a results visualization, a decision rule, and a decision log.

---

## Roles

**Human Lead.** The person directing this project. Owns Steps 2, 14, 15, 17, and 18. Approves all five gates. Selects the segment cut in Step 12 and specifies the visualization in Step 16. When a step says Human Lead, no agent may act on it.

**Nine agent roles, eleven agent files.** Dual implementation requires a second identical copy of Data Scientist and of Analytics Engineer, differing only in the `name` field.

| Role | Files |
| :--- | :--- |
| Analytics Engineer | 2 |
| Data Scientist | 2 |
| Second Brain | 1 |
| Red Team | 1 |
| Reviewer: Product Management | 1 |
| Reviewer: Merchandising | 1 |
| Reviewer: Design | 1 |
| Reviewer: Consumer Insights | 1 |
| Reviewer: Engineering | 1 |

Orchestration is handled by the main session and the Human Lead. Standing rules for it live in `CLAUDE.md`, not here.

---

## Where files go

This section is binding. Read it before writing any file.

| Folder | Contents | Git |
| :--- | :--- | :--- |
| `artifacts/` | Deliverables: specs, charts, reports, summary tables | Tracked. Public. |
| `decisions/` | Decision log, one file per gate | Tracked. Public. |
| `raw/` | Raw API responses | Ignored. Never leaves the machine. |
| `processed/` | Intermediate tables | Ignored. Never leaves the machine. |
| `logs/` | Pull logs, error logs, run records | Ignored. Never leaves the machine. |

**Hard rule:** no file containing usernames, user IDs, or individual watch histories may be written to `artifacts/` or `decisions/`. Aggregates and counts only. If unsure whether a file qualifies, write it to `processed/` and ask the Human Lead.

This table also appears in `CLAUDE.md` and in every agent definition. If any two copies ever disagree, `CLAUDE.md` is the source of truth.

---

## Standing roles (no steps owned)

### Second Brain

Second Brain does not observe passively. It is a subagent and runs only when the Human Lead invokes it. Its memory directory does not exist until it first writes.

**Invoke it after every gate approval and after every result step.** Roughly ten times across the build. Skipped invocations mean the decision log has to be reconstructed at the end, which is the failure this role exists to prevent.

- [ ] Ingests every artifact, gate decision, red team transcript, and partner verdict it is given
- [ ] Maintains a live glossary of terms and thresholds with where each was set
- [ ] Runs consistency checks across steps
- [ ] Flags contradictions between what was approved at a gate and what downstream work assumed
- [ ] Writes only to its own memory directory. Writes nothing to `artifacts/`, `decisions/`, or any project folder.
- [ ] Carries no usernames, user IDs, or individual watch histories into memory. Project-scope memory is version controlled and public.
- [ ] Never sits in the critical path and cannot block or break anything

### Red Team

Fresh context on every review. Sees the output and the spec, never the reasoning that produced it.

**Brief at gates (Steps 1, 5, 6, 7, 8):** find the reason this rule is wrong. Assume it is. Name the alternative. Return a verdict of hold or proceed.

**Brief at results (Steps 9 through 13):** quote the specific sentence being claimed. State what the table would have to show for it to be true. Say whether it does. No general commentary.

### Partner reviewers

Review only. Never produce work. Each fires at its assigned step, not at the end. Every reviewer must return a position. "Interesting, some considerations" is a failed brief.

---

## Step 0: Access and setup

**Owner:** Analytics Engineer
**Mode:** Chained

The Trakt API application is already registered. The Client ID is in `.env` and is loaded at runtime. It is never written into a code file, a log, or an artifact.

The rate limit and the authentication answer are settled and recorded in `CLAUDE.md`. Trakt allows 1000 GET calls per 5 minutes at the application level, which is 200 per minute. Every endpoint this study uses is OAuth Optional and works with the Client ID alone on public profiles.

- [ ] Build a resumable client that throttles at 150 calls per minute, never at the 200 ceiling
- [ ] Use the Client ID alone. Do not build an OAuth flow.
- [ ] Log private profiles and move on. They return nothing.
- [ ] Retry with backoff on transient failures: timeouts, connection errors, and 5xx responses
- [ ] On a 429, read `Retry-After`, pause that many seconds, then resume. Never retry the same request in a loop. If 429s persist across several consecutive pauses, stop and report.
- [ ] Log the status, the `X-Ratelimit` object, `Retry-After`, the endpoint, and the method on every rate-limit event
- [ ] On a 403, hard stop and report. That is a block, not a throttle.
- [ ] Persist raw responses to `raw/` before parsing
- [ ] Never re-request what is already on disk

**Deliver:** working client, one successful test pull, documented rate limit
**Review:** Reviewer: Engineering on infrastructure constraints

---

## Step 1: Outcome definition

**Owner:** Data Scientist drafts
**Mode:** GATE. Requires written approval from the Human Lead.

- [ ] Unit of analysis: one user, one show
- [ ] Season 1 confirmed complete: watched the S1 finale AND at least 90 percent of S1 episodes
- [ ] Clock start: the later of the S2 finale date and the user's own first-pass S1 completion date. Not the premiere.
- [ ] Define three mutually exclusive outcome states: never started, started and left, continued. **AMENDED 2026-08-12 (`decisions/0034`): never-started is measured at `τ1` = clock start + `W` = 108 days; Continued is measured at `τ2` = clock start + `W + H` = 199 days.** The two published categories are measured over different horizons and must never be described as measured alike
- [ ] Abandonment point: highest S2 episode watched as a fraction of season length
- [ ] Count distinct episodes, never play events, to exclude rewatches
- [ ] W is not set at this step

**Deliver:** written definition doc in `artifacts/`
**Review:** Red Team, verdict hold or proceed
**Approval:** nothing proceeds until the Human Lead approves. No code runs first.

---

## Step 2: Show frame

**Owner:** Human Lead
**Mode:** Runs in parallel with Steps 0, 1, and 3

- [ ] Include shows with two or more seasons where S2 finished airing on or before **31 Dec 2025** (Human Lead, `decisions/0014`; this line read 2024 until 2026-08-12 and the frame was built at 2025 — see `decisions/0030`)
- [ ] Exclude anime
- [ ] Trim high-frequency cadence outliers such as daily strips and soaps
- [ ] Collect as fields and not filters: origin, platform, country, language, genre
- [ ] Collect as fields and not filters: S1 and S2 episode counts
- [ ] Collect as fields and not filters: S1 finale date, S2 premiere date, S2 finale date, gap length
- [ ] Record the count removed at each rule

**Deliver:** show frame table plus exclusion ledger in `artifacts/`
**Review:** Reviewer: Product Management. Verdict on whether the frame matches what a roadmap would need.

---

## Step 3: User discovery

**Owner:** Analytics Engineer
**Mode:** Chained

- [ ] Channel A: seed a few hundred public profiles, walk the follower graph outward through the API
- [ ] Channel B: collect owners of public lists
- [ ] Tag every username with its source channel. Required, not optional.
- [ ] Do not harvest usernames from comments on the shows being measured. That selects on the outcome.
- [ ] Run until usable-user yield plateaus
- [ ] Write the username pool to `raw/`. It never goes to `artifacts/`.
- [ ] Write the yield curve, which contains counts only, to `artifacts/`

**Deliver:** username pool with channel tags in `raw/`, yield curve in `artifacts/`
**Checkpoint:** the Human Lead reviews the yield curve before Step 4 runs at full scale. Not a gate, but Step 4 does not scale up without it.

---

## Step 4: Pull watch histories

**Owner:** Analytics Engineer
**Mode:** Chained

- [ ] Pull full episode-level watch history with timestamps for each discovered user
- [ ] Store raw in `raw/`, parse separately into `processed/`
- [ ] Log failures and private profiles to `logs/` rather than dropping silently
- [ ] Checkpoint continuously so the job survives interruption

**Deliver:** raw history store in `raw/`, pull log with success, private, and error counts in `logs/`, summary counts in `artifacts/`
**Review:** Reviewer: Engineering on throughput and failure rates

---

## Step 5: Contamination diagnostics

**Owner:** Analytics Engineer proposes
**Mode:** GATE. Requires written approval from the Human Lead.

TV Time shut down 15 July 2026 and users bulk-imported into Trakt. Imported timestamps are backfill, not real watch dates. Both W and the liveness rule run on timestamps, so this must be caught before either is derived.

- [ ] Flag accounts showing implausible bursts of historical logging concentrated in a short real-time span
- [ ] Flag bot and duplicate accounts
- [ ] Report the share of history that is plausibly backfilled overall
- [ ] Propose an exclusion rule. Do not adopt it.

**Deliver:** contamination report with counts and a proposed exclusion rule in `artifacts/`
**Review:** Red Team
**Approval:** nothing downstream runs until the Human Lead approves the exclusion rule

---

## Step 6: Derive window W

**Owner:** Data Scientist, dual implementation
**Mode:** GATE. Requires written approval from the Human Lead.

W is a number of days. It is derived here and used everywhere downstream.

- [ ] **Derive W on the Step 5 clean-record estimation sample: 128,099 pairs.** Human Lead decision, 2026-08-12, at the Step 5 gate (`decisions/0021-step5-contamination-gate.md`). The population that can answer the timing question sets the rule, and **the resulting W applies to ALL pairs**, including those the sample excludes. This is the same shape as D14 below — estimation sample and application population differ deliberately — and it composes with it: **the C1 restriction applies on top of the 128,099, not instead of it.** The sample and its waterfall (201,900 → 178,165 → 155,131 → 152,126 → 128,099) are published in `artifacts/step5-contamination-diagnostics.md`; both instances take the population from there rather than re-deriving it, so a difference in the diff is an implementation difference and not a population one. **The analysis population is 201,900 and is a different number — do not confuse them.**
- [ ] Restrict to users who did start S2
- [ ] **Estimate W on bucket C1 (all-at-once) shows ONLY, per the D12 classifier in Step 1 §10.0. C1 is the estimation sample; C0, C2, C3 and C4 are not.** Human Lead decision, 2026-08-10. Use the bucket name, not the words "binge shows" — both isolated instances must select the same rows from the same frame without consulting each other. On a C1 show the premiere and finale coincide, so every lag is non-negative by construction and the lag measures the one thing W is meant to capture.
- [ ] Anchor the lag on the S2 finale date, not the premiere, for weekly-release shows
- [ ] Plot the lag distribution from clock start to first S2 episode
- [ ] **Set `W` at the 90th percentile of the observed lag distribution on the C1 estimation sample.** Human Lead decision, 2026-08-12 (`decisions/0024-w-is-the-90th-percentile.md`). **This is a percentile, not a curve-flattening judgment.** Rationale: attribution-window practice sets the window at or slightly above the 90th percentile of the time-to-conversion distribution, with 75th to 90th the cited range. **The previous wording — "set W at the percentile where the curve flattens" — is withdrawn.** It produced two honest readings from two isolated instances **61 days apart** (46 and 107), because "flattens" was never defined and the lag tail is close to scale-free past about day 7, so there is no break in the density to read. Take the percentile of the **signed, untruncated** lag distribution as it stands, with no truncation, clipping, absolute values or dropped rows — see the negative-mass rules below, which are unchanged and still apply.
- [ ] **Measure the lag as a continuous instant difference, and take `W` as the CEILING of the resulting percentile.** Human Lead decision, 2026-08-12 (`decisions/0025-lag-unit-and-ceiling.md`). Do **not** floor the lag to whole days before taking the percentile, and do **not** floor or round the percentile itself. The reason is the window test, not a rounding preference: `τ1 = ⟦T0⟧ + W × 24h` and a pair is inside iff `watched_at < τ1`, so a pair is covered iff its **fractional** lag is strictly less than `W`. Flooring the lag puts a pair whose true lag is in `[107, 108)` at "107" while the test excludes it from a `W = 107` window — a systematic off-by-one **against** the operator the window is evaluated by. On the C1 sample the true percentile is 107.7135: `W = 107` covers **89.976%** and `W = 108` covers **90.020%**, so only the ceiling delivers the 90th percentile the rule asks for. **Two isolated instances differed by exactly one day on this and neither was wrong**, which is why it is written down.
- [ ] **Apply the resulting W to ALL shows, not only to C1.** Estimation sample and application population are deliberately different.
- [ ] **Plot the C1-only and all-shows lag distributions together**, so the reader can see how far the transfer assumption is being stretched

**Rule for the negative mass in the all-shows plot.** Human Lead decision, 2026-08-10. D14 removes negatives from the *estimation* sample only; the all-shows plot still carries them, and for a weekly show the negative mass is most of the started population rather than a tail. This step is dual implementation and Step 13's tested range is derived from this plot, so the handling is fixed here rather than left to each instance.

- [ ] **Plot the all-shows distribution SIGNED and UNTRUNCATED.** Negative lags appear at their actual values. **Do not truncate at zero, do not clip, do not take absolute values, and do not drop negative rows.** Truncation was withdrawn as indefensible: it maps every live weekly viewer to a point mass at zero whose height is set by the frame's cadence mix, making W an artifact of the frame rather than a fact about viewers
- [ ] **Never read W, or any percentile used to set W, off the all-shows curve.** W is read off the C1 curve only. The all-shows curve is descriptive: it exists to show the size of the transfer assumption, not to estimate anything
- [ ] **Report the negative mass as a count and a share of the started population, split by all five D12 buckets.** That split is the evidence that the negative mass is a cadence artifact and not viewer behaviour
- [ ] **Derive Step 13's W range deterministically from the two curves:** take the same percentile used to set W on C1, read it on the C1 curve and on the all-shows curve, and report both values. That interval is the minimum range Step 13 must cover. Stating the percentile once and reading it on both curves is what keeps two instances from producing different ranges
- [ ] State the percentile and the reason in one sentence
- [ ] State whether the C1 sample was large enough to support the percentile. That is a Step 6 question with the data in hand.

**Deliver:** lag distribution chart, chosen W, one-sentence justification, all in `artifacts/`
**Check:** two isolated instances run the same spec. The Human Lead diffs the numbers before reviewing.
**Review:** Red Team
**Approval:** this number must be defensible out loud. The Human Lead does not approve a value they cannot explain.

---

## Step 7: Liveness rule

**Owner:** Data Scientist, dual implementation
**Mode:** GATE. **RULE CHANGED to ALT-MATCHED 2026-08-14 (`decisions/0052`). Reruns pending; NOT approved.** Prior reruns on ALT-BROAD completed and both arms agreed on every published figure except one, reconciled at `0052` §6.

> ## THE RULE
>
> **A user-show pair is NOT LIVE if and only if EITHER:**
> - **`|A| = 0` AND the account shows no insertion instant after `τ1 = ⟦T0⟧ + W × 24h`; OR**
> - **`|A| ≥ 1` AND the pair is NOT Continued AND the account shows no insertion instant after
>   `τ2 = ⟦T0⟧ + (W + H) × 24h`.**
>
> **Otherwise it is live. Each null is tested at the instant its own outcome is read** — never-started
> at `τ1`, started-and-left at `τ2`. (`decisions/0052`, superseding ALT-BROAD's single `τ1` test.)
>
> **The second conjunct is the ruling, and it reaches BOTH nulls.** Liveness licenses trusting a null.
> **Under `0034` only Continued is established by positive evidence** — `F2 ∈ A_H` and
> `|A_H| ≥ ceil(0.90 × L2)`. **Never started is a null** (`|A| = 0`). **Started and left is ALSO a
> null**: `|A| ≥ 1` is observed, but **the failure to meet the Continued condition is not.**
>
> **And it is structural, not incidental.** `τ2 > τ1`, so **a pair silent after `τ1` is silent after
> `τ2` and can produce no evidence anywhere in the `[τ1, τ2)` window the Continued test reads.** It is
> scored "left" **by construction** — the exact failure liveness exists to prevent, applied to the
> second headline category. **This study is "never started versus started and quit"; both halves need
> the guard.**

**EVERY FIGURE BELOW STATES ITS POPULATION. There are two and they differ by construction:**

- **DERIV** — Step 5 line 4 less D10, **147,370**. **Requires S2 evidence.**
- **APPLY** — line 1 less D10, **196,654**. **This is what Step 8 filters at position 6.**

- [ ] **Exclusions: 99 pairs on DERIV (73 accounts), 703 on APPLY (216 accounts)** at `W = 108` — **604 never-started plus 99 started-and-left**. Under the superseded ALT the counts were 0 and 604. A Step 7 instance reporting 0 on DERIV and 604 on APPLY is correct and the two are **not** a divergence.
      **How the rule selects, under ALT-BROAD (`decisions/0049`):** **conjunct 2 (NOT Continued) narrows APPLY 196,654 → 52,514; conjunct 1 (no insertion after `τ1`) narrows 52,514 → 703.** *(Under the superseded ALT it was 196,654 → 33,373 → 604.)* **Conjunct 1 does most of the work**, which is why the count moves with `W`. **The 604 are NOT "exactly the pairs with no S2 record anywhere"** — APPLY holds **23,260** such pairs and **22,656 stay live**. Subset, not equality.
      **The DERIV zero is NOT forced by construction.** `has_s2` does **not** imply `|A| ≥ 1` — `|A|` needs an **in-`E2`** record — and **9,145 DERIV pairs are never-started**. Four line-4 pairs hold S2 records with no `E2` episode number, satisfy **both** conjuncts at every arm, and are removed one position earlier by **D10**. **The zero comes from the filter order and this pull date.**
- [ ] **Liveness runs on record INSERTION time, not claimed `watched_at`** (`decisions/0021`, gate 2 of 5). **Any record inserted after the window closed proves the account was alive, whatever date it claims.**
- [ ] **Read the stored play-`id` isotonic calibration at `processed/step5/calibration.npz`. NEITHER INSTANCE REFITS IT** (`0029`).
- [ ] **Liveness is a PAIR-LEVEL filter, anchored at `τ1`** (`0034`). Evidence is account-wide; the test is clock-start-relative and clock start is pair-specific. **One account can be live for one show and not another. Never drop a user wholesale.**
- [ ] **`τ2` DOES play a part, and the earlier "`τ2` plays no part" is WITHDRAWN (`decisions/0049`).** Under ALT-BROAD the **second conjunct IS the Continued test, which is read at `τ2 = ⟦T0⟧ + (W + H) × 24h` on `A_H`.** What remains true, and is what the withdrawn line meant: **the SILENCE test is anchored at `τ1` and only at `τ1`** (`0034`). **The rule reads two instants: silence at `τ1`, Continued at `τ2`.**
- [ ] **Do not reintroduce a pre-`τ1` requirement in any form.** Withdrawn twice — `0040` §1 and `0042` §3 — both times for contradicting gate `0021`.
- [ ] **Waterfall line 6 becomes OUTCOME-CONDITIONAL, and the spec says so** (`0046`). `|A| = 0` is evaluated before liveness is applied. **That is permitted and both arms proved it**: `|A|` and liveness are **row-local predicates on the position-5 output and commute exactly**, and `0029`'s ordering rationale is about **per-filter sample size**, which cannot reach position 7 because **outcome assignment removes no rows** — positions 1–6 are filters, position 7 is an annotation. **Report line 6 as outcome-conditional so two instances do not diverge on the waterfall while agreeing on every share.**
- [ ] **Monotone decrease is STRICT on BOTH populations under ALT-BROAD** — 703 on APPLY and 99 on DERIV, at every arm; the empty-set case does not arise (`0049`). **The `>=` coding at Step 8 is KEPT** — see there for why the reason changed but the coding did not.
- [ ] **"NOT Continued" means Step 1 §7 as amended by `0034`** — the negation of `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`, so it covers **both** Never started and Started-and-left. **`|A| = 0` alone is the superseded ALT form and is not the rule.** And `|A| = 0` is Step 1 §7's Never-started condition, **not** "no S2 evidence at all" — the competing reading gives a different set.
- [ ] **Report the exclusion count per `W` arm on APPLY**, so the `W`-coupling is visible (`0044` §1.2, corrected to APPLY by `0046`). **ALT-BROAD on APPLY: 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** at `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213. **The started-and-left component alone runs 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148 — a factor of 2.85, growing faster than the rule's own 1.5× coupling. Report it separately.**
- [ ] **D10 IS RE-DERIVED AT EACH ARM. Name the reading; do not freeze it.** Human Lead ruling, 2026-08-13 (`decisions/0047`). Right-censoring is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which **contains `W`**, so the censored population differs per arm. **Freezing D10 at `W = 108` gives, at `W` = 125 / 150 / 180 / 213: TOTALS 746 / 823 / 918 / 1,117, of which the never-started COMPONENT is 632 / 684 / 753 / 881** (`decisions/0050`). **The 632/684/753/881 figures were re-blessed at `0048` §7 as though they were totals; under ALT-BROAD they are a component**, and a Step 13 instance producing the frozen reading gets 823 / 1,117 and would file a false divergence against 684 / 881. **125 and 180 are not in the mandated grid**, so only the `W` = 150 and 213 entries are comparable to it — a different table. **An arm table that does not name the reading is not reproducible**, which instance A demonstrated by producing both.

### What was deleted, and why the record keeps it

- [ ] **A numeric threshold was derived three times — 632 d, then 1,293 d — and deleted.** Across 787 / 1,293 / 2,200 days and the parameter-free rule, the three outcome shares move **0.026 / 0.038 / 0.012 pp**, roughly **3% of the account-clustered sampling width**, and a continuous 30–4,000 day sweep moves nothing beyond **0.243 pp**. (`decisions/0042`, `0041` §4)
- [ ] **The quota property is why no threshold was defensible.** Taking a percentile of the distribution the test is applied to sets the level by the exclusion rate, not by any feature of the data (`0038` §4). **The data selects which pairs, never how many.**
- [ ] **`0036` §2.3's second edge case is WITHDRAWN** — it contradicted `0021` on 76.8% of the filter's exclusions (`0040` §1). **An account with insertion activity after `τ1` is live.**
- [ ] **`0041` §4's parameter-free wording — "an instant at or before `τ1` and one after it" — is WITHDRAWN.** It reinstated the withdrawn edge case verbatim and would have excluded **18,903 pairs from 1,434 of 2,402 accounts**, moving Continued −0.67 pp and Started-and-left +0.59 pp. **Do not reintroduce a pre-`τ1` requirement in any form.** (`0042` §2)

**Deliver:** the rule statement and the excluded counts, in `artifacts/`
**Check:** dual implementation diff
**Review:** Red Team
**Approval:** required before Step 8

---

## Step 8: Analysis table

**Owner:** Analytics Engineer, dual implementation
**Mode:** GATE. Requires written approval from the Human Lead.

Step 1 §9 hands this step a set of obligations that used to live only in that document. They are written out here, because this is the file the two isolated instances read.

**Filters and order**

- [ ] **Apply the filters in EXACTLY this order.** Human Lead decision, 2026-08-12 (`decisions/0029-step7-threshold-rule-and-w-propagation.md`). The final row set commutes, but **the required per-filter sample size does not** — two faithful instances applying the same filters in different orders would report different waterfalls on an identical table, and the diff could not tell that from a bug.
      **1.** Step 2 frame → **2.** `L2 = 1` exclusion → **3.** S1 completion rule → **4.** contamination exclusion (Step 5) → **5.** right-censoring → **6.** liveness rule → **7.** outcome assignment, **at two instants** — `|A| = 0` tested at `τ1`, the Continued condition tested at `τ2` (`decisions/0034`).
      Rationale for the two that could defensibly swap: **contamination before right-censoring** is already required below. **Right-censoring before liveness** because censoring is a property of the clock and `pull_date` — objective, and independent of behaviour — while liveness is a behavioural inference; running the objective filter first means liveness's marginal cost is measured on a fully observable population, which is the number Step 9's bound needs.
- [ ] **`W = 108 days`**, approved 2026-08-12 (`decisions/0026-step6-window-w-gate.md`). Never-started uses `τ1 = ⟦T0⟧ + 108 × 24h`; **Continued uses `τ2 = ⟦T0⟧ + (108 + 91) × 24h = ⟦T0⟧ + 199 days` (`decisions/0034`)**, with `A_H` the set `A` recomputed at that bound. **`|A| ≥ 1` at `τ1` remains a conjunct of Continued** — dropping it puts a day-150 starter completing by day 190 in two states at once. **The Step 6 deliverables state 107 (`-a`) and 107.7135 (`-b`); neither is the adopted value** — both predate the ceiling ruling in `decisions/0025`. Take the number from the decision entry, not from the artifacts.
- [ ] **Contamination exclusion runs BEFORE right-censoring**, so an import-stamped S1 completion date is counted as contamination rather than laundered into a censoring drop
- [ ] **Exclude `L2 = 1` shows from the headline population** and count them in the waterfall. At `L2 = 1`, Continued is equivalent to Started, Started-and-left is empty by construction, and `p` is never defined
- [ ] **Enforce the set-membership drop rule**: an episode whose `number` is not in the season's listed set `E` is dropped. This is an implementation check, not a data check — under set membership `|D| ≤ L` holds by construction
- [ ] **Every boundary test is the half-open UTC-instant form** of Step 1 §2.4. `date(watched_at) <= T1` must not appear anywhere in the implementation
- [ ] Build one row per user-show pair
- [ ] Include per row: outcome state, abandonment point, discovery channel, and all Step 2 show fields. **Retain `action` as a column** — Step 13 has an arm that needs it
- [ ] Record sample size after each filter

**Required counts, all to `artifacts/`, counts and aggregates only**

- [ ] **Both drop counts**: per show, and **per outcome** — the second being pairs whose entire S2 evidence was dropped, reported as a share of Never started
- [ ] **Negative-lag report (D2)**, split by which term of the `max()` binds
- [ ] **Resumption-rate report — D3′, which replaces D3** (`decisions/0034`). Of pairs scored **Started and left at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, report the **share** completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its **share of all Started-and-left**. **Run at every Step 13 `W` arm, each reporting its own cleared count and share** — the clearance contains `W`, so the subpopulation shrinks from 95.98% of Started-and-left at `W = 46` to 91.34% at `W = 213`. Report alongside, **labelled a count and not a rate**, the 3,440 Started-and-left pairs completing at any point before `τ_pull`, **with its exposure-weighting by show recency stated at the point of use**. The two do **not** bracket the quantity — both truncate observation and neither is a lower bound
- [ ] **Never-started post-window diagnostic (D8)**, measured over `H`, not to the pull date. **Unchanged by `decisions/0034` but no longer D3's symmetric counterpart** — D8 measures over `[τ1, τ2)` and D3′ over `[τ2, τ2 + H)`. **D8(ii) is the only bound on the never-started boundary**, and its size is Step 14's ledger item 10
- [ ] **Split-artifact counts (D9)**, both halves: the fabricated never-started row and the silently deleted S1-failing counterpart
- [ ] **Right-censoring removal as TWO lines** — the `max(W, 91)` term and the incremental `+ H` term — each with its upward direction on the headline named
- [ ] **Retained-pair counts PER AIR PERIOD after right-censoring, not only in aggregate.** Human Lead decision, 2026-08-12 (`decisions/0033-step8-per-air-period-censoring-counts.md`), closing the Product review's finding 5. The aggregate line above says 97.6% of pairs survive censoring at `W = 108` and hides that **the loss is cohort-asymmetric**: at the Step 13 arm of `W = 213` the 2023–2025 cohort loses **10.3%** of its pairs against **2.7%** pre-2020 (`decisions/0030`). Report it **for every `W` arm Step 13 tests**, since the asymmetry widens with `W` and the arms now run to 213. Without this line, whether the modern cohort survives to the headline in usable numbers is invisible — and it is the cohort a roadmap cares about most.
- [ ] **`pull_date`, the earliest and latest per-user fetch dates, and the count of records discarded for `watched_at >= pull_date`**
- [ ] **Per-bucket show and pair counts for all five D12 cadence buckets**, plus the count of shows within 1 day of a bucket boundary
- [ ] **Metadata-disagreement counts**, including the subset where `aired_episodes < |E|` for S2. Listed exceeding aired tightens the 90 percent threshold and pushes real completers out — name that direction
- [ ] Assert invariant: outcome states are mutually exclusive and sum to the sample
- [ ] Assert invariant, every row: **`A ⊆ A_H`** (`decisions/0034`). **Label it a code check, not a data check** — it is true by construction since `τ1 < τ2`, so it can only catch an implementation that computed the two sets wrongly and is not evidence for the rule
- [ ] **Assert invariant: filter counts decrease monotonically — CODED AS `>=`, NOT `>`.** Human Lead ruling, 2026-08-13 (`decisions/0047`). **KEPT, but its stated reason is corrected (`0049`).** Under the superseded ALT the DERIV exclusion set was empty and decrease was non-strict there. **Under ALT-BROAD decrease is STRICT on both populations at every arm.** `>=` is retained because **the invariant must not encode a property of one rule** — a filter position that legitimately removes nothing must not fail an assertion, and Step 13's arms and Step 8's other positions can produce exactly that.
- [ ] **Expect 703 liveness exclusions at position 6, `W = 108` — 604 never-started plus 99 started-and-left — and treat a mismatch as a POPULATION defect before an implementation one.** Human Lead ruling, 2026-08-13 (`decisions/0047`). Step 7 measured 604 on the application population, but built it from the Step 5 pair table rather than through positions 1–5. **A different count most likely means the frame join, the `L2 = 1` exclusion or the censoring differs — not that the liveness rule was coded wrong.** Check the population first.
- [ ] Assert invariant: distinct episodes never exceed season length
- [ ] Assert invariant, for every row: clock start is on or after the S2 finale date, clock start is on or after the first-pass S1 completion date, and clock start equals one of those two dates. The old invariant, no clock start precedes an S2 premiere, is vacuous under a finale-anchored clock and catches nothing. **This check must compute the first-pass S1 completion date INDEPENDENTLY, not read back the pipeline's value** — otherwise its equality clause proves nothing.
- [ ] Report all invariant results
- [ ] Write the table to `processed/`. The filter waterfall and invariant report, which are counts only, go to `artifacts/`.

**Deliver:** analysis table in `processed/`, filter waterfall and invariant report in `artifacts/`
**Check:** dual implementation diff
**Review:** Red Team on the filter order and the invariant set
**Approval:** required before any result is computed

---

## Step 9: Headline result

**Owner:** Data Scientist, dual implementation
**Mode:** Chained

- [ ] Of users who completed S1, compute the share who never started S2
- [ ] Compute the share who started and left
- [ ] Compute the share who continued
- [ ] Attach confidence intervals
- [ ] ~~**TEST WHETHER THE HEADLINE IS SENSITIVE ACROSS THE LIVENESS THRESHOLD'S CLUSTERED INTERVAL.**~~ **DISCHARGED and WITHDRAWN 2026-08-13 (`decisions/0046`).** The test was run, the headline was insensitive — 0.026 / 0.038 / 0.012 pp across 787 / 1,293 / 2,200 days — **and the threshold was deleted at `0042`. There is no interval to test across.**
- [ ] **Compute the never-started bound over the liveness exclusions scored NEVER STARTED. On APPLY: [16.6633%, 16.9704%], width 0.3071 pp, BOTH ENDPOINTS ON 196,654.** The ceiling equals the unfiltered share **as an identity**; both endpoints are attainable. **The 99 started-and-left exclusions enter neither endpoint, so this bound is IDENTICAL under ALT and ALT-BROAD.**
      **Superseded, and the record keeps them:** `0046` published **[16.7146%, 16.9704%]** — floor on 196,050, ceiling on 196,654, **mixed denominators**, and its floor sat **0.0513 pp above** the case liveness guards against. `0045` published **[16.7789%, 17.0355%]** for PF-LIMIT with the same defect. **Three consecutive bounds had an endpoint that did not cover the case the filter exists for** (`0047` §3); the standing rule is that **an endpoint states the population it is computed on and the estimand it bounds, and they must be the same population.**
- [ ] **Compute a SECOND bound, on the started-and-left share, OVER ALL 703 EXCLUSIONS. On APPLY: [9.6830%, 10.0405%], width 0.3575 pp, both endpoints on 196,654.** Human Lead ruling, 2026-08-14 (`decisions/0049`). **No such bound existed before ALT-BROAD.**
      **Why all 703 and not the 99.** The 99 are the pairs whose *exit* rests on a null — but **the 604 rest on an untrusted `|A| = 0`, and some of them may in truth have started and left.** A ceiling built on the 99 alone omits that case and **is not a ceiling on the unconditional estimand.**
      **Report the 99-only interval, [9.6830%, 9.7333%], width 0.0503 pp, as a LABELLED CONDITIONAL SUB-INTERVAL** — conditional on every never-started exclusion being truly never-started — **and never as the bound.** The two differ by a factor of seven.
      **Both arms reached this independently and both refused to adopt it themselves.** Instance A: the narrow reading *"would have made this the fourth consecutive bound failing that exact test."*
- [ ] **STATE THAT THE TWO CEILINGS CANNOT BOTH HOLD.** Human Lead ruling, 2026-08-14 (`decisions/0050`). **THERE ARE THREE CEILINGS, NOT TWO, AND NONE OF THEM CAN HOLD WITH THE OTHERS.** Never-started **16.9704%** (33,373), started-and-left **10.0405%** (19,745), **Continued 73.6537%** (144,140 + all excluded) — **sum 100.6646% on 196,654.**
      **Continued HAS a ceiling** — `(144,140 + excluded) / 196,654` — **because any EXCLUDED pair may in truth be Continued.** The parenthetical "no Continued pair is ever excluded" is true and **does not license treating Continued as a point.**
      **The excess is the excluded set counted once in every ceiling.** State the mechanism, not just the total.
      *(`0051` §2 called 73.6537% "on no population" and replaced it with Continued's point 73.2962%. **That was wrong** — 73.6537% is the Continued ceiling, both arms publish it, and `0052` §2 restores it. A Step 9 instance reading the corrected line would have deleted a number its own deliverable prints.)* **They are alternative worst cases over the same 604 pairs, not simultaneous ones**, and printing two upper ends unlabelled is the misreading the whole bound exercise exists to prevent. Instance B: *"both consume the same 604 pairs — and the write-up must say so rather than printing two ceilings that add up to more than the population."*
- [ ] **The never-started bound is DEGENERATE on DERIV — [6.2055%, 6.2055%] — so the dual control is `x = x` there.** Say so where it is published (instance B). The informative comparison is on APPLY.
- [ ] Compute the legacy form alongside it **only if it is labelled as not a bound**, per the reasoning above. Liveness is a pair-level filter (Step 7), so the excluded set is a set of user-show pairs, not of users.
- [ ] Report as a floor and a ceiling, not a single contestable number
- [ ] Report the full headline a second time at a 91-day window, which is Netflix's own reporting window, so the result is commensurable with the public argument. Anchor this arm on the later of the S2 premiere date and the first-pass S1 completion date, not on the finale, because Netflix's window runs from release. State plainly that this arm sits on a different origin than the primary headline and that the two are therefore not the same measurement at two window lengths.

**Deliver:** headline percentages with intervals and bounds, at both W and 91 days, in `artifacts/`
**Check:** dual implementation diff
**Review:** Red Team on claim warrant

---

## Step 10: Where they leave

**Owner:** Data Scientist
**Mode:** Chained

- [ ] Plot the distribution of abandonment points across the season for the started-and-left group
- [ ] Separate first-episode drops, mid-season drops, and near-finale drops
- [ ] Do not claim a specific episode. Progress is self-reported and approximate.
- [ ] **`p` is read on `A_H`, in the rank form.** Human Lead decision, 2026-08-12 (`decisions/0034`). Started-and-left is now assigned at `τ2`, so `p` is read on `A_H`. Let **`m_H = max(A_H)`**; then **`p = |{ e ∈ E2 : e ≤ m_H }| / L2`**. **`p = m_H / L2` is NOT the rule** — that raw-ratio form was withdrawn at the Step 1 gate because `L2` is a *count* of listed episodes and `m_H` an episode *number*, so where S2 numbering has a gap the ratio can exceed 1. It must not be reinstated.
- [ ] **Name the direction the amendment moves this chart.** The 2,246 pairs it moves out of Started-and-left are **the ones that got furthest**, so removing them shifts the abandonment distribution **earlier**. **The amendment makes abandonment look earlier on a published chart**, and Step 10 must say so rather than let a reader attribute the shift to behaviour. (`decisions/0034`)
- [ ] **Re-report the `p = 1.0` residual; do not carry it over.** §7 requires it as its own named category, and its size changes under `A_H` — the pairs that reach the finale but miss the 90 percent threshold are a different set at `τ2` than at `τ1`. (`decisions/0034`)
- [ ] **Do not read a `p` histogram across shows with very different `L2` as if the bins were comparable.** `p` is a fraction of a season, not a count of episodes; at `L2 = 2` it takes one of two values. (Step 1 §7)

**Deliver:** abandonment distribution chart in `artifacts/`
**Review:** Red Team on claim warrant. Reviewer: Consumer Insights on the qualitative why.

---

## Step 11: Discovery bias check

**Owner:** Data Scientist
**Mode:** Chained

- [ ] Recompute the headline separately within Channel A and Channel B
- [ ] Report the two results side by side with intervals
- [ ] State plainly whether the two agree, and whether "agree" means genuinely similar or merely not distinguishable at this sample size
- [ ] If they diverge, do not proceed to publication. Report the divergence and investigate.

**Deliver:** side-by-side comparison and one paragraph of interpretation in `artifacts/`
**Review:** Red Team on claim warrant

---

## Step 12: Segment cut

**Owner:** Data Scientist proposes, Human Lead selects
**Mode:** Chained

- [ ] Do not look at any cut before the headline is final
- [ ] List every candidate considered: origin, gap length between seasons, S1 episode count, user tenure
- [ ] Report results for the full candidate list, not only the one that showed a pattern
- [ ] The Human Lead selects one cut to carry into the write-up
- [ ] For the selected cut, report where the pattern holds and where it breaks

**Deliver:** full candidate results, then the selected cut, in `artifacts/`
**Review:** Red Team on claim warrant. Reviewer: Merchandising on which cut they would actually act on.

---

## Step 13: Robustness

**Owner:** Data Scientist
**Mode:** Chained

- [ ] Vary W above and below the derived value of **`W = 108`** (`decisions/0026-step6-window-w-gate.md`; the Step 6 artifacts state 107 and 107.7135 and **neither is the adopted value**). **Cover at least the range Step 6 reports** — the same percentile read on the C1 curve and on the all-shows curve. That gap is the size of the transfer assumption D14 accepted, so it is the range that tests it.
- [ ] **The W arms must also span 46 to 107 days.** Human Lead decision, 2026-08-12 (`decisions/0024-w-is-the-90th-percentile.md`). Those are the two values two isolated instances produced from the undefined "flattens" criterion before it was replaced by a fixed percentile. **The definition is now unambiguous, but the sensitivity of the result to it is not thereby known**, and 46 to 107 is the measured size of that reading. This range composes with the C1-versus-all-shows range above: **cover the union of the two, not whichever is wider.**
- [ ] **The W arms must also extend ABOVE the adopted `W`, with arms at 150 and 213 days.** Human Lead decision, 2026-08-12 (`decisions/0027-step13-w-arms-above-the-adopted-value.md`). **213 is the 90th percentile among C1 pairs with 8 or more years of exposure** — the direction the right-censoring diagnostic runs, and an upper bound rather than a rival estimate, since exposure and cohort are not separable on this data. Every other mandated range tops out at or below the adopted `W = 108`, so without these two arms **the sensitivity would not test the one direction the known bias points.** 150 sits between the adopted value and the bound so the response is not read off two endpoints alone. Direction, stated so the arms are interpretable: a larger `W` admits later starters and moves the never-started share **down**.
- [ ] **Report the retained-row count for every W arm.** The right-censoring rule contains W, so each arm re-censors the population and the arms do NOT share a denominator.
- [ ] **Hold `H` constant across every arm that varies W.** Otherwise **D3′** and D8 are not comparable between arms. (D3 was replaced by D3′ at `decisions/0034`; the requirement is unchanged and now governs D3′.)
- [ ] ~~**Vary the liveness threshold — and REFIT IT PER `W` ARM.**~~ **WITHDRAWN 2026-08-13 (`decisions/0044`), and `0038` §6's refit requirement is withdrawn with it. THERE IS NO THRESHOLD TO VARY OR REFIT** — `0042` deleted it. This item had no referent and a data-scientist instance would have tried to execute it.
- [ ] **REPORT THE LIVENESS EXCLUSION COUNT PER `W` ARM.** Human Lead ruling, 2026-08-13 (`decisions/0044`). **The rule has no parameter of its own, but it is fully determined by `W`:** its exclusion set **is** the open-ended bucket, and that bucket is a pure function of `W` — **On APPLY — the population Step 13 runs on — 833 at `W = 38` to 1,670 at 213, a factor of 2.0** (`0046`). *(The 348 → 949 figures first recorded here were **DERIV** and are superseded for this purpose; they remain correct on DERIV.)* **Report the ALT-BROAD exclusion count per arm on APPLY: 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864 at `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 — a factor of 1.61.** Report the **started-and-left component separately: 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148, a factor of 2.85**, which grows faster than the rule itself. *(ALT's 485 → 716 series is superseded and must not be ordered.)* Report the count at every arm so the coupling is visible. **`W` and liveness are not independent axes and never were** — deleting the threshold made the coupling total rather than removing it.
- [ ] Vary the S1 completion rule at 100 percent and at 90 percent. **That is the threshold, not the date definition — the two arms below are separate and neither is covered by it**
- [ ] **Arm: S1 completion DATE as last-observed rather than first-pass**, per Step 1 §5. Required by Step 1 §9, and it does more than test a choice: **recompute D2 inside this arm.** D2 on the operative first-pass clock cannot see the rewatch artifact the Step 1 §5 addendum documents — a rewatch cannot move a first-pass clock start, so the primary D2 count will read zero for that failure mode, and **a zero there is not evidence it is rare.** This arm is the only place its frequency is measurable
- [ ] **Arm: `action`-type, excluding `checkin`-only and manual-`watch`-only evidence**, per Step 1 §2.3. Requires the `action` column retained at Step 8. Exists because Step 1 made a permissive choice and the permissiveness should be shown not to be load-bearing
- [ ] Report which conclusions survive all variations
- [ ] Report which do not
- [ ] Record the tested ranges. Step 16 needs them.

**Deliver:** sensitivity table and tested ranges in `artifacts/`
**Review:** Red Team on claim warrant

---

## Step 14: Honest limits

**Owner:** Human Lead
**Mode:** Written before Step 15

- [ ] State that Trakt users are self-selected trackers, not a general audience
- [ ] State that logging is voluntary and incomplete
- [ ] State that progress timestamps are approximate
- [ ] State that this is observational and makes no causal claim about why

### The bias ledger — seven directional statements, plus three from the Step 1 §7 amendment

Human Lead decision, 2026-08-12 (`decisions/0028-step14-carries-every-routed-limitation.md`). The
original checklist carried **one** bias mechanism; seven are now known. Each states its mechanism,
its direction on the never-started share, and its source.

> **These must be reported separately and MUST NOT be netted into a single direction.** They arise
> from different mechanisms on different populations. Two of them are not even the same kind of
> quantity — a population change alters what is being estimated, an estimator bias moves the
> estimate on a fixed population — and averaging them would be a category error, not a
> simplification. Nothing here licenses the claim that they offset.

- [ ] **1. Step 3 seeding — DOWN.** The pool was seeded from movie-comment authors, which biases it toward heavy, currently-active trackers, who are likelier to continue to S2. Step 11 as written cannot detect it: both discovery channels select on public-facing activity, so agreement between them is not evidence of unbiasedness. (`decisions/0008`)
- [ ] **2. Liveness exclusion — UP, not DOWN. SIGN CORRECTED 2026-08-13 (`decisions/0043`).** ~~Excluding pairs that fail the liveness test removes accounts that stopped logging, which are disproportionately the ones that would have scored never-started. Compounds with 1 rather than offsetting it.~~ **That was the reasoning, and it is measured false for the approved rule on this study's own data.** Applying liveness moves the never-started share **from 6.2055% to 6.2373% — UP by 0.032 pp.**
      **THE SIGN IS POPULATION-SCOPED AND BOTH DIRECTIONS MUST BE CARRIED. Figures below are ALT-BROAD (`decisions/0050`); every earlier figure in this bullet was PF-LIMIT's or ALT's and is superseded.**
      **APPLY (line 1 less D10, 196,654 — what Step 8 filters): DOWN 0.2474 pp**, 16.9704% → 16.7231%.
      **DERIV (line 4 less D10, 147,370): UP 0.0042 pp**, 6.2055% → 6.2096% — **a pure denominator effect, since 0 of the 99 DERIV exclusions are never-started.**
      **The exclusion set is NOT entirely never-started.** APPLY's 703 = **604 never-started + 99 started-and-left**; DERIV's 99 = **0 + 99**. The claim that it was, that DERIV moved by 0, and the figures **−0.2558** (ALT) and **−0.192 / 0.032** (PF-LIMIT) are all **withdrawn and must not be restated.**
      **Publish the APPLY direction and state the DERIV direction beside it with this mechanism.**
      **Mechanism of the UP direction on DERIV.** The rule excludes on account silence after `τ1`, and **0 of the 99 DERIV exclusions are never-started**, so the never-started numerator is unchanged and only the denominator falls — the share rises. **On APPLY the 604 never-started exclusions dominate and the share falls.**
      **Consequence for Step 9's bounds:** they are computed on 703 pairs of 196,654 on APPLY and 99 of 147,370 on DERIV, so **they are narrow because the filter is small, not because the inference is tight.** *(The earlier text here — PF-LIMIT as "the approved rule", "seven in seven of the 751… six in seven — 652", and "Option C" — is superseded by `0048` and `0049` and must not be restated.)*
- [ ] **3. Tail cap — UP.** The 300-page forecast cap skipped the pool's heaviest trackers, **0.93% of the pool**. Runs opposite to 1 and 2, so it partially offsets; at 0.93% the magnitude is negligible either way, and it is stated because every other exclusion in this study is. (`decisions/0010`)
- [ ] **4. Sweep-completeness tolerance discard — UP.** The 287 discarded users' completers hold S2 evidence at **89.78%** against **88.52%** retained — **+1.27 points, 95% CI [0.87, 1.66], p < 0.001** — so removing them removes S2-watchers preferentially. Pooled effect on the descriptive: **0.13 points**. Compounds with 3. (`decisions/0023`, `artifacts/step5-discard-outcome-neutrality.md`)
- [ ] **5. Step 5 population change — UP, and it is exact.** Excluding 1,542 pairs pushes the share down and excluding 16,665 pushes it up; **net −15,123 pairs, direction up.** This is a change in *what is estimated*, not an error in the estimate. (`decisions/0021`)
- [ ] **6. Step 5 estimator bias on the retained population — DOWN, and it is bounded, not counted.** Contaminated timestamps written *earlier* than truth pull records into the window and hide never-starters as started, so the reported share is a **floor**. **Guaranteed for 8,372 pairs** — air-date-stamped (4,988) and corrupt pre-1990 (3,384), where claimed ≤ true is structural. **Assumed for 42,019 (90.1%)** — the `backfilled` tag means claimed ≪ *insert*, **not** claimed < *true*, and a 2015 watch imported in 2026 and written as 2018 runs *against* the floor. **State the qualifier with the direction; it does not travel without it.** (`decisions/0021`)
- [ ] **7. A larger `W` — DOWN.** A wider window admits later starters. The adopted `W = 108` sits at the low end of the plausible range because right-censoring is one-sided: the C1 p90 rises to **213 days** among pairs with ≥8 years of exposure. **This does not offset 6 even though both point down** — the mechanisms differ, one being a window-width choice and the other a timestamp defect, so they compound. (`decisions/0026`, `decisions/0027`)

**Items 8, 9 and 10 come from the Step 1 §7 amendment (`decisions/0034`). They publish TOGETHER and
none may be netted against another.** Item 8 is a **definitional change**, not an estimator bias:
`0028`'s no-netting rule extends to it unchanged.

- [ ] **8. The Continued boundary at `τ1 + H` — a definitional change; no direction claimed against truth.** Evaluating Continued at `τ2 = ⟦T0⟧ + 199 days` rather than `τ1` reclassifies **2,246** pairs that completed S2 between day 108 and day 199 from **Started and left** to **Continued**. Never-started is untouched, so its share does not move — but the ratio does: never-started : started-and-left goes **0.485 → 0.557**, a **14.8% shift**, and **Started-and-left itself falls 12.9%, from 17,420 to 15,174**. Both are stated: the ratio is what the study reports, the category count is what a chart shows. **Neither figure is an error bar** — the old boundary and the new one are each exact measurements of their own definition. **Continued is a 199-day statement while never-started is a 108-day statement**, and the two must not be described as measured alike. (`decisions/0034`)
- [ ] **9. Late completers beyond `τ2` — DOWN; at least 3,440 pairs.** The amendment reclassifies the late completers it can see and leaves the rest scored as abandoners. Of the **5,686** Started-and-left pairs that eventually complete S2, **2,246 are reclassified and 3,440 are not** — **19.75%** of the old Started-and-left group, **22.67%** of the new one. **These pairs continued and are counted as having left, so started-and-left is overstated and the ratio understated.** **3,440 is a floor** — the estimation sample excludes pairs the Step 5 waterfall drops, and it is not right-censored. Measured by **D3′** as a fixed-horizon rate on a cleared subpopulation, reported per Step 13 arm, with the exposure-weighted count beside it. (`decisions/0034`)
- [ ] **10. The never-started boundary at `τ1` while Continued is decided at `τ2` — UP; at least 1,573 pairs.** A pair that starts S2 after `τ1` and completes by `τ2` satisfies `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)` but has `|A| = 0`, so it is scored **Never started** — a pair that demonstrably continued. **1,575 on the estimation sample, 1,573 after right-censoring**, and that is **a floor for D8's population, not the count on it**. As a share, 18.64% of the 8,449 scored Never started is a **CEILING** — that denominator excludes the 23,735 pairs with no S2 record at all, which belong in D8's. **No corrected never-started count or ratio is given**: both known channels push the same way and neither is measured. **This bias is not created by the amendment** — those pairs are Never started under the pre-amendment rule too; `A_H` only makes them measurable. **It is the counterweight to item 9 and must be published beside it**, but the two counts act on different components of the ratio and **MUST NOT be netted** — item 9 on the denominator, item 10 on the numerator. Measured by **D8(ii)**. (`decisions/0034`)
- [ ] **Step 9's bounds and Step 9's published shares are on DIFFERENT POPULATIONS, and on one of them the point estimate falls outside its own bound.** Human Lead ruling, 2026-08-14 (`decisions/0052`). The bounds are computed on the **position-5** population (196,654 APPLY / 147,370 DERIV); **the published shares are post-liveness** (195,951 / 147,271). **On APPLY containment holds by arithmetic accident.** **On DERIV it fails outright: the published never-started share is 6.2096% and the published bound is [6.2055%, 6.2055%] — the point estimate lies OUTSIDE its own identified set.** Both arms printed these within two pages of each other and neither said they were on different populations. **State which population each bound bounds at the point of publication.** `0047` §3 fixed endpoint-versus-endpoint and left estimand-versus-headline open; this closes it as a stated limitation, not a repair.
- [ ] **The liveness rule's insertion clock carries a calibration residual, discharged at `W = 108` only.** Human Lead ruling, 2026-08-14 (`decisions/0050`), routed here because **recording a limit only in `decisions/` is not recording it.** **22.68%** of dated records (6,271,584 of 27,656,434) claim a `watched_at` **later than their own calibrated insertion instant**, and the rule's first conjunct **is** a comparison between an interpolated instant and `τ1`. **Clamping is inert** — the clamp value 2026-08-10T20:48Z postdates every D10-surviving `τ1`, so **0 of 66,961 APPLY pairs on clamped accounts are excluded.** **The exclusion set is stable at the residual covering ~91% of records** (703 → [701, 703]) **and not stable in the tail** (±125 d → [414, 1284]); under a direction-only correction **700 of 703 survive and none is created.** **The started-and-left component is the fragile one:** median margin **81.3 days** against 202.5 for never-started, spanning **19×** under tail residual against 2.5×, with **525 of 703 on accounts whose last record is a `watch`, where the residual is not directly measurable.** **All stability figures are `W = 108` only; Step 13 runs to `W = 213`, where the exclusion set is 864 and the started-and-left component 148.**
- [ ] **The liveness rule is a biconditional and `0021` licenses only one direction.** `0021` establishes *insertion after `τ1` ⟹ live* — a **sufficient** condition. The rule also asserts the converse: *no insertion after `τ1` ∧ ¬Continued ⟹ not live*. **ALT-BROAD narrows where that assertion is made, from PF-LIMIT's 1,355 pairs to 703. It does not justify it.** Both arms and Red Team left this open across five reviews; it is recorded as a limitation rather than closed. (`decisions/0048` §9, `0050`)
- [ ] **ALT-BROAD leaves 297 pairs in the channel its own warrant describes.** The warrant is that a pair silent after `τ1` can produce no evidence in `[τ1, τ2)` and is scored "left" by construction — **but that holds identically for a pair silent after `τ1 + ε` for any ε < 91 days.** Measured: **297 pairs on APPLY are ¬Continued, live only because they inserted after `τ1`, and had their last insertion inside `(τ1, τ2)`** — **207 never-started and 90 started-and-left**. **The rule closes 703 of 1,000 such pairs, 70.3%, and leaves 29.7% open**, and **the started-and-left bound treats all 90 as observed.** (`decisions/0050`)
- [ ] **The liveness filter moves the result very little, and Step 9's bounds rest on it.** **CORRECTED 2026-08-14 (`decisions/0049`) — this bullet quoted ALT's movements under an ALT-BROAD heading.** Measured under **ALT-BROAD on APPLY**: **−0.2474 / +0.2630 / −0.0156 pp**, from **703 exclusions of 196,654, 216 accounts**; on **DERIV**, **+0.0042 / +0.0554 / −0.0595 pp** from 99 exclusions of 147,370, 73 accounts. **The superseded figures must not be restated:** ALT's −0.2558 / +0.2258 / +0.0300, and PF-LIMIT's 0.032 / 0.023 / 0.009 on 751 of 147,370. **The "0.05 pp" previously written here was the width of a conditional interval, not a share movement.** Step 9's bounds are computed on these sets, so **they are narrow because the filter is small, not because the inference is tight.**
- [ ] ~~**Step 7's liveness threshold is derived on a narrower population than it is applied to.**~~ **MOOT under the adopted rule (`decisions/0046`).** ALT is **definitional, not derived** — nothing is fitted on one population and applied to another, so the 1.4418%-against-1% mismatch cannot arise. **What replaces it as the limitation, corrected 2026-08-14 (`0048`): under ALT-BROAD the exclusion set is 99 on DERIV and 703 on APPLY, so Step 7's dual run exercises the rule on BOTH populations** — the DERIV diff is **99 against 99 on 73 accounts** rather than the `0 = 0` it was under ALT. **What the gate still cannot establish** is that Step 8's position-6 population is the one Step 7 reconstructed: both arms build APPLY from the Step 5 pair table, not through Step 8's positions 1–5.
- [ ] **The anchor choice has no stated ground, and that is on the record.** There is no argument in Step 1 for preferring `τ2 = ⟦T0⟧ + (W + H)` to `first-S2-watch + H`. Four were attempted during review and all four failed. **§2 of the amendment** — not Step 2, which is the frame ledger and has no lag distribution — carries the marginal-lag distribution, and it is the *start-anchored* rule's own distribution, produced by `src/step6_completion_lag.py`. (`artifacts/step1-amendment-continued-boundary.md` §21)

### Non-bias limitations routed here

- [ ] **The 4,988 partly-air-date pairs (2.27%).** A *single* air-date-stamped S2 record has `watched_at ≤ S2 finale ≤ T0 < τ1` by construction, so it forces `|A| ≥ 1` on its own and the pair cannot score never-started whatever the viewer did. Unresolvable without `W`-dependent filtering, which was rejected because it would make the analysis population a function of `W` and **corrupt the dual-implementation control**. Adoption 1's "entirely" boundary has no basis in the mechanism; a proof closed 2,352 of the original 7,340 and the rest stand. (`decisions/0021`)
- [ ] **The flip bound is 0 to 44,458 — 22.0% of the retained population.** The insert-time test rules out only ~5% of candidates, because a backfilled record is by definition written long after the date it claims. **No point estimate exists and none may be inferred.** (`decisions/0021`)
- [ ] **The sweep-completeness rule validates itself against itself.** Leg 1 gates on `page_count`, which is `ceil(item_count / 250)` in all 2,839 ledger rows and therefore derived from the very header leg 2's tolerance exists to absorb. A short final page proves the sweep ended; a full final page proves nothing, and leg 1 cannot tell them apart. A better instrument — the final-page shape test — existed at ~2,800 calls and no re-pull and was **declined on cascade cost, not on merit**. (`decisions/0023`)
- [ ] **The frame skews toward larger titles, and the skew is structural.** The candidate set is shows with **≥50 S1 completers in the pool**, so small and niche titles are absent by construction and no result generalises to them. The frame is also **systematically older than the catalogue** — 66.5% of it has an S2 finale before 2020 — because unaired and recent second seasons are excluded. (`artifacts/step2-frame-ledger-and-distributions.md`, `decisions/0015`, `decisions/0020`)
- [ ] **`W` is ±18 days, not a point estimate.** 25,120 C1 pairs come from only **206 shows**, and the show is the binding cluster: the iid interval is ±8 days, the show-clustered interval is [89, 125]. The 90th percentile itself is **imported from attribution-window practice, not selected by the data** — moving to the 85th percentile buys 61.7 days. (`decisions/0024`, `decisions/0026`)
- [ ] **The size cap is partly a cadence threshold.** Of the 51 shows the 26-episode cap removes, **44 are C4** and none is C1, so C4 fell from 476 to 425 shows. **A C4 result is not a statement about slow-release shows in general** — the longest-running titles were removed from it — and C4 is where abandonment is most likely to be exposure-driven rather than preference-driven. **Air period and cadence are also strongly confounded** and are not independent cuts. (`decisions/0020`, `decisions/0017`)
- [ ] **Platform fragmentation is not a variable in this study.** Per-season network is 0.71% populated, so "seasons split across services" has no representation in the data. No result may control for it, stratify on it, or rule it out. The show-level `network` is a **present-day** value and must not be read as release-time availability. (`decisions/0016`)
- [ ] **The sweep-completeness discard rate is not homogeneous, and this study does not establish what drives it.** Per-bin discards across the ten history-volume strata run **20, 27, 34, 30, 26, 44, 31, 18, 22, 35** over ~284 attempted per bin — a range of **6.3% to 15.5%** against a pooled 10.1%. **Bin 5 at 15.5% is roughly +3 SD** on a binomial at p = 0.101, n = 284. The rate shows **no monotone trend** across bins spanning forecasts of 1 to 292 pages, so **sweep length is not the mechanism** — which was the obvious candidate and is ruled out. What is left is unidentified. This compounds with the discard already being **outcome-non-neutral** (`decisions/0023`: +1.27 points on has-any-S2), because an unexplained selection mechanism cannot be argued to be harmless. Reported as a limitation, **not fixed**. (`decisions/0033`, `artifacts/partner-reviews-steps-2-and-4.md` §2E)
- [ ] **The live-call ledger under-counts real API spend by 246 calls, and the mechanism is unbounded.** `live_calls` is the `requests_sent` delta measured inside `pull_user`, and **a run killed mid-sweep never writes its ledger row while its calls have already been sent.** Actual requests in Step 4: **126,391**; recorded: **126,145**. 81 of the 246 are the interrupted user, confirmed against its cached pages. The three documented guards all protect against an offline replay *zeroing* the ledger; **none addresses under-count-by-interruption**, and it compounds with every kill. **For any statement about API spend, `logs/api_requests.ndjson` is the authoritative count, not `live_calls_recorded`.** 0.2% today. (`decisions/0032`, `artifacts/partner-reviews-steps-2-and-4.md` §2C)
- [ ] **`logs/step4_failures.ndjson` reads 301 failures where there were 287.** It carries **14 duplicate rows** — the 7 `error_short_read` users written twice, once by the live run and once by an offline replay with `live_calls: 0` on every row. `OfflineGuard` protects the canonical ledger and `state.json` from replays, but **the failure log and the API log are pinned to `LOGS_DIR` regardless of `--state-dir`**, so replays pollute them. The truth is **287 terminal discards and zero unrecovered errors** — all 7 short reads were retried to `complete`. **Read failure counts from `processed/step4/pull_ledger.jsonl`, never from the failure log.** (`decisions/0032`, `artifacts/partner-reviews-steps-2-and-4.md` §2D)
- [ ] **The right-censoring margin is 24 days.** The frame caps the S2 finale at 2025-12-31 and right-censoring admits `T0` only up to **2026-01-24** at `W = 108` — 24 days of clearance, where the approved Step 1 text was written assuming ~13 months. **No show is lost**, but `W` is itself ±18 days show-clustered, so the slack is now smaller than the uncertainty in the number that consumes it. (`artifacts/step1-outcome-definition.md` post-approval addendum 2026-08-12, `decisions/0030`)
- [ ] **Censoring is cohort-asymmetric, and it removes the users least like the ones it leaves.** The loss falls entirely on the uncapped `S1_completion_date` term. At the Step 13 arm of `W = 213` the **2023–2025 cohort loses 10.3% of its pairs against 2.7% for pre-2020**. The survivors from recent titles are those who completed S1 early — early adopters, who are the users **likeliest to continue** — so the modern cohort is not merely smaller but differently selected. **The `W = 213` arm added to test the censoring bias is itself the most censored arm.** (`decisions/0027`, `decisions/0030`)
- [ ] **The study rests on a stopped pull.** 2,549 users of 4,050 planned, **62.9%**. The stop is proportional across all ten strata to within 6.1 points, so it is not an arbitrary prefix — but it is still a subsample, and every count in the study recomputes if the pull resumes. (`decisions/0009`, `artifacts/s1-completer-diagnostic.md` §1)

**Deliver:** limits section in `artifacts/`, placed up front in the write-up and not buried
**Review:** Reviewer: Consumer Insights. Verdict on whether the population is defensible.

---

## Step 15: Decision rule

**Owner:** Human Lead
**Mode:** Chained

- [ ] Convert the finding into an action: given this signal, at this threshold, do this
- [ ] State explicitly which titles do not need support. A recommendation that only adds spend is not a strategy.
- [ ] Name the experiment that would validate the rule
- [ ] State what that experiment would cost
- [ ] State what the estimate would have to be wrong about for the experiment to disagree

**Deliver:** one-page decision rule in `artifacts/`
**Review:** Reviewer: Product Management on whether it is worth building. Reviewer: Merchandising on what they would do differently and which titles get deprioritized. Reviewer: Design on whether it is expressible on a surface. Reviewer: Engineering on experiment feasibility and cost.

---

## Step 16: Results visualization

**Owner:** Data Scientist builds, Human Lead specifies
**Mode:** Chained

The Human Lead decides the format at the time of the build. The two options are not equivalent.

- [ ] Option A, static: charts embedded in the write-up. Fast.
- [ ] Option B, interactive: reader moves W and watches the headline move. **There is no liveness threshold** — deleted at `0042`; the liveness rule has no free parameter of its own (`0044`, `0046`). Slower to build. Far stronger, because it shows the judgment calls are honest instead of asking the reader to take them on trust.
- [ ] Whichever is chosen, the headline, the abandonment distribution, and the filter waterfall all need to be visible
- [ ] If interactive, bound the controls to the ranges recorded in Step 13 so no one can drive it somewhere that was never tested

**Deliver:** visualization in `artifacts/`, embedded or linked
**Review:** Reviewer: Design. Verdict on whether it reads without explanation.

---

## Step 17: Write-up and publish

**Owner:** Human Lead
**Mode:** Chained

- [ ] Open on the problem and the split, not on the data or the method
- [ ] Write the method in plain language, detail goes in an appendix
- [ ] Confirm a reader without statistics can follow the argument
- [ ] Publish with a live link
- [ ] Confirm the public repo contains no file from `raw/`, `processed/`, or `logs/`

**Deliver:** published write-up, live link, public repo
**Review:** Reviewer: Design. Verdict on whether it can be explained without statistics.

---

## Step 18: Decision log

**Owner:** Human Lead, assembled continuously by Second Brain
**Mode:** Runs throughout

Each entry records:

- [ ] What was decided
- [ ] What the alternatives were
- [ ] Why this one
- [ ] What it costs
- [ ] Where the Red Team or a partner reviewer disagreed and how it was resolved

**This is the primary artifact.** The analysis shows the work. The log shows the judgment.

---

## Sequencing notes

- Steps 3 and 4 are the long pole and run unattended. Start them first.
- Step 2 runs in parallel with Steps 0, 1, and 3.
- Step 5 blocks Steps 6 and 7. Never derive thresholds on contaminated timestamps.
- Step 13 must record its tested ranges before Step 16 begins.
- Step 14 is drafted before Step 15, so the conclusion is written against known limits.
- The Human Lead starts and stops long-running pulls. Agents do not schedule them.

---

## Gate summary

Five gates. Nothing proceeds without written approval from the Human Lead at each.

- [x] Step 1: outcome definition — **APPROVED by the Human Lead, 2026-08-10.** `H = 91 days` and the D12 cadence thresholds adopted by name; `pull_date` adopted in form with its value deliberately deferred to Step 4's schedule; Red Team's B2 overruled and recorded as accepted risk. See `artifacts/step1-outcome-definition.md`.
- [ ] Step 5: contamination exclusion rule
- [ ] Step 6: window W
- [ ] Step 7: liveness rule
- [ ] Step 8: analysis table

Each is a question that will be asked out loud. If an agent decided it and the Human Lead did not, it cannot be answered.

---

## Dual implementation

Applies to Steps 6, 7, 8, and 9. Two instances in isolated context run the same written spec with no sight of each other. The Human Lead diffs the numbers. Any divergence is either a bug or an ambiguity in the spec, and both need to be known.

The two instances must receive byte-identical instructions. If the task is described twice in different words, a difference in their output proves nothing.
