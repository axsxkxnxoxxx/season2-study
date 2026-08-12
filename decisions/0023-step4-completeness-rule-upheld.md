# Decision 0023 — The sweep-completeness rule stands as adopted; three findings against it become Step 14 limitations

| | |
| :--- | :--- |
| **Decision** | **`decisions/0012` is upheld.** The 2% residual tolerance is not changed and Red Team's final-page shape test is **not adopted**. Three findings against the rule are recorded as **Step 14 limitations**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Review** | Red Team, one round, **HOLD**. Overruled on cascade cost, not on merit. |
| **Closes** | `decisions/README.md` **item 15** — 0012 changed a rule inside an approved gate and had never been reviewed. It has now been reviewed. |
| **Evidence commissioned during the review** | `artifacts/step5-discard-outcome-neutrality.md` |
| **Status** | Closed |

---

## The ruling

> Keep the rule as adopted. Do not change the tolerance, do not adopt the shape test.
>
> The correction is 0.13 points on the pooled rate. Changing the tolerance restates the cohort,
> which re-runs the completer diagnostic, which moves the Step 2 frame's ≥50 candidate rule and the
> 1,138-show frame with it. **The cascade cost exceeds the size of the correction.**

The cascade is real and worth naming in full, because it is the whole of the reason: tolerance →
cohort size → completer counts per show → which shows clear ≥50 completers → the candidate set →
the frame → the structural thresholds applied to it → the 220,107 pairs → the approved Step 5 rule
computed on them. A 0.13-point correction at the far end does not justify re-deriving that chain.

**Red Team was not overruled on the substance.** Its finding stands as recorded below; what was
weighed against it is cost, and that weighing is stated rather than implied.

---

## Three findings recorded as Step 14 limitations

### 1. The rule validates itself against itself

Leg 1 requires full **`page_count`** coverage. **`page_count` is `ceil(item_count / 250)` — verified
in all 2,839 ledger rows, zero mismatches** — so it is derived from `item_count`, the header whose
unreliability is 0012's entire argument for existing.

The consequence is structural. A short final page proves the sweep reached the end of the history:
the server ran out of records before it ran out of page. **A full final page proves nothing** — the
sweep stopped at the last page the bad header allowed for, while records may still have been
flowing. Leg 1 cannot tell those apart, and Step 1 §0 says a truncated sweep "is indistinguishable
from a genuine 'never started' and lands directly in the study's headline category."

### 2. The discard is not outcome-neutral

Measured directly, at zero API cost, on the discarded users' still-cached raw pages
(`artifacts/step5-discard-outcome-neutrality.md`):

| | Discarded (287) | Retained (2,549) |
| :--- | ---: | ---: |
| Completer pairs | 25,035 | 220,107 |
| **Has-any-S2 rate** | **89.78%** | **88.52%** |
| 95% CI | [89.40, 90.15] | [88.38, 88.65] |

**Difference +1.27 points, 95% CI [0.87, 1.66], z = 5.98, p < 0.001.** The intervals do not overlap.

**Direction: discarded users are more likely to have S2 evidence**, so removing them pushes the
never-started share **up**. It **compounds with the Step 3 seeding bias and the liveness bias rather
than offsetting them** — those push the share down, and nothing shows the three cancel.

**Pooled effect: 0.13 points.** The 287 carry 10.2% of the combined pair pool, so restoring them
would move the pooled descriptive from 88.52% to 88.65%. This is the number the ruling is weighed
against.

### 3. A better instrument exists and was not used

Red Team's **final-page shape test** — every interior page full at `limit`, final page strictly
between 0 and `limit`, computed from `page_item_counts`, which `classify_sweep` already builds —
would discriminate genuine sweep completion from a full final page **exactly**, rather than by
calibration. It is strictly stronger than the 2% tolerance on the failure mode Step 1 §0 cares
about and strictly weaker on the artifact 0012 proved benign.

Cost: **zero API calls** over what is on disk; users failing the test resolve at **one call each**,
bounded near **2,800 calls, about 19 minutes** at the 150/min throttle. **No re-pull is required.**

