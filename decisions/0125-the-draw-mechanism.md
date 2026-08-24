# Decision 0125 — the draw MECHANISM is fixed; and a spec element earns its place by determining the output

| | |
| :--- | :--- |
| **Decision** | ***THE DRAW MECHANISM IS `rng.integers` DRAWING ACCOUNT INDICES, NOT `multinomial`. WEIGHTS ARE FORMED BY COUNTING THE DRAWN INDICES.*** **`0124` fixed the frame and said one RNG seeded once with the stream consumed continuously; arm `b` satisfied that LITERALLY and still drew a different replicate set.** ***THE CHUNKING IS DELIBERATELY NOT SPECIFIED — see §3.*** **The test of completeness is bit-identical replicate sets, and it is RUN, not assumed.** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-24 |
| **Amends** | `0124`, one level lower |
| **Status** | **FILED.** **Arm `a` emits its replicate set as EVIDENCE; arm `b` reruns; the completeness test runs after both.** |

---

## 1. The ruling

**The spec names, and names only:**

1. **The generator — `numpy.random.default_rng`.**
2. **The seed — `20260818`** (`0103`).
3. **The call — `rng.integers(0, n_frame, size=(m, n_frame))`.**
4. **That weights are formed by COUNTING THE DRAWN INDICES.**

***Nothing else.***

## 2. Why one level lower was necessary

**`0124` fixed the frame and the draw order. Arm `b` implemented it literally** — one RNG at module scope, seeded once, one call, the resulting matrix shared by every group — ***and still drew a different replicate set.***

***BECAUSE `integers` AND `multinomial` ARE DIFFERENT SAMPLERS OVER THE SAME DISTRIBUTION AND CONSUME THE STREAM DIFFERENTLY.*** **Same seed, same frame, same `B`, different draws.** **Measured: `integers`-derived weights and `multinomial` weights are not equal under one seed, while both give row sums of exactly `n_frame`.** ***The distribution is right in both. The realisation is not the same.***

## 3. ***Why the CHUNKING came out of the spec***

**A first draft of this ruling named the chunking, on the reasoning that it "determines stream consumption." IT DOES NOT.** **Measured under one seed on `n_frame` = 2,481: `CHUNK` 200, `CHUNK` 500 and a single call produce ARRAYS THAT ARE IDENTICAL.**

> ***A SPEC ELEMENT EARNS ITS PLACE BY DETERMINING THE OUTPUT.***

**One that does not is **a second thing to keep in sync for nothing** — and worse, ***it makes the spec look complete in a place where completeness does not matter***, which is attention spent where no divergence can arise.

***AND IT WOULD HAVE BEEN THE SAME ERROR ONE LEVEL DOWN FROM THE ONE THIS RULING EXISTS TO FIX.*** `0124`
named a level that did not determine the draw and the divergence survived beneath it; naming the
chunking would have added a level that determines nothing at all. **Removed on measurement, not on
taste.**

## 4. ***THE FINDING: a spec is complete when two implementations agree, not when its author runs out of things to name***

***EACH RULING FIXED WHAT ITS AUTHOR COULD SEE, AND THE DIVERGENCE SURVIVED ONE LEVEL LOWER:***

| ruling | fixed | survived beneath it |
| :--- | :--- | :--- |
| **`0103`** | `B`, the **seed**, the resampling unit | the statistic |
| **`0118`** | the **statistic** — both levels and paired movements | the frame and the draw order |
| **`0124`** | the **frame** and the **draw order** | ***the draw MECHANISM*** |
| **`0125`** | the **mechanism** | ***unknown until two implementations are compared*** |

> ***A SPEC IS COMPLETE WHEN TWO IMPLEMENTATIONS PRODUCE IDENTICAL OUTPUT, NOT WHEN IT HAS NAMED
> EVERYTHING ITS AUTHOR THOUGHT OF.***
>
> ***THE REMAINING FREEDOM IS INVISIBLE UNTIL TWO IMPLEMENTATIONS TRIP OVER IT.***

