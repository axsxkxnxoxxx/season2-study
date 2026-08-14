---
name: decision-log-step18
description: Coverage map of the decision log of record in decisions/ (0001-0064, through the Step 7 gate approval), which judgments still have no file, and assembled five-field text pending handoff to the Human Lead
metadata:
  type: project
---

# Step 18 decision log — coverage map and pending text

**`decisions/` is the artifact of record. This memory is not the decision log and must not
duplicate it.** Step 18 assembles from `decisions/`. My job is coverage and consistency: which
judgments have a file, which do not, and whether the files still match the artifacts.

**Ownership:** the Human Lead writes every file in `decisions/`. I hand over assembled text and
stop. I never write there and never edit an entry — if I think one is wrong or incomplete I report
it ([[open-items-and-contradictions]] X2, X3, X4).

**Format, from `task-sheet.md` Step 18 — five fields per entry:** what was decided, what the
alternatives were, why this one, what it costs, and where the Red Team or a partner reviewer
disagreed and how it was resolved. *"This is the primary artifact. The analysis shows the work. The
log shows the judgment."*

---

> **This file is propagation surface 7** (`CLAUDE.md` §Propagation). **A stale entry here has already
> been fed back into a ruling** — see `0051` §2 and [[withdrawn-claims-register]] mode G. Correct it
> here **and** grep the other six surfaces; read-back alone is not verification.

## Coverage as of 2026-08-14 — `0001`–`0064`

| Files | Cover | Five-field completeness |
| :--- | :--- | :--- |
| `README.md` | Index, gate checklist, **19 open items** (1, 4, 12, 13, 14, 17 struck as closed) | n/a — index |
| `0001`–`0004` | Step 1 gate (incl. D10, D11, D12, B2 overruled); D15 endpoint; D14 W sample; 403 handling | Full |
| **`0005`–`0008`** | Step 3: stopping rule, twelve crawl constants, channel cost trade, seed source | Full, and each names the reviewer disagreement. **All four Open — awaiting ratification** |
| `0009`–`0012` | Step 4: pull order, tail cap, `pull_date` value, sweep completeness | Full. `0009`, `0010` and `0012` each record **the framing that was wrong and why**, which is unusually good for the "why this one" field |
| `0013`–`0020` | Step 2: delegation, no content filters, unaired S2, per-season network, air period, size quintile base, `pool_completers`, structural thresholds | Full |
| **`0021`** | **Step 5 gate closed.** The rule, four rulings made inside the gate, two standing rulings, four Step 14 limitations, three recorded errors, and what it unblocks | **Full, and it is the best-formed entry in the log** — it carries the four-round review history, the reasoning quoted verbatim, and the errors that entered rulings before being caught |
| **`0022`** | The two standing rulings propagated into `task-sheet.md` Steps 6 and 7 | Full. Notably records **who found it** and why the dual-implementation control could not have |
| **`0023`** | `0012` reviewed and upheld; three findings become Step 14 limitations | Full, and it does the harder thing: **states that Red Team was overruled on cost and not on merit**, so a future reader cannot infer the shape test was examined and found wanting |
| **`0024`** | "Flattens" withdrawn; `W` is the 90th percentile; Step 13 arms span 46–107 | **Full, and it is the best "alternatives" field in the log** — the alternative is not hypothetical, it is a measured 61-day spread produced by two instances from the same words |
| **`0025`** | The lag is a continuous instant difference; `W` is the **ceiling** | Full. Names the pattern it is the third instance of, and scopes itself forward to Step 7 |
| **`0026`** | **Step 6 gate closed. `W = 108`.** Four things that travel with the number; one unresolved conflict between approved documents | Full |
| **`0027`** | Step 13 `W` arms at 150 and 213 | Full, including why 150 exists — so a non-linear response is traced rather than interpolated between two endpoints |
| **`0028`** | Step 14 carries seven bias statements and eight non-bias limitations | Full, and it argues *substantively* why the ledger must not be netted rather than issuing it as a caution |
| **`0029`** | `W = 108` propagated to Steps 7, 8, 13 and both Step 6 artifacts; Step 7's threshold rule; Step 8's filter order | **Full, and the only entry in the log that is deliberately left partly Open** — the Step 7 percentile is **proposed at the 99th and not adopted**, and the entry says Step 7 must not launch until it is ruled. Its "alternatives" field is unusually strong: 90th / 95th / 99th priced by **false-dead rate** — one gap in ten, twenty, a hundred. It also **flags a caution the percentile does not answer** (the compounding false-dead rate over many gaps, ≈39% at the 99th over 50) rather than letting the ruling settle a question it does not reach |
| **`0030`** | The 2024/2025 contradiction; `show_network` dropped; five reception fields added; `size_quintile` separated from exposure | **Full, and the best "why not the obvious fix" field in the log** — per-year normalisation *over*-corrected worse than raw under-corrected (32.9% vs 12.3% against a 14.8% base), with the mechanism named. Also models how to correct an approved gate **without** reopening it: Step 1 *relies* on the cutoff, Step 2 *sets* it, so it is an addendum. Records the reviewer's one **wrong** example (`The Killing`) beside its six right ones |
| **`0031`** | The ≥50 completer floor, justified against its own sensitivity curve | **Full, and the most honest "what it costs" field.** It publishes a curve showing the threshold is **genuinely sensitive** — ±one step changes the candidate set by ~half — and says *no such defence is available here, and none is offered.* It also **refuses a number the reviewer asked for**: the frame at ≥25 costs 1,699 live calls and is not claimed |
| **`0032`** | Step 4 deliverables regenerated; the pull stopped **safely, not cleanly**; resume repriced | Full. Its judgment is the **characterisation**, not the fix: *"'exited cleanly' implies the run's own record is trustworthy, and it was the untrustworthy record that this entry exists to fix."* Records the engineering **PASS** and its evidence — zero 429s, zero 403s, 3 transient events in 126,391 requests — beside the defect |
| **`0033`** | Step 8 reports per-air-period retained counts per `W` arm; the discard-rate anomaly to Step 14 | Full. Notable for **separating what a null result rules out from what it leaves open**: no monotone trend rules out sweep length as the mechanism, which is the useful half; the +3 SD residual at bin 5 is unidentified and is not claimed to be noise |
| **`0034`** | **Step 1 §7 amended. Continued at `τ2` = 199 days.** Gate 1 reopened as an amendment and re-approved | **Full, and it is now the strongest entry in the log on the "where a reviewer disagreed" field** — eleven rounds, the rule never broken, four failed anchor grounds tabled with how each failed, and Red Team's "should not be cut" recorded as **not followed**. See [[amendment-step1-continued-boundary]] |

