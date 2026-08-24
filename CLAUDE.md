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

Steps 6, 7, 8, 9 **and 13** run twice. Steps 6, 7, 9 and 13 use data-scientist and data-scientist-b. Step 8 uses analytics-engineer and analytics-engineer-b.

***STEP 13 IS DUAL. Human Lead ruling, 2026-08-18 (`0103`), resolving a live conflict between this list and `task-sheet.md`***, which argued the `W` grid must be fixed because *"two instances on different grids produce tables that CANNOT BE DIFFED AT ALL"* — presupposing a duality this list did not grant. **Found by `reviewer-engineering` on the Step 8b review and reported rather than charged to the schema.** **Resolved in favour of dual:** Step 13 varies `W` across eight arms **and the completion rule alongside**, making it **the most spec-heavy step remaining** — and **every divergence in this build has come from an unstated convention in a spec, not from a coding error.**

Both instances receive the same written spec from a file. Never describe the task twice in your own words: a difference in output would then prove nothing.

Neither instance sees the other's work, asks about it, or reads its output folder. The Human Lead diffs the numbers.

Any divergence is either a bug or an ambiguity in the spec. Report it. Do not reconcile it.

## Commit messages never carry cross-arm content

***A COMMIT MESSAGE IS A SURFACE AN ARM CAN READ WHILE PERFECTLY OBEYING THE ISOLATION RULE.***
Recorded 2026-08-24 (`0125` §5d), found by arm `b` reporting it against itself.

An arm ran `git log -- src/step9_b_2_bootstrap.py` — **correctly path-scoped to its own namespace** —
and the message it returned carried **the other arm's exit codes and check counts.** ***PATH-SCOPING
CANNOT PREVENT THAT.*** `0123` scoped the search **pattern**; this scopes **what a properly-scoped
search is allowed to return.** ***A rule that constrains only HOW AN ARM LOOKS cannot reach what the
repository puts in front of it.***

**So: a commit message STATES WHAT CHANGED AND CITES THE DECISION ENTRY.** ***Cross-arm content — one
arm's counts, exit codes, findings or figures — goes in `decisions/`, which passes through the Human
Lead's diff, and NEVER into the log.***

***HISTORY IS NOT REWRITTEN.*** **Messages before 2026-08-24 carry cross-arm content**, and **an arm
that meets it REPORTS RATHER THAN READS.** **Arm `b` did exactly that — it measured the figure itself
rather than adopting the one in the message, and the two did not agree.** ***That is the required
behaviour, not a lapse.***

**This is the same shape as `## Cross-arm characterisations never enter a launch instruction`, one
surface out:** that rule closed the prompt, **this one closes the log.** **Both exist because an arm
is structurally forbidden to re-measure what it is told.**

## Cross-arm characterisations never enter a launch instruction

**`## Dual implementation` says neither instance sees the other's work. A LAUNCH INSTRUCTION IS A WAY
FOR IT TO SEE IT.** Recorded 2026-08-16 (`0095`), found by Red Team's ninth pass.

**Relaying one arm's shape into the other arm's prompt routes around the isolation rule** — and it is
worse than reading the folder, because **the receiving arm is structurally FORBIDDEN from re-measuring
what it was told.** A relayed characterisation is **a measurement with an expiry date that its holder
cannot check**, so it can only go stale. **It went stale in one build**: arm a published a two-way/
three-way falsifiability divergence against arm b, sourced from a Red Team pass relayed in its prompt,
while arm b's current build published **the same 6 + 1 + 2 split** and named exactly which side the
third fell on.

**A fabricated divergence in a gate deliverable is worse than a missed one**: it pre-empts the one
authority permitted to make cross-arm statements — **the Human Lead's diff.**

**So: an arm's launch instruction states the SPEC and the arm's OWN defects. It never states what the
other arm does, publishes, splits, names or reports** — not from a Red Team pass, not from a prior run's
report. **Where a Red Team finding is inherently comparative, the finding goes to the Human Lead and only
the non-comparative half reaches the arm.**

***AMENDED 2026-08-17 (`0096`), Human Lead ruling: `decisions/` MAY carry cross-arm content, and the
earlier form of this rule — which excluded "a decision entry" — is WITHDRAWN.*** **A ruling has to record
what each arm found in order to explain why it was ruled, and forbidding that would mean a ruling cannot
cite its own evidence.**

