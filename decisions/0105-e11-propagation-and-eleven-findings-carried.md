# Decision 0105 — E11 fixed: my `0103` propagation reached two of four sites; eleven findings carried

| | |
| :--- | :--- |
| **Decision** | **No new ruling. E11 is fixed** — `0103`'s propagation reached **two of four sites**, and I reported it as *"corrected at the point of use."* **Both `data-scientist` files then carried two contradictory statements about whether Step 9 was unblocked, ten lines apart.** **All four sites now name the ONE surviving element.** ***`reviewer-engineering` returned "yes, with named exceptions — ELEVEN, two blocking at Step 9 and one at Step 13," and OWNED ITS OWN CONTRIBUTION to two of them.*** **E1, E2 and E3 are carried for the Human Lead.** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s Step 8b **re-review** of v1.1.0 |
| **Amends** | `0104` §2's claim that the stale bootstrap line was corrected |
| **Verified by** | `check_surfaces.py`; the negative and positive halves both run on the four sites |
| **Status** | Open. **Step 9 is blocked by E1, E2 and levels-vs-movements — three independent causes.** |

---

## 1. E11 — mine, and it is the shape the read-back rule exists for

**`0104` §2 said the stale bootstrap line was *"corrected at the point of use."* It reached `:108` and
`:150`. It did not reach `:49` or `:165–171`.**

**So both `data-scientist` files carried, simultaneously:** the correction saying `B`, the seed and the
unit are fixed — **and** *"**THE BOOTSTRAP IS UNSPECIFIED AND THIS BLOCKS STEP 9**"* with *"all three …
must be fixed identically."* **Ten lines apart in one case.**

***That is `CLAUDE.md`'s read-back-plus-grep rule failing exactly as written***: *"a file can hold both at
once — an adopted figure and its superseded predecessor live in the same file, sometimes ten lines apart,
each declaring the other wrong."* **I read the edit back and did not grep for what remained.**

**And `reviewer-engineering` named the consequence precisely: it reaches the right outcome — stop — for
the wrong reason**, three unfixed rather than one. **A correct instruction resting on a false premise
survives until the premise is load-bearing, and then it does not.**

**All four sites now name the one surviving element**, verified both ways: the unqualified form returns
**0** on both files, and `levels-vs-movements` returns **4**.

**One more stale claim fixed in the same pass**: *"Step 8 is the remaining gate"* — **Step 8 was approved
at `0098` and all five gates are approved.**

**And a requirement the reviewer added that I have propagated:** when levels-vs-movements **is** fixed,
**a check must assert both arms' `statistic` agree** — the way `S23` asserts the inline restatement —
**or the fix will be recorded and unpoliced.**

## 2. The two blockers the Human Lead must rule on

***E1 — `S17` requires a block that `$.block_ownership` forbids Step 9 from writing.*** The validator
fails any file without `$.cross_arm_divergences`; the schema does **not** require it; and the ownership
registry marks it `owner_step: human_lead`, `may_first_writer_fill: false`,
`forbidden_to_compute_here: ["step9", "step13"]`. **Verified on disk.**

**So an isolated Step 9 arm has three options and no honest one**: omit and fail, declare
`performed: false` and fail, or declare a **cross-arm search it is structurally forbidden to have
performed, because it cannot see the other arm.** ***The validator does not merely permit the
fabrication — it is the only path to exit 0.***

***E2 — "diffed IN this schema" has no writer.*** `dual_status: "dual"` requires **both** `arms.a` and
`arms.b`. **Two instances that never see each other's work cannot jointly produce one document**, and
**no merge owner is named** — nor could an arm be one, under isolation. **The schema silently answered a
question that needs a ruling: one file per arm, or a merged file with a named owner.** **E1 and E3 both
depend on the answer.**

***E3 — Step 13 is dual and only its HEADLINE is dual-capable.*** `0104` said its payload nests per
producing arm "exactly as Step 9's does." **That is true of `headline` alone.** The per-arm liveness
series, `d3_prime`, `retained_by_air_period`, `action_type_counts`, the variant blocks and
`tested_ranges` each have **one slot** — and `task-sheet.md:857` says in terms that **a schema with one
slot per figure forces a reconciliation the spec forbids.** **Cheap now, expensive after Step 13 runs.**

## 3. What the reviewer owned about its own first pass

***It marked two of the eleven as its own doing, unprompted.***

- **F4 was under-specified by it**: it asked for the empty-versus-unsearched distinction **without asking
  who owns the search** — and **E1 and E5 are the direct result.**
- **F1 and F3 it framed as *"the schema requires more than the spec asks"***, which it now calls
  **correct and incomplete**: *"each absence branch is also a hole, and I did not say where the floor
  was. E4, E7 and E8 are the bill for that."*

**That is the same standard this chain applies to the arms, applied by a reviewer to itself**, and it is
worth recording because **a review that cannot do this produces findings that compound rather than
converge.**

## 4. Carried, with the reviewer's own ordering

**Cheapest first, its words:** **E1 and E5 are one afternoon in the validator. E4 and E7 are three lines
each. E2 and E3 need a ruling BEFORE the arm reruns**, or the Step 13 rework lands after Step 13 has
run. **E11 was a grep away and is done.**

**Also carried:** **E6** — `S24` holds as claimed, but its registry is **writer-fillable**, so it is a
**self-consistency check, not a conformance check**, and the schema **has no CI slot a `W` percentile
could ever occupy**; **E8** — mandated deliverables now optional, including **Step 11's intervals swept
in with Step 12/13's residue**, and **`subpopulation_cuts` without the `search_record` that
`cross_arm_divergences` got, which is the list where cherry-picking is the named risk**; **E9** —
`ratio_block` stores **no operands**, so a derived number's inputs are absent from the file; **E10** —
`$.block_ownership` is **a label, not a control**, and is **closed at top level and open where the risk
is.**

**On levels-vs-movements the reviewer confirms the disposition is right**, and adds that **nothing else
in the schema is blocked behind it** — **E1 and E2 block Step 9 independently and would do so even if it
were ruled tomorrow.**

## 5. Scope

- **Surfaces reached: 2–3** (all four sites, identically). **No artifact changed; neither arm ran.**
- **Zero API calls.** **Step 9 is NOT begun.**
