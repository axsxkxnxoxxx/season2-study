# Decision 0066 — Step 8b is propagated, with the two amendments its drafting predates

| | |
| :--- | :--- |
| **Decision** | **Step 8b, output schema, is added to `task-sheet.md` between Steps 8 and 9** and to both `analytics-engineer` files identically. **Owner: Analytics Engineer. Mode: Chained. Review: Engineering.** Two amendments: **the key is `W` alone**, because the liveness rule is parameter-free; and **Step 9 publishes TWO bounds, not one**, on **both populations**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The step was defined in a prior session and **never propagated** — it existed in neither `task-sheet.md` nor either agent file |
| **Status** | Closed. **Step 8b is NOT launched.** It is Chained and sits behind Step 8, which is the remaining gate. |

---

## 1. The step, as defined

**Define the JSON schema the Step 16 visualization reads from.** One entry per tested arm, each carrying
the three outcome shares, a confidence interval on each, the bounds, the retained row count, the
abandonment distribution and the filter waterfall counts. **Emit a placeholder file with illustrative
values and the identical schema**, so Step 16 can be built before results exist. **Steps 9 through 13
write into this schema directly. No conversion layer.**

**Deliver:** schema definition, placeholder file. **Review:** Engineering, on whether Steps 9 through 13
can write into it without restructuring their outputs.

## 2. Amendment 1 — the key is `W` alone

The original read *"one entry per tested combination of `W` and liveness threshold."*

**There is no liveness threshold.** One was derived **three times** — 632 days, then 1,293 — and
**deleted** at `0042`, because taking a percentile of the distribution the test is applied to sets the
level by the exclusion rate rather than by any feature of the data. **The adopted rule is
parameter-free** (`0048`, approved at `0064`).

**So the schema is keyed on `W` alone**, and neither number may appear as a schema key. **Recorded with
it, because a blind grep gets this wrong: `632` is also the legitimate frozen-D10 never-started
component at `W = 125`** (`0051` §3 item 9).

## 3. Amendment 2 — two bounds, on two populations

The original read *"floor and ceiling bound"*, singular. **Step 9 publishes two.**

| | Floor / ceiling | Conditional sub-interval |
| :--- | :--- | :--- |
| **Never started** | yes | **none — structurally** |
| **Started and left** | yes | **yes** |

**Never-started has no sub-interval, and the schema must say so rather than omit the field.** The
sub-interval conditions on *that bound's own* exclusion set (`CLAUDE.md`, `## Derived figures`), so for
never-started it does not exist. **An absent field and an inapplicable one must not look alike** — this
study has spent seven entries on figures that were superseded and looked current, and a missing field
that looks like an omission is the same failure in the other direction.

**And on DERIV the never-started bound is DEGENERATE** — `[6.2055%, 6.2055%]`, width 0.0, zero
never-started exclusions. **A zero-width bound must not read as missing data.**

**On DERIV the started-and-left sub-interval COINCIDES with its bound**, because the never-started
exclusion component is 0 there. **Coincidence is recorded as a measured fact**, not by writing the same
numbers twice with no note.

**Both bounds on both populations — APPLY 196,654 and DERIV 147,370 — as separate arithmetic, never one
field with a population flag**, and **every bound field states its population**, which is the standing
rule from `0047`.

**The Human Lead's phrasing was "each with floor, ceiling and the conditional sub-interval."** Taken
literally that gives never-started a sub-interval it does not have. **Implemented as above and flagged
rather than followed to the letter**, because the schema is the artifact Step 16 reads and an
inapplicable field would be built against.

## 4. Four things the step needs that its drafting also predates

**Not amendments the Human Lead named — consequences of rulings made since, written in because a schema
that omits them cannot hold Step 9's output.**

- **Continued has a ceiling and it is part of the entry** (`0050`, `0052`). **The three ceilings cannot
  all hold** — APPLY 100.7104%, DERIV 100.1276% — so the schema carries **the sum and the excess per
  population** and must not let a consumer read three ceilings as simultaneous. **Continued is never
  emitted as a point.**
- **The scope qualifier is a field, not caption prose** (`0062`): *covering with respect to
  insertion-dormancy, exhaustively; open only across channel classes (D4, D9)*. **D4 and D9 publish
  alongside and are never folded in**, so the schema has slots for them.
- ~~**A dual step is diffed IN this schema**~~ ***RETIRED by `0107` (E2, found by `reviewer-engineering`): it has NO WRITER — two isolated instances cannot jointly produce one document, and no arm may be the merge owner without defeating dual implementation. **A dual step is diffed BETWEEN TWO ARM FILES, BY THE HUMAN LEAD, BEFORE THE MERGE.*** The rest of this item stands, scoped to the MERGED document, which must hold **both arms' values where the arms
  legitimately differ.** The bound ÷ sampling-width ratios use **two conventions and are reported, not
  reconciled** (`0058`, `0063`). **One slot per figure would force a reconciliation the spec forbids** —
  the schema would silently do what `0057` did by hand and `0058` reverted.
- **Each CI records the bootstrap settings that produced it.** `B`, seed and levels-vs-movements all
  differ between the arms and **the spec fixes none of them**. **An unfixed spec must be visible in the
  output**, not silent.

## 5. Why "no conversion layer" is the load-bearing line

**A conversion layer is a second definition of every figure**, and **two definitions of one figure is
the defect this study has hit most often**: `0058` (hand-patching reached one file and missed another),
`0061` (one literal in two writers, one edited), `0062` (`STATEMENTS` and `figure_table()` created
precisely to end it). **The step's own instruction is the control.**

**And the placeholder is the same hazard.** It must be **unmistakable as a placeholder** — a top-level
flag a consumer cannot miss, values that cannot be mistaken for measurements. **A placeholder that reads
as data is the failure mode**, and it would reach Step 16, which is the visualization.

## 6. Scope

- **Propagated to `task-sheet.md` and both `analytics-engineer` files identically**; the pair is
  byte-identical apart from `name:`. **Verified by grep, not by read-back** (`CLAUDE.md`).
- **Not propagated to the `data-scientist` pair.** Steps 9–13 *write into* this schema, but the schema
  is the Analytics Engineer's deliverable and does not exist yet. **When it does, the `data-scientist`
  files gain the obligation to write into it** — recorded here so that pass is not forgotten, which is
  how the covering qualifier went six entries reaching no agent file.
- ~~**Nothing is launched.** Step 8b is Chained and sits behind Step 8, which is the remaining gate.~~ ***SUPERSEDED 2026-08-18 (`0102`): Step 8 was APPROVED at `0098` and Step 8b RAN as arm `a`.*** **And §6's carried obligation — that the `data-scientist` pair gains the duty to write into this schema once it exists — is DISCHARGED at `0102`. It had gone 35 entries undone**, which is the failure §6 was written to prevent.
- **Zero API calls.**
