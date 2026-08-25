# Decision 0128 — the scratch workspace is arm-scoped; and the accommodation audit

| | |
| :--- | :--- |
| **Decision** | ***(1) THE SCRATCH WORKSPACE IS PARTITIONED PER ARM.*** **The fourth isolation channel, and the fix is the Human Lead's because no scoping the arm controls could close it** — *it did not choose the directory's contents.* ***(2) AN ACCOMMODATION AUDIT RUNS BEFORE STEP 10.*** **Each arm enumerates, for its own code and deliverables only, what it built to live with a constraint since lifted and what its artifact still claims about a limit that no longer holds.** ***A report, not a fix.*** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-25 |
| **Occasioned by** | An arm disclosing that its own working directory held another arm's filenames; and `0127` §4b–4d |
| **Status** | **FILED. The workspace is partitioned. THE AUDIT IS RUNNING AND STEP 10 IS NOT BEGUN.** |

---

## 1. The fourth channel

**An arm ran `ls -la` on its own working directory — a directory whose contents it did not choose — and
five of the other arm's filenames came back.** **It opened none, isolated its own snapshot into a
subdirectory, used only that, and reported.**

***THE WORKSPACE IS NOW PARTITIONED, NOT POLICED BY INSTRUCTION.*** Each arm writes only to
`<scratchpad>/arm_<arm>/`, **and an `ls` of that directory returns only its own files.** **141 loose
entries were archived out of the shared root.**

**A rule telling an arm not to look at what is in front of it is the weakest form of this fix** — and
it is the form each of the other three channels had to replace.

| | rule | closes |
| :--- | :--- | :--- |
| `0123` | search patterns arm-scoped **in the pattern** | how an arm **looks** |
| `0125` §5d | commit messages carry no cross-arm content | what a **log** returns |
| `0126` | a shared control emits arm-scoped output | what a **shared control** emits |
| ***`0128`*** | **the scratch workspace is partitioned** | ***what a WORKSPACE contains*** |

> ***ALL FOUR WERE FOUND THE SAME WAY — BY AN ARM REPORTING AGAINST ITSELF, AFTER THE CHANNEL HAD
> ALREADY FIRED. NONE WAS PREDICTED.***
>
> **`0126` said the list is not known in advance. It still is not.** ***The right posture is that a
> FIFTH exists and has not fired yet*** — **and that the thing which finds it will be an arm's
> disclosure, not a control.**

## 2. The accommodation audit

***`0127` §4b established that an accommodation for a constraint is a debt that comes due when the
constraint is lifted, and that no control looks for one.*** **§4c then proved the corollary within a
single ruling: the Human Lead named nine notes and two lines; the writer found three more sites,
including one it says would have stayed live had it read the count literally.**

> ***AN ENUMERATION OF ACCOMMODATION SITES MADE BY ANYONE BUT THE WRITER IS AN UNDERCOUNT.***

**So each arm is asked, about its own code and deliverables only:**

> **What did you build to live with a constraint that has since been lifted, and what does your artifact
> still claim about a limit that no longer holds?**

**The lifted constraints are NAMED so the question is answerable** — **the `ci` endpoint typing, the
frame and draw order, the per-group re-seed, the placeholder sentinel** — **and each arm is asked for
anything it knows of that the Human Lead has not named.** *(That last clause is the one that matters:
the named list is the Human Lead's, and the undercount is the Human Lead's to expect.)*

**Each arm enumerates its own. Neither enumerates the other's. Neither is asked to fix anything.**
***Arm `a`'s skip was found BY ACCIDENT, in a run authorised for something else.***

## 3. ***And the reason a report is the only instrument available***

**`0127` §4d, recorded here because it is why the audit cannot be replaced by a check:**

> ***THE NINE-OF-EIGHTEEN FILE VALIDATED EXACTLY AS CLEANLY AS THE EIGHTEEN-OF-EIGHTEEN ONE.***

**Re-running the emitter with the sign filter reintroduced emits 9 of 18, and the validator returns
`ok: true, checks_failed: 0`.** **`S41` requires both statistics to APPEAR; nothing asserts that every
MEASURED interval was published.**

> ***A SCHEMA CHECKS WHAT IS IN A FILE. NOTHING CHECKS WHAT A WRITER DECIDED NOT TO PUBLISH.***

**That is the whole case for asking rather than testing.** **A withheld measurement leaves no trace in
the artifact** — **no wrong figure for the numeric halves, no withdrawn phrase for the phrase half, no
stale hash for `S44`** — ***and the only record that it was withheld is the writer's own knowledge.***

