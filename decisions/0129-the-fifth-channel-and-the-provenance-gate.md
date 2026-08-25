# Decision 0129 — the fifth channel closed; the Step 7 hand-edit stands; and a producer records its own hash

| | |
| :--- | :--- |
| **Decision** | **Three rulings.** ***(1) ANY SHARED CONTROL AN ARM RUNS WHOSE OUTPUT IT CANNOT SCOPE GETS ARM-SCOPED OUTPUT*** — `git status` included — **and a control invoking another control PASSES `STEP_ARM` THROUGH.** ***(2) THE STEP 7 HAND-EDIT STANDS***, and the disposition is recorded so it is not later read as `0092` ignored. ***(3) A PRODUCER RECORDS ITS OWN HASH AT WRITE TIME, so a consumer COMPARES rather than ASSUMES.*** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-25 |
| **Occasioned by** | Two arms disclosing the fifth channel independently, and one proposing the provenance fix |
| **Status** | **FILED.** |

---

## 1. ***The fifth channel — and `0128` predicted it***

`0128` §1 closed the workspace and said, in terms:

> ***"The right posture is that a FIFTH exists and has not fired yet — and that the thing which finds
> it will be an arm's disclosure, not a control."***

***IT FIRED THE SAME DAY, AND WAS FOUND EXACTLY AS PREDICTED.*** **`git status --porcelain` at the
repository root returns every arm's paths.** ***Two arms disclosed it independently. Neither used it.***

| | rule | closes |
| :--- | :--- | :--- |
| `0123` | search patterns arm-scoped **in the pattern** | how an arm **looks** |
| `0125` §5d | commit messages carry no cross-arm content | what a **log** returns |
| `0126` | `check_surfaces.py` emits arm-scoped output | what **one shared control** emits |
| `0128` | the scratch workspace is partitioned | what a **workspace** contains |
| ***`0129`*** | ***ANY shared control an arm runs*** | ***what EVERY such control emits*** |

***THE RULE IS NOW THE CLASS, NOT THE INSTANCE.*** **`0126` closed one control by name and the next one
was found by an arm tripping over it.** **Closing them one at a time is how a channel family is
enumerated by accident.**

**`src/arm_scoped_status.py`** wraps `git status`, **reusing `check_surfaces.arm_of` so there is ONE
definition of what an arm owns**, not two. **Probed on a real cross-arm dirty tree: each arm sees its
own path, the other's is withheld, and the total is whole in both views.** **An unrecognised `STEP_ARM`
refuses to run.**

***AND THE COUNT IS NEVER WITHHELD.*** **Hiding it would substitute the empty-result-equals-clean-result
defect for a leak** — the trade `0126` refused, refused again here.

### ***The channel reopened one level down, inside a control***

**An arm found `check_surfaces.py` invoked from its own harness WITHOUT `STEP_ARM`, capturing the other
arm's paths into its process.** ***A closed channel reopens wherever a control calls a control and
drops the scope.*** **So: a control that invokes another passes `STEP_ARM` through.**

**And the subtler form, found by the other arm in its own child process:** an invocation with **no
`env=` at all** *inherits* the variable — **so it carried when an operator happened to set it and ran
UNSCOPED when they did not.** ***An inherited scope is not a passed scope: it is a scope that works
until someone forgets.*** **Now explicit, defaulting to the arm's own.**

## 2. The Step 7 hand-edit stands — and why that is not `0092` ignored

**An arm hand-edited `artifacts/step7-liveness-bb-a.md` to place a knowingly-historical note beside
figures a reader meets there, and FLAGGED it as a `0092` deviation.**

> ***DISPOSITION: where a gate is CLOSED and a note must reach a reader of that gate's artifact, THE
> PRODUCING ARM MAY PLACE IT, AND FLAGS IT. FLAGGING IS WHAT MAKES IT LEGITIMATE.***

**`0092` reserves correction to a rerun by the producing arm. Here the producing arm is the editor, the
gate must not re-run, and the note is not a correction** — **it restates no adopted figure, cites the
gate that approved the settings and the rulings that replaced them, and says why silence would be read
two ways, both wrong.**

***THE FLAG IS THE MECHANISM, NOT A COURTESY.*** **An unflagged hand-edit of the same file is still the
defect `0092` exists to stop** — *"unsigned text in a signed deliverable."* **What distinguishes this
is that the arm declared it, so a reader can see a hand-edit was made and by whom.**

## 3. ***The provenance gate: a claim its mechanism could not deliver***

> ***AN ARTIFACT ASSERTING WHICH SCRIPT PRODUCED IT, WHERE NOTHING CHECKS THAT THE ASSERTION IS
> CURRENT, IS A CLAIM ITS MECHANISM CANNOT DELIVER.*** **That is the shape four earlier findings had.**

**The instance: a published `produced_by_script_sha256_12`, hashed LIVE from the producer, asserting
that script produced the consumer's input.** ***It becomes false the instant the producer is edited
without a rerun*** — which is why an arm deferred a correction rather than falsify it.

***AND THE PRODUCER-SIDE RECORDING ALREADY EXISTED.*** **Stage 1 already hashed its own source at write
time.** ***What was missing was the COMPARISON*** — so no rerun was needed, and the arm neither edited
stage 1 nor re-drew the bootstrap. **It also reported that moving the recording INTO the consumed file
would require a rerun AND change the producer's hash, which the new gate would then correctly
reject — and stopped on that variant rather than taking it.**

***REPRODUCED IN BOTH DIRECTIONS, AND THE FIRST IS THE ONE THAT MATTERS:***

| | |
| :--- | :--- |
| **BEFORE** | **exit 0, file written.** It published the **EDITED** script's hash beside the **UNCHANGED** input's hash. ***NOTHING OBJECTED.*** |
| **AFTER** | **exit 1**, `PROVENANCE GATE: HARD STOP → STALE PRODUCER`, ***nothing written*** |

**Four further cases, including one that exists only to prove another is not vacuous** — a redirection
to an *unmodified* copy accepted, so the perturbed copy's rejection is the perturbation and not the
redirection.

**The gate compares three things and every one is a hard stop:** recorded against live producer hash;
the manifest's `{n_frame, B, seed}` against the consumed file's own values — ***same-run corroboration
against the source, not a plausibility range*** (`0123` §3); and a third file's recorded input hashes
against those files live. **An absent manifest or key is a hard stop, never a default.**
***On disagreement the artifact is NOT re-emitted, so the stale claim is never published.***

**Carried, not closed:** **a SECOND producer records its path but not its hash**, so one published field
remains a live-hashed assertion nothing can compare. **The arm published it marked `verified: false`
with the reason, and reported that fixing it moves two published leaves and therefore awaits
authorisation.** ***It also reported two of its own new fields as literals that cannot fail*** —
unreachable when false because the hard stop fires first, **"licensed by the hard stop above them, not
by their own value."**

## 4. Scope

- **No figure moved in either arm. Verified leaf by leaf.**
- **Zero API calls. Step 10 not begun.**
