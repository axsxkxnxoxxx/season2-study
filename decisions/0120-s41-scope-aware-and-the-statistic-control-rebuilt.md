# Decision 0120 — S41's empty branch becomes scope-aware; Step 12 is exempt; the statistic control rebuilt, and the arm found two defects in it

| | |
| :--- | :--- |
| **Decision** | ***HUMAN LEAD RULING: `S41`'s empty branch is SCOPE-AWARE and STEP 12 IS EXEMPT from the paired-movement requirement***, on the schema's own warrant. **`S17`'s shape under F4.** **Plus `E1`, `E2`, `E3` fixed with reproduction-before-fix, and `H1`–`H5` rebuilt in `check_surfaces.py`.** ***AND THE ARM FOUND TWO DEFECTS IN MY OWN WORK, one of them inside the sentence `0118` made canonical.*** **Schema v1.6.0 → v1.7.0.** |
| **Decided by** | **Human Lead** (ruling 1); the rest implemented on `reviewer-engineering`'s v1.6.0 review |
| **Date** | 2026-08-19 |
| **Amends** | `0118` §1 and §3; `0119` §5; `task-sheet.md` Step 9 |
| **Verified by** | `check_surfaces.py` **exit 0**, 8 surfaces, 260 files; selftest **exit 0**, mutations **90 → 95**, `checks_without_force: []`; three placeholders at **41 checks, 0 failures** |
| **Status** | Open. **v1.7.0 returns to `reviewer-engineering`. Step 9 NOT begun.** |

---

## 1. RULING — Step 12 is exempt, and the exemption does not widen

***`S41`'s `not by_arm` branch was UNCONDITIONAL***, so a Step 12 arm file **doing exactly what the
schema says Step 12 does** failed it. The schema's own warrant, `step8b-output-schema.json:2075`:
*"Step 12 lists every candidate cut and **mandates intervals nowhere**."*

**The Human Lead's reasoning, recorded as given:**

> Requiring Step 12 to carry intervals would force it to **manufacture two figures it was never asked
> to compute**, one a paired movement between configurations the spec does not name — **a fabrication
> to satisfy a control, which is the defect `E1` was.** And it would make the schema's own warrant
> text false, which is **fixing a control by breaking a statement of fact.**

**`S41` joins `CHECK_SUBJECT`** so `_declare_scope_emptiness()` reaches it; the branch now reports
`EMPTY_DECLARED` with its restriction named and its coverage counted.

***THE EXEMPTION IS STEP 12's ALONE, AND IT IS DEMONSTRATED, NOT ASSERTED.*** On identical fixtures:

| step9 | step10 | step11 | step12 | step13 |
| :--- | :--- | :--- | :--- | :--- |
| **FAIL** | **FAIL** | **FAIL** | ***EMPTY_DECLARED*** | **FAIL** |

***AND THE ARM'S OWN FIRST FIXTURE HAD THE HOLE THIS TABLE EXISTS TO CLOSE.*** It derived
`must_fail` from `V.INTERVALS_NOT_MANDATED_BY_STEP` — **the table under test** — so **adding `step9`
to that table moved the expectation along with the behaviour and the selftest still exited 0.**
**That is `0111` E4's *"a table read from the file under test could only agree with itself"*, reached
through code rather than through data.** The expectation now lives in `S41_EXEMPT_BY_RULING =
{"step12"}`, **written from the ruling, not from the implementation**; widening the validator's table
drives selftest **exit 1** with `tables_agree: false`.

## 2. E1, E2, E3 — reproduced first, then rejected

***Every one was reproduced BEFORE it was fixed, and each fix shown to reject exactly the reproduced
file.*** A fix asserted to work is not a fix.

