# Decision 0016 — Per-season network is dropped as a field; platform fragmentation is not a variable in this study

| | |
| :--- | :--- |
| **Decision** | The **per-season `network` field is dropped** from the Step 2 frame. It is 0.71% populated and cannot support a measurement. **Platform fragmentation is therefore not a variable in this study**, and the limitation is stated wherever a structural threshold is justified without it. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Closes** | The **first** of the two open problems in [0014](0014-no-content-filters-structural-fields.md) §"platform fragmentation is unverified" — whether the API exposes a per-season network. It does, and it is empty. |
| **Does not close** | The **second** problem, which survives and now attaches to the show-level `network`. See below. |
| **Status** | Closed |

---

## The measurement

[0014](0014-no-content-filters-structural-fields.md) named a resolution rule in advance: *"if it
cannot be measured, it is dropped as a field and the limitation is stated."* This applies it, on
evidence rather than on expectation.

Across all 2,094 candidate shows fetched with `GET /shows/:id/seasons?extended=episodes,full`:

| | |
| :--- | ---: |
| Season objects seen, season 0 excluded | 6,645 |
| Of those, `network` non-null | **47 (0.71%)** |
| Shows with **zero** distinct season-level networks | 2,080 |
| Shows with exactly one | 13 |
| Shows with **two or more** | **1** |

**The field exists and is empty.** At 0.71% populated it supports no distribution, no
stratification and no comparison.

**Exactly one show in 2,094 carries two distinct season-level network values.** That is a count
consistent with noise, and it is **not** read as evidence of fragmentation. Reading a single row as
a finding is precisely the inference [0014](0014-no-content-filters-structural-fields.md) forbade
when it said *"do not infer fragmentation."*

## What is dropped and what is kept

**Dropped:** the columns `s1_network` and `s2_network` are removed from `processed/step2/frame.csv`.

**Kept:** the population counts above are retained in `processed/step2/frame-summary.json` under
`field_inventory`, so the decision stays auditable without a refetch. The raw bodies are cached
under `raw/shows/`, so nothing is unrecoverable.

## The limitation, stated as 0014 requires

**Platform fragmentation is not a variable in this study.** The concept "this show's seasons were
split across services" has no representation in the data available. No result may claim to control
for it, stratify on it, or rule it out as an explanation. Where a structural threshold is justified
in later steps, this absence is named rather than passed over.

## The second problem survives, and it has moved

[0014](0014-no-content-filters-structural-fields.md) identified a second problem it called "the
harder one, because it survives the first": a present-day field describes availability **now**, not
availability at release, and the thing that would have affected viewing is the latter.

That problem is **not** closed here, and it has attached itself to a new field. The show-level
`network` from `GET /shows/:id?extended=full` was pulled on 2026-08-12 and is **100% populated
across the frame, 150 distinct values**. It is tempting to use, and it carries exactly the defect
0014 warned about: it records **today's** network, so a title that moved services between seasons
shows only its current one, and a title whose seasons originally split shows no trace of the split.

> **`show_network` must not be used as a release-time availability measure.** It is a present-day
> catalogue value. It is retained as a descriptive field only.

## What this does not change

- **No show was included or excluded on network.** This is a field decision, not a filter decision.
  The frame's 1,226 shows are unaffected in composition.
- **`decisions/0014` stays Open.** Its other open item — the deferred gap-length and season-size
  thresholds — is untouched by this entry.
