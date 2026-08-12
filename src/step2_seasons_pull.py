"""Step 2 frame, fetch pass: /shows/:id/seasons?extended=episodes,full.

One call per candidate show. Candidates are the shows with >= 50 S1 completers
in the full-pool completer diagnostic. Resumable: a show already carrying a
ledger row is never re-requested, and the client serves anything already in
raw/ from disk without a network call.

Writes a trimmed per-show extract; the untouched bodies stay in raw/ via the
client's own cache. No selection rule is applied here. This pass fetches.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from trakt_client import TraktClient, AccessBlocked, RateLimitPersistent  # noqa: E402

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
DIAG = ROOT / "processed" / "s1-completer-diagnostic-per-show.csv"
OUTDIR = ROOT / "processed" / "step2"
EXTRACT = OUTDIR / "seasons_extract.jsonl.gz"
LEDGER = OUTDIR / "seasons_ledger.jsonl"
PROGRESS = ROOT / "logs" / "step2_seasons_progress.json"
RUNLOG = ROOT / "logs" / "step2_seasons_run.json"

MIN_COMPLETERS = 50


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def trim_season(s: dict) -> dict:
    """Keep every field the frame or the field-inventory question needs.

    Episode objects are reduced to what Step 1 Section 3 reads plus the air
    date; overviews, images, ratings and translations are dropped.
    """
    eps = []
    for e in s.get("episodes") or []:
        eps.append({
            "number": e.get("number"),
            "season": e.get("season"),
            "first_aired": e.get("first_aired"),
            "episode_type": e.get("episode_type"),
            "runtime": e.get("runtime"),
            "trakt": (e.get("ids") or {}).get("trakt"),
        })
    return {
        "number": s.get("number"),
        "title": s.get("title"),
        "episode_count": s.get("episode_count"),
        "aired_episodes": s.get("aired_episodes"),
        "first_aired": s.get("first_aired"),
        "network": s.get("network"),
        "total_runtime": s.get("total_runtime"),
        "trakt": (s.get("ids") or {}).get("trakt"),
        "episodes": eps,
    }


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    d = pd.read_csv(DIAG, usecols=["show_trakt_id", "title", "completers"])
    cand = d[d["completers"] >= MIN_COMPLETERS].sort_values(
        "completers", ascending=False).reset_index(drop=True)
    print(f"candidates: {len(cand)} shows with >= {MIN_COMPLETERS} S1 completers", flush=True)

    done: set[int] = set()
    if LEDGER.exists():
        with open(LEDGER) as fh:
            for line in fh:
                try:
                    done.add(int(json.loads(line)["show_trakt_id"]))
                except Exception:
                    continue
    todo = cand[~cand["show_trakt_id"].isin(done)]
    print(f"already on disk: {len(done)} | to fetch: {len(todo)}", flush=True)

    client = TraktClient(run_label="step2_seasons")
    started = time.time()
    counts = {"ok": 0, "unavailable": 0, "error": 0, "cache": 0}
    stop_reason = None

    extract_fh = gzip.open(EXTRACT, "at")
    ledger_fh = open(LEDGER, "a")
    try:
        for i, row in enumerate(todo.itertuples(), 1):
            sid = int(row.show_trakt_id)
            endpoint = f"shows/{sid}/seasons"
            rec = {
                "show_trakt_id": sid,
                "requested_at": utcnow(),
                "endpoint": endpoint,
            }
            try:
                resp = client.get(endpoint, {"extended": "episodes,full"})
            except AccessBlocked as exc:
                # Not a user resource: a 403 here is a block, not a throttle.
                stop_reason = f"AccessBlocked on {endpoint}: {exc}"
                rec.update(outcome="blocked", detail=str(exc)[:400])
                ledger_fh.write(json.dumps(rec) + "\n")
                break
            except RateLimitPersistent as exc:
                stop_reason = f"RateLimitPersistent on {endpoint}: {exc}"
                rec.update(outcome="rate_limited", detail=str(exc)[:400])
                ledger_fh.write(json.dumps(rec) + "\n")
                break

            if resp.from_cache:
                counts["cache"] += 1
            if not resp.ok:
                counts["unavailable" if resp.unavailable else "error"] += 1
                rec.update(outcome="unavailable" if resp.unavailable else "error",
                           status=resp.status, from_cache=resp.from_cache)
                ledger_fh.write(json.dumps(rec) + "\n")
                continue

            seasons = resp.data or []
            if not isinstance(seasons, list):
                counts["error"] += 1
                rec.update(outcome="error", status=resp.status, detail="body is not a list")
                ledger_fh.write(json.dumps(rec) + "\n")
                continue

            counts["ok"] += 1
            trimmed = [trim_season(s) for s in seasons if isinstance(s, dict)]
            extract_fh.write(json.dumps({
                "show_trakt_id": sid,
                "seasons": trimmed,
            }) + "\n")
            rec.update(outcome="ok", status=resp.status, from_cache=resp.from_cache,
                       seasons_returned=len(trimmed),
                       season_numbers=sorted(
                           [s["number"] for s in trimmed if s["number"] is not None]))
            ledger_fh.write(json.dumps(rec) + "\n")

            if i % 100 == 0 or i == len(todo):
                extract_fh.flush()
                ledger_fh.flush()
                el = time.time() - started
                rate = i / el * 60 if el else 0
                prog = {
                    "updated_at": utcnow(),
                    "fetched_this_run": i,
                    "to_fetch": int(len(todo)),
                    "counts": dict(counts),
                    "shows_per_min": round(rate, 1),
                    "client": client.summary(),
                }
                PROGRESS.write_text(json.dumps(prog, indent=2))
                print(f"  {i}/{len(todo)}  ok={counts['ok']} "
                      f"unavail={counts['unavailable']} err={counts['error']} "
                      f"cache={counts['cache']}  {rate:.0f}/min", flush=True)
    finally:
        extract_fh.close()
        ledger_fh.close()

    run = {
        "run_label": "step2_seasons",
        "started_at": datetime.fromtimestamp(started, timezone.utc).isoformat(),
        "finished_at": utcnow(),
        "elapsed_min": round((time.time() - started) / 60, 2),
        "candidates": int(len(cand)),
        "fetched_this_run": int(len(todo)) if stop_reason is None else None,
        "counts": counts,
        "stop_reason": stop_reason,
        "client_summary": client.summary(),
    }
    RUNLOG.write_text(json.dumps(run, indent=2))
    print(json.dumps(run, indent=2))
    return 1 if stop_reason else 0


if __name__ == "__main__":
    raise SystemExit(main())
