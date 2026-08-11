# Step 0: Access and Setup

**Owner:** Analytics Engineer · **Mode:** Chained · **Reviewer:** Engineering
**Status:** Engineering verdict was proceed. Three blockers and four should-fixes
were authorized and are closed. The finding that blocked the Step 4 pull design is
**closed by the Human Lead, 2026-08-10** — see Section 0.
**Dates:** first cut and Engineering review 2026-08-10; fixes and endpoint decision same day.

Three things were due: a working resumable client, one successful test pull, and the
documented rate limit. All three are below, followed by the review fixes and the
endpoint finding, which is now resolved.

---

## 0. Finding that needed a decision before Step 4 — **CLOSED**

> **RESOLVED by the Human Lead, 2026-08-10.** The replacement source is
> **`GET /users/:id/history`, unfiltered, one sweep per user.** `/users/:id/watched/shows`
> is **not** used by this study for outcome measurement, for the reasons set out below.
>
> **"One sweep" means one logical pass per user, not one call.** The unfiltered history
> endpoint paginates exactly as `watched/shows` does, and more heavily: a probe profile
> returned `item_count = 15812` at `page_count = 1582` with `limit=10`, which is roughly
> **64 pages at `limit=250`** for a single user. Any Step 4 throughput estimate must be
> built on pages, not on users. The one-call-per-user assumption that this section
> disproved for `watched/shows` must not be reintroduced for `history`.
>
> **The sweep must be complete, and that is a correctness requirement rather than a
> performance one.** Records come back newest-first, so a truncated sweep is
> indistinguishable from a genuine "never started" and lands directly in the study's
> headline category. Capping pages at Step 4 would silently manufacture the result.
> `artifacts/step1-outcome-definition.md` §0 records the same dependency from the other
> side; the two files agree.
>
> **What the decision fixes:** unfiltered (the endpoint mixes `type: episode` with
> `type: movie`, and Step 7 liveness draws on the whole sweep as account-wide evidence, so
> filtering server-side would destroy the liveness input); per-episode `watched_at`
> timestamps, which is the property `watched/shows` lacked and the reason it was rejected;
> and `action` retained rather than filtered, since Step 5 contamination diagnostics run on
> it.
>
> Recorded in `decisions/`. The original finding is preserved unedited below, because it is
> the warrant for the decision.

**Original finding, as written when it was open:**

The design decision was to pull histories with **one call per user** to
`/users/:id/watched/shows`, returning the full watched library **with per-episode
timestamps**, instead of per-user-per-show history calls. Confirming the pagination
behaviour was in scope. Both halves of the premise turn out to be wrong, so this is
reported rather than worked around.

**1. It paginates.** `X-Pagination-Page-Count` is greater than 1 for any profile with
more than one page of shows. The `limit` parameter is honoured but **silently clamped
at 250**: a request for `limit=1000` came back with `X-Pagination-Limit: 250`. Cost is
therefore `ceil(shows_watched / 250)` calls per user, not one. The probe profile,
which has several hundred watched shows, needs 2. This is cheap and the client now
handles it strictly, but the one-call-per-user assumption should not be carried into
a Step 4 throughput estimate.

**2. It carries no per-episode timestamps at all.** This is the part that matters.
Four parameter variants were tried — no parameters, `extended=full`, `limit=1`,
`limit=1000` — and every record came back with the same five keys:

```
plays, last_watched_at, last_updated_at, reset_at, show
```

There is no `seasons` key and no `episodes` key in any variant. What the endpoint
returns for a third-party public profile under Client-ID-only auth is a **show-level
aggregate**: a total play count and a single "last watched" timestamp for the whole
show. Trakt's documentation describes seasons and episodes being included by default;
that is not what the API returns here.

Why this blocks the study rather than merely inconveniencing it. Step 1 defines S1
completion as the S1 finale plus 90 percent of S1 episodes, the abandonment point as
the highest S2 episode watched, and requires counting distinct episodes rather than
play events. None of those can be computed from a per-show play count. A single
`last_watched_at` per show also cannot separate an S1 completion date from an S2
start date, which is what the clock start in Step 1 is built from.

A secondary hazard even at show level: `last_watched_at` is the **most recent** watch,
so for any rewatcher it is not the first-watch date. That is exactly the timestamp
class Step 5 exists to distrust.

**This is a design decision and it is the Human Lead's.** I have not substituted an
endpoint, have not benchmarked alternatives, and have not run anything against a user
history beyond the four probe calls that answered the pagination question. Step 4
cannot be built against `/users/:id/watched/shows` as specified, and I am stopping
here rather than choosing the replacement.

