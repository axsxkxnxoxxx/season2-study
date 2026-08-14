# Decision 0076 — `p` is a code check, two real data checks are added, D9's keys are defined, and three propagation misses are closed

| | |
| :--- | :--- |
| **Decision** | **The `p` invariant is a CODE CHECK**, on both instances' proof — my `0074` label was wrong. **On the post-`0074` set that made it FIVE of six unfalsifiable with ZERO pure data checks**, so **two genuine data checks are added**: no account dropped wholesale, and no `access_denied` account read as empty. **D9's strict and loose keys are DEFINED in the spec.** `CLAUDE.md`'s two "seven surfaces" instructions and Step 1 §2.3's `action`-column requirement are corrected. **Both arms rerun.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's first Step 8 review — HOLD |
| **Status** | Closed. **Both arms rerun on the amended spec. Step 8 is not adopted.** |

---

## 1. `p` — the label was wrong and the correction inverts the finding

`0074` §2 called it a **DATA CHECK** and argued *"it can fail on real data, which almost nothing else
here can."* **Both instances labelled it a CODE CHECK, with the same proof**, and they are right:
**Started-and-left requires `|A| ≥ 1`, so `m_H` exists**, and **set membership bounds the rank numerator
in `[1, L2]`**. **No data configuration puts `p` outside `(0, 1]`.** It fails only on the withdrawn
raw-ratio form.

**I ruled on a label without checking what the two instances had labelled it** — the same failure as
adopting Red Team's 73.6537% without checking its population at `0051`.

**And it inverts the answer to this gate's own open item.** On the post-`0074` set of six — partition,
monotone, `|D| ≤ L`, `A ⊆ A_H`, clock-start, `p` — the true figure is **FIVE of six unfalsifiable, with
ZERO pure data checks.** The only assertion with force was the clock-start equality, and only via the
independent recomputation. **"Four of six" was published in `0069`, `0070`, `0074`, `task-sheet.md`,
both agent files, both invariant reports and the Red Team brief.** Corrected in every one.

## 2. Two data checks added, because the set had none

**Both can fail on real data, and both are the failure modes this study is built against.**

- **No account is dropped wholesale by the pair-level liveness filter.** Assert that the count of
  accounts holding **both a live and a not-live pair** exceeds zero. **703 pairs from 216 accounts is
  consistent with a pair-level AND an account-level implementation**, and **nothing in the set
  distinguished them.** `CLAUDE.md`: *"One account can be live for one show and not another. Never drop
  a user wholesale."*
- **No `access_denied` or skipped account is read as empty.** Assert that no account recorded
  `access_denied`, over-tolerance or otherwise skipped contributes a pair scored never-started.
  `CLAUDE.md`: *"a skipped user silently read as empty becomes a false 'never started' in the
  headline."* **This one fails in the direction of the result**, which is the worst direction available.

**The set is now eight: five pure code checks, one code-by-construction with force only as specified,
and two that can fail on real data.**

## 3. D9's keys — the ruled key was undefined everywhere an instance can read

`0074` §5 ruled **"use the strict key — no year stripping."** **"Strict" and "loose" existed only inside
instance B's code, which instance A is forbidden to read.** **The ruled key was undefined on every
surface an isolated instance reads, so a re-run against the ruling would have reproduced the
divergence.**

**Both are now defined in `task-sheet.md` and both `analytics-engineer` files:**

- **STRICT:** lowercase the slug, drop every non-alphanumeric character, **strip nothing else** —
  `re.sub(r"[^a-z0-9]", "", slug.lower())`.
- **LOOSE:** remove a **trailing four-digit year** first, then apply strict.
- **Neither strips a trailing digit group of arbitrary length.** That reduces `the-100` to `the` and is
  **a third key** — the one instance A used, unlabelled, which is why it published **76 complementary
  pairs against B's 75**.

**That divergence is REPORTED, NOT RECONCILED**, and it was missing from `0073` §3's list of "the four
divergences" and from `0074` §5, which adopted "loose finds 75" as the run's figure when the arms had
measured 76 and 75.

## 4. Three propagation misses

| Miss | Where | Now |
| :--- | :--- | :--- |
| **`CLAUDE.md` said eight surfaces once and seven twice** | line 49 listed eight; **line 62 — the operative instruction — said "grep all seven"**, and line 127 likewise. **`0074` §6's claim was true of the list and false of the instruction, and the omitted surface was the new one** | both corrected to **eight** |
| **Step 1 §2.3's `action`-column requirement** | live and unmarked at line 306, **while `0073` §2 marked §9's hand-off list and cited §2.3 as "the ground for it"** — its own named error class, in the file it was editing | marked, with §2.3's own argument as the ground |
| **My own edit discipline** | **two of three edit batches this turn never persisted** — the script asserted mid-run and its single write was never reached, so the p label, the two new invariants and the Step 14 restatement silently did not land, while the `analytics-engineer` block did. **The files went out of sync and the grep caught it, not me** | redone with **every assertion evaluated before any mutation**, then read back **and** grepped |

## 5. What is NOT changed

**Red Team's blocker 4 — that no artifact on disk is the object the rulings describe — is answered by
the rerun, not by an edit.** Both arms rerun on the amended spec.

**Its non-blocking findings stand open and are not resolved here:** the 94-record denominator, where it
argues one figure **is** wrong on its face and the predicted gap is 167 rather than 94; A's mislabelled
DERIV waterfall row; **position 4 being common-mode**, so the 196,654 agreement closes `0047` §7 for the
frame join, `L2 = 1`, the S1 walk and censoring **but not for the contamination exclusion**; the
single-arm D11 row check; D3′'s non-monotone step between `W = 91` and `W = 107`; and the unlabelled
populations at N9–N11.

## 6. Scope

- **`task-sheet.md`, both `analytics-engineer` files, `CLAUDE.md`, `artifacts/step1-outcome-definition.md`,
  and `decisions/0069`, `0070`, `0074` amended in place.** Pair byte-identical apart from `name:`; all
  eight surfaces PASS.
- **Not the `data-scientist` pair** — none of this changes what Step 9 receives.
- **Zero API calls in this entry. Step 8 is not adopted.**
