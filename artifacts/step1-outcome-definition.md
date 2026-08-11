# Step 1: Outcome Definition

**Owner:** Data Scientist (drafts) · **Mode:** GATE · **Reviewer:** Red Team (hold / proceed)
**Status:** **APPROVED — ADOPTED.** Written approval given by the Human Lead on **2026-08-10**,
in session, at the Step 1 gate. This document is now the operative definition. Steps downstream
of the Step 1 gate are unblocked; the four remaining gates (Steps 5, 6, 7, 8) are unaffected and
still bind.
**Date:** 2026-08-10 · **Revised four times, 2026-08-10:** Human Lead decisions, then the
authorized revision following Red Team's first HOLD, then the revision following the second,
then this revision following Red Team's **third HOLD**
**W is not set in this document.** No code was written or run to produce it.

> **Approval record — Human Lead decision, 2026-08-10.**
> **Step 1 is approved.** Approval covers this document as a whole, including the items that
> entered it as proposals: **D8, D9** (second revision, Section 10.0b) and **D10 through D13**
> (third revision, Section 10.0c). They are adopted; the "proposed and unadopted" framing that
> attached to them while the gate was open no longer applies.
> Two were adopted by name at approval: **`H = 91 days` (D10)** and **the D12 cadence
> thresholds** as proposed. **`pull_date` (D11)** is adopted in *form* only — its *value* is
> **deliberately deferred** until Step 4's schedule is known. That deferral is a decision, not
> an omission or an oversight: the constraint `pull_date ≤ earliest per-user fetch date` cannot
> be honoured by a value chosen before the pull is scheduled. Setting `pull_date` is a Human
> Lead act and no agent performs it.
> **Red Team returned HOLD on B2 and was overruled** — recorded as accepted risk in the table
> at the head of this document, with the objection, the ruling, and the reason.
> Approval was given by the Human Lead in writing in this session. No agent recorded it on its
> own authority, and no agent adopted its own proposal.
>
> **Post-approval addendum, 2026-08-10 — evidence only, no rule changed.** One finding was added
> to **Section 5** after approval, on Human Lead instruction: the probe profile's S1/S2 overlap
> **inverts** under the Section 2.2 dedup, from 41.31 days of overlap to 360.73 days of
> separation, making it a rewatch artifact and making definition (a) produce a **negative clock
> start** on a real profile. It is recorded as **strengthening the existing warrant** for
> first-pass completion and for the **D2** diagnostic. **No rule, threshold, definition or
> required output changed, and the gate remains approved.** Source:
> `artifacts/step0-history-endpoint-probe.md`. Any future edit that changes a *rule* reopens the
> gate; this one does not.

This document defines what is being measured, on one user-show pair, from episode-level
watch history alone. It fixes the population, the clock, the three outcome states, the
abandonment point, and every counting rule needed to compute them deterministically. It
does not set W, does not set the liveness threshold, and does not set the contamination
exclusion rule. Those are Steps 6, 7, and 5.

**Red Team returned HOLD three times. All three revisions were authorized in response.** Seven
settled items — Human Lead decisions and items already closed in `task-sheet.md` — are recorded
in Section 10.0 and incorporated into the body of the document rather than appended to it. Two
required outputs added by the second revision are in Section 10.0b; four added by this revision
are in Section 10.0c. **Two** open questions remain in Section 10.1 — question 2 was decided by
the Human Lead on 2026-08-10 as D14 — each carrying a
recommendation that the Human Lead decides.

**What the second HOLD changed.** Three blocking findings and five secondary ones. The
structural change was in **Sections 3, 4 and 7**: season membership is defined by the
season's **listed episode-number set**, not by the numeric range `1..F`. That single change is
what makes `|D1| ≤ L1`, `|A| ≤ L2` and `p ∈ (0, 1]` true by construction rather than by
assertion. Section 10.0b added the missing post-window diagnostic for the **Never started**
category, which is the one the study is named after.

**What the third HOLD changed.** Four blocking findings, all of them about objects this
document names but never made operational. In order of how much they move a number:

1. **A fixed post-window horizon `H` now exists (Section 6, D10).** The previous draft claimed
   right-censoring at `T0 + max(W, 91) ≤ pull date` guaranteed every retained pair 91 days of
   post-window observation. It does not: the guarantee is `max(W, 91) − W = max(0, 91 − W)`
   days, which is 61 at `W = 30` and **zero** at any `W ≥ 91`, and Step 6 has not run so this
   document cannot know which side of 91 `W` falls on. Worse, D3 and D8 measured "to the pull
   date" carry exposure that varies by a factor of six across the frame, so they were never
   rates at all. Both are now measured over a constant `H`.
2. **The window boundary is now a UTC-instant comparison (Section 2.4, D13).** "On or before
   `T1`" compared a full timestamp against a date and admitted two faithful implementations one
   day apart. This is the operator that assigns every outcome state and it feeds the
   dual-implementation diffs at Steps 8 and 9.
3. **`pull_date` is now a single global frozen cutoff (Section 0, D11).** Step 4 is a multi-day
   unattended pull, so per-user fetch date would make right-censoring user-dependent and the
   diagnostics non-comparable.
4. **The cadence classifier has numeric thresholds and is exhaustive (Section 10.0, D12).** "On
   the order of" and "near zero" are not thresholds, and they left hiatus and multi-drop seasons
   in neither bucket. The classifier gates the Step 6 estimation sample, a required Step 9
   stratum, and a mandatory Step 12 candidate; two isolated Step 6 instances reading the old
   sentence could legitimately have produced different `W`s.

Separately, **the Section 3.3 precondition is CLOSED**: the Step 0 probe
(`artifacts/step0-episode-listing-endpoint-probe.md`) confirms the listed episode-number set is
obtainable on the Client ID alone. Sections 3.3, 9 and 11 are updated. Two limits from that
probe are carried rather than overread, and Section 3 must **not** be read as "gaps handled."

**Claims from earlier drafts that are withdrawn as false, and one objection accepted as a
known risk. Each is marked where it appeared** rather than quietly deleted:

| Withdrawn or accepted claim | Where | Disposition |
| :--- | :--- | :--- |
| Entry and exit are symmetric | Section 7 | They are not — S1 completion is evaluated over all time, S2 completion within `W`. The asymmetry is now stated as a bias with a known direction, and D3 measures it. |
| Right-censoring costs zero rows | Sections 6, 10.1 Q3 | `S1_completion_date` is uncapped, so it removes recent S1 completers, who are disproportionately likely to continue. It moves the headline **up**. |
| Truncating negative lags at zero | 10.1 Q2 | W estimated on binge-release shows only, then applied to all. |
| `p ∈ (0, 1]` follows from `p = m / L2` | Section 7 | It does not when `F2 > L2`. |
| **Rank-based `p` is safe because out-of-set episodes are dropped upstream** | Section 7 (2nd draft) | **False.** The old drop rule dropped `number > F`, `number < 1`, and missing fields — an episode numbered *inside* `1..F` but *absent* from the listed set survived all three, which is exactly the numbering-gap case. Membership is now defined by **set**, so the drop rule does the work the claim assumed. Section 3. |
| **Liveness is a statement about the account** | Sections 0, 1, 9 (both drafts) | **Mis-scoped.** The evidence is account-wide, but the test is `activity after T0 + W` and `T0` is pair-specific, so the same account can be live for one show and not another. Liveness is a **pair-level** filter. Sections 0, 1, 9. |
| **Right-censoring at `T0 + max(W, 91)` guarantees 91 days of post-window observation** | Section 10.0b (3rd draft) | **False by subtraction.** The window closes at `T1 = T0 + W`, so the guarantee is `max(W, 91) − W = max(0, 91 − W)` days: 61 at `W = 30`, **zero** at `W ≥ 91`, and true as written only at `W = 0`. Replaced by an explicit horizon `H` declared in Section 6 (D10). |
| **D3 and D8 measured "to the pull date" are rates** | Section 10.0, 10.0b (3rd draft) | **They were exposure-weighted mixtures whose weight is show recency.** A 2016 title gets ~10 years of post-window observation, a title whose S2 finale aired 31 Dec 2024 gets ~18 months. Direction: **D8 systematically understates later-starting for recent titles, so "never" looks most true exactly where the frame is newest.** Replaced by a constant horizon `H` (D10). |
| **"On or before `T1`" is a single unambiguous operator** | Section 7 (2nd, 3rd drafts) | **Ambiguous by one day.** `T1` is a date and the canonical timestamp is a UTC instant; `date(watched_at) ≤ T1` and `watched_at ≤ T1T00:00:00Z` are both faithful readings of the old text and disagree on every evening watch. Replaced by the half-open instant interval in Section 2.4 (D13). |
| **"Pull date" needs no definition** | Sections 6, 10.0, 10.0b (all drafts) | **Undefined and load-bearing.** Step 4 fetches each user on a different day, so per-user fetch date makes right-censoring user-dependent and the diagnostics non-comparable, while a global cutoff is a different rule on a different population. Replaced by a single global frozen cutoff (D11, Section 0). |
| **A show is weekly when its span is "on the order of" `(L2 − 1) × 7` days and binge when it is "near zero"** | Section 10.0 (3rd draft) | **Not thresholds, and not exhaustive.** A weekly season with a mid-season hiatus, a two-episode premiere, or a two-per-week drop lands in neither bucket, and a required stratum with unassigned members gets silently pooled. Replaced by the five-bucket numeric classifier in Section 10.0 (D12). |
| **ACCEPTED RISK — not withdrawn: the liveness bound is inflated** | Section 10.0, Step 9 | **Objection (Red Team):** a pair that binged all of S2 inside `W` and then left Trakt is excluded by the Step 7 liveness filter as not-live, and the Step 9 bound then relabels every inactivity-excluded pair "never started" — so a demonstrable continuer is counted as a decliner and the bound is inflated. **Ruling (Human Lead): overruled, do not fix.** **Reason:** the liveness bound is deliberately worst-case. It is not an estimate and is not presented as one; it is the ceiling of the reported floor-and-ceiling pair, and its whole function is to answer "what if every excluded pair were a decliner." A bound that quietly reclassified the pairs it could explain away would no longer be a bound. The inflation is real, is in the direction the bound is built to run, and is stated wherever the bound appears. |

