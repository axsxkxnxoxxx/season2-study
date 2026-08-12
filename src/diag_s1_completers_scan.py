"""Scan the Step 4 parsed store and extract season-1 / season-2 episode records.

READ ONLY. Zero network calls. Reads processed/step4/parsed/*.jsonl.gz only.

Emits a compact binary intermediate to processed/ for the diagnostic to
vectorise over. Nothing is deduplicated here; dedup is a definitional act
(Step 1 Sec 2.1/2.2) and is applied in the analysis pass.
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

RE_NUM = re.compile(r'"number": (-?\d+|null)')
RE_SEA = re.compile(r'"season": (-?\d+|null)')
RE_SHOW = re.compile(r'"show_trakt": (-?\d+|null)')
RE_WAT = re.compile(r'"watched_at": (?:"([^"]*)"|null)')

EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


def parse_ts(s: str) -> int:
    # Trakt writes ISO-8601 UTC with a trailing Z. Seconds since epoch, int.
    try:
        return int(
            datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S")
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
    except Exception:
        return np.iinfo(np.int64).min


def scan_one(args):
    idx, path = args
    shows, seasons, numbers, ts = [], [], [], []
    n_lines = 0
    n_ep = 0
    n_s12_dropped_missing = 0
    n_missing_ts = 0
    n_nonpos_number = 0
    seen_ids = set()
    dup_ids = 0
    with gzip.open(path, "rt") as fh:
        for line in fh:
            n_lines += 1
            # fast reject: only season 1 and season 2 episode rows are needed
            if '"season": 1,' in line:
                sea = 1
            elif '"season": 2,' in line:
                sea = 2
            else:
                if '"type": "episode"' in line:
                    n_ep += 1
                continue
            n_ep += 1
            m_show = RE_SHOW.search(line)
            m_num = RE_NUM.search(line)
            if m_show is None or m_show.group(1) == "null" or m_num is None or m_num.group(1) == "null":
                n_s12_dropped_missing += 1
                continue
            num = int(m_num.group(1))
            if num < 1:
                n_nonpos_number += 1
                continue
            m_w = RE_WAT.search(line)
            if m_w is None or m_w.group(1) is None:
                n_missing_ts += 1
                t = np.iinfo(np.int64).min
            else:
                t = parse_ts(m_w.group(1))
            rid = line.partition('"id": ')[2].partition(',')[0]
            if rid in seen_ids:
                dup_ids += 1
            else:
                seen_ids.add(rid)
            shows.append(int(m_show.group(1)))
            seasons.append(sea)
            numbers.append(num)
            ts.append(t)
    n = len(shows)
    arr = {
        "user": np.full(n, idx, dtype=np.int32),
        "show": np.asarray(shows, dtype=np.int64),
        "season": np.asarray(seasons, dtype=np.int8),
        "number": np.asarray(numbers, dtype=np.int32),
        "ts": np.asarray(ts, dtype=np.int64),
    }
    stats = {
        "lines": n_lines,
        "episode_records": n_ep,
        "s12_kept": n,
        "s12_dropped_missing_show_or_number": n_s12_dropped_missing,
        "s12_number_lt_1": n_nonpos_number,
        "s12_missing_watched_at": n_missing_ts,
        "s12_duplicate_record_ids": dup_ids,
    }
    return idx, arr, stats


def main():
    files = sorted(PARSED.glob("*.jsonl.gz"))
    print(f"{len(files)} parsed user files", flush=True)
    jobs = list(enumerate(files))
    parts = []
    total = {}
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        for k, (idx, arr, stats) in enumerate(ex.map(scan_one, jobs, chunksize=8)):
            parts.append(arr)
            for key, val in stats.items():
                total[key] = total.get(key, 0) + val
            if (k + 1) % 250 == 0:
                print(f"  {k+1}/{len(files)}", flush=True)

    out = {
        key: np.concatenate([p[key] for p in parts]) for key in ("user", "show", "season", "number", "ts")
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    np.savez(OUT, **out)
    meta = {
        "n_users": len(files),
        "user_files_sha_order": "sorted filename order; index is positional and carries no identity",
        "totals": total,
    }
    with open(str(OUT) + ".meta.json", "w") as fh:
        json.dump(meta, fh, indent=2)
    print(json.dumps(total, indent=2))
    print(f"rows kept: {len(out['user']):,}")


if __name__ == "__main__":
    main()
