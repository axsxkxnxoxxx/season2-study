# Decision 0067 — `0064` is propagated; propagation failure #22, in the approval entry itself

| | |
| :--- | :--- |
| **Decision** | **The Step 7 approval is carried into the five files agents read.** `task-sheet.md`'s Step 7 mode line, its **Gate summary** (Steps 5, 6 and 7 all unticked), and all four pipeline agent files said the gate was open. **Two further stale lines fixed:** `task-sheet.md:258`, which blessed the superseded rule's answer inside the bullet withdrawing that rule, and `:96`, which carried the superseded 403 rule. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-13 |
| **Occasioned by** | The Step 8 read-back. **Both `analytics-engineer` instances found it independently**, before Step 8 launched |
| **Status** | Closed. **No judgment items are touched** — the four the read-back raised are the Human Lead's. |

---

## 1. #22, and where it happened

**`0064` approved the gate, `decisions/README.md` was ticked, and the approval reached no file an agent
reads.** `CLAUDE.md`'s own line is *"Recorded only in `decisions/` is not recorded"* — **broken in the
approval entry, which is the one place it most obviously applies.**

| Surface | Said | Now |
| :--- | :--- | :--- |
| `task-sheet.md:229` | *"NOT approved; seven Red Team HOLDs"* | **APPROVED 2026-08-13**, and it was **fifteen** reviews |
| `task-sheet.md` Gate summary | Steps **5, 6 and 7 all unticked** | all three ticked with dates — 5 and 6 were approved **2026-08-12** and had been unticked since |
| both `analytics-engineer` files | *"The gate is OPEN and Step 8 does not launch until it closes"* | approved; **Step 8 is the remaining gate** |
| both `data-scientist` files | *"Reruns pending; NOT approved. The gate is OPEN."* | approved; reruns complete; `0064` reached **neither** file before this |

**The Gate summary had been wrong for two days on Steps 5 and 6**, which no control covers: it is prose
about state, carrying no figure and no withdrawn phrase.

## 2. The 604/0 blessing — found by instance B

`task-sheet.md:258`, **inside the bullet that supersedes ALT**:

> ~~*"A Step 7 instance reporting 0 on DERIV and 604 on APPLY is correct and the two are not a
> divergence."*~~

**Written for ALT. False under the approved rule.** Under ALT-BROAD the answer is **703 on APPLY and 99
on DERIV**, and B's own definition file says 604 means a superseded rule was implemented and that **is**
a divergence. **It blessed the superseded rule's answer inside the sentence withdrawing that rule, in
the file the isolated instances read** — an instance following it would have filed a correct result as
wrong, or a wrong one as correct, and the dual diff would have agreed with it.

## 3. The 403 rule — `task-sheet.md:96`

Still read *"On a 403, hard stop and report."* **`CLAUDE.md` is authoritative on API discipline and
amended that on 2026-08-10**, because the unconditional form would halt an unattended Step 4 pull on a
single private profile. Replaced with the amended rule in full: **classify before acting**; on a user
resource **skip, log, continue**, bounded by **5** consecutive unconfirmed user-403s with no intervening
2xx and **200** in a run, **only a 2xx resets the streak**; not on a user resource, **hard stop**;
**ambiguity resolves strict**; and **a skipped user is `access_denied`, not a user with no history.**

## 4. What this entry does not do

**The four judgment items the read-back raised are the Human Lead's and are untouched:** waterfall
line 1's base population; the D11 question at position 3 (**220,103 against the published 220,107**);
the censoring-order discrepancy (**`0033`'s table reproduces on position-3 output, not on the position-4
output the mandated order requires**); and whether **`processed/` becomes an eighth propagation
surface** — `adopted_rule.json` holds revision-3 figures and no control covers it.

**Both pairs verified byte-identical apart from `name:`. All three controls PASS. Zero API calls.
Step 8 has not launched.**
