---
name: gate-step7-liveness
description: The Step 7 liveness gate as a narrative — five rules in succession (632d, 1293d, PF-LIMIT, ALT, ALT-BROAD) plus the ALT-MATCHED adopt-and-revert, fifteen Red Team HOLDs split 1-8 rule / 9-15 record, twenty-one propagation failures, the warrant that selected the rule, and the self-correction cascade; APPROVED at decisions/0064
metadata:
  type: project
---

# Step 7, the liveness gate — the longest and messiest stretch of the study

> # **APPROVED. `decisions/0064`, Human Lead, 2026-08-13. GATE 4 OF 5 IS CLOSED.**
>
> **Record: `artifacts/step7-gate-approval.md`.** The rule is **ALT-BROAD**. **The approval is
> UNCONDITIONAL** — the nine-item §4 residual is **open and published, not resolved**, and the Human
> Lead **confirmed that framing rather than accepting it as the drafter's**. **Step 8 may launch, and
> Step 8 is the remaining gate.**
>
> **Two things the approval deliberately does NOT do.** It does not rule on **where the unspecified
> bootstrap blocks** — *"blocking Step 9, not Step 8"* is **Red Team's recommendation from its twelfth
> review**, carried as the recommendation it is. And it does not fix the **date discrepancy** it flags:
> the approval is dated **2026-08-13** as the Human Lead gave it, while `0060`–`0063` — including
> `0063`, which carries the **652** that §3 rests on — are dated **2026-08-13**.

**Twenty-nine decision entries (`0035`–`0064`), FIFTEEN Red Team reviews and FIFTEEN HOLDs**, nine dual
runs, **zero API calls throughout**. Gate 4 of 5 was approved twice, reopened twice, and approved a third
and final time.

**The rule was changed and changed back inside one day.** `0052` adopted ALT-MATCHED; `0053` amended
approved gate `0021` to fit it; `0054` reverted all of it — **ALT-MATCHED withdrawn, `0053` withdrawn
in its entirety, `0021`'s amendment reverted, `0048` §9 restored** — and instead **widened the
started-and-left floor** to cover the same 90 pairs. See the ALT-MATCHED section below.

**Why this file exists:** the individual entries are each correct about what they decided. Only the
sequence shows what actually happened, and the sequence is the Step 18 material.

---

## The spine — four rules in succession, and none of them is the first one

| # | Rule | Where | Fate |
| :-- | :--- | :--- | :--- |
| 1 | **A numeric threshold, 632 d** — 99th percentile of the bracketing-gap distribution on the 152,126, interval [528, 787] | `0039` **APPROVED** | **SUSPENDED** by `0040` |
| 1b | **1,293 d** — same rule, extended reference set (open-ended entered as `+∞`) | `0041`, provisional | Never approved |
| 2 | **PF-LIMIT** — not live iff **no insertion after `τ1`**. Threshold **DELETED** | `0042` **APPROVED** | **SUPERSEDED** by `0046` |
| 3 | **ALT** — not live iff no insertion after `τ1` **AND `\|A\| = 0`** | `0046` | **SUPERSEDED** by `0048` |
| 4 | **ALT-BROAD** — not live iff no insertion after `τ1` **AND NOT Continued** | `0048` **ADOPTED**; **restored `0054`** | **Current**, with the S&L floor widened. Gate still open |
| 5 | **ALT-MATCHED** — one silence test per null: `τ1` for never-started, **`τ2`** for started-and-left | `0052` **ADOPTED** | **REVERTED by `0054`** |

**Superseded status line, recorded because it is what went wrong: this memory carried ALT-MATCHED as
*"RECORDED, NOT ADOPTED (`0050` §4)"* through its adoption AND its revert**, and Red Team's eighth
Step 7 review found it. **The full status history is `0050` §4 proposed → `0052` §1 adopted → `0054`
reverted.** It must never be cited as the rule, and it must never be dropped from the record either.

### ALT-MATCHED — adopted and reverted inside one day

**Adopted at `0052`**, on Red Team's sixth HOLD. The argument was ALT-BROAD's own warrant turned
against it: *a pair silent through `[τ1, τ2)` cannot produce the evidence the Continued test reads* —
**that holds identically for a pair silent after `τ1 + ε` for any ε < 91 days**, so the failure mode is
continuous and ALT-BROAD **cut it at one end.** Both arms reran and confirmed every expectation: APPLY
**703 → 793** (604 NS + **189** S&L, 256 accounts), never-started bound unchanged, DERIV **188**, and
instance B confirmed the newly-excluded set **is** the channel set **by index equality, not by count**.

**`0053` then amended `0021`** — an amendment to an approved gate, stated as such — reading *"after the
window"* as *"after the window for the question being asked."* Measured stake: **90 APPLY and 89 DERIV
exclusions show an insertion after `τ1`**, 47.3% of DERIV's whole exclusion set; under `0048` §9's
gloss every one would have been forced live. **That count was 0 under ALT-BROAD**, which is why the
conflict surfaced only then.

**Reverted at `0054`**, on Red Team's seventh HOLD, for three reasons:

1. **It bought nothing.** On all three identified sets, **ALT-BROAD-with-a-covering-floor and
   ALT-MATCHED are numerically identical.** All ALT-MATCHED moved was the point estimate — S&L
   9.7177% → 9.6762% — by deleting the 90 least-robust rows, **and it paid for that with an amendment
   to an approved gate, a contradiction with `0034`, a fragility transfer, and a nine-defect
   propagation wave.**
2. **`0053`'s premise was false.** It claimed the `τ1` anchoring was *"only by accident of when `0021`
   was written."* **`0034` — the entry that created the second window, the same date — ruled it in
   terms: *"Liveness stays anchored at `τ1`."*** `0051` re-affirmed it with both windows in view.
   **`0053` amended `0021` and withdrew `0048` §9 while leaving `0034` standing, uncited and
   unmentioned** — so the adopted rule contradicted a live ruling in an approved gate.
3. **The warrant was false for the pairs it was adopted to capture.** A record inserted at `s` can
   carry any `watched_at ≤ s`, and `0021` Adoption 3 keeps post-dated records — so an account last
   active at `s ∈ (τ1, τ2)` **could** have produced Continued evidence.
   **And the continuity argument is symmetric — it proves no instant in `[τ1, τ2]` is warranted, not
   that `τ2` is.**

