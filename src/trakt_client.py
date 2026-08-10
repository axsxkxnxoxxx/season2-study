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
403         Hard stop and report (AccessBlocked). That is a block, not a
            throttle. Full response headers, including X-Private-User, are
            written to logs/ BEFORE raising, and the endpoint is recorded so a
            resumed run stops without re-requesting the blocked resource.
Pagination  A missing or non-integer pagination header is an error, never a
            silent stop. Accumulated items are reconciled against the reported
            item count and a short read is a failure, not data.
Logging     Status, the X-Ratelimit object, Retry-After, endpoint and method are
            logged for every request, not only rate-limit events.
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


# ---------------------------------------------------------------------------
# Exceptions. All of these stop the run.
# ---------------------------------------------------------------------------


class TraktClientError(Exception):
    """Base class for hard stops."""


class AccessBlocked(TraktClientError):
    """403. A block, not a throttle. Hard stop and report."""


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

        self._blocked = self._load_blocked()
        self._consecutive_429_pauses = 0
        self._total_429_pauses = 0
        self.counters = {
            "requests_sent": 0,
            "served_from_cache": 0,
            "ok": 0,
            "unavailable": 0,
            "transient_retries": 0,
            "rate_limit_pauses": 0,
            "stale_cache_entries": 0,
            "errors": 0,
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

    # -- blocked endpoints -------------------------------------------------

    def _load_blocked(self) -> set[str]:
        """Endpoints that previously returned 403. A resumed run must not
        request them again: repeatedly requesting into something that just
        blocked us is the stop-restart livelock this set exists to prevent.
        The hard stop is preserved; only the network call is skipped.
        Clear logs/blocked_endpoints.ndjson to retry a resolved block.
        """
        blocked: set[str] = set()
        if not self.blocked_log_path.exists():
            return blocked
        for line in self.blocked_log_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                blocked.add(json.loads(line)["endpoint"])
            except (ValueError, KeyError):
                continue
        return blocked

    def _record_block(
        self,
        endpoint: str,
        params: dict[str, Any],
        resp: requests.Response | None,
        xrl: Any,
        retry_after: float | None,
    ) -> str | None:
        """Persist the whole 403 before raising, so the evidence survives the
        hard stop and a resumed run knows not to re-hit this endpoint.

        X-Private-User is the block-versus-private-profile disambiguation.
        Trakt advertises it in access-control-expose-headers.
        """
        headers = dict(resp.headers) if resp is not None else {}
        private_user = None
        for key, value in headers.items():
            if key.lower() == "x-private-user":
                private_user = value
                break
        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "run": self.run_label,
            "event": "hard_stop_403",
            "method": "GET",
            "endpoint": endpoint,
            "params": params,
            "status": 403,
            "x_private_user": private_user,
            "x_ratelimit": xrl,
            "retry_after": retry_after,
            "response_headers": headers,
            "body_excerpt": (resp.text[:500] if resp is not None else None),
        }
        line = json.dumps(self._redact(record), sort_keys=True, default=str)
        self._refuse_if_secret(line, str(self.blocked_log_path))
        with self.blocked_log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        self._blocked.add(endpoint)
        return private_user

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
        elif meta.get("status") not in UNAVAILABLE_STATUSES:
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
                f"GET {endpoint} previously returned 403 and is recorded in "
                f"{self.blocked_log_path}. Not re-requested. The run stops here. "
                f"Inspect the recorded headers, including X-Private-User, then clear "
                f"that file to retry."
            )

        url = f"{API_BASE}/{endpoint.lstrip('/')}"
        pauses_for_this_request = 0
        transient_attempt = 0

        while True:
            self.throttle.wait_for_slot()
            resp = None
            err_kind = None
            err_detail = None
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

            # --- 403: a block, not a throttle. Record, then hard stop. -----
            if status == 403:
                self.counters["errors"] += 1
                private_user = self._record_block(endpoint, params, resp, xrl, retry_after)
                self._log({
                    "event": "hard_stop_403",
                    "method": "GET",
                    "endpoint": endpoint,
                    "status": 403,
                    "x_ratelimit": xrl,
                    "retry_after": retry_after,
                    "x_private_user": private_user,
                    "recorded_to": str(self.blocked_log_path),
                })
                raise AccessBlocked(
                    f"403 on GET {endpoint}. This is a block, not a throttle. Run "
                    f"stopped. X-Private-User={private_user!r} X-Ratelimit={xrl!r} "
                    f"Retry-After={retry_after!r}. Full headers written to "
                    f"{self.blocked_log_path}; this endpoint will not be re-requested."
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
                time.sleep(delay)
                continue

            # --- terminal outcomes ----------------------------------------
            # Consecutive counter resets on success, per the "several
            # consecutive pauses" rule in CLAUDE.md. The cumulative per-run
            # budget above does not reset, so alternation is still caught.
            self._consecutive_429_pauses = 0
            ok = 200 <= status < 300
            unavailable = status in UNAVAILABLE_STATUSES

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
                if page == 1 and resp.unavailable:
                    # Private or absent profile on the first page is the
                    # documented log-and-move-on case, not a truncation.
                    yield resp
                    return
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

        Returns (items, info). info['unavailable'] is True for a private or
        absent profile, which is the one non-error empty result.
        """
        items: list[Any] = []
        pages = 0
        unavailable = False
        for resp in self.get_paginated(endpoint, params, limit=limit):
            if resp.unavailable:
                unavailable = True
                break
            pages += 1
            items.extend(resp.data or [])
        return items, {"pages": pages, "items": len(items), "unavailable": unavailable}

    def summary(self) -> dict[str, int]:
        return dict(self.counters)


# Backwards-compatible alias: the throttle was in-memory only in the first cut.
SlidingWindowThrottle = SharedThrottle
