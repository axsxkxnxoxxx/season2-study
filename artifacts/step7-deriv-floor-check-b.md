# Step 7 — verification of the DERIV started-and-left floor and Continued ceiling

**Instance:** `data-scientist-b`, namespace `b` · **Date:** 2026-08-13 · **API calls: 0** · **Adopts nothing.**

> **This is a verification, not an adoption.** The proposed correction was reproduced from this
> instance's own stored pair-level arrays and asserted against them. It was not taken on the strength of
> having been proposed.

Task: `specs/step7-deriv-floor-verification.md`. Machine-readable companion:
`artifacts/step7-deriv-floor-check-b.json`. Working files: `processed/step7/df_b/`.

**Rule, unchanged: ALT-BROAD (`decisions/0048`).** A pair is NOT LIVE iff **both** the account shows no
insertion instant after that pair's `τ1` **and** the pair is not Continued. Silence anchored at `τ1` and
only at `τ1`. `W = 108`, `H = 91`.

---

## 1. What was recomputed, and from what

Every figure below was recomputed from the pair-level boolean arrays in
`processed/step7/mm_b/pairs.npz` and `processed/step7/mm_b/outcomes.npz` — 201,900 rows, the Step 5
line-1 contamination-clean pair table — by re-deriving `τ1 = ⟦T0⟧ + 108 × 24h`,
`τ2 = ⟦T0⟧ + 199 × 24h`, the ALT-BROAD liveness predicate and the channel predicate from first
principles. **Nothing was read out of a stored aggregate and reported.** The stored aggregates
(`processed/step7/bb_b/waterfall.json`, `processed/step7/mm_b/channel.json`) were then asserted against
the recomputation and agree on every count.

Two self-consistency assertions passed before any result was formed: the stored `no_after_tau1_W108`
flag equals `max_insertion ≤ τ1` on all 201,900 rows with zero mismatches, and the three outcome states
partition both populations exactly.

Populations, stated once and then labelled at every point of use:

| | definition | n |
| :--- | :--- | ---: |
| **APPLY** | Step 5 line 1 less D10, D10 re-derived at `W = 108` | **196,654** |
| **DERIV** | Step 5 line 4 less D10, D10 re-derived at `W = 108` | **147,370** |

## 2. The proposed correction — every row CONFIRMED

**DERIV, n = 147,370.**

| row | proposed | reproduced here | verdict |
| :--- | ---: | ---: | :--- |
| channel count | **89** | **89** | **CONFIRMED** |
| S&L floor, extreme ALL | **16,655 → 11.3015%** | **16,655 → 11.3015%** | **CONFIRMED** |
| S&L floor, extreme NONE | 16,744 → 11.3619% | 16,744 → 11.3619% | **CONFIRMED** |
| S&L ceiling | 16,843 → 11.4291%, unchanged between extremes | 16,843 → 11.4291%, unchanged | **CONFIRMED** |
| Continued ceiling, extreme ALL | **121,570 → 82.4930%** | **121,570 → 82.4930%** | **CONFIRMED** |

**Nothing is refuted.** `16,744 − 89 = 16,655` holds on my own arrays, and the adopted DERIV bound is
**[11.3015%, 11.4291%], width 0.1276 pp** — numerator `16,843 − 16,655 = 188` pairs. The superseded
un-widened width was 0.0672 pp, numerator 99.

## 3. Both populations side by side — the four quantities

All counts are pairs. **Every share names its denominator.**

| quantity | **APPLY**, n = 196,654 | **DERIV**, n = 147,370 |
| :--- | ---: | ---: |
| exclusions (never-started + started-and-left) | **703** = 604 + 99 | **99** = 0 + 99 |
| retained never-started / S&L / Continued | 32,769 / 19,042 / 144,140 | 9,145 / 16,744 / 121,382 |
| **1. channel count** (¬Continued, `\|A\| ≥ 1`, last insertion in `(τ1, τ2]`) | **90** | **89** |
| channel including its never-started component | 297 = 207 + 90 | 92 = 3 + 89 |
| **2. S&L floor, extreme NONE** | 19,042 → **9.6830%** | 16,744 → **11.3619%** |
| **2. S&L floor, extreme ALL** *(adopted)* | **18,952 → 9.6372%** | **16,655 → 11.3015%** |
| **3. S&L ceiling** | 19,745 → **10.0405%** | 16,843 → **11.4291%** |
| **3. does the ceiling move between extremes?** | **No — 0.0000 pp** | **No — 0.0000 pp** |
| **4. Continued ceiling, extreme ALL** *(adopted)* | **144,933 → 73.6995%** | **121,570 → 82.4930%** |
| Continued ceiling, extreme NONE | 144,843 → 73.6537% | 121,481 → 82.4327% |
| Continued floor | 144,140 → 73.2962% | 121,382 → 82.3655% |
| bound width, widened | **0.4032 pp** (793 pairs) | **0.1276 pp** (188 pairs) |

