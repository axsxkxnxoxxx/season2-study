# Decision 0085 — Red Team B1, B2, P4 and the line-6 asymmetry are fixed; B3 is carried; two directed items had no referent

| | |
| :--- | :--- |
| **Decision** | **B1 fixed:** the spec now requires each arm to **name the universe its D9 clustering runs over**, and `0084` §5 item 3 is **re-filed as an ARM DIVERGENCE**, which is what it is. **B2 fixed:** the `p_at_bound` emptiness is emitted on **both populations at both positions, four cells each** — `CLAUDE.md`'s standing rule, not a new one. **P4 fixed:** the coextensivity chain has **three links, not two**, and `max(E2) = F2` is **not** construction. **The line-6 marginal decomposition (652 **and** 1,355) publishes in both arms.** **B3 is CARRIED — it needs a Human Lead ruling.** **Two directed items had no referent and were not propagated.** |
| **Recorded by** | Analytics Engineer, on Red Team's third-pass HOLD and the Human Lead's instruction to fix the blockers |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's **third** Step 8 gate review: **HOLD**, three blocking, four publishing |
| **Amends** | `0084` §5 item 3 (mis-filed as arm-against-spec); `0083` §2 (the construction chain, and its APPLY-only table); `0084`'s own JSON branch of the phrase control |
| **Verified by** | `check_surfaces.py` **PASS** with a **proximity probe** on the fixed JSON branch; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **11/11 CONFIRMED**; the `analytics-engineer` pair byte-identical apart from `name:` |
| **Status** | Open. **Step 8 is NOT approved. B3 blocks and is the Human Lead's.** |

---

## 1. Two directed items had no referent — checked before acting, not propagated

**This is the fifth occurrence** of the pattern recorded at `0078` §1 and `0082` §1, and the first since
the Human Lead identified its cause and asked that findings be reported with the figures they rest on
and where those figures live. **Both items were checked against the files; neither is propagated.**

**(a) *"The column count is 89, not 88, and `f2_in_A_H` is not a column. Correct `task-sheet.md` Step 8
and both `analytics-engineer` files."***

**Already correct, and corrected by `0083` §3, committed at `0af0d92` before the arms were launched.**

| file | line | reads |
| :--- | ---: | :--- |
| `task-sheet.md` | 332 | **89 NAMES, EXACTLY THESE** |
| `task-sheet.md` | 390 | *replaced by the **89-NAME ENUMERATION*** |
| `.claude/agents/analytics-engineer.md` | 280 | **89 NAMES, EXACTLY THESE** |
| `.claude/agents/analytics-engineer-b.md` | 280 | **89 NAMES, EXACTLY THESE** |

**`f2_in_A_H` is marked NOT AN EMITTED COLUMN at the point of use in all three.** **Both arms enumerate
89**, verified as **sets, off disk**, not by counting: `processed/step8/{a,b}/analysis_table.csv.gz`
headers are **set-equal at 89 names**, with `p_at_bound` and `silent_at_tau1` present and `f2_in_A_H`
absent. **Nothing to correct.**

**(b) *"Invariant 7's population is the post-liveness set, not the position-5 set — they differ by 703
rows, and its own coverage identity catches it."***

**Invariant 7 is not a row-set invariant.** In `task-sheet.md`'s own numbering it is **"No account
dropped wholesale"**, and **its population is ACCOUNTS** — stated at the point of use in the spec and in
both arms' deliverables:

> **7. No account dropped wholesale** — **both populations**: the 2,422 accounts in APPLY's …

The 703 is a **row** count, and 196,654 − 195,951 = 703 is the gap between the **row** sets. **Invariant
7 runs on neither.** Its population is already stated, so there is no point-of-use gap to close.

**And the change would disarm it.** Invariant 7 exists to compare **the accounts holding a position-5
pair against the accounts surviving liveness** — that comparison *is* the check. **Anchoring it to the
post-liveness set makes it compare a set with itself and it can no longer fail.** That is the *"invariant
that cannot fail on any data"* class this study has spent three entries labelling.

**Neither item corresponds to any of Red Team's three blockers**, which are D9 clustering universes,
arm A's missing DERIV cells, and two unasserted mandates.

## 2. B1 — the arms clustered different universes, and I filed it as the wrong kind of defect

| | largest loose clusters |
| :--- | :--- |
| **Arm A** | `secondchance` 8, `theisland` 7, `maigret` 6 |
| **Arm B** | `thetwilightzone` 10, `thetraitors` 7, `manhunt` 5 |

**Disjoint. No shared member, maxima 8 against 10** — while **every count around them reconciles**:
complementary pairs 0 / 75 / 76 on both, half (a) 0 and 6 on both, half (b) 0 and 27 on both. **So it is
not a counting difference. It is a difference in which set of shows is being clustered, and the spec
never said which.**

**Why it blocks rather than publishes:** the loose key publishes for exactly one reason — **it bounds how
wrong strict could be** — and **the cluster examples are the evidence for that warrant.** Two arms
producing different evidence for one warrant means **the warrant is not reproducible while the
deliverables read as though it is.**

***`0084` §5 item 3 filed this as arm-against-SPEC*** — a wording question about what *"largest cluster"*
ranks by, citing arm A's list against the spec's three names. **The same evidence is arm-against-arm,
which is the dual diff**, and the standing rule is that a divergence is reported as one. **It was
mis-filed partly because arm B's list happens to match the spec's names**, which makes the whole thing
read as an arm-A wording problem. **Re-filed.**

