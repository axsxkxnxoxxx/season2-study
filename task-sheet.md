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
- [ ] **On a 403, CLASSIFY IT BEFORE ACTING.** ~~On a 403, hard stop and report. That is a block, not a throttle.~~ ***SUPERSEDED*** — amended by the Human Lead 2026-08-10 and carried in `CLAUDE.md`, which is authoritative on API discipline; the unconditional form would halt an unattended Step 4 pull on a single private profile. **On a USER RESOURCE: skip that user, log it with full headers, continue** — bounded by two circuit breakers, **5** consecutive unconfirmed user-403s with no intervening 2xx, and **200** in a run. **Only a 2xx resets the streak.** **NOT on a user resource** — or on one where `X-Private-User` is present and false-like or unrecognised — **hard stop and report. That is a block, not a throttle.** **Ambiguity resolves strict.** **A skipped user is `access_denied`, NOT a user with no history**, and must stay distinguishable downstream.
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
**Mode:** GATE. **APPROVED by the Human Lead, 2026-08-13 (`decisions/0064`; record at `artifacts/step7-gate-approval.md`). GATE 4 OF 5 IS CLOSED.** The approved rule is **ALT-BROAD**, restored at `0054` after ALT-MATCHED was reverted. **Fifteen Red Team reviews and fifteen HOLDs — but reviews 1–8 contested the RULE and 9–15 found propagation and control defects in figures derived from an unchanged rule**, none of which altered the rule, the population, the exclusion counts or any bound endpoint. **The approval is UNCONDITIONAL and the residual is published, not resolved** — nine items, `artifacts/step7-gate-approval.md` §4. Both arms have run on ALT-BROAD and on ALT-MATCHED; all figures for both are on record.

> ## THE RULE
>
> **A user-show pair is NOT LIVE if and only if BOTH: the account shows no insertion instant after
> that pair's `τ1 = ⟦T0⟧ + W × 24h`, AND the pair is NOT Continued.** Otherwise it is live.
>
> **The silence test is anchored at `τ1` and only at `τ1`** — ruled by `0034` in the entry that created
> the second window, re-affirmed by `0051`, and **restored by `0054` after ALT-MATCHED was reverted.**
>
> **AND ITS EVIDENCE IS RESTRICTED TO RECORDS DATED BEFORE `τ_pull`.** Human Lead ruling 2, 2026-08-13
> (`0070`, propagated here by `0072`). **This applies an existing ruling consistently; it is not a new
> one.** **D11, approved at the Step 1 gate, makes `τ_pull` a GLOBAL FROZEN CUTOFF and discards records
> at or after it from EVERY computation** — and the silence test is a computation. **The unstated
> version produced the reported-not-reconciled 792 (A) against 791 (B) at Step 7**, where one arm
> applied the restriction and the other did not. **Measured before the ruling, because this is an
> approved gate: exclusions are 703 on APPLY and 99 on DERIV either way**, since no insertion instant
> exceeds the clamp at 2026-08-10T20:48Z and D10 already forces `τ1 ≤ τ_pull − 91 d`. **The restriction
> is inert on the exclusion set and bites on the robustness tail.** **STEP 13 READS THIS BLOCK and
> re-runs the rule across eight `W` arms; the scope holds at every one.**
>
> **And "after `τ1`" is STRICT** (`0068`): a pair is silent iff it has **no insertion instant `> τ1`**,
> so an instant falling exactly **at** `τ1` does **not** make the account live.
> **ALT-MATCHED — silence at `τ2` for the started-and-left branch — is WITHDRAWN**: it produced
> **numerically identical bounds** on all three identified sets and cost an amendment to an approved
> gate. (`decisions/0054`)
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

- [ ] **Exclusions at `W = 108`: APPLY 703 from 216 accounts (604 never-started + 99 started-and-left); DERIV 99 from 73 accounts (0 + 99).** Superseded: ALT-MATCHED 793/189 APPLY and 188 DERIV, **ALT 604/0**. ***The sentence that stood here — "a Step 7 instance reporting 0 on DERIV and 604 on APPLY is correct and the two are not a divergence" — was written for ALT and is WITHDRAWN (`0067`, found by instance B). It is FALSE under the approved rule*** — it blessed the superseded rule's answer inside the bullet withdrawing that rule, in the file the isolated instances read. **Under ALT-BROAD the answer is 703 on APPLY and 99 on DERIV. An instance reporting 604/0 has implemented ALT, and that IS a divergence.**
            **How the rule selects:** conjunct 2 (NOT Continued) narrows APPLY **196,654 → 52,514**; conjunct 1 (no insertion after `τ1`) narrows **52,514 → 703**. **Conjunct 1 does most of the work**, which is why the count moves with `W`.
      **The DERIV zero is NOT forced by construction.** `has_s2` does **not** imply `|A| ≥ 1` — `|A|` needs an **in-`E2`** record — and **9,145 DERIV pairs are never-started**. Four line-4 pairs hold S2 records with no `E2` episode number, satisfy **both** conjuncts at every arm, and are removed one position earlier by **D10**. **The zero comes from the filter order and this pull date.**
