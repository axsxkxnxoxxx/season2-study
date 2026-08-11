# Step 0: Access and Setup

**Owner:** Analytics Engineer · **Mode:** Chained · **Reviewer:** Engineering
**Status:** Engineering verdict was proceed. Three blockers and four should-fixes
were authorized and are closed. The finding that blocked the Step 4 pull design is
**closed by the Human Lead, 2026-08-10** — see Section 0. The 403 ambiguity that would have
halted Step 4 on one private user is **closed by an authorized Human Lead amendment,
2026-08-10** — see Section 7.
**Dates:** first cut and Engineering review 2026-08-10; fixes and endpoint decision same day;
403 amendment same day.

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

**403:** classified, then acted on, after the evidence is persisted either way. An
application-level 403 is an immediate hard stop with no retry; a 403 on a single user
resource skips that user and the run continues, under two circuit breakers. See fix 2
and Section 7.

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
endpoint raises without a network call. To retry a resolved block, clear that file.
**Superseded in part by Section 7:** the record is now written for both branches of the
403 rule, not only for hard stops, and each record carries an `outcome` field.

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
API. **44 of 44 checks pass** (27 before the Section 7 amendment; 17 added by it).

| Group | Checks |
| :--- | :--- |
| Throttle | below ceiling; blocks at cap; survives restart; shared between siblings; unreadable state is conservative |
| 403, block branch | non-user resource hard stops and records full headers; reserved/bare `users` path hard stops; `X-Private-User: false` hard stops; unrecognised header value hard stops; resumed run does not re-request; legacy log record reads as a hard stop |
| 403, skip branch | `X-Private-User: true` skips and continues; header absent skips and continues; skipped user is not re-requested and stays `access_denied`; skip index survives a cleared cache; pre-amendment cache meta reads `access_denied` False |
| 403, circuit breakers | consecutive user 403s escalate; an intervening 2xx resets the streak; a 401 does not reset it; confirmed-private 403s do not trip breaker A; the cumulative budget stops the run |
| 403, completeness | a mid-sweep 403 never returns partial history; a skipped user is distinguishable from one with no history; a first-page 403 is move-on |
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
2. ~~**403 on a user endpoint remains ambiguous, by design.**~~ **CLOSED by the Human Lead,
   2026-08-10**, as an authorized amendment to the `CLAUDE.md` 403 rule, implemented before
   Step 4. See Section 7. A 403 on a **user resource** now skips that user, logs it with full
   headers, and continues; a 403 that indicates an **application-level block** still hard
   stops. `X-Private-User` is used where available. One private user can no longer halt a
   multi-day unattended pull.
3. **No Sabbath or wall-clock scheduling is built in**, and none was added here. Start
   and stop remain manual, per the task sheet.
4. **No live 429 or 403 has been observed.** Those paths are proven against a fake
   session only. Their first live exercise will be during Step 3 or Step 4. This is the
   standing caveat on Section 7: the 403 classifier has never met a real 403, which is why
   its inferences and assumptions are labelled as such and why every ambiguous case resolves
   to a hard stop.
5. **The throttle ring uses wall-clock time**, since it must be shared across processes
   and survive restarts. A backwards system-clock jump would make it over-cautious,
   never over-permissive. Flagging the direction of the failure, which is the safe one.

---

## 7. 403 handling: the two cases, separated

**Authorized amendment to the `CLAUDE.md` 403 rule, Human Lead, 2026-08-10.** Resolves
Section 6 open item 2 before Step 4. `CLAUDE.md` says "On a 403: hard stop and report."
That is retained for application-level 403s and narrowed for user resources, because under
the unamended rule **one private user halts a multi-day unattended pull**. `CLAUDE.md` is
the Human Lead's file and has not been edited by me; the text there and the behaviour here
now differ, and that divergence is flagged rather than resolved unilaterally.

### 7.1 The evidence this rule is built on

**No live 403 has ever been observed by this project.** `logs/api_requests.ndjson` holds
25 × 200 and 2 transport errors: no 401, no 403, no 429. So the classifier is stated
against labelled evidence rather than against expected behaviour.

