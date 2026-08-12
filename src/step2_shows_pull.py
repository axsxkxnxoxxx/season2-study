"""Step 2 frame, show-metadata pass: /shows/:id?extended=full.

One call per IN-FRAME show. The 868 candidates that never reached the frame
are not fetched: they are excluded, and the study has no use for their
metadata that would justify the spend.

Resumable. Bodies land in raw/ via the client cache, so a rebuild is free.
Records every scalar field the payload carries, so the field inventory is
read off what arrived rather than off an assumed schema.
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
STEP2 = ROOT / "processed" / "step2"
FRAME = STEP2 / "frame.csv"
EXTRACT = STEP2 / "shows_extract.jsonl.gz"
LEDGER = STEP2 / "shows_ledger.jsonl"
PROGRESS = ROOT / "logs" / "step2_shows_progress.json"
RUNLOG = ROOT / "logs" / "step2_shows_run.json"

DROP = {"images", "overview", "trailer", "homepage", "available_translations"}


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def trim(show: dict) -> dict:
    out = {}
    for k, v in show.items():
        if k in DROP:
            continue
        if k == "ids":
            out["trakt"] = v.get("trakt")
            out["imdb"] = v.get("imdb")
            continue
        out[k] = v
    return out


def main() -> int:
    frame = pd.read_csv(FRAME, usecols=["show_trakt_id"])
    ids = [int(x) for x in frame["show_trakt_id"].tolist()]
    print(f"in-frame shows: {len(ids)}", flush=True)

    done: set[int] = set()
    if LEDGER.exists():
        with open(LEDGER) as fh:
            for line in fh:
                try:
                    done.add(int(json.loads(line)["show_trakt_id"]))
                except Exception:
                    continue
    todo = [s for s in ids if s not in done]
    print(f"already on disk: {len(done)} | to fetch: {len(todo)}", flush=True)

    client = TraktClient(run_label="step2_shows")
    started = time.time()
    counts = {"ok": 0, "unavailable": 0, "error": 0, "cache": 0}
    stop_reason = None

    ex_fh = gzip.open(EXTRACT, "at")
    led_fh = open(LEDGER, "a")
    try:
        for i, sid in enumerate(todo, 1):
            endpoint = f"shows/{sid}"
            rec = {"show_trakt_id": sid, "requested_at": utcnow(), "endpoint": endpoint}
            try:
                resp = client.get(endpoint, {"extended": "full"})
            except AccessBlocked as exc:
                stop_reason = f"AccessBlocked on {endpoint}: {exc}"
                rec.update(outcome="blocked", detail=str(exc)[:400])
                led_fh.write(json.dumps(rec) + "\n")
                break
            except RateLimitPersistent as exc:
                stop_reason = f"RateLimitPersistent on {endpoint}: {exc}"
                rec.update(outcome="rate_limited", detail=str(exc)[:400])
                led_fh.write(json.dumps(rec) + "\n")
                break

            if resp.from_cache:
                counts["cache"] += 1
            if not resp.ok or not isinstance(resp.data, dict):
                counts["unavailable" if resp.unavailable else "error"] += 1
                rec.update(outcome="unavailable" if resp.unavailable else "error",
                           status=resp.status)
                led_fh.write(json.dumps(rec) + "\n")
                continue

            counts["ok"] += 1
            ex_fh.write(json.dumps({"show_trakt_id": sid, "show": trim(resp.data)}) + "\n")
            rec.update(outcome="ok", status=resp.status, from_cache=resp.from_cache)
            led_fh.write(json.dumps(rec) + "\n")

            if i % 100 == 0 or i == len(todo):
                ex_fh.flush()
                led_fh.flush()
                el = time.time() - started
                PROGRESS.write_text(json.dumps({
                    "updated_at": utcnow(), "fetched_this_run": i, "to_fetch": len(todo),
                    "counts": dict(counts),
                    "shows_per_min": round(i / el * 60, 1) if el else 0,
                    "client": client.summary(),
                }, indent=2))
                print(f"  {i}/{len(todo)}  ok={counts['ok']} "
                      f"unavail={counts['unavailable']} err={counts['error']}", flush=True)
    finally:
        ex_fh.close()
        led_fh.close()

    run = {
        "run_label": "step2_shows",
        "finished_at": utcnow(),
        "elapsed_min": round((time.time() - started) / 60, 2),
        "in_frame_shows": len(ids),
        "counts": counts,
        "stop_reason": stop_reason,
        "client_summary": client.summary(),
    }
    RUNLOG.write_text(json.dumps(run, indent=2))
    print(json.dumps(run, indent=2))
    return 1 if stop_reason else 0


if __name__ == "__main__":
    raise SystemExit(main())
