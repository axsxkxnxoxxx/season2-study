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
- [ ] Define three mutually exclusive outcome states measured at clock start plus W: never started, started and left, continued
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

- [ ] Include shows with two or more seasons where S2 finished airing on or before 31 Dec 2024
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

## Step 7: Derive liveness threshold

**Owner:** Data Scientist, dual implementation
**Mode:** GATE. Requires written approval from the Human Lead.

Two separate things are defined here and they must not be confused. The **threshold** is a gap length derived from the data. The **rule** is how that threshold is applied, and the rule composes with W because it is evaluated after the window closes.

- [ ] **Liveness runs on record INSERTION time, not on the claimed `watched_at`.** Human Lead decision, 2026-08-12, at the Step 5 gate (`decisions/0021-step5-contamination-gate.md`). **Any record inserted after the window closed proves the account was alive, whatever date it claims** — backfilling an old show is still activity. Gaps computed on claimed dates would read a 2026 import of a 2015 season as a 2015 event and score a live account dead. This ruling is what withdrew the proposed Step 5 account-level exclusion layer, whose sole premise was that import noise is not liveness evidence.
- [ ] **The play-`id` insert-time calibration is a required input, and neither instance refits it.** Step 5 established that the Trakt play `id` is a global auto-increment assigned at insert, and fitted an isotonic id → wall-clock curve on `checkin` and `scrobble` records only — imports do not mint those — held out on disjoint accounts at a median error of four minutes. The curve is at `processed/step5/calibration.npz`, produced by `src/step5_calibrate.py`. **Both instances read that stored curve. Neither refits it**, because two independently fitted curves would differ and the diff would then confound a calibration difference with an implementation difference, which is the one thing the dual run exists to rule out.
- [ ] Derive the threshold independently. Do not use W as an input to the derivation.
- [ ] Plot the distribution of gaps between consecutive **insertion** instants per user, per the two items above
- [ ] Set the threshold well beyond the normal gap
- [ ] State where and why
- [ ] Write the resulting rule: a **user-show pair** counts as live if the account shows logged activity after that pair's clock start plus W, with gaps under the threshold. Liveness **evidence** is account-wide — the whole sweep, other shows and movies included, not restricted to the show under study — but the **test** is clock-start-relative and clock start is pair-specific, so **liveness is a pair-level filter**. One account can be live for one show and not for another. Do not drop a user wholesale on a liveness test.

**Deliver:** gap distribution chart, chosen threshold, rule statement, all in `artifacts/`
**Check:** dual implementation diff
**Review:** Red Team
**Approval:** required before Step 8

---

## Step 8: Analysis table

**Owner:** Analytics Engineer, dual implementation
**Mode:** GATE. Requires written approval from the Human Lead.

Step 1 §9 hands this step a set of obligations that used to live only in that document. They are written out here, because this is the file the two isolated instances read.

**Filters and order**

- [ ] Apply frame, contamination exclusions, S1 completion rule, W, liveness rule, **right-censoring**, and the **`L2 = 1` exclusion** in a fixed documented order
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
- [ ] **Resumption-rate report (D3)**, measured over the fixed horizon `H`
- [ ] **Never-started post-window diagnostic (D8)**, measured over `H`, not to the pull date
- [ ] **Split-artifact counts (D9)**, both halves: the fabricated never-started row and the silently deleted S1-failing counterpart
- [ ] **Right-censoring removal as TWO lines** — the `max(W, 91)` term and the incremental `+ H` term — each with its upward direction on the headline named
- [ ] **`pull_date`, the earliest and latest per-user fetch dates, and the count of records discarded for `watched_at >= pull_date`**
- [ ] **Per-bucket show and pair counts for all five D12 cadence buckets**, plus the count of shows within 1 day of a bucket boundary
- [ ] **Metadata-disagreement counts**, including the subset where `aired_episodes < |E|` for S2. Listed exceeding aired tightens the 90 percent threshold and pushes real completers out — name that direction
- [ ] Assert invariant: outcome states are mutually exclusive and sum to the sample
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
- [ ] Compute the bound: what the never-started share becomes if every inactivity-excluded **pair** is treated as a decliner. Liveness is a pair-level filter (Step 7), so the excluded set is a set of user-show pairs, not of users.
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