The channel's never-started component — **207 on APPLY, 3 on DERIV** — is measured and reported but
does **not** enter the started-and-left floor, which is what the spec asked for and what the arithmetic
`16,744 − 89` encodes. Those pairs are not in the started-and-left count to begin with.

**A note the DERIV column needs.** The DERIV never-started bound is **degenerate — [6.2055%, 6.2055%]**,
because the never-started exclusion component is 0 there; the started-and-left bound and its
"conditional sub-interval over the S&L exclusions alone" therefore **coincide** on DERIV. And the DERIV
post-liveness never-started point estimate is **6.2096% on 147,271**, which lies **0.0042 pp outside its
own bound on 147,370** — the bound bounds the position-5 population and the estimate is post-liveness.
Reproduced here; it is the population mismatch `0055` §6 routes to Step 14, not a new finding.

**The three ceilings still cannot all hold**, and the widening is what makes the excess exact.
**APPLY:** 16.9704% + 10.0405% + 73.6995% = **100.7104%**, excess **1,397 pairs** = 2 × 604 + 99 + 90.
**DERIV:** 6.2055% + 11.4291% + 82.4930% = **100.1276%**, excess **188 pairs** = 2 × 0 + 99 + 89. Both
reproduce the decomposition in the task sheet exactly.

## 4. Does the endpoint move between the extremes?

**Yes, on both populations, and by more on DERIV.**

| | floor movement | ceiling movement |
| :--- | ---: | ---: |
| **APPLY**, n = 196,654 | **0.0458 pp** (90 pairs) | **0.0000 pp** |
| **DERIV**, n = 147,370 | **0.0604 pp** (89 pairs) | **0.0000 pp** |

The choice is **not** numerically empty. It is larger on DERIV than on APPLY despite one fewer pair,
because the DERIV denominator is 25% smaller — a point worth stating, since the population that got the
correction last is the one where it matters more. On DERIV the 89 channel pairs are **47.3% of the whole
bound width** (89 of 188); on APPLY the 90 are **11.3%** (90 of 793). **The un-widened DERIV bound was
missing nearly half of its own uncertainty.**

**The widening is one-sided and the ceiling genuinely does not move.** The channel pairs are retained and
observed as started-and-left, so they are already inside the ceiling's numerator; the ceiling asks how
large the true started-and-left count could be, and admitting that a channel pair might be Continued
cannot raise it. The **Continued** ceiling moves in lockstep with the floor, by the same 89 and 90 —
which is the correct behaviour, since the same admission that lets a channel pair leave the S&L floor is
what lets it enter the Continued ceiling.

**One ambiguity in the question, flagged so it cannot bite later** (DF-4 in the JSON). "The ceiling under
extreme ALL" has a second reading: if both endpoints were evaluated inside the single world "all channel
pairs are truly Continued", the ceiling would fall to **16,754 → 11.3687% on DERIV** and **19,655 →
9.9947% on APPLY**. **Those are not bound endpoints and must not be recorded as any.** A bound's floor
and ceiling are **alternative worst cases over one set of admissible worlds, not two readings of one
joint state** — the task sheet says exactly this — so the floor is taken at the corner where every
channel pair is Continued and no exclusion is S&L, and the ceiling at the corner where every channel
pair is S&L and every exclusion is too. Under that reading, which is the one a bound means, the proposed
table's "unchanged" is right.

## 5. Is the widened floor the right endpoint — and does any margin statistic belong?

**The widened floor is the right endpoint, and I would hold that position without the movement measured
above.** The floor answers a question about the *support* of the set of worlds the evidence admits: what
is the smallest true started-and-left count consistent with what we observed? A channel pair is
¬Continued, live only because it inserted after `τ1`, and silent from its last insertion `s ∈ (τ1, τ2]`.
Continued is read on `A_H`, the episodes with `watched_at < τ2`. That pair's history after `s` is
**unobserved by construction**, so a world in which it completed S2 inside `(s, τ2)` is consistent with
every byte we hold. It is admissible. A floor that excludes an admissible world is not a floor, and
`0052` §4's ground for declining to widen — that it would be the fifth consecutive non-covering endpoint
— inverts the relation, since widening is the operation that makes an endpoint covering.

**No margin statistic belongs in an endpoint's justification. Not p5, not the median, not the minimum,
not any of them.** Three reasons, and I hold all three.

