"""Step 8, namespace `a`. THE RUN. One pipeline run, stages in order.

GATE. Adopts nothing. Zero API calls: every stage reads data already on disk.

This exists because decisions/0079 (B5) requires the POSITION-3 DROP SET to be written by the
SAME PIPELINE RUN that writes the analysis table, not by a helper script as a side file. D9 half
(b) is measured on those rows and cannot be computed without them, and their absence returns 0
SILENTLY -- a plausible-looking data finding rather than an error. A helper script's side file is
not a thing the next run is obliged to produce; a stage of this run is.

Order, and what each stage owes the next:

  1  scan          episode records -> pair-level primitives, drop-rule coverage counts
  2  positions     S1 completion walk (INDEPENDENT), the clock, positions 1-5,
                   and the POSITION-3 DROP SET DELIVERABLE
  4b slugs         show id -> slug map, which D9 needs for both keys
  3  table         positions 6 and 7 at W = 108, the 89-column analysis table
  4  arms          the per-arm required counts over the fixed W grid
  5  diagnostics   the required counts and the eight invariants; READS the drop set
  6  emit          the two artifacts, generated from the stage outputs

Usage: python src/step8_a_run.py [--skip-scan] [--skip-slugs]
  The two skips exist only for re-emitting after an artifact-text change; a compliance run passes
  neither, and the run record below states which stages actually executed.
"""
import json
import os
import subprocess
import sys
import time

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
OUT = os.path.join(ROOT, "processed/step8/a")
LOGS = os.path.join(ROOT, "logs")

STAGES = [
    ("1_scan", "step8_a_1_scan.py"),
    ("2_positions", "step8_a_2_positions.py"),
    ("4b_slugs", "step8_a_4b_slugs.py"),
    ("3_table", "step8_a_3_table.py"),
    ("4_arms", "step8_a_4_arms.py"),
    ("5_diagnostics", "step8_a_5_diagnostics.py"),
    ("6_emit", "step8_a_6_emit.py"),
]


def main():
    skip = set()
    if "--skip-scan" in sys.argv:
        skip.add("1_scan")
    if "--skip-slugs" in sys.argv:
        skip.add("4b_slugs")

    os.makedirs(OUT, exist_ok=True)
    os.makedirs(LOGS, exist_ok=True)
    record = {"step": 8, "instance": "a", "api_calls": 0,
              "what": "one Step 8 run: the analysis table and the position-3 drop set are written "
                      "by the same run (decisions/0079 B5)",
              "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "stages": []}
    for name, script in STAGES:
        if name in skip:
            record["stages"].append({"stage": name, "status": "SKIPPED BY FLAG"})
            print(f"[skip] {name}", flush=True)
            continue
        t0 = time.time()
        print(f"[run ] {name} ({script})", flush=True)
        p = subprocess.run([sys.executable, os.path.join(SRC, script)], cwd=SRC)
        dt = round(time.time() - t0, 1)
        record["stages"].append({"stage": name, "script": f"src/{script}",
                                 "returncode": p.returncode, "seconds": dt})
        if p.returncode != 0:
            record["status"] = f"FAILED at {name}"
            with open(os.path.join(LOGS, "step8_a_run.json"), "w") as fh:
                json.dump(record, fh, indent=2)
            sys.exit(p.returncode)
        print(f"[ok  ] {name} in {dt}s", flush=True)

    record["status"] = "COMPLETE"
    record["finished_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    with open(os.path.join(LOGS, "step8_a_run.json"), "w") as fh:
        json.dump(record, fh, indent=2)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
