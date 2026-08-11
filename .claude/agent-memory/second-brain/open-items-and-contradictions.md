---
name: open-items-and-contradictions
description: Live register of open items and cross-step contradictions in the Season 2 study, each with its two conflicting sources named — re-verified against the files 2026-08-10 after decisions 0001-0003 and the Step 5 post-approval addendum
metadata:
  type: project
---

# Open items and contradictions — re-verified 2026-08-10

**Why this file exists:** Second Brain surfaces contradictions and names the two things that
conflict. It does not decide, arbitrate, or fix. Every entry names its two sources so the Human
Lead can rule without re-reading the corpus.

**How to apply:** re-check each entry against the files before raising it. Several close by
ordinary progress rather than by a decision — three did on 2026-08-10.

**The decision log of record is `decisions/`.** It now holds `README.md`, `0001`, `0002`,
`0003`. Where a decision file and this memory differ, `decisions/` governs on who decided what
and when; the deliverable it approves governs on substance. I never edit `decisions/` — I report.

---

## Closed on 2026-08-10 — recorded so they are not re-raised

| Was | Item | How it closed |
| :--- | :--- | :--- |
| C1 | Step 4 endpoint decided in Step 1 but listed as open-and-blocking in Step 0 | Human Lead ruled `GET /users/:id/history`, unfiltered, one sweep per user. **D15**, decision **0002**. `artifacts/step0-access-and-setup.md` §0 and §6.1 now carry a resolution box and a struck-through open item; Step 1 §0 agrees. Verified. |
| C2 | Two figures in an approved public artifact had no public source | `src/step0_history_probe.py`, `logs/step0_history_probe.json`, and `artifacts/step0-history-endpoint-probe.md` exist. Both figures reproduce from one cached response at **zero live calls**. Verified all three paths. |
| C5 | Step 6 estimation sample specified two ways on a dual-implementation gate | Human Lead ruled **C1 bucket only**, applied to all shows. **D14**, decision **0003**. `task-sheet.md` Step 6 now carries it by bucket name, so both isolated instances read it from the file they actually read. Verified at `task-sheet.md` Step 6 and Step 13. |

---

## OPEN — carried forward

### O1. `pull_date` has no value (was C3)

Adopted in **form** (D11), value **deliberately deferred** to Step 4's schedule. Human Lead act;
no agent performs it. Constraint: `pull_date ≤ earliest per-user fetch date in the whole Step 4
sweep`. **Any step that right-censors, or computes D3, D8 or D9, is blocked on this value.**
Carried in `decisions/README.md` open item 1. Still the one outstanding item from Step 1.

### O2. The gap hypothesis is untested and belongs to no step (was C4)

Whether Trakt represents a numbering gap by **omitting** the number or by **listing a
placeholder** is unknown. If it lists a placeholder, `number ∈ E` for a non-existent episode,
the drop rule readmits the exact case the set rule was built to exclude, and `L := |E|` counts
an episode that does not exist. **Section 3 must not be read as "gaps handled."** Step 1 §3.3
assigns it to "wherever `E` is first pulled at scale", which is not a step and has no owner.
`decisions/README.md` open item 3 now carries it — registered, still unowned.

### O3. Step 1 obligations that reach a step only through Step 1's handoff list (was C6, widened)

The Human Lead's established pattern is: **if two isolated instances must obey a rule, write it
into `task-sheet.md`**, the file they actually read. That pattern was applied at Step 7, Step 9
(pair-level liveness), Step 6 and Step 13 (D14). **It has not been applied to Step 8.**

- `task-sheet.md` Step 8 enumerates filters as "frame, contamination exclusions, S1 completion
  rule, W, and liveness rule". **Right-censoring is not named as a filter at all**, though Step 1
  §6 imposes an ordering constraint on it (contamination *before* censoring) and requires its
  removal reported as **two lines**. The **`L2 = 1` exclusion** is likewise absent. So are D2, D3,
  D8, D9, both drop counts, the five cadence-bucket lines, the boundary-proximity count, the
  metadata-disagreement counts, the `pull_date` reporting trio, and `action` retention.
- `artifacts/step1-outcome-definition.md` §9 (Step 8 handoff) is the only place all of that
  exists.

