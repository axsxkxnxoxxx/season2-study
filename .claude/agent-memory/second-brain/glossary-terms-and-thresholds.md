---
name: glossary-terms-and-thresholds
description: Live glossary of every term, threshold and constant in the Season 2 abandonment study, each tagged with the step, decision and gate that fixed it and whether it is set, deferred, or still open — current through Steps 2, 3, 4 and Step 5 revision 6 (2026-08-12)
metadata:
  type: reference
---

# Glossary — terms, thresholds, and where each was set

**Current through 2026-08-12**, after Steps 3, 4, 2 and Step 5 revision 6. This is an index, not a
substitute for the artifacts. Verify against the file before acting on any row.

Status vocabulary: **FIXED** (set and gate closed) · **DEFERRED** (form fixed, value owed)
· **OPEN** (gate has not run) · **PROPOSED** (agent produced it, gate not approved).

## The five items the Human Lead named as glossary-critical

| Term | Value / status | Where set | Gate |
| :--- | :--- | :--- | :--- |
| **`W`** — the window, in days | **Value OPEN. Both factors of its sample are FIXED and both are now in `task-sheet.md`.** Estimation sample is **two-factor**: cadence bucket **C1 only** (D14 / `0003`) applied **on top of** — not instead of — a **provenance-clean sample of 128,099 pairs** (`0021` ruling 1). Result applies to all shows and all provenances. Step 6 launched 2026-08-12 as a dual pair. | Value: Step 6. Cadence: D14. Provenance: `0021`. Both propagated by `0022` | Step 6 gate, **not approved** |
| **Liveness threshold** | **OPEN. Not set.** A gap length derived from data; Step 7 must derive it without using `W` as an input. **Basis fixed:** liveness runs on **record insertion time**, not claimed `watched_at` (`0021` ruling 2). The play-`id` calibration is a **required input and neither instance refits it** — written into `task-sheet.md` Step 7 by `0022`, along with the gap-distribution item now reading **insertion instants** | Step 7; basis `0021`, spec `0022` | Step 7 gate, **not approved** |
| **S1 completion rule** | **FIXED.** `F1 ∈ D1` **and** `\|D1\| ≥ ceil(0.90 × L1)`, distinct episodes, membership by the listed set `E1`. Now applied against **real** `E1` from the Step 2 frame, not a proxy (`0019`). | Step 1 §4 | **Step 1 gate, APPROVED 2026-08-10** |
| **Contamination exclusion rule** | **FIXED.** Exclude **16,665** pairs whose S2 evidence is *entirely* air-date-stamped, plus **1,542** with no S2 evidence and a fabricated binding clock start. Total **18,207**; retains **201,900 of 220,107 (91.73%)**. Disjoint by construction. | Step 5 §9, revision 6 | **Step 5 gate, APPROVED 2026-08-12, `0021`. Gate 2 of 5** |
| **Filter order** | **OPEN. Not set.** Step 8 owns it. `task-sheet.md` Step 8 names the members — frame, contamination, S1 completion, W, liveness, right-censoring, `L2 = 1` — and one ordering constraint: **contamination before right-censoring**. The order among the rest is Step 8's. | Step 8 | Step 8 gate, **not approved** |

## Decision numbering on the public record — `decisions/`

`0001` Step 1 gate · `0002` Step 4 endpoint (D15) · `0003` W estimation sample (D14) · `0004` 403
handling · `0005` Step 3 stopping rule · `0006` Step 3 crawl constants · `0007` Step 3 channel cost
· `0008` Step 3 seed source · `0009` Step 4 pull order · `0010` Step 4 tail cap · `0011` `pull_date`
· `0012` sweep completeness · `0013` Step 2 delegation · `0014` no content filters · `0015` unaired
S2 · `0016` per-season network dropped · `0017` air period · `0018` size quintile base · `0019`
`pool_completers` recomputed · `0020` structural thresholds · **`0021` Step 5 gate APPROVED** ·
**`0022` the two Step 5 rulings written into `task-sheet.md`** · **`0023` `0012` upheld after a Red
Team HOLD**.

**Authority split.** `0001–0004` and `0009–0023` are Human Lead. **`0005–0008` are agent-taken and
still Open, awaiting ratification** — the README's authority note now names all four correctly.

## Clock, window, horizon — unchanged from Step 1 except `pull_date`

