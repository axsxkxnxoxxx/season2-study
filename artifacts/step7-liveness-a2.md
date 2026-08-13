# Step 7 (rerun) — liveness threshold on the corrected reference distribution

**Instance A2. GATE. This is a proposal. Nothing here is adopted.**

| | |
| :--- | :--- |
| **Spec** | `task-sheet.md` Step 7 (lines 226–262); `decisions/0037`; `decisions/0036` §2 (§1's basis withdrawn); `0029`, `0025`, `0021`, `0026`, `0034` |
| **Inputs** | `processed/step5/full_scan.npz` (27,656,813 records, 2,549 accounts), `processed/step5/calibration.npz` (**read, not refitted**), `processed/step5/pair_revision5.csv` |
| **API calls** | **0** |
| **Step 5 waterfall** | 201,900 → 178,165 → 155,131 → 152,126 → 128,099 — **reproduced exactly**, asserted in code |
| **Chart** | `artifacts/step7-gap-distribution-a2.png` |
| **Machine-readable** | `artifacts/step7-liveness-a2.json` |
| **Row-level intermediates** | `processed/step7/a2/` (never leaves this machine) |

---

## 1. The proposal, in one block

> **Threshold: 504 days**, the 99th percentile of the **bracketing-gap** distribution measured on the
> 128,099 clean estimation sample (raw 503.0756 d, ceiling per `0025`).
>
> **Rule.** A **user-show pair** is **live** if, on the account's whole sweep — all shows, all movies,
> all record kinds — there exists a distinct insertion instant **at or before** that pair's
> `τ1 = ⟦T0⟧ + 108 × 24h` **and** a distinct insertion instant **after** `τ1`, **and** the gap between
> those two instants is **strictly less than the threshold**. Otherwise the pair is **not live**.
> Insertion instants come from the stored Step 5 play-`id` calibration, never from claimed
> `watched_at`. Evidence is account-wide; the test is pair-specific; **a user is never dropped
> wholesale.**

**The population the threshold is measured on is the single largest judgement call in this run and the
spec does not settle it** (§5.1). The threshold ranges from **504 to 914 days** across the five
waterfall levels. Every level is reported below so the Human Lead can pick rather than inherit mine.

---

## 2. The gap unit, executed exactly as `0037` §4 states it

Insertion instant = `np.interp(rid, knot_rid, knot_time)` on the stored curve. Per account: every
record's instant, sorted ascending, **runs of exactly equal instants collapsed to one** (exact float
equality — no rounding, no bucketing at any resolution), then consecutive differences.

| | |
| ---: | :--- |
| 27,656,813 | records in the sweep |
| 2,549 | accounts |
| 25,864,798 | distinct insertion instants |
| **1,792,015 (6.48%)** | records collapsed as exact ties |
| 25,862,249 | pooled gaps |
| **7,812** | median gaps per account |

This reproduces the reading `0037` §4 recorded as instance A's — **pooled 99th = 3.4432 d → 4 days.**
That figure is retained here only as the contrast; it is **not** the reference distribution.

**`0037` §2's strengthening is confirmed on this run:** the median account has 7,812 gaps, so a
whole-sweep test at the 99th percentile trips with probability ≈ 1 for a typical account. The rule's
shape (`0036` §2) is doing necessary work.

---

## 3. The corrected reference distribution

The bracketing gap is the gap between the last distinct insertion instant at or before `τ1` and the
first after it. Its distribution, by population:

| Population | pairs | measured gaps | median | p75 | p95 | **p99 raw** | **p99 ⌈⌉** |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Analysis population | 201,900 | 157,995 | 2.0101 d | 9.035 d | 240.49 d | 913.3559 | **914** |
| has S2 evidence | 178,165 | 138,077 | 1.9675 d | 8.468 d | 229.91 d | 902.0110 | **903** |
| `T0` not contaminated | 155,131 | 132,628 | 1.8935 d | 7.018 d | 138.93 d | 638.9547 | **639** |
| completing rec. not post-dated | 152,126 | 129,630 | 1.8816 d | 6.895 d | 124.91 d | 631.8031 | **632** |
| **`W` estimation sample** | **128,099** | **122,941** | 1.8247 d | 6.280 d | 101.31 d | 503.0756 | **504** |

The pooled/bracketing contrast at the analysis population — median **0.0000006 d** vs **2.0101 d**,
p75 **9.03 d** — reproduces `0037` §1's table to the digit.

---

## 4. What the correction does to the realised failure rate

`0037` recorded **37.4%** of measured bracketing gaps exceeding the pooled-99th threshold. **This run
reproduces it at 0.373936** on the 201,900 analysis population (0.330012 on the clean sample).