**This is why the dual control is not redundancy.** **Every one of these four elements was invisible to
review** — each was idiomatic code that read correctly to anyone sharing its assumptions — **and each
became visible only as a difference between two files.** ***`0123` recorded the first divergence a
reading agent could not have found; this is the fourth consecutive one.***

## 5. The completeness test — RUN, not assumed

***THE TWO REPLICATE SETS ARE COMPARED ELEMENT-WISE AND THE RESULT IS REPORTED EITHER WAY.***

> ***IF THEY ARE NOT BIT-IDENTICAL THE SPEC IS STILL INCOMPLETE, AND THE HUMAN LEAD WANTS TO KNOW THAT
> RATHER THAN HAVE IT WORK.***

**Arm `a` emits its replicate set.** ***That is NOT a rerun of its figures and does not touch its
exemption*** — **nothing it published moves, and the emission is EVIDENCE rather than a correction.**
**Without it the completeness test compares nothing, and the test is the point.** *(Measured before
this ruling: `processed/step9/a/` held only `measured.json`; arm `a` built its indices in chunks,
counted them and kept nothing.)*

**Arm `b` reruns in place — no new supersession layer**, on `0124`'s collapse ruling.

## 5b. ***THE TEST RAN. THE SPEC IS COMPLETE ON ITS OWN TERMS.***

***THE TWO REPLICATE SETS ARE ELEMENT-WISE IDENTICAL.***

| | |
| :--- | :--- |
| **cells compared** | **24,810,000** |
| **cells differing** | ***0*** |
| replicates | 10,000, **0 differing** |
| row sums | `n_frame` = 2,481 in both |
| **uint16 C-order digest** | ***`d5c5fef3c4937cb683464dddb69adf98…` from BOTH*** |

**Compared ELEMENT-WISE on the matrices, not on the file hashes** — arm `a`'s point, adopted: *"the npz
file hash is not the right object; compression and dtype choice are STORAGE, not the draw."* **Arm `a`
stored `uint16`, arm `b` stored `int16`. The storage differs and the draw does not.**

***TWO INDEPENDENT IMPLEMENTATIONS FOLLOWING §1's FOUR NAMED ELEMENTS PRODUCED BIT-IDENTICAL REPLICATE
SETS.*** **On §4's test — *a spec is complete when two implementations produce identical output* — this
one is complete.**

***AND IT IS THE FIRST TIME IN THIS BUILD A SPEC ELEMENT HAS BEEN FIXED AND THEN DEMONSTRATED TO CLOSE
THE FREEDOM RATHER THAN ASSUMED TO.*** `0103`, `0118` and `0124` each named what their author could see
and were believed complete; **each was wrong and the divergence surfaced one level lower.** **This one
was TESTED, and the test is what makes the claim different in kind from the three before it.**

**Two supporting measurements, each taken by the arm that could take it:**

- **Arm `a`** established its emitted matrix is **the one behind its published intervals** — 72/72
  endpoints reproduced **bit-exact, tolerance NONE** — with two negative controls: a valid set at seed
  `20260819` returns **0 of 72**, and `multinomial` **at the same seed** also returns **0 of 72**.
- **Arm `b`** measured the mechanism change on its own build: `multinomial` against `integers`+count,
  **10,000 of 10,000 replicates and 17,158,682 of 24,810,000 cells differing**, both row-sum constant.
  ***The distribution is right in both; the realisation is not the same.***

**Chunk-independence was re-measured by both arms rather than cited from §3** — arm `a` at 2000 against
its emitting run's 200, arm `b` at single-call, 200 and 500 — **all bit-identical.** **`dtype` was
tested and is NOT a fifth element:** a redraw with no `dtype` kwarg is bit-identical, so the explicit
`dtype=np.int64` in arm `a`'s code is numpy's default.

## 5c. ***A CONDITIONAL MARK IS A FUNCTION OF TWO FILES***

**Human Lead ruling, 2026-08-24, correcting a premise the Human Lead had given the arm.**

