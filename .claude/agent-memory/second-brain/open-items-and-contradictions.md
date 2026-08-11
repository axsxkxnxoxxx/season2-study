---
name: open-items-and-contradictions
description: Live register of open items and cross-step contradictions in the Season 2 study, each with its two conflicting sources named — re-verified 2026-08-11 after Step 3 completed, including three arithmetic contradictions inside the Step 3 artifacts themselves
metadata:
  type: project
---

# Open items and contradictions — re-verified 2026-08-11 (Step 3 complete)

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry names its two sources so the Human
Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it. Several close by
ordinary progress rather than by a decision — three did on 2026-08-10.

**The decision log of record is `decisions/`.** It now holds `README.md`, `0001`, `0002`,
`0003`, `0004`. Where a decision file and this memory differ, `decisions/` governs on who decided
what and when; the deliverable it approves governs on substance. I never edit `decisions/` — I
report.

---

## Closed on 2026-08-11 — verified, do not re-raise

| Was | Item | How it closed |
| :--- | :--- | :--- |
| O3 | Step 1 §9 obligations reached Step 8 and Step 13 only through Step 1's handoff list, not through the file the isolated instances read | **`task-sheet.md` Step 8 now writes them out in full** — right-censoring and the `L2 = 1` exclusion named as filters, the fixed documented order, contamination-before-censoring, the set-membership drop rule, the half-open UTC form with `date(watched_at) <= T1` banned by name, `action` retained, and every required count: both drop counts, D2, D3, D8, D9, censoring as two lines, the `pull_date` trio, five cadence buckets plus the boundary-proximity count, metadata disagreements. Step 8's preamble says explicitly it is written there "because this is the file the two isolated instances read." **Step 13 now carries both robustness arms** — last-observed S1 date (line 361) and the `action`-type arm — with the threshold-vs-date-definition distinction spelled out. Verified line by line. |
| N3 | Provenance gap closed in fact, open on the record | `decisions/0001` bullet 4 is now struck through and annotated **CLOSED 2026-08-10** with the three paths; `decisions/README.md` item 4 likewise. Verified. |
| N5 | `decisions/0001` said "six claims withdrawn", the table has twelve rows | `0001` "Standing record" now reads **twelve rows: eleven withdrawn or corrected, plus the one accepted risk (B2)**, with a dated footnote recording the earlier conflation. Verified. |

## Closed on 2026-08-10 — recorded so they are not re-raised

| Was | Item | How it closed |
| :--- | :--- | :--- |
| C1 | Step 4 endpoint decided in Step 1 but listed as open-and-blocking in Step 0 | Human Lead ruled `GET /users/:id/history`, unfiltered, one sweep per user. **D15**, decision **0002**. `artifacts/step0-access-and-setup.md` §0 and §6.1 now carry a resolution box and a struck-through open item; Step 1 §0 agrees. Verified. |
| C2 | Two figures in an approved public artifact had no public source | `src/step0_history_probe.py`, `logs/step0_history_probe.json`, and `artifacts/step0-history-endpoint-probe.md` exist. Both figures reproduce from one cached response at **zero live calls**. Verified all three paths. |
| C5 | Step 6 estimation sample specified two ways on a dual-implementation gate | Human Lead ruled **C1 bucket only**, applied to all shows. **D14**, decision **0003**. `task-sheet.md` Step 6 now carries it by bucket name, so both isolated instances read it from the file they actually read. Verified at `task-sheet.md` Step 6 and Step 13. |

---

## OPEN — carried forward

### O1. `pull_date` has no value (was C3)

Adopted in **form** (D11), value **deliberately deferred** to Step 4's schedule. Human Lead act;
no agent performs it. Constraint: `pull_date ≤ earliest per-user fetch date in the whole Step 4
sweep`. **Any step that right-censors, or computes D3, D8 or D9, is blocked on this value.**
Carried in `decisions/README.md` open item 1. Still the one outstanding item from Step 1.

### O2. The gap hypothesis is untested and belongs to no step (was C4)

