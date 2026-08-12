"""Set `records` to null on discarded_over_tolerance ledger rows.

Those rows already use null for every other withheld field — `parse`,
`parsed_path`, and `is_data: false` — but carried `records: 0`. A consumer
reading `records` without also reading `outcome` sees a real zero, and per
CLAUDE.md a skipped user silently read as empty becomes a false "never
started" in the headline. `items_discarded` still records what was fetched
and thrown away, so no information is lost.

Rewrites processed/step4/pull_ledger.jsonl in place, atomically, and refuses
to proceed unless every other field on every row is byte-identical.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

LEDGER = Path("/Users/alyanashantel/Documents/season2-study/processed/step4/pull_ledger.jsonl")
TARGET = "discarded_over_tolerance"


def main():
    rows = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    before = len(rows)

    changed = 0
    for r in rows:
        if r.get("outcome") == TARGET and r.get("records") == 0:
            r["records"] = None
            changed += 1

    # verify: nothing but `records` on discarded rows may differ
    original = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    assert len(original) == len(rows) == before, "row count moved"
    for o, n in zip(original, rows):
        for k in set(o) | set(n):
            if k == "records" and o.get("outcome") == TARGET:
                continue
            assert o.get(k) == n.get(k), f"unexpected change on {k}"

    shutil.copy2(LEDGER, LEDGER.with_suffix(".jsonl.bak"))
    tmp = LEDGER.with_suffix(".jsonl.part")
    tmp.write_text("".join(json.dumps(r) + "\n" for r in rows))
    tmp.replace(LEDGER)

    after = [json.loads(l) for l in LEDGER.read_text().splitlines() if l.strip()]
    still_zero = sum(1 for r in after if r.get("outcome") == TARGET and r.get("records") == 0)
    now_null = sum(1 for r in after if r.get("outcome") == TARGET and r.get("records") is None)
    print(json.dumps({
        "rows": len(after), "rows_before": before, "rows_changed": changed,
        "discarded_rows_with_records_null": now_null,
        "discarded_rows_still_zero": still_zero,
        "backup": str(LEDGER.with_suffix(".jsonl.bak").name),
    }, indent=2))


if __name__ == "__main__":
    main()