**The distinction is what the isolation rule is FOR.** It exists to stop the arms **copying each other's
implementation**, not to keep **a number the Human Lead has already ruled on** out of reach. **An
unruled characterisation relayed into a prompt is a measurement the receiving arm cannot check. A ruled
figure in a decision entry has already been through the Human Lead's diff** — it is a spec input, not a
peek at the other arm's work.

**But the leak is made EXPLICIT rather than accidental.** **Both arm files state that decision entries
may contain cross-arm content**, so an arm reading `decisions/` knows what it is reading and is not
stumbling into a route around isolation. **An arm may cite such content, naming `decisions/` as its
source. It may never open the other arm's output folder, and it may never treat a cross-arm figure as
something it measured.**

## Propagation

A ruling lands in `decisions/` **and** in every file an agent reads. Recorded only in `decisions/` is not recorded.

**There are eight surfaces**, and all eight are checked on every edit:

1. `task-sheet.md`
2. `.claude/agents/data-scientist.md`
3. `.claude/agents/data-scientist-b.md`
4. `.claude/agents/analytics-engineer.md`
5. `.claude/agents/analytics-engineer-b.md`
6. `artifacts/` — deliverables carrying superseded figures are stamped, not left to be read as current
7. `.claude/agent-memory/second-brain/` — it is fed back into rulings, and stale memory has already caused a wrong one
8. `processed/` — **the first file an implementation reaches for.** `adopted_rule.json` carried revision-3 figures against the approved revision-6 rule while no control covered it, and a Step 8 instance had to work around it. Data tables are data; **the figures live in the metadata files**, and large tables are skipped by size and **listed, never silently**

**Read-back plus grep. Read-back alone is not verification.** Human Lead ruling, 2026-08-13. Reading an edit back proves the new text landed. Only grep proves the old text is gone, and a file can hold both at once — three consecutive propagation failures were exactly that, an adopted figure and its superseded predecessor live in the same file, sometimes ten lines apart, each declaring the other wrong.

So after any edit: grep all EIGHT surfaces for the superseded strings and require **zero hits**, except where a string is explicitly named as superseded at the point of use. Report the hit counts.

**And grep the corrected string too, requiring non-zero.** Added 2026-08-13 by the analytics-engineer, who found the negative half insufficient on the first run under it: **a figure that was never written returns zero hits on every superseded form of itself.** The DERIV bound was absent from all five spec files rather than present and stale, so the negative grep passed clean on a file set that contained the defect. A defect has two shapes — the wrong figure present, and the right figure missing — and the negative grep sees only the first.

**A grep hit is not a defect until you read the line.** Several figures in this study are correct on one population or scope and superseded on another, and a check that treats every hit as a defect chases them while a check that dismisses them misses the real ones. The register of known false positives is maintained in `.claude/agent-memory/second-brain/glossary-terms-and-thresholds.md`; the decision entry that adds or withdraws a row cites it.

**Registering a string as a false positive disarms the control against it.** Do it only when the legitimate reading is verified live under the *adopted* rule, and withdraw the row the moment it stops being. `9.6830%` was registered as legitimate and was superseded on four surfaces at the time — the exemption was granted to the one string the control most needed to catch.

## Generated files that function as checks

**A check nobody can see is not a check.** Human Lead ruling, 2026-08-13 (`0082`). **A generated file that functions as a check is COMMITTED** — a verification living only in a working tree verifies nothing anyone else can rely on, and it is invisible to all eight propagation surfaces, which is where the defects this project keeps finding actually hide.

**Condition, and it is not optional: a committed generated file states WHAT GENERATED IT and WHEN.** Otherwise it becomes the stale-figure problem the provenance rule exists to prevent — a file that looks authoritative, is read as current, and was produced by a pipeline that has since moved. **A generated file without its provenance is worse than no file**, because it is trusted.

**This governs the generated artifacts that already exist**, including `src/step7_regenerate_derived.py`'s output blocks and the stamps it writes.

## Derived figures

**When a bound endpoint moves, every figure computed from it moves.** Correcting an endpoint and leaving its derived quantities behind has now happened twice in consecutive entries. So each endpoint carries a written list, and **the list is checked as a set whenever that endpoint moves** — not the figure that prompted the correction, the whole set.

