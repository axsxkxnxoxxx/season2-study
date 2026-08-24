# Decision 0126 — the ordering guard, and the third channel closed

| | |
| :--- | :--- |
| **Decision** | **Two rulings.** ***(1) The register generator re-runs the stamper's comparison READ-ONLY and HARD-STOPS on disagreement*** — arm `b` builds it, its scripts, its dependency. ***(2) `check_surfaces.py` gains an ARM-SCOPED OUTPUT MODE*** — the Human Lead's, because **an arm is directed to run it and cannot scope it.** ***The coverage number and the exit code stay whole.*** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-24 |
| **Occasioned by** | Arm `b` reporting both against itself, unprompted, in one run |
| **Status** | **FILED.** |

---

## 1. The ordering guard

***A REGISTER SHORT BY TWO ROWS IS INDISTINGUISHABLE FROM A CORRECT ONE ON A PASSING RUN.***

**That is `CLAUDE.md`'s empty-result-equals-clean-result class — but located in the DEPENDENCY BETWEEN
TWO SCRIPTS rather than inside one.** Every prior instance was a check that looked nowhere; **this is a
check that looked at a stale input and could not tell.**

***IT HAS ALREADY FIRED ONCE.*** `0125` moved the corrected emission; **the register generator re-ran
and the stamper did not**; the register reads the stamper's mark set, so it ran against a stale one and
**two rows went missing silently.** Those two values — `0.0224` and `0.0318` pp — were **superseded,
unmarked AND unregistered**: not merely unmarked, ***unpoliced.***

> ***WHERE ONE ARTIFACT IS GENERATED FROM ANOTHER'S OUTPUT, THE CONSUMER MUST BE ABLE TO DETECT THAT
> THE PRODUCER IS STALE.***
>
> ***A PIPELINE ORDER THAT IS CORRECT ONLY WHEN RUN IN ORDER IS NOT A CONTROL.***

**A convention that the scripts are run in sequence is a convention. It is not enforced, it is not
checked, and it is invisible when broken** — which is the definition this study uses for a defect
waiting.

## 2. The third channel

***`check_surfaces.py` PRINTS THE OTHER ARM'S PATHS, AND THE ARMS ARE DIRECTED TO RUN IT.***
**No scoping an arm controls can avoid it.** **Arm `b` raised it, having just been ruled on for the
`git log` case, and correctly reported rather than read.**

| | rule | closes |
| :--- | :--- | :--- |
| **`0123`** | search patterns are arm-scoped **in the pattern** | **how an arm LOOKS** |
| **`0125` §5d** | commit messages carry no cross-arm content | **what a properly-scoped LOG RETURNS** |
| ***`0126`*** | **a shared control emits arm-scoped output** | ***what a SHARED CONTROL PUTS IN FRONT OF IT*** |

***ALL THREE EXIST BECAUSE AN ARM IS FORBIDDEN TO RE-MEASURE WHAT IT IS TOLD, AND EVERY CHANNEL THAT
TELLS IT SOMETHING HAS TO BE CLOSED SEPARATELY.*** **Three channels in three rulings, each found only
when it fired.** ***The generalisation is not "close these three" — it is that the isolation rule is a
property of EVERY path into an arm's context, and the list of those paths is not known in advance.***

## 3. What the mode does, and the line it does not cross

**`STEP_ARM=a` or `STEP_ARM=b`.** The arm sees **its own paths, every shared surface, and the counts
and exit code IN FULL.** **Other arms' paths print as `<withheld: arm a path>` and their number is
reported.**

> ***THE COVERAGE NUMBER STAYS WHOLE.*** **An arm must still be able to tell a clean result from a
> looked-nowhere one.** **Suppressing the count as well would substitute THIS CONTROL'S OWN FOUNDING
> DEFECT for a leak** — and that defect has fired three times in this study.

**Nothing is excluded from the CHECK, only from the PRINTING**, and the closing line says so at every
run. **An unset `STEP_ARM` prints everything: that is the Human Lead's view.** **A value other than
`a` or `b` REFUSES TO RUN rather than guessing a scope.**

**Ownership is by NAMED FORM only** — `…-a.json`, `…-a2.md`, `src/step9_b_*`, `processed/step9/a/`.
***Deliberately not a loose match:*** `task-sheet.md`, `CLAUDE.md`, `processed/step2/frame.csv`,
`src/check_surfaces.py`, `src/step7_register.py` and `processed/step5/adopted_rule.json` are **shared
and stay visible to everyone**, and `_selftest_arm_scope()` asserts each of them is attributed to no
arm. **A scoper that hid a shared surface would break the study to fix a leak.**

**Probed in all three views on a real failure** — a withdrawn phrase planted in an arm-`a` artifact:

| view | path shown | exit |
| :--- | :--- | :--- |
| unset (Human Lead) | `artifacts/step9-headline-a.md line 252` | **1** |
| `STEP_ARM=b` | ***`<withheld: arm a path>` line 252*** | **1** |
| `STEP_ARM=a` — its own file | `artifacts/step9-headline-a.md line 252` | **1** |

***THE FAILURE IS NEVER HIDDEN FROM ANYONE. ONLY THE PATH IS.***

## 4. Until the guard is built, and after

**The arms were instructed as arm `b` behaved: if a shared control's output puts another arm's paths in
front of you, YOU HAVE NOT BREACHED — report it and do not read them.** ***That instruction stands even
now the mode exists***, because **a mode has to be switched on, and an arm that forgets is in exactly
the position arm `b` was in.**

## 5. Scope

- **No figure moves. This entry adds two controls and changes no measurement.**
- ***The `$defs/ci` percent-vs-pp typing is NOT ruled here.*** Still open, still the Human Lead's.
- **Zero API calls. Step 10 not begun.**