### `0035`–`0050` — the Step 7 block. Sixteen entries, five Red Team HOLDs, gate still OPEN.
### (The block now runs to `0064` — **thirty entries, fifteen reviews, fifteen HOLDs, gate APPROVED.** See below.)

**Read [[gate-step7-liveness]] first. The individual entries are each correct about what they
decided; only the sequence shows what happened, and the sequence is the Step 18 material.**

| Files | Cover | Five-field completeness |
| :--- | :--- | :--- |
| **`0035`** | The agent definition files are **live spec**; Step 10 receives `0034`; two propagation errors and five stale expressions | **Full, and its "why this one" field is the strongest structural argument in the log:** *"a dual pair whose two halves read the same stale brief produces a clean diff and a wrong answer, and the diff is the only instrument this study has for catching a spec defect."* Occasioned by `second-brain` |
| `0036` | Threshold at the 99th percentile; the test applies to the **gap bracketing `τ1`**, not the whole sweep | Full. Its §2.1 is the model for pricing a rule's *shape* rather than its level — the compounding false-dead table, and *"no percentile fixes it"* |
| `0037` | `0036` §1's basis **withdrawn** (length bias); gap unit fixed; namespaces assigned explicitly | **Full, and notable for recording a strengthening separately from a correction** — §2 makes `0036` §2's case *stronger* while §1 withdraws its sibling. Also the first entry to credit a formulation to an arm by name: *"the reference distribution and the test statistic are not the same object"* |
| `0038` | Spec frozen: reference 152,126, one gap per pair, quota and inertness disclosed, `W`-coupling accepted | **Full, and its "what it costs" field is unusually honest:** *"Between a number identified by nothing and a number whose advertised property is false, this study takes the first and says so."* Its §5 is corrected in place twice |
| **`0039`** | **Step 7 APPROVED at 632 d** — **later SUSPENDED** | Full **as a record of a decision that did not survive**. Kept with its errors marked in place, because *"the reasoning that produced them is part of the record"* — which is the right disposition and worth naming as precedent |
| **`0040`** | Gate **REOPENED**; `0021` reinstated; the 18,250 returned; derivation moved after D10 | **Full, and the best "where a reviewer disagreed" field in the block.** Its §7 is the entry the write-up should quote: *exact agreement between the two arms is **weak** evidence of correctness, because agreement was the design goal* |
| `0041` | Extended reference set, provisional; **no threshold approved** pending the sensitivity test | Full. **Status Open by its own line**, and superseded by `0042` the same day. Its §5 is where propagation failure was first tabled as a pattern rather than an incident |
| **`0042`** | **Threshold DELETED**; PF-LIMIT adopted | **Full, and the cleanest "why this one" in the study:** the headline cannot distinguish 787 from 2,200 days, 0.026/0.038/0.012 pp against a 3% share of the sampling width. Its §7 answers "was the work wasted" without defensiveness. **Its §1 claim is withdrawn two entries later** |
| `0043` | Bias-2 sign corrected DOWN→UP; `0042` §4's figures corrected | Full on the correction; **introduces three errors of its own**, all caught at `0045` |
| `0044` | "No free parameter" **withdrawn**; the rule is fully determined by `W` | **Full, and §1.1 is the sentence Step 18 should lift verbatim:** *"the study deleted a parameter it had varied — 787 to 2,200 days — and handed the rule's entire authority to a parameter it had not varied in the same test."* Sharpens item 46 to the five-file surface |
| `0045` | Option C bound; ALT rejected — **rejection later withdrawn** | Full on process, **wrong on substance**: it rejected ALT on a measurement taken where ALT cannot have an effect. Its §2 is still valuable — it separates *rejected on effect* from *rejected on feasibility* and records that the ordering is **not** a barrier to future outcome-conditional filters |
| **`0046`** | **ALT adopted**; `0045`'s rejection withdrawn; **§0's population rule** | **Full, and §0 is the second standing control in the study.** Its diagnosis is the durable part: *"It is reaching for the number that supports the ruling being written rather than checking which population produced it."* Three of its own sections are corrected in place by `0047` and a fourth by `0048` |
| `0047` | `0046` §1/§4/§7 corrected; D10 re-derived per arm; `>=` invariant | Full. Adds the **third-consecutive-bound** finding and the endpoint/estimand rule. **Misses `0046` §2's "751 directly observed"** — caught one entry later |
| **`0048`** | **ALT-BROAD adopted** | **Full, and it carries the warrant the whole gate turned on** — two nulls, not one, and `τ2 > τ1` makes Started-and-left's exit structural. Its §3 dismantles both of an arm's objections **using the arm's own words elsewhere in the same artifact**, which is a distinctive use of the "where a reviewer disagreed" field. §8 states what was **deliberately not touched**, per item 46 |
| `0049` | Joint S&L bound over all 703; six record defects; calibration residual discharged | **Full, and it records the one clean win of the block:** both arms independently refused a bound that would have been the fourth consecutive failure of the same test — *"the standing rule worked before it could be broken a fourth time, and it worked in the arms rather than in the ruling."* **Its header asserts a five-file pass that did not happen**, which `0050` opens by saying |
| **`0050`** | Six file defects fixed **and verified on disk**; limits routed to Step 14; the channel measured at **297 pairs** | **Full, and its §0 is the most self-aware opening in the log:** it declines to claim a propagation pass and puts the verification in the transcript. Adopts Red Team's formulation — *"'recorded, not repaired' is a legitimate way to close a gate; recording it only in a `decisions/` entry is not."* **Not indexed in `decisions/README.md`** — see [[open-items-and-contradictions]] V2 |

