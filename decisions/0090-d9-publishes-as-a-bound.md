# Decision 0090 — D9 publishes as a bound: strict is the floor, loose is the ceiling, neither is the point estimate

| | |
| :--- | :--- |
| **Decision** | **D9 publishes as a BOUND.** **Strict is the FLOOR, loose is the CEILING, both labelled, and NEITHER is the point estimate** — neither endpoint may be quoted as *"D9's result"*. ***SUPERSEDES `0074` ruling 5's framing, "USE THE STRICT KEY AND REPORT THE LOOSE COUNT ALONGSIDE", under which STRICT WAS THE ANSWER and loose was context.*** **The bound applies to every D9 quantity that has both forms**: complementary pairs `[0, 75]`, half (a) `[0, 6]`, half (b) `[0, 27]`. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-16 |
| **Occasioned by** | The Human Lead, applying `0074` ruling 5's own reason one step further |
| **Amends** | `0074` ruling 5 (the framing, not the keys); `0078` §3 is extended, not superseded |
| **Verified by** | `check_surfaces.py` **PASS**; the `analytics-engineer` pair byte-identical apart from `name:` |
| **Status** | Open. **Step 8 is NOT approved.** **This ruling does NOT address Red Team's two blockers** — see §3 |

---

## 1. The ruling is `0074` ruling 5's own reason, carried through

**The loose count publishes for exactly one stated reason: it BOUNDS HOW WRONG STRICT COULD BE.** A
quantity published *because it bounds another* **is an endpoint**, not a footnote. **Under the old
framing the endpoint was printed and the interval was not**, which invited every reader to take strict's
`0` as the answer.

**This argument has already run once in this study.** `0078` §3 extended the loose count to half (b)
*"because `0074` ruling 5's own reason applies to half (b) exactly as it applies to half (a)."*
**Same reason, one step further.**

**Direction is part of the label, and it is not symmetric.** **Strict is the FLOOR** because it matches
only slugs identical modulo punctuation, so it **cannot over-count**. **Loose is the CEILING** because
stripping a trailing year **merges genuinely different shows** — remakes and national versions.
**The error runs OPPOSITE to D9's own lower-bound caveat**, which is why the interval publishes rather
than being resolved away.

**Two guards recorded with it.** **The third key is not an endpoint**: stripping a trailing digit group
of arbitrary length reduces `the-100` to `the`, and its **76** is a *different key's answer*, reported
as a divergence and never as the ceiling. **And a zero floor is not an absence of evidence** — `0` is a
**measured** floor on a stated coverage, and the coverage publishes beside it, or the bound is
indistinguishable from a check that looked nowhere.

## 2. One reading taken, and it is flagged

**The ruling says *"applied to this half"*, singular.** **Implemented as applying to EVERY D9 quantity
with both forms** — complementary pairs `[0, 75]`, half (a) `[0, 6]`, half (b) `[0, 27]`.

**The reason is `0078` §3's:** publishing a bound for one half and a point estimate for the other
**leaves the reader unable to bound the total**, which is the exact defect `0078` §3 was written to
correct. **If a single half was meant, say so and it narrows.**

## 3. What this ruling does NOT do

**It does not touch either of Red Team's fifth-pass blockers**, and the gate does not move on it alone.

- **F1** — the outcome-state count on the separating interval `[τ, τ + 24h)`, four numbers, both bounds
  × both populations. **Measured by neither arm.**
- **F2** — one arm's `real = len(parts) > 1` independence proxy, under which **three "REAL ARITHMETIC"
  identities are complementary partitions of one mask and cannot fail**, including the one its
  deliverable calls *"the identity that closes the hole"*.

**Red Team: *"HOLD lifts on F1 and F2 alone."*** **Neither needs a ruling** — both are defects in the
arms' own deliverables, and neither moves a published figure. **They are folded into this rerun**, so
the cycle carries the ruling and the two fixes together rather than costing two.

## 4. Scope

- **No population change, no bound endpoint on the headline estimand moves.** **D9's own numbers do not
  change** — `0`, `75`, `6`, `27` and the divergent `76` are all already measured. **What changes is
  which of them is presented as the answer.**
- **Surfaces reached: 1** (`task-sheet.md`, including `0074` r5's framing marked superseded at the point
  of use) and **4–5** (both `analytics-engineer` files, identically). **2–3 not applicable.**
- **Zero API calls.**
- **Both arms rerun. Step 8 then goes to Red Team for a SIXTH pass.**