## 3b. ***THE AUDIT RAN. BOTH ARMS FOUND THINGS NO CONTROL WOULD HAVE.***

***NEITHER ARM'S FINDINGS OVERLAP THE OTHER'S, AND NEITHER WAS FOUND BY A CONTROL.*** **Everything
below is each arm's report of its own work, verified where checkable. NOTHING IS FIXED BY THIS ENTRY.**

### The two that a check could never have reached

***AN ACCOMMODATION BAKED INTO THE CONTROL THAT VERIFIES THE ACCOMMODATION'S OUTPUT.*** One arm's
weights selftest **hardcodes the endpoint count of the nine-of-eighteen file**. Run now: **exit 1**,
`ci_objects_found: 36, endpoint_values_checked: 72, reproduced: 72, mismatches: []`. ***All 72 endpoints
reproduce and the check fails only because it was told to expect 54.*** **The sign filter was one level
down; this is the same debt sitting in the verifier.** *(And that selftest has not been run against the
completed artifacts — the newly published movement CIs have never been checked against the replicate
set.)*

***TWELVE MEASURED INTERVALS PUBLISHED NOWHERE.*** The other arm bootstrapped **three** objects per
state and published **two**. Verified: **24 endpoints of `levels_position_5_pct` appear in NONE of its
three artifacts** — they exist only under gitignored `processed/`. **No decision to withhold them is
recorded in any file.** ***And they are the quantity that speaks to the gap the arm itself publishes***
— *"the bounds and the shares are on different populations"*, with a DERIV point estimate outside its
own bound. **The position-5 level interval is the sampling uncertainty on the population the bounds
bound.** **The arm reports it as unsure whether publishing them is in Step 9's scope and does not
resolve it.**

> ***`0127` §4d SAID A SCHEMA CANNOT CHECK WHAT A WRITER DECIDED NOT TO PUBLISH. HERE IS WHAT THAT
> BOUGHT: TWELVE INTERVALS, TWENTY-FOUR ENDPOINTS, INVISIBLE TO EVERY CONTROL, FOUND ONLY BY ASKING.***

### Claims now false in published artifacts

**Four sites in one arm assert the frame and draw order are unfixed** — `0124`/`0125` fixed them; the
arm's own values comply and no figure moves. ***The worst sits under a heading reading "Divergences —
REPORTED, NOT RECONCILED", which is exactly `0127` §4c item 2*** — *"and I did not notice that the entry
immediately below it had become the same thing."* **One of the four also describes a filter the arm did
not write**: *"the 9 with non-negative endpoints"*, when the filter dropped an interval whose upper
endpoint was positive.

**And in the other arm, inherited placeholder prose is false in a non-placeholder file.** Verified:
`$.placeholder` is **`false`** while `$.notes.reading_a_placeholder` says ***"This file's flag is
true."*** A second inherited note claims the movement branch holds **a declared type fixture**; the file
holds **twelve real measurements, six negative.** ***`0127` §3 flagged that string as MOVED during the
migration and did not flag its TRUTH-VALUE*** — the arm names that as the half nobody checked.
**A third inherited block disagrees with the arm's own block four lines away about how many bootstrap
elements the spec fixes — four against seven, in one published file.**

### Second definitions, and a typed count that cannot follow its figures

**One arm types `NPOP = {"APPLY": 196654, "DERIV": 147370}` while `waterfall_block()` READS the same
figure from a structure already open in the same process.** ***They agree today***, which is precisely
*"a reconstruction that agrees today is still a second definition tomorrow"* — **and eight lines below
it, the same file reads the adopted-rule revision rather than typing it, with a comment explaining
why.** ***The same reasoning, not applied to the line above.***

**A `dtype` kwarg deviates from `0125`'s named call.** The arm **measured it inert** — spec-verbatim
redraw, bit-identical — and reported the literal deviation anyway, *"because `0125`'s whole point is
that a mechanism difference which looks inert is what survived three prior fixings."*

**A `.md` corner table silently deduplicates rows on a key that omits a column the table displays.**
Every dropped row is identical today; **two corners differing only in `Continued` would collapse and
show the reader the wrong value.**

### ***What the audit says about the audit***

**Both arms distinguished EMPTY from UNEXAMINED and said what they examined to reach it** — one
reporting **zero `999` hits across six scripts** to establish it built nothing to cope with sentinels,
the other **zero sign filters anywhere in its code**. ***Neither arm's list overlaps the other's, and
both found items outside the four constraints the Human Lead named*** — **which is the fifth clause
doing its work.**