| Symbol | Definition | Where | Status |
| :--- | :--- | :--- | :--- |
| `T0` | `max(S2_finale_air_date, first-pass S1_completion_date)` | Step 1 §6, D1 | FIXED |
| `τ0` / `τ1` | `⟦T0⟧` / `τ0 + W × 24h`; window `[τ0, τ1)` | §2.4, D13 | FIXED in form |
| In-window test | **`watched_at < τ1`**. Strict, half-open, instants only | §2.4, D13 | FIXED |
| `H` | **91 days**, fixed, not a function of `W` | §6, D10 | FIXED |
| Right-censoring | retain iff **`⟦T0⟧ + (max(W, 91) + H) × 24h ≤ τ_pull`** | §6, D10 | FIXED in form |
| **`pull_date` / `τ_pull`** | **`pull_date = 2026-08-11`, `τ_pull = 2026-08-11T00:00:00Z`.** Every record with `watched_at ≥ τ_pull` is discarded. | **`0011`, Human Lead 2026-08-11** | **FIXED — D11's deferred value is now closed** |

`0011`'s constraint check: earliest per-user fetch instant **2026-08-11T05:01:26Z ≥ τ_pull** ✓.
Consequence carried in `0011`: the discarded tail is ~1 day for early-fetched users and ~2 for
late-fetched ones, so **the discarded-record count is not evenly distributed across the pool.**

## Step 2 frame — the population every result is computed on

**Owner Human Lead, execution delegated to an agent under `0013`.** Artifact:
`artifacts/step2-frame-ledger-and-distributions.md`.

**Frame: 1,138 shows, 220,107 S1-completer pairs.** Candidate set 2,094 shows (≥50 completers).
Exclusion ledger, in the order the rules were written:

| # | Rule | Removed | Remaining |
| :-- | :--- | ---: | ---: |
| 0 | Candidate set, ≥50 S1 completers | — | 2,094 |
| 3 | No real season 2 | 796 | 1,298 |
| 4 | S2 listed but unaired (`aired_episodes = 0`) — **`0015`** | 12 | 1,286 |
| 5 | S2 finale aired after 2025-12-31 (`first_aired < 2026-01-01T00:00:00Z`, half-open per D13) | 60 | **1,226** |
| 6 | Season over **26 episodes** (S1 or S2) — **`0020`** | 51 | 1,175 |
| 7 | Gap over **1,095 days** (S1 finale → S2 premiere) — **`0020`** | 37 | **1,138** |

Rules 1, 2 and 8 removed 0. Rules 6 and 7 overlap on exactly 1 show, so order is immaterial.
**Season 0 is filtered inside every show, never used to exclude one** — 878 candidates carried one.

### Structural thresholds — `0020`, Human Lead 2026-08-12

- **No minimum season size.** `ceil(0.90 × L1)` already scales per show. `L1 = 1` and `L1 = 2` are
  retained; `min(L1) = 1`, `min(L2) = 2`, so **no in-frame show has `L2 = 1`**.
- **Max 26 episodes** on either season. 26 is the traditional full broadcast season; the cut is
  insensitive from 26 to 40 (1.1–2.4% of pairs). **22 was rejected** at 196 shows / 13.8% of pairs.
- **Max 1,095-day gap** (3 years). The empty `3 y+` bucket is the cap made visible.
- Combined cost **88 shows, 12,851 pairs, 5.5%.**
- **The size cap is partly a cadence threshold: 44 of its 51 shows are C4.** C4 falls 476 → 425.
  A C4 result is computed on a population stripped of its longest-running titles.

### Other Step 2 definitions

| Term | Definition | Where |
| :--- | :--- | :--- |
| **Air period** | **Calendar year of the S2 finale**, bucketed **pre-2020 / 2020–2022 / 2023–2025**, bracketing the production shutdown. Frame: 757 / 213 / 168. **Strongly collinear with cadence — not an independent cut.** | `0017` |
| **Size quintile** | Cut over **the frame**, not the 2,094 candidates, on the **recomputed** `pool_completers`. Frame bins **238 / 221 / 224 / 227 / 228**. **A quintile label is not a stable identifier** — rebuild the frame and every boundary moves. | `0018` (see [[open-items-and-contradictions]] X3: `0018` still publishes the superseded 1,226-frame bins) |
| **`pool_completers`** | Step 1 §4 applied against **real** `E1`, `L1 = \|E1\|`, `F1 = max(E1)`. **The max-observed proxy is superseded and no result may use it.** Changes nothing on this frame (proxy = real on 1,225 of 1,226). | `0019` |
| **No content filters** | Anime and daily-strip/soap exclusions **dropped before first use.** The concern was release structure, not genre. Release structure is recorded as **fields**, thresholds set separately. The jp shows that left (92 → 60) left via the 26-episode cap, not by genre or country. | `0014`, Closed 2026-08-12 |
| **Per-season network** | **DROPPED as a field.** 47 of 6,645 season objects populated (0.71%); one show in 2,094 with two distinct values, read as noise. **Platform fragmentation is not a variable in this study** — no result may control for it, stratify on it, or rule it out. | `0016` |
| **`show_network`** | Show-level, 100% populated, 150 distinct — but it records **today's** network. **Must not be used as a release-time availability measure.** Descriptive only. | `0016`, README open item 18(b), still open |

