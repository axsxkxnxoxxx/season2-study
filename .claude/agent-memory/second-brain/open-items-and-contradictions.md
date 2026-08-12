---
name: open-items-and-contradictions
description: Live register of open items and cross-step contradictions in the Season 2 study, each with its two conflicting sources named — re-verified 2026-08-12 after Steps 3, 4, 2 and Step 5 revision 6, including seven new contradictions and the five conclusions whose stated reason was corrected
metadata:
  type: project
---

# Open items and contradictions — re-verified 2026-08-12

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry names its two sources so the Human
Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it. Several close by
ordinary progress rather than by a decision.

**The decision log of record is `decisions/`** — `README.md` plus `0001`–`0020`. Where a decision
file and this memory differ, `decisions/` governs on who decided what and when; the deliverable it
approves governs on substance. I never edit `decisions/` — I report.

---

## NEW — surfaced 2026-08-12, in priority order

### X1. Both of Step 5's standing rulings are missing from the file the isolated instances read

**This is the highest-consequence item on the register.**

- `artifacts/step5-contamination-diagnostics.md` §3: *"Under **ruling 2** this calibration is a
  **required input to Step 7**, which now needs an insertion time for every record."* §9.5 withdrew
  **Layer 3 entirely** — 35,861 pairs — because "its sole premise was that import noise is not
  liveness evidence, and under insertion-time liveness it **is** evidence."
- `task-sheet.md` **Step 7**, lines 231–235: *"Plot the distribution of gaps between consecutive
  logged events per user"*; the rule is written on *"logged activity"*. **Insertion time appears
  nowhere. The play-`id` calibration appears nowhere.** Both isolated Step 7 instances, reading only
  this, will derive gaps on **claimed `watched_at`.**

Two things make this worse than an ordinary omission:

1. **The dual-implementation regime cannot catch it.** Its only signal is divergence between the two
   instances. Two instances reading the same silent spec **agree** — on the wrong clock. A silent
   spec produces a clean diff, which reads as confirmation.
2. **The precedent is already established twice, by the Human Lead, for exactly this reason.** D14
   was written into `task-sheet.md` Step 6 *by bucket name* so both instances select the same rows;
   the pair-level liveness scope correction was written into Steps 7 and 9 because Step 1 could not
   fix it from inside its own file. `task-sheet.md` Step 8's preamble says outright it carries the
   obligations "because this is the file the two isolated instances read."

**Same class, one step earlier and less urgent:** ruling 1's **128,099 provenance-clean estimation
sample**. `task-sheet.md` Step 6 says only *"Restrict to users who did start S2"* plus D14's C1
restriction. The estimation sample is now **two-factor — cadence and provenance** — and only the
cadence factor is in the file. Less urgent because Step 6 runs downstream of the Step 5 gate; but if
the gate is approved without amending Step 6, the two instances will estimate `W` on a different
sample than Step 5 specified.

**Both rulings currently exist only inside an artifact for an unapproved gate.** Ruling 2 has
already been spent — it is why Layer 3 is not on the table.

### X2. `decisions/README.md` item 13 states a figure its own cited source contradicts

- **`decisions/README.md` open item 13**, closed and **ACCEPTED by the Human Lead 2026-08-12**:
  *"`min(L1) = 1` over the frame and **159 in-frame shows have `L1 ≤ 6`**"*, citing
  `artifacts/step2-frame-ledger-and-distributions.md` §3.2.
- **That §3.2** gives S1 episode buckets `1–3` = **13** and `4–6` = **139**. Total **152**.
  Independently confirmed in `processed/step2/frame-summary.json` → `s1_L_hist`.

**Likely cause, stated as a hypothesis:** 159 was computed on the **1,226-show frame**, before
`0020` removed 88 shows. 159 − 152 = 7, and the 1,095-day gap rule could plausibly account for
seven short-S1 shows. Both `0020` and item 13 are dated 2026-08-12 and their order is not recorded.

**Consequence is small and the ruling does not move** — the exposure bound is 22 accounts, and that
comes from the screen records, not from the frame. But this is a **number in the decision log of
record that its own cited section contradicts**, and that log is the Step 18 artifact.

### X3. `decisions/0018` publishes quintile bins for a frame that no longer exists

- **`0018`**: *"The **title size quintile is cut over the 1,226-show frame**"*, with the adopted
  bins tabled as **247 / 244 / 249 / 241 / 245** (sums to 1,226). `decisions/README.md`'s row for
  `0018` repeats "the 1,226-show frame."
- **`artifacts/step2-frame-ledger-and-distributions.md` §7**: `size_quintile` is
  **238 / 221 / 224 / 227 / 228** (sums to 1,138), "cut over the frame per `0018`."

