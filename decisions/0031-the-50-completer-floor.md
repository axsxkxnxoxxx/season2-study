# Decision 0031 — The ≥50 S1-completer floor, justified against its own sensitivity curve

| | |
| :--- | :--- |
| **Decision** | The candidate-set rule — **shows with ≥50 S1 completers in the pool** — **stands as adopted.** This entry supplies the justification it never had. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-12 |
| **Occasioned by** | `reviewer-product`'s Step 2 review, finding 3 |
| **Status** | Closed |

---

## Why this entry exists

The ≥50 floor is **the largest population rule in the study.** It takes the pool from **44,617
shows with any S1 evidence to 2,094 candidates**, and the seven ledger rules then take that to
**1,138**. The frame is **2.6% of the shows the pool has evidence for.**

It was the only rule of that magnitude with **no decision entry of its own**. It appears inside
`0014`, `0019` and `0023` — always as an inherited rule referenced in passing. By contrast a
12-show exclusion got [0015](0015-step2-unaired-s2-exclusion.md) to itself, and the 26-episode cap
got [0020](0020-step2-structural-thresholds.md) with a full insensitivity table.

`0014` set the discipline for this study explicitly: **look at the distribution, then draw the
line.** Every other threshold went through it. This one did not. The reviewer's charge is that a
rule with this much downstream leverage should not be the only one nobody decided, and that is
correct.

## The sensitivity curve, which is what was missing

Candidate shows at each floor, from `artifacts/s1-completer-diagnostic.md`. **Zero API calls.**

| Floor | Candidate shows | vs. adopted |
| ---: | ---: | ---: |
| ≥10 | 7,643 | +265% |
| ≥25 | 3,793 | **+81%** |
| **≥50 (adopted)** | **2,094** | — |
| ≥75 | 1,378 | −34% |
| ≥100 | 1,038 | **−50%** |
| ≥250 | 361 | −83% |

**This is a genuinely sensitive threshold**, and the entry does not pretend otherwise. Moving it one
step either way changes the candidate set by roughly half. `0020` could defend 26 episodes on the
grounds that 26→40 moved the frame by ≤1.3 points of pairs; **no such defence is available here**,
and none is offered.

### What the floor is actually buying, measured inside the frame

| In-frame shows with | Shows | Share of frame | Pairs carried | Share of pairs |
| :--- | ---: | ---: | ---: | ---: |
| 50–59 completers | 152 | 13.4% | 8,233 | **3.7%** |
| 50–74 completers | 329 | 28.9% | 20,096 | **9.1%** |
| 50–99 completers | 480 | 42.2% | 33,063 | **15.0%** |

Frame median is **115** completers, p25 is **71**.

**The asymmetry is the argument.** Shows near the floor are 42% of the frame by count and 15% of it
by pairs. Raising the floor to 100 would discard nearly half the titles to buy 15% fewer rows;
lowering it to 25 would admit 1,699 more shows, each contributing on the order of tens of pairs, at
a cost of **1,699 API calls** to fetch their seasons. **The floor is where per-show statistical
weight stops justifying per-show acquisition cost**, and that is the honest reason for it — not a
property of the distribution, which has no break at 50.

## What cannot be computed, and is not claimed

**The frame at ≥25 is not computable from what is on disk.** The candidate set at that floor is
3,793 shows and seasons metadata was fetched only for the 2,094. Producing the comparison would cost
**1,699 live calls**. The reviewer asked for "one number: what the frame looks like at ≥25", and
that number is **not free** — the candidate count is, the frame is not.

So this entry justifies the floor on the curve above and on the cost argument, and **does not claim
the frame would be materially unchanged at 25.** It might not be.

## The consequence, stated for Step 14

**The frame is a large-title frame by construction**, and this is now carried as a Step 14
limitation. Small and niche shows are absent, and **no result generalises to them.**

The reviewer's product-side objection is recorded because it is the one that matters for the
write-up: **a slate's hard renewal calls cluster in the marginal performer, not the top 2.6%.** The
study can say what happens to titles with a measurable audience. It cannot say what happens to the
ones a commissioning editor is most uncertain about, and Step 15's decision rule must not be
phrased as though it can.

There is a second-order effect worth naming: **the floor is a higher bar for recent titles**, since
a 2025 show must accumulate 50 completers in months where a 2012 show had fourteen years. The
2023–2025 cohort is therefore not merely smaller but **differently selected** — a point the frame
write-up previously attributed entirely to the exclusion of unaired second seasons.
[0030](0030-frame-field-corrections.md) separates that effect out of the size quintile; it cannot be
removed from the frame's composition.

## Why the floor is not moved

Moving it now would restate the cohort, which re-runs the completer diagnostic, which moves the
candidate set and the frame — the same cascade [0023](0023-step4-completeness-rule-upheld.md)
declined to trigger for a 0.13-point correction. Lowering it would additionally cost 1,699 API calls
against a study whose access is its scarcest resource.

**The floor stands. What changes is that it now has a stated warrant, a published sensitivity curve,
and a named limitation** — which is what the reviewer asked for, and what it lacked.
