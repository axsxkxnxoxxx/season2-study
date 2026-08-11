# Decision 0004 — 403 handling: skip the user, hard stop the block

| | |
| :--- | :--- |
| **Decision** | A 403 on a **user resource** skips that user, logs it with full headers, and continues, bounded by two circuit breakers. Any other 403 still **hard stops**. Ambiguity resolves strict. |
| **Decided by** | Human Lead |
| **Date** | 2026-08-10 |
| **Amends** | `CLAUDE.md`, API discipline — previously "On a 403: hard stop and report" with no exceptions |
| **Closes** | `artifacts/step0-access-and-setup.md` §6 open item 2 |
| **Implementation** | `src/trakt_client.py`; rule and evidence in `artifacts/step0-access-and-setup.md` §7 |
| **Status** | Closed. Offline checks 27/27 → **44/44**. Zero live calls. |

---

## Why the old rule had to change

The old rule was correct about the thing it was protecting: losing Trakt access would end the
study, and an application-level block is not something to retry through. But it made no
distinction between a block and a refusal, and **Step 4 is a multi-day unattended pull**. Under
the old rule a single private or restricted profile halts an overnight run.

Step 0 had already flagged the ambiguity (§6 open item 2): Trakt documents **401** for a private
profile, which the client treats as unavailable-and-move-on, but if Trakt returns **403**
instead, one private user stops everything. **No live 403 has ever been observed** — that path
was proven against a fake session only. So this decision is made on inference, and the
implementation is built to say so.

## The rule

Classified in order:

1. **Not a user resource** → hard stop.
2. **`X-Private-User` present and false-like** → hard stop. Trakt is saying this profile is not
   private, so the refusal is not explained by privacy.
3. **`X-Private-User` present but unrecognized** → hard stop. Not guessed at.
4. **`X-Private-User` true-like** → skip.
5. **User resource, header absent** — the expected live case → skip.

"User resource" is `users/<id>[/...]`. Bare `users` and the reserved account segments (`me`,
`settings`, `requests`, `hidden`, `likes`, `saved_filters`, `follows`) hard stop.

**`X-Private-User` is positive confirmation only.** The evidence forced this: the header carries
a real value on `GET /users/:id` only, and is **absent on all 11 captured
`/users/:id/history` and `/users/:id/watched/shows` responses** — precisely the endpoint family
Step 4 uses. Its absence therefore carries no information and must never be read as "not
private." A rule keying on the header's presence would have misfired on essentially every real
user 403. **The endpoint path is the primary discriminator.**

## Two circuit breakers bound the permissive path

Because the discriminator is inferential rather than observed:

- **A — 5** consecutive unconfirmed user-403s with no intervening 2xx → hard stop. Only a 2xx
  resets the streak; a 401 or 404 does not. Exposure to a block that first surfaces on a user
  endpoint is bounded at 5 requests.
- **B — 200** user-403s in a run → hard stop. A tripwire, not a discriminator: 403-at-volume
  contradicts Trakt's documented 401-for-private, so it means the model is wrong.

Both are constructor arguments.

## Where it misfires, in both directions

- **Permissive residual:** up to 200 requests into a resource-scoped block before breaker B
  fires.
- **Strict residual:** a stopped run on a cluster of five private users.

**Ambiguity resolves strict.** A false hard stop costs wall-clock but no API budget and no data —
the client resumes from disk. A false skip risks the study's access, which is unrecoverable.

## A skipped user is not a user with no history

This is a correctness requirement, not bookkeeping. Step 1 §0 makes sweep completeness load-
bearing: a missing user read as empty becomes a **false "never started"** in the study's headline
category. Four mechanisms keep them apart:

- `access_denied` is its own response field, never folded into `unavailable`.
- `fetch_all()` returns an explicit outcome of `complete` / `unavailable` / `access_denied`. All
  three can carry zero items; only one of them is data.
- Cache meta carries `access_denied`, so per-user state survives a restart without the log.
- A log index is readable back for Step 4 reconciliation.

A **mid-sweep** 403 raises and **discards the pages already read** rather than returning a partial
sweep, reporting the discarded count while the pages stay in `raw/` for a resume.

`logs/blocked_endpoints.ndjson` was **extended, not replaced**: it now takes a record for both
branches with `outcome`, `decision_reason`, `is_user_resource`, full response headers,
`X-Private-User`, `X-Ratelimit`, `Retry-After`, a body excerpt, and both breaker counters.
Legacy records with no `outcome` read as hard stops.

## Note on the cache schema

`SCHEMA_VERSION` was **deliberately not bumped** for the new `access_denied` meta field. Bumping
it would trigger the client's stale-cache re-fetch across every Step 0-era entry, changing the
probe figures that `artifacts/step0-history-endpoint-probe.md` and the approved Step 1 addendum
cite as evidence. The field defaults to `False`, which is correct for every pre-amendment entry,
and a check pins that default.

## Standing caveat

**The live behaviour is still unobserved.** §7.1 of the Step 0 artifact labels each claim
documented / observed / inferred / assumed. The first live exercise of either branch will be
during Step 3 or Step 4, and it should be treated as a test of this rule rather than as routine.