**The lists close transitively.** When an endpoint moves, check its list, **and the list of every figure on that list, to fixpoint.** A one-hop check is not enough and the gap has already bitten: the started-and-left floor moves the Continued ceiling, which moves the three-ceiling sum and the excess count — and `1,307 / 100.6646%` left live in both `data-scientist` files was **propagation failure #16, "the severe one."** It is two hops from the floor. A list that stops at the first hop does not reach the failure it was written to prevent.

**Started-and-left floor** — eight derived figures:

1. the **bound width** itself — the floor is its lower endpoint, and this figure has the longest defect history in the study (the 0.4033/0.4032 artifact, corrected twice)
2. the **conditional sub-interval** floor and width (the conditioning constrains the never-started exclusions only, so this floor moves with the bound floor and its width is never the exclusion count alone)
3. the **attainable-corner table** — the floor corner and the Continued value in that row
4. the **bound ÷ account-clustered sampling width** ratio, per arm
5. the **sub-interval ÷ sampling width** ratio, per arm — second-order, off item 2
6. the **per-`W` sensitivity series**, every arm, both bounds, both populations — **Step 13 is the consumer**, so a series carrying the un-widened floor at each arm is a live defect eight figures wide
7. any **ratio between two widths** — e.g. "the sub-interval is a factor of N narrower than the bound", which moves when either width does
8. the **Continued ceiling**, whose own list then runs

**Never-started floor** — four: the attainable-corner table's floor corner and its Continued value; the bound width; the bound ÷ sampling width ratio; and the Continued ceiling, whose own list then runs. *(It has no conditional sub-interval — the sub-interval conditions on this bound's own exclusion set.)*

**Any ceiling** — three: the **three-ceiling sum and its excess**, on each population separately; the **excess mechanism** count (`2 × never-started exclusions + started-and-left exclusions`); and the corner table row that attains it.

**Register every superseded value the move creates, not just the one that prompted the correction.** Each figure on a list that moves leaves a superseded string behind, and an unregistered string is one the grep control will not flag. Correcting four figures and registering one is how three of them stay live.

**One register, in `src/step7_register.py`, imported by every script that checks.** Two hand-maintained copies diverged by an entry after a single use, and neither held the values that were wrong. **A value can be superseded in one file and correct in another** — the two arms' ratios are — so the register is scoped by file where it needs to be, and **the positive half must cover the entry's own corrections**, which is what it did not do.

**Both populations, always.** APPLY and DERIV are separate lists with separate arithmetic, and a correction applied to one and not the other is the same defect as not applying it at all.

**Add a row when a new figure is derived; never remove one.** A list that shrinks is how the next one gets missed.

**Derived figures are REGENERATED, not patched.** Human Lead ruling, 2026-08-13. Four consecutive decisions corrected these artifacts by hand-patching individual values into published files, and every finding in Red Team reviews 9 through 11 was a value a patch reached in one file and missed in another, or reached in the `.md` and missed in the `.json`, or reached a ratio and missed its numerator. Eleven entries of one error class is a method that cannot converge.

So: `src/step7_regenerate_derived.py` reads the stored counts and writes **every** derived figure into **both halves of both arms** from a single expression each, then verifies numerically that no superseded value survives at any path. Anything derived belongs in it. **If you find yourself editing a derived number by hand, that is the defect.**

***CONSTRAINT ON FUTURE SCHEMA EDITS, recorded 2026-08-18 (`0109`), named by `reviewer-engineering`:***
**the `step_dual_status` rename fails loudly ONLY BECAUSE `by_producing_arm` is NOT inside a `oneOf`.**
**If an absence branch is ever added there, a writer emitting the old `dual_status` key stops failing
against `additionalProperties: false` and instead produces a silent `matched 0 oneOf branches` at the
parent** — ***the loud failure becomes an invisible one.*** **This is a property of TODAY'S BUILD, not
of the design, and it must be re-checked whenever an absence branch is added anywhere above a renamed
key.**

**The two arms' sampling-width conventions are named inputs**, so one arm's denominator cannot silently become the other's; reconciling a divergence is a spec decision and must be visible as one.