**It is a category error.** Admissibility is a property of the support; a margin is a property of the
measure. `p5 = 1.7 days` removes exactly zero pairs from the admissible set. Even the pair at the
minimum — **0.1333 days, 3.2 hours, reproduced here on both populations** — could have finished the
season inside that remainder, and binge viewing is precisely the regime where many episodes carry
`watched_at` values hours apart. The question a floor asks is *can it*, and the answer is yes at every
percentile of the margin distribution. Plausibility answers a different question that no endpoint is
asking.

**It is non-robust in a way that is self-demonstrating here.** The same statistic on the same 90 pairs:
**p5 = 1.6552 days, median = 44.5272 days.** I reproduced both from my own arrays, and they are the same
quantity — `τ2` minus the last insertion instant — differing only in which quantile is quoted. `0054`
quoted the tail to argue the 90 "had ample opportunity and did not"; the median says the typical channel
pair had **48.9% of its Continued window unobserved**. An argument whose conclusion flips on the choice
of quantile was never being carried by the evidence; it was being carried by the choice. **`0055`'s
cherry-picking charge is confirmed arithmetically, not merely accepted.** And the failure is symmetric —
the median is equally inadmissible, and I would refuse it just as fast if it were quoted to widen
something I wanted widened.

**It reintroduces a threshold through the side door.** "The margin is large enough that we may treat
these as truly S&L" is a threshold rule with an unowned parameter, and Step 7's entire history —
`0042`'s parameter-free gate, `0044` §2's withdrawal of the instruction to vary a liveness threshold —
is the removal of exactly that shape from this step. Putting it back in the *justification* rather than
the *rule* does not make it not a parameter; it makes it a parameter no one is varying in Step 13.

**Where the margin distribution does belong: as a Step 14 limitation, reported as a distribution and
never as a single quantile.** It is the honest way to say how large the exposure is — "for half of the
channel pairs, roughly half the Continued window is unobserved" is a true and useful sentence. It
describes the endpoint's size. It must not set it. That is why the distributions are in this file's JSON
under a key that says they were measured and not used.

## 6. Defects found — reported, not fixed

**DF-1, high. `artifacts/step7-liveness-bb-a.md` and `-bb-b.md` print the un-widened DERIV figures with
no supersession stamp.** `bb-b.md:176` carries **"DERIV: [11.3619%, 11.4291%], width 0.0672 pp"** and
`:184` carries **"DERIV [82.3655%, 82.4327%], width 0.0672 pp"**; `bb-a.md:185` and `:206` carry the
same pair. `0055` §3 makes `artifacts/` the seventh propagation surface and §5a states this exposure
would be **"stamped, not rewritten."** **It is not stamped.** Running the control `0055` §3 mandates:
the negative half fails — the superseded forms are present and unmarked — and the **positive half fails
too**, since `11.3015`, `82.4930`, `16,655` and `121,570` return **zero hits in either `bb` file**.
This is the exact shape `0055` §5a warned about, in the deliverable pair named for the **adopted** rule,
and one of the two files is this instance's own. Not fixed: propagation is assigned elsewhere and the
brief forbids self-repair of the record.

**DF-2, low. `0055` §3's false-positive register for `16,744` is incomplete.** It names one legitimate
reading (`bb-a.md:109`, the post-liveness count on 147,271 → 11.3695%). A **third** exists:
`artifacts/step7-sensitivity-b.md:76` carries 16,744 as the parameter-free `0021` rule's started-and-left
count on a different denominator again. An incomplete register produces an unexplained grep hit and
invites a propagation pass to "correct" a correct number.

**DF-3, low. The channel window is written two ways in the operative files** — `(τ1, τ2]` in
`specs/step7-deriv-floor-verification.md`, `(τ1, τ2)` in `task-sheet.md:350` and in
`.claude/agents/data-scientist-b.md`. **Measured inert at `W = 108`:** open, half-closed and closed
forms all give **90 on APPLY and 89 on DERIV**, identical to the count from the stored "no insertion
after `τ2`" flag, because no pair's last insertion falls exactly on either instant. **Inert is not
specified**, and it need not stay inert at another arm.

**DF-4, medium. The spec's item 3 admits the joint-state reading described in §4 above.** The proposed
answer is correct; the alternative numbers are derivable from the same files and are not endpoints.
Named so they cannot be re-derived and mistaken for the ceiling.

**Snapshot check.** My snapshotted definition file was compared against on-disk `task-sheet.md`,
`CLAUDE.md` and `decisions/0055` on every figure in scope. **It agrees on all of them** — it carries
16,655 → 11.3015%, 121,570 → 82.4930% and width 0.1276 pp, and names 16,744 → 11.3619%, 0.0672 pp and
121,481 → 82.4327% as superseded. The only disagreement found is DF-3's boundary form.

---

**This instance adopts nothing, did not read the other arm's output, and did not ask about it.**
