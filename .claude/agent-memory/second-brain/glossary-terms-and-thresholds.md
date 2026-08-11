---
name: glossary-terms-and-thresholds
description: Live glossary of every term, threshold and constant in the Season 2 abandonment study, each tagged with the step and gate that fixed it and whether it is set, deferred, or still open — includes the Step 3 crawl constants, which were set by an agent inside a chained step with no gate
metadata:
  type: reference
---

# Glossary — terms, thresholds, and where each was set

Authoritative text is `artifacts/step1-outcome-definition.md`. This is an index, not a
substitute. Verify against the file before acting on any row.

Status vocabulary: **FIXED** (set and gate closed) · **DEFERRED** (form fixed, value owed)
· **OPEN** (gate has not run).

## The five items the Human Lead named as glossary-critical

| Term | Value / status | Where set | Gate |
| :--- | :--- | :--- | :--- |
| **`W`** — the window, in days | **Value OPEN. Estimation sample FIXED.** Step 1 §11 does not set the value. The sample it is derived from is **bucket C1 (all-at-once) only**, per D12, and the result is **applied to all shows** — D14, decision `0003`, Human Lead 2026-08-10. Carried in `task-sheet.md` Steps 6 and 13, so both isolated instances read it. | Value: Step 6. Sample: Step 1 §10.1 Q2 → D14 | Step 6 gate, **not approved** |
| **Liveness threshold** | **OPEN. Not set.** A gap length derived from data; Step 7 must derive it without using `W` as an input. | Step 7 | Step 7 gate, **not approved** |
| **S1 completion rule** | **FIXED.** `F1 ∈ D1` **and** `\|D1\| ≥ ceil(0.90 × L1)`, on distinct episodes, membership by the listed set `E1`. `ceil`, stated in episodes not percent. Failing pairs never enter the population — they are not "never started". | Step 1 §4 | **Step 1 gate, APPROVED 2026-08-10** |
| **Contamination exclusion rule** | **OPEN. Not set.** Step 1 fixes exactly one thing about it: it runs **before** right-censoring, so an import-stamped S1 completion date is counted as contamination rather than laundered into a censoring drop. | Step 5 proposes; ordering constraint from Step 1 §6 | Step 5 gate, **not approved** |
| **Filter order** | **OPEN. Not set.** Step 1 §11 disclaims it; Step 8 owns it. The only ordering Step 1 imposes is contamination-before-censoring. | Step 8 | Step 8 gate, **not approved** |

## Decision numbering — where a term was fixed on the public record

`decisions/` is the log of record: `0001` Step 1 gate, `0002` Step 4 endpoint (D15), `0003` W
estimation sample (D14), `0004` 403 handling. D-numbers live in
`artifacts/step1-outcome-definition.md` §10.0. A term tagged **D14** or **D15** below post-dates
the Step 1 gate and was decided separately.

## Step 3 crawl constants — agent-set, pre-registered in code, partly ratified

**Authoritative source: `src/step3_user_discovery.py:169-191`**, one block, quotable. Mirrored into
`artifacts/step3-yield-curve.json` → `plan` and `logs/step3_run.json` → `plan`. Run 2026-08-11.

**None of these appears in `task-sheet.md`**, but they were **not undocumented**: the module
docstring (lines 10-82) carries an affirmative rationale for nearly every one, written **before the
run** — "all chosen in advance", "all three committed in advance". Quote the docstring, not a
reconstruction. Status: **agent-taken under Chained latitude.** `TARGET_USABLE` is recorded in
`decisions/0005` and is **Open — awaiting ratification**; the rest are unrecorded as of 2026-08-11.

