# Decision 0101 — R3 closed: the Step 8 trap figures move into the single register

| | |
| :--- | :--- |
| **Decision** | **The Step 8 numeric trap figures are now in `src/step7_register.py` as `STEP8_LEGITIMATE`, 14 rows.** They lived **only in `second-brain`'s memory** — a **second hand-maintained register**, which is the hazard `0059` B3 forbids. **TRANSFERRED, NOT AUTHORED**: every reading is `second-brain`'s, carried across with its scope and its file citation. **Wired as a live control that FAILS on a DEAD ROW**, and adversarially probed. |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-18 |
| **Occasioned by** | The Human Lead: *"Close R3. Two registers is the hazard `0059` B3 forbids."* |
| **Verified by** | `check_surfaces.py` **exit 0**; the dead-row control **probed by injection** |
| **Status** | Closed. **Step 8 remains APPROVED (`0098`).** |

---

## 1. Why two registers is the hazard, in this file's own words

`src/step7_register.py`'s header, from `0059` B3:

> *"There were TWO hand-maintained registers — one in the regenerator, one in the checker — already
> divergent by one entry after a single entry's use, and **NEITHER contained the values that were
> actually wrong.** Two registers is one register plus a defect waiting."*

**The Step 8 trap figures reproduced exactly that shape.** `168`/`153`, `75`/`76`, `46,428`/`46,366`,
`726,102`/`726,103`, `71`/`59`, `20`/`17`, and the second readings of `703` and `604` **existed in one
place, and that place was `second-brain`'s memory** — **surface 7, which is fed back into rulings, and
which has itself carried stale figures before.**

## 2. Transferred, not authored — and that distinction is the whole job

***Every reading below is `second-brain`'s, carried across with its scope and its file citation.***
**Re-deriving them here would have created the THIRD register rather than closing the second.**

**The two dangerous rows are the coincidences**, and both arms flag them themselves:

- **`703` — two readings, both current, unrelated quantities that happen to be equal.** (i) ALT-BROAD's
  APPLY liveness exclusion count, 604 + 99 from 216 accounts. (ii) **distinct S2 episodes in the
  separating interval `[τ1, τ1+24h)` on APPLY position 5**, both arms, sitting beside `[τ2, τ2+24h)` =
  303 and the DERIV pair 595 / 261. **The defect is quoting either as the other.**
- **`604` — two readings, both current.** (i) the never-started **component** of 703 on APPLY, 191
  accounts. (ii) **invariant 8's scope note**: the 7 accounts skipped on one attempt but yielding data on
  another hold **604 position-5 pairs**, 119 never-started. **The defect is `604` as a liveness exclusion
  TOTAL — that is ALT's superseded answer, and producing it at position 6 IS a divergence.**

**Every row carries BOTH halves — the reading that makes the figure correct AND the use that makes it a
defect — and an assertion at import enforces it.** **A row with an empty defect column is a blanket
exemption**, which is the shape `second-brain` found on `703` and repaired, and it is how `9.6830` was
registered as legitimate while superseded on four surfaces.

## 3. What the control can and cannot do, stated rather than implied

***It cannot adjudicate whether a given occurrence names its scope.*** That is prose, and it is
`CLAUDE.md`'s **third blindness class**, which has no control and is recognised by what a claim *means*.
**Claiming otherwise would be the "control asserted to exist" defect this study has hit repeatedly.**

***What it CAN do is prove the register is LIVE, and catch the one failure a trap register has of its
own: A ROW THAT MATCHES NOTHING.***

**Why a dead row must fail.** **Registering a value as legitimate DISARMS the control against it.** A row
for a figure that no longer appears anywhere **cannot protect a real reading** — it can only sit there
**waiting to excuse a future coincidence**. **Dead rows are how a register decays into a blanket
exemption.**

**Measured: 14 registered figures × 256 files, 17 to 467 occurrences each, no dead rows.**

**Probed by injection, not asserted**: a row that can match nothing **fires, names itself, and exits 1**;
the register was restored byte-identical afterwards. **So "no dead rows" is a clean result, not an empty
one** — the distinction `0084` got wrong and this chain has since had to keep re-earning.

## 4. Scope

- **No population change, no figure moves, no rule change. Step 8's approval is untouched.**
- **`second-brain`'s glossary keeps its rows.** **It is no longer the only home**, which is what R3 asked
  for; **the source of record is now `src/step7_register.py`**, and a divergence between them is now
  visible rather than invisible.
- **Surfaces reached:** `src/`. **Neither arm ran.**
- **Zero API calls.**
- **R3 is CLOSED. R4 and R9 remain open and publish with the gate.**