**One sourcing claim is corrected rather than withdrawn, and is now closed.** An early draft
said Step 0 had confirmed the season-length source; Step 0 had confirmed only that
`GET /shows/:id/seasons?extended=full` returns per-season **counts**, and a count is not a
list. The Step 0 episode-listing probe has since supplied the list. Section 3.3 records the
precondition as **CLOSED** and names the recommended endpoint variant.

---

## 0. Data source and what may not be used

**Source, decided by the Human Lead, 2026-08-10:** `GET /users/:id/history`, unfiltered, one
sweep per user. Each record carries `id`, `watched_at`, `action`, `type`, and for episodes an
`episode` object (`season`, `number`, `title`, `ids`) plus a `show` object.

This decision closes the blocking finding in `artifacts/step0-access-and-setup.md` §0, which
established that `/users/:id/watched/shows` returns a show-level aggregate with **no
per-episode timestamps** and therefore cannot support S1 completion, the abandonment point,
or distinct-episode counting. It is recorded in `decisions/`, and the Step 0 artifact and this
one agree. **"One sweep" is one logical pass, not one call:** the endpoint paginates at
roughly **64 pages per user at `limit=250`** on the probe profile, so Step 4 throughput is
estimated in pages.

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

  > **Amended 2026-08-11 by the Human Lead — `decisions/0012-sweep-completeness-rule.md`.**
  > **The requirement above is unchanged. The *test* for it has changed.** Completeness is judged
  > by **full `X-Pagination-Page-Count` coverage plus a residual within 2 percent** of
  > `X-Pagination-Item-Count`, not by exact equality with that header. The Step 4 pilot showed
  > `X-Pagination-Item-Count` is not an exact count of the records this endpoint returns: seven of
  > ten users mismatched, in **both** directions (−97 to +20), while page and item headers stayed
  > identical across every page and two different page sizes returned the identical record set. A
  > user outside the tolerance is **discarded and logged, never truncated**, and stays
  > distinguishable downstream the way `access_denied` does.
  >
  > **This is a rule change inside an approved gate artifact.** Per the approval record at the head
  > of this document, an edit that changes a rule reopens the gate; this one does. It is recorded as
  > a Human Lead amendment and **has not been put to Red Team.**
- **The endpoint mixes `type: episode` with `type: movie`.** For outcome measurement, only
  `type: episode` records belonging to the show in question are used. **Liveness (Step 7) draws
  on the whole sweep but is evaluated per pair.** Its *evidence* is not restricted to the show
  under study — other shows and movies count as logged activity. Its *test*, per Step 7, is
  activity after `T0 + W`, and `T0` is pair-specific (Section 6), so **liveness is a pair-level
  filter and the same account can be live for one show and not for another**. The previous
  draft called it "a statement about the account" in three places; that was wrong and is
  corrected here, in Section 1, and in Section 9, so the two isolated Step 7 instances do not
  diff on it. Whether the gap distribution is built on raw play events or on deduplicated
  episodes is **Step 7's analysis to run**, and Step 1 does not decide it.

**Timezone and granularity.** `watched_at` is ISO 8601 UTC. **Ordering is always on the full
UTC timestamp**; date reduction applies to clock arithmetic only — `T0`, `T1`, lags, and
gaps are whole numbers of days, because W is a number of days — and never to sequencing, so
the tiebreak in Section 2.2 fires only when two full timestamps are exactly equal.

**That ruling settles ordering and arithmetic. It does not settle the boundary test**, which
compares a full timestamp against a date — and that comparison is what assigns every outcome
state. **Section 2.4 defines it, once, as a UTC-instant comparison**, and Sections 6, 7 and
10.0b use no other form.

**The pull cutoff `pull_date` is a single global constant, not the day a given user was
fetched.** Step 4 is a multi-day unattended pull: each user's history is fetched on a
different day. An earlier draft used the phrase "pull date" without defining it, while
right-censoring (Section 6), D3, D8 and D9 all lean on it. Per-user fetch date is the wrong
object twice over — right-censoring would remove different pairs depending on the accident of
scheduling order, and a user fetched early would show an empty tail that a user fetched late
would not, which makes the diagnostics non-comparable across exactly the axis they are
supposed to be constant on.

> **D11.** `pull_date` is **one calendar date, fixed as a constant for the whole study**. It
> defines the frozen cutoff instant `τ_pull := pull_date at 00:00:00Z`. **Every record with
> `watched_at ≥ τ_pull` is discarded from every computation in this document, whether or not
> it was fetched.** No computation anywhere uses a per-user fetch date.
>
> **Constraint on its value:** `pull_date` must be **no later than the earliest per-user fetch
> date in the whole Step 4 sweep**. Otherwise a user fetched on day 1 is credited with an
> absence of activity that was never observed.
>
> **Who sets it:** the Human Lead, as a single declared value, once Step 4's schedule is
> known. Step 1 fixes the *form* of the constant and its constraint, not its value — Step 4 has
> not run.
>
> **Required in the waterfall:** the value of `pull_date`, the earliest and latest per-user
> fetch dates, and the count of records discarded for `watched_at ≥ τ_pull`. The last of those
> is the visible price of freezing the cutoff, and it is reported rather than absorbed.

**`first_aired` is UTC too, and that is not free.** Air dates enter this document through the
S2 finale date in `T0` (Section 6). Trakt's `first_aired` is a UTC instant. A US primetime
broadcast — 21:00 ET is 01:00 UTC the following day — therefore carries a **UTC date one day
after its US air date**. For most US weekly shows `T0`, and hence `T1`, is systematically **up
to one day late**. The effect is small against any plausible `W` of tens of days, but it is
**one-directional, not noise**: a later `T1` grants one extra day of the one-sided inclusion
test in Section 7, so it moves the never-started share marginally **down**. It is named rather
than corrected, because correcting it would require a per-show broadcast timezone that the
frame does not carry, and because a half-corrected mix of UTC and local dates would be worse
than a consistent one. **The rule is: air dates and `watched_at` are both reduced to UTC
calendar dates and compared on that basis. No local-timezone conversion is applied anywhere,
in either direction** — the viewer's own timezone is unknown and unknowable from this data.

---

## 1. Unit of analysis and population

**Unit:** one user, one show. One row per `(user, show.ids.trakt)` pair. A pair appears at
most once, no matter how many times either season was watched.

**Population for the headline:** pairs where the user **completed S1** by the rule in
Section 4, on a show in the Step 2 frame, surviving the Step 5 contamination exclusions and
the Step 7 liveness rule.

Filter order, sample size after each filter, and the invariant checks are Step 8's, not
this document's. What Step 1 fixes is *what each filter is testing*.

**Liveness is an eligibility filter, not an outcome state, and it operates on pairs.** Outcome
states are assigned only among pairs that pass it. It is **not** a filter on accounts: because
Step 7's test is activity after `T0 + W` and `T0` differs by show (Section 6), one account can
pass for a show whose window closed in 2021 and fail for a show whose window closed in 2024.
Any implementation that drops a *user* wholesale on a liveness test is doing something this
document does not define. This matters for Step 9: the bound is computed by moving the
inactivity-*excluded* **pairs** into "never started," which is only coherent because they were
never assigned a state in the first place. Phrases like "inactivity-excluded users" are
replaced throughout by "inactivity-excluded pairs"; the unit is the pair everywhere in this
document, without exception.

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

### 2.4 Instant boundaries: how a date bound becomes a timestamp test

**This rule was added under Red Team blocking finding B3 and it is the single most
consequential line in the document, because it is the operator that assigns every outcome
state and it feeds the dual-implementation diffs at Steps 8 and 9.**

The defect: `T1` is a **date** (`T0 + W` days, Section 6), the canonical timestamp (2.2) is a
full **UTC instant**, and Section 7 compared them with the words "on or before `T1`."
Section 0's ruling that date reduction applies to clock arithmetic and never to sequencing
covers neither object. So `watched_at = 2024-03-14T21:00:00Z` against `T1 = 2024-03-14` is
**included** under `date(watched_at) ≤ T1` and **excluded** under
`watched_at ≤ T1T00:00:00Z`, and both were faithful readings of the old text. Two isolated
implementations could differ on a large share of rows and neither would be wrong.

> **D13. Every date bound in this document is expanded to a UTC instant at midnight, and every
> membership test is a half-open interval on instants: closed on the left, open on the right.**
>
> Write `⟦d⟧` for the instant `d at 00:00:00Z`. Then:
>
> | Object | Instant form | Test |
> | :--- | :--- | :--- |
> | Clock start | `τ0 := ⟦T0⟧` | — |
> | Window close | `τ1 := τ0 + W × 24h` (identically `⟦T0 + W days⟧ = ⟦T1⟧`) | — |
> | In-window (Section 7, set `A`) | `(−∞, τ1)` — **no lower bound**, per the one-sided rule in Section 7 | **`watched_at < τ1`** |
> | Post-window horizon (D3, D8) | `[τ1, τ1 + H × 24h)` | **`τ1 ≤ watched_at < τ1 + H × 24h`** |
> | Right-censoring (Section 6) | — | **`τ0 + (max(W, 91) + H) × 24h ≤ τ_pull`** |
> | Frozen cutoff (Section 0) | `τ_pull := ⟦pull_date⟧` | **`watched_at < τ_pull`** |
>
> No other comparison form appears anywhere in this document, and no implementation of it may
> use one. In particular `date(watched_at) ≤ T1` is **withdrawn** and must not be written.

Four properties, stated because each of them is why this form was chosen:

- **The window is exactly `W` days long.** `[τ0, τ1)` spans `W × 24h`, so "a window of `W`
  days" means `W` days. The inclusive reading spans `W + 1` calendar days, which is a silent
  off-by-one against the number Step 6 derives and against every lag Step 6 measures.