| Claim | Standing | Basis |
| :--- | :--- | :--- |
| Trakt's published status table gives 403 one meaning: invalid API key or unapproved app. It attaches no user-level meaning to 403. | **Documented** | Trakt status-code table |
| The documented status for a profile not visible to an app-only request is **401**. | **Documented** | Trakt status-code table; already how the client treats 401 |
| `X-Private-User` exists and is advertised in `access-control-expose-headers`. | **Documented, and confirmed on 12 of 12 captured responses** | `raw/**/*.meta.json` |
| `X-Private-User` is emitted with a real value on `GET /users/:id` only (`false` for a public profile). | **Observed** | 1 of 12 captured responses |
| `X-Private-User` is **absent on every captured `/users/:id/history` and `/users/:id/watched/shows` response** — 0 of 11. | **Observed** | `raw/**/*.meta.json` |
| An application-level block is a property of the Client ID, so it would refuse every endpoint rather than one user. | **Inferred** | from the documented meaning of 403 |
| Trakt does not return 403-without-the-header for a private profile on a history endpoint. | **Assumed** | unobserved either way |

**The decisive observation is the fifth row.** `X-Private-User` is missing from the exact
endpoint family Step 4 uses, even on a 200 for a public user. So **absence of the header
carries no information** and cannot be read as "not a private user". Any rule that keys on
presence would misfire on essentially every real user 403. The header is therefore used
**only as positive confirmation**, never as the primary discriminator. The primary
discriminator is the endpoint path, backed by circuit breakers.

### 7.2 The rule as implemented

Applied in order, in `TraktClient._classify_403`:

| # | Condition | Decision |
| :-- | :--- | :--- |
| 1 | Endpoint is not a user resource | **HARD STOP** |
| 2 | User resource, `X-Private-User` present and false-like | **HARD STOP** — Trakt says this profile is not private, so the refusal is not explained by privacy |
| 3 | User resource, `X-Private-User` present but unrecognised | **HARD STOP** — not guessed at |
| 4 | User resource, `X-Private-User` true-like | **SKIP**, confirmed private |
| 5 | User resource, header absent (the expected live case) | **SKIP**, unconfirmed, counted against both breakers |

"User resource" means `users/<id>` or `users/<id>/...`. A bare `users`, any non-`users`
path, and the reserved authenticated-account segments (`me`, `settings`, `requests`,
`hidden`, `likes`, `saved_filters`, `follows`) are **not** user resources and hard stop.

Two circuit breakers bound the skip path:

- **A, consecutive.** 5 unconfirmed user-403s with no intervening 2xx → hard stop. An
  app-level block refuses everything, so an intervening 2xx is evidence we are not blocked;
  **only a 2xx resets the streak** — a 401 or 404 does not. Confirmed-private 403s neither
  increment nor reset it. Exposure after a real block that first surfaces on a user endpoint
  is therefore bounded at **5 requests**, and no request is ever repeated.
- **B, cumulative.** 200 user-403s in one run → hard stop. Not a discriminator, a tripwire:
  reaching it would mean 403-for-private is real and common, which contradicts the documented
  model, and a human should see the evidence before thousands more calls rest on it. Both
  limits are constructor arguments.

### 7.3 Where the rule misfires, in each direction

- **Too permissive.** If an app-level block returned 403 *only* on user endpoints and the
  pull kept receiving 2xx in between, breaker A would keep resetting and the block would be
  absorbed as skips until breaker B fired. Cost: up to 200 requests into a block. Judged
  unlikely, since a key-level block is not resource-scoped, but it is the residual risk and
  it is why breaker B exists at all.
- **Too strict.** If Trakt returns 403 with `X-Private-User: false` for some non-privacy
  user-level refusal — a deleted or suspended account, say — the run hard stops on one user.
  Cost: wall-clock until a human looks. Likewise a genuine cluster of five consecutive
  private users, plausible under the Channel A follower-graph crawl, trips breaker A.

**The asymmetry is deliberate.** Wrong in the permissive direction risks the study's API
access. Wrong in the strict direction costs wall-clock but **no API budget and no data**:
every response is already on disk and the run resumes exactly where it stopped. That is why
every ambiguous case resolves to a hard stop.

