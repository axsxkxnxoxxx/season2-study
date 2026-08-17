# Decision 0099 — `second-brain`'s post-gate catch-up; a withdrawn cluster name live on three spec surfaces; the two-FALSE-class hazard

| | |
| :--- | :--- |
| **Decision** | **No new ruling.** `second-brain` is current to `0098` and the gate closure. **Two defects it found are actioned here.** **K1: a cluster name `0089` §2(c) withdrew in terms was still live on `task-sheet.md` and both `analytics-engineer` files**, contradicting its own file 65 lines lower, and **invisible to the dual diff because both copies are identical.** **K2: *"the FALSE class is empty"* is SAFE for one class and WRONG BY 17,895 ROWS for the other**, and the unqualified form sat in `src/step7_register.py`. **Step 8b is unblocked and is exactly the consumer.** |
| **Recorded by** | Analytics Engineer, on `second-brain`'s catch-up |
| **Date** | 2026-08-17 |
| **Occasioned by** | The post-approval catch-up across `0089`–`0098` |
| **Verified by** | `check_surfaces.py` — **all halves and the positive half over surface 7**, which `second-brain` asked for because several of its new figures were **absent rather than stale**, the shape the negative grep cannot see |
| **Status** | Closed. **Step 8 remains APPROVED (`0098`). Step 8b and Step 9 are unblocked and NOT launched.** |

---

## 1. K1 — a withdrawn cluster name, live on three spec surfaces

`task-sheet.md:664` and both `analytics-engineer` files at `:257` read *"under U1 the largest clusters
are `secondchance` (8), `theisland` (7), **`maigret` (6)**."*

***`0089` §2(c) withdrew that in terms:*** **"THE THIRD PLACE IS NOT DETERMINED AND THIS ENTRY SHOULD NOT
HAVE NAMED ONE."** There is a **six-way tie at 6** — `blackout`, `hunted`, `maigret`, `missing`,
`thefamily`, `yourhonor` — and which appears third is **the tie-break, which no rule specifies.**
**Neither arm picked `maigret`.**

**Both agent files contradicted themselves 65 lines lower**, at `:321`: *"with a six-way tie at 6 whose
ordering is unruled."* **And the dual diff could not see it, because both copies are identical** — the
standing limit, demonstrated again.

**Nothing published is wrong**: residual 7 of the gate approval publishes the tie, and both arms list all
six keys. **The defect is that an instance reading the spec would name a third place the ruling says is
not determined.** **Marked at the point of use on all three surfaces.**

**Three other occurrences were read and left**: `task-sheet.md:660` and the agent files at `:254` use
`maigret` correctly, to say that **ranking by distinct show IDs displaces it with `blackout`**; and
`task-sheet.md:522` quotes it describing the historical arm divergence. **A grep hit is not a defect
until you read the line.**

## 2. K2 — one sentence, two classes, 17,895 rows apart

***"The FALSE class is empty" is SAFE for CLASS 1 and WRONG for CLASS 2***, and **two different FALSE
classes sit on the same page** of arm a's §3.1:

| | what it is | value |
| :--- | :--- | :--- |
| **CLASS 1** | the **coextensivity gap** — rows saturated but not final, or final but not saturated | **0** on all four populations |
| **CLASS 2** | the **column's own FALSE value** — Started-and-left rows where `p < 1.0` | **17,895 / 17,812 / 15,771 / 15,688** |

**Arm a names the hazard itself**: *"a consumer that reads 'the FALSE class is empty' and provisions a
two-valued column is wrong by 17,895 rows."*

***Step 8b is unblocked and is exactly that consumer*** — it builds the schema Steps 9–13 write into,
**with no conversion layer.**

**`second-brain` found the unqualified sentence in its own memory in three places and corrected them.**
**It then reported that the same sentence sits in `src/step7_register.py`'s `GROUNDS_WITHDRAWN["0083
SS2"]`, and did not touch it — `src/` is not its surface.** **Qualified here**, with both class values
and the instruction never to restate the sentence without naming which class.

## 3. What `second-brain` verified rather than assumed

**Its three trap-table repairs held**, checked row by row: `703` now carries two live readings **with a
populated illegitimate column**; `604` has its own row; and `1,355` / `751` are stated as **current and
mandated** under `0085` §5, with the old *"never restate"* wording corrected. **The gate approval's own
line-6 decomposition confirms them.**

**It declined two things, both correctly.** It listed two further ground-withdrawals as **candidates
only** rather than adding them to its register — *"extending my human half past the source would be the
two-registers defect committed by me."* **And it did not renumber the Mode H / Mode I letter collision**,
which is the Human Lead's.

## 4. Carried for the Human Lead

- **The Mode H / Mode I collision** — its register defined H as *an asserted action never taken*; the
  ground-withdrawal class went in as **I** rather than renumbering, because **H's ten instances are cited
  by letter elsewhere.**
- **`441` against `439` needle candidates.** `0095` §3 says 441; `0096` §3 and residual 8 say 439.
  **Neither is a defect count**, and no entry states the relation.
- **The Red Team pass-count offset.** Totals now agree at eleven, but the intermediate numbering never
  reconciled — `0091` §2 says *"sixth pass, F3"* where the arm's report says *"seventh pass, finding 3"*,
  and `0092` names no pass. **Low consequence for figures; the review sequence IS the Step 18 artifact.**
- **Whether `second-brain`'s R2–R9 need dispositioning** now the gate is closed.
- **`GROUNDS_WITHDRAWN` holds three**, and two more from this stretch are candidates: `0091` §1's line-6
  warrant, and `0089` §2(a)'s strictness attribution. **The statistics behind both are still true.**

## 5. Scope

- **No population change, no figure moves, no rule change. Step 8's approval is untouched.**
- **Surfaces reached: 1, 4–5** (K1), **7** (`second-brain`'s own files), and `src/` (K2).
- **Zero API calls.** **Neither arm ran.**
