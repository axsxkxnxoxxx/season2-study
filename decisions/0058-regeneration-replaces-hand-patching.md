# Decision 0058 — derived figures are regenerated, not patched; the two ratio conventions are reported, not reconciled

| | |
| :--- | :--- |
| **Decision** | **Hand-patching stops.** `src/step7_regenerate_derived.py` reads the stored counts and writes **every** derived figure into **both halves of both arms** from a single expression each, then verifies numerically that no superseded value survives. **`src/check_surfaces.py` replaces textual grep** — it matches at both precisions across all seven surfaces, which is the only form that can see the `.json` halves. **Finding 3 reverted: the two arms' ratio conventions are reported as two numbers.** Stamps are **negative only**. Dates corrected. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **eleventh** Step 7 HOLD |
| **Amends** | `0057` §1 (a false count), §2 (the ratio reconciliation); `0052`–`0057` dates, in place |
| **Verified by** | `src/check_surfaces.py` — **PASS, both halves, all seven surfaces, 96 files** |
| **Status** | Closed. **Step 7 goes to Red Team. The gate is OPEN.** |

---

## 1. The method was the defect, and Red Team named it

**Four consecutive decisions corrected these artifacts by hand-patching individual values into
published files.** Every finding in reviews 9, 10 and 11 was a value a patch reached in one file and
missed in another, or reached in the `.md` and missed in the `.json`, or reached a ratio and missed its
numerator. **Eleven entries of one error class is a method that cannot converge, and `0057` was the
twelfth.**

**`0057` §1 claimed "fifteen values corrected in each file, listed and verified individually." That is
false.** The patch matched on a whitelist of key names, so three regions with different key names were
walked straight past: the **attainable-corner table** in both populations, the whole
**`sampling_error.*.bound_endpoints`** block except one line, and the **per-`W` series**. The one line
that did move was the ratio — **the patch reached the ratio and missed both its operands.**

## 2. What the regeneration script fixes by construction

`src/step7_regenerate_derived.py`. **Counts are the only inputs**; everything else is one expression.

| Red Team finding | Closed how |
| :--- | :--- |
| 1 corner table | a declared target **path**, not a guessed key |
| 2 `sampling_error` block | declared target paths; **paths absent in an arm's schema are LISTED, never silently skipped** — 6 in arm a, 28 in arm b, printed every run |
| 4 per-`W` series | **cannot** be regenerated: only `W = 108` masks are on disk. So it is **declared scope-limited by renaming its key** — `per_arm_SUPERSEDED_computed_under_closed_window_and_unwidened_floor` — which survives a reader who never opens the note |
| 5 legitimate strings in the superseded list | ~~a value still live anywhere cannot enter the list, because the list is generated from the same expressions that produce the live values~~ **WITHDRAWN (`0059`): the mechanism NEVER FIRED.** `LIVE_ELSEWHERE` was compared against a `SUPERSEDED_VALUES` dict that **never contained `0.3575` or `0.0672`**, so the filter was a no-op and `_dropped` was always empty. **They are out because they were never put in — the property was asserted, not structural.** They are now in the shared register's `LEGITIMATE` table with their reading stated, which is a declaration and not a mechanism |
| 6 4-dp register vs 6-dp literals | matching is **numeric at a tolerance**, never textual |
| 7 corrected values in stamps | **the `.md` stamp is negative only.** It names superseded strings and points at the generated block; it restates **no** adopted figure. Verified: `9.6372`, `0.0961`, `0.4032`, `73.3924`, `11.3015`, `82.4930` all occur **zero** times in either stamp |

**One claim in this table is withdrawn and the withdrawal belongs here, not in a footnote.** Row 5 described a structural property that **never operated**. It is the same shape as the entries this chain has been correcting: a control asserted to exist rather than verified to fire. **Red Team found it by reading the code rather than the claim** (`0059`).

**And the trap the fix had to avoid, which the script encodes rather than remembers.** `19042` is *also*
the post-liveness started-and-left **point estimate**, in `outcome_shares`, `waterfall` and
`ordering_commutation_check`. **Targets are declared by path, so a value-wide substitution cannot
happen.** The generated block says so, so the next reader does not "fix" them.

## 3. Finding 3 — reverted. Two conventions, two numbers

**`0057` wrote arm b's denominator into arm a's file.** `0.509 = 0.403245 / 0.7922`, and **`0.7922` is
arm b's.** Arm a's own is `0.7602`, which gives `0.5304`.

