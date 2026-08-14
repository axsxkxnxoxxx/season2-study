# Decision 0078 — a count needs its provenance; two proposed rulings withdrawn for want of a source; D9 reports four numbers

| | |
| :--- | :--- |
| **Decision** | **Every count names the pipeline it was measured on, not only its population** — `0047`'s rule one layer down. **58,345 pairs and 178 of 2,549 are restated with their build, values unchanged.** **Two rulings the Human Lead proposed are WITHDRAWN: their figures had no source in the repo and contradicted both arms' measurements.** **D9 reports both halves under both keys — four numbers, not three.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 rerun, and a proposed pair of rulings the agent declined to propagate |
| **Status** | Closed. **Step 8 is not adopted.** |

---

## 1. Two proposed rulings, withdrawn — and this belongs on the record

**The Human Lead proposed two rulings whose figures had no source in the repository, and the agent
refused to propagate them.** Recorded here in full, at the Human Lead's instruction, **because that is
the control working and a record that omits it overstates how the rest was reached.**

**Proposed ruling 1** would have restated position 3's drop set as **5,652,563 records** rather than
58,345 pairs, and the discovery-channel overlap as **66 accounts** rather than 178, on the ground that
both figures had "gone stale by being followed."

**Checked before propagating, and it does not hold:**

- **Both arms measured 58,345 pairs and 178 of 2,549 accounts in the reruns that executed against the
  current spec.** Those reruns **postdate** `0075` and `0077`. They *are* the current pipeline, so the
  figures cannot have gone stale by being followed — they were measured after the rulings, not before.
- **`5,652,563` appears nowhere in the repository.** It is a **record**-scale quantity — the record
  universe is ~6,065,704 examined — while position 3's drop set is defined in **pairs**. If the intended
  object is *the records belonging to those pairs*, that is a **different quantity needing a different
  name**, not a correction to this one.
- **`66` matches no population either arm reports.** The three measured overlaps are **324 of 5,694**,
  **178 of 2,549**, and **174 of 2,422**.

**Proposed ruling 2** would have adopted instance A's "6 D9 complementary pairs" and recorded that
**instance B returned 0 because it never had the retained drop set.**

**Also contradicted by the deliverables:**

- **B has the drop set** — `processed/step8/b/position3_drop_set.csv.gz`, **58,345 rows**, written this
  run.
- **The two arms do not disagree on D9 at all.** Both report **strict 0, loose 75, third key 76**, and
  both report half (a) as **0 strict / 6 loose**. **The 6-against-0 is the strict-versus-loose
  difference WITHIN each arm** — which `0074` ruling 5 already governs — **not a divergence between
  them.** There was nothing to adopt and nothing to reconcile.

**Both withdrawn as stated. The Human Lead confirmed there was no source.** **Writing either figure
into the spec would have put unsourced numbers there that two independent measurements disagree with —
the exact failure this chain exists to prevent, committed on instruction.**

## 2. The principle survives, and it is the durable part

**A count needs its PROVENANCE, not only its POPULATION.**

`0047`'s standing rule fixed *"which population produced this figure."* **This is that rule one layer
down: which BUILD produced it.** **A count without its provenance can be correct when written and wrong
when read**, because the pipeline moved underneath it and nothing in the text says which pipeline it
belongs to. **The proposed rulings were an attempt to fix exactly that, on figures that turned out not
to need it** — the instinct was right and the instances were wrong.

**Restated, values unchanged:**

- **58,345 pairs — position-3 rule, position-5 build of 2026-08-13**, reproduced independently by both
  arms.
- **324 of 5,694 on the Step 3 discovery pool and 178 of 2,549 on the accounts pulled — same build**,
  both reproduced by both arms.
- **A third reading is recorded and NOT published: 174 of the 2,422 accounts in the APPLY position-5
  population** (instance B). **Recorded so it is not later read as a divergence** — which is the same
  provenance problem in its other form.

**The rule is now a standing requirement at the head of Step 8's required counts.**

## 3. D9 — four numbers, not three

**The one live asymmetry:** instance A published **half (b) under strict only**; instance B published it
**under both keys.**

**Required: both halves under both keys.** **This follows from `0074` ruling 5's own reason rather than
from a preference.** The loose count publishes **because it bounds how wrong strict could be** — and
**that reason applies to half (b) exactly as it applies to half (a).** **Publishing the bound for one
half and withholding it for the other leaves the reader unable to bound the total**, and **the error
runs opposite to D9's own lower-bound caveat**, which is the direction they were not warned about.

**Instance B's treatment is the required one.**

## 4. Surfaces

**REACHED:** `task-sheet.md` Step 8 — the provenance rule as a standing requirement, both figures
restated, and the D9 four-number requirement — and **both `analytics-engineer` files**, identically.
**Pair verified byte-identical apart from `name:`. All eight surfaces PASS.**

**DELIBERATELY NOT REACHED:**

- **The `data-scientist` pair** — the provenance rule is general, but **none of these three changes what
  Step 9 receives**, and Step 9 consumes Step 8's output rather than recomputing it (`0071`). **When the
  provenance rule is applied beyond Step 8 it reaches them; it is not applied beyond Step 8 here**, and
  that is a scope limit, not an omission.
- **`CLAUDE.md`** — the provenance rule is a Step 8 requirement in this entry, not yet a project-wide
  standing control. **Promoting it is a separate ruling and is not taken here.**
- **The arms' artifacts and `src/`** — no value changes, and their text is the record of the run that
  produced the figures being labelled.

## 5. Scope

- **No figure moves.** Two are relabelled, one is recorded rather than published, and one reporting
  requirement is widened from three numbers to four.
- **Zero API calls. Step 8 is not adopted.**
