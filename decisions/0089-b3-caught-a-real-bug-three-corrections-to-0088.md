# Decision 0089 — B3's per-site assertion caught a real bug; three corrections to `0088`; the tie-break is a new gap

| | |
| :--- | :--- |
| **Decision** | **No new ruling. `0088`'s three rulings are implemented and the entry itself is corrected in three places.** ***B3 EARNED ITS COST ON THE FIRST RUN:*** instance B's per-site D11 table **found a real defect in its own previous build** — D11 was reaching the four `action_count_s1_*` columns with no ruling behind it, and **asserted per site those four would have FAILED on r3.** **Three corrections to `0088`:** the boundary window was named as the interval on which the forms **agree**; `747,478` was mischaracterised; and §3 **named a third-place cluster that is not determined.** **The tie-break is CARRIED for the Human Lead**, with `specs/` as a possible ninth surface. |
| **Recorded by** | Analytics Engineer, on both arms' rerun findings |
| **Date** | 2026-08-16 |
| **Occasioned by** | The 2026-08-16 reruns against `0088`, builds `a/2026-08-16-0088` and `b/…-r4` |
| **Amends** | `0088` §1(a), §2 and §3; `0087` §2 (the "62 apart" reading) |
| **Verified by** | `check_surfaces.py` **PASS**; the `analytics-engineer` pair byte-identical apart from `name:` |
| **Status** | Open. **Step 8 is NOT approved. Two items carried for the Human Lead in §4.** |

---

## 1. B3 worked, and it worked on the first run

**The ruling was to measure rather than publish a residual. The measurement immediately found a defect
no control, no review and no arm had seen in five builds.**

**Instance B's per-site D11 table: 13 sites, D11 applied at 12, asserted at each.** The S1-side
carry-through **has a ruling behind it only for the completion walk** (`0068` publishes line 1 at
220,107) — **but it was also reaching the four `action_count_s1_*` columns, where nothing exempts it.**

> ***Asserted per site, those four sites would have FAILED on r3.***

**D11 is now applied there: 73 records (49 watch / 1 checkin / 23 scrobble), 44 pairs in the record
universe, 4 of them in the APPLY position-5 row set.** **No waterfall line, outcome share or invariant
moves.** The single `no` in the table is the S1 completion walk, and **three distinct objects sit behind
it: 73 records → 72 distinct episodes → 60 whose canonical instant is post-cutoff.**

**This is the argument for the ruling, made by the ruling.** A per-site assertion found in one run what
*"D11 is applied to every computation"* had asserted in prose across five builds and two gate reviews.

**And B3(c) returned more than a pass.** `tau2 > τ_pull` is 0 on both populations — **but 20 APPLY rows
and 17 DERIV rows sit with `tau2` EXACTLY at `τ_pull`.** **The bound is attained: a `>=` form of the
same assertion would fail.** **A passing assertion at the bound and one with slack are not the same
evidence**, and only the arm that measured it can tell them apart.

**Instance B also rebuilt its coverage apparatus** against `0087` §4: its r3 build **hardcoded
`identity_holds: True` at invariants 2, 4 and 7**, and its aggregate chained `.get(…, .get(…, True))`
so **an invariant carrying no coverage key contributed a pass.** Rebuilt so that **the population size
comes from a different file than the asserted count** — **9 of 9 identities independently sourced, 0
literals, 0 defaults** — and demonstrated failing: an invariant asserted on 195,951 while naming
position 5 now reports `195,951 + 0 = 196,654` and **fails**, which is exactly the r3 gap at invariant 6.

## 2. Three corrections to `0088`, all found by the arms

**(a) The boundary window was the wrong interval.** `0088` §1(a) named `[τ1 − 24h, τ1)`. **`T0` is
day-floored, so `τ1` and `τ2` are midnight-aligned**, which makes `date(ts) < date(τ1)` identical to
`ts < τ1` below the boundary — **the named window is where the two forms AGREE.** The separating
interval is **`[τ1, τ1 + 24h)`**.

***CORRECTED 2026-08-16, Red Team fifth pass, F1. This entry said "Both arms emitted both intervals
rather than only the one ruled." THAT IS FALSE OF ARM B.*** **Arm A emits the separating interval — 703
episodes on 311 rows at `τ1` and 303 on 136 at `τ2` on APPLY, 595/275 and 261/117 on DERIV. Arm B emits
the RULED window and the single instant exactly at `τ1`, and nothing else**; the separating interval
appears nowhere in its deliverable or its source. **Only ONE arm emitted both.**

***AND THE VERDICT THIS ENTRY ADOPTED WAS MEASURED ON THE WRONG SET.*** Arm B's `OCCUPIED_INERT` and
*"no outcome state differs between the two forms"* is a claim about **the set on which the forms
differ**, computed on **1 row of the 311.** **Adopting it here repeated the exact defect this section
was written to correct** — a statement right in substance and wrong in the object it names — **inside
the entry fixing the first instance of it.**

