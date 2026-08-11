"""
Step 0 addendum: the history-endpoint shape probe, reproduced from cache.

Why this file exists
--------------------
artifacts/step1-outcome-definition.md cites two empirical figures and attributes
both to "the Step 0 probe":

  Section 2.1  123 play records covering 96 distinct (season, number) pairs on a
               single profile, 28 percent inflation, 25 episodes appearing more
               than once. This is the warrant for counting DISTINCT EPISODES
               rather than play events.
  Section 5    the first S2 watch preceded the last S1 watch by about six weeks.
               This is the warrant for first-pass S1 completion, definition (b),
               rather than max(watched_at) over S1, definition (a).

Both numbers came from an undocumented run tagged `step0-history-probe` in
logs/api_requests.ndjson: two GETs, no script, no run record. The responses are
on disk under raw/. This script recomputes both figures from those cached
bodies so the public numbers are reproducible from the repo. Both figures come
from the SAME single response, so one script covers both.

The run also produced the pagination figure quoted in Section 1 (roughly 64
pages per user at limit=250 on the probe profile), so that is recomputed here
too rather than left as a third loose citation.

Scope discipline
----------------
Recomputation, not a data pull. ZERO network calls when the cache is warm. The
script refuses to go live unless --allow-live is passed, and it checks the cache
for the client's stale-meta rule first: an entry written under an older meta
schema version is silently re-fetched by the client, which would turn a
zero-call reproduction into billed calls. If that would happen the script says
so and stops instead of absorbing the cost.

The username is an argument. It is not hard-coded and it is not retained in any
pool: this is an endpoint probe, not user discovery, and Step 3 has not run. The
show is hard-coded because the cache key is the endpoint path, and only the
show the original run pulled is on disk.

The Client ID is loaded from .env by the client at runtime and appears nowhere
in this file, in logs/, or in artifacts/.

Writes:  logs/step0_history_probe.json  (machine-local, may retain the handle)
Reads :  raw/ cache only

Run: .venv/bin/python src/step0_history_probe.py <public-username>
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from trakt_client import (  # noqa: E402
    LOGS_DIR,
    SCHEMA_VERSION,
    AccessBlocked,
    MissingCredential,
    RateLimitPersistent,
    TraktClient,
    TraktClientError,
)

LOG_PATH = LOGS_DIR / "step0_history_probe.json"

# The show the original `step0-history-probe` run pulled, by Trakt ID. Hard-coded
# for the same reason step1_episode_listing_probe.py hard-codes its slug: the
# cache key is the endpoint path, and this is the one show on disk. A show ID is
# not a user identifier.
SHOW_TRAKT_ID = 1398

# Exactly the two requests the original run made. Params must match byte for
# byte: the cache key is a hash of the canonicalised param dict, so any drift
# here misses the cache and costs a live call.
PER_SHOW_PARAMS = {"limit": 250, "page": 1}
UNFILTERED_PARAMS = {"limit": 10, "page": 1}

# The page-size Step 4 would actually use, for the pages-per-user estimate.
STEP4_PAGE_SIZE = 250


def _iso(ts: str) -> datetime:
    """Trakt stamps history as ...Z; fromisoformat wants an offset."""
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _cache_state(client: TraktClient, endpoint: str, params: dict) -> dict:
    """Would this request be served from disk, or would it go live?

    Mirrors TraktClient._read_cache without touching the network. The
    schema-version check is the one that bit the episode-listing probe: a meta
    file written under an older schema is treated as absent and silently
    re-fetched.
    """
    body_path, meta_path = client.cache_paths(endpoint, params)
    state = {
        "endpoint": endpoint,
        "params": params,
        "meta_present": meta_path.exists(),
        "body_present": body_path.exists(),
        "entry_schema_version": None,
        "current_schema_version": SCHEMA_VERSION,
        "would_serve_from_disk": False,
        "reason": None,
    }
    if not meta_path.exists():
        state["reason"] = "no meta file on disk; request has never been made"
        return state
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        state["reason"] = f"meta unreadable ({type(exc).__name__}); client would re-fetch"
        return state
    state["entry_schema_version"] = meta.get("schema_version")
    if meta.get("schema_version") != SCHEMA_VERSION:
        state["reason"] = (
            "STALE META: entry predates the current schema, the client would "
            "silently re-fetch and this would not be a zero-call run"
        )
        return state
    if not body_path.exists():
        state["reason"] = "meta present but body missing; client would re-fetch"
        return state
    state["would_serve_from_disk"] = True
    state["reason"] = "warm"
    return state


# --- the two figures --------------------------------------------------------


def duplicate_inflation(records: list) -> dict:
    """Section 2.1: how far play records overstate distinct episodes.

    The dedup key is (season, number) within the one show, which is the
    show-scoped form of the Section 2.1 key (show, season, number). Records that
    are not episodes are excluded before counting: a movie has no season.
    """
    episodes = [r for r in records
                if isinstance(r, dict) and r.get("type") == "episode"
                and isinstance(r.get("episode"), dict)]
    pairs = [(r["episode"].get("season"), r["episode"].get("number")) for r in episodes]
    counts = Counter(pairs)
    distinct = len(counts)
    multiplicity = Counter(counts.values())

    # Section 2.1 also claims episode.ids.trakt is NOT canonical and may
    # disagree with (season, number). Checkable here for free.
    ids_per_pair = {}
    for r in episodes:
        key = (r["episode"].get("season"), r["episode"].get("number"))
        tid = (r["episode"].get("ids") or {}).get("trakt")
        ids_per_pair.setdefault(key, set()).add(tid)
    pairs_with_multiple_ids = sum(1 for v in ids_per_pair.values() if len(v) > 1)
    distinct_episode_trakt_ids = len({
        (r["episode"].get("ids") or {}).get("trakt") for r in episodes
    })

    return {
        "play_records": len(episodes),
        "non_episode_records_excluded": len(records) - len(episodes),
        "distinct_season_number_pairs": distinct,
        "surplus_records": len(episodes) - distinct,
        "inflation_ratio": (len(episodes) / distinct) if distinct else None,
        "inflation_pct": (100.0 * (len(episodes) / distinct - 1)) if distinct else None,
        "episodes_in_more_than_one_record": sum(1 for v in counts.values() if v > 1),
        "multiplicity_distribution": {str(k): v for k, v in sorted(multiplicity.items())},
        "max_records_for_one_episode": max(counts.values()) if counts else None,
        "distinct_history_record_ids": len({r.get("id") for r in episodes}),
        "actions_seen": dict(Counter(r.get("action") for r in episodes)),
        "seasons_present": sorted({s for s, _ in pairs if s is not None}),
        "distinct_episode_trakt_ids": distinct_episode_trakt_ids,
        "pairs_mapping_to_more_than_one_episode_trakt_id": pairs_with_multiple_ids,
        "trakt_id_agrees_with_season_number_key":
            distinct_episode_trakt_ids == distinct and pairs_with_multiple_ids == 0,
    }


def s1_s2_overlap(records: list) -> dict:
    """Section 5: does a first S2 watch precede a last S1 watch?

    Computed two ways on purpose.

      all_records          definition (a), max(watched_at) over every S1 record.
                           This is the reading that produces the cited overlap.
      collapsed_earliest   the same comparison after the Section 2.2 rule, one
                           timestamp per distinct episode and the earliest wins.

    If the overlap is present in the first and absent in the second, the overlap
    is a rewatch artifact, which is exactly the argument Section 5 makes for
    first-pass completion.
    """
    episodes = [r for r in records
                if isinstance(r, dict) and r.get("type") == "episode"
                and isinstance(r.get("episode"), dict)]

    all_ts: dict[int, list[datetime]] = {}
    earliest: dict[tuple, datetime] = {}
    for r in episodes:
        season = r["episode"].get("season")
        watched = r.get("watched_at")
        if season is None or not watched:
            continue
        ts = _iso(watched)
        all_ts.setdefault(season, []).append(ts)
        key = (season, r["episode"].get("number"))
        if key not in earliest or ts < earliest[key]:
            earliest[key] = ts

    collapsed: dict[int, list[datetime]] = {}
    for (season, _number), ts in earliest.items():
        collapsed.setdefault(season, []).append(ts)

    def compare(bucket: dict[int, list[datetime]]) -> dict:
        s1 = sorted(bucket.get(1, []))
        s2 = sorted(bucket.get(2, []))
        if not s1 or not s2:
            return {"computable": False}
        last_s1, first_s2 = s1[-1], s2[0]
        days = (last_s1 - first_s2).total_seconds() / 86400.0
        return {
            "computable": True,
            "s1_timestamps": len(s1),
            "s2_timestamps": len(s2),
            "last_s1_watch": last_s1.isoformat(),
            "first_s2_watch": first_s2.isoformat(),
            "first_s2_precedes_last_s1": days > 0,
            "overlap_days": round(days, 2),
            "overlap_weeks": round(days / 7.0, 2),
        }

    return {
        "all_records_definition_a": compare(all_ts),
        "collapsed_earliest_section_2_2": compare(collapsed),
        "per_season_record_counts": {
            str(s): len(v) for s, v in sorted(all_ts.items())
        },
        "per_season_distinct_counts": {
            str(s): len(v) for s, v in sorted(collapsed.items())
        },
    }


def pagination_estimate(pagination: dict, payload: list) -> dict:
    """Section 1: pages per user for a full unfiltered history sweep."""
    item_count = pagination.get("item_count")
    pages = (-(-item_count // STEP4_PAGE_SIZE)) if isinstance(item_count, int) else None
    types = Counter(r.get("type") for r in payload if isinstance(r, dict))
    return {
        "endpoint_form": "GET /users/:id/history",
        "pagination_headers": pagination,
        "total_history_items_for_probe_profile": item_count,
        "assumed_step4_page_size": STEP4_PAGE_SIZE,
        "pages_per_user_at_step4_page_size": pages,
        "record_types_in_first_page": dict(types),
        "mixes_movies_and_episodes": len(types) > 1,
        "record_keys": sorted(payload[0].keys()) if payload and isinstance(payload[0], dict) else [],
    }


# --- driver -----------------------------------------------------------------


def main(username: str, allow_live: bool) -> int:
    started = datetime.now(timezone.utc)
    try:
        client = TraktClient(run_label="step0-history-probe")
    except MissingCredential as exc:
        print(f"BLOCKED: {exc}")
        return 2

    per_show_endpoint = f"users/{username}/history/shows/{SHOW_TRAKT_ID}"
    unfiltered_endpoint = f"users/{username}/history"

    planned = [
        (per_show_endpoint, PER_SHOW_PARAMS, "per_show_history"),
        (unfiltered_endpoint, UNFILTERED_PARAMS, "unfiltered_history_shape"),
    ]

    findings: dict = {
        "run": "step0-history-probe",
        "reproduction_of": "the untagged step0-history-probe run in logs/api_requests.ndjson",
        "started_at": started.isoformat(),
        "auth_mode": "client-id-only, no OAuth",
        "network_call_budget": 0,
        "allow_live": allow_live,
        "show_trakt_id": SHOW_TRAKT_ID,
    }

    # -- cache preflight, BEFORE any client.get ------------------------------
    preflight = [_cache_state(client, ep, params) for ep, params, _ in planned]
    findings["cache_preflight"] = preflight
    cold = [p for p in preflight if not p["would_serve_from_disk"]]

    if cold and not allow_live:
        findings["outcome"] = "STOP: cache not warm, refusing to spend live calls"
        findings["cold_requests"] = cold
        findings["finished_at"] = datetime.now(timezone.utc).isoformat()
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        LOG_PATH.write_text(json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8")
        print("STOP: this would not be a zero-call run.")
        for entry in cold:
            print(f"  {entry['endpoint']} {entry['params']}: {entry['reason']}")
        print("Re-run with --allow-live only if the Human Lead has budgeted the calls.")
        print(f"  run record: {LOG_PATH}")
        return 8

    calls: list[dict] = []
    try:
        responses = {}
        for endpoint, params, label in planned:
            sent_before = client.counters["requests_sent"]
            resp = client.get(endpoint, params)
            calls.append({
                "label": label,
                "method": "GET",
                "endpoint": endpoint,
                "params": params,
                "status": resp.status,
                "ok": resp.ok,
                "served_from_disk": resp.from_cache,
                "went_live": client.counters["requests_sent"] > sent_before,
                "pagination_headers": resp.pagination,
                "raw_path": str(resp.raw_path) if resp.raw_path else None,
            })
            responses[label] = resp

        per_show = responses["per_show_history"]
        unfiltered = responses["unfiltered_history_shape"]

        if not per_show.ok or not isinstance(per_show.data, list):
            findings["outcome"] = f"STOP: per-show history unusable, HTTP {per_show.status}"
            raise SystemExit(_finish(findings, calls, client, 6))

        records = per_show.data
        findings["section_2_1_duplicate_inflation"] = duplicate_inflation(records)
        findings["section_5_s1_s2_overlap"] = s1_s2_overlap(records)
        findings["section_1_pagination"] = pagination_estimate(
            unfiltered.pagination, unfiltered.data if isinstance(unfiltered.data, list) else []
        )

        infl = findings["section_2_1_duplicate_inflation"]
        ovl = findings["section_5_s1_s2_overlap"]["all_records_definition_a"]
        findings["cited_vs_reproduced"] = {
            "play_records": {"cited": 123, "reproduced": infl["play_records"]},
            "distinct_pairs": {"cited": 96, "reproduced": infl["distinct_season_number_pairs"]},
            "inflation_pct": {"cited": 28.0,
                              "reproduced": round(infl["inflation_pct"], 3)
                              if infl["inflation_pct"] is not None else None},
            "episodes_more_than_once": {"cited": 25,
                                        "reproduced": infl["episodes_in_more_than_one_record"]},
            "overlap_weeks": {"cited": 6.0, "reproduced": ovl.get("overlap_weeks")},
            "pages_per_user": {
                "cited": 64,
                "reproduced": findings["section_1_pagination"]["pages_per_user_at_step4_page_size"],
            },
        }
        findings["outcome"] = "completed"

    except AccessBlocked as exc:
        findings["outcome"] = "HARD STOP: 403"
        findings["error"] = str(exc)
    except RateLimitPersistent as exc:
        findings["outcome"] = "STOP: persistent 429"
        findings["error"] = str(exc)
    except TraktClientError as exc:
        findings["outcome"] = f"STOP: {type(exc).__name__}"
        findings["error"] = str(exc)

    return _finish(findings, calls, client, 0 if findings.get("outcome") == "completed" else 1)


def _finish(findings: dict, calls: list, client: TraktClient, code: int) -> int:
    findings["calls"] = calls
    findings["live_calls_used"] = client.counters["requests_sent"]
    findings["counters"] = client.summary()
    findings["throttle_spend"] = client.throttle.spent()
    findings["finished_at"] = datetime.now(timezone.utc).isoformat()

    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(findings, indent=2, sort_keys=True), encoding="utf-8")

    if findings.get("outcome") == "completed":
        infl = findings["section_2_1_duplicate_inflation"]
        ovl_a = findings["section_5_s1_s2_overlap"]["all_records_definition_a"]
        ovl_b = findings["section_5_s1_s2_overlap"]["collapsed_earliest_section_2_2"]
        print(f"live calls used: {findings['live_calls_used']}")
        print(f"2.1  {infl['play_records']} play records -> "
              f"{infl['distinct_season_number_pairs']} distinct (season, number), "
              f"{infl['inflation_pct']:.2f}% inflation, "
              f"{infl['episodes_in_more_than_one_record']} episodes in >1 record")
        print(f"5    definition (a), all records: first S2 precedes last S1 by "
              f"{ovl_a['overlap_days']} days ({ovl_a['overlap_weeks']} weeks)")
        print(f"5    Section 2.2 collapsed-earliest: overlap "
              f"{ovl_b['overlap_days']} days ({ovl_b['overlap_weeks']} weeks)")
        print(f"1    {findings['section_1_pagination']['pages_per_user_at_step4_page_size']} "
              f"pages per user at limit={STEP4_PAGE_SIZE}")
    print(f"run record: {LOG_PATH}")
    return code


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--allow-live"]
    if len(args) != 1:
        print(__doc__)
        raise SystemExit(1)
    raise SystemExit(main(args[0], "--allow-live" in sys.argv[1:]))
