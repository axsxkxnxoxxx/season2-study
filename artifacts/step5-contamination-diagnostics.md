# Step 5: Contamination Diagnostics

**Owner:** Analytics Engineer. **Mode:** GATE.
**Revision 6, 2026-08-12. FINAL — the adopted rule is complete and no decision is outstanding.**
Adoption 3 was dropped on 2026-08-12, which was the last item that could move the rule.
**Red Team returned PROCEED on this revision** at its fourth round, with four corrections since applied. **The gate was approved by the Human Lead on 2026-08-12** — `decisions/0021-step5-contamination-gate.md`. Steps 6, 7 and 8 are unblocked and each remains an unapproved gate of its own.

**Every remaining item in this document is a stated limitation, not a pending choice.** §17 says
which is which. Nothing below asks the Human Lead to decide anything further.

Round 3 stated it would **not object to the adopted rule on its merits**: D1 was ruled and
implemented correctly, D2's re-rule is right and now publishes its method, and E2-E6 are cleanly
resolved. **F1, F2 and F3 are about the write-up around the rule, not the rule.** The adopted rule is
unchanged by this revision — the exclusions remain the 16,665 and the 1,542, retaining **201,900**.

Both Red Team reviews of rounds 1 and 2 are on disk at `artifacts/step5-red-team-reviews.md`.

**Adoption 3 is dropped (§9.3). The §11 four-readings conflict is moot** — there is no rule left for
the readings to apply — **and Red Team's E3 indeterminacy is closed with it (§14).** The 4,988
partly-stamped pairs (§12) remain a **limitation carried to Step 14**, not an open decision.

Counts and shares only. Everything keyed to an account stays in `processed/step5/`.

---

## 0. The outcome definition governs. The revision-3 principle is withdrawn.

Revision 3 was written on this sentence:

> ~~Timestamp accuracy is not a concern for this study. The outcome is whether someone watched
> season 2, not when.~~

**That sentence is withdrawn. It described an ever-started study, and this is not one.** Approved
Step 1 §7 stands and gate 1 stays closed:

> Let `A` = the set of **distinct** S2 episodes whose canonical timestamp satisfies
> **`watched_at < τ1`**. **Never started** ⇔ **`|A| = 0`**.

**The outcome operator is a timestamp comparison.** A fabricated S2 timestamp does not merely make a
pair untidy; it moves the pair between outcome states. Step 1's mandatory diagnostic **D8** exists
for precisely the population the withdrawn principle said could not exist — never-started pairs
holding S2 evidence dated in `[τ1, τ1 + H×24h)` — and records that *"a pair that started S2 on day
`W + 1` is called 'never' by this document."*

**The Human Lead's reasoning for keeping Step 1 §7, recorded:**

> Ever-started is the wrong study for this frame. Exposure spans 55 years and 69 percent of pairs
> are pre-2020, so a to-the-pull-date rate would be a mixture weighted by show recency and newer
> titles would look worse by construction. It also collapses "started four years late" and "started
> opening week" into one row, which is the conflation this study exists to break.

Everything below is justified against `|A| = 0` under `watched_at < τ1`, or it is dropped.

### 0.1 The deterministic mechanism that follows

Air-date stamping (§4, mode 3) writes an episode's **original broadcast instant**. For an S2
episode that instant is **≤ the S2 finale air date ≤ `T0` < `τ1`** by construction. So an
air-date-stamped S2 record lands in `A` **on its own**, and the pair cannot score Never started.
Where the whole season is stamped, `F2 ∈ A` and `|A| ≥ ceil(0.90 × L2)` both hold and the pair
scores **Continued**. *(Written before the 2026-08-12 amendment, which moved Continued to `A_H` at
`τ2`. The conclusion holds a fortiori: `A ⊆ A_H` since `τ1 < τ2`, so a pair satisfying both conjuncts
on `A` satisfies them on `A_H`. The argument is unaffected.)*

Revision 1 §3 said exactly this — *"the strongest possible 'continued' signal… left alone these
would bias W downward and inflate Continued."* Revision 3 reversed it on no new evidence, only on
the withdrawn principle. **Revision 1 was right.**

---

## 1. The adopted rule and what it retains

| | Pairs |
| :--- | ---: |
| S1-completer pairs in the frame | 220,107 |
| **Excluded — S2 evidence entirely air-date-stamped** (adoption 1, narrowed) | **16,665** |
| **Excluded — contaminated `T0`, no S2 evidence** (adoption 2, censoring) | **1,542** |
| Excluded for post-dating — **adoption 3 dropped** | **0** |
| **ANALYSIS POPULATION** | **201,900 — 91.73%** |
| **W estimation sample** (Ruling 1, determinate) | **128,099** |

Post-dated records are **tagged and kept out of the W estimation sample, not deleted**: 3,296
post-dated pairs stay in the analysis population.

The two adopted exclusions are **disjoint by construction** — one requires no S2 evidence, the other
requires S2 evidence. Verified overlap: **0**.

Retained on purpose, because their contamination carries no guaranteed direction:

| Retained despite contamination | Pairs |
| :--- | ---: |
| Contaminated `T0`, has S2 evidence | 23,067 |
| First S2 watch contaminated in some class | 46,642 (26.2% of retained pairs with S2 evidence) |
| S2 evidence *partly* air-date-stamped | 7,340 — of which **2,352 closed**, **4,988 open** (§12) |

---

## 2. Revision history

| | Rev 1 | Rev 2 | Rev 3 | Rev 4 | Rev 5 | **Rev 6 FINAL** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Exclusion | 71,235 | 24,609 | 1,542 (+ad. 3) | 18,207 | 18,207 | **18,207** |
| Retained | 148,872 | 195,498 | 215,258-218,565 | 201,900 | 201,900 | **201,900** |
| Adoption 3 | — | — | unruled | unruled | unruled | **dropped** |
| Open decisions | 3 | 3 | 2 | 2 | 1 | **none** |