Whether Trakt represents a numbering gap by **omitting** the number or by **listing a
placeholder** is unknown. If it lists a placeholder, `number ∈ E` for a non-existent episode,
the drop rule readmits the exact case the set rule was built to exclude, and `L := |E|` counts
an episode that does not exist. **Section 3 must not be read as "gaps handled."** Step 1 §3.3
assigns it to "wherever `E` is first pulled at scale", which is not a step and has no owner.
`decisions/README.md` open item 3 now carries it — registered, still unowned.

### O4. `L2 = 1` classifies into C2 "weekly" before it is excluded

At `L2 = 1`, `weekly_span = 0`, so `span ∈ {2, 3}` falls through C1 and lands in **C2 weekly**
under D12 first-match ordering. Harmless **only because** `L2 = 1` shows are excluded from the
headline population (§7) — but the exclusion happens at **Step 8** while the classification is
available from **Step 2** onward. Anyone who classifies before excluding sees nonsense weekly
buckets. The order matters and is written down nowhere. **Narrowed 2026-08-11:** `task-sheet.md`
Step 8 now names the `L2 = 1` exclusion as a filter in the fixed documented order, so the Step 8
end is covered. The exposure that remains is anything that classifies between Step 2 and Step 8.

### O5. Critical path — updated 2026-08-11

Step 3 is **complete**. `pull_date` (O1) is the next structural blocker and is now **actionable**:
its constraint is `pull_date ≤ earliest per-user fetch date in the whole Step 4 sweep`, and
Step 3 has produced the sweep's size (~210,500 calls, ≥23.4 h). The Human Lead sets it. Then:
Step 4 → Step 5 gate → Steps 6 and 7 gates → Step 8 gate. Step 2 (Human Lead) runs in parallel
and gates nothing here, but **no usable user becomes an analysis row without it**.

**403 and 429 status, updated.** `decisions/README.md` open item 9 says the first live exercise of
the 403 rule "will be during Step 3 or Step 4". **Step 3 is done and saw zero 403s** — run counter
`user_403_skipped: 0`, `rate_limit_pauses: 0`, `http_429: 0` across all 36 rounds. Both 403
branches and the 429 path remain **unexercised against the live API**. The item has not moved; its
wording is now stale on the disjunction and should read Step 4. **The transport-retry path did
run** — see S2 below — so of the three failure paths in `CLAUDE.md`, one is now live-tested and
two are not.

---

## NEW — surfaced 2026-08-11 from Step 3

Step 3 is Chained, not a gate, and produced **no decision file**. That is procedurally correct.
The items below are not about that; three of them are arithmetic inside the published artifacts.

### S1. CLOSED 2026-08-11 — the funnel's floor line was 6, the true total is 232

Raised by me, verified by the Human Lead, **write-up corrected**. §1 now prints **232 (5.4 % of
screened)** with `4,320 − 232 = 4,088` shown, and §9 position 4 now says the floor "did reject 232
accounts, so it is not inert". 6 was round 36's value read as a total. Recorded because the
recurrence risk is generic: **a per-round column summed wrongly into a funnel row.**

### S2. CLOSED 2026-08-11 — "zero errors" was wrong and is corrected

Raised by me, verified, **write-up corrected**. §1 now carries a counters table: requests sent
5,309, OK 5,300, **HTTP 5xx 16, transport errors 1, transient retries 9 (all recovered,
`errors: 0`)**, rate-limit pauses 0. It also states the failures fell on discovery calls, every
round showing `screen_other_status: 0`.

**The load-bearing consequence stands:** the retry-with-backoff branch of `CLAUDE.md` API
discipline **is now live-tested, nine times, successfully**. The 403 branches and the 429 path are
still unexercised. One of three failure paths is proven; two are not.

### S3. NARROWED 2026-08-11 — the pair counts were semantics; the reciprocity figure is a bug

**Resolved half:** 7,103 vs 6,166 is not an error. Each edge record carries two directions —
`(follower, followee)`, the social graph, and `(src, dst)`, the crawl traversal — and the write-up
now tabulates both, directing Step 11 to the social reading. Confirmed in
`src/step3_user_discovery.py:748-749`, which assigns follower/followee by whether the record came
from `/followers` or `/following`.