**D12 as applied on the real frame:** C0 **0** · C1 206 (18.1%) · C2 340 (29.9%) · C3 167 (14.7%)
· C4 425 (37.3%). **Fragility count: 7 shows within one day of a bucket boundary, 0.6%** — by
D12's own test the thresholds are **not load-bearing** and a Step 13 arm on them is not indicated.
(238 sit within three days, but 220 of those are same-day drops at distance exactly 2 by
construction. **The one-day figure is the meaningful one.**)

## Step 5 — contamination vocabulary. PROPOSED, gate not approved.

**Artifact `artifacts/step5-contamination-diagnostics.md`, revision 6, FINAL.** Reviews in
`artifacts/step5-red-team-reviews.md`. See [[gate-step5-contamination]] for the arc.

### Layer 1 record tags — no rows dropped. Required by Step 7 and Step 8.

| Tag | Definition |
| :--- | :--- |
| `corrupt` | `watched_at` absent or pre-1990 |
| `backfilled` | `τ_ins(id) − watched_at > 180 d` |
| `airdate_stamped` | `(show, season, episode, instant)` tuple shared by **≥5 unrelated accounts** |
| `postdated` | `watched_at` more than **30 d after** insert |
| `clean` | none of the above |

**The 180-day threshold is a conservative judgment, not a data-determined break.** Per-day density
is monotone decreasing throughout; revision 1's "trough" was a bin-width artifact (Red Team C1).
**The only real break after 1 day is at 7 days.**

### The instrument — the play-`id` insert-time calibration

The Trakt play `id` is a global auto-increment assigned at **write** time, so it orders records by
insertion regardless of what `watched_at` claims. Fitted on `checkin` and `scrobble` only (a bulk
import mints `watch` rows), monotonised by **isotonic regression (PAVA)**, not a cumulative max.
**Held-out validation** (fit on even-indexed accounts, test on 2,185,696 real-time records of
odd-indexed accounts, no account in both): **median lag +0.003 d, 90.5% within one day.** Residual
error runs slightly **early**, so the diagnostic **under-flags**. Zero API calls.
Artefacts: `processed/step5/calibration.npz`, `record_lag.npz`.

### The insert-time bound

*A viewer cannot log an episode before watching it*, so a record's insert instant is an **upper
bound** on when it was truly watched. Latest defensible clock start:
`T0_latest = max(S2_finale_date, date(max τ_ins over the S1 completion evidence))`.
**Correct basis: the completion prefix, with the `max()` in force.**

| Population | Pairs | Median elapsed at `T0_latest` | Open at `W = 60` |
| :--- | ---: | ---: | ---: |
| The **1,542** (excluded) | 1,542 | **40.0 d** | **58.6%** |
| The **720** (C5, no S2, retained) | 720 | **1,738 d** | **7.92%** |
| — the 425, two-class | 425 | 1,717 | 13.4% |
| — the 295, air-date class | 295 | 1,762 | 0.0% |
| Every pair with no S2 evidence | 25,277 | 1,532 | 11.3% |

**`1,738 d / 7.92%` is the figure to use for the 720.** "Median 2,150 d / 8.1%" is **withdrawn** —
it came from a unit bug plus the wrong basis. See [[withdrawn-claims-register]].

### The two populations — Step 5 ruling 1

> **W is derived from clean records only, then applied to everyone.**

| Population | Pairs | Who reads it |
| :--- | ---: | :--- |
| **Analysis population** | **201,900** | Step 8 classifies these |
| **W estimation sample** | **128,099. Determinate.** | Step 6, which applies D14's C1 restriction **on top** |

