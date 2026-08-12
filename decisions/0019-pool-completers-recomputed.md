# Decision 0019 — `pool_completers` is recomputed on real season lengths; the max-observed proxy is superseded

| | |
| :--- | :--- |
| **Decision** | **`pool_completers` is recomputed on the real `E1`, `L1` and `F1` now in the Step 2 frame.** The max-observed season-length proxy is **superseded, and no result may use it.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Status** | Closed |
| **Related** | Step 1 §3.1, which forbids `F := L` outside the §3.3 fallback; [0013](0013-step2-execution-delegation.md) condition 2, whose stated premise this entry corrects |

---

## What was replaced

The S1-completer diagnostic had no Step 2 frame to draw on, so it substituted a proxy: `L1_hat :=
F1_hat :=` the maximum S1 episode number observed across the pooled cohort. That is exactly the
shape Step 1 §3.1 forbids — `F := L` — and the diagnostic said so at the time, used it only because
nothing else existed, and marked it not adopted.

The frame now carries the real thing, one call per show from
`GET /shows/:id/seasons?extended=episodes,full` with season 0 filtered: a real episode-number set
`E1`, a real `L1 = |E1|`, and a real `F1 = max(E1)`. The proxy has no further reason to exist.

The recompute applies the **approved Step 1 §4 rule** unchanged — `F1 ∈ D1` and
`|D1| ≥ ceil(0.90 × L1)`, with `D1` the distinct S1 episodes whose number is a **member** of the
real `E1` — against real inputs.

## The result: nothing moved, and that is a finding rather than a null

| | Proxy | Real |
| :--- | ---: | ---: |
| Total S1-completer pairs, in-frame | 232,958 | **232,958** |
| Shows whose count rose | — | **0** |
| Shows whose count fell | — | **0** |
| Shows falling below 50 completers | — | **0** |

**The reason is checkable and was checked: the proxy `L1_hat` equals the real `|E1|` on 1,225 of the
1,226 in-frame shows.** That is what the diagnostic predicted for this population — on a show with
at least 50 completers, at least 50 users independently reached the true finale, so max-observed and
true season length coincide.

The single exception is **Star Trek: Prodigy**: real `L1 = 19` with `F1 = 20` — 19 episodes numbered
up to 20, the only internal-gap season in the frame — against a proxy `L1_hat` of 20. Both give a
bar of 18 episodes and the same finale episode, so its count is 74 either way.

**This is not a rehabilitation of the proxy.** It was never trustworthy in the long tail, where most
shows carry one or two users and a single viewer's stopping point sets the whole season length. It
happens to have been exact on the ≥50-completer population, and nowhere else is that claimed.

`pool_completers_proxy` is retained as a column so the two remain diffable without a rerun.

## A correction to the reasoning in 0013 condition 2

[0013](0013-step2-execution-delegation.md) condition 2 required the completer diagnostic to be
re-run on the full pool before the frame was built, reasoning that **"completer counts only rise"**
as the pool grows, so shows below 50 would cross it.

**That premise is not strictly true**, and the mechanism is the same proxy defect described above.
Adding users can raise `L1_hat` for a show, which both raises the `ceil(0.90 × L1)` bar and moves
`F1_hat` to an episode the earlier users had not watched — retroactively **un-completing** them.
Measured across the 41,964 shows present in both the 2,134-user and 2,549-user runs:

| | |
| :--- | ---: |
| Shows whose completer count **fell** | **118** |
| — of those, shows whose `L1_hat` rose | 118 (all of them) |
| Total completer pairs lost | 177 |
| Shows at ≥50 completers whose `L1_hat` rose | **0** |

Every affected show is in the long tail. The ≥50 candidate set was untouched — all 1,700 shows from
the earlier run were retained and 394 newly crossed, with none dropping out.

**The conclusion of 0013 condition 2 stands; only its stated reason is corrected.** The recompute
was necessary because counts **move**, not because they only rise. Both directions matter once a
threshold is drawn on them, and a rule justified by a one-directional premise is fragile in a way
the two-directional statement is not.

## One thing this does not decide

**The ≥50 candidate rule was applied to the proxy counts and has not been re-applied to the
recomputed ones.** On this frame the question is moot — zero in-frame shows fall below 50 — but the
candidate set's basis remains proxy-derived, and that is stated rather than left implied. If the
frame is rebuilt after a resumed pull, whether the threshold is applied to real counts from the
outset is a live question, not a settled one.
