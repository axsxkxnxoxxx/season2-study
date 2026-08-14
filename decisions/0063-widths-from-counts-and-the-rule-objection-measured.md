# Decision 0063 — widths are computed from counts; the rule objection is closed on measurement; the residual is logged

| | |
| :--- | :--- |
| **Decision** | **2.5 fixed:** every bound width is now `(ceil_n − floor_n) / n`, not a difference of two 6-dp rounded percentages — the construction the register itself names as a rounding artifact. **The rule objection is CLOSED ON MEASUREMENT**: Red Team's no-conjunct-2 alternative **is PF-LIMIT**, adopted at `0041` and superseded at `0046`, and the 652 it asked for is printed in `0045` §1. **Everything else from review 15 is LOGGED AS OUTSTANDING, not fixed.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **fifteenth** Step 7 HOLD |
| **Verified by** | `check_surfaces.py` **PASS**, `step7_regenerate_derived.py` **PASS**, `step7_floor_extremes.py` **11/11 CONFIRMED** |
| **Status** | Closed. **Step 7's approval is drafted for the Human Lead at `artifacts/step7-gate-approval-DRAFT.md` and is UNSIGNED.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-14**. The clock had advanced mid-session and the date was taken from it rather than from the working day the entry belongs to. **Corrected in place across every surface, with this note, exactly as `0058` §6 did** — the decision log is a public tracked artifact and a date that quietly moves is worth less than one that visibly did. **Ruled by the Human Lead: the dates on `0060`–`0063` are wrong, not the approval.** The Step 7 approval at `0064` stands at **2026-08-13**, and with this correction it no longer predates `0063`, which carries the 652 measurement it rests on.

---

## 1. The rule objection — closed on measurement, and the measurement was already in the record

**Red Team's fifteenth review moved off the record and onto the rule**, for the first time since review 8. Its argument: conjunct 2 is `NOT Continued`, so the filter is **outcome-conditional** — a silent pair is excluded iff it is not Continued, and Continued pairs are structurally unexcludable. Its proposed alternative, *"the one nobody has priced"*: **drop conjunct 2.** Its close condition: report `|cont ∧ (last ≤ τ1)|`.

**Measured. One line, zero API calls, on masks already on disk:**

| | n | ALT-BROAD | **cont ∧ silent** | no conjunct 2 | growth |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **652** | **1,355** | 1.93× |
| **DERIV** | 147,370 | 99 | **652** | **751** | 7.59× |

**The alternative is PF-LIMIT.** 1,355 and 751 are PF-LIMIT's own exclusion counts, and **`0045` §1's table gives its DERIV split as `751 = 0 never-started + 652 Continued + 99 started-and-left`.** The 652 Red Team asked for **has been printed in the record since `0045`**, at the entry that kept PF-LIMIT.

**So the premise fails.** *"Not one of the four drops conjunct 2"* is false: **PF-LIMIT is the no-conjunct-2 rule.** It was adopted at `0041`/`0042` and superseded at `0046`/`0048`. The rule family was tested against exactly this alternative, before ALT-BROAD existed.

**And the pricing is what settles it.** Dropping conjunct 2 excludes **652 Continued pairs — pairs that satisfy `F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)`, on evidence they demonstrably produced.** Liveness exists to stop a null being trusted when the account may have been dead. **Continued is not a null.** Excluding a pair whose positive evidence is in hand is the one thing the rule cannot coherently do, and it is why `0046` moved off PF-LIMIT.

**What survives, and it is not nothing.** **The size of the outcome-conditioning is 652 on both populations** — 0.3315% of APPLY, 0.4424% of DERIV. That is now **measured rather than argued**, and it publishes with the limitation at Step 14 instead of standing as an unquantified concern. **The objection is answered in the direction that keeps the rule, and the number that answers it is one Red Team could have read.**

## 2. 2.5 — a width is a count over a denominator

`derive()` computed every width as `round(pct(ceil_n, n) − pct(floor_n, n), 6)` — **a difference of two 6-dp rounded percentages, which is precisely the construction `SUPERSEDED[0.4033]` names as *"a rounding artifact"*.** The register held the diagnosis and the generator committed the disease.

**It showed.** The **same 793 pairs** on the **same 196,654** produced, in one generated block:

| | was | now |
| :--- | ---: | ---: |
| `APPLY.sl.width` | 0.403246 | **0.403246** |
| `APPLY.cont.width` | **0.403247** | **0.403246** |

**One quantity, two values, an ulp apart** — the S&L bound and the Continued bound span the same excluded pairs, so their widths are the same number. **And `bb-b.json`'s corrected `0.403245 → 0.403246` at `0062` landed on the exact form by coincidence**, not by construction.

**Fixed:** `width = pct(ceil_n − floor_n, n)`, with two asserts — each width equals its own count over the denominator, and the S&L and Continued widths are equal. Regenerated; all four now exact.

## 3. Logged as outstanding, deliberately not fixed

**These are recorded and carried, not closed.** Every one is a defect in the *control apparatus or the record*, none changes a published figure, and each is stated here so approval is given with them in view rather than around them.

| # | Finding | Why it is carried |
| :-- | :--- | :--- |
| **2.1** | **`compare_halves()` cannot fail.** Both sides are `figure_table(arm)` serialized twice in one process from the same `D`. It does not compare the `.md` a reader sees: `md_block()` renders its tables from `D`/`C` and its ratios from `ratios()`, a separate expression. Statements are compared as **keys only, never text** | B9's shape one level up — a comparison whose two sides are the same object |
| **2.2** | **Four published sub-interval ratios are outside all 72 figures**, outside CANON, outside `_DERIVED.figures`, uncompared — and **arm a's is checked by nothing**, since `RATIO_LAYOUT["a"]` has no `"sub"` band | `0062` §3's "every derived figure" is false by four |
| **2.3** | **The `_DERIVED` block is write-only** — exempt from both negative halves and counted by both positive halves, so `ADOPTED_IN`'s md/json result is satisfiable by the generator's own appendix | The bodies do carry them; that is luck, not what the check established |
| **2.4** | **The covering qualifier is on eight surfaces in FIVE wordings**, and the `analytics-engineer` pair carries **the first clause only** while instructing that any table carrying the bound carries the qualifier | `0062` §4 conceded no control catches this and added none. The `REQUIRED_PHRASES` mirror of `WITHDRAWN_PHRASES` is the fix and is not built |
| **2.6** | **Both registers say `LEGITIMATE` disarms the control; the code never consults it in the negative loop.** `legit_unused` is computed and unused; `UNUSED` does not fail | Direction is toward strictness |
| **S1–S7** | `READ_FAILURES` discarded on the in-process path; **the regenerator never runs the phrase half** — the thing that wrote B8 into four files still does not check for withdrawn phrases after writing; surface 6 still suffix-filtered while 7 was fixed; `ABSENT_OK` unanchored and first-match-wins, so `"width_pp"` can excuse a `sampling_error` path with the wrong reason; `_crosschecked >= 1` permits the "claimed both, reached one" defect it criticises; **`bb-{a,b}.md:3`'s hand stamp is stale and names the glossary as canonical register** — B3's two-registers defect reinstated in prose, outside `BEGIN…END`, carrying no number and no phrase so no control sees it; the glossary trap table is structurally orphaned | S6 is the one I would fix first |
| **DF-3** | `specs/step7-deriv-floor-verification.md`'s **Background** still says `(τ1, τ2]` while `0057` adopted open, and inertness is **not** expected at `W = 213`, which is Step 13's grid | Instance B raised it; the spec is a completed task's brief, not a live instruction |

## 4. What the fifteen reviews actually found

**Reviews 1–8 contested the rule.** They produced the sign correction, the withdrawal of "no free parameter", the deletion of the numeric threshold, the four rule generations, the widened floor, and the `τ1` anchoring — **substantive findings that changed what is measured.**

**Reviews 9–15 found propagation and control defects in figures derived from an unchanged rule.** Not one of them changed the rule, the population, the exclusion counts, or any bound endpoint on its own arithmetic. **They changed where numbers were written, which numbers were checked, and whether a claim about a check was true.**

**That distinction is the case for approval and it is also the case for the caveats**: the analysis has been stable for eleven consecutive reviews, and the machinery around it has needed seven entries to catch up.

## 5. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **No figure changes** — `cont.width` moves `0.403247 → 0.403246`, which is a correction of an artifact, not a re-measurement.
- **Zero API calls**, including the 652.
- **Step 8 does not launch. The gate is not closed by this entry.**