*(A second property was claimed here — that a value still live somewhere cannot enter the superseded list, because the list is generated. **Withdrawn 2026-08-13: the mechanism never fired.** The filter compared against a list that never contained the values in question, so it was a no-op. `0.3575` and `0.0672` are out because they were never put in. A control asserted to exist is not a control, and this one was found by reading the code rather than the claim.)*

**Stamps are negative only.** A stamp naming the corrected value guarantees the positive grep passes whether or not the body was fixed. A stamp names what is superseded and points at the generated block; it restates no adopted figure.

**A file-level stamp declares a file's STATUS, never its individual values.** Exempting a whole file because a stamp appears in its head exempted 19 `.md` and 16 `.json` files — the entire Step 7 artifact set, including both **operative** deliverables — and a wrong ratio survived a passing check inside one of them. A wholly superseded file is exempted by **name, in the source, with a reason**; a partially superseded one is checked value by value.

**An empty result and a clean result are the same value, and only the control knows which it produced.** A check that finds nothing because it looked nowhere must **fail**, not pass — three controls in six entries reported clean while checking zero rows. Every path that can return "nothing found" states whether it found nothing or looked at nothing, and prints its coverage count.

**One definition per statement and per figure.** If two writers render the same sentence, that is two places to withdraw it from and the withdrawal will reach one. Both halves render one object, and **agreement between them is compared off disk, never asserted.**

**A withdrawal is a correction, and a generated file cannot be corrected by hand.** A withdrawn sentence was struck in the three places a human had typed it and left in the generator, which wrote it back over all four operative deliverables on the next run — the same file then asserting it in a generated block and striking it 240 lines lower in prose. **If a claim is emitted by a script, the script is where it is withdrawn.**

**The numeric controls cannot see a claim.** This chain withdraws claims about as often as it corrects figures, so `WITHDRAWN_PHRASES` in `src/step7_register.py` holds the withdrawn ones and `check_surfaces.py` scans `.md` text and JSON strings for any occurrence outside a strikethrough or a withdrawal note.

**Three blindness classes, and only two are checked.** The controls see **wrong numbers** (`check_surfaces.py`, numerically, at both precisions) and **withdrawn claims** (`WITHDRAWN_PHRASES`). They do not see **a withdrawn ARGUMENT built from correct statistics.**

The instance that named the class: `0054` §3 argued the widened floor from *"the 90 have p5 margin 1.7 days, minimum 0.13."* `0055` §2 withdrew that as cherry-picked — the same 90 have median 44.5, and the correct ground carries no margin statistic at all. **But 1.7 and 0.13 are correct statistics**, withdrawn only as *grounds*, so there is no superseded number for the numeric half to match; and the argument was paraphrased rather than quoted, so there is no phrase for the phrase half to match. **It survived in `second-brain`'s memory across three files and nine entries, and only a reading agent found it.**

**No control is built for this.** A withdrawn argument is recognised by what it *claims*, not by its text or its digits, and a checker that tried would be a prose checker. **What stands in for one: when an entry withdraws a ground rather than a figure, say so in the withdrawn-claims register and name the statistics that are still true but no longer load-bearing** — the statistic is not wrong, the use of it is.

**Known limit, still open:** both numeric halves walk **numeric leaves only**, so a superseded *figure* inside a JSON **string** remains invisible to them. **Do not record a gap as harmless without checking whether it is currently occupied** — this one was written down as *"not a defect today"* while a defect was sitting in it, in four files.

**Check with `src/check_surfaces.py`, not with `grep`.** Matching is numeric, at a tolerance, across all EIGHT surfaces. Textual grep cannot see the JSONs: the register stores 4-dp strings and the JSON stores 6-dp literals, so `9.6830` is not a substring of `9.682997`. Every value that survived review 11 was one whose registered form rounds up and therefore could never match.

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

## A ruling is not closed until it is in the artifacts

**A ruling recorded in `decisions/` and propagated to the spec is NOT closed. It is closed when the
ARTIFACTS carry it.** Human Lead ruling, 2026-08-16 (`0093`).

**The mechanism, and it is structural rather than a lapse: the arms only rewrite their deliverables on a
RUN.** So every ruling lands in `decisions/`, reaches `task-sheet.md` and the agent files the same hour,
and **both arms go on publishing the superseded text until the next rerun** — during which the ruling is
recorded as done, the propagation control passes on all eight surfaces, and `artifacts/` still says the
old thing. **Every ruling since `0084` has passed through that window.**

