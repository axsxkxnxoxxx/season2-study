# Decision 0009 — Step 4 pulls in stratified round-robin order

| | |
| :--- | :--- |
| **Decision** | Sort the pool by corrected `step4_pages_forecast`, cut into **ten equal-count bins**, and pull one user from each bin in turn. Deterministic order within bins. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-11 |
| **Applies to** | Step 4, before launch |
| **Status** | Closed |

**Why this decision exists.** Step 4 costs ~210,500 calls and ~23.4 hours at the 150 GET/minute
throttle, and is not expected to finish the pool in the available window. **An early stop must
therefore leave a representative sample rather than an arbitrary slice** — the pull order is what
decides which.

---

## The original framing, and why it was amended

**The Human Lead's first instruction was median-out:** sort by forecast page count, pull median
users first, work outward. It was amended before anything ran, on evidence. Both the original and
the reason it changed are recorded, because the reasoning is what makes the final choice
defensible.

**Median-out leaves a *centered* slice, not a representative one.** Working outward symmetrically in
rank truncates **both tails at once**, and it does so on the axis that matters most: forecast page
count is a proxy for tracking intensity, which is a proxy for the outcome being measured. A sample
containing no heavy trackers is not representative of a population that contains them.

Simulated against the real distribution at a 10-hour cut-off:

| Order | Users pulled | Mean pages | p95 seen | **Heaviest user seen** |
| :--- | ---: | ---: | ---: | ---: |
| Median-out (original instruction) | 2,349 | 38.3 | 67 | **73** |
| **Stratified round-robin (adopted)** | **2,069** | **43.5** | **126** | **151** |
| Ascending (worst case) | 3,132 | 28.7 | 62 | 68 |
| **The pool itself** | 4,088 | **51.5** | **151** | **1,034** |

**After ten hours, median-out would not have pulled a single user above 73 pages**, in a pool
reaching 1,034.

**What median-out got right, and the amendment keeps:** it is deterministic and reproducible, and it
decisively beats ascending order. Those properties survive; only the tail behaviour changed.

## What was adopted, and what it costs

Ten equal-count bins, one user drawn from each in turn. **Every prefix is proportional across the
whole distribution, including both tails, by construction.**

**Cost: about 12 percent fewer users per hour** — 2,069 against 2,349 at ten hours — because the
order deliberately spends part of the window on heavy users instead of avoiding them. **That is the
purchase, not the overhead.** Those users are the sample's only evidence about the heavy end of the
distribution.

Accepted explicitly by the Human Lead: *"The 12% throughput cost is worth a prefix that stays
proportional across the full distribution."*

## What this decision does not do

It does not make an early stop *complete*. A prefix is proportional on **forecast page count** and
on nothing else. It carries every bias already on the record — the seeding bias
([0008](0008-step3-seed-source.md)), the liveness exclusion, and the fact that the pool is a
convenience sample rather than a saturated one ([0005](0005-step3-stopping-rule.md)). **Proportional
is not the same as unbiased**, and any early-stop result must be reported as a prefix of a biased
pool, not as a sample of Trakt.

**Required output:** the fraction of the pool completed, and the realized page distribution of what
was pulled against the pool's, so the proportionality claim is demonstrated rather than asserted.
