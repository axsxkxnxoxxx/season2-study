# Step 5 — Red Team reviews, rounds 1 and 2

**What this is:** the record of both adversarial reviews fired at the Step 5 gate. The `red-team`
agent is review-only and **wrote no files**; its findings existed solely in the session transcript
and would have been lost. They are transcribed here at the Human Lead's instruction, **before the
D1 ruling**, so that the ruling is made against a durable record rather than a conversation.

**Both rounds returned HOLD. The Step 5 gate is open.** Steps 6 and 7 remain blocked. Nothing in
this document approves, adopts, or proposes anything; the Red Team recommends and only the Human
Lead approves, in writing.

**Aggregates, counts and reasoning only.** No usernames, user IDs or individual watch histories.

| | |
| :--- | :--- |
| Round 1 | reviewed **revision 1** — the four-layer proposal, 32.4% exclusion. **HOLD**, B1–B3 blocking, C1–C5 corrections |
| Round 2 | reviewed **revision 3** — the adopted rule after Human Lead rulings. **HOLD**, D1–D3 blocking, E1–E6 corrections |
| Artifact under review | `artifacts/step5-contamination-diagnostics.md` |
| Reviewer constraints | Read, Grep, Glob only. Cannot execute code |

**Transcription note.** These are the Red Team's findings, reorganised for the page but not
softened. Where a claim was independently verified by the main session, that is marked in §3 and
kept separate from the review itself, so the reviewer's record stays unaltered.

---

## 1. Round 1 — against revision 1

**Verdict: HOLD.** B1, B2 and B3 each independently blocking.

**What the review credited.** The instrument is good. The play-`id` clock is a genuine second
clock, the held-out validation is properly constructed (fit on even-indexed accounts, test on odd,
no leakage), the PAVA correction is real and disclosed, and the TV Time dating is sharp. The
objections were to the rule, not the diagnostics.

### B1 — Layer 2 excluded on the S1 completion date; the clock start is not the S1 completion date

Approved Step 1 §6, and D1 in its decisions table, bind:

> `T0 = max(S2_finale_air_date, S1_completion_date)`

The artifact used "clock start" throughout to mean the first-pass S1 completion instant. The S2
finale term appeared nowhere; `src/step5_pairs.py` read `s1_E` and `s2_E` from the frame and never
opened `s2_finale_date`, which the frame carries.

Every contamination class Layer 2 targets fabricates dates **earlier** — backfill claims a date long
before the insert, air-date stamping writes an S1 episode's original broadcast instant, corrupt
dates are pre-1990 or epoch-zero. So wherever the fabricated S1 date falls at or before the S2
finale air date, `max()` absorbs the contamination entirely and `T0` is the finale date, which is
show metadata no import touched. Layer 2 removed those pairs anyway.

The headline sentence *"roughly one clock start in three was written by an import"* was therefore
not a statement about clock starts, but about one of two inputs to a `max()` where the other input
is clean, without establishing which binds.

The review also noted this put a terminology collision on the most load-bearing object in a document
two isolated Step 6 and Step 7 instances would read — a spec ambiguity under the dual-implementation
rule, not a wording preference.

**Named remedy:** condition the exclusion on which term binds. **Named as settleable at zero API
cost** by joining `pair_contamination.csv` (which carries `complete_rec_ts`) to `frame.csv` on
`show_trakt_id`.

### B2 — a rule was costed and then dropped without appearing anywhere

`src/step5_rule_costs.py` computed **P2, "P1 plus all S2 evidence air-date-stamped."** From
`rule_costs.csv`: P1 removed 71,235 and kept 148,872; P2 removed 71,855 and kept 148,252 — **620
pairs, 0.29 points.** It addressed the mode the artifact itself called "the most dangerous of the
three" and said would "bias W downward and inflate Continued." The artifact mentioned P2 or 620
nowhere: not proposed, not in the rejected-rules table, not deferred.

Separately: **50,533 pairs have S2 evidence that is entirely backfilled**, with no rule computed and
no cross-tab against Layer 2's survivors, so the artifact could not say how many carried into a
population Step 6 would read lag distributions off.

> The artifact did not merely decline to decide the three questions it lists. It decided a fourth
> against, silently, having costed it.

### B3 — Layer 4 and §8 rested on code not in the repository

`src/step5_rule_costs.py:29` loaded `processed/step5/throughput.npz` and took `days_over_48` from
it. **Nothing in `src/` wrote that file.** Same for `pair_completion_day_load.csv`.

`days_over_48` was the sole basis for Layer 4, the §5 bot table, and §8 — whose marginal-cost table
was the entire quantitative content of the largest deferred question in the document.

