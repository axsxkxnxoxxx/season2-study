# Decision 0030 — The 2024/2025 contradiction corrected, and three frame field changes

| | |
| :--- | :--- |
| **Decision** | **The 2025-12-31 cutoff stands.** Step 1's two false figures are corrected **by post-approval addendum, not by editing approved text**. `task-sheet.md` Step 2's date is fixed in place. Step 14 gains the censoring margin and its cohort asymmetry. **`show_network` is dropped**; **`rating`, `votes`, `comment_count`, `subgenres` and `airs.day` are added**; **`size_quintile` is separated from exposure.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Occasioned by** | `reviewer-product`'s Step 2 review — findings 1, 2 and 4, and its flagged date inconsistency |
| **Amends** | `artifacts/step1-outcome-definition.md` (addendum only); `task-sheet.md` Steps 2 and 14; `processed/step2/frame.csv`; supersedes part of [0016](0016-per-season-network-dropped.md) |
| **Status** | Closed |

---

## 1. The 2024 / 2025 contradiction

Step 1 stated the frame caps the S2 finale at **31 Dec 2024** in five places and built its
right-censoring margin argument on it. The frame was built at **2025-12-31** ([0014](0014-no-content-filters-structural-fields.md)),
and `task-sheet.md` Step 2 still said 2024.

**The Step 1 gate is NOT reopened.** Step 1 does not *set* the cutoff — it *relies* on it. The
cutoff is Step 2's rule and the Human Lead moved it. Nothing in Step 1's rules changed, which
distinguishes this from [0012](0012-sweep-completeness-rule.md), where a rule inside §0 was amended
and the reopening clause was reached.

**Two supporting figures are false, and both are corrected by addendum**, following this document's
own precedent of a post-approval addendum marked *"evidence only, no rule changed"*:

1. The cap is **2025-12-31**, not 2024-12-31.
2. The horizon is **199 days**, not 182 — line 823 assumed `max(W, 91) = 91`, and the adopted `W` is
   **108**.

**The conclusion survives. The margin does not.**

| | Cap | Horizon | Latest `T0` | Clearance |
| :--- | :--- | ---: | :--- | ---: |
| As Step 1 wrote it | 2024-12-31 | 182 d | 2026-02-10 | **~13 months** |
| As actually built | 2025-12-31 | 199 d | 2026-01-24 | **24 days** |

**Zero shows are lost at `W = 108`** — 214,858 of 220,107 pairs retained, 97.6% — which is why the
cutoff stands. But `W` is itself **±18 days** show-clustered, so the slack is now smaller than the
uncertainty in the number consuming it. Both facts are now Step 14 limitations.

**The censoring is cohort-asymmetric**, and this is the part worth carrying. The loss falls entirely
on the uncapped `S1_completion_date` term:

| Air period | Pairs kept at `W = 108` | at `W = 213` |
| :--- | ---: | ---: |
| pre-2020 | 98.0% | **97.3%** |
| 2020–2022 | 97.5% | 96.4% |
| **2023–2025** | 96.0% | **89.7%** |

Survivors from recent titles are those who completed S1 early — **early adopters, the users likeliest
to continue.** So the `W = 213` arm added by [0027](0027-step13-w-arms-above-the-adopted-value.md) to
test the censoring bias **is itself the most censored arm**, and it censors hardest in the cohort
whose behaviour it exists to probe.

## 2. `show_network` is dropped

[0016](0016-per-season-network-dropped.md) dropped *per-season* network and retained *show-level*
network as a descriptive field, disclosing it as a **present-day** value. **That characterisation was
too generous**, and this entry supersedes it.

Checked against the frame, the field errs in **both** directions:

| Title | Broadcaster at S1/S2 | `show_network` |
| :--- | :--- | :--- |
| Arrested Development (S2 2005) | FOX | **Netflix** |
| Lucifer (S2 2017) | FOX | **Netflix** |
| Designated Survivor (S2 2018) | ABC | **Netflix** |
| Manifest (S2 2020) | NBC | **Netflix** |
| Community (S2 2011) | NBC | **Yahoo! Screen** |
| Brooklyn Nine-Nine (S2 2015) | FOX | **FOX** — but it *ended* on NBC |

