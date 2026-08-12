---
name: withdrawn-claims-register
description: The study's own error log — claims asserted and later withdrawn or corrected, organised by failure mode, now covering Steps 1 through 5 and including the three errors that reached the Human Lead and the two that entered rulings
metadata:
  type: project
---

# Withdrawn-claims register

**Why this file exists:** every claim below was asserted confidently, survived at least one review,
and was later found false. The value is not the list — it is the **taxonomy**, because the same four
failure modes keep recurring and each one is checkable in advance.

**How to apply:** when reviewing any gate artifact, run all four checks below. They are cheap and
they have all caught something.

## The four failure modes, and the check that catches each

| # | Failure mode | The check |
| :--- | :--- | :--- |
| **A** | **Asserting a property that does not follow from the definitions given**, or naming an object without making it operational | Check every *"therefore"*, *"guarantees"* and quantitative range against the definitions **in the same document**. Check every named object for a numeric threshold. Reject "on the order of", "near zero", "approximately", "expected to be zero" |
| **B** | **Quoting a figure from a source that does not produce it.** Dominant mode in Steps 4–5, raised **four times** as B3, D3, F3 and again at round 4 | Grep the figure to a **file and a key**. An uncommitted figure is an **unverified** figure — proved when the decorative "164" was finally committed and turned out to also be **wrong** |
| **C** | **Quoting a cost against a baseline that no longer exists** | For every cost in a rejected-alternatives table, name the population it is computed on and check that population is still the adopted one |
| **D** | **A unit or order-of-magnitude error that nobody re-derived** | Sanity-check any figure that crosses a unit boundary — per-minute vs per-hour, nanoseconds vs microseconds — against a second route to the same number |

---

## Mode A — the original family, from Step 1

Twelve rows sit at the head of `artifacts/step1-outcome-definition.md`: **eleven withdrawn or
corrected claims plus one accepted risk (B2).** Recounted against the file; the table must not be
pruned. Six are false-by-construction:

| Claim | Why it was false |
| :--- | :--- |
| `p ∈ (0, 1]` follows from `p = m / L2` | Not when `F2 > L2`. Fixed by making `p` rank-based |
| Rank-based `p` is safe because out-of-set episodes are dropped upstream | The old drop rule caught `number > F`, `number < 1` and missing fields — an episode numbered *inside* `1..F` but *absent* from the listed set survived all three |
| Right-censoring at `T0 + max(W, 91)` guarantees 91 days of post-window observation | **False by subtraction.** The guarantee is `max(0, 91 − W)`: **zero** at any `W ≥ 91`. Fixed by declaring `H` |
| D3 and D8 measured "to the pull date" are rates | Exposure-weighted mixtures weighted by **show recency**. Fixed by the constant horizon `H` |
| "On or before `T1`" is a single unambiguous operator | Ambiguous by one day, on the operator that assigns **every** outcome state |
| A show is weekly when its span is "on the order of" `(L2−1)×7` | Not thresholds and not exhaustive; a required stratum with unassigned members gets silently pooled |

Five framing corrections: entry/exit are **not** symmetric (S1 evaluated over all time, S2 within
`W`); right-censoring does **not** cost zero rows; truncating negative lags at zero was withdrawn
because it made `W` a function of the frame's cadence mix; "pull date needs no definition" was
load-bearing in four places; **liveness is a pair-level filter**, not a statement about the account.

### Mode A continued into Steps 3–5

