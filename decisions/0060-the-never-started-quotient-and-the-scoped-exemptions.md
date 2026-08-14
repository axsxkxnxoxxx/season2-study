# Decision 0060 — arm a runs one convention; the exemptions are scoped; a sentence I published twice is withdrawn

| | |
| :--- | :--- |
| **Decision** | **B4:** arm a's never-started ratio takes the **floor-endpoint CI** — `0.307138 / 1.09 = 0.2818` — matching its own started-and-left convention, so **one arm no longer runs two conventions in one six-line block**. `check_ratios_written()` extended to the never-started quotient; **all four ratios in `ADOPTED_IN`**. **The "proof" sentence is WITHDRAWN from three places.** **B5:** `MARK` corrected to what `0059` §2 claimed. **B6:** the unreachable branch deleted, `DECLARE` **scoped per file and per value**. **B7:** the successor rule runs on the **emitting line**. The JSON string-field gap is recorded as a known limit. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Occasioned by** | Red Team's **thirteenth** Step 7 HOLD |
| **Amends** | `0058` §3 and `0059` §1 (a false citation, published twice); `0059` §2 (a control property the control lacked) |
| **Verified by** | `check_surfaces.py` **PASS**; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **10/10 CONFIRMED** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

*(Dated the 14th, correctly: `0052`–`0059` were corrected to the 13th at `0058` §6 because they had been dated a day ahead. The clock has since advanced. The correction was not reversed.)*

---

## 1. B4 — the defect I fixed in one quotient and reproduced in the other, same commit

`0059` created **four** ratio target paths. `check_ratios_written()` asserted **one**. **The
never-started quotient was written by the script and checked by nothing — the identical structure to
the hard-coded literal `0059` had just replaced.**

| | value | denominator | whose convention |
| :--- | ---: | ---: | :--- |
| what the script wrote | **0.2818** | 1.09 — floor-endpoint CI | **arm a's** |
| what every prose surface said | **0.2813** | 1.092 — under-the-rule CI | **arm b's** |

`0.2818` appeared in no `.md` in the repo. `0.2813` was in neither `SUPERSEDED` nor `SUPERSEDED_IN`, so
the negative half was silent; `0.2818` was in neither `ADOPTED` nor `ADOPTED_IN`, so the positive half
was silent. **`0059` §3's four newly-covered values were all started-and-left.**

**Ruled: arm a takes the floor-endpoint CI**, which is the convention its started-and-left ratio already
uses. **An arm must run one convention.** Arm a's published `0.2813` was on the other arm's, so the
divergence the study reports was being carried in one place and quietly resolved in another.

**Registered both ways:** `("bb-a", 0.2813)` in `SUPERSEDED_IN`, `("bb-a", 0.2818)` and
`("bb-b", 0.2721)` in `ADOPTED_IN`. **The third and fourth never-started ratios are DERIV's, both
exactly 0.0** — the DERIV never-started bound is degenerate, `[6.2055%, 6.2055%]`, width 0.0, zero
never-started exclusions. **They are deliberately not registered and the reason is stated in the
register**: `0.0` matches somewhere in nearly every file, so a row for it would flag everything and
disarm nothing. Two silently missing entries would have looked the same as this and meant something
different.

**`check_ratios_written()` now covers both bands**, asserts the two arms' denominators stay distinct in
each, and the run fails if any written quotient is not this arm's numerator over this arm's
denominator.

## 2. The sentence I published twice, withdrawn

> *"the never-started ratio was correctly left divergent at `0.2813` against `0.27211` in these same
> files, which is the proof this one should have been."*

**False.** `0.2813 = 0.307138 / 1.092`, and **`1.092` is the under-the-rule point estimate's CI — arm
b's convention.** So that pair was **one convention on two arms' bootstraps**, not two conventions
diverging. It is why they sit 0.009 apart while the genuine two-convention started-and-left pair sits
0.021 apart. **The genuinely divergent never-started pair is 0.2818 (a) against 0.2721 (b).**