Waterfall, monotone by construction: 201,900 → has S2 evidence 178,165 → `T0` not contaminated
155,131 → completing record not post-dated 152,126 → **first S2 watch clean 128,099**.

The analysis population **deliberately** retains 23,067 pairs with a fabricated `T0`, 46,642 whose
first S2 watch is contaminated, and 3,296 whose completing record is post-dated.

### Post-dating — the four readings, and why they are moot

**Adoption 3 was DROPPED (revision 6).** No pair is deleted for post-dating; records are tagged and
kept out of the W sample. The four readings are four ways to apply a rule that no longer exists.
Recorded because the **directions differ and a table ordered by retention alone hides that**:

| Reading | Retained | Bias direction |
| :--- | ---: | :--- |
| **Adopted — tag only, delete nothing** | **201,900** | neutral |
| P, delete the pair | 198,604 | never-started **down** |
| R1b, drop every post-dated S1 record | 198,817 | down |
| R1n, drop only the completing record | 199,957 | down |
| R3, re-date to insertion time | 201,900 | never-started **up** (median completion shift **−198.7 d**) |

The adopted rule coincides with R3 in **retained set**, not in method: R3 rewrites timestamps, the
adopted rule only tags them. That distinction is what avoids E4 — §2.2 (canonical timestamp = the
**minimum `watched_at`**) is untouched, and no re-dating bias is introduced. R3 would also have been
a **selective** re-dating: if `τ_ins` were trustworthy for 3,307 post-dated records it would be
trustworthy for 8,001,189 backfilled ones, where substitution moves completion much **later**.

### Contamination scale, for reference

| Class | Records | Share of 27,656,631 |
| :--- | ---: | ---: |
| Backfill >180 d | 8,001,189 | 28.9% |
| Air-date-stamped (mode 3) | 2,021,537 | 7.3% |
| Corrupt, pre-1990 (369,590 at exactly 1970-01-01) | 690,774 | 2.5% |
| Undated | 379 | 0.001% |
| **Union** | **8,831,718** | **31.9%** |

**Mode 3, air-date stamping**, was not previously identified: exact top of hour, seven days apart,
00:00–05:00 UTC, **up to 198 accounts sharing a single instant** (corrected from an uncommitted and
wrong "164"). **TV Time is a minority of the problem** — only 31.7% of backfill was written after
2026-06-01; the rest is eleven years of ordinary onboarding backfill. The shutdown wave is
3,115,531 records over four weeks (11.3% of the store) against a ~174,000 baseline, an **excess of
2.94 M records = 10.6%**.

## Step 3 crawl constants — agent-set, `0006`, Open awaiting ratification

**Source `src/step3_user_discovery.py:169-191`.** Full table retained; the load-bearing ones:

| Constant | Value | Note |
| :--- | :--- | :--- |
| `TARGET_USABLE` | **4,000** | The rule that actually stopped the run — **not** the plateau rule `task-sheet.md` names, which ran 36 rounds and never fired (final ratio 0.314 against a 0.20 trigger). `0005` |
| **`MIN_EPISODES_USABLE`** | **10** | `episodes.watched` from `GET /users/:id/stats` — an **account-wide** distinct-episode count, **not per-show**. Ten episodes across ten shows passes; nine inside one show fails. Removed **232** accounts and nothing else removed any. **Warrant accepted as not literally true** (README item 13, closed 2026-08-12): `min(L1) = 1` and 152 in-frame shows have `L1 ≤ 6`, so exposure is **at most 22 accounts, 0.5% of the 4,320 screened** — 210 of the 232 had zero episodes. All 232 recoverable at **0 live calls** |
| `call_budget` / plateau rule | 6,500 / 3-round MA ≤ 0.20 of peak on 2 consecutive rounds after ≥10 | budget 5,300 spent; plateau never fired |
| `n_seeds_target` / `max_depth` | 300 / 3 | Seeds = **movie-comment authors**, 172 distinct films, `0008`. Depth 3 never reached |
| `step4_page_limit` | 250 | matches `limit=250` in `0002` |

## Step 4 — the pull, and the rules that governed it

**Source: `GET /users/:id/history`, unfiltered, one sweep per user** (D15 / `0002`). One sweep is
one logical **pass**, not one call; throughput is estimated in **pages**.