- [ ] Vary W above and below the derived value. **Cover at least the range Step 6 reports** — the same percentile read on the C1 curve and on the all-shows curve. That gap is the size of the transfer assumption D14 accepted, so it is the range that tests it.
- [ ] **The W arms must also span 46 to 107 days.** Human Lead decision, 2026-08-12 (`decisions/0024-w-is-the-90th-percentile.md`). Those are the two values two isolated instances produced from the undefined "flattens" criterion before it was replaced by a fixed percentile. **The definition is now unambiguous, but the sensitivity of the result to it is not thereby known**, and 46 to 107 is the measured size of that reading. This range composes with the C1-versus-all-shows range above: **cover the union of the two, not whichever is wider.**
- [ ] **The W arms must also extend ABOVE the adopted `W`, with arms at 150 and 213 days.** Human Lead decision, 2026-08-12 (`decisions/0027-step13-w-arms-above-the-adopted-value.md`). **213 is the 90th percentile among C1 pairs with 8 or more years of exposure** — the direction the right-censoring diagnostic runs, and an upper bound rather than a rival estimate, since exposure and cohort are not separable on this data. Every other mandated range tops out at or below the adopted `W = 108`, so without these two arms **the sensitivity would not test the one direction the known bias points.** 150 sits between the adopted value and the bound so the response is not read off two endpoints alone. Direction, stated so the arms are interpretable: a larger `W` admits later starters and moves the never-started share **down**.
- [ ] **Report the retained-row count for every W arm.** The right-censoring rule contains W, so each arm re-censors the population and the arms do NOT share a denominator.
- [ ] **Hold `H` constant across every arm that varies W.** Otherwise D3 and D8 are not comparable between arms
- [ ] Vary the liveness threshold
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

### The bias ledger — seven directional statements

Human Lead decision, 2026-08-12 (`decisions/0028-step14-carries-every-routed-limitation.md`). The
original checklist carried **one** bias mechanism; seven are now known. Each states its mechanism,
its direction on the never-started share, and its source.

> **These must be reported separately and MUST NOT be netted into a single direction.** They arise
> from different mechanisms on different populations. Two of them are not even the same kind of
> quantity — a population change alters what is being estimated, an estimator bias moves the
> estimate on a fixed population — and averaging them would be a category error, not a
> simplification. Nothing here licenses the claim that they offset.

- [ ] **1. Step 3 seeding — DOWN.** The pool was seeded from movie-comment authors, which biases it toward heavy, currently-active trackers, who are likelier to continue to S2. Step 11 as written cannot detect it: both discovery channels select on public-facing activity, so agreement between them is not evidence of unbiasedness. (`decisions/0008`)
- [ ] **2. Liveness exclusion — DOWN.** Excluding pairs that fail the liveness test removes accounts that stopped logging, which are disproportionately the ones that would have scored never-started. Compounds with 1 rather than offsetting it. (Step 1 §7, Step 7)
- [ ] **3. Tail cap — UP.** The 300-page forecast cap skipped the pool's heaviest trackers, **0.93% of the pool**. Runs opposite to 1 and 2, so it partially offsets; at 0.93% the magnitude is negligible either way, and it is stated because every other exclusion in this study is. (`decisions/0010`)
- [ ] **4. Sweep-completeness tolerance discard — UP.** The 287 discarded users' completers hold S2 evidence at **89.78%** against **88.52%** retained — **+1.27 points, 95% CI [0.87, 1.66], p < 0.001** — so removing them removes S2-watchers preferentially. Pooled effect on the descriptive: **0.13 points**. Compounds with 3. (`decisions/0023`, `artifacts/step5-discard-outcome-neutrality.md`)
- [ ] **5. Step 5 population change — UP, and it is exact.** Excluding 1,542 pairs pushes the share down and excluding 16,665 pushes it up; **net −15,123 pairs, direction up.** This is a change in *what is estimated*, not an error in the estimate. (`decisions/0021`)
- [ ] **6. Step 5 estimator bias on the retained population — DOWN, and it is bounded, not counted.** Contaminated timestamps written *earlier* than truth pull records into the window and hide never-starters as started, so the reported share is a **floor**. **Guaranteed for 8,372 pairs** — air-date-stamped (4,988) and corrupt pre-1990 (3,384), where claimed ≤ true is structural. **Assumed for 42,019 (90.1%)** — the `backfilled` tag means claimed ≪ *insert*, **not** claimed < *true*, and a 2015 watch imported in 2026 and written as 2018 runs *against* the floor. **State the qualifier with the direction; it does not travel without it.** (`decisions/0021`)
- [ ] **7. A larger `W` — DOWN.** A wider window admits later starters. The adopted `W = 108` sits at the low end of the plausible range because right-censoring is one-sided: the C1 p90 rises to **213 days** among pairs with ≥8 years of exposure. **This does not offset 6 even though both point down** — the mechanisms differ, one being a window-width choice and the other a timestamp defect, so they compound. (`decisions/0026`, `decisions/0027`)