| Basis | threshold | measured-gap failure rate (201,900) | live share of 201,900 |
| :--- | ---: | ---: | ---: |
| **Withdrawn** — pooled 99th | 4 d | **37.3936%** | 48.99% |
| Corrected, derived **and** applied on 201,900 | 914 d | **0.9937%** | 77.48% |
| **Corrected, derived on 128,099, applied to 201,900** | **504 d** | **2.2817%** | 76.47% |

**Two things must be said about that middle number and neither is flattering.**

**(a) It is 100 − percentile by construction, not a finding.** Once the percentile is taken on the
distribution the rule tests, the exclusion rate is fixed by the choice of percentile alone. The
threshold is no longer an empirical statement about what normal activity looks like; it is a **quota**.
The percentile sweep makes this explicit — every row lands on 100 − p:

| percentile | 128,099 → threshold | delivered failure rate | 201,900 → threshold | delivered rate |
| ---: | ---: | ---: | ---: | ---: |
| 90.0 | 36 d | 9.86% | 82 d | 9.95% |
| 95.0 | 102 d | 4.97% | 241 d | 4.99% |
| 97.5 | 204 d | 2.47% | 471 d | 2.50% |
| **99.0** | **504 d** | **0.99%** | **914 d** | **0.99%** |
| 99.5 | 655 d | 0.50% | 1,405 d | 0.50% |
| 99.9 | 1,406 d | 0.10% | 2,937 d | 0.02% |

`0036` §1's conservative-direction argument (a false-dead removes a pair against a bias already running
down) is untouched and still points at the higher percentile. **But the Human Lead should choose the
99th knowing it is now a choice of exclusion rate, not an inference from behaviour.**

**(b) The stated rate is only delivered if derivation and application share a population.** Step 5's
precedent for `W` is *derived from clean records only, then applied to everyone*. Applying the
clean-sample 504 d to all 201,900 delivers **2.28%**, not 1%. **The same class of mismatch `0037`
withdrew — calibrating on one distribution and applying to another — recurs here in a milder form.**
It is reported, not repaired: repairing it means either deriving on the contaminated population or
abandoning the derive-clean precedent, and both are Human Lead calls.

---

## 5. Rule applied — the four counts, separately, at every population

| Population | threshold | **live** | **not live: measured gap** | **not live: no instant after `τ1`** | **not live: no instant at/before `τ1`** | not live total |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| 201,900 | 914 d | 156,425 | 1,570 | 5,209 | 38,696 | 45,475 |
| 178,165 | 903 d | 136,711 | 1,366 | 4,253 | 35,835 | 41,454 |
| 155,131 | 639 d | 131,304 | 1,324 | 4,253 | 18,250 | 23,827 |
| 152,126 | 632 d | 128,354 | 1,276 | 4,246 | 18,250 | 23,772 |
| **128,099** | **504 d** | **121,725** | **1,216** | **4,120** | **1,038** | **6,374** |
| *201,900 at the proposed 504 d* | *504 d* | *154,390* | *3,605* | *5,209* | *38,696* | *47,510* |

**The measured-gap test is now almost inert; the edge buckets do all the work.** At 201,900, the two
no-measured-gap buckets are **43,905 of 45,475 exclusions — 96.5%**. Even on the clean sample they are
**5,158 of 6,374 — 80.9%**. Whatever the Human Lead decides about the percentile changes very little;
what the buckets mean changes almost everything.

### 5.1 The 5,209 "no instant after `τ1`" bucket is mostly right-censoring, not death

Parallel to `0037` §3's finding on the other bucket, and new here:

- **71.0% of this bucket (3,700 of 5,209) have `τ1` falling after the end of the entire sweep** — after
  the last insertion instant in the whole dataset. On the clean sample it is **78.9% (3,249 of 4,120)**.
- Median `τ1` falls **72.4 days after the account's own last insertion instant**.

**These pairs are not silent accounts. Their window had not closed by pull time.** `0036` §2.3 rules
them not live and this run applied that unchanged, but the name of the bucket describes the wrong
thing for most of its members. Step 9's D10 right-censoring at `max(W, 91) + H` should remove most of
them *before* liveness is ever evaluated — **which makes the order of operations at Step 8/9 material,
and it is not written down anywhere I can find.** Routing this to the Human Lead, not resolving it.

### 5.2 The 38,696 "no instant at or before `τ1`" bucket reproduces `0037` §3 exactly

38,696 at 201,900; 18,250 once contaminated `T0` is excluded; **1,038** in the clean sample; median
`τ1` **1,578.11 days** before the account's first-ever insertion instant; **8,037** with `τ1` before
the calibration curve starts. Every figure matches `0037` §3. Recorded as already-routed to Step 14.

---

## 6. The threshold is now a function of `W`, and the standing instruction is unsatisfiable