**The principle survives; the numbers do not.** `0018` decided *cut over the frame, not the
candidates*, and that still holds. What changed is which frame — `0020` cut 1,226 → 1,138 on the
same day. **`0018` predicted its own invalidation in its closing section** — *"every quintile
boundary moves … a quintile label is not a stable identifier"* — and was then not updated when the
event it predicted occurred hours later. README open item 19 gestures at this but does not say the
published bins are superseded.

### X4. The README's authority note omits `0008`, the entry it most needs to name

- **`decisions/README.md`**: *"Entries 0001–0004 and 0013–0020 are Human Lead decisions. **0005–0007
  are agent-taken**, inside a Chained step, and are recorded retrospectively for ratification."*
- **`decisions/0008-step3-seed-source.md`**: *"Taken by: Analytics Engineer, inside a Chained step.
  Authority: **Not a Human Lead decision.** Status: **Open — for ratification.**"* Its second line
  calls it **"the highest-consequence agent choice in Step 3."**

The note also does not cover all twenty entries: 0001–0004 + 0005–0007 + 0013–0020 = 19. `0008` is
the one left out, and the note's stated purpose is to keep the line between "decided" and "defaulted
into" visible.

### X5. The Step 5 artifact says a review is pending that the reviews file records as complete

- **`artifacts/step5-contamination-diagnostics.md`**, header line and closing line:
  *"**Red Team reviews this revision.** Steps 6 and 7 remain blocked pending that review."*
- **`artifacts/step5-red-team-reviews.md`** §6: *"**Round 4 returned PROCEED and all four of its
  corrections have been applied.** The reviewer raised no further objection to the adopted rule on
  its merits at rounds 3 or 4."* Round 4 reviewed **revision 6**, the same revision.

The practical risk is directional and in the wrong direction: a reader of the gate artifact concludes
a review is still owed, when the reviews file says the ball is with the Human Lead. **Neither file is
wrong about the gate itself** — both correctly state it is not approved and that no agent records
approval.

### X6. `artifacts/pool-coverage-check.md` is a superseded snapshot and says nowhere that it is

- **It reports** 2,134 `complete`, **235** `discarded_over_tolerance`, 2,370 contributing users, and
  its own Limits section reads *"2,370 of 4,088 usable pool users, **58%**"* and *"no pull process
  was running at scan time."*
- **The pull has since stopped for good** at 2,549 `complete` / **287** discarded / 2,836 decided /
  **62.9%** (`artifacts/s1-completer-diagnostic.md` §1).

**The comparison that makes this actionable:** the S1-completer diagnostic faced the identical
problem and handled it correctly — it opens *"This supersedes the 2,134-user snapshot"* and
preserves the old outputs at `processed/diag_snapshot_2134u/`. The coverage check got no such
header. Every distributional figure in it — 44,866 shows, the per-show user counts, the 1970 spike
at 285,296 records — is on the smaller cohort and reads as current.

### X7. `0012` changed a rule inside an approved gate and has not been put to Red Team

Carried from `decisions/README.md` open item 15, elevated because the Step 5 gate is now the live
one and this sits underneath it.

- **The standing rule**, from the Step 1 approval record: *an edit that changes a **rule** reopens
  the gate; an edit that adds **evidence** does not.*
- **`0012`** changes the sweep-completeness test in `artifacts/step1-outcome-definition.md` §0 and
  in `0002` condition 2, from exact `item_count` equality to page coverage plus a 2% residual. Its
  own header says *"This changes a rule inside an approved gate artifact … the Human Lead may wish
  to put it to Red Team. Flagged, not decided."*

**The completeness *requirement* is untouched** — a truncated sweep is still never returned as data,
and the reasoning for it is unchanged. Only the *detection test* moved, and the evidence for moving
it is strong (7 of 10 pilot users failed exact equality on HTTP 200 responses; two page sizes
returned identical record sets). **This is not an objection to the change. It is that the study's own
gate-reopening rule was invoked, the exception was taken, and the review it names has not happened.**

---

## Claims whose basis moved — right conclusion, corrected reason

Five in this period. Recorded together because the pattern is now a property of the project, and
because Step 18 records *why* a decision was made, not only what it was. A conclusion that is right
for a newly-stated reason should be logged with the new reason, not the one that was in the room.

