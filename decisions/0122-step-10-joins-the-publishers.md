# Decision 0122 — Step 10 joins `INTERVAL_CLASS_PUBLISHERS`; it is not exempted

| | |
| :--- | :--- |
| **Decision** | ***STEP 10 JOINS `INTERVAL_CLASS_PUBLISHERS["outcome_shares"]` AND IS NOT EXEMPTED.*** **The merged placeholder's worked example of Step 10 was THE THING CORRECTED — not the check.** ***`window_w_percentile` is NOT reached by this ruling*** (§4). |
| **Decided by** | **Human Lead**, 2026-08-20 |
| **Date** | 2026-08-20 |
| **Amends** | `INTERVAL_CLASS_PUBLISHERS`; the merged placeholder's Step 10 example. **Does NOT amend `0121`** — see §3 |
| **Status** | **FILED 2026-08-20 and PROPAGATED.** Implemented in `artifacts/` at schema **v1.9.0**; ***this entry is the FIRST time it reaches a spec surface*** — §5 |

---

## 1. The ruling

**Step 10 joins `INTERVAL_CLASS_PUBLISHERS["outcome_shares"]`. It does NOT join
`INTERVALS_NOT_MANDATED_BY_STEP`.**

## 2. The reasoning, recorded as given

> **Step 10 measures outcome shares on the primary arm under a fixed bootstrap. That is a quantity
> with a real interval**, so exempting it would assert that **Step 10 mandates intervals nowhere,
> which is false** — and **the Step 12 exemption rested on that clause being TRUE of Step 12.** The
> merged placeholder's worked example of Step 10 as a headline absence **is the thing that is wrong**,
> and it is corrected to a shape Step 10 can actually write.

## 3. ***Why this strengthens `0121` rather than narrowing it***

**Before this ruling, Step 10 could not write a valid file at all.** The two tables were individually
defensible and **jointly closed against it**: with no intervals it failed `S41`; publishing
outcome-shares it failed `S38`, because the publisher table omitted `step10`. **The only escape was
`other_declared` — "the class for a quantity the record has not ruled on."** `reviewer-engineering`'s
warning, adopted: ***it must not be resolved by a Step 10 writer discovering `other_declared`.***

**The available fix was an exemption, and taking it would have hollowed out `0121`.** `0121`'s
exemption is warranted **by a true statement about Step 12** — it mandates intervals nowhere.
**Granting the same exemption to a step for which that statement is false would make the exemption a
convenience rather than a finding**, and would retroactively weaken the one it was modelled on.
***So the ruling went the other way: the step joins the publishers, and the EXAMPLE was corrected.***

**This is `0121` §2's second half applied again** — a control and a statement of fact disagreed, and
**the false object was corrected.** In `0121` the check was wrong; here **the placeholder was.**

## 4. ***`window_w_percentile` is NOT reached, and the reason is on the record***

**The arm reported this rather than deciding it, and its reasoning is adopted:**

> **`INTERVAL_CLASS_PUBLISHERS` is a PERMISSION table** — adding a step *licenses* it to attribute a
> quantity. **W is derived at Step 6, reported at Step 9's two window arms and across Step 13's grid.
> Step 10 charts the headline arm WITHOUT VARYING W.** So adding `step10` there would **license it to
> attribute a quantity it does not compute** — ***the exact state `0114` E11 closed***, when the sole
> placeholder attributed the window-W percentile to `step11`.

**The ruling's ground names OUTCOME SHARES and nothing else. A ruling reaches what its ground reaches.**

**A control consequence, reported rather than left to be inferred:** `MUTATIONS["S38"]` had attributed
an *outcome-shares* interval to `step10` and **stopped failing the moment this ruling landed** —
`checks_without_force: ["S38"]`. **The selftest caught its own loss of force**, and the mutation was
retargeted to the `window_w_percentile` row, **by predicate rather than by index**, so it exercises a
row that is still false. ***A mutation that stops discriminating when a ruling lands is a control
telling you the world moved under it.***

## 5. Propagation and the fixture

**Implemented in `artifacts/` at v1.9.0.** ~~Surfaces 1–5 carry nothing~~ ***TRUE UNTIL FILING.***
**The arm declined to propagate, correctly**, its only source being its launch instruction (`0120`
§6). ***FILED ALONGSIDE `0121` AND PROPAGATED 2026-08-20.***