The measure also appeared to differ from the version-controlled one. `src/step5_bots_dupes.py:136`
restricted throughput counting to non-backfill records — with the stated reason *"so that an
import's flat timestamps do not read as a bot"* — and reported 1,970 / 580 / 39. The artifact
reported 2,183 / 844 / 175. A 50→48 threshold change cannot take the ≥10-day count from 580 to 844.

### C1–C5, corrections required

**C1 — there is no trough; it is a bin-width artifact.** §2.2 claimed a "real trough" between 7 and
180 days and concluded the 180-day threshold "sits in the flat part." Per-day density from the
artifact's own table is **monotone decreasing throughout**: 0.233 %/day at 1–7 d, 0.061 at 7–30,
0.032 at 30–90, 0.020 at 90–180, 0.017 at 180 d–1 y, 0.010 at 1–2 y, 0.0062 at 2–5 y, 0.0043 at
5–10 y, 0.0007 beyond. The "trough" bins are 23–90 days wide; the bins beyond are 1,095–10,950 days
wide, and the figure plotted equal-width bars over them, so the rising far-right bars were a
plotting artifact — in the chart a reader would use to judge whether 180 sits in a flat region. The
only real break is at roughly **7 days**, a 3.8× drop, which the document already used elsewhere as
its near-real-time boundary. Remedy: reframe 180 days as a conservative judgment consistent with the
stated under-flagging direction, not a data-determined break.

**C2 — the pair-versus-account argument is circular.** "The best account rule leaves 21.1% of
survivors on a fabricated clock start, while the pair rule leaves 0%" is a tautology: the pair rule
is *defined* as removing exactly those pairs, and `clock_unusable_share_kept = 0.0` holds for every
pair-level variant for the same reason. The non-circular evidence is the distribution across
accounts, where the mass sits in the 25–75% band.

**C3 — post-dated records are untagged and undeferred.** ~377,000 dated records claim a watch date
more than 30 days *after* their insert instant. Layer 1 tagged them `clean` and they could serve as
clock starts. Either the timestamp is bogus or the calibration is off by more than a month there;
both readings argue against trusting the record. Detection was unbounded in one direction and absent
in the other.

**C4 — "duplicate accounts: none found" overstates a conditional negative.** The re-run was
restricted to `|lag| ≤ 7 d` records; an import-only duplicate pair leaves no real-time records and
is invisible, and 251 accounts have under 5% real-time records. Correct statement: a clean negative
**among accounts with real-time evidence**.

**C5 — "every retained pair has a clock start with a real logging date behind it" is an overclaim.**
70,044 pairs have at least one backfilled record among the S1 evidence establishing completion,
against 65,615 whose completing record is backfilled — so pairs reach the threshold through an
ordering that includes fabricated dates. The alternative rule, "exclude when any S1 evidence
establishing completion is contaminated," was absent from the rules-considered table.

### What the reviewer verified itself in round 1

Arithmetic across §6 and §7 (all reconciled, including that §7's components are additive because
backfill is computed only over dated non-corrupt records); the held-out figures against
`calibration_meta.json`, confirming the artifact's 1-day figure is computed at
`step5_calibrate.py:132` and is not a mislabel; zero API calls, by reading all eight `step5_*.py`
scripts and confirming none imports an HTTP client; that no usernames appear in public folders and
the account-keyed CSVs correctly sit in `processed/`; and that `step5_pairs.py:44` opens `frame.csv`
read-only and writes nothing under `processed/step2/`.

### Round 1 position

The three deferrals the artifact listed were correctly declined. But the list was incomplete: P2 was
costed and dropped, post-dating was measured and left untagged, and by defining "clock start" as the
S1 completion date the artifact decided the finale term out of scope without naming it — the one
that determined whether Layer 2's 32.4% was the right price or several times the right price.

---

## 2. Round 2 — against revision 3

**Verdict: HOLD.** D1, D2 and D3 each independently blocking.

Revision 3 followed two Human Lead rulings — *W is derived from clean records only then applied to
everyone*, and *liveness runs on record insertion time* — and five adoptions that replaced the
four-layer proposal with a much narrower rule.

### Part 1 — were the round 1 findings resolved?