**It was declined on cascade cost, not on merit.** That distinction is the point of recording it: a
future reader should not infer the instrument was examined and found wanting.

---

## Also recorded: how the 2% was set

**The pilot does not support the figure 0012 quotes.** 0012 states a replay "with a maximum residual
of **0.86 percent** against the 2 percent tolerance." `artifacts/step4-pilot-counts.json`, generated
on 20 users, records `max_abs_share_of_item_count: 0.11707` — **11.7%** — and a signed residual range
of −191 to **+131**. A reader of 0012 alone concludes the tolerance carries 2.3× headroom over the
worst observed case. It never did.

**Any value across a wide band gave the identical pilot partition.** The pilot's own percentiles show
p95 at **1.4%** and p99 = max at **11.7%**, with nothing in between — so every tolerance from roughly
1.5% to 11.7% would have split those 20 users the same way. **The most aggressive end of that band
was chosen**, without a sensitivity table and without the choice being stated as a choice.

**The full run shows no such gap.** On the final ledger's 287 discards the absolute residual share
runs min 2.01%, median 3.92%, max 99.9%, distributed **168 in the 2–5% band (58.5%)**, 59 in 5–10%,
60 above 10%. The threshold cuts through the middle of a continuous distribution: a 5% tolerance
would have retained 168 of the 287.

**24 of 235 under-count discards — corrected to 31 of 287.** The figures in the ruling as given were
read from a mid-run snapshot of 2,372 users. On the **final** ledger the count is **31 of 287
discards** whose residual is positive — accumulated records **exceeding** the header, which 0012's
own table calls *"benign, and in the safe direction: more data than advertised, not less."* The
implemented test is `abs(residual) <= tolerance * item_count`, two-sided, so it discards the
direction the decision declares safe. The remaining 256 are over-count.

**One structural asymmetry nobody chose.** Accumulated records can never exceed `limit × page_count`,
so a positive residual is capped at `limit − 1 = 249`. Above roughly 50 pages the under-count arm of
the test **cannot fire at all**. The rule presents as a symmetric two-sided threshold; it is a
one-sided test on large users and a size-correlated discard on small ones.

---

## Two corrections to 0012's own text, not to its rule

Neither changes the adopted rule; both are wrong as written and would mislead a Step 18 reader.

1. **The cross-page duplicate claim is misattributed.** 0012's third required output cites "**5
   duplicates in 14,236 records**" as *genuine cross-page duplicates*. The instrumentation records
   `cross_page_duplicate_records: affected_users 0, affected_records 0` across 2,137 users and
   22,725,090 records, and `within_page_duplicate_records: affected_records 147`. **Cross-page
   duplicates have never been observed in either run.** The anomaly that does occur — the same
   record `id` twice on one page, meaning a 250-slot page carried 249 distinct records — is not a
   required output, is described nowhere, and has no stated interpretation.
2. **0012 was marked `Status: Closed` while its own header said the Human Lead may wish to put it to
   Red Team.** A decision cannot be closed and pending review at once. It is closed **now**, by this
   entry, having been reviewed.

---

## What was fixed rather than recorded

**The ledger's false zero.** Discarded rows carried `records: 0` while using `null` for every other
withheld field. A consumer reading `records` without also reading `outcome` would have seen a real
zero, and per `CLAUDE.md` a skipped user read as empty becomes a false "never started". **`records`
is now `null` on all 287 discarded rows**, verified that no other field on any row changed.
`items_discarded` still carries what was fetched and thrown away.

---

## Scope

- **No number in the study moves.** Cohort 2,549, frame 1,138 shows, 220,107 pairs, Step 5's 201,900
  retained and 128,099 estimation sample all stand.
- **Nothing downstream was re-run**, and the tolerance was not touched.
- **The Step 1 gate is not reopened.** Red Team argued 0012 reaches the reopening clause by
  converting a categorical completeness requirement into a graded one. The Human Lead has ruled the
  rule stands; the reopening question is answered by that ruling, and the three findings travel to
  Step 14 rather than back to Step 1.
- **If the Step 4 pull ever resumes**, the cascade argument weakens — the cohort restates anyway —
  and the shape test should be reconsidered at that point rather than inherited as settled.
