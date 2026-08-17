# Decision 0100 — the five items `0099` §4 carried are closed

| | |
| :--- | :--- |
| **Decision** | **All five items carried at `0099` §4 are closed.** **The needle count is a LIVE MEASUREMENT, not a fixed figure** — the three "conflicting" numbers were never in conflict. **The canonical Red Team sequence is fixed here** and intermediate citations are flagged rather than rewritten. **The two ground-withdrawals `second-brain` listed as candidates are added to the single register.** **The Mode H / Mode I collision was in the BRIEFING, not in `second-brain`'s register** — its definitions stand. **R1–R9 are dispositioned.** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-17 |
| **Occasioned by** | `0099` §4, which carried five items for the Human Lead |
| **Verified by** | `check_surfaces.py` |
| **Status** | Closed. **Step 8 remains APPROVED (`0098`).** |

---

## 1. The needle count — a live measurement quoted as a constant

**`0095` §3 says 441. `0096` §3 and gate residual 8 say 439. The scan reads 442 today.**

***None of these is wrong and they were never in conflict.*** The scan counts candidate hits **across
every file on all eight surfaces**, so **it moves whenever the repository moves** — 441, then 439 after
one arm removed two of its own, then 442 as the record itself grew.

***The defect is quoting a live scan as though it were a constant***, and it is **`0096` §1's own lesson
one level in**: a measurement published as though it were permanent. **Corrected at all three points of
use, with the instruction to read the count from the scan and never from an entry.**

## 2. The canonical Red Team sequence for Step 8

***This is the authoritative list. Where an intermediate citation in `decisions/` or `artifacts/`
disagrees, THIS governs*** — and `second-brain` is right that **the review sequence IS a Step 18
artifact**, which is why it is fixed rather than left to be reconstructed.

| # | verdict | what it turned on |
| ---: | :--- | :--- |
| 1–2 | HOLD | the spec as read back; the required counts |
| 3 | HOLD | B1 D9 cluster universes · B2 arm a's missing DERIV cells · B3 the two unasserted mandates |
| 4 | HOLD | the surface-numbering inversion; D9's coverage counts unreconciled |
| 5 | HOLD | F1 the outcome-state count · F2 the independence proxy · F3 the needle register's scope |
| 6 | HOLD | the `+1` perturbation; the `0068` misattribution; the line-6 warrant |
| 7 | HOLD | N1 `p_at_bound`'s two FALSE classes · N2 the D2 168 · N3 the per-site D11 table · N4 the superseded count |
| 8 | HOLD | the fabricated cross-arm divergence; line 434's registered needle |
| 9 | HOLD | F1 the relay · F3/F4/F5 the shared controls |
| 10 | HOLD | ***the plateau diagnosis and the generator*** |
| 11 | **PROCEED** | *"The analysis table is right."* |

**Known off-by-one citations, flagged in place rather than rewritten** (`0058` §6's method): `0095`'s
*"still open from Red Team's fifth pass"*, and the `0091` §2 / arm-report disagreement over whether the
`+1`-perturbation finding was the sixth pass's F3 or the seventh's finding 3. **`0091` is right: it was
the sixth.** **Rewriting the citations would put unsourced numbers into entries their authors signed;
flagging them leaves the trail visible.**

## 3. The two ground-withdrawals, added to the single register

**`second-brain` listed them as candidates and declined to add them itself** — *"extending my human half
past the source would be the two-registers defect committed by me."* **That was the right call, and the
right place is `src/step7_register.py`, which is where they now are.**

- **`0091` §1** — *"line 6 does not move BECAUSE the silence test reads an insertion clock."*
  **Structurally wrong**: conjunct 2 is `NOT Continued`, an episode-timestamp computation that **moves
  on 55 APPLY and 45 DERIV rows** under the same counterfactual. **The counts are correct and the
  invariance is real; the REASON was not.** Still true: 703, 99, 55, 45.
- **`0089` §2(a)** — *"exactly 1 episode at `τ1`, SO `0068`'s strictness ruling moves a real row."*
  **Wrong object**: `0068` is about **insertion instants**; the 1 is a distinct S2 episode by canonical
  `watched_at`. **The ruling's own quantity is 0 on both populations, both arms** — vacuous.
  **A true count of the wrong thing.** Still true: 1.

**`GROUNDS_WITHDRAWN` now holds five.**

## 4. The Mode H / Mode I collision was in the briefing

***`second-brain`'s register is correct and was never the problem.*** It has defined **Mode H** since
2026-08-13 as **an asserted action never taken**. **The briefing I gave it used "Mode H" for the
ground-withdrawal class**, which is **Mode I**.

**So there is nothing to renumber**, and renumbering would have been the damaging move — **H's ten
instances are cited by letter elsewhere.** **`second-brain` declined to renumber and was right twice
over**: right that it was not its call, and right that the register did not need changing.

**Canonical, so the misuse does not recur: H = an asserted action never taken. I = a withdrawn GROUND
built from correct statistics.**

## 5. R1–R9, dispositioned

| | disposition |
| :--- | :--- |
| **R1** glossary forbade two figures the spec mandates | **CLOSED** — corrected, and the repair verified row by row at `0099` |
| **R2** Red Team pass numbering | **CLOSED by §2** — canonical sequence fixed, citations flagged in place |
| **R3** Step 8 trap figures live in one hand-maintained place | **OPEN, and it is the real one.** `second-brain`'s memory is the only home for `168`/`153`, `75`, `46,428`, `726,102`, `71`, `20` and the second readings of `703`/`604`. **The two-registers hazard `0059` B3 forbids.** **Closing it means a numeric Step 8 register in `src/step7_register.py`** — not done here, and named as the largest open item |
| **R4** a line-local control passing off an incidental word | **OPEN**, minor; the control is arm b's and the line is legitimate |
| **R5** `0093` listed `153` among D9's numbers | **CLOSED** — corrected at `0099`'s commit |
| **R6** a published artifact's resolver coverage one entry short | **CLOSED BY REMOVAL**, and recorded as such — the key is gone from `artifacts/` under `0096` §1. **Residual 2 working as designed, not the count becoming right** |
| **R7** the Mode H letter | **CLOSED by §4** — the collision was in the briefing |
| **R8** the two items carried at the gate | **CLOSED** — both published as gate residuals 7 and 8 |
| **R9** `0091` §1's residual answered by one arm only | **OPEN**, published as part of gate residual 4 |

**Three remain open — R3, R4, R9 — and all three publish with the gate rather than block anything.**

## 6. Scope

- **No population change, no figure moves, no rule change. Step 8's approval is untouched.**
- **Surfaces reached: 6** (the gate record's residual 8) and `src/`. **`decisions/` corrected at three
  points of use.** **Neither arm ran.**
- **Zero API calls.**
