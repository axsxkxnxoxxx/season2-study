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
    UserAccessDenied,
    DOCUMENTED_CEILING_PER_MIN,
    MAX_CONSECUTIVE_USER_403,
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
        # BaseException, not Exception: a scripted KeyboardInterrupt is how the
        # Ctrl-C paths are exercised, and KeyboardInterrupt is not an Exception.
        if isinstance(item, BaseException):
            raise item
        return item


def make_client(tmp: Path, script, no_throttle=True, **kwargs):
    client = TraktClient(
        raw_dir=tmp / "raw",
        logs_dir=tmp / "logs",
        run_label="offline-test",
        session=FakeSession(script),
        **kwargs,
    )
    if no_throttle:
        client.throttle.wait_for_slot = lambda: 0.0  # type: ignore[assignment]
    return client


def blocked_records(tmp: Path):
    path = tmp / "logs" / "blocked_endpoints.ndjson"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


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
# 403 — application-level block branch
#
# The rule these check is the Human Lead's amendment of 2026-08-10: a 403 on a
# user resource skips that user, a 403 that indicates an application-level
# block still hard stops. Every ambiguous case resolves to the hard stop.
# ==========================================================================


def t_403_on_non_user_resource_hard_stops_and_records_headers():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        headers = {
            "X-Ratelimit": '{"name":"UNAUTHED_API_GET_LIMIT"}',
            "access-control-expose-headers": "X-Private-User",
        }
        c = make_client(tmp, [FakeResponse(403, headers, '{"error":"blocked"}')])
        try:
            c.get("shows/breaking-bad/seasons")
        except AccessBlocked:
            assert len(c.session.calls) == 1, "403 was retried"
            recs = blocked_records(tmp)
            assert recs, "403 raised before anything was written to logs/"
            rec = recs[0]
            assert rec["endpoint"] == "shows/breaking-bad/seasons"
            assert rec["outcome"] == "hard_stop"
            assert rec["is_user_resource"] is False
            assert rec["response_headers"]["access-control-expose-headers"]
            assert rec["decision_reason"]
            assert "hard_stop_403" in (tmp / "logs" / "api_requests.ndjson").read_text()
            return
        raise AssertionError("an application-level 403 did not hard stop")


def t_403_on_reserved_user_segment_hard_stops():
    """`users/me/...` and `users/settings` are not third-party profiles, so a
    403 on them cannot be a private user. Also a bare `users`."""
    for endpoint in ("users/me/history", "users/settings", "users"):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            c = make_client(tmp, [FakeResponse(403, {}, "")])
            try:
                c.get(endpoint)
            except AccessBlocked:
                assert blocked_records(tmp)[0]["outcome"] == "hard_stop"
                continue
            raise AssertionError(f"403 on {endpoint} was treated as a skippable user")


def t_403_with_private_user_false_hard_stops():
    """Trakt says this profile is NOT private, yet refuses it. That is not
    explained by privacy, so it is treated as a block."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {"X-Private-User": "false"}, "")])
        try:
            c.get("users/redacted/history")
        except AccessBlocked as exc:
            assert "not explained by privacy" in str(exc)
            assert blocked_records(tmp)[0]["x_private_user"] == "false"
            return
        raise AssertionError("a contradicted 403 was skipped instead of stopping the run")


def t_403_with_unrecognised_private_user_value_hard_stops():
    """Do not guess at a header value we have never seen."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {"X-Private-User": "maybe"}, "")])
        try:
            c.get("users/redacted/history")
        except AccessBlocked as exc:
            assert "unrecognised" in str(exc)
            return
        raise AssertionError("an unrecognised X-Private-User value was guessed at")


def t_403_hard_stop_endpoint_not_rerequested_on_resume():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        first = make_client(tmp, [FakeResponse(403, {}, "")])
        try:
            first.get("shows/breaking-bad/seasons")
        except AccessBlocked:
            pass
        resumed = make_client(tmp, [FakeResponse(200, {}, "[]")])
        try:
            resumed.get("shows/breaking-bad/seasons")
        except AccessBlocked:
            assert len(resumed.session.calls) == 0, "resumed run re-requested a blocked endpoint"
            assert "blocked_endpoint_not_requested" in (
                tmp / "logs" / "api_requests.ndjson"
            ).read_text()
            return
        raise AssertionError("resumed run did not stop on a recorded block")


def t_legacy_403_record_without_outcome_is_read_as_hard_stop():
    """Every record written before the amendment was a hard stop. A legacy line
    has no `outcome` field, and the strict reading is the safe one."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        (tmp / "logs").mkdir(parents=True)
        (tmp / "logs" / "blocked_endpoints.ndjson").write_text(
            json.dumps({"event": "hard_stop_403", "endpoint": "users/redacted/history"}) + "\n"
        )
        c = make_client(tmp, [FakeResponse(200, {}, "[]")])
        try:
            c.get("users/redacted/history")
        except AccessBlocked:
            assert len(c.session.calls) == 0
            return
        raise AssertionError("a legacy 403 record was downgraded to a skip")


# ==========================================================================
# 403 — user-resource skip branch
# ==========================================================================


def t_403_on_user_resource_with_private_header_skips_and_continues():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        headers = {
            "X-Private-User": "true",
            "access-control-expose-headers": "X-Private-User",
            "X-Request-Id": "abc123",
        }
        c = make_client(tmp, [
            FakeResponse(403, headers, '{"error":"forbidden"}'),
            FakeResponse(200, {}, "[1,2]"),
        ])
        denied = c.get("users/redacted-a/history")
        assert denied.access_denied is True
        assert denied.ok is False
        assert denied.unavailable is False, "a skip must not masquerade as the 401 path"
        assert denied.data is None
        assert c.counters["user_403_skipped"] == 1

        # the run continues
        nxt = c.get("users/redacted-b/history")
        assert nxt.ok and nxt.data == [1, 2]

        rec = blocked_records(tmp)[0]
        assert rec["outcome"] == "skip_confirmed_private"
        assert rec["is_user_resource"] is True
        assert rec["x_private_user"] == "true"
        assert rec["response_headers"]["X-Request-Id"] == "abc123", "full headers not logged"
        assert rec["method"] == "GET" and rec["status"] == 403
        assert rec["decision_reason"]
        assert "user_403_skipped" in (tmp / "logs" / "api_requests.ndjson").read_text()


def t_403_on_user_resource_without_header_skips_and_continues():
    """The case the evidence says is the likely one: X-Private-User was absent
    on every captured history response, so a live 403 there probably carries no
    header either. Absence must not force a hard stop on one private user."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [
            FakeResponse(403, {"access-control-expose-headers": "X-Private-User"}, ""),
            FakeResponse(200, {}, "[1]"),
        ])
        denied = c.get("users/redacted-a/history")
        assert denied.access_denied and not denied.ok and not denied.unavailable
        assert c.get("users/redacted-b/history").ok, "run did not continue past a skip"
        rec = blocked_records(tmp)[0]
        assert rec["outcome"] == "skip_unconfirmed"
        assert rec["x_private_user"] is None
        assert rec["consecutive_user_403"] == 1


def t_skipped_user_is_not_rerequested_and_stays_access_denied():
    """Resume via the cache: the skip is on disk, so no network call, and the
    outcome that comes back is still access_denied, not an empty success."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {"X-Private-User": "true"}, "")])
        c.get("users/redacted/history")
        assert len(c.session.calls) == 1

        resumed = make_client(tmp, [FakeResponse(200, {}, "[1,2,3]")])
        again = resumed.get("users/redacted/history")
        assert len(resumed.session.calls) == 0, "a skipped user was re-requested"
        assert again.access_denied and again.from_cache
        assert again.data is None, "a skipped user came back carrying data"


def t_skipped_user_index_survives_a_cleared_cache():
    """Even with raw/ gone, the log is the index: no network call, and the
    access_denied outcome is preserved rather than degrading to a fresh pull."""
    import shutil

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {"X-Private-User": "true"}, "")])
        c.get("users/redacted/history")
        shutil.rmtree(tmp / "raw")

        resumed = make_client(tmp, [FakeResponse(200, {}, "[1,2,3]")])
        assert "users/redacted/history" in resumed.access_denied_endpoints()
        again = resumed.get("users/redacted/history")
        assert len(resumed.session.calls) == 0, "a skipped user was re-requested"
        assert again.access_denied and again.data is None
        assert resumed.counters["user_403_skipped"] == 1
        assert "access_denied_endpoint_not_requested" in (
            tmp / "logs" / "api_requests.ndjson"
        ).read_text()


def t_old_cache_meta_without_access_denied_reads_false():
    """The field was added without a SCHEMA_VERSION bump, because a bump would
    force a re-fetch of probe responses that approved artifacts cite. Every
    pre-amendment entry was a 200, so the default must be False."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(200, {}, "[1]")])
        c.get("shows/x")
        _, meta_path = c.cache_paths("shows/x", {})
        meta = json.loads(meta_path.read_text())
        del meta["access_denied"]
        meta_path.write_text(json.dumps(meta))

        c2 = make_client(tmp, [])
        r = c2.get("shows/x")
        assert r.from_cache and r.ok and r.access_denied is False
        assert len(c2.session.calls) == 0, "an unrelated entry was invalidated"


# ==========================================================================
# 403 — circuit breakers on the skip path
# ==========================================================================


def t_consecutive_user_403s_escalate_to_hard_stop():
    """An application-level block that first surfaces on a user endpoint must
    not be absorbed as an endless series of skips."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {}, "") for _ in range(20)])
        try:
            for i in range(20):
                c.get(f"users/redacted-{i}/history")
        except AccessBlocked as exc:
            assert "circuit breaker A" in str(exc)
            assert len(c.session.calls) == MAX_CONSECUTIVE_USER_403, (
                f"exposure after a block was {len(c.session.calls)} requests, "
                f"expected {MAX_CONSECUTIVE_USER_403}"
            )
            outcomes = [r["outcome"] for r in blocked_records(tmp)]
            assert outcomes[-1] == "hard_stop"
            assert outcomes.count("skip_unconfirmed") == MAX_CONSECUTIVE_USER_403 - 1
            return
        raise AssertionError("consecutive user 403s never escalated to a hard stop")


def t_intervening_success_resets_the_streak():
    """Scattered private users in a normal pull must never trip breaker A."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = []
        for _ in range(10):
            script.append(FakeResponse(403, {}, ""))
            script.append(FakeResponse(200, {}, "[1]"))
        c = make_client(tmp, script)
        for i in range(10):
            assert c.get(f"users/redacted-{i}/history").access_denied
            assert c.get(f"users/ok-{i}/history").ok
        assert c.counters["user_403_skipped"] == 10
        assert c._consecutive_user_403 == 0