| | Reproduced | After |
| :--- | :--- | :--- |
| **E1** | A Step 9 file with `"spec_status": "unfixed_at_time_of_writing"` **and all four elements in `fields_fixed_in_spec`** validated at **41 checks, 0 failures.** `spec_status` appeared **zero times** in the validator — `S40` policed `fields_not_fixed_in_spec` **by name** and never read the field carrying the claim | **1 schema error AND `S40=FAIL`** — both layers, so the diagnosis names the retirement rather than reading *"not one of the allowed values"* |
| **E2** | `"fields_fixed_in_spec": ["statistics"]` — `B`, seed and unit silently dropped — **passed `S40`** | `S40=FAIL`, naming *"Missing from both: `['B', 'resampling_unit', 'seed']`"*. **`_partition_failures()` is written once and called at both levels** — restating it one level down would have been the second definition the finding is about |
| **E3** | S30 emitted *"these **five** keys are normalised"* and joined **four** names into it, propagated to the generator and **all three placeholders** | **`ARM_LABELS_ARITY_WORD` is derived from `len()`.** *"five keys"* now returns **0** hits across the schema, three placeholders and both modules |

**`unfixed_at_time_of_writing` is removed from the enum**, on the arm's own call and stated as such:
**`B`, the seed and the statistic are fixed for EVERY entry**, so no entry can have an empty fixed
list and the token was reachable only as a contradiction of the entry's own lists. **`partly_fixed_in_spec`
is untouched and its referent verified live** — `a_show_clustered`, whose **unit** is genuinely
unfixed by `0103` §2.

## 3. H1–H5 — the statistic control, and the mechanism `0118` credited

**`0118` §3 is corrected at two points of use.**

- ***H3. The zero-coverage guard was UNSATISFIABLE DEAD CODE.*** `cov["chars"]` was assigned only
  inside the both-blocks-found branch, where a block always holds both markers and so is never zero;
  **every other path appends to `fails` first.** `_stat_verdict()` did not model it, **so deleting
  the line would not have failed the selftest.** ***The protection was real and came from the marker
  branches, not from the line `0118` §3 points at*** — `CLAUDE.md`'s **withdrawn-mechanism class,
  inside the entry that cites it.** Replaced by `STAT_MIN_CHARS`, a floor that **can** fail.
- **H5. The four "by VALUE" tests were SUBSTRING PRESENCE tests.** *"The arms may choose between
  levels and paired movements"* satisfied one **while reversing the ruling**; `account` also matched
  *"accounts"* and *"accounted for"*, in a block `0118` §4 requires to carry prose. **Now anchored
  patterns plus `STAT_FORBIDDEN`** — because **an assertion can be undone by ADDING a sentence, which
  no positive test can see.**
- **H4.** `STAT_BEGIN` was a **prefix with no closing `-->`**, so prose naming the marker moved the
  extraction start and **swallowed arbitrary text while byte-identity still passed** — the character
  count `0118` §3 cited as coverage was the first quantity to stop meaning anything. **Both markers
  are exact strings; duplicates now fail** instead of being resolved by first-occurrence.
- **H2. THREE implementations of one rule, ALREADY DISAGREEING.** A quoted END marker made
  `check_surfaces.py` exit 1 while `step8b_selftest.py` reported ok — **two controls, opposite
  verdicts, one file.** Collapsed to `extract_block()` / `stat_verdict()`; **the arm deleted its
  `_extract_block`, `BLOCK_MUST_NAME` and its hand-typed `["levels","movements"]` and imports mine.**
  *(The fix for a duplicated-register finding had itself introduced a third register.)*
- ***H1. NOT fixed by widening byte-identity.*** `scan_statistic_declaration()` reads **two of eight
  surfaces**, and **the only defect of this class ever found — `0119` §2, `analytics-engineer{,-b}.md:583`
  — sat in files it does not open**, contradicting all four elements while both copies stayed
  byte-identical. **Four unfixity phrases registered in `WITHDRAWN_PHRASES`, which scans all eight.**
  **Probed live by reintroducing `0119` §2's text verbatim on surface 4: exit 1, phrase named with
  file and line; restoring gave exit 0.**

**Selftest 6 → 15 assertions.** ***One residual is STATED rather than asserted away:*** a pattern
cannot read a sentence, and *"not `B` = 10,000 but 4,000"* satisfies the `B` pattern. **No assertion
is written for it — an assertion that cannot fail is what H3 was.**

## 4. ***The arm found two defects in my work, and the first is in the canonical sentence***