| Finding | Status | Basis |
| :--- | :--- | :--- |
| **B1** `max()` absorption | **Resolved, well** | §7 audit correct; binding terms 116,041 + 103,898 + 168 = 220,107; the absorption table re-partitions 71,235 into disjoint classes; residue 24,609. `src/step5_t0_binding.py` committed. Terminology fixed |
| **B2** P2 omitted | **Resolved** | Restored to the rejected table with a reason. Defect in how its cost is quoted — see E2 |
| **B3** uncommitted code | **Partly** | `src/step5_throughput.py` committed and the bot count corrected 175 → 126 on the survivor basis — exactly the inflation predicted. **But it recurs in §10 — see D3** |
| **C1** false trough | **Resolved, well** | `step5_figures.py` now plots `share / width` on a log density axis; stated densities match independent computation; the 7-day break adopted |
| **C2** circularity | **Moot** | Layer 2 not adopted, Layer 3 withdrawn |
| **C3** post-dating | **Resolved into a new problem** | Tagged in Layer 1; became adoption 3 and the §11 conflict — see E5 |
| **C4** duplicate overclaim | **Resolved** | Conditional negative stated, 251 untested accounts named |
| **C5** ordering | **Surfaced, mishandled** | See D2, D3 |

> The process worked. My objection is to the adopted rule, which I am seeing for the first time.

### D1 (blocking) — the governing principle contradicts the approved Step 1 outcome definition

The adopted principle: *"Timestamp accuracy is not a concern for this study. The outcome is whether
someone watched season 2, not when."*

For that to hold, "Never started" would have to mean "no S2 evidence, ever." Approved Step 1 §7:

> Let `A` = the set of **distinct** S2 episodes … whose canonical timestamp satisfies
> **`watched_at < τ1`** … **Never started** | `|A| = 0`

Never started means *no S2 episode dated before the window closed*. **The outcome operator is a
timestamp comparison.** And Step 1's mandatory diagnostic **D8** exists precisely for the population
the principle says cannot exist — never-started pairs holding S2 evidence dated in
`[τ1, τ1 + H × 24h)` — with the rationale: *"a pair that started S2 on day `W + 1` is called 'never'
by this document."*

**The consequence is not neutral retention.** Adoption 1 keeps 40,720 pairs whose first S2 watch is
contaminated, and the contamination has a direction. Air-date stamping writes the episode's original
broadcast instant; for an S2 episode that instant is ≤ the S2 finale ≤ `T0` < `τ1` **by
construction**. So every one of the **16,665 all-air-date-S2 pairs is guaranteed to land in `A`** and
score Started — and where the full season is stamped, `F2 ∈ A` and `|A| ≥ ceil(0.90 × L2)` both hold
and it scores **Continued**. Revision 1 §3 had said exactly this: *"the strongest possible 'continued'
signal … Left alone these would bias W downward and inflate Continued."* Revision 3 reversed that
conclusion on no new evidence — only the principle.

**The choice named for the Human Lead:** (a) amend Step 1 §7 to an ever-started definition, which
reopens gate 1 and voids `W`, D3, D8 and the three-state partition; or (b) narrow adoption 1 to
pairs whose S2 evidence can bear the `watched_at < τ1` comparison. *"They should be told that is the
choice, not 'tidy versus untidy timestamps.'"*

### D2 (blocking) — adoption 2 and the C5 ruling apply opposite logic to the same object

The 1,542 (excluded) and the 720 (retained) are both **pairs with no S2 evidence at all** and an
untrustworthy `T0`. One is removed as "cannot be evaluated," the other kept as "remains evaluable."

Neither stated reason holds. For a pair with zero S2 records, `|A| = 0` for **every** `τ1` — the
never-started answer is invariant to `T0`, so those pairs are perfectly evaluable.

What *does* depend on `T0` for such a pair is **right-censoring**: Step 1 D10 retains only if
`⟦T0⟧ + (max(W,91) + H) × 24h ≤ τ_pull`, so a fabricated-early `T0` lets a pair pass a censoring test
it should have failed. **That is a censoring defect, not an evaluability defect, and it is the real
case for excluding the 1,542.**

The reviewer endorsed the insert-time bound as the correct test, and the ruling on the 720 as
standing **on that corrected basis** — the 1,542 at median 40 days elapsed with 58.6% still inside an
open window at `W = 60`; the 720 at median 2,150 days with 8.1%. Two caveats: those figures appear
**nowhere** in the artifact or in `processed/step5/`, and the deliverable is what the isolated Step 6
and Step 8 instances read; and the same test destroys adoption 2's stated rationale, so **the Human
Lead needs to re-rule on the 1,542 and on the principle behind adoption 2**, not on the 720.

The section also quoted **5,694** and then reasoned throughout about **425**, the two-class figure —
leaving **295 C5 pairs with no S2 evidence unaccounted for**, the identical two-class/three-class
confusion the section was written to correct.

