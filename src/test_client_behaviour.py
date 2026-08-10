"""
Offline behaviour checks for TraktClient.

Every path that matters is a path we must not exercise against the live API:
403 blocks, 429 pauses, 5xx backoff, throttle saturation, truncated pagination
and the cache. These run against a fake session with a fake credential, so they
cost zero real calls.

Run: .venv/bin/python src/test_client_behaviour.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ["TRAKT_CLIENT_ID"] = "FAKE_CLIENT_ID_FOR_OFFLINE_TESTS_0123456789abcdef"

import requests  # noqa: E402

from trakt_client import (  # noqa: E402
    AccessBlocked,
    CredentialLeak,
    PaginationError,
    RateLimitPersistent,
    SharedThrottle,
    ShortRead,
    TraktClient,
    TransientFailure,
    DOCUMENTED_CEILING_PER_MIN,
    SCHEMA_VERSION,
    THROTTLE_PER_MIN,
)

PASSED: list[str] = []


class _StopSleeping(Exception):
    """Sentinel so a test can inspect the first computed wait without looping."""


def check(name: str, fn) -> None:
    fn()
    PASSED.append(name)
    print(f"  pass  {name}")


class FakeResponse:
    def __init__(self, status_code, headers=None, text="[]"):
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text


class FakeSession:
    """Replays a scripted list of responses/exceptions and counts calls."""

    def __init__(self, script):
        self.script = list(script)
        self.calls = []

    def get(self, url, headers=None, params=None, timeout=None):
        self.calls.append((url, dict(params or {})))
        item = self.script.pop(0) if self.script else FakeResponse(200)
        if isinstance(item, Exception):
            raise item
        return item


def make_client(tmp: Path, script, no_throttle=True):
    client = TraktClient(
        raw_dir=tmp / "raw",
        logs_dir=tmp / "logs",
        run_label="offline-test",
        session=FakeSession(script),
    )
    if no_throttle:
        client.throttle.wait_for_slot = lambda: 0.0  # type: ignore[assignment]
    return client


def no_sleep():
    """Neutralise time.sleep inside the client for the duration of a block."""
    import trakt_client as tc

    class _Ctx:
        def __enter__(self):
            self.real = tc.time.sleep
            self.slept = []
            tc.time.sleep = lambda s: self.slept.append(s)  # type: ignore[assignment]
            return self

        def __exit__(self, *exc):
            tc.time.sleep = self.real  # type: ignore[assignment]
            return False

    return _Ctx()


def page_headers(page, page_count, item_count, limit=100):
    return {
        "X-Pagination-Page": str(page),
        "X-Pagination-Limit": str(limit),
        "X-Pagination-Page-Count": str(page_count),
        "X-Pagination-Item-Count": str(item_count),
    }


# ==========================================================================
# Throttle
# ==========================================================================


def t_throttle_below_ceiling():
    assert THROTTLE_PER_MIN < DOCUMENTED_CEILING_PER_MIN
    with tempfile.TemporaryDirectory() as d:
        try:
            SharedThrottle(per_min=DOCUMENTED_CEILING_PER_MIN, state_dir=Path(d))
        except ValueError:
            return
    raise AssertionError("throttle accepted a value at the documented ceiling")


def t_throttle_blocks_at_limit():
    with tempfile.TemporaryDirectory() as d:
        slept = []
        th = SharedThrottle(per_min=3, per_5_min=10, state_dir=Path(d))
        for _ in range(3):
            th.wait_for_slot(sleep=slept.append)
        assert slept == [], "throttle slept before the cap was reached"
        try:
            th.wait_for_slot(sleep=lambda s: (_ for _ in ()).throw(_StopSleeping(s)))
        except _StopSleeping as exc:
            assert exc.args[0] > 0, "throttle did not block on the 4th call"
            return
        raise AssertionError("throttle did not block on the 4th call")


def t_throttle_survives_restart():
    """A fresh client object must inherit spend it did not make itself."""
    with tempfile.TemporaryDirectory() as d:
        first = SharedThrottle(per_min=3, per_5_min=10, state_dir=Path(d))
        for _ in range(3):
            first.wait_for_slot(sleep=lambda s: None)
        restarted = SharedThrottle(per_min=3, per_5_min=10, state_dir=Path(d))
        assert restarted.spent()["last_60s"] == 3, "restart forgot the persisted ring"
        try:
            restarted.wait_for_slot(sleep=lambda s: (_ for _ in ()).throw(_StopSleeping(s)))
        except _StopSleeping:
            return
        raise AssertionError("restarted throttle allowed a burst on an empty ring")


def t_throttle_shared_between_siblings():
    """Two processes on one Client ID must draw from one budget, not two."""
    with tempfile.TemporaryDirectory() as d:
        a = SharedThrottle(per_min=4, per_5_min=20, state_dir=Path(d))
        b = SharedThrottle(per_min=4, per_5_min=20, state_dir=Path(d))
        a.wait_for_slot(sleep=lambda s: None)
        a.wait_for_slot(sleep=lambda s: None)
        b.wait_for_slot(sleep=lambda s: None)
        b.wait_for_slot(sleep=lambda s: None)
        assert a.spent()["last_60s"] == 4 and b.spent()["last_60s"] == 4
        try:
            b.wait_for_slot(sleep=lambda s: (_ for _ in ()).throw(_StopSleeping(s)))
        except _StopSleeping:
            return
        raise AssertionError("sibling claimed its own full budget against a shared ceiling")


def t_throttle_unreadable_state_is_conservative():
    with tempfile.TemporaryDirectory() as d:
        state = Path(d) / "budget.json"
        state.write_text("{ this is not json")
        th = SharedThrottle(per_min=5, per_5_min=20, state_dir=Path(d))
        try:
            th.wait_for_slot(sleep=lambda s: (_ for _ in ()).throw(_StopSleeping(s)))
        except _StopSleeping as exc:
            assert exc.args[0] > 55, f"expected a near-full-window wait, got {exc.args[0]}"
            # and the corrupt file must have been repaired, or we loop forever
            payload = json.loads(state.read_text())
            assert len(payload["stamps"]) == 5
            return
        raise AssertionError("unreadable throttle state was treated as a fresh budget")


# ==========================================================================
# 403
# ==========================================================================


def t_403_hard_stops_and_records_headers():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        headers = {
            "X-Ratelimit": '{"name":"UNAUTHED_API_GET_LIMIT"}',
            "X-Private-User": "true",
            "access-control-expose-headers": "X-Private-User",
        }
        c = make_client(tmp, [FakeResponse(403, headers, '{"error":"blocked"}')])
        try:
            c.get("users/redacted/watched/shows")
        except AccessBlocked:
            assert len(c.session.calls) == 1, "403 was retried"
            blocked_file = tmp / "logs" / "blocked_endpoints.ndjson"
            assert blocked_file.exists(), "403 raised before anything was written to logs/"
            rec = json.loads(blocked_file.read_text().splitlines()[0])
            assert rec["endpoint"] == "users/redacted/watched/shows"
            assert rec["x_private_user"] == "true", "X-Private-User not captured"
            assert rec["response_headers"]["access-control-expose-headers"]
            assert "hard_stop_403" in (tmp / "logs" / "api_requests.ndjson").read_text()
            return
        raise AssertionError("403 did not hard stop")


def t_403_endpoint_not_rerequested_on_resume():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        first = make_client(tmp, [FakeResponse(403, {"X-Private-User": "true"})])
        try:
            first.get("users/redacted/watched/shows")
        except AccessBlocked:
            pass
        # resumed run: same logs dir, new client, no scripted responses
        resumed = make_client(tmp, [FakeResponse(200, {}, "[]")])
        try:
            resumed.get("users/redacted/watched/shows")
        except AccessBlocked:
            assert len(resumed.session.calls) == 0, "resumed run re-requested a blocked endpoint"
            assert "blocked_endpoint_not_requested" in (
                tmp / "logs" / "api_requests.ndjson"
            ).read_text()
            return
        raise AssertionError("resumed run did not stop on a recorded block")


# ==========================================================================
# 429
# ==========================================================================


def t_429_pauses_then_resumes():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(429, {"Retry-After": "2", "X-Ratelimit": '{"name":"UNAUTHED_API_GET_LIMIT"}'}),
            FakeResponse(200, {}, '{"ok":true}'),
        ]
        c = make_client(tmp, script)
        with no_sleep() as s:
            r = c.get("shows/x")
        assert r.ok and r.data == {"ok": True}
        assert s.slept == [2.0], f"paused {s.slept}, expected exactly Retry-After"
        log = (tmp / "logs" / "api_requests.ndjson").read_text()
        assert "rate_limit_pause" in log
        assert "UNAUTHED_API_GET_LIMIT" in log, "X-Ratelimit object not logged"
        assert '"retry_after": 2.0' in log, "Retry-After not logged"


def t_429_consecutive_stops():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(429, {"Retry-After": "1"}) for _ in range(6)])
        with no_sleep():
            try:
                c.get("shows/x")
            except RateLimitPersistent:
                assert len(c.session.calls) <= 3, "retried the same request in a loop"
                return
        raise AssertionError("persistent 429s did not stop the run")


def t_429_alternating_trips_cumulative_budget():
    """429/200/429/200 never trips a consecutive counter. It must still stop."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = []
        for _ in range(12):
            script.append(FakeResponse(429, {"Retry-After": "1"}))
            script.append(FakeResponse(200, {}, "[]"))
        c = make_client(tmp, script)
        with no_sleep():
            try:
                for i in range(12):
                    c.get(f"shows/x{i}")
            except RateLimitPersistent as exc:
                assert "cumulative" in str(exc), f"stopped for the wrong reason: {exc}"
                assert c._consecutive_429_pauses <= 1, "consecutive counter was doing the work"
                return
        raise AssertionError("alternating 429/200 never stopped the run")


