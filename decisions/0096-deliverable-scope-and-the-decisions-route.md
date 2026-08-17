# Decision 0096 — a deliverable asserts only what its own arm measured; `decisions/` may carry cross-arm content

| | |
| :--- | :--- |
| **Decision** | **RULING 1: a gate deliverable asserts its own figures, its own inputs and its own limits — and nothing else.** Not the state of other steps, other gates, the other arm, the shared controls, or the study as a whole. **The provenance rule applied to STATEMENTS rather than FIGURES.** **RULING 2: `decisions/` MAY carry cross-arm content** — a ruling must record what each arm found to explain why it was ruled — **but the leak is made EXPLICIT**: both arm files now say so, ***withdrawing `0095` §1's exclusion of "a decision entry."*** |
| **Decided by** | Human Lead |
| **Date** | 2026-08-17 |
| **Occasioned by** | Red Team's **tenth** Step 8 pass: **HOLD**, and its answer to the convergence question — **plateau with an identifiable generator** |
| **Amends** | `0095` §1 (ruling 2); `CLAUDE.md` gains a new section (ruling 1) |
| **Verified by** | `check_surfaces.py`; the `analytics-engineer` pair byte-identical apart from `name:` |
| **Status** | Open. **Step 8 is NOT approved. Both arms rerun against this entry.** |

---

## 1. Ruling 1 — a deliverable asserts only what its own arm measured

**Its own figures, inputs and limits. Nothing else.** **Not** the state of other steps or gates, **not**
the other arm, **not** the shared controls, **not** the study as a whole.

**The ground: an arm cannot know those things.** It measures a surface at one instant and publishes into
a file **that is never re-read against the world**, so **every such claim is expiry-dated from birth.**

**Three consecutive Red Team passes found a stale one, and the tenth found worse than stale**: arm a's
deliverable told its reader that `check_surfaces.py` **exits 1** when it exits 0. **True when the arm
measured it; false by the time it was read.** ***And arm a's behaviour was correct throughout*** — it
reported the failure with its cause named rather than removing a citation to go green. **The defect is
that a control's exit status was publishable in a permanent deliverable at all.**

**This is the `## Derived figures` provenance rule one category up.** A figure without its provenance is
unreadable; **a statement about a surface the arm does not own is unreadable the same way and worse,
because it reads as a finding.**

**Excluded concretely:** control exit statuses (to the Human Lead, and to `logs/`); the disk state of
other surfaces; build-history narration beyond a stamp and a run-record pointer; and **whether any step
or gate is approved, including this one.**

**Still required, because the arm measured them:** its own defects, its own open items, its own
divergences from the spec. **An arm that notices something wrong on a surface it does not own REPORTS it
and does not publish it as a finding.**

**Why this is the ruling that matters most.** Red Team's tenth pass identified the generator: **arm a's
waterfall is 826 lines of which roughly 120 is measurement.** The rest is build history and claims about
other surfaces — **and each build appends more of it.** Review retired about three per pass; the build
added about three. **Two of the tenth pass's three blockers were regenerations of defects the ninth pass
had closed.** This ruling removes the category rather than the instances.

## 2. Ruling 2 — `decisions/` may carry cross-arm content, and the arms are told so

***`0095` §1 forbade cross-arm content reaching an arm "not from a Red Team pass, not from a decision
entry, not from a prior run's report." The decision-entry exclusion is WITHDRAWN.***

**The ground, as given: a ruling has to record what each arm found in order to explain why it was
ruled.** Forbidding cross-arm content in `decisions/` would mean **a ruling cannot cite its own
evidence.**

***And the ruling names what the isolation rule is FOR***, which the earlier form did not: **it exists to
stop the arms COPYING EACH OTHER'S IMPLEMENTATION, not to keep a number the Human Lead has already ruled
on out of reach.**

**So the two routes are distinguished by whether the figure has been ruled:**

| | |
| :--- | :--- |
| **An UNRULED characterisation relayed into a launch instruction** | **FORBIDDEN, unchanged** (`0095` §1). It is a measurement the receiving arm **cannot check**, and it went stale in one build |
| **A RULED figure in a decision entry** | **PERMITTED.** It has already been through the Human Lead's diff — **a spec input, not a peek at the other arm's work** |

**The leak is made EXPLICIT rather than accidental.** **Both `analytics-engineer` files now state that
decision entries may contain cross-arm content**, so an arm reading `decisions/` **knows what it is
reading and is not stumbling into a route around isolation.**

**An arm may cite such content, naming `decisions/` as the source.** **It may NEVER open the other arm's
output folder, and it may NEVER treat a cross-arm figure as something it measured.**

***This resolves Red Team's F1 in the direction it could not choose for itself.*** It correctly found
that `0095` plugged one route and left another open, and that arm a uses the open one seven times — but
**whether that route should be open is a judgement about the study's purpose, not about the text.**
**It is open, deliberately, and now labelled.**

## 3. What Red Team found and this entry does not dispute

**The arithmetic is clean and was re-derived independently** — every waterfall line, both outcome
partitions, the 604/99 split, `p_at_bound` on four populations, the line-6 identities, D2's five
including DERIV's **153**, D11's `94 + 73 = 167`, and D9's `726,102 + 21,376 = 747,478`. **Its words:
"The analysis table is gate-ready as a measurement."** **Third consecutive pass reproducing it to the
row, and no arithmetic defect in either arm across the last three.**

**Carried, not ruled here:** the D9 tie-break; `specs/` and `CLAUDE.md` as candidate propagation
surfaces; the **439** untriaged needle candidates, with Red Team's proposal to **scope the register per
needle to the file set it was authored for and FAIL on that scope** while reporting repo-wide without
failing — *"not narrowing, because the authored scope IS the original scope"*; and `second-brain`'s
R1–R9.

## 4. Scope

- **No population change, no figure moves, no rule change to the measurement.**
- **Surfaces reached: `CLAUDE.md`, 1, 4–5.** **6 and 8 PENDING BOTH ARMS** — stated per `0093`.
- **Zero API calls.**
