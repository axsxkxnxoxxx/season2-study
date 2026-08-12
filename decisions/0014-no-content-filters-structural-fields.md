# Decision 0014 — No content-category filters in the Step 2 frame; selection is structural, and the thresholds are deferred

| | |
| :--- | :--- |
| **Decision** | The **anime exclusion and the daily-strip/soap exclusion are dropped.** The Step 2 frame applies **no content-category filter**. Release structure is recorded as **fields** — gap length, season size, platform fragmentation, cadence bucket — and the Human Lead sets structural thresholds **after** seeing their distributions. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Supersedes** | The two content filters as originally specified for Step 2. Nothing in the decision log had adopted them; they are dropped before first use. |
| **Status** | **Open** — the deferred thresholds are not yet set. See the two open items below. |

---

## Why the content filters were dropped

The concern behind "exclude anime" and "exclude soaps" was never genre. It was **release
structure** — that some titles release on a cadence, a season size, or an availability pattern under
which "finished season 1, never started season 2" does not mean what it means for a
twice-a-year prestige drama.

Genre is a poor proxy for that, in both directions. It over-excludes — plenty of anime releases in
exactly the seasonal cours structure the study is built to measure — and it under-excludes, since
non-anime titles run daily strips and non-soaps run 200-episode seasons. It also imports an
operational problem the study gains nothing from owning: Trakt's genre tagging is inconsistent, and
an anime rule lands differently depending on whether it keys on genre, country of origin, or
language. Every one of those three would produce a different population, and none of them is the
thing being controlled for.

**The structural properties are directly measurable.** Given that, a content filter is a lossy
stand-in for a field the frame already has to record.

## What replaces them

Nothing, at the filter stage. The frame records release structure as fields — gap length between
seasons, S1 and S2 episode counts, cadence bucket per the **D12 classifier** (the cadence rule in
the Step 1 outcome definition, not decision [0012](0012-sweep-completeness-rule.md)), premiere and
finale dates, air period, platform — and the Human Lead sets thresholds on those fields once their
distributions are visible.

This is the deliberate order: **look at the distribution, then draw the line.** A threshold chosen
before the distribution is visible is a guess, and a guess that shapes the population is the kind of
thing entries 0005 through 0008 exist to flag.

## Open item: the thresholds are deferred, not skipped

**Until the Human Lead sets them, the frame carries no exclusion on gap length and no exclusion on
season size.**

The consequence has to be stated plainly rather than discovered later: **any headline computed
before those thresholds are set is provisional.** It is computed over a population that includes
whatever release structures the candidate set happens to contain, including the ones the dropped
content filters were reaching for. A provisional headline is usable for diagnostics and for seeing
the distributions. It is not the study's result, and it must not be reported as one.

This is an open item, not a closed decision, and this file stays **Open** until the thresholds are
written.

## Open item: platform fragmentation is unverified

Platform fragmentation is one of the three structural properties the Human Lead cares about, and it
is the one that **may not be measurable at all.** Two distinct problems:

1. **It may not be exposed per season.** It is not established whether Trakt gives a per-season
   network or distributor, or only a single network on the show record. If it is one field per show,
   the concept "this show's seasons were split across services" has no representation in the data
   and cannot be computed from it.

2. **A present-day field may not describe the release.** Fragmented titles frequently consolidate —
   a season that originally landed on one service and its successor on another often end up on the
   same service years later, and the record reflects **today's** availability. The thing that would
   have affected viewing is availability **at the time of release**, which a current-state field
   does not carry.

The second problem is the harder one, because it survives the first: even if Trakt does expose
per-season networks, a per-season network read in 2026 is not evidence about what a viewer faced in
2021.

**Resolution rule: if it cannot be measured, it is dropped as a field and the limitation is stated**
— in the frame's write-up and again wherever a structural threshold is justified without it. It is
not silently omitted, and it is not approximated with a present-day value presented as a
release-time one.

## What the frame still filters on

Dropping the content filters does not make the frame unfiltered. These remain, and they are
structural or availability rules rather than content categories:

- **Candidate set:** shows with ≥50 S1 completers in the pool, from the completer diagnostic —
  recomputed on the full pool per [0013](0013-step2-execution-delegation.md) condition 2.
- **Season 0 is filtered** from all episode-set and length computations.
- **A show is included only if it has a real season 2 whose finale aired on or before
  2025-12-31**, on real air dates from the seasons endpoint — not on the max-observed or
  watch-date proxies.
- **Real season lengths and real episode number sets throughout.** `F := L` is forbidden by the
  approved Step 1 definition and no proxy substitutes for it here.