**REACHED:** **1** `task-sheet.md` (Step 10 section, 1 site); **2–3** both `data-scientist` files
(named in the canonical block's carve-out as the contrast case — *no other step is exempt* — 1 site
each); **4–5** both `analytics-engineer` files (1 site each, identical); **7** `second-brain` (1
site). **6** `artifacts/` carries it at v1.9.0. **8** `processed/` — **0 occurrences, verified.**

**The fixture is pinned to THIS ENTRY, not to either table.** Step 10 **FAILS** when it omits
intervals, **PASSES** when it publishes both objects, **FAILS** on levels-only. Verified live:
**dropping `step10` from `INTERVAL_CLASS_PUBLISHERS` drives exit 1; adding it to
`INTERVALS_NOT_MANDATED_BY_STEP` drives exit 1.**

## 6. Carried, not closed — `E2` and `E5`

**`E2` — `S42` CANNOT SEE THE DEFECT IT WAS BUILT NEXT TO.** `src/step8b_validate.py:3586-3588` reads
`schema_version.const`, `schema_id.const` and `$id` **all three from the file under test.** So it
catches **disagreement between them** and can **never** catch **a schema whose three identifiers are
uniformly one version behind its generator** — *"the artifacts carry the old thing until the next
rerun"*, which `CLAUDE.md` names as this project's own structural defect. **Nothing compares
`G.SCHEMA_VERSION` against the artifact's.**

> ***THAT IS THE TABLE-UNDER-TEST CLASS FOR THE THIRD TIME, AND IT IS SITTING INSIDE THE FIX FOR THE
> SECOND.*** The first was the E2 partition anchor; the second, the S41 fixture that read
> `INTERVALS_NOT_MANDATED_BY_STEP`; **this is the third, in the check written to close a version
> defect.** **Every one arrived inside the fix for a prior finding.** **To close before the next
> version bump.**

**`E5` — two rulings unpropagated, and a register row citing an entry that did not exist.** `0121` and
this entry both sat in `artifacts/` and on no spec surface. **And the `WITHDRAWN_PHRASES` rows added
for the E6 retirements cite `0121` — which did not exist when they were written.** ***The fifth
cite-before-write in this study, and the first inside the register built to catch that class.***

***AND MY DIAGNOSIS OF WHY THE RESOLVER MISSED IT WAS WRONG THE FIRST TIME. CORRECTED HERE.***
**I reported that a bare `"Withdrawn 0121"` matched none of `CITE`'s patterns and that this was why
`check_surfaces.py` exited 0. The first half is true. The second is not.**

**The hole was SCOPE-shaped, and that is the operative one.** `scan_citations()` walks `SURFACES`, and
***`src/` IS NOT A SURFACE***, so a citation in `src/step7_register.py` was invisible **whatever the
regex said.** **Widening the pattern alone left the control still passing at exit 0 with `0121`
absent** — found only because I probed both directions instead of declaring the fix good.
***A fix verified in one direction only is the shape this build has now produced four times.***

**Both halves were needed and both are closed:**

- **FORM** — the withdrawal and correction verbs this log actually writes, bare and unbackticked.
  Deliberately **not** a bare four-digit match: that catches years, counts and `W` values, and a
  resolver flagging every four-digit token would be withdrawn within a day. Probed: `Withdrawn 0121`,
  `Corrected at 0119`, `superseded by 0093` resolve; *"the 1980 count"* and *"W = 0108 days"* do not.
- **SCOPE** — `src/*.py` added to **the citation scan only**. ***`src/` is NOT promoted to a
  propagation surface*** — that is a `CLAUDE.md` change and the Human Lead's.

***Why the register is the sharp case:*** `CLAUDE.md` makes a register row's citation its **WARRANT**
— *"the decision entry that adds or withdraws a row cites it"* — so it is **the one place a dangling
cite DISARMS A CONTROL** rather than merely confusing a reader. **Both halves of the check were blind
to exactly that place.**

**Verified both directions: with `0121` absent, exit 1, naming *"cited in 2 file(s):
`src/check_surfaces.py`, `src/step7_register.py`"*; with it present, exit 0.** **The rows resolve once
this pair is filed** — one more reason the pair is filed together.
