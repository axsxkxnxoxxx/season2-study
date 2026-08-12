# Decision 0020 — The Step 2 structural thresholds: no minimum season size, maximum 26 episodes, maximum 1,095-day gap

| | |
| :--- | :--- |
| **Decision** | **No minimum season size.** **Maximum 26 episodes on either S1 or S2.** **Maximum 1,095 days between the S1 finale and the S2 premiere.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Closes** | [0014](0014-no-content-filters-structural-fields.md), which dropped the content-category filters and deferred these thresholds until the distributions were visible. **0014 moves to Closed.** |
| **Effect** | Frame **1,226 → 1,138 shows**, 232,958 → **220,107** S1-completer pairs |
| **Status** | Closed |

---

## The order these were decided in, and why it matters

[0014](0014-no-content-filters-structural-fields.md) set a deliberate sequence: **look at the
distribution, then draw the line.** A threshold chosen before the distribution is visible is a
guess, and a guess that shapes the population is the kind of thing entries 0005 through 0008 exist
to flag.

That sequence was followed. The frame was built with **no** structural exclusion, its distributions
were reported in `artifacts/step2-frame-ledger-and-distributions.md` §3.1 and §3.2 along with the
show and pair counts each candidate cutoff would remove, and these thresholds were set against
those numbers.

## No minimum season size

**Rationale as given: season length comes from the frame per show, and the 90 percent rule handles
short seasons correctly.**

The approved Step 1 §4 rule is `F1 ∈ D1` and `|D1| ≥ ceil(0.90 × L1)`, where `L1` is now the real
per-show season length from the Step 2 frame rather than a proxy
([0019](0019-pool-completers-recomputed.md)). The bar therefore **scales with the show**: a
three-episode season demands three episodes, an eight-episode season demands eight (7/8 is 87.5%,
below the bar). There is no sense in which a short season is measured more loosely than a long one,
so a floor would not be correcting a measurement defect.

What a floor **would** have done is remove the frame's largest titles. A `≥4` rule looked nearly
free at 13 shows, but 2,264 of the 3,125 pairs it removes belong to **Black Mirror (1,211)** and
**Sherlock (1,053)** — two of the highest-completer shows in the study, both three-episode seasons.
A `≥10` rule would have cost 443 shows and 89,396 pairs, 38% of the frame.

Consequence, stated plainly: **the frame retains `L1 = 1`** (Æon Flux, 55 pairs) and `L1 = 2`. At
`L1 = 1` the completion rule reduces to "watched the single episode." That is the rule behaving as
written, not an exception to it, and Step 1 §7 already retains `L1 = 1`.

## Maximum 26 episodes, on either S1 or S2

**Rationale as given: 26 is the traditional full broadcast season, so it separates shows made on a
normal season cycle from shows made continuously.**

That is the structural distinction the dropped content filters were reaching for, expressed as the
property itself rather than as genre. A show producing 40, 60 or 80 episodes in a season is not
running a season cycle; "finished season 1, never started season 2" does not carry the same meaning
for it, and that is the concern [0014](0014-no-content-filters-structural-fields.md) named.

**The cut is insensitive across a wide range, which is why 26 is defensible rather than arbitrary.**
Pairs removed, as a share of the 1,226-show frame:

| Cap | Shows cut | Pairs cut | Share of pairs |
| ---: | ---: | ---: | ---: |
| > 22 | 196 | 32,243 | **13.8%** |
| > 24 | 114 | 15,020 | 6.4% |
| **> 26** | **51** | **5,644** | **2.4%** |
| > 30 | 36 | 3,904 | 1.7% |
| > 40 | 23 | 2,588 | 1.1% |
| > 50 | 15 | 1,767 | 0.8% |

**Anywhere from 26 to 40 the frame changes by at most 1.3 percentage points of pairs.** The choice
inside that band is not load-bearing, which is the property a threshold should have.

