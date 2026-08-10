# Step 1: Outcome Definition

**Owner:** Data Scientist (drafts) · **Mode:** GATE · **Reviewer:** Red Team (hold / proceed)
**Status:** DRAFT — PROPOSED, NOT ADOPTED. Requires written approval from the Human Lead.
**Date:** 2026-08-10 · **Revised twice, 2026-08-10:** Human Lead decisions, then the
authorized revision following Red Team's HOLD
**W is not set in this document.** No code was written or run to produce it.

This document defines what is being measured, on one user-show pair, from episode-level
watch history alone. It fixes the population, the clock, the three outcome states, the
abandonment point, and every counting rule needed to compute them deterministically. It
does not set W, does not set the liveness threshold, and does not set the contamination
exclusion rule. Those are Steps 6, 7, and 5.

**Red Team returned HOLD on the previous draft. This revision was authorized in response.**
Seven settled items — Human Lead decisions and items already closed in `task-sheet.md` — are
recorded in Section 10.0 and incorporated into the body of the document rather than appended
to it. Four open questions remain in Section 10.1, each carrying a recommendation that the
Human Lead decides.

**Four claims from the previous draft are withdrawn as false, and each is marked as such where
it appeared** rather than quietly deleted:

| Withdrawn claim | Where | Replaced by |
| :--- | :--- | :--- |
| Entry and exit are symmetric | Section 7 | They are not — S1 completion is evaluated over all time, S2 completion within `W`. The asymmetry is now stated as a bias with a known direction, and D3 measures it. |
| Right-censoring costs zero rows | Sections 6, 10.1 Q3 | `S1_completion_date` is uncapped, so it removes recent S1 completers, who are disproportionately likely to continue. It moves the headline **up**. |
| Truncating negative lags at zero | 10.1 Q2 | W estimated on binge-release shows only, then applied to all. |
| `p ∈ (0, 1]` follows from `p = m / L2` | Section 7 | It does not when `F2 > L2`. `p` is now rank-based, and the range holds by construction. |

---

## 0. Data source and what may not be used

**Source, decided by the Human Lead:** `GET /users/:id/history`, unfiltered, one sweep per
user. Each record carries `id`, `watched_at`, `action`, `type`, and for episodes an
`episode` object (`season`, `number`, `title`, `ids`) plus a `show` object.

**Everything in this definition is computed from those records.** Specifically:

- **No drop flag is used, ever.** Trakt's dropped status is OAuth Required and unavailable
  to this study. The three outcome states are inferred from which distinct episodes appear
  in history and when. Watchlist, collection, and ratings are likewise not used.
- **`show.aired_episodes` is not used.** It appears directly on the `show` object inside
  every history record and is the obvious trap: it is a **show-wide** count of aired
  episodes, not a per-season count. Season lengths come from the source in Section 3.
- **The sweep must be complete.** The endpoint paginates and returns play events
  newest-first. A truncated sweep is indistinguishable from a genuine "never started" and
  would land in the headline. The "never started" state is only meaningful if the pull for
  that user is known complete; enforcement is Step 4's and Step 8's, but the dependency is
  recorded here because it is this definition that it breaks.
- **The endpoint mixes `type: episode` with `type: movie`.** For outcome measurement, only
  `type: episode` records belonging to the show in question are used. **Liveness (Step 7) is
  not restricted to the show under study**: it is a statement about the account, so it is
  evaluated across the user's whole sweep, other shows and movies included. Whether the gap
  distribution is built on raw play events or on deduplicated episodes is **Step 7's analysis
  to run**, and Step 1 does not decide it.

**Timezone and granularity.** `watched_at` is ISO 8601 UTC. **Ordering is always on the full
UTC timestamp**; date reduction applies to clock arithmetic only — `T0`, `T1`, lags, and
gaps are whole numbers of days, because W is a number of days — and never to sequencing, so
the tiebreak in Section 2.2 fires only when two full timestamps are exactly equal.

---

## 1. Unit of analysis and population

**Unit:** one user, one show. One row per `(user, show.ids.trakt)` pair. A pair appears at
most once, no matter how many times either season was watched.

**Population for the headline:** pairs where the user **completed S1** by the rule in
Section 4, on a show in the Step 2 frame, surviving the Step 5 contamination exclusions and
the Step 7 liveness rule.

Filter order, sample size after each filter, and the invariant checks are Step 8's, not
this document's. What Step 1 fixes is *what each filter is testing*.

**Liveness is an eligibility filter, not an outcome state.** Outcome states are assigned
only among users who pass it. This matters for Step 9: the bound is computed by moving the
inactivity-*excluded* users into "never started," which is only coherent because they were
never assigned a state in the first place.

---

## 2. Counting rules

These three rules are prior to everything else. Every count below obeys them.

### 2.1 Distinct episodes, never play events

