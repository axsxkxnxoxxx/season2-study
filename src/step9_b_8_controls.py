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
     "what": "Step 8b's schema + semantic validator, against THIS arm's corrected emission",
     "note_on_a_nonzero_that_is_not_new": (
         "This control returns non-zero, and `behaved_as_expected` is recorded FALSE rather "
         "than redefined, because a control whose expectation is edited to match its result "
         "stops being a control. THE NON-ZERO IS THE OPEN `$defs/ci` TYPING ITEM, which is the "
         "Human Lead's and which the decisions/0125 rerun was instructed not to touch: "
         "`ci.lower`/`ci.upper` are typed as a percent in [0, 100] while a paired MOVEMENT is "
         "signed, so every negative movement endpoint matches none of the anyOf branches. "
         "MEASURED, NOT ASSUMED, ACROSS THIS RERUN: 11 schema errors before and 11 after, at "
         "the SAME eleven paths, with `checks_failed` 0 in both -- the 43 semantic checks all "
         "pass. Nothing was dropped, rescaled or sign-flipped to make it go away.")},
    {"id": "step9_b_reproduction_harness",
     "cmd": ["python3", "src/step9_b_0b_reproduce.py"],
     "what": "this arm's own reproduction: both corrected checks run against the DEFECTIVE "
             "vector and then against the corrected one. A non-zero exit means the "
             "reproduction did not complete as stated."},
    {"id": "step9_b_frame_and_draw_order_reproduction",
     "cmd": ["python3", "src/step9_b_9_frame_repro.py"],
     "what": "decisions/0124: the CURRENT frame and draw order measured off the committed "
             "source, then the RULED ones, then both designs run and the change shown. It "
             "ASSERTS that no point estimate and no per-account pair total moves between the "
             "two designs, so a non-zero exit means the ruling moved more than an interval."},
    {"id": "step9_b_pairing_evidence",
     "cmd": ["python3", "src/step9_b_10_pairing_evidence.py"],
     "what": "decisions/0124 SS5: the pairing evidence RE-TAKEN on the new weights. It "
             "reproduces all 48 published endpoints from the recorded replicate set and then "
             "runs the same comparison against a deliberately UNPAIRED construction, which it "
             "must reject on every interval. A non-zero exit means either the reproduction "
             "failed or the probe passed -- and a probe that passes is not a test."},
    {"id": "step9_b_draw_mechanism_reproduction",
     "cmd": ["python3", "src/step9_b_15_mechanism_repro.py"],
     "what": "decisions/0125: the COMMITTED draw call read from git and the RULED one measured "
             "beside it, both drawn under one seed and compared element-wise; the chunking "
             "re-measured rather than cited; and the comparison shown REJECTING a different "
             "seed and the superseded sampler while ACCEPTING the ruled mechanism at another "
             "chunking. A non-zero exit means the defect did not reproduce, the chunking DOES "
             "determine the output, or a probe did not behave as required."},
    {"id": "step9_b_leaf_diff_of_the_finished_files",
     "cmd": ["python3", "src/step9_b_16_leaf_diff.py"],
     "what": "the leaf-by-leaf diff of the FINISHED emitted files against the same paths at the "
             "commit that preceded this rerun. Every moved numeric leaf must be a CI endpoint, "
             "a CI-derived ratio, or a leaf of the emission's own run record -- a declared "
             "class listed by path. A non-zero exit means something else moved."},
    {"id": "step9_b_leaf_diff_probe",
     "cmd": ["python3", "src/step9_b_16_leaf_diff.py", "--probe"],
     "what": "THE SAME DIFF, SHOWN FAILING. A protected point estimate is moved in memory and "
             "the identical classification must report it. THIS CONTROL IS EXPECTED TO EXIT "
             "NON-ZERO: exit 0 would mean the diff passed on a vector carrying a moved figure, "
             "which is the one outcome that would make its clean run worthless.",
     "expect_nonzero": True},
]

FILES = [
    "src/step9_b_0_clock.py", "src/step9_b_0b_reproduce.py", "src/step9_b_1_compute.py",
    "src/step9_b_2_bootstrap.py", "src/step9_b_3_emit.py", "src/step9_b_4_md.py",
    "src/step9_b_5_working_figures.py", "src/step9_b_7_emit_corrected.py",
    "src/step9_b_8_controls.py", "src/step9_b_9_frame_repro.py",
    "src/step9_b_10_pairing_evidence.py", "src/step9_b_15_mechanism_repro.py",
    "src/step9_b_16_leaf_diff.py",
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
        "run": "Step 9, arm b -- controls run AFTER the last edit of the 2026-08-24 rerun "
               "under decisions/0125 (the draw MECHANISM), which is one level below the "
               "2026-08-23 rerun under decisions/0124 (the frame and the draw order)",
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
        expect_nonzero = bool(c.get("expect_nonzero"))
        rec["controls"][c["id"]] = {
            "command": " ".join(c["cmd"]),
            "what": c["what"],
            "exit_status": p.returncode,
            # A DELIBERATE-FAILURE PROBE INVERTS WHAT A GOOD RESULT LOOKS LIKE, and a record
            # that prints only the number invites a reader to score it the usual way round.
            "expected_exit": "non-zero" if expect_nonzero else "zero",
            "behaved_as_expected": (p.returncode != 0) if expect_nonzero
                                   else (p.returncode == 0),
            "stdout_last_lines": tail,
            "stderr_last_lines": [ln for ln in (p.stderr or "").splitlines() if ln.strip()][-3:],
        }
    rec["files_after_the_last_edit"] = {f: sha12(f) for f in FILES}
    with open(OUT, "w") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    rec["every_control_behaved_as_expected"] = all(
        v["behaved_as_expected"] for v in rec["controls"].values())
    print(json.dumps({k: {"exit_status": v["exit_status"],
                          "expected_exit": v["expected_exit"],
                          "behaved_as_expected": v["behaved_as_expected"]}
                      for k, v in rec["controls"].items()}, indent=1))
    print("run record:", os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