**22 was considered and rejected.** It cuts **196 shows and 13.8% of pairs** — a jump of more than
5× over 26 — because it reaches into ordinary network drama, which is exactly the population the
study is meant to measure rather than exclude. The cliff sits between 24 and 22, not at 26.

What 26 removes is recognisably the continuous-production group: *Grey's Anatomy*, *Naruto*,
*Naruto Shippūden*, *Dragon Ball Z*, *One Piece*, *Hunter x Hunter*, *Pokémon*, *SpongeBob
SquarePants*, *Batman: The Animated Series*, *Star Trek*, *Last Week Tonight*.

### The size cap is partly a cadence threshold, and that has to be recorded

**Of the 51 shows the cap removes, 44 are C4 (slower than weekly), 6 are C3 and 1 is C2. None is
C1.** The mechanism is not subtle — a long season stretches the premiere-to-finale span, and D12
classifies on that span — but the consequence is:

> **The size cap is not cadence-neutral. It is partly a cadence threshold in disguise**, and it
> falls almost entirely on **C4**, the bucket where abandonment is **most likely to be
> exposure-driven** rather than preference-driven. A viewer facing a season that takes a year to
> release has more opportunity to lapse for reasons that are not about the show.

C4 is a required Step 9 stratum under D12. It drops from **476 to 425 shows**, and any C4 result is
now computed on a population from which the longest-running titles have been removed. **A C4
headline must not be read as a statement about slow-release shows in general.** This is stated here
so that no later step rediscovers it as a surprise, and so it is not mistaken for a finding about
cadence when it is an artifact of the size rule.

The related confound is already on record: air period and cadence are strongly collinear
([0017](0017-air-period-definition.md)), and the size cap interacts with both.

## Maximum gap 1,095 days

Three years, S1 finale to S2 premiere. It removes **37 shows and 7,207 pairs, 3.1% of the frame** —
the revival tail, where a viewer's failure to start S2 is a statement about a three-year absence
rather than about the show.

The distribution made the alternative unattractive: the **median gap is 315 days**, so any cutoff at
or below a year cuts the body of the distribution rather than a tail. A 365-day rule would have
discarded 43% of pairs. At 1,095 days the rule is a tail rule, which is what was wanted.

One show has a **negative** gap — *That's So Raven*, S2 premiering 155 days before the S1 finale,
Trakt's season boundaries disagreeing with broadcast order. **No lower bound was set, so it is
retained.**

## Application and final counts

Applied in the order decided — season size, then gap — as ledger steps 6 and 7 in
`artifacts/step2-frame-ledger-and-distributions.md` §2:

| # | Rule | Removed | Remaining |
| :-- | :--- | ---: | ---: |
| 5 | *(prior state: S2 finale on or before 2025-12-31)* | — | 1,226 |
| 6 | **Season over 26 episodes (S1 or S2)** | **51** | 1,175 |
| 7 | **Gap over 1,095 days** | **37** | **1,138** |

The two rules overlap on exactly **1** show, so applying them in the other order gives the same
frame.

**Final: 1,138 shows, 220,107 S1-completer pairs** — 92.8% of the shows and 94.5% of the pairs of
the unthresholded frame. In-frame ranges are now `L1` 1–26, `L2` 2–26, gap −155 to 1,085 days.
Cadence: C1 206, C2 340, C3 167, C4 425, C0 0.

## What this closes, and what it does not

**Closes [0014](0014-no-content-filters-structural-fields.md).** Its deferred thresholds are now
set, and its platform-fragmentation item was resolved by
[0016](0016-per-season-network-dropped.md). Both open items are discharged.

**A headline computed on this frame is no longer provisional on the threshold ground named in
0014.** It remains provisional on everything else that is unapproved: the Step 5 contamination
rule, the Step 6 window `W`, the Step 7 liveness threshold and the Step 8 analysis table are all
unapproved gates, and nothing downstream of them runs without written approval.

**The frame still rests on a stopped pull** at 62.9% of plan. If it resumes, the candidate set
grows and these thresholds are re-applied to a larger frame — the thresholds themselves are
population-independent, but the counts above are not.
