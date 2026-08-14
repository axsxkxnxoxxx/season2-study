# Decision 0079 — the drop set is a deliverable, provenance applies to everything, the overlap publishes in both units, and the four inert positions are labelled

| | |
| :--- | :--- |
| **Decision** | **B5:** the position-3 drop set is a **Step 8 deliverable produced by the pipeline**, not a helper script's side file. **B6:** the provenance rule applies to **every count and every invariant**, not two. **B7:** the channel overlap publishes in **both units, each with its consumer named**. **And the four inert filter positions are KEPT and LABELLED INERT with the reason.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's second Step 8 pass |
| **Status** | Closed. **Step 8 is not adopted.** |

---

## 1. B5 — the drop set is a deliverable

**D9 half (b) cannot be computed without the position-3 drop set, and its absence returns 0 SILENTLY** —
**a plausible-looking data finding rather than an error.** A zero split-artifact count publishes as
evidence the artefact does not occur.

**That is precisely the failure `0075` ruling 2 was written to prevent**, so **leaving the input as a
working file defeats the ruling that requires it.** A helper script's side file is not a thing the next
run is obliged to produce.

**Now: named in the deliverable list, written by the same pipeline run that writes the table**, carrying
each pair's distinct-episode counts and the show's threshold, which is what half (b) reads.

## 2. B6 — provenance applies to everything, or it argues against itself

`0078` established that **a count needs its provenance, not only its population**, and applied it to
**two figures**.

**Partial application is worse than none.** Two labelled figures **imply the other counts and the eight
invariants did not need it** — the reader takes the labels as marking the exceptional cases rather than
the rule. Step 8's required-counts section alone runs to **24 bullets**, and every invariant result is a
figure too.

**Every count, every invariant result and every waterfall figure carries the build it was measured on.**

**Red Team's finding stands behind this: `0078` is currently unexecuted** — **no count on either
surface carries its build**, because the ruling arrived after both arms had run.

## 3. B7 — both units, each with its consumer

**Picking one unit leaves the other consumer holding a wrong-unit figure.** All three readings publish:

| Figure | Unit | Consumer |
| :--- | :--- | :--- |
| **324 of 5,694** | discovery-pool **usernames** | Step 3's seeding-bias statement; **Step 14 ledger item 1** — the pool's composition |
| **178 of 2,549** | **accounts pulled** | Step 4 coverage reporting |
| **174 of 2,422 accounts; 17,783 of 196,654 pairs** | **position-5 population** | **Step 11** |

**One correction to the ruling as dictated, because the mapping is reversed against the files.** It
assigned **Step 11 to users** and **the pool statistic to accounts**. **Step 11 recomputes the headline
separately within Channel A and Channel B** — the headline is over **pairs on the position-5 row set**,
so Step 11 cuts **the analysis population, not the pool**; and **the pool statistic is the 5,694
usernames.** **The reverse of the dictated mapping.** The ruling's substance — both units, consumers
named — is executed correctly, and **all three readings publish rather than two.**

**This is the second ruling this session whose substance was right and whose instances were reversed**,
after the set-membership/S1-completion conflation at `0077`. Recorded because the pattern is the thing,
not the individual slip.

## 4. The four inert positions — kept and labelled

**Positions 1, 2, 3 and 7 each remove 0 rows**: the frame, the `L2 = 1` exclusion, the S1 completion
rule and outcome assignment.

**Keep them.** **Removing a position removes the check that would catch a future upstream change**, and
the point of a fixed order is that the waterfall is comparable across runs and across arms.

**But label them, with the reason.** **An unlabelled always-zero filter reads as evidence THE RULE FOUND
NOTHING when it is evidence THE RULE CANNOT FIRE — the same defect as an unlabelled code check**
(`0069`), and this step now has four of each.

| Position | Why it is inert |
| :--- | :--- |
| **1** frame | line 1 is already the frame |
| **2** `L2 = 1` | line 1 is already the `L2 > 1` S1-completer population (`0068`) — **and 0 `L2 = 1` shows exist in the frame**, measured by both arms |
| **3** S1 completion | same — **but position 3's RULE is not inert. It removes 58,345 pairs UPSTREAM of line 1**, which is why its drop set is a deliverable (§1). **The position is inert; the rule is the study's largest single exclusion** |
| **7** outcome assignment | it **annotates and removes nothing** (`0046`) |

**Row 3 is the one that matters.** Red Team's structural observation — that the study's largest single
exclusion appears in the waterfall as a `0` — is answered **not by reopening `0068` but by labelling the
position and publishing the rule's 58,345 as a deliverable.** The waterfall stays comparable and the
exclusion stops being invisible.

## 5. Surfaces

**REACHED:** `task-sheet.md` Step 8 — all four, including the deliverable line — and **both
`analytics-engineer` files, identically.** **Pair verified byte-identical apart from `name:`. All eight
surfaces PASS.**

**DELIBERATELY NOT REACHED:**

| Surface | Why |
| :--- | :--- |
| **both `data-scientist` files** | **B7's Step 11 row is the exception worth watching.** Step 11 is `data-scientist`-owned and now has a named figure — **174 of 2,422 accounts, 17,783 of 196,654 pairs.** It is **not propagated here** because Step 11 consumes Step 8's table and the channel flags are columns on it, so the figure travels in the data rather than in the spec. **If Step 11 is ever specified to quote the overlap, this needs a pass** — recorded so it is not discovered later |
| **`CLAUDE.md`** | B6 widens provenance **within Step 8**. **Promoting it to a project-wide standing control is a separate ruling and is still not taken** — `0078` §4 said the same and it remains true |
| **`artifacts/`, `processed/`, `second-brain`** | **no figure moves.** B5 changes who writes a file, B6 and B7 change labelling, and the inert-position ruling changes annotation. **Checked, not assumed** |

## 6. Scope

- **No published figure moves.** One input becomes a deliverable, every figure gains a build label, one
  figure gains two more readings, and four positions gain a label.
- **Both arms will need a rerun to execute B5, B6 and the labels** — none of the four is satisfiable by
  editing an artifact.
- **Zero API calls. Step 8 is not adopted.**