Round 1's B1-B3 and C1-C5 were resolved in revision 2. Round 2: **D1** §0; **D2** §9.2; **D3** §10
and §16; **E1** §13; **E2** §9.4; **E3** §14; **E4** §11; **E5** §11.3; **E6** §8.
**Round 3: F1** §13, the bias recomputed and the 30:1 ratio withdrawn; **F2** §12, shape 3 rejected
and 2,352 pairs closed; **F3** §10 and §16, the false certification replaced and the missing figures
committed to `src/step5_revision5.py`. **Revision 6** drops adoption 3, which makes §11 moot and
closes E3.

---

## 3. The instrument

`watched_at` cannot audit `watched_at`. The Trakt play `id` is a global auto-increment assigned when
Trakt writes the row, so it orders records by **insert** time regardless of what `watched_at` claims.
Calibrating id to wall-clock turns every record into a pair — claimed watch date, actual logging
date — and the gap is the **lag**. **Zero API calls**: `src/step5_scan_full.py` reads
`processed/step4/parsed/` only.

Fitted on `checkin` and `scrobble` records only, which a player emits at the moment of viewing.
`watch` rows are excluded from the fit because a bulk import produces exactly those. Evidence that
imports do not mint checkins: in the four highest id bands the `watch` median `watched_at` collapses
to 2021-2023 while checkin and scrobble medians keep tracking real time. Monotonised by isotonic
regression (PAVA), not a cumulative maximum.

**Held-out validation**, fit on even-indexed accounts, tested on the 2,185,696 real-time records of
odd-indexed accounts, no account in both: **median lag +0.003 days, 90.5% within one day.** Residual
error runs slightly **early**, so the diagnostic **under**-flags.

Under **ruling 2** this calibration is a **required input to Step 7**, which now needs an insertion
time for every record. `processed/step5/calibration.npz` and `record_lag.npz` carry it.

---

## 4. What is in the data

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

**Mode 3, air-date stamping**, was not previously identified: `(show, season, episode, instant)`
tuples shared by ≥5 unrelated accounts, landing on an exact top of the hour (63.5% of sampled
groups), seven days apart, at 00:00-05:00 UTC — US prime time. **Up to 198 of the 2,549 sampled
accounts share a single instant.** 2,021,537 records, median lag 3,012 days, 1,628 accounts affected. **This is the class §0.1
makes deterministic and the class adoption 1 now excludes on.**

*Correction.* Revision 5 quoted this maximum as **164**. That figure was uncommitted — Red Team's
point — and, once committed, **wrong**: it was the maximum over the first 4,000 qualifying groups
examined in an exploratory shell, not over all 155,626. The true maximum is **198**, now written by
`src/step5_airdate_and_dupes.py` to `airdate_and_dupes.json` as `max_accounts_per_group`. It enters
no rule, population, sample or bias statement, and `mode3_flags.npz` is byte-identical after the
recomputation, so nothing downstream moves.

**The 180-day threshold is a conservative judgment, not a data-determined break.** Per-day density is
monotone decreasing throughout; revision 1's claimed "trough" was a bin-width artifact. The only real
break after 1 day is at **7 days**.

---

## 5. TV Time

| Week beginning | Records written | Backfill share |
| :--- | ---: | ---: |
| baseline, Nov 2025 - Jun 2026 | ~43,000 / wk | 7-44% |
| **2026-07-02** | **2,052,000** | **81.5%** |
| 2026-07-09 | 705,476 | 74.2% |

TV Time shut down **15 July 2026**; the wave peaks in the fortnight before. Four weeks carry
**3,115,531 records — 11.3% of everything on disk** — against a baseline expectation of ~174,000,
so the **excess is 2.94 million records, 10.6% of the store**. Revision 1 attached the 11.3% to the
excess rather than to the wave and every revision through 5 repeated it; the two figures are now
attached to the quantities they belong to.

Only 31.7% of all backfill was written after 2026-06-01, so **TV Time is a minority of the
problem**; the rest is eleven years of ordinary onboarding backfill.

---

## 6. Bots and duplicate accounts

**Duplicate accounts: none, among accounts with real-time evidence.** Revision 1's apparent ten were
mode-3 artifacts. On |lag| ≤ 7 d records, maximum containment between any two accounts is **0.22**.
The limit: an import-only duplicate leaves no real-time records, and **251 accounts have under 5%
real-time records** and are untested.

**Bot signals: 126 accounts** with ≥30 claimed days carrying >48 distinct episodes, on the survivor
basis (corrected from 175, which came from code that inherited the import inflation it claimed to
control for).

---

## 7. The pair-level audit

`T0 = max(S2_finale_air_date, S1_completion_date)`, both UTC calendar dates (Step 1 §6, D1). **`T0`**
is the clock start; **S1 completion date** and **finale term** are its two inputs; **binding term**
is whichever `max()` selects. Binding: S1 completion date 116,041; finale 103,898; tie 168.

Every contamination class fabricates dates **earlier**, so where a fabricated S1 date falls at or
before the finale, `max()` discards it:

| Disjoint class of the completing record | Naive removal | Absorbed by `max()` | Still binding |
| :--- | ---: | ---: | ---: |
| Corrupt, pre-1990 | 3,703 | 3,699 | **4** |
| Air-date-stamped | 24,226 | 24,222 | **4** |
| Backfilled >180 d only | 43,306 | 18,705 | **24,601** |
| **Total** | **71,235** | **46,626 (65.5%)** | **24,609** |

