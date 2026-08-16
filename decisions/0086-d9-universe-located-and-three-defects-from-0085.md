# Decision 0086 — B1's axis is LOCATED and the choice is the Human Lead's; three defects `0085` itself introduced or left

| | |
| :--- | :--- |
| **Decision** | **B1's diagnostic is CLOSED: the D9 divergence is entirely a UNIVERSE difference, and instance B reproduced BOTH published lists from ONE build by varying only the universe.** Arm A publishes **U1**, arm B publishes **U3**, each named at the point of use. **Choosing the universe is a spec decision and is NOT made here.** **Three defects fixed:** `0085`'s propagation broke list indentation on surfaces 4–5 (**a substring match that started mid-line passed the uniqueness assertion**); the `analytics-engineer` pair said Step 8 was **NOT LAUNCHED** after four launches; and two read-backs on surface 6 carried the same stale claim, now stamped. **B3 remains open and still blocks.** |
| **Recorded by** | Analytics Engineer, on both arms' rerun findings |
| **Date** | 2026-08-16 |
| **Occasioned by** | The 2026-08-16 reruns against `0085`. **Both arms independently reported the indentation defect; each reported one of the two stale-launch surfaces** |
| **Amends** | `0085` §2 (which posed the universe question without measuring the axis) and `0085`'s own propagation |
| **Verified by** | `check_surfaces.py` **PASS**; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **11/11**; the pair byte-identical apart from `name:`, re-verified after each of the two edits |
| **Status** | Open. **Step 8 is NOT approved. B3 (`0085` §7) blocks and is the Human Lead's. The universe choice is a second item awaiting ruling.** |


> **SURFACE NUMBERING CORRECTED 2026-08-16 (`0087`).** This entry numbered the
> `analytics-engineer` pair **2–3** and the `data-scientist` pair **4–5**. `CLAUDE.md` numbers them
> the other way: **2–3 is the `data-scientist` pair, 4–5 is the `analytics-engineer` pair.**
> **The FILES edited were always the right ones; the NUMBERS naming them were inverted**, so the
> propagation record pointed a re-verifier at the two files that were not touched and exempted the
> two that were. **Found by Red Team on the fourth Step 8 pass, in `0086` — and it was in `0083`
> and `0085` too.** Corrected in place with this note, as `0058` §6 did.

---

## 1. B1 — the axis is located, and it is the whole of the divergence

**Instance B reproduced BOTH lists `0085` §2 quoted, from a single build, by varying only the universe.**
That is the measurement `0085` §2 asked for and did not have.

