---
name: user-human-lead
description: Who the Human Lead is on the Season 2 abandonment study, what they own, and how they make and record decisions
metadata:
  type: user
---

# The Human Lead

Directs the Season 2 abandonment study. Owns Steps 2, 14, 15, 17 and 18, approves all five
gates, selects the Step 12 segment cut, and specifies the Step 16 visualization. When a step
names them as owner, no agent acts on it — not draft it, not prepare it, not offer a version.

## How they decide, observed at the Step 1 gate (2026-08-10)

- **They rule against reviewers when the reasoning holds, and they record the objection anyway.** Red Team's B2 was overruled and the objection, the ruling, and the reason all went onto the public record rather than the objection being deleted.
- **They distinguish deferral from omission, explicitly.** `pull_date` was adopted in form with its value deferred, and the deferral was written up as a decision with its structural reason attached.
- **They adopt named items by name.** `H = 91 days` and the D12 thresholds were approved individually rather than swept in with the document, so the record shows which items got specific assent.
- **They fix the source file rather than routing around it.** When Step 1 flagged a scoping dependency it could not resolve, they amended `task-sheet.md` Steps 7 and 9 directly — the file the isolated instances actually read — which converted a future spec ambiguity into a future bug.
- **They keep provenance visible.** Sections 10.0b and 10.0c preserve which items came from Red Team, who drafted them, and who adopted them, so no agent can be read as having self-adopted.

## The pattern, confirmed again on 2026-08-10

- **Every decision that two isolated instances must obey goes into `task-sheet.md`**, not only into the artifact that reasoned about it. Done for pair-level liveness (Steps 7, 9), then again for D14 (Steps 6 and 13). The artifact keeps the warrant; the task sheet carries the rule. **Step 8 is the one place this has not yet been done** — see [[open-items-and-contradictions]] O3.
- **They close a provenance gap by making the run reproducible rather than by deleting the figure.** The undocumented probe became a script, a run record and a public write-up at zero live calls.
- **They distinguish an evidence edit from a rule edit on an approved artifact**, and say so in the approval record: a rule change reopens the gate, added evidence does not.
- **They keep the log of record and the working memory separate.** `decisions/` is the artifact; agent memory is continuity and consistency checking against it, and never edits it.

## What they want from Second Brain

The Step 18 decision log, assembled continuously and handed to them as text — they write the
files in `decisions/`. They ask for verification against the files rather than acceptance of a
briefing. See [[feedback-verify-against-files]].

## Working style cues

- Precise about ownership and about what an approval does and does not cover.
- Wants directions of bias named on the same line as the number, in both directions.
- Treats "we did not measure it" as unavailable for anything that lands in a published category.

Related: [[gate-step1-outcome-definition]], [[decision-log-step18]].
