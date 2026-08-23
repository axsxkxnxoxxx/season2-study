#!/usr/bin/env python3
"""Step 9, arm b -- REJECTION PROBE for the 0124 re-stamping guards.

WHY THIS EXISTS. decisions/0123 SS3, the Human Lead's ruling: A PRECONDITION THAT CANNOT FAIL ON
THE VECTOR IT POLICES IS NOT A CHECK -- it is worse than no check, because it occupies the slot
where a real one would sit. The 0124 layer in src/step9_b_6_stamp_superseded.py rests on two
claims that are exactly the shape of a vacuous guard if left unprobed:

    * that 0124 moved the CI endpoints AND NOTHING ELSE, so the protected families may stay
      unmarked; and
    * that every cell this script marks in the .md is a CI column of its own table.

A guard for either claim passes trivially on the file it was written against. So each is DRIVEN
TO FAILURE HERE, on a deliberately wrong input, and the failure message is printed. A guard that
cannot be shown failing is not trusted in this arm.

The probe runs on COPIES in a scratch directory. It never writes into artifacts/ or processed/.
Run:  python3 src/step9_b_12_restamp_selftest.py     (exit 0 = every guard fired as intended)
"""

import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import step9_b_6_stamp_superseded as M                                          # noqa: E402

SRC = {
    "COMMITTED_HEADLINE": M.COMMITTED_HEADLINE,
    "COMMITTED_MD": M.COMMITTED_MD,
    "COMMITTED_WORKING": M.COMMITTED_WORKING,
    "CORRECTED_HEADLINE": M.CORRECTED_HEADLINE,
    "CORRECTED_MD": M.CORRECTED_MD,
    "CORRECTED_WORKING": M.CORRECTED_WORKING,
}


ORIG_EMITTED = M.EMITTED_HEADLINE
ORIG_ROOT = M.ROOT


def fresh(tmp):
    """Copy every input the 0124 layer reads into tmp and repoint the module at them."""
    M.ROOT, M.EMITTED_HEADLINE = ORIG_ROOT, ORIG_EMITTED
    for name, path in SRC.items():
        dst = os.path.join(tmp, name.lower() + os.path.splitext(path)[1])
        shutil.copyfile(path, dst)
        setattr(M, name, dst)
    art = os.path.join(tmp, "artifacts")
    os.makedirs(art, exist_ok=True)
    shutil.copyfile(os.path.join(ROOT, M.EMITTED_HEADLINE), os.path.join(art, "h.json"))
    M.ROOT = tmp
    M.EMITTED_HEADLINE = "artifacts/h.json"
    return tmp


def run(fn):
    """Return (ok, message). ok=True means the layer completed without a hard stop."""
    try:
        fn({})
        return True, ""
    except SystemExit as e:                                                      # noqa: PERF203
        return False, str(e)


ORIG_MD_RULES = {k: dict(v) for k, v in M.MD_TABLE_RULES.items()}


def case(label, mutate, layer, expect_fragment):
    M.MD_TABLE_RULES = {k: dict(v) for k, v in ORIG_MD_RULES.items()}
    tmp = fresh(tempfile.mkdtemp(prefix="step9b0124-"))
    mutate(tmp)
    ok, msg = run(layer)
    hit = (not ok) and expect_fragment in msg
    print("  %-58s %s" % (label, "REJECTED as intended" if hit else "*** DID NOT FIRE ***"))
    if not hit:
        print("      completed without a hard stop" if ok else "      wrong message: " + msg[:300])
    else:
        print("      %s" % msg.split(".")[0][:160])
    shutil.rmtree(tmp, ignore_errors=True)
    return hit


def _edit_json(path, fn):
    d = json.load(open(path))
    fn(d)
    json.dump(d, open(path, "w"), indent=2, ensure_ascii=False)