def t_401_does_not_reset_the_streak():
    """A 401 is not proof the application is unblocked, so it must not clear
    the breaker. Only a 2xx does."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [FakeResponse(403, {}, "") for _ in range(3)]
        script.append(FakeResponse(401, {}, ""))
        script += [FakeResponse(403, {}, "") for _ in range(5)]
        c = make_client(tmp, script)
        try:
            for i in range(3):
                c.get(f"users/a{i}/history")
            assert c.get("users/private/history").unavailable
            for i in range(5):
                c.get(f"users/b{i}/history")
        except AccessBlocked as exc:
            assert "circuit breaker A" in str(exc)
            assert c._consecutive_user_403 == MAX_CONSECUTIVE_USER_403
            return
        raise AssertionError("a 401 reset the user-403 circuit breaker")


def t_confirmed_private_403s_do_not_trip_breaker_a():
    """Trakt explicitly saying `X-Private-User: true` is positive evidence that
    it is answering us normally, so those skips do not feed the streak."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {"X-Private-User": "true"}, "")
                              for _ in range(12)])
        for i in range(12):
            assert c.get(f"users/redacted-{i}/history").access_denied
        assert c.counters["user_403_skipped"] == 12
        assert c._consecutive_user_403 == 0


def t_cumulative_user_403_budget_stops_the_run():
    """Breaker B is a tripwire, not a discriminator: 403-for-private at volume
    contradicts the documented model and a human must see it."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = []
        for _ in range(30):
            script.append(FakeResponse(403, {"X-Private-User": "true"}, ""))
            script.append(FakeResponse(200, {}, "[1]"))
        c = make_client(tmp, script, max_user_403_per_run=6)
        try:
            for i in range(30):
                c.get(f"users/redacted-{i}/history")
                c.get(f"users/ok-{i}/history")
        except AccessBlocked as exc:
            assert "circuit breaker B" in str(exc)
            assert c._consecutive_user_403 == 0, "breaker A was doing the work"
            assert c._total_user_403 == 6
            return
        raise AssertionError("the cumulative user-403 budget never fired")


# ==========================================================================
# 403 — completeness of the sweep
# ==========================================================================


def t_mid_sweep_403_never_returns_partial_history():
    """The Step 1 §0 correctness requirement: a truncated sweep is
    indistinguishable from a genuine never-started, so partial is not data."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        script = [
            FakeResponse(200, page_headers(1, 3, 7, limit=3), "[1,2,3]"),
            FakeResponse(200, page_headers(2, 3, 7, limit=3), "[4,5,6]"),
            FakeResponse(403, {}, ""),
        ]
        c = make_client(tmp, script)
        try:
            list(c.get_paginated("users/redacted/history", limit=3))
        except UserAccessDenied as exc:
            assert "page 3" in str(exc)
        else:
            raise AssertionError("a mid-sweep 403 was treated as the end of the data")

        # fetch_all absorbs it so the run continues, but discards the partial.
        c2 = make_client(tmp, [FakeResponse(403, {}, "")])
        items, info = c2.fetch_all("users/redacted/history", limit=3)
        assert items == [], "a partial history was returned as data"
        assert info["outcome"] == "access_denied"
        assert info["complete"] is False
        assert info["discarded_items"] == 6
        assert info["pages"] == 2
        assert "partial_sweep_discarded_on_user_403" in (
            tmp / "logs" / "api_requests.ndjson"
        ).read_text()


def t_skipped_user_is_distinguishable_from_a_user_with_no_history():
    """Three empty results, three different outcomes. This is the property the
    headline number depends on."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [
            FakeResponse(200, page_headers(1, 1, 0), "[]"),   # genuinely empty
            FakeResponse(401, {}, ""),                        # private per docs
            FakeResponse(403, {}, ""),                        # refused
        ])
        empty = c.fetch_all("users/a/history")[1]
        private = c.fetch_all("users/b/history")[1]
        denied = c.fetch_all("users/c/history")[1]

        assert empty["outcome"] == "complete" and empty["complete"] is True
        assert private["outcome"] == "unavailable" and private["complete"] is False
        assert denied["outcome"] == "access_denied" and denied["complete"] is False
        assert len({empty["outcome"], private["outcome"], denied["outcome"]}) == 3
        assert empty["items"] == private["items"] == denied["items"] == 0, (
            "the three cases must be told apart by outcome, not by item count"
        )


def t_first_page_403_is_move_on_not_error():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [FakeResponse(403, {}, "")])
        pages = list(c.get_paginated("users/redacted/history"))
        assert len(pages) == 1 and pages[0].access_denied
        assert not pages[0].unavailable


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
        assert info == {
            "pages": 2,
            "items": 5,
            "unavailable": False,
            "access_denied": False,
            "skipped_too_long": False,
            "budget_exhausted": False,
            "discarded_over_tolerance": False,
            "complete": True,
            "outcome": "complete",
            "discarded_items": 0,
            "page_count_reported": 2,
            "item_count_reported": 5,
            "item_count_residual": 0,
            "accumulated_records": 5,
            "page_item_counts": [3, 2],
            "residual_tolerance": 0.0,
            "reconcile": "exact",
        }


# ==========================================================================
# Step 3 crawler. Added after engineering review returned HOLD on the first
# run. Each of these covers a defect that was found in production behaviour,
# so each is written to fail against the code as it was.
# ==========================================================================


def step3_env(tmp: Path):
    """Point the module's output directories at a temp tree."""
    import step3_user_discovery as s3

    class _Ctx:
        def __enter__(self):
            self.saved = (s3.LOGS_DIR, s3.ARTIFACTS, s3.RAW_STEP3)
            s3.LOGS_DIR = tmp / "logs"
            s3.ARTIFACTS = tmp / "artifacts"
            s3.RAW_STEP3 = tmp / "raw" / "step3"
            for path in (s3.LOGS_DIR, s3.ARTIFACTS, s3.RAW_STEP3):
                path.mkdir(parents=True, exist_ok=True)
            return s3

        def __exit__(self, *exc):
            s3.LOGS_DIR, s3.ARTIFACTS, s3.RAW_STEP3 = self.saved
            return False

    return _Ctx()


def step3_constants(**overrides):
    """Temporarily shrink the round sizes so a test round is a few calls.

    The stopping thresholds are never touched by this: only the per-round work
    sizes, and every test that cares asserts the thresholds separately.
    """
    import step3_user_discovery as s3

    class _Ctx:
        def __enter__(self):
            self.saved = {k: getattr(s3, k) for k in overrides}
            for k, v in overrides.items():
                setattr(s3, k, v)
            return s3

        def __exit__(self, *exc):
            for k, v in self.saved.items():
                setattr(s3, k, v)
            return False

    return _Ctx()


def seeded_crawler(tmp: Path, script, seeds=("alpha",), state_name="state"):
    """A crawler with its seeds planted directly, so a test does not have to
    script the comment feeds to reach the behaviour it is about."""
    import step3_user_discovery as s3

    client = make_client(tmp, script)
    crawler = s3.Step3Crawler(client, resume=False, state_dir=tmp / state_name)
    crawler.write_artifact = False
    for slug in seeds:
        crawler.users[slug] = {
            "username": slug, "trakt_id": None, "channel_first": "A",
            "in_a": True, "in_b": False, "edge": "seed", "depth": 0,
            "origin_seed": slug, "parent": None, "private": False,
            "deleted": False, "vip": False, "joined_at": None,
            "first_seen_round": 0, "seed_provenance": None, "lists_owned": [],
            "expansion": None, "screen": None,
        }
        crawler.seed_order.append(slug)
        crawler._enqueue_frontier(slug, 0, slug)
    crawler._journal = s3._RoundJournal()
    return crawler


def user_payload(slug):
    return json.dumps([{"user": {"username": slug, "ids": {"slug": slug, "trakt": 1}}}])


def stats_payload(episode_plays, movie_plays=0, include_total=False):
    body = {
        "movies": {"plays": movie_plays, "watched": movie_plays},
        "shows": {"watched": 5},
        "seasons": {},
        "episodes": {"plays": episode_plays, "watched": episode_plays},
        "network": {"followers": 1, "following": 1},
        "ratings": {"total": 0},
    }
    if include_total:
        body["total_plays"] = episode_plays + movie_plays
        body["progress"] = {"started": 1, "finished": 1, "dropped": 0}
    return json.dumps(body)


def t_step3_exit_code_is_nonzero_on_access_blocked():
    """`step3 && step4` must not read a 403 block as success."""
    import step3_user_discovery as s3

    for exc, expected in (
        (AccessBlocked("blocked"), s3.EXIT_ACCESS_BLOCKED),
        (RateLimitPersistent("saturated"), s3.EXIT_RATE_LIMIT_PERSISTENT),
        (TransientFailure("exhausted"), s3.EXIT_TRANSIENT_EXHAUSTED),
        (KeyboardInterrupt(), s3.EXIT_INTERRUPTED),
        (ValueError("bug"), s3.EXIT_UNEXPECTED),
    ):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            with step3_env(tmp) as mod:
                original_run = mod.Step3Crawler.run
                original_client = mod.TraktClient
                mod.TraktClient = lambda **kw: make_client(tmp, [])
                mod.Step3Crawler.run = lambda self: (_ for _ in ()).throw(exc)
                try:
                    code = mod.main(["--state-dir", str(tmp / "st")])
                finally:
                    mod.Step3Crawler.run = original_run
                    mod.TraktClient = original_client
                assert code == expected, f"{type(exc).__name__}: {code} != {expected}"


def t_step3_run_record_is_written_on_every_exit_path():
    """The old code skipped logs/step3_run.json entirely on TransientFailure,
    which is the exit where a reader most needs it."""
    import step3_user_discovery as s3

    for exc in (TransientFailure("exhausted"), ValueError("bug"), None):
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            with step3_env(tmp) as mod:
                original_run = mod.Step3Crawler.run
                original_client = mod.TraktClient
                mod.TraktClient = lambda **kw: make_client(tmp, [])
                if exc is None:
                    mod.Step3Crawler.run = lambda self: setattr(
                        self, "stop_reason", "done")
                else:
                    mod.Step3Crawler.run = lambda self: (_ for _ in ()).throw(exc)
                try:
                    mod.main(["--state-dir", str(tmp / "st")])
                finally:
                    mod.Step3Crawler.run = original_run
                    mod.TraktClient = original_client
                record = tmp / "logs" / "step3_run.json"
                assert record.exists(), f"no run record after {exc!r}"
                payload = json.loads(record.read_text())
                assert "exit_code" in payload and "counts" in payload