- [ ] **Liveness runs on record INSERTION time, not claimed `watched_at`** (`decisions/0021`, gate 2 of 5). **Any record inserted after the window closed proves the account was alive, whatever date it claims.**
- [ ] **Read the stored play-`id` isotonic calibration at `processed/step5/calibration.npz`. NEITHER INSTANCE REFITS IT** (`0029`).
- [ ] **Liveness is a PAIR-LEVEL filter, anchored at `τ1`** (`0034`). Evidence is account-wide; the test is clock-start-relative and clock start is pair-specific. **One account can be live for one show and not another. Never drop a user wholesale.**
- [ ] **`τ2` DOES play a part, and the earlier "`τ2` plays no part" is WITHDRAWN (`decisions/0049`).** Under ALT-BROAD the **second conjunct IS the Continued test, which is read at `τ2 = ⟦T0⟧ + (W + H) × 24h` on `A_H`.** **The rule reads two instants: SILENCE at `τ1`, CONTINUED at `τ2`.** **The silence test is anchored at `τ1` and only at `τ1`** (`0034`, `0051`, `0054`). *(ALT-MATCHED's per-branch anchoring — `τ2` for the started-and-left null — and its instruction that "anchored at `τ1` and only at `τ1`" was withdrawn are themselves **WITHDRAWN by `0054`**. An instance producing **703** is correct; **793 is ALT-MATCHED's and is a divergence.**)*
- [ ] **Do not reintroduce a pre-`τ1` requirement in any form.** Withdrawn twice — `0040` §1 and `0042` §3 — both times for contradicting gate `0021`.
- [ ] **Waterfall line 6 becomes OUTCOME-CONDITIONAL, and the spec says so** (`0046`). `|A| = 0` is evaluated before liveness is applied. **That is permitted and both arms proved it**: `|A|` and liveness are **row-local predicates on the position-5 output and commute exactly**, and `0029`'s ordering rationale is about **per-filter sample size**, which cannot reach position 7 because **outcome assignment removes no rows** — positions 1–6 are filters, position 7 is an annotation. **Report line 6 as outcome-conditional so two instances do not diverge on the waterfall while agreeing on every share.**
- [ ] **Monotone decrease is STRICT on BOTH populations under ALT-BROAD** — 703 on APPLY and 99 on DERIV, at every arm; the empty-set case does not arise (`0049`). **The `>=` coding at Step 8 is KEPT** — see there for why the reason changed but the coding did not.
- [ ] **"NOT Continued" means Step 1 §7 as amended by `0034`** — the negation of `|A| ≥ 1` ∧ `F2 ∈ A_H` ∧ `|A_H| ≥ ceil(0.90 × L2)`, so it covers **both** Never started and Started-and-left. **`|A| = 0` alone is the superseded ALT form and is not the rule.** And `|A| = 0` is Step 1 §7's Never-started condition, **not** "no S2 evidence at all" — the competing reading gives a different set.
- [ ] **Report the exclusion count per `W` arm on APPLY**, so the `W`-coupling is visible (`0044` §1.2, corrected to APPLY by `0046`). **ALT-BROAD on APPLY — this is the adopted rule's series: 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864** at `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213, **a 1.61× coupling.** **The started-and-left component alone runs 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148 — a factor of 2.85, growing faster than the rule's own coupling. Report it separately.** *(Superseded and not to be restated: **ALT-MATCHED's 604 / 621 / 713 / 754 / 793 / 793 / 878 / 952** with S&L 119 / 127 / 159 / 179 / 190 / 189 / 214 / 236 (`0053`, withdrawn); **ALT's 485 → 716** and its **1.5×** figure, which `0052` §8 struck and which survived here in the same line as the series it struck. Corrected by `0054`+ / propagation #15.)*
- [ ] **D10 IS RE-DERIVED AT EACH ARM. Name the reading; do not freeze it.** Human Lead ruling, 2026-08-13 (`decisions/0047`). Right-censoring is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, which **contains `W`**, so the censored population differs per arm. **Freezing D10 at `W = 108` gives, at `W` = 125 / 150 / 180 / 213: TOTALS **746 / 823 / 918 / 1,117**, of which the never-started COMPONENT is 632 / 684 / 753 / 881** (`decisions/0050`). **The 632/684/753/881 figures were re-blessed at `0048` §7 as though they were totals; under ALT-BROAD they are a component**, and a Step 13 instance producing the frozen reading gets 823 / 1,117 and would file a false divergence against 684 / 881. **125 and 180 are not in the mandated grid**, so only the `W` = 150 and 213 entries are comparable to it — a different table. **An arm table that does not name the reading is not reproducible**, which instance A demonstrated by producing both.

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
**Mode:** GATE. Requires written approval from the Human Lead. ***APPROVED by the Human Lead, 2026-08-17, UNCONDITIONALLY — gate 5 of 5, and ALL FIVE GATES ARE NOW APPROVED*** (`0098`, record at `artifacts/step8-gate-approval.md`). **Red Team returned PROCEED on its ELEVENTH pass.** **The eight residuals in §4 of the record are OPEN AND PUBLISHED and approval is unconditional with them so; the `logs/` provenance cost is ACCEPTED AS RECORDED, not a correction anyone will close; the five §5 limitations travel to Step 14.** **Step 8b and Step 9 are UNBLOCKED and NOT LAUNCHED** — a chained step returns to the Human Lead before the next one starts.

Step 1 §9 hands this step a set of obligations that used to live only in that document. They are written out here, because this is the file the two isolated instances read.

**Filters and order**

- [ ] **Apply the filters in EXACTLY this order.** Human Lead decision, 2026-08-12 (`decisions/0029-step7-threshold-rule-and-w-propagation.md`). The final row set commutes, but **the required per-filter sample size does not** — two faithful instances applying the same filters in different orders would report different waterfalls on an identical table, and the diff could not tell that from a bug.
      **1.** Step 2 frame → **2.** `L2 = 1` exclusion → **3.** S1 completion rule → **4.** contamination exclusion (Step 5) → **5.** right-censoring → **6.** liveness rule → **7.** outcome assignment, **at two instants** — `|A| = 0` tested at `τ1`, the Continued condition tested at `τ2` (`decisions/0034`).
      Rationale for the two that could defensibly swap: **contamination before right-censoring** is already required below. **Right-censoring before liveness** because censoring is a property of the clock and `pull_date` — objective, and independent of behaviour — while liveness is a behavioural inference; running the objective filter first means liveness's marginal cost is measured on a fully observable population, which is the number Step 9's bound needs.
- [ ] **WATERFALL LINE 1 IS THE S1-COMPLETER POPULATION: 220,107 PAIRS.** Human Lead ruling,
      2026-08-13 (`decisions/0068`), because the spec named no base and **four defensible readings sit
      on disk** — 2,900,762 (the frame cross-product), 278,452 (any S1-or-S2 record on a frame show),
      274,741 (any S1 record), and 220,107 (`pool_completers`). **Lines 1, 2 and 3 all moved with the
      choice, and two faithful instances would have reported different waterfalls on an identical
      table** — the exact failure the fixed filter order above exists to prevent, one position upstream
      of where that fix reached. **Take 220,107. It is the population this study is defined over:
      user-show pairs whose user completed season 1.** **Lines 2 and 3 follow from it** — line 2 is line
      1 less the `L2 = 1` shows, line 3 is line 2 less the pairs failing the S1 completion rule — and
      **no instance chooses a base.** *(Open and NOT resolved by this ruling: instance A measured that
      applying D11 at position 3 as Step 1 requires gives **220,103**, because 167 in-frame records
      carry `watched_at ≥ τ_pull` and `src/step2_build_frame.py` never touches the timestamp column.
      **The base is 220,107 as published; whether D11 moves it is a separate open question** and is
      listed as such.)*
- [ ] **`W = 108 days`**, approved 2026-08-12 (`decisions/0026-step6-window-w-gate.md`). Never-started uses `τ1 = ⟦T0⟧ + 108 × 24h`; **Continued uses `τ2 = ⟦T0⟧ + (108 + 91) × 24h = ⟦T0⟧ + 199 days` (`decisions/0034`)**, with `A_H` the set `A` recomputed at that bound. **`|A| ≥ 1` at `τ1` remains a conjunct of Continued** — dropping it puts a day-150 starter completing by day 190 in two states at once. **The Step 6 deliverables state 107 (`-a`) and 107.7135 (`-b`); neither is the adopted value** — both predate the ceiling ruling in `decisions/0025`. Take the number from the decision entry, not from the artifacts.
- [ ] **Contamination exclusion runs BEFORE right-censoring**, so an import-stamped S1 completion date is counted as contamination rather than laundered into a censoring drop
- [ ] **Exclude `L2 = 1` shows from the headline population** and count them in the waterfall. At `L2 = 1`, Continued is equivalent to Started, Started-and-left is empty by construction, and `p` is never defined
- [ ] **Enforce the set-membership drop rule**: an episode whose `number` is not in the season's listed set `E` is dropped. This is an implementation check, not a data check — under set membership `|D| ≤ L` holds by construction
- [ ] **Every boundary test is the half-open UTC-instant form** of Step 1 §2.4. `date(watched_at) <= T1` must not appear anywhere in the implementation
- [ ] **THE LIVENESS SILENCE TEST IS STRICT.** The rule is *"no insertion instant **after** `τ1`"*, so a pair is silent iff it has **no insertion instant `> τ1`** — an instant falling exactly **at** `τ1` is **not** after it and does **not** make the account live. **Stated here, in the step that applies the rule** (`0068`); it was determinable from the rule text and said nowhere in Step 8. **AND THE EVIDENCE IS RESTRICTED TO RECORDS DATED BEFORE `τ_pull`.** Human Lead ruling, 2026-08-13 (`0070`). **This is applying an existing ruling consistently, not a new one:** **D11, approved at the Step 1 gate, makes `τ_pull` a global frozen cutoff and discards records at or after it from EVERY computation** — and the silence test is a computation. **The unstated version produced the reported-not-reconciled 792 (A) against 791 (B) at Step 7**, where one arm applied the restriction and the other did not. **Measured before ruling, and it does not disturb the approved gate: exclusions are 703 on APPLY and 99 on DERIV either way**, because no insertion instant exceeds the clamp at 2026-08-10T20:48Z and D10 already forces `τ1 ≤ τ_pull − 91 d`.
- [ ] **THE COLUMN SET IS ENUMERATED, NOT COUNTED — 89 NAMES, EXACTLY THESE.** Human Lead ruling
      (`0080`, extended to 88 by `0081` and to 89 by `0082`), replacing `0077` §3's count. **Converged
      is not specified**, and **Step 8b's schema is built on this vocabulary**, so it is fixed before the
      schema exists. Emit exactly these, no more and no fewer:
      `abandonment_point_p`, `action_count_s1_checkin`, `action_count_s1_other`, `action_count_s1_scrobble`
      `action_count_s1_watch`, `action_count_s2_checkin`, `action_count_s2_other`, `action_count_s2_scrobble`
      `action_count_s2_watch`, `air_period`, `cadence_boundary_distance_days`, `cadence_bucket`
      `completers_per_year`, `discovered_channel_a`, `discovered_channel_b`, `e1_internal_gap`
      `e1_starts_at_1`, `e2_internal_gap`, `e2_starts_at_1`, `exclusion`
      `gap_days`, `has_s3_or_later_evidence`, `in_apply`, `in_deriv`
      `live`, `max_episode_in_A_H`, `max_season_number`, `n_A`
      `n_A_H`, `outcome`, `p_at_bound`, `pool_completers`
      `pool_completers_proxy`, `s1_E`, `s1_F`, `s1_L`
      `s1_aired_episodes_reported`, `s1_aired_lt_listed`, `s1_completion_date`, `s1_completion_used_a_post_cutoff_record`
      `s1_count_disagreement`, `s1_episode_count_reported`, `s1_exposure_years`, `s1_finale_date`
      `s1_premiere_date`, `s1_season_first_aired`, `s1_total_runtime`, `s2_E`
      `s2_F`, `s2_L`, `s2_aired_episodes_reported`, `s2_aired_lt_listed`
      `s2_count_disagreement`, `s2_episode_count_reported`, `s2_finale_date`, `s2_finale_year`
      `s2_premiere_date`, `s2_season_first_aired`, `s2_span_days`, `s2_total_runtime`
      `s2_weekly_span_days`, `season_numbers`, `seasons_returned`, `show_aired_episodes`
      `show_airs_day`, `show_certification`, `show_comment_count`, `show_country`
      `show_first_aired`, `show_genres`, `show_language`, `show_languages`
      `show_rating`, `show_runtime`, `show_status`, `show_subgenres`
      `show_trakt_id`, `show_votes`, `show_year`, `silent_at_tau1`
      `size_quintile`, `size_quintile_per_year`, `size_quintile_raw_count`, `t0_binding_term`
      `t0_date`, `tau1`, `tau2`, `title`
      `user_idx`
      **`p_at_bound` is NEW** (`0082`). **`silent_at_tau1` is IN** (`0081`) — the only way to recompute
      the **Continued-and-silent count, 652**, from this table, since the rule's second conjunct is
      `NOT Continued` so **`live` is true for every Continued pair regardless of silence**; that count
      closed the rule objection at `0063` §1 and is a published Step 14 limitation, and **its input
      living in Step 7's working files is the same shape as `0079`'s drop set.**
      **BOTH ARMS PUBLISH THE LINE-6 MARGINAL DECOMPOSITION — 652 AND 1,355, NOT ONE OF THEM.**
      Red Team third pass (`0085` §5). **703 is NOT the marginal cost of the silence test**: the
      silence test alone excludes **1,355** on APPLY, and the `NOT Continued` conjunct **spares 652**,
      giving `1,355 − 652 = 703`. ***One arm published 652 and not 1,355.*** **Derivable, so not a
      defect — but 1,355 is the figure that makes line 6 readable as a marginal cost**, and a reader
      with only 652 cannot recover it without knowing to add. **Publish both, on APPLY and DERIV, with
      the identity stated.**
      **Two columns stay DROPPED and both are free:** **`f2_in_A_H`**, derivable as
      `max_episode_in_A_H == s2_F`, and **`max_episode_in_A`**, read by nothing downstream.
      ***The count moved 88 → 89 as a mechanical consequence of adding `p_at_bound`; it is stated here
      rather than left to be recounted.***
- [ ] **COLUMN NAMES ARE FIXED, NOT LEFT TO THE INSTANCE.** Human Lead ruling, 2026-08-13 (`0077`).
      The rerun produced **88 columns against 87 for the SAME CONTENTS** — `in_population_APPLY` against
      `in_apply`, `n_rec_s1_watch` against `action_count_s1_watch`, `tau1_utc` against `tau1`,
      `max_episode_in_AH` against `max_episode_in_A_H`. **Step 8b defines the schema Steps 9–13 write
      into, so it would inherit the divergence.** **THE RULE: use the spec's own vocabulary at the point
      the spec defines the thing; where the spec does not name it, prefer the more explicit form.**
      Adopted:
      **`in_apply` / `in_deriv`** — the spec names the populations APPLY and DERIV and these are the
      shortest unambiguous forms. **`tau1` / `tau2`** — the spec writes `τ1` and `τ2` with no suffix.
      **`n_A` / `n_A_H` / `max_episode_in_A_H` / ~~`f2_in_A_H`~~** — the spec writes `A`, `A_H`, `|A|` and
      `F2 ∈ A_H`; **`AH` is not the spec's spelling.** ***`f2_in_A_H` IS NOT AN EMITTED COLUMN
      (`0080` §2, restated `0083` §3b): it is DROPPED as derivable — `max_episode_in_A_H == s2_F`.
      `0077`'s ruling here was about SPELLING and still governs `n_A`, `n_A_H` and `max_episode_in_A_H`;
      the COLUMN does not survive it. Marked rather than deleted, so the spelling ruling is not lost
      with it.*** **`action_count_s{1,2}_{watch,scrobble,checkin,other}`**
      — `0070` ruling 4 says *"per-pair COUNTS BY ACTION TYPE"*, and these are those words.
      **`discovered_channel_a` / `discovered_channel_b`** — `0070` ruling 3 says two booleans;
      `in_channel_*` is ambiguous with the population flags. **`t0_binding_term` / `t0_date` /
      `s1_completion_date`** — lower-case `t0`, no `_utc` suffix, since **every instant in this study is
      UTC by Step 1 §2.4 and a suffix on some columns implies the others are not.**
      **Keep both instances' extra columns**: **`has_s3_or_later_evidence`** (D4 reads it) and
      **`s1_completion_used_a_post_cutoff_record`** (the D11 question at position 3 reads it).
      ~~**The table is 89 columns.**~~ ***SUPERSEDED — the count is replaced by the 89-NAME ENUMERATION
      above (`0080`, taken to 88 by `0081` and to 89 by `0082`). BOTH Step 8 instances reported this
      sentence still reading as current one bullet below its replacement*** — the shape `0067` fixed at
      line 258 and `0076` fixed in the `p` heading. ***And this NOTE itself then carried the superseded
      88 for its own replacement — corrected at `0083` §3a, reported by instance A, fourth occurrence of
      the shape and the fourth found by an agent rather than by a control.*** **The enumeration's 89 is
      NOT `0077`'s 89**: `f2_in_A_H` out, `silent_at_tau1` and `p_at_bound` in. **Matching a count is not
      matching a set — assert on the names.** **`f2_in_A_H`, named in the adopted list above, is DROPPED
      as derivable** (`max_episode_in_A_H == s2_F`).
- [ ] **THE TABLE IS THE POSITION-5 ROW SET: 196,654 rows on APPLY, with `live` and `outcome` AS
      COLUMNS.** Human Lead ruling, 2026-08-13 (`0074`). **Both readings of "one row per pair" give
      identical counts** — the dual run produced 195,951 × 86 at position 7 and 196,654 × 87 at position
      5 — **so this is a ruling, not a correction.** **Rulings 1 and 7 established that downstream
      CONSUMES rather than REBUILDS, and carrying the liveness result as a column is that principle
      applied to the row set.** **Under the position-7 reading anything needing the excluded pairs
      reconstructs them, and a reconstruction that agrees today is still a second definition tomorrow**
      — invisible to the dual diff, because both instances would rebuild the same way.
- [ ] Build one row per user-show pair
- [ ] Include per row: outcome state, abandonment point, discovery channel, and all Step 2 show fields.
- [ ] **DISCOVERY CHANNEL IS TWO BOOLEAN COLUMNS, NOT ONE CATEGORICAL.** Human Lead ruling, 2026-08-13
      (`0070`). **324 of the 5,694-username Step 3 DISCOVERY POOL are in BOTH channels; on the 2,549 accounts
      actually pulled the overlap is 178 — both measured on the position-5 build of 2026-08-13 and
      reproduced by both arms** (`0078`). *(A third reading is stated in no ruling: **174 of the 2,422
      accounts in the APPLY position-5 population**, instance B. **Publish the first two; the third is
      recorded so it is not later read as a divergence.**)*
      **PUBLISH THE OVERLAP IN BOTH UNITS, EACH WITH ITS CONSUMER NAMED.** Human Lead ruling,
      2026-08-13 (`0079`). **Picking one leaves the other consumer holding a wrong-unit figure.**
      **324 of 5,694 DISCOVERY-POOL USERNAMES** — consumer: the **Step 3 seeding-bias statement** and
      **Step 14 ledger item 1**, which are about the pool's composition. **178 of 2,549 ACCOUNTS
      PULLED** — consumer: **Step 4 coverage reporting**. **174 of 2,422 ACCOUNTS and 17,783 of 196,654
      PAIRS in the position-5 population** — consumer: **Step 11**, which recomputes the headline within
      each channel and therefore cuts **the analysis population, not the pool**. ***Correction to the
      ruling as dictated: it assigned Step 11 to users and the pool statistic to accounts. The files
      show the reverse*** — Step 11 recomputes the headline, which is over pairs on the position-5 row
      set, while the pool statistic is the 5,694 usernames. **All three are published with their
      consumers; none is dropped.** ***`0070` ruling 3 stated "324 users" with NO POPULATION;
      both figures and their populations are given here by `0077`*** — **a count without its population
      is the shape that has recurred through this entire chain**, and it recurred in the ruling written
      to fix a different unlabelled figure. **Step 11 tests whether discovery method biased the pool**,
      so forcing a single value either **drops the overlap or assigns it arbitrarily** —
      and the arbitrary assignment would be invisible in the diff, since both instances would make it
      the same way only by luck. **Two flags let Step 11 cut on either channel or on the overlap.**
- [ ] **`action` IS NOT A ROW-LEVEL COLUMN. EMIT PER-PAIR COUNTS BY ACTION TYPE INSTEAD.** Human Lead
      ruling, 2026-08-13 (`0070`), superseding *"retain `action` as a column"*. **`action` is
      record-level and the row is a pair**, so a single value per row asserts one action per pair, which
      is false. **Step 1 already ruled that check-ins count as watching alongside `scrobble` and
      `watch`, on the ground that `action` is a property of the LOGGING CLIENT rather than of the
      viewing** — so it is **not an outcome variable** and must not be modelled as one. **Counts by
      action type support Step 13's arm without asserting anything about the pair.**
- [ ] Record sample size after each filter
- [ ] **FOUR FILTER POSITIONS REMOVE ZERO BY CONSTRUCTION. KEEP THEM AND LABEL THEM INERT, WITH THE
      REASON.** Human Lead ruling, 2026-08-13 (`0079`). **Positions 1, 2, 3 and 7** — the frame, the
      `L2 = 1` exclusion, the S1 completion rule and outcome assignment — **each remove 0 rows.**
      **Keep them: removing a position removes the check that would catch a future upstream change**, and
      the whole point of a fixed order is that the waterfall is comparable across runs and arms.
      **But an unlabelled always-zero filter reads as evidence THE RULE FOUND NOTHING when it is
      evidence THE RULE CANNOT FIRE — the same defect as an unlabelled code check** (`0069`). **State
      the reason at each:** position 1 because line 1 is already the frame; **positions 2 and 3 because
      line 1 is already the `L2 > 1` S1-completer population** (`0068`) — **and position 3's rule is not
      inert, it removes 58,345 pairs upstream of line 1, which is why its drop set is a deliverable**;
      position 7 because **outcome assignment annotates and removes nothing** (`0046`).
- [ ] **STEP 8 PRODUCES BOTH POPULATIONS, NOT APPLY ALONE.** Human Lead ruling, 2026-08-13 (`0070`).
      **APPLY** = line 1 less D10 = **196,654**; **DERIV** = Step 5 line 4 less D10 = **147,370**, which
      requires S2 evidence. **Step 9 publishes bounds on both and Step 8b reserves fields for both, so
      emitting APPLY alone forces something downstream to rebuild DERIV — a second definition of the
      same population, which is the defect this study has hit most often** (`0058`, `0061`, `0062`).
      **Instance B already rebuilt DERIV to the row, 147,370, from Step 8's own inputs**, so this is
      making an existing capability explicit, not adding work. **Emit the waterfall on both.**
- [ ] **EMIT THE D4 COUNT — S3 without S2.** Human Lead ruling, 2026-08-13 (`0070`). **Step 9 must bound
      it and Step 8b reserves a slot for it, so leaving it out forces Step 9 to compute it — a second
      definition again.** Step 8 holds the episode-level evidence; Step 9 does not.

**Required counts, all to `artifacts/`, counts and aggregates only**

- [ ] **EVERY COUNT AND EVERY INVARIANT IN STEP 8's OUTPUTS NAMES THE PIPELINE IT WAS MEASURED ON —
      ALL OF THEM, NOT TWO.** Human Lead ruling, 2026-08-13 (`0079`), extending `0078`. **Partial
      application is worse than none: two labelled figures imply the other counts and the eight
      invariants did not need it.** **Every bullet in this section, every invariant result, and every
      figure in the waterfall carries its build.** **EVERY COUNT NAMES THE PIPELINE IT WAS MEASURED ON,
      NOT ONLY ITS POPULATION.** Human Lead ruling, 2026-08-13 (`0078`) — **`0047`'s standing rule one layer down.** A count without its provenance **can be correct when written and wrong when read**, because the build moved underneath it and nothing in the text says which build it belongs to. **Write the pipeline at the point of use.**

- [ ] **Both drop counts**: per show, and **per outcome** — the second being pairs whose entire S2
      evidence was dropped, **reported as a share of Never started AT POSITION 5 = 33,373, with the
      post-liveness 32,769 reported alongside.** Human Lead ruling, 2026-08-13 (`0070`). **The drop
      count is a property of the filter, so it measures against what ENTERED the filter** — position 5
      is the liveness rule's input. **The difference is exactly the 604 never-started liveness
      exclusions, and that is itself informative**, which is why both are reported rather than one
      chosen.
- [ ] **Negative-lag report (D2), split THREE WAYS, not two: the S2 finale binds, the S1 completion
      binds, or BOTH bind.** Human Lead ruling, 2026-08-13 (`0070`). **168 pairs have both terms binding on APPLY and the binary split has nowhere to put them** — ***THE POPULATION WAS UNSTATED HERE, AND THE COUNT IS NOT POPULATION-INVARIANT.*** Red Team seventh pass N2, **corrected by BOTH arms on the 2026-08-16 rerun.** ~~168 cannot be correct on both~~ — ***THAT PREMISE IS FALSE AND IS WITHDRAWN.*** **Both arms measured every reading: APPLY is 168 at line 1 (220,107), at position 4 (201,900), at position 5 (196,654) AND post-liveness (195,951)** — all 168 tie pairs survive the APPLY chain, **so the two arms' differing readings would BOTH have given 168 and the agreement was INVARIANCE, not error.** ***DERIV IS 153*** (147,370 and 147,271), **and no entry recorded that until now — which is what made the missing label load-bearing.** **STATE THE POPULATION AT THE POINT OF USE AND MEASURE ON BOTH**: the standing provenance rule (`0047`, `0078` §2), and it bites here because **the count is invariant on APPLY and is not on DERIV.** **The dual diff reads 168 against 168 as agreement**, which is why seven passes did not see it. — an instance would have to choose a side, and two
      instances could choose differently. **A tie is its own category, not a tiebreak.**
- [ ] **Resumption-rate report — D3′, which replaces D3** (`decisions/0034`). Of pairs scored **Started and left at `τ2`** whose `⟦T0⟧ + (W + 2H) × 24h ≤ τ_pull`, report the **share** completing within `[τ2, τ2 + H)`, the **count** of that cleared subpopulation, and its **share of all Started-and-left** — **where "all Started-and-left" means the Started-and-left set ON THE POPULATION AND AT THE ARM NAMED AT THE POINT OF USE** (`0068`), never a figure carried from another arm or another population. **Each arm's denominator is its own.** **Run at every Step 13 `W` arm, each reporting its own cleared count and share** — the clearance contains `W`, so the subpopulation shrinks. **ON STEP 8's RIGHT-CENSORED POPULATIONS THE SERIES IS 99.53% OF STARTED-AND-LEFT AT `W = 46` DOWN TO 97.73% AT `W = 213` (APPLY).** Human Lead ruling, 2026-08-13 (`0075`). ***SUPERSEDED: 95.98% → 91.34%***, which `0034` measured on the **amendment's uncensored estimation sample**, not on Step 8's populations — **and it carried no population at the point of use, which is why `0068` §2a could fix the denominator and not the level.** **The population is stated here so the same gap cannot reopen.** **Both Step 8 instances measured 99.53% → 97.73% independently and identically.** Report alongside, **labelled a count and not a rate**, the 3,440 Started-and-left pairs completing at any point before `τ_pull`, **with its exposure-weighting by show recency stated at the point of use**. **THE 3,440 IS ON THE UNCENSORED ESTIMATION SAMPLE OF 128,099 — NOT ON STEP 8's POPULATION** (`0068`; measured at `0034` §3, where the Started-and-left group is 17,420 before the amendment and 15,174 after). **That is why Step 14 calls it a FLOOR**: the estimation sample excludes the pairs the Step 5 waterfall drops and is not right-censored. **Do not report it against APPLY or DERIV, and state its population wherever it appears.** The two do **not** bracket the quantity — both truncate observation and neither is a lower bound
- [ ] **Never-started post-window diagnostic (D8)**, measured over `H`, not to the pull date. **Unchanged by `decisions/0034` but no longer D3's symmetric counterpart** — D8 measures over `[τ1, τ2)` and D3′ over `[τ2, τ2 + H)`. **D8(ii) is the only bound on the never-started boundary**, and its size is Step 14's ledger item 10
- [ ] **Split-artifact counts (D9)**, both halves: the fabricated never-started row and the silently
      deleted S1-failing counterpart. **RETAIN THE 58,345 PAIRS THAT FAIL THE S1
      COMPLETION RULE — POSITION 3's RULE — AS A SIDE OUTPUT. 58,345 pairs, position-3 rule, measured on
      the position-5 build of 2026-08-13, reproduced independently by both arms** (`0078`). Human Lead ruling, 2026-08-13 (`0075`),
      ***restated by `0077` because it was UNMEASURABLE as written.*** **Position 3 removes ZERO rows
      from the waterfall** — line 1 is already the S1-completer population (`0068`) — **so "position 3's
      drop set" named an empty set**, and both arms had to choose an interpretation to compute anything.
      **They chose the same one and a ruling exists to stop them having to choose.** **The set is the
      pair universe less the completers: 58,345 pairs — position-3 rule, position-5 build of
      2026-08-13** — carrying each pair's distinct-episode counts
      and the show's threshold, which is what half (b) reads. **NOT the set-membership drop rule, which
      is a different rule and deletes 0 records** — naming it would put the wrong rule in the spec.
      **Half (b) is measured on these rows and cannot be computed without them.** Instance A
      found this by needing it. **An instance that does not discover it emits ZERO or fails — and a zero
      here reads as a data finding rather than a missing input**, which is the worse of the two
      failures. ~~**USE THE STRICT KEY AND REPORT THE LOOSE
      COUNT ALONGSIDE.**~~ ***SUPERSEDED by `0090`: D9 publishes as a BOUND, strict the floor and loose the ceiling, NEITHER the point estimate. Strict is no longer "the answer". See the bound bullet above.*** Human Lead ruling, 2026-08-13 (`0074`); **BOTH KEYS ARE DEFINED HERE by
      `0076`, because "strict" and "loose" existed only inside one instance's code, which the other is
      forbidden to read — so the ruled key was undefined on every surface an isolated instance reads,
      and a re-run against the ruling would have reproduced the divergence.**
      **STRICT: lowercase the slug and drop every non-alphanumeric character. Strip NOTHING else** —
      `re.sub(r"[^a-z0-9]", "", slug.lower())`. Two show IDs match only on the same slug modulo
      punctuation. **LOOSE: first remove a TRAILING FOUR-DIGIT YEAR, then apply the strict transform.**
      **Neither key strips a trailing digit group of arbitrary length** — that reduces `the-100` to
      `the`, and it is a THIRD key, not either of these. **One instance used it and published 76
      complementary pairs against the other's 75; that divergence is REPORTED, NOT RECONCILED** (`0076`). **The normalisation rule decides the
      entire number and none was specified:** strict finds **0** complementary signature pairs and loose
      finds **75**, so half (a) is **6 or 0** on an unstated choice. **Loose strips the year and merges
      genuinely different shows** — its largest clusters are **The Twilight Zone, The Traitors and
      Manhunt**, remakes and national versions rather than split metadata.
      **NAME THE UNIVERSE THE CLUSTERING RUNS OVER, AT THE POINT OF USE.** Red Team blocker B1, third
      pass, 2026-08-16 (`0085` §2). **THE TWO ARMS PUBLISHED DISJOINT CLUSTER LISTS ON IDENTICAL
      COUNTS** — one gave `secondchance` 8, `theisland` 7, `maigret` 6; the other `thetwilightzone` 10,
      `thetraitors` 7, `manhunt` 5 — **sharing no member, with maxima 8 against 10**, while every count
      around them reconciled (0 / 75 / 76 both arms; half (a) 0 and 6 both; half (b) 0 and 27 both).
      **That is not a counting difference. It is a difference in WHICH SET OF SHOWS IS BEING
      CLUSTERED**, and the spec never said. **The cluster examples are the EVIDENCE for the loose key's
      only warrant** — that it bounds how wrong strict could be — **so two arms producing different
      evidence for one warrant means the warrant is not reproducible while the deliverables read as
      though it is.** **State the universe explicitly**: all sweep show IDs carrying a slug, or the
      1,138 frame shows, or the D9 candidate pairs. **THE DIVERGENCE IS REPORTED, NOT RECONCILED** — ***SUPERSEDED by `0088` §3, which RULES the universe (U1) — see the bullet above. This text asked for the universe to be NAMED and left it unruled; it is now ruled, and the superseded framing sat BELOW its replacement in the same section, which is the shape `0067`, `0076` and `0083` §3a each fixed elsewhere (found by instance B, 2026-08-16).*** no
      universe is ruled here. **If the two arms name the SAME universe and still differ, one has a bug
      and that is the finding.** ***`0084` §5 item 3 filed this as an arm-against-SPEC wording question
      about what "largest cluster" ranks by. That was wrong: it is an ARM-AGAINST-ARM divergence, which
      is the dual diff, and it was mis-filed partly because one arm's list happens to match the three
      names above.*** **The loose count is reported
      because it BOUNDS HOW WRONG STRICT COULD BE**, and **the error runs OPPOSITE to D9's own
      lower-bound caveat** — which is why it publishes rather than being resolved away.
      **REPORT BOTH HALVES UNDER BOTH KEYS — FOUR NUMBERS, NOT THREE.** Human Lead ruling, 2026-08-13
      (`0078`), closing the one live asymmetry: **instance A published half (b) under strict only while
      instance B published it under both.** **The requirement follows from `0074` ruling 5's own
      reason** — the loose count is published **because it bounds how wrong strict could be**, and that
      reason **applies to half (b) exactly as it applies to half (a)**. **Publishing the bound for one
      half and withholding it for the other leaves the reader unable to bound the total**, and the error
      runs opposite to D9's own lower-bound caveat, which is the direction they were not warned about.
- [ ] **Right-censoring removal as TWO lines** — the `max(W, 91)` term and the incremental `+ H` term — each with its upward direction on the headline named
- [ ] **Retained-pair counts PER AIR PERIOD after right-censoring, not only in aggregate.** Human Lead decision, 2026-08-12 (`decisions/0033-step8-per-air-period-censoring-counts.md`), closing the Product review's finding 5. **97.40% of pairs survive right-censoring at `W = 108`** — **restated here because there is NO aggregate line above stating it** (`0068`), and **corrected from 97.6% by `0070`.** **KEEP THE MANDATED FILTER ORDER; the published percentage is what moves.** `0033`'s figures — 97.6 / 98.0 / 97.5 / 96.0, and 89.7% for 2023–2025 at `W = 213` — were computed on the **position-3** output (220,107). **The mandated order censors the position-4 output (201,900)**, which gives **97.40 / 97.8 / 97.4 / 95.9 and 89.5%**, and **turns the documented 10.3% loss into 10.5%.** **The order was set at `0029` on the stated ground that censoring is objective and independent of behaviour while contamination is not; the 10.3% predates it. Changing a filter order to preserve a published percentage is backwards.** **That aggregate hides that the loss is cohort-asymmetric**: at the Step 13 arm of `W = 213` the 2023–2025 cohort loses **10.5%** of its pairs against **3.0%** pre-2020 — **BOTH on the mandated order.** **10.5% not `0030`'s 10.3%, and 3.0% not its comparator 2.7%**, which were measured in the opposite order to the one this step mandates (`0070`, comparator corrected by `0073`). **`0070` moved the first figure and left the second**, so the sentence carried two orders at once — **found independently by both Step 8 instances**, which is what a dual run is for. Report it **for every `W` arm Step 13 tests**, since the asymmetry widens with `W` and the arms now run to 213. Without this line, whether the modern cohort survives to the headline in usable numbers is invisible — and it is the cohort a roadmap cares about most.
- [ ] **`pull_date`, the earliest and latest per-user fetch dates, and the count of records discarded for `watched_at >= pull_date`**
- [ ] **Per-bucket show and pair counts for all five D12 cadence buckets**, plus the count of shows within 1 day of a bucket boundary
- [ ] **Metadata-disagreement counts**, including the subset where `aired_episodes < |E|` for S2. Listed exceeding aired tightens the 90 percent threshold and pushes real completers out — name that direction
- [ ] **Assert invariant: the abandonment point `p` lies in `(0, 1]` on every Started-and-left row and
      is null elsewhere. CODE CHECK.** Specified by `0074`; ***label corrected from DATA CHECK by
      `0076`***, on **both instances' own proof**: Started-and-left requires `|A| ≥ 1` so `m_H` exists,
      and **set membership bounds the rank numerator in `[1, L2]`** — **no data configuration puts `p`
      outside `(0, 1]`**, and it fails only on the withdrawn raw-ratio form. **Keep it** — Step 10
      publishes `p` and both instances ran it unprompted — **but it proves the code, not the rule.**
- [ ] **The set-membership drop rule is a COVERAGE COUNT, NOT AN INVARIANT.** Human Lead ruling,
      2026-08-13 (`0074`), resolving a 7-against-6 divergence in the dual run. **Step 8's own bullet
      already calls it "an implementation check, not a data check."** **Report the records examined and
      the records dropped**; do not assert it. **`0069` established that an unlabelled code check reads
      as evidence FOR THE RULE when it is only evidence that the code ran**, and asserting this one adds
      another pass to a report where **five of six already cannot fail** (`0076`).
- [ ] **Assert invariant: NO ACCOUNT IS DROPPED WHOLESALE BY THE PAIR-LEVEL LIVENESS FILTER. DATA
      CHECK.** Human Lead ruling, 2026-08-13 (`0076`). **Assert that the count of accounts holding both
      a live and a not-live pair is greater than zero**, and report it. **703 pairs from 216 accounts is
      consistent with BOTH a pair-level and an account-level implementation** and nothing in the set
      distinguished them. `CLAUDE.md` and Step 7: *"One account can be live for one show and not
      another. Never drop a user wholesale."* **This can fail on real data.**
- [ ] **Assert invariant: NO `access_denied` OR SKIPPED ACCOUNT IS READ AS EMPTY. DATA CHECK.** Human
      Lead ruling, 2026-08-13 (`0076`). **Assert that no account recorded `access_denied`,
      over-tolerance or otherwise skipped contributes a pair scored never-started**, and report the
      counts. `CLAUDE.md`: *"a skipped user silently read as empty becomes a false 'never started' in
      the headline"*; rule and evidence at `artifacts/step0-access-and-setup.md` §7. **This can fail on
      real data, and it fails in the direction of the result.**
- [ ] **`p_at_bound` MARKS WHETHER `p` REACHED ITS BOUND, NOT WHY.** Human Lead ruling, 2026-08-16
      (`0083` §2), restating `0082`. **TRUE where `p` reached its bound; null where `p` is null.**
      ***SUPERSEDED — `0082` §2's definition by two MECHANISMS: "TRUE where the rank numerator saturated
      at `L2`, FALSE where the pair left at the final episode." Those clauses are COEXTENSIVE BY
      CONSTRUCTION and the FALSE class is EMPTY.*** On the adopted rank form
      `p = |{e ∈ E2 : e ≤ m_H}| / L2`, **the set-membership drop rule puts `m_H ∈ E2`**, so the numerator
      equals `L2` **iff** no listed episode exceeds `m_H`, **iff** `m_H = max(E2)`, **and `max(E2) = F2`**
      — which *is* "left at the final episode."
      ***THE CHAIN HAS THREE LINKS AND ONLY TWO ARE CONSTRUCTION.*** Red Team P4, third pass
      (`0085` §4). `numerator = L2 ⟺ m_H = max(E2)` is construction given `L2 := |E2|`, which the spec
      fixes. **`max(E2) = F2` IS NOT** — it holds only because **the finale is the highest-numbered
      listed episode**, and **where a season lists an episode numbered above its finale the two
      separate.** That is the `s2_aired_lt_listed` case **this step is told to count**. **It is
      measured, not assumed: 0 shows in frame** (`shows_where_max_E2_differs_from_L2 = 0`,
      `s2_aired_lt_listed` 0 shows), **and the frame does not move across Step 13's grid, so nothing
      reopens.** ***`0083` §2 named TWO causes for a future FALSE row. There are THREE, and this is the
      third*** — assert it and state its count.
      **EMIT THE EMPTINESS MEASUREMENT ON BOTH POPULATIONS, AT BOTH POSITIONS — FOUR CELLS EACH.**
      Red Team blocker B2, third pass (`0085` §3). **Total, in-both-classes, saturated-not-final,
      final-not-saturated, and in-neither — on APPLY position 5, APPLY post-liveness, DERIV position 5
      and DERIV post-liveness.** **This is `CLAUDE.md`'s standing rule, not a new one**: *both
      populations, always; a correction applied to one and not the other is the same defect as not
      applying it at all.* ***One arm emitted APPLY only, and `1,056` appeared nowhere in its
      deliverable*** — **while the ground for keeping the column at all is that "an emptiness asserted
      in prose and never emitted cannot be checked."** **On DERIV that ground was unmet.**
      **Measured, both arms, 2026-08-16 clean run, APPLY: at position 5, 1,246 rows in BOTH classes, 0
      saturated-not-final, 0 final-not-saturated, 0 in neither; post-liveness 1,230 / 0 / 0 / 0.
      DERIV: 1,072 / 0 / 0 / 0 at position 5 and 1,056 / 0 / 0 / 0 post-liveness** (instance B; the
      DERIV pair is stated here because `0083` §2 gave APPLY only and the standing rule requires both).
      ***AND 1,246 AND 1,230 ARE NO LONGER A SPLIT.*** They are correct counts and both arms reproduce
      them, but they are **one class counted twice, not two classes summed** — **using them as evidence
      that the column separates anything is a WITHDRAWN ARGUMENT** (`CLAUDE.md`, third blindness class).
      ***WITHDRAWN, and it is a MOTIVE not a figure (`0082` §2): "a distribution with a spike at 1.0
      means two different things about viewers and the column cannot say which." FALSE on the adopted
      form — the spike means one thing.*** **A SECOND fact, measured and NOT this argument: 0 of 1,138
      frame shows have any S2 numbering gap**, so `E2 = {1…L2}` everywhere and the rank form reduces to
      `m_H / L2`. **That one is DATA and could be false on another frame; the coextensivity would still
      hold.** **THE COLUMN IS KEPT**, because **Step 10 publishes the abandonment distribution off
      `abandonment_point_p` and needs the spike LABELLED**, and because **an emptiness asserted in prose
      and never emitted cannot be checked.** **It stays empty through Step 13's `W` grid** — the rank
      form and set membership are both `W`-invariant — **so a FALSE row anywhere means one of them has
      broken, and that is worth catching.** **Still report the `p = 1.0` totals: 1,246 at position 5 and
      1,230 post-liveness on APPLY**, as totals, not as a sum of two classes.
- [ ] **D9 PUBLISHES AS A BOUND, NOT A POINT ESTIMATE. STRICT IS THE FLOOR, LOOSE IS THE CEILING, BOTH
      LABELLED.** Human Lead ruling, 2026-08-16 (`0090`). ***SUPERSEDES the framing "USE THE STRICT KEY
      AND REPORT THE LOOSE COUNT ALONGSIDE" (`0074` ruling 5), under which STRICT WAS THE ANSWER and
      loose was context.*** **Neither endpoint is the point estimate and neither may be quoted as
      "D9's result".**
      **This is `0074` ruling 5's OWN REASON carried to its conclusion**: the loose count publishes
      **because it bounds how wrong strict could be**, and a quantity published to bound another is an
      **endpoint**, not a footnote. **`0078` §3 already ran this argument once** — it extended the loose
      count to half (b) *"because `0074` ruling 5's own reason applies to half (b) exactly as it applies
      to half (a)"*. **Same reason, one step further.**
      **THE BOUND IS `[strict, loose]` ON EVERY D9 QUANTITY THAT HAS BOTH FORMS**, not on the headline
      alone — **complementary signature pairs `[0, 75]`, half (a) `[0, 6]`, half (b) `[0, 27]`.**
      **Applying it to one and not the others is the defect `0078` §3 corrected**, and the ruling's
      phrase *"this half"* is read this way for that reason; **if the Human Lead meant a single half,
      say so and it narrows.**
      **DIRECTION IS PART OF THE LABEL.** **Strict is the FLOOR because it only matches slugs identical
      modulo punctuation, so it cannot over-count; loose is the CEILING because stripping a trailing
      year MERGES GENUINELY DIFFERENT SHOWS** — remakes and national versions. **The error runs OPPOSITE
      to D9's own lower-bound caveat**, which is why the interval is published rather than resolved away.
      **THE THIRD KEY IS NOT AN ENDPOINT.** Stripping a trailing digit group of arbitrary length reduces
      `the-100` to `the`; its **76** is a different key's answer, **reported as a divergence and never as
      the ceiling** (`0076`, `0078` §3).
      **A ZERO FLOOR IS NOT AN ABSENCE OF EVIDENCE.** `0` is a **measured** floor on a stated coverage,
      and the coverage publishes beside it — **a bound whose floor is 0 and whose coverage is unstated is
      indistinguishable from a check that looked nowhere.**
- [ ] **THE D9 CLUSTERING UNIVERSE IS U1 — ALL SLUGGED SWEEP SHOW IDs — RANKED BY DISTINCT STRICT KEYS
      MERGED.** Human Lead ruling, 2026-08-16 (`0088` §3), closing the gap `0085` §2 opened and `0086`
      §1 located. **BOTH ARMS CLUSTER THE SAME OBJECT: every distinct show ID appearing anywhere in the
      pulled sweep that carries a slug, deduplicated to one row per show ID.** **NOT U2 (the 1,138 frame
      shows) and NOT U3 (the 75 D9 candidate pairs).**
      **The ground:** the artifact D9 hunts is **a viewer's history splitting across two metadata
      entries for the same show**, and **that split can occur anywhere in a history, not only among
      shows that survived the frame filters.** **A universe inside the frame can only find splits where
      BOTH sides made the cut**, which is the narrowest case. **This is a bound on how wrong the data
      might be, and a bound computed on a narrow slice bounds very little.**
      ***RECORDED WITH THE RULING, because it changes what the ruling buys: D9's SEARCH ALREADY RUNS ON
      THE WHOLE SWEEP IN BOTH ARMS*** — 726,103 candidate `(user, show)` pairs examined across the
      sweep, 747,478 **distinct `(user, show)` pairs**. ***CORRECTED `0089` §2(b), propagated 2026-08-16 (`0094`): 747,478 IS DISTINCT `(user, show)` PAIRS. ~~undeduplicated season-coverage rows~~ — that axis was `0088` §2's and is WRONG. Arm A's undeduplicated row count is 1,217,122; arm B's own row object is 1,007,729 over a different mask. The relation that DOES hold: 747,478 − 21,376 S3-only = 726,102 against arm B's 726,103, the one-pair divergence both arms report.*** **So this ruling does NOT widen what D9 finds; the strict and
      loose counts are unchanged by it.** **It fixes WHICH CLUSTERS ARE ILLUSTRATED**, which is the
      evidence for the loose key's only warrant, and it **makes the two arms' `U1` one defined object**
      rather than two sets 62 apart under a shared label.
      **THE RANKING BASIS IS DISTINCT STRICT KEYS MERGED** — how many separate metadata entries the
      loose key collapsed into one. **It was unstated and it reorders the list on its own**: the same
      universe under the same key, ranked by distinct show IDs instead, displaces `maigret` with
      `blackout`. **Name the basis at the point of use; a list without it is not reproducible.**
      **`task-sheet.md`'s own former illustration — The Twilight Zone, The Traitors, Manhunt — was U3**
      and is **SUPERSEDED as the example**; under U1 the largest clusters are `secondchance` (8),
      `theisland` (7), ~~`maigret` (6)~~ ***— WITHDRAWN. `0089` §2(c): "THE THIRD PLACE IS NOT DETERMINED AND THIS ENTRY SHOULD NOT HAVE NAMED ONE." There is a SIX-WAY TIE at 6 — `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor` — and which appears third is the TIE-BREAK, which no rule specifies. NEITHER ARM PICKED `maigret`. Marked at the point of use 2026-08-17 (`0099`), found by `second-brain`: this line contradicted its own file 65 lines lower, and both copies being identical meant the dual diff could not see it. Published residual 7 of the gate approval.*** **The names are not wrong; they are a different universe's
      answer**, which is the whole reason this needed ruling.
- [ ] **A GATE DELIVERABLE ASSERTS ONLY WHAT ITS OWN ARM MEASURED.** Human Lead ruling, 2026-08-17
      (`0096` ruling 1). **Its figures, its inputs, its limits — and nothing else.** ***It does NOT
      assert the state of other steps, other gates, the other arm, the shared controls, or the study as
      a whole.*** **An arm cannot know those things**: it measures a surface at one instant and publishes
      into a file that is never re-read against the world, so **every such claim is expiry-dated from
      birth.** **THREE CONSECUTIVE RED TEAM PASSES FOUND A STALE ONE**, and the last was worse than
      stale — a deliverable told its reader that `check_surfaces.py` **EXITS 1** when it exits 0, true
      when measured and false when read.
      **This is the `## Derived figures` provenance rule applied to STATEMENTS rather than FIGURES.** A
      figure without its provenance is unreadable; **a statement about a surface the arm does not own is
      unreadable the same way and worse, because it looks like a finding.**
      **EXCLUDED, CONCRETELY: control exit statuses** — report them to the Human Lead, they belong in
      `logs/` and never in `artifacts/`; **the disk state of other surfaces** — which files exist, which
      carry a string, how many entries `decisions/` holds; **build-history narration** — a build stamp
      and a pointer to the run record, not a chronicle of what earlier builds got wrong; and **whether
      any step or gate is approved**, including this one.
      **STILL REQUIRED: the arm's own defects, its own open items, and its own divergences from the
      spec — those it measured.** **An arm that notices something wrong on a surface it does not own
      REPORTS IT to the Human Lead and does not publish it as a finding in a deliverable.**
- [ ] **`decisions/` MAY CARRY CROSS-ARM CONTENT, AND THE ARMS ARE TOLD SO.** Human Lead ruling,
      2026-08-17 (`0096` ruling 2). ***This WITHDRAWS `0095` §1's exclusion of "a decision entry."***
      **A ruling has to record what each arm found in order to explain why it was ruled**, and
      forbidding cross-arm content there would mean **a ruling cannot cite its own evidence.**
      **The distinction is what the isolation rule is FOR: it exists to stop the arms COPYING EACH
      OTHER'S IMPLEMENTATION, not to keep a number the Human Lead has already ruled on out of reach.**
      **An UNRULED characterisation relayed into a launch instruction is a measurement the receiving arm
      cannot check, and stays FORBIDDEN** (`0095` §1). **A RULED figure in a decision entry has already
      been through the Human Lead's diff — it is a spec input, not a peek at the other arm's work.**
      **The leak is made EXPLICIT rather than accidental**: both `analytics-engineer` files state this,
      so an arm reading `decisions/` knows what it is reading. **An arm may cite such content naming
      `decisions/` as the source; it may NEVER open the other arm's output folder, and it may NEVER
      treat a cross-arm figure as something it measured.**
- [ ] **THE TWO UNASSERTED MANDATES ARE MEASURED, NOT SELF-REPORTED.** Human Lead ruling, 2026-08-16
      (`0088` §1), on Red Team's B3/F1, which blocked the gate on the third and fourth passes.
      **The mandates are the HALF-OPEN UTC-INSTANT FORM and D11-AS-GLOBAL-CUTOFF** — not invariants 7
      and 8, which are already measured, already published and already labelled DATA CHECK by both arms.
      ~~**Both arms' compliance is TRUE and was independently confirmed** — no `.date()`, `dt.date`,
      `normalize()` or day-flooring anywhere in `step8_*.py`, instants int64 seconds throughout.~~
      ***WITHDRAWN 2026-08-16 (`0092` §4), found by instance A: THE BLANKET CLAIM IS FALSE OF ARM A and
      it was asserted about BOTH ARMS.*** Red Team's fourth pass verified it and it was recorded here as
      verified of both; **it was verified of neither.** ***`T0` IS DAY-FLOORED*** — which is exactly why
      `τ1` and `τ2` are midnight-aligned, and therefore why the boundary window `0088` §1(a) named,
      `[τ − 24h, τ)`, **was the interval on which the two forms AGREE.** **What IS true and is the
      operative requirement: no BOUNDARY TEST uses the date-level form** — `date(watched_at) <= T1` must
      not appear anywhere in the implementation. **State that, and do not restate the blanket claim about
      the module.**
      ***THAT IS NOT WHAT WAS MISSING. NOTHING MEASURED WHETHER EITHER MANDATE IS LOAD-BEARING ON THIS
      DATA*** — and an unmeasured pass is indistinguishable from a check that looked nowhere, which is
      this study's own standing rule. **Emit three things:**
      **(a) THE BOUNDARY WINDOW.** On the position-5 row set, **both populations**: the count of S2
      records in `[τ1 − 24h, τ1)`, the count falling **exactly at** `τ1`, and the same two at `τ2`.
      **These are the rows on which the half-open and date-level forms could differ. IF THE COUNT IS 0,
      LABEL THE INVARIANT VACUOUS — do not let it pass silently.** A zero that is stated as a zero is
      evidence; a zero that arrives as a pass is not.
      **(b) THE PER-SITE D11 TABLE.** D11 is stated to apply *"to EVERY computation"* and one arm names
      **five sites in prose with a count at none.** Emit records excluded by D11 at **each** site
      separately — `A`, `A_H`, each of the four `action_count_s{1,2}_*`, the liveness evidence, D9's
      coverage rows, and the S1 completion walk — **and assert at each site, not once and about the
      rest.**
      **(c) PROMOTE THE EXISTING ASSERTION.** `assert (tau2[pos5] > τ_pull).sum() == 0` already runs in
      one arm's pipeline but sits **outside the published invariant set**, so no reader of the
      deliverable can see it. **Publish it, labelled CODE CHECK.**
      **The ground for ruling rather than publishing a residual:** the unstated version of exactly this
      scope produced Step 7's **792-against-791**, where one arm applied the restriction and the other
      did not. **A mandate claimed satisfied with nothing measuring it is the shape that has already
      cost this study once.**
- [ ] **THE D9 COVERAGE QUANTITIES ARE REPORTED AS SEPARATE OBJECTS, NOT RECONCILED — AND THE MISLABEL
      IS FIXED.** Human Lead ruling, 2026-08-16 (`0088` §2), on Red Team's F2.
      **(a) FIX THE LABEL.** One arm publishes **46,428** and **46,366** for one labelled quantity **27
      lines apart in one section**. The second is computed off the **D9 coverage pivot** and is
      **mislabelled `distinct_show_ids_in_the_sweep`**; its *"0 carry no slug"* clause is therefore
      computed against the wrong base. **Correct the label to what it counts.**
      **(b) NAME WHAT EACH COVERAGE FIGURE COUNTS, AT THE POINT OF USE.** **747,478 and 726,103 ARE
      DIFFERENT OBJECTS AND ARE BOTH CORRECT**: 747,478 is ~~**undeduplicated user-show SEASON-COVERAGE
      ROWS**~~ ***CORRECTED `0089` §2(b), propagated 2026-08-16 (`0094`): 747,478 IS DISTINCT `(user, show)` PAIRS. ~~undeduplicated season-coverage rows~~ — that axis was `0088` §2's and is WRONG. Arm A's undeduplicated row count is 1,217,122; arm B's own row object is 1,007,729 over a different mask. The relation that DOES hold: 747,478 − 21,376 S3-only = 726,102 against arm B's 726,103, the one-pair divergence both arms report.*** 726,103 is **distinct candidate `(user, show)` PAIRS**. A user-show carrying two seasons
      contributes **two rows and one pair**. **THIS IS ONE NAME OVER TWO QUANTITIES, NOT A DIVERGENCE**
      — and **reconciling would collapse two real objects into one**, which the standing rule forbids.
      **Each arm states which it publishes and what it counts.**
      **(c) IF THE TWO ARMS' UNIVERSES DIFFER, THEY ARE TWO OBJECTS AND ARE NAMED AS TWO.** The arms'
      slugged-show-ID sets stood **62 apart** while both were called `U1`. **A shared label over two
      sets is the defect; the sets themselves may both be right.**
      **(d) STRIKE THE OVERSTATED SENTENCE.** ~~*"The run asserts this, so a report that omitted a
      population could not be written by this pipeline."*~~ **It is a control asserted to exist**, and
      **8 of 13 coverage identities are `cover(unit, pop, N, N)` where the population size and the
      asserted count are THE SAME EXPRESSION**, so they cannot detect an invariant run on a population
      other than the one named. **Struck whatever else is ruled.**
- [ ] **EVERY INVARIANT NAMES THE POPULATION IT RUNS ON, AT THE POINT OF USE — AND ACCOUNTS FOR EVERY
      ROW IN IT.** Human Lead ruling, 2026-08-13 (`0080`). **This is the provenance rule applied to
      invariants rather than to figures:** an invariant that **passes on one population and was never run
      on another reads as a pass on both.** **The dual run diverged on the coverage of five of the
      eight**, and one gap was a real hole: **one arm asserted `p` on 19,042 rows and the non-S&L clause
      on 177,513, summing to 196,555 against a 196,654-row table — 99 rows covered by neither clause**,
      and those 99 are exactly the started-and-left liveness exclusions. **A passing invariant whose
      coverage the instance chose is a code check on the instance's choice.**
      **EVERY invariant reports `rows_asserted + rows_not_asserted = rows_in_the_stated_population`, and
      the identity must hold.** The populations:
      **1. Outcome partition** — **the 196,654 position-5 row set AND the 195,951 live subset, both
      stated**, and the DERIV pair 147,370 / 147,271. The table carries all position-5 rows, so the
      partition holds on both and neither substitutes for the other.
      **2. Monotone filter counts** — **BOTH chains**, APPLY's seven positions and DERIV's.
      **3. `|D| ≤ L`** — **both seasons, on every pair the set-membership rule examines**, with the pair
      count and the record count stated. One arm ran S1 and S2 on 278,452 pairs, the other S2 only on
      196,654; **the wider is required and the narrower does not substitute.**
      **4. `A ⊆ A_H`** — the **196,654 position-5 row set**, every row.
      **5. Clock start** — the **196,654 position-5 row set**, every row, with the first-pass S1
      completion date **recomputed independently**, which is the only thing giving this one force.
      **6. `p ∈ (0, 1]`** — **all 19,141 Started-and-left rows at position 5**, null on the other
      **177,513**. **19,141 + 177,513 = 196,654 exactly**, and that identity is what closes the hole.
      **Do not take the numerator post-liveness and the denominator pre-liveness.**
      **7. No account dropped wholesale** — **both populations**: the 2,422 accounts in APPLY's
      position-5 row set and DERIV's, each reporting accounts holding both a live and a not-live pair.
      **8. No `access_denied` or skipped account read as empty** — **the full account ledger, in
      ACCOUNTS**, with the skipped classes counted separately and the pairs they contribute stated.
- [ ] **EVERY INVARIANT BELOW CARRIES A LABEL — CODE CHECK or DATA CHECK.** Human Lead ruling, 2026-08-13 (`0068`), resolving a live divergence: **the two read-back instances split 4-of-6 against 6-of-6** on how many cannot fail on data alone. **A code check catches an implementation that computed something wrongly; it cannot fail on any data, and it is not evidence for the rule.** A data check can fail on data. ***SUPERSEDED — "The count is four pure code checks, one that is a code check by construction and a genuine cross-check as specified, and one item that is not an invariant at all." That was the pre-`0076` reading of a SIX-member set; `0076` corrected it to FIVE of six with ZERO pure data checks, and the set is now NINE (`0088` §1c). Struck 2026-08-16 (`0089`), reported independently by BOTH arms — it was contradicted 280 lines lower in this same file.*** — which is why both readings were defensible and neither was stated.
- [ ] **Assert invariant: outcome states are mutually exclusive and sum to THE POST-POSITION-7 ROW SET** — the rows remaining after outcome assignment, which is the only population the phrase can mean and was not stated (`0068`). **CODE CHECK.** Step 1 §7's partition is proved exhaustive and disjoint, so this can only catch an assignment coded wrongly.
- [ ] Assert invariant, every row: **`A ⊆ A_H`** (`decisions/0034`). **CODE CHECK, not a data check** — true by construction since `τ1 < τ2`, so it can only catch an implementation that computed the two sets wrongly and is not evidence for the rule
- [ ] **Assert invariant: filter counts decrease monotonically — CODED AS `>=`, NOT `>`.** Human Lead ruling, 2026-08-13 (`decisions/0047`). **KEPT, but its stated reason is corrected (`0049`).** Under the superseded ALT the DERIV exclusion set was empty and decrease was non-strict there. **Under ALT-BROAD decrease is STRICT on both populations at every arm.** `>=` is retained because **the invariant must not encode a property of one rule** — a filter position that legitimately removes nothing must not fail an assertion, and Step 13's arms and Step 8's other positions can produce exactly that. **CODE CHECK** (`0068`): filters only remove rows, so this can fail only on an implementation that adds them — a duplicating join, most likely. **And it is load-bearing in fact, not only in principle: position 2 removes exactly 0 pairs on this frame**, which both read-back instances measured independently.
- [ ] **Expect 703 liveness exclusions at position 6, `W = 108`, ON APPLY = 196,654 — the position-5 output — 604 never-started plus 99 started-and-left, from 216 accounts — and treat a mismatch as a POPULATION defect before an implementation one.** **The denominator is stated because the count alone cannot be checked without it** (`0068`). **On DERIV = 147,370 the same rule excludes 99, all started-and-left, from 73 accounts.** **THIS IS NOT AN INVARIANT** — see the invariant labelling below. It is a **population reconciliation**, and the spec's own instruction to suspect the population first is what makes it one. **793 is ALT-MATCHED's withdrawn answer; producing it means the reverted two-anchor rule was implemented, and that IS a divergence.** (`0054`) Human Lead ruling, 2026-08-13 (`decisions/0047`). Step 7 measured 604 on the application population, but built it from the Step 5 pair table rather than through positions 1–5. **A different count most likely means the frame join, the `L2 = 1` exclusion or the censoring differs — not that the liveness rule was coded wrong.** Check the population first.
- [ ] **Assert invariant: distinct episodes never exceed season length. CODE CHECK, not a data check** (`0068`) — **Step 8's own set-membership bullet already establishes `|D| ≤ L` by construction**, since an episode whose `number` is not in the season's listed set `E` is dropped. **It is labelled here for the same reason `A ⊆ A_H` is: an unlabelled code check reads as evidence for the rule, and it is not.**
- [ ] Assert invariant, for every row: clock start is on or after the S2 finale date, clock start is on or after the first-pass S1 completion date, and clock start equals one of those two dates. The old invariant, no clock start precedes an S2 premiere, is vacuous under a finale-anchored clock and catches nothing. **This check must compute the first-pass S1 completion date INDEPENDENTLY, not read back the pipeline's value** — otherwise its equality clause proves nothing. **CODE CHECK BY CONSTRUCTION, DATA CHECK AS SPECIFIED** (`0068`). `T0 = max(S2_finale_air_date, S1_completion_date)`, so "on or after both" and "equals one of them" are true of any correct `max()` — **but the independence requirement is what gives it force**: recomputing the S1 completion date from the records can disagree with the pipeline's stored value, and that disagreement is a real finding. **Read back rather than recomputed, it degrades to a code check and proves nothing.**
- [ ] Report all invariant results
- [ ] Write the table to `processed/`. The filter waterfall and invariant report, which are counts only, go to `artifacts/`.

**Deliver:** analysis table in `processed/`; **the position-3 drop set — the 58,345 pairs failing the S1
completion rule — as a PIPELINE OUTPUT of the same run, not a helper script's side file**; filter waterfall
and invariant report in `artifacts/`

- [ ] **THE POSITION-3 DROP SET IS A DELIVERABLE, PRODUCED BY THE PIPELINE.** Human Lead ruling,
      2026-08-13 (`0079`). **D9 half (b) cannot be computed without it, and its absence returns 0
      SILENTLY** — a plausible-looking data finding rather than an error. **That is exactly what `0075`
      ruling 2 was written to prevent, so leaving the input as a working file defeats the ruling that
      requires it.** It must be **named in the deliverable list**, **written by the same pipeline run
      that writes the table**, and **carry each pair's distinct-episode counts and the show's
      threshold**, which is what half (b) reads.
**Check:** dual implementation diff
**Review:** Red Team on the filter order and the invariant set
**Approval:** required before any result is computed

---

## Step 8b: Output schema

**Owner:** Analytics Engineer
**Mode:** Chained

**Defined in a prior session and never propagated.** Added to this file 2026-08-13 (`decisions/0066`)
with two amendments that postdate its drafting, both marked below.

- [ ] **Define the JSON schema the Step 16 visualization reads from.**
- [ ] **One entry per tested `W` arm.** ***AMENDED:*** the original said *"per tested combination of `W`
      and liveness threshold."* **There is no liveness threshold.** A numeric threshold was derived
      three times — 632 d, then 1,293 d — and **DELETED** (`0042`); the adopted rule is **parameter-free**
      (`0048`, approved `0064`). ~~**The key is `W` alone.**~~ ***SUPERSEDED TWICE and this line is the
      ORIGINAL, not a restatement: `0102` added `clock_origin`, `0111` (E2) added `producing_step`.
      THE KEY IS ~~`(W_days, clock_origin, producing_step)`~~. ***SUPERSEDED — a FOURTH dimension was added at `0114` (E14): the key is `(W_days, clock_origin, producing_step, adopted_rule_revision)`. Marked at the point of use 2026-08-19 (`0116`), found by arm `a`: `0114`'s propagation ADDED the four-field key in new text and left the three-field statements standing — in three places BELOW their own replacement. `0113` §2's defect, one entry later, and invisible to `check_surfaces.py` because an arm key is a STRUCTURAL CLAIM, not a number or a registered phrase.****** **What this bullet's amendment actually
      ruled — that NO LIVENESS PARAMETER enters the key — stands untouched**, and is why `632` and
      `1,293` must not reappear as schema
      keys — and note that **`632` is also the legitimate frozen-D10 never-started component at
      `W = 125`**, so a blind grep for the deleted threshold produces a false positive there (`0051` §3).
- [ ] **Each entry carries, for that arm:** the **three outcome shares**; a **confidence interval on
      each**; the **bounds** (below); the **retained row count**; the **abandonment distribution**; and
      the **filter waterfall counts**.
- [ ] **THE BOUNDS ARE TWO, NOT ONE, AND BOTH POPULATIONS CARRY THEM.** ***AMENDED:*** the original said
      *"floor and ceiling bound,"* singular. Step 9 publishes **two**:
      - **Never started** — floor and ceiling. **No conditional sub-interval**: the sub-interval
        conditions on *this bound's own* exclusion set, so it does not exist for never-started
        (`CLAUDE.md`, `## Derived figures`). **The schema records it as structurally absent, with the
        reason, rather than omitting the field** — an absent field and an inapplicable one must not look
        alike. **On DERIV this bound is DEGENERATE**, `[6.2055%, 6.2055%]`, width 0.0, and the schema
        must be able to express a zero-width bound without it reading as missing data.
      - **Started and left** — floor, ceiling, **and the conditional sub-interval**, which is the
        started-and-left share *given that every never-started exclusion is a true decline*. **Its
        conditioning constrains the 604 and says nothing about the 90**, so its floor moves with the
        bound floor (`0056`). **On DERIV the sub-interval COINCIDES with the bound**, because the
        never-started exclusion component is 0 there — the schema must record coincidence as a measured
        fact, not by writing the same numbers twice with no note.
      - **Both on APPLY (n = 196,654) and DERIV (n = 147,370). Every bound field states its population**
        (standing rule, `0047`). **APPLY and DERIV are separate arithmetic, never one field with a
        population flag.**
- [ ] **Continued has a CEILING and it is part of the entry** (`0050`, `0052`). **The three ceilings
      cannot all hold** — APPLY sums to 100.7104%, DERIV to 100.1276% — so **the schema must carry the
      three-ceiling sum and its excess per population**, and must not permit a consumer to read three
      ceilings as simultaneous. **Continued must not be emitted as a point.**
- [ ] **Carry the scope qualifier as a field, not as prose in a caption** (`0062`): the bound is
      **covering with respect to insertion-dormancy, exhaustively; open only across channel classes
      (D4, D9)**. **D4 and D9 publish alongside and are never folded in**, so the schema has slots for
      them.
- [ ] ***ARM FILES DO NOT CARRY `channel_classes`.*** Human Lead ruling, `0114` (E8). **It holds Step
      8's D4 and D9 figures, so requiring it in seven arm files creates SEVEN WRITERS OF A FIGURE NONE OF
      THEM PRODUCED.** ***Q1's class at the top level, and the FOURTH appearance of
      one-slot-vs-one-definition.*** **Add the `TOP_LEVEL_PUBLISHER` row: the MERGED document carries it
      ONCE, filled at Step 13b, sourced from Step 8's artifact.** **Arm files use the ABSENCE IDIOM.**
- [ ] ***PUBLISHER ROWS KEY ON ARM IDENTITY, NOT PRODUCING STEP ALONE.*** Human Lead ruling, `0114`
      (E13). ***Where the schema's own text says NO PRODUCER EXISTS at an arm, an absence record is
      LEGAL there and `S22` must accept it.*** **The schema's text and its control currently disagree
      — the TEXT IS RIGHT.** **`BLOCK_PUBLISHER` makes `S22` require `waterfall`,
      `liveness_exclusions` and `retained_by_air_period` wherever a `step9` entry is primary, including
      a PREMIERE-ANCHORED arm where the schema itself says nothing produces one.**
      ***ABSENCE STATED, NOT SILENCE*** — the record is required; what is not required is a figure no
      step makes.
- [ ] ***THE ADOPTED-RULE REVISION JOINS THE KEY AS A FOURTH IDENTITY DIMENSION.*** Human Lead ruling,
      `0114` (E14). **The key is `(W_days, clock_origin, producing_step, adopted_rule_revision)`.**
      ***Same lineage as `clock_origin` (`0102`) and `producing_step` (`0111` E2): a setting under which
      the measurement was taken that was invisible in the key.***
      ***AND THIS ONE HAS ALREADY BEEN OCCUPIED*** — **`processed/step5/adopted_rule.json` carried
      REVISION-3 figures against the approved REVISION-6 rule, and a Step 8 instance had to work around
      it** (`CLAUDE.md`, surface 8). **If a Step 5 or Step 7 amendment lands between Step 9's run and
      Step 13's, their entries at one setting are different measurements — and without this dimension
      `S2` calls the rerun a duplicate.**
      ***VERIFIED BEFORE RULING, not assumed: NO revision key exists anywhere in any of the three
      placeholders.*** **It is ABSENT, not carried incorrectly** — so this adds a dimension rather than
      correcting one.
- [ ] ***AN ARM ENTRY'S IDENTITY INCLUDES ITS PRODUCING STEP.*** Human Lead ruling, `0111` (E2).
      **The key is ~~`(W_days, clock_origin, producing_step)`~~.** ***SUPERSEDED — a FOURTH dimension was added at `0114` (E14): the key is `(W_days, clock_origin, producing_step, adopted_rule_revision)`. Marked at the point of use 2026-08-19 (`0116`), found by arm `a`: `0114`'s propagation ADDED the four-field key in new text and left the three-field statements standing — in three places BELOW their own replacement. `0113` §2's defect, one entry later, and invisible to `check_surfaces.py` because an arm key is a STRUCTURAL CLAIM, not a number or a registered phrase.*** ***Step 9's `W = 108` and Step 13's
      `W = 108` are DIFFERENT MEASUREMENTS OF ONE SETTING and both must exist as distinct entries.***
      **This is the `(W_days, clock_origin)` collision ONE DIMENSION OUT, and it takes the same fix —
      ADD THE MISSING IDENTITY DIMENSION.** ***It must NOT be resolved by restricting which step may
      occupy a shared `W` value***: the grid contains 91 and 108, Step 9 publishes headlines there, and
      Step 13 computes a headline at every grid arm. **Four payloads, two slots, was the symptom; the
      missing dimension is the cause.**
- [ ] ***STEP 13'S SIX NON-HEADLINE OUTPUTS TAKE PER-ARM NESTING, THE SAME SHAPE AS ITS HEADLINE.***
      Human Lead ruling, `0111` (E1). **`d3_prime`, `tested_ranges`, `conclusions_surviving`,
      `conclusions_not_surviving`, `d2_recomputed_inside_this_arm` and `action_type_counts` each had
      ONE SLOT where TWO ARMS write.** ***One slot where two arms write forces the reconciliation
      `0107` §3 forbids*** — the merge would have to drop an arm or reconcile.
      ***THIS IS THE THIRD APPEARANCE OF ONE DEFECT***, after `0107` §4 (a dual step's arm file had no
      legal shape) and `0109` (§1's duplication). **The fix is the same WIDENING both prior instances
      took, because widening keeps ONE DEFINITION PER FIGURE.**
- [ ] **Emit a placeholder file with illustrative values and the IDENTICAL schema**, so Step 16 can be ***— THREE PLACEHOLDERS, ONE PER DOCUMENT ROLE, amended by `0110` (M4/M9): the MERGED document, a DUAL step's ARM FILE, and a SINGLE-ARM step's SOLE FILE.*** **`0109` fixed granularity at one file per step per arm, which makes three distinct legal shapes**, and **a role with no placeholder is a shape Step 16 would be built without** — the same reason the spec required one in the first place. **The arm emitted all three and correctly did NOT amend its own spec to match; that is this entry's job.**
      built before results exist. **The placeholder must be unmistakable as one** — a top-level flag a
      consumer cannot miss, and values that cannot be mistaken for measurements. **A placeholder that
      reads as data is the failure mode**, and this study has spent seven entries on figures that were
      superseded and looked current.
- [ ] **Steps 9 through 13 write into this schema DIRECTLY. No conversion layer.** That is the point of
      the step: a conversion layer is a second definition of every figure, and **two definitions of one
      figure is the defect this study has hit most often** (`0058`, `0061`, `0062`).
- [ ] ~~**The two arms of a dual step write the same schema and are diffed in it.**~~ ***FIRST CLAUSE
      RETIRED by `0107` (E2): the two arms write the SAME SCHEMA but NOT THE SAME FILE. A dual step is
      DIFFED BETWEEN TWO ARM FILES, BY THE HUMAN LEAD, BEFORE THE MERGE — not inside one file, which
      had no writer. SIXTH assertive surface, found by arm `a` on the rerun; `0107` §5 found five and
      named four. It is this step's own spec bullet, and the arm correctly declined to edit it —
      propagating a ruling into its own spec is not an arm's to do.*** **The SECOND clause stands and
      is unaffected**: one slot per figure would force a reconciliation the spec forbids **in the
      MERGED document**. Step 9 is dual, so the
      schema must hold **both arms' values for a figure where the arms legitimately differ** — the
      **bound ÷ sampling width ratios use two conventions and are REPORTED, NOT RECONCILED** (`0058`,
      `0063`). **A schema with one slot per figure would force a reconciliation the spec forbids.**
- [ ] **The bootstrap is unspecified and Step 9's CIs are not diffable until it is fixed** — `B`, seed
      and levels-vs-movements all differ between the arms. The schema must **record which bootstrap
      settings produced each CI**, so an unfixed spec is visible in the output rather than silent.

**Deliver:** schema definition, **three placeholder files — merged, arm-file, sole-file** (`0110`).

**Review:** Engineering, on whether Steps 9 through 13 can write into it without restructuring their
outputs.

## Step 9: Headline result

**Owner:** Data Scientist, dual implementation
**Mode:** Chained

- [ ] Of users who completed S1, compute the share who never started S2
- [ ] Compute the share who started and left
- [ ] Compute the share who continued
- [ ] **THE BOOTSTRAP IS FIXED: 10,000 RESAMPLES, RESAMPLED AT THE ACCOUNT LEVEL, SEED 20260818.**
      Human Lead ruling, 2026-08-18 (`0103`), closing the gap `0056` left open and **unblocking Step 9**,
      which `reviewer-engineering` found could not write **anything at all** while `ci.bootstrap_ref` was
      required against an unspecified bootstrap.
      **EVERY INTERVAL RECORDS ITS SEED, ITS RESAMPLE COUNT AND ITS RESAMPLING UNIT, at the point of
      use** — *"so an unfixed spec is visible in the output rather than silent."*
      **ACCOUNT LEVEL, because pairs are not independent — one account contributes many — and pair-level
      resampling understates the interval.** **This build has measured that clustering, and the
      measurements are on the record**: Step 7's threshold interval is **account-clustered [528, 787]**
      against an **i.i.d. [632, 645]** that *"overstates precision by roughly twentyfold"* (`0039`).
      **THE FIXED SEED IS WHAT MAKES THE TWO ARMS COMPARABLE** — without it, a difference between them
      could be **sampling noise rather than a divergence**, and this study's entire dual control rests on
      that distinction.
      ***THE SEED VALUE ITSELF IS ARBITRARY AND ITS FIXITY IS THE POINT.*** `20260818` is set here so the
      spec states one; **change it freely, but never leave it unstated.**
      ***AND ONE CAUTION THAT IS NOT A DISAGREEMENT: THE BINDING CLUSTER IS NOT THE SAME FOR EVERY
      QUANTITY.*** **`W`'s interval is SHOW-clustered** — 25,120 C1 pairs from only **206 shows**, and
      **`task-sheet.md` names the SHOW as the binding cluster there**: i.i.d. ±8 days, show-clustered
      [89, 125], ±18 days (`0024`, `0026`). **So account-level resampling is right for the outcome
      shares, whose clustering is by account, and would UNDERSTATE a show-bound quantity.** **The
      per-interval `resampling_unit` field this ruling mandates is exactly what makes that visible** — a
      quantity whose binding cluster is the show must say `show`, not inherit `account` silently.
      **Report any interval where the two units disagree materially; do not reconcile it.**
- [ ] **STEP 13 IS DUAL** (`0103`), resolving the conflict between `CLAUDE.md`'s dual list, which omitted
      it, and this file's own argument that the `W` grid must be fixed because **two instances on
      different grids produce tables that cannot be diffed at all** — which presupposed the duality.
      **Found by `reviewer-engineering` on the Step 8b review.** **Ruled dual:** Step 13 varies `W`
      across eight arms **and the completion rule alongside**, making it **the most spec-heavy step
      remaining**, and **every divergence in this build has come from an unstated convention in a spec
      rather than a coding error.**
- [ ] **ATTACH CONFIDENCE INTERVALS — AND THE BOOTSTRAP IS UNSPECIFIED. THIS BLOCKS STEP 9, NOT STEP 8.** Human Lead ruling, 2026-08-13 (`0056`). **The two Step 7 arms diverged on all three of `B`, seed and statistic** — **A: B = 4,000, seed 20260813, on the movements; B: B = 2,000, seed 20260814, on the levels** — and a dual step whose CIs are built three different ways **produces a divergence that proves nothing.** **`0052` §6 recorded this as "unreconciled and now specified." It was never specified: the string "bootstrap" appears ZERO times in `task-sheet.md`, `CLAUDE.md` and all four pipeline agent files.** That claim is **struck in place** — it is a completed action asserted and not taken, the same class as `0055` §5a. **Specify all three before Step 9 launches**: the resampling unit is the **account** (clustered, per `0044`), and `B`, the seed and whether the interval is on levels or on movements must be fixed **identically for both arms** in this file. **Until they are, Step 9's CIs are not diffable.**
- [ ] ~~**TEST WHETHER THE HEADLINE IS SENSITIVE ACROSS THE LIVENESS THRESHOLD'S CLUSTERED INTERVAL.**~~ **DISCHARGED and WITHDRAWN 2026-08-13 (`decisions/0046`).** The test was run, the headline was insensitive — 0.026 / 0.038 / 0.012 pp across 787 / 1,293 / 2,200 days — **and the threshold was deleted at `0042`. There is no interval to test across.**
- [ ] **Compute the never-started bound over the liveness exclusions scored NEVER STARTED. On APPLY: [16.6633%, 16.9704%], width 0.3071 pp, BOTH ENDPOINTS ON 196,654.** The ceiling equals the unfiltered share **as an identity**; both endpoints are attainable. **The 99 started-and-left exclusions enter neither endpoint, so this bound is IDENTICAL under ALT and ALT-BROAD.**
      **Why the never-started floor is NOT widened, although 207 channel pairs are never-started** (`0056`, from `0021` and instance B). **The 207 are retained pairs, ¬Continued, scored never-started, whose last insertion falls inside `(τ1, τ2)`** — the same dormancy channel whose started-and-left arm forced the S&L floor down to 18,952. **They do not widen this bound, and the reason is the anchoring, not the count.** Never-started is the null `|A| = 0`, **read at `τ1`**, and **every one of the 207 has an insertion after `τ1`** — which is exactly what gate `0021` licenses: *an insertion after the window closed proves the account was alive.* **Their null is observed, not conceded.** The 90 differ because the **Continued** condition they negate is read at **`τ2`**, and they are dormant before it. **State this where the bound is published**; without it a reader who has seen the S&L widening will reopen this one. (DERIV's channel never-started component is **3**, and the same warrant applies.)
      **Superseded, and the record keeps them:** `0046` published **[16.7146%, 16.9704%]** — floor on 196,050, ceiling on 196,654, **mixed denominators**, and its floor sat **0.0513 pp above** the case liveness guards against. `0045` published **[16.7789%, 17.0355%]** for PF-LIMIT with the same defect. **Three consecutive bounds had an endpoint that did not cover the case the filter exists for** (`0047` §3); the standing rule is that **an endpoint states the population it is computed on and the estimand it bounds, and they must be the same population.**
- [ ] **Compute a SECOND bound, on the started-and-left share, over ALL exclusions AND WIDENED TO COVER THE CHANNEL PAIRS — ON BOTH POPULATIONS.** Human Lead ruling, 2026-08-13 (`decisions/0054`; **DERIV widened by `decisions/0055`**). **EVERY ENDPOINT STATES ITS POPULATION AT THE POINT OF USE, and APPLY and DERIV are published side by side.**
      **On APPLY, n = 196,654, over all 703 exclusions: [9.6372%, 10.0405%], width 0.4032 pp** *(**0.4033 is instance B's rounding artifact**, differenced from rounded endpoints; `793 / 196,654 = 0.40325`. Withdrawn by `0055` §5 — `0054` published it four paragraphs after withdrawing another of B's.)* — floor `18,952 / 196,654`, ceiling `19,745 / 196,654`.
      **On DERIV, n = 147,370, over all 99 exclusions: [11.3015%, 11.4291%], width 0.1276 pp** — floor `16,655 / 147,370`, ceiling `16,843 / 147,370`.
      **Why the floor is widened, and it is widened on BOTH.** The retained pairs that are ¬Continued, live only because they inserted after `τ1`, and whose last insertion falls inside `(τ1, τ2)` — **90 on APPLY, 89 on DERIV** — **could not produce evidence dated after that instant**, so they may in truth be Continued. **The floor must admit that.** On APPLY 18,952 / 196,654 = **9.6372%** is what does — **18,952, not 19,042**; on DERIV **16,655 = 16,744 − 89**, giving **11.3015%**. `0049`'s **[9.6830%, 10.0405%]** did not, and `0052` §4 declined to widen it on the ground that doing so *"would have been the fifth consecutive bound with a non-covering endpoint"* — **exactly backwards: widening is what makes it covering.**
      **The widening is ONE-SIDED: the ceiling does not move on either population**, because the channel pairs are already counted as started-and-left in it. The ground is **admissibility, not plausibility** (`0055` §2) — a floor is a worst case, so no margin statistic enters it, and **p5 = 1.7 days and median = 44.5 days are both inadmissible here.**
      ***SUPERSEDED, named here so it cannot be read as current (`0055` §1): the DERIV floor 16,744 → 11.3619% and the DERIV width 0.0672 pp.*** They were `0054`'s un-widened DERIV figures, left behind when APPLY was widened. **A Step 9 instance publishing them publishes a floor 0.0604 pp ABOVE the case the filter exists to guard against.**
      **THE BOUND'S SCOPE, AND IT PUBLISHES WITH THE BOUND.** Human Lead ruling, 2026-08-13 (`0062`), from instance A and sharpened by Red Team. **The bound is covering with respect to INSERTION-DORMANCY, exhaustively; open only across CHANNEL CLASSES (D4, D9).** The widening rule is one line: **concede every pair that was dormant before the instant at which its own state-defining null is read** — `τ1` for the never-started null, `τ2` for the Continued null. **That is exhaustive, not open-ended**: every pair either was inserting through its test instant or was not, and it yields `33,373 − 604 = 32,769` and `19,141 − 189 = 18,952` **with no residue.** **So "covering" is not a claim without a stopping rule** — it has one, and the honest statement is narrower *and* stronger than "covering with respect to the identified channels." **D4 and D9 publish ALONGSIDE this bound and are not folded into it.** State this wherever the bound is published.
      **Report [9.6372%, 9.7333%], width 0.0961 pp, only as a labelled conditional sub-interval** — that is an **APPLY** figure, never the bound. **The conditioning constrains the 604 and says nothing about the 90**, so **the sub-interval floor moves with the bound floor and its width is 189 / 196,654, not 99 / 196,654.** ***SUPERSEDED (`0056`): [9.6830%, 9.7333%], width 0.0503 pp — correct only under the un-widened floor `0055` §1 withdrew. `9.6830` has NO legitimate reading under the adopted rule.*** `step7-liveness-mm-a.md:217` computed [9.6372%, 9.7333%] and warned in terms that Step 9 must not carry the old number. **On DERIV the bound and its conditional sub-interval COINCIDE**, because the never-started exclusion component is 0 there; say so where it is published.
      **The Continued ceiling moves in lockstep with the floor, on both populations: APPLY 144,933 / 196,654 = 73.6995%; DERIV 121,570 / 147,370 = 82.4930%.** ***SUPERSEDED (`0055` §1): the DERIV Continued ceiling 121,481 → 82.4327%.***
- [ ] **STATE THAT THE TWO CEILINGS CANNOT BOTH HOLD.** Human Lead ruling, 2026-08-13 (`decisions/0050`). **THERE ARE THREE CEILINGS, NOT TWO, AND NONE OF THEM CAN HOLD WITH THE OTHERS.** Never-started **16.9704%** (33,373), started-and-left **10.0405%** (19,745), **Continued 73.6995%** (144,140 + 703 + the 90) — **sum 100.7104% on 196,654.**
      **THOSE THREE ARE APPLY FIGURES. State the DERIV ceilings beside them, n = 147,370:** never-started **6.2055%**, started-and-left **11.4291%** (16,843), **Continued 82.4930%** (121,570) — the Continued ceiling **corrected by `0055` §1**, ***superseding 121,481 → 82.4327%***.
      **Continued HAS a ceiling** — `(144,140 + excluded) / 196,654` — **because any EXCLUDED pair may in truth be Continued.** The parenthetical "no Continued pair is ever excluded" is true and **does not license treating Continued as a point.**
      **Excess mechanism, refined (`0053` §4, retained):** each never-started exclusion appears in **all three** ceiling numerators — excess 2 each — and each started-and-left exclusion in **two** — excess 1 each. With the 90 admitted: **2 × 604 + 189 = 1,397 pairs = 0.7104 pp.** State the mechanism, not just the total.
      **The DERIV sum, which the record did not state anywhere** (instance A): 6.2055% + 11.4291% + 82.4930% = **100.1276% on 147,370**, excess **0.1276 pp = 188 pairs = 99 + 89.** **The excess equals the bound width on DERIV**, because the never-started exclusion component is 0 there, so each of the 188 is double-counted exactly once rather than some twice and some three times. **That coincidence is DERIV-only and must not be carried to APPLY**, where 604 never-started exclusions make excess (0.7104 pp) and width (0.4032 pp) different quantities.
      *(**73.6537% is itself SUPERSEDED by 73.6995% (`0054`); the exchange below is the record of an earlier error, not a live figure.** `0051` §2 called 73.6537% "on no population" and replaced it with Continued's point 73.2962%. **That was wrong** — 73.6537% is the Continued ceiling, both arms publish it, and `0052` §2 restores it. A Step 9 instance reading the corrected line would have deleted a number its own deliverable prints.)* **They are alternative worst cases over the same 604 pairs, not simultaneous ones**, and printing two upper ends unlabelled is the misreading the whole bound exercise exists to prevent. Instance B: *"both consume the same 604 pairs — and the write-up must say so rather than printing two ceilings that add up to more than the population."*
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

- [ ] **THE `W` ARM GRID IS 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 DAYS, AND THIS IS THE FIRST FILE
      TO SAY SO.** Human Lead ruling, 2026-08-13 (`0075`). **The grid has never existed in any file.**
      Step 6's deliverables state `[37, 107]` and `[37.70, 107.71]` and **neither says 38**; the bullets
      below constrain the arms without enumerating them; and the grid has travelled only as the INDEX of
      a reported series — *"537 / 550 / … at `W` = 38 / 46 / …"* — which is a reading, not a
      specification. **Instance A chose it and named the choice, which means the next instance may
      choose differently.** **Every Step 13 figure is indexed by the arm set, so two instances on
      different grids produce tables that CANNOT BE DIFFED AT ALL** — a failure of the dual
      implementation itself rather than a wrong number inside it. **Take the eight values above.**
- [ ] Vary W above and below the derived value of **`W = 108`** (`decisions/0026-step6-window-w-gate.md`; the Step 6 artifacts state 107 and 107.7135 and **neither is the adopted value**). **Cover at least the range Step 6 reports** — the same percentile read on the C1 curve and on the all-shows curve. That gap is the size of the transfer assumption D14 accepted, so it is the range that tests it.
- [ ] **The W arms must also span 46 to 107 days.** Human Lead decision, 2026-08-12 (`decisions/0024-w-is-the-90th-percentile.md`). Those are the two values two isolated instances produced from the undefined "flattens" criterion before it was replaced by a fixed percentile. **The definition is now unambiguous, but the sensitivity of the result to it is not thereby known**, and 46 to 107 is the measured size of that reading. This range composes with the C1-versus-all-shows range above: **cover the union of the two, not whichever is wider.**
- [ ] **The W arms must also extend ABOVE the adopted `W`, with arms at 150 and 213 days.** Human Lead decision, 2026-08-12 (`decisions/0027-step13-w-arms-above-the-adopted-value.md`). **213 is the 90th percentile among C1 pairs with 8 or more years of exposure** — the direction the right-censoring diagnostic runs, and an upper bound rather than a rival estimate, since exposure and cohort are not separable on this data. Every other mandated range tops out at or below the adopted `W = 108`, so without these two arms **the sensitivity would not test the one direction the known bias points.** 150 sits between the adopted value and the bound so the response is not read off two endpoints alone. Direction, stated so the arms are interpretable: a larger `W` admits later starters and moves the never-started share **down**.
- [ ] **Report the retained-row count for every W arm.** The right-censoring rule contains W, so each arm re-censors the population and the arms do NOT share a denominator.
- [ ] **Hold `H` constant across every arm that varies W.** Otherwise **D3′** and D8 are not comparable between arms. (D3 was replaced by D3′ at `decisions/0034`; the requirement is unchanged and now governs D3′.)
- [ ] ~~**Vary the liveness threshold — and REFIT IT PER `W` ARM.**~~ **WITHDRAWN 2026-08-13 (`decisions/0044`), and `0038` §6's refit requirement is withdrawn with it. THERE IS NO THRESHOLD TO VARY OR REFIT** — `0042` deleted it. This item had no referent and a data-scientist instance would have tried to execute it.
- [ ] **REPORT THE LIVENESS EXCLUSION COUNT PER `W` ARM.** Human Lead ruling, 2026-08-13 (`decisions/0044`). **The rule has no parameter of its own, but it is fully determined by `W`:** its exclusion set **is** the open-ended bucket, and that bucket is a pure function of `W` — **On APPLY — the population Step 13 runs on — 833 at `W = 38` to 1,670 at 213, a factor of 2.0** (`0046`). *(The 348 → 949 figures first recorded here were **DERIV** and are superseded for this purpose; they remain correct on DERIV.)* **Report the ALT-BROAD exclusion count per arm on APPLY: 537 / 550 / 633 / 664 / 701 / 703 / 789 / 864 at `W` = 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 — a factor of 1.61.** Report the **started-and-left component separately: 52 / 56 / 79 / 89 / 98 / 99 / 125 / 148, a factor of 2.85**, which grows faster than the rule itself. *(ALT's 485 → 716 series is superseded and must not be ordered.)* Report the count at every arm so the coupling is visible. **`W` and liveness are not independent axes and never were** — deleting the threshold made the coupling total rather than removing it.
- [ ] Vary the S1 completion rule at 100 percent and at 90 percent. **That is the threshold, not the date definition — the two arms below are separate and neither is covered by it**
- [ ] **Arm: S1 completion DATE as last-observed rather than first-pass**, per Step 1 §5. Required by Step 1 §9, and it does more than test a choice: **recompute D2 inside this arm.** D2 on the operative first-pass clock cannot see the rewatch artifact the Step 1 §5 addendum documents — a rewatch cannot move a first-pass clock start, so the primary D2 count will read zero for that failure mode, and **a zero there is not evidence it is rare.** This arm is the only place its frequency is measurable
- [ ] **Arm: `action`-type, excluding `checkin`-only and manual-`watch`-only evidence**, per Step 1 §2.3. ~~Requires the `action` column retained at Step 8.~~ ***SUPERSEDED by `0070` ruling 4, propagated here by `0073`.*** **Step 8 emits PER-PAIR COUNTS BY ACTION TYPE, not a row-level `action` column** — `action` is record-level and the Step 8 row is a pair, so one value per row would assert one action per pair, which is false. **This arm reads the counts**: a pair is `checkin`-only iff its `checkin` count is positive and its `scrobble` and `watch` counts are zero, and manual-`watch`-only likewise. **The arm is unchanged; only what it reads is.** Exists because Step 1 made a permissive choice and the permissiveness should be shown not to be load-bearing
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
- [ ] **2. Liveness exclusion — UP, not DOWN. SIGN CORRECTED 2026-08-13 (`decisions/0043`).** ~~Excluding pairs that fail the liveness test removes accounts that stopped logging, which are disproportionately the ones that would have scored never-started. Compounds with 1 rather than offsetting it.~~ **That was the reasoning, and it is measured false for the approved rule on this study's own data.** Applying liveness moves the never-started share **UP on DERIV — 6.2055% → 6.2096%, +0.0042 pp under ALT-BROAD.** *(**6.2373% / 0.032 pp** are PF-LIMIT's. This bullet's own closing sentence already forbids restating them, and it restated them four lines above. Corrected by `0055`, propagation #17.)*
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
- [ ] ~~**ALT-MATCHED closes the construction channel and pays for it in residual fragility.**~~ **WITHDRAWN 2026-08-13 (`decisions/0054`): the rule is REVERTED and `0053` is withdrawn entirely, so this limitation does not attach to the adopted rule.** **What survives, and publishes, is the measurement itself** (instance B): **the 90 APPLY / 89 DERIV channel pairs are by construction the ones closest to their own boundary — margin bounded above by `H` = 91 days, median 44.5 days against the 604's 202.5.** **Under ALT-BROAD those 90 are RETAINED and scored started-and-left**, and the **widened floor** is what carries the possibility that they are in truth Continued. The ±7-day residual figures **−6.3% / +14.8%** are ALT-MATCHED's; **ALT-BROAD's are −5.1% / +5.1%** and are the ones that publish.
- [ ] ~~**D10 admits `τ2 = τ_pull`, so some pairs have a zero-length post-`τ2` observation window** — 20 APPLY pairs, 2 excluded by construction.~~ **WITHDRAWN 2026-08-13 (`decisions/0054`): FALSE under the restored rule.** The silence test is anchored at **`τ1`**, and D10 requires `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`, so **`τ1 ≤ τ_pull − 91 days` for every surviving pair and the post-`τ1` observation window is never zero-length.** The finding was real for ALT-MATCHED, which read silence at `τ2`; it does not transfer. (Originally `0053`, instance A.)
- [ ] **Step 9's bounds and Step 9's published shares are on DIFFERENT POPULATIONS, and on one of them the point estimate falls outside its own bound.** Human Lead ruling, 2026-08-13 (`decisions/0052`). The bounds are computed on the **position-5** population (196,654 APPLY / 147,370 DERIV); **the published shares are post-liveness** (195,951 / 147,271). **On APPLY containment holds by arithmetic accident.** **On DERIV it fails outright: the published never-started share is 6.2096% and the published bound is [6.2055%, 6.2055%] — the point estimate lies OUTSIDE its own identified set.** Both arms printed these within two pages of each other and neither said they were on different populations. **State which population each bound bounds at the point of publication.** `0047` §3 fixed endpoint-versus-endpoint and left estimand-versus-headline open; this closes it as a stated limitation, not a repair.
- [ ] **The liveness rule's insertion clock carries a calibration residual, discharged at `W = 108` only.** Human Lead ruling, 2026-08-13 (`decisions/0050`), routed here because **recording a limit only in `decisions/` is not recording it.** **22.68%** of dated records (6,271,584 of 27,656,434) claim a `watched_at` **later than their own calibrated insertion instant**, and the rule's first conjunct **is** a comparison between an interpolated instant and `τ1`. **Clamping IS inert under the adopted `τ1`-only test — the clamp value 2026-08-10T20:48Z postdates every D10-surviving `τ1`, so no excluded pair sits on a clamped account, both arms.** *(`0053` recorded that clamping is NOT inert at `τ2` — 1 excluded pair — and ruled the old form must not be restated. **Withdrawn with ALT-MATCHED by `0054`: at `τ1` the old form IS the correct one.** It becomes live again only if a silence test is ever re-anchored later than `τ1`.)* **The exclusion set is stable at the residual covering ~91% of records** (703 → [701, 703]) **and not stable in the tail** (±125 d → [414, 1284]); under a direction-only correction **700 of 703 survive and none is created.** **The started-and-left component is the fragile one:** median margin **81.3 days** against 202.5 for never-started, spanning **19×** under tail residual against 2.5×, with **525 of 703 on accounts whose last record is a `watch`, where the residual is not directly measurable.** **All stability figures are `W = 108` only; Step 13 runs to `W = 213`, where the exclusion set is 864 and the started-and-left component 148.**
- [ ] **The commutation check shows the two filter orders agree on OBSERVED COUNTS. It does not show the estimand is unaffected.** Human Lead ruling, 2026-08-13 (`0058`), from Red Team's eleventh review. **Conjunct 2 of the liveness rule is `NOT Continued`, so liveness is OUTCOME-CONDITIONAL** — the artifact flags this itself at `position_6_label` and `0046` made waterfall line 6 outcome-conditional in the spec. **`ordering_commutation_check` demonstrates that `|A|` and liveness are row-local predicates that commute index-for-index on this data.** That is a statement about **counts on the observed sample**, and it is what both arms verified. **It is NOT a demonstration that conditioning the filter on the outcome leaves the estimand unchanged**, which is a different claim and is not tested anywhere in this study. **The bound construction is designed to absorb it** — every excluded pair is allowed to be in any state at the relevant endpoint — and `0046`, `0048` and `0054` argued that through. **Red Team would not hold on it and neither would I; it publishes as a limitation, not as a resolved question.**
- [ ] ~~**The two Step 8 instances examined different numbers of records under the set-membership rule —
      6,065,704 against 6,065,610, 94 apart — and BOTH reported 0 drops.** Reported unreconciled and
      routed here.~~ ***CLOSED 2026-08-16 (`0083` §1). IT IS NOT A STEP 14 LIMITATION and does not
      publish as one*** — a limitation is an uncertainty that **survives into a result**, and this one
      touches none: **the rule dropped ZERO records under every reading**, so the numerator is 0 three
      times over and nothing downstream reads the denominator. **It was never a divergence.** The two
      figures are two points on a **one-parameter family indexed by where D11 applies**: D11 discards
      **167** in-frame S1/S2 records dated at or after `τ_pull`, splitting **94 on the S2 side and 73 on
      the S1 side**, which is the whole of the gap. **Reading A — D11 nowhere — 6,065,704, line 1
      220,107** (instance A). **Reading B — D11 on the S2 side only, the S1 side carried at `0068`'s
      published line 1 — 6,065,610, line 1 220,107** (instance B). **Reading C — D11 on both sides —
      6,065,537, line 1 220,103.** **All three drop 0.** **The other candidate axes are all zero on both
      arms**: undated records, exact duplicate `(user, play id)` records, non-positive `number`.
      **`0074`'s "publish both numbers, not one" stands and is strengthened to THREE, each with its
      pipeline named at the point of use** — as a coverage figure, not an open question. **What stays
      open is NOT this: whether D11 applies to the S1 completion walk is `0068`'s own open item**, where
      reading C moves line 1 to 220,103 because **4 pairs stop being completers and 0 completion dates
      move.** **Choosing between B and C is answered there, not here** — recording it twice is how a
      ruling diverges from itself.
- [ ] **THE ASSERTION SET PROVES THE CODE, NOT THE RULE, AND THE INVARIANT REPORT MUST SAY SO.** Human Lead ruling, 2026-08-13 (`0070`), **restated by `0076` after the `p` label was corrected.** ***SUPERSEDED: "four of six cannot fail on any data."*** **On the post-`0074` set of six the true figure was FIVE OF SIX, WITH ZERO PURE DATA CHECKS** — the only assertion with force was the clock-start equality, and only via the independent recomputation. **That is why `0076` adds two genuine data checks.** **The set is now NINE: SIX pure code checks, one code-by-construction with force only as specified, and TWO that can fail on real data — added because the set had none.** **A report stating that all invariants passed overstates what was verified unless it names which ones COULD have failed.** The outcome partition, the monotone filter counts, distinct-episodes-vs-season-length and `A ⊆ A_H` are **code checks**: each is true by construction and can only catch an implementation that computed something wrongly. The clock-start check is a **code check by construction and a real cross-check only because the first-pass S1 completion date must be recomputed INDEPENDENTLY** — read back rather than recomputed it proves nothing. And the 703 expectation is **not an invariant at all** but a population reconciliation. **An unlabelled code check reads as evidence FOR THE RULE when it is only evidence that the code computed what it was told to** — and this study's invariant set is four-sixths of that. **Publish the labels with the results, not the count alone.** *(The two read-back instances split 4-of-6 against 6-of-6 on this, and both readings were defensible because the spec had labelled exactly one — `0069`.)*
- [ ] **The propagation failure count is a FIVE-SURFACE count, and the two surfaces it omits are now measured and non-zero.** Human Lead ruling, 2026-08-13 (`0057`), from `second-brain`'s U2. **All eighteen failures numbered #1–#18 were found on surfaces 1–5** — `task-sheet.md` and the four pipeline agent files — because those were the only surfaces checked. **`artifacts/` and `.claude/agent-memory/second-brain/` were added as surfaces 6 and 7 AFTER the count was fixed**, and the failure rate on them was recorded as *"unmeasured, not zero."* **It is now measured and non-zero at three:** **#19**, the `bb-{a,b}` stamp that certified superseded figures, found **inside the fix added for surface 6**; **#20**, both `.json` halves left carrying the first stamp and the withdrawn bound floor while the `.md` halves were corrected; and **#21**, `open-items-and-contradictions.md` blessing the superseded sub-interval with a ✓ one line from the corrected bound, because a propagation was scoped to one file and reported as a surface. **The count is NOT renumbered — 18 is a true count of surfaces 1–5 — but it must never be published as a total**, which is exactly how it reads without this bullet.
- [ ] **The liveness rule is a biconditional and `0021` licenses only one direction.** `0021` establishes *insertion after `τ1` ⟹ live* — a **sufficient** condition. The rule also asserts the converse: *no insertion after `τ1` ∧ ¬Continued ⟹ not live*. **ALT-BROAD narrows where that assertion is made, from PF-LIMIT's 1,355 pairs to 703. It does not justify it.** Both arms and Red Team left this open across five reviews; it is recorded as a limitation rather than closed. (`decisions/0048` §9, `0050`)
- [ ] **ALT-BROAD leaves 297 pairs in the channel its own warrant describes.** The warrant is that a pair silent after `τ1` can produce no evidence in `[τ1, τ2)` and is scored "left" by construction — **but that holds identically for a pair silent after `τ1 + ε` for any ε < 91 days.** Measured: **297 pairs on APPLY are ¬Continued, live only because they inserted after `τ1`, and had their last insertion inside `(τ1, τ2)`** — **207 never-started and 90 started-and-left**. **The channel figure is 52.4%, not 70.3%** (`0052` §3, routed here by `0055`): 70.3% pooled two categories with different coverage. **The 207 never-started pairs are NOT in the gap** — never-started is the null `|A| = 0` read at **`τ1`**, and every one of the 207 has an insertion after `τ1`, which is exactly what `0021` licenses. **On the implicated set alone ALT-BROAD closes 99 of 189 — 52.4%, leaving 47.6% open.** **The remaining 90 are NO LONGER treated as observed:** the started-and-left floor is widened to admit they may in truth be Continued (`0054`), which is a **stated bound, not a closure** — the pairs stay in the sample and the uncertainty is carried in the endpoint. (`decisions/0050`)
- [ ] **The liveness filter moves the result very little, and Step 9's bounds rest on it.** **CORRECTED 2026-08-13 (`decisions/0049`) — this bullet quoted ALT's movements under an ALT-BROAD heading.** Measured under **ALT-BROAD on APPLY**: **−0.2474 / +0.2630 / −0.0156 pp**, from **703 exclusions of 196,654, 216 accounts**; on **DERIV**, **+0.0042 / +0.0554 / −0.0595 pp** from 99 exclusions of 147,370, 73 accounts. **The superseded figures must not be restated:** ALT's −0.2558 / +0.2258 / +0.0300, and PF-LIMIT's 0.032 / 0.023 / 0.009 on 751 of 147,370. **The "0.05 pp" previously written here was the width of a conditional interval, not a share movement.** Step 9's bounds are computed on these sets, so **they are narrow because the filter is small, not because the inference is tight.**
- [ ] ~~**Step 7's liveness threshold is derived on a narrower population than it is applied to.**~~ **MOOT under the adopted rule (`decisions/0046`).** ALT is **definitional, not derived** — nothing is fitted on one population and applied to another, so the 1.4418%-against-1% mismatch cannot arise. **What replaces it as the limitation, corrected 2026-08-13 (`0048`): under ALT-BROAD the exclusion set is 99 on DERIV and 703 on APPLY, so Step 7's dual run exercises the rule on BOTH populations** — the DERIV diff is **99 against 99 on 73 accounts** rather than the `0 = 0` it was under ALT. **What the gate still cannot establish** is that Step 8's position-6 population is the one Step 7 reconstructed: both arms build APPLY from the Step 5 pair table, not through Step 8's positions 1–5.
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
- [ ] **Censoring is cohort-asymmetric, and it removes the users least like the ones it leaves.** The loss falls entirely on the uncapped `S1_completion_date` term. At the Step 13 arm of `W = 213` the **2023–2025 cohort loses 10.5% of its pairs against 3.0% for pre-2020** — **BOTH figures on the mandated order. 10.5% corrected from `0030`'s 10.3% by `0070`, and 3.0% corrected from its comparator 2.7% by `0073`**, which `0070` moved the first figure and left on the superseded order — **one sentence, two orders**, found independently by both Step 8 instances, which was measured on the position-3 output rather than the position-4 output Step 8's mandated filter order requires. The survivors from recent titles are those who completed S1 early — early adopters, who are the users **likeliest to continue** — so the modern cohort is not merely smaller but differently selected. **The `W = 213` arm added to test the censoring bias is itself the most censored arm.** (`decisions/0027`, `decisions/0030`)
- [ ] **The study rests on a stopped pull.** 2,549 users of 4,050 planned, **62.9%**. The stop is proportional across all ten strata to within 6.1 points, so it is not an arbitrary prefix — but it is still a subsample, and every count in the study recomputes if the pull resumes. (`decisions/0009`, `artifacts/s1-completer-diagnostic.md` §1)

**Deliver:** limits section in `artifacts/`, placed up front in the write-up and not buried
**Review:** Reviewer: Consumer Insights. Verdict on whether the population is defensible.

---

## Step 13b: Merged results document

**Owner:** Human Lead
**Mode:** Chained
**Review:** Engineering

***CREATED BY `0107`, the E2 ruling. MOVED AFTER STEP 14 by `0109` (M3), and its INPUTS FIXED AT
SEVEN by `0109` (M4/M5/M9).*** **Step 8b's schema said *"a dual step is diffed IN this
schema."* ***That claim had no writer and is RETIRED***: `dual_status: dual` requires both `arms.a` and
`arms.b`, and **two instances that never see each other's work cannot jointly produce one document** —
while **no arm may be the merge writer without defeating what dual implementation exists to do.**
**Arm isolation is the MECHANISM, not a side effect.**

- [ ] **ONE FILE PER ARM, everywhere upstream.** **Each arm writes its own document, and NO ARM WRITES
      INTO A DOCUMENT ANOTHER ARM WRITES INTO.** **This step is the only writer that reads both arms,
      and it is the only writer permitted to.**
- [ ] ***IT SITS AFTER STEP 14, NOT AFTER STEP 13.*** ***MOVED by `0109` (M3):*** **`S29` requires the
      merged document to publish `limitations`, and STEP 14 WRITES THAT BLOCK.** At the old position the
      only passing shape was **`limitations: []`** — **indistinguishable from *there are no limitations*,
      in the block carrying the ten-item bias ledger that MUST NOT BE NETTED, in the file Step 16
      renders from.** ***That is a FALSE STATEMENT TO THE READER, not a placeholder.*** **And it does
      NOT rerun after Step 14** — **two versions of one merged document is the stale-figure problem.**
      ***Verified before the move: Step 14 needs NO merged document*** — it is Human-Lead-owned, its
      bias ledger is sourced from `decisions/` and Step 9's bounds, and it references `13b` zero times.
      **It cannot run earlier than every writing step either.** **It has nothing to merge until
      every writing step has landed.** **It is NOT a gate** — `CLAUDE.md` fixes the gate list at five
      and **all five are approved.**
- [ ] ***INPUTS ARE SOURCES, NOT ONLY ARM FILES.*** Human Lead ruling, `0111` (E6): **the merge's
      input list records SOURCES.** ***Step 14's `limitations` is a NAMED NON-ARM-FILE SOURCE with
      its own provenance entry*** — it is an **eighth** source, it has **no arm**, and `0109` moved
      Step 13b after Step 14 precisely so it could be filled. **A ten-item bias ledger that MUST NOT
      BE NETTED cannot arrive in the reader-facing document with no recorded provenance.**
- [ ] ***THE MERGE TAKES NINE SOURCES.*** ***CORRECTED `0117`, found by `reviewer-engineering`: this
      section said SEVEN, corrected itself to EIGHT nineteen lines lower, and the anchor requires
      NINE.*** **Seven ARM FILES, plus Step 14's `limitations`, plus STEP 8's ARTIFACT — which
      `0114` E8 made a declared merge source when it moved `channel_classes` and
      `discovery_channel_overlap` out of the arm files.** ***`0114` E8 reached the Step 8b section of
      this file and NOT this one, the CONSUMER's*** — **so a Human Lead building the merge from this
      spec would declare eight and fail `S30` leg (f) on the first run.**
- [ ] ***AND THE BLOCKS ONLY THE MERGE MAY FILL ARE FOUR, NOT TWO*** (`0117`): `cross_arm_divergences`
      and `limitations`, **plus `channel_classes` and `discovery_channel_overlap`** (`0114` E8).
- [ ] ***SEVEN ARM FILES — ONE PER STEP PER ARM.*** Human Lead ruling, `0109` (M4/M5/M9),
      **resolving `0107`'s own §1-vs-§6 ambiguity in favour of §6.** **Step 9 writes TWO files, Step 13
      writes TWO, and Steps 10, 11 and 12 write ONE each.**
      ***Why §6 and not §1:*** **§1 would require Step 10's output to be DUPLICATED into two arm files —
      two copies of one figure, which is the defect class the no-conversion-layer rule exists to
      prevent.** **§6 requires a single-arm step's file to have a legal spine, which is a WIDENING —
      and every finding in this sequence has been fixed by widening, because widening keeps ONE
      DEFINITION PER FIGURE.** **The Human Lead has diffed the dual pairs BEFORE
      this step runs** — the diff is between two files, and **it is the diff, not the merge, that is
      the dual control.**
- [ ] **EMITS: ONE merged reader-facing document, AGAINST THE SAME SCHEMA**, carrying both arms'
      payloads under `arms.{a,b}` — **and the blocks only this step may fill**: `cross_arm_divergences`
      **with its real search record** (which an isolated arm is `forbidden_to_compute_here` and could
      only have fabricated), and `limitations` (`human_lead_only`).
- [ ] **STEP 16 RENDERS FROM THE MERGED DOCUMENT**, not from an arm file. **That is a cleaner input
      than a schema assembled by an unnamed party**, which is what the retired claim implied.
- [ ] **ENGINEERING REVIEW**, because this is **the last chance to catch a schema mismatch before Step
      16 renders from it.**
- [ ] ***WHAT SURVIVES FROM THE RETIRED CLAIM, UNCHANGED:*** where the two arms legitimately differ,
      **the MERGED document holds both** — the **bound ÷ sampling-width ratios use two conventions and
      are REPORTED, NOT RECONCILED** (`0058`, `0063`). ***One slot per figure would force a
      reconciliation the spec forbids — IN THE MERGED DOCUMENT. In a single arm's file it forces
      nothing, because there is no second arm's figure in it.*** **That is why E3 is closed by this
      ruling rather than fixed separately** (`0107` §3).

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
- [x] Step 5: contamination exclusion rule — **APPROVED by the Human Lead, 2026-08-12** (`decisions/0021`). *(An amendment at `0053` was withdrawn the same day by `0054`; the ruling stands as approved.)*
- [x] Step 6: window W — **APPROVED by the Human Lead, 2026-08-12 at `W = 108 days`** (`decisions/0026`)
- [x] Step 7: liveness rule — **APPROVED by the Human Lead, 2026-08-13** (`decisions/0064`; record at `artifacts/step7-gate-approval.md`). **ALT-BROAD, unconditional, residual published.**
- [ ] Step 8: analysis table — **the remaining gate**

Each is a question that will be asked out loud. If an agent decided it and the Human Lead did not, it cannot be answered.

---

## Dual implementation

Applies to Steps 6, 7, 8, and 9. Two instances in isolated context run the same written spec with no sight of each other. The Human Lead diffs the numbers. Any divergence is either a bug or an ambiguity in the spec, and both need to be known.

The two instances must receive byte-identical instructions. If the task is described twice in different words, a difference in their output proves nothing.
