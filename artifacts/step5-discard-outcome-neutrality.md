# Are the 287 discarded users outcome-neutral?

**What this is:** a read-only check requested by the Human Lead after Red Team's review of
`decisions/0012`. It asks the one question the existing bias evidence does not reach: **does the
sweep-completeness tolerance select on the outcome the study measures?**

**It is not a proposal.** No rule is changed, no tolerance is moved, nothing downstream is re-run.

**API calls: zero.** Under 0012 the 287 discarded users' pages were discarded rather than written to
`processed/step4/parsed/`, but the raw bodies were still cached under `raw/users/<slug>/history/` —
14,578 page files across all 287 users, every one present.

**Aggregates and counts only.** No usernames, user IDs or individual histories. Per-user and
per-pair detail is at `processed/step5/discard_neutrality/` (git-ignored).

**Reproducible at zero API cost:** `src/step5_discard_neutrality.py`.

---

## Headline

> **The discard is not outcome-neutral. It is detectably biased and the bias is small.**
>
> Discarded users' completers have a **higher** has-any-S2 rate than retained users' — **89.78% vs
> 88.52%**, a difference of **+1.27 points**, 95% CI **[0.87, 1.66]**, z = 5.98, p < 0.001.
>
> Restoring all 287 users would move this descriptive by **+0.13 points**, because they carry 10.2%
> of the combined pair pool.

Statistically clear, practically small. Both halves of that sentence are load-bearing and neither
should be quoted without the other.

---

## 1. Method, and why a difference here cannot be a difference in method

Both populations pass through **one metric function**. The Step 1 §4 completion rule is applied
against the **real `E1`, `L1` and `F1`** from the 1,138-show Step 2 frame, with membership by set per
§3.2, restricted to in-frame shows. A pair is a completer when `max(D1 ∩ E1) = F1` and
`|D1 ∩ E1| ≥ ceil(0.90 × L1)`.

The two populations differ only in **where their records are read from**, which is unavoidable: the
discarded users have no parsed store, by rule.

| Population | Source |
| :--- | :--- |
| 287 discarded | `raw/users/<slug>/history/*.json`, deduplicated by record `id` within user |
| 2,549 retained | `processed/s1s2_scan.npz`, the committed S1/S2 extract of the parsed store |

**The two extractors were cross-validated on shared users.** Running the raw extractor over retained
users — who have both a raw cache and a parsed file — and diffing the triple sets gives **exact
agreement on every user checked**: zero raw-only records, zero parsed-only records, on sets of up to
9,273 triples. The parsed store is a faithful transformation of the raw pages, so the source
difference introduces no measurement difference.

**Second validation, and the stronger one: the retained population reproduces 220,107 completer
pairs exactly** — the figure carried by Step 2 and by the approved Step 5 rule, computed here by an
independent path.

---

## 2. Item 1 — S1 completers per user

| | Discarded (287) | Retained (2,549) |
| :--- | ---: | ---: |
| Users | 287 | 2,549 |
| Users with ≥1 completer | 282 | 2,487 |
| Users with **zero** completers | **5** | 62 |
| **Mean completers per user** | **87.23** | **87.34** |
| p10 | 9.6 | 8.0 |
| p25 | 31.0 | 31.0 |
| **Median** | **64.0** | **71.0** |
| p75 | 125.5 | 126.0 |
| p90 | 191.0 | 189.0 |
| Max | 406 | 443 |
| **Total completer pairs** | **25,035** | **220,107** |

The distributions are close to indistinguishable in the mean (87.23 vs 87.34), the quartiles and the
tails. The medians differ by 7 pairs, with the discarded slightly lower.

**A denominator note, stated because it is the kind of thing that quietly biases a comparison.** The
retained per-user statistics above are computed over **2,520 users**, not 2,549: 29 retained users
carry no S1 or S2 record on any in-frame show at all and are absent from the scan. Adding them as
zeros would lower the retained median and mean slightly and would move the comparison **in the
direction of greater similarity**, not less. The discarded side includes all 287, its 5 zero-completer
users among them. The pair-level rates in §3 are unaffected — they have pairs, not users, as their
denominator.

---

## 3. Item 2 and 3 — the share of completers with any S2 evidence

This is the axis that matters. It is the closest pre-outcome descriptive to the study's headline, and
it is what a tolerance selecting on the outcome would move.

