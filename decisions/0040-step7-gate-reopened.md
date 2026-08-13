# Decision 0040 — The Step 7 gate is reopened: `0021` is reinstated, the 18,250 are returned, derivation moves after D10

| | |
| :--- | :--- |
| **Decision** | **The Step 7 gate is REOPENED and `0039`'s approval is suspended.** `0036` §2.3's **second edge case is WITHDRAWN** — it contradicted an approved gate. **The 18,250 pairs are returned to the population.** **Derivation moves to after D10.** The conservative-direction argument is **withdrawn**. Four superseded figures in `task-sheet.md` are corrected, and two errors in `0039` itself. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's gate review of Step 7, verdict **HOLD** |
| **Amends** | `decisions/0036` §2.3; `decisions/0039` §2, §6, §7 and status; `task-sheet.md` Step 7 and Step 9 |
| **Status** | Closed. **Step 7 reruns. Step 8 is NOT unblocked.** |

---

## 1. `0021` is reinstated, and `0036` §2.3(ii) is withdrawn

**Two bullets in the same step of the same file contradicted each other.**

`task-sheet.md` line 233, carrying `0021`'s standing ruling from **approved gate 2 of 5**:

> **Any record inserted after the window closed proves the account was alive, whatever date it
> claims** — backfilling an old show is still activity.

`0036` §2.3, second edge case:

> If there is **no insertion instant at or before `τ1`**, the pair is **not live.**

**Every pair in that bucket has insertion instants *after* `τ1` by construction** — the run records
**zero** accounts with no instants and a **minimum of three gaps per account**. So `0021` rules them
**live** and `0036` ruled them **dead**.

**That bucket is 18,250 pairs — 76.8% of the filter's 23,772 exclusions, and 12.0% of the frozen
population.** Nothing in `0036`, `0037`, `0038` or `0039` cited `0021` against it. `0037` §3 diagnosed
the mechanism correctly — a clock mismatch, `T0` on claimed `watched_at` against liveness on insertion
time — and then **routed it to Step 14 as a limitation.**

**A limitation is the wrong disposition for a rule that overrides an approved gate.** `0021` was
approved after four Red Team rounds. **`0036` is not a gate, and two of its three sections have already
been withdrawn.**

### 1.1 `0021` is also substantively right here

For a pair whose account began after `τ1`, **the entire history is an import**, and **whether S2
appears in that import is exactly the outcome.** Absence there is **more** informative than for a
real-time logger, not less. The rule carried one liveness concept — *was the account logging at `τ1`* —
while the data contains two failure modes, and it applied the wrong one to the larger.

**The 18,250 are returned. An account with insertion activity after `τ1` is live.**

## 2. Derivation moves to after D10

**`0038` §2.1 ranked this requirement first — "the derivation and application populations must be
identical" — and the run violated it.** Liveness is applied at **Step 8 position 6, after
right-censoring at position 5** (`0029`), so the application population is the **152,126 less D10**,
while both arms derived on the uncensored set. `0039` §6 noticed the uncensored derivation and treated
it as inflating one bucket's count rather than as the derive/apply mismatch the spec defines it to be.

**And the fix dissolves a problem the record had called forced.** `0039` §5 justified restricting the
reference to measured-gap pairs because open-ended gaps are **3.17%** of the extended set, so a 99th
percentile over it would be **infinite**. **After D10 the open-ended share falls to 894 / 130,524 =
0.685%, below 1%.** The 99th percentile over the extended set is then **finite**, an infinite gap
**fails a finite threshold on its own**, and **edge case (i) stops needing to be a separate ruling.**

Between §1 and §2, **both edge-case branches — which did 94.6% of the filter's work — are resolved
without a threshold argument.** One by an approved gate that was already on the books, one by running
the filters in the order the spec already fixes.

## 3. The conservative-direction argument is withdrawn

Every defence of erring high — `0036` §1, `0025`, `0029` §2, `task-sheet.md`, both arms' write-ups, and
`0039` §7 — cited **Step 14 bias 2**: *the accounts that **stop** logging are disproportionately the
ones that would have scored never-started.*

**That mechanism describes accounts that stopped. The 18,250 were accounts that started late.** Bias 2
is silent on them and its sign for them is unknown.