> **THE MARGIN ARGUMENT `0054` §3 USED HERE IS WITHDRAWN (`0055` §2) AND MUST NOT BE RESTATED.**
> `0054` supported reason 3 with *"the 90 have **p5 margin 1.7 days, minimum 0.13** — alive for ~89 of
> the 91 days."* **That is the tail. The record's own median for the same 90 is 44.5 days** (`0053` §5,
> instance B, carried in Step 14). **p5 supported the claim, the median contradicted it, and only p5 was
> quoted.** Instance B reproduced **p5 = 1.6552, median = 44.5272 on the same 90 pairs**, confirming the
> cherry-picking arithmetically.
>
> **The correct ground carries no margin statistic at all. A floor is a worst case, not an
> expectation** — the question is whether a channel pair *can* in truth be Continued, and it can: even at
> margin 0.13 days it could have completed S2 inside the unobserved remainder, since the Continued
> condition reads **distinct episodes** and a single binge clears it. **Admissibility sets an endpoint;
> plausibility does not enter. p5 = 1.7 and median = 44.5 are both inadmissible**, and **the median is
> the figure that would have been quoted had the conclusion needed defending the other way.**
>
> **Both arms went further than `0055` §2 and argued the whole CLASS out of endpoint justification.**
> **A:** admissibility is **binary**, a margin is **continuous**, so **no margin value can discharge the
> question** — its test is *"would the statistic at any value move the endpoint? If not, it is
> commentary."* **B:** admissibility is a property of the **support**, plausibility of the **measure**,
> and `p5 = 1.7` **removes zero pairs from the admissible set** — and the argument would **reintroduce an
> unowned threshold into the one step whose entire history is the removal of exactly that shape.**
> Margin statistics belong in Step 14 as a statement about **resolving power**, nowhere else.

> **`0054` §3 names the error class of this whole chain: *correcting a predecessor by overshooting
> into the mirror-image defect.*** That belongs in Step 18 beside the five-entry cascade below.

**The sweep neither arm was asked for** (`0054` §4, `src/step7_anchor_sweep.py`, zero API calls) swept
the silence anchor `τ1 → τ2` with never-started held at `τ1`: APPLY S&L **99 → 108 → 120 → 143 → 154 →
174 → 189**; APPLY total **703 → … → 793**; DERIV S&L **99 → … → 188**. **Smooth and monotone. No
elbow, no plateau, no natural cut anywhere in the interval** — which is precisely why **the bound must
be widened rather than a cut chosen.**

**What survives the revert:** the widened started-and-left floor **[9.6372%, 10.0405%] on APPLY**, the
Continued ceiling moving **73.6537% → 73.6995%**, `0053`'s **nine defect fixes where rule-independent**,
and two new Step 14 limitations — the 90 are by construction the pairs closest to their own boundary
(margin median **44.5 days** against the 604's **202.5**), and **D10 admits `τ2 = τ_pull`**, so 20 APPLY
pairs have a zero-length post-`τ2` window and 2 are excluded by construction.

**PF-BRACKET** is a fifth name in the record and was never a candidate: it is the *literal reading*
of `0041` §4's withdrawn wording, priced at 18,903 exclusions from 1,434 of 2,402 accounts. It exists
only to show what the wording would have cost.

---

## Fifteen Red Team HOLDs — and the division that carried the approval

> ## **REVIEWS 1–8 CONTESTED THE RULE. REVIEWS 9–15 CONTESTED THE RECORD.**
>
> **1–8 changed what is measured:** the bias-2 sign correction, the withdrawal of *"no free parameter"*,
> the derivation and then **deletion** of the numeric threshold, four rule generations, the widened
> floor, and the `τ1` anchoring.
>
> **9–15 found propagation and control defects in figures derived from an UNCHANGED rule. Not one
> changed the rule, the population, the exclusion counts, or any bound endpoint on its own arithmetic.**
> They changed **where numbers were written, which numbers were checked, and whether a claim about a
> check was true.**
>
> **`0063` §4: that distinction is the case for approval AND the case for the caveats** — *"the analysis
> has been stable for eleven consecutive reviews, and the machinery around it has needed seven entries
> to catch up."*
>
> **The rule statement was uncontested from review 5.** From review 8 Red Team explicitly **cleared** the
> `τ1` anchoring, the ALT-MATCHED revert, `0021`'s restoration and `0048` §9. **In reviews 12, 13 and 15
> it independently recomputed the arithmetic** — both partitions, all four widths, both attainable
> corners to exactly 100%, the excess identity, all six sampling ratios — **and confirmed it each time.**

### The one substantive challenge after review 8, and it closed on measurement

**Review 15 moved off the record and back onto the rule** for the first time since review 8. Its
argument: conjunct 2 is `NOT Continued`, so **the filter is outcome-conditional** — a silent pair is
excluded iff it is not Continued, and **Continued pairs are structurally unexcludable.** Its proposed
alternative, *"the one nobody has priced"*: **drop conjunct 2.**

**The premise fails. `0063` §1: the alternative IS PF-LIMIT** — adopted at `0041`/`0042`, superseded at
`0046`/`0048`. *"The rule family was tested against exactly this alternative, before ALT-BROAD existed."*
And **the 652 it asked for has been printed in the record since `0045` §1**, whose table gives PF-LIMIT's
DERIV split as `751 = 0 never-started + 652 Continued + 99 started-and-left`.

| | n | ALT-BROAD | **cont ∧ silent** | no conjunct 2 | growth |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **APPLY** | 196,654 | 703 | **652** | **1,355** | 1.93× |
| **DERIV** | 147,370 | 99 | **652** | **751** | 7.59× |

**The pricing settles it.** Dropping conjunct 2 excludes **652 Continued pairs — pairs satisfying
`F2 ∈ A_H` and `|A_H| ≥ ceil(0.90 × L2)`, on evidence they demonstrably produced.** Liveness exists to
stop a null being trusted when the account may have been dead; **Continued is not a null.**

**What survives is not nothing: the size of the outcome-conditioning is 652 on BOTH populations**, now
**measured rather than argued**, publishing with the Step 14 limitation instead of standing as an
unquantified concern. **`0063`'s own closing line on it: *"the objection is answered in the direction that
keeps the rule, and the number that answers it is one Red Team could have read."***

### The eight rule-contesting HOLDs

| # | Entry | What it turned on |
| :-- | :--- | :--- |
| **1** | `0040` | **`0036` §2.3(ii) contradicted an approved gate.** `0021` (gate 2 of 5) holds that any record inserted after the window closed **proves the account was alive**; `0036` ruled the "no instant at or before `τ1`" bucket **dead**. Every pair in it has instants after `τ1` **by construction**. **18,250 pairs — 76.8% of the filter's exclusions.** Nothing in `0036`–`0039` cited `0021` against it |
| **2** | `0043` | **Step 14's bias-2 sign was wrong**, in the study's central honesty artifact. The ledger said the liveness exclusion moves never-started **DOWN**; measured, it moved **UP**, because the filter preferentially deletes **confirmed continuers**. Instance B had named it — *"the filter is not selecting on the outcome it was built to protect"* — and it was not acted on until Red Team made it blocking |
| **3** | `0044` | **"No free parameter" is not what the evidence shows.** Deleting the threshold *made the coupling total*: PF-LIMIT's exclusion set **is** the open-ended bucket, a pure function of `W`, and **`W` was held at 108 for the entire sensitivity test that justified the deletion.** Plus **propagation failure #6** — neither `analytics-engineer` file stated the rule, and they are the first files the Step 8 instances read |
| **4** | `0046`, `0048` | **The not-live branch had no stated warrant.** `0021` licenses *insertion after `τ1` ⟹ live* — a **sufficient** condition, not the biconditional. Held three times; the third was dispositive. `0046` answered it by adopting a rule the warrant reaches; `0048` found the answer still stopped short |
| **5** | `0050` | **Propagation failure #9 — six defects live in all five files, produced by `0048` and `0049` themselves.** `0049`'s header asserted a five-file pass that did not happen. **Both members of every pair carried each defect identically**, so the dual diff would have shown agreement |
| **6** | `0052` | **The residual channel had a warrant problem, not just a size.** Answered by adopting ALT-MATCHED — **later reverted.** The same review exposed **`0051` §2's wrong V7 correction**, propagation **#12** (Step 9's two mandated sentences reached `task-sheet.md` and **neither** `data-scientist` file), the surviving 1.5× coupling figure, and the A-vs-B ratio divergence |
| **7** | `0054` | **The rule change bought nothing.** ALT-BROAD-with-a-covering-floor and ALT-MATCHED are **numerically identical on all three identified sets**, and `0053` had amended an approved gate **while leaving `0034` — the ruling that forbids the re-anchoring — standing and unmentioned.** Reverted. Also propagation **#13**: both `analytics-engineer` files carried *"EXPECT 793"* and *"EXPECT 703"* **ten lines apart**, and `task-sheet.md` Step 9 **never received `0053`'s pass at all** |
| **8** | `0055` | **A seventh propagation surface exists and is never checked — `second-brain`'s memory** — and `artifacts/` is the sixth and was not either. Answered by `CLAUDE.md` §Propagation: **seven surfaces, read-back PLUS grep.** The same review found **`0054` widened APPLY and left DERIV**, its own §1 identity implemented on one population of two |