24,609 pairs have a genuinely fabricated `T0`. **23,067 of them have S2 evidence and are retained**
(§9.1); the 1,542 without S2 evidence are excluded on the censoring argument (§9.2).

---

## 8. What Step 6 would read — E6 corrected

Red Team E6 is upheld: revision 3's §8 header quoted the full population and its percentages were
computed on the abandoned Layer-2 survivor subset. **The fix is not to relabel the old numerator but
to recompute on the population that now exists.** Both denominators are given so the correction is
checkable.

**Full frame, all 194,830 pairs with S2 evidence:**

| First S2 watch | Pairs | Share |
| :--- | ---: | ---: |
| Backfilled >180 d | 57,594 | 29.6% |
| Air-date-stamped | 21,653 | 11.1% |
| Corrupt | 3,384 | 1.7% |
| **Contaminated, any class** (classes overlap) | **63,307** | **32.5%** |

**After the adopted rule, 178,165 retained pairs with S2 evidence:**

| First S2 watch | Pairs | Share |
| :--- | ---: | ---: |
| Backfilled >180 d | 42,019 | 23.6% |
| Air-date-stamped | 4,988 | 2.8% |
| Corrupt | 3,384 | 1.9% |
| **Contaminated, any class** | **46,642** | **26.2%** |

Adoption 1 cuts air-date exposure in the retained population from 11.1% to 2.8%. Revision 3's
"40,720 / 23.7%" is withdrawn: 40,720 was computed on the 171,763 Layer-2 survivors and Layer 2 is
not adopted. Dividing that same numerator by the full denominator gives 20.9%, which mixes two bases;
**32.5% and 26.2% are the figures on the two populations that actually exist.**

### 8.1 The mode the instrument cannot see