| Conclusion, unchanged | Reason that was withdrawn | Reason that holds |
| :--- | :--- | :--- |
| **Recompute `pool_completers` on the full pool** (`0013` condition 2, done in `0019`) | "completer counts only rise" | **False.** 118 shows *fell*, 177 pairs lost, when adding users raised `L1_hat` and moved `F1_hat` to an episode earlier users had not watched — retroactively un-completing them. Counts **move**. All 118 are long-tail; the ≥50 set is untouched, which is why the candidate set is monotone in practice though the statistic is not in principle |
| **C5 needs no separate ruling; the 720 are retained** | "all 425 C5 pairs with no S2 evidence are already inside the 1,542" | **False — the sets are disjoint by construction**, overlap exactly **0**, and the count is **720**, not 425. Holds instead on the insert-time bound (720 at median **1,738 d**, **7.92%** open at `W = 60`, against 40 d and 58.6% for the 1,542), which Red Team independently endorsed as the right test |
| **Exclude the 1,542** (adoption 2) | "these pairs cannot be evaluated against the definition" | **False.** With zero S2 records `\|A\| = 0` for *every* `τ1`; the pair is perfectly evaluable. Holds instead as a **right-censoring defect** — a fabricated-early `T0` lets a pair pass a censoring test it should have failed (Red Team D2) |
| **Cap the tail at 300 forecast pages** (`0010`) | "a 907-page user is roughly six hours alone" | **Wrong by a factor of 60.** At 150 GET/min a 907-call user is **6.0 minutes**; the pool's heaviest user is 6.9 minutes. Holds instead as a **circuit breaker on forecast error** — and the wrong argument would have pointed at a far more aggressive cap, which at 150 pages would have removed 5% of the pool, all from the heavy end |
| **Order the pull so an early stop is survivable** (`0009`) | median-out, "sort by pages, pull median first, work outward" | Median-out leaves a **centered** slice, not a representative one: at ten hours it pulls **no user above 73 pages** in a pool reaching 1,034. Amended before launch to **stratified round-robin**, at a named 12% throughput cost |

**Two of these entered rulings before they were corrected** — the C5 disjointness error and the
insert-time bound quoted from a unit bug. Both are in [[withdrawn-claims-register]].

---

## Closed since 2026-08-11 — verified, do not re-raise

| Was | Item | How it closed |
| :--- | :--- | :--- |
| **O1 / S7** | `pull_date` had no value | **`0011`: `pull_date = 2026-08-11`, `τ_pull = 2026-08-11T00:00:00Z`.** Constraint verified — earliest per-user fetch 05:01:26Z. Right-censoring, D3, D8, D9 unblocked. `0011` carries S7's cost concern as a named consequence: the discarded tail is ~1 day for early-fetched users and ~2 for late-fetched, so **the discarded-record count is not evenly distributed and must not be read as if it were** |
| **N1** | Step 1 §8 read as though question 2 were open, and nothing stated how negatives are handled in the all-shows plot | **Both halves closed, verified line by line.** §8 now reads "It is now **DECIDED as D14**". `task-sheet.md` Step 6 now carries a full **"Rule for the negative mass in the all-shows plot"**: plot signed and untruncated, do not clip or drop; **never read W off the all-shows curve**; report negative mass split by all five D12 buckets; **derive Step 13's range deterministically** by reading the same percentile on both curves. The dual-implementation divergence risk N1 identified is closed at the source |
| **S3** | `reciprocal_pairs: 1353` vs a recount of 1,172 | **README item 12: fixed in `src/step3_backfill.py` and regenerated. 1,172 confirmed.** My per-record double-count hypothesis was correct |
| **S9** | `MIN_EPISODES_USABLE = 10`'s warrant unverified | **README item 13, closed and ACCEPTED 2026-08-12.** The warrant is **not literally true** and that is what was accepted, not denied: `min(L1) = 1`, so a 6-episode account is not arithmetically barred from an in-frame S1 completion. **Exposure at most 22 accounts, 0.5% of the 4,320 screened** — 210 of the 232 rejected had zero episodes. All 232 recoverable at **0 live calls**; a full history pull of all 232 costs 296 pages. **Not** recoverable: what the crawl would have found had they stayed in the frontier. (One figure inside the closure is contradicted — X2) |
| **S10** | README not updated for `0005` | `0005`–`0020` all indexed; open items renumbered to 19. (One gap remains — X4) |
| **S1, S2, S4, S5, S6, S8** | Step 3 write-up items | Absorbed into `0005`–`0008` and README items 10 and 11. **S5/S6 survive as README item 10**, below |
| **O5** | critical path | Superseded — see the current path below |

---

## OPEN — carried forward

### O2. The gap hypothesis is untested and still belongs to no step

Whether Trakt represents a numbering gap by **omitting** the number or by **listing a placeholder**
is unowned. `decisions/README.md` items 3 and 8 both carry it; item 8 exists to say **visibility is
not ownership.**

