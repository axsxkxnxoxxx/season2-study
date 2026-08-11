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
definitions actually written — eleven such claims were withdrawn or corrected at Step 1 alone,
plus one accepted risk (see [[withdrawn-claims-register]]). A memory system that records briefings instead of
artifacts would reproduce exactly that failure one layer up, and Second Brain is the thing
meant to catch it. The Human Lead also flags items *for* verification rather than asserting
them, which is an invitation to check, not a formality.

**How to apply.**
- Read the artifact end to end before writing memory about it, including the sections the briefing did not mention.
- Re-do the arithmetic on any number that gates a decision. It has caught real errors here — the "guarantees 91 days of post-window observation" claim was false by subtraction.
- Trace cited figures to a source. Two figures in the approved Step 1 document cited "the Step 0 probe" and appeared in neither public Step 0 artifact; found by looking, not by being told. Both were reproduced and the gap closed on 2026-08-10 — flagging it is what produced the probe write-up.
- Check the *other* files too. Contradictions live between artifacts, not inside them — Step 0's open-items list and Step 1's first sentence disagreed for a week about whether the Step 4 endpoint was decided. Also check whether a *closed* item is still recorded as open somewhere; stale records outlive the problem.
- **`decisions/` is the artifact of record and this memory is not.** Do not duplicate it. Hold what it does not carry — five-field entries for judgments covered only as "approved with the document" — and a coverage map of what it does. If an entry there looks wrong or incomplete, **report it; never edit it.**
- Never write to `artifacts/`, `decisions/`, or any project folder. Memory directory only. Hand assembled decision-log text to the Human Lead and let them write it.
- Surface the contradiction and name the two things that conflict. Do not approve, decide, or arbitrate, and never block the critical path.
- Carry no usernames, user IDs, or individual watch histories into memory. `logs/` contains usernames in endpoint paths; describe runs by their run tag and timestamp instead.

Related: [[user-human-lead]], [[open-items-and-contradictions]].