**Three further isolation disclosures, all volunteered, none used:** a wildcard `step9*a*.*` that is
*"not arm-scoping, it is a substring"*; an `ls | grep -c` returning a **count** spanning both arms,
*"which is more than nothing"*; and one arm confirming it ran **no `git log` at all**.

## 3c. The audit's findings were ruled and closed — and closing them found more

**Both arms fixed their own only. Verified: no published figure moved in either.**

***THE TWELVE ARE PUBLISHED.*** `$.declared_intervals` 12 → **24**. **The slot was the only one
available** — every `bounds` definition is `additionalProperties: false` with no CI slot, so *a bound
cannot hold its own sampling interval* — **and the append is at the END deliberately**, because the
stamper resolves committed indices into the corrected emission and interleaving would have re-pointed
both supersession layers. **The finding is in the file:** *"NO DECISION TO WITHHOLD THEM WAS EVER MADE
OR WRITTEN… A WITHDRAWAL LEAVES A TRACE AND A DEFAULT LEAVES NONE."* **A guard now counts the 36
measured intervals and requires each in the document, shown rejecting a mutated emitter.**

***THE OVERRIDE RULE IS A CONTROL, NOT A JUDGEMENT.*** Three tests — **self-reference**,
**self-contradiction**, **spec text** — with **682 string leaves scanned, 14 tripped, 3 overridden, 10
kept, 1 kept-and-reported**, and ***a leaf that trips and carries no verdict is a HARD STOP.***
**`0127` §3's miss is recorded in the file: the migration verified that string byte-identical at the
same path and never asked whether it was TRUE.** ***Moved and true are different questions.***

***AND IT FOUND A FOURTH INHERITED LEAF THE RULING DID NOT NAME*** — `spec_choices_made_by_step_8b[25]`,
also carrying the four-element count. **Verdict `KEEP_AND_REPORT`, and the distinction is not
ownership** — both blocks are `step8b`'s — ***it is NOTE versus RECORD***: **a dated record of another
step's reasoning was true when written, and rewriting it would falsify Step 8b's record of its own
choice.** **The exemption is one path wide, carries its reason, and WITHDRAWS ITSELF — the emitter
hard-stops if that leaf ever comes to agree.**

***THE ACCOMMODATION IN THE VERIFIER IS OUT, AND SO IS EVERY OTHER TYPED COUNT IN THAT FILE.*** The
selftest now derives its anchor from **what the arm MEASURED** rather than from the publication, so
**a withholding fails on coverage rather than on a constant someone must remember to update** — the
same class the audit was called to find, closed in the instrument that missed it. **Exit 0, 12/12,
72/72 bit-exact.** **Both typed population constants became reads**, one of them **beyond the letter of
the ruling and flagged as such**: *"leaving one typed literal beside a corrected one leaves a second
definition in place for the first consumer that reaches for it."*

***THE SUPPORT IS MEASURED*** — membership 2,481 at every arm, contributing 2,422 / 2,402 / 2,423 /
2,407 / 2,422 / 2,402 — **read from the matrix the published intervals came from, with a set-membership
precondition and 10/10 discriminating substitutions rejected.**

### ***`0128` PREDICTED A FIFTH CHANNEL. IT FIRED THE SAME DAY.***

**An arm disclosed `git status --porcelain` at the repository root returning the other arm's paths.**
***"`git status` is a shared control whose output no arm-side scoping can constrain"*** — **the `0126`
class, and `0126` closed only `check_surfaces.py`.** **A second arm disclosed the same command with a
bare directory scope.** ***And one arm found the `0126` channel inside its OWN control***, which ran
`check_surfaces.py` **without `STEP_ARM`** and captured the other arm's paths into its process.

> **`0128` §1 said the right posture is that a fifth exists and has not fired yet, and that an arm's
> disclosure would be what finds it.** ***Both halves held, within the day.*** **NOT RULED HERE.**

**Two `0092` boundary cases, both flagged rather than assumed:** an arm **hand-edited an approved gate's
artifact** to place a knowingly-historical note, being the producing arm on a step that must not be
re-run; and an arm **declined to correct a string** because the file publishes a live hash asserting
which script produced it — *"editing without a stage-1 rerun would make the provenance claim false."*
**It proposes the structural fix: have the producer record its own hash at write time so the two can be
compared rather than assumed.**

## 4. Scope

- **No figure moves. No artifact is corrected by this entry.**
- **The audit is a REPORT. Anything it surfaces is ruled separately.**
- **Zero API calls. Step 10 NOT begun.**