### The seven record-and-control HOLDs — reviews 9 to 15

**None changed the rule. All seven are about the machinery around it.**

| # | Entry | What it turned on |
| :-- | :--- | :--- |
| **9** | `0056` | **An endpoint moved and the four figures computed from it did not** — the same failure as `0054`, **one entry apart, and neither caught by the control written in between.** The sub-interval floor moves with the bound floor: the conditioning constrains the **604** and says nothing about the **90**. **`9.6830` de-registered — it has no legitimate reading** |
| **10** | `0057` | **The `.json` half certified what the `.md` half withdrew.** Both JSONs still carried the first stamp and *"everything_else_stands"* — **verbatim the sentence `0056` §4 had ruled false.** `0056`'s *"every occurrence is marked inline"* was **false in both files**: `bb-a.md:219` headed **OPERATIVE** four lines above the withdrawn floor; `bb-b.md:216` presented **the withdrawn non-covering bound as the arm's recommendation, in the file the gate reads.** That is **the fourth asserted-but-not-taken action in three entries, and this one was inside the correction for the third** |
| **11** | `0058` | **The METHOD was the defect.** `0057` §1's *"fifteen values corrected in each file, listed and verified individually"* is **false** — the patch matched on a key whitelist and **walked past three regions**, including *"the ratio, missing both its operands."* **Hand-patching abandoned.** Also: **the dates.** `0052`–`0057` were all dated **2026-08-13**, a day ahead, from a clock that advanced mid-work; **corrected in place with a note, not silently rewritten** |
| **12** | `0059` | **B1: the regeneration INVERTED the failure it was written to end** — it wrote both operands and left the quotient. **B2: the whole-file exemption exempted the entire Step 7 artifact set, including both OPERATIVE deliverables.** **B3: there were TWO hand-maintained registers, already divergent, and NEITHER contained the values that were actually wrong** |
| **13** | `0060` | **B4: the defect fixed in one quotient and reproduced in the other, same commit.** The never-started ratio was **written by the script and checked by nothing.** **B5: an entry asserting a control property the control did not have** — a string replace that failed to match and was not asserted on, **the third consecutive blocker of that exact shape.** **B6: the value scoping was written and UNREACHABLE** |
| **14** | `0061`, `0062` | **B8: a withdrawn sentence struck where humans typed it and left where the SCRIPT types it**, so the generator wrote it back to all four operative files every run — **and both controls were structurally blind to it.** **B9: `check_ratios_written()` skipped arm b in full and reported OK** |
| **15** | `0063` | **The rule objection** — drop conjunct 2 — **closed on measurement: it is PF-LIMIT, and it costs 652 Continued pairs.** Everything else **logged as outstanding, deliberately not fixed.** Plus **2.5: a width computed as a difference of two rounded percentages**, the exact construction the register names as a rounding artifact. *"The register held the diagnosis and the generator committed the disease"* |

**Red Team's standing contribution here is not a number. It is that FOURTEEN of the fifteen HOLDs were
against the *record*, not the *rule*.** Only HOLD 4 attacked the rule itself, and it is the one that
changed it twice. **HOLD 15 attacked it again and was answered with a number that was already in the
record.**

