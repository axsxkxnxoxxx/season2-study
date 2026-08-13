# Decision 0037 — `0036` §1's basis is withdrawn; the gap unit is fixed; the namespace mechanism is fixed

| | |
| :--- | :--- |
| **Decision** | **`0036` §1's "one in a hundred" basis is WITHDRAWN.** The reference distribution becomes the **bracketing-gap distribution itself**. **`0036` §2 — the rule's shape — stands unchanged.** The gap unit is fixed at **distinct insertion instants** with an exact collapse rule. Instance namespaces are **assigned explicitly in the prompt** from Step 8 onward. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Amends** | `decisions/0036` §1; `task-sheet.md` Step 7; `.claude/agents/data-scientist.md` and `data-scientist-b.md`, identically |
| **Occasioned by** | The Step 7 dual run of 2026-08-13. Both arms found the §1 defect **independently and in the same terms** |
| **Status** | Closed. **Step 7 reruns as a dual pair.** |

---

## 1. `0036` §1's basis is withdrawn — the reference distribution and the test statistic were different objects

**What §1 said:** *"At the 95th, one ordinary gap in twenty trips the threshold; at the 99th it is one
in a hundred."*

**That is true of a uniformly drawn gap and false of the gap this rule tests.** The threshold was a
percentile of the **pooled** gap distribution, while §2's rule selects the gap **bracketing `τ1`**.
**The bracketing gap is length-biased:** a gap of length `L` covers `L` of calendar time, so the
probability that a fixed instant falls inside it is proportional to `L`. Long gaps are therefore
massively over-represented among bracketing gaps — the inspection paradox.

**Measured, by both arms independently and in agreement:**

| | Pooled | Bracketing |
| :--- | ---: | ---: |
| Median gap | 0.0000006 d | **2.01 d** |
| 75th percentile | — | 9.03 d |
| **Share exceeding the pooled-99th threshold** | 1% by construction | **37.4%** |

**Raising the percentile does not repair it** — the 99.9th still fails 27% of measured-gap pairs. The
defect is that the calibration was performed on one distribution and applied to another.

**Instance A's formulation is the precise one and is adopted into the record:** *"the reference
distribution and the test statistic are not the same object."*

**The correction:** take the percentile **on the bracketing-gap distribution itself**, so the stated
rate is the rate the rule delivers. Both instances propose the threshold it yields; **neither adopts
it.**

**The percentile remains the 99th** unless the Human Lead rules otherwise on seeing the corrected
distribution. `0036` §1's *conservative-direction* argument is untouched by this: a false-dead removes
a pair, and the liveness exclusion already biases the never-started share **down** (Step 14, bias 2).
It was the "one in a hundred" arithmetic that failed, not the direction.

### 1.1 What is NOT withdrawn

**`0036` §2 — the rule's shape — stands in full.** The test applies to the gap bracketing `τ1`, not to
every gap in the sweep, and both arms corroborated the reason. **The whole-sweep alternative is worse,
not better**, and §1's failure is not an argument for returning to it.

## 2. The shape argument was understated by two orders of magnitude

`0036` §2.1 illustrated the compounding with accounts of 10 to 100 gaps, giving 9.6% and 63.4%.

**The median account in this data has 8,247 gaps.** At that count a whole-sweep test at the 99th
percentile trips with probability **≈ 1**. The compounding is not a tail risk to be weighed against
the rule's benefits; on this data it is a certainty for a typical account.

**Recorded as a strengthening of `0036` §2, not a correction to it.** Found by instance A.

## 3. The 38,696 "no instant at or before `τ1`" bucket is a clock mismatch, not absent users

`0036` §2.3 rules these pairs **not live**, and both arms applied that unchanged. **What they are is
not what the rule's name suggests.**

**`T0` is built from claimed `watched_at`; liveness runs on insertion time** (`0021`). The two clocks
are not the same, and for old shows they are far apart. In this bucket:

- the **median pair's `τ1` falls 1,578 days before the account's first-ever insertion instant**;
- **8,037 pairs have `τ1` before the calibration curve even starts.**

**These are not users who were absent. They are pairs whose window closed before the account existed
on the insertion clock.** The bucket is 19.17% of the 201,900 population; it falls to 1,038 in the
128,099 clean sample and to 18,250 once contaminated `T0` is excluded, so it is dominated by early or
corrupt `T0` — **but it is not empty in the clean sample.**

**Recorded, not repaired.** Repairing it means reconciling two clocks that `0021` deliberately
separated, which is a larger question than Step 7. **It routes to Step 14** as a limitation with its
mechanism named. Found by instance A.

## 4. The gap unit is fixed — this ambiguity produced a real divergence

The two arms diverged on the distinct-instants sensitivity variant: **A read 3.4432 d → 4 days, B read
6.03 d → 7 days.** Both were faithful to `0029`'s wording, which is the defect — **a spec that admits
two faithful readings four days apart is not a spec.**

> **The operation, stated so two instances cannot read it differently.** For each account, take the
> insertion instant of **every** record in its sweep; **sort ascending**; **collapse runs of EXACTLY
> equal instants to a single instant** — exact equality only, **no rounding, no bucketing to any
> resolution, no per-day or per-second collapse**; then take the **consecutive differences** of that
> sorted distinct sequence. Each difference is one gap.

**What this is not.** It is **not** one gap per consecutive pair of *records* — that reading
double-counts a batch insert as many near-zero gaps, and it is why 59.3% of pooled gaps were sub-second
in the first run. It is **not** a dedupe at any rounded resolution, because the resolution would be
unstated and therefore unreproducible.

**A sub-second gap between two genuinely distinct instants is a real gap and is retained.** Only exact
ties collapse.

## 5. The namespace mechanism is fixed

**Both instances wrote to letter `a` and collided.** The launch prompt said *"your letter is `a` if you
are `data-scientist`, `b` if you are `data-scientist-b`"* — **an agent cannot reliably determine its own
name from inside**, and `0035` had just made the two definition files byte-identical apart from
`name:` **by design**, so the letter was not derivable from the file either.

**From now on the namespace is assigned explicitly in each instance's prompt.** This is the one
permitted difference between two otherwise byte-identical dual-run prompts, and it must be the only
one.

**This run's numbers are accepted.** Both arms detected the collision, vacated the shared names, and
regenerated end-to-end in isolated directories, and **every published number agreed exactly** — which
is evidence the isolation held where it mattered. The artifacts are relabelled to their true producers:
instance B's now carry `-b`, and two orphaned scripts from B's pre-vacate phase are marked as such.

## 6. Scope

- **No approved threshold exists.** Step 7 remains an unapproved gate; the 4-day figure is superseded
  as a *basis* even though it may survive as a *number*.
- **Zero API calls**, then and on the rerun.
- Step 8 does not launch until Step 7 is approved.
