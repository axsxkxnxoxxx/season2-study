# Decision 0077 — the channel overlap gets its populations, position 3's drop set is restated, and column names are fixed

| | |
| :--- | :--- |
| **Decision** | **The discovery-channel overlap is 324 of the 5,694 Step 3 pool and 178 of the 2,549 accounts pulled** — `0070` ruling 3 gave "324 users" with no population. **`0075` ruling 2 is restated: position 3's drop set is the 58,345 pairs that fail the S1 completion rule**, because as written it named an empty set. **Column names are fixed at 89 columns**, before Step 8b's schema inherits an 88-against-87 divergence. **Both arms rerun.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 rerun. Instance A found the first two; the third is the arms' own naming divergence |
| **Status** | Closed. **Both arms rerun. Step 8 is not adopted.** |

---

## 1. The overlap — a count without its population, in the ruling written to fix one

`0070` ruling 3 said **"324 users are in both channels"** and named no population. **It is 324 of the
5,694-username Step 3 discovery pool, and 178 of the 2,549 accounts actually pulled.**

**Both figures and both populations are now stated at the point of use.**

**This is the shape that has recurred through the entire chain** — `0047`'s standing rule exists for it,
`0068` §2a listed seven instances of it, and it recurred **inside the ruling I wrote to fix a different
unlabelled figure.** Instance A caught it and stated both figures in its artifact **so the diff would
not read them as a divergence**, which is the right instinct and is why it surfaced at all.

## 2. Position 3's drop set — the ruling named an empty set

`0075` ruling 2 required *"position 3's drop set"* to be retained, because D9 half (b) is measured on
the rows position 3 removes.

**Position 3 removes ZERO rows from the waterfall.** Line 1 is already the S1-completer population
(`0068`), so the S1 completion rule deletes nothing at that position. **The ruling named an empty set,
and both arms had to choose an interpretation in order to compute anything at all.**

**They chose the same one — and a ruling exists precisely so they do not have to choose.**

**Restated: the 58,345 pairs that FAIL the S1 completion rule** — the pair universe less the completers
— carrying each pair's distinct-episode counts and the show's threshold, which is what half (b) reads.

**One correction to the ruling as dictated, and it matters because it would have put the wrong rule in
the spec.** The instruction called these *"the 58,345 records the set-membership rule deletes."* **The
set-membership drop rule is a different rule and deletes 0 records** — both arms measured that, on
6,065,704 and 6,065,610 records examined respectively. **58,345 is position 3's own rule, the S1
completion rule, and the unit is PAIRS, not records.** Written that way.

## 3. Column names — fixed before Step 8b inherits them

The rerun produced **88 columns against 87 for the same contents.** Every difference was naming:
`in_population_APPLY` / `in_apply`, `n_rec_s1_watch` / `action_count_s1_watch`, `tau1_utc` / `tau1`,
`max_episode_in_AH` / `max_episode_in_A_H`, `T0_binding_term` / `t0_binding_term`.

**Step 8b defines the schema Steps 9–13 write into. Left alone, it inherits the divergence** — and
`0066` ruled that Steps 9–13 write into that schema **directly, with no conversion layer**, precisely
because a conversion layer is a second definition of every figure.

**THE RULE: use the spec's own vocabulary at the point the spec defines the thing; where the spec does
not name it, prefer the more explicit form.** It decides every case without preference:

| Adopted | Because |
| :--- | :--- |
| `in_apply` / `in_deriv` | the spec names the populations APPLY and DERIV; shortest unambiguous form |
| `tau1` / `tau2` | the spec writes `τ1` and `τ2` with no suffix. **No `_utc`: every instant in this study is UTC by Step 1 §2.4, and suffixing some columns implies the others are not** |
| `n_A`, `n_A_H`, `max_episode_in_A_H`, `f2_in_A_H` | the spec writes `A`, `A_H`, `\|A\|`, `F2 ∈ A_H`. **`AH` is not the spec's spelling** |
| `action_count_s{1,2}_{watch,scrobble,checkin,other}` | `0070` ruling 4's own words: *"per-pair counts by action type"* |
| `discovered_channel_a` / `discovered_channel_b` | `0070` ruling 3 says two booleans; **`in_channel_*` collides with the population flags** |
| `t0_binding_term`, `t0_date`, `s1_completion_date` | lower-case, no `_utc`, consistent with the above |

**Both instances' extra columns are kept, not arbitrated away:** **`has_s3_or_later_evidence`**, which
D4 reads, and **`s1_completion_used_a_post_cutoff_record`**, which the still-open D11-at-position-3
question reads. **89 columns.**

## 4. Surfaces

**REACHED:** `task-sheet.md` Step 8 and both `analytics-engineer` files, identically; pair verified
byte-identical apart from `name:`. All eight surfaces PASS.

**DELIBERATELY NOT REACHED:** the `data-scientist` pair — **none of the three changes what Step 9
receives**, and `0071` already instructs Step 9 to consume Step 8's output rather than rebuild it.
**Step 8b is not yet written**, so the column names reach it when it is; that is the point of fixing
them now rather than after.

## 5. Scope

- **No published figure moves.** The overlap figures were always both true; only their labels were
  missing. The drop set and the column names are inputs and names.
- **Both arms rerun**, because all three are spec changes and neither arm has executed against them.
- **Zero API calls in this entry. Step 8 is not adopted.**