Evidence is in `logs/step0_watched_endpoint_probe.json`; the probe is reproducible via
`src/step0_watched_endpoint_probe.py`, which now runs entirely from cache at zero live
calls.

---

## 1. Documented rate limit

| Quantity | Value | Source |
| :--- | :--- | :--- |
| Trakt application-level ceiling | 1000 GET calls / 5 minutes | settled in `CLAUDE.md` |
| Equivalent per-minute ceiling | 200 GET / minute | 1000 ÷ 5 |
| **What this client runs at** | **150 GET / minute** | `CLAUDE.md`, throttle below the ceiling |
| Second guard, 5-minute rolling | 750 GET / 5 minutes | 150 × 5 |
| Headroom against the ceiling | 25 percent | 750 of 1000 |

Both windows are enforced as rolling windows before every outbound request, not as
fixed buckets. A fixed bucket would allow 150 calls in the last second of one minute
and 150 in the first second of the next, which is 300 in a two-second span and would
breach the ceiling. The rolling window makes that impossible. The throttle constructor
**refuses** any value at or above the documented ceiling, so the limit cannot be raised
to 200 by editing a constant without the check failing.

The limit is a property of the **Client ID, not of a process**, so the budget is held
in a lock-protected file on disk and shared by every process that uses it. See fix 1.

**Constraint worth knowing:** Trakt returns the `X-Ratelimit` object only on a 429.
Six live 200 responses across four endpoints were inspected and none carried it, nor
any other rate header. There is **no way to observe remaining budget in advance**.
Client-side throttling is the only defence; the first feedback the API gives is the
block itself. This is the largest infrastructure risk in the pipeline and is why the
throttle sits at 75 percent of ceiling rather than nearer to it.

---

## 2. Working client

`src/trakt_client.py`. Behaviour, against the contract in `CLAUDE.md`:

**Authentication.** Client ID only, read from `.env` at runtime. No OAuth flow.

**Resumability.** Every response is written to `raw/` **before** it is parsed, at a
deterministic path derived from endpoint plus sorted query parameters. A request
already on disk is served from disk and never re-sent. Negative outcomes (private
profile, 404) are cached too, so a resumed job does not re-request known-unavailable
users. Each page of a paginated pull is cached separately, so resume is page-granular.
Cache entries carry a schema version; see fix 4.

**Private profiles.** Recorded with status and endpoint, counted, and skipped. Not
retried, not re-requested, not silently dropped.

**Transient failures** (timeouts, connection errors, 5xx): exponential backoff with
jitter, 2s base, factor 2, capped at 60s, 5 attempts, then raise.

**429:** reads `Retry-After`, pauses exactly that many seconds, resumes. Capped at two
pauses for any single request, so the same request is never retried in a loop. Three
stop conditions: consecutive pauses, a cumulative per-run budget (fix 7), and a
`Retry-After` above 900s, which stops immediately rather than sleeping through it.

**403:** immediate hard stop, no retry, after the evidence is persisted. See fix 2.

**Logging.** Status, the `X-Ratelimit` object, `Retry-After`, endpoint and method are
written to `logs/api_requests.ndjson` for **every** request, not only rate-limit
events, plus cache hits, stale-cache detections, backoff events, pauses and hard
stops. Full response headers are kept in the raw metadata sidecar.

---

## 3. Test pull

One live call, plus one repeat call to prove resume.

| Field | Value |
| :--- | :--- |
| Endpoint | `GET /shows/:id/seasons?extended=full` |
| Authentication | Client ID alone, no OAuth |
| HTTP status | 200 |
| Payload | 6 seasons returned, S1 and S2 episode counts present |
| Raw persisted before parsing | yes, under `raw/` |
| Live requests sent | 1 |
| Repeat of the same request | served from disk, 0 additional network calls |
| 429s, 403s, transient retries, errors | 0, 0, 0, 0 |

A **show** endpoint was used deliberately: Step 0 is not user discovery, and pulling a
user endpoint here would have pre-empted Step 3.

**Total live cost of Step 0: 9 calls.** One test pull, one header probe, one re-run of
the test pull to refresh the stale cache entry described in fix 4, one profile check,
four `watched/shows` variants, and one repeat that was served from cache. Peak
observed spend was 4 calls in a 60-second window against a cap of 150.

Run records in `logs/step0_test_pull.json` and `logs/step0_watched_endpoint_probe.json`.
Both are machine-local and contain no usernames.