def t_step3_clean_stop_exits_zero():
    import step3_user_discovery as s3

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_env(tmp) as mod:
            original_run = mod.Step3Crawler.run
            original_client = mod.TraktClient
            mod.TraktClient = lambda **kw: make_client(tmp, [])
            mod.Step3Crawler.run = lambda self: setattr(
                self, "stop_reason", "budget: hit the Step 3 call cap")
            try:
                assert mod.main(["--state-dir", str(tmp / "st")]) == s3.EXIT_OK
            finally:
                mod.Step3Crawler.run = original_run
                mod.TraktClient = original_client


def t_step3_run_record_redacts_the_client_id():
    """logs/step3_run.json was the one write in the project that went out
    through a bare json.dumps with no credential guard."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_env(tmp) as mod:
            client = make_client(tmp, [])
            crawler = mod.Step3Crawler(client, resume=False, state_dir=tmp / "st")
            crawler.stop_reason = f"stopped while calling with key {client._client_id}"
            path = mod.write_run_record(crawler, client, None, 0)
            text = path.read_text()
            assert client._client_id not in text
            assert "<REDACTED>" in text


def t_step3_pool_write_is_atomic():
    """The old writer opened with "w", so a kill mid-write left a truncated
    file that is indistinguishable from a smaller complete pool."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [], seeds=("a", "b", "c"))
        crawler.write_pool()
        assert len(crawler.pool_path.read_text().splitlines()) == 3

        real_write = Path.write_text

        def explode(self, *args, **kwargs):
            if self.name.endswith(".part"):
                raise OSError("killed mid-write")
            return real_write(self, *args, **kwargs)

        crawler.users["d"] = dict(crawler.users["a"])
        Path.write_text = explode
        try:
            try:
                crawler.write_pool()
            except OSError:
                pass
        finally:
            Path.write_text = real_write
        lines = crawler.pool_path.read_text().splitlines()
        assert len(lines) == 3, f"truncated to {len(lines)} lines"
        for line in lines:
            json.loads(line)


def t_step3_deliverables_land_at_the_round_boundary():
    """Not in a finally. A SIGKILL must not be able to leave thousands of
    calls spent and no pool on disk."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_constants(EXPAND_USERS_PER_ROUND=1, LIST_PAGES_PER_ROUND=1,
                             SCREEN_CALLS_PER_ROUND=2, TARGET_USABLE=10 ** 9,
                             CALL_BUDGET=10 ** 9):
            crawler = seeded_crawler(tmp, [
                FakeResponse(200, {}, user_payload("kid")),
                FakeResponse(200, {}, "[]"),
                FakeResponse(200, {}, "[]"),
                FakeResponse(200, {}, stats_payload(500)),
                FakeResponse(200, {}, stats_payload(500)),
            ])
            crawler.max_rounds = 1
            crawler.run()
        assert crawler.pool_path.exists() and crawler.curve_path.exists()
        assert len(crawler.curve_path.read_text().splitlines()) == 1
        assert len(crawler.pool_path.read_text().splitlines()) >= 2


def t_step3_interrupted_round_is_discarded_whole():
    """A half-persisted round left users marked expanded whose followers were
    never read; resume never revisited them."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_constants(EXPAND_USERS_PER_ROUND=2, LIST_PAGES_PER_ROUND=1,
                             SCREEN_CALLS_PER_ROUND=2, TARGET_USABLE=10 ** 9,
                             CALL_BUDGET=10 ** 9):
            crawler = seeded_crawler(tmp, [
                FakeResponse(200, {}, user_payload("kid")),
                KeyboardInterrupt(),
            ], seeds=("alpha", "beta"))
            frontier_before = {k: list(v) for k, v in crawler.frontier.items()}
            users_before = set(crawler.users)
            try:
                crawler.run()
            except KeyboardInterrupt:
                pass
        assert crawler.expanded == set(), f"left expanded: {crawler.expanded}"
        assert set(crawler.users) == users_before, "a discarded round left users behind"
        assert {k: list(v) for k, v in crawler.frontier.items()} == frontier_before
        assert crawler.rounds == []
        assert len(crawler.discarded_rounds) == 1
        assert crawler.discarded_rounds[0]["reason"] == "KeyboardInterrupt"


def t_step3_user_is_expanded_only_after_both_edge_calls():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [
            FakeResponse(200, {}, user_payload("kid")),
            KeyboardInterrupt(),
        ])
        try:
            crawler.expand_channel_a(1)
        except KeyboardInterrupt:
            pass
        assert "alpha" not in crawler.expanded, (
            "marked expanded before its edges were read; resume would skip it")


def t_step3_403_expansion_is_not_a_zero_follower_user():
    """The conflation decisions/0004-403-handling.md exists to prevent,
    reintroduced at the discovery layer by a bare `continue`."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [
            FakeResponse(403, {"X-Private-User": "true"}, ""),   # alpha followers
            FakeResponse(403, {"X-Private-User": "true"}, ""),   # alpha following
            FakeResponse(200, {}, "[]"),                          # beta followers
            FakeResponse(200, {}, "[]"),                          # beta following
        ], seeds=("alpha", "beta"))
        stats = crawler.expand_channel_a(2)
        denied = crawler.users["alpha"]["expansion"]
        empty = crawler.users["beta"]["expansion"]
        assert denied["followers_outcome"] == "access_denied"
        assert denied["followers_returned"] is None
        assert denied["complete"] is False
        assert empty["followers_outcome"] == "ok"
        assert empty["followers_returned"] == 0
        assert empty["complete"] is True
        assert stats["expansions_access_denied"] == 2
        assert crawler.counts()["expansions_access_denied"] == 1


def t_step3_access_denied_counts_users_not_endpoints():
    """One user refused on followers, following and stats is one denied user,
    and a cache replay must not add another."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [
            FakeResponse(403, {"X-Private-User": "true"}, ""),
            FakeResponse(403, {"X-Private-User": "true"}, ""),
        ])
        crawler.expand_channel_a(1)
        assert crawler.access_denied_users == 1, crawler.access_denied_users
        assert crawler.access_denied_endpoint_hits == 2
        assert crawler.access_denied_live_hits == 2
        # Replay the same two endpoints from cache: still one user.
        crawler.expanded.clear()
        crawler._enqueue_frontier("alpha", 0, "alpha")
        crawler.expand_channel_a(1)
        assert crawler.access_denied_users == 1
        assert crawler.access_denied_live_hits == 2, "cache replays were counted as spend"


def t_step3_round_record_separates_a_plateau_from_a_stall():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_constants(EXPAND_USERS_PER_ROUND=1, LIST_PAGES_PER_ROUND=1,
                             SCREEN_CALLS_PER_ROUND=1, TARGET_USABLE=10 ** 9,
                             CALL_BUDGET=10 ** 9):
            crawler = seeded_crawler(tmp, [
                FakeResponse(200, {}, user_payload("kid")),
                FakeResponse(200, {}, "[]"),
                FakeResponse(200, {}, "[]"),
                FakeResponse(200, {}, stats_payload(500)),
            ])
            crawler.max_rounds = 1
            crawler.run()
        record = crawler.rounds[0]
        for field in ("channel_a_new_eligible", "channel_b_new_eligible",
                      "channel_a_yield_per_call", "channel_b_yield_per_call",
                      "frontier_size", "frontier_seeds_nonempty", "frontier_by_depth",
                      "expanded_this_round", "expanded_total", "neighbours_returned",
                      "neighbours_new", "neighbours_already_known",
                      "neighbour_dedup_rate", "lists_duplicate", "list_dedup_rate",
                      "rate_limit_pauses", "transient_retries",
                      "sleep_seconds_throttle", "sleep_seconds_rate_limit",
                      "sleep_seconds_backoff", "unaccounted_seconds",
                      "max_inter_request_gap_seconds", "stall_suspected",
                      "margin_above_trigger"):
            assert field in record, f"round record is missing {field}"
        assert record["channel_a_new_eligible"] == 1
        assert record["expanded_this_round"] == 1


def t_step3_stall_is_flagged_and_throttling_is_not():
    """2796 seconds with no 429 is a suspended machine, and the first run
    recorded it identically to 2796 seconds of throttling."""
    import step3_user_discovery as s3

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [])
        before = dict(crawler.client.counters)
        stalled = crawler._time_decomposition(2796.0, before)
        assert stalled["stall_suspected"] is True
        assert stalled["unaccounted_seconds"] > 2000

        crawler.client.counters["rate_limit_sleep_seconds"] += 2780.0
        crawler.client.counters["rate_limit_pauses"] += 3
        throttled = crawler._time_decomposition(2796.0, before)
        assert throttled["stall_suspected"] is False
        assert throttled["sleep_seconds_rate_limit"] == 2780.0
        assert throttled["unaccounted_seconds"] < s3.STALL_UNACCOUNTED_SECONDS


def t_step3_forecast_is_aggregated_and_not_based_on_a_missing_field():
    """users/:id/stats omits total_plays on 77 percent of payloads, so the old
    forecast divided a missing field read as zero and returned one page."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [
            FakeResponse(200, {}, stats_payload(1000, 250, include_total=False)),
            FakeResponse(200, {}, stats_payload(2000, 0, include_total=True)),
        ], seeds=("alpha", "beta"))
        crawler.screen(2)
        a = crawler.users["alpha"]["screen"]
        b = crawler.users["beta"]["screen"]
        assert a["stats_payload_variant"] == "reduced"
        assert a["total_plays_reported"] is None
        assert a["history_plays"] == 1250
        assert a["step4_pages_forecast"] == 5, a["step4_pages_forecast"]
        assert b["stats_payload_variant"] == "full"
        assert b["total_plays_reported"] == 2000
        assert b["step4_pages_forecast"] == 8
        forecast = crawler.step4_forecast()
        assert forecast["usable_users"] == 2
        assert forecast["total_pages"] == 13, forecast["total_pages"]
        assert forecast["max"] == 8 and forecast["min"] == 5
        assert forecast["mean_pages_per_user"] == 6.5
        assert forecast["extrapolated_to_target_usable"]["calls"] == 26000


def t_step3_full_edge_list_is_recorded_not_a_spanning_tree():
    """Keeping only the first parent leaves a tree, and a tree is acyclic by
    construction, so it cannot answer whether the pool is one clique."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [
            FakeResponse(200, {}, user_payload("shared")),   # alpha followers
            FakeResponse(200, {}, "[]"),
            FakeResponse(200, {}, user_payload("shared")),   # beta followers
            FakeResponse(200, {}, "[]"),
        ], seeds=("alpha", "beta"))
        crawler.expand_channel_a(2)
        crawler._flush_edges()
        edges = [json.loads(l) for l in crawler.edges_path.read_text().splitlines()]
        assert len(edges) == 2, edges
        assert {e["src"] for e in edges} == {"alpha", "beta"}
        assert crawler.users["shared"]["parent"] == "alpha"   # tree keeps one
        assert edges[0]["follower"] == "shared" and edges[0]["followee"] == "alpha"