**The spec now requires the universe named at the point of use** — all sweep show IDs carrying a slug,
the 1,138 frame shows, or the D9 candidate pairs. **No universe is ruled here; the divergence is
reported, not reconciled.** **If both arms name the same universe and still differ, one has a bug and
that is the finding.**

## 3. B2 — an emptiness asserted in prose and not emitted, on the population the entry omitted

**`0083` §2 keeps the column on the ground that *"an emptiness asserted in prose and never emitted cannot
be checked."*** **On DERIV, in one arm, that ground was unmet.** Its
`p_at_bound_totals_and_coextensivity` block carries `APPLY_position_5` and `APPLY_position_7` **and
nothing else**, and **`1,056` appears zero times in that arm's waterfall JSON.**

**The spec now requires four cells on each of four populations** — APPLY position 5, APPLY post-liveness,
DERIV position 5, DERIV post-liveness. **This is `CLAUDE.md`'s standing rule** — *both populations,
always* — **not a new requirement**, which is why it lands as a point-of-use statement rather than a
ruling.

**`0083` §2's table was APPLY-only and that is the root of it.** The DERIV figures — **1,072 / 0 / 0 / 0**
at position 5 and **1,056 / 0 / 0 / 0** post-liveness — **are now stated in the spec**, so an isolated
instance no longer has to decide whether the rule reaches them.

## 4. P4 — "by construction" had a link that was not construction

The chain is `numerator = L2` ⟺ `m_H = max(E2)` ⟺ `m_H = F2`.

**The first link is construction**, given `L2 := |E2|`, which the spec fixes. **The second is not.**
`max(E2) = F2` holds only because **the finale is the highest-numbered listed episode** — and **where a
season lists an episode numbered above its finale, they separate.** That is the `s2_aired_lt_listed` case
**this step is told to count.**

**`0083` §2 isolated a different fact** — 0 S2 numbering gaps — and correctly said the coextensivity
survives without it, since a mid-season gap does not move `max(E2)`. **The premise actually doing the
work went unstated.** **It is measured, not assumed: 0 shows in frame**
(`shows_where_max_E2_differs_from_L2 = 0`, `s2_aired_lt_listed` 0 shows), **and the frame does not move
across Step 13's grid, so nothing reopens.**

***`0083` §2 named two causes for a future FALSE row. There are three.*** Corrected on all three spec
surfaces.

## 5. The line-6 marginal decomposition — one arm published half of it

**703 is not the marginal cost of the silence test.** The silence test alone excludes **1,355** on APPLY;
the `NOT Continued` conjunct **spares 652**; `1,355 − 652 = 703`. **One arm published 652 and not
1,355** — derivable, so **not a defect**, but **1,355 is the figure that makes line 6 readable as a
marginal cost**, and a reader holding only 652 cannot recover it without knowing to add. **Both arms now
publish both, on both populations, with the identity stated.**

## 6. The JSON branch of the phrase control — my own fix dropped proximity

**Red Team P3.** `0084`'s new JSON branch tested `STRUCK` against the **whole string value** while the
`.md` branch windows it. **So any paragraph-length note mentioning a withdrawal anywhere exempted every
registered phrase inside it.**

**This is `0084` §2's shape, committed in the fix for `0084` §2** — the branch was justified on
*wrapping* (*"normalising it is enough and there is no cross-line problem"*) and **silently widened
`STRUCK` in the same move.** A stated justification covering one property while the change alters
another.

**Fixed, and not merely recorded.** Red Team checked occupancy and found the gap **empty** — no
registered phrase occurs in any Step 8 artifact `.json`. **It is still fixed**, because *"empty today"*
is precisely how the JSON-string limit was recorded at `0060` **while a defect was sitting in it**, which
`0061` then had to correct. **A proximity probe now demonstrates the difference**: a marker nine lines
from the phrase is invisible to the windowed test and visible to the whole-value test.

## 7. B3 — CARRIED. It is the Human Lead's.

**Two Step 8 mandates carry no assertion:**

- **the half-open UTC-instant form** — *"`date(watched_at) <= T1` must not appear anywhere in the
  implementation"*
- **D11 as a global cutoff**, discarding records at or after `τ_pull` *"from EVERY computation"*

**Neither is among the eight.** `tau_pull` occurs **once** in one arm's invariants JSON, as a parameter,
in no assertion. **Both arms state compliance in prose, which is a self-report** — and converting
self-reports into checks is what the invariant set is for.

**Why Red Team ranks it above the existing code checks:** a violation of either **moves the headline**,
which no failure of invariant 3 or 4 could. And **D11 is the exact axis the arms differ on** — the 94/73
split — which `0083` closed by declaring three readings publishable rather than by pinning where D11
bears.

**Two ways to close it, and the choice is a ruling:** add the two assertions, **or** rule in writing that
these mandates are verified by inspection and say where the inspection is recorded. **Not decided here.
The arms are rerunning against §§2–5; B3 is not among them, and Red Team will raise it again.**

## 8. Scope

- **No rule change, no population change, no bound endpoint moves.** No figure on any `CLAUDE.md`
  dependency list is touched, so no list is run.
- **Surfaces reached:** 1 (`task-sheet.md`), 2–3 (both `analytics-engineer` files, identically), and the
  control in `src/`. **Surfaces 4–5 deliberately not** — the `data-scientist` pair names none of these
  objects. **Surface 6 not edited** — both arms rerun. **Surface 7 not edited** — the glossary carries
  none of the four.
- **Zero API calls.**
- **Both arms rerun. Step 8 goes to Red Team for a fourth pass with B3 declared open.**
