# Decision 0081 — `silent_at_tau1` is restored; the column set is 88, enumerated

| | |
| :--- | :--- |
| **Decision** | **`silent_at_tau1` returns to the column set: 88 names, enumerated.** It is the only way to recompute the Continued-and-silent count from Step 8's table, and **its input living in a working file is the same shape as `0079`'s drop set.** **`0077`'s superseded "89 columns" is struck** — both instances reported it reading as current one bullet below its replacement. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | `0080` §2's stated loss, and a defect both Step 8 instances reported independently |
| **Status** | Closed. **The set is 88. A rerun on 88 is not launched here.** |

---

## 1. Why the column comes back

`0080` ruled 87 and **stated the loss at the point of use rather than burying it.** The loss is real:

**`silent_at_tau1` is not recoverable from `live` and `outcome` on Continued rows.** The liveness rule's
second conjunct is `NOT Continued`, so **`live` is true for every Continued pair regardless of
silence.** **Dropping the column means the Continued-and-silent count cannot be recomputed from Step 8's
table.**

**That count is 652** — the size of the outcome-conditioning, **the figure that closed Red Team's rule
objection at `0063` §1**, and a published Step 14 limitation.

**And the decisive argument is one this chain already made.** Its input living in **Step 7's working
files** rather than in Step 8's table is **exactly the shape of B5**: D9 half (b)'s input living in a
helper script's side file rather than in a deliverable. **`0079` ruled that a required input must not
live in a working file. Same argument, same fix.**

**The two free drops stand:** **`f2_in_A_H`** is derivable — `max_episode_in_A_H == s2_F` — and
**`max_episode_in_A`** is read by nothing downstream.

**All 88 names are enumerated** in `task-sheet.md` Step 8 and both `analytics-engineer` files, and the
lists are **verified identical to the ruling and to each other.**

## 2. The superseded count, struck — reported by both instances

**`task-sheet.md` carried `0080`'s enumeration and, one bullet later, `0077`'s *"The table is 89
columns."*** **Both Step 8 instances reported it independently**, and both resolved it the same way and
said why: `0080` is later, explicit, and self-consistent.

**Instance B named the consequence exactly:** *"an instance reading the two bullets in the other order
emits 89, and the dual diff would show a column divergence that is a spec defect rather than an
implementation one."*

**Instance A found a second copy the first did not mention** — both `analytics-engineer` files carried
the same pair **and additionally still listed `f2_in_A_H` as an adopted name**, which `0080` drops.
**Struck in all three surfaces.**

**This is the shape `0067` fixed at `task-sheet.md:258` and `0076` fixed in the `p` heading**: a
superseded statement left standing beside its replacement, in the file an isolated instance reads cold.
**Third occurrence, and each time it was an agent that found it.**

## 3. What the run on 87 established, and why it was worth letting finish

**The Human Lead ordered the in-flight rerun to complete rather than be killed**, on the ground that it
executes `0078`, `0079` and `0080` for the first time. It did, and **the arms agree on the entire column
SET** — 87 each, set-identical, differing only in emitted order.

**`0078` executed for the first time in the study.** Both arms now stamp a build identity — with input
fingerprints, source hashes and git HEAD — on every count, every waterfall line and every invariant, and
**both correctly kept ruled figures on the build they were ruled on**, which no ruling had specified.

**`0080` §3's coverage hole is closed and disclosed.** It was arm B's, and B closed it and **stated the
gap rather than quietly fixing it**: **19,141 + 177,513 = 196,654** in both arms, with the post-liveness
19,042 kept only as a labelled contrast.

**And A did something the ruling did not require: it emitted 652 as an aggregate** so the figure
survives the column's removal. **That is the loss being mitigated by the arm that lost it**, and it is
why the restoration costs nothing already computed.

## 4. Surfaces

**REACHED:** `task-sheet.md` Step 8 and both `analytics-engineer` files — **the 88-name enumeration and
the struck count**, verified name-by-name against the ruling and each other. **Pair byte-identical apart
from `name:`. All eight surfaces PASS.**

**DELIBERATELY NOT REACHED:** the `data-scientist` pair and Step 8b, for the reason `0080` §4 gives —
**the names reach them through Step 8b's schema, which is the single definition `0066` requires**, and
Step 8b is not yet written.

## 5. Scope

- **No figure moves.** One column returns, one superseded sentence is struck in three places.
- **Both arms' current tables are the superseded 87.** **A rerun on 88 is NOT launched by this entry** —
  the Human Lead's sequence is to diff this run first, close what it raises, and rerun once.
- **Zero API calls. Step 8 is not adopted.**