def t_step3_seed_and_channel_b_provenance_are_recorded():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [FakeResponse(200, {}, json.dumps([{
            "list": {"ids": {"trakt": 7, "slug": "l"}, "item_count": 3,
                     "user": {"username": "owner", "ids": {"slug": "owner"}}},
        }]))])
        crawler.expand_channel_b(1)
        owned = crawler.users["owner"]["lists_owned"]
        assert len(owned) == 1
        assert owned[0]["list_id"] == 7
        assert owned[0]["feed"] in ("lists/trending", "lists/popular")
        crawler._record_user({"username": "s", "ids": {"slug": "s"}}, "A", "seed",
                             depth=0, origin_seed="s",
                             seed_provenance={"feed": "comments/recent/all/movies",
                                              "movie_trakt_id": 42, "page": 1})
        assert crawler.users["s"]["seed_provenance"]["movie_trakt_id"] == 42


def t_step3_artifact_refuses_usernames_but_not_ordinary_prose():
    """The guard has to be usable. A bare substring sweep fires on slugs like
    "any" and "sean" inside English words, and a check that always fires is a
    check that gets deleted."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [], seeds=("any", "sean", "longuserslug99"))
        clean = {"note": "seasonal viewers rarely finish any season",
                 "counts": {"users": 3}}
        assert crawler._names_present_in(clean) == []
        assert crawler._names_present_in({"pool": ["longuserslug99"]}) == ["longuserslug99"]
        assert crawler._names_present_in({"error": "GET users/sean/stats failed"}) == ["sean"]
        assert crawler._names_present_in({"channel": "any"}) == ["any"]


def t_step3_yield_curve_artifact_is_counts_only():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step3_env(tmp) as mod:
            crawler = seeded_crawler(tmp, [], seeds=("longuserslug99",))
            crawler.write_artifact = True
            path = crawler.write_yield_curve_artifact()
            text = path.read_text()
            assert "longuserslug99" not in text
            assert (tmp / "artifacts" / "step3-yield-curve.csv").exists()
            crawler.stop_reason = "stopped at users/longuserslug99/followers"
            try:
                crawler.write_yield_curve_artifact()
                raise AssertionError("wrote a username to artifacts/")
            except ValueError:
                pass


def t_step3_stopping_thresholds_are_unchanged():
    """Making the metrics honest is in scope. Changing what the run would
    decide is not. This pins the numbers the plan committed to."""
    import step3_user_discovery as s3

    assert s3.MIN_ROUNDS_BEFORE_PLATEAU == 10
    assert s3.PLATEAU_FRACTION_OF_PEAK == 0.20
    assert s3.PLATEAU_CONSECUTIVE_ROUNDS == 2
    assert s3.TARGET_USABLE == 4000
    assert s3.MIN_EPISODES_USABLE == 10
    assert s3.CALL_BUDGET == 6500
    assert s3.N_SEEDS == 300
    assert s3.MAX_DEPTH == 3
    assert s3.NEIGHBOURS_PER_USER == 100
    assert s3.STEP4_PAGE_LIMIT == 250


def t_step3_plateau_margin_is_reported_without_moving_the_rule():
    import step3_user_discovery as s3

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        crawler = seeded_crawler(tmp, [])
        crawler.rounds = [{"yield_per_discovery_call": y} for y in
                          [12.33, 4.48, 5.07, 7.96, 4.19, 2.70, 2.15, 4.78, 1.56, 2.19]]
        state = crawler.plateau_state()
        assert state["plateaued"] is False
        assert 0.22 < state["ratio_to_peak"] < 0.24
        assert state["margin_above_trigger"] == round(
            state["ratio_to_peak"] - 0.20, 4)
        # These are the real yields from rounds 1-10 of the first run. The
        # moving average never actually crossed the 0.20 trigger, so the count
        # of rounds below it is zero: the run came within about three
        # percentage points and then rebounded. That margin is the whole point
        # of reporting it, and it was invisible in the old round record.
        assert state["rounds_below_threshold_so_far"] == 0
        assert state["rounds_until_rule_is_eligible"] == 0
        assert 0.02 < state["margin_above_trigger"] < 0.04


def t_step3_backfill_replay_cannot_reach_the_network():
    import step3_backfill as bf

    session = bf.FrozenSession()
    try:
        session.get("https://api.trakt.tv/users/x/followers")
        raise AssertionError("the offline guard let a request through")
    except bf.OfflineViolation:
        pass


# ==========================================================================
# Step 4 history pull. decisions/0009 (stratified round-robin order),
# decisions/0010 (tail cap, both halves), resume and interrupt safety, and the
# per-user fetch timestamps D11 needs. Every one of these is a path that must
# not be discovered live on a multi-day unattended run.
# ==========================================================================


def step4_env(tmp: Path):
    """Point the module's output directories at a temp tree."""
    import step4_history_pull as s4

    class _Ctx:
        def __enter__(self):
            self.saved = (s4.LOGS_DIR, s4.ARTIFACTS_DIR, s4.PROCESSED_DIR)
            s4.LOGS_DIR = tmp / "logs"
            s4.ARTIFACTS_DIR = tmp / "artifacts"
            s4.PROCESSED_DIR = tmp / "processed"
            for path in (s4.LOGS_DIR, s4.ARTIFACTS_DIR, s4.PROCESSED_DIR):
                path.mkdir(parents=True, exist_ok=True)
            return s4

        def __exit__(self, *exc):
            s4.LOGS_DIR, s4.ARTIFACTS_DIR, s4.PROCESSED_DIR = self.saved
            return False

    return _Ctx()


def fake_pool(tmp: Path, users, name="pool.jsonl") -> Path:
    """users: iterable of (slug, forecast_pages[, usable])."""
    path = tmp / name
    lines = []
    for item in users:
        slug, forecast = item[0], item[1]
        usable = item[2] if len(item) > 2 else True
        lines.append(json.dumps({
            "slug": slug,
            "username": slug,
            "channel_first": "A",
            "in_a": True,
            "in_b": False,
            "screen": {
                "usable": usable,
                "reason": "ok" if usable else "below_episode_floor",
                "step4_pages_forecast": forecast,
                "stats_payload_variant": "reduced",
                "history_plays": forecast * 250,
            },
        }))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def history_page(page, page_count, item_count, limit=250, n=1, base_id=0):
    """A page of episode history records shaped like Trakt's."""
    records = []
    for i in range(n):
        records.append({
            "id": base_id + i,
            "watched_at": "2024-05-0%dT12:00:00.000Z" % ((i % 9) + 1),
            "action": "scrobble",
            "type": "episode",
            "episode": {"season": 1, "number": i + 1,
                        "ids": {"trakt": 900 + i}, "title": "ep"},
            "show": {"title": "Show", "year": 2020, "aired_episodes": 20,
                     "ids": {"trakt": 55, "slug": "show"}},
        })
    return FakeResponse(200, page_headers(page, page_count, item_count, limit=limit),
                        json.dumps(records))


def step4_puller(tmp: Path, script, pool, **kwargs):
    import step4_history_pull as s4

    client = make_client(tmp, script)
    return s4.Step4Puller(
        client,
        state_dir=tmp / "processed" / "step4",
        pool_path=pool,
        sabbath_window=None,
        **kwargs,
    )


# -- decisions/0009: the pull order ----------------------------------------


def t_step4_order_is_stratified_round_robin_and_deterministic():
    import step4_history_pull as s4

    users = [(f"u{i:03d}", i + 1) for i in range(100)]
    shuffled = list(reversed(users))
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        plan_a = s4.build_plan(s4.load_pool(fake_pool(tmp, users, "a.jsonl")))
        plan_b = s4.build_plan(s4.load_pool(fake_pool(tmp, shuffled, "b.jsonl")))
    order_a = [e["slug"] for e in plan_a["order"]]
    order_b = [e["slug"] for e in plan_b["order"]]
    assert order_a == order_b, "the order depends on input row order"
    assert sorted(order_a) == sorted(u[0] for u in users), "the order is not a permutation"
    assert plan_a["bin_sizes"] == [10] * 10
    # First cycle takes one user from each of the ten bins, cheapest first
    # within the cycle, so it spans the whole distribution immediately.
    first_cycle = [e["bin"] for e in plan_a["order"][:10]]
    assert first_cycle == list(range(10)), first_cycle


def t_step4_every_prefix_is_proportional_across_both_tails():
    import step4_history_pull as s4

    # Deliberately skewed, like the real pool: a long thin tail.
    users = [(f"u{i:04d}", 1 + (i * i) // 40) for i in range(400)]
    with tempfile.TemporaryDirectory() as d:
        plan = s4.build_plan(s4.load_pool(fake_pool(Path(d), users)))
    result = s4.verify_prefix_proportionality(plan)
    assert result["holds"], result
    assert result["max_spread_between_unexhausted_bins"] <= 1
    assert result["prefixes_checked"] == len(plan["order"])
    # The claim that matters: a short prefix already contains the heavy end.
    top_bin = plan["n_bins"] - 1
    assert any(e["bin"] == top_bin for e in plan["order"][:10])


def t_step4_real_pool_order_is_proportional():
    """The property is checked on the actual pool, not only on a fixture."""
    import step4_history_pull as s4

    if not s4.POOL_PATH.exists():
        return
    plan = s4.build_plan(s4.load_pool(s4.POOL_PATH))
    result = s4.verify_prefix_proportionality(plan)
    assert result["holds"], result
    assert plan["eligible_users"] + plan["skipped_forecast_users"] == plan["usable_users"]
    assert len(plan["order"]) == plan["eligible_users"]


# -- decisions/0010 (a): the forecast cap ----------------------------------


def t_step4_forecast_cap_never_starts_the_user():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("small", 1), ("huge", 301)])
            p = step4_puller(tmp, [history_page(1, 1, 1, n=1)], pool)
            assert [e["slug"] for e in p.plan["order"]] == ["small"]
            assert [e["slug"] for e in p.plan["over_cap"]] == ["huge"]
            p.run()
            rows = p.latest_outcomes()
            assert rows["huge"]["outcome"] == "skipped_length_forecast"
            assert rows["huge"]["live_calls"] == 0, "a capped user was requested"
            assert rows["huge"]["forecast_pages"] == 301
            assert "301" in rows["huge"]["detail"]
            # Not folded into anything else, and not an empty success.
            assert rows["huge"]["is_data"] is False
            assert rows["huge"]["outcome"] not in ("unavailable", "access_denied", "complete")
            assert "huge" not in {c[0].split("/")[1] for c in p.client.session.calls
                                  if "/users/" in c[0]}