Step 8 is a **dual-implementation gate**. Whether the two instances receive §9 depends entirely
on what the Step 8 spec file contains when it is dispatched.

Same shape, lower stakes, at **Step 13** (not dual-implementation): `task-sheet.md` Step 13 was
amended on 2026-08-10 for D14's two obligations but still does not carry Step 1 §9's two
**required** robustness arms — **(i)** S1 completion date as last-observed rather than first-pass,
and **(ii)** the `action`-type arm excluding `checkin`-only and manual-`watch`-only evidence.
"Vary the S1 completion rule at 100 and 90 percent" is the *threshold*, not the *date definition*,
so it is not arm (i).

### O4. `L2 = 1` classifies into C2 "weekly" before it is excluded

At `L2 = 1`, `weekly_span = 0`, so `span ∈ {2, 3}` falls through C1 and lands in **C2 weekly**
under D12 first-match ordering. Harmless **only because** `L2 = 1` shows are excluded from the
headline population (§7) — but the exclusion happens at **Step 8** while the classification is
available from **Step 2** onward. Anyone who classifies before excluding sees nonsense weekly
buckets. The order matters and is written down nowhere.

### O5. Critical path, for sequencing awareness (was C7)

`Steps 3 and 4` are unblocked as of decision 0002 and are the long pole — `task-sheet.md` says
start them first. **`pull_date` (O1) is now the next structural blocker**, and it cannot be set
until Step 4's schedule exists. Then: Step 5 gate → Steps 6 and 7 gates → Step 8 gate.

---

## NEW — surfaced 2026-08-10

### N1. Section 8 still reads as though question 2 were open, and the residue is real

- `artifacts/step1-outcome-definition.md` **§8**: "Their treatment in the Step 6 lag distribution
  is a separate question and **stays open** (open question 2) … my **recommendation** in Section
  10.1 is the C1-only estimation sample."
- **§9, §10.1 and §11** of the same document: question 2 is **decided** as D14; "the negative-lag
  question that travelled with it is **closed** by the same decision."

§8 was not updated when D14 landed. That is the stale half. **The live half is that D14 does not
actually close the negatives everywhere:** it makes every lag in the *estimation sample*
non-negative by construction, but `task-sheet.md` Step 6 also requires the **all-shows** lag
distribution to be plotted alongside, and for a weekly show the negative mass is most of the
started population. Nothing states how negatives are treated in that plot.

Why this is not cosmetic: **Step 6 is a dual-implementation gate**, and `task-sheet.md` Step 13
defines the required robustness range as "the range implied by the gap between the C1-only and
all-shows lag distributions". If the two isolated instances handle the negative mass differently,
they diverge on the all-shows plot and the divergence **propagates into Step 13's tested range** —
the same class of failure D12 and D13 were written to prevent.

### N2. D2 is computed on definition (b), so it cannot count the failure the addendum points at

- `artifacts/step1-outcome-definition.md` **§5 addendum** (added post-approval): the probe profile
  is "the first observed instance of the failure D2 exists to measure", and "It establishes the
  failure mode is real and reachable, **not how common it is — that is what D2's count is for.**"
- **D2 as defined** (§5 required output, §10.0 D2 row, §9 Step 8 handoff): it counts pairs whose
  first S2 watch precedes **their clock start**, and clock start is built on **definition (b)**,
  first-pass completion, which a rewatch cannot move.

Under (b) this profile's lag is **+360.73 days**. It will **not** appear in the primary D2 count —
by construction, no (a)-style rewatch artifact can. D2 under (b) measures genuine parallel viewing,
which is a different quantity and a useful one, but it is not a frequency estimate for the
(a)-failure. That frequency would be D2 recomputed inside the **Step 13 arm (i)** last-observed
run, and **no step requires D2 in that arm** — arm (i) is not even in `task-sheet.md` Step 13 (O3).

Consequence to state when it is raised: whoever computes D2 should **expect zero** instances of
this profile's failure mode in the primary run, and should not read that zero as evidence the
failure is rare.

### N3. Two records of the provenance gap are now stale

- `decisions/README.md` open item 4 and `decisions/0001` "What this decision does NOT close",
  bullet 4: the two figures "trace only to an undocumented run in a machine-local log, with **no
  run record and no probe script in `src/`** … not reproducible from the repo. **Open.**"