***THE NUMBER THAT SETTLES B3 IS MEASURED BY NEITHER ARM:*** on `[τ, τ + 24h)`, **how many position-5
rows change OUTCOME STATE** under the forbidden `date(ts) ≤ date(τ)` form — **four numbers, both bounds
× both populations.** **Arm A reports episodes ADMITTED, not outcomes; arm B reports outcomes, on the
wrong set.** A never-started row with an episode in `[τ1, τ1+24h)` **flips to started**; a
started-and-left row with one in `[τ2, τ2+24h)` **can flip to Continued**. **Arm A already holds the 311
and 136 row masks.**

**What IS established, both arms, both populations: exactly 1 episode falls AT `τ1`**, so `0068`'s
strictness ruling moves a real row in `|A|`. **Instance B's THREE-STATE framing is adopted as a
framing** — empty boundary, occupied-and-inert, occupied-and-deciding — **but WHICH state obtains is
NOT yet measured, and this entry's "the measured state is occupied and inert" is WITHDRAWN.**

**(b) `747,478` was mischaracterised.** `0088` §2 called it *undeduplicated season-coverage rows*. **It
is distinct `(user, show)` pairs**; arm A's undeduplicated row count is **1,217,122**. **The label was
taken from the previous artifact's own `user_show_coverage_rows_undeduplicated` key — which was itself
part of what F2 flagged as mislabelled.** **The ruling's conclusion is unaffected and is implemented;
the axis it named was wrong.** *(Both arms' row objects are also measured over different masks — arm B's
1,007,729 is over the D11-filtered S1/S2 slice — **so the row counts are not comparable without the mask
named**, which arm B states at the point of use.)*

**(c) §3 named a third-place cluster that is not determined.** `secondchance` (8) and `theisland` (7)
are unique at their counts and **both arms reproduce them exactly.** **Third place is a SIX-WAY TIE at
6** — `blackout`, `hunted`, `maigret`, `missing`, `thefamily`, `yourhonor`. **`0088` §3 named `maigret`;
neither arm picked it**, and one publishes `blackout` under ascending-key-after-descending-count.
**Both arms reported this independently.** **A spec gap inside the ruling that closed a spec gap.**

## 3. Propagation and staleness, all reported by the arms

| | Fixed |
| :--- | :--- |
| **The assertion set is NINE and no surface said nine** | `0088` §1(c) promoted the ninth; `task-sheet.md` and both agent files still read *"EIGHT MEMBERS"*. **The negative grep passed clean — this is the POSITIVE half's catch**, which is why that half exists. Now **NINE: six pure code checks, one code-by-construction, two data** |
| **`task-sheet.md`'s pre-`0076` count** | *"four pure code checks…"* — the SIX-member reading `0076` corrected to five-of-six, **contradicted 280 lines lower in the same file.** Struck |
| **The superseded universe framing sat BELOW its replacement** | `0088` §3's bullet was filed above the older `5a`/`5` bullets **still reading "no universe is ruled here."** The shape `0067`, `0076` and `0083` §3a each fixed elsewhere. Marked at the point of use, all three surfaces |
| **`specs/step8-readback.md:3`** | *"Step 8 … has not launched"* — **fourth occurrence**, and the first three were stamped while **this source was missed**: `0086` §3 stamped the two artifacts generated *from* it. **Stamped, negative only** |

**Also corrected: `0087` §2's "62 apart" reading.** Instance A measured it — **U1 minus the coverage
pivot is 62 within that arm alone.** It was never a two-arm difference. **On U1 both arms now name one
object**, which is what `0088` §3 was for.

**And a genuine one-pair divergence the totals had hidden.** Arm A's D9 candidate split is
`435,642 + 8,834 + 281,626 = 726,102`; arm B's is `435,643 + 8,834 + 281,626 = 726,103`. **Two classes
agree exactly; the S1-only class differs by 1.** **No entry records it, because the totals had been read
as differing by the whole S3-only gap.** **Reported, not reconciled.**

## 4. Carried for the Human Lead — two items

| # | Item | Why it is yours |
| :-- | :--- | :--- |
| **1** | **The D9 tie-break.** Six keys tie at 6 and the arms publish different third places, both correct under their own rule. Options: rank ties by a named tie-break (ascending key is what one arm uses), publish **all six tied keys** rather than a third place, or state that ranks below the last unique count are not reported | **A ruling, not a measurement.** Every key at every rank already publishes under both bases, so nothing is lost while it is open |
| **2** | **Whether `specs/` becomes a NINTH propagation surface.** It holds the written specs handed to isolated instances, **nothing checks it**, and it has now carried a superseded claim through four occurrences | Red Team's F5. **The stamp is applied; the surface question is a `CLAUDE.md` change** |

## 5. Scope

- **No rule change, no population change, no bound endpoint moves.** **No published figure moves** —
  the `action_count_s1_*` correction touches 4 rows in the APPLY position-5 set and changes no waterfall
  line, outcome share or invariant.
- **Surfaces reached: 1** (`task-sheet.md`) and **4–5** (both agent files, identically). **6** — one
  stamp on `specs/step8-readback.md`, which is **not** currently a surface and is flagged as such.
- **Zero API calls.**
- **Step 8 goes to Red Team for a FIFTH pass, with both §4 items declared open in the brief.**