- **The window and the horizon tile without gap or overlap.** `[…, τ1)` then `[τ1, τ1 + H×24h)`
  partition the timeline at `τ1`. Under any other convention an event at the boundary is
  either counted twice or lost, and D3 and D8 are precisely counts of events just past that
  boundary.
- **It is one comparison, and it is `<`.** No `≤` on a timestamp, no date casting, no
  `23:59:59` sentinel. A sentinel would reintroduce the ambiguity at sub-second precision,
  which Trakt timestamps do carry.
- **The direction of the change is named, as everything else here is.** Relative to the
  inclusive reading, this removes one calendar day from the window, which moves the
  never-started share marginally **up**. It runs opposite to — and is of the same magnitude as
  — the one-day UTC finale skew in Section 0, which moves it **down**. Neither is corrected
  against the other; both are stated. Both are small against any plausible `W` of tens of days.

**One further one-day effect follows from `τ0 := ⟦T0⟧` and is named here.** `T0` is a date, so
a user who completed S1 at 21:00 has a clock that opens at 00:00 the same day, up to 24 hours
before the completion instant. That grants marginally more window and moves the never-started
share **down**. It is not corrected, for the same reason as the finale skew: the alternative is
a mixed date/instant clock, and a consistent convention beats a half-corrected one.

---

## 3. Season membership: the listed episode-number set

This section was rewritten under Red Team findings F1 and F2. The previous version defined
season membership by the numeric **range** `1..F` and claimed a drop rule that did not drop
what it needed to. Membership is now defined by **set**, and the set now has a named source.

### 3.1 The primitive object is a set, not a count

Per show, per season, the primitive is:

| Symbol | Meaning |
| :--- | :--- |
| `E1` | the **listed episode-number set** for season 1: the set of `number` values of the episodes the source lists for season 1 |
| `L1` | the size of `E1` — the S1 episode count |
| `F1` | `max(E1)` — the S1 finale number |
| `E2`, `L2`, `F2` | the same three objects for season 2 |

`L` and `F` are both **derived from `E`**, in that order, and are never obtained
independently of it. That is the point: three numbers that could disagree are replaced by one
object they are both computed from, so disagreement is not representable.

**`F := L` is forbidden.** Setting the finale number equal to the episode count is exactly the
assumption that a numbering gap violates, and it is the assumption that produced the withdrawn
`p ∈ (0, 1]` claim. `F` is `max(E)`. It is not `L`, not `episode_count`, and not
`aired_episodes`. The single exception is the fallback in 3.3, which is a different rule
adopted knowingly and only by decision of the Human Lead.

**Never `show.aired_episodes`** from the history payload, for the reason in Section 0.

**Specials are season 0 and are excluded** from `E1`, `E2`, from the completion test, and from
the abandonment point. They still count as logged activity for liveness.

### 3.2 Membership rule, replacing the out-of-range rule

> **An episode record counts toward a season if and only if its `number` is a member of that
> season's listed set.** A record is **dropped** when its `season`/`number` is missing, or when
> `number ∉ E` for the season it claims.

This replaces the previous rule, which dropped only `number > F`, `number < 1`, and missing
fields. **That rule let through exactly the case the gap machinery existed for**: an episode
numbered inside `1..F` but absent from `E` passed all three tests and survived. Two things
broke as a result, and both are repaired by the set rule:

- `|D1|` and `|A|` were defined over the range and could **exceed** `L1` and `L2`, so the Step
  8 invariant that Section 3 claimed to make enforceable was not, and `ceil(0.90 × L2)` could
  be satisfied by episodes that are not in the season.
- `m = max(A)` need not have been listed, so the rank-based `p` could have an **empty**
  numerator and return `p = 0`, outside its own stated range.

Under the set rule, `D1 ⊆ E1` and `A ⊆ E2` by construction, therefore `|D1| ≤ L1`,
`|A| ≤ L2`, and `m ∈ E2` whenever `A ≠ ∅`. **Section 7's `p ∈ (0, 1]` now holds for the reason
it claims.**

**Honest note on the Step 8 invariant.** Because `|D| ≤ L` is now true by construction, the
invariant "distinct episodes never exceed season length" no longer tests the data — it tests
the **implementation**. It fails only if an implementation filtered by range instead of by set,
which is precisely the bug this revision exists to prevent, so it is worth keeping and worth
describing accurately. It is a code check, not a data check. The data check is the drop count
below.

### 3.3 Where `E` comes from — the precondition, now CLOSED

**Status: CLOSED.** The previous draft carried this as a blocker: `E` had no confirmed source,
and everything in Sections 3, 4 and 7 depends on it. Step 2 collects episode **counts**, and a
count is not a list. That has since been tested — see
**`artifacts/step0-episode-listing-endpoint-probe.md`** — and the answer is yes on the Client
ID alone.

> **Requirement, unchanged.** `E1` and `E2` must be supplied as a **listed episode-number set
> per season**, and `E`, `L` and `F` must all be derived from **that same payload, for that
> show, from that pull**, so they cannot disagree with each other.
>
> **Precondition, CLOSED.** The probe called both candidate variants live with the Client ID
> and no OAuth and got **HTTP 200 on both**. Every episode object carries an integer `number`
> and an integer `season`, so `E` is read directly and `L := |E|`, `F := max(E)` follow from
> that one list.
>
> **Recommended variant, from the probe:
> `GET /shows/:id/seasons?extended=episodes,full`.** One call per show covers both seasons, and
> it is the only variant that returns season-level `episode_count` and `aired_episodes` **on the
> same payload as the episode list**, which is what makes the 3.4 disagreement check possible
> without a second source. `GET /shows/:id/seasons/:season` costs two calls per show for the
> same information minus the counts. The probe also records: **no pagination headers on any
> variant** (a paginated helper will raise), and **season 0 is returned and must be filtered**
> before `E` is built, per 3.1.
>
> Whether the set is added as a required Step 2 field or pulled separately remains the **Human
> Lead's** call, since Step 2 is theirs. Step 1 states the requirement, not the plan.

**Two limits from the probe, carried rather than overread.**

1. **The gap hypothesis remains UNTESTED, and Section 3 must not be read as "gaps handled."**
   The probe covered **one show with contiguous numbering**. It confirms the *shape* of the
   payload and the *auth*; it does not confirm how Trakt represents a numbering gap. The set
   machinery in 3.1 and 3.2 is correct **if and only if** Trakt represents a gap by **omitting
   the missing number from the listed set**. If Trakt instead lists a **placeholder episode
   object** at that number, the number is a member of `E`, the drop rule readmits exactly the
   case the set rule was built to exclude, and `L := |E|` counts an episode that does not
   exist. That is not an auth question and cannot be settled by another probe call on a
   contiguous show. **It is settled by finding an in-frame show with a known numbering gap and
   inspecting its payload**, which belongs wherever `E` is first pulled at scale, and it must be
   reported. Until then, what Section 3 buys is that `D1 ⊆ E1` and `A ⊆ E2` **relative to
   whatever `E` Trakt lists** — a real and sufficient guarantee for the invariants in 3.2 and
   for `p ∈ (0, 1]`, and **not** a claim that gapped seasons are measured correctly.
2. **Listed can exceed aired.** See 3.4, which the probe changed materially.

**Fallback, retained but no longer the auth contingency.** `E := {1, …, L}`, i.e. `F := L`, with
the write-up stating that numbering gaps are unhandled and the gap machinery deleted. It is no
longer reachable by an auth failure. It remains written down for the case where a specific
show's payload returns no episode list, and it is adopted — per show or at all — only by the
Human Lead. **It is not assumed here and must not be implemented pre-emptively.**

### 3.4 What gets counted when records are dropped

Two counts, not one. The previous draft required only the first.

1. **Per show:** the number of dropped episode records, and the number of distinct dropped
   `(season, number)` pairs. A show with many drops has a stale or wrong `E`, and that is what
   this count exists to reveal.
2. **Per outcome, and this is the one that was missing:** the number of **pairs whose entire S2
   evidence was dropped** — pairs with at least one dropped S2 record and `|A| = 0` after the
   drop rule. Counting drops per show hides the consequence that matters. If a show's `E2` is
   stale-low, a user's only S2 evidence is dropped and **the pair scores Never started**: a
   metadata error lands directly in the headline category. Reported as a count and as a share of
   the Never started group, with its direction named — it **inflates** Never started, the same
   direction as D4 and D9.

Shows where the source's `episode_count`, its `aired_episodes`, and `|E|` disagree for S1 or S2
are flagged and counted. `L := |E|` is what this document uses regardless.

**Third, and this is a direction the previous draft failed to name.** That draft said all three
counts "should agree" for in-frame seasons, on the reasoning that the frame caps S2 at 31 Dec
2024. **That is an expectation derived from the frame, not a verified property of the data, and
the probe found the opposite on the first show it tried.** Season 0 of the probe show returned
`episode_count = 10`, `aired_episodes = 8`, `|E| = 10` — **the listed set exceeded the aired
set by two.** Specials are excluded from `E` (3.1), so that particular case does not reach the
population, but it establishes that Trakt lists unaired episodes in the same array as aired
ones, on an ordinary show, with nothing in the payload marking them apart other than the count
mismatch. Nothing makes S1 or S2 immune.

The consequence is mechanical, because 3.1 fixes `L := |E|` regardless:

- **A listed-but-unaired episode inside S1 raises `L1`, which tightens `ceil(0.90 × L1)`.** A
  user who watched every episode that exists can then fail the completion test. **The population
  shrinks, and it shrinks specifically on shows with messy metadata** — not at random. The
  direction on the headline is not signed here, because who is removed depends on the show; the
  **size** of the removal is reported and the non-randomness is stated in the limits.
