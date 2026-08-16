# Decision 0084 — propagation failure #22; the phrase control was blind to line wrapping, and its probe certified the blindness

| | |
| :--- | :--- |
| **Decision** | **No new ruling. This entry applies standing rules to two defects an agent found in the previous entry's own propagation.** **#22:** `0083` §2 reached `second-brain`'s glossary **table row** and not its **bullet**, 71 lines above, which went on stating `0082`'s superseded definition and its withdrawn motive as current. **The phrase half could not see it: `WITHDRAWN_PHRASES` matched a literal substring against ONE LINE AT A TIME, and this repo hard-wraps prose**, so any registered claim over about six words was invisible wherever it wrapped. **Matching is now whitespace-normalised across line breaks, the coverage prints unconditionally, and a self-test asserts the wrapped case.** |
| **Recorded by** | Analytics Engineer, on the Human Lead's standing rules (`CLAUDE.md` `## Propagation`; *"a check that finds nothing because it looked nowhere must fail"*) |
| **Date** | 2026-08-16 |
| **Occasioned by** | **Instance A's rerun findings 2 and 3**, on the 2026-08-16-r2 execution of Step 8 against `0083` |
| **Amends** | `0083` §4's propagation table, which claimed surface 7 was reached; and `src/check_surfaces.py`'s phrase half |
| **Verified by** | `check_surfaces.py` **PASS**, with the fixed matcher and a **regression proof** on the exact pre-fix text; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **11/11 CONFIRMED** |
| **Status** | Closed. **Step 8 is the remaining gate and is NOT approved.** **Four items are carried for the Human Lead in §5.** |

---

## 1. Propagation failure #22 — the shape `CLAUDE.md` names, in the file that names it

`0083` §4 recorded surface 7 as **reached**. It was reached **once**. The glossary carries `p_at_bound`
in **two** places, and only one was corrected:

| line | what it said after `0083` | |
| ---: | :--- | :--- |
| **154** | the restated **WHETHER** form, the coextensivity, the empty FALSE class | **correct** |
| **83** | *"a boolean separating the two meanings of `p = 1.0`"*, `0082`'s **withdrawn motive**, and 1,246 / 1,230 as *"totals the two classes must sum to"* | **superseded, live** |

**This is verbatim the failure `CLAUDE.md` describes** — *"an adopted figure and its superseded
predecessor live in the same file, sometimes ten lines apart, each declaring the other wrong."* Here the
distance was **71 lines**, and the two entries were a **table row** and a **bullet**, which is why
correcting the one that a search for the term surfaces first felt like completing the propagation.

**Found by instance A on the rerun. Not by a control.** That is now the fourth consecutive defect of
this class found by a reading agent, after `0067`, `0076`, `0081` and `0083` §3.

## 2. The control could not see it — and the probe that "verified" the control certified the blindness

**`scan_phrases()` tested `phrase in line`, one line at a time.** This repository hard-wraps prose at
about 100 columns. **So a registered claim longer than roughly six words was invisible wherever it
happened to wrap**, which is most places it occurs. Three occurrences were live at the moment the half
reported `none`: the glossary bullet above, and two legitimate quotations inside withdrawal notes in the
`analytics-engineer` pair.

**And this is the part worth recording.** When `"means two different things about viewers"` was
registered at `0083`, it **was** adversarially probed — markers stripped, the check fired, the file
restored byte-identical — and the result was reported as establishing that the half's `none` was *"a
clean result, not an empty one."*

**The probe ran against `task-sheet.md`, where the sentence happens to sit on a single line.** It
demonstrated that the matcher fires **on the unwrapped case**, and it was reported as demonstrating that
the matcher fires. **A probe that exercises one branch and is described as exercising the control is the
same error as a check that looks nowhere and reports clean** — one level up, in the verification rather
than in the code. **The register's own text said the phrase half is matched against prose; nothing said
it was matched line by line, and nobody read the loop.** `CLAUDE.md` already carries the rule this
violates: *"a control asserted to exist is not a control, and this one was found by reading the code
rather than the claim."*

## 3. The fix, and the self-test caught a bug in the fix on its first run

**Matching is whitespace-normalised across line breaks.** The file becomes one lowercase string with
runs collapsed and lines rejoined by a single space, carrying a **character → line map** so a hit still
reports the line or line span it came from. **The `STRUCK` window is taken around the whole SPAN**, not
around a line, because a marker may sit either side of a claim that itself wraps.

**Three properties, none of them asserted in prose:**