def main():
    results = []

    print("CONTROL -- the guards must PASS on the real inputs, or a rejection proves nothing:")
    tmp = fresh(tempfile.mkdtemp(prefix="step9b0124-"))
    ok_json, msg_json = run(M.stamp_headline_0124)
    ok_md, msg_md = run(M.restamp_md_0124)
    print("  headline JSON layer  %s" % ("PASS" if ok_json else "HARD STOP: " + msg_json[:200]))
    print("  headline .md layer   %s" % ("PASS" if ok_md else "HARD STOP: " + msg_md[:200]))
    results += [ok_json, ok_md]
    shutil.rmtree(tmp, ignore_errors=True)

    print("\nREJECTION -- each guard driven to failure on a deliberately wrong input:")

    def protected_moved(tmp):
        # BOTH the preview and the emitted copy, so the preview-vs-emitted guard is satisfied
        # and the protected-family guard is the one under test. A probe that trips an EARLIER
        # guard proves that earlier guard and says nothing about this one.
        def f(d):
            b = d["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["b"]
            b["shares"]["never_started"]["numerator_pairs"] += 1
        _edit_json(M.CORRECTED_HEADLINE, f)
        _edit_json(os.path.join(tmp, "artifacts", "h.json"), f)
    results.append(case("a protected numerator moved", protected_moved,
                        M.stamp_headline_0124, "protected figures moved"))

    def unclaimed(tmp):
        def f(d):
            d["arms"][0]["headline"]["APPLY"]["a_brand_new_figure"] = 1.0
        _edit_json(M.COMMITTED_HEADLINE, f)
    results.append(case("a numeric family no rule claims", unclaimed,
                        M.stamp_headline_0124, "UNCLAIMED NAME IS A HARD STOP"))

    def stray_string(tmp):
        def f(d):
            d["arms"][0]["headline"]["APPLY"]["populations_differ_note"] += " CHANGED"
        _edit_json(M.CORRECTED_HEADLINE, f)
    results.append(case("a non-CI string moved", stray_string,
                        M.stamp_headline_0124, "not one of the CI-bearing string fields"))

    def pointer_lies(tmp):
        def f(d):
            b = d["arms"][0]["headline"]["APPLY"]["by_producing_arm"]["arms"]["b"]
            b["shares"]["never_started"]["ci"]["lower"] += 0.5
        _edit_json(os.path.join(tmp, "artifacts", "h.json"), f)
    results.append(case("the emitted artifact disagrees with the preview", pointer_lies,
                        M.stamp_headline_0124, "makes the pointer false"))

    def md_protected(tmp):
        lines = open(M.CORRECTED_MD).read().split("\n")
        for i, ln in enumerate(lines):
            if ln.startswith("| never started | **16.7231%**"):
                lines[i] = ln.replace("**16.7231%**", "**16.9999%**")
                break
        else:
            sys.exit("probe setup failed: the adopted-arm level row was not found")
        open(M.CORRECTED_MD, "w").write("\n".join(lines))
    results.append(case("a protected .md cell moved (a point estimate)", md_protected,
                        M.restamp_md_0124, "protected cells moved on the adopted arm"))

    def md_rule_incomplete(tmp):
        M.MD_TABLE_RULES = {k: ({"ci": v["ci"], "protected": v["protected"] - {6}}
                                if "horizon" in k else v)
                            for k, v in M.MD_TABLE_RULES.items()}
    results.append(case("a table rule that does not classify every column",
                        md_rule_incomplete, M.restamp_md_0124, "must be declared either CI or"))

    def md_unknown_table(tmp):
        lines = open(M.COMMITTED_MD).read().split("\n")
        for i, ln in enumerate(lines):
            if ln.startswith("| outcome | share (post-liveness) | pairs |"):
                lines[i] = ln.replace("| width |", "| spread |")
                break
        else:
            sys.exit("probe setup failed: the level-table header was not found")
        open(M.COMMITTED_MD, "w").write("\n".join(lines))
    results.append(case("an adopted-arm table whose header is not in the rules",
                        md_unknown_table, M.restamp_md_0124, "not in MD_TABLE_RULES"))

    print("\n%d of %d checks behaved as specified." % (sum(results), len(results)))
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