**HOLD 6 and HOLD 7 are a matched pair and Step 18 should present them that way:** the sixth found a
real defect and the repair adopted was the wrong one; the seventh found that the *right* repair —
widening a bound — had been rejected by `0052` §4 **for the very reason it fixed**. *"That is exactly
backwards: widening to 18,952 is what makes the endpoint covering."*

---

## Why the threshold was deleted — the headline could not tell 787 from 2,200 days

| Setting | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 787 d | 6.2109% | 82.3812% | 11.4078% |
| 1,293 d | 6.2325% | 82.3497% | 11.4178% |
| 2,200 d | 6.2373% | 82.3490% | 11.4137% |
| Parameter-free | 6.2373% | 82.3427% | 11.4201% |

**Max movement across all four: 0.026 / 0.038 / 0.012 pp — about 3% of the account-clustered
sampling width** (0.78 / 1.25 / 0.99 pp at B = 4,000). A continuous 30–4,000 day sweep moves nothing
beyond 0.243 pp. **Both arms produced these independently and identically to four decimal places.**

**These levels are on DERIV and are NOT results.** `0042` §5 and README item 47 both say so: Step 8
applies liveness to APPLY, whose extra lines carry contaminated `T0`. **The absolute shares move; the
flatness finding does not**, because the exclusion sets are under 1% of the population either way.

**One delta is statistically distinguishable and still immaterial:** the paired clustered CI for
787→2,200 on never-started is [+0.008, +0.046] pp, excluding zero, because nested subsets give
near-zero paired variance. **Detectable, not material** — instance A reported both facts rather than
the convenient one.

**The deeper reason is the quota property** (`0038` §4): a percentile of the distribution the test is
applied to sets the level **by the exclusion rate, not by any feature of the data**. Instance A:
*"a quota rather than a finding."* **There was never a number to find.**

**What the three derivations bought** (`0042` §7): deriving it three times is what established that
it does not matter. Along the way the same work exposed a rule contradicting an approved gate on
76.8% of its exclusions, a reference distribution calibrated on one population and applied to
another, an impossible invariance claim, and a wording that reinstated a withdrawn rule.

---

## The warrant that finally selected the rule

This is the one argument in the whole sequence that did analytical work, and it is short:

> **Liveness licenses trusting a null.** A pair whose outcome rests on positive evidence has nothing
> for liveness to protect.
>
> **Under `0034` only Continued rests on positive evidence** — `F2 ∈ A_H` and
> `|A_H| ≥ ceil(0.90 × L2)`.
>
> **Never started is a null.** **Started-and-left is ALSO a null — on exit.** `|A| ≥ 1` is observed;
> the *failure to meet the Continued condition* is not.
>
> **And it is structural, not incidental: `τ2 > τ1`**, so a pair silent after `τ1` is silent after
> `τ2` and **can produce no evidence anywhere in the `[τ1, τ2)` window the Continued test reads.**
> It is scored "left" **by construction** — the exact failure liveness exists to prevent, applied to
> the second headline category.

**This is why the gate ended where it did.** PF-LIMIT reached past the warrant (751 deletions with no
stated reason); ALT stopped short of it (guarded one null of two); ALT-BROAD is the rule the warrant
reaches. `0048` §4 puts it symmetrically: *"a gate whose deliverable is 'the rule statement' cannot
close on a rule half of whose deletions have no stated reason"* — **and it applies equally to a rule
that stops short of its own stated reason.**

**The warrant is an argument, not a measurement.** Instance B said so in those words, and it is why
Red Team's item 2 is **narrowed, not closed**, and now sits in Step 14 as a limitation: `0021`
licenses one direction of a biconditional. ALT-BROAD narrows where the unlicensed assertion is made
from 1,355 pairs to 703. **It does not justify it.**

---

## Twenty-one propagation failures, and the controls they produced

> **`#1`–`#18` ARE A SURFACES-1–5 COUNT AND MUST NEVER BE PUBLISHED AS A TOTAL** (`0057` §7). Surfaces 6
> and 7 were added **after** the count was fixed, and their failure rate was *"unmeasured, not zero."*
> **It is now measured and non-zero at three: #19** the stamp that certified superseded figures, **found
> inside the fix added for surface 6**; **#20** both `.json` halves left behind while the `.md` halves
> were corrected; **#21** `open-items-and-contradictions.md`'s blessed sub-interval — **this memory.**
> **The count is not renumbered. Whether to restate it against seven surfaces is the Human Lead's call.**

**`#14`–`#18`, from `0055` and `0056`:** #14, `task-sheet.md` Step 7 carrying *"anchored at `τ1` and only
at `τ1` is WITHDRAWN"* **28 lines below the line restoring it**; #15, ALT-BROAD's per-arm series
**labelled "ALT-MATCHED"** at Step 13 with the 1.5× coupling `0052` had recorded as fixed in three files;
**#16, the severe one** — both `data-scientist` files, byte-identical, carrying `[9.6830%, 10.0405%]`,
`1,307` / `100.6646%`, and ***"Continued 73.6537% (73.6995% was ALT-MATCHED's, withdrawn)"***, which
**tells an instance the ADOPTED ceiling is withdrawn, so an instance following it deletes a correct
number** — `0052` §2's failure exactly; #17, four Step 14 bullets publishing ALT-MATCHED's limitations as
current, citing withdrawn `0053`, restating the **70.3%** channel figure and PF-LIMIT's **0.032 pp** four
lines above the sentence forbidding it; #18, the derived-figure wave `0056` fixed.

**Two of #17's bullets were not merely stale but FALSE under the restored rule** — D10 admits
`τ2 = τ_pull`, so ALT-MATCHED had 20 pairs with a zero-length post-`τ2` window and 2 excluded by
construction, **which at `τ1` cannot arise** because D10 forces `τ1 ≤ τ_pull − 91 days`; and clamping,
recorded as **not** inert at `τ2`, **is** inert at `τ1`. **`0053` ruled the old form *"must not be
restated"*; at `τ1` the old form is the correct one.**

**And `0049` §6's launch-snapshot control did not cover any of this. It governs THE RULE. The bound is
not the rule** — the third control added to the propagation problem does not reach the thing that broke.

