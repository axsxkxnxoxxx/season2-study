"""Step 8 (instance b) -- stage 1b: the show_trakt -> show_slug map, for D9 only.

READ ONLY. ZERO network calls. Reads processed/step4/parsed/*.jsonl.gz.

D9's split signature needs "show titles or ids indicate the same title" across
show IDs that are NOT in the Step 2 frame -- a split puts S1 under one ID and S2
under another, and only one of the two need be in the frame. full_scan.npz keeps
the numeric show id and drops the slug, so the slug is rescanned here.

Detection is imperfect and the resulting count is a LOWER BOUND (Step 1 D9).

Out: processed/step8/b/show_slugs.json
"""
from __future__ import annotations

import gzip
import json
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
PARSED = ROOT / "processed" / "step4" / "parsed"
OUT = ROOT / "processed" / "step8" / "b"

RE_PAIR = re.compile(r'"show_slug": "([^"]*)", "show_trakt": (\d+)')


def scan(path: str) -> dict:
    seen: dict[int, str] = {}
    with gzip.open(path, "rt") as fh:
        for line in fh:
            m = RE_PAIR.search(line)
            if m is not None:
                sid = int(m.group(2))
                if sid not in seen:
                    seen[sid] = m.group(1)
    return seen


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(str(p) for p in PARSED.glob("*.jsonl.gz"))
    t = time.time()
    out: dict[int, str] = {}
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        for k, part in enumerate(ex.map(scan, files, chunksize=16)):
            out.update(part)
            if (k + 1) % 500 == 0:
                print(f"  {k+1}/{len(files)}  shows so far {len(out):,}"
                      f"  ({time.time()-t:.0f}s)", flush=True)
    (OUT / "show_slugs.json").write_text(json.dumps({str(k): v for k, v in out.items()}))
    print(f"{len(out):,} distinct show ids with a slug  ({time.time()-t:.0f}s)")


if __name__ == "__main__":
    main()
