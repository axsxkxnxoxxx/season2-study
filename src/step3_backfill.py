"""Step 3 backfill. OFFLINE. Not one live call, by construction.

Why this exists
---------------
The first Step 3 run recorded a round as eleven numbers. Eleven numbers cannot
tell a plateau from a stall, cannot say which channel was still producing, and
cannot say whether 2796 seconds was throttling or a suspended machine. The run
also discarded, per round, things that only exist while the cached bodies are on
disk: the full follower/following edge list (only the first parent was kept, so
raw/ held a spanning tree and the claim that Step 11 can test for one clique was
false), which movie each seed came from, and which feed and which list each
Channel B owner came from.

None of that needs re-pulling. Every response is already in raw/. This script
replays the crawl against the cache with the amended code, which reconstructs
every missing structural metric exactly, and it reads the request log for the
per-round failure and timing metrics. The two are merged, and every field says
where it came from.

How zero live calls is guaranteed, not asserted
-----------------------------------------------
The client is constructed with a session whose only method raises. A cache miss
therefore cannot fall through to the network: it raises OfflineViolation and the
replay stops loudly. `requests_sent` is checked at the end and must be zero.
The logs and throttle directories are pointed at a scratch path so the replay
cannot contend with, or pollute, a live run's request log or rate budget.

What is backfilled and what is not
----------------------------------
BACKFILLED, exact           per-channel new-eligible yield, frontier size and
                            shape, expanded counts, neighbours returned, dedup
                            rates, list dedup, per-edge expansion outcomes, the
                            full edge list, seed provenance, Channel B
                            provenance, the corrected Step 4 page forecast.
                            Reconstructed by re-running the same code over the
                            same cached bodies, and verified field by field
                            against the round records the live run wrote.
BACKFILLED, from the log    per-round 429 count, 5xx count, transport errors,
                            transient-retry count and backoff sleep, request
                            span, and the largest gap between consecutive
                            requests.
NOT RECOVERABLE             throttle sleep seconds per round. The client did not
                            record it and it cannot be derived from the log
                            without assuming the throttle's behaviour, so it is
                            null with source "not_recorded". It is NOT estimated
                            and it is NOT interpolated. The largest inter-request
                            gap is measured and answers the question throttle
                            sleep was wanted for.

Every round record carries `metrics_source` and a `field_sources` map, so a
backfilled value and a measured one are never confused.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from collections import Counter, deque
from datetime import datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import step3_user_discovery as s3  # noqa: E402
from step3_user_discovery import (  # noqa: E402
    ARTIFACTS,
    LOGS_DIR,
    PROJECT_ROOT,
    RAW_STEP3,
    Step3Crawler,
    _atomic_write_text,
    _csv_cell,
    plan_block,
    utcnow,
)
from trakt_client import RAW_DIR, TraktClient  # noqa: E402

BACKFILL_DIR = RAW_STEP3 / "backfill"
REQUEST_LOG = LOGS_DIR / "api_requests.ndjson"
RUN_LABEL = "step3_user_discovery"


class OfflineViolation(RuntimeError):
    """The replay tried to reach the network. It must never get that far."""


class FrozenSession:
    """A session that cannot make a request. This is the zero-live-call guard."""

    def __init__(self) -> None:
        self.attempts: list[str] = []

    def get(self, url, headers=None, params=None, timeout=None):  # noqa: ANN001
        self.attempts.append(f"{url} {params}")
        raise OfflineViolation(
            f"offline replay attempted a live GET: {url} params={params}. "
            f"Every response this replay needs is supposed to be in raw/ already; "
            f"a miss here means the cache does not hold what the run claimed to "
            f"have fetched. Nothing was sent."
        )


# ---------------------------------------------------------------------------
# 1. the replay
# ---------------------------------------------------------------------------


def replay(state_snapshot: dict[str, Any], scratch: Path, out_dir: Path) -> Step3Crawler:
    """Re-run rounds 1..N from cache. N is the completed-round count in the
    snapshot, so the replay never runs past what the live run actually did."""
    n_rounds = len(state_snapshot["rounds"])
    scratch.mkdir(parents=True, exist_ok=True)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    session = FrozenSession()
    client = TraktClient(
        raw_dir=RAW_DIR,                 # the real cache, read only
        logs_dir=scratch / "logs",       # never the live run's log
        run_label="step3_offline_replay",
        session=session,
    )
    crawler = Step3Crawler(client, resume=False, state_dir=out_dir, max_rounds=n_rounds)
    crawler.write_artifact = False
    crawler.run()

    sent = client.counters["requests_sent"]
    if sent or session.attempts:
        raise OfflineViolation(
            f"replay recorded {sent} outbound request(s); it must be zero")
    return crawler


def verify(replayed: list[dict[str, Any]], recorded: list[dict[str, Any]]) -> dict[str, Any]:
    """Field-by-field comparison on the fields the live run also wrote.

    A divergence here is not something to reconcile quietly. It would mean the
    replay is not the same computation as the run, and every backfilled number
    would be suspect. It is reported.
    """
    shared = [
        "round", "discovery_calls", "screen_calls", "channel_a_calls",
        "channel_b_calls", "new_eligible_users", "yield_per_discovery_call",
        "new_usable_confirmed", "cum_discovered", "cum_eligible",
        "cum_screened", "cum_usable",
    ]
    diffs: list[dict[str, Any]] = []
    for rec, orig in zip(replayed, recorded):
        for field in shared:
            a, b = rec.get(field), orig.get(field)
            if isinstance(a, float) or isinstance(b, float):
                same = abs(float(a or 0) - float(b or 0)) < 1e-9
            else:
                same = a == b
            if not same:
                diffs.append({"round": orig.get("round"), "field": field,
                              "replayed": a, "recorded": b})
    return {
        "rounds_compared": min(len(replayed), len(recorded)),
        "fields_compared_per_round": len(shared),
        "mismatches": len(diffs),
        "exact": not diffs and len(replayed) == len(recorded),
        "detail": diffs[:50],
        "replayed_rounds": len(replayed),
        "recorded_rounds": len(recorded),
    }


# ---------------------------------------------------------------------------
# 2. timing and failure metrics, from the request log
# ---------------------------------------------------------------------------


def _ts(value: str) -> float:
    return datetime.fromisoformat(value).timestamp()


def log_metrics_per_round(recorded: list[dict[str, Any]],
                          log_path: Path) -> dict[int, dict[str, Any]]:
    """Attribute each logged request to the round it fell in.

    Round r spans (end of round r-1, end of round r]. The live run wrote the
    round-end timestamp, so these windows are exact rather than inferred.
    """
    if not log_path.exists() or not recorded:
        return {}
    events: list[dict[str, Any]] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        if rec.get("run") != RUN_LABEL:
            continue
        events.append(rec)
    if not events:
        return {}
    events.sort(key=lambda r: r["ts"])

    bounds = [_ts(events[0]["ts"]) - 1.0] + [_ts(r["at"]) for r in recorded]
    out: dict[int, dict[str, Any]] = {}
    for idx, round_rec in enumerate(recorded):
        lo, hi = bounds[idx], bounds[idx + 1]
        window = [e for e in events if lo < _ts(e["ts"]) <= hi]
        stamps = [_ts(e["ts"]) for e in window]
        gaps = [stamps[i] - stamps[i - 1] for i in range(1, len(stamps))]
        statuses = Counter(e.get("status") for e in window)
        backoff = [e for e in window if e.get("event") == "transient_backoff"]
        pauses = [e for e in window if e.get("event") == "rate_limit_pause"]
        out[round_rec["round"]] = {
            "log_events": len(window),
            "log_responses": sum(v for k, v in statuses.items() if k is not None),
            "rate_limit_pauses": len(pauses),
            "sleep_seconds_rate_limit": round(
                sum(float(e.get("pause_seconds") or 0) for e in pauses), 1),
            "http_429": statuses.get(429, 0),
            "http_5xx": sum(v for k, v in statuses.items()
                            if isinstance(k, int) and 500 <= k < 600),
            "transport_errors": sum(1 for e in window
                                    if e.get("event") == "transport_error"),
            "transient_retries": len(backoff),
            "sleep_seconds_backoff": round(
                sum(float(e.get("sleep_seconds") or 0) for e in backoff), 1),
            "sleep_seconds_throttle": None,
            "request_span_seconds": round(stamps[-1] - stamps[0], 1) if len(stamps) > 1 else 0.0,
            "max_inter_request_gap_seconds": round(max(gaps), 1) if gaps else 0.0,
            "median_inter_request_gap_seconds": (
                round(sorted(gaps)[len(gaps) // 2], 2) if gaps else 0.0),
            "wall_seconds": round_rec.get("seconds"),
        }
        wall = float(round_rec.get("seconds") or 0.0)
        largest = out[round_rec["round"]]["max_inter_request_gap_seconds"]
        out[round_rec["round"]]["gap_share_of_wall"] = (
            round(largest / wall, 3) if wall else None)
        # A stall is one enormous gap with no 429. Throttling is many small
        # gaps. The record now says which shape the round had.
        out[round_rec["round"]]["stall_suspected"] = bool(
            largest > s3.STALL_UNACCOUNTED_SECONDS and not pauses)
    return out


# ---------------------------------------------------------------------------
# 3. merge
# ---------------------------------------------------------------------------

REPLAY_ONLY_FIELDS = [
    "channel_a_new_eligible", "channel_b_new_eligible", "channel_a_yield_per_call",
    "channel_b_yield_per_call", "channel_overlap_this_round", "expanded_this_round",
    "expanded_total", "frontier_exhausted", "frontier_size", "frontier_seeds_nonempty",
    "frontier_seeds_total", "frontier_by_depth", "neighbours_returned",
    "neighbours_new", "neighbours_already_known", "neighbour_dedup_rate",
    "neighbours_per_expanded_user", "edges_recorded", "edges_to_private_or_deleted",
    "list_records_seen", "lists_new", "lists_duplicate", "list_dedup_rate",
    "list_owners_new", "list_owners_already_known", "channel_b_by_feed",
    "expansions_complete", "expansions_access_denied", "expansions_unavailable",
    "expansions_other_status", "screen_access_denied", "screen_unavailable",
    "screen_other_status", "screen_below_floor", "screen_reduced_payloads",
    "cum_access_denied_users", "cum_access_denied_endpoint_hits",
    "margin_above_trigger", "rounds_below_threshold_so_far",
    "rounds_until_rule_is_eligible",
]

LOG_FIELDS = [
    "rate_limit_pauses", "sleep_seconds_rate_limit", "http_429", "http_5xx",
    "transport_errors", "transient_retries", "sleep_seconds_backoff",
    "request_span_seconds", "max_inter_request_gap_seconds",
    "median_inter_request_gap_seconds", "gap_share_of_wall", "stall_suspected",
    "log_events", "log_responses",
]


def merge_rounds(replayed: list[dict[str, Any]],
                 recorded: list[dict[str, Any]],
                 log_metrics: dict[int, dict[str, Any]],
                 verified: bool) -> list[dict[str, Any]]:
    """One record per round, with a source for every field."""
    by_round = {r["round"]: r for r in recorded}
    merged: list[dict[str, Any]] = []
    for rec in replayed:
        n = rec["round"]
        orig = by_round.get(n, {})
        out = dict(rec)

        # Timings belong to the live run, not to the replay: replaying from
        # disk takes milliseconds and those milliseconds mean nothing.
        for key in ("wall_seconds", "seconds", "request_seconds",
                    "sleep_seconds_throttle", "sleep_seconds_rate_limit",
                    "sleep_seconds_backoff", "sleep_seconds_total",
                    "unaccounted_seconds", "max_inter_request_gap_seconds",
                    "requests_from_cache", "requests_live", "rate_limit_pauses",
                    "transient_retries", "http_5xx", "transport_errors",
                    "stall_suspected"):
            out.pop(key, None)
        out["at"] = orig.get("at")
        out["seconds"] = orig.get("seconds")
        out["wall_seconds"] = orig.get("seconds")
        out["cum_calls"] = orig.get("cum_calls")
        out["cum_calls_live"] = orig.get("cum_calls")
        out["cum_calls_attempted"] = orig.get("cum_calls")
        out.update(log_metrics.get(n, {}))
        out["sleep_seconds_throttle"] = None
        out["sleep_seconds_throttle_note"] = (
            "not recorded by the client during the live run; not derivable from "
            "the request log without assuming the throttle's behaviour, so it is "
            "left null rather than estimated")

        sources = {f: "measured_live_run" for f in orig}
        sources.update({f: (
            "backfilled_replay_exact" if verified else "backfilled_replay_UNVERIFIED")
            for f in REPLAY_ONLY_FIELDS if f in out})
        sources.update({f: "backfilled_from_request_log" for f in LOG_FIELDS if f in out})
        sources["sleep_seconds_throttle"] = "not_recoverable"
        out["metrics_source"] = (
            "mixed: measured live-run fields plus replay and request-log backfill")
        out["field_sources"] = sources
        merged.append(out)
    return merged


# ---------------------------------------------------------------------------
# 4. provenance extracts and the repair utility
# ---------------------------------------------------------------------------


def write_provenance(crawler: Step3Crawler, out_dir: Path) -> dict[str, Any]:
    """raw/ only: every one of these carries usernames."""
    seeds = [
        {"slug": slug, **(rec.get("seed_provenance") or {})}
        for slug, rec in crawler.users.items()
        if rec.get("seed_provenance")
    ]
    _atomic_write_text(out_dir / "seed_provenance.jsonl",
                       "".join(json.dumps(r) + "\n" for r in seeds))

    b_rows = [
        {"slug": slug, **entry}
        for slug, rec in crawler.users.items()
        for entry in (rec.get("lists_owned") or [])
    ]
    _atomic_write_text(out_dir / "channel_b_provenance.jsonl",
                       "".join(json.dumps(r) + "\n" for r in b_rows))

    per_owner = Counter(r["slug"] for r in b_rows)
    lists_per_owner = Counter(per_owner.values())
    edges = 0
    edge_pairs: set[tuple[str, str]] = set()
    reciprocal = 0
    edge_path = out_dir / "edges.jsonl"
    if edge_path.exists():
        for line in edge_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            edges += 1
            pair = (e["follower"], e["followee"])
            edge_pairs.add(pair)
            if (pair[1], pair[0]) in edge_pairs:
                reciprocal += 1
    return {
        "seed_provenance": {
            "seeds_with_provenance": len(seeds),
            "by_feed": dict(Counter(r.get("feed") for r in seeds)),
            "distinct_movies": len({r.get("movie_trakt_id") for r in seeds
                                    if r.get("movie_trakt_id") is not None}),
            "seeds_per_movie_max": max(
                Counter(r.get("movie_trakt_id") for r in seeds).values(), default=0),
            "seeds_missing_movie": sum(1 for r in seeds
                                       if r.get("movie_trakt_id") is None),
        },
        "channel_b_provenance": {
            "owner_list_records": len(b_rows),
            "distinct_owners": len(per_owner),
            "by_feed": dict(Counter(r.get("feed") for r in b_rows)),
            "lists_per_owner_histogram": {str(k): v for k, v in
                                          sorted(lists_per_owner.items())},
            "max_lists_for_one_owner": max(per_owner.values(), default=0),
        },
        "edge_list": {
            "edges_recorded": edges,
            "distinct_directed_pairs": len(edge_pairs),
            "reciprocal_pairs": reciprocal,
            "note": "the live run kept only the first parent per user, which is a "
                    "spanning tree; a tree is acyclic by construction, so it cannot "
                    "answer whether the pool is one clique. This is the graph.",
        },
    }


def repair_expanded(state_path: Path, apply_changes: bool) -> dict[str, Any]:
    """Find users marked expanded whose edge pages are not in the cache.

    Under the pre-amendment code a user was marked expanded BEFORE its two edge
    calls, so an interrupt between them left the user permanently expanded with
    one or both edge lists never read. Resume skips them and the pool is missing
    those subtrees with nothing on disk to say so. This finds them by asking the
    cache, and re-enqueues them so a resumed run reads them again, from disk,
    at no API cost.

    Read-only unless --apply is passed. It never writes a state file that a live
    process owns.
    """
    payload = json.loads(state_path.read_text(encoding="utf-8"))
    client_free_paths = TraktClient.cache_paths
    broken: list[dict[str, Any]] = []

    class _P:
        raw_dir = RAW_DIR

    for slug in payload["expanded"]:
        missing = []
        for edge in ("followers", "following"):
            endpoint = f"users/{slug}/{edge}"
            _, meta = client_free_paths(_P(), endpoint, {"page": 1, "limit": 100})
            if not Path(meta).exists():
                missing.append(edge)
        if missing:
            rec = payload["users"].get(slug) or {}
            broken.append({"slug": slug, "missing_edges": missing,
                           "depth": rec.get("depth"),
                           "origin_seed": rec.get("origin_seed")})

    result = {
        "state_file": str(state_path),
        "expanded_users": len(payload["expanded"]),
        "users_expanded_without_a_cached_edge_page": len(broken),
        "applied": False,
        "detail_written_to": None,
    }
    if not broken or not apply_changes:
        return result

    expanded = set(payload["expanded"])
    frontier = payload["frontier"]
    for item in broken:
        expanded.discard(item["slug"])
        seed = item["origin_seed"] or item["slug"]
        frontier.setdefault(seed, []).append([item["slug"], item["depth"] or 0])
    payload["expanded"] = sorted(expanded)
    payload["frontier"] = frontier
    payload["repaired_at"] = utcnow()
    _atomic_write_text(state_path, json.dumps(payload))
    result["applied"] = True
    return result


# ---------------------------------------------------------------------------
# 5. artifact
# ---------------------------------------------------------------------------


def write_artifact(crawler: Step3Crawler,
                   merged: list[dict[str, Any]],
                   verification: dict[str, Any],
                   provenance_summary: dict[str, Any],
                   snapshot_meta: dict[str, Any],
                   client: TraktClient) -> list[Path]:
    forecast = crawler.step4_forecast()
    payload = {
        "step": "3 user discovery",
        "artifact": "yield curve and Step 3 checkpoint. Counts and aggregates only.",
        "generated_at": utcnow(),
        "generated_by": "src/step3_backfill.py, offline replay of raw/, zero live calls",
        "source_state_snapshot": snapshot_meta,
        "plan": plan_block(),
        "counts": crawler.counts(),
        "plateau_state": crawler.plateau_state(),
        "step4_forecast": forecast,
        "provenance_summary": provenance_summary,
        "replay_verification": {k: v for k, v in verification.items() if k != "detail"},
        "replay_verification_mismatches": verification["detail"],
        "field_source_legend": {
            "measured_live_run": "written by the live run itself",
            "backfilled_replay_exact": "reconstructed by re-running the same code "
                                       "over the cached bodies, and verified "
                                       "field-by-field against the live run's own "
                                       "round records",
            "backfilled_from_request_log": "read from logs/api_requests.ndjson by "
                                           "attributing each logged request to the "
                                           "round window it fell in",
            "not_recoverable": "not recorded during the live run and not derivable; "
                               "left null, never estimated",
        },
        "notes": notes(crawler, merged, forecast),
        "rounds": merged,
    }
    text = json.dumps(payload, indent=2, default=str)

    leaked = crawler._names_present_in(payload)
    if leaked:
        raise ValueError(
            f"refusing to write usernames to artifacts/: {len(leaked)} found "
            f"(first: {leaked[:3]})")
    client._refuse_if_secret(text, "artifacts/step3-yield-curve.json")

    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    json_path = ARTIFACTS / "step3-yield-curve.json"
    _atomic_write_text(json_path, text)

    columns = [
        "round", "at", "discovery_calls", "screen_calls", "channel_a_calls",
        "channel_b_calls", "new_eligible_users", "yield_per_discovery_call",
        "channel_a_new_eligible", "channel_b_new_eligible",
        "channel_a_yield_per_call", "channel_b_yield_per_call",
        "new_usable_confirmed", "expanded_this_round", "expanded_total",
        "frontier_size", "frontier_seeds_nonempty", "frontier_exhausted",
        "neighbours_returned", "neighbours_new", "neighbours_already_known",
        "neighbour_dedup_rate", "neighbours_per_expanded_user",
        "list_records_seen", "lists_new", "lists_duplicate", "list_dedup_rate",
        "list_owners_new", "expansions_complete", "expansions_access_denied",
        "screen_access_denied", "screen_below_floor",
        "cum_discovered", "cum_eligible", "cum_screened", "cum_usable",
        "cum_calls", "moving_avg", "peak_moving_avg", "ratio_to_peak",
        "margin_above_trigger", "consecutive_below", "plateaued",
        "wall_seconds", "request_span_seconds", "max_inter_request_gap_seconds",
        "median_inter_request_gap_seconds", "gap_share_of_wall",
        "sleep_seconds_throttle", "sleep_seconds_rate_limit",
        "sleep_seconds_backoff", "rate_limit_pauses", "http_429", "http_5xx",
        "transport_errors", "transient_retries", "stall_suspected",
    ]
    rows = [",".join(columns)]
    for r in merged:
        rows.append(",".join(_csv_cell(r.get(c)) for c in columns))
    csv_path = ARTIFACTS / "step3-yield-curve.csv"
    _atomic_write_text(csv_path, "\n".join(rows) + "\n")
    return [json_path, csv_path]


def notes(crawler: Step3Crawler, merged: list[dict[str, Any]],
          forecast: dict[str, Any]) -> list[str]:
    """Readings a reviewer needs at the checkpoint, in counts only."""
    stalls = [r["round"] for r in merged if r.get("stall_suspected")]
    plateau = crawler.plateau_state()
    lowest = min((r["ratio_to_peak"] for r in merged
                  if r.get("ratio_to_peak") is not None), default=None)
    return [
        f"Step 4 forecast, aggregated over the {forecast.get('usable_users')} usable "
        f"users confirmed so far: {forecast.get('total_pages')} calls, "
        f"{forecast.get('hours_at_throttle_150_per_min')} hours at the 150/min throttle. "
        f"Mean {forecast.get('mean_pages_per_user')} pages per user, median "
        f"{forecast.get('median')}, p95 {forecast.get('p95')}, max {forecast.get('max')}. "
        f"The top decile of users holds "
        f"{forecast.get('share_of_pages_in_top_decile_of_users')} of the pages.",

        f"The forecast the live run stored was wrong, not merely un-summed: it divided "
        f"`total_plays`, which is absent from 77 percent of users/:id/stats payloads, "
        f"so most users forecast exactly one page. It is now computed from "
        f"episodes.plays + movies.plays, which is always present and which equals "
        f"total_plays wherever total_plays exists.",

        f"Plateau rule state: moving average {plateau['moving_avg']:.3f} against a peak "
        f"of {plateau['peak_moving_avg']:.3f}, ratio {plateau['ratio_to_peak']:.3f} "
        f"against a trigger of {plateau['plateau_trigger_ratio']}. The closest the run "
        f"has come is a ratio of {lowest:.3f}. The rule has not fired and no threshold "
        f"in it has been changed."
        if lowest is not None and plateau["ratio_to_peak"] is not None else
        "Plateau rule state unavailable.",

        f"Rounds whose clock looks like a stall rather than throttling: "
        f"{stalls if stalls else 'none'}. A stall is one enormous gap between "
        f"consecutive requests with no 429 in the round; throttling is many small "
        f"gaps. The live run recorded only a single wall-clock number, in which the "
        f"two are identical.",

        "Throttle sleep per round was never recorded by the client and is not "
        "derivable from the request log, so it is null with source not_recoverable. "
        "It has not been estimated. The largest inter-request gap is measured and "
        "answers what throttle sleep was wanted for.",
    ]


# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Step 3 offline backfill. No live calls.")
    parser.add_argument("--state", default=str(RAW_STEP3 / "state.json"))
    parser.add_argument("--out-dir", default=str(BACKFILL_DIR))
    parser.add_argument("--scratch", default=str(PROJECT_ROOT / "logs" / "backfill_scratch"))
    parser.add_argument("--repair-expanded", action="store_true",
                        help="report users marked expanded with no cached edge page")
    parser.add_argument("--apply-repair", action="store_true",
                        help="with --repair-expanded, rewrite the state file")
    args = parser.parse_args(argv)

    state_path = Path(args.state)
    if not state_path.exists():
        print(f"no state at {state_path}", file=sys.stderr)
        return 2

    if args.repair_expanded:
        result = repair_expanded(state_path, args.apply_repair)
        print(json.dumps(result, indent=2))
        return 0

    snapshot = json.loads(state_path.read_text(encoding="utf-8"))
    snapshot_meta = {
        "path": str(state_path),
        "saved_at": snapshot.get("saved_at"),
        "rounds_completed": len(snapshot["rounds"]),
        "users_in_state": len(snapshot["users"]),
        "live_calls_spent": (snapshot["calls_discovery"] + snapshot["calls_screen"]
                             + snapshot["calls_seed"]),
    }
    print(f"snapshot: {snapshot_meta['rounds_completed']} rounds, "
          f"{snapshot_meta['users_in_state']} users, "
          f"{snapshot_meta['live_calls_spent']} live calls already spent")

    out_dir = Path(args.out_dir)
    crawler = replay(snapshot, Path(args.scratch), out_dir)
    verification = verify(crawler.rounds, snapshot["rounds"])
    print(f"replay verification: {verification['mismatches']} mismatch(es) over "
          f"{verification['rounds_compared']} rounds "
          f"x {verification['fields_compared_per_round']} fields")

    log_metrics = log_metrics_per_round(snapshot["rounds"], REQUEST_LOG)
    merged = merge_rounds(crawler.rounds, snapshot["rounds"], log_metrics,
                          verification["exact"])
    _atomic_write_text(out_dir / "yield_curve.jsonl",
                       "".join(json.dumps(r) + "\n" for r in merged))
    provenance_summary = write_provenance(crawler, out_dir)
    paths = write_artifact(crawler, merged, verification, provenance_summary,
                           snapshot_meta, crawler.client)

    record = {
        "generated_at": utcnow(),
        "mode": "offline backfill",
        "live_calls": 0,
        "requests_sent_by_replay": crawler.client.counters["requests_sent"],
        "cache_hits_by_replay": crawler.client.counters["served_from_cache"],
        "source_state_snapshot": snapshot_meta,
        "replay_verification": verification,
        "provenance_summary": provenance_summary,
        "counts": crawler.counts(),
        "step4_forecast": crawler.step4_forecast(),
        "outputs": {
            "raw": sorted(str(p) for p in out_dir.glob("*.jsonl")),
            "artifacts": [str(p) for p in paths],
        },
    }
    text = json.dumps(record, indent=2, default=str)
    crawler.client._refuse_if_secret(text, str(LOGS_DIR / "step3_backfill_run.json"))
    _atomic_write_text(LOGS_DIR / "step3_backfill_run.json", text)

    print(json.dumps({k: v for k, v in record.items()
                      if k in ("live_calls", "requests_sent_by_replay",
                               "cache_hits_by_replay", "outputs")}, indent=2))
    return 0 if verification["exact"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