**Unresolved half, and I think I have the mechanism.** `artifacts/step3-yield-curve.json` reports
`reciprocal_pairs: 1353`; recomputation from `edges.jsonl` gives **1,172**. The write-up flags this
and tells Step 11 to recompute rather than read the yield curve — the right handling.

My reading of `src/step3_backfill.py:362-364`:

```python
edge_pairs.add(pair)
if (pair[1], pair[0]) in edge_pairs:
    reciprocal += 1
```

The counter increments **per record**, not per distinct pair, and the pair is added *before* the
reverse is checked. A genuine mutual pair increments once, correctly, on the second direction —
but **every duplicate record of an edge whose reverse is already present increments it again**.
There are exactly `7,426 − 7,103 = 323` duplicate records under this keying, and
`1,353 − 1,172 = 181`, which is ≤ 323 and therefore consistent. Self-loops, if any exist, inflate
it the same way.

**So 1,172 is very likely right and 1,353 is a double-count at a named line.** Flagged as a
hypothesis: I read the code, I did not run it, and I did not verify which 181 records are the
duplicates. See the confidence note in [[decision-log-step18]].

### S4. The task sheet named one stopping rule; the run used another

- `task-sheet.md` Step 3: "**Run until usable-user yield plateaus.**"
- `logs/step3_run.json`: `stop_reason: "sufficiency: reached the usable-user target"`. Plateau
  ratio finished at **0.314** against a 0.20 trigger, `consecutive_below: 0`.

The write-up says this plainly and makes it the headline, which is the right handling. What has no
home is that **`TARGET_USABLE = 4000`, the rule that actually bound, appears nowhere in
`task-sheet.md`** — nor do the other ten crawl constants ([[glossary-terms-and-thresholds]]).
Substituting the stopping rule of a step is a judgment with alternatives, a cost and a reviewer
disagreement (Engineering HOLD). It currently exists only inside a write-up. See
[[decision-log-step18]] for what a Step 18 entry would need.

Two facts sharpen it, both from the per-round record and both in the write-up:
**(a)** at rounds 9 and 10 the ratio sat within 15 % of the trigger and round 11 rebounded 4–6×
(`channel_a_yield_per_call` 0.458 → 6.25), so at `MIN_ROUNDS_BEFORE_PLATEAU = 9` the run would have
declared a plateau that did not exist; **(b)** the peak is anchored at round 1, which discovers the
seeds' own neighbours at near-zero dedup and can never recur, so "20 % of peak" is a fixed absolute
threshold wearing a relative threshold's clothes.

### S5. Step 11's decision rule is asymmetric in the direction Step 3 says is uninformative

- `task-sheet.md` Step 11: "If they diverge, **do not proceed to publication.**" Divergence blocks;
  agreement, by implication, clears.
- `artifacts/step3-user-discovery.md` §4.3: Channel A selects on public social activity, Channel B
  on public list authorship — **both select on public-facing activity**. "A ≈ B … would read as
  'no discovery bias' when it actually means two draws from the same biased frame agree.
  **Agreement between the two channels is not evidence of unbiasedness.**"

So Step 11 as written can fail the study but cannot clear it, and the likely outcome is the one it
reads as clearance. §9 position 2 puts the remedy to the Human Lead: an activity-stratified
diagnostic in Step 11's brief, or the limitation stated at Step 14. Screening already captured
`followers`, `following`, `episodes_watched`, `joined_at`, `total_plays` per user, so the
diagnostic is computable from `raw/step3/` at **zero further live calls** — that is a fact about
cost, not a recommendation.

### S6. Step 14's checklist carries one downward bias; Step 3 found a second that compounds

- `task-sheet.md` Step 14: "State that excluding inactive users biases the never-started share
  **downward**." One line, one mechanism.