| Constant | Value | Note |
| :--- | :--- | :--- |
| `TARGET_USABLE` | **4,000** | The rule that actually stopped the run |
| `MIN_EPISODES_USABLE` | **10** | Account-wide episode floor. A **weak** definition of "usable" — a row still requires completing some show's S1 inside the Step 2 frame |
| `call_budget` | 6,500 | 5,300 spent, 1,200 unspent |
| Plateau rule | 3-round MA of new eligible per discovery call ≤ **0.20** of running peak, on **2** consecutive rounds, after **≥10** rounds | **Never fired.** Final ratio **0.314**, closest ever **0.193** |
| `n_seeds_target` | 300 | Movie-comment authors: 218 `comments/recent/all/movies`, 82 `comments/trending/all/movies`, 172 distinct films |
| `max_depth` | 3 | **Never reached.** Exit frontier was depth 1 and 2 only |
| `neighbours_per_user` | 100 | |
| `expand_users_per_round` | 12 | 432 of 5,694 users ever expanded |
| `list_pages_per_round` / `screen_calls_per_round` | 3 / 120 | |
| `step4_page_limit` | 250 | Matches the `limit=250` in D15 / decision `0002` |

**The pool: 4,088 usable users**, 5,694 discovered, 347 private, 5,347 eligible, 4,320 screened.
**1,027 eligible users were never screened** — a reserve costing ~1,027 calls, not stated as such
in the write-up. Channel split of usable: 2,306 Channel A / 1,782 Channel B.

**Stop reason: `sufficiency`, not plateau.** `task-sheet.md` Step 3 says "run until usable-user
yield plateaus." It did not. See [[open-items-and-contradictions]] S4.

## Step 4 cost — the number the Step 3 checkpoint exists to produce

**210,500 pages ≈ 210,500 calls ≈ 23.4 h** of pure throttled time at 150/min, over 4,088 users.
Mean **51.5** pages/user (sd 58.8), median 36, p75 66, p90 109, p95 151, p99 289, max 1,034. Top
decile of users holds 35.2 % of pages. Basis `pages = ceil((episodes.plays + movies.plays) / 250)`,
floor 1.

**Supersedes ~86,000 calls.** The earlier figure divided `total_plays`, **absent from 77 % of
`users/:id/stats` bodies** (Trakt returns two payload shapes), so most users forecast as exactly
1 page. Corrected figure is ~**2.4×**. `episodes.plays + movies.plays` matched `total_plays` in
549/549 bodies carrying both.

**Corroborates the D15 probe.** Decision `0002` cited ~64 pages/user from **one** profile. 64 sits
near p75 of the real distribution — mildly heavy, not an outlier. The n=1 figure held up. It is
still not a rate ([[open-items-and-contradictions]]).

## Data source — FIXED, D15 / decision `0002`

**`GET /users/:id/history`, unfiltered, one sweep per user.** Human Lead, 2026-08-10. Replaces
`/users/:id/watched/shows`, which returns a show-level aggregate with **no per-episode
timestamps** under Client-ID-only auth. Two conditions are part of the decision:

- **"One sweep" is one logical pass, NOT one call.** ~**64 pages per user at `limit=250`** on the
  probe profile. Step 4 throughput is estimated in **pages, not users**.
- **The sweep must be COMPLETE.** Records return newest-first, so a truncated sweep is
  **indistinguishable from a genuine "never started"** and lands in the headline. Enforcement is
  Step 4's and Step 8's.

Unfiltered because the endpoint mixes `type: episode` with `type: movie` and Step 7 liveness needs
the whole sweep as account-wide evidence; episode filtering happens locally, after the sweep.

## Standing rule — when a post-approval edit reopens a gate

Fixed 2026-08-10 in the approval record at the head of `artifacts/step1-outcome-definition.md`:
**an edit that changes a *rule* reopens the gate; an edit that adds *evidence* for a rule already
adopted does not.** The Section 5 addendum is the worked example — it inverted a cited figure and
changed no rule, threshold, definition or required output, and the gate remained approved. Apply
this test to any future amendment of an approved artifact.

## Probe figures — n = 1, existence proofs, NOT rates

From `artifacts/step0-history-endpoint-probe.md`, one profile and one show, reproduced at zero
live calls. **Nothing downstream may read these as population quantities.**

