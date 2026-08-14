# Decision 0073 — the censoring comparator is corrected; ruling 4's propagation is completed

| | |
| :--- | :--- |
| **Decision** | **The pre-2020 censoring comparator is 3.0%, not 2.7%** — `0070` moved the 2023–2025 figure to the mandated order and left its comparator on the superseded one, so **one sentence carried two orders.** **`0070` ruling 4 is completed:** three surfaces still required the `action` column it replaced, including a head bullet that contradicted the ruling **further down its own section.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 dual run. **Both instances found the comparator independently**; instance A found the three surviving `action`-column requirements |
| **Status** | Closed. **Step 8's two proposals stand unadopted; the gate is the Human Lead's.** |

---

## 1. The comparator — a correction that moved half a sentence

`0070` ruling 8 kept the mandated filter order and restated the cohort loss **10.3% → 10.5%**. **It did
not restate the figure that loss is compared against.** The sentence read *"the 2023–2025 cohort loses
**10.5%** of its pairs against **2.7%** for pre-2020"* — **the first figure on the position-4 output the
order mandates, the second on the position-3 output it supersedes.**

**On the mandated order the pre-2020 loss is 3.0%.** Corrected in **three places**: `task-sheet.md`
Step 8's per-air-period bullet, Step 14's cohort-asymmetry bullet, and — **marked rather than
rewritten**, because it is an approved gate deliverable — the same sentence in
`artifacts/step1-outcome-definition.md`, which carries the original 10.3 / 2.7 pair.

**Both Step 8 instances found this independently, which is what a dual run is for.** It is also the
narrowest instance yet of the error class this chain keeps hitting: **a correction that reaches the
figure it was aimed at and not the figure standing beside it.**

## 2. Ruling 4 — completed, and it contradicted itself in one file

`0070` ruling 4 replaced the row-level `action` column with **per-pair counts by action type**, on the
ground Step 1 §2.3 had already established: **`action` is a property of the LOGGING CLIENT, not of the
viewing**, so it is not an outcome variable. `0070` §5 recorded the ruling as reaching Step 8 and the
two `analytics-engineer` files. **That was true and incomplete.**

| Surface | Still required the column | Now |
| :--- | :--- | :--- |
| `task-sheet.md` **Step 13** | *"Requires the `action` column retained at Step 8"* | struck; **the arm reads the counts** — `checkin`-only iff its `checkin` count is positive and `scrobble` and `watch` are zero, manual-`watch`-only likewise. **The arm is unchanged; only what it reads is** |
| both **`analytics-engineer`** head bullets | *"retain `action` as a column, Step 13 has an arm that needs it"* | struck — **this bullet contradicted ruling 4 further down its own section**, which is the shape `0067` fixed at `task-sheet.md:258` and `0061` fixed in the generator |
| `artifacts/step1-outcome-definition.md` **§9 hand-off list** | *"retention of `action` as a column"* | **marked, not rewritten** — it is an approved gate deliverable. The note cites **§2.3 of the same document** as the ground, since that is where the reason already lived |

**Instance A found all three**, including the contradiction inside its own definition file, and **emitted
counts by type plus S2-evidence composition anyway** — reporting the defect rather than following it.
**That is the read-back discipline working at execution time.**

## 3. What this does not touch

- **Neither Step 8 proposal is adopted.** Step 8 is a gate; the two instances produced and stopped, and
  **approval is the Human Lead's alone.**
- **The four divergences stand unreconciled**, per `CLAUDE.md`: the **table grain** (A 195,951 × 86 at
  position 7; B 196,654 × 87 at position 5 with `live` and `outcome` as columns, **every count
  identical**); **7 invariants against 6**; **6,065,704 against 6,065,610** records examined by the
  set-membership rule, both reporting **0 drops**; and the shape of the `action` counts.
- **The open items both instances raised are untouched** — D9's unspecified title normalisation, which
  makes half (a) **6 or 0**; D3′'s cleared shares, which both measure at **99.53% → 97.73%** against the
  spec's 95.98% → 91.34%; D9 half (b)'s unwritten precondition; the `W` arm grid; and
  `processed/step5/adopted_rule.json`, which still carries revision-3 figures on a surface **no control
  covers.**

## 4. Scope

- **Two corrections. No figure the study publishes moves** — the comparator is a diagnostic, and ruling
  4 changes what is emitted, not what is measured.
- **`analytics-engineer` pair verified byte-identical apart from `name:`.**
- **Zero API calls.**
