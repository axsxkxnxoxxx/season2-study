# Decision 0044 — "No free parameter" is withdrawn; the liveness rule is fully determined by `W`; the rule is propagated to the files Step 8 reads

| | |
| :--- | :--- |
| **Decision** | **`0042` §1's "no free parameter" is WITHDRAWN.** The rule has **no parameter of its own** and is **fully determined by `W`** — its exclusion set runs **348 → 949 pairs** across the mandated Step 13 arms. **Step 13 reports the exclusion count per arm.** The liveness rule is **propagated into both `analytics-engineer` files**, and Step 13's threshold-refit instruction is **withdrawn**. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | Red Team's Step 7 gate review, blocking items 3 and 4 |
| **Amends** | `decisions/0042` §1; `decisions/0038` §6; `task-sheet.md` Steps 7 and 13; all four pipeline agent definitions |
| **Status** | Closed. **The Step 7 gate remains OPEN** — Red Team's item 2 is with both arms and unruled. |

---

## 1. "No free parameter" is withdrawn

`0042` §1 claimed: **"There is no threshold and no free parameter."** Red Team's finding:

> Deleting the threshold did not decouple anything — **it made the coupling total.** PF-LIMIT's
> exclusion set is the open-ended bucket, and that bucket is a pure function of `W`.

Measured by both arms, across the mandated Step 13 arms:

| `W` | 38 | 60 | 91 | **108** | 150 | 213 |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| **Exclusions** | 348 | 432 | 706 | **751** | 779 | **949** |

**A factor of 2.7.** Under the old rule `W` and the threshold were two coupled parameters; **under
PF-LIMIT there is one, and it is `W`** — which is itself **±18 days, show-clustered, `[89, 125]`**, and
whose 90th percentile was "imported from attribution-window practice, not selected by the data."

**And `W` was held at 108 for the entire sensitivity test that justified the deletion.** Instance B
stated this plainly in its own deliverable: *"It does not test sensitivity to `W`. `W` is held at 108
throughout."*

### 1.1 What the study actually did, stated so it is on the record

**The study deleted a parameter it had varied — 787 to 2,200 days — and handed the rule's entire
authority to a parameter it had not varied in the same test.**

That is the generalisable worry Red Team was asked about, and the answer is that **it has already
bitten here.** `0042` §1's claim was true only in a narrow accounting sense: the rule has no parameter
*of its own*. **Publishing "the liveness rule has no free parameter" without "its exclusion set ranges
348 to 949 pairs across the tested `W` arms" would misdescribe the rule to a reader.**

**The honest wording, now in every file: "no parameter of its own; fully determined by `W`."**

### 1.2 Step 13 reports the exclusion count per arm

So the coupling is visible in the output rather than only in this entry.

## 2. Step 13's refit instruction had no referent, and `0038` §6 is withdrawn with it

`task-sheet.md` Step 13 still ordered: *"**Vary the liveness threshold — and REFIT IT PER `W` ARM**"*,
with the 408 → 576 day figures. **There is no threshold to vary or refit.** `0042` deleted it and
nothing withdrew the requirement that depended on it — **a data-scientist instance would have tried to
execute it.**

**`0038` §6's refit requirement is withdrawn.** It is replaced by the per-arm exclusion count above,
which measures the same coupling on the rule that actually exists.

## 3. Propagation failure #6 — the rule was in neither file the Step 8 instances read first

**Checked across all five surfaces after `0042`:**

| Surface | Carried the rule? |
| :--- | :--- |
| `task-sheet.md` Step 7 | Yes |
| `data-scientist.md`, `data-scientist-b.md` | Yes |
| **`analytics-engineer.md`, `analytics-engineer-b.md`** | **No — no Step 7 bullet at all** |

**Those are the first files the two Step 8 instances read, and Step 8 is the step that *applies*
liveness, at filter position 6.** They carried a Step 5 bullet and a Step 8 bullet and nothing between;
the only mention of liveness was the word itself in the filter-order chain.

**This is the same shape as misses #1 and #2** in `0041` §5's table — *"ten decisions propagated to
`task-sheet.md`, none to `.claude/agents/`"* — **on the gate that launches next.**

**Both `analytics-engineer` files now carry the rule**, byte-identical apart from the `name:` field:
the biconditional, insertion time not claimed `watched_at`, the stored calibration never refitted, the
pair-level scope, the twice-withdrawn pre-`τ1` prohibition, the `W`-coupling with its 348–949 range,
and the fact that **the gate is open and Step 8 does not launch until it closes.**

### 3.1 Why item 46's countermeasure did not hold

Item 46 required that *"a ruling is not propagated until it is in every file an agent reads, and the
entry names which files those are."* **`0042` named none.** The obligation was recorded and then not
executed at the first opportunity.

**Sharpened, and this is the version that goes into practice: the propagation surface is five files —
`task-sheet.md` and the four pipeline agent definitions — and an entry that changes a rule must state
which of the five it touched and which it deliberately did not.** A ruling that names no files has not
been propagated, whatever the entry says.

## 4. What remains open

**Red Team's item 2 — that the not-live branch has no stated warrant — is not ruled here.** `0021`
licenses *"insertion after `τ1` → live"*, a **sufficient condition**, not the biconditional PF-LIMIT
adopts, and `0040` §3 arguably withdrew the only argument that covered the excluded set.

**Red Team's alternative rule — not live iff no insertion after `τ1` AND `|A| = 0` — has been put to
both `data-scientist` arms independently**, with its own stated obstacle: it conditions the population
on the outcome, and the approved filter order puts liveness at position 6 before outcome assignment at
7. **Neither arm sees the other's answer.** The Human Lead rules after both report.

**The Step 7 gate stays open. Step 8 does not launch.**

## 5. Scope

- **No population, threshold or result changes.** One published claim is withdrawn, one instruction
  withdrawn, one added, and the rule propagated to two files that lacked it.
- **Zero API calls.**
