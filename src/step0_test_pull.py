"""
Step 0 test pull: one live call against the Trakt API.

Deliberately a show endpoint, not a user endpoint. Step 0 is not user
discovery; harvesting or touching a username here would pre-empt Step 3.
/shows/:id/seasons is OAuth Optional and exercises exactly what Step 0 has to
prove: the Client ID alone authenticates, the throttle holds, raw lands in
raw/ before parsing, the rate-limit headers are logged, and a repeat call is
served from disk instead of the network.

Run: .venv/bin/python src/step0_test_pull.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import (  # noqa: E402
    LOGS_DIR,
    THROTTLE_PER_MIN,
    AccessBlocked,
    MissingCredential,
    RateLimitPersistent,
    TraktClient,
    TransientFailure,
)

TEST_ENDPOINT = "shows/breaking-bad/seasons"
TEST_PARAMS = {"extended": "full"}


def main() -> int:
    started = datetime.now(timezone.utc)
    try:
        client = TraktClient(run_label="step0-test-pull")
    except MissingCredential as exc:
        print(f"BLOCKED: {exc}")
        return 2

    print(f"throttle: {THROTTLE_PER_MIN} GET/min (documented ceiling 200/min)")
    print(f"test pull: GET /{TEST_ENDPOINT} {TEST_PARAMS}")

    try:
        first = client.get(TEST_ENDPOINT, TEST_PARAMS)
    except AccessBlocked as exc:
        print(f"BLOCKED (403): {exc}")
        return 3
    except RateLimitPersistent as exc:
        print(f"BLOCKED (429): {exc}")
        return 4
    except TransientFailure as exc:
        print(f"BLOCKED (transient): {exc}")
        return 5

    if not first.ok:
        print(f"test pull failed: HTTP {first.status}")
        return 6

    seasons = first.data or []
    numbered = [s for s in seasons if isinstance(s, dict) and s.get("number") is not None]
    s1 = next((s for s in numbered if s.get("number") == 1), None)
    s2 = next((s for s in numbered if s.get("number") == 2), None)

    # second call: must be served from disk, zero additional network requests
    sent_before = client.counters["requests_sent"]
    second = client.get(TEST_ENDPOINT, TEST_PARAMS)
    resume_ok = second.from_cache and client.counters["requests_sent"] == sent_before

    result = {
        "run": "step0-test-pull",
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": f"/{TEST_ENDPOINT}",
        "method": "GET",
        "http_status": first.status,
        "authenticated_with": "client_id_only",
        "seasons_returned": len(seasons),
        "s1_episode_count": (s1 or {}).get("episode_count"),
        "s2_episode_count": (s2 or {}).get("episode_count"),
        "raw_persisted": str(first.raw_path) if first.raw_path else None,
        "repeat_call_served_from_disk": resume_ok,
        "counters": client.summary(),
    }

    log_path = LOGS_DIR / "step0_test_pull.json"
    log_path.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    print(f"  HTTP {first.status}, {len(seasons)} seasons returned")
    print(f"  S1 episodes: {result['s1_episode_count']}, S2 episodes: {result['s2_episode_count']}")
    print(f"  raw persisted: {result['raw_persisted']}")
    print(f"  repeat call served from disk, no new request: {resume_ok}")
    print(f"  counters: {client.summary()}")
    print(f"  run record: {log_path}")
    return 0 if resume_ok else 7


if __name__ == "__main__":
    raise SystemExit(main())
