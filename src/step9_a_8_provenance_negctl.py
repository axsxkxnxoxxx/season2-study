"""Step 9, arm `a`: negative control for the PROVENANCE GATE (decisions/0129 ruling 3).

WHAT IS BEING POLICED. `src/step9_a_4_working_figures.py` publishes
`$.source.produced_by_script_sha256_12`, asserting that `src/step9_a_1_compute.py` produced
`processed/step9/a/measured.json`. Before 0129 that hash was taken LIVE at transcription time and
nothing compared it with anything: the assertion went false the instant the producer was edited
without a stage-1 rerun, and the extract published it anyway. 0129 names the class -- an artifact
asserting which script produced it, where nothing checks the assertion is current, is a claim its
mechanism cannot deliver.

WHY THIS CONTROL EXISTS RATHER THAN A NOTE. A precondition that cannot fail on the vector it
polices is not a check (decisions/0123 SS3), and the gate PASSES today, so a run that observed
only the passing case could not tell a working gate from one that cannot fail. This control
therefore shows the defect REPRODUCED first and the gate REJECTING it after, on the same inputs:

  A  gate REMOVED in memory, producer edited   -> exits 0 and publishes the EDITED script's hash
                                                  beside an UNCHANGED working-file hash. Nothing
                                                  objects. This is the pre-0129 state.
  B  gate PRESENT, producer edited             -> non-zero, STALE PRODUCER, no file written.
  C  gate PRESENT, producer intact             -> 0. (Passes on the right vector.)
  D0 gate PRESENT, manifest redirected to an
     UNMODIFIED copy                           -> 0. Proves D's rejection is caused by the
                                                  perturbation and not by the redirection.
  D  gate PRESENT, manifest copy with n_frame
     perturbed by one                          -> non-zero. P2 shown rejecting.
  E  gate PRESENT, frame_support copy with one
     recorded input hash perturbed             -> non-zero. P3 shown rejecting.

THE EXTRACT IS DERIVED HERE, NEVER COPIED TO DISK PERMANENTLY, and every run's output path is
redirected into a private temporary directory: a second copy of the extract would be a second
definition of every figure it writes, and an un-redirected run would overwrite the real
deliverable.

NO BOOTSTRAP IS RE-DRAWN. Nothing here writes to processed/, and runs A and B restore the
producer byte-for-byte, verified by hash, in a `finally` -- if the restore cannot be verified the
control fails loudly rather than leaving the tree edited.

STEP_ARM is passed through to every child (0129 ruling 1): a control that invokes another process
and drops the variable reopens the isolation channel one level down.

Run record goes to logs/ (CLAUDE.md, "Where a check's CODE lives, and where its OUTPUT lives"):
    STEP_ARM=a python3 src/step9_a_8_provenance_negctl.py
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = "/Users/alyanashantel/Documents/season2-study"
EXTRACT = os.path.join(ROOT, "src", "step9_a_4_working_figures.py")
PRODUCER = os.path.join(ROOT, "src", "step9_a_1_compute.py")
MANIFEST = os.path.join(ROOT, "processed", "step9", "a", "boot_weights_manifest.json")
FRAME_SUPPORT = os.path.join(ROOT, "processed", "step9", "a", "frame_support.json")

REAL_OUT = 'OUT = os.path.join(ROOT, "artifacts", "step9-working-figures-a.json")'
GATE_CALL = "PROVENANCE = provenance_gate()"
GATE_REMOVED = ('PROVENANCE = {"status": "GATE REMOVED BY THE NEGATIVE CONTROL -- '
                'this is the pre-0129 behaviour"}')
MANIFEST_BIND = "PRODUCER_MANIFEST = os.path.join(ROOT, PRODUCER_MANIFEST_REL)"
FS_BIND = "FRAME_SUPPORT = os.path.join(ROOT, FRAME_SUPPORT_REL)"
# The derived program lives in a temp directory, so its own `__file__`-derived ROOT would point
# there. ROOT is PINNED to the repository so every path the gate reads is the path the real run
# reads. This is an environment fixup and nothing else: it changes no input the gate compares.
ROOT_BIND = "ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"

CHILD_ENV = dict(os.environ)
CHILD_ENV.setdefault("STEP_ARM", "a")          # 0129 ruling 1: pass it through, never drop it


def sha256_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build(src, tmp, label, drop_gate=False, manifest=None, frame_support=None):
    """Derive the extract in memory with its output redirected, and write the program to run."""
    out_json = os.path.join(tmp, label + ".json")
    if src.count(ROOT_BIND) != 1:
        raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: the ROOT binding was not found "
                         "exactly once in " + EXTRACT + ".")
    prog = src.replace(ROOT_BIND, "ROOT = %r" % ROOT).replace(REAL_OUT, "OUT = %r" % out_json)
    if "OUT = %r" % out_json not in prog:
        raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: output path not redirected for "
                         + label + "; the control would overwrite the real deliverable.")
    if drop_gate:
        if prog.count(GATE_CALL) != 1:
            raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: the gate call was not found "
                             "exactly once in " + EXTRACT + ".")
        prog = prog.replace(GATE_CALL, GATE_REMOVED)
    if manifest:
        if prog.count(MANIFEST_BIND) != 1:
            raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: manifest binding not found.")
        prog = prog.replace(MANIFEST_BIND, "PRODUCER_MANIFEST = %r" % manifest)
    if frame_support:
        if prog.count(FS_BIND) != 1:
            raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: frame-support binding not found.")
        prog = prog.replace(FS_BIND, "FRAME_SUPPORT = %r" % frame_support)
    path = os.path.join(tmp, label + ".py")
    open(path, "w").write(prog)
    return path, out_json


def run(path, out_json):
    r = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=ROOT,
                       env=CHILD_ENV)
    blob = r.stdout + r.stderr
    rec = {
        "exit_code": r.returncode,
        "output_file_written": os.path.exists(out_json),
        "gate_message": next((ln for ln in blob.splitlines()
                              if "PROVENANCE GATE" in ln or "STALE PRODUCER" in ln), None),
        "stderr_tail": blob.strip().splitlines()[-1] if blob.strip() else None,
    }
    if os.path.exists(out_json):
        d = json.load(open(out_json))
        rec["published_produced_by_script_sha256_12"] = \
            d["source"]["produced_by_script_sha256_12"]
        rec["published_working_file_sha256_12"] = d["source"]["working_file_sha256_12"]
    return rec


src = open(EXTRACT).read()
if src.count(GATE_CALL) != 1:
    raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: `" + GATE_CALL + "` not found exactly "
                     "once in " + EXTRACT + ". The control would otherwise report clean while "
                     "testing nothing.")

results = {}
producer_before = sha256_of(PRODUCER)
measured_sha12 = sha256_of(os.path.join(ROOT, "processed", "step9", "a", "measured.json"))[:12]
restored_ok = None
tmp = tempfile.mkdtemp(prefix="step9_a_provenance_")
try:
    original_bytes = open(PRODUCER, "rb").read()
    try:
        # --- the edit the gate exists to catch: the producer changes, stage 1 is NOT re-run ----
        with open(PRODUCER, "ab") as fh:
            fh.write(b"\n# TRANSIENT EDIT by src/step9_a_8_provenance_negctl.py; removed in the "
                     b"same run.\n")
        results["A_before_fix__gate_removed_producer_edited"] = run(
            *build(src, tmp, "A_before_fix__gate_removed_producer_edited", drop_gate=True))
        results["B_after_fix__gate_present_producer_edited"] = run(
            *build(src, tmp, "B_after_fix__gate_present_producer_edited"))
    finally:
        with open(PRODUCER, "wb") as fh:
            fh.write(original_bytes)
        restored_ok = sha256_of(PRODUCER) == producer_before

    if not restored_ok:
        raise SystemExit("NEGATIVE CONTROL FAILED TO RESTORE " + PRODUCER + ". Restore it from "
                         "git before running anything else.")

    results["C_after_fix__gate_present_producer_intact"] = run(
        *build(src, tmp, "C_after_fix__gate_present_producer_intact"))

    clean_manifest = os.path.join(tmp, "manifest_unmodified.json")
    shutil.copyfile(MANIFEST, clean_manifest)
    results["D0_control__manifest_redirected_unmodified"] = run(
        *build(src, tmp, "D0_control__manifest_redirected_unmodified", manifest=clean_manifest))

    bad_manifest = os.path.join(tmp, "manifest_n_frame_perturbed.json")
    m = json.load(open(MANIFEST))
    m["n_frame"] = int(m["n_frame"]) - 1
    json.dump(m, open(bad_manifest, "w"), indent=1)
    results["D_after_fix__manifest_n_frame_perturbed"] = run(
        *build(src, tmp, "D_after_fix__manifest_n_frame_perturbed", manifest=bad_manifest))

    bad_fs = os.path.join(tmp, "frame_support_input_hash_perturbed.json")
    f = json.load(open(FRAME_SUPPORT))
    k = sorted(f["read_from"])[0]
    f["read_from"][k] = "0" * 12
    json.dump(f, open(bad_fs, "w"), indent=1)
    results["E_after_fix__frame_support_input_hash_perturbed"] = run(
        *build(src, tmp, "E_after_fix__frame_support_input_hash_perturbed", frame_support=bad_fs))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

A = results["A_before_fix__gate_removed_producer_edited"]
B = results["B_after_fix__gate_present_producer_edited"]
reproduced = (A["exit_code"] == 0 and A["output_file_written"]
              and A.get("published_produced_by_script_sha256_12") != producer_before[:12]
              and A.get("published_working_file_sha256_12") == measured_sha12)
rejected = (B["exit_code"] != 0 and not B["output_file_written"]
            and B["gate_message"] is not None)
passes_clean = results["C_after_fix__gate_present_producer_intact"]["exit_code"] == 0
p2 = (results["D0_control__manifest_redirected_unmodified"]["exit_code"] == 0
      and results["D_after_fix__manifest_n_frame_perturbed"]["exit_code"] != 0)
p3 = results["E_after_fix__frame_support_input_hash_perturbed"]["exit_code"] != 0
ok = all([reproduced, rejected, passes_clean, p2, p3, restored_ok])

record = {
    "control": "src/step9_a_8_provenance_negctl.py",
    "guards": "src/step9_a_4_working_figures.py :: provenance_gate()",
    "decision": "0129 ruling 3",
    "arm": "a", "step": "step9",
    "ran_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "runs_examined": len(results),
    "producer_sha256_12_when_intact": producer_before[:12],
    "measured_json_sha256_12": measured_sha12,
    "producer_restored_and_verified": restored_ok,
    "step_arm_passed_to_children": CHILD_ENV.get("STEP_ARM"),
    "what_a_pass_means": (
        "the defect is REPRODUCED with the gate removed -- an edited producer's hash is "
        "published beside an unchanged working-file hash and nothing objects -- and REJECTED "
        "with the gate present, on the same inputs. A control that observed only the passing "
        "run could not tell a working gate from one that cannot fail (decisions/0123 SS3)."),
    "assertions": {
        "A_reproduces_the_pre_0129_acceptance": reproduced,
        "B_gate_rejects_the_stale_producer": rejected,
        "C_gate_passes_on_the_current_producer": passes_clean,
        "D_same_run_corroboration_rejects_and_its_control_passes": p2,
        "E_frame_support_input_currency_rejects": p3,
        "producer_restored": restored_ok,
    },
    "results": results,
    "ok": ok,
}
os.makedirs(os.path.join(ROOT, "logs", "step9"), exist_ok=True)
out = os.path.join(ROOT, "logs", "step9", "a_provenance_gate_negative_control.json")
with open(out, "w") as fh:
    json.dump(record, fh, indent=1)
    fh.write("\n")
print(json.dumps(record, indent=1))
print("wrote", out)
raise SystemExit(0 if ok else 1)
