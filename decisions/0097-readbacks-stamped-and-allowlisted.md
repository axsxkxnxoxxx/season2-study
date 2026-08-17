# Decision 0097 — both Step 8 read-backs are stamped and allowlisted by name; four expired statements named

| | |
| :--- | :--- |
| **Decision** | **Both `artifacts/step8-readback-{a,b}.md` are stamped with the FOUR statements in them that have expired, and both are exempted BY NAME in `src/step7_register.py` with a reason.** A head stamp declares a file's status; **it does not exempt it** — that rule once exempted 19 `.md` and 16 `.json` files including both operative deliverables. **These are historical read-backs with no producing pipeline**, so `0092` cannot correct them by rerunning an arm. **Nothing in them is operative.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-17 |
| **Occasioned by** | Red Team's **eleventh** Step 8 pass, **F1** — and its verdict on that pass was **PROCEED** |
| **Verified by** | `check_surfaces.py` |
| **Status** | Closed. **Step 8's gate approval is drafted for the Human Lead and is UNSIGNED.** |

---

## 1. Four expired statements, named rather than corrected

Both files were written **2026-08-14** as read-backs of the spec. **Four of their observations were true then and are false now:**

| the statement | what is true |
| :--- | :--- |
| *"`processed/` is not one of `CLAUDE.md`'s **seven** propagation surfaces"* | **`CLAUDE.md` names EIGHT, and `processed/` IS surface 8** |
| *"`adopted_rule.json` publishes `analysis_population: 215,258`, `removed: 4,849`"* | that file carries a `_SUPERSEDED_FIGURES_CORRECTED_2026_08_13` block and the approved revision-6 figures; **both arms measure 18,207 / 201,900 of 220,107 against it** |
| *"`task-sheet.md` Step 7 header: NOT approved; seven Red Team HOLDs"* | **Step 7 was APPROVED 2026-08-13** (`0064`) |
| *"Step 0 still carries the superseded 403 rule"* | Step 0 carries the **classified** rule with the old form struck |

***No control can see any of them.*** They are **stale STATEMENTS built from once-true readings** —
`CLAUDE.md`'s **third blindness class**, which has no control and is recognised by what a claim *means*,
not by its digits or its text. **Eleven Red Team passes did not catch them**, and the eleventh found them
only because `0096` §1 drew a line these files sit outside.

**Named in the stamp rather than corrected**, because **these files have no producing pipeline** and
`0092` corrects a deliverable **by rerunning its arm**. There is no arm to rerun.

## 2. Why a stamp alone was not enough, and what closed it

**Red Team disputed the claim that these files were stranded between `0092` and `0096`, and it was
right.** Both already carried a hand-added `0086` status stamp, **so the precedent for a hand-applied
status stamp on these exact files existed in the files.** `0092` forbids hand-**correcting a
deliverable's content**; **declaring a non-pipeline file non-operative is not that.**

**But a stamp does not exempt a file.** `CLAUDE.md`: *"A file-level stamp declares a file's STATUS, never
its individual values. Exempting a whole file because a stamp appears in its head exempted 19 `.md` and
16 `.json` files — the entire Step 7 artifact set, including both OPERATIVE deliverables — and a wrong
ratio survived a passing check inside one."*

**So both mechanisms are applied, which is what the rule actually requires:** the **stamp** names what is
superseded, and the **allowlist entry** — by name, in `src/step7_register.py`, with a reason — exempts
the file. **`0086`'s stamp had done the first and neither had done the second.**

## 3. `0096` §1's boundary was one notch too narrow

`0096` §1 was scoped to *"a **gate deliverable**."* **`artifacts/` contains two files that are not gate
deliverables**, and the expiry-dated-assertion class survived in exactly those two.

**Red Team's own framing, and it is the right one:** *"The ruling was correct and its boundary was one
notch too narrow."* **That is a different diagnosis from the plateau it reported at the tenth pass** —
the generator was removed from the operative deliverables and persisted only where the rule did not
reach.

## 4. Scope

- **No population change, no figure moves, nothing operative touched.** **Neither arm ran**, and neither
  arm's four deliverables were edited.
- **Surfaces reached: 6** (the two stamps) and `src/` (the allowlist).
- **Zero API calls.**
- **Red Team returned PROCEED on the eleventh pass.** **Step 8 remains an UNAPPROVED gate**; the
  approval is drafted for the Human Lead and **records no approval by any agent.**