### Non-bias limitations routed here

- [ ] **The 4,988 partly-air-date pairs (2.27%).** A *single* air-date-stamped S2 record has `watched_at ≤ S2 finale ≤ T0 < τ1` by construction, so it forces `|A| ≥ 1` on its own and the pair cannot score never-started whatever the viewer did. Unresolvable without `W`-dependent filtering, which was rejected because it would make the analysis population a function of `W` and **corrupt the dual-implementation control**. Adoption 1's "entirely" boundary has no basis in the mechanism; a proof closed 2,352 of the original 7,340 and the rest stand. (`decisions/0021`)
- [ ] **The flip bound is 0 to 44,458 — 22.0% of the retained population.** The insert-time test rules out only ~5% of candidates, because a backfilled record is by definition written long after the date it claims. **No point estimate exists and none may be inferred.** (`decisions/0021`)
- [ ] **The sweep-completeness rule validates itself against itself.** Leg 1 gates on `page_count`, which is `ceil(item_count / 250)` in all 2,839 ledger rows and therefore derived from the very header leg 2's tolerance exists to absorb. A short final page proves the sweep ended; a full final page proves nothing, and leg 1 cannot tell them apart. A better instrument — the final-page shape test — existed at ~2,800 calls and no re-pull and was **declined on cascade cost, not on merit**. (`decisions/0023`)
- [ ] **The frame skews toward larger titles, and the skew is structural.** The candidate set is shows with **≥50 S1 completers in the pool**, so small and niche titles are absent by construction and no result generalises to them. The frame is also **systematically older than the catalogue** — 66.5% of it has an S2 finale before 2020 — because unaired and recent second seasons are excluded. (`artifacts/step2-frame-ledger-and-distributions.md`, `decisions/0015`, `decisions/0020`)
- [ ] **`W` is ±18 days, not a point estimate.** 25,120 C1 pairs come from only **206 shows**, and the show is the binding cluster: the iid interval is ±8 days, the show-clustered interval is [89, 125]. The 90th percentile itself is **imported from attribution-window practice, not selected by the data** — moving to the 85th percentile buys 61.7 days. (`decisions/0024`, `decisions/0026`)
- [ ] **The size cap is partly a cadence threshold.** Of the 51 shows the 26-episode cap removes, **44 are C4** and none is C1, so C4 fell from 476 to 425 shows. **A C4 result is not a statement about slow-release shows in general** — the longest-running titles were removed from it — and C4 is where abandonment is most likely to be exposure-driven rather than preference-driven. **Air period and cadence are also strongly confounded** and are not independent cuts. (`decisions/0020`, `decisions/0017`)
- [ ] **Platform fragmentation is not a variable in this study.** Per-season network is 0.71% populated, so "seasons split across services" has no representation in the data. No result may control for it, stratify on it, or rule it out. The show-level `network` is a **present-day** value and must not be read as release-time availability. (`decisions/0016`)
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
- [ ] Option B, interactive: reader moves W and the liveness threshold and watches the headline move. Slower to build. Far stronger, because it shows the judgment calls are honest instead of asking the reader to take them on trust.
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
- [ ] Step 7: liveness threshold
- [ ] Step 8: analysis table

Each is a question that will be asked out loud. If an agent decided it and the Human Lead did not, it cannot be answered.

---

## Dual implementation

Applies to Steps 6, 7, 8, and 9. Two instances in isolated context run the same written spec with no sight of each other. The Human Lead diffs the numbers. Any divergence is either a bug or an ambiguity in the spec, and both need to be known.

The two instances must receive byte-identical instructions. If the task is described twice in different words, a difference in their output proves nothing.