---

## 4. Engineering review fixes

### Blockers

**1. Throttle state now persists and is shared across processes.** It was an in-memory
list, which was wrong twice over: two sibling processes would each have claimed 150/min
against a 200/min ceiling, and an empty ring after a restart would have allowed a full
burst before a crash plus another after it. The ring now lives in
`logs/throttle/budget.json` under an exclusive `flock`, so every process using the
Client ID draws from one budget and a restart inherits spend it did not make. The lock
is held only for the read-decide-write step, never while sleeping, so siblings are
serialised at the decision and not at the wait. Verified with two real OS processes:
each tried to claim 8 slots against a shared cap of 10, and the ring ended at exactly
10. An **unreadable** state file is not treated as a fresh budget — we cannot tell what
was already spent, so it is rewritten as a full window and the caller waits it out.

**2. A 403 is now recorded before it is raised.** Previously the exception was raised
before anything hit disk, so a resumed run re-requested the blocked resource and halted
in the same place: a stop-restart livelock that repeatedly requests into something that
just blocked us. The full response header set, the endpoint, the params, `X-Ratelimit`,
`Retry-After` and a body excerpt are now appended to `logs/blocked_endpoints.ndjson`
**before** raising. That file is loaded at construction, and a request to a recorded
endpoint raises without a network call. The hard stop is unchanged and deliberately so.
To retry a resolved block, clear that file.

The captured headers include **`X-Private-User`**, which is the block-versus-private-profile
disambiguation flagged as missing in the first cut. Confirmed against `raw/`: Trakt lists
`X-Private-User` in `access-control-expose-headers` on every response, and emits it with a
real value on `/users/:id` (observed `false` for a public profile). It was not emitted on
`/users/:id/watched/shows` 200s, so whether it appears on a 403 there is still unobserved
— the client captures it whenever present. Worth noting for Step 3 and 4 design: because
`/users/:id` returns `X-Private-User` directly, private status is knowable from a cheap
profile call without provoking a 403 at all. That is a design choice, not mine to make.

**3. Pagination is now strict.** `get_paginated` used to return silently when the
page-count header was absent or not an integer, and both live endpoints probed in the
first cut returned 200 with no pagination headers whatsoever — so this was not a
theoretical path. At Step 4 scale a truncated history is indistinguishable from a
genuine never-started and would have landed in the headline number instead of a log.
Now: a missing or non-integer `page_count` or `item_count` raises `PaginationError`; a
non-list payload raises, because item counts cannot be reconciled against it; a failure
on any page after the first raises rather than ending the pull; and accumulated items
are reconciled against `X-Pagination-Item-Count` at the end, with a mismatch raising
`ShortRead`. A private or absent profile on the **first** page remains the documented
log-and-move-on case, which is the one legitimate empty result. `fetch_all()` is the
entry point Step 4 should use, since it enforces reconciliation. A caller that passes
`max_pages` or breaks early gets a logged truncation and no reconciliation, by design.

### Should-fixes

**4. Cache entries carry a schema version.** The schema drifted mid-Step-0: the
test-pull meta had no `response_headers` key and the probe meta two minutes later did,
which would have left the first entry permanently stale and served forever. Meta
records now carry `schema_version`, and an entry written under an older version is
logged as `cache_stale` and re-fetched instead of served. The one stale entry from the
first cut was refreshed live, at a cost of one call, and the log shows exactly one
`cache_stale` event. The trade-off is explicit: a schema bump costs a re-fetch of
affected entries, which is the right side to err on.

**5. Secret hygiene no longer relies on `assert`.** `python -O` strips asserts, which
would have removed the guard entirely in an optimised run. Both call sites now raise
`CredentialLeak`. Verified by running the guard under `python -O` in a subprocess.

**6. Two overclaims corrected.** Both were real and both are now true statements
because the code changed, not only the prose:

- *"Writes are atomic."* They were not. The body was written temp-then-rename but
  `meta_path.write_text()` was not, and the meta file is what `_read_cache` keys on —
  so a crash mid-write could have left a truncated meta. The meta write is now also
  temp-then-rename. The accurate statement: body first, meta second, both atomic, and
  the meta file is the commit record. A crash between the two leaves an orphan body
  that is simply re-fetched, never a half-read served as complete.