The Step 0 probe found **123 records covering 96 distinct `(season, number)` pairs on a
single profile — 28 percent inflation, with 25 episodes appearing more than once.** Play
events are therefore not a usable unit for any count in this study.

**Dedup key:** `(show.ids.trakt, episode.season, episode.number)`, scoped to the user.
`(season, number)` alone is not unique across shows, so the show ID is part of the key.

`episode.ids.trakt` is *not* the canonical key. Where present it should agree with
`(show, season, number)`; where it disagrees — which happens after Trakt metadata merges and
splits — `(show, season, number)` wins, because that is the key that maps onto season
length and onto the abandonment point. Disagreements are counted and logged, not silently
resolved.

This rule applies to the 90 percent test, the started/never-started split, and the
abandonment point. Whether it also applies to the Step 7 gap distribution is Step 7's to
decide, not Step 1's (Section 0).

### 2.2 One timestamp per distinct episode: the earliest

Collapsing duplicate records requires choosing which `watched_at` survives.

**The canonical timestamp for a distinct episode is the minimum `watched_at` across its
records.** Rationale: every date this study uses is a *first-pass* date — when the user
first completed S1, when they first started S2. A rewatch is not new information about
either. Taking the maximum would import exactly the rewatch distortion that Section 5
exists to remove.

Deterministic ordering, needed so two isolated implementations agree: sort collapsed
episodes ascending by canonical `watched_at`, **compared as full UTC timestamps and not as
dates** (Section 0); ties broken by episode number ascending, then by the smallest history
event `id`. The tiebreak therefore applies only to exactly equal timestamps, which is a real
case — bulk imports and season-at-once marks write identical values — and not to everything
sharing a calendar day.

### 2.3 Which records count as watching

`action` takes at least three values in this data: `scrobble`, `watch`, and `checkin`.

**All three count as watching the episode. A check-in counts.** Three reasons:

1. The outcome states depend on **whether the episode was ever viewed**, not on how the
   view was logged. A check-in is a first-person assertion that the user is watching that
   episode, and Trakt writes it into history as a watch of that episode.
2. `action` is a property of the **logging client**, not of the viewing. Some apps scrobble,
   some check in, some only support a manual mark-as-watched. Filtering on `action` would
   filter on the user's choice of app, which is a selection bias with no relation to the
   outcome, and it would push check-in-heavy users toward "never started."
3. Because we count **distinct episodes** (2.1), the known duplicate-generating pattern —
   a client writing both a `checkin` and a `scrobble` for one viewing — cannot inflate
   anything. The permissive `action` rule is safe precisely because the dedup rule is strict.

Any `action` value not in the three above is also treated as watching, and its record count
is logged so an unexpected value is visible rather than silently absorbed.

**One caveat, handed to Step 5, not resolved here.** `action: watch` includes manual
backfill and bulk import, where `watched_at` is a date the user or the importer supplied
rather than an observed one. That is a *timestamp* problem, not an *action* problem, and it
is exactly what the Step 5 contamination rule is for. Step 1 does not filter on `action`;
it requires that `action` be **retained as a column** in the Step 8 table so Step 5 can use
it and Step 13 can run a sensitivity arm on it (Section 9).

---

## 3. Where season length comes from

**S1 and S2 lengths come from the Step 2 show frame**, which collects S1 and S2 episode
counts as fields. Where the frame is not yet available, the same numbers come from
`GET /shows/:id/seasons` (per-season `episode_count` / `aired_episodes`), which is the
source the frame itself draws on. Step 0's test pull already confirmed that endpoint returns
per-season S1 and S2 counts under Client-ID-only auth.

**Never `show.aired_episodes`** from the history payload, for the reason in Section 0.

Definitions, per show:

| Symbol | Meaning |
| :--- | :--- |
| `L1` | number of episodes listed for season 1, excluding season 0 |
| `F1` | the S1 finale: the **highest** episode number listed for season 1 |
| `L2` | number of episodes listed for season 2, excluding season 0 |
| `F2` | the S2 finale: the highest episode number listed for season 2 |

`L1` is a **count** and `F1` is a **maximum**. For contiguously numbered seasons they are
equal. They are kept separate so that a season with a numbering gap does not silently break
the 90 percent denominator, and so that the Step 8 invariant "distinct episodes never exceed
season length" is testing the count against the count.

**Specials are season 0 and are excluded** from `L1`, `L2`, from the completion test, and
from the abandonment point. They still count as logged activity for liveness.

**Out-of-range episode records** — `number` greater than the highest listed number for that
season, or `number` less than 1, or a missing `season` or `number` — are dropped from the
counts and **counted separately per show**. A show with many such drops has a stale or wrong
frame entry, and that is what the count is there to reveal. This drop rule is what makes the
Step 8 invariant "distinct episodes never exceed season length" enforceable rather than
merely hopeful.