Trakt stamps "mark season watched" with the moment of the button press, so insert time and claimed
time are identical and lag is zero. Among records surviving every test, **38.2% of distinct
episode-days sit on a claimed day carrying >48 distinct episodes.** Under the restored Step 1 §7 this
is not harmless: a bulk-mark dated inside the window puts the pair in `A`. It is handled by ruling 1
(kept out of W's estimation sample), not by exclusion, and it remains a limit (§14).

---

## 9. THE ADOPTED RULE

### Layer 1 — record classification. No rows dropped.

`corrupt` (absent or pre-1990); `backfilled` (`τ_ins(id) − watched_at > 180 d`); `airdate_stamped`
(tuple shared by ≥5 accounts); `postdated` (`watched_at` >30 d after insert); else `clean`. Required
by Step 7 under ruling 2 and by §11.1.

### 9.1 Adoption 1, narrowed — exclude pairs whose S2 evidence is entirely air-date-stamped.

> **Exclude a pair when it has S2 evidence and *every* S2 record in `E2` is `airdate_stamped`.**

**Cost: 16,665 pairs.** This is Red Team's option (b), not option (a): Step 1 §7 is not amended and
gate 1 is not reopened.

The justification is §0.1 and it is deterministic, not probabilistic. An air-date-stamped S2 record
carries an instant **≤ the S2 finale ≤ `T0` < `τ1`**, so it lands in `A` by construction. These pairs
do not report an outcome; **the stamp reports it for them**, and it always reports Started, and where
the season is fully stamped, Continued.

**Kept: the 23,067 contaminated pairs that have S2 evidence.** Backfill has no guaranteed
relationship to `τ1` — a backfilled S2 record can carry any date — so those pairs are not classified
by their contamination. They are retained in the analysis population and excluded from W's estimation
sample (§14).

### 9.2 Adoption 2, re-ruled — the 1,542 go on a censoring defect, not an evaluability defect.

Red Team D2 is upheld. Revision 3 said these pairs "cannot be evaluated against the definition."
**That is wrong.** A pair with zero S2 records has `|A| = 0` for **every** `τ1`; the never-started
answer is invariant to `T0` and the pair is perfectly evaluable.

What does depend on `T0` is **right-censoring**. Step 1 **D10** retains a pair only if
`⟦T0⟧ + (max(W,91) + H) × 24h ≤ τ_pull`. A fabricated-**early** `T0` inflates apparent elapsed time
and **lets a pair pass a censoring test it should have failed.**

> **Exclude a pair when its S1 completion date is `corrupt`, `backfilled` or `airdate_stamped`, that
> date is the binding term of `T0`, and the pair has no S2 evidence.**

**Cost: 1,542 pairs.**

**The insert-time bound is the evidence.** A viewer cannot log an episode before watching it, so a
record's insert instant is an **upper bound** on when it was truly watched. The latest defensible
clock start is `T0_latest = max(S2_finale_date, date(max τ_ins over the S1 completion evidence))`.

| Population | Pairs | Median elapsed days at `T0_latest` | Share still inside an open window at `W = 60` |
| :--- | ---: | ---: | ---: |
| **The 1,542** — contaminated `T0`, no S2 | 1,542 | **40.0** | **58.6%** |
| The 720 — C5, no S2 (retained) | 720 | 1,738 | 7.9% |
| — of which the 425, two-class | 425 | 1,717 | 13.4% |
| — of which the 295, air-date class | 295 | 1,762 | 0.0% |
| Every pair with no S2 evidence | 25,277 | 1,532 | 11.3% |

**On the latest date they could defensibly have finished S1, the median excluded pair has 40 days of
elapsed observation and 58.6% are still inside a window that has not closed.** Their retention is an
artifact of the fabricated-early date, exactly as D10 anticipates. `W = 60` is illustrative only; W
is not set until Step 6.

**A discrepancy to record, and a correction to how revision 4 stated it.** The 720's figures are
published in two places as **median 2,150 days, 8.1%**. Revision 4 attributed the whole gap to
omitting the `max()` with the S2 finale. That was **half right**, and the correction offered to me —
that the difference is the completion-prefix versus all-S1-records basis, with the `max()`
included — is **also half right**. It is **two departures**, and the full grid shows which does what:

| Basis for `max τ_ins` | `max()` with S2 finale | Median elapsed | Share open at `W = 60` |
| :--- | :--- | ---: | ---: |
| **Completion prefix** | **yes — correct** | **1,738 d** | **7.92%** |
| Completion prefix | no | 2,190 d | 7.92% |
| Any S1 record | yes | 1,728 d | 8.06% |
| Any S1 record | no | **2,151 d** | **8.06%** |

**The 8.06% comes from the all-S1-records basis. The 2,150 median additionally requires the finale
term to be absent**, and it cannot come from anywhere else: `max(finale, x) ≥ x`, so including the
finale can only push `T0_latest` **later** and elapsed **smaller**. **2,150 > 1,738 is arithmetically
impossible with the `max()` in force on the same set.** The finale binds for **61.8%** of the 720,
which is why its absence moves the median by 450 days.

**Cause, now established and corrected in the public record.** The `max()` was written into the
original computation but was **inert**: `.astype("int64")` on a tz-aware datetime returns
**microseconds** in the pandas version in use, so dividing by 1e9 placed every S2 finale in January
1970, and a `max()` against January 1970 never binds. So the two departures were the all-records
basis and a **unit bug**, not a deliberate omission — revision 5 was right that the finale term had
to be absent and wrong to imply it had been left out on purpose.
`artifacts/step5-red-team-reviews.md` now carries the corrected four-cell grid.

The substantive point is unchanged: the completion prefix is the right basis, `T0` is a `max()` with
the finale, and **1,738 days / 7.92% is the figure to use**. The 1,542's figures are identical under
all four cells, so the D2 case does not depend on any of this.

### 9.3 Adoption 3 — DROPPED. No pair is deleted for post-dating.

> A post-dated record is an inaccurate timestamp on an episode that was watched, which is what I
> protected everywhere else. Tag the records and keep them out of the W estimation sample rather
> than deleting pairs.

**Cost: 0 pairs.** This accepts Red Team E5. Adoption 3 was the only clause in tension with the
principle applied everywhere else in this rule: a post-dated record is the same kind of object as a
backfilled one — an inaccurate date on an episode that was viewed — and P3 and Layer 2 were both
refused for exactly that reason. It also carried the most uncertain cost in the document, 0 to
3,307, and would have deleted 3,016 pairs holding S2 evidence.

**The Layer 1 `postdated` tag plus exclusion from the W estimation sample is the whole of the
treatment.** Both were already in place, which is E5's point: the narrow answer to C3 addresses the
concern **without deleting a single pair**. **3,296 post-dated pairs remain in the analysis
population** — 3,307 less the 11 already excluded as entirely air-date-stamped.

### 9.4 The 720 — retained, on the same bound.

C5 pairs have a **clean** completing record, so their `T0` rests on a real logging date, and the
bound above shows they are not censoring-fragile. **Retained.**

### 9.5 Rejected and withdrawn — E2, recosted on the adopted population

Revision 3 quoted these against the 195,498 Layer-2 survivors, a baseline that no longer exists.

| Candidate | Full scope | Marginal beyond the adopted rule | Disposition |
| :--- | ---: | ---: | :--- |
| **P2**, S2 evidence entirely air-date-stamped | 16,665 | — | **ADOPTED** as 9.1. Revision 3 rejected it; §0.1 reverses that |
| **P3**, S2 evidence entirely backfilled | **50,533 (23.0%)** | **35,179** | Not adopted. Backfill carries no guaranteed relation to `τ1`, so it does not classify the pair by itself. Revision 3 quoted 29,858 — a **41% understatement** |
| **Layer 2**, all contaminated `T0` | 24,609 | 23,034 | Not adopted. 23,067 have S2 evidence and are answerable |
| **Layer 3**, account-level | 35,861 | — | **Withdrawn** under ruling 2: its sole premise was that import noise is not liveness evidence, and under insertion-time liveness it **is** evidence |
| **Layer 4**, ≥30 days over 48 episodes | 126 accounts / 20,193 pairs | — | Rejected. Heavy bulk-markers, not bots; 90.6% of its pairs have S2 evidence |
| **L5**, bulk-mark exclusion | +39,446 | — | Not adopted; see §8.1 and §14 |
| Drop backfilled records, keep the pair | — | — | Rejected in every revision: deleting S2 evidence converts Started into Never-started and fabricates the headline |

---

## 10. C5 — full disposition, D3 answered

Revision 3 quoted **5,694** and then reasoned about **425**, leaving **295 pairs unaccounted for**.
The full disposition:

| C5 basis | Pairs | With S2 evidence | **Without S2 evidence** |
| :--- | ---: | ---: | ---: |
| Two-class: backfilled or corrupt S1 evidence | 4,188 | 3,763 | **425** |
| Three-class: adding air-date-stamped S1 evidence | **5,694** | 4,974 | **720** |
| *air-date class adds* | *1,506* | *1,211* | ***295*** |

**All 720 are retained**, on the bound in §9.2, and the 295 are the least fragile of the three groups
(0.0% inside an open window at `W = 60`). The 4,974 with S2 evidence are retained under §9.1 unless
their S2 evidence is entirely air-date-stamped. **Nothing is now unaccounted for.**

**D3 — the derivation.** Revision 3 named `src/step5_rule_costs_v2.py`, which computes no shift at
all, and quoted three rows of which only one reconciled to committed output. The mechanism figures
are recomputed and both bases are given:

| Definition of "an S1 record inserted after the observed completion instant" | Pairs | Share | Median shift | Max |
| :--- | ---: | ---: | ---: | ---: |
| Two-class, completion prefix | 3,531 | 84.3% | 124.4 d | 4,316.8 d |
| Two-class, any S1 record | 3,610 | 86.2% | 153.4 d | 4,916.2 d |
| **Three-class, completion prefix** | **4,606** | **80.9%** | **29.5 d** | 4,316.8 d |
| Three-class, any S1 record | 4,724 | 83.0% | 76.5 d | 4,916.2 d |

The three-class prefix row — median **29.5 days**, the least alarming figure available — was absent
from revision 3 and is restored. **C5 is real** on any basis: in 81-86% of these pairs an S1 record
was written after the instant the pair is recorded as having completed S1. It is not actionable,
because the bound in §9.2 shows the affected no-S2 pairs are not censoring-fragile.

**All four rows are written by `src/step5_revision5.py` into
`processed/step5/revision5.json` under `F3_C5_mechanism`.** Revision 4 certified these as committed
while naming `src/step5_rule_costs_v2.py`, which computes no shift at all; two of the four rows
existed only in throwaway shells. That was F3, the third occurrence of B3/D3, and it is why §16 now
names a single file and a single JSON key per figure.

---

## 11. Adoption 3 — considered, and rendered moot by the ruling

**This section is retained as a record of work considered. It is not an open item.** Adoption 3 was
dropped (§9.3), so the four readings below are four ways to apply a rule that no longer exists.
Nothing here requires a decision.

### 11.1 What was weighed

**For:** ~377,000 records claim a watch date more than 30 days **after** their insert instant, and
3,307 pairs have such a record as their S1 completing record. A post-dated completing record pushes
`T0` **later** than truth, which under D10 makes a pair fail censoring it should pass — the mirror of
§9.2.

**Against (Red Team E5, accepted):** a post-dated record is an inaccurate timestamp on an episode
that was viewed, which is what retention protects everywhere else. It is the class **most likely to
be instrument artifact** rather than data corruption — the calibration concedes a 2-3% tail beyond
180 days on the other side, and post-dating is that same tail reflected. And tagging plus exclusion
from the W estimation sample, both already done, addresses C3 **without deleting a pair**.

### 11.2 The four readings, recorded and moot

Post-dating arrives in **blocks**: affected pairs hold a **median of 12 post-dated S1 records**, so
"set aside the record" sets aside a dozen distinct episodes and the pair falls below
`|D1| ≥ ceil(0.90 × L1)`. That is why the readings diverge so widely.

| Reading | Retained | Post-dated pairs rescued | Bias direction |
| :--- | ---: | ---: | :--- |
| **Adopted — tag only, delete nothing** | **201,900 (91.73%)** | 3,307 | neutral |
| P, delete the pair | 198,604 (90.23%) | 0 | never-started down |
| R1b, drop every post-dated S1 record | 198,817 (90.33%) | 213 | never-started down |
| R1n, drop only the completing record | 199,957 (90.85%) | 1,356 | never-started down |
| R3, re-date to insertion time | 201,900 (91.73%) | 3,307 | never-started **up** |

The adopted outcome coincides in pair count with R3 but **not** in method: R3 rewrites timestamps,
the adopted rule leaves every timestamp untouched and merely tags it. That distinction matters
because of E4.

### 11.3 E4 stands on the record, and is now academic

**E4, first correction.** Revision 3 claimed Step 1 §2.3 as precedent for R3. **It does not hold.**
§2.3 governs *which records count as watching* and refuses to filter on `action`; it says nothing
about timestamps. The operative rule is **§2.2: the canonical timestamp is the minimum
`watched_at`.** R3 would substitute a fitted isotonic `τ_ins(id)` — with a 9.5% beyond-one-day tail —
for `watched_at`, which is a **rule change inside an approved gate**, and a **selective** one: if
`τ_ins` were trustworthy enough to re-date 3,307 post-dated records, the same argument would apply to
8,001,189 backfilled ones, where substitution would move completion much **later**.

**E4, second correction.** The four readings **do not share a bias direction.** R3's completion shift
is a median of **−198.7 days**, pushing `T0` earlier and never-started **up** — opposite to P, R1b
and R1n. A table ordered by retention alone hides that.

**The adopted rule avoids both objections**: it changes no timestamp, so §2.2 is untouched and no
re-dating bias is introduced.

## 12. The partly-stamped pairs — mostly closed, 4,988 left open

Adoption 1 excludes pairs whose S2 evidence is **entirely** air-date-stamped. **The deterministic
mechanism in §0.1 does not require "entirely".** A single air-date-stamped S2 record carries
`watched_at ≤ S2 finale ≤ T0 < τ1`, so it lands in `A` on its own and forces `|A| ≥ 1`.

### 12.1 Most of it closes with no `W` at all

Revision 4 computed the split, printed it, and then declared the whole 7,340 unanswerable. That was
wrong: **2,352 of them close by the same kind of ordering argument the mechanism itself rests on.**

For a pair whose **first** S2 watch is clean, let `c` be that record's canonical timestamp and `s`
any stamped record's. Since the clean record is the earliest, `c ≤ s`, and `s ≤ S2 finale ≤ T0 < τ1`.
So `c < τ1` **at every `W`**: the clean record lands in `A` regardless, and the stamp is redundant.
Those pairs would score Started on their clean evidence alone.

| | Pairs |
| :--- | ---: |
| S2 evidence with **any** air-date-stamped record | 24,005 |
| — entirely stamped, **excluded** by adoption 1 | 16,665 |
| — partly stamped, retained | 7,340 |
| — — **first S2 watch is clean → CLOSED, provably rescued, no `W` needed** | **2,352** |
| — — **first S2 watch is the stamp → OPEN** | **4,988** |

**The residual is 4,988 pairs, 2.27% of the frame — not 7,340 and not 3.6%.** It is a **limitation**,
not a pending decision: §12.2 rules on it and the exclusion is not extended.

For those 4,988 the stamp is the earliest S2 evidence, so whether their clean evidence also falls
before `τ1` depends on `τ1 = ⟦T0⟧ + W×24h`, which does not exist until Step 6 reports.

### 12.2 Shape 3 is rejected. Ruled.

Three shapes were available: exclude the 4,988 now; exclude none; or defer the test to Step 8 where
`W` exists and the question is answerable pair by pair. **The Human Lead has rejected the third:**

> Leave the 4,988 open and state it in Step 14. Do not make the analysis population a function of
> `W`. Shape 3 would break the dual-implementation control, which is worth more than recovering 2.3
> percent.

**The cost that rejection avoids, stated because revision 4 left it unnamed.** If the analysis
population were a function of `W`, then whenever the two Step 6 instances return different `W` — which
is the entire reason Step 6 is run twice — the two Step 8 instances would classify **different
populations**. The diff would then confound an implementation difference with a population
difference, and the control the dual-implementation regime exists to provide would be gone. A
population that moves with the parameter under test cannot test the parameter.

**The exclusion is not extended. The 4,988 stay in the analysis population and go to Step 14 as a
named limitation**, with the mechanism: each holds an S2 record stamped with a broadcast instant that
is inside the window by construction, and for each the stamp is the earliest S2 evidence, so it may
be deciding an outcome that the pair's clean evidence would not.

### 12.3 The boundary is still inconsistent, and that is on the record

**Adoption 1's "entirely" boundary has no basis in the §0.1 mechanism.** The rule excludes pairs on a
guarantee while retaining other pairs that carry the identical guarantee. The 2,352 closure reduces
that inconsistency from 7,340 pairs to **4,988**. **It does not remove it.** The boundary is a
practical line, not a principled one, and Step 14 should say so rather than imply the exclusion is
exhaustive.

---

## 13. Bias — F1: two statements, not one netted direction

Revision 4 put a population change and an estimator bias in one column and quoted a **30 : 1** ratio
computed as 46,642 / 1,542. **That ratio is withdrawn.** It ignored the 16,665 entirely — a removal
running the *other* way and itself **10.8×** the 1,542 — and its numerator is an **upper bound on
pairs at risk, not a count of flips**. "Thirty times larger" and "dominant" were not established and
are not claimed here. The two effects are not commensurable and Step 14 gets them separately.

### 13.1 Population change — exact, and the net is UP

This is arithmetic on which pairs leave the frame. No estimation.

| Removal | Pairs | Every one of them would have scored | Direction on never-started |
| :--- | ---: | :--- | :--- |
| The 1,542 — contaminated `T0`, no S2 evidence | 1,542 | Never started | down |
| The 16,665 — S2 evidence entirely air-date-stamped | 16,665 | Started, by construction (§0.1) | **up** |
| **Net** | **−15,123** | | **up** |

**The adopted exclusions on net raise the never-started share**, because they remove ten Started
pairs for every one Never-started pair. Revision 4's netted "down" was wrong on this component.

### 13.2 Estimator bias on the retained population — direction down, magnitude bounded

Separately, among pairs that **stay**, contaminated timestamps are written **earlier** than truth, and
that error is one-directional. An S2 record whose true watch fell after the window closes can be
pulled **into** the window; a record whose true watch was inside cannot be pushed out. So the error
can only convert **Never started → Started**, never the reverse. **Therefore the never-started share
this study reports is a FLOOR.**

#### The premise is guaranteed for 8,372 pairs and assumed for 42,019. This qualifier travels.

"Written earlier than truth" is **structural** for two of the three classes and **an assumption** for
the third, which is 90.1% of the mass. Splitting the retained contaminated set (classes overlap, so
they do not sum to 46,642):

| Class | Retained pairs | Is claimed ≤ true? |
| :--- | ---: | :--- |
| Air-date-stamped | 4,988 | **Guaranteed.** The stamp is the episode's broadcast instant and nobody watches before broadcast |
| Corrupt, pre-1990 | 3,384 | **Guaranteed.** A pre-1990 date precedes any true watch in this frame |
| **Backfilled >180 d** | **42,019 (90.1%)** | **Assumed, not guaranteed** |

**Why the backfill class is only assumed.** The `backfilled` tag means claimed ≪ **insert**. It does
**not** mean claimed < **true**. A user who watched in 2015, imported in 2026, and whose import wrote
2018 produces a backfilled record whose claimed date is **later** than truth. That record is pushed
**out** of the window, converting **Started → Never started** — the opposite direction, running
**against** the floor.

Early-skewed backfill remains the plausible reading, and it is the same premise §7's `max()`
absorption relies on. **But the two uses are not equally checkable.** §7 applies it to the
**observed claimed date versus the S2 finale**, both of which are on disk, so the absorption is
verified rather than assumed. §13.2 applies it to **claimed versus true**, and the true watch date is
precisely what the contamination destroyed. The floor is therefore guaranteed for 8,372 pairs and
rests on an unverifiable — though well-motivated — assumption for the other 42,019.

#### How large it could be, bounded with the instrument this step built

A contaminated record's true watch time is **≤ its insert instant**. So a pair whose first S2 watch
has `τ_ins < τ1` was inside the window whatever its claimed date says, and **cannot flip**. Only
`τ_ins ≥ τ1` pairs can:

| `W` | Retained pairs with contaminated first S2 watch | Ruled out by insert time | **Upper bound on flips** | % of retained |
| ---: | ---: | ---: | ---: | ---: |
| 30 | 46,642 | 1,987 | 44,655 | 22.1% |
| 60 | 46,642 | 2,184 | 44,458 | 22.0% |
| 91 | 46,642 | 2,370 | 44,272 | 21.9% |
| 120 | 46,642 | 2,518 | 44,124 | 21.9% |
| 180 | 46,642 | 2,886 | 43,756 | 21.7% |

**This bound is weak and is reported as weak.** It eliminates only about 5% of the candidates, because
a backfilled record is by definition written long after the date it claims, so `τ_ins ≥ τ1` for most
of them. It establishes an upper limit of roughly **22% of retained pairs** and it does **not**
establish that anything like that many actually flip — a pair that genuinely watched S2 inside the
window and logged it two years later is in this set and did not flip. **The true flip count is
somewhere between zero and 44,458 and this step cannot narrow it further.**

### 13.3 What Step 14 must carry

1. The adopted exclusions change the population and their **net effect is up** (§13.1), exactly.
2. Retained contaminated timestamps bias the estimator **down**, so the reported never-started share
   is a **floor** (§13.2) — consistent with Step 9's instruction to report a floor and a ceiling
   rather than a single contestable number. **Step 14 must publish the qualifier with the direction:
   the floor is structurally guaranteed for 8,372 retained pairs (air-date-stamped and pre-1990
   corrupt) and rests on an unverifiable assumption of early-skewed backfill for the other 42,019,
   90.1% of the mass.** Backfill guarantees claimed ≪ insert, not claimed < true, and any pair whose
   import wrote a date later than the true watch runs against the floor.
3. The bound on (2) is **wide**: up to ~22% of retained pairs are at risk, with no point estimate.
4. The **4,988** open partly-stamped pairs (§12) and the unprincipled "entirely" boundary (§12.3).

**These must not be netted into a single direction.** One is a counted population change and the
other is an unquantified estimator bias; combining them would give a number with no interpretation.

---

## 14. Ruling 1 — the two populations, and E3 closed

> **W is derived from clean records only, then applied to everyone.**

**Analysis population** — what Step 8 classifies: **201,900** pairs. It deliberately contains 23,067
pairs with a fabricated `T0`, 46,642 whose first S2 watch is contaminated, and 3,296 whose completing
record is post-dated.

**W estimation sample** — what Step 6 measures: pairs with S2 evidence, a `T0` that is neither
contaminated nor post-dated, and a clean first S2 watch. The waterfall, monotone by construction:

| Step | Pairs | Dropped |
| :--- | ---: | ---: |
| Analysis population | 201,900 | — |
| has S2 evidence | 178,165 | 23,735 |
| `T0` not contaminated | 155,131 | 23,034 |
| completing record not post-dated | 152,126 | 3,005 |
| first S2 watch clean | **128,099** | 24,027 |

> ### **W estimation sample = 128,099 pairs. Determinate.**

### 14.1 E3 is closed by the ruling, not argued away

Red Team E3 found that revision 3's claim of "128,099 under every reading" was true for the readings
that delete or drop and **false for R3**, which re-dates the post-dated record so the pair becomes
eligible and the sample grows to **131,043**. E3's conclusion followed: `W`'s derivation was **not
independent** of the §11 conflict, and choosing a reading would move both populations.

**That finding was correct, and revision 5 withdrew the invariance claim rather than defending it.**

**Dropping adoption 3 closes it.** R3 is not a candidate reading, because there is no rule for it to
be a reading of. Post-dated records are tagged and excluded from the estimation sample, and no
alternative treatment is on the table. **The sample is 128,099 and there is no second number.** The
indeterminacy is removed by the ruling, not resolved by argument — which is the honest description,
because nothing about the data changed.

Step 6 then applies its own D14 restriction to C1-bucket shows **on top** of this. The estimation
sample is two-factor — cadence bucket **and** provenance — and Step 6 applies both.

## 15. Limits

1. **The instrument is an estimate.** Median held-out error four minutes; 2-3% of known real-time
   records read >180 d of lag. §11.1's argument against adoption 3 turns on that tail.
2. **Errors run toward under-flagging.** Real contamination is somewhat worse.
3. **A `T0` can be too early even when the finale binds**, if true S1 completion happened after the
   finale but the records claim an earlier date. Nothing on disk detects it.
4. **§8.1 is not addressed by any exclusion.** Over a third of surviving records sit on
   bulk-assigned dates; ruling 1 keeps them out of `W`, and nothing removes them from the analysis
   population.
5. **The duplicate negative is conditional:** 251 accounts have too little real-time evidence to test.
6. **This covers the analysable cohort only** — the 2,549 `complete` accounts. The 287
   `discarded_over_tolerance`, 38 over-cap and 1,214 never-attempted accounts are **absent, not
   empty**.
7. **Air-date detection is a heuristic**, not a lookup against real air dates. §12's guarantee is only
   as good as the ≥5-account collision test.
8. **The 182 duplicate `(user, rid)` rows** from pagination overlap were dropped before all figures.

---

## 16. Reproduction

Read-only. **Zero API calls in this step or any of its six revisions.**

**Certification: per section, per key, exhaustive. No blanket claim.** Revision 4 asserted that every
figure came from committed code, which was false for nine of them; revision 5 fixed those but left a
sweeping closing sentence that the `164` figure in §4 falsified. Both are replaced by the routing
table below. A reader can grep any figure in this artifact to exactly one file and key.

| Artifact section | Source file | Key |
| :--- | :--- | :--- |
| §1 summary, §9 adopted rule, §14 waterfall and W sample | `revision5.json` | `FINAL_ADOPTED_RULE` |
| §3 held-out validation, §4 record classes, §5 TV Time wave | `revision5.json` | `F3_record_level` |
| §4 mode 3 groups, records, accounts, **max 198 accounts per group** | `airdate_and_dupes.json` | `mode3_airdate_stamp` |
| §4 action table, §4 density bands, §5 weekly histogram | `aggregates.json` | `by_action`, `weekly_insert_histogram_tail` |
| §6 duplicates and bot signals | `airdate_and_dupes.json`, `throughput.json` | `duplicates_realtime`, `survivor` |
| §7 binding terms and `max()` absorption | `t0_binding.json` | `of_that_set`, `by_class` |
| §8 first-S2-watch breakdowns, both denominators | `revision5.json` | `F3_section8` |
| §8.1 bulk-mark day-load shares | `throughput.json` | `survivor.over_24/48/96` |
| **§9.2 insert-time bound — 40.0, 58.6%, 1,717, 13.4%, 1,762, 0.0%, 1,532, 11.3%, and the 1,542 / 720 / 425 / 295 / 25,277 counts** | **`revision4.json`** | **`insert_time_bound`** |
| §9.2 four-cell reconciliation grid | `revision5.json` | `reconciliation_720_bound` |
| §9.5 rejected candidates recosted | `revision4.json` | `rejected_recost_on_adopted_population` |
| §10 C5 counts and all four mechanism rows | `revision5.json` | `F3_C5_mechanism`, `populations` |
| §11 four readings of adoption 3 | `postdate_readings.json` | `readings` |
| §12 partly-stamped split, 2,352 / 4,988 | `revision5.json` | `F2_partly_airdate` |
| §13.1 population change | `revision5.json` | `F1_population_change` |
| §13.2 class split and flip bound | `revision5.json` | `F3_section8.retained`, `F1_flip_upper_bound` |

| File | Role |
| :--- | :--- |
| `src/step5_scan_full.py` | rescan recovering the play `id` |
| `src/step5_calibrate.py` | id → insert-time calibration, PAVA, held-out validation |
| `src/step5_diagnose.py` | per-record lag, per-account metrics, aggregates |
| `src/step5_bots_dupes.py`, `src/step5_airdate_and_dupes.py` | bots; mode 3; duplicates on real-time records |
| `src/step5_throughput.py` | day-load, both variants |
| `src/step5_pairs.py` | pair reconstruction; completing-record and first-S2-watch provenance |
| `src/step5_t0_binding.py` | binding term of `T0`, absorption audit |
| `src/step5_adopted_rule.py` | C5 mechanism, first pass at the adopted rule |
| `src/step5_postdate_readings.py` | the four readings of adoption 3 |
| `src/step5_revision4.py` | insert-time bound, adopted-rule arithmetic, E2/E3/E6 |
| **`src/step5_revision5.py`** | **NEW — F1 flip bound, F2 closure, F3 figures, 720 reconciliation grid** |
| `src/step5_rule_costs.py`, `_v2.py` | revisions 1 and 2 cost tables, retained unmodified for diffing |
| `src/step5_figures.py` | figures; density panel |

Account-keyed outputs stay in `processed/step5/`: `pair_revision5.csv`, `revision5.json`,
`pair_revision4.csv`, `pair_adopted.csv`,
`pair_postdate_readings.csv`, `pair_t0.csv`, `pair_contamination.csv`, `user_metrics.csv`,
`bot_signals.csv`, `duplicate_pairs_realtime.csv`, `revision4.json`, `adopted_rule.json`,
`postdate_readings.json`, `rule_costs_v2.csv`, `throughput.npz`, `calibration.npz`,
`record_lag.npz`, `mode3_flags.npz`, `full_scan.npz`, `user_index.json`.

---

## 17. Status: no outstanding decisions. Four stated limitations.

**The adopted rule is complete.** Exclude the 16,665 and the 1,542; retain 201,900; derive `W` on
128,099. Adoption 3 is dropped, §11 is moot, E3 is closed. **Nothing in this document asks the Human
Lead to decide anything further.**

Four items remain, and every one is a **limitation to be stated**, not a choice to be made:

| # | Limitation | Where | Carried to |
| ---: | :--- | :--- | :--- |
| 1 | **4,988 partly-air-date-stamped pairs** retained, each holding an S2 record that is inside the window by construction and is that pair's earliest S2 evidence. Shape 3 was rejected: the analysis population must not be a function of `W` | §12 | Step 14 |
| 2 | **Adoption 1's "entirely" boundary is practical, not principled.** The rule excludes on a guarantee that 4,988 retained pairs also carry | §12.3 | Step 14 |
| 3 | **Two bias statements that must not be netted:** an exact population change whose net is **up** (+15,123 removed, ten Started pairs per Never-started pair), and a separate estimator bias whose direction is **down**, making the reported never-started share a **floor**, bounded above at ~22% of retained pairs and not point-estimated. **The floor carries a qualifier that must be published with it: structurally guaranteed for 8,372 retained pairs, assumed for the other 42,019 (90.1%), because `backfilled` means claimed ≪ insert, not claimed < true** | §13.2, §13.3 | Steps 9 and 14 |
| 4 | **Timestamp modes the instrument cannot see** — same-day bulk-marking (§8.1), a `T0` too early when the finale binds (§15 item 3), and the cohort's absent 1,539 accounts (§15 item 6) | §8.1, §15 | Step 14 |

**Handoffs.** Step 6 takes the 128,099 estimation sample (§14) and applies D14 on top. Step 7 takes
the play-`id` calibration as a required input under ruling 2 (§3). Step 8 takes the 201,900 analysis
population and the Layer 1 record tags (§9).

Red Team returned PROCEED on this revision at its fourth round; its four corrections are applied above. The gate was approved by the Human Lead on 2026-08-12 (`decisions/0021-step5-contamination-gate.md`). Steps 6, 7 and 8 are unblocked and each remains an unapproved gate of its own.