- `artifacts/step3-user-discovery.md` §4: movie-commenting marks **tracking intensity**; heavy
  trackers are likelier to continue to S2, to log completely, and to survive the Step 7 liveness
  filter. "**Direction: downward on the never-started share** … the two **compound; they do not
  cancel.**" Sharper still: seeds were drawn **27 days after the TV Time shutdown of 15 Jul 2026**
  from recency-ordered feeds, so the frame oversamples the migration cohort **Step 5 exists to
  exclude** — and if Step 5 removes a large slice, it removes it after the discovery budget is
  spent.

**Direction check — PASS, and it is the one that is easy to get backwards.** My glossary records
the liveness *bound* as moving the headline **up** (inactivity-excluded pairs counted as
decliners). That is consistent with the *exclusion* biasing it **down**. Step 3's claim and Step 1's
diagnostic point the same way. `task-sheet.md` Step 14 is a five-item checklist; the second
mechanism is not on it.

### S7. `pull_date`'s cost scales with Step 4's duration, which just grew 2.4×

- `decisions/0001` / D11: `τ_pull` is a **single global frozen cutoff**, `pull_date ≤ earliest
  per-user fetch date in the whole sweep`, and **every record with `watched_at ≥ τ_pull` is
  discarded**.
- `artifacts/step3-user-discovery.md` §6: Step 4 is **≥23.4 h** of pure throttled time,
  "realistically longer once latency and any overnight suspend are included" — and §8 records
  round 8 losing **2,796 s to a suspended machine**, so suspends are not hypothetical here.

The rule is right — it is what makes exposure equal across users. The point is that the discarded
tail is a function of sweep span, the span is now 2.4× the assumed one, and `⟦pull_date⟧` floors to
UTC midnight, so the discard can reach a full day beyond the sweep. Nobody has costed it. It is
also the argument *for* one of §9's positions (sampling the pool down) that §9 does not make.

### S9. The stated warrant for `MIN_EPISODES_USABLE = 10` rests on a premise Step 1 does not grant

- `src/step3_user_discovery.py:43-45`: "The floor of 10 episodes is deliberately far below anything
  the study needs: **a user with fewer than 10 episodes logged cannot have completed any season 1**,
  so this pre-applies the frame rather than biasing it."
- `artifacts/step1-outcome-definition.md` §7: **`L2 = 1` shows are excluded; `L1 = 1` is retained.**
  Nothing in Step 1 or in `task-sheet.md` Step 2 sets a minimum S1 length. The S1 completion rule is
  `|D1| ≥ ceil(0.90 × L1)`, so a show with `L1 = 6` is completed at 6 distinct episodes.

If the Step 2 frame contains **any** show with `L1 ≤ 9`, the floor excludes genuine S1 completers,
and it removed **232** accounts. The claim is stated as a certainty ("cannot") and is not one.

This is the exact failure mode in [[withdrawn-claims-register]] — *asserting a property that does
not follow from the definitions actually given* — and it is the seventh instance. It is cheaply
checkable the moment Step 2 exists: **`min(L1)` over the frame, ≥ 10 or not.** Until then the
warrant is unverified, not wrong. Direction if it fails: light trackers excluded, i.e. **downward**
on the never-started share, compounding with S6.

### S10. `decisions/README.md` has not been updated for `0005`

- `decisions/0005-step3-stopping-rule.md` exists, **Status: Open — awaiting ratification**.
- `decisions/README.md` index table ends at `0004`; the open-items list ends at item 9; nothing
  records that a decision is awaiting ratification.

The README is the index Step 18 assembles from. An Open decision that the index does not list is
the one most likely to be missed. Also still stale there: item 9's "first live exercise will be
during Step 3 or Step 4" — Step 3 is done and saw zero 403s.

### S8. 1,027 eligible users were discovered and never screened

`5,347 eligible − 4,320 screened = 1,027`. Not stated in the write-up, though its funnel implies
it. Two consequences. **(a)** Extending the pool without any new discovery costs ~1,027 screen
calls — relevant to §9 positions 1 and 3. **(b)** Screening ran FIFO at 120/round, so the unscreened
1,027 are disproportionately the **latest-discovered**, which are disproportionately **depth 2**.
The §4 "usable by depth" figures (290 / 1,393 / 623 / 1,782) therefore mix a depth effect with a
screening-order effect: depth-1 users are 80 % of their A-first cohort, depth-2 users only 36 %.
**Any depth-stratified diagnostic built for S5 must condition on screened, not on eligible**, or it
will read screening order as depth.

