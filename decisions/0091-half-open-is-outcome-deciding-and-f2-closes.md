# Decision 0091 — the half-open mandate is OUTCOME-DECIDING, not inert; F2 closes; three hardcoded literals removed

| | |
| :--- | :--- |
| **Decision** | **No new ruling. `0090` is implemented and Red Team's F1 and F2 are closed by measurement.** ***THE B3(a) VERDICT REVERSES: `OCCUPIED_INERT` → `OUTCOME_DECIDING`, both populations, both arms independently.*** **71 APPLY rows and 59 DERIV rows change outcome state** under the forbidden date-level form — **36 of them from never-started to Continued**, the two ends of the headline. **F2 was worse than reported**: the independence proxy admitted **all four** identity families, not one. **Both fixed and DEMONSTRATED, not asserted.** |
| **Recorded by** | Analytics Engineer, on both arms' rerun findings |
| **Date** | 2026-08-16 |
| **Occasioned by** | Red Team's **fifth** Step 8 HOLD (F1, F2), folded into the `0090` rerun |
| **Amends** | `0089` §2(a) — its adopted verdict was not merely measured on the wrong set, **it was WRONG**; `0090`'s own propagation |
| **Verified by** | `check_surfaces.py` **PASS**; the `analytics-engineer` pair byte-identical apart from `name:` |
| **Status** | Open. **Step 8 is NOT approved. Goes to Red Team for a SIXTH pass.** |

---

## 1. F1 — the mandate is load-bearing on the result, and the previous answer was wrong

**Both arms measured the settling number independently and agree to the row.** Position-5 rows whose
**outcome state changes** under the forbidden `date(ts) ≤ date(τ)` form, each bound varied alone:

| | `τ1` | `τ2` | joint |
| :--- | ---: | ---: | ---: |
| **APPLY** | **52** | **19** | **71** |
| **DERIV** | **45** | **14** | **59** |

**Transitions on APPLY:** **36 never-started → Continued**, 16 never-started → started-and-left, 19
started-and-left → Continued. ***Both directions run against the estimand***, and 36 of the 71 move a
pair between **the two states this study exists to separate.**

***`0089` §2(a) adopted "the measured state is occupied and inert." That verdict is not merely
unsupported — it is FALSE.*** It was computed on **1 row of the 311**. Withdrawing it was worth more
than it looked.

**A distinction neither arm had drawn before, and it matters:** **line 6 does not move at all** — 703 on
APPLY and 99 on DERIV **under every form** — because **the silence test reads an insertion clock, not an
episode timestamp.** So the mandate is **load-bearing on outcomes and inert on line 6**, and those had
been reported as one thing.

**Arm A's joint note, reported not reconciled:** it states the joint form gives 71 *"not 52 + 19, because
a row can flip twice"* — **but 52 + 19 = 71**, and arm B measured the joint and the sum separately and
found them equal. **The number agrees; the claim about why does not, in one arm's prose.**

**This publishes at Step 14.** The half-open form is not a coding convention on this data; it decides 71
APPLY outcomes.

## 2. F2 — the proxy admitted every family, and the fix is demonstrated

**Worse than the review found.** `real = parts is not None and len(parts) > 1` admitted **all four**
identity families, each a complementary partition of the same mask the population size is taken from:
invariant 1 (`never`/`left`/`continued`, exhaustive by their defining expressions), invariant 6
(`M & left`, `M & ~left`), invariant 7 (`mixed` + `wholesale` = `touched` by set algebra), invariant 9
(`τ2 ≤ τ_pull` and its complement). **None could fail on any data**, including the one the deliverable
called *"the identity that closes the hole."*

**Both remedies applied.** The population size is now sourced **independently of the asserted count** —
11 from the emitted `analysis_table.csv.gz`, 3 from earlier stages' JSON, 1 by an independent parse of
the ledger — and the label and claim are corrected.

***And the mechanism is DEMONSTRATED, not asserted*** — the distinction `0089` §1 got wrong and Red Team
caught. **All 15 identities are re-run against `population + 1` and must FAIL, asserted, with the
registry asserted non-empty.** **Invariant 6 reconstructs `0080` §3's exact mispairing —
`19,042 + 177,513 = 196,555` against `196,654`, 99 rows in neither — and the identity fails.**

**Arm B did the same on its side**: 6 injected defects run through the same `cover()`, `cover_ok()`,
`_independent_identity()` and the same published aggregate; **5 of 5 checkable cases caught**, asserted
so an escape aborts before a deliverable is written, **and the one that passes by design — a hardcoded
literal — named, with its separate counter reading 0.**

## 3. Three hardcoded literals, one inside the table built to stop self-reporting

**Arm A found `"holds": True` published as a literal at the `S1_completion_walk` site — inside the
per-site D11 table `0088` §1(b) created precisely so mandates would stop being self-reported.** Now
computed: the not-applied declaration is checked against the walk's own output — **4 completers used a
post-cutoff record, and a silent application would drive that to 0 and fail the assertion.**

**Two more removed:** `tau1_and_tau2_are_midnight_aligned_UTC` and `holds_on_every_frame_show`.
**`0087` §4 found hardcoded `True` in one arm; it reappeared in the other arm's brand-new B3(b) table
one entry later.**

**Both arms reproduce the attained bound**: `τ2 > τ_pull` is 0, but **20 APPLY and 17 DERIV rows sit
exactly at `τ_pull`**, so a `>=` form of invariant 9 would fail.

## 4. `0090`'s propagation missed the pair — my defect, reported by instance B

**`0090` struck `0074` ruling 5's framing at `task-sheet.md:506` and left the equivalent bullet UNMARKED
in both `analytics-engineer` files**, so *"D9 uses the STRICT key, with the loose count of 75 reported
alongside"* sat **below** its `0090` replacement, unqualified, **in the files the isolated instances
read.**

**The shape `0067`, `0076`, `0083` §3a and `0089` §3 each fixed elsewhere — and the second time in three
entries that one of these propagations reached `task-sheet.md` and missed the pair.** Marked at the point
of use, together with the **U3 example names** in the same bullet that `0088` §3 had already superseded.

## 5. Carried — unchanged, none blocking per Red Team

- **The D9 tie-break.** `secondchance` (8) and `theisland` (7) unique; **six keys tie at 6**. Every key
  at every rank publishes under both bases in both arms. **Red Team's position: publish all six and
  retire "third-largest" rather than invent a convention.**
- **`specs/` as a ninth surface.** **Red Team's position: adopt it.**
- **The one-pair D9 divergence** — `435,642` against `435,643` on the S1-only class, two classes agreeing
  exactly. Reported, not reconciled.
- **`0090` §2's flagged reading** of *"this half"*. Both arms implement the broad reading and say so at
  the point of use; **arm A names its §5.5 bound table as what narrows if a single half was meant.**

## 6. Scope

- **No population change, no waterfall line moves, no bound endpoint on the headline estimand moves.**
  **The 71 and 59 are a COUNTERFACTUAL** — the forbidden form is computed with the half-open baseline
  asserted to reproduce the pipeline's own states before diffing, and its only output is a count.
- **Surfaces reached: 4–5** (both agent files, identically — the `0090` residual). **1, 2–3, 7: no edit
  needed.** **6, 8: both arms rerun.**
- **Zero API calls.**