| Term | Value | Where |
| :--- | :--- | :--- |
| **Pull order** | **Stratified round-robin** over ten equal-count forecast-page bins, one user per bin in turn, deterministic within bins. Amends an initial **median-out** instruction, which left a *centered* slice with **no user above 73 pages** at ten hours in a pool reaching 1,034. Cost: **~12% fewer users/hour**, accepted explicitly. | `0009` |
| **Tail cap** | **300 forecast pages**, skip whole, never truncate — **plus an actual-pages guard** that discards mid-sweep overruns. Excludes **38 users, 0.93%**, keeps 92.8% of pages. Justified as a **circuit breaker on forecast error**, not as protection against a slow user. Direction **upward** on the headline. | `0010` |
| **Sweep completeness rule** | **Full `X-Pagination-Page-Count` coverage plus a residual within 2% of `X-Pagination-Item-Count`.** Exact equality is **not** required — the pilot failed 7 of 10 on residuals from −97 to +20, and under exact equality the study would discard ~70% of its pool. **Amends `0002` condition 2 and Step 1 §0 — a rule inside an approved gate.** **Reviewed by Red Team 2026-08-12, which returned HOLD; UPHELD by the Human Lead on cascade cost, not on merit (`0023`).** Three findings became Step 14 limitations. | `0012`, upheld by `0023` |
| **Over-tolerance users** | Pages **discarded, logged, never truncated**, and must stay distinguishable downstream exactly as `access_denied` does. **287 users on the final ledger**; their raw pages remain cached, which is what made the neutrality check possible at zero API cost | `0012` |

**`0012` requires three behaviours counted separately, never collapsed into the tolerance:** header
**over-count** (benign, 256 of the 287), header **under-count** (benign and in the safe direction —
**31 of 287**, corrected from a mid-run "24 of 235"), and duplicate records.

**The third is misattributed in `0012` and the correction is in `0023`.** `0012` cites "5 duplicates
in 14,236 records" as **cross-page** duplicates. Instrumentation records
`cross_page_duplicate_records: 0 users, 0 records` across 2,137 users and 22,725,090 records.
**Cross-page duplicates have never been observed in either run.** What does occur is **within-page**:
147 records, the same `id` twice on one page, meaning a 250-slot page carried 249 distinct records.
That behaviour **is not a required output, is described nowhere, and has no stated interpretation.**

**Proof that the residuals are not truncation:** page-count and item-count headers were identical on
every page of every sweep; and re-sweeping one user at `limit=100` returned the **identical record
set in identical order** as the cached `limit=250` sweep — 1,459 distinct records both ways, while
both headers reported 1,460.

### What `0023` established about the 2% tolerance, and what did not change

**Nothing in the study moves.** Cohort 2,549, frame 1,138 shows, 220,107 pairs, 201,900 retained,
128,099 estimation sample — all stand. The tolerance was not touched and nothing was re-run.

**Three findings now travel to Step 14 as limitations:**

1. **The rule validates itself against itself.** Leg 1 gates on `page_count`, which is
   **`ceil(item_count / 250)` in all 2,839 ledger rows, zero mismatches** — so it is derived from
   the very header leg 2 exists to absorb. A **short** final page proves the sweep reached the end;
   a **full** final page proves nothing, and leg 1 cannot tell them apart.
2. **The discard is NOT outcome-neutral.** Measured at zero API cost on the discarded users' cached
   raw pages: has-any-S2 **89.78% (discarded) vs 88.52% (retained)**, **+1.27 points, 95% CI [0.87,
   1.66], z = 5.98, p < 0.001**, intervals non-overlapping. **Direction: up** on the never-started
   share, **compounding with the seeding and liveness biases rather than offsetting them.**
   **Pooled effect 0.13 points** (88.52% → 88.65%), because the 287 carry 10.2% of the pair pool.
   *Statistically clear, practically small — neither half may be quoted without the other.*
3. **Red Team's final-page shape test** — every interior page full at `limit`, final page strictly
   between 0 and `limit` — would discriminate **exactly** rather than by calibration, at **~2,800
   calls, ~19 minutes, and no re-pull**. **Declined on cascade cost, not on merit.** If the pull
   ever resumes, the cascade argument weakens and the shape test should be reconsidered rather than
   inherited as settled.

**The ruling's stated reason, in full:** tolerance → cohort size → completer counts per show → which
shows clear ≥50 → the candidate set → the frame → the structural thresholds → the 220,107 pairs →
the approved Step 5 rule computed on them. **A 0.13-point correction at the far end does not justify
re-deriving that chain.**

