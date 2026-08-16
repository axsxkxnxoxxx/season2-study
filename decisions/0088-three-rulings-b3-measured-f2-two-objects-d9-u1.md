# Decision 0088 — B3 is measured; D9's two coverage quantities are two objects; the clustering universe is U1

| | |
| :--- | :--- |
| **Decision** | **B3: MEASURE BOTH.** The boundary window at `τ1` and `τ2`, a **per-site D11 table**, and the existing assertion **promoted into the published set**. A zero is labelled **vacuous**, never passed silently. **F2: REPORT BOTH AS SEPARATE OBJECTS.** **747,478 and 726,103 are different objects and both correct** — season-coverage **rows** against distinct `(user, show)` **pairs**. One arm's mislabel is fixed and the overstated coverage sentence is **struck**. **D9 UNIVERSE: U1**, all slugged sweep show IDs, **ranked by distinct strict keys merged.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's third and fourth Step 8 gate HOLDs. **B3 blocked on both** |
| **Amends** | `0085` §7 (B3 carried); `0086` §1 (the universe left open, and its false reconciliation sentence, already restricted at `0087`) |
| **Verified by** | `check_surfaces.py` **PASS**; the `analytics-engineer` pair byte-identical apart from `name:`, re-verified after **each** of the two propagation passes |
| **Status** | Open. **Step 8 is NOT approved.** Both arms rerun against this entry; Red Team gets a **fifth** pass |

---

## 1. B3 — measure both, and the two are not what the ruling named

**Ruled: measure both.** That is the option Red Team ranked first and the one that blocked two consecutive gate reviews.

***The ruling identified the two as invariants 7 and 8. They are not.*** **Invariants 7 and 8 are
already measured, already published, and already labelled DATA CHECK by both arms**, each carrying an
explicit *"THIS CAN FAIL ON REAL DATA"* annotation and a holding coverage identity —
`2422 + 0 = 2422` and `2402 + 0 = 2402` for invariant 7, `2874 + 0 = 2874` for invariant 8. **Red Team's
fourth pass praised exactly this**: *"both DATA CHECKS real and both reporting what they found."*
**Nothing is needed there, and the reasoning given for the ruling — that publishing them unmeasured
leaves two unchecked entries — describes a state that does not exist.**

**B3's two mandates are the HALF-OPEN UTC-INSTANT FORM and D11-AS-GLOBAL-CUTOFF.** The ruling's
*substance* — measure rather than publish a residual — **applies to them unchanged**, and is what is
propagated.

**What is and is not wrong today.** Both arms' compliance is **TRUE**, independently confirmed by Red
Team: no `.date()`, `dt.date`, `normalize()` or day-flooring anywhere in `step8_*.py`; instants are
int64 seconds throughout. **This was never a suspected bug.** What was missing is **any measurement of
whether either mandate is load-bearing on this data** — and an unmeasured pass is indistinguishable
from a check that looked nowhere.

**Three things are now emitted:**

- **(a) The boundary window**, position-5 row set, **both populations**. ***CORRECTED 2026-08-16
  (`0089`), by instance A: this entry named the window `[τ1 − 24h, τ1)`, WHICH IS THE INTERVAL ON WHICH
  THE TWO FORMS AGREE.*** `T0` is day-floored, so `τ1` and `τ2` are **midnight-aligned**, which makes
  `date(ts) < date(τ1)` identical to `ts < τ1` below the boundary. **The SEPARATING interval is
  `[τ1, τ1 + 24h)`.** **Both arms emitted both intervals rather than only the one named**, which is the
  only reason the measurement means anything — **an arm that answered with the named window alone would
  have returned a result on the interval that cannot separate the forms.** **Measured: exactly 1
  episode falls AT `τ1` on both populations, both arms**, so `0068`'s strictness ruling moves a real row
  in `|A|`; **and 0 outcome states differ**, because that row already has `|A| ≥ 1`. **If the count is 0,
  the invariant is labelled VACUOUS rather than passing silently.** ***Instance B's refinement, adopted:
  this is THREE states, not two — empty boundary / occupied-and-inert / occupied-and-deciding. Collapsing
  the middle into "vacuous" OR into "load-bearing for the result" are both misreadings***, and the
  measured state here is **occupied and inert**.
- **(b) A per-site D11 table.** D11 is specified to apply *"to EVERY computation"*, and one arm names
  **five sites in prose with a count at none.** Records excluded at **each** of `A`, `A_H`, the four
  `action_count_s{1,2}_*`, the liveness evidence, D9's coverage rows and the S1 walk — **asserted at
  each site, not once and about the rest.**
- **(c) The existing assertion promoted.** `assert (tau2[pos5] > τ_pull).sum() == 0` runs in one arm's
  pipeline today but sits **outside the published invariant set**, invisible to any reader of the
  deliverable. **Published, labelled CODE CHECK.**

**The ground for ruling rather than publishing a residual:** the unstated version of exactly this scope
produced Step 7's **792-against-791**, where one arm applied the restriction and the other did not.

## 2. F2 — two quantities under one name, and the ruling's conclusion is right

**Ruled: report both as separate objects, do not reconcile, fix the label.** **Correct — and the
figures are not the ones the ruling named.**

***The ruling described 747,478 and 726,103 as "show IDs against frame IDs." Neither is a show-ID count
and neither is frame-restricted.*** Both are **user-show quantities measured across the whole sweep**:

| figure | arm | what it counts |
| ---: | :--- | :--- |
| **747,478** | A | ***CORRECTED (`0089`): distinct `(user, show)` PAIRS.*** ~~undeduplicated season-coverage rows~~ — **that label was taken from the previous artifact's own `user_show_coverage_rows_undeduplicated` key, which was itself part of what F2 flagged as mislabelled.** Arm A's true undeduplicated row count is **1,217,122** |
| **726,103** | B | **distinct candidate `(user, show)` PAIRS** (435,643 + 8,834 + 281,626) |

**But the conclusion holds, and on a stronger footing than the reason given.** A user-show carrying two
seasons contributes **two rows and one pair**. **They are genuinely different objects, both correct, and
reconciling them would collapse two real quantities into one** — which the standing rule forbids.
**Each arm now states which it publishes and what it counts.**

**Also fixed:** one arm's **46,366**, computed off the D9 coverage pivot and **mislabelled
`distinct_show_ids_in_the_sweep`**, with a *"0 carry no slug"* clause computed against the wrong base.
**And where the arms' universes differ they are named as two objects** — the slugged-ID sets stood **62
apart** while both were called `U1`, which §3 now closes at the root.

***Struck whatever else is ruled:*** ~~*"The run asserts this, so a report that omitted a population
could not be written by this pipeline."*~~ **It is a control asserted to exist.** **8 of 13 coverage
identities are `cover(unit, pop, N, N)` where the population size and the asserted count are the same
expression**, so they cannot detect an invariant run on a population other than the one named.

## 3. D9's universe is U1, ranked by distinct strict keys merged

**Ruled: the whole sweep.** ***The ruling named it "U3"; U3 is the 75 candidate pairs, the narrowest
universe. The whole sweep is U1.*** **The reasoning identified U1 four separate ways** — *"the whole
sweep"*, *"the largest and slowest"*, *"can occur anywhere in a history"*, *"not only among shows that
survived the frame filters"* — **and the letter contradicted all four.** **Confirmed with the Human
Lead before propagating rather than resolved by inference.**

**Adopted: U1 — every distinct show ID appearing anywhere in the pulled sweep that carries a slug,
deduplicated to one row per show ID. Both arms cluster the same object.**

**The ground, as given:** the artifact D9 hunts is **a viewer's history splitting across two metadata
entries for one show**, and **that split can occur anywhere in a history.** A frame-restricted universe
finds only splits where **both sides made the cut** — the narrowest case — and **a bound computed on a
narrow slice bounds very little.**

***Recorded with the ruling, because it changes what the ruling buys: D9's SEARCH ALREADY RUNS ON THE
WHOLE SWEEP IN BOTH ARMS*** — 726,103 candidate pairs, 747,478 coverage rows. **So this does not widen
what D9 finds, and the strict and loose counts are unchanged by it.** What it fixes is **which clusters
are illustrated** — the evidence for the loose key's only warrant — and it **makes both arms' `U1` one
defined object** instead of two sets 62 apart under a shared label.

**The ranking basis is DISTINCT STRICT KEYS MERGED**, and it needed ruling because **it reorders the
list on its own**: the same universe under the same key, ranked by distinct show IDs, displaces
`maigret` with `blackout`. **The basis is named at the point of use.**

**`task-sheet.md`'s former illustration — The Twilight Zone, The Traitors, Manhunt — was U3 and is
SUPERSEDED as the example.** Under U1 the largest clusters are **`secondchance` (8)** and
**`theisland` (7)**, both unique at their counts and both reproduced exactly by both arms.

***THE THIRD PLACE IS NOT DETERMINED AND THIS ENTRY SHOULD NOT HAVE NAMED ONE.*** ~~`maigret` (6)~~ —
**there is a SIX-WAY TIE at 6**: `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor`.
**Which one appears third is the TIE-BREAK, which no rule specifies**, and the arms diverge on it: one
publishes `blackout` under ascending-key-after-descending-count, and `maigret` is equally correct under
another. **BOTH ARMS REPORTED THIS INDEPENDENTLY, and neither picked the name this entry gave.**
**A spec gap inside the ruling that closed a spec gap.** **CARRIED FOR THE HUMAN LEAD** (`0089` §4);
the divergence is reported, not reconciled, and every key at every rank publishes under both bases.

## 4. On the pattern — sixth occurrence, and the first with a working countermeasure

**All three rulings named the wrong referent** — invariants 7 and 8 for the half-open form and D11;
show IDs and frame IDs for rows and pairs; U3 for U1. **All three substantive decisions were sound and
all three are propagated.**

**What changed this time:** the Human Lead's standing instruction to report findings with the figures
they rest on and where they live **worked in the two cases where the substance was unambiguous** — each
mismatch was checkable against a named file and line, and each was checked before propagating. **On the
third it was not sufficient**, because the substance and the label pointed opposite ways with equal
force, so **it was put back rather than inferred.** **A rerun launched on the wrong universe would have
cost a full cycle and produced a Red Team pass on the wrong object.**

## 5. Scope

- **No population change, no bound endpoint moves, no `CLAUDE.md` dependency list touched.**
- **Surfaces reached: 1** (`task-sheet.md`) and **4–5** (both `analytics-engineer` files, identically —
  numbered per `CLAUDE.md`, after `0087` corrected the inversion in three entries). **2–3 deliberately
  not**: the `data-scientist` pair names none of these objects. **6, 7, 8: both arms rerun.**
- **Zero API calls.**
- **Both arms rerun. Step 8 goes to Red Team for a FIFTH pass.**
