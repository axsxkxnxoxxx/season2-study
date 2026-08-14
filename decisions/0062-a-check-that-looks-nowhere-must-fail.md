# Decision 0062 — a check that finds nothing because it looked nowhere must fail; one definition per statement; the qualifier propagated

| | |
| :--- | :--- |
| **Decision** | **B9:** `check_ratios_written()` skipped arm b in full and reported OK. **A missing path is now a failure, never a skip** — arm b's ratios are reached at their real location, regenerated, and `bb-b.json`'s `bound_width` corrected `0.403245 → 0.403246`. **Every allowlist and skip path in all three scripts audited** for the same shape; four more found and closed. **The generator now holds ONE definition per statement and per figure, rendered by both writers, with the two halves COMPARED off disk** — 72 figures and 8 statements, both arms. `LEGITIMATE` consulted; `ADOPTED_IN` distinguishes `.md` from `.json`; the surviving `assert` in `step7_floor_extremes.py` reported instead. **The covering qualifier propagated to all eight surfaces.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-14 |
| **Occasioned by** | Red Team's **fourteenth** Step 7 HOLD, item B9 and the four smaller items |
| **Amends** | `0060` §1 (a coverage claim true for one arm of two) |
| **Verified by** | `check_surfaces.py` **PASS**, `step7_regenerate_derived.py` **PASS**, `step7_floor_extremes.py` **11/11 CONFIRMED** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. B9 — the third control in six entries that reported clean while looking at nothing

`check_ratios_written()` did `se = doc.get("sampling_error", ...); if not se: continue`. **Arm b stores
its bootstrap under `bootstrap`, and `ABSENT_OK["b"]` allowlists `sampling_error` as legitimately
absent.** So the loop continued on both populations, **checked zero rows, and returned an empty failure
list** — which reads identically to "everything is right."

**`0060` §1's claim that "the run fails if any written quotient is not this arm's numerator over this
arm's denominator" was true for arm a only.** Arm b's four ratios were the original hand-computed
figures, never regenerated and never verified, and `bb-b.json` carried `bound_width: 0.403245` where the
adopted exact form is **0.403246**.

**Fixed three ways, and the third is the one that matters:**

1. **`RATIO_LAYOUT` declares where each arm actually stores its ratios** — `sampling_error…` for a,
   `bootstrap.by_population…` for b — so arm b is **reached**, not skipped.
2. Those paths are now **written targets**, so arm b's ratios are regenerated like everything else.
   `bound_width` is corrected.
3. **A missing path is a FAILURE, not a `continue`**, and the function additionally fails if
   `checked == 0`. **A check that looks nowhere cannot report OK**, by construction rather than by
   attention.

**Coverage now printed every run: 12 rows for arm a, 18 for arm b.**

## 2. The audit — four more of the same shape

| Where | It passed by | Now |
| :--- | :--- | :--- |
| `check_surfaces.py` — `json_numbers`, `json_strings`, `text_numbers` | `except Exception: return []`. **A file that fails to parse contributes zero numbers and the scan passes.** | Recorded in `READ_FAILURES` and **fails the run.** A file the control could not look at is not a clean file. Genuine binary is still skipped, and only for `UnicodeDecodeError` |
| `step7_regenerate_derived.py` — the input cross-check | `if u:` — an arm without `unfiltered_counts` was **skipped**, so the counts could be cross-checked against **one** arm while the docstring claimed both | Fails unless **at least one** arm cross-checked, and counts how many |
| `ABSENT_OK` | An entry that **never fires** was invisible — meaning the schema had moved under the allowlist and nothing said so | `unused_allowlist_entries()` fails the run |
| `SURFACES["7 second-brain"]` | globbed `*.md` only, so **a `.json` in that directory was outside the control entirely** | globs every file |

**The pattern is one sentence: an empty result and a clean result are the same value, and only the
control knows which it produced.** Every place that can return "nothing found" now says whether it found
nothing *or* looked at nothing.

## 3. One definition per statement and per figure

**B8 and B10 were the same literal living in two writers, one edited and one not.** Two copies of a
sentence is two places to withdraw it from, and the withdrawal reached one.

**`STATEMENTS` holds eight sentences; `figure_table()` holds 72 figures. Both writers render those two
objects and neither contains prose of its own about the figures.**

**And agreement is demonstrated, not asserted.** The `.md` half emits a `CANON` block;
`compare_halves()` reads **both rendered halves back off disk** and compares them key by key, failing on
any figure present in one and absent from the other, any value differing beyond `5e-7`, any statement-key
mismatch — **and on comparing zero figures**, which is §1's failure mode applied to the comparison
itself.

**Both arms: 72 figures, 8 statements, compared and agreeing.**

## 4. The four smaller items

- **`LEGITIMATE` was imported, printed, and never consulted** — a fourth docstring asserting a code
  property the code lacked. **Now enforced two ways:** a value cannot be both legitimate and superseded
  (a conflict fails the run), and a row that matches **nothing that occurs** is reported as `UNUSED` —
  an exemption granted against no occurrence is an exemption waiting for the wrong one.
- **`ADOPTED_IN` matched `frag in f`**, so `"bb-b"` hit `bb-b.md` and `bb-b.json` alike and "all six
  ratios report OK" did **not** establish that any was in the JSON. **It now records the extension and
  requires both.** All six report `in ['json', 'md']`.
- **`step7_floor_extremes.py`'s surviving `assert at_tau2 == 0`** — the last instance of instance A's
  D-2, in the file `0059` rewrote precisely to stop asserting conclusions. **Now a compared row with a
  verdict: 11/11 CONFIRMED.**
- **The covering qualifier reached no file an agent reads.** `0056` sharpened it and it lived only in
  `decisions/` for six entries while **Step 9 publishes the bound it qualifies.** Now on **all eight
  surfaces**: `task-sheet.md`, both `data-scientist` files, both `analytics-engineer` files, both
  operative deliverables (via `STATEMENTS`, so it cannot be edited out of one half), and the glossary.

**The qualifier, stated once:** *the bound is covering with respect to **insertion-dormancy,
exhaustively**; open only across **channel classes (D4, D9)**.* Concede every pair dormant before the
instant at which its own state-defining null is read — `τ1` for never-started, `τ2` for Continued.
**Exhaustive, not open-ended:** every pair either was inserting through its test instant or was not,
yielding `32,769` and `18,952` with **no residue**. **D4 and D9 publish alongside, never folded in.**

**The control apparatus could not have caught this**, and that is worth stating: it is numeric and
phrase-based, and **a missing qualifier is neither a wrong number nor a withdrawn claim.** Red Team found
it by grep on an idea.

## 5. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **One figure corrected** — `bb-b.json`'s `bound_width`, `0.403245 → 0.403246` — and it is the first
  arm-b figure this chain has regenerated rather than left hand-computed.
- **Zero API calls.**
- **Step 8 does not launch.**
