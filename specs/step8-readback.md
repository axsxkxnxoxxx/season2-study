# Step 8 — read-back. State the spec as you read it. **Do not execute.**

**This is not Step 8.** Step 8 is a gate, it is unapproved, and it has not launched. **Nothing in this
task builds a table, filters a row, or writes to `processed/`.**

**What the Human Lead wants** is the specification *as you read it*, before anyone runs it. Step 8 was
written some time ago and a great deal has changed since — a liveness gate approved after fifteen Red
Team reviews, four rule generations, a deleted threshold, a widened bound, and a long chain of
propagation corrections. **The question is whether the text now says what it is supposed to say.**

## Do exactly this

**Read `task-sheet.md` Step 8.** Read whatever else you need to understand it — `CLAUDE.md`, your own
definition file, `decisions/`, Step 1's outcome definition. **Then state, in your own words:**

1. **The filter order.** Enumerate the positions in the order you would apply them. For each, say what
   it removes and what it is applied *to*. **Say explicitly where liveness sits and what it operates
   on.**
2. **The required counts.** List every count, report and diagnostic the step obliges you to produce,
   and where each is written. **For each, say which population or subset it is computed over** — if the
   spec does not say, that is the finding.
3. **The invariants.** List every invariant you are required to assert, and for each say **what would
   have to be true of the data for it to fail**. If an invariant cannot fail on any data — if it is
   true by construction — **say so and say why.**

## Then, and this is the point of the exercise

4. **What in Step 8 is stale, ambiguous, contradictory, or impossible as written?** Be specific: quote
   the line, say what is wrong, and say what you would need in order to proceed. **Include anything that
   is stated in a way you could satisfy two different ways** — that is what a dual implementation
   diverges on.
5. **What does Step 8 require that no longer exists, or exists under another name?** Rules have been
   superseded, adopted, reverted and re-adopted. **If the step names something that has moved, name the
   thing it has moved to and cite where.**
6. **What would you have to decide yourself in order to run this?** Every such decision is a place the
   two instances can differ. **List them. Do not resolve them.**
7. **What does the step NOT ask for that you believe it needs**, given what Step 9 and Step 8b will read
   out of your output?

## Rules

- **DO NOT EXECUTE.** No table, no filters, no API calls, no writes to `processed/`. Reading files and
  reading stored data to check a count is fine; producing the deliverable is not.
- **Do not fix anything.** If Step 8 is wrong, **report it**. Do not edit `task-sheet.md`, any agent
  definition file, or any decision entry.
- **Do not read the other instance's output folder, and do not ask about it.** The Human Lead diffs.
- **Where your own definition file disagrees with `task-sheet.md`, `CLAUDE.md` or `decisions/`, the
  on-disk files win** and the disagreement is itself a finding worth reporting.
- **Every figure states which population produced it, at the point of use.** APPLY and DERIV are
  different populations with different `n`.
- **Uncertainty is the deliverable here.** If you do not know what a line means, say that you do not
  know, rather than choosing a reading and presenting it as the reading.

## Deliverable

Write **`artifacts/step8-readback-<your namespace letter>.md`**, report the path and a two-line summary,
and **stop.**