def t_step4_a_user_at_exactly_the_cap_is_pulled():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("edge", 300)])
            p = step4_puller(tmp, [], pool)
            assert [e["slug"] for e in p.plan["order"]] == ["edge"], \
                "'exceeds 300' must be strict; a 300-page user is inside the cap"
            assert p.plan["over_cap"] == []


# -- decisions/0010 (b): the actual-pages guard ----------------------------


def t_step4_actual_pages_over_cap_discards_and_never_truncates():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("liar", 5)])
            # Forecast said 5 pages. The server says 400.
            script = [history_page(1, 400, 100000, n=250)]
            p = step4_puller(tmp, script, pool)
            p.run()
            row = p.latest_outcomes()["liar"]
            assert row["outcome"] == "skipped_length_actual", row
            assert row["records"] == 0
            assert row["parsed_path"] is None, "a discarded sweep left data behind"
            assert row["page_count_reported"] == 400
            assert row["forecast_pages"] == 5
            # One call to refuse a 400-page sweep, not 301.
            assert row["live_calls"] == 1, row["live_calls"]
            assert not list((tmp / "processed" / "step4" / "parsed").glob("*.gz"))
            # Distinct from every other not-data outcome.
            assert row["outcome"] not in ("unavailable", "access_denied",
                                          "skipped_length_forecast", "complete")
            assert row["is_data"] is False


def t_step4_a_sweep_that_grows_past_the_cap_is_discarded_whole():
    """The mis-forecast case 0010 (b) exists for, in its mid-sweep form: pages
    already read are thrown away and no parsed file survives."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("grower", 2)])
            script = [
                history_page(1, 2, 6, limit=3, n=3, base_id=0),
                history_page(2, 9, 27, limit=3, n=3, base_id=3),
            ]
            p = step4_puller(tmp, script, pool, page_cap=3, page_limit=3)
            p.run()
            row = p.latest_outcomes()["grower"]
            assert row["outcome"] == "skipped_length_actual", row
            assert row["items_discarded"] == 3, row
            assert row["records"] == 0 and row["parsed_path"] is None
            assert not list((tmp / "processed" / "step4" / "parsed").glob("*.gz"))


def t_step4_the_two_skip_counts_are_reported_separately():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("liar", 5), ("huge", 999), ("ok", 1)])
            script = [history_page(1, 400, 100000, n=250),
                      history_page(1, 1, 1, n=1)]
            p = step4_puller(tmp, script, pool)
            p.run()
            counts = p.counts()
            assert counts["skipped_length_forecast"] == 1
            assert counts["skipped_length_actual"] == 1
            assert counts["by_outcome"]["complete"] == 1
            assert counts["outcomes_sum_to_decided"]
            log = json.loads(s4.write_pull_log(p).read_text())
            assert log["skipped_length_forecast"] == 1
            assert log["skipped_length_actual"] == 1
            assert log["success"] == 1


def t_step4_page_cap_reuses_the_403_discard_path():
    """0010 (b) says reuse the mid-sweep discard built for 0004, not write a
    second one. Both must land in the same fetch_all discard branch and both
    must return zero items with a not-data outcome."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [
            FakeResponse(200, page_headers(1, 3, 7, limit=3), "[1,2,3]"),
            FakeResponse(403, {}, "forbidden"),
        ])
        items, info = c.fetch_all("users/x/history", limit=3)
        assert items == [] and info["outcome"] == "access_denied"
        assert info["discarded_items"] == 3

        c2 = make_client(tmp / "b", [history_page(1, 400, 100000, n=250)])
        items2, info2 = c2.fetch_all("users/y/history", limit=250, page_cap=300)
        assert items2 == [] and info2["outcome"] == "skipped_too_long"
        assert info2["page_count_reported"] == 400
        assert info2["complete"] is False

        # And the case where pages HAVE been accumulated before the bound
        # fires: the sweep grows under us, which is what happens when the user
        # logs a play mid-pull. Those pages must be thrown away, not handed
        # back. Without this the guard would truncate rather than discard.
        c3 = make_client(tmp / "c", [
            history_page(1, 2, 6, limit=3, n=3, base_id=0),
            history_page(2, 9, 27, limit=3, n=3, base_id=3),
        ])
        items3, info3 = c3.fetch_all("users/z/history", limit=3, page_cap=3)
        assert items3 == [], "a partial sweep was returned as data"
        assert info3["outcome"] == "skipped_too_long"
        assert info3["discarded_items"] == 3, info3
        assert info3["pages"] == 1


def t_step4_never_uses_the_truncating_bound():
    """max_pages truncates and hands back data. It must appear nowhere in the
    Step 4 pull, because a truncated sweep reads as a genuine never-started."""
    source = (Path(__file__).resolve().parent / "step4_history_pull.py").read_text()
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("*"):
            continue
        assert "max_pages" not in stripped, f"max_pages used in Step 4: {line}"


def t_step4_budget_stop_is_not_a_length_skip_and_is_not_terminal():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("big", 50)])
            script = [history_page(1, 50, 12000, n=250)]
            p = step4_puller(tmp, script, pool, max_calls=3)
            p.run()
            assert "big" not in p.latest_outcomes(), \
                "a user postponed for budget was recorded as decided"
            assert p.deferred_this_run and \
                p.deferred_this_run[0]["reason"].startswith("forecast exceeds")
            assert p.counts()["skipped_length_actual"] == 0


# -- resume, interrupt, and the ledger -------------------------------------


def t_step4_completed_user_is_not_re_requested():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 2)])
            script = [history_page(1, 2, 4, n=2, base_id=0),
                      history_page(2, 2, 4, n=2, base_id=2)]
            p = step4_puller(tmp, script, pool)
            p.run()
            assert p.latest_outcomes()["u"]["outcome"] == "complete"
            assert p.client.counters["requests_sent"] == 2

            # Second run, same state dir, a session that would raise if used.
            p2 = step4_puller(tmp, [], pool)
            p2.run()
            assert p2.client.counters["requests_sent"] == 0, \
                "a decided user was re-requested"
            assert p2.latest_outcomes()["u"]["outcome"] == "complete"


def t_step4_interrupt_between_parse_and_ledger_leaves_no_false_completion():
    """The Step 3 trap in its Step 4 form: never claim a user is done before
    the data for it is on disk, and never leave a claim without the data."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 1)])
            script = [history_page(1, 1, 2, n=2)]
            p = step4_puller(tmp, script, pool)

            real_append = p._append_ledger

            def die(row):
                raise KeyboardInterrupt

            p._append_ledger = die  # kill after the parsed file, before the row
            try:
                p.run()
            except KeyboardInterrupt:
                pass
            assert p.latest_outcomes() == {}, "an interrupted user looked decided"
            parsed = list((tmp / "processed" / "step4" / "parsed").glob("*.gz"))
            assert len(parsed) == 1, "the parsed file should already be on disk"
            first_bytes = parsed[0].read_bytes()

            # Resume: the user is redone, entirely from cache, and the parsed
            # file is byte-identical.
            p2 = step4_puller(tmp, [], pool)
            p2._append_ledger = real_append.__func__.__get__(p2)
            p2.run()
            assert p2.client.counters["requests_sent"] == 0
            assert p2.latest_outcomes()["u"]["outcome"] == "complete"
            assert parsed[0].read_bytes() == first_bytes


def t_step4_ledger_is_append_only_and_last_row_wins():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 1)])
            # First attempt is discarded over tolerance; second reconciles.
            p = step4_puller(tmp, [history_page(1, 1, 99, n=2)], pool)
            p.run()
            assert p.latest_outcomes()["u"]["outcome"] == "discarded_over_tolerance"
            lines_after_first = len(p.ledger_path.read_text().splitlines())

            p2 = step4_puller(tmp, [history_page(1, 1, 2, n=2)], pool,
                              retry_outcomes=["discarded_over_tolerance"])
            # The failed page is cached, so the retry must not be served the
            # stale body: clear that one cache entry the way a human would.
            body, meta = p2.client.cache_paths(
                "users/u/history", {"page": 1, "limit": 250})
            body.unlink()
            meta.unlink()
            p2.run()
            assert len(p2.ledger_path.read_text().splitlines()) > lines_after_first, \
                "the ledger was rewritten rather than appended to"
            assert p2.latest_outcomes()["u"]["outcome"] == "complete"
            # Both attempts really spent calls, so both are counted.
            assert p2.live_calls_recorded() == 2


def t_step4_live_call_ledger_cannot_be_reduced():
    """The Step 3 trap: an offline replay spends nothing, and the ledger is the
    only record of what was spent."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 1)])
            p = step4_puller(tmp, [history_page(1, 1, 2, n=2)], pool)
            p.run()
            assert p.live_calls_recorded() == 1
            recorded = json.loads(p.state_path.read_text())["live_calls_recorded"]
            assert recorded == 1

            # A fresh puller over the same state dir with an empty ledger is
            # exactly what a replay looks like.
            p2 = step4_puller(tmp, [], pool)
            p2.ledger_rows = []
            try:
                p2._save_state()
            except s4.LedgerRegression:
                pass
            else:
                raise AssertionError("state accepted a reduced live-call total")
            assert json.loads(p.state_path.read_text())["live_calls_recorded"] == 1


def t_step4_offline_run_refuses_the_canonical_state_dir():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        pool = fake_pool(tmp, [("u", 1)])
        client = make_client(tmp, [])
        try:
            s4.Step4Puller(client, state_dir=s4.STATE_DIR, pool_path=pool, offline=True)
        except s4.OfflineGuard:
            return
        raise AssertionError("an offline run was allowed into the canonical state dir")


# -- D11: per-user fetch timestamps ----------------------------------------


def t_step4_fetch_timestamps_come_from_disk_not_the_wall_clock():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 2)])
            script = [history_page(1, 2, 4, n=2, base_id=0),
                      history_page(2, 2, 4, n=2, base_id=2)]
            p = step4_puller(tmp, script, pool)
            p.run()
            row = p.latest_outcomes()["u"]
            assert row["first_page_fetched_at"] and row["last_page_fetched_at"]
            assert row["first_page_fetched_at"] <= row["last_page_fetched_at"]

            # Rewrite the meta on disk to a date that cannot be "now", then
            # redo the user from cache. The reported time must follow the disk.
            _, meta = p.client.cache_paths("users/u/history", {"page": 1, "limit": 250})
            payload = json.loads(meta.read_text())
            payload["fetched_at"] = "2001-01-01T00:00:00+00:00"
            meta.write_text(json.dumps(payload))

            p2 = step4_puller(tmp, [], pool, retry_errors=True)
            entry = p2.plan["order"][0]
            row2 = p2.pull_user(entry)
            assert row2["first_page_fetched_at"] == "2001-01-01T00:00:00+00:00", row2
            assert p2.counts()["earliest_first_page_fetched_at"] == \
                "2001-01-01T00:00:00+00:00"


