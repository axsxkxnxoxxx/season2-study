# Decision 0071 — the `data-scientist` pass for `0070`'s rulings 1, 2 and 7

| | |
| :--- | :--- |
| **Decision** | **`0070`'s rulings 1, 2 and 7 are propagated to both `data-scientist` files identically.** Step 9 **consumes Step 8's DERIV and D4 and rebuilds neither**; the silence test's evidence is **restricted to records dated before `τ_pull`**, stated where the rule statement lives. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `0070` §5 named this pass as deliberately not done and stated what it would leave broken |
| **Status** | Closed. **Step 8 has not launched.** |

---

## 1. Rulings 1 and 7 — Step 9 consumes, it does not rebuild

**Step 8 now emits both populations — APPLY 196,654 and DERIV 147,370 — and the D4 count.** Step 9 is
told, in terms, **not to rebuild either.**

**Rebuilding is the second definition those rulings exist to prevent**, and a second definition of one
figure is the defect this study has hit more than any other (`0058`, `0061`, `0062`).

**Two sentences carry the weight, and they are the reason this is not merely a note:**

> **If Step 8's output does not carry DERIV or D4, say so and stop — do not reconstruct them.**
>
> **A reconstruction that agrees today is still a second definition tomorrow, and the dual diff cannot
> see it, because both instances would rebuild the same way.**

**The second is the one that matters.** A rebuild is invisible to the study's only cross-check: both
arms would reconstruct from the same inputs by the same route and agree, and agreement would be read as
verification. **That is `0055` §5c's shape** — two copies of one computation, differing only when
something upstream moves, and by then the diff has been reporting a pass for weeks.

## 2. Ruling 2 — stated where the rule statement lives

**The silence test's evidence is restricted to records dated before `τ_pull`.** **This applies an
existing ruling consistently; it is not a new one.** **D11, approved at the Step 1 gate, makes `τ_pull`
a global frozen cutoff and discards records at or after it from every computation** — and the silence
test is a computation.

**The unstated version produced the reported-not-reconciled 792 (A) against 791 (B) at Step 7**, where
one arm applied the restriction and the other did not.

**Measured before the ruling, because Step 7 is an approved gate: exclusions are 703 on APPLY and 99 on
DERIV either way.** No insertion instant exceeds the clamp at 2026-08-10T20:48Z, and D10 already forces
`τ1 ≤ τ_pull − 91 d`, **so the restriction is inert on the exclusion set and bites on the robustness
tail** — which is exactly where the divergence lived. **Step 13 re-runs the rule at eight arms, and the
scope holds at every one**, which is stated because that is where an unstated scope would next diverge.

## 3. Surfaces

**REACHED:** `.claude/agents/data-scientist.md` and `.claude/agents/data-scientist-b.md`.
**Verified byte-identical apart from `name:`** — the only diff is line 2.

**DELIBERATELY NOT REACHED:**

| Surface | Why | Standing risk |
| :--- | :--- | :--- |
| **`task-sheet.md` Step 8**, both `analytics-engineer` files | **already carry all three** from `0070` | none |
| **`artifacts/`, `.claude/agent-memory/second-brain/`** | **checked, not assumed.** These are forward-looking spec obligations; **no published figure moves** — ruling 2 was measured inert, and rulings 1 and 7 change who computes a number, not the number | none |
| **`task-sheet.md` Step 7's `THE RULE` block** | **outside this pass's scope, which was the `data-scientist` pair** | **NAMED, NOT SILENT: `task-sheet.md` states ruling 2 at Step 8 and in the `data-scientist` pair, and NOT in Step 7's rule block.** **Step 13 reads that block** when it re-runs the rule across eight arms. **Measured inert on the exclusion counts, so nothing published is wrong today** — but the scope is unstated in one of the two places the rule is written down, and that asymmetry is what produced the original divergence |

**The last row is the point of stating this table.** `0070` §5 named exactly this class of omission and
it is named again here rather than closed quietly or left to be found: **the same sentence now lives in
two of the three places the rule is stated.**

## 4. Scope

- **Three rulings, one pair, no figure changes.**
- **Zero API calls.**
- **Step 8 has not launched.**
