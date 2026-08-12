# Decision 0017 — Air period is the calendar year of the S2 finale, in three buckets

| | |
| :--- | :--- |
| **Decision** | **Air period := the calendar year of the S2 finale**, bucketed **pre-2020 / 2020–2022 / 2023–2025**. Chosen to bracket the 2020 production shutdown and to claim no finer distinction than that. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Resolves** | "Air period" appeared in the Step 2 field list as an undefined term. The executing agent did not compute it and reported the ambiguity rather than picking a reading, under [0013](0013-step2-execution-delegation.md) condition 3. |
| **Status** | Closed |

---

## Why it needed a decision

"Air period" could have meant the S1 span, the S1-premiere-to-S2-finale span, or the show's whole
run. Those are three different variables and they would have produced three different cuts of the
results. The frame carries all the components — S1 premiere, S1 finale, S2 premiere, S2 finale,
per-season runtime, full season list — so the ambiguity was in the concept, not in the data.

## The definition

`air_period := bucket(year(S2 finale first_aired))` with buckets:

| Bucket | Years | In-frame shows | Share |
| :--- | :--- | ---: | ---: |
| pre-2020 | ≤ 2019 | **817** | 66.6% |
| 2020–2022 | 2020–2022 | **223** | 18.2% |
| 2023–2025 | 2023–2025 | **186** | 15.2% |

No post-2025 bucket exists by construction: the frame's own inclusion rule caps the S2 finale at
2025-12-31, and [0015](0015-step2-unaired-s2-exclusion.md) removes seasons that have not aired.

**The stated reason for the boundaries is the 2020 production shutdown**, and the decision
deliberately claims nothing finer. A year-by-year or quarter-level period would imply a resolution
the study has no basis for.

## A confound that has to travel with this field

**Air period and cadence are strongly confounded on this frame**, and the two must not be treated as
independent cuts:

| Air period | C1 all-at-once | C2 weekly | C3 faster | C4 slower |
| :--- | ---: | ---: | ---: | ---: |
| pre-2020 | 84 | 254 | 73 | 406 |
| 2020–2022 | 80 | 58 | 43 | 42 |
| 2023–2025 | 50 | 46 | 62 | 28 |

Weekly (C2) and slower-than-weekly (C4) dominate the pre-2020 era and collapse after it;
all-at-once (C1) and faster-than-weekly (C3) become far more prevalent. This is the expected shape
of the streaming transition, and it means **a difference across air periods is not separable from a
difference across release cadences** without an explicit design that holds one fixed.

Cadence is already a **required Step 9 stratum** and a **mandatory Step 12 candidate** under D12. If
air period joins them as a cut, the collinearity above is the first thing any such cut has to
address, and it is recorded here so no later step rediscovers it as a surprise.

## Scope

This is a **field definition**, not a filter. No show is included or excluded on air period, and
none is proposed to be. Whether air period ever becomes an exclusion is a separate decision that
would fall under [0014](0014-no-content-filters-structural-fields.md)'s deferred-threshold process.