**Withdrawn in all three places it was written** — `bb-a.md`, `0058` §3, `0059` §1.

**The conclusion it was offered to support still stands and the evidence does not.** Reconciling the
started-and-left conventions at `0057` was still wrong. But **the figure I cited as proof was itself an
instance of the defect it was cited to certify**, and I published it twice without checking which
denominator produced it — **which is the same failure as adopting Red Team's 73.6537% without checking
its population at `0051`.**

## 3. B5 — an entry asserting a control property the control did not have

`0059` §2: *"`MARK` no longer matches `corrected`, `register`, `legitimate` or `ADOPTED`."* **All four
were still there.** The edit was a string replace that **failed to match and was not asserted on** —
**the third consecutive blocker of that exact shape**, after `0055` §5a's stamp and `0056`'s inline
marking.

**Corrected, and the correction now asserts itself:** four `assert _dead not in MARK.pattern` lines run
at import, so this claim cannot go stale silently again.

**Live consequence, exactly as predicted:** with `ADOPTED` gone from `MARK`, `glossary:195`'s `73.6537`
surfaced — its only marker in context was the word "adopted" on the next line. Marked properly.

**And the two dead alternatives are gone.** `not 0\\.4033|vs 0\\.4033` inside a raw string is a literal
backslash plus any character, so they could never match what they read as. A second thing on that line
that did not do what it said.

## 4. B6 — the value scoping was written and unreachable

`EXTREME_NONE_READINGS` guarded four values on a line matching `extreme[_ ]NONE` — but the **general
`DECLARE` branch three lines above already contained `extreme[_ ]NONE`**, so the value-scoped branch
could never change an outcome. **The register documented it as "a CONTEXT exemption, not a value
exemption"; the code did neither.**

So the phrase was disarming the control against `0.0503`, `0.4033`, `0.4703` and the scoped
`0.5090` / `0.0690` — **values the two-extremes table has nothing to do with** — and the same held for
`un-?widened`, `_scope`, `share_of_population`, `proposed_pct`.

**The general branch is deleted.** `DECLARE_SCOPED` is keyed **by file and by value**, and it is scoped
to where the exemption is actually load-bearing: **`step7-deriv-floor-check-*`, the verification arms'
deliverables**, which carry the two-extremes table and are deliberately not on the whole-file allowlist.
JSON **path** markers are separated into `DECLARE_JSON_PATH` and applied to paths only, never to prose,
because a path is structure and a line is a claim.

## 5. B7 — the successor rule ran on the block

`step7_register.py` and `0059` §5 both say **"a line** carrying both." The code ran `NUM.finditer` over
the ±2-line context. **Already satisfied non-adversarially:** the adopted 6-dp width `0.403246` is
within tolerance of `0.4032`, and it appears in every bound table — so it self-declared `0.4033` two
lines away in either direction.

**Now on the emitting line.** `MARK` keeps its two-line window, because a marker legitimately wraps; the
successor rule does not, because a successor two lines away is a coincidence and on the same line is a
sentence.

## 6. Known limit, recorded not closed

**Both controls walk numeric leaves only.** A superseded figure inside a JSON **string** — a note, a
narrative field, an estimand description — is invisible to `json_numbers()` and to `verify()`. **The
`.json` half of the negative control cannot see narrative fields at all.** Not a defect today. In
`CLAUDE.md`, in the register, and stated here rather than left to be discovered.

## 7. What Red Team does not contest

**The rule, for the ninth review.** B1, B2 and B3 confirmed actioned; instance A's D-2 confirmed
actioned as described. **It checked the allowlist's obvious trap and found it closed** — the `OPERATIVE`
guard is evaluated **before** the allowlist, so the key `step7-liveness-b` cannot exempt
`step7-liveness-bb-a` by substring. The `LIVE_ELSEWHERE` withdrawal is consistent with source.

## 8. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **No rerun.** One convention ruled, four exemptions scoped, one sentence withdrawn.
- **Zero API calls.**
- **Step 8 does not launch.**
