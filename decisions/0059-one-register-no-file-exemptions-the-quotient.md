# Decision 0059 — the quotient is a target path, the whole-file exemption is deleted, and there is one register

| | |
| :--- | :--- |
| **Decision** | **B1:** the bound-over-sampling-width **ratio is a declared target path** — the regenerator wrote both operands and left the quotient, the exact inverse of `0057`'s failure. **B2:** the **whole-file exemption is DELETED**; a file is exempt only by name, in the source, with a reason, and **the operative pair is not exemptible**. **B3:** one register in `src/step7_register.py`, imported by both scripts, **scoped by file** where a value is right in one arm and wrong in the other. Absent target paths now **fail**. Instance A's **D-2 actioned**. `0058`'s `LIVE_ELSEWHERE` claim **withdrawn — it never fired.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **twelfth** Step 7 HOLD |
| **Amends** | `0058` §2 row 5 (a mechanism that never operated); `CLAUDE.md` `## Derived figures` |
| **Verified by** | `src/check_surfaces.py` **PASS**; `src/step7_regenerate_derived.py` **PASS**; `src/step7_floor_extremes.py` **10/10 CONFIRMED, 0 REFUTED** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. B1 — the regeneration inverted the failure it was written to end

**`CLAUDE.md` puts the bound ÷ sampling width ratio on both dependency lists. `json_targets()`
declared neither.** So the script wrote both operands into `sampling_error.*.bound_endpoints` and left
the quotient sitting between them:

| `bb-a.json` | width | own CI | was | correct |
| :--- | ---: | ---: | ---: | ---: |
| APPLY | 0.403246 | 0.7602 | **0.509** | **0.5304** |
| DERIV | 0.127570 | 0.9744 | **0.069** | **0.1309** |

`0.509 = 0.403246 / 0.7922` — **arm b's denominator, in arm a's file.** `0058` §3 said "Reverted"; it
was reverted in the entry and not in the body. **`0057` reached the ratio and missed both operands; the
regeneration reached both operands and missed the ratio.** Same class, inverted, one entry later.

**Four paths added**, started-and-left and never-started, each population, **each divided by that arm's
own denominator.** The never-started denominators are now named too (`NS_RATIO_DENOMINATORS`). ~~because `0058` §3
records that the arms were correctly left divergent there — 0.2813 against 0.27211~~ **WITHDRAWN
(`0060`): that citation was false.** `0.2813` was computed on **arm b's** convention, so the pair was
one convention on two bootstraps. **Naming the denominators was right; the reason given was not, and
naming them is what exposed it** — the script then wrote `0.2818` on arm a's own convention while every
prose surface still said `0.2813`, which is how Red Team found it.

**`bb-a.md`'s `0.5090` line is struck**, with the reason: `0.7922` is the other arm's denominator.

**And the literal is now an assertion.** `"arms_own_published_ratio_is_retained_in_place_and_marked_superseded": True`
was a hard-coded constant that nothing checked and that was false. It is replaced by
`check_ratios_written()`, which **re-reads the written file and fails the run** unless the stored
quotient is this arm's numerator over this arm's denominator.

## 2. B2 — the negative half was inert on the entire artifact set

`file_stamped = bool(re.search(r"SUPERSEDED", head))` over the first 45 lines. **`bb-a.md` line 3 is
the partial-supersession stamp**, so every number in the operative deliverable was `declared` and the
negative half could not produce one hit from it. Measured: **19 `.md` and 16 `.json` files exempted in
whole** — essentially the whole Step 7 artifact set, **including both operative deliverables.**

**So `0058` §4's "22 unlabelled values found" were closed by exempting 36 files, not by labelling 22
values.** And `CLAUDE.md` requires a string be named superseded **at the point of use** — a stamp 300
lines above a value is not the point of use. **It is the disarming recorded against `9.6830` at `0056`,
applied to files instead of strings, and it is why a wrong ratio survived a passing check.**

**Deleted.** A file is exempt only by **name, in `WHOLLY_SUPERSEDED_FILES`, with a reason** — 33 files,
each printed with its reason every run. **`step7-liveness-bb-{a,b}` are excluded from the allowlist by
construction**, in code, not by remembering.

**Then the regexes, in that order, because while the file exemption stood they were not what held the
door open.** `MARK` no longer matches `corrected`, `register`, `legitimate` or `ADOPTED`; `DECLARE` no
longer matches bare `superseded`; `CONTEXT` is **6 → 2**.