# -- parsing ----------------------------------------------------------------


def t_step4_parsed_rows_keep_what_steps_5_7_and_8_need():
    import step4_history_pull as s4

    rows, stats = s4.parse_history([
        {"id": 1, "watched_at": "2024-01-02T03:04:05.000Z", "action": "scrobble",
         "type": "episode",
         "episode": {"season": 2, "number": 3, "ids": {"trakt": 77}, "title": "t"},
         "show": {"title": "S", "aired_episodes": 40, "ids": {"trakt": 5, "slug": "s"}}},
        {"id": 2, "watched_at": "2024-01-03T00:00:00.000Z", "action": "watch",
         "type": "movie", "movie": {"title": "M", "ids": {"trakt": 9}}},
        {"id": 1, "watched_at": "2024-01-02T03:04:05.000Z", "action": "scrobble",
         "type": "episode",
         "episode": {"season": 2, "number": 3, "ids": {"trakt": 77}},
         "show": {"ids": {"trakt": 5, "slug": "s"}}},
    ])
    assert rows[0] == {"id": 1, "watched_at": "2024-01-02T03:04:05.000Z",
                       "action": "scrobble", "type": "episode", "season": 2,
                       "number": 3, "episode_trakt": 77, "show_trakt": 5,
                       "show_slug": "s"}
    blob = json.dumps(rows)
    assert "aired_episodes" not in blob, "Step 1 §0 forbids show.aired_episodes"
    assert stats["episode_records"] == 2 and stats["movie_records"] == 1
    # Movies are kept: Step 7 liveness evidence is account-wide.
    assert rows[1]["type"] == "movie"
    # Duplicates are counted, never silently dropped: deduplication is a Step 8
    # definitional act, not a pull-time one.
    assert stats["duplicate_record_ids"] == 1 and len(rows) == 3
    assert stats["earliest_watched_at"] == "2024-01-02T03:04:05.000Z"


# -- errors and privacy -----------------------------------------------------


def t_step4_short_read_is_a_user_level_failure_not_a_run_stop():
    """Under the SUPERSEDED exact rule. Kept because the rule is still
    selectable and because a per-user failure must never stop the run."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("bad", 1), ("good", 1)])
            script = [history_page(1, 1, 99, n=2), history_page(1, 1, 2, n=2)]
            p = step4_puller(tmp, script, pool, reconcile="exact",
                             residual_tolerance=0.0)
            p.run()
            rows = p.latest_outcomes()
            assert rows["bad"]["outcome"] == "error_short_read"
            assert rows["good"]["outcome"] == "complete", "the run did not continue"
            assert rows["bad"]["is_data"] is False
            failures = (tmp / "logs" / "step4_failures.ndjson").read_text()
            assert "error_short_read" in failures


def t_step4_mid_sweep_403_stays_distinct_from_a_length_skip():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 3)])
            script = [history_page(1, 3, 7, n=3), FakeResponse(403, {}, "no")]
            p = step4_puller(tmp, script, pool)
            p.run()
            row = p.latest_outcomes()["u"]
            assert row["outcome"] == "access_denied"
            assert row["records"] == 0 and row["parsed_path"] is None
            assert row["items_discarded"] == 3


def t_step4_artifact_carries_no_usernames():
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("distinctiveslug1", 1)])
            p = step4_puller(tmp, [history_page(1, 1, 2, n=2)], pool)
            p.run()
            paths = s4.write_artifact(p, "unit")
            text = paths[0].read_text()
            assert "distinctiveslug1" not in text
            assert json.loads(text)["counts"]["by_outcome"]["complete"] == 1
            # And the guard actually fires when a name is present.
            try:
                s4.names_in({"who": "distinctiveslug1"}, {"distinctiveslug1"})
            except Exception:
                raise
            assert s4.names_in({"who": "distinctiveslug1"}, {"distinctiveslug1"}) \
                == ["distinctiveslug1"]


def t_step4_pagination_drift_is_caught_and_named():
    """A history that grows mid-sweep changes the headers. That is the direct
    mutation test; the item-count reconciliation was only an indirect one."""
    from trakt_client import PaginationDrift

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        c = make_client(tmp, [
            FakeResponse(200, page_headers(1, 3, 9, limit=3), "[1,2,3]"),
            FakeResponse(200, page_headers(2, 4, 10, limit=3), "[4,5,6]"),
        ])
        try:
            list(c.get_paginated("users/x/history", limit=3))
        except PaginationDrift as exc:
            assert "9" in str(exc) and "10" in str(exc)
        else:
            raise AssertionError("a history that moved mid-sweep was accepted")

        # Steady headers must NOT be read as drift.
        c2 = make_client(tmp / "b", [
            FakeResponse(200, page_headers(1, 2, 6, limit=3), "[1,2,3]"),
            FakeResponse(200, page_headers(2, 2, 6, limit=3), "[4,5,6]"),
        ])
        items, info = c2.fetch_all("users/y/history", limit=3)
        assert info["outcome"] == "complete" and len(items) == 6


def t_step4_adopted_completeness_rule_is_the_default():
    """decisions/0012, adopted 2026-08-11: page_count with a 2 percent residual
    tolerance IS the default. A run with no flags must use it.

    The client's own function default stays at the SUPERSEDED exact rule on
    purpose. 0012 amends decisions/0002 and Step 1 §0, which govern the history
    sweep; it does not speak for the follower and list endpoints Step 3 swept,
    whose evidence was gathered under exact. Exact is strictly the stricter of
    the two, so a caller that does not ask gets the stricter rule, and the
    adopted rule is applied deliberately at the layer 0012 governs."""
    import inspect

    import step4_history_pull as s4
    from trakt_client import TraktClient

    assert s4.COMPLETENESS_RULE == "page_count"
    assert s4.RESIDUAL_TOLERANCE == 0.02
    assert inspect.signature(s4.Step4Puller.__init__).parameters["reconcile"].default \
        == "page_count"
    assert inspect.signature(
        s4.Step4Puller.__init__).parameters["residual_tolerance"].default == 0.02
    # The library default is the stricter, superseded rule. Deliberate.
    assert inspect.signature(TraktClient.fetch_all).parameters["reconcile"].default \
        == "exact"
    assert inspect.signature(TraktClient.get_paginated).parameters["reconcile"].default \
        == "exact"

    parser_defaults = {}
    import argparse as _argparse

    real_parse = _argparse.ArgumentParser.parse_args

    def capture(self, argv=None, namespace=None):
        ns = real_parse(self, argv, namespace)
        parser_defaults.update(vars(ns))
        raise SystemExit(0)

    _argparse.ArgumentParser.parse_args = capture
    try:
        try:
            s4.main([])
        except SystemExit:
            pass
    finally:
        _argparse.ArgumentParser.parse_args = real_parse
    assert parser_defaults["completeness_rule"] == "page_count", parser_defaults
    assert parser_defaults["residual_tolerance"] == 0.02

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 1)])
            p = step4_puller(tmp, [], pool)
            assert p.reconcile == "page_count"
            assert p.residual_tolerance == 0.02
    for bad in ("loose", "", "page-count"):
        try:
            with tempfile.TemporaryDirectory() as d2:
                tmp2 = Path(d2)
                with step4_env(tmp2):
                    step4_puller(tmp2, [], fake_pool(tmp2, [("u", 1)]), reconcile=bad)
        except ValueError:
            continue
        raise AssertionError(f"an unknown completeness rule {bad!r} was accepted")


def t_step4_adopted_rule_tolerates_the_header_artefact_but_not_a_real_gap():
    """Under the adopted rule the pilot's observed residuals pass and a
    genuine gap still fails. Both halves matter: a rule that accepted anything
    would put a fabricated never-started in the headline."""
    from trakt_client import ResidualOutOfTolerance

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        # The real shape from the pilot: 1459 records against a header of 1460.
        c = make_client(tmp, [
            FakeResponse(200, page_headers(1, 2, 1460, limit=1000),
                         json.dumps(list(range(1000)))),
            FakeResponse(200, page_headers(2, 2, 1460, limit=1000),
                         json.dumps(list(range(1000, 1459)))),
        ])
        items, info = c.fetch_all("users/x/history", limit=1000,
                                  reconcile="page_count", residual_tolerance=0.02)
        assert info["outcome"] == "complete"
        assert len(items) == 1459
        assert info["item_count_residual"] == -1

        # A real half-missing sweep is discarded, and it is discarded WHOLE.
        c2 = make_client(tmp / "b", [
            FakeResponse(200, page_headers(1, 1, 1000, limit=1000),
                         json.dumps(list(range(400)))),
        ])
        items2, info2 = c2.fetch_all("users/y/history", limit=1000,
                                     reconcile="page_count", residual_tolerance=0.02)
        assert info2["outcome"] == "discarded_over_tolerance"
        assert info2["complete"] is False
        assert items2 == [], "a partial sweep was returned as data"
        assert info2["discarded_items"] == 400
        assert info2["item_count_residual"] == -600

        # get_paginated still raises, so no caller can consume it as a sweep.
        c3 = make_client(tmp / "c", [
            FakeResponse(200, page_headers(1, 1, 1000, limit=1000),
                         json.dumps(list(range(400)))),
        ])
        try:
            list(c3.get_paginated("users/z/history", limit=1000,
                                  reconcile="page_count", residual_tolerance=0.02))
        except ResidualOutOfTolerance as exc:
            assert "tolerance" in str(exc)
            assert isinstance(exc, ShortRead)
            return
        raise AssertionError("a 400-of-1000 sweep passed the adopted rule")


def t_step4_tolerance_boundary_is_exactly_two_percent():
    """The boundary is inclusive at the tolerance and fails just past it, and
    there is NO absolute floor: 0012 says 2 percent, so a residual of 1 on a
    21-record user is over tolerance and is discarded.

    The floor matters because an earlier draft had one, and it silently widened
    the rule to 4.8 percent on small histories."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        # 980 of 1000: residual -20, exactly 2.0 percent. Inclusive -> complete.
        at = make_client(tmp / "at", [
            FakeResponse(200, page_headers(1, 1, 1000, limit=1000),
                         json.dumps(list(range(980)))),
        ])
        _, info_at = at.fetch_all("users/a/history", limit=1000,
                                  reconcile="page_count", residual_tolerance=0.02)
        assert info_at["outcome"] == "complete", "the boundary is not inclusive"
        assert info_at["item_count_residual"] == -20

        # 979 of 1000: residual -21, 2.1 percent. Just past -> discarded.
        past = make_client(tmp / "past", [
            FakeResponse(200, page_headers(1, 1, 1000, limit=1000),
                         json.dumps(list(range(979)))),
        ])
        _, info_past = past.fetch_all("users/b/history", limit=1000,
                                      reconcile="page_count", residual_tolerance=0.02)
        assert info_past["outcome"] == "discarded_over_tolerance"

        # No absolute floor: 20 of 21 is 4.8 percent and is discarded.
        small = make_client(tmp / "small", [
            FakeResponse(200, page_headers(1, 1, 21, limit=1000),
                         json.dumps(list(range(20)))),
        ])
        _, info_small = small.fetch_all("users/c/history", limit=1000,
                                        reconcile="page_count", residual_tolerance=0.02)
        assert info_small["outcome"] == "discarded_over_tolerance", \
            "an absolute +/-1 floor has crept back in"

        # And the over-count direction is tested on the same boundary.
        over = make_client(tmp / "over", [
            FakeResponse(200, page_headers(1, 1, 1000, limit=1000),
                         json.dumps(list(range(1020)))),
        ])
        _, info_over = over.fetch_all("users/d/history", limit=1000,
                                      reconcile="page_count", residual_tolerance=0.02)
        assert info_over["outcome"] == "complete"
        assert info_over["item_count_residual"] == 20