**So it is not present-day, not release-time, and not consistently either.** That is strictly worse
than the disclosed defect: a present-day value has a known direction of error you could bound; this
has none. *Community* tagged Yahoo! Screen is neither — Yahoo! Screen no longer exists.

**73 of the 177 Netflix-tagged shows have a pre-2020 S2 finale.** Some are genuine Netflix originals;
the rate of error cannot be determined without a title-by-title audit.

**Why dropped rather than warned.** "Streaming vs linear" is the first cut a slate owner asks for,
and this field was 100% populated with 150 distinct values, sitting exactly where the answer would
go. A §"descriptive field only" caveat is not a strong enough guard against a field that tempting: a
Step 12 cut run on it would produce a result that is **actively misleading and looks clean**. **A
field that cannot be used is safer absent than present.**

*One correction to the review that raised this: its `The Killing` example does not hold. The frame's
row is the Danish original (S2 finale 2009, network DR1), not the AMC remake. The other six stand.*

## 3. A reception axis is added — `rating`, `votes`, `comment_count`, `subgenres`, `airs.day`

All were already in the cached `GET /shows/:id?extended=full` bodies on disk. **Zero API calls, zero
new privacy surface, no inclusion rule touched** — the frame is still 1,138 shows and 220,107 pairs.

**The frame previously had no reception axis at all.** Its only measure of a title's standing was
`pool_completers`, internal to this study's own pool. The consequence was not a missing nicety:
**every structural finding was confounded and the confound could not be checked.** "Long gaps abandon
more" could not be separated from "long gaps happen to troubled shows that were poorly received" — an
objection a product owner raises in the first ten minutes, and the study had no response.

Population over the frame: `rating` **1,138/1,138**, `votes` **1,138**, `airs_day` **1,123**,
`subgenres` **1,088**.

**The honest objection, recorded with the field.** `rating` is measured in 2026, *after* S2, so a
show whose S2 disappointed may carry a depressed rating partly **because of the outcome being
studied**. It is a contaminated predictor. Two responses: `votes` is far less outcome-contaminated
and is an **external** popularity measure independent of the pull; and the alternative to a
contaminated stratifier is **no stratifier at all**. A disclosed confound is worth more than an
absent variable. **Any result cut on `rating` must state this.**

## 4. `size_quintile` is separated from exposure

`pool_completers` counts users who completed S1 **ever**, so a 2012 title has had fourteen years to
accumulate them and a 2025 title four. Cut raw, the quintile was a **size-and-age composite**, not a
size field.

Three candidates were computed and measured against the frame's own **14.8%** share of 2023–2025
titles:

| Definition | 2023–2025 share of Q5 | Verdict |
| :--- | ---: | :--- |
| Raw count | **12.3%** | under-corrects |
| Completers per year | **32.9%** | **over-corrects, and by more** |
| **Within air-period cohort** | **14.9%** | **neutral by construction** |

**Per-year was the obvious fix and it is the wrong one.** Completions are front-loaded after release,
so dividing by total elapsed years penalises an old title whose accumulation tapered a decade ago.
Median `completers_per_year` runs **8.5** (pre-2020), **16.3** (2020–2022), **28.7** (2023–2025) — a
monotone gradient that is pure age, not size.

**`size_quintile` is now the within-cohort rank.** `size_quintile_raw_count` and
`size_quintile_per_year` are retained under explicit names so the three can never be confused, and
`completers_per_year` and `s1_exposure_years` are carried as fields.

## Scope

- **No inclusion rule changed.** 1,138 shows, 220,107 pairs, all seven ledger rules untouched.
- **Zero API calls.** Everything came from cached bodies and the existing frame.
- **The window for this closes when Step 8 locks.** After that, adding a show field means re-running
  a dual-implementation gate.
- **[0016](0016-per-season-network-dropped.md) is superseded in part**: its per-season finding stands,
  its retention of show-level network does not.
- The ≥50 completer floor is addressed separately in [0031](0031-the-50-completer-floor.md).
