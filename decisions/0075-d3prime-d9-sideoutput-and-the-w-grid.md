# Decision 0075 — D3′'s cleared shares, D9 half (b)'s side output, and the `W` arm grid

| | |
| :--- | :--- |
| **Decision** | **D3′'s cleared-share series is 99.53% → 97.73%** on Step 8's right-censored populations, with the population **stated at the point of use**. **Position 3's drop set is retained as a side output**, because D9 half (b) is measured on the rows it removes. **The `W` arm grid is 38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 — written down for the first time.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 dual run's three unruled items |
| **Status** | Closed. **Neither Step 8 proposal is adopted.** |

---

## 1. D3′ — the level moves, the finding does not

**`0034` published 95.98% at `W = 46` falling to 91.34% at `W = 213`.** It measured that on **the
amendment's uncensored estimation sample**, and **it carried no population at the point of use.**

**On Step 8's right-censored populations the series is 99.53% → 97.73% (APPLY)** — measured
**independently and identically by both Step 8 instances**, which is the strongest form this study's
evidence takes.

**The direction and the shrinkage stand; the level does not.** **`0068` §2a could fix the denominator
and not the level**, which is precisely why this needed a ruling rather than a restatement: a
denominator is recoverable from the record, a level measured on a different population is not.

**The population is now stated wherever the series appears**, so the gap that produced this cannot
reopen.

## 2. D9 half (b) — an input the spec never said to keep

**Half (b) is measured on the rows position 3 REMOVES**, so **it cannot be computed without them**, and
**no line of Step 8 said to retain them.** **Instance A found this by needing it.**

**The failure mode is what makes it worth a ruling:** an instance that does not discover it **emits zero
or fails — and a zero here reads as a DATA FINDING rather than a MISSING INPUT.** A silently-zero
split-artifact count would be published as evidence that the artefact does not occur.

**Position 3's drop set is retained as a side output.**

## 3. The `W` arm grid — it had never existed in any file

**38 / 46 / 77 / 91 / 107 / 108 / 150 / 213 days.** **This entry and `task-sheet.md` Step 13 are the
first statement of it anywhere.**

**How it went unstated for so long:** Step 6's deliverables say **`[37, 107]`** and **`[37.70,
107.71]`**, and **neither says 38.** Step 13's bullets *constrain* the arms — vary above and below 108,
span 46 to 107, add 150 and 213 — **without enumerating them.** And the grid has travelled only as the
**index of a reported series**: *"537 / 550 / … at `W` = 38 / 46 / …"*. **An index is a reading. It is
not a specification.**

**Instance A chose the grid and named the choice, which means the next instance may choose
differently.**

**Why this is the most serious of the three.** **Every Step 13 figure is indexed by the arm set.** Two
instances on different grids produce **tables that cannot be diffed at all** — not tables that disagree
on a number, but tables with no shared index. **That is a failure of the dual implementation itself
rather than a wrong number inside it**, and the diff would report it as total divergence with no way to
localise the cause.

## 4. Which surfaces each reached, and which it deliberately did not

| Ruling | Reached | Deliberately not |
| :--- | :--- | :--- |
| **1. D3′ 99.53% → 97.73%** | `task-sheet.md` Step 8; **both `data-scientist` files**; **both `analytics-engineer` files**; **`decisions/0034`, amended in place**; **`artifacts/step1-outcome-definition.md` and `artifacts/step1-amendment-continued-boundary.md`, MARKED not rewritten** — approved gate deliverables whose figures were correct for the sample they used; `second-brain`'s glossary | **the Step 8 arms' own artifacts and `src/`** — both instances already flagged the discrepancy correctly; their text is the record of the run that found it |
| **2. D9 half (b) side output** | `task-sheet.md` Step 8; **both `analytics-engineer` files** | **the `data-scientist` pair** — D9 is a Step 8 output. Step 9 consumes it and does not compute it (`0071`) |
| **3. The `W` grid** | `task-sheet.md` Step 13; **both `data-scientist` files** (Step 13 is theirs); **both `analytics-engineer` files** (Step 8 reports per-arm counts); `second-brain`'s glossary | **Step 6's deliverables** — `[37, 107]` and `[37.70, 107.71]` were correct for what Step 6 derived, which is a value, not a grid. **The grid is a Step 13 choice and belongs where Step 13 is specified** |

**Both pairs verified byte-identical apart from `name:`. All eight surfaces PASS.**

## 5. Scope

- **One published level moves** — D3′'s cleared shares, a diagnostic. **No headline figure, no bound
  endpoint, no exclusion count changes.**
- **Two inputs are now specified that were being inferred**: a retained drop set and an arm grid.
- **Zero API calls. Neither Step 8 proposal is adopted; the gate is the Human Lead's.**
