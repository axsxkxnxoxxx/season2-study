"""Step 5 scan: extract the FULL parsed history store, including the record `id`.

READ ONLY. Zero network calls. Reads processed/step4/parsed/*.jsonl.gz only.

Why a new scan: processed/s1s2_scan.npz kept (user, show, season, number, ts) but
dropped the Trakt play `id`. The `id` is an auto-increment assigned at INSERT time,
so it is the only field on disk that carries information about when a record was
written, as opposed to when the user claims the watch happened. Contamination
detection needs exactly that contrast, so the id has to be rescanned.

Also unlike the S1/S2 scan this keeps every record, episode and movie, every
season. Backfill is an account-level act and the evidence for it is account-wide.
"""
from __future__ import annotations

import gzip
import json
import os
import re
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
PARSED = ROOT / "processed" / "step4" / "parsed"
OUT = Path(sys.argv[1])

RE_ID = re.compile(r'"id": (-?\d+)')
RE_NUM = re.compile(r'"number": (-?\d+|null)')
RE_SEA = re.compile(r'"season": (-?\d+|null)')
RE_SHOW = re.compile(r'"show_trakt": (-?\d+|null)')
RE_WAT = re.compile(r'"watched_at": (?:"([^"]*)"|null)')
RE_ACT = re.compile(r'"action": "([a-z_]+)"')

NULL_TS = np.iinfo(np.int64).min
ACTIONS = {"watch": 0, "checkin": 1, "scrobble": 2}


def parse_ts(s: str) -> int:
    try:
        return int(
            datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
    except Exception:
        return NULL_TS


def scan_one(args):
    idx, path = args
    ids, ts, kind, action, show, season, number = [], [], [], [], [], [], []
    n_lines = 0
    n_bad_id = 0
    n_missing_ts = 0
    n_unparsed_ts = 0
    unknown_actions = {}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            n_lines += 1
            m_id = RE_ID.search(line)
            if m_id is None:
                n_bad_id += 1
                continue
            ids.append(int(m_id.group(1)))

            m_w = RE_WAT.search(line)
            if m_w is None or m_w.group(1) is None:
                n_missing_ts += 1
                t = NULL_TS
            else:
                t = parse_ts(m_w.group(1))
                if t == NULL_TS:
                    n_unparsed_ts += 1
            ts.append(t)

            m_a = RE_ACT.search(line)
            a = m_a.group(1) if m_a else ""
            code = ACTIONS.get(a, -1)
            if code == -1:
                unknown_actions[a] = unknown_actions.get(a, 0) + 1
            action.append(code)

            if '"type": "episode"' in line:
                kind.append(1)
                m_show = RE_SHOW.search(line)
                m_sea = RE_SEA.search(line)
                m_num = RE_NUM.search(line)
                show.append(
                    int(m_show.group(1))
                    if m_show and m_show.group(1) != "null"
                    else -1
                )
                season.append(
                    int(m_sea.group(1)) if m_sea and m_sea.group(1) != "null" else -2147483648
                )
                number.append(
                    int(m_num.group(1)) if m_num and m_num.group(1) != "null" else -2147483648
                )
            else:
                kind.append(0)
                show.append(-1)
                season.append(-2147483648)
                number.append(-2147483648)

    n = len(ids)
    arr = {
        "user": np.full(n, idx, dtype=np.int32),
        "rid": np.asarray(ids, dtype=np.int64),
        "ts": np.asarray(ts, dtype=np.int64),
        "kind": np.asarray(kind, dtype=np.int8),
        "action": np.asarray(action, dtype=np.int8),
        "show": np.asarray(show, dtype=np.int64),
        "season": np.asarray(season, dtype=np.int32),
        "number": np.asarray(number, dtype=np.int32),
    }
    stats = {
        "lines": n_lines,
        "kept": n,
        "no_id": n_bad_id,
        "missing_watched_at": n_missing_ts,
        "unparsed_watched_at": n_unparsed_ts,
    }
    return idx, arr, stats, unknown_actions


def main():
    files = sorted(PARSED.glob("*.jsonl.gz"))
    print(f"{len(files)} parsed user files", flush=True)
    jobs = list(enumerate(files))
    parts = []
    total = {}
    unknown = {}
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        for k, (idx, arr, stats, ua) in enumerate(ex.map(scan_one, jobs, chunksize=8)):
            parts.append((idx, arr))
            for key, val in stats.items():
                total[key] = total.get(key, 0) + val
            for key, val in ua.items():
                unknown[key] = unknown.get(key, 0) + val
            if (k + 1) % 500 == 0:
                print(f"  {k+1}/{len(files)}", flush=True)

    parts.sort(key=lambda p: p[0])
    out = {
        key: np.concatenate([p[1][key] for p in parts])
        for key in ("user", "rid", "ts", "kind", "action", "show", "season", "number")
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    np.savez(OUT, **out)

    # username index: stays in processed/, never leaves it
    with open(OUT.parent / "user_index.json", "w") as fh:
        json.dump({"order": "sorted filename", "users": [f.name[: -len(".jsonl.gz")] for f in files]}, fh)

    meta = {"n_users": len(files), "totals": total, "unknown_actions": unknown}
    with open(str(OUT) + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(json.dumps(meta, indent=2))
    print(f"rows: {len(out['rid']):,}")


if __name__ == "__main__":
    main()