- **A listed-but-unaired episode inside S2 raises `L2`, which tightens `ceil(0.90 × L2)`.** That
  direction *is* signed: pairs that would have been **Continued** are pushed into **Started and
  left**, so it **overstates abandonment**. `F2 = max(E2)` may also be an episode that never
  aired, in which case `F2 ∈ A` is unsatisfiable and **no pair on that show can ever score
  Continued**.

> **Required, therefore, and not merely "flagged":** the count of in-frame shows where
> `episode_count`, `aired_episodes` and `|E|` disagree for S1 or for S2; the count of **pairs**
> on those shows; and, separately, the count of shows where `aired_episodes < |E|` for S2,
> which is the subset where Continued may be unreachable. The check is one comparison on a
> payload already being fetched (3.3), so there is no cost argument for skipping it.

---

## 4. S1 completion

> **Season 1 counts as complete when the user watched the S1 finale AND at least 90 percent
> of S1 episodes.**

Made exact:

- Let `D1` = the set of **distinct** S1 episodes for that user and show **whose number is a
  member of `E1`**, per Sections 2.1 and 3.2. Membership is by **set**, not by the range
  `1..F1`; the range form was the F1 defect and is withdrawn.
- **Required:** `F1 ∈ D1` **and** `|D1| ≥ ceil(0.90 × L1)`.
- `D1 ⊆ E1` by construction, so `|D1| ≤ L1` and the 90 percent test cannot be satisfied by
  episodes that are not in the season.

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

> **The overlap inverts under dedup, and that is the sharper finding.** Added 2026-08-10 from
> `artifacts/step0-history-endpoint-probe.md`, which made this run reproducible. **This
> strengthens the existing warrant for first-pass completion and for the D2 negative-lag
> diagnostic. It is not a new decision, it changes no rule, and the gate remains approved.**
>
> The six-week overlap is computed over **all S1 play records** — which is definition (a)
> below, the definition this section argues against. Recomputed on the same profile after the
> Section 2.2 earliest-per-distinct-episode collapse, the comparison reverses: **the first S2
> watch *follows* the last S1 watch by 360.73 days.** Precisely: 41.31 days of overlap under
> (a), 360.73 days of separation under (b).
>
> So the overlap is **entirely a rewatch artifact**. It is not evidence that this viewer watched
> S2 out of order; it is evidence that the last-observed timestamp is measuring a rewatch. That
> distinction is the whole argument of this section, and it is now observed rather than
> asserted.
>
> **What it costs to get wrong, on a real profile rather than a hypothetical.** Under definition
> (a) this profile's S1 completion date lands *after* its first S2 watch, so the clock start it
> produces is later than the event the clock is meant to time — **a negative clock start on a
> real, non-hypothetical profile.** The Step 8 clock-start invariant (D6) catches it, and D2
> counts pairs in this condition as a required output. This profile is one such pair, and it is
> the first observed instance of the failure D2 exists to measure.
>
> **Scope, stated so this is not overread.** One profile, one show. It establishes that the
> failure mode is real and reachable, not how common it is — that is what D2's count is for.

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

**A third way, now observed rather than argued.** On the probe profile definition (a) is not
merely biased, it is **arithmetically impossible**: it places the S1 completion date 360.73 days
after the first S2 watch, so the clock starts after the event it exists to time. See the box at
the head of this section. An argument about bias can be traded off against something; a clock
start that runs backwards cannot.

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

**Both terms are UTC calendar dates and the finale term carries a known one-day skew.** Trakt's
`first_aired` is a UTC instant, so a US primetime finale dates one day later in UTC than in its
broadcast market (Section 0). For most US weekly shows `T0` and `T1` are therefore up to one
day late, which grants one extra day of the one-sided test in Section 7 and moves the
never-started share marginally **down**. Small against a `W` of tens of days, one-directional,
and named here rather than corrected, because the frame carries no per-show broadcast timezone
and a partial correction would be worse than a consistent convention.

The window closes at **`T1 = T0 + W days`**, evaluated as the instant `τ1 = ⟦T0⟧ + W × 24h`
with the half-open test in Section 2.4 — the window is `[⟦T0⟧, τ1)` and is exactly `W` days
long. W is set in Step 6 and is not set here.

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
  weighted average over the frame's cadence mix, so it moves if the mix moves. **Every bucket
  of the D12 classifier is reported separately alongside it** — all five, not just weekly and
  binge — with intervals, so a reader can see how much of any difference is exposure.
- **Cadence is a mandatory entry on the Step 12 candidate list**, alongside origin, gap
  length, S1 episode count, and user tenure — and it is the one candidate with a known
  mechanical driver, which must be said when its result is reported so a mechanical artifact
  is not read as an audience finding.

The classification itself is **D12 in Section 10.0**, with numeric thresholds and an exhaustive
bucket list. The previous draft described it in two words — "on the order of" and "near zero" —
which were not thresholds and left hiatus and multi-drop seasons unassigned.

D1 is still the right call: premiere anchoring has the opposite and worse defect, scoring a
user who waits for a full season as a decliner, and it puts Continued out of reach inside W.
The exposure asymmetry is the price, and it is paid openly by stratifying rather than by
hoping the pooled number is fair.

### The post-window horizon `H`, and right-censoring

**A pair whose window has not closed by the pull cutoff cannot be classified.** That is the
first job of right-censoring. The second job — added here under Red Team blocking finding B1 —
is to guarantee a **constant amount of observation after the window closes**, because D3 and D8
are measured there.

**The previous draft's guarantee was false.** It asserted that `T0 + max(W, 91) ≤ pull date`
gives every retained pair at least 91 days of post-window observation. Do the subtraction: the
window closes at `T1 = T0 + W`, so the guaranteed post-window observation is
`max(W, 91) − W = max(0, 91 − W)` days. That is 61 days at `W = 30`, **zero at `W = 91`, and
zero at every `W > 91`**. The sentence is true only at `W = 0`, and **Step 6 has not run, so
this document cannot know which side of 91 `W` lands on.**

**The larger problem is exposure, not arithmetic.** D3 and D8 were both defined as "any further
S2 episode watched after `T1` and before the pull date." That denominator is not constant. A
pair on a 2016 show gets roughly ten years of post-window observation; a pair on a show whose
S2 finale aired 31 Dec 2024 gets roughly eighteen months. **Pooled, D3 and D8 were not rates —
they were exposure-weighted mixtures whose weight is show recency.** The direction matters and
is bad: **D8 systematically understates later-starting for recent titles, so "never" looks most
true exactly where the frame is newest**, which is exactly where the public argument is loudest.

> **D10. A fixed post-window horizon `H` is declared here: `H = 91 days`.**
>
> **Right-censoring rule:** retain a pair only if
> **`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`**, with `τ_pull` the frozen cutoff from Section 0
> and the comparison per Section 2.4.
>
> **D3 and D8 are measured over `[τ1, τ1 + H × 24h)` — the `H` days immediately following the
> window close — and never "to the pull date."** Exposure is then constant across every
> retained pair and the shares are rates that can be compared across shows and pooled.

**Why the rule takes that form.** Two requirements conjoin. B1 requires `T0 + W + H ≤ pull` so
the horizon is fully observed. Open question 3 requires `T0 + max(W, 91) ≤ pull` so the primary
headline and the 91-day arm share a population — an argument this revision does not disturb.
The 91-day arm reports the same diagnostics, so its close needs `H` behind it too. Taking the
conjunction and giving both closes their horizon gives `max(W, 91) + H`. The guarantee sentence
is now true by construction rather than decoratively: **every retained pair has exactly `H`
observed days after `T1`, at any `W`.**

**And it covers the 91-day arm too, which is worth one line of arithmetic rather than an
assumption.** The arm is premiere-anchored (D5): `T0' = max(S2_premiere, S1_completion)`. Since
the premiere never falls after the finale, `T0' ≤ T0`, so
`T0' + 91 + H ≤ T0 + 91 + H ≤ T0 + max(W, 91) + H ≤ pull_date`. The arm's window close and its
`H` days of horizon are both inside observed time for every pair the primary headline retains,
which is the same population — as open question 3 requires.

**Why `H = 91`.** It is the same quarter as the Netflix reporting window the Step 9 arm exists
to be commensurable with, so "how many of the 'never started' started within a quarter of the
window closing" is a question with an existing public meaning rather than an arbitrary one. It
is declared **here, before Step 6 runs, and is not a function of `W`** — which is the property
that makes it a fixed horizon rather than a second free parameter. Step 13 may vary `W`; `H` is
held constant across those arms, or D3 and D8 stop being comparable between them.

**What `H` costs in retained rows, relative to the previous rule.** The requirement moves from
`max(W, 91)` days of clearance to `max(W, 91) + 91`. The cost falls **entirely on the
`S1_completion_date` term of `T0`**, not on the show term: the frame caps the S2 finale at
31 Dec 2024, and 31 Dec 2024 plus 182 days is mid-2025, comfortably inside any 2026 pull, so no
show is lost. What is lost is pairs whose **first-pass S1 completion date falls in the `H`-day
band immediately before the old cutoff** — roughly, the most recent 91 days of S1 completions
that the previous rule would have kept. In a pull dated around Aug 2026 and `W ≤ 91`, that moves
the effective S1-completion cutoff from about May 2026 to about Feb 2026.

**And it costs them in the flattering direction, which is why the count is not optional.** These
are the same people right-censoring already removes and for the same reason: recent S1
completers, who found an old show lately, have the whole series available, and are
disproportionately likely to roll straight into S2. **Removing more of them moves the
never-started share further up.**

> **Required in the Step 8 waterfall:** the right-censoring removal reported as **two lines, not
> one** — pairs removed by the `max(W, 91)` term, and the **incremental** pairs removed by the
> `+ H` term — each with the upward direction of its effect named on the same line. A single
> combined figure would hide the price of `H` inside a removal that predates it.

**Right-censoring is not a free guard, and an earlier draft of this document was wrong to call
it one.**
The frame caps the S2 finale at 31 Dec 2024, but `S1_completion_date` is **uncapped** — a
user can finish S1 of a 2019 show in 2026. Since `T0 = max(...)`, those users have a `T0`
near `τ_pull` and are removed by right-censoring. They are not a random slice:

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
   in the same line — and split into the `max(W, 91)` term and the incremental `+ H` term, per
   D10 above.
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