### `0051`–`0054` — the ALT-MATCHED adopt-and-revert. Four entries, two Red Team HOLDs, one day.

| Files | Cover | Five-field completeness |
| :--- | :--- | :--- |
| `0051` | V1–V7 and housekeeping | **Full on process, wrong on substance in §2.** It corrected two instances of "figure quoted without checking its population" **and committed a third in the same entry**, by adopting `second-brain`'s stale summary over the arms' JSON. Withdrawn by `0052` §2 |
| **`0052`** | **ALT-MATCHED ADOPTED**; `0051` §2 withdrawn; channel corrected to **52.4%**; propagation #12; the A-vs-B ratio; the population mismatch routed to Step 14 | **Full, and its §2 is the most valuable paragraph in the block for Step 18** — it records *how the error happened* rather than only that it did, and names the near-miss: *"a Step 9 instance reading the corrected line against its own deliverable would have deleted a correct number."* **Its §1 is reverted two entries later** |
| `0053` | `0021` amended for two windows; `0048` §9 withdrawn; nine defects | **WITHDRAWN IN ITS ENTIRETY — the only such entry in the log.** Retained with its nine defect fixes standing where rule-independent. **Its "where a reviewer disagreed" field is empty and that is the defect**: it amended an approved gate while leaving `0034`, the ruling that forbids the change, uncited |
| **`0054`** | **ALT-BROAD RESTORED**, S&L floor **widened**, `0053` withdrawn, `0021`'s amendment reverted, `0048` §9 restored; propagation #13; two divergences reported not reconciled | **Full, and it is the strongest "why not the alternative" field since `0030`** — it does not argue ALT-MATCHED is wrong in principle, it shows it is **numerically identical** to the cheaper repair on all three identified sets and therefore *"moved only point estimates while costing an amendment to an approved gate."* Its §4 sweep is evidence **neither arm was asked for**. **Its §7 restates the 0.4033 artifact its own §6 withdrew** |