### The original thirteen

**A ruling lands in a decision entry and not in the file the agents read.** README item 46, which
still says "five times now."

| # | The miss | Caught by |
| :-- | :--- | :--- |
| 1 | Ten decisions to `task-sheet.md`, none to `.claude/agents/` | `second-brain`, `0035` |
| 2 | `0034`'s three Step 10 requirements: in the approved text, in no spec | `second-brain`, `0035` |
| 3 | `0036` applied to the Step 7 bullet body, not its "NOT LAUNCHED — UNRULED" header | instance A |
| 4 | `0039` corrected `0038` §5 and not `task-sheet.md` line 248 | Red Team, `0040` |
| 5 | `0040` corrected four task-sheet figures and **missed line 266 — the one that sets the threshold** | both arms |
| 6 | Neither `analytics-engineer` file stated the liveness rule — **the files Step 8 reads first** | Red Team, `0044` |
| 7 | The withdrawn "vary the liveness threshold" survived in the two files `0044` had itself named | `0046` |
| 8 | Five stale `task-sheet.md` lines, incl. **line 332 carrying the superseded bound as operative Step 9 instruction** | `0048` |
| 9 | **Six defects in all five files, produced by `0048` and `0049`**; `0049`'s header claimed a pass that did not happen | Red Team, `0050` |
| 10–11 | **V1 and V5–V6**: the superseded ALT per-arm series live at Step 13 in both `data-scientist` files; `task-sheet.md` Step 14 restating a figure it withdraws four lines below | `second-brain`, into `0051` |
| 12 | **Step 9's two mandated sentences reached `task-sheet.md` and NEITHER `data-scientist` file** — verified by grep returning zero matches across `.claude/agents/`. Step 9 is dual, `CLAUDE.md` sends the agent to its definition file, **and both copies carried the same omission, so the diff structurally could not see it** | `0052` §5 |
| 13 | **Both `analytics-engineer` files carried "EXPECT 793" at line 77 and "EXPECT 703" at line 88** — two mutually exclusive instructions ten lines apart, each declaring the other's number a divergence, **identical in both copies**, in the file **Step 8 launches from**. **And `task-sheet.md` Step 9 never received `0053`'s pass at all** — still carrying 703, the non-covering bound, 73.6537% and 100.6646%. That is #12 **repeated one entry later in the same section** | `0054` §5 |

**#12 and #13 are the same defect one entry apart, and both were produced by the entry that fixed the
previous one.** That is the propagation analogue of the self-correction cascade below.

**The four controls, each added because the same failure recurred somewhere new:**

1. **Item 46's five-file surface** (`0044` §3.1). *The propagation surface is `task-sheet.md` plus
   the four pipeline agent definitions, and an entry that changes a rule must state which of the five
   it touched and which it deliberately did not.* **A ruling that names no files has not been
   propagated, whatever the entry says.**
2. **`0046` §0's population rule.** *Every figure in a decision entry states which population
   produced it, at the point of use. An entry that cites a number without its population is not
   propagated.* Written after three consecutive entries each corrected the previous one and **each
   committed the same error.** Extended by `0047` §3 to interval endpoints: *an endpoint states the
   population it is computed on and the estimand it bounds, and they must be the same population.*
3. **`0049` §6's agent-launch snapshot practice.** An agent's definition is **snapshotted at
   launch**, so a file edited and an agent launched in the same turn can disagree and **the agent
   cannot see it is holding an old copy.** *Every launch prompt for a spec-bearing step states the
   operative rule verbatim and tells the instance that where its definition disagrees with
   `decisions/` or the on-disk `task-sheet.md`, the on-disk file wins.* **The launch prompt, not the
   definition file, is the authority at launch.**

4. **`CLAUDE.md` §Propagation, 2026-08-13 — SEVEN surfaces, and read-back PLUS grep.** The five-file
   surface is now seven: **`artifacts/`** (surface 6, deliverables carrying superseded figures are
   stamped) and **`.claude/agent-memory/second-brain/`** (surface 7). **Neither was ever checked before
   2026-08-13.** And: *"Read-back alone is not verification. Reading an edit back proves the new text
   landed. Only grep proves the old text is gone, and a file can hold both at once — three consecutive
   propagation failures were exactly that."* Require **zero grep hits** on every superseded string
   except where explicitly named as superseded at the point of use, and **report the hit counts.**

5. **The positive counterpart to the grep** (`0055` §3). **A figure that was never written returns zero
   hits on every superseded form of itself** — the DERIV bound existed on no surface, so the mandated
   negative grep would have reported a clean pass on a file set containing the defect. **Grep the
   CORRECTED string and require non-zero.** *Added to `CLAUDE.md` by the agent that found it, on its
   first run under control 4.*

6. **Regeneration, not hand-patching** (`0058`–`0062`). **Four consecutive decisions patched values by
   hand and every finding in reviews 9, 10 and 11 was a value a patch reached in one file and missed in
   another.** *"Eleven entries of one error class is a method that cannot converge."* Now: **one
   register** (`src/step7_register.py`), **one expression per derived figure** written into both halves
   of both arms, **numeric matching at both precisions** plus a **withdrawn-phrase half**, **dependency
   lists that close to FIXPOINT**, and —

   > **A CHECK THAT FINDS NOTHING BECAUSE IT LOOKED NOWHERE MUST FAIL (`0062`).** `check_ratios_written()`
   > read a key arm b does not use, was allowlisted for its absence, **checked zero rows and returned an
   > empty failure list — which reads identically to "everything is right."** **An empty result and a
   > clean result are the same value, and only the control knows which it produced.** Four more of the
   > same shape were found in one audit. **This was the third control in six entries that reported clean
   > while looking at nothing.**

**`0050` §0 adds the practice control, unnamed but standing:** every edit verified by reading the file
back, with the verification in the transcript. It exists because `0049` recorded a pass it had not
done — **and control 4 exists because read-back by itself let #13 through.**

> **The recurring shape across controls 4, 5 and 6, and it is the Step 18 material:** *four
> asserted-but-not-taken actions in three entries* (`0057` §2), **the third consecutive blocker of that
> exact shape** (`0060` B5), **a fourth docstring asserting a code property the code lacked** (`0062`
> §4). **An entry that says a check was run is not evidence the check was run**, which is why `0060` B5's
> correction now **asserts itself** — four `assert _dead not in MARK.pattern` lines run at import, *"so
> this claim cannot go stale silently again."*