Shows where `episode_count` and `aired_episodes` disagree for S1 or S2 are flagged and
counted. Given the Step 2 frame requires S2 to have finished airing on or before
31 Dec 2024, they should agree; a disagreement means the show is not what the frame thinks
it is.

---

## 4. S1 completion

> **Season 1 counts as complete when the user watched the S1 finale AND at least 90 percent
> of S1 episodes.**

Made exact:

- Let `D1` = the set of **distinct** S1 episodes for that user and show, in range `1..F1`,
  per Sections 2.1 and 3.
- **Required:** `F1 ∈ D1` **and** `|D1| ≥ ceil(0.90 × L1)`.

`ceil` is the strict reading of "at least 90 percent." For `L1 = 10` it requires 9. For
`L1 = 8` it requires 8, i.e. all of them, because 7 of 8 is 87.5 percent. The threshold is
stated in episodes, not in a rounded percentage, so it is reproducible.

A user-show pair failing this test is **not in the population**. It is not a "never started"
— it never entered.

---

## 5. The S1 completion **date**, and the rewatch problem

This is the second Step 0 finding and it must be resolved here because clock start is built
on it. On the probe profile, **the first S2 watch preceded the last S1 watch by six weeks**:
histories are not monotonic, because people rewatch.

Two candidate definitions of "the user's own S1 completion date":

| | Definition | Behaviour |
| :--- | :--- | :--- |
| **(a)** | The **last observed** S1 timestamp: `max watched_at` over all S1 records | Moves forward every time the user rewatches S1, potentially by years |
| **(b)** | **First-pass completion**: the earliest date at which the Section 4 test was satisfied | Fixed once satisfied; later rewatches cannot move it |

### Proposed: (b), first-pass completion.

**Algorithm.** Collapse S1 records to distinct episodes with the earliest-timestamp rule
(2.2). Sort ascending by that timestamp with the tiebreak in 2.2. Walk forward accumulating
the distinct set `D`. **The S1 completion date is the `watched_at` date of the first episode
at which `F1 ∈ D` and `|D| ≥ ceil(0.90 × L1)` both hold.** If they never both hold, the pair
is out of the population per Section 4.

The walk handles both real patterns correctly. A user who watched all of S1 in 2019 and
rewatched five episodes in 2022 completes in 2019 — the distinct set was already full. A
user who watched E1–E6 in 2019, stopped, and finished in 2022 completes in 2022, which is
genuinely when they completed.

### Why (b), stated as the reason it will be challenged

Definition (a) is wrong on the merits in two ways. It measures the wrong event: the question
this study asks is *when did the choice to continue to S2 become available*, and that is the
first-pass date, not the date of a rewatch years later. And it is **biased by engagement**:
under (a), the heavier a rewatcher a user is, the later their clock starts and the more time
they are granted to start S2. That grants the longest windows to exactly the most engaged
users, which is a bias running straight into the headline.

### The consequence for clock start, stated plainly

`(b) ≤ (a)` always, and strictly less for any rewatcher. So **(b) produces an earlier clock
start, an earlier close, and therefore a *higher* never-started share than (a) would.** That
is the direction that strengthens the headline claim, and it should be said out loud rather
than discovered by the Red Team.

Two things are done about it. First, (b) is defended on the merits above, not on the
result. Second, **Step 13 must carry definition (a) as a robustness arm** — recompute the
headline with the S1 completion date set to the last observed S1 timestamp. If the headline
survives (a), the choice of (b) is not load-bearing. If it does not survive, that is a
finding and it is reported.

### The consequence for the Step 8 invariant, stated plainly

**The old invariant, "no clock start precedes an S2 premiere," is vacuous under a
finale-anchored clock and has been replaced.** `task-sheet.md` Step 8 now requires, for every
row:

> clock start is on or after the S2 finale date, clock start is on or after the first-pass S1
> completion date, and clock start **equals one of those two dates**.

The replacement is a genuine improvement over the old check and it is worth being precise
about why, because the reason is narrow. The two inequalities alone would still be vacuous —
they restate `max()`. **The equality clause is what does the work.** An implementation that
used definition (a), last-observed S1, would produce a clock start equal to the last-observed
date for any rewatcher whose rewatch fell after the S2 finale; that value equals neither the
finale date nor the first-pass completion date, and the invariant fails. So the new invariant
**does** catch a last-observed implementation, provided the check computes the first-pass date
independently rather than reading back whatever the pipeline used.

What it still does not do is tell anyone whether first-pass is the *right choice*. It
enforces that the definition on paper is the definition in the code. The question of whether
that definition describes real viewing is what the required diagnostic below is for. Reading
a passing invariant as evidence about the rewatch decision would be a mistake, and it is the
kind that survives into a published number, so it is stated in the body rather than in a
footnote.

### Required output: the negative-lag diagnostic

**Decided by the Human Lead. This is a required output, not a proposal.**

