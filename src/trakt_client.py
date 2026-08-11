"""
Resumable, throttled Trakt API client for the Season 2 abandonment study.

Step 0 deliverable. The behavioural contract implemented here is the one written
in CLAUDE.md ("API discipline") and task-sheet.md (Step 0). CLAUDE.md is the
source of truth; if this docstring and CLAUDE.md ever disagree, CLAUDE.md wins.

Contract
--------
Auth        Client ID only, read from .env at runtime (TRAKT_CLIENT_ID).
            No OAuth flow. The Client ID is never written to a code file,
            a log, or an artifact. Log records and metadata are redacted, and
            a response body containing the Client ID is refused, not written.
Throttle    150 GET/minute against a documented ceiling of 200/minute (1000 per
            5 minutes, application level). The budget is held in a lock-
            protected file on disk, so it is shared by every process using this
            Client ID and it survives a restart. Never run at the ceiling.
Resume      Every response is persisted to raw/ before it is parsed. A request
            whose payload is already on disk is served from disk and is never
            re-requested. This includes negative outcomes (private profiles,
            404s). Cache entries carry a schema version; an entry written under
            an older schema is treated as stale rather than served forever.
Transient   Timeouts, connection errors and 5xx: retry with exponential
            backoff and jitter, bounded attempts.
429         Read Retry-After, pause that many seconds, resume. The same request
            is never retried in a loop. The run stops on several consecutive
            pauses, and also on a cumulative per-run budget, so an alternating
            429/200 pattern cannot hide sustained saturation.
403         Two cases, distinguished. A 403 on an *application-level* resource
            is a block: hard stop and report (AccessBlocked). A 403 on a *user*
            resource skips that user, is counted, and the run continues. Both
            write full response headers to logs/blocked_endpoints.ndjson BEFORE
            acting, and both record the endpoint so a resumed run does not
            re-request it. The skip path is bounded by two circuit breakers so
            an application-level block that first appears on a user endpoint
            cannot be absorbed as a long series of skips. See the "403" section
            below and artifacts/step0-access-and-setup.md §6 item 2.

            A skipped user is NOT the same object as a user with no history:
            it surfaces as TraktResponse.access_denied, as a distinct cache
            meta flag, and as outcome="access_denied" from fetch_all(). A
            caller can never mistake it for an empty 200.
Pagination  A missing or non-integer pagination header is an error, never a
            silent stop. Accumulated items are reconciled against the reported
            item count and a short read is a failure, not data.
Logging     Status, the X-Ratelimit object, Retry-After, endpoint and method are
            logged for every request, not only rate-limit events.

403: what is documented, what is inferred, what is assumed
---------------------------------------------------------
Amendment authorized by the Human Lead, 2026-08-10. CLAUDE.md as written says
"On a 403: hard stop and report." That is retained for application-level 403s
and narrowed for user resources, because under the unamended rule a single
private user would halt a multi-day unattended Step 4 pull.

No live 403 has ever been observed by this project. logs/api_requests.ndjson
holds 200s and transport errors only; no 401, 403 or 429. So the classifier
below rests on the following, labelled honestly:

DOCUMENTED  Trakt's published status-code table gives 403 one meaning:
            forbidden, i.e. invalid API key or unapproved application. It
            attaches no user-level meaning to 403. The documented status for a
            profile that is not visible to an app-only request is 401.
DOCUMENTED  X-Private-User exists and Trakt advertises it in
            access-control-expose-headers on every response captured so far
            (12 of 12).
OBSERVED    X-Private-User is emitted with a real value on GET /users/:id only
            (value "false" for a public profile). It was NOT emitted on any
            /users/:id/history or /users/:id/watched/shows response, which is
            the endpoint family Step 4 uses. Therefore ABSENCE OF THE HEADER
            CARRIES NO INFORMATION and cannot be read as "not a private user".
            This is why the header is used only as positive confirmation and is
            never the primary discriminator.
INFERRED    An application-level block is a property of the Client ID, not of
            one resource, so it would 403 every endpoint rather than one user.
            This is the warrant for both the path test and the streak breaker.
ASSUMED     That Trakt does not return 403, with no X-Private-User header, for
            a private profile on a history endpoint. If that assumption is
            wrong the skip path is the correct behaviour anyway; the cumulative
            tripwire exists to surface it to a human either way.

Decision procedure for a 403, in order:
  1. Endpoint is not a user resource        -> HARD STOP. An app-level block.
  2. X-Private-User present and false-like  -> HARD STOP. Trakt says this user
                                               is not private, so the refusal
                                               is not explained by privacy.
  3. X-Private-User present, unrecognised   -> HARD STOP. Do not guess.
  4. X-Private-User present and true-like   -> SKIP, confirmed private.
  5. User resource, header absent           -> SKIP, unconfirmed, and count it
                                               against both circuit breakers.

Circuit breakers on the skip path:
  A. MAX_CONSECUTIVE_USER_403 unconfirmed user-403s with no intervening 2xx
     -> HARD STOP. An app-level block 403s everything, so an intervening 2xx is
     evidence we are not blocked; only a 2xx resets the streak. Exposure after
     a real block that first appears on a user endpoint is therefore bounded at
     MAX_CONSECUTIVE_USER_403 requests, and no request is ever repeated.
  B. MAX_USER_403_PER_RUN in one run -> HARD STOP. Not a discriminator: a
     tripwire. Reaching it would mean 403-for-private-profile is real and
     common, which contradicts the documented model, and a human should see the
     evidence before thousands more calls are spent on that assumption.

Cost asymmetry, stated deliberately. Wrong in the permissive direction risks
the study's API access. Wrong in the strict direction costs wall-clock on an
unattended run but costs no API budget and no data, because every response is
already on disk and the run resumes where it stopped. That asymmetry is why
every ambiguous case above resolves to HARD STOP.
"""

from __future__ import annotations

import fcntl
import json
import hashlib
import os
import random
import re
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Documented constants. See artifacts/step0-access-and-setup.md.
# ---------------------------------------------------------------------------

API_BASE = "https://api.trakt.tv"
API_VERSION = "2"