# ==========================================================================
# Transient
# ==========================================================================


def t_5xx_backoff_then_success():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(503),
            requests.ConnectionError("reset"),
            requests.Timeout("slow"),
            FakeResponse(200, {}, "[1,2,3]"),
        ]
        c = make_client(tmp, script)
        with no_sleep():
            r = c.get("shows/x")
        assert r.ok and r.data == [1, 2, 3]
        assert c.counters["transient_retries"] == 3


def t_5xx_backoff_exhausts():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(500) for _ in range(10)])
        with no_sleep():
            try:
                c.get("shows/x")
            except TransientFailure:
                return
        raise AssertionError("exhausted backoff did not raise")


# ==========================================================================
# Cache
# ==========================================================================


def t_cache_prevents_second_request():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, '{"a":1}')])
        first = c.get("shows/x", {"extended": "full"})
        assert first.ok and not first.from_cache
        second = c.get("shows/x", {"extended": "full"})
        assert second.from_cache, "second call was not served from disk"
        assert second.data == {"a": 1}
        assert len(c.session.calls) == 1, "re-requested what was already on disk"
        c.session.script = [FakeResponse(200, {}, '{"a":2}')]
        third = c.get("shows/x", {"extended": "metadata"})
        assert not third.from_cache and len(c.session.calls) == 2