**So the argument covered the 1,276 gap-test exclusions and the ~880 genuine silences — about 9% of the
filter — and nothing else.** `0039` §7 carried it forward as though it covered the whole rule.
**Withdrawn as a justification for the edge-case branches.** It remains valid for the gap test itself.

## 4. Four superseded figures were standing in `task-sheet.md` as operative spec

**`0039` corrected `0038` §5 and did not correct the task sheet — and Step 8 launches off the task
sheet.** Line 248 still carried, verbatim, the claim `0039` §4 had declared arithmetically impossible.

| Line | Stated | Measured on the frozen population |
| :--- | ---: | ---: |
| **248** | 3.45% / 96.55%, **invariant across the 90th–99.9th** | **5.37% / 94.63%**, ranging 36.5% → 0.4% — **and the invariance is impossible** |
| 242 | 37.4% exceed the pooled-99th | **34.12%** |
| 246 | weighting lever 159 d / 202 d | **190 d** |
| 235 | `W`-coupling 408→576, 885→973 | **576→697** |

**All four were measured on populations the spec had already moved away from.** All four are corrected,
each labelled with what it superseded. **Both figures at line 248 change again** once §1 and §2 take
effect, so the spec now requires each instance to **measure and state the split on its own population**
rather than repeat a number.

## 5. Two errors in `0039` itself

**§6 recorded a divergence that does not exist.** It said instance A measured 3,367 against the sweep
end while B measured 3,352 against the pull date, "definitional." **A reports both figures** —
`of_which_tau1_past_global_sweep_end: 3367` and `of_which_tau1_past_pull_instant: 3352` — and **B's
3,352 matches A's pull-instant figure exactly.** Two references, one dataset, no disagreement. The
entry invented a divergence between arms that agreed. **The ~880 are also pairs, not accounts** — 879
and 894 on the two references.

**§2's "identical on every published number" is false as written.** The two markdown artifacts publish
**34.1%** and **36.96%** for the same quantity on the same population. Both computed 0.34121
internally, so it is a ceiling-versus-raw comparator difference rather than a computational divergence
— **but the two public artifacts contradict each other on their face**, and both misattribute the
difference to "a different population" in their own corroboration tables.

## 6. Step 9 must test whether the threshold is load-bearing at all

**Recompute the headline at both endpoints of the liveness threshold's account-clustered interval**,
alongside the point value.

- **If the headline is insensitive across that band, the threshold is DELETED rather than published
  with an interval.** The honest rule becomes *"the account has insertion evidence bracketing `τ1`"*,
  with **no free parameter**.
- **If it is sensitive, the threshold is load-bearing** and the band must be propagated into the
  headline as a sensitivity range — **which no step currently does.**

Red Team's assessment of the interval, which is what makes this the right question: `[528, 787]` spans
roughly **±275 pairs, ±0.18pp of the population**, and it was estimated from **300 bootstrap
replicates** whose endpoints are the 7th and 8th order statistics quoted to the day — against **B =
1000** for the i.i.d. interval it is contrasted with, and **instance A ran no bootstrap at all.** *"An
interval that wide around a quantity that inert is an argument for deleting the number, not for
publishing it with an interval."*

**Zero API calls. Answerable on cached data.**

## 7. On the dual run's exact agreement

**Weak evidence of correctness, and the record should say so.** Every published quantity is a
deterministic function of frozen inputs — the same cached sweep, the same stored calibration curve
neither arm refits, an exactly-specified collapse rule, a named percentile, a named population.
**Agreement was `0038`'s design goal.** It confirms the spec is unambiguous; it cannot confirm the spec
is right.

Both arms said as much implicitly by listing six and seven judgement calls the spec still does not
settle — including the `np.interp` clamping of **6,956** records, which they happened to resolve
identically and which would have changed every downstream number had either chosen otherwise. **And the
one place they did independent work — the bootstrap — is where the approval took its second headline
number, with no cross-check.**

## 8. Scope

- **`0039`'s approval is suspended, not deleted.** The entry stands with its errors marked, because the
  reasoning that produced them is part of the record.
- **Step 7 reruns on the corrected spec** as a dual pair with explicitly assigned namespaces.
- **Step 8 does not launch.** Gate 4 of 5 is open again.
- **Zero API calls.**
