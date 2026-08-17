# Decision 0094 — `0089` §2(b) reaches the spec; two withdrawn claims registered; the missing-entry defect recurs

| | |
| :--- | :--- |
| **Decision** | **No new ruling.** `0089` §2(b)'s correction is propagated to surfaces 1, 4 and 5 — **it had reached `decisions/` only, which is why arm b republished the superseded axis.** Two claims withdrawn on the 2026-08-16 runs are registered. A gap the registration exposed is closed: **the phrase half could not see a withdrawal marked by its JSON KEY.** ***AND THIS ENTRY WAS ITSELF MISSING FOR A DAY*** — cited 8 times with no file, **the second occurrence in three entries**, after `0092` §2 recorded the first and observed that no control can see it. **A control is added.** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's eighth pass F1, traced to its root by instance B; instance A's register recommendation; and the recurrence, found while auditing citations before a `second-brain` catch-up |
| **Amends** | `0088` §2's axis, on the spec surfaces; `src/check_surfaces.py`'s JSON branch |
| **Verified by** | `check_surfaces.py` **exit 0, PASS all halves, all EIGHT surfaces**; `step7_regenerate_derived.py` **VERIFIED**; `step7_floor_extremes.py` **11/11** |
| **Status** | Closed for its own content. **Step 8 is NOT approved.** |

---

## 1. F1's root was a propagation failure, not an arm defect

**`0089` §2(b) corrected `0088` §2's axis for `747,478` two entries ago — in `decisions/` only.** The
superseded characterisation stayed **live and unmarked** at `task-sheet.md:654` and `:707` and in **both
`analytics-engineer` files at `:249`** — the files the isolated instances read.

**Arm b read `analytics-engineer-b.md:274` and faithfully republished it.** ***That is `0093` in reverse:
the ruling reached `decisions/` and not the spec, and the arm did what the spec told it.*** **Red Team
scored it against arm b; it belongs to the propagation.**

**Propagated now, with the relation that does hold stated at the point of use:** `747,478` is **distinct
`(user, show)` pairs**; less the **21,376** S3-only component that is **726,102**, against arm b's
**726,103** — the one-pair divergence both arms already report, **unreconciled.**

## 2. Two withdrawn claims registered, on instance A's recommendation

- **`"reached surface 1 and no other"`** — arm a's hardcoded propagation reading, published beside live
  counts that a rerun could contradict, and did.
- **`"can still be a different set of rows"`** — arm a's symmetric-difference-0 warrant. ***This one is
  `CLAUDE.md`'s THIRD BLINDNESS CLASS*** — a withdrawn **argument built from correct statistics** — so it
  goes to `GROUNDS_WITHDRAWN` **with the statistics named as still true and no longer load-bearing**:
  symmetric difference 0, and the 55 APPLY / 45 DERIV rows on which conjunct 2 moves.

## 3. A gap the registration exposed, and the marker sweep it triggered

**The phrase half's JSON branch tested `STRUCK` against the VALUE only**, so a withdrawal marked by its
**JSON key** — a field named `WITHDRAWN_SENTENCE` — was invisible. **The key IS the point-of-use marker
`CLAUDE.md` requires**; the branch now reads the path. The `.md` branch has no analogue, because a line
has no key.

**Arm a's sweep then found five more of the same shape**, all marked in the **emitter**, none
hand-edited, and **two were passing only by accident**:

| | |
| :--- | :--- |
| `0092`'s own withdrawn premise, quoted twice | one copy passed **only off the words *"was false"* in the NEXT item** |
| `0074` r5's framing, superseded by `0090` | the line said **"SUPERSEDES"** — which **neither `MARK` nor `STRUCK` matches**, both being `superseded\|superseding`. A near-miss in the marker vocabulary |
| `0088` §2's axis (§1 above) | |
| the `p_at_bound` table's two quotes of `0082`'s superseded definition | |
| `step8_a_lib.py`'s `WHAT_MOVED`, landing in 5 JSON strings and 6 `processed/` files | passed **only because an unrelated `WITHDRAWN` sat ~2,000 characters later in the same blob** — a whole-value `STRUCK` check is **proximity-blind on long values**, the same defect fixed in the JSON branch and not fixed for large single strings |

**Arm a correctly declined to mark quotes of CURRENTLY ADOPTED spec text**, which would have been the
over-correction.

**Nothing measured moved:** leaf-by-leaf JSON diff over **2,747 and 782 leaves, identical key sets, 0
numeric and 0 boolean diffs.**

## 4. The missing-entry defect recurred, and now has a control

***`0092` §2 recorded that its own entry did not exist. This entry did not exist either*** — **cited 8
times across `task-sheet.md`, the agent files and both arms' artifacts, with no file in `decisions/`.**
**Second occurrence in three entries.**

**`0092` §2 named the reason no control saw it:** *"`check_surfaces.py` checks the eight surfaces for
wrong and withdrawn content; it does not check that a cited entry exists."* **A gap recorded and left
open is a gap that recurs** — which is `0060` §6's lesson, and this is its second demonstration.

**The control is now built.** `check_surfaces.py` extracts every four-digit decision citation from all
eight surfaces, resolves it against `decisions/`, **prints its coverage count**, and **fails on any
citation with no file.** **It fails if it finds zero citations**, because a resolver that resolves
nothing must not report clean.

## 5. Scope

- **No population change, no figure moves, no rule change.**
- **Surfaces reached: 1, 4–5** (§1's propagation, verified byte-identical apart from `name:`), and
  **6, 8 for arm a** by its rerun. **Arm b's 6 and 8 carry §1's correction from its own earlier run.**
- **Zero API calls.**