def t_unavailable_is_cached_not_retried():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(401, {}, "")])
        r = c.get("users/redacted/history")
        assert r.unavailable and not r.ok
        assert c.counters["unavailable"] == 1
        r2 = c.get("users/redacted/history")
        assert r2.from_cache and r2.unavailable, "private profile was re-requested"
        assert len(c.session.calls) == 1
        assert "unavailable_profile_or_resource" in (
            tmp / "logs" / "api_requests.ndjson"
        ).read_text()


def t_raw_written_before_parse():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, "{not json")])
        r = c.get("shows/x")
        assert r.ok and r.data is None
        assert r.raw_path is not None and r.raw_path.exists()
        assert r.raw_path.read_text() == "{not json"


def t_meta_carries_schema_version():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, "[]")])
        c.get("shows/x")
        _, meta_path = c.cache_paths("shows/x", {})
        meta = json.loads(meta_path.read_text())
        assert meta["schema_version"] == SCHEMA_VERSION
        assert "response_headers" in meta


def t_stale_schema_entry_is_refetched_not_served():
    """The exact failure seen in Step 0: a meta written under an older schema
    must not be served forever."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, '{"v":"old"}')])
        c.get("shows/x")
        _, meta_path = c.cache_paths("shows/x", {})
        meta = json.loads(meta_path.read_text())
        del meta["schema_version"]
        meta.pop("response_headers", None)
        meta_path.write_text(json.dumps(meta))

        c2 = make_client(tmp, [FakeResponse(200, {"X-Test": "1"}, '{"v":"new"}')])
        r = c2.get("shows/x")
        assert not r.from_cache, "a stale-schema entry was served from cache"
        assert r.data == {"v": "new"}
        assert c2.counters["stale_cache_entries"] == 1
        assert "cache_stale" in (tmp / "logs" / "api_requests.ndjson").read_text()
        assert json.loads(meta_path.read_text())["schema_version"] == SCHEMA_VERSION


# ==========================================================================
# Secret hygiene
# ==========================================================================


def t_client_id_never_written_anywhere():
    """Scans every file written, bodies included, not just meta sidecars."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        cid = os.environ["TRAKT_CLIENT_ID"]
        c = make_client(tmp, [FakeResponse(200, {"X-Echo": cid}, '{"ok":1}')])
        c.get("shows/x")
        scanned = 0
        for path in tmp.rglob("*"):
            if path.is_file():
                scanned += 1
                body = path.read_text(encoding="utf-8", errors="replace")
                assert cid not in body, f"Client ID leaked into {path}"
        assert scanned >= 3, "scan covered too few files to mean anything"


