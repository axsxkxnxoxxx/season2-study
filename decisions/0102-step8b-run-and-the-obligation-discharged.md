# Decision 0102 — Step 8b is run; the `data-scientist` obligation `0066` §6 carried is discharged after 35 entries

| | |
| :--- | :--- |
| **Decision** | **Step 8b is RUN**, as **arm `a`** — single-arm, and **the spec names no instance, so that was the launcher's choice, recorded in both artifacts.** **Deliverables: `artifacts/step8b-output-schema.json` and `artifacts/step8b-placeholder.json`**, with a validator and a mutation self-test. ***And `0066` §6's carried obligation is DISCHARGED*** — the `data-scientist` pair now carries the duty to write into the schema. **It had gone 35 entries undone**, which is the failure §6 was written to prevent. **Step 8b found a real collision in `0066`'s own amendment 1.** |
| **Recorded by** | Analytics Engineer |
| **Date** | 2026-08-18 |
| **Occasioned by** | The Human Lead: *"Run Step 8b."* Unblocked by `0098`, gate 5 of 5 |
| **Amends** | `0066` §9 (*"Nothing is launched"*) and `0066` §6 (the carried obligation), and **`0066`'s amendment 1** — see §2 |
| **Verified by** | The placeholder **validates against its own schema, 0 failures**; **23 mutations each fail the check they target**; `check_surfaces.py` |
| **Status** | Closed. **Step 9 is NOT begun** — a chained step returns to the Human Lead first. |

---

## 1. The obligation that went 35 entries undone

**`0066` §6 recorded, in terms:** *"When it does, the `data-scientist` files gain the obligation to write
into it — **recorded here so that pass is not forgotten, which is how the covering qualifier went six
entries reaching no agent file.**"*

***The schema now exists, and the pass had not been done.*** **Zero mentions of Step 8b in either
`data-scientist` file**, `0066` to `0101`. **The entry that predicted the failure did not prevent it**,
and it went **six times longer** than the case it cited.

**Discharged now.** Both files carry: the schema's path, the validator to run **before** writing, and
**"NO CONVERSION LAYER"** with the reason — *a conversion layer is a second definition of every figure,
and two definitions of one figure is this study's most frequent defect* (`0058`, `0061`, `0062`).

**They also carry the structural guards, so Steps 9–13 satisfy them rather than work around them**:
never-started's sub-interval accepts **only** the `applicable: false` form; Continued's floor accepts
**only** an absence record; **the three ceilings cannot all hold** and `simultaneous` is `const false`;
**every bound must reference `$.scope_qualifiers`** so the covering qualifier cannot be stripped; and
**every CI must reference `$.bootstrap_settings`**, because the spec fixes neither `B` nor the seed nor
levels-vs-movements, and **an unfixed spec must be visible rather than silent.**

**And the `p_at_bound` hazard reaches them at the point of use**: two required objects, not one — because
**they are different classes and one of them is not empty** (`0099` §2), and **a consumer that provisions
a two-valued column is wrong by 17,895 rows.**

## 2. Step 8b found a real collision in `0066`'s own amendment

**`0066`'s amendment 1 ruled the key is `W` ALONE**, on the correct ground that **there is no liveness
threshold** — one was derived three times and deleted at `0042`.

***That ground holds and the key does not.*** **The `W` grid contains a finale-anchored 91-day arm, and
Step 9 separately requires a 91-day headline anchored on the S2 PREMIERE**, stating plainly that the two
are **not the same measurement at two window lengths**. **Under a `W`-only key those two entries
collide.**

**The key is `(W_days, clock_origin)`.** **The amendment's point is preserved** — no liveness parameter
enters the key, and **`632` and `1,293` appear nowhere in either artifact**, verified.

## 3. What was checked rather than asserted

- **The placeholder validates against the identical schema**: 19 of 21 checks pass, **2 are N/A on a
  placeholder and are reported as N/A with the site count they would have examined**, not as passes.
- **23 mutations each fail the check they target.** The self-test proves the checks *can* fail — the
  distinction this chain got wrong at `0089` §1 and has had to keep re-earning.
- **No study figure is hard-coded.** `196,654`, `147,370`, `6.2055`, `703`, `604`, `1,355`, `17,895`,
  `100.7104` — **zero hits in both files**, verified. **The `W` grid is parsed out of `task-sheet.md` at
  run time rather than typed.**
- **The placeholder is unmistakable as one**: a top-level `placeholder: true`, 2,558 sentinel measurement
  slots and 908 prefixed writer-text slots, **enforced in BOTH directions** — a sentinel or a leftover
  prefix in a file flagged as real data **fails**. `0066` §5: *a placeholder that reads as data is the
  failure mode, and it reaches Step 16.*

**Arm `a` applied `0096` ruling 1 to its own deliverable**: `check_surfaces.py`'s result was **reported
to the Human Lead and written to `logs/`, not published in `artifacts/`.**

## 4. Two limits of its own control, recorded by the arm

- **The validator implements a SUBSET of JSON Schema**, and **nothing independent cross-checks it** —
  `jsonschema` is unavailable and installing it needs the network.
- **The derived-figure and waterfall arithmetic checks cannot run on a placeholder.** They report **N/A
  with the site count they would have examined**, and are exercised only against a de-sentinelled copy
  in the self-test.

**Both are stated in `$.known_limits_of_this_schema` in the deliverable itself**, which is what `0096`
§1 still requires: **an arm's own limits are exactly what it must publish.**

## 5. Scope

- **Surfaces reached: 2–3** (the `data-scientist` pair, §1's obligation), **4–5** (Step 8b's status),
  and **6** (the two new artifacts). **`0066` marked at both points.**
- **Zero API calls.** **Step 9 is NOT begun.**
