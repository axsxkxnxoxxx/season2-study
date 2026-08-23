#!/usr/bin/env python3
"""Step 9, arm `b`: RUN the controls and record what they returned.

WHY THIS IS A SCRIPT AND NOT A HAND-WRITTEN RECORD.
  A run record that asserts an exit status is a claim; one that CAPTURES it is a
  measurement. This invokes each control as a subprocess and writes back the exit
  status it actually received, so the record cannot drift from the run.

WHERE THINGS LIVE (decisions/0109). The CODE is here in src/ and is committed, so any
reviewer can see what was run. The OUTPUT goes to logs/ and never to artifacts/: a
control's exit status is not this arm's measurement of the study and does not belong in
a deliverable (CLAUDE.md, "A deliverable asserts only what its own arm measured").

SCOPE. Every path named below is this arm's own or shared spec. No arm-`a` path is read,
and the file arguments are literal -- there is no glob that could span arms.

Run:  python3 src/step9_b_8_controls.py
"""
import datetime
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "logs", "step9_b_controls_after_rerun.json")

CONTROLS = [
    {"id": "check_surfaces",
     "cmd": ["python3", "src/check_surfaces.py"],
     "what": "the shared propagation control, all eight surfaces, both halves"},
    {"id": "step8b_validate__corrected_emission",
     "cmd": ["python3", "src/step8b_validate.py",
             "artifacts/step9-headline-corrected-2026-08-21-b.json"],
     "what": "Step 8b's schema + semantic validator, against THIS arm's corrected emission"},
    {"id": "step9_b_reproduction_harness",
     "cmd": ["python3", "src/step9_b_0b_reproduce.py"],
     "what": "this arm's own reproduction: both corrected checks run against the DEFECTIVE "
             "vector and then against the corrected one. A non-zero exit means the "
             "reproduction did not complete as stated."},
]

FILES = [
    "src/step9_b_0_clock.py", "src/step9_b_0b_reproduce.py", "src/step9_b_1_compute.py",
    "src/step9_b_2_bootstrap.py", "src/step9_b_3_emit.py", "src/step9_b_4_md.py",
    "src/step9_b_5_working_figures.py", "src/step9_b_7_emit_corrected.py",
    "src/step9_b_8_controls.py",
    "processed/step9/b/stage1_counts.json", "processed/step9/b/stage2_bootstrap.json",
    "artifacts/step9-headline-corrected-2026-08-21-b.json",
    "artifacts/step9-headline-corrected-2026-08-21-b.md",
    "artifacts/step9-working-figures-corrected-2026-08-21-b.json",
    "artifacts/step9-headline-b.json", "artifacts/step9-headline-b.md",
    "artifacts/step9-working-figures-b.json",
]


def sha12(rel):
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


def main():
    rec = {
        "run": "Step 9, arm b -- controls run AFTER the last edit of the 2026-08-21 rerun",
        "generator": "src/step9_b_8_controls.py",
        "generator_sha256_12": sha12("src/step9_b_8_controls.py"),
        "recorded_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "why_this_is_in_logs": "decisions/0109: the CODE is in src/ and committed; the RUN "
                               "RECORD, including exit statuses, goes to logs/ and never to "
                               "artifacts/.",
        "exit_statuses_are_captured_not_asserted": True,
        "api_calls": 0,
        "adopts": "nothing",
        "controls": {},
    }
    for c in CONTROLS:
        p = subprocess.run(c["cmd"], cwd=ROOT, capture_output=True, text=True)
        tail = [ln for ln in (p.stdout or "").splitlines() if ln.strip()][-3:]
        rec["controls"][c["id"]] = {
            "command": " ".join(c["cmd"]),
            "what": c["what"],
            "exit_status": p.returncode,
            "stdout_last_lines": tail,
            "stderr_last_lines": [ln for ln in (p.stderr or "").splitlines() if ln.strip()][-3:],
        }
    rec["files_after_the_last_edit"] = {f: sha12(f) for f in FILES}
    with open(OUT, "w") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(json.dumps({k: {"exit_status": v["exit_status"]}
                      for k, v in rec["controls"].items()}, indent=1))
    print("run record:", os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
