# Season 2 Abandonment Study

Measuring, at the individual level, what share of people who finished a show's season 1 never started season 2 versus started it and quit. Public Trakt watch histories are the data source.

The full specification is in task-sheet.md. Each agent's own steps are written into its definition file. Read the task sheet only when you need context beyond your own steps.

## Human Lead

The Human Lead is the person directing this project. They own Steps 2, 14, 15, 17, and 18, and they approve all five gates.

When a step names the Human Lead as owner, no agent acts on it. Do not draft it, do not prepare it, do not offer a version of it.

## Gates

Five steps are gates: Step 1 outcome definition, Step 5 contamination exclusion rule, Step 6 window W, Step 7 liveness threshold, Step 8 analysis table.

At a gate, the owning agent produces the artifact and stops. It does not adopt its own proposal and it does not begin the next step. Only the Human Lead approves, in writing, in this session.

Nothing downstream of a gate runs until that approval is given. If a step depends on a gate that has not been approved, say so and stop.

An agent never records its own approval.

## Handoff

When an agent finishes a step:

1. Write the deliverable to the folder named in its definition.
2. Report the file path and a two-line summary of what is in it.
3. Stop.

Do not begin the next step. Do not summarize what you would do next.

A chained step still returns to the Human Lead before the next one starts. Chained means no written approval is required, not that steps run back-to-back unattended.

## Dual implementation

Steps 6, 7, 8, and 9 run twice. Steps 6, 7, and 9 use data-scientist and data-scientist-b. Step 8 uses analytics-engineer and analytics-engineer-b.

Both instances receive the same written spec from a file. Never describe the task twice in your own words: a difference in output would then prove nothing.

Neither instance sees the other's work, asks about it, or reads its output folder. The Human Lead diffs the numbers.

Any divergence is either a bug or an ambiguity in the spec. Report it. Do not reconcile it.

## Propagation

A ruling lands in `decisions/` **and** in every file an agent reads. Recorded only in `decisions/` is not recorded.

**There are seven surfaces**, and all seven are checked on every edit:

1. `task-sheet.md`
2. `.claude/agents/data-scientist.md`
3. `.claude/agents/data-scientist-b.md`
4. `.claude/agents/analytics-engineer.md`
5. `.claude/agents/analytics-engineer-b.md`
6. `artifacts/` — deliverables carrying superseded figures are stamped, not left to be read as current
7. `.claude/agent-memory/second-brain/` — it is fed back into rulings, and stale memory has already caused a wrong one

**Read-back plus grep. Read-back alone is not verification.** Human Lead ruling, 2026-08-14. Reading an edit back proves the new text landed. Only grep proves the old text is gone, and a file can hold both at once — three consecutive propagation failures were exactly that, an adopted figure and its superseded predecessor live in the same file, sometimes ten lines apart, each declaring the other wrong.

So after any edit: grep all seven surfaces for the superseded strings and require **zero hits**, except where a string is explicitly named as superseded at the point of use. Report the hit counts.

**And grep the corrected string too, requiring non-zero.** Added 2026-08-14 by the analytics-engineer, who found the negative half insufficient on the first run under it: **a figure that was never written returns zero hits on every superseded form of itself.** The DERIV bound was absent from all five spec files rather than present and stale, so the negative grep passed clean on a file set that contained the defect. A defect has two shapes — the wrong figure present, and the right figure missing — and the negative grep sees only the first.

**A grep hit is not a defect until you read the line.** Several figures in this study are correct on one population or scope and superseded on another, and a check that treats every hit as a defect chases them while a check that dismisses them misses the real ones. The register of known false positives is maintained in `.claude/agent-memory/second-brain/glossary-terms-and-thresholds.md`; the decision entry that adds or withdraws a row cites it.

**Registering a string as a false positive disarms the control against it.** Do it only when the legitimate reading is verified live under the *adopted* rule, and withdraw the row the moment it stops being. `9.6830%` was registered as legitimate and was superseded on four surfaces at the time — the exemption was granted to the one string the control most needed to catch.

## Derived figures

**When a bound endpoint moves, every figure computed from it moves.** Correcting an endpoint and leaving its derived quantities behind has now happened twice in consecutive entries. So each endpoint carries a written list, and **the list is checked as a set whenever that endpoint moves** — not the figure that prompted the correction, the whole set.

