# Decision 0061 — a withdrawn sentence was struck where humans typed it and left where the script types it

| | |
| :--- | :--- |
| **Decision** | **B8:** the withdrawn "proof" sentence is removed from **all three writers** in `src/step7_regenerate_derived.py` — the `.md` block, the `.json` `_DERIVED` field, and the source comment that gave the withdrawn claim as the reason `NS_RATIO_DENOMINATORS` exists. Regenerated and confirmed gone from all four operative files. **Both controls were structurally blind to it**, and the JSON string-field gap recorded yesterday as *"not a defect today"* **was already a defect on the day it was recorded**. The register now holds **withdrawn phrases as well as values**, checked against `.md` text and JSON strings. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Occasioned by** | Red Team's **fourteenth** Step 7 HOLD |
| **Amends** | `0060` §2 (a withdrawal that reached three of four places); `0060` §6 (a limit recorded as hypothetical while it was live) |
| **Verified by** | `check_surfaces.py` **PASS — negative, phrase and positive halves**; `step7_regenerate_derived.py` **PASS**; `step7_floor_extremes.py` **10/10 CONFIRMED** |
| **Status** | Closed. **The gate is OPEN. B9 and B10's remainder are NOT addressed here** — see §5. |

---

## 1. B8 — the withdrawal reached three of four places, and the fourth was the one that rewrites the others

`0060` §2 said the sentence was *"withdrawn in all three places it was written."* **It was withdrawn
from the three places a human had typed it, and left in the one place a script types it.**

`src/step7_regenerate_derived.py` emitted it twice per arm:

| Writer | Went to |
| :--- | :--- |
| `md_block()` | `bb-a.md:77` **and** `bb-b.md:77` |
| `apply_json()`, the `_DERIVED` `"why"` field | `bb-a.json` **and** `bb-b.json`, with the numbers |
| the source comment at `:155-157` | not to disk — it gave the withdrawn claim as the **reason `NS_RATIO_DENOMINATORS` exists** |

**So `bb-a.md` contradicted itself inside one file.** Line 77, in the block headed *"GENERATED, do not
hand-edit"* that the stamp points to as where the corrected figures live, **asserted** the sentence.
Line 316, in hand prose 240 lines lower, **struck** it. The file did not know — **and the generated
block wins on every regeneration.**

**This is the failure mode `0058` created the generator to end**, arriving from the other direction. The
generator was built because hand-patching reached one file and missed another. Here the hand-correction
reached three files and missed the generator, **which then wrote its version back over all four.** A
generated artifact is not a place you can correct by hand at all — and a withdrawal is a correction.

**All three removed.** The `.md` and `.json` writers now record that a sentence was there and was
withdrawn, with the reason, rather than restating it. The comment now gives the **real** reason the
denominators are named — an unnamed denominator is how one arm's convention quietly becomes both arms'
— and records that the justification it previously carried was false, **and that naming them is what
exposed it**: the script then wrote arm a's own `0.2818` while every prose surface still said `0.2813`.

**Confirmed after regeneration:** the phrase is gone from `bb-{a,b}.md`, from both JSONs, and from the
generator. It survives at `bb-a.md:316` **inside a strikethrough with its withdrawal note**, which is
the record and is correct.

## 2. Both controls were blind, and the gap was not hypothetical

**The `.md` form carries no numbers. The `.json` form is a string under `_DERIVED`, which `verify()`
skips by key.** The numeric halves — `json_numbers()`, `text_numbers()`, `verify()` — parse
number-shaped tokens. **A withdrawn claim is prose. Neither half can see one.**

**And this is the part worth recording plainly.** `0060` §6 recorded the JSON string-field gap as a
known limit and called it *"not a defect today."* **It was already a defect on the day it was recorded**
— B8 was live in a `.json` string under `_DERIVED` and in `.md` prose carrying no numbers, in all four
operative deliverables, at the moment the limit was written down as hypothetical. **Recording a gap as
harmless is not the same as checking whether it is**, and the entry that wrote it down did not check.

## 3. The register now holds phrases

`WITHDRAWN_PHRASES` in `src/step7_register.py`: five fragments of claims this chain has withdrawn, each
with what it asserted and where it was withdrawn. `check_surfaces.py` gains a **third half** that scans
`.md` text **and JSON string values** and reports every occurrence **not inside a strikethrough or a
withdrawal note.**

**It is not a general prose checker and does not pretend to be.** It closes one specific recurring
shape: **this chain withdraws claims about as often as it corrects figures, and until now only the
figures were checked.**

**The numeric gap is partially closed and stated as such.** A superseded **number** inside a JSON string
is still invisible to the numeric half.

## 4. The new control's first run found B10, and it is fixed

**Not in this ruling's scope — the phrase half flagged it on its first execution**, which is the
argument for the phrase half.

`md_block()` was still writing *"The arm's own published ratio is retained in place above and marked
superseded"* into both arms — **the same hard-coded literal `0059` removed from the JSON half after
finding that nothing checked it and that it was false.** Removed from the JSON, left in the `.md`:
**B8's exact shape, in the same function, one sentence apart.**

It is also false on its face for arm `b`, whose published `0.5090` is its **current** ratio, in
`ADOPTED_IN`.

**Fixed, and the real limit kept** — the denominator is the CI of the pre-widening floor point and was
not re-bootstrapped.

## 5. What is NOT fixed here, and it is a blocker

**B9 stands.** `check_ratios_written()` returns without checking anything for arm b: `bb-b.json` has no
`sampling_error` key — its bootstrap is under `bootstrap`, which `ABSENT_OK["b"]` allowlists — so the
loop `continue`s on both populations and **the denominators-stay-distinct assert never executes for arm
b either.** `0060` §1's claim that the run fails on any wrong quotient is **true for arm a only.**

**Arm b's four ratios are still the original hand-computed figures**, never regenerated and never
verified, and `bb-b.json` carries `bound_width: 0.403245` where the adopted exact form is **0.403246**.
**Half the dual implementation is uncovered.** Not addressed in this entry and not to be read as closed.

**Also outstanding, from review 14:** `LEGITIMATE` is imported and printed but never consulted in the
matching loop — a fourth docstring asserting a code property the code lacks, fail-safe in direction;
`ADOPTED_IN` matches on `frag in f`, so it cannot distinguish a `.md` hit from a `.json` hit;
`step7_floor_extremes.py:52` still **asserts** `at_tau2 == 0` rather than reporting it, in the file
`0059` rewrote to convert conclusions into compared data; and instance A's **"covering with respect to
insertion-dormancy"** qualifier reaches no spec file, no agent file, no operative deliverable and not
the glossary, while Step 9 publishes the bound it qualifies.

## 6. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **No rerun and no new figure.** Three writers, one comment, one phrase register.
- **Zero API calls.**
- **Step 8 does not launch.**
