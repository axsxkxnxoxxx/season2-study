# Step 5: Contamination Diagnostics

**Owner:** Analytics Engineer. **Mode:** GATE.
**Status: RULED ON by the Human Lead. This revision records the ADOPTED rule.**
**Revision 3, 2026-08-12.** Revision 1 proposed; revision 2 corrected after Red Team **HOLD**;
this revision records what was adopted. **Red Team reviews this revision next.**

One conflict between two adoptions is **reported and not resolved** (§11). One open question of
implementation follows from it. Steps 6 and 7 remain blocked until those are settled.

Counts and shares only. Everything keyed to an account stays in `processed/step5/`.

---

## 0. The governing principle

In the Human Lead's words:

> **Timestamp accuracy is not a concern for this study. The outcome is whether someone watched
> season 2, not when.**

> **The never-started definition holds throughout. Pairs are removed only where they cannot be
> evaluated against it, not because their timestamps are untidy.**

Every exclusion below is justified against that sentence or dropped. It reverses the direction this
step had been travelling: revisions 1 and 2 both proposed to delete pairs because their timestamps
were fabricated. The ruling says fabricated timestamps only matter where they change an answer, and
for a pair that demonstrably watched S2 they do not.

**Consequence, stated plainly:** the adopted rule removes **1.6% to 2.2%** of the population.
Revision 1 proposed 32.4% and revision 2 proposed 11.2%. Both were answering the wrong question.

---

## 1. The adopted rule and what it retains

| | Pairs |
| :--- | ---: |
| S1-completer pairs in the frame | 220,107 |
| **Excluded: contaminated `T0`, no S2 evidence** (adoption 2) | **1,542** |
| **Excluded: future-dated records** (adoption 3) | **0 to 3,307 — reading-dependent, §11** |
| **RETAINED, analysis population** | **215,258 to 218,565 (97.80% - 99.30%)** |
| **W estimation sample** (Ruling 1, §12) | **128,099 — identical under every reading** |

Deliberately retained, per adoption 1:

| Retained despite contamination | Pairs |
| :--- | ---: |
| Contaminated `T0`, but has S2 evidence | **23,067** |
| Entire S2 evidence air-date-stamped | **16,665** |
| First S2 watch contaminated in some class | 40,720 |

**Rejected:** P2 (air-date pairs), Layer 4 (throughput accounts). **Withdrawn:** Layer 3, under
ruling 2. **Costed and not taken:** Layer 2, the 24,609.

---

## 2. Revision history

| | Rev 1 | Rev 2 | **Rev 3 (adopted)** |
| :--- | ---: | ---: | ---: |
| Operative exclusion | 71,235 (32.4%) | 24,609 (11.2%) | **1,542 + adoption 3** |
| Retained | 148,872 | 195,498 | **215,258 - 218,565** |
| Object audited | S1 completion instant | binding term of `T0` | binding term, then **evaluability** |

