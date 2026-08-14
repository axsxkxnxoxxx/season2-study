# Decision 0074 — six rulings on Step 8's divergences, and `processed/` becomes the eighth surface

| | |
| :--- | :--- |
| **Decision** | **Table grain: position 5, 196,654 rows, `live` and `outcome` as columns.** **The `p` invariant is specified**; **the set-membership rule is a coverage count**; **the 94-record denominator is reported unreconciled**; **D9 uses the strict key with the loose 75 alongside**; and **`processed/` is the EIGHTH propagation surface** — `adopted_rule.json` corrected, `CLAUDE.md` and both control scripts extended. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 dual run's four divergences and its open items |
| **Status** | Closed. **Neither Step 8 proposal is adopted; the gate is the Human Lead's.** |

---

## 1. Table grain — a ruling, not a correction

**Both readings gave identical counts.** Instance A emitted **195,951 × 86** at position 7; instance B
emitted **196,654 × 87** at position 5 with `live` and `outcome` as columns. **Every waterfall number,
every outcome count and every bound numerator agreed.** So nothing was wrong; a choice was unstated.

**Ruled: position 5, with the liveness result carried as a column.** **Rulings 1 and 7 established that
downstream CONSUMES rather than REBUILDS, and this is that principle applied to the row set.** Under the
position-7 reading, **anything needing the excluded pairs reconstructs them — and a reconstruction that
agrees today is still a second definition tomorrow**, invisible to the dual diff because both instances
would rebuild the same way.

## 2. The `p` invariant — specified, not dropped

`p ∈ (0, 1]` on every Started-and-left row, null elsewhere. **DATA CHECK.**

**Neither the spec nor `0069` listed it; both instances ran it unprompted.** **It is a data check on a
set where four of six are code checks** — it can fail on real data, which almost nothing else in that
set can — and **Step 10 publishes `p`.** Specifying it is the cheaper direction: dropping it would
remove the only assertion in Step 8 that could catch a data defect in the abandonment point.

## 3. The set-membership rule — a coverage count, not an invariant

**Resolving the 7-against-6 divergence.** A asserted it as a seventh invariant; B reported it as
coverage. **Step 8's own bullet already calls it *"an implementation check, not a data check."***

**Report records examined and records dropped; do not assert it.** `0069` established that **an
unlabelled code check reads as evidence FOR THE RULE when it is only evidence that the code ran**, and
asserting this one adds a seventh pass to a report where four of six already cannot fail.

## 4. The 94-record denominator — reported unreconciled

**6,065,704 (A) against 6,065,610 (B), and both reported 0 drops.** **Neither figure is wrong on its
face, both report the same result, and nothing downstream depends on the denominator** — it is a
coverage figure for a rule that dropped nothing. **Publish both numbers, not one.** Routed to Step 14,
per `CLAUDE.md`: *report it, do not reconcile it.*

## 5. D9 — the strict key, with the loose count alongside

**The normalisation rule decides the entire number and none was specified.** **Strict finds 0
complementary signature pairs; loose finds 75**, so **half (a) is 6 or 0 on an unstated choice.**

**Ruled: strict.** **Loose strips the year and merges genuinely different shows** — its largest clusters
are **The Twilight Zone, The Traitors and Manhunt**: remakes and national versions, **not split
metadata**, which is the artefact D9 exists to count.

**The loose count publishes alongside because it bounds how wrong strict could be** — and because **the
error runs OPPOSITE to D9's own lower-bound caveat.** A reader told the figure is a floor would be
wrong in the direction they were not warned about, which is worse than the uncertainty itself.

## 6. `processed/` is the eighth propagation surface

**Second time it has bitten.** `adopted_rule.json` carried **revision-3 figures — 4,849 removed,
215,258 retained** — against the **approved revision-6 rule: 16,665 + 1,542 = 18,207 removed, 201,900
retained of 220,107** (`0021`). **One Step 8 instance read the exclusion from `pair_revision5.csv` and
re-asserted the Step 5 waterfall line by line instead; the other worked around it.**

**It is the first file an implementation reaches for, and no control covered it.**

**Corrected**: the approved figures are added, **the revision-3 block is retained and labelled** rather
than deleted, and the file states why it mattered. **`CLAUDE.md` now lists eight surfaces**, and both
control scripts scan the new one — **254 files, up from 96.**

**And the scoping is where the care went, because a surface that fails on noise gets switched off:**

- **Data tables are excluded by suffix and the count is reported, never silently.** A numeric matcher
  over arbitrary data yields **coincidence, not propagation defects** — `duplicate_pairs.csv` alone
  returned 12 "hits" on per-row measurements that round near a superseded width. **The figures this
  surface exists for live in the metadata files.**
- **The per-arm working directories are allowlisted BY NAME with reasons** — `processed/step7/bb_a/`
  and its siblings are **the record of what one instance computed under the rule generation it ran**,
  superseded by definition, exactly like the stamped artifacts.
- **`adopted_rule.json` and its kind are NOT exemptible, in code** — `PROCESSED_NEVER_EXEMPT` is checked
  **before** the allowlist, so the file this ruling exists for cannot be waved through by a directory
  rule. **That is the same guard shape as `OPERATIVE` on surface 6.**

**All eight surfaces PASS.**

## 7. Scope

- **Rulings 1–5 propagated to `task-sheet.md` Step 8 and both `analytics-engineer` files identically**;
  pair verified byte-identical apart from `name:`. **Ruling 4 additionally routed to Step 14.**
- **Ruling 6 reached `CLAUDE.md`, `src/check_surfaces.py`, `src/step7_register.py`,
  `src/step7_regenerate_derived.py` and `processed/step5/adopted_rule.json`.**
- **Deliberately not reached:** the `data-scientist` pair — **none of the six changes what Step 9
  receives.** Ruling 1 changes the row set Step 9 reads, and **`0071` already tells Step 9 to consume
  Step 8's output rather than rebuild it**, which is the instruction that matters either way.
- **No Step 8 proposal is adopted. Zero API calls.**