Measured at the window close `τ1`, from distinct S2 episodes only.

Let `A` = the set of **distinct** S2 episodes for that user and show **whose number is a member
of `E2`** (Section 3.2), whose canonical timestamp (2.2) satisfies **`watched_at < τ1`**, where
`τ1 = ⟦T0⟧ + W × 24h` is the window-close **instant** defined in Section 2.4. Let
`m = max(A)` when `A` is non-empty.

**The phrase "on or before `T1`" from earlier drafts is withdrawn and must not be reinstated.**
`T1` is a date and `watched_at` is a UTC instant, so that phrase admitted two faithful and
incompatible implementations one day apart — `date(watched_at) ≤ T1` and
`watched_at ≤ T1T00:00:00Z` — on the one operator that assigns every row's outcome state and
feeds the dual-implementation diffs at Steps 8 and 9. **The test is `watched_at < τ1`. It is a
strict inequality between two instants, it is stated once in Section 2.4, and the same
convention governs D3, D8 and right-censoring so no second reading survives anywhere.** Membership is by **set**, not by the range `1..F2`; the
range form was the F1 defect and is withdrawn. `A ⊆ E2` by construction, so `|A| ≤ L2` and
`m ∈ E2`.

| State | Condition |
| :--- | :--- |
| **Never started** | `\|A\| = 0` |
| **Continued** | `\|A\| ≥ 1` **and** `F2 ∈ A` **and** `\|A\| ≥ ceil(0.90 × L2)` |
| **Started and left** | `\|A\| ≥ 1` **and not** the Continued condition |

**Mutually exclusive and exhaustive by construction.** The partition is
`A = ∅` / `(A ≠ ∅ ∧ C)` / `(A ≠ ∅ ∧ ¬C)`, so no eligible pair can fall in two states or in
none. This is what satisfies the Step 8 invariant that the states sum to the sample. It holds
for any well-defined `A`, and Section 3.2 is what makes `A` well-defined.

### The degenerate case: `L2 = 1`

**Stated here rather than pushed to the frame, because Step 2 is the Human Lead's and Step 1
does not add filters to it.** When `L2 = 1`, `E2 = {F2}` and `ceil(0.90 × 1) = 1`, so
`|A| ≥ 1 ⟺ F2 ∈ A ⟺` the Continued condition. **Continued becomes equivalent to Started,
Started-and-left is empty by construction, and `p` — defined only on Started-and-left — is
never defined.** The three-state partition degenerates to two, and a two-state row cannot
contribute to a headline that splits started-and-left from continued.

> **Rule: pairs on shows with `L2 = 1` are excluded from the headline population at Step 8, and
> the count of shows and of pairs excluded is reported in the waterfall.**

`L1 = 1` is not degenerate in the same way — completion is simply "watched the one episode" —
and such pairs are retained. Small `L2` is not excluded either, but it is coarse: at `L2 = 2`,
`ceil(0.90 × 2) = 2`, so Started-and-left is exactly "watched one of the two," and `p` takes
one of two values. **Step 10 must not read a `p` histogram across shows with very different
`L2` as if the bins were comparable**; that is a presentation constraint on the abandonment
distribution, and it follows from `p` being a fraction of a season, not a count of episodes.

Three properties worth stating:

- **The bound is one-sided, and under finale anchoring that is load-bearing.** The interval
  `(−∞, τ1)` has no lower bound, so a user who watched S2 episodes *before* their clock started is
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

> `p = |{ e ∈ E2 : e ≤ m }| / L2`

That is, the position of the highest watched episode within the season's actual episode list,
over the length of that list. Both numerator and denominator count listed episodes, so
`p ∈ (0, 1]`.

**The second draft justified that range with a false premise, and Red Team was right to hold on
it.** It claimed episodes outside the listed set were "already dropped upstream by the
out-of-range rule in Section 3." They were not: the old rule dropped `number > F2`,
`number < 1`, and missing fields, and a number inside `1..F2` but absent from `E2` — the
numbering-gap case the fix existed for — passed all three. So `m` need not have been listed; if
`E2` began above `m`, the numerator was **0** and `p = 0`, outside the stated range.

**What actually secures the range is the set-membership rule in Section 3.2**, adopted in this
revision: `A ⊆ E2`, therefore `m ∈ E2`, therefore `m` itself is in the numerator set and the
numerator is at least 1; and the numerator counts a subset of `E2`, so it is at most `L2`.
`p ∈ (0, 1]` **now holds by construction, for the reason claimed.** Under the 3.3 fallback,
where `E2 := {1, …, L2}`, this reduces to `m / L2` and the range holds by the contiguity
assumption that the fallback explicitly labels as unhandled.

For a contiguously numbered season — which is nearly all of them — the rank form is identical
to `m / L2`, so the fix changes no ordinary case and closes the pathological one. Defined
**only for the Started-and-left group**, computed on distinct episodes so a rewatch cannot move
it.

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

**Their treatment in the Step 6 lag distribution was a separate question. It is now DECIDED as
D14** (Human Lead, 2026-08-10; formerly open question 2). Step 6 restricts to users who did
start S2 and plots the lag from clock start to first S2 episode; for this group that lag is
**negative**, and after D1 the negative mass is not a tail — for a weekly show it is most of the
started population. That is why the question was never "what do we do with the negatives" but
"which shows can W honestly be estimated on at all," and the answer adopted is the **C1-only**
estimation sample (D12) rather than any repair applied to the negatives. W must be defensible
out loud, and a number whose value depends on the frame's cadence mix is not.

**D14 removes the negatives from the *estimation* sample only, and that is not the whole
problem.** `task-sheet.md` Step 6 also requires the **all-shows** lag distribution to be plotted
alongside the C1-only one, so the transfer assumption is visible. That all-shows plot still
carries the negative mass. Step 6 is a **dual-implementation gate**, and Step 13's required
W range is defined off that same plot, so two instances treating the negatives differently would
diverge and the divergence would propagate into the tested range. **`task-sheet.md` Step 6
therefore carries an explicit rule for the all-shows plot; it is Step 6's spec, not Step 1's, and
this document takes no position on it beyond recording that the gap was real.**

---

## 9. What this definition hands to later steps

Recorded here so nothing is reconstructed later from memory.

- **The `E` precondition is CLOSED.** The listed episode-number set is obtainable on the Client
  ID alone; see `artifacts/step0-episode-listing-endpoint-probe.md`. The recommended variant is
  **`GET /shows/:id/seasons?extended=episodes,full`**, which returns `E` and the season-level
  counts on one payload, one call per show. `L`, `F`, `p` and the 90 percent test are computable
  as defined, and the labelled fallback is no longer an auth contingency. **Two limits travel
  with this:** the probe covered one show with contiguous numbering, so **the gap hypothesis —
  that Trakt represents a numbering gap by omitting the number rather than listing a placeholder
  — is UNTESTED, and Section 3 must not be read as "gaps handled"**; and **listed can exceed
  aired** (Section 3.4), which shrinks the population on shows with messy metadata. Whether `E`
  becomes a Step 2 field remains the Human Lead's.
- **One value is still needed from the Human Lead, and it is not Step 1's to set:** the value of
  the global frozen cutoff `pull_date` (D11), **deliberately deferred** until Step 4's schedule
  is known. `H = 91 days` (D10) and the D12 cadence thresholds were **approved by name** at the
  Step 1 gate on 2026-08-10 and are no longer outstanding.
- **Step 5** receives: `action` is not filtered on at Step 1, so manual and imported
  timestamps are still in the data when Step 5 runs, which is the correct order. Step 5's
  exclusion must also be applied **before** right-censoring, so an import-stamped S1 completion
  date is counted as contamination rather than laundered into a censoring drop (Section 6).
- **Step 6** receives: `T0` anchored on the S2 finale per D1 (Section 6), the first-S2-watch
  date on distinct episodes, and the **D12 cadence classifier**, which under **D14 (Human Lead,
  2026-08-10) *is* the estimation sample** — bucket **C1 only**, applied as written rather than
  paraphrased, with the resulting W applied to all shows. **This is no longer an open question;
  it is decided, and `task-sheet.md` Step 6 carries it**, so both isolated instances receive it
  from the file they read rather than from this document. The negative-lag question that
  travelled with it is closed by the same decision: on a C1 show premiere and finale coincide,
  so every lag in the estimation sample is non-negative by construction and there is nothing to
  truncate. Because `T0` and the Step 6 lag now share the same origin, W is derived and applied
  against one clock rather than two.
- **Step 7** receives, and this is the corrected version: liveness **evidence** is account-wide
  — the whole sweep, other shows and movies included, **not** restricted to the show under
  study — but the liveness **test** is `T0 + W`-relative and `T0` is pair-specific, so
  **liveness is a pair-level filter**. One account can be live for one show and not for another.
  The earlier "statement about the account" phrasing is withdrawn (Sections 0, 1). Where Step 7's
  rule says "after clock start plus W," the boundary it means is the instant `τ1` of Section 2.4,
  tested as `watched_at ≥ τ1` — the complement of the in-window test, so no event falls on both
  sides or neither.
  **Both isolated Step 7 instances receive the pair-level wording.** This is now a claim of fact
  and the repo backs it: the Human Lead has amended `task-sheet.md` Step 7, which is the file the
  two isolated instances actually read, so that the rule is written on a **user-show pair**, the
  account-wide-evidence / pair-specific-test distinction is stated there, and dropping a user
  wholesale on a liveness test is explicitly forbidden. `task-sheet.md` Step 9's bound is likewise
  now written over inactivity-excluded **pairs**, not users. The pair-level scoping therefore no
  longer reaches the instances only through this document, and a divergence on scope between them
  would be a **bug rather than a spec ambiguity**. An earlier draft of this section asserted the
  same claim while the task sheet still said "user"; that assertion was unbacked when made and was
  withdrawn, and it is restated here only because the underlying file changed.
  Whether the gap distribution is built on raw play events or
  on deduplicated episodes remains Step 7's analysis to run; Step 1 takes no position.