Red Team's three blocking findings against revision 1 were all verified and all upheld; the
corrections they forced (B1's `max()` absorption, B2's restored P2, B3's committed throughput code,
C1's density correction, C2's circularity, C5's ordering contamination) stand in this revision and
are what made the Human Lead's ruling computable. The diagnostics in §3-§8 are unchanged.

---

## 3. The instrument

`watched_at` cannot audit `watched_at`. An import rewrites that field wholesale. The Trakt play `id`
is a global auto-increment assigned when Trakt writes the row, so it orders records by **insert**
time regardless of what `watched_at` claims. Calibrating id to wall-clock turns every record into a
pair — claimed watch date, actual logging date — and the gap is the **lag**. **Zero API calls**:
`src/step5_scan_full.py` reads `processed/step4/parsed/` only.

**Fitted on `checkin` and `scrobble` records only**, which a player emits at the moment of viewing.
`watch` rows are excluded from the fit because a bulk import produces exactly those. Evidence that
imports do not mint checkins: in the four highest id bands the `watch` median `watched_at` collapses
to 2021-2023 while checkin and scrobble medians keep tracking real time (2026-07-03, 07-05, 07-11,
07-28). Monotonised by isotonic regression (PAVA), not a cumulative maximum — the first
implementation used a cummax, one contaminated bin ratcheted the whole curve, and it reported a
2,065-day median lag on records logged in real time.

**Held-out validation**, fitted on even-indexed accounts and tested on the 2,185,696 real-time
records of odd-indexed accounts, no account in both: **median lag +0.003 days, 90.5% within one
day.** Residual error runs slightly **early**, so the diagnostic **under**-flags.

Under **ruling 2** this calibration is no longer only a diagnostic: it is a **required input to
Step 7**, which now needs an insertion time for every record. `processed/step5/calibration.npz` and
`record_lag.npz` carry it.

---

## 4. What is in the data

Three contamination modes, over 27,656,631 records on 2,549 accounts:

| Class | Records | Share |
| :--- | ---: | ---: |
| Backfill >180 d | 8,001,189 | 28.9% |
| Corrupt, pre-1990 (369,590 at exactly 1970-01-01) | 690,774 | 2.5% |
| Undated | 379 | 0.001% |
| Air-date-stamped | 2,021,537 | 7.3% |
| **Union** | **8,831,718** | **31.9%** |

| Action | Records | Median lag | Backfilled >180 d |
| :--- | ---: | ---: | ---: |
| `watch` | 22,597,404 | 0.04 d | **35.0%** |
| `checkin` | 1,133,846 | -0.02 d | 1.7% |
| `scrobble` | 3,234,228 | 0.01 d | 2.1% |

**Mode 3, air-date stamping**, was not previously identified: a class of import stamps `watched_at`
with the episode's **original broadcast instant**. Signature is a `(show, season, episode, instant)`
tuple shared by ≥5 unrelated accounts, landing on an exact top of the hour (63.5% of sampled groups),
seven days apart, at 00:00-05:00 UTC — US prime time. Up to 164 sampled accounts share one instant.
2,021,537 records, median lag 3,012 days, 1,628 accounts affected.

**The 180-day threshold is a conservative judgment, not a data-determined break.** Per-day density
is monotone decreasing throughout (30.941 %/day at ±1 d, then 0.227, 0.0598, 0.0310, 0.0199, 0.0175,
0.0102, 0.0062, 0.0043, 0.0008). Revision 1's claimed "trough" was an artifact of plotting raw band
shares over bands 2 to 9,716 days wide. The only real break after 1 day is at **7 days**. The choice
spans 5 points of sample across 7 d to 365 d, so it is not load-bearing — which, under the governing
principle, now matters even less than it did.

---

## 5. TV Time

Confirmed and dated to the week.

| Week beginning | Records written | Backfill share |
| :--- | ---: | ---: |
| baseline, Nov 2025 - Jun 2026 | ~43,000 / wk | 7-44% |
| 2026-06-25 | 151,144 | 75.4% |
| **2026-07-02** | **2,052,000** | **81.5%** |
| 2026-07-09 | 705,476 | 74.2% |
| 2026-07-16 | 206,911 | 49.2% |

TV Time shut down **15 July 2026**; the wave peaks in the fortnight before, which is when users
racing to migrate would export. Four weeks carry 3,115,531 records against a baseline expectation of
~174,000 — an excess of **2.94 million records, 11.3% of everything on disk**. 324 accounts have
their largest 7-day backfill burst inside that window.

**TV Time is nonetheless a minority of the problem**: only 31.7% of backfill was written after
2026-06-01. The rest is eleven years of ordinary onboarding backfill.

---

## 6. Bots and duplicate accounts

**Duplicate accounts: none, among accounts with real-time evidence.** Revision 1's apparent ten were
mode-3 artifacts — two unrelated accounts carrying the same air-date stamp share an exact signature.
Re-run on |lag| ≤ 7 d records, maximum containment between any two accounts is **0.22**. The limit:
an import-only duplicate leaves no real-time records and is invisible, and **251 accounts have under
5% real-time records** and are effectively untested.

**Bot signals: 126 accounts** on the survivor basis (corrected from revision 1's 175, which came from
uncommitted code counting all dated records and so inherited the import inflation it claimed to
control for).

| Accounts with N claimed days carrying >48 distinct episodes | ALL records | SURVIVOR records |
| :--- | ---: | ---: |
| ≥10 days | 844 | **591** |
| **≥30 days** | 175 | **126** |
| ≥100 days | 8 | **6** |

---

## 7. The pair-level audit

Approved Step 1 §6, decision D1: `T0 = max(S2_finale_air_date, S1_completion_date)`, both as UTC
calendar dates, the finale term from the Step 2 frame. **Terminology, fixed for the two isolated
Step 6 and Step 8 instances:** `T0` is the clock start, the value of the `max()`. **S1 completion
date** and **finale term** are its two inputs. **Binding term** is whichever the `max()` selects.

The 220,107 pairs reproduce Step 2's count exactly. Binding term: S1 completion date 116,041; S2
finale date 103,898; tie 168.

Every contamination class fabricates dates **earlier**, so where a fabricated S1 date falls at or
before the finale, `max()` discards it and `T0` is show metadata no import can touch:

| Disjoint class of the completing record | Naive removal | Absorbed by `max()` | Still binding |
| :--- | ---: | ---: | ---: |
| Corrupt, pre-1990 | 3,703 | 3,699 (99.9%) | **4** |
| Air-date-stamped | 24,226 | 24,222 (100.0%) | **4** |
| Backfilled >180 d only | 43,306 | 18,705 (43.2%) | **24,601** |
| **Total** | **71,235** | **46,626 (65.5%)** | **24,609** |

Those 24,609 are the pairs whose `T0` is genuinely fabricated. **The Human Lead did not exclude
them.** Only the 1,542 of them with no S2 evidence are excluded (§9).

### 7.1 Two errors nothing detects

**A `T0` can be too early even when the finale binds.** If true S1 completion happened after the S2
finale but the records claim an earlier date, computed `T0` is the finale and is wrong. Nothing on
disk detects this; detecting it needs the true watch date, which is what was destroyed.

**Ordering contamination (C5).** A completing record can be clean while the *sequence* that made it
the completing record used fabricated dates. Removing those pushes true completion **later**, and
`max()` does **not** absorb that, because a later true completion can overtake the finale. §10.

---

## 8. What Step 6 would read

Step 6 reads its lag off **the first S2 watch**. Of the 220,107 pairs, 194,830 have S2 evidence:

| Among pairs with S2 evidence | Pairs | Share |
| :--- | ---: | ---: |
| First S2 watch backfilled >180 d | ~35,040 | 20.4% |
| First S2 watch air-date-stamped | ~21,574 | 12.6% |
| First S2 watch corrupt | ~3,351 | 2.0% |
| **First S2 watch contaminated, any class** | **40,720** | **23.7%** |
| Entire S2 evidence air-date-stamped | 16,665 | 8.6% |

*(Percentages of the 171,763 with S2 evidence that also survive the unadopted Layer 2; the counts
are the measured ones.)*

**All of this is retained in the analysis population under adoption 1**, and **excluded from W's
estimation sample under ruling 1**. That is the whole point of keeping the two populations distinct
(§12).

### 8.1 The mode the instrument cannot see

Trakt stamps "mark season watched" with the moment of the button press, so insert time and claimed
time are identical, lag is zero, and every test here passes it. Among records surviving every test,
**38.2% of distinct episode-days sit on a claimed day carrying >48 distinct episodes** — over 24
hours of television. 43.4% at >24, 34.7% at >96.

Under the governing principle this is now much less alarming than revision 2 made it sound. It
corrupts *when*, not *whether*. It bears on Step 6 and is handled by ruling 1, not by exclusion.

---

## 9. THE ADOPTED RULE

Each clause is stated with the evaluability test it passes.

### Layer 1 — record classification. No rows dropped.

Every record is tagged and the tag travels with it into `processed/`: `corrupt` (absent or pre-1990);
`backfilled` (`τ_ins(id) − watched_at > 180 d`); `airdate_stamped` (tuple shared by ≥5 accounts);
`postdated` (`watched_at` more than 30 d after insert); else `clean`. Layer 1 changes no denominator
and is required by Step 7 under ruling 2.

### Adoption 1 — keep all pairs with S2 evidence, whatever their timestamps.

> A pair with S2 evidence answers the never-started question by inspection. Its timestamps may be
> fabricated; the fact of the S2 watch is not.

**Retains 23,067 pairs with a fabricated `T0`, 16,665 whose entire S2 evidence is air-date-stamped,
and 40,720 whose first S2 watch is contaminated.**

### Adoption 2 — exclude contaminated `T0` where there is no S2 evidence.

> **Exclude a pair when its S1 completion date is tagged `corrupt`, `backfilled` or
> `airdate_stamped`, that date is the binding term of `T0`, and the pair has no S2 evidence.**

**Cost: 1,542 pairs.** These are the only pairs where the fabrication changes an answer. They sit in
the headline never-started category, and their "never started within W of `T0`" is measured against a
window starting on a date nobody watched anything. They cannot be evaluated against the definition.

### Adoption 3 — exclude future-dated records.

**Cost: 0 to 3,307 pairs depending on reading. See §11 — this is the unresolved conflict.**

### Rejected and withdrawn

| Candidate | Cost | Disposition |
| :--- | ---: | :--- |
| **Layer 2**, exclude all contaminated `T0` | 24,609 | **Not adopted.** 23,067 of them have S2 evidence and are answerable regardless of when. Only the 1,542 residue survives as adoption 2. |
| **P2**, exclude pairs whose S2 evidence is entirely air-date-stamped | +16,632 | **Rejected.** The air-date stamp corrupts *when* they watched S2, not *whether*. The outcome is unchanged. |
| **P3**, entirely backfilled S2 evidence | +29,858 | Not proposed after P2's rejection; same argument applies with more force. |
| **Layer 3**, account-level | 35,861 | **Withdrawn** under ruling 2: its sole premise was that import noise is not liveness evidence, and under insertion-time liveness it **is** evidence. |
| **Layer 4**, ≥30 days over 48 episodes | 126 accounts / 20,193 pairs | **Rejected.** Heavy bulk-markers, not bots; **90.6%** of the pairs it removes have S2 evidence and are protected by adoption 1. |
| **L5**, bulk-mark exclusion | +39,446 | Not adopted. §8.1 corrupts *when*, not *whether*. |
| Drop backfilled records, keep the pair | — | Rejected in every revision: deleting S2 evidence converts started-and-left into never-started and fabricates the headline. |

---

## 10. C5, corrected

**Two corrections were asked for. One is a genuine correction to my number; the other is a claim I
have to report as incorrect, with evidence.**

**The count.** Both 4,188 and 5,694 are right, on different bases. `pair_contamination.csv` **does**
carry `s1_ev_airdate` — I persisted it in revision 2 — so the third class is available:

| C5 basis | Pairs | With S2 evidence |
| :--- | ---: | ---: |
| Two-class: backfilled or corrupt S1 evidence | **4,188** | 3,763 (89.9%) |
| Three-class: adding air-date-stamped S1 evidence | **5,694** | 4,974 (87.4%) |
| *air-date class adds* | *1,506* | |

Reconstructing from the two columns gives 4,188. I quote **5,694** because the air-date class is
persisted and is real. Derivation is in `src/step5_rule_costs_v2.py`; both are now reported.

**The mechanism.** Confirmed, and it reconciles to the definition used:

| Definition of "inserted after completion" | Pairs | Share | Median shift | Max |
| :--- | ---: | ---: | ---: | ---: |
| Any S1 record in the pair (two-class base) | **3,610** | 86.2% | **153.4 d** | **4,916.2 d** |
| Only records in the completion prefix (two-class) | 3,531 | 84.3% | 124.4 d | 4,316.8 d |
| Any S1 record (three-class base) | 4,724 | 83.0% | 76.5 d | 4,916.2 d |

The first row matches the figures put to me (3,602 / 86% / 152 / 4,916) to within rounding, so that
is the definition in use. **C5 is real**: in 86% of these pairs at least one S1 record was inserted
*after* the observed completion instant, so the true completion could be later by a median of 153
days and up to 4,916.

**The correction I have to report.** The stated reason C5 needs no ruling — *"the remaining 425 are
already inside the 1,542"* — **is not correct. The two sets are disjoint by construction**, and the
overlap is exactly 0:

- C5 is *defined* as pairs whose completing record is **clean** (`comp_contaminated == False`).
- The 1,542 is *defined* as pairs whose completing record is **contaminated** and binding.

So **414 of the 425 C5 pairs without S2 evidence are retained** under the adopted rule, not excluded
by adoption 2. (11 of the 425 have a post-dated completing record and fall under adoption 3.)

**The conclusion still holds, on a different basis.** A C5 pair's `T0` rests on a *clean* completing
record, so its window starts on a real logging date and it remains evaluable against the never-started
definition. What is uncertain is only whether completion should have been dated later — a *when*
question, which the governing principle puts out of scope. **C5 needs no separate ruling.** I record
the changed reasoning because the original reason would not survive Red Team.

---

## 11. THE CONFLICT — reported, not resolved

**Adoption 1** keeps all pairs with S2 evidence. **Adoption 3** excludes future-dated records.
**3,016 of the 3,307 post-dated pairs have S2 evidence**, so the two adoptions point opposite ways
for them. The post-dated set is **disjoint from the 1,542** (overlap exactly 0, verified).

The suggested resolution was that "future-dated **records**" is a record-level instruction, so the
pair survives with a recomputed `T0`. **Computing it exactly, as asked, shows the record-level
reading is itself ambiguous, and the ambiguity is worth more than the original conflict.**

**Why: post-dating arrives in blocks.** Pairs with a post-dated completing record hold a **median of
12 post-dated S1 records** each, not one. Post-dating is a block property like every other
contamination class in this store. So "set aside the record" removes a dozen distinct episodes, and
the pair drops below the `|D1| ≥ ceil(0.90 × L1)` threshold and ceases to be an S1 completer at all.

Four defensible operations, all computed:

| Reading | What it does | Removed | **Retained** | Post-dated pairs rescued |
| :--- | :--- | ---: | ---: | ---: |
| **P** | delete the pair outright | 4,849 | **215,258 (97.80%)** | 0 |
| **R1b** | drop every post-dated S1 record, recompute | 4,636 | **215,471 (97.89%)** | 213 |
| **R1n** | drop only the post-dated completing record | 3,493 | **216,614 (98.41%)** | 1,356 |
| **R3** | substitute the record's insertion time, re-sort, recompute | 1,542 | **218,565 (99.30%)** | 3,307 |

**The record-level reading does not do what it was expected to do.** Under R1b only **213 of 3,307**
pairs survive; **3,094 collapse** because they can no longer satisfy the S1 completion rule. Of the
3,016 with S2 evidence, only **202** are rescued and **2,814** collapse. So R1b resolves the conflict
in favour of adoption 3 for 93% of the disputed pairs, not in favour of adoption 1.

**R3 is the only reading that rescues all 3,307** and it lands exactly on the 218,565 upper bound.
It is the only one under which the episode stays in `D1`, and there is a precedent for it: Step 1
§2.3 conditions on whether the episode was *viewed*, not on whether its date is usable, and the
S1-completer diagnostic already applied exactly that logic to undated records. Under R3 the S1
completion date moves **earlier** by a median of 199 days, which makes `T0` more often finale-bound.

**A broad record-level rule also reaches pairs adoption 3 never named:** 1,240 pairs hold post-dated
S1 records that are not the completing record, and **585 of them collapse** under R1b.

**Reported, not resolved.** I am not choosing between P, R1b, R1n and R3. The spread is **3,307
pairs, 1.5% of the population**, and the choice also determines whether 2,814 pairs with S2 evidence
are deleted in apparent contradiction of adoption 1.

**Final retained pair count, both readings as asked:**
- **Pair-level: 215,258 (97.80%).**
- **Record-level: 215,471 (97.89%) under the literal drop; 218,565 (99.30%) under re-dating.**

---

## 12. Ruling 1 — the two populations, kept visibly distinct

> **W is derived from clean records only, then applied to everyone.**

`T0` is used twice, and the ruling separates them. This distinction is now the main structural fact
of the step, because adoption 1 deliberately retains contaminated pairs that must not inform W.

**Analysis population** — what Step 8 classifies. **215,258 to 218,565** pairs. It contains 23,067
pairs with fabricated `T0` and 40,720 whose first S2 watch is contaminated, all retained on purpose,
because the outcome is *whether*.

**W estimation sample** — what Step 6 measures. Pairs with S2 evidence, a clean `T0`, and a clean
first S2 watch:

> **W estimation sample = 128,099 pairs.**

**It is identical under all four readings of adoption 3** (P, R1b, R1n, R3), because a post-dated
`T0` is excluded from the estimation sample whether or not the pair is retained for analysis. That
makes W's derivation robust to the unresolved conflict in §11 — the conflict changes the analysis
population and does not change W.

Step 6 then applies its own D14 restriction to C1-bucket shows **on top** of this. The estimation
sample is two-factor — cadence bucket **and** provenance — and Step 6 applies both.

**§10(b) of revision 2 is moot.** It asked whether Layer 2 removed pairs from the Step 8 headline or
only from W's estimation sample. Layer 2 is not adopted, so the question does not arise.

---

## 13. Direction of the bias

Under the adopted rule the bias is **far smaller than under any rejected candidate**, because
adoption 1 keeps the S2-watchers that every rejected rule removed.

The 1,542 excluded pairs are **100% without S2 evidence**, so they are all pairs that would have
counted as never-started. **Excluding them pushes the never-started share down** — the opposite
direction from revisions 1 and 2, whose exclusions removed S2-watchers preferentially and pushed it
up (93.7% of Layer 2's removals had S2 evidence, against 87.9% retained).

The magnitude is small: 1,542 against a never-started category of roughly 25,000, so of order 6% of
that category, before adoption 3. **Step 14 needs this, and it needs the sign, which has flipped
between revisions.**

---

## 14. Limits

1. **The instrument is an estimate.** Median held-out error four minutes; 2-3% of known real-time
   records read >180 d of lag, presumably dates edited after the fact.
2. **Errors run toward under-flagging.** Real contamination is somewhat worse.
3. **§7.1 is undetectable.** A true S1 completion after the finale recorded with an earlier
   fabricated date yields a `T0` that is too early and passes every adopted test.
4. **§8.1 is unresolved** and now out of scope by ruling rather than by evidence. Over a third of
   surviving records sit on bulk-assigned dates; W absorbs this through ruling 1.
5. **The duplicate negative is conditional:** 251 accounts have too little real-time evidence to test.
6. **This covers the analysable cohort only** — the 2,549 `complete` accounts. The 287
   `discarded_over_tolerance`, 38 over-cap and 1,214 never-attempted accounts are **absent, not
   empty**, and nothing here characterises them.
7. **Air-date detection is a heuristic**, not a lookup against real air dates.
8. **The 182 duplicate `(user, rid)` rows** from pagination overlap were dropped before all figures.

---

## 15. Reproduction

Read-only. **Zero API calls in this step or any of its three revisions.** The id clock is already
inside the data on disk; no live-call budget was used.

| File | Role |
| :--- | :--- |
| `src/step5_scan_full.py` | rescan recovering the play `id` |
| `src/step5_calibrate.py` | id → insert-time calibration, PAVA, held-out validation |
| `src/step5_diagnose.py` | per-record lag, per-account metrics, aggregates |
| `src/step5_bots_dupes.py` | first-pass bot and duplicate detection |
| `src/step5_airdate_and_dupes.py` | mode 3; duplicates redone on real-time records |
| `src/step5_throughput.py` | day-load, both variants |
| `src/step5_pairs.py` | pair reconstruction; completing-record and first-S2-watch provenance |
| `src/step5_t0_binding.py` | binding term of `T0`, absorption audit |
| `src/step5_rule_costs_v2.py` | corrected cost table for the rejected candidates |
| `src/step5_adopted_rule.py` | **NEW** — adopted rule, C5 mechanism, W estimation sample |
| `src/step5_postdate_readings.py` | **NEW** — all four readings of adoption 3 |
| `src/step5_rule_costs.py` | revision 1's table, retained unmodified for diffing |
| `src/step5_figures.py` | figures; left panel is density |

Account-keyed outputs stay in `processed/step5/`: `pair_adopted.csv`, `pair_postdate_readings.csv`,
`pair_t0.csv`, `pair_contamination.csv`, `user_metrics.csv`, `bot_signals.csv`,
`duplicate_pairs_realtime.csv`, `rule_costs_v2.csv`, `adopted_rule.json`, `postdate_readings.json`,
`step6_exposure.json`, `throughput.npz`, `calibration.npz`, `record_lag.npz`, `mode3_flags.npz`,
`full_scan.npz`, `user_index.json`.

---

## 16. Open before Steps 6 and 7 run

1. **§11: which reading of adoption 3.** Four operations, spread of 3,307 pairs. Under three of the
   four, 2,814 pairs with S2 evidence are deleted, which reads against adoption 1. Not resolved here.
2. **§10: the C5 rationale is corrected.** The conclusion stands, the stated reason does not; the 425
   are disjoint from the 1,542, not inside it, and 414 of them are retained.
3. **Confirm the two populations** in §12 — analysis 215,258-218,565, W estimation 128,099 — since
   Step 6 and Step 8 are dual-implementation and both instances read this document.

Red Team reviews this revision. Steps 6 and 7 stay blocked until item 1 is settled.
