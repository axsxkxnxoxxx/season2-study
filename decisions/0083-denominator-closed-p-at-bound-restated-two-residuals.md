# Decision 0083 — the set-membership denominator is CLOSED; `p_at_bound` marks WHETHER, not WHY; two residuals fixed

| | |
| :--- | :--- |
| **Decision** | **The 94-record denominator difference is CLOSED, not a Step 14 limitation.** It was never a divergence: the two published figures are two points on a **one-parameter family indexed by where D11 applies**, the parameter is `0068`'s own open item, and **every member of the family drops zero records.** All three readings publish with their pipelines named. **`p_at_bound` marks WHETHER `p` reached its bound, not WHY** — `0082` §2's two clauses are **coextensive by construction**, so the FALSE class is empty and the motive sentence is **WITHDRAWN**. **Two residuals fixed**: the stale `88` inside a strike-through, and `0077`'s adopted-name table still listing `f2_in_A_H` as adopted. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-16 |
| **Occasioned by** | The clean dual run of 2026-08-16, in which **both arms independently** decomposed the denominator and **both arms independently** measured the two `p_at_bound` classes as the same set; and residual 8 of `artifacts/step8-waterfall-a.md`, reported by instance A and not editable by it |
| **Amends** | `0074` §4 (routed the denominator to Step 14); `0082` §2 (its definition's FALSE clause and its motive sentence) |
| **Verified by** | `check_surfaces.py` **PASS — all halves, all EIGHT surfaces**; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **11/11 CONFIRMED** |
| **Status** | Closed. **Step 8 is the remaining gate and it is NOT approved.** |


> **SURFACE NUMBERING CORRECTED 2026-08-16 (`0087`).** This entry numbered the
> `analytics-engineer` pair **2–3** and the `data-scientist` pair **4–5**. `CLAUDE.md` numbers them
> the other way: **2–3 is the `data-scientist` pair, 4–5 is the `analytics-engineer` pair.**
> **The FILES edited were always the right ones; the NUMBERS naming them were inverted**, so the
> propagation record pointed a re-verifier at the two files that were not touched and exempted the
> two that were. **Found by Red Team on the fourth Step 8 pass, in `0086` — and it was in `0083`
> and `0085` too.** Corrected in place with this note, as `0058` §6 did.

---

## 1. The set-membership denominator — closed, because there was never a conflict to reconcile

`0074` §4 ruled the difference **reported unreconciled** and **routed it to Step 14** as a limitation,
on the ground that *"neither figure is wrong on its face."* **That ground was right and the routing was
wrong.** Both arms have now produced the decomposition, and it is exact.

**The parameter is where D11 — the global `τ_pull` cutoff — is applied.** D11 discards **167** in-frame
S1/S2 episode records dated at or after `τ_pull`. **They split 94 on the S2 side and 73 on the S1 side**,
and that split is the whole of the difference.

| Reading | D11 applied | records examined | records dropped | waterfall line 1 |
| :--- | :--- | ---: | ---: | ---: |
| **A** | nowhere | **6,065,704** | **0** | 220,107 |
| **B** | **S2 side only** — the S1 side carried at `0068`'s published line 1 | **6,065,610** | **0** | 220,107 |
| **C** | **both sides** | **6,065,537** | **0** | **220,103** |

`6,065,704 − 94 = 6,065,610`. `6,065,704 − 167 = 6,065,537`. **Instance A published reading A, instance
B published reading B**, and each named its pipeline.

**Why it closes.** A Step 14 limitation is an uncertainty that **survives into a result**. This one
touches no result: the rule it is the denominator of **dropped zero records under every reading**, so the
numerator is 0 three times over and nothing downstream reads the denominator. **`0074`'s "publish both
numbers, not one" stands and is strengthened to three** — but it publishes as a **coverage figure with
its pipeline**, not as an open question.

**The other candidate axes were checked and are all zero**, on both arms: undated records, exact
duplicate `(user, play id)` records, and records with a non-positive `number`. **The 94 has one cause and
it is fully accounted.**

**What stays open, and it is NOT this.** Whether D11 applies to the **S1 completion walk** is `0068`'s
own open item — reading C moves line 1 to **220,103**, because **4 pairs stop being completers** and
**0 completion dates move**. **Choosing between B and C is that question, answered there, not here.**
Recording it in two places is how a ruling gets made twice and diverges.

**Provenance** (`0078` §2): every figure in this section is measured on the **2026-08-16 clean run**,
arms `a` and `b`, and is stated in `artifacts/step8-waterfall-{a,b}.json` and
`processed/step8/{a,b}/`.

## 2. `p_at_bound` — it marks WHETHER `p` reached its bound, not WHY

**`0082` §2 defined the column by two mechanisms.** TRUE where *"the rank numerator saturated at `L2`"*;
FALSE where *"the pair left at the final episode."* **Those are the same set, by construction.**

**The proof is one line of the adopted form.** `p = |{e ∈ E2 : e ≤ m_H}| / L2`, and the
**set-membership drop rule puts `m_H ∈ E2`**. So the numerator equals `L2` **iff** no listed episode
exceeds `m_H`, **iff** `m_H = max(E2) = F2` — which *is* "left at the final episode." **Neither clause
can hold without the other.**

**Measured, both arms, independently, and they agree row for row** (2026-08-16 clean run, APPLY):

| population | `p = 1.0` rows | in both classes | saturated, not final | final, not saturated | in neither |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **position 5** | **1,246** | **1,246** | **0** | **0** | **0** |
| **post-liveness** | **1,230** | **1,230** | **0** | **0** | **0** |

**A second fact, measured and NOT the same argument: 0 of 1,138 frame shows have any S2 numbering
gap**, so `E2 = {1…L2}` everywhere and the rank form reduces to `m_H / L2`. **That one is DATA and could
be false on another frame; the coextensivity above would still hold.** Stated separately because
collapsing them would make a construction argument look like a frame accident.

**So the statement at the point of use is the WHETHER form:** `p_at_bound` is **TRUE where `p` reached
its bound**, null where `p` is null. **It does not say why, because on the adopted form there is only one
why.**

**WITHDRAWN, and it is a MOTIVE, not a figure** — `0082` §2's:

> ~~*"a distribution with a spike at 1.0 means two different things about viewers and the column cannot
> say which"*~~

**False on the adopted rank form.** The spike means one thing. **Registered in `WITHDRAWN_PHRASES`**
(`src/step7_register.py`), which `check_surfaces.py` scans in `.md` text and JSON strings.

**Per `CLAUDE.md`'s third-blindness-class rule, the statistics that remain TRUE but are no longer
load-bearing: 1,246 and 1,230.** They are correct counts and both arms reproduce them. **What is
withdrawn is reading them as a SPLIT** — they are one class counted twice, not two classes summed.
**Any use of them as evidence that the column separates something is the withdrawn argument.**

**The column is KEPT, and the reason changes.** Not because it decomposes the spike — it does not — but
because **Step 10 publishes the abandonment distribution off `abandonment_point_p` and needs the spike
LABELLED**, and because **an emptiness asserted in prose and never emitted cannot be checked.** The
FALSE class stays empty through Step 13's `W` grid, since the emptiness follows from the rank form and
set membership, both of which are `W`-invariant. **If a future run ever produces a FALSE row, the rank
form or the set-membership rule has broken, and that is worth catching.**

## 3. The two residuals — both reported by instance A, neither editable by it

`artifacts/step8-waterfall-a.md` §8 reported both, correctly, and flagged both as **not this instance's
to amend.** **Both are the shape `0081` §2 fixed — a superseded count standing beside its replacement —
surviving inside a withdrawal note and a quoted table rather than in live prose.** Fourth occurrence of
that shape after `0067`, `0076` and `0081`, **and the fourth found by an agent rather than by a
control.**

**(a) The stale `88`.** The strike-through withdrawing `0077`'s *"the table is 89 columns"* said it was
*"replaced by the 88-name ENUMERATION"* — **but the enumeration directly above it is 89 names**, `0082`
having added `p_at_bound` after `0081` set it at 88. **A withdrawal note carrying a superseded count for
its own replacement.** Corrected to 89 on all three surfaces, with the 88 retained as the intermediate
state it was.

**(b) `f2_in_A_H` in `0077`'s adopted-name table.** The table is quoted in all three surfaces and lists
`f2_in_A_H` among the **adopted** names, while a bullet in the same section **drops it as derivable**
(`max_episode_in_A_H == s2_F`). **`0077`'s ruling was about SPELLING — `A_H`, not `AH` — and that ruling
still stands; the column does not.** Marked at the point of use in all three surfaces rather than
deleted, because deleting it would lose the spelling ruling that governs `n_A`, `n_A_H` and
`max_episode_in_A_H`.

**Verified: the enumeration is 89 names and the three surfaces' name sets are IDENTICAL** — checked as
sets, off disk, not by counting.

## 4. Scope and propagation

**Surfaces reached — and the count is what `CLAUDE.md` requires, not a claim that they were "checked":**

| # | Surface | Reached | What landed |
| :-- | :--- | :--- | :--- |
| 1 | `task-sheet.md` | **yes** | §1 closure, §2 restatement and withdrawal, both residuals |
| **4–5** | `analytics-engineer{,-b}.md` | **yes, identically** | the same three, verified byte-identical apart from `name:` |
| **2–3** | `data-scientist{,-b}.md` | **deliberately NOT** | neither file names the denominator, `p_at_bound` or the column set. **Step 10 reads `p_at_bound` and will gain the WHETHER statement when Step 10's obligations are written** — recorded here so the pass is not forgotten, which is how the covering qualifier went six entries reaching no agent file |
| 6 | `artifacts/` | **no edit** | both arms' deliverables already state all three readings with pipelines and already report the coextensivity as measured. **They were RIGHT; this entry ratifies them** |
| 7 | `second-brain` memory | **yes** | the glossary's denominator row said *"REPORTED, NOT RECONCILED … Routed to Step 14"* |
| 8 | `processed/` | **no edit** | `step8/{a,b}/` are per-arm working output and carry each arm's own reading, which is correct for them |

- **No rule change, no population change, no bound endpoint moves.** No figure on any dependency list
  in `CLAUDE.md` §`Derived figures` is touched, so no list is run.
- **Zero API calls.**
- **Both arms rerun against this entry**, distinct namespaces `a` and `b`.
- **Step 8 does not close by this entry.** It goes to Red Team for a third pass.
