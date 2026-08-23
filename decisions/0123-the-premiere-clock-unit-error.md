# Decision 0123 — the premiere-clock unit error; why two vacuous preconditions passed on a wrong vector; and the first divergence a reading agent could not have found

| | |
| :--- | :--- |
| **Decision** | **Arm `b`'s `W91_s2_premiere` premiere-clock vector was wrong in ALL 278,452 entries by a factor of 1000** — a **unit** error, `10 ** 9` against a `datetime64[us, UTC]` dtype. **The premiere term was inert: `T0'` equalled the S1 completion date on 193,940 of the 196,654 retained APPLY pairs.** ***BOTH PRECONDITIONS GUARDING IT PASSED, AND COULD NOT HAVE FAILED.*** **Corrected by the producing arm; the superseded figures are STAMPED, NOT DELETED.** **An isolation lapse is logged with the arm's own account.** |
| **Found by** | ***Arm `b`, on its own code, on the Human Lead's question*** |
| **Date** | 2026-08-23 |
| **Amends** | `artifacts/step9-headline-b.json` and `artifacts/step9-working-figures-b.json` at `c790f3a`, `W91_s2_premiere` only; both `data-scientist` files |
| **Status** | **FILED 2026-08-23 and PROPAGATED** — §9. **The `$defs/ci` percent-vs-pp typing is NOT ruled here and remains the Human Lead's.** |

---

## 1. The defect

```python
prem_epoch = (prem.astype("int64") // 10 ** 9).reindex(arms.pair_show).to_numpy().astype(np.int64)
#                                    ^^^^^^^
```

**`10 ** 9` assumes `datetime64[ns]`. Measured, `prem` is `datetime64[us, UTC]`** — pandas 3.0.5 returns microsecond resolution — **so the divisor for seconds is `10 ** 6`, and every value is epoch-seconds ÷ 1000.**

**Measured consequences, by the arm, on its own data:**

- `prem_epoch` spans **1970-01-01T06:05:45 to 1970-01-21T10:23:31**; correct span 1970-09-12 to 2025-12-11; **`(prem_epoch == correct).sum()` = 0.** **1,138 distinct premiere dates collapse onto 18 calendar days.**
- ***The premiere term is INERT.*** `t0_prem = np.maximum(prem_epoch, s1_date)`, and the largest wrong value is 1,765,411 s — below essentially every real `s1_date`. **`T0' == s1_date` on 217,385 of 278,452 pairs, and on 193,940 of the 196,654 in APPLY (98.6%).** **The premiere-anchored arm was, as computed, anchored on the S1 completion date alone.**
- Where the premiere term *did* win the max — 61,067 pairs, 2,714 in APPLY — **it won only because `s1_date` was 0 or the year-0001 sentinel**, substituting a January-1970 `T0'`.

## 2. ***Why nothing caught it: both guards were vacuous***

`premiere_arm_preconditions` carried `t0_is_earlier_or_equal_for_every_pair` and
`tau2_observable_on_every_retained_pair_{APPLY,DERIV}`. **All three were `true`.**

***THEY WERE GUARANTEED BY `T0' ≈ 0` AND COULD NOT HAVE FAILED.*** A `T0'` in January 1970 is earlier
than every finale date, and a `τ2` computed from it is observable before every `τ_pull`. **The wronger
the vector, the more certainly they pass.** **Demonstrated, not argued: the reproduction ran the
removed preconditions against the defective vector on disk and all three returned `true`.**

**And `pairs_where_t0_moves: 87,441` was not measuring what its name says** — with the premiere term
inert it counted *"finale date later than S1 completion"*, a fact about the **finale** clock.

***This is `CLAUDE.md`'s "a control asserted to exist is not a control", in its worst form: not a check
that never fires, but a check whose passing is CAUSED by the defect it is supposed to detect.***

## 3. ***The arm's own DEF-A / DEF-B scoring, and why a calendar window is not a check***

Asked to count implausible entries, the arm **defined plausibility before counting and then scored
four definitions**, because the choice was load-bearing:

| def | rule | implausible |
| :--- | :--- | :--- |
| **A** | value ∈ **the frame's true premiere epoch-seconds** | ***278,452 — every entry*** |
| **B** | `0 ≤ v ≤ τ_pull` — **a calendar window** | ***0*** |
| C | midnight-aligned, `v % 86400 == 0` | 278,170 |
| D | within `[min, max]` of the true premiere epoch-seconds | 278,452 |

> ***"DEF-B is exactly why I did not use a calendar window: every value lands inside
> `[1970-01-01, τ_pull]` and A WINDOW CHECK PASSES CLEAN ON A VECTOR THAT IS WRONG IN EVERY ENTRY."***

**A range check tests that a number is not absurd. It cannot test that a number is the RIGHT one.**
**Set membership against the source can.** ***The adopted replacement is the DEF-A shape*** — the epoch
values compared against the frame's true premiere dates — **and the Human Lead ruled the replacement
must be a check that FAILS on the wrong vector.**

## 4. The fix, and why the divisor is not a constant

***THE RESOLUTION IS DERIVED FROM THE DTYPE, NOT ASSUMED.*** `src/step9_b_0_clock.py`:
`resolution_of()` reads the unit off the dtype and **hard-stops on an unrecognised resolution rather
than defaulting**; `epoch_seconds()` **cross-checks elementwise against numpy's unit-declared cast**,
reaching the same seconds by a different route, **so a wrong tick rate cannot survive both.**

***`10 ** 6` appears nowhere as a divisor.*** **Replacing one hardcoded constant with another would
have been the same defect with a different number**, and a pandas version change could reintroduce it.

**Also fixed:** `arms.t0` is restored in `try/finally`, asserted twice — it had been mutated and never
restored, so any later `run()` in that module would have been silently premiere-clocked.

**Reproduction before fix, as required:** the corrected check **rejects the vector on disk** —
*"1138 of 1138 rows disagree with the frame; first mismatch decoded `1970-01-14` against frame
`2005-09-20`"* — and **accepts the corrected vector**, 0 mismatches on 279,590 rows.

## 5. What moved, and what did not

**148 numeric leaves moved, all inside `W91_s2_premiere`.** APPLY never-started **42.7682% →
18.1507%**; started-and-left **6.6628% → 13.1468%**; continued **50.5690% → 68.7026%**; exclusions
**160 → 606**; three-ceiling excess **320 → 1,213**. DERIV never-started **40.0725% → 7.9974%**.
**One movement changed sign class**, so its `movement_sign_stable` goes **true → false**.

***`W108_s2_finale` did NOT move, verified rather than assumed:*** **664 leaves under `arms[0]` and 102
across `declared_intervals[0..5]`, ZERO differing**, bootstrap endpoints included — it is computed
before the mutation and the seed is fixed. **The harness control re-ran and agrees on all 13 Step 8
values.**

**STAMPED, NOT DELETED.** Human Lead ruling: the superseded figures **were correctly produced under a
defective vector, and the record of what the defect produced is the evidence for the finding.** Marked
at each point of use, with the corrected emission published beside them.

## 6. The isolation lapse — logged, not fatal

**Arm `b` self-reported TWO lapses, both unprompted.** (i) a `grep` scoped `src/*.py` returned a
single line from `src/step9_a_2_emit.py`; (ii) `ls artifacts/ | grep -i 'step9'` — a bare directory —
returned **three arm-`a` filenames**. **It opened no file in either case and nothing from them
informed any figure.** *(A third, `ls -la logs/ | grep -i step9_b`, it reported later: the scoping was
in the filter rather than in the pattern, and only its own filenames reached it.)*

***Same disposition for all of them: logged, not fatal.*** **And a timing fact, recorded because it is
a fact and NOT because the arm offered it as mitigation — it did not:** **lapse (ii) preceded the
scoping rule reaching that arm's definition file.** The rule below was written after it.

***THE HUMAN LEAD'S RULING, RECORDED AS GIVEN:***

> **The arm disclosed a breach that would have been undetectable had it stayed silent, and that is
> what the rule exists to produce.**
>
> ***I did not treat the agreement with arm `a` as evidence the run was clean — that reasoning is
> circular and is not the ground for accepting it.***

**That second sentence is the load-bearing one.** *"The arms agree, so the breach was harmless"*
**assumes what the diff is for.** A breach that imported the other arm's figure would produce
agreement — **so agreement cannot be the test of whether one occurred.** The ground for accepting the
run is **the disclosure plus the arm's account of scope**, not the numbers.

***The fix is structural: a namespace-wide search IS a read.*** A `grep`/`glob`/`find` over `src/*.py`
or the repo root **returns the other arm's lines into context without opening one of its files** —
which is why it can be written by accident and why the file-level rule missed it. **Both
`data-scientist` files now require every search pattern to be scoped to the arm's own namespace before
it runs**, with shared spec exempt, and **the block is byte-identical across the two.**

## 6b. ***The episode's own shape recurred INSIDE the correction for it***

***The corrected emission asserted a check that no longer existed.*** `$.arms[1].note` and §9 of the
`.md` continued to state the un-re-censored row set was **"CHECKED rather than assumed: `T0' <= T0`
holds for every pair"** — **while the boolean that checked it had been removed, as vacuous, by the
correction itself.** **The arm found this against its own work and published it as an open defect
rather than quietly rewriting the prose.**

***HUMAN LEAD RULING:*** **either recompute it non-vacuously or strike the claim.** ***"Do not soften
the sentence — a claim of having checked is either TRUE or it is REMOVED."***

**The arm recomputed rather than struck**, on the ground that the sentence is **the entire warrant**
for running the premiere arm on the adopted arm's position-5 rows, and *"striking it would leave the
file making a population choice with no stated ground."* The replacement, `T0PRIME-ORDER`, raises
rather than returning a flag, and has three parts — **reconstruction** of `T0'` against the frame's own
premiere **strings**, so the truth side never passes through the epoch conversion; **the ordering**;
and **the consequence** on `τ2`.

***AND THE ARM MEASURED WHICH PART CARRIES THE FAILABILITY, RATHER THAN ASSERTING IT.*** On the
defective vector: **rejected at part 1, 155,556 of 278,452 pairs** — *"`T0'` decodes to 1970-01-17,
reconstruction says 2014-09-23, frame premiere 2014-09-23."* **And part 2 run alone on that same
vector returns `True`**, recorded beside it. ***Part 2 IS the removed boolean; part 1 is the half that
can fail.*** On the corrected vector: accepted, 900,928 rows, 0 mismatches.

***That a vacuous warrant survived into the correction for a vacuous warrant is the finding, not an
embarrassment.*** **The class does not announce itself** — which is §2 restated one level in.

## 6c. The stamping, the merge, and the register

**`0123` disposes of three consequences, all ruled by the Human Lead:**

**(a) STAMP, DO NOT DELETE — and the `.md` stamping stands.** The superseded figures **were correctly
produced under a defective vector, and the record of what the defect produced is the evidence for the
finding.** Marked at the point of use: **197 fields in the headline JSON, 50 in the working-figures
extract, 36 lines in the `.md`.** ***The Human Lead extended it to the `.md`:*** *"Leaving 36 unmarked
superseded lines beside a corrected emission publishes the thing the stamping prevents."*
**`W108_s2_finale` carries ZERO marks** — verified against `c790f3a`, 664 leaves under `arms[0]` and
102 across `declared_intervals[0..5]`, **0 differing.** **Marking it would assert a defect that is not
there.**

**(b) The glob collision.** Both documents carried `document_scope.arm = "b"`, so a Step 13b glob would
read the superseded and corrected files as **two arms**. ***The arm was right that an arm does not
decide what the merge reads*** — so it added a distinguishing instance value,
`step9-b-corrected-2026-08-21`, and **rewrote its own note that had said which file 13b "should take."**
***The merge's input contract names which it takes, and Step 13b is the Human Lead's to write.***

**(c) The register gap was the Human Lead's, and closing it found two more things.** None of the
superseded premiere figures was in `src/step7_register.py`, so **`check_surfaces.py` passed because it
never looked for them.** **81 live `(file, value)` rows added**, each verified to occur in its file
before being written — *a row that matches nothing is inert.* **Probed both directions:**
reintroducing `42.768227` unmarked on `task-sheet.md` drives **exit 1**; with the open rows isolated,
the negative half returns **0** hits.

> ***SEVEN SUPERSEDED VALUES ARE DELIBERATELY UNREGISTERED AND ARE THEREFORE UNPOLICED:*** 41, 52, 83,
> 104, 108, 160, 320. **Measured collisions: `108` occurs 644 times across 123 files — it is `W`; `52`
> occurs 219 times; `41` occurs 52 times.** Registering them would flag hundreds of correct readings
> and the register would be withdrawn within a day. ***Stated as a gap rather than left silent.***

***AND THE LIVE REGISTER IMMEDIATELY FOUND TWO DEFECTS NOTHING ELSE HAD:***

1. ***A false positive in the checker itself, mine.*** 14 correctly-stamped leaves reported as
   unmarked, because `stamped_field_paths()` read only **same-level** sibling strings and arm `b`'s
   working-figures stamps sit **one level down**, in a `_superseded` object. **The checker's own blind
   spot, found by running a live register against real stamps.** Fixed; those 14 now resolve.
2. ***A misclassification in the stamping, arm `b`'s — RULED AND CLOSED, §6d.*** 12 paths flagged:
   `denominator_pairs` and `on_population_n` in all six premiere shares blocks. ***They are the
   POST-LIVENESS denominators, this arm's own output, and they moved*** — 196,494 → 196,048 and
   147,318 → 147,297.

## 6d. ***The classification rule, named because the instance was not the defect***

**Human Lead ruling, 2026-08-23: arm `b` re-stamps the 12** — *"Mark them as superseded at their points
of use, pointing at the corrected values, same form as the other 197."* **Done: 12 marks, verified with
`check_surfaces.py`'s OWN exemption reader rather than the arm's, 12/12 covered. `check_surfaces.py`
now exits 0, and the register rows still fire** — probed both ways: **stripping the two names from one
stamp drives exit 1 at exactly those paths; writing `196,494` into an unstamped region drives exit 1
there.** ***The row still fires; the stamp is what silences it.***

***BUT THE INSTANCE WAS NOT THE DEFECT.*** The stamper keyed `NOT_THIS_ARMS_OUTPUT` on **the last path
component alone**, so `denominator_pairs` was excluded **by name, in both of its readings** — and it has
two. **Under `bounds` it is 196,654: Step 8's position-5 population, consumed unchanged, correctly
unmarked. Under `shares` it is the post-liveness denominator, which moved.** ***The same name, in one
file, four levels apart, meaning two different things.***

***THE RULE THE HUMAN LEAD NAMED:***

> ***A figure is Step 8's ONLY IF THIS ARM CONSUMED IT WITHOUT RECOMPUTING IT. Anything downstream of
> this arm's own liveness filter is THIS ARM'S, whatever it was derived from.***

**Recorded where the classifier reads it — at the branch, in `classify_numeric()`, not in a docstring
away from it.** ***And it is not enforced by a list:*** a population size counts as Step 8's **only when
it still holds Step 8's figure**, compared against the `n_position_5` declared on its own enclosing
`headline.<POPULATION>` and **read from the file** — *"a hardcoded 196654 would be a second definition
of Step 8's figure inside this arm."* **No enclosing population is a hard stop, not a default.**

**`n_position_5` and `n_post_liveness` sat side by side and were classified alike.** ***That adjacency
is why the call looked safe, and it is the whole lesson: a field NAME cannot answer whether this arm
recomputed the figure.***

## 6e. Two more, both found by acting on the ruling

***(i) THE COMMITTED ARTIFACT WAS NOT THE COMMITTED GENERATOR'S OUTPUT.*** Replaying `7c94bc9`'s
stamper against the pre-stamp file yields **200 marks; the committed file carried 197.** The three
missing were **string** marks the numeric half cannot see. ***This is `0093`'s artifacts-lag-the-ruling
window occurring INSIDE A SINGLE ARM, between one of its own runs and the next.*** The arm made its
stamper **regenerative** — strip and rebuild — rather than skip-if-token-present, *"which is the
mechanism that let a grown field list go unwritten."*

***(ii) A `[` IN A STAMPED FIELD NAME VOIDED THE ENTIRE STAMP — my control, reported by the arm.***
`STAMP_FIELDS` excluded `[` and `]` and terminated on a bare `]`, so a name like
`spec_choices_this_arm_made[0]` **made the whole match fail and dropped every other name in that stamp
with it.** ***The failure surfaces as a fresh exit-1 row on an UNRELATED figure — it reads like a false
positive rather than like a voided stamp.*** **The arm worked around it inside its own namespace and
correctly did not edit the shared control; the fix is mine and is done**, indices accepted, terminator
now `]` followed by whitespace or end, probed on all three forms.

***Both of these were found only because the register was made live and then acted on.*** **A register
that had stayed empty would have left all four defects — the 12, the 3, the voided stamp and the
nested-stamp blind spot — invisible and passing.**

## 7. ***What this episode is: the first divergence a reading agent could not have found***

***EVERY PRIOR DIVERGENCE IN THIS BUILD WAS CAUGHT BY SOMEONE READING.*** The stale arm keys, the
borrowed ground, the four-versus-five key count, `0118`'s grep that never ran, the version bump that
reached one identifier — **all of them were visible in the text to a sufficiently careful reader.**

***THIS ONE WAS NOT.*** The line is idiomatic. `// 10 ** 9` is what one writes for nanoseconds and
reads correctly to anyone who assumes the dtype it assumes. **Nothing on the surface is wrong.** The
defect lives in **a property of the data that the code never interrogates**, and the artifacts it
produced are **internally consistent** — the arm's re-run reproduced its own published values exactly,
*"consistently wrong, not divergent."*

***It required two implementations to trip over it.*** **A 42.77% never-started share against 18.15%
at the same arm is not a figure a reader can adjudicate** — both are plausible, both are
internally coherent, and neither file contains the other's. **The dual control did the thing it exists
for, and it is the first time in this build that it, rather than a reader, was the mechanism.**

***AND THE VACUOUS PRECONDITIONS ARE WHY NOTHING ELSE COULD.*** **A guard that cannot fail is worse
than no guard**, because it occupies the slot where a real one would sit. Had either precondition been
DEF-A-shaped, the arm would have hard-stopped at its own first run and there would have been no
divergence to diff. **The dual control caught what the arm's own controls were built not to see.**

## 8. Scope

- **`W108_s2_finale` is untouched. No other arm and no other step is affected by this entry.**
- ***The `$defs/ci` percent-vs-pp typing is NOT ruled here.*** Arm `b`'s corrected file still fails
  structurally on negative paired movements, **12 errors → 11 only because one endpoint turned
  positive.** **Nothing was dropped, rescaled or sign-flipped. That ruling remains the Human Lead's.**
- **Zero API calls. Step 10 not begun.**