def t_step4_over_tolerance_user_is_discarded_and_stays_distinguishable():
    """decisions/0012: the same treatment access_denied gets. Its own outcome,
    never folded into unavailable, never into a skip, never into an error, and
    never represented by an empty result. Only `complete` means the user
    watched nothing."""
    import step4_history_pull as s4

    assert "discarded_over_tolerance" in s4.TERMINAL_OUTCOMES
    assert "discarded_over_tolerance" not in s4.ERROR_OUTCOMES
    assert "discarded_over_tolerance" not in s4.DATA_OUTCOMES

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("bad", 1), ("empty", 1), ("good", 1)])
            script = [
                history_page(1, 1, 99, n=2),     # residual -97 on 99: discarded
                history_page(1, 1, 0, n=0),      # genuinely watched nothing
                history_page(1, 1, 2, n=2),      # ordinary complete user
            ]
            p = step4_puller(tmp, script, pool)
            p.run()
            rows = p.latest_outcomes()
            assert rows["bad"]["outcome"] == "discarded_over_tolerance"
            assert rows["empty"]["outcome"] == "complete"
            assert rows["good"]["outcome"] == "complete", "the run did not continue"

            # Discarded, not truncated: nothing partial was kept.
            assert rows["bad"]["is_data"] is False
            assert rows["bad"]["records"] == 0
            assert rows["bad"]["parsed_path"] is None
            assert rows["bad"]["items_discarded"] == 2
            assert not list((tmp / "processed" / "step4" / "parsed").glob("bad*"))

            # A zero-episode `complete` and a discard are not the same object.
            assert rows["empty"]["is_data"] is True
            assert rows["empty"]["records"] == 0

            # Counted on its own, and not inside any other bucket.
            counts = p.counts()
            assert counts["by_outcome"]["discarded_over_tolerance"] == 1
            assert counts["by_outcome"].get("unavailable", 0) == 0
            assert counts["by_outcome"].get("error_short_read", 0) == 0
            assert counts["by_outcome"].get("skipped_length_actual", 0) == 0
            log = json.loads((tmp / "logs" / "step4_pull_log.json").read_text()) \
                if (tmp / "logs" / "step4_pull_log.json").exists() else None
            log = log or json.loads(
                s4.write_pull_log(p, tmp / "logs" / "pl.json").read_text())
            assert log["discarded_over_tolerance"] == 1
            assert log["errors"] == 0
            assert log["private_or_absent"] == 0
            failures = (tmp / "logs" / "step4_failures.ndjson").read_text()
            assert "discarded_over_tolerance" in failures


