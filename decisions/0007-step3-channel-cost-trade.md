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

The factor of 2 is real: expansion reads both `users/:id/followers` and `users/:id/following` per
user. 27 discovery calls × 36 rounds = **972**, matching `logs/step3_run.json` → `calls.discovery`
exactly.

## Why, in the agent's own pre-run words

*(An earlier version of this entry said the rationale "was never written down" and reconstructed it.
That was wrong: it is pre-registered in the module docstring of `src/step3_user_discovery.py`,
written before the run. Corrected 2026-08-11 — it was documented in the wrong place, not absent.)*

On reading both endpoints: *"Outbound follows reach different communities than inbound ones, so using
both widens the walk."*

On Channel B's ceiling: *"`lists/trending` and `lists/popular`, paged at limit=100. **Both report the
same 20,211-list universe**, so they are two orderings of one pool and are deduped by list id."*

**Channel B was known in advance to be drawing from a single bounded pool.** That is the strongest
available justification for capping it at 3 calls a round — and it is not stated as such anywhere.
No rationale is recorded for 12 and 3 specifically.

**Step 11 needs two channels that select differently.** A discovery-bias check comparing two arms is
worthless if one arm is a rounding error, so buying Channel A's users at a higher unit price is
purchasing *arm independence* rather than users. That is a coherent defence and probably the right
one, but it is inferred from the design rather than stated in it.

## The cost argument against the split does not survive the margin

`artifacts/step3-user-discovery.md` §5 argues the allocation is "on cost alone … the opposite of what
one would choose," on whole-run averages of 3.6 users per call for A against 18.0 for B.

**Those averages invert at the margin.** Recomputed from the per-round record over rounds 25–36 — the
period the write-up itself identifies as Channel B's exhaustion:

| Rounds 25–36 | New eligible | Discovery calls | Per call |
| :--- | ---: | ---: | ---: |
| Channel A | 1,528 | 288 | **5.31** |
| Channel B | 146 | 36 | **4.06** |

**Over the last third of the run, Channel A was the cheaper channel.** Reallocating toward B would
have bought less than its headline 18.0 rate implies, because that rate was collapsing against a
20,211-list universe known to be bounded from the outset.

**The honest qualification:** Channel A's marginal advantage is high-variance. Three rounds — 26, 29
and 27 — supply **853 of those 1,528 users, 56 percent from a quarter of the rounds**. A's *expected*
marginal rate beat B's; its *reliability* did not. This finding and §3's "hub-luck, not convergence"
are the same fact from two sides.

## What the split still cannot be defended against

**Its rigidity.** The allocation never responded to what the channels were doing. Channel B was still
drawing 3 calls a round at dedup 0.89, buying almost nothing. A split that adapted would have moved
calls away from B once dedup crossed a threshold. Whether that is worth building is a question for a
future discovery run, not for this pool.

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

**One figure was a bug and is now resolved. The correct value is 1,172 reciprocal pairs; the
`reciprocal_pairs: 1353` in `artifacts/step3-yield-curve.json` is wrong.**

`src/step3_backfill.py` adds each pair to the seen-set *before* checking whether its reverse is
present, and increments **per record** rather than per distinct pair. `edges.jsonl` holds
`7,426 − 7,103 = 323` duplicate records, so every duplicate of an edge whose reverse was already
seen increments again. Reproduced by executing both algorithms against `edges.jsonl`: the
add-then-check per-record form returns **exactly 1,353**; correct distinct-pair counting returns
**1,172**. `distinct_directed_pairs: 7103` is unaffected and correct.

The same pattern inflates the traversal-reading figure of 235 by the same mechanism. Until the
yield-curve JSON is regenerated, **Step 11 should recompute reciprocity from `edges.jsonl`.**

## For the Human Lead

Ratify the arm-independence rationale, or record a different one. See
`artifacts/step3-user-discovery.md` §5 and §9 position 2 — the same evidence bears on whether
Step 11's brief needs an activity-stratified diagnostic, since a two-arm comparison where both arms
select on public-facing activity can fail the study but cannot clear it.
