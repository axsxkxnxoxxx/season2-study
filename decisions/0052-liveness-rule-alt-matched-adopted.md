# Decision 0052 — ALT-MATCHED is adopted; `0051`'s V7 correction is withdrawn; five further defects fixed

| | |
| :--- | :--- |
| **Decision** | **ALT-MATCHED is ADOPTED** — silence tested at **`τ1`** for the never-started null and at **`τ2`** for the started-and-left null. **`0051`'s V7 correction is WITHDRAWN**: 73.6537% is the Continued ceiling and both arms publish it. **The channel figure is corrected to 52.4%.** Propagation **#12**, the mode line, the 1.5× coupling and the A-vs-B ratio divergence are fixed. **The population mismatch is recorded as a Step 14 limitation.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's **sixth** Step 7 HOLD |
| **Supersedes** | ALT-BROAD (`0048` §1); **`0051` §2 entirely** |
| **Propagated to — all five files** | `task-sheet.md` (Steps 7, 9, 13, 14); `data-scientist.md`; `data-scientist-b.md`; `analytics-engineer.md`; `analytics-engineer-b.md`. **Not touched, checked not assumed:** `red-team.md`, `second-brain.md`, the five `reviewer-*.md` |
| **Status** | Closed. **Step 7 reruns on ALT-MATCHED. The gate is OPEN.** |


> **DATE CORRECTED 2026-08-13.** This entry was written and dated **2026-08-13**, which is tomorrow. Entries `0052` through `0057` all carried it, and the drift began when the session's clock advanced mid-work and the date was carried forward from an earlier entry rather than re-read. **Corrected in place across every surface, with this note, rather than silently rewritten** — the decision log is a public tracked artifact. Found by Red Team on its eleventh review; recorded at `0058` §6.

---

## 1. The adopted rule

> **A pair is NOT LIVE if and only if EITHER:**
> - **`|A| = 0` AND the account shows no insertion instant after `τ1`; OR**
> - **`|A| ≥ 1` AND NOT Continued AND the account shows no insertion instant after `τ2`.**

**Each null is tested at the instant its own outcome is read.** Never-started is read at `τ1`;
started-and-left is read at `τ2`, because the Continued condition it negates is read at `τ2`.

**Why ALT-BROAD was insufficient.** It tested both nulls at `τ1`. Its own warrant — *a pair silent
through `[τ1, τ2)` cannot produce the evidence the Continued test reads, so it is scored "left" by
construction* — **holds identically for a pair silent after `τ1 + ε` for any ε < 91 days.** The failure
mode is continuous in the silence instant and **ALT-BROAD cut it at one end.** ALT-MATCHED cuts it at
the instant that matters for each null.

**Expected effect, to be confirmed by the rerun rather than assumed:** APPLY exclusions **703 → 793**,
the started-and-left component **99 → 189**. **The never-started bound is unchanged** — the additional
90 are started-and-left and enter neither of its endpoints. **DERIV is unmeasured.**

**No new anchor and no new parameter.** Both instants are already computed.

## 2. `0051`'s V7 correction is withdrawn — 73.6537% is the Continued ceiling

`0051` §2 asserted *"73.6537% is on no population."* **It is on 196,654: it is the Continued
ceiling, `(144,140 + 703) / 196,654`.** **Both current deliverables publish it** — `bb-a.md` §5,
`bb-b.md` §4.3 — and both JSONs carry `ceiling_pct: 73.6537…`.

**So the original sum was THREE ceilings, not two, and 16.9704 + 10.0405 + 73.6537 = 100.6646% is
arithmetically right.**

**How the error happened, recorded because it is the point.** `second-brain`'s memory mislabelled the
figure as *"the Continued **floor**"* and concluded it could not be reconstructed. **`0051` adopted that
diagnosis without checking it against the arms' own JSON** — **the exact failure `0046` §0 exists to
prevent, committed in the entry that corrected two other instances of it** — and attributed the number
to Red Team while doing so.

**And the correction was worse than the error.** `task-sheet.md` was left presenting Continued as a
**point**, 73.2962%, with the parenthetical *"no Continued pair is ever excluded."* **That parenthetical
is true and does not license it: Continued has a ceiling precisely because any EXCLUDED pair may in
truth be Continued.** A Step 9 instance reading the corrected line against its own deliverable would
have hit a direct contradiction and **deleted a correct number.**

**Restored, with the mechanism stated.** *(Mechanism refined by `0053`: "counted once in every ceiling"
was too coarse. **Each never-started exclusion appears in ALL THREE ceiling numerators — excess 2 each —
and each started-and-left exclusion in TWO — excess 1 each.** Under ALT-MATCHED that is
`2 × 604 + 189 = 1,397` pairs = **0.7104 pp**, and the three ceilings sum to **100.7104%**.)* **The three
are alternative worst cases over one set, not simultaneous ones.**

## 3. The channel figure is corrected: 52.4%, not 70.3%

`0050` §4 reported **297 pairs** in the channel — 207 never-started + 90 started-and-left — and
concluded ALT-BROAD closed **70.3%** of it.