def t_secret_in_response_body_is_refused():
    """Bodies are written verbatim, so the guard has to be in the write path,
    not in the redactor."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        cid = os.environ["TRAKT_CLIENT_ID"]
        c = make_client(tmp, [FakeResponse(200, {}, json.dumps({"echo": cid}))])
        try:
            c.get("shows/x")
        except CredentialLeak:
            body_path, _ = c.cache_paths("shows/x", {})
            assert not body_path.exists(), "leaking body was written before the refusal"
            return
        raise AssertionError("a response body containing the Client ID was accepted")


def t_secret_guard_survives_dash_O():
    """python -O strips asserts. The guard must be a raise."""
    import subprocess

    code = (
        "import sys; sys.path.insert(0, %r)\n"
        "import os; os.environ['TRAKT_CLIENT_ID']='X'*40\n"
        "from trakt_client import TraktClient, CredentialLeak\n"
        "import tempfile, pathlib\n"
        "d=tempfile.mkdtemp()\n"
        "c=TraktClient(raw_dir=pathlib.Path(d)/'raw', logs_dir=pathlib.Path(d)/'logs')\n"
        "try:\n"
        "    c._refuse_if_secret('X'*40, 'test')\n"
        "except CredentialLeak:\n"
        "    print('RAISED')\n"
    ) % str(Path(__file__).resolve().parent)
    out = subprocess.run(
        [sys.executable, "-O", "-c", code], capture_output=True, text=True
    )
    assert "RAISED" in out.stdout, f"guard did not survive -O: {out.stdout} {out.stderr}"


# ==========================================================================
# Pagination
# ==========================================================================


def t_pagination_walks_pages_and_resumes():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(200, page_headers(p, 3, 3), json.dumps([p])) for p in (1, 2, 3)
        ]
        c = make_client(tmp, script)
        pages = list(c.get_paginated("users/redacted/history", limit=100))
        assert [p.data for p in pages] == [[1], [2], [3]]
        c2 = make_client(tmp, [])
        pages2 = list(c2.get_paginated("users/redacted/history", limit=100))
        assert all(p.from_cache for p in pages2) and len(c2.session.calls) == 0


def t_missing_pagination_header_raises():
    """Both live Step 0 endpoints returned 200 with no pagination headers.
    That must be loud, not a silent single-page stop."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, "[1,2,3]")])
        try:
            list(c.get_paginated("users/redacted/history"))
        except PaginationError as exc:
            assert "page_count" in str(exc)
            return
        raise AssertionError("missing pagination headers stopped silently")


def t_non_integer_pagination_header_raises():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        headers = page_headers(1, 1, 1)
        headers["X-Pagination-Page-Count"] = "many"
        c = make_client(tmp, [FakeResponse(200, headers, "[1]")])
        try:
            list(c.get_paginated("users/redacted/history"))
        except PaginationError:
            return
        raise AssertionError("non-integer pagination header was accepted")