**Started-and-left floor** — four derived figures:

1. the **conditional sub-interval** floor (the conditioning constrains the never-started exclusions only, so this floor moves with the bound floor and is never narrower by the channel count)
2. the **attainable-corner table** — the floor corner and the Continued value in that row
3. the **bound ÷ account-clustered sampling width** ratio, per arm
4. the **Continued ceiling**, which moves in lockstep because the conceded pairs land in Continued

**Never-started floor** — three: the attainable-corner table's floor corner and its Continued value; the bound ÷ sampling width ratio; and the Continued ceiling. *(It has no conditional sub-interval — the sub-interval conditions on this bound's own exclusion set.)*

**Any ceiling** — three: the **three-ceiling sum and its excess**, on each population separately; the **excess mechanism** count (`2 × never-started exclusions + started-and-left exclusions`); and the corner table row that attains it.

**Both populations, always.** APPLY and DERIV are separate lists with separate arithmetic, and a correction applied to one and not the other is the same defect as not applying it at all.

**Add a row when a new figure is derived; never remove one.** A list that shrinks is how the next one gets missed.

**The dual diff cannot catch a propagation failure.** Both members of a pair are byte-identical by design, so an error written into both is invisible to it. Propagation is checked by grep, never by the diff.

## API discipline

Losing Trakt access would end this study, so these rules outrank speed.

**Rate limit.** Trakt allows 1000 GET calls per 5 minutes at the application level, which is 200 per minute. Throttle at 150 per minute. Never run at the ceiling.

**Never re-request what is already on disk.**

**On a 429:** read the `Retry-After` header, pause that many seconds, then resume. Never retry the same request in a loop. If 429s persist across several consecutive pauses, stop and report. Log the status, the `X-Ratelimit` object, `Retry-After`, the endpoint, and the method every time.

**On a 403:** classify it before acting. Amended by the Human Lead, 2026-08-10; the earlier rule was "hard stop, always," which would halt an unattended Step 4 pull on a single private profile.

- **On a user resource:** skip that user, log it with full headers, and continue. Bounded by two circuit breakers: **5** consecutive unconfirmed user-403s with no intervening 2xx hard stops, and **200** user-403s in a run hard stops. Only a 2xx resets the streak — a 401 or 404 does not.
- **Not on a user resource** — or on a user resource where `X-Private-User` is present and false-like, or present and unrecognized: **hard stop and report.** That is a block, not a throttle.
- **Ambiguity resolves strict.** A false hard stop costs wall-clock but no API budget and no data, because the client resumes from disk. A false skip risks the study's access.

`X-Private-User` is **positive confirmation only.** It is absent from every captured response on the endpoint family Step 4 uses, so its absence carries no information and must never be read as "not private." The endpoint path is the primary discriminator.

A skipped user is **not** a user with no history. It is recorded as `access_denied` and must stay distinguishable downstream — a skipped user silently read as empty becomes a false "never started" in the headline. Rule and evidence in `artifacts/step0-access-and-setup.md` §7.

**On timeouts, connection errors, and 5xx:** retry with backoff.

**Authentication.** Every endpoint this study uses is OAuth Optional and works with the Client ID alone on public profiles. Do not build an OAuth flow. Private profiles return nothing; log them and move on — Trakt documents 401 for these, but see the 403 rule above, which exists because a private profile may return 403 instead. Dropped status is OAuth Required and unavailable, so the three outcome states are inferred from episode-level history, never from a drop flag.

**The Client ID** lives in .env and is loaded at runtime. It is never written into a code file, a log, or an artifact.

## Where things live

| Folder | Contents | Git |
| :--- | :--- | :--- |
| `artifacts/` | Deliverables. Aggregates and counts only. | Public |
| `decisions/` | Decision log | Public |
| `raw/` | Raw API responses | Never leaves this machine |
| `processed/` | Intermediate tables | Never leaves this machine |
| `logs/` | Run records and errors | Never leaves this machine |

No usernames, user IDs, or individual watch histories in `artifacts/` or `decisions/`. If unsure, write to `processed/` and ask the Human Lead.

Agents do not spawn other agents. Only the Human Lead runs an agent.
