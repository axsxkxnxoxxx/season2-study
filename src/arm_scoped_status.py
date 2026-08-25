#!/usr/bin/env python3
"""`git status`, arm-scoped. Decision 0129, closing the FIFTH isolation channel.

WHY THIS EXISTS. An arm ran `git status --porcelain` at the repository root and the other arm's
paths came back. TWO ARMS DISCLOSED IT INDEPENDENTLY, on the same day 0128 §1 predicted that a
fifth channel existed and that an arm's disclosure would be what found it. Neither used it.

`git status` is a SHARED CONTROL whose output no arm-side scoping can constrain: an arm has a
legitimate need to know whether its tree is clean, and `--porcelain -- <paths>` still forces the
arm to enumerate a scope it may get wrong. 0126 gave check_surfaces.py an arm-scoped mode for
exactly this reason and closed only that one control. This is the same fix for the next one.

WHAT IT DOES NOT DO. It does not hide the fact that other paths changed -- an arm must still be
able to tell a clean tree from a dirty one, so THE COUNT IS REPORTED AND THE EXIT CODE IS WHOLE.
Withholding the count would substitute the empty-result-equals-clean-result defect for a leak,
which is the trade 0126 refused and this refuses for the same reason.

Usage:  STEP_ARM=a python3 src/arm_scoped_status.py
        STEP_ARM unset prints everything -- the Human Lead's view.
"""
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_surfaces as CS                                         # noqa: E402


def main():
    out = subprocess.run(["git", "status", "--porcelain"],
                         capture_output=True, text=True, check=False)
    if out.returncode != 0:
        sys.exit(f"git status failed: {out.stderr.strip()}")
    rows = [ln for ln in out.stdout.split("\n") if ln.strip()]
    shown, withheld = [], {"a": 0, "b": 0}
    for ln in rows:
        path = ln[3:].split(" -> ")[-1]
        owner = CS.arm_of(path)
        if CS.STEP_ARM is None or owner is None or owner == CS.STEP_ARM:
            shown.append(ln)
        else:
            withheld[owner] += 1
    for ln in shown:
        print(ln)
    n = sum(withheld.values())
    print(f"\n-- {len(rows)} changed path(s) in the tree; {len(shown)} shown, {n} withheld {withheld}")
    if CS.STEP_ARM is None:
        print("-- STEP_ARM unset: every path printed (Human Lead view).")
    else:
        print(f"-- STEP_ARM={CS.STEP_ARM}: THE TOTAL ABOVE IS WHOLE. Nothing was excluded from the "
              f"COUNT, only from the LISTING. A withheld path belongs to another arm: if you needed "
              f"it, you needed that arm's work -- report it, do not seek it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