| universe | clustering | largest | maximum |
| :--- | :--- | :--- | ---: |
| **U1** — slugged show IDs (***the two arms' U1 are NOT one set — see the restriction below***) | by loose key | `secondchance` 8, `theisland` 7, `maigret` 6 | **8** |
| **U2** — the **1,138** frame shows | by loose key | — | **2** |
| **U3** — the **75** D9 candidate complementary pairs | by loose key | `thetwilightzone` 10, `thetraitors` 7, `manhunt` 5 | **10** |

**`0085` §2's "maxima 8 against 10" is exactly U1 against U3.** **Neither arm had a bug.** Each computed
a defensible object and the spec named neither.

**Arm A publishes U1; arm B publishes U3.** Both now name it at the point of use, which is what `0085`
§2 required. **REPORTED, NOT RECONCILED.**

**Two further things the arms surfaced that the spec also does not fix, and they compound:**

- **The RANKING BASIS was unstated too.** Arm A ranks by **distinct strict keys merged** and emits a
  second ranking by **distinct show IDs** beside it, which reorders the list — `secondchance` 8,
  `theisland` 7, **`blackout` 7**. **Same universe, same key, different list.**
- **The UNITS differ between universes**, so a cluster size from U1 is not comparable to one from U3:
  distinct show IDs per key against complementary signature rows per key. **A reader comparing 8 to 10
  is comparing two different quantities.**

**`task-sheet.md`'s own illustration — The Twilight Zone, The Traitors, Manhunt — is U3.** So the spec's
example silently presumed one universe while its instruction named none, **which is why arm B's list
matched it and arm A's did not, and why `0084` §5 filed the whole thing as an arm-A wording problem.**

**Not ruled here.** The loose key publishes because it **bounds how wrong strict could be**, and which
universe makes that bound meaningful is a judgement about the estimand.

***RESTRICTED 2026-08-16 (`0087`), Red Team F2.*** This section said ***"every D9 count still reconciles
across both arms."*** **That generalises past what was checked and is FALSE as written.**

**The FIVE RULED counts do reconcile** — strict 0, loose 75, third key 76, half (a) 0 and 6, half (b) 0
and 27 — **and that is the whole of what was verified.** **THREE COVERAGE counts do NOT:**

1. **Arm A publishes 46,428 and 46,366 for one labelled quantity, 27 lines apart in one section.** The
   second is computed off the **D9 coverage pivot** and **mislabelled as the sweep**, and its "0 carry no
   slug" clause is therefore computed on the wrong base.
2. **The two arms' "U1" are consequently TWO DIFFERENT SETS, 62 IDs apart.** **Naming "U1" does not
   identify the object**, so the axis this section claims to have located is located only to the first
   digit.
3. **The user-show coverage rows are unreconciled — 747,478 (A) against 726,103 (B)** — **reported by
   neither arm and by no entry until now.**

**D9's ruled result is 0 and 0, and the coverage counts are the only thing separating that from "looked
nowhere."** That is why these are not bookkeeping. **And the U1 parenthetical above compounded it: both
of its numbers are recoverable from arm A alone, so it was never the arm-against-arm comparison it read
as.** **The universe question remains unruled and the three coverage defects are open.**

## 2. `0085`'s propagation broke the list structure on surfaces 4–5

**Both arms reported it independently.** `0085` §2's item entered `0074`'s six-ruling list as **`5a`**,
and **ruling 5 dropped from 8-space to 4-space indentation**, so the list rendered `4, 5a, 5, 6` with
**`5a` nested under ruling 4's D11 text** and **ruling 5 promoted to a top-level Step 8 mandate** rather
than one of `0074`'s six.

**The cause is a bug in how the propagation matched, not a typo.** The script's anchor string began with
**four** spaces; the line on disk had **eight**. **A four-space-prefixed string is a substring of an
eight-space line**, so `count(old) == 1` **passed on a mid-line match**, and the replacement spliced in
at column 4, leaving the original's first four spaces stranded ahead of it.

**The uniqueness assertion cannot catch this**, because the match genuinely is unique. **What catches it
is anchoring to line starts**, which the repair used: both blocks were located by
`line.lstrip().startswith(...)` and re-indented, never by substring. **Content was complete and correct
throughout; no figure was affected** — which is exactly why no numeric control saw it and both readers
did.

## 3. "NOT LAUNCHED" after four launches — surfaces 4–5 and 6

**Surfaces 4–5.** The `analytics-engineer` pair's Step 8 bullet read **"GATE, dual implementation. NOT
LAUNCHED."** Step 8 has launched **four times**; both arms have executed against the spec through
`0085`; Red Team has returned **three** gate reviews. **Unapproved is not unlaunched, and the line read
as the latter in the file the isolated instances consult.** Corrected, with the superseded phrase named.

**Surface 6.** `artifacts/step8-readback-{a,b}.md` carry *"Step 8 is a gate, it is unapproved, and it has
not launched."* **True when written on 2026-08-14; half of it is now false.** **Stamped, not edited** —
they are historical read-backs, and `CLAUDE.md` requires a deliverable carrying a superseded claim to be
stamped rather than left to read as current. **The stamps are negative only**: each names what is
superseded, confirms the *unapproved* half still holds, points at the operative spec and deliverables,
and **restates no adopted figure.**

**Arm A reported the surface-4 instance; arm B reported the surface-6 instance. Neither control saw
either**, because both are prose about state carrying no number and no registered phrase — the first
blindness class, still unchecked by design.

## 4. Both arms reconcile on every measured value

**Nothing moved.** Both arms report all four `0085` changes as presentational or additive, with no rule,
population or bound endpoint affected.

- **Waterfall** identical on both populations: 220,107 / 220,107 / 220,107 / 201,900 / 196,654 /
  195,951 / 195,951.
- **Liveness**: 703 from 216 accounts on APPLY (604 + 99), 99 from 73 on DERIV (0 + 99).
- **Columns**: 89, set-equal to the enumeration, both arms.
- **`p_at_bound`, four populations × the full cell set, both arms**: APPLY 1,246 / 0 / 0 / 0 and
  1,230 / 0 / 0 / 0; **DERIV 1,072 / 0 / 0 / 0 and 1,056 / 0 / 0 / 0.** **B2 is satisfied in both arms.**
- **Line-6 marginal decomposition, both arms**: **APPLY 1,355 − 652 = 703; DERIV 751 − 652 = 99.**
- **The three-link chain measured, both arms**: link 3 labelled **NOT construction**, with
  `max(E2) ≠ F2` on **0 of 1,138** frame shows and `s2_aired_lt_listed` **0 shows**.
- **All eight invariants pass**, every coverage identity holding.

**A fact neither arm had stated before and arm A emitted unprompted:** the `NOT Continued` conjunct
spares **652 on DERIV as well as APPLY** — Continued requires S2 evidence, so every Continued-and-silent
pair is a DERIV pair, and **the two populations differ at line 6 only through the silence-alone term**,
1,355 against 751.

**Build tags diverge by design.** Arm A tagged `a/2026-08-16-0085` rather than reusing `a/2026-08-16`,
**because two builds now exist on that date for that arm and reuse would make every figure ambiguous
between the reviewed run and this one.** Arm B used `b: … 2026-08-16-r3 (spec through 0085)`. **The
convention is unstated in the spec; both arms disambiguated and did so differently. Reported.**

## 5. Carried — two items, both the Human Lead's

| | Item | Status |
| :-- | :--- | :--- |
| **B3** (`0085` §7) | The **half-open UTC-instant form** and **D11** carry no assertion; both arms self-report in prose | **BLOCKS.** Arm A notes one half may be **promotion rather than new work** — it already asserts D11's inertness on the outcome windows at `src/step8_a_3_table.py:98`, **outside the published invariant set and so invisible to any reader of the deliverable.** `date(watched_at) <= T1` appears nowhere in either implementation, but that remains a self-report |
| **The D9 universe** | U1 / U2 / U3, plus the unstated **ranking basis** | **Does not block.** Every D9 count reconciles; the divergence is located, named in both arms, and reported |

## 6. Scope

- **No rule change, no population change, no figure moves.**
- **Surfaces reached:** **4–5** (indentation and the launch status, identically) and 6 (two stamps).
  **Surface 1 needed no edit** — `task-sheet.md`'s D9 bullet already carries `0085` §2's requirement and
  its list structure was not touched by the defective match. **Surfaces 2–3, 7, 8: not applicable.**
- **Zero API calls.**
- **Step 8 goes to Red Team for a fourth pass, with B3 declared open in the brief.**