| Claim | Where | Correction |
| :--- | :--- | :--- |
| *"A user with fewer than 10 episodes logged **cannot** have completed any season 1"* | `src/step3_user_discovery.py:43-45` | **Not true.** `min(L1) = 1` over the frame. Stated as a certainty and is not one. Accepted rather than fixed — exposure bounded at 22 accounts |
| *"Timestamp accuracy is not a concern for this study. The outcome is whether someone watched season 2, not when."* | Step 5 revision 3, its **governing principle** | **Withdrawn.** It described an ever-started study. Step 1 §7 makes the outcome operator a **timestamp comparison**, `\|A\| = 0` under `watched_at < τ1`. Red Team D1 |
| *"These pairs cannot be evaluated against the definition"* (the 1,542) | Step 5 revision 3 | **False.** With zero S2 records `\|A\| = 0` for every `τ1`. Re-ruled onto a **censoring** defect. Red Team D2 |
| *"The whole 7,340 partly-stamped population is unanswerable until `W` exists"* | Step 5 revision 4 §12 | **False for 2,352 of them** — if the first S2 watch is clean, `c ≤ s ≤ finale ≤ T0 < τ1` at any `W`. The artifact **computed the split, printed it, and then declared the whole set open.** Red Team F2 |
| *"128,099 under every reading"* | Step 5 revision 3 | Proved for two readings, **false for R3**, which grows the sample to **131,043**. Withdrawn rather than defended. Red Team E3 |
| R3's precedent is Step 1 §2.3 | Step 5 revision 3 | §2.3 governs *which records count as watching* and says nothing about timestamps. The operative rule is **§2.2**. Red Team E4 |
| *"Completer counts only rise"* as the pool grows | `decisions/0013` condition 2 | **118 shows fell**, 177 pairs lost. Counts **move**. Corrected by `0019` — the instruction was right, the reason was wrong |
| *"There is a real trough between 7 and 180 days"* | Step 5 revision 1 | A **bin-width artifact**; per-day density is monotone decreasing throughout. 180 days is a conservative judgment, not a data-determined break. The only real break is at **7 days**. Red Team C1 |
| *"Duplicate accounts: none found"* / *"ten duplicate accounts"* | Step 5 revisions 1–2 | The ten were **mode-3 artifacts**. The negative is **conditional** — an import-only duplicate leaves no real-time records and 251 accounts are untestable. Red Team C4 |
| *"Every retained pair has a clock start with a real logging date behind it"* | Step 5 revision 1 | Overclaim; pairs reach the completion threshold through an ordering that includes fabricated dates. Red Team C5 |
| *"The best account rule leaves 21.1% on a fabricated clock start, the pair rule 0%"* | Step 5 revision 1 | **Circular** — the pair rule is *defined* as removing exactly those pairs. Red Team C2 |

---

## Mode B — figures quoted from sources that do not produce them

**Raised four separate times, each time inside work written to answer the previous occurrence.**

1. **B3, round 1.** Layer 4, the bot table and §8 all rested on `days_over_48` from
   `processed/step5/throughput.npz` — **written by nothing in `src/`.** It also disagreed with the
   version-controlled measure: 1,970 / 580 / 39 committed against 2,183 / 844 / 175 published, and
   a 50→48 threshold change cannot take a count from 580 to 844. Once committed, the bot count fell
   **175 → 126** — exactly the import inflation the code claimed to control for.
2. **D3, round 2.** §10's headline C5 figures were not in the repository; the named derivation
   (`step5_rule_costs_v2.py`) **computes no shift at all**. The committed three-class median of
   **29.5 d** — the least alarming figure available — was **absent**, while the artifact led with
   153.4 d. *B3 recurring, inside the section written to answer Red Team.*
3. **F3, round 3.** Revision 4 **affirmatively certified** that every figure came from committed
   code. False for **nine**, two of them the same rows D3 was about. *"A gate artifact that falsely
   certifies its own reproducibility is worse than one that makes no such claim — the false
   certificate defeats the check the Human Lead would otherwise run."*
4. **Round 4, fourth occurrence.** Revision 5's replacement blanket sentence — *"No figure in this
   artifact is produced outside `src/`"* — was falsified by a single decorative figure, "up to
   **164** accounts share one instant." The reviewer called it decorative and said holding on it
   would be scrupulosity.

**Committing the 164 revealed it was also wrong. The true maximum is 198** — 164 had been the
maximum over the **first 4,000 of 155,626** qualifying groups in an exploratory shell.
`mode3_flags.npz` is byte-identical after recomputation, so nothing downstream moved.