**(a) *"ALL THREE ELEMENTS ARE NOW FIXED"* — and FOUR are listed.** In the
`BOOTSTRAP-STATISTIC` block itself, at `data-scientist{,-b}.md:243`, **and in `0118` §1 and
`task-sheet.md`.** ***This is E3's own class — a count restated instead of derived — inside the
sentence `0118` made canonical and required to be byte-identical across two files.*** Corrected to
**four** at all four sites, with the note that `0056` §159's list named **three** (`B`, seed,
statistic) because the **unit** was fixed separately by `0044`/`0103` §2. **The arm did not edit it:
it is the data-scientists' spec and must stay byte-identical. Reported, and corrected here.**

**(b) The statistic pattern was UNANCHORED.** Appending a third object — *"levels and paired
movements **and ratios**"* — **satisfied both my pattern and the arm's derived-token check, in both
copies.** ***The one probe of six that came back green when it should not have.*** **Reproduced
before fixing, anchored on the closing `**`, and the arm's probe added to the selftest.**

**Both were found by an arm reading a surface it does not own. That is now five consecutive findings
from a reading agent rather than a control.**

## 5. Three limits, assessed by the arm and agreed

- **The single-arm extension was Step 8b's INFERENCE, not the ruling.** `0118` lives in the two
  `data-scientist` files, which own Steps 6, 7, 9 and 13; **Steps 10, 11 and 12 never received the
  canonical block.** Recorded as **spec choice #29** with its ground; **the Step 12 half is recorded
  as a RULING, not a choice.**
- ***A `paired_movement_<arm>` is not a movement of anything in particular*** — and **the previous
  bullet was worse than silent**, closing with *"a movement states in `quantity` which two
  configurations it is a movement between, so the pairing is READABLE."* **`quantity` is free writer
  text.** ***A control asserted to exist.*** **Struck, with NO mitigation offered**: inventing a
  vocabulary of configurations would make every writer name a pair this schema chose.
- **`0119` §5's *"`S32` catches an arm mislabel"* is one notch too strong.** Both sides are the
  writer's own declarations, so **a COHERENT mislabel is unobservable.** `S32` catches an
  **incoherent reference**; **the coherent mislabel is the Human Lead's diff to catch.** **Corrected
  in the emitting script**, per *"if a claim is emitted by a script, the script is where it is
  withdrawn."*

## 6. Propagation — reached, and NOT reached

| Surface | State |
| :--- | :--- |
| **1 `task-sheet.md`** | **REACHED — 1 site** (the three-vs-four count). **0 occurrences of any v1.7.0-corrected schema string**, verified |
| **2–3 `data-scientist{,-b}.md`** | **REACHED — 2 sites each**: the marker restructure and the three-vs-four count. **Byte-identical, `diff` to the `name:` line alone** |
| **4–5 `analytics-engineer{,-b}.md`** | **0 occurrences of any corrected string**, verified. *(Their `:583` was corrected at `0119`.)* |
| **6 `artifacts/`** | **REACHED — 4 files regenerated.** 2 residual hits, **both read and both legitimate**: the schema names the retired token **as retired**, and `step0-access-and-setup.md:66`'s *"five keys"* is about **API record keys** |
| **7 `second-brain/`** | **0 occurrences, verified** |
| **8 `processed/`** | **0 occurrences, verified** |
| **`decisions/`** | **REACHED — `0118` §1 and §3 (3 sites), `0119` §5 (via the emitting script)** |

***THE ARM CORRECTLY REFUSED TO PROPAGATE THE RULING ITSELF.*** It reported that surfaces 1–5
carried **nothing about the S41 ruling**, that it had **no `decisions/` entry**, and that it **would
not write ruling text into a spec surface sourced only from its launch prompt.** **That is right —
a launch instruction is not a citable source — and this entry is what it was waiting for.**

## 7. Scope

- **No figure moves. No population changes. Zero API calls. Step 9 NOT begun.**
- **`read_not_typed` stays carried, out of scope by instruction.**
- **Open and unchanged: the needle register's 442 untriaged candidates.**