`task-sheet.md` Step 7 says: *"Derive the threshold independently. Do not use `W` as an input to the
derivation."* **Under `0037` that instruction cannot be obeyed.** The reference distribution is the set
of gaps *selected at* `τ1 = ⟦T0⟧ + W × 24h`, so `W` chooses which gaps enter the distribution the
percentile is taken on. Measured across the Step 13 `W` arms (`0027`), plus the 91-day arm:

| `W` | threshold on 128,099 | threshold on 201,900 |
| ---: | ---: | ---: |
| 46 | 408 d | 885 d |
| 60 | 423 d | 887 d |
| 91 | 497 d | 912 d |
| **108** | **504 d** | **914 d** |
| 150 | 520 d | 963 d |
| 213 | 576 d | 973 d |

**A 168-day movement on the clean sample across the arms Step 13 is required to run.** Two consequences
the Human Lead should rule on:

1. **`0036` §3's claim that "the threshold is derived independently of `W`, though the test instant is a
   function of it" is no longer true after `0037`.** It survives only in the weak sense that the *gap
   unit* does not contain `W`. The **threshold** does.
2. **Step 13 varies `W` and the liveness threshold as separate robustness axes.** Under the corrected
   basis they are coupled. Either the threshold is re-derived at each `W` arm — in which case the two
   axes are not independent and the arms are not comparable in the way Step 13 assumes — or it is held
   at its `W = 108` value, in which case every non-adopted arm delivers a failure rate other than the
   stated one. **I have not chosen; this needs a ruling before Step 13.**

---

## 7. Judgement calls the spec did not settle

Listed because the dual run exists to surface them, not to have them quietly resolved.

1. **Which population the reference distribution is measured on.** *Not settled anywhere.* The spec
   says only "assert your population against the published waterfall." I propose **128,099** — it is
   the named Step 5 estimation sample, it is what Step 6 used for the other derived threshold, and the
   standing constraint is *never derive thresholds on contaminated timestamps* (23,034 pairs in the
   analysis population have a fabricated `T0`, hence a fictitious `τ1`, hence a gap bracketing an
   instant that never existed). **Counter-argument, which I think is respectable:** `152,126` is the
   more principled clean level, because the 152,126 → 128,099 filter is about the *first S2 watch*,
   which plays no part in either `τ1` or liveness — it excludes 24,027 pairs for an irrelevance and
   moves the threshold by 128 days. **Spread across the five levels: 504 to 914 days.** This is where I
   expect the two instances to diverge.
2. **Pair-weighted vs distinct-gap-weighted percentile.** One long gap on a heavy account brackets many
   pairs. Pair-weighted (chosen — "the rate the rule delivers" is a rate over pairs) gives **504 d** on
   the clean sample; weighting distinct `(account, gap)` keys gives **159 d** (89,624 keys vs 122,941
   pairs). On 201,900: **914 d** vs **202 d**. **This is a larger lever than the percentile choice.**
3. **Percentile method.** `np.percentile` default (`linear`) taken. On the clean sample the panel
   spans 501.75 (`lower`) to 503.96 (`higher`), i.e. **502 to 504 days after the ceiling** — the
   ceiling does not absorb the method difference. On 201,900 all eight methods agree exactly.
4. **Ceiling to whole days**, per `0025` and the Step 6 precedent, rather than a ceiling in continuous
   units. Raw 503.0756 → 504 moves the delivered rate from 1.0005% to 0.9891%. Immaterial here but it
   is a convention, not a derivation.
5. **Strictly-less-than.** Not live iff `gap ≥ threshold`, from `0025`'s rationale (a). **Zero pairs sit
   exactly on any threshold tested**, so the operator is immaterial on this data — stated so a diff on
   it is not mistaken for a bug.
6. **"Every record in its sweep" taken literally**: all 27,656,813 records, including **2,763,257 movie
   records** (`kind = 0`) and all three `action` values. Nothing filtered on show, season, kind or
   contamination class — liveness evidence is account-wide and insertion time is uncontaminated by
   construction.
7. **`np.interp` clamps outside the knot range.** 1,862 records fall below the curve's start and 5,094
   above its end; the below-curve ones all map to the identical first knot time and therefore collapse
   into a single instant under the exact-tie rule. Reported, not corrected — the curve is not mine to
   refit.
8. **Right-censored pairs are ruled not live** per `0036` §2.3, unchanged, despite §5.1's finding that
   most of that bucket is censoring. Applying the rule as written rather than amending it mid-run.
9. **`τ1` uses `⟦T0⟧`, UTC midnight of the `T0` date**, per Step 1 §7. `T0` is read from
   `pair_revision5.csv`; no pair in the table has a missing `T0`.

---

## 8. Status

**Gate. Proposal only. Not adopted, and no threshold is in force.** The Human Lead approves and diffs
against the other instance. Zero API calls were made. No usernames, user IDs or individual watch
histories appear in this file, in `step7-liveness-a2.json`, or in the chart.