**What Step 18 should take from `0051`–`0054`, and it is not in any single entry:**

1. **A rule was adopted, an approved gate was amended to fit it, and both were reverted within one
   day — and the record is not dishonest, because `0053` is retained withdrawn rather than deleted.**
   `0039` set that precedent for a suspended approval; `0053` extends it to a full withdrawal.
2. **The decisive test was "what does the change buy," asked numerically.** `0054` §1 is one table.
   **A gate that had turned for eleven entries on warrants and arguments closed the question with an
   identity.** That belongs beside `0042`'s threshold deletion as the block's second clean judgment.
3. **`0052` §2 is the case for the seven-surface propagation rule** and should be quoted where the
   controls are described: **five surfaces were checked, `artifacts/` and `second-brain`'s memory were
   not, and the unchecked one fed a wrong ruling.**
4. **Two arm divergences are on the record unreconciled, per `CLAUDE.md`** — robustness survival 792
   vs 791 (a `≤ τ_pull` restriction A states and B does not) and the bound width 0.4032 vs 0.4033 *(**0.4032 is adopted**; `0.4033` is instance B's rounding artifact, differenced from rounded endpoints, and has **no legitimate reading** — `0058`)*.
   **Neither arm flagged either, and the gate's own Check line is "dual implementation diff."** The
   write-up should not claim the diff caught them; a human reading two artifacts did.

### `0055`–`0064` — the machinery catching up, and the approval. Ten entries, seven Red Team HOLDs.

**The shape of this block is different from every other, and Step 18 should say so in one sentence:
the ANALYSIS stopped moving at `0055` and the RECORD took nine more entries to become true about it.**

| Files | Cover | Five-field completeness |
| :--- | :--- | :--- |
| **`0055`** | DERIV floor widened to 11.3015%; **the margin argument withdrawn as cherry-picked**; the grep control and the seventh surface; propagation #14–#17 | **Full, and §2 is the best "why not the obvious defence" in the block.** It refuses its own predecessor's supporting statistic on the ground that *"p5 supported the claim, the median contradicted it, and only p5 was quoted"* — **and then refuses margin statistics as a class**, because *"admissibility sets an endpoint; plausibility does not enter."* Both arms reached that independently and went further than the entry did. **Its §3 also records the control's own limit on its first run: a negative grep passes on a figure that was never written** |
| **`0056`** | Sub-interval corrected to [9.6372%, 9.7333%]; **`9.6830` DE-REGISTERED**; the dependency list | **Full, and the "what it costs" field is the sharpest admission in the log:** registering `9.6830` as a false positive *"disarmed the grep control against the one string it most needed to catch, on four surfaces, in the section that created the control"* |
| **`0057`** | The JSON halves; transitive dependency lists; **the channel window fixed to `(τ1, τ2)` OPEN**; surface 7 is the DIRECTORY; U2 measured at three | **Full. §5 is the model for closing a carried ambiguity**: it does not split the difference, it shows the adopted warrant already decides — *"at `s = τ2` that remainder is EMPTY"* — and then explains why fixing it at `W = 108`, where both forms are inert, is not premature: **at `W = 213` the boundary is the data's own edge** |
| **`0058`** | **Regeneration replaces hand-patching**; the two ratio conventions REPORTED not reconciled; dates corrected | **Full, and it is the entry that changes the METHOD rather than a number.** *"Eleven entries of one error class is a method that cannot converge, and `0057` was the twelfth."* **§6's date correction is a model of the log's own honesty rule** — a public tracked artifact corrected in place with a note, not silently rewritten |
| **`0059`** | The quotient is a target path; **the whole-file exemption DELETED**; **one register** | **Full. Its B2 finding is the one a reader should be shown**: the old exemption covered *"the entire Step 7 artifact set including both OPERATIVE deliverables, and it is why a wrong ratio survived a passing check."* **A stamp 300 lines above a value is not the point of use** |
| **`0060`** | Arm a runs one convention (`0.2818`); exemptions scoped per file and per value; **a sentence withdrawn from three places** | **Full, and §2 is the block's mode-G echo:** the figure cited as proof *"was itself an instance of the defect it was cited to certify, and I published it twice without checking which denominator produced it — the same failure as adopting Red Team's 73.6537% without checking its population at `0051`"* |
| **`0061`** | **Withdrawn CLAIMS are emitted by the generator**; the register holds phrases | **Full. Its finding is structural and generalises past this study:** a sentence was struck *"in the three places a human had typed it and left in the one place a SCRIPT types it."* **Both controls were blind by construction** — the `.md` form carries no numbers, the `.json` form is a string `verify()` skips |
| **`0062`** | **A check that looks nowhere must FAIL**; one definition per statement; the covering qualifier on eight surfaces | **Full, and §1's sentence is the one to lift: *"an empty result and a clean result are the same value, and only the control knows which it produced."*** §4 also records what the controls **cannot** do: *"a missing qualifier is neither a wrong number nor a withdrawn claim. Red Team found it by grep on an idea"* |
| **`0063`** | Widths from counts; **the rule objection closed on MEASUREMENT (652)**; the residual **logged, not fixed** | **Full, and it is the entry that breaks the cascade.** It fixes one thing and **logs seven findings as outstanding rather than correcting them under a blocking review** — after twelve consecutive entries in which the correcting entry introduced the next defect, **that is the change of method.** Its §1 also does the harder thing: it answers a challenge **in the direction that keeps the rule** and says *"the number that answers it is one Red Team could have read"* |
| **`0064`** | **STEP 7 GATE APPROVED. ALT-BROAD, UNCONDITIONAL, residual published** | **Full, and its §3 is the case for approval stated as a distinction rather than a verdict:** reviews **1–8 changed what is measured**, reviews **9–15 changed where numbers were written, which were checked, and whether a claim about a check was true.** **§2 records two amendments the Human Lead made to the drafters' own wording** — demoting *"blocking Step 9, not Step 8"* to Red Team's recommendation, and **confirming rather than accepting** the "with these open, not around them" framing. **That is the five-field format's "where a reviewer disagreed" field working on the drafter** |

**What Step 18 should take from `0055`–`0064`:**

1. **Approving with a published residual is a decision, and it should be presented as one.** Nine items
   are open, the approval is **unconditional**, and the Human Lead confirmed the framing in terms. The
   alternative — conditioning the gate on them — would have blocked Step 8 on **control defects that
   change no published figure.**
2. **The distinction between reviews 1–8 and 9–15 is the whole argument** and it is falsifiable:
   *"not one changed the rule, the population, the exclusion counts, or any bound endpoint."*
3. **A challenge answered with a number already in the record is worth recording as such.** `0063` §1
   does not soften it: the premise was false, **and the study had printed the refuting figure at `0045`.**
4. **Mode H — asserted actions never taken — is the block's dominant failure** and is now in
   [[withdrawn-claims-register]] with ten instances. The remedy that worked is **making the claim assert
   itself**, not making it more carefully.
5. **`0057` §7's counting rule must survive into the write-up: `#1`–`#18` is a surfaces-1–5 count and
   reads as a total without it.**

**Gate checklist:** **Steps 1 (amended and re-approved), 5, 6 and 7 closed. FOUR of five. Step 8 is the
only gate left and it MAY NOW LAUNCH.** **Step 7 was approved twice, reopened twice, and approved a
third and final time at `0064` — fifteen Red Team reviews, fifteen HOLDs, nine dual runs, zero API
calls.** **The Step 5 gate (`0021`, gate 2 of 5) was amended by `0053` and the amendment reverted by
`0054` the same day; it stands as approved.**

**One item flagged and NOT fixed, and it is on the log itself:** `artifacts/step7-gate-approval.md`
records that the approval is dated **2026-08-13** as the Human Lead gave it, while `0060`–`0063` —
**including `0063`, which carries the 652 the approval's §3 rests on** — are dated **2026-08-14**. It is
flagged to the Human Lead for confirmation or correction and **not fixed without a ruling**, `0058` §6
having corrected a date drift in the other direction. **The two things that conflict are the approval's
own date line and `0063`'s.**

**Four entries now credit `second-brain` by name** — `0022`, `0028`, `0029` and `0035`, all four
propagation gaps found on a post-gate consistency pass. Recorded without comment: the role is
continuity, and the log is the Human Lead's.

### What Step 18 should take from the Step 7 block, beyond the entries

1. **A gate can be approved, suspended, re-approved and reopened without the record becoming
   dishonest — if suspended entries are kept with their errors marked in place.** `0039` is the
   precedent and `0040` §8 states the principle.
2. **The five-entry self-correction cascade is the finding, not the entries.** `0042` through `0047`
   each corrected its predecessor and each introduced a defect doing it. Instance A's line from
   inside `0045` — *"the seventh instance, inside the entry correcting the sixth"* — is the honest
   summary, and `0046` §0 names the cause as motivated number-selection rather than inattention.
3. **Six standing controls came out of TWENTY-ONE propagation failures**, each written after the same
   failure recurred somewhere new: item 46's five-file surface; `0046` §0's population rule; `0049` §6's
   launch-snapshot practice; `CLAUDE.md` §Propagation's **seven** surfaces with read-back **plus grep**;
   `0055` §3's **positive** counterpart (grep the corrected string, require non-zero); and `0058`–`0062`'s
   **regeneration from one register**, whose governing rule is *"a check that finds nothing because it
   looked nowhere must fail."* **`#1`–`#18` is a surfaces-1–5 count and must never be published as a
   total; #19–#21 are the first found on surfaces 6 and 7.** A write-up that reports the controls without
   the failure count makes the process look more orderly than it was — **and one that reports 18 as the
   total repeats the error the count itself records.**
4. **The dual-implementation regime's limits are now measured, not asserted.** `0040` §7 (agreement
   was the design goal), `0047` §4 (DERIV's diff is literally `0 = 0`), `0050` §0 (both halves
   carried every defect identically). **These belong beside the Step 6 block's success case, or the
   write-up will overclaim what running everything twice bought.**