| | Discarded (287) | Retained (2,549) |
| :--- | ---: | ---: |
| Completer pairs | 25,035 | 220,107 |
| Of those, with any S2 evidence | 22,477 | 194,830 |
| **Has-any-S2 rate** | **89.78%** | **88.52%** |
| 95% CI (Wilson) | **[89.40, 90.15]** | **[88.38, 88.65]** |

**The intervals do not overlap.**

---

## 4. Item 4 — do the populations differ?

**Yes.**

| | |
| :--- | ---: |
| Difference in has-any-S2 rate | **+1.27 points** |
| 95% CI on the difference | **[0.87, 1.66]** |
| z | 5.98 |
| Two-sided p | **< 0.001** |

**The discard is therefore not outcome-neutral.** The condition the Human Lead set — *"if the
discarded users' has-any-S2 rate matches the retained population, the discard is outcome-neutral"* —
is not met.

### Direction, and what it does to the headline

Discarded users are **more** likely to have S2 evidence. Removing them removes S2-watchers
preferentially, which leaves the retained population **slightly poorer in S2 starters** and therefore
pushes the never-started share **up**.

**Magnitude.** The 287 carry **10.2%** of the combined pair pool. Restoring them would move the
pooled has-any-S2 descriptive from **88.52% to 88.65%, a change of +0.13 points.** The rate
difference is 1.27 points; the effect on the pooled figure is a tenth of that, because the discarded
are a tenth of the pool.

### Reading this correctly

- **"Has any S2 evidence" is not an outcome state.** No window, no liveness filter, no `W`, no
  contamination exclusion is applied here. It is a presence count and a **ceiling** on "Started" — the
  same descriptive already reported in `artifacts/s1-completer-diagnostic.md` §5.
- **The significance is a function of sample size as much as effect size.** At n = 25,035 against
  n = 220,107, a 1.27-point gap is easily detected. The same gap in a study of 500 pairs would not be.
- **A small directional bias is not the same as a safe one.** It compounds rather than cancels with
  the biases already on record: the Step 3 seeding bias and the liveness bias both push the
  never-started share **down**, and this pushes it **up**. They are not required to offset, and
  nothing here shows that they do.

---

## 5. What this does and does not settle

**Settles:** the tolerance's discard is correlated with the outcome descriptive, at a magnitude
bounded near a tenth of a point on the pooled figure. That is now a measured number rather than an
untested assumption, and it is the axis the history-volume stratification in
`artifacts/s1-completer-diagnostic.md` §1 could not reach.

**Does not settle:**

1. **Why.** No mechanism is established. The discarded users are heavier trackers on average and the
   residual is a header artifact of unknown cause; whether the correlation runs through volume,
   through account age, or through something else is untested.
2. **Whether the rule should change.** That is Red Team's open finding on `decisions/0012` and a
   Human Lead decision. This check was explicitly scoped not to touch the tolerance.
3. **Whether the same bias holds at the outcome level.** The three-state outcome needs `W`, which
   Step 6 has not set. This measures the ceiling, not the state.
4. **The other 0012 findings.** Red Team's central objection — that leg 1 gates on `page_count`,
   which is `ceil(item_count / 250)` in all 2,839 ledger rows and therefore derived from the very
   header 0012 proves unreliable — is untouched by this check and remains open.

---

## 6. A ledger correction made alongside this check

Discarded ledger rows carried `"records": 0` while using `null` for every other withheld field
(`parse`, `parsed_path`, `is_data: false`). A consumer reading `records` without also reading
`outcome` would see a real zero, and under `CLAUDE.md` a skipped user read as empty becomes a false
"never started" in the headline.

**`records` is now `null` on all 287 discarded rows**, matching every other withheld field. No
count changes; `items_discarded` still carries what was fetched and thrown away. Applied by
`src/step5_fix_ledger_records_null.py`, which rewrites in place and verifies the row count and every
other field is untouched.

---

## 7. Files

| File | Contents |
| :--- | :--- |
| `artifacts/step5-discard-outcome-neutrality.md` | this file |
| `processed/step5/discard_neutrality/summary.json` | every figure above, machine-readable |
| `processed/step5/discard_neutrality/discarded_per_user.csv` | completer count per discarded user |
| `processed/step5/discard_neutrality/discarded_pairs.csv` | one row per discarded completer pair, with its has-S2 flag |
| `src/step5_discard_neutrality.py` | the check, re-runnable at zero API cost |
| `src/step5_fix_ledger_records_null.py` | the ledger correction in §6 |
