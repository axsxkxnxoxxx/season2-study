# Decision 0051 — V1 and V7 fixed, plus nine housekeeping items from `second-brain`'s catch-up

| | |
| :--- | :--- |
| **Decision** | **V1:** both `data-scientist` files ordered ALT's superseded 485→716 series at Step 13 — corrected. **V7:** the two-ceilings sum is **100.3071%**, not 100.66%, and the excess is **exactly 604/196,654** — corrected with the mechanism stated. **Nine housekeeping items** cleared, including **14 superseded Step 7 artifacts stamped**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `second-brain`'s catch-up through `0050`, findings V1–V11 |
| **Status** | Closed. **Step 7's gate is OPEN and no Red Team review has run since its fifth HOLD.** |

---

## 1. V1 — propagation failure #10, in the string `0050` had just fixed

**Both `data-scientist` files, line 122, Step 13:**

> report the liveness exclusion count per `W` arm on APPLY — **485 at `W = 38` to 716 at 213**

**That is ALT's superseded series.** **Line 68 of the same files** carried ALT-BROAD's correct one, and
`task-sheet.md` says in terms: *"ALT's 485 → 716 series is superseded and must not be ordered."*

**So the instruction the task sheet forbids was the one the definition file gave, for the same step.**
`0050` fixed this exact string in three places and missed the Step 13 occurrence in both files.

**Why nothing would have caught it: Step 13 is Chained and single-implementation — there is no diff —
and `CLAUDE.md` sends the agent to its definition file first.**

**Corrected** to `537 / 550 / 633 / 664 / 701 / 703 / 789 / 864` with the started-and-left component
`52 / 56 / 79 / 89 / 98 / 99 / 125 / 148` reported separately, and ALT's series named as superseded at
the point of use.

## 2. V7 — the Continued figure matched no population, and it was mine

`0050` §3 and `task-sheet.md` published: *"16.9704 + 10.0405 + **73.6537** = **100.66%**."*

**73.6537% is on no population.** Recomputed from the arms' own masks:

| On APPLY, n = 196,654 | Count | Share |
| :--- | ---: | ---: |
| Never-started ceiling | 33,373 | **16.9704%** |
| Started-and-left ceiling | 19,745 | **10.0405%** |
| **Continued** — no Continued pair is ever excluded | **144,140** | **73.2962%** |
| **Sum** | | **100.3071%** |

**The excess is 0.3071 pp, and it is exactly 604 / 196,654.** **That is the mechanism and it is what
gets stated** — the same 604 pairs counted once in each ceiling, alternative worst cases over one set
rather than simultaneous ones. **The claim survives; the number and the reason are both cleaner than
what was published.**

**How it happened, recorded rather than glossed: the figure was taken from Red Team's review and
propagated without checking its population** — the exact failure `0046` §0's standing rule exists to
prevent, **committed in the entry that routed that rule into Step 14.**

## 3. Nine housekeeping items

| | Item | Disposition |
| :-- | :--- | :--- |
| 1 | **No index row for `0050`** in `decisions/README.md` | Added |
| 2 | **The gate checklist quoted PF-LIMIT** — two rule generations stale | Rewritten to ALT-BROAD, with the four-rule sequence and the five HOLDs named, and **"no review has run since"** stated |
| 3–4 | **Items 30 and 31 unstruck** although `0036` closed both by name, and the percentile they turn on was **deleted** | Both struck, with item 31's own observation — *no percentile fixes a shape problem* — recorded as what led to the deletion |
| 5 | **Item 46 said "five times"**; the count is **ten**, and it omitted `0049` §6's launch-snapshot control | Count corrected; **all four standing controls listed** |
| 6 | **Step 14's bias 2 half-fixed** — the withdrawn 0.032 pp figure live at one line while another said it must not be restated, plus PF-LIMIT as *"the approved rule"*, "seven in seven of the 751" and Option C | Residue rewritten on ALT-BROAD; the superseded text named so it is not restated |
| 7 | **`0034` line 35 still said "`τ2` plays no part in the liveness test"** — withdrawn from the task sheet by `0049` but never marked in **the gate document that originated it** | Amended in place. **Under ALT-BROAD `τ2` does play a part** — the second conjunct is the Continued test. **What `0034` actually fixed, and what stands, is that the SILENCE test is `τ1`-anchored** |
| 8 | **Twenty Step 7 deliverables across eight generations**, only the `bb` pair current; `step7-liveness-alt-a.md` carried *"the exclusion set is empty on DERIV at every arm"* — **the claim `0049` called false in five files — live and unmarked in a public artifact** | **14 superseded markdown artifacts stamped** with a header naming the current rule, the current deliverables, and every superseded figure class by name |
| 9 | **`632` is both a deleted threshold and the legitimate frozen-D10 never-started component at `W = 125`** | Recorded. **A blind grep for deleted thresholds produces false positives here**; the 632 at `W = 125` is correct and must not be struck |

## 4. What this does not fix

**`second-brain` raised eleven findings and this entry disposes of V1, V7 and the housekeeping.** The
remainder are recorded in its memory with their two conflicting sources named, and it deliberately
proposed no dispositions.

**Step 7's gate is OPEN.** Red Team's fifth review returned **HOLD** on propagation failure #9, that
was actioned by `0050`, and **no review has run since** — a fact the gate checklist now states rather
than leaving to inference.

## 5. Scope

- **No rule, population, bound or result changes.** One superseded instruction, one wrong figure, and
  nine record defects.
- **Zero API calls.** V7 was recomputed from the arms' stored masks.
