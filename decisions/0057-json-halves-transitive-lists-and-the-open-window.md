# Decision 0057 — the JSON halves are corrected, the dependency lists close transitively, and the channel window is fixed to the open form

| | |
| :--- | :--- |
| **Decision** | **Both `.json` deliverables are corrected and re-stamped** — the machine-readable half certified the numbers the prose half withdrew. **Every superseded occurrence in `bb-{a,b}.md` is now actually marked inline**, which `0056` claimed and had not done. **The dependency lists close TRANSITIVELY** and gain four missing items. **`0.0503`, `0.3575` and `73.3466` are registered.** **The channel window is fixed to `(τ1, τ2)`, open at `τ2`** — settled by the adopted warrant, not ambiguous. **Surface 7 is the DIRECTORY.** **U2 is carried to Step 14 as measured and non-zero at three.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **tenth** Step 7 HOLD |
| **Amends** | `0056` §4 (an asserted marking not taken), `0056`'s header (surface-7 scope), `0056` §5 (list depth and membership) |
| **Propagated to — SEVEN surfaces, directory-scoped** | `task-sheet.md`; both `data-scientist` files; `artifacts/step7-liveness-bb-{a,b}.{md,json}`; **all of `.claude/agent-memory/second-brain/`, not one file in it**; `CLAUDE.md`; `specs/step7-deriv-floor-verification.md`; `src/step7_floor_extremes.py` |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-14**, which is tomorrow. Entries `0052` through `0057` all carried it, and the drift began when the session's clock advanced mid-work and the date was carried forward from an earlier entry rather than re-read. **Corrected in place across every surface, with this note, rather than silently rewritten** — the decision log is a public tracked artifact. Found by Red Team on its eleventh review; recorded at `0058` §6.

---

## 1. The JSON halves — the file certified what its own prose withdrew

**`0056` re-stamped the `.md` and not the `.json`.** Both JSONs still carried the **first** stamp,
citing `0054` and `0055` and not `0056`, and still carried `"everything_else_stands"` — **verbatim the
sentence `0056` §4 had ruled false.** Underneath it: `floor_numerator: 19042`, `width_pp: 0.050342`,
`ceiling_pct: 73.653727`, `..._over_sampling_width: 0.4703`.

**The positive half of the grep control failed outright:** `0.0961`, `73.3924` and `0.509` returned
**zero hits in both files** — the missing-figure shape the counterpart exists to catch, **in the half a
Step 9 instance parses rather than reads.**

**Fifteen values corrected in each file, listed and verified individually**, plus the DERIV sub-interval
ratio and a new explicit joint-bound ratio the arms never published:

| | `bb-a` | `bb-b` |
| :--- | :--- | :--- |
| S&L floor, APPLY | `19042 → 18952`, `9.682997 → 9.637231` | same |
| S&L floor, DERIV | `16744 → 16655`, `11.361878 → 11.301486` | same |
| sub-interval width, APPLY | `0.050342 → 0.096108` | `0.050342 → 0.096108` |
| bound width, APPLY / DERIV | `0.357481 → 0.403245` / `0.067178 → 0.127570` | same |
| Continued ceiling, APPLY / DERIV | `73.653727 → 73.699493` / `82.432653 → 82.493045` | same |
| bound ÷ sampling width | `0.4703 → 0.509` | ratio `0.0635 → 0.1213` (sub-interval), **new** `..._JOINT_BOUND` = `0.509` APPLY / `0.131` DERIV |

**What deliberately did NOT move, and this is the trap the fix had to avoid.** `19042` also appears as
`outcome_shares.APPLY.under_the_rule.counts.started_and_left`, in `waterfall.APPLY_final_states` and in
`ordering_commutation_check` — **that is the post-liveness POINT ESTIMATE, not the bound floor, and it
is correct.** A value-wide substitution would have corrupted three point estimates and the commutation
check. **The patch matched on key as well as value**, and the surviving `19042` occurrences were
inspected line by line. **The new stamp says so explicitly**, so the next reader does not "fix" them.

## 2. The inline marking `0056` asserted and had not done

`0056`'s stamp said *"Every occurrence below is superseded, and each is marked inline."* **False in both
files, and Red Team named the worst two:** `bb-a.md:219` was headed **OPERATIVE** four lines above the
withdrawn floor, and `bb-b.md:216` read *"Recommendation for the gate, not a decision: publish (ii)
[9.6830%, 10.0405%] as the bound"* — **the withdrawn non-covering bound, presented as the arm's
recommendation, in the file the gate reads.**

**That is the fourth asserted-but-not-taken action in three entries** — after `0052` §6's
specification, `0055` §5a's stamp and `0055` §5c's register row — **and this one was inside the
correction for the third.**

**Now actually done**, row by row: the OPERATIVE heading struck, both bound-table rows and the DERIV
line marked, the corner table, the Continued block, the two readings table, the recommendation, the
per-`W` floor series, and the width-ratio sentence.

**And the claim is now bounded rather than universal.** **Two strings below are legitimate and are
deliberately NOT marked:** `0.0672%` and `0.3575%` as **shares of population** — `99 / 147,370` and
`703 / 196,654`. The stamp names them. **A blanket "everything below is superseded" would have been
false in the other direction**, which is how the first stamp failed.

## 3. The lists close transitively, and gain four items

