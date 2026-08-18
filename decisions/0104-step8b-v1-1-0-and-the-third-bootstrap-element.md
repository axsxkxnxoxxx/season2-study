# Decision 0104 — Step 8b v1.1.0 closes all nine findings; levels-vs-movements is the one element still unfixed

| | |
| :--- | :--- |
| **Decision** | **No new ruling. Step 8b reran and closed all nine of `reviewer-engineering`'s findings by WIDENING the schema**, which keeps one definition per figure. **Validator: 27 checks (was 21), four terminal states, 33 mutations each failing the check they target.** ***One thing is NOT closed and it is a spec gap: `0103` fixed `B`, the seed and the resampling unit, but NOT levels-vs-movements — and the spec requires all THREE fixed identically, so STEP 9 REMAINS BLOCKED on that third element alone.*** |
| **Recorded by** | Analytics Engineer, on arm `a`'s Step 8b rerun |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s Step 8b review, F1–F9, and `0103`'s two rulings |
| **Verified by** | The placeholder validates with **0 failures**; **33 mutations each fail their target** and the case that must *not* fail does not; `check_surfaces.py` **exit 0** |
| **Status** | Open. **Step 8b returns to `reviewer-engineering`. Step 9 is blocked on §2.** |

---

## 1. All nine closed, and one gap the review did not find

**The review's structural conclusion held**: **not one finding was a step's output shape being
incompatible with the schema** — every one was the schema **requiring more or labelling less** — so all
nine fix by **widening**, and the **no-conversion-layer** rule survives intact.

**F1** block absences carrying status, reason and `owning_step`, with the DERIV per-arm liveness series
going in as `superseded_for_this_purpose` · **F2** `row_set`, `row_set_label` and `n_rows_in_row_set`
required, the per-population slot an array so all four cells exist · **F3** `ci_or_absence` for the
residue the ruling did not reach · **F4** a `search_record` and a fourth status, **EMPTY_DECLARED**,
which is **not** a failure while VACUOUS still is · **F5** `dual_status`, `arms.sole`, and
`not_a_dual_step` added to the absence enum · **F6** a `d3_prime_block` per arm and population · **F7**
`histograms` as an array with a `stratum` descriptor · **F8** implemented rather than retitled — S12 now
evaluates five identity families and cross-checks a `machine_checked` flag against what the code
actually evaluates, and S13 now asserts **position *k*'s `n_in` equals position *k−1*'s `n_out`**, which
is where a waterfall actually breaks · **F9** a required `$.block_ownership` registry, with
`channel_classes.d4`/`.d9` marked `copied_not_computed` and `limitations` as `human_lead_only`.

***And one gap the review did not find, which the arm found while fixing F1***: **the per-air-period
retained counts lived INSIDE the waterfall block**, so **an absent waterfall would have orphaned a figure
mandated at every arm.** Moved to `$.arms[].retained_by_air_period` — **one place, not a copy.**

**`0103` §2's caution is built for rather than assumed away.** `resampling_unit` is an **enum, not a
`const`**; `$.binding_clusters` maps quantity class → binding cluster with its source; **S24 fails an
interval whose unit differs from its class's binding cluster** unless it carries an `unit_disagreement`
record marked `reported_not_reconciled`. ***And a quantity class absent from the registry cannot carry a
CI at all*** — which is what makes silent inheritance impossible rather than merely discouraged.

## 2. The third bootstrap element, and Step 9 is still blocked on it

***`0103` fixed `B` = 10,000, the seed = `20260818`, and the resampling unit = account. It did not fix
LEVELS-VS-MOVEMENTS.***

**Both `data-scientist` files require all three fixed identically for both arms** — verified at
`.claude/agents/data-scientist.md:49` and `:169`. **So Step 9 remains blocked, on that one element.**

**Recorded in the schema as unfixed** — `bootstrap_spec.fields_not_fixed_in_spec` — **and varying per arm
in the registry**, which is `0103`'s own principle applied to the element `0103` did not reach: *an
unfixed spec must be visible in the output rather than silent.*

***This is a spec gap for the Human Lead, and the arm was right that it is not Step 8b's to rule.***

**And my own propagation of `0103` left a line stale**: both `data-scientist` files still read *"the spec
fixes neither `B` nor the seed nor levels-vs-movements."* **Two of those three are now fixed.**
Corrected at the point of use, with the surviving gap named.

## 3. Two limits the arm records about its own work

- ***The schema cannot tell whether a block absence is honest.*** It can require status, reason and
  owning step, and **forbid one on the primary headline arm** — but **a writer that declares a missing
  producer where one exists still validates.**
- **The bundled validator implements a JSON Schema subset with nothing independent to cross-check it**,
  and **Step 8b is single-arm, so there is no dual diff on the schema itself.**

**Both are in `known_limits_of_this_schema`**, which is what `0096` §1 requires: **an arm's own limits are
exactly what it must publish.**

## 4. Scope

- **No study figure is hard-coded in either artifact** — `196,654`, `147,370`, `6.2055`, `703`, `604`,
  `1,355`, `17,895`, `100.7104`, `9.6830`, `18,952`, `33,373`, **`632`, `1,293`** — **zero hits in both**,
  verified. **The `W` grid is still parsed from `task-sheet.md` at run time.**
- **Surfaces reached: 6** (both artifacts) and **2–3** (the stale bootstrap line). **Neither arm of Step 8
  ran.**
- **Zero API calls.** **Step 9 is NOT begun.**