| Figure | Printed in Step 1 | Actual |
| :--- | :--- | :--- |
| Play-record inflation | "28 percent" | **28.125 %** — 123 records, 96 distinct pairs, 27 surplus records, **25** episodes duplicated (two appear three times; 27 and 25 answer different questions and are both right) |
| S1/S2 overlap under definition (a) | "six weeks" | **41.31 days = 5.90 weeks** |
| Same comparison under definition (b), after the §2.2 collapse | — | **inverts to 360.73 days of separation** — the overlap is entirely a rewatch artifact |
| Pages per user at `limit=250` | "roughly 64" | 64 |

Untested rather than confirmed on this profile: `episode.ids.trakt` disagreeing with
`(season, number)` — 96 IDs against 96 pairs, zero disagreements. See
[[open-items-and-contradictions]] N4.

## Liveness scoping — fixed at Step 1, and it moved

Liveness **evidence** is account-wide (whole sweep, other shows and movies included).
Liveness **test** is `watched_at ≥ τ1`, and `τ1` is pair-specific, so **liveness is a
pair-level filter**. One account can be live for one show and not another. Dropping a user
wholesale is forbidden. The earlier "statement about the account" phrasing is a withdrawn
claim — see [[withdrawn-claims-register]]. Backed in the repo: the Human Lead amended
`task-sheet.md` Steps 7 and 9 on 2026-08-10, so both isolated Step 7 instances read the
pair-level wording from the file they actually read. A scope divergence between them is now a
**bug, not a spec ambiguity**.

## Clock, window, horizon

| Symbol | Definition | Where | Status |
| :--- | :--- | :--- | :--- |
| `T0` | `max(S2_finale_air_date, first-pass S1_completion_date)` — finale-anchored, not premiere | Step 1 §6, D1 | FIXED |
| `τ0` | `⟦T0⟧`, i.e. `T0` at `00:00:00Z` | §2.4, D13 | FIXED |
| `τ1` | `τ0 + W × 24h`. Window is `[τ0, τ1)`, exactly `W` days | §2.4, D13 | FIXED in form; numeric only once `W` exists |
| In-window test | **`watched_at < τ1`**. Strict, half-open, instants only. `date(watched_at) ≤ T1` is withdrawn and must not be written anywhere | §2.4, D13 | FIXED |
| `H` | **91 days**, fixed post-window horizon. Not a function of `W`. Held constant across every Step 13 arm that varies `W` | §6, D10 | **FIXED — adopted by name at approval** |
| Post-window horizon interval | `[τ1, τ1 + H × 24h)` — where D3 and D8 are measured. Never "to the pull date" | §6, D3, D8 | FIXED |
| Right-censoring | retain iff **`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`** | §6, D10 | FIXED |
| `pull_date` / `τ_pull` | Single **global frozen cutoff**, `τ_pull := ⟦pull_date⟧`; every record with `watched_at ≥ τ_pull` is discarded. Never a per-user fetch date | §0, D11 | **DEFERRED — value outstanding.** See [[open-items-and-contradictions]] |

`pull_date` constraint: must be **no later than the earliest per-user fetch date in the whole
Step 4 sweep**. Human Lead sets it, once Step 4's schedule is known. This is the only item
Step 1 leaves outstanding that downstream computation blocks on.

## Season membership

`E` = the **listed episode-number set** for a season. `L := |E|`. `F := max(E)`. All three from
one payload, one show, one pull. **`F := L` is forbidden.** Specials (season 0) excluded from
`E` but still count as logged activity for liveness. Membership is by **set**, never by the
range `1..F` — that range form is a withdrawn claim.

Source, closed by the Step 0 probe: **`GET /shows/:id/seasons?extended=episodes,full`**, one
call per show, both seasons plus the season-level counts on one payload. Client ID alone,
HTTP 200, no pagination headers, season 0 returned and must be filtered.
(`artifacts/step0-episode-listing-endpoint-probe.md`.)

`show.aired_episodes` from the history payload is **never** used — it is show-wide, not
per-season.

## Outcome states, measured at `τ1` on distinct S2 episodes

`A` = distinct S2 episodes with `number ∈ E2` and `watched_at < τ1`. The interval is
`(−∞, τ1)` — **one-sided, no lower bound**, which is what keeps the live-viewing audience of
every weekly show from being scored never-started under finale anchoring.