**Considered and rejected: a live canary.** On a user 403, issue one request to a global
endpoint; a 403 there proves an app-level block. It rests on the same unverified inference
as the path test, and breaker A extracts the same evidence from the pull's own traffic at no
extra call. Not built.

**Also rejected as a discriminator: the response body.** No 403 body has ever been captured,
and a key-level block may be served by the edge rather than the API, so body shape is
unverified. A 500-character excerpt is logged as evidence; nothing branches on it.

### 7.4 A skipped user is counted and recoverable, not dropped

Step 1 §0 makes sweep completeness a correctness requirement: a missing or truncated user is
indistinguishable from a genuine "never started" and lands in the headline. Four mechanisms
keep a skipped user distinguishable downstream:

1. **`TraktResponse.access_denied`** is its own field. It is never folded into `unavailable`
   and never into an empty 200.
2. **`fetch_all()` returns `outcome`** with exactly three values — `complete`, `unavailable`,
   `access_denied` — plus `complete: bool`. All three can carry zero items; only `complete`
   is data. An empty `complete` is a real user with no history. The other two are absence of
   evidence, not evidence of absence.
3. **The raw cache meta carries `access_denied: true`**, so the per-user state is on disk and
   survives a restart without consulting any log. A resumed run does not re-request the user
   and does not degrade the outcome to a fresh pull.
4. **`logs/blocked_endpoints.ndjson` is the index.** The existing 403-evidence convention is
   **extended, not replaced**: it now receives a record for *both* branches, each carrying
   `outcome` (`hard_stop` / `skip_confirmed_private` / `skip_unconfirmed`),
   `decision_reason`, `is_user_resource`, method, endpoint, status, full response headers,
   `X-Private-User`, `X-Ratelimit`, `Retry-After`, a body excerpt, and both breaker counters.
   `TraktClient.access_denied_endpoints()` reads it back. **Step 4 should reconcile its user
   list against it**: every discovered user must land in exactly one of parsed history,
   unavailable, access-denied, or error, and the four counts must sum to the users attempted.
   A legacy record with no `outcome` field is read as a hard stop, since every record written
   before this amendment was one.

A **mid-sweep** 403 is the sharpest case: pages 1–2 succeed, page 3 is refused. The pages
already read are a partial history, so `get_paginated` raises `UserAccessDenied` and
`fetch_all` **discards them** and reports `access_denied` with `discarded_items`. Partial
history is never returned as data. The pages stay in `raw/`, so a later retry is a resume
rather than a re-pull.

### 7.5 One consequence for the Human Lead to note

`CLAUDE.md` still reads "On a 403: hard stop and report. That is a block, not a throttle."
The client no longer behaves that way for user resources. **I have not edited `CLAUDE.md`** —
it is the Human Lead's file. If the amendment is to be the standing rule, that line needs
updating to match, and the Human Lead is the only one who can do it. Until then this section
is the operative description and the divergence is deliberate and recorded.

`SCHEMA_VERSION` was **not** bumped for the new `access_denied` meta field. The field is
absent on every pre-amendment cache entry and all of those are 200s, so the `False` default
is correct for them; bumping would force a re-fetch of the probe responses that
`artifacts/step0-history-endpoint-probe.md` and the `step1-outcome-definition.md` addendum
cite as evidence, changing that evidence underneath approved documents. A check pins the
default so the omission cannot rot silently.

---

## Files

| Path | Contents | Git |
| :--- | :--- | :--- |
| `src/trakt_client.py` | The client | tracked, no secrets |
| `src/test_client_behaviour.py` | Offline behaviour checks, 44/44 pass | tracked |
| `src/step0_test_pull.py` | The test pull | tracked |
| `src/step0_watched_endpoint_probe.py` | Endpoint confirmation, username is an argument | tracked |
| `artifacts/step0-access-and-setup.md` | This document | tracked, public |
| `raw/…` | Probe responses | machine-local |
| `logs/api_requests.ndjson` | Every request | machine-local |
| `logs/blocked_endpoints.ndjson` | 403 evidence, created on first block | machine-local |
| `logs/throttle/budget.json` | Shared rate budget | machine-local |
| `logs/step0_test_pull.json`, `logs/step0_watched_endpoint_probe.json` | Run records | machine-local |
