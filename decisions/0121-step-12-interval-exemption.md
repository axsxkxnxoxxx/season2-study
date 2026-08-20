# Decision 0121 — Step 12's interval exemption, and the carve-out the writers must read

| | |
| :--- | :--- |
| **Decision** | ***STEP 12 IS EXEMPT from the paired-movement interval requirement.*** **A Step 12 file that carries no interval DECLARES that emptiness rather than failing to fill it.** ***THE EXEMPTION IS FROM PRODUCING INTERVALS, NOT FROM PRODUCING THEM COMPLETELY:*** a Step 12 file that HAS published intervals owes both objects like any other. |
| **Decided by** | **Human Lead**, 2026-08-19, ruling relayed at `0120` §1 |
| **Date** | 2026-08-20 |
| **Amends** | `0118` as applied to Step 12; `data-scientist{,-b}.md:259` — **see §3, the carve-out** |
| **Status** | **FILED 2026-08-20 and PROPAGATED.** `0120` implemented this in `artifacts/`; ***this entry is the FIRST time it reaches a spec surface*** — see §5 |

---

## 1. The ruling

**Step 12 is exempt.** `S41`'s empty branch is **scope-aware**: a Step 12 file with no arm-knowable interval reports `EMPTY_DECLARED` with its restriction named and its coverage counted, rather than failing.

## 2. The ground, which is the schema's own warrant

`artifacts/step8b-output-schema.json:2075`, written before the ruling and by a different hand:

> *"a CI is still legitimately absent where the spec does not ask the writing step for one — **Step 12
> lists every candidate cut and mandates intervals nowhere**, and Step 13's per-arm sensitivity series
> is a series of shares, not of intervals."*

**The Human Lead's reasoning, recorded as given:**

> Requiring Step 12 to carry intervals would force it to **manufacture two figures it was never asked
> to compute**, one a paired movement between configurations the spec does not name — **a fabrication
> to satisfy a control.** And it would make **the schema's own warrant text false**, which is
> **fixing a control by breaking a statement of fact.**

***Both halves matter.*** The first is why the writer must not be compelled. The second is why the
**check** was corrected rather than the **warrant**: a control and a statement of fact disagreed, and
**the statement of fact was the one that was true.**

## 3. ***THE CARVE-OUT, AND THE WRITERS MUST READ IT***

`.claude/agents/data-scientist.md:259` and `-b.md:259`, inside the canonical `BOOTSTRAP-STATISTIC`
block, tell every writer:

> **"Every interval declares its `statistic` at the point of use, and both statistics appear.** A run
> that emits only one is **incomplete**, not merely differently designed."

***THAT SENTENCE HAS AN EXCEPTION AND CURRENTLY STATES NONE.*** **A Step 12 writer reading only its
own surfaces will manufacture the two figures this ruling exists to spare it** — which is the
fabrication the ruling's own ground forbids. **`reviewer-engineering` found this on the v1.9.0 pass.**

**The carve-out, in the words that must reach both writer files:**

> ***"A run that emits only one is incomplete" applies to a step the spec ASKS for intervals.***
> **Step 12 is asked for none** — it lists every candidate cut and mandates intervals nowhere
> (`0121`). **A Step 12 file that carries no interval DECLARES that emptiness and is complete.**
> ***But the exemption is from PRODUCING intervals, not from producing them COMPLETELY: if a Step 12
> file publishes any interval, it owes BOTH objects like any other file*** — a step that has already
> computed them is manufacturing nothing.

**The block is byte-identical across the two files and `scan_statistic_declaration()` fails if they
diverge, so the carve-out lands in both or in neither.**

## 4. What the exemption does NOT cover, demonstrated rather than asserted

**It is Step 12's alone.** On identical fixtures: **step9 FAIL, step10 FAIL, step11 FAIL, step12
`EMPTY_DECLARED`, step13 FAIL.** The expectation lives in `S41_EXEMPT_BY_RULING = {"step12"}`,
**written from this ruling**, and widening the validator's own table drives the selftest to exit 1
with `tables_agree: false`.

***That guard exists because the first fixture did not have it:*** it derived `must_fail` from the
table under test, so **adding a step to that table moved the expectation along with the behaviour and
the selftest still passed.** The arm found and reported that against itself. **It is the same class
now carried as `0122` §6's E2 — the third occurrence.**

**And it does not cover a Step 12 file that HAS intervals.** `s41_exempt` originally gated the
per-owner missing-object branch too, so a Step 12 file publishing forty **levels-only** intervals
passed with a note. **Narrowed to the empty branch alone**, on this ruling's own ground.

## 5. ***PROPAGATION — done on filing, 2026-08-20***

~~**`0120` implemented it in `artifacts/` and in the controls. Surfaces 1–5 carry nothing about it**~~
***TRUE UNTIL THIS ENTRY WAS FILED; NO LONGER.*** **`0120` implemented it in `artifacts/` and in the
controls, and for two days it existed on NO spec surface.** ***Filing propagated it.***

**The producing arm declined to propagate it, and was right to.** Its only source was its launch
instruction, and ***a launch instruction is not a citable source*** — `0120` §6. **The entry is the
citable source, which is why it exists.**

**REACHED:** **1** `task-sheet.md` (Step 12 section, 1 site); **2–3** both `data-scientist` files
(§3's carve-out **inside** the canonical block, so byte-identity covers it — 1 site each, `diff` to
the `name:` line alone); **4–5** both `analytics-engineer` files (1 site each, identical); **7**
`second-brain/open-items-and-contradictions.md` (1 site). **6** `artifacts/` already carries the
mechanism at v1.9.0. **8** `processed/` — **not applicable, 0 occurrences, verified.**

***`artifacts/` does NOT carry the carve-out and should not*** — it is a writer instruction, not a
schema field.