- `src/step0_history_probe.py`, `logs/step0_history_probe.json` and
  `artifacts/step0-history-endpoint-probe.md` all exist and reproduce both figures at zero live
  calls.

The item is closed in fact and open on the record. The Human Lead owns both files.

### N4. An unobserved premise sits inside an approved rule

- `artifacts/step1-outcome-definition.md` §2.1: `episode.ids.trakt` "should agree with
  `(show, season, number)`; where it disagrees — **which happens after Trakt metadata merges and
  splits** — `(show, season, number)` wins … Disagreements are counted and logged."
- `artifacts/step0-history-endpoint-probe.md` §2: 96 distinct episode Trakt IDs against 96
  distinct pairs, **zero disagreements**, no pair mapping to more than one ID. "Not contradicted;
  simply **untested** by this profile."

Not load-bearing for the rule — `(show, season, number)` wins either way — but the *mechanism*
asserted (merges and splits reassign episode IDs) is the **same mechanism D9's split signature
depends on**. If the mechanism is rarer or shaped differently than assumed, the D9 lower bound is
weaker than its wording implies. One profile is not evidence either way; it is the absence of
evidence, and it is now on the public record as such.

### N5. `decisions/0001` undercounts the withdrawn-claims table

- `decisions/0001` "Standing record": "a table of **six claims withdrawn as false** across the
  three revisions, plus this accepted risk."
- The table at the head of `artifacts/step1-outcome-definition.md`: **twelve rows — eleven
  withdrawn or corrected claims plus the one accepted risk.** Six of the eleven are false-by-
  construction; the other five are framing corrections, and at least three of those are described
  in the body as withdrawn *because they were false*.

A description error in the log of record, not a decision error. Worth folding into any edit the
Human Lead is already making to `0001`, since the table "is not to be pruned" and the count is
how anyone checks that.

### N6. Minor — the Step 0 file index is stale

`artifacts/step0-access-and-setup.md` "Files" table lists `step0_test_pull.py` and
`step0_watched_endpoint_probe.py` but not `src/step1_episode_listing_probe.py`,
`src/step0_history_probe.py`, or their run records. Each has its own write-up, so nothing is
lost; the index is just no longer complete.

---

## Checks that PASS — recorded so they are not re-litigated

Verified 2026-08-10 against the current files:

- **Both probe figures reproduce.** 123 records, 96 distinct pairs, 25 episodes duplicated, 27
  surplus records, 64 pages at `limit=250` — all exact. "28 percent" is 28.125 %; "six weeks" is
  5.90 weeks (41.31 days). Rounding only, both in the direction that makes the printed number
  rounder rather than larger.
- **27 surplus records and 25 duplicated episodes are both correct and are different questions.**
  Two episodes appear three times. Do not "correct" one to the other.
- **The 96 is derived from history, not from `show.aired_episodes`** — which also reads 96 on that
  payload. Coincidence of a completionist profile. §2.1's rule stands independently, and §0
  forbids `aired_episodes` outright.
- **The §5 addendum changes no rule.** Verified line by line: §4, §5's definition (b), §6, §7,
  §2.2, D2's requirement text and the §9 handoff lists are unchanged. The addendum adds evidence
  and a scope limit. The gate remains approved and the approval record says so.
- **`task-sheet.md` Step 6 carries D14 by bucket name**, not as "binge shows", and Step 13 carries
  both the range obligation and the per-arm retained-row count.
- **Privacy boundary intact.** No username, user ID, or watch history in `artifacts/` or
  `decisions/`. The new probe write-up names neither profile nor show and keeps episode-level
  material in `logs/` and `raw/`. The username is a script argument, not hard-coded.
- **Zero live API calls were spent on the reproduction.** `requests_sent: 0`,
  `served_from_cache: 2`.
- Previously verified and still true: censoring clearance costs no show; the `+H` cost estimate;
  the 91-day arm sits inside the primary censored population; D12 is exhaustive and mutually
  exclusive under first-match; the boundary convention is used consistently and no second reading
  survives; both one-day directions are declared and neither is netted off.

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]],
[[decision-log-step18]], [[withdrawn-claims-register]], [[step1-open-questions]].
