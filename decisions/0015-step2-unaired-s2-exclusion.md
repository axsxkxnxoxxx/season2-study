# Decision 0015 — A season 2 that is listed but has not aired is not a season 2 for the frame

| | |
| :--- | :--- |
| **Decision** | The **12 candidate shows whose season 2 is listed with episodes but carries no finale air date are excluded** from the Step 2 frame. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Resolves** | The one case the Step 2 selection rules did not decide, held by the executing agent under [0013](0013-step2-execution-delegation.md) condition 3 rather than resolved. |
| **Status** | Closed |

---

## What the rule said, and why it did not decide

The written inclusion rule is *"include a show if it has a real season 2 whose finale aired on or
before 31 Dec 2025."* It states a condition on an air date.

These 12 shows have a season 2 that is **real in the metadata** — it is listed, it has episodes,
those episodes have numbers — but the finale episode `max(E2)` carries **no `first_aired` at all**.
The rule tests a date that does not exist. It does not return false; it fails to apply.

Under [0013](0013-step2-execution-delegation.md) condition 3 an underspecified rule is **reported,
not resolved**, so the agent held these 12 out of the frame *and* out of the post-cutoff exclusion
bucket, and reported them. This entry decides them.

## Why they are excluded

**All 12 report `aired_episodes = 0` for season 2.** That is the API's own positive statement that
nothing in the season has aired — not a missing value, but a count of zero. A season with zero aired
episodes cannot have a finale that aired on or before the cutoff, so under any reading of the rule
these shows fail it.

They are upcoming seasons, and several are high-profile:

| Title | Pool completers | S2 episodes listed |
| :--- | ---: | ---: |
| A Knight of the Seven Kingdoms | 550 | 1 |
| Dexter: Resurrection | 303 | 10 |
| Dune: Prophecy | 288 | 8 |
| Cyberpunk: Edgerunners | 262 | 1 |
| All of Us Are Dead | 243 | 1 |
| Creature Commandos | 171 | 1 |
| Young Sherlock | 125 | 3 |
| The Institute | 111 | 8 |
| Supacell | 109 | 1 |
| Moving | 71 | 1 |
| The Madison | 65 | 6 |
| The Celebrity Traitors | 53 | 1 |

## Why this is not merely folded into the "S2 finale after 2025-12-31" rule

It would have been convenient to score them as late finales and move on. That would have been
wrong in a way that matters for auditability: a show whose S2 finale aired in March 2026 and a show
whose S2 has not aired at all are **different data conditions**, and only one of them is a date
comparison. Collapsing them would have made the ledger say the cutoff removed 72 shows when it
removed 60.

They are recorded as their own ledger step — **step 4, "S2 listed but unaired," 12 shows** — in
`artifacts/step2-frame-ledger-and-distributions.md` §2, and listed at
`processed/step2/excluded_s2_unaired.csv`.

## Consequence

The frame excludes the newest continuations in the catalogue. That is correct for this study —
"finished S1, never started S2" is unmeasurable for a season nobody could have started — but it
means **the frame is systematically older than the catalogue**, and the effect is visible in the air
period distribution: 66.6% of in-frame shows have an S2 finale before 2020
(`artifacts/step2-frame-ledger-and-distributions.md` §3.4). Any claim about *current* audience
behaviour inherits that skew.

If the Step 4 pull resumes and the frame is rebuilt after some of these seasons air, they become
eligible. Nothing here is permanent; the rule is re-evaluated on whatever the metadata says at
rebuild time.
