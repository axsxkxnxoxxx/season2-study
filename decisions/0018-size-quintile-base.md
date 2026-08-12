# Decision 0018 — The title size quintile is cut over the frame, not over the candidate set

| | |
| :--- | :--- |
| **Decision** | The **title size quintile is cut over the 1,226-show frame**, not over the 2,094 candidates. Rationale as given: the quintile exists to cut results, and results exist only for in-frame shows. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Resolves** | The Step 2 field list asked for "a title size quintile by completer count" without naming the population the quintiles are cut over. Reported as ambiguous by the executing agent under [0013](0013-step2-execution-delegation.md) condition 3; both cuts were recorded as separate columns pending this decision. |
| **Status** | Closed |

---

## Why the base mattered

The two readings are not cosmetic. Cutting over the 2,094 candidates and then keeping only the
in-frame shows produces a **right-skewed** set of bins, because the 796 shows with no season 2 are
disproportionately small and dropping them pushes the survivors upward:

| Quintile | Cut over the **frame** (adopted) | Cut over the **candidates** (rejected) |
| :--- | ---: | ---: |
| Q1 | 247 | 200 |
| Q2 | 244 | 229 |
| Q3 | 249 | 226 |
| Q4 | 241 | 262 |
| Q5 | 245 | 309 |

The rejected base gives bins that are not quintiles of anything the study reports on: Q5 would carry
25.2% of in-frame shows and Q1 16.3%. Any "by size quintile" table built on it would have unequal
bins while being labelled as quintiles, which is the kind of thing that survives into a chart and
misleads silently.

The adopted base gives 247 / 244 / 249 / 241 / 245 — even by construction, and every bin is a bin of
shows that actually produce results.

## Implementation

Single column, `size_quintile`, on `processed/step2/frame.csv`, computed on the **recomputed**
`pool_completers` from [0019](0019-pool-completers-recomputed.md) rather than on the superseded
proxy. The `size_quintile_candidates` column from the first build is removed.

## A dependency worth naming

The quintile is a function of the frame, and **the frame is a function of a stopped pull**. If the
Step 4 pull resumes, more shows cross the ≥50-completer bar, the frame grows, and **every quintile
boundary moves** — the same mechanic that [0013](0013-step2-execution-delegation.md) condition 2
required the candidate set be recomputed for.

Consequence: **a quintile label is not a stable identifier for a show.** It is valid against the
frame it was cut on and must be recomputed, not carried forward, if the frame is rebuilt. Any result
reported by quintile should name the frame it was cut against.
