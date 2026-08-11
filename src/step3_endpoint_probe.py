"""Step 3 reconnaissance: confirm the shape of every endpoint the crawl will use.

Spends at most 8 live calls. Nothing about the crawl design is committed until
this has run, because a wrong assumption about an endpoint's shape at Step 3
scale is thousands of wasted calls.

Questions this answers:
  1. Does /users/:id/stats work Client-ID-only, and does it carry the fields the
     "usable user" screen needs (episode count, follower/following degree)?
  2. Does /users/:id/followers and /following work, and do they paginate?
  3. Does /lists/trending and /lists/popular work, and does each record carry the
     owning user? (Channel B)
  4. Does /comments/recent/... work as a Channel A seed source, restricted to
     MOVIES so that nothing is harvested from comments on any measured show?

Output: logs/step3_endpoint_probe.json (machine-local; may name the probe user).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import TraktClient  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROBE_USER = "justin"  # already on disk from Step 0; no new user is touched


def shape(value, depth=0):
    """Describe a JSON value's structure without dumping its content."""
    if depth > 3:
        return "..."
    if isinstance(value, dict):
        return {k: shape(v, depth + 1) for k, v in list(value.items())[:20]}
    if isinstance(value, list):
        return [shape(value[0], depth + 1)] if value else []
    return type(value).__name__


def main() -> int:
    client = TraktClient(run_label="step3_endpoint_probe")
    results: dict[str, object] = {
        "probed_at": datetime.now(timezone.utc).isoformat(),
        "probes": {},
    }

    probes = [
        ("user_stats", f"users/{PROBE_USER}/stats", None),
        ("user_followers", f"users/{PROBE_USER}/followers", {"limit": 10, "page": 1}),
        ("user_following", f"users/{PROBE_USER}/following", {"limit": 10, "page": 1}),
        ("lists_trending", "lists/trending", {"limit": 10, "page": 1}),
        ("lists_popular", "lists/popular", {"limit": 10, "page": 1}),
        ("comments_recent_movies", "comments/recent/all/movies", {"limit": 10, "page": 1}),
    ]

    for name, endpoint, params in probes:
        try:
            resp = client.get(endpoint, params)
            record = {
                "endpoint": endpoint,
                "params": params,
                "status": resp.status,
                "ok": resp.ok,
                "unavailable": resp.unavailable,
                "access_denied": resp.access_denied,
                "from_cache": resp.from_cache,
                "pagination": resp.pagination,
                "payload_type": type(resp.data).__name__,
                "n_items": len(resp.data) if isinstance(resp.data, list) else None,
                "shape": shape(resp.data[0]) if isinstance(resp.data, list) and resp.data
                         else shape(resp.data),
            }
        except Exception as exc:  # noqa: BLE001 - probe records the failure
            record = {
                "endpoint": endpoint,
                "params": params,
                "exception": type(exc).__name__,
                "detail": str(exc)[:400],
            }
        results["probes"][name] = record
        print(f"{name:26s} -> {record.get('status', record.get('exception'))}")

    results["client_counters"] = client.summary()
    out = PROJECT_ROOT / "logs" / "step3_endpoint_probe.json"
    out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\nwrote {out}")
    print(json.dumps(client.summary(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