# Bump when the shape of a cache meta record changes. Entries written under an
# older version are stale and are re-fetched rather than served forever.
SCHEMA_VERSION = 2

# Documented Trakt application-level ceiling: 1000 GET calls per 5 minutes.
DOCUMENTED_CEILING_PER_5_MIN = 1000
DOCUMENTED_CEILING_PER_MIN = 200

# What we actually run at. Below the ceiling, never at it. Application level,
# so this budget is shared across every process using the Client ID.
THROTTLE_PER_MIN = 150
THROTTLE_PER_5_MIN = 750

# Transient failure backoff.
TRANSIENT_MAX_ATTEMPTS = 5
TRANSIENT_BACKOFF_BASE_S = 2.0
TRANSIENT_BACKOFF_FACTOR = 2.0
TRANSIENT_BACKOFF_MAX_S = 60.0

# 429 handling.
MAX_429_PAUSES_PER_REQUEST = 2      # never retry the same request in a loop
MAX_CONSECUTIVE_429_PAUSES = 3      # several consecutive pauses: stop and report
MAX_429_PAUSES_PER_RUN = 6          # cumulative, never reset: catches 429/200 alternation
DEFAULT_RETRY_AFTER_S = 60.0
MAX_ACCEPTABLE_RETRY_AFTER_S = 900.0

REQUEST_TIMEOUT_S = 30.0

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "raw"
LOGS_DIR = PROJECT_ROOT / "logs"

# Status codes that mean "this user's data is not available to an app-only
# request". Trakt returns these for private profiles and for deleted accounts.
# They are recorded, not retried, and not re-requested.
UNAVAILABLE_STATUSES = (401, 404, 405, 423)

# --- 403 classification ----------------------------------------------------
# See the "403" section of the module docstring for the evidence behind these.

# A 403 is eligible to be treated as a user-level skip only if its endpoint is
# a user resource: "users/<id>" or "users/<id>/...". Everything else, including
# a bare "users" and the reserved segments below, hard stops.
USER_PATH_ROOT = "users"

# Segments that appear where a username would but are not a username. These are
# the authenticated-account endpoints; this study does not use them, and a 403
# on one of them is not a private third-party profile. Strict side on purpose.
RESERVED_USER_SEGMENTS = frozenset({
    "me", "settings", "requests", "hidden", "likes", "saved_filters", "follows",
})

# X-Private-User is a string header. Only these exact tokens are recognised; an
# unrecognised value hard stops rather than being guessed at.
PRIVATE_USER_TRUE = frozenset({"true", "1", "yes"})
PRIVATE_USER_FALSE = frozenset({"false", "0", "no"})

# Circuit breakers on the user-403 skip path.
MAX_CONSECUTIVE_USER_403 = 5    # unconfirmed user-403s with no intervening 2xx
MAX_USER_403_PER_RUN = 200      # cumulative tripwire, never resets

# Decisions returned by _classify_403.
DECISION_HARD_STOP = "hard_stop"
DECISION_SKIP_CONFIRMED = "skip_confirmed_private"
DECISION_SKIP_UNCONFIRMED = "skip_unconfirmed"
SKIP_DECISIONS = (DECISION_SKIP_CONFIRMED, DECISION_SKIP_UNCONFIRMED)


# ---------------------------------------------------------------------------
# Exceptions. All of these stop the run.
# ---------------------------------------------------------------------------


class TraktClientError(Exception):
    """Base class for hard stops."""


class AccessBlocked(TraktClientError):
    """An application-level 403. A block, not a throttle. Hard stop and report.

    Raised only for a 403 that the classifier could not attribute to a single
    user resource, and for a user-403 that tripped a circuit breaker.
    """


class UserAccessDenied(TraktClientError):
    """A user-resource 403 that arrived part-way through a multi-page pull.

    Not a hard stop: the run continues and the user is skipped. It is an
    exception rather than a return value because the pages already accumulated
    are a partial history, and a partial history is indistinguishable from a
    genuine "never started" once it reaches the analysis table. The caller must
    handle this explicitly; it can never be silently returned as data.
    """


class RateLimitPersistent(TraktClientError):
    """429s persisted beyond the configured budget. Stop and report."""


class MissingCredential(TraktClientError):
    """TRAKT_CLIENT_ID is not present in the environment or .env."""


class TransientFailure(TraktClientError):
    """Backoff attempts exhausted on a transient failure."""


class CredentialLeak(TraktClientError):
    """A write was about to put the Client ID on disk. Refused."""


class PaginationError(TraktClientError):
    """Pagination headers absent or unusable. A silent stop here would look
    like a genuine never-started at Step 4, so it is raised instead."""


class ShortRead(TraktClientError):
    """Accumulated items did not reconcile against the reported item count."""


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------


@dataclass
class TraktResponse:
    endpoint: str
    status: int
    ok: bool
    unavailable: bool          # private profile / not found: log and move on
    data: Any                  # parsed JSON, or None
    from_cache: bool
    raw_path: Path | None
    pagination: dict[str, Any] = field(default_factory=dict)
    # A user-resource 403 that was skipped rather than hard stopped. Kept as a
    # field of its own, never folded into `unavailable`, so that downstream code
    # can tell "we were refused access to this user" apart from both "this user
    # does not exist / is private per Trakt's documented 401" and "this user has
    # no history". All three are empty; only one of them is data.
    access_denied: bool = False


# ---------------------------------------------------------------------------
# Throttle: shared across processes, persisted across restarts
# ---------------------------------------------------------------------------