> **This is the load-bearing lesson of Step 5: an uncommitted figure is an unverified figure.**
> It was raised four times, dismissed once as decorative, and the decorative one was wrong.

**The fix that finally worked** is not a promise: revision 6 §16 is a **routing table — per section,
per key, exhaustive, no blanket claim** — so any figure greps to exactly one file and one key.

---

## Mode C — costs quoted against baselines that no longer exist

- **E2.** P2's "+16,632" and P3's "+29,858" were computed on the 195,498 Layer-2 survivors, and
  **Layer 2 is not adopted.** On the adopted population they are 16,665 and **50,533** — P3
  understated by **41%**, in the one table that tells the Human Lead what was refused.
- **E6 / revision 3's "40,720 / 23.7%".** Header quoted the full population; percentages were
  computed on the abandoned Layer-2 survivor subset. Dividing the same numerator by the full
  denominator gives 20.9%, which **mixes two bases**. Withdrawn; **32.5% and 26.2%** are the figures
  on the two populations that actually exist, and both denominators are now published.
- **The 30 : 1 ratio (F1).** `46,642 / 1,542`, **ignoring the 16,665** — a removal running the other
  way and itself **10.8×** the 1,542. Against the net exclusion the ratio is **3.1**. "Thirty times
  larger" and "dominant" were not established. Its numerator is also an **upper bound on pairs at
  risk, not a count of flips**. Round 2's "roughly 26 times larger" (E1) is the same error one
  revision earlier.
- **§5's 11.3%.** Attached to the **excess** when it is the share of the **full wave**; present since
  revision 1 and repeated through revision 5. The excess is **10.6%**. Both figures are now attached
  to the quantities they belong to.
- **Step 4's ~86,000 calls.** Divided `total_plays`, **absent from 77% of `users/:id/stats` bodies**,
  so most users forecast as exactly one page. True figure **~210,500**, a **2.4×** error, and it is
  what `0010` cites as the reason a forecast-error circuit breaker is needed at all.
- **`0012`'s "24 of 235 under-count discards."** Read from a **mid-run snapshot of 2,372 users.** On
  the final ledger it is **31 of 287**. Same class as E2 — a figure computed on a population that
  had moved by the time it was published. Corrected in `0023`.

### The sharpest instance: an indifference band quoted as headroom

**`0012` states a replay "with a maximum residual of 0.86 percent against the 2 percent tolerance."**
`artifacts/step4-pilot-counts.json` records `max_abs_share_of_item_count: 0.11707` — **11.7%** —
with a signed range of −191 to +131. **A reader of `0012` alone concludes the tolerance carries 2.3×
headroom over the worst observed case. It never did.**

Worse than a wrong number: the pilot's p95 is **1.4%** and p99 = max is **11.7%** with nothing
between, so **every tolerance from ~1.5% to 11.7% gave the identical partition of those 20 users.**
The quoted figure was not evidence for 2% over any alternative — it was a coincidence of where the
band happened to be read. **The most aggressive end of the band was chosen, with no sensitivity
table, and the choice was not stated as a choice.** On the full run the gap does not exist: 168 of
the 287 discards (58.5%) sit in the 2–5% band. `0023`.

### A claim attached to a phenomenon that has never been observed

**`0012`'s third required output cites "5 duplicates in 14,236 records" as *genuine cross-page
duplicate records*** and builds a required-output obligation on them. Instrumentation records
`cross_page_duplicate_records: 0 affected users, 0 affected records` across 2,137 users and
22,725,090 records. **Cross-page duplicates have never been observed in either run.**

The anomaly that *does* occur is **within-page** — 147 records, the same `id` twice on one page,
meaning a 250-slot page carried 249 distinct records. It is **not a required output, is described
nowhere, and has no stated interpretation.** So the rule mandates measuring something that does not
happen while the thing that does happen is unmeasured and unexplained. Corrected in `0023`; the
adopted rule is unchanged.

---

## Mode D — unit and order-of-magnitude errors

Both of these reached the Human Lead and one entered a ruling.