5. **The threshold's deletion is the block's headline judgment and it is defensible.** Three
   derivations established that the number did not matter; the quota property explains why there was
   never a number to find. **`0042` §7 is the paragraph that makes discarded work legible as
   evidence.**

**`0034` sets a new bar, and it is a different bar from `0021`'s.** `0021` showed the five-field
format at full strength on a *gate*. `0034` shows it on a *reversal inside an approved gate*, and
its distinctive contribution is recording **what could not be justified**: the amendment is adopted
with **no stated ground** for preferring `τ2` to first-S2-watch + `H`, four attempts are tabled with
their refutations, and the entry says the absence *"is the honest record and is not to be repaired
by a fifth attempt without new evidence."* **A decision log that can record an unfilled "why this
one" field without either faking it or blocking is doing the thing Step 18 exists to do.**

**Two propagation gaps `0034` left**, both in [[open-items-and-contradictions]]: **Step 10's spec**
(W2) and **the agent definition files** (W1). `0029` and `0034` between them amended `task-sheet.md`
Steps 1, 7, 8, 13 and 14 — and Step 10 is the one consuming step that moved and was not written to.

**`0021` sets a bar for the three remaining gate entries.** It records not just the rule but the
rulings made *during* the gate, the standing rulings that outlive it, the limitations that travel
forward, and the errors that reached the Human Lead — including two that **entered rulings before
being caught**, with the note that the conclusions survived on better bases. That is the five-field
format working at full strength, and it is the model for Steps 6, 7 and 8.

