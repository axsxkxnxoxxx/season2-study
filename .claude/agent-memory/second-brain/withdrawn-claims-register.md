---
name: withdrawn-claims-register
description: Standing record of claims this study asserted and later withdrew as false, plus the one objection accepted as a known risk — the study's own error log
metadata:
  type: project
---

# Withdrawn-claims register

**Fact:** ten claims were marked withdrawn-or-accepted in the table at the head of
`artifacts/step1-outcome-definition.md`. Six of them were withdrawn **as false** across the
revisions (the rest are corrections of framing or the one accepted risk). The table is a
standing record of what this study has already gotten wrong and it must not be lost.

**Why:** every one of these was asserted confidently in a draft and survived at least one
review. The failure mode is consistent and worth naming: **asserting a property that does not
follow from the definitions actually given**, or **naming an object without making it
operational**. That is the thing to check for at Steps 5, 6, 7 and 8.

**How to apply:** when reviewing any new gate artifact, check every "therefore", every
"guarantees", and every quantitative range claim against the definitions in the same
document. Check every named object for a numeric threshold. Do not accept "on the order of",
"near zero", "approximately", or "expected to be zero".

## The false-by-construction family

| Claim | Why it was false |
| :--- | :--- |
| `p ∈ (0, 1]` follows from `p = m / L2` | It does not when `F2 > L2`. `L2` is a count, `m` is a number. Fixed by making `p` rank-based |
| Rank-based `p` is safe because out-of-set episodes are dropped upstream | The old drop rule dropped `number > F`, `number < 1`, and missing fields — an episode numbered *inside* `1..F` but *absent* from the listed set survived all three, which is exactly the numbering-gap case |
| Right-censoring at `T0 + max(W, 91)` guarantees 91 days of post-window observation | **False by subtraction.** The guarantee is `max(0, 91 − W)` days: 61 at `W = 30`, **zero** at any `W ≥ 91`, true as written only at `W = 0`. Fixed by declaring `H` |
| D3 and D8 measured "to the pull date" are rates | They were exposure-weighted mixtures whose weight is **show recency** — ~10 years for a 2016 title, ~18 months for one whose S2 finale aired 31 Dec 2024. Fixed by the constant horizon `H` |
| "On or before `T1`" is a single unambiguous operator | Ambiguous by one day; `date(watched_at) ≤ T1` and `watched_at ≤ T1T00:00:00Z` are both faithful readings and disagree on every evening watch. On the operator that assigns **every** outcome state |
| A show is weekly when its span is "on the order of" `(L2−1)×7` and binge when "near zero" | Not thresholds and not exhaustive — hiatus, two-episode premiere and two-per-week seasons land in neither bucket, and a required stratum with unassigned members gets silently pooled |

## The framing corrections

| Claim | Correction |
| :--- | :--- |
| Entry and exit are symmetric | They are not. S1 completion is evaluated over **all time**, S2 completion **within `W`**. Same arithmetic, different quantifier. The asymmetry pushes pairs into Started-and-left; D3 measures how much |
| Right-censoring costs zero rows | `S1_completion_date` is uncapped, so censoring removes recent S1 completers — people who found an old show lately, who are disproportionately likely to continue. It moves the headline **up** |
| Truncating negative lags at zero | Withdrawn; it made `W` a function of the frame's cadence mix rather than of viewer behaviour |
| "Pull date" needs no definition | Undefined and load-bearing in four places |
| Liveness is a statement about the account | **Mis-scoped.** The evidence is account-wide, the test is pair-specific. Liveness is a **pair-level** filter |

## The one accepted risk

The liveness bound is inflated, and it stays that way by Human Lead ruling. Full objection,
ruling and reason in [[gate-step1-outcome-definition]].

## One live provenance gap, not a withdrawn claim

Two figures in the approved public document — the **28 percent play-event inflation** in §2.1
and the **six-week S1/S2 overlap** in §5 — are numerically correct but cite "the Step 0 probe"
and appear in **neither** public Step 0 artifact. See [[open-items-and-contradictions]].

Related: [[glossary-terms-and-thresholds]], [[gate-step1-outcome-definition]].