### D3 (blocking) — §10's headline C5 figures are not in the repository

§15 named `src/step5_rule_costs_v2.py` as the derivation; it computes no shift at all. The committed
source is `step5_adopted_rule.py`, and `adopted_rule.json` reports:

| Basis | Inserted-after | pct | Median shift | Max |
| :--- | ---: | ---: | ---: | ---: |
| two-class (completion prefix) | 3,531 | 84.3% | 124.4 d | 4,316.8 d |
| three-class | 4,606 | 80.9% | **29.5 d** | 4,316.8 d |

The artifact's §10 gives three rows, of which **only the middle one reconciles**. The committed
three-class row — median shift **29.5 days**, the least alarming figure available — is absent, while
the artifact leads with 153.4 d and concludes "C5 is real." B3 recurring, inside the section written
to answer Red Team.

### E1–E6, corrections required

**E1 — the sign is right and the scope is not.** Verified: the 1,542 are 100% no-S2-evidence, all
would have scored Never started, and removing them lowers the never-started share. **Sign correct,
down.** But §13 covers only the *exclusion*. The larger bias is the *retention*: backfill and
air-date stamping both write dates **earlier** than truth, so contaminated S2 records are pulled
**into** the window, converting Never-started into Started — the same direction, and roughly **26
times larger** (40,720 versus 1,542). Step 14 is being handed the sign of the small effect while the
large one goes unstated.

**E2 — the rejected-rules table quotes costs against an abandoned baseline.** P2's "+16,632" and
P3's "+29,858" are computed on the 195,498 Layer-2 survivors, and Layer 2 is not adopted. On the
adopted population the figures are 16,665 and **50,533**. P3 — pairs whose entire S2 evidence is
backfilled — is dismissed in one clause at 29,858 when its true scope is about **23% of the
population**: a 41% understatement in the one table that tells the Human Lead what was refused.

**E3 — "identical under every reading" is proved for two readings and probably false for the one
that matters.** `step5_adopted_rule.py:222` hard-excludes any pair whose *original* completing record
was post-dated, which makes 128,099 invariant across two readings. Under **R3** the record is
re-dated to insertion time and is no longer post-dated, so evaluated post-substitution those 3,307
pairs become eligible and the sample grows. The invariance of 128,099 is the stated reason `W`
survives the unresolved conflict, and it is unverified for the reading that rescues the most pairs.
Settleable in one line.

**E4 — R3's claimed Step 1 §2.3 precedent does not hold, and R3 reopens gate 1.** §2.3 governs
*which records count as watching* and refuses to filter on `action`; it says nothing about
timestamps. The operative timestamp rule is §2.2 — the canonical timestamp is the **minimum
`watched_at`**. R3 substitutes a fitted isotonic `τ_ins(id)`, with a 9.5% beyond-one-day tail and a
2–3% >180-day tail, for `watched_at`: a rule change inside an approved gate. Two further defects
unnamed in the artifact — it is a **selective** re-dating (if `τ_ins` is trustworthy for 3,307
post-dated records, why not for 8,001,189 backfilled ones, where substitution would move completion
much later), and R3's completion shift is median **−198.7 days**, pushing never-started **up**, the
opposite direction from adoption 2 and from the retained contamination. **The four readings have
different bias directions and are tabled only by pair count.**

**E5 — declining to choose among the four readings is correct, but the prior question was not
asked.** Under the governing principle, why does adoption 3 exist at all? A post-dated record is an
inaccurate timestamp on an episode that was viewed — exactly what adoption 1 protects and what P2 was
rejected for. Post-dating is also the class most likely to be instrument artifact rather than data
corruption, since the calibration concedes a 2–3% tail on the other side. It is the only clause in
tension with its own governing principle, it carries the most uncertain cost (0 to 3,307), and the
narrow answer to C3 — tag them and keep them out of the `W` estimation sample, both already done —
addresses the concern **without deleting a single pair**.

**E6 — §8's header and its percentages use different denominators.** 40,720 / 194,830 = **20.9%**,
not 23.7%, and the sub-rows sum to 59,965 against 40,720 because the classes overlap. Step 6 reads
this section.

### Round 2 position

> Revision 3 answered every finding I raised, and the B1 absorption audit in particular is the right
> piece of work done properly. Rejecting Layer 2 on the strength of it is defensible.
>
> But the rule that replaced it rests on a sentence that is false against the gate the Human Lead
> already approved. … **HOLD.** D1, D2 and D3 each block independently. D1 is first: it is not a
> Step 5 question and Step 5 cannot settle it. It is a question about what Step 1 §7 means, and it
> goes back to the Human Lead before any exclusion is recorded.

