---
name: process-incidents-and-safeguards
description: Operational incidents in the Season 2 study that destroyed or corrupted machine-local data, their shared root cause, and the safeguards they imply — distinct from the analytical withdrawn-claims register
metadata:
  type: project
---

# Process incidents — what got broken while doing the work

Distinct from [[withdrawn-claims-register]], which records claims that were **wrong**. This
records operations that were **destructive**. Both matter for Step 18; only the first is currently
visible anywhere in the repo.

**Why:** the analytical record is heavily reviewed — three Red Team HOLDs, an Engineering HOLD,
twelve withdrawn claims. The operational record is not reviewed at all, and Step 4 is a ≥23-hour
unattended pull over 210,500 calls where the same class of mistake costs an irreplaceable API
budget rather than a rerun.

**How to apply:** before any regeneration, backfill or replay is run over `raw/`, `processed/` or
`logs/`, ask where its output goes and what is already there. Raise it once, name the risk, stop.

## Step 3, 2026-08-11 — one root cause, two losses

**Root cause: `src/step3_backfill.py --out-dir` was pointed at the live `raw/step3/` directory.**
Its default is a separate backfill directory (`BACKFILL_DIR`, `src/step3_backfill.py:583`); the
default was overridden. Two things followed from that one action:

1. **The live call ledger in `raw/step3/state.json` was zeroed** by the replay rewriting the state
   file. Restored from `logs/step3_run.json`. The file carries its own `ledger_note` recording
   `restored_at: 2026-08-11T03:41:30Z+restore` and naming the command that did it. **Verified
   present** — this one is self-documenting, which is the right outcome.
2. **Two backup directories under `raw/step3/` were destroyed.** The regenerated files supersede
   them, so analytical loss was small, but **the old-code output is not recoverable** — which
   means the spanning-tree edge list produced by the live run can never be compared against the
   backfilled one. `raw/step3/` now holds six files and no backup directory. **Verified.**

**What makes this worth carrying rather than filing away:** the replay was itself a correctness
measure — it backfilled round metrics and verified them at **0 mismatches over 36 rounds × 12
fields at zero live calls**, which is exactly the discipline this project wants. The tool was
right; the destination was wrong. A verification step overwrote the thing it was verifying.

**Update 2026-08-12 — it happened a second time, and it now has a standing remedy on the record.**
`decisions/README.md` open item 16: *"`step3_backfill.py --out-dir raw/step3` zeroes the call ledger
in `state.json` … **This has happened twice** and been restored from `logs/step3_run.json` both
times."* The remedy named there: **restore after every regeneration, or use the script's default
out-dir, which does not touch that file.** The item stays open because the ledger is **the only
record of Step 3's spend against the API budget and it is gitignored** — a git-tracked artifact
would have made both incidents recoverable by `git checkout`.

**Generalised, because Step 5 ran six revisions of regeneration over `processed/step5/`:** a replay
that regenerates its own inputs can silently overwrite the evidence it was run to check. Step 5's
regeneration of `revision4.json` after the unit-bug correction is the same shape and went the right
way — I verified the corrected values are in the file — but it was verified by reading, not
guaranteed by design.

## Step 4, caught 2026-08-12 — a near-miss on the exact failure `CLAUDE.md` names

**The pull ledger carried `"records": 0` on all 287 `discarded_over_tolerance` rows**, while using
`null` for every other withheld field (`parse`, `parsed_path`, `is_data: false`).

`CLAUDE.md` states the hazard in as many words: *"a skipped user silently read as empty becomes a
false 'never started' in the headline."* `0010` and `0012` both require discarded and skipped users
to stay distinguishable **exactly as `access_denied` does** — a distinct outcome, never folded into
any skip category, **never represented by an empty result**. A consumer reading `records` without
also reading `outcome` would have seen a real zero.

**Fixed:** `records` is now `null` on all 287 discarded rows, by
`src/step5_fix_ledger_records_null.py`, which rewrites in place and verifies the row count and every
other field is untouched. `items_discarded` still carries what was fetched and thrown away.

**Why this is worth carrying.** Nothing was lost and no number moved — it was caught before any
downstream step read the field. But **the rule was written three times, in `CLAUDE.md`, `0010` and
`0012`, and the implementation still emitted the value the rule forbids.** A rule stated in prose
does not enforce itself at the schema level. **When a category means "absent", check that every
field on that row says absent** — one field saying `0` is enough to defeat all three statements.

## Related, not an incident: one round that looked like the API and was not

Round 8 recorded 2,796 s wall clock against a single 2,697 s inter-request gap — 96.5 % of the
round — with **zero 429s**. A suspended machine, not throttling. Fixed by decomposing the round
clock into throttle sleep, rate-limit sleep, backoff sleep, in-request time and unaccounted time.
Two things to carry: **the machine suspends**, which over a ≥23-hour Step 4 is a scheduling fact
rather than an anomaly ([[open-items-and-contradictions]] S7); and per-round **throttle sleep is
`not_recoverable`** and was left `null` rather than estimated, which is the handling to expect and
to defend if anyone asks for a number there.

Related: [[open-items-and-contradictions]], [[decision-log-step18]],
[[glossary-terms-and-thresholds]].