- **Step 8** receives: the filter order is Step 8's, but these are its responsibility to
  enforce — the **set-membership** drop rule (Section 3.2), which is now an implementation check
  rather than a data check; **both** drop counts, per show and **per outcome**, the second being
  pairs whose entire S2 evidence was dropped (Section 3.4); exclusion and counting of `L2 = 1`
  shows (Section 7); the **required** negative-lag report split by binding term (D2); the
  **required** resumption-rate report (D3); the **required** never-started post-window
  diagnostic (D8, Section 10.0b); the **required** split-artifact counts (D9, Section 10.0b);
  the right-censoring removal reported as **two lines** — the `max(W, 91)` term and the
  **incremental `+ H` term** — each with its upward direction named (D10, Section 6); the
  ordering constraint that Step 5 contamination exclusion runs *before* right-censoring
  (Section 6); `pull_date`, the earliest and latest per-user fetch dates, and the count of
  records discarded for `watched_at ≥ τ_pull` (D11, Section 0); **per-bucket show and pair
  counts for all five D12 cadence buckets** plus the count of shows within 1 day of a bucket
  boundary (Section 10.0); the **metadata-disagreement counts** of Section 3.4, including the
  subset where `aired_episodes < |E|` for S2; and
  retention of `action` as a column. The three-part clock-start invariant in `task-sheet.md`
  should compute the first-pass S1 completion date **independently**, not read back the
  pipeline's value, or its equality clause proves nothing (Section 5). Every boundary test is
  the half-open instant form of Section 2.4; `date(watched_at) ≤ T1` must not appear anywhere
  in the implementation.
- **Step 9** receives: the cadence stratum requirement, now **all five D12 buckets reported
  separately** (Section 6, Section 10.0); the S3-without-S2 bound
  (D4) and the **split-artifact bound (D9)** reported alongside the liveness bound, with the
  liveness bound's inflation recorded as an **accepted risk** by Human Lead ruling rather than
  repaired; the
  **never-started post-window diagnostic (D8)** measured over the fixed horizon `H` and not to
  the pull date, which moves the headline **down** and must be
  reported with the bounds that move it up; and the 91-day arm's separate origin (D5), which
  must be stated in the write-up and not smoothed over. Both the primary and the 91-day arm run
  on the same right-censored population, `max(W, 91) + H` (D10).
- **Step 10** receives: `p` is a fraction of a season, so bins are not comparable across shows
  with very different `L2` (Section 7); the `p = 1.0` residual is its own named category and is
  not merged into "near-finale."
- **Step 12** receives: cadence as a mandatory candidate on the list, **classified by D12 into
  five buckets rather than two**, and flagged as the one
  candidate with a known mechanical driver (Section 6).
- **Step 13** receives two required robustness arms from this document, in addition to the
  ones already in its own step: **(i)** S1 completion date as last-observed rather than
  first-pass, per Section 5; **(ii)** an `action`-type arm excluding `checkin`-only and
  manual-`watch`-only evidence, per Section 2.3. Both exist because a permissive choice was
  made here and the permissiveness should be shown not to be load-bearing. **`H` is held
  constant across every arm that varies `W`** (D10) — otherwise D3 and D8 are not comparable
  between arms — and because the right-censoring rule contains `W`, **each `W` arm re-censors
  the population**, so the arms do not share a denominator and the retained-row count must be
  reported per arm.

---

## 10. Settled items, and open questions

### 10.0 Settled — decided by the Human Lead or already closed in `task-sheet.md`

None of these are mine to re-propose. All are incorporated into the body of this document.

| # | Settled item | Where it lands |
| :--- | :--- | :--- |
| **D1** | **Clock start is anchored on the S2 finale air date, not the S2 premiere.** `T0 = max(S2_finale_air_date, S1_completion_date)`. Rationale and cost in Section 6. Binge shows are unaffected. | Sections 6, 7, 8 |
| **D2** | **Negative-lag diagnostic, required output.** Count of pairs whose first S2 watch precedes `T0`, split by which term of the `max()` binds. Counts only, to `artifacts/`. **Warrant strengthened 2026-08-10, no change to the rule:** the probe profile's S1/S2 overlap inverts under the Section 2.2 dedup — 41.31 days of overlap on all play records, 360.73 days of separation on distinct episodes — so it is a rewatch artifact, and definition (a) would give that profile a **negative clock start**. First observed instance of the failure D2 counts. | Section 5 |
| **D3** | **Resumption-rate diagnostic, required output.** See below. Counts only, to `artifacts/`. | Sections 7, 10.0 |
| **D4** | **S3-without-S2 is a reported bound at Step 9**, alongside the liveness bound. Not a Step 13 arm, not conditional on a trigger. | Section 10.0, handoff in Section 9 |
| **D5** | **The Step 9 91-day arm is re-anchored on `max(S2_premiere_date, first-pass S1 completion)`**, not the finale, because Netflix's window runs from release. | Section 10.0, handoff in Section 9 |
| **D6** | **The vacuous Step 8 invariant is replaced** by the three-part clock-start check now written into `task-sheet.md` Step 8. | Section 5 |
| **D7** | **Cadence is a required Step 9 stratum and a mandatory Step 12 candidate**; right-censoring removals are reported unconditionally with their direction named; Step 5 contamination exclusion runs before right-censoring. | Section 6 |
| **D10** | **`H = 91 days` is adopted as the post-window horizon** (Human Lead, 2026-08-10, at approval). Right-censoring is `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`; D3 and D8 measure over `[τ1, τ1 + H)`. Proposed in Section 10.0c, adopted by name. | Sections 6, 10.0b, 10.0c |
| **D11** | **`pull_date` is a single global frozen cutoff** — adopted in **form**. Its **value is deliberately deferred** to Step 4's schedule (Human Lead, 2026-08-10). Not an omission: the constraint `pull_date ≤ earliest per-user fetch date` cannot be honoured by a value fixed before the pull is scheduled. | Section 0, 10.0c |
| **D12** | **The cadence classifier thresholds are adopted as proposed** (Human Lead, 2026-08-10, at approval): five exhaustive buckets `C0`–`C4`, numeric thresholds, first-match ordering. | Section 10.0, 10.0c |
| **D13** | **Half-open UTC-instant boundaries** (`watched_at < τ1`, applied identically to `A`, D3, D8 and right-censoring) are adopted with the document. | Section 2.4, 10.0c |
| **D14** | **Open question 2 is decided (Human Lead, 2026-08-10): W is estimated on bucket C1 (all-at-once) shows ONLY, per D12, and applied to all shows.** Estimation sample and application population differ deliberately. Two obligations travel with it, both now in `task-sheet.md`: Step 6 plots the C1-only and all-shows lag distributions together, and Step 13 varies W over at least the range those two imply. The transfer assumption — that binge viewers' delay-to-start behaviour carries to weekly viewers — is an assumption, not a finding, and is stated as such. | Section 10.1 Q2, `task-sheet.md` Steps 6 and 13 |
| **D15** | **The Step 4 source is `GET /users/:id/history`, unfiltered, one sweep per user** (Human Lead, 2026-08-10), closing the blocking finding in `artifacts/step0-access-and-setup.md` §0. "One sweep" is one logical pass, **not** one call: ~64 pages per user at `limit=250`. The sweep must be **complete** — truncation is indistinguishable from "never started." | Section 0, `artifacts/step0-access-and-setup.md` §0 and §6 |

**D12, the cadence classifier, stated as thresholds.** *The previous draft's version —
"weekly-release when the premiere-to-finale span is on the order of `(L2 − 1) × 7` days and
all-at-once when that span is near zero" — is withdrawn.* Those are not thresholds, and the
pair of them is not exhaustive: a weekly season with a mid-season hiatus, a two-episode
premiere, or a two-per-week drop lands in **neither** bucket. That is not a cosmetic gap. This
classifier gates the **Step 6 estimation sample** (open question 2 recommends estimating `W` on
binge shows only, which makes `W` itself a function of the classifier), a **required Step 9
stratum**, and a **mandatory Step 12 candidate** — and a required stratum with unassigned
members gets silently pooled into whichever bucket an implementation happens to prefer. Two
isolated Step 6 instances given the old sentence could legitimately produce different `W`s,
which would show up as a spurious dual-implementation divergence.

Classification still needs no new field. The Step 2 frame carries the S2 premiere date `P`, the
S2 finale date `F_d`, and `L2 = |E2|` from Section 3. Let

> `span := F_d − P`, in whole UTC calendar days (Section 0), and
> `weekly_span := (L2 − 1) × 7`.

> **Buckets are evaluated in the order listed, first match wins.** That ordering is part of the
> definition, not an implementation note: it is what makes the classification exhaustive **and**
> mutually exclusive even where bands would otherwise overlap at small `L2`.
>
> | # | Bucket | Condition | In the Step 6 estimation sample? |
> | :--- | :--- | :--- | :--- |
> | **C0** | **Unclassifiable** | `P`, `F_d` or `L2` missing, or `span < 0` | No |
> | **C1** | **All-at-once (binge)** | `span ≤ 1` | **Yes — and only this bucket** |
> | **C2** | **Weekly** | `abs(span − weekly_span) ≤ 3` | No |
> | **C3** | **Faster than weekly** | `1 < span < weekly_span − 3` | No |
> | **C4** | **Slower than weekly** | `span > weekly_span + 3` | No |
>
> **Every in-frame season lands in exactly one bucket.** C0 absorbs missing and impossible
> data; C1–C4 partition `span ≥ 0` given the first-match rule.

