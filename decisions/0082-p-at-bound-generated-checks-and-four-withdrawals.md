# Decision 0082 — `p_at_bound` is added, generated checks are committed, and four proposed rulings are withdrawn

| | |
| :--- | :--- |
| **Decision** | **`p_at_bound` is added — a boolean separating the two meanings of `p = 1.0`.** The column set becomes **89, enumerated.** **A generated file that functions as a check is COMMITTED, and must state what generated it and when** — added to `CLAUDE.md`. **Four proposed rulings are WITHDRAWN: none of their referents exists on disk.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Four proposed rulings, two of which survive on figures that exist |
| **Status** | Closed. **Both arms rerun on the two surviving rulings.** |

---

## 1. Four proposed rulings, withdrawn — and this is the second occurrence

**Recorded as `0078` §1 recorded the first, at the Human Lead's instruction, because the control working
is the part worth having on the record.**

| Proposed | Why it was not propagated |
| :--- | :--- |
| **1. Deduplicate `has_s2_evidence` / `s2_evidence_any`, publish 88** | **There is no duplicate column.** Neither name is in either arm's table or in the verified 88-name list, and **neither table contains ANY duplicate column name** — checked directly. The two names exist in the repo in **different eras and different files**: `has_s2_evidence` in Step 7 artifacts and source, `s2_evidence_any` in `src/step5_pairs.py` and `step5_rule_costs_v2.py`. **They have never been columns of the same table.** And 88 was already published by `0081` |
| **2. Split the over-strict invariant into a bound and `A ⊆ E2` / `D1 ⊆ E1`** | **Neither arm uses those terms anywhere.** What both report is *"distinct episodes never exceed season length (`\|D\| ≤ L`)"*, **labelled CODE CHECK**, running after `0080` on **both seasons over all 278,452 pairs** with its coverage identity holding: `278,452 + 0 not asserted = 278,452` |
| **3. A `p = 1.0` boolean, on 4,224 rows** | **`4,224` appears in no artifact or JSON in the repository.** Both arms publish **1,246 at position 5 and 1,230 post-liveness.** **The principle survives on the real figures — see §2** |
| **4. Commit `spec_columns.py`** | **The file does not exist.** Zero files in the repository contain the string. **The principle needs no referent and survives — see §3** |

**The pattern, stated because it has now happened twice: the reasoning holds and the referents are
invented.** At `0078` the provenance instinct was right and its two figures had no source. Here **three
of the four principles are ones the record should want** — split an over-strict check, disambiguate a
two-meaning column, commit the file that would have caught a defect — **and every referent is absent.**
**Directionally right, specifically wrong.**

**The Human Lead identified the cause: reading from a report rather than from the files.** That is the
same failure the `0051` mislabel was — adopting a figure without checking it against the arms' own
output — and it is why `CLAUDE.md` makes the on-disk files authoritative over any summary of them.

## 2. `p_at_bound` — the surviving half of proposed ruling 3

**`p = 1.0` carries two meanings computed differently**: the pair **left at the final episode**, or **the
abandonment point is at its bound**, the rank numerator having saturated at `L2`.

**`p_at_bound` is TRUE where `p = 1.0` arises from the bound, FALSE where it arises from the final
episode**, null where `p` is null.

**Why it matters, and this is the part that stands on the files: Step 10 publishes the abandonment
distribution off `abandonment_point_p`.** **A spike at 1.0 means two different things about viewers, and
the column cannot currently say which.**

**Both arms must report the split of the `p = 1.0` rows into the two classes, on the totals they
themselves published — 1,246 at position 5 and 1,230 post-liveness on APPLY — and the classes must sum
to those.**

**The column set moves 88 → 89 as a mechanical consequence, stated rather than left to be recounted**,
given that this count has been 87, 88, 89 and 90 across four entries. **All 89 names are enumerated in
all three surfaces and verified name-by-name against the ruling and each other.**

## 3. Generated files that function as checks — proposed ruling 4's principle

**A check nobody can see is not a check.** **A generated file that functions as a check is committed** —
a verification living only in a working tree verifies nothing anyone else can rely on, and **it is
invisible to all eight propagation surfaces, which is where the defects this project keeps finding
actually hide.**

**Condition, and it is not optional: a committed generated file states WHAT GENERATED IT and WHEN.**
Otherwise it becomes **the stale-figure problem the provenance rule exists to prevent** — a file that
looks authoritative, is read as current, and was produced by a pipeline that has since moved. **A
generated file without its provenance is worse than no file, because it is trusted.**

**In `CLAUDE.md` as a standing rule**, governing the generated artifacts that already exist — including
`src/step7_regenerate_derived.py`'s output blocks and the stamps it writes.

## 4. Surfaces

**REACHED:** `task-sheet.md` Step 8 and both `analytics-engineer` files — **the 89-name enumeration and
the `p_at_bound` specification**, verified identical to the ruling and to each other. **`CLAUDE.md`** —
the generated-files rule. **Pair byte-identical apart from `name:`. All eight surfaces PASS.**

**DELIBERATELY NOT REACHED:** the `data-scientist` pair and Step 8b. **Step 10 is the consumer of
`p_at_bound` and is `data-scientist`-owned** — but Step 10 reads Step 8's table through **Step 8b's
schema**, which is the single definition `0066` requires and which is not yet written. **When Step 8b is
built, `p_at_bound` reaches Step 10 through it. If Step 10 is ever specified to name the column
directly, that needs a pass** — recorded so it is not discovered later.

## 5. Scope

- **No published figure moves.** One column is added, one count moves as a consequence, one standing
  rule is added, and four proposed rulings are withdrawn without reaching any file.
- **Both arms rerun** on the two surviving rulings.
- **Zero API calls. Step 8 is not adopted.**