class SharedThrottle:
    """Rolling-window rate budget held in a lock-protected file.

    Trakt's limit is application level: it is a property of the Client ID, not
    of a process. An in-memory ring would let two sibling processes each claim
    150/min against a 200/min ceiling, and would forget everything on restart,
    allowing a burst before a crash plus a full burst after it. The ring
    therefore lives on disk under an exclusive flock, so all processes draw
    from one budget and a restart inherits the spend that already happened.

    Two windows are enforced before every outbound request: 60s capped at
    per_min, and 300s capped at per_5_min. Both sit below the documented
    ceiling and the constructor refuses a value at or above it.
    """

    STATE_VERSION = 1

    def __init__(
        self,
        per_min: int = THROTTLE_PER_MIN,
        per_5_min: int = THROTTLE_PER_5_MIN,
        state_dir: Path | None = None,
        log: Callable[[dict[str, Any]], None] | None = None,
    ):
        if per_min >= DOCUMENTED_CEILING_PER_MIN:
            raise ValueError("throttle must sit below the documented ceiling, never at it")
        if per_5_min >= DOCUMENTED_CEILING_PER_5_MIN:
            raise ValueError("throttle must sit below the documented ceiling, never at it")
        self.per_min = per_min
        self.per_5_min = per_5_min
        self.state_dir = Path(state_dir or (LOGS_DIR / "throttle"))
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.state_dir / "budget.json"
        self.lock_path = self.state_dir / "budget.lock"
        self._log = log or (lambda record: None)

    # -- lock --------------------------------------------------------------

    @contextmanager
    def _locked(self) -> Iterator[None]:
        """Exclusive across processes. Held only for the read-decide-write
        step, never while sleeping, so siblings are serialised at the decision
        and not at the wait."""
        with self.lock_path.open("a+") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    # -- state -------------------------------------------------------------

    def _load_locked(self, now: float) -> list[float]:
        """Read and prune the ring. Must be called under the lock.

        A missing file is a genuinely fresh budget and starts empty. An
        unreadable file is not: we cannot tell how much was already spent, so
        it is rewritten as a full window and the caller waits it out. These
        rules outrank speed.
        """
        if not self.state_path.exists():
            return []
        try:
            payload = json.loads(self.state_path.read_text(encoding="utf-8"))
            stamps = [float(t) for t in payload["stamps"]]
            if payload.get("version") != self.STATE_VERSION:
                raise ValueError("state version mismatch")
        except (ValueError, OSError, KeyError, TypeError) as exc:
            conservative = [now] * self.per_min
            self._save_locked(conservative)
            self._log({
                "event": "throttle_state_unreadable",
                "detail": str(exc)[:200],
                "action": "assumed a full window was already spent",
            })
            return conservative
        stamps = sorted(t for t in stamps if t >= now - 300.0)
        return stamps

    def _save_locked(self, stamps: list[float]) -> None:
        payload = {"version": self.STATE_VERSION, "stamps": stamps}
        tmp = self.state_path.with_suffix(".json.part")
        tmp.write_text(json.dumps(payload), encoding="utf-8")
        tmp.replace(self.state_path)

    def _wait_for(self, stamps: list[float], now: float) -> float:
        waits = []
        in_min = [t for t in stamps if t >= now - 60.0]
        if len(in_min) >= self.per_min:
            waits.append(in_min[-self.per_min] + 60.0 - now)
        if len(stamps) >= self.per_5_min:
            waits.append(stamps[-self.per_5_min] + 300.0 - now)
        return max(waits) if waits else 0.0

    # -- api ---------------------------------------------------------------

    def wait_for_slot(self, sleep: Callable[[float], Any] = time.sleep) -> float:
        """Block until a slot is free, then claim it. Returns seconds slept."""
        slept = 0.0
        while True:
            with self._locked():
                now = time.time()
                stamps = self._load_locked(now)
                wait = self._wait_for(stamps, now)
                if wait <= 0:
                    stamps.append(now)
                    self._save_locked(stamps)
                    return slept
            sleep(wait)
            slept += wait

    def note_external_pause(self, seconds: float) -> None:
        """A 429 pause already elapsed in wall-clock time, so the persisted
        ring prunes itself on the next read. Kept for call-site clarity."""
        with self._locked():
            now = time.time()
            self._save_locked(self._load_locked(now))

    def spent(self) -> dict[str, int]:
        """Current spend in each window. Diagnostics only."""
        with self._locked():
            now = time.time()
            stamps = self._load_locked(now)
        return {
            "last_60s": len([t for t in stamps if t >= now - 60.0]),
            "last_300s": len(stamps),
            "cap_60s": self.per_min,
            "cap_300s": self.per_5_min,
        }


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


def _load_client_id(env_path: Path | None = None) -> str:
    load_dotenv(dotenv_path=env_path or (PROJECT_ROOT / ".env"), override=False)
    client_id = os.environ.get("TRAKT_CLIENT_ID", "").strip()
    if not client_id:
        raise MissingCredential(
            "TRAKT_CLIENT_ID is not set. It must live in .env and be loaded at runtime."
        )
    return client_id


