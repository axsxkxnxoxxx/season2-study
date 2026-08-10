"""
Step 0 addendum: confirm the pagination behaviour and payload shape of
/users/:id/watched/shows.

The Human Lead's design decision is to pull histories with one call per user to
/users/:id/watched/shows, returning the full watched library with per-episode
timestamps, instead of per-user-per-show history calls. Confirming whether that
endpoint paginates was put in scope. Two things had to be measured, and both
are measured here from a single public profile:

  1. does it paginate, and what is the real maximum page size
  2. does the payload actually carry per-episode timestamps

The username is an argument. It is not hard-coded and it is not retained in any
pool: this is an endpoint probe, not user discovery, and Step 3 has not run.
Results are written to logs/, which never leaves the machine.

Run: .venv/bin/python src/step0_watched_endpoint_probe.py <public-username>
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import LOGS_DIR, TraktClient  # noqa: E402

EPISODE_TIMESTAMP_KEYS = {"seasons"}


def describe(resp) -> dict:
    items = resp.data if isinstance(resp.data, list) else []
    first = items[0] if items else {}
    return {
        "http_status": resp.status,
        "pagination": resp.pagination,
        "items_returned": len(items),
        "record_keys": sorted(first.keys()) if isinstance(first, dict) else None,
        "carries_seasons_or_episodes": bool(EPISODE_TIMESTAMP_KEYS & set(first))
        if isinstance(first, dict) else False,
    }


def main(username: str) -> int:
    client = TraktClient(run_label="step0-endpoint-probe")
    endpoint = f"users/{username}/watched/shows"

    profile = client.get(f"users/{username}")
    if not profile.ok:
        print(f"probe username did not resolve: HTTP {profile.status}")
        return 2
    if (profile.data or {}).get("private"):
        print("probe username is private; pick a public one")
        return 3

    variants = {
        "default_no_params": {},
        "extended_full": {"extended": "full"},
        "limit_1": {"limit": 1, "page": 1},
        "limit_1000": {"limit": 1000, "page": 1},
    }
    findings = {name: describe(client.get(endpoint, params))
                for name, params in variants.items()}

    paginates = any(f["pagination"].get("page_count", 0) > 1 for f in findings.values())
    honoured_limits = {name: f["pagination"].get("limit") for name, f in findings.items()}
    max_page_size = findings["limit_1000"]["pagination"].get("limit")
    item_count = findings["default_no_params"]["pagination"].get("item_count")
    episode_level = any(f["carries_seasons_or_episodes"] for f in findings.values())

    result = {
        "run": "step0-endpoint-probe",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "endpoint": "/users/:id/watched/shows",
        "paginates": paginates,
        "requested_vs_honoured_limit": honoured_limits,
        "max_page_size": max_page_size,
        "item_count_for_probe_profile": item_count,
        "calls_per_user_at_max_page_size": (
            None if not (item_count and max_page_size)
            else -(-item_count // max_page_size)
        ),
        "carries_per_episode_timestamps": episode_level,
        "record_keys_observed": findings["default_no_params"]["record_keys"],
        "variants": findings,
        "counters": client.summary(),
        "throttle_spend": client.throttle.spent(),
    }

    out = LOGS_DIR / "step0_watched_endpoint_probe.json"
    out.write_text(json.dumps(result, indent=2, default=str), encoding="utf-8")

    print(f"paginates: {paginates}")
    print(f"max page size honoured: {max_page_size} (limit=1000 was clamped)")
    print(f"calls per user at max page size: {result['calls_per_user_at_max_page_size']}")
    print(f"carries per-episode timestamps: {episode_level}")
    print(f"record keys: {result['record_keys_observed']}")
    print(f"live calls used: {client.summary()['requests_sent']}")
    print(f"written to: {out}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