**One observation now exists, in the benign direction, n = 1.**
`artifacts/step2-frame-ledger-and-distributions.md` §6 finds **exactly one in-frame show with an
internal `E1` gap** — Star Trek: Prodigy, 19 episodes numbered to 20 — and **zero** with an internal
`E2` gap. Nineteen listed for a maximum of twenty means Trakt **omitted** the number rather than
listing a placeholder, which is the branch that leaves `L := |E|` correct. The artifact's own
wording is right: *"remains near-untested."* One show is not the answer; it is one data point, and
it is the first.

**A second Step 2 finding retires part of the original worry.** The four absolute-numbering shows
(*Naruto*, *Naruto Shippūden*, *One Piece*, *Hunter x Hunter*) had histories using the **same**
absolute numbers as the metadata — 100% overlap on all four — so **set membership handles that shape
and the withdrawn `1..F` range form would have failed on all four.** All four have since left the
frame via the 26-episode cap, so the evidence stands but the exposure is gone.

### O4. The `L2 = 1` / cadence-classification ordering is still written nowhere

At `L2 = 1`, `weekly_span = 0`, so `span ∈ {2, 3}` falls through C1 into **C2 "weekly"** under D12
first-match ordering — harmless only because `L2 = 1` shows are excluded, and the exclusion happens
at Step 8 while classification is available from Step 2.

**Does not arise on the current frame: `min(L2) = 2`, zero in-frame shows at `L2 = 1`.** Carried
because the ordering is still unwritten and **the frame changes if the pull resumes.** README item 7.

### README item 10 — the pool's bias, and the diagnostic that cannot detect it

Two mechanisms running the **same** way, **compounding rather than cancelling**, both pushing the
never-started share **down**:

- **Seeding** (`0008`): movie-commenting marks tracking intensity; heavy trackers are likelier to
  continue to S2, to log completely, and to survive the Step 7 liveness filter. Seeds were drawn
  **27 days after the TV Time shutdown** from recency-ordered feeds, so the frame oversamples the
  migration cohort **Step 5 exists to exclude** — and Step 5 removes it *after* the discovery budget
  is spent.
- **Liveness exclusion**, which `task-sheet.md` Step 14 already carries as its one downward bias.

**Step 11 as written cannot clear the study, only fail it.** Both channels select on public-facing
activity, so **agreement between them is not evidence of unbiasedness**, and agreement is the likely
outcome. The remedy is computable from `raw/step3/` at **zero further live calls** — but any such
diagnostic **must condition on *screened*, not *eligible***, or FIFO screening order (1,027 eligible
users never screened, skewed toward depth 2) reads as a depth effect.

**Direction check — PASS.** The liveness *bound* moves the headline **up**; the liveness *exclusion*
moves it **down**. Those are consistent, and it is the pair that is easiest to get backwards.

**Now three exclusions with declared directions, and they do not all run the same way:** seeding
**down**, liveness **down**, the `0010` tail cap **up** (0.93%, negligible in magnitude but named
because every other exclusion is), and Step 5's adopted exclusions **up** on net (ten Started pairs
removed per Never-started pair).

### README item 11 — Step 4 is not expected to finish the pool, and the pull is stopped

~210,500 calls, ~23.4 h. `0009` makes an early stop survivable and `0010` trims 1.7 h. **Whether to
resume or to sample the pool down remains unsettled**, and everything frame-derived moves if it
resumes (README item 19): the ≥50 candidate rule, every size-quintile boundary, the structural
threshold counts.

### README item 18(b) — `show_network` is a present-day value

Problem (a) is closed: per-season network **does** exist on the API and is **empty** — 0.71%
populated, dropped as a field (`0016`). **Platform fragmentation is not a variable in this study**;
no result may control for it, stratify on it, or rule it out. Problem (b) survives and has moved to
a different field: show-level `network` is 100% populated but records **today's** network, so a
title that moved services between seasons shows only its current one. **Must not be read as
release-time availability.**

### README item 2 — Step 1 §10.1 open questions 1 and 3

Still open. The Continued boundary and the right-censoring rule. Each carries a Data Scientist
recommendation and a decision from nobody. See [[step1-open-questions]].

### Critical path, 2026-08-12

Steps 1, 3, 4 (stopped) and 2 are done. **Step 5 is the live gate** — revision 6 FINAL, Red Team
PROCEED, awaiting the Human Lead's written approval. Then Steps 6 and 7 (both dual-implementation,
both blocked), then Step 8. **X1 should be settled before Step 7 launches, not after**, because the
dual-implementation diff will not surface it.

