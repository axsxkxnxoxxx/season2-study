# Decision 0024 — `W` is the 90th percentile of the C1 lag distribution, not a curve-flattening judgment

| | |
| :--- | :--- |
| **Decision** | **`W` is the 90th percentile of the observed lag distribution on the C1 estimation sample.** The prior wording — *"set W at the percentile where the curve flattens"* — is **withdrawn**. Step 13's `W` arms must span **46 to 107 days**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Amends** | `task-sheet.md` Step 6 and Step 13 |
| **Occasioned by** | Step 6 run 1, in which two isolated instances produced `W = 46` and `W = 107` from the same spec and the same data |
| **Status** | Closed |

---

## What the dual run found

Step 6 ran as a dual pair against the unamended spec. **The two instances agreed on every input and diverged 2.3× on the output.**

| | Instance A | Instance B |
| :--- | ---: | ---: |
| `W` estimation sample | 128,099 | 128,099 |
| C1 pairs | **25,120** | **25,120** |
| C1 negative lags | **689 (2.74%)** | **689 (2.74%)** |
| C2 negative lags | **11,369** | **11,369** |
| "Flat" read as | first week buying < 1.0 pp coverage | marginal day buying < 0.05% of sample |
| Percentile selected | 85th | 90th |
| **`W`** | **46 days** | **107 days** |
| Step 13 range reported | [11, 46] | [37, 107] |

Every population figure and intermediate diagnostic matches **to the pair**. The divergence isolates to a single undefined word.

**This is not a parameterisation difference.** Instance A's own sensitivity sweep runs 29 to 89 days across a fourfold change in its threshold and never reaches 107. The two criteria differ in kind — one measures coverage bought per *week*, the other per *day* — and both are faithful readings of "flattens".

**Neither instance was wrong.** This is the outcome the dual-implementation regime exists to produce: *"Any divergence is either a bug or an ambiguity in the spec. Report it. Do not reconcile it."* It was reported and not reconciled.

## Why "flattens" could not have worked

Both instances found the same thing about the data, independently: **past roughly day 7 the C1 lag density is close to scale-free**, with a log-log slope between −1.1 and −1.5 across every decade from one week to four years. There is no break in the density to read. The only genuine elbow is at day 7, and `W = 7` is plainly not the window this study wants.

So "the percentile where the curve flattens" asked for a feature the distribution does not have. Any instance obeying it had to invent a criterion, and the criterion — not the data — then set the number. Instance A said so in its own write-up: *"anyone defending 46 out loud has to be willing to say that 39 and 65 were also available."*

## The rule adopted, and its warrant

> **`W` = the 90th percentile of the observed lag distribution on the C1 estimation sample.**

Rationale as given:

> Attribution-window practice sets the window at or slightly above the 90th percentile of the
> time-to-conversion distribution, with 75th to 90th the cited range. A percentile is unambiguous;
> "flattens" produced two honest readings 61 days apart.

Two properties matter more than the specific value:

1. **It is unambiguous.** Two isolated instances computing the 90th percentile of the same sample cannot disagree except by a bug — which is exactly what the dual run is supposed to detect. The previous wording made the diff uninformative, because a divergence could not be told from a difference in judgment.
2. **It is a convention, and it is labelled as one.** The 90th percentile is not a property of this data; it is imported practice. Nothing in the lag distribution selects it, and the decision does not pretend otherwise.

**The signed, untruncated rule is unchanged and still binds.** The percentile is taken on the distribution as it stands — no truncation, no clipping, no absolute values, no dropped rows. The negative-mass handling already in Step 6 continues to apply.

## Step 13's arms

> **The W arms must span 46 to 107 days**, and this composes with the existing C1-versus-all-shows range: **cover the union, not whichever is wider.**

The reasoning is worth stating because it is easy to mistake for redundancy now that the definition is fixed. **Making a definition unambiguous does not make the result insensitive to it.** 46 and 107 are the measured spread of two honest readings of the same instruction, and that spread is a real quantity about how much the headline depends on a convention. Fixing the wording removes the *disagreement*; it does not remove the *dependence*. Step 13 is where dependence gets tested.

## What is not decided here

- **`W` itself is not set.** Step 6 is still an unapproved gate. This entry fixes the *rule* for deriving `W`; the number it produces is the deliverable of the re-run and must be approved on its own.
- **D14's warrant remains wrong.** Both instances found that `decisions/0003` D14 and Step 1 §9 state every C1 lag is non-negative by construction while **689 are negative** — 459 binding on the S1-completion term, which `max()` can select on a C1 show, and 230 on the finale, of which 135 are the known one-day UTC skew and **95 are unexplained, out to −495 days**. Worth ≤6 days of `W` either way, so it is not load-bearing for the number, but the warrant is false and the 95 have no account. **Not addressed by this entry.**
- **The censoring direction stands unresolved.** Instance B reports that restricting C1 to pairs with ≥8 years of exposure moves the 90th percentile from 107 to 213, and that it could not separate censoring from cohort effects. A higher `W` moves the never-started share **down**.

## Process: distinct output namespaces

Run 1's two instances were given **byte-identical prompts** — correct, because describing the task twice in different words would have made any divergence uninterpretable — but they were left with **identical default output paths and collided**. Instance B's script was overwritten mid-run and it renamed its outputs to an `-instance-a` suffix, which is why that suffix does not match the agent that produced it.

**Each instance now receives a distinct output namespace.** Per the Human Lead: *"That is not part of the task description and does not weaken the diff."* The spec stays byte-identical; only the destination differs.

No output was lost in run 1, and the identical inputs are themselves evidence the collision never reached the computation. Run 1 is preserved in git at commit `9c5fbd3` as the evidence for this entry, and its artifacts are removed from the working tree to avoid being mistaken for deliverables.