> **Step 8 must count and report the number of user-show pairs whose first S2 watch date is
> strictly earlier than their clock start** — a negative lag — as a count and as a share of
> the population, **split by which term of the `max()` is binding**: the user's S1
> completion date, or the show's S2 finale air date.

The split is what makes it diagnostic, and under finale anchoring (Section 6) it is doing
real work, because the two terms now mean different things:

- **S1-term negative lags** are the ones this section is about. They are users who watched
  S2 before finishing S1 — genuine parallel viewing under definition (b), and largely rewatch
  artifact under definition (a). **This count is the actual test of the choice made in this
  section**, and it is the number to look at instead of the invariant. It should be small
  under (b); if it is not, definition (b) needs re-examination.
- **S2-finale-term negative lags** are not an anomaly at all under finale anchoring. They are
  the normal case for anyone who watched a weekly-release season while it was still airing.
  They are expected to be a large share of started users, and their size is information about
  the show frame's cadence mix rather than about data quality.

Counts only, so it belongs in `artifacts/`. The two sub-counts must be reported separately;
a single combined figure would hide the S1-term signal underneath the much larger
S2-finale-term mass, which would defeat the purpose of asking for it.

---

## 6. Clock start

**Decided by the Human Lead: clock start is anchored on the S2 finale, not the S2 premiere.**

> **Clock start `T0` = the later of the S2 finale air date and the user's own S1 completion
> date.**

`T0 = max(S2_finale_air_date, S1_completion_date)`, both as UTC calendar dates, with the S2
finale air date taken from the Step 2 show frame — which already collects it as a field — and
the S1 completion date from Section 5.

The window closes at **`T1 = T0 + W days`**. W is set in Step 6 and is not set here.

### Why the finale, and not the premiere

Three reasons, all of which will be asked about out loud:

1. **Consistency with Step 6.** Step 6 already anchors the lag on the S2 finale date for
   weekly-release shows. Anchoring the outcome clock on the premiere while deriving W against
   the finale would mean W was measured on one origin and applied to another. The two must be
   the same origin or the number is not interpretable.
2. **"Continued" is otherwise unreachable inside W for weekly shows.** A 13-episode weekly
   season takes roughly 84 days to finish airing. Under premiere anchoring, a user cannot
   watch the S2 finale within a window shorter than that, because the finale has not aired
   yet — so the Continued state would be an artifact of release cadence rather than a
   description of the viewer.
3. **Premiere anchoring scores waiting for a full season as never-started.** A user who waits
   for a weekly season to finish and then watches it is not a decliner, but under premiere
   anchoring with any short W they are counted as one. That collapses "declined" and "waiting
   to binge" into a single number, which is precisely the conflation this study exists to break.

**Binge-release shows are unaffected.** Where a season drops all at once, the premiere and
finale air dates coincide, so `T0` is identical under either anchoring. The decision changes
weekly-release shows only.

### The cost, stated explicitly: unequal exposure, not calendar timing

**The cost of D1 is that weekly and binge shows are not measured on equal exposure.** The
window `W` is not the whole of a user's opportunity to start S2. S2 becomes available at the
**premiere**, but under D1 the clock starts at the **finale**, so:

| Cadence | Elapsed opportunity to have started S2 by `T1` |
| :--- | :--- |
| Weekly release | `airing_span + W`, where `airing_span = S2_finale − S2_premiere` |
| Binge release | `W`, since `airing_span = 0` |

For a 13-episode weekly season, `airing_span ≈ 84` days. Every one of those days is time in
which a user could have started S2 and, if they did, they are counted as **Started** by the
one-sided bound in Section 7. **The never-started share is therefore mechanically lower for
weekly titles than for binge titles, by construction rather than by behaviour**, and the size
of that mechanical gap scales with season length.

This is a confound in the headline, not a presentational detail. Two consequences follow and
both are required, not suggested:

- **Cadence is a required reported stratum of the Step 9 headline.** The pooled number is a
  weighted average over the frame's cadence mix, so it moves if the mix moves. Weekly and
  binge must be reported separately alongside it, with intervals, so a reader can see how
  much of any difference is exposure.
- **Cadence is a mandatory entry on the Step 12 candidate list**, alongside origin, gap
  length, S1 episode count, and user tenure — and it is the one candidate with a known
  mechanical driver, which must be said when its result is reported so a mechanical artifact
  is not read as an audience finding.

D1 is still the right call: premiere anchoring has the opposite and worse defect, scoring a
user who waits for a full season as a decliner, and it puts Continued out of reach inside W.
The exposure asymmetry is the price, and it is paid openly by stratifying rather than by
hoping the pooled number is fair.

**Right-censoring.** A pair whose window has not closed by the data pull date cannot be
classified. Proposed rule: **require `T0 + max(W, 91) days ≤ pull date`**, using 91 rather
than W alone so that the primary headline and the 91-day arm in Step 9 run on the **same
population**.

