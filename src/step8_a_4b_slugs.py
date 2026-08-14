"""Step 8, namespace `a`. STAGE 4b of 5 — the show-id -> slug map D9 needs.

GATE. Adopts nothing. Zero API calls: reads processed/step4/parsed/*.jsonl.gz, which is the
already-fetched store.

D9 (Step 1 SS10.0b) asks for split-artifact counts on BOTH halves. Its signature is a pair of
show IDs in one user's sweep with complementary season coverage and the same title, so it needs
a title for every show ID in the sweep, including IDs outside the Step 2 frame. `show_slug` is
the only title-carrying field in the parsed store, so it is collected here.

Output: processed/step8/a/show_slugs.csv
"""
import gzip
import os
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

ROOT = Path("/Users/alyanashantel/Documents/season2-study")
PARSED = ROOT / "processed/step4/parsed"
OUT = ROOT / "processed/step8/a"

RE = re.compile(r'"show_slug": "([^"]*)", "show_trakt": (-?\d+|null)')


def one(path):
    seen = set()
    with gzip.open(path, "rt") as fh:
        for line in fh:
            m = RE.search(line)
            if m and m.group(2) != "null":
                seen.add((int(m.group(2)), m.group(1)))
    return seen


def main():
    files = sorted(PARSED.glob("*.jsonl.gz"))
    assert len(files) == 2549, f"{len(files)} parsed files"
    allseen = set()
    with ProcessPoolExecutor(max_workers=min(8, os.cpu_count() or 4)) as ex:
        for k, s in enumerate(ex.map(one, files, chunksize=16)):
            allseen |= s
            if (k + 1) % 500 == 0:
                print(f"{k+1}/{len(files)} files, {len(allseen)} (id, slug) pairs", flush=True)
    df = pd.DataFrame(sorted(allseen), columns=["show_trakt_id", "show_slug"])
    df.to_csv(OUT / "show_slugs.csv", index=False)
    print(f"{len(df)} (id, slug) pairs, {df.show_trakt_id.nunique()} distinct show ids")
    dup = df.show_trakt_id.duplicated(keep=False).sum()
    print(f"show ids carrying more than one slug: {dup}")


if __name__ == "__main__":
    main()