| State | Condition |
| :--- | :--- |
| Never started | `\|A\| = 0` |
| Continued | `\|A\| ≥ 1` and `F2 ∈ A` and `\|A\| ≥ ceil(0.90 × L2)` |
| Started and left | `\|A\| ≥ 1` and not Continued |

Mutually exclusive and exhaustive by construction.

**Abandonment point** `p = |{ e ∈ E2 : e ≤ m }| / L2` where `m = max(A)` — rank-based, not
`m / L2`. `p ∈ (0, 1]` by construction under the set rule. Defined **only** for Started-and-left.
`p = 1.0` is its own named residual category at Step 10 and is not merged into "near-finale".

## Counting rules

- **Distinct episodes, never play events.** Dedup key `(show.ids.trakt, episode.season, episode.number)`, scoped to the user. `episode.ids.trakt` is not canonical; disagreements are counted and logged.
- **Canonical timestamp = minimum `watched_at`** across a distinct episode's records. Ordering on full UTC timestamps, ties broken by episode number then smallest history event `id`.
- **All `action` values count as watching**, `checkin` included. `action` is retained as a column for Step 5 and a Step 13 arm.
- Date reduction applies to clock arithmetic only, never to sequencing.

## D12 cadence classifier — adopted by name, 2026-08-10

`span := F_d − P` in whole UTC days; `weekly_span := (L2 − 1) × 7`. **First match wins**, and
the ordering is part of the definition.

| # | Bucket | Condition | In Step 6 estimation sample? |
| :--- | :--- | :--- | :--- |
| C0 | Unclassifiable | `P`, `F_d` or `L2` missing, or `span < 0` | No |
| C1 | All-at-once (binge) | `span ≤ 1` | **Yes — and only this bucket. DECIDED**, D14 / decision `0003`, 2026-08-10 |
| C2 | Weekly | `abs(span − weekly_span) ≤ 3` | No |
| C3 | Faster than weekly | `1 < span < weekly_span − 3` | No |
| C4 | Slower than weekly | `span > weekly_span + 3` | No |

Checked: C1–C4 partition `span ≥ 0` under first-match, and C0 absorbs missing/impossible. All
five are reported as their own line in the Step 8 waterfall and the Step 9 cadence stratum.
Required alongside: **the count of shows within 1 day of any bucket boundary**, so the
convention's fragility is a number rather than an assumption.

## Population rules Step 1 added that the task sheet does not carry

- **`L2 = 1` shows are excluded from the headline population at Step 8**, with the show and pair counts reported. At `L2 = 1` the three-state partition degenerates to two and `p` is never defined. `L1 = 1` is retained.
- Step 10 must not compare `p` bins across shows with very different `L2`.

## Required diagnostics fixed at Step 1

| ID | Output | Direction on the headline |
| :--- | :--- | :--- |
| D2 | Negative-lag count, **split by which term of the `max()` binds**. Computed on the operative clock, i.e. **definition (b)** — so no (a)-style rewatch artifact can appear in it. A zero here is not evidence the (a)-failure is rare ([[open-items-and-contradictions]] N2) | diagnostic |
| D3 | Resumption rate for Started-and-left, over `[τ1, τ1 + H)` | diagnostic |
| D4 | S3-without-S2 reported as a bound at Step 9 | **down** |
| D8 | Never-started post-window diagnostic, over `[τ1, τ1 + H)` | **down** |
| D9 | Split-artifact counts (both halves) plus a Step 9 bound | **down**, plus unmeasured denominator loss |
| Liveness bound | inactivity-excluded **pairs** treated as decliners | **up** |
| Right-censoring removal | reported as **two lines** — `max(W, 91)` term and incremental `+ H` term | **up** |
| Dropped-S2-evidence count | pairs with `\|A\| = 0` only after the drop rule | **up** on Never started |

Related: [[gate-step1-outcome-definition]], [[withdrawn-claims-register]],
[[open-items-and-contradictions]], [[decision-log-step18]].