def t_short_read_raises():
    """The Step 4 nightmare: a truncated history that looks like never-started."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(200, page_headers(1, 2, 250), json.dumps(list(range(100)))),
            FakeResponse(200, page_headers(2, 2, 250), json.dumps(list(range(100)))),
        ]
        c = make_client(tmp, script)
        try:
            list(c.get_paginated("users/redacted/history", limit=100))
        except ShortRead as exc:
            assert "200" in str(exc) and "250" in str(exc)
            return
        raise AssertionError("a 200-of-250 short read was returned as data")


def t_mid_pull_failure_raises():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(200, page_headers(1, 3, 3), "[1]"),
            FakeResponse(404, {}, ""),
        ]
        c = make_client(tmp, script)
        try:
            list(c.get_paginated("users/redacted/history", limit=1))
        except PaginationError as exc:
            assert "page 2" in str(exc)
            return
        raise AssertionError("a mid-pull failure was treated as the end of the data")


def t_first_page_private_is_move_on_not_error():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(401, {}, "")])
        pages = list(c.get_paginated("users/redacted/history"))
        assert len(pages) == 1 and pages[0].unavailable


def t_fetch_all_reconciles():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(200, page_headers(1, 2, 5, limit=3), "[1,2,3]"),
            FakeResponse(200, page_headers(2, 2, 5, limit=3), "[4,5]"),
        ]
        c = make_client(tmp, script)
        items, info = c.fetch_all("users/redacted/history", limit=3)
        assert items == [1, 2, 3, 4, 5]
        assert info == {"pages": 2, "items": 5, "unavailable": False}


def main() -> int:
    print("offline behaviour checks")
    checks = [
        ("throttle sits below the documented ceiling", t_throttle_below_ceiling),
        ("throttle blocks once the per-minute cap is reached", t_throttle_blocks_at_limit),
        ("throttle survives restart, no post-crash burst", t_throttle_survives_restart),
        ("sibling processes share one budget", t_throttle_shared_between_siblings),
        ("unreadable throttle state is treated conservatively", t_throttle_unreadable_state_is_conservative),
        ("403 hard stops and records full headers incl. X-Private-User", t_403_hard_stops_and_records_headers),
        ("resumed run does not re-request a blocked endpoint", t_403_endpoint_not_rerequested_on_resume),
        ("429 pauses for Retry-After then resumes", t_429_pauses_then_resumes),
        ("consecutive 429s stop the run", t_429_consecutive_stops),
        ("alternating 429/200 trips the cumulative budget", t_429_alternating_trips_cumulative_budget),
        ("5xx and transport errors back off then succeed", t_5xx_backoff_then_success),
        ("exhausted backoff raises", t_5xx_backoff_exhausts),
        ("cache prevents a second request", t_cache_prevents_second_request),
        ("private/unavailable is recorded and not re-requested", t_unavailable_is_cached_not_retried),
        ("raw is written before parsing", t_raw_written_before_parse),
        ("cache meta carries a schema version", t_meta_carries_schema_version),
        ("stale-schema entry is re-fetched, not served forever", t_stale_schema_entry_is_refetched_not_served),
        ("Client ID reaches no file, bodies included", t_client_id_never_written_anywhere),
        ("a response body containing the Client ID is refused", t_secret_in_response_body_is_refused),
        ("the secret guard survives python -O", t_secret_guard_survives_dash_O),
        ("pagination walks pages and resumes from disk", t_pagination_walks_pages_and_resumes),
        ("missing pagination header raises", t_missing_pagination_header_raises),
        ("non-integer pagination header raises", t_non_integer_pagination_header_raises),
        ("short read raises instead of returning data", t_short_read_raises),
        ("mid-pull failure raises", t_mid_pull_failure_raises),
        ("private first page is move-on, not error", t_first_page_private_is_move_on_not_error),
        ("fetch_all reconciles item counts", t_fetch_all_reconciles),
    ]
    failures = []
    for name, fn in checks:
        try:
            check(name, fn)
        except Exception as exc:  # noqa: BLE001
            failures.append((name, exc))
            print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")
    print(f"\n{len(PASSED)}/{len(checks)} passed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