def t_step4_three_way_classification_is_counted_separately():
    """decisions/0012 is explicit that the tolerance must not absorb three
    different phenomena. Header over-count, header under-count and genuine
    cross-page duplicate records are classified per user, counted separately,
    and NOT assumed mutually exclusive."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            # Residuals are kept small relative to the header on purpose: these
            # users are inside the 2 percent tolerance, which is the whole
            # point. The tolerance accepts them; the classification still has
            # to say which of the three things each one is.
            # Names are ordered so the deterministic pull order (forecast, then
            # slug) matches the scripted responses below.
            pool = fake_pool(tmp, [("a_over", 2), ("b_under", 2), ("c_dup", 2)])
            script = [
                # over-count: header claims 200, endpoint returns 199
                history_page(1, 2, 200, n=100, base_id=0),
                history_page(2, 2, 200, n=99, base_id=100),
                # under-count: header claims 200, endpoint returns 201
                history_page(1, 2, 200, n=100, base_id=1000),
                history_page(2, 2, 200, n=101, base_id=1100),
                # duplicate: ids 2098 and 2099 come back on BOTH pages, AND the
                # header under-counts, so this user is in two categories at once
                history_page(1, 2, 199, n=100, base_id=2000),
                history_page(2, 2, 199, n=100, base_id=2098),
            ]
            p = step4_puller(tmp, script, pool)
            p.run()
            rows = p.latest_outcomes()
            assert all(r["outcome"] == "complete" for r in rows.values())

            cls = {k: r["parse"]["classification"] for k, r in rows.items()}
            assert cls["a_over"]["header_over_count"] is True
            assert cls["a_over"]["header_under_count"] is False
            assert cls["a_over"]["residual_on_accumulated"] == -1
            assert cls["b_under"]["header_under_count"] is True
            assert cls["b_under"]["residual_on_accumulated"] == 1

            # The duplicate is CROSS-page and is reported as its own number.
            assert cls["c_dup"]["cross_page_duplicate_ids"] == 2
            assert cls["c_dup"]["cross_page_duplicate_records"] == 2
            assert cls["c_dup"]["accumulated_records"] == 200
            assert cls["c_dup"]["distinct_record_ids"] == 198
            # Not mutually exclusive: the same user is also a header case.
            assert cls["c_dup"]["header_under_count"] is True

            # The two residuals are different quantities and both are carried.
            assert cls["c_dup"]["residual_on_accumulated"] == 1
            assert cls["c_dup"]["residual_on_distinct_ids"] == -1
            assert cls["c_dup"]["residual_basis"] == "accumulated_records"

            agg = p.classification_counts()
            assert agg["header_over_count"]["users"] == 1
            assert agg["header_under_count"]["users"] == 2
            assert agg["cross_page_duplicate_records"]["affected_users"] == 1
            assert agg["cross_page_duplicate_records"]["affected_records"] == 2
            assert agg["users_with_both_a_header_residual_and_duplicates"] == 1
            assert agg["totals"]["accumulated_records"] == 600
            assert agg["totals"]["distinct_record_ids"] == 598
            assert agg["totals"]["duplicate_records_total"] == 2


def t_step4_within_page_duplicates_are_not_counted_as_cross_page():
    """The cross-page number is the one 0012 asks for, so a repeat that never
    crossed a page boundary must not inflate it."""
    import step4_history_pull as s4

    items = [{"id": 1}, {"id": 1}, {"id": 2}, {"id": 3}, {"id": 2}]
    # pages: [1,1,2] then [3,2]. id 1 repeats WITHIN page 1; id 2 crosses.
    cls = s4.classify_sweep(items, [3, 2], 5)
    assert cls["cross_page_duplicate_ids"] == 1
    assert cls["cross_page_duplicate_records"] == 1
    assert cls["within_page_duplicate_records"] == 1
    assert cls["duplicate_records_total"] == 2
    assert cls["distinct_record_ids"] == 3

    # Without page attribution the cross-page figures are None, not a guess.
    blind = s4.classify_sweep(items, None, 5)
    assert blind["page_attribution_available"] is False
    assert blind["cross_page_duplicate_ids"] is None
    assert blind["cross_page_duplicate_records"] is None
    assert blind["duplicate_records_total"] == 2

    # Slices that do not tile the record list are refused rather than trusted.
    bad = s4.classify_sweep(items, [3, 99], 5)
    assert bad["page_attribution_available"] is False


def t_step4_residual_distribution_covers_discarded_users_too():
    """0012 asks for the residual distribution across the pool so the 2 percent
    tolerance can be judged. A distribution of survivors only cannot say
    whether the threshold is in the right place, so the discarded users are in
    it."""
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("a", 1), ("b", 1), ("c", 1)])
            script = [
                history_page(1, 1, 100, n=100, base_id=0),    # residual 0
                history_page(1, 1, 100, n=99, base_id=200),   # residual -1, 1%
                history_page(1, 1, 100, n=50, base_id=400),   # residual -50, discarded
            ]
            p = step4_puller(tmp, script, pool)
            p.run()
            dist = p.residual_distribution()
            assert dist["users_measured"] == 3, dist
            assert dist["includes_discarded_users"] is True
            assert dist["signed_residual"]["min"] == -50
            assert dist["signed_residual"]["zero"] == 1
            assert dist["signed_residual"]["negative_header_over_count"] == 2
            assert dist["abs_share_of_item_count"]["users_over_tolerance"] == 1
            assert dist["abs_share_of_item_count"]["users_within_tolerance"] == 2
            assert sum(dist["bands_by_abs_share"].values()) == 3
            assert dist["basis"].startswith("accumulated records")


def t_step4_consecutive_over_tolerance_discards_trip_a_tripwire():
    """A discard is not an error and does not move the error breaker, which
    would otherwise leave a systemic residual fault free to discard the whole
    pool one benign-looking user at a time. And the stop is not exit 0."""
    import step4_history_pull as s4

    n = s4.MAX_CONSECUTIVE_OVER_TOLERANCE
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            users = [(f"u{i:03d}", 1) for i in range(n + 5)]
            pool = fake_pool(tmp, users)
            script = [history_page(1, 1, 999, n=1) for _ in range(n + 5)]
            p = step4_puller(tmp, script, pool)
            p.run()
            assert p.consecutive_over_tolerance >= n
            assert p.abnormal_stop is True
            assert "consecutive users discarded" in (p.stop_reason or "")
            decided = p.latest_outcomes()
            assert len(decided) == n, \
                f"the tripwire did not stop the walk: {len(decided)} decided"
            assert p.consecutive_errors == 0, "a discard moved the error breaker"


def t_step4_progress_file_is_pollable_and_carries_no_usernames():
    """A 22-hour unattended run has to be checkable without attaching to it,
    and the progress file is in logs/ but is still counts only."""
    import step4_history_pull as s4

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("gravedigger", 1), ("umbrellastand", 1)])
            script = [history_page(1, 1, 2, n=2, base_id=0),
                      history_page(1, 1, 2, n=2, base_id=10)]
            p = step4_puller(tmp, script, pool)
            p.run()
            payload = json.loads(p.progress_path.read_text())
            assert payload["pid"] == os.getpid()
            assert payload["users_decided_total"] == 2
            assert payload["finished"] is True
            assert payload["completeness_rule"] == "page_count"
            assert payload["residual_tolerance"] == 0.02
            assert payload["by_outcome"]["complete"] == 2
            blob = payload_text = p.progress_path.read_text()
            for name in ("gravedigger", "umbrellastand"):
                assert name not in blob, f"the progress file leaked {name}"
            assert s4.names_in(payload, s4.pool_names(p)) == []
            assert "TRAKT" not in payload_text
            # and it is readable back by the status reader
            assert s4.print_status(p.progress_path) == 0


def t_step4_sabbath_window_is_honoured():
    import step4_history_pull as s4
    from datetime import datetime as dt

    window = s4.parse_sabbath_window("FRI 17:30-SAT 20:30")
    assert s4.parse_sabbath_window("off") is None
    assert s4.in_sabbath(dt(2026, 8, 14, 18, 0), window)      # Friday evening
    assert s4.in_sabbath(dt(2026, 8, 15, 12, 0), window)      # Saturday midday
    assert not s4.in_sabbath(dt(2026, 8, 14, 16, 0), window)  # Friday afternoon
    assert not s4.in_sabbath(dt(2026, 8, 15, 21, 0), window)  # Saturday night
    assert not s4.in_sabbath(dt(2026, 8, 11, 18, 0), window)  # Tuesday

    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        with step4_env(tmp):
            pool = fake_pool(tmp, [("u", 1)])
            p = step4_puller(tmp, [history_page(1, 1, 2, n=2)], pool)
            p.sabbath_window = window
            import step4_history_pull as mod
            saved = mod.in_sabbath
            mod.in_sabbath = lambda now, w: True
            try:
                p.run()
            finally:
                mod.in_sabbath = saved
            assert p.latest_outcomes() == {}
            assert p.client.counters["requests_sent"] == 0
            assert "Sabbath" in (p.stop_reason or "")


def main() -> int:
    print("offline behaviour checks")
    checks = [
        ("throttle sits below the documented ceiling", t_throttle_below_ceiling),
        ("throttle blocks once the per-minute cap is reached", t_throttle_blocks_at_limit),
        ("throttle survives restart, no post-crash burst", t_throttle_survives_restart),
        ("sibling processes share one budget", t_throttle_shared_between_siblings),
        ("unreadable throttle state is treated conservatively", t_throttle_unreadable_state_is_conservative),
        ("403 on a non-user resource hard stops and records full headers", t_403_on_non_user_resource_hard_stops_and_records_headers),
        ("403 on a reserved/bare users path hard stops", t_403_on_reserved_user_segment_hard_stops),
        ("403 with X-Private-User false hard stops", t_403_with_private_user_false_hard_stops),
        ("403 with an unrecognised X-Private-User value hard stops", t_403_with_unrecognised_private_user_value_hard_stops),
        ("resumed run does not re-request a blocked endpoint", t_403_hard_stop_endpoint_not_rerequested_on_resume),
        ("a legacy 403 log record is read as a hard stop", t_legacy_403_record_without_outcome_is_read_as_hard_stop),
        ("user 403 with X-Private-User true skips and the run continues", t_403_on_user_resource_with_private_header_skips_and_continues),
        ("user 403 with the header absent skips and the run continues", t_403_on_user_resource_without_header_skips_and_continues),
        ("a skipped user is not re-requested and stays access_denied", t_skipped_user_is_not_rerequested_and_stays_access_denied),
        ("the skip index survives a cleared cache", t_skipped_user_index_survives_a_cleared_cache),
        ("pre-amendment cache meta reads access_denied False", t_old_cache_meta_without_access_denied_reads_false),
        ("consecutive user 403s escalate to a hard stop", t_consecutive_user_403s_escalate_to_hard_stop),
        ("an intervening 2xx resets the user-403 streak", t_intervening_success_resets_the_streak),
        ("a 401 does not reset the user-403 streak", t_401_does_not_reset_the_streak),
        ("confirmed-private 403s do not trip breaker A", t_confirmed_private_403s_do_not_trip_breaker_a),
        ("the cumulative user-403 budget stops the run", t_cumulative_user_403_budget_stops_the_run),
        ("a mid-sweep 403 never returns partial history", t_mid_sweep_403_never_returns_partial_history),
        ("a skipped user is distinguishable from one with no history", t_skipped_user_is_distinguishable_from_a_user_with_no_history),
        ("a first-page 403 is move-on, not error", t_first_page_403_is_move_on_not_error),
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
        # -- Step 3 crawler ------------------------------------------------
        ("step3 exits non-zero on every loud failure", t_step3_exit_code_is_nonzero_on_access_blocked),
        ("step3 writes a run record on every exit path", t_step3_run_record_is_written_on_every_exit_path),
        ("step3 exits zero only on a committed stopping rule", t_step3_clean_stop_exits_zero),
        ("the step3 run record redacts the Client ID", t_step3_run_record_redacts_the_client_id),
        ("the user pool is written atomically", t_step3_pool_write_is_atomic),
        ("deliverables land at the round boundary, not in a finally", t_step3_deliverables_land_at_the_round_boundary),
        ("an interrupted round is discarded whole", t_step3_interrupted_round_is_discarded_whole),
        ("a user is expanded only after both edge calls", t_step3_user_is_expanded_only_after_both_edge_calls),
        ("a 403 expansion is not a zero-follower user", t_step3_403_expansion_is_not_a_zero_follower_user),
        ("access_denied counts users, not endpoints or cache replays", t_step3_access_denied_counts_users_not_endpoints),
        ("the round record separates a plateau from a stall", t_step3_round_record_separates_a_plateau_from_a_stall),
        ("a stall is flagged and throttling is not", t_step3_stall_is_flagged_and_throttling_is_not),
        ("the Step 4 forecast is aggregated and not built on a missing field", t_step3_forecast_is_aggregated_and_not_based_on_a_missing_field),
        ("the full edge list is recorded, not a spanning tree", t_step3_full_edge_list_is_recorded_not_a_spanning_tree),
        ("seed and Channel B provenance are recorded", t_step3_seed_and_channel_b_provenance_are_recorded),
        ("the privacy guard catches usernames and not ordinary prose", t_step3_artifact_refuses_usernames_but_not_ordinary_prose),
        ("the yield curve artifact is counts only", t_step3_yield_curve_artifact_is_counts_only),
        ("the stopping thresholds are unchanged", t_step3_stopping_thresholds_are_unchanged),
        ("the plateau margin is reported without moving the rule", t_step3_plateau_margin_is_reported_without_moving_the_rule),
        ("the backfill replay cannot reach the network", t_step3_backfill_replay_cannot_reach_the_network),
        # -- Step 4 history pull -------------------------------------------
        ("step4 order is stratified round-robin and deterministic", t_step4_order_is_stratified_round_robin_and_deterministic),
        ("every prefix is proportional across both tails", t_step4_every_prefix_is_proportional_across_both_tails),
        ("the real pool's order is proportional at every prefix", t_step4_real_pool_order_is_proportional),
        ("a forecast over the cap is never started", t_step4_forecast_cap_never_starts_the_user),
        ("a user at exactly the cap is pulled", t_step4_a_user_at_exactly_the_cap_is_pulled),
        ("actual pages over the cap discard, never truncate", t_step4_actual_pages_over_cap_discards_and_never_truncates),
        ("a sweep that grows past the cap is discarded whole", t_step4_a_sweep_that_grows_past_the_cap_is_discarded_whole),
        ("the two skip counts are reported separately", t_step4_the_two_skip_counts_are_reported_separately),
        ("the page cap reuses the 403 discard path", t_step4_page_cap_reuses_the_403_discard_path),
        ("step4 never uses the truncating bound", t_step4_never_uses_the_truncating_bound),
        ("a budget stop is neither a length skip nor terminal", t_step4_budget_stop_is_not_a_length_skip_and_is_not_terminal),
        ("a completed user is not re-requested", t_step4_completed_user_is_not_re_requested),
        ("an interrupt leaves no false completion", t_step4_interrupt_between_parse_and_ledger_leaves_no_false_completion),
        ("the ledger is append-only and last row wins", t_step4_ledger_is_append_only_and_last_row_wins),
        ("the live-call ledger cannot be reduced", t_step4_live_call_ledger_cannot_be_reduced),
        ("an offline run refuses the canonical state dir", t_step4_offline_run_refuses_the_canonical_state_dir),
        ("fetch timestamps come from disk, not the wall clock", t_step4_fetch_timestamps_come_from_disk_not_the_wall_clock),
        ("parsed rows keep what Steps 5, 7 and 8 need", t_step4_parsed_rows_keep_what_steps_5_7_and_8_need),
        ("a short read is a user failure, not a run stop", t_step4_short_read_is_a_user_level_failure_not_a_run_stop),
        ("a mid-sweep 403 stays distinct from a length skip", t_step4_mid_sweep_403_stays_distinct_from_a_length_skip),
        ("the step4 artifact carries no usernames", t_step4_artifact_carries_no_usernames),
        ("pagination drift is caught and named", t_step4_pagination_drift_is_caught_and_named),
        # -- decisions/0012: the adopted completeness rule -------------------
        ("the adopted completeness rule is the default", t_step4_adopted_completeness_rule_is_the_default),
        ("the adopted rule tolerates the artefact, not a real gap", t_step4_adopted_rule_tolerates_the_header_artefact_but_not_a_real_gap),
        ("the tolerance boundary is exactly 2 percent, with no floor", t_step4_tolerance_boundary_is_exactly_two_percent),
        ("an over-tolerance user is discarded and stays distinguishable", t_step4_over_tolerance_user_is_discarded_and_stays_distinguishable),
        ("the three behaviours are counted separately, not absorbed", t_step4_three_way_classification_is_counted_separately),
        ("a within-page repeat is not counted as cross-page", t_step4_within_page_duplicates_are_not_counted_as_cross_page),
        ("the residual distribution includes the discarded users", t_step4_residual_distribution_covers_discarded_users_too),
        ("consecutive over-tolerance discards trip a tripwire", t_step4_consecutive_over_tolerance_discards_trip_a_tripwire),
        ("the progress file is pollable and carries no usernames", t_step4_progress_file_is_pollable_and_carries_no_usernames),
        ("the Sabbath window is honoured", t_step4_sabbath_window_is_honoured),
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