---

## NEW — surfaced 2026-08-10

### N1. Section 8 still reads as though question 2 were open, and the residue is real

- `artifacts/step1-outcome-definition.md` **§8**: "Their treatment in the Step 6 lag distribution
  is a separate question and **stays open** (open question 2) … my **recommendation** in Section
  10.1 is the C1-only estimation sample."
- **§9, §10.1 and §11** of the same document: question 2 is **decided** as D14; "the negative-lag
  question that travelled with it is **closed** by the same decision."

§8 was not updated when D14 landed. That is the stale half. **The live half is that D14 does not
actually close the negatives everywhere:** it makes every lag in the *estimation sample*
non-negative by construction, but `task-sheet.md` Step 6 also requires the **all-shows** lag
distribution to be plotted alongside, and for a weekly show the negative mass is most of the
started population. Nothing states how negatives are treated in that plot.

Why this is not cosmetic: **Step 6 is a dual-implementation gate**, and `task-sheet.md` Step 13
defines the required robustness range as "the range implied by the gap between the C1-only and
all-shows lag distributions". If the two isolated instances handle the negative mass differently,
they diverge on the all-shows plot and the divergence **propagates into Step 13's tested range** —
the same class of failure D12 and D13 were written to prevent.

### N2. D2 is computed on definition (b), so it cannot count the failure the addendum points at

- `artifacts/step1-outcome-definition.md` **§5 addendum** (added post-approval): the probe profile
  is "the first observed instance of the failure D2 exists to measure", and "It establishes the
  failure mode is real and reachable, **not how common it is — that is what D2's count is for.**"
- **D2 as defined** (§5 required output, §10.0 D2 row, §9 Step 8 handoff): it counts pairs whose
  first S2 watch precedes **their clock start**, and clock start is built on **definition (b)**,
  first-pass completion, which a rewatch cannot move.

Under (b) this profile's lag is **+360.73 days**. It will **not** appear in the primary D2 count —
by construction, no (a)-style rewatch artifact can. D2 under (b) measures genuine parallel viewing,
which is a different quantity and a useful one, but it is not a frequency estimate for the
(a)-failure. That frequency would be D2 recomputed inside the **Step 13 arm (i)** last-observed
run, and **no step requires D2 in that arm** — arm (i) is not even in `task-sheet.md` Step 13 (O3).

Consequence to state when it is raised: whoever computes D2 should **expect zero** instances of
this profile's failure mode in the primary run, and should not read that zero as evidence the
failure is rare.

### N3. CLOSED 2026-08-11 — see the closed table above.

### N4. An unobserved premise sits inside an approved rule

- `artifacts/step1-outcome-definition.md` §2.1: `episode.ids.trakt` "should agree with
  `(show, season, number)`; where it disagrees — **which happens after Trakt metadata merges and
  splits** — `(show, season, number)` wins … Disagreements are counted and logged."
- `artifacts/step0-history-endpoint-probe.md` §2: 96 distinct episode Trakt IDs against 96
  distinct pairs, **zero disagreements**, no pair mapping to more than one ID. "Not contradicted;
  simply **untested** by this profile."

Not load-bearing for the rule — `(show, season, number)` wins either way — but the *mechanism*
asserted (merges and splits reassign episode IDs) is the **same mechanism D9's split signature
depends on**. If the mechanism is rarer or shaped differently than assumed, the D9 lower bound is
weaker than its wording implies. One profile is not evidence either way; it is the absence of
evidence, and it is now on the public record as such.

### N5. CLOSED 2026-08-11 — see the closed table above.

### N6. Minor — the Step 0 file index is stale

`artifacts/step0-access-and-setup.md` "Files" table lists `step0_test_pull.py` and
`step0_watched_endpoint_probe.py` but not `src/step1_episode_listing_probe.py`,
`src/step0_history_probe.py`, or their run records. Each has its own write-up, so nothing is
lost; the index is just no longer complete.