**This is not a free guard, and an earlier draft of this document was wrong to call it one.**
The frame caps the S2 finale at 31 Dec 2024, but `S1_completion_date` is **uncapped** — a
user can finish S1 of a 2019 show in 2026. Since `T0 = max(...)`, those users have a `T0`
near the pull date and are removed by right-censoring. They are not a random slice:

- They are people who **found an old show recently**. The entire series is already available
  to them, they arrived by choice rather than by marketing, and there is no inter-season wait
  to survive.
- They are therefore **disproportionately likely to roll straight into S2** — that is, to be
  Continued or at least Started.
- Removing likely continuers from the denominator **moves the never-started share upward**.
  Right-censoring biases the headline in the direction that flatters the claim, and the size
  of the removal is the size of the concern.

Two requirements follow:

1. **The right-censoring removal count is reported unconditionally in the Step 8 waterfall**,
   never suppressed as "expected to be zero," with the upward direction of its effect named
   in the same line.
2. **Ordering constraint: the Step 5 contamination exclusion runs *before* right-censoring,
   not after.** A bulk import stamps a recent `watched_at` on old viewing, which produces a
   spuriously recent first-pass S1 completion date and therefore a recent `T0`. If censoring
   ran first, that user would leave the sample as a censoring drop and never appear in the
   contamination counts — the import artifact would be laundered into a timing exclusion and
   become invisible. Contamination first, censoring second, so each removal is attributed to
   the thing that actually caused it.

The rule itself remains open question 3 in Section 10.1.

---

## 7. The three outcome states

Measured at `T1 = T0 + W`, from distinct S2 episodes only.

Let `A` = the set of **distinct** S2 episodes for that user and show, in range `1..F2`, whose
canonical timestamp (2.2) is **on or before `T1`**. Let `m = max(A)` when `A` is non-empty.

| State | Condition |
| :--- | :--- |
| **Never started** | `|A| = 0` |
| **Continued** | `|A| ≥ 1` **and** `F2 ∈ A` **and** `|A| ≥ ceil(0.90 × L2)` |
| **Started and left** | `|A| ≥ 1` **and not** the Continued condition |

**Mutually exclusive and exhaustive by construction.** The partition is
`A = ∅` / `(A ≠ ∅ ∧ C)` / `(A ≠ ∅ ∧ ¬C)`, so no eligible pair can fall in two states or in
none. This is what satisfies the Step 8 invariant that the states sum to the sample.

Three properties worth stating:

- **The bound is one-sided, and under finale anchoring that is load-bearing.** "On or before
  `T1`" has no lower bound, so a user who watched S2 episodes *before* their clock started is
  correctly counted as **started**, not as never started. With `T0` anchored on the S2 finale
  (Section 6), every user who watched a weekly season while it was airing falls into this
  case. The one-sided bound is what keeps the finale-anchoring decision from misclassifying
  the entire live-viewing audience as never-started. Section 8 covers the group.
- **Entry and exit are NOT symmetric, and an earlier draft claimed they were.** The arithmetic
  is the same on both sides — finale plus `ceil(0.90 × L)` — but the *quantifier* is not. S1
  completion is evaluated over **all of time**: a user qualifies if they ever completed S1, at
  any point in their history. S2 completion is evaluated **within `W` days of `T0`**. A user
  who takes eighteen months to finish S1 still enters the population; a user who takes
  `W + 1` days to finish S2 is scored Started-and-left. **The definition is generous on entry
  and strict on exit, and that asymmetry pushes pairs into Started-and-left.** It is a real
  bias with a known direction, it is not repaired by keeping the arithmetic matched, and the
  required resumption diagnostic (Section 10.0, D3) exists to measure how much of
  Started-and-left it accounts for. Open question 1 in Section 10.1 records the alternative
  boundary and defends the drafted one on grounds other than symmetry.
- **No drop flag, no watchlist, no self-reported status.** Only which distinct episodes are
  in history, and when.

### Abandonment point

> **Abandonment point `p` = highest S2 episode watched, as a fraction of season length.**

An earlier draft defined this as `p = m / L2` and asserted `p ∈ (0, 1]`. **That assertion does
not follow.** `L2` is a *count* of listed S2 episodes and `m` is an episode *number*; where S2
numbering has a gap, `F2 > L2` and `m / L2` can exceed 1. Section 3 keeps `L2` and `F2`
separate precisely because they can differ, and the range claim quietly assumed they could not.

**Resolved by making `p` rank-based rather than a raw number ratio:**

> `p = |{ listed S2 episode numbers ≤ m }| / L2`