1. **The coverage prints unconditionally, hit or no hit** — `6 registered phrases × 219 files (19,408
   lines, 56,775 JSON strings); 35 skipped` — **and the run asserts the counts are non-zero.** `none`
   with no coverage beside it is indistinguishable from *looked nowhere*.
2. **A self-test runs at import**: a registered phrase, hard-wrapped, must be found. **It failed on the
   first run of the fix** — rejoining un-stripped lines left a **double space at every wrap**, so the
   matcher was still blind, one character narrower. **The fix's own defect was caught by the test
   written with it**, which is the whole argument for writing the test with it.
3. **A regression proof, on the exact pre-fix text**: the old per-line matcher is **BLIND** to it, the
   new one **FINDS** it. Run and recorded, not asserted.

**The fixed control immediately fired on the corrected glossary bullet**, because the withdrawn sentence
is quoted there inside a supersession note whose marker sat outside the context window. **Marked at the
point of use with a strikethrough**, per `CLAUDE.md`'s exemption for a string *"explicitly named as
superseded at the point of use."* **The control finding its own author's text is the control working.**

## 4. The definition files are a SESSION SNAPSHOT — both arms reported it independently

**Both instances reported that the copy of their own definition file supplied in their prompt was
pre-`0083`**, carrying the stale `88` note and `0082`'s two-mechanism `p_at_bound`, while the on-disk
file was current. **Both worked from disk and filed the disagreement as a finding, which is the standing
rule working exactly as written.**

**The consequence is not local to this run.** A ruling propagated to `.claude/agents/*.md` **mid-session**
lands on disk, passes `check_surfaces.py` and every grep, and **still does not reach an instance launched
later in that same session.** **Surfaces 2–5 are reliably current only in a fresh session.**

**No control can see this**, because the file the control checks is correct. **The instruction to prefer
the on-disk file is the only thing standing between this and a dual run executing a superseded spec** —
and it held here **because both instances are told to prefer disk and both did.**

**Recorded, not ruled.** Whether this becomes a rule in `CLAUDE.md` — a mandated re-read, or a
fresh-session requirement for any launch after a propagation — is the Human Lead's.

## 5. Carried for the Human Lead — four items, none resolved here

| # | Item | Why it needs a ruling |
| :-- | :--- | :--- |
| **1** | **`0083` §1's "other candidate axes are all zero" needs a SCOPE.** True **on the in-frame S1/S2 slice**: 0 undated, 0 duplicate `(user, play id)`, 0 non-positive `number`. **Across the whole sweep there are 379 undated and 182 duplicate records**, none in the slice (instance B) | **A zero published without its scope reads as a zero everywhere** — the shape this chain keeps catching. It is a wording defect in `0083`, not a measurement error |
| **2** | **`0083` §2's coextensivity table is APPLY-only.** DERIV measures **1,072 / 0 / 0 / 0** at position 5 and **1,056 / 0 / 0 / 0** post-liveness (instance B) | **`CLAUDE.md`: both populations, always.** `0083` §2 states one and the standing rule requires two |
| **3** | **D9's loose-key example clusters do not match the spec's.** Measured: `secondchance` (8 strict keys), `theisland` (7), `maigret` (6). The spec names The Twilight Zone, The Traitors, Manhunt (instance A) | **The counts agree; the examples do not.** A difference in what "largest cluster" ranks by, and the spec's examples are cited in three places |
| **4** | **D3′ is not monotone in `W` between the 91 and 107 arms** — 98.81% then 98.84% on APPLY. Reproduced by both arms, unsmoothed | **Carried open since `0075`.** Step 13 is the consumer |

## 6. Scope

- **No rule change, no population change, no figure moves.** Nothing measured changed between the
  2026-08-16 and 2026-08-16-r2 runs; instance A reports its invariants JSON differing **only in build
  hashes and git HEAD**. **`0083` changed what figures are called, not what they are.**
- **Both arms reconcile**: column sets **set-equal at 89 names**, waterfalls identical on both
  populations, **703 = 604 + 99 from 216 accounts** and **99 = 0 + 99 from 73**, all eight invariants
  passing with every coverage identity holding, and **all three denominator readings present in both**.
- **Surfaces reached:** 7 (`second-brain`'s glossary bullet) and the control in `src/`. **Surfaces 1–5
  needed no edit** — the wrapped occurrences there are legitimate quotations inside withdrawal notes,
  **read before being dismissed**, per `CLAUDE.md`'s rule that a hit is not a defect until you read the
  line.
- **Zero API calls.**
- **Step 8 goes to Red Team for a third pass. The gate is OPEN.**