> **Surface 7 is why this file matters beyond continuity.** `0052` §2: this memory mislabelled the
> Continued ceiling **73.6537%** *(itself SUPERSEDED by 73.6995%, `0054`)* as a *"Continued floor"* and concluded it could not be reconstructed;
> **`0051` §2 adopted that diagnosis without checking it against the arms' own JSON** — *"the exact
> failure `0046` §0 exists to prevent, committed in the entry that corrected two other instances of
> it"* — issued a wrong correction, and **a Step 9 instance reading the corrected line against its own
> deliverable would have deleted a correct number.** **Stale memory is not a filing problem.**

> **The dual-implementation control cannot catch this class at all.** Both halves of every pair
> carried each `0050` defect identically. `0035` §1 is the general statement: *a dual pair whose two
> halves read the same stale brief produces a clean diff and a wrong answer.*

---

## Repeated self-correction failure — five consecutive entries, each correcting its predecessor and each introducing a defect

**This is the pattern most worth carrying into Step 18, because it is a property of the process and
not of any one entry.**

| Entry | Corrected | Introduced |
| :--- | :--- | :--- |
| `0042` | `0041` §4's wording | §4 quoted **the deleted 1,293-day rule's** deltas as the approved rule's |
| `0043` | `0042` §4's deltas, and bias 2's sign | Published the **DERIV** direction as the study's; prescribed a remedy on "~40 never-started exclusions" that **are zero**; merged two claims into "six in seven" |
| `0045` | `0043`, three ways | Rejected ALT on **the DERIV row, where ALT is zero by construction**; published a bound that **mixed denominators** and whose floor was not a floor |
| `0046` | `0045`'s rejection and its bound | §1's two explanations both wrong; §4's bound **mixed denominators again**; §7 too pessimistic; §2's table called 99 null-based pairs "directly observed" |
| `0047` | `0046` §1, §4, §7 | **Missed `0046` §2's "751 directly observed"** — caught one entry later by Red Team's fourth review |

**And it did not stop at five. Three more entries continued it, and the eighth is the one that reached
furthest:**

| Entry | Corrected | Introduced |
| :--- | :--- | :--- |
| `0051` | V1–V7 and housekeeping | **§2 declared 73.6537% *"on no population"*** — it is the Continued ceiling, both arms publish it, both JSONs carry it. **Adopted `second-brain`'s stale memory as a diagnosis without checking the arms' JSON**, and **attributed the number to Red Team while doing so.** The "correction" left `task-sheet.md` presenting Continued as a **point** |
| `0052` | `0051` §2 entirely; the channel figure; four more | **Adopted ALT-MATCHED**, reverted two entries later. **§4 rejected the widened floor for the reason the widened floor repairs.** Its §4 floor 9.6373% and §7 figure 6.2096% both wrong |
| `0053` | `0052` §4, §7 and nine defects | **Amended an approved gate on a false premise, leaving `0034` uncited.** **Mandated population labels and then omitted them four rows above the row that requires them.** Wrote ALT-BROAD's DERIV bound miss as 0.0041 against both arms' 0.0042. **Withdrawn in its entirety** |

**And it ran another eight entries. The cascade is the longest single pattern in the study.**

| Entry | Corrected | Introduced |
| :--- | :--- | :--- |
| `0054` | `0053` entirely; the rule restored; the floor widened | **§7 published `0.4033`, the artifact its own §6 had just named as one.** **Widened APPLY and left DERIV** — its own identity implemented on one population of two. Supported the floor with a **cherry-picked p5** |
| `0055` | `0054` §1, §3, §6, §7, §8 | Its §5 heading said *"Three"* above **four** bullets; its §5a asserted *"is stamped"* for **a step not taken** — *"the error this entry exists to control, committed inside it for the second time"*; its §5c added a register row **that was not added**; it corrected **four** derived figures and registered **one** |
| `0056` | `0055` §3, §5, §5c; `0052` §6 | **Claimed every occurrence marked inline — false in both files**, with the withdrawn bound sitting under an **OPERATIVE** heading and as an arm's **recommendation**. Left both `.json` halves untouched. Propagated to *"the glossary"* and **reported it as surface 7, which is the DIRECTORY** |
| `0057` | `0056` §4, its header, §5 | **§1's *"fifteen values corrected, listed and verified individually"* is FALSE** — a key whitelist walked past three regions, and *"reached the ratio and missed both its operands"* |
| `0058` | `0057` §1, §2; the dates | **Reverted the ratio reconciliation in the entry and not in the body**, leaving `0.509` in arm a. **Published the ~~"which is the proof"~~ sentence — WITHDRAWN at `0060` §2** — itself an instance of the defect it certified |
| `0059` | `0058` §2, §3 | **Created four ratio target paths and asserted ONE** — the never-started quotient written by the script and checked by nothing, *"the identical structure to the hard-coded literal it had just replaced."* **Republished the "proof" sentence.** §2 asserted a `MARK` property `MARK` did not have |
| `0060` | `0059` §1, §2; `0058` §3 | **§1's coverage claim was true for arm a only** — arm b was skipped in full. **§6 recorded the JSON-string limit as *"not a defect today"* while it was ALREADY LIVE in all four operative deliverables** |
| `0062` | `0060` §1 | *"Every derived figure"* is **false by four** — the sub-interval ratios sit outside every control (`0063` §3 item 2.2) |

**`0063` broke the pattern: it fixed one thing (widths from counts) and LOGGED THE REST AS OUTSTANDING
rather than correcting it under a blocking review.** Given twelve consecutive entries in which the
correcting entry introduced the next defect, **that is the change of method, and Step 18 should say so.**

**Instance A's line, from inside `0045`: *"the seventh instance, inside the entry correcting the
sixth."*** The named error class is **a figure measured on one configuration or population, quoted as
if measured on another** — `0038` §5, `0039` §2, `0039` §6, `0042` §4, `0043` §2, `0045` §4.1, and on.

