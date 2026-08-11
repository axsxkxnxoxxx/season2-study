# Decision 0007 — Channel A took 89 percent of discovery calls at 5× the cost per user

| | |
| :--- | :--- |
| **Decision** | The per-round discovery budget was split 24 calls to Channel A (follower graph) against 3 to Channel B (public-list owners), fixed for every round regardless of observed yield. |
| **Taken by** | Analytics Engineer, inside a Chained step |
| **Authority** | **Not a Human Lead decision.** The task sheet requires both channels; it says nothing about their relative spend. |
| **Date taken** | 2026-08-11, before the run |
| **Date recorded** | 2026-08-11, after the run, on Human Lead instruction |
| **Status** | **Open — recorded for ratification.** The rationale is defensible but was never stated at the time. |

---

## The split, and what each channel returned

`EXPAND_USERS_PER_ROUND = 12` at 2 calls each = **24 Channel A calls per round**.
`LIST_PAGES_PER_ROUND = 3` = **3 Channel B calls per round**. Fixed, never adapted.

| | Channel A | Channel B |
| :--- | ---: | ---: |
| Discovery calls | 864 (**89%**) | 108 (**11%**) |
| New eligible users | 3,102 (61%) | 1,945 (39%) |
| **Users per call** | **3.6** | **18.0** |
| Usable users, by first channel | 2,306 | 1,782 |

**Channel A cost 5× per user and returned under two-thirds of the eligible pool.** On cost alone
the split is the opposite of what one would choose. 324 users were reached by both channels.

## The defence, stated now because it was not stated then

**Step 11 needs two channels that select differently.** The whole purpose of the tagging requirement
is a discovery-bias check, and a check comparing two arms is worthless if one arm is a rounding
error. Buying Channel A's users at 5× is therefore purchasing *arm independence*, not users — which
makes cost-per-user the wrong yardstick.

**That is a coherent rationale and it is probably the right one. It was never written down.** No
comparison was made, no alternative split was costed, and the trade appears nowhere in the code
comments or the plan docstring. It is being reconstructed after the fact, which is why it is
recorded as needing ratification rather than as settled.

## What the split cannot be defended against

**Its rigidity.** The allocation never responded to what the channels were doing, and by the end
they were doing opposite things:

- **Channel B exhausted itself.** List dedup climbed from 0.20 at round 1 to 0.74–0.89 from round 25
  on; new eligible users fell from 125 per round to 6–24. It was still being given 3 calls a round
  at the end, buying almost nothing.
- **Channel A never converged.** Yield swung between 0.04 and 15.08 per call with no trend,
  depending on whether a round happened to expand a high-degree account.

A split that adapted would have moved calls away from B once dedup crossed some threshold. Whether
that is worth building is a question for any future discovery run, not for this pool.

## Consequences, not decisions

Recorded so they are not mistaken for choices anyone made: **Channel B's exhaustion**, **Channel A's
hub-luck variance**, and **the frontier growing monotonically to 2,970 without ever draining** are
all outcomes observed after the fact. Only the 24:3 allocation was decided.

## A caveat on the graph statistics this decision produced

`raw/step3/edges.jsonl` holds 7,426 records, each carrying both a crawl-traversal direction
`(src, dst)` and a social direction `(follower, followee)`. **Step 11 wants the social graph:
7,103 distinct directed pairs.** The traversal reading (6,166) counts a mutual follow as reciprocal
only when the crawl happened to expand both endpoints, so its reciprocity is an artifact of walk
order.

**One figure is unresolved:** `artifacts/step3-yield-curve.json` reports `reciprocal_pairs: 1353`
where recomputation from `edges.jsonl` gives **1,172**; `distinct_directed_pairs: 7103` agrees
exactly. **Step 11 should recompute reciprocity from `edges.jsonl` rather than read it from the
yield curve**, until the discrepancy is resolved.

## For the Human Lead

Ratify the arm-independence rationale, or record a different one. See
`artifacts/step3-user-discovery.md` §5 and §9 position 2 — the same evidence bears on whether
Step 11's brief needs an activity-stratified diagnostic, since a two-arm comparison where both arms
select on public-facing activity can fail the study but cannot clear it.