That is, the position of the highest watched episode within the season's actual episode list,
over the length of that list. Both numerator and denominator now count listed episodes, so
`p ∈ (0, 1]` **holds by construction**: the numerator is at least 1 since `m` is itself
listed, and at most `L2`. For a contiguously numbered season — which is nearly all of them —
this is identical to `m / L2`, so the fix changes no ordinary case and closes the pathological
one. Defined **only for the Started-and-left group**, computed on distinct episodes so a
rewatch cannot move it.

Episodes with numbers not in the season's listed set are already dropped upstream by the
out-of-range rule in Section 3, which is what lets the numerator be well-defined here.

`p` can equal exactly 1.0 for a Started-and-left user: someone who watched the S2 finale but
fewer than 90 percent of S2. That is a real behaviour — skipping ahead — and not the same
thing as a near-finale drop. **Step 10 reports it as its own named residual category and does
not merge it into "near-finale."** Its size should be checked early; it is what open
question 1 in Section 10.1 turns on.

Step 10's own constraint stands and is restated here because it is definitional: progress is
self-reported and approximate, so `p` supports statements about **regions** of a season and
does not support a claim about a specific episode.

---

## 8. Users who started S2 before their clock started

The finale-anchoring decision (Section 6) makes this group **large rather than marginal**, and
it now has two distinct populations inside it. Section 5 requires them to be counted
separately for exactly this reason.

- **S2-finale-term.** Anyone who watched a weekly-release season while it was still airing
  starts S2 before `T0`, because `T0` is the finale air date. This is not an error and not an
  edge case; for a weekly show it is what ordinary live viewing looks like.
- **S1-term.** Users whose S1 completion date is the binding term and who nevertheless
  watched S2 first — genuine out-of-order viewing. Under first-pass completion (Section 5)
  this should be a small group and is no longer a rewatch artifact.

**Treatment for the outcome states: keep them, classified as Started.** That is what the
one-sided bound in Section 7 already does, and it is correct — they demonstrably did start.
Any other treatment would misclassify the live-viewing audience of every weekly show.

**Their treatment in the Step 6 lag distribution is a separate question and stays open**
(open question 2). Step 6 restricts to users who did start S2 and plots the lag from clock
start to first S2 episode; for this group that lag is **negative**, and after D1 the negative
mass is not a tail — for a weekly show it is most of the started population. That is why the
question is no longer "what do we do with the negatives" but "which shows can W honestly be
estimated on at all," and my recommendation in Section 10.1 is the binge-only estimation
sample rather than any repair applied to the negatives. W must be defensible out loud, and a
number whose value depends on the frame's cadence mix is not.

---

## 9. What this definition hands to later steps

Recorded here so nothing is reconstructed later from memory.

- **Step 5** receives: `action` is not filtered on at Step 1, so manual and imported
  timestamps are still in the data when Step 5 runs, which is the correct order. Step 5's
  exclusion must also be applied **before** right-censoring, so an import-stamped S1 completion
  date is counted as contamination rather than laundered into a censoring drop (Section 6).
- **Step 6** receives: `T0` anchored on the S2 finale per D1 (Section 6), the first-S2-watch
  date on distinct episodes, and the open question about how negative lags enter the lag
  distribution (open question 2). Because `T0` and the Step 6 lag now share the same origin, W
  is derived and applied against one clock rather than two.
- **Step 7** receives: liveness is a statement about the **account**, so it is evaluated over
  the user's whole sweep and is **not restricted to the show under study**. Whether the gap
  distribution is built on raw play events or on deduplicated episodes is Step 7's analysis to
  run; Step 1 takes no position.
- **Step 8** receives: the filter order is Step 8's, but five things here are its
  responsibility to enforce — the out-of-range drop rule (Section 3) that makes the
  season-length invariant meaningful; the **required** negative-lag report split by binding
  term (D2); the **required** resumption-rate report (D3); the unconditional right-censoring
  removal count with its direction named, and the ordering constraint that Step 5 contamination
  exclusion runs *before* right-censoring (Section 6); and retention of `action` as a column.
  The new three-part clock-start invariant in `task-sheet.md` should compute the first-pass S1
  completion date **independently**, not read back the pipeline's value, or its equality clause
  proves nothing (Section 5).
- **Step 9** receives: the cadence stratum requirement (Section 6); the S3-without-S2 bound
  (D4) reported alongside the liveness bound; and the 91-day arm's separate origin (D5), which
  must be stated in the write-up and not smoothed over.
- **Step 12** receives: cadence as a mandatory candidate on the list, flagged as the one
  candidate with a known mechanical driver (Section 6).
- **Step 13** receives two required robustness arms from this document, in addition to the
  ones already in its own step: **(i)** S1 completion date as last-observed rather than
  first-pass, per Section 5; **(ii)** an `action`-type arm excluding `checkin`-only and
  manual-`watch`-only evidence, per Section 2.3. Both exist because a permissive choice was
  made here and the permissiveness should be shown not to be load-bearing.

---

## 10. Settled items, and open questions

### 10.0 Settled — decided by the Human Lead or already closed in `task-sheet.md`