**Re-run honestly, the real count is 12**, not zero — the two B1 ratios in `bb-a.json`, three in the
verification arm's deliverable, and seven narrative lines in `second-brain`. All now fixed or marked.

**One new rule replaces the loosening it undoes.** A line carrying **both a superseded value and its
successor** is self-declaring: it is narrating the transition, which is what a record does. That is a
principled marker, unlike widening a regex until narration happens to match.

## 3. B3 — one register, scoped

Two hand-maintained registers, **already divergent by one entry after a single use**, and **neither
held the values that were wrong.** Now `src/step7_register.py`, imported by both.

**The register is scoped by file where it must be.** `0.509` is **arm b's correct figure and arm a's
wrong one**, because the arms divide by different denominators and `0058` reports rather than
reconciles that. A flat value register cannot express this — **which is exactly why `0.509` sat wrong in
arm a through two reviews.** `SUPERSEDED_IN` and `ADOPTED_IN` are keyed on `(file, value)`.

**And the positive half now covers this chain's own corrections.** `0.5304`, `0.1309`, `0.5090`,
`0.1310` were adopted by `0058` and checked by nothing. All four are in `ADOPTED_IN` and all four
report **OK**.

## 4. The three smaller ones, and one withdrawal

- **Absent target paths fail.** `put()` returned `False`, the path was printed, and the script exited 0
  — **28 declared derived figures in arm b were never written and nothing failed.** Each absent path
  must now be allowlisted **per arm with a reason** (arm b's bootstrap lives under `bootstrap`, not
  `sampling_error`; the corner table is arm a's object); anything absent and unlisted fails the run.
- **The `.md` bodies were verified by nothing.** `verify()` walked only the JSONs — and B1 lived in a
  `.md` at line 310. The regenerator now calls the checker's own `scan()` and fails on any unlabelled
  hit in either operative deliverable.
- **`f"{v:.4f}".rstrip("0")`** turned any integer-valued float into nonsense (`10.0 → "1"`). Gone with
  the local register.

**Withdrawn: `0058` §2's row 5.** It claimed a value still live anywhere **cannot** enter the superseded
list, because the list is generated. **The mechanism never fired.** `LIVE_ELSEWHERE` was compared
against a dict that never contained `0.3575` or `0.0672`, so the filter was a no-op and `_dropped` was
always empty. **They are out because they were never put in.** The property was **asserted, not
structural** — the same shape as the failures this chain has been correcting, and **Red Team found it by
reading the code rather than the claim.** Withdrawn here and in `CLAUDE.md`; the two values are now in
`LEGITIMATE` with their reading stated, which is a declaration and does not pretend to be a mechanism.

## 5. Instance A's D-2, actioned

`src/step7_floor_extremes.py` **hardcoded its own conclusions as bare asserts**, so it could confirm and
could not refute: a wrong recomputation raises `AssertionError` and reads as "the code is broken", never
as "the expected value is wrong". **Instance A flagged this itself; `0055` §5c recorded it and did not
act.**

**The expectations are now data**, compared row by row, with `CONFIRMED` / `REFUTED` printed and a
non-zero exit on any refutation. **10/10 rows CONFIRMED.**

**And the `W = 213` claim is labelled for what it is.** The script was cited as the source for it while
containing only an argument. It now carries
`"status": "ARGUED, NOT MEASURED"`, `"why_not_measured": "only W = 108 masks are on disk"`, and
`"do_not_cite_this_script_as_evidence_for_W213": true`. **The argument stands — D10 forces
`τ1 ≤ τ_pull − 91 d`, so at `W = 213` `τ2` sits at or adjacent to `τ_pull` where a mass point lies — and
it is an argument, not a measurement.**

## 6. What Red Team does not contest

**The rule, for the eighth review.** It independently checked `derive()` — the partition, both corners
to 100%, the excess identity `2·ns_x + sl_x + ch`, the one-sided widening — and calls the arithmetic
internally consistent and the open-window choice right: **at `s = τ2` the unobserved remainder is empty,
so conceding would over-widen.** It also agrees the commutation caveat belongs at Step 14 as a stated
limitation.

**Its closability distinction is adopted:** a gate **can** close over a visibly reported spec ambiguity,
and the two ratio conventions qualify. It **cannot** close over an operative deliverable that states two
different values for the same figure and does not know it. **That is B1, and B1 is fixed.**

## 7. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **No rerun and no new measurement.** Every value is a function of counts already on disk.
- **Zero API calls.**
- **Step 8 does not launch.**
