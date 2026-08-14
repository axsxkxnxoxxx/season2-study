# Decision 0080 — the column set is enumerated, and every invariant names the population it runs on

| | |
| :--- | :--- |
| **Decision** | **The column set is 87 ENUMERATED NAMES, not a count** — `0077` §3's count is replaced. **Every invariant names the population it runs on and accounts for every row in it**, with `rows_asserted + rows_not_asserted = rows_in_the_stated_population` required to hold. **Both arms rerun.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's second Step 8 pass — its two blockers |
| **Status** | Closed. **Both arms rerun. Step 8 is not adopted.** |

---

## 1. The columns — enumerated, because converged is not specified

**The arms converged on the same 87 names this run.** `0077` §3 gave a **count** — and the count was
arithmetically unreachable, which both arms independently reported and Red Team confirmed: the
intersection is 87, A-only is `silent_at_tau1` and `max_episode_in_A`, B-only is `f2_in_A_H`, **union
90.** Neither arm was compliant: **B emitted every adopted name and missed the count; A hit the count
and dropped an adopted name.**

**Converged is not specified. Nothing prevents the next run from diverging**, and **Step 8b's schema is
built on this vocabulary**, with Steps 9–13 writing into it directly and no conversion layer (`0066`).
**So it is fixed before the schema exists rather than after.**

**All 87 names are listed in `task-sheet.md` Step 8 and in both `analytics-engineer` files.**

## 2. What the 87 drops, stated because it is a real loss

**Three columns are dropped, one arm each.** Two are cheap: **`f2_in_A_H` is derivable** —
`max_episode_in_A_H == s2_F` — and **`max_episode_in_A`** is not read by anything downstream.

**`silent_at_tau1` is not cheap, and this needs saying rather than burying.**

**It is NOT recoverable from `live` and `outcome` on Continued rows.** `live` is true for every Continued
pair **regardless of silence**, because the rule's second conjunct is `NOT Continued`. **So dropping the
column means the count of Continued-and-silent pairs cannot be recomputed from Step 8's table.**

**That count is 652** — the size of the outcome-conditioning, the figure that **closed Red Team's rule
objection at `0063` §1** and that publishes as a Step 14 limitation.

**It remains recomputable from the Step 7 masks. It is no longer recomputable from Step 8's table.**
**The trade is stated at the point of use, and adding the column back makes the set 88.**

## 3. Invariant coverage — the provenance rule, applied to invariants

`0078` and `0079` established that **a figure needs the build it was measured on.** **This is the same
rule one step sideways: an invariant that passes on one population and was never run on another READS
AS A PASS ON BOTH.**

**The dual run diverged on the coverage of five of the eight**, and **one of those gaps was a real
hole.** One arm asserted `p` on **19,042** rows with a non-S&L clause of **177,513** — summing to
**196,555 against a 196,654-row table.** **99 rows were covered by neither clause, and those 99 are
exactly the started-and-left liveness exclusions**: the numerator was taken post-liveness and the
denominator pre-liveness. **Neither report disclosed the gap, no control could see it, and it survived
two reruns.**

**A passing invariant whose coverage the instance chose is a code check on the instance's choice.**

**Every invariant now reports `rows_asserted + rows_not_asserted = rows_in_the_stated_population`, and
the identity must hold.** The eight populations:

| # | Invariant | Population |
| :-- | :--- | :--- |
| 1 | outcome partition | **196,654 AND 195,951, both stated**, plus DERIV 147,370 / 147,271 — the table carries all position-5 rows, so neither substitutes for the other |
| 2 | monotone filter counts | **both chains**, APPLY's seven positions and DERIV's |
| 3 | `\|D\| ≤ L` | **both seasons, every pair the set-membership rule examines**, pair count and record count stated. **The wider reading is required; the narrower does not substitute** |
| 4 | `A ⊆ A_H` | the 196,654 position-5 row set, every row |
| 5 | clock start | 196,654, every row, **with the S1 completion date recomputed independently** — the only thing giving this one force |
| 6 | `p ∈ (0, 1]` | **all 19,141 Started-and-left rows**, null on **177,513**. **19,141 + 177,513 = 196,654 exactly**, which is the identity that closes the hole |
| 7 | no account dropped wholesale | **both populations**, 2,422 APPLY accounts and DERIV's |
| 8 | no `access_denied` read as empty | **the full account ledger, in ACCOUNTS**, skipped classes counted separately with the pairs they contribute |

## 4. Surfaces

**REACHED:** `task-sheet.md` Step 8 and **both `analytics-engineer` files, identically** — the 87 names
in full and the eight coverage populations in full. **Pair verified byte-identical apart from `name:`.
All eight surfaces PASS.**

**DELIBERATELY NOT REACHED:**

- **Step 8b** — it is not written. **That is the point of fixing the vocabulary now:** `0066` requires
  Steps 9–13 to write into its schema directly, so the names must be settled **before** the schema
  exists, not reconciled after.
- **Both `data-scientist` files** — Steps 9–13 consume the table and do not build it. **The column names
  reach them through Step 8b's schema, which is the single definition `0066` requires.**
- **`CLAUDE.md`** — the invariant-coverage rule is a Step 8 requirement here. **Promoting either it or
  `0078`'s provenance rule to a project-wide control remains a separate ruling, still not taken**, now
  three entries running.

## 5. Scope

- **No published figure moves.** One vocabulary is fixed, one information-bearing column is dropped with
  the loss stated, and eight coverage populations are specified.
- **Both arms rerun.** **Neither of these, nor any of `0079`'s four, is satisfiable by editing an
  artifact** — B5 changes who writes the drop set, B6 labels every figure with its build, the inert
  positions are labelled in pipeline output, and **`0078` has never executed at all.**
- **Zero API calls in this entry. Step 8 is not adopted.**