None of these are mine to re-propose. All are incorporated into the body of this document.

| # | Settled item | Where it lands |
| :--- | :--- | :--- |
| **D1** | **Clock start is anchored on the S2 finale air date, not the S2 premiere.** `T0 = max(S2_finale_air_date, S1_completion_date)`. Rationale and cost in Section 6. Binge shows are unaffected. | Sections 6, 7, 8 |
| **D2** | **Negative-lag diagnostic, required output.** Count of pairs whose first S2 watch precedes `T0`, split by which term of the `max()` binds. Counts only, to `artifacts/`. | Section 5 |
| **D3** | **Resumption-rate diagnostic, required output.** See below. Counts only, to `artifacts/`. | Sections 7, 10.0 |
| **D4** | **S3-without-S2 is a reported bound at Step 9**, alongside the liveness bound. Not a Step 13 arm, not conditional on a trigger. | Section 10.0, handoff in Section 9 |
| **D5** | **The Step 9 91-day arm is re-anchored on `max(S2_premiere_date, first-pass S1 completion)`**, not the finale, because Netflix's window runs from release. | Section 10.0, handoff in Section 9 |
| **D6** | **The vacuous Step 8 invariant is replaced** by the three-part clock-start check now written into `task-sheet.md` Step 8. | Section 5 |
| **D7** | **Cadence is a required Step 9 stratum and a mandatory Step 12 candidate**; right-censoring removals are reported unconditionally with their direction named; Step 5 contamination exclusion runs before right-censoring. | Section 6 |

Cadence classification needs no new field: the Step 2 frame already carries S2 premiere date,
S2 finale date, and S2 episode count, so a show is weekly-release when the premiere-to-finale
span is on the order of `(L2 − 1) × 7` days and all-at-once when that span is near zero.

**D3, stated in full.** Symmetric in purpose to D2: D2 measures what the clock's *start*
hides, D3 measures what the window's *close* hides.

> Of user-show pairs scored **Started and left** at `T1`, report: **(i)** the share with any
> further distinct S2 episode watched after `T1` and before the pull date, and **(ii)** the
> share satisfying the Continued condition — `F2 ∈ A` and `|A| ≥ ceil(0.90 × L2)` — at **any**
> time before the pull date. Counts and shares only, to `artifacts/`.

This is the measurement of the entry/exit asymmetry named in Section 7. Started-and-left is
scored inside `W` while S1 completion is scored over all time, so some unknown portion of that
group are slow finishers rather than abandoners. D3 makes the portion known instead of
arguable. A high (ii) would mean the primary headline's Started-and-left share is substantially
a window artifact, and that finding would have to reach the write-up whether or not it is
convenient.

**D4, stated in full.** A user-show pair with S3-or-later episodes logged but **no** S2
episodes at all is scored **Never started** by the rule in Section 7. That is literally true
and almost certainly a logging gap: watching S3 without S2 is rare behaviour, missing S2 rows
is not. It is a **known misclassification with a known direction** — it inflates the headline
category — so it is not a footnote and not a contingent Step 13 arm.

> **Step 9 reports it as a bound**, alongside the liveness bound: what the never-started share
> becomes when every S3-without-S2 pair is removed from that category. Counts and shares only.

Two bounds, two directions, both reported: the liveness bound moves the never-started share
**up** by treating inactivity-excluded users as decliners; the S3-without-S2 bound moves it
**down** by removing pairs that are probably logging artifacts. Reporting only the first would
present the study's uncertainty as if it ran one way.

**D5, and why it must be said out loud.** The 91-day arm exists to be commensurable with
Netflix's public window, which runs from **release**, so it is anchored on the premiere while
the primary headline is anchored on the finale. **The two are therefore not the same
measurement at two window lengths.** They sit on different origins, and for a weekly show the
origins differ by the whole airing span. Any presentation that lines them up as "our number"
versus "our number at Netflix's window" is misleading, and the difference between them mixes a
window-length effect with an origin effect that cannot be separated after the fact. `task-sheet.md`
requires this to be stated plainly at Step 9; it is recorded here so the requirement is visible
to whoever reads the definition rather than only to whoever reads Step 9.

### 10.1 Open questions, each with a recommendation

Four remain. **These are recommendations. The Human Lead decides them; I have adopted none of
them, and the document stands unapproved.**