**`0056`'s lists were one hop deep, and the gap had already bitten.** Started-and-left floor item 4 was
"the Continued ceiling" — and the Continued ceiling's own list carries the **three-ceiling sum** and the
**excess count**. `1,307 / 100.6646%` left live in both `data-scientist` files **was propagation failure
#16, the one `0056` called "the severe one."** **It is two hops from the floor. The list written to
prevent #16's class did not reach #16.**

**`CLAUDE.md` now says the lists close to fixpoint**: when an endpoint moves, check its list, and the
list of every figure on that list.

**Four items added, taking the started-and-left floor from four to eight:** the **bound width itself**
(item 3 named the ratio but not its numerator, and the width has the longest defect history in the
study); the **sub-interval ÷ sampling width** ratio, second-order off the sub-interval; the **per-`W`
sensitivity series**, eight figures per population with **Step 13 as consumer**; and **any ratio between
two widths** — `bb-b.md`'s *"a factor of 7 (0.0503 vs 0.3575)"* is **4.2** under the adopted figures.
Never-started goes from three to four with the bound width.

## 4. Three strings registered, and why the omission was systematic

`0056` corrected four derived figures and registered **one**. **`0.0503`, `0.3575` and `73.3466` got no
row — and those three are precisely the strings that were still live and unmarked.** The register is the
operational half of the grep control, so an unregistered string is one the control will not flag.

`CLAUDE.md` now carries the general rule: **register every superseded value a move creates, not only the
one that prompted the correction.**

| String | Legitimate reading | Superseded reading |
| :--- | :--- | :--- |
| **`0.0503`** | **none** | the sub-interval width — it is **0.0961 pp** |
| **`0.3575`** | `703 / 196,654` = 0.3575%, the APPLY exclusion **share of population** | the bound **width** — it is **0.4032 pp**. *Same string, two meanings, one live* |
| **`73.3466`** | **none** | the Continued value in the corner floor row — it is **73.3924%** |

## 5. The channel window is fixed to the open form — it was settled, not ambiguous

**Carried as "unspecified" through four reviews. Red Team is right that the adopted warrant decides
it**, and the argument is short enough that carrying it was the error:

**A pair is conceded because, silent from insertion instant `s`, it could have generated Continued
evidence in the unobserved remainder `(s, τ2)`. At `s = τ2` that remainder is EMPTY** — nothing
admissible is missing, so the pair must **not** be conceded. **The scope statement adopted at `0056` §9
gives the same answer by a second route:** *dormant **before** the instant at which its own
state-defining null is read* — a pair inserting **at** `τ2` was not dormant before `τ2`.

**So `(τ1, τ2]` was wrong, not ambiguous, and it erred by conceding a pair with zero unobserved
remainder — past what admissibility licenses**, which is exactly the overreach the floor may not commit.

**Fixed now rather than at Step 13, for a reason that does not depend on taste.** Both arms measured the
two forms inert at `W = 108`. **That does not transfer.** D10 forces `τ1 ≤ τ_pull − 91 days`, so at
`W = 213` the surviving tail has **`τ2` at or adjacent to `τ_pull`** — and `τ_pull` is where a **mass
point in last-insertion instants** sits. **Inertness was measured against an interior boundary; at 213
the boundary is the data's own edge.**

**`src/step7_floor_extremes.py` now computes the open form and ASSERTS the inertness rather than
assuming it** — zero pairs sit exactly at `τ2` at `W = 108`, and every figure is unchanged: channel 90 /
89, floors 18,952 / 16,655, Continued ceilings 144,933 / 121,570. **The assert is written to fail at any
arm where it stops being inert.**

## 6. Surface 7 is the directory

**`0056`'s header propagated to "`second-brain`'s glossary."** `CLAUDE.md` defines surface 7 as
`.claude/agent-memory/second-brain/` — **the directory.** The glossary was corrected;
`open-items-and-contradictions.md` was not, and it carried:

> S&L bound, WIDENED: [9.6372%, 10.0405%] ✓ … **Conditional sub-interval width 0.0503 pp = 99/196,654 ✓**

**The corrected bound and its withdrawn sub-interval one line apart, both blessed with a check mark**,
and `99/196,654` is the exact claim `0056` §1 refuted. **A propagation was scoped to a file and reported
as a surface.** Corrected, and `0056`'s header is amended in place to say so.

## 7. U2 to Step 14 — measured and non-zero at three

**All eighteen numbered propagation failures were found on surfaces 1–5**, because those were the only
surfaces checked. **6 and 7 were added after the count was fixed**, and their failure rate was recorded
as *"unmeasured, not zero."*

**It is now measured and non-zero at three:** **#19**, the stamp that certified superseded figures, found
**inside the fix added for surface 6**; **#20**, both `.json` halves left behind while the `.md` halves
were corrected; **#21**, `open-items-and-contradictions.md`'s blessed sub-interval.

**The count is not renumbered — 18 is a true count of surfaces 1–5 — but it must never be published as a
total**, which is how it reads without the bullet now in Step 14.

## 8. Scope

- **No rule change.** ALT-BROAD stands, silence anchored at `τ1`. **The window fix is a boundary form,
  not a rule change**, and is measured inert at the adopted arm.
- **No rerun.** Fifteen values per JSON, one stamp, the inline marking, four list items, three register
  rows, one boundary character, one scope correction.
- **Zero API calls.**
- **Step 8 does not launch.**
