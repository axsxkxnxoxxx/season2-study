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
**Mode:** GATE. **RULE CHANGED 2026-08-13 (`decisions/0046`). Reruns pending; NOT approved.**

> ## THE RULE
>
> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND `|A| = 0`.** Otherwise it is live.
>
> **The second conjunct is the ruling.** Liveness exists to license trusting a **null**, and the null
> is `|A| = 0`. **A pair with `|A| ≥ 1` has its outcome directly observed and there is no null to
> license** — so the rule does not reach it.

**EVERY FIGURE BELOW STATES ITS POPULATION. There are two and they differ by construction:**

- **DERIV** — Step 5 line 4 less D10, **147,370**. **Requires S2 evidence.**
- **APPLY** — line 1 less D10, **196,654**. **This is what Step 8 filters at position 6.**

- [ ] **Exclusions: 0 pairs on DERIV, 604 pairs on APPLY.** The DERIV zero is **forced by construction** — line 4 requires S2 evidence, so no line-4 pair can have `|A| = 0` *and* no S2 record. **The 604 on APPLY are exactly the pairs with no S2 record anywhere.** A Step 7 instance reporting 0 on DERIV and 604 on APPLY is correct and the two are not a divergence.
- [ ] **Liveness runs on record INSERTION time, not claimed `watched_at`** (`decisions/0021`, gate 2 of 5). **Any record inserted after the window closed proves the account was alive, whatever date it claims.**
- [ ] **Read the stored play-`id` isotonic calibration at `processed/step5/calibration.npz`. NEITHER INSTANCE REFITS IT** (`0029`).
- [ ] **Liveness is a PAIR-LEVEL filter, anchored at `τ1`** (`0034`). Evidence is account-wide; the test is clock-start-relative and clock start is pair-specific. **One account can be live for one show and not another. Never drop a user wholesale.**
- [ ] **`τ2` plays no part.**
- [ ] **Do not reintroduce a pre-`τ1` requirement in any form.** Withdrawn twice — `0040` §1 and `0042` §3 — both times for contradicting gate `0021`.
- [ ] **Waterfall line 6 becomes OUTCOME-CONDITIONAL, and the spec says so** (`0046`). `|A| = 0` is evaluated before liveness is applied. **That is permitted and both arms proved it**: `|A|` and liveness are **row-local predicates on the position-5 output and commute exactly**, and `0029`'s ordering rationale is about **per-filter sample size**, which cannot reach position 7 because **outcome assignment removes no rows** — positions 1–6 are filters, position 7 is an annotation. **Report line 6 as outcome-conditional so two instances do not diverge on the waterfall while agreeing on every share.**
- [ ] **The monotone-decrease invariant holds only NON-STRICTLY** where the exclusion set is empty, which it is on DERIV. State it.
- [ ] **`|A| = 0` means Step 1 §7's Never-started condition** — not "no S2 evidence at all." The competing reading gives a different set and the two must not be confused.
- [ ] **Report the exclusion count per `W` arm on APPLY**, so the `W`-coupling is visible (`0044` §1.2, corrected to APPLY by `0046`).

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
- [ ] Assert invariant: filter counts decrease monotonically
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
- [ ] **Compute the bound over the liveness exclusions, which under the adopted rule are ALL never-started by construction.** **On APPLY: [16.7146%, 16.9704%], width 0.2558 pp.** **The ceiling equals the unfiltered share as an identity** — the excluded set is a subset of never-started, so returning every excluded pair as a decliner reproduces the unfiltered population exactly. **Both endpoints are attainable.**
      **What this replaces, and the correction is on the record.** `0045` published **[16.7789%, 17.0355%]** for PF-LIMIT under "Option C" and claimed the same identity. **That interval mixed two denominators** — floor on 195,299, ceiling on 195,903 — and **its floor was not a floor**: if all 604 had actually started, the share is **16.727%**, *below* the published floor and outside the interval, which is the exact case liveness exists to guard against. **The internally consistent PF-LIMIT interval was [16.727%, 17.0355%], width 0.308 pp**, and **the identity claim was false for PF-LIMIT** — it is a property of the adopted rule, not of PF-LIMIT (`0046` §2).
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
- [ ] **REPORT THE LIVENESS EXCLUSION COUNT PER `W` ARM.** Human Lead ruling, 2026-08-13 (`decisions/0044`). **The rule has no parameter of its own, but it is fully determined by `W`:** its exclusion set **is** the open-ended bucket, and that bucket is a pure function of `W` — **On APPLY — the population Step 13 runs on — 833 at `W = 38` to 1,670 at 213, a factor of 2.0** (`0046`). *(The 348 → 949 figures first recorded here were **DERIV** and are superseded for this purpose; they remain correct on DERIV.)* **Under the adopted rule report the ALT exclusion count per arm on APPLY: 485 at `W = 38` to 716 at 213, a factor of 1.5** — coupling mitigated, not removed. Report the count at every arm so the coupling is visible. **`W` and liveness are not independent axes and never were** — deleting the threshold made the coupling total rather than removing it.
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
      **THE SIGN IS POPULATION-SCOPED, AND BOTH DIRECTIONS MUST BE CARRIED (`decisions/0045`).** On the **derivation** population (line 4 less D10, 147,370) it is **UP 0.032 pp** — 6.2055% → 6.2373%. On the **application** population (line 1 less D10, 196,654, **which is what Step 8 filters**) it is **DOWN 0.192 pp** — 16.9704% → 16.7789%. **Line 4 requires S2 evidence**, so the **604** never-started pairs with **no S2 record anywhere** exist only on the application population; excluding them is what pulls the share down there. **Publish the application-population direction, and state the derivation-population direction beside it with this mechanism.** **UNDER THE ADOPTED RULE (`0046`) the sign is unambiguous and DOWN on both populations**: the exclusion set is entirely never-started, so removing it can only lower the share — 0 excluded on DERIV so no movement there, and **DOWN 0.2558 pp on APPLY**. The UP direction was a property of PF-LIMIT deleting 751 confirmed continuers, and PF-LIMIT is superseded.
      **Mechanism of the UP direction on the derivation population.** The rule excludes on account silence after `τ1`, but **a pair scored Continued carries positive episode-level evidence that the account was logging in the window** — `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)` — which later silence cannot corrupt. So the filter **preferentially deletes confirmed continuers.** Measured on the threshold rule's 1,282-pair exclusion set, of which the approved rule's 751 are the open-ended subset: **1,079 Continued, 163 Started-and-left, 40 Never started.** Instance B's own words: *"the filter is not selecting on the outcome it was built to protect."*
      **It therefore does NOT compound with bias 1. It offsets it**, by a trivial amount. Do not restate the old direction anywhere.
      **Consequence for Step 9's bound, which must be stated with it:** the bound treats every excluded pair as a decliner, and **seven in seven of the 751 have positive S2 evidence, and six in seven — 652 — are confirmed continuers.** (Two claims, previously merged into one and understated.) Treating a confirmed continuer as a decliner is not a conservative bound — it is an arithmetic operation on a set chosen for a reason unrelated to the uncertainty being bounded. **Report the bound over the never-started exclusions only** (`0045`, Option C). ~~or compute it on the ~40 never-started exclusions instead~~ — **that remedy is WITHDRAWN and was unexecutable: the approved rule's never-started exclusion count on the derivation population is ZERO**, not ~40. The ~40 was read off the deleted 1,293-day rule. (Step 1 §7, Step 7, `decisions/0043`)
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
- [ ] **The liveness filter as a whole barely moves the result, and Step 9's bound rests on it.** Against **no liveness filter at all**, the approved rule moves the three shares by **0.032 / 0.023 / 0.009 pp** — smaller than the third significant figure of every share, and roughly **2% of the account-clustered sampling width**. **751 pairs of 147,370 are excluded, from 166 accounts of 2,402.** Step 9's liveness bound — what the never-started share becomes if every excluded pair is treated as a decliner — is computed on that set, so **the bound is narrow because the filter is nearly inert, not because the inference is tight.** Report it as such. (`decisions/0042` §4)
- [ ] ~~**Step 7's liveness threshold is derived on a narrower population than it is applied to.**~~ **MOOT under the adopted rule (`decisions/0046`).** ALT is **definitional, not derived** — nothing is fitted on one population and applied to another, so the 1.4418%-against-1% mismatch cannot arise. **What replaces it as the limitation: the rule's exclusion set is 0 on DERIV and 604 on APPLY**, so Step 7's own dual run cannot exercise the rule at all and its diff is `0 = 0` on the derivation population. **The rule is first exercised at Step 8.**
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