| # | Question | My recommendation | Why, in one line |
| :--- | :--- | :--- | :--- |
| **1** | Continued boundary: S2 finale **plus** ≥ 90 percent, or finale alone? | **Finale plus 90 percent** | Finale-alone would score a user who watched 2 of 13 episodes and skipped to the end as having continued, which understates abandonment in the direction that flatters the headline. |
| **2** | How is W estimated when most started users have negative lags? | **Estimate W on binge-release shows only, then apply it to all shows** | On a binge show premiere and finale coincide, so every lag is a genuine post-availability delay and W is a property of viewer behaviour rather than of the frame's cadence mix. |
| **3** | Right-censoring at `T0 + max(W, 91) ≤ pull date`, or `T0 + W`? | **`max(W, 91)`** | It costs real users, not zero, but it is the only version under which the primary and the 91-day arm share a denominator — and D5 already makes those two hard enough to compare. |
| **4** | Trakt show merges and splits across the pair key `show.ids.trakt` | **Count at Step 8, build nothing yet** | Reconciliation logic written against an unmeasured problem is speculative; the count is nearly free and settles whether the problem exists. |

Detail where the one-liner is not enough:

**1. Continued boundary.** Drafted as **finale AND `|A| ≥ ceil(0.90 × L2)`**. *The symmetry
argument used in the first draft is withdrawn: it was false.* S1 completion is evaluated over
all time and S2 completion within `W` days, so the two tests share arithmetic but not
quantifiers, and matching the arithmetic does not make the rule symmetric (Section 7). Three
grounds that do hold:

- **Direction of the error.** Finale-alone admits the skip-to-finale viewer — someone who
  watched the premiere and the finale and nothing else — as Continued. That undercounts
  abandonment, which is the direction that makes the study's own headline look better. A rule
  should not fail toward its author's conclusion.
- **The cost is visible, not hidden.** The strict rule creates the `p = 1.0` residual, and
  Section 7 requires it reported as its own named category at Step 10. The lenient rule's
  cost, by contrast, is silently absorbed into Continued where no one can size it.
- **D3 covers the strict rule's real weakness.** The objection to finale-plus-90 is that it
  catches slow finishers; that is exactly what the resumption diagnostic measures, so the
  weakness is bounded by a reported number rather than by argument.

*Recommendation: keep finale plus 90 percent, report the `p = 1.0` residual by name, and read
it together with D3.* If D3 returns a high resumption share, revisit this boundary and the
value of W together, since they are the same problem seen from two ends.

**2. Estimating W under D1.** *The truncate-at-zero recommendation from the previous draft is
withdrawn.* Truncation maps every live weekly viewer to a point mass at zero, and the height
of that mass is set by how many weekly shows the frame happens to contain — so W would become
an artifact of the frame's cadence composition rather than a fact about viewers. Change the
show mix, change W, with no change in behaviour. That is not defensible out loud, which is the
bar Step 6 has to clear.

*Recommendation: estimate W on binge-release shows only, then apply the resulting W to all
shows.* On a binge show the premiere and finale coincide, so `T0` is the moment the whole
season became available, every lag is non-negative by construction, and the lag measures the
one thing W is supposed to capture: how long a viewer takes to start something that is sitting
there available. That is a clean estimation sample for a quantity that is then applied
uniformly.

What it costs, stated so it is not discovered later: it assumes the delay-to-start behaviour
of binge viewers transfers to weekly viewers, which is an assumption and not a finding. Two
things should accompany it — the binge-only and all-shows lag distributions plotted together
so the reader can see how different they are, and a Step 13 arm varying W over the range the
two distributions imply. Whether the binge-only estimation sample is large enough to support
the percentile is a question for Step 6 with the data in hand, not for Step 1.

**3. Right-censoring.** *The "expected cost is zero rows" claim from the previous draft is
withdrawn; it was false on this document's own definitions.* The frame caps the S2 finale but
not `S1_completion_date`, so censoring removes users who completed S1 recently — people who
found an old show lately, who are disproportionately likely to continue, and whose removal
pushes the never-started share up (Section 6). *Recommendation: still `max(W, 91)`*, because
the alternative computes the two headlines on different denominators on top of the different
origins D5 already introduces, and two differences at once cannot be attributed. The removal
count is reported unconditionally either way, with its direction named, and if it is large the
right response is to say so in the limits rather than to switch rules to shrink it.

**4. Show merges and splits.** The pair key is `show.ids.trakt`. If Trakt merged or split a
show's metadata between a user's watch and our pull, one user's viewing could key to two show
IDs and appear as two pairs. *Recommendation: count occurrences at Step 8 and report; write no
reconciliation logic until the count justifies it.* Expected volume is low, the count is nearly
free, and the cost of being wrong is bounded and visible in a reported number.

---

## 11. What this document does not do

- It does not set **W**. Step 6.
- It does not set the **liveness threshold** or the liveness rule. Step 7.
- It does not set the **contamination exclusion rule**. Step 5.
- It does not set the **filter order**. Step 8.
- It does not resolve the **four open questions in Section 10.1**. Each carries a
  recommendation from me and a decision from nobody.
- It does not adopt itself. Everything in Section 10.0 came from the Human Lead or from
  `task-sheet.md` and is recorded as theirs. Nothing downstream of this gate runs until the
  Human Lead approves this document in writing, and no approval is recorded by me.