**How the 2% was actually set, recorded in `0023`.** The pilot's p95 is **1.4%** and p99 = max is
**11.7%**, with nothing in between, so **every tolerance from ~1.5% to 11.7% split those 20 users
identically** — and the most aggressive end of that band was chosen, with no sensitivity table and
without the choice being stated as a choice. **On the full run there is no such gap:** absolute
residual share over the 287 discards runs min 2.01%, median 3.92%, max 99.9%, with **168 (58.5%) in
the 2–5% band** — so a 5% tolerance would have retained 168 of the 287. The threshold cuts through
the middle of a continuous distribution.

**One structural asymmetry nobody chose.** Accumulated records can never exceed
`limit × page_count`, so a positive residual is capped at **249**. **Above roughly 50 pages the
under-count arm cannot fire at all.** The rule presents as a symmetric two-sided threshold; it is a
one-sided test on large users and a size-correlated discard on small ones. It also discards **31 of
287** users in the direction `0012`'s own table calls *"benign, and in the safe direction."*

## The population chain — every number a result rests on

See [[population-chain-steps-2-3-4]] for the reconciliations. Headline figures:

**4,088 usable users** → 4,050 in plan after the 38 over-cap → **pull stopped at 2,836 decided
(70.0%)** → **2,549 `complete`** (287 discarded over tolerance) → 44,617 shows with an S1 record →
**2,094 candidates** at ≥50 completers → **1,138-show frame, 220,107 pairs** → Step 5 proposes
**201,900 analysis population** and **128,099 W estimation sample**.

## Standing rule — when a post-approval edit reopens a gate

**An edit that changes a *rule* reopens the gate; an edit that adds *evidence* for a rule already
adopted does not.** Fixed 2026-08-10 in the Step 1 approval record. **`0012` is the first edit that
fails this test and was recorded as a Human Lead amendment anyway** — README open item 15 flags it
as not yet put to Red Team.

## Probe figures — n = 1, existence proofs, NOT rates

Play-record inflation **28.125%** (123 records, 96 distinct pairs, 27 surplus records, **25**
episodes duplicated — 27 and 25 answer different questions and are both right). S1/S2 overlap
**41.31 d under definition (a)**, inverting to **360.73 d of separation under (b)**. 64 pages per
user at `limit=250`. `episode.ids.trakt` disagreement with `(season, number)`: **untested**, not
confirmed — and the Step 2 frame's four absolute-numbering shows have since been removed by the
26-episode cap, though their finding stands (100% overlap on all four; the **withdrawn `1..F`
range form would have failed on all four**).

## Season membership, outcome states, counting rules

Unchanged from Step 1 and still governing.

`E` = the **listed episode-number set**; `L := |E|`; `F := max(E)`. **`F := L` is forbidden**
except by Human Lead adoption of the §3.3 fallback. Source `GET /shows/:id/seasons?extended=
episodes,full`, one call per show. `show.aired_episodes` is **never** used.

`A` = distinct S2 episodes with `number ∈ E2` and `watched_at < τ1`, over `(−∞, τ1)` — **one-sided,
no lower bound**. Never started ⇔ `|A| = 0`. Continued ⇔ `|A| ≥ 1` and `F2 ∈ A` and
`|A| ≥ ceil(0.90 × L2)`. Started-and-left is the remainder. Abandonment point
`p = |{e ∈ E2 : e ≤ m}| / L2` where `m = max(A)` — rank-based, defined only for Started-and-left.

Counting: **distinct episodes, never play events**, dedup key `(show.ids.trakt, season, number)`
scoped to the user; **canonical timestamp = minimum `watched_at`**; **all `action` values count as
watching**, `checkin` included, with `action` retained as a column.

## Required diagnostics fixed at Step 1 — unchanged

D2 negative-lag split by binding term · D3 resumption over `[τ1, τ1 + H)` · D4 S3-without-S2 bound ·
D8 never-started post-window · D9 split-artifact counts · liveness bound (**up**) · right-censoring
removal as **two lines** · dropped-S2-evidence count. `L2 = 1` shows excluded at Step 8 (**moot on
the current frame — `min(L2) = 2`**).

Related: [[gate-step1-outcome-definition]], [[gate-step5-contamination]],
[[population-chain-steps-2-3-4]], [[open-items-and-contradictions]], [[withdrawn-claims-register]],
[[decision-log-step18]].