### 403 and 429 — one of three failure paths is live-tested

README item 9. **Step 4 has now run** and, per `artifacts/pool-coverage-check.md` §1, saw
`access_denied` **0**, `private_or_absent` **0**, `user_403_skipped` **0** across 102,798 persisted
history pages, every one a 2xx payload. **So Step 4 did not exercise the 403 rule either**, and
README item 9's wording — *"Step 4 is now the first exercise"* — is stale in the same way its
predecessor was. The retry-with-backoff branch remains the only live-tested path.

### N2, N4, N6 — carried unchanged, not re-verified this pass

N2 (D2 computed on definition (b) cannot count the (a)-style failure the §5 addendum points at;
**expect zero, and zero is not evidence of rarity** — now also README item 6). N4 (the
`episode.ids.trakt` disagreement mechanism is asserted and unobserved, and it is the mechanism D9's
split signature depends on — README item 5). N6 (the Step 0 file index is stale). Last verified
2026-08-11.

---

## Checks that PASS — recorded so they are not re-litigated

Verified 2026-08-12. Arithmetic reconciliations are in [[population-chain-steps-2-3-4]].

- **Step 5's rule composes correctly with Step 1's filter order.** Adoption 2 excludes 1,542 pairs
  *on a censoring rationale*, applied as a **contamination** exclusion — and `task-sheet.md` Step 8
  requires contamination to run **before** right-censoring precisely so *"an import-stamped S1
  completion date is counted as contamination rather than laundered into a censoring drop."* The
  Step 5 rule is the first live instance of that ordering doing what it was written to do. Not a
  contradiction — a confirmation.
- **The §16 routing of the 720's bound figures to `revision4.json` is correct, not stale.** I
  checked the file directly: `processed/step5/revision4.json` was regenerated and carries **1,738 /
  1,717 / 1,762**, the corrected values. The 425 and 295 sub-rows also reconcile to the corrected
  **7.92%**, not the withdrawn 8.06%. **This was the obvious place for the unit bug to have survived
  and it did not.**
- **No superseded Step 5 exclusion figure is quoted as current.** The revision table labels 71,235
  / 24,609 / 1,542 as history; §9.5 recosts every rejected candidate on the adopted population and
  says so; §8 gives **both** denominators so the E6 correction is checkable.
- **"Clock start" is now used uniformly.** The B1 collision is fixed: Step 5 §7 states *"`T0` is the
  clock start; **S1 completion date** and **finale term** are its two inputs; **binding term** is
  whichever `max()` selects."* Grepped every `.md` in the repo — no remaining use of "clock start"
  to mean the S1 completion instant alone.
- **Step 2's rate discipline was verified, not asserted** — max **150** requests in any rolling 60 s
  window, checked against the persisted throttle ring. The run's own `shows_per_min` counter reading
  318 is a cumulative-average artifact of a front-loaded limiter and **not** a breach; the artifact
  says so, which is the right handling of a misleading counter.
- **Step 2's metadata integrity checks all return 0.** `episode_count` / `aired_episodes` / `|E|`
  agree on every in-frame show for both seasons. The listed-but-unaired hazard §3.4 predicted does
  not reach the frame — removed by the 31 Dec 2025 cutoff, **verified rather than expected.**
- **Privacy boundary intact.** All 2,549 usernames tested against every file in `artifacts/` and
  `decisions/`; only `right` and `orphan` match, both ordinary English words. Step 2 shows titles,
  which are public catalogue metadata. Account-keyed material stays in `processed/step5/` and
  `raw/`.
- **Zero API calls in Step 5 and all six of its revisions**, and zero in both diagnostics. The
  request log's last entry is the Step 2 shows pull; no `step5` run label exists. Step 2's rebuild
  cost is **0 calls** — all bodies cached.
- **`0012`'s residuals are not truncation**, on two independent proofs: page-count and item-count
  headers identical on every page of every sweep including one of 105 pages; and a `limit=100`
  re-sweep returned the **identical record set in identical order** as the cached `limit=250` sweep,
  1,459 distinct records both ways against a header claiming 1,460.
- **D12's fragility test passes on real data.** 7 shows within one day of a bucket boundary, 0.6% —
  so by D12's own test the thresholds are **not load-bearing** and a Step 13 arm on them is not
  indicated. The 238-within-three-days figure is not the right one: 220 of those are same-day drops
  whose distance is exactly 2 by construction.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[gate-step5-contamination]], [[population-chain-steps-2-3-4]], [[decision-log-step18]],
[[withdrawn-claims-register]], [[step1-open-questions]].