**This is why `artifacts/` is surface 6 and why the sign-off rule above exists.** The two rules are one
mechanism seen from both ends: **a deliverable is corrected only by rerunning its arm**, so **a ruling is
closed only after that rerun has happened.**

**Consequences, and none of them is optional:**

- **A decision entry does not say "closed" while the artifacts still carry the superseded text.** It says
  what is propagated and what is **pending a rerun**, and names which.
- **A propagation report states which surfaces are reached AND which await a run.** *"Surfaces 1, 4–5
  reached; 6 and 8 pending both arms"* is the honest form. **A propagation report that lists six surfaces
  and omits that two carry stale text is the defect this rule exists to stop.**
- **Never edit an artifact to close this gap** — that is the sign-off rule, and it is how the gap becomes
  unsigned text instead of stale text.

## A deliverable asserts only what its own arm measured

**A gate deliverable asserts its own figures, its own inputs and its own limits — and nothing else.**
Human Lead ruling, 2026-08-17 (`0096`). **It does not assert the state of other steps, other gates, the
other arm, the shared controls, or the study as a whole.**

**An arm cannot know those things.** It measures a surface at one instant and publishes into a file that
is never re-read against the world, so **every such claim is expiry-dated from birth**. **Three
consecutive Red Team passes found a stale one**, and the last was worse than stale: a deliverable told
the reader `check_surfaces.py` **exits 1** when it exits 0 — true when measured, false when read.

**This is the `## Derived figures` provenance rule applied to STATEMENTS rather than FIGURES.** A figure
without its provenance is unreadable; **a statement about a surface the arm does not own is unreadable
the same way, and worse, because it looks like a finding.**

**What this excludes, concretely:**

- **Control exit statuses.** Whether a shared control passes is not the arm's measurement. Report the
  observation to the Human Lead; it belongs in `logs/`, never in `artifacts/`.
- **Disk state of other surfaces** — which files exist, which carry a string, how many entries are in
  `decisions/`. **Measured at an instant, published forever.**
- **Build-history narration.** A build stamp and a pointer to the run record, not a chronicle of what
  earlier builds got wrong.
- **The status of other steps or gates**, including whether Step 8 itself is approved.

**What it still requires:** the arm's own defects, its own open items, and its own divergences from the
spec — **those are things it measured.** **An arm that notices something wrong on another surface REPORTS
IT to the Human Lead and does not publish it as a finding in a deliverable.**

## Where a check's CODE lives, and where its OUTPUT lives

**The CODE goes in `src/` and is committed. The RUN RECORD goes to `logs/`.** Human Lead ruling,
2026-08-18 (`0109`), because two rules had been read as pointing opposite ways.

**`0082` — *"a check nobody can see is not a check"* — is satisfied by THE CODE BEING VISIBLE**, in
`src/`, on a propagation surface, readable by any reviewer. **`0096` ruling 1 sends EVIDENCE ABOUT THE
TOOLING to `logs/` rather than `artifacts/`**, because a deliverable asserts only what its own arm
measured, and a control's exit status is not that.

***They do not conflict. They govern different objects*** — `0082` governs **the check**, `0096` governs
**the report of having run it**. **A selftest committed to `src/` with its output in `logs/` satisfies
both.**

## Artifact sign-off

**No artifact is trusted without its producing arm's sign-off.** Human Lead ruling, 2026-08-16 (`0092`).
**A deliverable is corrected by RERUNNING the arm that produced it, never by hand-editing the file.**
Hand-editing puts **unsigned text into a signed deliverable**, and `artifacts/` is what Red Team reads,
what Step 9 consumes, and propagation surface 6.

**This holds even when the change is labelling only and no figure moves** — *especially* then, because
that is exactly when hand-editing looks harmless. **The producing arm is the only party that can
attest the text matches what its pipeline computed**; an editor who did not run the pipeline is
asserting agreement rather than establishing it, which is the shape this study has spent eleven entries
on.

**It is the `## Derived figures` rule one level up:** derived figures are regenerated, not patched, and
**deliverables are rerun, not patched.** The scripts already refuse to hand-patch a number; this refuses
to hand-patch a sentence.

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