**The cascade's final lesson, from `0054` §3, and it is different from `0046` §0's:** the failure is
not only *reaching for the number that supports the ruling*. It is **overshooting into the mirror-image
defect** — `0052` answered "ALT-BROAD cut a continuous failure mode at one end" by cutting it at the
*other* end, on an argument that proves neither end is warranted. **`0054` §7 then published `0.4033`,
the rounding artifact its own §6 had just named as one, one page apart.** Eleven entries in, the
correcting entry is still the highest-risk place in the log.

**`0046` §0 names the cause and it is not inattention:** *"It is reaching for the number that
supports the ruling being written rather than checking which population produced it."*

**Three consecutive bounds had an endpoint outside the feasible set** (`0047` §3): `0043`'s ceiling,
`0045`'s floor on the other side, `0046`'s floor on a mixed denominator. **The fourth was refused —
by both arms, independently, before the ruling** (`0049` §2). Instance A named the stake: the narrow
S&L reading *"would have made this the fourth consecutive bound failing that exact test."* **The
standing rule worked before it could be broken a fourth time, and it worked in the arms rather than
in the ruling.** That is the one clean win in this sequence and Step 18 should say so.

---

## What the dual runs actually bought, and what they did not

**`0040` §7 is the honest statement and it should survive into the write-up:**

> **Exact agreement between the two arms is WEAK evidence of correctness.** Every published quantity
> is a deterministic function of frozen inputs — the same cached sweep, the same stored calibration
> neither arm refits, an exactly-specified collapse rule, a named percentile, a named population.
> **Agreement was `0038`'s design goal.** It confirms the spec is unambiguous; **it cannot confirm
> the spec is right.**

**What the diffs did buy, in order:** 4 days apart on the gap unit (`0037` §4) → 410 days apart on
the reference population, 504 vs 914 (`0038` §1) → 787 vs 790 on a bootstrap endpoint, inside
measured seed noise (`0041`) → exact agreement thereafter. **Each divergence was a spec ambiguity,
and each was closed by naming the operation rather than describing it.**

**Under ALT the DERIV diff was literally `0 = 0` at every arm from 38 to 213** — on the population
Step 7 is defined, derived and reviewed on. Red Team's formulation: *a gate cannot close on `0 = 0`
when a measured alternative, selected by the gate's own stated warrant, makes the control informative
and has never been ruled on.* **ALT-BROAD makes it 99 against 99 on 73 accounts — informative for the
first time in this step.**

**The never-started bound is still degenerate on DERIV — [6.2055%, 6.2055%] — so that control is
`x = x` there** (`0050` §3). The informative comparison is on APPLY.

**The bootstraps became diffable for the first time at the `0053` run** — both B = 4,000,
account-clustered, both levels and movements, seeds stated. Before that they were **not diffable at
all** and nobody had said so: A used B = 4,000 / seed 20260813 / **movements**, B used 2,000 / seed
20260814 / **levels**, and *"the spec fixes neither and Step 9 must attach confidence intervals"*
(`0052` §6). **That gap survived `0049`, `0050` and `0051` unactioned while the gate's own Check line
is "dual implementation diff."**

**Two divergences reported and NOT reconciled, per `CLAUDE.md`** (`0054` §6):

- **Robustness survival: instance A finds 792 of 793, instance B finds 791** — off by exactly one on
  each population, **consistent with a `≤ τ_pull` restriction A states and B does not.** A spec
  ambiguity; **neither arm flagged it and neither did `0053`.**
- **Bound width: A gives 0.4032 pp exact (`793/196,654`); B gives 0.4033 pp differenced from rounded
  endpoints and computes its ratios from it.** `0053` §6 promoted B's 52.7% ratio into the record;
  **it is a rounding artifact and is withdrawn.**

**Also reconciled, and it is A's figure: the bound-versus-sampling ratio is 45%, not 6%** (`0052` §6).
B computed its 6% on the conditional sub-interval **it had itself argued is not the bound** —
understating the systematic range against sampling error by **7.5×** and contradicting its own §4.2.

**Both arms repeatedly argued against their own recommendations**, which is the reason the rulings
had the evidence they needed: A recommended adopting ALT and named that it *"empties the unwarranted
branch without warranting it"*; B recommended against ALT-BROAD and had already refuted its own
argument elsewhere in the same artifact, calling ALT's clean sign *"an arithmetic identity, not
evidence."*

---

## Two things recorded and not repaired

- **The 38,696 clock-mismatch bucket** (`0037` §3). `T0` is built from claimed `watched_at`; liveness
  runs on insertion time. The median pair's `τ1` falls **1,578 days before the account's first-ever
  insertion instant**, and 8,037 pairs have `τ1` before the calibration curve starts. **These are not
  absent users — they are pairs whose window closed before the account existed on the insertion
  clock.** Routed to Step 14. Note this bucket was subsequently *returned to the population* by
  `0040` §1, so its residue is a limitation, not an exclusion.
- **The un-guarded channel, 297 pairs** (`0050` §4, **remeasured at `0052` §3**). The warrant holds
  identically for a pair silent after `τ1 + ε` for any ε < 91 days — **the failure mode is continuous
  and the rule cuts it at one end.** Last insertion in the channel sits at median 51.4 days past `τ1`,
  p90 85.1, max 90.9 — filling the window.
  **The channel figure is 52.4%, not 70.3%.** *`0050` §4's "ALT-BROAD closes 703 of 1,000 such pairs
  (70.3%) and leaves 29.7% open" is **superseded** and must not be restated.* **Its denominator pooled
  two categories with different coverage:** the channel's **207 never-started pairs are not in the
  gap** — never-started is the null `|A| = 0` read at **`τ1`**, and **every one of the 207 has an
  insertion after `τ1`**, which is exactly what `0021` licenses. **The added warrant implicates only
  the 90 started-and-left pairs.** On the implicated set alone **ALT-BROAD closes 99 of 189 — 52.4%,
  leaving 47.6% open.**
  **And `0050` §4's disposition of the 90 — *"treated as observed by the new S&L bound"* — did not
  carry its own consequence.** `0052` §4 carried it: if the 90 in truth continued, the S&L numerator is
  18,952 and the floor is **9.6372%**, below the then-published 9.6830%. **`0054` widened the bound to
  cover them** rather than deleting them, which is where the gate now stands.

## The calibration residual — discharged, with its limit

`0049` §5, the last item standing under the rule's first conjunct, which **is** a comparison between
an interpolated instant and `τ1`.

