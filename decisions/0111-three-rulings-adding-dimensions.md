# Decision 0111 — E1, E2, E6: three rulings, all of them adding a dimension rather than restricting a use

| | |
| :--- | :--- |
| **Decision** | ***E1: Step 13's SIX non-headline outputs take PER-ARM NESTING, the same shape as its headline. THIRD appearance of one defect; the same widening both prior instances took.*** ***E2: an arm entry's identity includes its PRODUCING STEP — the key is `(W_days, clock_origin, producing_step)`. NOT resolved by restricting which step may occupy a shared `W`.*** ***E6: the merge's input list records SOURCES, not only arm files; Step 14's `limitations` is a named non-arm-file source with its own provenance entry.*** |
| **Decided by** | **Human Lead** |
| **Date** | 2026-08-18 |
| **Occasioned by** | `reviewer-engineering`'s third Step 8b review: **not clear for Step 13b** |
| **Status** | Open. **The agent-fixable set goes to the arm. Step 9 blocked by levels-vs-movements, which remains the Human Lead's.** |

---

## 1. One rule behind all three: widening, never restricting

***Every one of these adds a dimension rather than forbidding a use***, and the constant is `0107` §3:
**one slot where two arms write forces the reconciliation the spec forbids.**

**E1 is the THIRD appearance of that defect.** `0107` §4: *a dual step's arm file had no legal shape at
all.* `0109`: §1's reading would have **duplicated** one figure into two files. **Now: a dual step's
non-headline output has no legal MERGED shape.** ***Each time the fix was widening, and each time
widening kept ONE DEFINITION PER FIGURE*** — which is why the same fix applies without argument.

**E2 is the `(W_days, clock_origin)` collision ONE DIMENSION OUT.** `0102` added `clock_origin` because
a finale-anchored and a premiere-anchored 91-day arm are different measurements colliding under a
`W`-only key. ***Step 9's `W = 108` and Step 13's `W = 108` are the same shape of collision one level
further out: different measurements of one setting.*** **Same fix: add the missing identity dimension.**

***And the ruling names what NOT to do***: **do not resolve it by restricting which step may occupy a
shared `W` value.** **That would make the schema decide an ownership question the spec does not**, and
would drop a measurement rather than hold it.

## 2. E6 — the input list records sources

**`0109` moved Step 13b after Step 14 precisely so `limitations` could be filled.** **Step 14 delivers a
limits section, not a schema file**, so it is **not one of the seven** and had **no way to be recorded.**

***A ten-item bias ledger that MUST NOT BE NETTED cannot arrive in the reader-facing document with no
recorded provenance.*** **It is an eighth source, it has no arm, and it gets its own provenance entry.**

## 3. To the arm — each reproduced before fixed, the fix demonstrated against the reproduced file

***The Human Lead's standing method, and it is what made M1 checkable***: reproduce, then fix, then
demonstrate the fix rejects exactly the reproduced file.

- **The Q1 duplication.** **Step 11's placeholder writes `action_type_counts`, which its own ownership
  table marks `published_by_step: step9`, `may_first_writer_fill: false`** — ***the exact duplication
  `0109` §1 chose §6 to prevent, shipped in the file Step 11's writer will copy.*** **Fix the
  placeholder AND add the missing control**: a **presence** check failing a file that carries a block
  its own ownership table assigns to another step. ***Only absences are policed today, and that
  asymmetry is what let this ship*** — the file is checked for writing too little and never for writing
  too much.
- **E3b.** **`S30` checks payload → input and never input → payload.** **A merge dropping an entire
  declared input validates clean** — ***occupied by the shipped placeholder***, which declares
  `(step12, sole)` as input #7 while **zero payloads name a step12 file.** **M1 inverted: one file
  supplying two arms was caught, one file supplying nothing is not, and it needs no forgery — only an
  omission.**
- **E4.** **`S22` reads `ownership_map` out of the file under test**, so **any arm file can exempt
  itself by editing one string.** ***`S31` already records why that cannot work*** — *"a table read from
  the file under test could only agree with itself"* — **and that reasoning was not carried across.**
  **Carry the external-table mechanism over, covering `d3_prime` and `retained_by_air_period`, which
  have no backstop.**

## 4. The M1 residual, corrected

***The published limit bounds the rung the selftest pins, not the rung above it.*** **`S30` normalises
five keys and not `convention_definition`** — arm a's convention in arm a's words — **and a forger making
the copy internally coherent rewrites that sentence anyway.** **The moment they do, the identical-payload
signal inverts to `0 of N`, which is what a GENUINE merge produces.**

**Publish the corrected residual**: ***`S30` raises the cost of a false merge to a fabricated input file
plus one rewritten sentence, and past that there is no in-file signal at all.*** **Say where the limit is
published that THE DIFF REMAINS THE CONTROL past that rung.**

***An understated limit in the file Step 16 renders from is the kind of false statement `0109` exists to
prevent*** — the same reasoning that moved Step 13b rather than allowing `limitations: []`.

## 5. Scope

- **Surfaces reached: 1** (`task-sheet.md` — Step 8b and Step 13b) and **4–5** (both
  `analytics-engineer` files, identically). **The schema, validator and placeholders are the arm's.**
- **Zero API calls. Step 9 NOT begun.** ***Levels-vs-movements remains open and remains the Human
  Lead's.***