**What the extra buckets are for, named so they cannot be absorbed.** C3 is where a
two-episode premiere, a two-per-week drop, and a split-batch "part 1 / part 2" release land.
C4 is where a mid-season hiatus and irregular scheduling land. **Neither may be folded into C1
or C2**, because the exposure asymmetry that makes cadence a confound at all (Section 6) scales
with `span`, and C3 and C4 have `span` values that belong to neither of the two clean cases.
**C0, C1, C2, C3 and C4 are each reported as their own line** in the Step 8 waterfall (shows and
pairs) and in the Step 9 cadence stratum (headline with intervals). Where a bucket is too small
to support an interval, **report the count and say so** — do not pool it.

**The thresholds are conventions, and they are stated as such.** `span ≤ 1` rather than
`span = 0` for binge, because a same-day drop can straddle midnight UTC (Section 0). `± 3` days
for weekly, because it absorbs a mid-season change of broadcast day and the same one-day UTC
skew without reaching a full week's slip, which is a genuinely different release pattern.
**Required with the counts: the number of shows falling within 1 day of any bucket boundary**,
so the classifier's fragility is a visible number rather than an assumption. If that count is
large, the thresholds are load-bearing and Step 13 should carry an arm on them; if it is small,
they are not, and that is worth knowing before `W` is derived on top of them.

**D3, stated in full.** Symmetric in purpose to D2: D2 measures what the clock's *start*
hides, D3 measures what the window's *close* hides.

> Of user-show pairs scored **Started and left** at `τ1`, report: **(i)** the share with any
> further distinct S2 episode whose canonical timestamp falls in **`[τ1, τ1 + H × 24h)`** — the
> fixed horizon `H = 91 days` from D10 — and **(ii)** the share satisfying the Continued
> condition — `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)`, where `A_H` is the set `A` recomputed
> with the bound moved from `τ1` to `τ1 + H × 24h` — over that same horizon. Counts and shares
> only, to `artifacts/`.

**The horizon replaces "before the pull date," and that is a correction, not a tightening.**
Measured to the pull date, D3's denominator ran from eighteen months to ten years depending on
when the show aired, so the pooled figure was an exposure-weighted mixture rather than a rate
(Section 6, D10). Over a constant `H` it is a rate, comparable across shows and poolable. Right
censoring guarantees the horizon is fully observed for every retained pair.

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

**The liveness bound is a deliberate worst case, and that is recorded as an accepted risk
rather than argued here.** Red Team objected that it is inflated: a pair that binged all of S2
inside `W` and then left Trakt is excluded by the Step 7 liveness filter and then relabelled
"never started" by the bound. The Human Lead **overruled** the objection — the bound's function
is to answer "what if every excluded pair were a decliner," and a bound that reclassified the
pairs it could explain away would stop being a bound. The objection, the ruling and the reason
are in the accepted-claims table at the head of this document. The inflation is real, runs in
the direction the bound is built to run, and is stated wherever the bound appears.

Bounds in both directions, all reported: the liveness bound moves the never-started share
**up** by treating inactivity-excluded pairs as decliners; the S3-without-S2 bound (D4), the
split-artifact bound (D9), and the dropped-S2-evidence count (Section 3.4) all move it **down**
by removing pairs that are probably logging or metadata artifacts. Reporting only the first
would present the study's uncertainty as if it ran one way.

**D5, and why it must be said out loud.** The 91-day arm exists to be commensurable with
Netflix's public window, which runs from **release**, so it is anchored on the premiere while
the primary headline is anchored on the finale. **The two are therefore not the same
measurement at two window lengths.** They sit on different origins, and for a weekly show the
origins differ by the whole airing span. Any presentation that lines them up as "our number"
versus "our number at Netflix's window" is misleading, and the difference between them mixes a
window-length effect with an origin effect that cannot be separated after the fact. `task-sheet.md`
requires this to be stated plainly at Step 9; it is recorded here so the requirement is visible
to whoever reads the definition rather than only to whoever reads Step 9.

### 10.0b Required outputs added by this revision

**Provenance, and their status now.** D1–D7 above are Human Lead decisions or `task-sheet.md`
closures. **D8 and D9 are neither in origin: they are Red Team blocking finding F3 and secondary
finding 1**, written into the definition under the authorization to revise. They entered as
proposals and **are now adopted** by the Human Lead's approval of Step 1 on 2026-08-10. The
provenance is kept on the record so it stays clear that they were drafted by the Data Scientist
and adopted by the Human Lead, never self-adopted.

| # | Required output | Direction on the headline |
| :--- | :--- | :--- |
| **D8** | **Never-started post-window diagnostic.** The symmetric counterpart to D3, for the category the study is named after. | **Down** |
| **D9** | **Split-artifact counts and bound.** Trakt show splits manufacture Never started rows; treated as a known misclassification, not as a counting nuisance. | **Down**, plus an unmeasured denominator loss |

**D8, stated in full.** D3 asks what the window's close hides for **Started and left**. Nothing
asked the same question of **Never started** — which is the category that gets published as
"never," and the one word in the headline a reader will take most literally.

> Of user-show pairs scored **Never started** at `τ1`, report: **(i)** the count and share with
> any distinct S2 episode whose canonical timestamp falls in **`[τ1, τ1 + H × 24h)`**, `H = 91`
> days per D10, and **(ii)** the count and share satisfying the Continued condition —
> `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)` — over that same horizon. Counts and shares only,
> to `artifacts/`.

**The fixed horizon matters most here, and the previous draft had it backwards.** Measured to
the pull date, D8 gave a 2016 title ten years in which its never-starters could be caught
starting late and a 31 Dec 2024 title about eighteen months. Pooled, that **understates
later-starting for recent titles** — so "never" looked most true exactly where the frame is
newest, which is exactly where the public argument is loudest. Over `[τ1, τ1 + H)` every pair
gets the same 91 days and the share is a rate.

Three things make this cheap and non-optional:

- **It is computable for the whole population, and now that claim is true.** The previous draft
  justified it with a guarantee that does not hold: right-censoring at
  `T0 + max(W, 91) ≤ pull date` gives `max(0, 91 − W)` days of post-window observation, which is
  zero at any `W ≥ 91`. The rule is now `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull` (D10), which
  guarantees exactly `H` observed days after `τ1` **at every value of `W`**, so there is no
  subgroup for which the question is unanswerable.
- **It is the same query as D3 with the state filter changed.** No new data, no new join.
- **It moves the headline down**, and that is exactly why it belongs. Section 10.0 argues that
  reporting only bounds which move the headline **up** would present the study's uncertainty as
  if it ran one way. Publishing "never started" without ever checking how many of them started
  later would be that failure in its purest form: a pair that started S2 on day `W + 1` is
  called "never" by this document, and D8 is what makes the size of that group a number instead
  of an objection.

The direction is reported alongside the figure. D8 is a **diagnostic**, not a reclassification:
no pair moves state on account of it. If (i) or (ii) is large, the honest response is a
statement in the limits and a Step 13 arm on `W`, not a silent redefinition of "never."

**D9, stated in full. This replaces the previous draft's open question 4, which was wrong to
treat splits as a counting nuisance.** The pair key is `show.ids.trakt`. If Trakt **split** a
show's metadata between a user's viewing and our pull, S1 records key to `ID_A` and S2 records
to `ID_B`. Then:

- Pair `(user, ID_A)` has a complete S1 and `|A| = 0`. **It scores Never started.** The user
  watched S2. The row is fabricated, and it is fabricated directly into the headline category.
- Pair `(user, ID_B)` fails the S1 completion test and **disappears from the population
  entirely**, unreported, as though it had never been considered.

That is structurally identical to D4 — a known misclassification with a known direction — and
it gets D4's treatment, not a deferral:

> **Step 8 reports both counts**: (a) pairs scored Never started that carry a split signature,
> and (b) pairs dropped at S1 completion that carry the same signature, which is the silent
> half. **Step 9 reports the split-artifact bound** alongside the liveness bound and D4: what
> the never-started share becomes when every split-signature pair is removed from that
> category. Counts and shares only.

**Signature.** A candidate is a `(user, show_id)` pair where the user's sweep contains episodes
of another show ID whose season coverage is complementary — one ID carrying S1 and not S2, the
other S2 and not S1 — and whose show titles or `ids` indicate the same title. **Detection is
imperfect and the count is a lower bound; that is stated wherever the number appears.** Merges
are the mirror case and are less dangerous: they combine two IDs into one, which can only add
evidence to a pair, not remove it. They are counted with the same query and reported separately.

What remains open is only whether **reconciliation logic** is written — that is, whether split
pairs are merged back into one row rather than merely counted. My recommendation is unchanged
and modest: **count first, reconcile only if the count justifies it.** But the counting and the
bound are no longer conditional on anything, because "we did not measure it" is not an available
answer for a row that lands in the published category.

### 10.0c Definitions and required outputs added by this revision

**Provenance, and their status now.** D10 through D13 originate as **Red Team blocking findings
B1, B4, B5 and B3**, written into the definition under the authorization to revise. They entered
this document as proposals. **They are now adopted**, by the Human Lead's approval of Step 1 on
2026-08-10: `H = 91` (D10) and the D12 thresholds were adopted **by name** at approval, and D13
was adopted with the document. **D11 is adopted in form only** — `pull_date`'s **value** is
deliberately deferred to Step 4's schedule and remains a Human Lead act. The provenance is kept
on the record deliberately: these four are Red Team findings that the Data Scientist drafted and
the Human Lead adopted, and no agent adopted its own proposal at any point.