- **22.68%** of dated records (6,271,584 of 27,656,434) claim a `watched_at` **later** than their own
  calibrated insertion instant.
- **Clamping is inert — a clean discharge.** Clamp value **2026-08-10T20:48Z**, while D10 forces
  `τ1 ≤ 2026-05-12` at every arm, so **0 of 66,961 APPLY pairs on clamped accounts are excluded.**
- **Sound at the mass, not in the tail.** Residual is **bimodal**: median ≈ 0.02 d, p90 ≈ 0.107 d,
  upper tail 77–125 d. At the ~91% mass the exclusion set is stable (703 → [701, 703]); at ±7 d,
  [686, 717]; **at ±124.6 d, [414, 1284].**
- **Direction-only cross-check: 700 of 703 APPLY exclusions survive and none is created.** Only 3 of
  703 excluded pairs' accounts claim any `watched_at` after `τ1`.
- **The stated limit: the started-and-left component is the fragile one.** Median margin **81.3 days**
  against **202.5** for never-started, spans **19×** under tail residual against 2.5×, and **525 of
  703 sit on accounts whose last record is a `watch`, where the residual is not directly measurable.**
- **All stability figures are `W = 108` only.** Step 13 runs to `W = 213`, where the exclusion set is
  864 and the S&L component 148.

---

## The channel window — fixed to `(τ1, τ2)`, OPEN at `τ2`. It was settled, not ambiguous

**Carried as "unspecified" through four reviews**, after both arms independently found the spec writing
it `(τ1, τ2]` in one place and `(τ1, τ2)` in three, **measured it inert at `W = 108` — zero pairs sit
exactly at `τ2`, verified rather than assumed — and both reported it unspecified rather than picking
one.** That is the dual run working.

**`0057` §5: Red Team is right that the adopted warrant decides it, and the argument is short enough
that carrying it was the error.** A pair is conceded because, silent from insertion instant `s`, **it
could have generated Continued evidence in the unobserved remainder `(s, τ2)`. At `s = τ2` that
remainder is EMPTY** — nothing admissible is missing, so the pair must **not** be conceded. The adopted
scope statement gives the same answer by a second route: *dormant **before** the instant at which its own
state-defining null is read* — **a pair inserting AT `τ2` was not dormant before `τ2`.**

**So `(τ1, τ2]` was WRONG, not ambiguous, and it erred by conceding a pair with zero unobserved
remainder — past what admissibility licenses**, which is exactly the overreach a floor may not commit.

**Fixed then rather than at Step 13, for a reason that does not depend on taste.** Both arms measured the
two forms inert at `W = 108`; **that does not transfer.** D10 forces `τ1 ≤ τ_pull − 91 days`, so at
**`W = 213` the surviving tail has `τ2` at or adjacent to `τ_pull` — and `τ_pull` is where a MASS POINT
in last-insertion instants sits.** *"Inertness was measured against an interior boundary; at 213 the
boundary is the data's own edge."* **`src/step7_floor_extremes.py` now computes the open form and
ASSERTS the inertness rather than assuming it**, written to fail at any arm where it stops being inert.
**Carried defect: `specs/step7-deriv-floor-verification.md`'s Background still says `(τ1, τ2]`** —
a completed task's brief, not a live instruction (`0063` §3, DF-3).

---

## The residual, as APPROVED — published, not resolved

**The approval is UNCONDITIONAL. Nine items are open and publish with the result. None is a condition on
the gate and none gates Step 8.** Full list at `artifacts/step7-gate-approval.md` §4.

**Limitations of the rule → Step 14:** **1** the **biconditional gap** (`0021` licenses sufficiency only;
ALT-BROAD narrows the unlicensed assertion from 1,355 pairs to 703 and **does not justify it**) · **2**
**outcome-conditionality, size 652**, with `ordering_commutation_check` showing the orders agree on
**observed counts, not that the estimand is unchanged** · **3** the **calibration residual**, discharged
at `W = 108` only against a Step 13 grid reaching 213 · **4** the **population mismatch** — bounds on
position-5, shares post-liveness, **and on DERIV the point estimate lies outside its own bound** · **5**
**297 pairs still in the channel** (207 never-started whose null `0021` licenses, 90 started-and-left whom
the widened floor admits).

**Blocking Step 9, not Step 8 — RED TEAM'S RECOMMENDATION, NOT A RULING:** **6** the **bootstrap is
unspecified** in `B`, seed **and** statistic; `0052` §6's *"now specified"* is struck; **Step 9's CIs are
not diffable until all three are fixed.**

**Control defects carried (`0063` §3):** **7** `compare_halves()` cannot fail · four sub-interval ratios
outside every control, **arm a's checked by nothing** · the `_DERIVED` block **write-only**, so
`ADOPTED_IN`'s md/json result is *"satisfiable by the generator's own appendix"* · the covering qualifier
in **five wordings** with the `analytics-engineer` pair carrying **one clause** · `LEGITIMATE` disarming
nothing while two registers say it does · **the regenerator never running the phrase half** — *"the thing
that wrote B8 into four files still does not check for withdrawn phrases after writing"*, and the item
the Human Lead named as the one to fix first · DF-3.

**Reported, not reconciled — per `CLAUDE.md`:** **8** robustness survival **792 (A) / 791 (B)**, off by
one on each population, from a `τ_pull` restriction **A states and B does not**, which **neither arm
flagged and `0053` did not either** · **9** **the two sampling-width conventions**, arm a on the floor
endpoint's own bootstrap CI and arm b on the CI of the under-the-rule point estimate. **The spec fixes
neither.**

**Verification standing at drafting:** `check_surfaces.py` **PASS** across negative, phrase and positive
halves on seven surfaces · `step7_regenerate_derived.py` **PASS**, 84 target paths, 30 ratio rows, both
halves compared · `step7_floor_extremes.py` **11/11 CONFIRMED, 0 REFUTED** · both dual pairs
**byte-identical apart from `name:`** · **zero API calls in the entire chain.**

Related: [[glossary-terms-and-thresholds]], [[open-items-and-contradictions]],
[[decision-log-step18]], [[withdrawn-claims-register]], [[gate-step5-contamination]],
[[amendment-step1-continued-boundary]].