**One structural improvement worth naming.** `0022` exists because a ruling recorded in two places
was still missing from the third. The log now carries the standing check as README item 23. **Every
remaining gate entry should end by naming what it propagated to `task-sheet.md`, or stating that it
propagated nothing.** `0026` did **not** do this, and `W = 108` was consequently absent from the
Step 7 and Step 8 specs — **closed as `0029`**, which does exactly that and adds README items 30–32.
`0033` and `0034` both now carry the propagation statement explicitly. **The practice took four
entries to become habit and it should not be allowed to lapse at Steps 7, 8 or 9.**

**The Step 6 block is where the dual-implementation regime paid for itself, and Step 18 should say
so with the numbers.** `0024` and `0025` exist *only* because two isolated instances ran the same
words and produced different answers — 61 days apart, then one day apart. **Neither finding was
visible in a single run and the first was not visible in the spec.** That is a defensible answer to
"why did you run everything twice," and it is worth more in the write-up than the value of `W`.
See [[gate-step6-window-w]].

---

## What Steps 2–5 did well, as precedent for Step 18

Three practices worth naming because they make the five-field format easy to fill later:

1. **`0009`, `0010` and `0012` each record the instruction that was amended and why**, not just the
   final rule. `0010` states it explicitly: *"a cap defended by the wrong argument is a cap nobody
   can re-derive later."* That sentence is the "why this one" field doing its job.