---

## 3. Independent verification by the main session

Kept separate from the reviews so the reviewer's record stands unaltered. Each item below was
checked directly against the repository, not taken on the reviewer's word.

| Claim | Result |
| :--- | :--- |
| **B1** — Step 1 binds `T0 = max(S2_finale_air_date, S1_completion_date)` | **Confirmed**, §6 and D1. "Finale" appears **zero** times in revision 1, not once as the review stated — which strengthens it |
| **B1** — corrected cost | **Computed.** Of 71,235, **46,583 finale-binds + 43 ties = 46,626 absorbed (65.5%)**; **24,609 still binding = 11.18%**. Corrupt and air-date classes contribute **8 binding pairs** between them |
| **B2** — P2 costed and dropped | **Confirmed** from `rule_costs.csv`: P1 71,235 / P2 71,855. Artifact mentions P2 or 620 zero times |
| **B3** — orphan inputs | **Confirmed.** `throughput.npz` read at `step5_rule_costs.py:29`, written by nothing in `src/` |
| **C1** — no trough | **Confirmed.** Per-day density monotone decreasing across every band |
| **D1** — Step 1 §7 and D8 | **Confirmed verbatim.** Never started is `|A| = 0` under `watched_at < τ1`; D8 counts never-started pairs holding S2 evidence and states *"a pair that started S2 on day W + 1 is called 'never' by this document"* |
| **D1** — deterministic Started/Continued | **Confirmed structurally.** An air-date-stamped S2 record carries that episode's broadcast instant ≤ S2 finale ≤ `T0` < `τ1`, so it always lands in `A` |
| **D3** — figures not in the repo | **Confirmed.** 3,610 / 153.4 / 4,916.2 appear nowhere in `src/`; `adopted_rule.json` carries a three-class median of 29.5 d that the artifact omits |
| **Zero API calls** | **Confirmed.** The request log's last entry is `2026-08-12T00:55:39Z` from the Step 2 shows pull; no `step5` run label exists |
| **No username leak** | **Confirmed.** All 2,549 usernames tested against every file in `artifacts/` and `decisions/`; only `right` and `orphan` match, both ordinary English words |

**Two errors originated in the main session, reached the Human Lead, and were caught by the
analytics-engineer.** Recorded because one of them entered a ruling:

1. C5 was reported as **4,188** against the artifact's 5,694, on the basis that
   `pair_contamination.csv` had no column for air-date-stamped S1 evidence. It does —
   `s1_ev_airdate`, added in revision 2, after the header had been read. **5,694 is correct**;
   4,188 is the two-class subset.
2. The Human Lead was told **"all 425 C5 pairs with no S2 evidence are already inside the 1,542."**
   **False.** The sets are **disjoint by construction** — C5 requires a clean completing record, the
   1,542 a contaminated binding one; overlap is exactly **0**, and the correct count is **720**. The
   ruling that C5 needs no separate ruling cited this claim as half its basis. The conclusion appears
   to survive on the insert-time evidence (720 at median 2,150 days elapsed, 8.1% open at `W = 60`,
   against 40 days and 58.6% for the 1,542), which the Red Team independently endorsed as the right
   test — but the stated basis was wrong.

---

## 4. What is outstanding at the time of writing

**The gate is open.** Steps 6 and 7 are blocked.

1. **D1 — the definitional conflict.** Not a Step 5 question. Amend Step 1 §7 to an ever-started
   definition, which reopens gate 1, or narrow adoption 1 to pairs whose S2 evidence can bear the
   `watched_at < τ1` test.
2. **D2 — re-rule adoption 2** on the censoring rationale rather than the evaluability one, and
   account for the 295 unexplained C5 pairs.
3. **D3 — commit the derivation** behind §10 or withdraw its figures.
4. **E1 — state the retention bias** alongside the exclusion bias, for Step 14.
5. **E2, E3, E6 — arithmetic and baseline corrections.**
6. **E4, E5 — the four readings of adoption 3**, their differing bias directions, and whether
   adoption 3 should exist at all.

---

## 5. Files

| File | Contents |
| :--- | :--- |
| `artifacts/step5-red-team-reviews.md` | this file — the record of both reviews |
| `artifacts/step5-contamination-diagnostics.md` | the artifact under review, revision 3 |
| `artifacts/step5-contamination-figures.png` | its figures |
| `artifacts/step1-outcome-definition.md` | the approved gate D1 turns on — §6, §7, D8, D10 |
| `processed/step5/` | account-keyed outputs and machine-readable results. Never leaves this machine |
