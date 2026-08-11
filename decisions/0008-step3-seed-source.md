# Decision 0008 — Step 3 seeded from movie-comment authors

| | |
| :--- | :--- |
| **Decision** | Channel A was seeded from the first 300 distinct public authors of comments on **movies**, drawn from `comments/recent/all/movies` and `comments/trending/all/movies`. |
| **Taken by** | Analytics Engineer, inside a Chained step |
| **Authority** | **Not a Human Lead decision.** `task-sheet.md` Step 3 says "seed a few hundred public profiles" and prohibits harvesting from comments on the shows being measured; it does not say where seeds come from. |
| **Pre-registered** | **Yes**, with its rationale and a remedy, in the module docstring of `src/step3_user_discovery.py`, written before the run |
| **Date taken / recorded** | Taken 2026-08-11 before the run; recorded 2026-08-11 after it |
| **Status** | **Open — for ratification at the Step 3 checkpoint** |

**This is the highest-consequence agent choice in Step 3.** It determines the composition of the
pool every downstream share is computed over, and it drives the whole of
`artifacts/step3-user-discovery.md` §4. It is recorded separately from
[0006](0006-step3-crawl-constants.md) because it is a design choice rather than a constant, and
folding it into a list of numbers would bury it.

---

## What was done

| | |
| :--- | :--- |
| Seeds | 300 |
| `comments/recent/all/movies` | 218 |
| `comments/trending/all/movies` | 82 |
| `comments/updates/all/movies` | **0** — configured, never reached, 300 filled first |
| Distinct films | 172 |
| Max seeds from one film | 24 |
| Cost | 10 live calls |

## The rationale, pre-registered

From the docstring, before the run:

> "Seeds: ~300 public profiles taken from authors of recent/trending/updated comments on MOVIES.
> Movies cannot be in the Step 2 frame (the frame is TV shows with two or more seasons), so this
> harvests nothing from comments on any show being measured and cannot select on the outcome. **It is
> adjacent to a prohibition**, so `seed_source` and `depth` are recorded per user and depth-0 users
> can be excluded wholesale at Step 11 if the Human Lead wants that."

**The narrow argument is correct.** The task sheet's prohibition — *"Do not harvest usernames from
comments on the shows being measured. That selects on the outcome."* — is satisfied. No user entered
the pool because of anything they did on a measured show. The agent also recognised the choice sat
next to a prohibition and instrumented for it in advance, which is why the remedy below is available
at all.

## Why it still biases the pool

**"Cannot select on the outcome" is not "does not bias the pool," and the pre-registration treats
them as equivalent.** Selecting on a covariate correlated with the outcome biases an estimate as
effectively as selecting on the outcome itself.

Movie-commenting is a strong marker of **tracking intensity**. Commenters are a small hyperactive
minority. Heavy trackers are likelier to continue into S2, likelier to log completely, and likelier
to survive the Step 7 liveness filter.

> **Direction: downward on the never-started share — the study's headline.**
> The **same direction** as the liveness-exclusion bias Step 14 must disclose. The two **compound.**

Three things make this sharper than a generic self-selection caveat:

1. **Timing collides with Step 5.** Seeds were drawn on 2026-08-11 from recency-ordered feeds, **27
   days after the TV Time shutdown of 15 Jul 2026**. A recent-comment feed on that date oversamples
   the migration cohort — precisely the population Step 5's contamination rule exists to detect and
   exclude. If Step 5 removes a large slice, it removes it **after** the discovery budget is spent.
2. **The pre-registered remedy is cosmetic.** Excluding depth-0 users drops 300 of 5,694. Depth-1
   users are *followers of commenters*, and follower graphs are homophilous, so the selection
   propagates rather than staying with the seeds. Usable users by depth: 290 at depth 0, 1,393 at
   depth 1, 623 at depth 2, 1,782 with no depth (Channel B).
3. **Step 11 as specified cannot detect it.** Channel A selects on public social activity, Channel B
   on public list authorship — **both select on public-facing activity.** A ≈ B is the likely result
   and would read as "no discovery bias," when it means two draws from the same biased frame agree.
   **Agreement between the arms is not evidence of unbiasedness**, and Step 11's brief does not say
   so.

## The alternative, and what it would have cost

No alternative was recorded. The realistic ones and their costs:

| Alternative | Cost |
| :--- | :--- |
| Seed from public-list owners only (Channel B's source) | Cheaper per user, but collapses the two arms into one source and destroys Step 11's comparison entirely |
| Seed from comments on **TV shows outside the Step 2 frame** | Closer to the target population, but "outside the frame" is only knowable once Step 2 exists — and Step 3 runs in parallel with Step 2 by design |
| Random or ID-space sampling | Trakt exposes no such endpoint under Client-ID-only auth |

**The choice was constrained more than the write-up implies.** Step 3 runs in parallel with Step 2,
so no frame-aware seeding was available. That is a real defence of the decision and an argument that
the *sequencing* is what should be revisited, not the seeding.

## What is measurable, and is not yet specified

Screening already recorded `followers`, `following`, `episodes_watched`, `joined_at`, `total_plays`
and progress fields per user. **The activity distribution of the pool is therefore measurable from
`raw/step3/` at zero further live calls.** A depth- or activity-stratified diagnostic would put a
number on this bias instead of leaving it a caveat.

**One constraint on how.** Screening ran FIFO at 120 per round and left 1,027 eligible users
unscreened, skewed toward depth 2 (depth 1 screened at ~80 percent of its cohort, depth 2 at ~36
percent). **Any such diagnostic must condition on *screened*, not *eligible*,** or it reports a
screening-order effect as a depth effect. See [0006](0006-step3-crawl-constants.md).

## For the Human Lead

Ratify, or direct otherwise. Two live questions, both in
`artifacts/step3-user-discovery.md` §9 position 2:

1. **Does Step 11's brief gain an activity-stratified diagnostic?** As written, Step 11 can *fail*
   the study on divergence but cannot *clear* it on agreement — which is the direction §4 says is
   uninformative.
2. **Or does Step 14 state the limitation instead?** Step 14's checklist currently carries one
   downward bias (inactive-user exclusion). This is a second, running the same way.
