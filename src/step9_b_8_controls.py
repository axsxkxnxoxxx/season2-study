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
     # ARM-SCOPED OUTPUT (decisions/0126). A SHARED CONTROL'S OUTPUT IS THE THIRD CROSS-ARM
     # CHANNEL: check_surfaces.py prints every surface's paths, including the other arm's, and
     # no scoping this arm controls can prevent that. STEP_ARM makes it print `<withheld>` for
     # paths belonging to another arm and report their number. THE COVERAGE AND THE EXIT CODE
     # ARE NEVER REDUCED -- nothing is excluded from the check, only from the printing. This
     # control captured the subprocess's stdout WITHOUT the variable set, which put the other
     # arm's paths into this arm's process; corrected here and reported.
     "env": {"STEP_ARM": "b"},
     "what": "the shared propagation control, all eight surfaces, both halves, run with "
             "STEP_ARM=b so another arm's paths are withheld from this arm's output "
             "(decisions/0126)"},
    {"id": "step8b_validate__corrected_emission",
     "cmd": ["python3", "src/step8b_validate.py",
             "artifacts/step9-headline-corrected-2026-08-21-b.json"],
     "what": "Step 8b's schema + semantic validator, against THIS arm's corrected emission",
     "note_on_the_expectation": (
         "THIS EXPECTATION CHANGED BECAUSE THE WORLD DID, AND THE OLD ONE IS RECORDED SO THE "
         "CHANGE IS NOT SILENT. Until schema v1.10.0 this control returned NON-ZERO and "
         "`behaved_as_expected` was recorded FALSE rather than redefined, because a control "
         "whose expectation is edited to match its result stops being a control. The non-zero "
         "was the `$defs/ci` typing item: `ci.lower`/`ci.upper` were typed as a percent on "
         "[0, 100] while a paired MOVEMENT is signed, so every negative movement endpoint "
         "matched none of the anyOf branches. decisions/0126 typed a CI endpoint BY ITS "
         "STATISTIC -- movements on $defs/pp, levels on $defs/percent -- and decisions/0127 "
         "recorded the migration. The item is CLOSED, not worked around: nothing was dropped, "
         "rescaled or sign-flipped, and the expectation is now zero because the defect is "
         "gone rather than because the bar moved.")},
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
    {"id": "step9_b_ordering_guard_rejection_probe",
     "cmd": ["python3", "src/step9_b_17_ordering_repro.py"],
     "what": "the ORDERING GUARD driven to failure on the condition that actually fired, "
             "constructed in both directions, and then shown PASSING on the current tree with "
             "its coverage printed. A guard shown only passing has not been shown to "
             "discriminate. A non-zero exit means it failed to reject, or passed vacuously."},
    {"id": "step9_b_three_rulings_reproduction_after",
     "cmd": ["python3", "src/step9_b_19_ruling_repro.py", "--after"],
     "what": "the three findings ruled 2026-08-25, re-measured in the CORRECTED state: all 24 "
             "position-5 level endpoints reachable in the artifacts, the three inherited leaves "
             "rewritten and the one that looks like a fourth kept, no typed NPOP literal -- and "
             "the new population read driven to failure on four wrong sources and accepted on "
             "the real one."},
    {"id": "step9_b_nothing_already_published_moved",
     "cmd": ["python3", "src/step9_b_20_publication_verify.py"],
     "what": "the 2026-08-25 emission compared leaf by leaf and BY CLASS against the same three "
             "paths at HEAD. Every numeric leaf must be unchanged, nothing lost, every added "
             "leaf inside a licensed class, and all three stamped originals byte-identical. A "
             "non-zero exit means a published figure moved."},
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
    "src/step9_b_16_leaf_diff.py", "src/step9_b_17_ordering_repro.py",
    "src/step9_b_19_ruling_repro.py", "src/step9_b_20_publication_verify.py",
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
        "run": "Step 9, arm b -- controls run AFTER the last edit of the 2026-08-25 emission "
               "under the Human Lead's three rulings of that date: publish the twelve "
               "position-5 level intervals that were measured and never emitted, rewrite the "
               "three inherited placeholder leaves that are false in a non-placeholder file, "
               "and turn the typed population constant into a read. AN EMISSION CHANGE: no "
               "bootstrap was re-run and no figure recomputed",
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
        env = dict(os.environ)
        env.update(c.get("env") or {})
        p = subprocess.run(c["cmd"], cwd=ROOT, capture_output=True, text=True, env=env)
        tail = [ln for ln in (p.stdout or "").splitlines() if ln.strip()][-3:]
        expect_nonzero = bool(c.get("expect_nonzero"))
        rec["controls"][c["id"]] = {
            "command": " ".join(c["cmd"]),
            "what": c["what"],
            "exit_status": p.returncode,
            # A DELIBERATE-FAILURE PROBE INVERTS WHAT A GOOD RESULT LOOKS LIKE, and a record
            # that prints only the number invites a reader to score it the usual way round.
            "expected_exit": "non-zero" if expect_nonzero else "zero",
            "env_overrides": c.get("env") or {},
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
