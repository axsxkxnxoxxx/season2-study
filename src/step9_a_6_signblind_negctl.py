"""Step 9, arm `a`: negative control for the SIGN-BLIND EMISSION guard.

WHAT IS BEING POLICED. `src/step9_a_2_emit.py` publishes every paired-movement interval this arm
measured, whatever its sign, and raises `SIGN-BLIND EMISSION FAILED` if the number published is
not the number measured. A guard that only ever passes is not a guard, so this control SHOWS IT
REJECTING the vector it exists to reject: the emitter's source is read, the withdrawn sign filter
(`if lo < 0 or hi < 0: continue`) is reintroduced IN MEMORY, and the mutated program is run
against scratch output paths. The guard must exit non-zero on that run and zero on the real one.

The emitter is DERIVED here, never copied to disk: a second copy of the emitter would be a second
definition of every figure it writes, which is this study's most frequent defect class.

Neither run re-draws the bootstrap. Both read processed/step9/a/measured.json, which is not
written by either.

Run record goes to logs/ (CLAUDE.md, "Where a check's CODE lives, and where its OUTPUT lives"):
    STEP_ARM=a python3 src/step9_a_6_signblind_negctl.py
"""
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile

ROOT = "/Users/alyanashantel/Documents/season2-study"
EMIT = os.path.join(ROOT, "src", "step9_a_2_emit.py")

# decisions/0129 ruling 1: a control that invokes another process must PASS STEP_ARM THROUGH
# rather than drop it, or the isolation channel reopens one level down. Inheritance carried it
# when the operator remembered to set it; this makes it explicit and supplies this arm's own
# value when they did not, so the child can never run un-scoped.
CHILD_ENV = dict(os.environ)
CHILD_ENV.setdefault("STEP_ARM", "a")

SKIP_ANCHOR = ("declared = []\n"
               "for spec, pop, outcome, lo, hi in MOVEMENTS:\n"
               "    iid = ")
SKIP_REINTRODUCED = ("declared = []\n"
                     "for spec, pop, outcome, lo, hi in MOVEMENTS:\n"
                     "    if lo < 0 or hi < 0:\n"
                     "        continue\n"
                     "    iid = ")

src = open(EMIT).read()
if src.count(SKIP_ANCHOR) != 1:
    raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: the emission loop this control mutates "
                     "was not found exactly once in " + EMIT + ". The control would otherwise "
                     "report clean while testing nothing.")

results = {}
with tempfile.TemporaryDirectory() as tmp:
    for label, body in (("guard_should_pass__unmutated", src),
                        ("guard_should_fail__sign_filter_reintroduced",
                         src.replace(SKIP_ANCHOR, SKIP_REINTRODUCED))):
        prog = body.replace(
            'OUT_JSON = os.path.join(ROOT, "artifacts", "step9-headline-a.json")',
            'OUT_JSON = %r' % os.path.join(tmp, label + ".json")
        ).replace(
            'os.path.join(ROOT, "logs", "step9", "a_validate.json")',
            '%r' % os.path.join(tmp, label + "-validate.json"))
        if 'OUT_JSON = %r' % os.path.join(tmp, label + ".json") not in prog:
            raise SystemExit("NEGATIVE CONTROL CANNOT BE BUILT: output path not redirected; the "
                             "control would overwrite the real deliverable.")
        path = os.path.join(tmp, label + ".py")
        open(path, "w").write(prog)
        r = subprocess.run([sys.executable, path], capture_output=True, text=True, cwd=ROOT,
                           env=CHILD_ENV)
        tail = [ln for ln in r.stdout.splitlines() if "paired movements measured" in ln]
        results[label] = {
            "exit_code": r.returncode,
            "counts_line": tail[0] if tail else None,
            "guard_message": next((ln for ln in (r.stdout + r.stderr).splitlines()
                                   if "SIGN-BLIND EMISSION FAILED" in ln), None),
        }

ok = (results["guard_should_pass__unmutated"]["exit_code"] == 0
      and results["guard_should_fail__sign_filter_reintroduced"]["exit_code"] != 0
      and results["guard_should_fail__sign_filter_reintroduced"]["guard_message"] is not None)

record = {
    "control": "src/step9_a_6_signblind_negctl.py",
    "guards": "src/step9_a_2_emit.py :: SIGN-BLIND EMISSION FAILED",
    "arm": "a", "step": "step9",
    "ran_at_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "runs_examined": 2,
    "step_arm_passed_to_children": CHILD_ENV.get("STEP_ARM"),
    "what_a_pass_means": ("the guard exits 0 on the emitter as it stands and NON-ZERO when the "
                          "withdrawn sign filter is reintroduced. A control that only observed "
                          "the passing run could not tell a working guard from one that cannot "
                          "fail."),
    "results": results,
    "ok": ok,
}
os.makedirs(os.path.join(ROOT, "logs", "step9"), exist_ok=True)
out = os.path.join(ROOT, "logs", "step9", "a_signblind_guard_negative_control.json")
with open(out, "w") as fh:
    json.dump(record, fh, indent=1)
    fh.write("\n")
print(json.dumps(record, indent=1))
print("wrote", out)
raise SystemExit(0 if ok else 1)