| # | What it fixes | Where it lives | Effect on a reported number |
| :--- | :--- | :--- | :--- |
| **D10** | **Fixed post-window horizon `H = 91 days`.** Right-censoring tightened to `⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`; D3 and D8 measured over `[τ1, τ1 + H)` instead of "to the pull date." | Section 6, D3, D8 | Removes an exposure confound whose weight was show recency; costs the most recent `H` days of S1 completers, which moves the headline **up** |
| **D11** | **`pull_date` is a single global frozen cutoff**, not per-user fetch date. `τ_pull := ⟦pull_date⟧`; records at or after it are discarded. Value set by the Human Lead, constrained to be no later than the earliest per-user fetch date. | Section 0 | Makes right-censoring and every diagnostic comparable across users instead of dependent on pull scheduling order |
| **D12** | **Cadence classifier with numeric thresholds, five exhaustive buckets, first-match ordering.** | Section 10.0 | Makes the Step 6 estimation sample, the Step 9 stratum and the Step 12 candidate deterministic; removes a real source of spurious dual-implementation divergence in `W` |
| **D13** | **Half-open UTC-instant boundaries.** `watched_at < τ1` and nothing else, applied identically to `A`, D3, D8 and right-censoring. | Section 2.4 | Removes a one-day ambiguity on the operator that assigns **every** outcome state; the window is now exactly `W` days, which moves the headline marginally **up** |

**Two of these four change numbers on their own, and both directions are already named in the
body rather than here**: D10's incremental censoring removal moves the never-started share up
(Section 6), and D13's one-day tightening moves it up while the Section 0 finale skew moves it
down by a comparable amount. D11 and D12 do not move a number by themselves; they remove
degrees of freedom that would otherwise let two faithful implementations disagree.

**What D10, D11 and D12 needed, and what is still outstanding.** `H` needed approval, not input:
**approved at 91 days**. The D12 thresholds needed approval: **approved as proposed** — they are
conventions, and the count of shows near a boundary (Section 10.0) is still the thing that tells
anyone whether the convention was load-bearing, so that count remains required. **One item is
still outstanding and it is the only one:** `pull_date` needs a **value** from the Human Lead
once Step 4's schedule is known. Step 1 fixes its form and its constraint. Any step that
right-censors, or that computes D3, D8 or D9, is blocked on that value — not on this gate.

### 10.1 Open questions, each with a recommendation

**Two remain.** Of the original four: show splits is resolved as D9, and **question 2 is decided
as D14** (Human Lead, 2026-08-10) — its text is kept below, marked as decided, because the
reasoning is the warrant for the decision and Step 6 needs it. **Questions 1 and 3 are still
open, and
Step 1's approval did not close them.** Approval covers the definition as written, including the
*drafted* boundary each question sits next to; it is not a ruling on the alternatives. Each
carries a recommendation from the Data Scientist and a decision from nobody. The Human Lead
decides them, and until then the drafted boundary is what the document says and what any
implementation follows.

| # | Question | My recommendation | Why, in one line |
| :--- | :--- | :--- | :--- |
| **1** | Continued boundary: S2 finale **plus** ≥ 90 percent, or finale alone? | **Finale plus 90 percent** | Finale-alone would score a user who watched 2 of 13 episodes and skipped to the end as having continued, which understates abandonment in the direction that flatters the headline. |
| **2** | How is W estimated when most started users have negative lags? | **Estimate W on bucket C1 (all-at-once) only, then apply it to all shows** | On a C1 show premiere and finale coincide, so every lag is a genuine post-availability delay and W is a property of viewer behaviour rather than of the frame's cadence mix. |
| **3** | Right-censoring on `max(W, 91)`, or on `W` alone? | **`max(W, 91)`, now carried as `max(W, 91) + H` per D10** | It costs real pairs, not zero, but it is the only version under which the primary and the 91-day arm share a denominator — and D5 already makes those two hard enough to compare. The `+ H` term is a separate requirement and does not touch that argument. |
| ~~4~~ | ~~Trakt show merges and splits~~ | **Closed. Now D9 (Section 10.0b).** | Splits do not merely miscount, they manufacture rows in the headline category and silently delete their counterparts, so counting and a bound are required rather than deferred. |

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

**2. Estimating W under D1. — DECIDED, no longer open. See D14 in Section 10.0.** The
Human Lead adopted the recommendation below on 2026-08-10: **W is estimated on bucket C1
(all-at-once) shows only, per the D12 classifier, and the resulting W is applied to all
shows.** `task-sheet.md` Step 6 now carries this, so both isolated Step 6 instances receive it
from the file they actually read. The reasoning is retained below as the warrant, including
what the decision costs.

*The truncate-at-zero recommendation from an earlier draft is
withdrawn.* Truncation maps every live weekly viewer to a point mass at zero, and the height
of that mass is set by how many weekly shows the frame happens to contain — so W would become
an artifact of the frame's cadence composition rather than a fact about viewers. Change the
show mix, change W, with no change in behaviour. That is not defensible out loud, which is the
bar Step 6 has to clear.

*Adopted (was: recommendation): estimate W on **bucket C1 (all-at-once)** shows only, per the
D12 classifier, then apply the resulting W to all shows.* **C1 is the estimation sample and C0,
C2, C3 and C4 are not** — stated as a bucket name rather than as the words "binge shows" precisely because
the two isolated Step 6 instances must select the same rows from the same frame without
consulting each other. On a C1 show the premiere and finale coincide, so `T0` is the moment the whole
season became available, every lag is non-negative by construction, and the lag measures the
one thing W is supposed to capture: how long a viewer takes to start something that is sitting
there available. That is a clean estimation sample for a quantity that is then applied
uniformly.

What it costs, stated so it is not discovered later: it assumes the delay-to-start behaviour
of binge viewers transfers to weekly viewers, which is an assumption and not a finding. **Two
things accompany the decision and are now required rather than suggested**, both written into
`task-sheet.md` — the C1-only and all-shows lag distributions plotted together at Step 6 so the
reader can see how far the transfer assumption is stretched, and a Step 13 arm varying W over
**at least** the range those two distributions imply, since that gap is the size of the
assumption and therefore the range that tests it. Whether the C1 estimation sample is large
enough to support the percentile is a question for Step 6 with the data in hand, not for
Step 1; `task-sheet.md` Step 6 now requires that answer be stated.

**3. Right-censoring.** *The "expected cost is zero rows" claim from the previous draft is
withdrawn; it was false on this document's own definitions.* The frame caps the S2 finale but
not `S1_completion_date`, so censoring removes users who completed S1 recently — people who
found an old show lately, who are disproportionately likely to continue, and whose removal
pushes the never-started share up (Section 6). *Recommendation: still `max(W, 91)`*, because
the alternative computes the two headlines on different denominators on top of the different
origins D5 already introduces, and two differences at once cannot be attributed. The removal
count is reported unconditionally either way, with its direction named, and if it is large the
right response is to say so in the limits rather than to switch rules to shrink it.

**4. Show merges and splits — closed, see D9.** *The "count at Step 8, build nothing yet"
framing is withdrawn.* It treated a split as a counting nuisance of unknown size. It is not: a
split gives one pair a complete S1 and no S2 evidence, which **scores Never started**, while
its counterpart fails S1 completion and leaves the population unrecorded. A fabricated row in
the published category is a misclassification with a direction, and that is D4's situation, so
it gets D4's treatment. Counting and the bound are now required outputs (Section 10.0b).
Reconciliation logic remains unwritten, and that part of the old recommendation stands.

---

## 11. What this document does not do

- It does not set **W**. Step 6. It does now fix the **estimation sample** W is derived from —
  bucket C1 only, per D14 — but the value is Step 6's and remains a gate.
- It does not set the **liveness threshold** or the liveness rule. Step 7.
- It does not set the **contamination exclusion rule**. Step 5.
- It does not set the **filter order**. Step 8.
- It does not resolve the **two open questions remaining in Section 10.1** — questions 1 and 3.
  Each carries a recommendation from the Data Scientist and a decision from nobody. Question 2
  was decided by the Human Lead as D14; question 4 was resolved as D9.
- It does not add a field or a filter to **Step 2**, which is the Human Lead's. Section 3.3
  states what this definition *requires* — the listed episode-number set — and names the
  recommended endpoint. Whether that requirement is met as a Step 2 field, as a separate pull, or
  not at all is theirs to decide.
- **It does not set `pull_date`, and that is deliberate.** D11 fixes the form of the constant and
  the constraint on its value. The **value is deferred by Human Lead decision** until Step 4's
  schedule is known — recorded as a deferral, not as an omission, because the constraint
  `pull_date ≤ earliest per-user fetch date` cannot be honoured by a value chosen before the pull
  is scheduled. This is the **only** item this document leaves outstanding that downstream
  computation blocks on.
- **It does not test the gap hypothesis.** The Section 3.3 precondition is closed, but the probe
  covered one show with contiguous numbering. Whether Trakt represents a numbering gap by
  **omitting** the number or by **listing a placeholder** is untested, and Section 3 is not a
  claim that gaps are handled. Settling it requires a show with a known gap, at the point where
  `E` is first pulled at scale.
- **No code was written or run for this document, per the gate.** The Step 0 episode-listing
  probe it now cites was run by the Analytics Engineer as Step 0 infrastructure, not by me and
  not for this document; the earlier line here — "no call was made to test it" — described this
  document's own conduct and still does.
- It does not adopt the **Section 3.3 fallback** (`F := L`, gaps unhandled). The fallback is
  written down so it is not improvised later; adopting it is a decision, not a default.
- The **task-sheet wording dependency** formerly flagged here is **closed**, and not by this
  document: the Human Lead amended `task-sheet.md` Steps 7 and 9 to pair-level scoping directly.
  Step 1 recorded the gap; the Human Lead resolved it in their own file. Section 9 now states the
  pair-level claim as fact rather than as an open dependency.
- **It did not adopt itself, and that record stands even though it is now adopted.** Everything
  in Section 10.0 came from the Human Lead or from `task-sheet.md` and is recorded as theirs.
  **D8 and D9 (Section 10.0b) and D10 through D13 (Section 10.0c) were drafted by the Data
  Scientist** under the authorization to revise, and were held as proposals until the Human Lead
  approved them — `H = 91` and the D12 thresholds **by name**, the rest with the document, on
  **2026-08-10**. The Human Lead also **overruled Red Team on B2**, recorded as accepted risk in
  the table at the head of the document. **The approval is the Human Lead's and was given in
  writing in this session; no agent recorded its own approval at any point.** The approval record
  is at the head of this document.