**The arms use different conventions**: **a** divides by the **floor endpoint's own bootstrap CI
width**; **b** divides by the CI width of the **under-the-rule point estimate**. **The spec fixes
neither, so it is a spec ambiguity — report it, do not reconcile it.**

**Red Team's proof that the reconciliation was wrong is internal to the same files:** the
**never-started** ratio was correctly left divergent at **0.2813 (a)** against **0.27211 (b)**. Same
figure class, two treatments, one entry.

**Reverted.** `RATIO_DENOMINATORS` names both, per arm, so **no expression in the script can produce one
arm's ratio from the other arm's denominator without the substitution being visible** — and an assert
fails if the two are ever made equal. Recomputed under each arm's own convention:

| | arm a, denominator 0.7602 | arm b, denominator 0.7922 |
| :--- | ---: | ---: |
| **APPLY** bound ÷ sampling width | **0.5304** | **0.5090** |
| **DERIV** bound ÷ sampling width | **0.1309** | **0.1310** |

**Stated with it, because it is a real limit:** arm a's denominator is the CI of the **pre-widening**
floor point and was **not re-bootstrapped**. The recomputation reuses it.

## 4. What the checker found that the grep could not

`src/check_surfaces.py` parses every number-shaped token on all seven surfaces — **96 files** — and
compares numerically. On its first run it returned **22 unlabelled superseded values**, none of which
textual grep had been able to see:

- **`step7-liveness-mm-{a,b}.md`** — the **reverted rule's** deliverables — carried **no supersession
  stamp at all.** Eight hits. Now stamped in whole, and retained rather than deleted, because they are
  the record `0054` used to establish the two rules give identical bounds, and because their DERIV
  figures were computed there first.
- **Sixteen `step7-*.json`** from earlier rule generations had **no `_SUPERSEDED` key** — a JSON has no
  prose to carry an inline marker, which is why every one of review 11's six JSON findings was there.
- **`open-items-and-contradictions.md`'s V7 postmortem** stated `73.6537%` as the Continued ceiling
  without noting it has since moved to `73.6995%`. The postmortem's point is the mislabelling; the value
  moved underneath it.

**It also refused two false positives correctly**, which is the half a blunter check gets wrong: the
**extreme-NONE column** of the two-extremes table *is* `9.6830 / 11.3619 / 73.6537 / 82.4327` — both
arms were asked for it — and `0.3575` / `0.0672` as **shares of population** are correct. **Context
decides, not the value.**

**Both halves now PASS.** Negative: zero unlabelled hits. Positive: every adopted value present on
every surface that owns it — and **`9.6372`'s ownership excludes the two `analytics-engineer` files**,
because they deliberately hold no Step 9 figures (`0055` §5a).

## 5. Finding 8 — the scope sentence

**The per-`W` series was computed under the CLOSED window and the un-widened floor, at every arm.** The
inertness of the window form is asserted at **`W = 108` only** — open 90 / 89 against closed 90 / 89 —
and **is not expected to hold at `W = 213`**, where D10 forces `τ1 ≤ τ_pull − 91 d` so `τ2` sits at or
adjacent to `τ_pull`, and a mass point in last-insertion instants sits there. **Step 13 is the consumer
and must recompute it.** In the generated block, in the JSON key name, and in `CLAUDE.md`'s list.

## 6. Dates — corrected in place, not silently

**`0052` through `0057` were all dated 2026-08-14. Today is 2026-08-13.** The drift began when the
session clock advanced mid-work and the date was carried from an earlier entry rather than re-read.

**Corrected on every surface — 49 files — and each of the six entries carries a note saying so**, rather
than being silently rewritten. **The decision log is a public tracked artifact**, and a date that
quietly changes is worth less than one that visibly did.

## 7. Step 14 — the commutation caveat

**`ordering_commutation_check` shows the two filter orders agree on OBSERVED COUNTS. It does not show
the estimand is unaffected.** Conjunct 2 is `NOT Continued`, so liveness is **outcome-conditional** —
the artifact flags this itself and `0046` made waterfall line 6 outcome-conditional in the spec. What
both arms verified is that `|A|` and liveness are row-local predicates that commute index-for-index on
this data. **That the conditioning leaves the estimand unchanged is a different claim and is tested
nowhere in this study.** The bound construction is designed to absorb it. **Routed to Step 14 as a
limitation, not as a resolved question** — Red Team would not hold on it and neither would I.

## 8. Scope

- **No rule change.** ALT-BROAD, silence at `τ1`, window `(τ1, τ2)` open.
- **No rerun and no new measurement.** Every value is a function of counts already on disk.
- **Zero API calls.**
- **Step 8 does not launch.**