**"A 907-page user is roughly six hours alone."** At the study's **150 GET/minute** throttle a
907-call user is **6.0 minutes**; the pool's heaviest user is 1,034 pages = **6.9 minutes**. Six
hours is what you get at **150 calls per hour** — and the 23.4-hour whole-pool estimate is computed
at 150/minute, so the two cannot both hold (210,500 calls at 150/hour would be **58 days**).
**Consequence: no single user can stall the run**, so the tail cap has no defence as protection
against a slow user. `0010` records the correction rather than quietly fixing it, because **a cap
defended by the wrong argument is a cap nobody can re-derive later** — and the wrong argument
pointed at a much more aggressive threshold.

**"Median 2,150 days, 8.1%" for the 720.** Quoted as canonical and **written into the D1-round
ruling**. It required **two** departures from the correct basis, and the cause of the second was a
unit bug: **`.astype("int64")` on a tz-aware datetime returns microseconds in the pandas version in
use**, so dividing by 1e9 placed every S2 finale in **January 1970** and the `max()` against it was
**silently inert.**

| Basis for the bound | `max()` with finale | Median elapsed | Open at `W = 60` |
| :--- | :--- | ---: | ---: |
| **Completion prefix — the figure to use** | **yes** | **1,738 d** | **7.92%** |
| Completion prefix | no | 2,190 d | 7.92% |
| Any S1 record | yes | 1,728 d | 8.06% |
| Any S1 record | **no — what was quoted** | **2,150 d** | **8.06%** |

**Caught from arithmetic alone:** `max(finale, x) ≥ x` can only push `T0` **later** and elapsed
**smaller**, so 2,150 > 1,738 is impossible with the `max()` in force on the same set. The finale
term binds for **61.8%** of the 720, which is why its absence moves the median by ~450 days.

**The first correction to this was itself wrong** — it claimed the `max()` had been included and only
the basis differed. Recorded because a correction that is not re-derived is just another claim.

---

## The three errors that originated in the main session and reached the Human Lead

Caught by the analytics-engineer. **Two entered rulings.**

1. **C5 reported as 4,188 against the artifact's 5,694**, on the basis that
   `pair_contamination.csv` had no column for air-date-stamped S1 evidence. **It does** —
   `s1_ev_airdate`, added in revision 2, after the header had been read. 5,694 is correct; 4,188 is
   the two-class subset.
2. **"All 425 C5 pairs with no S2 evidence are already inside the 1,542."** **False. The sets are
   disjoint by construction** — C5 requires a *clean* completing record, the 1,542 a *contaminated*
   binding one. Overlap is exactly **0** and the correct count is **720**. **The ruling that C5
   needs no separate ruling cited this claim as half its basis.**
3. **The 2,150 d / 8.1% figure above**, quoted as canonical into a ruling. Method-dependent and
   produced by the unit bug.

**All three conclusions survive**, on evidence Red Team independently endorsed as the right test.
**The stated bases did not.** See [[open-items-and-contradictions]] "Claims whose basis moved."

---

## Step 3's three, closed

Funnel floor line printed **6** when the true total was **232** (a per-round column summed wrongly
into a funnel row). *"Zero errors"* when the run had **16 HTTP 5xx, 1 transport error, 9 transient
retries** — all recovered, which is why the retry-with-backoff branch is the one live-tested failure
path. `reciprocal_pairs: 1353` was a **per-record double count**; the true value is **1,172**, since
fixed and regenerated.

## The one accepted risk

The liveness bound is inflated, and it stays that way by Human Lead ruling. A bound that
reclassified the pairs it could explain away would no longer be a bound. Full reasoning in
[[gate-step1-outcome-definition]].

## One premise still asserted and unobserved

That Trakt metadata merges and splits make `episode.ids.trakt` disagree with `(season, number)`.
Zero disagreements on the probe profile — **not contradicted, untested.** The same mechanism
underwrites D9's split signature. [[open-items-and-contradictions]] N4.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[gate-step5-contamination]], [[open-items-and-contradictions]].