**That denominator pooled two categories with different coverage.** **The 207 never-started pairs are
not in the gap:** never-started is the null `|A| = 0` read at **`τ1`**, and every one of the 207 **has
an insertion after `τ1`** — its null is exactly what `0021` licenses. **The warrant ALT-BROAD added
implicates only the started-and-left pairs.**

**On the implicated set alone: ALT-BROAD closed 99 of 189 — 52.4%, leaving 47.6% open.** Not 70.3% /
29.7%.

**ALT-MATCHED closes the remaining 90.**

## 4. The floor this fixes, and it would have been the fifth

`0050` §4 recorded that the 90 *"are treated as observed by the new S&L bound"* and did not carry the
consequence. **Taken seriously: if the 90 in truth continued — the case the warrant says cannot be
ruled out — the started-and-left numerator is 18,952 and the floor is **9.6372%** *(corrected from 9.6373% by `0053`; numerator 18,952 confirmed by both arms)*, which is 0.0458 pp
below the published 9.6830%, on a bound 0.3575 pp wide.**

**By `0047` §3's own test that would have been the FIFTH consecutive bound with a non-covering
endpoint — and it is the endpoint `0049` §2 was written to get right.**

**Adopting ALT-MATCHED closes the 90 rather than widening the floor around them**, which is why it is
preferred to the two alternatives Red Team named: moving the floor to 9.6373%, or ruling that the
identified set is defined over excluded pairs only and naming the 90 at publication.

## 5. Propagation #12 — Step 9's two mandated sentences reached one file of three

`0050` §3 says *"Step 9 gains the two-ceilings sentence and the DERIV degeneracy note."* **Both landed
in `task-sheet.md` and in NEITHER `data-scientist` file** — verified by grep returning zero matches
across `.claude/agents/`.

**Step 9 is dual implementation, `CLAUDE.md` sends the agent to its definition file, and both copies
carried the same omission — so the diff structurally could not see it.** That is `0050` §0's own stated
mechanism and `0050`'s own defect #2 repeated one entry later.

**Both files now carry three Step 9 obligations:** the three ceilings, the DERIV degeneracy, and the
population mismatch below.

## 6. The A-versus-B ratio divergence, reconciled: 45% is correct

`bb-a.md` §5 gives the started-and-left bound as **0.47×** the account-clustered sampling width;
`bb-b.md` §3 gives **6%**.

**B computed the ratio on the conditional sub-interval it had itself argued is not the bound** — its
JSON field is `started_and_left_over_SL_exclusions`, `bound_width: 0.0503`, `ratio: 0.0635`. **Under
the adopted bound the ratio is 0.3575 / 0.7922 = 45%**, which is A's figure.

**B's summary understates the systematic range against sampling error by 7.5× and contradicts its own
§4.2.** It went unactioned by `0049`, `0050` and `0051`, **and the gate's own Check line is "dual
implementation diff."** Recorded here as the divergence it is.

**Also recorded, unreconciled and now specified:** the two bootstraps are not diffable — A used
B = 4,000, seed 20260813, on the **movements**; B used 2,000, seed 20260814, on the **levels**. The
spec fixes neither and Step 9 must attach confidence intervals.

## 7. Recorded as a Step 14 limitation: the bounds and the shares are on different populations

**The bounds are on the position-5 population** (196,654 / 147,370); **the published shares are
post-liveness** (195,951 / 147,271).

**On APPLY containment holds by arithmetic accident. On DERIV it fails outright: the published
never-started share is **6.2134%** under ALT-MATCHED *(this entry said 6.2096%, which is ALT-BROAD's — corrected by `0053`)* and the published bound is [6.2055%, 6.2055%] — the point estimate lies
outside its own identified set.** Both arms printed these within two pages of each other and neither
said they were on different populations.

`0047` §3 fixed endpoint-versus-endpoint and **left estimand-versus-headline open.** This closes it as
a **stated limitation**, not a repair, and requires Step 9 to name which population each bound bounds.

## 8. Two smaller record fixes

- **`task-sheet.md`'s mode line** for the gate under review still cited `0046`, dated 2026-08-13, and
  said *"reruns pending"* when they were complete. Corrected.
- **The "1.5× `W`-coupling" figure** survived in three files. **That is ALT's** (716/485 = 1.48).
  **ALT-BROAD's is 1.61×** (864/537), which `task-sheet.md` already stated correctly at Step 13 — the
  file contradicted itself on the rule's own coupling, one line below the series corrected to fix
  exactly that.

## 9. What Red Team clears, and what stays open as a limitation

**It does not contest the rule statement**, and it names four items as legitimately closable —
already in Step 14: the **biconditional gap**; the **calibration residual tail** and its `W = 108`-only
scope; **arm-wide residual stability**; and the **Step 8 position-6 population reconstruction.**

**`0049` §5 is also corrected here:** it cleared the residual dual-control item calling the arms' tails
*"a property of a bimodal distribution rather than a divergence."* **They do not differ.** Both report
identical fit-family residual percentiles; the 77.5-versus-124.6 that looked like disagreement is
instance A reporting **two different statistics.** **An agreement was logged as a tolerated
disagreement**, in the entry that discharged the residual.

## 10. Scope

- **Rule change.** Both arms rerun on ALT-MATCHED.
- **Zero API calls.**
- **Step 8 does not launch.**
