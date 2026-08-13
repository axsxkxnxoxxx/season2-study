# Decision 0043 — Step 14's bias 2 has the wrong sign: the liveness exclusion moves never-started UP, not DOWN

| | |
| :--- | :--- |
| **Decision** | **Step 14 bias 2's direction is CORRECTED from DOWN to UP.** The approved liveness rule moves the never-started share **from 6.2055% to 6.2373% — up 0.032 pp** — because it preferentially deletes **confirmed continuers**. **`0042` §4's 0.027 / 0.016 / 0.011 figures are corrected to 0.032 / 0.023 / 0.009.** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's gate review of Step 7, finding 5 (blocking) and finding 1 |
| **Amends** | `task-sheet.md` Step 14 bias 2 and the liveness-inertness item; `decisions/0042` §4 |
| **Status** | Closed. **Step 7's gate remains OPEN** — Red Team's other three blocking items are not addressed here. |

---

## 1. The sign error

`task-sheet.md` Step 14, bias 2, as it stood:

> **2. Liveness exclusion — DOWN.** Excluding pairs that fail the liveness test removes accounts that
> stopped logging, which are disproportionately the ones that would have scored never-started.
> **Compounds with 1** rather than offsetting it.

**Measured on this study's own data, for the approved rule:**

| | Never started |
| :--- | ---: |
| No liveness filter at all | 6.2055% |
| **PF-LIMIT — the approved rule** | **6.2373%** |

**The filter raises the never-started share by 0.032 pp.** The ledger said down. **It is up.**

### 1.1 Why — and the mechanism was in the arms' own artifacts

The rule excludes on **account silence after `τ1`**. But a pair scored **Continued** carries **positive
episode-level evidence that the account was logging in the window** — `F2 ∈ A_H` and
`|A_H| ≥ ceil(0.90 × L2)` — and **later silence cannot corrupt that classification.** There is nothing
for liveness to protect on such a pair, and the rule deletes it anyway.

**Measured composition of the threshold rule's 1,282-pair exclusion set**, of which the approved rule's
**751** are the open-ended subset:

| | Pairs |
| :--- | ---: |
| **Continued** | **1,079** |
| Started and left | 163 |
| Never started | **40** |

**Instance B named it in its own deliverable:** *"the filter is not selecting on the outcome it was
built to protect."* It was reported and not acted on until Red Team made it blocking.

### 1.2 Two consequences the ledger must now carry

**It does not compound with bias 1. It offsets it**, by a trivial amount. The old entry asserted the
opposite, and "compounds" was doing work in the ledger's overall argument.

**Step 9's liveness bound bounds the wrong set.** The bound treats every excluded pair as a decliner.
**Roughly six in seven of the 751 have positive S2 evidence, most of them confirmed continuers.**
Treating a confirmed continuer as a decliner is **not a conservative bound** — it is an arithmetic
operation on a set chosen for a reason unrelated to the uncertainty being bounded. Red Team's
assessment: *"meaningless, not merely uninformative."* **Report it as narrow AND as bounding the wrong
set, or compute it on the ~40 never-started exclusions instead.**

### 1.3 How it survived

**`0040` §3 withdrew this argument once** — for the edge-case branches — **and the withdrawal never
reached `task-sheet.md` line 423.** Bias 2 then became the **sole surviving Step 14 statement about
what the liveness filter does**, with the wrong sign, in the study's central honesty artifact.

## 2. `0042` §4 quoted the deleted rule's numbers

`0042` §4 stated that **the approved rule** moves the shares **0.027 / 0.016 / 0.011 pp** against no
filter. **Those are the 1,293-day threshold row's deltas — the rule that was deleted.**

| Comparison | Never started | Continued | Started and left |
| :--- | ---: | ---: | ---: |
| 1,293 d vs no filter | 0.027 | 0.016 | 0.011 |
| **PF-LIMIT vs no filter — correct** | **0.032** | **0.023** | **0.009** |

**Instance A's sentence said "at 1,293 d" explicitly, and this entry lifted it and changed its subject
to "the approved rule."** Same error class as `0038` §5 and `0039` §2/§6: **a figure measured on one
configuration, quoted as if measured on another.** Sixth instance.

Trivial in magnitude — 0.005 pp — and it is a finding anyway for two reasons Red Team gave: **it erred
in the direction that made the approved rule look more inert on never-started**, the share the study
exists to report; and **it had already propagated verbatim into `task-sheet.md` as an operative Step 14
instruction**, which is the sentence that would have been published about the filter's size.

## 3. What this entry does not do

**Red Team's other three blocking items are open and the Step 7 gate remains open with them:**

- **The not-live branch has no stated warrant.** `0021` licenses *"insertion after `τ1` → live"* — a
  sufficient condition, not the biconditional PF-LIMIT adopts. `task-sheet.md`'s *"this is the ruling
  the whole rule now rests on"* is not true as written.
- **"No free parameter" is not what the evidence shows.** PF-LIMIT's exclusion set ranges **348 → 949
  pairs** across the mandated Step 13 `W` arms, and **`W` was held at 108 throughout the sensitivity
  test.**
- **Propagation failure #6:** neither `analytics-engineer` file states the liveness rule, and they are
  the first files the **Step 8** instances read. `task-sheet.md` still orders Step 13 to *"vary the
  liveness threshold and refit it per `W` arm"* — an instruction with no referent.

**Step 8 does not launch.**

## 4. Scope

- **No population, threshold or rule changes here.** Two published figures and one published direction
  are corrected.
- **Zero API calls.**