def _slug(part: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", part)[:120]


class TraktClient:
    def __init__(
        self,
        raw_dir: Path = RAW_DIR,
        logs_dir: Path = LOGS_DIR,
        run_label: str = "run",
        throttle: SharedThrottle | None = None,
        session: requests.Session | None = None,
        env_path: Path | None = None,
        max_consecutive_user_403: int = MAX_CONSECUTIVE_USER_403,
        max_user_403_per_run: int = MAX_USER_403_PER_RUN,
    ):
        self._client_id = _load_client_id(env_path)
        self.raw_dir = Path(raw_dir)
        self.logs_dir = Path(logs_dir)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.run_label = run_label
        self.request_log_path = self.logs_dir / "api_requests.ndjson"
        self.blocked_log_path = self.logs_dir / "blocked_endpoints.ndjson"

        self.throttle = throttle or SharedThrottle(
            state_dir=self.logs_dir / "throttle", log=self._log
        )
        self.session = session or requests.Session()

        self.max_consecutive_user_403 = max_consecutive_user_403
        self.max_user_403_per_run = max_user_403_per_run

        self._blocked, self._access_denied = self._load_403_index()
        self._consecutive_429_pauses = 0
        self._total_429_pauses = 0
        self._consecutive_user_403 = 0
        self._total_user_403 = 0
        self.counters = {
            "requests_sent": 0,
            "served_from_cache": 0,
            "ok": 0,
            "unavailable": 0,
            "transient_retries": 0,
            "rate_limit_pauses": 0,
            "stale_cache_entries": 0,
            "user_403_skipped": 0,
            "errors": 0,
            # Failure and sleep accounting. A caller that samples these before
            # and after a unit of work can say how much of its wall-clock time
            # was throttle, how much was a 429 pause, how much was backoff, and
            # how much was neither. Without that, a machine suspend and a
            # sustained throttle are the same number to a reader, and one of
            # those is a stall and the other is the system working.
            "http_5xx": 0,
            "transport_errors": 0,
            "throttle_sleep_seconds": 0.0,
            "rate_limit_sleep_seconds": 0.0,
            "backoff_sleep_seconds": 0.0,
            "request_seconds": 0.0,
        }

    # -- secret hygiene ----------------------------------------------------

    def _redact(self, value: Any) -> Any:
        if isinstance(value, str):
            return value.replace(self._client_id, "<REDACTED>")
        if isinstance(value, dict):
            return {k: ("<REDACTED>" if k.lower() in {"trakt-api-key", "authorization"}
                        else self._redact(v)) for k, v in value.items()}
        if isinstance(value, list):
            return [self._redact(v) for v in value]
        return value

    def _refuse_if_secret(self, text: str, destination: str) -> None:
        """A raise, not an assert: `python -O` strips asserts and this check
        must survive that. A Trakt Client ID is a 64-char hex string, so a
        substring match cannot plausibly be a false positive."""
        if len(self._client_id) >= 16 and self._client_id in text:
            raise CredentialLeak(
                f"refusing to write the Client ID to {destination}"
            )

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "trakt-api-version": API_VERSION,
            "trakt-api-key": self._client_id,
            "User-Agent": "season2-abandonment-study/0.1 (research; contact via repo)",
        }

    # -- logging -----------------------------------------------------------

    def _log(self, record: dict[str, Any]) -> None:
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run": self.run_label,
            **record,
        }
        line = json.dumps(self._redact(record), sort_keys=True, default=str)
        self._refuse_if_secret(line, str(self.request_log_path))
        with self.request_log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    @staticmethod
    def _ratelimit_object(resp: requests.Response | None) -> Any:
        """Trakt returns X-Ratelimit as a JSON object in a header, and in
        practice only on a 429."""
        if resp is None:
            return None
        raw = resp.headers.get("X-Ratelimit") or resp.headers.get("x-ratelimit")
        if not raw:
            return None
        try:
            return json.loads(raw)
        except (ValueError, TypeError):
            return raw

    @staticmethod
    def _retry_after(resp: requests.Response | None) -> float | None:
        if resp is None:
            return None
        raw = resp.headers.get("Retry-After")
        if raw is None:
            return None
        try:
            return float(raw)
        except (TypeError, ValueError):
            return None

    # -- 403 classification and evidence -----------------------------------

    @staticmethod
    def _is_user_resource(endpoint: str) -> bool:
        """True iff the endpoint addresses one named third-party user.

        "users/<id>" and "users/<id>/anything" qualify. A bare "users", any
        non-users path, and the reserved authenticated-account segments do not:
        a 403 on those cannot be one private profile, so it hard stops.
        """
        parts = [p for p in endpoint.strip("/").split("/") if p]
        if len(parts) < 2 or parts[0].lower() != USER_PATH_ROOT:
            return False
        return parts[1].lower() not in RESERVED_USER_SEGMENTS

    @staticmethod
    def _private_user_header(headers: dict[str, Any]) -> Any:
        for key, value in headers.items():
            if key.lower() == "x-private-user":
                return value
        return None

    def _classify_403(
        self, endpoint: str, headers: dict[str, Any]
    ) -> tuple[str, str, Any]:
        """Decide whether a 403 is an application-level block or one user.

        Returns (decision, reason, raw X-Private-User value). Every ambiguous
        case resolves to a hard stop; see the module docstring for what is
        documented, what is inferred and what is assumed. The circuit breakers
        are applied by the caller, not here, because they depend on run state.
        """
        raw = self._private_user_header(headers)
        token = raw.strip().lower() if isinstance(raw, str) else None

        if not self._is_user_resource(endpoint):
            return (
                DECISION_HARD_STOP,
                "403 on a non-user resource. An application-level block is a "
                "property of the Client ID, not of one profile, so this cannot "
                "be a private third-party user.",
                raw,
            )
        if token in PRIVATE_USER_FALSE:
            return (
                DECISION_HARD_STOP,
                "403 on a user resource with X-Private-User explicitly false. "
                "Trakt states this profile is not private, so the refusal is "
                "not explained by privacy and is treated as a block.",
                raw,
            )
        if token in PRIVATE_USER_TRUE:
            return (
                DECISION_SKIP_CONFIRMED,
                "403 on a user resource with X-Private-User true. Trakt's own "
                "statement that the profile is private. Skip this user.",
                raw,
            )
        if token is not None:
            return (
                DECISION_HARD_STOP,
                f"403 on a user resource with an unrecognised X-Private-User "
                f"value ({raw!r}). Not guessed at.",
                raw,
            )
        return (
            DECISION_SKIP_UNCONFIRMED,
            "403 on a user resource with X-Private-User absent. Absence is the "
            "observed norm on the history endpoints (0 of 11 non-profile "
            "responses carried it), so it is not evidence either way. Skipped "
            "under the consecutive and cumulative circuit breakers.",
            raw,
        )

    def _load_403_index(self) -> tuple[set[str], set[str]]:
        """Replay logs/blocked_endpoints.ndjson into two sets.

        Endpoints that previously hard stopped must not be requested again: a
        resumed run that re-requests into something that just blocked us is the
        stop-restart livelock this set exists to prevent. Endpoints that were
        skipped as a user-level 403 must not be re-requested either, but they
        do not stop the run.

        A legacy record with no `outcome` field is read as a hard stop. Every
        record written before this amendment was a hard stop, and the strict
        reading is the safe one. Clear the file to retry a resolved block.
        """
        blocked: set[str] = set()
        denied: set[str] = set()
        if not self.blocked_log_path.exists():
            return blocked, denied
        for line in self.blocked_log_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                record = json.loads(line)
                endpoint = record["endpoint"]
            except (ValueError, KeyError):
                continue
            if record.get("outcome") in SKIP_DECISIONS:
                denied.add(endpoint)
            else:
                blocked.add(endpoint)
        return blocked, denied

    def _record_403(
        self,
        endpoint: str,
        params: dict[str, Any],
        resp: requests.Response | None,
        xrl: Any,
        retry_after: float | None,
        decision: str,
        reason: str,
        private_user: Any,
    ) -> None:
        """Persist the whole 403 before acting on it.

        Written for BOTH branches, and written before the raise or the skip, so
        the evidence survives a hard stop and a skipped user is never silently
        dropped. logs/blocked_endpoints.ndjson is the existing convention for
        403 evidence and is extended rather than replaced: every record now
        carries `outcome` and `decision_reason`, and the file is now the
        authoritative index of both blocks and skips.
        """
        headers = dict(resp.headers) if resp is not None else {}
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run": self.run_label,
            "event": "hard_stop_403" if decision == DECISION_HARD_STOP else "user_403_skipped",
            "outcome": decision,
            "decision_reason": reason,
            "is_user_resource": self._is_user_resource(endpoint),
            "method": "GET",
            "endpoint": endpoint,
            "params": params,
            "status": 403,
            "x_private_user": private_user,
            "x_ratelimit": xrl,
            "retry_after": retry_after,
            "response_headers": headers,
            "body_excerpt": (resp.text[:500] if resp is not None else None),
            "consecutive_user_403": self._consecutive_user_403,
            "total_user_403_this_run": self._total_user_403,
        }
        line = json.dumps(self._redact(record), sort_keys=True, default=str)
        self._refuse_if_secret(line, str(self.blocked_log_path))
        with self.blocked_log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        if decision == DECISION_HARD_STOP:
            self._blocked.add(endpoint)
        else:
            self._access_denied.add(endpoint)

    def access_denied_endpoints(self) -> set[str]:
        """Endpoints skipped by a user-level 403, this run and every previous
        one recorded in the log. Step 4 reconciles its user list against this
        so a skipped user is accounted for, not missing."""
        return set(self._access_denied)

    # -- cache -------------------------------------------------------------

    def cache_paths(self, endpoint: str, params: dict[str, Any] | None) -> tuple[Path, Path]:
        """Deterministic on-disk location for one request.

        raw/<mirrored endpoint path>/<param hash>.json  (body)
        raw/<mirrored endpoint path>/<param hash>.meta.json (commit record)
        """
        clean = endpoint.strip("/")
        parts = [_slug(p) for p in clean.split("/") if p] or ["_root"]
        canonical = json.dumps(params or {}, sort_keys=True, separators=(",", ":"))
        digest = hashlib.sha1(canonical.encode("utf-8")).hexdigest()[:16]
        directory = self.raw_dir.joinpath(*parts)
        return directory / f"{digest}.json", directory / f"{digest}.meta.json"

    def _read_cache(self, body_path: Path, meta_path: Path, endpoint: str) -> TraktResponse | None:
        if not meta_path.exists():
            return None
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return None
        if meta.get("schema_version") != SCHEMA_VERSION:
            self.counters["stale_cache_entries"] += 1
            self._log({
                "event": "cache_stale",
                "method": "GET",
                "endpoint": endpoint,
                "status": None,
                "x_ratelimit": None,
                "retry_after": None,
                "entry_schema_version": meta.get("schema_version"),
                "current_schema_version": SCHEMA_VERSION,
                "action": "re-fetching, entry predates the current meta schema",
            })
            return None
        data = None
        if body_path.exists():
            try:
                data = json.loads(body_path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                return None
        elif meta.get("status") not in UNAVAILABLE_STATUSES and not meta.get("access_denied"):
            return None
        return TraktResponse(
            endpoint=meta.get("endpoint", endpoint),
            status=meta.get("status", 0),
            ok=bool(meta.get("ok")),
            unavailable=bool(meta.get("unavailable")),
            data=data,
            from_cache=True,
            raw_path=body_path if body_path.exists() else None,
            pagination=meta.get("pagination", {}) or {},
            # Absent on every entry written before the 403 amendment, and every
            # one of those was a 200, so the default is correct for them. This
            # is why the field was added without a SCHEMA_VERSION bump: a bump
            # would force a re-fetch of probe responses that approved artifacts
            # cite as evidence, and would change that evidence under them.
            access_denied=bool(meta.get("access_denied")),
        )

    def _write_cache(
        self,
        body_path: Path,
        meta_path: Path,
        endpoint: str,
        params: dict[str, Any] | None,
        status: int,
        ok: bool,
        unavailable: bool,
        text: str | None,
        headers: dict[str, Any],
        pagination: dict[str, Any],
        access_denied: bool = False,
    ) -> Any:
        """Persist raw to raw/ BEFORE parsing. Returns parsed JSON or None.

        Body first, meta second. The meta file is the commit record: nothing is
        served from cache without it, so a crash between the two writes leaves
        an orphan body that is simply re-fetched, never a half-read served as
        complete. Both writes are temp-file-then-rename.
        """
        body_path.parent.mkdir(parents=True, exist_ok=True)
        if text is not None and ok:
            self._refuse_if_secret(text, str(body_path))
            tmp = body_path.with_suffix(".json.part")
            tmp.write_text(text, encoding="utf-8")
            tmp.replace(body_path)
        meta = {
            "schema_version": SCHEMA_VERSION,
            "endpoint": endpoint,
            "method": "GET",
            "params": params or {},
            "status": status,
            "ok": ok,
            "unavailable": unavailable,
            "access_denied": access_denied,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "pagination": pagination,
            "x_ratelimit": headers.get("_x_ratelimit"),
            "retry_after": headers.get("_retry_after"),
            "response_headers": headers.get("_all") or {},
        }
        payload = json.dumps(self._redact(meta), sort_keys=True, default=str)
        self._refuse_if_secret(payload, str(meta_path))
        meta_tmp = meta_path.with_suffix(".json.part")
        meta_tmp.write_text(payload, encoding="utf-8")
        meta_tmp.replace(meta_path)

        if text is None or not ok:
            return None
        try:
            return json.loads(text)
        except ValueError:
            return None

    # -- the request -------------------------------------------------------

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        allow_unavailable: bool = True,
    ) -> TraktResponse:
        """One throttled, cached, resumable GET.

        Serves from raw/ when the request is already on disk. Otherwise waits
        for a throttle slot, sends, persists raw before parsing, and logs.
        """
        params = {k: v for k, v in (params or {}).items() if v is not None}
        body_path, meta_path = self.cache_paths(endpoint, params)

        cached = self._read_cache(body_path, meta_path, endpoint)
        if cached is not None:
            self.counters["served_from_cache"] += 1
            self._log({
                "event": "cache_hit",
                "method": "GET",
                "endpoint": endpoint,
                "status": cached.status,
                "retry_after": None,
                "x_ratelimit": None,
            })
            return cached

        if endpoint in self._blocked:
            self.counters["errors"] += 1
            self._log({
                "event": "blocked_endpoint_not_requested",
                "method": "GET",
                "endpoint": endpoint,
                "status": 403,
                "x_ratelimit": None,
                "retry_after": None,
            })
            raise AccessBlocked(
                f"GET {endpoint} previously returned an application-level 403 and is "
                f"recorded in {self.blocked_log_path}. Not re-requested. The run stops "
                f"here. Inspect the recorded headers, including X-Private-User, then "
                f"clear that file to retry."
            )

        if endpoint in self._access_denied:
            # Previously skipped as a user-level 403, and the cached body has
            # since been cleared. Do not re-request: requesting into a refusal
            # again is the behaviour the block rules exist to avoid. Return the
            # same access_denied outcome so the user stays counted and stays
            # distinguishable from a user with no history.
            self.counters["user_403_skipped"] += 1
            self._log({
                "event": "access_denied_endpoint_not_requested",
                "method": "GET",
                "endpoint": endpoint,
                "status": 403,
                "x_ratelimit": None,
                "retry_after": None,
                "recorded_in": str(self.blocked_log_path),
            })
            return TraktResponse(
                endpoint=endpoint, status=403, ok=False, unavailable=False,
                data=None, from_cache=True, raw_path=None, access_denied=True,
            )

        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        pauses_for_this_request = 0
        transient_attempt = 0

        while True:
            self.counters["throttle_sleep_seconds"] += (
                self.throttle.wait_for_slot() or 0.0
            )
            resp = None
            err_kind = None
            err_detail = None
            sent_at = time.time()
            try:
                self.counters["requests_sent"] += 1
                resp = self.session.get(
                    url, headers=self._headers(), params=params, timeout=REQUEST_TIMEOUT_S
                )
                status = resp.status_code
            except (requests.Timeout, requests.ConnectionError) as exc:
                err_kind = type(exc).__name__
                err_detail = str(exc)[:300]
                status = None
            except requests.RequestException as exc:
                err_kind = type(exc).__name__
                err_detail = str(exc)[:300]
                status = None
            self.counters["request_seconds"] += time.time() - sent_at
            if status is None:
                self.counters["transport_errors"] += 1
            elif 500 <= status < 600:
                self.counters["http_5xx"] += 1

            xrl = self._ratelimit_object(resp)
            retry_after = self._retry_after(resp)

            self._log({
                "event": "response" if status is not None else "transport_error",
                "method": "GET",
                "endpoint": endpoint,
                "params": params,
                "status": status,
                "x_ratelimit": xrl,
                "retry_after": retry_after,
                "error_kind": err_kind,
                "error_detail": err_detail,
            })

            # --- 403: block, or one user? Classify, record, then act. ------
            if status == 403:
                resp_headers = dict(resp.headers) if resp is not None else {}
                decision, reason, private_user = self._classify_403(endpoint, resp_headers)

                if decision in SKIP_DECISIONS:
                    self._total_user_403 += 1
                    if decision == DECISION_SKIP_UNCONFIRMED:
                        # Only unconfirmed 403s feed the streak. A confirmed
                        # private profile is positive evidence that Trakt is
                        # answering us normally, so it is not evidence of a
                        # block; it does not reset the streak either.
                        self._consecutive_user_403 += 1
                    if self._consecutive_user_403 >= self.max_consecutive_user_403:
                        decision = DECISION_HARD_STOP
                        reason = (
                            f"circuit breaker A: {self._consecutive_user_403} consecutive "
                            f"user-resource 403s with no intervening 2xx. An "
                            f"application-level block refuses every endpoint, so a run of "
                            f"user-403s uninterrupted by a success is treated as a block "
                            f"that first surfaced on a user endpoint, not as a run of "
                            f"private profiles."
                        )
                    elif self._total_user_403 >= self.max_user_403_per_run:
                        decision = DECISION_HARD_STOP
                        reason = (
                            f"circuit breaker B: {self._total_user_403} user-resource 403s "
                            f"in this run. Trakt documents 401, not 403, for a profile "
                            f"that is not visible to an app-only request, so 403 at this "
                            f"volume contradicts the documented model and a human must see "
                            f"the evidence before more calls are spent on it."
                        )

                self._record_403(
                    endpoint, params, resp, xrl, retry_after, decision, reason, private_user
                )
                self._log({
                    "event": "hard_stop_403" if decision == DECISION_HARD_STOP else "user_403_skipped",
                    "outcome": decision,
                    "decision_reason": reason,
                    "is_user_resource": self._is_user_resource(endpoint),
                    "method": "GET",
                    "endpoint": endpoint,
                    "params": params,
                    "status": 403,
                    "x_ratelimit": xrl,
                    "retry_after": retry_after,
                    "x_private_user": private_user,
                    "response_headers": resp_headers,
                    "consecutive_user_403": self._consecutive_user_403,
                    "total_user_403_this_run": self._total_user_403,
                    "recorded_to": str(self.blocked_log_path),
                })

                if decision == DECISION_HARD_STOP:
                    self.counters["errors"] += 1
                    raise AccessBlocked(
                        f"403 on GET {endpoint}. Treated as an application-level block, "
                        f"not a single user. Run stopped. Reason: {reason} "
                        f"X-Private-User={private_user!r} X-Ratelimit={xrl!r} "
                        f"Retry-After={retry_after!r}. Full headers written to "
                        f"{self.blocked_log_path}; this endpoint will not be re-requested."
                    )

                # Skip path: this user only, run continues. Persist the outcome
                # so a resumed run neither re-requests it nor loses the fact
                # that the user was refused rather than empty.
                self.counters["user_403_skipped"] += 1
                self._write_cache(
                    body_path, meta_path, endpoint, params, 403, False, False,
                    None,
                    {
                        "_x_ratelimit": xrl,
                        "_retry_after": retry_after,
                        "_all": resp_headers,
                    },
                    {},
                    access_denied=True,
                )
                return TraktResponse(
                    endpoint=endpoint, status=403, ok=False, unavailable=False,
                    data=None, from_cache=False, raw_path=None, access_denied=True,
                )

            # --- 429: pause exactly Retry-After, then resume. -------------
            if status == 429:
                self.counters["rate_limit_pauses"] += 1
                self._consecutive_429_pauses += 1
                self._total_429_pauses += 1
                pauses_for_this_request += 1
                pause = retry_after if retry_after is not None else DEFAULT_RETRY_AFTER_S

                if pause > MAX_ACCEPTABLE_RETRY_AFTER_S:
                    raise RateLimitPersistent(
                        f"429 on GET {endpoint} with Retry-After={pause}s, beyond the "
                        f"{MAX_ACCEPTABLE_RETRY_AFTER_S}s cap. Run stopped. X-Ratelimit={xrl!r}"
                    )
                if self._consecutive_429_pauses >= MAX_CONSECUTIVE_429_PAUSES:
                    raise RateLimitPersistent(
                        f"429s persisted across {self._consecutive_429_pauses} consecutive "
                        f"pauses (latest endpoint GET {endpoint}). Run stopped and reported "
                        f"rather than retried into a block. X-Ratelimit={xrl!r} "
                        f"Retry-After={retry_after!r}"
                    )
                if self._total_429_pauses >= MAX_429_PAUSES_PER_RUN:
                    raise RateLimitPersistent(
                        f"cumulative 429 budget exhausted: {self._total_429_pauses} pauses "
                        f"in this run (latest endpoint GET {endpoint}). Sustained saturation "
                        f"that alternates 429 and 200 never trips the consecutive counter, so "
                        f"this budget stops it. Run stopped. X-Ratelimit={xrl!r}"
                    )
                if pauses_for_this_request > MAX_429_PAUSES_PER_REQUEST:
                    raise RateLimitPersistent(
                        f"GET {endpoint} returned 429 after {pauses_for_this_request - 1} "
                        f"pauses. Refusing to retry the same request in a loop. Run stopped. "
                        f"X-Ratelimit={xrl!r} Retry-After={retry_after!r}"
                    )

                self._log({
                    "event": "rate_limit_pause",
                    "method": "GET",
                    "endpoint": endpoint,
                    "status": 429,
                    "x_ratelimit": xrl,
                    "retry_after": retry_after,
                    "pause_seconds": pause,
                    "consecutive_pauses": self._consecutive_429_pauses,
                    "total_pauses_this_run": self._total_429_pauses,
                })
                self.counters["rate_limit_sleep_seconds"] += pause
                time.sleep(pause)
                self.throttle.note_external_pause(pause)
                continue

            # --- transport error or 5xx: retry with backoff ---------------
            if status is None or 500 <= status < 600:
                transient_attempt += 1
                self.counters["transient_retries"] += 1
                if transient_attempt >= TRANSIENT_MAX_ATTEMPTS:
                    self.counters["errors"] += 1
                    raise TransientFailure(
                        f"GET {endpoint} failed {transient_attempt} times "
                        f"(last status={status}, error={err_kind}). Backoff exhausted."
                    )
                delay = min(
                    TRANSIENT_BACKOFF_BASE_S * (TRANSIENT_BACKOFF_FACTOR ** (transient_attempt - 1)),
                    TRANSIENT_BACKOFF_MAX_S,
                )
                delay += random.uniform(0, delay * 0.25)   # jitter
                self._log({
                    "event": "transient_backoff",
                    "method": "GET",
                    "endpoint": endpoint,
                    "status": status,
                    "x_ratelimit": xrl,
                    "retry_after": retry_after,
                    "attempt": transient_attempt,
                    "sleep_seconds": round(delay, 2),
                })
                self.counters["backoff_sleep_seconds"] += delay
                time.sleep(delay)
                continue

            # --- terminal outcomes ----------------------------------------
            # Consecutive counter resets on success, per the "several
            # consecutive pauses" rule in CLAUDE.md. The cumulative per-run
            # budget above does not reset, so alternation is still caught.
            self._consecutive_429_pauses = 0
            ok = 200 <= status < 300
            unavailable = status in UNAVAILABLE_STATUSES

            # Only a 2xx resets the user-403 streak. A 401 or 404 is not proof
            # that the application is unblocked, so it does not clear it: the
            # conservative reading costs at most a stopped run, which resumes
            # from disk at no API cost.
            if ok:
                self._consecutive_user_403 = 0

            pagination = {}
            if resp is not None:
                for header, key in (
                    ("X-Pagination-Page", "page"),
                    ("X-Pagination-Limit", "limit"),
                    ("X-Pagination-Page-Count", "page_count"),
                    ("X-Pagination-Item-Count", "item_count"),
                ):
                    val = resp.headers.get(header)
                    if val is not None:
                        try:
                            pagination[key] = int(val)
                        except ValueError:
                            pagination[key] = val

            data = self._write_cache(
                body_path, meta_path, endpoint, params, status, ok, unavailable,
                resp.text if resp is not None else None,
                {
                    "_x_ratelimit": xrl,
                    "_retry_after": retry_after,
                    "_all": dict(resp.headers) if resp is not None else {},
                },
                pagination,
            )

            if ok:
                self.counters["ok"] += 1
            elif unavailable:
                self.counters["unavailable"] += 1
                self._log({
                    "event": "unavailable_profile_or_resource",
                    "method": "GET",
                    "endpoint": endpoint,
                    "status": status,
                    "x_ratelimit": xrl,
                    "retry_after": retry_after,
                })
                if not allow_unavailable:
                    raise TraktClientError(f"GET {endpoint} returned {status}")
            else:
                self.counters["errors"] += 1

            return TraktResponse(
                endpoint=endpoint,
                status=status,
                ok=ok,
                unavailable=unavailable,
                data=data,
                from_cache=False,
                raw_path=body_path if ok else None,
                pagination=pagination,
            )

    # -- pagination --------------------------------------------------------

    @staticmethod
    def _require_int(pagination: dict[str, Any], key: str, endpoint: str) -> int:
        value = pagination.get(key)
        if not isinstance(value, int):
            raise PaginationError(
                f"GET {endpoint}: pagination header '{key}' is missing or not an "
                f"integer (got {value!r}; headers seen: {pagination!r}). Refusing to "
                f"stop silently: a truncated history is indistinguishable from a "
                f"genuine never-started once it reaches the analysis table."
            )
        return value

    def get_paginated(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        limit: int = 100,
        max_pages: int | None = None,
    ) -> Iterator[TraktResponse]:
        """Yield pages, strictly.

        Each page is cached separately, so an interrupted multi-page pull
        resumes at the first page not on disk.

        Missing or non-integer pagination headers raise. Accumulated items are
        reconciled against the reported item count and a mismatch raises. The
        reconciliation runs only if the generator is consumed to completion; a
        caller that breaks early, or passes max_pages, gets a logged
        truncation and no reconciliation.
        """
        page = 1
        total_items = 0
        declared_item_count: int | None = None
        page_count: int | None = None

        while True:
            page_params = dict(params or {})
            page_params.update({"page": page, "limit": limit})
            resp = self.get(endpoint, page_params)

            if not resp.ok:
                if page == 1 and (resp.unavailable or resp.access_denied):
                    # Private or absent profile on the first page is the
                    # documented log-and-move-on case, not a truncation. A
                    # user-level 403 on the first page is the same shape: no
                    # data was accumulated, so nothing can be truncated.
                    yield resp
                    return
                if resp.access_denied:
                    raise UserAccessDenied(
                        f"GET {endpoint}: page {page} returned a user-level 403 after "
                        f"{page - 1} successful page(s). The user is skipped and the run "
                        f"continues, but the {page - 1} page(s) already read are a partial "
                        f"history and are not returned as data: a truncated sweep is "
                        f"indistinguishable from a genuine never-started."
                    )
                raise PaginationError(
                    f"GET {endpoint}: page {page} returned HTTP {resp.status} after "
                    f"{page - 1} successful page(s). A partial multi-page read is a "
                    f"failure, not data."
                )

            if not isinstance(resp.data, list):
                raise PaginationError(
                    f"GET {endpoint}: page {page} returned {type(resp.data).__name__}, "
                    f"not a list. Item counts cannot be reconciled."
                )

            page_count = self._require_int(resp.pagination, "page_count", endpoint)
            declared_item_count = self._require_int(resp.pagination, "item_count", endpoint)
            total_items += len(resp.data)

            yield resp

            if max_pages is not None and page >= max_pages:
                self._log({
                    "event": "pagination_truncated_by_caller",
                    "method": "GET",
                    "endpoint": endpoint,
                    "status": resp.status,
                    "x_ratelimit": None,
                    "retry_after": None,
                    "pages_read": page,
                    "page_count": page_count,
                })
                return
            if page >= page_count:
                break
            page += 1

        if declared_item_count is not None and total_items != declared_item_count:
            raise ShortRead(
                f"GET {endpoint}: accumulated {total_items} items across {page} page(s) "
                f"but X-Pagination-Item-Count reported {declared_item_count}. Treating a "
                f"short read as a failure, not as data."
            )

        self._log({
            "event": "pagination_complete",
            "method": "GET",
            "endpoint": endpoint,
            "status": 200,
            "x_ratelimit": None,
            "retry_after": None,
            "pages_read": page,
            "items": total_items,
            "item_count_header": declared_item_count,
        })

    def fetch_all(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        limit: int = 100,
    ) -> tuple[list[Any], dict[str, Any]]:
        """Fully consume a paginated endpoint with reconciliation enforced.

        Returns (items, info). info['outcome'] is the field callers should
        branch on, and it has exactly three values:

          "complete"       a full, reconciled sweep. Only this one is data.
          "unavailable"    private or absent profile (Trakt's documented 401).
          "access_denied"  a user-level 403; the user was skipped.

        info['complete'] is True only for "complete". An empty items list with
        outcome "complete" means the user genuinely has no history; an empty
        items list under either other outcome means we never saw their history
        and must not be read as evidence about what they watched.

        A mid-sweep 403 is caught here rather than propagated, so an unattended
        run continues, but the pages already read are discarded rather than
        returned: partial history is not data. The pages stay in raw/, so a
        later retry is a resume, not a re-pull.
        """
        items: list[Any] = []
        pages = 0
        unavailable = False
        access_denied = False
        discarded_items = 0
        try:
            for resp in self.get_paginated(endpoint, params, limit=limit):
                if resp.unavailable:
                    unavailable = True
                    break
                if resp.access_denied:
                    access_denied = True
                    break
                pages += 1
                items.extend(resp.data or [])
        except UserAccessDenied as exc:
            access_denied = True
            discarded_items = len(items)
            items = []
            self._log({
                "event": "partial_sweep_discarded_on_user_403",
                "method": "GET",
                "endpoint": endpoint,
                "status": 403,
                "x_ratelimit": None,
                "retry_after": None,
                "pages_read_before_denial": pages,
                "items_discarded": discarded_items,
                "detail": str(exc)[:300],
            })

        complete = not (unavailable or access_denied)
        outcome = (
            "access_denied" if access_denied
            else "unavailable" if unavailable
            else "complete"
        )
        return items, {
            "pages": pages,
            "items": len(items),
            "unavailable": unavailable,
            "access_denied": access_denied,
            "complete": complete,
            "outcome": outcome,
            "discarded_items": discarded_items,
        }

    def summary(self) -> dict[str, int]:
        return dict(self.counters)


# Backwards-compatible alias: the throttle was in-memory only in the first cut.
SlidingWindowThrottle = SharedThrottle
