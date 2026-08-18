# Decision 0103 — the bootstrap is fixed; Step 13 is dual

| | |
| :--- | :--- |
| **Decision** | **BOOTSTRAP: 10,000 resamples, resampled at the ACCOUNT level, fixed seed `20260818` stated in the spec. Every interval records its seed, resample count and RESAMPLING UNIT at the point of use**, so an unfixed spec is visible in the output rather than silent. **This unblocks Step 9**, which could not write anything at all. **STEP 13 IS DUAL**, resolving a live `CLAUDE.md` / `task-sheet.md` conflict in favour of dual. |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s Step 8b review, F3 and F5 — and `0056`, which left the bootstrap open and named it as blocking Step 9 |
| **Amends** | `CLAUDE.md` `## Dual implementation`; `0056`'s open bootstrap |
| **Status** | Closed. **Step 8b reruns against F1–F9 and returns to `reviewer-engineering`.** |

---

## 1. The bootstrap, and why the unit is the load-bearing part

**10,000 resamples. Account-level. Seed `20260818`.** **Every interval records all three at the point of
use.**

**Account level because pairs are not independent — one account contributes many — and pair-level
resampling understates the interval.** **This build has measured that**: Step 7's threshold interval is
**account-clustered [528, 787]** against an **i.i.d. [632, 645]** which `0039` records as
*"overstat[ing] precision by roughly twentyfold."*

***The fixed seed is what makes the two arms comparable.*** Without it **a difference between them could
be sampling noise rather than a divergence** — and **this study's entire dual control rests on that
distinction.** **The seed VALUE is arbitrary and its FIXITY is the point**; `20260818` is set so the spec
states one, and it may be changed freely but never left unstated.

## 2. One caution recorded with the ruling, and it is not a disagreement

***THE BINDING CLUSTER IS NOT THE SAME FOR EVERY QUANTITY.***

**The ruling cited two clustering measurements. One supports account-level and one does not**, and both
are on the record:

| quantity | binding cluster | measured |
| :--- | :--- | :--- |
| **Step 7's threshold** | **account** | account-clustered **[528, 787]** vs i.i.d. **[632, 645]**, ~20× (`0039`) |
| **`W`** | ***SHOW*** | 25,120 C1 pairs from **206 shows**; i.i.d. **±8 d**, show-clustered **[89, 125]** = **±18 d** (`0024`, `0026`) |

***`task-sheet.md` names the SHOW as the binding cluster for `W`, in terms.*** **So account-level is
right for the outcome shares — whose clustering is by account — and would UNDERSTATE a show-bound
quantity.**

***And the ruling's own mechanism is what makes this detectable:*** the mandated **`resampling_unit` per
interval** means a show-bound quantity **must say `show` rather than inherit `account` silently.**
**Report a material disagreement between the two units; do not reconcile it.**

*(For the record, the ruling's "±18 rather than 13" reads **±8** in the source — `task-sheet.md:1073`.
The direction and the magnitude of the point are unaffected.)*

## 3. Step 13 is dual

**`CLAUDE.md`'s dual list named Steps 6, 7, 8 and 9. `task-sheet.md` argued the `W` grid must be fixed
because *"two instances on different grids produce tables that CANNOT BE DIFFED AT ALL"* — which
presupposes a duality the list did not grant.** **A live spec conflict, found by
`reviewer-engineering` and reported rather than charged to the schema's author.**

***Resolved in favour of dual.*** Step 13 varies **`W` across eight arms and the completion rule
alongside**, which makes it **the most spec-heavy step remaining** — and **every divergence in this build
has come from an unstated convention in a spec rather than from a coding error.**

**Consequence for the schema: Step 13's payload nests per producing arm exactly as Step 9's does**, which
also disposes of `reviewer-engineering`'s F5 for that step.

## 4. Scope

- **No population change, no figure moves. Step 8's approval is untouched.**
- **Surfaces reached:** `CLAUDE.md`, **1** (`task-sheet.md`), **2–3** (the `data-scientist` pair,
  identically — they compute the intervals). **4–5 not applicable**: the analytics-engineer pair
  computes no CI.
- **`632` and `1,293` appear nowhere in either Step 8b artifact** — verified. **The deleted threshold is
  not reintroduced by fixing the bootstrap.**
- **Zero API calls.**