---

## Checks that PASS — recorded so they are not re-litigated

Verified 2026-08-11 on Step 3:

- **Every funnel identity except the floor line reconciles.** `5,694 − 347 private − 0 deleted =
  5,347 eligible`. `3,749 A-first + 1,945 B-first = 5,694`, and A by depth `300 + 1,734 + 1,715 =
  3,749`. Usable by channel `2,306 + 1,782 = 4,088`; usable A by depth `290 + 1,393 + 623 = 2,306`.
  Calls `10 seed + 972 discovery + 4,318 screen = 5,300`, and `4,318 live + 2 cache = 4,320
  screened` — the two cache hits are why screened exceeds screen calls. The **only** broken line is
  the floor count (S1).
- **The 61/39 channel split is over non-seed eligible users, not all eligible.** `3,102 + 1,945 =
  5,047`, plus the 300 seeds = 5,347. It follows that **all 347 private profiles were Channel-A
  non-seed discoveries**. The write-up does not state the base; the arithmetic is sound.
- **Step 4 forecast arithmetic.** `4,088 × 51.49 = 210,500`; `210,500 / 150 / 60 = 23.39 h`;
  `4,000 × 51.49 ≈ 205,969`. Histogram users sum to 4,088.
- **The replay is what it claims.** 36 rounds × 12 fields, 0 mismatches, 0 live calls, 5,302 cache
  hits. Throttle-sleep seconds are `null` with `not_recoverable`, never estimated — the honest
  handling, and the CSV column is genuinely empty in all 36 rows.
- **Privacy boundary intact.** `artifacts/step3-user-discovery.md`, `.json` and `.csv` carry counts
  and aggregates only — no username, user ID, list slug or film title anywhere. Identifiers stay in
  `raw/step3/`. Verified.
- **The seeding rule was obeyed.** Seeds are movie-comment authors across 172 films; movies cannot
  enter the Step 2 frame, so the `task-sheet.md` Step 3 prohibition on harvesting from comments on
  measured shows is satisfied. The bias in S6 is a different objection and the write-up says so.

Verified 2026-08-10 against the current files:

- **Both probe figures reproduce.** 123 records, 96 distinct pairs, 25 episodes duplicated, 27
  surplus records, 64 pages at `limit=250` — all exact. "28 percent" is 28.125 %; "six weeks" is
  5.90 weeks (41.31 days). Rounding only, both in the direction that makes the printed number
  rounder rather than larger.
- **27 surplus records and 25 duplicated episodes are both correct and are different questions.**
  Two episodes appear three times. Do not "correct" one to the other.
- **The 96 is derived from history, not from `show.aired_episodes`** — which also reads 96 on that
  payload. Coincidence of a completionist profile. §2.1's rule stands independently, and §0
  forbids `aired_episodes` outright.
- **The §5 addendum changes no rule.** Verified line by line: §4, §5's definition (b), §6, §7,
  §2.2, D2's requirement text and the §9 handoff lists are unchanged. The addendum adds evidence
  and a scope limit. The gate remains approved and the approval record says so.
- **`task-sheet.md` Step 6 carries D14 by bucket name**, not as "binge shows", and Step 13 carries
  both the range obligation and the per-arm retained-row count.
- **Privacy boundary intact.** No username, user ID, or watch history in `artifacts/` or
  `decisions/`. The new probe write-up names neither profile nor show and keeps episode-level
  material in `logs/` and `raw/`. The username is a script argument, not hard-coded.
- **Zero live API calls were spent on the reproduction.** `requests_sent: 0`,
  `served_from_cache: 2`.
- Previously verified and still true: censoring clearance costs no show; the `+H` cost estimate;
  the 91-day arm sits inside the primary censored population; D12 is exhaustive and mutually
  exclusive under first-match; the boundary convention is used consistently and no second reading
  survives; both one-day directions are declared and neither is netted off.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[decision-log-step18]], [[withdrawn-claims-register]], [[step1-open-questions]].
