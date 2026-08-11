---
name: feedback-verify-against-files
description: On this study, verify every briefed fact against the artifact before recording it — the document governs over any summary, including the Human Lead's own
metadata:
  type: feedback
---

# Verify against the files. The document governs, not the briefing.

**Rule.** When the Human Lead briefs an arc — a gate outcome, a red team verdict, a partner
review — treat the briefing as a pointer, not as the record. Read the artifact and record what
it says. Where the two differ, the artifact wins. They have said this explicitly: *"Do not rely
on this summary where the document differs; the document governs."*

**Why.** This study's characteristic failure is a confident claim that does not follow from the
definitions actually written — ten such claims were withdrawn or accepted as risks at Step 1
alone (see [[withdrawn-claims-register]]). A memory system that records briefings instead of
artifacts would reproduce exactly that failure one layer up, and Second Brain is the thing
meant to catch it. The Human Lead also flags items *for* verification rather than asserting
them, which is an invitation to check, not a formality.

**How to apply.**
- Read the artifact end to end before writing memory about it, including the sections the briefing did not mention.
- Re-do the arithmetic on any number that gates a decision. It has caught real errors here — the "guarantees 91 days of post-window observation" claim was false by subtraction.
- Trace cited figures to a source. Two figures in the approved Step 1 document cite "the Step 0 probe" and appear in neither public Step 0 artifact; that was found by looking, not by being told.
- Check the *other* files too. Contradictions live between artifacts, not inside them — Step 0's open-items list and Step 1's first sentence disagree about whether the Step 4 endpoint was decided.
- Never write to `artifacts/`, `decisions/`, or any project folder. Memory directory only. Hand assembled decision-log text to the Human Lead and let them write it.
- Surface the contradiction and name the two things that conflict. Do not approve, decide, or arbitrate, and never block the critical path.
- Carry no usernames, user IDs, or individual watch histories into memory. `logs/` contains usernames in endpoint paths; describe runs by their run tag and timestamp instead.

Related: [[user-human-lead]], [[open-items-and-contradictions]].