- *"The Client ID is redacted from every write."* It was not. Redaction covers log
  records and metadata sidecars; **response bodies are written verbatim** and always
  will be, because raw fidelity is the point of `raw/`. Rather than weaken the claim I
  added the missing guard: a response body containing the Client ID is refused and
  raises, so nothing is written at all. The accurate statement is now: logs and
  metadata are redacted, bodies are refused if they contain the key, and the Client ID
  reaches no file on disk by either route. The test's glob was widened from
  `*.meta.json` to every file written, bodies included, so the check and the claim
  match.

**7. The 429 stop condition no longer depends on consecutiveness alone.** An
alternating 429/200 pattern reset the consecutive counter every other request and so
never tripped a stop, making sustained saturation invisible across an unattended run.
A cumulative per-run budget of 6 pauses was added, and it never resets. The consecutive
counter is kept and still resets on success, because "several consecutive pauses" is
the wording in `CLAUDE.md` and that is a settled constraint; the cumulative budget sits
alongside it rather than replacing it. Both are tested, including an explicit
429/200/429/200 case that asserts the cumulative rule is what fires.

---

## 5. Verification without spending API calls

`src/test_client_behaviour.py` exercises every failure path against a scripted fake
session. The paths that matter are precisely the ones we must never provoke on the live
API. **27 of 27 checks pass.**

| Group | Checks |
| :--- | :--- |
| Throttle | below ceiling; blocks at cap; survives restart; shared between siblings; unreadable state is conservative |
| 403 | hard stops and records full headers incl. `X-Private-User`; resumed run does not re-request |
| 429 | pauses for `Retry-After`; consecutive stop; alternating 429/200 trips the cumulative budget |
| Transient | 5xx and transport errors back off then succeed; exhausted backoff raises |
| Cache | prevents a second request; unavailable recorded and not re-requested; raw written before parse; meta carries schema version; stale-schema entry re-fetched |
| Secrets | Client ID in no file incl. bodies; body containing it is refused; guard survives `python -O` |
| Pagination | walks and resumes; missing header raises; non-integer header raises; short read raises; mid-pull failure raises; private first page is move-on; `fetch_all` reconciles |

Cross-process locking is additionally verified against two real OS processes.

---

## 6. Open items for the Human Lead

1. ~~**The Step 4 endpoint decision above.** The blocking one.~~ **CLOSED by the Human Lead,
   2026-08-10:** the source is `GET /users/:id/history`, unfiltered, one sweep per user.
   See the resolution box in Section 0 and the entry in `decisions/`. Step 4 is unblocked on
   this item. **Two conditions travel with it:** the sweep must be **complete** — a truncated
   sweep is indistinguishable from "never started" and lands in the headline — and throughput
   must be estimated in **pages, not users** (~64 pages per user at `limit=250` on the probe
   profile).
2. **403 on a user endpoint remains ambiguous, by design.** The rule says a 403 is a
   block and stops the run. Trakt's documented behaviour for a private profile is 401,
   which the client treats as unavailable-and-move-on. If Trakt returns 403 for a
   private profile, one private user would halt a Step 4 pull — but it will now halt
   with the headers captured and the endpoint recorded, so the cause is diagnosable
   from `logs/blocked_endpoints.ndjson` and a resume will not hammer it.
3. **No Sabbath or wall-clock scheduling is built in**, and none was added here. Start
   and stop remain manual, per the task sheet.
4. **No live 429 or 403 has been observed.** Those paths are proven against a fake
   session only. Their first live exercise will be during Step 3 or Step 4.
5. **The throttle ring uses wall-clock time**, since it must be shared across processes
   and survive restarts. A backwards system-clock jump would make it over-cautious,
   never over-permissive. Flagging the direction of the failure, which is the safe one.

---

## Files

| Path | Contents | Git |
| :--- | :--- | :--- |
| `src/trakt_client.py` | The client | tracked, no secrets |
| `src/test_client_behaviour.py` | Offline behaviour checks, 27/27 pass | tracked |
| `src/step0_test_pull.py` | The test pull | tracked |
| `src/step0_watched_endpoint_probe.py` | Endpoint confirmation, username is an argument | tracked |
| `artifacts/step0-access-and-setup.md` | This document | tracked, public |
| `raw/…` | Probe responses | machine-local |
| `logs/api_requests.ndjson` | Every request | machine-local |
| `logs/blocked_endpoints.ndjson` | 403 evidence, created on first block | machine-local |
| `logs/throttle/budget.json` | Shared rate budget | machine-local |
| `logs/step0_test_pull.json`, `logs/step0_watched_endpoint_probe.json` | Run records | machine-local |