2. **Red Team rounds 1–4 were transcribed to disk before the ruling that turned on them**, at the
   Human Lead's instruction, because the reviewer is review-only and writes no files. Without that,
   the D1 ruling would have been made against a conversation. **The "where a reviewer disagreed"
   field would otherwise have been unwritable for the entire Step 5 gate.**
3. **`0006` and `0008` were commissioned retrospectively** for choices nobody was obliged to record
   at the time. `0008` says why it is separate from `0006`: *"it is a design choice rather than a
   constant, and folding it into a list of numbers would bury it."*

---

## Judgments with NO file of their own — I hold the assembled text

Adopted and operative, but covered in `0001` only as "approved with the document." Each is a real
judgment with alternatives and a cost. Hand over when the Human Lead next writes to `decisions/`.

**D1 — clock start anchored on the S2 finale, not the premiere.** *Alternative:* premiere anchoring.
*Why:* Step 6 already anchors the lag on the finale; under premiere anchoring "Continued" is
unreachable inside any `W` shorter than the airing span, making the state an artifact of cadence;
and it scores a viewer who waits for a season then binges as a decliner — the exact conflation the
study exists to break. *Costs:* unequal exposure — opportunity to start S2 by `τ1` is
`airing_span + W` for weekly and `W` for binge, so **the never-started share is mechanically lower
for weekly titles by construction**, and the gap scales with season length. Paid openly: cadence
becomes a required Step 9 stratum and a mandatory Step 12 candidate flagged as the one candidate
with a known mechanical driver. *Disagreement:* none on D1 itself; its consequence became open
question 2, decided as D14 / `0003`. **New evidence 2026-08-12:** the frame is 29.9% C2 and 37.3%
C4, so the exposed population is most of it — D1's cost is not a corner case.

**Season membership by listed set, not numeric range.** *Alternative:* the range `1..F`. *Why:* the
range rule let through the exact case the gap machinery existed for. Under the set rule `D1 ⊆ E1`
and `A ⊆ E2` **by construction**. *Costs:* the Step 8 invariant "distinct episodes never exceed
season length" stops being a data check and becomes an **implementation** check. *Disagreement:*
Red Team second HOLD, F1 and F2, accepted in full. **Now vindicated on real data:** four
absolute-numbering shows in the candidate set used the same absolute numbers in history and
metadata, 100% overlap on all four, and **the withdrawn range form would have failed on all four.**

**First-pass S1 completion date, not last-observed.** *Alternative:* `max watched_at` over all S1
records. *Why:* (a) measures the wrong event and is **biased by engagement**. *Costs:* `(b) ≤ (a)`
always, so first-pass gives a **higher never-started share** — the direction that strengthens the
study's own headline, which is why the choice is defended on the merits and why **Step 13 must carry
(a) as a robustness arm** (`task-sheet.md` Step 13 now does, line 361). *Disagreement:* Red Team
pressed on whether the replacement Step 8 invariant tests anything; conceded and narrowed — the two
inequalities are vacuous, the **equality clause** does the work, and only if the check computes the
first-pass date **independently**.