> ***"Record that my premise was wrong: I told the arm the `0124` stamps point at a path and not a
> value. TRUE OF THE JSON, FALSE OF THE `.md` CELL MARKS, which are written conditionally on differing
> from the corrected emission and therefore RE-PARTITION when the corrected values move."***

**Arm `b` was instructed to verify rather than assume it, did, and found the premise false: the `.md`
stamper marks a cell IFF its value differs from the corrected emission.** When `0125` moved the
corrected values, **two W108 started-and-left width cells became superseded while unmarked** — 0.0224
→ 0.0228 pp and 0.0318 → 0.0321 pp — **and one ratio mark became superfluous**, 33× coinciding again.

***THE ARM MEASURED IT, SAW ITS STAMPER WRITE EXACTLY THOSE THREE CHANGES, REVERTED BYTE-IDENTICALLY
AND STOPPED*** rather than acting on a premise it had disproved. **That is the behaviour the rule is
for, and it is recorded as right.**

> ***THE GENERALISATION: A CONDITIONAL MARK IS A FUNCTION OF TWO FILES. WHEN EITHER MOVES, THE MARK SET
> MOVES. ANY MARK WRITTEN BY COMPARISON MUST BE RECOMPUTED WHEN EITHER SIDE CHANGES.***

**This is `0124` §5b one turn further on.** That entry established **a stamp is a CLAIM, and a claim
about what did NOT change goes stale.** ***This establishes that a claim made BY COMPARISON goes stale
when EITHER side moves — including the side that is not being corrected.***

## 5d. ***COMMIT MESSAGES ARE A CROSS-ARM LEAK VECTOR, AND THE FIX IS THE HUMAN LEAD'S***

**Arm `b` ran `git log -- src/step9_b_2_bootstrap.py` — CORRECTLY path-scoped to its own namespace —
and it returned a commit message carrying arm-`a` characterisations** (*"Arm a exit 0 (43 checks, 0
fail)…"*). ***PATH-SCOPING CANNOT PREVENT THAT.*** **The arm used none of it and measured the figure
itself — 11 structural errors on both generations — rather than adopting the "12" in that message.**

> ***HUMAN LEAD RULING, recorded as given:*** **"Commit messages are a cross-arm leak vector and the fix
> is mine. `0123`'s rule scopes search patterns; a path-scoped `git log` still returns my prose, and I
> have been writing arm-a characterisations into messages all week.**
>
> **From here: COMMIT MESSAGES STATE WHAT CHANGED AND CITE THE DECISION ENTRY. Cross-arm content — one
> arm's counts, exit codes, findings or figures — goes in `decisions/`, WHICH PASSES THROUGH MY DIFF,
> not into the log an arm can read while properly scoped."**

***HISTORY IS NOT REWRITTEN.*** **Messages before this ruling carry cross-arm content, and an arm
encountering it REPORTS RATHER THAN READS — as arm `b` did.** **That is now a rule and not a lapse on
the arm's part.**

**`0123` scoped the search PATTERN; this scopes the CONTENT of what a properly-scoped search can
return.** ***A rule that constrains only how an arm looks cannot reach what the repository puts in
front of it.***

## 6. ***The commit-qualified reference pattern is now ROUTINE***

**Each in-place re-emission leaves a set of values that existed only in a committed file since
overwritten, ***reachable only as `<commit>:<path>`***.** **`0124` recorded the pattern as a
correction to one reference** — the cross-arm diff's input at `7c94bc9:` — **and it is now the normal
case rather than the exception.**

***A BARE PATH PLUS HASH IS RESOLVABLE ONLY UNTIL SOMETHING ELSE OCCUPIES THE PATH; A COMMIT-QUALIFIED
PATH RESOLVES FOREVER.*** **Any reference to a re-emitted artifact is written commit-qualified from the
start, not amended into that form after a collision.**

## 7. Scope

- **Arm `a`'s published figures do not move. Arm `b`'s CI endpoints and CI-derived ratios move; nothing else does.**
- ***The `$defs/ci` percent-vs-pp typing is NOT ruled here.*** Still open, still the Human Lead's.
- **Zero API calls. Step 10 not begun.**