**D13 — half-open UTC-instant boundaries.** *Alternatives:* `date(watched_at) ≤ T1`; a `23:59:59`
sentinel. *Why:* "on or before `T1`" admitted two faithful implementations one day apart on the
single operator that assigns every outcome state; the half-open form makes the window exactly `W`
days and makes window and horizon tile at `τ1` without gap or overlap. *Costs:* removes one calendar
day, moving the never-started share marginally **up**; named, not netted. *Disagreement:* Red Team
third HOLD, B3, accepted in full. **In live use:** Step 2's 2025-12-31 cutoff is applied as
`first_aired < 2026-01-01T00:00:00Z`, citing D13.

**D8 — never-started post-window diagnostic.** *Alternative:* report nothing for that category.
*Why:* "never" is the one word in the headline a reader takes most literally, and a pair that
started on day `W+1` is called "never." *Costs:* moves the headline **down**, which is why it
belongs. *Disagreement:* Red Team second HOLD, F3; entered as a proposal, held, adopted by the Human
Lead. **D8 later became load-bearing in a way nobody planned:** Red Team's D1 cited its existence as
proof that Step 1 §7 is a timestamp rule, which is what defeated the revision-3 principle.

**D9 — show splits as a known misclassification, with a bound.** *Why:* a split gives one ID a
complete S1 and `|A| = 0`, **fabricating a row directly into the published category**, while the
other disappears unrecorded. *Costs:* detection is imperfect and the count is a **lower bound**;
reconciliation logic stays unwritten. *Disagreement:* Red Team second HOLD, accepted. *Live caveat:*
the split mechanism is asserted, not observed.

**Liveness is a pair-level filter (scope correction).** *Why:* it was mis-scoped and would have
removed whole accounts on a test that only ever applied to one of their shows. *Costs:* none to the
definition; the cost was procedural — **the Human Lead amended `task-sheet.md` Steps 7 and 9
directly**, so a scope divergence between the two Step 7 instances is now a **bug, not a spec
ambiguity**. **This is the precedent [[open-items-and-contradictions]] X1 turns on.**

---

## Still with no decision file at all

1. **§10.1 open questions 1 and 3**, when ruled — the Continued boundary **conjuncts** and the
   right-censoring rule. Each carries a Data Scientist recommendation and a decision from nobody.
   **Q1's warrant now has a dangling term**: it turns on D3, which `0034` abolished. See
   [[open-items-and-contradictions]] W4 and [[step1-open-questions]].
2. ~~**The Step 7 liveness percentile.**~~ **CLOSED** — ruled at the 99th by `0036`, then the whole
   threshold was **deleted** at `0042`. `0029` is still recorded Open on it and README item 30 still
   says Step 7 must not launch until it is ruled; both are **overtaken, not closed**
   ([[open-items-and-contradictions]] V4, V11).
2b. ~~**The Step 7 gate itself, when it closes.**~~ **CLOSED as `0064`, 2026-08-13.** It inherited
   `0048` §9's open item — **`0021` licenses one direction of a biconditional and the converse is
   asserted, not justified** — and that is now **residual item 1**, a Step 14 limitation published with
   the result rather than a blocker. **The remaining gate entry to write is Step 8's.**
3. **The gap hypothesis**, if and when it is assigned an owner (README items 3 and 8).
4. **Ratification of `0005`–`0008`**, which are the only Open entries in the log.
5. **Whether to resume the Step 4 pull or sample the pool down** (README items 11 and 19). Every
   frame-derived boundary moves if it resumes.
6. **Step 11's brief vs Step 14's limitation** (README item 10) — the seeding-bias diagnostic.

## One misattribution risk to keep watching

`0005` credits Engineering's HOLD with the position that *"stating plainly that the plateau would
not fire is better than manufacturing one."* That sentence is **the agent's own, pre-registered** at
`src/step3_user_discovery.py:76` **before the run**. Engineering's distinct contribution was that it
**should have gone to the Human Lead before the run**. Do not let the log credit the reviewer with
the agent's foresight, or the agent with the reviewer's objection. **The same care applies to Step
5:** revision 1 §3 already said air-date stamping was "the strongest possible 'continued' signal"
and would "inflate Continued" — revision 3 reversed it, and Red Team D1 restored it. **Red Team
recovered a position the artifact had itself held and abandoned**, which is a different contribution
from originating it, and the artifact says so.

Related: [[gate-step1-outcome-definition]], [[gate-step5-contamination]],
[[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[withdrawn-claims-register]], [[population-chain-steps-2-3-4]], [[step1-open-questions]].
